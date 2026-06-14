# Security: uXSS in Chrome on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40091336](https://issues.chromium.org/issues/40091336) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | iOS |
| **Reporter** | th...@inbox.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2018-05-09 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Universal XSS by using "..;@" within the url :~D

**VERSION**  

Chrome Version: [66.0.3359.122] + [stable]  

Operating System: [iOS]

**REPRODUCTION CASE**

Basically if we run this javascript code " history.replaceState('','','..;@www.google.com:%3443/') " from any domain using "HTTPS:" our URL domain is being replaced to that one..

For example: if this code is run on my site <https://web-safety.net/> the the url is being replaced to <https://www.google.com> yet the contents remain under my control.. Therefore etc. we can run unrestricted XHR requests as long as the path is not absolute ('../myAccountInfo','../../SomeOtherSensitiveInformation')

Proof of Concept displaying Cookies in an iframe from <https://www.google.com>  

<https://web-safety.net/uxss_ios.html>

This should work fine on any iOS on Chrome

Hope you like it! :~D

Cheers  

Tom

## Attachments

- [01.jpg](attachments/01.jpg) (image/jpeg, 123.7 KB)
- [02.jpg](attachments/02.jpg) (image/jpeg, 666.5 KB)
- [03.jpg](attachments/03.jpg) (image/jpeg, 701.6 KB)
- [04.jpg](attachments/04.jpg) (image/jpeg, 435.1 KB)

## Timeline

### el...@chromium.org (2018-05-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-05-09)

eugenebut: Could you take a look at this?

I don't have an iOS device to test with, so leaving Unconfirmed but applying the labels as if it were for tracking.

[Monorail components: Mobile>WebView>Glue UI>Browser>Mobile]

### eu...@chromium.org (2018-05-09)

thomi@, is this bug reproducible in Safari or Firefox?

### eu...@chromium.org (2018-05-09)

This is a URL spoofing bug, where omnibox URL is incorrectly displayed. But I don't see XSS and "This are your cookies from 'www.google.com': don't print cookies.

### th...@inbox.com (2018-05-09)

Hey!
First.. Make sure you got some cookies already from www.google.com in the first place in case you are using incognito ;)
Secondly make sure you are accessing my PoC over HTTPS! Otherwise it will not work as the Origin does not mach HTTP..

Thirdly it's kind of weird.. if you do alert(document.domain) it will come back as: www.google.com says: web-safety.net
Yet we have access to cookies and we can do unrestricted XHR requests...

Do you want different types of examples of PoC?

### th...@inbox.com (2018-05-09)

Also this PoC only works on Chrome on iOS...
There are different ways to achieve that on other browsers on iOS or Safari on Mac but I think is irrelevant as this subject only focuses on Chrome.. Right?

### el...@chromium.org (2018-05-09)

It would be helpful if you could include screenshots of your reproduction.

(We are interested in understanding whether this reproduces in Safari and Firefox on iOS to better understand whether the root cause of the bug is in WebKit, or in WKWebView, or in Chrome code, which will help speed up the triage process).

### eu...@chromium.org (2018-05-09)

Firefox crashes and I can reproduce this bug in stock WKWebView by executing very short JavaScript. rdar://40109702

Danyao, could you please take a look if this is something you or Ali can fix in WebKit? All the information is available with rdar://40109702.

Pink, could you please escalate this bug with Apple.

I will think if we can workaround the issue.

### th...@inbox.com (2018-05-10)

Here is a new Proof of Concept: https://web-safety.net/uxss_poc.html
Works on Chrome on iOS only...

Also I have attached screenshots what comes up on my screen.

Do you still want to me to create another PoC for Safari? Or you don't need it anymore?

### pi...@chromium.org (2018-05-10)

Yes please create a PoC for Safari. It will help with our discussions with Apple. 

### pi...@chromium.org (2018-05-10)

I escalated to our ADR team. 

### eu...@chromium.org (2018-05-10)

Thank you Tomasz! It looks like some time is needed for XSS attack to steal cookie from iframe. As a workaround we could crash the browser once we detect the attack.

