# Missing return after ShutdownForBadMessage in SimpleDevToolsProtocolClient leads to past-end OOB read in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [504156069](https://issues.chromium.org/issues/504156069) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Browser Automation>Headless |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | kv...@google.com |
| **Created** | 2026-04-19 |
| **Bounty** | $3,000.00 |

## Description

# Missing return after ShutdownForBadMessage in SimpleDevToolsProtocolClient leads to past-end OOB read in the browser process

## Summary

A missing `return` statement after `ShutdownForBadMessage` in `SimpleDevToolsProtocolClient::DispatchProtocolMessageTask` allows a compromised renderer to trigger an out-of-bounds read on the browser process main thread. When the client receives a DevTools message whose JSON `id` field does not match any pending callback, it correctly identifies the situation as a bad message but fails to stop execution, falling through to dereference a past-end iterator on the `pending_response_map_` flat\_map. Because `ShutdownForBadMessage` only asynchronously terminates the renderer and does not halt the calling function, the subsequent `std::move(it->second)` reads memory beyond the backing vector of the map. The bug is reachable from a compromised renderer attached via DevTools in headless command mode (`--dump-dom`, `--screenshot`, or `--print-to-pdf`) on all desktop platforms. No GPU is required.

## Bisect

Introducing Commit: `0394e41d758adca1673f2e9aa7f13bc18cbc1b5d`

- Date: 2022-10-25
- Author: Peter Kvitek
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/3943190>

The vulnerable code has been present since the file was first added and has never been corrected.

## Root Cause

The DevTools protocol stack validates responses at two separate layers using two independent identifiers. When the browser dispatches a command to a renderer, `DevToolsSession` tracks the command by its Mojo `call_id` in `waiting_for_response_`. Independently, `SimpleDevToolsProtocolClient` tracks the same command by the JSON `id` it placed in the protocol message, storing the callback in `pending_response_map_`. Responses returning from the renderer pass through `DevToolsSession::DispatchProtocolResponse`, which checks only the Mojo `call_id`, then forwards the opaque message body to the client. The client then extracts the JSON `id` and looks it up in its own map.

When the JSON `id` is not found, `DispatchProtocolMessageTask` enters the error branch, calls `ShutdownForBadMessage`, but does not return:

```
// components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc
void SimpleDevToolsProtocolClient::DispatchProtocolMessageTask(
    base::DictValue message) {
  if (std::optional<int> id = message.FindInt(kId)) {
    auto it = pending_response_map_.find(*id);
    if (it == pending_response_map_.cend()) {
      LOG(ERROR) << "Unexpected message id=" << *id;
      agent_host_->GetProcessHost()->ShutdownForBadMessage(
          content::RenderProcessHost::CrashReportMode::GENERATE_CRASH_DUMP);
      // No return here. Execution continues.
    }
    ResponseCallback callback(std::move(it->second));   // OOB read
    pending_response_map_.erase(it);                     // CHECK crash
    std::move(callback).Run(std::move(message));
    return;
  }
  // ...
}

```

`ShutdownForBadMessage` sends a termination signal to the renderer process and returns immediately; it does not terminate the current function, halt the browser thread, or throw. Control proceeds to `std::move(it->second)` with `it` still pointing to `cend()`. Because `pending_response_map_` is a `base::flat_map` backed by a sorted `std::vector`, dereferencing `cend()` performs a read past the end of the vector's storage. The `flat_tree::erase` method that follows does contain `CHECK(position != body_.end())`, but this fires only after the memory safety violation has already occurred.

A compromised renderer can reach this code without needing to guess valid Mojo `call_id` values. The renderer holds a `DevToolsSessionHost` remote and can call `DispatchProtocolNotification` at any time. Unlike `DispatchProtocolResponse`, which validates the `call_id` against `waiting_for_response_` before forwarding, `DispatchProtocolNotification` applies no such check:

```
// content/browser/devtools/devtools_session.cc
void DevToolsSession::DispatchProtocolNotification(
    blink::mojom::DevToolsMessagePtr message,
    blink::mojom::DevToolsSessionStatePtr updates) {
  ApplySessionStateUpdates(std::move(updates));
  DispatchProtocolResponseOrNotification(client_, agent_host_,
                                         std::move(message));
}

```

It forwards the opaque message directly to `client_->DispatchProtocolMessage`. If the message contains an `id` field, `SimpleDevToolsProtocolClient` treats it as a response and enters the vulnerable lookup path. The renderer can therefore inject `{"id":99999,"result":{}}` as a notification, bypassing all transport-level validation, and trigger the OOB read in the browser process.

