# Security: Possible to leak global window object via console

| Field | Value |
|-------|-------|
| **Issue ID** | [40095798](https://issues.chromium.org/issues/40095798) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-07-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The global window object is typically accessed through a proxy that allows access checks to be performed. The actual global object is set as a hidden prototype on the proxy and isn't usually exposed to user JavaScript.

The devtools console, however, will display the hidden prototype when a window object is logged and expanded. A page can then access the hidden prototype using custom formatters (if enabled). This allows the page to bypass access checks in some cases.

The console will also display a prototype when it's not hidden, but when the page doesn't normally have access to it. This gives a second method for the page to access the context of a cross-origin target page.

**VERSION**  

Chrome Version: Tested on 75.0.3770.142 (stable) and 77.0.3860.0 (canary)  

Operating System: Windows 10 Pro, version 1903

**REPRODUCTION CASE**

1. In the devtools settings, enable custom formatters.
2. The attached files form two simple websites. Download site1\_index.html and site1\_main.js into a directory and run the following command:

python3 -m http.server 8080

3. Next, download site2\_index.html into another directory and run the following command:

python3 -m http.server 8081

site2\_index.html makes the following modification to the Object prototype:

Object.prototype.testVariable = {};

4. In the browser, navigate to the following location:

<http://localhost:8080/site1_index.html>

5. This page includes a cross-origin iframe (<http://localhost:8081/site2_index.html>). One second after the page loads, it will log the cross-origin window object and location object to the console.

When you expand the window object, the hidden prototype will be captured by a custom devtools formatter. To demonstrate that this has occurred, the value of testVariable set on the hidden prototype will be logged to the console. This should result in output like the following:

testVariable value set on hidden window prototype:  

{}

A similar thing happens when you expand the location object. The prototype is captured and the testVariable value is logged to the console.

In both cases, the prototype shouldn't be available. In the first case, it's because the prototype is the hidden global object. Being able to access that object means that the page can bypass access checks (at least when the target window is in the same renderer process).

In the second case, the location prototype isn't hidden, but the page doesn't normally have access to it. Being able to access it means the page can modify the prototype and any objects in its prototype chain (which is just Object in this case).

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [site1_index.html](attachments/site1_index.html) (text/plain, 236 B)
- [site1_main.js](attachments/site1_main.js) (text/plain, 2.0 KB)
- [site2_index.html](attachments/site2_index.html) (text/plain, 168 B)

## Timeline

### in...@chromium.org (2019-07-22)

caseq@, can you please help to triage this devtools issue.

[Monorail components: Platform>DevTools]

### ca...@chromium.org (2019-07-22)

[Empty comment from Monorail migration]

[Monorail components: -Platform>DevTools Platform>DevTools>JavaScript]

### sh...@chromium.org (2019-08-06)

yangguo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2019-08-07)

+szuend@, who is looking at something similar

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a5fd60e15a3ed1cf5bf6deeed791e5dc5a40126f

commit a5fd60e15a3ed1cf5bf6deeed791e5dc5a40126f
Author: Simon Zünd <szuend@chromium.org>
Date: Thu Aug 08 07:19:54 2019

Calls to {console} require an access check for the provided arguments

This CL adds an access check for the arguments to all calls to
{console} like {console.log}. This is needed since the DevTools
protocol notificiation event does not contain the context in which
the {console.log} call occurred. Only the context of the argument.
When DevTools then reads properties for the preview of the argument,
it uses arguments context, instead of the calling context, potentially
leaking objects/exceptions into the calling context.

Bug: chromium:987502, chromium:986393
Change-Id: I6f7682f7bee94a28ac61994bad259bd003511c39
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1741664
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63122}

[modify] https://crrev.com/a5fd60e15a3ed1cf5bf6deeed791e5dc5a40126f/src/builtins/builtins-console.cc
[modify] https://crrev.com/a5fd60e15a3ed1cf5bf6deeed791e5dc5a40126f/test/unittests/api/access-check-unittest.cc


### sz...@chromium.org (2019-08-08)

David: I think this bug also got fixed with the CL above, but could you please verify that this is indeed the case. Locally the issue no longer reproduces, but I just want to make sure. Please reopen this issue if there is still a way to leak the global window object.

### sh...@chromium.org (2019-08-08)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-13)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
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

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### la...@google.com (2019-08-23)

yangguo@ - please respond to C#10 to  consider M77 merge request

### sz...@chromium.org (2019-08-23)

1. Yes, security bug is severe enough.
2. https://crrev.com/c/1741664
3. Yes, part of canary as of 3878
4. Security fix
5. No
6. No

### la...@google.com (2019-08-24)

merge approved for M77 branch 3865

### sh...@chromium.org (2019-08-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sz...@chromium.org (2019-08-28)

[Empty comment from Monorail migration]

### sz...@chromium.org (2019-08-28)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/52f1d69ecab4b2bfe6fbe2a1c72cfdb846c33168

commit 52f1d69ecab4b2bfe6fbe2a1c72cfdb846c33168
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Jul 23 08:44:17 2021

Revert "Calls to {console} require an access check for the provided arguments"

This reverts commit a5fd60e15a3ed1cf5bf6deeed791e5dc5a40126f.

Reason for revert: As per crbug/1213374 this is not applied consistently. E.g. wrapping object into an array will bypass access checks. With the crrev/c/3041424 however, only accessible properties are shown in console, so logging a restricted object is no longer unsafe.

Original change's description:
> Calls to {console} require an access check for the provided arguments
>
> This CL adds an access check for the arguments to all calls to
> {console} like {console.log}. This is needed since the DevTools
> protocol notificiation event does not contain the context in which
> the {console.log} call occurred. Only the context of the argument.
> When DevTools then reads properties for the preview of the argument,
> it uses arguments context, instead of the calling context, potentially
> leaking objects/exceptions into the calling context.
>
> Bug: chromium:987502, chromium:986393
> Change-Id: I6f7682f7bee94a28ac61994bad259bd003511c39
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1741664
> Commit-Queue: Simon Zünd <szuend@chromium.org>
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#63122}

Bug: chromium:987502, chromium:986393, chromium:1213374
Change-Id: I92a8bb7663ff97de8831ddeb2c8560fb9fa1c12e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3046189
Reviewed-by: Simon Zünd <szuend@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/master@{#75881}

[modify] https://crrev.com/52f1d69ecab4b2bfe6fbe2a1c72cfdb846c33168/src/builtins/builtins-console.cc
[modify] https://crrev.com/52f1d69ecab4b2bfe6fbe2a1c72cfdb846c33168/test/unittests/api/access-check-unittest.cc


### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/986393?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095798)*
