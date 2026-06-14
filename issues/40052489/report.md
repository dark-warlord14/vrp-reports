# Google Chrome PDFium Javascript Active Document Memory Corruption Vulnerability -  TALOS-2020-1092  

| Field | Value |
|-------|-------|
| **Issue ID** | [40052489](https://issues.chromium.org/issues/40052489) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Internals>Plugins>PDF |
| **Platforms** | Mac |
| **Reporter** | [Deleted User] |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-06-04 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15

Steps to reproduce the problem:
Please review attached advisory and poc file

What is the expected behavior?

What went wrong?
### Summary

A memory corruption vulnerability exists in the way Google Chrome 83.0.4103.61 executes Javascript inside PDF documents. A specially crafted web page can cause out of bounds memory access. To trigger this vulnerability, the victim must visit a malicious webpage or open a malicious PDF document.

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: n/a
OS Version: OS X 10.14.6
Flash Version:

## Attachments

- [relaxed_load.pdf](attachments/relaxed_load.pdf) (application/pdf, 794 B)

## Timeline

### cl...@chromium.org (2020-06-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5713789216948224.

### ts...@chromium.org (2020-06-04)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@google.com (2020-06-04)

Did not reproduce either on clusterfuzz or on tip-of-tree pdfium using pdfium_test.  Specifically, what chromium version are you using (see about:version)?

### cl...@chromium.org (2020-06-04)

Testcase 5713789216948224 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5713789216948224.

### cl...@chromium.org (2020-06-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6225104402448384.

### ts...@google.com (2020-06-04)

And yet trying to open the document in chrome 83 on chromeos did crash the plugin.

### th...@chromium.org (2020-06-04)

The bug reporter mentioned 83.0.4103.61.

In my local build on Linux, I see:

# Fatal error in ../../v8/src/objects/js-objects.cc, line 4363
# Debug check failed: prototype_users->Get(slot) == HeapObjectReference::Weak(*user) (<unprintable> vs. <unprintable>)

### th...@chromium.org (2020-06-04)

Crash ID: 8edddc2d9897fe5a

Thread 0 (id: 0x0001c94f) CRASHED [SIGSEGV /SEGV_MAPERR @ 0x000015ef1b000000 ]
0x0000562f3c63f588	(chrome -vector:656)		CFXJS_Engine::NewFXJSBoundObject(int, FXJSOBJTYPE)
0x0000562f3c650304	(chrome -cjs_document.cpp:254)		CJS_Document::getField_static(v8::FunctionCallbackInfo<v8::Value> const&)

### ts...@google.com (2020-06-05)

Debug build of chrome is hitting:
#
# Fatal error in ../../v8/src/objects/js-objects.cc, line 4363
# Debug check failed: prototype_users->Get(slot) == HeapObjectReference::Weak(*user) (<unprintable> vs. <unprintable>).
#


### ts...@google.com (2020-06-05)

And stack is something like:

READ of size 8 at 0x604000000008 thread T0 (chrome)
    #0 0x55ac473d6fd9 in size ./../../buildtools/third_party/libc++/trunk/include/vector:656:46
    #1 0x55ac473d6fd9 in CollectionSize<int, std::__1::vector<std::__1::unique_ptr<CFXJS_ObjDefinition, std::__1::default_delete<CFXJS_ObjDefinition> >, std::__1::allocator<std::__1::unique_ptr<CFXJS_ObjDefinition, std::__1::default_delete<CFXJS_ObjDefinition> > > > > ./../../third_party/pdfium/third_party/base/stl_util.h:127:60
    #2 0x55ac473d6fd9 in MaxObjDefinitionID ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:325:10
    #3 0x55ac473d6fd9 in ObjDefinitionForID ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:332:27
    #4 0x55ac473d6fd9 in CFXJS_Engine::NewFXJSBoundObject(int, FXJSOBJTYPE) ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:580:41
    #5 0x55ac47407e9e in CJS_Document::getField(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) ./../../third_party/pdfium/fxjs/cjs_document.cpp:255:47
    #6 0x55ac4742d111 in void JSMethod<CJS_Document, &(CJS_Document::getField(CJS_Runtime*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&))>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/pdfium/fxjs/js_define.h:128:23
    #7 0x55ac43a71800 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158:3
    #8 0x55ac43a6eddd in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:111:36
    #9 0x55ac43a6c572 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:141:5
    #10 0x55ac46081e17 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit ??:0:0
    #11 0x55ac46017474 in Builtins_InterpreterEntryTrampoline ??:0:0
    #12 0x55ac46014fb9 in Builtins_JSEntryTrampoline ??:0:0
    #13 0x55ac46014d97 in Builtins_JSEntry ??:0:0
    #14 0x55ac43d78542 in Call ./../../v8/src/execution/simulator.h:142:12
    #15 0x55ac43d78542 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/execution.cc:367:33
    #16 0x55ac43d770ba in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:461:10
    #17 0x55ac438d7583 in v8::Script::Run(v8::Local<v8::Context>) ./../../v8/src/api/api.cc:2089:7
    #18 0x55ac473d7dfe in CFXJS_Engine::Execute(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cfxjs_engine.cpp:561:25
    #19 0x55ac474c6eec in CJS_Runtime::ExecuteScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_runtime.cpp:164:10
    #20 0x55ac47449746 in CJS_EventContext::RunScript(fxcrt::WideString const&) ./../../third_party/pdfium/fxjs/cjs_event_context.cpp:53:23
    #21 0x55ac472d7b1e in RunScript ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:461:13
    #22 0x55ac472d7b1e in CPDFSDK_ActionHandler::RunDocumentOpenJavaScript(CPDFSDK_FormFillEnvironment*, fxcrt::WideString const&, fxcrt::WideString const&) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:384:3
    #23 0x55ac472d7430 in CPDFSDK_ActionHandler::ExecuteDocumentOpenAction(CPDF_Action const&, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:148:9
    #24 0x55ac472d6e58 in CPDFSDK_ActionHandler::DoAction_DocOpen(CPDF_Action const&, CPDFSDK_FormFillEnvironment*) ./../../third_party/pdfium/fpdfsdk/cpdfsdk_actionhandler.cpp:26:10
    #25 0x55ac473251da in CPDFSDK_FormFillEnvironment::ProcOpenAction() ./../../third_party/pdfium/fpdfsdk/cpdfsdk_formfillenvironment.cpp:629:23


### ts...@google.com (2020-06-05)

[Empty comment from Monorail migration]

### ts...@google.com (2020-06-05)

FYI, a debug build of pdfium_test hits the same assert even if the asan build isn't seeing the corruption.

### cl...@chromium.org (2020-06-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6225104402448384

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x60b000000008
Crash State:
  CJS_Document::getField
  void JSMethod<CJS_Document, &
  v8::internal::FunctionCallbackArguments::Call
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=775331

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6225104402448384

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6225104402448384 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### ts...@chromium.org (2020-06-05)

Assigning to V8 triage sheriff - Perhaps you can find an owner to point me at what would case V8 to trip over this first assert in the debug case.  

[Monorail components: Blink>JavaScript]

### ts...@chromium.org (2020-06-05)

(And also noting that the reporter suggests that somehow a circular prototype chain was not detected).

### [Deleted User] (2020-06-05)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-05)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-05)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9b9ba210f32c2a33cff3502a75eb84c39ad5576a

commit 9b9ba210f32c2a33cff3502a75eb84c39ad5576a
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jun 05 22:51:06 2020

Make PDFium JS host object have immutable prototypes

It is doubtful that any legitimate PDF would ever change __proto__
on these objects, and those that do are just trying to muck with us.

Bug: chromium:1091404
Change-Id: I99367281e796b91c1858fead3eb18a3a655291f1
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/70430
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/9b9ba210f32c2a33cff3502a75eb84c39ad5576a/testing/resources/javascript/immutable_proto_expected.txt
[add] https://pdfium.googlesource.com/pdfium/+/9b9ba210f32c2a33cff3502a75eb84c39ad5576a/testing/resources/javascript/immutable_proto.in
[modify] https://pdfium.googlesource.com/pdfium/+/9b9ba210f32c2a33cff3502a75eb84c39ad5576a/fxjs/cfxjs_engine.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b274fe0e2ebffe75329f8841a20e8f3da7a8ca94

commit b274fe0e2ebffe75329f8841a20e8f3da7a8ca94
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Jun 06 07:15:07 2020

Roll PDFium from 6389dd163731 to 8d477f73bf8b (5 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/6389dd163731..8d477f73bf8b

2020-06-06 thestig@chromium.org Forward declare more in xfa_js_embedder_test.h.
2020-06-06 thestig@chromium.org Remove |bFillFullcover| and |bThinLine| from CPDF_RenderOptions.
2020-06-06 thestig@chromium.org Remove |CPDF_RenderOptions::bOverprint|.
2020-06-06 thestig@chromium.org Change CFDE_TextOut::Piece members from int to size_t.
2020-06-05 tsepez@chromium.org Make PDFium JS host object have immutable prototypes

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1091404
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: If57dbfa4b6bd54449ea30714d4c0134c443c661c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2233653
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#775874}

[modify] https://crrev.com/b274fe0e2ebffe75329f8841a20e8f3da7a8ca94/DEPS


### cl...@chromium.org (2020-06-06)

ClusterFuzz testcase 6225104402448384 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=775873:775874

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-06)

Requesting merge to stable M83 because latest trunk commit (775874) appears to be after stable branch point (756066).

Requesting merge to beta M84 because latest trunk commit (775874) appears to be after beta branch point (768962).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-07)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-06-08)

