# Security: Renderer segfault when a malformed png file is loaded.

| Field | Value |
|-------|-------|
| **Issue ID** | [40079217](https://issues.chromium.org/issues/40079217) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI |
| **Reporter** | ao...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2010-02-14 |
| **Bounty** | $500.00 |

## Description

Loading the attached png file or a page containing it causes two 
segmentation faults and a sad tab in 32-bit Ubuntu, and either normal 
error behavior, tab getting stuck in loading or a browser death via 
segmentation fault (memory corruption or a double free) in Fedora 12 on 
x86_64.

To reproduce the issue, open the attached png file or a page containing 
it.

The issue may be related to #35446. This one however uses a different 
file format and arises when just one file is opened or included in a 
page, so I reported it separately.

This issue occurs at least in Linux using the following versions:

Chromium: 5.0.307.7 (Developer Build 38400) Ubuntu / Ubuntu 9.10 / Linux 
genopad 2.6.31-19-generic #56-Ubuntu SMP Thu Jan 28 01:26:53 UTC 2010 
i686 GNU/Linux

Google Chrome: 5.0.307.7 (Official Build 38400) beta / Fedora 12 /x86_64

The double free gives a rather uninformative memory dump. If you fail to 
reproduce this and it is not already fixed in ToT, I can try to get a 
backtrace or some other information if you give some instructions.

I have no idea whether this is exploitable. Easily triggerable 
segmentation faults can turn out to be such, so I'm reporting it here.


## Attachments

- [bad.png](attachments/bad.png) (image/x-png, 6.2 KB)
- [png.jpeg](attachments/png.jpeg) (image/jpeg, 30.6 KB)
- [chrome-329.tar.gz](attachments/chrome-329.tar.gz) (application/x-gzip, 27.8 KB)
- [segv-18d2-gdb.txt](attachments/segv-18d2-gdb.txt) (text/plain, English; charset=us-ascii, 6.1 KB)

## Timeline

### ao...@gmail.com (2010-02-15)

I just noticed there is also a daily chromium feed for Ubuntu. The issue also 
affects the current one (5.0.329.0 (Developer Build 39037) Ubuntu). The attached 
archive contains a few extra images, each causing the segmentation fault at a 
different address, but having the same ip and all but one the same sp. Probably the 
same bug, but added here in case they might be of use in checking the fix.

### sk...@chromium.org (2010-02-17)

I got the html file with the images in chrome-329.tar.gz to crash Chromium 5.0.307.1 on 
Windows Vista x64 once, outside a debugger. In a debugger, I was unable to reproduce, 
so I can't really add anything.

### ao...@gmail.com (2010-02-17)

Here is a gdb trace from the Chromium	5.0.330.0 (Developer Build 39077) Ubuntu 
when opening the first png file. Seems to be a libpng thing. Ubuntu currently has 
1.2.37-1.

I made a quick shotgun test around the images in chrome-329.tar.gz. In Linux almost 
all of the over a thousand derived files which also caused the error had unique 
eips at constant offsets of one kilobyte or so. Hopefully that's not due to an 
indirect jump or a return ;) In case you want to try out more images, some are now 
at http://kiwi.cabal.fi/misc/chromium-35732/images.html.

### ao...@gmail.com (2010-02-17)

No jumps, it's just where the malloc_consolidate happens to be. With some more
debugging symbols the top of backtrace begins:
#0  malloc_consolidate (av=<value optimized out>) at malloc.c:5084
#1  0x0121b4e2 in _int_malloc (av=<value optimized out>, 
    bytes=<value optimized out>) at malloc.c:4338
#2  0x0121d898 in *__GI___libc_malloc (bytes=744) at malloc.c:3638
#3  0x085d2a17 in malloc (size=744) at base/process_util_linux.cc:575
#4  0x002f7b58 in ?? () from /usr/lib/libpng12.so.0
#5  0x002edab9 in png_create_read_struct_2 () from /usr/lib/libpng12.so.0
#6  0x002edeba in png_create_read_struct () from /usr/lib/libpng12.so.0
#7  0x08d0c308 in PNGImageReader (this=0xa320a98, data=0xa3010c8,allDataReceived=true)
    at third_party/WebKit/WebCore/platform/image-decoders/png/PNGImageDecoder.cpp:82


### sk...@chromium.org (2010-02-17)

I'll put an analysis of the contents of each file here, which may help track down the 
root cause(s):

### sk...@chromium.org (2010-02-17)

