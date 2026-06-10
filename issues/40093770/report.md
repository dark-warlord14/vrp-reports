# Chromium - Exposed GPU profiler allows to dump all URLs and headers from requested pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40093770](https://issues.chromium.org/issues/40093770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>WebView |
| **Platforms** | Android |
| **Reporter** | st...@gmail.com |
| **Assignee** | aw...@google.com |
| **Created** | 2019-01-16 |
| **Bounty** | $4,000.00 |

## Description

================
This issue was originally reported on 1/11/19 in Public Trackers > Android External Security Reports as b/122676405, so this bug should be flagged as externally reported. Reporter is stoshins@gmail.com. I'm filing this bug per a separate email thread. Original report is copied below in its entirety. 
================

Hi. I told about the bug to Kevin Deus, Dave Weinstein and Sebastian Porst in our internal email, but didn't get a reply yet.

On December 23th I scanned Samsung Browser and found exposed GPU profiler in file org/chromium/content/browser/TracingControllerAndroid.java which appeared to be a real Chromium bug.
I tested it in the latest Chrome on my rooted Samsung Galaxy S8 (Android 7.0)

That profiler saves web data to arbitrary path, on the attached screenshot (2018-12-24_1727.png) I've shown login to Gmail. It leaks all urls and headers.

Later I retested it in PayPal app, seems that all apps which use WebViews are vulnerable to this, and the bug is present in master branch (https://github.com/chromium/chromium/blob/master/content/public/android/java/src/org/chromium/content/browser/TracingControllerAndroidImpl.java).

So to force an app which use a WebView to start dumping all the data, just broadcast an intent with action "app_package.GPU_PROFILER_START"

## Attachments

- [2018-12-24_1727.png](attachments/2018-12-24_1727.png) (image/png, 113.1 KB)

## Timeline

### aw...@google.com (2019-01-16)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-16)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-01-16)

This is definitely a real issue, I confirmed this locally with various apps and Chrome itself. Every embedder of the Chromium content layer on Android has this broadcast receiver - despite the comment in TracingControllerAndroidImpl implying the app has to register it, it's actually registered automatically by BrowserStartupControllerImpl in content unconditionally :(

There is already https://crbug.com/chromium/898816 tracking removing this entirely once our profiling scripts no longer use it - currently I think they still do, so just removing this now will break perf bots(?) and maybe other things?

Probably the smallest change to make to fix the issue for now would be to make BrowserStartupControllerImpl only register the broadcast receiver when running on a debuggable build of the Android platform (BuildInfo.isDebugAndroid()), which would disable it for end user devices while keeping it active on the test devices we use for bots/local development - that'd resolve the major issue here. Maybe also add some validation of the filename for the trace to prevent it being used to write files to unexpected places (though for the bot use case I suspect it's necessary to allow the trace to be written to /sdcard which is visible to other apps, so that wouldn't entirely resolve the security issue by itself).

### to...@chromium.org (2019-01-16)

As presented this is an information disclosure: the trace can contain sensitive information which other apps on the device, or the user themselves via adb, can access, and there doesn't appear to be anything preventing other apps from triggering it either.

I haven't looked into the implications of the code using a caller-supplied filename to write the trace in detail - being able to create a file in an arbitrary place that's writable by the app receiving the broadcast might have further implications, though the attacker can't really control what will be written to the file. (not sure if it can overwrite an existing file?)

### to...@chromium.org (2019-01-16)

This has also been there for ages, it was not recently introduced.

### aw...@google.com (2019-01-16)

[Empty comment from Monorail migration]

### st...@gmail.com (2019-01-16)

Hi, 
> not sure if it can overwrite an existing file?
It can, when I performed my first tests, I was overwriting the same file.

> can't really control what will be written to the file
It can partially be controllable e.g. in case of Chrome when attacker loads custom web page and forces the profiler to dump controllable values from headers.

Will that issue be publicly disclosed when resolved? I'd like to add something that I don't want to become public

### to...@chromium.org (2019-01-16)

The overall file format will still be our trace data, even if there's small parts of attacker-controlled data embedded in it, so it's unlikely to be able to be successfully read as, say, a sqlite database or other internal file format, which reduces the usefulness to an attacker (but not to zero).

Yes, we make security bugs publicly accessible once they have been fixed for ~14 weeks: https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#TOC-Can-you-please-un-hide-old-security-bugs-



### jd...@chromium.org (2019-01-16)

torne@, you seem well situated to take ownership of this, so I've added you as such. If you're not the right person, feel free to re-assign.

I've also marked this as medium-severity, as it could result in exposure of some sensitive user information.

### to...@chromium.org (2019-01-16)

I can implement a quick fix that disables it unless the android build is debuggable as that's trivial. If that ends up breaking something (because some part of our infrastructure expects this to work on a user build, or similar) I'll have to pass it off to someone who knows more about the profiler as I won't be able to fix the tools not to require this (i.e. i can't fix https://crbug.com/chromium/898816) :)

### jd...@chromium.org (2019-01-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f68b18e1ec1cadb432998d3ccc084e0a8c1ae5cd

commit f68b18e1ec1cadb432998d3ccc084e0a8c1ae5cd
Author: Torne (Richard Coles) <torne@google.com>
Date: Thu Jan 17 15:31:41 2019

Only enable tracing broadcasts on debug Android.

Don't register the tracing broadcast receiver unless we're on a debug
build of the OS. Regular usage of tracing should be using the DevTools
API, not the old adb_profile_chrome script that uses this broadcast.

Bug: 898816, 922627
Change-Id: Ibf172dab29da878000ab60f48bed6e1862aa35e8
Reviewed-on: https://chromium-review.googlesource.com/c/1416171
Reviewed-by: Bo <boliu@chromium.org>
Reviewed-by: Eric Seckler <eseckler@chromium.org>
Reviewed-by: Sami Kyöstilä <skyostil@chromium.org>
Commit-Queue: Richard Coles <torne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#623691}
[modify] https://crrev.com/f68b18e1ec1cadb432998d3ccc084e0a8c1ae5cd/content/public/android/java/src/org/chromium/content/browser/BrowserStartupControllerImpl.java


### to...@chromium.org (2019-01-17)

OK - that should prevent this being used on user devices entirely, which resolves the immediate security issue here. I'll leave it for a couple of days so we can check if this causes any problems with build/test/perf infrastructure that might rely on this in a configuration we didn't forsee, and if nothing is broken we can probably merge to 72 safely.

### st...@gmail.com (2019-01-17)

I'm disappointed that it was labeled as a Medium severity bug. It allows to dump data not only from Chrome (and private browsing in Chrome), but also all other apps. Auth tokens could be leaked from tons of places.

### jd...@chromium.org (2019-01-18)

[Empty comment from Monorail migration]

[Monorail components: Mobile>WebView]

### st...@gmail.com (2019-01-22)

Hi, please let me know when I can disclose it, after 14 weeks or earlier?

### to...@chromium.org (2019-01-22)

Nothing obviously broke as a result; requesting merge to 72. Change should only affect a legacy profiling tool.

Do we want to merge this to 71 as well? The tag was added in #16 but 72 is being released soon and this issue has existed for many years already; unless we were already planning a stable respin it's unlikely to be worth it.

### sh...@chromium.org (2019-01-22)

This bug requires manual review: We are only 6 days from stable.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-01-22)

