# V8 type confusion of Undefined as v8::Function in ServiceWorkerGlobalScope::FetchHandlerType

| Field | Value |
|-------|-------|
| **Issue ID** | [40062472](https://issues.chromium.org/issues/40062472) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Linux |
| **Reporter** | wx...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2023-01-03 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

1.a  

2.  

3.

**Problem Description:**  

a

**Additional Comments:**

\*\*Chrome version: \*\* 111.0.5517.0 \*\*Channel: \*\* Canary

**OS:** Linux

## Attachments

- [service-worker.js](attachments/service-worker.js) (text/plain, 5.6 KB)
- [0001-fix-type-confusion.patch](attachments/0001-fix-type-confusion.patch) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-03)

1. gsutil cp  gs://chromium-brwoser-asan/linux-debug/asan-linux-debug-1088129.zip .
2. unzip it and run "./chrome --no-sandbox"
3. git clone https://github.com/GoogleChrome/samples --depth 1 
4. change "samples/service-worker/prefetch/service-worker.js" to my service-worker.js
5. enter the dir samples  and run "cd ../ && python -m SimpleHTTPServer"
6. visit http://127.0.0.1:8000/samples/service-worker/prefetch/index.html
7. the render will crash, I don't have the symbol.

```
16191:16471:0103/170005.575649:FATAL:v8_initializer.cc(727)] V8 error: Value is not a Function (v8::Function::Cast).
#0 0x55d8d7c87a47 (/home/raven/work/asan-linux-debug-1088129/chrome+0xa5cfa46)
#1 0x7f06761952ec (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xe902eb)
#2 0x7f0675906f24 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0x601f23)
#3 0x7f0675906d95 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0x601d94)
#4 0x7f06759f93c7 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0x6f43c6)
#5 0x7f05c442400a (/home/raven/work/asan-linux-debug-1088129/libblink_core.so+0x4e8d009)
#6 0x7f05ad405588 (/home/raven/work/asan-linux-debug-1088129/libv8.so+0x2141587)
#7 0x7f05a3a44916 (/home/raven/work/asan-linux-debug-1088129/libblink_modules.so+0x9490915)
#8 0x7f05a3add7ed (/home/raven/work/asan-linux-debug-1088129/libblink_modules.so+0x95297ec)
#9 0x7f066f2eed5e (/home/raven/work/asan-linux-debug-1088129/libcontent.so+0xea57d5d)
#10 0x7f066f301c0e (/home/raven/work/asan-linux-debug-1088129/libcontent.so+0xea6ac0d)
#11 0x7f066f3018ae (/home/raven/work/asan-linux-debug-1088129/libcontent.so+0xea6a8ad)
#12 0x7f066f30153e (/home/raven/work/asan-linux-debug-1088129/libcontent.so+0xea6a53d)
#13 0x7f066f301399 (/home/raven/work/asan-linux-debug-1088129/libcontent.so+0xea6a398)
#14 0x7f067581fa0a (/home/raven/work/asan-linux-debug-1088129/libbase.so+0x51aa09)
#15 0x7f0675e41484 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xb3c483)
#16 0x7f0675f42d96 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xc3dd95)
#17 0x7f0675f421b7 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xc3d1b6)
#18 0x7f0675f3ff28 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xc3af27)
#19 0x7f0675f42913 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xc3d912)
#20 0x7f0675a729d9 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0x76d9d8)
#21 0x7f0675f4418a (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xc3f189)
#22 0x7f0675f44462 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xc3f461)
#23 0x7f0675ca0a1d (/home/raven/work/asan-linux-debug-1088129/libbase.so+0x99ba1c)
#24 0x7f05b727ca7a (/home/raven/work/asan-linux-debug-1088129/libblink_platform.so+0x4dcca79)
#25 0x7f067609d874 (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xd98873)
#26 0x7f067623176c (/home/raven/work/asan-linux-debug-1088129/libbase.so+0xf2c76b)
#27 0x7f05908e1609 (/usr/lib/x86_64-linux-gnu/libpthread-2.31.so+0x8608)
#28 0x7f058ff98163 (/usr/lib/x86_64-linux-gnu/libc-2.31.so+0x11f162)
Task trace:
#0 0x7f066f2ee195 (/home/raven/work/asan-linux-debug-1088129/libcontent.so+0xea57194)
#1 0x7f066002e79d (/home/raven/work/asan-linux-debug-1088129/libmojo_public_system_cpp.so+0x7b79c)
#2 0x7f066002e79d (/home/raven/work/asan-linux-debug-1088129/libmojo_public_system_cpp.so+0x7b79c)
#3 0x7f05cb2831ca (/home/raven/work/asan-linux-debug-1088129/libblink_core.so+0xbcec1c9)
#4 0x7f06600332ff (/home/raven/work/asan-linux-debug-1088129/libmojo_public_system_cpp.so+0x802fe)
```


