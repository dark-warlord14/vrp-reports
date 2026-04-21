# Security: WebView and Chromium based browser Omnibar Spoofing with Race Condition

| Field | Value |
|-------|-------|
| **Issue ID** | [40053991](https://issues.chromium.org/issues/40053991) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, Internals>Compositing, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2020-11-25 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to spoof address bar with secure padlock. It involve race condition in navigation, if "<https://www.google.com/csi>" (w/ header 204 No Content) loaded first, the address bar will show the spoofed address with attacker controlled content.

I think it's similar to <https://crbug.com/chromium/672847> and <https://crbug.com/chromium/497588> which involve race condition and unresponsive renderer. I think the PoC html can be improved further to increase the win probability.

Currently I can't reproduce this on official Google Chrome and official chromium browser, because it won't stop the navigation even it won the race.

From my current testing, it is affect browser based on Android WebView and Chromium:

- Microsoft Edge (Android)
- Samsung Internet Beta (Android)
- NAVER Whale (Windows, Android, Linux)
- Firefox Lite (Android)
- Via Browser (Android)  
  
  and more...

**VERSION**  

Android System WebView Version: 86.0.4240.198 (Updated on Nov 11, 2020)

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- [spoof.1.html](attachments/spoof.1.html) (text/plain, 718 B)
- [microsoft-edge-demonstration.mp4](attachments/microsoft-edge-demonstration.mp4) (video/mp4, 358.8 KB)
- [firefox-lite-tried-to-win-race.mp4](attachments/firefox-lite-tried-to-win-race.mp4) (video/mp4, 595.0 KB)
- [firefox-lite-win-race-straight.mp4](attachments/firefox-lite-win-race-straight.mp4) (video/mp4, 149.4 KB)
- [cleared_data_thumbnail.png](attachments/cleared_data_thumbnail.png) (image/png, 60.7 KB)

## Timeline

### [Deleted User] (2020-11-25)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-11-25)

I can reproduce this on 89.0.4335.0 on Android, although it's a bit inconsistent (about half the time, Amazon.com ends up loading instead of the "spoof" text). It think it's a bit easier to repro in Incognito. Also interesting is that when changing tabs away and back to the spoofing tab, the top chrome (and the Omnibox) updates significantly faster than the web contents (so the other tab's web contents stick around for a bit, although then the spoof text is lost).

As this allows spoofing the apparent omnibox origin with content controlled by the attacker, but it does not appear to be interactable, I think this is Severity-Medium (it would be High, but lack of interactivity is a strong mitigation) and Impact-Stable. creis@ you've looked into similar bugs before -- could you take a look into this one?

Also of note: the test case hits a DCHECK in ScrollbarLayerImplBase [1], so you need to use a release build without DCHECKs enabled to repro this.

[1] https://source.chromium.org/chromium/chromium/src/+/master:cc/layers/scrollbar_layer_impl_base.cc;l=90;drc=a18be1fcec48ea572192369f55d57bbf8bee3ce9

[Monorail components: UI>Browser>Navigation]

### es...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-12-01)

https://crbug.com/chromium/1153204 contains a possibly more reliable repro.

### cr...@chromium.org (2020-12-02)

I may need to get someone else to help, since I don't have a good Android test environment for this.  I can try to offer a few pointers as I dig myself out from OOO, though.

cthomp@: Can you clarify whether you reproduced it in Chrome or another browser?  And did the spoof last longer than 4 seconds?

I'm curious why this would only affect other Chromium based browsers.  I don't think the defense for this would depend on things outside content/, and I think many of those browsers include the chrome/ layer anyway.

### su...@gmail.com (2020-12-02)

> I may need to get someone else to help, since I don't have a good Android test environment for this.

Today I tried this on WebView Browser Tester 86.0.4240.198 on Android Emulator - Nexus 5 API 30 (w/ Play Store) -> Clear Play Store data -> Update Android System WebView to 86.0.4240.198.

I able to reproduce this (most of the time) on WebView Browser Tester 86.0.4240.198, the address bar and content is spoofed, but the address bar show https://www.google.com:82 instead of https://www.amazon.com

On WebView based browser (Firefox Lite, Via Browser) the address bar show https://www.amazon.com (as on video above).

### su...@gmail.com (2020-12-02)

> I'm curious why this would only affect other Chromium based browsers.

After further testing, this is also affect Chrome on Android, I able to reproduce it using more reliable PoC on https://crbug.com/chromium/1153204. 

### cr...@chromium.org (2020-12-08)

Thanks-- the repro from https://crbug.com/chromium/1153204 does help.  I've discovered several issues, and I'm CC'ing some folks who might be familiar with them.

There's a simpler version posted at http://csreis.github.io/tests/interrupt-popup.html, without direct explanation describing what behavior it causes.  Repro steps:
0) Start Chrome without Site Isolation (e.g., on Android or on desktop with the flags mentioned below).
1) Click "Open Window."
2) Switch back to opener window and click "Add Content."
3) Click "Navigate Window" from opener window, to navigate (and commit) to example.com and interrupt loading with a 204 HTTP response.

