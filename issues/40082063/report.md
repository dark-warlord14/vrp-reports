# Security: CSP does not block svg image in nested iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40082063](https://issues.chromium.org/issues/40082063) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG, Platform>Extensions |
| **Reporter** | ma...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2015-05-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

1. Go to <http://vulnerabledoma.in/csp_svg_set_element> and confirm image is blocked by CSP.
2. Go to <http://vulnerabledoma.in/csp_svg_set_element_frame1.html> . The image is loaded and you can see Google logo.

Due to this bug, an attacker can bypass CSP partially and load arbitrary image in target domain. If attacker can include user's sensitive information as part of image request, attacker can get that information without user interaction.

**VERSION**  

42.0.2311.135 m

## Attachments

- [testext.zip](attachments/testext.zip) (application/zip, 493 B)
- [server.js](attachments/server.js) (text/javascript, 1.3 KB)

## Timeline

### ri...@chromium.org (2015-05-12)

Wow, that's surprising behavior - thank you for the detailed report! Adding mkwst@ who I've seen on some SVG/CSP bugs before.

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### md...@chromium.org (2015-05-12)

Hm, I can't reproduce this with 44.0.2391.0.  The second page appears blank and produces a CSP error message in the console:

    Refused to load the image 'https://www.google.com/images/srpr/logo11w.png?6.56578663344593' because it violates the following Content Security Policy directive: "default-src 'none'". Note that 'img-src' was not explicitly set, so 'default-src' is used as a fallback.

So looks like it's already been fixed since M42?

### ri...@chromium.org (2015-05-12)

For what it's worth, I do see the Google logo in 44.0.2391.0 on my laptop - strange.

### md...@chromium.org (2015-05-12)

Other Chrome engineers also report that they see the CSP violation instead of the Google logo on both 44.0.2391.0 and 42.0.2311.135.  It seems like something odd is happening on your machines.

Can one of you try to reproduce the misbehavior and attach a net-internals log for it?  See https://sites.google.com/a/chromium.org/dev/for-testers/providing-network-details

Thanks

### ma...@gmail.com (2015-05-12)

I found interesting thing. Probably, this bug is around Chrome extensions.

Please install Adblock Plus. You will be able to reproduce this bug.
https://chrome.google.com/webstore/detail/adblock-plus/cfhdojbkjhnklbpkdaibdccddilifddb

### es...@chromium.org (2015-05-13)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-05-13)

Ahhh, nice catch! Can confirm that it doesn't happen for me if Adblock Plus is disabled.

### mk...@chromium.org (2015-05-13)

It would not shock me to find that ABP was screwing with CSP headers. :/

### md...@chromium.org (2015-05-14)

Any thoughts on how to proceed here then?  Do we have a standard way of dealing with security bugs introduced by extensions with >=1e7 users?

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

schenney@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### sc...@chromium.org (2015-05-18)

CSP is not at all my thing. Bringing in benwells@ for extensions, as the comment stream indicates we're letting extensions mess with CSP.

### mb...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-19)

Removing owner so that this gets back into the queue for triage by the security sheriff.

Also, it seems like this has been raised before in https://crbug.com/chromium/244976. Should this really be high severity?

### [Deleted User] (2015-05-19)

We can't really stop extensions from messing with the CSP headers, on principle. It's been discussed before. We can attempt to offer targeted APIs for achieving the same goal without punching through a security hole.

### [Deleted User] (2015-05-19)

Can we remove the restrict-view-securityteam label so adblock plus devs can read the bug?

### se...@gmail.com (2015-05-19)

Can reproduce it with either of following extensions installed, on Chrome 41.0.2272.89 and 44.0.2398.0:

Adblock Plus
Privacy Badger
Awesome Screenshot
Ghostery
AdBlock

Note that Adblock Plus (as most of the extensions in the list) never mess with headers. In fact the CSP header is still set to "default-src 'none'", according to the devtools, but the image is still loaded.

### [Deleted User] (2015-05-19)

OK thanks for looking into it. I guess something in the webRequest API has unintended consequences.

### se...@gmail.com (2015-05-19)

I tracked the issue down, and it is caused by registering a "load" event on the document with the capturing phase:

  document.addEventListener("load", function() {}, true);

I have attached a proof-of-concept extension only running the line above from a content script. This is sufficient to reproduce the issue.

### [Deleted User] (2015-05-19)

Whoa that's crazy. mkwst do you have an idea of how to track this down? It sounds more like an isolated world issue then.

### mk...@chromium.org (2015-05-19)

Interesting. We bypass the main world CSP if we're in an isolated world that has a CSP set (which can be/is blank in most cases). I don't understand why adding a capturing event listener in the isolated world would cause that check to flip out.

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/bindings/core/v8/ScriptController.cpp&sq=package:chromium&type=cs&l=219&rcl=1432037082 is the check.

CCing haraken@ and jochen@, as there was some refactoring in the bindings that might be related (a long time ago)...

