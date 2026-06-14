# CSP bypass with import maps

| Field | Value |
|-------|-------|
| **Issue ID** | [40094281](https://issues.chromium.org/issues/40094281) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>Script, Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2019-03-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Import maps allow defining import script urls without declearing nonce in script element. Landing this feature would basically allow CSP bypass on sites that uses module import.This feature is planned for Origin Trials in Chrome 74. See: <https://developers.google.com/web/updates/2019/03/kv-storage>

**VERSION**  

Chrome Version: 74 dev + chrome://flags/#enable-experimental-web-platform-features  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Go to <https://test.shhnjk.com/imap.php>

## Attachments

- [imap.php](attachments/imap.php) (text/plain, 502 B)

## Timeline

### wf...@chromium.org (2019-03-13)

mkwst can you help with triage of this bug? Thanks.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### rs...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>HTML>Modules]

### Ju...@microsoft.com (2019-03-13)

May I know why this is Security_Severity-Low?

### do...@chromium.org (2019-03-13)

So, the thing to understand about import maps is that the `import "x"` specifier is not referencing a URL, but instead an arbitrary string which gets remapped via the map into a real URL. See https://github.com/WICG/import-maps/blob/master/Security%20and%20Privacy.md for more.

With that in mind, is the bug here that normally

import {storage} from 'data:application/javascript,const%20storage=()=>{};storage.set=(a,b)=>{alert(self.origin)};export%20{storage};'

would not work (given Content-Security-Policy: script-src 'nonce-test')

but the provided repro does work? If so, that would be a bug indeed.

### rs...@chromium.org (2019-03-13)

Re: #3: Full CSP bypass is usually Medium, with partial at Low. In this case, the mitigating factor of requiring enable-experimental-web-platform-features makes it Low.

### Ju...@microsoft.com (2019-03-13)

> In this case, the mitigating factor of requiring 
> enable-experimental-web-platform-features makes it Low.
As I explain, that is not the case for Chrome 74. Origin Trials will declaring of token via meta tag. Which is possible assumption here since CSP is mitigation for XSS, and XSS means there's some content injection, therefore meta tag can also be injected.

### hi...@chromium.org (2019-03-14)

Thanks for feedback!

I think at least <script type="importmap"> should obey the script-src inline
check just like an inline script.
(In the test case above, <script type="importmap"> should also have nonce="test",
or otherwise the import map should be rejected)

IIUC in this case this is sufficient?
(I'm not so sure whether this is sufficient in general though)

> https://crbug.com/chromium/941340#c4

<script type="module">import {storage} from 'data:...';</script>

=> the data URL script is NOT executed.

<script type="module" nonce="test">import {storage} from 'data:...';</script>

=> the data URL script IS executed.

<script type="importmap">...</script>
<script type="module" nonce="test">import {storage} from ''/path/to/kv-storage-polyfill.mjs';</script>

=> the data URL script IS executed (but actually should NOT be executed).

<script type="importmap" nonce="test">...</script>
<script type="module" nonce="test">import {storage} from ''/path/to/kv-storage-polyfill.mjs';</script>

=> the data URL script IS executed (and this is OK?).


[Monorail components: -Blink>HTML>Modules Blink>HTML>Script]

### mk...@chromium.org (2019-03-14)

https://github.com/WICG/import-maps/issues/105 suggests that the maps themselves should be subject in some way to CSP (as they offer a more robust version of the capability `base-uri` aims to govern). I agree with that suggestion, and with hiroshige@'s note below that they should be explicitly nonced or safelisted. I don't have a strong opinion about the syntax, and I'm open to suggestions. :)

With regard to the script that's actually executed, https://github.com/WICG/import-maps/blob/master/spec.md#import-url-fetches isn't exactly fleshed out, but it appears that y'all simply want to modify the URL before passing it into Fetch. That seems reasonable, and means that CSP doesn't need to change in order to specify the way that the source lists govern imports. So, I agree with Domenic: if `data:` isn't enabled in the page's policy, import maps shouldn't allow it to be loaded.

### mk...@chromium.org (2019-03-14)

(And I'll bump this back to medium, as origin trials are indeed enough like shipping a feature to count.)

### sh...@chromium.org (2019-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-14)

[Empty comment from Monorail migration]

### hi...@chromium.org (2019-03-14)

> https://github.com/WICG/import-maps/issues/105

Does anyone have specific opinions on how CSPs are applied to import maps?
If so, could you comment in the github thread?

Drafted a CL:
(Applies CSP checks to inline import maps just like an inline script)
https://chromium-review.googlesource.com/c/chromium/src/+/1525017

Does the expectations in the tests reasonable?

### Ju...@microsoft.com (2019-03-16)

>Does the expectations in the tests reasonable?
LGTM

### sh...@chromium.org (2019-03-18)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-03-18)

Reminder M74 is ALREADY branched and going to Beta this week. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix & request a merge to M74 ASAP, so the change gets enough beta coverage. Thank you.

### go...@chromium.org (2019-03-18)

Reminder M74 is ALREADY branched and going to Beta this week. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix & request a merge to M74 ASAP, so the change gets enough beta coverage. Thank you.

### go...@chromium.org (2019-03-20)

Reminder M74 is ALREADY branched and going to Beta THIS week. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix & request a merge to M74 ASAP, so the change gets enough beta coverage. Thank you.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/53c0db4bf947b45761c45c67851fc1695a1aa03a

commit 53c0db4bf947b45761c45c67851fc1695a1aa03a
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Wed Mar 20 19:27:23 2019

[Import Maps] Apply inline-script CSP checks to import maps

Bug: 941340
Change-Id: I1d8d6aebad4650b638f0b7ccdbfae55d398e905e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1525017
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Commit-Position: refs/heads/master@{#642608}
[modify] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/renderer/core/script/script_loader.cc
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/applied-to-target-dynamic.sub.tentative.html
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/applied-to-target.sub.tentative.html
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/hash-failure.tentative.html
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/hash.tentative.html
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/nonce-failure.tentative.html
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/nonce.tentative.html
[add] https://crrev.com/53c0db4bf947b45761c45c67851fc1695a1aa03a/third_party/blink/web_tests/external/wpt/import-maps/csp/unsafe-inline.tentative.html


### ko...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### hi...@chromium.org (2019-03-22)

The CL (https://crbug.com/chromium/941340#c20) 75.0.3740.0.
Requesting merge to M-74.

While still the discussion on https://github.com/WICG/import-maps/issues/105 is ongoing, it's better to merge the CL as a baseline protection for CSS bypass.

### hi...@chromium.org (2019-03-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-22)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-23)

+adetaylor@ (Security TPM) for M74 merge review.

### sh...@chromium.org (2019-03-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-25)

[Empty comment from Monorail migration]

### ab...@google.com (2019-03-25)

branch:3729

### go...@chromium.org (2019-03-26)

Pls merge your change to M74 branch 3729 ASAP so we can pick it up for this week beta release. Thank you.

### cr...@appspot.gserviceaccount.com (2019-03-26)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/3ae016549b6ac83bbfc3ec1044292af82d80d13b

Commit: 3ae016549b6ac83bbfc3ec1044292af82d80d13b
Author: hiroshige@chromium.org
Commiter: hiroshige@chromium.org
Date: 2019-03-26 01:43:18 +0000 UTC

[Import Maps] Apply inline-script CSP checks to import maps

Bug: 941340
Change-Id: I1d8d6aebad4650b638f0b7ccdbfae55d398e905e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1525017
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#642608}(cherry picked from commit 53c0db4bf947b45761c45c67851fc1695a1aa03a)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1537324
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#442}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### na...@google.com (2019-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-26)

Congrats! The Panel decided to reward $1,000 for this report. 

### na...@google.com (2019-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hi...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

### is...@google.com (2019-10-15)

This issue was migrated from crbug.com/chromium/941340?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Script, Blink>SecurityFeature>ContentSecurityPolicy]
[Monorail blocking: crbug.com/chromium/848607]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094281)*