In your previous comment you mentioned that the vulnerability also allows to perform unrestricted XHR. Do you think it would be possible to execute XHR-based attack faster than iframe-based attack? Crashing the browser will limit the time available for the attack to succeed.

### eu...@chromium.org (2018-05-10)

Developed a workaround to crash when URL change is detected. The crash will reduce the time available for this attack, which should either mitigate or make the attack impractical. The fix will be landed behind the finch flag: crrev.com/c/1054196

### pi...@chromium.org (2018-05-10)

We briefly discussed in OH if this ever could happen for legitimate sites. What's the risk or likelihood of that?

### pi...@chromium.org (2018-05-10)

+mardini as FYI

### eu...@chromium.org (2018-05-10)

I believe it's unlikely that legitimate web sites would execute "history.replaceState('','','..;@another_domain/')" script. The crash will be launched behind the flag, so I guess we'll see if legitimate web sites crash.

### th...@inbox.com (2018-05-10)

So.. Here is PoC that should work on Safari on MacOS as well as on all other iOS based browsers (Safari, Firefox, Edge etc.) apart from Chrome iOS:
https://web-safety.net/uxss_poc_safari.html

I got a weird feeling that "history.replaceState" might not be the only way for this uXSS to work.. But I am not an expert ;)

Anyways.. Don't forget that this bug also allows for unrestricted open redirection on all domains as well.. Long story short, thanks to this I was able to find 4 XSS on *.google.com, yet guys said that those are not valid bugs as it's a browser bug in relation to open redirection..
Example: Some data URL is being controlled.. https://someService.googleapis.com/..;@custom_domain.com/

Let me know if I can help you in any way.. :)



### eu...@chromium.org (2018-05-10)

Just to clarify comments #13 and #16. The workaround is to crash only if URL's password or username contains the origin of the previous URL. The crash is targeted specifically for this vulnerability and should not affect legitimate web sites. 

### th...@inbox.com (2018-05-10)

I guess this solution should do the trick..
Also XHR request takes a while too.. might be even longer than iframe + innerHTML to it.

### eu...@chromium.org (2018-05-10)

Thanks Tomasz! I don't think Chrome can do better than crashing. The real fix should be done in WebKit.

### pi...@chromium.org (2018-05-11)

Eugene, can you make sure the radar has the Safari info in it? That's our best avenue to getting apple to pay attention. 

### eu...@chromium.org (2018-05-11)

Updated rdar://

### el...@chromium.org (2018-05-11)

Continuing the conversation from https://chromium-review.googlesource.com/c/chromium/src/+/1054196/2/ios/web/web_state/ui/crw_web_controller.mm#5199

If (_documentURL.GetOrigin() != newURL.GetOrigin()) inside URLDidChangeWithoutDocumentChange, isn't that *alone* enough to indicate that we're in an exploitable situation? Is there any scenario in which having a document's origin mismatch the URL's origin isn't a vulnerability?

### eu...@chromium.org (2018-05-11)

|If (_documentURL.GetOrigin() != newURL.GetOrigin())| is more broad than the check in the CL. _documentURL detection in Chrome is not 100% reliable and using more broad check can lead to crashes during legitimate navigations (so yes, there are scenarios when _documentURL may be incorrect for a brief period of time). We working on refactoring navigation stack to improve _documentURL detection.



### da...@chromium.org (2018-05-15)

CC a couple of Apple security folks.

The bug is seems to be an error in URL parsing. Within WebKit, "https://web-safety.net/..;..;@mobile.twitter.com/robots.txt" is parsed correctly into the following parts:
- host: "web-safety.net"
- path: "/..;..;@mobile.twitter.com/robots.txt"
- user: ""
- password: ""

However, when this URL is sent to the network layer, the data returned is from https://mobile.twitter.com/robots.txt. So I suspect the error happens when the URL is serialized in the WebKit -> NetworkProcess IPC, and when reparsed, it is interpreted differently.

