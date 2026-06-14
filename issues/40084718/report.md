# Security: UAF with namespace nodes in XPointer ranges

| Field | Value |
|-------|-------|
| **Issue ID** | [40084718](https://issues.chromium.org/issues/40084718) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2016-4658 |
| **Reporter** | we...@aevum.de |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-06-28 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

XPointer ranges fail to copy namespace nodes, resulting in use-after-free errors.

**VERSION**  

Chrome Version: 51.0.2704.106 stable  

Operating System: Windows 10, 64-bit

**REPRODUCTION CASE**  

See the attached files xpointer-ns-uaf.xml and xpointer-ns-uaf.xsl. If you open the XML file locally, make sure to run Chrome with --allow-file-access-from-files.

FULL DETAILS  

The XPath implementation of libxml2 handles namespace nodes differently than other nodes. Since they're not part of the XML parse tree, they are copied between node sets. The XPointer implementation fails to make a copy of namespace nodes when creating range objects, resulting in use-after-free errors.

Memory errors involving xmlNode structs and xmlNs pseudo-nodes are hard to exploit since most code in libxml2 first checks the node type which can't be manipulated easily. I can't think of an obvious way to leverage this bug.

The example that triggers the bug uses the XSLT "document" function to trigger the evaluation of an XPointer expression. Other mechanisms could be probably used as well.

A patch against libxml2 master is attached. The patch simply disallows namespace nodes in XPointer ranges.

From what I can tell, the XPointer implementation in libxml2 is incomplete and looks rather buggy. It might be a good idea to disable XPointer support completely in xmlconfig.h.

DISCLOSURE  

I contribute to libxml2 occasionally. I haven't shared details about this issue with anyone, and I don't plan to do so until it is fixed in Webkit browsers. I didn't write any parts of the buggy code. This bug was found with afl-fuzz and ASan.

## Attachments

- [xpointer-ns-uaf.xml](attachments/xpointer-ns-uaf.xml) (text/plain, 69 B)
- [xpointer-ns-uaf.xsl](attachments/xpointer-ns-uaf.xsl) (text/plain, 213 B)
- [xpointer-ns-uaf.diff](attachments/xpointer-ns-uaf.diff) (application/octet-stream, 6.9 KB)

## Timeline

### cl...@chromium.org (2016-06-28)

[Comment Deleted]

### cl...@chromium.org (2016-06-28)

[Comment Deleted]

### pa...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5631727754280960

### pa...@chromium.org (2016-06-28)

Thank you for this report, and for the patch! I suggest that if you have a confidential way to contact the libxml2 project (and it sounds like you might), that you also report this to them so that they can integrate the patch ASAP. Doing so will not jeopardize your chances of getting a Chromium vulnerability reward — our bias is toward getting the bug fixed, and our rewards program should incentivize that first of all. :)

### pa...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>XML]

### pa...@chromium.org (2016-06-30)

scottmg, you're the only person in both third_party/libxslt/OWNERS and third_party/libxml/OWNERS, so here's a present for you. :) Looks like we should get the patch integrated in upstream, and then pull the latest stable from upstream (and carry the patch locally until then).

Hmm, ClusterFuzz says it can't repro the bug, yet does produce this stack trace (with ASan):

