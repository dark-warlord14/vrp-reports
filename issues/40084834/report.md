# Security: SEGV on unknown address in toCSSValuePair

| Field | Value |
|-------|-------|
| **Issue ID** | [40084834](https://issues.chromium.org/issues/40084834) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation |
| **Reporter** | fi...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-07-13 |
| **Bounty** | $3,000.00 |

## Description

# **VULNERABILITY DETAILS** ASSERTION FAILED: value.isValuePair() ../../third\_party/WebKit/Source/core/css/CSSValuePair.h(88) : const blink::CSSValuePair &blink::toCSSValuePair(const blink::CSSValue &) 1 0x55a76b99adc6 2 0x55a76bc891ad 3 0x55a76b9983fb 4 0x55a76b97fc7a 5 0x55a76b982d61 6 0x55a76b9858b5 7 0x55a76add9691 8 0x55a76add1c50 9 0x55a76adcb6e4 10 0x55a769e88880 11 0x55a769e8cf6e 12 0x55a769e7b552 13 0x55a76b1bac12 14 0x55a76b1b6eeb 15 0x55a76b1b554c 16 0x55a76b6d05b5 17 0x55a7687126e1 18 0x55a771346103 19 0x55a77443bac0 20 0x55a774471c74 21 0x55a762abffb2 22 0x55a776b240c5 23 0x55a776b1fa74 24 0x55a776b264f8 25 0x55a762abffb2 26 0x55a762942926 27 0x55a762943720 28 0x55a762944d5b 29 0x55a76294ee9e 30 0x55a7629b20ba 31 0x55a770fefd02 ASAN:DEADLYSIGNAL

==27466==ERROR: AddressSanitizer: SEGV on unknown address 0x00009f7537dd (pc 0x55a76b99adc6 bp 0x7fffe868d930 sp 0x7fffe868d920 T0)  

==27466==The signal is caused by a READ memory access.  

#0 0x55a76b99adc5 in toCSSValuePair third\_party/WebKit/Source/core/css/CSSValuePair.h:88:1  

#1 0x55a76b99adc5 in blink::CSSLengthPairInterpolationType::maybeConvertValue(blink::CSSValue const&, blink::StyleResolverState const&, WTF::Vector<std::\_\_1::unique\_ptr<blink::InterpolationType::ConversionChecker, std::\_\_1::default\_delete[blink::InterpolationType::ConversionChecker](javascript:void(0);) >, 0ul, WTF::PartitionAllocator>&) const third\_party/WebKit/Source/core/animation/CSSLengthPairInterpolationType.h:24  

#2 0x55a76bc891ac in blink::CSSInterpolationType::maybeConvertSingle(blink::Keyframe::PropertySpecificKeyframe const&, blink::InterpolationEnvironment const&, blink::InterpolationValue const&, WTF::Vector<std::\_\_1::unique\_ptr<blink::InterpolationType::ConversionChecker, std::\_\_1::default\_delete[blink::InterpolationType::ConversionChecker](javascript:void(0);) >, 0ul, WTF::PartitionAllocator>&) const third\_party/WebKit/Source/core/animation/CSSInterpolationType.cpp:64:12  

#3 0x55a76b9983fa in blink::InterpolationType::maybeConvertPairwise(blink::Keyframe::PropertySpecificKeyframe const&, blink::Keyframe::PropertySpecificKeyframe const&, blink::InterpolationEnvironment const&, blink::InterpolationValue const&, WTF::Vector<std::\_\_1::unique\_ptr<blink::InterpolationType::ConversionChecker, std::\_\_1::default\_delete[blink::InterpolationType::ConversionChecker](javascript:void(0);) >, 0ul, WTF::PartitionAllocator>&) const third\_party/WebKit/Source/core/animation/InterpolationType.h:57:34  

#4 0x55a76b97fc79 in blink::InvalidatableInterpolation::maybeConvertPairwise(blink::InterpolationEnvironment const&, blink::UnderlyingValueOwner const&) const third\_party/WebKit/Source/core/animation/InvalidatableInterpolation.cpp:35:64  

#5 0x55a76b982d60 in blink::InvalidatableInterpolation::ensureValidInterpolation(blink::InterpolationEnvironment const&, blink::UnderlyingValueOwner const&) const third\_party/WebKit/Source/core/animation/InvalidatableInterpolation.cpp:129:78  

#6 0x55a76b9858b4 in blink::InvalidatableInterpolation::applyStack(WTF::Vector<WTF::RefPtr[blink::Interpolation](javascript:void(0);), 1ul, WTF::PartitionAllocator> const&, blink::InterpolationEnvironment&) third\_party/WebKit/Source/core/animation/InvalidatableInterpolation.cpp:196:76  

#7 0x55a76add9690 in void blink::StyleResolver::applyAnimatedProperties<(blink::CSSPropertyPriority)2>(blink::StyleResolverState&, WTF::HashMap<blink::PropertyHandle, WTF::Vector<WTF::RefPtr[blink::Interpolation](javascript:void(0);), 1ul, WTF::PartitionAllocator>, WTF::DefaultHash[blink::PropertyHandle](javascript:void(0);)::Hash, WTF::HashTraits[blink::PropertyHandle](javascript:void(0);), WTF::HashTraits<WTF::Vector<WTF::RefPtr[blink::Interpolation](javascript:void(0);), 1ul, WTF::PartitionAllocator> >, WTF::PartitionAllocator> const&) third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:1182:13  

#8 0x55a76add1c4f in blink::StyleResolver::applyAnimatedProperties(blink::StyleResolverState&, blink::Element const\*) third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:1143:5  

#9 0x55a76adcb6e3 in blink::StyleResolver::styleForElement(blink::Element\*, blink::ComputedStyle const\*, blink::StyleSharingBehavior, blink::RuleMatchingBehavior) third\_party/WebKit/Source/core/css/resolver/StyleResolver.cpp:833:9  

#10 0x55a769e8887f in blink::Document::inheritHtmlAndBodyElementStyles(blink::StyleRecalcChange) third\_party/WebKit/Source/core/dom/Document.cpp:1526:47  

#11 0x55a769e8cf6d in blink::Document::updateStyle() third\_party/WebKit/Source/core/dom/Document.cpp:1779:9  

#12 0x55a769e7b551 in blink::Document::updateStyleAndLayoutTree() third\_party/WebKit/Source/core/dom/Document.cpp:1717:5  

#13 0x55a76b1bac11 in blink::FrameView::updateStyleAndLayoutIfNeededRecursiveInternal() third\_party/WebKit/Source/core/frame/FrameView.cpp:2703:26  

#14 0x55a76b1b6eea in blink::FrameView::updateStyleAndLayoutIfNeededRecursive() third\_party/WebKit/Source/core/frame/FrameView.cpp:2683:5  

#15 0x55a76b1b554b in blink::FrameView::updateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) third\_party/WebKit/Source/core/frame/FrameView.cpp:2529:5  

#16 0x55a76b6d05b4 in blink::PageAnimator::updateAllLifecyclePhases(blink::LocalFrame&) third\_party/WebKit/Source/core/page/PageAnimator.cpp:85:11  

#17 0x55a7687126e0 in blink::WebViewImpl::updateAllLifecyclePhases() third\_party/WebKit/Source/web/WebViewImpl.cpp:2012:5  

#18 0x55a771346102 in content::RenderWidgetCompositor::UpdateLayerTreeHost() content/renderer/gpu/render\_widget\_compositor.cc:1016:14  

#19 0x55a77443babf in cc::ProxyMain::BeginMainFrame(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >) cc/trees/proxy\_main.cc:199:21  

#20 0x55a774471c73 in Invoke<base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:214:12  

#21 0x55a774471c73 in MakeItSo<void (cc::ProxyMain::\*const &)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > base/bind\_internal.h:303  

#22 0x55a774471c73 in void base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > >, void ()>::RunImpl<void (cc::ProxyMain::\* const&)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > const&, 0ul, 1ul>(void (cc::ProxyMain::\* const&)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >), std::\_\_1::tuple<base::WeakPtr[cc::ProxyMain](javascript:void(0);), base::internal::PassedWrapper<std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState, std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > > > const&, base::IndexSequence<0ul, 1ul>) base/bind\_internal.h:346  

#23 0x55a762abffb1 in Run base/callback.h:389:12  

#24 0x55a762abffb1 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#25 0x55a776b240c4 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue\*, scheduler::internal::TaskQueueImpl::Task\*) components/scheduler/base/task\_queue\_manager.cc:315:19  

#26 0x55a776b1fa73 in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task\_queue\_manager.cc:218:13  

#27 0x55a776b264f7 in Invoke<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:214:12  

#28 0x55a776b264f7 in MakeItSo<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), const base::TimeTicks &, const bool &> base/bind\_internal.h:303  

#29 0x55a776b264f7 in RunImpl<void (scheduler::TaskQueueManager::\*const &)(base::TimeTicks, bool), const std::\_\_1::tuple<base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool> &, 0, 1, 2> base/bind\_internal.h:346  

#30 0x55a776b264f7 in base::internal::Invoker<base::internal::BindState<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool), base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);), base::TimeTicks, bool>, void ()>::Run(base::internal::BindStateBase\*) base/bind\_internal.h:324  

#31 0x55a762abffb1 in Run base/callback.h:389:12  

#32 0x55a762abffb1 in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:51  

#33 0x55a762942925 in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:494:19  

#34 0x55a76294371f in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message\_loop/message\_loop.cc:503:5  

#35 0x55a762944d5a in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:627:13  

#36 0x55a76294ee9d in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:35:31  

#37 0x55a7629b20b9 in base::RunLoop::Run() base/run\_loop.cc:35:10  

#38 0x55a770fefd01 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:198:23  

#39 0x55a7627f13f7 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:343:14  

#40 0x55a7627f5aa5 in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:785:12  

#41 0x55a7627f018d in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:20:28  

#42 0x55a76170aea5 in ChromeMain chrome/app/chrome\_main.cc:84:12  

#43 0x7f9455f34740 in \_\_libc\_start\_main (/usr/lib/libc.so.6+0x20740)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV third\_party/WebKit/Source/core/css/CSSValuePair.h:88:1 in toCSSValuePair  

==27466==ABORTING

**VERSION**  

Chromium: 54.0.2795.0 (Developer Build) (64-bit) (asan-linux-release-404895)  

Chrome: 53.0.2785.8 (Official Build) dev-m (32-bit)  

Chrome: 54.0.2794.0 (Official Build) canary (32-bit)

**REPRODUCTION CASE**

<style>
@keyframes AAAA {99% { border-radius: var(--VVVV) }}
</style>
<script>
function crash() {
document.body.style.cssText = 'animation: AAAA +99.99s 9999'
}
</script>
<body onload='crash()'>

## Timeline

### cl...@chromium.org (2016-07-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5133903849586688

### cl...@chromium.org (2016-07-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5133903849586688

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  value.isValuePair()
  blink::CSSLengthPairInterpolationType::maybeConvertValue
  blink::CSSInterpolationType::maybeConvertSingle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=402485:402738

Minimized Testcase (0.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97_dNm4sF7otcOpyRe-RshD7WjrOOoZ5Zew2KXIWeO2dXKCxRluRklmIoX-0i40-6symYS_Sf_7EpN5D9L-PwuCWrSdJvlxps2Ws3544OieLFBC0q5--FyiffIMEaNEczXQ5xQLD994vQyXAlLubXo4-3N8Kg?testcase_id=5133903849586688
<style>
	@keyframes AAAA {99% { border-radius: var(--VVVV) }}
</style>
<script>
function crash() {
	document.body.style.cssText = 'animation: AAAA +99.99s 9999'
}
</script>
<body onload='crash()'>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ta...@google.com (2016-07-13)

alancutter@, I wonder if you could take a look at this. It seems similar to https://bugs.chromium.org/p/chromium/issues/detail?id=590609

[Monorail components: Blink>CSS]

### al...@chromium.org (2016-07-14)

Thanks for assigning this to me, this is an animation bug.

[Monorail components: -Blink>CSS Blink>Animation]

### al...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### al...@chromium.org (2016-07-14)

This would have been introduced by https://chromium.googlesource.com/chromium/src/+/6b045cf7e0fe8f7eb94dc94508d75dbde7e63365/ which added the CSSPendingSubstitutionValue class.

I'm a little concerned that this was never caught by ClusterFuzz, I think some work ought to be done in adding better fuzzing for custom properties and var() given they seem to be breaking existing assumptions about how CSSVariables work here and there.

### al...@chromium.org (2016-07-14)

Confirmed this was introduced by 6b045cf7e0fe8f7eb94dc94508d75dbde7e63365 (Chrome 53).

### sh...@chromium.org (2016-07-14)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2016-07-14)

M53 beta launch is coming soon.Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix before 6:00 PM PST, Monday (07/18/16). Thank you.

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6ca1fb7dc6ea62d05099bc87b5a11f19f11a8ae

commit f6ca1fb7dc6ea62d05099bc87b5a11f19f11a8ae
Author: alancutter <alancutter@chromium.org>
Date: Fri Jul 15 04:34:41 2016

Avoid mishandling CSSPendingSubstitutionValues in CSS animations

This change ensures we have a code path for CSSPendingSubstitutionValues
during animation, it does not attempt to perform the correct animated
behaviour just yet.

BUG=627756

Review-Url: https://codereview.chromium.org/2146053003
Cr-Commit-Position: refs/heads/master@{#405699}

[add] https://crrev.com/f6ca1fb7dc6ea62d05099bc87b5a11f19f11a8ae/third_party/WebKit/LayoutTests/animations/animate-shorthand-var-crash.html
[modify] https://crrev.com/f6ca1fb7dc6ea62d05099bc87b5a11f19f11a8ae/third_party/WebKit/Source/core/animation/CSSInterpolationType.cpp


### al...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2016-07-16)

ClusterFuzz has detected this issue as fixed in range 405656:405727.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5133903849586688

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  value.isValuePair()
  blink::CSSLengthPairInterpolationType::maybeConvertValue
  blink::CSSInterpolationType::maybeConvertSingle
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=402485:402738
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=405656:405727

Minimized Testcase (0.20 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97_dNm4sF7otcOpyRe-RshD7WjrOOoZ5Zew2KXIWeO2dXKCxRluRklmIoX-0i40-6symYS_Sf_7EpN5D9L-PwuCWrSdJvlxps2Ws3544OieLFBC0q5--FyiffIMEaNEczXQ5xQLD994vQyXAlLubXo4-3N8Kg?testcase_id=5133903849586688
<style>
	@keyframes AAAA {99% { border-radius: var(--VVVV) }}
</style>
<script>
function crash() {
	document.body.style.cssText = 'animation: AAAA +99.99s 9999'
}
</script>
<body onload='crash()'>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-07-16)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-18)

+awhalley@, whether it is ok to take this merge in for M53 or not. Please note that fix has been already verified by clusterfuzz.

### aw...@chromium.org (2016-07-18)

Looks good to merge to M53.

### go...@chromium.org (2016-07-18)

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/627756#c16. Please merge ASAP or latest by 5:00 PM PST today so we can take it for M53 dev release tomorrow. Thank you.


### bu...@chromium.org (2016-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9fbce092057bbf5490f989bbe949c8820c01f415

commit 9fbce092057bbf5490f989bbe949c8820c01f415
Author: Alan Cutter <alancutter@chromium.org>
Date: Tue Jul 19 00:51:36 2016

Avoid mishandling CSSPendingSubstitutionValues in CSS animations

This change ensures we have a code path for CSSPendingSubstitutionValues
during animation, it does not attempt to perform the correct animated
behaviour just yet.

BUG=627756

Review-Url: https://codereview.chromium.org/2146053003
Cr-Commit-Position: refs/heads/master@{#405699}
(cherry picked from commit f6ca1fb7dc6ea62d05099bc87b5a11f19f11a8ae)

Review URL: https://codereview.chromium.org/2162773002 .

Cr-Commit-Position: refs/branch-heads/2785@{#211}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[add] https://crrev.com/9fbce092057bbf5490f989bbe949c8820c01f415/third_party/WebKit/LayoutTests/animations/animate-shorthand-var-crash.html
[modify] https://crrev.com/9fbce092057bbf5490f989bbe949c8820c01f415/third_party/WebKit/Source/core/animation/CSSInterpolationType.cpp


### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

Congratulations! The panel has decided to reward $3,000 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-10-21)

This issue was migrated from crbug.com/chromium/627756?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084834)*
