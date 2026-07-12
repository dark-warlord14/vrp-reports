# UAF in Metal LibraryCache

| Field | Value |
|-------|-------|
| **Issue ID** | [497724490](https://issues.chromium.org/issues/497724490) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | he...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-30 |
| **Bounty** | $16,000.00 |

## Description

### Summary

ANGLE's Metal shader-library cache returns a `LibraryCacheEntry &` from [`LibraryCache::getCacheEntry`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_library_cache.mm;l=88) while holding `mCacheLock`, but [`LibraryCache::getOrCompileShaderLibrary`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_library_cache.mm;l=55) drops that cache lock before taking `entry.lock`. Once the cache was converted to an evicting `HashingMRUCache`, concurrent shader-link tasks could call `TrimCache` and destroy the referenced entry before the caller locks it, leading to the UAF in GPU process during Metal library compilation.

### Details

[`CreateMslShaderLib`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/ProgramExecutableMtl.mm;l=349) compiles translated MSL through the display-global Metal library cache. [`LibraryCache::getOrCompileShaderLibrary`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_library_cache.mm;l=55) obtains a reference to an entry and only then locks that entry's mutex:

```
ASSERT(source != nullptr);
LibraryCache::LibraryCacheEntry &entry =
    getCacheEntry(LibraryKey(source, macros, disableFastMath, usesInvariance));

// Lock this cache entry while compiling the shader. This causes other threads calling this
// function to wait and not duplicate the compilation.
std::lock_guard<std::mutex> entryLockGuard(entry.lock);
if (entry.library)
{
    return entry.library;
}

entry.library = CreateShaderLibrary(metalDevice, *source, macros, disableFastMath,
                                    usesInvariance, errorOut);
return entry.library;

```

[`LibraryCache::getCacheEntry`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_library_cache.mm;l=88) protects lookup and insertion with `mCacheLock`, but it returns a reference to an object stored inside the MRU container and releases the cache lock before the caller touches that reference again. The same function also trims the MRU before inserting:

```
    // Lock while searching or adding new items to the cache.
    std::lock_guard<std::mutex> cacheLockGuard(mCacheLock);

    auto iter = mCache.Get(key);
    if (iter != mCache.end())
    {
        return iter->second;
    }

    angle::TrimCache(kMaxCachedLibraries, kGCLimit, "metal library", &mCache);

    iter = mCache.Put(std::move(key), LibraryCacheEntry());
    return iter->second;

```

That means the lifetime guarantee on `entry` ends when `mCacheLock` is released. A second worker can immediately re-enter `getCacheEntry`, hit [`angle::TrimCache`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_library_cache.mm;l=99), and erase the least-recently-used node that the first thread still references. The destructor for [`LibraryCacheEntry`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/mtl_library_cache.mm;l=135) does lock `entry.lock`, but that only serializes destruction with in-flight compilation if the caller already has a valid pointer to the same object. Therefore it does not prevent a caller from dereferencing after the container node itself has been freed, and thus cause the UAF.

### Bisection

This issue is introduced by the commit <https://chromium-review.googlesource.com/c/angle/angle/+/4614362>, which introduced the MRUCache, making the attacker available to free TrimCache and cause UAF.

### Reproduction

Host the poc.html using `python3 -m http.server 8080`

Run chromium (e.g., <https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1606755.zip>) with:

```
./Chromium.app/Contents/MacOS/Chromium http://127.0.0.1:8080/poc.html http://127.0.0.1:8080/poc.html http://127.0.0.1:8080/poc.html http://127.0.0.1:8080/poc.html

```

You would observe the UAF shown in `asan.txt`.

### Suggested Fix

The minimal fix is to store cache entries with ref-counted pointer.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 60.6 KB)
- [poc.html](attachments/poc.html) (text/html, 3.0 KB)
- [reproduction-497724490.mp4](attachments/reproduction-497724490.mp4) (video/mp4, 39.0 MB)

## Timeline

### he...@gmail.com (2026-03-30)

Attach the reproduction video

### ja...@google.com (2026-03-31)

[security triage]

Thanks for the asan stack trace and poc and video. I don't have a mac system but triaging as reproducible. Adding GPU team members to take a look.

### ja...@google.com (2026-04-01)

Setting found in to extended stable.

### ch...@google.com (2026-04-01)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-01)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-02)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7722080>

Metal: Store LibraryCacheEntry in a shared\_ptr

---


Expand for full commit details
```
     
    This ensures that if an entry is removed from the cache while it is 
    compiling, it is not deleted until it is fully unreferenced. 
     
    If there were > kMaxCachedLibraries simultaneous compile requests, it 
    was possible that the cache gets trimmed while threads are compiling and 
    we can end up writing to removed cache entries. 
     
    Bug: chromium:497724490 
    Change-Id: Iba4281d5d12c6882de51fc1bf88d60157ffc7fb6 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7722080 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/mtl_library_cache.h`
- M `src/libANGLE/renderer/metal/mtl_library_cache.mm`

---

Hash: [3bb4e2424dc4424edc30cddb384817bcab078438](https://chromiumdash.appspot.com/commit/3bb4e2424dc4424edc30cddb384817bcab078438)  

Date: Wed Apr 1 19:54:06 2026


---

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7727503>

Roll ANGLE from a10f04f18a35 to 3bb4e2424dc4 (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/a10f04f18a35..3bb4e2424dc4 
     
    2026-04-02 geofflang@chromium.org Metal: Store LibraryCacheEntry in a shared_ptr 
    2026-04-02 ynovikov@chromium.org Skip DrawThenInvalidateThenVerifyDepthStencil on iOS 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,syoussefi@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:497724490 
    Tbr: syoussefi@google.com 
    Change-Id: I3e1abe6e9ffb96aa44312bb33527413625d52a3a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7727503 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1609437}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [fde92d9984ae608e11b25cee3b2717b63d7ceb06](https://chromiumdash.appspot.com/commit/fde92d9984ae608e11b25cee3b2717b63d7ceb06)  

Date: Thu Apr 2 19:50:24 2026


---

### ch...@google.com (2026-04-03)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1609437) appears to be after stable branch point (1582197).

Merge review required: a commit with DEPS changes was detected.

Requesting merge to beta (M147) because latest trunk commit (1609437) appears to be after beta branch point (1596535).

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ge...@chromium.org (2026-04-07)

1. <https://chromium-review.googlesource.com/7722080>
2. Yes
3. No
4. No
5. No

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $16000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### he...@gmail.com (2026-04-23)

Thank you very much. If there would be CVE assign to this, I would like to change my credit to "Syn4pse (@ret2happy)".

Thanks a lot!

### ch...@google.com (2026-07-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497724490)*