If the popup was occluded during step 3, the stale paint will remain indefinitely.  If it was pulled out into a window of its own and was visible at the time, the stale paint goes away after 4 seconds, as we would normally expect.  (Note: I have mixed luck repro'ing this on Android, but I've seen it happen there.  It's quite consistent on desktop without Site Isolation.)

Some of the issues involved:

1) The issue occurs when Site Isolation is disabled, not just on Android.
You can repro it in a non-official desktop build with --disable-site-isolation-trials (but be careful on official builds, which get affected by enterprise policy and may force Site Isolation enabled).
I thought it might have worked even with Site Isolation if the victim and the 204 URL were same-site and shared a process, but that doesn't appear to be the case.  It appears the attacker and victim might need to share a process, though I haven't confirmed that yet.  (If so, that would be an additional mitigating factor.)

2) For some reason, the same-process case allows the 204 URL to prevent the victim page from painting even though the victim page has committed.
There's no ongoing_navigation_request in Navigator::OnBeginNavigation, so there must be something else that prevents the committed page from making further progress.  Perhaps that's something the Loading team would know about?  It would be great to let the committed page continue loading despite the 204 URL's "failure" if we can.  CC'ing japhet@ and arthursonzogni@ in case they have any ideas, but others should feel free to chime in.

3) When the victim page commits, we start the RenderWidgetHostImpl::new_content_rendering_timeout_ paint timer so that the paint will be cleared after 4 seconds if nothing paints from the new page.  However, even though we *do* get to ForceFirstFrameAfterNavigationTimeout and call ClearDisplayedGraphics, we *don't* actually clear the graphics (in the case that the victim tab was not visible).  This appears to be due to r598124 in https://crbug.com/chromium/878372 from samans@ (who has left the team).  That CL changed DelegatedFrameHostAndroid::ResetFallbackToFirstNavigationSurface() to return early here, breaking the security invariant of ClearDisplayedGraphics and causing us to leave an attacker-controlled paint visible in the tab.  We need to fix this.  jonross@: Can you help point us to someone who can help with this?

4) When the 204 URL commits with no content (prior to the paint timer issue above), we get to OnRequestFailedInternal and notify WebContentsObservers about DidFinishNavigation.  At least on desktop, this is triggering ThumbnailReadinessTracker::DidFinishNavigation and ScopedThumbnailCapture::ScopedThumbnailCapture, which calls UpdateVisibilityAndNotifyPageAndView and eventually ForceFirstFrameAfterNavigationTimeout().  It appears we end up taking a tab thumbnail capture of the old attacker-displayed content to use for the newly committed URL in the tab strip.  I suspect we do not ever want to use a paint from the previous commit, but maybe solving the paint timer issue above will make this go away by clearing the stale paint before tab capture.  CC'ing collinbaker@ just in case.  (Does this code apply on Android?  I don't have an Android build set up to see how we get to ForceFirstFrameAfterNavigationTimeout() on that platform; maybe alexmos@ can help with that part of the repro.)

I suspect the paint timer fix will be the quickest disruption to this bug, so I'll assign to jonross@ to help find an owner for that part.  We can continue looking at the other issues in parallel.  Thanks!

