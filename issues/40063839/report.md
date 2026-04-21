# Security: Memory corruption due to HeapVector iterator invalidation

| Field | Value |
|-------|-------|
| **Issue ID** | [40063839](https://issues.chromium.org/issues/40063839) |
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

In function ServiceWorkerGlobalScope::FetchHandlerType, it iterates all registered fetch event listeners and calls JSEventListener::GetEffectiveFunction to get the listener function [1]. JSEventListener::GetEffectiveFunction may calls v8::Object::Get to retrieve the "handleEvent" property of the listener object [2], which may executes user defined JS code and invalidates the iterator by removing fetch event listeners.

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

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc;l=2636;drc=48340c1e35efad5fb0253025dcc36b3a9573e258>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/js_event_listener.cc;l=35;drc=48340c1e35efad5fb0253025dcc36b3a9573e258>

**VERSION**  

Chrome Version: stable + dev

**REPRODUCTION CASE**

1. Apply the patch.diff, this is to avoid early crash referred in [crbug.com/1429197](https://crbug.com/1429197).
2. Host poc.html & worker.js  
   
   python -m http.server 8000
3. out\release\chrome.exe <http://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Backtrace:  

blink::ServiceWorkerGlobalScope::FetchHandlerType [0x00007FFE62AB18A6+278]  

content!content::ServiceWorkerContextClient::SendWorkerStarted [0x00007FFE78579CED+15565]  

base::TaskAnnotator::RunTaskImpl [0x00007FFEC5F2D22A+378]  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFEC5F4E714+1156]  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFEC5F4E124+196]  

base::MessagePumpDefault::Run [0x00007FFEC5EBF2B5+149]  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFEC5F4F2CE+382]  

base::RunLoop::Run [0x00007FFEC5EFC3B7+519]  

blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run [0x00007FFE644AE2BB+1307]  

