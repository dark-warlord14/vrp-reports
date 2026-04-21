# Security: UAF in CacheAliasSearchPrefetchURLLoader::StartPrefetchRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [40059973](https://issues.chromium.org/issues/40059973) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Preload |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ry...@chromium.org |
| **Created** | 2022-06-15 |
| **Bounty** | $1,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

When you type things into omnibox, a request can be sent even if you don't press enter because Chromium can prefetch answers to make things speedier. As you press enter, Chromium will use `CacheAliasSearchPrefetchURLLoader` to check prefetch responses from cache and if no match is available, it'll fetch the URL directly.

This bug does not require a compromised renderer.

In `CacheAliasSearchPrefetchURLLoader::SetUpForwardingClient`, our attack window begins [1] as the object's lifetime is now tied to mojo receiver and not to `Profile` anymore.  

We then have 4 different paths [2][3][4][5] that'll all lead to UAF in `CacheAliasSearchPrefetchURLLoader::StartPrefetchRequest` when dereferencing `profile_` if `Profile` has been destroyed in the meanwhile. [0] `prefetch_loader_` is owned by `CacheAliasSearchPrefetchURLLoader` so callback [5] is still valid after Profile destruction.

```
void CacheAliasSearchPrefetchURLLoader::SetUpForwardingClient(  
    std::unique_ptr<SearchPrefetchURLLoader> loader,  
    const network::ResourceRequest& resource_request,  
    mojo::PendingReceiver<network::mojom::URLLoader> receiver,  
    mojo::PendingRemote<network::mojom::URLLoaderClient> forwarding_client) {  
  resource_request_ =  
      std::make_unique<network::ResourceRequest>(resource_request);  
  
  // Bind to the content/ navigation code.  
  DCHECK(!receiver_.is_bound());  
  
  // At this point, we are bound to the mojo receiver, so we can release  
  // |loader|, which points to |this|.  
  receiver_.Bind(std::move(receiver));    //// [1]  
  loader.release();  
  receiver_.set_disconnect_handler(base::BindOnce(  
      &CacheAliasSearchPrefetchURLLoader::MojoDisconnectWithNoFallback,  
      weak_factory_.GetWeakPtr()));  
  forwarding_client_.Bind(std::move(forwarding_client));  
  
  // The prefetch is already in the disk cache when there is no prefetch loader.  
  if (!prefetch_loader_) {  
    StartPrefetchRequest();                     //// [2]  
    return;  
  }  
  
  prefetch_loader_->RecordNavigationURLHistogram(resource_request_->url);  
  
  // Either use the prefetch, restart to the direct URL, or wait for headers to  
  // complete.  
  if (prefetch_loader_->ReadyToServe()) {  
    StartPrefetchRequest();                      //// [3]  
  } else if (prefetch_loader_->ReceivedError()) {  
    RestartDirect();                             //// [4]  
  } else {  
    prefetch_loader_->SetHeadersReceivedCallback(  
        base::BindOnce(&CacheAliasSearchPrefetchURLLoader::HeadersReceived, //// [5]  
                       base::Unretained(this)));  
  }  
}  

```

The last path [5] allows for the widest attack window between the object's lifetime being bound to receiver [1] and `profile_` being dereferenced [0] as the callback will run once headers are received and this will depend on how slow your internet connection is.  

Once the headers are received, `StartPrefetchRequest` will run and `profile_` will be dereferenced but there is no check that `profile_` is still alive thus leading to UAF. [0]

```
void CacheAliasSearchPrefetchURLLoader::StartPrefetchRequest() {  
  network::ResourceRequest prefetch_request = \*resource_request_;  
  
  prefetch_request.load_flags |= net::LOAD_ONLY_FROM_CACHE;  
  prefetch_request.url = prefetch_url_;  
  
  auto url_loader_factory = profile_->GetDefaultStoragePartition()    //// [0] UAF  
                                ->GetURLLoaderFactoryForBrowserProcess();  

```

I can hit the breakpoint in [0] with my debugger and it does result in a crash but for some reason I can't make it work yet on my asan build.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/prefetch/search_prefetch/cache_alias_search_prefetch_url_loader.cc;l=51;drc=0e47fede6c04a1c03aed24541a98d7ce66a5889e>  

[0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/prefetch/search_prefetch/cache_alias_search_prefetch_url_loader.cc;l=98;drc=0e47fede6c04a1c03aed24541a98d7ce66a5889e>

**VERSION**  

Chrome Version: Chromium 105.0.5121.0  

Operating System: Ubuntu 20.04.4 LTS

**REPRODUCTION CASE**  

In terms of reproducibility, the attack window depends on your internet connection so you might get better results if you use a proxy and hold the response from the server for a second to give more time for Profile to be destroyed.  

0/ set your proxy to intercept responses  

1/ Launch chrome  

out/Debug/chrome --user-data-dir=/tmp/xxx/ --enable-features=SearchNavigationPrefetch,SearchPrefetchUsesNetworkCache  

2/ type something in omnibox  

3/ press enter and immediately close window (at that point, the response is still in limbo in the proxy)  

4/ stop intercept and that'll trigger [5] which will trigger [0] and your browser should hopefully crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: micah hu (@micah\_hu)

## Timeline

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-15)

