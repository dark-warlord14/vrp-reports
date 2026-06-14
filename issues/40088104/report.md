# Security: Form field validation bubbles can appear after navigating to another origin

| Field | Value |
|-------|-------|
| **Issue ID** | [40088104](https://issues.chromium.org/issues/40088104) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Validation |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | lu...@chromium.org |
| **Created** | 2017-06-16 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 61.0.3131.0 canary  

Operating System: Windows 7

**REPRODUCTION CASE**  

Note: This is a regression bug seen on Canary.

See <https://crbug.com/chromium/673163> and <https://crbug.com/chromium/704560>

1. Open the test case
2. Click on the button and observe

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 149.1 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 988 B)

## Timeline

### el...@chromium.org (2017-06-16)

Interesting. The bubble persists, even as you switch to a different tab.

The bisect points to a single CL which seems credible:
You are probably looking for a change made after 479537 (known good), but no later than 479538 (first known bad).

https://chromium.googlesource.com/chromium/src/+/6e8a61ba16f529f02841fb75a50f15ec45726411

[Monorail components: Blink>Forms>Validation]

### es...@chromium.org (2017-06-16)

lukasza, can you please take a look?

### es...@chromium.org (2017-06-16)

[Empty comment from Monorail migration]

### lu...@chromium.org (2017-06-16)

When reproing the problem on Windows ToT build and on Linux ToT (with some extra ad-hoc debugging statements), I see that 1) the renderer tries to send ViewHostMsg_HideValidationMessage message (*), but 2) the message gets filtered out by CanSendWhileSwappedOut.

(*)     content::RenderViewImpl::HideValidationMessage [0x00007FFD710928DD+99]
        blink::ValidationMessageClientImpl::HideValidationMessage [0x00007FFD71E3B20C+112]
        blink::Document::DispatchUnloadEvents [0x00007FFD71C1B3A0+130]
        blink::FrameLoader::DispatchUnloadEvent [0x00007FFD70E3BEC0+94]
        blink::FrameLoader::PrepareForCommit [0x00007FFD70E3E408+222]
        blink::WebFrame::Swap [0x00007FFD70C46377+63]
        content::RenderFrameImpl::OnSwapOut [0x00007FFD7106DB5D+567]

Despite swapped-out filtering happening on Windows and Linux, for some reason I can only repro the problem on Windows Canary and ToT build, but not on Mac Canary and not on Linux ToT build.  I don't know yet why this Linux (and Mac) manage to clear the UI even when ViewHostMsg_HideValidationMessage message gets dropped.

I think that ultimately the *browser* (not the renderer) should trigger clearing of *all* UI specific to the old page, after WebContents commits navigation to another page.

To limit security impact to users on Canary and Dev channel I went ahead and kicked off a revert of r479538 : https://codereview.chromium.org/2938423002.



### lu...@chromium.org (2017-06-16)

It seems that the difference between Windows and Linux is that on Linux, the validation bubble is destroyed by the following callstack:

        #1 0x55c07ac9d603 ValidationMessageBubbleView::~ValidationMessageBubbleView()
    #2 0x55c07ac9d739 ValidationMessageBubbleView::~ValidationMessageBubbleView()
    #3 0x7f59527c6956 views::Widget::OnNativeWidgetDestroyed()
    #4 0x7f59527e229c views::NativeWidgetAura::OnWindowDestroyed()
    #5 0x7f5952d9e011 aura::Window::~Window()
    #6 0x7f5952d9e749 aura::Window::~Window()
    #7 0x7f5951e5668e wm::TransientWindowManager::OnWindowDestroying()
    #8 0x7f5952d9dea4 aura::Window::~Window()
    #9 0x7f5952d9e749 aura::Window::~Window()
    #10 0x7f595475684b content::RenderWidgetHostImpl::Destroy()
    #11 0x7f595475786b content::RenderWidgetHostImpl::ShutdownAndDestroyWidget()
    #12 0x7f59547546c7 content::RenderViewHostImpl::ShutdownAndDestroy()
    #13 0x7f5954516466 content::FrameTree::ReleaseRenderViewHostRef()
    #14 0x7f595453c77f content::RenderFrameHostImpl::~RenderFrameHostImpl()
    #15 0x7f595453d089 content::RenderFrameHostImpl::~RenderFrameHostImpl()
    #16 0x7f595455f4d5 content::RenderFrameHostManager::DeleteFromPendingList()
    #17 0x7f595453bdd9 content::RenderFrameHostImpl::OnSwappedOut()

On Windows, ValidationMessageBubbleView is not destroyed.


