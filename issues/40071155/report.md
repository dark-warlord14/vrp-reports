# UAF in v8_inspector DomainDispatcherImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40071155](https://issues.chromium.org/issues/40071155) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2023-09-01 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

will attach details soon.

**Problem Description:**  

renderer UAF

**Additional Comments:**

\*\*Chrome version: \*\* 118.0.5979.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 33.0 KB)
- [background.js](attachments/background.js) (text/plain, 55 B)
- [manifest.json](attachments/manifest.json) (text/plain, 205 B)
- [poc.html](attachments/poc.html) (text/plain, 61 B)
- [poc.js](attachments/poc.js) (text/plain, 184.0 KB)

## Timeline

### [Deleted User] (2023-09-01)

[Empty comment from Monorail migration]

### za...@chromium.org (2023-09-01)

Can you please upload a PoC? Thanks! 

### za...@chromium.org (2023-09-01)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-09-01)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-09-01)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-09-01)

[Empty comment from Monorail migration]

### cr...@google.com (2023-09-01)

https://crbug.com/chromium/1478242#c2: Was the "Hotlist-gTech-Source-Feedback" label added by mistake? If so, free to remove it (and me!) from this bug. If intentional, would you be able to share how our team (consumer support) may be able to assist? The hotlist triggered an alert on our end so just wanted to check-in. Thanks!

### za...@chromium.org (2023-09-01)

Sorry about the confusion, I was adding Needs-Feedback tag but the auto complete got messed up. I have removed you from cc list. 

### za...@chromium.org (2023-09-01)

 hedonistsmith@ Can you please provide more details. Thanks for reporting.

### he...@gmail.com (2023-09-02)

I've tried to minimize the PoC, but failed. But I think it might be helpful to debug the root cause since the PoC is stable.

A current stable reproduction method on 118.0.5979.0 Linux Chrome:

Load the attached PoC extension (no extra flag required), after the website popup, wait for some seconds and close the browser by ctrl+c.

### ke...@chromium.org (2023-09-06)

Thanks for the report.

I haven't been able to repro but the ASAN trace might be enough to go on.

This looks like an extension using the v8 inspector and inducing a UAF on receipt of a mojo message after a session has been destroyed.

Assigning to the v8 sheriff for triage.

[Monorail components: Blink>JavaScript]

### is...@chromium.org (2023-09-07)

Seems to be related to V8 inspector. Assigning to DevTools folks to find a better owner.

[Monorail components: -Blink>JavaScript Platform>DevTools>JavaScript]

### sz...@chromium.org (2023-09-07)

I'll be OOO next two weeks so assigning to Danil for now. I can take over afterwards in case it's needed.

### ds...@chromium.org (2023-09-14)

I can't reproduce this either

### he...@gmail.com (2023-09-14)

There might be a race between the blink::DevToolsSession::DispatchProtocolCommandImpl [1] (on InspectorTaskRunner) and blink::DevToolsSession::Detach [2] (on mojo_task_runner). When DevToolsSession::Detach (frees DevToolsSession) happens before DevToolsSession::DispatchProtocolCommand due to the different thread sequence they are running on, UAF happens on the freed DevToolsSession object.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/devtools_session.cc;l=111-117;drc=e672a665ffa8fe4901184f03922e2cc548399da5

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/devtools_session.cc;l=157-158;drc=31fb07c05718d671d96c227855bfe97af9e3fb20

### ds...@chromium.org (2023-09-14)

Andrey, wdyt?

### ca...@chromium.org (2023-09-14)

This reproduces well for me. I'm still trying to make sense of it, though, as a few things don't add up here.

Re https://crbug.com/chromium/1478242#c15, please note that [1] is a method of IOSession, which is not applicable to the crash at hands. We only dispatch few commands on the IO session, and the one in the crash is `Runtime.enable`.

The dump also clearly shows this is directly invoked by mojo, rather than being posted via `inspector_task_runner_`:

    #4 0x56501d9a90de in v8_crdtp::UberDispatcher::DispatchResult::Run() ./../../v8/third_party/inspector_protocol/crdtp/dispatch.cc:509:3
    #5 0x56501d92e609 in v8_inspector::V8InspectorSessionImpl::dispatchProtocolMessage(v8_inspector::StringView) ./../../v8/src/inspector/v8-inspector-session-impl.cc:407:39
    #6 0x5650359e0e0e in blink::DevToolsSession::DispatchProtocolCommandImpl(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul>) ./../../third_party/blink/renderer/core/inspector/de
