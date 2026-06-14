# Security: Select Options Can Escape Across Tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [41494315](https://issues.chromium.org/issues/41494315) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Select, Blink>HTML, Internals>Sandbox>SiteIsolation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-01-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using the select option and showPicker(), an attacker could overlay content on other tabs from a malicious site.

Below is a proof-of-concept page; when a victim clicks on a malicious site, the select options are displayed over other tabs opened by the victim.

**VERSION**  

Chrome Version: 121.0.6167.86 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Download the poc.html file.
2. Open the poc.html file in the latest stable version of Google Chrome.
3. Open a different website (this can also be done later) and interact with the malicious site by clicking anywhere. Check if the select option for the malicious site is shown on every tab the user tries to visit.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 904 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.2 MB)

## Timeline

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### li...@chromium.org (2024-01-24)

Hello,

Thanks for your report! 
I'm setting this to a medium right now because it looks like this breaks the same origin policy, but I don't see if it's possible to get code exec.



[Monorail components: Blink>HTML]

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### cr...@chromium.org (2024-01-24)

Thanks for the report!  I've confirmed on Linux, so I'll add a few platforms.  (Haven't tested on Android.)  It appears this sends a flood of showPicker() calls, and that it's possible for the browser to display the select popup over the wrong tab or page (apparently depending on a race, since it's not consistent in a debug build).

That means no code is running in the wrong origin, but it's definitely a problem for the select menu to be displayed over the wrong tab or page.  jarhar@: Do you know how that works, and whether we can identify in the browser process which frame asked to show the select popup?

I'll add the Site Isolation component since we would like to ensure better display isolation between origins, even if it's not a data leak.

[Monorail components: Blink>Forms>Select Internals>Sandbox>SiteIsolation]

### [Deleted User] (2024-01-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2024-01-24)

I believe that consuming user activation after the check for user activation would fix this. I filed a spec bug to suggest doing so: https://github.com/whatwg/html/issues/10084

### cr...@chromium.org (2024-01-24)

https://crbug.com/chromium/1521345#c6: That may be a good partial fix (e.g., for the flood of IPCs), but that probably wouldn't prevent a well timed IPC from showing up over the wrong tab or page.  Is there code in the browser process for showing this popup (e.g., RenderWidget) that might be able to enforce that it shows up over content from the right renderer process?

### ja...@chromium.org (2024-01-24)

Good point. I can't get the popup to show over other tabs on macos or linux because I can't click on other tabs while there are popups being spammed, but I can on a chrome dev on windows.

Based on some brief reading, it looks like WebContentsImpl::CreateNewPopupWidget is the place in the browser process that creates the popup. Do you have any advice on how I can compare the tab thats showing to the tab that requested to create the popup?

### cr...@chromium.org (2024-01-24)

Good question.  It looks like RenderWidgetHost is given the initiating WebContents (i.e., RenderWidgetHostDelegate) when it's created here:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;drc=70a6711e08e9f9e0d8e4c48e9ba5cab62eb010c2;l=4650

I would have expected that to be sufficient for there to be logic to cause the RenderWidgetHost to be hidden if the tab changes (or ideally if the document that created the popup navigates away as well), but I don't know enough about RenderWidgetHost or RenderWidgetHostView to say.  We might have to find someone who can help with that.

danakj@: I know it's been a long time since you've looked at RenderWidgetHost related code, but would you have any tips or know who we could ask?  Thanks!

### ja...@chromium.org (2024-01-24)

Thanks, I'll try building on windows to do some debugging but it will take some time

### ha...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### ja...@chromium.org (2024-01-25)

Not sure if its the best fix yet, but I made something that seems to work based on manual testing: https://chromium-review.googlesource.com/c/chromium/src/+/5237056

### cr...@chromium.org (2024-01-27)

Thanks for working on the fix and a test!

Looks like the CL in https://crbug.com/chromium/1521345#c12 is ignoring the select popup if the tab isn't visible.  Are we confident that the attack can't happen from a visible WebContents?  Could it happen if you went back to the NTP in the same (visible) WebContents, or can that not happen?  (I haven't been able to repro it that way, so maybe something rules that out?)

### fa...@gmail.com (2024-01-29)

Hi, jarhar@ Mozilla is also in support of the spec mentioned in https://github.com/whatwg/html/issues/10084, as I have also reported a similar issue to Firefox.

### is...@google.com (2024-01-29)

This issue was migrated from crbug.com/chromium/1521345?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>Select, Blink>HTML, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-09)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-02-24)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-03-05)

Project: chromium/src
Branch: main

commit 20dd9861775e1041511c9101830389c15e614b0e
Author: Joey Arhar <jarhar@chromium.org>
Date:   Tue Mar 05 19:40:59 2024

    Don't create popups for hidden tabs
    
    This patch adds visibility checks in content to prevent invisible or
    background tabs from creating <select> popups, which would allow them to
    render popups on top of other tabs.
    
    This patch also sends cancel mojo messages via PopupMenuClient in the
    browser when the browser process doesn't end up creating a popup in the
    first place so that the renderer doesn't think that a popup is showing
    when there actually isn't. This was needed in order to write a test that
    works.
    
    Fixed: 1521345
    Change-Id: If4ed34243467e5310b93a55df2efa5777d1a0e56
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5237056
    Reviewed-by: Scott Violet <sky@chromium.org>
    Reviewed-by: Charlie Reis <creis@chromium.org>
    Commit-Queue: Joey Arhar <jarhar@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1268620}

