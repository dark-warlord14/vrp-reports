# Security: UAF in UrlLoaderFactoryProxyImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40053360](https://issues.chromium.org/issues/40053360) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vu...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2020-09-15 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

UrlLoaderFactoryProxyImpl is created with mojo::MakeSelfOwnedReceiver, and it holds a raw pointer to the RenderFrameHost without observing its lifetime.

Code Review

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/chrome_browser_interface_binders.cc;l=384;bpv=0;bpt=0>

```
void BindUrlLoaderFactoryProxy(  
    content::RenderFrameHost\* frame_host,  
    mojo::PendingReceiver<chrome::mojom::UrlLoaderFactoryProxy> receiver) {  
  UrlLoaderFactoryProxyImpl::Create(frame_host, std::move(receiver));  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/loader/url_loader_factory_proxy_impl.cc;l=18;bpv=0;bpt=0>

```
// static  
void UrlLoaderFactoryProxyImpl::Create(  
    content::RenderFrameHost\* frame_host,  
    mojo::PendingReceiver<chrome::mojom::UrlLoaderFactoryProxy> receiver) {  
  mojo::MakeSelfOwnedReceiver(  
      std::make_unique<UrlLoaderFactoryProxyImpl>(frame_host),  
      std::move(receiver));  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/loader/url_loader_factory_proxy_impl.cc;l=24;bpv=0;bpt=0>

```
UrlLoaderFactoryProxyImpl::UrlLoaderFactoryProxyImpl(  
    content::RenderFrameHost\* frame_host)  
    : frame_host_(frame_host) {}  

```

In `UrlLoaderFactoryProxyImpl::GetProxiedURLLoaderFactory()` , raw pointer `frame_host_` is used at :  

<https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/loader/url_loader_factory_proxy_impl.cc;l=31;bpv=0;bpt=0>

```
void UrlLoaderFactoryProxyImpl::GetProxiedURLLoaderFactory(  
    mojo::PendingRemote<network::mojom::URLLoaderFactory> original_factory,  
    mojo::PendingReceiver<network::mojom::URLLoaderFactory> proxied_factory) {  
  auto\* process = frame_host_->GetProcess();  
  auto\* browser_context = process->GetBrowserContext();  
  auto\* web_request_api =  
      extensions::BrowserContextKeyedAPIFactory<extensions::WebRequestAPI>::Get(  
          browser_context);  
  DCHECK(web_request_api);  
  
  web_request_api->MaybeProxyURLLoaderFactory(  
      browser_context, frame_host_, process->GetID(),  
      content::ContentBrowserClient::URLLoaderFactoryType::kDocumentSubResource,  
      /\*navigation_id=\*/base::nullopt, &proxied_factory,  
      /\*headber_client=\*/nullptr);  
  
  mojo::FusePipes(std::move(proxied_factory), std::move(original_factory));  
}  

```

UrlLoaderFactoryProxyImpl takes a raw pointer to RenderFrameHost, but it outlives RenderFrameHost,When RenderFrameHost is destructed it destroys the interface, but messages can still be queued on the binding. When this message is handled, |frame\_host\_| is used by `UrlLoaderFactoryProxyImpl::GetProxiedURLLoaderFactory()` method but the RenderFrameHost object that this pointer reference to is freed.  

the raw pointer to render\_frame\_host\_ resulting in a heap use-after-free in the browser process.

Note that this is \*not\* a renderer bug; it's a browser process bug that's reachable from the renderer.So it can lead to sandbox escape.

Patch Suggestion

Make the UrlLoaderFactoryProxyImpl a WebContentsObserver and clear its reference to the RenderFrameHost when the render frame is deleted.

You can refer to similar cases(<https://crbug.com/1122917https://crbug.com/1078671>).

**VERSION**  

Chrome Version:

**REPRODUCTION CASE**  

I will provide PoC as soon as possible. Thanks

Type of crash: browser

PATCH  

I will provide PoC as soon as possible. Thanks

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### vu...@gmail.com (2020-09-15)

here is patch.file

### li...@chromium.org (2020-09-15)

mmenke - could you take a look at this suggested patch or reassign if you're not the right person? Thanks!

[Monorail components: Internals>Network]

### mm...@chromium.org (2020-09-15)

I'm unfamiliar with this code - it looks like it was added literally yesterday.

### vu...@gmail.com (2020-09-16)

here is poc.html and asan.log

### [Deleted User] (2020-09-16)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vu...@gmail.com (2020-09-17)

update credit infomation

Reporter credit:	
Zhiyi Zhang from Codesafe Team of Legendsec at Qi'anxin Group

### vu...@gmail.com (2020-09-27)

[Comment Deleted]

### [Deleted User] (2020-09-29)

horo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2020-10-06)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-10-06)

