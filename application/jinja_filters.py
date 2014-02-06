# -*- coding: utf-8 -*-

import sys
import inspect


def set_up_jinja_filters(_app):
    this_module = sys.modules[__name__]

    def is_mod_function(_func):
        return inspect.isfunction(_func) and inspect.getmodule(_func) == this_module
    for func in [func for func in this_module.__dict__.itervalues() if is_mod_function(func)]:
        if func.__name__ != 'set_up_jinja_filters':
            _app.jinja_env.filters[func.__name__] = func

__all__ = [set_up_jinja_filters]
