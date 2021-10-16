"""Test sphinx content checks."""
from pathlib import Path
import re
import sys

import pytest

from sphinx_content import ParseFunctionDef, main

PROJ_ROOT = Path(__file__, "..", "..").resolve()


@pytest.mark.parametrize(
    "name,line,expected",
    [
        ("param", ":param name: description", True),
        ("param", "   :param name: description", False),
        ("param", ":param (int) name: description", True),
        ("param", ":param (int or str) name: description", True),
        ("param", "  :param with never ending", False),
        ("type", ":type name: description", True),
        ("type", "   :type name: description", False),
        ("type", ":type name: int or something", True),
        ("type", ":type (int or str) name: description", False),
        ("type", "  :type with never ending", False),
        ("meta", ":meta name: description", True),
        ("meta", "   :meta name: description", False),
        ("meta", ":meta name: int or something", True),
        ("meta", ":meta (int or str) name: description", False),
        ("meta", "  :meta with never ending", False),
        ("returns", ":returns:", True),
        ("returns", ":returns:    ", True),
        ("returns", ":returns:   Description ", True),
        ("returns", ":returns  [description] ", False),
        ("raises", ":raises Exception:", True),
        ("raises", ":raises Exception, OtherExc:    ", True),
        ("raises", ":raises:   Description ", False),
        ("raises", ":raises  Exception ", False),
        ("yield", ":yield:", True),
        ("yield", ":yield:    ", True),
        ("yield", ":yield:   Description ", True),
        ("yield", ":yield  [description] ", False),
        ("yield", ":yield  [description] :", False),
        ("rtype", ":rtype:", True),
        ("rtype", ":rtype:    ", True),
        ("rtype", ":rtype:   Description ", True),
        ("rtype", ":rtype  [description]", False),
        ("rtype", ":rtype  [description] :", False),
    ],
)
def test_regexes(name, line, expected):
    """Confirm that the regexes are matching what we want.

    Note that docstring deals with whitespace and there shouldn't be anything in front of it.
    """
    regex = ParseFunctionDef.regexes[name]
    assert bool(re.match(regex, line)) == expected


def test_sample_file(capsys):
    """Compare in/out file with lots of cases."""
    input_file = PROJ_ROOT / "tests" / "fixtures" / "sample_file.py"
    output_file = PROJ_ROOT / "tests" / "fixtures" / "output_sample_file.txt"

    sys.argv = [__file__, str(input_file)]
    assert main() == 1

    expected = output_file.read_text().replace("PROJ_ROOT", str(PROJ_ROOT))
    out, err = capsys.readouterr()
    assert err == ""
    assert out == expected
