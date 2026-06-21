# chrome://image allows arbitrary images to be navigated to as a trusted chrome page

| Field | Value |
|-------|-------|
| **Issue ID** | [40059921](https://issues.chromium.org/issues/40059921) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>WebUI |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-06-10 |
| **Bounty** | $2,000.00 |

## Description

This was originally reported by ndevtk@protonmail.com in https://crbug.com/chromium/1269049, using a POC of an extension opening a page.

chrome://image fetches an image from the web.  Since it is a chrome:-scheme page, Chrome displays this as a trusted chrome page in the omnibox UI (e.g., try visiting chrome://image/?https://http.cat/200).  This seems very bad (in general).

While web pages can't open these links, extensions can (see the original bug for a discussion on extensions opening various types of pages).  Luckily, extensions cannot directly access this page, nor, in theory, intercept the request.  It also *looks* like this context does not have special webui bindings like chrome.send or sensitive extension APIs, so a malicious image _hopefully_ wouldn't get too much power.  Additionally, we have checks in place to make this harder.  The image is not just downloaded and embedded:

// The sanitized image source provides a convenient mean to embed images into
// WebUIs. For security reasons WebUIs are not allowed to download and decode
// external images in their renderer process. The sanitized image source allows
// external images in WebUIs by downloading the image in the browser process,
// decoding the image in an isolated utility process, re-encoding the image as
// PNG and sending the now sanitized image back to the requesting WebUI.

Even so, this doesn't seem like a good state.

One solution here is obviously to just block extensions from opening chrome://image, but that seems like the wrong fix (since a user tricked into visiting that site via any other method is still shown a "trusted chrome page").  Instead, I can think of two more holistic fixes:

1) Is there a reason chrome://image needs to be on the chrome:-scheme?  (Can / should it be on chrome-untrusted or something else?)  The idea of serving arbitrary web content from chrome:// seems generally risky.  I don't have a good idea about what chrome://image is actually used for, so not sure what would make sense here.  +lukasza@ (security) might have some opinions here.  It looks like chrome://image is used in the NTP, judging from the owners file here [1], so +tluk@ might be able to chime in more on its usage.

2) Is there a reason to allow chrome://image to open as the main frame in a tab?  If it's solely for embedding images in webui, there's no reason we should ever actually need to navigate directly to it.  Can we restrict it (and any other internal-only chrome:-scheme handlers) to not allow navigations?  lukasza@, you're probably the best to answer this one, too.

3) Barring that, at minimum, we should just not badge chrome://image as a trusted chrome scheme page.  This is probably the weakest of the options, since it would still be served from the chrome: scheme, but at least helps.

I'm not sure who the right owner for this is, since I think it would depend on our approach.  Lukasz, tentatively passing to you for now since I think you'll have the most relevant input here on the best direction to go, but we can pass to a webui owner if it looks like the right change is to alter how chrome://image is handled.

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/sanitized_image_source.h;l=35-41;drc=a96295c188bbd51c9ec30a2269183159dda42d40
[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/webui/resources/cr_elements/cr_auto_img/OWNERS;l=1;drc=40f93d183c32660886a5be49734684f45d72ca1e

## Timeline

### es...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### lu...@chromium.org (2022-06-13)

@nasko, can you PTAL to help triage this bug (as somebody most familiar with WebUI in Chrome Security Architecture team)?

FWIW, to me option #2 (disallowing *navigations* to chrome://image...) seemed most appealing.  My initial plan was to try replying with a `X-Frame-Options: DENY` (and researching/hoping something similar can be used to disallow main frame navigations).  This plan seems problematic, because `StartURLLoader` in `content/browser/webui/web_ui_url_loader_factory.cc` populates the HTTP headers in `resource_response` in a provider-agnostic way (i.e. giving `SanitizedImageSource` no control over the HTTP response headers).

My other plan for option #2 was to modify SanitizedImageSource::StartDataRequest to check if the request comes from a WebUI frame.
1) `StartDataRequest` doesn't get/see the `network::ResourceRequest::request_initiator` (i.e. to only allow `chrome://`-scheme initiators) nor `network::ResourceRequest::mode` (i.e. to only allow `kNoCors` and disallow `kNavigate`)
2) `StartDataRequest` doesn't see HTTP request headers (and besides `Sec-Fetch-Site` wouldn't be populate for non-HTTP requests)
3) `StartDataRequest` *does* get/see `content::WebContents::Getter` - I am not sure if this can be used to robustly identify the initiator - I worry that 
        3.1) `WebContents` won't identify the *frame* where the request comes from.  (e.g. I assume that the main frame can be a WebUI frame, but that it can embed an iframe that is not a WebUI frame)
        3.2) `web_contents->GetMainFrame()->GetLastCommittedOrigin()` will return a *previously* committed origin and might not work if `SanitizedImageSource` handles a pending omnibox-initiated, or extension-initiated navigation

[Monorail components: UI>Browser>WebUI]

### nd...@protonmail.com (2022-06-14)

If headers where used it would be good to check for Sec-Fetch-Dest: image to make sure its only used in a image context.

I think this should be on chrome-untrusted:// that is blocked for extensions https://chromium-review.googlesource.com/c/chromium/src/+/3284045
https://chromium.googlesource.com/chromium/src/+/master/docs/chrome_untrusted.md

I noticed it has Google Photos support not sure if everything ending with ".ggpht.com",".google.com",".googleusercontent.com" is safe and if that requires it to be over https and if redirects are not allowed (since google probably has a open redirect)

