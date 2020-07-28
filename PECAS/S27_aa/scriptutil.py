# Utility routines for model calibration/utility scripts

import errno
import shutil
from typing import Optional, Iterable, List, Sequence
from itertools import chain

import errorutil as eu


# Determines the file name that would be used as the backup by the backup()
# function, without actually backing up the file.
def backup_name(fname, itnum):
    return suffix_name(fname, "_" + str(itnum) + "_")


# Creates an iteration-tagged backup of the specified file.
# The backup has the iteration number, bracketed by underscores,
# between the base file name and the extension.
def backup(fname, itnum):
    shutil.copyfile(fname, backup_name(fname, itnum))


# Inserts the specified suffix into the given filename immediately before
# the dot and extension. For example, suffix_name("foo.txt", "bar") returns
# "foobar.txt".
def suffix_name(fname, suffix):
    bits = fname.split(".")
    if len(bits) == 1:
        return fname + suffix
    else:
        return ".".join(bits[0:-1]) + suffix + "." + bits[-1]


# Pluralizes a noun if n is not 1. The plural form is given by plur; if omitted,
# the plural is the singular with "s" appended.
def pl(n, sing, plur=None):
    if n == 1:
        return sing
    elif plur is None:
        return sing + "s"
    else:
        return plur


# "Inclusive range" - both start and stop are inclusive, which is more intuitive
# for some applications.
def irange(start, stop):
    return list(range(start, stop + 1))


# Returns the index of the specified column name in the specified list of column names.
# The source parameter is the name of the source that is being read (e.g. a CSV filename)
# so that helpful error messages can be produced on missing columns.
def colindex(source: str, available_cols: Sequence[str], col: str) -> int:
    try:
        return available_cols.index(col)
    except ValueError:
        raise eu.MissingColumn(col, available_cols, source)


# Returns the index of the specified column names in the specified list of column names.
# The source parameter is the name of the source that is being read (e.g. a CSV filename)
# so that helpful error messages can be produced on missing columns.
def colindices(source: str, available_cols: Sequence[str], *cols: str) -> List[int]:
    return [colindex(source, available_cols, col) for col in cols]


# Returns the indices of the specified values in the specified list.
# Useful for finding column positions in a CSV file with headers.
# Not optimized in any way, so only good for small lists.
def indices(alist, *values):
    return [alist.index(value) for value in values]


# Returns the elements of the row indicated by the list of column indices.
# This is designed so you can directly pass in the result of colindices.
def elements(row: Sequence[str], cols: Sequence[int]):
    return [row[i] for i in cols]


# Converts a string to a bool the way you'd expect, rather than the stupid
# way that the built-in bool() function does it.
def tobool(string):
    lower = string.lower()
    if lower == "true":
        return True
    elif lower == "false":
        return False
    else:
        raise ValueError(string)


# Returns value forced to be between minvalue and maxvalue inclusive.
def clip(value, minvalue, maxvalue):
    if value < minvalue:
        value = minvalue
    if value > maxvalue:
        value = maxvalue
    return value


# Returns a value from a nested dictionary indexed by the specified keys. Returns
# the default value if a key is absent at any level.
def get_in(a_dict, keys, default):
    cursor = a_dict
    for key in keys:
        if key not in cursor:
            return default
        cursor = cursor[key]
    return cursor


# Adds a mapping to a nested dictionary. The keys are used to index into each layer
# of the dictionary. If a key at any level is absent, it is automatically created.
def assoc_in(a_dict, keys, value):
    cursor = a_dict
    for key in keys[:-1]:
        if key not in cursor:
            cursor[key] = {}
        cursor = cursor[key]
    cursor[keys[-1]] = value


# Takes a nested dictionary and flips the order of the outermost two nests.
# For example, if ndict["foo"]["bar"] == "spam" in the original dictionary,
# then flipkeys(ndict)["bar"]["foo"] == "spam". The result is always a plain
# Python dictionary, regardless of the class of the argument.
def flipkeys(ndict):
    result = {}
    for key1, indict in ndict.items():
        for key2, value in indict.items():
            inresult = result.setdefault(key2, {})
            inresult[key1] = value
    return result


# Combination of zip and iteritems, used for stepping through several parallel
# dictionaries that have the same keys. Returns an iterable of 2-tuples. The
# first element is the key. The second is itself a tuple containing the value
# corresponding to that key in each of the dictionaries. If the key sets are
# not equal, only the keys that are present in all of the dictionaries are
# returned. The first dictionary must allow iteration over its keys; the others
# only need to support item access by key, so any object with a suitable
# __getitem__ method is allowed.
def zipitems(*dicts):
    for key in dicts[0]:
        try:
            yield key, tuple([d[key] for d in dicts])
        except KeyError:
            pass


# Reverses zip: turns a list of tuples into a tuple of lists
def unzip(a_list):
    return tuple(list(x) for x in zip(*a_list))


# Opens a file for writing, as if by open(fname, "w"). If the file cannot be
# opened (because it is locked or it is a directory, for example), then this
# function will try appending " (1)" to the filename. If that also fails, then
# it will try appending " (2)", and so on. Eventually, this function will
# return a valid file object. This function will immediately raise an IOError
# if the directory being written to does not exist.
# Set binary=True to use binary mode ("wb") instead of text mode.
def smart_open(fname, binary=False):
    mode = "wb" if binary else "w"
    try:
        return open(fname, mode)
    except IOError as e:
        if e.errno != errno.EACCES:
            raise e
        i = 1
        while True:
            bracname = suffix_name(fname, " (" + str(i) + ")")
            try:
                return open(bracname, mode)
            except IOError:
                if e.errno != errno.EACCES:
                    raise e
                i += 1


# Returns the best match to the specified value from among the specified options,
# or None if there are no good matches.
# The tolerance parameter indicates how closely the value has to match -
# 0 means anything goes, 1 means exact matches only (up to case differences).
def best_match(value: str, options: Iterable[str], tolerance=0.6) -> Optional[str]:
    if value in options:
        return value
    else:
        import difflib
        def match(x):
            return difflib.SequenceMatcher(None, value, x).ratio()
        suggestion = max(options, key=match)
        if match(suggestion) > tolerance:
            return suggestion


# An unmodifiable dictionary-like object that maps everything to itself.
# It "contains" all possible elements.
# Retrieving or iterating over the keys, values, or items is undefined,
# since an IdDict "contains" infinitely many elements in an unspecified order.
# If a dictionary is passed to the constructor, its mappings will be used
# where possible, with all other keys still mapped to themselves.
class IdDict:
    # noinspection PyDefaultArgument
    def __init__(self, mappings={}):
        self.mappings = dict(mappings)

    def __getitem__(self, key):
        if key in self.mappings:
            return self.mappings[key]
        else:
            return key

    def __contains__(self, key):
        return True


# Class that automatically interprets a comma-separated list of ranges, like 2-5,8,27-32
class RangeList:
    def __init__(self, arg):
        def parse_range(r):
            if len(r) == 0:
                return []
            parts = r.split("-")
            if len(parts) > 2:
                raise ValueError("Invalid range: {}".format(r))
            return range(int(parts[0]), int(parts[-1]) + 1)

        self.list = list(dict.fromkeys(chain.from_iterable(map(parse_range, arg.split(",")))))
