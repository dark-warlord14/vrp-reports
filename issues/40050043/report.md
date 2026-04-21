# Using the CSS Layout API and contenteditable causes the page to crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40050043](https://issues.chromium.org/issues/40050043) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Mac, Windows |
| **Reporter** | yi...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2019-09-03 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36

Steps to reproduce the problem:
1. Enable chrome://flags/#enable-experimental-web-platform-features
2. Open https://yisibl.github.io/houdini-demo/masonry/index.html

What is the expected behavior?

What went wrong?
The page has crashed.

Did this work before? N/A 

Does this work in other browsers? N/A

Chrome version: 76.0.3809.132  Channel: canary
OS Version: OS X 10.14.5
Flash Version:

## Attachments

- [test-layout-api.html](attachments/test-layout-api.html) (text/plain, 327 B)

## Timeline

### sa...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2019-09-03)

Tested on 78.0.3878.0 (Developer Build) (64-bit),  76.0.3809.132 (Official Build) (64-bit), but not reproducible.

yiorsi@gmail.com: could you find the crash report in chrome://crashes and send the crash report ID?

### yi...@gmail.com (2019-09-03)

Crash ID：3325f9ed3b704c2d

### ma...@chromium.org (2019-09-03)

[Comment Deleted]

### ma...@chromium.org (2019-09-03)

cont.#c4, this is a DCHECK - it's unlikely to be the cause of yiorsi's crash.

The crash report shows the following stacktrace:
0x0000000110127295	(Google Chrome Framework -ng_constraint_space.cc:44 )	blink::NGConstraintSpace::CreateFromLayoutObject(blink::LayoutBlock const&, bool)

+ikilpatrick@chromium.org, could you take a look?

### ma...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-09-04)

Adding security labels, as pointed out in https://crbug.com/chromium/1000480, but setting Security_Impact-None since it requires #enable-experimental-web-platform-features.

### es...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-05)

[Empty comment from Monorail migration]

### ik...@chromium.org (2020-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### aj...@google.com (2021-02-19)

Is this still behind the #enable-experimental-web-platform-features flag, does anyone fancy being an owner?

### ma...@chromium.org (2021-02-19)

[Empty comment from Monorail migration]

### aj...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### aj...@google.com (2021-02-23)

I cannot repro this on Windows asan - perhaps it is fixed?

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-03-16)

 ikilpatrick, kojii: Any chance this could have been fixed? (see https://crbug.com/chromium/1000248#c16)

### ko...@chromium.org (2021-03-16)

Thanks for checking, yes, this should have been fixed when we shipped crbug.com/707656.

### [Deleted User] (2021-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-03-24)

Congratulations, yiorsi@! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let me know the name or handle by which you'd like to be credited in release notes. Nice work and thank you for this report! 

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-06-24)

This issue was migrated from crbug.com/chromium/1000248?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/707656]
[Monorail blocking: crbug.com/chromium/726125]
[Monorail mergedwith: crbug.com/chromium/1000480]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050043)*
