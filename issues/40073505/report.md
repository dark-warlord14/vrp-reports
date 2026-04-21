# Security:  heap-use-after-free on RenderFrameHostImpl::Init

| Field | Value |
|-------|-------|
| **Issue ID** | [40073505](https://issues.chromium.org/issues/40073505) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Apps>BrowserTag |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 18...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2023-09-27 |
| **Bounty** | $20,000.00 |

## Description

Hey, The bug found by occasionally when I inverstigate [another bug](https://bugs.chromium.org/p/chromium/issues/detail?id=1444360).

When I inverstigate above code, I found [RenderFrameHostManager::CommitPending](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=4702;drc=150d8c7e45daeef094be8ec8852e3486eed8f59d;bpv=1;bpt=1?q=CommitPending&ss=chromium%2Fchromium%2Fsrc) could delte the `|RenderFrameHostImpl|` object.

``` c++
void RenderFrameHostManager::CommitPending(
    std::unique_ptr<RenderFrameHostImpl> pending_rfh,
    std::unique_ptr<StoredPage> pending_stored_page,
    bool clear_proxies_on_commit) {
  [...]
  old_render_frame_host = SetRenderFrameHost(std::move(pending_rfh));
  [...]
  UnloadOldFrame(std::move(old_render_frame_host)); //  [+] here
  [...]
}

```

And see this code:

``` c++
void RenderFrameHostImpl::Init() {
  [...]
  if (pending_navigate_) {  //  [+] @c
    [...]
    frame_tree_node()->navigator().OnBeginNavigation(   //  [+] @a
        frame_tree_node(), std::move(pending_navigate_->common_params),
        std::move(pending_navigate_->begin_navigation_params),
        std::move(pending_navigate_->blob_url_loader_factory),
        std::move(pending_navigate_->navigation_client),
        EnsurePrefetchedSignedExchangeCache(), initiator_process_id,
        std::move(pending_navigate_->renderer_cancellation_listener));
    pending_navigate_.reset();  //  [+] @b
  }
}
```

`|OnBeginNavigation|` will finnaly call `|CommitPending|` function, and reuse this pointer at `@b` which will trigger the uaf bug.

Here is the call path(u could see the deails in the asan.txt file):

```
OnBeginNavigation -> TakeNavigationRequest -> GetFrameHostForNavigation -> CommitPending -> UnloadOldFrame
```

And we need to pass the `|pending_navigate_(@c)|` check,  which only enable in android platform. In [this document](https://chromium.googlesource.com/chromium/src/+/main/docs/android_build_instructions.md#installing-and-running-chromium-on-a-device), to make a pure html trigger the code pass need a `|android device|`, but I only have windows machine(shame of this part :( ). So I use this way which introduced in [this bug https://crbug.com/chromium/1487110#c9](https://bugs.chromium.org/p/chromium/issues/detail?id=1444360#c9).

And some tips about this poc code:

``` c++
  //    [+] make the process died
  {
    // Trigger a renderer kill by calling DoSomething() which will cause a bad
    // message to be reported.
    RenderProcessHostBadIpcMessageWaiter kill_waiter(main_process);
    mojo::Remote<mojom::TestService> service;
    main_process->BindReceiver(service.BindNewPipeAndPassReceiver());
    service->DoSomething(base::DoNothing());
    EXPECT_EQ(bad_message::RPH_MOJO_PROCESS_ERROR, kill_waiter.Wait());
  }
```

I use this code to make the render prcoeess died, leecroso use `|max length mismatch|` in his original poc:

```
void RenderFrameHostImpl::UpdateTitle(
  [...]
  if (received_title.length() > blink::mojom::kMaxTitleChars) {
    mojo::ReportBadMessage("Renderer sent too many characters in title.");    <-------- [4]
    return;
  }
  [...]
}
```

But I think `|OOM|` should trigger render process died too. So there don't need a render bug. It still should be marked as `|critical|`.

##   reproduce

git version:

```
PS D:\gad_bless\src> git log
commit fba53700a512a2c2bb6a4dbc9539dcc83dee433e (grafted, HEAD, origin/main)
Author: Minoru Chikamune <chikamune@chromium.org>
Date:   Wed Aug 30 10:58:12 2023 +0000

    Extend PageLoad.Clients.{SameOrigin,CrossOrigin}.* histograms' expire date

    Bug: 1474509
    Change-Id: I83efc47a1a7eb07c0684f2e83d2b83e68db2aeb5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4821967
    Reviewed-by: Yoshisato Yanagisawa <yyanagisawa@chromium.org>
    Reviewed-by: Shunya Shishido <sisidovski@chromium.org>
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
    Commit-Queue: Minoru Chikamune <chikamune@chromium.org>
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1190036}
```

Add the patch.cpp code to `|content\browser\renderer_host\render_process_host_browsertest.cc|`. compile with asan version.

and run this command , it should generate the asan log:

```
.\out\asan\content_browsertests.exe --gtest_filter=All/RenderProcessHostTest.CausedRenderFrameHostImplInitCrashBy18f/Default
```

##  bitsec

This [patch](https://codereview.chromium.org/2472253002) introduce this code. But in this old version, it should not call `|UnloadOldFrame|`, it should call `|SwapOutOldFrame(std::move(old_render_frame_host))|` to free this object.

##  patch

patch should be simple, we could move the `|reset before OnBeginNavigation|`, because it won't change the result.

```
void RenderFrameHostImpl::Init() {
  [...]
  if (pending_navigate_) {  //  [+] @c
    [...]
    pending_navigate_.reset();  //  [+] @b
    frame_tree_node()->navigator().OnBeginNavigation(   //  [+] @a
        frame_tree_node(), std::move(pending_navigate_->common_params),
        std::move(pending_navigate_->begin_navigation_params),
        std::move(pending_navigate_->blob_url_loader_factory),
        std::move(pending_navigate_->navigation_client),
        EnsurePrefetchedSignedExchangeCache(), initiator_process_id,
        std::move(pending_navigate_->renderer_cancellation_listener));
    //  [+] Do not add code after  this, `|OnBeginNavigation|` maybe delete this
  }
}
```

## Attachments

- [patch.cpp](attachments/patch.cpp) (text/plain, 2.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 24.0 KB)

## Timeline

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-27)

Alex, would you be kind enough to take a look here?

My understanding is that this report is saying that a UaF can occur under certain timing conditions when the renderer process happens to die. (I agree with the reporter that we should expect renderers to die at any moment in an attacker-controlled fashion). But I don't understand enough about the browser-side navigation code to know if it's real.

The commit from the git log above shipped in M118 but this code hasn't changed recently, so I'm setting a FoundIn to assume this goes back to Extended Stable or beyond.

I can't get the POC to work. Even on the specific git version above, I see these errors from the POC:

===
[3368072:3368072:0927/095236.277300:WARNING:bluez_dbus_manager.cc(247)] Floss manager not present, cannot set Floss enable/disable.
[3368112:3368112:0927/095236.918257:WARNING:sandbox_linux.cc(393)] InitializeSandbox() called with multiple threads in process gpu-process.
[3368112:3368112:0927/095236.944624:WARNING:gpu_memory_buffer_support_x11.cc(49)] dri3 extension not supported.
../../content/browser/renderer_host/render_process_host_browsertest.cc:2712: Failure
Value of: NavigateToURL(shell(), url)
  Actual: false
Expected: true
Stack trace:
#0 0x55a68034e034 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xa9d8033)
#1 0x55a684ed60c7 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xf5600c6)
#2 0x55a684edf22b (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xf56922a)
#3 0x7f524464a084 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x524a083)
#4 0x7f5244653d6e (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x5253d6d)
#5 0x7f524463e2d0 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x523e2cf)
#6 0x7f524854ee5f (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x914ee5e)
#7 0x7f5248554993 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x9154992)
#8 0x7f5248553c55 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x9153c54)
#9 0x7f524854b0a5 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x914b0a4)
#10 0x7f524854b442 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x914b441)
#11 0x55a684ed33af (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xf55d3ae)

[3368072:3368072:0927/095237.866047:INFO:CONSOLE(1)] "Uncaught ReferenceError: clickLinkToSelf is not defined", source: __const_std::string&_script__ (1)
../../content/browser/renderer_host/render_process_host_browsertest.cc:2718: Failure
Value of: ExecJs(shell(), "clickLinkToSelf();")
  Actual: false (a JavaScript error: "ReferenceError: clickLinkToSelf is not defined
    at __const_std::string&_script__:1:2):
        {clickLinkToSelf();
         ^^^^^
)
Expected: true
Stack trace:
#0 0x55a68034e3b6 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xa9d83b5)
#1 0x55a684ed60c7 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xf5600c6)
#2 0x55a684edf22b (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xf56922a)
#3 0x7f524464a084 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x524a083)
#4 0x7f5244653d6e (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x5253d6d)
#5 0x7f524463e2d0 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x523e2cf)
#6 0x7f524854ee5f (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x914ee5e)
#7 0x7f5248554993 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x9154992)
#8 0x7f5248553c55 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x9153c54)
#9 0x7f524854b0a5 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x914b0a4)
#10 0x7f524854b442 (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/libcontent.so+0x914b441)
#11 0x55a684ed33af (/usr/local/google/home/adetaylor/chromium/src/out/ASAN/content_browsertests+0xf55d3ae)


==
and then I get a timeout rather than a UaF. So I can't at all confirm that this is real. But even if I could have got the POC to work, I'd have needed some CSA advice on whether this is a realistic scenario so sending your way to shortcut further messing around.

Provisionally setting severity as if this is a UaF in the browser process which can be triggered by a compromised renderer. Perhaps even an uncompromised renderer could fiddle with timing enough to achieve this, in which case it would be Critical subject to any other mitigating factors, but this seems unlikely since we don't have a known way to trigger this except actual C++. But please do consider the correct severity if you do deem this a real bug.

Setting OS to Android only per the comments about the check at @c.

[Monorail components: Internals>Sandbox>SiteIsolation]

### ad...@google.com (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### 18...@gmail.com (2023-09-27)

plz update the code to your custom path, sorry for forgot this.

``` c++
GURL url("file:///D:/gad_bless/src/content/test/data/simple_links.html");
```

### ad...@google.com (2023-09-27)

Ah of course, yes, thanks.

### [Deleted User] (2023-09-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2023-09-27)

Thanks for the report! This does seem like a valid issue.  OnBeginNavigation will call GetFrameHostForNavigation to pick a target RenderFrameHost for the navigation, and assuming it picks a new RFH, it's possible for that RFH to be swapped in immediately, without waiting for the navigation to commit (notice PerformEarlyRenderFrameHostSwapIfNeeded on the asan free stack).  That early swap calls CommitPending, which eventually calls Unload() on the old RFH, which may indeed legitimately delete that RFH [1].  And all this can happen synchronously starting from OnBeginNavigation, so the pending_navigation_ deref after that call is definitely bad.

Navigating out of a crashed RFH will always follow this early swap path, as we always force a new RFH to be created in this case.  We also do the early swap in some corner cases where we can't reuse an initial RFH for the navigation - see https://crbug.com/chromium/1485586 for the known ones (I've actually been working on removing them).  Fortunately, I don't think any of them apply here: web pages can't navigate to WebUI, hosted apps/extensions/<webview> tags aren't relevant on Android, and dynamic isolation wouldn't do a BrowsingInstance swap because there are two windows in the BrowsingInstance [2].  So a crash/OOM may indeed be required for this, and you'd need to time it to occur after the new window is created, but before the navigation is resumed.

I'll dig more into when and where pending_navigate_ is used.  I do also recall it was an Android (AW?) thing but don't remember any of the context.  +boliu@ who worked on r566315, which was somewhat related, and might help with the background of this.

Thanks also for providing a sample test; the key part seems to be set_delay_popup_contents_delegate_for_testing() on the Shell, which turns on the delayed navigation behavior.  The fix should indeed be simple (we shouldn't reset pending_navigate_ before OnBeginNavigation as we are actually using stuff from it in that call, but we could move it to a local copy, check a WeakPtr and return early, etc).

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=5149;drc=e7ba521f1e9fe2e384e270f1e579a6438463e463

[2] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=126;drc=72ede6393a8091c892108eee4b60bb69aa5d30c6

### 18...@gmail.com (2023-09-28)

Hey, If I don't misunderstanding this. If I call `|PendingDeletionCheckCompletedOnSubtree|`, I won't  need crash the render process. If it is, I think the bug should be marked `|sec-critical|`. see the bug |https://bugs.chromium.org/p/chromium/issues/detail?id=1417122|.

I have some question about this.

1. first , could I have bug bounty and cve assign for this, if it is , plz credit as @18楼梦想改造家. Thx.
2. second, about u say the fix, I know chrome always use two way to fix these bug. one move code like I describe, another way try to use `|Weak_Self(weak_ptr)|` to prevent it. However , If I don't misunderstand anything, we use `|WeakSelf|` when the code is complicated, but here is so simple, So I just use this way.
3. About the `|pending_navigate_|` , I believe this should be related to `|android|` platform, because it introduced when chrome try to solve a `|android|`  bug(you could see the blame history).
4. Finnaly, Could I debug chromium android version without `|android device|`?

Thx!

### 18...@gmail.com (2023-09-28)

Even if it need crash render process... Maybe it should be marked as sec-critical. like 1444360 describe....

### bo...@chromium.org (2023-09-28)

Delaying navigation for popup is probably for AW. With AW, If the popup is allowed, then we need to give the embedding app a chance to create a new WebView and insert all the necessary throttles and callbacks and whatnot, which happens asynchronously. While that's pending, we have to hold off the navigation in the popup.

> 4. Finnaly, Could I debug chromium android version without `|android device|`?

You can try an emulator which should be good enough for this kind of testing

### al...@chromium.org (2023-09-29)

A few updates.  I've looked more closely at pending_navigate_ plumbing.  For it to be set, we need to start a renderer-initiated navigation (via RFHI::BeginNavigation) while RFHI::waiting_for_init_ is true, which happens for all new popup main frame RFHs created on the window.open path (via CreateNewWindow), as long as we aren't suppressing the opener and swapping to a new BrowsingInstance (see WebContents::CreateParams::renderer_initiated_creation).  Shortly after CreateNewWindow(), ShowCreatedWindow() checks WebContentsDelegate::ShouldResumeRequestsForCreatedWindow(), and if that is true (default implementation is true), it calls ResumeLoadingCreatedWebContents() which eventually resets waiting_for_init_ to false.  So for this bug to be possible, ResumeLoadingCreatedWebContents() needs to return false, and then we need to get a new navigation via RFHI::BeginNavigation(), which would populate pending_navigate_.  (Usually, the renderer calling window.open(url) will already trigger these in the right order: CreateNewWindow, then ShowCreatedWindow, then BeginNavigation for the provided url.)

ResumeLoadingCreatedWebContents() returns false in three cases: Android Webview [1]  (always false), Chrome on Android [2] (forwards the call to Java [3], which returns false if new tabs are created asynchronously, if they need new activities - I'm not really sure when that happens, maybe boliu@ knows?), and, most interestingly, guest views [4].  The latter means that this is not just Android, since guest views are a desktop-only thing.  I've confirmed that this repros on Linux by modifying one of the <webview> window.open tests, which works as follows: (1) have the <webview> tag call window.open which the embedder intercepts, (2) have the embedder create a new <webview> tag while processing the newwindow event but delay calling event.window.attach() on it, (3) wait for the <webview> process to send its window.open BeginNavigation IPC which gets deferred via pending_navigate_, (4) crash the <webview> tag process, (5) have the embedder call event.window.attach() now.  Note that this does require the guestview's embedder to register and respond to newwindow events, which limits the scope somewhat - e.g., I doubt any of our WebUIs that embed <webview> tags support newwindow (though I don't know for sure), and similarly, I don't think non-<webview>-tag guestview cases (like PDF) do either. So this might be just Chrome apps that have <webview> tags and handle newwindow events, and those are deprecated everywhere except ChromeOS.  For now, though, let me add all desktop platforms out of an abundance of caution, and I'll also add the guestview component so the owners there can comment further on the scope.

After playing with that repro, I do believe that a renderer crash is necessary to trigger this, in all these cases.  This is because for this path, window.open() will not create an unused initial RFH with an unassigned SiteInstance and unused process, but rather it will keep the new RFH in the old SiteInstance to start with, and also the initial RFH is live (as it's created in the renderer calling window.open).  In this state, the early commit optimization cannot apply to the initial RFH, even if a new RFH is needed for the navigation.  So the crashed case is the only one that can lead to swapping RFHs and synchronously destroying the old RFH after calling OnBeginNavigation.

Also, quick note about the provided test (thanks for including it in the report!).  I can confirm that I got a modified version of it working locally.  Note, however, that it's hitting a couple of DCHECKs first [5] in RenderWidgetHostImpl::Init() (called just before resuming the pending_navigate_ navigation).  Commenting those out, though, I do get the UAF reported by asan.  If these DCHECKs were CHECKs, they would crash the browser process before we got to the UAF, but alas that's not the case yet.

[1] https://source.chromium.org/chromium/chromium/src/+/main:android_webview/browser/aw_web_contents_delegate.cc;l=255;drc=77806a4cacd6357ff9b2fcb63ad8f53f62453d6d

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/android/tab_web_contents_delegate_android.cc;l=342;drc=77806a4cacd6357ff9b2fcb63ad8f53f62453d6d

[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/app/tab_activity_glue/ActivityTabWebContentsDelegateAndroid.java;l=162;drc=aa78b431380e08988cccde7e6e2a167568da64a9

[4] https://source.chromium.org/chromium/chromium/src/+/main:components/guest_view/browser/guest_view_base.cc;l=657;drc=77806a4cacd6357ff9b2fcb63ad8f53f62453d6d

[5] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_impl.cc;l=761-762;drc=77806a4cacd6357ff9b2fcb63ad8f53f62453d6d

[Monorail components: Platform>Apps>BrowserTag]

### 18...@gmail.com (2023-09-29)

> Also, quick note about the provided test (thanks for including it in the report!).  I can confirm that I got a modified version of it working locally.  Note, however, that it's hitting a couple of DCHECKs first [5] in RenderWidgetHostImpl::Init() (called just before resuming the pending_navigate_ navigation).  Commenting those out, though, I do get the UAF reported by asan.  If these DCHECKs were CHECKs, they would crash the browser process before we got to the UAF, but alas that's not the case yet.

Yes, for the code in the windows platform, seems it doesen't support in `|debug asan version|`, In release version, the dcheck won't work....

### bo...@chromium.org (2023-09-29)

> Chrome on Android [2] (forwards the call to Java [3], which returns false if new tabs are created asynchronously, if they need new activities - I'm not really sure when that happens, maybe boliu@ knows?)

This one I don't know. //chrome code is generally outside my area

### mc...@chromium.org (2023-09-29)

Regarding guest view, yeah, as far as I'm aware, the usage of ResumeLoadingCreatedWebContents is for webview's newwindow handling. The reason is similar to the AW case where the embedder needs a chance to register handlers before the first navigation. WebViewNewWindowTest.NewWindow_WebRequest demonstrates this.

> I doubt any of our WebUIs that embed <webview> tags support newwindow (though I don't know for sure)
The only ones I'm aware of discard the opened window and just use the target URL to open their own window. Here's an example [1]. But, yeah, I haven't audited them.

>  I don't think non-<webview>-tag guestview cases (like PDF) do either
For MimeHandlerView and ExtensionOptions, they use IsWebContentsCreationOverridden and CreateCustomWebContents. So I don't think we would reach this code. It would probably help to have the individual guest derived classes implement ShouldResumeRequestsForCreatedWindow, rather than doing it in the base class. I'm not sure about AppView.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/chromeos/add_supervision/add_supervision_ui.ts;drc=5a9d881327f7c556d3e3f7ea36c210d6e3af54c1;l=116

### al...@chromium.org (2023-10-02)

https://crbug.com/chromium/1487110#c15: thanks, looks like your https://chromium-review.googlesource.com/c/chromium/src/+/4906388 is confirming that only <webview> guests reach this code, not MimeHandlerView (pdf) or ExtensionView.

One other finding: after fixing the bug with pending_navigate_ cleanup, it turns out that allowing the navigation to proceed after a renderer crash doesn't really work - in particular, pending_navigate_ contains a remote NavigationClient endpoint, which of course has been disconnected as part of the crash.  If we just allow the navigation to proceed, the NavigationRequest will try to use that provided NavigationClient (see NavigationRequest::SetNavigationClient()), and the first thing this client will do is generate a disconnect event, OnNavigationClientDisconnected, which will cancel the navigation.  After a quick chat with CSA folks, I think it's simplest to just clear pending_navigate_ if there's a crash, similar to how we cancel other NavigationRequests owned by RFH in RenderFrameHostImpl::RenderProcessGone().

### al...@chromium.org (2023-10-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0763aad8eee441188871aec608a3e011827ce3ca

commit 0763aad8eee441188871aec608a3e011827ce3ca
Author: Kevin McNee <mcnee@chromium.org>
Date: Tue Oct 03 15:29:54 2023

Override ShouldResumeRequestsForCreatedWindow for webviews and not all guests

The guest view base class currently overrides
ShouldResumeRequestsForCreatedWindow to support the webview newwindow
event. This code path is not relevant to any other guest view type.
For ExtensionOptions and MimeHandlerView, the code is not reachable
due to the way new WebContents are created. For AppView, calling
window.open from an embedded app technically does create a guest
WebContents, but it's immediately destroyed due to AppViewGuest not
implementing AddNewContents. Using the default value for
ShouldResumeRequestsForCreatedWindow here does not seem to have
an observable difference to the app.

For clarity, we now just override the behaviour for webviews.

Bug: 1487110
Low-Coverage-Reason: OTHER Unreachable code cannot be covered.
Change-Id: I03babe749731c012375d4ad31a122584f2a8bfef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4906388
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1204672}

[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/extensions/browser/guest_view/extension_options/extension_options_guest.cc
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/extensions/browser/guest_view/web_view/web_view_guest.cc
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/extensions/browser/guest_view/mime_handler_view/mime_handler_view_guest.h
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/extensions/browser/guest_view/mime_handler_view/mime_handler_view_guest.cc
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/extensions/browser/guest_view/web_view/web_view_guest.h
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/components/guest_view/browser/guest_view_base.h
[modify] https://crrev.com/0763aad8eee441188871aec608a3e011827ce3ca/extensions/browser/guest_view/extension_options/extension_options_guest.h


### aj...@google.com (2023-10-03)

Hello - if commit in https://crbug.com/chromium/1487110#c18 fixes this issue could you mark it as Fixed

### al...@chromium.org (2023-10-03)

No, https://crbug.com/chromium/1487110#c18 doesn't fix this yet.  The fix will be in https://chromium-review.googlesource.com/c/chromium/src/+/4908270 which I'll land soon.

### 18...@gmail.com (2023-10-04)

> No, https://crbug.com/chromium/1487110#c18 doesn't fix this yet.  The fix will be in https://chromium-review.googlesource.com/c/chromium/src/+/4908270 which I'll land soon.

Hey, alexmos@chromium.org, once u fix it,  would u mind change it to Security_Severity-Critical? because it has similar primitive like https://crbug.com/chromium/1444360, which has been marked as Security_Severity-Critical. Thx!

### gi...@appspot.gserviceaccount.com (2023-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/093daae65d50511c2027d01f9188681749b5a1be

commit 093daae65d50511c2027d01f9188681749b5a1be
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Thu Oct 05 17:59:40 2023

Fix RFHI::pending_navigate_ cleanup after crashes and early RFH swaps.

When resuming a navigation that had been saved into
RenderFrameHostImpl::pending_navigate_, we need to account for the
fact that OnBeginNavigation() calls GetFrameHostForNavigation() which
may perform an early RenderFrameHost swap and synchronously destroy
the old RFH.

There's also no need to keep a pending_navigate_ around after the
corresponding renderer process crashes, so this CL also adds logic to
clear it.  Resuming such a navigation would require additional work,
since the NavigationClient stashed in pending_navigate_ is no longer
usable and would just immediately call the disconnect handler and
cancel the navigation.  But there isn't really any benefit to adding
that complexity, and we already cancel the RFH's other ongoing
navigations when its renderer process dies.

This CL also tweaks the logic in RenderWidgetHostImpl to allow the
resuming logic (ResumeLoadingCreatedWebContents) to work without
hitting DCHECKs, if it's called after a renderer process crash. This
case never worked cleanly before, but is supported now (and allows the
new test to work without crashing).

Bug: 1487110
Change-Id: Icd6a55002e52729e6ee966210efba1a5ce23eb55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908270
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1205927}

[modify] https://crrev.com/093daae65d50511c2027d01f9188681749b5a1be/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/093daae65d50511c2027d01f9188681749b5a1be/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/093daae65d50511c2027d01f9188681749b5a1be/content/browser/renderer_host/render_widget_host_impl.cc


### al...@chromium.org (2023-10-05)

This should be fixed by r1205927.  After some discussions with dcheng@ and cthomp@, I'm also changing severity to critical, since (1) an uncompromised renderer could potentially exploit this by triggering an OOM/crash just after a window.open() call (before the embedder has a chance to unblock navigations), where the OOM especially seems easy to do, and (2) this affects Android Webview where a standard user flow can load a page that does this, and while it also probably requires the embedder app to support new window events, this might be fairly common - so overall I'm conservatively assuming no strong mitigating factors.  And indeed, https://crbug.com/chromium/1444360 had similar prerequisites in terms of renderer triggering a crash/OOM.

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-06)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-06)

Requesting merge to extended stable M116 because latest trunk commit (1205927) appears to be after extended stable branch point (1160321).

Requesting merge to other stable M117 because latest trunk commit (1205927) appears to be after other stable branch point (1181205).

Requesting merge to stable M118 because latest trunk commit (1205927) appears to be after stable branch point (1192594).

Requesting merge to dev M119 because latest trunk commit (1205927) appears to be after dev branch point (1204232).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to stable.

Merge review required: M118 has already been cut for stable release.

Merge review required: M119 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117, 118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-07)

Requesting merge to extended stable M116 because latest trunk commit (1205927) appears to be after extended stable branch point (1160321).

Requesting merge to other stable M117 because latest trunk commit (1205927) appears to be after other stable branch point (1181205).

Requesting merge to stable M118 because latest trunk commit (1205927) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1205927) appears to be after beta branch point (1204232).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to stable.

Merge review required: M118 has already been cut for stable release.

Merge review required: M119 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117, 118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-08)

Requesting merge to extended stable M116 because latest trunk commit (1205927) appears to be after extended stable branch point (1160321).

Requesting merge to other stable M117 because latest trunk commit (1205927) appears to be after other stable branch point (1181205).

Requesting merge to stable M118 because latest trunk commit (1205927) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1205927) appears to be after beta branch point (1204232).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to stable.