[Monorail components: Blink>Loader Internals>Compositing Internals>Sandbox>SiteIsolation UI>Browser>TabStrip]

### co...@chromium.org (2020-12-08)

re (4): this code isn't used on Android, just on desktop. Either way, I think displaying a thumbnail from a previous commit or from a failed commit is a bug.

I'm not sure how to handle this though. Upon a 204/205, should the old thumbnail be discarded and a new one captured? Even though in the normal case, this will be the same page?

Forgive me if the answer is obvious, I don't understand this exploit.

### jo...@chromium.org (2020-12-08)

Can I be added to https://crbug.com/chromium/1153204 so that I can see the additional context / repro steps?

### cr...@chromium.org (2020-12-09)

https://crbug.com/chromium/1152894#c10: Sure, just CC'd you.  Sorry for the delay there.

https://crbug.com/chromium/1152894#c9: In general, it seems like we shouldn't create a thumbnail of a tab after a DidFinishNavigation unless the last committed URL has produced a paint.  In this exploit, an about:blank tab is created, content is injected into it, URL A commits, then URL B returns an HTTP 204 response (no content).

If URL A had painted, it would be fine to create a thumbnail of it after its own DidFinishNavigation.  Similarly, I wouldn't be concerned if we updated the thumbnail of URL A at later points in time, such as when URL B "aborts" via a 204 response (since URL B never commits a new document).  However, we never get a paint from URL A's document at all in this bug, so it seems wrong to create a thumbnail after either URL A's DidFinishNavigation or URL B's DidFinishNavigation.  Here, the thumbnail includes the stale injected content from the about:blank document before URL A, which is wrong.

I suspect that fixing ForceFirstFrameAfterNavigationTimeout to actually clear the stale paint (while creating a thumbnail) would make this less important, since the thumbnail would be blank in that case rather than a stale paint.  Still, I agree with you that it may be safer if you can check whether there has been a paint since the URL committed, before trying to grab a thumbnail.

### jo...@chromium.org (2020-12-09)

+kylechar@ another Viz owner whom I'll need for reviews.

I'm taking a look at the Viz-side changes that are needed. 

A few things I've noted while debugging this:

1) For Desktop, BrowserNavigator::Nagivate is not being triggered, which would normally lead to advancing the Surfaces.
     Though RenderWidgetHostViewAura::OnDidNavigateMainFrameToNewPage is notified when we begin these navigations.

2) Android is a bit trickier. While it is similarly notified of thew navigation, it contains a mix of hidden-navigation edge cases and optimizations. With the goal of allocating the new surface once we start to become visible.

3)  Our Surface Eviction paths don't like being invoked when not visible

4)  SurfaceLayer with either invalid surfaces, or not-yet-produced surfaces, seems to be insufficient for invalidating the thumbnail imagery. 

I'm not familiar with the thumbnail taking, but will take a look to see how we can cancel when there is no valid surface.




### jo...@chromium.org (2020-12-10)

+dfried@ an OWNER of chrome/browser/ui/thumbnails

Hi,
While looking into this issue I've ran into an edge case with ThumbnailReadinessTracker.

I'm dealing with a navigation that never completed the document load. However when ThumbnailReadinessTracker::DidStartNavigation is called it correctly identified that NavigationShouldInvalidateThumbnail. 

However I am not familiar enough to know how/if we clear ThumbnailTabHelper::thumbnail_.

In this particular bug I'm looking at fixing how RenderWidgetHostImpl handles these interrupted navigations, by evicting the old/pre-navigation surfaces. This allows us to not present the old content on a tab change.

A side effect of this would be that the copy requests never return until a new valid surface is presented. So ThumbnailTabHelper::StoreThumbnail wouldn't be called. In the interim mousing over the tab seems to show the previous thumbnail image.

I'd appreciate any insight here on how we could clear the thumbnail in this case.



### co...@chromium.org (2020-12-10)

Huh, looks like the thumbnail doesn't get cleared. I think the best place to do this would be https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/thumbnails/thumbnail_tab_helper.cc;l=186;drc=0348a1421914f3609d287cb5645a856f5eb2542c when transitioning to PageReadiness::kNotReady