### wx...@gmail.com (2023-01-03)

the bug reason 

```
ServiceWorkerGlobalScope::FetchHandlerType() {
  EventListenerVector* elv = GetEventListeners(event_type_names::kFetch);
  if (!elv) {
    return mojom::blink::ServiceWorkerFetchHandlerType::kNoHandler;
  }
  v8::Isolate* isolate = GetIsolate();
  v8::HandleScope handle_scope(isolate);
  // TODO(crbug.com/1349613): revisit the way to implement this.
  // The following code returns kEmptyFetchHandler if all handlers are nop.
  for (RegisteredEventListener& e : *elv) {
    EventTarget* et = EventTarget::Create(ScriptController()->GetScriptState());
    v8::Local<v8::Value> v =
        To<JSBasedEventListener>(e.Callback())->GetEffectiveFunction(*et);  // here will enter JSEventListener::GetEffectiveFunction maybe return js undefined
   
    // here not check the type of v, and cast it to v8::function, will cause the type confusion.
    if (!v.As<v8::Function>()->Experimental_IsNopFunction()) {
      return mojom::blink::ServiceWorkerFetchHandlerType::kNotSkippable;
    }
  }
  return mojom::blink::ServiceWorkerFetchHandlerType::kEmptyFetchHandler;
}
```

### wx...@gmail.com (2023-01-03)

here is the suggest patch

### da...@chromium.org (2023-01-03)

Thanks for the report.



Looks like we don't enable V8_ENABLE_CHECKS in production which means that .As<v8::Function>() does not check when doing the cast.
https://source.chromium.org/chromium/chromium/src/+/main:v8/BUILD.gn;l=141?ss=chromium%2Fchromium%2Fsrc&q=v8_enable_v8_checks

Here's where GetEffectiveFunction can return Undefined: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/js_event_handler.cc;l=28-33;drc=7e7414b2ce1f1ccb9e8b5ba578528d97abd6c6ad;bpv=1;bpt=1

The type confusion seems to be limited to Undefined, not arbitrary v8 objects.

The code was introduced in https://chromium-review.googlesource.com/c/chromium/src/+/3805086 with the ability to confuse the types. JSEventHandler::GetEffectiveFunction() hasn't changed in > 5 years. => FoundIn 106.0.5229.0

[Monorail components: Blink>ServiceWorker]

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2023-01-04)

[Empty comment from Monorail migration]

### yy...@chromium.org (2023-01-05)

Thanks for the report.  The patch in https://crbug.com/chromium/1404639#c04 looks good to me.


### yy...@chromium.org (2023-01-05)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-05)

LGTM

### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f68e9991d68d7ee36eb679cf5ffec06ab89569ac

commit f68e9991d68d7ee36eb679cf5ffec06ab89569ac
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Fri Jan 06 07:11:54 2023

Ensure v8::Value type is v8::Function in FetchHandlerType().

In the previous code, we did not confirm the returned v8::Value is
v8::Function or not in ServiceWorkerGlobalScope::FetchHandlerType().
If non function type is set as an fetch event listener, it causes
misbehavior.

Bug: 1404639
Change-Id: I7bc32f91108b2ffd3c5e8dc0464f2fa4adc41e8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4137870
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089635}

[modify] https://crrev.com/f68e9991d68d7ee36eb679cf5ffec06ab89569ac/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/f68e9991d68d7ee36eb679cf5ffec06ab89569ac/content/test/data/service_worker/non_function_fetch_event.js
[modify] https://crrev.com/f68e9991d68d7ee36eb679cf5ffec06ab89569ac/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### yy...@chromium.org (2023-01-06)

I will revisit this when the code goes to canary.

### [Deleted User] (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

Requesting merge to beta M109 because latest trunk commit (1089635) appears to be after beta branch point (1070088).

Requesting merge to dev M110 because latest trunk commit (1089635) appears to be after dev branch point (1084008).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-07)

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-07)

Merge review required: M109 has already been cut for stable release.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yy...@chromium.org (2023-01-10)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It is a security issue, which is marked Severity-Medium by Danak in https://crbug.com/chromium/1404639#c05.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4137870

3. Have the changes been released and tested on canary?

