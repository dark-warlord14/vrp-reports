# Security: Google Chrome <any version> Extensions Web Accessible Resources Bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40083512](https://issues.chromium.org/issues/40083512) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Reporter** | l3...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2016-01-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Every chrome extension has a manifest.json file, which holds a 'web\_accessible\_resources' field. This field states every 'internal' resource of the extension that can be accessed via the web. For this PoC we will focusing on the Adblock Plus extension (URL: <https://chrome.google.com/webstore/detail/adblock-plus/cfhdojbkjhnklbpkdaibdccddilifddb>).  

So the web\_accessible\_resources of Adblock Plus is only the 'block.html' page.  

Now, lets see what happens when we try

to open an iframe to 'options.html' (options.html is the settings page of Adblock Plus, and it is not in the web\_accessible\_resources) - We are getting the error: "Denying load of chrome-extension://cfhdojbkjhnklbpkdaibdccddilifddb/options.html. Resources must be listed in the web\_accessible\_resources manifest key in order to be loaded by pages outside the extension."

Now, lets open an iframe to 'block.html'.  

AND THEN, lets call a JS function that JUST changes the source of the iframe to 'options.html'  

BOOM! it works.  

The only exception that is being thrown is this: "Uncaught TypeError: chrome.extension.getBackgroundPage is not a function".

The reason for this is that when the source of an iframe is a page which is allowed in the 'web\_accessible\_resources' field, a JS function is able to change it to a non-allowed page.

**VERSION**  

Chrome Version: [47.0.2526.106 m] stable, but it works on earlier version too.  

Operating System: Windows 10 x64, but it works on earlier Operation systems too (I have tested on Win7 64 and 32 bit).

**REPRODUCTION CASE**  

Please watch this private PoC video: <https://www.youtube.com/watch?v=vKshCUGAnRc> and the 3 included html files - one without the 'magic' - without the function that causes the security bug, one with the function the causes the security bug and one with 2 iframes - iframe with the function and iframe without.  

Basicly, all you have to do is:

1. Create an iframe element with 'src=' to an allowed page of the extension.
2. Create an 'onload' event, which calls a javascript function.
3. This function should only change the 'src=' of the iframe to a non-allowed page of the extension.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

-- No Crashes --

Thank you.

## Attachments

- [with_magic.html](attachments/with_magic.html) (text/html, 450 B)
- [before_magic.html](attachments/before_magic.html) (text/html, 171 B)
- [with_and_without.html](attachments/with_and_without.html) (text/html, 764 B)

## Timeline

### ri...@chromium.org (2016-01-13)

Thanks for the detailed report!

meacer@, could you give some guidance on what the impact of this bug might be (and who might be good to look at a fix? I'm guessing clickjacking type attacks for tricking users into changing extension settings?

### ri...@chromium.org (2016-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-13)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-01-14)

Oops, it looks like meacer@ is out this week, mind taking a look at this, asargent@?

### as...@chromium.org (2016-01-14)

Sure, I'll take a look. 

### as...@chromium.org (2016-01-15)

BTW, rickyz: the main security risks I'm aware of are laid out at the documentation for web_accessible_resources:

https://developer.chrome.com/extensions/manifest/web_accessible_resources

"Prior to <when we added the web_accessiable_resources feature> all resources within an extension could be accessed from any page on the web. This allowed a malicious website to fingerprint the extensions that a user has installed or exploit vulnerabilities (for example XSS bugs) within installed extensions. Limiting availability to only resources which are explicitly intended to be web accessible serves to both minimize the available attack surface and protect the privacy of users."


### ri...@chromium.org (2016-01-15)

Ah, thanks for the pointer, asargent@. I'm going to mark this one as medium severity then.

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-01-15)

