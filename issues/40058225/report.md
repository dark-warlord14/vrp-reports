# Security DCHECK failed: IsA<Derived>(from) in ng_layout_input_node.cc:96 blink::NGLayoutInputNode::TableCellColspan 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058225](https://issues.chromium.org/issues/40058225) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2021-12-14 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4676.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-951304.zip

#Reproduce
1. chrome --js-flags='--expose_gc --allow-natives-syntax' --no-sandbox --enable-blink-test-features --user-data-dir=notexits fuzz-00012.html

What is the expected behavior?

What went wrong?
Type of crash
render tab

#MiniPOC
Come soon

#Analysis
Come soon

#Patch
Not yet

#asan
[17108:11596:1214/053034.931:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from). 
Backtrace:
	base::debug::CollectStackTrace [0x00007FFDDC57B212+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:305)
	base::debug::StackTrace::StackTrace [0x00007FFDDC3A255A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:197)
	logging::LogMessage::~LogMessage [0x00007FFDDC3DAA0C+860] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:587)
	blink::NGLayoutInputNode::TableCellColspan [0x00007FFDE8B41DB9+521] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_layout_input_node.cc:96)
	blink::NGTableBorders::ComputeTableBorders [0x00007FFDE85D4305+4565] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\table\ng_table_borders.cc:147)
	blink::NGTableNode::GetTableBorders [0x00007FFDEA5B7868+680] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\table\ng_table_node.cc:18)
	blink::ComputeBorders [0x00007FFDE7B2F63E+462] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_length_utils.cc:1282)
	blink::CalculateInitialFragmentGeometry [0x00007FFDE7B31FB7+359] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_length_utils.cc:1452)
	blink::NGBlockNode::Layout [0x00007FFDE78A6957+1399] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:435)
	blink::NGBlockLayoutAlgorithm::LayoutNewFormattingContext [0x00007FFDEA448533+3395] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1526)
	blink::NGBlockLayoutAlgorithm::HandleNewFormattingContext [0x00007FFDEA444F65+3477] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1317)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA436BC1+6705] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:694)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA434C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFDE78C79D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFDE78A7617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::`anonymous namespace'::LayoutInflow [0x00007FFDEA4529D7+887] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:121)
	blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFDEA451B96+2070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1652)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA436C7E+6894] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:698)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA434C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFDE78C79D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFDE78A7617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::`anonymous namespace'::LayoutInflow [0x00007FFDEA4529D7+887] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:121)
	blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFDEA451B96+2070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1652)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA436C7E+6894] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:698)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA434C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFDE78C79D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFDE78A7617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::`anonymous namespace'::LayoutInflow [0x00007FFDEA4529D7+887] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:121)
	blink::NGBlockLayoutAlgorithm::HandleInflow [0x00007FFDEA451B96+2070] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:1652)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA436C7E+6894] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:698)
	blink::NGBlockLayoutAlgorithm::Layout [0x00007FFDEA434C8A+378] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_layout_algorithm.cc:441)
	blink::`anonymous namespace'::CreateAlgorithmAndRun<blink::NGBlockLayoutAlgorithm,`lambda at ../../third_party/blink/renderer/core/layout/ng/ng_block_node.cc:206:28'> [0x00007FFDE78C79D5+325] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:117)
	blink::NGBlockNode::Layout [0x00007FFDE78A7617+4663] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\ng_block_node.cc:502)
	blink::LayoutNGMixin<blink::LayoutTableCaption>::UpdateInFlowBlockLayout [0x00007FFDE8479C4F+1071] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_mixin.cc:392)
	blink::LayoutNGBlockFlowMixin<blink::LayoutRubyRun>::UpdateNGBlockLayout [0x00007FFDE7D11645+245] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\layout_ng_block_flow_mixin.cc:241)
	blink::LayoutBlock::UpdateLayout [0x00007FFDE42D0404+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:464)
	blink::LayoutBlockFlow::PositionAndLayoutOnceIfNeeded [0x00007FFDE4425C05+1653] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:837)
	blink::LayoutBlockFlow::LayoutBlockChild [0x00007FFDE4427D5E+1566] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:952)
	blink::LayoutBlockFlow::LayoutBlockChildren [0x00007FFDE44217A1+1953] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:1649)
	blink::LayoutBlockFlow::LayoutChildren [0x00007FFDE441BB10+1248] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:622)
	blink::LayoutBlockFlow::UpdateBlockLayout [0x00007FFDE441A8CF+1183] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block_flow.cc:483)
	blink::LayoutView::UpdateBlockLayout [0x00007FFDE11C250D+2109] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:338)
	blink::LayoutBlock::UpdateLayout [0x00007FFDE42D0404+196] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_block.cc:464)
	blink::LayoutView::UpdateLayout [0x00007FFDE11C2FC4+1780] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_view.cc:379)
	blink::LocalFrameView::PerformLayout [0x00007FFDE105795C+4684] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:837)
	blink::LocalFrameView::UpdateLayout [0x00007FFDE105A5CD+1197] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:898)
	blink::LocalFrameView::UpdateStyleAndLayoutInternal [0x00007FFDE107E29E+1038] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3334)
	blink::LocalFrameView::UpdateStyleAndLayout [0x00007FFDE10630A4+340] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3274)
	blink::Document::UpdateStyleAndLayout [0x00007FFDE1126F71+801] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2477)
	blink::HTMLPlugInElement::LayoutEmbeddedContentForJSBindings [0x00007FFDE43348E9+73] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_plugin_element.cc:487)
	blink::HTMLPlugInElement::PluginWrapper [0x00007FFDE4333BEB+827] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_plugin_element.cc:390)
	blink::V8HTMLObjectElement::NamedPropertyGetterCustom [0x00007FFDEA30B296+1014] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\custom\v8_html_plugin_element_custom.cc:146)
	blink::V8HTMLObjectElement::NamedPropertyGetterCallback [0x00007FFDE77CDD8F+223] (C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_html_object_element.cc:91)
	v8::internal::PropertyCallbackArguments::CallNamedGetter [0x00007FFDD8A243DC+860] (C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:181)
	v8::internal::`anonymous namespace'::GetPropertyWithInterceptorInternal [0x00007FFDD8E97196+1142] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-objects.cc:1140)
	v8::internal::JSObject::GetPropertyWithInterceptor [0x00007FFDD8E96CB7+247] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-objects.cc:5182)
	v8::internal::Object::GetProperty [0x00007FFDD8FAB0FC+444] (C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1159)
	v8::internal::LoadIC::Load [0x00007FFDD89CF494+6724] (C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:510)
	v8::internal::Runtime_LoadNoFeedbackIC_Miss [0x00007FFDD89F6F5A+1066] (C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2593)

Did this work before? N/A 

Chrome version: 100.0.4676.0  Channel: n/a
OS Version: 10.0

## Attachments

- [fuzz-00012.html](attachments/fuzz-00012.html) (text/plain, 241.4 KB)
- [h1.js](attachments/h1.js) (text/plain, 3.7 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 155.7 KB)
- [minipoc.html](attachments/minipoc.html) (text/plain, 235 B)
- [repro.html](attachments/repro.html) (text/plain, 123.9 KB)
- [tc.html](attachments/tc.html) (text/plain, 187 B)
- [tc-evil.html](attachments/tc-evil.html) (text/plain, 294 B)

## Timeline

### [Deleted User] (2021-12-14)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-14)

I suspect this is a dupe of https://crbug.com/chromium/1278988

### m....@gmail.com (2021-12-14)

Hah~ hope it not.
upload minipoc
```
<html>
<meta charset="utf-8">
<title>CHROME MAIN</title>
<script src="testharness.js"></script>
<body onload="start();">

