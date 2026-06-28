# UAF in XNN reshape 

| Field | Value |
|-------|-------|
| **Issue ID** | [492450480](https://issues.chromium.org/issues/492450480) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-03-13 |
| **Bounty** | $43,000.00 |

## Description

### Summary

A valid WebNN graph containing a long chain of `reshape()` operations can trigger the UAF in XNNPACK during graph build. In [`xnn_subgraph_optimize_common_subgraphs`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=2695), it caches a pointer to `subgraph->nodes[input_producer_id]`, then calls `xnn_define_static_reshape()`, which may grow and relocate the node array, and finally dereferences and clears the stale pointer, leading to the UAF.

### Details

[`optimize_common_subgraphs_merge_reshapes`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=2695) keeps a raw pointer to `input_producer` across an operation that can append a new node:

At [`optimize_common_subgraphs_merge_reshapes`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=2702), the rewrite captures and later reuses a node pointer after inserting a replacement reshape:

```
  // Check that we are the only consumer of the input node.
  const uint32_t input_id = node->inputs[0];
  struct xnn_value* input_value = &subgraph->values[input_id];
  const uint32_t input_producer_id = input_value->producer;
  if (input_producer_id == XNN_INVALID_NODE_ID ||
      input_value->num_consumers != 1) {
    return xnn_status_success;
  }
  struct xnn_node* input_producer = &subgraph->nodes[input_producer_id];

  // Check all the interesting combinations.

  // reshape(reshape(x)).
  if (input_producer->type == xnn_node_type_static_reshape &&
      node->type == xnn_node_type_static_reshape) {
    XNN_RETURN_IF_ERROR(
        xnn_shape_fill_gaps(&input_producer->params.static_reshape.new_shape,
                            &node->params.static_reshape.new_shape));
    XNN_RETURN_IF_ERROR(
        xnn_define_static_reshape(
            subgraph, node->params.static_reshape.new_shape.num_dims,
            node->params.static_reshape.new_shape.dim,
            input_producer->inputs[0], node->outputs[0],
            node->flags | XNN_NODE_FLAG_DONT_ELIDE),
        "Failed to create Binary Addition node.");
    node = move_last_node_to(subgraph, node_id);
    node->inputs[0] = input_producer->inputs[0];
    input_value = &subgraph->values[node->inputs[0]];
    if (input_value->first_consumer == input_producer_id) {
      input_value->first_consumer = node->id;
    }
...
    (*changes)++;
  }

```

This append is unsafe because [`xnn_subgraph_add_nodes`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=251) explicitly reallocates `subgraph->nodes` when the current slab is full:

At [`xnn_subgraph_add_nodes`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/xnnpack/src/src/subgraph.c;l=251), adding one node can move the entire node array, and invalidate the backing pointer [1], and thus leading to the UAF.

```
enum xnn_status xnn_subgraph_add_nodes(xnn_subgraph_t subgraph,
                                       size_t num_nodes) {
  struct xnn_node* nodes = subgraph->nodes;
  const size_t size = subgraph->num_nodes;
  const size_t capacity = subgraph->num_reserved_nodes;

  if (capacity < size + num_nodes) {
    const size_t new_capacity =
        max(min(capacity * 2, capacity + 512), capacity + max(num_nodes, 64));
    assert(new_capacity >= size + num_nodes);
    nodes =
        xnn_reallocate_memory(nodes, new_capacity * sizeof(struct xnn_node));
    if (nodes == NULL) {
      xnn_log_error("failed to allocate %zu bytes for subgraph nodes",
                    new_capacity * sizeof(struct xnn_node));
      return xnn_status_out_of_memory;
    }

    subgraph->num_reserved_nodes = new_capacity;
    subgraph->nodes = nodes;
  }
  subgraph->num_nodes = size + num_nodes;
  struct xnn_node* new_nodes = nodes + size;
  for (size_t i = 0; i < num_nodes; i++) {
    xnn_node_clear(&new_nodes[i]); // [1] invalidate the backing nodes
    new_nodes[i].id = size + i;
  }

  return xnn_status_success;
}

```
### Bisection

This issue is introduced by the commit <https://source.chromium.org/chromium/_/chromium/external/github.com/google/XNNPACK/+/e7276ec1410d8a132b8cf4da410b1eaafd1a5262>, which introduce the incorrect implementation of reshape.

### Reproduction

Run chrome from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1598914.zip` with the following command:

```
./chrome --enable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork --no-sandbox poc.html

```

You would observe the UAF shown in `asan.txt`

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 98.5 KB)
- [poc.html](attachments/poc.html) (text/html, 515 B)

## Timeline

### dc...@chromium.org (2026-03-16)

I was able to reproduce on Mac with `-enable-features=WebMachineLearningNeuralNetwork --disable-features=WebNNCoreML`. Tagging similarly to the other WebNN issues since I think this depends on changing features from their default state.

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6340901542592512.

### 24...@project.gserviceaccount.com (2026-03-16)

Detailed Report: https://clusterfuzz.com/testcase?key=6340901542592512

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7b41869041f8
Crash State:
  define_copy_node
  xnn_define_static_reshape
  xnn_subgraph_optimize_common_subgraphs
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1599928

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6340901542592512

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ds...@google.com (2026-03-16)

Likely fix is here: cl/884627086. I haven't tested it with the reported reproducer (I'm not set up to build and test Chrome), but the fix basically means that we don't call `xnn_subgraph_add_nodes` here any more.

### ds...@google.com (2026-03-16)

External PR: <https://github.com/google/XNNPACK/pull/9699>

### re...@chromium.org (2026-03-16)

Confirmed that the PR in [comment #6](https://issues.chromium.org/issues/492450480#comment6) resolves the ASan error.

### 24...@project.gserviceaccount.com (2026-03-16)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Reilly Grant [reillyg@chromium.org](mailto:reillyg@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7676838>

Roll TFLite/LiteRT to Next Green Version

---


Expand for full commit details
```
     
    Version Changes: 
    XNNPACK: b1ba7db0d48be76c032061b98d68f094b066e53e to ee91cc745bc715bfa38c5e8241aeb435ca59f433 
    tflite: da1b60beb415211263748ba44021921876192556 to 24d66fbe6c5e87d291207494e4e83d39de3f7d90 
    litert: 2d7ebf8846ee010e4766c925c228bdea993f7322 to 13469058b8ee37e2153481ba49644764666ad275 
     
    Bug: 388311883 
    Fixed: 492450480 
    Cq-Include-Trybots: luci.chrome.try:optimization_guide-linux;luci.chrome.try:optimization_guide-mac-arm64;luci.chrome.try:optimization_guide-mac-x64;luci.chrome.try:optimization_guide-win32;luci.chrome.try:optimization_guide-win64 
    Include-Ci-Only-Tests: chromium.android:android-pie-arm64-rel|android_browsertests 
    Change-Id: Iaee681d6d88a7187f81088bd674bd36dda7a62b0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7676838 
    Commit-Queue: Reilly Grant <reillyg@chromium.org> 
    Auto-Submit: Reilly Grant <reillyg@chromium.org> 
    Reviewed-by: Steven Holte <holte@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600937}

