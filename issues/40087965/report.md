# Security: Mac-only URL bar spoofing via HTTPS error interstitial?

| Field | Value |
|-------|-------|
| **Issue ID** | [40087965](https://issues.chromium.org/issues/40087965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Interstitials, UI>Browser>Navigation, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2017-06-02 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 61.0.3119.0 (Developer Build) (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**

1. Lunch the test case
2. Click on the button and wait

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 206 B)
- [Screen Shot 2017-06-02 at 18.08.43.png](attachments/Screen Shot 2017-06-02 at 18.08.43.png) (image/png, 193.4 KB)
- [actual.mov](attachments/actual.mov) (application/octet-stream, 1.7 MB)
- [how to repro.mov](attachments/how to repro.mov) (application/octet-stream, 1.9 MB)

## Timeline

### el...@chromium.org (2017-06-02)

In your repro, was the spoof persistent (e.g. showed on screen for more than 4 seconds) or ephemeral?

I wasn't able to reproduce the UI shown in the screenshot in either Canary or Stable, but with a ToT Chromium build I was in this state for ~500ms or so before the interstitial error content overwrote the content in the page.

[Monorail components: UI>Browser>Interstitials UI>Browser>Omnibox>SecurityIndicators]

### ch...@gmail.com (2017-06-02)

The was spoof was persistent not ephemeral. It does take several attempts.

### mb...@chromium.org (2017-06-02)

I just tried to repro this on Linux but wasn't able to. Charlie, I think you've fixed similar bugs in the past. Would you mind taking a look or reassigning this?

I'm tentatively assigning low severity to this since it seems somewhat racy and it retains the "Not secure" warning. Feel free to adjust if you disagree (in either direction).

### cr...@chromium.org (2017-06-02)

Thanks for the report, but I'm not able to repro this either.  Is there anything you can change to make it more reliable?

### ch...@gmail.com (2017-06-03)

You're welcome Charlie. I uploaded a video to see how I repro this bug, it seems like pretty hard to repro.

### ch...@gmail.com (2017-06-03)

1. Open the test case (A)
2. Click on the button to open a new tab (B)
3. Back to the page (A) and wait 5 seconds
4. Switch the page (B)

The adress bar shows expired.badssl.com but the content of google.com.

I believe this the easy way to repro this bug.

### sh...@chromium.org (2017-06-03)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-06-06)

Thanks.  I was finally able to repro this, but only on Mac.  I'm surprised, since I'm not aware of much Mac-specific code in interstitials or navigations.

On a Linux debug build, I see the same 'Blocked a frame with origin "null"' error on the DevTools console as in the video, but the interstitial always sticks around.

On Windows Canary 61.0.3122.0, I usually see the same thing, but a few times I've seen an Aw Snap page replace the interstitial.  Strangely, there's no entry for it in chrome://crashes, so I'm not sure what's causing it.

