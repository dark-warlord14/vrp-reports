# Security: URL Spoof with http authentication dialog and pdf prompt dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40081962](https://issues.chromium.org/issues/40081962) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth, Internals>Plugins>PDF, Platform>Apps>BrowserTag |
| **Reporter** | ch...@gmail.com |
| **Assignee** | wj...@chromium.org |
| **Created** | 2015-04-29 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

This bug can display a prompt dialog box through a pdf file, under a url of a different origin, which displays an http authentication dialog box.

**VERSION**  

Chrome Version: [42.0.2311.135 ] + [stable]  

[44.0.2384.0] + [trunk build]  

Operating System: [Windows 8, Ubuntu 14.04]

**REPRODUCTION CASE**  

Required software: Web server with support for php.  

Web server should serve content from 127.0.0.1 and 127.0.0.2.  

Enable chrome pdf plugin if it is disabled.

1. Download urlspoof3.html, auth.php, formsubmit.pdf, pdfForm.php and userresponse.php.
2. Host downloaded files on local web server's root folder.
3. Open chrome
4. Visit <http://127.0.0.1/urlspoof3.html>  
   
   <http://127.0.0.1/urlspoof3.html> will load formsubmit.pdf.
5. formsubmit.pdf will display a prompt dialog which will ask user's age.
6. After 2 seconds page will be redirected to <http://127.0.0.2/auth.php>
7. But confirm dialog displayed from <http://127.0.0.1/urlspoof3.html> will remain.  
   
   Authenitication dialog displayed from <http://127.0.0.2/auth.php> will be visible under confirm dialog.
8. Enter a number in prompt dialog and press OK.
9. Wait 5 seconds.  
   
   formsubmit.pdf will submit number typed by user to <http://127.0.0.1/pdfForm.php>  
   
   But this form submission will be not visible through browser UI.  
   
   This form submission request will be visible in web server's access log file.
10. Open a new tab and visit <http://127.0.0.1/userresponse.php>  
    
    userresponse.php will display number typed by user.

\* formsubmit.pdf contains javascript code to display Confirm message box and to submit form. You can view this code by opening formsubmit.pdf in a pdf editor and viewing code for Javascript OpenAction.

## Attachments

- [urlspoof3.html](attachments/urlspoof3.html) (text/html, 181 B)
- [userresponse.php](attachments/userresponse.php) (text/plain, 167 B)
- [formsubmit.pdf](attachments/formsubmit.pdf) (application/pdf, 1.5 KB)
- [pdfForm.php](attachments/pdfForm.php) (text/plain, 81 B)
- [auth.php](attachments/auth.php) (text/plain, 177 B)

## Timeline

### ch...@gmail.com (2015-04-29)

This bug is separated from https://crbug.com/chromium/477278.
Please see https://crbug.com/chromium/482380#c13 of https://crbug.com/chromium/477278.

### cr...@chromium.org (2015-04-29)

Assigning labels based on the previous bug.

@raymes: Can you take a look?

@meacer: Do you think this should be medium or low severity?  In the similar https://crbug.com/chromium/295695, https://crbug.com/chromium/482380#c28 rated it as low because (1) it depends on the victim site showing an interstitial and (2) the prompt is a limited form of a spoof.  In this case, the spoof is a bit more effective against sites that use HTTP auth, since the user is already expecting a dialog for entering a password and they might put it into the wrong dialog.  Tentatively assigning medium severity.

### cl...@chromium.org (2015-04-29)

[Empty comment from Monorail migration]

### ra...@chromium.org (2015-05-01)

[Empty comment from Monorail migration]

### pa...@google.com (2015-05-01)

[Empty comment from Monorail migration]

### ra...@chromium.org (2015-05-04)

Hmm it would be great if someone with more WebContentsImpl knowledge could chime in here. I'm seeing something quite interesting. WebContentsImpl::DidStartProvisionalLoad gets fired during the redirect but it doesn't seem to get further than that, and so I don't think there is anything in the code that will cause the dialogs to disappear by that stage. I guess that the modal credentials dialog prevents it from getting further.

As to why this doesn't happen in other circumstances (e.g. with iframes popping alerts, etc.) usually this jams up the renderer from being able to do anything else since everything is running in the same process. So the redirect will never get hit until the modal dialogs are clicked away. However in our case we have a BrowserPlugin running in a separate process from the embedder so the redirect is running in parallel with the alert dialog.

So my gut feeling is that we will actually see this problem occur with OOPIF as well. I tried to test this theory however it appears that modal dialogs don't work at all when coming from cross-process iframes at present.

### ra...@chromium.org (2015-05-05)

creis: do you have any suggestions regarding #6? Thanks!

