# Security:  Access to freed stack memory in blink::PerformanceMonitor::Did() 

| Field | Value |
|-------|-------|
| **Issue ID** | [40088656](https://issues.chromium.org/issues/40088656) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input, Platform>DevTools>Performance |
| **Platforms** | Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2017-08-10 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

	There is a stack buffer overflow in blink::PerformanceMonitor::Did() when browsing a specially crafted web page while Developer tools is open.
	
	Steps to reproduce:
	
	1. Open Developer tools.
	2. Open StackBOF_PerformanceMonitorDid_Repro.htmlin Chrome browser ASAN build.
	3. ASAN reports a stack buffer overflow in blink::PerformanceMonitor::Did().



VERSION
	Chrome Version: Chromium	62.0.3181.0 (Developer Build) (32-bit) 
	( https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release%2Fasan-win32-release-493054.zip?generation=1502311633835318&alt=media )
	Operating System: Windows 10 

REPRODUCTION CASE 
	StackBOF_PerformanceMonitorDid_Repro.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: 

	=================================================================
	==17992==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x00b5a2fc at pc 0x161bb90f bp 0x00b5853c sp 0x00b58530
	READ of size 1 at 0x00b5a2fc thread T0

		#0 0x161bb90e in blink::PerformanceMonitor::Did C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\frame\PerformanceMonitor.cpp:192
		#1 0x16d45ffb in blink::probe::CallFunction::~CallFunction C:\b\c\b\win_asan_release\src\out\release\gen\blink\core\CoreProbesImpl.cpp:1214
		#2 0x19b26952 in blink::V8ScriptRunner::CallFunction C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\bindings\core\v8\V8ScriptRunner.cpp:698
		#3 0x19be6bf9 in blink::V8EventListener::CallListenerFunction C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\bindings\core\v8\V8EventListener.cpp:115
		#4 0x19bd113e in blink::V8AbstractEventListener::InvokeEventHandler C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\bindings\core\v8\V8AbstractEventListener.cpp:146
		#5 0x19bd0c52 in blink::V8AbstractEventListener::HandleEvent C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\bindings\core\v8\V8AbstractEventListener.cpp:104
		#6 0x19bd08e1 in blink::V8AbstractEventListener::handleEvent C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\bindings\core\v8\V8AbstractEventListener.cpp:92
		#7 0x1612d0c0 in blink::EventTarget::FireEventListeners C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\EventTarget.cpp:770
		#8 0x1612ba72 in blink::EventTarget::FireEventListeners C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\EventTarget.cpp:631
		#9 0x1ab29215 in blink::Node::HandleLocalEvents C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\Node.cpp:2179
		#10 0x1611fac7 in blink::NodeEventContext::HandleLocalEvents C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\NodeEventContext.cpp:63
		#11 0x161233d0 in blink::EventDispatcher::Dispatch C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\EventDispatcher.cpp:182
		#12 0x1611f23c in blink::EventDispatchMediator::DispatchEvent C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\EventDispatchMediator.cpp:51
		#13 0x1612132e in blink::EventDispatcher::DispatchEvent C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\EventDispatcher.cpp:59
		#14 0x1612fece in blink::ScopedEventQueue::EnqueueEventDispatchMediator C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\ScopedEventQueue.cpp:60
		#15 0x161215b6 in blink::EventDispatcher::DispatchScopedEvent C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\events\EventDispatcher.cpp:75
		#16 0x1ab293ef in blink::Node::DispatchScopedEvent C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\Node.cpp:2184
		#17 0x1a9ea744 in blink::DispatchChildRemovalEvents C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\ContainerNode.cpp:1416
		#18 0x1a9ea0cd in blink::ContainerNode::WillRemoveChild C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\ContainerNode.cpp:589
		#19 0x1a9e9713 in blink::ContainerNode::RemoveChild C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\ContainerNode.cpp:662
		#20 0x1a9e862e in blink::ContainerNode::ReplaceChild C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\ContainerNode.cpp:550
		#21 0x1ae27bd8 in blink::ReplaceChildrenWithFragment C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\editing\serializers\Serialization.cpp:701
		#22 0x1aad1f13 in blink::Element::setInnerHTML C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\Element.cpp:2990
		#23 0x19dbe78d in blink::V8Element::innerHTMLAttributeSetterCallback C:\b\c\b\Win_ASan_Release\src\out\Release\gen\blink\bindings\core\v8\V8Element.cpp:2178
		#24 0x1055680d in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments.cc:25
		#25 0x107b25b7 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:112
		#26 0x107afe25 in v8::internal::Builtins::InvokeApiFunction C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:219
		#27 0x1175a710 in v8::internal::Object::SetPropertyWithAccessor C:\b\c\b\win_asan_release\src\v8\src\objects.cc:1618
		#28 0x11796b3a in v8::internal::Object::SetPropertyInternal C:\b\c\b\win_asan_release\src\v8\src\objects.cc:4733
		#29 0x117962db in v8::internal::Object::SetProperty C:\b\c\b\win_asan_release\src\v8\src\objects.cc:4765
		#30 0x114fbacf in v8::internal::StoreIC::Store C:\b\c\b\win_asan_release\src\v8\src\ic\ic.cc:1653
		#31 0x11513cb2 in v8::internal::Runtime_StoreIC_Miss C:\b\c\b\win_asan_release\src\v8\src\ic\ic.cc:2484

	Address 0x00b5a2fc is located in stack of thread T0 at offset 380 in frame
		#0 0x1a9e805d in blink::ContainerNode::ReplaceChild C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\dom\ContainerNode.cpp:497

	  This frame has 7 object(s):
		[16, 192) 'ref.tmp.i190'
		[256, 260) 'child.i'
		[272, 276) 'ref.tmp.i' (line 142)
		[288, 344) 'targets' (line 535)
		[384, 440) 'post_insertion_notification_targets' (line 536) <== Memory access at offset 380 underflows this variable
		[480, 481) 'ref.tmp' (line 572)
		[496, 497) 'ref.tmp59' (line 575)
	HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
		  (longjmp, SEH and C++ exceptions *are* supported)
	SUMMARY: AddressSanitizer: stack-buffer-overflow C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\core\frame\PerformanceMonitor.cpp:192 in blink::PerformanceMonitor::Did
	Shadow bytes around the buggy address:
	  0x3016b400: f8 f3 f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00
	  0x3016b410: 00 00 00 00 f1 f1 f8 f2 f8 f8 f8 f3 f3 f3 f3 f3
	  0x3016b420: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
	  0x3016b430: f1 f1 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8
	  0x3016b440: f8 f8 f8 f8 f8 f8 f8 f8 f2 f2 f2 f2 f2 f2 f2 f2
	=>0x3016b450: f8 f2 f8 f2 00 00 00 00 00 00 00 f2 f2 f2 f2[f2]
	  0x3016b460: 00 00 00 00 00 00 00 f2 f2 f2 f2 f2 f8 f2 f8 f3
	  0x3016b470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
	  0x3016b480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
	  0x3016b490: f1 f1 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8 f8
	  0x3016b4a0: f8 f8 f8 f8 f8 f8 f8 f8 f3 f3 f3 f3 f3 f3 f3 f3
	Shadow byte legend (one shadow byte represents 8 application bytes):
	  Addressable:           00
	  Partially addressable: 01 02 03 04 05 06 07 
	  Heap left redzone:       fa
	  Freed heap region:       fd
	  Stack left redzone:      f1
	  Stack mid redzone:       f2
	  Stack right redzone:     f3
	  Stack after return:      f5
	  Stack use after scope:   f8
	  Global redzone:          f9
	  Global init order:       f6
	  Poisoned by user:        f7
	  Container overflow:      fc
	  Array cookie:            ac
	  Intra object redzone:    bb
	  ASan internal:           fe
	  Left alloca redzone:     ca
	  Right alloca redzone:    cb
	==17992==ABORTING


## Attachments

- [StackBOF_PerformanceMonitorDid_Repro.html](attachments/StackBOF_PerformanceMonitorDid_Repro.html) (text/plain, 1.8 KB)

## Timeline

### cl...@chromium.org (2017-08-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5433426286215168.

### cl...@chromium.org (2017-08-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4522729775824896.

### ts...@chromium.org (2017-08-10)

Seems unlikely that CF will be able to hit this because of the gestures involved.

### ts...@chromium.org (2017-08-10)

Sev medium due to one-byte wild read + devtools requirement.

### ts...@chromium.org (2017-08-10)

I'm not sure how far back this goes.  Pinged CF folks about adding gestures.

tkent, you've performed some work in ContainerNode in the recent past, perhaps you could have a look or re-assign as appropriate?  Thanks.

### ts...@chromium.org (2017-08-10)

+pfeldman for the devtools aspect, though my guess is that the suspicious value is coming from below.

### ts...@chromium.org (2017-08-10)

[Empty comment from Monorail migration]

[Monorail components: Blink Platform>DevTools>Performance]

### ke...@chromium.org (2017-08-10)

re #5: The Clusterfuzz jobs had the --auto-open-devtools-for-tabs command line flag set, but apparently that doesn't succeed in making it repro.

### sh...@chromium.org (2017-08-11)

[Empty comment from Monorail migration]

### ea...@chromium.org (2017-08-14)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>Input]

### tk...@chromium.org (2017-08-16)

It looks an issue of PerformanceMonitor class.  DevTools team should handle this.


### pf...@chromium.org (2017-08-17)

[Empty comment from Monorail migration]

### al...@chromium.org (2017-08-17)

[Empty comment from Monorail migration]

### al...@chromium.org (2017-08-17)

[Comment Deleted]

### al...@chromium.org (2017-08-17)

The problem is that Document::Shutdown() is called between Will and Did for probe::UserCallback. As soon as document loses its frame it cannot provide CoreProbeSink anymore, so 'Did' signal is not dispatched to the probe observers.

PerformanceMonitor does not expect unpaired Will & Did and crashes.

### bu...@chromium.org (2017-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f3270e31783e826b59086622789f6c3613f3792

commit 8f3270e31783e826b59086622789f6c3613f3792
Author: Alexei Filippov <alph@chromium.org>
Date: Fri Aug 18 00:12:20 2017

[instrumentation] Make sure the probe sink is still available when Did callbacks are invoked.

The patch makes it store the probe sink used in probe Will callbacks to
ensure the same sink will be used for Did callbacks.

BUG=754145

Change-Id: Iaa043c0240e9e84a117c9a168fc6cc15a4b1bbf6
Reviewed-on: https://chromium-review.googlesource.com/619598
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Commit-Queue: Alexei Filippov <alph@chromium.org>
Cr-Commit-Position: refs/heads/master@{#495391}
[modify] https://crrev.com/8f3270e31783e826b59086622789f6c3613f3792/third_party/WebKit/Source/build/scripts/templates/InstrumentingProbesImpl.cpp.tmpl
[modify] https://crrev.com/8f3270e31783e826b59086622789f6c3613f3792/third_party/WebKit/Source/build/scripts/templates/InstrumentingProbesInl.h.tmpl
[modify] https://crrev.com/8f3270e31783e826b59086622789f6c3613f3792/third_party/WebKit/Source/core/frame/PerformanceMonitor.cpp


### al...@chromium.org (2017-08-21)

[Empty comment from Monorail migration]

### al...@chromium.org (2017-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-21)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-21)

+awhalley@ for M61 merge review

### aw...@google.com (2017-08-21)

alph@ - any more changes expected or can we mark this as fixed?

### al...@chromium.org (2017-08-21)

It is fixed. I just didn't want to close it before merging to M61 to not lose it from my radar.

### aw...@google.com (2017-08-21)

alph@ - thanks for the quick response! Please merge once govind@ adds the approval label. (For future reference the usual flow is to mark once fixed, and we've got automation that will pick that a merge is needed (though you applied the request manually so it's all good in this case :-) )

govind@ - good for 61


### go...@chromium.org (2017-08-21)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/754145#c23. Please merge ASAP. Thank you.

### al...@chromium.org (2017-08-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3f20531816089e903f9cebcc27a9e60c249d8cc1

commit 3f20531816089e903f9cebcc27a9e60c249d8cc1
Author: Alexei Filippov <alph@chromium.org>
Date: Mon Aug 21 18:05:29 2017

[instrumentation] Make sure the probe sink is still available when Did callbacks are invoked.

The patch makes it store the probe sink used in probe Will callbacks to
ensure the same sink will be used for Did callbacks.

BUG=754145
TBR=alph@chromium.org

(cherry picked from commit 8f3270e31783e826b59086622789f6c3613f3792)

Change-Id: Iaa043c0240e9e84a117c9a168fc6cc15a4b1bbf6
Reviewed-on: https://chromium-review.googlesource.com/619598
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Commit-Queue: Alexei Filippov <alph@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#495391}
Reviewed-on: https://chromium-review.googlesource.com/624187
Reviewed-by: Alexei Filippov <alph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#704}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/3f20531816089e903f9cebcc27a9e60c249d8cc1/third_party/WebKit/Source/build/scripts/templates/InstrumentingProbesImpl.cpp.tmpl
[modify] https://crrev.com/3f20531816089e903f9cebcc27a9e60c249d8cc1/third_party/WebKit/Source/build/scripts/templates/InstrumentingProbesInl.h.tmpl
[modify] https://crrev.com/3f20531816089e903f9cebcc27a9e60c249d8cc1/third_party/WebKit/Source/core/frame/PerformanceMonitor.cpp


### sh...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-01)

The VRP panel decided to award $500 for this report, noting the user interaction required of opening dev tools.  Many thanks for the report!

### aw...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### lo...@gmail.com (2017-10-19)

Did you forgot to do the wired transfer for this report? It's been almost two months since the status was changed to "reward-inprocess".

### aw...@google.com (2017-10-19)

Hi loobenyang@ - looking into this now and I'll follow up with you over email.  Thanks for the ping!

### sh...@chromium.org (2017-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-11-28)

This issue was migrated from crbug.com/chromium/754145?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Input, Platform>DevTools>Performance]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088656)*