I think so.
https://chromium.googlesource.com/chromium/src/+log/111.0.5523.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.  This is a fix.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

I am not sure if it is a major issue, but the users can easily hit this issue with the way explained in https://crbug.com/chromium/1404639#c02 and crash the renderer at least.

### [Deleted User] (2023-01-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-11)

M109 merge approved, please merge this fix to branch 5414 at your earliest convenience (before 10am Friday, 20 January) so this fix can be included in the M109/Stable security refresh 
M108 merge approved, please merge this fix to branch 5359 so this fix can be included in the next M108/Extended security refresh. 

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations raven! The VRP Panel has decided to award you $7000 for this report + $500 patch bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1b03f77af5941c5a258d199f3d3d4846fdca353a

commit 1b03f77af5941c5a258d199f3d3d4846fdca353a
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Thu Jan 12 23:54:26 2023

Ensure v8::Value type is v8::Function in FetchHandlerType().

In the previous code, we did not confirm the returned v8::Value is
v8::Function or not in ServiceWorkerGlobalScope::FetchHandlerType().
If non function type is set as an fetch event listener, it causes
misbehavior.

(cherry picked from commit f68e9991d68d7ee36eb679cf5ffec06ab89569ac)

Bug: 1404639
Change-Id: I7bc32f91108b2ffd3c5e8dc0464f2fa4adc41e8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4137870
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1089635}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4159491
Reviewed-by: Minoru Chikamune <chikamune@chromium.org>
Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#1356}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/1b03f77af5941c5a258d199f3d3d4846fdca353a/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/1b03f77af5941c5a258d199f3d3d4846fdca353a/content/test/data/service_worker/non_function_fetch_event.js
[modify] https://crrev.com/1b03f77af5941c5a258d199f3d3d4846fdca353a/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ffe482466bb96b94b7fe9c2a5b35dff55f41e6c2

commit ffe482466bb96b94b7fe9c2a5b35dff55f41e6c2
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Fri Jan 13 00:14:55 2023

Ensure v8::Value type is v8::Function in FetchHandlerType().

In the previous code, we did not confirm the returned v8::Value is
v8::Function or not in ServiceWorkerGlobalScope::FetchHandlerType().
If non function type is set as an fetch event listener, it causes
misbehavior.

(cherry picked from commit f68e9991d68d7ee36eb679cf5ffec06ab89569ac)

Bug: 1404639
Change-Id: I7bc32f91108b2ffd3c5e8dc0464f2fa4adc41e8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4137870
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1089635}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4159531
Reviewed-by: Minoru Chikamune <chikamune@chromium.org>
Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1328}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/ffe482466bb96b94b7fe9c2a5b35dff55f41e6c2/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/ffe482466bb96b94b7fe9c2a5b35dff55f41e6c2/content/test/data/service_worker/non_function_fetch_event.js
[modify] https://crrev.com/ffe482466bb96b94b7fe9c2a5b35dff55f41e6c2/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b54c9142fedb84cb12b9d23880ce14a7c248bf6e

commit b54c9142fedb84cb12b9d23880ce14a7c248bf6e
Author: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Date: Fri Jan 13 00:31:28 2023

Ensure v8::Value type is v8::Function in FetchHandlerType().

In the previous code, we did not confirm the returned v8::Value is
v8::Function or not in ServiceWorkerGlobalScope::FetchHandlerType().
If non function type is set as an fetch event listener, it causes
misbehavior.

(cherry picked from commit f68e9991d68d7ee36eb679cf5ffec06ab89569ac)

Bug: 1404639
Change-Id: I7bc32f91108b2ffd3c5e8dc0464f2fa4adc41e8a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4137870
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1089635}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4151228
Reviewed-by: Minoru Chikamune <chikamune@chromium.org>
Auto-Submit: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#254}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/b54c9142fedb84cb12b9d23880ce14a7c248bf6e/content/browser/service_worker/service_worker_version_browsertest.cc
[add] https://crrev.com/b54c9142fedb84cb12b9d23880ce14a7c248bf6e/content/test/data/service_worker/non_function_fetch_event.js
[modify] https://crrev.com/b54c9142fedb84cb12b9d23880ce14a7c248bf6e/third_party/blink/renderer/modules/service_worker/service_worker_global_scope.cc


### yy...@chromium.org (2023-01-13)

Merge to M108, 109, and 110 has finished.  Please let me know if there is anything else I have to do.

### wx...@gmail.com (2023-01-13)

Cheers 😄

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1404639?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062472)*