Maybe WebKit should escape ";" and "@" when processing replace state URLs. This seems to be what happens when "https://web-safety.net/..;..;@mobile.twitter.com/robots.txt" is entered directly into the address bar in iOS Safari.

Does anyone know what Blink does?


### dd...@apple.com (2018-05-15)

Tracking internally at Apple as: <rdar://problem/40258457>


### bu...@chromium.org (2018-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ba1815a412382038e41adc189134fcb1b75784aa

commit ba1815a412382038e41adc189134fcb1b75784aa
Author: Eugene But <eugenebut@google.com>
Date: Tue May 15 17:12:35 2018

Crash on unexpected URL change.

Bug: 841105
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: I4471a98cdef13e54b790ebcd565d59c67dba8bfd
Reviewed-on: https://chromium-review.googlesource.com/1054196
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#558760}
[modify] https://crrev.com/ba1815a412382038e41adc189134fcb1b75784aa/ios/web/features.mm
[modify] https://crrev.com/ba1815a412382038e41adc189134fcb1b75784aa/ios/web/public/features.h
[modify] https://crrev.com/ba1815a412382038e41adc189134fcb1b75784aa/ios/web/web_state/ui/crw_web_controller.mm


### eu...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-15)

This bug requires manual review: Less than 10 days to go before AppStore submit on M67
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pi...@chromium.org (2018-05-15)

Should we leave this open as ExternalDependency, since we probably want to remove the force-crashing when Apple fixes the bug for real? That, or file a new bug to track it.

### ka...@chromium.org (2018-05-15)

Can we get unit tests please? Also how confident are you in this fix, Eugene?

### ka...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-05-15)

Marking as ExternalDependency, because the code references this bug.

No, we can not write unit tests which verify that the app crashes. This is a risky fix which can introduce new crashes, but the change is behind the flag which can be turned off  on the server. Given the severity of this bug I believe we have to merge this to M67 per Security_Severity-High SLA.

### ka...@chromium.org (2018-05-15)

Approving per the high security severity and the fact that the change is behind a flag. Please merge asap.

### bu...@chromium.org (2018-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/763ba59928da808a9b3f0da1ac777122f33507d3

commit 763ba59928da808a9b3f0da1ac777122f33507d3
Author: Eugene But <eugenebut@google.com>
Date: Tue May 15 20:44:48 2018

Crash on unexpected URL change.

TBR=eugenebut@google.com

(cherry picked from commit ba1815a412382038e41adc189134fcb1b75784aa)

Bug: 841105
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: I4471a98cdef13e54b790ebcd565d59c67dba8bfd
Reviewed-on: https://chromium-review.googlesource.com/1054196
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#558760}
Reviewed-on: https://chromium-review.googlesource.com/1060377
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#609}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/763ba59928da808a9b3f0da1ac777122f33507d3/ios/web/features.mm
[modify] https://crrev.com/763ba59928da808a9b3f0da1ac777122f33507d3/ios/web/public/features.h
[modify] https://crrev.com/763ba59928da808a9b3f0da1ac777122f33507d3/ios/web/web_state/ui/crw_web_controller.mm


### eu...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-16)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-05-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-05-23)

[Empty comment from Monorail migration]

### sr...@chromium.org (2018-05-23)

Verified in M67.0.3396.57 beta
iOS: 11.4 beta#6, 11.3.1, 11.2.6
Devices: iPhoneX, iPad Pro, iPhone8

App crashes as soon as the test URL from initial report is opened.

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sr...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### li...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### mp...@chromium.org (2018-06-01)

Re-opening this bug.  eugenebut@ can explain why.

### eu...@chromium.org (2018-06-01)

The workaround had non-trivial amount of false positive crashes. We will disable the workaround in M67 with Finch kill switch until we deal we those crashes.

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Congratulations thomi@! The Chrome VRP panel decided to award $7,500 for this report.

Note that we usually only reward once the bug has been fixed, and this one just reopened, but in this case I'm going to process it now anyway.

 

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-06-05)

We fixed false positive crashes and shipped refresh build to AppStore. Finch kill switch was not used.

### sh...@chromium.org (2018-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/841105?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091336)*
