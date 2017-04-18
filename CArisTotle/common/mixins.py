class AutoReprMixin:
    def __repr__(self):
        substrings = ("{!s}={!r}".format(k, v) for k, v in self.__dict__.items() if not k.startswith('_'))
        substrings = (substring if len(substring) < 42 else (substring[:38] + "...'") for substring in substrings)
        return "{!s}({!s})".format(self.__class__.__name__, ', '.join(substrings))
