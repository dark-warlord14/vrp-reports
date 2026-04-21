# Drag and Drop Can Navigate to File and Chrome URIs Without Restriction

| Field | Value |
|-------|-------|
| **Issue ID** | [342579972](https://issues.chromium.org/issues/342579972) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>DataTransfer, UI>Browser>Navigation, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Windows |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ay...@chromium.org |
| **Created** | 2024-05-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Usually, navigation from an online site to a file URI or Chrome URI is blocked with "about:blank," but using Chrome drag and drop, the navigation is possible without restriction.

Below, the proof-of-concept demonstration shows four cases:

- Case 1: Drag a normal link - which is blocked.
- Case 2: Drag and drop a file URI using setData to open a local file - which worked.
- Case 3: Drag and drop a Chrome URI using setData - which worked.
- Case 4: Drag and drop a Chrome URI to kill Chrome using setData - which worked.

What is the expected output? What do you see instead?
I expect that clicking the link will navigate to "about:blank," since links in PDFs should not be allowed to navigate to "file://" or "chrome://" URLs. Instead, dragging the link results in successfully navigating to the local file or Chrome URI.

**VERSION**

Chrome Version: Tested on both the Stable [125.0.6422.76 (Official Build) (64-bit) (cohort: Control) ] and Canary [ 127.0.6498.3 (Official Build) canary (64-bit) (cohort: Clang-64) ]versions

Operating System: Windows 11

**REPRODUCTION CASE**

1. Download the poc.html file below and host it on a server.
2. Open your server address on the latest Chrome version, or you can use the link <https://test-ece44.web.app/poc-drag/poc.html> for testing.
3. Test each case and see that the first case is blocked, while the following cases are not, making it possible to trigger all types of navigation. For example, an attacker can navigate to any file URI on the victim's computer or a specific Chrome URL, which can be used to their advantage.

**CREDIT INFORMATION**

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.3 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.8 MB)

## Timeline

### fa...@gmail.com (2024-05-24)

Similar issue: <https://issues.chromium.org/issues/40082882>

### mp...@google.com (2024-05-28)

I think we should probably restrict this action with drag and drop, at least with a drag from web content.

### dc...@chromium.org (2024-05-28)

Hm... this used to work. I wonder why it stopped working?

### dc...@chromium.org (2024-05-28)

Oh I think this is maybe the tabstrip doing something custom. The tabstrip folks should take a look at this.

### dc...@chromium.org (2024-05-28)

FWIW, in Blink, this goes through the 'standard' navigation APIs: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/page/drag_controller.cc;l=320;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9>

And presumably this gets filtered somewhere, though I can't find where exactly atm. I'll ask around to see if anyone remembers where :)

### mp...@google.com (2024-05-28)

This reproduces on M124 extended stable.

### pe...@google.com (2024-05-29)

Setting milestone because of s2 severity.

### dc...@chromium.org (2024-05-29)

I did some testing for variants. If you drag and drop a chrome:// URL on top of a Chrome shortcut on Windows desktop, it doesn't launch anything. I think this is good and WAI. I did not test Mac.

One other artifact of us using `FilterURL()` for the primary blocking is that if you drag and drop a chrome:// URL onto **another** chrome:// page, that works. I'm not sure if we actually want that to work. We probably don't, and perhaps that suggests that we should fix the tabstrip bug (but also re-evaluate how the blocking works for drops on web content)

### cr...@chromium.org (2024-05-29)

