#!/usr/bin/env python
"""Extensions to the see module"""

import sys
import re
from pprint import pformat

from see import see


def see_methods(thing, pattern=None):
    """Filter result of see to only methods

    If pattern is not None treat it as a regexp to filter further
    """
    result = see(thing)
    pattern = pattern or '\w'
    regexp = re.compile(f'{pattern}.*[)]$')
    return result.filter(regexp)


def see_attributes(thing, pattern=None):
    """Filter result of see to only not methods

    If pattern is not None treat it as a regexp to filter further
    """
    result = see(thing)
    pattern = pattern or ''
    regexp = re.compile(f'{pattern}.*[^)]$')
    return result.filter(regexp)


def spread(thing, exclude=None):
    """Spread out the attributes of thing onto stdout

    exclude is a list of regular expressions
        attributes matching any if these will not be shown
        if the default of None is used it is set to ['__.*__']
    """
    ids = []
    if not exclude:
        exclude = ['__.*__']
    exclusions = [re.compile(e) for e in exclude]

    def spread_out_an_attribute(v, separator):
        if not v:
            return repr(v)
        if id(v) in ids:
            return str(v)
        return spread_out_the_attributes(v, separator)

    def spread_out_the_attributes(thing, separator):
        if not thing or not hasattr(thing, '__dict__'):
            return pformat(thing)
        ids.append(id(thing))
        attributes_list = []
        for k, v in list(thing.__dict__.items()):
            if isinstance(v, type(sys)):
                continue
            if callable(v):
                continue
            excluded = False
            for exclusion in exclusions:
                if exclusion.search(k):
                    excluded = True
                    break
            if excluded:
                continue
            if hasattr(v, '__repr__'):
                value = v.__repr__()
            else:
                value = spread_out_an_attribute(v, separator)
            lines = separator.join(value.splitlines())
            attributes_list.append(f'{k} : {lines}')
        attributes_string = separator.join(attributes_list)
        ids.pop()
        class_name = thing.__class__.__name__
        klass = hasattr(thing, '__class__') and class_name or dir(thing)
        return f'''<{klass}{separator}{attributes_string}\n{separator[1:-2]}>'''

    print(spread_out_the_attributes(thing, '\n\t'))
