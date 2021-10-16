"""Sphinx style docstring checks for common issues.

Common issues checked for:
* VSCode defaults: The default values like [description] or [summary] should not be allowed
* Empty docstrings. Having :param or :return without anything after it passes pylint
* No newline before sphinx fields.

Exits non-zero on fail.
"""
import argparse
import ast
from pathlib import Path
import re
import sys
from typing import List, Optional, Union

FuncDef = Union[ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Parse python files in a path for docstring errors"
    )
    parser.add_argument("path", nargs="*", type=Path, help="Path(s) to search for python files.")
    return parser.parse_args()


class ParseFunctionDef:
    """Parse the function/class definitions."""

    regexes = {
        "param": r":param .*:",  # Support typing inside of this if it happens
        "type": r":type \S+:",  # This should only ever be a variable name
        "meta": r":meta \S+:",  # This is probably only ever private/publics
        "raises": r":raises .*:",
        "returns": r":returns:",
        "rtype": r":rtype:",
        "yield": r":yield:",
    }

    def __init__(self, function_def, path):
        self.function_def = function_def
        self.errors = []
        self.path = path

    def docstring(self) -> Optional[str]:
        """Docstring for a specific function definition.

        :returns: parsed docstring for an object or None if None is found.
        """
        try:
            return ast.get_docstring(self.function_def)
        except TypeError:
            return None

    @property
    def name(self) -> str:
        """Function name."""
        try:
            return self.function_def.name
        except AttributeError:
            return ""

    @property
    def lineno(self):
        """Return line number for sorting or 0 if not found."""
        try:
            return self.function_def.lineno
        except AttributeError:
            return 0

    def obj_type(self) -> str:
        """Description of the object type.

        :returns: The ast object type string.
        """
        return self.function_def.__class__.__name__

    def print_errors(self) -> None:
        """Print out of errors for an object."""
        if self.errors:
            print(f"*** {self.path}:{self.name}:{self.lineno}")
            print("\n".join(self.errors))
            print()

    def run_checks(self) -> int:
        """Run checks.

        :return: number of errors
        """
        if self.docstring() is None:
            return
        self.check_defaults()
        self.cehck_empty_docstring()
        self.check_empty_fields()
        self.check_newlines()
        self.print_errors()
        return len(self.errors)

    def check_defaults(self):
        """Check for default docstring generation.

        This includes [description], [summary], [type]

        Side-effect: Error strings are added to self.errors.
        """
        errors = re.findall(r"\[summary\]", self.docstring())
        errors += re.findall(r":.*: *\[description\]", self.docstring())
        errors += re.findall(r":.*: *\[type\]", self.docstring())
        if errors:
            self.errors += [f"default-docstring-error: {x}" for x in errors]

    def check_newlines(self):
        """Check for newlines before parameters.

        Side-effect: Error strings are added to self.errors.
        """
        line_regex = "|".join([f"{x}.*" for x in self.regexes.values()])
        matches = re.findall(f".*\n(?:{line_regex})", self.docstring(), re.M)
        if not matches:
            return

        prev_line, sphinx_line = matches[0].split("\n")
        if prev_line.strip():
            self.errors.append(f"missing-newline-error: '{sphinx_line}' needs newline before")

    def cehck_empty_docstring(self):
        """Error if docstring is empty."""
        if not self.docstring().strip():
            self.errors.append("empty-docstring-error: no docstring content")

    def check_empty_fields(self):
        """Check for types/parameters defined without descriptions.

        Pylint will catch when they are missing but does not check for content.
        """
        line_regex = "|".join([fr"{x}\s*$" for x in self.regexes.values()])
        matches = re.findall(line_regex, self.docstring(), re.M)
        if not matches:
            return
        for line in matches:
            if line.startswith(":meta"):
                continue
            self.errors.append(f"missing-description-error: {line}")


def function_definitions(fpath: Path) -> List[ParseFunctionDef]:
    """Return a list of function definition objects to be parsed.

    :param fpath: Path to file to parse
    :return: List of objects for each item in the file to be parsed
    """

    module = ast.parse(fpath.read_text())
    functions = [ParseFunctionDef(x, fpath) for x in ast.walk(module)]
    functions.sort(key=lambda x: x.lineno)
    return functions


def check_docstrings(fpath: Path) -> int:
    """Check docstrings for errors.

    :param fpath: Path to file to check docstrings
    :return: unix-style return code, 1 if errors are found
    """
    print("INFO: Checking file", fpath)
    returncodes = [x.run_checks() for x in function_definitions(fpath)]
    return bool(any(returncodes))


def main() -> int:
    """Run main function.

    :return: unix-style return code.
    """
    opts = parse_args()

    errors = 0
    for path in opts.path:
        if path.is_dir():
            paths = path.glob("**/*.py")
        else:
            paths = [path]
        for fname in paths:
            errors += check_docstrings(fname)

    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