### se...@gmail.com (2015-05-19)

I recreated the proof-of-concept page, with nodejs (attached), and played a little around with the issue:

* I wasn't able to bypass CSP checks by registering the event listener with a script on the page.
* The extension must register the event listener before the frame is loaded (I had to move the content script to document_start to reproduce the issue reliably, since the page loads faster locally).
* If using an <img> tag (instead an SVG image) the issue doesn't occur.
* If setting the "xlink:href" attribute directly on the <image> element (instead with <set attributeName="xlink:href>) the issue doesn't occur.
* With less than two surrounding frames the issue doesn't occur.
* With more than two surrounding frames the issue occurs less often.

### jo...@chromium.org (2015-05-27)

This bug was introduced in https://codereview.chromium.org/200923002 which invokes shouldBypassMainWorldCSP in the context of a microtask

in the repro case given here, the img microtask happens to be executed as part of execution of the event handler in the isolated world.

fix here: https://codereview.chromium.org/1153233002

### jo...@chromium.org (2015-05-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195981

------------------------------------------------------------------
r195981 | jochen@chromium.org | 2015-05-27T14:57:16.944524Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/ImageLoader.cpp?r1=195981&r2=195980&pathrev=195981
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Microtask.h?r1=195981&r2=195980&pathrev=195981

Correctly set ScriptState in the image loader microtask

BUG=487155
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/1153233002
-----------------------------------------------------------------

### jo...@chromium.org (2015-05-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195985

------------------------------------------------------------------
r195985 | jochen@chromium.org | 2015-05-27T16:03:17.225847Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Microtask.h?r1=195985&r2=195984&pathrev=195985
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/parser/HTMLScriptRunner.cpp?r1=195985&r2=195984&pathrev=195985
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebKit.cpp?r1=195985&r2=195984&pathrev=195985
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8RecursionScope.cpp?r1=195985&r2=195984&pathrev=195985
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Microtask.cpp?r1=195985&r2=195984&pathrev=195985
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=195985&r2=195984&pathrev=195985
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=195985&r2=195984&pathrev=195985

Correctly keep track of isolates for microtask execution

BUG=487155
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/1161823002
-----------------------------------------------------------------

### cl...@chromium.org (2015-05-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-05-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196007

------------------------------------------------------------------
r196007 | dmurph@chromium.org | 2015-05-27T21:24:43.679658Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/ImageLoader.cpp?r1=196007&r2=196006&pathrev=196007
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Microtask.h?r1=196007&r2=196006&pathrev=196007

Revert of Correctly set ScriptState in the image loader microtask (patchset #1 id:1 of https://codereview.chromium.org/1153233002/)

Reason for revert:
Tree on failure, might be causing the issues w/ leaking

https://code.google.com/p/chromium/issues/detail?id=492829&thanks=492829&ts=1432760699

Original issue's description:
> Correctly set ScriptState in the image loader microtask
> 
> BUG=487155
> R=haraken@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=195981

TBR=haraken@chromium.org,jochen@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=487155

Review URL: https://codereview.chromium.org/1162483002
-----------------------------------------------------------------

### in...@chromium.org (2015-05-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196071

------------------------------------------------------------------
r196071 | jochen@chromium.org | 2015-05-28T16:08:11.913925Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/ImageLoader.cpp?r1=196071&r2=196070&pathrev=196071
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Microtask.h?r1=196071&r2=196070&pathrev=196071

Reland "Correctly set ScriptState in the image loader microtask"

Original review: https://codereview.chromium.org/1153233002/

BUG=487155
R=haraken@chromium.org

Review URL: https://codereview.chromium.org/1163543002
-----------------------------------------------------------------

### jo...@chromium.org (2015-06-02)

For r196071

### jo...@chromium.org (2015-06-02)

[Empty comment from Monorail migration]

### pe...@google.com (2015-06-02)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### pe...@chromium.org (2015-06-02)

Merge approved for m44 branch 2403.

### bu...@chromium.org (2015-06-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196330

------------------------------------------------------------------
r196330 | jochen@chromium.org | 2015-06-02T16:53:16.217043Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/loader/ImageLoader.cpp?r1=196330&r2=196329&pathrev=196330
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/dom/Microtask.h?r1=196330&r2=196329&pathrev=196330

Merge 196071 "Reland "Correctly set ScriptState in the image loa..."

> Reland "Correctly set ScriptState in the image loader microtask"
> 
> Original review: https://codereview.chromium.org/1153233002/
> 
> BUG=487155
> R=haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/1163543002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1146223008
-----------------------------------------------------------------

### ha...@chromium.org (2015-06-17)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

masatokinugawa: shall we pay you using your details that you've registered with the Google Web reward program or would you like us to send you a different registration form? 

### ma...@gmail.com (2015-08-17)

Please use my details that I've registered with the Google Web reward program.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-08)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

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

### va...@chromium.org (2018-11-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-29)

This issue was migrated from crbug.com/chromium/487155?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SVG, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082063)*