I think ThumbnailImage should have an additional method ClearThumbnail(). Seems the only way to do it currently would be to call AssignSkBitmap with a blank or empty bitmap. The implementation should be as simple as `data_->data.clear()`.

You're welcome to make this change if you're already working in that area. If not I can do it as well.

### jo...@chromium.org (2020-12-11)

I can make it a part of the change. Thanks for advice, that does allow for us to clear the thumbnail. Then the evicted surface prevents getting a new one while we don't have content to display.

### jo...@chromium.org (2020-12-11)

Potential CL is in flight: https://chromium-review.googlesource.com/c/chromium/src/+/2585790

### jo...@chromium.org (2020-12-14)

+khushalsagar@ an owner of ui/android for context on this as it pertains to the review.

### jo...@chromium.org (2020-12-15)

+boliu@ an owner of ui/android for context on this as it pertains to the review.

### jo...@chromium.org (2020-12-16)

The behaviour introduced in the code review leaves a grey region where the thumbnail normally displays. With a globe favicon in the middle of the region. (This seems to be the default favicon as the page that fails to load does not have its own custom one.)

See attached image of the new behaviour

### jo...@chromium.org (2020-12-16)

Regarding the new failing test:

browser_tests DeferAllScriptBrowserTest.DeferAllScriptRestoredPreviewWithBackForwardCache

This test attempts to take a screenshot during teardown:

