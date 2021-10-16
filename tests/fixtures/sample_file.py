"""This is a sample file for parsing sphinx errors"""
# pylint: disable=missing-class-docstring,too-few-public-methods
# pylint: disable=empty-docstring, missing-function-docstring,no-self-use


def func():
    """Docstring Title.

    :returns: return code
    :rtype: int
    """


class NoDocstrings:
    # This class has no docstrings, nothing should ever happen!
    def __init__(self):
        pass

    def run(self):
        ...


class WithDocstrings:
    """This class has docstrings that are correct.

    :param name: name of thing
    """

    def __init__(self, name):
        self.name = name

    def run(self, cmd):
        """Docstring Title.

        Description.

        :param cmd: Details about cmd.
        :type cmd: str
        :returns: return code
        :rtype: int
        :meta private:
        """


class DefaultDocstringErrors:
    """This class has some issues with default docstrings.

    :param abc: [description]
    :type abc: [type]
    """

    def default_summary(self):
        """[summary]"""

    def default_param(self, name):
        """Title here.

        :param name: [description]
        :type name: [type]
        """

    def default_return(self):
        """Testing the return type defaults are caught.

        :returns: [description]pyla
        :rtype: [type]
        """

    def default_yield(self):
        """Testing the default yield description is caught.

        :yield: [description] but other stuff here.
        :rtype: [type]"""

    def default_raise(self):
        """Test that the default raise is caught.

        :raises TypeError: [description]
        """


# fmt: off
class EmptyDescriptions:
    """
    This class has some issues forgetting to enter docstrings.

    :param abc:
    :type abc:    
    """
# fmt: on
    def empty_summary(self):
        """"""

    def empty_param(self, name):
        """Title here.

        :param name:
        :type name:
        """

    def empty_return(self):
        """Testing the return type defaults are caught.

        :returns:
        :rtype:"""

    def empty_yield(self):
        """Testing the default yield description is caught.

        :yield:
        :rtype:
        """

    def empty_raise(self):
        """Test that the default raise is caught.

        :raises TypeError:
        """

class EmptyClassDocstring:
    """"""


class NoNewlineDocstringErrors:
    """This class is needing newlines.
    :param name: name of class
    """

    def newline_param(self):
        """
        Missing newline before
        :param name: name
        """

    def newline_type(self):
        """
        Missing newline before
        :type name: name
        """

    def newline_raises(self):
        """
        Testing indented newlines
            maybe that's tricky?
        :raises TypeError: type error
        """

    def newline_yield(self):
        """Missing newline before
        :yield: yields
        """

    def newline_rtype(self):
        """Missing newline before
        :rtype: int
        """

    def newline_return(self):
        """Missing newline before
        :returns: int
        """

    def newline_meta(self):
        """This one is annoying if it doesn't work! Things show up!
        :meta private:
        """


class ValidCases:
    """Describe some tricky but passing cases."""

    def valid_cases(self):
        """This is ok because I'm going to describe
        :param and then never close the colon.
        """

    def extra_spaces(self):
        """This will have a lot of extra spaces.

        :param name: name

        :param value: value
            with some line wrapping
        :type value: int
        """

    def multi_fail(self):
        """[summary]
        :returns: something
        """
