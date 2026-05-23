# Security: Malicious WebGL page can capture and upload contents of other tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [40086275](https://issues.chromium.org/issues/40086275) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android |
| **Reporter** | pa...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2016-12-19 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using WebGL, a malicious web page can capture the contents of other tabs  

as images and upload them to a server. Reproducible on a Samsung Galaxy S6.  

Probably MEDIUM severity.

**VERSION**  

Chrome Version: [55.0.2883.91] + [stable]  

Operating System: [Android 6.0.1; SM-G920F Build/MMB29K]  

Samsung Galaxy S6 UK model.

**REPRODUCTION CASE**  

Note that since the issue might only be reproducible on the Samsung Galaxy S6,  

you may prefer to just read `README.md` in the zip, which includes the reproduction instructions.  

I attach `index.html`, a self-contained HTML file demonstrating the issue.  

I also attach a zip archive with more details, the HTML file,  

and a self-contained Python 3 script that will serve the HTML file  

and will save the uploaded PNG image files captured by the HTML file.  

It also includes some sample images to show what can be captured;  

these are also described in the README.md.  

See README.md for instructions and more details.

## Attachments

- [index.html](attachments/index.html) (text/plain, 9.9 KB)
- [webgl-bug.zip](attachments/webgl-bug.zip) (application/octet-stream, 3.5 MB)
- [webgl-bug2.zip](attachments/webgl-bug2.zip) (application/octet-stream, 3.5 MB)

## Timeline

### mb...@chromium.org (2016-12-19)

I unfortunately don't have access to a Galaxy S6 to test this, but this looks like an interesting bug.

Ken, any ideas here? I'm wondering if there's any additional validation we could do.

[Monorail components: Internals>GPU>WebGL]

### kb...@chromium.org (2016-12-19)

I tested this on a Google Pixel and can't reproduce the capture of corrupted VRAM.

I'd like to understand better whether the browser thinks the WebGL context's been lost at the time toDataURL is called. If it is, we should return a blank image rather than attempting to actually perform the readback.

The problem appears to be related to the injection of this long-running no-op loop in the fragment shader:

  for(
      int GLF_live3i = 0;
      GLF_live3i < 12244;
      GLF_live3i ++
  )
  {
  }

The first time I tried this test case on my MacBook Pro it caused a GPU hang and reset, but it wasn't reproducible afterward. I didn't have the server running (would be better if it was written in Python 2.x for macOS compatibility) but did see a flash of what looked like garbage VRAM.

Reducing to low security severity and P2 because evidence is that this affects only specific devices. We'd need one to diagnose this in more detail. Prudhvi, do we have an S6 in house that we can use for testing?


[Monorail components: Blink>WebGL]

### pb...@chromium.org (2016-12-19)

[Empty comment from Monorail migration]

### pa...@gmail.com (2016-12-20)

I am fairly certain the WebGL context is not lost on the Samsung Galaxy S6. There is no popup and no refreshing occurred. 

The included fragment shader indeed probably only works for ARM Mali GPUs as in the Samsung Galaxy S6. I think some Sony Xperia phones may also have Mali GPUs, if that helps. 

A different fragment shader might be able to cause a similar issue on other GPUs. Sometimes adding a "discard" or early "return" statement (possibly conditional on a uniform) is enough to cause garbage. But in this case we indeed believe it is the long running loop. 

Changing the loop bound can also have an effect. E.g. a lower loop bound might not hang certain GPUs. Note that the loop bound could be provided in a uniform parameter, so a straightforward loop bound static analysis is unlikely to be enough to detect this. 

I attach an updated zip where `server.py` works with Python 2 and 3. 


### kb...@chromium.org (2016-12-20)

Thanks. No garbage observed with your server on macOS 10.11.6 with Chrome 57.0.2956.0 (Official Build) canary (64-bit).

Ligi, Prudhvi, do we have a Samsung Galaxy S6 on which I could run a test? Ligi, assigning to you so this doesn't get dropped.


### am...@chromium.org (2016-12-20)

[Empty comment from Monorail migration]

### kb...@chromium.org (2016-12-20)

Got the S6 (thanks Prudhvi), and confirm that garbage is observed when running the test case.

Upgrading this back to Security_Severity-Medium and P1. I think the information leak is significant.

Filed internal bug b/33757419 about this, in the bug category for the Mali GPU. I'll also contact a couple of colleagues at ARM and Samsung who may be able to help triage this.

My best guess is that the Mali GPU is aborting a long-running command buffer without signaling that the context is lost via the GL_KHR_robustness extension, although Chrome is allocating its contexts with that reset strategy turned on (visible in about:gpu). Chrome needs that reset notification in order to lose the WebGL context and prevent information leakage such as this. There is already code in place for this purpose.

