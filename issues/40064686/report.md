# Security: Chrome for Android Slowdown with JS then Navigate able to Hide Omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [40064686](https://issues.chromium.org/issues/40064686) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation>BFCache |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2023-05-19 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When running location.reload() in loop then slowing down Chrome with slowdown code, in the testcase I'm using calculatePrimes for the slowdown code and queueMicroTask to set src on image element, then when navigate away with e.g. window.history.go(-2) it able to hide Chrome omnibox

The testcase1 is very reliable on Chrome Beta 114.0.5735.33, I able to reproduce on multiple device including on Android 11 Mi 9T, Android 12 Redmi Note 9 Pro, and Android Emulator Pixel\_3\_API\_33.

I also able to reproduce this on Chrome 113.0.5672.131 and Chrome Dev 115.0.5776.0 but using different testcase, the timing on both version is different than on Chrome Beta, I'll share the testcase later after I able figure out the slowdown timing to reliably hide the omnibox as on Chrome Beta.

**VERSION**

- Chrome 113.0.5672.131
- Chrome Beta 114.0.5735.33
- Chrome Dev 115.0.5776.0

**REPRODUCTION CASE**

1. Open Chrome Beta
2. Visit <https://sourc7.duckdns.org/googlevrp-fullnavigatorgist1/spoofpage.html>
3. Tap "Tap Here" link
4. Tap "testcase1" link
5. Page will navigate back and hide the omnibox

If still doesn't work try below steps (Copy link address method):

1. Open Chrome Beta
2. Visit <https://sourc7.duckdns.org/googlevrp-fullnavigatorgist1/spoofpage.html>
3. Long tap on "Tap here" link
4. On Chrome context menu, tap "Copy link address"
5. Tap the omnibox
6. Tap "Link you copied"
7. Tap "testcase1" link
8. Page will navigate back and hide the omnibox

**CREDIT INFORMATION**  

Irvan Kurniawan (sourc7)

## Attachments

- [testcase1.html](attachments/testcase1.html) (text/plain, 1.0 KB)
- [Chrome Beta 114.0.5735.33 on Mi 9T.mp4](attachments/Chrome Beta 114.0.5735.33 on Mi 9T.mp4) (video/mp4, 4.9 MB)
- [Chrome Beta 114.0.5735.33 on Redmi Note 9 Pro with Copy Link Address method.mp4](attachments/Chrome Beta 114.0.5735.33 on Redmi Note 9 Pro with Copy Link Address method.mp4) (video/mp4, 7.6 MB)
- [testcase1.zip](attachments/testcase1.zip) (application/octet-stream, 15.2 KB)
- [Screenrecorder-2023-05-24-03-46-08-831.mp4](attachments/Screenrecorder-2023-05-24-03-46-08-831.mp4) (video/mp4, 2.6 MB)

## Timeline

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-05-19)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-22)

Hi jdonnelly@, I am assigning this to you as for an Omnibox related bug. I'm unsure what the severity might be, so I am leaving that field unset. Please help in assigning and reviewing the priority for this bug. Thank you!

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-05-23)

reporter, please attach content of your page to the bug, as we are unable to visit external sites from security bugs.

I am not able to fully understand the implications of this bug - the videos you show are showing the correct google.com url, it seems.

### su...@gmail.com (2023-05-23)

> reporter, please attach content of your page to the bug, as we are unable to visit external sites from security bugs.

Ok I will try attach the page into this bug

> I am not able to fully understand the implications of this bug - the videos you show are showing the correct google.com url, it seems.

I'm trying to demonstrate hide omnibox like https://crbug.com/chromium/1270593 and https://crbug.com/chromium/1300253, I just changing the iframe url from abc.xyz to blog.google/technology/research. The omnibox shows google.com, the reality it is showing blog.google/technology/research. I can change the iframe url to another domain.


### su...@gmail.com (2023-05-23)

> reporter, please attach content of your page to the bug, as we are unable to visit external sites from security bugs.

Here I attach testcase1.zip, I have successfully tested this also working on my local server:
1. On your PC unzip the testcase1.zip
2. On the testcase1 folder
3. Open Terminal then run "python -m http.server 8000"
4. Launch new terminal then run "python -m http.server 8001"
5. On Android Phone
6. Open Chrome Beta
7. Visit yourserverip:8000
8. Tap "Tap here" link
9. Tap "testcase1" link
10. Page will navigate back and hide the omnibox (omnibox replaced with omnibox spoof image on google.com)

If the omnibox is still not hidden, then try again or try copy link address method:
1. Open Chrome Beta
2. Visit yourserverip:8000
3. Long tap on "Tap here" link
4. On Chrome context menu, tap "Copy link address"
5. Tap the omnibox
6. Tap "Link you copied"
7. Tap "testcase1" link
8. Page will navigate back and hide the omnibox (omnibox replaced with omnibox spoof image on google.com)


### su...@gmail.com (2023-05-23)

Attached video show that I able to reproduce the testcase1.zip on my local server

### su...@gmail.com (2023-05-25)

@jdonnelly @wfh I have attached the testcase1.zip to reproduce locally and new demonstration video, is there any update?

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-05-31)

jinsukkim: Assigning to you since you were able to resolve https://crbug.com/1270593 and https://crbug.com/1300253, in the hopes that you have some idea of what may be the issue here.

### ca...@chromium.org (2023-06-02)

I believe this would be high severity under "Complete control over the apparent origin in the omnibox" 

### ji...@chromium.org (2023-06-02)

[Empty comment from Monorail migration]

### tw...@chromium.org (2023-06-02)

Re #12 -- is fullscreen mode involved in the repro steps somehow? Scanning through this it doesn't seem like it.