The attack surface is headless command mode. `SimpleDevToolsProtocolClient` is only instantiated by `HeadlessCommandHandler`, which is created when Chrome is launched with `--dump-dom`, `--screenshot`, or `--print-to-pdf`. These headless command-line flags see significant real-world adoption. The Chrome for Developers documentation promotes them as the primary built-in headless features. Docker images packaging headless Chrome for server-side use have accumulated substantial pull counts (zenika/alpine-chrome over 10 million pulls, browserless/chrome over 100 million pulls). The PHP package spatie/browsershot, whose v2 invoked the Chrome headless CLI directly, has over 32 million Packagist installs. Projects such as chromehtml2pdf position themselves as drop-in replacements for wkhtmltopdf using `--print-to-pdf`, and the official Chrome blog recommends `--dump-dom` as a zero-code server-side rendering solution (<https://developer.chrome.com/blog/headless-chrome-ssr-js-sites>). These flags are commonly used in CI pipelines, lightweight PDF generation services, and shell-based web scraping workflows where the target URL is attacker-controlled.

## Reproduce

The vulnerability is platform-independent. The reproduction below uses Linux paths.

Apply the renderer-side patch that simulates a compromised renderer forging a DevTools notification with a mismatched id field.

```
cd ~/chromium/src
git apply issue_devtools_oob/patch.diff

```

Configure the ASAN build with the following `out/asan-release/args.gn`. If the build directory already exists with a suitable ASAN configuration, this step can be skipped.

```
is_asan = true
is_debug = false
is_component_build = true

```

Build Chrome.

```
autoninja -C out/asan-release chrome

```

Launch headless Chrome in dump-dom mode, pointing at the included PoC page or any URL.

```
ASAN_OPTIONS=detect_odr_violation=0 out/asan-release/chrome --headless --dump-dom issue_devtools_oob/poc.html

```

The patched renderer sends a forged `DispatchProtocolNotification` carrying `{"id":99999,"result":{}}` to the browser process. When `SimpleDevToolsProtocolClient::DispatchProtocolMessageTask` receives this message, it looks up id 99999 in its `pending_response_map_`, gets `cend()`, calls `ShutdownForBadMessage` without returning, and falls through to dereference the past-end iterator. ASAN reports a container-overflow READ of size 8 on the browser main thread (T0) and aborts. The full ASAN trace is in `asan.log`.

After verification, revert the patch with `git checkout -- .` to restore the tree to a clean state.

ASAN output:

```
==82459==ERROR: AddressSanitizer: container-overflow on address 0x7bc6485a1d78 at pc 0x555bcf39ef97 bp 0x7ffd1f229930 sp 0x7ffd1f229928
READ of size 8 at 0x7bc6485a1d78 thread T0 (chrome)
    #0 0x555bcf39ef96 in simple_devtools_protocol_client::SimpleDevToolsProtocolClient::DispatchProtocolMessageTask(base::DictValue) base/memory/scoped_refptr.h:264:54
    #1 0x555bcf3a10e7 in base::internal::Invoker<...>::RunImpl<...> base/functional/bind_internal.h:740:12
    #2 0x7f96ccb61b59 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #3 0x7f96ccbdc1d0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #4 0x7f96ccbdb1a6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:40
    #5 0x7f96ccdb41c9 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #6 0x7f96ccbdd823 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:640:12
    #7 0x7f96ccaccc72 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #8 0x7f96adee7d03 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1103:18
    #9 0x7f96adeeff76 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15
    #10 0x7f96adedf1b5 in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #11 0x7f96b13bf745 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:696:10
    #12 0x7f96b13c2e6d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1320:10
    #13 0x7f96b13c23c6 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:12
    #14 0x7f96b13bcae3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:356:36
    #15 0x7f96b13bce6a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:369:10
    #16 0x555bc1218215 in ChromeMain chrome/app/chrome_main.cc:194:12
    #17 0x7f9656e29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

0x7bc6485a1d78 is located 8 bytes inside of 32-byte region [0x7bc6485a1d70,0x7bc6485a1d90)
allocated by thread T0 (chrome) here:
    #0 0x555bc12162bd in operator new(unsigned long)
    #1 0x555bcf3a2431 in std::__Cr::vector<std::__Cr::pair<int, base::OnceCallback<void (base::DictValue)>>>::emplace<...>
    #2 0x555bcf3a2029 in simple_devtools_protocol_client::SimpleDevToolsProtocolClient::SendCommand(...) components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc:212:30
    #3 0x7f96acfbf225 in headless::HeadlessCommandHandler::OnDevToolsProtocolExposed() components/headless/command_handler/headless_command_handler.cc:384:3
    #4 0x7f96acfc1a23 in base::internal::Invoker<...>::RunOnce(...) base/functional/bind_internal.h:740:12
    #5 0x555bcf39dc6e in simple_devtools_protocol_client::SimpleDevToolsProtocolClient::DispatchProtocolMessage(...) components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc:113:7

SUMMARY: AddressSanitizer: container-overflow base/memory/scoped_refptr.h:264:54 in simple_devtools_protocol_client::SimpleDevToolsProtocolClient::DispatchProtocolMessageTask(base::DictValue)

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 305 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 2.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 11.0 KB)

## Timeline

### me...@google.com (2026-04-20)

Thanks for the report.

kvitekp@: Could you PTAL?

### ch...@google.com (2026-04-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-21)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-21)

Project: chromium/src  

Branch:  main  

Author:  Peter Kvitek [kvitekp@chromium.org](mailto:kvitekp@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7779642>

[DevTools] Fix missing return in SimpleDevToolsProtocolClient

---


Expand for full commit details
```
     
    Bug: 504156069 
    Change-Id: I3da05ff017148775cf0cdf7a427233d3792ced2d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7779642 
    Auto-Submit: Peter Kvitek <kvitekp@chromium.org> 
    Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    Commit-Queue: Peter Kvitek <kvitekp@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1618241}

