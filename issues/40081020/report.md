# It's possible to load chrome-extension:// URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40081020](https://issues.chromium.org/issues/40081020) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | co...@gmail.com |
| **Assignee** | lu...@chromium.org |
| **Created** | 2014-12-16 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36

Steps to reproduce the problem:
1.Add a form element to a page with a named frame as a target.  Set the method as 'post' and the action attribute as any chrome-extension:// URL.
2. Add an input element as a child element of the form so there is a button to click.
3. Click the button.

Note this also works using named windows/frames and calling the open function.  Also it doesn't gain the full privileges of the extension, but this is something I was working on getting to.  I sometimes have a problem of time to work on security research related things, and this is one of those times.  I'm putting this out there now before my downtime, but note I do plan on getting back to this as soon as I'm active again as I'm sure something really bad could come from this.  Also note that to see this work with named windows it's necessary to use an embedded iframe, but it works essentially the same.  I have more issues to bring to the table, but that will be when I'm active again which hopefully wont be long.

What is the expected behavior?
No window should be loaded with a chrome-extension:// or chrome:// URL

What went wrong?
The built in extension which appears in network logs as 'data:text/html,chromewebdata' seems to be the culprit here, especially when calling open with a named window.  Since it is actually an extension it can load extension URLs.

Did this work before? N/A 

Chrome version: 39.0.2171.65  Channel: n/a
OS Version: 
Flash Version: Shockwave Flash 15.0 r0

I've chosen to load chrome-extension://eemcgdkfndhakfknompkggombfjjjeno/main.html here just because it becomes chrome://bookmarks which to me is scary.

## Attachments

- [extensionLoad-testcase-new.html](attachments/extensionLoad-testcase-new.html) (text/html, 237 B)
- [extensionLoad-testcase-mod01.html](attachments/extensionLoad-testcase-mod01.html) (text/html, 249 B)
- [extensionLoad-testcase-alt.html](attachments/extensionLoad-testcase-alt.html) (text/html, 593 B)

## Timeline

### ts...@chromium.org (2014-12-16)

@kalman, care to take a look or re-assign as appropriate?  Thanks.

### ts...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-16)

[Empty comment from Monorail migration]

### co...@gmail.com (2014-12-16)

How would this qualify in terms of the rewards program?  I will be doing additional work on this quite soon, and I believe this could become much more serious and even possibly a full system compromise.  Still digging through the built in extensions, and looking for any way to load these pages with them retaining full privileges.

### [Deleted User] (2014-12-17)

How is this any worse than an iframe to a chrome-extension:// URL?

### me...@chromium.org (2014-12-17)

I think the small additional risk is that you need to check some sort of CSRF token on the extension side? Otherwise any site could theoretically add bookmarks. It sounds like a problem with a specific extension though, not with the extension system.

### [Deleted User] (2014-12-17)

Hm, I'm missing something, but again how is the XSRF threat any worse for this form case vs an iframe?

### me...@chromium.org (2014-12-17)

You are right, it's not.

### [Deleted User] (2014-12-17)

Btw, the web_accessible_resources key is supposed to help with the iframe case. Extensions need to whitelist which pages can be embedded.

It would be a legitimate bug if this post mechanism bypasses web_accessible_resources.

### co...@gmail.com (2014-12-17)

It does bypass web_accessible_resources.  You can load any file that's a part of any extension.

### co...@gmail.com (2014-12-17)

If you want a testcase that shows this off, I'll include a testcase that loads icons from the webstore built in extension which immediately crashes chrome triggering built in debugging breakpoints.  With this method you can load any file in any built in extension.

### [Deleted User] (2014-12-17)

> It does bypass web_accessible_resources 

Ok. Bad.

> I'll include a testcase that loads icons from the webstore built in extension
> which immediately crashes chrome triggering built in debugging breakpoints

That would be very interesting.

### co...@gmail.com (2014-12-17)

This shows a crash as soon as the page attempts to load one of the icons from the webstore extension.  This is still using the post method and a new tab, but this works almost exactly the same using an embedded iframe and calling the open function with a named window.  On the first call to open it denies access based on web_accessible_resources, but then another call to open using the same window name loads the resource just fine.  Like i said it's the built in extension at the URL chrome-extension://idddmepepmjcgiedknnmlbadcokidhoa/index.html(the cannot load URL page) which is at fault, at least when using named frames and calling open.  The form method is something I've used in firefox with similar results, and was surprised to see it work in chrome too :-)