#6 0x7ff3eaaa5534 content::DelegatedFrameHost::CopyFromCompositingSurfaceInternal()
#7 0x7ff3eaaa52f3 content::DelegatedFrameHost::CopyFromCompositingSurface()
#8 0x7ff3ea2e0986 content::RenderWidgetHostViewBase::CopyMainAndPopupFromSurface()
#9 0x7ff3ea2d2b31 content::RenderWidgetHostViewAura::CopyFromSurface()
#10 0x55a296959ca1 ThumbnailTabHelper::CaptureThumbnailOnTabHidden()
#11 0x55a29695c22e ThumbnailTabHelper::TabStateTracker::OnVisibilityChanged()
#12 0x7ff3ea7862b6 content::WebContentsImpl::SetVisibilityAndNotifyObservers()::$_40::operator()()
#13 0x7ff3ea754200 content::WebContentsImpl::WebContentsObserverList::ForEachObserver<>()
#14 0x7ff3ea747497 content::WebContentsImpl::SetVisibilityAndNotifyObservers()
#15 0x7ff3ea73933a content::WebContentsImpl::UpdateVisibilityAndNotifyPageAndView()
#16 0x7ff3ea780a1a content::WebContentsImpl::UpdateWebContentsVisibility()
#17 0x7ff3ea7c30eb content::WebContentsViewAura::UpdateWebContentsVisibility()
#18 0x7ff3ea7c48a8 content::WebContentsViewAura::OnWindowOcclusionChanged()
#19 0x7ff3debad4b9 aura::Window::SetOcclusionInfo()
#20 0x7ff3debc96ce aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder()
#21 0x7ff3debc9739 aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder()
#22 0x7ff3debd8cbc std::__Cr::default_delete<>::operator()()
#23 0x7ff3debd8c4a std::__Cr::unique_ptr<>::reset()
#24 0x7ff3debd3b19 std::__Cr::unique_ptr<>::~unique_ptr()
#25 0x7ff3debcf18f aura::WindowOcclusionTracker::MaybeComputeOcclusion()
#26 0x7ff3debd0f25 aura::WindowOcclusionTracker::Unpause()
#27 0x7ff3deb97131 aura::Env::UnpauseWindowOcclusionTracking()
#28 0x7ff3debcd429 aura::WindowOcclusionTracker::ScopedPause::~ScopedPause()
#29 0x7ff3deba908e aura::Window::SetVisible()
#30 0x7ff3deba90b7 aura::Window::Hide()
#31 0x7ff3efb80520 views::DesktopNativeWidgetAura::Hide()
#32 0x7ff3efb1e2f1 views::Widget::Hide()
#33 0x55a296cdd93a BrowserView::OnWindowCloseRequested()
#34 0x7ff3efb3f5b0 views::NonClientView::OnWindowCloseRequested()
#35 0x7ff3efb1da14 views::Widget::CloseWithReason()
#36 0x7ff3efb1dcb7 views::Widget::Close()
#37 0x55a296cd551c BrowserView::Close()
#38 0x55a2932d109c BrowserCloseManager::CloseBrowsers()
#39 0x55a2932d1466 BrowserCloseManager::CheckForDownloadsInProgress()
#40 0x55a2932d1312 BrowserCloseManager::TryToCloseBrowsers()
#41 0x55a2932d0f27 BrowserCloseManager::StartClosingBrowsers()
#42 0x55a292babbf2 chrome::CloseAllBrowsers()
#43 0x55a2929dcae9 BrowserProcessPlatformPartBase::AttemptExit()
#44 0x55a292babb42 chrome::AttemptExitInternal()
#45 0x55a292babf25 chrome::AttemptExit()
#46 0x55a28cf43ae7 base::internal::FunctorTraits<>::Invoke<>()
#47 0x55a28cf43abd base::internal::InvokeHelper<>::MakeItSo<>()
#48 0x55a28cf43a81 _ZN4base8internal7InvokerINS0_9BindStateIPFvvEJEEES3_E7RunImplIS4_NSt4__Cr5tupleIJEEEJEEEvOT_OT0_NS8_16integer_sequenceImJXspT1_EEEE
#49 0x55a28cf43a4c base::internal::Invoker<>::RunOnce()
#50 0x7ff3f76275f1 _ZNO4base12OnceCallbackIFvvEE3RunEv
#51 0x7ff3f77ef182 base::TaskAnnotator::RunTask()
#52 0x7ff3f783515a base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#53 0x7ff3f7834925 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#54 0x7ff3f78353b9 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#55 0x7ff3f76e1da1 base::MessagePumpGlib::HandleDispatch()
#56 0x7ff3f76e24f1 base::(anonymous namespace)::WorkSourceDispatch()
#57 0x7ff3be6ffb9b g_main_context_dispatch
#58 0x7ff3be6ffe48 (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.6600.1+0x51e47)
#59 0x7ff3be6ffeff g_main_context_iteration
#60 0x7ff3f76e1eb0 base::MessagePumpGlib::Run()
#61 0x7ff3f78359e0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#62 0x7ff3f7780f55 base::RunLoop::Run()
#63 0x55a2928ec95a InProcessBrowserTest::RunUntilBrowserProcessQuits()
#64 0x55a2928eddbc InProcessBrowserTest::QuitBrowsers()
#65 0x55a2928edc42 InProcessBrowserTest::PostRunTestOnMainThread()
#66 0x55a293abadbf content::BrowserTestBase::ProxyRunTestOnMainThreadLoop()
.... test launching part of stack....


Previously this would generate a viz::CopyOutputRequest, and forward the request to the GPU process. However before the changes in content/ there was still a valid Surface to perform the request on.

It appears that with this test a navigation has begun, but not completed, before the test attempts to tear down the browser. 
                      [delegated_frame_host.cc(467)] OnNavigateToNewPage LocalSurfaceId(7, 1, F8F0...)
                      [delegated_frame_host.cc(154)] JR CopyFromCompositingSurfaceInternal current LocalSurfaceId(0, 0, 0000...) pre-navigation LocalSurfaceId(7, 1, F8F0...)

With there being no valid surface we are canceling the request in DelegatedFrameHost::CopyFromCompositingSurfaceInternal.

viz::CopyOutputRequests always post-tasks its' callback, and it seems to be doing this on a worker thread instead of the UI thread in this particular case. Whereas the non-shutdown cases seen in resolving the bug occur on the UI thread.

