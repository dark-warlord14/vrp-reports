# Security: heap after free at `RenderFrameHostManager::GetFrameHostForNavigation`

| Field | Value |
|-------|-------|
| **Issue ID** | [40073755](https://issues.chromium.org/issues/40073755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 18...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2023-09-29 |
| **Bounty** | $1,000.00 |

## Description

Hey, I want to report a UAF bug at [RenderFrameHostManager::GetFrameHostForNavigation](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1527). however , The bug is a strange bug(because there not only one bug, and I don't know should I report them in spearete issues, so I just write it at here), so I write it in details. the most related bugs in the `|pre knowledge part|` been introduced. If u are not intersting about this, feel free skip it, and read the conclusion part.

##  pre knowledge

The fist bug been found when I inverstigate does `|GetFrameHostForNavigation|` function could free a `|NavigationRequest object|`? , because in [navigation_request.cc](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc) too much code don't check the `|this object|` has been destory by this function or not....

```
    if (auto result =
            frame_tree_node_->render_manager()->GetFrameHostForNavigation(  //  [+] @a
                this, &browsing_context_group_swap_, &rfh_selected_reason);
        result.has_value()) {
      render_frame_host_ = result.value()->GetSafeRef();
    } else {
      [....]
    }

    // GetFrameHostForNavigation() should update associated_rfh_type_, so it
    // should never be NONE here.
    DCHECK_NE(AssociatedRenderFrameHostType::NONE, associated_rfh_type_);

    if (!Navigator::CheckWebUIRendererDoesNotDisplayNormalURL(  //  [+] @b
            GetRenderFrameHost(), GetUrlInfo(),
            /* is_renderer_initiated_check */ false)) {
      CHECK(false);
    }
```

Like this one, If I could `|delete this pointer|`, I should `|trigger a uaf at @b|`.

And with more inverstigate, I found `|GetFrameHostForNavigation|` will finnally could call [RenderFrameHostManager::CommitPending](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=4702;bpv=1;bpt=1), which will call  `UnloadOldFrame` , and finnal destory a `|RenderFrameHostImpl|` object.

The `|RenderFrameHostImpl|` destructor has [a very intersting code](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=1719) at here:

```
  // Cancel the navigations (including the ones that are not owned by this
  // RenderFrameHost) that intends to commit in this RenderFrameHost, as they
  // can no longer do so.
  {
    CHECK(frame_tree_node_);
    NavigationRequest* navigation_request =
        frame_tree_node_->navigation_request();
    if (navigation_request) {
      if (navigation_request
              ->GetRenderFrameHostRestoredFromBackForwardCache() == this) {
        CHECK(navigation_request->IsServedFromBackForwardCache());  //  [+] @a
        frame_tree_node_->RestartBackForwardCachedNavigationAsync(
            navigation_request->nav_entry_id());
      } else if (navigation_request->state() >=
                     NavigationRequest::WILL_PROCESS_RESPONSE &&
                 navigation_request->GetRenderFrameHost() == this) {
        frame_tree_node_->ResetNavigationRequest( //  [+] @b
            NavigationDiscardReason::kRenderFrameHostDestruction);
        // As we are unable to come up with a case that will lead to this path,
        // we instead record the dumps for debugging the scenario.
        // TODO(crbug.com/1430653): if we verify that this path is impossible,
        // replace the `DumpWithoutCrashing` with a `CHECK`. Otherwise, add a
        // new browser test for it.
        base::debug::DumpWithoutCrashing();
        NOTREACHED();
      }
    }
  }
```

Here are two path, which both are intersting.

1. If we could hit `|@a|`, we could `|reset|` the `|navigation_request_|` in function `|RestartBackForwardCachedNavigationAsync|`. 
2. at `@b`, it will hit a `DCHECK error`, in release version, we will reset the `|navigation_request_|`.

I am not familiar with `|BackForwardCache|`, so I abandon `|@b|`, even if it is more intersting, because if we use `|@a|`, we more like use `|bug|` to build `|bug|`.

Then I looked into chrome codebase, try to find `|a|` way to hit the path.

And I found an intersting comment which by `|rakina@chromium.org|` at [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=5408), 

```
    // Reset the RenderFrameHost that had been computed for the commit of the
    // navigation.
    // TODO(https://crbug.com/1416916): Reconsider if we really need to unset
    // the `render_frame_host_` here, as the NavigationRequest might stay alive
    // for a bit longer to commit an error page.
    render_frame_host_ = absl::nullopt;
```

My answer is no... If we remove this, I could trigger the bug easily... u could use a smaple test which named `|4278923_issue.cpp|` to trigger a asan log(4278923_issue_asan.txt). 

I found `NavigationRequest::OnWillProcessResponseChecksComplete` is hard to trigger this bug, because it always set `|render_frame_host_|` be nullptr. So I try to search another way, I found two function is intersting:

1. [NavigationURLLoaderImpl::OnComplete](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=1073)
2. [NavigationRequest::OnWillCommitWithoutUrlLoaderChecksComplete](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=5441)

The above function both could call `|OnRequestFailedInternal|` without reset `|render_frame_host_|`. 

The poc Which I offered use `|NavigationRequest::OnWillCommitWithoutUrlLoaderChecksComplete|`. 

##  conclusioin part

In function [RenderFrameHostManager::GetFrameHostForNavigation](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1527)

```
    // Check for cases that a speculative RenderFrameHost cannot be used and
    // create a new one if needed.
    if (!speculative_render_frame_host_ ||
        speculative_render_frame_host_->GetSiteInstance() !=
            dest_site_instance.get()) {
      [...]
      DiscardSpeculativeRFH(NavigationDiscardReason::kNewNavigation); //  [+] @a
      [...]
    } else {
      AppendReason(reason,
                   "GetFrameHostForNavigation / existing-speculative-rfh");
    }
    DCHECK(speculative_render_frame_host_);

    navigation_rfh = speculative_render_frame_host_.get();
    request->SetAssociatedRFHType(  //  [+] @b
        NavigationRequest::AssociatedRenderFrameHostType::SPECULATIVE);

```

at `|@a|`, `|DiscardSpeculativeRFH|` could free the `|request|` object, and use at `|@b|` will trigger the `|UAF|` bug(U could see the details in the asan.txt).

##  reproduce

My chormium version is:

``` c++
commit 3dfd75b7f885d39eb5c712fa2ba9f65020558796 (grafted, HEAD, origin/main)
Author: Rupert Wiser <bewise@chromium.org>
Date:   Thu Sep 28 12:08:08 2023 +0000

    Revert "Reland "[Page Zoom] Add unit tests for PageZoomPreference""

    This reverts commit aad044411044dc3c2b38e1eb871d28aa159fecf2.
```

just replace the `|ThrottleDeferAndCancelCommitWithoutUrlLoader|` function which in `|navigation_request_browsertest.cc|` into `|patch.cpp|`, build chromium with asan , run this command:

> .\out\asan\content_browsertests.exe  --gtest_filter=NavigationRequestBrowserTest.ThrottleDeferAndCancelCommitWithoutUrlLoader

U should see asan error like `|asan.txt|`.

##  note

I offer the poc in sample test file way, But chromium team seems more like pure html way. And unlike [https://crbug.com/chromium/1487110](https://bugs.chromium.org/p/chromium/issues/detail?id=1487110) which I report before. The bug not only trigger in android platform, So I could build it by myself :( , I will upload the `|pure html poc|` soon. 


##  bitsec & patch

The bug history is so complicated, In old version, we could trigger this in another easy way, but for this trigger poc, this comment is needed.

>   https://chromium-review.googlesource.com/c/chromium/src/+/4210858

And the patch is complicated too... bandage patch seems not fit at here, I will think about this once I finish my work...

Thx!

## Attachments

- [patch.cpp](attachments/patch.cpp) (text/plain, 3.4 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 23.5 KB)
- [4278923_issue.cpp](attachments/4278923_issue.cpp) (text/plain, 3.3 KB)
- [4278923_issue_asan.txt](attachments/4278923_issue_asan.txt) (text/plain, 23.7 KB)
- [server.py](attachments/server.py) (text/plain, 1.7 KB)
- [found_18f.pem](attachments/found_18f.pem) (application/octet-stream, 2.8 KB)
- [fake_asan.log](attachments/fake_asan.log) (text/plain, 32.4 KB)
- [fake_patch.diff](attachments/fake_patch.diff) (text/plain, 1.5 KB)

## Timeline

### [Deleted User] (2023-09-29)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-29)

We definitely do prefer pure HTML reproduction cases if you can make one! There are two reasons:
a) it gives very direct evidence that this is exploitable by a remote attacker
b) it enables us to use our automated triage systems which can assemble lots more information about what went wrong.

This is definitely more useful and important than a patch to fix the bug.

Do you really think you'll be able to come up with an HTML reproducer here? When?

### ad...@google.com (2023-09-29)

cc rakina@ who is mentioned in the bug description :) Rakina, whether or not this turns out to be a valid security bug, it sounds like you have a possible answer to your TODO.

