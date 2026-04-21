# Security DCHECK failed: IsA<Derived>(from) in ng_block_node.cc:1032 blink::NGBlockNode::FirstChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40058237](https://issues.chromium.org/issues/40058237) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2021-12-15 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4761.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-951496.zip

#Reproduce
1. chrome --js-flags='--expose_gc --allow-natives-syntax' --no-sandbox --enable-blink-test-features --user-data-dir=notexits fuzz-01.html

What is the expected behavior?

What went wrong?
Type of crash
render tab

#Analysis
Not yet

#Patch
Not yet

#asan
[5056:19984:1214/144909.380:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from). 
Backtrace:
	base::debug::CollectStackTrace [0x00007FFC42A2B212+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:305)
	base::debug::StackTrace::StackTrace [0x00007FFC4285255A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:197)
	logging::LogMessage::~LogMessage [0x00007FFC4288AA0C+860] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:587)
	blink::NGBlockNode::FirstChild [0x00007FFC4DD67645+1141] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:1032)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E5F87+3575] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:607)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E4C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFC4DD779D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFC4DD57617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::`anonymous namespace'::LayoutInflow [0x00007FFC509029D7+887] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:121)
	blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFC50901B96+2070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1652)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E6C7E+6894] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:698)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E4C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::NGColumnLayoutAlgorithm::CalculateBalancedColumnBlockSize [0x00007FFC508D956A+1642] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_column_layout_algorithm.cc:1132)
	blink::NGColumnLayoutAlgorithm::LayoutRow [0x00007FFC508D3AD4+2212] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_column_layout_algorithm.cc:609)
	blink::NGColumnLayoutAlgorithm::LayoutChildren [0x00007FFC508CE55C+3660] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_column_layout_algorithm.cc:425)
	blink::NGColumnLayoutAlgorithm::Layout [0x00007FFC508CC8C7+1287] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_column_layout_algorithm.cc:259)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGColumnLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFC4DD773F9+329] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFC4DD57617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFC508F8533+3395] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1526)
	blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFC508F4F65+3477] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1317)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E6BC1+6705] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:694)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E4C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFC4DD779D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFC4DD57617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::`anonymous namespace'::LayoutInflow [0x00007FFC509029D7+887] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:121)
	blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFC50901B96+2070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1652)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E6C7E+6894] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:698)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E4C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFC4DD779D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFC4DD57617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::`anonymous namespace'::LayoutInflow [0x00007FFC509029D7+887] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:121)
	blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFC50901B96+2070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1652)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E6C7E+6894] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:698)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFC508E4C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFC4DD779D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFC4DD57617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::LayoutNGMixin<blink::LayoutTableCaption>::UpdateInFlowBlockLayout [0x00007FFC4E929C4F+1071] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_mixin.cc:392)
	blink::LayoutNGBlockFlowMixin<blink::LayoutRubyRun>::UpdateNGBlockLayout [0x00007FFC4E1C1645+245] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_block_flow_mixin.cc:241)
	blink::LayoutBlock::UpdateLayout [0x00007FFC4A780404+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:464)
	blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFC4A8D5C05+1653] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:837)
	blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFC4A8D7D5E+1566] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:952)
	blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFC4A8D17A1+1953] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1649)
	blink::LayoutBlockFlow::LayoutChildren [0x00007FFC4A8CBB10+1248] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:622)
	blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFC4A8CA8CF+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
	blink::LayoutView::UpdateBlockLayout [0x00007FFC4767250D+2109] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:338)
	blink::LayoutBlock::UpdateLayout [0x00007FFC4A780404+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:464)
	blink::LayoutView::UpdateLayout [0x00007FFC47672FC4+1780] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:379)
	blink::LocalFrameView::PerformLayout [0x00007FFC4750795C+4684] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:837)
	blink::LocalFrameView::UpdateLayout [0x00007FFC4750A5CD+1197] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:898)
	blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FFC4752E29E+1038] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3334)
	blink::LocalFrameView::UpdateStyleAndLayout [0x00007FFC475130A4+340] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3274)
	blink::Document::UpdateStyleAndLayout [0x00007FFC475D6F71+801] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2477)
	blink::HTMLPlugInElement::LayoutEmbeddedContentForJSBindings [0x00007FFC4A7E48E9+73] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_plugin_element.cc:487)
	blink::HTMLPlugInElement::PluginWrapper [0x00007FFC4A7E3BEB+827] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_plugin_element.cc:390)
	blink::V8HTMLObjectElement::NamedPropertyGetterCustom [0x00007FFC507BB296+1014] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\custom\v8_html_plugin_element_custom.cc:146)
	blink::V8HTMLObjectElement::NamedPropertyGetterCallback [0x00007FFC4DC7DD8F+223] (C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_html_object_element.cc:91)
	v8::internal::PropertyCallbackArguments::CallNamedGetter [0x00007FFC3EED43DC+860] (C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:181)
	v8::internal::`anonymous namespace'::GetPropertyWithInterceptorInternal [0x00007FFC3F347196+1142] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-objects.cc:1140)
	v8::internal::JSObject::GetPropertyWithInterceptor [0x00007FFC3F346CB7+247] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-objects.cc:5182)
	v8::internal::Object::GetProperty [0x00007FFC3F45B0FC+444] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1159)
	v8::internal::LoadIC::Load [0x00007FFC3EE7F494+6724] (C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:510)
	v8::internal::Runtime_LoadNoFeedbackIC_Miss [0x00007FFC3EEA6F5A+1066] (C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2593)

