# Detecting if the XSS Auditor was triggered by changing the hash

| Field | Value |
|-------|-------|
| **Issue ID** | [40092270](https://issues.chromium.org/issues/40092270) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-08-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

If a page is redirected to itself and has a hash set, no navigation is performed, instead, only the hash is changed.

This behavior is different when the page is being blocked by the XSS Auditor. In this case, if the page is redirected to itself and has a hash set, a navigation will happen.

Knowning this, it's possible to infer with certainty whether a cross-origin page triggered the XSS Auditor or not by checking the number of times the page is loaded after being redirected to itself.

This issue is very similar to <https://crbug.com/chromium/396544> and because of that, the PoC will only be demonstrating how to detect if the XSS Auditor was triggered, given the consequences of this were already discussed in the other issue.

**VERSION**  

Chrome 68.0.3440.106  

Chrome 70.0.3530.0

**REPRODUCTION CASE**

1. Open <https://lbherrera.github.io/lab/xss-auditor/hash.html>
2. Check the alert.

## Attachments

- [server1-hash.html](attachments/server1-hash.html) (text/plain, 816 B)
- [server2-auditor.html](attachments/server2-auditor.html) (text/plain, 129 B)

## Timeline

### va...@chromium.org (2018-08-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### va...@chromium.org (2018-08-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-07)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-09-22)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2018-10-02)

tsepez@: I was giving a look into this again and there is a variation of this attack that allows an attacker to detect if a cross-window navigation triggered the XSS Auditor. I am not sure if I should file a new bug about this, what do you think?

// history.length will be 2 when the XSS Auditor was triggered
var win = window.open('https://bharl.github.io/test/auditor.html#<script>let secret="1337";</script>');

setTimeout(function() {
	win.location.href="https://bharl.github.io/test/auditor.html#random";
	win.location.href="https://example.org";
}, 3000);

// history.length will be 3 when the XSS Auditor was not triggered
var win = window.open('https://bharl.github.io/test/auditor.html#<script>..................</script>');

setTimeout(function() {
	win.location.href="https://bharl.github.io/test/auditor.html#random";
	win.location.href="https://example.org";
}, 3000);

### ts...@chromium.org (2018-10-02)

I think we can track both of them here.  Thanks.

### ts...@chromium.org (2018-10-02)

Updating title.

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### he...@gmail.com (2018-11-14)

tsepez@: Gareth Heyes published an article (https://portswigger.net/blog/exposing-intranets-with-reliable-browser-based-port-scanning) where he is abusing this bug to scan ports (but didn't make the connection to use it to detect the XSS Auditor). Given that, maybe the priority on this bug should be increased (before someone arrives at the same conclusion and starts to exploit this).

Also, I was revisiting the attack scenario, and it's possible to use this to perform a XS-Search attack on almost any website (which I think would increase the severity of this bug).

I will be following with a real world PoC to demonstrate this revised attack to see what you think.

### ts...@chromium.org (2018-11-14)

Thanks. I'm trying to remember why we're looking for reflections in the hash in the first place, if the hash is never even seen by the server and can't be reflected. So maybe a quick improvement is to drop the hash from the URL before scanning it. 

### he...@gmail.com (2018-11-14)

Dropping the hash would improve the situation only if the user was trying to bruteforce tokens or something like that (because then he would need more requests to achieve the same).

But the attack still could be carried on by iframing the url below:
https://victim.com/index.php?xss=<script>token=123;</script>

And then redirecting it to:
https://victim.com/index.php?xss=<script>token=123;</script>#random

### ts...@chromium.org (2018-11-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fae997a21159afe19af4ffeef44b997f11161358

commit fae997a21159afe19af4ffeef44b997f11161358
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Nov 15 18:01:59 2018

XSSAuditor: do not look for reflection in URL fragment.

The server never sees it, so it can't be part of a reflected XSS. It
may be part of a DOM XSS, but XSSAuditor doesn't handle these, except
for a few document.write() cases that aren't likely to manifest in
the wild (but are hit by tests).

Bug: 877347
Change-Id: I6835c7702d0a8db829f5fde17be15015112a5e13
Reviewed-on: https://chromium-review.googlesource.com/c/1336368
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Cr-Commit-Position: refs/heads/master@{#608430}
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-expected.txt
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-inline-event-expected.txt
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-inline-event-null-char-expected.txt
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-inline-event-null-char.html
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-inline-event.html
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-javascript-URL-expected.txt
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-javascript-URL.html
[delete] https://crrev.com/b268b3ed370ba2885cc5c2fe8230dde91be40d20/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location.html
[modify] https://crrev.com/fae997a21159afe19af4ffeef44b997f11161358/third_party/blink/renderer/core/html/parser/xss_auditor.cc


### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-14)

(bulk edit: herrerahlb@gmail.com is the new email address for luan.herrera@hotmail.com)

### he...@gmail.com (2019-01-28)

tsepez@: I think this bug is missing from https://chromium.googlesource.com/chromium/src.git/+/543ab577f3ce4a1c64af827a4dbdaa37804845c2 given it will also be fixed by it.

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this? Has this been fixed by #18 or #21?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-06-20)

tsepez, is this fixed?

### ts...@chromium.org (2019-06-20)

Not entirely.  The effect is somewhat minimized, but final resolution depends on the overall fate of XSSauditor.

### he...@gmail.com (2019-07-23)

Hi,

I was giving a look into Chrome's VRP FAQ regarding the disclosure of bugs before you had the chance to fix them and was wondering if the disclosure of a bug after the 90-day deadline makes it ineligible for a bounty. If it does not, would be possible for this report to be disclosed?

Thanks!

### aw...@google.com (2019-07-25)

Opening up per request in https://crbug.com/chromium/877347#c29. Given it's been so long, yes, we'd still consider this for reward once fixed.  Cheers!

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-08-13)

Obsolete per https://crbug.com/968591

### aw...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### aw...@google.com (2019-09-09)

(also worth considering in conjunction with https://bugs.chromium.org/p/chromium/issues/detail?id=898081)

### sh...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $1,000 for this report :)

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/877347?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092270)*