### 18...@gmail.com (2023-09-29)

[Comment Deleted]

### ra...@chromium.org (2023-10-03)

Thanks for the report! I haven't looked into this too deeply, but I think this can lead to a real UAF. I'll take a look at this with leimy@ and report back.

[Monorail components: UI>Browser>Navigation]

### 18...@gmail.com (2023-10-03)

Hey, Thanks for your reply. 

I promise `|adetaylor|` I will  archive the pure html in one weeks. But this week autually is China's National Day, and I need to attend my friend's wedding. So, for the next two to three days, I won't be able to continue spending time on this vulnerability. I'm truly sorry about this. I will write about my current research progress, and if you're interested, I hope this can help you a bit.

To trigger this vulnerability, a necessary condition must be met. When the function `RenderFrameHostManager::GetFrameHostForNavigation` is invoked, it's essential that the render_frame_host_ bound to the NavigationRequest is not null. This is crucial. Personally, I find the most interesting way to achieve this is by using the `CancelDeferredNavigation` function to trigger OnRequestFailedInternal. Please note that this is my personal view on what's most interesting, but it's not the only triggering path.

About this path:

```
void NavigationRequest::CancelDeferredNavigationInternal(
    NavigationThrottle::ThrottleCheckResult result) {
  [...]
  NavigationState old_state = state_;
  SetState(CANCELING);  //  [+] @a
  [...]
  switch (old_state) {
    case WILL_START_REQUEST:
      OnStartChecksComplete(result);
      return;
    case WILL_REDIRECT_REQUEST:
      OnRedirectChecksComplete(result);
      return;
    [...]
  }
}
```