vahl@ Please reply to https://crbug.com/chromium/1091404#c23, which helps in merged decision. 

The Cl in https://crbug.com/chromium/1091404#c18 isn't landed on Canary yet.

+Adetaylor@(Security TPM) for merged approval after Canary coverage.

### va...@chromium.org (2020-06-08)

As you're the owner of the change, please reply to https://crbug.com/chromium/1091404#c23, which helps in merged decision. 

### na...@google.com (2020-06-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-06-08)

re: merge, one line change, should be good to merge.
re v8: the CL just breaks the exploit chain, would be good to know what v8 does when it encounters an object with c++ bindings with a mutable prototype that gets frozen.

### ad...@chromium.org (2020-06-08)

Tom, do you think there's even the tiniest chance that some legitimate PDFs might rely on mutable protos? We are even more nervous than usual about merging fixes to M83 because of no-meetings-weeks making it harder to rectify problems.

I'm approving merge to M84 (branch 4147) but will wait for your thoughts before M83 approval.

### ts...@chromium.org (2020-06-08)

I'd be surprised if acrobat even supported .__proto__ since it was introduced only about a dozen years ago IIRC, ... but Lei would be able to tell for sure.

### ts...@chromium.org (2020-06-08)

And I'm wrong.  A web search shows some public reports of issues with __proto__ in acrobat.
So I'm in agreement with Ade, let's roll merge in 84 only.

