# OOB write in SkARGB32_Black_Blitter::blitAntiH -> sk_memset32_SSE2

| Field | Value |
|-------|-------|
| **Issue ID** | [40056576](https://issues.chromium.org/issues/40056576) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ep...@google.com |
| **Created** | 2012-04-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports an unknown address crash when the attached page is opened.

**VERSION**  

Chrome Version: 19.0.1084.15 beta, 20.0.1097.0 dev  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**

1. get memset.svg and memset.html
2. $ chrome-san memset.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==18437== ERROR: AddressSanitizer crashed on unknown address 0x7fb8ba36d084 (pc 0x7fb7dae981a0 sp 0x7fff25c7ee70 bp 0x7fff25c7ee70 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x7fb7dae981a0 in sk\_memset32\_SSE2(unsigned int\*, unsigned int, int) ???:0  

#1 0x7fb7dae58b4c in SkARGB32\_Black\_Blitter::blitAntiH(int, int, unsigned char const\*, short const\*) ???:0  

#2 0x7fb7dad9feb6 in hline(int, int, int, int, SkBlitter\*, int) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#3 0x7fb7dad9c244 in do\_anti\_hairline(int, int, int, int, SkIRect const\*, SkBlitter\*) third\_party/skia/src/core/SkScan\_Antihair.cpp:0  

#4 0x7fb7dad9b9a4 in SkScan::AntiHairLineRgn(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*) ???:0  

#5 0x7fb7dada1fcd in hair\_path(SkPath const&, SkRasterClip const&, SkBlitter\*, void (\*)(SkPoint const&, SkPoint const&, SkRegion const\*, SkBlitter\*)) third\_party/skia/src/core/SkScan\_Hairline.cpp:0  

#6 0x7fb7dad2c63f in SkDraw::drawPath(SkPath const&, SkPaint const&, SkMatrix const\*, bool) const ???:0  

#7 0x7fb7dad2ca5c in SkDraw::drawRect(SkRect const&, SkPaint const&) const ???:0  

#8 0x7fb7dad1b69b in SkCanvas::drawRect(SkRect const&, SkPaint const&) ???:0  

#9 0x7fb7dbc17b99 in WebCore::GraphicsContext::strokeRect(WebCore::FloatRect const&, float) ???:0  

[...]

## Attachments

- [memset.html](attachments/memset.html) (text/plain; charset=us-ascii, 23 B)
- [memset.svg](attachments/memset.svg) (text/plain; charset=us-ascii, 149 B)
- [memset-asan.txt](attachments/memset-asan.txt) (text/x-c; charset=us-ascii, 10.2 KB)

## Timeline

### ke...@google.com (2012-04-12)

Skia is trying to draw a rectangle with some huge y-values. It hits a bunch of asserts in debug where it checks for overflows, and ends up getting a bad pointer back from fDevice.getAddr32(x, y) which is then written to. It's an OOB write; this could amount to an arbitrary write, but it's hard to tell.

I'm calling this a Skia bug but it might end up being SVG. In the SVG part of the stack the values look sane.

I'll attach the CF report after analysis completes...

As an aside, it's unsatisfying if cluster-fuzz sees an OOB write and calls that "Security: No", as appears to be happening here. If that's correct then are we missing fuzzing hits?

### ke...@chromium.org (2012-04-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=35917061

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f875a224084
Crash State:
  - crash stack -
  sk_memset32_SSE2
  SkARGB32_Black_Blitter::blitAntiH
  hline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129170:129376

Minimized Testcase (0.35 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95at7S5oiygjd_XWXjIU6h14GoBtW6xq9PouK7naK9U3fcUE9r1KLCjDXIXtVBRi1dMwjBhr8rYntQ0F3jPvi0G2V4cBxlFOEbxV_A2S40AS1JQp0-bcxI49W3Hhyi_6te_39XS9VHCa0Iy98hXl7cvFS1hRw

### ke...@chromium.org (2012-04-12)

Regression range implies this is a Skia bug also.

The initial report claims this affects beta but the CF report disagrees.

### ao...@gmail.com (2012-04-12)

The initial reporter persists that this indeed affects beta, which is why he filed this now instead of waiting for spare time to have a look at the cause :)

To verify, sudo apt-get update && sudo apt-get install google-chrome-beta && google-chrome memset.html & sleep 2; dmesg | grep chrome | tail -n 1 -> [  227.610572] chrome[3015]: segfault at 7f3a7a9a7004 ip 00007f397abba5e7 sp 00007fff81ea0808 error 6 in chrome[7f397975e000+429d000]

### in...@chromium.org (2012-04-12)

It does affect beta. Right now, there is a little problem in building up beta branch on CF, which i am fixing it now. Man, people keep adding build dependencies from time to time :)

### in...@chromium.org (2012-04-13)

Elliot, does this looks like a dup of something you fixed recently ?

### [Deleted User] (2012-04-13)

[Empty comment from Monorail migration]

### ep...@google.com (2012-04-13)

I can repro the segfault on Chrome	19.0.1084.15 (not ASAN) on my remote Linux instance...

[2616333.492420] chrome[21784]: segfault at 7f4f0f553004 ip 00007f4e0f5015e7 sp 00007fffd2328008 error 6 in chrome[7f4e0e0a5000+429d000]

Google Chrome	19.0.1084.15 (Official Build 130829) beta
OS	Linux
WebKit	536.5 (@113215)
JavaScript	V8 3.9.24.7
Flash	11.2 r202
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.15 Safari/536.5
Command Line	 /usr/bin/google-chrome --flag-switches-begin --flag-switches-end
Executable Path	/opt/google/chrome/google-chrome
Profile Path	/home/epoger/.config/google-chrome/Default

### ep...@google.com (2012-04-13)

I downloaded chrome-linux-132258 from http://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?path=Linux_x64/ , and I get the segfault there too... so we should be able to reproduce it on any tip-of-tree Linux build.

[2617162.347246] chrome[25670]: segfault at 7f6174815004 ip 00007f6073eb87d7 sp 00007fffba035398 error 6 in chrome[7f607280f000+47a2000]

Chromium	20.0.1102.0 (Developer Build 132258)
OS	Linux
WebKit	536.8 (@114131)
JavaScript	V8 3.10.2.1
Flash	11.2 r202
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.8 (KHTML, like Gecko) Chrome/20.0.1102.0 Safari/536.8
Command Line	 ./chrome --flag-switches-begin --flag-switches-end
Executable Path	/home/epoger/chrome-old-binaries/chrome-linux-x64/chrome-linux-132258/chrome
Profile Path	/home/epoger/.config/chromium/Default

### ep...@google.com (2012-04-13)

[original summary was: "UNKNOWN in sk_memset32_SSE2"]


### ep...@google.com (2012-04-13)

Assigning over to Mike- he has been able to reproduce this in gdb with a local Linux build, and will follow up.

### js...@chromium.org (2012-04-14)

All high and critical severity security regressions are release blockers.

### cl...@chromium.org (2012-04-15)

ClusterFuzz has detected this issue as fixed in range 132349:132350.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=35917061

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f875a224084
Crash State:
  - crash stack -
  sk_memset32_SSE2
  SkARGB32_Black_Blitter::blitAntiH
  hline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129170:129376
Fixed: https://cluster-fuzz.appspot.com/revisions?range=132349:132350

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95at7S5oiygjd_XWXjIU6h14GoBtW6xq9PouK7naK9U3fcUE9r1KLCjDXIXtVBRi1dMwjBhr8rYntQ0F3jPvi0G2V4cBxlFOEbxV_A2S40AS1JQp0-bcxI49W3Hhyi_6te_39XS9VHCa0Iy98hXl7cvFS1hRw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### js...@chromium.org (2012-04-15)

I don't see anything in the commit range that would imply a fix. Seems it might be spurious.

### ao...@gmail.com (2012-04-15)

Sad tab in 132363, but CF likely confused because ASan says just:
==12499== Warning: client program overrides the handler for signal 11.
==12505== Warning: client program overrides the handler for signal 11.
==12505== Warning: client program overrides the handler for signal 11.

### in...@chromium.org (2012-04-15)

Yeah ASAN's SEGV handler got disabled in the recent clang roll. We got it fixed now and removed the bad builds. Please ignore c#13.

### [Deleted User] (2012-04-17)

fixed in skia rev. 3713


### in...@chromium.org (2012-04-17)

[Empty comment from Monorail migration]

### ep...@google.com (2012-04-17)

taking ownership to do the M19 merge, once we confirm fixed in next canary build...

### sc...@gmail.com (2012-04-17)

[Empty comment from Monorail migration]

### ep...@google.com (2012-04-19)

http://code.google.com/p/skia/source/detail?r=3713 rolled into Chrome as https://src.chromium.org/viewvc/chrome?view=rev&revision=132983 , a few hours ago.

I'm going to let that bake in Chrome/WebKit until Monday; if all looks well at that point, I will do the M19 merge.


### cl...@chromium.org (2012-04-19)

ClusterFuzz has detected this issue as fixed in range 132979:132999.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=35917061

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7f875a224084
Crash State:
  - crash stack -
  sk_memset32_SSE2
  SkARGB32_Black_Blitter::blitAntiH
  hline
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129170:129376
Fixed: https://cluster-fuzz.appspot.com/revisions?range=132979:132999

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95at7S5oiygjd_XWXjIU6h14GoBtW6xq9PouK7naK9U3fcUE9r1KLCjDXIXtVBRi1dMwjBhr8rYntQ0F3jPvi0G2V4cBxlFOEbxV_A2S40AS1JQp0-bcxI49W3Hhyi_6te_39XS9VHCa0Iy98hXl7cvFS1hRw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ep...@google.com (2012-04-20)

Yup, I downloaded chrome-linux-132983 from http://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?path=Linux_x64/ , and I don't see the segfault anymore.

Still, waiting until Monday to do the M19 merge...

### ep...@google.com (2012-04-23)

merged http://code.google.com/p/skia/source/detail?r=3713 into Skia's chrome/1084 branch as http://code.google.com/p/skia/source/detail?r=3756

### ep...@google.com (2012-04-23)

Keeping assigned to myself to verify fix in M19...

I will check http://chromegw.corp.google.com/viewvc/chrome/releases/ for the next M19 build after 19.0.1084.33 , and confirm that the bug went from broken to fixed as of that new build.

### ep...@google.com (2012-04-25)

I have just downloaded the following binaries from http://chrome-master2.mtv.corp.google.com/official_builds/ and viewed the repro case (memset.html) on my remote Linux instance:

19.0.1094.33 : Aw, snap!
19.0.1094.35 : blank page, no "Aw, snap!"

18.0.1025.166 : page with a single dot

So it appears that:
- this bug has been fixed in M19 as of 19.0.1094.35
- this bug does not affect M18

At what point do we mark the bug "Fixed"?

### sc...@gmail.com (2012-04-25)

Thanks for the verification! Since this never impacted stable, we can mark it Fixed once the fix ships in the next Beta release.

Generally, there's no harm in leaving something in FixUnreleased indefinitely. We go back and clean them out (also stripping Restrict-View in the process) every once in a while.

### sc...@gmail.com (2012-05-04)

Nice regression catch Aki.
$1000

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

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

This issue was migrated from crbug.com/chromium/123029?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056576)*
