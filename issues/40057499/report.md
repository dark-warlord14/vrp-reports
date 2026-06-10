# Security: Busy Rendering Cause Layer to Persist on Target Website Allow Address Bar Spoofing & Clickjacking Attack

| Field | Value |
|-------|-------|
| **Issue ID** | [40057499](https://issues.chromium.org/issues/40057499) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Input |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2021-10-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using huge CSS font-size, line height then combined with large border radius, Chromium will appear sluggish when rendering the page. After first-paint rendering, zooming in and scroling the page will also prolong busy rendering times.

While Google Chrome busy rendering the page layer, then subsequently visit another website (e.g. example.com, permission.site, etc.) the busy layer will persist on target website, more interestingly sometimes the target page DOM is interactable while page shows the spoofed busy page layers which leads to clickjacking attack.

I can only reproduce this on Chrome for Android, is it possible because of "Multiple Raster Threads: disabled" on Android? I think it's a regression, because on older versions of Chrome it won't feel sluggish when rendering the page so the layer will not persist.

TESTED WORKING ON

- Chrome 94.0.4606.71 on Android 11; Mi 9T
- Chrome Dev 96.0.4655.4 on Android 11; Mi 9T
- Chrome Canary 96.0.4659.3 on Android 11; Mi 9T
- Chrome 94.0.4606.61 on Android 11; Redmi Note 9 Pro
- Chrome Dev 96.0.4655.4 on Android 11; Redmi Note 9 Pro
- Vivaldi Snapshot (UA Chrome/94.0.4606.47) on Android Emulator Pixel\_2\_API\_29 (Play Store edition)

Graphics Feature Status (chrome://gpu) on Mi 9T

- Canvas: Hardware accelerated
- Canvas out-of-process rasterization: Enabled
- Compositing: Hardware accelerated
- Multiple Raster Threads: Disabled
- Out-of-process Rasterization: Hardware accelerated
- OpenGL: Enabled
- Rasterization: Hardware accelerated
- Skia Renderer: Enabled
- Surface Control: Enabled
- Video Decode: Hardware accelerated
- Vulkan: Disabled
- WebGL: Hardware accelerated
- WebGL2: Hardware accelerated

**REPRODUCTION CASE**  

A) Steps to reproduce (location.href)

1. Visit attached spoof-locationhref.html
2. After few seconds the address bar changed to <https://permission.site> while page layer still on spoof-locationhref.html.
3. Try clicking anywhere on the page, sometimes the click will passthrough to permission.site while page layer still on spoof page.

B) Steps to reproduce (window.open)

1. Visit attached spoof-windowopen.html
2. After couple of seconds, tap the page to trigger the window.open
3. While layer still on spoof page, try clicking anywhere on the page, sometimes the click will passthrough to permission.site while page layer still on spoof page.

(If the spoof layer not persist on permission.site as on PoC video, try zooming-in or scrolling the page (to prolong the busy rendering) before tap the page or location.href changed to permission.site)

**CREDIT INFORMATION**  

Irvan Kurniawan (sourc7)

## Attachments

- [spoof-locationhref.html](attachments/spoof-locationhref.html) (text/plain, 765 B)
- [spoof-windowopen.html](attachments/spoof-windowopen.html) (text/plain, 751 B)
- [Busy Rendering Spoof Layer with window.open (interactable clickjack to GitHub).mp4](attachments/Busy Rendering Spoof Layer with window.open (interactable clickjack to GitHub).mp4) (video/mp4, 220.5 KB)
- [Spoof Layer reproducible on Android Emulator Pixel_2_API_29 with Vivaldi UA Chrome 94.0.4606.47.mp4](attachments/Spoof Layer reproducible on Android Emulator Pixel_2_API_29 with Vivaldi UA Chrome 94.0.4606.47.mp4) (video/mp4, 364.3 KB)
- [spoof-windowopen-badssl.html](attachments/spoof-windowopen-badssl.html) (text/plain, 759 B)
- [Spoof layer and click passthrough on security_interstitials page.mp4](attachments/Spoof layer and click passthrough on security_interstitials page.mp4) (video/mp4, 896.0 KB)
- [spoof-locationhref-fps.html](attachments/spoof-locationhref-fps.html) (text/plain, 1.3 KB)
- [spoof-locationhref-badssl-fps.html](attachments/spoof-locationhref-badssl-fps.html) (text/plain, 1.2 KB)
- [spoof layer click passthrough to googlechrome.github.io.mp4](attachments/spoof layer click passthrough to googlechrome.github.io.mp4) (video/mp4, 4.8 MB)
- [trace_android.json.gz](attachments/trace_android.json.gz) (application/octet-stream, 329.3 KB)
- [android-stable.png](attachments/android-stable.png) (image/png, 51.1 KB)
- [crbug40057499-uma-affected-by-preloading.webm](attachments/crbug40057499-uma-affected-by-preloading.webm) (video/webm, 1.2 MB)
- [spoof4-tweaked-rescale1.html](attachments/spoof4-tweaked-rescale1.html) (text/html, 1.2 KB)
- [Screen_Recording_20260123_034711_Chrome_Samsung_S23+.mp4](attachments/Screen_Recording_20260123_034711_Chrome_Samsung_S23+.mp4) (video/mp4, 433.7 KB)
- [spoof4-tweaked-timed-touchscreentest.html](attachments/spoof4-tweaked-timed-touchscreentest.html) (text/html, 832 B)
- [touch_interactable_passthrough_test_Chrome_Samsung_S23+.mp4](attachments/touch_interactable_passthrough_test_Chrome_Samsung_S23+.mp4) (video/mp4, 430.2 KB)
- [Facebook_Tiktok_Request_Access_Chrome.jpg](attachments/Facebook_Tiktok_Request_Access_Chrome.jpg) (image/jpeg, 268.2 KB)
- [Facebook_Canva_Request_Access_Chrome.jpg](attachments/Facebook_Canva_Request_Access_Chrome.jpg) (image/jpeg, 220.8 KB)
- [Facebook_Overlay_Page_One_Tap_Authorize_App_Chrome_Samsung_S23+.mp4](attachments/Facebook_Overlay_Page_One_Tap_Authorize_App_Chrome_Samsung_S23+.mp4) (video/mp4, 1.1 MB)
- [spoof4-tweaked-timed-facebook-authorize.html](attachments/spoof4-tweaked-timed-facebook-authorize.html) (text/html, 1.8 KB)
- [GitHub_Authorize_Apps.jpg](attachments/GitHub_Authorize_Apps.jpg) (image/jpeg, 304.4 KB)
- [GitLab_Authorize_Apps.jpg](attachments/GitLab_Authorize_Apps.jpg) (image/jpeg, 372.0 KB)

## Timeline

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-10-04)

Here the additional PoC video shows reproducible on Android Emulator Pixel_2_API_29 with Vivaldi UA Chrome 94.0.4606.47 using spoof-locationhref.html

### rs...@chromium.org (2021-10-04)

Thanks! I'm tentatively triaging this as Medium, although I believe it may be a "not a bug". That is, this doesn't allow spoofing of the trusted UI, as far as I can tell, but largely refers to the disconnect between the omnibox updating and the page contents rendering. I'm not sure if we consider those security bugs; certainly, it'd be worth reconsidering if you're able to remain and interact with the original page in a way that leads to some confusion.

For example, you mention that it _could_ lead to click jacking, but have you tried to actually gain/retain interactivity with the content in a way that leads to origin confusion?

[Monorail components: Internals>GPU>Rasterization]

### su...@gmail.com (2021-10-04)

It also possible for the spoof layer to persist and click to passthrough to security_interstitials page as in the attached PoC video below.

### [Deleted User] (2021-10-04)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2021-10-04)

> it'd be worth reconsidering if you're able to remain and interact with the original page in a way that leads to some confusion.
> For example, you mention that it _could_ lead to click jacking, but have you tried to actually gain/retain interactivity with the content in a way that leads to origin confusion?

Hi Rsleevi thanks for the update, on the PoC video it shows I able to interact with permission.site GitHub page button, I able to tap the button (on permission.site) while page still on spoofed layer, which redirect to permission.site GitHub page and the spoof layer also still intact for a seconds.

According to Wikipedia https://en.wikipedia.org/wiki/Clickjacking is "a malicious technique of tricking a user into clicking on something different from what the user perceives...", in this case the omnibox already changed to permission.site while attacker able to control the layer. On real scenario attacker able to spoof the layer with "click here" button tricking victim to click i.e Amazon 1-click order, retweet button, like button, delete account button, and etc. so victim unaware that "click here" button on spoofed layer will also click the button on legit website.

However the testcase is still intermittent and device dependent, sometimes the spoof layer is goes away too fast after the omnibox changed and sometimes the click not passthrough as on PoC video.

### rs...@chromium.org (2021-10-04)

Thanks! I'm tentatively triaging this as High - it seems we shouldn't be delivering events until at least one update has been painted, as kenrb@ mentioned. Based on the video, it appears the event is being delivered (in this case, to the "Proceed Anyways" text) before the actual page contents have been displayed.

[Monorail components: UI>Browser>Navigation]

### xi...@chromium.org (2021-10-06)

Given that the page is interactable in this case, severity high seems to be appropriate.

+more folks from Navigation and Paint to shed some light on why the events are delivered before the targeted page is painted. pdr@, tentatively assign to you. Feel free to reroute, thanks!

[Monorail components: Blink>Paint]

### [Deleted User] (2021-10-06)

[Empty comment from Monorail migration]

### sc...@chromium.org (2021-10-06)

The viz compositor is supposed to present a blank white page when the displayed URL switches in situations where the new content is not presented within 5 seconds. That doesn't seem to be happening reliably and I would consider that the first thing to figure out.

Meanwhile, input to the renderer should be disabled when we are either deferring main frame updates or commits for the incoming page, which covers the period from navigation commit to first painted content. However It is also the case that the message to re-enable input comes when the renderer passes the paint information to the compositor, not when the compositor actually puts it on the screen. There may also be a period during load, before we begin deferring main frame updates, during which input will be handled (although we should not be doing anything with it at all because we are not doing main frame updates).

But the above also suggests a problem with the compositor or viz processing frames, in that the content has been committed to cc but it's not getting to the screen fast enough.

I believe this could be fixed once and for all by making use of swap promises to ensure a frame is presented before allowing input, and making tests check for this, and dealing with any other breakage. I recently learned that we have the code to do this because it is a supported WebView API.



[Monorail components: -Internals>GPU>Rasterization Internals>Services>Viz]

### [Deleted User] (2021-10-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pd...@chromium.org (2021-10-08)

I agree that the video in https://crbug.com/chromium/1255485#c4 seems like clickjacking but I spent some time and could not reproduce in chrome 94 on android.

Stephen, do you know who would be a good owner for this?

### su...@gmail.com (2021-10-19)

I've improved the testcase to start spoof when only the FPS is lower (busy rendering started), it now more reliable on across device I tested (Xiaomi Mi 9T, Redmi Note 9 Pro, and Android Emulator Pixel_2_API_29 using Vivaldi Snapshot).

I also attached spoof testcase that redirect to https://googlechrome.github.io/samples/event-istrusted/ in order to demonstrate click able to passthrough to "Generate Trusted Event" button on googlechrome.github.io site when layer still on spoof site.

I've tested this it now works more reliably than previous attached testcase, I hope Chromium team now able to reproduce as in the attached video.

### [Deleted User] (2021-10-21)

schenney: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pd...@chromium.org (2021-10-21)

I uploaded the testcase (spoof-locationhref-fps.html) to https://pr.gg/spoof3.html. I can reproduce on desktop 97.0.4676.0/Canary on desktop (macos) with mobile emulation enabled. I can also reproduce on android.

### ke...@chromium.org (2021-10-26)

As schenney@ mentioned in https://crbug.com/chromium/1255485#c10, if the rendered graphics from the previous page are still visible for more than a few seconds after the URL bar updates, then that might be a separate bug from the clicks being processed before a compositor frame from the new page has been submitted. From the videos it isn't clear to me that the 4-second stale content timer is failing, but that is the first thing to verify. The temporary URL bar mismatch while the new page is rendering is not a bug as long as it is under that time threshold.

### [Deleted User] (2021-11-05)

schenney: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-01-24)

Security marshall ping: this issue has exceeded the 60 day deadline we set for fixing high severity security issues. schenney: can you please urgently follow up on this investigation and help identify what the next steps are to fix it?

### sc...@chromium.org (2022-01-24)

Someone in the Viz team should try to figure out why the frame is not being replaced after 4 seconds as it always should be.

[Monorail components: -Blink>Paint -UI>Browser>Navigation]

### do...@chromium.org (2022-01-24)

+viz people, can you follow up on #23 please?

(FYI schenny, security bugs are restricted to the security team and directly cc'd folks by default, so please prefer to directly assign and cc folks if you need to change component)

### do...@chromium.org (2022-01-24)

*actually +viz folks this time, can you please urgently follow up on #23?

### su...@google.com (2022-01-25)

I don't have an Android device to test on, Kyle can you or someone from viz team take a look?  I'm not sure why we wouldn't show the new page contents immediately after switching to a new page.  The only thing I can think of is that the old page submitted so much GPU work that we can't even display the new page for some time.  In which case the best approach would be to delay handling input events until one frame of the new page is displayed perhaps using SwapPromise as suggested above.

### ky...@chromium.org (2022-01-25)

I can reproduce something with https://pr.gg/spoof3.html on a Pixel 3. It's taking ~7s for old renderer contents to be replaced after the address bar changes. That doesn't seem unexpected though as the 4 second timeout is in the browser process. There is a delay from when the timeout triggers in the browser to when the display shows that update. The browser needs to submit a new CompositorFrame that no longer has the old renderer as a fallback SurfaceId, viz has to receive that compositor frame, trigger a redraw, then the GPU needs to finish any queued up GPU work and pending swaps/frames before the new content is drawn and presented.

The renderer for spoof3.html is sending a ton of raster work to the GPU and keeping the GPU main thread 100% busy. The renderer GPU command buffer will be lower priority than the display compositor normally. If some texture from the renderer is needed for display (aka anything in the renderer CompositorFrame that the browser is embedding) then the GPU scheduler will elevate the renderer GPU command buffer to highest priority. All work issued by the renderer will be run on the GPU main thread until that SyncToken is fulfilled. So if the renderer is issuing a lot of raster work and it's embedded by the browser then the GPU main thread is going to be busy until that work is finished.

I've captured a trace and attached it here. The malicious renderer is sending a non-stop stream of raster work to the GPU process and since it's currently embedded by the display compositor it's getting prioritized over other non-display related GPU work. The navigation timeout starts at 23.3ms and fires at 27.3ms as expected. There are max two pending swaps by the look of things. The display compositor is waiting for previous swap to finish before it starts the next frame at 27.3ms. It's not until 32.07ms that the raster work finishes and the display compositor can start on the next frame. At this point the browser gets the next OnBeginFrame and submits a CompositorFrame that doesn't embed the malicious renderer. That CompositorFrame arrives in viz at 32.08ms.

Since there were two pending swaps at 27.3ms and only one swap returned at 32.07ms there is still one swap happening which embeds the malicious renderer. The raster work for that next frame finished at 35.0ms. At this point the timeout takes effect, the malicious renderer is no longer being embedded (so it's GPU command buffer is no longer prioritized) and the GPU main thread stops being so busy.

Given how the timeout is implemented its WAI that it can take longer than 4 seconds for the timeout update to get presented. Even if we moved the timeout to viz there would still be a delay between timeout triggering and when an update reaches the display since all pending GPU work for previous pending swaps still needs to finish first.

The fact that we are routing input to the new renderer before it's visible seems problematic though.

[Monorail components: UI>Input>Text]

### ky...@chromium.org (2022-01-25)

[Empty comment from Monorail migration]

[Monorail components: -UI>Input>Text UI>Input]

### sc...@chromium.org (2022-01-27)

The solution does indeed seem to be gating input on a swap promise. I can try that mid next week but maybe someone else can get there faster. I would expect it to take a while to land as the last time I tried truly suppressing all input until a renderer->compositor commit I broke the accessibility stuff in ChromeOS.

### ky...@chromium.org (2022-01-27)

Input changes seem like the best way to fix the security concerns here. The way GPU command buffer is currently structured it can't just skip some of the GPU work provided by a client if it's taking too long. Changing that is a big task although it might be more feasible now with all the work being done on raw draw.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### sc...@chromium.org (2022-02-02)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-03-03)

[gpu-triage] Gentle ping

### ad...@google.com (2022-03-28)

schenney@ hopes to work on this this week.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-04-05)

Bumpity!

### sc...@chromium.org (2022-04-06)

Feeling the bump, but also feeling the effects of an infection. This is really next when I get back to coding, at least to see what breaks when forcing input to wait on frame presentation.

### sc...@chromium.org (2022-04-18)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-05-06)

schenney@: Friendly ping from the marshal. Any updates? Thanks!

### sc...@chromium.org (2022-05-09)

I'm going to have to give this up because I have switched teams and have no tiem for the amount of work required. The fix is to:
1) Update the RenderWidgetInputManager (I think ) to block all input on a Compositor SwapPromise for the first committed frame of the new page.
2) Fix the enormous number of teats and features that are likely to break with this.
 (a) Option one is to switch tests to always allow immediate input and have a flag to say a test should not (for tests that are testing the discarded input feature itself). That would reverse the current situation but maybe lead to increased flaky tests.
 (b) Add the same SwapPromise for all tests when synthetic input is requested. That would probably fix a slew of flaky tests too.

