# Security: Fetch API reveals existence of Redirection in no-cors mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40089770](https://issues.chromium.org/issues/40089770) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Network>FetchAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2018-4117 |
| **Reporter** | ah...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2017-12-03 |
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

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**VULNERABILITY DETAILS**  

Fetch API can detect if the request is redirected even when in fetch mode "no-cors". If the request mode is set to opaque, this information should not be determinable.

**VERSION**  

Chrome Version: latest stable  

Operating System: Windows 10

**REPRODUCTION CASE**  

I do not own the website. When using fetch api in "no-cors" mode the response is set to opaque. Which means no information about if the request is redirected should be revealed.

//Normal, correct behaviour, works fine  

fetch("<https://jigsaw.w3.org/HTTP/300/307.html>", {  

mode: 'no-cors'  

}).then(function (response) {  

if (response.redirected) {  

console.log("Redirected")  

} else {}  

return response.blob()  

}).then(function (imageBlob) {  

console.log("Found")  

}).catch(function () {  

console.log("Error request blocked.")  

})

//Limitation bypass  

fetch("<https://jigsaw.w3.org/HTTP/300/307.html>", {  

mode: 'no-cors',  

redirect: "error"  

}).then(function (response) {  

return response.blob()  

}).then(function (imageBlob) {  

console.log("Downloaded")  

}).catch(function () {  

console.log("Redirected or Error")  

})

## Timeline

### el...@chromium.org (2017-12-03)

At first glance, this looks like a spec issue to me; I don't see anything in https://fetch.spec.whatwg.org/#concept-request-redirect-mode that implies something different should happen in the case of |redirect: "error"| for a no-cors request.


[Monorail components: Blink>Network>FetchAPI]

### ah...@gmail.com (2017-12-03)

[Comment Deleted]

### ra...@chromium.org (2017-12-04)

horo: could you please help triage? Thanks!

### pa...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-12-04)

Sorry I meant to be Impact stable rather than RBS

### ty...@chromium.org (2017-12-04)

elawrence@ is right, I think. "Main fetch" has a step to taint a response, but it happens only when the response obtained by the step 5 is not a network error. "Scheme fetch" returns a network error returned by "HTTP fetch".

Looks SRI has the same issue though SRI is specified to run "match" on a tainted response which may just always fail.

That said, it looks it's been already discussed. horo@ should be familiar with the details.
https://github.com/whatwg/fetch/issues/79


### ho...@chromium.org (2017-12-04)

I think this is a spec issue.
The same problem exists in all other major browsers (Safari, FireFox and Edge).

I think https://github.com/whatwg/fetch/issues/79 is different from this issue.
That fetch spec https://crbug.com/chromium/79 was to protect a web site which is using service worker and redirection from XSS attack.

But this issue is not related to service worker.
For example you can detect whether the web site visitor is an Gmail user or not using this code:
  fetch("https://mail.google.com/mail/u/0/", {
    mode: 'no-cors',
    redirect: 'error',
    credentials: 'include'
  })
  .then(() => {
    console.log('GMail user');
  }).catch(() => {
    console.log('Not GMail user');
  });


annevk@
What do you think?

### an...@gmail.com (2017-12-04)

It seems this was introduced in https://github.com/whatwg/fetch/issues/66#issuecomment-118638144.

My analysis there seems correct, but the fix didn't restrict things to same-origin requests unfortunately. (We were much worse about enforcing review for pull requests back then unfortunately, although those are still hard to come by. Getting more security on all things service workers touched would be good.)

I think the correct fix here would be enforcing that request's mode is "navigate", "websocket", or "same-origin". That should be an assert somewhere in the fetching and algorithm. If request's mode is something else a TypeError seems appropriate in the API (the Request constructor).

Does that help? I can work on more detailed proposed changes to be made after this and equivalent bugs against other browsers are opened up if that's desirable.