If we can repro on a local build, it'd be helpful to know what code is hiding the browser controls.

[Monorail components: -UI>Browser>Omnibox UI>Browser>Toolbar]

### ji...@chromium.org (2023-06-02)

My bad - just throught this was also about fullscreen. Will take a look.

### tw...@chromium.org (2023-06-02)

It. could be that fullscreen code is getting hit somehow, but it could be something else. 

I wonder if we might be able to dump a stack trace here to see what (if anything) is trying to hide browser controls from the Java side: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsConstraintsHelper.java;drc=b8a0323a84f483b25e94b3a24d80fda16c5dd1ae;l=180 

### [Deleted User] (2023-06-03)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-17)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2023-06-20)

Jinsuk, have you been able to repro to confirm whether this is fullscreen related or not?

### ji...@chromium.org (2023-06-28)

Will look into it today.

### an...@chromium.org (2023-06-30)

Hi Jinsuk, a quick checkin to see if there is any update on a repro. Thanks!  - secondary shepherd

### ji...@chromium.org (2023-06-30)

[Empty comment from Monorail migration]

### ji...@chromium.org (2023-06-30)

This is fortunately 100% reproducible on Pixel XL/QP1A. Investigation so far indicates this doesn't have to do with fullscreen. There is a subtle timing issue that causes the problem.

> I wonder if we might be able to dump a stack trace here to see what (if anything) is trying to hide browser controls from the Java side: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsConstraintsHelper.java;drc=b8a0323a84f483b25e94b3a24d80fda16c5dd1ae;l=180

The browser-controls-state (or visibility-constraints) never turns to "hide" - it is either "shown" or "both" all through the time.

In normal cases, navigation doesn't involve omnibox visibility change.  The JS in testcase1.html however does some tricks to get it hidden:

    function main() {
        location.reload()   // 1
        calculatePrimes(1000, 100000)  // 2
        window.queueMicrotask(spoof)
    }

    function spoof() {
        document.getElementById("image").src = null  // 3

        setInterval(function () {
            window.history.go(-2)
        }, 9)
    }

Line 1, 2, and 3 work together to make this happen.  Following stack trace at BrowserControlsManager shows the moment:

06-30 12:35:16.580  1132  1132 I crdebug : offset-changed top: -196 topmo: 0
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.Debug.printStack(Debug.java:19)
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.BrowserControlsManager.onOffsetsChanged(BrowserControlsManager.java:636)
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.BrowserControlsManager.-$$Nest$monOffsetsChanged(Unknown Source:0)
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.BrowserControlsManager$3.onBrowserControlsOffsetChanged(BrowserControlsManager.java:239)
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.tab.TabBrowserControlsOffsetHelper.notifyControlsOffsetChanged(TabBrowserControlsOffsetHelper.java:98)
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.tab.TabBrowserControlsOffsetHelper.setTopOffset(TabBrowserControlsOffsetHelper.java:74)
06-30 12:35:16.581  1132  1132 I crdebug :      at org.chromium.chrome.browser.tab.TabViewAndroidDelegate.onTopControlsChanged(TabViewAndroidDelegate.java:93)
06-30 12:35:16.581  1132  1132 I crdebug :      at android.os.MessageQueue.nativePollOnce(Native Method)
06-30 12:35:16.581  1132  1132 I crdebug :      at android.os.MessageQueue.next(MessageQueue.java:336)


If any of the lines 1/2/3 is missing, the omnibox won't get hidden - or if it does, it is immediately restored like below :

06-30 12:35:02.846  1132  1132 I crdebug : offset-changed top: 0 topmo: 0
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.Debug.printStack(Debug.java:19)
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.BrowserControlsManager.onOffsetsChanged(BrowserControlsManager.java:636)
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.BrowserControlsManager.-$$Nest$monOffsetsChanged(Unknown Source:0)
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.fullscreen.BrowserControlsManager$3.onBrowserControlsOffsetChanged(BrowserControlsManager.java:239)
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.tab.TabBrowserControlsOffsetHelper.notifyControlsOffsetChanged(TabBrowserControlsOffsetHelper.java:98)
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.tab.TabBrowserControlsOffsetHelper.setTopOffset(TabBrowserControlsOffsetHelper.java:74)
06-30 12:35:02.847  1132  1132 I crdebug :      at org.chromium.chrome.browser.tab.TabViewAndroidDelegate.onTopControlsChanged(TabViewAndroidDelegate.java:93)
06-30 12:35:02.847  1132  1132 I crdebug :      at android.os.MessageQueue.nativePollOnce(Native Method)
06-30 12:35:02.847  1132  1132 I crdebug :      at android.os.MessageQueue.next(MessageQueue.java:336)


@twellington Not sure what could possibly cause the browser controls visibility change during the navigation. If you gave me some pointers you think are worth checking, I may be able to dig further. 

### tw...@chromium.org (2023-07-05)

cc'ing Sinan who has done the most work on the team with browser controls offsets

For the 06-30 12:35:02.846  1132  1132 I crdebug : offset-changed top: 0 topmo: 0 line, I wonder if we can track down what's causing the top controls offset to become 0 in the first place -- either looking at the Java APIs or adding logging in C++, e.g. to browser_controls_offset_manager

There is this general https://crbug.com/chromium/640641 about sites being able to hide the toolbar which has a lot of issues dup'ed against it. This might be a variation of that... Jinsuk, cc'ed you on https://crbug.com/chromium/1457924 -- wondering if you could review to see if there's overlap

### dc...@chromium.org (2023-07-18)