Thanks for the report! +ryansturm@ based on git blame. This is a browser UaF, but requires profile shutdown. Setting severity to high for now.

[Monorail components: Internals>Preload]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### ry...@chromium.org (2022-06-16)

Is [5] the only case that can UAF, and is this only a vulnerability with SearchPrefetchUsesNetworkCache enabled? If so, SearchPrefetchUsesNetworkCache is not enabled anywhere and is only partially implemented (although some version of it was on in canary for a few days).

Is CacheAliasSearchPrefetchURLLoader the UAF or is profile the UAF? I could see the base::unretained being the real problem with this.

Either way, I'll just remove the feature code rather than fix it, as we are not going to enable that feature without a total re-write.

Please let me know if there is a way to UAF without enabling SearchPrefetchUsesNetworkCache, as that would be a large concern.

### ry...@chromium.org (2022-06-16)

I found another case in similar code that will actually be rolled out eventually, so I'll fix both places, and I can file a different bug to remove the feature.

### ry...@chromium.org (2022-06-16)

Candidate CL that I'll try to get merge back to 104:
https://chromium-review.googlesource.com/c/chromium/src/+/3709539/

None of the code paths with this problem are currently running on any release channel.

### mi...@gmail.com (2022-06-16)

https://crbug.com/chromium/1336622#c4 From reading the code, it seems to me that [2][3][4] as well as [5] should trigger UAF but in practice, the timing window is very tight and we can't really know exactly when exactly profile gets destroyed so I haven't been able to try it. This is why [5] is more convenient because the delay in getting the response lengthens the attack window.

As far as I can tell, that code can only be hit with `SearchPrefetchUsesNetworkCache` enabled but I'm not yet experienced enough to tell if it'd be possible to hit that code if I had a compromised renderer.

I believe the problem here is the raw pointer to profile_. I think this instance of `base::unretained` is fine as the callback only runs if `prefetch_loader_` [0] is still alive which is a `std::unique_ptr<StreamingSearchPrefetchURLLoader>` owned by `CacheAliasSearchPrefetchURLLoader`.

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/prefetch/search_prefetch/cache_alias_search_prefetch_url_loader.h;l=125;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4

### ry...@chromium.org (2022-06-16)

I see what you are saying. I'll replace the raw ptrs to profile since the mojo ownership does cause a delay in destroying the object and profile could shut down in that delay.

### [Deleted User] (2022-06-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e681b6e30edd8872c97cdd9e713f9f97ca519346

commit e681b6e30edd8872c97cdd9e713f9f97ca519346
Author: Ryan Sturm <ryansturm@chromium.org>
Date: Thu Jun 16 19:31:04 2022

[Fix it] Removing profile raw ptr from mojo lifetime prefetch objects

This CL replaces some raw ptrs to Profile with weak ptrs or scoped ref
ptrs to the relevant objects that profile was used to get. Since these
objects are managed via mojo there is a time gap where using a profile
raw pointer can UAF during/after profile shutdown.

Bug: 1336622
Change-Id: I1bd3fec618d9f1f5225c1e8efb5c3a4e6d30bfab
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3709539
Reviewed-by: Max Curran <curranmax@chromium.org>
Commit-Queue: Ryan Sturm <ryansturm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1015041}

[modify] https://crrev.com/e681b6e30edd8872c97cdd9e713f9f97ca519346/chrome/browser/prefetch/search_prefetch/cache_alias_search_prefetch_url_loader.h
[modify] https://crrev.com/e681b6e30edd8872c97cdd9e713f9f97ca519346/chrome/browser/prefetch/search_prefetch/cache_alias_search_prefetch_url_loader.cc
[modify] https://crrev.com/e681b6e30edd8872c97cdd9e713f9f97ca519346/chrome/browser/prefetch/search_prefetch/streaming_search_prefetch_url_loader.h
[modify] https://crrev.com/e681b6e30edd8872c97cdd9e713f9f97ca519346/chrome/browser/prefetch/search_prefetch/streaming_search_prefetch_url_loader.cc
[modify] https://crrev.com/e681b6e30edd8872c97cdd9e713f9f97ca519346/chrome/browser/prefetch/search_prefetch/search_prefetch_service.h


### ry...@chromium.org (2022-06-16)

I'll wait a few days before merging, but all the paths that could actually be re-pro'd are not enabled broadly.

### xi...@chromium.org (2022-06-17)

Thanks for the quick fix! Since SearchPrefetchUsesNetworkCache is not enabled anywhere, adjusting the impact to none.

### ry...@chromium.org (2022-06-21)

Since this isn't enabled elsewhere, I don't think this meets the merge guidelines.

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

this issue appears fairly hard to exploit given the tight race condition with user input and being fairly substantially mitigated, and also being a shutdown bug; this appears to be more of a borderline low to medium severity issue, so adjusting severity accordingly 

### am...@chromium.org (2022-06-29)

Congratulations, Micah! The VRP Panel has decided to award you $1,000 for this report. The reward amount was based on the lower potential of exploitability and the substantial mitigations presented by the preconditions listed in the comment above. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1336622?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059973)*