### co...@gmail.com (2014-12-18)

The extension id I mentioned above may be wrong, playing around with a new chromebook I just picked up and I believe it loads a different extension for diagnosing errors.

Here is another testcase using an embedded iframe clearly showing two recurring calls open to load the extension icon.  If you look in the javascript console after the page load, you will clearly see that this way also bypasses web_accessible_resources.

The issue here when using open is that when adding a named window as a second argument it seems to use that window's URL for the security check.  This window shows up as data:text/html,chromewebdata and it obviously has privileges to load anything from chrome-extension:// URLs.

I just thought I should say too, I know I'm new to you guys guys but I've been working with mozilla through their bounty program for over two years now.  I say that to let you know I *hopefully* wont be bringing bugs to the table that aren't legitimate ;-)

### co...@gmail.com (2014-12-19)

I was curious if this should be broken down into two different bugs?  My reasoning for that is that this is obviously two different bypass methods, and with the form method as said it would be possible(with a lot of work) to add or modify existing bookmarks and send data to any other extensions that expects POST data.

My major concern with this originally was that someone could possibly trick the webstore extension into installing a malicious third party extension, but with the built in debugging breakpoints that doesn't seem to be a concern.  Either way this is definitely leading to some nastiness.

### cl...@chromium.org (2015-01-08)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### co...@gmail.com (2015-01-08)

I was going to ask about any updates regarding this factoring in time for the holiday breaks but apparently clusterfuzz beat me to it :-)

Don't count on anything coming from it but I'm going to try to work in the time to look this over more in depth and *possibly* suggest a viable patch, but don't hold your breath.  If something is already close in that regards please let me know.

### [Deleted User] (2015-01-08)

I haven't had a chance to look at it. Just got back from break and it's not top of my list (yet).

### co...@gmail.com (2015-01-08)

I expected as much honestly, you guys and mozilla employees seem to get some nice lengthy breaks.  I don't think this should be shifted in priority because as long as the wrong eyes aren't on this I can't see the leg work to make this more dangerous being done.  In regards to my working on a patch, I'll look it over but my C++ skills lacks when compared with you guys I'm sure.

### cl...@chromium.org (2015-01-30)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### co...@gmail.com (2015-02-05)

Any updates here?  Also thought I would just ask even though this isn't the right place, any inside info on pwn2own and pwnium this year?  I doubt you guys know anything since nothing has been published, but usually by now there's some info floating around.  Playing with my chromebook I realized how valuable this bug may be to gaining a little leverage there.  Just wondering guys, don't bash on me! :-)

### [Deleted User] (2015-02-05)

Still haven't had time to look into it. From memory and skimming over the bug again, the problem is that there is a way to bypass web_accessible_resources. That's only a problem with websites exploiting an extension which relies on web_accessible_resources  being a key part of its security model. Not unrealistic, but unlikely to be something that can own a computer. Not to say it's not worth fixing - (lower side of) medium severity is correctly labeled.

### co...@gmail.com (2015-02-05)

I do agree with the severity rating here so yeah no worries.  I have been able to come up with some very clever things in the past though, so I rarely stop following up on issues that could become bigger.  When the python shell was first added to chrome before you had to explicitly enable it I could launch a version of it which was a bit more scary.  The chromebook has far more extensions and that's where I'll be looking to see if this could get worse, but even if I was lucky enough to find some exploitable memory issues would still have to break out the sandbox for the PPAPI and NaCL stuff.  Hmm I wonder if it's the worth the time digging?  Thanks for your quick response kalman.  I'll try to bring something with more meat to table and actually pique your interest ;-)

### js...@chromium.org (2015-02-06)

I'm bumping down the severity. While this does violate a part of our security model, the sole impact we're aware of is a minor fingerprinting leakage. So, we can't really justify medium-severity, unless there's a demonstration that it can be leveraged for something more serious.

### co...@gmail.com (2015-02-07)