Secondary security shepherd here; just checking in to see if there's been any update on the investigation here. The omnibox is an important security surface, and if pages are able to arbitrarily hide it and keep it hidden, that is bad. :)

### tw...@chromium.org (2023-07-18)

Jinsuk -- any updates on whether this is a new issue or whether it's captured by the previous similar bugs and should be marked as a duplicate?

cc'ing Kevin for viz

### ji...@chromium.org (2023-07-18)

This issue looks different from the others deduped to https://crbug.com/chromium/640641. I don't have access to them all but they are mostly achieving the hack by actually entering fullscreen, or doing something after having users scroll the browser controls away manually.  This one found a way to have the browser controls scrolled hidden using js & navigation only. 

From the discussion in https://crbug.com/chromium/640641, I get the impression that the severity of the issue is not assessed high, since the browser controls will be restored as soon as users are tricked into typing in something (such as their login credential) - we're not in fullscreen mode after all.

I think it's still important to understand what initiates browser controls offset change in the repro scenario. I'm having some problem in getting native traces as my debug build keeps crashing :(

Sinan, could we use your insight/intuition on what could possible 
    

### ji...@chromium.org (2023-07-18)

possibly initiate the browser control offset change?

### si...@google.com (2023-07-18)

I just talked to Jinsuk offline. For visibility, these are the first things I would check/log:

- Whether BrowserControlsOffsetManager::UpdateBrowserControlsState() [1] is called at all. It is possible that we call client_->SetCurrentBrowserControlsShownRatio(0,0) in this function and hide the controls.
- Whether SetCurrentBrowserControlsShownRatio [2] is called with 0 values.
- I also wonder if the BrowserControls on the main thread [3] is still functional. It shouldn't be since the scroll unification is enabled by default (115+), but I might be wrong.

[1] https://source.chromium.org/chromium/chromium/src/+/main:cc/input/browser_controls_offset_manager.cc;drc=d90e2ff3856c18f2b1bd73a0f69984af6f9fcf4d;l=137
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:cc/trees/layer_tree_host_impl.cc;l=3954;drc=636048a55ca7e2e35d5a15ba10d64b03dfe8c588;bpv=0;bpt=1
[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/browser_controls.cc?q=browser_controls%5C.cc%20(-file:R.java%20-file:R.txt%20case:yes)&ss=chromium

### ji...@chromium.org (2023-07-19)

Thanks Sinan for suggestions. When the problem occurs, BrowserControlsOffsetManager::UpdateBrowserControlsState() indeed is called, which calculates |final_top_shown_ratio| to be 0. So client_->SetCurrentBrowserControlsShownRatio(0,0) is passed the value and hide the controls.

But it's still not straightforward to understand what actually triggered it. The trace goes back into Blink which doesn't give me clues:

07-19 11:28:20.811 13476 13796 W chromium: [WARNING:browser_controls_offset_manager.cc(204)] crdebug update-state: 
07-19 11:28:20.811 13476 13796 W chromium: [WARNING:layer_tree_host_impl.cc(3958)] crdebug ratio: 0

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  00000000005d4e6b  base::debug::StackTrace::StackTrace(unsigned long)                                ../../base/debug/stack_trace.cc:221:12
  00000000003262d3  cc::LayerTreeHostImpl::SetCurrentBrowserControlsShownRatio(float, float)          ../../cc/trees/layer_tree_host_impl.cc:3959:3
  00000000001fb283  cc::BrowserControlsOffsetManager::UpdateBrowserControlsState(cc::BrowserControlsState, cc::BrowserControlsState, bool)  ../../cc/input/browser_controls_offset_manager.cc:208:14
  0000000001219bcf  blink::InputHandlerProxy::UpdateBrowserControlsState(cc::BrowserControlsState, cc::BrowserControlsState, bool)  ../../third_party/blink/renderer/platform/widget/input/input_handler_proxy.cc:1586:19
  000000000122c767  blink::WidgetInputHandlerManager::UpdateBrowserControlsState(cc::BrowserControlsState, cc::BrowserControlsState, bool)  ../../third_party/blink/renderer/platform/widget/input/widget_input_handler_manager.cc:1149:25
  0000000001a6c72b  blink::mojom::blink::WidgetInputHandlerStubDispatch::Accept(blink::mojom::blink::WidgetInputHandler*, mojo::Message*)  gen/third_party/blink/public/mojom/input/input_handler.mojom-blink.cc:7900:13
  000000000003d56b  mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)             ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54
  0000000000045287  mojo::MessageDispatcher::Accept(mojo::Message*)                                   ../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
  000000000003ee1f  mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)              ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20
  0000000000047e07  mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)  ../../mojo/public/cpp/bindings
/lib/multiplex_router.cc:1096:42
  000000000004796f  mojo::internal::MultiplexRouter::Accept(mojo::Message*)                           ../../mojo/public/cpp/bindings/lib/multiplex_router.cc:710:7
  0000000000045287  mojo::MessageDispatcher::Accept(mojo::Message*)                                   ../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
  000000000003482b  mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)     ../../mojo/public/cpp/bindings/lib/connector.cc:561:49
  0000000000035243  mojo::Connector::ReadAllAvailableMessages()                                       ../../mojo/public/cpp/bindings/lib/connector.cc:618:14
  000000000003506b  mojo::Connector::OnHandleReadyInternal(unsigned int)                              ../../mojo/public/cpp/bindings/lib/connector.cc:451:3
  000000000003500b  mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)                  ../../mojo/public/cpp/bindings/lib/connector.cc:417:3


Will add additional logs and dig around for more clues


### si...@google.com (2023-07-19)

