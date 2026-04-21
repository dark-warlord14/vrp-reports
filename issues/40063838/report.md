# Security:  Memory corruption due to accessing invalid context

| Field | Value |
|-------|-------|
| **Issue ID** | [40063838](https://issues.chromium.org/issues/40063838) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2023-03-30 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

The function ServiceWorkerGlobalScope::FetchHandlerType calls JSEventListener::GetEffectiveFunction at line [1], and the latter may calls v8::Object::Get to retrieve the "handleEvent" property of the listener object [2]. If "handleEvent" is an accessor, Invoke will be called to execute the getter. The problem is that the caller (FetchHandlerType) does not ensure a valid context exists at this time, resulting in memory corruption for accessing invalid context object at line [3].

bisect: This was introduced in <https://chromium.googlesource.com/chromium/src/+/6306836d087b41de48780b8d4e7b1f0bd35de365>

```
mojom::blink::ServiceWorkerFetchHandlerType  
ServiceWorkerGlobalScope::FetchHandlerType() {  
  // skip  
  for (RegisteredEventListener& e : \*elv) {  
    EventTarget\* et = EventTarget::Create(ScriptController()->GetScriptState());  
    v8::Local<v8::Value> v =  
        To<JSBasedEventListener>(e.Callback())->GetEffectiveFunction(\*et);    // ===> [1]  
    if (!v->IsFunction() ||  
        !v.As<v8::Function>()->Experimental_IsNopFunction()) {  
      return mojom::blink::ServiceWorkerFetchHandlerType::kNotSkippable;  
    }  
  }  
  //skip  
}  
  
v8::Local<v8::Value> JSEventListener::GetEffectiveFunction(  
    EventTarget& target) {  
  // skip  
    if (v8_listener.As<v8::Object>()  
            ->Get(isolate->GetCurrentContext(),  
                  V8AtomicString(isolate, "handleEvent"))    // ===> [2]  
            .ToLocal(&property) &&  
        property->IsFunction()) {  
      return GetBoundFunction(property.As<v8::Function>());  
    }  
  }  
  
V8_WARN_UNUSED_RESULT MaybeHandle<Object> Invoke(Isolate\* isolate,  
                                                 const InvokeParams& params) {  
  // skip  
  if (params.execution_target == Execution::Target::kCallable) {  
    Handle<Context> context = isolate->native_context();    // ===> [3]  
    if (!context->script_execution_callback().IsUndefined(isolate)) {  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc;l=2636;drc=48340c1e35efad5fb0253025dcc36b3a9573e258>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/js_event_listener.cc;l=35;drc=48340c1e35efad5fb0253025dcc36b3a9573e258>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/execution/execution.cc;l=383;drc=48340c1e35efad5fb0253025dcc36b3a9573e258>

**VERSION**  

Chrome Version: stable + dev

**REPRODUCTION CASE**

1. Host poc.html & worker.js  
   
   python -m http.server 8000
2. out\release\chrome.exe <http://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Received fatal exception EXCEPTION\_ACCESS\_VIOLATION  

Backtrace:  

v8::internal::`anonymous namespace'::Invoke [0x00007FFE67F08901+2225] v8::internal::Execution::Call [0x00007FFE67F08159+265] v8::internal::Object::GetPropertyWithDefinedGetter [0x00007FFE6830745C+2972] v8::internal::Object::GetPropertyWithAccessor [0x00007FFE683069AF+239] v8::internal::Runtime::GetObjectProperty [0x00007FFE6845F4FE+254] v8::Object::Get [0x00007FFE67D26B39+249] blink::JSEventListener::GetEffectiveFunction [0x00007FFE656CF229+281] blink::ServiceWorkerGlobalScope::FetchHandlerType [0x00007FFE62AB18CF+319] content::ServiceWorkerContextClient::SendWorkerStarted [0x00007FFE78579CED+15565] base::TaskAnnotator::RunTaskImpl [0x00007FFEC5F2D22A+378] base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFEC5F4E714+1156] base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFEC5F4E124+196] base::MessagePumpDefault::Run [0x00007FFEC5EBF2B5+149] base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFEC5F4F2CE+382] base::RunLoop::Run [0x00007FFEC5EFC3B7+519] blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run [0x00007FFE644AE2BB+1307] base::`anonymous namespace'::ThreadFunc [0x00007FFEC5FC99FB+267]  

BaseThreadInitThunk [0x00007FFF03DC7614+20]  

RtlUserThreadStart [0x00007FFF04A626A1+33]

\*\*Fix Suggestion\*\*  

Define a context scope before calling JSEventListener::GetEffectiveFunction.

diff --git a/third\_party/blink/renderer/modules/service\_worker/service\_worker\_global\_scope.cc b/third\_party/blink/renderer/modules/service\_worker/service\_worker\_global\_scope.cc  

index e068d77ebbf66..dccf3583717b9 100644  

--- a/third\_party/blink/renderer/modules/service\_worker/service\_worker\_global\_scope.cc  

+++ b/third\_party/blink/renderer/modules/service\_worker/service\_worker\_global\_scope.cc  

@@ -2628,6 +2628,7 @@ ServiceWorkerGlobalScope::FetchHandlerType() {  

}  

v8::Isolate\* isolate = GetIsolate();  

v8::HandleScope handle\_scope(isolate);

- v8::Context::Scope scope(ScriptController()->GetScriptState()->GetContext());  
  
  // TODO([crbug.com/1349613](https://crbug.com/1349613)): revisit the way to implement this.  
  
  // The following code returns kEmptyFetchHandler if all handlers are nop.  
  
  for (RegisteredEventListener& e : \*elv) {

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 165 B)
- [worker.js](attachments/worker.js) (text/plain, 165 B)

## Timeline

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5359610857455616.

### mp...@chromium.org (2023-03-30)

[Empty comment from Monorail migration]

### yy...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### yy...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### yy...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-04-01)

[Empty comment from Monorail migration]

[Monorail components: Blink>ServiceWorker]

### [Deleted User] (2023-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-04-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/299385e09d41d5ce3abd434879b5f9b0a8880cd7

commit 299385e09d41d5ce3abd434879b5f9b0a8880cd7
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Mon Apr 03 00:44:38 2023

Use ScriptState::Scope instead of setting HandleScope.

Since `GetEffectiveFunction` may call `Get` if the given v8 listener is
an object, we need to prepare `v8::Context::Scope` before calling it.
Blink already have a helper class to prepare the environment for the
script execution, which has already been used used in other
ServiceWorkerGlobalScope member functions.  It is `ScriptState::Scope`
This CL also use it instead.

Bug: 1429197
Change-Id: Idbcfdfa9c06160a18b57155a9540f72eed4ec0b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4387655
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1125148}