Sounds like a good move, I'll be retouching on this issue here soon with focus being on the chromebook since it has additional built in extensions, but it would be lucky to find anything that would make this bad seeing as the extensions load with partial privileges.  I'll update with anything I find that points to a more security sensitive issue but I believe that's doubtful.

### la...@google.com (2015-08-24)

Adding default Pri-2

### [Deleted User] (2015-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-14)

Hi rdevlin.cronin@ - is still still applicable?

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-08-26)

Revisiting old bugs.

I investigated this a bit.  It's rather strange.  When the form submits, we receive a request to RenderFrameHostImpl::CreateNewWindow() [1] with the target extension url.  This method correctly checks whether or not the site should be able to open the URL through ContentBrowserClient::ShouldAllowOpenURL() [2], which leads to ChromeContentBrowserClientExtensionsPart::ShouldAllowOpenURL() which correctly returns false (since the resource isn't in web_accessible_resources) [3].  This leads to the URL in RenderFrameHostImpl::CreateNewWindow() being re-written to about:blank [4].  So far, so good.

However, we then receive a call to RenderFrameHostImpl::BeginNavigation() [5] with the same target extension url, and that one seems to correctly load.

At this point, it looks like the flaw is in the content layer (we're either not correctly respecting the call to ShouldAllowOpenURL(), or we're missing a second call in the BeginNavigation() stack if the double-navigation is intentional), and I'm a bit out of my depth.

alexmos@, lukasza@, any recommendations?  And/or, volunteers? ; )

[1] https://cs.chromium.org/chromium/src/content/browser/frame_host/render_frame_host_impl.cc?l=3895&rcl=e0bb634deb88ffd35335cf9e4af0f13de4a0bf31
[2] https://cs.chromium.org/chromium/src/content/browser/frame_host/render_frame_host_impl.cc?l=3911&rcl=e0bb634deb88ffd35335cf9e4af0f13de4a0bf31
[3] https://cs.chromium.org/chromium/src/chrome/browser/extensions/chrome_content_browser_client_extensions_part.cc?l=707&rcl=e0bb634deb88ffd35335cf9e4af0f13de4a0bf31
[4] https://cs.chromium.org/chromium/src/content/browser/frame_host/render_frame_host_impl.cc?l=3913&rcl=e0bb634deb88ffd35335cf9e4af0f13de4a0bf31
[5] https://cs.chromium.org/chromium/src/content/browser/frame_host/render_frame_host_impl.cc?l=4123&rcl=e0bb634deb88ffd35335cf9e4af0f13de4a0bf31

### co...@gmail.com (2019-08-26)

I know this is old and kind of a dead issue, but the original security issue here was by using this technique(as it worked then) would allow one to profile installed and possibly exploitable extensions installed in an end users chrome browser.  At the time that was in fact a sec-moderate and payable, but the rating was lowered I believe with a comment that the person originally assigned hadn't even ran the PoC/testcase.

Maybe this should be reviewed again ;)  Either way I'm glad people are getting to this.  Wish I could help more guys but these days are hectic for me to say the least.

### rd...@chromium.org (2019-08-27)

Thanks for the comment!

I'll let one of the folks more familiar with severity ratings weigh in for the final say, but I don't think that just profiling the user's installed extensions is a medium-severity issue (I think low is correct).  While it's true that this could be used in combination with a vulnerability in an extension, we don't currently include extension-introduced vulnerabilities (as opposed to vulnerabilities in the extensions system itself).

If there were a way for the site to run code in the context window (thus gaining access to extension APIs), that would be higher severity, but I don't believe there currently is with this bug.

All that said, it is still absolutely something we should fix!

### co...@gmail.com (2019-08-28)

Give me a little time today, I'm setup to work which is rare.  At one point I do remember having access to extension windows with JS but it has been some years, and I have some other things to look into.  I've been one of the Mozilla guys on and off for years, and this bug right here is what turned me off from trying anything with google for the most part.

This was a medium-severity issue until it was dropped to low at day 58 IIRC.  There's a comment near the beginning about having not even ran the testcase before dropping the rating.  

All good though, at least someone is getting to it finally.  I'll see if I can spread some time around today and look into other things it could lead to or be applied to.  Thanks guys.

### lu...@chromium.org (2019-08-29)

