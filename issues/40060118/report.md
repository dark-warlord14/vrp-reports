# Security: webRequest API allows extensions to XSS chrome.google.com and gain access to webstorePrivate API

| Field | Value |
|-------|-------|
| **Issue ID** | [40060118](https://issues.chromium.org/issues/40060118) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Platform>Extensions, Webstore |
| **Reporter** | [Deleted User] |
| **Assignee** | ba...@chromium.org |
| **Created** | 2012-06-22 |
| **Bounty** | $2,000.00 |

## Description

*No description available.*

## Attachments

- deleted (application/octet-stream, 0 B)
- [bug-134101.patch](attachments/bug-134101.patch) (text/x-diff; charset=us-ascii, 6.1 KB)

## Timeline

### js...@chromium.org (2012-06-22)

This bug itself isn't that bad, since it requires a malicious extension. However, the bigger worry is that it looks like a stepping stone to a sandbox escape.

### js...@chromium.org (2012-06-22)

Sorry, I didn't mean to sound dismissive. I was just providing context for the severity rating. In terms of larger scale attacks, the big fear is in using this as a component of a sandbox escape (e.g. http://blog.chromium.org/2012/06/tale-of-two-pwnies-part-2.html ).

### js...@chromium.org (2012-06-22)

[Empty comment from Monorail migration]

### mp...@chromium.org (2012-06-22)

Makes sense. The webRequest API uses the URL being fetched, not the URL of the page doing the fetching, to determine permissions. It sounds like #0's suggestion is right - we should restrict any requests made by the webstore.

### aa...@chromium.org (2012-06-22)

Yeah, I think the issue here is that we shouldn't be exposing resource requests through the webRequest API that are embedded from hosts you don't have host permissions for.

### mp...@chromium.org (2012-06-22)

Maybe CanExtensionAccessURL should take into account the first_party_for_cookies URL? (I'm not sure which field on URLRequest contains the host that issued the request, if any.)

### aa...@chromium.org (2012-06-22)

I looked into this for the downloads API. first_party_for_cookies usually works, but there are some cases where it isn't included (I think due to privacy settings or something?). I think my conclusion was that there's currently no reliable way to get this information out of URLRequest.

### ba...@chromium.org (2012-06-25)

I can look into the first_party_for_cookies approach. Maybe we want to use that as a first step to raise the barrier.

Unfortunately, though, this won't be a perfect fix even if we get it right due to the possibility of cache poisoning (kudos for Bernhard for pointing this out). We wonder whether isolated apps could help us.

### ba...@chromium.org (2012-06-25)

Here is a patch for the proposed change for https://crbug.com/chromium/134101#c7 (not sure whether I am supposed to upload it into codereview).

I could verify this only in debug builds after applying this patch:

diff --git a/content/browser/web_contents/render_view_host_manager.cc b/content/browser/web_contents/render_view_host_manager.cc
index a440682..30774c4 100644
--- a/content/browser/web_contents/render_view_host_manager.cc
+++ b/content/browser/web_contents/render_view_host_manager.cc
@@ -236,7 +236,7 @@ void RenderViewHostManager::DidNavigateMainFrame(
 }
 
 void RenderViewHostManager::SetWebUIPostCommit(WebUIImpl* web_ui) {
-  DCHECK(!web_ui_.get());
+  //DCHECK(!web_ui_.get());
   web_ui_.reset(web_ui);
 }

Otherwise the DCHECK would fire:
[10339:10339:2413158038712:FATAL:render_view_host_manager.cc(239)] Check failed: !web_ui_.get(). 
Backtrace:
        base::debug::StackTrace::StackTrace() [0x7ff374096bae]
        logging::LogMessage::~LogMessage() [0x7ff3740c7911]
        RenderViewHostManager::SetWebUIPostCommit() [0x7ff376e29113]
        WebContentsImpl::DidNavigateMainFramePostCommit() [0x7ff376e37e7c]
        WebContentsImpl::DidNavigate() [0x7ff376e39057]
        content::RenderViewHostImpl::OnMsgNavigate() [0x7ff376d974e9]
        content::RenderViewHostImpl::OnMessageReceived() [0x7ff376d94fc1]
        content::RenderProcessHostImpl::OnMessageReceived() [0x7ff376d83502]
        IPC::ChannelProxy::Context::OnDispatchMessage() [0x7ff36e00a2f5]
        base::internal::RunnableAdapter<>::Run() [0x7ff36e00d706]
        base::internal::InvokeHelper<>::MakeItSo() [0x7ff36e00d1d6]
        base::internal::Invoker<>::Run() [0x7ff36e00cab3]
        base::Callback<>::Run() [0x7ff37408f56d]
        MessageLoop::RunTask() [0x7ff3740cc29e]
        MessageLoop::DeferOrRunPendingTask() [0x7ff3740cc3b5]
        MessageLoop::DoWork() [0x7ff3740ccb9b]
        base::MessagePumpGlib::RunWithDispatcher() [0x7ff374070dc2]
        base::MessagePumpGlib::Run() [0x7ff3740711a2]
        MessageLoop::RunInternal() [0x7ff3740cbf73]
        MessageLoop::RunHandler() [0x7ff3740cbe2a]
        MessageLoopForUI::RunWithDispatcher() [0x7ff3740cd02c]
        ChromeBrowserMainParts::MainMessageLoopRun() [0x7ff379be3a83]
        content::BrowserMainLoop::RunMainMessageLoopParts() [0x7ff376b765c9]
        (anonymous namespace)::BrowserMainRunnerImpl::Run() [0x7ff376b7829a]
        BrowserMain() [0x7ff376b74d90]
        content::RunNamedProcessTypeMain() [0x7ff376b518b4]
        content::ContentMainRunnerImpl::Run() [0x7ff376b5264c]
        content::ContentMain() [0x7ff376b50f27]
        ChromeMain [0x7ff3792735dd]
        main [0x7ff37927359c]


### ba...@chromium.org (2012-06-25)

[Empty comment from Monorail migration]

### cr...@chromium.org (2012-06-25)

@https://crbug.com/chromium/134101#c9: The downside with isolated storage is that the user would have to sign into the Chrome Web Store separately from their normal Google sign-in.  Seems like we should make it possible to know what page is making a request, regardless of which sub-resource URL it's requesting.

@https://crbug.com/chromium/134101#c10: You can check the private checkbox on a code review if you're concerned about visibility.  Only the folks CC'd will see it.

### ba...@chromium.org (2012-06-25)

Regarding the private checkbox: I suppose that it would show up in the RSS feeds. Justin: please let me know if you want me to upload the patch.

### js...@chromium.org (2012-06-25)

You can just upload the patch as normal. We'd like better handling of private patches (and we've asked the codesite team before) but the truth is that the fixes sit much longer after being checked into the tree before shipping to stable anyway.

### aa...@chromium.org (2012-06-26)

[Empty comment from Monorail migration]

### aa...@chromium.org (2012-06-26)

An easy hack might be to check the process ID of the originating request. We isolate the store in its own process, so it should be easy to identify requests originating from it.


### ba...@chromium.org (2012-06-26)

Can you point me to the location where this happens? I wonder whether there is a simple way to check whether a specific process ID is associated with the CWS.

### ba...@chromium.org (2012-06-26)

@creis: I think you are the master of render process switches. If I remove the chrome.webRequest.onBeforeRequest.addListener(onBeforeRequest, {urls: ["https://www.google.com/jsapi"]}, ["blocking"]); from background.js from the extension of the original post, the extension does not use the web request API anymore. Still it produces the DCHECK of https://crbug.com/chromium/134101#c10. Could you look into this?

### aa...@chromium.org (2012-06-26)

It would be really good to get this into M21 if we can find a nice surgical fix.

### ba...@chromium.org (2012-06-26)

I agree. You have two CLs for review.

### cr...@chromium.org (2012-06-26)

@https://crbug.com/chromium/134101#c18: Dominic, can you CC me on the code review so I can try out the latest patch?  I'm not clear why it's affecting whether a web_ui_ object exists on the tab's RenderViewHostManager.

### ba...@chromium.org (2012-06-26)

Done. You don't need to apply the changelists, though. The easiest way to observe this behavior is: Download and unzip storexss.zip from the original post. Delete the first line of background.js and install the extension in a Chrome with DCHECKs enabled.

### cr...@chromium.org (2012-06-26)

This is odd.  CC'ing estade@, who recently re-did the WebUI stuff in RenderViewHostManager.

Evan, the storexss.zip extension here is triggering a DCHECK in RVHM::SetWebUIPostCommit (on tip-of-tree), if you comment out all but the last line of background.js.  We're getting there because the extension is opening a popup to the Chrome Web Store.  WebContentsImpl::DidNavigateMainFramePostCommit is trying to assign a WebUI to the opened window, but it already has a WebUI.

I don't understand why we're assigning a WebUI to the opened window in that case if it already has one.  Can you take a look?

### bu...@chromium.org (2012-06-27)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=144529

------------------------------------------------------------------------
r144529 | battre@chromium.org | Wed Jun 27 13:10:22 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_api.cc?r1=144529&r2=144528&pathrev=144529
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_api_unittest.cc?r1=144529&r2=144528&pathrev=144529
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.h?r1=144529&r2=144528&pathrev=144529
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.cc?r1=144529&r2=144528&pathrev=144529

Use the first_party_for_cookies URL to filter which requests the WebRequest API sees


BUG=134101
TEST=see bug report


Review URL: https://chromiumcodereview.appspot.com/10636056
------------------------------------------------------------------------

### es...@chromium.org (2012-06-28)

this falls outside the realm of my refactor. I don't know why this code exists at all:

  if (opener_web_ui_type_ != WebUI::kNoWebUI) {
    // If this is a window.open navigation, use the same WebUI as the renderer
    // that opened the window, as long as both renderers have the same
    // privileges.
    if (delegate_ && opener_web_ui_type_ == GetWebUITypeForCurrentState()) {
      WebUIImpl* web_ui = static_cast<WebUIImpl*>(CreateWebUI(GetURL()));
      // web_ui might be NULL if the URL refers to a non-existent extension.
      if (web_ui) {
        render_manager_.SetWebUIPostCommit(web_ui);
        web_ui->RenderViewCreated(GetRenderViewHost());
      }
    }
    opener_web_ui_type_ = WebUI::kNoWebUI;
  }

I did not originate or ever remember reading this code. I don't know what the valid use case is. I don't know why opener_web_ui_type_ isn't kNoWebUI for the extension's bg page. If it does have some valid use case, then I would agree that we probably don't need to create the new webui if one already exists (like if the website is the CWS or a chrome:// page).

### ba...@chromium.org (2012-06-29)

Matt landed this code way back in http://codereview.chromium.org/172120 (chrome/browser/tab_contents/tab_contents.cc)

### ba...@chromium.org (2012-06-29)

I have verified that r144529 works as intended on 22.0.1189.0 canary. The popup shows only the CWS.

### ba...@chromium.org (2012-06-29)

CC'ing Karen to be sure that she can see the bug.

### ka...@google.com (2012-06-29)

thsis is marked as security so i am assuming security team will approve it. :)