=================================================================
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b0002731e8 at pc 0x7f391ae2e00e bp 0x7ffefc5fffd0 sp 0x7ffefc5fffc8
READ of size 4 at 0x60b0002731e8 thread T0 (chrome)
SCARINESS: 45 (4-byte-read-heap-use-after-free)
    #0 0x7f391ae2e00d in xmlXPtrCoveringRange third_party/libxml/src/xpointer.c:1996:21
    #1 0x7f391ae2e00d in xmlXPtrRangeFunction third_party/libxml/src/xpointer.c:2078
    #2 0x7f391ae0c0d3 in xmlXPathCompOpEval third_party/libxml/src/xpath.c:13597:17
    #3 0x7f391ae0625f in xmlXPathCompOpEval third_party/libxml/src/xpath.c:13988:26
    #4 0x7f391ade944a in xmlXPathRunEval third_party/libxml/src/xpath.c:14563:2
    #5 0x7f391ae34b6b in xmlXPtrEvalXPtrPart third_party/libxml/src/xpointer.c:1040:2
    #6 0x7f391ae34b6b in xmlXPtrEvalFullXPtr third_party/libxml/src/xpointer.c:1149
    #7 0x7f391ae34b6b in xmlXPtrEvalXPointer third_party/libxml/src/xpointer.c:1278
    #8 0x7f391ae34b6b in xmlXPtrEval third_party/libxml/src/xpointer.c:1381
    #9 0x7f392c35395b in xsltDocumentFunctionLoadDocument third_party/libxslt/libxslt/functions.c:180:14
    #10 0x7f392c35395b in xsltDocumentFunction third_party/libxslt/libxslt/functions.c:342
    #11 0x7f391ae0c0d3 in xmlXPathCompOpEval third_party/libxml/src/xpath.c:13597:17
    #12 0x7f391ae0625f in xmlXPathCompOpEval third_party/libxml/src/xpath.c:13988:26
    #13 0x7f391ade944a in xmlXPathRunEval third_party/libxml/src/xpath.c:14563:2
    #14 0x7f391ade7dcb in xmlXPathCompiledEvalInternal third_party/libxml/src/xpath.c:14930:11
    #15 0x7f391ade7a71 in xmlXPathCompiledEval third_party/libxml/src/xpath.c:14993:5
    #16 0x7f392c31d780 in xsltPreCompEval third_party/libxslt/libxslt/transform.c:379:11
    #17 0x7f392c31d780 in xsltValueOf third_party/libxslt/libxslt/transform.c:4563
    #18 0x7f392c311f17 in xsltApplySequenceConstructor third_party/libxslt/libxslt/transform.c:2755:17
    #19 0x7f392c30ff0b in xsltApplyXSLTTemplate third_party/libxslt/libxslt/transform.c:3216:5
    #20 0x7f392c30dcb5 in xsltProcessOneNode third_party/libxslt/libxslt/transform.c:2184:2
    #21 0x7f392c324a24 in xsltApplyStylesheetInternal third_party/libxslt/libxslt/transform.c:6054:5
    #22 0x7f39212d1dd4 in blink::XSLTProcessor::transformToString(blink::Node*, WTF::String&, WTF::String&, WTF::String&) third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:338:31
    #23 0x7f392129bd6d in blink::DocumentXSLT::applyXSLTransform(blink::Document&, blink::ProcessingInstruction*) third_party/WebKit/Source/core/xml/DocumentXSLT.cpp:109:21
    #24 0x7f392129cc14 in blink::DocumentXSLT::sheetLoaded(blink::Document&, blink::ProcessingInstruction*) third_party/WebKit/Source/core/xml/DocumentXSLT.cpp:173:13
    #25 0x7f391fa7ffa2 in blink::ProcessingInstruction::sheetLoaded() third_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:186:14
    #26 0x7f391fa81666 in blink::ProcessingInstruction::setXSLStyleSheet(WTF::String const&, blink::KURL const&, WTF::String const&) third_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:228:5
    #27 0x7f3920b1fecd in blink::XSLStyleSheetResource::checkNotify() third_party/WebKit/Source/core/fetch/XSLStyleSheetResource.cpp:90:12
    #28 0x7f3920acd7fe in blink::Resource::finish(double) third_party/WebKit/Source/core/fetch/Resource.cpp:434:5
    #29 0x7f3920af99f8 in blink::ResourceFetcher::didFinishLoading(blink::Resource*, double, long, blink::ResourceFetcher::DidFinishLoadingReason) third_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:926:19
    #30 0x7f392cff5717 in content::WebURLLoaderImpl::Context::OnCompletedRequest(int, bool, bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, base::TimeTicks const&, long) content/child/web_url_loader_impl.cc:764:16
    #31 0x7f392cf86329 in content::ResourceDispatcher::OnRequestComplete(int, content::ResourceRequestCompletionStatus const&) content/child/resource_dispatcher.cc:379:9
    #32 0x7f392cf8c9fc in DispatchToMethodImpl<content::ResourceDispatcher *, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), int, content::ResourceRequestCompletionStatus, 0, 1> base/tuple.h:126:3
    #33 0x7f392cf8c9fc in DispatchToMethod<content::ResourceDispatcher *, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), int, content::ResourceRequestCompletionStatus> base/tuple.h:133
    #34 0x7f392cf8c9fc in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), void, std::__1::tuple<int, content::ResourceRequestCompletionStatus> > ipc/ipc_message_templates.h:26
    #35 0x7f392cf8c9fc in bool IPC::MessageT<ResourceMsg_RequestComplete_Meta, std::__1::tuple<int, content::ResourceRequestCompletionStatus>, void>::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void, void (content::ResourceDispatcher::*)(int, content::ResourceRequestCompletionStatus const&)>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void*, void (content::ResourceDispatcher::*)(int, content::ResourceRequestCompletionStatus const&)) ipc/ipc_message_templates.h:121
    #36 0x7f392cf7dcb7 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) content/child/resource_dispatcher.cc:510:5
    #37 0x7f392cf7c45d in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) content/child/resource_dispatcher.cc:126:3
    #38 0x7f392d071017 in Run<std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > base/bind_internal.h:160:12
    #39 0x7f392d071017 in MakeItSo<base::internal::RunnableAdapter<void (*)(std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> >)> &, std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > base/bind_internal.h:312
    #40 0x7f392d071017 in base::internal::Invoker<base::IndexSequence<0ul>, base::internal::BindState<base::internal::RunnableAdapter<void (*)(std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> >)>, void (std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> >), base::internal::PassedWrapper<std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > >, false, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:364
    #41 0x7f3918704fc1 in Run base/callback.h:397:12
    #42 0x7f3918704fc1 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51
    #43 0x7f392d08c6bc in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(scheduler::internal::WorkQueue*, scheduler::internal::TaskQueueImpl::Task*) components/scheduler/base/task_queue_manager.cc:289:19
    #44 0x7f392d0883cc in scheduler::TaskQueueManager::DoWork(base::TimeTicks, bool) components/scheduler/base/task_queue_manager.cc:201:13
    #45 0x7f392d08ebe7 in Run<scheduler::TaskQueueManager *, const base::TimeTicks &, const bool &> base/bind_internal.h:187:12
    #46 0x7f392d08ebe7 in MakeItSo<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(base::TimeTicks, bool)> &, base::WeakPtr<scheduler::TaskQueueManager>, const base::TimeTicks &, const bool &> base/bind_internal.h:325
    #47 0x7f392d08ebe7 in base::internal::Invoker<base::IndexSequence<0ul, 1ul, 2ul>, base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::*)(base::TimeTicks, bool)>, void (scheduler::TaskQueueManager*, base::TimeTicks, bool), base::WeakPtr<scheduler::TaskQueueManager>, base::TimeTicks, bool>, true, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:364
    #48 0x7f3918704fc1 in Run base/callback.h:397:12
    #49 0x7f3918704fc1 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:51
    #50 0x7f3918587015 in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:475:19
    #51 0x7f3918587e3f in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop/message_loop.cc:484:5
    #52 0x7f391858929c in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:601:13
    #53 0x7f39185937ad in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:33:31
    #54 0x7f39185f6939 in base::RunLoop::Run() base/run_loop.cc:35:10
    #55 0x7f3918584748 in base::MessageLoop::Run() base/message_loop/message_loop.cc:294:12
    #56 0x7f3926d028c1 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:199:37
    #57 0x7f391842c787 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:345:14
    #58 0x7f3918430ed5 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:787:12
    #59 0x7f391842b50d in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:20:28
    #60 0x7f3917359ee3 in ChromeMain chrome/app/chrome_main.cc:84:12
    #61 0x7f390c7a2f44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287

