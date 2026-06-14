# Bad cast with svg:g element

| Field | Value |
|-------|-------|
| **Issue ID** | [40083124](https://issues.chromium.org/issues/40083124) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-09-10 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: [6.0.472.55] + stable  

Operating System: win 7 and xp

**REPRODUCTION CASE**  

Just open the xhtml file.

Type of crash: [tab]  

Crash State:  

1.  

eax=02baccc0 ebx=00d41200 ecx=00d413a8 edx=00d414bc esi=00d413a8 edi=00d413a8  

eip=56537265 esp=0012f5d4 ebp=0012f5fc iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00000246  

56537265 ?? ???

ChildEBP RetAddr  

WARNING: Frame IP not in any known module. Following frames may be wrong.  

0012f5d0 02236ef5 0x56537265  

0012f5fc 022370d0 chrome\_1c30000!Hunspell\_create\_key+0x4a09c8  

0012f624 02238180 chrome\_1c30000!Hunspell\_create\_key+0x4a0ba3  

0012f7f0 0215b9bc chrome\_1c30000!Hunspell\_create\_key+0x4a1c53

## 2. eax=0012eddc ebx=00d43a48 ecx=0121abd8 edx=80000010 esi=0012eddc edi=121abd80 eip=02161bd1 esp=0012ed90 ebp=0012ee3c iopl=0 nv up ei pl nz na po nc cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00000202

chrome\_1c30000!Hunspell\_create\_key+0x3cb6a4:  

02161bd1 a5 movs dword ptr es:[edi],dword ptr [esi] es:0023:121abd80=???????? ds:0023:0012eddc=a0d07798  

ChildEBP RetAddr  

WARNING: Stack unwind information not available. Following frames may be wrong.  

0012ee3c 0215baad chrome\_1c30000!Hunspell\_create\_key+0x3cb6a4  

0012eec4 020d32d9 chrome\_1c30000!Hunspell\_create\_key+0x3c5580  

0012ef00 0215b7ba chrome\_1c30000!Hunspell\_create\_key+0x33cdac

## Attachments

- [j.rar](attachments/j.rar) (application/x-rar; charset=binary, 3.4 KB)
- [load.html](attachments/load.html) (text/html; charset=us-ascii, 941 B)
- [ss.dmp](attachments/ss.dmp) (application/octet-stream; charset=binary, 32.4 KB)

## Timeline

### sc...@gmail.com (2010-09-10)

Thanks wooshi, we'll use this bug to track the svg:g case:

<svg:g xmlns:svg="http://www.w3.org/2000/svg" > </svg:g>

(For simple repros like this, please put them inline instead of in a RAR file :)


### sc...@gmail.com (2010-09-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-09-10)

Upstream bug https://bugs.webkit.org/show_bug.cgi?id=45562

Patch posted for review.


### js...@chromium.org (2010-09-10)

Upstream patch landed at: http://trac.webkit.org/changeset/67236


### js...@chromium.org (2010-09-11)

@wooshi - we were unable to reproduce any form of corruption or other exploitable condition on the file in /1/2.xhtml


### sc...@gmail.com (2010-09-11)

@wooshi: sure you put the correct file in the rar for /1/2.xhtml ? :)

### wo...@gmail.com (2010-09-11)

Sure, maybe you will wait some time (on my x60s laptop(chrome 6.0.472.55, windows 7), it's about 20 secs,and sometimes the chrome told me need kill the pages ), I test it on my xp and win7, all works. I think it's not hard to repro. now I attached another bug for fun (it's free,:)), this is a funny one when you check the source code,I think like a integer problem,but I have no time to analyze it, you need wait the page load complete and refresh once,:) .



### sc...@gmail.com (2010-09-11)

@wooshi: thanks for the additional bug.
Could you file an individual bug for each individual issue? It makes it easier for us to pay you, and the base reward is now typically doubled to $1000 for good, careful reports ;-)

Regarding "load.html": I can't be sure about this, because I can't catch the crash in a debug build (the script is killed due to excessive memory consumption). But it seems very harmless and is likely an out-of-memory condition. Catching the tab crash in an optimized build, I see:
0x08f502b2:	movl   $0x0,0xbbadbeef
That indicates that the CRASH() macro was called. This macro safely takes down a tab be writing to 0xbbadbeef and then NULL (just in case 0xbbadbeef was mapped).

If you are seeing a different, more serious-looking condition with load.html then please file a new bug with registers included :)


