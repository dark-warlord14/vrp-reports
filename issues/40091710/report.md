# Security: Automatic file execution without any warnings 

| Field | Value |
|-------|-------|
| **Issue ID** | [40091710](https://issues.chromium.org/issues/40091710) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2018-06-20 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 69.0.3464.2 (Official Build) canary (64-bit)  

Operating System: Windows 7

(repro <https://crbug.com/chromium/666824>.)

**REPRODUCTION CASE**

1. Install the extension.
2. The program (shell.hta) should be opened without any warnings, and it's definitely bad behavior.

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 1.9 MB)
- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 1.8 KB)

## Timeline

### ch...@gmail.com (2018-06-20)

[Empty comment from Monorail migration]

### oc...@chromium.org (2018-06-20)

qinmin, could you please take a look as the person that fixed  https://crbug.com/chromium/666824 ?

.hta seems to be on the dangerous files list: https://cs.chromium.org/chromium/src/chrome/browser/resources/safe_browsing/download_file_types.asciipb?q=download_file_types.asciipb&sq=package:chromium&dr&l=1862

did this regress?

[Monorail components: UI>Browser>Downloads]

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-06-26)

Any update on this bug?

### qi...@chromium.org (2018-06-26)

I am not able to repro the bug on linux, does this has to be on windows?
On linux, i loaded the unpacked extension, then nothing happens

Shakti, can you help test this bug see if it reproduces?

### ch...@gmail.com (2018-06-26)

I can only repro this on Windows.

### sh...@chromium.org (2018-06-26)

Yes, I was able to reproduce this on Windows 10

### ke...@chromium.org (2018-07-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-11)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2018-07-11)

i think this is an issue with fake user gesture. 

In DownloadsOpenFunction, we check whether there is an user gesture before opening the download here: https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/downloads/downloads_api.cc?type=cs&q=downloads_ap&g=0&l=1462

But seems the fake mouse click can bypass that check. 

Since dcheng@ is the author of WebContents::HasRecentInteractiveInputEvent(), assigning it to him to investigate. 
if HasRecentInteractiveInputEvent() can be easily spoofed, then we might need to remove that bypass path and always prompt user.

### dc...@chromium.org (2018-07-12)

What is chrome.debugger? Is this an interface to devtools?

If devtools can trigger arbitrary input from the browser-side via Input.dispatchMouseEvent, then there's really not much I can do. I suppose we can gate the downloads prompt on if the extension has debugger permissions as well, and always prompt in that case?

(I'm not familiar with the downloads API implementation itself, so this should stay with someone on the downloads team)

### pa...@chromium.org (2018-07-12)

Yes, the `chrome.debugger` API is known to be extremely powerful. https://developer.chrome.com/extensions/debugger

+rdevlin.cronin, meacer, who know more about extensions APIs, gestures as security mechanisms, and secure UX and API design concerns generally.

[Monorail components: Platform>Extensions>API]

### dc...@chromium.org (2018-07-12)

There's a bunch of indirection here, but jannhorn pointed me at https://cs.chromium.org/chromium/src/content/browser/renderer_host/render_widget_host_impl.cc?rcl=f340807ff46e1662b09c0cf4f73e788a0cbf946b&l=1219, which is the entrypoint for Input.dispatchMouseEvent.

I'm not sure how hard it would be to add a bit to these input events so we could know not to call the RenderWidgetHostDelegate here: https://cs.chromium.org/chromium/src/content/browser/renderer_host/render_widget_host_impl.cc?rcl=cdcc3926f1af7e14fce9dd7337a0127dde9a10ef&l=2491

But that would be another possible solution.

### dg...@chromium.org (2018-07-12)

This is interesting - so any extension page can open downloaded files if there was a user gesture? I guess we can disallow debugging the pages which have access to chrome.downloads api. Devlin, mind taking a look? Should be similar to restricting file:/// access.

### dt...@chromium.org (2018-07-12)

dcheng@ sounds like you need to augment this function:

https://cs.chromium.org/chromium/src/third_party/blink/public/platform/web_input_event.h?g=0&l=256

1) pass in the input event or a bool to say from_debugger.

2) Check it is via the debugger: event.modifiers & kFromDebugger

See:
https://cs.chromium.org/chromium/src/third_party/blink/public/platform/web_input_event.h?g=0&l=256

### dt...@chromium.org (2018-07-12)

Err; I meant https://cs.chromium.org/chromium/src/content/browser/web_contents/web_contents_impl.cc?g=0&l=5939 as the first link

### dg...@chromium.org (2018-07-12)

Wait, do you want to make injected DevTools input events skip some processing? Please don't, we try hard to make them behave as real events would. That's very important for testing/automation scenarios.

### bu...@chromium.org (2018-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a4a89a53791a508896b388b0d818644834c0d6d

commit 9a4a89a53791a508896b388b0d818644834c0d6d
Author: Min Qin <qinmin@chromium.org>
Date: Thu Jul 12 18:55:57 2018

Always prompt user if opening a download thru extensions with debugger permission

The user gesture can be faked, so we shouldn't trust it

BUG=854455

Change-Id: Ib42911a77d3f519554a5b9a4c1464ec50e79f268
Reviewed-on: https://chromium-review.googlesource.com/1135525
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#574652}
[modify] https://crrev.com/9a4a89a53791a508896b388b0d818644834c0d6d/chrome/browser/extensions/api/downloads/downloads_api.cc


### ch...@gmail.com (2018-07-13)

Fixed?

### qi...@chromium.org (2018-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-16)

[Empty comment from Monorail migration]

### dc...@chromium.org (2018-07-19)

Is it possible for a hostile extension with debugger permissions to trigger a download to open from another extension using this input injection?

### aw...@chromium.org (2018-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-07-23)

Hi Khalil - the VRP panel decided to award $500 for this report, but noted that they may not reward bugs of this type in the future.  Cheers!

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-07-23)

Thanks a lot Andrew! :-)

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-10-19)

This issue was migrated from crbug.com/chromium/854455?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### gi...@gmail.com (2026-01-16)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091710)*
