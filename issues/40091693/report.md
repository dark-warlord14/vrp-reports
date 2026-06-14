# XSS by hosting JS and JSON looking file

| Field | Value |
|-------|-------|
| **Issue ID** | [40091693](https://issues.chromium.org/issues/40091693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | go...@chromium.org |
| **Created** | 2018-06-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36

Steps to reproduce the problem:
1. Go to https://attack.shhnjk.com/pay_handler.html
2. Hold Enter key for 3 seconds
3. Observe that attacker gets XSS capability in test.shhnjk.com

What is the expected behavior?
Nothing happens

What went wrong?
TL;DR: Ability to host JS file and JSON file to specific origin causes XSS

Chrome implemeted something called "JIT payment app installation" in Payment Handler API. This feature allows installation of cross-origin payment app in user's browser when user clicks on "pay" button of native Payment UI.
This trivially happens by holding Enter key for 3 seconds (it takes 3 seconds to fetch all the manifests and scripts).

Payment Handler API requires Service Worker. This Service Worker can also handle fetch events as it was previously possible (good design, right?).

Now, "JIT payment app installation" is made possible by manifest files. And Web App Manifest speficies location of service worker scripts. Long story short, an attacker needs to host/controll following 2 files in victim's origin.

1. Web App Manifest file
2. Service Worker script file

Where both file works even if it responds with `Content-Disposition: attachment`. And Content Type of Web App Manifest file doesn't matter. Service Worker script is sometime easy to have in victim's origin because of JSONP API (which I included in the demo).

So "JIT payment app installation" provides new ability to install service worker without having script execution in victim's origin

Feel free to split the bugs but please CC me so that I know when it's been fixed and where.

Did this work before? N/A 

Chrome version: 69  Channel: canary
OS Version: 10.0
Flash Version:

## Timeline

### s....@gmail.com (2018-06-18)

I think the main discussion we need to have here is:
Is installation of service worker without script execution a thing?

I already confirmed that I can have XSS on at least one site which offers bounty and I'm sure there are more websites affected. And it's not only an XSS but "Service Worker Capability". JIT payment app installation is not a standard feature and I think it deserves more discussion and reviews.

If this has already been discussed, then I'm fine with it. I just need to get bounty from someone else :)

### wf...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Payments]

### s....@gmail.com (2018-06-19)

Oh, spec says to fetch Web App Manifest with mode "cors". So that's at least a bug.
https://www.w3.org/TR/payment-method-manifest/#fetch-wam

But this doesn't make much difference since attacker could also have payment method manifest hosted on victim's origin (since my attack scenario assume that JSON file can be hosted).

### wf...@chromium.org (2018-06-19)

Given preconditions here, I think this probably sounds like a Low, but estark please correct me if I'm wrong.

### s....@gmail.com (2018-06-19)

Hmm, I think this deserves Medium severity. Given preconditions are not that difficult in some websites (most of the websites that allows user uploads to).

### sh...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-06-21)

I am not quite understand this problem.

Recently, I made a change that require web app manifest, script and its registration scope must come from the same origin. Before that the web page created payment request must support that payment method and that payment method manifest must point to the web app manifest.

Could you describe it in more details?

### s....@gmail.com (2018-06-22)

I tested repro step with latest Canary with MAC. You need to enabled following 2 flags (because you made it behind the flag).
#just-in-time-service-worker-payment-app
#service-worker-payment-apps

In websites where attacker can upload JSON and JS files, changes you mentioned in https://crbug.com/chromium/853937#c7 is not enough because attacker can host all mentioned files in victim's domain.

Right now, attacker can register payment method with attacker.com/pay and that responds with `link: <https://victim.com/uploads/payment-manifest.json>; rel="payment-method-manifest"`. This bypasses all the checks available right now.



### s....@gmail.com (2018-06-22)

Dear security folks, you might want to check why cross-origin no-cors JSON fetching is allowed here. This might be potential bypass of CORB.

### go...@chromium.org (2018-06-22)

"Right now, attacker can register payment method with attacker.com/pay and that responds with `link: <https://victim.com/uploads/payment-manifest.json>; rel="payment-method-manifest"`. This bypasses all the checks available right now."

To make sure I understand this correctly. So the content in 'https://victim.com/uploads/payment-manifest.json' is messed by attacker or not? What's the result of that? Install of the victim's service worker Or install of the attacker's service worker (with what scope?).

### s....@gmail.com (2018-06-22)

Attacker uploads `https://victim.com/uploads/payment-manifest.json`, `https://victim.com/uploads/manifest.json`, and `https://victim.com/uploads/sw.js`. This will allow attacker to install Service Worker on victim's domain (without having JS execution in victim's domain).

