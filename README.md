## Python Integer Representations & Arithmetic Library

This tool may be useful to system software developers (for example, compiler or binutils developers). Here are functions for representing integers in a convenient form and functions for arithmetic over integers of arbitrary format.

### Formats

The integer arguments of almost all functions can be of any of 4 formats:
* **decimal** &mdash; usual python integer (`0`, `7`, `-2`, ...);
* **hexadecimal** &mdash; string with or without prefix ``'0x'`` (``'0xf'``, ``'a7'``, and even ``'-0xcf'``);
* **binary** &mdash; string with prefix `'0b'` (`'0b010110'`, `'0b0'`, ...);
* **float** &mdash; usual python float (Why not? `0.0`, `17.`, `-3.`, ...).

You can globaly specify the default output format for arithmetic functions by call `psetmode` or localy for each interface (by their parameter `fmt`).

### Representations

`c2repr` gives two's complement representation in any output format in accordance with the current signedness and int width (signed 64-bit by default).

    >>> from pir import *

    >>> c2repr(5, 'b')
    '0b101'

    >>> c2repr(-10)
    '0xfffffffffffffff6'

    >>> c2repr('8000000000000000', 'd')
    -9223372036854775808

    >>> c2repr('4000000000000000', 'd')
    4611686018427387904

Meaning of `prepr` by example. The operation `sethi  %hi(0x103c00), %o3` (see Sparc Instruction Set) is encoded to `1700040f`. We can clearly expand the code instructions on its fields. For this we need to know the numbers of the last bits of all fields:

    >>> prepr('1700040f', [31, 29, 24, 21])
    ['00', '01011', '100', '0000000000010000001111']

    >>> prepr('1700040f', [31, 29, 24, 21], 'h')
    ['0x0', '0xb', '0x4', '0x40f']

Why `'0x40f'` and not `0x103c00`? It's ok. `sethi` sets just 22 high bits:

    # Left shift
    >>> pls('0x40f', 10)
    '0x103c00'

We could just decompose any integer by bytes:

    >>> prepr(3932166)
    ['00111100', '00000000', '00000110']

### Arithmetic

You can globaly specify the signedness and the integer width by `psetmode`:

    >>> from pir import *

    # Default mode: signed, 64-bit, hexadecimal default output
    >>> pgetmode()
    [True, 64, 'h']
    >>> psub('0x100', 15)
    '0xf1'

    # Signed 8-bit int with decimal output by default
    >>> psetmode(True, 8, 'd')
    >>> pgetmode()
    [True, 8, 'd']
    >>> psub('0x100', 15.)
    -15
    >>> psub('0x100', '0b1111', 'b')
    '0b11110001'

**pir** contains several other elementary arithmetic functions:

    >>> psetmode(True, 8, 'd')
    >>> pmul(3, padd(pdiv('f', '0b100'), prem(11, '0x3')))
    15
    >>> psetbits(15, [3, 4], '0b10')
    23
    >>> padd(pintmin(), pintmax())
    -1