### ra...@chromium.org (2015-05-11)

ping

### cr...@chromium.org (2015-05-18)

Sorry, I was out on vacation.  (Really wish there was a OOO setting for crbug.)

Can you point me to the code that puts up the dialog in the PDF case?  It doesn't seem to go through WebContentsImpl::RunJavaScriptMessage, and I don't know where to look.

### ra...@chromium.org (2015-05-19)

No worries :) 

We call WebFrame::callFunctionEvenIfScriptDisabled with alert()/confirm()/prompt().

https://code.google.com/p/chromium/codesearch#chromium/src/content/renderer/pepper/ppb_var_deprecated_impl.cc&ct=xref_usages&gs=cpp:content::%253Canonymous-namespace%253E::CallDeprecatedInternal(PP_Var,%2520PP_Var,%2520unsigned%2520int,%2520PP_Var%2520*,%2520PP_Var%2520*)::result@chromium/../../content/renderer/pepper/ppb_var_deprecated_impl.cc:9065%257Cdef&l=269&gsn=result

### cr...@chromium.org (2015-05-19)

Thanks!  I'll try to catch that in a debugger to see what to suggest.

### cr...@chromium.org (2015-05-19)

I think I see what's happening.  The inner (guest) WebContents is showing the dialog via WebContentsImpl::RunJavaScriptMessage (contrary to what I said in https://crbug.com/chromium/482380#c9), which gives it a dialog_manager_.

Later, the *outer* (embedder) WebContents shows an interstitial page.  That gets to WebContentsImpl::AttachInterstitialPage, which would normally call dialog_manager_->CancelActiveAndPendingDialogs(this) to dismiss any modal dialogs once the interstitial is shown.  However, dialog_manager_ is still null in the outer (embedder) WebContents, so it doesn't call CancelActiveAndPendingDialogs.

This seems like a problem with BrowserPlugin.  The guest is maintaining dialog state, and the embedder is trying to clear it.  Ideally the guest would let the embedder handle the operation directly, but that seems unlikely in this case (e.g., because RunJavaScriptMessage is closely tied to the RenderFrameHost in the guest).  OOPIFs won't face this because they share the same WebContents.

lazyboy@/fsamuel@: How do you usually handle this type of problem with BrowserPlugin?  Should the embedder tell all of its guests to CancelActiveAndPendingDialogs (in all the places it would normally do that itself)?  Is it even possible to iterate over all of its guests?

### ra...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### la...@chromium.org (2015-05-20)

@12, Yes, we do have "broadcast to all guests" pattern:
For example we broadcast when system's screen info changes:
WebContentsImpl::ScreenInfoChanged() ->
BrowserPluginEmbedder::ScreenInfoChanged() ->
GetBrowserPluginGuestManager()->ForEachGuest(web_contents(), base::Bind(
      &BrowserPluginEmbedder::NotifyScreenInfoChanged));
ref:
https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/browser_plugin/browser_plugin_embedder.cc&l=64

### wj...@chromium.org (2015-05-20)

It seems like having the embedder broadcast to all guests to CancelActiveAndPendingDialogs() is sensible, though I've just started to read this thread and it's possible I'm missing something.

