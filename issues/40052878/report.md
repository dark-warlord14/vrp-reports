# Security: Possible for apps to access http/https sites outside of a webview context via blob URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40052878](https://issues.chromium.org/issues/40052878) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage, Blink>Storage>FileAPI, Internals>Sandbox>SiteIsolation, Platform>Apps>BrowserTag, Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2020-07-17 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

An app can embed another site within one of its pages using the webview tag. The embedded site then uses distinct storage for things like cookies and local storage. That means the embedded site doesn't have access to the data stored in the associated Chrome profile.

However, when a blob is created and a URL for that blob is generated (via URL.createObjectURL), the URL is associated with the origin of the embedded site and can be loaded within the Chrome profile.

Using that fact, an app can load an arbitrary http/https site within a webview, create a blob, generate a URL for that blob and then load the URL within the associated profile. As blobs can represent HTML data, this allows an app to run code within a http/https site in the associated profile (outside of the webview).

**VERSION**  

Chrome Version: Tested on 84.0.4147.89 (stable) and 86.0.4205.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached app.
2. Once installed, the app will open page.html in a new app window.
3. page.html contains a webview that loads <https://www.google.com>. Once the embedded site has finished loading, the app calls the executeScript method to run the following code within the webview:

let blob = new Blob(["<script>console.log('Code run via webview app')</script>"], {type: "text/html"});  

let url = URL.createObjectURL(blob);  

window.open(url);

4. A "newwindow" listener added to the webview then creates a new tab in response to the window.open call:

chrome.browser.openTab({url: e.targetUrl});

This results in the blob being loaded and the code it contains running within the context of the associated origin (<https://www.google.com>) within the current profile.

Aside from http/https URLs, this also works with any other web safe scheme a webview can load (e.g. chrome-search:).

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 38 B)
- [manifest.json](attachments/manifest.json) (text/plain, 272 B)
- [page.html](attachments/page.html) (text/plain, 123 B)
- [page.js](attachments/page.js) (text/plain, 626 B)

## Timeline

### me...@chromium.org (2020-07-21)

When I tried reproducing this I got the following errors:
```
The source list for Content Security Policy directive 'script-src' contains an invalid source: ''wasm-eval''. It will be ignored.
```
And
```
<webview>: A new window was blocked.
```

And when I tried accessing some stuff I put in local storage on google.com, it wasn't accessible from the webview. So I don't think I got the POC working.

CCing caseq@ and rdevlin.cronin@ in case they have any ideas.

[Monorail components: Platform>Extensions]

### de...@gmail.com (2020-07-21)

In this case, the errors are expected. I'm not sure of the precise reason for the first, but the second will be triggered whenever a webview tries to open a new window.

It's true that you can't access anything from within the webview. The issue is that the blob that's loaded in the associated Chrome profile can access the profile data. You can verify that by opening the devtools within the blob: tab that's opened and test reading/writing local storage.

### aj...@google.com (2020-07-21)

I've confirmed the repro but I'm not a webview expert. Could someone on the webview team take a look?

Setting High severity as this might be a site isolation bypass but happy to be corrected by someone who understands the security model of this area better than I do.

[Monorail components: Platform>Apps>BrowserTag]

### [Deleted User] (2020-07-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-07-23)

Assigning an owner. Please feel free to assign to someone else if they are working on fixing this.

### mc...@chromium.org (2020-07-23)