### sc...@chromium.org (2016-06-30)

I have graciously bequeathed this horrible mess to Dominic. But if he's out I might be able to look into it.

### sh...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-07-05)

I have looked over this patch and put it up for review here: https://codereview.chromium.org/2121073002

With the next roll I will try disabling XPointer. Unfortunately our traditional ways to determine use for XML on the web may not be effective; the use counter for XSLT is already an order of magnitude below where we'd remove a feature.

I have filed a blank upstream bug: https://bugzilla.gnome.org/show_bug.cgi?id=768423

### mm...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

### dd...@apple.com (2016-07-11)

> ddkilzer, per wellnhofer's point about disclosure, could you indicate when WebKit picks this up so we can push the repro and patches into the upstream bug tracker?

This change will ship with the major OS releases (macOS 10.12 Sierra, iOS 10, tvOS 10, watchOS 3) as we don't have another software update release available, and we don't ship libxml2 outside each OS.

See also https://crbug.com/chromium/623378, https://crbug.com/chromium/624011#c13.



### dd...@apple.com (2016-07-11)

> With the next roll I will try disabling XPointer. Unfortunately our traditional ways to determine use for XML on the web may not be effective; the use counter for XSLT is already an order of magnitude below where we'd remove a feature.

Nick, do you plan to fix XPointer to allow namespace nodes to be copied (to restore this functionality) after the security patch lands?


