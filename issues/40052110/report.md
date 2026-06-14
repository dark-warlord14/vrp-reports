# Security: javascript URI sandbox flags aren't propagated in a blank string case

| Field | Value |
|-------|-------|
| **Issue ID** | [40052110](https://issues.chromium.org/issues/40052110) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2020-04-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Iframe sandbox flags aren't propagated to the child frame document load for a javascript:'' URI's. This only seems to reproduce with a blank string initial JavaScript URI in an iframes src attribute.

I haven't tested on many variants of Chrome however I can see this is a change since Chromium 70, but I think this issue happened in Chrome 80.  

I can see that Chrome inspector considers the scope of the Iframe as the same origin, where as previously it was considered as about:blank.

Looking through the code I notice that:

- The flags are being parsed correctly and attached to the HTMLFrameOwnerElement::SetSandboxFlags()
- just after document construction `FrameLoader::EffectiveSandboxFlags()` is called and doesn't appear to have an opener with the flags set on it. (Printing out frame\_owner\_sandbox\_flags\_.value() you see the value getting dropped through frame construction)

**VERSION**  

Chrome Version: 81.0.4044.113 (Official Build) (64-bit) reproduces on Brave Version 1.7.92 Chromium: 80.0.3987.163 (Official Build) (64-bit) also.  

Operating System: Mac and Ubuntu 18.04.4 LTS

**REPRODUCTION CASE**

I have attached a proof of concept of the issue but also inline, you will notice in older Chrome the alert doesn't fire and the location isn't changed.

1. A frame is set to having javascript:""
2. Sandboxing flags are set on the frame such that modals and location changes are prevented. (allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation allow-presentation)
3. The onload event immediately writes to the frames document a new document which runs JavaScript

This code is used in advert delivery platforms, however the expectation is that the advert provider can prevent navigations. Unfortunately I don't think they are able to change the URI due to breakage/legacy reasons.

The issue also reproduces with "allow-top-navigation". The issue doesn't appear to reproduce in any other browser that isn't Chromium based and I don't see any intentional changes to Web Platform Tests to explain the breakage.

<html>
<body>
<iframe
src="javascript:''"
onload="this.contentWindow.document.write(`<body><script type='text/javascript' >(function() {alert(1); top.location.href = 'https://example.com'; })()</script></body>`)"
sandbox="allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation allow-presentation"
>
</iframe>
</body>
</html>

**CREDIT INFORMATION**

Reporter credit: Jonathan Kingston

## Attachments

- [index.html](attachments/index.html) (text/plain, 389 B)

## Timeline

### me...@chromium.org (2020-04-24)

Thanks for the report.

I bisected this change to the range https://chromium.googlesource.com/chromium/src/+log/2b7dac61d81a4e22f28fdf0aea74ec3f04da7025..7d9fc47ce1698df5a821ff8189837f470dfe5134

The only relevant CL is https://chromium.googlesource.com/chromium/src/+/1ed633c70656732739018bbfb5e3bff77ac60d79

chenleihu@, can you please take a look as the owner of this CL?

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### ch...@google.com (2020-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-25)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2020-04-27)

[Empty comment from Monorail migration]

### ki...@gmail.com (2020-04-27)

This also applies to URL encoded JavaScript that returns a non zero value:

<iframe src="javascript:(function()%20%7B%20return%20decodeURIComponent(%22%253Cbody%253E%253Cscript%2520type%253D%2522text%252Fjavascript%2522%253E(function()%2520%257Balert(1)%253B%2520top.location%2520%253D%2520'https%253A%252F%252Fexample.com'%253B%257D)()%253C%252Fscript%253E%253C%252Fbody%253E%22)%7D)()"
sandbox="allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation allow-presentation"
></iframe>


The same seems to apply with: `srcdoc='<script type="application/javascript">document.write(<javascript uri contents>)</script>'`

### ki...@gmail.com (2020-04-27)

Sorry the *same doesn't seem to apply* with srcdoc. (I'm working on using this as a mitigation).

The bug title probably needs to be changed to reflect the wider scope of the issue.

### dt...@chromium.org (2020-05-04)

[Empty comment from Monorail migration]

### ch...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### ch...@google.com (2020-05-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/45bcb4d547a5efecae80f4c9a48cef854af91d7f

commit 45bcb4d547a5efecae80f4c9a48cef854af91d7f
Author: Charlie Hu <chenleihu@google.com>
Date: Mon May 11 17:05:21 2020

Fix uninitialized frame policy issue in javascript url

This CL follows up the previous CL that fixed the timing bug on
frame policy(https://chromium-review.googlesource.com/c/chromium/src/+/1852905).

There was a uncovered code path for subframe navigation where frame
policy is not initialized.

Bug: 1074340
Change-Id: I3840cd5a4f8b18f0976b164e5c768ad56eb6e492
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2181318
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Commit-Queue: Charlie Hu <chenleihu@google.com>
Cr-Commit-Position: refs/heads/master@{#767358}

[modify] https://crrev.com/45bcb4d547a5efecae80f4c9a48cef854af91d7f/third_party/blink/renderer/bindings/core/v8/script_controller.cc


### [Deleted User] (2020-05-11)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-21)

Congrats! The Panel decided to award $1,000 for this report

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c46b9cb16595c8385f563599b845cbe799c7e184

commit c46b9cb16595c8385f563599b845cbe799c7e184
Author: Charlie Hu <chenleihu@google.com>
Date: Tue Dec 15 18:39:51 2020

[Frame Policy] Add test to verify frame policy works correctly in javascript url

Previous fix(https://chromium-review.googlesource.com/c/chromium/src/+/2181318)
on uninitialized frame policy in javascript url
navigation does not include a test case because it is a security
fix.

Since the fix has landed in M84 which is stable right now, this CL
adds the test case for the fix.

Bug: 1074340
Change-Id: Ia10a972183b02cdac28a2f29cabb7f13caf168e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2297708
Commit-Queue: Charlie Hu <chenleihu@google.com>
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Cr-Commit-Position: refs/heads/master@{#837169}

[add] https://crrev.com/c46b9cb16595c8385f563599b845cbe799c7e184/third_party/blink/web_tests/external/wpt/permissions-policy/permissions-policy-javascript-url-frame-policy.https.html


### is...@google.com (2020-12-15)

This issue was migrated from crbug.com/chromium/1074340?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052110)*
