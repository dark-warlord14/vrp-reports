# chrome_1c30000!SkAlphaRuns::Break+0x13 - Memory Corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40080944](https://issues.chromium.org/issues/40080944) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | sp...@gmail.com |
| **Assignee** | wj...@chromium.org |
| **Created** | 2010-05-10 |
| **Bounty** | $500.00 |

## Description

Chrome Version :  

Google Chrome 4.1.249.1064  

WebKit 532.5  

V8 1.3.18.22  

URLs (if applicable) : (Attached test file "poc.htm" to reproduce issue).  

Other browsers tested: IE8, FF 3.5 , Safari 4  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 4: OK  

Firefox 3.6.3: OK  

**IE 7:**  

**IE 8:**

**What steps will reproduce the problem?**

1. Open the attached html file with Chrome

**What is the expected result?**

The memory use should stay stable.  

The google child proccess shouldn't crash.

**What happens instead?**

Usage CPU 50%  

Crash of child proccess or process never ends.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

more.dmp - Crash dump  

info.txt - more informations about problem.

## Attachments

- [info.txt](attachments/info.txt) (text/plain, English; charset=us-ascii, 11.6 KB)
- [poc.html](attachments/poc.html) (text/html; charset=us-ascii, 653 B)
- [more.dmp](attachments/more.dmp) (data, 20.5 KB)
- [SkAlphaRuns..Break ReadAV@Arbitrary (ff625aa34f06d0f797bcdc02f0cdffbf).html](attachments/SkAlphaRuns..Break ReadAV@Arbitrary (ff625aa34f06d0f797bcdc02f0cdffbf).html) (exported SGML document text, 893.3 KB)
- [poc2.html](attachments/poc2.html) (text/html; charset=us-ascii, 657 B)

## Timeline

### th...@chromium.org (2010-05-10)

Doesn't crash on Linux, just chews a cpu.

### th...@chromium.org (2010-05-10)

Senorblanco to triage.

### sp...@gmail.com (2010-05-12)

[Comment Deleted]

### sp...@gmail.com (2010-05-12)

On linux i didn't test it.... but as i wrote in "info.txt" there are two situations :
crash or deadlock.
thestig : child process ends ?? 
On my Windows XP SP3 chrome child process never ends or crash and of course chews cpu


### be...@gmail.com (2010-05-19)

Tested with 6.0.411.0 (47700) on Windows Vista - nothing unexpected happens, not even 
excessive CPU usage.

Tested with 4.1.249.1064 unknown (45376) on Windows Vista - excessive CPU usage, but 
nothing else. I'll let it run a couple of times overnight to see if I can find a 
crash.

It might be that Skia is not handling OOM gracefully, given that the PoC creates a 
VERY large canvas. I have 4Gb on my test machine, so I may not see the crash because 
it takes too long to fill up the address space? Just speculating...


### sc...@gmail.com (2010-05-20)

Thanks for the report. Adding security labels.
The info.txt document indicates an out-of-bounds read due to a wild pointer. I'm not 
sure that's memory corruption in and of itself, but it might easily lead to a second-
order out-of-bounds-write effect.

cc:ing Justin who has helped with Skia security in the past.

### sc...@gmail.com (2010-05-20)

poc.html sad-tabs 5.0.375.39 on Linux fairly quickly for me. I don't have debug 
details.

### sk...@chromium.org (2010-05-20)

I ran it overnight in 6.0.411.0 (47700), letting the code run for 30 minutes max: it
crashed once in 20 runs. I've attached the details extracted from the debugger. The crash is in:

http://code.google.com/p/skia/source/browse/trunk/src/core/SkAlphaRuns.cpp#44