Sorry for the delay.
Created a CL to fix this.
https://chromium-review.googlesource.com/c/chromium/src/+/2449676/

### vu...@gmail.com (2020-10-06)

hi @horo , https://crbug.com/chromium/1128270#c1 is a valid patch file for this bug. FYR

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1b624807138ec25519a7b1a22b94c55fcf5bf26

commit c1b624807138ec25519a7b1a22b94c55fcf5bf26
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Wed Oct 07 02:24:19 2020

Stop keeping raw pointer of RenderFrameHost in UrlLoaderFactoryProxyImpl

Bug: 1128270
Change-Id: I29d6caaba1093baf46d3ac6086db3aca7a4cb4e0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2449676
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#814518}

[modify] https://crrev.com/c1b624807138ec25519a7b1a22b94c55fcf5bf26/chrome/browser/loader/url_loader_factory_proxy_impl.cc
[modify] https://crrev.com/c1b624807138ec25519a7b1a22b94c55fcf5bf26/chrome/browser/loader/url_loader_factory_proxy_impl.h


### ho...@chromium.org (2020-10-07)

>  vulbugs@
Thank you for your patch :)
But I have submitted the fix in a different way.


### vu...@gmail.com (2020-10-07)

horo@ It is pretty good!

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

This release blocking issue appears to be targeted for M87, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after October 01 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-87 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### la...@google.com (2020-10-08)

[Empty comment from Monorail migration]

### la...@google.com (2020-10-08)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9da826d3525d0675e589d80f452b3702ae453415

commit 9da826d3525d0675e589d80f452b3702ae453415
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Fri Oct 09 02:31:53 2020

[M87] Stop keeping raw pointer of RenderFrameHost in UrlLoaderFactoryProxyImpl

(cherry picked from commit c1b624807138ec25519a7b1a22b94c55fcf5bf26)

Bug: 1128270
Change-Id: I29d6caaba1093baf46d3ac6086db3aca7a4cb4e0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2449676
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#814518}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2462750
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#178}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/9da826d3525d0675e589d80f452b3702ae453415/chrome/browser/loader/url_loader_factory_proxy_impl.cc
[modify] https://crrev.com/9da826d3525d0675e589d80f452b3702ae453415/chrome/browser/loader/url_loader_factory_proxy_impl.h


### la...@google.com (2020-10-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-14)

Congratulations! The VRP program has decided to award $20,000 for this bug.

### ad...@google.com (2020-10-16)

[Empty comment from Monorail migration]

### vu...@gmail.com (2020-11-25)

hello, this bug is fixed in release version 87.0.4280.66, but I can't find the CVE about this bug .
https://chromium.googlesource.com/chromium/src.git/+/refs/tags/87.0.4280.66/chrome/browser/loader/url_loader_factory_proxy_impl.cc

### [Deleted User] (2021-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-15)

Re https://crbug.com/chromium/1128270#c28 sorry for the delayed reply. We only allocate CVEs for bugs which impact our stable channel, and thanks to you we fixed this before it impacted stable. (In the language of all our bug labels, it's "Security_Impact-Head" not "Security_Impact-Stable".)

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1128270?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1134480]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053360)*
