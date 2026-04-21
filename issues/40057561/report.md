# URL Spoof after crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40057561](https://issues.chromium.org/issues/40057561) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Windows |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2021-10-10 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36

Steps to reproduce the problem:
Run the following code:

// Go to same origin (Page to display)
let w = open(location.href);

// Go to URL to show
w.location = "https://http.cat/200";

// Crash somehow (Devtools task manager, bug, crash from eTLD)

w.location = "data:html,foo";

What is the expected behavior?
For the URL to reflect the content being displayed.

What went wrong?
The content of example.com was put on https://http.cat/200

Did this work before? N/A 

Chrome version: 94.0.4606.81  Channel: stable
OS Version: 10.0

Not yet got the page responsive.
Requires a crash.

Seems similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1111646

## Attachments

- [ext - Copy.png](attachments/ext - Copy.png) (image/png, 49.0 KB)

## Timeline

### [Deleted User] (2021-10-10)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-11)

Thanks for the report. It seems that the repro steps are exactly the same as the repro steps in https://crbug.com/1172690#c25. And that bug was marked as a duplicate. 

To clarify, are you saying that https://crbug.com/1172690 was not fixed or this report is actually a different issue? Thanks!

### nd...@protonmail.com (2021-10-12)

Yes, this is different minor changes have been made.

### nd...@protonmail.com (2021-10-12)

Its no longer using document.write() this time its showing the page content and is using the same process as the same origin from window.open()

### [Deleted User] (2021-10-12)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2021-10-12)

To provide my point this is it pretending to be a chrome-extension.
It does also work for real URLs I just only toke a screenshot of this.

### nd...@protonmail.com (2021-10-14)

Any progress with verifying it?
I understand its very similar to the public bug it could probably be found by accident.

### bd...@chromium.org (2021-10-15)

The repro steps in this bug is exactly the same as https://bugs.chromium.org/p/chromium/issues/detail?id=1111646#c27 minus step 5. 

When I did this step: w.location = "data:html,foo"; I got a blank page and did not see example.com which is expected. I did the steps in Windows stable

Also adding @dcheng as they were the owner of the simliar bug.

[Monorail components: Blink>Loader UI>Browser>Navigation]

### [Deleted User] (2021-10-15)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-15)

Thanks for the explanation. I'm able to reproduce on version 94.0.4606.81:
1) Visit example.com
2) In DevTools: let w = winodw.open(location.href); w.location = "https://http.cat/200";
3) Kill the https://http.cat/200 process in Chrome's task manager.
4) In the original tab: w.location = "data:html,foo";

The said tab gets replaced with the content on example.com, while the URL still shows https://http.cat/200.

+fergal@ to take a look, since you looked into https://crbug.com/1169844. Also add some folks who was involved in https://crbug.com/1172690 to double check. Thanks!

[Monorail components: Internals>Sandbox>SiteIsolation]

### xi...@chromium.org (2021-10-15)

Oops, looks like bdea@ is already looking into it. I'd defer to bdea@ to triage it.

### dc...@chromium.org (2021-10-15)

There is definitely something broken here, but I'm not able to repro a URL spoof. For me, the tab just doesn't paint after trying to navigate the crashed frame to a data: URL (which is also broken).

### nd...@protonmail.com (2021-10-15)

Not sure why its sometimes a spoof and sometimes white.
It may depend on what page is used for testing.

### al...@chromium.org (2021-10-15)

FWIW, I was also able to repro on Windows canary 96.0.4660.6, beta 95.0.4638.49, and stable 94.0.4606.81.  I started at https://csreis.github.io rather than example.com.  I also noticed that after the last step, the opened tab had a console error, "Not allowed to navigate top frame to data URL: data:html,foo", so the data URL blocking code for main frames might be involved here.  Notably, several other folks in CSA were not able to repro, so I wonder if there's a field trial involved and I just happened to be in the right group.