<style>
tr:nth-child(odd){
container-type: size;
}
.cs17 td,th{
column-count: 15;
</body>
</html>
```

### cl...@chromium.org (2021-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4571411513147392.

### cl...@chromium.org (2021-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5152283920498688.

### me...@chromium.org (2021-12-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>Layout]

### me...@chromium.org (2021-12-16)

Like https://crbug.com/chromium/1278988, this bug also needs --enable-blink-test-features, so I suppose it's also Impact=None. Can you please confirm?

### me...@chromium.org (2021-12-20)

These look like type confusion bugs since the very next line casts the object so assigning high severity.

### cl...@chromium.org (2021-12-21)

Detailed Report: https://clusterfuzz.com/testcase?key=5152283920498688

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::NGLayoutInputNode::TableCellColspan
  blink::NGTableBorders::ComputeTableBorders
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=949949:949956

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5152283920498688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### me...@chromium.org (2021-12-21)

+CC mstensho due to https://chromium-review.googlesource.com/c/chromium/src/+/3317340

### ms...@chromium.org (2021-12-22)

Also crashes without LayoutNGBlockFragmentation enabled.

Relevant part of the layout tree:

          LayoutNGTable 0x162c00a03af8 	TABLE id="results"
            LayoutNGTableSection 0x162c00a03c10	THEAD
              LayoutNGTableRow 0x162c00a03d18	TR
*               LayoutTableCell 0x162c00a03e20	TH
                  LayoutMultiColumnFlowThread (anonymous) 0x162c00a03ff0
                    LayoutText 0x162c00a04220	#text "Result"
                  LayoutMultiColumnSet (anonymous) 0x162c00a042c0

We're mixing legacy and NG layout inside a table, which isn't allowed. Legacy fallback is probably triggered by multicol.

The attached file reproduces the crash in a regular build with DCHECKs enabled. All we need to pass is --run-web-tests

### ms...@chromium.org (2021-12-22)

Introduced by https://chromium-review.googlesource.com/c/chromium/src/+/3323072 ([@container] Do not re-attach container inclusive ancestors)

We cannot switch layout engine in the middle of a table. The table container, table section, table row and table cell all need to use the same engine.

### ms...@chromium.org (2021-12-22)

Could we disallow @container for table sections, captions, rows and cells until NG is fully shipped (i.e. when we'll no longer get legacy fallback)?

Note that it's really not necessary to fall back to legacy with tc.html, as long as LayoutNGBlockFragmentation is enabled. There's nothing inside the multicol that NG can't handle (in fact, there's nothing inside at all). But there are other cases where a legacy fallback would be necessary. Attaching another test.

### cl...@chromium.org (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2021-12-27)

Only possible with features only enabled for testing.

### fu...@chromium.org (2022-01-05)

Feature disabled by default.

### fu...@chromium.org (2022-01-05)

mstensho@ This seems to be fixed by this CL: https://chromium-review.googlesource.com/c/chromium/src/+/3367620

Is it a dupe?


### cl...@chromium.org (2022-01-05)

ClusterFuzz testcase 5152283920498688 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=955679:955680

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### m....@gmail.com (2022-01-06)

re https://crbug.com/chromium/1279665#c18
Even if the feature is not enabled by default, it should still be a security issue.
If there is no other reason, please set the type as a security issue, because this also affects VRP, I suggest CC a security team member(like amyressler@chromium.org) to solve it together.

### ms...@chromium.org (2022-01-06)

This just got "fixed" by accident. We get a false negative for DefinitelyNewFormattingContext() on the table cell in ForceLegacyLayoutInFragmentationContext(), and we end up switching the entire table over to legacy. So the problem is gone, as long as we don't interleave style and layout. The guard that was added in https://chromium-review.googlesource.com/c/chromium/src/+/3323072 doesn't work, because that's in ForceLegacyLayoutInFormattingContext(), which doesn't get involved. I think I'll clean up the code a little, so that ForceLegacyLayoutInFragmentationContext() actually will use ForceLegacyLayoutInFormattingContext() for the last leg of the ancestry walk.

PS: Notice the subtle name differences; ForceLegacyLayoutInFragmentationContext vs. ForceLegacyLayoutInFormattingContext. :-/

### ms...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-01-06)

RE https://crbug.com/chromium/1279665#c20 Are you sure that this CL fixes the issue, because the CL version seems to be 949683 and the version I reproduced is 951304.

### ms...@chromium.org (2022-01-06)

The revision number is for https://chromium-review.googlesource.com/c/chromium/src/+/3367620 is #955680.
The fuzzer also bisected to this one, and I've verified it manually as well. But I'm going to file another CL that will make this fuzzer crash reproduce again, because CL:3367620 unintentionally ended up bypassing the fix added by https://chromium-review.googlesource.com/c/chromium/src/+/3323072 . CL:3323072 is what introduced this crasher in the first place, and as long as it hasn't been fixed properly, we need to let it keep on crashing. :)

### ms...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### ms...@chromium.org (2022-01-07)

As expected, this one is back, because of:

https://chromium.googlesource.com/chromium/src/+/d1a79b32e4c96c88b1ef785c8931c1f125ccc807 (Avoid (failed) logic duplication for legacy layout fallback.). See https://crbug.com/chromium/1279665#c26.

### fu...@chromium.org (2022-01-14)

I'm not able to repro this on recent main.


### ms...@chromium.org (2022-01-14)

Turns out that it got fixed by https://chromium-review.googlesource.com/c/chromium/src/+/3370281 - are we safe then? I guess we are, if container queries are always disabled inside multicol (unless HasFullNGFragmentationSupport(), in which case there'll never be any legacy fallback anyway), and container queries are disallowed on table* display types. This seems to be the case?

### fu...@chromium.org (2022-02-02)

Container queries are not disallowed on table display types, but they will always evaluate to 'unknown'. Anyway, we will not interleave style/layout for those cases. Considering this fixed, then.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-02-09)

follow-up: can we change the DCHECK() in casting.h to a hard CHECK()?  If we have the means to determine an incorrect sub-class cast, we should hard stop.

### fu...@chromium.org (2022-02-09)

> follow-up: can we change the DCHECK() in casting.h to a hard CHECK()?  If we have the means to determine an incorrect sub-class cast, we should hard stop.

Not as part of this issue. That would be a much larger topic and should have its own crbug issue.


### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations - the VRP Panel has decided to award you $5,000 for this report! Thanks for your efforts and nice work. 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-05-11)

This issue was migrated from crbug.com/chromium/1279665?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1285151]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058225)*
