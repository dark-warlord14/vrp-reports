# Security: UAF in CaptionHostImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40052216](https://issues.chromium.org/issues/40052216) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ab...@google.com |
| **Created** | 2020-05-06 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

CaptionHostImpl is created with mojo::MakeSelfOwnedReceiver, and it holds a raw pointer to the RenderFrameHost without observing its lifetime.

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/accessibility/caption_host_impl.cc;drc=2903761f6d8e51ffefce4b5b1354f53750454dbd;l=20?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

void CaptionHostImpl::Create(  

content::RenderFrameHost\* frame\_host,  

mojo::PendingReceiver[chrome::mojom::CaptionHost](javascript:void(0);) receiver) {  

mojo::MakeSelfOwnedReceiver(std::make\_unique<CaptionHostImpl>(frame\_host), // => raw pointer is passed  

std::move(receiver));  

}

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/accessibility/caption_host_impl.cc;drc=2903761f6d8e51ffefce4b5b1354f53750454dbd;l=27?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

CaptionHostImpl::CaptionHostImpl(content::RenderFrameHost\* frame\_host)  

: frame\_host\_(frame\_host) {}

In CaptionHostImpl::OnTranscription(), raw pointer |frame\_host\_| is used at:

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/accessibility/caption_host_impl.cc;drc=2903761f6d8e51ffefce4b5b1354f53750454dbd;l=32?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

void CaptionHostImpl::OnTranscription(  

chrome::mojom::TranscriptionResultPtr transcription\_result) {  

if (!frame\_host\_)  

return;  

auto\* web\_contents = content::WebContents::FromRenderFrameHost(frame\_host\_);  

if (!web\_contents)  

return;

But CaptionHostImpl object outlives RenderFrameHost. This leads RenderFrameHost maybe be freed but there is a message of CaptionHost interface still be in queue. When this message is handled, |frame\_host\_| is used but the RenderFrameHost object that this pointer reference to is freed => lead to UAF bug!

Two possible patches are also included. One has CaptionHostImpl inherit from WebContentsObserver to observe the render frame destruction and clear its reference. The other patch has CaptionHostImpl store the (process\_id, frame\_id) pair in place of the raw pointer and perform dynamic lookup of the render frame host object.

**VERSION**  

Chrome Version: 84.0.4136.2  

Operating System: Windows 10

**REPRODUCTION CASE**  

First we need to enable Live Captions feature

- enable `Live Captions` feature through chrome://flags/#enable-accessibility-live-captions
- enable `Live caption` in chrome://settings/accessibility

I use prebuilt asan chromium from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-765844.zip?generation=1588732255668077&alt=media>

To reproduce you need a local build of chrome; run the attached script

python copy\_mojo\_js\_bindings.py /path/to/chrome/.../asan-win32-release\_x64-765844/gen .  

python -m SimpleHTTPServer&  

chrome.exe --enable-blink-features=MojoJS '<http://localhost:8000/live_caption.html>'

Note that this is \*not\* a renderer bug; it's a browser process bug that's reachable from the renderer. The attached poc is using the MojoJS bindings to trigger the issue, but a compromised renderer could perform the same actions without any special settings.

============================================

## Attachments

- [mojo_1.zip](attachments/mojo_1.zip) (application/octet-stream, 2.8 MB)
- [log_crash_asan.txt](attachments/log_crash_asan.txt) (text/plain, 20.1 KB)

## Timeline

### cl...@chromium.org (2020-05-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5733341704290304.

### cl...@chromium.org (2020-05-06)

Testcase 5733341704290304 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5733341704290304.

### oc...@google.com (2020-05-06)

abigailbklein, could you please help take a look at this ?

[Monorail components: UI>Accessibility]

### ab...@google.com (2020-05-06)

Hi there, thanks for your detailed explanation of this bug. I just yesterday sent a CL out for review which addresses this: https://chromium-review.googlesource.com/c/chromium/src/+/2183011. This is the second proposal that huyna89@gmail.com proposed above (store the (process_id, frame_id) pair in place of the raw pointer and perform dynamic lookup of the render frame host object). I investigated the first proposal (CaptionHostImpl inherit from WebContentsObserver to observe the render frame destruction and clear its reference) but it would have been more complicated, as adding the CaptionHostImpl, which is in chrome/, as an observer to WebContentsImpl, which is in contents/, is not trivial.

### [Deleted User] (2020-05-06)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2020-05-06)

https://chromium-review.googlesource.com/c/chromium/src/+/2183011 is LGTM'd and in the commit queue.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4c51ac4e1a8062543f3a6054f6d6de875e748bae

commit 4c51ac4e1a8062543f3a6054f6d6de875e748bae
Author: Abigail Klein <abigailbklein@google.com>
Date: Wed May 06 19:45:02 2020

[Live Caption] CaptionHostImpl clears reference to RenderFrameHost on
destruction of render frame.

Make the CaptionHostImpl a WebContentsObserver and clear its reference
to the RenderFrameHost when the render frame is deleted.

Bug: 1055150, 1078671
Change-Id: If9295f61a7665503f558ea6147a0fbf3bef8a5e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2183011
Commit-Queue: Abigail Klein <abigailbklein@google.com>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#766108}

[modify] https://crrev.com/4c51ac4e1a8062543f3a6054f6d6de875e748bae/chrome/browser/accessibility/caption_controller.cc
[modify] https://crrev.com/4c51ac4e1a8062543f3a6054f6d6de875e748bae/chrome/browser/accessibility/caption_controller.h
[modify] https://crrev.com/4c51ac4e1a8062543f3a6054f6d6de875e748bae/chrome/browser/accessibility/caption_host_impl.cc
[modify] https://crrev.com/4c51ac4e1a8062543f3a6054f6d6de875e748bae/chrome/browser/accessibility/caption_host_impl.h


### ab...@google.com (2020-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-07)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-11)

[Empty comment from Monorail migration]

### mb...@google.com (2020-05-13)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-14)

Congrats! The Panel decided to award $20,000 for this report. Nice one! 

### [Deleted User] (2020-05-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

abigailbklein@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ab...@google.com (2020-07-01)

mmoroz@, I don't have access to the form. Will you please share it with me?

### [Deleted User] (2020-08-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cs...@google.com (2021-10-15)

No crashes have been reported and the code is presumed fixed.

### cs...@google.com (2021-10-15)

No crashes have been reported and the code is presumed fixed.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1078671?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052216)*