Hmm, this looks like the process hop from browser to renderer. If you print the stack trace in RenderWidgetHostImpl::UpdateBrowserControlsState [1], you may be able to find out where this call comes from in the browser.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/render_widget_host_impl.cc;l=2674;drc=c3f32fac9e8a61bf1e1c54c1022a96af097cf687;bpv=0;bpt=1

### [Deleted User] (2023-07-19)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2023-07-19)

Thanks again Sinan for the additional pointer. I was able to figure out what triggered it -  BackFowardCacheImpl::RestoreBrowserControlsState [1] The browser controls hidden by the logic is expected to be restored later, as explained in the comment in the code, but it apparently never happens in the specific scenario.

I'm not familiar with the relevant flow, so it's not clear to me if this (i.e. |prev_top_controls_shown_ratio| == 0.f) should not have happen in the first place, or we rather need to figure out why the next browser control visibility restoration is not happening.

Assigning to carlscab@ who worked on the logic for his feedback.
 



[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/back_forward_cache_impl.cc;l=315;drc=d90e2ff3856c18f2b1bd73a0f69984af6f9fcf4d

### si...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### ca...@google.com (2023-07-19)

I will be ooo for a few days and it has been quite a long time since I looked at bfcache. altimin might be able to help finding somebody with more current knowledge.

### al...@chromium.org (2023-07-20)

Rakina, this seems like a bfcache bug. Could you take a look or route this further among TOK folks?

### ra...@chromium.org (2023-07-20)

So it looks like the  BackFowardCacheImpl::RestoreBrowserControlsState code was introduced at crrev.com/c/1949783 to fix crbug.com/1005745, which was also a bug where we didn't show the omnibox again after navigation. The fix there tries to make the current state of the browser and the renderer to be in sync by telling the bfcached renderer that it's hidden when the browser side state says the omnibox is hidden. Then when the browser's omnibox state is updated to show the omnibox, the renderer won't reject the update to show the omnibox.

It's not clear to me from the discussions, but it looks like before navigating back to the spoofed page, the omnibox state is already hidden by the code in testcase1.html, as mentioned in https://crbug.com/chromium/1447237#c24. In this case, maybe the BackFowardCacheImpl::RestoreBrowserControlsState() is just trying to make sure the bfcached renderer's state is the same as the current browser omnibox state. So maybe the problem is, after that, there's no updates on the browser side to actually show the omnibox after that? Does that sound plausible?

Let me assign this back to jinsukkim@, as I'm not familiar with how the omnibox update flow works when it's already hidden and a navigation happens, etc. If the browser side state is actually correct and we already requested to show the omnibox, I can help look into that too. (However, I can't seem to repro this bug on my device, is it possible to have a simplified repro that can be put in a browser test somehow?)

### su...@gmail.com (2023-07-24)

> I was able to figure out what triggered it -  BackFowardCacheImpl::RestoreBrowserControlsState [1] The browser controls hidden by the logic is expected to be restored later

After compiled Chromium for Android, I able to reproduce this very reliably on Samsung Galaxy S23+. 

I also confirmed after removed the cached_rfh->GetPage().UpdateBrowserControlsState(cc::BrowserControlsState::kBoth, cc::BrowserControlsState::kHidden, false); code, I'm no longer able to reproduce the hide omnibox.



### dc...@chromium.org (2023-07-24)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation>BFCache]

### ji...@chromium.org (2023-07-24)

Unassigning myself for someone with more familiarity with BFCache/Browser controls to investigate it further.

[Monorail components: -UI>Browser>Toolbar]

### su...@gmail.com (2023-07-24)

> So it looks like the BackFowardCacheImpl::RestoreBrowserControlsState code was introduced at crrev.com/c/1949783 to fix crbug.com/1005745, which was also a bug where we didn't show the omnibox again after navigation.

I've tried installed Chrome Version 79.0.3916.3, after press back button, the omnibox is still hidden (as on previous tab state). 

After the BackFowardCacheImpl::RestoreBrowserControlsState code was landed, on the Chrome 82.0.4057.2, after press back button, the omnibox is now restored/reappear. From that, it looks like the code is introduced to restore the omnibox after back/forward navigation.

However on the latest Chromium source code, after removed the BackFowardCacheImpl::RestoreBrowserControlsState code, the omnibox is still restored/reappear. It looks like another code now also trigger the show omnibox.

As the BackFowardCacheImpl::RestoreBrowserControlsState code is introduce to restore the omnibox, I think the cc::BrowserControlsState::kShown is should be used, instead of cc::BrowserControlsState::kHidden on following code:

cached_rfh->GetPage().UpdateBrowserControlsState(
        cc::BrowserControlsState::kBoth, cc::BrowserControlsState::kHidden,
        // Do not animate as we want this to happen "instantaneously"
        false);
  }  

I investigated that cc::BrowserControlsState::kHidden is causing BrowserControlsOffsetManager::UpdateBrowserControlsState to set final_top_shown_ratio = TopControlsMinShownRatio(); to 0. When the final_top_shown_ratio = 0 it trigger BrowserControlsManager.updateBrowserControlsOffsets -> BrowserControlsManager.setPositionsForTab to hide the omnibox.

When I change the cc::BrowserControlsState::kHidden to cc::BrowserControlsState::kShown, I no longer able to reproduce the hide omnibox.



### tw...@chromium.org (2023-07-24)

This is marked as a P1 security issue so it should have an assigned owner to keep the ball rolling. Routing back to rakina@ to investigate whether changes to cached_rfh->GetPage().UpdateBrowserControlsState make sense.

### su...@gmail.com (2023-07-24)

> I can help look into that too. (However, I can't seem to repro this bug on my device, is it possible to have a simplified repro that can be put in a browser test somehow?)

I'm on Chromium git commit 45a78232 (Jul 18, 2023), on that build I'm able to reproduce hide omnibox very reliably on Samsung Galaxy S23+, Redmi Note 9 Pro, and Xiaomi Mi 9T.

My args.gn for the build is very simple:
target_os = "android"
target_cpu = "arm64"


### ra...@google.com (2023-07-25)

OK, I managed to repro this on an Android emulator right now. It looks like there is a race condition here. Before the navigation back to the bfcached page, the omnibox is hidden, but there is an ongoing update from the browser to the renderer to show the omnibox again, just before the BFCache restore navigation happens. The browser-side top_controls_shown_ratio is still not updated since the renderer side hasn't sent an acknowledgement/state update message to the browser (last_render_frame_metadata_ [1] hasn't been updated, I think).

At the same time, the BFCache logic at BackFowardCacheImpl::RestoreBrowserControlsState() doesn't know about the ongoing update to show the omnibox, and thinks that since top_controls_shown_ratio is < 1 (from this code [2]), the renderer state needs to be updated to hidden to match it. Then after that nothing updates the renderer to show the omnibox again, as from the browser's perspective it already sent the message to show the omnibox before the bfcache restore, and the bfcache code is actually making the renderer side out of sync with the browser side here.

A possible solution here is to make the BFCache renderer update code check the latest state sent by the browser, instead of the latest state that is acknowledged by the renderer. Maybe we need to save a "last_sent_browser_controller_state_" or something? Or maybe there's a better solution?

(cc skym@ who seems to be the last person who touched UpdateBrowserControlsState, and jonross@ who introduced the RenderFrameMetadata stuff, in case they have opinions).


[1]: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/render_frame_metadata_provider_impl.cc;l=93;drc=a742c65cc620d2b7b262b5514540ebdb510a7121
[2]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/back_forward_cache_impl.cc;l=334;drc=839ab79fab0151ee1e570db4cd7e7500f9076f61

### sk...@chromium.org (2023-07-25)

Hey, I'm not very familiar with a lot that's happening here, so sorry for dumb questions. But trying to read all the comments so far, I'm confused.

My understanding was that on any navigation, we should show the omnibox for 3 seconds. Are there special bfcache rules that make this not the case? Trying to test this myself on the URL in https://crbug.com/chromium/1447237#c1, it seems like we send out BrowserControlsState::kBoth from TabStateBrowserControlsVisibilityDelegate.java very quickly, there's no 3 second delay.

Trying to understand why this is happening, we get a #cancelEnableFullscreenLoadDelay(), see Java stack at [1]. What is a didFailLoad, and is that what's supposed to be happening?

[1] https://paste.googleplex.com/5141519806758912

### sk...@chromium.org (2023-07-25)

C++ (browser) side of ::DidFailLoad() [1], though it's just an IPC getting wired from renderer. Looks like the error code is -3 (ABORTED).

FWIW, if I comment out the contents of #onPageLoadFailed() [2], our toolbar stays on the screen in my testing. Not that this would be a reasonable fix.

[1] https://paste.googleplex.com/4541988857708544
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java;l=122;drc=9b182c5cc3a32acac5880288d0bbddbb9fc4f516

### ra...@google.com (2023-07-26)

Thanks for investigating skym@! 

From my understanding:
1. The testcase1.html page triggers a bunch of computation, a reload, and a back navigation (which will restore a page from bfcache).
2. The bfcache restore navigation to spoofpage.html sees that the omnibox is currently hidden, and tells [1] the bfcached page in the renderer that the omnibox is currently hidden, in case the bfcached renderer state is out of sync (since it won't be updated about the omnibox state while it's bfcached). This is so that when the browser triggers omnibox to be shown again, that renderer won't reject it thinking that it's the same state (shown) as it already tracks.

What I thought happened was what I mentioned in https://crbug.com/chromium/1447237#c45, because before the BackFowardCacheImpl::RestoreBrowserControlsState() call that change the renderer state to hidden, there is actually a TabBrowserControlsConstraintsHelper::UpdateState() call from Android java code that updates the renderer state to kShown, but the BFCache code still thinks the omnibox is hidden after that. But maybe some other callers updated the omnibox and I just missed them from my logging...

Following your findings, I logged the DidFailLoad() calls and it looks like you're right, that indeed only shows up when the bug reproduces. That call came from unloading the testcase1 page while it hasn't fully loaded yet, so we notify the browser that the page load failed there. See full stack trace at [2]. It seems like when we fail the load of a page we cancel the omnibox hiding/fullscreen delay, while if we finish the load correctly we will delay [3] the omnibox hiding/fullscreen for 3 seconds like skym@ mentioned.

I don't know why this logic is that way, but if we want to keep it, I think we need to know if the failed load is happening on a document that is currently unloading/not active, and ignore that on the Android code (or even earlier). It looks like we pass IsInPrimaryMainFrame() and already filter out [4] updates coming from pages that are not the primary one (e.g. prerendered pages), but apparently it's still returning true in this case somehow. I'll file a separate bug for that.

So, question to android folks here: Why do we hide the omnibox when the page fails the load? Doesn't that open a way for malicious pages to hide the omnibox by triggering load failures somehow? Is that something that we can change, or should we go with the solution above where we filter load failure messages from unloading documents?

[1]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/back_forward_cache_impl.cc;l=334;drc=839ab79fab0151ee1e570db4cd7e7500f9076f61
[2]: https://paste.googleplex.com/5589004442402816
[3]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java;l=117;drc=9b182c5cc3a32acac5880288d0bbddbb9fc4f516
[4]: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabWebContentsObserver.java;l=212;drc=7d2d8ccab2b68fbbfc5e1611d45bd4ecf87090b8

### jo...@chromium.org (2023-07-26)

Have we considered always showing the omnibox during/after navigation. Even if the previously cached page had hidden it?

There have been load fail issues before, where we evict/clear the graphical surface of the renderer area. So we have a precedent of ignoring bfcached content

### tw...@chromium.org (2023-07-26)

> So, question to android folks here: Why do we hide the omnibox when the page fails the load?

The logic linked in TabStateBrowserControlsVisibilityDelegate isn't hiding the toolbar when page load finishes. After a page load starts, TabStateBrowserControlsVisibilityDelegate sets the toolbar to shown and prevents it from hiding while the page is loading and for 3 seconds after load finishes -- via  BrowserControlsState.SHOWN. If the load fails, we cancel that so the toolbar can be hidden through normal means (e.g. page scroll, fullscreen) -- via BrowserControlsState.BOTH. (or at least that's what's supposed be happening per my read of TabStateBrowserControlsVisibilityDelegate)


If page load doesn't fail, perhaps this 3 second lock on browser controls being visible in TabStateBrowserControlsVisibilityDelegate is preventing the bfcache update to Hidden from taking effect? And in the case of the page load failing, TabStateBrowserControlsVisibilityDelegate has set BrowserControlsState.SHOWN prior to bfcache trying to set to hidden?

### sk...@chromium.org (2023-07-26)

TabStateBrowserControlsVisibilityDelegate expects to see a #onPageLoadStarted(), and then either #onDidFinishNavigationInPrimaryMainFrame() or #onPageLoadStarted(). Like Theresa said, we cancel on #onPageLoadStarted() because we have given up seeing a #onDidFinishNavigationInPrimaryMainFrame(), and we don't want to perpetually keep the browser controls in kShown.

Another way to look at it, is our (TabStateBrowserControlsVisibilityDelegate's) expectations of the contract here is being broken. Testing on my device, I see:

#onPageLoadStarted (testcase1)
#onDidFinishNavigationInPrimaryMainFrame() (testcase1)
#onPageLoadStarted (testcase1)
#onPageLoadStarted (spoofpage.html)
#didFailPageLoad() (testcase1)
#onDidFinishNavigationInPrimaryMainFrame() (testcase1)
#onDidFinishNavigationInPrimaryMainFrame() (spoofpage.html)

The trick here is that the #onPageLoadStarted() call for spoofpage.html happens *before* the #didFailPageLoad() for testcase1. They're out of order. Since we're dealing with a single tab, I would have expected all of the testcase1 events to precede the spoofpage.html events, but that's clearly not the case.

I trace back exactly why the #didFailPageLoad() code and see when it was originally added, but gave up when I got to the clank upstream cl https://codereview.chromium.org/1141283003.

I briefly chatted with tedchoc@ about this issue yesterday, and he mentioned it didn't seem too terrible to just leave the toolbar locked when we hit #didFailPageLoad(). Failed page loads are likely infrequent, and a locked toolbar isn't the end of the world either. A better compromise here would be to just let the 3 seconds run it's course on #didFailPageLoad(). Treat it identically to #onDidFinishNavigationInPrimaryMainFrame(). We've already forced the toolbar to be shown at that point. But these options are all really just hacks, though it would simplify defending against this kind of issue.

It seems like there's actually 2 separate bugs that are both required for this to happen:
1) The issue rakina@ described where the bfcache allows the toolbar to be hidden w/o user interaction. I don't fully understand this one.
2) TabStateBrowserControlsVisibilityDelegate doesn't force kShown for 3 seconds on a real navigation.