+ awhalley@ (Security TPM) for M72 merge review.

### aw...@google.com (2019-01-22)

torne@ - is there any reason why this might break legitimate usage, or would anybody using it already be using debug build? 

### to...@chromium.org (2019-01-22)

It may break some legitimate usage by people outside chromium/google. Internally we use debug builds of android pretty universally because there's a bunch of benefits for development/testing, but externally only the emulator is a debug build and the only way to get a debug build for a physical device is to build it yourself from AOSP (for the Google devices that are supported in AOSP only).

The longer term goal is to remove this capability *entirely* from all builds, however - we don't want anyone to be relying on this and tools should be using the (supported) devtools protocol, not an undocumented broadcast. I'm only not removing it entirely now because it's not clear whether all our infrastructure has been migrated to a better approach yet.

### aw...@google.com (2019-01-22)

Thanks torne@ - one more question on severity - it was conjectured that that this an export from a NetLog, if so it could include request/response bytes based on the NetLog mode, do you know if this might be the case?

### to...@chromium.org (2019-01-22)

It logs a whole bunch of different trace categories including netlog and blink. This definitely ends up logging URLs and header values. I don't think that it will by default the *bodies* of the requests/responses, but the header values are enough that it's a serious information disclosure (since this includes auth tokens, cookies, etc).