Right now, even Payment Manifest could be hosted from attacker's domain due to improper CORS check in fetching web app manifest (see https://crbug.com/chromium/853937#c3).

Website like visual studio team services allows user to upload arbitrary file in project's origin. But they protect mis-use of uploaded files by adding `Content-Disposition: attachment` and `X-Frame-Options: Deny` response headers to uploaded files. But it doesn't help in this case because Chrome ignores those headers and let it go through.

### go...@chromium.org (2018-06-22)

Okay, it looks matched my understanding.

I think this should unlikely happen in real world. Payment handler developers should not allow external users have write access to their payment handler JSON and JS files.
Manually install payment handlers (do not use JIT) could also have this problem if they don't verify and protect their JSON and JS files.

### s....@gmail.com (2018-06-22)

You didn't get me. This attack doesn't target Payment App providers. But it target's website who allows uploading files (this can be text file, as I mentioned previously). Because attacker's purpose of uploading those file is to get Service Worker installed and have XSS (though, Payment app can be installed too). Payment method will still be called "attacker.com/pay", but this app will all work in origin of "victim.com".

### go...@chromium.org (2018-06-23)

Ah, get your idea, so you mean attacker may host the JSON and JS file on github, for example, then it gets registered with github origin.

### s....@gmail.com (2018-06-23)

Yes, that's right (though, I don't think Github is vulnerable) :)

### go...@chromium.org (2018-06-23)

