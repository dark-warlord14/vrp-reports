# An iframe on a different domain can change the location to about:blank which enables you to access properties on the window. document.baseURI is leaked from the parent frame.

| Field | Value |
|-------|-------|
| **Issue ID** | [40059980](https://issues.chromium.org/issues/40059980) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ga...@portswigger.net |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-06-16 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


An iframe on a different domain can change the location to about:blank which enables you to access properties on the window. document.baseURI is leaked from the parent frame.


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

When you have the following structure:

domain a -> domain b iframe -> child iframe

It's possible to change child iframe to about:blank from domain a, this then enables you to read properties on the child iframe. One of the properties is document.baseURI and this contains the current location of domain b iframe at the time about:blank is assigned.

Here my enumeration tool demonstrates the issue:
https://portswigger-labs.net/hackability/inspector/?input=x.contentWindow[0].location=%27about:blank%27;setTimeout(()=%3Ealert(x.contentWindow[0].document.baseURI),500)&html=%3Ciframe%20src=//subdomain1.portswigger-labs.net/hackability/inspector?html=%253Ciframe%253E%20id=x%20width=1000%20height=1000%3E

An iframe is injected which points to subdomain1.portswigger-labs.net this then has a child iframe the URL isn't important since it can be changed later. The top most frame then assigns about:blank to the nested child with x.contentWindow[0].location='about:blank', this then allows the top frame to read properties on the nested child frame. document.baseURI contains the current URL of the parent iframe (not the top frame).

It's possible to modify the URL of the domain b iframe and you can read that modification from the top frame:
https://portswigger-labs.net/hackability/inspector/?input=x.contentWindow[0].location=%27about:blank%27;setTimeout(()=%3Ealert(x.contentWindow[0].document.baseURI),500)&html=%3Ciframe%20src=//subdomain1.portswigger-labs.net/hackability/inspector?input=location.hash=1337%26html=%253Ciframe%253E%20id=x%20width=1000%20height=1000%3E

In the example above I modify the hash of the domain b iframe to include a hash of 1337. This can be read by the top frame.


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker gains the ability to read the URL of a cross domain iframe provided the site has at least one frame and the site is frameable.


---

### The cause


#### What version of Chrome have you found the security issue in?

Version 102.0.5005.61 (Official Build) (x86_64)


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Information Leak


#### How would you like to be publicly acknowledged for your report?

Gareth Heyes




## Attachments

- [index.html](attachments/index.html) (text/plain, 307 B)
- [target.html](attachments/target.html) (text/plain, 110 B)
- [Capture d’écran du 2022-06-30 12-19-02.png](attachments/Capture d’écran du 2022-06-30 12-19-02.png) (image/png, 16.2 KB)

## Timeline

### ch...@appspot.gserviceaccount.com (2022-06-16)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-16)

Thanks for the report! Is it possible to provide a minimized poc in html form and attach it to the bug? That could help us better understand the issue. Thanks!

### ga...@portswigger.net (2022-06-17)

[Comment Deleted]

### [Deleted User] (2022-06-17)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@portswigger.net (2022-06-17)

[Comment Deleted]

### ga...@portswigger.net (2022-06-17)

Sorry for the first message it was incorrect. I've confirmed this works on an actual server:
https://portswigger-labs.net/chrome-infoleak-sWpsDfkg9102/

I've also attached the files

### xi...@chromium.org (2022-06-17)

Thanks for providing the PoC. I'm able to reproduce. I wonder if this is because the iframe domain (https://subdomain1.portswigger-labs.net/) is a subdomain of the mainframe (https://portswigger-labs.net/), so the mainframe is able to get its baseURI. Does it reproduce if the iframe is a separate domain?

+arthursonzogni@ to evaluate whether this is a security bug. Triage the same way as https://crbug.com/1276172. Thanks!

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-18)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@portswigger.net (2022-06-20)

It seems that subdomain2 can read subdomain1's URL but not different domains. This could be an issue if a site uses a subdomain to isolate it from the main domain. attachments.domain.com will be able to read domain.com URL or other subdomains provided they could be framed.

https://subdomain2.portswigger-labs.net/xss/xss.php?x=%3Cscript%3Eonload=function(){x.contentWindow[0].location=%27//subdomain1.portswigger-labs.net/chrome-infoleak-sWpsDfkg9102/target.html%27;setTimeout(()=%3E{x.contentWindow[0][0].location.href=%27about:blank%27;},500);setTimeout(()=%3Ealert(x.contentWindow[0][0].document.baseURI),600)}%3C/script%3E%3Ciframe%20src=%22//portswigger-labs.net/xss/xss.php?x=%3Ciframe%20src=/%3E%22%20id=x%3E