### ad...@chromium.org (2020-06-08)

Oh gosh. OK, 84 it is. Thanks for searching Tom.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-09)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/bee2261eab794536f236013fa8c9d01728ed326b

commit bee2261eab794536f236013fa8c9d01728ed326b
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jun 09 22:32:04 2020

Merge to M84: Make PDFium JS host object have immutable prototypes

It is doubtful that any legitimate PDF would ever change __proto__
on these objects, and those that do are just trying to muck with us.

TBR: thestig@chromium.org
Bug: chromium:1091404
Change-Id: I99367281e796b91c1858fead3eb18a3a655291f1
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/70430
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 9b9ba210f32c2a33cff3502a75eb84c39ad5576a)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/70471
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/bee2261eab794536f236013fa8c9d01728ed326b/testing/resources/javascript/immutable_proto_expected.txt
[add] https://pdfium.googlesource.com/pdfium/+/bee2261eab794536f236013fa8c9d01728ed326b/testing/resources/javascript/immutable_proto.in
[modify] https://pdfium.googlesource.com/pdfium/+/bee2261eab794536f236013fa8c9d01728ed326b/fxjs/cfxjs_engine.cpp


### na...@google.com (2020-06-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-11)

Congrats! The Panel decided to award $2,000 for this report! 

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-12)

Do you have a CVE assigned for this issue and a pubic disclosure release date?

### ad...@chromium.org (2020-06-12)

It will get a CVE when we release it, which is expected around to be in M84 so July 14th: https://chromiumdash.appspot.com/schedule

### [Deleted User] (2020-06-12)

Thanks for the update.

### ke...@chromium.org (2020-06-16)

Adding yyounan at his request.

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

Please confirm exact date that this issue is ready for public disclosure


### ad...@chromium.org (2020-07-14)

14 weeks after the bug was fixed. That is 12th September. We may well be willing to open it up earlier if you have a compelling need, but certainly we'd want to wait a few weeks until M84 is rolled out to the majority of the stable population.

Meanwhile a very brief description will be going out with the release notes today and the CVE description in the next couple of days.

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-14)

Since it is beyond 14 weeks, we will plan for public disclosure on our end.

### ad...@chromium.org (2020-09-14)

Sounds good! Thanks for waiting!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1091404?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052489)*