[FATAL:thumbnail_tab_helper.cc(280)] Check failed: ::content::BrowserThread::CurrentlyOn(content::BrowserThread::UI). Must be called on Chrome_UIThread; actually called on ThreadPoolForegroundWorker.
#0 0x7f6b8deea95f base::debug::CollectStackTrace()
#1 0x7f6b8dc725ea base::debug::StackTrace::StackTrace()
#2 0x7f6b8dc725a5 base::debug::StackTrace::StackTrace()
#3 0x7f6b8dcbe1f9 logging::LogMessage::~LogMessage()
#4 0x7f6b8dcbe939 logging::LogMessage::~LogMessage()
#5 0x7f6b8dc31e5b logging::CheckError::~CheckError()
#6 0x5635a2af91cd ThumbnailTabHelper::StoreThumbnail()
#7 0x5635a2af90ef ThumbnailTabHelper::StoreThumbnailForTabSwitch()
#8 0x5635a2afc1cf base::internal::FunctorTraits<>::Invoke<>()
#9 0x5635a2afc061 base::internal::InvokeHelper<>::MakeItSo<>()
#10 0x5635a2afbfa8 _ZN4base8internal7InvokerINS0_9BindStateIM18ThumbnailTabHelperFvNS_9TimeTicksERK8SkBitmapEJNS_7WeakPtrIS3_EES4_EEEFvS7_EE7RunImplIS9_NSt4__Cr5tupleIJSB_S4_EEEJLm0ELm1EEEEvOT_OT0_NSG_16integer_sequenceImJXspT1_EEEES7_
#11 0x5635a2afbf21 base::internal::Invoker<>::RunOnce()
#12 0x7f6b7f483af6 _ZNO4base12OnceCallbackIFvRK8SkBitmapEE3RunES3_
#13 0x7f6b810a7c82 content::DelegatedFrameHost::CopyFromCompositingSurface()::$_0::operator()()
#14 0x7f6b810a7c1c base::internal::FunctorTraits<>::Invoke<>()
#15 0x7f6b810a7bb7 base::internal::InvokeHelper<>::MakeItSo<>()
#16 0x7f6b810a7b57 _ZN4base8internal7InvokerINS0_9BindStateIZN7content18DelegatedFrameHost26CopyFromCompositingSurfaceERKN3gfx4RectERKNS5_4SizeENS_12OnceCallbackIFvRK8SkBitmapEEEE3$_0JSH_EEEFvNSt4__Cr10unique_ptrIN3viz16CopyOutputResultENSK_14default_deleteISN_EEEEEE7RunImplISI_NSK_5tupleIJSH_EEEJLm0EEEEvOT_OT0_NSK_16integer_sequenceImJXspT1_EEEEOSQ_
#17 0x7f6b810a7af1 base::internal::Invoker<>::RunOnce()
#18 0x7f6b7b5e9d66 _ZNO4base12OnceCallbackIFvNSt4__Cr10unique_ptrIN3viz16CopyOutputResultENS1_14default_deleteIS4_EEEEEE3RunES7_
#19 0x7f6b7b5e9cd6 base::internal::FunctorTraits<>::Invoke<>()
#20 0x7f6b7b5e9bc2 base::internal::InvokeHelper<>::MakeItSo<>()
#21 0x7f6b7b5e9b72 _ZN4base8internal7InvokerINS0_9BindStateINS_12OnceCallbackIFvNSt4__Cr10unique_ptrIN3viz16CopyOutputResultENS4_14default_deleteIS7_EEEEEEEJSA_EEEFvvEE7RunImplISC_NS4_5tupleIJSA_EEEJLm0EEEEvOT_OT0_NS4_16integer_sequenceImJXspT1_EEEE
#22 0x7f6b7b5e9b1c base::internal::Invoker<>::RunOnce()
#23 0x7f6b8dc285f1 _ZNO4base12OnceCallbackIFvvEE3RunEv
#24 0x7f6b8ddf0182 base::TaskAnnotator::RunTask()
#25 0x7f6b8de66608 base::internal::TaskTracker::RunSkipOnShutdown()
#26 0x7f6b8de66250 base::internal::TaskTracker::RunTaskWithShutdownBehavior()
#27 0x7f6b8de65d61 base::internal::TaskTracker::RunTask()
#28 0x7f6b8df20a95 base::internal::TaskTrackerPosix::RunTask()
#29 0x7f6b8de6524f base::internal::TaskTracker::RunAndPopNextTask()
#30 0x7f6b8de7fec2 base::internal::WorkerThread::RunWorker()


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/865a12d72b770520f88775d5e37810ead62d82c8

