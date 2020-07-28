class KnownError(Exception):
    """
    Base class for errors in the errorutil module.
    """

    def __init__(self, msg, hint):
        super().__init__(msg + ("" if hint is None else ("; " + hint)))
        self.hint = hint


class BlankCell(KnownError):
    """
    Raised when a cell in an input table is supposed to contain a value
    but is blank instead. More helpful than an error message complaining about
    being unable to find ''.
    """

    def __init__(self, cell_type, source, hint=None):
        super().__init__(
            "Blank {} cell found in file {}".format(cell_type, source), hint)
        self.cell_type = cell_type
        self.source = source


class FailedLookup(KnownError):
    """
    Raised when a value from one data source refers to a value in another data
    source, but that value is missing. Covers what would be a foreign key
    violation in a database system.
    """

    def __init__(self, key_type, full_key, key_source, lookup_location, hint=None):
        super().__init__(
            "Couldn't find the {} {} (defined in {}) anywhere in {}"
                .format(key_type, full_key, key_source, lookup_location), hint)
        self.key_type = key_type
        self.full_key = full_key
        self.key_source = key_source
        self.lookup_location = lookup_location


class MissingColumn(KnownError):
    """
    Raised when a required column in a data table is missing.
    """

    def __init__(self, col_name, available_cols, source, hint=None):
        super().__init__(
            "No column {} in {}; available columns are {}"
            .format(col_name, source, ", ".join(available_cols)), hint)
        self.col_name = col_name
        self.available_cols = available_cols
        self.source = source


class InvalidSetting(KnownError):
    """
    Raised when a setting has been given an invalid value.
    """

    def __init__(self, setting_name, setting_value, hint=None):
        super().__init__(
            "The setting {} cannot equal {}".format(setting_name, setting_value),
            hint
        )
        self.setting_name = setting_name
        self.setting_value = setting_value
