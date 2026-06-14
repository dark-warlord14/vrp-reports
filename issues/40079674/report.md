# Security: Cache-based SOP-Bypass for Images

| Field | Value |
|-------|-------|
| **Issue ID** | [40079674](https://issues.chromium.org/issues/40079674) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>SVG |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2014-06-04 |
| **Bounty** | $2,000.00 |

## Description

Hello,

I've got a cache-based SOP-bypass for images in the current up-to-date versions of Chrome:

In essence, I can bypass the SOP restrictions to load any protected image the victim has access to (like from private gallery albums etc.) and exfiltrate it to my attacker origin, as long as the image is served without anti-cache headers. So basically it boils down to a SOP-bypass that makes use of image caching to bypass SOP checks. It doesn't matter if the image is served over https or http.



In what Browser/OS/Platform/Version?

	* Current up-to-date Chrome on Windows and Mac (for example on my Mac it's Version 35.0.1916.114)



Here are the steps to reproduce (I've set up a demo on two domains for you to see it in action):

1) Open (in Chrome) the victim's "secret photo album" at http://0xbeef.de/secret/index.html (login using HTTP Auth with user "test" and password "secret"). 

	* Note that this could also be a cookie based auth: I've tested that also, but here for simplicity it's HTTP auth - either way, the folder http://0xbeef.de/secret/ is protected including the victim's secret image to exfiltrate http://0xbeef.de/secret/secret.jpg



2) Open in another tab/window the page controlled by the attacker at http://christian-schneider.net/exploits/chrome/SOP_Image_Cache.html

	* This page uses SVG as well as Canvas to "embed" the secret image cross-origin and strip it as dataURL and echoes it via alert and a textarea. This is just for you to easily verify the exploit by copying the dataURL content from the textarea into some <img src="...."> in order to see that this really is *the* secret image, the attacker has accessed from the victim's login, effectively bypassing the SOP for canvas-images *without* triggering a "tainted canvas" security exception. 

	* The point is that the exploit uses the <object> tag *before* dynamically fetching the same image referenced from within the SVG and effectively exploits that the image cache does not enforce the SOP when it is embedded into an SVG using xlink. Eventually <img> would also work to "populate" the cache instead of just <object>.

	* Using other ways to embed cross-origin images and exfiltrate them using Canvas result in a "tainted canvas" security exception. But this way works ;)


Real world exploitation scenarios would either know the image URLs or simply brute force (for ascending numbers in image file names in protected galleries for example) to secretly exfiltrate private photo albums or other "secret" document images from the victims (like online banking charts of private portfolios or alike). The only "requirement" for the attacker is that the image is not served with anti-caching headers, which would otherwise effectively prevent the cache-based image SOP-bypass. But this "requirement" holds true for most protected photo albums or alike, which could be leaked that way... At least when a minimal caching period is allowed.

Another exploitation scenario is for the attacker to check wether the victim is logged in with some sites or not in case the sites serve different images or not depending on the logged-in state.


In case of questions using the above demonstration, please contact me (see below)…


I hope that the given information helps you to enhance the security of your products and I'm happy to further assist you in solving this vulnerability and/or retesting possible solutions/patches. 



Best Regards,
Christian

-- 

Christian Schneider
Software Developer, Whitehat Hacker & Trainer

Twitter:						@cschneider4711
Email:						mail@Christian-Schneider.net
Web Application Security Blog:		www.Christian-Schneider.net


## Attachments

- [Screen Shot 2014-06-05 at 01.24.12.png](attachments/Screen Shot 2014-06-05 at 01.24.12.png) (image/png, 981.0 KB)

## Timeline

### ch...@gmail.com (2014-06-04)

Also note that other ways of trying this without SVG result in a "tainted canvas" exception, like this: http://christian-schneider.net/exploits/chrome/Without_SVG.html

The Without_SVG.html example tries it without SVG and it fails to exfiltrate the secret image by triggering the "tainted canvas" security exception. In contrast, the exploit at http://christian-schneider.net/exploits/chrome/SOP_Image_Cache.html effectively exfiltrates the secret image...

### pa...@google.com (2014-06-04)

When I copy and paste your data: URL, I just get a gray rectangle (which is what we expect from a tainted canvas). So you can exfiltrate a gray square, but not a real image.