Did OP file an equivalent bug against Firefox? (And maybe Edge/Safari, they shipped this too I guess even though they don't have service workers?)

### ah...@gmail.com (2017-12-04)

[Comment Deleted]

### an...@gmail.com (2017-12-04)

ahsanejaz26, please copy me (I'm annevk@annevk.nl) if you can. I'd like to make sure we all end up with the same fix.

### ah...@gmail.com (2017-12-04)

I have filed for Firefox and Edge. 

### ah...@gmail.com (2017-12-04)

[Comment Deleted]

### ah...@gmail.com (2017-12-04)

Someone needs to file for Safari

### an...@gmail.com (2017-12-04)

I filed https://bugs.webkit.org/show_bug.cgi?id=180347.

### an...@gmail.com (2017-12-04)

[Empty comment from Monorail migration]

### dv...@mozilla.com (2017-12-04)

Firefox equivalent is https://bugzilla.mozilla.org/show_bug.cgi?id=1422710

### ho...@chromium.org (2017-12-04)

Thank you for filing bugs.
I think checking the request's mode looks good.


### ra...@chromium.org (2017-12-05)

In my mind it's unclear what kind of attacks this could be used for and thus what the severity should be. Tentatively assigning low severity, but horo or others, could you please outline the risks involved with this bug?

### an...@gmail.com (2017-12-05)

The risk is that you can more easily determine whether a user has an account with a given site (assuming the site offers credential-based redirects, which is quite common). However, a determined attacker is likely also able to figure this out through timing attacks.

### ah...@gmail.com (2017-12-05)

[Comment Deleted]

### sh...@chromium.org (2017-12-05)

[Empty comment from Monorail migration]

### an...@gmail.com (2017-12-05)

In https://bugzilla.mozilla.org/show_bug.cgi?id=1422710#c5 Ben suggested to instead return a network error by modifying step 5 in https://fetch.spec.whatwg.org/#main-fetch as follows:

* request’s mode is "no-cors" 
  1. If request's redirect mode is "error" return a NetworkError.
  2. Set request’s response tainting to "opaque".
  3. Return the result of performing a scheme fetch using request.

I think that would work and would less likely break existing code that does not expect an exception. I would only suggest to also check (and therefore block) "manual" as otherwise we make timing attacks rather easy.

### an...@gmail.com (2017-12-05)

[Empty comment from Monorail migration]

### ho...@chromium.org (2017-12-07)

Reassigning to tyoshino@

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### an...@gmail.com (2018-04-17)

Is someone planning on fixing this? I'm planning on updating the specification. Since WebKit already published tests I guess this attack is already publicly known, but it would still be nice not to spread the knowledge further without fixes having landed.

(Removing Owner as tyoshino left.)

### an...@gmail.com (2018-04-17)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-04-17)

I'm a bit confused - Is https://github.com/whatwg/fetch/commit/14858d3e9402285a7ff3b5e47a22896ff3adc95d the fix you mention?

### an...@gmail.com (2018-04-18)

Yeah, I was confused and we already made the change. My bad.

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2018-04-19)

Please be aware that I think the upstream test that landed today does not match what landed in the spec.  I'm working on a PR to update the test and will share it here when its ready.

### [Deleted User] (2018-04-19)

Please see:

https://github.com/w3c/web-platform-tests/pull/10536

### bu...@chromium.org (2018-04-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a62f913109fc1566230f5963bbf69ee65274ebc8

commit a62f913109fc1566230f5963bbf69ee65274ebc8
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Apr 24 02:23:37 2018

[Fetch API] Fix redirect leak on "no-cors" requests

The spec issue is now fixed, and this CL follows the spec change[1].

1: https://github.com/whatwg/fetch/commit/14858d3e9402285a7ff3b5e47a22896ff3adc95d

Bug: 791324
Change-Id: Ic3e3955f43578b38fc44a5a6b2a1b43d56a2becb
Reviewed-on: https://chromium-review.googlesource.com/1023613
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#552964}
[delete] https://crrev.com/79ca910048175c9118606b96a840516ace45f6c7/third_party/WebKit/LayoutTests/external/wpt/fetch/api/redirect/redirect-mode-expected.txt
[delete] https://crrev.com/79ca910048175c9118606b96a840516ace45f6c7/third_party/WebKit/LayoutTests/external/wpt/fetch/api/redirect/redirect-mode-worker-expected.txt
[modify] https://crrev.com/a62f913109fc1566230f5963bbf69ee65274ebc8/third_party/blink/renderer/core/fetch/fetch_manager.cc


### yh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

Thanks for the report ahsanejaz26@ - the VRP panel decided to award $500 for this! A member of our finance team will be in touch to arrange for payment. Also, how would you like to be credited in the Chrome release notes?

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### ah...@gmail.com (2018-05-04)

Hi,
Thanks a lot for the reward! 
Crediting like this would be fine "AhsanEjaz - @AhsanEjazA".

### ah...@gmail.com (2018-05-05)

Hi,
One more thing, the bug has been disclosed to Webkit and Mozilla already, after Chromium, as stated in early comments of the thread. The fix for Webkit is there, and they assigned it CVE-2018-4117, for their products. https://nvd.nist.gov/vuln/detail/CVE-2018-4117 . I'm not sure if Mozilla and Webkit are "third parties who are not directly involved in fixing the bug" or not.

### aw...@google.com (2018-05-07)

ahsanejaz26@ - thanks for hilighting that, but it wont' be a problem for the VRP payment

### fa...@chromium.org (2018-05-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-31)

This issue was migrated from crbug.com/chromium/791324?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/834895]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089770)*