ChromeVox (the accessibility features on ChromeOS) broke the last time I tried suppressing input. Something would need to be done there.

### ke...@chromium.org (2022-05-17)

Thanks for the explanation, schenney@.

backer@: Is this something that the Viz folks could pick up?

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ma...@google.com (2022-06-01)

(Another marshal bump. Also just pinged some folks via email.)

### ma...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### ky...@chromium.org (2022-06-01)

I didn't find anything surprising in https://crbug.com/chromium/1255485#c28 around the viz/gpu behaviour. The 4 second timeout is working as expected and the browser produces a new CompositorFrame to clear the old renderer content after 4 seconds. The malicious renderer has queued up so much GPU work it takes a few extra seconds for the new browser CompositorFrame to be presented.

Is there still a chrome team that works on input who would be familiar with the code mentioned in https://crbug.com/chromium/1255485#c40?

### zm...@chromium.org (2022-06-02)

Robert: I don't know who still work in input, but maybe you can help triage?

GPU process can get into this situation on running a slow user shader (from WebGL or WebGPU), so what happened here is not unique. The easiest way to address the security concern is to change the input side behavior, as kylechar pointed out in https://crbug.com/chromium/1255485#c30.

### [Deleted User] (2022-06-03)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-10)

Security marshal here. flackr@, could you help triage this ticket? (will ping as well)

### fl...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### fl...@chromium.org (2022-06-10)

Mehdi, could you look into the change proposed by schenney on https://crbug.com/chromium/1255485#c40 ? I think it makes perfect sense that if the user has not yet seen the new page that we shouldn't send events to it. From the user's point of view they are still interacting with the old site until they can see the new one and since the old site has unloaded already silently dropping the events is the best equivalent of sending them to the old site we can do.

### su...@google.com (2022-06-16)

(gpu triage) gentle ping for an update

### me...@chromium.org (2022-06-20)

I am working on the bug, as stated above, current plan is to drop input events in WidgetInputHandlerManager::DispatchEvent until FirstContentfulPaint happens.

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc?q=WidgetInputHandlerManager::DispatchEvent

### me...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-06-27)

Patch up : https://crrev.com/c/3715237
WebFrameWidgetImpl knows when FirstVisuallyNonEmptyPaint happens, WebFrameWidgetImpl notifies WidgetBase, WidgetBase notifies WidgetInputHandlerManager, and in WidgetInputHandlerManager::DispatchEvent we will drop input events until notified about FirstVisuallyNonEmptyPaint.

When we tested this on a local build we noticed a slight delay between the time a frame is painted and the time user can actually interact with the page. We will land this behind a flag and add some metric to see the delay between the time that the first paint actually happens and time of the first not dropped input event, to see how good or bad it is.


### zm...@google.com (2022-07-07)

Please push on the reviewers to land this sooner

### gi...@appspot.gserviceaccount.com (2022-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40

commit 4db00b9c9a988fb79ed9ddcafbc4c2296619ab40
Author: Mehdi Kazemi <mehdika@chromium.org>
Date: Fri Jul 08 14:25:20 2022

Drop input events until first visually non-empty paint happens

WebFrameWidgetImpl knows when FirstVisuallyNonEmptyPaint happens,
WebFrameWidgetImpl notifies WidgetBase,
WidgetBase notifies WidgetInputHandlerManager,
and in WidgetInputHandlerManager::DispatchEvent we will drop
input events until notified about firstVisuallyNonEmptyPaint.

Bug: 1255485
Change-Id: I0f290663298dfc0a6eecc5f200f4e6e225d05642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715237
Commit-Queue: Mehdi Kazemi <mehdika@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022144}

[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/chrome/browser/flag_descriptions.cc
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/chrome/browser/about_flags.cc
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/public/common/features.h
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/common/features.cc
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/chrome/browser/flag_descriptions.h
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/renderer/platform/widget/widget_base.h
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/renderer/platform/widget/widget_base.cc
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/chrome/browser/flag-metadata.json
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/4db00b9c9a988fb79ed9ddcafbc4c2296619ab40/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h


### me...@chromium.org (2022-07-12)

The change is available on Chrome Canary on Play Store. I tried it on my android phone and cannot reproduce the problem with the URL provided in https://crbug.com/chromium/1255485#c27. I'm working on a metric to make sure the events we are dropping this way are not affecting user experience much.

If you wanna try, make sure you enable the flag first chrome://flags/#drop-input-events-before-first-paint.



### zm...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Services>Viz]

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e43a6100d8083d70cfe4a216d31357ada1da59e2

commit e43a6100d8083d70cfe4a216d31357ada1da59e2
Author: Mehdi Kazemi <mehdika@chromium.org>
Date: Mon Jul 25 20:10:33 2022

Add UMA for suppressed input events

We are planning to drop input events in
WidgetInputHandlerManager::DispatchEvent if user has not seen first
paint yet.
There is a delay between when user actually sees first paint and when
WidgetInputHandlerManager is notified about it. During this time all of
the events (other than move events) will be dropped. We want to record
the number of events that we are going to drop and the delay between the
time of the first (non-move) dropped event and the time
WidgetInputHandlerManager is notified about first paint.

Bug: 1255485
Change-Id: Id54724dcce39ae2ba06b07cd76834ad88fb3e11a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3758367
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Mehdi Kazemi <mehdika@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027921}

[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/tools/metrics/histograms/metadata/page/histograms.xml
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/third_party/blink/renderer/platform/widget/widget_base.h
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/third_party/blink/renderer/platform/widget/widget_base.cc
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/e43a6100d8083d70cfe4a216d31357ada1da59e2/tools/metrics/histograms/metadata/others/histograms.xml


### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-08-09)

Here are the metrics for the implemented solution (Dropping input events before first paint):

PageLoad.Internal.SuppressedEventsCountBeforePaint
https://uma.googleplex.com/p/chrome/timeline_v2?sid=bbdd498ce35e7bb1feb7c710af84b585

PageLoad.Internal.SuppressedEventsTimingBeforePaint
https://uma.googleplex.com/p/chrome/timeline_v2?sid=c676f6aec0b2911d32405aaee61cd512

Will check the results again this week and move on to adding a flag that says input events should not be dropped for tests.


### sc...@chromium.org (2022-08-12)

There's already a flag that many tests use: --allow-pre-commit-input so maybe you could just rename it --allow-pre-paint-input and switch everything over?

There's also this bug, https://bugs.chromium.org/p/chromium/issues/detail?id=1202236, which may offer a better way that can be enabled in all tests that use input. Way back bokan@ tried to do this another way and ran into problems, but something that waits on metrics might be better. See https://chromium-review.googlesource.com/c/chromium/src/+/1663848 for the patch I had when I took over the work.

### [Deleted User] (2022-09-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-09-12)

We are taking a closer look at the results of the metrics, there is a potential behavior regression in the proposed solution (suppressing input events before first paint).
https://uma.googleplex.com/p/chrome/timeline_v2?sid=56b9ddde8aa57400a613b35678bc10da (99, 99.9 percentiles)




### mu...@chromium.org (2022-09-21)

After a through investigation of the timings of incoming signals at WidgetInputHandlerManager, we (mehdika and I) concluded that the lack of a reliable signal about GPU updates is the core problem here.  We were able to record a video where (after the navigation) WIHM::DidFirstVisuallyNonEmptyPaint was called and the new page was shown to the user, but the GPU still switched the buffer to pre-nav content.

See this video [1] at 22~23th second where the screen goes from brown (old content) to github (the new page) then blue again (old content) then finally github page again.

In other words, WIHM state for input suppression [2] needs a signal from the GPU when the GPU is done with pre-nav work.


[1] https://drive.google.com/file/d/1q0xjVwpkkMhNY5zTYdyqxHkd0ALg-3oF/view?usp=sharing
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h;drc=5e23336d543816202a70de6dc6cdf721350adf22;l=342


### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-09-30)

[Security marshal here] Thanks for the update, mustaq@. To clarify, is the conclusion that the fix on https://crbug.com/chromium/1255485#c56 is not sufficient because of the timing issue? Will you be able to work on the actual fix (adding a reliable signal about GPU updates)?

### me...@chromium.org (2022-09-30)

We tried to reproduce What mustaq@ explained in https://crbug.com/chromium/1255485#c65 on a real phone, but we weren't successful.
Yes the fix on https://crbug.com/chromium/1255485#c56 is not sufficient because of the timing issue, at 99.9% users will see the new page for about 1050ms and not able to interact with the page.
We have some update to that fix on https://crbug.com/chromium/1255485#c56 to use shared memory to understand when First Paint happens to get rid of the timing issue.




### me...@chromium.org (2022-09-30)

I'm investigating the shared memory solution, but haven't implemented it yet.

### ye...@google.com (2022-10-11)

[Security Marshal] I chatted with mehdika@ who said he's working on the shared memory solution this sprint, and will have an update next week.

### me...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-11-07)

Hi there, this is your friendly security marshal checking in with a transparency update. I spoke with @mehdika and learned progress is challenged by both the complexity of identifying a viable solution and time pressure from competing priorities. @mehdika and @flackr are working to identify a solution. 

### me...@chromium.org (2022-11-29)

We had a meeting to discuss why the proposed solution at 99.9% is not good (With the proposed solution the user is not able to interact with the new page for about 1100ms after they have seen the new page). 
The problem could be solved by changing the priority of FCP notification sent to WidgetInputHandlerManager (i.e. if we give it the highest priority, then we are sure that it's the fastest way of telling WidgetInputHandlerManager about FCP, even if there is some delay)
With the current version of the solution we are not sure how much of the delay is because of the handling of other input events. 


### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-12-07)

Security marshal here. mehdika@ thanks for the update in https://crbug.com/chromium/1255485#c73. What is the next step at this point? Are you going to try changing the priority of the FCP notification?

### me...@chromium.org (2022-12-12)

We are discussing (with the metrics team) how changing the priority of presentation feedback will affect processing of the other events (because if it increases the priority very high, we will end up in the same situation we have now, i.e. we'll dispatch some of the input events that we shouldn't)

This is one of the metrics on Android-Stable: https://uma.googleplex.com/p/chrome/timeline_v2?sid=8ab23e807ec17537f14c8c6a8f1fbcdd
0ms shows the number of times the behavior was good (i.e. fcp happened then input events were dispatched, no event was a candidate of being dropped, remember the drop only happens when the flag is on) 
0.87% of the times there are some events that are candidates of being dropped, by fixing the priority of the presentation feedback we're looking to see how this number will change, and also make sure the ones we are planning to drop should actually be dropped.


### pd...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-12-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29dac6362abf2b81e4b5820ca8761c3ece12f590

commit 29dac6362abf2b81e4b5820ca8761c3ece12f590
Author: Mehdi Kazemi <mehdika@chromium.org>
Date: Tue Jan 03 16:52:32 2023

Update drop-input-events-before-first-paint flag expiry milestone

Bug: 1255485
Change-Id: I5ba47cc992b8d6c6028335bbe77cfeb9985e014a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133064
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Mehdi Kazemi <mehdika@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088265}

[modify] https://crrev.com/29dac6362abf2b81e4b5820ca8761c3ece12f590/chrome/browser/flag-metadata.json


### [Deleted User] (2023-02-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2023-02-03)

[security marshal] Hi mehdika@, could you provide an update on this ticket?

It looks like you were running some experiments and getting feedback from the Metrics team (https://crbug.com/chromium/1255485#c76). Do you have a plan for next steps?

Thank you

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### fl...@chromium.org (2023-02-08)

The work remaining here is to prioritize the presentation timestamp notification the same as input events and make sure this eliminates events that would be dropped which arrived after the presentation.

There was also a question of whether we are correctly receiving presentation timestamps for subframes - not sure if this has been sorted out. We need to make sure that subframes are getting this message and unblocking input.

### [Deleted User] (2023-03-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-03-27)

Hi mustaq@! Is this something you can make progress on? If not, what's the major blocker? Thanks!

### do...@chromium.org (2023-03-28)

To reinforce #75, this is our third oldest high severity security bug, being open for a year and a half. It would be great to get some attention on it. :)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-04-11)

(pinged mustaq@ offline)

### mu...@chromium.org (2023-04-11)

No progress last week as I originally hoped, sorry.  I had to start supporting another project (SDA) before M114!

### kh...@chromium.org (2023-05-05)

I recently stumbled upon the code for this feature: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc;l=583;drc=e0e0d24aaa54727dc0a8bc4b159ccdf80d3f5d8d.

It looks like we're still routing events to the renderer process but discarding them in the input processing code in the renderer. From a security standpoint, shouldn't this be done in the browser process?

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### mu...@chromium.org (2023-06-09)

> It looks like we're still routing events to the renderer process but discarding them in the input processing code in the renderer. From a security standpoint, shouldn't this be done in the browser process?

The security concern here comes from possible abuse of the dispatched event by the page script, not from the perspective of a compromised renderer process.  If we can figure out a *reliable* way to drop input events in the renderer process, that's all we need here.  In case this question is meant to be about general event handling instead, please note that the renderer has to consider a lot of factors (e.g. if the page has any event handler) to decide if the event should be dropped or not, and this happens only after the browser has already decided to send the event to that renderer.

### an...@chromium.org (2023-06-30)

Hi mustaq@, friendly ping to see if you have any update on this issue - secondary security shepherd

### mu...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

### mu...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/879091558cbaddcde4654df6375d253f48112953

commit 879091558cbaddcde4654df6375d253f48112953
Author: Mustaq Ahmed <mustaq@google.com>
Date: Thu Jul 06 16:10:14 2023

Extend the expiry of the flag drop-input-events-before-first-paint

Bug: 1255485
Change-Id: Id25bf73fb54b23a8caf2a158e4888aa951157680
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4664846
Reviewed-by: Steve Kobes <skobes@chromium.org>
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1166575}

[modify] https://crrev.com/879091558cbaddcde4654df6375d253f48112953/chrome/browser/flag-metadata.json


### mu...@chromium.org (2023-07-07)

My observations on current UMA data:

- PaintHolding.InputTiming3: Do 9.5% of all non-move event-dispatches happen before first paint?  I can’t believe this.  Either I misinterpreted the outcome, or there is an issue with the metric.
  https://uma.googleplex.com/p/chrome/timeline_v2?sid=609ee76aac7566eeea2634fdb3304ff2

- PageLoad.Internal.SuppressedEventsTimingBeforePaint: 24ms at 99p, 1ms at 95p.  The user can’t at all feel the 24ms gap with first paint, so this looks acceptable.
  https://uma.googleplex.com/p/chrome/timeline_v2?sid=4b061e3753c8cea4d4b1c61d58d2e05b

- PageLoad.Internal.SuppressedEventsCountBeforePaint: 19 events at 99p, 1 event at 95p.  I am suspecting that "19" perhaps includes “event batches” from a few interactions.
  https://uma.googleplex.com/p/chrome/timeline_v2?sid=d7fce30b767aa9a72fca8f6eda41319d

### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e91f595a6ad4820dfea365d5299f989ee37a1cea

commit e91f595a6ad4820dfea365d5299f989ee37a1cea
Author: Mustaq Ahmed <mustaq@google.com>
Date: Tue Jul 11 18:44:25 2023

Add UMA for number interactions that could be suppressed before paint

We are planning to drop input events at WidgetInputHandlerManager
DispatchEvent if user has not seen first paint yet.  We already have
an UMA for the number events that would be affected but the count from
the field seems too large at the 99th percentile.  We suspect this is
because of suppressed swipes since each swipe dispatches at least 9
events from WIHM (a single swipe typically dispatches the following
events in order: TouchStart, GestureTapDown, GestureShowPress,
GestureTapCancel, GSB, TouchScrollStarted, some GSUs, TouchEnd and
GSE).  In our experiments, we frequently got 15+ events from a short
swipe.

In this CL, we are adding an alternate UMA for number of affected user
interactions.  If this number turn out to be small (a few), it should
be okay to drop all events from those few interactions.

OBSOLETE_HISTOGRAMS=PaintHolding.InputTiming3 was replaced by PaintHolding.InputTiming4 on 2023-07-11

Bug: 1255485
Change-Id: I73f59b459b775c4ad887bd2ce24d2566d16b5e30
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4670946
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1168852}

