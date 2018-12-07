"""
[P]ython [I]nteger [R]epresentations & Arithmetic Library

Almost all arguments for functions of this module can be decimal,
hexadecimal ('0x...' or without '0x'), binary ('0b...') or float.
Arithmetic function results format is hexadecimal by default
(you can change this by calling the function `psetmode()` or
with the optional parameter `fmt` for almost any function).

By default integers are signed, integer width is equal 64
(you can change this by calling the function `psetmode()`).
"""

"""
For update:

import sys, importlib
importlib.reload(sys.modules['pir'])
from pir import *
"""

from textwrap import wrap

############################################################
###                    Representation                    ###
############################################################

# By default, all integers are signed
is_signed = True

# By default the integer width is equal to 64
int_width = 64

# The default output format is hexadecimal
out_format = 'h'
ftable = {'d': int, 'h': hex, 'b': bin, 'f': float}

def psetmode(signed=None, width=None, fmt=None):
    """Set parameters of integers in module:
    signed - signed/unsigned integers. Should be equal True or False;
    width  - width of integer (including the sign bit). Should be > 0;
    fmt    - determine format of arithmetic results by default.
             May be equal:
              'd' - usual integer (decimal),
              'h' - string-hexadecimal begining with '0x',
              'b' - string-binary begining with '0b',
              'f' - usual float"""

    global is_signed, int_width, out_format

    if signed != None:
        is_signed = bool(signed)

    if width != None:
        assert width > 0
        int_width = int(width)

    if fmt:
        fmt = fmt.lower()
        assert fmt in ftable
        out_format = fmt

def pgetmode():
    return [ is_signed, int_width, out_format ]

def pint(a):
    """Convert {float, int, hex, bin} -> int"""
    if type(a) == type(''):
        if a[:2] == '0b' or a[:3] == '-0b':
            return int(a, 2)
        else:
            return int(a, 16)
    else:
        return int(a)

def inconv(a):
    """Convert {float, int, hex, bin} -> int;
    value is truncated to the integer width"""
    x = pint(a)

    # Truncate
    x &= ((1<<int_width)-1)

    # Converse unsigned int to signed back
    if is_signed:
        if x >= (1<<(int_width-1)):
            x -= (1<<int_width)

    return x

def outconv(x, fmt=None):
    """Convert positive decimal value according to format `fmt` (if it's given)
    or default format `out_format` (see `setoutformat()`)"""
    assert type(x) == type(0)
    assert x >= 0
    if fmt:
        return ftable[fmt](x)
    else:
        return ftable[out_format](x)

def c2repr(X, fmt=None):
    """Represent value in a manner 'Two's complement' to given format;
    value is truncated to the integer width

    In [..]: psetmode(True, 4, 'h')
    In [..]: c2repr(-2)
    Out[..]: '0xe'

    In [..]: c2repr(-2, 'd')
    Out[..]: -2

    In [..]: c2repr(14, 'd')
    Out[..]: -2

    In [..]: psetmode(False, 4, 'h')
    In [..]: c2repr(-1, 'd')
    Out[..]: 15"""

    x = pint(X)

    # Truncate
    x &= ((1<<int_width)-1)

    # Converse unsigned int to signed back
    if is_signed:

        if not fmt:
            fmt = out_format
        assert fmt in ['d', 'f', 'h', 'b']

        if x >= (1<<(int_width-1)) and fmt in ['d', 'f']:
            return -outconv((1<<int_width) - x, fmt)

    # Usual formated output
    return outconv(x, fmt)

def prepr(X, ends=[], fmt=None):
    """Get bitwise representation of integer `X` by bytes (if list `ends`
    is empty) or by fields (if list `ends` determine boarders of fields).

    X    - integer in any form (int, hex, bin or float);
    ends - list of last bit numbers of every field;
    fmt    - format of output ('d', 'h', 'b' or 'f')

    In [..]: prepr(3932166)
    Out[..]: ['00111100', '00000000', '00000110']

    In [..]: prepr(3932166, fmt='b')
    Out[..]: ['0b111100', '0b0', '0b110']

    In [..]: prepr(3932166, [22, 17, 15, 13, 7])
    Out[..]: ['01111', '00', '00', '000000', '00000110']

    In [..]: prepr(3932166, [7, 13, 15, 17, 22], 'h')
    Out[..]: ['0xf', '0x0', '0x0', '0x0', '0x6']"""

    # For convenience reverse bitwise representation
    rev_X = bin(pint(X))[-1:1:-1]

    if not ends:
        # Just split representation by bytes
        y = [ x[::-1].zfill(8) for x in wrap(rev_X, 8)[::-1] ]
    else:
        # Add to y all other fields
        y = []
        i = 0
        ends = sorted(ends)
        for j in ends:
            y.append(rev_X[i:j+1][::-1].zfill(j+1-i))
            i = j+1

        # Reverse back fields order
        y = y[::-1]

    if fmt:
        return [ outconv(int(x, 2), fmt) for x in y ]
    else:
        return y