As u see, at `|@a|`, any state will be update to `|CANCELING|`. so we could choose any `old_state`. But I the most interesting state are `|WILL_REDIRECT_REQUEST|` and `|WILL_START_REQUEST|`, because they won't update `|render_frame_host_|` like `| NavigationRequest::OnWillProcessResponseChecksComplete|`.

And another important tips is :

``` c++
void NavigationRequest::OnRequestFailedInternal(
    const network::URLLoaderCompletionStatus& status,
    bool skip_throttles,
    const absl::optional<std::string>& error_page_content,
    bool collapse_frame) {
  [...]
  if (MaybeCancelFailedNavigation())
    return;
  [...]
  SelectFrameHostForOnRequestFailedInternal(status.exists_in_cache,
                                            skip_throttles, error_page_content);
}
```

we need pass `|MaybeCancelFailedNavigation|` check, that's means `|net::ERR_ABORTED == net_error_|` should return false.

Sumarry this:

1. I need find a throttle which overwrite `|WillStartRequest|` or `|WillRedirectRequest|` function, which give me a good `old_state`.
2. The throttle could call `|CancelDeferredNavigation|` and the `|net_error_|` should not be `|net::ERR_ABORTED |`.

I constructed a fake PoC to demonstrate that my hypothesis is correct. U could use this step to repro it.

``` c++
set the git to commit `|3dfd75b7f885d39eb5c712fa2ba9f65020558796|`.
set the patch: patch -p1 < fake_patch.diff
compile chromium: compile chromium `release asan` version
start the server: Python38\python3.exe .\server.py // [+] python 3.8 seems important
run this command to trigger a asan error:
>   out/asan/chrome.exe --user-data-dir=D:\bad_log  "https://localhost:8000/poc.html" --no-first-run --no-sandbox // [+] change D:\bad_log to your custome directory...
```

And I found that many 'throttle' cases meet the conditions described above. like [SupervisedUserNavigationThrottle](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_navigation_throttle.cc;l=198).

Sadly, When I build a poc for this `|throttle|`, I found If I use `|WILL_REDIRECT_REQUEST|` to hit the `|CancelDeferredNavigationInternal|`. I found when I hit this function, The `|NavigationRequest's|` field `|render_frame_host_|` already be `|null|`. So I need find a way to hit the `|CancelDeferredNavigationInternal|` function with `|WILL_REDIRECT_REQUEST|` , and the `|render_frame_host_|` should not be `null`. I still inverstigating this, but `Windbg TTD` work bad for `|chrome|`, so It need a little time. When I come back, I will try to finish this.

Thx.

### aj...@google.com (2023-10-03)

Looking at fake_patch - could you explain what state you are simulating here:-

--- a/content/browser/renderer_host/navigation_request.cc
+++ b/content/browser/renderer_host/navigation_request.cc
@@ -6774,6 +6774,8 @@ void NavigationRequest::CancelDeferredNavigationInternal(
          state_ == WILL_START_REQUEST || state_ == WILL_REDIRECT_REQUEST);
 
   EnterChildTraceEvent("CancelDeferredNavigation", this);
