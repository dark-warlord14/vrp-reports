# Security: UAF in BackForwardCache

| Field | Value |
|-------|-------|
| **Issue ID** | [40060508](https://issues.chromium.org/issues/40060508) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation>BFCache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2022-08-05 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**

When `RenderFrameHostManager` unload[1] the old frame, the old RenderFrameHost can be stored in the BackForwardCache:

```
if (can_store) {  
      auto stored_page = CollectPage(std::move(old_render_frame_host));  
      auto entry =  
          std::make_unique<BackForwardCacheImpl::Entry>(std::move(stored_page));  
      // Ensures RenderViewHosts are not reused while they are in the cache.  
      for (RenderViewHostImpl\* rvh : entry->render_view_hosts()) {  
        rvh->EnterBackForwardCache();  
      }  
      back_forward_cache.StoreEntry(std::move(entry));     <<<<===================  
      return;  
    }  

```

During the preparation[2] of the stored\_page, the RenderViewHost will be stored as a raw pointer into the page[a].  

And if the NewBrowsingContextStateOnBrowsingContextGroupSwap flag[3] is enabled, which will create a new BrowsingContextState for cross-BrowsingInstance navigations.  

The RenderFrameProxyHost will not be handled like the legacy mode[b,c], which will finally move the ownership of RenderFrameProxyHost into StoredPage:

```
std::unique_ptr<StoredPage> RenderFrameHostManager::CollectPage(  
    std::unique_ptr<RenderFrameHostImpl> main_render_frame_host) {  
  DCHECK(main_render_frame_host->is_main_frame());  
  
  std::set<RenderViewHostImpl\*> render_view_hosts;  
  BrowsingContextState::RenderFrameProxyHostMap proxy_hosts;  
  
  PrepareForCollectingPage(main_render_frame_host.get(), &render_view_hosts,  
                           &proxy_hosts);  
  
  auto stored_page = std::make_unique<StoredPage>(  
      std::move(main_render_frame_host), std::move(proxy_hosts),  
      std::move(render_view_hosts));  
  return stored_page;  
}  
  
void RenderFrameHostManager::PrepareForCollectingPage(  
[...]  
  for (auto& it :  
       main_render_frame_host->browsing_context_state()->proxy_hosts()) {  
    // This avoids including the proxy created when starting a  
    // new cross-process, cross-BrowsingInstance navigation, as well as any  
    // restored proxies which are also in a different BrowsingInstance.  
    if (instance->IsRelatedSiteInstance(it.second->GetSiteInstance())) {  
      (\*render_view_hosts).insert(it.second->GetRenderViewHost());       <<<<=================== [a]  
      // When BrowsingContextState is decoupled from the FrameTreeNode and  
      // RenderFrameHostManager (legacy mode is disabled), proxies and  
      // replication state will be stored in a separate BrowsingContextState,  
      // which won't need any updates. However, RenderViewHosts are still stored  
      // in FrameTree (which, for example, is shared between the new page and  
      // the page entering BFCache), so they have to be collected explicitly.  
      if (features::GetBrowsingContextMode() ==  
          features::BrowsingContextStateImplementationType::  
              kLegacyOneToOneWithFrameTreeNode) {  
        (\*proxy_hosts)[it.first] = std::move(it.second);                 <<<<=================== [b]  
      }  
    }  
  }  
  
  // Since proxies are not collected, we can return early here.  
  if (features::GetBrowsingContextMode() ==  
      features::BrowsingContextStateImplementationType::  
          kSwapForCrossBrowsingInstanceNavigations) {  
    return;  
  }  
  
  // Remove the previously extracted proxies from the  
  // RenderFrameHostManager, which also removes their respective  
  // SiteInstanceGroup::Observer.  
  for (auto& it : \*proxy_hosts) {  
    main_render_frame_host->browsing_context_state()  
        ->DeleteRenderFrameProxyHost(it.second->site_instance_group());  <<<<=================== [c]  
  }  
}  

```

Instead, it will be cleaned up by BrowsingContextState when the active frame count of the SiteInstanceGroup reaches 0[4]:

```
void SiteInstanceGroup::DecrementActiveFrameCount() {  
  if (--active_frame_count_ == 0) {  
    for (auto& observer : observers_)  
      observer.ActiveFrameCountIsZero(this);  <<<<===================  
  }  
}  

```
```
void BrowsingContextState::ActiveFrameCountIsZero(  
    SiteInstanceGroup\* site_instance_group) {  
  // |site_instance_group| no longer contains any active RenderFrameHosts, so we  
  // don't need to maintain a proxy there anymore.  
  RenderFrameProxyHost\* proxy = GetRenderFrameProxyHost(site_instance_group);  
  CHECK(proxy);  
  
  TRACE_EVENT_INSTANT("navigation",  
                      "BrowsingContextState::ActiveFrameCountIsZero",  
                      ChromeTrackEvent::kBrowsingContextState, this,  
                      ChromeTrackEvent::kRenderFrameProxyHost, proxy);  
  
  DeleteRenderFrameProxyHost(site_instance_group);  <<<<===================  
}  

```

However during the closing of the current tab, CloseWebContentses[5] will finally destruct the RenderFrameHostImpl, which will make active\_frame\_count\_ be 0 causing the destruction of RenderFrameProxyHost.  

At the same time, the destruction of RenderFrameProxyHost and RenderFrameHostImpl will cause the reference count of RenderViewHost to decrease to 0, causing RenderViewHost also to be destructed.

And the function SendDetachWebContentsNotifications[6] will finally access the dangling pointer `render_view_host`[7] stored in the cache entry.

```
bool TabStripModel::CloseTabs(base::span<content::WebContents\* const> items,  
                              uint32_t close_types) {  
   [...]  
   const bool closed_all =  
      CloseWebContentses(items, close_types, &notifications);  <<<<=================== [5]  
  
  // When unload handler is triggered for all items, we should wait for the  
  // result.  
  if (!notifications.detached_web_contents.empty())  
    SendDetachWebContentsNotifications(&notifications);  <<<<=================== [6]  
   [...]  
}  

```

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=758;drc=95e83f4fedc332ebf795ffcf4bfcf5b5f4fc13c7>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=635;drc=95e83f4fedc332ebf795ffcf4bfcf5b5f4fc13c7>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/browsing_context_state.cc;l=16;drc=144570103872b18d1b42489732c52c05fee8c3fd>

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/site_instance_group.cc;l=66;drc=2f3304a4b07df74dce8cc370264197ba3061bcf3>

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=1876;drc=3452787ce8ecfc41886eec1df408ffdfffa626d0>  

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=1881;drc=3452787ce8ecfc41886eec1df408ffdfffa626d0>

[7]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=9235;drc=1c6dd3e20c0967a410220dcc1e8c75c12f008da9>

**VERSION**  

Chrome Version: stable with NewBrowsingContextStateOnBrowsingContextGroupSwap feature

**REPRODUCTION CASE**

Apply the attached poc.diff  

$ python3 -m http.server 8000  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=NewBrowsingContextStateOnBrowsingContextGroupSwap "<http://localhost:8000/poc.html>"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 28.4 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 1.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 336 B)
- [blank.html](attachments/blank.html) (text/plain, 5 B)
- [close.html](attachments/close.html) (text/plain, 40 B)