commit 865a12d72b770520f88775d5e37810ead62d82c8
Author: Jonathan Ross <jonross@chromium.org>
Date: Wed Dec 16 22:33:00 2020

Evict Surfaces from Before Navigation When Re-using DelegatedFrameHost

When we are not applying site-isolation a DelegatedFrameHost can be 
re-used when navigating between different pages. This can occur on 
Android as well as with the un-supported flag
--disable-site-isolation-trials.

When RenderWidgetHostImpl::ForceFirstFrameAfterNavigationTimeout is 
invoked, as either from tab-changing, or from thumbnailing, we set 
fallback surfaces. This is intended to be the first viz::SurfaceId that 
was generated by navigation.

However if a navigation fails we don't actually embed a new surface. The
DelegatedFrameHost then ends up utilizing outdated surfaces as the 
fallback.

This change updates DelegatedFrameHost to be notified of when a 
navigation begins. If we fail to embed a new surface by the timeout, 
we evict the surface that predates the navigation.

The ThumbnailTabHelper has been updated to also clear its currently 
cached thumbnail in the case that the page has transitioned back to the
unready state. Thus clearing thumbnails that exist from before a 
navigation.

TEST=NoCompositingRenderWidgetHostViewBrowserTest.
         NoFallbackAfterHiddenNavigationFails

Bug: 1152894
Change-Id: Ia5734abb5201a56c271114a891bc81212a3aa975
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2585790
Reviewed-by: Dana Fried <dfried@chromium.org>
Reviewed-by: Jonathan Ross <jonross@chromium.org>
Reviewed-by: kylechar <kylechar@chromium.org>
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Bo <boliu@chromium.org>
Commit-Queue: Jonathan Ross <jonross@chromium.org>
Cr-Commit-Position: refs/heads/master@{#837779}

[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/chrome/browser/ui/thumbnails/thumbnail_tab_helper.cc
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/chrome/browser/ui/thumbnails/thumbnail_image.h
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/content/browser/renderer_host/delegated_frame_host.h
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/chrome/browser/ui/thumbnails/thumbnail_tab_helper.h
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/content/browser/renderer_host/delegated_frame_host.cc
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/ui/android/delegated_frame_host_android.cc
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/content/browser/renderer_host/render_widget_host_view_base.h
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/ui/android/delegated_frame_host_android.h
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/content/browser/renderer_host/render_widget_host_view_android.cc
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/content/browser/renderer_host/render_widget_host_view_browsertest.cc
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/chrome/browser/ui/thumbnails/thumbnail_image.cc
[modify] https://crrev.com/865a12d72b770520f88775d5e37810ead62d82c8/content/browser/renderer_host/render_widget_host_view_aura.cc


### cr...@chromium.org (2020-12-16)

Thanks jonross@!  Does r837779 take care of points (3) and (4) from https://crbug.com/chromium/1152894#c8?  That seems like it would take care of most of the security impact, allowing us to look into (2) in a separate issue (i.e., why same-process 204 interrupts loading but cross-process 204 doesn't).

### jo...@chromium.org (2020-12-17)

Correct,  r837779 addresses points (3) and (4) from https://crbug.com/chromium/1152894#c8. This address the behaviours seen on Android, as well as desktop with --disable-site-isolation-trials.

In the review dfried@ and collinbaker@ identified some follow-up work for the thumbnail portion of the fix. However as the previous thumbnail is cleared by the patch this should be sufficient to alleviate the security concerns.

You are also correct that point (2) can be investigated as a separate issue.

I'm going to assign this to collinbaker@ for the thumbnail follow-up.

### ad...@google.com (2020-12-21)

jonross@ would you mind filing a separate crbug for the follow up work, then marking this crbug as Fixed? That will cause Sheriffbot to initiate the merge process for getting this security bug merged back to the appropriate branches. (As an externally reported medium severity bug, I think sheriffbot will choose to merge this to beta, but only after the VRP panel have confirmed the severity).

### da...@chromium.org (2020-12-22)

I think the CL in #21 is causing crashes: https://bugs.chromium.org/p/chromium/issues/detail?id=1160146#c10

collin would you be able to have a look as jonross is away?

### [Deleted User] (2020-12-25)

collinbaker: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-01-05)

https://crbug.com/chromium/1163121 filed to track the follow-up work so that merging work for r837779 can be tracked here. Per https://crbug.com/chromium/1152894#c35

Per https://crbug.com/chromium/1152894#c25 it's suspected that this has introduced a crash in https://crbug.com/chromium/1160146. I am not marking this as fixed until we've addressed the crash. I don't want to merge back crashes.

### kh...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-01-08)

A fix to the blocking crash in https://crbug.com/chromium/1160146 was landed by https://chromium-review.googlesource.com/c/chromium/src/+/2611174

I'm going to request a merge for both that as well as r837779

### [Deleted User] (2021-01-08)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2021-01-08)

1. M-88 yes
     M-87 no, as it is after stable release
2. https://chromium-review.googlesource.com/c/chromium/src/+/2585790
    https://chromium-review.googlesource.com/c/chromium/src/+/2611174
3. Yes
4. Yes, was requested for M-87. Should be at least merged into M-88
5. Security bug found in Stable
6. No
7. N/A


### go...@chromium.org (2021-01-08)

+adetaylor@ (Security TPM) for M88 merge review. Thank you.

### ad...@chromium.org (2021-01-08)

As this is a medium severity bug, and there's already been some hints of instability, I think we should let this organically release in M89 instead of merging to M88 (which doesn't have too long till we release).