While my initial reaction to fixing #2 is to change the Java browser code (TabStateBrowserControlsVisibilityDelegate), maybe that's not right. Hopefully others can chime in, is it actually intended that we should be seeing out of order events. If we really should be handling this, perhaps we should be tracking the URL or navigation id so that we can tell the that 
#onPageLoadStarted(spoofpage.html) -> #didFailPageLoad(testcase1) shouldn't cancel our 3 second timer.

### ra...@chromium.org (2023-07-27)

On the loading & navigations events being interleaved, yes I think those are possible. Here's what triggers the events:
- onDidStartNavigationInPrimaryMainFrame is triggered when a NavigationRequest is started, e.g. a link is clicked. The previous page is still shown at this point.
- onPageLoadStarted is triggered by didStartNavigationInPrimaryMainFrame [1], so it should have the same timing.
- onDidFinishNavigationInPrimaryMainFrame is triggered when a NavigationRequest is destructed. This can be caused by the navigation being cancelled (e.g. another navigation starts, etc), or by the navigation actually committing. The previous page is still shown on the former case, while the newly committed page would've already replaced it on the latter case.
- didFailPageLoad is called when a page load failed, which can happen when the page is still shown, or when the page gets unloaded (and a new page has been shown instead).

On why RestoreBrowserControlsState sends the kHidden update when restoring a page from BFCache:
It's more or less described in this comment from carlscab@ in the CL that introduced it: https://chromium-review.googlesource.com/c/chromium/src/+/1949783/11#message-31eddaf2698d231bf62267a2f4d727d976f619b2