## Timeline

### [Deleted User] (2022-08-05)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-05)

Thanks for the report!

fergal@, could you PTAL?

Marking this Security_Impact-None because AFAICT NewBrowsingContextStateOnBrowsingContextGroupSwap is not enabled by default anywhere. 

[Monorail components: UI>Browser>Navigation>BFCache]

### cr...@chromium.org (2022-08-05)

This seems very similar to https://crbug.com/chromium/1349086.  hbolaria@, can you take a look as well?

[Monorail components: Internals>Sandbox>SiteIsolation]

### fe...@google.com (2022-08-06)

Please CC me on 1349086, I don't have access.

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### cr...@chromium.org (2022-08-08)

[Empty comment from Monorail migration]

### fe...@google.com (2022-08-09)

Assigning to hbolaria to determine if this is a dupe.

### ra...@chromium.org (2022-08-09)

(reassigning to hbolaria@google.com as it looks like hbolaria@chromium.org doesn't exist?)

### hb...@google.com (2022-08-15)

This isn't quite a dupe of crbug.com/1349086 but the cause is exactly the same - that the new implementation of BrowsingContextState (non-legacy mode) needs to be revised. As noted in https://crbug.com/chromium/1350442#c15 on that bug, this doesn't appear to happen in legacy mode, and isn't exposed anywhere unless run from the command line. 

The issue with active frame count is a known issue that needs to be fixed, and this patch (https://chromium-review.googlesource.com/c/chromium/src/+/3404093) shows the failures. There have been issues of proxies existing for differing lifetimes to the BrowsingContextState, and this may be related to that.


### le...@gmail.com (2022-08-15)

Yes, agree with it. The new implementation of BrowsingContextState requires further modification. And I submited a new bug about BrowsingContextState, you can handle them together: https://crbug.com/chromium/1352972.

### ke...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2022-09-30)

https://chromium-review.googlesource.com/c/chromium/src/+/3911476 has fixed this issue.

https://crbug.com/chromium/1352972 also seems to be assignable to dtapuska@ to fix.

### le...@gmail.com (2022-10-05)

Friendly ping for the assignment mentioned in https://crbug.com/chromium/1350442#c14. And this issue could be marked as fixed.

### ra...@chromium.org (2022-10-05)

Yep crrev.com/c/3911476  should fix the RVH UAF here, thanks Dave for the fix and leecraso@ for noticing. crbug.com/1352972 is still not fixed though, not sure if dtapuska@ is up for that, as he isn't working on BrowsingContextState.

### [Deleted User] (2022-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-13)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $30,000 for this report. Nice finding! Thank you for your efforts in finding and reporting this issue to us --- great work! 

### am...@chromium.org (2022-10-13)

While I am here, reducing this issue to high severity as it relies on the precondition of a compromised renderer. 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### le...@gmail.com (2022-10-17)

Thanks a lot!

### [Deleted User] (2023-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-01-11)

This issue was migrated from crbug.com/chromium/1350442?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation>BFCache]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060508)*
