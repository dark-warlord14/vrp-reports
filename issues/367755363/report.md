# Security: heap-use-after-free in content::RenderFrameHostImpl::delegate

| Field | Value |
|-------|-------|
| **Issue ID** | [367755363](https://issues.chromium.org/issues/367755363) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Portals |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gl...@google.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2024-09-18 |
| **Bounty** | $36,000.00 |

## Description

# VULNERABILITY DETAILS

The `AIManager` mojo interface can be obtained by the renderer. When binding the receiver, the browser will save the corresponding context to the ReceiverSet [0].

```
void AIManagerKeyedService::AddReceiver(
    mojo::PendingReceiver<blink::mojom::AIManager> receiver,
    AIContextBoundObjectSet::ReceiverContext context) {
  receivers_.Add(this, std::move(receiver), context); // [0]
}

```

Type definition of context:

```
  using ReceiverContext =
      std::variant<content::RenderFrameHost*, base::SupportsUserData*>; // [1]

```

For requests sent from a regular frame, the context here is actually a raw pointer to `RenderFrameHost`.
However, there is no code that guarantees the consistency of the lifecycles of `AIManagerKeyedService` and the iframe. `AIManagerKeyedService` can completely outlive `RenderFrameHost`! If the iframe is removed before calling the functionality of `AIManagerKeyedService`, it will lead to a UAF.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_manager_keyed_service.cc;drc=8b00b43b06712a6c61f59f2e9f9230459d2a9025;l=308>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_context_bound_object_set.h;drc=8b00b43b06712a6c61f59f2e9f9230459d2a9025;l=27>

## **Vulnerability Trigger**

An attacker can trigger the UAF with the following steps:

1. Bind the `AIManager` interface in a child frame.
2. Send this interface handle to the parent frame.
3. Remove the child frame from the parent frame.
4. Trigger an IPC call to `AIManager` that uses the already freed `RenderFrameHost` object.

Our provided POC demonstrates these steps in detail. Please refer to the code for specifics.

## **Exploitability Analysis**

We note that this UAF is not yet protected by MiraclePtr (for details, see asan.txt):

```
MiraclePtr Status: NOT PROTECTED

```

RenderFrameHost UAF is a known vulnerability pattern that is frequently exploited to achieve sandbox escape. For specific examples, refer to [case 1](https://issues.chromium.org/issues/40057346) and [case 2](https://blog.theori.io/cleanly-escaping-the-chrome-sandbox-1c38abd3c9cb).

At least on Windows, using our provided POC, it's easy to achieve full control of `RenderFrameHost`. Below is the crash site displayed by windbg; for a detailed backtrace, see windbg.txt.

```
0:046> g
(3578.20cc): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for C:\Users\dalao\AppData\Local\Chromium\Application\130.0.6712.0\base.dll
base!absl::container_internal::raw_hash_set<absl::container_internal::FlatHashMapPolicy<const void *,std::__Cr::unique_ptr<base::SupportsUserData::Data,std::__Cr::default_delete<base::SupportsUserData::Data> > >,absl::container_internal::HashEq<const void *,void>::Hash,absl::container_internal::HashEq<const void *,void>::Eq,std::__Cr::allocator<std::__Cr::pair<const void *const,std::__Cr::unique_ptr<base::SupportsUserData::Data,std::__Cr::default_delete<base::SupportsUserData::Data> > > > >::fits_in_soo [inlined in base!absl::container_internal::raw_hash_set<absl::container_internal::FlatHashMapPolicy<const void *,std::__Cr::unique_ptr<base::SupportsUserData::Data,std::__Cr::default_delete<base::SupportsUserData::Data> > >,absl::container_internal::HashEq<const void *,void>::Hash,absl::container_internal::HashEq<const void *,void>::Eq,std::__Cr::allocator<std::__Cr::pair<const void *const,std::__Cr::unique_ptr<base::SupportsUserData::Data,std::__Cr::default_delete<base::SupportsUserData::Data> > > > >::find<const void *>+0x23]:
00007ffd`5e3fb0c3 48833901        cmp     qword ptr [rcx],1 ds:41414141`41414141=????????????????

```

We believe this vulnerability has extremely high exploitability, is stable, and easy to trigger. We recommend that the Chrome team fix it promptly.

# BISECTION

Introduced by <https://chromium.googlesource.com/chromium/src/+/d37f2ff9881443eca070192a005b9853e8a3bf74>

# VERSION

Chrome Version: 130.0.6712.0, HEAD + stable

Operating System: All

# REPRODUCTION CASE

Host poc files on an HTTP server.

```
$ python copy_mojo_js_bindings.py
$ python -m http.server
$ ./chrome --enable-blink-features=MojoJS,MojoJSTest 'http://localhost:8000/poc.html'

```
# CRASH INFORMATION

Type of crash: browser

Crash log: see asan.txt and windbg.txt

# CREDIT INFORMATION

Reporter credit: DARKNAVY(@DarkNavyOrg)

## Attachments

- [crash.txt](attachments/crash.txt) (text/plain, 27.3 KB)
- [windbg.txt](attachments/windbg.txt) (text/plain, 10.4 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/x-python, 653 B)
- [poc.zip](attachments/poc.zip) (application/zip, 2.8 KB)
- [child.html](attachments/child.html) (text/html, 308 B)
- [poc.html](attachments/poc.html) (text/html, 514 B)
- [poc.js](attachments/poc.js) (text/javascript, 1.4 KB)
- [utils.js](attachments/utils.js) (text/javascript, 2.7 KB)

## Timeline

### ma...@google.com (2024-09-18)

@Reporter, thank you for the detailed report. Could you please attach the PoC in an non-archive format? Otherwise we can't process it. Thank you!

The issue was introduced in [d37f2ff9881443eca070192a005b9853e8a3bf74](https://chromiumdash.appspot.com/commit/d37f2ff9881443eca070192a005b9853e8a3bf74), which landed in M129. It was then [reverted](https://chromiumdash.appspot.com/commit/5b766167b8e7400af24c27120960417f5936f2f4), but the revert is only in M130 and doesn't seem to have been cherry-picked to 130. So M129 would continue to be vulnerable.

There also is an M130 [reland](https://chromiumdash.appspot.com/commit/ca4b05d37bde39e1835ddc668dcf1e36d9d12b3f), which at a first glance I assume mitigates the issue by making the `ReceiverContext` pointer types `raw_ref`s instead.

(@Reporter, could you confirm whether you also believe HEAD to be vulnerable beyond the M130 reland commit? 130.0.6712.0 is before the original revert even, but your report makes the claim that HEAD is affected also.)

High/S1 for browser UAF preconditioned on a renderer compromise.

leimy@, could you PTAL? It looks like we would probably want to merge that rollback to M129 at least.

### vu...@darknavy.com (2024-09-19)

Uploaded the POC files, please take a look.

Regarding the version issue, my local build is based on commit ad7668b08d3fa13445049f0ec387419b077d8ede.

```
commit ad7668b08d3fa13445049f0ec387419b077d8ede (HEAD -> main, origin/main, origin/HEAD)
Author: CJ Huang <chenjih@google.com>
Date:   Wed Sep 11 10:27:19 2024 +0000

```

The stacktraces on both Linux and Windows were obtained from this version, and 130.0.6712.0 was retrieved from the UI.

### vu...@darknavy.com (2024-09-19)

The `raw_ref` of `ReceiverContext` is only used in the class `CreateContextBoundObjectTask`, but when stored in `AIManagerKeyedService`, it still uses the raw pointer of the context [0]

```
  receivers_.Add(this, std::move(receiver), context); // [0]

```

At the point where the UAF is triggered [1], raw pointer of the context is used.

```
void AIManagerKeyedService::CreateTextSession(
    mojo::PendingReceiver<blink::mojom::AITextSession> receiver,
    blink::mojom::AITextSessionSamplingParamsPtr sampling_params,
    const std::optional<std::string>& system_prompt,
    CreateTextSessionCallback callback) {
  // Since this is a mojo IPC implementation, the context should be non-null;
  AIContextBoundObjectSet* context_bound_object_set =
      AIContextBoundObjectSet::GetFromContext(receivers_.current_context()); // [1]

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_manager_keyed_service.cc;drc=8e948282d37c0e119e3102236878d6f4d5052c16;l=307>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ai/ai_manager_keyed_service.cc;drc=8e948282d37c0e119e3102236878d6f4d5052c16;l=366>

### pe...@google.com (2024-09-19)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-09-30)

Project: chromium/src  

Branch: main  

Author: Mingyu Lei <[leimy@chromium.org](mailto:leimy@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5872369>

Clear AIManager receiver when the context is destroyed

---


Expand for full commit details
```
Clear AIManager receiver when the context is destroyed

This CL puts an `AIManagerReceiverRemover` in the
`AIContextBoundObjectSet`, and it removes the receiver from the set
when the context is destroyed.

This ensures the receiver and the connection never outlives the
RenderFrameHost or the WorkerHosts, so it's not possible to have them used after freed.

Since the `AIContextBoundObjectSet` will always contain at least the
remover, the `OnAllContextBoundObjectsRemoved()` method is removed,
and the tests are updated accordingly.

Bug: 367755363
Change-Id: I2729b7f581c3f276473cfd56331a47efede35527
Validate-Test-Flakiness: skip
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5872369
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Mingyu Lei <leimy@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1361672}

```

---

Files:

- M `chrome/browser/ai/ai_context_bound_object.h`
- M `chrome/browser/ai/ai_context_bound_object_set.cc`
- M `chrome/browser/ai/ai_context_bound_object_set.h`
- M `chrome/browser/ai/ai_manager_keyed_service.cc`
- M `chrome/browser/ai/ai_manager_keyed_service.h`
- M `chrome/browser/ai/ai_manager_keyed_service_unittest.cc`
- M `chrome/browser/ai/ai_summarizer_unittest.cc`
- M `chrome/browser/ai/ai_test_utils.cc`
- M `chrome/browser/ai/ai_test_utils.h`

---

Hash: 1a751d5120b0642391bceaf68795fa55f0043698  

Date:  Mon Sep 30 06:10:52 2024


---

### le...@google.com (2024-10-01)

A temporary fix has been submitted to solve the issue, it should be part of M131. It clears the entry from the ReceiverSet so there is no dangling raw pointers to the RenderFrameHost any more.

I tested this with the poc provided by the reporter and the UAF should be resolved. However, I'm wondering if this kind of attack will work without MojoJS. If the AIAssistant object is created via the JS constructor from the child frame, and moved to the parent frame. It will fail the validity check of ScriptState after the child frame is destroyed. So it won't have a chance to talk to the browser and hit the freed RFH raw pointer.

martinkr@ is it still recommended to cherry pick this fix back to M130?

### el...@chromium.org (2024-10-01)

Security shepherd: I'm not martinkr@, but I think we should merge this Pri-1 Sev-1 security bug fix to M130 if this code is reachable in M130.

### pe...@google.com (2024-10-02)

Merge review required: M130 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### le...@google.com (2024-10-02)

Thanks, I have added the merge-request: 130 label.

Also since this vulnerability was introduced in M129, do we need to consider merging to there as well?

### le...@google.com (2024-10-02)

For the merge request question:

Why does your merge fit within the merge criteria for these milestones?

- It's a security bug that may lead to use-after-free of RFH raw pointers.

What changes specifically would you like to merge? Please link to Gerrit.

- <https://chromium-review.googlesource.com/c/chromium/src/+/5872369>

Have the changes been released and tested on canary?

- Yes

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

- No

If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

- I have manually tested it, but it would be great if the security people can help to verify as well.

### am...@chromium.org (2024-10-02)

Hi, thanks for addressing this issue. In the future, for security issues, please simply close the bug as Fixed. Blintz bot will update the bug with the appropriate merge review tags based on foundin, security impact, and severity. [1]
Yes, since this issue was introduced in M129 and there are over two weeks left of M129 as Stable, this should be reviewed for backmerge to M129 as well.

[1] <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#Security-merge-triage>

### am...@chromium.org (2024-10-02)

<https://crrev.com/c/5872369> has been on canary since four almost four days and there don't appear to be any stability or other issues presented
approved for merge to M130 and M129
please complete these merges to M130 Beta / branch 6723 and M129 Stable / branch 6668 by EOD tomorrow / Thursday 3 October so this fix can be included into next week's updates

### da...@google.com (2024-10-03)

Your change has been approved. We will be taking M130 Beta RC cut tonight. Please land your changes before 5:30PM PST.

### pe...@google.com (2024-10-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@chromium.org (2024-10-07)

per discussion wiht amy@ and security team we have decided its ok to merge this to m130 and not to 129 respin this week ( as there are merge conflicts when we tried to CP) ,so please complete your merges before 10am PST Oct 8 so it can go in m130 release. 



### ap...@google.com (2024-10-08)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Mingyu Lei <[leimy@chromium.org](mailto:leimy@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5914072>

[M130] Clear AIManager receiver when the context is destroyed

---


Expand for full commit details
```
[M130] Clear AIManager receiver when the context is destroyed

This CL puts an `AIManagerReceiverRemover` in the
`AIContextBoundObjectSet`, and it removes the receiver from the set
when the context is destroyed.

This ensures the receiver and the connection never outlives the
RenderFrameHost or the WorkerHosts, so it's not possible to have them used after freed.

Since the `AIContextBoundObjectSet` will always contain at least the
remover, the `OnAllContextBoundObjectsRemoved()` method is removed,
and the tests are updated accordingly.

(cherry picked from commit 1a751d5120b0642391bceaf68795fa55f0043698)

Bug: 367755363
Change-Id: I2729b7f581c3f276473cfd56331a47efede35527
Validate-Test-Flakiness: skip
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5872369
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Mingyu Lei <leimy@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1361672}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5914072
Auto-Submit: Mingyu Lei <leimy@chromium.org>
Cr-Commit-Position: refs/branch-heads/6723@{#1086}
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `chrome/browser/ai/ai_context_bound_object.h`
- M `chrome/browser/ai/ai_context_bound_object_set.cc`
- M `chrome/browser/ai/ai_context_bound_object_set.h`
- M `chrome/browser/ai/ai_manager_keyed_service.cc`
- M `chrome/browser/ai/ai_manager_keyed_service.h`
- M `chrome/browser/ai/ai_manager_keyed_service_unittest.cc`
- M `chrome/browser/ai/ai_summarizer_unittest.cc`
- M `chrome/browser/ai/ai_test_utils.cc`
- M `chrome/browser/ai/ai_test_utils.h`

---

Hash: 2fe3360d38513037cbd277f9609e94c49217accb  

Date:  Tue Oct 08 06:05:42 2024


---

### pe...@google.com (2024-10-08)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2024-10-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
$35,000 for high quality report of memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-09)

Congratulations darknavy! Thank you for your efforts and reporting this issue to us -- great work!

### rz...@google.com (2024-10-10)

Labelling as not applicable for 126 LTS because the affected code isn't present in the branch.

### pe...@google.com (2025-01-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $35,000 for high quality report of memory corruption in a non-sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/367755363)*