############################################################
###                      Arithmetic                      ###
############################################################

def padd(a1, a2, fmt=None):
    """Sum of integers"""
    return c2repr(inconv(a1) + inconv(a2), fmt)

def psub(a1, a2, fmt=None):
    """Subtraction of integers"""
    return c2repr(inconv(a1) - inconv(a2), fmt)

def pmul(a1, a2, fmt=None):
    """Multiplication of integers"""
    return c2repr(inconv(a1) * inconv(a2), fmt)

def pdiv(a1, a2, fmt=None):
    """Division of integers"""
    return c2repr(inconv(a1) // inconv(a2), fmt)

def pdivf(a1, a2):
    """Division of integers with float result"""
    return inconv(a1) / inconv(a2)

def prem(a1, a2, fmt=None):
    """Remainder of the division of integers"""
    return c2repr(inconv(a1) % inconv(a2), fmt)

def pls(a, i, fmt=None):
    """Logical left shift of integers"""
    return c2repr(inconv(a) << inconv(i), fmt)

def prs(a, i, fmt=None):
    """Logical right shift of integers"""
    return c2repr(inconv(a) >> inconv(i), fmt)

def pand(a1, a2, fmt=None):
    """Bitwise AND"""
    return c2repr(inconv(a1) & inconv(a2), fmt)

def por(a1, a2, fmt=None):
    """Bitwise OR"""
    return c2repr(inconv(a1) | inconv(a2), fmt)

def pxor(a1, a2, fmt=None):
    """Bitwise XOR"""
    return c2repr(inconv(a1) ^ inconv(a2), fmt)

def pmask(l, h, fmt=None):
    """Get mask. Example:

    In [..]: pmask(1, 3, 'b')
    Out[..]: '0b1110'"""
    return c2repr(((-1)<<inconv(l)) & (~((-1)<<(inconv(h)+1))), fmt)

def pgetbits(a, r, fmt=None):
    """Get bit or bits range of integer. Example:

    In [..]: c2repr(694, 'b')
    Out[..]: '0b1010110110'

    In [..]: pgetbits(694, 7, 'd')
    Out[..]: 1

    In [..]: pgetbits(694, [3, 7], 'b')
    Out[..]: '0b10110'"""
    if type(r) == type(0):
        return c2repr((inconv(a) & (1<<r)) >> r, fmt)
    else:
        return c2repr((inconv(a) & pmask(r[0], r[1], 'd')) >> r[0], fmt)

def psetbits(a, r, v=-1, fmt=None):
    """Assign the value `v` to the bits specified by `r`. Example:

    In [..]: c2repr(694, 'b')
    Out[..]: '0b1010110110'

    In [..]: psetbits(694, 1, 0, 'b')
    Out[..]: '0b1010110100'

    In [..]: psetbits(694, [2, 7], fmt='b')
    Out[..]: '0b1011111110'

    In [..]: psetbits(694, [2, 7], '0b010101', 'b')
    Out[..]: '0b1001010110'"""
    if type(r) == type(0):
        v_mask = 1 << r
        return c2repr( (inconv(a) & (~v_mask))
                       | (inconv(v) << r) & v_mask, fmt)
    else:
        v_mask = pmask(r[0], r[1], 'd')
        return c2repr( (inconv(a) & (~v_mask))
                       | (inconv(v) << r[0]) & v_mask, fmt)

def pdropbits(a, r, fmt=None):
    """Set bits to zero (it is psetbits(a, r, v=0, fmt))"""
    return psetbits(a, r, 0, fmt)

def pintmin(fmt=None):
    """Get minimum integer according to current mode"""
    if is_signed:
        return c2repr(1<<(int_width-1), fmt)
    else:
        return c2repr(0, fmt)

def pintmax(fmt=None):
    """Get maximum integer according to current mode"""
    if is_signed:
        return c2repr(~(1<<(int_width-1)), fmt)
    else:
        return c2repr(-1, fmt)


############################################################
###                         Test                         ###
############################################################

def testpir():
    s, w, f = is_signed, int_width, out_format

    psetmode(True, 64, 'h')
    assert ( prepr(3932166) == ['00111100', '00000000', '00000110'] )
    assert ( prepr('0x3c0006') == ['00111100', '00000000', '00000110'] )
    assert ( prepr('3c0006') == ['00111100', '00000000', '00000110'] )
    assert ( prepr('0b1111000000000000000110')
             == ['00111100', '00000000', '00000110'] )
    assert ( prepr(3932166.) == ['00111100', '00000000', '00000110'] )
    assert ( prepr(3932166, [7, 13, 15, 17, 22])
             == ['01111', '00', '00', '000000', '00000110'] )
    assert ( prepr(3932166, fmt='b') == ['0b111100', '0b0', '0b110'] )
    assert ( prepr(3932166, [7, 13, 15, 17, 22], 'h')
             == ['0xf', '0x0', '0x0', '0x0', '0x6'] )
    assert ( psub('0b100000', padd('a', 11)) == '0xb' )
    psetmode(fmt='b')
    assert ( pmul(3, padd(pdiv('f', '0b100'), prem(11, '0x3'))) == '0b1111' )
    psetmode(width=4)
    assert ( c2repr(-1) == '0b1111' )
    assert ( c2repr(8) == c2repr(-8) == '0b1000' )
    assert ( c2repr(7) == c2repr(-9) == '0b111' )
    psetmode(fmt='h')
    assert ( padd(15, 15) == '0xe' )
    assert ( psub(1, 15) == '0x2' )
    assert ( padd(7, 1., fmt='b') == '0b1000' )
    assert ( pmul('0b1000', '0b111') == '0x8' )
    assert ( pmul('0b1000', '0b111', fmt='f') == -8. )
    assert ( c2repr(14, fmt='d') == -2 )
    assert ( c2repr(14, fmt='h') == '0xe' )
    assert ( pmul('0b1000', '0b110', fmt='d') == 0 )
    assert ( padd(7, 7, 'd') == -2 )
    assert ( psub(1, 2, 'd') == -1 )
    psetmode(width=64)
    assert ( psub('0b100000', padd('a', 11)) == '0xb' )
    assert ( psub('0b10000', padd('a', 11)) == '0xfffffffffffffffb' )
    psetmode(fmt='b')
    assert ( pmul(3, padd(pdiv('f', '0b100'), prem(11, '0x3'))) == '0b1111' )
    assert ( pgetmode() == [True, 64, 'b'] )
    psetmode(signed=False, width=4, fmt='h')
    assert ( padd(7, 7, 'd') == 14 )
    assert ( psub(1, 2) == '0xf' )
    assert ( psub(1, 2, 'd') == 15 )
    assert ( psub(1, 1000) == '0x9' )
    assert ( c2repr(-1, 'd') == 15 )
    psetmode(False, 6, 'b')
    assert ( pintmin() == '0b0' and pintmax() == '0b111111' )
    psetmode(True)
    assert ( pintmin() == '0b100000' and pintmax() == '0b11111' )
    assert ( padd(pintmin(), pintmax(), 'd') == -1 )
    assert ( psub(pintmin(), 1, 'd') == pintmax('d') == 31 )
    psetmode(True, 64, 'f')
    assert ( pand(204, 694, 'h') == '0x84' and por(204, 694, 'h') == '0x2fe' )
    assert ( pxor(204, 694, 'h') == '0x27a' and pmask(1, 3, 'b') == '0b1110' )
    assert ( pgetbits(694, 7, 'd') == 1 )
    assert ( pgetbits(694, [3, 7], 'b') == '0b10110' )
    assert ( psetbits(694, 1, 0, 'h') == '0x2b4' )
    assert ( psetbits(694, [2, 7], fmt='h') == '0x2fe' )
    assert ( psetbits(694, [2, 7], '0b010101', 'b') == '0b1001010110' )
    assert ( pdropbits('0b10100', 2, 'd') == 16 )

    psetmode(s, w, f)

