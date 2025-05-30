import sys


class ComparableMixin:
    """Implements rich operators for an object."""

    def _cmpkey(self):
        raise NotImplementedError("Class must implement _cmpkey method")

    def _compare(self, other, method):
        try:
            return method(self._cmpkey(), other._cmpkey())
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other". Try the reverse comparison
            return NotImplemented

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)


class BlobComparableMixin(ComparableMixin):
    """Allow blob objects to be comparable with both strings and blobs."""

    def _compare(self, other, method):
        if isinstance(other, (str, bytes)):
            # Just compare with the other string
            return method(self._cmpkey(), other)
        return super()._compare(other, method)


class StringlikeMixin:
    """Make blob objects behave like Python strings.

    Expects that classes that use this mixin to have a _strkey() method that
    returns the string to apply string methods to. Using _strkey() instead
    of __str__ ensures consistent behavior between Python 2 and 3.
    """

    def _strkey(self) -> str:
        raise NotImplementedError("Class must implement _strkey method")

    def __repr__(self):
        """Returns a string representation for debugging."""
        class_name = self.__class__.__name__
        text = str(self)
        return f'{class_name}("{text}")'

    def __str__(self):
        """Returns a string representation used in print statements
        or str(my_blob)."""
        return self._strkey()

    def __len__(self):
        """Returns the length of the raw text."""
        return len(self._strkey())

    def __iter__(self):
        """Makes the object iterable as if it were a string,
        iterating through the raw string's characters.
        """
        return iter(self._strkey())

    def __contains__(self, sub):
        """Implements the `in` keyword like a Python string."""
        return sub in self._strkey()

    def __getitem__(self, index):
        """Returns a  substring. If index is an integer, returns a Python
        string of a single character. If a range is given, e.g. `blob[3:5]`,
        a new instance of the class is returned.
        """
        if isinstance(index, int):
            return self._strkey()[index]  # Just return a single character
        else:
            # Return a new blob object
            return self.__class__(self._strkey()[index])

    def find(self, sub, start=0, end=sys.maxsize):
        """Behaves like the built-in str.find() method. Returns an integer,
        the index of the first occurrence of the substring argument sub in the
        sub-string given by [start:end].
        """
        return self._strkey().find(sub, start, end)

    def rfind(self, sub, start=0, end=sys.maxsize):
        """Behaves like the built-in str.rfind() method. Returns an integer,
        the index of the last (right-most) occurrence of the substring argument
        sub in the sub-sequence given by [start:end].
        """
        return self._strkey().rfind(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        """Like blob.find() but raise ValueError when the substring
        is not found.
        """
        return self._strkey().index(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        """Like blob.rfind() but raise ValueError when substring is not
        found.
        """
        return self._strkey().rindex(sub, start, end)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        """Returns True if the blob starts with the given prefix."""
        return self._strkey().startswith(prefix, start, end)

    def endswith(self, suffix, start=0, end=sys.maxsize):
        """Returns True if the blob ends with the given suffix."""
        return self._strkey().endswith(suffix, start, end)

    # PEP8 aliases
    starts_with = startswith
    ends_with = endswith

    def title(self):
        """Returns a blob object with the text in title-case."""
        return self.__class__(self._strkey().title())

    def format(self, *args, **kwargs):
        """Perform a string formatting operation, like the built-in
        `str.format(*args, **kwargs)`. Returns a blob object.
        """
        return self.__class__(self._strkey().format(*args, **kwargs))

    def split(self, sep=None, maxsplit=sys.maxsize):
        """Behaves like the built-in str.split()."""
        return self._strkey().split(sep, maxsplit)

    def strip(self, chars=None):
        """Behaves like the built-in str.strip([chars]) method. Returns
        an object with leading and trailing whitespace removed.
        """
        return self.__class__(self._strkey().strip(chars))

    def upper(self):
        """Like str.upper(), returns new object with all upper-cased characters."""
        return self.__class__(self._strkey().upper())

    def lower(self):
        """Like str.lower(), returns new object with all lower-cased characters."""
        return self.__class__(self._strkey().lower())

    def join(self, iterable):
        """Behaves like the built-in `str.join(iterable)` method, except
        returns a blob object.

        Returns a blob which is the concatenation of the strings or blobs
        in the iterable.
        """
        return self.__class__(self._strkey().join(iterable))

    def replace(self, old, new, count=sys.maxsize):
        """Return a new blob object with all occurrences of `old` replaced
        by `new`.
        """
        return self.__class__(self._strkey().replace(old, new, count))
