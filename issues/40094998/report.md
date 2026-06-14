# Security: Security: Same Origin Policy bypass and local file disclosure via <portal> element

| Field | Value |
|-------|-------|
| **Issue ID** | [40094998](https://issues.chromium.org/issues/40094998) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Portals, UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | lf...@chromium.org |
| **Created** | 2019-05-13 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

The new <portal> elements contains a security issue that makes it possible to bypass SOP as well as to read local files.

This happens when a "javascript:" URI is assigned to <portal> src attribute. Chromium then behaves as if the user manually entered the "javascript:" URI in the address bar, executing the code in the context of the current <portal> origin.

So the general idea is:

const p = document.createElement('portal');  

p.src = '<https://mail.google.com>';  

// after a while:  

p.src = 'javascript:portalHost.postMessage(document.documentElement.outerHTML,"\*")';  

// the code above will get executed in the context of <https://mail.google.com>

The another, probably separate issue is that you can assign arbitrary schemes to <portal>.src, for instance "file:///" or "chrome:///flags".

**VERSION**  

Chrome Version: 76.0.3793.0 Canary + chrome://flags/#enable-portals enabled  

Operating System: macOS 10.14.4

**REPRODUCTION CASE**  

Please see the attachment and press "Go", "/etc/passwd" or Google. It loads the content of a given URL in portal, and then assigns a javascript URI.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Michal Bentkowski

## Attachments

- [exploit.html](attachments/exploit.html) (text/plain, 849 B)

## Timeline

### va...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>HTML>Portal]

### lf...@chromium.org (2019-05-13)

Marking it as no impact since this feature is not launched.

### lf...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### lf...@chromium.org (2019-05-14)

[Empty comment from Monorail migration]

### lf...@chromium.org (2019-05-15)

[Empty comment from Monorail migration]

### dc...@chromium.org (2019-05-15)

[Empty comment from Monorail migration]

### dc...@chromium.org (2019-05-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2019-05-15)

Thanks for the report!  It will be very important to get the right restrictions in place for which URLs a portal can be told to navigate to, since it's a different security model than most GuestViews (where the embedder is assumed to have more control over the guest).

[Monorail components: UI>Browser>Navigation]

### dc...@chromium.org (2019-05-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-05-17)

If this can really read arbitrary local files, maybe it should be Critical severity? (The severity guidelines, https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md, only talk about code execution, but that may be too limited?)

### pa...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/69ec73d0fabce5b339b0b125fc60f6722e7e958d

commit 69ec73d0fabce5b339b0b125fc60f6722e7e958d
Author: Lucas Furukawa Gadani <lfg@chromium.org>
Date: Fri May 17 18:15:09 2019

Portals: Restrict portal navigations to HTTP family.

This is also enforced with a renderer kill in case the browser receives
a non-HTTP navigation request.

Bug: 962500
Change-Id: Id7c122ba80ef1cc00620d07d5ecdb1f268b04d79
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1615499
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#660918}

[modify] https://crrev.com/69ec73d0fabce5b339b0b125fc60f6722e7e958d/content/browser/portal/portal.cc
[modify] https://crrev.com/69ec73d0fabce5b339b0b125fc60f6722e7e958d/content/browser/portal/portal_browsertest.cc
[modify] https://crrev.com/69ec73d0fabce5b339b0b125fc60f6722e7e958d/third_party/blink/renderer/core/html/portal/html_portal_element.cc


### lf...@chromium.org (2019-05-17)

This should fix the major issue of being able to navigate to chrome:, data:, blob: and javascript: URLs. We'll follow up on adding further restrictions in https://crbug.com/chromium/964395.

Since the feature isn't launched, we don't need to merge the fixes.


### mp...@google.com (2019-05-17)

Marking as critical due to arbitrary file access, which along with file write is one of the biggest reasons we don't want to allow arbitrary code execution in the first place.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/53511d46a059446be0913c208f24b313d050c932

commit 53511d46a059446be0913c208f24b313d050c932
Author: Lucas Furukawa Gadani <lfg@chromium.org>
Date: Fri May 17 20:46:06 2019

Portals: Add test that portals can't load data, javascript or about URLs.

Bug: 962500
Change-Id: Ib5e275a7f31be3a7e24dfc7bf976b6e2866624fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1614703
Commit-Queue: Lucas Gadani <lfg@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#661004}

[add] https://crrev.com/53511d46a059446be0913c208f24b313d050c932/third_party/blink/web_tests/external/wpt/portals/portal-non-http-navigation.html


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3cfbfbc2cade4a00360638810392fedbabcc7392

commit 3cfbfbc2cade4a00360638810392fedbabcc7392
Author: Findit <findit-for-me@appspot.gserviceaccount.com>
Date: Sat May 18 00:48:48 2019

Revert "Portals: Restrict portal navigations to HTTP family."

This reverts commit 69ec73d0fabce5b339b0b125fc60f6722e7e958d.

Reason for revert:

Findit (https://goo.gl/kROfz5) identified CL at revision 660918 as the
culprit for flakes in the build cycles as shown on:
https://analysis.chromium.org/p/chromium/flake-portal/analysis/culprit?key=ag9zfmZpbmRpdC1mb3ItbWVyQwsSDEZsYWtlQ3VscHJpdCIxY2hyb21pdW0vNjllYzczZDBmYWJjZTViMzM5YjBiMTI1ZmM2MGY2NzIyZTdlOTU4ZAw

Sample Failed Build: https://ci.chromium.org/buildbot/chromium.memory/Linux%20ChromiumOS%20MSan%20Tests/12979

Sample Failed Step: viz_content_browsertests

Sample Flaky Test: PortalBrowserTest.NavigateToChrome

Original change's description:
> Portals: Restrict portal navigations to HTTP family.
> 
> This is also enforced with a renderer kill in case the browser receives
> a non-HTTP navigation request.
> 
> Bug: 962500
> Change-Id: Id7c122ba80ef1cc00620d07d5ecdb1f268b04d79
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1615499
> Commit-Queue: Lucas Gadani <lfg@chromium.org>
> Reviewed-by: Charlie Reis <creis@chromium.org>
> Reviewed-by: Jeremy Roman <jbroman@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#660918}


Change-Id: I3322c1b1721eca98d08ce9b39f2363cf23b424b5
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 962500
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1618315
Cr-Commit-Position: refs/heads/master@{#661127}

[modify] https://crrev.com/3cfbfbc2cade4a00360638810392fedbabcc7392/content/browser/portal/portal.cc
[modify] https://crrev.com/3cfbfbc2cade4a00360638810392fedbabcc7392/content/browser/portal/portal_browsertest.cc
[modify] https://crrev.com/3cfbfbc2cade4a00360638810392fedbabcc7392/third_party/blink/renderer/core/html/portal/html_portal_element.cc


### sh...@chromium.org (2019-05-18)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-05-20)

is this fixed? It looks like the CL was reverted. Preemptively re-opening. Please close again if I'm wrong.

### pa...@chromium.org (2019-05-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-05-21)

(Moving view restrictions back to Restrict-View-SecurityNotify since this some folk got notifications and then lost access: note it's Security_Impact-None)

### [Deleted User] (2019-05-21)

Adding venkatk@microsoft.com to ensure it's portd to Edge.

### mi...@bentkowski.info (2019-05-26)

For the record: I verified that the issue is fixed in 76.0.3805.0.

### lf...@chromium.org (2019-05-27)

Yes, the fix relanded in https://chromium-review.googlesource.com/c/chromium/src/+/1621871, bugdroid must be on holidays.


### na...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-29)

Congrats! The Panel decided to reward $10,000 for this report 

### mi...@bentkowski.info (2019-05-30)

That is nice, thanks!

### mi...@bentkowski.info (2019-05-30)

And also - this Monday I'd like to have a presentation on Confidence conference (https://confidence-conference.org/2019/krakow.html) in which I'd like to say a few words about <portal> in a so-called Community Corner. Assuming that this bug is already fixed and was present only in Canary and behind the flag, is that okay for you to talk about it?

### pa...@google.com (2019-05-30)

+awhalley and +adetaylor explicitly for the question in #28.

### aw...@google.com (2019-05-31)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-06-01)

michael@bentkowski.info - sorry for the late reply to https://crbug.com/chromium/962500#c28 but I wanted to do some checks before replying. Yes - that's fine - you can talk about this bug. Thanks again for the report!

### lf...@chromium.org (2019-07-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jb...@chromium.org (2019-11-27)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-07)

lfg@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-03-16)

Was the test from https://chromium-review.googlesource.com/c/chromium/src/+/1614703 ever relanded?

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### is...@google.com (2020-10-12)

This issue was migrated from crbug.com/chromium/962500?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Portals, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/963162, crbug.com/chromium/963553, crbug.com/chromium/969700, crbug.com/chromium/987261]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094998)*