[modify] https://crrev.com/e91f595a6ad4820dfea365d5299f989ee37a1cea/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h
[modify] https://crrev.com/e91f595a6ad4820dfea365d5299f989ee37a1cea/tools/metrics/histograms/metadata/page/histograms.xml
[modify] https://crrev.com/e91f595a6ad4820dfea365d5299f989ee37a1cea/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc
[modify] https://crrev.com/e91f595a6ad4820dfea365d5299f989ee37a1cea/tools/metrics/histograms/metadata/others/histograms.xml


### mu...@chromium.org (2023-07-20)

We will look into the field data after 2 weeks.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-08-16)

[secondary shepherd] Hi mustaq@, could you please share an update on the findings from the field data?

### mu...@chromium.org (2023-08-16)

We have newly added UMA data available from Canary and Dev channels:

- PaintHolding.InputTiming4: The question from https://crbug.com/chromium/1255485#c98 remains...how is it possible to have ~9% of all non-move event-dispatches before first paint?
https://uma.googleplex.com/p/chrome/timeline_v2?sid=9d2e72571d527c5436c9eb3ceee467a3

- PageLoad.Internal.SuppressedInteractionsCountBeforePaint: 1 interaction at 95p, 1.9 at 99p looks okay, supports our hypothesis in https://crbug.com/chromium/1255485#c98 that "event batches" are affecting PageLoad.Internal.SuppressedEventsCountBeforePaint.
https://uma.googleplex.com/p/chrome/timeline_v2?sid=a2ee4156c56e216ec9cdfee453a97a7f

### fl...@chromium.org (2023-08-16)

Given that the P99 of PageLoad.Internal.SuppressedEventsTimingBeforePaint is well less than 100ms, we can probably turn this feature on to resolve the security issue and fix the priority of the FCP notification later right?

### mu...@chromium.org (2023-08-16)

I agree...PageLoad.Internal.SuppressedEventsTimingBeforePaint at P99 is significantly below 100ms:
- Below 24ms is Stable: https://uma.googleplex.com/p/chrome/timeline_v2?sid=00f532b86717a54026095c5d86cea8c8
- ~60ms in Canary/Dev: https://uma.googleplex.com/p/chrome/timeline_v2?sid=6357b0595fa0c21d28e29ae615274a89


### mu...@chromium.org (2023-08-16)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-09-06)

> we can probably turn this feature on to resolve the security issue and fix the priority of the FCP notification later right?

Hi mustaq@ can we ship the drop-input-events-before-first-paint to user? Currently I see this one is blocked on https://crbug.com/chromium/1361208, I hope the https://crbug.com/chromium/1361208 able to get resolved, so we can turn on the drop-input-events-before-first-paint by default to resolve this security issue (mark this as Fixed). Thanks!

### mu...@chromium.org (2023-09-06)

Yes, that's the plan: investigate the blocked issue which occurs when drop-input-events-before-first-paint is enabled.

### mu...@chromium.org (2023-09-27)

FYI the blocker issue is caused by the fact that a cross-origin frame never receives a layout lifecycle update signal (we are working on a fix now).

For this bug, we need to add an UMA to verify that similar problem doesn't happen on the topmost frame; looks like waiting for 10secs should be enough:
https://uma.googleplex.com/p/chrome/timeline_v2?sid=02b82ae48f298a96c270154fb1d74d87

### mu...@chromium.org (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-11-02)

Hello, security shepherd here. Is the fix for #111 completed?

Can we resolve the security portion of this bug, then work on followups as needed if there are further concerns? This has been a known security issue for 2 years now, which does not match with our expectations for the Chrome product.

### mu...@chromium.org (2023-11-02)

We resolved the main blocker (https://crbug.com/chromium/1361208) few weeks ago.  The other bug (https://crbug.com/chromium/1490296) is not a blocker, correcting the dependency now.

To expose the fix that's behind a flag now (https://chromium-review.googlesource.com/c/chromium/src/+/4803165), we still need a new UMA to confirm that the topmost frame always receives layout lifecycle update.

### bo...@google.com (2023-11-06)

@mustaq, thanks for all your persistence. From https://crbug.com/chromium/1255485#c115 it sounds like there will be another delay to get UMA metrics to confirm the fix. What's the expected time frame for that feedback cycle? 

### mu...@chromium.org (2023-11-06)

In the unlikely case we can push the new UMA metric into M120, we would get a solid signal by mid-Dec.  Otherwise, Mid Jan.

I mentioned "unlikely" because M120 has branched already, and I am not sure if I can commit to it this week among other priorities.

### el...@chromium.org (2023-11-24)

Secondary security shepherd: marking NextAction for mid-January of 2024. Thanks for sticking with this :)

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-08)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### mu...@chromium.org (2024-01-25)

By the end of the week we are expecting to update our existing histograms to cover the missing paint signal case (see https://crbug.com/chromium/1255485#c111).

### gi...@appspot.gserviceaccount.com (2024-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c8dbe86cdc5b404edd99fd9997ebd0ecfa95d4a1

commit c8dbe86cdc5b404edd99fd9997ebd0ecfa95d4a1
Author: Mustaq Ahmed <mustaq@google.com>
Date: Wed Jan 31 18:16:13 2024

Updated UMA to detect missing first-paint signal at top frame

Behind a flag we already have a fix for the bug.  The fix suppresses
input to the page until first paint signal arrives.  Before we flip the
flag, we want to make sure that the topmost frame always receives the
signal, in order to rule out the possibility of input event starvation.

OBSOLETE_HISTOGRAM[PageLoad.Internal.SuppressedEventsCountBeforePaint]=Replaced by PageLoad.Internal.SuppressedEventsCountBeforePaint2
OBSOLETE_HISTOGRAM[PageLoad.Internal.SuppressedEventsTimingBeforePaint]=Replaced by PageLoad.Internal.SuppressedEventsTimingBeforePaint2
OBSOLETE_HISTOGRAM[PageLoad.Internal.SuppressedInteractionsCountBeforePaint]=Replaced by PageLoad.Internal.SuppressedInteractionsCountBeforePaint2

Bug: 1255485
Change-Id: Ic87bae3a2cd7364740ffb5d4071b25b0f9452a8f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5142727
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1254608}

[modify] https://crrev.com/c8dbe86cdc5b404edd99fd9997ebd0ecfa95d4a1/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h
[modify] https://crrev.com/c8dbe86cdc5b404edd99fd9997ebd0ecfa95d4a1/tools/metrics/histograms/metadata/page/histograms.xml
[modify] https://crrev.com/c8dbe86cdc5b404edd99fd9997ebd0ecfa95d4a1/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc


### mu...@chromium.org (2024-01-31)

We will now wait for the new histograms.

### fl...@chromium.org (2024-02-01)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1255485?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1361208]
[Monorail blocking: crbug.com/chromium/1490296]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-19)

The NextAction date has arrived: 2024-02-19

### mu...@chromium.org (2024-02-22)

Something seems terribly off with the new UMA data PageLoad.Internal.SuppressedEventsTimingBeforePaint2! In M123 (which is still mostly in Dev/Canary) we are seeing the following histogram buckets:

- below 1ms: 65.24%,
- above 10sec: 33.61%

<https://uma.googleplex.com/p/chrome/timeline_v2?sid=340a317c1cc7aa9f8707c30d866f9067>

This is not reliable hence not actionable.

### mu...@chromium.org (2024-02-27)

Two possible causes of the UMA anomalies we experienced in this bug a few times so far:

- I encountered `WidgetInputHandlerManager::DidNavigate` getting called twice per navigation, which interfered with timer start a few times for me locally. Below are the stack traces for the first and second calls in order. It is not clear to me why we had the first call added [here](https://chromium-review.googlesource.com/c/chromium/src/+/3715237/13/third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc).

```
#3 blink::WidgetInputHandlerManager::DidNavigate()
#4 blink::WidgetInputHandlerManager::Create()
#5 blink::WidgetBase::InitializeCompositing()
#6 blink::WebFrameWidgetImpl::InitializeCompositingInternal()
#7 blink::WebFrameWidgetImpl::InitializeCompositing()
#8 content::RenderFrameImpl::CreateMainFrame()
#9 content::AgentSchedulingGroup::CreateWebView()
#10 content::AgentSchedulingGroup::CreateView()

#3 blink::WidgetInputHandlerManager::DidNavigate()
#4 blink::WebFrameWidgetImpl::DidNavigate()
#5 blink::LocalFrameClientImpl::DispatchDidCommitLoad()
#6 blink::DocumentLoader::CommitNavigation()
#7 blink::FrameLoader::CommitDocumentLoader()
#8 blink::FrameLoader::CommitNavigation()
#9 blink::WebLocalFrameImpl::CommitNavigation()
#10 content::RenderFrameImpl::CommitNavigationWithParams()

```

- The latest UMA data suggests to me me that [`WebFrameWidgetImpl::PresentationCallbackForMeaningfulLayout`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/web_frame_widget_impl.cc;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090;l=3133) occasionally gets a zero `first_paint_time`. If this is the case, I won't be surprised because the `first_paint_time` parameter seemed to remain unused for a while, maybe because of changes in caller's expectations. We need to dig deeper into this.

### pe...@google.com (2024-03-04)

The NextAction date has arrived: 2024-03-04 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ap...@google.com (2024-03-05)

Project: chromium/src
Branch: main

commit 0fc2b8c904f431d4a7106f8e70c5ba20442be8f0
Author: Mustaq Ahmed <mustaq@google.com>
Date:   Tue Mar 05 21:09:41 2024

    Suppress possible double-counting of the UMA for input suppression
    
    Behind a flag we already have a fix for the bug.  The fix suppresses
    input to the page until first paint signal arrives.  Before we flip
    the flag, we want to make sure that the topmost frame always receives
    the signal, in order to rule out the possibility of input event starvation.
    
    The UMA data seems to have a problem, we encountered too many
    occurrences for PageLoad.Internal.SuppressedEventsTimingBeforePaint2
    when max-delay is reached.  This CL fixes two possible causes of the anomaly:
    
    - If WIHM is re-used across a navigation, the max-delay timer was not
      reset, and this possibly caused wrongly counting such a navigation
      if it happened within 15 sec.
    
    - We are suspecting that the `first_paint_time` received by
      WIHM::RecordEventMetricsForPaintTiming maybe zero even when
      max-delay is not reached.  See comment#148 in the bug.  To isolate
      the UMA from being affected by this possibility, we are passing a
      separate boolean parameter to indicate max-delay reached.
    
    The CL also fixed uninitialized `suppressing_input_events_state_`, and renamed `WIHM::DidNavigate` to better reflect its purpose.
    
    Bug: 40057499
    Change-Id: I509ed40821208f44fa969207aa78abdbd1dd022d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5332511
    Reviewed-by: Robert Flack <flackr@chromium.org>
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1268690}

M       third_party/blink/renderer/core/frame/web_frame_widget_impl.cc
M       third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc
M       third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h

https://chromium-review.googlesource.com/5332511


### pe...@google.com (2024-03-18)

The NextAction date has arrived: 2024-03-18 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### su...@gmail.com (2024-04-04)

