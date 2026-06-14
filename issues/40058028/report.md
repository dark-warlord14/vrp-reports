# AddressSanitizer: heap-use-after-free in blink::Screen::AreWebExposedScreenPropertiesEqual

| Field | Value |
|-------|-------|
| **Issue ID** | [40058028](https://issues.chromium.org/issues/40058028) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Screen>MultiScreen, UI>Browser>WebAppInstalls>Desktop |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dm...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2021-11-25 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0

Steps to reproduce the problem:
I reproduce this in MacOS Big Sur (11.6) with BetterDummy (https://github.com/waydabber/BetterDummy/releases/tag/v1.0.10) to simulate another screens. Maybe it's reproducible in another OS, but need another scenario. So, please, use MacOS and install BetterDummy (https://github.com/waydabber/BetterDummy#installation).

1. Open Chromium (command: "./Chromium --user-data-dir=/tmp/temporary-home-directory")
2. Enable Experimental Web Platform Features flag (chrome://flags/#enable-experimental-web-platform-features).
3. Restart Chromium.
4. Download and unzip file "screens.zip" attached to report.
5. Open directory with contents of archive in terminal (cd $unzipped_directory)
6. Run command: "python3 -m http.server 8081" (replace 8081 with any available port if necessary).
7. In Chromium open URL: http://localhost:8081/main.html (replace 8081 if you change this port on previous step).
8. Open Chromium in full screen.
9. Run BetterDummy.
10. Click "Start"
11. Allow to access screens API.
12. Click BetterDummy icon in menu bar and create random new "dummy".
13. Repeat step 12 when print dialog will be displayed in Chromium.
14. Close print dialog.
15. You will see ASAN report in Terminal.

I will attach video with reproduce in next comment.

What is the expected behavior?
No heap-use-after-free on screens interaction.

What went wrong?
Heap-Use-After-Free occurs when user changing screens configuration while Chromium process print operation.

Looks like, "print" process prevent detection of screen count/configuration changes and this lead to heap-use-after-free if user make changes in screen configuration while printing.

Did this work before? N/A 

Chrome version: 98.0.4702.0 (Developer Build) (x86_64)  Channel: n/a
OS Version: OS X 10.15

## Attachments

- [heap-uaf-screens.txt](attachments/heap-uaf-screens.txt) (text/plain, 32.5 KB)
- [screens.zip](attachments/screens.zip) (application/octet-stream, 956 B)
- [ChromiumHeapUseAfterFreeViaScreens.mp4](attachments/ChromiumHeapUseAfterFreeViaScreens.mp4) (video/mp4, 9.3 MB)
- [crbug1273841.html](attachments/crbug1273841.html) (text/plain, 1.1 KB)

## Timeline

### dm...@gmail.com (2021-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-25)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

Thanks for the report. I can reproduce this. While the repro requires --enable-experimental-web-platform-features, this does appear to be in origin trial (https://www.chromestatus.com/feature/5252960583942144) meaning it is web-exposed.

pwnall: both owners of this feature (msw, enne) are currently OOO. Could you help route to someone?

[Monorail components: UI>Browser>WebAppInstalls]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2021-11-30)

Thank you very much for this report! There are two awesome things here.

1. Using print() in an event handler.
2. Using Betterdummy to simulate external monitor. I wasn't aware of this.

Do we have a disclosure deadline here? I'm asking because the Origin Trial expires in ~2 weeks, on December 14, and the best-case scenario that I see is us getting a fix rolled out to Stable in early December, shaving off around 1 week. If letting the OT lapse is an option, we can make sure we tackle this vulnerability before we start another OT or ship the API.

### pw...@chromium.org (2021-11-30)

Two refinements two the repro process:
1. I was able to repro with a laptop and a single external monitor. I think this matters, because it shows it's not just a case of betterdummy causing an unusual set of events. 
2. I attached a one-file repro, based on the original proof-of-concept. I didn't seem to need the iframe to tickle the problem.

New repro steps:

1. Connect the external monitor.
2. Launch Chrome pointing at the page, served from any HTTP server.
    ASAN_OPTIONS=detect_odr_violation=0 out/Asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/crbug1273841 --enable-experimental-web-platform-features http://localhost:8080/crbug1273841.html
3. Wait for the button to read "Armed".
4. Disconnect the external monitor.
5. Wait for Chrome's Print dialog to show up.
6. Re-connect the external screen.
7. Wait for the screen to come online.
8. Press the Cancel button on Chrome's Print dialog.
9. Wait for the renderer crash.

Betterdummy (which is also available via "brew install betterdummy") is a very handy way of simulating this external monitor. "Create new dummy" > (any option) instead of connecting an external monitor, "Discard dummy" instead of disconnecting the external monitor.


On a DCHECK-enabled build, I'm getting the following DCHECK instead of an ASAN crash. The DCHECK shows up in the same contexts as the ASAN crash (with either Betterdummy, or a real external monitor).

[_:FATAL:screen_details.cc(143)] Check failed: new_it != new_infos.screen_infos.end(). 
0   libbase.dylib                       0x000000010939ba09 base::debug::CollectStackTrace(void**, unsigned long) + 9
1   libbase.dylib                       0x000000010926e843 base::debug::StackTrace::StackTrace() + 19
2   libbase.dylib                       0x0000000109293a6f logging::LogMessage::~LogMessage() + 175
3   libbase.dylib                       0x0000000109294a3e logging::LogMessage::~LogMessage() + 14
4   libblink_modules.dylib              0x000000012eaa3f64 blink::ScreenDetails::UpdateScreenInfos(blink::LocalDOMWindow*, display::ScreenInfos const&) + 1572
5   libblink_core.dylib                 0x0000000125c0ec48 _ZN4base8internal7InvokerINS0_9BindStateIZN5blink18WebFrameWidgetImpl25DidUpdateSurfaceAndScreenERKN7display11ScreenInfosEE4$_11JS6_bEEEFvPNS3_17WebLocalFrameImplEEE3RunEPNS0_13BindStateBaseESC_ + 152
6   libblink_core.dylib                 0x0000000125c0b9c5 WTF::ThreadCheckingCallbackWrapper<base::RepeatingCallback<void (blink::WebLocalFrameImpl*)>, void (blink::WebLocalFrameImpl*)>::Run(blink::WebLocalFrameImpl*) + 101
7   libblink_core.dylib                 0x0000000125bfe3f5 blink::(anonymous namespace)::ForEachLocalFrameControlledByWidget(blink::LocalFrame*, base::RepeatingCallback<void (blink::WebLocalFrameImpl*)> const&) + 101
8   libblink_core.dylib                 0x0000000125bfe42b blink::(anonymous namespace)::ForEachLocalFrameControlledByWidget(blink::LocalFrame*, base::RepeatingCallback<void (blink::WebLocalFrameImpl*)> const&) + 155
9   libblink_core.dylib                 0x0000000125c094a8 blink::WebFrameWidgetImpl::DidUpdateSurfaceAndScreen(display::ScreenInfos const&) + 600
10  libblink_platform.dylib             0x0000000129a4d1c6 blink::WidgetBase::UpdateSurfaceAndScreenInfo(viz::LocalSurfaceId const&, gfx::Rect const&, display::ScreenInfos const&) + 486
11  libblink_core.dylib                 0x0000000125bff801 blink::WebFrameWidgetImpl::ApplyVisualPropertiesSizing(blink::VisualProperties const&) + 129
12  libblink_core.dylib                 0x0000000125bff142 blink::WebFrameWidgetImpl::UpdateVisualProperties(blink::VisualProperties const&) + 578
13  libblink_platform.dylib             0x0000000129a48886 blink::WidgetBase::UpdateVisualProperties(blink::VisualProperties const&) + 326
14  libblink_platform.dylib             0x000000012a1cada5 blink::mojom::blink::WidgetStubDispatch::Accept(blink::mojom::blink::Widget*, mojo::Message*) + 805
15  libbindings.dylib                   0x0000000108a3101f mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) + 623
16  libbindings.dylib                   0x0000000108a37f7f mojo::MessageDispatcher::Accept(mojo::Message*) + 271
17  libbindings.dylib                   0x0000000108a32c5a mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) + 154
18  libipc.dylib                        0x000000010a6402a0 IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) + 720

