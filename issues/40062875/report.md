# v8 oob read in turboshaft::Graph::IncrementInputUses

| Field | Value |
|-------|-------|
| **Issue ID** | [40062875](https://issues.chromium.org/issues/40062875) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | 5n...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-02-02 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

v8 version:head  

build flag:  

gn gen out/x64\_release --args="target\_cpu="x64" symbol\_level=2 is\_debug=false is\_component\_build=false v8\_enable\_backtrace = true v8\_enable\_disassembler=true v8\_enable\_object\_print=true"

run arg:  

--interrupt-budget=1000 --harmony-struct --maglev --stress-maglev --turboshaft

**Problem Description:**  

v8 crash on oob read obj,gdb crash state:  

\*RAX 0x7f1b30031918 ◂— 0x10002002b /\* '+' \*/  

\*RBX 0x7f1bbd29b8b8 —▸ 0x7f1b30028830 —▸ 0x55ce66e2ee60 ◂— 0x2a118  

\*RCX 0x7f1b30030d18 ◂— 0xffffffff00000515  

\*RDX 0xffffffff  

\*RDI 0x3400  

\*RSI 0x1  

R8 0x0  

\*R9 0xffffffff  

\*R10 0xc00  

\*R11 0x7f1bbd29b8b8 —▸ 0x7f1b30028830 —▸ 0x55ce66e2ee60 ◂— 0x2a118  

\*R12 0x7f1b30028830 —▸ 0x55ce66e2ee60 ◂— 0x2a118  

\*R13 0xbf0  

\*R14 0xc00  

\*R15 0xffffffff  

\*RBP 0x7f1bbd29b820 —▸ 0x7f1bbd29ba60 —▸ 0x7f1bbd29bad0 —▸ 0x7f1bbd29bb70 —▸ 0x7f1bbd29bbd0 ◂— ...  

\*RSP 0x7f1bbd29b7e0 —▸ 0x7f1bbd29b820 —▸ 0x7f1bbd29ba60 —▸ 0x7f1bbd29bad0 —▸ 0x7f1bbd29bb70 ◂— ...  

\*RIP 0x55ce6617264b ◂— movzx esi, byte ptr [rcx + rdx + 1]  

──────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────  

► 0x55ce6617264b movzx esi, byte ptr [rcx + rdx + 1]  

0x55ce66172650 cmp sil, 0xff  

0x55ce66172654 je 0x55ce6617265e <0x55ce6617265e>  

↓  

0x55ce6617265e mov byte ptr [rax + 1], 1  

0x55ce66172662 mov r13, qword ptr [rbx + 8]  

0x55ce66172666 mov r12d, r14d  

0x55ce66172669 shr r12d, 4  

0x55ce6617266d mov rax, qword ptr [r13 + 0x98]  

0x55ce66172674 mov rcx, qword ptr [r13 + 0xa0]  

0x55ce6617267b sub rcx, rax  

0x55ce6617267e sar rcx, 2  

───────────────────────────────[ SOURCE (CODE) ]────────────────────────────────  

In file: /home/r00t/v8/v8/src/compiler/turboshaft/graph.h  

786  

787 template <class Op>  

788 void IncrementInputUses(const Op& op) {  

789 for (OpIndex input : op.inputs()) {  

790 Operation& input\_op = Get(input);  

► 791 auto uses = input\_op.saturated\_use\_count;  

792 if (V8\_LIKELY(uses != Operation::kUnknownUseCount)) {  

793 input\_op.saturated\_use\_count = uses + 1;  

794 }  

795 }  

796 }

For stack trace,see stacktrace.txt

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [10.js](attachments/10.js) (text/plain, 167 B)
- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 3.7 KB)

## Timeline

### [Deleted User] (2023-02-02)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-03)

Setting Security_Impact-None because Turboshaft is still experimental.

Passing to the Turboshaft folks for further analysis.

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### fl...@google.com (2023-02-03)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4896962418769920.

### te...@chromium.org (2023-02-10)

Assigning based on Clusterfuzz regression range.

### cl...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-10)

Detailed Report: https://clusterfuzz.com/testcase?key=4896962418769920

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  dominating_frame_state.valid() in graph-builder.cc
  v8::internal::compiler::turboshaft::GraphBuilder::Process
  v8::internal::compiler::turboshaft::BuildGraph
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=85770:85771

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4896962418769920

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2023-02-10)

[Empty comment from Monorail migration]

### te...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### te...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-15)

ClusterFuzz testcase 4896962418769920 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=85819:85820

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations! The VRP Panel has decided to award you $7,000 for this report as turboshaft was not behind --experimental at the time of reporting. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-26)

This issue was migrated from crbug.com/chromium/1412343?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1412642, crbug.com/chromium/1412975]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062875)*