vtools_session.cc:258:18
    #7 0x5650359e05bb in blink::DevToolsSession::DispatchProtocolCommand(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul>) ./../../third_party/blink/renderer/core/inspector/devtoo
ls_session.cc:228:10
    #8 0x565023e28f3e in blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession*, mojo::Message*) ./gen/third_party/blink/public/mojom/devtools/devtools_agent.mojom-blink.c
c:1318:13
    #9 0x56502a2050a4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54
    #10 0x56502a220a64 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19

Besides, `DevToolsSession::Detach()`, which is the only place that releases `v8_session_`, sets io_session_ to null before that, which would result in IsDetached() returning true, and thus us bailin out in [2]

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/devtools_session.cc;drc=8cc1a8043323107797090275c8239d6b89a508d1;l=29

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/devtools_session.cc;drc=31fb07c05718d671d96c227855bfe97af9e3fb20;l=251



### ca...@chromium.org (2023-09-18)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-09-18)

Ok, here's what happens, the session is torn down on nested message loop, while paused on breakpoint. The nested message loop occurs just within `V8RuntimeAgentImpl::enable()`, namely while running this line: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-runtime-agent-impl.cc;drc=a6bdc8f2993883fc55eb9cb0945694299b056675;l=1076

The client-side implementation is harmless at the first glance:

void MainThreadDebugger::beginEnsureAllContextsInGroup(int context_group_id) {
  LocalFrame* frame = WeakIdentifierMap<LocalFrame>::Lookup(context_group_id);
  frame->GetSettings()->SetForceMainWorldInitialization(true);
}

... but changing ForceMainWorldInitialization causes invalidation of DOM worlds: 
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/page/page.cc;drc=71d3885ad42265ebd0f9b09fa1eb074314f25123;l=760

Which re-enters v8 and may pause on a breakpoint.


### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-09-25)

caseq@ I'm assuming that this code hasn't changed lately and therefore that this isn't a recent regression. Labelling thusly but please let me know if I'm wrong!

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-09-26)

Yeah, this doesn't look like a recent regression to me. I'm not even sure if this can be reproduced programmatically without sending signals to browser (note PoC suggests using ctrl+c to terminate the browser). I haven't succeeded in reproducing this in a test, and my current theory that the order of disconnection of mojo pipes during process termination may be different from that of our manual teardown when a session is terminated. Also, this only crashes renderer which is already under control of the CDP client, so actual security impact is fairly limited.

FWIW, this is caused by `DevToolsSession::Detach()` being invoked on a nested message loop by mojo while handling pipe shutdown. In my tests this is always running _after_ the message loop exits (and is thus safe).

### he...@gmail.com (2023-10-18)

Hi team, any update? Thank you very much.

### bm...@chromium.org (2023-10-20)

This P1 issue has been open for more than 30 days and therefore violates the Chrome SLOs (go/chrome-slo) that P1s have to be fixed within 4 weeks.

Please take a look again and prioritize fixing this issue. If it turns out that the issue was marked as P1 incorrectly (or the conditions for the initial prioritization changed), please lower priority and provide an explanation.


### he...@gmail.com (2023-10-24)

friendly ping -

### he...@gmail.com (2023-11-28)

Hi caseq@, maybe we could store weak pointer in the local variable before enter the message loop [1] and check the weak pointer right after the message loop to avoid the UAF issue here.

[1]https://source.chromium.org/chromium/chromium/src/+/main:v8/src/inspector/v8-runtime-agent-impl.cc;drc=a6bdc8f2993883fc55eb9cb0945694299b056675;l=1076

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1478242?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### he...@gmail.com (2024-02-07)

friendly ping -

### pe...@google.com (2024-02-21)

caseq: Uh oh! This issue still open and hasn't been updated in the last 147 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### bm...@google.com (2024-02-22)

