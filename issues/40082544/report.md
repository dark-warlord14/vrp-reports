# Security: CSS font loading API bypasses CORS

| Field | Value |
|-------|-------|
| **Issue ID** | [40082544](https://issues.chromium.org/issues/40082544) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>WebFonts |
| **Reporter** | sd...@gmail.com |
| **Assignee** | ks...@chromium.org |
| **Created** | 2015-07-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Cross-origin restriction for CSS font loading API can be bypasses with 308 redirector in same origin of the document.

**VERSION**  

Chrome Version: 43.0.2357.134 stable  

Operating System: Windows 7 Professional Service Pack 1

**REPRODUCTION CASE**

1. At first the expected behavior here is as the following URL.  
   
   <http://csrf.jp/chrome/font/expected.html>

This document tries to load a cross-origin font like this.  

var f = new FontFace("newfont", "url(<http://alice.csrf.jp/VeraSeBd.ttf>)", {});  

But the loading error is shown on the console because the font doesn't send an Access-Control-Allow-Origin header.

2. But the flaw I found is the following.  
   
   <http://csrf.jp/chrome/font/unexpected.html>

This document also loads same font as 1) but it's through 308 redirector like this.  

var f = new FontFace("newfont", "url(/http.php?s=308&u=<http://alice.csrf.jp/VeraSeBd.ttf>)", {});  

Then, the font can be loaded with bypassing CORS restriction and the font is successfully applied to the document.

## Timeline

### pa...@chromium.org (2015-07-22)

Assigning to jww to verify.

### mk...@chromium.org (2015-07-22)

+Kenji: One more reason to drop the CORS restriction? :)

### ke...@chromium.org (2015-07-22)

Nope, that horse won't die ;) The CORS restriction was never meant to be hard to circumvent. If you were caught doing this, you would have a hard time convincing anyone that you didn't know. The other aspect that was mentioned to me was that it's also a deterrent for hot linking (it seems that having that for images from the get go would have been appreciated by many). 

### jw...@chromium.org (2015-07-22)

Kenji, are you arguing that this is not a bug? I thought this was as simple as "FontFace requires CORS, but 308 redirect somehow bypasses lack of CORS headers."

### ke...@chromium.org (2015-07-22)