+  //    [+] assume I has already build a `|OnRedirectChecksComplete|` state
+  SetState(WILL_REDIRECT_REQUEST);
   NavigationState old_state = state_;
   SetState(CANCELING);
   if (complete_callback_for_testing_ &&

normally this function immediately calls SetState(CANCELING) ?

### 18...@gmail.com (2023-10-03)

it will make the old state be `| WILL_REDIRECT_REQUEST  |`. `| simulating |` the `| CancelDeferredNavigationInternal  |` function called by overwrite `|WillStartRequest|` function.

### aj...@google.com (2023-10-03)

[Empty comment from Monorail migration]

### aj...@google.com (2023-10-03)

With the poc in https://crbug.com/chromium/1487944#c6 I'm not able to reproduce a crash on Windows. It might be helpful to know your build arguments and operating system?

### 18...@gmail.com (2023-10-03)

# Build arguments go here.
# See "gn args <out_dir> --list" for available build arguments.
is_debug = false
is_asan = true
dcheck_always_on = false
enable_rust = false
treat_warnings_as_errors = false

Intersting, I could repro it on my machine stable.

### 18...@gmail.com (2023-10-03)

and my system is windows, does u change -user-data-dir=D:\bad_log to your custom directory?

### 18...@gmail.com (2023-10-03)

and plz put found_18f.pem server.py in same folder, so API deprecated. So python 3.8 is important.

### 18...@gmail.com (2023-10-03)

and plz put found_18f.pem server.py in same folder, some API has been deprecated, so python 3.8 is important.

### aj...@google.com (2023-10-03)

python 3.8 is fairly old and no longer available with an installer for security updates - can you try to reproduce the issue with an up to date python?

### 18...@gmail.com (2023-10-03)

Python 3.11.1 is ok.

### aj...@google.com (2023-10-04)

+dcheng as this rhymes with https://crbug.com/chromium/1421404

assigning to rakina to take a look - I'm not able to reproduce this issue and don't know enough about navigation to determine if the report is reasonable or not.

Tentatively assigning High severity (difficult to reproduce crash in the browser) and FoundIn-116.

### [Deleted User] (2023-10-04)

[Empty comment from Monorail migration]

### nt...@chromium.org (2023-10-04)

[Empty comment from Monorail migration]

### ra...@chromium.org (2023-10-05)

Thanks, finally managed to take a deeper look at this with leimy@ today. The test indeed showed that we can get into a situation in the middle of RenderFrameHostManager::GetFrameHostForNavigation() that led to the deletion of the NavigationRequest we're passing in there, and then we try to access the deleted NavigationRequest, causing a use-after-free.

The steps required are:
1. Make a NavigationRequest that already reached a stage where render_frame_host_ is already set to a speculative RenderFrameHost. In the test, it's an about:blank navigation that already reached the "WillCommitWithoutUrlLoader" step, which had already set the render_frame_host_ from "SelectFrameHostForCrossDocumentNavigationWithNoUrlLoader()"
2. Make the NavigationRequest try to commit an error page instead, by canceling it through a NavigationThrottle::WillCommitWithoutUrlLoader() 
3. When picking the RFH for the error page by calling GetFrameHostForNavigation(), the previously created speculative RenderFrameHost, which is no longer suitable for the navigation, will be deleted, so that a new speculative RenderFrameHost can be created for the error page.
4. The speculative RFH's destructor sees that there is a navigation whose GetRenderFrameHost() is itself. Thinking that the NavigationRequest needs to be destroyed with it, it triggers the deletion of that navigation.
5. When we get back to the GetFrameHostForNavigation() call, we still have a pointer to the request that is already deleted and tries using it.

The code that deletes the NavigationRequest from the RFH destructor was added in crrev.com/c/4737853 which got into version 117.0.5926.2, so let me update the label. To immediately address the UAF, we can just remove the part where we delete the NavigationRequest, and also set the NavigationRequest's render_frame_host_ to absl::nullopt within OnRequestFailedInternal (most callers already do this before calling the function, but the one in OnWillCommitWithoutUrlLoaderChecksComplete() didn't. If we didn't UAF that case will lead to a failed CHECK within OnRequestFailedInternal.

Outside of the fix above, leimy@ and I talked about how the render_frame_host_ seemingly had an invariant that once it's set from OnResponseStarted etc, it will never changed. However, that's not true when the navigation ends up committing an error page instead due to it getting cancelled by throttles (specifically from WillCommitWithoutUrlLoader or WillProcessResponse throttles). We should either make it clear that that's possible, or even better, make it so that it's actually true (i.e. only set render_frame_host_ when we are 100% sure we will commit in that RenderFrameHost). Mingyu agreed to write a doc so that we can discuss it with other navigation folks.

On whether this can happen in real life: I think only cancellations triggered from WillCommitWithoutUrlLoader() can lead to the bug here, and it seems like only DocumentPictureInPictureNavigationThrottle::WillCommitWithoutUrlLoader() -> ClosePiPWindowAndCancelNavigation() has the code that can lead to the cancellation right now. So I guess it is possible for this to happen IRL, but only when navigating to about:blank while in picture-in-picture mode. Not sure how easy it is to get to that situation, maybe steimel@ can comment.

@reporter: let us know if NavigationURLLoaderImpl::OnComplete() can somehow lead us to the UAF also. I'm not entirely sure when that function can be called, actually. Is it possible to get there after we set the RFH from OnResponseStarted etc?

### [Deleted User] (2023-10-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-10-05)

Any navigation within a document picture-in-picture window causes the pip window to close, and so the point of the DocumentPictureInPictureNavigationThrottle is to cancel those navigations and force the window to close. You could start a navigation to about:blank in the pip window using `window.location`, but it would be canceled and the window closed. Whether or not that would be an issue with this UAF is beyond my comprehension :)

