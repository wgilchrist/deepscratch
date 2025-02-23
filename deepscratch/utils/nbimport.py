import io, os, sys, types

import ast
import io
import traceback
from nbformat import read

from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import register_line_magic

from importlib.machinery import SourceFileLoader, ModuleSpec
from importlib.abc import Loader

import traceback
import linecache



class DirectoryFinder(Loader):
    """Module Loader for Jupyter Notebooks"""

    def __init__(self, path=None):
        super().__init__()

    def find_dir(self, fullname, path=None):
        name = fullname.rsplit(".", 1)[-1]
        name = name.replace("_", " ")
        if not path:
            path = ["/"]
        for d in path:
            for f in os.listdir(d):
                fmt_f = f.split(". ", 1)[
                    -1
                ].lower()  # format f: 1. Notebook.ipynb becomes notebook.ipynb
                if fmt_f == name:
                    return d + os.path.sep + f

    def find_spec(self, fullname, path=None, target=None):
        dir_path = self.find_dir(fullname, path)
        if dir_path:
            spec = ModuleSpec(fullname, self, origin=dir_path)
            return spec
        else:
            return

    def create_module(self, spec):
        mod = types.ModuleType(spec.name)
        mod.__file__ = spec.origin
        mod.__loader__ = self
        mod.__spec__ = spec
        mod.__package__ = spec.name
        mod.__path__ = [spec.origin]
        mod.__dict__["get_ipython"] = get_ipython
        sys.modules[spec.name] = mod
        return mod

    def exec_module(self, module):
        pass


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""

    def __init__(self):
        self.loaders = {}
        self.shell = InteractiveShell.instance()

    def find_notebook(self, fullname, path=None):
        name = fullname.rsplit(".", 1)[-1]
        name = name.replace("_", " ") + ".ipynb"
        if not path:
            path = ["/"]
        for d in path:
            for f in os.listdir(d):
                fmt_f = f.split(". ", 1)[
                    -1
                ].lower()  # format f: 1. Notebook.ipynb becomes notebook.ipynb
                if fmt_f == name:
                    return d + os.path.sep + f

    def find_spec(self, fullname, path=None, target=None):
        nb_path = self.find_notebook(fullname, path)
        if nb_path:
            spec = ModuleSpec(fullname, self, origin=nb_path)
            return spec
        else:
            return

    def create_module(self, spec):
        """import a notebook as a module"""
        
        mod = types.ModuleType(spec.name)
        mod.__file__ = spec.origin
        mod.__loader__ = self
        mod.__dict__["get_ipython"] = get_ipython
        print(spec.name)
        sys.modules[spec.name] = mod

        return mod

    def exec_module(self, mod):
        with io.open(mod.__file__, "r", encoding="utf-8") as f:
            nb = read(f, 4)

        for i, cell in enumerate(nb.cells, start=1):
            if cell.cell_type == "code":
                execute_definitions(cell.source, mod.__dict__, filename=mod.__file__, cell_number=i)

        return mod

import os
import ast
import tempfile
import traceback
import linecache

import linecache

def execute_definitions(cell_source, module_globals, filename=None, cell_number=None):
    # Use a default filename if none is provided.
    filename = filename or "notebook.ipynb"
    try:
        tree = ast.parse(cell_source, filename=filename)
    except Exception:
        traceback.print_exc()
        return

    selected_nodes = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
            selected_nodes.append(node)

    if not selected_nodes:
        return

    if cell_number is not None:
        compile_filename = f"{filename} (cell {cell_number})"
    else:
        compile_filename = filename

    new_tree = ast.Module(body=selected_nodes, type_ignores=[])
    ast.fix_missing_locations(new_tree)
    
    # Update linecache so that the traceback shows the cell source
    source_lines = cell_source.splitlines(keepends=True)
    # The tuple format is: (size, mtime, lines, filename)
    # Here we use len(cell_source) as a dummy size and None for mtime.
    linecache.cache[compile_filename] = (len(cell_source), None, source_lines, compile_filename)

    try:
        compiled = compile(new_tree, filename=compile_filename, mode="exec")
        exec(compiled, module_globals)
    except Exception:
        traceback.print_exc()
