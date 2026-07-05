# WebNN DirectML Constant Tensor Use-After-Free

| Field | Value |
|-------|-------|
| **Issue ID** | [484319071](https://issues.chromium.org/issues/484319071) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Windows |
| **Reporter** | ci...@gmail.com |
| **Assignee** | br...@intel.com |
| **Created** | 2026-02-13 |
| **Bounty** | $16,000.00 |

## Description

---

### Report description

WebNN DirectML Constant Tensor Use-After-Free

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/services/webnn/dml/graph_impl_dml.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

- ASan crash: Chromium 146.0.7678.0 (Developer Build) (64-bit), Windows x64, `--in-process-gpu`
- Release crashes: Chrome 144.0.7559.133 (Official Build) (64-bit) (cohort: Stable)

Chrome's WebNN DirectML backend stores raw `WebNNTensorImpl*` pointers to constant tensors across asynchronous graph compilation boundaries. JavaScript can destroy the tensor during the async gap, causing DML to dereference a dangling pointer in the GPU process. The freed 264-byte `TensorImplDml` object is replaceable via heap spray, giving the attacker control over the `ID3D12Resource*` bound as a graph constant. The spray uses `CreatePendingConstant` Mojo calls to allocate 264-byte `HeapArray<uint8_t>` buffers on the same thread and size class as the freed object, with Mojo receiver ordering guaranteeing the build → destroy → spray sequence; 4/4 attempts replaced the freed object.

DirectML (a Microsoft system DLL loaded via `LoadSystemLibrary()`, with no Clang CFI) makes COM vtable calls on this attacker-controlled pointer. Crash dumps confirm `rdi = 0x4141414141414141` inside `directml!ValidateBufferBinding`, and a DLL chain PoC redirects DML's vtable dispatch to execute `user32!WaitForInputIdle` (visible on the call stack).

GPU process UAF from JavaScript with demonstrated controlled vtable hijack and CFG-valid function execution. Heap spray was 100% reliable in testing. MiraclePtr does NOT protect this pointer (`WebNNTensorImpl*`, not `raw_ptr<T>`). CFI is not enabled on Windows.

#### Affected Code

During `ValidateGraphImpl()`, constant tensor refs are extracted as raw pointers:

```
// webnn_graph_builder_impl.cc:3162
scoped_refptr<WebNNTensorImpl> tensor_impl =
    context_->GetWebNNTensorImpl(id_and_handle_it->second);
// ...validation...
graph_constant_tensors.emplace_back(operand_id, tensor_impl.get());
// scoped_refptr goes out of scope at end of block, only raw pointer survives

```

This raw pointer survives two async hops (ThreadPool permutation transpose at line 2963 + DML compilation at line 6907). During either async gap, the renderer can destroy the tensor via `MLTensor.destroy()`, which fires `OnDisconnect()` → `RemoveWebNNTensorImpl()` → destructor. Two UAF dereferences exist in `graph_impl_dml.cc`:

1. Line 6441 (`CreateAndBuildInternal`): `tensor_impl->data_type()` and `tensor_impl->shape()` - reachable after the first async boundary (TransposePendingPermutation ThreadPool hop). This is the earlier crash point.
2. Line 6196 (`OnCompilationComplete`): `constant_tensor_impl->buffer()` - reachable after both async boundaries. This is where the `ID3D12Resource*` is read and passed to DirectML for COM vtable dispatch.

### Steps to Reproduce

Prerequisites: The WebNN API must be enabled, and the DirectML backend must be active. In testing, the following flags were required:

```
--enable-features=WebMachineLearningNeuralNetwork,WebNNDirectML
--disable-features=WebNNOnnxRuntime

```

`WebMachineLearningNeuralNetwork` is enabled by default but was explicitly set in ASan builds. `WebNNDirectML` is disabled by default (the default Windows backend is OnnxRuntime, which does not support constant tensors). Only the DML backend exercises the vulnerable code path since ORT, TFLite, CoreML, and LiteRT all reject constant tensor creation.

Windows only. Any system with DX12 support. No user interaction required.

#### PoC 1: Controlled Pointer (`poc_webnn_dml_uaf.html`) - auto-fires on load

1. Launch Chrome with flags above (for ASan, add `--in-process-gpu`)
2. Navigate to `poc_webnn_dml_uaf.html`
3. PoC auto-fires: creates constant tensor, starts `build()`, immediately `destroy()`s the tensor, sprays 30x 264-byte objects with `0x4141414141414141` at buffer\_ offset (0xE0)
4. GPU process crashes

#### PoC 2: DLL Chain Escalation (`poc_webnn_dml_dll_chain.html`) - button-triggered

This PoC demonstrates that the controlled vtable pointer leads to attacker-chosen function execution. It simulates an attacker who has obtained DLL base addresses through a separate information disclosure (for example, a renderer info leak).

1. Run PoC 1 first, collect DLL bases from Crashpad dump: `lm m kernel32; lm m user32`
2. Enter bases in PoC 2 input fields, select "WaitForInputIdle" chain, click "Run DLL Chain Exploit"
3. Same UAF mechanism, but sprays a kernel32 `.rdata` address into `buffer_`
4. DML follows the pointer chain: `[A] = B (.data)` then `[B+0x38] = C (function)` then calls C

Note: The DLL offsets in PoC 2 are specific to the test system's Windows build. You will need to extract kernel32 and user32 base addresses from a PoC 1 Crashpad dump and update the offsets for your DLL versions.

#### Crash Evidence: ASan (Chromium 146.0.7678.0 Developer Build, x64, `--in-process-gpu`)

```
==12152==ERROR: AddressSanitizer: heap-use-after-free on address 0x120efd3e1fa0
READ of size 8 at 0x120efd3e1fa0 thread T24

USE:
  #0 Microsoft::WRL::ComPtr<ID3D12Resource>::Get      wrl/client.h:370
  #1 webnn::dml::TensorImplDml::buffer                tensor_impl_dml.h:39
  #2 webnn::dml::GraphImplDml::OnCompilationComplete   graph_impl_dml.cc:6196

FREE:
  #1  TensorImplDml::'scalar deleting dtor'            tensor_impl_dml.h:37
  #12 WebNNContextImpl::RemoveWebNNTensorImpl           webnn_context_impl.cc:353
  #13 WebNNTensorImpl::OnDisconnect                     webnn_tensor_impl.cc:189

ALLOC:
  #1 MakeRefCounted<TensorImplDml>                      scoped_refptr.h:151
  #2 ContextImplDml::CreateTensorImpl                   context_impl_dml.cc:700

0x120efd3e1fa0 is located 224 bytes inside of 264-byte region [0x120efd3e1ec0, 0x120efd3e1fc8)
  offset 224 (0xE0) = buffer_ field (ComPtr<ID3D12Resource>)

MiraclePtr Status: NOT PROTECTED
This crash is still exploitable with MiraclePtr.

```
#### Crash Evidence: Crashpad Controlled Pointer (Chrome 144.0.7559.133 Stable, release)

```
FAULTING_IP: directml!BindingValidator::ValidateBufferBinding+0x58
    mov rax, qword ptr [rdi]    ; load COM vtable from fake ID3D12Resource*
    mov rbx, qword ptr [rax+38h] ; next: load function pointer from vtable

Exception: ACCESS_VIOLATION (c0000005)
rdi = 0x4141414141414141    ; our spray value at buffer_ offset 0xE0

```
#### Crash Evidence: Crashpad DLL Chain (Chrome 144.0.7559.133 Stable, release)

```
Call stack:
  ntdll!KiRaiseUserExceptionDispatcher+0x3a
  USER32!WaitForInputIdle+0x38                              ; FUNCTION EXECUTED
  directml!BindingValidator::ValidateBufferBinding+0x7d     ; DML vtable call site
  directml!BindingValidator::ValidateBindingDesc+0x77
  directml!BindingValidator::ValidateInputBindings+0x4d
  directml!DmlBindingTable::BindInputs+0x7d
  chrome!... (WebNN graph build pipeline)

Exception: STATUS_INVALID_HANDLE (c0000008)
rbx = 0x00007FFD71353C68 = kernel32+0xA3C68 (our spray value = address A)

```
### Fix

Replace raw `WebNNTensorImpl*` with `scoped_refptr<WebNNTensorImpl>` in the constant tensor operands map. In `webnn_graph_builder_impl.cc` at line 3162, change:

```
graph_constant_tensors.emplace_back(operand_id, tensor_impl.get());

```

to:

```
graph_constant_tensors.emplace_back(operand_id, tensor_impl);

```

Then update downstream signatures from `base::flat_map<OperandId, WebNNTensorImpl*>` to `base::flat_map<OperandId, scoped_refptr<WebNNTensorImpl>>` in:

- `webnn_context_impl.h`: `CreateGraphImpl` parameter
- `webnn_graph_builder_impl.h`: `ValidateGraphSuccessResult` member and `DidTransposePendingPermutations` parameter
- `graph_impl_dml.cc`: `OnCompilationComplete`, `CreateAndBuildInternal`, `CreateAndBuild`
- All other backend `CreateGraphImpl` implementations (`context_impl_ort.cc`, `context_impl_tflite.cc`, `context_impl_coreml.mm`, `context_impl_litert.cc`)

This keeps the tensor alive for the entire async graph build lifecycle.

## Bisect

The vulnerable raw pointer pattern was introduced in:

- Commit: `42cb30d76e94ad3494fc8a3567760e74ece54509`
- Date: 2025-05-21
- Message: "Reland 'WebNN: support constant tensors'"
- CL: <https://chromium-review.googlesource.com/c/chromium/src/+/6557622>

#### Impact analysis

- GPU process crash (DoS) from any web page with DML backend enabled, highly reliable
- Controlled COM vtable hijack: attacker-chosen `ID3D12Resource*` passed to DirectML. The attacker controls `rdi`, which DirectML unconditionally dereferences as a COM vtable and dispatches through - equivalent to instruction pointer control via the heap spray.
- No CFI on Windows (`sanitizers.gni` enables CFI only on Linux x64/ChromeOS), and DirectML itself is an uninstrumented system DLL loaded via `LoadSystemLibrary()`.
- DLL chain technique: with knowledge of DLL bases (per-boot constants on Windows), the attacker can construct pointer chains in kernel32/user32 .rdata/.data that match DML's expected COM vtable layout, redirecting dispatch to CFG-valid exported functions.
- Demonstrated CFG-valid function execution: `user32!WaitForInputIdle` confirmed on the call stack via Crashpad dump (see PoC 2 evidence above).
- GPU process has weak sandbox: no Win32k lockdown (unlike renderer), privileged GpuHost Mojo interface to browser process, full D3D12/DXGI access, COM MTA initialized.

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.133 Stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [poc_webnn_dml_uaf.html](attachments/poc_webnn_dml_uaf.html) (text/html, 3.4 KB)
- [poc_webnn_dml_dll_chain.html](attachments/poc_webnn_dml_dll_chain.html) (text/html, 4.7 KB)
- [asan_webnn_dml_uaf_out.txt](attachments/asan_webnn_dml_uaf_out.txt) (text/plain, 31.0 KB)

## Timeline

### re...@chromium.org (2026-02-13)

Note, the WebNNDirectML flag is disabled by default and given DirectML is deprecated in favor of the Windows ML framework (ONNX Runtime, controlled by the WebNNOnnxRuntime flag) this isn't exploitable in production and likely never will be.

### br...@intel.com (2026-02-13)

To be more specific: the exploit relies on constant `MLTensor` support. This could become exploitable but not currently, since DML only has support and is disabled in production.

### ci...@gmail.com (2026-02-14)

Thanks for the quick triage. I'd just like to highlight that this UAF currently exists in Chrome Stable with MiraclePtr Status: `NOT PROTECTED`. Moreover, the report demonstrates RDI control, 100% reliable heap spray, and CFG-valid function execution via controlled vtable hijack - not just a crash. Additionally, bugs behind disabled-by-default flags are generally in scope.

I understand DML may be deprecated in favor of ORT, but the vulnerable code ships in Stable today and the raw pointer pattern at webnn\_graph\_builder\_impl.cc:3162 is backend-agnostic - it would affect any future backend that supports constant tensors.

### re...@chromium.org (2026-02-17)

Fair point. This needs to be fixed but not for M-146.

### ci...@gmail.com (2026-03-04)

Attaching unabridged ASan output; apologies for the delay on this information.

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Bryan Bernhart [bryan.bernhart@intel.com](mailto:bryan.bernhart@intel.com)  

Link:    <https://chromium-review.googlesource.com/7629079>

WebNN: Use scoped\_refptr for constant tensor operands

---


Expand for full commit details
```
     
    Updates the WebNN service to use scoped_refptr instead of raw pointers 
    when passing constant tensor operands during graph creation and 
    building. 
     
    Ensures that the underlying tensor resources remain valid throughout the 
    asynchronous graph compilation and initialization process across 
    backends. 
     
    Bug: 484319071 
    Change-Id: Id7762291afb5dc0fa1e2be5c6f47deafa92fbfcc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629079 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Bernhart, Bryan <bryan.bernhart@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#1594302}

```

---

Files:

- M `services/webnn/coreml/context_impl_coreml.h`
- M `services/webnn/coreml/context_impl_coreml.mm`
- M `services/webnn/coreml/graph_impl_coreml.h`
- M `services/webnn/coreml/graph_impl_coreml.mm`
- M `services/webnn/dml/context_impl_dml.cc`
- M `services/webnn/dml/context_impl_dml.h`
- M `services/webnn/dml/graph_impl_dml.cc`
- M `services/webnn/dml/graph_impl_dml.h`
- M `services/webnn/ort/context_impl_ort.cc`
- M `services/webnn/ort/context_impl_ort.h`
- M `services/webnn/ort/graph_impl_ort.cc`
- M `services/webnn/ort/graph_impl_ort.h`
- M `services/webnn/tflite/context_impl_litert.cc`
- M `services/webnn/tflite/context_impl_litert.h`
- M `services/webnn/tflite/context_impl_tflite.cc`
- M `services/webnn/tflite/context_impl_tflite.h`
- M `services/webnn/tflite/graph_impl_litert.cc`
- M `services/webnn/tflite/graph_impl_litert.h`
- M `services/webnn/tflite/graph_impl_tflite.cc`
- M `services/webnn/tflite/graph_impl_tflite.h`
- M `services/webnn/webnn_context_impl.h`
- M `services/webnn/webnn_graph_builder_impl.cc`
- M `services/webnn/webnn_graph_builder_impl.h`
- M `services/webnn/webnn_graph_builder_impl_unittest.cc`
- M `services/webnn/webnn_graph_impl_unittest.cc`

---

Hash: [91ea8012b89e66a2be2ed27284ea98e7dceee70c](https://chromiumdash.appspot.com/commit/91ea8012b89e66a2be2ed27284ea98e7dceee70c)  

Date: Wed Mar 4 23:59:59 2026


---

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@google.com (2026-06-25)

(this remains in the queue for the panel, hold on!)

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
High Quality. Renderer RCE / memory corruption in a sandboxed process with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484319071)*