I tried to describe below my understanding of how navigations to a non-WAR extension URL work (based on some experiments and tests).  I'll try to chat with nasko@ about 3.1 below.


1. *local subframe* navigation (iframe.src = ...) is *blocked* via

1.1. *renderer-side*: ChromeExtensionsRendererClient::WillSendRequest sets the URL to chrome-extension://invalid (aka kExtensionInvalidRequestURL) if ResourceRequestPolicy::CanRequestResource says that it cannot be accessed (e.g. non-WAR).  Note that the browser-side ExtensionNavigationThrottle::WillStartOrRedirectRequest has a check whether the extension exists (and this will fail for chrome-extension://invalid).  Note that retaining the renderer-side check above might be important to prevent timing attacks - see the comment from ResourceRequestPolicy::CanRequestResource

1.2. *browser-side*: ExtensionNavigationThrottle::WillStartOrRedirectRequest - blocked by WAR check (but this is only trigerred if the renderer-side check doesn't change the target URL to chrome-extension://invalid)


2. *remote subframe* navigation (iframe.src = ...) is *dropped* via

2.1. *browser-side #1*: RenderFrameProxyHost::OnOpenURL forwards the navigation request to NavigatorImpl::NavigateFromFrameProxy which silently returns because of ShouldAllowOpenURL.

2.1.1. QUESTION: Should ShouldAllowOpenURL checks be based on (more precise) |initiator_origin| rather than |source_site_instance|?  FWIW, I don't see any bugs caused by this today.

2.1.2. QUESTION: Is silently dropping a navigation request a (separate) bug?

2.2. *browser-side #2*: Even after removing the check in 2.1, the navigation is blocked because it is caught by the same check as 1.2 above (WAR check in ExtensionNavigationThrottle::WillStartOrRedirectRequest)

2.2.1. QUESTION: Why do we need both ExtensionNavigationThrottle checks and ShouldAllowOpenURL checks?


3. *main-frame* navigation (e.g. what happens in the bug here) is *incorrectly allowed* via

3.1. *browser-side*: ExtensionNavigationThrottle::WillStartOrRedirectRequest 1) excludes main-frame navigations from some of the checks and 2) fumbles around looking at parents and the ancestor chain instead of looking at the request initiator.  This is why the navigation is incorrectly allowed.

3.1.1. AFAICT the special-casing of main-frame navigations goes all the way back to r398189 (where ExtensionNavigationThrottle was introduced).  I see a comment there saying that "Top-level navigations should always be allowed" [1] and I see that this CL excludes main frames from the throttle [2].

[1] https://codereview.chromium.org/2042483002/patch/80001/90007
[2] https://codereview.chromium.org/2042483002/patch/80001/90001

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### lu...@chromium.org (2019-08-29)

I cobbled together a WIP CL @ https://chromium-review.googlesource.com/c/chromium/src/+/1776854 

I think it is a reasonable CL to land to address the bug at hand, but it seems that some follow-up, clean-up CLs might be required (to avoid duplicating the code [across the ExtensionNavigationThrottle vs ShouldAllowOpenURL] + to avoid initiating the checks multiple times [e.g. in NavigatorImpl::NavigateFromFrameProxy *and* in ExtensionNavigationThrottle]).

### al...@chromium.org (2019-09-11)

Quick thoughts on a couple of questions here:

> 2.1. *browser-side #1*: RenderFrameProxyHost::OnOpenURL forwards the navigation request to NavigatorImpl::NavigateFromFrameProxy which silently returns because of ShouldAllowOpenURL.
> 2.1.1. QUESTION: Should ShouldAllowOpenURL checks be based on (more precise) |initiator_origin| rather than |source_site_instance|?  FWIW, I don't see any bugs caused by this today.

I think that makes sense and seems strictly better.  I guess one question is, are we worried about cases like sandboxed extension iframes that navigate a proxy to an extension's resource.  Seems that this would have an opaque initiator origin and would be subject to stricter checks than if we used the source SiteInstance?

> 2.1.2. QUESTION: Is silently dropping a navigation request a (separate) bug?

