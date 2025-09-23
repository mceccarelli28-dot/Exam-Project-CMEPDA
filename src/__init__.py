# Copyright (C) 2025 Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#i dont know what this is about, i only know the things from metarep:


import pathlib
import subprocess

from ._version import __version__ as __base_version__

METAREP_SRC = pathlib.Path(__file__).parent
METAREP_ROOT = METAREP_SRC.parent.parent
METAREP_TESTS = METAREP_ROOT / "tests"
METAREP_DOCS = METAREP_ROOT / "docs"


def _git_suffix() -> str:
    """If we are in a git repo, we want to add the necessary information to the
    version string.

    This will return something along the lines of ``+gf0f18e6.dirty``.
    """
    # pylint: disable=broad-except
    kwargs = dict(cwd=METAREP_ROOT, stderr=subprocess.DEVNULL)
    try:
        # Retrieve the git short sha to be appended to the base version string.
        args = ["git", "rev-parse", "--short", "HEAD"]
        sha = subprocess.check_output(args, **kwargs).decode().strip()
        suffix = f"+g{sha}"
        # If we have uncommitted changes, append a `.dirty` to the version suffix.
        args = ["git", "diff", "--quiet"]
        if subprocess.call(args, stdout=subprocess.DEVNULL, **kwargs) != 0:
            suffix = f"{suffix}.dirty"
        return suffix
    except Exception:
        return ""


__version__ = f"{__base_version__}{_git_suffix()}"


#It goes without saying, the source code (i.e., the actual Python modules) is typically the most important part of your repository. (Ironically, this is not the case for this repo.) At the very minimum the source code includes
#a __init__.py, a special Python file that is used to mark a directory as a Python package (in the simplest case the the file can be empty.
#    all the Python modules that your package ships—this should be self-explaining and, quite possibly, is the only thing you ever cared about before reading this;
#depending on how exactly you do versioning, you might have a _version.py file (the precise name might differ)—more on this at the page about Versioning.
#In terms of where the source code actually lives, the basic answer is: isolated in a single folder with the same name as the package. This folder can live at the top level in the repository structure, or further embedded in a src folder, which is sometimes referred as flat vs. src layout. To make a long story short, the Python package authority recommends the latter (src layout) and this is what we use here. You find (a lot of) additional information here