### js...@chromium.org (2012-06-29)

Yeah, if it merges clean fire away.

### bu...@chromium.org (2012-07-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=145136

------------------------------------------------------------------------
r145136 | battre@chromium.org | Mon Jul 02 04:07:36 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api.cc?r1=145136&r2=145135&pathrev=145136
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_unittest.cc?r1=145136&r2=145135&pathrev=145136
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.cc?r1=145136&r2=145135&pathrev=145136
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.h?r1=145136&r2=145135&pathrev=145136

Merge 144529 - Use the first_party_for_cookies URL to filter which requests the WebRequest API sees


BUG=134101
TEST=see bug report


Review URL: https://chromiumcodereview.appspot.com/10636056

TBR=battre@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10696073
------------------------------------------------------------------------

### sc...@gmail.com (2012-07-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-07-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=145168

------------------------------------------------------------------------
r145168 | battre@chromium.org | Mon Jul 02 11:52:22 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api.cc?r1=145168&r2=145167&pathrev=145168
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_unittest.cc?r1=145168&r2=145167&pathrev=145168
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.cc?r1=145168&r2=145167&pathrev=145168
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.h?r1=145168&r2=145167&pathrev=145168

Revert 145136 - Merge 144529 - Use the first_party_for_cookies URL to filter which requests the WebRequest API sees