[modify] https://crrev.com/299385e09d41d5ce3abd434879b5f9b0a8880cd7/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/299385e09d41d5ce3abd434879b5f9b0a8880cd7/content/test/data/service_worker/fetch_event_with_handle_event_property.js
[modify] https://crrev.com/299385e09d41d5ce3abd434879b5f9b0a8880cd7/content/test/content_unittests_bundle_data.filelist
[modify] https://crrev.com/299385e09d41d5ce3abd434879b5f9b0a8880cd7/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### yy...@chromium.org (2023-04-03)

I have used a part of the reporter's PoC code in the test.  Please let me know if it is an issue.

### yy...@chromium.org (2023-04-03)

With the https://crbug.com/chromium/1429197#c11 change, the issue has been fixed.

### [Deleted User] (2023-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-03)

Requesting merge to extended stable M110 because latest trunk commit (1125148) appears to be after extended stable branch point (1084008).

Requesting merge to other stable M111 because latest trunk commit (1125148) appears to be after other stable branch point (1097615).

Requesting merge to stable M112 because latest trunk commit (1125148) appears to be after stable branch point (1109224).

Requesting merge to dev M113 because latest trunk commit (1125148) appears to be after dev branch point (1121455).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-04-03)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/chromium/src/+/4387655

2. Has this fix been tested on Canary?