```

---

Files:

- M `DEPS`
- M `third_party/litert/README.chromium`
- M `third_party/litert/src`
- M `third_party/tflite/README.chromium`
- M `third_party/tflite/src`
- M `third_party/xnnpack/README.chromium`
- M `third_party/xnnpack/build_identifier.c`
- M `third_party/xnnpack/src`

---

Hash: [5c4eff139a71fe4847e257f46ba94ad0f63329cb](https://chromiumdash.appspot.com/commit/5c4eff139a71fe4847e257f46ba94ad0f63329cb)  

Date: Wed Mar 18 01:09:15 2026


---

### 24...@project.gserviceaccount.com (2026-03-18)

ClusterFuzz testcase 6340901542592512 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1600934:1600942

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### re...@chromium.org (2026-03-19)

This fix has been on Canary for 24 hours. Requesting a merge.

### ch...@google.com (2026-03-19)

Merge review required: a commit with DEPS changes was detected.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### re...@chromium.org (2026-03-19)

**Why does your merge fit within the merge criteria for these milestones?**  

It is a security issue.

**What changes specifically would you like to merge? Please link to Gerrit.**  

<https://github.com/google/XNNPACK/pull/9699> needs to be manually cherry-picked onto <https://chromium.googlesource.com/external/github.com/google/XNNPACK/+/refs/heads/chromium/7727>.

**Have the changes been released and tested on canary?**  

Yes.

**Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?**  

Yes. It is enabled by default but kill-switchable with the `WebMachineLearningNeuralNetwork` flag.

**If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.**  

No.

### dr...@chromium.org (2026-03-20)

No crashes in Canary. Merge approved to M147.

### re...@chromium.org (2026-03-20)

Cherry-pick out for review: <https://chromium-review.git.corp.google.com/c/external/github.com/google/XNNPACK/+/7689939>

### dx...@google.com (2026-03-20)

Project: external/github.com/google/XNNPACK  

Branch:  chromium/7727  

Author:  Reilly Grant [reillyg@google.com](mailto:reillyg@google.com)  

Link:    <https://chromium-review.googlesource.com/7689939>

[M147] Fix crash when rewriting reshape(reshape(x))

---


Expand for full commit details
```
     
    This rewrite reused pointers across a call that could have reallocated the nodes array. In this case, I think we should simply not add the node? It's unclear why the reshape fusion does this, but reshape(expand_dims(x)) or other rewrites do not. The existing reshape was already being modified/invalidated anyways (by the `xnn_shape_fill_gaps` call). 
     
    (Cherry-picked from commit 474163f8aec45c77b48009eef6bb62886c3f25bd.) 
     
    PiperOrigin-RevId: 884666280 
    Bug: 492450480 
    Change-Id: I493e2c400574044840c171361f2688da76f1fe1c

```

---

Files:

- M `src/subgraph.c`

---

Hash: [1d9165389e59d29915d88d1cf5cac2ab23b48954](https://chromiumdash.appspot.com/commit/1d9165389e59d29915d88d1cf5cac2ab23b48954)  

Date: Fri Mar 20 23:46:04 2026


---

### aj...@google.com (2026-04-01)

Sev=High as !Android

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality.  Memory corruption in a sandboxed process with bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492450480)*
