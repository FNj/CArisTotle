class AutoReprMixin:
    # def __repr__(self):
    #     substrings = ("{!s}={!s}".format(k, v) for k, v in self.__dict__.items() if not k.startswith('_'))
    #     substrings = [substring if len(substring) < 42 else (substring[:38] + "...'") for substring in substrings]
    #     substrings.sort(key=(lambda substring: len(substring)))
    #     return "{!s}({!s})".format(self.__class__.__name__, ', '.join(substrings))
    #
    # def __str__(self):
    #     return self.__class__.__name__ + ' ' + str(self.id)

    pass  # TODO: Decide what to do with this