The broadcast receiver also accepts a bunch of parameters to change the tracing behaviour and though I haven't checked in detail it's possible you can make it trace even more things that way.

### aw...@google.com (2019-01-22)

Thanks torne@. I think given that it's worth taking in 72, even at this very late stage. Is there anybody we should give a heads up that this functionality now will require a debug build?

### go...@chromium.org (2019-01-22)

Approving merge to M72 branch 3626 based on comments #18 and #25. Please merge ASAP. Thank you.

### aw...@google.com (2019-01-22)

Marking as fixed. Please file another bug if we want to do more hardening work.

### to...@chromium.org (2019-01-22)

The only known place this gets used is the adb_profile_chrome script in the chromium tree, which I believe is called by some of our perf testing infrastructure and it's possible that people who have checkouts of chromium use it.

I'll see if I can land a followup CL in master to update the script to explicitly fail if it's a user build of android, and/or to just warn that the script is deprecated and people need to use devtools.

### to...@chromium.org (2019-01-22)

I'll do the followup on https://crbug.com/chromium/898816 which is tracking removing the script/this code entirely.

### cr...@appspot.gserviceaccount.com (2019-01-22)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/318a79045ace18d73e1115d086599e036d0496ba

Commit: 318a79045ace18d73e1115d086599e036d0496ba
Author: torne@google.com
Commiter: torne@chromium.org
Date: 2019-01-22 21:33:06 +0000 UTC

Only enable tracing broadcasts on debug Android.

Don't register the tracing broadcast receiver unless we're on a debug
build of the OS. Regular usage of tracing should be using the DevTools
API, not the old adb_profile_chrome script that uses this broadcast.

TBR=torne@google.com

(cherry picked from commit f68b18e1ec1cadb432998d3ccc084e0a8c1ae5cd)

Bug: 898816, 922627
Change-Id: Ibf172dab29da878000ab60f48bed6e1862aa35e8
Reviewed-on: https://chromium-review.googlesource.com/c/1416171
Reviewed-by: Bo <boliu@chromium.org>
Reviewed-by: Eric Seckler <eseckler@chromium.org>
Reviewed-by: Sami Kyöstilä <skyostil@chromium.org>
Commit-Queue: Richard Coles <torne@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#623691}
Reviewed-on: https://chromium-review.googlesource.com/c/1427386
Reviewed-by: Richard Coles <torne@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#764}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### to...@chromium.org (2019-01-22)

giving this to Andrew to respond to reporter's question in #17 - they want to know when they can disclose

### aw...@google.com (2019-01-22)

re question in #17, now this is going out in M72, if you could wait until February 19th that would be great: it'll give a chance for the Stable rollout to reach 100% and folk to update.

### st...@gmail.com (2019-01-23)

Thanks awhalley@,
sure I can wait until February 19th :)

### st...@gmail.com (2019-01-25)

Hi, will a user be required to install latest Android OS updates to patch the bug, or Chromium layer is updated thru Play Market automatically?

### to...@chromium.org (2019-01-25)

On devices that include the Play Store, both Chrome and WebView will be automatically updated via the Play Store per the schedule mentioned in #32.

For AOSP devices that don't include the Play Store the device vendor/ROM image builder is responsible for updating WebView, either via a system update or a WebView update if they have configured their own mechanism for updating WebView (e.g. via their own app store).

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Congrats! The Panel decided to reward $4,000 for this report :) 

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### mn...@chromium.org (2019-03-19)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-03-21)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/922627?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/897023]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093770)*