### nd...@protonmail.com (2022-06-14)

chrome://favicon and chrome://favicon2 should also be labeled as untrusted.
And maybe chrome://userimage/serialized-user-id for chromeos although im not able to verify.

### rd...@chromium.org (2022-06-14)

Just a couple quick additional thoughts:

> If headers where used it would be good to check for Sec-Fetch-Dest: image to make sure its only used in a image context.

That's nifty!  We *might* be able to get away with this for chrome://image if all the consumers are internal and we audit that they only use this in an image.  This probably wouldn't work for chrome://favicon, though (and we'd have to be careful about using it in chrome://favicon2) because those are used by extensions, and they may be (legitimately) using it in other contexts.  For instance, I think it's completely legitimate to fetch() favicon data.  However, if we have a top-frame restriction, I think that still makes sense to enforce.

> chrome://favicon and chrome://favicon2 should also be labeled as untrusted.

This is reasonably straightforward for chrome://favicon2 (though requires updating all the callsites), but is probably not something we can do for chrome://favicon for the same reason as above - it's used by extensions.

### na...@chromium.org (2022-06-15)

+1 to lukasza@'s suggestion of just not allowing navigations to chrome://image. We don't have any expected usage in such a context, so we should not be allowing it. In ideal world, any chrome: URL that we try navigating to should have a corresponding WebUI object (https://crbug.com/chromium/776896) and if we get to that point, we can just plain disallow navigating to any chrome: URL that does not resolve to a corresponding WebUI.

While I'd like to fix this, realistically I won't be able to do it in the near future, so I'm marking this as available. If I get some spare cycles to take a stab at a fix, I will assign it to myself again.

### na...@chromium.org (2022-06-16)

Looking into this further, this part of the annotation[1] is concerning:

setting: "This feature cannot be disabled by settings."

Does that allow this feature to bypass any URL filtering put in place by administrators? It is not clear to me whether SimpleURLLoader goes through the required checks or not.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/sanitized_image_source.cc;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;l=191


[Monorail components: UI>Browser>Navigation]

### nd...@protonmail.com (2022-06-17)

I tried to do a https://chromeenterprise.google/policies/?policy=URLBlocklist for "ndev.tk"

https://ndev.tk/icon.png "ERR_BLOCKED_BY_ADMINISTRATOR"
chrome://image/?https://ndev.tk/icon.png DUCK!

incognito mode says "ERR_INVALID_URL"

### cr...@chromium.org (2022-06-17)

https://crbug.com/chromium/1335567#c8: Thanks for confirming.  That indeed sounds like a policy bypass.

Nasko and I met to discuss this yesterday, and we share significant concerns about the design of chrome://image.  I'm not aware of a way to get arbitrary HTML content shown, but allowing arbitrary images still has a lot of problems (even if polyglots like https://lcamtuf.coredump.cx/squirrel/ don't survive).

Confirmed security issues:
1) Allows users to bypass enterprise policies and view images that should be blocked (per https://crbug.com/chromium/1335567#c8).
2) Allows extensions or social engineering attacks to show attacker controlled images with a chrome:// URL, resulting in a URL spoof (e.g., a privileged chrome:// URL telling the user to call a malicious support number).

Additional risks that would only be one small bug away:
3) It appears likely that the Google bearer token may leak if an attacker can get IsGooglePhotosUrl to return true for a URL under the attacker's control.  For example, I think attacker-controlled scripts may be hosted on googleusercontent.com, and www.google.com/url?q= is a redirector that only sometimes shows an interstitial page.  The validation in IsGooglePhotosUrl seems far from ideal.
4) If any HTML or active content can survive the transcoding, it will run at an extremely high privilege level and could likely escape the sandbox.  This is hopefully unlikely, but I haven't audited how errors or other corner cases are handled.
5) This may allow Sec-Fetch-Site or other header bypasses, where an image might not have been served under normal circumstances.
6) This seems very close to a Site Isolation bypass, putting content from multiple sites into the same chrome://image process.  If any of that content were active, it would be a problem.

It's also concerning that this URL handler is instantiated for the NTP, but it's available for any tab or page to use once a single NTP has been created, even if that NTP has gone away.

I strongly agree that the design of chrome://image should be changed.
* Blocking navigations to the URL seems most important.
* Moving it from chrome:// to chrome-untrusted:// also seems important.
* Would it be possible to not have a URL at all, and instead give the NTP a Mojo API to fetch the transcoded image bytes (e.g., as an ArrayBuffer) for putting into a canvas?  That avoids all of these redirector problems.

In general, this seems to have some of the same problems that the chrome-distiller:// scheme had in https://crbug.com/chromium/991888, which eventually required validating the URL parameter in r693009.  That case involved HTML but was also intended not to allow scripts or other active content.

mahmadi@: Can you help us find an owner familiar with chrome://image for resolving these issues?  I'm assigning to you because you're in the NTP owners list and we suspect this feature is for the NTP, and since we shouldn't leave security bugs unassigned.  Thanks!

[Monorail components: Enterprise Internals>Sandbox>SiteIsolation UI>Browser>NewTabPage]

### nd...@protonmail.com (2022-06-18)

To add to https://crbug.com/chromium/1335567#c4
chrome://download-internals/ (Bypasses enterprise policy)
chrome://extension-icon/ghbmnnjooekpmoecnnnilnnbdlolhkhi/128/1 (Extension icon as trusted)
chrome://app-icon/ (App icon as trusted)
chrome://fileicon/?path= (Not sure)

