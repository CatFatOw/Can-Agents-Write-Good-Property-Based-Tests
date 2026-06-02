"""
General functions for HTML manipulation.
"""

import re as _re
from html.entities import html5 as _html5


__all__ = ['escape', 'unescape']
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def escape(s, quote=True):
    args = [s, quote]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_escape__mutmut_orig, x_escape__mutmut_mutants, args, kwargs, None)


def x_escape__mutmut_orig(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_1(s, quote=False):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_2(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = None # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_3(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace(None, "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_4(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", None) # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_5(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_6(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", ) # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_7(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("XX&XX", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_8(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "XX&amp;XX") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_9(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&AMP;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_10(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = None
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_11(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace(None, "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_12(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", None)
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_13(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_14(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", )
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_15(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("XX<XX", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_16(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "XX&lt;XX")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_17(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&LT;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_18(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = None
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_19(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(None, "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_20(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", None)
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_21(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace("&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_22(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", )
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_23(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace("XX>XX", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_24(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "XX&gt;XX")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_25(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&GT;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_26(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = None
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_27(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace(None, "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_28(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', None)
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_29(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace("&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_30(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', )
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_31(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('XX"XX', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_32(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "XX&quot;XX")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_33(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&QUOT;")
        s = s.replace('\'', "&#x27;")
    return s


def x_escape__mutmut_34(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = None
    return s


def x_escape__mutmut_35(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace(None, "&#x27;")
    return s


def x_escape__mutmut_36(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', None)
    return s


def x_escape__mutmut_37(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace("&#x27;")
    return s


def x_escape__mutmut_38(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', )
    return s


def x_escape__mutmut_39(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('XX\'XX', "&#x27;")
    return s


def x_escape__mutmut_40(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "XX&#x27;XX")
    return s


def x_escape__mutmut_41(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#X27;")
    return s

x_escape__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_escape__mutmut_1': x_escape__mutmut_1, 
    'x_escape__mutmut_2': x_escape__mutmut_2, 
    'x_escape__mutmut_3': x_escape__mutmut_3, 
    'x_escape__mutmut_4': x_escape__mutmut_4, 
    'x_escape__mutmut_5': x_escape__mutmut_5, 
    'x_escape__mutmut_6': x_escape__mutmut_6, 
    'x_escape__mutmut_7': x_escape__mutmut_7, 
    'x_escape__mutmut_8': x_escape__mutmut_8, 
    'x_escape__mutmut_9': x_escape__mutmut_9, 
    'x_escape__mutmut_10': x_escape__mutmut_10, 
    'x_escape__mutmut_11': x_escape__mutmut_11, 
    'x_escape__mutmut_12': x_escape__mutmut_12, 
    'x_escape__mutmut_13': x_escape__mutmut_13, 
    'x_escape__mutmut_14': x_escape__mutmut_14, 
    'x_escape__mutmut_15': x_escape__mutmut_15, 
    'x_escape__mutmut_16': x_escape__mutmut_16, 
    'x_escape__mutmut_17': x_escape__mutmut_17, 
    'x_escape__mutmut_18': x_escape__mutmut_18, 
    'x_escape__mutmut_19': x_escape__mutmut_19, 
    'x_escape__mutmut_20': x_escape__mutmut_20, 
    'x_escape__mutmut_21': x_escape__mutmut_21, 
    'x_escape__mutmut_22': x_escape__mutmut_22, 
    'x_escape__mutmut_23': x_escape__mutmut_23, 
    'x_escape__mutmut_24': x_escape__mutmut_24, 
    'x_escape__mutmut_25': x_escape__mutmut_25, 
    'x_escape__mutmut_26': x_escape__mutmut_26, 
    'x_escape__mutmut_27': x_escape__mutmut_27, 
    'x_escape__mutmut_28': x_escape__mutmut_28, 
    'x_escape__mutmut_29': x_escape__mutmut_29, 
    'x_escape__mutmut_30': x_escape__mutmut_30, 
    'x_escape__mutmut_31': x_escape__mutmut_31, 
    'x_escape__mutmut_32': x_escape__mutmut_32, 
    'x_escape__mutmut_33': x_escape__mutmut_33, 
    'x_escape__mutmut_34': x_escape__mutmut_34, 
    'x_escape__mutmut_35': x_escape__mutmut_35, 
    'x_escape__mutmut_36': x_escape__mutmut_36, 
    'x_escape__mutmut_37': x_escape__mutmut_37, 
    'x_escape__mutmut_38': x_escape__mutmut_38, 
    'x_escape__mutmut_39': x_escape__mutmut_39, 
    'x_escape__mutmut_40': x_escape__mutmut_40, 
    'x_escape__mutmut_41': x_escape__mutmut_41
}
x_escape__mutmut_orig.__name__ = 'x_escape'


# see https://html.spec.whatwg.org/multipage/parsing.html#numeric-character-reference-end-state

_invalid_charrefs = {
    0x00: '\ufffd',  # REPLACEMENT CHARACTER
    0x0d: '\r',      # CARRIAGE RETURN
    0x80: '\u20ac',  # EURO SIGN
    0x81: '\x81',    # <control>
    0x82: '\u201a',  # SINGLE LOW-9 QUOTATION MARK
    0x83: '\u0192',  # LATIN SMALL LETTER F WITH HOOK
    0x84: '\u201e',  # DOUBLE LOW-9 QUOTATION MARK
    0x85: '\u2026',  # HORIZONTAL ELLIPSIS
    0x86: '\u2020',  # DAGGER
    0x87: '\u2021',  # DOUBLE DAGGER
    0x88: '\u02c6',  # MODIFIER LETTER CIRCUMFLEX ACCENT
    0x89: '\u2030',  # PER MILLE SIGN
    0x8a: '\u0160',  # LATIN CAPITAL LETTER S WITH CARON
    0x8b: '\u2039',  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x8c: '\u0152',  # LATIN CAPITAL LIGATURE OE
    0x8d: '\x8d',    # <control>
    0x8e: '\u017d',  # LATIN CAPITAL LETTER Z WITH CARON
    0x8f: '\x8f',    # <control>
    0x90: '\x90',    # <control>
    0x91: '\u2018',  # LEFT SINGLE QUOTATION MARK
    0x92: '\u2019',  # RIGHT SINGLE QUOTATION MARK
    0x93: '\u201c',  # LEFT DOUBLE QUOTATION MARK
    0x94: '\u201d',  # RIGHT DOUBLE QUOTATION MARK
    0x95: '\u2022',  # BULLET
    0x96: '\u2013',  # EN DASH
    0x97: '\u2014',  # EM DASH
    0x98: '\u02dc',  # SMALL TILDE
    0x99: '\u2122',  # TRADE MARK SIGN
    0x9a: '\u0161',  # LATIN SMALL LETTER S WITH CARON
    0x9b: '\u203a',  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x9c: '\u0153',  # LATIN SMALL LIGATURE OE
    0x9d: '\x9d',    # <control>
    0x9e: '\u017e',  # LATIN SMALL LETTER Z WITH CARON
    0x9f: '\u0178',  # LATIN CAPITAL LETTER Y WITH DIAERESIS
}

_invalid_codepoints = {
    # 0x0001 to 0x0008
    0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8,
    # 0x000E to 0x001F
    0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19,
    0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
    # 0x007F to 0x009F
    0x7f, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a,
    0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96,
    0x97, 0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f,
    # 0xFDD0 to 0xFDEF
    0xfdd0, 0xfdd1, 0xfdd2, 0xfdd3, 0xfdd4, 0xfdd5, 0xfdd6, 0xfdd7, 0xfdd8,
    0xfdd9, 0xfdda, 0xfddb, 0xfddc, 0xfddd, 0xfdde, 0xfddf, 0xfde0, 0xfde1,
    0xfde2, 0xfde3, 0xfde4, 0xfde5, 0xfde6, 0xfde7, 0xfde8, 0xfde9, 0xfdea,
    0xfdeb, 0xfdec, 0xfded, 0xfdee, 0xfdef,
    # others
    0xb, 0xfffe, 0xffff, 0x1fffe, 0x1ffff, 0x2fffe, 0x2ffff, 0x3fffe, 0x3ffff,
    0x4fffe, 0x4ffff, 0x5fffe, 0x5ffff, 0x6fffe, 0x6ffff, 0x7fffe, 0x7ffff,
    0x8fffe, 0x8ffff, 0x9fffe, 0x9ffff, 0xafffe, 0xaffff, 0xbfffe, 0xbffff,
    0xcfffe, 0xcffff, 0xdfffe, 0xdffff, 0xefffe, 0xeffff, 0xffffe, 0xfffff,
    0x10fffe, 0x10ffff
}


def _replace_charref(s):
    args = [s]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__replace_charref__mutmut_orig, x__replace_charref__mutmut_mutants, args, kwargs, None)


def x__replace_charref__mutmut_orig(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_1(s):
    s = None
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_2(s):
    s = s.group(None)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_3(s):
    s = s.group(2)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_4(s):
    s = s.group(1)
    if s[1] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_5(s):
    s = s.group(1)
    if s[0] != '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_6(s):
    s = s.group(1)
    if s[0] == 'XX#XX':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_7(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[2] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_8(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] not in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_9(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'XXxXXX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_10(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xx':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_11(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'XX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_12(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = None
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_13(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(None, 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_14(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), None)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_15(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_16(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), )
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_17(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(None), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_18(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].lstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_19(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[3:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_20(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip('XX;XX'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_21(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 17)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_22(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num not in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_23(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF and num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_24(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 55297 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_25(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 < num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_26(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num < 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_27(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 57344 or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_28(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num >= 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_29(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 1114112:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_30(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num not in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_31(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(None)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_32(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s not in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_33(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(None, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_34(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, None, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_35(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, None):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_36(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_37(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_38(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, ):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_39(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s) + 1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_40(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-2, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_41(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 2, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_42(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, +1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_43(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -2):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' + s


def x__replace_charref__mutmut_44(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return '&' - s


def x__replace_charref__mutmut_45(s):
    s = s.group(1)
    if s[0] == '#':
        # numeric charref
        if s[1] in 'xX':
            num = int(s[2:].rstrip(';'), 16)
        else:
            num = int(s[1:].rstrip(';'))
        if num in _invalid_charrefs:
            return _invalid_charrefs[num]
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return '\uFFFD'
        if num in _invalid_codepoints:
            return ''
        return chr(num)
    else:
        # named charref
        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s)-1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return 'XX&XX' + s

x__replace_charref__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__replace_charref__mutmut_1': x__replace_charref__mutmut_1, 
    'x__replace_charref__mutmut_2': x__replace_charref__mutmut_2, 
    'x__replace_charref__mutmut_3': x__replace_charref__mutmut_3, 
    'x__replace_charref__mutmut_4': x__replace_charref__mutmut_4, 
    'x__replace_charref__mutmut_5': x__replace_charref__mutmut_5, 
    'x__replace_charref__mutmut_6': x__replace_charref__mutmut_6, 
    'x__replace_charref__mutmut_7': x__replace_charref__mutmut_7, 
    'x__replace_charref__mutmut_8': x__replace_charref__mutmut_8, 
    'x__replace_charref__mutmut_9': x__replace_charref__mutmut_9, 
    'x__replace_charref__mutmut_10': x__replace_charref__mutmut_10, 
    'x__replace_charref__mutmut_11': x__replace_charref__mutmut_11, 
    'x__replace_charref__mutmut_12': x__replace_charref__mutmut_12, 
    'x__replace_charref__mutmut_13': x__replace_charref__mutmut_13, 
    'x__replace_charref__mutmut_14': x__replace_charref__mutmut_14, 
    'x__replace_charref__mutmut_15': x__replace_charref__mutmut_15, 
    'x__replace_charref__mutmut_16': x__replace_charref__mutmut_16, 
    'x__replace_charref__mutmut_17': x__replace_charref__mutmut_17, 
    'x__replace_charref__mutmut_18': x__replace_charref__mutmut_18, 
    'x__replace_charref__mutmut_19': x__replace_charref__mutmut_19, 
    'x__replace_charref__mutmut_20': x__replace_charref__mutmut_20, 
    'x__replace_charref__mutmut_21': x__replace_charref__mutmut_21, 
    'x__replace_charref__mutmut_22': x__replace_charref__mutmut_22, 
    'x__replace_charref__mutmut_23': x__replace_charref__mutmut_23, 
    'x__replace_charref__mutmut_24': x__replace_charref__mutmut_24, 
    'x__replace_charref__mutmut_25': x__replace_charref__mutmut_25, 
    'x__replace_charref__mutmut_26': x__replace_charref__mutmut_26, 
    'x__replace_charref__mutmut_27': x__replace_charref__mutmut_27, 
    'x__replace_charref__mutmut_28': x__replace_charref__mutmut_28, 
    'x__replace_charref__mutmut_29': x__replace_charref__mutmut_29, 
    'x__replace_charref__mutmut_30': x__replace_charref__mutmut_30, 
    'x__replace_charref__mutmut_31': x__replace_charref__mutmut_31, 
    'x__replace_charref__mutmut_32': x__replace_charref__mutmut_32, 
    'x__replace_charref__mutmut_33': x__replace_charref__mutmut_33, 
    'x__replace_charref__mutmut_34': x__replace_charref__mutmut_34, 
    'x__replace_charref__mutmut_35': x__replace_charref__mutmut_35, 
    'x__replace_charref__mutmut_36': x__replace_charref__mutmut_36, 
    'x__replace_charref__mutmut_37': x__replace_charref__mutmut_37, 
    'x__replace_charref__mutmut_38': x__replace_charref__mutmut_38, 
    'x__replace_charref__mutmut_39': x__replace_charref__mutmut_39, 
    'x__replace_charref__mutmut_40': x__replace_charref__mutmut_40, 
    'x__replace_charref__mutmut_41': x__replace_charref__mutmut_41, 
    'x__replace_charref__mutmut_42': x__replace_charref__mutmut_42, 
    'x__replace_charref__mutmut_43': x__replace_charref__mutmut_43, 
    'x__replace_charref__mutmut_44': x__replace_charref__mutmut_44, 
    'x__replace_charref__mutmut_45': x__replace_charref__mutmut_45
}
x__replace_charref__mutmut_orig.__name__ = 'x__replace_charref'


_charref = _re.compile(r'&(#[0-9]+;?'
                       r'|#[xX][0-9a-fA-F]+;?'
                       r'|[^\t\n\f <&#;]{1,32};?)')

def unescape(s):
    args = [s]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_unescape__mutmut_orig, x_unescape__mutmut_mutants, args, kwargs, None)

def x_unescape__mutmut_orig(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' not in s:
        return s
    return _charref.sub(_replace_charref, s)

def x_unescape__mutmut_1(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if 'XX&XX' not in s:
        return s
    return _charref.sub(_replace_charref, s)

def x_unescape__mutmut_2(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' in s:
        return s
    return _charref.sub(_replace_charref, s)

def x_unescape__mutmut_3(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' not in s:
        return s
    return _charref.sub(None, s)

def x_unescape__mutmut_4(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' not in s:
        return s
    return _charref.sub(_replace_charref, None)

def x_unescape__mutmut_5(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' not in s:
        return s
    return _charref.sub(s)

def x_unescape__mutmut_6(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' not in s:
        return s
    return _charref.sub(_replace_charref, )

x_unescape__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_unescape__mutmut_1': x_unescape__mutmut_1, 
    'x_unescape__mutmut_2': x_unescape__mutmut_2, 
    'x_unescape__mutmut_3': x_unescape__mutmut_3, 
    'x_unescape__mutmut_4': x_unescape__mutmut_4, 
    'x_unescape__mutmut_5': x_unescape__mutmut_5, 
    'x_unescape__mutmut_6': x_unescape__mutmut_6
}
x_unescape__mutmut_orig.__name__ = 'x_unescape'
