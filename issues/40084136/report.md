# CSP 'referrer' directive ignored for preload requests

| Field | Value |
|-------|-------|
| **Issue ID** | [40084136](https://issues.chromium.org/issues/40084136) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | ki...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2016-04-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36

Steps to reproduce the problem:
1. 
write a html page like this
<?php
header("Content-Security-Policy: referrer origin-when-crossorigin");
?>
<html>
<head>
<link href="http://www.style.com" rel="stylesheet" type="text/css" />
</head>
<img src="https://www.img1.com/">
<img src="http://www.img2.com/x.png">
<img src="http://www.img3.com" rel=”noreferrer”>
<iframe src="http://www.iframe.com/"></iframe>
<script src="http://www.script.com/"></script>
<script>
var xmlhttp;
xmlhttp = new XMLHttpRequest();
xmlhttp.open('http://www.ajaxtesttest.com').send();
</script>
</html>

2. 
set the csp header:
Content-Security-Policy: referrer origin-when-crossorigin
or
Content-Security-Policy: referrer origin-when-cross-origin

3.
view this html page in chrome, and you will see that we can bypass the csp policy by using img/script/link tags

What is the expected behavior?
the resource requested from the webpage with csp header set  should not send the entire referer

What went wrong?
A tag href/JS ajax/iframe-src/Object-data/embed-src will follow the referrer policy in CSP header.
but, style-link-href/img-src/script-src can bypass the csp referer policy header.

btw,
we find that the csp policy in meta tag works fine ,like this:
<meta http-equiv="Content-Security-Policy" content="referrer origin-when-cross-origin">
we think  csp header should be the same with meta tag

Did this work before? N/A 

Chrome version: 50.0.2661.75  Channel: beta
OS Version: OS X 10.11.2
Flash Version: Shockwave Flash 21.0 r0

## Timeline

### ki...@gmail.com (2016-04-21)

affected all platform besides OSX

### rs...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### jw...@chromium.org (2016-04-21)

Assigning to estark@, since referer is in her realm.

### es...@chromium.org (2016-04-21)

This is a preload issue. We pick up a document's referrer policy from meta tags if we scan one while preloading, but we don't use a referrer policy set via header. Looks like we just need to be using document->getReferrerPolicy() here: https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/html/parser/HTMLPreloadScanner.cpp&sq=package:chromium&l=802&rcl=1461222997

### sh...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e49d943e9f5f90411313e64d0ae6b646edc85043

commit e49d943e9f5f90411313e64d0ae6b646edc85043
Author: estark <estark@chromium.org>
Date: Thu Apr 28 01:08:51 2016

Use document referrer policy when preloading

Previously, preload requests used the referrer policy from meta tags
encountered during scanning, but not from headers delivered with the
page. This CL uses the document's current referrer policy when the
preload scan starts.

BUG=605451

Review-Url: https://codereview.chromium.org/1913983002
Cr-Commit-Position: refs/heads/master@{#390264}

[add] https://crrev.com/e49d943e9f5f90411313e64d0ae6b646edc85043/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/referrer-from-document-on-preload-expected.html
[add] https://crrev.com/e49d943e9f5f90411313e64d0ae6b646edc85043/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/referrer-from-document-on-preload.php
[modify] https://crrev.com/e49d943e9f5f90411313e64d0ae6b646edc85043/third_party/WebKit/Source/core/html/parser/HTMLPreloadScanner.cpp
[modify] https://crrev.com/e49d943e9f5f90411313e64d0ae6b646edc85043/third_party/WebKit/Source/core/html/parser/HTMLPreloadScannerTest.cpp


### es...@chromium.org (2016-04-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-04-28)

Updating title to be more specific

### cl...@chromium.org (2016-04-28)

[Empty comment from Monorail migration]

### ki...@gmail.com (2016-04-28)

Thank you for your quick response to this security issue.
How can i get a CVE number, could you assign it?  : )

### es...@chromium.org (2016-04-28)

+timwillis

### ti...@google.com (2016-05-09)

Hello,

CVE-IDs are only assigned where the bug is in a stable build (this issue in in stable) and the bug meets the severity for a reward. We'll take this to our reward panel and let you know if it meets the threshold for a reward and a CVE-ID.

### ki...@gmail.com (2016-05-10)

all right, this issue bypass the chrome W3C standard security policy , i think it should be assigned a CVE-ID. any way , waiting for your conclusions , thank you~ 

### ki...@gmail.com (2016-06-01)

is there any conclusion?

### aw...@chromium.org (2016-07-14)

Congratulation, the panel has decided to award $500 for this bug.  Our finance team will be in touch in the new few weeks with more details.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### ki...@gmail.com (2016-07-18)

Thank you very much, i recieved a email from your finance team. i'll follow the steps in the email. so , is there a CVE-ID assigned or acknowledgment later ?  :)  hope for that

### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-22)

+awhalley@ whether to take this merge in for M53 Dev release on Tuesday (07/26).

### aw...@chromium.org (2016-07-22)

Humm - this should already be in 53 (commit was at 390264, 53 branched at 403382).  

+mbarbella@ - a sheriffbot hiccup or me getting the wrong end of the stick?

### mb...@chromium.org (2016-07-22)

This is related to the same issue we discussed yesterday (it's trying to request a merge to beta using stable + 1 instead of the actual beta milestone). I should be able to fix this later today.

### go...@chromium.org (2016-07-22)

+awhalley@, do we need a merge to M52?

### aw...@chromium.org (2016-07-22)

Nope, already in M52.

### sh...@google.com (2016-07-22)

[Automated comment] Commit may have occurred before M53 branch point (6/30/2016), needs manual review.

### go...@chromium.org (2016-07-22)

Per https://crbug.com/chromium/605451#c24, this is already in M53 branch 2785. So removing "Merge-Review-53" label. 

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/605451?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084136)*
