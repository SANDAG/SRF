from psycopg2 import ProgrammingError
from psycopg2.extras import execute_batch

_NO_ARG = object()


class Querier:
    def __init__(self, connect, debug_log=None, cursor_factory=None, **kwargs):
        self.connect = connect
        self.debug_log = debug_log
        self.cursor_factory = cursor_factory
        self.kwargs = kwargs
        self._entered = False
    
    def __enter__(self):
        self._conn = self.connect()
        self._entered = True
        return self

    # noinspection PyBroadException
    def __exit__(self, *args):
        try:
            self._entered = False
            self._conn.close()
        except Exception:
            pass
    
    def query(self, query, debug_log=_NO_ARG, cursor_factory=_NO_ARG, **kwargs):
        with self.transaction(cursor_factory) as tr:
            return tr.query(query, debug_log, **kwargs)
    
    def query_many(self, query, argslist, debug_log=_NO_ARG, **kwargs):
        with self.transaction() as tr:
            tr.query_many(query, argslist, debug_log, **kwargs)

    def query_external(self, fname, start=None, end=None, debug_log=_NO_ARG, **kwargs):
        with self.transaction() as tr:
            tr.query_external(fname, start, end, debug_log, **kwargs)

    def callproc(self, procname, parameters=_NO_ARG, debug_log=_NO_ARG, **kwargs):
        with self.transaction() as tr:
            tr.callproc(procname, parameters, debug_log, **kwargs)

    def dump_to_csv(self, query, fname, debug_log=_NO_ARG, **kwargs):
        with self.transaction() as tr:
            tr.dump_to_csv(query, fname, debug_log, **kwargs)

    def load_from_csv(self, table, fname, header=True, debug_log=_NO_ARG, **kwargs):
        with self.transaction() as tr:
            tr.load_from_csv(table, fname, header, debug_log, **kwargs)
    
    def transaction(self, cursor_factory=_NO_ARG, **kwargs):
        return Transaction(self, cursor_factory, **kwargs)

    def vacuum(self, table, analyze=False, **kwargs):
        with self.connect() as conn:
            conn.autocommit = True
            cur = conn.cursor(cursor_factory=self.cursor_factory)
            full_kwargs = dict(self.kwargs)
            full_kwargs.update(kwargs)
            query = "vacuum analyze {}" if analyze else "vacuum {}"
            query = query.format(table).format(**full_kwargs)
            cur.execute(query)


class Transaction:
    def __init__(self, querier, cursor_factory, **kwargs):
        self._querier = querier
        if cursor_factory is _NO_ARG:
            cursor_factory = querier.cursor_factory
        self._cursor_factory = cursor_factory
        self._kwargs = kwargs
        self._collapsed_entry = False
    
    def __enter__(self):
        if not self._querier._entered:
            self._querier.__enter__()
            self._collapsed_entry = True
        self._conn = self._querier._conn
        self._conn.__enter__()
        self._cur = self._conn.cursor(cursor_factory=self._cursor_factory)
        self._cur.__enter__()
        return self

    # noinspection PyBroadException
    def __exit__(self, *args):
        try:
            try:
                self._cur.__exit__(*args)
            finally:
                try:
                    self._conn.__exit__(*args)
                finally:
                    if self._collapsed_entry:
                        self._querier.__exit__(*args)
        except Exception:
            pass
    
    def query(self, query, debug_log=_NO_ARG, **kwargs):
        kwargs = self._full_kwargs(kwargs)
        debug_log = self._real_debug_log(debug_log)
        query = query.format(**kwargs)
        
        debug_log.log("Executing query:")
        debug_log.log(self._cur.mogrify(query, kwargs).decode())
        self._draw_line(debug_log)
        
        self._cur.execute(query, kwargs)
        try:
            result = self._cur.fetchall()
            return result
        except ProgrammingError:
            return None
    
    def query_many(self, query, argslist, debug_log=_NO_ARG, **kwargs):
        kwargs = self._full_kwargs(kwargs)
        debug_log = self._real_debug_log(debug_log)
        query = query.format(**kwargs)
        
        debug_log.log("Executing batch query:")
        debug_log.log(query)
        self._draw_line(debug_log)
        
        execute_batch(self._cur, query, argslist)
    
    def query_external(self, fname, start=None, end=None, debug_log=_NO_ARG, **kwargs):
        result = None
        
        with open(fname, encoding="utf-8-sig") as fin:
            lines = list(fin)
            it = iter(lines)
            if start is not None:
                for line in it:
                    line = line.strip()
                    if line.startswith("--"):
                        line = line[2:].strip()
                        if line == start:
                            break

            finished = False
            while not finished:
                query = ""
                for line in it:
                    if line.startswith("--"):
                        if end is not None:
                            comment = line[2:].strip()
                            if comment == end:
                                finished = True
                                break
                    else:
                        if line.strip():
                            query += line
                else:
                    finished = True
                
                if not query.strip():
                    continue
                
                new_result = self.query(query, debug_log, **kwargs)
                if new_result is not None:
                    result = new_result
                    
        return result

    def callproc(self, procname, parameters=_NO_ARG, debug_log=_NO_ARG, **kwargs):
        kwargs = self._full_kwargs(kwargs)
        debug_log = self._real_debug_log(debug_log)
        if parameters is _NO_ARG:
            parameters = []
        procname = procname.format(**kwargs)

        debug_log.log("Calling procedure {} with parameters {}".format(procname, parameters))
        self._draw_line(debug_log)

        self._cur.callproc(procname, parameters)
    
    def dump_to_csv(self, query, fname, debug_log=_NO_ARG, **kwargs):
        kwargs = self._full_kwargs(kwargs)
        debug_log = self._real_debug_log(debug_log)
        query = self._cur.mogrify(query.format(**kwargs), kwargs).decode()
        fname = fname.format(**kwargs)
        
        debug_log.log("Dumping to file {} results of query:".format(fname))
        debug_log.log(query)
        self._draw_line(debug_log)
        
        with open(fname, "w") as outf:
            self._cur.copy_expert(
                    "copy ({}) to stdout csv header".format(query), outf)
    
    def load_from_csv(self, table, fname, header=True, debug_log=_NO_ARG, **kwargs):
        kwargs = self._full_kwargs(kwargs)
        debug_log = self._real_debug_log(debug_log)
        table = table.format(**kwargs)
        fname = fname.format(**kwargs)
        
        debug_log.log("Loading file {} into table {}".format(fname, table))
        self._draw_line(debug_log)
        
        with open(fname, "r") as outf:
            self._cur.copy_expert(
                    "copy {} from stdin csv{}".format(table, " header" if header else ""), outf)
    
    def _full_kwargs(self, kwargs):
        full_kwargs = dict(self._querier.kwargs)
        full_kwargs.update(self._kwargs)
        full_kwargs.update(kwargs)
        return full_kwargs
    
    def _real_debug_log(self, debug_log):
        if debug_log is _NO_ARG:
            debug_log = self._querier.debug_log
        if debug_log is None:
            debug_log = NullLogger()
        return debug_log

    @staticmethod
    def _draw_line(debug_log):
        return debug_log.log("-" * 80)

        
class NullLogger:
    def log(self, text):
        pass