The above is probably caused by the fact that on Windows (unlike on Linux), I don't see any calls to the constructor of TransientWindowManager, so that later the validation popup is not getting tracked by:

    #1 0x7f5951e55081 wm::TransientWindowManager::AddTransientChild()
    #2 0x7f59527e04dd views::NativeWidgetAura::InitNativeWidget()
    #3 0x7f59527c3e7f views::Widget::Init()
    #4 0x7f595274893c views::BubbleDialogDelegateView::CreateBubble()
    #5 0x55c07ac9d4c4 ValidationMessageBubbleView::ValidationMessageBubbleView()
    #6 0x55c07ac7fb2f TabDialogsViews::ShowValidationMessage()
    #7 0x55c07abae3ca Browser::ShowValidationMessage()

### lu...@chromium.org (2017-06-16)

+sky@ and estade@: in case they i) want to look deeper into the cause of the Linux-vs-Windows difference that I tried starting to explain in https://crbug.com/chromium/733940#c5 or ii) have some advise on how to implement a generic mechanism for cleaning up page-specific UI after navigations (see below).

FWIW, the fact that the validation bubble disappears on Linux seems to be triggered by swapping the frames, but I think this wouldn't help in case a compromised renderer doesn't send ViewHostMsg_HideValidationMessage and the navigation doesn't require a process swap.  In other words, I still think we need to modify the browser process to clear page-specific UI elements when navigating to another page.  I am not yet sure about the exact code change that can do this:

- WebContentsImpl::DidFinishNavigation could just call WebContentsDelegate::HideValidationMessage (if NavigationHandle says 1) HasCommitted and 2) !IsSameDocument).  This is simple, but limited to validation bubbles.

- Maybe we can somehow wire wm::TransientWindowManager 1) to work across all platforms and 2) destroy page-specific widgets upon navigation.  This wouldn't be limited to validation bubbles, but I am unclear how the code for this would look like.

### es...@chromium.org (2017-06-16)

I don't think all transient windows would want to go away on navigations. I don't really know offhand the best place in content to add this, but here's my guess. When the tab crashes we close outstanding UI (dialogs, validation bubble, etc)[1]. When we navigate, we only close dialogs [2]. Maybe the validation bubble closing should be folded into CancelActiveAndPendingDialogs()?

[1] https://cs.chromium.org/chromium/src/content/browser/web_contents/web_contents_impl.cc?rcl=f9a5a0bad8b766df4faa51fdb1c74f01318d0128&l=4672
[2] https://cs.chromium.org/chromium/src/content/browser/web_contents/web_contents_impl.cc?rcl=f9a5a0bad8b766df4faa51fdb1c74f01318d0128&l=3702

### ni...@chromium.org (2017-06-16)

[Empty comment from Monorail migration]

### lu...@chromium.org (2017-06-16)

Thank you very much for suggesting CancelActiveAndPendingDialogs - this works and seems like a good place for the kind of UI resetting that we need here.

I can try putting together a //chrome layer browser test to protect against regressions, but it is not clear to me how to detect whether the validation bubble is being shown or not.  I think I can either
1. add a Browser::IsValidationMessageShownForTesting (just returning !!validation_message_bubble_)
2. count children of web_contents->GetRenderWidgetHostView()->GetNativeView() (since ValidationMessageBubbleView if present will be one of the children).

I am leaning toward #1.

### sh...@chromium.org (2017-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-17)

[Empty comment from Monorail migration]

### lu...@chromium.org (2017-06-19)

This bug should be fixed by the revert at https://codereview.chromium.org/2938423002.  OTOH, I'd like to keep this bug open to also add a regression test for the scenario covered by this bug - I have a WIP CL @ https://codereview.chromium.org/2949593003.

### lu...@chromium.org (2017-06-19)