### nd...@protonmail.com (2022-06-18)

Not sure if the policy is meant to be hard to bypass :/
Also not sure what the rules are if a user can go to chrome:// then they can already run JavaScript in a trusted process.

"Save link as" with a redirect.
Creating an image with a redirect.
If Image is cached.

### cr...@chromium.org (2022-06-21)

burunduk@: Can you help us understand the severity of the policy bypass mentioned in https://crbug.com/chromium/1335567#c8 and https://crbug.com/chromium/1335567#c9?  Are cases like that considered a problem for the URLBlocklist?  Presumably if https://example.com is blocked, we should also block chrome://image?https://example.com as well?

### na...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-06-22)

While the usage of chrome://image is limited to the New Tab Page at the moment, I can see how other WebUI surfaces could start using it for embedding external images. So it's good that we're talking about this security risk now.

Moving chrome://image/ to chrome-untrusted://image seems trivial enough given its limited usage. But to help me understand, how is the case of chrome://image/ different that chrome://favicon2 or chrome://favicon whose usage is a lot more widespread? If these technically pose the same risk, would blocking navigations to these urls be the more pressing and principled fix?


### bu...@chromium.org (2022-06-22)

Not sure how can I help, I worked on something related only three years ago, as my noogler bug was related to URL blocking. Maybe +mnissler@ can give more insights.

From what I know, some enterprises (especially schools when using chromebooks) care a lot about blocking their users to access some content, so for them it could be a severe issue. Also limiting chrome://image to embedded images doesn't sound like a solution, as it would be pretty easy to write a page (or an extension? I didn't get whether it works with extensions or not) which does the embedding.

### ti...@chromium.org (2022-07-01)

From some quick code search it looks like chrome://image is also used by CrOS' personalization app (cc'ing owner cowmoo@) and the nearby share WebUI (cc'ing owner hansberry@). There might be more users.

IIRC, chrome://image needed to be on the chrome:// scheme because chrome:// pages are not allowed to fetch chrome-untrusted:// resources. I'm not aware of any use case where chrome://image needs to be the top-level URL. It's nice for development; but not critical.

Sending external images to requesting WebUIs via Mojo is a neat idea. tluk@ mentioned this is also done for the CrOS background image. I'm not sure if there are performance implications though. I believe we would still like the hosting HTML element be img to keep the current behavior. If that's possible and since chrome://image is mostly used via the cr-auto-img helper [1] switching to Mojo might actually be fairly seamless.

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/webui/resources/cr_elements/cr_auto_img/cr_auto_img.ts;drc=a96295c188bbd51c9ec30a2269183159dda42d40

### dp...@chromium.org (2022-07-01)

A lot of problem and good ideas have surfaced in this discussion, and it is getting a bit hard to follow or track all of them. I think it would be super useful for someone who has a good understanding of the issue to summarize the probelm and potential mitigations, so that we can prioritize them and evaluate them.

I'll just highlight something that Devlin said earlier, since that's what seems the most odd from a design/architecture perspective

> It's also concerning that this URL handler is instantiated for the NTP, but it's available for any tab or page to use once a single NTP has been created, even if that NTP has gone away.

Can we eliminate chrome://image/ completely, and instead have each individual WebUI page that needs that functionality expose it via its own host? Like <img src="chrome://new-tab-page/image?url=...">

And any other pages that needs that functionality would have to expose it from its own host. This seems would bypass a lot of the problems with the current chrome://image/ design.



### ma...@chromium.org (2022-07-01)

+1 to what dpapad proposed in #17. It's nice to be able to conveniently host images via <img> elements rather than using mojom. It shouldn't be much extra work for each WebUI page to host them provided most of the logic is readily available in utilities.

passing on to tiborg@ now that he's back :)

### ma...@chromium.org (2022-07-01)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-07-01)

https://crbug.com/chromium/1335567#c17 I think the issues that maybe should be in different issues are...

Issues from https://crbug.com/chromium/1335567#c9
chrome://image

Bypass URLBlocklist
chrome://image
chrome://download-internals
Open redirect with save link as.

Displays external content as a secure chrome page. (Should prevent top level access)
chrome://image
chrome://extension-icon
chrome://app-icon
chrome://favicon
chrome://favicon2
chrome://userimage/serialized-user-id
chrome://fileicon/?path= (No idea probably not an issue)

### co...@chromium.org (2022-07-06)

ccing two more people that recently worked on chrome://image to support google photos browsing in chrome://personalization WebUI.

https://crbug.com/chromium/1335567#c9 seems relevant for google photos specifically

> 3) It appears likely that the Google bearer token may leak if an attacker can get IsGooglePhotosUrl to return true for a URL under the attacker's control.  For example, I think attacker-controlled scripts may be hosted on googleusercontent.com, and www.google.com/url?q= is a redirector that only sometimes shows an interstitial page.  The validation in IsGooglePhotosUrl seems far from ideal.

Sending internet-downloaded images from to a WebUI via mojom is cumbersome, and loses out on the simplicity of browser caching and inspecting via devtools during development that chrome://image offers. So keeping chrome://image functionality in some way would be very helpful for chrome://personalization.

I'm also in favor of creating a `chrome://personalization/image?url=` handler. Is it then also possible to make sure that this is only called from an `img` tag on `chrome://personalization` domain?

### ck...@chromium.org (2022-07-06)

`chrome://personalization/image` (with analogues for NTP et al.) sounds good to me. I think we could even continue using cr-auto-img by adding a required host attribute (populated with personalization/ntp/whatever for each image).