BUG=134101
TEST=see bug report


Review URL: https://chromiumcodereview.appspot.com/10636056

TBR=battre@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10696073

TBR=battre@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10693073
------------------------------------------------------------------------

### ba...@chromium.org (2012-07-02)

I had to revert because the unittest does not compile on the beta branch. I'll try again once I can solve the dependency hell of gclient.

### bu...@chromium.org (2012-07-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=145285

------------------------------------------------------------------------
r145285 | battre@chromium.org | Tue Jul 03 04:49:00 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api.cc?r1=145285&r2=145284&pathrev=145285
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_unittest.cc?r1=145285&r2=145284&pathrev=145285
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.cc?r1=145285&r2=145284&pathrev=145285
 M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/extensions/api/web_request/web_request_api_helpers.h?r1=145285&r2=145284&pathrev=145285

Use the first_party_for_cookies URL to filter which requests the WebRequest API sees

Merge of r144529.

BUG=134101
TEST=see bug report
TBR=battre@chromium.org

Review URL: https://chromiumcodereview.appspot.com/10702079
------------------------------------------------------------------------

### sc...@gmail.com (2012-07-31)

[Empty comment from Monorail migration]

### ba...@chromium.org (2012-07-31)

[Empty comment from Monorail migration]

### ba...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-08-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=152551

------------------------------------------------------------------------
r152551 | battre@chromium.org | 2012-08-21T13:19:10.430439Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/declarative_webrequest/webrequest_action_unittest.cc?r1=152551&r2=152550&pathrev=152551
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/declarative_webrequest/webrequest_action.cc?r1=152551&r2=152550&pathrev=152551
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_api.cc?r1=152551&r2=152550&pathrev=152551
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_permissions_unittest.cc?r1=152551&r2=152550&pathrev=152551
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_permissions.cc?r1=152551&r2=152550&pathrev=152551
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/extensions/api/web_request/web_request_permissions.h?r1=152551&r2=152550&pathrev=152551

Protect Chrome WebStore based on process IDs


BUG=134101


Review URL: https://chromiumcodereview.appspot.com/10825102
------------------------------------------------------------------------

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-18)

[Empty comment from Monorail migration]

### aw...@google.com (2016-11-18)

Congratulations, the panel has decided to reward $2,000 for this bug.  Cheers!

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/134101?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Platform>Extensions, Webstore]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060118)*
