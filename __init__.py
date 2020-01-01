#!/bin/env python

from .backend import get_backend, set_backend

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


def reload_mvlib():
    from importlib import reload, import_module

    def reload_module(submodule: str):
        module = import_module(submodule, __package__)
        reload(module)

    for str_module in __all__:
        reload_module("." + str_module)


set_backend(None)  # 初始化backend
