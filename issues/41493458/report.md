# Security: `Android` Top-level redirect from cross-origin iframe by setting `Content-Security-Policy: sandbox allow-top-navigation` Bypass of Issue 1251790

| Field | Value |
|-------|-------|
| **Issue ID** | [41493458](https://issues.chromium.org/issues/41493458) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>PopupBlocker |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | lb...@google.com |
| **Created** | 2024-01-22 |
| **Bounty** | $3,000.00 |

## Description

# **VULNERABILITY DETAILS**

After Fixing <https://crbug.com/chromium/1251790> , i've found that this bug come back in Chrome for Android, Regression of <https://crbug.com/chromium/1251790> .

Top-level redirect possible from cross-origin iframe without user-interaction by setting this header `Content-Security-Policy: sandbox allow-top-navigation` in the response.

This bypasses the patch for <https://crbug.com/1145553>

# **VERSION**

Chrome Version: 122.0.6256.0  

Channel:Canary  

OS: Android 14; Pixel6 Device

# Bisection `Fix of main Issue`:

[1] <https://chromium-review.googlesource.com/c/chromium/src/+/3842458>  

[2] <https://chromium-review.googlesource.com/c/chromium/src/+/2688360>

# **REPRODUCTION CASE** :

app.py

```
#!/usr/bin/env python3  
from flask import Flask, Response  
  
app = Flask(__name__)  
  
@app.route("/test")  
def test():  
    resp = Response("""  
    <script>  
        top.location = "https://google.com";  
    </script>  
    """, mimetype="text/html")  
    resp.headers["Content-Security-Policy"] = "sandbox allow-top-navigation allow-scripts"  
    return resp  
  
app.run(host="0.0.0.0", debug=True)  

```

once the flask app is started any page that embeds <http://localhost:5000/test> should be redirected to <https://google.com> , which have LIVE URL "  

<https://painted-dandelion-juravenator.glitch.me/demo?sandbox_header=1>" .

# Simple Reproduction with Live Poc

in Android make sure before repro make sure of these points  

1- open chrome canary in android and press three vertical dots to open dropdown menu  

2- Select Settings , then Under `Advanced` part select `Site Settings`  

3- Scroll down under `Content >> Popups and redirects` should be blocked just check this .

# Repro Steps:

1-Navigate to <https://foggy-malleable-land.glitch.me/demo> or <https://vrphunt.com/chrome/android/csp-par.html>  

2-Click on button `Iframe site showing intended behavior` you will see redirection happens  

3-Click on button `Iframe site showing bypass` you will see redirection also happens

## Hints:

in the url `https://painted-dandelion-juravenator.glitch.me/demo?sandbox_header=1` embedded inside live poc which redirects to google.com , this url has header `Content-Security-Policy: sandbox allow-top-navigation` in the response , and this embedded file content is

```
  <script>  
    top.location = "https://google.com";  
  </script>  
    

```

============

What is wrong and what is intended ?

In Chrome for Desktop the fix has landed and Stop iframes from allowing themselves to navigate top without gesture , and showing "Redirect blocked" message , But in Android this bug is found again and redirection happens.

++You Can Also Repro in Chrome for Desktop and see the difference in Action , which will help.

## ==================== **CREDIT INFORMATION**

Reporter credit: Ahmed ElMasry

## Attachments

- [csp-par.html](attachments/csp-par.html) (text/plain, 439 B)
- [poc-canary-csp_22012024_155106_7501.mp4](attachments/poc-canary-csp_22012024_155106_7501.mp4) (video/mp4, 2.8 MB)

## Timeline

### [Deleted User] (2024-01-22)

[Empty comment from Monorail migration]

### ke...@chromium.org (2024-01-24)

Thanks for the report.

You are reporting this as a regression on Canary but the behaviour on Stable seems to match. Is there a difference that I am missing?

jkarlin@: Are you able to take a look at this or pass it on to someone who can? I've set the flags to match https://crbug.com/chromium/1251790.

[Monorail components: UI>Browser>PopupBlocker]

### am...@chromium.org (2024-01-29)

The version number presented in the original report appears to just be the Chrome version the reporter was using when reporting this issue and not a recent regression.
Setting to FoundIn-120 since this is current Extended Stable / oldest active release channel and adding other folks relevant to past work to cc: 


### [Deleted User] (2024-01-29)

[Empty comment from Monorail migration]

### jk...@chromium.org (2024-01-29)

Liam, PTAL, thanks!

### lb...@google.com (2024-01-29)

I was able to reproduce on Chrome stable running on a stock Android device. Going to take a closer look to see what the underlying issue is.

### lb...@google.com (2024-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lb...@google.com (2024-01-30)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-30)

[Empty comment from Monorail migration]

### lb...@google.com (2024-02-01)

Thanks everyone for your patience while I looked into this. I think I found the culprit. This has to do with how user activation interacts with site isolation (more specifically the lack of site isolation).

The problem:

If site isolation is enabled (which we do on platforms with more resources), a cross-origin navigation results in a whole new renderer process being created. In the demo page linked, the iframe starts out not navigated to any page, and then navigates to a cross-origin page (not a cross-site page, which will be important further down the line), which results in a new process being created for the now out-of-process iframe (OOPIF).

If site isolation is NOT enabled (which we do on lower-resource platforms like Android), the existing process is re-used when the iframe does that cross-origin navigation, and the iframe doesn't become an OOPIF.

Before the iframe does its initial navigation, it is considered to be same-origin to its embedder. When you click in a page, that page gets user activation, and any same-origin subframes also get user activation. So for this demo page, clicking on the main page will give that un-navigated iframe user activation. This includes when you click on the button to navigate the iframe, since at that point the iframe still hasn't done its navigation.

Here's where the problem arises. If an iframe navigates and reuses its process, the old user activation state will be reused as well, including "sticky" user activation (i.e. a bit that tracks if a user interacted with a page at least once during its lifetime). So even though the user never clicked in this newly navigated page, it *thinks* the user did, because there's a leftover bit from the previous page.

This problem is manifesting in the form of our framebusting interventions because they check user activation to determine if a frame can do a top-level navigation, and in this case, the user activation state is kept from the previous page that had just received a legitimate user activation event.

The solution:

The most obvious fix would be to clear user activation states whenever a navigation happens. However, that has been tried in the past, and ended up breaking a legacy PayPal payment system (see: https://bugs.chromium.org/p/chromium/issues/detail?id=1336672#c48). This payment system specifically relies on keeping user activation state as it navigates a fenced frame to a cross-origin page (same site, different subdomain), so we can't clear for cross-origin navigations either.

The best we can do, which should also fix this regression, is to clear user activation state on a cross-site navigation. That means that an A.com -> B.com navigation will clear user activation, but an A.com -> subdomain.A.com navigation will not.

### lb...@google.com (2024-02-01)

I just realized I wrote "fenced frame" in the last message when I meant "iframe". It should read "This payment system specifically relies on keeping user activation state as it navigates an iframe to a cross-origin page".

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1520485?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### lb...@google.com (2024-02-15)

Update: The fix is in review, and I'm hoping to get the necessary approvals to submit it before I leave for vacation next week. If that timeline slips, averge@ has agreed to take over the CL while I'm OOO.

### pe...@google.com (2024-03-02)

lbrady: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### av...@chromium.org (2024-03-04)

Providing an update on Liam's behalf:

The [CL](https://crrev.com/c/5269464?tab=comments) to fix this has gone through a couple more rounds of comments. The primary blocker is further review and approval by CSA, but some folks were OOO recently.

[creis@chromium.org](mailto:creis@chromium.org), [alexmos@chromium.org](mailto:alexmos@chromium.org), do you have some time this coming week for another review pass?

### ap...@google.com (2024-03-07)

Project: chromium/src
Branch: main

commit 38b84561d09e8f061ecd69623f90435c19a37792
Author: Liam Brady <lbrady@google.com>
Date:   Thu Mar 07 22:11:26 2024

    Clear user activation on cross-site navigations.
    
    When full site isolation is disabled, renderer processes and
    RenderFrameHosts are re-used when performing cross-site navigations.
    This includes user activation state, and, more specifically, the sticky
    `has_been_active_` bit in `UserActivationState`.
    
    Currently, the `UserActivationState` on the renderer-side is reset only
    if the navigation's associated frame is a main frame. That means that if
    an iframe navigates to a cross-site page, its sticky user activation
    state will be the leftover state from the previous page. So, if a user
    interacted with the previous page in any capacity, the newly loaded page
    will think it has received a user gesture, essentially using an
    unintentional cache of the user activation state.
    
    This becomes an issue when dealing with our framebusting interventions.
    We only allow an iframe to do a top-level navigation if it received a
    user gesture. However, if an iframe's previous document received a user
    activation, or worse, if the iframe was not navigated to anything and
    got a user activation because its embedder was interacted with, this
    allows the current document to circumvent our framebusting
    interventions. The latter happens because of same-origin descendant
    activation behavior. See:
    https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/frame_tree_node.cc;l=766-778;drc=30753b1135fa271a3b45bbdbfef6567e46733a7f;bpv=1;bpt=1
    
    Note that this problem does not exist if site isolation is enabled
    (which is by default on desktop platforms), since a cross-site
    navigation will create a whole new process with a fresh
    `UserActivationState`.
    
    To fix this, this CL clears the user activation state on cross-site
    subframe navigations in the renderer (user activation is already cleared
    for main frames). To ensure that same-site navigations persist user
    state even if a cross-origin or same-origin navigation results in a new
    process or RenderFrameHost being created, this CL also explicitly
    transfers sticky user activation state for all same-site
    cross-RenderFrameHost navigations. This takes place in the browser, and
    the resulting bit to determine if a frame should have sticky user
    activation is passed to the renderer.
    
    The ultimate end goal is to unconditionally clear the user activation
    state for all cross-document navigations. That unfortunately is not
    possible today as there are entrenched use cases that rely on sticky
    user activation state being cached for same-site navigations. See:
    https://crbug.com/40228985.
    
    This CL also fixes the aforementioned regression when enabling the
    RenderDocument feature, since this CL will now preserve the sticky user
    activation state regardless of what
    process/RenderFrameHost/RenderDocument state the navigation results in.
    
    This CL adds some tests to the no-auto-wpt-origin-isolation test suite, which requires some additional description:
    
    * These tests are running on all platforms because site isolation behavior may differ per platform
    * All of the tests in the-iframe-element are being added because it would be useful to understand their behavior in all expected process
    configurations
    * The total time taken for this test suite on linux-rel showed a total time percentage of <0.3%
    
    Bug: 41493458
    Change-Id: Ibec11437fcd03470571e04a4e0dfaadffddf6c03
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5269464
    Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
    Reviewed-by: Charlie Reis <creis@chromium.org>
    Reviewed-by: Jeremy Roman <jbroman@chromium.org>
    Reviewed-by: Robert Flack <flackr@chromium.org>
    Reviewed-by: Andrew Verge <averge@chromium.org>
    Commit-Queue: Liam Brady <lbrady@google.com>
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
    Reviewed-by: danakj <danakj@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1269856}

M       content/browser/isolated_origin_browsertest.cc
M       content/browser/renderer_host/frame_tree_node.cc
M       content/browser/renderer_host/frame_tree_node.h
M       content/browser/renderer_host/navigation_controller_impl.cc
M       content/browser/renderer_host/navigation_entry_impl.cc
M       content/browser/renderer_host/navigation_request.cc
M       content/browser/renderer_host/navigation_request_browsertest.cc
M       content/browser/renderer_host/navigator.cc
M       content/browser/renderer_host/render_frame_host_impl.cc
M       content/browser/renderer_host/render_frame_host_impl.h
M       content/browser/site_per_process_browsertest.cc
M       content/renderer/render_frame_impl.cc
M       third_party/blink/common/frame/user_activation_state.cc
M       third_party/blink/public/common/frame/user_activation_state.h
M       third_party/blink/public/mojom/frame/user_activation_update_types.mojom
M       third_party/blink/public/mojom/navigation/navigation_params.mojom
M       third_party/blink/public/web/web_navigation_params.h
M       third_party/blink/renderer/core/frame/frame.cc
M       third_party/blink/renderer/core/frame/frame.h
M       third_party/blink/renderer/core/frame/remote_frame.cc
M       third_party/blink/renderer/core/loader/document_loader.cc
M       third_party/blink/renderer/core/loader/document_loader.h
M       third_party/blink/web_tests/TestExpectations
M       third_party/blink/web_tests/VirtualTestSuites
M       third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/resources/sandbox-top-navigation-helper.js
A       third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-child-cross-origin.tentative.sub.window.js
A       third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-cross-site.tentative.sub.window.js
M       third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/sandbox-top-navigation-user-activation.tentative.sub.window.js

https://chromium-review.googlesource.com/5269464


### el...@gmail.com (2024-03-10)

Hello Liam.,
Thank you for your hard work and everyone who contributed in solving this one.

`from my side i can confirm that this issue is now resolved as per my test on Chrome Canary 124.0.6347.0` as now there is a popup blocking redirection, and the behavior goes in tight direction now.

'Attachment for behavior after CL attached below'

- **Now feel free to Mark this as Fixed/Verified**

Thank you.

### am...@google.com (2024-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-14)

Congratulations Ahmed! The Chrome VRP Panel has decided to award you $3,000. We did notice that you pointed to two past reports of similar issues and this is generally done with the expectation of the same reward amount. The reward amount here was decided upon based on the thoroughness and quality of this report versus the high quality / the exploitability and demonstrations provided in the past reports. We appreciate your efforts here and appreciate you reporting this issue to us!

### el...@gmail.com (2024-03-14)

Hello Amy.,
Thank you , but just wanted to know is this report is less quality so the the reward amount was dropped from 5k to 3k , i think just wrote a good quality report , with more investigation results, just asking to take this into account for future reports , if you feel that the report can get same reward of the two main ones please take another look and reassess. I was waiting 5k 😞
Thank you

### am...@chromium.org (2024-03-14)

Hi Ahmed, hopefully you saw the explanation about the reward amount in [comment #21](https://issues.chromium.org/issues/41493458#comment21).
In terms of taking into account for future reports, each report is evaluated as a standalone issue -- based on the security bug, impact, exploitability, and report quality presented in the individual report. Past reports or rewards are not indicative of future reports.
We're not saying this isn't a good report, we are just saying that some of the past reports truly hit the high quality make and demonstrated the full exploitability of this issue.

### el...@gmail.com (2024-03-14)

deleted

### pe...@google.com (2024-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493458)*