Lowering severity as this requires a chrome app to be installed (see the reasoning in https://crbug.com/683523#c10).

### wj...@chromium.org (2020-07-24)

Removing people who no longer work on WebView, and adding more security folks.

Question for the security team: what is the potential here for misuse?

### wj...@chromium.org (2020-07-24)

[Empty comment from Monorail migration]

### cr...@chromium.org (2020-07-25)

https://crbug.com/chromium/1106890#c8: This is a legitimate security bug that allows an app to access a victim site's data in the default StoragePartition, simply by requesting the ability to load the victim site in a GuestView.  The premise of Chrome apps is that their GuestViews live in separate StoragePartitions from normal tabs, so the app won't have access to the user's usual credentials and data from their Chrome tabs.  In that sense, this bug is a bit of a Site Isolation violation, with the caveat from https://crbug.com/chromium/1106890#c7 that it requires installing an app to do so.  I agree with Medium severity.

The root cause here is that blob URLs appear to be shared across StoragePartitions, IIUC.  A blob URL created in a GuestView should not be accessible from a normal tab, and this has security consequences because the GuestView-created blob page runs in the victim's origin once loaded in a normal tab.  However, I'm a bit surprised because I see StorageParitionImpl::GetBlobRegistry(), which would imply on the surface that it should be specific to a StoragePartition.  It must go wrong somewhere along the way?

mek@: Would you be able to take a look at why blob URLs created in one StoragePartition are able to load in a different StoragePartition?  Thanks!

I'm also curious if the same bug is true for filesystem URLs?  Those have similar properties, and I wouldn't be surprised.

[Monorail components: Blink>Storage Blink>Storage>FileAPI Internals>Sandbox>SiteIsolation]

### me...@chromium.org (2020-07-25)

Currently blobs themselves are per-profile, I don't think for any particular reason (i.e. ChromeBlobStorageContext::GetFor(BrowserContext*)). And blob URLs are also managed by the same BlobStorageContext, so they also end up being per profile. This was thought to be okay, since URLs are unguessable anyway, so it doesn't really matter how they are resolvable (they additionally can only be resolved same-origin). But yeah, since webview lets you execute code as a different origin, but same profile that breaks that assumption.

We should probably make at least blob URLs per storage partition. It has also been suggested to make them scoped to an agent cluster (https://github.com/w3c/FileAPI/issues/153) which would be even better of course. Although that one also has a chance of being web-incompatible, so I guess for fixing this bug we'll have to go for per storage partition at first. Probably easiest by decoupling blob URLs from BlobStorageContext entirely.

### me...@chromium.org (2020-07-28)

Some tricky bits when trying to fix this: not all places we resolve blob URLs have easy access to a suitable StoragePartition. For example content::DownloadManagerImpl needs to be able to resolve blob URLs but is only associated with a BrowserContext. Maybe just using the default storage partition is good enough in that case.

Trickier is content::NavigationRequest::CreateBrowserInitiated. There I'm really not sure what the correct storage partition would be to use, and I'm not even sure if there is a single storage partition that is correct there. I.e. we have <webview> browser tests that explicitly verify that the webview can resolve blob URLs that were created outside the webview (https://crbug.com/chromium/652077). Not sure if outside blob URLs should also be able to resolve as sub-resources in <webview>, but it certainly isn't as simple as having separate blob URL maps per storage partition.

### cr...@chromium.org (2020-07-28)

Thanks for looking into this!  Wow, I'd forgotten about https://crbug.com/chromium/652077, where we had to let apps create blob URLs to load within guests.  I wonder if there's a way to support that case within the app's origin without more generally leaking blobs between GuestViews and other StoragePartitions.  (Not sure about the other cases you mention without looking closer, but hopefully we can find good answers there without letting blobs from guests escape into normal tabs.)

### me...@chromium.org (2020-07-29)

For the very narrow use case of https://crbug.com/chromium/652077 it seems like we might be able to do something like lookup blob URLs in the current storage partition, and additionally look it up in the storage partition with the same partition domain and empty partition name (i.e. the storage partition for the app itself). Or just not bother and break that use case since chrome apps are on the chopping block anyway...

Actually doing such a multi-step lookup would be a lot simpler after some other refactoring in how blob URLs work. But that wouldn't be the kind of change we would want to backport. Although to be fair, any solution here is going to be touching quite a bit of code. Is this the kind of security bug where we'd be happy to just roll out the fix with the normal release process?

### cr...@chromium.org (2020-07-30)

https://crbug.com/chromium/1106890#c14: Thanks-- I tend to agree, though I lean towards adding the special case for Chrome Apps rather than breaking them.

I'm somewhat inclined to aim for a good fix here even if it means we can't merge it.  The requirement to install an app that abuses it is a mitigating factor, and any apps that are discovered abusing it could be forcibly removed from the CWS.  I'd like to get adetaylor@'s confirmation on that, though.

adetaylor@: Is it ok if the fix for this isn't mergeable, given the implications in https://crbug.com/chromium/1106890#c10?

### ad...@chromium.org (2020-07-30)

Absolutely. If the fix is complex it's fine for this to be rolled out in the normal organic release process.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/889eb719836eace8c7b792eec89ce281d8f11691

commit 889eb719836eace8c7b792eec89ce281d8f11691
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Thu Aug 06 23:15:01 2020

[FileAPI] Refactor how BlobURLLoaderFactory works.

Rather than resolving a mojo Blob to a BlobDataHandle, just forward the
request to the Blob and let the blob create the URL Loader. This way we
decouple BlobURLLoaderFactory from any blob internals, paving the way
for further separating out the blob URL registry from the rest of the
blob system, making it easier to change where parts of the blob system
live (for example moving Blob URLs to be per storage partition, or in
the future perhaps per agent cluster).

This does increase binary size significantly because the added mojom
method results in java bindings being generated for a lot of interfaces
and structs that were previously not generated. In the future this
increase can be eliminated by making it possible to tag methods in
mojom files with what languages they should create bindings for, or by
rewriting BlobURLLoader itself to operate on a mojo Blob, rather than
forward the entire URLRequest to the mojo blob (https://crbug.com/1111835).

Bug: 1106890
Binary-Size: Size increase is unavoidable (see above).
Change-Id: I4fa3c6a5ddf6f8be5ce299e9d1fd95eaef75ec5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2330311
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#795695}

[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/content/browser/blob_storage/chrome_blob_storage_context.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/content/renderer/service_worker/service_worker_subresource_loader_unittest.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_impl.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_impl.h
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_url_loader.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_url_loader.h
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_url_loader_factory.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_url_loader_factory.h
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/blob/blob_url_store_impl.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/test/fake_blob.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/storage/browser/test/fake_blob.h
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/third_party/blink/public/mojom/blob/blob.mojom
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/third_party/blink/renderer/platform/blob/testing/fake_blob.cc
[modify] https://crrev.com/889eb719836eace8c7b792eec89ce281d8f11691/third_party/blink/renderer/platform/blob/testing/fake_blob.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98f465d27454f40690199ed1c32ab0ce2f8f3230

commit 98f465d27454f40690199ed1c32ab0ce2f8f3230
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Fri Aug 07 01:20:50 2020

[FileAPI] Split BlobUrlRegistry of from BlobStorageRegistry.

In preparation for making BlobUrlRegistry per storage partition, this
cleans up the code a bit by moving all the blob URL logic to a separate
class. This CL itself should not have any behavior changes, it is purely
moving code around.

Also fixes some naming inconsistencies (URL vs Url among others).

Bug: 1106890
Change-Id: I0e7f9f8597d280ee2f69286c5a35cbb3997c9d9f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2330314
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#795748}

[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/content/browser/blob_storage/blob_registry_wrapper.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/content/browser/blob_storage/blob_url_unittest.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/content/browser/blob_storage/chrome_blob_storage_context.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/content/browser/blob_storage/chrome_blob_storage_context.h
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/BUILD.gn
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_registry_impl.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_registry_impl.h
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_registry_impl_unittest.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_storage_context.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_storage_context.h
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_storage_context_unittest.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_storage_registry.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_storage_registry.h
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_storage_registry_unittest.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_loader_factory.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_loader_factory.h
[add] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_registry.cc
[add] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_registry.h
[add] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_registry_unittest.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_store_impl.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_store_impl.h
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/blob_url_store_impl_unittest.cc
[modify] https://crrev.com/98f465d27454f40690199ed1c32ab0ce2f8f3230/storage/browser/blob/view_blob_internals_job.cc


### [Deleted User] (2020-08-13)

mek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-28)

mek: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8ffda44d4be8df2ea01ed48366527f97834e2a13

commit 8ffda44d4be8df2ea01ed48366527f97834e2a13
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Thu Sep 03 18:29:47 2020

[FileAPI] Change BlobUrlRegistry to be per storage partition.

Different storage partitions should not be able to resolve blob URLs
created in other partitions. To ensure this, give each partition their
own blob url registry.

There is one exception though, a <webview> inside a chrome app should
be able to resolve blob URLs that were created by the chrome app. To
enable this, we add the concept of a "fallback url registry" to
BlobUrlRegistry, and pass the BlobUrlRegistry of the app in as fallback
when creating the storage partition for a <webview>.

Bug: 1106890
Change-Id: I809f24a2c0b4d8d21e53d46bb6d3e2027b21281b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2324110
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Aaron Colwell <acolwell@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#804321}

[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/chrome/browser/extensions/api/identity/web_auth_flow.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/chrome/test/data/extensions/platform_apps/web_view/shim/main.js
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/blob_storage/blob_registry_wrapper.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/blob_storage/blob_registry_wrapper.h
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/blob_storage/chrome_blob_storage_context.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/blob_storage/chrome_blob_storage_context.h
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/frame_host/ipc_utils.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/frame_host/navigation_request.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/storage_partition_impl.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/storage_partition_impl.h
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/storage_partition_impl_map.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/worker_host/dedicated_worker_host.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/browser/worker_host/shared_worker_connector_impl.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/public/browser/storage_partition_config.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/content/public/browser/storage_partition_config.h
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/storage/browser/blob/blob_url_registry.cc
[modify] https://crrev.com/8ffda44d4be8df2ea01ed48366527f97834e2a13/storage/browser/blob/blob_url_registry.h


### me...@chromium.org (2020-09-03)

With that CL this should be fixed in M87.

### [Deleted User] (2020-09-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-08)

Requesting merge to beta M86 because latest trunk commit (804321) appears to be after beta branch point (800218).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-08)

This bug requires manual review: M86's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-09-08)

To me, this looks significantly too complex to risk merging to M86 for a medium severity bug. Would you agree mek@?

### me...@chromium.org (2020-09-08)

Yes, I'd think so too. I think there is enough in the whole navigation flow that isn't understood very well that makes it hard to be fully confident that the fix doesn't have unintended side effects.

### ad...@chromium.org (2020-09-08)

OK. Let's wait till M87.

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations! The VRP panel has decided to award $15,000 for this report.

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1106890?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Storage, Blink>Storage>FileAPI, Internals>Sandbox>SiteIsolation, Platform>Apps>BrowserTag, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052878)*