Yes, is there websites allow uploading files will provide main origin to access the files, like github requires proceed user name (https://w3c.github.io/payment-handler/).

### s....@gmail.com (2018-06-23)

Just uploaded following example
https://community.ubnt.com/ubnt/attachments/ubnt/EdgeMAX/212666/1/test.txt

This site offers bounty (https://hackerone.com/ubnt).

### go...@chromium.org (2018-06-23)

Then, this could also happen for a normal service worker, right? Attacker can upload service worker installing page to the victim origin. Then somehow direct the user to that page.

### s....@gmail.com (2018-06-23)

>Then, this could also happen for a normal service worker, right?
No, to install Service Worker, you need to have script execution on that origin. Because you need to call `navigator.serviceWorker.register("sw.js")`. This is why this feature brings new attack surface (see https://crbug.com/chromium/853937#c1).

### go...@chromium.org (2018-06-23)

[Comment Deleted]

### s....@gmail.com (2018-06-23)

Because they have `Content-Disposition: attachment` and `X-Frame-Options: Deny` set to all  uploaded file (see https://crbug.com/chromium/853937#c11). How will you render html file with those response header?

### go...@chromium.org (2018-06-23)

yes, is there websites can upload html files and publish them through that origin?

### go...@chromium.org (2018-06-23)

My bad, respond too fast, ignore https://crbug.com/chromium/853937#c20. 

### s....@gmail.com (2018-06-23)

There are sites like "visual studio team services" or "Cybozu.com" which allows uploads of any file in main origin, but I can't show you how because that requires authentication (though, VSTS seems to have public projects). You can try VSTS (https://visualstudio.microsoft.com/team-services/) free and test this if you want.

### go...@chromium.org (2018-06-23)

Thanks for reporting and clarifying these information. 

To sum up:
Attacker can create a fake payment method 'attacker.com/pay' to be used in a website's payment request. When users activate payment request in that website, chrome will fetch the attacker's payment method manifest. In the payment method manifest, it points to a web app manifest hosted on victim's origin. Then, JIT will download the web app manifest and JS from the victim's origin and register that JS in the victim's origin.


### wf...@chromium.org (2018-06-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-23)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-06-23)

+lukasza for https://crbug.com/chromium/853937#c9 (possible CORB bypass)

### es...@chromium.org (2018-06-23)

Adding some other site isolation people because lukasza is OOO. Please see c#9

### lu...@chromium.org (2018-06-25)

s.h.h.n.j.k@, could you please help me understand when you expect CORB to block a response?

Most importantly: Which response should be blocked by CORB?

   - I see that https://crbug.com/chromium/853937#c11 talks about payment-manifest.json and manifest.json.
       - Is one of *these* resources the one you expect to be protected by CORB?
       - It is unclear to me how requests for these 2 resources are initiated
         and who can see the data in the responses?
           - If the browser initiates the requests, then CORB should not block
             the response - the browser should be careful to avoid exposing
             the received data to another origin.
           - If a cross-origin renderer initiates the requests, then CORB should
             indeed block the response.  How is the request initiated in this case?
             How would I go about reproing lack of CORB blocking?

   - Maybe one way to clarify this would be to provide the following details
     about the response you expect to be blocked by CORB?:
       - URL of the requested resource
       - Origin of the request initiator
       - Response headers, in particular: Content-Type and X-Content-Type-Options
       - Does response body sniff as JSON (or is it Javascript and/or HTML and/or something else)?
       - Whether the response data is exposed to Javascript running in another origin
         (VS if the response data is only consumed by the browser / network stack)


Thank you for the report and your patience helping with understanding all the details.

### s....@gmail.com (2018-06-25)

> - I see that https://crbug.com/chromium/853937#c11 talks about payment-manifest.json and manifest.json.
> - Is one of *these* resources the one you expect to be protected by CORB?
Yes, I was suspecting both or either of them.

> - If the browser initiates the requests, then CORB should not block
> the response - the browser should be careful to avoid exposing
> the received data to another origin.
Those are most probably browser initiated requests. So this is most probably not a CORB bypass. I researched a bit but I couldn't find a way to leak cross-origin JSON content too.

Sorry for the false alarm :(

### go...@chromium.org (2018-06-27)

Remove payment handler blocking label since JIT has been put behind flag and disabled by default in >= M68. 

### ab...@google.com (2018-07-03)

Bulk update: M68 stable cut is scheduled for July 19th. This issue is marked as RB-Stable, so please take a look at it before. Thanks!

### ma...@chromium.org (2018-07-03)

As per comment in https://crbug.com/chromium/853937#c33 as well as my own confirmation, we've disabled this feature in M68 via the code (merged) as well as through Finch.

### sh...@chromium.org (2018-07-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-07-09)

The feature is disabled in M-68, so remove it from release blocker,

### sh...@chromium.org (2018-07-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/562da5192ff110199fe290bdb7ea76d8118071fd

commit 562da5192ff110199fe290bdb7ea76d8118071fd
Author: gogerald <gogerald@google.com>
Date: Tue Jul 10 21:20:09 2018

[Payments] Restrict just-in-time payment handler to payment method domain and its subdomains

Bug: 853937
Change-Id: I148b3d96950a9d90fa362e580e9593caa6b92a36
Reviewed-on: https://chromium-review.googlesource.com/1132116
Reviewed-by: Mathieu Perreault <mathp@chromium.org>
Commit-Queue: Ganggui Tang <gogerald@chromium.org>
Cr-Commit-Position: refs/heads/master@{#573911}
[modify] https://crrev.com/562da5192ff110199fe290bdb7ea76d8118071fd/components/payments/content/installable_payment_app_crawler.cc


### go...@chromium.org (2018-07-11)

The fix is small and only affects the feature behind the flag, so trying to merge it to M68.

Verified in Canary,

### sh...@chromium.org (2018-07-11)

This bug requires manual review: We are only 12 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-13)

gogerald@ - looks like the relevant flags aren't set to be enabled in M68, is that the case, or are there plans for a stable field trial in 68?

### go...@chromium.org (2018-07-13)

I was hoping to trial it in M68, but we have an upcoming minor change, so move it to M69, thanks

### aw...@chromium.org (2018-07-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-07-23)

Hi s.h.h.n.j.k@ - the VRP panel decided to award $3,000 for this report.  Cheers!

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-23)

Thanks!

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2018-11-28)

I looked at https://chromium-review.googlesource.com/c/chromium/src/+/1132116/ and noticed that there was no discussion of why the payment handler restriction would be scoped to same-site and not same-origin.

I'm concerned about this because it allows XSS and SW installation within the site boundary if the vulnerable origin hosts any user-uploaded content (even if file uploads are delivered with headers that would prevent the content from being rendered/executed, e.g. C-D: attachment, CSP: sandbox, etc.). There are some major application ecosystems where this is possible.

Can we change InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed to apply a restriction to same-origin instead?

### sh...@chromium.org (2018-11-28)

gogerald: Uh oh! This issue still open and hasn't been updated in the last 137 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2018-11-28)

We're discussing this over email.

### sh...@chromium.org (2018-11-28)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ro...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/853937?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091693)*
