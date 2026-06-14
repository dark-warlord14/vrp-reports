# Security: Possible to retrieve cross-origin data in certain cases using devtools custom formatters

| Field | Value |
|-------|-------|
| **Issue ID** | [40096102](https://issues.chromium.org/issues/40096102) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | bm...@chromium.org |
| **Created** | 2019-08-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When using the "with" statement on a cross-origin object (at least in the case where the associated cross-origin frame is within the same renderer), the devtools debugger will display the properties of the object, even if the frame being debugged doesn't have access to them.

These properties will be passed to any custom formatters that are set up in the page being debugged, allowing it to gain access to them. It's possible to cause the debugger to break by using the "debugger" statement, so the properties can be obtained provided custom formatters are enabled and the user opens the devtools.

It's also possible to obtain some of the cross-origin properties (specifically, arrays) even if custom formatters aren't enabled, though it requires the user to manually expand the properties.

**VERSION**  

Chrome Version: Tested on 76.0.3809.132 (stable) and 78.0.3893.0 (canary)  

Operating System: Windows 10 Pro, version 1903

**REPRODUCTION CASE**

1. In the devtools settings, enable custom formatters.
2. Download file1.html and file2.html and place them in a directory.
3. Open file1.html in the browser and then open the devtools. This page includes a cross-origin iframe (file2.html) and sets up the following timer:

setInterval(() => {  

with (iframe.contentWindow) {  

debugger;  

}  

}, 5000);

This should mean that the debugger breaks a short time after you open the devtools. When it does, the contents of the cross-origin window will be shown in the debugger's scope pane and the window properties will be passed through a custom formatter file1.html has set up.

This custom formatter specifically looks for a function defined by file2.html and when it finds it, it prints the following message to the console:

Found customFunction:  

ƒ customFunction () {

}

4. As mentioned above, it's also possible for the cross-origin data to be passed to the frame being debugged, even without custom formatters. To demonstrate this, expand the "array" property in the scope pane when the debugger is paused.

The array will be passed to the Object.getOwnPropertyNames function defined in the main frame, which will simply print any object it receives. This should result in the following message being shown in the devtools console:

Object.getOwnPropertyNames called with:  

(500) [empty × 500]

This occurs because the array is passed through buildObjectFragment:

<https://cs.chromium.org/chromium/src/third_party/blink/renderer/devtools/front_end/object_ui/ObjectPropertiesSection.js?l=1286&rcl=336ec68042b7d0242b5f7968c4a13b9d6d15f19f>

One final point is that showing the window properties in the scope pane results in inconsistencies in what's displayed. Properties that have a getter won't be displayed, because a security exception will be thrown when attempting to retrieve them, but properties without a getter will be displayed.

If you make a call like:

with (iframe.contentWindow.location) {  

debugger;  

}

then none of the properties set on the location object itself will be shown (apart from href and replace), but all of the properties set on the cross-origin prototype will be shown.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [file1.html](attachments/file1.html) (text/plain, 1.1 KB)
- [file2.html](attachments/file2.html) (text/plain, 224 B)

## Timeline

### ct...@chromium.org (2019-08-27)

Related but slightly different from https://crbug.com/chromium/993706, so adding the same folks from that bug here. Not sure if these will have the same root-cause/fix though. If they do, feel free to dupe.



[Monorail components: Platform>DevTools]

### bm...@chromium.org (2019-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-28)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2019-08-28)

It seems to me that custom formatters are a bad idea, and should at least not be supplied by the context in the debugging context. We could think about extending DevTools itself with custom formatters, but the current way custom formatters are implemented just cause problems.

### ct...@chromium.org (2019-08-28)

bmeurer@ Can you help find someone who can own this bug? We require owners for all Security issues, and the internal bug doesn't appear to be an external dependency.

### bm...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools>JavaScript]

### bm...@chromium.org (2019-08-29)

I've looked into this today, and I'm able to reproduce the problem. But it seems that the root cause is the use of the monkey-patched Object.getOwnPropertyNames(), which is unrelated to the custom formatters.

Also I'm not sure about the Security aspect here, since this is only possible to exploit if DevTools is open _and_ the setting for "Enable custom formatters" is turned on, which is not the case by default.

### ha...@chromium.org (2019-08-30)

I would also guess that the security impact here is low in this case.

### bm...@chromium.org (2019-08-30)

Ok, security issue fix in-flight: https://chromium-review.googlesource.com/c/v8/v8/+/1776093

The fact that we use monkey-patchable Object functions is due to the way that DevTools uses the callFunctionOn API in the CDP, which is quite surprising and probably not a good idea at all, but at least not a security problem. We'll get to that later hopefully.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7dad47c69303ce7b100c36a45deb3f68e1bc59b8

commit 7dad47c69303ce7b100c36a45deb3f68e1bc59b8
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Fri Aug 30 10:50:40 2019

[inspector] Generate custom previews in the objects creation context.

Generating custom previews can invoke user specified JavaScript (via the
`window.devtoolsFormatters` custom formatters feature). These custom
formatters were previously invoked in the main page context, even for
objects coming from other `<iframe>`s. Instead of using the main
renderer context, we should instead generate the custom preview in the
creation context of the object.

Bug: chromium:997925
Change-Id: Ia07915cff6680153b6727e68117ed565e60bc1c2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1776093
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63476}

[modify] https://crrev.com/7dad47c69303ce7b100c36a45deb3f68e1bc59b8/src/inspector/custom-preview.cc
[modify] https://crrev.com/7dad47c69303ce7b100c36a45deb3f68e1bc59b8/src/inspector/custom-preview.h
[modify] https://crrev.com/7dad47c69303ce7b100c36a45deb3f68e1bc59b8/src/inspector/injected-script.cc


### bm...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-04)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-04)

bmeurer@ - please respond to C#15 to consider the M77 merge request

### ya...@chromium.org (2019-09-05)

To answer #14: this fix is in V8.

1: Yes
2: CL to merge: https://chromium-review.googlesource.com/c/v8/v8/+/1776093
3: Yes
4: This is a security issue
5: No

### la...@google.com (2019-09-05)

merge approved for M77 branch 3865

### la...@google.com (2019-09-06)

I am going to have this move to M78 as we are one day from cutting M77 Stable RC and this is not an RBS.

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/997925?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>DevTools>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096102)*