[Monorail components: -UI>Browser>WebAppInstalls UI>Browser>WebAppInstalls>Desktop]

### pw...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### pw...@chromium.org (2021-12-01)

Adding folks who may be willing and able to review a prospective fix.

### [Deleted User] (2021-12-16)

pwnall: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-31)

pwnall: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2022-01-02)

The Origin Trial for the Windows Placement API ended on December 14, 2021. We still have a security vulnerability in the implementation, but it's only active for users who enable custom flags. https://developer.chrome.com/origintrials/#/view_trial/-8087339030850568191

### en...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### ms...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-02-07)

Hey Victor, would you like to proceed with https://crrev.com/c/3310042 or pass this issue to me?

### ms...@chromium.org (2022-02-07)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-02-25)

I have a WIP CL at https://ccrrev.com/c/3489926

[Monorail components: Blink>Screen>MultiScreen]

### gi...@appspot.gserviceaccount.com (2022-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c6c31a113479c289c299f5121dc2d62cb9802d46

commit c6c31a113479c289c299f5121dc2d62cb9802d46
Author: Mike Wasserman <msw@chromium.org>
Date: Fri Feb 25 21:38:56 2022

Window Placement: Fix crash from recursion amid change dispatch

UpdateScreenInfos() crashed in recursive calls from DispatchEvent().
(i.e. on screen events during a handler's nested window.print() loop)

Enqueue async event dispatch to avoid UpdateScreenInfos() recursion.
Also, skip change event dispatch steps during class initialization.
Add a regression test to prevent similar crashes in the future.

This change was spun out from https://crrev.com/c/3310042

Bug: 1273841
Test: Automated; No crash on screen events amid handler print() loops.
Change-Id: I80bd177f43893a5d638736fe8a4b5b861b50357f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3489926
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Mike Wasserman <msw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#975279}

[add] https://crrev.com/c6c31a113479c289c299f5121dc2d62cb9802d46/chrome/browser/window_placement/window_placement_printing_interactive_uitest.cc
[modify] https://crrev.com/c6c31a113479c289c299f5121dc2d62cb9802d46/third_party/blink/renderer/modules/screen_enumeration/screen_details.cc
[modify] https://crrev.com/c6c31a113479c289c299f5121dc2d62cb9802d46/chrome/test/BUILD.gn
[modify] https://crrev.com/c6c31a113479c289c299f5121dc2d62cb9802d46/third_party/blink/renderer/modules/screen_enumeration/screen_details.h
[modify] https://crrev.com/c6c31a113479c289c299f5121dc2d62cb9802d46/chrome/browser/window_placement/DEPS


### ms...@chromium.org (2022-02-25)

This is fixed, let's verify on a Canary soon and then request merge to M100 refs/branch-heads/4896.

### [Deleted User] (2022-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-27)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-02-28)

Verified on 101.0.4914.0 (Developer Build) (64-bit) - 5d4470c662b65339665d069756fd17fd8085cc55-refs/heads/main@{#975534}
(I'm not sure offhand how to get an ASAN-enabled build for verifying the fix on the actual canary channel)
Requesting merge of https://crrev.com/c/3489926 to M100 - refs/branch-heads/4896

### [Deleted User] (2022-02-28)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2022-02-28)

FWIW, the DEPS change in the CL is only to support testing.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
This fixes a Security_Severity-High heap-use-after-free crash.
2. What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/3489926
3. Have the changes been released and tested on canary?
Yes, I tested Mac 101.0.4915.0, although this crash only reproduces on debug or ASAN builds, so it never crashed on release builds, AFAIK.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, this fixes a crashed related to functionality enabled by a new feature.
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A this change applies to all desktop platforms.
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No; the CL adds automated testing; and the fix can be verified by me or others on the bug. Manual verification bu the test team is not necessarily required.

### ms...@chromium.org (2022-03-02)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-03-02)

[Empty comment from Monorail migration]

### sr...@google.com (2022-03-02)

Merge approved for M100 branch: pls refer to go/chrome-branches for info

### gi...@appspot.gserviceaccount.com (2022-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/699fb79e27d695b2f364be37c10e12d8f87d859c

commit 699fb79e27d695b2f364be37c10e12d8f87d859c
Author: Mike Wasserman <msw@chromium.org>
Date: Thu Mar 03 02:09:45 2022

Window Placement: Fix crash from recursion amid change dispatch

UpdateScreenInfos() crashed in recursive calls from DispatchEvent().
(i.e. on screen events during a handler's nested window.print() loop)

Enqueue async event dispatch to avoid UpdateScreenInfos() recursion.
Also, skip change event dispatch steps during class initialization.
Add a regression test to prevent similar crashes in the future.

This change was spun out from https://crrev.com/c/3310042

(cherry picked from commit c6c31a113479c289c299f5121dc2d62cb9802d46)

Bug: 1273841
Test: Automated; No crash on screen events amid handler print() loops.
Change-Id: I80bd177f43893a5d638736fe8a4b5b861b50357f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3489926
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Mike Wasserman <msw@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#975279}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3501252
Auto-Submit: Mike Wasserman <msw@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#228}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[add] https://crrev.com/699fb79e27d695b2f364be37c10e12d8f87d859c/chrome/browser/window_placement/window_placement_printing_interactive_uitest.cc
[modify] https://crrev.com/699fb79e27d695b2f364be37c10e12d8f87d859c/third_party/blink/renderer/modules/screen_enumeration/screen_details.cc
[modify] https://crrev.com/699fb79e27d695b2f364be37c10e12d8f87d859c/chrome/test/BUILD.gn
[modify] https://crrev.com/699fb79e27d695b2f364be37c10e12d8f87d859c/third_party/blink/renderer/modules/screen_enumeration/screen_details.h
[modify] https://crrev.com/699fb79e27d695b2f364be37c10e12d8f87d859c/chrome/browser/window_placement/DEPS


### [Deleted User] (2022-03-03)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-03-03)

[Empty comment from Monorail migration]

### ms...@google.com (2022-03-03)

FWIW, I don't think a merge to M99 or earlier is warranted.
The feature wasn't enabled by default before M100, and the OT allowing sites to enable the feature experimentally has long since ended.
So this functionality would only be possible if the user explicitly enabled chrome://flags/#enable-experimental-web-platform-features or similar.

### am...@google.com (2022-03-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### gm...@google.com (2022-03-09)

Not applicable to LTS-96 per https://crbug.com/chromium/1273841#c31

### [Deleted User] (2022-06-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1273841?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Screen>MultiScreen, UI>Browser>WebAppInstalls>Desktop]
[Monorail blocking: crbug.com/chromium/1255960, crbug.com/chromium/897300]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058028)*