Regarding /1/2.xhtml, I did let it run for well over 20 seconds. When I came back from lunch, it had finished running with no crash. This was on Linux, though. We will re-try with Windows and Mac. Again, if we can get this to reproduce, we will want to track it with a separate bug.

### js...@chromium.org (2010-09-11)

We tested on Windows Vista, 7, and XP, and couldn't get a repro. The worst case was the forced termination on memory exhaustion.

### wo...@gmail.com (2010-09-12)

I upload 1/2.xhtml to you , the stack like this:

chrome_5a910000!WebCore::RenderBlock::layoutColumns+0x350:
5ae41bd1 a5              movs    dword ptr es:[edi],dword ptr [esi] es:0023:1c49c830=???????? ds:0023:001ef254=18c08f3b
1:019> .dump ss.dmp
Creating ss.dmp - mini user dump
Dump successfully written
1:019> kv
ChildEBP RetAddr  Args to Child              
001ef2b4 5ae3ba22 016053e0 ffffffff 00000008 chrome_5a910000!WebCore::RenderBlock::layoutColumns+0x350 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 4271]
001ef33c 5ae3b7d4 00000001 016053e0 5ae3cd6f chrome_5a910000!WebCore::RenderBlock::layoutBlock+0x230 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1206]
001ef3f0 5ad73db7 01605110 00000000 00dde600 chrome_5a910000!WebCore::RenderBlock::layout+0x17 (FPO: [0,0,1]) (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp @ 1120]
001ef410 5ad70e10 00dde600 00000000 00000000 chrome_5a910000!WebCore::RenderView::layout+0xed (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderview.cpp @ 127]
001ef448 5adba3a8 01629800 01605110 00ebb800 chrome_5a910000!WebCore::ScrollView::visibleContentRect+0x64 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\platform\scrollview.cpp @ 211]
001ef494 5ad8395f 00000001 00e4e000 00e4e028 chrome_5a910000!WebCore::FrameView::layout+0x500 (CONV: thiscall) [d:\b\slave\chrome-official\build\src\third_party\webkit\webcore\page\frameview.cpp @ 761]
001ef4b8 5ad571a9 001ef4dc 5ad570bb 00e4e000 chrome_5a910000!WebCore::Document::implicitClose+0x2ab (CONV: thiscall) [d:\b\slave\chr



### sc...@gmail.com (2010-09-15)

An opportunity arose to patch the svg:g bad cast bug into v6.

Merge to 472: http://src.chromium.org/viewvc/chrome?view=rev&revision=59538

Leaving WillMerge as I think this still needs to be merged to 517.

### sc...@gmail.com (2010-09-16)

@wushi: congrats! The <svg:g> test case provisionally qualifies for a $500 Chromium Security Reward.
For high quality reports, you can easily get $1000 for bugs like this. To get rewarded at the $1000 level, please:
- File one distinct Chromium bug per distinct crash.
- For very simple repro cases, such as <svg:g xmlns:svg="http://www.w3.org/2000/svg" > </svg:g> -- please just paste the HTML inline in the bug report.

Please file a separate bug for 1/2.xhtml if you can still reproduce it. (If you do file a separate bug, please include your screen resolution and default Chromium window size in pixels -- one of your repros only crashes when the Chromium window is a certain size!)

### in...@chromium.org (2010-09-17)

Merged to 517.

### sc...@gmail.com (2010-09-22)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/55114?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083124)*
