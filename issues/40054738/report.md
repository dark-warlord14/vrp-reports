# Security: Memory Corruption in MaskSuperBlitter

| Field | Value |
|-------|-------|
| **Issue ID** | [40054738](https://issues.chromium.org/issues/40054738) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | w3...@gmail.com |
| **Assignee** | ep...@google.com |
| **Created** | 2012-03-09 |
| **Bounty** | $1,000.00 |

## Description

Tested on 19.0.1061.1 Win7 64
Tested on 17.0.963.78 Win7 32

<svg>
 <line transform="scale(-20,100)"  y2="4044044px" stroke="rgb(1% ,1% ,1%)" >
 </line>
</svg>

4:061:x86> kb
ChildEBP RetAddr  Args to Child              
0018cfb4 7df1859f 0018d018 0018d068 00000000 ntdll32!ZwRaiseException+0x12
0018d004 7df3735c 0018d018 0018d068 00000000 ntdll32!RtlReportException+0x20
0018d338 7df0069a 00000000 fffffffe fffffffe ntdll32!RtlInvalidHandlerDetected+0x8f
0018d388 7decb3b5 00000000 0000004d 0018ffb0 ntdll32!RtlIsValidHandler+0x80
0018d408 7de80133 0018d420 0018d470 0018d420 ntdll32!RtlDispatchException+0x10e
0018d414 0018d420 0018d470 c0000005 00000000 ntdll32!KiUserExceptionDispatcher+0xf
WARNING: Frame IP not in any known module. Following frames may be wrong.
0018d75c 02b4629f 0018d830 e2166e00 000000ae 0x18d420
0018d77c 02b462eb 0018d830 00000000 e2166e55 chrome_2b40000!_VEC_memzero+0x36
0018d7a0 02fff9a4 0018d824 00000000 e2166e61 chrome_2b40000!_VEC_memzero+0x82
0018d7bc 02bba2d2 0018dc54 00b1ca80 0018e3f0 chrome_2b40000!MaskSuperBlitter::MaskSuperBlitter+0xb2 [c:\b\build\slave\chrome-official\build\src\third_party\skia\src\core\skscan_antipath.cpp @ 434]
0018dcbc 00000000 00000000 00000000 00000000 chrome_2b40000!SkScan::AntiFillPath+0x1a2 [c:\b\build\slave\chrome-official\build\src\third_party\skia\src\core\skscan_antipath.cpp @ 670]


## Attachments

- [117588.html](attachments/117588.html) (text/plain; charset=us-ascii, 99 B)

## Timeline

### sc...@gmail.com (2012-03-10)

Hi Elliot, I don't have time to triage this right now so I thought I'd make sure you were quickly cc:ed
Is it perhaps similar to the other issue you're looking into with Mike?

### sk...@chromium.org (2012-03-10)

Thanks W3bd3vil, nice find!
Upstream: https://code.google.com/p/skia/issues/detail?id=523

Classic set of integer math issues: no checks for negative height or integer overflow in MaskSuperBlitter:

skia\src\core\skscan_antipath.cpp
MaskSuperBlitter::MaskSuperBlitter(SkBlitter* realBlitter, const SkIRect& ir,
                                   const SkRegion& clip)
        : BaseSuperBlitter(realBlitter, ir, clip) {
    SkASSERT(CanHandleRect(ir));

    fMask.fImage    = (uint8_t*)fStorage;
    fMask.fBounds   = ir;
    fMask.fRowBytes = ir.width();
    fMask.fFormat   = SkMask::kA8_Format;

    fClipRect = ir;
    fClipRect.intersect(clip.getBounds());

    // For valgrind, write 1 extra byte at the end so we don't read
    // uninitialized memory. See comment in add_aa_span and fStorage[].
    memset(fStorage, 0, fMask.fBounds.height() * fMask.fRowBytes + 1);
}
The repro creates a SkIRect with bottom < top (0n3261812 < 0n3261956), thus negative height (-144).

skia\include\core\SkRect.h:
    /**
     *  Returns the rectangle's height. This does not check for a valid rect
     *  (i.e. top <= bottom) so the result may be negative.
     */
    int height() const { return fBottom - fTop; }


### sc...@gmail.com (2012-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-03-12)

[Empty comment from Monorail migration]

### ep...@google.com (2012-03-12)

[old summary was: Security: Memory Corruption Skia]
[changed from M17 to M18 ReleaseBlock-Stable]

Should this be listed as an M18 release blocker?  I have taken the liberty of marking it as such; Karen, feel free to undo that if it's wrong.

### to...@chromium.org (2012-03-12)

[Empty comment from Monorail migration]

### to...@chromium.org (2012-03-12)

The 4-line <svg> snippet above reproduces consistently on M18; reed@ has a clean proposed fix that I'm testing.

### to...@chromium.org (2012-03-12)

Skia r3364 fixes this crash on both Win M19 and Linux M18; it should roll into Canary in the next day or to, and meanwhile is small and isolated enough we should consider drovering it back to M18 and M17.

### sc...@gmail.com (2012-03-12)

I think we're done with M17 patches, but M18 is an awesome idea. Any chance you could do that today?


### ep...@google.com (2012-03-12)

taking ownership to merge http://code.google.com/p/skia/source/detail?r=3364  into M18

### ep...@google.com (2012-03-12)

For comparison during future verification steps:

I can confirm that I get a "sad tab" (Aw, Snap!) when viewing the attached page on these browsers:

19.0.1067.0 (Official Build 126101) canary
18.0.1025.96 (Official Build 126091)

(running on my desktop Mac with OS 10.6.8)



### in...@chromium.org (2012-03-12)

Thanks Elliot. Just a fyi, merge deadline is 7 pm tonight.

### ep...@google.com (2012-03-12)

Merge to skia's chrome/1025 landed as http://code.google.com/p/skia/source/detail?r=3365

Once we have seen the sample page fare better in the next M18 build, we can mark this as Fixed/Verified...

### ep...@google.com (2012-03-13)

Warning: http://code.google.com/p/skia/source/detail?r=3364 , which I merged into M18 to fix this bug, MAY cause other problems.

Mike sent a Skia DEPS roll (3350->3370) to the trybots as https://chromiumcodereview.appspot.com/9691010/ , and there are hundreds of layout_test failures in Linux and 16 layout_test failures on Mac.  (Windows layout_tests did not run, probably because of typical Windows buildbot problems.)

Mike's previous Skia DEPS roll attempt (3350->3363), https://chromiumcodereview.appspot.com/9662062/ , did not have these layout_test failures, so the tests seem to have been broken in the range 3364-3370.

I have just kicked off trybots for another Skia DEPS roll to 3365 at https://chromiumcodereview.appspot.com/9689043/ .  Tomorrow morning we can compare its results to the other ones and see what's breaking the layout tests…


### ka...@google.com (2012-03-13)

elliott, please make sure to revert from branch if it turns out this change is indeed causing issues. 

### ep...@google.com (2012-03-13)

Good news all around...

1. I have confirmed that the sample page is now rendered OK in 18.0.1025.97 (Official Build 126303), downloaded from http://chrome-master2.mtv.corp.google.com/official_builds/ , so this bug is indeed fixed in M18.

2. The Skia DEPS roll to 3365 did fine in the trybots (see https://chromiumcodereview.appspot.com/9689043/ ), so we do not have any evidence that the merge of 3364 will introduce layout_test failures.


I have two questions for Karen:

1. So, do we leave this with the status FixUnreleased, or move it to Verified, or what?

2. Can you please point me at accurate documentation of the battery of tests that these official branch builds are run through?  I would hope that they are being run through layout_tests, for example, to make sure that the particular combination of merged patches hasn't broken anything.  It seems bad if we are relying too much on tip-of-tree tests to validate builds on other branches...




### in...@chromium.org (2012-03-13)

1. Yes please leave it in fixunreleased.

2. Use go/betabuilders

### sc...@gmail.com (2012-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-13)

Great work!

@w3bd3vil: with what name should we credit you in our release notes?

### w3...@gmail.com (2012-03-13)

"Omair" I have a single name. Thanks scarybeasts!


### sc...@gmail.com (2012-03-14)

Thank you Omair.
And welcome to the Chromium Security Reward Program!
For reports like this (memory corruption, good test case) we reward at the $1000 level.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### w3...@gmail.com (2012-03-14)

Cool! Thanks!

And how do I collect the reward?

### sc...@gmail.com (2012-03-14)

We'll e-mail you to get you enrolled in our supply system.

### sc...@gmail.com (2012-03-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-26)

[Empty comment from Monorail migration]

### w3...@gmail.com (2012-03-28)

scarybeasts, Does it usually take this long to get enrolled?

### sc...@gmail.com (2012-03-28)

We reach out once the fix is live in stable channel.
I hear a rumour that might be today, keep an eye out ;-)

### w3...@gmail.com (2012-05-03)

It's been a while. And I have no one contacting me yet for the reward.

### [Deleted User] (2012-05-03)

w3bd3vil, thanks for the ping. Looks like this was fixed when m18 went to stable but this bug never got marked as fixed. THat probably made it fall through the filters scarybeasts uses to do payouts. Sorry about that.

Scarybeasts, are you aware of a reason this is still open or did this fall through the cracks somehow?

### sc...@gmail.com (2012-05-03)

Sorry for the delay @w3bd3vil. I haven't done a sweep of pending payments in a while. I was actually planning to do one Friday.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-06-01)

Payment is in system now... it can take up to a few weeks for the wire to arrive.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/117588?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/118352, crbug.com/chromium/120013]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054738)*