mustaq@ is there an update on UMA data after commit on [comment #150](https://issues.chromium.org/issues/40057499#comment150)?

### df...@google.com (2024-04-12)

PLEASE NOTE:
This added flakiness to a bunch of tests, which were sending input after the page reported as loaded.

We added a workaround for new, Kombucha-based tests using `WebContents::CompletedFirstVisuallyNonEmptyPaint()` to prevent sending certain types of inputs before the page is painted (see [this CL](https://chromium-review.googlesource.com/c/chromium/src/+/5410959) for details). This does not, however, fix flakiness in old-style interactive\_ui\_tests, so there may just be various regressions as a result.

There is also the separate [issue 332895669](https://issues.chromium.org/issues/332895669) which means that in Lacros tests on Linux with Wayland, `WebContents::CompletedFirstVisuallyNonEmptyPaint()` intermittently *never* becomes true, resulting in all manner of bugs due to this new behavior. Right now we are recommending people work around the flakiness as well as possible, possibly disabling tests on Lacros, but that's not a great long-term solution.

In general, in the future, please let the Chrome Desktop UI team (and specifically me) know if you make further changes to the design that could generate race conditions with input processing.

### mu...@chromium.org (2024-04-12)

[dfried@google.com](mailto:dfried@google.com): Could you please clarify which tests are mentioned in #153? Our changes here are still behind a flag!

### df...@google.com (2024-04-12)

Huh. So erikchen@ and I have been trying to track down intermittent test failures, and we believed that one of the CLs on this thread changed Chrome behavior so that WebContents would not accept input events until they had received their first contentful paint. I can pick back through our discussion, but it's also possible we misinterpreted when this rule was created.

Note that if any of these changes were enabled in fieldtrial\_testing\_config.json, that would be sufficient to cause the issues; even if they are behind a DISABLED\_BY\_DEFAULT flag.

It looks like this behavior (drop input events before paint) has been part of chrome for a while, but was introduced after many tests were written that did not take this into account. I guess it's just a rare enough issue that we only noticed the source of the flakiness recently. It's possible that it was exacerbated by recent Wayland work that might have caused the bug I mentioned in my previous comment.

### mu...@chromium.org (2024-04-17)

The updated UMA data from M124 Beta (and Dev/Canary too) shows very similar histogram buckets that already confused us ~2 months ago (in #147 above):

- below 1ms: 62.73%,
- above 10sec: 36.30%

<https://uma.googleplex.com/p/chrome/timeline_v2?sid=a7b0eee4a135d2045d17eb52f98ca33e>

It seems impossible that so many first-paint signals could be getting delayed >10s without us seeing a high volume of bug reports. The only other conclusion I can make at this point is that the first-paint hookup we are using is not reliable! I will be happy to learn that I missed something here!!!

### mu...@chromium.org (2024-04-17)

I am unable to repro the bug on desktop, even with mobile emulation (unlike #16).

### fl...@chromium.org (2024-04-18)

I expect that the cases in which it repros is some particular situation that you've not recreated.

It's probably better to either

1. Look at how other first paint metrics work and see what the difference is here. E.g. it seems odd that PageLoad.PaintTiming.NavigationToFirstPaint is reported only half as many times as this metric so unless half of pages loaded never report, or
2. Dig into where specifically we don't get to notifying about first paint. E.g. it looks like we schedule this notification from WebFrameWidgetImpl::DidMeaningfulLayout. If we knew how often we got there, we should be able to get an idea whether we are missing calls to DidMeaningfulLayout or whether sometimes NotifyPresentationTime does not successfully notify. There may be pre-existing metrics to get some of this data, or we could add new ones if needed.

### mu...@chromium.org (2024-04-24)

I investigated how the first paint signal works in practice both for normal page loads and for the repro in #16 above, and didn't observe any missing signal or duplicate signal problem.

FYI I was able to repro the problem consistently on an emulated device in Android Developers Studio and never on my Linux desktop.

---

I observed an anomaly in setting/resetting bits in `suppressing_input_events_state_` both on emulator and on desktop: quite frequently `WIHM::InitializeInputEventSuppressionStates` resets the `kDeferMainFrameUpdates` bit while turning on the `kHasNotPainted` bit.

- The code suggests this is deliberate but I don't quite see why; any suggestions welcome.
- The `kDeferMainFrameUpdates` bit seems unrelated to the UMA in question here (PageLoad.Internal.SuppressedEventsTimingBeforePaint2), I am trying to confirm this now.

### mu...@chromium.org (2024-04-24)

The anomaly I mentioned above is not relevant, it only affects a different histogram.

### mu...@chromium.org (2024-04-25)

Because on desktop we are seeing ~1/3 of first-paint-delays in the 10+ sec bucket, I tried browsing quite a few sites with the hope that I would spot a real 10+ sec delay in a `DidFirstVisuallyNonEmptyPaint` call. I spotted none in my local build with logging!

Anyway, I sent out <https://chromium-review.googlesource.com/c/chromium/src/+/5485266> to aid our UMA analysis in case the reported delay in first paint may be noisy.

### mu...@chromium.org (2024-04-29)

While investigating a possible UMA problem, I encountered the missing first-contentful-point signal case twice while using back/forward buttons between two pages. The exact condition is still not clear.

### mu...@chromium.org (2024-04-30)

We finally have a clear answer to the UMA discrepancy: a preloading/prerendering heuristic somewhere for a previously visited is causing the initiation of `WidgetInputHandlerManager` way before the page is shown. See the attached video, where:

- navigating to a non-cached page at [0:13] causes the initiation to happen "normally" after hitting <enter> on address bar, but
- navigating to a cached page at [0:25] causes the initiation to happen too early---at the moment the typed address gets auto-completed, even before hitting <enter>!

(This also corrects the observation in #162: back/forward navigation is not the real cause.)

### ap...@google.com (2024-05-01)

Project: chromium/src
Branch: main

commit 9d9540c3188ed9aa6d9ed92ede67136247004831
Author: Mustaq Ahmed <mustaq@google.com>
Date:   Wed May 01 18:53:00 2024

    Extend the expiry of drop-input-events-before-first-paint
    
    We need more time to investigate any possible impact of the existing
    fix.
    
    Bug: 40057499
    Change-Id: I82987978e610a7d612d1fd1e25bfa4022e1d2962
    Fixed: 335052506
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5505050
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
    Reviewed-by: Kevin Ellis <kevers@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1294981}

M       chrome/browser/flag-metadata.json

https://chromium-review.googlesource.com/5505050


### mu...@chromium.org (2024-05-08)

Rob and I decided to make the following changes to related histograms:

- Isolate PageLoad.Internal.SuppressedEventsTimingBeforePaint2 from Prerendring by starting the timer on event dispatch which would make it closer to our goal.
- Add a new Boolean histogram to log timeout.
- Possibly update PaintHolding.InputTiming4 logging to exactly match the event suppression logic.

### mu...@chromium.org (2024-05-30)

We are expecting to land in a few days the change for the first two bullets in [Comment#165](https://issues.chromium.org/issues/40057499#comment165).

### ap...@google.com (2024-06-04)

Project: chromium/src
Branch: main

commit f95480a21202c8d584c9214cc524240d1ae4f95c
Author: Mustaq Ahmed <mustaq@google.com>
Date:   Tue Jun 04 19:41:30 2024

    Add a new histogram to log missing first paint after event dispatch.
    
    Our data suggests that the existing SuppressedEventsTimingBeforePaint
    is perhaps affected by noisy first paint timing.  Moreover, our
    timeout logic was affected in the wild by early initialization of
    WidgetInputHandlerManager through pre-rendering.
    
    This CL updates the related histograms as follows:
    - adds the histogram SuppressedEventsBeforeMissingFirstPaint that is
      logged only if no paint signal is received in 15sec after the first
      event dispatch, and
    - logging of 3 existing histograms is modified very slightly: the
      timeout bucket will be logged 15 sec after the first dispatch (vs
      after WIHM initiation).
    
    OBSOLETE_HISTOGRAM[PageLoad.Internal.SuppressedEventsCountBeforePaint2]=Replaced by PageLoad.Internal.SuppressedEventsCountBeforePaint3
    OBSOLETE_HISTOGRAM[PageLoad.Internal.SuppressedEventsTimingBeforePaint2]=Replaced by PageLoad.Internal.SuppressedEventsTimingBeforePaint3
    OBSOLETE_HISTOGRAM[PageLoad.Internal.SuppressedInteractionsCountBeforePaint2]=Replaced by PageLoad.Internal.SuppressedInteractionsCountBeforePaint3
    
    Bug: 40057499
    Change-Id: I0c058cc485c89e8864704bb0676eafe01709e90d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5485266
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org>
    Reviewed-by: Robert Flack <flackr@chromium.org>
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
    Reviewed-by: Ian Clelland <iclelland@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1310120}

M       third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc
M       third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.h
M       tools/metrics/histograms/metadata/page/histograms.xml

https://chromium-review.googlesource.com/5485266


### mu...@chromium.org (2024-06-04)

We will watch the Beta numbers a week after M127 branch.

### pe...@google.com (2024-06-17)

The NextAction date has arrived: 2024-06-17
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pg...@google.com (2024-06-17)

Thank you for the fix!!

Is the third bullet (`Possibly update PaintHolding.InputTiming4 logging to exactly match the event suppression logic.`) in [comment #165](https://issues.chromium.org/issues/40057499#comment165) required to mark this bug as fixed (=fixed in main, but may need merges)?

### mu...@chromium.org (2024-06-18)

pgrace@: This is not fixed yet, we are still trying to confirm that the fix won't suppress real user interactions.

### mu...@chromium.org (2024-06-18)

We have *preliminary data* from the new/updated metrics:
<https://uma.googleplex.com/p/chrome/timeline_v2?sid=01b2629f209b764c5b0c1e10f6fc2fad>

- PageLoad.Internal.SuppressedEventsBeforeMissingFirstPaint is true 9.62% of the time, which is still higher than we expected!
- PageLoad.Internal.SuppressedEventsTimingBeforePaint3 10+sec bucket exactly matched the above 9.62%. This disproves the last hypothesis in [Comment#161](https://issues.chromium.org/issues/40057499#comment161) ("the reported delay in first paint may be noisy").

### mu...@chromium.org (2024-07-10)

The latest UMA shows ~10% cases are missing the first paint signal. The number is much lower (below 1%) in non-Windows platforms.

Next step for us: we will look into where the WIHM "first paint" notification is coming from. We previously suspected it may be wrongly linked to "meaningful paint" so switching it to something closer to "FCP" would be the right solution.

### ar...@chromium.org (2024-08-08)

*secondary security shepherd*

Hello Mustaq,
Did you manage to make progress the last month about #173 ?

### mu...@chromium.org (2024-08-21)

Unfortunately no progress on #173! It involves a quite bit of investigation and code changes...hoping to get back in a few weeks.

### ad...@google.com (2024-09-08)

mustaq@ JFYI this is our second-oldest high severity security bug - hoping you'll find time to make progress soon, or could you put it on your Q4 OKRs?

### mu...@chromium.org (2024-09-09)

Dedicating a part of Q4 for this makes sense. (I don't have bandwidth in the last few weeks in Q3.)

### pe...@google.com (2024-09-30)

The NextAction date has arrived: 2024-09-30
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### mu...@chromium.org (2024-10-01)

I am planning to focus on this bug next week (Oct 7), in particular the next step mentioned in #173.

### mu...@chromium.org (2024-10-01)

Another point that came up yesterday (thanks to rbyers@) is that if we end up suppressing all input in the "intermediate state" (i.e. the state that page B is loaded but didn't get painted), the browser should somehow communicate the "suppressed state" to the user.

### mm...@chromium.org (2024-10-01)

(This is a long thread. I tried to read the history but I might have missed some of the specifics, so sorry if some of the suggestions are not relevant).

My understanding is there are a few distinct issues on this thread:

- Which paint should we mark? There was some iteration through history but FCP seems to be the new direction?
- We have a race between FCP.presentation\_time (since feedback takes time to process) and Event.timeStamp (which is scheduled and prioritized differently)

Idea: After paint but before presentation feedback for the paint, could we manage a queue of WebInputEvents which might have a timestamp that comes after presentation time? We could work on prioritization of presentation feedback to decrease the latency gap, but it would at least mean we dont (a) dispatch events that were sent to a misplaced frame, while (b) not dropping more events than needed.

---

IMHO if the event.timeStamp is only a few ms larger than the presentation time of the previous paint, dropping that event is not likely a UX concern. Except for testing & automation use cases, it seems impossible for a user to have a real interaction this quickly after first paint.

---

We're seeing in INP data that there are still a lot of interactions reported before FCP. I'm seeing in Chrometto traces examples of users "rage clicking" for many seconds which the new page isn't loaded.

I wonder if its possible if new features are increasing the likelihood here? Perhaps cross-document view transitions, more prerendering, or fancy animating back navigations...

### mm...@chromium.org (2024-10-02)

I investigate some "Interactions before FCP" use cases based on field data, and I think FCP isn't always well behaved.  Some of the data might be skewed not because of early interactions but because of artificially late/missing FCP.

If we intend to filter events until a paint, we migth want to stick to First Paint not First Contentful Paint.  Or, fix FCP.

### fl...@chromium.org (2024-10-02)

> Which paint should we mark? There was some iteration through history but FCP seems to be the new direction?

Any paint is fine, as long as the user isn't seeing / trying to interact with the previous page's visuals anymore, to avoid the previous page directing the user to click on something that has a different meaning on the new page.

Note arguably we may want to drop events even near after the paint for the same reason. E.g. imagine the previous page navigates away leaving a retry button visible, which the user taps in frustration until the page responds (i.e. loads the new page) where the position of the button results in a click performing some detrimental action.

### mm...@chromium.org (2024-10-02)

Agreed. Similar to layout shifts, the user requires some minimum time after content shifts/swaps before we can expect they meant to interact with that new target.

Further, even after the user sees the correct target they want to interact with, I think sites tend to require even more time before actually being ready to accept events, anyway (as discussed at TPAC last week).

### an...@chromium.org (2024-10-25)

*secondary shepherd*

Hi mustaq@, just checking in to see if there is any update on your end since c#179,#180. Thanks!

### mu...@chromium.org (2024-10-25)

I resumed the work earlier this week, looking into the PaintHolding direction.

### pe...@google.com (2024-11-09)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-24)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mu...@chromium.org (2024-12-06)

In the last few days, the particular Android emulator I used reproduced the bug for several seconds consistently (I meant the time gap between the address bar switching to the new site and the new site getting painted). That gave me a large enough time window to confirm two important things:

- I was able to send input to the unpainted page to initiate a navigation there, [video1](https://drive.google.com/file/d/14CiU42ma8ZeNDEYv9wacSQTS6K0GNn-5/view?usp=drive_link&resourcekey=0-5JrCSatSwZDQwToyuoXJOA). Details: in the video I made a few clicks between 17s-19s at a location where the new page would show a link, then I moved the mouse off the page. When the new page is finally visible at the 23s mark, one of the past clicks navigates to the link (which opens a second tab in this case).
- Unfortunately the "paint" signal used by the paint-holding feature no longer looks like a solid solution to this problem, [video2](https://drive.google.com/file/d/1LwJP7mXcura77lDIPYbxgh_BEVddddQP/view?usp=drive_link&resourcekey=0-bsPEa04G_8jyDwo4hj9oiw). Details: I added a console log at [RWHI OnRenderFrameMetadataChangedAfterActivation](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_impl.cc;drc=5103ac6102b144aff2bb3b45fe525521ecf3320d;l=3769) which is the signal to the browser that the renderer has sent a frame to viz. In the video, the newly-loaded page receives the signal right before the 8s mark but the page is visible only after 12s. To confirm that the signal received at the 8s mark was logged at the correct RWH, I scrolled the page near the end of the video and observed the same RWH address. Thanks to [vmpstr@chromium.org](mailto:vmpstr@chromium.org) for his help with this investigation.

### mu...@chromium.org (2024-12-06)

We are still planning to drop all input events received until `RWHI::RenderFrameMetadataChangedAfterActivation` gets called: it will serve as a mitigation (vs a complete solution). In video2 in [Comment #189](https://issues.chromium.org/issues/40057499#comment189), this will reduce the clickjacking window by ~2s (the address bar switches to the new URL at the 6s mark while the metadata signal is received at the 8s mark).

### mu...@chromium.org (2024-12-10)

We now have the first prototype to suppress input events in the browser until the renderer has produced content: <https://crrev.com/c/6085077>

This works fine on my local Linux build but Android emulator occasionally becomes unresponsive. I am now dry-running it hoping to find a test that finds the crack. In the meantime I would appreciate a quick initial review. FYI [vmpstr@chromium.org](mailto:vmpstr@chromium.org).

### ap...@google.com (2024-12-17)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6094543>

Add UMAs for first metadata signal to renderer host.

---


Expand for full commit details
```
Add UMAs for first metadata signal to renderer host. 
 
We are planning to skip sending input events from the renderer host to 
the renderer until the renderer has pushed some content to viz.  We will 
do this only for the renderer that has become visible (unhidden) at 
least once, to avoid sending events to pre-renderered pages. 
 
This CL adds UMAs to confirm that the two signals (for unhiding and for 
content update from the renderer) are sane, therefore the planned 
solution won't block input in valid use-cases. 
 
Bug: 40057499 
Change-Id: I7430dbe2e92101d18d58107d36ba1e201cdc87ff 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6094543 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Chris Harrelson <chrishtr@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1397310}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_manager.cc`
- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`
- M `tools/metrics/histograms/metadata/renderer/histograms.xml`

---

Hash: deef671671127ea87e0c7a6241031f94da6ac63f  

Date:  Tue Dec 17 07:34:49 2024


---

### mu...@chromium.org (2025-01-14)

The initial UMA data (from Canary and Dev) is not immediately actionable!

- Renderer.ContentProduction.DelayFromUnhide looks great (between 120~300ms depending on OS).
- Renderer.ContentProduction.SignalReceived is not "mostly true" as we have been expecting (only between 24% on CrOS and 71% on Android).

<https://uma.googleplex.com/p/chrome/timeline_v2?sid=527ece2d74e30e1e756f9a1da06be7e3>

### mu...@chromium.org (2025-01-17)

My local repros confirmed that the UMA discrepancy in [Comment #193](https://issues.chromium.org/issues/40057499#comment193) is caused by subframes. Subframe are known to be safe, see [Issue 40074208](https://issues.chromium.org/issues/40074208).

I just created an RBS blocker bug ([Issue 390568192](https://issues.chromium.org/issues/390568192)) to have the UMA fixed asap.

### ap...@google.com (2025-01-20)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6179761>

Fix UMAs for first metadata signal to renderer host

---


Expand for full commit details
```
Fix UMAs for first metadata signal to renderer host 
 
This CL fixes UMAs we added previously to limit to top-frame only. We 
already confirmed that the bug does not repro in subframes, see 
https://issues.chromium.org/40074208. 
 
We are planning to skip sending input events from the renderer host 
to the renderer until the renderer has pushed some content to viz. 
We will do this only for the top-frame renderers that have become 
visible (unhidden) at least once, to avoid sending events to 
pre-renderered pages. 
 
Bug: 40057499 
Fixed: 390568192 
Change-Id: I4f3da29fb2b61654e64f53bfe6426bd9a0c50243 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6179761 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1408767}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`

---

Hash: 9622d3c7c14d4b67ffb8add61f80e54dd0059ec9  

Date:  Mon Jan 20 12:39:36 2025


---

### ap...@google.com (2025-01-21)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6187850>

Fix UMAs for first metadata signal to renderer host

---


Expand for full commit details
```
Fix UMAs for first metadata signal to renderer host 
 
This CL fixes UMAs we added previously to limit to top-frame only. We 
already confirmed that the bug does not repro in subframes, see 
https://issues.chromium.org/40074208. 
 
We are planning to skip sending input events from the renderer host 
to the renderer until the renderer has pushed some content to viz. 
We will do this only for the top-frame renderers that have become 
visible (unhidden) at least once, to avoid sending events to 
pre-renderered pages. 
 
(cherry picked from commit 9622d3c7c14d4b67ffb8add61f80e54dd0059ec9) 
 
Bug: 40057499 
Fixed: 391329375 
Change-Id: I4f3da29fb2b61654e64f53bfe6426bd9a0c50243 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6179761 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1408767} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6187850 
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org> 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Auto-Submit: Harry Souders <harrysouders@google.com> 
Owners-Override: Harry Souders <harrysouders@google.com> 
Cr-Commit-Position: refs/branch-heads/6943@{#616} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`

---

Hash: 5cefb8651fa96e44b4124a4e7e87e27b6674cbe0  

Date:  Tue Jan 21 13:20:39 2025


---

### ap...@google.com (2025-01-22)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6190729>

UMAs for metadata signal to host: skip self-owned RenderWidgets

---


Expand for full commit details
```
UMAs for metadata signal to host: skip self-owned RenderWidgets 
 
Self-owned widgets are for popups like color/date-time chooser or 
<select> elements.  We don't need to include them in our UMA. 
 
Bug: 40057499 
Fixed: 390568192 
Change-Id: I57e326005d0c2fce95c7d0fc2bf4f5f0cf15e3d5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6190729 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1409953}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`

---

Hash: ee14308a51d49191fa1fde5294f64820fd86dd84  

Date:  Wed Jan 22 14:00:07 2025


---

### ap...@google.com (2025-01-23)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6191093>

UMAs for metadata signal to host: skip self-owned RenderWidgets

---


Expand for full commit details
```
UMAs for metadata signal to host: skip self-owned RenderWidgets 
 
Self-owned widgets are for popups like color/date-time chooser or 
<select> elements.  We don't need to include them in our UMA. 
 
(cherry picked from commit ee14308a51d49191fa1fde5294f64820fd86dd84) 
 
Bug: 40057499 
Fixed: 391844634 
Change-Id: I57e326005d0c2fce95c7d0fc2bf4f5f0cf15e3d5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6190729 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1409953} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6191093 
Cr-Commit-Position: refs/branch-heads/6943@{#747} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`

---

Hash: 846e53013f8010f58cf7ae20088cab60112191d8  

Date:  Thu Jan 23 10:01:48 2025


---

### mu...@chromium.org (2025-01-27)

The [initial](https://uma.googleplex.com/p/chrome/timeline_v2?sid=1b548337c25e4f68e8c8ed8a960a679b) Renderer.ContentProduction.SignalReceived data from the UMA improvements above look promising on Android but not great on desktop platforms.

### ap...@google.com (2025-01-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6204301>

[CodeHealth] Remove RWHI new\_content\_rendering\_delay methods.

---


Expand for full commit details
```
[CodeHealth] Remove RWHI new_content_rendering_delay methods. 
 
Only one of these methods are used, and that has an alternate. 
 
Bug: 40057499 
Change-Id: If4505ee2a9f620762c123c71a3f600e478e9a62b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6204301 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1412263}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.h`
- M `content/browser/renderer_host/render_widget_host_view_aura_unittest.cc`

---

Hash: 8c00153ff50c482e058f46d5f61a10fa86a8af1a  

Date:  Tue Jan 28 06:26:31 2025


---

### ap...@google.com (2025-01-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6204441>

UMAs for metadata signal to host: consider browser 4sec deadline

---


Expand for full commit details
```
UMAs for metadata signal to host: consider browser 4sec deadline 
 
If the browser doesn't see the metadata signal within a 4sec delay (as 
defined by new_content_rendering_timeout_), we will release input 
events without waiting further for the metadata signal (fallback). 
 
This CL updates the internal state to consider this case as if the 
metadata signal was received. 
 
Bug: 40057499 
Change-Id: I9a02787b6e078dd81a31198ca482fb3c01bb1d6c 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6204441 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1412264}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`

---

Hash: 86e933d958e55136c21c012e697bd9c949e4fcc8  

Date:  Tue Jan 28 06:28:28 2025


---

### mu...@chromium.org (2025-01-28)

jonross@: Here is a [video](https://drive.google.com/file/d/16hL0XNtibmF14Ety8D--F0xzTjknK8fF/view?usp=drive_link&resourcekey=0-dVcjzLEyXG4a48sJ3ZVdiA) where Page A (site pr.gg) is visible when the mouse is clicked at 0:24sec, and then the click went to Page B (github.io) to follow a link there to Page C (github.com). See the [trace](https://drive.google.com/file/d/1uwws-BFmgI2AIA0U2V-Iu8-p-dNHj_iQ/view?usp=drive_link&resourcekey=0-LI2wf4ncscwE1rLxHWgD1A) recorded in the video.

### mu...@chromium.org (2025-01-28)

Here is a second pair of [video](https://drive.google.com/file/d/1GaL11nQGTnLVcMyD2xWpKFL0cVmsNxPQ/view?usp=drive_link&resourcekey=0-VK0S1pIhKAVNn01gQYtDjw) and [trace](https://drive.google.com/file/d/108SYDCapV5VBfUGJiGSlnJDmldENYik8/view?usp=drive_link&resourcekey=0-YxM0Qz7KHijXmmImSF9ORw) where the click on Page B didn't cause a navigation there.

### mu...@chromium.org (2025-01-28)

Apparently the FCP signal (at `LocalFrameView::OnFirstContentfulPaint`) is not a good signal for us because the video in [comment#203](https://issues.chromium.org/issues/40057499#comment203) shows this signal coming *before* the content metadata signal at the browser (see the console log at 0:11). Is this order expected?

### jo...@chromium.org (2025-01-29)

I've requested access to the videos/traces. Is there a slice id for the `LocalFrameView::OnFirstContentfulPaint` in the trace from #203?

### jo...@chromium.org (2025-01-29)

So it seems that `LocalFrameView::OnFirstContentfulPaint` is tied to when Blink is done preparing the PaintOps. Which is before frame submission. `PaintTiming::ReportPresentationTime` is the callback that gets registered to receive `viz::FrameTimingDetails`, that doesn't currently have an associated trace.

The trace from #203 is a bit odd, as it seems to show the Renderer submitting frames early that are listed as "Paritally Presented". Around the "Global First Contentful Paint". However the actual Blink up then ends up being much slower: <https://screenshot.googleplex.com/3PTvXD4HiqA8UqV> I suspect that `PaintTiming::ReportPresentationTime` would be triggered at the end of that long `PipelineReporter` with Slice id `29995`

### mu...@chromium.org (2025-01-30)

"the actual Blink up then ends up being much slower": that's odd because renderer pid=18102 is Page B (github.io) in the trace in [Comment#202](https://issues.chromium.org/issues/40057499#comment202), which seems like a lightweight page. Any chance this only "appears" longer because it got blocked on something? The video shows that this renderer appeared only momentarily while it received the tap way before that moment of time.

### mu...@chromium.org (2025-01-30)

On a related investigation, I tried a few special Chrome pages (chrome://settings etc) and found the paintholding signal getting received every time.

### ap...@google.com (2025-02-04)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6216039>

Add UMAs to track lifespan of a renderer host since shown

---


Expand for full commit details
```
Add UMAs to track lifespan of a renderer host since shown 
 
We are planning to skip sending input events from the renderer host to 
the renderer until the renderer has pushed some content to viz. We will 
do this only for the renderer that has become visible (unhidden) at 
least once, to avoid sending events to pre-renderered pages. 
 
To verify that the planned solution won't block input in valid 
use-cases, this CL adds 3 UMAs to check that the renderer hosts that 
never receive content update signals from renderers are short-lived: 
- navigation to commit delay, 
- lifespan from commit, and 
- lifespan from first shown. 
Also updates a past UMA to record missing data as zero, like the added 
UMAs above. 
 
Bug: 40057499 
Change-Id: Ib3e845debf3ac49a91af94bcb91b30299d8b7462 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6216039 
Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
Reviewed-by: Chris Harrelson <chrishtr@chromium.org> 
Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
Commit-Queue: Chris Harrelson <chrishtr@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1415641}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`
- M `tools/metrics/histograms/metadata/renderer/histograms.xml`

---

Hash: 53a45c96a19536b3a3bdc5444206fdd823244640  

Date:  Tue Feb 04 09:54:58 2025


---

### mu...@chromium.org (2025-02-04)

I explored FCP today and ruled it out as a possible signal to unblock input because of the same challenges we faced here with FMP (see [Comment #173](https://issues.chromium.org/issues/40057499#comment173)): on both [Windows](https://uma.googleplex.com/p/chrome/timeline_v2?sid=87e24f0cfe1423cebe67446366f53df3) and [Android](https://uma.googleplex.com/p/chrome/timeline_v2?sid=7e224324b2528f5be901b63be4476c6d), the users see ~10sec delay in FCP ~1% of the time.

### mu...@chromium.org (2025-02-05)

Two good news on the browser-side paint-holding front:

- Our update to `Renderer.ContentProduction.SignalReceived` ([Comment #201](https://issues.chromium.org/issues/40057499#comment201)) to correctly include paint-holding 4sec deadline now shows [80-93%](https://uma.googleplex.com/p/chrome/timeline_v2?sid=7c163e4a319b5059cd09ff2358c218ea) signal availability on all platforms!
- We finally have a consistently reproducible explanation for the high rate of missing signal cases: repeatedly hit a history nav button (back or forward) to skip over "heavyweight" pages. We believe this explains the missing signal cases, we are still waiting for the timing data from [Comment #209](https://issues.chromium.org/issues/40057499#comment209) to confirm this hypothesis.

### ap...@google.com (2025-02-11)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6253186>

UMAs for metadata signal to host: exclude non-primary frame tree

---


Expand for full commit details
```
UMAs for metadata signal to host: exclude non-primary frame tree 
 
While the last UMA we added shows a positive correlation between the 
missing metadata signal case and short-lived RWHs, we have about 4x 
other cases w/o RWH lifespan data.  We believe most of those cases 
are for non-primary frames (where `compositor_metric_recorder_` is 
null) but those cases also include primary frames that never received 
commit signals. 
 
This CL updates the UMA to exclude non-primary frames so that we can 
confirm that missing the commit signal case is rare. 
 
Bug: 40057499 
Change-Id: I725f790682ba56bc03145aaaa3a349658c7a7aca 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6253186 
Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1418959}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_impl.cc`

---

Hash: ea8675d166ffee39fcb4fc3d9e20d0ba00ae59ec  

Date:  Tue Feb 11 15:43:21 2025


---

### ap...@google.com (2025-02-12)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6250222>

[CodeHealth] Drop the feature kDropInputEventsBeforeFirstPaint

---


Expand for full commit details
```
[CodeHealth] Drop the feature kDropInputEventsBeforeFirstPaint 
 
It was a WIP fix for a bug.  We are not pursuing a different solution. 
 
Bug: 40057499 
Change-Id: Ifffb08c5d7aa4ef9eb2a2121a1578cbeca80a6b8 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6250222 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1419255}

```

---

Files:

- M `chrome/browser/about_flags.cc`
- M `chrome/browser/apps/link_capturing/link_capturing_navigation_throttle_browsertest.cc`
- M `chrome/browser/flag-metadata.json`
- M `chrome/browser/flag_descriptions.cc`
- M `chrome/browser/flag_descriptions.h`
- M `chrome/browser/web_applications/web_app_link_capturing_parameterized_browsertest.cc`
- M `third_party/blink/common/features.cc`
- M `third_party/blink/public/common/features.h`
- M `third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc`

---

Hash: 066ca56f586d27252aef6e5526907bfc3a17d3cf  

Date:  Wed Feb 12 06:27:29 2025


---

### ap...@google.com (2025-02-19)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6085077>

Drop input events in the browser until the renderer produces content.

---


Expand for full commit details
```
Drop input events in the browser until the renderer produces content. 
 
This CL lands the first prototype solution behind a new flag 
kDropInputEventsWhilePaintHolding.  The solution is to start the 
InputRouter in an inactive state for any user-visible top frame while 
paint-holding is active. 
 
We still have quite a few test failures if we enable this feature.  We 
will fix them through follow-up CLs. 
 
Bug: 40057499 
Change-Id: Id98c27ac635fe6a71f4f84b50e1b2e7acc9fe1bd 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6085077 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Reviewed-by: Robert Flack <flackr@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1422193}

```

---

Files:

- M `components/input/input_router.h`
- M `components/input/input_router_impl.cc`
- M `components/input/mock_input_router.h`
- M `components/input/render_input_router.cc`
- M `content/browser/renderer_host/input/input_router_impl_unittest.cc`
- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `third_party/blink/common/features.cc`
- M `third_party/blink/public/common/features.h`

---

Hash: 917cd517d194ff4eadbf25bdd8b0052973729e17  

Date:  Wed Feb 19 13:59:55 2025


---

### mu...@chromium.org (2025-02-20)

Risk analysis: The latest data suggests that the last commit above, when enabled, would work at least 98+% of the time.

- The paint-holding signal is missing in ~13% cases ([Renderer.ContentProduction.SignalReceived](https://uma.googleplex.com/p/chrome/timeline_v2?sid=432b8d035a2c522db82d78c09c680a23) is "false").
- Within that missing bucket, the RWH lives longer than than 4sec (the paint-holding timeout) for about ~15% of the cases ([Renderer.ContentProduction.LifespanFromUnhide](https://uma.googleplex.com/p/chrome/timeline_v2?sid=0501e875f2e5ec34b114af1e2101541d)).
- 15% x 13% is 1.95%.

Today's email discussion concluded that we need to consider Chrome error pages as a special case for the above analysis. WIP.

### ap...@google.com (2025-02-21)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6286768>

RenderFrameHostImpl: Record commit times for error pages.

---


Expand for full commit details
```
RenderFrameHostImpl: Record commit times for error pages. 
 
`SendCommitFailedNavigation` did not record commit times, which made 
it impossible to isolate (for UMA purposes) the error pages that are 
short-lived. 
 
Bug: 40057499 
Change-Id: Ibf95c96cbaeb1c3755f851b52d5f69ac76177283 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6286768 
Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1423167}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`

---

Hash: 4dd8031dbcafed6347db03dfc26b40944043ab07  

Date:  Fri Feb 21 08:32:12 2025


---

### ap...@google.com (2025-02-27)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6305181>

Notify RWH about paint-holding state, whether active or not.

---


Expand for full commit details
```
Notify RWH about paint-holding state, whether active or not. 
 
We use this signal to properly set RWH input-router event suppression 
state.  We only care about input-suppression for RWHs that has/had 
paint-holding active. 
 
Bug: 40057499 
Change-Id: Idcfdfb9f0b9e975ca5ace3713de60488bf6acea9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6305181 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1425749}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_manager.cc`
- M `content/browser/renderer_host/render_widget_host_impl.cc`
- M `content/browser/renderer_host/render_widget_host_impl.h`
- M `content/browser/renderer_host/render_widget_host_unittest.cc`
- M `content/browser/renderer_host/render_widget_host_view_aura_unittest.cc`

---

Hash: f70e9bcff08b08af874fac8d897c834fc350f096  

Date:  Thu Feb 27 07:59:44 2025


---

### ap...@google.com (2025-02-27)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed <[mustaq@google.com](mailto:mustaq@google.com)>  

Link:      <https://chromium-review.googlesource.com/6188131>

Fix RenderWidgetHostTest input router active state.

---


Expand for full commit details
```
Fix RenderWidgetHostTest input router active state. 
 
This change is a no-op when DropInputEventsWhilePaintHolding feature 
is disabled, and makes the test passing when enabled. 
 
Bug: 40057499 
Change-Id: I17ffb0bfd16e01bd240198cb8e017abc8a5cd62b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6188131 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1425973}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_unittest.cc`

---

Hash: 1215d731963c47dbf1d19adf8c2e1883c6eeed7c  

Date:  Thu Feb 27 14:07:53 2025


---

### me...@google.com (2025-03-14)

[Secondary security shepherd] Hi mustaq@, this is one of the oldest open bugs in the security queue. Could you provide a quick update? Thanks!

### mu...@chromium.org (2025-03-17)

Last week we completed a risk analysis for our planned fix (suppress input events while paint-holding) and concluded that the risk factor is ~0.05%: <https://docs.google.com/document/d/1h7iYh34Yw5tOs-mA0IuTyrnvkm0k1gI1fHMFl8EgMz4/edit?usp=sharing&resourcekey=0-D2A9YN5DBnCUBt7a_KPk0w>

We are planning to kickoff a 50% Beta trial for the fix after we have all browser tests green (~6 more to fix).

### dx...@google.com (2025-03-24)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6382598>

Restore InputRouter state after RenderInputRouter switches it.

---


Expand for full commit details
```
     
    Most RenderInputRouter seems to switch to a new InputRouter soon after 
    the RenderWidgetHost was constructed, not clear why.  In our case, this 
    means the new InputRouter's active state must match the state from the 
    old instance initialized at RenderWidgetHostImpl ctor. 
     
    Bug: 40057499 
    Change-Id: I61ecc220aca7732ba6367ffa1fec7a2e1edb631a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6382598 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1436901}

```

---

Files:

- M `components/input/render_input_router.cc`

---

Hash: a4640b229ed8147846fb55559aff9d92c5f7864d  

Date:  Mon Mar 24 16:26:09 2025


---

### dx...@google.com (2025-04-01)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6392535>

Fix PrerenderBrowserTest dependency on paint-holding input suppression

---


Expand for full commit details
```
     
    These tests utilize input events and are agnostic to paint-holding. 
     
    Bug: 40057499 
    Change-Id: Iddf3dc74c545df5facc35b4fc4e0ebcac82a011c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6392535 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1441039}

```

---

Files:

- M `content/browser/preloading/prerender/prerender_browsertest.cc`

---

Hash: 7fbbd7f8817513bbf94443c390cabe4040398db1  

Date:  Tue Apr 1 17:56:30 2025


---

### dx...@google.com (2025-04-03)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6427062>

Fix browser\_tests that don't need to wait for paint-holding for input

---


Expand for full commit details
```
     
    Tests that are paint-holding agnostic need to end paint-holding before 
    sending input events to the page.  We are expecting to suppress input 
    events to a page during the paint-holding period (this is currently 
    behind the flag `kDropInputEventsWhilePaintHolding`). 
     
    Bug: 40057499 
    Change-Id: Ia8eb410afb9707f308e3ea3e0f04ce26448f769c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6427062 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1442198}

```

---

Files:

- M `chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc`
- M `chrome/browser/ui/blocked_content/popup_tracker_browsertest.cc`
- M `chrome/browser/ui/web_applications/test/web_app_navigation_browsertest.cc`
- M `content/public/test/browser_test_utils.cc`
- M `content/public/test/browser_test_utils.h`

---

Hash: 149d660576fa52b4f6b60a8ab29dc88196912a0e  

Date:  Thu Apr 3 16:07:22 2025


---

### dx...@google.com (2025-04-03)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6426988>

Fix PrerenderBrowserTest parent class dependency on paint-holding

---


Expand for full commit details
```
     
    These tests utilize input events and are agnostic to paint-holding. 
     
    This is our second attempt to fix the prerender test here, by moving 
    the flag to the parent test class. 
     
    Bug: 40057499 
    Change-Id: I47670f7c95f31977f096e557ece1b48701c6c2ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6426988 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1442316}

```

---

Files:

- M `content/browser/preloading/prerender/prerender_browsertest.cc`

---

Hash: 924a60679e2b0ef725b8f3a46dbbfbc4c12bb2e9  

Date:  Thu Apr 3 18:39:25 2025


---

### dx...@google.com (2025-04-03)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6431006>

Fix RenderWidgetHostTouchEmulatorBrowserTest with paint-holding.

---


Expand for full commit details
```
     
    The test utilizes input events and is agnostic to paint-holding. 
     
    Bug: 40057499 
    Change-Id: I394f4fe18a101be5f61b9be627246eddcac7453c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6431006 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Commit-Queue: Avi Drissman <avi@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1442391}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_browsertest.cc`

---

Hash: ba5ff5d451107e82ce3bb90c0e7e935d50533463  

Date:  Thu Apr 3 20:35:34 2025


---

### dx...@google.com (2025-04-17)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6459663>

Make ui\_test\_utils::NavigateToURL\* independent of paint-holding

---


Expand for full commit details
```
     
    The tests relying on ui_test_utils::NavigateToURL* methods expect to 
    interact with the loaded page after the navigation is complete, and they 
    are agnostic to paint-holding. Paint-holding is the browser feature to 
    continue to show a snapshot of the pre-navigation page (instead of a 
    blank page) until the renderer for the post-navigation page has pushed 
    content to the GPU. 
     
    We are planning to hold back input events from a page while 
    paint-holding is active, to mitigate a bug with user interactions with a 
    stale page. That change would make a few tests in 
    PasswordGenerationInteractiveTest.* unresponsive to input. 
     
    This CL forces an end to paint-holding after the navigation waits to 
    preserve the coverage by the affected tests. 
     
    Bug: 40057499 
    Change-Id: If3a9bafef94494c5074d9e9e3ca473463fd25f72 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6459663 
    Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1448356}

```

---

Files:

- M `chrome/test/base/ui_test_utils.cc`

---

Hash: 10e69a876fdea6bcee450615e99f9b1e81da4450  

Date:  Thu Apr 17 16:17:31 2025


---

### dx...@google.com (2025-04-17)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6462774>

Fix a SignInViewControllerBrowserTest paint-holding expectation

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The test modified here sends an input event to a page without waiting 
    for the end of paint-holding. Because the test is not related to 
    paint-holding, we are adding a forced end of paint-holding w/o affecting 
    the test's purpose. 
     
    Bug: 40057499 
    Change-Id: Ib814a26cdf7d8981e63d473404b941dee15bf660 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6462774 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Alex Ilin <alexilin@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1448366}

```

---

Files:

- M `chrome/browser/ui/signin/signin_view_controller_interactive_uitest.cc`

---

Hash: c2a831d65c8a314076af7d36a64a24f314c33056  

Date:  Thu Apr 17 16:29:37 2025


---

### dx...@google.com (2025-04-23)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6478308>

Unlink inspector-protocol InputInjector from PaintHolding.

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active.  Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until 
    the renderer for the post-navigation page has pushed content to the 
    GPU. 
     
    Because inspector-protocol input injection use-cases are disjoint 
    from the problem we are fixing in this bug, we are excluding these 
    injected events from our input-hold-back plan. 
     
    Bug: 40057499 
    Change-Id: I9cf2a569ce6320fa2a870963355e80b495aa1434 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6478308 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1450587}

```

---

Files:

- M `content/browser/devtools/protocol/input_handler.cc`

---

Hash: 95685daa270ab4081139f1a7471e5077010bf757  

Date:  Wed Apr 23 16:00:18 2025


---

### dx...@google.com (2025-05-01)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6495719>

RenderWidgetHostViewAuraBrowserMockIMETest paint-holding expectation

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The tests modified here send input events to pages without waiting for 
    the end of paint-holding. Because the test is not related to 
    paint-holding, we are adding a forced end of paint-holding w/o affecting 
    the test's purpose. 
     
    Bug: 40057499 
    Change-Id: I75b5657b09cc7c5c6eb91592f6ad46dd6ada3a38 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6495719 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1454637}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_aura_vk_browsertest.cc`

---

Hash: 54b9376556b725cf9d6a0ba9ac9e64a90b6badf5  

Date:  Thu May 1 20:15:21 2025


---

### dx...@google.com (2025-05-01)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6500975>

QuickAnswersBrowserTest: fix paint-holding dependency.

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The test modified here sends an input event to pages without waiting for 
    the end of paint-holding. Because the test is not related to 
    paint-holding, we are adding a forced end of paint-holding w/o affecting 
    the test's purpose. 
     
    Bug: 40057499 
     
     
    Enable for testing. 
     
    Change-Id: I0a585d4d2c4336c1a2eb8e80354a6347e575e9d3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6500975 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Xiaohui Chen <xiaohuic@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1454649}

```

---

Files:

- M `chrome/browser/ui/ash/quick_answers/quick_answers_browsertest_base.cc`

---

Hash: 87351620d164c665bff923cb557f9e57dff2d86a  

Date:  Thu May 1 20:27:32 2025


---

### dx...@google.com (2025-05-02)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6501100>

RenderWidgetHostViewMacTests should signal "no paint-holding"

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    Most of the tests here send input events to mock RHWs for which there is 
    no paint-holding. This CL signals the mock RWHs accordingly to make them 
    responsive to input events. 
     
    Bug: 40057499 
    Change-Id: I8a62ac100a9384eb81b4026bcd0457a315e428ae 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6501100 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1454962}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_mac_unittest.mm`

---

Hash: 5d9e32331d47d96abbb05cc4f4adf4088edb2b34  

Date:  Fri May 2 14:01:19 2025


---

### dx...@google.com (2025-05-06)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6501475>

Correct paint-holding expectation in HostedOrWebAppTest.CtrlClickLink

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The test modified here sends input events to pages without waiting for 
    the end of paint-holding. Because the test is not related to 
    paint-holding, we are adding a forced end of paint-holding w/o affecting 
    the test's purpose. 
     
    Bug: 40057499 
    Change-Id: Iffcb701ac67d4d18629271cf65431fbd927cdc20 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6501475 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Alan Cutter <alancutter@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1456327}

```

---

Files:

- M `chrome/browser/ui/extensions/hosted_app_browsertest.cc`

---

Hash: 7a62454a11190ac97e736aa1a3733ddd7e0ac8a2  

Date:  Tue May 6 14:55:17 2025


---

### dx...@google.com (2025-05-09)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6512615>

UrlOverridingTest.java: fix click in testRedirectToTrustedCaller

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The test modified here sends click the pages without waiting for 
    renderer content. Because the test is agnostic to paint-holding, we are 
    ending paint-holding early to keep the test working. 
     
    Bug: 40057499 
     
    Change-Id: I78af0b4cf338978782165a658e8eb706b2bd65a0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6512615 
    Commit-Queue: Yaron Friedman <yfriedman@chromium.org> 
    Reviewed-by: Yaron Friedman <yfriedman@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1458100}

```

---

Files:

- M `chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java`
- M `content/public/test/android/javatests/src/org/chromium/content_public/browser/test/util/WebContentsUtils.java`
- M `content/public/test/android/web_contents_utils.cc`

---

Hash: 21c2f04d4724be8d4202f992e1f3dace9617359d  

Date:  Fri May 9 14:31:57 2025


---

### dx...@google.com (2025-05-09)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6520012>

Make 5 Android WebView test classes compatible to paint-holding

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The tests affected here send input events to test pages, and they can no 
    longer do so immediately after the page load. Since these tests are 
    agnostic to point-holding, we are simulating end of paint-holding right 
    after page loads and keep these tests working after the above change. 
     
    Bug: 40057499 
    Change-Id: Ib99be746422ca60f51457bd8b0186faa54b6d2a8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6520012 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Commit-Queue: Bo Liu <boliu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1458123}

```

---

Files:

- M `android_webview/javatests/src/org/chromium/android_webview/test/AwAutofillTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/AwContentsClientOnRendererUnresponsiveTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/AwContentsClientShouldInterceptRequestTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/AwZoomTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/WebKitHitTestTest.java`

---

Hash: 66846ff23565254550a3f2ae8e2d792036857201  

Date:  Fri May 9 15:24:16 2025


---

### dx...@google.com (2025-05-09)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6525526>

Make 4 more Android WebView test classes compatible to paint-holding

---


Expand for full commit details
```
     
    This is a follow-up fix to https://crrev.com/c/6520012 for 4 more 
    classes where input events are sent to test pages without waiting for an 
    end of paint-holding. 
     
    Bug: 40057499 
    Change-Id: I92b330e3cd4746a478ea417e4fff8430bd7ef1c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6525526 
    Commit-Queue: Bo Liu <boliu@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1458374}

```

---

Files:

- M `android_webview/javatests/src/org/chromium/android_webview/test/ClientOnReceivedHttpErrorTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/ContextMenuTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/PopupWindowTest.java`
- M `android_webview/javatests/src/org/chromium/android_webview/test/WebViewModalDialogOverrideTest.java`

---

Hash: da29495ee048e0205de38d88b98127a49fbd6bb0  

Date:  Fri May 9 22:18:04 2025


---

### dx...@google.com (2025-05-12)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6532632>

Make AndroidScrollIntegrationTest's compatible to paint-holding

---


Expand for full commit details
```
     
    This is another (probably the last) follow-up fix to 
    https://crrev.com/c/6520012: fixes tests in the class where input 
    events are sent to test pages without waiting for an end of 
    paint-holding. 
     
    Bug: 40057499 
    Change-Id: Ib9dcc8853bf4cd3cada5238dade721d68aebf5d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6532632 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1458861}

```

---

Files:

- M `android_webview/javatests/src/org/chromium/android_webview/test/AndroidScrollIntegrationTest.java`

---

Hash: 9b1a46b419829c3e12442204af9feb6da2694bd7  

Date:  Mon May 12 15:20:21 2025


---

### dx...@google.com (2025-05-12)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6533139>

Fix two DownloadContentTest's that sometimes fail for paint-holding

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    These tests send input events to RHWs without waiting for 
    paint-holding.  They occasionally pass perhaps because the "work" 
    before input dispatch usually takes longer than paint-holding. 
     
    This CL makes the tests independent of paint-holding timing. 
     
    Bug: 40057499 
    Change-Id: I34cce45bf57952cff7bd28c93ecb77c295d42818 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6533139 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1459051}

```

---

Files:

- M `content/browser/download/download_browsertest.cc`

---

Hash: 66ecf73d8b4ccc4521cb6babcfed1daa0e714de6  

Date:  Mon May 12 20:06:29 2025


---

### dx...@google.com (2025-05-13)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6537247>

BtmTabHelperBrowserTest: fix one test's reliance on paint-holding

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    BtmTabHelperBrowserTest.ChromeBrowsingDataRemover_Basic sends input 
    events to RHWs without waiting for paint-holding.  This CL makes the 
    test independent of paint-holding timing. 
     
    Bug: 40057499 
    Change-Id: I627bd267b190c375adb99c6c18408bd66eb4f176 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6537247 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1459715}

```

---

Files:

- M `content/browser/btm/btm_helper_browsertest.cc`

---

Hash: 9966f10e1418a791b49eaa0db420e57af3d55683  

Date:  Tue May 13 21:15:42 2025


---

### dx...@google.com (2025-05-14)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6546458>

Skip input suppression in Android WebViews.

---


Expand for full commit details
```
     
    Input suppression was added in `widget_host` to avoid sending user 
    events to a page whose URL is different from the one shown in the 
    address bar.  Android WebViews don't show URLs, so input suppression 
    don't apply there. 
     
    Bug: 40057499 
    Change-Id: I5d8b8e048ebb3e8f77d6f2312ecacfac2bec9a9f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6546458 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1460145}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_android.cc`

---

Hash: e923ccbf431e8429cabc3fd08c99dd2079b70e2f  

Date:  Wed May 14 16:15:55 2025


---

### dx...@google.com (2025-05-15)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6533981>

Disable paint-holding input-suppression in 2 InputOnVizTest's

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    We have been fixing tests that would be affected by the input 
    suppression, and the common solution we applied is to simulate the end 
    of paint-holding after a page-load. All other 100+ tests have been 
    resolved, and the two tests here turned to be challenging. Because 
    InputOnViz is not a shipped yet, we are disabling input-suppression for 
    these tests to be able to start a finch trial for that feature. 
     
    Bug: 40057499 
    Change-Id: I9757cb1ed443ee92a7240438d4efa36cd8d7609c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6533981 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Theresa Sullivan <twellington@chromium.org> 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1460778}

```

---

Files:

- M `chrome/android/javatests/src/org/chromium/chrome/browser/input/InputOnVizTest.java`

---

Hash: e5bda4d25f11b2d13dd893c0eebf7429ab308d17  

Date:  Thu May 15 16:20:28 2025


---

### dx...@google.com (2025-05-15)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6553062>

RenderWidgetHostViewAuraBrowserMockIMETest paint-holding fix pass 2

---


Expand for full commit details
```
     
    This is a follow-up CL to https://crrev.com/c/6495719: the 3 tests 
    here fail only occasionally (flaky), and we missed them in the first 
    pass. 
     
    Bug: 40057499 
    Change-Id: Icdaabafb892b8dd991e45380011ca637c81ba3ef 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6553062 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1460906}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_aura_vk_browsertest.cc`

---

Hash: 5f5118a221cdeb2a5d280232311f2a2e70e6cea8  

Date:  Thu May 15 19:37:55 2025


---

### dx...@google.com (2025-05-15)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6552338>

BtmTabHelperBrowserTest pass 2 fix for paint-holding input suppression

---


Expand for full commit details
```
     
    This is a follow-up CL to https://crrev.com/c/6537247: the 2 tests 
    here fail occasionally (flaky), missed our radar at the first pass. 
     
    Bug: 40057499 
    Change-Id: I64d81c808f704961b89ad201c8c8a5a02d7bb2d3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6552338 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1460957}

```

---

Files:

- M `content/browser/btm/btm_helper_browsertest.cc`

---

Hash: d51114d9fac65f6447e2fc36711f1140a61439c4  

Date:  Thu May 15 20:49:25 2025


---

### dx...@google.com (2025-05-15)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6479262>

Field trial config for DropInputEventsWhilePaintHolding

---


Expand for full commit details
```
     
    Bug: 40057499 
    Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1460996}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04  

Date:  Thu May 15 21:36:52 2025


---

### dx...@google.com (2025-05-16)

Project: chromium/src  

Branch: main  

Author: [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6551985>

Revert "Field trial config for DropInputEventsWhilePaintHolding"

---


Expand for full commit details
```
     
    This reverts commit c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04. 
     
    Reason for revert: 
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5117201427202048 
     
    Sample build with failed test: https://ci.chromium.org/b/8714768220467717649 
    Affected test(s): 
    [ninja://content/test:content_browsertests/BackForwardCacheBrowserTest.TextInputStateUpdated](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fcontent%2Ftest:content_browsertests%2FBackForwardCacheBrowserTest.TextInputStateUpdated?q=VHash%3A2594b7c85d1b7e63) 
     
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5117201427202048&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F6479262&type=BUG 
     
    Original change's description: 
    > Field trial config for DropInputEventsWhilePaintHolding 
    > 
    > Bug: 40057499 
    > Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1460996} 
    > 
     
    Bug: 40057499 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I9350be1bdbe6d9f065f11efb57e45480cb0b18b4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6551985 
    Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Owners-Override: Stefan Zager <szager@google.com> 
    Reviewed-by: Stefan Zager <szager@chromium.org> 
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1461120}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: b06aac33c77f6f4ce99297d3972c8d8eeb030b21  

Date:  Fri May 16 01:53:20 2025


---

### dx...@google.com (2025-05-16)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6557424>

Make two content-browsertests aware of paint-holding input-suppression

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    We have been fixing tests that would be affected by the input 
    suppression, and this two on mac15-arm64-rel-testsmissed our radar. 
     
    Bug: 40057499 
    Change-Id: I397c468a984262b6b0ff453519d7f650ac730e5a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6557424 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1461661}

```

---

Files:

- M `content/browser/back_forward_cache_browsertest.cc`
- M `content/browser/renderer_host/render_widget_host_browsertest.cc`

---

Hash: 17d4e67a6c021690c6d3c61fd91e31a624df7cf2  

Date:  Fri May 16 22:27:34 2025


---

### dx...@google.com (2025-05-19)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6557064>

Reland "Field trial config for DropInputEventsWhilePaintHolding"

---


Expand for full commit details
```
     
    This is a reland of commit c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04 
     
    Original change's description: 
    > Field trial config for DropInputEventsWhilePaintHolding 
    > 
    > Bug: 40057499 
    > Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1460996} 
     
    Bug: 40057499 
    Change-Id: I73b5b71ba7debed55de18a5c6bfaa098a5aa0472 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6557064 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1462453}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: cbadbe77927a08dfc6728054417ceb25b62b56a4  

Date:  Mon May 19 21:52:17 2025


---

### dx...@google.com (2025-05-20)

Project: chromium/src  

Branch: main  

Author: Yifan Luo [lyf@chromium.org](mailto:lyf@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6567425>

Revert "Reland "Field trial config for DropInputEventsWhilePaintHolding""

---


Expand for full commit details
```
     
    This reverts commit cbadbe77927a08dfc6728054417ceb25b62b56a4. 
     
    Reason for revert: [Gardener] Test failures 
     
    Bug: 40057499 
    Original change's description: 
    > Reland "Field trial config for DropInputEventsWhilePaintHolding" 
    > 
    > This is a reland of commit c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04 
    > 
    > Original change's description: 
    > > Field trial config for DropInputEventsWhilePaintHolding 
    > > 
    > > Bug: 40057499 
    > > Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    > > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1460996} 
    > 
    > Bug: 40057499 
    > Change-Id: I73b5b71ba7debed55de18a5c6bfaa098a5aa0472 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6557064 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1462453} 
     
    Bug: 40057499, 418929575 
    Change-Id: Iac8822fc7f824ad7023ac19603bb2d2a4160126d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6567425 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Yifan Luo <lyf@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1462651}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: 3013ae9076c517ec36753362c231359fbcfe6fc7  

Date:  Tue May 20 09:18:11 2025


---

### dx...@google.com (2025-05-22)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6579525>

Fix paint-holding wait in two browser tests in renderer\_host/input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    Fifteen tests here fail on linux-chromeos-rel, perhaps occasionally 
    only. 
     
    Bug: 40057499, 418929575 
    Change-Id: If0552b4eb1b20d01d4e8e31a309b5ac59c84f236 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6579525 
    Commit-Queue: Jonathan Ross <jonross@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Jonathan Ross <jonross@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1464284}

```

---

Files:

- M `content/browser/renderer_host/input/touch_selection_controller_client_aura_browsertest.cc`
- M `content/browser/renderer_host/input/wheel_event_listener_browsertest.cc`

---

Hash: 6e9386639bb0ed92d20d007a432d11e8d6c1aaee  

Date:  Thu May 22 19:00:28 2025


---

### dx...@google.com (2025-05-23)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6578966>

Fix paint-holding wait in two RenderWidgetHostViewAura browser tests

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    The two tests here fail on linux-chromeos-rel, perhaps occasionally 
    only. 
     
    Bug: 40057499, 418929575 
    Change-Id: Ia615bdf21be60eb76c021eac8f9473767e7f4ff9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6578966 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1464474}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_aura_browsertest.cc`

---

Hash: 0d8a6b3cff50a01b76425af9a393ef3dc8a04933  

Date:  Fri May 23 00:45:11 2025


---

### dx...@google.com (2025-05-23)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6580315>

AutofillTest: fix paint-holding wait before sending input.

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    The tests here fail on linux-chromeos-rel, perhaps occasionally only. 
     
    (The CL also includes a small cleanup to unify two similar helper 
    functions.) 
     
    Bug: 40057499, 418929575 
    Change-Id: I5390fb7daf57c3a8a4d4c7cb9eee8ca0f9bd8e29 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6580315 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Stephen McGruer <smcgruer@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1464770}

```

---

Files:

- M `chrome/browser/autofill/autofill_browsertest.cc`

---

Hash: 9889c7663c555e628629d86d115d49e15574a90b  

Date:  Fri May 23 15:32:26 2025


---

### dx...@google.com (2025-05-23)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6579959>

Reland "Field trial config for DropInputEventsWhilePaintHolding"

---


Expand for full commit details
```
     
    This is the second reland attempt of commit 
    c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04 
     
    ***** 
    PLEASE DO NOT REVERT IF A FEW BROWSER TESTS FAIL. 
     
    We encountered and fixed tests that fails only occasionally, and we 
    will fix any remaining ones quickly: just assign the bug to me. 
    ***** 
     
    Original change's description: 
    > Field trial config for DropInputEventsWhilePaintHolding 
    > 
    > Bug: 40057499 
    > Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1460996} 
     
    Bug: 40057499 
    Change-Id: If46b558fa46318adcbf25559564a4064bfd8f23a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6579959 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1464786}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: 8dd449c392d22ca1ffb594a80f27b4ab4a55e089  

Date:  Fri May 23 15:58:23 2025


---

### dx...@google.com (2025-05-23)

Project: chromium/src  

Branch: main  

Author: Kartar Singh [kartarsingh@google.com](mailto:kartarsingh@google.com)  

Link:      <https://chromium-review.googlesource.com/6578425>

Revert "Reland "Field trial config for DropInputEventsWhilePaintHolding""

---


Expand for full commit details
```
     
    This reverts commit 8dd449c392d22ca1ffb594a80f27b4ab4a55e089. 
     
    Reason for revert: This breaks with InputVizard enabled which is default enabled for some time in testing config on Android. 
     
    Bug: 40057499 
    Original change's description: 
    > Reland "Field trial config for DropInputEventsWhilePaintHolding" 
    > 
    > This is the second reland attempt of commit 
    > c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04 
    > 
    > ***** 
    > PLEASE DO NOT REVERT IF A FEW BROWSER TESTS FAIL. 
    > 
    > We encountered and fixed tests that fails only occasionally, and we 
    > will fix any remaining ones quickly: just assign the bug to me. 
    > ***** 
    > 
    > Original change's description: 
    > > Field trial config for DropInputEventsWhilePaintHolding 
    > > 
    > > Bug: 40057499 
    > > Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    > > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1460996} 
    > 
    > Bug: 40057499 
    > Change-Id: If46b558fa46318adcbf25559564a4064bfd8f23a 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6579959 
    > Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1464786} 
     
    Bug: 40057499 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I4cb888d1c23f90bfb4af552e91405e97ab69f992 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6578425 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Kartar Singh <kartarsingh@google.com> 
    Reviewed-by: Henrique Nakashima <hnakashima@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1464888}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: f4a0ed026557fccdfc586bee44d77615274ef5e6  

Date:  Fri May 23 18:40:20 2025


---

### jo...@chromium.org (2025-05-23)

I think the security fix `if (!IsActive() && base::FeatureList::IsEnabled( blink::features::kDropInputEventsWhilePaintHolding))` is also needed where we try to transfer to Viz

<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_android.cc;drc=acd9caa1a2a249d1073aacb9f5b6bfbd812ef46b;l=1544>

### mu...@chromium.org (2025-05-23)

Thanks [jonross@chromium.org](mailto:jonross@chromium.org) for the suggestion.

Wondering how to confirm this change works for InputViz. I will try re-enabling [this disabled test](https://chromium-review.googlesource.com/c/chromium/src/+/6533981) but not sure if that's good enough. FYI [kartarsingh@google.com](mailto:kartarsingh@google.com)

### pe...@google.com (2025-05-27)

The NextAction date has arrived: 2025-05-27
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### dx...@google.com (2025-05-27)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6588699>

Add chrome://flags/#drop-input-events-while-paint-holding

---


Expand for full commit details
```
     
    This allows regression investigation with the feature 
    kDropInputEventsWhilePaintHolding. 
     
    Bug: 40057499, 420413451 
    Change-Id: Ie20e084c5dff9931571b7d75ba5d238208141740 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6588699 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1465957}

```

---

Files:

- M `chrome/browser/about_flags.cc`
- M `chrome/browser/flag-metadata.json`
- M `chrome/browser/flag_descriptions.cc`
- M `chrome/browser/flag_descriptions.h`
- M `tools/metrics/histograms/enums.xml`

---

Hash: 2b1978b0b5066dabc9adf8d1287245dd3196ce41  

Date:  Tue May 27 15:57:59 2025


---

### dx...@google.com (2025-05-27)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6593092>

ContentTextSelectionTest: fix paint-holding wait before sending input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    The tests here occasionally fail on android-13-x64-rel. 
     
    Bug: 40057499, 419858650 
    Change-Id: I449f53fd3b1a7901b79fae02883cf82f499399fa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6593092 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Yaron Friedman <yfriedman@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466043}

```

---

Files:

- M `content/public/android/javatests/src/org/chromium/content/browser/ContentTextSelectionTest.java`

---

Hash: 3f8038fa846a5c400aacd4f3a2deec96c6de9b08  

Date:  Tue May 27 18:02:52 2025


---

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6588348>

Make InputViz work with paint-holding input-suppression

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    InputViz maintains its own copy of `InputRouter` which starts in an 
    inactive state like a renderer `InputRouter`.  However, unlike the 
    latter, Viz's copy of the `InputRouter` never receives the 
    end-of-paint-holding signal that could switch it to an active state. 
     
    This CL makes the input router in Viz always active, and uses the 
    active/inactive state of the renderer input router to decide if input 
    would be transferred to Viz or not. 
     
    Bug: 40057499 
    Fixed: 420413451 
    Change-Id: I3c9a15c308f87326614f277b8bcc1304105030a8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6588348 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Theresa Sullivan <twellington@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466442}

```

---

Files:

- M `chrome/android/javatests/src/org/chromium/chrome/browser/input/InputOnVizTest.java`
- A `chrome/android/javatests/src/org/chromium/chrome/browser/input/OWNERS`
- M `components/viz/service/input/input_manager.cc`
- M `content/browser/renderer_host/render_widget_host_view_android.cc`

---

Hash: 8971191aa3e344599ac24b67d627846102cbdc45  

Date:  Wed May 28 13:57:17 2025


---

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6596375>

Android content.browser.input tests: fix paint-holding before input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. The tests here are known to be affected occasionally on 
    android-13-x64-rel. 
     
    Bug: 40057499, 419858650 
    Change-Id: I136bc41907236ff1f0325a808dbcf6f264ae7712 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6596375 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466524}

```

---

Files:

- M `content/public/android/javatests/src/org/chromium/content/browser/input/ImeActivityTestRule.java`
- M `content/public/android/javatests/src/org/chromium/content/browser/input/SelectPopupTest.java`

---

Hash: c4b57153922bf52e0278749cc557ae3df8f98afa  

Date:  Wed May 28 16:16:15 2025


---

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6597715>

BrowserSideFlingBrowserTest: paint-holding wait before sending input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. The tests here are known to be affected occasionally on 
    android-13-x64-rel 
     
    Bug: 40057499, 419858650 
    Change-Id: I21abb0eb7437ea81d3d3f59b2f972f70cf255ac1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6597715 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Commit-Queue: Robert Flack <flackr@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466526}

```

---

Files:

- M `content/browser/renderer_host/input/fling_browsertest.cc`

---

Hash: d425902307134fa18465d9c717cad4245fae1db1  

Date:  Wed May 28 16:18:22 2025


---

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6597361>

Fix paint-holding wait before input in a few content/browser/ tests

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. The tests here are known to be affected occasionally on 
    android-13-x64-rel. 
     
    Bug: 40057499, 419858650 
    Change-Id: Ifb5409bc27772648bfa65a5709bd247297cf2418 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6597361 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Commit-Queue: Avi Drissman <avi@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466556}

```

---

Files:

- M `content/browser/attribution_reporting/attribution_src_browsertest.cc`
- M `content/browser/site_per_process_browsertest.cc`

---

Hash: ba573cfc83c45c57a7d3be02d1c53b6d1ecb7e80  

Date:  Wed May 28 17:06:18 2025


---

### dx...@google.com (2025-05-28)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6598398>

Reland "Field trial config for DropInputEventsWhilePaintHolding"

---


Expand for full commit details
```
     
    This is the third reland attempt of commit c32e50dbaff1ddaa8ee07887ef832f1d5f27ce04 
     
    ***** 
    PLEASE DO NOT REVERT IF A FEW BROWSER TESTS FAIL. 
     
    We encountered and fixed tests that fails only occasionally, and we 
    will fix any remaining ones quickly: just assign the bug to me. 
    ***** 
     
    Original change's description: 
    > Field trial config for DropInputEventsWhilePaintHolding 
    > 
    > Bug: 40057499 
    > Change-Id: Ibda4f77bbf65592ecedf7a836a6b66b6b37be0a0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6479262 
    > Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    > Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1460996} 
     
    Bug: 40057499 
    Change-Id: Ic0e9e5929e2051d20eaab8f45a23b73722c052fb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6598398 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466690}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: 32a60cf3e6cc0f41b4a8173e20dea34d3aab7446  

Date:  Wed May 28 20:31:36 2025


---

### dx...@google.com (2025-05-29)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6601894>

AutoscrollBrowserTest: Fix paint-holding wait before input dispatch

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    Bug: 40057499 
    Change-Id: I51302189d26630aa1d9aca4fd1200e212ca220da 
    Fixed: 418889669 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6601894 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Commit-Queue: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1466989}

```

---

Files:

- M `content/browser/renderer_host/input/autoscroll_browsertest.cc`

---

Hash: 8cb71b458f73a26f73a691b731a599b3e7c959b7  

Date:  Thu May 29 14:45:51 2025


---

### dx...@google.com (2025-05-29)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6601634>

SitePerProcessHitTestBrowserTest: Fix paint-holding wait before input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    Out of 66 `NavigateToURL()` calls in 
    `site_per_process_hit_test_browsertest.cc`, only the three changed here 
    don't call `WaitForHitTestData()`. 
     
    Fixed: 418320100 
    Bug: 40057499 
    Change-Id: I32c574200724ebf36a0da60beee5cde5f21166e7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6601634 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1467072}

```

---

Files:

- M `content/browser/site_per_process_hit_test_browsertest.cc`

---

Hash: f429c34972c45982c550564937dbcc2d1624eee0  

Date:  Thu May 29 17:45:22 2025


---

### dx...@google.com (2025-05-30)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6604618>

WebContentsObserverBrowserTest: Fix paint-holding wait before input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events.  This CL fixes the only WebContentsObserverBrowserTest 
    that relies on input event. 
     
    Fixed: 418853897 
    Bug: 40057499 
    Change-Id: Iff23be904eeb0caacc229ed22d03c81d5fb63203 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6604618 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1467503}

```

---

Files:

- M `content/browser/web_contents/web_contents_observer_browsertest.cc`

---

Hash: 039972e76386288e14605dacf35aa32200ebdae4  

Date:  Fri May 30 16:01:10 2025


---

### dx...@google.com (2025-05-30)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6604911>

WebAppLinkCapturingBrowserTest: Fix paint-holding wait before input

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    This CL is part of our fixing tests that would be affected by the input 
    suppression because they don't wait for paint-holding before sending 
    input events. 
     
    Fixed: 418950142 
    Bug: 40057499 
    Change-Id: I322aaa80145ab9814c4d4e0d00f0328dc8c4b5a7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6604911 
    Auto-Submit: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1467640}

```

---

Files:

- M `chrome/browser/ui/web_applications/web_app_link_capturing_browsertest.cc`

---

Hash: b0f37ed5a4d0432271921deb9005abac8dc6b6fa  

Date:  Fri May 30 20:14:04 2025


---

### mu...@chromium.org (2025-06-09)

We have 50% Canary/Dev trial running since May30, and we saw no regressions so far.

We saw one "accidental" regression with InputViz which was caused by an omission of the PR in [Comment #258](https://issues.chromium.org/issues/40057499#comment258) our original finch config. The problem was fixed through cl/766175528.

### mu...@chromium.org (2025-07-09)

More than 2 weeks have passed since we started 50% Beta trial on June24.

- We have got [Issue 428702162](https://issues.chromium.org/issues/428702162) which is a test flakiness problem.
- We saw no regressions in the wild so far.

### dx...@google.com (2025-07-09)

Project: chromium/src  

Branch: main  

Author: Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:      <https://chromium-review.googlesource.com/6705813>

End paint-holding before input to deflake UrlOverridingTest's.

---


Expand for full commit details
```
     
    To mitigate a bug with user interactions with a stale page, we are 
    planning to hold back input events from a page while paint-holding is 
    active. Paint-holding is the browser feature to continue to show a 
    snapshot of the pre-navigation page (instead of a blank page) until the 
    renderer for the post-navigation page has pushed content to the GPU. 
     
    The tests modified here send user input to the pages without waiting 
    for renderer content. Because the tests are agnostic to paint-holding, 
    we are ending paint-holding early to keep the tests working. 
     
    Fixed: 428702162 
    Bug: 40057499 
    Change-Id: I9f17d0e65ec3841e345b7202a5e290f1ca2dabfa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6705813 
    Reviewed-by: Michael Thiessen <mthiesse@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1484538}

```

---

Files:

- M `chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java`
- M `chrome/test/android/javatests/src/org/chromium/chrome/test/util/ChromeTabUtils.java`

---

Hash: 54073609b2143511187df88ba0dd0dc7a9ec16d5  

Date:  Wed Jul 9 19:49:32 2025


---

### mu...@chromium.org (2025-09-03)

We started 10% stable experiment on Jul21, which got reverted on Aug19.

### mu...@chromium.org (2025-10-01)

Here is a doc explaining what we observed when a website stops responding after swipes during a navigation (with the flag enabled).
<https://docs.google.com/document/d/1ggelxoNlenXjRlEs7novnMQAzNqYmzW3dh5vCUQOLjg/edit?usp=sharing>

### mu...@chromium.org (2025-10-16)

Thanks to the suggestion from [amanvr@google.com](mailto:amanvr@google.com), we now have a solution to the non-responsiveness after swipes during a navigation (with the flag enabled).

### dx...@google.com (2025-10-20)

Project: chromium/src  

Branch:  main  

Author:  Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:    <https://chromium-review.googlesource.com/7049338>

Unify the code to drop input events with FilterAndSendWebInputEvent

---


Expand for full commit details
```
     
    We originally had the input droppping code at the event dispatch code 
    for each event type. This CL moves that code to the method 
    `InputRouterImpl::FilterAndSendWebInputEvent` to unify the new calls to 
    the callbacks with the existing calls there. 
     
    The original implementation had issues with ack processing for touch 
    input. More precisely, it missed notifying `WidgetInputHandler` through 
    `DispatchEventCallback` for these events. Not sure why this affected 
    only swipes during a navigation. 
     
    We confirmed through manual testing that this CL resolves the 
    non-responsiveness problem after swipes during a navigation (with the 
    flag enabled). 
     
    Bug: 40057499 
    Change-Id: Id432b108a294be8789f1c4aca395de13724cb8ea 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7049338 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Aman Verma <amanvr@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1532268}

```

---

Files:

- M `components/input/input_router_impl.cc`
- M `components/input/render_input_router.cc`
- M `content/browser/renderer_host/input/mock_input_router_client.cc`
- M `content/browser/renderer_host/input/mock_input_router_client.h`

---

Hash: [1fda96c72f3c8cc2ac62f5f5f62ace4e3a2325ef](https://chromiumdash.appspot.com/commit/1fda96c72f3c8cc2ac62f5f5f62ace4e3a2325ef)  

Date: Mon Oct 20 14:44:46 2025


---

### dx...@google.com (2025-10-21)

Project: chromium/src  

Branch:  main  

Author:  Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:    <https://chromium-review.googlesource.com/7064132>

Extend the expiry of Renderer.ContentProduction.\* by a few months

---


Expand for full commit details
```
     
    We are hoping to ship kDropInputEventsBeforeFirstPaint soon but 
    leaving the histograms around for a while still makes sense in case 
    the feature causes any regression. 
     
    Fixed: 446669956 
    Bug: 40057499 
    Change-Id: I2320cf2827a17de89272061c74b568aeeaf0eeb4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7064132 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Chris Harrelson <chrishtr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1533179}

```

---

Files:

- M `tools/metrics/histograms/metadata/renderer/histograms.xml`

---

Hash: [01c2f67c7438e819f802e17928986df1d94d3564](https://chromiumdash.appspot.com/commit/01c2f67c7438e819f802e17928986df1d94d3564)  

Date: Tue Oct 21 20:01:16 2025


---

### mu...@chromium.org (2025-10-22)

Today we resumed the finch trial with min\_version 143.0.7485.0 where the fix above landed. We will ramp it up to include Beta 50% next week right before the first Beta release for M143.

### pe...@google.com (2025-10-27)

The NextAction date has arrived: 2025-10-27
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### mu...@chromium.org (2025-10-28)

The finch config for 50% Beta trial landed yesterday.

### mu...@chromium.org (2025-12-10)

The finch trial was promoted to 1% Stable before the start of M143 release, then to 10% Stable since Dec 4.

### aw...@google.com (2026-01-05)

Would you be able to give an update on the state of the rollout, and when we expect this to be launched to 100% stable?

### mu...@chromium.org (2026-01-06)

We are expecting to promote it to 100% Stable in a week.

### dx...@google.com (2026-01-07)

Project: chromium/src  

Branch:  main  

Author:  Mustaq Ahmed [mustaq@google.com](mailto:mustaq@google.com)  

Link:    <https://chromium-review.googlesource.com/4803165>

Enable suppressing input event dispatch while paint-holding.

---


Expand for full commit details
```
     
    This CL enables DropInputEventsWhilePaintHolding to prevent a 
    yet-to-be-painted page respond to input events. 
     
    Bug: 40057499 
    Change-Id: I658bcd7407701b824afa250810d4c521ae3357f9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4803165 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Commit-Queue: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1565636}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`
- M `third_party/blink/common/features.cc`

---

Hash: [e59c879671847925d53aa3413a6d3b1969d73743](https://chromiumdash.appspot.com/commit/e59c879671847925d53aa3413a6d3b1969d73743)  

Date: Wed Jan 7 15:20:56 2026


---

### aw...@google.com (2026-01-12)

Thanks. Are we OK to close this out? I take that users are protected via the finch config while we wait for the commit to make it to stable?

### mu...@chromium.org (2026-01-13)

Our finch config to enable the mitigation on 100% Stable landed on Jan 9: cl/854270010

Because this bug is very hard to repro and then we have already landed a mitigation, I am closing this as fixed. I filed [Issue 475587459](https://issues.chromium.org/issues/475587459) to cover the remaining problem with address bar updates.

### wf...@chromium.org (2026-01-21)

This is a serious bug (thank you for fixing it) however requires too many unreasonable actions for a reasonable and prudent user, so this should be severity medium (not high).

### su...@gmail.com (2026-01-22)

> Because this bug is very hard to repro and then we have already landed a mitigation, I am closing this as fixed.

Thank you @mustaq,

I found that by lowering the "Periodically re-scale ..." interval code from `2300` to `10` in spoof-locationhref-fps.html or spoof3.html, I was able to reproduce this more consistently, including on Samsung S23+, Samsung S25+, and Android Emulator Pixel\_9 (Intel Core Ultra 9 285k) on Arch Linux, as shown in the attached video (recorded on Drop input events to Disabled).

### su...@gmail.com (2026-01-22)

> I was able to reproduce this more consistently, including on Samsung S23+, Samsung S25+, and Android Emulator Pixel\_9 (Intel Core Ultra 9 285k) on Arch Linux, as shown in the attached video (recorded on Drop input events to Disabled).

Attached the testcase + screen recording for the touch-passthrough test on <https://touchscreentest.com>

### su...@gmail.com (2026-01-26)

> This is a serious bug (thank you for fixing it) however requires too many unreasonable actions for a reasonable and prudent user, so this should be severity medium (not high).

Thanks @wf.. for the feedback,

For one-tap [clickjacking](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Clickjacking) scenario, I was able to demonstrate it able to overlay the page, e.g. in real attack scenario, putting "I'm not a robot" or "tap here" button right on top of the "Allow", "Authorize" or "Continue as user" button. When the user one tap it, the tap goes through to the real button underneath, so they end up granting the app access without realizing it. As shown in the attached video below.

### su...@gmail.com (2026-01-26)

> For one-tap [clickjacking](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Clickjacking) scenario

I’ve attached examples of OAuth authorization apps screens from GitHub and GitLab. These are good illustrations of high-value targets for one-tap clickjacking, since a single tap can grant broad access permissions.

### sp...@google.com (2026-01-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline / Lower Impact security UI spoofing, mitigated by complex timing prerequisites


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057499)*
