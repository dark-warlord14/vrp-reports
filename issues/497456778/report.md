# WebML Double-Free Via XNNPACK LUT-Fusion

| Field | Value |
|-------|-------|
| **Issue ID** | [497456778](https://issues.chromium.org/issues/497456778) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | h2...@gmail.com |
| **Assignee** | we...@intel.com |
| **Created** | 2026-03-29 |
| **Bounty** | $43,000.00 |

## Description

# VULNERABILITY DETAILS

This is a double-free in XNNPACK's quantized unary LUT-fusion optimization, reachable through Chromium's WebNN CPU backend.

The optimization becomes incorrect when a temporary LUT-building subgraph copies a previously generated LUT value that still carries `XNN_VALUE_FLAG_NEEDS_CLEANUP`

At that point, ownership of the LUT buffer is duplicated across:

1. the real outer XNNPACK subgraph
2. the temporary stack-allocated subgraph used to synthesize another LUT

The temporary runtime frees the LUT buffer first, then outer runtime later frees the same pointer again.

## Relevant Code Paths

### 1. The pass scans quantized unary chains and fuses at most 10 nodes

[xnn\_subgraph\_fuse\_unary\_quantized\_into\_lut()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=1938;bpv=1;bpt=0) walks the subgraph, recognizes unary-elementwise chains with quantized 8-bit input, and builds a temporary subgraph on the stack:

```
void xnn_subgraph_fuse_unary_quantized_into_lut(xnn_subgraph_t subgraph) {
  for (uint32_t n = 0; n < subgraph->num_nodes; n++) {
    struct xnn_node* node = &subgraph->nodes[n];
    if (node->type == xnn_node_type_invalid) {
      continue;
    }

    const uint32_t input_id =
        is_pure_unary_elementwise(subgraph, node, NULL, 0);
    if (input_id == XNN_INVALID_VALUE_ID) {
      continue;
    }

    const struct xnn_value* input_value = &subgraph->values[input_id];
    if (input_value->datatype == xnn_datatype_invalid ||
        xnn_datatype_size_bits(input_value->datatype) != 8) {
      continue;
    }

    struct xnn_subgraph unary_subgraph;
    memset(&unary_subgraph, 0, sizeof(unary_subgraph));
    struct xnn_value unary_values[XNN_MAX_UNARY_FUSION_VALUES];
    uint32_t value_map[XNN_MAX_UNARY_FUSION_VALUES];
    struct xnn_node unary_nodes[XNN_MAX_UNARY_FUSION_NODES];
    ...

    do {
      nodes_to_fuse[unary_subgraph.num_nodes] = node;
      const struct xnn_node* new_node = copy_node_to_static_subgraph(
          subgraph, node, value_map, &unary_subgraph);
      ...
      node = &subgraph->nodes[output->first_consumer];
    } while (... &&
             unary_subgraph.num_nodes < XNN_MAX_UNARY_FUSION_NODES);

```

The chain-recognition [helper](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=1727;bpv=1;bpt=0) treats any unary-elementwise node as eligible and returns its first input:

```
static uint32_t is_pure_unary_elementwise(xnn_subgraph_t subgraph,
                                          const struct xnn_node* node,
                                          const uint32_t* unary_values,
                                          uint32_t num_unary_values) {
  switch (node->type) {
    case xnn_node_type_unary_elementwise:
      assert(node->num_inputs >= 1);
      return node->inputs[0];

```
### 2. A successful fusion creates a heap LUT and stores it as a `NEEDS_CLEANUP` value

When the pass decides to replace the tail of a chain with a LUT node, [replace\_node\_with\_lut()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=1880;bpv=1;bpt=0) allocates a 256-byte buffer and stores it inside a new subgraph value:

```
static bool replace_node_with_lut(xnn_subgraph_t subgraph,
                                  struct xnn_node* node, uint32_t input_id,
                                  uint32_t unary_input_id,
                                  xnn_subgraph_t unary_subgraph) {
  ...
  uint8_t* lut = xnn_allocate_memory(256 * sizeof(uint8_t));
  ...

  struct xnn_value* lut_value = xnn_subgraph_new_internal_value(subgraph);
  lut_value->flags |= XNN_VALUE_FLAG_NEEDS_CLEANUP;
  lut_value->data = lut;
  ...

```

After this runs:

- the LUT buffer is heap memory
- ownership is recorded only implicitly, via `XNN_VALUE_FLAG_NEEDS_CLEANUP`
- the outer subgraph believes it owns that buffer

### 3. The rewritten LUT node is still a unary-elementwise node

After creating the LUT value, the fused node is rewritten [in place](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=1928;bpv=1;bpt=0):

```
xnn_define_unary_elementwise_lut_in_place(node, input_id, node->outputs[0],
                                          lut_value->id);

```

And [xnn\_define\_unary\_elementwise\_lut\_in\_place()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph/unary.c;l=462;bpv=1;bpt=0) leaves it as a `xnn_node_type_unary_elementwise` node with two inputs. This means the outer scan can later revisit this rewritten node as the head of another unary chain.

```
enum xnn_status xnn_define_unary_elementwise_lut_in_place(
  struct xnn_node* node,
  uint32_t input_id,
  uint32_t output_id,
  uint32_t lut_id)
{
  node->type = xnn_node_type_unary_elementwise;
  node->unary_operator = xnn_unary_invalid;
  node->num_inputs = 2;
  node->inputs[0] = input_id;
  node->inputs[1] = lut_id;
  node->num_outputs = 1;
  node->outputs[0] = output_id;

```
### 4. The temporary subgraph shallow-copies values, including cleanup ownership

When the pass builds a temporary subgraph, it uses [copy\_value\_to\_static\_subgraph()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=1790;bpv=1;bpt=0) (via  `copy_node_to_static_subgraph`):

```
static uint32_t copy_value_to_static_subgraph(xnn_subgraph_t src_subgraph,
                                              const struct xnn_value* src_value,
                                              uint32_t* value_map,
                                              xnn_subgraph_t dst_subgraph) {
  ...
  if (is_new) {
    ...
    struct xnn_value* dst_value = &dst_subgraph->values[dst_id];
    dst_subgraph->num_values++;
    *dst_value = *src_value;
    dst_value->id = dst_id;
    dst_value->producer = XNN_INVALID_NODE_ID;
    dst_value->first_consumer = XNN_INVALID_NODE_ID;
  }
  return dst_id;
}

```

I believe this is the root cause of the issue, the struct assignment `*dst_value = *src_value;` copies the data pointer, allocation type and `flags`. So if `src_value` is the previously generated LUT value, the value in the temporary subgraph receives the heap pointer and the `XNN_VALUE_FLAG_NEEDS_CLEANUP` flag.

### 5. The temporary runtime shallow-copies the same state again

[run\_subgraph\_to\_make\_lut()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=1835;bpv=1;bpt=0) creates a temporary runtime from the temporary subgraph:

```
static enum xnn_status run_subgraph_to_make_lut(xnn_subgraph_t subgraph,
                                                uint32_t input_id,
                                                uint32_t output_id,
                                                uint8_t* lut) {
  xnn_runtime_t runtime;
  XNN_RETURN_IF_ERROR(xnn_create_runtime_v4(
      subgraph, NULL, NULL, NULL, XNN_FLAG_NO_OPERATOR_FUSION, &runtime));
  ...
fail:
  xnn_delete_runtime(runtime);
  return status;
}

```

Inside [xnn\_create\_runtime\_v4](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/runtime.c;l=668;bpv=1;bpt=0), all subgraph values are copied into runtime values:

```
xnn_subgraph_analyze_consumers_and_producers(subgraph);
for (size_t i = 0; i < subgraph->num_values; i++) {
  xnn_runtime_value_copy(runtime->values + i, subgraph->values + i);
  runtime->values[i].id = subgraph->values[i].id;
}

```

And [xnn\_runtime\_value\_copy()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=218;bpv=1;bpt=0) is also a shallow copy of ownership-relevant state:

```
void xnn_runtime_value_copy(struct xnn_runtime_value* dst_value,
                            const struct xnn_value* src_value) {
  dst_value->type = src_value->type;
  dst_value->datatype = src_value->datatype;
  dst_value->quantization = src_value->quantization;
  dst_value->shape = src_value->shape;
  dst_value->size = src_value->size;
  dst_value->allocation_type = src_value->allocation_type;
  dst_value->flags = src_value->flags;
  ...
  dst_value->data = src_value->data;

```

At this point both subgraphs believe they own the same heap allocation.

### 6. Temporary runtime teardown frees the borrowed LUT

When the temporary runtime is destroyed, [xnn\_delete\_runtime()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/runtime.c;l=1157;bpv=1;bpt=0) does:

```
enum xnn_status xnn_delete_runtime(
  xnn_runtime_t runtime)
{
  ...
  if (runtime->values != NULL) {
    for (size_t i = 0; i < runtime->num_values; i++) {
      struct xnn_runtime_value* value = &runtime->values[i];
      if (value->allocation_type == xnn_allocation_type_dynamic ||
          value->flags & XNN_VALUE_FLAG_NEEDS_CLEANUP) {
        xnn_release_memory(value->data);
      }
    }
    xnn_release_memory(runtime->values);
  }

```

Because the copied runtime value still has `XNN_VALUE_FLAG_NEEDS_CLEANUP`, the temporary runtime frees the LUT buffer while the outer graph still needs it.

### 7. The outer runtime later frees the same pointer again

After graph compilation finishes, the outer XNNPACK runtime is created from the real subgraph. That real subgraph still contains the original LUT value with the same pointer and the same cleanup flag. Later, when the WebNN graph is destroyed, the outer runtime reaches the same `xnn_delete_runtime()` code path and frees LUT1 a second time.

# VERSION

Chrome Version: 148.0.7762.0 + dev (commit e8325ba6197afa4eecfb53d261fcb1531fa97c66)

Operating System: Linux

I believe this bisects to the [commit that introduced](https://github.com/google/XNNPACK/commit/d53998c15484da984bef27b5d791c103461c98aa) the pass in XNNPACK.

# REPRODUCTION CASE

The issue can be reached straight from JavaScript, no need for a compromised renderer.

To reproduce:

`./chrome --no-sandbox --enable-features=WebMachineLearningNeuralNetwork poc.html`

GN args used for testing:

```
is_debug = false
symbol_level = 2
dcheck_always_on = false
is_asan = true

```

See the attached `asan_backtrace.txt` for the full backtrace of the crash.

# FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: GPU process crash

# CREDIT INFORMATION

Reporter credit: TFGC

## Attachments

- [asan_backtrace.txt](attachments/asan_backtrace.txt) (text/plain, 209.6 KB)
- [poc.html](attachments/poc.html) (text/html, 1.7 KB)
- [run-chrome-asan.log](attachments/run-chrome-asan.log) (text/plain, 49.8 KB)

## Timeline

### da...@google.com (2026-04-01)

Thanks! I was able to reproduce this. AIUI, WebNN is not enabled (yet?) so setting Security\_Impact-None.

### aj...@google.com (2026-04-02)

Repros.

### ni...@intel.com (2026-04-09)

@we...@intel.com, please take a look. This issue might be fixed in XNNPACK itself.

### we...@intel.com (2026-04-09)

Sure, I will investigate this.

### dx...@google.com (2026-04-13)

Project: chromium/src  

Branch:  main  

Author:  Wei Wang [wei4.wang@intel.com](mailto:wei4.wang@intel.com)  

Link:    <https://chromium-review.googlesource.com/7754105>

Roll src/third\_party/xnnpack/src/ 211341d5a..bcefe9ae6 (19 commits)

---


Expand for full commit details
```
     
    Roll XNNPACK to apply security fix[1]. 
     
    https://chromium.googlesource.com/external/github.com/google/XNNPACK.git/+log/211341d5a2a6..bcefe9ae64c8 
     
    $ git log 211341d5a..bcefe9ae6 --date=short --no-merges --format='%ad %ae %s' 
    2026-04-12 dsharlet Minor SIMD cleanups 
    2026-04-10 vksnk Update Google Benchmark, KleidiAI, and slinky dependencies. 
    2026-04-10 fbarchard Update SDE version to 10.8 
    2026-04-10 dsharlet Remove constraint that we don't rewrite broadcasts to be producers of external outputs 
    2026-04-10 dsharlet Add rewrite for f(broadcast(x)) -> broadcast(f(x)) 
    2026-04-10 dsharlet Reduce max rank of binary op testing in YNNPACK 
    2026-04-10 ritownsend [gn] ci: restore format check 
    2026-04-10 gonnet Add `xnn_datatype_qint4` datatype. 
    2026-04-10 gonnet `fully-connected` does not care whether the `int32` bias vector is channel-wise or tensor-wise quantized, since it assumes it has the same quantization as the weights. 
    2026-04-10 gonnet Mark `binary_test` with `timeout = "moderate"` to avoid flakiness due to timeouts. 
    2026-04-10 dsharlet Add `slice_dim0` helper 
    2026-04-10 samfuller Adds missing GEMMBenchmark overload for qp8_f32_qc8w_gemm_minmax and corrects qp8_f32_qc4w microkernels and associated functions to use xnn_f32_qc4w_minmax_params instead of xnn_f32_minmax_params. 
    2026-04-10 gonnet Demote some logging for subgraph rewrites from `xnn_log_info` to `xnn_log_debug`. 
    2026-04-10 wei4.wang Initial upload. 
    2026-04-09 dsharlet Minor simplifications of static_broadcast nodes 
    2026-04-09 dsharlet Give slinky our assumptions to reduce overhead 
    2026-04-09 dsharlet Update slinky in XNNPACK 
    2026-04-09 vksnk Handle identity casts for scalar vectors in simd wrappers 
    2026-04-09 dsharlet Add fp64 reduce support 
     
    Created with: 
      roll-dep src/third_party/xnnpack/src 
     
    [1] https://github.com/google/XNNPACK/pull/9935 
     
    Bug: 497456778 
    Change-Id: I7418b9e70cd3ee1dea541587c70f0ccd7e3b425f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7754105 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1613831}

```

---

Files:

- M `DEPS`
- M `third_party/xnnpack/README.chromium`
- M `third_party/xnnpack/src`

---

Hash: [f2a57a348f533e846f022b33b7ac42d9d4d7b7d1](https://chromiumdash.appspot.com/commit/f2a57a348f533e846f022b33b7ac42d9d4d7b7d1)  

Date: Mon Apr 13 17:35:02 2026


---

### aj...@chromium.org (2026-04-16)

Is this fixed? If so please mark as Fixed.

### sp...@google.com (2026-05-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497456778)*
