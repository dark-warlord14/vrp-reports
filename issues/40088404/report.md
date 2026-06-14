# alert() titles from apps leak to webpages in the same process

| Field | Value |
|-------|-------|
| **Issue ID** | [40088404](https://issues.chromium.org/issues/40088404) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux |
| **Reporter** | an...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2017-07-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36

Steps to reproduce the problem:
1. Install the Inbox by Gmail app (https://chrome.google.com/webstore/detail/inbox-by-gmail/pkclgpgponpjmpfokoepglboejdobkpl).
2. Open the app or go to inbox.google.com.
3. Run alert() in the console and observe that the title is "Inbox by Gmail". (If it isn't, the Inbox app isn't installed.)
4. Middle-click a link in Inbox to open an external site in a new tab.
5. Run alert() in the new tab and observe that the title is still "Inbox by Gmail", even though the website is not Inbox.

What is the expected behavior?
Normal webpages should have an alert title like "example.com says:".

What went wrong?
If a website is running in the same process as an app, the website's alerts will inherit the app's alert title.  Here, the external webpage gets the alert title "Inbox by Gmail", which allows it to impersonate Inbox.

Did this work before? N/A 

Chrome version: 59.0.3071.115  Channel: stable
OS Version: Ubuntu 16.04
Flash Version: 

Tested with both the Inbox and Gmail apps (with Gmail you must open the app directly, visiting gmail.com won't work).

AFAICT this is https://crbug.com/chromium/661388, which was closed as "no repro, no hints as to what happened, no idea what's going on" over six months ago.

This only occurs when the webpage is in the same process as the app, which does not happen if the link is ctrl-clicked or clicked normally. Possibly https://crbug.com/chromium/23815 is related? Nevertheless, sharing a process with an app shouldn't affect anything about a webpage (and vice versa).

## Attachments

- [inbox-inherited-title.png](attachments/inbox-inherited-title.png) (image/png, 15.2 KB)

## Timeline

### ke...@chromium.org (2017-07-19)

Devlin, are you able to reproduce this and figure out what happened in https://crbug.com/chromium/661388?

### rd...@chromium.org (2017-07-19)

Fun!

Avi is probably most qualified to take a look at this, as JS dialog master (Avi, happy to help if I can!).

I wonder if this is related to any of the hosted apps process behavior that the site isolation team has been running into - +a smattering of site isolation folks as well.

### av...@chromium.org (2017-07-19)

The JavaScript dialog code gets the title to use for the dialog by making a call to JavaScriptDialogExtensionsClient::GetExtensionName(). If that function returns false then no special name is used, but if it returns true, then that means that the JavaScriptDialogExtensionsClient is saying "hey, yep, that WebContents is really an extension, and there's a special name that you need to use for dialogs spawned by it".

There are two implementations of JavaScriptDialogExtensionsClient::GetExtensionName(). One is the stub implementation in DefaultExtensionsClient, which always returns false. The other is the real implementation used in Chrome, that lives in the extensions code. Let's take a look.

This is implemented in /extensions/components/javascript_dialog_extensions_client/javascript_dialog_extension_client_impl.cc : 

  bool GetExtensionName(content::WebContents* web_contents,
                        const GURL& origin_url,
                        std::string* name_out) override {
    const Extension* extension = GetExtensionForWebContents(web_contents);
    // ...

OK, what does GetExtensionForWebContents() look like?

const Extension* GetExtensionForWebContents(
    content::WebContents* web_contents) {
  return GetProcessManager(web_contents)->GetExtensionForWebContents(
      web_contents);
}

Two calls.

One to GetProcessManager, but that only cares about the BrowserContext/Profile of the WebContents.

One to ProcessManager::GetExtensionForWebContents:

const Extension* ProcessManager::GetExtensionForWebContents(
    const content::WebContents* web_contents) {
  if (!web_contents->GetSiteInstance())
    return nullptr;
  return extension_registry_->enabled_extensions().GetByID(
      GetExtensionIdForSiteInstance(web_contents->GetSiteInstance()));
}

This extracts the SiteInstance for the WebContents, finds the extension id for it, then looks up the extension.

----

What is going on here?

Is this an extensions issue? It's assuming that all WebContentses in the SiteInstance belong to the extension.

If that is a valid assumption: there is a bug in the middle-click logic that allows the new page to spawn in the same SiteInstance/process as the app.

If that is not a valid assumption: there is a bug in the extensions code that assumes that every WebContents in a SiteInstance is an extension WebContents.

Either way this is not a JavaScript dialogs issue.

Remanding to the extensions team for further proceedings consistent with this decision.

### rd...@chromium.org (2017-07-19)

Thanks for the analysis, Avi!  Nasko, Charlie, Alex - any insight into whether this is desired behavior or a bug from a process standpoint?  We *could* change the GetExtensionForWebContents() logic to go based on URL, but I'm not sure that's necessarily an improvement.

### ke...@chromium.org (2017-07-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>WindowDialog]

### cr...@chromium.org (2017-07-19)

https://crbug.com/chromium/746517#c3: That's not a valid assumption, so this is a bug in the extensions code.  In this case, we're talking about a hosted app, and hosted app SiteInstances can *definitely* include cross-site web pages that are not part of the hosted app.  (That allows things like OAuth popup dialogs to work.)  We can't assume that the entire SiteInstance is part of the hosted app.

Devlin, can you take a look at updating the extension code here to use the URL?

(As a side note, Łukasz changed the behavior of middle click in M60 to open in a new process in https://crbug.com/chromium/23815, but this bug could still occur on window.open and targeted links within a hosted app even in M60.)

### av...@chromium.org (2017-07-19)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WindowDialog Platform>Extensions]

### rd...@chromium.org (2017-07-19)

> Devlin, can you take a look at updating the extension code here to use the URL?

On it.  Will we need to worry about a race condition here?  i.e., the frame is created for a given extension before an url is committed.  (It's possible we might just need to experiment and see).

In cursory exploration, also found crbug.com/746572.  Seems mostly unrelated in terms of the code itself.

### sh...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-07-20)

https://crbug.com/chromium/746517#c8: In general, the dialog will be shown by the last committed page, so the last committed URL for the frame is the right thing to use.  You raise a good point about the initial blank document in a frame, though, which could be scripted by the opener/parent.  I guess we'd want to use the origin of the frame in that case, or just fall back to what we do normally do for about:blank (i.e., "This page" for main frames or "An embedded page" for subframes).

### sh...@chromium.org (2017-08-03)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2017-08-03)

Thanks for the ping, sheriffbot!

Circling back to this after a week of travel.

@11, my question wasn't just for dialogs, but in general.  We said that ProcessManager::GetExtensionForWebContents() using site instance is incorrect, and should be changed.  One option is to use URL.  But this method is used for a lot more than just JS dialog attribution (task management, dev tools, context menus, and more!).  So even though there's no risk of a race with JS dialogs (because we know that the page must have committed in order to have script running), is that the case for all of them?  Or will we have to worry about a race in certain conditions?  If so, is there any other feasible way to get an extension associated with a given web contents?  (I think we've traditionally used site instance, for better or worse.) 

### bu...@chromium.org (2017-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a282e33fb1c600499d2c7ff1e633de22865549c

commit 7a282e33fb1c600499d2c7ff1e633de22865549c
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Aug 10 01:54:10 2017

[Extensions] Account for hosted apps in GetExtensionForWebContents

ProcessManager::GetExtensionForWebContents() returns the extension
associated with a provided web contents. It does this by looking up
the site instance's url, which is handy because it
a) is normalized for extensions and hosted apps (i.e., even hosted
   apps have chrome-extension:// urls in their site instances), and
b) it works before first commit, which is necessary in certain set up
   instances.
   
However, this returns the incorrect result when a vanilla web page is
hosted in a hosted app's site instance. Account for this instance in
the ProcessManager, and add a browser test for the same.

Bug: 746517
Change-Id: Ibc4a29dd60fb919be9dfe2989f027bc731a4440e
Reviewed-on: https://chromium-review.googlesource.com/604719
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#493219}
[modify] https://crrev.com/7a282e33fb1c600499d2c7ff1e633de22865549c/chrome/browser/extensions/process_manager_browsertest.cc
[modify] https://crrev.com/7a282e33fb1c600499d2c7ff1e633de22865549c/extensions/browser/process_manager.cc
[modify] https://crrev.com/7a282e33fb1c600499d2c7ff1e633de22865549c/extensions/browser/process_manager.h


### rd...@chromium.org (2017-08-10)

This should be fixed, and no longer repros for me locally.  anowlcalledjosh@, did you want to verify from your end to double-check?

### an...@gmail.com (2017-08-10)

Yep, looks like this is fixed. Would this be eligible for a reward under the VRP?

### rd...@chromium.org (2017-08-11)

Closing it out.

Adding awhalley@ for VRP.

### aw...@google.com (2017-08-11)

Yep, it will be considered by the panel shortly.  Cheers!

### sh...@chromium.org (2017-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-14)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-14)

+awhalley@ for M61 merge review.


### aw...@google.com (2017-08-14)

govind@ - good for 61

### go...@chromium.org (2017-08-14)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/746517#c23. Please merge ASAP. Thank you.

### bu...@chromium.org (2017-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/436901103ce80a654288a39f3ba60e1041d017ec

commit 436901103ce80a654288a39f3ba60e1041d017ec
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Mon Aug 14 20:40:04 2017

[Extensions] Account for hosted apps in GetExtensionForWebContents

ProcessManager::GetExtensionForWebContents() returns the extension
associated with a provided web contents. It does this by looking up
the site instance's url, which is handy because it
a) is normalized for extensions and hosted apps (i.e., even hosted
   apps have chrome-extension:// urls in their site instances), and
b) it works before first commit, which is necessary in certain set up
   instances.

However, this returns the incorrect result when a vanilla web page is
hosted in a hosted app's site instance. Account for this instance in
the ProcessManager, and add a browser test for the same.

TBR=rdevlin.cronin@chromium.org

(cherry picked from commit 7a282e33fb1c600499d2c7ff1e633de22865549c)

Bug: 746517
Change-Id: Ibc4a29dd60fb919be9dfe2989f027bc731a4440e
Reviewed-on: https://chromium-review.googlesource.com/604719
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#493219}
Reviewed-on: https://chromium-review.googlesource.com/614462
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#553}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/436901103ce80a654288a39f3ba60e1041d017ec/chrome/browser/extensions/process_manager_browsertest.cc
[modify] https://crrev.com/436901103ce80a654288a39f3ba60e1041d017ec/extensions/browser/process_manager.cc
[modify] https://crrev.com/436901103ce80a654288a39f3ba60e1041d017ec/extensions/browser/process_manager.h


### aw...@google.com (2017-08-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-28)

Nice one! The VRP panel decided to award $500 for this bug. A member of our finance team will be in touch shortly to arrange payment.

### aw...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/746517?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088404)*