If we also restrict navigation to these host-specific image URLs, would that be a sufficient fix? I didn't totally follow the discussion about redirects.

### nd...@protonmail.com (2022-07-06)

"make sure that this is only called from an `img` tag on `chrome://personalization`"
Not sure if extensions can modify it but checking for the headers Sec-Fetch-Dest: image and Sec-Fetch-Mode: same-origin might work.

Image should use Cross-Origin-Resource-Policy: same-origin

Feel free to correct me :)

### lu...@chromium.org (2022-07-06)

RE: https://crbug.com/chromium/1335567#c23: ndevtk@: `Sec-Fetch-Site: same-origin`

AFAIK `Sec-Fetch-...` HTTP request headers are only attached to HTTP requests (i.e. I expect them to be missing in WebUI / chrome://... requests).  OTOH, every implementation of mojom::URLLoaderFactory::CreateLoaderAndStart should be able to inspect network::ResourceRequest::request_initiator - hopefully this is plumbed through and available where needed for this bug.

### [Deleted User] (2022-07-16)

tiborg: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2022-07-21)

Can someone please give a bit of detail on how the proposal of adding the image handler to each WebUI will work in practice? The reason chrome://image is usable outside of WebUIs is that we do not remove URLDataSource instances once registered and they live for the rest of the browser process lifetime. They do not check what context the requests are made from, so we tend to rely in practice on chrome: scheme not being requestable by regular renderers. It does mean that anything in the omnibox would just work.

If we still use URLDataSource to serve WebUI specific images, we will still have the same problem unless we solve the URLDataSource lifetime problem.

### nd...@protonmail.com (2022-07-21)

I think the fix was to "inspect network::ResourceRequest::request_initiator" and block the request if its not a trusted origin.
Such navigation's from the omnibox or chrome.windows.create etc would not have a request_initiator of a trusted origin so would get blocked.
This would also mean other chrome:// pages could not use the feature unless added.

You probably want a better explanation so just wait for someone else to reply.

The secure chrome page part of this would be safer as a list of allowed origins.

### dp...@chromium.org (2022-07-21)

> Can someone please give a bit of detail on how the proposal of adding the image handler to each WebUI will work in practice?

@nasko: My thinking at https://crbug.com/chromium/1335567#c17 when I proposed the following

> Can we eliminate chrome://image/ completely, and instead have each individual WebUI page that needs that functionality expose it via its own scheme? Like <img src="chrome://new-tab-page/image?url=...">

was that each individual WebUIController could intercept such requests and drop them if they don't originate from the same WebUI page, such that 'chrome://new-tab-page/image?url=...' only work if requested by another chrome://new-tab-page/ context. I believe this should be possible by leveraging with  the SetRequestFilter() mechanism at [1], but I have not actually tried it locally.


[1] https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/web_ui_data_source.h;l=115-133;drc=ead449e91b32cf231f53fb2f3999413ee06b791a

### dp...@chromium.org (2022-07-21)

> I believe this should be possible by leveraging with  the SetRequestFilter() mechanism at [1], but I have not actually tried it locally.

Perhaps this is not possible currently, since ShouldHandleAccessibilityRequestCallback seems to only receive the path being requested, but nothing about the context making the request.  Not sure how easy it would be to pass the requestor URL to ShouldHandleAccessibilityRequestCallback, or if it is even possible.

### dp...@chromium.org (2022-07-21)

. Perhaps this is not possible currently, since ShouldHandleAccessibilityRequestCallback

Correction: Meant to type "ShouldHandleRequestCallback".

### nd...@protonmail.com (2022-07-21)

https://crbug.com/chromium/1335567#c24 says about request_initiator is the issue that "ShouldHandleRequestCallback" is unable to access this?
Im just going to keep failing at my own report :)

### dp...@chromium.org (2022-07-21)

> https://crbug.com/chromium/1335567#c24 says about request_initiator is the issue that "ShouldHandleRequestCallback" is unable to access this?
> hopefully this is plumbed through and available where needed for this bug.

If we were to follow this approach, then yes it seems that it is not currently plumbed through and available in ShouldHandleRequestCallback().

Having said that, in https://crbug.com/chromium/1335567#c28 I was trying to explain to nasko@ the rationale behind my previous idea, and not necessarily dictate how it should be implemented. There are others in this thread probably more experienced with the network stack that can consider altertative implementations.

The high level idea is to limit "chrome://<foo>/image?url=" responses to requests made by chrome://<foo>/ contexts. Then the fact that the WebUIDataSource for chrome://<foo> stays around even after a WebUI page has been closed would no longer be a problem, because it would be unusable by other contexts anyway. This is currently not possible with the reused chrome://image/ data source.

### [Deleted User] (2022-07-31)

tiborg: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### cr...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-03-22)

Any progress with this?

### ar...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-09)

I merged https://crbug.com/chromium/1453501, about bypassing URLBlockList using chrome://download-internals. It was described several time in the bug. For instance in https://crbug.com/chromium/1335567#c20. This way, this bug keeps the paternity. Maybe we should split it if we think fixing it would require different approaches?


### dp...@chromium.org (2023-06-15)

> This way, this bug keeps the paternity. Maybe we should split it if we think fixing it would require different approaches?

I think is best to keep these bugs separate for now. While they are related, they are not happening beause of the same culprit. In other words, I think each of these would need to be fixed individually anyway.

### nd...@protonmail.com (2023-07-21)