### ga...@portswigger.net (2022-06-21)

Here's the simplified test case on a different subdomain:
https://subdomain2.portswigger-labs.net/chrome-infoleak-sWpsDfkg9102/

### ar...@google.com (2022-06-22)

Thanks!

I am unfamiliar with document::baseUri, but the implementation problem is self explanatory:
```
    // TODO(tkent): Referring to ParentDocument() is not correct.  See
    // crbug.com/751329.
    if (Document* parent = ParentDocument())
      return parent->BaseURL();
```

The about:blank document base URL fallback to it's parent baseURL(). It explains this bug.


It also means this problem was known since 2017.

### ar...@chromium.org (2022-06-22)

[Comment Deleted]

### ar...@chromium.org (2022-06-22)

> It also means this problem was known since 2017.

I meant: "The problem existed since at least 2017". However this bug report is useful, because it shows how a cross-origin parent can learn the origin of its children, as long as they are same-domain.

### ga...@portswigger.net (2022-06-22)

> because it shows how a cross-origin parent can learn the origin of its children, as long as they are same-domain.

Not just the origin but the whole URL including query string or hash at the point when about:blank is assigned

### ar...@chromium.org (2022-06-22)

> Not just the origin but the whole URL including query string or hash at the point when about:blank is assigned

Good point!

### ar...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f78ff0ca58822afbde3c9628da90df460d27f37f

commit f78ff0ca58822afbde3c9628da90df460d27f37f
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Wed Jun 29 10:48:08 2022

Add regression test for document.baseURI.

The `document.baseURI` is wrongly implemented in Chrome for about:blank
and about:srcdoc.
It allows leaking cross-origin data. The leak happens only when the two
origin are hosted by the same process.

This patch adds regression tests. I am going to mitigate this bug in a
follow-up.

Bug: 1336904
Change-Id: I027249095fc7ba55dc3f68c772a72f473cfec409
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3723568
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019052}

[modify] https://crrev.com/f78ff0ca58822afbde3c9628da90df460d27f37f/third_party/blink/renderer/core/dom/document.cc
[add] https://crrev.com/f78ff0ca58822afbde3c9628da90df460d27f37f/third_party/blink/web_tests/external/wpt/html/infrastructure/urls/terminology-0/document-base-url-initiated-grand-parent.https.window.js
[modify] https://crrev.com/f78ff0ca58822afbde3c9628da90df460d27f37f/third_party/blink/web_tests/FlagExpectations/disable-site-isolation-trials
[add] https://crrev.com/f78ff0ca58822afbde3c9628da90df460d27f37f/third_party/blink/web_tests/platform/generic/virtual/no-auto-wpt-origin-isolation/external/wpt/html/infrastructure/urls/terminology-0/document-base-url-initiated-grand-parent.https.window-expected.txt
[modify] https://crrev.com/f78ff0ca58822afbde3c9628da90df460d27f37f/third_party/blink/web_tests/VirtualTestSuites
[add] https://crrev.com/f78ff0ca58822afbde3c9628da90df460d27f37f/third_party/blink/web_tests/platform/generic/external/wpt/html/infrastructure/urls/terminology-0/document-base-url-initiated-grand-parent.https.window-expected.txt


### gi...@appspot.gserviceaccount.com (2022-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2aece79fb7b505d8cb5c04a0b9c651a528bd52b1

commit 2aece79fb7b505d8cb5c04a0b9c651a528bd52b1
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Wed Jun 29 12:30:47 2022

Avoid leaking cross-origin data via document.baseURI.

This patch do not improve document.baseURI implementation. It is still
wrong.

The least we can do is preventing it from leaking cross-origin data.

Bug: 1336904
Change-Id: I53d23b12134c4c0c7866353a6e09c327a3ac443b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726194
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019091}

[modify] https://crrev.com/2aece79fb7b505d8cb5c04a0b9c651a528bd52b1/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/2aece79fb7b505d8cb5c04a0b9c651a528bd52b1/third_party/blink/web_tests/FlagExpectations/disable-site-isolation-trials
[delete] https://crrev.com/a5a78267507c8e0b647f1c785e3dfc6c4fb43929/third_party/blink/web_tests/platform/generic/virtual/no-auto-wpt-origin-isolation/external/wpt/html/infrastructure/urls/terminology-0/document-base-url-initiated-grand-parent.https.window-expected.txt