When the history navigation to spoofpage restores that page from BFCache, it sees that the top_controls_shown_ratio of the previous page is 0, and makes sure that the BFCached renderer state is aligned with that, so that its renderer won't reject attempt to show the URL bar again (because it thinks there is nothing that needs to be changed, as the URL bar is already marked as shown in that renderer). It assumes that after DidFinishNavigation, something will tell the renderer to set the state to kShown again.

I have some things I'm still confused about:
- Is the top_controls_shown_ratio we see at that point is accurate? I tried logging at the places where we update the RenderFrameMetadata, but nothing seems to be updating that value to 0 before the BFCache navigation, so I'm confused why we see the value as 0 when going through the BFCache logic.
- Do we still send the kShown message after DidFinishNavigation as mentioned above? I don't see any happening after the BFCache restore navigation committed. Is that stopped by the didFailPageLoad? (I thought the didFailPageLoad only makes it so that it's *possible* to hide the omnibox, as twellington@ mentioned).
- How is the omnibox showing/hiding actually triggered, and how is it related to top_controls_shown_ratio state tracking? The TabStateBrowserControlsVisibilityDelegate seems like it's only responsible for whether it's possible to show/hide the omnibox, and don't control the actual showing/hiding themselves..


For problem #1, I don't think the BFCache logic intends to actually hide the omnibox, as its goal is to just make the renderer state in sync with the actual UI state. If it actually causes the omnibox to be hidden while previously it wasn't, then it sounds like there's something wrong with the top_controls_shown_ratio tracking (it indicates the omnibox is hidden, but it's actually shown?).