void SkAlphaRuns::Break(int16_t runs[], uint8_t alpha[], int x, int count)
{
    SkASSERT(count > 0 && x >= 0);

//  SkAlphaRuns::BreakAt(runs, alpha, x);
//  SkAlphaRuns::BreakAt(&runs[x], &alpha[x], count);

    int16_t* next_runs = runs + x;
    uint8_t*  next_alpha = alpha + x;
    while (x > 0)
    {
        int n = runs[0];   ////// KaB00m!
        SkASSERT(n > 0);

        if (x < n)
        {
            alpha[x] = alpha[0];
            runs[0] = SkToS16(x);
            runs[x] = SkToS16(n - x);
            break;
        }
        runs += n;
        alpha += n;
        x -= n;
    }
Local vars:
  count = 1
  alpha = 0x03201D74
  runs = 0x031C1D40 (address of invalid read)
  next_alpha = 0x03201D74
  x = 31122

This code is being called from:

http://code.google.com/p/skia/source/browse/trunk/src/core/SkAlphaRuns.cpp#100

void SkAlphaRuns::add(int x, U8CPU startAlpha, int middleCount, U8CPU stopAlpha, U8CPU maxValue)
{
    SkASSERT(middleCount >= 0);
    SkASSERT(x >= 0 && x + (startAlpha != 0) + middleCount + (stopAlpha != 0) <= fWidth);

    int16_t*    runs = fRuns;
    uint8_t*     alpha = fAlpha;

    if (startAlpha)
    {
        SkAlphaRuns::Break(runs, alpha, x, 1); ///// call here
Local vars:
  middleCount = 53
  startAlpha = 0x1f
  maxValue = 0x40
  x = 50
  stopAlpha = 0x1f
Unfortunately the "this" pointer wasn't recoverable at the time of the crash, so I cannot tell you the values of 
member attributes such as runs/fRuns.

It appears that the "x" value has mysteriously gone UP rather than down: it started as 50, the code does "x-=n" 
and it ends up being 31122... I think that may be a clue as to why this code crashes; n was negative and is not 
supposed to be negative. The SkASSERT should catch this if it is enabled, but I expect it is not.

I'v adjusted the priority/severity as I am worried that this may be exploitable if you know how to trigger it 
correctly.

Hope this helps.

### sk...@chromium.org (2010-05-20)

Actually I can confirm that n < 0 from looking at the disassembly and the registers:
chrome_6abf0000!SkAlphaRuns::Break+0x13 [c:\b\slave\chrome-
official\build\src\third_party\skia\src\core\skalpharuns.cpp @ 44]:
  6ac465c5 0fbf31          movsx   esi,word ptr [ecx]

this is "int n = runs[0];", so esi == n. Looking at the registers:

eax=00007992 ebx=00000032 ecx=031c1d40 edx=031d1064 esi=ffff86a0 edi=031fa3e2
eip=6ac465c5 esp=0040e0f0 ebp=0040e0f8 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202

esi=ffff86a0 == -7960

### js...@chromium.org (2010-05-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-05-25)

senorblanco@, now that you're back have you had a chance to look at this? :)

### se...@chromium.org (2010-05-25)

Not yet.  Will take a look tomorrow.

### js...@chromium.org (2010-05-27)

Just a heads up. I left this going for a day with a trunk build on my z600 and never 
got a crash.

### se...@chromium.org (2010-06-02)

I haven't been able to repro this yet, but I'm still looking into it.  I don't see 
any crashes or spinning CPU under trunk (r47687).

This canvas is not particularly big (10000 x 150 x RGBA = ~6M), so it shouldn't 
automatically cause an out-of-memory condition.  That said, here are some things 
about canvas:

- it's one of the few places in the renderer where malloc() returning 0 will not 
cause the renderer to kill itself  (this was implemented since otherwise it's just 
too easy to crash the renderer:  create a 16Kx15K canvas on a moderately-loaded 32bit 
machine)

- this is done in skia/ext/SkMemory_new_handler, when Skia calls sk_malloc_flags() 
without SK_MALLOC_THROW -- this is how Skia indicates it expects that 
sk_malloc_flags() can fail, and will be handled gracefully by Skia.

As I said, though, I don't think this is an OOM condition since the canvas is fairly 
small.

I thought that perhaps retrieving the context before resizing the canvas might be 
causing a problem, but it doesn't seem to be.  The context is not reallocated when 
the canvas is re-sized, only the image buffer is reallocated.

I'll see if I can get a 4.1 build to repro, or failing that, stare at the Skia code 
to see if anything obvious pops out at me.

It would also be extremely helpful if this can be repro'ed under Purify or valgrind.

### se...@chromium.org (2010-06-02)

Sorry, that should be 100000 x 150 * RGBA = 60M.

### se...@chromium.org (2010-06-03)

OK, I've attached a variant that will cause an assert to fire consistently in debug.

Basically, this is overflowing the fixed-point conversions in SkFDot6ToFixed:

    SkASSERT((x << 10 >> 10) == x);

This may or may not be related to the original bug.  If I look at the original crash, 
it seems as if an int is being stored in an int16_t (SkAlphaRuns.cpp:24), which could 
easily give a negative value if the width is big enough (>=32K).  I'm just guessing 
though; I never actually managed to get it to crash that way.

If this diagnosis is correct, there are a couple of possible solutions:

1)  Limit canvases to 32767x32767 in size.  This should work, since all coordinates 
are cropped against the canvas limits, so the resulting coords should fit in 16.16 
fixed point in all cases.  This will prevent users from being able to create 
100,000x150 canvases, though (the current case).  Note that there is already a 
limitation of 256Mpixels, computed as 32Kx8K pixels.

2)  Turn ENSURE_VALUE_SAFETY_FOR_SKIA back on in WebKit.  This is a big hammer that 
will break some layout tests and previously-fixed bugs.

3)  Put some lower level coordinate-range checks for anything using the super 
sampling blitters, or converting to fixed-point.  This would probably fix these 
particular crashes, but might leave others lurking.

