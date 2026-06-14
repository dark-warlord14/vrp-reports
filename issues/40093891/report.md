# Framebusting protection bypass because a download redirected cross-origin gets processed as a main frame navigation

| Field | Value |
|-------|-------|
| **Issue ID** | [40093891](https://issues.chromium.org/issues/40093891) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2019-01-29 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.0 Safari/537.36 Edg/73.0.74.0

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/frame_busted.php?url=https://www.google.com

What is the expected behavior?
Top frame doesn't navigate to cross-origin page without user gesture. See: https://www.chromestatus.com/feature/5851021045661696

What went wrong?
When download is triggered to same-origin page which redirects to cross-origin page, cross-origin download protection kicks in (i.e. https://www.chromestatus.com/features/4969697975992320). Cross-origin download will be blocked, and download request will be reverted to navigation request. But this navigation is triggered on top frame instead of navigating iframe, which results in bypassing framebusting protection.

Did this work before? N/A 

Chrome version: 71  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [frame_busted.php](attachments/frame_busted.php) (text/plain, 112 B)
- [download_redirector.php](attachments/download_redirector.php) (text/plain, 197 B)
- [framebusting.mp4](attachments/framebusting.mp4) (video/mp4, 5.8 MB)
- [spoof.mp4](attachments/spoof.mp4) (video/mp4, 13.4 MB)

## Timeline

### me...@chromium.org (2019-01-29)

Reproduced on stable on Linux, adding other OSes that I suspect this affects.
Labeling this Low-Severity since it is a gesture requirement bypass.
japhet@ could you please take a look?

[Monorail components: Blink>SecurityFeature]

### ja...@chromium.org (2019-01-29)

It looks like this is a side effect of https://crbug.com/chromium/831073. If a download redirects cross-origin, we convert it to a navigation. However, we appear to target that navigation at the top frame unconditionally, instead of the frame that initiated the navigation? At least, that's what it looks like from https://chromium-review.googlesource.com/c/chromium/src/+/1138081

jochen, would you mind taking a look at this, as the author of the CLs in https://crbug.com/chromium/831073?

### ja...@chromium.org (2019-01-30)

I threw together a quick patch that fixes this locally (https://chromium-review.googlesource.com/c/chromium/src/+/1444951), but I have no idea if there are design problems with it, and I didn't write a test.

### Ju...@microsoft.com (2019-01-30)

Okay, this bug can be also used for address bar spoof.

Repro:
1. Go to https://test.shhnjk.com/frame_busted.php?url=https://www.google.com:8080/
2. Open Devtools (Press F12 on Windows)
Result shows https://www.google.com:8080/ in address bar where as contents is from https://test.shhnjk.com/frame_busted.php.

### jo...@chromium.org (2019-01-30)

hey, thanks for the report, and thanks Nate for looking into this.

I think you're patch is correct. We'd probably also have to pipe the user activation status through.

re https://crbug.com/chromium/926105#c4 - I guess the navigation is also incorrectly treated as something the user typed into the omnibox, that's why the URL shows up before the navigation commits.

### jo...@chromium.org (2019-01-30)

Nate, do you want to take your patch and add tests, or would you rather have me take over?

### ja...@chromium.org (2019-01-30)

@jochen, I'm going out on paternity leave in the next couple days (hopefully!), so if you could take over, I'd be grateful.

### jo...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2f81d000fdb5331121cba7ff81dfaaec25b520a5

commit 2f81d000fdb5331121cba7ff81dfaaec25b520a5
Author: Jochen Eisinger <jochen@chromium.org>
Date: Wed Feb 06 13:02:11 2019

When turning a download into a navigation, navigate the right frame

Code changes from Nate Chapin <japhet@chromium.org>

Bug: 926105
Change-Id: I098599394e6ebe7d2fce5af838014297a337d294
Reviewed-on: https://chromium-review.googlesource.com/c/1454962
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Jochen Eisinger <jochen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#629547}
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/chrome/browser/download/download_browsertest.cc
[add] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/chrome/test/data/downloads/download-attribute.html
[add] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/chrome/test/data/downloads/message.html
[add] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/chrome/test/data/downloads/page-with-frame.html
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/content/browser/download/download_resource_handler.cc
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/content/browser/loader/resource_dispatcher_host_impl.cc
[modify] https://crrev.com/2f81d000fdb5331121cba7ff81dfaaec25b520a5/content/browser/loader/resource_dispatcher_host_impl.h


### jo...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-02-13)

Hi jun.kokatsu@microsoft.com from the VRP panel: can you please remember to upload the source for your PoC to the bug tracker as well as providing a link to the PoC. Thanks.

### wf...@chromium.org (2019-02-13)

Hi Jun - also, screenshots or video really help, because it's hard for us to revisit a bug since it might be fixed by the time we come to reward. Thanks in advance.

### Ju...@microsoft.com (2019-02-13)

Hi Will! Sorry about that :( I'm attaching PoCs and Videos :) Works in latest Stable.

### aw...@google.com (2019-02-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

And $500 for this one, many thanks!

### Ju...@microsoft.com (2019-02-25)

Thanks awhalley@!

Please note that bounty for report from this account should go to charity (not to my personal bank account)! And credit for this account (if applicable) should be following

Jun Kokatsu, Microsoft Browser Vulnerability Research

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/926105?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093891)*