For problem #2, tracking the navigation ID sounds reasonable to me, although you can't do that with the load events. I wonder if you can just listen to the navigation events instead of the load events? (maybe not good if you want to ensure the omnibox is still shown until the page's dom is loaded and the loading bar disappear though..)


[1]: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabWebContentsObserver.java;l=241;drc=714e1e34e823b7b4bc172fa4bdefee5aaf5e5fff

### te...@chromium.org (2023-07-27)

From a historical perspective, I don't recall why some methods in TabStateBrowserControlsVisibilityDelegate use load signals vs navigation signals...but most of those signals pre-existed onDidFinishNavigationInPrimaryMainFrame and NavigationHandles, so this is likely just a mixture of "what worked at the time".

Per the comment in #51, I think having onPageLoadFailed call scheduleEnableFullscreenLoadDelayIfNecessary instead of cancelEnableFullscreenLoadDelay seems reasonable. My very, very vague rationale was that the failed case was where you were on a page and you clicked on a link that failed to load, and we wanted the omnibox to be scrollable immediately because you never left that page. If instead it was locked for 3 seconds after the failed event (assuming load fails aren't frequent) seems an OK compromise.

In general, we try to ensure the omnibox is forcibly shown on navigation. We do this by sending SHOWN as the constraints to the browser controls offset manager:
https://source.chromium.org/chromium/chromium/src/+/main:cc/input/browser_controls_offset_manager.cc;drc=d90e2ff3856c18f2b1bd73a0f69984af6f9fcf4d;l=137
Through that, the various shown ratios are calculated as part of the renderer metadata and the browser adjust layers accordingly.

Having BFCache restore the browser controls state "seems" wrong to me, but I haven't dug deeply enough to understand more.

### al...@chromium.org (2023-07-27)

Re: current BFCache behaviour: when we implemented it, we were primarily concerned about keeping the browser and the renderer state in sync (therefore choosing to persist the existing value on the browser side).

I didn't think about the requirement to show the omnibox on the navigation, so not forcing the browsing control state to be "VISIBLE" is not intentional here.

### tw...@chromium.org (2023-07-28)

>  If instead it was locked for 3 seconds after the failed event (assuming load fails aren't frequent) seems an OK compromise.

+1, this seems like a reasonable trade off to me too.

If we simply release in didFailPageLoad, I think in Sky's example we'd be releasing earlier than the intent of the current logic which iiuc is "lock once page load starts, and leave locked for 3 seconds until page load completes"

If we unlocked in didFailPageLoad without checking URLs, in Sky's example we'd do the following:

1) #onPageLoadStarted (testcase1)
2) #onDidFinishNavigationInPrimaryMainFrame() (testcase1)
3) #onPageLoadStarted (testcase1)
4) #onPageLoadStarted (spoofpage.html)
5) #didFailPageLoad() (testcase1) <-- naively could start 3 second timer
6) #onDidFinishNavigationInPrimaryMainFrame() (testcase1)
7) #onDidFinishNavigationInPrimaryMainFrame() (spoofpage.html) <-- should actually start 3 second timer here

In this flow, at step #5 onPageLoadFailed doesn't currently get a GURL but maybe we could wire one through? 

Then we could track the URL for the last #onPageLoadStarted and ignore #5 and #7 since they don't match. Not sure if Tab#getUrl would be flipped over yet at event #5 and #6, but if is, that could be another option.

Sky or Jinsuk -- since you have a repro setup, wondering if you might be able to continue help debugging / landing on a solution?

> Re: current BFCache behaviour: ...

This seems worth digging into as well, even if we mitigate this specific security report by updates to TabStateBrowserControlsVisibilityDelegate

### tw...@chromium.org (2023-07-28)

One idea on for things to investigate on the bfcache logic:

Right now //content/browser/renderer_host/back_forward_cache_impl.cc uses check prev_top_controls_shown_ratio < 1 to determine whether to request to hide.

What's the actual value of prev_top_controls_shown_ratio when we hit this issue? Is //cc/input/browser_controls_offset_manager.cc is already aware a show has been requested?

### ra...@chromium.org (2023-08-01)

Per https://crbug.com/chromium/1447237#c53 and https://crbug.com/chromium/1447237#c55, it looks like the next step to fix this bug is on the Android side, so assigning to skym@ for that.