Simon, can you take a look please? In particular [comment #28](https://issues.chromium.org/issues/40071155#comment28) and [comment #20](https://issues.chromium.org/issues/40071155#comment20) already outline the solution.

### pe...@google.com (2024-02-22)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-03-28)

szuend: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sz...@google.com (2024-10-10)

I tried the weak pointer approach but it doesn't work with our current architecture. [comment#20](https://issues.chromium.org/issues/40071155#comment20) doesn't outline a solution, just documents the root cause.

Can we lower severity and priority of this bug since the repro requires forcefull termination via Ctrl+C?

### pg...@google.com (2024-10-10)

[secondary shepherd]

I believe the severity would have been set to medium because UAFs in the renderer processes are considered high severity (S1), but as this comes with the mitigation that this requires a forceful termination, and hence downgraded to medium (S2). I don't think a ctrl+c is a rare enough of an interaction to consider it more mitigated to downgrade to a low severity bug ([severity guidelines here](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md))

### sz...@google.com (2024-10-14)

As a mitigation we could ignore pauses coming during `Runtime.enable()`. I don't know what debugging workflows this would break. What kind of scripts are executed during `ForceMainWorldInitialization`? If it's just some obscure prototype hacks that would be fine, but if inline scripts / onload handlers are executed during `ForceMainWorldInitialization`, then we can't disable pauses.

### sz...@google.com (2024-10-15)

Does this still reproduce? I'm unable to get the same UaF. I don't manage to pause during `Runtime.enable` to trigger the nested message loop teardown.

### dx...@google.com (2025-04-15)

Project: v8/v8  

Branch: main  

Author: Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6433946>

[inspector] Add V8Inspector::connectShared

---


Expand for full commit details
```
     
    This CL adds a version of the 'connect' method that returns a shared_ptr 
    rather than a unique_ptr. 
     
    This allows us to defer deconstruction of V8InspectorSession objects. 
    We use this in "dispatchProtocolMessage" for now. 
     
    The main reason is that blink is allowed to tear down V8 sessions on 
    the nested run-loop, while actual agent/session functions remain on 
    the stack. This CL attempts to fix this in a more general way than 
    patching adhocs UaF. 
     
    Note that its not clear if this fixes all instances where the session 
    dies on the nested run loop: There are other entry points into 
    inspector agent code that can then transition into JS and then run 
    a nested event loop, e.g. client events or interrupts. 
     
    Bug: 40071155 
    Change-Id: I48f599cfcda2cf8ed71e3b865a6d2e71daa59061 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6433946 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#99784}

```

---

Files:

- M `include/v8-inspector.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-inspector-session-impl.h`
- M `test/inspector/isolate-data.cc`
- M `test/inspector/isolate-data.h`

---

Hash: 73b918cfcdb38b4472b118f00e5649309013b202  

Date:  Tue Apr 15 04:33:38 2025


---

### dx...@google.com (2025-04-23)

Project: chromium/src  

Branch: main  

Author: Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6478470>

[inspector] Use std::shared\_ptr for V8InspectorSession

---


Expand for full commit details
```
     
    This allows V8 to delay tearing down the V8InspectorSession instance in 
    case V8 session/agents are still on the stack during 
    DevToolsSession::Detach. 
     
    Bug: 40071155 
    Change-Id: I240e39d87a8c46e2978f4343b3a55fcfc54a607e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6478470 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1450809}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: 345c61f3a65a4d7a36166a049e8dbe0138dcb9da  

Date:  Wed Apr 23 21:27:32 2025


---

### ch...@google.com (2025-04-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-04-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2025-04-25)

Project: chromium/src  

Branch: main  

Author: [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6485822>

Revert "[inspector] Use std::shared\_ptr for V8InspectorSession"

---


Expand for full commit details
```
     
    This reverts commit 345c61f3a65a4d7a36166a049e8dbe0138dcb9da. 
     
    Reason for revert: 
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5090085084069888 
     
    Sample build with failed test: https://ci.chromium.org/b/8716738537424725073 
    Affected test(s): 
    [ninja://:blink_web_tests/http/tests/inspector-protocol/target/resume-on-close.js](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2F:blink_web_tests%2Fhttp%2Ftests%2Finspector-protocol%2Ftarget%2Fresume-on-close.js?q=VHash%3A9b30675a77baf900) 
     
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5090085084069888&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F6478470&type=BUG 
     
    Original change's description: 
    > [inspector] Use std::shared_ptr for V8InspectorSession 
    > 
    > This allows V8 to delay tearing down the V8InspectorSession instance in 
    > case V8 session/agents are still on the stack during 
    > DevToolsSession::Detach. 
    > 
    > Bug: 40071155 
    > Change-Id: I240e39d87a8c46e2978f4343b3a55fcfc54a607e 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6478470 
    > Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    > Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    > Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1450809} 
    > 
     
    Bug: 40071155 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I3f9c1bfffdc6084fb7df507bd617b5b922ef264d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6485822 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1451614}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: e5a4db27ff132c70d4f906480b6aef5d8748bea5  

Date:  Fri Apr 25 04:20:31 2025


---

### dx...@google.com (2025-12-08)

Project: chromium/src  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7232873>

Reland "[inspector] Use std::shared\_ptr for V8InspectorSession"

