# Heap-use-after-free in SkARGB32_Black_Blitter::blitAntiH

| Field | Value |
|-------|-------|
| **Issue ID** | [40059942](https://issues.chromium.org/issues/40059942) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-06-19 |
| **Bounty** | $1,000.00 |

## Description

Repro-file as attachment.

Chrome version: ASAN 21.0.1170.0
OS:Ubuntu 11.04 x86_64

I hope you can get the repro-file reduced with better results than I did.

ASAN Report snippet:

=================================================================
==3174== ERROR: AddressSanitizer heap-use-after-free on address 0x7fb2b939a004 at pc 0x7fb2c99293f2 bp 0x7fff6daba2d0 sp 0x7fff6daba2c8
READ of size 4 at 0x7fb2b939a004 thread T0
    #0 0x7fb2c99293f2 in SkARGB32_Black_Blitter::blitAntiH(int, int, unsigned char const*, short const*) ???:0
    #1 0x7fb2c9876be2 in hline(int, int, int, int, SkBlitter*, int) third_party/skia/src/core/SkScan_Antihair.cpp:0
    #2 0x7fb2c9873160 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:0
    #3 0x7fb2c9872b62 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:0
    #4 0x7fb2c9872b62 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:0
    #5 0x7fb2c9872b62 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:0
    #6 0x7fb2c9872b62 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:0

.
.
.



## Attachments

- [SkARGB32BlackBlitterblitAntiHint37b.html](attachments/SkARGB32BlackBlitterblitAntiHint37b.html) (text/html; charset=us-ascii, 142.6 KB)
- [symbolized_log.txt](attachments/symbolized_log.txt) (text/x-c; charset=us-ascii, 8.4 KB)
- [crbug133571-cf-minimized.html](attachments/crbug133571-cf-minimized.html) (application/octet-stream; charset=binary, 20.2 KB)
- [asan-log-133571.txt](attachments/asan-log-133571.txt) (text/x-c; charset=us-ascii, 16.3 KB)

## Timeline

### pa...@chromium.org (2012-06-19)

ClusterFuzz report coming soon. reed, it looks like you own the methods in the stack trace; could you and/or epoger please take a look, or point us to someone who knows? Thanks!

### pa...@chromium.org (2012-06-19)

CF is taking forever to find a regression. Going to update the bug with the CF report as-is; given the age of this code I suspect it affects stable.

### pa...@google.com (2012-06-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=64492209

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f0a49a03004
Crash State:
  - crash stack -
  SkARGB32_Black_Blitter::blitAntiH
  hline
  - free stack -
  v8::internal::Assembler::~Assembler
  v8::internal::RegExpImpl::CompileIrregexp
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94L97gqaeGekLGmG2FaWgS8MDlSzdH9JZPkUpNf_SLAM0knV7gOBqEQ9scfBTimUZX4GmFOlZh0YKhQNkZjqnVrVVOriFuR7NC5JnENUqkDqh-6v2EMpGSWvGyNP4TrMJVDFhickrBDFVSlo8xlLf86TCOHzydT_EsBFOLFCicAeqznMhc

### in...@chromium.org (2012-06-20)

Fixing milestone based on clusterfuzz report.

Elliot, Mike, we have a spike of these Skia bugs. can you please help to fix these.

### [Deleted User] (2012-06-20)

[Empty comment from Monorail migration]

### ep...@google.com (2012-06-28)

I'm not ignoring this... I hope to have time to take a stab at reproducing it on Monday.

### js...@chromium.org (2012-06-29)

Bulk Edit: m20 is shipped. Rolling open m19 bugs forward.

### ep...@google.com (2012-07-02)

I can consistently reproduce the ASAN error as follows (on my desktop Goobuntu Linux machine, operating it remotely via NX):

1. Download/unzip asan-linux-release-143037 from https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

2. Launch: ./asan-linux-release-143037/chrome --no-first-run --single-process --disable-gpu-plugin --disable-gpu-rendering --disable-accelerated-compositing --disable-webgl --disable-accelerated-2d-canvas --user-data-dir=/tmp/user_profile_chrome_0

3. View minimized repro case from clusterfuzz report (attached here)

Here's the output I see:

==28322== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fe9ad2be004 at pc 0x7fe9d1c500e2 bp 0x7fe9b3c669d0 sp 0x7fe9b3c669c8
READ of size 4 at 0x7fe9ad2be004 thread T19
    #0 0x7fe9d1c500e2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3c280e2)
    #1 0x7fe9d1b9d342 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b75342)
    #2 0x7fe9d1b998c0 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b718c0)
    #3 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #4 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #5 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #6 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #7 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #8 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #9 0x7fe9d1b992c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b712c2)
    #10 0x7fe9d1b99090 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b71090)
    #11 0x7fe9d1b9f5e4 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b775e4)
    #12 0x7fe9d1b2955d (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3b0155d)
    #13 0x7fe9d1b18a93 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3af0a93)
    #14 0x7fe9d2a83628 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x4a5b628)
    #15 0x7fe9d2726d0c (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x46fed0c)
    #16 0x7fe9d43dcee1 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x63b4ee1)
    #17 0x3482fcf33917 (+0x2d917)
    #18 0x3482fcf31d7a (+0x2bd7a)
    #19 0x3482fcf243bd (+0x1e3bd)
    #20 0x3482fcc098ce (+0x38ce)
    #21 0x3482fcc24961 (+0x1e961)
    #22 0x3482fcc11417 (+0xb417)
    #23 0x7fe9d0f23d15 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x2efbd15)
    #24 0x7fe9d0e61e16 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x2e39e16)
    #25 0x7fe9d2d06b32 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x4cdeb32)
    #26 0x7fe9d2d05aad (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x4cddaad)
    #27 0x7fe9d2cf08d9 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x4cc88d9)
    #28 0x7fe9d35faa50 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x55d2a50)
    #29 0x7fe9d35fa607 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x55d2607)
    #30 0x7fe9d2090f6b (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x4068f6b)
    #31 0x7fe9d2090760 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x4068760)
    #32 0x7fe9d33806f5 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x53586f5)
    #33 0x7fe9d3392cb3 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x536acb3)
    #34 0x7fe9d200dd9c (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3fe5d9c)
    #35 0x7fe9d328f5f7 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x52675f7)
    #36 0x7fe9d29170b8 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x48ef0b8)
    #37 0x7fe9d04aa796 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x2482796)
    #38 0x7fe9d041feb5 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x23f7eb5)
    #39 0x7fe9d04205fc (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x23f85fc)
    #40 0x7fe9d0421b62 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x23f9b62)
    #41 0x7fe9d042b8f7 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x24038f7)
    #42 0x7fe9d041eb02 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x23f6b02)
    #43 0x7fe9d041ccee (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x23f4cee)
    #44 0x7fe9d04a2d8d (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x247ad8d)
    #45 0x7fe9d0497c6c (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x246fc6c)
    #46 0x7fe9d724ac2c (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x9222c2c)
0x7fe9ad2be004 is located 28 bytes to the right of 104-byte region [0x7fe9ad2bdf80,0x7fe9ad2bdfe8)
freed by thread T0 here:
    #0 0x7fe9d724e3a2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x92263a2)
    #1 0x7fe9d1c78c32 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3c50c32)
    #2 0x7fe9d1b1ed77 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3af6d77)
    #3 0x7fe9d1b0e44f (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3ae644f)
    #4 0x7fe9d1b0df99 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3ae5f99)
    #5 0x7fe9cf017454 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xfef454)
    #6 0x7fe9cf016fab (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xfeefab)
    #7 0x7fe9cf0166ba (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xfee6ba)
    #8 0x7fe9cefb8389 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xf90389)
    #9 0x7fe9cefb5c08 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xf8dc08)
    #10 0x7fe9cc499188 (/usr/lib/libgtk-x11-2.0.so.0.2000.1+0x142188)
previously allocated by thread T0 here:
    #0 0x7fe9d724e222 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x9226222)
    #1 0x7fe9d1c78835 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3c50835)
    #2 0x7fe9d1c0fe2a (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x3be7e2a)
    #3 0x7fe9cf01762b (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xfef62b)
    #4 0x7fe9cf016eb5 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xfeeeb5)
    #5 0x7fe9cf0166ba (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xfee6ba)
    #6 0x7fe9cefb8389 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xf90389)
    #7 0x7fe9cefb5c08 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xf8dc08)
    #8 0x7fe9cc499188 (/usr/lib/libgtk-x11-2.0.so.0.2000.1+0x142188)
Thread T19 created by T0 here:
    #0 0x7fe9d72433b5 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x921b3b5)
    #1 0x7fe9d049782c (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x246f82c)
    #2 0x7fe9d049770d (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x246f70d)
    #3 0x7fe9d04a25d4 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x247a5d4)
    #4 0x7fe9d556a8db (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x75428db)
    #5 0x7fe9d558059d (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x755859d)
    #6 0x7fe9d5669903 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x7641903)
    #7 0x7fe9d5669c3d (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x7641c3d)
    #8 0x7fe9d57ea60b (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x77c260b)
    #9 0x7fe9d5656e74 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x762ee74)
    #10 0x7fe9d5656d07 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x762ed07)
    #11 0x7fe9d5631c95 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x7609c95)
    #12 0x7fe9d5632bae (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x760abae)
    #13 0x7fe9cef95698 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xf6d698)
    #14 0x7fe9cf0cd69c (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x10a569c)
    #15 0x7fe9cf0c9cc5 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x10a1cc5)
    #16 0x7fe9cf0c947a (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x10a147a)
    #17 0x7fe9cf0c7ea6 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x109fea6)
    #18 0x7fe9cf0c4776 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x109c776)
    #19 0x7fe9cf0bcf1e (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x1094f1e)
    #20 0x7fe9cf0c02c6 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x10982c6)
    #21 0x7fe9cfd5dd67 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x1d35d67)
    #22 0x7fe9cfd5a6c2 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x1d326c2)
    #23 0x7fe9d542ad97 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x7402d97)
    #24 0x7fe9d542d8e6 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x74058e6)
    #25 0x7fe9d5427feb (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x73fffeb)
    #26 0x7fe9d02d82ae (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x22b02ae)
    #27 0x7fe9d02d9940 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x22b1940)
    #28 0x7fe9d02d66b5 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0x22ae6b5)
    #29 0x7fe9cedbfd37 (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xd97d37)
    #30 0x7fe9cedbfc9b (/usr/local/google/home/epoger/old-chrome-binaries/asan/asan-linux-release-143037/chrome+0xd97c9b)
    #31 0x7fe9c7f5dc4d (/lib/libc-2.11.1.so+0x1ec4d)
==28322== ABORTING
Stats: 178M malloced (193M for red zones) by 463539 calls
Stats: 4M realloced by 18305 calls
Stats: 163M freed by 384238 calls
Stats: 30M really freed by 134645 calls
Stats: 364M (93237 full pages) mmaped in 91 calls
  mmaps   by size class: 8:327660; 9:40955; 10:28665; 11:12282; 12:4096; 13:2048; 14:768; 15:768; 16:1152; 17:224; 18:32; 19:24; 20:4; 21:2; 22:4; 
  mallocs by size class: 8:377530; 9:37512; 10:28341; 11:11175; 12:3867; 13:2101; 14:815; 15:690; 16:1234; 17:210; 18:33; 19:21; 20:4; 21:2; 22:4; 
  frees   by size class: 8:305394; 9:33745; 10:27201; 11:9980; 12:3271; 13:1854; 14:712; 15:645; 16:1190; 17:189; 18:27; 19:21; 20:3; 21:2; 22:4; 
  rfrees  by size class: 8:118206; 9:5251; 10:7788; 11:1398; 12:871; 13:402; 14:478; 15:68; 16:157; 17:19; 18:3; 19:4; 
Stats: malloc large: 274 small slow: 2510
Shadow byte and word:
  0x1ffd35a57c00: fa
  0x1ffd35a57c00: fa fa fa fa fa fa fa fa
More shadow bytes:
  0x1ffd35a57be0: fa fa fa fa fa fa fa fa
  0x1ffd35a57be8: fa fa fa fa fa fa fa fa
  0x1ffd35a57bf0: fd fd fd fd fd fd fd fd
  0x1ffd35a57bf8: fd fd fd fd fd fd fd fd
=>0x1ffd35a57c00: fa fa fa fa fa fa fa fa
  0x1ffd35a57c08: fa fa fa fa fa fa fa fa
  0x1ffd35a57c10: fd fd fd fd fd fd fd fd
  0x1ffd35a57c18: fd fd fd fd fd fd fd fd
  0x1ffd35a57c20: fa fa fa fa fa fa fa fa



### ep...@google.com (2012-07-02)

I am currently checking out a new asan-debug Chrome tree; once it's checked out, I will build it and see if I can reproduce this bug locally.  Then maybe I can track it down in the debugger...

### in...@chromium.org (2012-07-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-16)

Elliot, friendly ping.

### ep...@google.com (2012-07-23)

I can reproduce this error when opening the above crbug133571-cf-minimized.html in my locally built release binary, on my Linux desktop via NX:

Chromium	22.0.1209.0 (Developer Build 146872)
OS	Linux
WebKit	537.1 (trunk/Source/WebCore/Configurations@122718)
JavaScript	V8 3.12.11
Flash	11.2 r202
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1209.0 Safari/537.1
Command Line	 out/Release/chrome --flag-switches-begin --flag-switches-end file:///home/epoger/bugs
Executable Path	/usr/local/google/home/epoger/src/chrome/asan-release/src/out/Release/chrome
Profile Path	/home/epoger/.config/chromium/Default

Full asan log is attached; here's the top:
=================================================================
==8412== ERROR: AddressSanitizer heap-use-after-free on address 0x7f1a617ba004 at pc 0x7f1a761707c2 bp 0x7fff3300ce70 sp 0x7fff3300ce68
READ of size 4 at 0x7f1a617ba004 thread T0
    #0 0x7f1a761707c2 in SkARGB32_Black_Blitter::blitAntiH(int, int, unsigned char const*, short const*) third_party/skia/src/core/SkBlitter_ARGB32.cpp:254
    #1 0x7f1a760d9cd3 in call_hline_blitter(SkBlitter*, int, int, int, unsigned int) third_party/skia/src/core/SkScan_Antihair.cpp:83
    #2 0x7f1a760da398 in hline(int, int, int, int, SkBlitter*, int) third_party/skia/src/core/SkScan_Antihair.cpp:110
    #3 0x7f1a760d7841 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:418
    #4 0x7f1a760d6fd2 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:263
    #5 0x7f1a760d6fd2 in do_anti_hairline(int, int, int, int, SkIRect const*, SkBlitter*) third_party/skia/src/core/SkScan_Antihair.cpp:263


### ep...@google.com (2012-07-23)

When I view the same crbug133571-cf-minimized.html in my locally built debug binary in gdb, on my Linux desktop via NX, I get an assert failure:

Chromium	22.0.1209.0 (Developer Build 146887)
OS	Linux
WebKit	537.1 (trunk/Source/WebCore/Configurations@121656)
JavaScript	V8 3.12.11
Flash	11.2 r202
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1209.0 Safari/537.1
Command Line	 out/Debug/chrome --flag-switches-begin --flag-switches-end
Executable Path	/usr/local/google/home/epoger/src/chrome/asan-debug/src/out/Debug/chrome
Profile Path	/home/epoger/.config/chromium/Default

[9629:9657:277808282901:FATAL:SkBitmap.h(729)] ./third_party/skia/include/core/SkBitmap.h:729: failed assertion "(unsigned)x < fWidth && (unsigned)y < fHeight"

Backtrace:
	base::debug::StackTrace::StackTrace() [0x7fffc9773a04]
	logging::LogMessage::~LogMessage() [0x7fffc98df7ed]
	SkDebugf_FileLine() [0x7fffd0c69be4]
	SkBitmap::getAddr32() [0x7fffc912075b]
	SkARGB32_Black_Blitter::blitAntiH() [0x7fffd0e78118]
	call_hline_blitter() [0x7fffd0a086e9]
	hline() [0x7fffd0a0c4e9]
	do_anti_hairline() [0x7fffd09f81ca]
	SkScan::AntiHairLineRgn() [0x7fffd09f2468]
	hair_path() [0x7fffd0a19c91]
	SkScan::AntiHairPath() [0x7fffd0a1a648]
	SkDraw::drawPath() [0x7fffd078ebfc]
	SkDevice::drawPath() [0x7fffd077856d]
	SkCanvas::drawPath() [0x7fffd072915b]
	WebCore::GraphicsContext::strokePath() [0x7fffd51297b2]
	WebCore::CanvasRenderingContext2D::stroke() [0x7fffd468372d]
	WebCore::CanvasRenderingContext2DV8Internal::strokeCallback() [0x7fffdadcd178]
	v8::internal::HandleApiCallHelper<>() [0x7fffccc7f0df]
	v8::internal::Builtin_Impl_HandleApiCall() [0x7fffccc7de36]
	v8::internal::Builtin_HandleApiCall() [0x7fffccc54650]
	0x33792e90618e

I tried to view x, y, fWidth, and fHeight in the debugger, but the debugger says they have all been optimized out.

Mike/Brian, any thoughts?

### [Deleted User] (2012-07-26)

Understood. I have a pending cl on skia that fixes this (I believe) by reliably detecting non-finite values in a path (in this tests cases, there are infinities) and just rejects trying to draw it.

### [Deleted User] (2012-07-26)

fixed in skia rev. 4785 (built upon rev. 4784)

### cl...@chromium.org (2012-07-28)

ClusterFuzz has detected this issue as fixed in range 148729:148774.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=64492209

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fd5e0efe004
Crash State:
  - crash stack -
  SkARGB32_Black_Blitter::blitAntiH
  hline
  - free stack -
  v8::internal::Assembler::~Assembler
  v8::internal::RegExpImpl::CompileIrregexp
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129392:129412
Fixed: https://cluster-fuzz.appspot.com/revisions?range=148729:148774

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95hchTI8R_qhSTCdsOd6XibVzkfur7y0N2sOcIh7LrJim0mwDO9bpG-F-jTm6z2a1ozJYoQ2NyqL_l-hh8hSJ5_2qQZHmk8Br53L_eCaLhdcGUXi0mBnUn5uSkVIasUHlf6vfUFa1pbzYSI2ky1Zy4Z27t49Ulq-iRNZqefeG4cEGoDSSE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2012-07-28)