Merge review required: M118 has already been cut for stable release.

Merge review required: M119 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117, 118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2023-10-09)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4908270 only

2. Has this fix been tested on Canary?
There isn't an easy way to test the actual repro on canary; the scenario needs Android Webview or <webview> tags and requires specific timing which is covered in the included test.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
The fix is out in 120.0.6050.0 and I checked that there don't seem to be any new crashes in the affected code since that version. 

4. Does this fix pose any known compatibility risks?
No

5. Does it require manual verification by the test team? If so, please describe required testing.
No


### pg...@google.com (2023-10-09)

Merge approved for r1205927 to M118 and M119!
please merge to branch 5993 by EOD MTV Time Thursday Oct 12 to get this fix into the M118 stable refresh
and please merge to branch 6045 at your earliest convenience to get this fix into beta 

We don't have any more releases planned for M116 and M117 - removing the review labels

### gi...@appspot.gserviceaccount.com (2023-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d756d71a652ce5b537f83a020eb2db7c2335817c

commit d756d71a652ce5b537f83a020eb2db7c2335817c
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Mon Oct 09 17:14:13 2023

[M118] Fix RFHI::pending_navigate_ cleanup after crashes and early RFH swaps.

When resuming a navigation that had been saved into
RenderFrameHostImpl::pending_navigate_, we need to account for the
fact that OnBeginNavigation() calls GetFrameHostForNavigation() which
may perform an early RenderFrameHost swap and synchronously destroy
the old RFH.

