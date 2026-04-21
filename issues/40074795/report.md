# Uaf in EmbeddedPermissionPrompt::~EmbeddedPermissionPrompt And defects in raw_ptr with ASAN

| Field | Value |
|-------|-------|
| **Issue ID** | [40074795](https://issues.chromium.org/issues/40074795) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2023-10-13 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

commit at a5a7c2b61c212a326ee6e6bd190048907417053e

1. compile Chromium with ASAN enabled
2. copy the `\*.mojom.js` file to the folder of `poc.html` and start a HTTP server
3. run `./chrome --enable-blink-features=MojoJS,MojoJSTest --enable-features=PermissionElement --user-data-dir=/tmp/noexist`
4. open two browser windows and navigate one to the `poc.html` then merge the two windows.

**Problem Description:**

1. Analysis  
   
   1.1 The Uaf  
   
   This is a very simple and classic pattern, `prompt_view_` is a raw\_ptr in Class `EmbeddedPermissionPrompt`[1], and `prompt_view_` could be deleted before `EmbeddedPermissionPrompt`, so when `EmbeddedPermissionPrompt` uses the freed `prompt_view_`, Uaf occurs.  
   
   In order to free the `prompt_view_`, we could merge two different Browser windows, this will free `promit_view_`, but will not free `EmbeddedPermissionPrompt`. You can see the poc.webm for more details.

```
EmbeddedPermissionPrompt::~EmbeddedPermissionPrompt() {  
  if (prompt_view_) {  
    prompt_view_->GetWidget()->Close();  
  }  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/embedded_permission_prompt.cc;l=114;bpv=0;bpt=1>

2. Bisect  
   
   This UAF is introduced in this commit: 2790300f72201c55a60ff9c7f83e03dcc85432d1  
   
   This commit affects Chrome Dev 120.0.6051.2
3. Patch  
   
   Maybe you should use a weak ptr to ensure the lifetime of `prompt_view_`.  
   
   Also, check the implement of raw\_ptr with ASAN.

**Additional Comments:**  

[Important] Uaf -> Overflow  

Apparently this Uaf is protected by MiraclePtr according to the `asan.txt`. However, after some debugging, I found that this Uaf could be transformed into a Heap-buffer-overflw.

Step :

1. compile Chromium with ASAN enabled
2. copy the `\*.mojom.js` file to the folder of `poc-overflow.html` and start a HTTP server
3. run `./chrome --enable-blink-features=MojoJS,MojoJSTest --enable-features=PermissionElement --user-data-dir=/tmp/noexist`
4. open two browser windows and navigate one to the `poc-overflow.html` then merge the two windows. When you see the MediaStream window, chose anyone to share, and you will see the overflow.  
   
   See the `poc-overflow.webm` for more details.

This is strange and I debug the Chromium with ASAN for a while to find the root cause:  

According to the debugging info, I find this code path: `GetForDereference`[2] => `SafelyUnwrapPtrForDereference`[3] => `SafelyUnwrapForDereference`[4].  

In `SafelyUnwrapForDereference`, `IsFreedHeapPointer` returns a false which means the `address` is not a freed heap pointer, so the condition of IF doesn't hold and `CrashImmediatelyOnUseAfterFree` will not be invoked. ==> No UAF will be reported by ASAN, so no raw\_ptr PROTECTED.

```
void SafelyUnwrapForDereference(uintptr_t address) {  
  if (RawPtrAsanService::GetInstance().is_dereference_check_enabled() &&  
      IsFreedHeapPointer(address)) {  // `IsFreedHeapPointer` return false!  
    RawPtrAsanService::SetPendingReport(  
        RawPtrAsanService::ReportType::kDereference,  
        reinterpret_cast<void\*>(address));  
    CrashImmediatelyOnUseAfterFree(address);  
  }  
}  

```

Then I analyze the code of `IsFreedHeapPointer` and find that line 34 - line 40 will return false.  

The `address >= region_base + region_size` is true, that's interesting.

```
bool IsFreedHeapPointer(uintptr_t address) {  
  // Use `__asan_region_is_poisoned` instead of `__asan_address_is_poisoned`  
  // because the latter may crash on an invalid pointer.  
  if (!__asan_region_is_poisoned(reinterpret_cast<void\*>(address), 1)) {  
    return false;  
  }  
  
  // Make sure the address is on the heap and is not in a redzone.  
  void\* region_ptr;  
  size_t region_size;  
  const char\* allocation_type = __asan_locate_address(  
      reinterpret_cast<void\*>(address), nullptr, 0, &region_ptr, &region_size);  
  
  auto region_base = reinterpret_cast<uintptr_t>(region_ptr);  
  if (strcmp(allocation_type, "heap") != 0 || address < region_base ||  
      address >=    //@audit the `address >= region_base + region_size` is true and will return false directly!  
          region_base + region_size) {  // We exclude pointers one past the end  
                                        // of an allocations from the analysis  
                                        // for now because they're to fragile.  
    return false;  
  }  
  
  // Make sure the allocation has been actually freed rather than  
  // user-poisoned.  
  int free_thread_id = -1;  
  __asan_get_free_stack(region_ptr, nullptr, 0, &free_thread_id);  
  return free_thread_id != -1;  
}  

```

Next I analyze the code in `__asan_locate_address` to figure out why `region_base` and `region_size` is less than `address`. And finally I find this function `FindHeapChunkByAddress`[6], the returned AsanChunkView of `FindHeapChunkByAddress` is not the correct Chunk, it is much less than the `addr`.

```
  AsanChunkView FindHeapChunkByAddress(uptr addr) {  
    AsanChunk \*m1 = GetAsanChunkByAddr(addr);  
    sptr offset = 0;  
    if (!m1 || AsanChunkView(m1).AddrIsAtLeft(addr, 1, &offset)) {  
      // The address is in the chunk's left redzone, so maybe it is actually  
      // a right buffer overflow from the other chunk before.  
      // Search a bit before to see if there is another chunk.  
      AsanChunk \*m2 = nullptr;  
      for (uptr l = 1; l < GetPageSizeCached(); l++) {  
        m2 = GetAsanChunkByAddr(addr - l);  
        if (m2 == m1) continue;  // Still the same chunk.  
        break;  
      }  
      if (m2 && AsanChunkView(m2).AddrIsAtRight(addr, 1, &offset))  
        m1 = ChooseChunk(addr, m2, m1);  
    }  
    return AsanChunkView(m1);  
  }  

```

Since that I'm not familiar with the implementation of ASAN, I can only guess that the call to `MediaStream` break some shadow memory of Asan or the Heap Chunk, so Asan can not find the correct Chunk to identify a Uaf.

I also test this Uaf on Chromium Dev without ASAN and find that it uses a different `SafelyUnwrapPtrForDereference` function, maybe this one :[7].  

So this in only a problem in raw\_ptr with ASAN.

[2] <https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h;l=833>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_hookable_impl.h;l=81>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:base/memory/raw_ptr_asan_hooks.cc;l=70>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:base/memory/raw_ptr_asan_hooks.cc;l=20>  

[6] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/extensions/cxx_debugging/third_party/llvm/src/compiler-rt/lib/asan/asan_allocator.cpp;l=848>  

[7] <https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_backup_ref_impl.h;l=243>

\*\*Chrome version: \*\* 120 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 979 B)
- [asan.txt](attachments/asan.txt) (text/plain, 25.3 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 957.3 KB)
- [poc-overflow.html](attachments/poc-overflow.html) (text/plain, 2.1 KB)
- [asan-overflow.txt](attachments/asan-overflow.txt) (text/plain, 12.1 KB)
- [poc-overflow.webm](attachments/poc-overflow.webm) (video/webm, 873.4 KB)

## Timeline

### me...@gmail.com (2023-10-13)

And here is the file for overflow.

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-14)

Thanks for the report and thank you for digging into the weirdness around MiraclePtr. I'll loop in some experts to help look into what is happening there -- for now I'll triage this as though there *is* a way to bypass the MiraclePtr protections, but my guess is that for shipping configurations the protections are present (and we will later downgrade the severity by one level).

andypaicu@ could you PTAL?

Setting Severity-High as this is a browser-process UAF but it requires specific user interaction and it isn't immediately clear if this is remotely exploitable. As the PermissionElement feature is not enabled anywhere, setting Impact-None. (If this is in fact protected by MiraclePtr we would decrease the severity for Medium, per https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#TOC-MiraclePtr.)

[Monorail components: UI>Browser>Permissions>Prompts]

### me...@gmail.com (2023-10-17)

[Comment Deleted]

### me...@gmail.com (2023-10-24)

[Comment Deleted]

### me...@gmail.com (2023-10-31)

[Comment Deleted]

### me...@gmail.com (2023-11-09)

Hello, any update?

### an...@chromium.org (2023-11-09)

I've got a fix in progress: https://chromium-review.googlesource.com/c/chromium/src/+/5012814. 

I'm unsure about what to do with the MiraclePtr concern. cthomp@ has this been any progress on that part? Do you need this bug kept open after the UAF is fixed?

### gi...@appspot.gserviceaccount.com (2023-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b44d5d160d3e9b4cf7cfde332f9f3d3d9f074a79

commit b44d5d160d3e9b4cf7cfde332f9f3d3d9f074a79
Author: Andy Paicu <andypaicu@chromium.org>
Date: Thu Nov 09 18:07:25 2023

Fix UAF in EmbeddedPermissionPrompt by using a ViewTracker

A ViewTracker ensures we never risk using the view after it's free. At
worst we'll cause a null segmentation fault if we don't null check.

Also do the same in the legacy prompt bubble which also uses a raw
pointer.

Bug: 1492385
Change-Id: Iff50d68724731bbb352e0c8ec8b92880ea6df19f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5012814
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Thomas Nguyen <tungnh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1222395}

[modify] https://crrev.com/b44d5d160d3e9b4cf7cfde332f9f3d3d9f074a79/chrome/browser/ui/views/permissions/permission_prompt_bubble.h
[modify] https://crrev.com/b44d5d160d3e9b4cf7cfde332f9f3d3d9f074a79/chrome/browser/ui/views/permissions/embedded_permission_prompt.cc
[modify] https://crrev.com/b44d5d160d3e9b4cf7cfde332f9f3d3d9f074a79/chrome/browser/ui/views/permissions/embedded_permission_prompt.h
[modify] https://crrev.com/b44d5d160d3e9b4cf7cfde332f9f3d3d9f074a79/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc


### ct...@chromium.org (2023-11-09)

Thanks for the fix!

> Do you need this bug kept open after the UAF is fixed?

I think we can mark this as fixed, and treat this as potentially not protected by MiraclePtr (so keep it as Severity-High). Chatting with Security folks internally, it seems like the alternate repro shown in https://crbug.com/chromium/1492385#c1 is actually a subtly different way of triggering the crash, in a way that bypasses MiraclePtr  (or maybe just messes up ASAN's ability to track liveness). Fixing the underlying root cause (the UAF) should address both and we can mark this as fixed overall.

### an...@chromium.org (2023-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-10)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-11-30)

Hello, any updates about the reward?

### ma...@google.com (2023-12-01)

Thanks for the detailed analysis on the BRP-ASan crash (and the second testcase).

I have verified that this is protected by MiraclePtr, and why the second testcase reports 
incorrectly. In particular, in the second testcase, there are enough allocations between 
the "free" and the "use" to empty the ASan quarantine, which is why the analysis is incorrect.
This limitation is documented here:
https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md#limitations

If the second testcase is run with a larger quarantine size such as
`ASAN_OPTIONS=quarantine_size_mb=1024`, the analysis is consistent with the first
testcase, and will correctly report this issue as a protected use-after-free.

Increasing the quarantine size will significantly increase memory usage of ASan builds, so
for use-cases like fuzzing we didn't want to override this setting by default, but increasing
the quarantine size is definitely the best "first step" to understanding what's going on when
the results initially don't make sense.

### en...@chromium.org (2023-12-01)

Thanks for the additional context, Mark!

cthomp@, andypaicu@, is the Severity-High rating still appropriate in light of https://crbug.com/chromium/1492385#c15?

### am...@google.com (2023-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-07)

Congratulations, Krace! The Chrome VRP Panel has decided to award you $3,000 for this report of a highly mitigated security bug -- mitigated by BRP and user interaction + bisect bonus. We appreciate your secondary test case that allowed for some interesting analysis as communicated by markbrand@ in https://crbug.com/chromium/1492385#c15 (and was also the cause of the delay in the reward decision). Thank you for your efforts here and reporting this issue and a dual set of testcases to us! 

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1492385?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074795)*