### we...@aevum.de (2016-07-12)

ddkilzer, namespace nodes in XPointer ranges were always broken, so my patch doesn't remove any functionality. I have no plans to make non-security fixes to libxml2's XPointer implementation.

### do...@chromium.org (2016-07-15)

FWIW I plan to disable XPointer with the next libxml/xslt roll. I'll CC you if we learn that breaks sites. I'm curious, does the libxml/xslt WebKit picks up from the system on OS X/iOS have XPointer enabled?

### dd...@apple.com (2016-07-15)

> I'm curious, does the libxml/xslt WebKit picks up from the system on OS X/iOS have XPointer enabled?

Yes, XPointer is enabled on libxml2 that ships with iOS and macOS.  However, I'm pretty sure you have to enable it at runtime as well (via the 'XML_WITH_XPTR' xmlFeature enum in <libxml/parser.h>).

Loading Nick's test case in Safari and Chrome shows that XPointer isn't enabled for the web:

error on line 1 at column 1: Extra content at the end of the document


### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6eee7eee18990d52a5e0723058f0e4d186e1e278

commit 6eee7eee18990d52a5e0723058f0e4d186e1e278
Author: dominicc <dominicc@chromium.org>
Date: Thu Jul 28 03:45:44 2016

Add a helper function for allocating XPointer ranges.

BUG=624011

Review-Url: https://codereview.chromium.org/2121073002
Cr-Commit-Position: refs/heads/master@{#408330}

[modify] https://crrev.com/6eee7eee18990d52a5e0723058f0e4d186e1e278/third_party/libxml/README.chromium
[modify] https://crrev.com/6eee7eee18990d52a5e0723058f0e4d186e1e278/third_party/libxml/src/xpointer.c


### we...@aevum.de (2016-08-05)

If nobody objects, I'll post the details of this bug to the protected entry in the libxml2 bug tracker in the next days and add a couple of CCs.

### dd...@apple.com (2016-08-05)

> If nobody objects, I'll post the details of this bug to the protected entry in the libxml2 bug tracker in the next days and add a couple of CCs.

Are you planning to use this one?  <https://bugzilla.gnome.org/show_bug.cgi?id=768423>

Seems fine.  Would be good to keep the upstream bug and this bug private until all affected parties can ship the fix.

Apple's fix will go out with macOS 10.12 Sierra, iOS 10, watchOS 3 and tvOS 10 (and an iTunes update for Windows).  I don't have specific dates for these, but it's fine to open this up when the first one or more of those ships to all customers, probably in September.


### in...@chromium.org (2016-08-25)

Is the security issue gone with c#17, if yes, please mark as Fixed.

### sh...@chromium.org (2016-08-28)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### we...@aevum.de (2016-08-29)

I just copied the details to the libxml2 bug tracker (private URL): https://bugzilla.gnome.org/show_bug.cgi?id=768423

@ddkilzer, there's no runtime switch for XPointer support so this should affect Safari as well.

### dd...@apple.com (2016-09-02)

Apple is planning to use CVE-2016-4658 for this issue.


### do...@chromium.org (2016-09-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-04)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-09-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-09)

[Automated comment] Commit may have occurred before M54 branch point (8/25/2016), needs manual review.

### bu...@google.com (2016-09-13)

Based on the commit date this should already be in M54.  I think this got merge-requested by sheriffbot since the issue itself wasn't resolved until 9/3.

I checked out the 2840 branch and verified this change is present.  Removing the merge request labels.

### we...@aevum.de (2016-10-12)

This is now fixed upstream: https://git.gnome.org/browse/libxml2/commit/?id=c1d1f7121194036608bf555f08d3062a36fd344b

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Nice, $3,500 for this report!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/624011?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084718)*
