# Security: UAF in DirectSocketsServiceImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40053185](https://issues.chromium.org/issues/40053185) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vu...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2020-08-28 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

DirectSocketsServiceImpl is created with mojo::MakeSelfOwnedReceiver, and it holds a raw pointer to the RenderFrameHost without observing its lifetime.

Code Review

This bug need to enable `kDirectSockets` feature on android  

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/browser_interface_binders.cc;l=743;bpv=0;bpt=1>

```
#if !defined(OS_ANDROID)  
  if (base::FeatureList::IsEnabled(features::kDirectSockets)) {  
    map->Add<blink::mojom::DirectSocketsService>(  
        base::BindRepeating(&DirectSocketsServiceImpl::CreateForFrame));  
  }  

```

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=39;drc=852cbbc09103cd88b9a7a10066d31d4ea4e3f89e;bpv=1;bpt=0>

```
// static  
void DirectSocketsServiceImpl::CreateForFrame(  
    RenderFrameHost\* render_frame_host,  
    mojo::PendingReceiver<blink::mojom::DirectSocketsService> receiver) {  
  DCHECK_CURRENTLY_ON(BrowserThread::UI);  
  mojo::MakeSelfOwnedReceiver(  
      std::make_unique<DirectSocketsServiceImpl>(\*render_frame_host),  
      std::move(receiver));  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=30;drc=852cbbc09103cd88b9a7a10066d31d4ea4e3f89e;bpv=1;bpt=0>

```
DirectSocketsServiceImpl::DirectSocketsServiceImpl(RenderFrameHost& frame_host)  
    : frame_host_(&frame_host) {}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=114;drc=852cbbc09103cd88b9a7a10066d31d4ea4e3f89e;bpv=1;bpt=0>  

In DirectSocketsServiceImpl::GetNetworkContext(), raw pointer `frame_host_` is used at :

```
network::mojom::NetworkContext\* DirectSocketsServiceImpl::GetNetworkContext() {  
  return frame_host_->GetStoragePartition()->GetNetworkContext();  
}  

```

We can use `DirectSocketsServiceImpl::OpenTcpSocket()` or `DirectSocketsServiceImpl::OpenUdpSocket()` to call `DirectSocketsServiceImpl::GetNetworkContext()`  

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/direct_sockets/direct_sockets_service_impl.cc;l=43;drc=852cbbc09103cd88b9a7a10066d31d4ea4e3f89e;bpv=1;bpt=0>

```
void DirectSocketsServiceImpl::OpenTcpSocket(  
    blink::mojom::DirectSocketOptionsPtr options,  
    OpenTcpSocketCallback callback) {  
  if (!options) {  
    mojo::ReportBadMessage("Invalid request to open socket");  
    return;  
  }  
  net::Error result = EnsurePermission(\*options);  
  
  // TODO(crbug.com/1119681): Collect metrics for usage and permission checks  
  
  if (result == net::OK) {  
    // TODO(crbug.com/905818): GetNetworkContext()->CreateTCPConnectedSocket  
    GetNetworkContext();                                                        // <--- invoke   
    NOTIMPLEMENTED();  
  }  
  
  std::move(callback).Run(result);  
}  
  
void DirectSocketsServiceImpl::OpenUdpSocket(  
    blink::mojom::DirectSocketOptionsPtr options,  
    OpenUdpSocketCallback callback) {  
  if (!options) {  
    mojo::ReportBadMessage("Invalid request to open socket");  
    return;  
  }  
  net::Error result = EnsurePermission(\*options);  
  
  // TODO(crbug.com/1119681): Collect metrics for usage and permission checks  
  
  if (result == net::OK) {  
    // TODO(crbug.com/1119620): GetNetworkContext()->CreateUDPSocket  
    GetNetworkContext();                                                        // <--- invoke  
    NOTIMPLEMENTED();  
  }  
  
  std::move(callback).Run(result);  
}  

```

DirectSocketsServiceImpl takes a raw pointer to RenderFrameHost, but it outlives RenderFrameHost,When RenderFrameHost is destructed it destroys the interface, but messages can still be queued on the binding. When this message is handled, |frame\_host\_| is used by `DirectSocketsServiceImpl::OpenTcpSocket()` or `DirectSocketsServiceImpl::OpenUdpSocket()` method but the RenderFrameHost object that this pointer reference to is freed.  

the raw pointer to render\_frame\_host\_ resulting in a heap use-after-free in the browser process.

Note that this is \*not\* a renderer bug; it's a browser process bug that's reachable from the renderer.So it can lead to sandbox escape.

Patch Suggestion

Make the DirectSocketsServiceImpl a WebContentsObserver and clear its reference to the RenderFrameHost when the render frame is deleted.

You can refer to similar cases(<https://crbug.com/1073015> <https://crbug.com/1078671>).

**VERSION**  

Chrome Version: Dev

**REPRODUCTION CASE**  

I will provide PoC as soon as possible. Thanks

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit:  

Zhiyi Zhang from Codesafe Team of Legendsec at Qi'anxin Group

## Attachments

- [directsockets.html](attachments/directsockets.html) (text/plain, 1.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.7 KB)

## Timeline

### ts...@chromium.org (2020-08-28)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-08-28)

[marking component as websockets although the new direct socket feature should likely be added as its own component in the bug tracker]


[Monorail components: Blink>Network>WebSockets]

### [Deleted User] (2020-08-28)

[Empty comment from Monorail migration]

### er...@chromium.org (2020-08-29)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Network>WebSockets Blink>Network]

### er...@chromium.org (2020-08-30)

https://chromium-review.googlesource.com/c/chromium/src/+/2383531

### vu...@gmail.com (2020-08-30)

Here are the poc and asan log.



### vu...@gmail.com (2020-08-30)

[Comment Deleted]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fe9666e737fb3c733e0f1574f575e5d40a3b4f2e

commit fe9666e737fb3c733e0f1574f575e5d40a3b4f2e
Author: Eric Willigers <ericwilligers@chromium.org>
Date: Mon Aug 31 03:04:56 2020

Direct Sockets: Detect when render frame is deleted

DirectSocketsServiceImpl is now a WebContentsObserver.

OpenTcpSocket() and OpenUdpSocket() now fail safely if they are called
after the RenderFrameHost is destroyed.


Bug: 1122917
Change-Id: I4a880c9aee73271cd5895818e0da3d85e32a8e5b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2383531
Auto-Submit: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Glen Robertson <glenrob@chromium.org>
Reviewed-by: Glen Robertson <glenrob@chromium.org>
Cr-Commit-Position: refs/heads/master@{#803005}

[modify] https://crrev.com/fe9666e737fb3c733e0f1574f575e5d40a3b4f2e/content/browser/direct_sockets/direct_sockets_service_impl.cc
[modify] https://crrev.com/fe9666e737fb3c733e0f1574f575e5d40a3b4f2e/content/browser/direct_sockets/direct_sockets_service_impl.h
[add] https://crrev.com/fe9666e737fb3c733e0f1574f575e5d40a3b4f2e/content/browser/direct_sockets/direct_sockets_unittest.cc
[modify] https://crrev.com/fe9666e737fb3c733e0f1574f575e5d40a3b4f2e/content/test/BUILD.gn


### er...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-31)

[Empty comment from Monorail migration]

### er...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-08)

ericwilligers@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-09-09)

Assuming applies to all OSs other than Android.

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations! The VRP panel has decided to award $20,000 for this report. Thanks for raising it.

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

hi, vulbugs@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-03-29)

This issue was migrated from crbug.com/chromium/1122917?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1122904]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053185)*