For the Mac repro steps, it looks like we're hitting a case that the interstitial page gets dismissed but the NavigationController's transient entry is still around.  That would be a bug with interstitials.  (It doesn't seem to be a case of a missing NotifyNavigationStateChanged call, because the stale URL is still present after switching tabs.)

avi@, do you know any Mac-specific code that might dismiss an interstitial?  I'll try to get a build going to investigate, but it might not be ready today.

[Monorail components: UI>Browser>Navigation]

### av...@chromium.org (2017-06-06)

Offhand, no.

This might be related to the "#2" case in https://bugs.chromium.org/p/chromium/issues/detail?id=703655#c19, which would be exciting since that's the one I couldn't repro with logging.

### cr...@chromium.org (2017-06-06)

Ah, nice.  That gives us a bit of a lead.  My build is still going, but maybe I can look closer tomorrow if you don't see an explanation yet.

There must be something about the failed navigation attempt from the opener that dismisses the interstitial on Mac only.  And it *does* look specific to the case that the popup is cross-process from the opener, which in the example happens because https://www.google.com is the default search provider.  It also works for https://docs.google.com, which is a hosted app.  It does not work for https://csreis.github.io, which stays in the same process as the opener.

### cr...@chromium.org (2017-06-07)

Sigh.  I've got a debug build, but I can't repro it there.

I also can't repro it in a clean profile on Mac Canary, even testing on versions 61.0.3121.0, 61.0.3122.0, and 61.0.3123.0.  (I think I was using 61.0.3122 yesterday when I saw it.)

I did just get it to repro on 61.0.3123.0 in a profile with lots of other things in it.  For reference, both PlzNavigate and TopDocumentIsolation were disabled.  Also, the reason that switching back to the opener tab helps (per https://crbug.com/chromium/729105#c6) is that we apparently throttle script tasks in background tabs, so the timeouts in the script weren't consistently firing when the new tab is visible.  However, it's still not a reliable repro there, and I'm not sure what else I'm missing.

We certainly want to track this down, but I'll need to find some more reliable way to see it in practice to find out what's causing it.



### cr...@chromium.org (2017-06-07)

Aha!  I finally found why it wasn't reproing, and it's pretty subtle.  You have to be signed into Google, which causes the www.google.com page to have some extra subframe commits on notifications.google.com.  It *also* matters that we throttle the www.google.com page when it's the background page, so that these subframes don't commit until you switch tabs to make the interstitial visible.  If you time it right, the subframes will commit while the interstitial is showing.

The crazy thing is that we don't delete the interstitial in this case, but rather we just call RenderWidgetHostView::Show() on the page hidden behind the interstitial's overlay.  That means the interstitial page is still around (hence the URL and title corresponding to it), but we show the underlying current RenderFrameHost instead.

The bug appears to be in EnsureRenderFrameHostVisibilityConsistent, which jam@ added in r457626 (though I think that was a refactor of code from lfg@?).  That doesn't take into account the case that an interstitial is showing, and so we call Show() on the current RFH when it commits (via CommitPendingIfNecessary()) even though it's not supposed to become visible.

We should update it to know about interstitials, and we should add an invariant somewhere that you can't call Show() on a RenderWidgetHostView of a RFH while it's hidden behind an interstitial.

From looking at the code, I don't see any reason for this to be Mac specific.  I also threw together a much simpler repro case that doesn't require google.com or signing in-- it just uses a subframe commit while viewing the interstitial.  I'll upload it and test it on other platforms tomorrow, since I need to run.

### cr...@chromium.org (2017-06-08)

Here's a simpler repro which works reliably on Mac.  Just paste it into DevTools on a page, and use any interstitial-inducing URL that you want to show in the address bar.

f = document.createElement("iframe"); f.src = "http://tests.netsekure.org/slow.php?seconds=5"; document.body.appendChild(f);  location.href="https://expired.badssl.com";

Note that there's no need for the window.open or history.back call.  You just need a new subframe to commit (AUTO_SUBFRAME, not MANUAL_SUBFRAME) after the interstitial is showing.  That will trigger a Show() call on the underlying RenderWidgetHostView.

Apparently RenderWidgetHostViewMac must behave differently here than other platforms, since the repro doesn't work on Windows, Linux, or ChromeOS.  The Mac version appears to let the Show() call take precedence over the interstitial's visible RenderWidgetHostView.

(Side note: I'm seeing that Aw Snap on Windows Canary that I mentioned in https://crbug.com/chromium/729105#c8.  Still no crash dump, so I should take a look at it in a debugger.)

### cr...@chromium.org (2017-06-08)

mbarbella@: I think this might warrant Medium severity now that it's reliable.  It's not High since it still shows the "Not Secure" / strikethrough, only works for URLs that trigger interstitials, and is Mac-specific, but it's at least fairly easy to do.

### lf...@chromium.org (2017-06-08)

I've tried to cleanup the code around the EnsureRenderFrameHostVisibilityConsistent before, but that wasn't easy or straightforward, and I couldn't come up with a solution that was better than what we currently have so I ended up abandoning the efforts there.

This code was added to fix https://crbug.com/chromium/522795, see also https://crbug.com/chromium/401859 and the comments on RenderWidgetHostImpl::RendererExited.

The main problem is that once a renderer dies, the browser process destroys the RenderWidgetHostView. Since the RenderWidgetHost's visibility is updated by the RenderWidgetHostView, that stops happening for crashed renderers.

That means so when a tab is focused/unfocused (WebContentsImpl::{WasShown,WasHidden} gets called), the list of RenderWidgetHostViews won't include RenderWidgetHostViews associated with the RenderWidgetHosts on crashed renderers. At this point, the visibility between WebContents and RenderViewHost becomes inconsistent.


### sh...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-09)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-10)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-06-14)

The crash seems like only a stack-overflow.

### cr...@chromium.org (2017-06-16)

clamy@, can you take a look at the repro steps in https://crbug.com/chromium/729105#c13 when running with PlzNavigate (--enable-browser-side-navigation)?  The URL spoof described in this bug will only occur on Mac, but on all platforms the subframe should commit in the background after the interstitial is showing.

That's not happening in PlzNavigate.  We get to NavigationRequest::CommitNavigation for the subframe's URL, then the renderer sends the stream request and we get to ResourceDispatcherHostImpl::OnBeginRequest for the stream URL, but we never get to RenderFrameImpl::DidCommitProvisionalLoad.  I don't see how something in the IO thread would know that an interstitial is showing, so I'm not sure why the subframe navigation isn't completing.  Do you know why it's failing?

I ask because this is causing my test for the URL spoof fix to time out in PlzNavigate in https://codereview.chromium.org/2938313002/.  It's possible I could disable the test in PlzNavigate since the URL spoof itself doesn't repro there, but this seems like unexpected behavior that could indicate a bug of its own.  I'd like to understand it more before sweeping it under the rug.  :)

### cl...@chromium.org (2017-06-16)

@creis: I've tried to reproduce the issue, pasting f = document.createElement("iframe"); f.src = "http://tests.netsekure.org/slow.php?seconds=5"; document.body.appendChild(f);  location.href="https://expired.badssl.com";

Both with and without PlzNavigate, the commit of http://tests.netsekure.org/slow.php?seconds=5 is blocked by Mixed Contents check.

I switched to the https version of the URL, and in both cases the iframe commits. I don't see a difference in behavior between PlzNavigate and non PlzNavigate. I was testing on trunk by the way.

What I did see though is that devtools wouldn't respond when I hit enter in the console in one case in PlzNavigate, but that might have been because the interstitial was already showing. I will confirm.

### cl...@chromium.org (2017-06-16)

Ok so that doesn't happen without PlzNavigate. Without PlzNavigate, even if the interstitial is showing, I can repeat the command in DevTools and create how many iframes I want.

However, when PlzNavigate is enabled, I can't have the console execute JavaScript when the intersitial is showing. I think this is because of the RenderFrameDevToolsAgentHost. In its PlzNavigate version, we buffer messages while the frame is navigating, so I suspect we won't be sending them while the instertitial is showing (since the main frame is navigating). This may have changed with dgozman's recent patches, but it doesn't appear to.

I don't think this is related to the issue you were seeing though. I'll try to patch the CL and see if I can understand the test timeout.

### cl...@chromium.org (2017-06-16)

I have patched your CL and ran it with PlzNavigate and the test doesn't time out for me. (I'm testing on Linux).

### cl...@chromium.org (2017-06-16)

Ah my bad, I didn't notice the test was disabled when PlzNavigate is enabled. Will try again.

### cl...@chromium.org (2017-06-16)

Ok so now that I have re-enabled it on PlzNavigate it does indeed time out, and I think that's working as intended.

When we start showing the interstitial page, we also ask the ResourceDispatcherHost to block all requests from frames of the page. (https://cs.chromium.org/chromium/src/content/browser/frame_host/interstitial_page_impl.cc?gsn=TakeActionOnResourceDispatcher&l=862).

So when the request for the blob url needed to commit the subframe comes in, it is identified as a request from the frame and block by the ResourceDispatcherHost (https://cs.chromium.org/chromium/src/content/browser/loader/resource_dispatcher_host_impl.cc?dr=CSs&l=2286). Which is want I believe.

Of course, with sufficiently bad interleaving that doesn't work -> like if the interstitial is shown just after the subframe requested the resource. And it could break when we switch to a Mojo stream to request the body of the resource (ie I have 0 idea how kinuko & folks implemented this).

### cr...@chromium.org (2017-06-16)

#27: Thanks.  I think that confirms that I should just disable the test in PlzNavigate, at least for the time being.  Agreed that there may be races where it's still possible to commit, and we may want to think about how to test that.

(I guess I can see the reasoning for blocking the requests, and hopefully this will all be moot when we refactor interstitials in https://crbug.com/chromium/448486.)

### bu...@chromium.org (2017-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/adca986a53b31b6da4cb22f8e755f6856daea89a

commit adca986a53b31b6da4cb22f8e755f6856daea89a
Author: creis <creis@chromium.org>
Date: Fri Jun 16 19:12:11 2017

Don't show current RenderWidgetHostView while interstitial is showing.

Also moves interstitial page tracking from RenderFrameHostManager to
WebContents, since interstitial pages are not frame-specific. This was
necessary for subframes to detect if an interstitial page is showing.

BUG=729105
TEST=See https://crbug.com/chromium/729105#c13 of bug for repro steps
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2938313002
Cr-Commit-Position: refs/heads/master@{#480117}

[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/interstitial_page_impl.cc
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/interstitial_page_impl.h
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/interstitial_page_impl_browsertest.cc
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/navigator_delegate.h
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/frame_host/render_frame_host_manager.h
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/adca986a53b31b6da4cb22f8e755f6856daea89a/content/browser/web_contents/web_contents_impl.h


### cr...@chromium.org (2017-06-17)

The fix should be in 61.0.3133.0, though the Mac Canary hasn't updated yet for me to verify.  If it looks good on Monday I'll request a merge.

### ch...@gmail.com (2017-06-17)

Verified on Chromium 61.0.3134.0 on Mac. Thanks Charlie for the quick fix. 

### sh...@chromium.org (2017-06-18)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-06-19)

Thanks for confirming!  I've also verified it in today's 61.0.3135.0 Mac Canary. 
 Requesting merge to M60.

I've also confirmed that the spoof is possible in 59.0.3071.104 (Mac Stable), since it was introduced in r457626.  awhalley@: Do you think this qualifies for a stable merge to M59?  (It allows showing attacker content under an interstitial-inducing URL, only on Mac.)

### sh...@chromium.org (2017-06-19)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@google.com (2017-06-21)

This change meets for the bar and is approved for merging into M60 (build 3112)

### bu...@chromium.org (2017-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c958784507ff188871ddbe78461876aa8463d3cd

commit c958784507ff188871ddbe78461876aa8463d3cd
Author: Charles Reis <creis@chromium.org>
Date: Thu Jun 22 15:27:53 2017

Don't show current RenderWidgetHostView while interstitial is showing.

Also moves interstitial page tracking from RenderFrameHostManager to
WebContents, since interstitial pages are not frame-specific. This was
necessary for subframes to detect if an interstitial page is showing.

BUG=729105
TEST=See https://crbug.com/chromium/729105#c13 of bug for repro steps
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2938313002
Cr-Original-Commit-Position: refs/heads/master@{#480117}
Review-Url: https://codereview.chromium.org/2954503003 .
Cr-Commit-Position: refs/branch-heads/3112@{#442}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}

[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/interstitial_page_impl.cc
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/interstitial_page_impl.h
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/interstitial_page_impl_browsertest.cc
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/navigator_delegate.h
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/frame_host/render_frame_host_manager.h
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/c958784507ff188871ddbe78461876aa8463d3cd/content/browser/web_contents/web_contents_impl.h


### aw...@chromium.org (2017-06-27)

The panel decided to award $500 for this bug!

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/729105?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Interstitials, UI>Browser>Navigation, UI>Browser>Omnibox>SecurityIndicators]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087965)*
