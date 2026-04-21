# Security: Security DCHECK failed: !NeedsLayout() || ChildLayoutBlockedByDisplayLock() in blink::LayoutObject::AssertLaidOut

| Field | Value |
|-------|-------|
| **Issue ID** | [40054167](https://issues.chromium.org/issues/40054167) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Layout, Blink>MathML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | rb...@igalia.com |
| **Created** | 2020-12-14 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

**VERSION**  

Chrome Version: 89.0.4350.4 (Developer Build) (64-bit)  

Revision 29c0d89383f97531bef022ee9606d26a194dec6d-refs/branch-heads/4350@{#7}  

Operating System: Linux-4.15.0-112-generic-x86\_64-with-Ubuntu-18.04-bionic

**REPRODUCTION CASE**

Load the following test case with a debug chrome build with the --enable-experimental-web-platform-features flag:

<math>
<mmultiscripts>
<n></n>
<mprescripts></mprescripts>
<mmultiscripts></mmultiscripts>
<mover></mover>
<mprescripts></mprescripts>
</mmultiscripts>
</math>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Backtrace:

[1214/151343.562095:INFO:layout\_object.cc(4798)]  

LayoutView 0x615000007600 #document  

LayoutNGBlockFlow 0x6130000439c0 HTML  

LayoutNGBlockFlow 0x613000043b80 BODY  

LayoutNGMathMLBlock 0x6120000100c0 math  

LayoutNGMathMLBlock 0x612000010240 mmultiscripts  

LayoutNGMathMLBlock 0x6120000103c0 n  

\* LayoutNGMathMLBlock 0x612000010540 mprescripts  

LayoutNGMathMLBlock 0x6120000106c0 mmultiscripts  

LayoutNGMathMLBlock 0x612000010840 mover  

LayoutNGMathMLBlock 0x6120000109c0 mprescripts  

LayoutText 0x60f000009280 #text "\n"  

[1214/151343.562384:FATAL:layout\_object.h(500)] Security DCHECK failed: !NeedsLayout() || ChildLayoutBlockedByDisplayLock().  

#0 0x5568d287ae1b <unknown>  

#1 0x5568df667b09 <unknown>  

#2 0x5568df3b7193 <unknown>  

#3 0x5568df40f387 <unknown>  

#4 0x5568e7b691b4 <unknown>  

#5 0x5568e7b3b687 <unknown>  

#6 0x5568e709e102 <unknown>  

#7 0x5568e709ebf7 <unknown>  

#8 0x5568e709d78e <unknown>  

#9 0x5568e91ba81e <unknown>  

#10 0x5568e70c59a2 <unknown>  

#11 0x5568eb0c2804 <unknown>  

#12 0x5568eb1fa0cd <unknown>  

#13 0x5568eb0835c9 <unknown>  

#14 0x5568eb070acf <unknown>  

#15 0x5568eb06fbdf <unknown>  

#16 0x5568eb07a70a <unknown>  

#17 0x5568eb074d89 <unknown>  

#18 0x5568eb0743f7 <unknown>  

#19 0x5568db82b73e <unknown>  

#20 0x5568db853c5e <unknown>  

#21 0x5568db8551c7 <unknown>  

#22 0x5568db82b73e <unknown>  

#23 0x5568df52b931 <unknown>  

#24 0x5568df5801e1 <unknown>  

#25 0x5568df584548 <unknown>  

#26 0x5568df52b931 <unknown>  

#27 0x5568df58c607 <unknown>  

#28 0x5568df58bd10 <unknown>  

#29 0x5568df42cc24 <unknown>  

#30 0x5568df58e2bd <unknown>  

#31 0x5568df4c7d1b <unknown>  

#32 0x5568f02c02af <unknown>  

#33 0x5568d28eb4ca <unknown>  

#34 0x5568d28eca59 <unknown>  

#35 0x7f913794ebf7 <unknown>  

#36 0x5568d284432a <unknown>  

Task trace:  

#0 0x5568eb108d30 <unknown>  

#1 0x5568eb087d77 <unknown>

# AddressSanitizer:DEADLYSIGNAL

==40080==ERROR: AddressSanitizer: ABRT on unknown address 0x03e900009c90 (pc 0x7f913796bfb7 bp 0x7ffe44cefe50 sp 0x7ffe44cefc00 T0)  

#0 0x7f913796bfb7 in \_\_GI\_raise /build/glibc-S7xCS9/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:51 (discriminator 3)  

#1 0x5568df40fd9a in logging::LogMessage::~LogMessage() base/logging.cc:883  

#2 0x5568e7b691b3 in blink::LayoutObject::AssertLaidOut() const third\_party/blink/renderer/core/layout/layout\_object.h:500  

#3 0x5568e7b3b686 in AssertSubtreeIsLaidOut third\_party/blink/renderer/core/layout/layout\_object.h:509  

#4 0x5568e7b3b686 in UpdateLayout third\_party/blink/renderer/core/frame/local\_frame\_view.cc:995  

#5 0x5568e709e101 in blink::Document::ImplicitClose() third\_party/blink/renderer/core/dom/document.cc:3861  

#6 0x5568e709ebf6 in blink::Document::CheckCompletedInternal() third\_party/blink/renderer/core/dom/document.cc:3937  

#7 0x5568e709d78d in blink::Document::CheckCompleted() third\_party/blink/renderer/core/dom/document.cc:3911  

#8 0x5568e91ba81d in blink::FrameLoader::FinishedParsing() third\_party/blink/renderer/core/loader/frame\_loader.cc:387  

#9 0x5568e70c59a1 in blink::Document::FinishedParsing() third\_party/blink/renderer/core/dom/document.cc:6993  

#10 0x5568eb0c2803 in blink::HTMLConstructionSite::FinishedParsing() third\_party/blink/renderer/core/html/parser/html\_construction\_site.cc:631  

#11 0x5568eb1fa0cc in blink::HTMLTreeBuilder::Finished() third\_party/blink/renderer/core/html/parser/html\_tree\_builder.cc:2958  

#12 0x5568eb0835c8 in blink::HTMLDocumentParser::end() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1289  

#13 0x5568eb070ace in blink::HTMLDocumentParser::AttemptToRunDeferredScriptsAndEnd() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:1304  

#14 0x5568eb06fbde in blink::HTMLDocumentParser::PrepareToStopParsing() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:516  

#15 0x5568eb07a709 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::\_\_1::unique\_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::\_\_1::default\_delete[blink::HTMLDocumentParser::TokenizedChunk](javascript:void(0);) >, bool\*) third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:861  

#16 0x5568eb074d88 in blink::HTMLDocumentParser::PumpPendingSpeculations() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:911  

#17 0x5568eb0743f6 in blink::HTMLDocumentParser::ResumeParsingAfterYield() third\_party/blink/renderer/core/html/parser/html\_document\_parser.cc:597  

#18 0x5568db82b73d in Run base/callback.h:101  

#19 0x5568db82b73d in RunInternal third\_party/blink/renderer/platform/wtf/functional.h:256  

#20 0x5568db82b73d in Run third\_party/blink/renderer/platform/wtf/functional.h:241  

#21 0x5568db853c5d in Run base/callback.h:101  

#22 0x5568db853c5d in Run third\_party/blink/renderer/platform/scheduler/common/post\_cancellable\_task.cc:47  

#23 0x5568db8551c6 in Invoke<void (blink::TaskHandle::Runner::\*)(const blink::TaskHandle &), base::WeakPtr[blink::TaskHandle::Runner](javascript:void(0);), blink::TaskHandle> base/bind\_internal.h:498  

#24 0x5568db8551c6 in MakeItSo<void (blink::TaskHandle::Runner::\*)(const blink::TaskHandle &), base::WeakPtr[blink::TaskHandle::Runner](javascript:void(0);), blink::TaskHandle> base/bind\_internal.h:657  

#25 0x5568db8551c6 in RunImpl<void (blink::TaskHandle::Runner::\*)(const blink::TaskHandle &), std::tuple<base::WeakPtr[blink::TaskHandle::Runner](javascript:void(0);), blink::TaskHandle>, 0, 1> base/bind\_internal.h:710  

#26 0x5568db8551c6 in RunOnce base/bind\_internal.h:679  

#27 0x5568db82b73d in Run base/callback.h:101  

#28 0x5568db82b73d in RunInternal third\_party/blink/renderer/platform/wtf/functional.h:256  

#29 0x5568db82b73d in Run third\_party/blink/renderer/platform/wtf/functional.h:241  

#30 0x5568df52b930 in Run base/callback.h:101  

#31 0x5568df52b930 in RunTask base/task/common/task\_annotator.cc:163  

#32 0x5568df5801e0 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:199  

#33 0x5568df584547 in Invoke<void (base::sequence\_manager::internal::ThreadControllerImpl::\*)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) &, const base::sequence\_manager::internal::ThreadControllerImpl::WorkType &> base/bind\_internal.h:498  

#34 0x5568df584547 in MakeItSo<void (base::sequence\_manager::internal::ThreadControllerImpl::\*const &)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);) &, const base::sequence\_manager::internal::ThreadControllerImpl::WorkType &> base/bind\_internal.h:657  

#35 0x5568df584547 in RunImpl<void (base::sequence\_manager::internal::ThreadControllerImpl::\*const &)(base::sequence\_manager::internal::ThreadControllerImpl::WorkType), const std::tuple<base::WeakPtr[base::sequence\_manager::internal::ThreadControllerImpl](javascript:void(0);), base::sequence\_manager::internal::ThreadControllerImpl::WorkType> &, 0, 1> base/bind\_internal.h:710  

#36 0x5568df584547 in Run base/bind\_internal.h:692  

#37 0x5568df52b930 in Run base/callback.h:101  

#38 0x5568df52b930 in RunTask base/task/common/task\_annotator.cc:163  

#39 0x5568df58c606 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351  

#40 0x5568df58bd0f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:264  

#41 0x5568df42cc23 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39  

#42 0x5568df58e2bc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:460  

#43 0x5568df4c7d1a in base::RunLoop::Run() base/run\_loop.cc:131  

#44 0x5568f02c02ae in content::RenderViewTest::LoadHTMLWithUrlOverride(char const\*, char const\*) content/public/test/render\_view\_test.cc:381  

#45 0x5568d28eb4c9 in LoadHTML content/test/fuzzer/fuzzer\_support.h:27  

#46 0x5568d28eb4c9 in LLVMFuzzerTestOneInput content/test/fuzzer/renderer\_fuzzer.cc:22  

#47 0x5568d28eca58 in main testing/libfuzzer/unittest\_main.cc:57  

#48 0x7f913794ebf6 in \_\_libc\_start\_main /build/glibc-S7xCS9/glibc-2.27/csu/../csu/libc-start.c:310

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: ABRT /build/glibc-S7xCS9/glibc-2.27/signal/../sysdeps/unix/sysv/linux/raise.c:51 (discriminator 3) in \_\_GI\_raise  

==40080==ABORTING  

Aborted (core dumped)

**CREDIT INFORMATION**  

Reporter credit: Renata Hodovan  

This issue was found by the Grammarinator fuzzer.

## Attachments

- [test.html](attachments/test.html) (text/plain, 208 B)

## Timeline

### [Deleted User] (2020-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6260575742263296.

### do...@chromium.org (2020-12-15)

+some layout folks. ClusterFuzz doesn't appear to have any ASAN + dchecks builds so it didn't repro this, but would you be able to investigate?

[Monorail components: Blink>Layout]

### ms...@chromium.org (2020-12-15)

Reproducible locally with --enable-blink-features=MathMLCore or --enable-experimental-web-platform-features.

### [Deleted User] (2020-12-15)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fw...@igalia.com (2020-12-15)

Rob is in holidays so I'll take a look tomorrow.

### fw...@igalia.com (2020-12-15)

Just reading the DOM vs Layout trees of the report, it seems there is a mismatch for the first mprescripts, in the former it's a direct child of mmultiscripts and in the latter case it's not. This might confuse the mmultiscripts algo.

### ms...@chromium.org (2020-12-15)

Removing ReleaseBlock. MathML isn't enabled by default.

### dg...@chromium.org (2020-12-15)

[Empty comment from Monorail migration]

### fw...@igalia.com (2020-12-16)

> Just reading the DOM vs Layout trees of the report, it seems there is a mismatch for the first mprescripts, in the former it's a direct child of mmultiscripts and in the latter case it's not. This might confuse the mmultiscripts algo.

OK I stand corrected I was confused by the indentation. The issue is just that IsValidMultiscript() accepts two mprescripts while the layout algo assumes only 1 ; contrary to what is defined in the spec https://mathml-refresh.github.io/mathml-core/#prescripts-and-tensor-indices-mmultiscripts ; I will upload a patch.

### [Deleted User] (2020-12-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### fw...@igalia.com (2020-12-17)

> This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

Patch uploaded: https://chromium-review.googlesource.com/c/chromium/src/+/2593643

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ef8fbdd7bef05ffb52961c2a17b45145c2fb7a13

commit ef8fbdd7bef05ffb52961c2a17b45145c2fb7a13
Author: Frédéric Wang <fwang@igalia.com>
Date: Thu Dec 17 09:16:43 2020

Treat mmultiscripts with two <mprescripts> children as invalid

Per [1], mmultiscripts can only have one in-flow <mprescripts/> child so
this CL fixes IsValidMultiscript() to align with the specification.
It also makes similar adjustment for the corresponding fatal checks in
NGMathScriptsLayoutAlgorithm::GatherChildren (rather than just checking
the index of a previous <mprescripts> is nonzero, which does not work if
there is no post-scripts). This fixes an assertion about node not being
laid out due to the fact that the mmultiscripts algorithm only performs
layout of at most one <mprescript>.

[1] https://mathml-refresh.github.io/mathml-core/#prescripts-and-tensor-indices-mmultiscripts

Bug: 1158375, 6606
Change-Id: I26964b2ef287585392db7f1854251b4b21075aef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593643
Commit-Queue: Frédéric Wang <fwang@igalia.com>
Reviewed-by: Morten Stenshorne <mstensho@chromium.org>
Cr-Commit-Position: refs/heads/master@{#837987}

[add] https://crrev.com/ef8fbdd7bef05ffb52961c2a17b45145c2fb7a13/third_party/blink/web_tests/external/wpt/mathml/crashtests/mmultiscripts-with-two-prescripts.html
[modify] https://crrev.com/ef8fbdd7bef05ffb52961c2a17b45145c2fb7a13/third_party/blink/renderer/core/layout/ng/mathml/ng_math_scripts_layout_algorithm.cc
[modify] https://crrev.com/ef8fbdd7bef05ffb52961c2a17b45145c2fb7a13/third_party/blink/renderer/core/layout/ng/mathml/ng_math_layout_utils.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### fw...@igalia.com (2022-06-09)

This is fixed.

[Monorail components: Blink>MathML]

### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-27)

AFAICT, this looks like a fix for the failed security DCHECK and is still a medium severity issue, as MathML is not enabled by default, it should have still be labeled as a medium severity security bug, but with Security_Impact-None, I have updated this issue accordingly, please feel free to correct if any of my assertions are wrong. 

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your effort and reporting this issue to us! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1158375?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Layout, Blink>MathML]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054167)*
