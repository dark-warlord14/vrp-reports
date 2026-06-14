# Wrong security state when redirecting to HTTP

| Field | Value |
|-------|-------|
| **Issue ID** | [40085275](https://issues.chromium.org/issues/40085275) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Mac, Windows |
| **Reporter** | jl...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-09-01 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2845.0 Safari/537.36

Steps to reproduce the problem:
Visit https://www.google.com/#newwindow=1&q=%22http.badssl.com%22
 and click on the first result.

What is the expected behavior?

What went wrong?
Lock icon is shown. Devtools Security Panel says this page is secure.

Did this work before? Yes 

Chrome version: 55.0.2845.0  Channel: canary
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: 

Correct behavior in 414731
Bad behavior in 415292

## Attachments

- [Screen Shot 2017-11-20 at 13.56.07.png](attachments/Screen Shot 2017-11-20 at 13.56.07.png) (image/png, 224.3 KB)

## Timeline

### el...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-09-01)

Regression on Windows and OS X. Looks okay in 55.0.2844, bad in 2845 and 2846, so this is a very recent regression.

### es...@chromium.org (2016-09-01)

Suspect this'll be fixed by https://codereview.chromium.org/2299843002/?

[Monorail components: -UI Security>UX]

### es...@chromium.org (2016-09-01)

(I can't reproduce on 55.0.2846.0 on OS X though.)

### va...@chromium.org (2016-09-01)

I can repro it on: 55.0.2845.0 canary (64-bit) on OSX.
Seems like a duplicate of https://crbug.com/chromium/642838 (SSL state not updated on restoring tab).

### va...@chromium.org (2016-09-02)

re-opening since the fix for https://crbug.com/chromium/642838 did not fix this.

jam@ -- do you want to take on this one also?

### va...@chromium.org (2016-09-02)

[Empty comment from Monorail migration]

### ja...@chromium.org (2016-09-02)

doh, looking. I didn't test this case.

### va...@chromium.org (2016-09-03)

[Empty comment from Monorail migration]

### aa...@google.com (2016-09-03)

When you add Type-Bug-Security, make sure to add Restrict-View-SecurityTeam.

### va...@chromium.org (2016-09-04)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-09-06)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-09-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2016-09-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5

commit 0576b13b74ef273fe311a95cbbb9e1a3bc8045c5
Author: jam <jam@chromium.org>
Date: Wed Sep 07 05:13:10 2016

Fix incorrect SSL state being shown for client redirects.

BUG=643173
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2305093002
Cr-Commit-Position: refs/heads/master@{#416849}

[modify] https://crrev.com/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5/chrome/browser/ssl/ssl_browser_tests.cc
[add] https://crrev.com/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5/chrome/test/data/ssl/in_page_navigation_during_load.html
[add] https://crrev.com/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5/chrome/test/data/ssl/redirect.html
[add] https://crrev.com/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5/chrome/test/data/ssl/redirect_with_mixed_content.html
[modify] https://crrev.com/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/0576b13b74ef273fe311a95cbbb9e1a3bc8045c5/content/browser/frame_host/navigation_controller_impl.h


### ja...@chromium.org (2016-09-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### sh...@chromium.org (2016-12-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-11-14)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-20)

Reproduced with 55.0.2845.0

(used example.com to confirm I could interact with the page, follow links etc, which I could)

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Hi jleedev@ - the Chrome VRP (after a rather long delay, sorry about that!) looked at this issue and decided to reward $2,000!  A member of our finance team will be in touch to arrange details.  Also, how would you like to be credited?

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### jl...@gmail.com (2017-12-01)

Yay! Josh Lee.

### is...@google.com (2017-12-01)

This issue was migrated from crbug.com/chromium/643173?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/643905, crbug.com/chromium/643926, crbug.com/chromium/643963, crbug.com/chromium/644120, crbug.com/chromium/645434, crbug.com/chromium/645485]
[Monorail mergedinto: crbug.com/chromium/642838]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085275)*
