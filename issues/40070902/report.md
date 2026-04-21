# heap-use-after-free in ReadAnythingAppController::OnActiveAXTreeIDChanged(ui::AXTreeID const&, long long, GURL const&)

| Field | Value |
|-------|-------|
| **Issue ID** | [40070902](https://issues.chromium.org/issues/40070902) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility>ReadingMode, UI>Browser>TopChrome>SidePanel |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zy...@gmail.com |
| **Assignee** | fr...@google.com |
| **Created** | 2023-08-30 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description


heap-use-after-free in ReadAnythingAppController::OnActiveAXTreeIDChanged(ui::AXTreeID const&, long long, GURL const&)


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


#### Which URL (or repository) have you found the vulnerability in?

chrome/renderer/accessibility/read_anything_app_controller.cc


---

### The problem


#### Please describe the technical details of the vulnerability

Reproduce:

1. Run ASAN chromium:
```
➜  ./Chromium.app/Contents/MacOS/Chromium
```

2. Open reading mode for the sidebar

3. visit "chrome-untrusted://read-anything-side-panel.top-chrome/" in Tab A

4. After the page has finished loading, if you visit any other websites in Tab A, Chromium will crash due to a heap-use-after-free error.

```
SUMMARY: AddressSanitizer: heap-use-after-free read_anything_app_controller.cc:426 in ReadAnythingAppController::OnActiveAXTreeIDChanged(ui::AXTreeID const&, long long, GURL const&)
Shadow bytes around the buggy address:
  0x61d000041800: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x61d000041880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x61d000041900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x61d000041980: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa
  0x61d000041a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x61d000041a80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d000041b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d000041b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d000041c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d000041c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x61d000041d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
...
```


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

heap-user-after-free


---

### The cause


#### What version of Chrome have you found the security issue in?

Chromium [115.0.5787.0]/ Chrome canary [118.0.5976.0 ]


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)


#### How would you like to be publicly acknowledged for your report?

retsew0x01




## Attachments

- [asanlog.txt](attachments/asanlog.txt) (text/plain, 2.6 KB)
- [screenrecorder2023-08-30.mov](attachments/screenrecorder2023-08-30.mov) (video/quicktime, 12.4 MB)
- [full_asanlog.txt](attachments/full_asanlog.txt) (text/plain, 34.4 KB)
- [screenshot_chrome_stable_version.png](attachments/screenshot_chrome_stable_version.png) (image/png, 282.8 KB)

## Timeline

### ch...@appspot.gserviceaccount.com (2023-08-30)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-08-30)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-08-30)

Attach the screen record.

### zy...@gmail.com (2023-08-30)

Attach the full ASAN log.

### zy...@gmail.com (2023-08-31)

Sorry, correct a description: This vulnerability does not cause a crash.

And the heap-Use-after-free's root cause was:


read_anything::mojom::UntrustedPageStubDispatch::Accept(read_anything::mojom::UntrustedPage*, mojo::Message*)

->chrome/renderer/accessibility/read_anything_app_controller.cc
```
void ReadAnythingAppController::OnActiveAXTreeIDChanged(
    const ui::AXTreeID& tree_id,
    ukm::SourceId ukm_source_id,
    const GURL& url) {
  if (tree_id == model_.active_tree_id()) {
    return;
  }
  ui::AXTreeID previous_active_tree_id = model_.active_tree_id();
  model_.SetActiveTreeId(tree_id);
  model_.SetActiveUkmSourceId(ukm_source_id);
  model_.SetActiveTreeSelectable(GetSelectable(url));
  // Delete all pending updates on the formerly active AXTree.
  // TODO(crbug.com/1266555): If distillation is in progress, cancel the
  // distillation request.
  model_.ClearPendingUpdates();
  model_.set_requires_distillation(false);

  // TODO(b/1266555): Use v8::Function rather than javascript. If possible,
  // replace this function call with firing an event.
  std::string script = "chrome.readingMode.showLoading();";
  render_frame_->ExecuteJavaScript(base::ASCIIToUTF16(script));

  // When the UI first constructs, this function may be called before tree_id
  // has been added to the tree list in AccessibilityEventReceived. In that
  // case, do not distill.
  if (model_.active_tree_id() != ui::AXTreeIDUnknown() &&
      model_.ContainsTree(model_.active_tree_id())) {
    Distill();
  }
}
```

### ph...@chromium.org (2023-08-31)

I can reproduce in M116.

Hi abigailbklein@ could you take a look at this security bug please?

[Monorail components: UI>Accessibility>ReadingMode UI>Browser>TopChrome>SidePanel]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### ab...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-08-31)

(I am a bot: this is an auto-cc on a security bug)

### ab...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-09-01)

Hello, this is the first memory corruption vulnerability I've discovered on Chrome, so I'd like to ask: what are the rules for rating heap-use-after-free as high or medium severity? I noticed that most publicly reported heap-use-after-free vulnerabilities are rated as high severity. Thanks!

### zy...@gmail.com (2023-09-01)

It also affects the release version of macOS, the OS tag should be added `macOS`. In theory, Windows is also affected.

### ab...@google.com (2023-09-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

[secondary security shepherd] Hi OP, thanks for the report. UAFs that require user interaction can be reduced in severity at times depending on the amount of user interaction. Since this is an accessibility issue and there is some interaction expected from Accessibility features, I am going to convert this to High severity. 