I think it's a bug and it's similar to the other one with SW and fetch. The response should be opaque and therefore not usable (the font shouldn't be used to render the text).

### jw...@chromium.org (2015-07-22)

Cool. Who's worked on these in the past that can take a look? Horo?

### ke...@chromium.org (2015-07-22)

I believe this would be in Sakamoto san field of expertise. I hope I'm right about the opaque aspect.

### pa...@chromium.org (2015-07-23)

So, what are the thoughts as to security severity? Is this a DRM problem or a security problem?

### ks...@chromium.org (2015-07-23)

I think security severity is low. CORS for web fonts is a kind of DRM feature rather than a security feature. Also, one major browser, Safari, does not apply CORS to webfonts at all.

### ks...@chromium.org (2015-07-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-07-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=199364

------------------------------------------------------------------
r199364 | ksakamoto@chromium.org | 2015-07-23T09:20:26.666701Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/webfont/webfont-cors-expected.html?r1=199364&r2=199363&pathrev=199364
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/webfont/webfont-cors.html?r1=199364&r2=199363&pathrev=199364
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/CSSFontFaceSrcValue.cpp?r1=199364&r2=199363&pathrev=199364
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/serviceworker/fetch-request-resources.html?r1=199364&r2=199363&pathrev=199364
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/CSSFontFaceSrcValue.h?r1=199364&r2=199363&pathrev=199364

Webfont fetch should be CORS-enabled even for same-origin URL

Before this patch, webfont request was made with no-cors mode when the
URL of font face was same-origin. However, that same-origin request may
be redirected to another origin.

This patch makes webfont requests use cors mode for (initially)
same-origin requests too, in order to let ResourceFetcher handle
same/cross origin stuff. (This matches how <img crossorigin> works.)

BUG=512678
TEST=http/tests/webfont/webfont-cors.html

Review URL: https://codereview.chromium.org/1250793008
-----------------------------------------------------------------

### ks...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ks...@chromium.org (2015-07-28)

Requesting merge to M45.

### pe...@google.com (2015-07-28)

Approved for M45 (branch: 2454)

### bu...@chromium.org (2015-07-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=199556

------------------------------------------------------------------
r199556 | ksakamoto@chromium.org | 2015-07-28T03:41:00.334348Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/css/CSSFontFaceSrcValue.cpp?r1=199556&r2=199555&pathrev=199556
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/serviceworker/fetch-request-resources.html?r1=199556&r2=199555&pathrev=199556
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/css/CSSFontFaceSrcValue.h?r1=199556&r2=199555&pathrev=199556
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/webfont/webfont-cors-expected.html?r1=199556&r2=199555&pathrev=199556
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/webfont/webfont-cors.html?r1=199556&r2=199555&pathrev=199556

Merge 199364 "Webfont fetch should be CORS-enabled even for same..."

> Webfont fetch should be CORS-enabled even for same-origin URL
> 
> Before this patch, webfont request was made with no-cors mode when the
> URL of font face was same-origin. However, that same-origin request may
> be redirected to another origin.
> 
> This patch makes webfont requests use cors mode for (initially)
> same-origin requests too, in order to let ResourceFetcher handle
> same/cross origin stuff. (This matches how <img crossorigin> works.)
> 
> BUG=512678
> TEST=http/tests/webfont/webfont-cors.html
> 
> Review URL: https://codereview.chromium.org/1250793008

TBR=ksakamoto@chromium.org

Review URL: https://codereview.chromium.org/1256403002
-----------------------------------------------------------------

### ks...@chromium.org (2015-08-07)

This was subtler than I thought. My patch caused multiple regressions (crbug.com/516192, crbug.com/516743). I'm hesitant to merge all the fixes to M45.
Considering the low severity of this bug, I would like to revert r199556 (M45 merge), while trying to fix the regressions in M46.

Requesting revert of r199556 in M45 branch.


### pe...@google.com (2015-08-07)

Approved for M45 (branch: 2454)

### bu...@chromium.org (2015-08-07)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=200151

------------------------------------------------------------------
r200151 | ksakamoto@chromium.org | 2015-08-07T06:54:17.419703Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/css/CSSFontFaceSrcValue.cpp?r1=200151&r2=200150&pathrev=200151
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/serviceworker/fetch-request-resources.html?r1=200151&r2=200150&pathrev=200151
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/css/CSSFontFaceSrcValue.h?r1=200151&r2=200150&pathrev=200151
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/webfont/webfont-cors-expected.html?r1=200151&r2=200150&pathrev=200151
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/webfont/webfont-cors.html?r1=200151&r2=200150&pathrev=200151

Revert 199556 "Merge 199364 "Webfont fetch should be CORS-enable..."

> Merge 199364 "Webfont fetch should be CORS-enabled even for same..."
> 
> > Webfont fetch should be CORS-enabled even for same-origin URL
> > 
> > Before this patch, webfont request was made with no-cors mode when the
> > URL of font face was same-origin. However, that same-origin request may
> > be redirected to another origin.
> > 
> > This patch makes webfont requests use cors mode for (initially)
> > same-origin requests too, in order to let ResourceFetcher handle
> > same/cross origin stuff. (This matches how <img crossorigin> works.)
> > 
> > BUG=512678
> > TEST=http/tests/webfont/webfont-cors.html
> > 
> > Review URL: https://codereview.chromium.org/1250793008
> 
> TBR=ksakamoto@chromium.org
> 
> Review URL: https://codereview.chromium.org/1256403002

TBR=ksakamoto@chromium.org

Review URL: https://codereview.chromium.org/1281843002
-----------------------------------------------------------------

### np...@chromium.org (2015-08-25)

[Empty comment from Monorail migration]

### ks...@chromium.org (2015-08-27)

Fixed in M46.

### ti...@google.com (2015-08-30)

Removing merge-merged-2454 label as this change was reverted.

@ksakamoto - can you please provide the CL that was merged to trunk so we can mark this as completed for M46?

### ks...@chromium.org (2015-08-31)

https://src.chromium.org/viewvc/blink?revision=199364&view=revision is the fix, which is landed before M46 branch.

### ti...@google.com (2015-08-31)

Thanks! This change will roll out with M46 - no merge to M45 required.

### ti...@google.com (2015-10-13)

Our panel decided to reward you $500 for this report.

Panel notes: The panel wasn't sure if this bypassed anything other than DRM, but wanted to err on the side of rewarding in case it does and due to the quality of your reports.

We'll credit you as "sdna.muneaki.nishimura" in our release notes tomorrow. Please update this issue if you'd prefer to use another name for credit. This issue will also receive a CVE shortly and our finance team will be in contact this week to collect payment details. IF that doesn't happen, please contact me directly at timwillis@ or update this bug.

Thanks again!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### sd...@gmail.com (2015-10-13)

Thanks, please use "Muneaki Nishimura (nishimunea)" for the credit.

### ti...@google.com (2015-10-13)

Shall do!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-10-30)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/512678?no_tracker_redirect=1

[Multiple monorail components: Blink>WebFonts, Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082544)*