base::`anonymous namespace'::ThreadFunc [0x00007FFEC5FC99FB+267]  

BaseThreadInitThunk [0x00007FFF03DC7614+20]  

RtlUserThreadStart [0x00007FFF04A626A1+33]

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 830 B)
- [poc.html](attachments/poc.html) (text/plain, 165 B)
- [worker.js](attachments/worker.js) (text/plain, 500 B)

## Timeline

### [Deleted User] (2023-03-30)

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

When I defined the specification, I tried to follow GetEffectiveFunction behavior because I did not recognize the attack like this.  However, it seems to bring modification of the event listener list by defining the get function that modifies the event listener list.  What do you think if I make it not support the handleEvent property?
Especially, I suggest to omit Step 4 in https://w3c.github.io/ServiceWorker/#all-fetch-listeners-are-empty-algorithm

### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5105ce37a6853d52ec97894bf6969b3c29a23afd

commit 5105ce37a6853d52ec97894bf6969b3c29a23afd
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Wed Apr 05 11:47:04 2023

Stop supporting { handleEvent }.

Make the code aligned with the following specification update:
https://github.com/w3c/ServiceWorker/pull/1676

With the previous specification and code, event listener vector
can be modified during the GetEffectiveFunction execution, which may
bring unexpected vector state.

Change-Id: I732c4c9ab2caebc49a7f4ef52640df7b8476d838
Bug: 1429201
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4394402
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Domenic Denicola <domenic@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1126483}

[modify] https://crrev.com/5105ce37a6853d52ec97894bf6969b3c29a23afd/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/5105ce37a6853d52ec97894bf6969b3c29a23afd/content/test/data/service_worker/fetch_event_object_removing_itself.js
[modify] https://crrev.com/5105ce37a6853d52ec97894bf6969b3c29a23afd/content/test/content_unittests_bundle_data.filelist
[modify] https://crrev.com/5105ce37a6853d52ec97894bf6969b3c29a23afd/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### yy...@chromium.org (2023-04-06)

Although the spec update is not merged yet, let me mark this fixed because the code fix has been merged.

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

Requesting merge to stable M112 because latest trunk commit (1126483) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1126483) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Merge review required: M113 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-04-07)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/chromium/src/+/4394402

2. Has this fix been tested on Canary?

maybe.
It is included in https://chromium.googlesource.com/chromium/src/+log/114.0.5698.0

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

We have tests to confirm the behavior under typical service worker usages.
The CL has been merged after checked by such tests.

4. Does this fix pose any known compatibility risks?

Pragmatically, no.
However, it is fair to say yes technically because the fix has been merged before waiting for the specification fix: https://github.com/w3c/ServiceWorker/pull/1676.
But as you can see in https://github.com/w3ctag/design-reviews/issues/815, no other major browser vendors seem to follow our latest proposal released in https://github.com/w3c/ServiceWorker/issues/1671.  There should not be actual compatibility issues.

5. Does it require manual verification by the test team? If so, please describe required testing.

I do not think so.  Automated tests included in the CL covers the case.

### [Deleted User] (2023-04-07)

Requesting merge to stable M112 because latest trunk commit (1126483) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1126483) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Merge review required: M113 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-08)

Requesting merge to stable M112 because latest trunk commit (1126483) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1126483) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Merge review required: M113 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-08)

Requesting merge to stable M112 because latest trunk commit (1126483) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1126483) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Merge review required: M113 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-09)

Requesting merge to stable M112 because latest trunk commit (1126483) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1126483) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Merge review required: M113 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-04-10)

I think the merge questions are answered in https://crbug.com/chromium/1429201#c12, but the sheriff bot may missed it for some reasons?
Let me answer it again.

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/chromium/src/+/4394402

2. Has this fix been tested on Canary?

Yes.
It is included in https://chromium.googlesource.com/chromium/src/+log/114.0.5698.0

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

We have tests to confirm the behavior under typical service worker usages.
The CL has been merged after checked by such tests.

4. Does this fix pose any known compatibility risks?

Pragmatically, no.
However, it is fair to say yes technically because the fix has been merged before waiting for the specification fix: https://github.com/w3c/ServiceWorker/pull/1676.
But as you can see in https://github.com/w3ctag/design-reviews/issues/815, no other major browser vendors seem to follow our latest proposal released in https://github.com/w3c/ServiceWorker/issues/1671.  There should not be actual compatibility issues.

5. Does it require manual verification by the test team? If so, please describe required testing.

I do not think so.  Automated tests included in the CL covers the case.


### go...@chromium.org (2023-04-10)

This is Blink, not applicable to iOS. 

### [Deleted User] (2023-04-10)

Requesting merge to stable M112 because latest trunk commit (1126483) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1126483) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Merge review required: M113 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-10)

Now that this fix has had enough bake time on Canary it doesn't appear to result in any issues to prevent it from being merged; however, I notice the mentions of the spec update not being merged in a few comments above -- what is the status of that? Are there any issues if this fix is merged without the spec updated being merged? 

Pending the responses to this, merge tentatively approved for M113 and M112 
As long as there are no issues potentially introduced by asymmetrically merging this fix without the spec change, please merge this fix to branch 5672 before EOD tomorrow / Tuesday, 11 April so this fix can be included in the next M113/beta release on Wednesday. 

Please also merge this fix to branch 5615 by EOD Thursday, 13 April, so this fix can be included in the M112/Stable respin release on Tuesday. 


### yy...@chromium.org (2023-04-11)

Re: #20
The spec update has not been merged yet (https://github.com/w3c/ServiceWorker/pull/1676).  The PR does not get any comments from other vendors.
Since Chromium only implements the feature, fixing without the spec update should not bring any interoperability issues.
(FYI, no signals from other vendors https://groups.google.com/a/chromium.org/g/blink-dev/c/tEFS0BH8UmE/m/kSIIFJFOBAAJ)

I plan to merge the fixes.  Can I ask you to set Merge approval labels?

### am...@chromium.org (2023-04-11)

Thank you for the update / response. Merges approved, merge labels updated accordingly.

### gi...@appspot.gserviceaccount.com (2023-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9933547b5124508232f09e6e1c0d09e0999dac53

commit 9933547b5124508232f09e6e1c0d09e0999dac53
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Tue Apr 11 04:45:57 2023

[M113] Stop supporting { handleEvent }.

Make the code aligned with the following specification update:
https://github.com/w3c/ServiceWorker/pull/1676

With the previous specification and code, event listener vector
can be modified during the GetEffectiveFunction execution, which may
bring unexpected vector state.

(cherry picked from commit 5105ce37a6853d52ec97894bf6969b3c29a23afd)

Change-Id: I732c4c9ab2caebc49a7f4ef52640df7b8476d838
Bug: 1429201
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4394402
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Domenic Denicola <domenic@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1126483}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4411225
Reviewed-by: Minoru Chikamune <chikamune@chromium.org>
Cr-Commit-Position: refs/branch-heads/5672@{#442}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/9933547b5124508232f09e6e1c0d09e0999dac53/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/9933547b5124508232f09e6e1c0d09e0999dac53/content/test/data/service_worker/fetch_event_object_removing_itself.js
[modify] https://crrev.com/9933547b5124508232f09e6e1c0d09e0999dac53/content/test/content_unittests_bundle_data.filelist
[modify] https://crrev.com/9933547b5124508232f09e6e1c0d09e0999dac53/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### [Deleted User] (2023-04-11)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-04-11)

Same as https://bugs.chromium.org/p/chromium/issues/detail?id=1429197#c29

1. Was this issue a regression for the milestone it was found in?

Yes.  The code has been implemented for M106, and M108 must be affected.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

Yes, but this fix must be independent from the changes.  That is because:
- the fix only updates the way to decide fetch_handler_type, and the code change won't be scattered.  User of the fetch_handler_type do not need to be updated for the change.
- and, major implementations for the feature has already been shipped as M106, and no large scale code update is needed for the way we handle fetch_handler_type.

### rz...@google.com (2023-04-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f58218891f8cbd9186f11e31a0a93391c9f21b2e

commit f58218891f8cbd9186f11e31a0a93391c9f21b2e
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Tue Apr 11 07:12:34 2023

[M112] Stop supporting { handleEvent }.

Make the code aligned with the following specification update:
https://github.com/w3c/ServiceWorker/pull/1676

With the previous specification and code, event listener vector
can be modified during the GetEffectiveFunction execution, which may
bring unexpected vector state.

(cherry picked from commit 5105ce37a6853d52ec97894bf6969b3c29a23afd)

Change-Id: I732c4c9ab2caebc49a7f4ef52640df7b8476d838
Bug: 1429201
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4394402
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Domenic Denicola <domenic@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1126483}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4408837
Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
Reviewed-by: Minoru Chikamune <chikamune@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#1203}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/f58218891f8cbd9186f11e31a0a93391c9f21b2e/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/f58218891f8cbd9186f11e31a0a93391c9f21b2e/content/test/data/service_worker/fetch_event_object_removing_itself.js
[modify] https://crrev.com/f58218891f8cbd9186f11e31a0a93391c9f21b2e/content/test/content_unittests_bundle_data.filelist
[modify] https://crrev.com/f58218891f8cbd9186f11e31a0a93391c9f21b2e/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


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

1. Just https://crrev.com/c/4406580
2. Low, only a simple conflict with a missing file
3. 112, 113
4. Yes

### gm...@google.com (2023-04-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, Rong! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

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

### gm...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b887639bad4bde0e3776f93048249b5837fd6948

commit b887639bad4bde0e3776f93048249b5837fd6948
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Wed Apr 26 10:33:18 2023

[M108-LTS] Stop supporting { handleEvent }.

M108 merge issues:
  content_unittests_bundle_data.filelist:
    Not present in 108, skipped; Only used in iOS tests on main

Make the code aligned with the following specification update:
https://github.com/w3c/ServiceWorker/pull/1676

With the previous specification and code, event listener vector
can be modified during the GetEffectiveFunction execution, which may
bring unexpected vector state.

(cherry picked from commit 5105ce37a6853d52ec97894bf6969b3c29a23afd)

Change-Id: I732c4c9ab2caebc49a7f4ef52640df7b8476d838
Bug: 1429201
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4394402
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1126483}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4406580
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1449}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/b887639bad4bde0e3776f93048249b5837fd6948/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/b887639bad4bde0e3776f93048249b5837fd6948/content/test/data/service_worker/fetch_event_object_removing_itself.js
[modify] https://crrev.com/b887639bad4bde0e3776f93048249b5837fd6948/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### rz...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1429201?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1347319]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063839)*