Note that the fingerprinting aspect here is irrelevant because the exploit requires a web accessible resource (and one is all you need to fingerprint the extensions).  I'm also not sure how severe the increased attack surface is - we provide very little functionality to extension iframes in web pages for exactly this reason (and the capabilities are the same from any resource loaded in the web page's iframe).  I'm not sure how much damage an attacker could do by loading a non-WAR within an iframe.

Though we should absolutely fix this, I think it's probably only Severity-Low.  asargent@, wdyt?

### l3...@gmail.com (2016-01-15)

Hi, I just wanted to add a possible attack vector/method using this security issue:
One can add his site to the Adblock Whitelist, or change a certain setting.
In addition, whenever an extension interacts with the system internal files, clickjacking to a non-web_accessible_resource page might be very dangerous.
There is a reason why a certain page (like the 'options.html' page of the Adblock Plus extension) are not accessible through the web. Think of any currently existing extension which interacts with an internal setting or file. a non-web_accessible_resource page of this extension might expose or leak very sensitive info about the user.

### rd...@chromium.org (2016-01-15)

@10 those are interesting attacks, but I'm a little confused.  Again, an iframed extension page (WAR or not) doesn't have many powers, by design (which is why the getBackgroundPage function fails - we don't allow the chrome.extension API [or most others] in an "unblessed" context).  If a website could *really* modify extension options from an unblessed context, it seems like a bug in the extension that could already be exploited - e.g., the extension isn't validating data/senders from chrome.runtime.sendMessage, which could be called by anything already.  Am I missing something?

Of course, I'm not saying this isn't something that should be fixed (it absolutely is a bug, and thanks again for the find!) and not saying that it's not a security vulnerability - just trying to correctly address the severity (and, again, even Severity-Low means that there *is* a security bug, and we need to fix it). :)

### as...@chromium.org (2016-01-15)

@11 In a simple example I tried, the context in the mistakenly navigated iframe was unblessed and no privileged extension APIs were available. The only remaining risk I thought of so far are situations where for some reason a supposedly non-web-accessible extension page uses messaging to request the background page do some privileged operation, and the background page isn't careful to check both the tab url and sender url in the MessageSender information that came with the message. I'd expect this to be fairly rare though since the obvious thing is to just use the extension APIs directly. 



### as...@chromium.org (2016-01-15)

+cc mkwst

Mike -

This bug report demonstrates that if the initial URL of an iframe in some third-party origin page points at an extension page listed in web_accessible_resources, but then the iframe's src attribute is changed to an extension page which isn't listed, chrome will then allow that resource to load (I've confirmed this). If the initial URL of the iframe is a non-allowed page, then we do the right thing and the resource load is blocked. 

Is this a bug in Blink, or are we doing this wrong in the extension resource loading code? Our current implementation for making extension resources web accessible is to send an "Access-Control-Allow-Origin: *" header for any extension resources that are specified in the web_accessible_resources list in the extension manifest (at the end of extensions/browser/extension_protocols.cc). 

I've tested a local patch where for urls that should *not* be web_accsessible I send either an "X-Frame-Options: SAMEORIGIN" header or add "frame-ancestors 'self'" to the Content-Security-Policy header, and that does seem to fix this bug. Does this sound like the right fix to you?


### as...@chromium.org (2016-01-15)

actually cc mkwst for real - Mike, please see what I just wrote in https://crbug.com/chromium/576867#c13

### mk...@chromium.org (2016-01-18)

Where are you doing the check for loading the content into the frame? My intuition would be that this needs to be part of the navigation chain, and might be a regression based on the OOPIF work that's ongoing. CCing creis@.

> I've tested a local patch where for urls that should *not* be web_accsessible I
> send either an "X-Frame-Options: SAMEORIGIN" header or add "frame-ancestors
> 'self'" to the Content-Security-Policy header, and that does seem to fix this
> bug. Does this sound like the right fix to you?

Do we allow these pages to be opened in popups? If so, these headers won't help.


### cr...@chromium.org (2016-01-20)

@15: I don't think the OOPIF code has changed anything about how web_accessible_resources are verified in default Chrome.  Our changes would likely only affect this if --site-per-process or --isolate-extensions were passed at startup.

Also, I think you're right about popups being a concern.  XFO and CSP don't seem like the right way to implement this.

@13: I'm missing part of your explanation.  What prevents the non-web-accessible-resources from being requested today?  (Something must disable them by default, if Access-Control-Allow-Origin makes them work.)

I would have expected something in ResourceRequestPolicy::CanRequestResource and/or a browser-side equivalent.  Maybe that check is assuming that the frame's own page is initiating the load, when the load is actually coming from another frame (possibly in a different window).

### as...@chromium.org (2016-01-20)

Ok, I looked at the code a bit more and it looks like our existing code for deciding whether to allow resource loads is in the appropriately named "AllowExtensionResourceLoad" function in extensions/browser/extension_protocols.cc

(https://code.google.com/p/chromium/codesearch#chromium/src/extensions/browser/extension_protocols.cc&l=324)

Tracing through that, I also found this interesting comment in extensions/browser/url_request_util.cc:

  // Extensions with web_accessible_resources: allow loading by regular
  // renderers. Since not all subresources are required to be listed in a v2
  // manifest, we must allow all loads if there are any web accessible
  // resources. See http://crbug.com/179127.

(https://code.google.com/p/chromium/codesearch#chromium/src/extensions/browser/url_request_util.cc&rcl=1453235893&l=88)

I wonder if this bug is fallout from that.



### cr...@chromium.org (2016-01-20)

[+nasko for https://crbug.com/chromium/576867#c17]

Ah, I'd blocked that memory out.  Sigh, backwards compatibility...  Maybe there's still a way to distinguish based on the frame that's initiating the navigation?

### lg...@chromium.org (2016-01-22)

According to the severity guidelines, we should theoretically aim for 48 (pre-stable, about to go to stable) if there's something to fix.

asargent@: That comment seems wrong‽ [1] states that only whitelisted loads are allowed.

The logic in the documentation is more like:

    if (extension->manifest_version() < 2 && !WebAccessibleResourcesInfo::HasWebAccessibleResources(extension)) {
      *allowed = true;
    } else if (!WebAccessibleResourcesInfo::HasWebAccessibleResources(extension)) {
      // This case can be collapsed into the third case if IsResourceWebAccessible() returns false when web_accessible_resources is not in the manifest.
      *allowed = false;
    } else {
      *allowed = IsResourceWebAccessible(extension, resource_root_relative_path);
    }

Can't we just change the logic to that?
(We might break use cases, but we'd be aligning better with documented API guarantees.)

[1] https://developer.chrome.com/extensions/manifest/web_accessible_resources#availability

### as...@chromium.org (2016-01-22)

@19 If I understand the history correctly from comments on https://crbug.com/chromium/179127 and https://chromiumcodereview.appspot.com/12457042 , I think the problem is that enough developers got this wrong that we decided implementing the documented policy would break too many extensions. Instead it seems we aimed for a policy more like "any resource listed in web_accessible_resources can be loaded by 3rd party content, and subresources like images/js/css/etc. are transitively allowed to be loaded if they are being requested by a page listed in web_accessible_resources". But it seems we got the implementation of that a little wrong, and I'm investigating if we can do better. 

Re: priority and timeline to get a patch, see comments 11 and 12 from Devlin and I if you haven't already. (I am actively working on this, but multiplexing with other ongoing work).


### na...@chromium.org (2016-01-22)

The context is that we wanted to have *any* resource listed in web_accessible_resources, but we had a bug. You correctly identified that any HTML document listed in web_accessible_resources was allowed to include any subresources without them being explicitly listed. In the CL you pointed to, I tried to lock this down, but enough extensions broke that I had to revert the lockdown. This is why it was listed as a requirement in some future manifest v3.

What should not be allowed though is navigating to another HTML document that is not listed in web_accessible_resources. This is a bug and should be fixed.

### as...@chromium.org (2016-01-27)

I may have tracked down where the bug is happening. In the extensions renderer code we have a function called ResourceRequestPolicy::CanRequestResource, and to decide if a non-web-accessible resource request should be allowed it calculates a variable called "is_own_resource" to try and determine if this is a request for a sub-resource (an image, script file, etc.) by one of the extension's own pages. 

https://code.google.com/p/chromium/codesearch#chromium/src/chrome/renderer/extensions/resource_request_policy.cc&l=86

It calculates that by comparing the origin of |frame_url| to the extension's base url. This works correctly for sub-resources, but unfortunately isn't correct for frame navigations. In the case of frame navigations, the |frame_url| will be the url we are transitioning *from*. 

This is why in the described attack, it works to start with a frame to a web-accessible url, and then navigate it to one that isn't supposed to be accessible. 

Consider this scenario:

An extension which has:
public.html   (only item listed in web_accessible_resources)
private.html


<some other origin>/attack.html
-frame1 with src="chrome-extension://<extension id>/public.html"
-frame2 with src="chrome-extension://<extension id>/private.html"

The resource load for frame1 will currently succeed because public.html is in  web_accessible_resources, but the resource load for frame2 will not because "about:blank" will be the |frame_url| during the call to ResourceRequestPolicy::CanRequestResource, and that's not same origin as the extension. However if we then navigate frame1 to "chrome-extension://<extension id>/private.html", inside ResourceRequestPolicy::CanRequestResource |frame_url| will be "chrome-extension://<extension id>/public.html" whose origin is a match for the extension. 

I've looked around a little at ways to tell the difference between frame navigations and subresource requests inside ResourceRequestPolicy::CanRequestResource, but it's not clear to me if we have enough information there. I also looked to see if we have the right information in the browser side check in ExtensionProtocolHandler::MaybeCreateJob, but so far haven't found anything (the referrer of the URLRequest seems to be empty, or we could possibly have used that to distinguish frame navigations and subresource requests). 

nasko or others: any advice on the right approach here?


### na...@chromium.org (2016-01-27)

Thanks for digging this out! I have to poke around it a bit more to see if there is a better way to solve this, but a simple fix would be to look at the PageTransition. Navigations in subframes are marked AUTO_SUBFRAME or MANUAL_SUBFRAME.

### as...@chromium.org (2016-01-27)

FYI, looks like the |transition_type| in the request for the private page has core type of LINK, not AUTO_SUBFRAME or MANUAL_SUBFRAME, and has a qualifier of CLIENT_REDIRECT.

### l3...@gmail.com (2016-02-10)

Hi there, I have possibly detected another bug which is kinda related to this one.
I have submitted it under bug #585969.

Cheers,
@l33terally

### ra...@chromium.org (2016-02-18)

nasko/asargent: any updates here? Thanks!

### as...@chromium.org (2016-02-18)

I was hoping nasko might have another suggestion, since as far as I could tell what he suggested in https://crbug.com/chromium/576867#c23 doesn't work. 

### cr...@chromium.org (2016-02-18)

Nasko is out this week, but I'm taking a brief look.

Looking at ResourceRequestPolicy::CanRequestResource, I'm not clear what the policy is supposed to be for subframes.

Suppose you're on chrome-extension://<extension id>/public.html.  We've determined that it's allowed to load non-web-accessible subresources like images, and CanRequestResource allows that.  But is it allowed to load non-web-accessible iframes if it does so in its own code?

If so, we have to approach this from a different angle and distinguish which frame is requesting the navigation.  If a frame in the extension itself is requesting it, then the current logic is correct and the non-web-accessible document is loaded into the target iframe.  If some other non-extension frame is requesting it (as in the attack), we have to block it.  I don't know if that information is easily available or not.

It's simpler if web-accessible pages are NOT allowed to load non-web-accessible iframes (though this risks some of the compatibility issues Nasko mentioned in https://crbug.com/chromium/576867#c21).  In this case, we can just identify if the resource is being requested for loading within a frame or not, and we can work out the details of comments 23-24.

Hopefully we can do the latter.  It sounds like the PageTransition might not be set properly (or early enough) if you're seeing LINK for a subframe request.  Looks like we're getting it from the NavigationState in RenderFrameImpl::willSendRequest.  Maybe we need an update to RenderFrameImpl::didStartProvisionalLoad?

Also, what is the PageTransition value for non-navigation subresource requests, like images?

### l3...@gmail.com (2016-02-24)

Hi, is there anything new? Thanks!

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-03-03)

Just so the CC's are aware, here is another similar bug: 589237

### l3...@gmail.com (2016-03-09)

Just checking in - are there any updates regarding this security issues? Thanks in advance :=)

### cl...@chromium.org (2016-03-25)

asargent@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### l3...@gmail.com (2016-04-11)

@asargent - No progress on this bug for 3 months, I would love to help in any other issue that you may face. What is the status on this submission?

### na...@chromium.org (2016-04-12)

I'll take a poke at this in the next few days. As per offline chat, asargent@ will help with writing up an automated test case for this and I will help investigate if we can find a way to fix it either renderer side or browser side.

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-04-19)

Ok, here's a test to aid development/debugging: https://codereview.chromium.org/1895233004

also handing off bug ownership to nasko

### na...@chromium.org (2016-04-21)

I've finally had a chance to look into this. The problem is likely introduced by a CL of mine long time ago - https://codereview.chromium.org/55163006. It added allowing for the resource request to proceed if it was a navigation, but missed to check whether the resource is present in web_accessible_resources. The fix should be something along these lines:

diff --git a/extensions/browser/url_request_util.cc b/extensions/browser/url_request_util.cc
index c7321eb..a471e2f 100644
--- a/extensions/browser/url_request_util.cc
+++ b/extensions/browser/url_request_util.cc
@@ -23,6 +23,8 @@ bool AllowCrossRendererResourceLoad(net::URLRequest* request,
                                     const Extension* extension,
                                     InfoMap* extension_info_map,
                                     bool* allowed) {
+  DCHECK_EQ(extension->url(), request->url().GetWithEmptyPath());
+
   const content::ResourceRequestInfo* info =
       content::ResourceRequestInfo::ForRequest(request);
 
@@ -48,10 +50,13 @@ bool AllowCrossRendererResourceLoad(net::URLRequest* request,
     return true;
   }
 
-  // If the request is for navigations outside of webviews, then it should be
-  // allowed. The navigation logic in CrossSiteResourceHandler will properly
-  // transfer the navigation to a privileged process before it commits.
-  if (content::IsResourceTypeFrame(info->GetResourceType()) && !is_guest) {
+  // If the request is for navigations to web_accessible_resource outside of
+  // GuestView, then it should be allowed. The navigation logic in
+  // CrossSiteResourceHandler will properly transfer the navigation to a
+  // privileged process before it commits.
+  if (content::IsResourceTypeFrame(info->GetResourceType()) && !is_guest &&
+      WebAccessibleResourcesInfo::IsResourceWebAccessible(extension,
+                                                          resource_path)) {
     *allowed = true;
     return true;
   }
@@ -87,10 +92,11 @@ bool AllowCrossRendererResourceLoad(net::URLRequest* request,
 
   // Extensions with web_accessible_resources: allow loading by regular
   // renderers. Since not all subresources are required to be listed in a v2
-  // manifest, we must allow all loads if there are any web accessible
-  // resources. See http://crbug.com/179127.
+  // manifest, we must allow all subresource loads if there are any web
+  // accessible resources. See http://crbug.com/179127.
   if (extension->manifest_version() < 2 ||
       WebAccessibleResourcesInfo::HasWebAccessibleResources(extension)) {
+    DCHECK(!content::IsResourceTypeFrame(info->GetResourceType()));
     *allowed = true;
     return true;
   }

asargent@, would you mind combining it with your test and getting it committed? I suspect this will not be the final version, but at least shows the idea of what needs to be fixed.
Thanks!

### sh...@chromium.org (2016-05-04)

asargent: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-18)

asargent: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2016-05-24)

Oops, sorry, I had stopped following this bug. From comments #9 and #11, it sounds like this has no security implications - not even for fingerprinting (please correct me if I'm mistaken). Based on this, I'm removing the security labels and making this public, though either way, friendly ping on getting the fix + test landed :-)

### l3...@gmail.com (2016-05-24)

Sorry, I have to disagree. By allowing an iframe to be opened with a page that is not in the web_accessible_resources scope, a clickjacking attack can be performed.

For example, lets take a look at the latest version of the famous AdBlock Plus extension.
In the past, the web_accessible_resources contained the 'block.html' page, but now, because of security issues, the 'block.html' was removed from there. Using this *security vulnerability* I am able to perform a clickjacking attack against users and make them add values to AdBlock's 'block.html' text area.

This issue is almost six months old. It is clearly a security issue with a low to moderate (medium) risk level because of clickjacking, regardless the fact that some pages that are loaded using this vulnerability are unblessed.

If I may, let me quote rdevlin comment from the 15 of January this year:
"Of course, I'm not saying this isn't something that should be fixed (it absolutely is a bug, and thanks again for the find!) and *not saying that it's not a security vulnerability*".

Thanks.

### ri...@chromium.org (2016-05-24)

Hm, I had assumed based on https://crbug.com/chromium/576867#c12:

"the context in the mistakenly navigated iframe was unblessed and no privileged extension APIs were available"

that it wasn't possible to perform any privileged actions with clickjacking. Is there some other attack I'm missing here?

### ri...@chromium.org (2016-05-24)

(Or to take the adblock plus example, can tricking a user into adding values to the block.html textarea cause settings to be modified even though privileged extension APIs are unavailable?)

### l3...@gmail.com (2016-05-24)

Please look at this PoC video I have made: https://youtu.be/ALpQTi_ty_c

Thanks

### as...@chromium.org (2016-05-24)

FWIW I do think it's reasonable to consider this a security vulnerability, albeit a relatively low risk one. 

A few of us have been working on a fix for this as a part of a class of related bugs that all share the same problem in the code, and hopefully we'll have something to land before too long. 

### ri...@chromium.org (2016-05-24)

Strange, I wasn't able to reproduce this on current stable (50.0.2661.102) and up. As mentioned, I get:

common.js:65 Uncaught TypeError: chrome.extension.getBackgroundPage is not a 
function

implying that the iframed page doesn't have access to privileged APIs. What version of Chrome did you test this on?

Anyway, reraising to low since there are apparently conditions those privileged APIs are available - it would be useful to work out what the difference between the video and my attempts to repro was.

### l3...@gmail.com (2016-05-25)

This is my chrome version:
Version 50.0.2661.102 m
 
Google Chrome is up to date.

### sh...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### l3...@gmail.com (2016-05-29)

OK, this security vulnerability is half a year old. It opens a path to a severe clickjacking attack, sort of CSRF attack and a lot of options to hurt people's extensions. I don't know why the priority to this bug is so low.
As for a fix - Correct me if I'm wrong, but a patch should check the context from within the iframe source is being changed, or the destination it is being changed. If the destination is not a web_accessible_resource - deny it.

### bu...@chromium.org (2016-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5cf9d45c437b7b2d899e46f2f324c147a2743eb7

commit 5cf9d45c437b7b2d899e46f2f324c147a2743eb7
Author: nasko <nasko@chromium.org>
Date: Wed Jun 01 05:34:56 2016

Disallow navigation to documents not explicitly listed as web accessible.

The existing check for web accessible resources is inadequate and allows
navigations to non-whitelisted pages to succeed. This patch ensures that
the document is listed explicitly in the manifest when a navigation is
performed to it.

BUG=576867

Review-Url: https://codereview.chromium.org/2007133004
Cr-Commit-Position: refs/heads/master@{#397066}

[modify] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/chrome/browser/extensions/extension_protocols_unittest.cc
[modify] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/chrome/browser/extensions/extension_resource_request_policy_apitest.cc
[add] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/chrome/test/data/extensions/api_test/extension_resource_request_policy/iframe_navigate.html
[add] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/chrome/test/data/extensions/api_test/extension_resource_request_policy/some_accessible/manifest.json
[add] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/chrome/test/data/extensions/api_test/extension_resource_request_policy/some_accessible/private.html
[add] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/chrome/test/data/extensions/api_test/extension_resource_request_policy/some_accessible/public.html
[modify] https://crrev.com/5cf9d45c437b7b2d899e46f2f324c147a2743eb7/extensions/browser/url_request_util.cc


### bu...@chromium.org (2016-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a4a128d5c500528e70139c14c51bb326fe357746

commit a4a128d5c500528e70139c14c51bb326fe357746
Author: nasko <nasko@chromium.org>
Date: Wed Jun 01 05:38:51 2016

Disable IframeNavigateToInaccessible test on Site Isolation FYI bots.

BUG=576867
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2026163002
Cr-Commit-Position: refs/heads/master@{#397068}

[modify] https://crrev.com/a4a128d5c500528e70139c14c51bb326fe357746/testing/buildbot/filters/isolate-extensions.browser_tests.filter
[modify] https://crrev.com/a4a128d5c500528e70139c14c51bb326fe357746/testing/buildbot/filters/site-per-process.browser_tests.filter


### na...@chromium.org (2016-06-02)

l33terally@gmail.com, can you confirm the bug no longer repros for you in 53.0.2756.0 and alter?

### l3...@gmail.com (2016-06-02)

Hi @nasko,
Can you supply a link to this version? I'm currently on the roads.

### na...@chromium.org (2016-06-02)

This is the latest canary release for Mac and Windows as of today. Just restarting a Canary instance should have picked up the update or open chrome://help/ to force a check for updates.

### l3...@gmail.com (2016-06-02)

Hi @nasko, I can confirm that this vulnerability is no longer working under version 53.0.2756.0

After recieving the bounty, is it OK if I'll write a post about this vulnerability on http://FogMarks.com?

Thanks.

### na...@chromium.org (2016-06-02)

Adding timwillis@ who is in charge of the bounty program and can answer those types of questions.

In the meantime I will close this one as fixed. Thanks!

### l3...@gmail.com (2016-06-02)

Awesome, thank you!

In the updates page on googlechromereleases.blogspot.com please add the following caption:
@l33terally (FogMarks.com)

Thanks again for helping me keep Chrome users safe! :-)

### ti...@google.com (2016-06-02)

Hello - let's take this to the reward panel and see if it meets the threshold for reward and credit in our release notes. 

We do prioritize bugs on the voting panel by severity, so it might take a few weeks for this one to bubble up to the top of the agenda, as it's a low severity issue. Feel free to update this bug or ping me at timwillis@ in a few weeks if you want an update.

As for writing about it - go ahead. This bug has been open for so long that it would be unfair to ask you to wait any longer. The access to this bug is now public, so feel free to link/share this bug on your post for more context.

### as...@chromium.org (2016-06-16)

[Empty comment from Monorail migration]

### l3...@gmail.com (2016-06-27)

Hello, has the reward panel took a decision?

Thanks

### aw...@chromium.org (2016-07-06)

Congratulations!  The panel has awarded $500 for this report.  Many thanks!  It will go in for processing and you should have somebody from our finance team reach out in the next few weeks.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/576867?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/589237]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083512)*
