

# Introduction #

The dbformat is similar to original signsrch.

The parser recognizes following lines: **----**, **TITLE**, **TYPE** and **DATA**:
  * ---- is used to separate signatures
  * everything after "DATA" is treated as a signature

```
TITLE:Inverse Modified DCT pm128 (liba52)

TYPE:32
DATA:
0x00,0x10,0x20,0x30,0x40,0x50,0x60,0x70,0x08,0x28,0x48,0x68,0x18,0x38,0x58,0x78,0x04,0x14,0x24,0x34,0x44,0x54,0x64,0x74,0x0c,0x1c,0x2c,0x3c,0x4c,0x5c,0x6c,0x7c,
0x02,0x12,0x22,0x32,0x42,0x52,0x62,0x72,0x0a,0x2a,0x4a,0x6a,0x1a,0x3a,0x5a,0x7a,0x06,0x16,0x26,0x36,0x46,0x56,0x66,0x76,0x0e,0x2e,0x4e,0x6e,0x1e,0x3e,0x5e,0x7e,
0x01,0x11,0x21,0x31,0x41,0x51,0x61,0x71,0x09,0x29,0x49,0x69,0x19,0x39,0x59,0x79,0x05,0x15,0x25,0x35,0x45,0x55,0x65,0x75,0x0d,0x1d,0x2d,0x3d,0x4d,0x5d,0x6d,0x7d,
0x03,0x13,0x23,0x33,0x43,0x53,0x63,0x73,0x0b,0x2b,0x4b,0x6b,0x1b,0x3b,0x5b,0x7b,0x07,0x17,0x27,0x37,0x47,0x57,0x67,0x77,0x0f,0x1f,0x2f,0x3f,0x4f,0x5f,0x6f,0x7f, 

----
```

# types #

Type can contain following strings: **AND**, **CRC**, **LOGIC**, **STRING**, **ASCII**,
folowed by coolon and a list of possible bit-lengths, e.g: `TYPE:ASCII:8,32`, `TYPE:AND:32,64`

