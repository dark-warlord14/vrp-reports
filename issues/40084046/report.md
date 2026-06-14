# Security: Universal XSS using a flaw in the load deferral logic

| Field | Value |
|-------|-------|
| **Issue ID** | [40084046](https://issues.chromium.org/issues/40084046) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-04-08 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

This is a regression from <https://crrev.com/f92a1f3b9> . Previously, ResourceLoader::start bailed out if ResourceLoader::m\_defersLoading was true. Now, it calls setDefersLoading on the associated WebURLLoader instead:

---

void ResourceLoader::start(ResourceRequest& request)  

{  

(...)  

m\_loader = adoptPtr(Platform::current()->createURLLoader());  

m\_loader->setDefersLoading(m\_fetcher->defersLoading());  

ASSERT(m\_loader);  

m\_loader->setLoadingTaskRunner(m\_fetcher->loadingTaskRunner());

```
if (m_resource->options().synchronousPolicy == RequestSynchronously)  
    requestSynchronously(request);  
else  
    m_loader->loadAsynchronously(WrappedResourceRequest(request), this);  

```
## }

## void WebURLLoaderImpl::setDefersLoading(bool value) { context\_->SetDefersLoading(value); }

## void WebURLLoaderImpl::Context::SetDefersLoading(bool value) { if (request\_id\_ != -1) resource\_dispatcher\_->SetDefersLoading(request\_id\_, value); (...) }

Note that |resource\_dispatcher\_->SetDefersLoading(request\_id\_, value)| isn't called because |request\_id\_| isn't set until after the |m\_loader->loadAsynchronously| call in ResourceLoader::start. Therefore, if a load is started after instantiating a ScopedPageLoadDeferrer, the pending request is never marked as deferred and it's allowed to proceed regardless of the deferral state of the fetcher. This allows an attacker to load cross-origin documents in numerous unexpected circumstances.

**VERSION**  

Chrome 51.0.2700.0 (Dev)  

Chromium 51.0.2703.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.0 KB)

## Timeline

### ke...@chromium.org (2016-04-08)

Thanks for the report.

japhet@: Can you please take a look?

[Monorail components: Blink>Loader]

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-04-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c5a3e99a81bee5f325b81be3d21f5daf1854b572

commit c5a3e99a81bee5f325b81be3d21f5daf1854b572
Author: japhet <japhet@chromium.org>
Date: Thu Apr 21 21:44:06 2016

Enable setting deferral state on ResourceDispatcher at request start

In https://chromium.googlesource.com/chromium/src/+/f92a1f3b9,
blink's ResourceLoader stopped handling load deferrals,
instead leaving it to WebURLLoaderImpl. However,
WebURLLoaderImpl can't quite do everything it needs to, as
ResourceDispatcher also needs to note that the load is
deferred, and it can't do that until a PendingRequest has
been created. Give ResourceDispatcher a way to immediately
mark a load a deferred on start.

BUG=601706

Review URL: https://codereview.chromium.org/1881023004

Cr-Commit-Position: refs/heads/master@{#388910}

[modify] https://crrev.com/c5a3e99a81bee5f325b81be3d21f5daf1854b572/content/child/resource_dispatcher.h
[modify] https://crrev.com/c5a3e99a81bee5f325b81be3d21f5daf1854b572/content/child/web_url_loader_impl.cc
[modify] https://crrev.com/c5a3e99a81bee5f325b81be3d21f5daf1854b572/content/child/web_url_loader_impl_unittest.cc


### sh...@chromium.org (2016-04-22)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-22)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### go...@chromium.org (2016-04-22)

Please merge your change to M51 branch 2704 before 5:00 PM PST Monday (04/25/16) so we can take it for next week M51 Beta candidate cut. Thank you.

### bu...@chromium.org (2016-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cdb8e78779913eca8c5860c8cb8642752b2b9a83

commit cdb8e78779913eca8c5860c8cb8642752b2b9a83
Author: Nate Chapin <japhet@chromium.org>
Date: Fri Apr 22 21:02:07 2016

Enable setting deferral state on ResourceDispatcher at request start

In https://chromium.googlesource.com/chromium/src/+/f92a1f3b9,
blink's ResourceLoader stopped handling load deferrals,
instead leaving it to WebURLLoaderImpl. However,
WebURLLoaderImpl can't quite do everything it needs to, as
ResourceDispatcher also needs to note that the load is
deferred, and it can't do that until a PendingRequest has
been created. Give ResourceDispatcher a way to immediately
mark a load a deferred on start.

BUG=601706

Review URL: https://codereview.chromium.org/1881023004

Cr-Commit-Position: refs/heads/master@{#388910}
(cherry picked from commit c5a3e99a81bee5f325b81be3d21f5daf1854b572)

Review URL: https://codereview.chromium.org/1910343006 .

Cr-Commit-Position: refs/branch-heads/2704@{#194}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/cdb8e78779913eca8c5860c8cb8642752b2b9a83/content/child/resource_dispatcher.h
[modify] https://crrev.com/cdb8e78779913eca8c5860c8cb8642752b2b9a83/content/child/web_url_loader_impl.cc
[modify] https://crrev.com/cdb8e78779913eca8c5860c8cb8642752b2b9a83/content/child/web_url_loader_impl_unittest.cc


### ja...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-06)

Another $7,500 for the tab!

### sh...@chromium.org (2016-07-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-08-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/601706?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084046)*