I'll also look at the BFCache side of things more soon. I think I'm still confused on like where the true state of the omnibox is tracked. Is it purely in the renderer? How does the top_controls_shown_ratio and  BrowserControlsState interact with each other? Are those the only states controling the omnibox?
To answer https://crbug.com/chromium/1447237#c56, I think what we see on the browser side when doing the BFCache restore navigation is prev_top_controls_shown_ratio == 0. I don't know if the renderer still thinks that's the case, and how that relates to the BrowserControlsState. Maybe what BFCache should do is to update the top_controls_shown_ratio  directly without changing the constraints, but I don't know if that's possible.

### tw...@chromium.org (2023-08-01)

>  I think I'm still confused on like where the ...

There's a readme that explains the browser controls here:
https://source.chromium.org/chromium/chromium/src/+/main:docs/ui/android/browser_controls.md

### su...@gmail.com (2023-08-03)

> However on the latest Chromium source code, after removed the BackFowardCacheImpl::RestoreBrowserControlsState code, the omnibox is still restored/reappear. It looks like another code now also trigger the show omnibox.

Ok, after checking out some code, I found another code that fix crbug.com/1005745 (without BackFowardCacheImpl::RestoreBrowserControlsState code) is crrev.com/c/4252197, it do add controls_initialized_ = false; on RenderWidgetHostViewAndroid::HideInternal, so when press back on bfcache page, it will restore back/reshow the omnibox.

### sk...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### sk...@google.com (2023-08-07)

[Empty comment from Monorail migration]

### ra...@chromium.org (2023-08-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/10198af7f2c0c7a1566635ee67253c594273c380

commit 10198af7f2c0c7a1566635ee67253c594273c380
Author: Sky Malice <skym@chromium.org>
Date: Tue Aug 08 17:40:06 2023

Wait 3 seconds instead of releasing browser controls on failed load.

Bug: 1447237
Change-Id: If2a4a5374a4919a7388a5377925c1d412eed9746
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4757919
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Sky Malice <skym@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1181022}

[add] https://crrev.com/10198af7f2c0c7a1566635ee67253c594273c380/chrome/android/junit/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegateTest.java
[modify] https://crrev.com/10198af7f2c0c7a1566635ee67253c594273c380/chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java
[modify] https://crrev.com/10198af7f2c0c7a1566635ee67253c594273c380/chrome/android/chrome_junit_test_java_sources.gni


### sk...@google.com (2023-08-10)

The TabStateBrowserControlsVisibilityDelegate change is done and in M-117. Re-assigning to rakina@ for the BFCache side of things.

https://chromiumdash.appspot.com/commit/10198af7f2c0c7a1566635ee67253c594273c380

### ra...@chromium.org (2023-08-14)

Thanks for the fix! Does that mean the repro no longer works after that CL? Or do we still need changes on the BFCache side of things?
If it is the former, I think we should mark this bug as fixed first (so that we can merge back etc if needed) and file a separate bug to make the BFCache logic make more sense. If it is the latter, let me temporarily assign this to fergal@ to prioritize since I am out sick at the moment and will probably still be out for the next week.

### [Deleted User] (2023-08-14)

fergal: Uh oh! This issue still open and hasn't been updated in the last 86 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-08-30)

> Thanks for the fix! Does that mean the repro no longer works after that CL?

I've tested this on Samsung Galaxy S23+ Android 13 and Xiaomi Mi 9T Android 11, I confirm the commit on https://crbug.com/chromium/1447237#c63 has been fixed the issue.

rakina@ fergal@ as the issue has been resolved, can we marked this as Fixed? Thanks!

### ra...@chromium.org (2023-08-31)

Thanks, let me mark this as fixed (and change the owner to skym@ who made the fix). The BFCache logic improvement can be done separately.

### sk...@google.com (2023-08-31)

Is there a separate bug tracking the #1 problem of https://crbug.com/chromium/1447237#c52 that we can link in this bug for posterity?

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

Requesting merge to stable M116 because latest trunk commit (1181022) appears to be after stable branch point (1160321).

Not requesting merge to beta (M117) because latest trunk commit (1181022) appears to be prior to beta branch point (1181205). If this is incorrect, please replace the Merge-NA-117 label with Merge-Request-117. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-08-31)

Thank you everyone for the amazing team effort on this bug!!
@rakina, please update this bug with the BFCache improvements when you get a chance

Removing merge review label for 117 as the fix landed on M117

@skym, this is of a short notice, but:
Merge approved for M116! please merge the fix to branch 5845 by today Thursday Aug 31 EOD (MTV time) to get this fix into the M116 respin! 


### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1646af4880f4060ae8ccf818900cb168b68d6068

commit 1646af4880f4060ae8ccf818900cb168b68d6068
Author: Sky Malice <skym@chromium.org>
Date: Thu Aug 31 21:24:17 2023

Wait 3 seconds instead of releasing browser controls on failed load.

(cherry picked from commit 10198af7f2c0c7a1566635ee67253c594273c380)

Bug: 1447237
Change-Id: If2a4a5374a4919a7388a5377925c1d412eed9746
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4757919
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Sky Malice <skym@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1181022}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4833841
Cr-Commit-Position: refs/branch-heads/5845@{#1701}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[add] https://crrev.com/1646af4880f4060ae8ccf818900cb168b68d6068/chrome/android/junit/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegateTest.java
[modify] https://crrev.com/1646af4880f4060ae8ccf818900cb168b68d6068/chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java
[modify] https://crrev.com/1646af4880f4060ae8ccf818900cb168b68d6068/chrome/android/chrome_junit_test_java_sources.gni


### pg...@google.com (2023-09-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### ra...@chromium.org (2023-09-08)

(re https://crbug.com/chromium/1447237#c70, sorry, just managed to file the follow-up bug on the BFCache logic today at crbug.com/1480455 !)

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations, Irvan! The Chrome VRP Panel has decided to award you $7,500 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1447237?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064686)*