---


Expand for full commit details
```
     
    This is a reland of commit 345c61f3a65a4d7a36166a049e8dbe0138dcb9da 
     
    The reland fixes a chicken-egg problem: The V8InspectorSession 
    destructor resumes execution if the session is paused, but if we 
    delay V8InspectorSession destruction, we'll never resume, so the 
    stack will never be torn down. 
     
    The solution is to call `stop` explicitly when detaching from V8 
    in blink. This terminates the nested message loop, allows execution 
    to resumse, and once the stack is unwound, the V8InspectorSession 
    instance is cleaned up. 
     
    Original change's description: 
    > [inspector] Use std::shared_ptr for V8InspectorSession 
    > 
    > This allows V8 to delay tearing down the V8InspectorSession instance in 
    > case V8 session/agents are still on the stack during 
    > DevToolsSession::Detach. 
    > 
    > Bug: 40071155 
    > Change-Id: I240e39d87a8c46e2978f4343b3a55fcfc54a607e 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6478470 
    > Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    > Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    > Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1450809} 
     
    Fixed: 40071155 
    Change-Id: I5829f2e8484e5cb5130dca94e63c0c7e088b08e6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7232873 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1555687}

```

---

Files:

- M `PRESUBMIT.py`
- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [531984a74b5f6b72af0c8129507a6ec725f82193](https://chromiumdash.appspot.com/commit/531984a74b5f6b72af0c8129507a6ec725f82193)  

Date: Mon Dec 8 20:58:53 2025


---

### sp...@google.com (2025-12-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Highly mitigated code execution in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dr...@chromium.org (2026-01-09)

[security triage] Looks like our automation dropped the ball here, but since this is Medium severity we should consider this for a merge to M144. Manually doing the merge request now, and I'll review the fix shortly.

### dr...@chromium.org (2026-01-12)

On a further look, there's nothing to merge here. On the day this was fixed, our automation should have tagged this for a merge to M144 Beta. But today M144 has been cut for Stable and M145 is about to be in Beta. We don't merge Medium severity bugs into Stable, so we'll have to be content with this being fixed in M145.

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7585774>

[inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
    Change-Id: Ia6ecd31df995c358ea2fcc9f48f59cd3ee7ad4f3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7585774 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586235}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [7d8b22f0bcaa82823f31b8bd53e026a670c5a64f](https://chromiumdash.appspot.com/commit/7d8b22f0bcaa82823f31b8bd53e026a670c5a64f)  

Date: Wed Feb 18 07:08:16 2026


---

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7602272>

[M146] [inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
     
    (cherry picked from commit 7d8b22f0bcaa82823f31b8bd53e026a670c5a64f) 
     
    Change-Id: I9bded1b9d0ea491f146d9f83045cd396540aff54 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602272 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1207} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [2ea2412f22e4864badb0ba6b1072cf12879cdc8c](https://chromiumdash.appspot.com/commit/2ea2412f22e4864badb0ba6b1072cf12879cdc8c)  

Date: Tue Feb 24 10:25:59 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606141>

[M144] [inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
    (cherry picked from commit 7d8b22f0bcaa82823f31b8bd53e026a670c5a64f) 
     
    Change-Id: If97b600d695e066aacd283d92c7dba7ba1e112c6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606141 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4760} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [523d8b83478e992b99dcbfdf347e06e4e7ac9371](https://chromiumdash.appspot.com/commit/523d8b83478e992b99dcbfdf347e06e4e7ac9371)  

Date: Wed Feb 25 09:54:12 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7604098>

[M145] [inspector] Pass ManagedChannel when connecting to V8

---


Expand for full commit details
```
     
    This CL makes DevToolsSession inherit from V8Inspector::ManagedChannel. 
    This allows the V8 inspector to extend the life-time as needed, should 
    there still be CDP commands in-flight when the session detaches. 
     
    Bug: 40071155 
    Fixed: 483853098 
    (cherry picked from commit 7d8b22f0bcaa82823f31b8bd53e026a670c5a64f) 
     
    Change-Id: I46d2dd9b825865f223c2e891f21805884a1e6559 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7604098 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3355} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/devtools_session.cc`
- M `third_party/blink/renderer/core/inspector/devtools_session.h`

---

Hash: [a58cdac50a6fbaf631f03d0fc707339617c521a3](https://chromiumdash.appspot.com/commit/a58cdac50a6fbaf631f03d0fc707339617c521a3)  

Date: Wed Feb 25 10:02:09 2026


---

### ch...@google.com (2026-03-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071155)*