### dc...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### al...@chromium.org (2021-10-15)

Posting my variations in case it's helpful:

f475deb0-377be55a
313957be-ca7d8d80
af81735d-ca7d8d80
4dc415b1-ca7d8d80
7e184ca7-ca7d8d80
90a7075b-8456389e
16b16054-377be55a
8e73c278-ca7d8d80
1fa5b2f3-377be55a
59b6f412-377be55a
60d4b352-377be55a
5fff72eb-377be55a
325b8c14-12ede6a2
273268f8-a9c1148c
eddd0d82-bd8d826e
7536a4f6-ca7d8d80
87f33ad6-ca7d8d80
5d093a14-ca7d8d80
8816d952-65bced95
3095aa95-3f4a17df
c27fec31-920bf621
e799dcad-12ede6a2
fcd625f7-377be55a
edb58ea9-377be55a
a2629469-ca7d8d80
1bb6a450-ca7d8d80
deb1cb12-78b7da10
47bd2c48-ca7d8d80
1e7be480-6edc92c7
1e940a7c-ca7d8d80
76cbd0ec-12ede6a2
47b5f350-377be55a
4749874c-9cc37238
ab544014-ca7d8d80
f2cb61f-377be55a
a2fd384c-5c0c03aa
5d77151b-377be55a
c1abf59f-ca7d8d80
bf4029fe-364c5591
65570806-20f58b6f
e17bdae7-9c88f5c6
dd8d67e-1f8c5973
f6f5c542-12ede6a2
aba0c93-377be55a
a582a1b8-ad75ce17
6a5f15b-ca7d8d80
d89faab1-ca7d8d80
722b8030-ca7d8d80
3042ad4b-ca7d8d80
e4a357e9-ca7d8d80
f96fd6bf-bddd9fc3
6262de83-377be55a
7b7adda-ca7d8d80
12325be2-12ede6a2
61c68934-ca7d8d80
5e3a236d-59e286d0
e79de56c-d682eef0
357a64de-d682eef0
8bccc03b-ca7d8d80
facdb7bf-ca7d8d80
2b4e7fda-8d1a7638
d809cc5d-1f8c5973
28114f9b-8f65fe02
291d0672-7c933c8b
7a911e9f-ca7d8d80
b75782da-ca7d8d80
8c8d8faf-6edc92c7
255dfea8-ca7d8d80
cbb84eed-e5bf8a5d
e153f4cb-377be55a
ca5a2953-ca7d8d80
4863d2b7-ca7d8d80
3487aa71-ca7d8d80
5fe247df-ca7d8d80
ad46906e-ca7d8d80
234de0a0-ca7d8d80
261b9697-ca7d8d80
d3566fbd-8ca19036
a0a65d04-377be55a
4ea303a6-ecbb250e
cb47d7a6-ca7d8d80
f48aee36-377be55a
7aa46da5-c946b150
4210aecc-377be55a
c9e4cf65-12ede6a2
9af490f6-ca7d8d80
2e36b1b8-ca7d8d80
c1003591-12ede6a2
334be1ac-377be55a
fbe267b5-12ede6a2
7cec0dd3-1f8c5973
26464629-ca7d8d80
f323d3f0-ca7d8d80
5d2c15d5-b51e90cc
5176c13e-ca7d8d80
7760b5b2-ca7d8d80
eb084fc2-ca7d8d80
e8c68789-ca7d8d80
bf15c287-65bced95
1354da85-781294a7
ad4acdda-ca7d8d80
931c5f72-c9ea5ad5
494d8760-52325d43
f47ae82a-86f22ee5
3ac60855-3ec2a267
63dcb6a3-29f53bb4
e706e746-c42a4255
f296190c-2502111b
4442aae2-7158671e
f690cf64-d7f6b13c
ed1d377-e1cc0f14
75f0f0a0-e1cc0f14
e2b18481-6754d7b7
e7e71889-4ad60575
3a8271ac-12c226
b1ceb06f-d1372334
15ad48ac-377be55a
25692333-ca7d8d80
2d3dfd19-ca7d8d80
e1368496-ca7d8d80
248e3a0-ca7d8d80
dba92675-12ede6a2
595f5eb0-ca7d8d80
3673692f-12ede6a2
bef5c006-ca7d8d80
17b84626-ca7d8d80
b4e05be7-9c7cf9bf
1b4184a1-8693a4e4
fb50494f-72cac062
547e761a-3f4a17df
89f843ca-2cbb00ec
5e31bb48-75513c66
a9deeaf7-bcdae55b
d661ac70-20c6468c
a461b170-377be55a
dd82d379-33c3eba5
def27776-ca7d8d80
733cb831-ca7d8d80
b53f3ef9-65bced95
2856aa31-f23d1dea
6b366ac3-ca7d8d80
4da3fbb2-ca7d8d80


