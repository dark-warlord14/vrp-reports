# UAF in ModelContext::ForEachScriptTool

| Field | Value |
|-------|-------|
| **Issue ID** | [483853103](https://issues.chromium.org/issues/483853103) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Agentic Platform>WebMCP |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-02-12 |
| **Bounty** | $10,000.00 |

## Description

### Summary

`navigator.modelContextTesting.listTools()` reaches [`ModelContext::ForEachScriptTool`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/script_tools/model_context.cc;l=160), which unconditionally calls `ComputeInputSchema()` on each declarative tool pointer stored in [`tool_map_`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/script_tools/model_context.h;l=127). Declarative tool registration stores a raw pointer in [`ModelContext::ToolData::declarative_tool`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/script_tools/model_context.h;l=116), and the pointer is not traced in GC. After iframe/document shutdown, a lifecycle gap in form-side unregister logic can leave a stale map entry; once the underlying `HTMLFormMcpTool` is reclaimed, `ForEachScriptTool` dereferences a dangling pointer and triggers renderer UAF/use-after-poison.

> Note that the root cause of this issue is different with the recent reported [issue 483569512](https://issues.chromium.org/issues/483569512). And the fix in the [issue 483569512](https://issues.chromium.org/issues/483569512) does not mitigate this issue as well.

### Details

The current implementation path for DeclarativeWebMCPTool is: declarative form registration -> raw pointer retained in `ModelContext::tool_map_` -> unregister skipped in a shutdown edge case -> later schema refresh dereferences stale pointer.

In [`ModelContext::RegisterDeclarativeTool`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/script_tools/model_context.cc;l=475), declarative registration stores `DeclarativeWebMCPTool*` into `ToolData`:

```
void ModelContext::RegisterDeclarativeTool(String name,
                                           String description,
                                           DeclarativeWebMCPTool* tool) {
  auto script_tool = mojom::blink::ScriptTool::New();
  auto* tool_data = MakeGarbageCollected<ToolData>();
  script_tool->name = name;
  script_tool->description = description;
  script_tool->input_schema = "{}";  // For now
  tool_data->script_tool = std::move(script_tool);
  tool_data->declarative_tool = tool;

  tool_map_.insert(name, std::move(tool_data));
  OnToolsChanged();
}

```

In [`ModelContext::ToolData::Trace`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/script_tools/model_context.cc;l=528), only the V8 tool function is traced; the declarative pointer is not:

```
void ModelContext::ToolData::Trace(Visitor* visitor) const {
  visitor->Trace(v8_tool_function);
}

```

In [`HTMLFormElement::UpdateMcpDefinitionsIfNeeded`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/html_form_element.cc;l=302), the function returns early when `ModelContext` is unavailable (e.g., detached document with no `domWindow()/navigator()`), so the unregister path is skipped in that state:

```
ModelContext* model_context = nullptr;
if (auto* window = GetDocument().domWindow(); window && window->navigator()) {
  model_context = ModelContextSupplement::modelContext(*window->navigator());
}
if (!model_context) {
  return;
}

if (IsValidWebMCPForm()) {
  ...
  model_context->unregisterTool(active_webmcp_tool_->ToolName(),
                                ASSERT_NO_EXCEPTION);
  active_webmcp_tool_ = nullptr;
}

```

Later, [`ModelContext::ForEachScriptTool`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/script_tools/model_context.cc;l=160) updates declarative schemas on iteration and dereferences the stale pointer:

```
void ModelContext::ForEachScriptTool(
    base::FunctionRef<void(const mojom::blink::ScriptTool&)> func) const {
  for (const auto& tool : tool_map_) {
    auto tool_data = tool.value;
    // Always update the input schema, since the DOM might have changed.
    if (auto* declarative_tool = tool_data->declarative_tool) {
      tool_data->script_tool->input_schema =
          declarative_tool->ComputeInputSchema();
    }
    func(*tool_data->script_tool);
  }
}

```

Therefore, we can leverage the following chain to achieve UAF: implementation stores an untraced raw pointer -> lifecycle edge skips unregister -> GC reclaims the declarative tool object -> `listTools()` reaches `ForEachScriptTool` and dereferences freed memory.

### REPRODUCTION

Build args on commit `349bddcf54ebcd90e7d4d6b00433982956d3b33e` in Linux:

```
is_asan=true
is_component_build=true
dcheck_always_on=false
is_debug=false

```

Run command:

```
./chrome --user-data-dir=/tmp/xx --enable-features=WebMCPTesting --enable-experimental-web-platform-features --no-first-run --no-sandbox --js-flags=--expose-gc poc.html

```

We should observe the Use-after-Poison crash shown in the asan.txt.

This has been reachable in the M145, and will be shipped in the M146 dev trial.

### Bisection

This issue is introduced by the commit 3df80580897d24fbb730c0ee411f25ffe04e766b.

### SUGGESTED FIX

Make declarative tool lifetime GC-safe at the `ToolData` boundary and enforce stale-entry pruning during iteration.

We may:

1. Change `ToolData::declarative_tool` from raw `DeclarativeWebMCPTool*` to a GC-traceable handle.
2. Update `ToolData::Trace()` to trace declarative tool references.
3. Add a defensive guard in `ForEachScriptTool` to skip and remove entries whose declarative tool is no longer valid before calling `ComputeInputSchema()`.

This keeps `tool_map_` entries from holding dangling declarative pointers and prevents `listTools()` from dereferencing reclaimed objects.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 9.1 KB)
- [poc.html](attachments/poc.html) (text/html, 3.1 KB)

## Timeline

### om...@chromium.org (2026-02-12)

Based on the stack trace in `asan.txt` above, this is a blink crash, not a V8 crash.

### za...@google.com (2026-02-12)

Hi masonf@, can you take a look at this blink bug. It seems like we have a vulnerability in renderer process related to the WebMCPTesting feature.

### ch...@google.com (2026-02-13)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  main  

Author:  Mason Freed [masonf@chromium.org](mailto:masonf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7577275>

Make DeclarativeWebMCPTool garbage collected

---


Expand for full commit details
```
     
    Previously, ModelContext::RegisterDeclarativeTool stored a raw pointer 
    to a DeclarativeWebMCPTool in ToolData. If the underlying tool (e.g., an 
    HTMLFormMcpTool associated with a form) was reclaimed by GC while still 
    registered, subsequent calls to ForEachScriptTool (via 
    navigator.modelContext.listTools()) would dereference a dangling 
    pointer. 
     
    This CL fixes the issue by making DeclarativeWebMCPTool garbage 
    collected.  This ensures that any registered declarative tool is kept 
    alive as long as it remains in the ModelContext tool map. 
     
    Fixed: 483853103 
    Change-Id: I5422ffaafc52cb7c52549823e6a243627992066c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7577275 
    Auto-Submit: Mason Freed <masonf@chromium.org> 
    Reviewed-by: Ben Greenstein <bengr@chromium.org> 
    Commit-Queue: Ben Greenstein <bengr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1584900}

```

---

Files:

- M `third_party/blink/renderer/core/html/forms/html_form_element.h`
- M `third_party/blink/renderer/core/script_tools/model_context.cc`
- M `third_party/blink/renderer/core/script_tools/model_context.h`
- M `third_party/blink/renderer/core/script_tools/model_context_test.cc`

---

Hash: [2ba59d32b3ea3125e8c5aa6acddaf7d411fca7a7](https://chromiumdash.appspot.com/commit/2ba59d32b3ea3125e8c5aa6acddaf7d411fca7a7)  

Date: Fri Feb 13 22:04:07 2026


---

### ch...@google.com (2026-02-14)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1584900) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1584900) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-14)

**Merge approved:** your change passed merge requirements and is auto-approved for M146. Please go ahead and merge the CL to branch 7680 (refs/branch-heads/7680) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-14)

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

### ma...@chromium.org (2026-02-17)

Given that this is gated behind several experimental flags, I don't think it needs to be back-merged to M145. I just put up a CL to merge to M146.

### dx...@google.com (2026-02-17)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Mason Freed [masonf@chromium.org](mailto:masonf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7583841>

[M146] Make DeclarativeWebMCPTool garbage collected

---


Expand for full commit details
```
     
    Previously, ModelContext::RegisterDeclarativeTool stored a raw pointer 
    to a DeclarativeWebMCPTool in ToolData. If the underlying tool (e.g., an 
    HTMLFormMcpTool associated with a form) was reclaimed by GC while still 
    registered, subsequent calls to ForEachScriptTool (via 
    navigator.modelContext.listTools()) would dereference a dangling 
    pointer. 
     
    This CL fixes the issue by making DeclarativeWebMCPTool garbage 
    collected.  This ensures that any registered declarative tool is kept 
    alive as long as it remains in the ModelContext tool map. 
     
    (cherry picked from commit 2ba59d32b3ea3125e8c5aa6acddaf7d411fca7a7) 
     
    Fixed: 483853103 
    Change-Id: I5422ffaafc52cb7c52549823e6a243627992066c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7577275 
    Auto-Submit: Mason Freed <masonf@chromium.org> 
    Reviewed-by: Ben Greenstein <bengr@chromium.org> 
    Commit-Queue: Ben Greenstein <bengr@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1584900} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7583841 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#541} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/html/forms/html_form_element.h`
- M `third_party/blink/renderer/core/script_tools/model_context.cc`
- M `third_party/blink/renderer/core/script_tools/model_context.h`
- M `third_party/blink/renderer/core/script_tools/model_context_test.cc`

---

Hash: [b9372e169d0cbca015802007118937b5f899d7c9](https://chromiumdash.appspot.com/commit/b9372e169d0cbca015802007118937b5f899d7c9)  

Date: Tue Feb 17 21:23:08 2026


---

### ch...@google.com (2026-02-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-02-18)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dr...@chromium.org (2026-02-19)

Per [#comment9](https://issues.chromium.org/issues/483853103#comment9), removing the M145 merge label.

### qk...@google.com (2026-02-19)

Added `Not-Applicable-138` and `Not-Applicable-144` label because the suspected CL[1] was not included in M138 and M144.

[1] <https://chromium-review.googlesource.com/c/chromium/src/+/7428254>

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High Quality. Renderer RCE / memory corruption in a sandboxed process.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### he...@gmail.com (2026-03-06)

deleted

### ch...@google.com (2026-05-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High Quality. Renderer RCE / memory corruption in a sandboxed process.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483853103)*