I would like to use a separate bug (https://crbug.com/chromium/734729) to pursue other issues with how the form validation bubble is handled.  I think most of these issues would go away if the bubble was drawn together with the rest of the web content (rather than being drawn/hosted in a separate widget, with a separate set of IPCs for controlling this widget).

### bu...@chromium.org (2017-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/15399f887a0e8498253dc4496446eee83158e96a

commit 15399f887a0e8498253dc4496446eee83158e96a
Author: lukasza <lukasza@chromium.org>
Date: Thu Jun 22 21:59:14 2017

Move navigation-induced hiding of form-validation-bubble to the browser process.

Moving hiding of the form validation bubble to the browser process has
the following benefits:
- It allows simplifying/removing code from Blink (in particular it
  allows removing some of the code added in r459701).
- It makes the hiding immune against compromised renderers.
- It makes the hiding work even if ViewHostMsg_HideValidationMessage IPC
  gets filtered out (i.e. see CanSendWhileSwappedOut method in
  content::SwappedOutMessages).  This in turn will allow relanding
  of r479538.

BUG=733940
TEST=Manually verified that bugs 733940, 704560, 673163 are still fixed.

Review-Url: https://codereview.chromium.org/2949593003
Cr-Commit-Position: refs/heads/master@{#481681}

[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/dom/DocumentTest.cpp
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/html/HTMLFormControlElementTest.cpp
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/page/ValidationMessageClient.h
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/page/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/15399f887a0e8498253dc4496446eee83158e96a/third_party/WebKit/Source/core/page/ValidationMessageClientImpl.h


### bu...@chromium.org (2017-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/77083a5a889ea093f3343a68c543359c6a16f206

commit 77083a5a889ea093f3343a68c543359c6a16f206
Author: dcheng <dcheng@chromium.org>
Date: Fri Jun 23 08:34:45 2017

Revert of Move navigation-induced hiding of form-validation-bubble to the browser process. (patchset #2 id:20001 of https://codereview.chromium.org/2949593003/ )

Reason for revert:
Causing failures on WebKit Linux Trusty Leak.

({"numberOfLiveDocuments":[1,2],"numberOfLiveNodes":[4,62],"numberOfLiveResources":[0,2],"numberOfLiveSuspendableObjects":[2,3]})

Original issue's description:
> Move navigation-induced hiding of form-validation-bubble to the browser process.
>
> Moving hiding of the form validation bubble to the browser process has
> the following benefits:
> - It allows simplifying/removing code from Blink (in particular it
>   allows removing some of the code added in r459701).
> - It makes the hiding immune against compromised renderers.
> - It makes the hiding work even if ViewHostMsg_HideValidationMessage IPC
>   gets filtered out (i.e. see CanSendWhileSwappedOut method in
>   content::SwappedOutMessages).  This in turn will allow relanding
>   of r479538.
>
> BUG=733940
> TEST=Manually verified that bugs 733940, 704560, 673163 are still fixed.
>
> Review-Url: https://codereview.chromium.org/2949593003
> Cr-Commit-Position: refs/heads/master@{#481681}
> Committed: https://chromium.googlesource.com/chromium/src/+/15399f887a0e8498253dc4496446eee83158e96a

TBR=tkent@chromium.org,alexmos@chromium.org,estade@chromium.org,avi@chromium.org,lukasza@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=733940

Review-Url: https://codereview.chromium.org/2956593003
Cr-Commit-Position: refs/heads/master@{#481827}

[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/dom/DocumentTest.cpp
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/html/HTMLFormControlElementTest.cpp
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/page/ValidationMessageClient.h
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/page/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/77083a5a889ea093f3343a68c543359c6a16f206/third_party/WebKit/Source/core/page/ValidationMessageClientImpl.h


### bu...@chromium.org (2017-06-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/041634d6b54ab33ca9c506ec137fc4961d7792f1

commit 041634d6b54ab33ca9c506ec137fc4961d7792f1
Author: lukasza <lukasza@chromium.org>
Date: Mon Jun 26 18:21:10 2017

[reland] Move navigation-induced hiding of form-validation-bubble to the browser process.

Moving hiding of the form validation bubble to the browser process has
the following benefits:
- It allows simplifying/removing code from Blink (in particular it
  allows removing some of the code added in r459701).
- It makes the hiding immune against compromised renderers.
- It makes the hiding work even if ViewHostMsg_HideValidationMessage IPC
  gets filtered out (i.e. see CanSendWhileSwappedOut method in
  content::SwappedOutMessages).  This in turn will allow relanding
  of r479538.

BUG=733940
TEST=Manually verified that bugs 733940, 704560, 673163 are still fixed.
TBR=alexmos@chromium.org

Review-Url: https://codereview.chromium.org/2956673002
Cr-Commit-Position: refs/heads/master@{#482327}

[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/dom/DocumentTest.cpp
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/html/HTMLFormControlElementTest.cpp
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/page/Page.h
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/page/ValidationMessageClient.h
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/page/ValidationMessageClientImpl.cpp
[modify] https://crrev.com/041634d6b54ab33ca9c506ec137fc4961d7792f1/third_party/WebKit/Source/core/page/ValidationMessageClientImpl.h


### va...@chromium.org (2017-06-29)

Can this bug be marked as fixed now?
- you friendly secondary security sheriff

### ch...@gmail.com (2017-06-29)

This seems like fixed on Canary.

### lu...@chromium.org (2017-06-29)

Yes, sorry for the delay.  This can be marked as fixed.  Relanding of r479538 is tracked by https://crbug.com/chromium/733314.  OOPIF support is tracked by https://crbug.com/chromium/736009.  Some other security concerns are tracked by https://crbug.com/chromium/734729.

### sh...@chromium.org (2017-06-30)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-24)

Hi! $500 for the report - thanks as ever!

### ch...@gmail.com (2017-07-24)

Thanks Andrew :)

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-10-06)

This issue was migrated from crbug.com/chromium/733940?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088104)*
