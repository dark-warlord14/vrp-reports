# Security: TrustedTypes does not block assignment when modifying existing attribute value via nodeValue/textContent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058798](https://issues.chromium.org/issues/40058798) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>TrustedTypes |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2022-02-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

TrustedTypes blocks the following cases:

```
iframe.setAttribute('srcdoc','XSS');//blocked  
iframe.srcdoc='XSS';//blocked  

```

But if the existing attribute value is modified via the nodeValue or textContent property, it does not block the assignment. e.g.:

```
iframe.attributes.srcdoc.nodeValue='XSS';  
iframe.attributes.srcdoc.textContent='XSS';  

```

This should be expected to be blocked.

**VERSION**  

Version 100.0.4892.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**  

You can reproduce it here: <https://vulnerabledoma.in/ttbypass_attr_nodeValue_textContent.html>  

I attached the same HTML.

**CREDIT INFORMATION**

Reporter credit: Masato Kinugawa

## Attachments

- [ttbypass_attr_nodeValue_textContent.html](attachments/ttbypass_attr_nodeValue_textContent.html) (text/plain, 492 B)
- [ttbypass_attr_nodeValue_textContent2.html](attachments/ttbypass_attr_nodeValue_textContent2.html) (text/plain, 517 B)

## Timeline

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### ye...@google.com (2022-02-16)

frame-src needs to be set in the CSP in order to lock the iframe src attribute. This also is not a chrome specific vulnerability.

If you get a working exploit with frame-src enabled in the CSP I recommend filing the bug at https://bughunters.google.com/report.

### ma...@gmail.com (2022-02-16)

This is not a CSP bypass but it is a TrustedTypes bypass. TruesedTypes is a security feature to block the "assignment" itself (not the script execution).

### ma...@gmail.com (2022-02-16)

Note that these assignments are not blocked not only for the srcdoc attribute but also for other XSS sinks, which should be blocked (e.g. event handler, script-src).
I created the PoC for the script-src and onclick: https://vulnerabledoma.in/ttbypass_attr_nodeValue_textContent2.html

### ko...@google.com (2022-02-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>TrustedTypes]

### ko...@google.com (2022-02-22)

[Empty comment from Monorail migration]

### ko...@google.com (2022-02-23)

Daniel, can you look at these? I think this is mentioning the attribute node direct modification, the most relevant bits being described https://github.com/w3c/webappsec-trusted-types/issues/248#issuecomment-576373688.

### ko...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-23)

I've attempted to open the repro but I am not sure what it demonstrates. I just see 2 imgs that are not loaded, so it's hard to check what versions of Chrome it would repro in.

### [Deleted User] (2022-02-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@chromium.org (2022-03-03)

Can repro. I agree this is a Trusted Types bypass, and particularly agree with https://crbug.com/chromium/1298122#c0, https://crbug.com/chromium/1298122#c3 and https://crbug.com/chromium/1298122#c4.

(No idea what to do with this, yet.)

### vo...@chromium.org (2022-03-03)

[Empty comment from Monorail migration]

### vo...@chromium.org (2022-03-03)

[still tentative]

Most DOM Node apis have an external (JS-callable) version and an internal one, where the JS-callable one does additional checks, while the internal one is expected to do as it's told. A common pattern is that the JS-callable one has an ExceptionState argument, and the internal one doesn't. For Attr::setAttribute this applies as well. It turns out that:

- Attr::setNodeValue doesn't take an ExceptionState
- it calls the ExceptionState-less Attr::setAttribute
- ExceptionState-less Attr::setAttribute doesn't run the TT check, because 1, it looks like it'd be internal-use only, and 2, it doesn't have an ExceptionState to report the exception to.

The net result is that setting the nodeValue on a DOM Attribute node doesn't ever run the TT check, while setting the attribute directly would have.

### vo...@chromium.org (2022-03-08)

Fix in progress, crrev.com/c/3497765.

### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9903cb3f093dd569bbc19aaab525cd0239a98366

commit 9903cb3f093dd569bbc19aaab525cd0239a98366
Author: Daniel Vogelheim <vogelheim@chromium.org>
Date: Mon Mar 14 13:04:04 2022

[Trusted Types] Ensure Trusted Types check runs on all Attr methods.

Ensure that assigning to a DOM attribute's nodeValue or
textContent property runs the same checks as calling setValue.

BUG: 1298122
Change-Id: Ia71f18ca98a4bcea58ec1014c71bcb0944d9aecb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3503905
Reviewed-by: Yifan Luo <lyf@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Commit-Queue: Daniel Vogelheim <vogelheim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#980525}

[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/character_data.cc
[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/character_data.h
[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/node.idl
[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/node.h
[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/attr.h
[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/node.cc
[add] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/web_tests/external/wpt/trusted-types/block-string-assignment-to-attribute-via-attribute-node.tentative.html
[modify] https://crrev.com/9903cb3f093dd569bbc19aaab525cd0239a98366/third_party/blink/renderer/core/dom/attr.cc


### vo...@chromium.org (2022-03-14)

Should be fixed now. Thanks for the report!

(Explanation in https://crbug.com/chromium/1298122#c13 was correct. Link in https://crbug.com/chromium/1298122#c14 was incorrect; https://crbug.com/chromium/1298122#c15 is the correct CL. )

I set FoundIn to M83, which is when TT was launched, since I think this bug has been in since the initial release.

### [Deleted User] (2022-03-14)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-14)

[Empty comment from Monorail migration]

### vo...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### vo...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

Requesting merge to beta M100 because latest trunk commit (980525) appears to be after beta branch point (972766).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

Merge review required: M100 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-17)

M100 merge approved; please merge this fix to branch 4896 NLT 12p PDT/8p CET Monday, 21 March so this fix can be included in M100 stable cut -- thank you

### am...@chromium.org (2022-03-18)

after talking off-bug to a vogelheim@, there is moderate risk with introducing this fix to M100 stable; removing merge approval and letting this fix matriculate into M101 rather than be merged to stable at this time 

### vo...@chromium.org (2022-03-18)

https://crbug.com/chromium/1298122#c25: 
1.This is a security fix. The release guidelines do say, "any security issue", so it should be in scope.
2. https://crbug.com/chromium/1298122#c15 (https://chromium-review.googlesource.com/c/chromium/src/+/3503905)
3. Yes, but not for long. This landed only this week.
4. No.
5. n/a
6. n/a

Generally, I'm a bit skeptical on a backmerge just before stable:
- IMHO, the fix is medium risky, on grounds that the code area (DOM implementation) is fairly fundamental, but I don't know it super well.
- IMHO, the risk of the underlying security issue is moderate, since it isn't exploitable by itself and has been in the code for a while.

Overall, I'd be happier if the fix had a bit more time to "bake in". Of course, I'll be happy to follow whatever decision the release folks take.

### vo...@google.com (2022-03-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations, Masato! The VRP Panel would like to extend to you a $1,000 reward for this issue. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### vo...@chromium.org (2022-04-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1298122?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058798)*
