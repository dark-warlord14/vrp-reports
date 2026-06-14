# Security: Screen capture via WebGL texture

| Field | Value |
|-------|-------|
| **Issue ID** | [40077507](https://issues.chromium.org/issues/40077507) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Reporter** | da...@gmail.com |
| **Assignee** | gm...@chromium.org |
| **Created** | 2013-05-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A vulnerability to capture other webpage screen information was found in WebGL while trying to upload the texture data via WebGL's texImage2D. If the target is invalid, an image of a previous rendering made by Google Chrome is transfered to the texture. It is known that all the elements styled with absolute position, can be captured. But it is known that it also occurs with other CSS statements, although the other cases were not reproduced.

**VERSION**  

Chrome Version: Versión 26.0.1410.64 m  

Operating System: Windows 7 Home Premium - Service Pack 1

**REPRODUCTION CASE**  

The reproduction case is attached with two pages.

1. The capturer page
2. The captured page

To reproduce, just open both pages, navigate in the Captured Page and switch back to the Capturer Page. The Capturer Page will show the captured image on a WebGL Canvas.

POSSIBLE CAUSE  

If the elements are being rendered as a texture, it would possibly be fixed with an texture unbinding.

## Attachments

- [Chrome Screen Capture Vulnerability.rar](attachments/Chrome Screen Capture Vulnerability.rar) (application/x-rar; charset=binary, 2.1 KB)

## Timeline

### ae...@chromium.org (2013-05-03)

Thanks for the report. Reproduces on Windows 7 26.0.1410.64.

### ae...@chromium.org (2013-05-03)

[Empty comment from Monorail migration]

### ae...@chromium.org (2013-05-03)

Also seems to use the previous texture if you remove texImage2D call completely.

@kbr: could you take a look at this?


### kb...@chromium.org (2013-05-03)

CC'ing more people. Could one of the CC'd people please take a look some time today?


### da...@gmail.com (2013-05-03)

So looks like texImage2D is unecessary. Maybe the call is ignored.

### ba...@chromium.org (2013-05-03)

I can reproduce this in both the latest Canary and Stable on Windows, but only when using ANGLE. If I pass --use-gl=desktop to the Stable build the problem does not appear.

As a side note it seems that the most recent Canary builds (at least the Aura ones) don't allow you to turn off ANGLE.

### zm...@chromium.org (2013-05-03)

I can't reproduce on my Windows 7 bot in both stable (26.0.1410.64) and Canary (28.0.1497.1)

I am on a ATI GPU though (ATI Radeon HD 4800) while most of you are on NVIDIA

### kb...@chromium.org (2013-05-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-07)

Hey Dan, Brandon, or John, I'm trying to triage any ownerless security bugs (see Mark's email on Code 28). Can one of you own this one? 

### kb...@chromium.org (2013-05-07)

Talked with @gman; this is definitely a regression. Happens only with NVIDIA cards on Windows, and only with ANGLE.

The texImage2D call in the capturing page is meaningless. It has bogus arguments and will simply generate an OpenGL error. For some reason, rendering with an incomplete texture (which should cause a black texture to be bound by the command buffer) is causing another random texture, from the compositor, to be referenced.

Gregg said he'd look into it. Assigning.


### in...@chromium.org (2013-05-08)

From preconditions mentioned in c#0 and c#10, lowering severity.

### da...@gmail.com (2013-05-08)

Please, note that this is not an unusual user behavior. Even if it is, it can be easily induced by the capturer page.

This vulnerability was tested on some big banks and most of their pages suits perfectly for this vulnerability.

Also note that Windows + NVidia computers are very common (at least here in Brazil), which increases the possible number of victims.

I will be waiting the fix. And congratulations for the great professionalism.

### js...@chromium.org (2013-05-08)

Is it possible for the capturing page to read back the data in the canvas or is it just that the stale data is getting rendered to the screen?

### da...@gmail.com (2013-05-08)

Yes, you can use glReadPixels to read back the data and send it to any place.

### jb...@chromium.org (2013-05-09)

I just tried to do a bisect and got http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=/trunk/src&range=160416%3A160445 , which includes an ANGLE roll http://src.chromium.org/viewvc/chrome?revision=160437&view=revision . Not certain that the bisect is correct, as I'm not sure the repro is 100% reliable.

### kb...@chromium.org (2013-05-09)

There are multiple changes to ANGLE's texture handling code in that range:

https://code.google.com/p/angleproject/source/list?num=25&start=1298

It would be helpful if TransGaming folks could help assess whether any of them are particularly likely to have caused this regression.


### [Deleted User] (2013-05-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-10)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### sh...@chromium.org (2013-05-11)