Re: [comment #9](https://issues.chromium.org/issues/342579972#comment9):

I think it's probably intentional that dragging chrome:// (and even file://) URLs from a chrome:// URL works, since chrome:// pages are meant to be trustworthy and shouldn't have links that are dangerous to drag. With that said, I wouldn't be opposed to blocking it (in a separate issue) to be safe, if there weren't use cases that depend on dragging URLs in chrome:// pages.

For this particular bug, it looks like we normally call FilterURL on the dragged URL pretty early, in RenderWidgetHostImpl::StartDragging [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_impl.cc;drc=74660652ad627e748c7a871d3227791879c47514;l=2725).

However, in this repro, the URL is not stored in `drop_data.url`, but rather in `drop_data.text`. That means it doesn't go through FilterURL, and apparently there's some later code (which I haven't found) that converts the text into a URL to be used when the navigation actually occurs in BrowserRootView::NavigateToDroppedUrls [here](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/frame/browser_root_view.cc;drc=cda32d827e6ba0cd30b4cf7e86cb2a73062f8160;l=598).

Ironically, the DropInfo used in NavigateToDroppedUrls actually contains URLs that have gone through a function named [FilterURLsForDropability](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/frame/browser_root_view.cc;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9;l=110), but which does *not* actually call FilterURL or otherwise prevent chrome:// or file:// URLs.

(Doubly ironically, RenderWidgetHostImpl::StartDragging intentionally allows javascript: URLs to be dragged, but that's one of the few things FilterURLsForDropability prevents.)

I'm not sure what the expected flow for drag and drop is and where the best place to put the missing check(s) would be, but FilterURLsForDropability certainly sounds like a good candidate.

### dc...@chromium.org (2024-05-30)

To clarify, it's possible to drag one of the #2/#3/#4 links from the PoC page and drop it on a chrome:// page and have that successfully navigate. I suppose it's possible that's somehow falling through to `NavigateToDroppedUrls()`, but I would be really surprised if that were the case—I'm 99% sure this is going through the standard `BeginNavigation()` flow, but `FilterURL()` doesn't block it in this case.

TBH, I am not convinced that we should allow drag-and-drop navigations to work for anything other than http: and https: links... (especially for text->url navigations).

### dc...@chromium.org (2024-05-30)

Also see [issue 40174984](https://issues.chromium.org/issues/40174984) for synthesizing URLs from text.

### cr...@chromium.org (2024-06-07)

[Navigation triage]

Thanks dpenning@ for taking a look! I'll mark this as triaged.

### pe...@google.com (2024-06-21)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dp...@google.com (2024-06-26)

I dont believe this is an issue with the TabStrip, since it doesnt have access to the RenderProcessHost of the tab where the drag originated from. I think the issue here is that we are allowing the URL of the dragged tab to be manipulated via the "dragstart" event in javascript after FilterURLs has been called. We should instead, on any element drag data getting updated, call this FilterURL method, since the manipulation should surface from the correct renderprocesshost. Im going to pass this back to estade@ who assigned to tbergquist@. 

### es...@chromium.org (2024-06-26)

> Im going to pass this back to estade@ who assigned to tbergquist@.

technically, I believe dcheng did that. But in any case, the most active owner for dnd is christinesm@ and/or MS folks. Christine, can you own and/or find an owner for this?

### pe...@google.com (2024-07-13)

christinesm: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2024-07-31)

Friendly ping.

### ay...@chromium.org (2024-08-02)

Looks like this might be happening in the 'paste and go' logic [here](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/frame/browser_root_view.cc;l=254;drc=cda32d827e6ba0cd30b4cf7e86cb2a73062f8160) where it converts text content to a URL. As dpenning@ mentioned though, I don't think it has access to the RenderProcessHost of the tab it originated from at this point to properly call FilterURL.

Wondering if anyone has any recommendations on how to approach this (rather new to this code area).

I tested in M99 and I was still able to repro, so doesn't seem like a recent regression.

### fa...@gmail.com (2024-11-14)

Hi, looking at the 'paste and go' logic as described above. I could suggest we try to block drag-and-drop functionality similarly to how it disallows `javascript:` URLs.

```
    // Disallow javascript: URLs to prevent self-XSS.
    if (url.SchemeIs(url::kJavaScriptScheme)) {
        continue;
    }

```

I have tried implementing a similar check for `chrome:` and `file:` URLs. I tested this build, and it successfully blocked chrome, file schemes. However, i need to could allowing drag-and-drop when the parent scheme matches. I also encountered an issue where drag-and-drop from the user's computer to the browser window, which was also blocked with this simple fix.

```
    // Disallow javascript: URLs to prevent self-XSS.
    if (url.SchemeIs(url::kJavaScriptScheme)) {
        continue;
    }

    // Disallow chrome: URLs, except when matching the parent scheme.
    if (url.SchemeIs(content::kChromeUIScheme) && parent_scheme != content::kChromeUIScheme) {
        continue;
    }

    // Disallow file: URLs, except when matching the parent scheme.
    if (url.SchemeIs(url::kFileScheme) && parent_scheme != url::kFileScheme) {
        continue;
    }

```

I created the `parent_scheme` variable to retrieve the parent scheme by calling `web_contents->GetLastCommittedURL()` and using `scheme()`.

Attempted fix: <https://chromium-review.googlesource.com/c/chromium/src/+/6428889>

### dc...@chromium.org (2025-04-03)

This was recently fixed by https://chromium-review.googlesource.com/c/chromium/src/+/6400553. I didn't know about this bug, but the fix for that applies here as well.

### sp...@google.com (2025-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
thank you reward -- while this report was the first report of this issue, a newer report of higher quality and demonstrating higher impact was also reported and helped to achieve the issue being prioritized and resolved


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-10)

Thank you for reporting this issue to us!

### fa...@gmail.com (2025-04-10)

Thanks, I tried fixing this myself, but things didn’t go so well for me with this issue. I’ll try do my best on the next one. Inshallah.

### ch...@google.com (2025-04-30)

deleted

### ch...@google.com (2025-07-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pu...@gmail.com (2025-07-17)

deleted

### pu...@gmail.com (2025-07-17)

deleted

## Bounty Award

> thank you reward -- while this report was the first report of this issue, a newer report of higher quality and demonstrating higher impact was also reported and helped to achieve the issue being prioritized and resolved

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342579972)*