A       chrome/browser/select_popup_browsertest.cc
M       chrome/test/BUILD.gn
M       content/browser/renderer_host/render_frame_host_impl.cc
M       content/browser/web_contents/web_contents_impl.cc

https://chromium-review.googlesource.com/5237056


### am...@google.com (2024-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-14)

Congratulations, Shaheen! The Chrome VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us!

### fa...@gmail.com (2024-03-15)

Thank you!

### am...@chromium.org (2024-04-26)

It appears this fix would have rolled out in the M124 Stable milestone <https://chromiumdash.appspot.com/commit/20dd9861775e1041511c9101830389c15e614b0e>

I've added the release label and relevant hotlist so that it can be picked up pgrace@'s update process

### ap...@google.com (2024-06-01)

Project: chromium/src
Branch: main

commit a08c78bcc5aee86d74174ee1e1925d4fe003f67a
Author: Joey Arhar <jarhar@chromium.org>
Date:   Sat Jun 01 01:44:59 2024

    Make showPicker() consume user activation
    
    Allowing the page to call showPicker() on select elements as much as it
    wants without consuming user activation may result in the user being
    unable to interact with the browser UI due to popups always taking
    focus.
    
    The HTML spec also says to do this for input elements, so I added code
    to do it there as well.
    
    This patch also modified the select showPicker test because calling
    showPicker on a select twice in a row in the test somehow resulted in
    blink not seeing any input events on the second test_driver.bless(),
    perhaps because the select's popup is still open and is somehow
    intercepting the input.
    
    HTML spec: https://github.com/whatwg/html/pull/10344
    
    Bug: 1521345
    Fixed: 343302069, 343093082, 343473478
    Change-Id: If6308a67bac9050f695d18d275ea86c23ac22b0d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5235516
    Commit-Queue: Joey Arhar <jarhar@chromium.org>
    Reviewed-by: Di Zhang <dizhangg@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1309009}

M       third_party/blink/renderer/core/html/forms/html_input_element.cc
M       third_party/blink/renderer/core/html/forms/html_select_element.cc
M       third_party/blink/renderer/platform/runtime_enabled_features.json5
M       third_party/blink/web_tests/TestExpectations
D       third_party/blink/web_tests/external/wpt/html/semantics/forms/the-input-element/click-user-gesture-expected.txt
D       third_party/blink/web_tests/external/wpt/html/semantics/forms/the-select-element/show-picker-user-gesture-expected.txt
M       third_party/blink/web_tests/external/wpt/html/semantics/forms/the-select-element/show-picker-user-gesture.html
D       third_party/blink/web_tests/flag-specific/enable-skia-graphite/external/wpt/html/semantics/forms/the-input-element/show-picker-disabled-readonly-expected.txt
D       third_party/blink/web_tests/platform/linux/external/wpt/html/semantics/forms/the-input-element/show-picker-user-gesture-expected.txt
D       third_party/blink/web_tests/platform/mac-mac14-arm64/external/wpt/html/semantics/forms/the-input-element/show-picker-disabled-readonly-expected.txt
D       third_party/blink/web_tests/platform/mac/external/wpt/html/semantics/forms/the-input-element/show-picker-disabled-readonly-expected.txt
D       third_party/blink/web_tests/platform/mac/external/wpt/html/semantics/forms/the-input-element/show-picker-user-gesture-expected.txt
D       third_party/blink/web_tests/platform/win/external/wpt/html/semantics/forms/the-input-element/show-picker-disabled-readonly-expected.txt
D       third_party/blink/web_tests/platform/win11-arm64/external/wpt/html/semantics/forms/the-input-element/click-user-gesture-expected.txt
D       third_party/blink/web_tests/platform/win11-arm64/external/wpt/html/semantics/forms/the-input-element/show-picker-disabled-readonly-expected.txt
D       third_party/blink/web_tests/platform/win11-arm64/external/wpt/html/semantics/forms/the-select-element/show-picker-user-gesture-expected.txt

https://chromium-review.googlesource.com/5235516


### pe...@google.com (2024-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ap...@google.com (2024-09-06)

Project: chromium/src
Branch: main

commit 2efa01075cc5b7aafc6436fb20b8eef8957a1071
Author: Joey Arhar <jarhar@chromium.org>
Date:   Fri Sep 06 17:04:49 2024

    Remove ShowPickerConsumeUserActivation flag
    
    This has been enabled by default since M127, so it is safe to remove
    now.
    
    Bug: 1521345, 343302069, 343093082, 343473478
    Change-Id: I26850604974c5284bba965ee55fd123618b2ce11
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5840528
    Commit-Queue: Traian Captan <tcaptan@chromium.org>
    Reviewed-by: Traian Captan <tcaptan@chromium.org>
    Auto-Submit: Joey Arhar <jarhar@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1352118}

M       third_party/blink/renderer/core/html/forms/html_input_element.cc
M       third_party/blink/renderer/core/html/forms/html_select_element.cc
M       third_party/blink/renderer/platform/runtime_enabled_features.json5

https://chromium-review.googlesource.com/5840528


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41494315)*