That was an intentional change from rewriting the target URL to about:blank, explained in point 3 of the description here: https://codereview.chromium.org/2454563003  At the time, if we modified the target URL to about:blank, it would end up getting ignored and staying in the same RFH, and somehow still navigating to the blocked URL.  This predated PlzNavigate, so it's very likely that this isn't a problem anymore.  Regardless, if we properly blocked this case and showed an error, seems like that'd be even better.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-09-11)

RE: https://crbug.com/chromium/442579#c38: alexmos@: Breaking changes

You are right that the proposed fix is technically a breaking change - after the proposed fix:
1. A web initiator cannot navigate a main frame to a non-WAR extension resource.  This seems uncontroversial - this fixes the security bug here.
2. A sandboxed extension frame cannot navigate a main frame to a non-WAR extension resource.  This seems to be a natural consequence of the fix - opaque origins are distinct from an extension origin.  While we could in theory look at a origin-precursor information here, I think that we should avoid having extension-specific differences in SOP behavior.

I hope that the breakage from this change will be small (i.e. affect no extensions or a small number of extensions).  I also hope that if extension resources truly need to be exposed to additional contexts, then the extension author can relatively easily mark them as web-accessible.

### lu...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/feddf7e33d2a72575d726b832fec22d5887d47cb

commit feddf7e33d2a72575d726b832fec22d5887d47cb
Author: Lukasz Anforowicz <lukasza@chromium.org>
Date: Wed Sep 18 22:13:23 2019

Use |initiator_origin| in ExtensionNavigationThrottle.

Before this CL, ExtensionNavigationThrottle would more-or-less ignore
main frame navigations (except for special-casing some GuestView
scenarios).  This allowed some undesirable navigations as pointed out in
https://crbug.com/442579.  After this CL the throttle continues with
WebAccessibleResources checks even for main frames.

Before this CL, ExtensionNavigationThrottle would check if the target
is one of WebAccessibleResources iff the frame being navigated has an
ancestor that has a different origin than the target of the navigation.
This doesn't work for main frames (which have no parent).  This could
be addressed by also going over opener relationship, but the right fix
here is to directly consider |initiator_origin| (which is trustworthy
and browser-verified).  After this CL, |initiator_origin| is considered.

Applying the throttle checks to more navigations means that the throttle
has to replicate some exceptions from
ChromeContentBrowserClientExtensionsPart::ShouldAllowOpenURL.
Specifically, the throttle needs to ignore navigations ignored by
origins with chrome://, chrome-search:// and devtools:// schemes.

Additionally the changes mean that opaque origins (even if they have
been derived from an extension origin) cannot navigate to
non-WebAccessibleResources.  This requires tweaking the
sandboxed_pages_csp test.

Bug: 442579
Change-Id: Iebc72b05fece9d0936214f5f8e00802b59e84fd1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1776854
Auto-Submit: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/master@{#697794}

[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/browser/extensions/chrome_extensions_browser_client.cc
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/browser/extensions/chrome_extensions_browser_client.h
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/browser/extensions/extension_navigation_throttle_unittest.cc
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/browser/extensions/extension_resource_request_policy_apitest.cc
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/test/data/extensions/api_test/sandboxed_pages_csp/manifest.json
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/test/data/extensions/platform_apps/web_view/load_webview_accessible_resource/embedder.js
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/chrome/test/data/frame_tree/page_with_two_frames_remote_and_local.html
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/extensions/browser/extension_navigation_throttle.cc
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/extensions/browser/extensions_browser_client.cc
[modify] https://crrev.com/feddf7e33d2a72575d726b832fec22d5887d47cb/extensions/browser/extensions_browser_client.h


### lu...@chromium.org (2019-09-20)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-09-20)

GIven that this bug is evaluated as Security_Severity-Low, I don't think we plan to merge the fix to M78 and/or M77.

### sh...@chromium.org (2019-09-21)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-09-25)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-06)

codycrews00@gmail.com - how would you like to be credited in the Chrome release notes?

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### co...@gmail.com (2019-12-08)

Just use my name, Cody Crews.  I've been using it with Mozilla for years, along with maybe a few others ;-)

Thanks guys, possibly more to come.  I've had a hectic time getting to sec research for a while.

### ad...@google.com (2019-12-09)

Thanks codycrews@!

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/442579?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>Navigation]
[Monorail blocking: crbug.com/chromium/883549]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081020)*