This seems inactive :(

### na...@chromium.org (2024-01-03)

[Navigation triage] Please prioritize fixing this security bug. Our policy[1] for fixing medium severity bugs is current or next milestone, which has been exceeded multiple times since the bug has been filed.

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#TOC-Medium-severity

### ti...@chromium.org (2024-01-04)

Apologies for the inactivity. Admittedly, I don't have the cycles at the moment to provide a fix. Given that SanitizedImageSource has found wider-spread adoption in web UIs, passing this to WebUI owner dpapad to triage further.

### dp...@chromium.org (2024-01-04)

[Comment Deleted]

### dp...@chromium.org (2024-01-04)

> ... but will ask to see if other ongoing efforts can be re-prioritized to make cycles for this

Adding robliao@ as FYI for the scheduling discussion.

### dp...@chromium.org (2024-01-04)

@nasko, @tiborg: I *dont* think I have the cycles for this currently either, but will ask to see if other ongoing efforts can be re-prioritized to make cycles for this. Even so, the main issue here is that we have not identified any fix yet. Beyond an idea I posted in https://crbug.com/chromium/1335567#c28 (and haven't even tried it) are there any other fixes that come to mind?

### ti...@chromium.org (2024-01-04)

It also seems like there are two issues being discussed here:
(1) chrome://image/... can be the top frame and dupe the user into believing arbitrary images are trusted Chrome pages.
(2) chrome://image/... can bypass URL blocklist policies.

I think this bug was originally about (1) only. Let's scope this bug to (1). And file another one for (2) if it is a concern.

For (1), I think the Sec-Fetch-Dest idea proposed in https://crbug.com/chromium/1335567#c3 has merit. If that can be made to work it might be the most seamless since we won't have to touch all users of SanitizedImageSource.

### nd...@protonmail.com (2024-01-05)

I think https://crbug.com/chromium/1335567#c24 says a reason for not using Sec-Fetch and that maybe network::ResourceRequest::request_initiator would work instead.
Regarding bypassing IsGooglePhotosUrl I think <ip>.bc.googleusercontent.com refers to someones google cloud compute server if that allowed dont even need a open redirect.

A basic check would be if the initiator starts with chrome://, chrome-extension:// then allow it otherwise dont.

### nd...@protonmail.com (2024-01-05)

Ah https://crbug.com/chromium/1335567#c2 says `StartDataRequest` doesn't get/see the `network::ResourceRequest::request_initiator` and also allowing extensions is a bad idea.
I have no idea about this ideally you could just use a NavigationThrottle

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/1335567?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>NewTabPage, UI>Browser>WebUI]
[Monorail blocking: crbug.com/chromium/1279611]
[Monorail mergedwith: crbug.com/chromium/1453501]
[Monorail components added to Component Tags custom field.]

### nd...@protonmail.com (2024-05-07)

Any progress with this? been open for a long time Jun 10, 2022.  

As per `chrome://image/?https://http.cat/200` the cat is still a secure chrome page. (Version 126.0.6465.0)

### dp...@chromium.org (2024-05-07)

> Any progress with this? 

Not that I know of. I am un-assigning from  myself as I am not actively working on this, and it would increase the chances of someone else picking this up. Will also bring it up again in prioritization discussions.

### ca...@chromium.org (2024-05-08)

dpapad: Is there someone else you could suggest as owner for this?

### dp...@chromium.org (2024-05-08)

cc'ing robliao to help.

> dpapad: Is there someone else you could suggest as owner for this?

Ideally whoever owns these files should be the primary go-to person/team. Having said that, it seems that these files are now loosely owned (the team that added them is not explicitly marked as an owner AFAICT).

### nd...@protonmail.com (2024-05-09)

Well there's a lot of people in this issue, Anyone want to adopt some `.cc` files :)

### ro...@chromium.org (2024-05-09)

Routing to tiborg to see if we can schedule in migrating some clients like NTP to a more restricted image mechanism as discussed above.

### aj...@google.com (2024-09-16)