### dc...@chromium.org (2021-10-15)

I haven't really narrowed down what's causing this. I do think there are two questions to consider here:

creis@: what should we be showing in the omnibox for an early committed frame when we're navigating after a crash? I think we probably should not be persisting the old URL. Even though the opener window cannot poke at the DOM anymore, the early committed crash frame is not necessarily related to the old URL either (as demonstrated by this bug).

Separately, I suspect there is some bug where something is incorrectly holding on to the last thing a renderer painted. It's unclear what that is though. The reason the early committed frame isn't painting is almost certainly because of https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/frame/local_frame_view.cc;l=4650;drc=cec3ae634439682f480b439d3eaf11544a3429c9 (which is tracked as https://crbug.com/chromium/1231231).

### dc...@chromium.org (2021-10-16)

I tried to bisect variations, but I was not able to find a culprit. I suspect it is not a finch experiment, as I *was* able to consistently reproduce this on both Windows (stable and dev) and Linux (stable), but not on Mac (stable or canary).

pdr@ mentions that it's probably something inside the compositor that's hanging on to the last painted image. At this point, I don't really know where to look though. CCing a few people who might have some more ideas...

Once we diagnose the stale paint issue, I will split this into two sub bugs:
1. figure out what to do with the omnibox URL for early crashed frames
2. make sure we clear the last painted image on a crash

I do have one question about cross-origin paint holding. It has this to say:

> The Paint Holding Cross Origin feature extends Paint Holding to most
> navigations. Paint Holding defers the first commit of rendering
> data from the main thread to the compositor until after First
> Contentful Paint, or a 500ms timeout, has occurred.

Presumably, during this period of time, we just use the previously rendered content? Where does the logic for retaining that live? Is it possible it's somehow not being cleared when a render process crashes? And is there any reason this logic might operate differently on Mac vs other platforms?

### dc...@chromium.org (2021-10-16)

One other interesting thing that xinghuilu@ noted (and I reproduced):

let w = window.open(location.href); w.location = 'https://http.cat/200';

and then terminating the render process will not reproduce the bug.

The initial navigation to location.href (e.g. example.com in the reproduction I tested) must complete before navigating to https://http.cat/200. Presumably, this is because that initial navigation to location.href is needed to cache the painted content that is later incorrectly shown.

### [Deleted User] (2021-10-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2021-10-19)

The viz compositor (the thing that actually controls what's on the screen) displays a given frame until it is told to display the next one, or a blank surface (at least as far as I know). So if we never tell it to update the display surface, it won't. The browser process can talk to viz, but I have no idea how crashes are communicated around the various processes.

Paint Holding doesn't behave any differently cross platform. Mac uses different structures for the rendered surfaces and it's possible that the core Mac libraries are doing more than the GL libraries.

I do have this comment in the security review for Paint Holding, which may addrewss someo f the issues here:

<verbatim>
This feature [Paint Holding] won't affect the 4s timeout as is because the new_content_rendering_timeout_ signal goes directly to the display compositor to replace the visible surface with a fallback, regardless of what the rendering is doing. I just checked to code.

It occurs to me that I should hook up the new_content_rendering_timeout_ to always stop deferring BeginMainFrame and Commit on the renderer as well. That way no matter what happens we'll generate and push a frame as soon as possible after the 4s. That will address some problems we have with frames never starting at all.
</verbatim>

### jo...@chromium.org (2021-10-20)

For https://crbug.com/chromium/1258363#c18 questions
>> pdr@ mentions that it's probably something inside the compositor that's hanging on to the last painted image. At this point, I don't really know where to look though. CCing a few people who might have some more ideas...

Viz will hold onto/display the previous content (Surface) submitted by the Renderer until either
   - Renderer submits new content
   - Browser tells Viz to evict the current Renderer content.

I would expect that a Renderer crash would trigger CompositorFrameSinkImpl::OnClientConnectionLost. But while we currently clear out the connection info, we may be keeping the Surface around.

>> Presumably, during this period of time, we just use the previously rendered content? Where does the logic for retaining that live?

SurfaceManager::InvalidateFrameSinkId should be called based on the Renderer crash. IIRC this keeps the most recent Surface alive.

I'm not familiar with how the Browser process is told of the Renderer crash. However when the Browser re-creates the Renderer it should be updating Viz of the new connection. Which should lead to clearing the old Surface.

>> And is there any reason this logic might operate differently on Mac vs other platforms?

DelegatedFrameHost::EmbedSurface / DelegatedFrameHostAndroid::EmbedSurface handle telling Viz of the new Surface. However there are platform specific usage differences. Each platform has its own RenderWidgetHostViewBase implementation. So there may be a Mac edge case here.


### dc...@chromium.org (2021-10-21)

> I would expect that a Renderer crash would trigger CompositorFrameSinkImpl::OnClientConnectionLost. But while we currently clear out the connection info, we may be keeping the Surface around.

Do we need to keep the surface around?

> I'm not familiar with how the Browser process is told of the Renderer crash. However when the Browser re-creates the Renderer it should be updating Viz of the new connection. Which should lead to clearing the old Surface.

So to be clear, the scenario here is:

  1. load foo.com
  2. foo.com opens a new window to foo.com
  3. opened window navigates to bar.com
  4. crash bar.com renderer
  5. attempt to navigate to data: URL in opened window

So we don't need to create a new renderer in step 5. When we trigger the early commit, we simply reuse the renderer that we already have for foo.com.

What does "clearing the old surface" mean? And what happens if the new frame never generates any compositor frames?

### jo...@chromium.org (2021-10-21)

> Do we need to keep the surface around?

Typically I wouldn't expect it to be there long. I'd expect the "Aw, Snap" to appear and replace it. We could look at clearing it all out and displaying a blank region.

> So to be clear, the scenario here is:

>   1. load foo.com
>   2. foo.com opens a new window to foo.com
>   3. opened window navigates to bar.com
At this point I expect Viz to have released all surfaces from "foo.com"
>   4. crash bar.com renderer
Here is where I'd expect "bar.com" to be around shortly until the "Aw, Snap" appears.
>   5. attempt to navigate to data: URL in opened window
Here we set a navigation timeout, and keep displaying whatever content was there. With typically two outcomes:
  1. Navigation completes, Viz stops shows any "bar.com" content
         RenderWidgetHostView*::OnDidNavigateMainFrameToNewPage should be called by WebContentsImpl::DidNavigateMainFramePostCommit when a Renderer is being re-used for a different URL Origin.
  2. Timeout is reached, Viz clears the "bar.com" content, you get a blank region
         RenderWidgetHostImpl::ForceFirstFrameAfterNavigationTimeout is called

> So we don't need to create a new renderer in step 5. When we trigger the early commit, we simply reuse the renderer that we already have for foo.com.

I've never looked at a crashed renderer attempting a subsequent navigation. In the past year we've seen some bugs where a navigation commit never completes the navigation, and Android kept previous URL content around. It sounds like crash+navigation might be triggering a similar error.

> What does "clearing the old surface" mean? And what happens if the new frame never generates any compositor frames?

The Browser tells Viz to stop showing the old surface, after waiting N frames. (Varies per platform/reason we are clearing). Which leads to two outcomes:
  1. We get the new compositor frames. We discard the old surface from memory.
  2. Nothing arrives by the deadline.  We discard the old surface from memory. Next VSync we show a blank region.


### dc...@chromium.org (2021-10-22)

> Typically I wouldn't expect it to be there long. I'd expect the "Aw, Snap" to appear and replace it. We could look at clearing it all out and displaying a blank region.

It does get replaced by an "Aw, Snap". However, today, we have an early commit optimization. What happens in this case is the omnibox is still display "bar.com" but displays a surface from "foo.com". I have no idea why.

> I've never looked at a crashed renderer attempting a subsequent navigation. In the past year we've seen some bugs where a navigation commit never completes the navigation, and Android kept previous URL content around. It sounds like crash+navigation might be triggering a similar error.

Where should I add logging to try to narrow this down? To be clear, this is not a crashed renderer attempting a subsequent navigation. There are two renderers involved in this: foo.com and bar.com. bar.com crashes. foo.com attempts to navigate after the crash, and navigating to data: URLs causes the process selection to choose the foo.com renderer. But the navigation itself is then cancelled since we no longer allow renderer-initiated navigations to top-level data URLs.

### nd...@protonmail.com (2021-10-23)

The white page happens when the new window is not visible. maybe to do with how background tabs are handled.

### jo...@chromium.org (2021-10-25)

> Where should I add logging to try to narrow this down? To be clear, this is not a crashed renderer attempting a subsequent navigation. There are two renderers involved in this: foo.com and bar.com. bar.com crashes. foo.com attempts to navigate after the crash, and navigating to data: URLs causes the process selection to choose the foo.com renderer. But the navigation itself is then cancelled since we no longer allow renderer-initiated navigations to top-level data URLs.

This is the part of the stack that I'm not familiar with. creis@ can likely give more guidance. NavigationRequest::StartNavigation, Navigator::DidFailLoadWithError, and WebContentsImpl's NavigatorDelegate methods are likely the best place.

I'm only familiar with when that leads into calling RenderWidgetHost* classes.

From that description it sounds like RenderWidgetHostImpl::ForceFirstFrameAfterNavigationTimeout isn't firing, nor do we have an explicit path to it from the cancellation. Also sounds like the URL bar needs to be updated in relation to the cancellation too.

### dc...@chromium.org (2021-10-25)

I'll take a look at ForceFirstFrameAfterNavigationTimeout(), but at this point, I'm 99% certain there's some issue with disposing the old surface. Do we have an internal pool of surfaces that we keep around somewhere and reuse, to avoid churning resources?

In the browser process, we have something like this:

1. new RFH for foo.com -> some surface
2. navigate to bar.com
3. new RFH for bar.com -> some other surface
4. <crash bar.com>
5. new RFH for foo.com when attempting to navigate to data:html,foo

The problem is somehow, the RFH in step 5 is getting associated with the surface used for the RFH in step 1. Any idea on how that could happen? Even if RFH 5 *never* generates a frame, there is no reason we retained the last frame generated by step 1 and reused in step 5.

### jo...@chromium.org (2021-10-25)

Could you record a Trace for "UI Rendering" and enable "viz.surface_id_flow" under "Edit categories". That can let us confirm if a Surface from RFH 1 is being shown at step 5. 



### dc...@chromium.org (2021-10-27)

It looks like we're getting a new surface. I'm not familiar enough with viz to keep tracing at this; jonross@ has volunteered to help / find someone who can investigate this a bit more.

To reproduce the steps in the attached trace (only works on Windows or Linux):
1. Open a new window. Navigate to example.com
2. Open inspector for the example.com frame.
3. const w = window.open(location.href);
4. Once the newly opened window is fully loaded, w.location = 'https://http.cat/200'; Wait for this to load as well.
5. Open the task manager. Kill the render process for 'https://http.cat/200'. This will generate a sad frame in the opened window.
6. Go back to the already-opened inspector instance. w.location = 'data:html,foo'.
7. The opened window now shows the content that was previously painted after step 3. This is incorrect.

Right now, there are three aspects to mitigating this bug:
1. I am working on a CL to make initial empty documents paint at least once. This will resolve the problem for non-compromised renderers.
2. We need to understand where the 'ghost image' in step 7 is coming from in viz. This could be a bug or something else. I am relying on jonross@ or someone else from the viz team to resolve this.
3. Removing the early commit optimization (https://crbug.com/chromium/1072817) so we no longer have to deal with the implications of the omnibox displaying the old URL when we've already done an early commit (which may not be in a renderer for the origin of the old URL).

3 is a long-term fix.

1 and 2 are more short-term fixes that may not be robust to compromised renderers, but should nonetheless be done. Ideally, we land both fixes, and decide which one is simpler/safer to merge if needed.

### nd...@protonmail.com (2021-10-29)

Not sure if this makes it worse :/

A browser extension with no permissions can use chrome.tabs.update(ID, {url: "chrome://heapcorruptioncrash"});
To force crash any tab.

Its also possible to use chrome.processes but that can be fixed just by changing the warning to something better then "Read your browsing history" since it seems to do a bit more then that.

### nd...@protonmail.com (2021-10-31)

Regarding https://crbug.com/chromium/1258363#c31 I have made https://bugs.chromium.org/p/chromium/issues/detail?id=1265197#c2 for it. (Since its just me complaing about the tabs API with no permissions)

### jo...@chromium.org (2021-11-02)

I'm taking a look now.

From an initial look this seems to be a bug in Navigation. When https://crbug.com/chromium/1258363#c30 step 6 occurs the Browser process does the following:
#2 0x5556838793e3 content::DelegatedFrameHost::EmbedSurface()
#3 0x5556836168b8 content::RenderWidgetHostViewAura::SynchronizeVisualProperties()
#4 0x5556836162e6 content::RenderWidgetHostViewAura::SetSize()
#5 0x55568376bc0d content::WebContentsImpl::NotifySwappedFromRenderManager()
#6 0x5556835c66fc content::RenderFrameHostManager::CommitPending()
#7 0x5556835c9588 content::RenderFrameHostManager::GetFrameHostForNavigation()
#8 0x5556835c895d content::RenderFrameHostManager::DidCreateNavigationRequest()
#9 0x5556834a9175 content::FrameTreeNode::CreatedNavigationRequest()
#10 0x5556835727c8 content::Navigator::Navigate()
#11 0x555683536df9 content::NavigationControllerImpl::NavigateFromFrameProxy()
#12 0x5556835730da content::Navigator::NavigateFromFrameProxy()
#13 0x5556835d6bed content::RenderFrameProxyHost::OpenURL()

content::WebContentsImpl::NotifySwappedFromRenderManager is actually swapping out the RenderFrameHostImpl of the Crashed Renderer to the one that was previously created on Step 3. 

At first it seems to be treating the scenario similar to using the 'Back' button. 
    - Though that is grayed out in this particular interaction. 
    - The 'Back' navigation however triggers RenderWidgetHostView*::OnDidNavigateMainFrameToNewPage/WebContentsImpl::DidNavigateMainFramePostCommit path that is a part of the Surface Eviction.
   - The stack above never triggers that path.

In both cases RenderFrameHostManager selects the previous RenderWidgetHostViewAura, which just tells Viz to re-embed the last surface.
 
For https://crbug.com/chromium/1258363#c30 question 2)
   - The ghost image is actually the last valid Surface submitted by the "example.com" site before the navigation to  'https://http.cat/200'
   - This is an expected behaviour for when a pending commit like this occurs.
   - Normally the commit completes, and the Renderer submits new frames
   - The timeout to evict old-content is hooked up to post-commit calls, and is not occurring in this case.

Reading https://crbug.com/chromium/1072817, this seems to be another symptom of that. 

As an interim step we could look to hooking up the timeout that normally happens post-commit. However that would not address that the URL would stay incorrect.




### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-12-08)

Per https://crbug.com/chromium/1258363#c30 we have a change up for review that is a mitigation of the old 'ghost image' being displayed:

https://chromium-review.googlesource.com/c/chromium/src/+/3307264

### nd...@protonmail.com (2021-12-09)

:) although to avoid a different spoof bug from this behavior the URL needs to at least display "about:blank" on crash.

### dc...@chromium.org (2021-12-09)

> although to avoid a different spoof bug from this behavior the URL needs to at least display "about:blank" on crash.

While it's true the URL doesn't match the renderer it's committed in, and that's an issue, because we shouldn't have to trust the renderer is not compromised. But in a non-compromised renderer, I don't think there should be a URL spoof issue?

### nd...@protonmail.com (2021-12-09)

Its an improvement but "the URL doesn't match the renderer it's committed in" may cause other bugs,
Since this bug did not use a compromised renderer.
It should not be possible to navigate a crashed tab without the URL changing.

### nd...@protonmail.com (2021-12-10)

I think its now the 3rd time now this has been exploited in a non-compromised renderer,
Since https://bugs.chromium.org/p/chromium/issues/detail?id=1226909 also abused this.

Thats why I dont trust the fix.

### gi...@appspot.gserviceaccount.com (2021-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61ec65342db11143d9ec4232587c95c1f075d562

commit 61ec65342db11143d9ec4232587c95c1f075d562
Author: Jonathan Ross <jonross@chromium.org>
Date: Tue Dec 14 23:01:40 2021

Evict Fallback Surface During Failed Commit

RenderFrameHostManager::CommitPending can re-use an existing
RenderViewHostImpl, which can have a Fallback Surface from previous
navigations. When swapping it is possible that the current
RenderWidgetHostView* was deleted, such as for a Renderer crash. This
leaves us with no current Surface to take as a new Fallback Surface.

It is possible for CommitPending to be for invalid target, effectively
failing. RenderFrameHostManager::CommitPendingIfNecessary can also
cancel on-going navigations.

Previously RenderWidgetHostView* would set a timeout at the start of
navigation, so that if navigation fails we could clear any Fallback
Surface. However when the above occurs there is no navigation, but we
have the Fallback Surface from a previous navigation.

This change updates RenderFrameHostManager::CommitPending to notify its
Delegate of this impending inability to swap Fallback Surfaces.
RenderWidgetHostView* will then clear the previous Fallback Surfaces.

TEST= content_browsertests
  NoCompositingRenderWidgetHostViewBrowserTest.NoFallbackIfSwapFailedBeforeNavigation
      content_unittests
  All/RenderFrameHostManagerTestWithSiteIsolation.TwoTabsOneNavigatesAndCrashesThenNavigatesBack/{0,1}
  *CrossOriginOpenerPolicyBrowserTest.CoopPageCrashIntoNonCoop*

Bug: 1258363, 1072817
Change-Id: Id545767366843ab607db925e0e4815668a4f7ab2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307264
Reviewed-by: Bo Liu <boliu@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Jonathan Ross <jonross@chromium.org>
Cr-Commit-Position: refs/heads/main@{#951710}

[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_mac.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_browsertest.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_mac.mm
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_frame_host_manager.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/ui/android/delegated_frame_host_android.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_base.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_android.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/test/test_render_view_host.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/delegated_frame_host.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/delegated_frame_host.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_android.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_aura.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_frame_host_manager.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/test/test_render_view_host.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/ui/android/delegated_frame_host_android.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_widget_host_view_aura.h
[modify] https://crrev.com/61ec65342db11143d9ec4232587c95c1f075d562/content/browser/renderer_host/render_frame_host_manager_unittest.cc


### jo...@chromium.org (2021-12-15)

Regarding #37 I believe that regardless of the compromised/not state of the Renderer, that leaving the URL not matching is incorrect:
  - There is nothing stopping the Renderer from producing new frames, but with the incorrect URL
  - The Reload button reloads the current displaying URL, not the visible Renderer
  - This does not match the behaviour of clicking the Back button while on a crashed Renderer. (Which does change to reflect the old Renderer becoming visible)

This is an inconsistent UX, with a potential path for further spoofing issues.

The example repro in #30 was great for finding the 'ghost image'. I do feel that we need one more step to completely fix this issue. From #30 Step 6.
   w.location = 'data:html,foo'
This is when we attempt to navigate from the crashed 'https://http.cat/200' to that invalid location. I think that when this navigation begins we need to update the URL to either match the Renderer being swapped in 'example.com' or whatever URL that location would be interpreted as.

dcheng@ / cries@ whom would be best to look into this next step of the fix?

### nd...@protonmail.com (2022-01-13)

It seems this depends on https://crbug.com/chromium/1072817 being fixed otherwise crashed tabs need there own URL like they do with there origin.
Or like how it was done in the crossoriginisolated bug and add COOP on crash to prevent navigation's.

### nd...@protonmail.com (2022-01-14)

Not sure if connected but when using a 204 header, Its also possible for the URL to use the same process.
PoC with onclick:
f = document.createElement("iframe");
f.srcdoc = "<script>document.onclick = e => { w = open('https://httpstat.us/204') }</script>";
document.body.appendChild(f);

Im trying to find out if this affects iframes so far I got it to crash on iframe creation that seems strange.

### nd...@protonmail.com (2022-01-21)

Is progress being made with this bug?

It seems the steps for this issue are in the public bug,
So the ghost image patch would be good to apply :)

Getting a tab to crash does not seem like a valid security migration,
Last time this bug was reported there was a way to crash any origin.

Or any extension can do it (still not fixed, no one replying), that's assuming it requires a crash but https://crbug.com/chromium/1258363#c43 seem to say otherwise.

I dont want a duplicate bug of my duplicate bug.



### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-07-20)

dcheng - is there perhaps another owner who could take a look at this old bug? Thanks!

### nd...@protonmail.com (2022-07-23)

I think the issue that was fixed is the ghost image.
The URL doesn't match the renderer it's committed in with a 204 header (https://crbug.com/chromium/1258363#c43) or an after crash navigation (https://crbug.com/chromium/1258363#c10)
Should also be fixed so an active owner would be good if this is not being tracked in a different issue.

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-27)

I'm going to mark this as fixed because the issue as reported isn't occuring anymore. Yes, a compromised renderer could produce invalid/weird frames, but realistically, if someone has that level of control, we're already in a lot of trouble as they almost certainly have arbitrary code execution in the renderer.

Similarly if a server replies with 204, it can't control the content in the page: it's a no-content response.

While it's possible to mess with the URL display to try to blank it out (it's pretty unclear what it should show for blocked navigations or the 204 case), that seems very likely to just open up other potential problematic interactions.

In the future, we hope to remove the early commit optimization; that's tracked as https://crbug.com/chromium/1072817 and will resolve the remaining concerns here.

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### nd...@protonmail.com (2023-02-03)

Thanks :)

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1258363?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail blocked-on: crbug.com/chromium/1072817]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057561)*