Maybe.  It has already been available as:
https://chromium.googlesource.com/chromium/src/+log/114.0.5693.0

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

I believe existing tests ensure that this CL does not bring any stability regressions and risks.  The CL is fairly simple because it just started to use `ScriptState::Scope` as other functions in the file does.

4. Does this fix pose any known compatibility risks?

I do not think so.

5. Does it require manual verification by the test team? If so, please describe required testing.

I do not think so.

### yy...@chromium.org (2023-04-03)

FYI, there is a related security bug:
https://bugs.chromium.org/p/chromium/issues/detail?id=1429201


### [Deleted User] (2023-04-04)

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-04)

Merge review required: M112 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-04)

Merge review required: M111 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-05)

chatted with mpdenton@ who was able to repro this issue (and just got to add that here), the weird access violation stack trace is because we were dereferencing some very strange value, and Intel CPUs give weird results for non-canonical address like this. But it is a deref of something that should definitely not be deref'ed. 


### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations Rong Jian! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### yy...@chromium.org (2023-04-06)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

This is a security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4387655

3. Have the changes been released and tested on canary?

Maybe.  It has already been available as:
https://chromium.googlesource.com/chromium/src/+log/114.0.5693.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

I do not think so.

### gi...@appspot.gserviceaccount.com (2023-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99df77d2ca1527b48db3cc81a2b46007460359c5

commit 99df77d2ca1527b48db3cc81a2b46007460359c5
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Thu Apr 06 06:57:36 2023

[M113] Use ScriptState::Scope instead of setting HandleScope.

Since `GetEffectiveFunction` may call `Get` if the given v8 listener is
an object, we need to prepare `v8::Context::Scope` before calling it.
Blink already have a helper class to prepare the environment for the
script execution, which has already been used used in other
ServiceWorkerGlobalScope member functions.  It is `ScriptState::Scope`
This CL also use it instead.

(cherry picked from commit 299385e09d41d5ce3abd434879b5f9b0a8880cd7)

Bug: 1429197
Change-Id: Idbcfdfa9c06160a18b57155a9540f72eed4ec0b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4387655
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1125148}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4402615
Cr-Commit-Position: refs/branch-heads/5672@{#289}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/99df77d2ca1527b48db3cc81a2b46007460359c5/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/99df77d2ca1527b48db3cc81a2b46007460359c5/content/test/data/service_worker/fetch_event_with_handle_event_property.js
[modify] https://crrev.com/99df77d2ca1527b48db3cc81a2b46007460359c5/content/test/content_unittests_bundle_data.filelist
[modify] https://crrev.com/99df77d2ca1527b48db3cc81a2b46007460359c5/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### [Deleted User] (2023-04-06)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-04-06)

1. Was this issue a regression for the milestone it was found in?

Yes.  The code has been implemented for M106, and M108 must be affected.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

Yes, but this fix must be independent from the changes.  That is because:
- the fix only updates the way to decide fetch_handler_type, and the code change won't be scattered.  User of the fetch_handler_type do not need to be updated for the change.
- and, major implementations for the feature has already been shipped as M106, and no large scale code update is needed for the way we handle fetch_handler_type.

### rz...@google.com (2023-04-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-08)

m113 merge approved, please merge this fix to branch 5672 by EOD Tuesday, 11 April so this fix can be included in the next M113/Beta
m112 merge approved, please merge this fix to branch 5615 at your earliest convenience so this fix can be included in the next Stable/112 security respin -- thank you! 

### am...@google.com (2023-04-08)

M112 is now Stable/Extended Stable, there are no further releases of M110 and M111

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2b30a50d0e62940cc183c287770a1affeffb7ebf

commit 2b30a50d0e62940cc183c287770a1affeffb7ebf
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Mon Apr 10 05:32:06 2023

[M112] Use ScriptState::Scope instead of setting HandleScope.

Since `GetEffectiveFunction` may call `Get` if the given v8 listener is
an object, we need to prepare `v8::Context::Scope` before calling it.
Blink already have a helper class to prepare the environment for the
script execution, which has already been used used in other
ServiceWorkerGlobalScope member functions.  It is `ScriptState::Scope`
This CL also use it instead.

(cherry picked from commit 299385e09d41d5ce3abd434879b5f9b0a8880cd7)

Bug: 1429197
Change-Id: Idbcfdfa9c06160a18b57155a9540f72eed4ec0b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4387655
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1125148}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4411454
Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#1191}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/2b30a50d0e62940cc183c287770a1affeffb7ebf/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/2b30a50d0e62940cc183c287770a1affeffb7ebf/content/test/data/service_worker/fetch_event_with_handle_event_property.js
[modify] https://crrev.com/2b30a50d0e62940cc183c287770a1affeffb7ebf/content/test/content_unittests_bundle_data.filelist
[modify] https://crrev.com/2b30a50d0e62940cc183c287770a1affeffb7ebf/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### pb...@google.com (2023-04-10)

