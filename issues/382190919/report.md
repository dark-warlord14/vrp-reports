# Array out-of-bounds access vulnerability in the maglev phi untagging optimization.

| Field | Value |
|-------|-------|
| **Issue ID** | [382190919](https://issues.chromium.org/issues/382190919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-12-04 |
| **Bounty** | $20,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

## 1 Maglev Graph Build

During optimization, the Graph constructed by Maglev based on bytecode is roughly as follows, and I have annotated the corresponding JS code for each part in the graph.

```
After graph building
    ...
    Block b2 
     14: ReduceInterruptBudgetForLoop(13)  
         ↳ lazy @22 (4 live vars)
     16: Jump b3
      │  with gap moves:
      │    - n17:(x) → 19: φᵀ r0 (x)
      │    - n18:(x) → 20: φᵀ r3 (x)
      ▼
╭──►Block b3 peeled (effects:)    // for (let i = 0; i < 5; i++) {
│    19: φᵀ r0 (n17, n30) (compressed) → (x), 21 uses
│    20: φᵀ r3 (n18, n31) (compressed) → (x), 2 uses 
│    21: CheckedSmiUntag [n20:(x)] → (x), 3 uses
│    22: Int32Compare(LessThan) [n21:(x), n10:(x)] → (x), 0 uses 🪦 
│╭───23: BranchIfInt32Compare(LessThan) [n21:(x), n10:(x)] b4 b5
││    ↓
││  Block b4     // loop body
││   25: CheckedSmiUntag [n19:(x)] → (x), 1 uses 
││   26: Int32DecrementWithOverflow [n25:(x)] → (x), 2 uses // v3--
││   27: Int32IncrementWithOverflow [n21:(x)] → (x), 2 uses 
││   28: ReduceInterruptBudgetForLoop(13) 
││   30: Int32ToNumber [n26:(x)] → (x), 1 uses
││   31: Int32ToNumber [n27:(x)] → (x), 1 uses
╰──◄─29: JumpLoop b3
 │       with gap moves:
 │         - n30:(x) → 19: φᵀ r0 (x)
 │         - n31:(x) → 20: φᵀ r3 (x)
 │ 
 ╰─►Block b5
        // use_v3 = v3; 
     32: LoadTaggedFieldForContextSlot(0x14, compressed) [n3:(x)] → (x), 1 uses
     33: ThrowReferenceErrorIfHole [n32:(x)] 
     34: CheckSmi [n19:(x)]
     35: StoreTaggedFieldNoWriteBarrier(0x14) [n3:(x), n19:(x)] 
        // Reflect.apply();
     40: 🐢 CallKnownJSFunction(0x09b10025d6a9 <SharedFunctionInfo apply>) [n38:(x), n39:(x), n37:(x), n4:(x)] → (x), 0 uses, but required
╭────41: Jump b7
│        with gap moves:
│          - n36:(x) → 56: φᵀ r1 (x)
│  
│   Block b6 (exception handler)
│    42: φᵀₑ <accumulator> (compressed) → (x), 1 uses
│    ...
│    55: Jump b7
│     │  with gap moves:
│     │    - n36:(x) → 56: φᵀ r1 (x)
│     ▼
╰┬─►Block b7 (effects: ua)    // the body of the do-while loop
 │   56: φᵀ r1 (n36, n36, n19) (compressed) → (x), 1 uses     // This phi node represents v15 and v3
 │   58: 🐢 CallBuiltin(KeyedStoreIC_Megamorphic) [n57:(x), n56:(x), n18:(x), n3:(x)] → (x), 0 uses, but required 
 │   61: ReduceInterruptBudgetForLoop(7) 
 │   62: Jump b8
 │    │  with gap moves:
 │    │    - n63:(x) → 64: φᵀ r2 (x)
 │    ▼
 │╭►Block b8 peeled (effects:)    // empty loop: for (let i40 = 100; i40; --i40) {}
 ││  64: φᵀ r2 (n63, n70) (compressed) → (x), 3 uses 
 ││╭──65: BranchIfToBooleanTrue [n64:(x)] b9 b10
 │││   ↓
 │││ Block b9 
 │││  66: CheckedSmiUntag [n64:(x)] → (x), 1 uses
 │││  67: Int32DecrementWithOverflow [n66:(x)] → (x), 2 uses 
 │││  68: ReduceInterruptBudgetForLoop(7) 
 │╰─◄─69: JumpLoop b8
 │ │      with gap moves:
 │ │        - n70:(x) → 64: φᵀ r2 (x)
 │ │
 │ ╰►Block b10
 │╭───71: BranchIfReferenceEqual [n19:(x), n8:(x)] b12 b11    // Determine whether the do-while loop should continue
 ││    ↓
 ││  Block b11
 ││   72: ReduceInterruptBudgetForLoop(27) 
 ╰──◄─73: JumpLoop b7    // backedge for do-while loop
  │       with gap moves:
  │         - n19:(x) → 56: φᵀ r1 (x)
  │ 
  ╰─►Block b12
    ...

```

The above Maglev Graph can be represented as the following CFG.

```
    B3 <--+    // for (let i = 0; i < 5; i++) { ... }
    |\    |  
    | +-->B4 
    |
    V
    B5        B6 (exception handler)    // try-catch
    |         |
    +---------+
        |
        V
   +--> B7    // do { ... }while();
   |    |
   |    V
   |    B8<---+    // for (let i40 = 100; i40; --i40) { }
   |    |\    |
   |    | +->B9
   |    V  
   |    B10
   |    |
   |    V
   +----B11

```

We need to pay special attention to `56: φᵀ r1 (n36, n36, n19)` node in `B7`, this special Phi has three input nodes.

## 2 Maglev Phi Untagging

`MaglevPhiRepresentationSelector::PreProcessBasicBlock()` is applied to every BasicBlock in the Maglev Graph, and the function is as follows.

```
BlockProcessResult MaglevPhiRepresentationSelector::PreProcessBasicBlock(
    BasicBlock* block) {
  // Previously processing current_block_, now preparing to handle block
  PreparePhiTaggings(current_block_, block);
  current_block_ = block;

  if (block->has_phi()) {  
    auto& phis = *block->phis();

    auto first_retry = phis.begin();
    auto end_retry = first_retry;
    bool any_change = false;

    for (auto it = phis.begin(); it != phis.end(); ++it) { 
      Phi* phi = *it;
      switch (ProcessPhi(phi)) {   // Optimizing the type of phi node
        ...
      }
    }
    ...
  }

  return BlockProcessResult::kContinue;
}

```

The crash occurs during the process of `PreProcessBasicBlock()` handling `B7`.

We need to pay attention to two functions within it: `PreparePhiTaggings()` and `ProcessPhi()`.

## 3 Add elements to merge\_values\_

1. `MaglevPhiRepresentationSelector::PreparePhiTaggings()`

```
void MaglevPhiRepresentationSelector::PreparePhiTaggings(
    BasicBlock* old_block, const BasicBlock* new_block) {
  ...
  // Clear the predecessor list
  predecessors_.clear();

  if (!new_block->is_merge_block()) {    // If it's not a merge block, this block only has one predecessor
    BasicBlock* pred = new_block->predecessor();    // Get the predecessor of this block
    predecessors_.push_back(pred->snapshot());    // Put it into predecessors_
  } else {    // If it's a merge block, the merge block must have multiple predecessors (such as back edge or merge edge of if)
    int skip_backedge = new_block->is_loop();    // Determine if it is a loop
    for (int i = 0; i < new_block->predecessor_count() - skip_backedge; i++) {
      BasicBlock* pred = new_block->predecessor_at(i);    // Get the predecessor of new_block
      predecessors_.push_back(pred->snapshot());    // Only two elements will be placed in predecessors_
    }
  }
  ...

  // Start a new snapshot based on predecessors_ 
  phi_taggings_.StartNewSnapshot(base::VectorOf(predecessors_), merge_taggings);
}

```

This function collects predecessor nodes other than `LoopJump`. `B7` has three predecessor BasicBlocks: `B5, B6, B11`. Among them, `B11` is `LoopJump`, which will be skipped, so the `predecessors_ = {B5->snapshot(), B6->snapshot()}` is passed into `StartNewSnapshot()` (later written as `B5->snapshot()` as `S5`, the rest is the same).

Debugging found that since `B6` has no input nodes, `S6 = root_snapshot_`. The SnapshotTable at this time is as follows.

```
    root_snapshot_, S6, log: [0, 0)
            |
           /
          /
         /
       S5, log: [0, 1) 

```

2. `SnapshotTable::StartNewSnapshot()` will call two functions for processing.

```
template <class Value, class KeyData = NoKeyData>
class SnapshotTable {
  void StartNewSnapshot(base::Vector<const Snapshot> predecessors,
                        const MergeFun& merge_fun,
                        const ChangeCallback& change_callback = {}) {
    StartNewSnapshot(predecessors, change_callback);
    MergePredecessors(predecessors, merge_fun, change_callback);
  }
}

```

3. `StartNewSnapshot()` will find the nearest common ancestor node of `{S5, S6}`, which is `root_snapshot_`, and then create `S7` with `root_snapshot_` as the parent node. The SnapshotTable is as follows.

```
    root_snapshot_, S6, log: [0, 0)
            |        |
           /          \
          /            \
         /              \
       S5, log: [0, 1)   \
                        S7, log: [1, Invaild)

```

4. `MergePredecessors()`

```
template <class Value, class KeyData>
template <class MergeFun, class ChangeCallback>
void SnapshotTable<Value, KeyData>::MergePredecessors(
    base::Vector<const Snapshot> predecessors, const MergeFun& merge_fun,
    const ChangeCallback& change_callback) {
  ...

  SnapshotData* common_ancestor = current_snapshot_->parent;    // root_snapshot_

  for (uint32_t i = 0; i < predecessor_count; ++i) {
    for (SnapshotData* predecessor = predecessors[i].data_; 
         predecessor != common_ancestor; predecessor = predecessor->parent) { 
      base::Vector<LogEntry> log_entries = LogEntries(predecessor);
      for (const LogEntry& entry : base::Reversed(log_entries)) {
        RecordMergeValue(entry.table_entry, entry.new_value, i,
                         predecessor_count);
      }
    }
  }
  ...
}

```

This method will traverse the `LogEntry` of `SnapshotData` between `[predecessor, common_ancestor)`. In this case,

- For `S5`, it will access `[S5, root_snapshot_)`, which is the `LogEntry` in `S5`, and then call `RecordMergeValue()` for processing.
- For `S6`, `[S6, root_snapshot_)` is empty.

```
    root_snapshot_, S6, log: [0, 0)    <== common_ancestor
            |        |
           /          \
          /            \
         /              \
       S5, log: [0, 1)   \
                        S7, log: [1, Invaild)    <== current_snapshot_

```

5. `RecordMergeValue()`

```
template <class Value, class KeyData>
void SnapshotTable<Value, KeyData>::RecordMergeValue(
    TableEntry& entry,  
    const Value& value, 
    uint32_t predecessor_index,    // 0
    uint32_t predecessor_count    // 2
) {

  if (predecessor_index == entry.last_merged_predecessor) {
    ...
  }

  if (entry.merge_offset == kNoMergeOffset) { 
    // Reserve predecessor_count elements in merge_values_
    entry.merge_offset = static_cast<uint32_t>(merge_values_.size());
    merging_entries_.push_back(&entry);
    merge_values_.insert(merge_values_.end(), predecessor_count, entry.value);
  }

  merge_values_[entry.merge_offset + predecessor_index] = value;
  entry.last_merged_predecessor = predecessor_index;
}

```

Note: When `RecordMergeValue()` processes the `LogEntry` in `S5`, `predecessor_index = 0`, and `predecessor_count = 2`. Therefore, **`merge_values_.insert()` will insert two slots in the array**.

## 4 Access merge\_values\_

Then, it will enter the `ProcessPhi()` method to optimize `phi`. The crash occurs when `ProcessPhi()` handles `56: φᵀ r1 (n36, n36, n19)` in `B7`.

By adding the `--trace-maglev-phi-untagging` option, you can see that before optimizing `n56`, its input phi node `n19: phi` will be optimized to the `Int32` type by `ProcessPhi()`.

```
Considering for untagging: n19
  + use_reprs  : {Int32}
  + input_reprs: {Int32}
  + intersection reprs: {Int32}
  => Untagging to Int32
    @ Input 0 (n17): Making Int32 instead of Smi
    @ Input 1 (n30): Bypassing conversion
...

Considering for untagging: n56
  + use_reprs  : {Tagged}
  + input_reprs: {Int32, Float64}
  => Leaving tagged [incompatible uses]

```

1. `ProcessPhi()`

```
MaglevPhiRepresentationSelector::ProcessPhiResult
MaglevPhiRepresentationSelector::ProcessPhi(Phi* node) {
  ...
  ValueRepresentationSet input_reprs;   
  ...
  bool has_tagged_phi_input = false;   
  for (int i = 0; i < node->input_count(); i++) {  
    ValueNode* input = node->input(i).node();
    if (input->Is<SmiConstant>()) {   
      ...
    } else if (Constant* constant = input->TryCast<Constant>()) { 
      ...
    } else if (input->properties().is_conversion()) {  
      ...
    } else if (Phi* input_phi = input->TryCast<Phi>()) {   
      ...
    } else { 
      ...  
      // If the input is tagged, and it is not required to perform tagging operations to become tagged
      // Then we will not perform hosit operations, nor will we carry out untag optimizations
      input_reprs.RemoveAll();
      break;
    }
  }

  // Get the usage information of phi
  UseRepresentationSet use_reprs;
  if (node->is_loop_phi() && !node->get_same_loop_uses_repr_hints().empty()) {
    // {node} is a loop phi that has uses inside the loop; we will tag/untag
    // based on those uses, ignoring uses after the loop.
    use_reprs = node->get_same_loop_uses_repr_hints();
  } else {
    use_reprs = node->get_uses_repr_hints();
  }
  ...
  
  if (use_reprs.contains(UseRepresentation::kTagged) ||
      use_reprs.contains(UseRepresentation::kUint32) || use_reprs.empty()) {
    // For phi nodes used as tagged types, we will not perform untagged operations
    TRACE_UNTAGGING("  => Leaving tagged [incompatible uses]");
    EnsurePhiInputsTagged(node);
    return default_result;
  }
  ...
}

```

`ProcessPhi()` first calculates two sets of types:

- `input_reprs`: The representation of the input nodes of `phi`. The input node `n36` of `n56` is of `Int32` type, and `n19` is also a phi node, but it has been optimized to `Float64` type. So for `n56`, `input_reprs={Int32, Float64}`.
- `use_reprs`: The value of `phi` will be used as what type. In this case, the value of `n56` will only be used as tagged.

Since the value of `n56` is used as a tagged type, `ProcessPhi()` gives up the optimization for this node, calls `EnsurePhiInputsTagged()` to ensure that all input nodes of `n56` are tagged, and then exits.

2. `EnsurePhiInputsTagged()`

```
void MaglevPhiRepresentationSelector::EnsurePhiInputsTagged(Phi* phi) { 
  for (int i = 0; i < phi->input_count(); i++) {    // Traverse all inputs of Phi
    ValueNode* input = phi->input(i).node();    // Get the input node  
    if (Phi* phi_input = input->TryCast<Phi>()) {    // If it is a phi node
      phi->change_input(    // Perform tagging operation for this input phi node
          i, EnsurePhiTagged(phi_input, phi->predecessor_at(i),
                             NewNodePosition::kEndOfBlock, nullptr, i));
    } else {
      ...
    }
  }
}

```

`EnsurePhiInputsTagged()` traverses the `phi` nodes in the input nodes of `n56`, that is, `n19`, and calls `EnsurePhiTagged()` to ensure that the value of the phi node `n19` is tagged.

Note: `n19` is the third input node of `n56`, so the `predecessor_index` parameter passed into `EnsurePhiTagged()` is `2`.

3. `EnsurePhiTagged()`

```
ValueNode* MaglevPhiRepresentationSelector::EnsurePhiTagged(
    Phi* phi,     // n19
    BasicBlock* block, 
    NewNodePosition pos,
    const ProcessingState* state, 
    std::optional<int> predecessor_index    // 2
  ) {
  ...

  // Try to find an existing Tagged conversion for {phi} in {phi_taggings_}.
  if (phi->has_key()) {
    if (predecessor_index.has_value()) {    // 2
      if (ValueNode* tagging = phi_taggings_.GetPredecessorValue(    // <==
              phi->key(), predecessor_index.value())) {
        return tagging;
      }
    } else {
      if (ValueNode* tagging = phi_taggings_.Get(phi->key())) {
        return tagging;
      }
    }
  }
  ...
}

```

`EnsurePhiTagged()` first calls `phi_taggings_.GetPredecessorValue()` to query whether the untagged phi node `n19` has been tagged before. If it has, it gets the node and directly returns it.

4. `GetPredecessorValue()`

```
template <class Value, class KeyData = NoKeyData>
class SnapshotTable {
  ...
  const Value& GetPredecessorValue(Key key, int predecessor_index) {
    if (key.entry_->merge_offset == kNoMergeOffset)  return Get(key);
    return merge_values_[key.entry_->merge_offset + predecessor_index];
  }
}

```

Finally, we've arrived at the point where an array out-of-bounds error occurs. The `SnapshotTable::RecordMergeValue()` method inserts two elements into `merge_values_`. However, when querying, `key.entry_->merge_offset=0, predecessor_index = 2`, so it will access `merge_values_[2]`, leading to an array out-of-bounds error.

This out-of-bounds range might lead to the construction of an incorrect Maglev Graph in the phi untagging, which is a complex vulnerability. I'm not sure if it can be exploited.

## 5 Commit Bisect

After analyzing the source code, I am confident that this vulnerability originates from commit: `c3935610c0f95c93b48e5647ec59bf855df58c64`.

This means that this vulnerability was introduced on 5/8/2023, at a time when the `maglev` compiler was not even enabled by default. I am surprised that this vulnerability has survived for so long.

VERSION

V8: from commit c3935610c0f95c93b48e5647ec59bf855df58c64 to the latest version.

REPRODUCTION CASE

`poc.js`:

```
let use_v3;
let obj = {};

function f1() {
  
    // Create a phi node and trigger the maglev untagged optimization
    let v3 = 5;
    for (let i = 0; i < 5; i++) {
        v3--;
    }
    use_v3 = v3;    // Prevent v3 from being deleted

    let v15 = 1.2;

    // The try statement and the catch statement each have a path that leads to do{...}while()
    try {
        Reflect.apply();    // Used to throw an exception
    } catch(e) {
    }

    // The BasicBlock corresponding to do{...}while() has three incoming edges: 
    // the try statement, the catch statement, and the loop's back edge
    do {
        obj[v15] = 1;   // tagged use of v3
        v15 = v3;
        for (let i40 = 100; i40; --i40) {
        }
    } while (v3);
}

%PrepareFunctionForOptimization(f1);
f1();
f1();
%OptimizeMaglevOnNextCall(f1);
f1();

```

Run the following with a debug-compiled version of V8:

```
./d8 \
    --allow-natives-syntax \
    ./poc.js

```

You will get the following crash:

```
#
# Fatal error in ../../src/zone/zone-containers.h, line 247
# Debug check failed: pos < size() (2 vs. 2).
#

```

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: 303f06e3

## Timeline

### cl...@appspot.gserviceaccount.com (2024-12-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6565510997016576.

### 24...@project.gserviceaccount.com (2024-12-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-12-04)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/bc5ebd949c2dea946f4493942db460ecb56e0652 ([fuzzing] Allow OptimizeMaglevOnNextCall for fuzzing

Without adding this to the allow-list, https://crrev.com/c/4124118 was
likely having no effect.

Bug: v8:7700
Change-Id: Idee1e44d42aea19b3388765c7ae666c743dd88c3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4967414
Commit-Queue: Michael Achenbach <machenbach@chromium.org>
Reviewed-by: Carl Smith <cffsmith@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90547}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-12-04)