```

---

Files:

- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc`
- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc`

---

Hash: [2b6338737f6c5062ecb7d70d7b9676fe2a678e1d](https://chromiumdash.appspot.com/commit/2b6338737f6c5062ecb7d70d7b9676fe2a678e1d)  

Date: Tue Apr 21 16:18:49 2026


---

### ch...@google.com (2026-04-22)

Requesting merge to M146 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit is in 149.

Requesting merge to M148 because latest trunk commit is in 149.

### ch...@google.com (2026-04-22)

**M146** merge request created. **Please update [crbug/505251515](https://crbug.com/505251515) to have this merge reviewed.**

### ch...@google.com (2026-04-22)

**M147** merge request created. **Please update [crbug/505252136](https://crbug.com/505252136) to have this merge reviewed.**

### ch...@google.com (2026-04-22)

**M148** merge request created. **Please update [crbug/505252155](https://crbug.com/505252155) to have this merge reviewed.**

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
moderately mitigated browser memory corruption


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Peter Kvitek [kvitekp@chromium.org](mailto:kvitekp@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7850910>

[M148] [DevTools] Fix missing return in SimpleDevToolsProtocolClient

---


Expand for full commit details
```
     
    Original change's description: 
    > [DevTools] Fix missing return in SimpleDevToolsProtocolClient 
    > 
    > Bug: 504156069 
    > Change-Id: I3da05ff017148775cf0cdf7a427233d3792ced2d 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7779642 
    > Auto-Submit: Peter Kvitek <kvitekp@chromium.org> 
    > Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    > Commit-Queue: Peter Kvitek <kvitekp@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1618241} 
     
    (cherry picked from commit 2b6338737f6c5062ecb7d70d7b9676fe2a678e1d) 
     
    Bug: 505252155,504156069 
    Change-Id: I3da05ff017148775cf0cdf7a427233d3792ced2d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7850910 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Alex N. Jose <alexnj@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3251} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc`
- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc`

---

Hash: [ab8b2fa9a53b23038d3966333b5c6bb5a54b7beb](https://chromiumdash.appspot.com/commit/ab8b2fa9a53b23038d3966333b5c6bb5a54b7beb)  

Date: Tue May 19 17:42:55 2026


---

### pe...@google.com (2026-05-19)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Peter Kvitek [kvitekp@chromium.org](mailto:kvitekp@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7850911>

[M147] [DevTools] Fix missing return in SimpleDevToolsProtocolClient

---


Expand for full commit details
```
     
    Original change's description: 
    > [DevTools] Fix missing return in SimpleDevToolsProtocolClient 
    > 
    > Bug: 504156069 
    > Change-Id: I3da05ff017148775cf0cdf7a427233d3792ced2d 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7779642 
    > Auto-Submit: Peter Kvitek <kvitekp@chromium.org> 
    > Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    > Commit-Queue: Peter Kvitek <kvitekp@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1618241} 
     
    (cherry picked from commit 2b6338737f6c5062ecb7d70d7b9676fe2a678e1d) 
     
    Bug: 505252136,504156069 
    Change-Id: I3da05ff017148775cf0cdf7a427233d3792ced2d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7850911 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Alex N. Jose <alexnj@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#4449} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc`
- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client_unittest.cc`

---

Hash: [5aeb143b88544545b99f44a9d7c9b3b86f843e02](https://chromiumdash.appspot.com/commit/5aeb143b88544545b99f44a9d7c9b3b86f843e02)  

Date: Tue May 19 18:13:21 2026


---

### kv...@google.com (2026-05-29)

This change affects SimpleDevToolsProtocolClient which in production is only used for Headless Chrome command line commands (--dump-dom, --screenshot and --print-to-pdf) implementation. Headless Chrome is not supported on Chrome OS, so there is no need to merge it there.

### qk...@google.com (2026-06-09)

Add LTS-NotApplicable-144 label according to the comment #14.

### ch...@google.com (2026-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504156069)*