### jo...@chromium.org (2021-01-11)

With the merge review leading to rejections, there is no more work to be done here. All follow up work for Thumbnails is tracked in https://crbug.com/chromium/1163121.

I'll close this as fixed now. Thank you everyone for the help in debugging the issue, and getting a fix landed!

### [Deleted User] (2021-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

Congratulations, Irvan! The VRP Panel has decided to award you $3,000 for this report. A member of the finance will soon be in touch to arrange payment. Nice work and thank you for your submission!

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-01-23)

Thank you very much for the reward!

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-04)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@gmail.com (2021-06-09)

For me this issue is still reproduced on Chrome if the internet connection is slow. May happened if the mobile signal is weak or on the restricted connection.

To reproduce it:
1. Restrict internet connection for the device to 64 kbit/s;
2. Use original issue steps.

Is such case of low speed connection an issue needs to be fixed?


### jo...@chromium.org (2021-06-09)

Could you file a new issue for this? Feel free to list it as related to this one.

Please include steps to reproduce. 
   - Including if you were using the test page (http://csreis.github.io/tests/interrupt-popup.html) or if you were using other sites. 
   - As well as what was the error looked like.

### al...@gmail.com (2021-06-10)

Thanks,  I asked in the new issue: https://bugs.chromium.org/p/chromium/issues/detail?id=1218366. 

### li...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1152894?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Internals>Compositing, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail blocked-on: crbug.com/chromium/1160146]
[Monorail blocking: crbug.com/chromium/1163121, crbug.com/chromium/1453638]
[Monorail mergedwith: crbug.com/chromium/1153204]
[Monorail components added to Component Tags custom field.]

### mk...@opera.com (2026-01-15)

It seems to me this issue is still not fixed in WebView (Tested on M144), should it be? Any chances to get access to this ticket <https://bugs.chromium.org/p/chromium/issues/detail?id=1218366> ?
Is the site-per-process flag required to be enabled for the fix to work?
Is the site-per-process flag planned to ever be enabled by default for WebView?

### to...@google.com (2026-01-20)

> It seems to me this issue is still not fixed in WebView (Tested on M144), should it be?

Do you have a repro case for this in WebView - a test app with source code? Or otherwise a specific reason to believe that you're seeing this specific issue with painting and not something else?

WebView's callbacks unfortunately have complex and not-clearly-documented behaviors for legacy compatibility, and this makes it difficult to implement a URL bar in a way that's robust to this kind of timing-based spoofing - seeing the implementation code for updating the URL bar would help figure out what the problem actually is.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053991)*