00000000+222C42CD segv-18d2.png = PNG {
                    // *** Warning: expected at least one "IEND" chunk
00000000+00000008   header = struct PNG_HEADER { // 0x5|5 members
00000000+00000001     0x89 = BYTE: 0x89|137
00000001+00000003     Signature = string(0x3|3 bytes): 'PNG'
00000004+00000002     CR_LF = string(0x2|2 bytes): '\r\n'
00000006+00000001     ESC = string(0x1|1 bytes): '\x1a'
00000007+00000001     LF = string(0x1|1 bytes): '\n'
00000007            } // end struct PNG_HEADER header
00000008+00000019   chunk_1 = PNG_CHUNK {
00000008+00000004     length = DWORD: 0x0000000D|13
0000000C+00000004     type = string(0x4|4 bytes): 'IHDR' // critical, public, not safe to copy
-- chunk data ------------------------------------------------------------------
                      data = 0xD|13 bytes
00000000+0000000D     data = struct PNG_IHDR { // 0x7|7 members
00000000+00000004       Width = DWORD: 0x000000A7|167 // W*H => 0xA3BD|41917
00000004+00000004       Height = DWORD: 0x000000FB|251
00000008+00000001       BitDepth = BYTE: 0x08|8
00000009+00000001       ColorType = BYTE: 0x06|6 // color used, alpha channel used
0000000A+00000001       Compression = BYTE: 0x00|0 // deflate/inflate with 32K sliding window
0000000B+00000001       Filter = BYTE: 0x00|0 // adaptive filtering with five basic filter types
0000000C+00000001       Interlace = BYTE: 0x00|0 // no interlace
0000000C              } // end struct PNG_IHDR data
--------------------------------------------------------------------------------
0000001D+00000004     crc = DWORD: 0x0F5A8460|257590368
                      // *** Warning: actual calculated crc is 0xD9262661
00000020            } // end PNG_CHUNK chunk_1
00000021+00000012   chunk_2 = PNG_CHUNK {
00000021+00000004     length = DWORD: 0x00000006|6
00000025+00000004     type = string(0x4|4 bytes): 'bKGD' // ancillary, private, safe to copy
                      // *** Warning: expected third character to be [A-Z]
00000029+00000006     data = string(0x6|6 bytes): '\x00\xff\x00\xff\x00\xff'
0000002F+00000004     crc = DWORD: 0xA0BDA793|2696783763
                      // *** Warning: actual calculated crc is 0xE5681335
00000032            } // end PNG_CHUNK chunk_2
00000033+00001867   chunk_3 = PNG_CHUNK {
00000033+00000004     length = DWORD: 0x0000185B|6235
00000037+00000004     type = string(0x4|4 bytes): 'IATx' // critical, public, not safe to copy
                      // *** Warning: expected critical chunk value to be "IHDR", "PLTE", "IDAT" or "IEND"
0000003B+0000185B     data = string(0x185B|6235 bytes): '\x9c\xed\xdd{PT\xe7\xfd\x06\xf0\xe7\xb0\xbb(Y\xee...'
00001896+00000004     crc = DWORD: 0x4458544E|1146639438
                      // *** Warning: actual calculated crc is 0x895BB93D
00001899            } // end PNG_CHUNK chunk_3
0000189A+222C2A33   chunk_4 = PNG_CHUNK {
0000189A+00000004     length = DWORD: 0x222C2A27|573319719
0000189E+00000004     type = string(0x4|4 bytes): '\x11\x16\x95\x93'
                      // *** Warning: expected first character to be [A-Za-z]
                      // *** Warning: expected second character to be [A-Za-z]
                      // *** Warning: expected third character to be [A-Z]
                      // *** Warning: expected fourth character to be [A-Za-z]
000018A2+222C2A27     data = string(0x222C2A27|573319719 bytes): '\x08\x8b\xcaI\x84E\xe5$\xc2R\x02\xf8\x9ew\x08B\x8...'
                      // *** Warning: string ends 0x222C29FF|573319679 bytes beyond end of stream
                      // *** Warning: string ends 0x222C29FF|573319679 bytes beyond end of container
222C42C9+00000004     crc = DWORD: 0x00000000|0
                      // *** Warning: value starts 0x222C29FF|573319679 bytes beyond end of stream
                      // *** Warning: value ends 0x222C29FF|573319679 bytes beyond end of container
                      // *** Warning: actual calculated crc is 0x37568439
222C42CC            } // end PNG_CHUNK chunk_4
222C42CC          } // end PNG segv-18d2.png

