# Improper handling of duplicate `<html>` and `<body>` tags enables CSP nonce leakage

| Field | Value |
|-------|-------|
| **Issue ID** | [41485789](https://issues.chromium.org/issues/41485789) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | fe...@gmail.com |
| **Assignee** | ph...@google.com |
| **Created** | 2023-12-19 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Visit [https://poc.minimal.blue/nonce?name=%3Cstyle%3Ebody[nonce\\*=secret]{background:red}%3C/style%3E%3Cbody](https://poc.minimal.blue/nonce?name=%3Cstyle%3Ebody%5Bnonce%5C*=secret%5D%7Bbackground:red%7D%3C/style%3E%3Cbody) The page is served with the header `Content-Security-Policy: script-src 'nonce-secret'`
2. Notice that the CSS selector `body[nonce\*=secret]` can access the value of the CSP nonce, applying the style to the page (red background). This enables an attacker to bypass the CSP by leaking the nonce value via CSS.
3. An equivalent attack can be performed by injecting an unterminated `<html` tag: [https://poc.minimal.blue/nonce?name=%3Cstyle%3Ehtml[nonce\\*=secret]{background:red}%3C/style%3E%3Chtml](https://poc.minimal.blue/nonce?name=%3Cstyle%3Ehtml%5Bnonce%5C*=secret%5D%7Bbackground:red%7D%3C/style%3E%3Chtml)

**Problem Description:**  

Please CC Marco Squarcina ([squarcina@gmail.com](mailto:squarcina@gmail.com)) to this bug

According to the HTML spec, whenever the CSP policy is delivered to the browser over an HTTP header, CSP nonce values must by hidden to CSS selectors to prevent exfiltration via side-channels, see <https://html.spec.whatwg.org/multipage/urls-and-fetching.html#nonce-attributes> and <https://github.com/whatwg/html/issues/2369>.

We discovered that a markup injection before a `<script>` element, which includes the nonce attribute, can result in the nonce value being accessible. This behavior can be replicated by injecting a dangling `<html` or `<body` tag, as shown in the code below. Assume that a valid CSP policy is set via an HTTP header, e.g., `Content-Security-Policy: script-src 'nonce-secret'`:

<!DOCTYPE html>
<head>
<title>PoC</title>
</head>
<body>
<h1>CSP Nonce Bypass</h1>
Hello <style>body[nonce\\*=sec]{background:green}</style><body
<script nonce="secret" src="https://example.com/good.js"></script>
</body>
</html>

Please refer to [https://poc.minimal.blue/nonce?name=%3Cstyle%3Ebody[nonce\\*=secret]{background:red}%3C/style%3E%3Cbody](https://poc.minimal.blue/nonce?name=%3Cstyle%3Ebody%5Bnonce%5C*=secret%5D%7Bbackground:red%7D%3C/style%3E%3Cbody) for a working example.

The issue affects major browsers including Chrome, Safari, and Firefox. We are jointly reporting the vulnerability to Apple and Mozilla.

### Detailed information and root cause

After some investigation, we believe that the issue is caused by how the HTML parser handles duplicate `<html>` and `<body>` elements. These elements are merged into their original (i.e., parent) elements, causing all the attributes of the duplicate tags to be added to the parent element. To exemplify this, the following code

<!DOCTYPE html>
<html lang="en">
<head></head>
<body>
<html a="w">
<html b="0"></html>
</html>
<html c="y"></html>
</body>
</html>

gets parsed as

<!DOCTYPE html>
<html lang="en" a="w" b="0" c="y">
<head></head>
<body></body>
</html>

We noticed that the merging operation bypasses standard security checks, including hiding the `nonce` attribute. Given that these checks are omitted, the `nonce` attribute is merged into the parent `<html>` tag as a normal attribute resulting accessible through CSS selectors.

### Code analysis

The `HTMLTreeBuilder::ProcessStartTagForInBody` function has special cases for handling `<html>` and `<body>` tags inside the document. These special cases call the `HTMLConstructionSite::InsertHTMLBodyStartTagInBody` and `InsertHTMLHtmlStartTagInBody` functions, respectivly.

(Code from <https://chromium.googlesource.com/chromium/src/+/f2e5b0194c80a3fda50d2bd0c36d94650c249d17/third_party/blink/renderer/core/html/parser/html_tree_builder.cc>)

Both functions rely on calling `HTMLConstructionSite::MergeAttributesFromTokenIntoElement` to merge the attributes into the original element, without performing any validation before using the `Element::setAttribute` method (which subsequently calls `Element::SetAttributeInternal`):

(Code from <https://chromium.googlesource.com/chromium/src/+/f2e5b0194c80a3fda50d2bd0c36d94650c249d17/third_party/blink/renderer/core/html/parser/html_construction_site.cc>)  

(Code from <https://chromium.googlesource.com/chromium/src/+/f2e5b0194c80a3fda50d2bd0c36d94650c249d17/third_party/blink/renderer/core/dom/element.cc>)

We believe that the lack of safeguards in the implementation of the tag merging code could lead to additional vulnerabilities that should be promptly investigated.

Cheers,  

Georg Felber (TU Wien)  

Marco Squarcina (TU Wien)

**Additional Comments:**

\*\*Chrome version: \*\* 120.0.6099.109 \*\*Channel: \*\* Stable

**OS:** Linux

## Timeline

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### bb...@google.com (2023-12-19)

I appear to be able to replicate this in a situation similar to the above. 

Initially setting Security-level Medium pending other's involvement. 

### bb...@google.com (2023-12-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### bb...@google.com (2023-12-19)

mkwest, titouan - Could you please take a look and advice on priority and severity?  I've put this on ContentSecurityPolicy for now but really, it's kind of a bug in the html parser.  Your thoughts would be appreciated. 

### bb...@google.com (2023-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### ad...@google.com (2023-12-19)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-12-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2023-12-21)

Redirecting to clamy@, I've since switched teams.

### sq...@gmail.com (2023-12-21)

The Firefox issue is being tracked at https://bugzilla.mozilla.org/show_bug.cgi?id=1871112

### ph...@chromium.org (2023-12-22)

Could the solution be to add <body and <html checks here? https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/csp/content_security_policy.cc;l=155-156;drc=8e78783dc1f7007bad46d657c9f332614e240fd8;bpv=1;bpt=1

If so, I should be able to upload a CL soon.

### ph...@chromium.org (2023-12-22)

No I think I was mistaken.  Those checks were for a different kind of attack.

### ph...@chromium.org (2023-12-22)

The issue here seems like `HideNonce()` was somehow not executed on the body tag.  Trying to dig into why it wasn't.

### ph...@chromium.org (2023-12-22)

From the DevTools, the two `body` tags were molded into one with the nonce value.  `HideNonce()` was executed on a body tag, but the nonce value was null so `HideNonce()` did nothing.  I'm not sure whether it was called on the tag before or after they're molded together.

### ph...@chromium.org (2023-12-22)

Also re-reading the checks in https://crbug.com/chromium/1513216#c13, I think it is about the same attack, but somehow for body tags, the `ContentSecurityPolicy::IsNonceableElement()` was never called.

### ph...@chromium.org (2023-12-22)

I get it now.  The `InsertedInto()` was called when the first body element was found, which didn't have the nonce attribute yet.  When the second body/html tag was found, we merge the attributes into the existing element.  All I needed to do is add a `HideNonce()` call there. See https://crrev.com/c/5149755

### sq...@gmail.com (2023-12-23)

We didn't test the revision, but it should fix the edge case we reported. Still, we are somehow concerned that there could be additional underlying issues due to the inconsistent execution flow between a typical tag creation and a special case like tag merging. For example, attribute changes caused by html and body tag merging does not seem to trigger mutation events (if we correctly understood the code).

Mozilla folks are also investigating the alignment of the implementation to the spec: https://html.spec.whatwg.org/#parsing-main-inbody It would be good to sync the efforts to ensure cross-browser consistency.

### gi...@appspot.gserviceaccount.com (2023-12-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/62d76556fcf250ecb0f63874be8cdd3db51f2a64

commit 62d76556fcf250ecb0f63874be8cdd3db51f2a64
Author: Jonathan Hao <phao@chromium.org>
Date: Mon Dec 25 17:20:10 2023

[CSP] Hide nonce before merging attributes to html or body tags.

See https://crbug.com/1513216

Bug: 1513216
Change-Id: I6dd69249ad35b53f77d7f1fec2662d4074b2cc01
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5149755
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Jonathan Hao <phao@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1240901}

[modify] https://crrev.com/62d76556fcf250ecb0f63874be8cdd3db51f2a64/third_party/blink/renderer/core/dom/element.h
[modify] https://crrev.com/62d76556fcf250ecb0f63874be8cdd3db51f2a64/third_party/blink/renderer/core/html/parser/html_construction_site.cc


### gi...@appspot.gserviceaccount.com (2023-12-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a18df8a55306e6519bae468b4cd9ae60a0ae8e99

commit a18df8a55306e6519bae468b4cd9ae60a0ae8e99
Author: Jonathan Hao <phao@chromium.org>
Date: Wed Dec 27 15:52:59 2023

[CSP] Regression WPT for nonce hiding on dangling html/body

See bug or https://crrev.com/c/5149755

Bug: 1513216
Change-Id: Ie04e0d900e8d49ffd99fc60579f50cbd460cad2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5148217
Commit-Queue: Jonathan Hao <phao@chromium.org>
Commit-Queue: Yifan Luo <lyf@chromium.org>
Reviewed-by: Yifan Luo <lyf@chromium.org>
Auto-Submit: Jonathan Hao <phao@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1241168}

[add] https://crrev.com/a18df8a55306e6519bae468b4cd9ae60a0ae8e99/third_party/blink/web_tests/external/wpt/content-security-policy/nonce-hiding/dangling-html-or-body.html.headers
[add] https://crrev.com/a18df8a55306e6519bae468b4cd9ae60a0ae8e99/third_party/blink/web_tests/external/wpt/content-security-policy/nonce-hiding/dangling-html-or-body.html


### ph...@chromium.org (2023-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-28)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-29)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-30)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-31)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-01)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@chromium.org (2024-01-02)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/5149755

2. Has this fix been tested on Canary?
Yes.  Tested on 122.0.6218.0 (Official Build) canary (arm64) 

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
No known risks.

4. Does this fix pose any known compatibility risks?
No known risks.

5. Does it require manual verification by the test team? If so, please describe required testing.
No.

### [Deleted User] (2024-01-02)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-03)

Requesting merge to beta M121 because latest trunk commit (1241168) appears to be after beta branch point (1233107).

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-04)

tbh, while this change is small, I'm not sure of the potential ramifications of this change in terms of CSP as a whole; and since we are in the middle of 121 in Beta cycle and it is going to be promoted to Stable in a couple of weeks + Mozilla is working on their fix for a similar issue, I think it would be best to defer backmerging this fix and let it matriculate into Stable on it's own. Please let me know if there are any issues with this (or re-add the merge label, which will return this issue back to my review queue). 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### mk...@google.com (2024-01-09)

+Anne from WebKit to coordinate on a similar report.

### an...@gmail.com (2024-01-09)

[Comment Deleted]

### an...@gmail.com (2024-01-09)

Heya, thanks for adding me Mike! It would be great if we could better coordinate these kind of cross-browser issues in the future. I have the following concerns:

1. https://github.com/web-platform-tests/wpt/pull/43803 landed in public. It doesn’t seem great to zero-day everyone that way.
2. It landed without .tentative. That seems bad as the HTML standard does not cover the behavior you added.
3. The fix you created allows content to overwrite an existing nonce.

Our tentative fix only uses the nonce attribute if there was not one already or if the private nonce field was empty. We would be open to dropping nonce attributes added in this manner instead.

### ph...@chromium.org (2024-01-09)

About 1 and 2, it was my mistake to land the WPT in public before fixes are deployed.  I'll make sure to loop you in future cross-browser issues like this and I'll also add .tentative to the test names.

About 3, I'm not sure what you mean by overwriting an existing nonce.  My understanding from https://github.com/whatwg/html/pull/2373 is that HideNonce() clears the nonce attribute on the element but stores it internally so the getter can still get it, which follows the spec.
mkwst@: Is that true?

### an...@gmail.com (2024-01-09)

Thanks, that's appreciated. I hope we can use this incident to make progress on https://github.com/whatwg/meta/issues/281.

And that is true. But if a trusted script did body.nonce = "blah" and then you had this markup injection following that, you'd end up with a different nonce. It's somewhat contrived, but I prefer our fix or simply not forwarding the nonce attribute at all.

### ph...@chromium.org (2024-01-09)

I see.  That makes sense.  Anne@: Are we in the process of adding your suggested behavior to the spec?

### an...@gmail.com (2024-01-10)

I think we should wait with that until everyone has shipped. We can coordinate what a possible change to HTML might look like in private.

### an...@gmail.com (2024-01-18)

I created https://github.com/whatwg/html/security/advisories/GHSA-wwmc-fjr4-mcg5 to coordinate.

### sq...@gmail.com (2024-01-18)

Anne, can you add us (i.e., the original reporters) to the GitHub issue to follow the progress? Our handles are "gfelber" and "lavish". Thanks!

### am...@google.com (2024-01-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-19)

Congratulations Georg and Marco! The Chrome VRP Panel has decided to award you $3,000 for this high quality report of an exploitation mitigation bypass. A member of our Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-20)

This issue was migrated from crbug.com/chromium/1513216?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### ph...@google.com (2024-03-05)

1. Number of CLs needed for this fix and links to them.
   
   - One CLs. The second one is just tests so may not be necessary.
   - <https://chromium.googlesource.com/chromium/src/+/62d76556fcf250ecb0f63874be8cdd3db51f2a64>
2. Level of complexity (High, Medium, Low - Explain)
   
   - Low. Basically a one-line fix.
3. Has this been merged to a stable release? beta release?
   
   - It's already in stable.
4. Overall Recommendation (Yes, No)
   
   - Yes.

### ap...@google.com (2024-03-14)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 81a4b090dbb51132b3e5cdac9152f18451fcf0f9
Author: Jonathan Hao <phao@chromium.org>
Date:   Thu Mar 14 16:09:22 2024

    [M120-LTS][CSP] Hide nonce before merging attributes to html or body tags.
    
    See https://crbug.com/1513216
    
    (cherry picked from commit 62d76556fcf250ecb0f63874be8cdd3db51f2a64)
    
    Bug: 1513216
    Change-Id: I6dd69249ad35b53f77d7f1fec2662d4074b2cc01
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5149755
    Commit-Queue: Jonathan Hao <phao@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1240901}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5340567
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Reviewed-by: Jonathan Hao <phao@chromium.org>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Owners-Override: Michael Ershov <miersh@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1988}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/core/dom/element.h
M       third_party/blink/renderer/core/html/parser/html_construction_site.cc

https://chromium-review.googlesource.com/5340567


### ap...@google.com (2024-04-01)

Project: chromium/src
Branch: refs/branch-heads/6099_225

commit ee544f4b9aa17d9a2673d31b7ec57dfa1e9478bb
Author: Richard Yeh <rcy@google.com>
Date:   Mon Apr 01 14:58:54 2024

    [CfM-R120] Squash changes from branch-heads/6099 through 2024-03-27 (111 commits).
    
    Obtained from:
      git checkout branch-heads/6099_225
      gclient sync -D
      git cherry-pick ^HEAD branch-heads/6099
    
    Skipped all conflicts:
      Automated update from google3
      Incrementing VERSION to 120.0.6099.*
      [lacros skew tests] Refresh skew tests for M12*
    
    120.0.6099.233
    
    [lacros] Filter flaky test DetachToOwnWindowFromMaximizedWindow/0
    
    Merge: Flaky on M121
    
    DetachToBrowserTabDragControllerTest.DetachToOwnWindowFromMaximizedWindow/0
    is quite flaky on Lacros. This CL adds it to the corresponding filter
    file (next to many other TabDragging tests that are already filtered).
    
    (cherry picked from commit 7e6089dfc656ceb28bc41a556b5ba95e86d9d827)
    
    Bug: 1489116, 1336691, 1516748
    Change-Id: I99abf7c0220f357f3a652b7dc836b1e9eb2b96f7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4998866
    Auto-Submit: Marc Treib <treib@chromium.org>
    Commit-Queue: Marc Treib <treib@chromium.org>
    Reviewed-by: Ankush Singh <ankushkush@google.com>
    Commit-Queue: Ankush Singh <ankushkush@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1218738}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5193090
    Auto-Submit: Robert Liao <robliao@chromium.org>
    Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
    Commit-Queue: Robert Liao <robliao@chromium.org>
    Owners-Override: Robert Liao <robliao@google.com>
    Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1774}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [Gardening] Disable OSSettingsCrostiniPageTest.AllJsTests
    
    Merge: Flaky on M120
    
    This test appears to be flaky.
    
    (cherry picked from commit e4f8f393c42737d8160e404c35e6c3ed88a215ff)
    
    Bug: 1504815
    Change-Id: Ieeac876bae0816ebe49bb8833ea7e1b80fb2c396
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5057468
    Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
    Commit-Queue: Ian Vollick <vollick@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1228498}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5193349
    Reviewed-by: Wes Okuhara <wesokuhara@google.com>
    Owners-Override: Robert Liao <robliao@google.com>
    Commit-Queue: Robert Liao <robliao@chromium.org>
    Commit-Queue: Wes Okuhara <wesokuhara@google.com>
    Auto-Submit: Robert Liao <robliao@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1775}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.234
    
    [M120] Infra: Remove linux-wayland-rel from required CQ builders
    
    linux-wayland-rel is not providing much value in CQ, as it has uniquely
    detected only a small number of failures in the last 90 days. It is
    also a very expensive builder resource-wise. As a result, we are
    removing it from the list of mandatory CQ builders.
    
    (cherry picked from commit a87d89251412480ac24abff3c8cea2812c83cecb)
    
    Bug: 1498240
    Change-Id: I3ef8bb673ba4d81dfc9a3b6ba380df47debd97e7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5020413
    Reviewed-by: Stephanie Kim <kimstephanie@google.com>
    Commit-Queue: Gary Tong <gatong@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1224017}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5193168
    Reviewed-by: Gary Tong <gatong@chromium.org>
    Auto-Submit: Garrett Beaty <gbeaty@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1777}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.75.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8759057723462663857
    
    Change-Id: Id2d11091dab6403436e80804d444caf324f5b170
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5196267
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1779}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I1476376f01b765c10d1b399327d24d9cdf879d26
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5194565
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1780}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.235
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I4035d496316056f91e8dccaeb890bca55cf9dc87
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5195729
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1785}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.76.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758967063165942289
    
    Change-Id: I89298dc2c416c3212538d04e0ba9597f9b53fa32
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5196810
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1786}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.236
    
    Automated Commit: LKGM 15662.77.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758876679277724417
    
    Change-Id: Iad20825e2f584174a80974682e4cb2bdc3732037
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5197892
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1791}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I9a37c17000b4da6edc1d86fbc07391856861e257
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5198847
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1793}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.237
    
    Roll src/clank in M120 from c5a1fb211796 to 4e72ff435bcf
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/c5a1fb211796..4e72ff435bcf
    
    Generated by: go/bbid/8758743600659139025
    
    Change-Id: Iae0311f9fc5323c8920be0539c6da3b671c57ce2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5200925
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1797}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.78.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758785958706729233
    
    Change-Id: I388ee67a7bd405c624c6d73dd84284b213e6249c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5200751
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1798}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I2306a528e2473edb9a5c372b7e53e9974007123a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5200547
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1799}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [lacros] Update lacros QA qualified version
    
    This CL will update lacros version in //chrome/LACROS_QA_QUALIFIED_VERSION. This
    file will be used in Upreving the RootFS-Lacros in the CROS image.
    
    If this CL caused regressions, please revert and pause the autoroller at
    https://luci-scheduler.appspot.com/jobs/chrome/lacros-qa-qualified-tracking-roller
    Also please file a bug to OS>LaCrOS>Partner, and CC svenzheng@chromium.org.
    
    R=rubber-stamper@appspot.gserviceaccount.com
    
    Change-Id: I143a341b0872b69ef73bf2fef5a481bf9a669b00
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5201885
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: lacros-tracking-roller@chops-service-accounts.iam.gserviceaccount.com <lacros-tracking-roller@chops-service-accounts.iam.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1802}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Fix OverlayProcessorWebview::Manager life-time
    
    Class is created on RenderThread and we guarantee that it will be alive
    until display compositor is destroyed, but UpdateOverlayBuffer is run
    on GpuMain and can be posted while OverlayProcessor is alive but run
    right after it's destroyed.
    
    Manager can already outlive OverlayProcessor due to pending callbacks
    and can be destroyed on both threads, so we can just extend life-time
    for the duration of UpdateOverlayBuffer.
    
    (cherry picked from commit 86a87b972fe850b48542bfc435a92c766e0a13c6)
    
    Bug: 1515741
    Change-Id: I80584596951b98ce99b9b4cbd4a3364278d1e967
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5176835
    Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
    Reviewed-by: Bo Liu <boliu@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1244651}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5199999
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1803}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.238
    
    Automated Commit: LKGM 15662.79.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758695469932918097
    
    Change-Id: Iba95a92240546c2ec59468ae16a8221866f889e9
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5203232
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1806}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll ChromeOS Arm Experimental AFDO profile from 120-6099.42-1701691574-benchmark-120.0.6099.78-r1 to 120-6099.186-1704106678-benchmark-120.0.6099.192-r1
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/cros-afdo-arm-exp-chromium-stable
    Please CC c-compiler-chrome@google.com,mobiletc-prebuild@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Chromium Stable Branch: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Tbr: mobiletc-prebuild@google.com
    Change-Id: Ie5fa06964ec66c590269745f7b19b79019c0cc3a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5205900
    Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1809}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll ChromeOS Atom AFDO profile from 120-6099.42-1701691574-benchmark-120.0.6099.80-r1 to 120-6099.203-1704712844-benchmark-120.0.6099.235-r1
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/cros-afdo-atom-chromium-stable
    Please CC c-compiler-chrome@google.com,mobiletc-prebuild@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Chromium Stable Branch: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Tbr: mobiletc-prebuild@google.com
    Change-Id: Ib0e841b8130bbfc8cf7f9ef9ee7efddcdb9967a9
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5204863
    Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1810}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll ChromeOS Bigcore AFDO profile from 120-6099.42-1701686458-benchmark-120.0.6099.80-r1 to 120-6099.186-1704710639-benchmark-120.0.6099.235-r1
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/cros-afdo-bigcore-chromium-stable
    Please CC c-compiler-chrome@google.com,mobiletc-prebuild@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Chromium Stable Branch: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Tbr: mobiletc-prebuild@google.com
    Change-Id: I0f2dec06bc667d15440eb3db904b638aad5e0881
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5203240
    Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1811}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll ChromeOS Arm AFDO profile from 120-6099.42-1701693515-benchmark-120.0.6099.80-r1 to 120-6099.186-1704113013-benchmark-120.0.6099.204-r1
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/cros-afdo-arm-chromium-stable
    Please CC c-compiler-chrome@google.com,mobiletc-prebuild@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Chromium Stable Branch: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Tbr: mobiletc-prebuild@google.com
    Change-Id: Ia5e42b1d7e5380407babb7e2ad3cb40adc3d4a24
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5206097
    Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1812}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120][infra] De-orchestrate linux-wayland-rel.
    
    try/linux-wayland-rel was removed from the CQ by
    https://crrev.com/c/5020413. For builders that aren't on the CQ, we
    don't use the orchestrator pattern because non-CQ try builders aren't
    run nearly as often as CQ builders and so they don't benefit nearly as
    much by having machines dedicated to performing compilation for them.
    
    Bug: 1511076
    Change-Id: Ib22d6af4c9ce9a0bc99e51b8c5b07fbde09cf6ad
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5193464
    Commit-Queue: Garrett Beaty <gbeaty@google.com>
    Reviewed-by: Gary Tong <gatong@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1813}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [Merge 120] Not creating experiment manager for ash internal profiles
    
    (cherry picked from commit 0a7532844504cea5abfd9595cdb1a9a4045ffc85)
    
    Bug: 1516997
    Change-Id: Ifbfffcd523d9f2a21d7cbca6ad1fed218e9382e8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5182037
    Reviewed-by: Anton Maliev <amaliev@chromium.org>
    Commit-Queue: Nan Lin <linnan@chromium.org>
    Reviewed-by: Ryan Tarpine <rtarpine@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1244913}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5189905
    Cr-Commit-Position: refs/branch-heads/6099@{#1815}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/v8 in M120 from 6372efd0ead5 to e13e29a9b6ba
    Commits rolled:
    https://chromium.googlesource.com/v8/v8.git/+log/6372efd0ead5..e13e29a9b6ba
    
    Generated by: go/bbid/8758622806360917009
    
    Change-Id: I311639ad5ed4c1817caa7f4d5e1d213925c3d28e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5207671
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1816}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll Amd64 AFDO from 120.0.6099.80_rc-r1-merged to 120.0.6099.235_rc-r1-merged
    
    This CL may cause a small binary size increase, roughly proportional
    to how long it's been since our last AFDO profile roll. For larger
    increases (around or exceeding 100KB), please file go/crostc-bug.
    
    Please note that, despite rolling to chrome/android, this profile is
    used for both Linux and Android.
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/afdo-chromium-stable
    Please CC c-compiler-chrome@google.com,mobiletc-prebuild@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Chromium Stable Branch: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Tbr: mobiletc-prebuild@google.com
    Change-Id: I44130336329f7a5ab0af85ba2315e329db896512
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5204864
    Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1817}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.259
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I4d8ed054753b79ea4a4623434d67e76569856e6c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5212025
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1820}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.80.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758604760377473665
    
    Change-Id: Ia4e8302f5ca183f2e50ac54412c0fe1b8514e67d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5212125
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1821}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/internal in M120 from 364f1c4fb31a to 79571debd475
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/364f1c4fb31a..79571debd475
    
    Generated by: go/bbid/8758520884339931857
    
    Change-Id: I96bf51a57de0ae46bb06d4e36cfb3f98272d7167
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5215225
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1825}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.260
    
    Automated Commit: LKGM 15662.81.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758514256847721809
    
    Change-Id: Ifade9c76e795b46a07876d8704c4693f4d18be7d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5215116
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1828}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I26e9cc48055ca97d8c0de82396cb8f15eb17b2a8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5215009
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1829}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120] mojom_ts_generator: Handle empty module path identically to '/'
    
    Fixes an issue with Python 3.11.2. Workaround originally proposed at
    https://bugs.chromium.org/p/chromium/issues/detail?id=1422178#c4
    
    (cherry picked from commit 360261c3d45265809604fb64f558dcbee5df50fb)
    
    Bug: 1422178
    Change-Id: I2486fca59de0b28efc38020de8cd3d01a56eca98
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5125915
    Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1238190}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5200977
    Commit-Queue: Josip Sokcevic <sokcevic@chromium.org>
    Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1832}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Update rendering state of automatic pull nodes before graph rendering
    
    In rare cases, the rendering fan out count of automatic pull node
    does not match the main thread fan out count after recreating
    a platform destination followed by disconnection.
    
    This CL forces the update of the rendering state of automatic
    pull nodes before graph rendering to make sure that fan out counts
    are synchronized before executing the audio processing function call.
    
    NOTE: This change makes 2 WPTs fail. The follow-up work is planned
    to address them once this patch is merged.
    
    (cherry picked from commit f4bffa09b46c21147431179e1e6dd2b27bc35fbc)
    
    Bug: 1505080
    Test: Locally confirmed that ASAN doesn't crash on all repro cases.
    Change-Id: I6768cd8bc64525ea9d56a19b9c58439e9cdab9a8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5131958
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1246718}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5214669
    Auto-Submit: Hongchan Choi <hongchan@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1833}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.265
    
    Automated Commit: LKGM 15662.82.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758423826930322225
    
    Change-Id: Ibd8ac7d50401709abb6db57141f27c7d3d8555c3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5219773
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1837}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.266
    
    Automated Commit: LKGM 15662.83.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758333062829739617
    
    Change-Id: Ia0ee3db028bb79faa5cb9a8629e5fd8c2d063478
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5220530
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1841}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I677f05e4d58f9cbebfd4ca0c0331c960279cc9ad
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5221401
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1842}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.267
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I139634985aafa0442b8089852729fc9e92006558
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5224301
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1846}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.84.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758242345705406305
    
    Change-Id: I6cac57959a3fc3b9f946f83b3de9166d00f8079c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5224363
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1847}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.268
    120.0.6099.269
    
    [skylab_tests] Update skylab cros img (release)
    
    This cl only affect Lacros or Skylab on-device config builders like
    lacros-amd64-generic-chrome-skylab or "ChromeOS FYI Release Skylab
    (kevin)". This cl will certainly NOT affect linux-lacros builders
    (linux-lacros-tester-rel, linux-lacros-rel, etc) or any other platforms.
    This CL will update cros image version for skylab tests.
    CROS_BOARD_DEV, CROS_BOARD_BETA and CROS_BOARD_STABLE are updated according
    to Omaha.
    
    If this CL caused regressions, please revert and pause the autoroller at
    https://luci-scheduler.appspot.com/jobs/chrome/lacros-skylab-tests-cros-img-roller
    Also please file a bug to OS>LaCrOS>Partner, and CC svenzheng@chromium.org.
    
    R=rubber-stamper@appspot.gserviceaccount.com
    
    Requires-Testing: True
    Change-Id: I5217cc24d4b41261b6ddd7aa4910fcc712e4172b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5227020
    Auto-Submit: skylab-test-cros-roller@chops-service-accounts.iam.gserviceaccount.com <skylab-test-cros-roller@chops-service-accounts.iam.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1852}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/clank in M120 from 4e72ff435bcf to 19ba5fd69e3d
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/4e72ff435bcf..19ba5fd69e3d
    
    Generated by: go/bbid/8758107530093051793
    
    Change-Id: I6707f52ba3ef0b76615625acb2c5472a1a5f4674
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5228077
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1854}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.85.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758151863628590097
    
    Change-Id: I46cb4b74f53e6fc6fe5e703a638884115f71db63
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5227766
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1855}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I55ab59bc742fda9941faa48a096f7ba79f8e7093
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5225183
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1856}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Fix use-after-free in DrawTextInternal
    
    DrawTextInternal was calling GetOrCreatePaintCanvas multiple times,
    once at the start of the function, once inside of the
    BaseRenderingContext2DAutoRestoreSkCanvas helper class and once in the
    Draw call. GetOrCreatePaintCanvas destroys the canvas resource provider
    if the GPU context is lost. If this happens on the second call to
    GetOrCreatePaintCanvas, destroying the resource provider will
    invalidate the cc::PaintCanvas returned by the first call to
    GetOrCreatePaintCanvas.
    
    The GPU process can technically crash at any point during the renderer
    process execution (perhaps because of something another renderer
    process did). We therefore have to assume that any call to
    GetOrCreatePaintCanvas can invalidate previously returned
    cc::PaintCanvas.
    
    (cherry picked from commit d4a197e4913f8e5072263b59aedc29f2b5af3e93)
    
    Change-Id: Ifa77735ab1b2b55b3d494f886b8566299937f6fe
    Fixed: 1511567
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5198419
    Reviewed-by: Fernando Serboncini <fserb@chromium.org>
    Commit-Queue: Jean-Philippe Gravel <jpgravel@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1248204}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5230237
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1859}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120] Fix UAF in SourceStreamToDataPipe
    
    SourceStreamToDataPipe::ReadMore() is passing a callback with
    Unretained(this) to net::SourceStream::Read(). But this callback may be
    called even after the SourceStream is destructed. This is causing UAF
    issue (crbug.com/1511085).
    
    To solve this problem, this CL changes ReadMore() method to pass a
    callback with a weak ptr of this.
    
    (cherry picked from commit 6e36a69da1b73f9aea9c54bfbe6c5b9cb2c672a5)
    
    Bug: 1511085
    Change-Id: Idd4e34ff300ff5db2de1de7b303841c7db3a964a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5179746
    Reviewed-by: Adam Rice <ricea@chromium.org>
    Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1244526}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5231558
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1860}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.270
    
    Roll src/v8 in M120 from e13e29a9b6ba to 71b6b5a68e08
    Commits rolled:
    https://chromium.googlesource.com/v8/v8.git/+log/e13e29a9b6ba..71b6b5a68e08
    
    Generated by: go/bbid/8758011277371366193
    
    Change-Id: I7d804b29213127ee09d9f8a990e5f4fa634637fc
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5233001
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1862}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Iacdd731345139414635519c706e1cd81f6ee12ba
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5232662
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1863}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.86.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8758057195378695121
    
    Change-Id: Id6306c045ec8ccc3598cc46aa7ebb2c4501b1317
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5234396
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1864}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Skipped Exit early from RTCPeerConnection
    120.0.6099.271
    
    Automated Commit: LKGM 15662.87.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8757966747157109265
    
    Change-Id: I6e4e95c4ee157b741abb4c73d10db421d24f3c6b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5236809
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1870}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [omnibox][calc][m120] Unlaunch on android
    
    m120 merge.
    
    Android calc suggestions have a bug, where they display the user's input
    instead of calc query.
    
    E.g., if the user types '1+1, then '1+2';
    Then desktop will display: '1+2 = 3' & '1+1 = 2';
    But android will display:  '1+2 \n = 3' & '1+2 \n = 2'.
    
    It's not trivial to switch from displaying the user input to displaying
    match contents on android because for some reason the match contents
    isn't piped to the android autocompletion code (for neither search nor
    calc provider calc matches).
    
    Perhaps when parsing search suggestions, there's some platform specific
    code? Or perhaps the search server response is differs slighty per
    platform? Android devs don't have time to dig into this at the moment,
    so we're instead unlaunching calc suggestions on android.
    
    Originally launched in 120.0.6099.0 with crrev.com/c/4930540 .
    
    (cherry picked from commit 897a2b965233faf75757809e9e1107c249b2d646)
    
    Bug: 1470347, 1518782, b/320563075
    Change-Id: I30262691f42d869e3791d69368e14ff8be8c6a5d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5207230
    Commit-Queue: manuk hovanesian <manukh@chromium.org>
    Reviewed-by: Tomasz Wiszkowski <ender@google.com>
    Auto-Submit: manuk hovanesian <manukh@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1249050}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5237012
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1871}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Ia7a426a4c01761717ffb9b14dda2b63e00987a9f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5236766
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1872}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [merge to 120] desks: Fix crash when tabbing library view while fading out
    
    This patch applies the same treatment to the library view that the
    desks bar got in CL:4912335. This would also apply it to other overview
    UI, that do not have a known crash, but could also use this treatment.
    
    (cherry picked from commit 45981be256d929b22ea1c55fdf5089f2475f000f)
    
    Test: manual
    Test: ash_unittests *TabbingDuringExitAnimation*
    Bug: b/302708219
    Change-Id: Ia96c0fba3a1d126c2bd8d8520d86e4a3f7f0cb79
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5078819
    Reviewed-by: Yongshun Liu <yongshun@chromium.org>
    Commit-Queue: Sammie Quon <sammiequon@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1232868}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5235902
    Cr-Commit-Position: refs/branch-heads/6099@{#1875}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Crash Fix for removing layer on shutdown
    
    The ripple_layer_ is removed during shutdown, but the layers parent
    is already unlinked, resulting in a UAF.
    
    The views::View dtor first recursively unlinks all parent layers via
    a call to views::View::OrphanLayers, then it deletes the view. This
    means that the assumption that layer()->parent() exists in
    TrayBackgroundView: :RemoveRippleLayer() is not valid when it is called
    in the TrayBackgroundView Dtor if the view is in the process of being
    removed via a call to views::View::RemoveAllChildViews().
    
    (cherry picked from commit 0a739afb0abed768dce74621a39ad0b5ab87930d)
    
    (cherry picked from commit dd6f1f7b361d11f81b020023c3863034739be3ac)
    
    Bug: b:317118003
    Change-Id: I5459989ac778fe927e8e287b5151ae25300c5143
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5166508
    Commit-Queue: Jon Mann <jonmann@chromium.org>
    Auto-Submit: Alex Newcomer <newcomer@chromium.org>
    Commit-Queue: Alex Newcomer <newcomer@chromium.org>
    Reviewed-by: Jon Mann <jonmann@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1242668}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5202135
    Reviewed-by: Ahmed Mehfooz <amehfooz@chromium.org>
    Commit-Queue: Ahmed Mehfooz <amehfooz@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6167@{#1439}
    Cr-Original-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5239154
    Cr-Commit-Position: refs/branch-heads/6099@{#1876}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.272
    
    [omnibox][calc][m120] Unlaunch on ios
    
    m120 merge.
    
    iOS calc suggestions don't display their query; they only display the
    answer.
    
    E.g., if the user types '1+1, then '1+2'; Then desktop will display:
    '1+2 = 3' & '1+1 = 2'; But iOS will display: '= 3' & ' = 2'.
    
    Originally launched in 120.0.6099.0 with crrev.com/c/4930540 .
    Unlaunched on android in m122 with crrev.com/c/5207230 .
    
    (cherry picked from commit 590d671aff9daad0085ab8bf9cf9186464e0328a)
    
    Bug: 1470347, 1518782, b/320563075
    Change-Id: I65933d50069a7bd06385109a9a399a7df657b69e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5218531
    Auto-Submit: manuk hovanesian <manukh@chromium.org>
    Commit-Queue: Justin Donnelly <jdonnelly@chromium.org>
    Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
    Commit-Queue: manuk hovanesian <manukh@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1249646}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5238426
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1878}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I8eb5d3851ac376f44a533b69c3c5b700d9ca803b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5238990
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1880}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.273
    120.0.6099.274
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I65dde475d6ae4f19ec765501e5483ed17b7601ca
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5243512
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1889}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Automated Commit: LKGM 15662.90.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8757694997572842305
    
    Change-Id: I056182b39cea8c31eb0fd225c86e838b4cc7a375
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5243557
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1891}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.275
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Ic4e800ba6fa5a458a3132870434b8a274cf6ad5e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5245045
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1894}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.276
    120.0.6099.277
    
    Roll src/clank in M120 from 19ba5fd69e3d to 787d88b447ee
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/19ba5fd69e3d..787d88b447ee
    
    Generated by: go/bbid/8757473357244128369
    
    Change-Id: I3c4ad297dda1d1b32598c513a7beb16be191b9eb
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5249547
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1899}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Disabled failing tests in PageInfoViewTest
    
    This CL disables the following tests:
    
    - testShowCookiesSubpageTrackingProtection
    - testShowCookiesSubpageTrackingProtectionBlockAll
    - testShowCookiesSubpageUserBypassOn
    
    (cherry picked from commit 5fa385eb73736be49719775f90140bf392d041eb)
    
    Bug: 1510968
    Change-Id: I0a9a46027ace63f7361ef992e96b4dee883e4238
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5117517
    Reviewed-by: Marlon Facey <mfacey@chromium.org>
    Commit-Queue: Salvador Guerrero Ramos <salg@google.com>
    Owners-Override: Salvador Guerrero Ramos <salg@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1236497}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5249748
    Commit-Queue: Joe Downing <joedow@chromium.org>
    Owners-Override: Joe Downing <joedow@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1902}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    6099: Move tests on internal chromeos-reven bot to jammy
    
    This was likely forgotten in the bionic->jammy migration earlier
    last year, and are the last things preventing the internal bionic
    test pool from switching 100% to jammy. This ought to be safe.
    
    This migrates both suites on this bot:
    https://ci.chromium.org/ui/p/chrome/builders/luci.chrome.ci/chromeos-reven-chrome
    
    (cherry picked from commit 2b69a5fbc9b7165116d2edca8c62fb20d3963089)
    
    Bug: 1412588
    Change-Id: Ic3a051551abb90fcfc68824841934289cb0b0e75
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5246127
    Commit-Queue: Ben Pastene <bpastene@chromium.org>
    Reviewed-by: Struan Shrimpton <sshrimp@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1253631}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5250870
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1903}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    6099: Move lacros's internal sizes tests to jammy
    
    (cherry picked from commit 443d785f57d6692b8f213d28b5180764e6f46b0e)
    
    Bug: 1412588
    Change-Id: I3ca94f8bc854f3e45ce5d35a5bd2421faa5ee262
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5250868
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Ben Pastene <bpastene@chromium.org>
    Auto-Submit: Ben Pastene <bpastene@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1254006}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5249537
    Cr-Commit-Position: refs/branch-heads/6099@{#1904}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120] ipcz: Fix a few weak asserts
    
    DriverMemory cloning should not weakly assert success, as it can fail in
    real production scenarios. Now Clone() will return an invalid
    DriverMemory object if it fails to duplicate the internal handle.
    Existing callers of Clone() are already durable to an invalid output, so
    this change results in graceful failures instead of undefined behavior.
    
    This also replaces some weak asserts in DriverTransport creation with
    hardening asserts. We may want to fail more gracefully if these end
    up crashing a lot, but it seems unlikely.
    
    (cherry picked from commit 4bd18c5a3a7a935716bbed197fba6d45a1122894)
    
    Fixed: 1521571
    Change-Id: Id764b33ead8bbba58e61b3270920c839479eaa4a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5240312
    Commit-Queue: Ken Rockot <rockot@google.com>
    Reviewed-by: Alex Gough <ajgo@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1252882}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5250958
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ken Rockot <rockot@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1905}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.278
    
    Roll src/ios_internal in M120 from 54e6940dde9c to 9cac2cd3eef6
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/ios_internal.git/+log/54e6940dde9c..9cac2cd3eef6
    
    Generated by: go/bbid/8757378983828949857
    
    Change-Id: I99b75134e5a7c696eaab6a2d5777bbd589bfdcd4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5250629
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1907}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I7100b3bd7abc5b61f7e7bae1cd0542143217d31e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5253537
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1910}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.279
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Ibdaca2baadd552af79cf7282f70b0e86be156315
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5255859
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1912}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Racy iterator use and crash on BMP image CP'd earlier to CfM-R120.
    
    120.0.6099.280
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Id28de4489a72580bfe99e276141a9faff217fb61
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5259188
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1918}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.281
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: If1b759da4e32c312b8d1f660e73311aae79d417f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5262809
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1922}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.282
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I7cdbfbd3d4b496683ac578bda248807640d7a8f4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5266478
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1925}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.283
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Ief819d1e33729d8141c3c826f5c00ab95e77b3bd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5268123
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1928}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.284
    
    Roll src/clank in M120 from 787d88b447ee to 672936694581
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/787d88b447ee..672936694581
    
    Generated by: go/bbid/8756841067020099745
    
    Change-Id: Ib3d941830cadff1aaf8a46bba5665d9f28a3395e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272462
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1931}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I89702cd7c5fb1f2b59266ae1abdd7fe4ff14cc0d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272463
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1932}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.285
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I9dcd9bd8a92ecf19b2a08dc2b7179da589e1e2f3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272155
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1934}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/internal in M120 from 79571debd475 to ceb6dcdc41aa
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/79571debd475..ceb6dcdc41aa
    
    Generated by: go/bbid/8756718382207782465
    
    Change-Id: Ib842812e05a48a4bcec5cecc73e9555fe3bbc4b8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5273827
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1935}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.286
    
    kiosk: Add a parent window to the diagnose dialog
    
    This is the diagnose dialog reachable from the network dialog during
    Kiosk launch. The dialog is currently broken, when you click "diagnose"
    nothing happens at the time. The dialog is actually created behind the
    splash screen, and sometimes is visible above the Kiosk app after
    launch.
    
    When in-session the dialog can be leveraged among other bugs to escape
    Kiosk.
    
    This change adds a parent window to the dialog, so it is displayed in
    the login screen correctly and gets closed when the login screen is gone
    after Kiosk launches.
    
      "diagnose", see the dialog appears, connect to internet, see the kiosk
      launches and the dialog disappears.
    
    (cherry picked from commit e40ada20757d3f59bf8046c654ceb0426bd310e1)
    
    Bug: b:322775376
    Test: manual - launch kiosk while offline, see the network dialog, click
    Change-Id: I802055a19b56b4fbe8bfd2e04dcf937eeac73e8f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5249069
    Reviewed-by: Ben Franz <bfranz@chromium.org>
    Reviewed-by: Denis Kuznetsov <antrim@chromium.org>
    Commit-Queue: Edman Anjos <edman@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1253921}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272410
    Cr-Commit-Position: refs/branch-heads/6099@{#1937}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [LTC-120] Disable all ash-level accelerators during the kiosk launch
    
    This fixes an issue where you can briefly use accelerators after the
    kiosk launch is started. This has been part of an exploit where users
    were able to use the SystemTrayBubble after the kiosk launch has started
    and perform subsequent actions.
    
    (cherry picked from commit 3e85561a0e38c43dfccd9ebda37444272a41f469)
    
    Bug: b/315762117
    Test: KioskLaunchControllerTest
    Change-Id: I1a311c2b9989c9f5e46e9400220e7d4a4e8588c0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5140206
    Reviewed-by: Jeroen Dhollander <jeroendh@google.com>
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1252578}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272829
    Cr-Commit-Position: refs/branch-heads/6099@{#1938}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Ic9d45e3664f83ca0b4c3e26d1e944f9c69853ff8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5274414
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1939}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/clank in M120 from 672936694581 to 68d7e5a40fb0
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/672936694581..68d7e5a40fb0
    
    Generated by: go/bbid/8756614570385526945
    
    Change-Id: I3c15d095fda67352028a1641c3fc82b58a88af31
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5281095
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1940}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.287
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I0959d88f7ac2ab5e5d9923bb865fd152bc10d836
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5281419
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1942}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120] kiosk: Close new browsers by closing tabs instead of window
    
    Currently we close new browsers with `browser->window()->Close()`. Turns
    out this can fail in certain conditions, e.g. if the user is currently
    dragging the window. This leads to the possibility that a new window
    does not get closed.
    
    This change uses `browser->tab_strip_model()->CloseAllTabs()` that seems
    to be more resilient and closes the browser window during drag events.
    
    Note this is a bandaid fix, the ideal solution is to prevent the window
    from opening on the first place, not to close it after the fact.
    
    This is behind the `kKioskCloseAllTabs` feature flag. Enable it with the
    `--enable-features=KioskCloseAllTabs` arg in /etc/chrome_dev.conf.
    
          and the window still closes during a drag.
    
    (cherry picked from commit e090938556780999db8cca6dfde8aab52b57300b)
    
    Bug: b:322954900
    Test: manual - do the steps in b/322775376, verify step 11 does not work
    Change-Id: Iae6beba499e66d7849551331bc10e55179051024
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5249989
    Commit-Queue: Edman Anjos <edman@chromium.org>
    Reviewed-by: Ben Franz <bfranz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1254484}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272320
    Commit-Queue: Jeroen Dhollander <jeroendh@google.com>
    Auto-Submit: Edman Anjos <edman@chromium.org>
    Reviewed-by: Jeroen Dhollander <jeroendh@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1943}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.288
    120.0.6099.289
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Iefb47982eb55c71df4dbad152dae22dee2f224b1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5284254
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1946}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.290
    
    [M120-LTC] Prevent SessionAbortedDialog dismissal via keyboard accelerator
    
    This dialog has no Cancel/Close button, but it can still
    be dismissed via keyboard accelerator. This CL fixes the
    exploit mentioned in the issue, but extra work might be required
    to fix this behavior at dialog framework level.
    
    (cherry picked from commit 7495fc4e18459d3110e2125f2804c4c33185eea7)
    
    Bug: b:315761861
    Change-Id: I15291f74f625a0759403bd73f208455e1e96d8d7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5126184
    Reviewed-by: Allen Bauer <kylixrd@chromium.org>
    Commit-Queue: Denis Kuznetsov <antrim@chromium.org>
    Auto-Submit: Denis Kuznetsov <antrim@chromium.org>
    Reviewed-by: Xiyuan Xia <xiyuan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1239090}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5272398
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1948}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120] kiosk: Clear kKioskCloseAllTabs feature
    
    (cherry picked from commit 98a855ef4f8b52d6883fb4084ee4ec5530d89b2c)
    
    Fixed: b:323129396
    Test: manual, and requested manual QA
    Change-Id: I27c6c6541b2321206f39e6852ec3535b5e6805aa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5257717
    Reviewed-by: Ben Franz <bfranz@chromium.org>
    Auto-Submit: Edman Anjos <edman@chromium.org>
    Commit-Queue: Edman Anjos <edman@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1257894}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5277127
    Reviewed-by: Roland Bock <rbock@google.com>
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1949}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/ios_internal in M120 from 9cac2cd3eef6 to 0f0760f5646b
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/ios_internal.git/+log/9cac2cd3eef6..0f0760f5646b
    
    Generated by: go/bbid/8756293708904915873
    
    Change-Id: Ibf0d3cdd94e631ff3ff8b18c69617d582b487b83
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5285994
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1950}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: If15521cfc53c6752467989a7c06148faab2568df
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5285835
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1951}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.291
    120.0.6099.292
    
    Roll src/clank in M120 from 68d7e5a40fb0 to f91ef213617a
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/68d7e5a40fb0..f91ef213617a
    
    Generated by: go/bbid/8756205001221757441
    
    Change-Id: Ib10166597fdbc435901a670d5c87ee017bd7ef19
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5291194
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1954}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.293
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I559dce366635d62a4157024043ab2077406e2b39
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5292777
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1956}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.294
    
    Roll src/internal in M120 from ceb6dcdc41aa to ada5f5df1eb0
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/ceb6dcdc41aa..ada5f5df1eb0
    
    Generated by: go/bbid/8756078542047255233
    
    Change-Id: I07801fa379490e881580a7f5a3450d152eaa443a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5296601
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1958}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.295
    
    Automated Commit: LKGM 15662.94.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8756092197071420145
    
    Change-Id: I052f8793bbe239def2e4fead7ed0fd5e91073662
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5299022
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1960}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: Iebb568552cfca24bda2f08504cf86e9ce81b6ac7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5300994
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1961}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.296
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I24771756249eac4c861a7c71452171596d8ac923
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5303514
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1963}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Consolidate expectations for headers.optional.html
    
    M120 Merge: Flaky on M120 Mac-11 or Mac-10.16
    
    This test fails or times out on Mac - this just unifies the
    expectations for all Mac platforms to avoid flakiness.
    
    (cherry picked from commit 56521d8d760ab4344929729c022d04fc33301fb4)
    
    Fixed: 1498528
    Bug: 1401590
    Change-Id: I47958fb279cc4372b929392815190c101e82faba
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5009840
    Auto-Submit: Mason Freed <masonf@chromium.org>
    Reviewed-by: David Baron <dbaron@chromium.org>
    Commit-Queue: Mason Freed <masonf@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1222389}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5304020
    Commit-Queue: Robert Liao <robliao@chromium.org>
    Owners-Override: Robert Liao <robliao@google.com>
    Reviewed-by: Mason Freed <masonf@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1964}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.297
    120.0.6099.298
    
    Updating XTBs based on .GRDs from branch 6099
    
    Change-Id: I65692a71bf3f59ef10329abe4e16d900f870e769
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5305655
    Auto-Submit: Ben Mason <benmason@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1967}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.299
    120.0.6099.300
    
    Roll src/clank in M120 from f91ef213617a to 06b33c8dd2b8
    Commits rolled:
    https://chrome-internal.googlesource.com/clank/internal/apps.git/+log/f91ef213617a..06b33c8dd2b8
    
    Generated by: go/bbid/8755570821173155489
    
    Change-Id: I9356f9c2d76d2e4afabe4548f340cb2dbbb58c60
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5309375
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1970}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [infra] Turn down unnecessary platforms.
    
    M120 is now shipping only cros for LTS and mac & win for extended
    stable.
    
    Change-Id: I5a097d717b85ee5814575f307622ced7a5dab88c
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5314282
    Commit-Queue: Garrett Beaty <gbeaty@google.com>
    Reviewed-by: Erik Staab <estaab@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1971}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll src/internal in M120 from ada5f5df1eb0 to 11c01c165385
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/ada5f5df1eb0..11c01c165385
    
    Generated by: go/bbid/8755457575135024977
    
    Change-Id: Ic9ac609ae45589f7ad34d1dd8338463f656d5450
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5314681
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1972}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    M120: [kiosk]: Close browser windows opened before the kiosk app launched
    
    Since https://crrev.com/c/5046569 all preexisting browser windows are
    closed when launching a ChromeApp in kiosk, and this CL extends this to
    all kiosk session types.
    
    Bug: b:315761322
    Tests: Manually deployed ChromeApp and PWA, with and without lacros
    Change-Id: I8dbb101bb7474a12ff14ff83fc88766caf0d75f2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5214989
    Commit-Queue: Jeroen Dhollander <jeroendh@google.com>
    Reviewed-by: Irina Fedorova <irfedorova@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1252594}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5307695
    Reviewed-by: Jeroen Dhollander <jeroendh@google.com>
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1973}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    M120: kiosk: Make closing browsers more realistic in unit-tests
    
    We add a tab to the browser window to make sure that CloseAllTabs
    actually executes the Close. This is done by creating a FakeBrowser
    object that owns the actual Browser object, adds the tab and listens to
    the close callback on the TestBrowserWindow. This is a more complete
    test, because previously we only checked that all tabs were being
    closed but not that the window was closed.
    
    Bug: b/325401325
    Test: kiosk_browser_session_unittest.cc
    Change-Id: I09935faa34bceee6f390e89ddaae22e8240dedd8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5295499
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Reviewed-by: Irina Fedorova <irfedorova@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1261518}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5307139
    Cr-Commit-Position: refs/branch-heads/6099@{#1974}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    M120: Reland "kiosk: Crash kiosk session if unable to close browser window"
    
    This is a reland of commit 753b156c6e00c0af03e6ca23fc3f1e8b17b3ba18
    
    Original change's description:
    > kiosk: Crash kiosk session if unable to close browser window
    >
    > If we find that an undesired browser window did not close as expected,
    > we crash the browser process. This will result in the kiosk session
    > restarting.
    >
    > Bug: b/325401325
    > Test: KioskBrowserSessionDeathTest
    > Change-Id: Ie59031e69c944bb649a8b318e8238f1316d01ff9
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5291238
    > Reviewed-by: Sergii Bykov <sbykov@google.com>
    > Commit-Queue: Irina Fedorova <irfedorova@google.com>
    > Reviewed-by: Irina Fedorova <irfedorova@google.com>
    > Cr-Commit-Position: refs/heads/main@{#1261556}
    
    Bug: b/325401325
    Change-Id: Ide8b6003df8a0659b136cea7a30e1fb86ffda4e3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5301389
    Reviewed-by: Ben Franz <bfranz@chromium.org>
    Commit-Queue: Irina Fedorova <irfedorova@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1262307}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5307795
    Reviewed-by: Irina Fedorova <irfedorova@google.com>
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1975}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    M120: kiosk: Fall back to browser->window()->Close() in case of no tabs
    
    In a previous CL we moved from browser->window()->Close() to
    browser->tab_strip_model()->CloseAllTabs() as the method to close
    unwanted browser windows. However, this can become a no-op if no tabs
    are present. So fall back to the old method for that case.
    
    Bug: b/325453088
    Test: kiosk_browser_session_unittest.cc
    Change-Id: I78384920ab860213c858af1d0cc01536179637a5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5301525
    Commit-Queue: Ben Franz <bfranz@chromium.org>
    Reviewed-by: Jeroen Dhollander <jeroendh@google.com>
    Reviewed-by: Irina Fedorova <irfedorova@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1262347}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5306916
    Reviewed-by: Roland Bock <rbock@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1976}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120-LTS] Disable per context gl texture cache due to MT devices
    
    This issue only reproduces on MT devices and only when oop-c is
    disabled. The suspicion here is the multiple contexts (virtual
    Angle contexts) result in egl dma reimport of the same buffer. It is
    known that there is an issue with doing this operation.[0] In
    noticing this bug I am also reenabling oop-c for lacros.[1]
    
    [0]
    https://bugs.chromium.org/p/chromium/issues/detail?id=1343521
    
    [1]
    https://chromium-review.googlesource.com/c/chromium/src/+/5013392
    
    (cherry picked from commit cbb1328067901809861e1e426fc09b82f444d8cb)
    
    Bug: 1498703
    Change-Id: I8003070ada4b8c83f3b8f6a823ef9b66d7aa1ba7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5013833
    Commit-Queue: Peter McNeeley <petermcneeley@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1222351}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5325917
    Owners-Override: Mohamed Omar <mohamedaomar@google.com>
    Reviewed-by: Peter McNeeley <petermcneeley@chromium.org>
    Commit-Queue: Zakhar Voit <voit@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1977}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    PageInfo: Disabled failing tests for M120
    
    The tests produce the wrong image because of some CL that was merged
    after branch point and skia gold does not support approving images on
    branches so we can only disable the test.
    
    Bug: 40076122
    Change-Id: Idd215165dd103cef0a153d48d677d92e870a4faf
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5331873
    Reviewed-by: Filipa Senra <fsenra@google.com>
    Auto-Submit: Christian Dullweber <dullweber@chromium.org>
    Commit-Queue: Filipa Senra <fsenra@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1978}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120] Corrected ShelfShutdownConfirmationBubble size
    
    ShelfShutdownConfirmationBubble modifies the size of ContentView after
    setting the size of BubbleDialog. However, the size of the widget is not
    modified synchronously at this time.
    
    (cherry picked from commit 110f091c1addd4421c062691eb457df039c3e420)
    
    Bug: b/321182074
    Change-Id: Iabfd488db07c6528e36cb476a75db534ddbd917b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5232971
    Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
    Reviewed-by: Mike Wasserman <msw@chromium.org>
    Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1252378}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5333694
    Auto-Submit: Keren Zhu <kerenzhu@chromium.org>
    Commit-Queue: Mike Wasserman <msw@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1979}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.301
    
    Automated Commit: LKGM 15662.97.0 for chromeos.
    
    Uploaded by https://ci.chromium.org/b/8754017286666155553
    
    Change-Id: I6cdf5c86650ff186ed8eea23a2a079cce597e638
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5357971
    Commit-Queue: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Bot-Commit: ChromeOS bot <3su6n15k.default@developer.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1981}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120][infra] Turn down mac and windows builders.
    
    Extended stable is over for M120, so mac and windows are no longer
    necessary.
    
    Change-Id: I2d2a94cfa7862aa4f683b818b23cff4954a06304
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5362716
    Commit-Queue: Garrett Beaty <gbeaty@google.com>
    Reviewed-by: Erik Staab <estaab@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1982}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll commits from side projects in M120
    
    Roll src/internal in M120 from 11c01c165385 to 159781054e72
    Commits rolled:
    https://chrome-internal.googlesource.com/chrome/src-internal.git/+log/11c01c165385..159781054e72
    
    Generated by: http://go/bbid/8753651298827578529
    
    Change-Id: I780e03c73d683e2e303189a90a6b9ffe2c9135e0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5367580
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1983}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll commits from side projects in M120
    
    Roll src/v8 in M120 from 71b6b5a68e08 to f1995520e2c3
    Commits rolled:
    https://chromium.googlesource.com/v8/v8.git/+log/71b6b5a68e08..f1995520e2c3
    
    Generated by: http://go/bbid/8753572025907594289
    
    Change-Id: Ifc6bf2c93bd94ac4a2979f7b414534529ec2d85b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5369173
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1984}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120-LTS] Stop running timers on ShutdownOnUiThread
    
    (cherry picked from commit c703c622fa8eb93f1a6b95b109c77a3c0a414683)
    
    Bug: 1515252
    Change-Id: I9fe9384c49b46d04f4ed1fa257cd9bae4c531f2d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5172685
    Commit-Queue: Florian Jacky <fjacky@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1243459}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5323665
    Owners-Override: Michael Ershov <miersh@google.com>
    Commit-Queue: Zakhar Voit <voit@google.com>
    Reviewed-by: Florian Jacky <fjacky@chromium.org>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1985}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    Roll commits from side projects in M120
    
    Roll src/v8 in M120 from f1995520e2c3 to cf616dbd25f2
    Commits rolled:
    https://chromium.googlesource.com/v8/v8.git/+log/f1995520e2c3..cf616dbd25f2
    
    Generated by: http://go/bbid/8753492753809636497
    
    Change-Id: I77de4366566af352c7556f968927fd08a4f394d6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5370452
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1986}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120-LTS] Introduce DeviceHardwareVideoDecodingEnabled device policy
    
    (cherry picked from commit 4d64f17bab69e728794639ffb7af07cd97f4171c)
    
    Bug: b:313418482, b:295536513
    Change-Id: I8945353bbdf775b62d2997ea819f222f6a89cffb
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5062792
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
    Commit-Queue: Jeroen Dhollander <jeroendh@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1231831}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5371923
    Auto-Submit: Jeroen Dhollander <jeroendh@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1987}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120-LTS][CSP] Hide nonce before merging attributes to html or body tags.
    
    See https://crbug.com/1513216
    
    (cherry picked from commit 62d76556fcf250ecb0f63874be8cdd3db51f2a64)
    
    Bug: 1513216
    Change-Id: I6dd69249ad35b53f77d7f1fec2662d4074b2cc01
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5149755
    Commit-Queue: Jonathan Hao <phao@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1240901}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5340567
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Reviewed-by: Jonathan Hao <phao@chromium.org>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Owners-Override: Michael Ershov <miersh@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1988}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120-LTS][Read Anything] Remove RenderFrame pointer from AXTreeDistiller
    
    Remove dangling RenderFrame pointer. Instead, pass in the RenderFrame
    from the app controller.
    
    (cherry picked from commit 2696ed29caedaa156153fceae404c4c4d983ef51)
    
    Bug: 1517513
    Change-Id: Ia206909e11c4357e308c3c34efe195cf20a7a1bf
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5193845
    Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1248178}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5343092
    Reviewed-by: Kristi Saney <kristislee@google.com>
    Reviewed-by: Michael Ershov <miersh@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1989}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.302
    
    Roll commits from side projects in M120
    
    Roll src/third_party/skia in M120 from 349c1179c43e to 009c7925d24c
    Commits rolled:
    https://skia.googlesource.com/skia.git/+log/349c1179c43e..009c7925d24c
    
    Generated by: http://go/bbid/8753069966918426689
    
    Change-Id: Ic25612a57315f2c10771a909866cba7b23861fd6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5379022
    Bot-Commit: Chrome Release Bot (LUCI) <chrome-official-brancher@chops-service-accounts.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1991}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    120.0.6099.303
    120.0.6099.304
    
    m120: mb: Prepare for the presence of the '--ide=json' arg to be configured
    
    This adds a "--write-ide-json" arg to all mb.py commands that run gen
    that will eventually control whether the "--ide=json" arg is passed to
    gn-gen. This arg can add up to 60s in gn-gen time, and most bots don't
    need it.
    
    So after this CL lands:
    - it will be cherry-picked to all branches with active bots on them
    - the bots that actually need it will pass the flag down to mb.py via
      their recipes (since it's only specific recipes that need it)
    - the commented-out condition here will be removed
    
    The final step should then speed-up gn-gen for most bots, including
    every bot on the cq.
    
    (cherry picked from commit 7dff072688ac0ee7922ae468b8c789f167c645d7)
    
    Bug: 330760869
    Change-Id: Ia18422821320963673f2521bd4ba8a2a5078d238
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5389549
    Reviewed-by: Garrett Beaty <gbeaty@google.com>
    Commit-Queue: Ben Pastene <bpastene@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1277968}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5399128
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#1995}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    
    [M120][infra] Set properties on orchestrators instead of compilators.
    
    The orchestrator recipe is going to be modified to propagate necessary
    properties on to the compilator so that the compilators do not need any
    properties configured (besides recipe). This limits the runtime
    configuration of the builder to just the orchestrator, which is the
    builder that is actually triggered and surfaced for CQ runs.
    
    (cherry picked from commit d6409d7f4f7c51a3675c729c4185fdfce81b9443)
    
    Bug: 327554081
    Change-Id: I0adca3e6155774b22423e34f83afe601711211c3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5370695
    Reviewed-by: Ben Pastene <bpastene@chromium.org>
    Commit-Queue: Garrett Beaty <gbeaty@google.com>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1278454}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5398580
    Cr-Original-Commit-Position: refs/branch-heads/6099@{#1996}
    Cr-Original-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5402058
    Commit-Queue: Xiyuan Xia <xiyuan@chromium.org>
    Owners-Override: Kyle Williams <kdgwill@chromium.org>
    Reviewed-by: Xiyuan Xia <xiyuan@chromium.org>
    Auto-Submit: Richard Yeh <rcy@google.com>
    Owners-Override: Richard Yeh <rcy@google.com>
    Reviewed-by: Kyle Williams <kdgwill@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099_225@{#20}
    Cr-Branched-From: 6d3cc0dac5057925e096b1329680124b19f35842-refs/branch-heads/6099@{#1762}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       DEPS
M       android_webview/browser/gfx/overlay_processor_webview.cc
M       ash/session/session_aborted_dialog.cc
M       ash/shelf/shelf_shutdown_confirmation_bubble.cc
M       ash/shortcut_viewer/strings/shortcut_viewer_strings_es.xtb
M       ash/shortcut_viewer/strings/shortcut_viewer_strings_id.xtb
M       ash/shortcut_viewer/strings/shortcut_viewer_strings_vi.xtb
M       ash/strings/ash_strings_af.xtb
M       ash/strings/ash_strings_ar.xtb
M       ash/strings/ash_strings_be.xtb
M       ash/strings/ash_strings_bg.xtb
M       ash/strings/ash_strings_de.xtb
M       ash/strings/ash_strings_el.xtb
M       ash/strings/ash_strings_en-GB.xtb
M       ash/strings/ash_strings_es-419.xtb
M       ash/strings/ash_strings_es.xtb
M       ash/strings/ash_strings_fa.xtb
M       ash/strings/ash_strings_fi.xtb
M       ash/strings/ash_strings_fr-CA.xtb
M       ash/strings/ash_strings_fr.xtb
M       ash/strings/ash_strings_gl.xtb
M       ash/strings/ash_strings_hr.xtb
M       ash/strings/ash_strings_hy.xtb
M       ash/strings/ash_strings_id.xtb
M       ash/strings/ash_strings_is.xtb
M       ash/strings/ash_strings_it.xtb
M       ash/strings/ash_strings_ja.xtb
M       ash/strings/ash_strings_kk.xtb
M       ash/strings/ash_strings_km.xtb
M       ash/strings/ash_strings_kn.xtb
M       ash/strings/ash_strings_ko.xtb
M       ash/strings/ash_strings_lt.xtb
M       ash/strings/ash_strings_lv.xtb
M       ash/strings/ash_strings_mk.xtb
M       ash/strings/ash_strings_mr.xtb
M       ash/strings/ash_strings_ms.xtb
M       ash/strings/ash_strings_nl.xtb
M       ash/strings/ash_strings_or.xtb
M       ash/strings/ash_strings_pl.xtb
M       ash/strings/ash_strings_pt-BR.xtb
M       ash/strings/ash_strings_ro.xtb
M       ash/strings/ash_strings_ru.xtb
M       ash/strings/ash_strings_sl.xtb
M       ash/strings/ash_strings_sr-Latn.xtb
M       ash/strings/ash_strings_sr.xtb
M       ash/strings/ash_strings_sw.xtb
M       ash/strings/ash_strings_th.xtb
M       ash/strings/ash_strings_uk.xtb
M       ash/strings/ash_strings_vi.xtb
M       ash/strings/ash_strings_zh-CN.xtb
M       ash/strings/ash_strings_zh-HK.xtb
M       ash/system/tray/tray_background_view.cc
M       ash/webui/camera_app_ui/resources/strings/camera_strings_kn.xtb
M       ash/webui/camera_app_ui/resources/strings/camera_strings_pt-BR.xtb
M       ash/webui/camera_app_ui/resources/strings/camera_strings_vi.xtb
M       ash/wm/desks/desk_mini_view_animations.cc
M       ash/wm/desks/templates/saved_desk_unittest.cc
M       ash/wm/overview/overview_utils.cc
M       ash/wm/overview/overview_utils.h
M       chrome/LACROS_QA_QUALIFIED_VERSION
M       chrome/android/javatests/src/org/chromium/chrome/browser/page_info/PageInfoViewTest.java
M       chrome/android/profiles/newest.txt
M       chrome/android/webapk/strings/translations/android_webapk_strings_ar.xtb
M       chrome/android/webapk/strings/translations/android_webapk_strings_ru.xtb
M       chrome/android/webapk/strings/translations/android_webapk_strings_vi.xtb
M       chrome/app/resources/chromium_strings_bs.xtb
M       chrome/app/resources/chromium_strings_de.xtb
M       chrome/app/resources/chromium_strings_fi.xtb
M       chrome/app/resources/chromium_strings_hr.xtb
M       chrome/app/resources/chromium_strings_it.xtb
M       chrome/app/resources/chromium_strings_or.xtb
M       chrome/app/resources/chromium_strings_pt-BR.xtb
M       chrome/app/resources/chromium_strings_ru.xtb
M       chrome/app/resources/generated_resources_af.xtb
M       chrome/app/resources/generated_resources_ar.xtb
M       chrome/app/resources/generated_resources_be.xtb
M       chrome/app/resources/generated_resources_bg.xtb
M       chrome/app/resources/generated_resources_ca.xtb
M       chrome/app/resources/generated_resources_da.xtb
M       chrome/app/resources/generated_resources_de.xtb
M       chrome/app/resources/generated_resources_el.xtb
M       chrome/app/resources/generated_resources_en-GB.xtb
M       chrome/app/resources/generated_resources_es-419.xtb
M       chrome/app/resources/generated_resources_es.xtb
M       chrome/app/resources/generated_resources_et.xtb
M       chrome/app/resources/generated_resources_eu.xtb
M       chrome/app/resources/generated_resources_fa.xtb
M       chrome/app/resources/generated_resources_fi.xtb
M       chrome/app/resources/generated_resources_fr-CA.xtb
M       chrome/app/resources/generated_resources_fr.xtb
M       chrome/app/resources/generated_resources_gl.xtb
M       chrome/app/resources/generated_resources_hi.xtb
M       chrome/app/resources/generated_resources_hr.xtb
M       chrome/app/resources/generated_resources_hu.xtb
M       chrome/app/resources/generated_resources_hy.xtb
M       chrome/app/resources/generated_resources_id.xtb
M       chrome/app/resources/generated_resources_is.xtb
M       chrome/app/resources/generated_resources_it.xtb
M       chrome/app/resources/generated_resources_iw.xtb
M       chrome/app/resources/generated_resources_ja.xtb
M       chrome/app/resources/generated_resources_km.xtb
M       chrome/app/resources/generated_resources_kn.xtb
M       chrome/app/resources/generated_resources_ko.xtb
M       chrome/app/resources/generated_resources_ky.xtb
M       chrome/app/resources/generated_resources_lt.xtb
M       chrome/app/resources/generated_resources_lv.xtb
M       chrome/app/resources/generated_resources_mk.xtb
M       chrome/app/resources/generated_resources_mr.xtb
M       chrome/app/resources/generated_resources_ms.xtb
M       chrome/app/resources/generated_resources_my.xtb
M       chrome/app/resources/generated_resources_ne.xtb
M       chrome/app/resources/generated_resources_nl.xtb
M       chrome/app/resources/generated_resources_no.xtb
M       chrome/app/resources/generated_resources_or.xtb
M       chrome/app/resources/generated_resources_pa.xtb
M       chrome/app/resources/generated_resources_pl.xtb
M       chrome/app/resources/generated_resources_pt-BR.xtb
M       chrome/app/resources/generated_resources_pt-PT.xtb
M       chrome/app/resources/generated_resources_ro.xtb
M       chrome/app/resources/generated_resources_ru.xtb
M       chrome/app/resources/generated_resources_sk.xtb
M       chrome/app/resources/generated_resources_sl.xtb
M       chrome/app/resources/generated_resources_sq.xtb
M       chrome/app/resources/generated_resources_sr-Latn.xtb
M       chrome/app/resources/generated_resources_sr.xtb
M       chrome/app/resources/generated_resources_sv.xtb
M       chrome/app/resources/generated_resources_sw.xtb
M       chrome/app/resources/generated_resources_th.xtb
M       chrome/app/resources/generated_resources_tr.xtb
M       chrome/app/resources/generated_resources_uk.xtb
M       chrome/app/resources/generated_resources_vi.xtb
M       chrome/app/resources/generated_resources_zh-CN.xtb
M       chrome/app/resources/generated_resources_zh-HK.xtb
M       chrome/app/resources/generated_resources_zh-TW.xtb
M       chrome/app/resources/google_chrome_strings_af.xtb
M       chrome/app/resources/google_chrome_strings_am.xtb
M       chrome/app/resources/google_chrome_strings_ar.xtb
M       chrome/app/resources/google_chrome_strings_be.xtb
M       chrome/app/resources/google_chrome_strings_bg.xtb
M       chrome/app/resources/google_chrome_strings_bs.xtb
M       chrome/app/resources/google_chrome_strings_ca.xtb
M       chrome/app/resources/google_chrome_strings_de.xtb
M       chrome/app/resources/google_chrome_strings_el.xtb
M       chrome/app/resources/google_chrome_strings_en-GB.xtb
M       chrome/app/resources/google_chrome_strings_es.xtb
M       chrome/app/resources/google_chrome_strings_et.xtb
M       chrome/app/resources/google_chrome_strings_eu.xtb
M       chrome/app/resources/google_chrome_strings_fa.xtb
M       chrome/app/resources/google_chrome_strings_fi.xtb
M       chrome/app/resources/google_chrome_strings_fr-CA.xtb
M       chrome/app/resources/google_chrome_strings_fr.xtb
M       chrome/app/resources/google_chrome_strings_gl.xtb
M       chrome/app/resources/google_chrome_strings_hr.xtb
M       chrome/app/resources/google_chrome_strings_id.xtb
M       chrome/app/resources/google_chrome_strings_is.xtb
M       chrome/app/resources/google_chrome_strings_it.xtb
M       chrome/app/resources/google_chrome_strings_ja.xtb
M       chrome/app/resources/google_chrome_strings_ky.xtb
M       chrome/app/resources/google_chrome_strings_lt.xtb
M       chrome/app/resources/google_chrome_strings_lv.xtb
M       chrome/app/resources/google_chrome_strings_mk.xtb
M       chrome/app/resources/google_chrome_strings_ms.xtb
M       chrome/app/resources/google_chrome_strings_nl.xtb
M       chrome/app/resources/google_chrome_strings_or.xtb
M       chrome/app/resources/google_chrome_strings_pl.xtb
M       chrome/app/resources/google_chrome_strings_pt-BR.xtb
M       chrome/app/resources/google_chrome_strings_ro.xtb
M       chrome/app/resources/google_chrome_strings_ru.xtb
M       chrome/app/resources/google_chrome_strings_sk.xtb
M       chrome/app/resources/google_chrome_strings_sl.xtb
M       chrome/app/resources/google_chrome_strings_sr-Latn.xtb
M       chrome/app/resources/google_chrome_strings_sr.xtb
M       chrome/app/resources/google_chrome_strings_sv.xtb
M       chrome/app/resources/google_chrome_strings_sw.xtb
M       chrome/app/resources/google_chrome_strings_th.xtb
M       chrome/app/resources/google_chrome_strings_tr.xtb
M       chrome/app/resources/google_chrome_strings_uk.xtb
M       chrome/app/resources/google_chrome_strings_vi.xtb
M       chrome/app/resources/google_chrome_strings_zh-CN.xtb
M       chrome/app/resources/google_chrome_strings_zh-HK.xtb
M       chrome/app/resources/google_chrome_strings_zh-TW.xtb
M       chrome/browser/ash/login/app_mode/kiosk_launch_controller.cc
M       chrome/browser/ash/login/app_mode/kiosk_launch_controller.h
M       chrome/browser/ash/login/app_mode/kiosk_launch_controller_unittest.cc
M       chrome/browser/ash/login/screens/error_screen.cc
M       chrome/browser/ash/policy/core/device_policy_decoder.cc
M       chrome/browser/chromeos/app_mode/kiosk_browser_session_unittest.cc
M       chrome/browser/chromeos/app_mode/kiosk_browser_window_handler.cc
M       chrome/browser/chromeos/app_mode/kiosk_browser_window_handler.h
M       chrome/browser/content_settings/host_content_settings_map_unittest.cc
M       chrome/browser/lacros/app_mode/kiosk_accelerator_browsertest.cc
M       chrome/browser/password_check/android/internal/java/strings/translations/android_password_check_strings_vi.xtb
M       chrome/browser/readaloud/android/resources/translations/android_readaloud_strings_gl.xtb
M       chrome/browser/recent_tabs/internal/android/java/strings/translations/android_restore_tabs_strings_fa.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_fa.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_is.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_it.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_km.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_ky.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_my.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_ne.xtb
M       chrome/browser/resources/chromeos/accessibility/strings/accessibility_strings_sv.xtb
M       chrome/browser/tpcd/experiment/BUILD.gn
M       chrome/browser/tpcd/experiment/experiment_manager_impl.cc
M       chrome/browser/tpcd/experiment/experiment_manager_impl_unittest.cc
M       chrome/browser/ui/android/fast_checkout/internal/java/strings/translations/android_fast_checkout_strings_fa.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ar.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_be.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ca.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_da.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_de.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_en-GB.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_es-419.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_es.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_et.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_fa.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_fr-CA.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_fr.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_gl.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_hi.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_hr.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_id.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_it.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ja.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_kn.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ko.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_mk.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_mr.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ms.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_nl.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_or.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_pl.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_pt-BR.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_pt-PT.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ro.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_ru.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_sv.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_th.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_tr.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_vi.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_zh-CN.xtb
M       chrome/browser/ui/android/strings/translations/android_chrome_strings_zh-TW.xtb
M       chrome/browser/ui/views/page_info/page_info_bubble_view_dialog_browsertest.cc
M       chrome/browser/ui/webui/ash/connectivity_diagnostics_dialog.cc
M       chrome/browser/ui/webui/ash/connectivity_diagnostics_dialog.h
M       chrome/renderer/accessibility/ax_tree_distiller.cc
M       chrome/renderer/accessibility/ax_tree_distiller.h
M       chrome/renderer/accessibility/ax_tree_distiller_browsertest.cc
M       chrome/renderer/accessibility/read_anything_app_controller.cc
M       chrome/renderer/accessibility/read_anything_app_controller_browsertest.cc
M       chrome/test/base/test_browser_window.cc
M       chrome/test/base/test_browser_window.h
M       chrome/test/data/webui/settings/chromeos/os_settings_browsertest.js
M       chromeos/CHROMEOS_LKGM
M       chromeos/profiles/arm-exp.afdo.newest.txt
M       chromeos/profiles/arm.afdo.newest.txt
M       chromeos/profiles/atom.afdo.newest.txt
M       chromeos/profiles/bigcore.afdo.newest.txt
M       chromeos/strings/chromeos_strings_ar.xtb
M       chromeos/strings/chromeos_strings_bs.xtb
M       chromeos/strings/chromeos_strings_da.xtb
M       chromeos/strings/chromeos_strings_de.xtb
M       chromeos/strings/chromeos_strings_es.xtb
M       chromeos/strings/chromeos_strings_fa.xtb
M       chromeos/strings/chromeos_strings_fr.xtb
M       chromeos/strings/chromeos_strings_is.xtb
M       chromeos/strings/chromeos_strings_it.xtb
M       chromeos/strings/chromeos_strings_ja.xtb
M       chromeos/strings/chromeos_strings_kk.xtb
M       chromeos/strings/chromeos_strings_km.xtb
M       chromeos/strings/chromeos_strings_kn.xtb
M       chromeos/strings/chromeos_strings_ky.xtb
M       chromeos/strings/chromeos_strings_lv.xtb
M       chromeos/strings/chromeos_strings_mr.xtb
M       chromeos/strings/chromeos_strings_no.xtb
M       chromeos/strings/chromeos_strings_or.xtb
M       chromeos/strings/chromeos_strings_pt-BR.xtb
M       chromeos/strings/chromeos_strings_ru.xtb
M       chromeos/strings/chromeos_strings_sv.xtb
M       chromeos/strings/chromeos_strings_uk.xtb
M       chromeos/strings/chromeos_strings_vi.xtb
M       clank
M       components/browser_ui/strings/android/translations/browser_ui_strings_ar.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_ca.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_da.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_de.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_en-GB.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_es-419.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_es.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_et.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_fa.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_fr-CA.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_fr.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_hi.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_it.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_iw.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_ja.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_kn.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_ko.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_or.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_pl.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_pt-BR.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_ru.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_sv.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_th.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_vi.xtb
M       components/browser_ui/strings/android/translations/browser_ui_strings_zh-CN.xtb
M       components/content_settings/core/browser/host_content_settings_map.cc
M       components/embedder_support/android/java/strings/translations/web_contents_delegate_android_strings_vi.xtb
M       components/omnibox/browser/omnibox_feature_configs.cc
M       components/omnibox/resources/translations/omnibox_pedal_synonyms_ms.xtb
M       components/policy/proto/chrome_device_policy.proto
M       components/policy/resources/policy_templates_de.xtb
M       components/policy/resources/policy_templates_fr.xtb
M       components/policy/resources/policy_templates_id.xtb
M       components/policy/resources/policy_templates_it.xtb
M       components/policy/resources/policy_templates_pt-BR.xtb
M       components/policy/resources/policy_templates_vi.xtb
M       components/policy/resources/policy_templates_zh-TW.xtb
M       components/policy/resources/templates/device_policy_proto_map.yaml
M       components/policy/resources/templates/policies.yaml
A       components/policy/resources/templates/policy_definitions/Miscellaneous/DeviceHardwareVideoDecodingEnabled.yaml
M       components/policy/test/data/policy_test_cases.json
A       components/policy/test/data/pref_mapping/DeviceHardwareVideoDecodingEnabled.json
M       components/strings/components_strings_ar.xtb
M       components/strings/components_strings_ca.xtb
M       components/strings/components_strings_da.xtb
M       components/strings/components_strings_de.xtb
M       components/strings/components_strings_en-GB.xtb
M       components/strings/components_strings_es-419.xtb
M       components/strings/components_strings_es.xtb
M       components/strings/components_strings_eu.xtb
M       components/strings/components_strings_fa.xtb
M       components/strings/components_strings_fr-CA.xtb
M       components/strings/components_strings_fr.xtb
M       components/strings/components_strings_gl.xtb
M       components/strings/components_strings_hi.xtb
M       components/strings/components_strings_hr.xtb
M       components/strings/components_strings_it.xtb
M       components/strings/components_strings_iw.xtb
M       components/strings/components_strings_ja.xtb
M       components/strings/components_strings_kn.xtb
M       components/strings/components_strings_ko.xtb
M       components/strings/components_strings_mr.xtb
M       components/strings/components_strings_ms.xtb
M       components/strings/components_strings_nl.xtb
M       components/strings/components_strings_or.xtb
M       components/strings/components_strings_pl.xtb
M       components/strings/components_strings_pt-BR.xtb
M       components/strings/components_strings_pt-PT.xtb
M       components/strings/components_strings_ru.xtb
M       components/strings/components_strings_sk.xtb
M       components/strings/components_strings_sl.xtb
M       components/strings/components_strings_sq.xtb
M       components/strings/components_strings_sv.xtb
M       components/strings/components_strings_th.xtb
M       components/strings/components_strings_tr.xtb
M       components/strings/components_strings_uk.xtb
M       components/strings/components_strings_vi.xtb
M       components/strings/components_strings_zh-CN.xtb
M       components/strings/components_strings_zh-TW.xtb
M       gpu/config/gpu_finch_features.cc
D       infra/config/generated/builders/ci/Android FYI Release (Pixel 6)/properties.json
D       infra/config/generated/builders/ci/Android Release (Nexus 5X)/properties.json
D       infra/config/generated/builders/ci/Android Release (Nexus 5X)/shadow-properties.json
D       infra/config/generated/builders/ci/Android WebView O (dbg)/properties.json
D       infra/config/generated/builders/ci/Android WebView P (dbg)/properties.json
D       infra/config/generated/builders/ci/Android arm Builder (dbg)/properties.json
D       infra/config/generated/builders/ci/Android arm Builder (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Android arm64 Builder (dbg)/properties.json
D       infra/config/generated/builders/ci/Android arm64 Builder (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Android arm64 Builder All Targets (dbg)/properties.json
D       infra/config/generated/builders/ci/Android arm64 Builder All Targets (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Android x64 Builder All Targets (dbg)/properties.json
D       infra/config/generated/builders/ci/Android x64 Builder All Targets (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Android x86 Builder (dbg)/properties.json
D       infra/config/generated/builders/ci/Android x86 Builder (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Cast Android (dbg)/properties.json
D       infra/config/generated/builders/ci/Cast Android (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Cast Linux Debug/properties.json
D       infra/config/generated/builders/ci/Cast Linux Debug/shadow-properties.json
D       infra/config/generated/builders/ci/Cast Linux/properties.json
D       infra/config/generated/builders/ci/Cast Linux/shadow-properties.json
D       infra/config/generated/builders/ci/Dawn Linux x64 DEPS Builder/properties.json
D       infra/config/generated/builders/ci/Dawn Linux x64 DEPS Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Dawn Linux x64 DEPS Release (Intel UHD 630)/properties.json
D       infra/config/generated/builders/ci/Dawn Linux x64 DEPS Release (NVIDIA)/properties.json
D       infra/config/generated/builders/ci/Dawn Mac x64 DEPS Builder/properties.json
D       infra/config/generated/builders/ci/Dawn Mac x64 DEPS Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Dawn Mac x64 DEPS Release (AMD)/properties.json
D       infra/config/generated/builders/ci/Dawn Mac x64 DEPS Release (Intel)/properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x64 DEPS Builder/properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x64 DEPS Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x64 DEPS Release (Intel)/properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x64 DEPS Release (NVIDIA)/properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x86 DEPS Builder/properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x86 DEPS Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x86 DEPS Release (Intel)/properties.json
D       infra/config/generated/builders/ci/Dawn Win10 x86 DEPS Release (NVIDIA)/properties.json
D       infra/config/generated/builders/ci/GPU FYI Android arm64 Builder/properties.json
D       infra/config/generated/builders/ci/GPU FYI Android arm64 Builder/shadow-properties.json
D       infra/config/generated/builders/ci/GPU Linux Builder/properties.json
D       infra/config/generated/builders/ci/GPU Linux Builder/shadow-properties.json
D       infra/config/generated/builders/ci/GPU Mac Builder/properties.json
D       infra/config/generated/builders/ci/GPU Mac Builder/shadow-properties.json
D       infra/config/generated/builders/ci/GPU Win x64 Builder/properties.json
D       infra/config/generated/builders/ci/GPU Win x64 Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Linux ASan LSan Builder/properties.json
D       infra/config/generated/builders/ci/Linux ASan LSan Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Linux ASan LSan Tests (1)/properties.json
D       infra/config/generated/builders/ci/Linux Builder (Wayland)/properties.json
D       infra/config/generated/builders/ci/Linux Builder (Wayland)/shadow-properties.json
D       infra/config/generated/builders/ci/Linux Builder (dbg)/properties.json
D       infra/config/generated/builders/ci/Linux Builder (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Linux Builder/properties.json
D       infra/config/generated/builders/ci/Linux Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Linux Release (NVIDIA)/properties.json
D       infra/config/generated/builders/ci/Linux TSan Builder/properties.json
D       infra/config/generated/builders/ci/Linux TSan Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Linux TSan Tests/properties.json
D       infra/config/generated/builders/ci/Linux TSan Tests/shadow-properties.json
D       infra/config/generated/builders/ci/Linux Tests (Wayland)/properties.json
D       infra/config/generated/builders/ci/Linux Tests (dbg)(1)/properties.json
D       infra/config/generated/builders/ci/Linux Tests/properties.json
D       infra/config/generated/builders/ci/Mac Builder (dbg)/properties.json
D       infra/config/generated/builders/ci/Mac Builder (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Mac Builder/properties.json
D       infra/config/generated/builders/ci/Mac Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Mac Release (Intel)/properties.json
D       infra/config/generated/builders/ci/Mac Retina Release (AMD)/properties.json
D       infra/config/generated/builders/ci/Mac10.15 Tests/properties.json
D       infra/config/generated/builders/ci/Mac11 Tests/properties.json
D       infra/config/generated/builders/ci/Mac12 Tests/properties.json
D       infra/config/generated/builders/ci/Mac13 Tests (dbg)/properties.json
D       infra/config/generated/builders/ci/Mac13 Tests/properties.json
D       infra/config/generated/builders/ci/Oreo Phone Tester/properties.json
D       infra/config/generated/builders/ci/Win Builder (dbg)/properties.json
D       infra/config/generated/builders/ci/Win Builder (dbg)/shadow-properties.json
D       infra/config/generated/builders/ci/Win Builder/properties.json
D       infra/config/generated/builders/ci/Win Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Win x64 Builder/properties.json
D       infra/config/generated/builders/ci/Win x64 Builder/shadow-properties.json
D       infra/config/generated/builders/ci/Win10 Tests x64/properties.json
D       infra/config/generated/builders/ci/Win10 Tests x64/shadow-properties.json
D       infra/config/generated/builders/ci/Win10 x64 Release (NVIDIA)/properties.json
D       infra/config/generated/builders/ci/android-12-x64-rel/properties.json
D       infra/config/generated/builders/ci/android-12-x64-rel/shadow-properties.json
D       infra/config/generated/builders/ci/android-cronet-arm-dbg/properties.json
D       infra/config/generated/builders/ci/android-cronet-arm-dbg/shadow-properties.json
D       infra/config/generated/builders/ci/android-cronet-arm-rel/properties.json
D       infra/config/generated/builders/ci/android-cronet-arm-rel/shadow-properties.json
D       infra/config/generated/builders/ci/android-cronet-mainline-clang-x86-dbg/properties.json
D       infra/config/generated/builders/ci/android-cronet-mainline-clang-x86-dbg/shadow-properties.json
D       infra/config/generated/builders/ci/android-cronet-x64-dbg/properties.json
D       infra/config/generated/builders/ci/android-cronet-x64-dbg/shadow-properties.json
D       infra/config/generated/builders/ci/android-cronet-x86-dbg-10-tests/properties.json
D       infra/config/generated/builders/ci/android-cronet-x86-dbg/properties.json
D       infra/config/generated/builders/ci/android-cronet-x86-dbg/shadow-properties.json
D       infra/config/generated/builders/ci/android-official/properties.json
D       infra/config/generated/builders/ci/android-official/shadow-properties.json
D       infra/config/generated/builders/ci/android-oreo-x86-rel/properties.json
D       infra/config/generated/builders/ci/android-oreo-x86-rel/shadow-properties.json
D       infra/config/generated/builders/ci/android-pie-arm64-dbg/properties.json
D       infra/config/generated/builders/ci/android-pie-arm64-rel/properties.json
D       infra/config/generated/builders/ci/android-pie-arm64-rel/shadow-properties.json
D       infra/config/generated/builders/ci/chromeos-amd64-generic-dbg/properties.json
D       infra/config/generated/builders/ci/chromeos-amd64-generic-dbg/shadow-properties.json
D       infra/config/generated/builders/ci/chromeos-amd64-generic-lacros-dbg/properties.json
D       infra/config/generated/builders/ci/chromeos-amd64-generic-lacros-dbg/shadow-properties.json
M       infra/config/generated/builders/ci/chromeos-amd64-generic-rel-gtest/properties.json
M       infra/config/generated/builders/ci/chromeos-amd64-generic-rel-renamed/properties.json
M       infra/config/generated/builders/ci/chromeos-amd64-generic-rel/properties.json
M       infra/config/generated/builders/ci/chromeos-arm-generic-rel/properties.json
M       infra/config/generated/builders/ci/chromeos-arm64-generic-rel/properties.json
M       infra/config/generated/builders/ci/chromeos-jacuzzi-rel/properties.json
M       infra/config/generated/builders/ci/chromeos-octopus-rel/properties.json
D       infra/config/generated/builders/ci/fuchsia-arm64-cast-receiver-rel/properties.json
D       infra/config/generated/builders/ci/fuchsia-arm64-cast-receiver-rel/shadow-properties.json
D       infra/config/generated/builders/ci/fuchsia-arm64-rel/properties.json
D       infra/config/generated/builders/ci/fuchsia-arm64-rel/shadow-properties.json
D       infra/config/generated/builders/ci/fuchsia-official/properties.json
D       infra/config/generated/builders/ci/fuchsia-official/shadow-properties.json
D       infra/config/generated/builders/ci/fuchsia-x64-cast-receiver-rel/properties.json
D       infra/config/generated/builders/ci/fuchsia-x64-cast-receiver-rel/shadow-properties.json
D       infra/config/generated/builders/ci/fuchsia-x64-rel/properties.json
D       infra/config/generated/builders/ci/fuchsia-x64-rel/shadow-properties.json
D       infra/config/generated/builders/ci/ios-simulator-cronet/properties.json
D       infra/config/generated/builders/ci/ios-simulator-cronet/shadow-properties.json
D       infra/config/generated/builders/ci/ios-simulator-full-configs/properties.json
D       infra/config/generated/builders/ci/ios-simulator-full-configs/shadow-properties.json
D       infra/config/generated/builders/ci/ios-simulator/properties.json
D       infra/config/generated/builders/ci/ios-simulator/shadow-properties.json
D       infra/config/generated/builders/ci/lacros-amd64-generic-rel-non-skylab/properties.json
D       infra/config/generated/builders/ci/lacros-amd64-generic-rel-non-skylab/shadow-properties.json
D       infra/config/generated/builders/ci/lacros-amd64-generic-rel/properties.json
D       infra/config/generated/builders/ci/lacros-amd64-generic-rel/shadow-properties.json
D       infra/config/generated/builders/ci/lacros-arm-generic-rel-skylab/properties.json
D       infra/config/generated/builders/ci/lacros-arm-generic-rel-skylab/shadow-properties.json
D       infra/config/generated/builders/ci/lacros-arm-generic-rel/properties.json
D       infra/config/generated/builders/ci/lacros-arm-generic-rel/shadow-properties.json
D       infra/config/generated/builders/ci/lacros-arm64-generic-rel-skylab/properties.json
D       infra/config/generated/builders/ci/lacros-arm64-generic-rel-skylab/shadow-properties.json
D       infra/config/generated/builders/ci/lacros-arm64-generic-rel/properties.json
D       infra/config/generated/builders/ci/lacros-arm64-generic-rel/shadow-properties.json
D       infra/config/generated/builders/ci/linux-chromeos-dbg/properties.json
D       infra/config/generated/builders/ci/linux-chromeos-dbg/shadow-properties.json
M       infra/config/generated/builders/ci/linux-chromeos-rel/properties.json
D       infra/config/generated/builders/ci/linux-lacros-builder-rel/properties.json
D       infra/config/generated/builders/ci/linux-lacros-builder-rel/shadow-properties.json
D       infra/config/generated/builders/ci/linux-lacros-dbg/properties.json
D       infra/config/generated/builders/ci/linux-lacros-dbg/shadow-properties.json
D       infra/config/generated/builders/ci/linux-lacros-tester-rel/properties.json
D       infra/config/generated/builders/ci/linux-official/gn-args.json
D       infra/config/generated/builders/ci/linux-official/properties.json
D       infra/config/generated/builders/ci/linux-official/shadow-properties.json
D       infra/config/generated/builders/ci/mac-arm64-rel/properties.json
D       infra/config/generated/builders/ci/mac-arm64-rel/shadow-properties.json
D       infra/config/generated/builders/ci/mac-official/properties.json
D       infra/config/generated/builders/ci/mac-official/shadow-properties.json
D       infra/config/generated/builders/ci/mac11-arm64-rel-tests/properties.json
D       infra/config/generated/builders/ci/mac12-arm64-rel-tests/properties.json
D       infra/config/generated/builders/ci/mac13-arm64-rel-tests/properties.json
D       infra/config/generated/builders/ci/win-official/properties.json
D       infra/config/generated/builders/ci/win-official/shadow-properties.json
D       infra/config/generated/builders/ci/win32-official/properties.json
D       infra/config/generated/builders/ci/win32-official/shadow-properties.json
M       infra/config/generated/builders/gn_args_locations.json
D       infra/config/generated/builders/try/android-12-x64-rel-compilator/properties.json
D       infra/config/generated/builders/try/android-12-x64-rel/properties.json
D       infra/config/generated/builders/try/android-arm-compile-dbg/properties.json
D       infra/config/generated/builders/try/android-arm64-rel-compilator/properties.json
D       infra/config/generated/builders/try/android-arm64-rel/properties.json
D       infra/config/generated/builders/try/android-cronet-arm-dbg/properties.json
D       infra/config/generated/builders/try/android-cronet-mainline-clang-x86-dbg/properties.json
D       infra/config/generated/builders/try/android-cronet-x64-dbg/properties.json
D       infra/config/generated/builders/try/android-cronet-x86-dbg-10-tests/properties.json
D       infra/config/generated/builders/try/android-official/properties.json
D       infra/config/generated/builders/try/android-oreo-arm64-dbg/properties.json
D       infra/config/generated/builders/try/android-pie-arm64-dbg/properties.json
D       infra/config/generated/builders/try/android-webview-oreo-arm64-dbg/properties.json
D       infra/config/generated/builders/try/android-webview-pie-arm64-dbg/properties.json
D       infra/config/generated/builders/try/android-x64-cast/properties.json
D       infra/config/generated/builders/try/android-x86-rel-compilator/properties.json
D       infra/config/generated/builders/try/android-x86-rel/properties.json
D       infra/config/generated/builders/try/android_compile_dbg/properties.json
D       infra/config/generated/builders/try/android_compile_x64_dbg/properties.json
D       infra/config/generated/builders/try/android_compile_x86_dbg/properties.json
D       infra/config/generated/builders/try/android_cronet/properties.json
D       infra/config/generated/builders/try/android_optional_gpu_tests_rel/properties.json
D       infra/config/generated/builders/try/chromeos-amd64-generic-dbg/properties.json
D       infra/config/generated/builders/try/chromeos-amd64-generic-lacros-dbg/properties.json
M       infra/config/generated/builders/try/chromeos-amd64-generic-rel-compilator/properties.json
M       infra/config/generated/builders/try/chromeos-amd64-generic-rel-renamed/properties.json
D       infra/config/generated/builders/try/dawn-linux-x64-deps-rel/properties.json
D       infra/config/generated/builders/try/dawn-mac-x64-deps-rel/properties.json
D       infra/config/generated/builders/try/dawn-win10-x64-deps-rel/properties.json
D       infra/config/generated/builders/try/dawn-win10-x86-deps-rel/properties.json
D       infra/config/generated/builders/try/fuchsia-arm64-cast-receiver-rel/properties.json
D       infra/config/generated/builders/try/fuchsia-arm64-rel/properties.json
D       infra/config/generated/builders/try/fuchsia-official/properties.json
D       infra/config/generated/builders/try/fuchsia-x64-cast-receiver-rel-compilator/properties.json
D       infra/config/generated/builders/try/fuchsia-x64-cast-receiver-rel/properties.json
D       infra/config/generated/builders/try/fuchsia-x64-rel/properties.json
D       infra/config/generated/builders/try/gpu-fyi-cq-android-arm64/properties.json
D       infra/config/generated/builders/try/ios-simulator-compilator/properties.json
D       infra/config/generated/builders/try/ios-simulator-cronet/properties.json
D       infra/config/generated/builders/try/ios-simulator-full-configs/properties.json
D       infra/config/generated/builders/try/ios-simulator/properties.json
D       infra/config/generated/builders/try/lacros-amd64-generic-rel-non-skylab/properties.json
D       infra/config/generated/builders/try/lacros-amd64-generic-rel/properties.json
D       infra/config/generated/builders/try/lacros-arm-generic-rel-skylab/properties.json
D       infra/config/generated/builders/try/lacros-arm-generic-rel/properties.json
D       infra/config/generated/builders/try/lacros-arm64-generic-rel-skylab/properties.json
D       infra/config/generated/builders/try/lacros-arm64-generic-rel/properties.json
D       infra/config/generated/builders/try/linux-blink-rel/properties.json
D       infra/config/generated/builders/try/linux-chromeos-compile-dbg/properties.json
D       infra/config/generated/builders/try/linux-chromeos-dbg/properties.json
M       infra/config/generated/builders/try/linux-chromeos-rel-compilator/properties.json
M       infra/config/generated/builders/try/linux-chromeos-rel/properties.json
D       infra/config/generated/builders/try/linux-lacros-dbg/properties.json
D       infra/config/generated/builders/try/linux-lacros-rel-compilator/properties.json
D       infra/config/generated/builders/try/linux-lacros-rel/properties.json
D       infra/config/generated/builders/try/linux-official/gn-args.json
D       infra/config/generated/builders/try/linux-official/properties.json
D       infra/config/generated/builders/try/linux-rel-compilator/properties.json
D       infra/config/generated/builders/try/linux-rel/properties.json
D       infra/config/generated/builders/try/linux-wayland-rel-compilator/properties.json
D       infra/config/generated/builders/try/linux-wayland-rel/properties.json
D       infra/config/generated/builders/try/linux-x64-castos-dbg/properties.json
D       infra/config/generated/builders/try/linux-x64-castos/properties.json
D       infra/config/generated/builders/try/linux_chromium_asan_rel_ng-compilator/properties.json
D       infra/config/generated/builders/try/linux_chromium_asan_rel_ng/properties.json
D       infra/config/generated/builders/try/linux_chromium_compile_dbg_ng/properties.json
D       infra/config/generated/builders/try/linux_chromium_dbg_ng/properties.json
D       infra/config/generated/builders/try/linux_chromium_tsan_rel_ng-compilator/properties.json
D       infra/config/generated/builders/try/linux_chromium_tsan_rel_ng/properties.json
D       infra/config/generated/builders/try/linux_optional_gpu_tests_rel/properties.json
D       infra/config/generated/builders/try/mac-official/properties.json
D       infra/config/generated/builders/try/mac-rel-compilator/properties.json
D       infra/config/generated/builders/try/mac-rel/properties.json
D       infra/config/generated/builders/try/mac10.15-blink-rel/properties.json
D       infra/config/generated/builders/try/mac11-arm64-rel/properties.json
D       infra/config/generated/builders/try/mac11.0-blink-rel/properties.json
D       infra/config/generated/builders/try/mac11.0.arm64-blink-rel/properties.json
D       infra/config/generated/builders/try/mac12-arm64-rel/properties.json
D       infra/config/generated/builders/try/mac12-tests/properties.json
D       infra/config/generated/builders/try/mac12.0-blink-rel/properties.json
D       infra/config/generated/builders/try/mac12.0.arm64-blink-rel/properties.json
D       infra/config/generated/builders/try/mac13-arm64-rel-compilator/properties.json
D       infra/config/generated/builders/try/mac13-arm64-rel/properties.json
D       infra/config/generated/builders/try/mac13-blink-rel/properties.json
D       infra/config/generated/builders/try/mac13.arm64-blink-rel/properties.json
D       infra/config/generated/builders/try/mac_chromium_10.15_rel_ng/properties.json
D       infra/config/generated/builders/try/mac_chromium_11.0_rel_ng/properties.json
D       infra/config/generated/builders/try/mac_chromium_compile_dbg_ng/properties.json
D       infra/config/generated/builders/try/mac_optional_gpu_tests_rel/properties.json
D       infra/config/generated/builders/try/win-official/properties.json
D       infra/config/generated/builders/try/win-rel-compilator/properties.json
D       infra/config/generated/builders/try/win-rel/properties.json
D       infra/config/generated/builders/try/win10.20h2-blink-rel/properties.json
D       infra/config/generated/builders/try/win11-arm64-blink-rel/properties.json
D       infra/config/generated/builders/try/win11-blink-rel/properties.json
D       infra/config/generated/builders/try/win32-official/properties.json
D       infra/config/generated/builders/try/win_chromium_compile_dbg_ng/properties.json
D       infra/config/generated/builders/try/win_chromium_compile_rel_ng/properties.json
D       infra/config/generated/builders/try/win_optional_gpu_tests_rel/properties.json
M       infra/config/generated/cq-usage/default.cfg
M       infra/config/generated/cq-usage/full.cfg
M       infra/config/generated/cq-usage/mega_cq_bots.txt
M       infra/config/generated/health-specs/health-specs.json
M       infra/config/generated/luci/commit-queue.cfg
M       infra/config/generated/luci/cr-buildbucket.cfg
M       infra/config/generated/luci/luci-milo.cfg
M       infra/config/generated/luci/luci-notify.cfg
M       infra/config/generated/luci/luci-scheduler.cfg
M       infra/config/generated/luci/project.cfg
M       infra/config/generated/luci/realms.cfg
M       infra/config/generated/testing/mixins.pyl
M       infra/config/generated/testing/test_suites.pyl
M       infra/config/generated/testing/variants.pyl
M       infra/config/lib/orchestrator.star
M       infra/config/lib/try.star
M       infra/config/settings.json
M       infra/config/subprojects/chromium/try/tryserver.chromium.chromiumos.star
M       infra/config/subprojects/chromium/try/tryserver.chromium.fuchsia.star
M       infra/config/subprojects/chromium/try/tryserver.chromium.linux.star
M       infra/config/subprojects/chromium/try/tryserver.chromium.mac.star
M       infra/config/subprojects/chromium/try/tryserver.chromium.win.star
M       infra/config/targets/basic_suites.star
M       infra/config/targets/cros-skylab-variants.json
M       infra/config/targets/mixins.star
M       internal
M       ios/chrome/app/strings/resources/ios_chromium_strings_da.xtb
M       ios/chrome/app/strings/resources/ios_chromium_strings_is.xtb
M       ios/chrome/app/strings/resources/ios_chromium_strings_pl.xtb
M       ios/chrome/app/strings/resources/ios_chromium_strings_pt-PT.xtb
M       ios/chrome/app/strings/resources/ios_chromium_strings_uk.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_da.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_is.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_it.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_ja.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_pl.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_pt-BR.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_pt-PT.xtb
M       ios/chrome/app/strings/resources/ios_google_chrome_strings_ru.xtb
M       ios/chrome/app/strings/resources/ios_strings_ar.xtb
M       ios/chrome/app/strings/resources/ios_strings_be.xtb
M       ios/chrome/app/strings/resources/ios_strings_da.xtb
M       ios/chrome/app/strings/resources/ios_strings_de.xtb
M       ios/chrome/app/strings/resources/ios_strings_en-GB.xtb
M       ios/chrome/app/strings/resources/ios_strings_es-419.xtb
M       ios/chrome/app/strings/resources/ios_strings_es.xtb
M       ios/chrome/app/strings/resources/ios_strings_fa.xtb
M       ios/chrome/app/strings/resources/ios_strings_fr.xtb
M       ios/chrome/app/strings/resources/ios_strings_hi.xtb
M       ios/chrome/app/strings/resources/ios_strings_hr.xtb
M       ios/chrome/app/strings/resources/ios_strings_hy.xtb
M       ios/chrome/app/strings/resources/ios_strings_it.xtb
M       ios/chrome/app/strings/resources/ios_strings_ja.xtb
M       ios/chrome/app/strings/resources/ios_strings_kn.xtb
M       ios/chrome/app/strings/resources/ios_strings_ko.xtb
M       ios/chrome/app/strings/resources/ios_strings_mr.xtb
M       ios/chrome/app/strings/resources/ios_strings_or.xtb
M       ios/chrome/app/strings/resources/ios_strings_pl.xtb
M       ios/chrome/app/strings/resources/ios_strings_pt-BR.xtb
M       ios/chrome/app/strings/resources/ios_strings_pt-PT.xtb
M       ios/chrome/app/strings/resources/ios_strings_ru.xtb
M       ios/chrome/app/strings/resources/ios_strings_sk.xtb
M       ios/chrome/app/strings/resources/ios_strings_th.xtb
M       ios/chrome/app/strings/resources/ios_strings_tr.xtb
M       ios/chrome/app/strings/resources/ios_strings_uk.xtb
M       ios/chrome/app/strings/resources/ios_strings_vi.xtb
M       ios/chrome/app/strings/resources/ios_strings_zh-CN.xtb
M       ios/chrome/app/strings/resources/ios_strings_zh-TW.xtb
M       ios/chrome/credential_provider_extension/strings/resources/ios_credential_provider_extension_strings_pt-BR.xtb
M       ios/chrome/credential_provider_extension/strings/resources/ios_credential_provider_extension_strings_vi.xtb
M       ios_internal
M       mojo/public/tools/bindings/generators/mojom_ts_generator.py
M       remoting/resources/remoting_strings_mr.xtb
M       remoting/resources/remoting_strings_vi.xtb
M       services/network/public/cpp/source_stream_to_data_pipe.cc
M       services/network/public/cpp/source_stream_to_data_pipe_unittest.cc
M       testing/buildbot/chrome.json
M       testing/buildbot/filters/linux-lacros.interactive_ui_tests.filter
M       testing/buildbot/internal.chromeos.fyi.json
M       testing/buildbot/mixins.pyl
M       testing/buildbot/test_suite_exceptions.pyl
M       testing/buildbot/test_suites.pyl
M       testing/buildbot/variants.pyl
M       third_party/blink/public/strings/translations/blink_accessibility_strings_or.xtb
M       third_party/blink/public/strings/translations/blink_accessibility_strings_zh-CN.xtb
M       third_party/blink/renderer/core/dom/element.h
M       third_party/blink/renderer/core/html/parser/html_construction_site.cc
M       third_party/blink/renderer/modules/canvas/canvas2d/base_rendering_context_2d.cc
M       third_party/blink/renderer/modules/webaudio/analyser_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_handler.cc
M       third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc
M       third_party/blink/renderer/modules/webaudio/deferred_task_handler.cc
M       third_party/blink/web_tests/TestExpectations
M       third_party/blink/web_tests/external/wpt/html/semantics/links/hyperlink-auditing/headers.optional-expected.txt
M       third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-audioworklet-interface/audioworkletprocessor-process-frozen-array.https.html
A       third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-audioworklet-interface/process-parameters.https-expected.txt
D       third_party/blink/web_tests/platform/mac-mac11-arm64/external/wpt/html/semantics/links/hyperlink-auditing/headers.optional-expected.txt
D       third_party/blink/web_tests/platform/mac-mac12-arm64/external/wpt/html/semantics/links/hyperlink-auditing/headers.optional-expected.txt
D       third_party/blink/web_tests/platform/mac-mac13-arm64/external/wpt/html/semantics/links/hyperlink-auditing/headers.optional-expected.txt
M       third_party/ipcz/src/ipcz/driver_memory.cc
M       third_party/ipcz/src/ipcz/driver_transport.cc
M       third_party/libaddressinput/chromium/resources/address_input_strings_ar.xtb
M       third_party/libaddressinput/chromium/resources/address_input_strings_id.xtb
M       third_party/libaddressinput/chromium/resources/address_input_strings_it.xtb
M       third_party/libaddressinput/chromium/resources/address_input_strings_th.xtb
M       third_party/libaddressinput/chromium/resources/address_input_strings_vi.xtb
M       third_party/skia
M       tools/mb/mb.py
M       tools/metrics/histograms/enums.xml
M       ui/accessibility/extensions/strings/accessibility_extensions_strings_vi.xtb
M       ui/chromeos/translations/ui_chromeos_strings_be.xtb
M       ui/chromeos/translations/ui_chromeos_strings_ca.xtb
M       ui/chromeos/translations/ui_chromeos_strings_fa.xtb
M       ui/chromeos/translations/ui_chromeos_strings_fi.xtb
M       ui/chromeos/translations/ui_chromeos_strings_hr.xtb
M       ui/chromeos/translations/ui_chromeos_strings_id.xtb
M       ui/chromeos/translations/ui_chromeos_strings_is.xtb
M       ui/chromeos/translations/ui_chromeos_strings_it.xtb
M       ui/chromeos/translations/ui_chromeos_strings_iw.xtb
M       ui/chromeos/translations/ui_chromeos_strings_kn.xtb
M       ui/chromeos/translations/ui_chromeos_strings_ky.xtb
M       ui/chromeos/translations/ui_chromeos_strings_mk.xtb
M       ui/chromeos/translations/ui_chromeos_strings_mr.xtb
M       ui/chromeos/translations/ui_chromeos_strings_or.xtb
M       ui/chromeos/translations/ui_chromeos_strings_pl.xtb
M       ui/chromeos/translations/ui_chromeos_strings_pt-PT.xtb
M       ui/chromeos/translations/ui_chromeos_strings_ru.xtb
M       ui/chromeos/translations/ui_chromeos_strings_sl.xtb
M       ui/chromeos/translations/ui_chromeos_strings_sq.xtb
M       ui/chromeos/translations/ui_chromeos_strings_sv.xtb
M       ui/chromeos/translations/ui_chromeos_strings_ta.xtb
M       ui/chromeos/translations/ui_chromeos_strings_vi.xtb
M       ui/strings/translations/ui_strings_nl.xtb
M       ui/strings/translations/ui_strings_pt-BR.xtb
M       ui/strings/translations/ui_strings_vi.xtb
M       v8

https://chromium-review.googlesource.com/5402058


### pe...@google.com (2024-04-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41485789)*