Did this work before? N/A 

Chrome version: 99.0.4761.0  Channel: n/a
OS Version: 10.0

## Attachments

- [fuzz-01.html](attachments/fuzz-01.html) (text/plain, 1.3 KB)
- [h1.js](attachments/h1.js) (text/plain, 741 B)

## Timeline

### [Deleted User] (2021-12-15)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-16)

futhark: One more, could you please help triage? Thanks.

[Monorail components: Blink>Layout]

### me...@chromium.org (2021-12-20)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-01-05)

Starts crashing with --enable-blink-features=LayoutNGBlockFragmentation


### ms...@chromium.org (2022-01-05)

Feature not enabled by default.

### ms...@chromium.org (2022-01-05)

No crash if we also --enable-blink-features=LayoutNGBlockInInline , which should be enabled for testing soon enough.

### m....@gmail.com (2022-01-06)

re https://crbug.com/chromium/1280132#c5
Even if the feature is not enabled by default, it should still be a security issue.
If there is no other reason, please set the type as a security issue, because this also affects VRP, I suggest CC a security team member(like amyressler@chromium.org) to solve it together.

### ms...@chromium.org (2022-01-06)

What's VRP?
There's no security risk to users, so Bug-Security seems wrong. We won't ship LayoutNGBlockFragmentation with this bug present.

### m....@gmail.com (2022-01-06)

If the bug can't impact Chrome users by default, this is denoted instead by the Security-Impact_None label. See the security labels document for more information. The bug should still have a severity set according to these guidelines.

For more information, refer to the link below
https://source.chromium.org/chromium/chromium/src/+/main:docs/security/severity-guidelines.md
https://source.chromium.org/chromium/chromium/src/+/main:docs/security/security-labels.md
https://source.chromium.org/chromium/chromium/src/+/main:docs/security/vrp-faq.md

### ms...@chromium.org (2022-01-06)

Thanks for the links. Changing it back to a security bug.

### am...@google.com (2022-01-06)

Thank you for tagging me in. This is correct that security bugs in features not enabled by default are still considered and should be handled as such, but denoted as Security_Impact-None. So while this was sheriffed at high, there isn't the same SLO to fix. But we would definitely want to have this addressed before the feature is enabled for testing. 
It's also helpful to note that security DHECK failures can be indicative of a security issue, but also may not be and aren't always exploitable. Any additional data that could be provided to demonstrate exploitability and this as a security issue is especially helpful and most welcomed. 

### am...@chromium.org (2022-01-06)

[Comment Deleted]

### am...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-06)

Sorry, trying to do too much at once and now using correct account. Security triaged security bugs need to have an owner, so reassigning back to you, mstensho@. Please feel free to reassign to someone more appropriate based on how your team is triaging and prioritizing security bugs. 

### cl...@chromium.org (2022-01-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5650572862357504.

### cl...@chromium.org (2022-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4671972096933888.

### do...@chromium.org (2022-01-18)

mstensho: is this (like https://crbug.com/chromium/1279665) also fixed by https://chromium-review.googlesource.com/c/chromium/src/+/3370281 ?

### ms...@chromium.org (2022-01-19)

No - see https://crbug.com/chromium/1280132#c6. The test in https://crbug.com/chromium/1280132#c0 is still crashing. https://chromium-review.googlesource.com/c/chromium/src/+/2956771 is about to land, though, which should fix it.

### ms...@chromium.org (2022-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-01-26)

Hi, VRP panel here. We are looking at this bug and note that in https://crbug.com/chromium/1280132#c18 it is stated that https://chromium-review.googlesource.com/c/chromium/src/+/3370281 does not fix this bug, but instead the CL https://chromium-review.googlesource.com/c/chromium/src/+/2956771 fixes. However, looking at https://chromium-review.googlesource.com/c/chromium/src/+/2956771 it seems that this is disabling the feature rather than making any code changes.

Can you confirm that this underlying bug is, in fact, fixed? Thanks.

### ms...@chromium.org (2022-01-26)

It finally got fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2956771 , which is about enabling LayoutNGBlockInInline for testing.

The bug showed up in the first place because we enabled another feature for testing - LayoutNGBlockFragmentation. LayoutNGBlockInInline will be enabled for stable before LayoutNGBlockFragmentation is enabled for stable.

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

[Comment Deleted]

### am...@chromium.org (2022-02-04)

Congratulations on another one! The VRP Panel has decided to award you $5,000 for this report. Thank you for your this report and nice work! 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-05-05)

This issue was migrated from crbug.com/chromium/1280132?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/716930]
[Monorail blocking: crbug.com/chromium/829028]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058237)*