r1278 looks like the likeliest candidate, as it directly influences ANGLE's handling of incomplete textures with invalid parameters at creation time. 

I don't think Nicolas can see this page even though he's been CC'ed-- I've filled him in and asked him to help investigate.

### sh...@chromium.org (2013-05-13)

ANGLE's 1278 revision does indeed look like it caused the issue. The ANGLE team has a fix in progress.

### in...@chromium.org (2013-05-14)

Do we have a link to the angle bug, so that we can track progress. We need the fix soon for security code 28.

### sh...@chromium.org (2013-05-14)

TransGaming's been handling it on their internal issue system, but I filed a public bug so that it'll be visible when it lands externally.

http://code.google.com/p/angleproject/issues/detail?id=424

### sh...@chromium.org (2013-05-14)

A fix has been committed at r2209 in the ANGLE tree.

### in...@chromium.org (2013-05-14)

Thanks. just a fyi, we would need to roll these angle fixes on trunk, m28, m27. Current list

https://code.google.com/p/angleproject/source/detail?r=2207
https://code.google.com/p/angleproject/source/detail?r=2209

### jb...@chromium.org (2013-05-14)

Should the command buffer also be able to detect the incomplete texture and bind a black texture itself? I think it already does that for some other cases.

### kb...@chromium.org (2013-05-14)

It's already doing that. Was the problem that the black texture the command buffer uses was incomplete?


### gm...@chromium.org (2013-05-15)

That black texture should be impossible to be incomplete as it's a 1x1
pixel texture.

I'd like to understand the bug more. Is there an explanation? Is this the
issue that Ken found that 0 width textures are not replaced by the command
buffer?

### kb...@chromium.org (2013-05-15)

Yes, I'm 99% sure that the black texture is fine. The problem was that the unallocated texture coming from WebGL wasn't flagged by the command buffer as needing to be replaced with the black texture.


### kb...@chromium.org (2013-05-15)

Filed https://crbug.com/chromium/240961 for catching this case in the command buffer.


### gm...@chromium.org (2013-05-15)

Technically isn't the problem ANGLE not drawing in black for textures that
are not texture complete? Yes, the command buffer should not rely on that
the but GL spec is clear what's supposed to happen.

### sh...@chromium.org (2013-05-15)

Yes, ANGLE should have been returning black for any sample from an incomplete texture. That issue has now been addressed in the ANGLE tree, as noted upthread.

### [Deleted User] (2013-05-28)

Gregg, Shannon, if we wanted to fix this in 27, would we need both the ANGLE and Chrome fix or would either of them suffice? 

### sh...@chromium.org (2013-05-28)

I believe either should suffice-- I know at least that the ANGLE fix doesn't require the Chrome fix to address the issue; someone Chrome-side can say more certainly than I can whether the reverse is true.

### kb...@chromium.org (2013-05-28)

I think the ANGLE fix but not the Chromium fix should be merged back to M27. The Chromium fix is more for defense-in-depth, and has the potential to negatively impact performance.


### [Deleted User] (2013-05-28)

What's our confidence factor on the ANGLE fix? With the trunk now containing the extra checks in Chromium, does the ANGLE code alone get properly exercised in Canary/Dev ? 

### gm...@chromium.org (2013-05-28)

That ANGLE fix is more appropriate. 

The Chrome fix added some perf issues which need to be addressed before we push that upstream.

### [Deleted User] (2013-05-28)

ANGLE fix merged to chrome_m27 branch at rev 2250 . 


### [Deleted User] (2013-05-29)

On second thought, I'm not comfortable checking that change in and unleashing it straight to stable. The revision right before it also deals with 0x0 textures so it's shaking my confidence about what exactly we were testing for the brief period that the ANGLE fix was in (before the chromium fix landed). 

I'll err on the side of caution and revert the ANGLE merge. This is not a regression new to M27. 


### [Deleted User] (2013-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2013-05-29)

The plan of record for the ANGLE fix is to roll it out in M28 Beta and assuming it all goes smoothly we'll include in the next M27 stable update (assuming there will be another one).


### sc...@gmail.com (2013-06-07)

@vangelis: has the ANGLE fix been merged to M28?

### [Deleted User] (2013-06-08)

Yep, it did yesterday as a result of this change: https://chromereviews.googleplex.com/8440014/


### sc...@gmail.com (2013-06-08)

@vangelis: great, thanks for the update!

### pa...@chromium.org (2013-06-27)

$500 for this one. Thanks!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### da...@gmail.com (2013-06-27)

Thanks! :)

### sc...@gmail.com (2013-07-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/237611?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077507)*