There's also no need to keep a pending_navigate_ around after the
corresponding renderer process crashes, so this CL also adds logic to
clear it.  Resuming such a navigation would require additional work,
since the NavigationClient stashed in pending_navigate_ is no longer
usable and would just immediately call the disconnect handler and
cancel the navigation.  But there isn't really any benefit to adding
that complexity, and we already cancel the RFH's other ongoing
navigations when its renderer process dies.

This CL also tweaks the logic in RenderWidgetHostImpl to allow the
resuming logic (ResumeLoadingCreatedWebContents) to work without
hitting DCHECKs, if it's called after a renderer process crash. This
case never worked cleanly before, but is supported now (and allows the
new test to work without crashing).

(cherry picked from commit 093daae65d50511c2027d01f9188681749b5a1be)

Bug: 1487110
Change-Id: Icd6a55002e52729e6ee966210efba1a5ce23eb55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908270
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1205927}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4923011
Owners-Override: Krishna Govind <govind@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/5993@{#1208}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/d756d71a652ce5b537f83a020eb2db7c2335817c/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/d756d71a652ce5b537f83a020eb2db7c2335817c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/d756d71a652ce5b537f83a020eb2db7c2335817c/content/browser/renderer_host/render_widget_host_impl.cc


### [Deleted User] (2023-10-09)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2023-10-09)

https://crbug.com/chromium/1487110#c33:
1. This wasn't a recent regression.  It's likely been around for a while, before M114.
2. No.


### gi...@appspot.gserviceaccount.com (2023-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/da9d5bc3cbb66467123dd256460e833d846104d1

commit da9d5bc3cbb66467123dd256460e833d846104d1
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Mon Oct 09 18:14:34 2023

[M119] Fix RFHI::pending_navigate_ cleanup after crashes and early RFH swaps.

When resuming a navigation that had been saved into
RenderFrameHostImpl::pending_navigate_, we need to account for the
fact that OnBeginNavigation() calls GetFrameHostForNavigation() which
may perform an early RenderFrameHost swap and synchronously destroy
the old RFH.

There's also no need to keep a pending_navigate_ around after the
corresponding renderer process crashes, so this CL also adds logic to
clear it.  Resuming such a navigation would require additional work,
since the NavigationClient stashed in pending_navigate_ is no longer
usable and would just immediately call the disconnect handler and
cancel the navigation.  But there isn't really any benefit to adding
that complexity, and we already cancel the RFH's other ongoing
navigations when its renderer process dies.

This CL also tweaks the logic in RenderWidgetHostImpl to allow the
resuming logic (ResumeLoadingCreatedWebContents) to work without
hitting DCHECKs, if it's called after a renderer process crash. This
case never worked cleanly before, but is supported now (and allows the
new test to work without crashing).

(cherry picked from commit 093daae65d50511c2027d01f9188681749b5a1be)

Bug: 1487110
Change-Id: Icd6a55002e52729e6ee966210efba1a5ce23eb55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908270
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1205927}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4923109
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/6045@{#206}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/da9d5bc3cbb66467123dd256460e833d846104d1/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/da9d5bc3cbb66467123dd256460e833d846104d1/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/da9d5bc3cbb66467123dd256460e833d846104d1/content/browser/renderer_host/render_widget_host_impl.cc


### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-10-12)

1. One - https://crrev.com/c/4930701
2. Low - simple conflicts
3. M118
4. Yes

### gm...@google.com (2023-10-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-13)

Congratulations @18楼梦想改造家! The Chrome VRP Panel has decided to award you $20,000 for this report of a browser process memory corruption + $7,000 for renderer RCE (given since a compromised renderer is not necessary to trigger the browser process UAF) + $1,000 bisect bonus. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- excellent work! 

### 18...@gmail.com (2023-10-13)

Thank u , u are generous!

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/90b27947157fefc821097ad8eff719bc137552f5

commit 90b27947157fefc821097ad8eff719bc137552f5
Author: Zakhar Voit <voit@google.com>
Date: Tue Oct 17 10:54:06 2023

[M114-LTS] Fix RFHI::pending_navigate_ cleanup after crashes and early RFH swaps.

When resuming a navigation that had been saved into
RenderFrameHostImpl::pending_navigate_, we need to account for the
fact that OnBeginNavigation() calls GetFrameHostForNavigation() which
may perform an early RenderFrameHost swap and synchronously destroy
the old RFH.

There's also no need to keep a pending_navigate_ around after the
corresponding renderer process crashes, so this CL also adds logic to
clear it.  Resuming such a navigation would require additional work,
since the NavigationClient stashed in pending_navigate_ is no longer
usable and would just immediately call the disconnect handler and
cancel the navigation.  But there isn't really any benefit to adding
that complexity, and we already cancel the RFH's other ongoing
navigations when its renderer process dies.

This CL also tweaks the logic in RenderWidgetHostImpl to allow the
resuming logic (ResumeLoadingCreatedWebContents) to work without
hitting DCHECKs, if it's called after a renderer process crash. This
case never worked cleanly before, but is supported now (and allows the
new test to work without crashing).

(cherry picked from commit 093daae65d50511c2027d01f9188681749b5a1be)

(cherry picked from commit d756d71a652ce5b537f83a020eb2db7c2335817c)

Bug: 1487110
Change-Id: Icd6a55002e52729e6ee966210efba1a5ce23eb55
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4908270
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1205927}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4923011
Owners-Override: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5993@{#1208}
Cr-Original-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4930701
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1621}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/90b27947157fefc821097ad8eff719bc137552f5/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/90b27947157fefc821097ad8eff719bc137552f5/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/90b27947157fefc821097ad8eff719bc137552f5/content/browser/renderer_host/render_widget_host_impl.cc


### rz...@google.com (2023-10-18)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1487110?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Apps>BrowserTag]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073505)*