I'm leaning towards #1.

### js...@chromium.org (2010-06-03)

As I remember ENSURE_VALUE_SAFETY_FOR_SKIA used to cap canvas width at 32767, so I'm 
entirely in favor of #1. 

We also discussed #3 several months ago, but the switch to floating point math solved 
the problem cases we'd been seeing. However, I think it's worth considering again if we 
continue to see problems.


### se...@chromium.org (2010-06-15)

Well, ENSURE_VALUE_SAFETY_FOR_SKIA is slightly different, in that it attempts to cap the coordinates passed to Skia (and does so incorrectly in some cases), rather than capping the canvas size.

I think it'd be great to have a belt-and-suspenders approach, and do both #1 and #3.  #3 would make Skia more robust, and #1 would prevent any similar problems from WebKit.

### da...@chromium.org (2010-06-15)

[Empty comment from Monorail migration]

### se...@chromium.org (2010-06-18)

[Empty comment from Monorail migration]

### wj...@chromium.org (2010-06-21)

Have started looking at this.

BTW, I don't seem to be able to view the bug URL (
http://code.google.com/p/chromium/issues/detail?id=43813) in Chrome on my
gLaptop (I get "Forbidden\nYour client does not have permission to get URL
/p/chromium/issues/detail?id=43813 from this server.") but I can view it in
FireFox. I can view other Chromium issues (e.g.
http://code.google.com/p/chromium/issues/detail?id=46591) in Chrome no
problem ... is this normal?

### js...@chromium.org (2010-06-21)

wjmaclean@ - The bug is view restricted, so you have to be logged in as your @chromium.org account. You were probably logged in from your @google.com account.

Also, since I forgot to mention it earlier, I'd definitely prefer options #1 and #3, like Stephen suggested.


### wj...@chromium.org (2010-06-22)

Thanks ... got it working. It would be nice if the server, instead of saying
"Forbidden", could just say something like "You need to be logged in to view
this page ...", and maybe even take me to a login screen :-)

### js...@chromium.org (2010-06-24)

I didn't realize we lost the owner here. This has been punted for over a month, so we really should try to get it fixed for the next stable refresh. 

wjmaclean@ - are you working on this or should it be on someone else's plate?


### wj...@chromium.org (2010-06-24)

I am looking into this. I'm starting from the premise we need to decide on which approach above (or combination thereof) to best address the problem, and studying the code to figure out implementations detail.

### sp...@gmail.com (2010-06-24)

[Comment Deleted]

### sp...@gmail.com (2010-06-24)

i hope this will be fixed in the next stable refresh.

### js...@chromium.org (2010-06-24)

Thanks wjmaclean@. I was just cleaning out the security list and noticed that this one was still pending.


### sp...@gmail.com (2010-07-03)

when the fix will be ready ? in 10 july it will 2 month after the report .

### js...@chromium.org (2010-07-03)

This is by far the oldest high-severity external report in the security queue. If we don't have a fix in time for the next security refresh (maybe 2-3 weeks) I think the only option is to re-enable ENSURE_VALUE_SAFETY_FOR_SKIA on stable branch. And we'll have to consider the same thing on v6 if it's not resolved by code freeze.


### wj...@chromium.org (2010-07-07)

I've been working on some other bugs, but will switch back to this one full-time  given its time-critical nature.

I am confident that solution (1) can be done fairly quickly, but I do have a question:

It would be nice to localize this change to Skia. This can be done by clipping canvas size in, say, platform_canvas_linux.cc or maybe SkBitmap. But this leaves WebKit un-informed about the change in size, and notifying WebKit would require changing the WebKit API. Ugh.

This causes a problem, since when WebCore::HTMLCanvasElement::paint() is called, it passes the original canvas size in, but the associated bitmap size is wrong, so it gets 'stretched' to match ...

A hacky solution would be to detect when the requested destination rect matched the original canvas size, and modify it (possibly in paintSkBitmap() or even SkCanvas::drawBitmapRect()) to draw to the right size. Of course, if anyone ever really wanted it to stretch ...?

Is there a preferred way to do this? I assume we want to avoid making changes in WebKit while implementing (1), if possible.

BTW, is Skia under git control? It doesn't seem to be in my local repository ...

### se...@chromium.org (2010-07-07)

I'd actually prefer to do the change in WebKit, since it already has constraints on the total size of the canvas (256Kpixels).  You can put the changes behind an #if PLATFORM(CHROMIUM), or (perhaps better), #if USE(SKIA), since that will confine it to Win/Linux, and reflects the fact that the constraint is imposed by Skia.

Skia is under svn control, but the "src" and "include" subdirectories are pulled separately from the skia repo (skia.googlecode.com)  This is done to avoid bringing in a lot of unused stuff.  You can see this in chromium's DEPS file:

  "src/third_party/skia/src":
    "http://skia.googlecode.com/svn/trunk/src@" + Var("skia_revision"),
  "src/third_party/skia/include":
    "http://skia.googlecode.com/svn/trunk/include@" + Var("skia_revision"),

### wj...@chromium.org (2010-07-07)

OK, so presumably I'll do this in HTMLCanvasElement so that it filters down
to the required Skia ImageBuffer calls?

### wj...@chromium.org (2010-07-09)

Regarding solution (1), a WebKit security bug (41962) has been created and a patch submitted. It is a small patch, so I hope to land it in a fairly short timeframe.

Is fixing (1) suffucuent to resolve security issues related to this issue?

I am starting to look at what is required to implement solution (3).

### js...@chromium.org (2010-07-09)

The fix in https://bugs.webkit.org/show_bug.cgi?id=41962 looks sufficient to close this bug, but we'll need to test it. If it's good we can open a follow-on bug for implementing option #3 as well.

### in...@chromium.org (2010-07-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-12)

+darin


### js...@chromium.org (2010-07-13)

Landed upstream as: http://trac.webkit.org/changeset/63219

Note to me: The merge will need to be manual and use the first Webkit patch (not the final patch). Canvas was refactored after the original patch was submitted. So, the files in 375 don't exist on Webkit trunk anymore.


### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52383 

------------------------------------------------------------------------
r52383 | jschuh@chromium.org | 2010-07-14 13:35:32 -0700 (Wed, 14 Jul 2010) | 26 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/canvas/canvas-skia-excessive-size-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/canvas/canvas-skia-excessive-size.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/dom/CanvasSurface.cpp?r1=52383&r2=52382
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/dom/CanvasSurface.h?r1=52383&r2=52382

2010-07-09  W. James MacLean <wjmaclean@chromium.org>

        Reviewed by NOBODY (OOPS!)

        https://crbug.com/chromium/41962 Limit html canvas element dimensions to 32767 for Skia platform
        https://bugs.webkit.org/show_bug.cgi?id=41962

        Test: fast/canvas/canvas-skia-excessive-size.html

         * WebCore/dom/CanvasSurface.h
         * WebCore/dom/CanvasSurface.cpp
         (WebCore::CanvasSurface::convertLogicalToDevice):

2010-07-09  W. James MacLean <wjmaclean@chromium.org>

        Reviewed by NOBODY (OOPS!)

        https://crbug.com/chromium/41962 Limit html canvas element dimensions to 32767 for Skia platform
        https://bugs.webkit.org/show_bug.cgi?id=41962

        * fast/canvas/canvas-skia-excessive-size.html: Added.
        * fast/canvas/canvas-skia-excessive-size-expected.txt: Added.

BUG=43813
TBR=jschuh@chromium.org
Review URL: http://codereview.chromium.org/2944020
------------------------------------------------------------------------


### js...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### sp...@gmail.com (2010-07-15)

how can i easy test fix ? 

### ma...@google.com (2010-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2010-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2010-07-21)

Verified on mac 5.0.375.121 (Official Build 52864) beta

### sc...@gmail.com (2010-07-21)

@sp3x: congratulations! You've qualified for a $500 reward under the Chromium Security Reward program. We should have a release out including this fix this week. If you could withhold disclosure until that time, it would be appreciated.

### sc...@gmail.com (2010-07-21)

Oh, and what name (plus optional affiliation) would you like us to use for credit? I can use sp3x@securityreason.com unless I hear otherwise.

### sp...@gmail.com (2010-07-22)

Thank you @scarybeasts, for credit it would be nice : sp3x of SecurityReason.com

### sc...@gmail.com (2010-08-02)

This one was Chrome specific so releasing.
@sp3x: thanks again! You can e-mail me, cevans@chromium.org for details on how to get paid.

### sp...@gmail.com (2010-08-11)

@scarybeasts : I sended two mails to cevans@chromium.org but i didn't got any respond.

### sc...@gmail.com (2010-08-31)

Payment is in the electronic system. Since this is your first reward, keep an eye out for successful arrival. Allow a few weeks.

Thanks again!

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/43813?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080944)*