That being said, read-anything is still behind a flag and does not appear to be launched / enabled by default, so I'm also converting this to SI-None, since this does not impact users at this time. 

Security issues, even those impacting unlaunched features, cannot go without owners. Assigning to jocelyntran@ based on read-anything owners file and abigailbklein@ is currently OOO. 

### am...@chromium.org (2023-09-05)

[Empty comment from Monorail migration]

### jo...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-09-06)

That being said, read-anything is still behind a flag and does not appear to be launched / enabled by default
----------

Hi, I found that it was already enabled by default in the >M115 stable version. Please refer to the attached screenshot. This is the Chrome stable version that I just downloaded and installed, without making any modifications to the Chrome://flags settings.

### dt...@chromium.org (2023-09-06)

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)
------
This is a sandboxed / untrusted renderer process.

### dt...@chromium.org (2023-09-06)

In terms of a fix, I think any navigation of the untrusted read anything url should trigger the side panel. See the lens navigation throttle for an example:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/lens/lens_side_panel_navigation_helper.h;l=35?q=lens%20navigation%20throttle&ss=chromium

It does what I think is the desired behavior.

### dt...@chromium.org (2023-09-06)

Jacob, do you have time to take a look?

### fr...@google.com (2023-09-06)

@dtseng@chromium.org Yes, I've been keeping an eye on this. 

### fr...@google.com (2023-09-13)

Some tests should be added to verify the new feature of opening the sidebar when the Read anything url is put in. 

Additionally it would be worth investigating a better way of detecting the difference between a navigation to that URL from the address bar vs the sidebar loading itself. 

### [Deleted User] (2023-10-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-10-18)

ReadAnything is currently enabled on Stable at 10%, and since use of ReadAnything is a precondition, this issue is no longer SI-None. Updating as FoundIn-118. This issue likely existing farther back, but 118 is currently the oldest active release channel. 
Reduced to medium severity since this is in a renderer sandboxed process not in the browser process. This is also mitigated by user interaction. 

### [Deleted User] (2023-10-30)

francisjp: Uh oh! This issue still open and hasn't been updated in the last 46 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fr...@google.com (2023-10-30)

Update: Still working out the details for implementing the tests. 

### gi...@appspot.gserviceaccount.com (2023-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7e17c410d27eb52160b8619e1675da1d41c74713

commit 7e17c410d27eb52160b8619e1675da1d41c74713
Author: Jacob Francis <francisjp@google.com>
Date: Fri Nov 10 19:52:00 2023

[Read Anything] Fix heap use after free

This fixes a use after free bug in asan by not allowing a user
to open reading mode in the main content area.

The new behavior causes the browser to open the reading mode panel
when the user puts the Read Anything URL into the address bar.

Links were already blocked.

Bug: 1477151
Change-Id: I2e29a5e113e1f9f0eb3addf6f1ba172c4b804ce7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4851342
Reviewed-by: Colin Blundell <blundell@chromium.org>
Reviewed-by: Mike Wasserman <msw@chromium.org>
Commit-Queue: Jacob Francis <francisjp@google.com>
Cr-Commit-Position: refs/heads/main@{#1223092}

[add] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/side_panel/read_anything/OWNERS
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/webui/side_panel/read_anything/read_anything_app_toolbar_browsertest.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/webui/side_panel/read_anything/read_anything_app_read_aloud_browsertest.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/views/side_panel/side_panel_coordinator.h
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/webui/side_panel/read_anything/read_anything_app_browsertest.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/side_panel/side_panel_enums.h
[add] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/views/side_panel/read_anything/read_anything_side_panel_navigation_throttle.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/webui/side_panel/read_anything/DEPS
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/views/side_panel/side_panel_web_ui_view.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/webui/chrome_url_data_manager_browsertest.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/views/side_panel/side_panel_coordinator.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/extensions/extension_untrusted_webui_apitest.cc
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/BUILD.gn
[add] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/side_panel/read_anything/read_anything_side_panel_navigation_throttle.h
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/side_panel/side_panel_ui.h
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/ui/views/side_panel/side_panel_web_ui_view.h
[modify] https://crrev.com/7e17c410d27eb52160b8619e1675da1d41c74713/chrome/browser/chrome_content_browser_client.cc


### [Deleted User] (2023-12-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fr...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this heavily mitigated security bug, mitigated by not being remote exploitable, amount of user interaction required, and the low potential for exploitability given the UI interactions required to trigger this issue as demonstrated. Thank you for your efforts and reporting this issue to us. 

### zy...@gmail.com (2023-12-14)

Thanks! Hope to greet you at the next ESCAL8 event. Last time in Tokyo, I wasn't sure which one was you.

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-27)

Hope to meet you at next ESCAL8 or some future event as well. I was the one with the brown hair that gave the talk about Chrome Security during BugSWAT :) 

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1477151?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Accessibility>ReadingMode, UI>Browser>TopChrome>SidePanel]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2024-03-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### rz...@google.com (2024-03-26)

1. <https://crrev.com/c/5341709>
2. Low, simple conflicts
3. 121
4. No, the CL broke 20+ unrelated tests

### gm...@google.com (2024-04-09)

Rejecting merge for LTS

### ni...@google.com (2024-05-28)

marking fixed per comment 35

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070902)*