(Please ignore the CRC warnings - I'm probably calculating them wrong as valid images get those as well)
Oddities:
- "IATx" is not a critical header, so it should not start with a capital.
- 4th chunk is corrupt: the size is too large and it has an invalid type descriptor.

### sk...@chromium.org (2010-02-17)

00000000+BDF3DFB3 segv-33d2.png = PNG {
                    // *** Warning: expected at least one "IEND" chunk
00000000+00000008   header = struct PNG_HEADER { // 0x5|5 members
00000000+00000001     0x89 = BYTE: 0x89|137
00000001+00000003     Signature = string(0x3|3 bytes): 'PNG'
00000004+00000002     CR_LF = string(0x2|2 bytes): '\r\n'
00000006+00000001     ESC = string(0x1|1 bytes): '\x1a'
00000007+00000001     LF = string(0x1|1 bytes): '\n'
00000007            } // end struct PNG_HEADER header
00000008+00000019   chunk_1 = PNG_CHUNK {
00000008+00000004     length = DWORD: 0x0000000D|13
0000000C+00000004     type = string(0x4|4 bytes): 'IHDR' // critical, public, not safe to copy
-- chunk data ------------------------------------------------------------------
                      data = 0xD|13 bytes
00000000+0000000D     data = struct PNG_IHDR { // 0x7|7 members
00000000+00000004       Width = DWORD: 0x00000124|292 // W*H => 0xFF80|65408
00000004+00000004       Height = DWORD: 0x000000E0|224
00000008+00000001       BitDepth = BYTE: 0x08|8
00000009+00000001       ColorType = BYTE: 0x06|6 // color used, alpha channel used
0000000A+00000001       Compression = BYTE: 0x00|0 // deflate/inflate with 32K sliding window
0000000B+00000001       Filter = BYTE: 0x00|0 // adaptive filtering with five basic filter types
0000000C+00000001       Interlace = BYTE: 0x00|0 // no interlace
0000000C              } // end struct PNG_IHDR data
--------------------------------------------------------------------------------
0000001D+00000004     crc = DWORD: 0xAAF71BFA|2868321274
                      // *** Warning: actual calculated crc is 0xD07D8869
00000020            } // end PNG_CHUNK chunk_1
00000021+00000012   chunk_2 = PNG_CHUNK {
00000021+00000004     length = DWORD: 0x00000006|6
00000025+00000004     type = string(0x4|4 bytes): 'bKGD' // ancillary, private, safe to copy
                      // *** Warning: expected third character to be [A-Z]
00000029+00000006     data = string(0x6|6 bytes): '\x00\xff\x00\xff\x00\xff'
0000002F+00000004     crc = DWORD: 0xA0BDA793|2696783763
                      // *** Warning: actual calculated crc is 0xE5681335
00000032            } // end PNG_CHUNK chunk_2
00000033+0000200C   chunk_3 = PNG_CHUNK {
00000033+00000004     length = DWORD: 0x00002000|8192
00000037+00000004     type = string(0x4|4 bytes): 'IADT' // critical, public, not safe to copy
                      // *** Warning: expected critical chunk value to be "IHDR", "PLTE", "IDAT" or "IEND"
0000003B+00002000     data = string(0x2000|8192 bytes): 'x\x9c\xed\xdd{xLw\xfe\x07\xf0\xf7\xc9Ln#\xa5$.\x1...'
0000203B+00000004     crc = DWORD: 0x73E74E41|1944538689
                      // *** Warning: actual calculated crc is 0x5F6B345C
0000203E            } // end PNG_CHUNK chunk_3
0000203F+BDF3BF74   chunk_4 = PNG_CHUNK {
0000203F+00000004     length = DWORD: 0xBDF3BF68|3186868072
00002043+00000004     type = string(0x4|4 bytes): '\xd6\xacY\x88'
                      // *** Warning: expected first character to be [A-Za-z]
                      // *** Warning: expected second character to be [A-Za-z]
                      // *** Warning: expected third character to be [A-Z]
                      // *** Warning: expected fourth character to be [A-Za-z]
00002047+BDF3BF68     data = string(0xBDF3BF68|3186868072 bytes): '\x8a\x8aBdd$\xda\xda\xda:\xbc\x1f\x15\x00\xd1\x1a...'
                      // *** Warning: string ends 0xBDF3ABE5|3186863077 bytes beyond end of stream
                      // *** Warning: string ends 0xBDF3ABE5|3186863077 bytes beyond end of container
BDF3DFAF+00000004     crc = DWORD: 0x00000000|0
                      // *** Warning: value starts 0xBDF3ABE5|3186863077 bytes beyond end of stream
                      // *** Warning: value ends 0xBDF3ABE5|3186863077 bytes beyond end of container
                      // *** Warning: actual calculated crc is 0x5F469632
BDF3DFB2            } // end PNG_CHUNK chunk_4
BDF3DFB2          } // end PNG segv-33d2.png

Oddities:
- "IADT" is not a critical header, so it should not start with a capital.
- 4th chunk is corrupt: the size is too large and it has an invalid type descriptor.

### sk...@chromium.org (2010-02-17)

00000000+F38B12B8 segv-4621.png = PNG {
                    // *** Warning: expected at least one "IEND" chunk
00000000+00000008   header = struct PNG_HEADER { // 0x5|5 members
00000000+00000001     0x89 = BYTE: 0x89|137
00000001+00000003     Signature = string(0x3|3 bytes): 'PNG'
00000004+00000002     CR_LF = string(0x2|2 bytes): '\r\n'
00000006+00000001     ESC = string(0x1|1 bytes): '\x1a'
00000007+00000001     LF = string(0x1|1 bytes): '\n'
00000007            } // end struct PNG_HEADER header
00000008+00000019   chunk_1 = PNG_CHUNK {
00000008+00000004     length = DWORD: 0x0000000D|13
0000000C+00000004     type = string(0x4|4 bytes): 'IHDR' // critical, public, not safe to copy
-- chunk data ------------------------------------------------------------------
                      data = 0xD|13 bytes
00000000+0000000D     data = struct PNG_IHDR { // 0x7|7 members
00000000+00000004       Width = DWORD: 0x000000A7|167 // W*H => 0xA3BD|41917
00000004+00000004       Height = DWORD: 0x000000FB|251
00000008+00000001       BitDepth = BYTE: 0x08|8
00000009+00000001       ColorType = BYTE: 0x06|6 // color used, alpha channel used
0000000A+00000001       Compression = BYTE: 0x00|0 // deflate/inflate with 32K sliding window
0000000B+00000001       Filter = BYTE: 0x00|0 // adaptive filtering with five basic filter types
0000000C+00000001       Interlace = BYTE: 0x00|0 // no interlace
0000000C              } // end struct PNG_IHDR data
--------------------------------------------------------------------------------
0000001D+00000004     crc = DWORD: 0x0F5A8460|257590368
                      // *** Warning: actual calculated crc is 0xD9262661
00000020            } // end PNG_CHUNK chunk_1
00000021+00000012   chunk_2 = PNG_CHUNK {
00000021+00000004     length = DWORD: 0x00000006|6
00000025+00000004     type = string(0x4|4 bytes): 'bKGD' // ancillary, private, safe to copy
                      // *** Warning: expected third character to be [A-Z]
00000029+00000006     data = string(0x6|6 bytes): '\x00\xff\x00\xff\x00\xff'
0000002F+00000004     crc = DWORD: 0xA0BDA793|2696783763
                      // *** Warning: actual calculated crc is 0xE5681335
00000032            } // end PNG_CHUNK chunk_2
00000033+00001867   chunk_3 = PNG_CHUNK {
00000033+00000004     length = DWORD: 0x0000185B|6235
00000037+00000004     type = string(0x4|4 bytes): 'IADT' // critical, public, not safe to copy
                      // *** Warning: expected critical chunk value to be "IHDR", "PLTE", "IDAT" or "IEND"
0000003B+0000185B     data = string(0x185B|6235 bytes): 'x\x9c\xed\xdd{PT\xe7\xfd\x06\xf0\xe7\xb0\xbb(Y\xe...'
00001896+00000004     crc = DWORD: 0x86C18307|2260828935
                      // *** Warning: actual calculated crc is 0x16573BFF
00001899            } // end PNG_CHUNK chunk_3
0000189A+F38AFA1E   chunk_4 = PNG_CHUNK {
0000189A+00000004     length = DWORD: 0xF38AFA12|4085971474
0000189E+00000004     type = string(0x4|4 bytes): '*\x00Bz'
                      // *** Warning: expected first character to be [A-Za-z]
                      // *** Warning: expected second character to be [A-Za-z]
                      // *** Warning: expected third character to be [A-Z]
                      // *** Warning: expected fourth character to be [A-Za-z]
000018A2+F38AFA12     data = string(0xF38AFA12|4085971474 bytes): 'h\xf5\xea\xd5\x88\x8d\x8d\xed\xd2}\xd5\xed\xcf\x8...'
                      // *** Warning: string ends 0xF38ACC9B|4085959835 bytes beyond end of stream
                      // *** Warning: string ends 0xF38ACC9B|4085959835 bytes beyond end of container
F38B12B4+00000004     crc = DWORD: 0x00000000|0
                      // *** Warning: value starts 0xF38ACC9B|4085959835 bytes beyond end of stream
                      // *** Warning: value ends 0xF38ACC9B|4085959835 bytes beyond end of container
                      // *** Warning: actual calculated crc is 0x862AECED
F38B12B7            } // end PNG_CHUNK chunk_4
F38B12B7          } // end PNG segv-4621.png

Oddities:
- "IADT" is not a critical header, so it should not start with a capital.
- 4th chunk is corrupt: the size is too large and it has an invalid type descriptor.

### sk...@chromium.org (2010-02-17)

00000000+2AC5E610 segv-8008.png = PNG {
                    // *** Warning: expected at least one "IEND" chunk
00000000+00000008   header = struct PNG_HEADER { // 0x5|5 members
00000000+00000001     0x89 = BYTE: 0x89|137
00000001+00000003     Signature = string(0x3|3 bytes): 'PNG'
00000004+00000002     CR_LF = string(0x2|2 bytes): '\r\n'
00000006+00000001     ESC = string(0x1|1 bytes): '\x1a'
00000007+00000001     LF = string(0x1|1 bytes): '\n'
00000007            } // end struct PNG_HEADER header
00000008+00000019   chunk_1 = PNG_CHUNK {
00000008+00000004     length = DWORD: 0x0000000D|13
0000000C+00000004     type = string(0x4|4 bytes): 'IHDR' // critical, public, not safe to copy
-- chunk data ------------------------------------------------------------------
                      data = 0xD|13 bytes
00000000+0000000D     data = struct PNG_IHDR { // 0x7|7 members
00000000+00000004       Width = DWORD: 0x00000124|292 // W*H => 0xFF80|65408
00000004+00000004       Height = DWORD: 0x000000E0|224
00000008+00000001       BitDepth = BYTE: 0x08|8
00000009+00000001       ColorType = BYTE: 0x06|6 // color used, alpha channel used
0000000A+00000001       Compression = BYTE: 0x00|0 // deflate/inflate with 32K sliding window
0000000B+00000001       Filter = BYTE: 0x00|0 // adaptive filtering with five basic filter types
0000000C+00000001       Interlace = BYTE: 0x00|0 // no interlace
0000000C              } // end struct PNG_IHDR data
--------------------------------------------------------------------------------
0000001D+00000004     crc = DWORD: 0xAAF71BFA|2868321274
                      // *** Warning: actual calculated crc is 0xD07D8869
00000020            } // end PNG_CHUNK chunk_1
00000021+00000012   chunk_2 = PNG_CHUNK {
00000021+00000004     length = DWORD: 0x00000006|6
00000025+00000004     type = string(0x4|4 bytes): 'bKGD' // ancillary, private, safe to copy
                      // *** Warning: expected third character to be [A-Z]
00000029+00000006     data = string(0x6|6 bytes): '\x00\xff\x00\xff\x00\xff'
0000002F+00000004     crc = DWORD: 0xA0BDA793|2696783763
                      // *** Warning: actual calculated crc is 0xE5681335
00000032            } // end PNG_CHUNK chunk_2
00000033+0000200C   chunk_3 = PNG_CHUNK {
00000033+00000004     length = DWORD: 0x00002000|8192
00000037+00000004     type = string(0x4|4 bytes): 'IDAD' // critical, public, not safe to copy
                      // *** Warning: expected critical chunk value to be "IHDR", "PLTE", "IDAT" or "IEND"
0000003B+00002000     data = string(0x2000|8192 bytes): 'ATx\x9c\xed\xdd{xLw\xfe\x07\xf0\xf7\xc9Ln#\xa5$.\...'
0000203B+00000004     crc = DWORD: 0x7A65E7D2|2053498834
                      // *** Warning: actual calculated crc is 0x0FE46A42
0000203E            } // end PNG_CHUNK chunk_3
0000203F+2AC5C5D1   chunk_4 = PNG_CHUNK {
0000203F+00000004     length = DWORD: 0x2AC5C5C5|717604293
00002043+00000004     type = string(0x4|4 bytes): 'pvv\xc6' // ancillary, private, safe to copy
                      // *** Warning: expected third character to be [A-Z]
00002047+2AC5C5C5     data = string(0x2AC5C5C5|717604293 bytes): '\xa3G\x8fp\xea\xd4)\x98\x9b\x9bs\xc9!\x12\x89\x90...'
                      // *** Warning: string ends 0x2AC55083|717574275 bytes beyond end of stream
                      // *** Warning: string ends 0x2AC55083|717574275 bytes beyond end of container
2AC5E60C+00000004     crc = DWORD: 0x00000000|0
                      // *** Warning: value starts 0x2AC55083|717574275 bytes beyond end of stream
                      // *** Warning: value ends 0x2AC55083|717574275 bytes beyond end of container
                      // *** Warning: actual calculated crc is 0x12CDE402
2AC5E60F            } // end PNG_CHUNK chunk_4
2AC5E60F          } // end PNG segv-8008.png

Oddities:
- "IDAD" is not a critical header, so it should not start with a capital.
- 4th chunk is corrupt: the size is too large and it has an invalid type descriptor.

### sk...@chromium.org (2010-02-17)

00000000+222C42CD bad.png = PNG {
                    // *** Warning: expected at least one "IEND" chunk
00000000+00000008   header = struct PNG_HEADER { // 0x5|5 members
00000000+00000001     0x89 = BYTE: 0x89|137
00000001+00000003     Signature = string(0x3|3 bytes): 'PNG'
00000004+00000002     CR_LF = string(0x2|2 bytes): '\r\n'
00000006+00000001     ESC = string(0x1|1 bytes): '\x1a'
00000007+00000001     LF = string(0x1|1 bytes): '\n'
00000007            } // end struct PNG_HEADER header
00000008+00000019   chunk_1 = PNG_CHUNK {
00000008+00000004     length = DWORD: 0x0000000D|13
0000000C+00000004     type = string(0x4|4 bytes): 'IHDR' // critical, public, not safe to copy
-- chunk data ------------------------------------------------------------------
                      data = 0xD|13 bytes
00000000+0000000D     data = struct PNG_IHDR { // 0x7|7 members
00000000+00000004       Width = DWORD: 0x000000A7|167 // W*H => 0xA3BD|41917
00000004+00000004       Height = DWORD: 0x000000FB|251
00000008+00000001       BitDepth = BYTE: 0x08|8
00000009+00000001       ColorType = BYTE: 0x06|6 // color used, alpha channel used
0000000A+00000001       Compression = BYTE: 0x00|0 // deflate/inflate with 32K sliding window
0000000B+00000001       Filter = BYTE: 0x00|0 // adaptive filtering with five basic filter types
0000000C+00000001       Interlace = BYTE: 0x00|0 // no interlace
0000000C              } // end struct PNG_IHDR data
--------------------------------------------------------------------------------
0000001D+00000004     crc = DWORD: 0x0F5A8460|257590368
                      // *** Warning: actual calculated crc is 0xD9262661
00000020            } // end PNG_CHUNK chunk_1
00000021+00000012   chunk_2 = PNG_CHUNK {
00000021+00000004     length = DWORD: 0x00000006|6
00000025+00000004     type = string(0x4|4 bytes): 'bKGD' // ancillary, private, safe to copy
                      // *** Warning: expected third character to be [A-Z]
00000029+00000006     data = string(0x6|6 bytes): '\x00\xff\x00\xff\x00\xff'
0000002F+00000004     crc = DWORD: 0xA0BDA793|2696783763
                      // *** Warning: actual calculated crc is 0xE5681335
00000032            } // end PNG_CHUNK chunk_2
00000033+00001867   chunk_3 = PNG_CHUNK {
00000033+00000004     length = DWORD: 0x0000185B|6235
00000037+00000004     type = string(0x4|4 bytes): 'IATx' // critical, public, not safe to copy
                      // *** Warning: expected critical chunk value to be "IHDR", "PLTE", "IDAT" or "IEND"
0000003B+0000185B     data = string(0x185B|6235 bytes): '\x9c\xed\xdd{PT\xe7\xfd\x06\xf0\xe7\xb0\xbb(Y\xee...'
00001896+00000004     crc = DWORD: 0x4458544E|1146639438
                      // *** Warning: actual calculated crc is 0x895BB93D
00001899            } // end PNG_CHUNK chunk_3
0000189A+222C2A33   chunk_4 = PNG_CHUNK {
0000189A+00000004     length = DWORD: 0x222C2A27|573319719
0000189E+00000004     type = string(0x4|4 bytes): '\x11\x16\x95\x93'
                      // *** Warning: expected first character to be [A-Za-z]
                      // *** Warning: expected second character to be [A-Za-z]
                      // *** Warning: expected third character to be [A-Z]
                      // *** Warning: expected fourth character to be [A-Za-z]
000018A2+222C2A27     data = string(0x222C2A27|573319719 bytes): '\x08\x8b\xcaI\x84E\xe5$\xc2R\x02\xf8\x9ew\x08B\x8...'
                      // *** Warning: string ends 0x222C29FF|573319679 bytes beyond end of stream
                      // *** Warning: string ends 0x222C29FF|573319679 bytes beyond end of container
222C42C9+00000004     crc = DWORD: 0x00000000|0
                      // *** Warning: value starts 0x222C29FF|573319679 bytes beyond end of stream
                      // *** Warning: value ends 0x222C29FF|573319679 bytes beyond end of container
                      // *** Warning: actual calculated crc is 0x37568439
222C42CC            } // end PNG_CHUNK chunk_4
222C42CC          } // end PNG bad.png

Oddities:
- "IATx" is not a critical header, so it should not start with a capital.
- 4th chunk is corrupt: the size is too large and it has an invalid type descriptor.

There seems to be a clear pattern here: an invalid "critical" tag followed by a corrupted 4th chunk.

### sk...@chromium.org (2010-02-17)

Hey, that link (http://kiwi.cabal.fi/misc/chromium-35732/images.html) seems to trigger AVs pretty easily. I'm seeing evidency of memory corruption in tcmalloc.

001fe11c 6300b65e chrome_62f80000!tcmalloc::SLL_Next(void * t = 0x000029b0)+0x6 [i:\trunk\src\third_party\tcmalloc\chromium\src\linked_list.h @ 42]
001fe12c 6300b628 chrome_62f80000!tcmalloc::SLL_Pop(void ** list = 0x00710038)+0x1e [i:\trunk\src\third_party\tcmalloc\chromium\src\linked_list.h @ 56]
001fe148 6300b565 chrome_62f80000!tcmalloc::ThreadCache::FreeList::Pop(void)+0x88 [i:\trunk\src\third_party\tcmalloc\chromium\src\thread_cache.h @ 198]
001fe16c 6300bafc chrome_62f80000!tcmalloc::ThreadCache::Allocate(unsigned int size = 0x20)+0xc5 [i:\trunk\src\third_party\tcmalloc\chromium\src\thread_cache.h @ 344]
001fe184 6300cf1b chrome_62f80000!`anonymous namespace'::do_malloc(unsigned int size = 0x20)+0x8c [i:\trunk\src\third_party\tcmalloc\chromium\src\tcmalloc.cc @ 818]
001fe198 6300d394 chrome_62f80000!malloc(unsigned int size = 0x20)+0x5b [i:\trunk\src\base\allocator\allocator_shim.cc @ 110]
001fe1a8 6300d36e chrome_62f80000!generic_cpp_alloc(unsigned int size = 0x20, bool nothrow = false)+0x14 [i:\trunk\src\base\allocator\generic_allocators.cc @ 16]
001fe1b8 630d80fa chrome_62f80000!operator new(unsigned int size = 0x20)+0xe [i:\trunk\src\base\allocator\generic_allocators.cc @ 28]
001fe1dc 630cefc7 chrome_62f80000!IPC::ChannelProxy::Send(class IPC::Message * message = 0x063f2d70)+0x4a [i:\trunk\src\ipc\ipc_channel_proxy.cc @ 280]
001fe2cc 630cef64 chrome_62f80000!IPC::SyncChannel::SendWithTimeout(class IPC::Message * message = 0x063f2d70, int timeout_ms = -1)+0x47 [i:\trunk\src\ipc\ipc_sync_channel.cc @ 387]
001fe2e4 63ff6247 chrome_62f80000!IPC::SyncChannel::Send(class IPC::Message * message = 0x063f2d70)+0x24 [i:\trunk\src\ipc\ipc_sync_channel.cc @ 381]
001fe308 634fdf1d chrome_62f80000!ChildThread::Send(class IPC::Message * msg = 0x063f2d70)+0x87 [i:\trunk\src\chrome\common\child_thread.cc @ 83]
001fe318 6400071a chrome_62f80000!RenderThread::Send(class IPC::Message * msg = 0x063f2d70)+0x1d [i:\trunk\src\chrome\renderer\render_thread.h @ 98]
001fe4cc 64006902 chrome_62f80000!ResourceDispatcher::OnReceivedData(class IPC::Message * message = 0x02e2a528, int request_id = 31, void * shm_handle = 0x0000022c, int data_len = 8192)+0x9a [i:\trunk\src\chrome\common\resource_dispatcher.cc @ 358]
001fe4fc 640016f8 chrome_62f80000!IPC::MessageWithTuple<Tuple3<int,void *,int> >::Dispatch<ResourceDispatcher,int,void *,int>(class IPC::Message * msg = 0x02e2a528, class ResourceDispatcher * obj = 0x02da9dc0, <function> * func = 0x64000680)+0x52 [i:\trunk\src\ipc\ipc_message_utils.h @ 1028]
001fe5b4 6400014a chrome_62f80000!ResourceDispatcher::DispatchMessageW(class IPC::Message * message = 0x02e2a528)+0xd8 [i:\trunk\src\chrome\common\resource_dispatcher.cc @ 519]
001fe7f4 63ff6485 chrome_62f80000!ResourceDispatcher::OnMessageReceived(class IPC::Message * message = 0x02e2a528)+0x36a [i:\trunk\src\chrome\common\resource_dispatcher.cc @ 295]
001fe8c8 630d7ce5 chrome_62f80000!ChildThread::OnMessageReceived(class IPC::Message * msg = 0x02e2a528)+0x45 [i:\trunk\src\chrome\common\child_thread.cc @ 109]
001fe8e0 630dab03 chrome_62f80000!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message * message = 0x02e2a528)+0x85 [i:\trunk\src\ipc\ipc_channel_proxy.cc @ 204]
001fe8f0 630d9f15 chrome_62f80000!DispatchToMethod<IPC::ChannelProxy::Context,void (class IPC::ChannelProxy::Context * obj = 0x02da6180, <function> * method = 0x630d7c60, struct Tuple1<IPC::Message> * arg = 0x02e2a528)+0x13 [i:\trunk\src\base\tuple.h @ 422]


### la...@chromium.org (2010-02-19)

Using an automated filter to classify this issue into an area...gulp

### sc...@gmail.com (2010-02-19)

Oo! Great bug, aohelin!
Provisionally good for a reward :)
Reproduces on x86_64, same stack trace as #4

#0  0x00007ffff258d2d0 in malloc_consolidate () from /lib/libc.so.6
#1  0x00007ffff258f922 in _int_malloc () from /lib/libc.so.6
#2  0x00007ffff2591360 in malloc () from /lib/libc.so.6
#3  0x0000000000c30c5f in malloc (size=1200) at base/process_util_linux.cc:575
#4  0x00007ffff3742bf8 in ?? () from /usr/lib/libpng12.so.0
#5  0x00007ffff373a0b6 in png_create_read_struct_2 ()
   from /usr/lib/libpng12.so.0
#6  0x00007ffff373a3b7 in png_create_read_struct () from /usr/lib/libpng12.so.0
#7  0x000000000177a554 in PNGImageReader (this=0x7fffe86da990, 
    decoder=0x7fffe86f7020)
    at third_party/WebKit/WebCore/platform/image-decoders/png/PNGImageDecoder.cpp:102
#8  0x000000000177a028 in WebCore::PNGImageDecoder::setData (
    this=0x7fffe86f7020, data=0x7fffe820db70, allDataReceived=true)
    at third_party/WebKit/WebCore/platform/image-decoders/png/PNGImageDecoder.cpp:188
#9  0x0000000001763aba in WebCore::ImageSource::setData (this=0x7fffe86f6fa0, 
    data=0x7fffe820db70, allDataReceived=true)
    at third_party/WebKit/WebCore/platform/graphics/ImageSource.cpp:87
#10 0x0000000001763b5a in WebCore::ImageSource::clear (this=0x7fffe86f6fa0, 
    destroyAll=true, clearBeforeFrame=0, data=0x7fffe820db70, 
    allDataReceived=true)
    at third_party/WebKit/WebCore/platform/graphics/ImageSource.cpp:61
---Type <return> to continue, or q <return> to quit---
#11 0x000000000174360b in WebCore::BitmapImage::destroyDecodedData (
    this=0x7fffe86f6f80, destroyAll=true)
    at third_party/WebKit/WebCore/platform/graphics/BitmapImage.cpp:89
#12 0x0000000001671068 in WebCore::CachedImage::destroyDecodedData (
    this=0x7fffe81f25a0)
    at third_party/WebKit/WebCore/loader/CachedImage.cpp:335
#13 0x000000000167108a in WebCore::CachedImage::clear (this=0x7fffe81f25a0)
    at third_party/WebKit/WebCore/loader/CachedImage.cpp:229
#14 0x00000000016710c5 in WebCore::CachedImage::error (this=0x7fffe81f25a0)
    at third_party/WebKit/WebCore/loader/CachedImage.cpp:307
#15 0x0000000001671a52 in WebCore::CachedImage::data (this=0x7fffe81f25a0, 
    data=..., allDataReceived=true)
    at third_party/WebKit/WebCore/loader/CachedImage.cpp:285
#16 0x00000000016b6597 in WebCore::Loader::Host::didFinishLoading (
    this=0x7fffe81da270, loader=0x7fffe81f6440)
    at third_party/WebKit/WebCore/loader/loader.cpp:397
#17 0x0000000001ac22dd in WebCore::SubresourceLoader::didFinishLoading (
    this=0x7fffe81f6440)
    at third_party/WebKit/WebCore/loader/SubresourceLoader.cpp:184
#18 0x00000000016ae6e2 in WebCore::ResourceLoader::didFinishLoading (
    this=0x7fffe81f6440)
    at third_party/WebKit/WebCore/loader/ResourceLoader.cpp:403
#19 0x000000000205ad0c in WebCore::ResourceHandleInternal::didFinishLoading (
---Type <return> to continue, or q <return> to quit---
    this=0x4d329f0)
    at third_party/WebKit/WebKit/chromium/src/ResourceHandle.cpp:147
#20 0x0000000001d5c0c0 in webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest 
(this=0x4d79d50, status=..., security_info="")
    at webkit/glue/weburlloader_impl.cc:543
#21 0x0000000001f8a579 in ResourceDispatcher::OnRequestComplete (
    this=0x7fffe808c5f0, request_id=8, status=..., security_info="")
    at chrome/common/resource_dispatcher.cc:461


### sc...@gmail.com (2010-02-19)

kiwi.cabal.fi not responding any more - hope I didn't hit it too hard :(

### ao...@gmail.com (2010-02-19)

Yay, you caused a bug which has appeared about twice a year to raise it's head. Now I
finally have a trace on that one. This seems to go both ways =)

### sc...@gmail.com (2010-02-19)

I will find an owner for this...

### ag...@chromium.org (2010-02-19)

Analysis: as expected, all the backtraces are bogus and just show evidence of memory 
corruption. The failure occurs like this:

(line numbers reference third_party/WebKit/WebCore/platform/image-
decoders/png/PNGImageDecoder.cpp@54996)

1) the size of a PNG is requested (PNGImageDecoder::isSizeAvailable:192)
2) We don't have the size, so we call decode
3) In decode (PNGImageDecoder::decode:397), we call m_reader->decode
4) We process one chunk of data (PNGImageReader::decode:142)
5) We check to see if we have the size yet, by calling isSizeAvailable
6) Steps 1..4 repeat because we recursed
7) This time, however, libpng throws an error
8) We end up in decodingFailed:57, which calls PNGImageDecoder::decodingFailed:215, 
which sets 
m_failed = true
9) decodingFailed:59 longjmps out to the inner activation frame for 
PNGImageReader::decode 
(line 133)
10) we return to PNGImageDecoder::decode:399 where the m_failed flag causes us to 
free the 
PNGImageReader
11) Stack frames unwind until we end up in the outer PNGImageReader::decode (from 
step 5)
12) We're screwed. We're walking on free() memory, corrupting malloc's structures. 
Game over.

Am filing a WebKit bug with the patch. Will update this bug once done.

### ag...@chromium.org (2010-02-19)

https://bugs.webkit.org/show_bug.cgi?id=35167

### sc...@gmail.com (2010-02-22)

[Empty comment from Monorail migration]

### pk...@chromium.org (2010-02-22)

Upstream bug is fixed in r55108.  I will merge this to 249s and 249.  Please speak up 
(or just address the issue) if any other branches need merging.

### sc...@gmail.com (2010-02-22)

Using "FixUnreleased" so I can track it as an unreleased security bug.

Do we believe this affects 249 / 249s?

### pk...@chromium.org (2010-02-22)

You got in just ahead of me.  This bug does not exist in 249s or 249.  It was 
introduced on trunk somewhat recently by Yong Li upstream.  So unless we intend to do a 
patch to 307 for Linux (Mac doesn't use this file), I don't think it needs merging 
anywhere.

### sc...@gmail.com (2010-02-24)

@aohelin: thanks so much for your help with this hard-to-reproduce bug :)
We'd like to offer you one of our $500 rewards. Please e-mail me, cevans@chromium.org 
if you wish to accept!

### sk...@chromium.org (2010-02-28)

Funny fact: the only thing needed to trigger this is a file with a png extention and a 
png header: "echo 89PNG>test.png" should suffice to trigger it according to my 
framework.

### js...@chromium.org (2010-06-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: assuming these security changes did not impact stable based on some fuzzy filtering.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/35732?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/32281]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079217)*