http://christian-schneider.net/exploits/chrome/SOP_Image_Cache.html shows a gray rectangle, then the alert, then the textarea with the data: URL in it.

http://christian-schneider.net/exploits/chrome/Without_SVG.html doesn't seem to work at all?

### ch...@gmail.com (2014-06-04)

On Windows it also works using Crome "Version 35.0.1916.114 m" (Stable)

### ch...@gmail.com (2014-06-04)

yep, sorry I uploaded a more detailed explaining SOP_Image_Cache.html and so you tried while I was refining the exploit. It is important to use the two buttons I've now introduced to better understand how the caching thing works.

### ch...@gmail.com (2014-06-04)

Without_SVG.html  is expected to not work at all (tainted canvas) and SOP_Image_Cache.html works using the two steps go1() and go2()

### ch...@gmail.com (2014-06-04)

Attached you find the screenshot for the working exploit when victim is logged-in with  http://0xbeef.de/secret/index.html and visits http://christian-schneider.net/exploits/chrome/SOP_Image_Cache.html 

### pa...@chromium.org (2014-06-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-06-05)

The proof of concept now works; I was able to get the data: URI to show real pixels this time instead of just a grey rectangle.

### pa...@chromium.org (2014-06-05)

tsepez, pdr, schenney: do you know of someone who could take this bug on?

### pd...@chromium.org (2014-06-05)

Excellent report, thank you for filing this.

I'll dig into this ASAP (working on other P1 bugs for the remainder of today though).

### ch...@gmail.com (2014-06-06)

You're welcome... Thanks for developing a great browser! I'm glad to help.

Feel free to test your fixes against the two URLs above... I'll keep them online and just added immediate rendering of the exfiltrated image (instead of the alert), so that no copy/paste of the data:URI is required for quicker testing/validating of your fixes.



Typical exploitation scenarios for the attack would be to:

* Exfiltrate secret images (protected photo albums, online banking portfolio charts, in-browser documents like scan images, ...) as long as they are at least cacheable for a short period (seconds).

* "Logged-in with" checking to determine if a victim is currently logged in with some service (by simply trying to exfiltrate some logo or alike only accessible in the authenticated web pages)

* "History stealing" by modifying the attack to selectively omit the attacker pre-populating the browser cache (remove the object tag for example) and thus the exploit only triggers when victim's browser has already visited a non-secret image of the site to check before (i.e. then it's a history match).

### pd...@chromium.org (2014-06-07)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-06-07)

Just as a small side note: Out of research I've made a quick test with GMail attachments: 

The GMail image attachments of received mails are served with a

     content-disposition:attachment; filename="secret.png"

response header. Due to the type of attack where the image is loaded from within an SVG, it is even possible to exfiltrate the GMail image attachments from logged-in GMail victims (I've tested this with a dummy pentesting account). Fortunately the attacker has to know the "th" id URL parameter (which attackers hopefully don't - so no real danger for GMail). 

But this demonstrates that for the embedding of images into SVG, the "content-disposition" response header is not relevant/checked, as though GMail attachments are served with this header, the above attack was able to exfiltrate the emailed image attachment.



### pd...@chromium.org (2014-06-08)

Narrowed this down to not properly handing resources pulled out of the memory cache.

@tsepez/security team, please cc me on crbug.com/381017.

### in...@chromium.org (2014-06-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-06-08)

ok added you.

### pd...@chromium.org (2014-06-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-06-13)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=176084

------------------------------------------------------------------
r176084 | pdr@chromium.org | 2014-06-13T03:22:36.319984Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/css-import.css?r1=176084&r2=176083&pathrev=176084
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/image-with-css-import.svg?r1=176084&r2=176083&pathrev=176084
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceFetcher.cpp?r1=176084&r2=176083&pathrev=176084
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/image-wrapper.svg?r1=176084&r2=176083&pathrev=176084
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/svg-image-with-cached-remote-image-expected.html?r1=176084&r2=176083&pathrev=176084
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/svg-image-with-css-import-expected.html?r1=176084&r2=176083&pathrev=176084
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/svg-image-with-cached-remote-image.html?r1=176084&r2=176083&pathrev=176084
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/svg-image-with-css-import.html?r1=176084&r2=176083&pathrev=176084
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/image-wrapper-with-no-image.svg?r1=176084&r2=176083&pathrev=176084