There is no support for "HEX" and "BIG" types which were present in original base.
(HEX was to mark some hex signatures in crappy format, BIG was used to specify, that signature in big-endian format shouldn't be generated).
**`FLOAT`** signatures were unified and replaced - more on that below.

(If you're surprised by the example, yes it actually might have sense to specify `ASCII` type signature with bit-length of 32)

## `LOGIC` and `AND` types ##

`AND` is a kind of wildcard signature, for example the following signature for MD5 constants:
```
TITLE:MD5 constants

TYPE:AND:32
DATA:
0x67452301,0x10325477,0x67452302,0x10325476, 
```
means that specified DWORDs should occur in the file in **specified order**, but between those dwords, there can be up-to 20 bytes.

In other words, this signature is converted into following (two) ClamAV signatures:
```
MD5 constants [32.lil.AND]:0:*:01234567{-20}77543210{-20}02234567{-20}76543210
MD5 constants [32.big.AND]:0:*:67452301{-20}10325477{-20}67452302{-20}10325476
```


`LOGIC` signatures, are bit more fun, consider following signature
```
TITLE:UPX miniacc

TYPE:LOGIC:64
DATA:
0x00000005deece66d,0x00000005deece66d,0x5851f42d4c957f2d,0x5851f42d4c957f2d,
0x5851f42d4c957f2d,0xb5026f5aa96619e9,0x000038eb3ffff6d3, 
```

as you can see few values in this signature are duplicated, this is made on purpose, this will cause to generate **logical** signature, that will require the following (this is **little endian**, so bytes are reversed):
  * `6de6ecde05000000` pattern will have to occur **twice or more times in the file**
  * `e91966a95a6f02b5` pattern will have to occur in the file
  * `2d7f954c2df45158` pattern will have to occur **three times or more in the file**
  * `d3f6ff3feb380000` pattern will have to occur in the file

To summarize this, following two signatures will be generated (in ldb file):
```
UPX miniacc [64.lil.LOGIC];Target:0;(0>2)&1&(2>3)&3;6de6ecde05000000;e91966a95a6f02b5;2d7f954c2df45158;d3f6ff3feb380000
UPX miniacc [64.big.LOGIC];Target:0;(0>2)&1&(2>3)&3;00000005deece66d;b5026f5aa96619e9;5851f42d4c957f2d;000038eb3ffff6d3
```

## other types ##

`STRING` and `ASCII` are actually **REQUIRED** for ascii and string signatures (mainly to simplify code and logic)

`CRC` is a special kind of signature, for which you only need to specify polynomial, for each there will be 4 signatures generated, by combining endianness and reflection: (lil,big)x(reflected,non-reflected).
The tables are generated using [PyCrc](http://www.tty1.net/pycrc/index_en.html)

# Signature data #

As you've seen above In case of non-ascii,non-string signatures, the signature itself contains the data as hex values (BYTEs, WORDs, DWORDs, QWORDs).

But keep in mind that the signature itself is generated based on **bit-length** specifier, so for example, for this signature:
```
TITLE:Generic squared map

TYPE:8,16,32
DATA:
0x00,0x01,0x04,0x05,0x10,0x11,0x14,0x15,0x40,0x41,0x44,0x45,0x50,0x51,0x54,0x55, 
```
there will be five signatures generated:
  * Generic squared map [8.byt.16]
  * Generic squared map [16.lil.32], Generic squared map [16.big.32]
  * Generic squared map [32.lil.64], Generic squared map [32.big.64]

(ofc for 8-bit length little/big endian sigs are not generated)

In some cases it may be easier/better to specify signature in decimal, e.g:
```
TITLE:GSM table gsm_B

TYPE:16
DATA:
     0,     0,  2048, -2560,    94, -1792,  -341, -1144, 
```

The negative values should be properly changed based on **bit-length** specifier.

In cases where negative value doesn't fit, there will be warning,
if positive value, doesn't fit, the process should be broken, and the **clamifier.py** should quit with some more or less sensible error message.

Mentioned warning, looks like this: ` [-] warning overflow found in sig:  G726 40kbit/s 5bits per sample table (iquant_tbl)`, that signature is specified in following way:
```
TITLE:G726 40kbit/s 5bits per sample table (iquant_tbl) 

TYPE:16,32
DATA:
-2147483648,        -66,         28,        104,        169,        224,        274,        318,
        358,        395,        429,        459,        488,        514,        539,        566,
        566,        539,        514,        488,        459,        429,        395,        358,
        318,        274,        224,        169,        104,         28,        -66,-2147483648, 
```

So the warning is printed because "-2147483648" obviously doesn't fit in 16-bits.

Parser will try to do "it's best", and it will try to cast it, as it would [normaly be casted in C](http://ideone.com/wJOmd)

## STRING / ASCII ##

those are rather self-explantory:
```
TITLE:Bzip2 signature

TYPE:STRING:8
DATA:
"BZh91A"

----

TITLE:rfc3548 Base 32 Encoding

TYPE:ASCII:8,32
DATA:
'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
'Q','R','S','T','U','V','W','X','Y','Z','2','3','4','5','6','7',
```

# FLOAT signatures #

As I've said before, `FLOAT` signatures have been replaced by they hex counterparts (it actually doesn't make sense to keep such sigs in "plain-text").

Every float signature, has been replaced by two signatures (one for 64-bit doubles, one for 32-bit floats):
```
TITLE:libavcodec COOK cplscale3 (flt64)

TYPE:64
DATA:
0x3fef66a4e0000002,0x3fedfbe25ffffffe,0x3fec07a7c0000004,0x3fe6a09e5ffffffc,
0x3fdee0223ffffffc,0x3fd65b849ffffffa,0x3fc8a6b4dfffffee,

----

TITLE:libavcodec COOK cplscale3 (flt32)

TYPE:32
DATA:
0x3f7b3527,0x3f6fdf13,0x3f603d3e,0x3f3504f3,0x3ef70112,0x3eb2dc25,0x3e4535a7, 
```

Yes, this is definitely loss in readability, but gain in **portability**