new report [issue 366375482](https://issues.chromium.org/issues/366375482) feels like a duplicate of this issue but I would appreciate someone taking a look for confirm

### dp...@chromium.org (2024-09-16)

> new report [issue 366375482](https://issues.chromium.org/issues/366375482) feels like a duplicate of this issue but I would appreciate someone taking a look for confirm

Seems like a duplicate to me as well.

Also it seems that the discussion/investigation here has mostly stalled. From my side, it would be helpful if nasko@ (or someone else from the security team) could chime-in with regards to comments #33 and #47, on whether the proposal would help address the problem and whether it is feasible (serving `chrome://<foo>/image?url=...` requests if they are initiated from within a `chrome://<foo>/` context)

### nd...@protonmail.com (2024-09-17)

I think so for `chrome://image`
`chrome://extension-icon`
`chrome://app-icon`
`chrome://favicon`
`chrome://favicon2`
`chrome://userimage/serialized-user-id`
`chrome://fileicon/`

Comment 6 says about favicon usage with extensions.

Any bugs with `URLBlockList` left would be a separate issue.

### nd...@protonmail.com (2024-09-17)

I know I'm not who your asking just want to see progress on this issue from 2022.

### cr...@chromium.org (2024-09-18)

Yes, we discussed this in the CSA meeting yesterday, and I'll try to chime in while nasko@ is busy. At a high level, checking the initiator is useful (to discourage its use outside of WebUI pages), but it does not seem sufficient for fixing this issue. This is because users can still bypass the blocking policy by opening a WebUI page and then requesting the image from there (e.g., via DevTools if it's available, or by finding a WebUI page with code that can load it for them) to bypass policy. We suspect the image fetching logic for this feature needs to use the same blocking logic as other network requests.

I'm also wondering if [issue 366375482](https://issues.chromium.org/issues/366375482) should be split back out. I don't see any discussion of the `custom_background_image` case in this bug report, in which case the other reporter should get credit for pointing that one out. Do they use the same code under the hood, or does it need a separate fix?

I'm on my way to an appointment, but I can try to do a closer read through both bugs afterward to see if I've missed anything.

### nd...@protonmail.com (2024-09-18)

If its `chrome-untrusted://new-tab-page/custom_background_image?url=https%3A%2F%2Fhttp.cat/200` then yeah not anything to do with this report as that's on `chrome-untrusted://`  

In comment 21 there's multiple ways to bypass the policy this report was not about that as shown in the first comment.  

The initiator patch was assuming the attacker doesn't have physical access to the users device, great to fix both but not enough to block fixing the spoofing attack.

### dp...@chromium.org (2024-09-18)

> We suspect the image fetching logic for this feature needs to use the same blocking logic as other network requests.

I don't have any knowledge about which layer is the blocking logic residing, but the code in question uses `network::SimpleURLLoader::Create()` to create the request [1]. If there is an easy way to respect blocked URLs via this codepath, then this might not be that hard to fix.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/sanitized_image_source.cc;l=269;drc=406947a0f1e0e6b596d387b6b14156f369e8c55d>

### nd...@protonmail.com (2024-09-18)

Makes sense for the enterprise policy to be enforced for every network request made from chromium even in trusted chrome pages.
This seems separate from the original concern I did not know it would be treated as a security issue.

### cr...@chromium.org (2024-09-19)

A few quick updates before I post a larger summary of what's left:

- Per [#comment48](https://issues.chromium.org/issues/40059921#comment48), I've split out the policy blocklist issue into <https://crbug.com/368087667>, along with a potential lead on how to check the blocklist.
- Per [#comment63](https://issues.chromium.org/issues/40059921#comment63), I've split <https://crbug.com/366375482> back out into its own bug. That custom\_background\_image case also has additional issues that need to be addressed.
- The Buganizer migration had incorrectly marked <https://crbug.com/40065551> as a duplicate of this bug (due to <http://b/325072672>), so I split it back out and marked it fixed again, as it was before the migration.

### cr...@chromium.org (2024-09-19)

After [#comment66](https://issues.chromium.org/issues/40059921#comment66), we can narrow the work in this bug to the following issues:

- Navigations to chrome://image should be prevented entirely. This could likely be done with a NavigationThrottle or possibly checking Sec-Fetch-Dest headers.
- Resource requests to chrome://image should verify the initiator of the request is a chrome:// page. Optionally, chrome://image could also be split into separate handlers for each WebUI that needs it and limited to requests from that WebUI, per [#comment18](https://issues.chromium.org/issues/40059921#comment18). Whether it's split or not, the URLDataSource(s) will continue to exist once they're created, so it's important to limit who can request those URLs.

@dpapad: I think your proposal in [#comment59](https://issues.chromium.org/issues/40059921#comment59) covers at least the second bullet, correct? That would help, and we also don't want those pages to be able to navigate to the image URL, for the first bullet.

It may make sense to split out separate bugs for the other affected URLs in [#comment60](https://issues.chromium.org/issues/40059921#comment60), as well as the Google Photos problem brought up in [#comment10](https://issues.chromium.org/issues/40059921#comment10). tiborg@: Feel free to do that if it simplifies the work needed for this bug.

Finally, based on the existence of chrome-untrusted://new-tab-page/custom\_background\_image, I'm curious if we actually can use chrome-untrusted:// for this chrome://image case? (Maybe tiborg@'s concern in [#comment17](https://issues.chromium.org/issues/40059921#comment17) about chrome:// pages requesting chrome-untrusted:// resources has been fixed?)

Hope that helps move this bug towards a fix!

### pe...@google.com (2024-10-26)

tiborg: Uh oh! This issue still open and hasn't been updated in the last 169 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

tiborg: Uh oh! This issue still open and hasn't been updated in the last 184 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### na...@chromium.org (2025-05-23)

[Navigation Triage] tiborg@, can we ensure we are making progress on this issue? It has been open for quite a while now and we should be making consistent progress towards resolving it. Looks like [comment #67](https://issues.chromium.org/issues/40059921#comment67) has some concrete steps that can be taken.

### ti...@chromium.org (2025-07-31)

I'm assigning this to dpapad@ for triage. I'm the original author of chrome://image. But this has become a utility used across [multiple WebUIs](https://source.chromium.org/search?q=cr-auto-img%20-file:%5Eout&sq=-file:%5Eout%2F&start=1) and, thus, should probably be handled at the framework level.

I want to bring attention to my [comment #17](https://issues.chromium.org/issues/40059921#comment17). AFAICT, chrome://image use is mostly wrapped into [cr-auto-img](https://source.chromium.org/chromium/chromium/src/+/main:ui/webui/resources/cr_elements/cr_auto_img/cr_auto_img.ts). This should make it fairly seamless to switch chrome://image for something else, e.g. Mojo, in case this allows us to go with a more robust solution.

> Finally, based on the existence of chrome-untrusted://new-tab-page/custom\_background\_image, I'm curious if we actually can use chrome-untrusted:// for this chrome://image case? (Maybe tiborg@'s concern in [#comment17](https://issues.chromium.org/issues/40059921#comment17) about chrome:// pages requesting chrome-untrusted:// resources has been fixed?)

chrome-untrusted://new-tab-page/custom\_background\_image is iframed on the NTP. Turning each image loaded into WebUIs into an iframe is probably not tractable (due to performance and UX).

### dp...@chromium.org (2025-07-31)

Once again this bug is assigned to me (previously assigned at [comment#44](https://issues.chromium.org/issues/40059921#comment44), unassigned at [comment#53](https://issues.chromium.org/issues/40059921#comment53)), while I don't have cycles to work on this, nor is there someone on the WebUI team I can delegate this to, so no sure how to "triage" properly.

It sounds that we haven't agreed on which team owns this bug, and therefore which team should put it in the OKRs to drive the fix, which sounds like a process failure. For example this bug hasn't been in the WebUI OKRs since filed.

[Comment#67](https://issues.chromium.org/issues/40059921#comment67) has some concrete suggestions, (like *"Navigations to chrome://image should be prevented entirely."*), but also some fairly vague/costly (like "*Optionally, chrome://image could also be split into separate handlers for each WebUI that needs it*"). If we have identified smaller steps that contribute towards fixing this bug, perhaps splitting them off to individual child bugs will make it more likely for someone to prioritize and fix.

> Whether it's split or not, the URLDataSource(s) will continue to exist once they're created, so it's important to limit who can request those URLs.

Would fixing <https://issues.chromium.org/issues/389737044> also help then? This lifecycle issue seems to be coming up quite a bit.

> I want to bring attention to my [comment #17](https://issues.chromium.org/issues/40059921#comment17). AFAICT, chrome://image use is mostly wrapped into cr-auto-img. This should make it fairly seamless to switch chrome://image for something else, e.g. Mojo, in case this allows us to go with a more robust solution

Auditing and updating all users of cr-auto-img to use Mojo APIs instead is far from trivial. Note that there are actually two copies for cr-auto-img, one for Desktop and one for CrOS. You can see uages for each at [1] and [2] respectively, which span a lot of different WebUIs.

[1] <https://source.chromium.org/search?q=%22resources%2Fcr_elements%2Fcr_auto_img%2Fcr_auto_img.js%22%20-file:out%2F%20-file:go%2F%20-file:luci%2F%20-file:third_party%2F%20-file:appengine%2F%20-file:v8%2F%20-file:chrome%2Ftest%2Fdata%2Fwebui&sq=&ss=chromium>

[2] <https://source.chromium.org/search?q=%22resources%2Fash%2Fcommon%2Fcr_elements%2Fcr_auto_img%2Fcr_auto_img.js%22%20-file:out%2F%20-file:go%2F%20-file:luci%2F%20-file:third_party%2F%20-file:appengine%2F%20-file:v8%2F&ss=chromium>

### el...@chromium.org (2025-09-02)

I'll take this one on as an IC project and try to sort it out.

### dp...@chromium.org (2025-09-03)

Feel free to take a look at <https://chromium-review.googlesource.com/c/chromium/src/+/6813891> where I tried to implement a NavigationThrottle, which kind of works but not fully. It prevents direct navigations, but clicking the "reload" button, or restarting the browser with the "Continue where you left off" setting still loads the `chrome://image` URL. Perhaps someone who knows a bit more about this part of the stack can easily tweak the conditions to work as needed.

### el...@chromium.org (2025-09-03)

Thanks! I will have a look and see if I can fix this.

### el...@chromium.org (2026-02-04)

Looking at this one again: I think this makes sense to fix and I'll aim to work on it during the next couple of weeks.

### el...@chromium.org (2026-02-06)

I have read over this bug (in its entirety) and here is a summary of where we are and what I'm going to do.

There are 3 security risks here:

1. Extensions can navigate the main frame to chrome://image/$url to cause $url to be shown as trusted Chrome UI, which creates phishing risk. It's probably also possible to self-phish users in this way somehow.
2. Loads of chrome://image/$url?isGooglePhotos=true cause SanitizedImageSource to send an OAuth bearer token with the request. If an attacker can cause $url to redirect to a host they control, or otherwise read the headers of that request, they can maybe steal a token. The check for which values of $url are allowed is quite loose: the host part of the URL just has to end with one of ".ggpht.com", ".google.com", and ".googleusercontent.com".
3. chrome://image bypasses URL blocklists and similar.

Risk (1) is fixable by forbidding loads of chrome://image that aren't happening in an image context (ie, preventing main-frame and subframe loads of it). That's what the NavigationThrottle approach in #74 is getting at, as well as the proposal around Sec-Fetch-Dest.
Risk (2) is a little harder to deal with. We don't have conclusive proof that this is possible but it seems very likely that it is. The best fix I can think of would be to prevent loading chrome://image with arbitrary URLs when isGooglePhotos=true (i.e. tighten the validation logic) but I don't know if we can tighten it enough to fix the problem.
Risk (3) is not a security bug, but a functional bug in the enterprise policy. We could fix it by causing the URL loader that chrome://image uses to check the blocklist.

There are a couple of approaches available which would be harder / longer-term but which would obviate the need for chrome://image entirely, which would be nice because I don't see how we would fix (2). Those options are:

1. Add a Mojo API which allows WebUIs to fetch a guaranteed-safe image, probably by issuing a request, decoding, and re-encoding, then sending them a data: URL containing the re-encoded image data. This would require changes to <cr-auto-img> to invoke this Mojo API and would maybe be gruesome to integrate into actual image loading, but it would fix the other problems of chrome://image maybe.
2. Allow WebUIs to load images in the normal way (ie make <img> tags with network sources Just Work in WebUIs). From a risk perspective we'd need to have memory-safe decoders to make this doable, otherwise the risk of code execution in WebUI renderers would probably be too high. Unfortunately we'd need memory-safe decoders for *all* the formats that data\_decoder supports, because I think there are cases (eg in Lens) where chrome://image can be used on arbitrary web image URLs.

### or...@chromium.org (2026-02-06)

AFAICT, 2. is only used for the Personalization App/Wallpaper App on ChromeOS. We could move that functionality into their own WebuiDataSource and make it so that those imgs can only be loaded from chrome://personalization-app.

### el...@chromium.org (2026-02-25)

I have a fix for (1) awaiting review: <https://chromium-review.git.corp.google.com/c/chromium/src/+/7561815> - this will also mitigate (3) enough for me not to worry about it.

For (2), I am unsure if there is an actual security bug here - this whole thing seems quite speculative. *If* there's a bug the consequences could be bad, but I am not sure how to get attacker access to the token via that mechanism.

### nd...@protonmail.com (2026-02-25)

Yeah <https://issues.chromium.org/u/1/issues/40059921#comment4> did not confirm it was possible to exploit. The most likely would be bc.googleusercontent.com a service used by Google Cloud customers.
I think why its not been tested is because its not over HTTPS and I didn't want to leak my auth token :)

### nd...@protonmail.com (2026-02-25)

Well its harder to test then expected I would need to setup ChromeOS, Server, Certificate but it seems like it would work just trust me.

### el...@chromium.org (2026-02-25)

You would need to somehow get an SSL certificate for googleusercontent.com though because we refuse to fetch images except over HTTPS, right?

### nd...@protonmail.com (2026-02-25)

It depends if you allow redirects then no otherwise yes might try <https://letsencrypt.org/docs/challenge-types/#http-01-challenge> just getting an server on googleusercontent with https would be a good start to prove impact.

### el...@chromium.org (2026-02-25)

Basically, I think that it is possible to construct hypotheticals for (2), but I can't tell whether it is actually a big problem for real or not. In particular, I don't know how you would cause a request to chrome://image/https://<attacker-controlled>.googleusercontent.com?isGooglePhotos=true to actually be issued after I land <https://chromium-review.googlesource.com/c/chromium/src/+/7561815>. That fix will prevent extensions navigating to chrome://image, and I don't think an extension could run in a webui context that would let it splice a subresource in.

Do you have an attack path in mind?

### nd...@protonmail.com (2026-02-25)

Yeah after the patch since you or extensions cant navigate there it seems fine.
<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/sanitized_image_source.cc;drc=50dbcddad2f8e36ddfcec21d4551f389df425c37;bpv=1;bpt=1;l=71> however having a IsGooglePhotosUrl function that allows URLs that are not Google Photos is not ideal.

### el...@chromium.org (2026-02-26)

It's definitely not, I'll still file a cleanup bug to address that - but not a security bug I think. Thanks!

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Elly [ellyjones@chromium.org](mailto:ellyjones@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7561815>

webui: reject chrome://image loads

---


Expand for full commit details
```
     
    We should never allow navigations to chrome://image; this origin is used 
    exclusively to load external images as subresources in webui. Allowing 
    it in the main frame opens up a phishing vector for extensions that can 
    open a new tab to chrome://image to load chrome://image?<phishing URL> 
    and have the page content (an image) show as "trusted chrome UI". 
     
    To prevent that, this change installs a new navigation throttle 
    (ImageNavigationThrottle) which forbids loads of chrome://image. 
     
    This change is based off dpapad@'s earlier attempt: 
    https://chromium-review.googlesource.com/c/chromium/src/+/6813891 
     
    Bug: 40059921 
    Change-Id: I32d839d793accbc2ed6903ab69203028c7e2f24f 
    Thanks: dpapad, nasko 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7561815 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Commit-Queue: Elly FJ <ellyjones@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590929}

```

---

Files:

- M `chrome/browser/chrome_content_browser_client_navigation_throttles.cc`
- M `chrome/browser/ui/BUILD.gn`
- A `chrome/browser/ui/webui/image/image_navigation_throttle.cc`
- A `chrome/browser/ui/webui/image/image_navigation_throttle.h`
- A `chrome/browser/ui/webui/image/image_navigation_throttle_browsertest.cc`
- A `chrome/browser/ui/webui/image/image_navigation_throttle_unittest.cc`
- M `chrome/test/BUILD.gn`

---

Hash: [ef26f22809c0808f4256dc5fcc9f84d4f84b03b7](https://chromiumdash.appspot.com/commit/ef26f22809c0808f4256dc5fcc9f84d4f84b03b7)  

Date: Thu Feb 26 18:18:17 2026


---

### el...@chromium.org (2026-02-26)

Fixed :) the cleanup bug mentioned in #86 is <https://issues.chromium.org/issues/487938770>.

### aj...@google.com (2026-05-15)

Does the fix also fix the initial report <https://issues.chromium.org/40057884> ?

### nd...@protonmail.com (2026-05-15)

It blocks chrome://image to prevent Google Photos token leaks. Seems unrelated.

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Security UI spoofing.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### nd...@protonmail.com (2026-06-19)

Strange that message didn't say `This payment will be issued by Bugcrowd` wonder who is getting the reward :)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059921)*