Enforce SVG image security rules

SVG images have unique security rules that prevent them from loading
any external resources. This patch enforces these rules in
ResourceFetcher::canRequest for all non-data-uri resources. This locks
down our SVG resource handling and fixes two security bugs.

In the case of SVG images that reference other images, we had a bug
where a cached subresource would be used directly from the cache.
This has been fixed because the canRequest check occurs before we use
cached resources.

In the case of SVG images that use CSS imports, we had a bug where
imports were blindly requested. This has been fixed by stopping all
non-data-uri requests in SVG images.

With this patch we now match Gecko's behavior on both testcases.

BUG=380885, 382296

Review URL: https://codereview.chromium.org/320763002
-----------------------------------------------------------------

### pd...@chromium.org (2014-06-13)

Requesting a merge into all channels (particularly for crbug.com/382296).

### in...@chromium.org (2014-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2014-06-13)

Approved, but please let it bake a bit more on canary before merging.  Let's target for merge Monday or early Tuesday.

### ke...@chromium.org (2014-06-16)

Is this fixed or are there more changed needed?

### pd...@chromium.org (2014-06-16)

The bug here has been fixed, only the merge is left to do.

matthewyuan asked me to wait until today to do the merge. I will be merging this in a few hours, just waiting on https://crbug.com/384989 to be confirmed as not related to this patch.

### bu...@chromium.org (2014-06-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=176225

------------------------------------------------------------------
r176225 | pdr@chromium.org | 2014-06-16T17:14:48.514011Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/resources/image-wrapper.svg?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/svg-image-with-cached-remote-image-expected.html?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/svg-image-with-css-import-expected.html?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/svg-image-with-cached-remote-image.html?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/svg-image-with-css-import.html?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/resources/image-wrapper-with-no-image.svg?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/resources/css-import.css?r1=176225&r2=176224&pathrev=176225
   A http://src.chromium.org/viewvc/blink/branches/chromium/1985/LayoutTests/http/tests/security/resources/image-with-css-import.svg?r1=176225&r2=176224&pathrev=176225
   M http://src.chromium.org/viewvc/blink/branches/chromium/1985/Source/core/fetch/ResourceFetcher.cpp?r1=176225&r2=176224&pathrev=176225

Merge 176084 "Enforce SVG image security rules"

> Enforce SVG image security rules
> 
> SVG images have unique security rules that prevent them from loading
> any external resources. This patch enforces these rules in
> ResourceFetcher::canRequest for all non-data-uri resources. This locks
> down our SVG resource handling and fixes two security bugs.
> 
> In the case of SVG images that reference other images, we had a bug
> where a cached subresource would be used directly from the cache.
> This has been fixed because the canRequest check occurs before we use
> cached resources.
> 
> In the case of SVG images that use CSS imports, we had a bug where
> imports were blindly requested. This has been fixed by stopping all
> non-data-uri requests in SVG images.
> 
> With this patch we now match Gecko's behavior on both testcases.
> 
> BUG=380885, 382296
> 
> Review URL: https://codereview.chromium.org/320763002

TBR=pdr@chromium.org

Review URL: https://codereview.chromium.org/333273006
-----------------------------------------------------------------

### ke...@chromium.org (2014-06-16)

[Empty comment from Monorail migration]

### pd...@chromium.org (2014-06-16)

[Empty comment from Monorail migration]

### pd...@chromium.org (2014-06-19)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

Congratulations - $2000 for this report ($1000 for the report + $1000 bonus for report quality/PoC). 

We'll credit you in the M36 release notes as "Christian Schneider". Someone should contact you in the next two weeks to arrange payment. If you haven't heard anything, please update this bug or contact me directly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
          *********************************

### ti...@chromium.org (2014-07-15)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-07-15)

wow, thx!! ;)

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-15)

Lifting view restriction so that Christian can reference in his blog (fix rolled out in M36).

### ti...@chromium.org (2014-09-17)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/380885?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>SVG]
[Monorail mergedwith: crbug.com/chromium/381017]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079674)*
