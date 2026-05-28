# Security: UAP in IDBFactory::DidAllowIndexedDB

| Field | Value |
|-------|-------|
| **Issue ID** | [40069646](https://issues.chromium.org/issues/40069646) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2023-08-16 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS

VERSION

chrome commit run by fuzzer:
NOTE THAT IT'S NOT A GIT COMMIT FOR BISECTION.

```
commit a7b98a1e333e69afaf7ef17f86bcf0440f5c043b (HEAD -> main, origin/main, origin/HEAD)
Author: Sana Akbani <sanaakbani@google.com>
Date:   Tue Aug 15 02:17:53 2023 +0000

    Deprecate PCA Web Contents Observer and migrate to PCA Service & History Service Observer

    Bug: b/1324053, b/1321222
    Change-Id: If3872a1aa3a98f77bf185561aa6d20e70801bd68
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4687798
    Reviewed-by: Robert Ogden <robertogden@chromium.org>
    Reviewed-by: Sophie Chang <sophiechang@chromium.org>
    Commit-Queue: Sana Akbani <sanaakbani@google.com>
    Cr-Commit-Position: refs/heads/main@{#1183475}
```
Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide any minimized poc or stably repro poc at this time. However, I have provided the ASAN log and execution log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: renderer
Crash State: see asan log

[0] The function IDBFactory::AllowIndexedDB creates an IDBFactory::DidAllowIndexedDB callback, which is then passed to the AllowStorageAccess function. Due to IdbFactory being an object managed by the Oilpan garbage collector, **an incorrect usage of weak_factory_.GetWeakPtr** instead of WrapWeakPersistent(this) is causing improper reference retention during Oilpan garbage collection. As a result, the IDBFactory object is erroneously collected during garbage collection.

```cpp
void IDBFactory::AllowIndexedDB(base::OnceCallback<void()> callback) {
  ...

  settings_client->AllowStorageAccess(
      WebContentSettingsClient::StorageType::kIndexedDB,
      WTF::BindOnce(&IDBFactory::DidAllowIndexedDB, //------->[0]
                    weak_factory_.GetWeakPtr()));
}

template <typename T>
class GlobalIndexedDBImpl final
    : public GarbageCollected<GlobalIndexedDBImpl<T>>,
      public Supplement<T> {
    ...
    IDBFactory* IdbFactory(ExecutionContext* context) {
        if (!idb_factory_)
            idb_factory_ = MakeGarbageCollected<IDBFactory>(context);
        return idb_factory_;
    }
```


[1] The function ContentSettingsAgentImpl::AllowStorageAccess wraps the callback as original_cb and uses a new callback new_cb to invoke it. 
The GetContentSettingsManager().AllowStorageAccess is a Mojo call, eventually leads to the invocation of the IDBFactory::DidAllowIndexedDB function. This is also in line with the scenario presented in the ASan log.

```cpp
  // Controls whether access to the given StorageType is allowed for this frame.
  // Runs asynchronously.
  virtual void AllowStorageAccess(StorageType storage_type,
                                  base::OnceCallback<void(bool)> callback) {
    std::move(callback).Run(true);
  }

void ContentSettingsAgentImpl::AllowStorageAccess(
    StorageType storage_type,
    base::OnceCallback<void(bool)> callback) {
  ...

  // Passing the `cache_storage_permissions_` ref to the callback is safe here
  // as the mojo::Remote is owned by `this` and won't invoke the callback if
  // `this` (and in turn `cache_storage_permissions_`) is destroyed.
  base::OnceCallback<void(bool)> new_cb = base::BindOnce(
      [](base::OnceCallback<void(bool)> original_cb, StoragePermissionsKey key,
         base::flat_map<StoragePermissionsKey, bool>& cache_map, bool result) {
        cache_map[key] = result;
        std::move(original_cb).Run(result);
      },
      std::move(callback), key, std::ref(cached_storage_permissions_));

  GetContentSettingsManager().AllowStorageAccess( //------>[1]
      routing_id(), ConvertToMojoStorageType(storage_type),
      frame->GetSecurityOrigin(), frame->GetDocument().SiteForCookies(),
      frame->GetDocument().TopFrameOrigin(), std::move(new_cb));
}

mojom::ContentSettingsManager&
ContentSettingsAgentImpl::GetContentSettingsManager() {
  if (!content_settings_manager_)
    BindContentSettingsManager(&content_settings_manager_);
  return *content_settings_manager_;
}
...

mojo::Remote<mojom::ContentSettingsManager> content_settings_manager_;
...
AllowStorageAccess(
    int32 render_frame_id,
    StorageType storage_type,
    url.mojom.Origin origin,
    network.mojom.SiteForCookies site_for_cookies,
    url.mojom.Origin top_frame_origin) => (bool allowed);
...
```

[2] During the execution of IDBFactory::DidAllowIndexedDB, if the thread that owns the Oilpan objects is terminated, the termination garbage collection destroys the objects. This leads to the release of the IDBFactory, triggering a use-after-free write at [2].

```
void IDBFactory::DidAllowIndexedDB(bool allow_access) {
  DCHECK(!allowed_.has_value());
  allowed_ = allow_access; //----->[2]

  for (auto& callback : callbacks_waiting_on_permission_decision_) {
    std::move(callback).Run();
  }
  callbacks_waiting_on_permission_decision_.clear();
}
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/indexeddb/idb_factory.cc;l=477;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/content_settings/renderer/content_settings_agent_impl.cc;l=257;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/indexeddb/idb_factory.cc;l=483;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;


## Bisects
The issue is introduced by the code change at： https://source.chromium.org/chromium/chromium/src/+/348f421e8d31bf4b3b13e93d1af508cdccdf7817

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 7.3 KB)
- [asan-in-14988c.log](attachments/asan-in-14988c.log) (text/plain, 8.3 KB)
- [execution.log](attachments/execution.log) (text/plain, 61.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 7.3 KB)
- [execution.log](attachments/execution.log) (text/plain, 61.5 KB)
- [asan-in-14988c.log](attachments/asan-in-14988c.log) (text/plain, 8.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 8.3 KB)

## Timeline

### ki...@gmail.com (2023-08-16)

VULNERABILITY DETAILS

VERSION

chrome commit run by fuzzer:
NOTE THAT IT'S NOT A GIT COMMIT FOR BISECTION.

```
commit a7b98a1e333e69afaf7ef17f86bcf0440f5c043b (HEAD -> main, origin/main, origin/HEAD)
Author: Sana Akbani <sanaakbani@google.com>
Date:   Tue Aug 15 02:17:53 2023 +0000

    Deprecate PCA Web Contents Observer and migrate to PCA Service & History Service Observer

    Bug: b/1324053, b/1321222
    Change-Id: If3872a1aa3a98f77bf185561aa6d20e70801bd68
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4687798
    Reviewed-by: Robert Ogden <robertogden@chromium.org>
    Reviewed-by: Sophie Chang <sophiechang@chromium.org>
    Commit-Queue: Sana Akbani <sanaakbani@google.com>
    Cr-Commit-Position: refs/heads/main@{#1183475}
```
Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide any minimized poc or stably repro poc at this time. However, I have provided the ASAN log and execution log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: renderer
Crash State: see asan log

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-08-16)

Hello, thanks for the report. We really need a minimized test case/PoC to be able to debug this meaningfully. The execution and ASAN logs don't seem to have enough specific information.
christinesm@chromium.org, can you take a quick look to see if there is anything you can glean from them? Thanks! 

[Monorail components: Blink>Storage>IndexedDB]

### ki...@gmail.com (2023-08-16)

Hi, we've analyzed the root cause today based on the asan log and successfully got the RCA, but also found that the vulnerability was reverted in ff25d287866b8c91630fbd14d9a85b3bd4c8e1e4 earlier today. Please close this report.

### [Deleted User] (2023-08-16)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2023-08-16)

OK, thanks for following up.

### ki...@gmail.com (2023-08-24)

[0] The function IDBFactory::AllowIndexedDB creates an IDBFactory::DidAllowIndexedDB callback, which is then passed to the AllowStorageAccess function. Due to IdbFactory being an object managed by the Oilpan garbage collector, **an incorrect usage of weak_factory_.GetWeakPtr** instead of WrapWeakPersistent(this) is causing improper reference retention during Oilpan garbage collection. As a result, the IDBFactory object is erroneously collected during garbage collection.

```cpp
void IDBFactory::AllowIndexedDB(base::OnceCallback<void()> callback) {
  ...

  settings_client->AllowStorageAccess(
      WebContentSettingsClient::StorageType::kIndexedDB,
      WTF::BindOnce(&IDBFactory::DidAllowIndexedDB, //------->[0]
                    weak_factory_.GetWeakPtr()));
}

template <typename T>
class GlobalIndexedDBImpl final
    : public GarbageCollected<GlobalIndexedDBImpl<T>>,
      public Supplement<T> {
    ...
    IDBFactory* IdbFactory(ExecutionContext* context) {
        if (!idb_factory_)
            idb_factory_ = MakeGarbageCollected<IDBFactory>(context);
        return idb_factory_;
    }
```


[1] The function ContentSettingsAgentImpl::AllowStorageAccess wraps the callback as original_cb and uses a new callback new_cb to invoke it. 
The GetContentSettingsManager().AllowStorageAccess is a Mojo call, eventually leads to the invocation of the IDBFactory::DidAllowIndexedDB function. This is also in line with the scenario presented in the ASan log.

```cpp
  // Controls whether access to the given StorageType is allowed for this frame.
  // Runs asynchronously.
  virtual void AllowStorageAccess(StorageType storage_type,
                                  base::OnceCallback<void(bool)> callback) {
    std::move(callback).Run(true);
  }

void ContentSettingsAgentImpl::AllowStorageAccess(
    StorageType storage_type,
    base::OnceCallback<void(bool)> callback) {
  ...

  // Passing the `cache_storage_permissions_` ref to the callback is safe here
  // as the mojo::Remote is owned by `this` and won't invoke the callback if
  // `this` (and in turn `cache_storage_permissions_`) is destroyed.
  base::OnceCallback<void(bool)> new_cb = base::BindOnce(
      [](base::OnceCallback<void(bool)> original_cb, StoragePermissionsKey key,
         base::flat_map<StoragePermissionsKey, bool>& cache_map, bool result) {
        cache_map[key] = result;
        std::move(original_cb).Run(result);
      },
      std::move(callback), key, std::ref(cached_storage_permissions_));

  GetContentSettingsManager().AllowStorageAccess( //------>[1]
      routing_id(), ConvertToMojoStorageType(storage_type),
      frame->GetSecurityOrigin(), frame->GetDocument().SiteForCookies(),
      frame->GetDocument().TopFrameOrigin(), std::move(new_cb));
}

mojom::ContentSettingsManager&
ContentSettingsAgentImpl::GetContentSettingsManager() {
  if (!content_settings_manager_)
    BindContentSettingsManager(&content_settings_manager_);
  return *content_settings_manager_;
}
...

mojo::Remote<mojom::ContentSettingsManager> content_settings_manager_;
...
AllowStorageAccess(
    int32 render_frame_id,
    StorageType storage_type,
    url.mojom.Origin origin,
    network.mojom.SiteForCookies site_for_cookies,
    url.mojom.Origin top_frame_origin) => (bool allowed);
...
```

[2] During the execution of IDBFactory::DidAllowIndexedDB, if the thread that owns the Oilpan objects is terminated, the termination garbage collection destroys the objects. This leads to the release of the IDBFactory, triggering a use-after-free write at [2].

```
void IDBFactory::DidAllowIndexedDB(bool allow_access) {
  DCHECK(!allowed_.has_value());
  allowed_ = allow_access; //----->[2]

  for (auto& callback : callbacks_waiting_on_permission_decision_) {
    std::move(callback).Run();
  }
  callbacks_waiting_on_permission_decision_.clear();
}
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/indexeddb/idb_factory.cc;l=477;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/content_settings/renderer/content_settings_agent_impl.cc;l=257;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/indexeddb/idb_factory.cc;l=483;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

### ki...@gmail.com (2023-08-24)

## Bisects
The issue is introduced by the code change at： https://source.chromium.org/chromium/chromium/src/+/348f421e8d31bf4b3b13e93d1af508cdccdf7817

### ki...@gmail.com (2023-08-24)

Add new asan log

### ki...@gmail.com (2023-08-24)

I am not sure whether the above analysis is completely correct, but I think the use of weak_ptr here should be the key to the problem.
Please further analyze and fix this vulnerability according to the asan log.

### es...@chromium.org (2023-08-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c0e062a84d3afabe9746313587a60f708ff8bd84

commit c0e062a84d3afabe9746313587a60f708ff8bd84
Author: Evan Stade <estade@chromium.org>
Date: Sat Aug 26 00:31:12 2023

IndexedDB: cancel IDBFactory callbacks on oilpan GC.

The WeakPtrFactory is used to invalidate mojo callbacks when the
execution context is destroyed (not just when IDBFactory is destroyed).
It must also invalidate pointers when IDBFactory is being finalized.

Bug: 1473193
Change-Id: I99769f1465bebeff99caba15b3278d0378636508
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4810922
Commit-Queue: Evan Stade <estade@chromium.org>
Reviewed-by: Nathan Memmott <memmott@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1188615}

[modify] https://crrev.com/c0e062a84d3afabe9746313587a60f708ff8bd84/third_party/blink/renderer/modules/indexeddb/idb_factory.cc
[modify] https://crrev.com/c0e062a84d3afabe9746313587a60f708ff8bd84/third_party/blink/renderer/modules/indexeddb/idb_factory.h


### hc...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-29)

Since this is a non-interactive uaf write issue for the render process, Maybe it should be security-high?

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-30)

I have reorganized the previous comment for easier Chrome VRP reward assessment.


VULNERABILITY DETAILS
## Bisects
The issue is introduced by the code change at： 
1. https://chromium-review.googlesource.com/c/chromium/src/+/4781019
```
Reland "IDBFactory clean ups."
This relands commit 934b1f58d579211e74884e544ecaed8f7fe61f29.
...
```

2. https://chromium-review.googlesource.com/c/chromium/src/+/4757570
```
IDBFactory clean ups.

Some minor changes to improve clarity. These changes should be
functionally equivalent.

* Rename factory_ to remote_
* Make IDBFactory an ExecutionContextLifecycleObserver so the context
  is always accessed in a consistent way instead of a hodge podge
* remove `task_runner_` and just retrieve from the ExecutionContext
  every time

Bug: 717812
Change-Id: I97ca77fe45b698814b77e33fd4f3c1f7aad3ba0a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4757570
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1183201}
```

## Root Cause
[0] The function IDBFactory::AllowIndexedDB creates an IDBFactory::DidAllowIndexedDB callback, which is then passed to the AllowStorageAccess function. Due to IdbFactory being an object managed by the Oilpan garbage collector, **an incorrect usage of weak_factory_.GetWeakPtr** instead of WrapWeakPersistent(this) is causing improper reference retention during Oilpan garbage collection. As a result, the IDBFactory object is erroneously collected during garbage collection.

```cpp
void IDBFactory::AllowIndexedDB(base::OnceCallback<void()> callback) {
  ...

  settings_client->AllowStorageAccess(
      WebContentSettingsClient::StorageType::kIndexedDB,
      WTF::BindOnce(&IDBFactory::DidAllowIndexedDB, //------->[0]
                    weak_factory_.GetWeakPtr()));
}

template <typename T>
class GlobalIndexedDBImpl final
    : public GarbageCollected<GlobalIndexedDBImpl<T>>,
      public Supplement<T> {
    ...
    IDBFactory* IdbFactory(ExecutionContext* context) {
        if (!idb_factory_)
            idb_factory_ = MakeGarbageCollected<IDBFactory>(context);
        return idb_factory_;
    }
```


[1] The function ContentSettingsAgentImpl::AllowStorageAccess wraps the callback as original_cb and uses a new callback new_cb to invoke it. 
The GetContentSettingsManager().AllowStorageAccess is a Mojo call, eventually leads to the invocation of the IDBFactory::DidAllowIndexedDB function. This is also in line with the scenario presented in the ASan log.

```cpp
  // Controls whether access to the given StorageType is allowed for this frame.
  // Runs asynchronously.
  virtual void AllowStorageAccess(StorageType storage_type,
                                  base::OnceCallback<void(bool)> callback) {
    std::move(callback).Run(true);
  }

void ContentSettingsAgentImpl::AllowStorageAccess(
    StorageType storage_type,
    base::OnceCallback<void(bool)> callback) {
  ...

  // Passing the `cache_storage_permissions_` ref to the callback is safe here
  // as the mojo::Remote is owned by `this` and won't invoke the callback if
  // `this` (and in turn `cache_storage_permissions_`) is destroyed.
  base::OnceCallback<void(bool)> new_cb = base::BindOnce(
      [](base::OnceCallback<void(bool)> original_cb, StoragePermissionsKey key,
         base::flat_map<StoragePermissionsKey, bool>& cache_map, bool result) {
        cache_map[key] = result;
        std::move(original_cb).Run(result);
      },
      std::move(callback), key, std::ref(cached_storage_permissions_));

  GetContentSettingsManager().AllowStorageAccess( //------>[1]
      routing_id(), ConvertToMojoStorageType(storage_type),
      frame->GetSecurityOrigin(), frame->GetDocument().SiteForCookies(),
      frame->GetDocument().TopFrameOrigin(), std::move(new_cb));
}

mojom::ContentSettingsManager&
ContentSettingsAgentImpl::GetContentSettingsManager() {
  if (!content_settings_manager_)
    BindContentSettingsManager(&content_settings_manager_);
  return *content_settings_manager_;
}
...

mojo::Remote<mojom::ContentSettingsManager> content_settings_manager_;
...
AllowStorageAccess(
    int32 render_frame_id,
    StorageType storage_type,
    url.mojom.Origin origin,
    network.mojom.SiteForCookies site_for_cookies,
    url.mojom.Origin top_frame_origin) => (bool allowed);
...
```

[2] During the execution of IDBFactory::DidAllowIndexedDB, if the thread that owns the Oilpan objects is terminated, the termination garbage collection destroys the objects. This leads to the release of the IDBFactory, triggering a use-after-free write at [2].

```
void IDBFactory::DidAllowIndexedDB(bool allow_access) {
  DCHECK(!allowed_.has_value());
  allowed_ = allow_access; //----->[2]

  for (auto& callback : callbacks_waiting_on_permission_decision_) {
    std::move(callback).Run();
  }
  callbacks_waiting_on_permission_decision_.clear();
}
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/indexeddb/idb_factory.cc;l=477;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/content_settings/renderer/content_settings_agent_impl.cc;l=257;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/indexeddb/idb_factory.cc;l=483;drc=bb2d66f5c212d3b5883fac31d6ce20f1164d693f;

## Other
This will cause a non-interactive UAF write vulnerability in the render process, which I think may be Security_Severity-High.
Since it does not affect the release, it should be Security_Impact-None.

REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide any minimized poc or stably repro poc at this time. However, I have provided the ASAN log and execution log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: renderer
Crash State: see asan log


### es...@chromium.org (2023-09-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-06)

Without a POC or reproduction, it's not clear that this is readily exploitable, so I have conservatively raised this to high severity based that a UAF in the renderer process is achievable and premise this was fuzzer discovered. 

While we greatly appreciate prompt reporting of vulnerabilities as well as the additional and more comprehensive data in comment c#18, when discovering bugs in ongoing work in tot/ head, it is most helpful to provide a more thorough and comprehensive report as part of the original report so that we can best triage and work toward resolution. While providing a more comprehensive summary for VRP, the goal for VRP is to move bugs faster from discovery -> reporting -> fix and providing details ahead of the fix is most and genuinely appreciated and helpful. 

### [Deleted User] (2023-09-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-07)

Not requesting merge to dev (M118) because latest trunk commit (1188615) appears to be prior to dev branch point (1192594). If this is incorrect, please replace the Merge-NA-118 label with Merge-Request-118. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M118. Please go ahead and merge the CL to branch 5993 (refs/branch-heads/5993) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-11)

[Description Changed]

### es...@chromium.org (2023-09-11)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-09-12)

Please merge your change to M118 by 2:00 PM PT today, Tuesday, Sept 12th so we can take it in for tomorrow's M118 beta promotion. Thank you.

Branch Details: https://chromiumdash.appspot.com/branches

### es...@chromium.org (2023-09-12)

this doesn't need to be merged to m118 or any other branch AFAIA: https://chromiumdash.appspot.com/commit/c0e062a84d3afabe9746313587a60f708ff8bd84

### wf...@chromium.org (2023-09-13)

[Empty comment from Monorail migration]

### ts...@google.com (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations Kiprey! The VRP Panel has decided to award you $7,000 for this report +$1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### ts...@google.com (2023-09-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-09-15)

Please merge your change to M118 ASAP.
Branch Details: https://chromiumdash.appspot.com/branches

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-09-19)

Please merge your change to M118 by 2:00 PM PT today so it can be included in tomorrow's beta release. Beta RC cut today @2:30 PM PT.

Branch Details: https://chromiumdash.appspot.com/branches.

If it is already merged, please remove "Merge-Approved-118" label. 



### es...@chromium.org (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1473193?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1475525]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069646)*