### ra...@chromium.org (2023-10-06)

Thanks! Actually, I looked at the CANCEL_AND_IGNORE throttles again today, and it looks like none of them can actually lead to GetFrameHostForNavigation, because there is a MaybeCancelFailedNavigation() check [1]  that will cause the NavigationRequest to get cancelled and deleted instead of committing an error page.

Both DocumentPictureInPictureNavigationThrottle [2] and SubframeHistoryNavigationThrottle [3] can cancel the navigation with CANCEL_AND_IGNORE, and the default net_error_code for that is ABORTED [4] and will be caught by this check [5] in MaybeCancelFailedNavigation() and return early and not call GetFrameHostForNavigation, avoiding the use-after-free case mentioned in https://crbug.com/chromium/1487944#c20.

So luckily the UAF isn't possible to happen outside of test code that explicitly tries to cause the throttle to commit an error page now e.g.  by explicitly setting the net error code to ERR_BLOCKED_BY_RESPONSE when cancelling through the throttle, like in the reporter's test. 

For the NavigationURLLoaderImpl::OnComplete() caller in https://crbug.com/chromium/1487944#c0, I also think that can't cause the UAF, since it will call NavigationRequest::OnRequestFailed() [6] that says it is "Called if the request fails before receving a response.", which means there's no way for us to call that after OnResponseStarted (where we set the RFH). So we won't hit the accidental deletion like mentioned in https://crbug.com/chromium/1487944#c20.

@reporter: Please let us know if there is actually to repro this outside of tests!

[1]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4635;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
[2]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/picture_in_picture/document_picture_in_picture_navigation_throttle.cc;l=62;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
[3]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/subframe_history_navigation_throttle.cc;l=43;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
[4]: https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/navigation_throttle.cc;l=20;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
[5]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=9051;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
[6]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4514;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771

### 18...@gmail.com (2023-10-06)

Hey, rakina@chromium.org, I just finish my holiday now. And I am little tired... I will start inverstigate it tomorrow... So I can't give u full answer which u ask... Sorry for this part. 

Here is my previously inverstigate result.

> Both DocumentPictureInPictureNavigationThrottle [2] and SubframeHistoryNavigationThrottle [3] can cancel the navigation with CANCEL_AND_IGNORE, and the default net_error_code for that is ABORTED [4] and will be caught by this check [5] in MaybeCancelFailedNavigation() and return early and not call GetFrameHostForNavigation, avoiding the use-after-free case mentioned in https://crbug.com/chromium/1487944#c20.

I fully agree with u we can't trigger the `|bug|` by call from `|NavigationRequest::CancelDeferredNavigationInternal|`, however, in my personal views, your analysis  is not the root reason why it can't trigger from it.

In order to trigger this vulnerability, we need to meet the following conditions.

1. When we call `|CancelDeferredNavigation|`, the `|net_error_|` should be not `|net::ERR_ABORTED|`. because we need to pass the `|MaybeCancelFailedNavigation|` check, That's why I say [ SupervisedUserNavigationThrottle::OnInterstitialResult](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_navigation_throttle.cc;l=198) is intersting.
2. To trigger the bug, Our old_state must be `|WILL_REDIRECT_REQUEST or  WILL_START_REQUEST|`.

To understand this, see the code in `|NavigationRequest::OnWillProcessResponseChecksComplete|`. it also set `|render_frame_host|` be `null` when it call `| OnRequestFailedInternal|`.

```
    render_frame_host_ = absl::nullopt;
    [...]
    OnRequestFailedInternal(
        network::URLLoaderCompletionStatus(result.net_error_code()),
        true /* skip_throttles */, result.error_page_content(),
        false /* collapse_frame */);
```

However, assume we hit the `|NavigationRequest::CancelDeferredNavigationInternal|` with `|WILL_REDIRECT_REQUEST or WILL_START_REQUEST|` state. We will found this `|NavigationRequest|` object's `|render_frame_host_|` will always be `|null|`, So it can't pass this check:

```
      } else if (navigation_request->state() >=
                     NavigationRequest::WILL_PROCESS_RESPONSE &&
                 navigation_request->GetRenderFrameHost() == this) {  //  [+] This will return null: navigation_request->GetRenderFrameHost()
        frame_tree_node_->ResetNavigationRequest( //  [+] @b
            NavigationDiscardReason::kRenderFrameHostDestruction);
        [...]
      }
```

I found when chromium set `|render_frame_host_|`, it just happen when the state already be `|WILL_COMMIT_WITHOUT_URL_LOADER|` or `|WILL_PROCESS_RESPONSE|`, `|WILL_FAIL_REQUEST|`.

1. https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=2624;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
2. https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4256;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
3. https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4730;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771

Sadly, there are function named `|CheckStateTransition|`, that's means we can translate the state from `|WILL_REDIRECT_REQUEST|` to the above three state, but We can't translate from the previous 3 state to `|WILL_REDIRECT_REQUEST|`. So when we hit `|NavigationRequest::CancelDeferredNavigationInternal|` with `|WILL_REDIRECT_REQUEST|` state, the `|render_frame_host_|` will always be null. 

In my personal views, It's the real root reason why we can't trigger the bug from `|NavigationRequest::CancelDeferredNavigationInternal|`.

Here are intersting code at [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=1531;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771):

```
  navigation_request->render_frame_host_ = render_frame_host->GetSafeRef(); //  [+] set
  navigation_request->StartNavigation();  //  [+] set to `|WILL_START_REQUEST|`

  return navigation_request;
```

However, I think this `|navigation_request|` more like a cache `|navigation_request|`, It won't commit. So it can't change the state from `|WILL_START_REQUEST|` to `|WILL_REDIRECT_REQUEST|`.

### 18...@gmail.com (2023-10-06)

> @reporter: let us know if NavigationURLLoaderImpl::OnComplete() can somehow lead us to the UAF also. I'm not entirely sure when that function can be called, actually. Is it possible to get there after we set the RFH from OnResponseStarted etc?

Again, I am a little confused with this part too... When I start my holiday, my original plan is when I finish my holiday, I will inverstaige it...

I tried search chromium code base. Sadly, I don't found `|OnResponseStarted|` function which u mentioned... So I don't know about this part.

But `|NavigationURLLoaderImpl::OnComplete|` surely could lead us to the UAF...

```
void NavigationRequest::OnRequestFailed(
    const network::URLLoaderCompletionStatus& status) {
  DCHECK_NE(status.error_code, net::OK);

  OnRequestFailedInternal(
      status, false /* skip_throttles */,
      absl::nullopt /* error_page_content */,
      status.should_collapse_initiator /* collapse_frame */);
}
```

because it will finnaly called `|OnRequestFailedInternal|` without reset `|render_frame_host_|`.

I don't know what happened in `|OnResponseStarted|` because I can't find this function, So I can't comment about it.

However, Like the above analysis, I think there are a way to trigger the bug.

1. If our state is `|WILL_COMMIT_WITHOUT_URL_LOADER|` or `|WILL_PROCESS_RESPONSE|`, `|WILL_FAIL_REQUEST|`. It means the `|render_frame_host_|` is not `nullptr`
2. Then we call `|NavigationURLLoaderImpl::OnComplete -> NavigationRequest::OnRequestFailed -> ...|`

Maybe we have change to trigger this bug.

So the only question is :

> If our state is  `|WILL_COMMIT_WITHOUT_URL_LOADER|` or `|WILL_PROCESS_RESPONSE|`, `|WILL_FAIL_REQUEST|`, in the future logical, could we call `|NavigationURLLoaderImpl::OnComplete|` function?