This merge has been approved for M113, please help complete your merges asap (before 1pm PST) tomorrow, so the change can be included in this week's RC build for beta releases.`

We would like to get the changes as much beta time as possible, so please complete your merges asap to M113 branch(go/chrome-branches).


### yy...@google.com (2023-04-10)

I think the fix has been merged to M113 at https://bugs.chromium.org/p/chromium/issues/detail?id=1429197#c27.


### yy...@google.com (2023-04-10)

Also FYI but there is an issue that happens after this change has been merged:
https://bugs.chromium.org/p/chromium/issues/detail?id=1429201
I suggest you to proceed the merge review soon.

### rz...@google.com (2023-04-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-04-11)

1. https://crrev.com/c/4405896, but the fix for https://crbug.com/1429201 need to be merged after it lands (see https://crbug.com/chromium/1429197#c37)
2. Low, only a few simple conflicts
3. 112, 113
4. Yes

### gm...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-17)

merge to 113 already happened in c#27 

### am...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-19)

[Empty comment from Monorail migration]

### yy...@chromium.org (2023-04-20)

[Empty comment from Monorail migration]

### gm...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbb228e5d45576c60f5d3314f386bd3265654a37

commit cbb228e5d45576c60f5d3314f386bd3265654a37
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Wed Apr 26 09:00:54 2023

[M108-LTS] Use ScriptState::Scope instead of setting HandleScope.

M108 merge issues:

  third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc:
    Conflicting declarations for isolate

  content_unittests_bundle_data.filelist:
    Not present in 108, skipped; Only used in iOS tests on main

Since `GetEffectiveFunction` may call `Get` if the given v8 listener is
an object, we need to prepare `v8::Context::Scope` before calling it.
Blink already have a helper class to prepare the environment for the
script execution, which has already been used used in other
ServiceWorkerGlobalScope member functions.  It is `ScriptState::Scope`
This CL also use it instead.

(cherry picked from commit 299385e09d41d5ce3abd434879b5f9b0a8880cd7)

Bug: 1429197
Change-Id: Idbcfdfa9c06160a18b57155a9540f72eed4ec0b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4387655
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1125148}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4405896
Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1448}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/cbb228e5d45576c60f5d3314f386bd3265654a37/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/cbb228e5d45576c60f5d3314f386bd3265654a37/content/test/data/service_worker/fetch_event_with_handle_event_property.js
[modify] https://crrev.com/cbb228e5d45576c60f5d3314f386bd3265654a37/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### rz...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1429197?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1347319]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063838)*