Are there other places where we have duplicate state across embedder/guest that we should be concerned about? Maybe unrelated, but I recently noticed that opening a PDF inside another WebView (e.g. in BrowserSample) allows the PDF inside the webview to generate a context-navigation menu, and open a tab in the main browser context ... that also seems like a potential problem (I've filed this issue as: https://code.google.com/p/chromium/issues/detail?id=489939).

### ra...@chromium.org (2015-05-20)

wjmaclean/paulmeyer - is it ok if I assign to one of you since it's more generally BrowserPlugin related?

### ra...@chromium.org (2015-05-20)

Please do let me know if you won't have time for this though. Thanks!

### cr...@chromium.org (2015-05-20)

https://crbug.com/chromium/482380#c15: Yeah, I'd be concerned about this type of bug happening in other parts of WebContents.  It could probably happen anywhere that the inner guest WebContents has some state that the user interacts with via the outer embedder WebContents...

For this bug, I'm ok with having the embedder tell its guests in all the places that WebContentsImpl calls CancelActiveAndPendingDialogs.  We should think about ways to generalize this to work better for other (and future) cases, though.

### cr...@chromium.org (2015-05-20)

Exploring a possible solution here:
https://codereview.chromium.org/1150843002/

Also CC'ing Avi for context on dialogs and interstitials.

### pa...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89a0f782193755ad7a0b93c58dbcc1b96528405f

commit 89a0f782193755ad7a0b93c58dbcc1b96528405f
Author: creis <creis@chromium.org>
Date: Wed May 27 16:13:17 2015

Dismiss browser plugin modal dialogs when the embedder needs to.

Test from wjmaclean@.  PDF simply shows an alert dialog using script.

BUG=482380
TEST=See bug for repro steps.

Review URL: https://codereview.chromium.org/1150843002

Cr-Commit-Position: refs/heads/master@{#331584}

[modify] http://crrev.com/89a0f782193755ad7a0b93c58dbcc1b96528405f/chrome/browser/ui/browser_browsertest.cc
[add] http://crrev.com/89a0f782193755ad7a0b93c58dbcc1b96528405f/chrome/test/data/alert_dialog.pdf
[modify] http://crrev.com/89a0f782193755ad7a0b93c58dbcc1b96528405f/content/browser/browser_plugin/browser_plugin_embedder.cc
[modify] http://crrev.com/89a0f782193755ad7a0b93c58dbcc1b96528405f/content/browser/browser_plugin/browser_plugin_embedder.h
[modify] http://crrev.com/89a0f782193755ad7a0b93c58dbcc1b96528405f/content/browser/web_contents/web_contents_impl.cc
[modify] http://crrev.com/89a0f782193755ad7a0b93c58dbcc1b96528405f/content/browser/web_contents/web_contents_impl.h


### cr...@chromium.org (2015-05-27)

Should be fixed in r331584.  We should be able to verify in tomorrow's canary to decide whether to merge the fix.

### cl...@chromium.org (2015-05-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cr...@chromium.org (2015-06-01)

Verified the fix.  This has been live since 45.0.2415.0 and is looking safe to merge.  (I had a brief scare from https://crbug.com/chromium/495214, which was a crash involving extension dialogs that started in the same timeframe as this CL, but there's another CL responsible for that one.)

Ok to merge this to M44?

### pe...@google.com (2015-06-01)

Approved for M44 (branch: 2403)

### bu...@chromium.org (2015-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0fc455a3b21e2a6ac68771641c2a4b04008349c0

commit 0fc455a3b21e2a6ac68771641c2a4b04008349c0
Author: creis <creis@chromium.org>
Date: Tue Jun 02 01:15:13 2015

Dismiss browser plugin modal dialogs when the embedder needs to.

Test from wjmaclean@.  PDF simply shows an alert dialog using script.

TBR=nasko,sky
BUG=482380
TEST=See bug for repro steps.
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1150843002

Cr-Commit-Position: refs/heads/master@{#331584}
(cherry picked from commit 89a0f782193755ad7a0b93c58dbcc1b96528405f)

Review URL: https://codereview.chromium.org/1153873005

Cr-Commit-Position: refs/branch-heads/2403@{#165}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/0fc455a3b21e2a6ac68771641c2a4b04008349c0/chrome/browser/ui/browser_browsertest.cc
[add] http://crrev.com/0fc455a3b21e2a6ac68771641c2a4b04008349c0/chrome/test/data/alert_dialog.pdf
[modify] http://crrev.com/0fc455a3b21e2a6ac68771641c2a4b04008349c0/content/browser/browser_plugin/browser_plugin_embedder.cc
[modify] http://crrev.com/0fc455a3b21e2a6ac68771641c2a4b04008349c0/content/browser/browser_plugin/browser_plugin_embedder.h
[modify] http://crrev.com/0fc455a3b21e2a6ac68771641c2a4b04008349c0/content/browser/web_contents/web_contents_impl.cc
[modify] http://crrev.com/0fc455a3b21e2a6ac68771641c2a4b04008349c0/content/browser/web_contents/web_contents_impl.h


### cr...@chromium.org (2015-06-02)

Shall I merge this to M43 as well?

### pe...@google.com (2015-06-03)

[Automated comment] Request affecting a post-stable build (M43), manual review required.

### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/0fc455a3b21e2a6ac68771641c2a4b04008349c0

commit 0fc455a3b21e2a6ac68771641c2a4b04008349c0
Author: creis <creis@chromium.org>
Date: Tue Jun 02 01:15:13 2015


### cr...@chromium.org (2015-06-08)

@dxie: Friendly ping: should I merge this to M43?

### th...@chromium.org (2015-06-08)

laforge is the release manager for M43, not dxie.

### cr...@chromium.org (2015-06-12)

We'll stick with M44 for this one.

### ti...@google.com (2015-06-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

As mentioned in the release notes, $500 for this report as well. We'll be in contact to collect details, though please contact me at timwillis@ if you haven't heard from our finance department in a week.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-02)

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

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/482380?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>Auth, Internals>Plugins>PDF, Platform>Apps>BrowserTag]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081962)*