In my personal views, In the normal logical, This should be hard(I'm not sure this 100%). However, assume we have remote-code-excute ability in the render process. maybe we could call `|NavigationURLLoaderImpl::OnComplete|`(Just call it from mojo....) after the above three state.

I am not a navigation expert, So If anything I am wrong, welcome to figure it. Thx!

### 18...@gmail.com (2023-10-06)

> @reporter: let us know if NavigationURLLoaderImpl::OnComplete() can somehow lead us to the UAF also. I'm not entirely sure when that function can be called, actually. Is it possible to get there after we set the RFH from OnResponseStarted etc?

Again, I am a little confused with this part too... When I start my holiday, my original plan is when I finish my holiday, I will inverstaige it...

I tried search chromium code base. Sadly, I don't found `|OnResponseStarted|` function which u mentioned... So I don't know about this part.

But `|NavigationURLLoaderImpl::OnComplete|` surely could lead us to the UAF...

```
void NavigationRequest::OnRequestFailed(
    const network::URLLoaderCompletionStatus& status) {
  DCHECK_NE(status.error_code, net::OK);

  OnRequestFailedInternal(
      status, false /* skip_throttles */,
      absl::nullopt /* error_page_content */,
      status.should_collapse_initiator /* collapse_frame */);
}
```

because it will finnaly called `|OnRequestFailedInternal|` without reset `|render_frame_host_|`.

I don't know what happened in `|OnResponseStarted|` because I can't find this function, So I can't comment about it.

However, Like the above analysis, I think there are a way to trigger the bug.

1. If our state is `|WILL_COMMIT_WITHOUT_URL_LOADER|` or `|WILL_PROCESS_RESPONSE|`, `|WILL_FAIL_REQUEST|`. It means the `|render_frame_host_|` is not `nullptr`
2. Then we call `|NavigationURLLoaderImpl::OnComplete -> NavigationRequest::OnRequestFailed -> ...|`

Maybe we have chance to trigger this bug.

So the only question is :

> If our state is  `|WILL_COMMIT_WITHOUT_URL_LOADER|` or `|WILL_PROCESS_RESPONSE|`, `|WILL_FAIL_REQUEST|`, in the future logical, could we call `|NavigationURLLoaderImpl::OnComplete|` function?

In my personal views, In the normal logical, This should be hard(I'm not sure this 100%). However, assume we have remote-code-excute ability in the render process. maybe we could call `|NavigationURLLoaderImpl::OnComplete|`(Just call it from mojo....) after the above three state.

I am not a navigation expert, So If anything I am wrong, welcome to figure it. Thx!

### ra...@chromium.org (2023-10-06)

Thanks! 
Re https://crbug.com/chromium/1487944#c24: Yeah I don't think it's possible to move back the NavigationState to WILL_REDIRECT_REQUEST, thus I think the window where the RFH -> NavigationRequest deletion is when the state is >= WILL_PROCESS_RESPONSE.

Re https://crbug.com/chromium/1487944#c26: That's a good point, I asked around and dcheng@ mentioned that the loader might be untrustworthy (e.g. if it's controlled by a Service Worker), so it's possible to get a malicious NavigationURLLoaderImpl::OnComplete() at arbitrary timing. However, I think we might be saved by this invariant [1] from this comment that says "At least one of |loader_| or |render_frame_host_| is null/absl::nullopt".

Looking at NavigationRequest::OnResponseStarted() [2] and OnRequestFailedInternal() [3] it looks like this invariant holds because we always reset the loader at the start, before assigning value to render_frame_host_ (and for navigations that don't need a URL loader to commit, we never set the loader in the first place).  This means that it should be impossible to trigger NavigationURLLoaderImpl::OnComplete() if the render_frame_host_ is already set (I think). But please let us know if there is a way to somehow bypass that, as that would be good to fix as well.


[1]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.h;l=2009;drc=0c8ffbe78dc0ef2047849e45cefb3f621043e956
[2]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=3977;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771
[3]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4615;drc=f5bdc89c7395ed24f1b8d196a3bdd6232d5bf771

### 18...@gmail.com (2023-10-06)

Thanks! 

Re https://crbug.com/chromium/1487944#c27: That's a good point too, I never focus on this `|invariant|` before. I will start inverstigate it tomorrow, and report back.

By the way:

>  This means that it should be impossible to trigger NavigationURLLoaderImpl::OnComplete() if the render_frame_host_ is already set (I think). But please let us know if there is a way to somehow bypass that, as that would be good to fix as well.

In my personal views, If the finial result is that I can't trigger the bug in the real chrome, I still think it deserve to be fix the code. With my initial sample test, at least it been proved the logical at here have risk to lead to UAF. And with this `|comment|:`

``` c++
        // As we are unable to come up with a case that will lead to this path,
        // we instead record the dumps for debugging the scenario.
        // TODO(crbug.com/1430653): if we verify that this path is impossible,
        // replace the `DumpWithoutCrashing` with a `CHECK`. Otherwise, add a
        // new browser test for it.
        base::debug::DumpWithoutCrashing();
        NOTREACHED();
```

chromium team haven't decide whether we can't hit the path or not, this path could lead to high-sec bug. So I think it deserve to be fix it.

Anyway, when I finish my all work, I will report back. Thank!

### 18...@gmail.com (2023-10-07)

Hey,  rakina@chromium.org. Now I fully agree with u.

>  Looking at NavigationRequest::OnResponseStarted() [2] and OnRequestFailedInternal() [3] it looks like this invariant holds because we always reset the loader at the start, before assigning value to render_frame_host_ (and for navigations that don't need a URL loader to commit, we never set the loader in the first place).  This means that it should be impossible to trigger NavigationURLLoaderImpl::OnComplete() if the render_frame_host_ is already set (I think). But please let us know if there is a way to somehow bypass that, as that would be good to fix as well.

When `|render_frame_host_|` has been set, `|loader|` will be reset too. This prevent we won't trigger the bug. The only chance is we post 2 task. assume it in a chain. after loader_ been reset, we still run next task, and next task called `|OnRequestFailedInternal|` . But it is too complicated and beyond my area.

So feel free to close this issue, and mark it as `|wontfix|`. Thx!

### ra...@chromium.org (2023-10-09)

Sorry, I didn't mean to make it like I want to close this bug, I just want to try figure out a direct repro here. Even if it's not actually possible to hit the UAF in production code, it's still quite close to being an actual security bug due to the misunderstanding of the liftemes of the RFH. So this is still a good report, and we will land some fixes related to this. Thanks a lot for reporting!

### 18...@gmail.com (2023-10-09)

re https://crbug.com/chromium/1487944#c30: Thx! But it still means even if we land some fixes related to this,  I still can't get bounty about this? 

### am...@chromium.org (2023-10-10)

Since this issue does not impact shipped / production versions of Chrome, updating this issue to Security_Impact-None.

The SLO should get automatically adjusted by sheriffbot to no longer being Pri-1. 

WRT https://crbug.com/chromium/1487944#c31, OP -- thank you for the report. Each fixed/closed issue of an external security bug goes to the VRP panel for evaluation once it is closed. 
It is important to note, however, that issues that do not impact production Chrome, and therefore users, are not generally eligible for VRP reward. This report will still undergo evaluation once the issue has been resolved and the report closed, and the VRP Panel decision will be made available here once that occurs. 

### 18...@gmail.com (2023-10-11)

thx for your reply

### gi...@appspot.gserviceaccount.com (2023-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/12bd4771e37b6effcf73f35a06bed080a620779a

commit 12bd4771e37b6effcf73f35a06bed080a620779a
Author: Mingyu Lei <leimy@chromium.org>
Date: Thu Oct 12 11:12:34 2023

Always reset RFH before `NavigationRequest::OnRequestFailedInternal()`

When a NavigationRequest fails, the `render_frame_host_` member in the
NavigationRequest might have been chosen previously. If the
NavigationRequest is needed for an error page commit, a new value of
`render_frame_host_` will be recomputed, which will delete the
previously picked speculative RFH.

In some cases, the `render_frame_host_` member in the
NavigationRequest is not reset before `OnRequestFailedInternal()`,
and it will cause the destruction of the NavigationRequest when the
RFH is destroyed. Since the NavigationRequest is used for the error
page commit, there will be a potential UaF case.

This CL ensures the `render_frame_host_` is always set to null before
`OnRequestFailedInternal()`, it also removes one of the
NavigationRequest reset logic (which we believe should not happen) from
the RFH's destructor. A browser test is added for the situation
mentioned above.

Bug: 1487944
Change-Id: I295dc4fbb95e82bcc494b0b872d4648341aa6177
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4924175
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Mingyu Lei <leimy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1208754}

[modify] https://crrev.com/12bd4771e37b6effcf73f35a06bed080a620779a/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/12bd4771e37b6effcf73f35a06bed080a620779a/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/12bd4771e37b6effcf73f35a06bed080a620779a/content/browser/renderer_host/navigation_request_browsertest.cc


### 18...@gmail.com (2023-10-12)

I undelete all my delete comment(becuase I can't find a native way to trigger it, I think it is ugly :( , So I delete it before.) but for the patch, I decide undelete it, once someday similar problem occurs, it maybe offer a little help...

### ra...@chromium.org (2023-10-13)

Thanks all, I think crrev.com/c/4924175 made it so that this potential UAF won't be possible to be hit in production code, so let me mark this bug as fixed (which will trigger the process mentioned in https://crbug.com/chromium/1487944#c32). leimy@ will still look into improving the current documentation and safeguards on RFH use as mentioned in https://crbug.com/chromium/1487944#c20.

### 18...@gmail.com (2023-10-13)

re https://crbug.com/chromium/1487944#c36, hey, sorry for bother u, would u mind allow me to access the document too. navigation is too intersting and complicated. So I am so intersted about this document.

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-18)

Thank you for the report and your efforts to help us identify if this issue can be triggered in production Chrome. Due to these efforts, we (the Chrome VRP) did want to extend to you a small thank you reward of $1,000. Thank you for your efforts in reporting this issue to us as well as the efforts toward determining if this impacted production code in any way!

### 18...@gmail.com (2023-10-18)

Thx!

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-19)

This issue was migrated from crbug.com/chromium/1487944?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073755)*
