# Security: Type Confusion in Portal::ActivateImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40059476](https://issues.chromium.org/issues/40059476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Portals |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2022-04-26 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

In RenderWidgetHostViewAura::TakeFallbackContentFrom, the parameter `view` is casted to RenderWidgetHostViewAura [1], and there is a DCHECK indicates the `view` can not be an instance of RenderWidgetHostViewChildFrame. However, this is not the case when calling Portal::ActivateImpl in a <webview> tag.

Portal::ActivateImpl calls TakeFallbackContentFrom at line [2] with `outer_contents_main_frame_view`, and `outer_contents_main_frame_view` comes from `outer_contents`. If `outer_contents` is created by a <webview> tag, `outer_contents_main_frame_view` would be an instace of RenderWidgetHostViewChildFrame. This would case a type confusion between RenderWidgetHostViewAura and RenderWidgetHostViewChildFrame. The attached stack\_trace.txt shows memory corruption due to accessing invalid address.

```
void RenderWidgetHostViewAura::TakeFallbackContentFrom(  
    RenderWidgetHostView\* view) {  
  DCHECK(!static_cast<RenderWidgetHostViewBase\*>(view)  
              ->IsRenderWidgetHostViewChildFrame());  
  RenderWidgetHostViewAura\* view_aura =  
      static_cast<RenderWidgetHostViewAura\*>(view);    // ===> [1]  
  
  
void Portal::ActivateImpl() {  
  if (outer_contents_main_frame_view) {  
    // Take fallback contents from previous WebContents so that the activation  
    // is smooth without flashes.  
    portal_contents_main_frame_view->TakeFallbackContentFrom(    // ===> [2]  
        outer_contents_main_frame_view);  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_aura.cc;l=2828;drc=68ddd902509f2655d2b16605abd1f1276226294f>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/portal/portal.cc;l=620;drc=167ca64398568235a79f82bfb177f2a3694f2495>

**VERSION**  

Chrome Version: 100.0.4896.127 stable + dev

**REPRODUCTION CASE**

1. Download the attached files to <dir>
2. Setup HTTPServer  
   
   cd path/to/dir && python -m SimpleHTTPServer 8000
3. Run  
   
   out/asan/chrome --enable-logging=stderr --enable-features=Portals --load-extension=path/to/dir

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see stack\_trace.txt for details

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 170 B)
- [background.js](attachments/background.js) (text/plain, 69 B)
- [index.html](attachments/index.html) (text/plain, 83 B)
- [poc.html](attachments/poc.html) (text/plain, 283 B)
- [stack_trace.txt](attachments/stack_trace.txt) (text/plain, 12.4 KB)

## Timeline

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-27)

Thanks for the report.

+portals OWNERs, can you please investigate? Assigning a high severity for type confusion in the browser process, but None impact as Portals haven't launched yet.

[Monorail components: Blink>Portals]

### ad...@chromium.org (2022-04-27)

Thanks for filing this!

mcnee@: Should we just be disallowing portal activation inside guests?

### mc...@chromium.org (2022-04-27)

I think in principle, it should be possible to support portals in a <webview>, but I think for the short term the safer bet is to reject activation.

### mc...@chromium.org (2022-04-27)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/3611511

### gi...@appspot.gserviceaccount.com (2022-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d365002b1c357d3dc672361e7ce123633323ba06

commit d365002b1c357d3dc672361e7ce123633323ba06
Author: Kevin McNee <mcnee@chromium.org>
Date: Thu Apr 28 14:25:15 2022

Don't crash when activating a portal in a guest view

While it should be possible to activate a portal in a guest view, this
has not yet been implemented. For now, we reject activation in this
case.

Bug: 1319841
Change-Id: I30a6f528fab0c960d1720060497c81342dbe5ca5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3611511
Reviewed-by: Adithya Srinivasan <adithyas@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Commit-Position: refs/heads/main@{#997195}

[modify] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/third_party/blink/renderer/core/html/portal/portal_contents.cc
[modify] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/chrome/browser/apps/guest_view/web_view_browsertest.cc
[add] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/chrome/test/data/extensions/platform_apps/web_view/shim/portal_host.html
[modify] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/chrome/test/data/extensions/platform_apps/web_view/shim/main.js
[modify] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/content/browser/portal/portal.cc
[modify] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/third_party/blink/public/mojom/portal/portal.mojom
[add] https://crrev.com/d365002b1c357d3dc672361e7ce123633323ba06/chrome/test/data/extensions/platform_apps/web_view/shim/portal_content.html


### mc...@chromium.org (2022-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Congratulation! The VRP Panel has decided to award you $20,000 for this report. Thank you for your time and efforts in discovering this bug and reporting it to us. Nice work!

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-05)

This issue was migrated from crbug.com/chromium/1319841?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059476)*