I'm not sure what we can do about this yet. Marking ExternalDependency to indicate that we don't have any solutions yet from the Chrome side, and need feedback from ARM.


### sh...@chromium.org (2016-12-20)

[Empty comment from Monorail migration]

### pa...@gmail.com (2017-01-25)

Could I check the status of this?

1. Has the issue been reported to ARM? To whom? Has there been a response?
2. Has the issue been reported to Samsung? To whom? Has there been a response?
3. Can we get cc'ed in these conversations? And/or is there an id or reference number (from ARM/Samsung) we can use if we want to refer to these bug reports?
4. Do ARM and Samsung know that the shader was generated by fuzzing (using GLFuzz)?

Thanks


### am...@chromium.org (2017-01-26)

I've asked those questions on our internal bug.  What I can share now is that Samsung is definitely aware of this; hopefully we can answer the rest of your questions in the near future.

kbr@, can you circle back once we have more details?

### kb...@chromium.org (2017-01-27)

Yes, I'll update this bug when either ARM or Samsung gets back to us.


### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### la...@chromium.org (2017-06-20)

[Empty comment from Monorail migration]

[Monorail components: -Internals>GPU>WebGL]

### pa...@gmail.com (2017-07-18)

Could I check on the status of this? 

### kb...@chromium.org (2017-07-18)

Asked ARM/Samsung for a status update on the internal bug b/33757419 .


### pa...@gmail.com (2017-07-19)

I can no longer reproduce this after updating my Samsung S6 (Europe). 
Android 7.0; SM-G920F Build/NRD90M

The rendered image is transparent and, sometimes, the context is lost (I see "Rats! WebGL hit a snag"). 


### kb...@chromium.org (2017-07-19)

Thanks. That's the expected behavior; KHR_robustness is supposed to lose the context in this situation. I've asked for confirmation on b/33757419 but most likely we'll have to close this as WontFix (no longer reproducible). Also, we never got a bug ID from ARM or Samsung.


### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### pa...@gmail.com (2017-08-03)

Thanks. We have confirmation from Samsung that they saw the bug report and confirmation from ARM that they saw the report and fixed the bug thanks to our report. 

### kb...@chromium.org (2017-08-08)

That's great news.


### kb...@chromium.org (2017-08-08)

Closed the internal bug as Fixed, but closing this one as WontFix since we didn't make any code changes to Chromium in response, and since it's no longer reproducible after a rollout of Samsung's newest driver.


### sh...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### pa...@gmail.com (2017-08-10)

Is it possible to manually check if we are still eligible for a reward? My understanding of the program is that we might still be eligible. But I assume we are automatically marked as ineligible when the status is changed to WontFix. 

"Bugs may be eligible even if they are part of the base operating system and can manifest through Chrome."

"...bugs may be eligible even if they are caused by components of the operating system or standard libraries. We're interested in rewarding any information that enables us to better protect our users. In the event of bugs in an external component, we are happy to take care of responsibly notifying other affected parties."


### kb...@chromium.org (2017-08-10)

Oops. Sorry, didn't mean to break your eligibility for a reward, especially since the capture of content occurred through the browser.

Marking as ExternalDependency again and resetting the reward label.


### pa...@gmail.com (2017-08-10)

Thanks so much. Hopefully it is not necessary for the bug to be marked as Fixed/Verified to trigger the next stage of the reward process. If it is necessary, perhaps this bug can be manually flagged for review, as we believe it is fixed (and the fix is deployed) but this may not be clear. 

### aw...@google.com (2017-08-11)

Thanks!  Going to mark this as Fixed since the security issue is indeed fixed (this is in line with how we track this in similar situations, like security bugs in Flash).  The VRP panel will look at this soon.  Thanks!

### sh...@chromium.org (2017-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-14)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2017-08-14)

Per c#24 there is nothing to merge here, but correct me if I'm wrong...

### pa...@gmail.com (2017-08-18)

That's right! I think the aim is to mark this as fixed, merged, etc. (whatever is appropriate), despite the fact that there are no changes to Chromium, so that the rewards panel will review this. I am not sure if some additional labels are needed. 

### aw...@chromium.org (2017-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-28)

Congratulations! The Chrome VRP panel decided to award $2,000 for this report. A member of our finance team will be in touch to arrange payment.

### aw...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### pa...@gmail.com (2017-11-04)

Thanks! We received the reward! Since the fix was actually released some time ago (I think probably around April 2017), is it possible to make this Chromium issue/report public so we can refer to it?

### sh...@chromium.org (2017-11-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-11-18)

This issue was migrated from crbug.com/chromium/675658?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086275)*