Detailed Report: https://clusterfuzz.com/testcase?key=6565510997016576

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  pos < size() in zone-containers.h
  v8::internal::ZoneVector<v8::internal::maglev::ValueNode*>::at
  v8::internal::maglev::MaglevPhiRepresentationSelector::EnsurePhiTagged
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90546:90547

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6565510997016576

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### am...@chromium.org (2024-12-04)

Thanks for the super detailed report, 303f06e3! Very nice find and thank you for finding and reporting this.

The POC did indeed reproduce. I don't trust Clusterfuzz's bisect since it bisecting to adding kOptimizeMaglevOnNextCall to the allow list for fuzzing.
But it does concur that this has been around for sometime. Assigning to dmercadier@ instead based on <https://crrev.com/c/4442189>.

### cl...@appspot.gserviceaccount.com (2024-12-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5514499465347072.

### ma...@chromium.org (2024-12-05)

The bisect is correct, but can be improved. Before [this](https://chromium-review.googlesource.com/c/v8/v8/+/4967414), `%OptimizeMaglevOnNextCall` was not allowed to be used during fuzzing. But we can bisect further back by rewriting the test to use `%OptimizeFunctionOnNextCall` and the flag --optimize-on-next-call-optimizes-to-maglev.

I reuploaded a case [here](https://clusterfuzz.com/testcase-detail/5514499465347072) with this modification.

### dm...@chromium.org (2024-12-05)

Fun one, thanks for the report.

This can likely lead to type confusion: instead of an OOB access into the snapshot table, we could instead create additional Phis and retagging before, such that we use an incorrect input for the backedge (ie, the retagging of another Phi) (since merge\_values\_ in the snapshot table is one big array for all the phi inputs of all phi, and not one array per phi). Then, if this new phi flows into something that was assuming a specific shape (because the graph builder determined this shape based on the initial inputs of the phi), then we could be assuming the wrong shape for an object, hence the type confusion.

Fix incoming (<https://crrev.com/c/6074772>).

### pe...@google.com (2024-12-05)

Setting milestone because of s0/s1 severity.

### hu...@gmail.com (2024-12-05)

Yes, that's exactly what I thought, it's not a simple array out-of-bounds vulnerability.

### ap...@google.com (2024-12-05)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6074772>

[maglev] Avoid retagging loop phi backedges too early

---


Expand for full commit details
```
[maglev] Avoid retagging loop phi backedges too early 
 
When we decide that a loop phi should remain tagged, we call 
EnsurePhiInputsTagged to ensures that it only has tagged inputs, which 
calls EnsurePhiTagged, which might cause retagging of any untagged 
phi it has as input. 
 
In order to avoid retagging multiple times the same Phi, we have a 
SnaphotTable (`phi_taggings_`), which records existing tagging in the 
predecessors, and in which EnsurePhiTagged looks to avoid creating 
new retagging nodes. For loop phis, the backedge predecessor won't 
have an entry yet in this SnapshotTable (since we only visit loops 
once, this has to be the first time we visit the header and thus 
we can't have already visited the backedge block), and we should 
thus not call EnsurePhiTagged on the backedge. 
 
Note that the backedge input will anyways be properly tagged when 
FixLoopPhisBackedge is later called from the JumpLoop backedge. 
 
Fixed: chromium:382190919 
Change-Id: I5452ab41b3b37de3232d387b2414c0f5650bbfa9 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6074772 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97578}

```

---

Files:

- M `src/maglev/maglev-phi-representation-selector.cc`
- A `test/mjsunit/maglev/regress-382190919.js`

---

Hash: e4ecfc909687511aeb20b88ce6ae2a7a1a80afe5  

Date:  Thu Dec 05 16:03:33 2024


---

### pe...@google.com (2024-12-06)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-12-06)

Merge review required: M132 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-12-06)

Merge review required: M131 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-12-06)

Merge review required: M130 is already shipping to stable.

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

### am...@chromium.org (2024-12-10)

<https://crrev.com/c/6074772> approved for merges; please merge to 13.2 asap, so this fix can be included in next Beta. Please merge to 13.1 and 13.0 NLT EOD Thursday 12 December so this fix can be included in next weeks' Stable and Extended Stable updates.

### ap...@google.com (2024-12-11)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6084685>

Merged: [maglev] Avoid retagging loop phi backedges too early

---


Expand for full commit details
```
Merged: [maglev] Avoid retagging loop phi backedges too early 
 
When we decide that a loop phi should remain tagged, we call 
EnsurePhiInputsTagged to ensures that it only has tagged inputs, which 
calls EnsurePhiTagged, which might cause retagging of any untagged 
phi it has as input. 
 
In order to avoid retagging multiple times the same Phi, we have a 
SnaphotTable (`phi_taggings_`), which records existing tagging in the 
predecessors, and in which EnsurePhiTagged looks to avoid creating 
new retagging nodes. For loop phis, the backedge predecessor won't 
have an entry yet in this SnapshotTable (since we only visit loops 
once, this has to be the first time we visit the header and thus 
we can't have already visited the backedge block), and we should 
thus not call EnsurePhiTagged on the backedge. 
 
Note that the backedge input will anyways be properly tagged when 
FixLoopPhisBackedge is later called from the JumpLoop backedge. 
 
Fixed: chromium:382190919 
(cherry picked from commit e4ecfc909687511aeb20b88ce6ae2a7a1a80afe5) 
 
Change-Id: I9742967003cf108b0805601a4f9bc6d9934e734f 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6084685 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Camillo Bruni <cbruni@chromium.org> 
Commit-Queue: Camillo Bruni <cbruni@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#38} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/maglev/maglev-phi-representation-selector.cc`
- A `test/mjsunit/maglev/regress-382190919.js`

---

Hash: be40691f8a4dd37fd3cea9d5550d1665ff7b986d  

Date:  Thu Dec 05 16:03:33 2024


---

### pe...@google.com (2024-12-11)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
high-quality report of V8 security bug that impacts Stable and older versions of Chrome


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Congratulations 303f06e3! Thank you for your efforts and your most excellent reporting of this issue -- amazing work! If we had a `Prettiest Bug Report` award it would definitely go to you! 🏆🐛📜

### am...@chromium.org (2024-12-12)

=======================================================
| @~ @~ @~ @~ @~ @~ @~ @~ ~@ ~@ ~@ ~@ ~@ ~@ ~@ ~@ |
|                                                                                                                   |
|                                                This award for                                          |
|                                  Prettiest Security Bug Report                               |
|                                             is presented by                                            |
|                                            Chrome Security                                           |
|                                                        to                                                        |
|                              303f06e3  for crbug.com/382190919                     |
|                                                        on                                                       |
|                                          11 December 2024                                        |
|                                                                                                                   |
| @~ @~ @~ @~ @~ @~ @~ @~ ~@ ~@ ~@ ~@ ~@ ~@ ~@ ~@ |
======================================================

This report was so pretty, we made an award especially for you and this report. :) 