ClusterFuzz has detected this issue as fixed in range 148729:148774.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=64492209

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fd5e0efe004
Crash State:
  - crash stack -
  SkARGB32_Black_Blitter::blitAntiH
  hline
  - free stack -
  v8::internal::Assembler::~Assembler
  v8::internal::RegExpImpl::CompileIrregexp
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129392:129412
Fixed: https://cluster-fuzz.appspot.com/revisions?range=148729:148774

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95hchTI8R_qhSTCdsOd6XibVzkfur7y0N2sOcIh7LrJim0mwDO9bpG-F-jTm6z2a1ozJYoQ2NyqL_l-hh8hSJ5_2qQZHmk8Br53L_eCaLhdcGUXi0mBnUn5uSkVIasUHlf6vfUFa1pbzYSI2ky1Zy4Z27t49Ulq-iRNZqefeG4cEGoDSSE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-07-28)

Since the last skia roll was reverted, we can't close it yet. http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=148875&r2=148874&pathrev=148875

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-06)

verified on ClusterFuzz that skia rolled forward and Mike's skia rev. 4785 fixed this.

### cl...@chromium.org (2012-08-06)

ClusterFuzz has detected this issue as fixed in range 148967:149009.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=64492209

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fd5e0efe004
Crash State:
  - crash stack -
  SkARGB32_Black_Blitter::blitAntiH
  hline
  - free stack -
  v8::internal::Assembler::~Assembler
  v8::internal::RegExpImpl::CompileIrregexp
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129392:129412
Fixed: https://cluster-fuzz.appspot.com/revisions?range=148967:149009

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95hchTI8R_qhSTCdsOd6XibVzkfur7y0N2sOcIh7LrJim0mwDO9bpG-F-jTm6z2a1ozJYoQ2NyqL_l-hh8hSJ5_2qQZHmk8Br53L_eCaLhdcGUXi0mBnUn5uSkVIasUHlf6vfUFa1pbzYSI2ky1Zy4Z27t49Ulq-iRNZqefeG4cEGoDSSE

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

Thank you @attekett for all these Skia bugs.
OOB read => $500

### sc...@gmail.com (2012-08-21)

Upping reward to $1000. This is part of a cluster of duplicates -- all from @attekett -- one of which does show an OOB write fault. See https://code.google.com/p/chromium/issues/detail?id=138293

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-13)

Does not need merge since already in m22.

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/133571?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/138238]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059942)*