### ar...@chromium.org (2022-06-29)

Let's wait for a day in M105 canary to verify this patch. Then, I will ask to cherry-pick into M104 so that user's can benefits from this sooner.

### ar...@google.com (2022-06-30)

The patch reached 105.0.5151.0
I verified the canary version. It now shows "about:blank". That's still wrong, but at least, we are no more leaking cross-origin data.

This is a security fix. It would be great for users to benefits from this early. I am asking a M104 beta cherry-pick.

### [Deleted User] (2022-06-30)

Merge rejected: M104 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2022-06-30)

> Merge rejected: M104 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Okay, then this is Pri-1.

### [Deleted User] (2022-06-30)

Merge review required: M104 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2022-07-01)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

=> This fixes a security issue: leaking cross-origin URLs.

2. What changes specifically would you like to merge? Please link to Gerrit.

=> https://chromium-review.googlesource.com/c/chromium/src/+/3726194

3. Have the changes been released and tested on canary?

=> It does. See https://crbug.com/chromium/1336904#c21

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

=> No. The bug was there for at least 5 years.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

=> N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

=> Not really needed IMO. Navigating to https://subdomain2.portswigger-labs.net/chrome-infoleak-sWpsDfkg9102/ should display "about:blank".

### ar...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

We don't generally backmerge fixes for low severity issues; given this change is fairly minimal and has been on Canary for over a week, I am okay with this backmerge. I just want to make not of that here as this is outside general security backmerge process. 

### ar...@google.com (2022-07-08)

@amyressler. Landing this patch has some potential of breaking websites. For instance a parent with a sandboxed iframe can no more use document.baseURI. So, I am Happy to do nothing if you believe this is low severity. I am not totally sure about the severity however.
Cherry-picking it into M105 would make it reaches most users 28 days earlier. (Aug 2 vs Aug 30)

This bug allowed reading arbitrary cross-origin URL (including /path #fragment ?attribute).
There are some mitigating factors:
- [Site isolation] on Desktop and partially on Android. It reduces the scope from cross-origin, to same-domain.
- [COOP, XFO, CSP:frame-ancestor] when used correctly. They can make the WindowProxy of the website not accessible to the attacker.

Note: I just realized https://crbug.com/chromium/1336904#c1 pointed out there was a similar bug: https://crbug.com/1276172. It is probably fixed by the same patch. I will check Monday. The first only warned about leak in between a parent with a same-origin sandboxed children. Not sure how Chrome VRP is going to handle this.

### am...@chromium.org (2022-07-08)

Hi, Arthur. Thank you for the details you provided. I concur that this is a borderline medium severity issue.
However, considering the potential breakage and the existing mitigations, I'm not super keen on CP'ing to 104 given that stable release for that is 2 August as you note. 

WRT to the issue pointed out in https://crbug.com/chromium/1336904#c1; please confirm this issue is a duplicate of that. Since the fix was landed here, please merge that issue into this one. I've cc'ed myself onto that issue. If this issue is a true duplicate of that, I'll need to manually get that one into the VRP queue for reward consideration as that one was reported first and prior to this report by quite some time. 
Thanks! 



### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2022-07-11)

Hi @amyressler.


I added a test. We can say the issue pointed out in https://crbug.com/chromium/1336904#c7 (https://crbug.com/chromium/1276172) is not the same. I say this, because it isn't fixed yet. My patch was only about about:blank, but I noticed it was also not correctly implemented for about:srcdoc.  It is still not fixed. Since it would require a different fix, we can say they are different. They also have different impact, because about:srcdoc is guaranteed to be created by its parent.

### ar...@chromium.org (2022-07-11)

BTW. Both bugs are "children" from https://crbug.com/chromium/751329 where it was noticed the document.baseURI implementation was wrong.

### am...@chromium.org (2022-07-12)

Thank you for the update and info arthursonzogni@; removing merge label for 104 and allowing time for the other issue to be fixed as well and appears not special handling will be required from a VRP aspect either. 

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations, Gareth! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2023-12-21)

Just to leave a breadcrumb here, the new NewBaseUrlInheritanceBehavior feature from https://groups.google.com/a/chromium.org/g/blink-dev/c/qhl64uMLjGA/m/SiugtWfvBAAJ now causes the grandchild frame to inherit its baseURI from the initiator of the navigation (i.e., the grandparent frame) rather than the parent frame, which is the same place it inherits the origin.  That means there's still no cross-origin leak from the parent to the grandparent.  (This came up in https://crbug.com/chromium/1513364.)

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1336904?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059980)*