### hu...@gmail.com (2024-12-12)

Haha, thank you for your special reward. Detailed reports can aid in fixing vulnerabilities, and also help other researchers learn about V8. I believe it's a thing worth doing

### pe...@google.com (2024-12-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-12-12)

1. https://chromium-review.googlesource.com/c/v8/v8/+/6089731
2. Low - There was no conflict.
3. 132
4. Yes. According to comment #8, the bisect was correct. So,  M126 contains the suspected CL[1].

[1] https://chromium-review.googlesource.com/c/v8/v8/+/4442189

### ol...@chromium.org (2024-12-12)

Merged to 13.1 and 13.0 too in <https://chromium-review.googlesource.com/c/v8/v8/+/6087795> and <https://chromium-review.googlesource.com/c/v8/v8/+/6084686>

Not sure why they don't show up here...

### pe...@google.com (2024-12-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2025-01-27)

Project: v8/v8  

Branch: refs/branch-heads/12.6  

Author: Darius Mercadier <[dmercadier@chromium.org](mailto:dmercadier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6089731>

[M126-LTS][maglev] Avoid retagging loop phi backedges too early

---


Expand for full commit details
```
[M126-LTS][maglev] Avoid retagging loop phi backedges too early 
 
When we decide that a loop phi should remain tagged, we call 
EnsurePhiInputsTagged to ensures that it only has tagged inputs, which 
calls EnsurePhiTagged, which might cause retagging of any untagged 
phi it has as input. 
 
In order to avoid retagging multiple times the same Phi, we have a 
SnaphotTable (`phi_taggings_`), which records existing tagging in the 
predecessors, and in which EnsurePhiTagged looks to avoid creating 
new retagging nodes. For loop phis, the backedge predecessor won't 
have an entry yet in this SnapshotTable (since we only visit loops 
once, this has to be the first time we visit the header and thus 
we can't have already visited the backedge block), and we should 
thus not call EnsurePhiTagged on the backedge. 
 
Note that the backedge input will anyways be properly tagged when 
FixLoopPhisBackedge is later called from the JumpLoop backedge. 
 
(cherry picked from commit e4ecfc909687511aeb20b88ce6ae2a7a1a80afe5) 
 
Fixed: chromium:382190919 
Change-Id: I5452ab41b3b37de3232d387b2414c0f5650bbfa9 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6074772 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#97578} 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6089731 
Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Cr-Commit-Position: refs/branch-heads/12.6@{#86} 
Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2} 
Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

```

---

Files:

- M `src/maglev/maglev-phi-representation-selector.cc`
- A `test/mjsunit/maglev/regress-382190919.js`

---

Hash: 5c4b4ba808a404476aa13bca8ebf55a7d28439a3  

Date:  Thu Dec 05 16:03:33 2024


---

### ch...@google.com (2025-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high-quality report of V8 security bug that impacts Stable and older versions of Chrome

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/382190919)*
