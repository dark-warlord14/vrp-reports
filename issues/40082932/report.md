# Security: Disrupting the omnibox from the attacker's website.

| Field | Value |
|-------|-------|
| **Issue ID** | [40082932](https://issues.chromium.org/issues/40082932) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, UI>Browser>Navigation |
| **CVE IDs** | CVE-2015-6782 |
| **Reporter** | he...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2015-09-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display arbitrary content under the URL of the website that the user is trying to access (from the attacker's page, through the omnibox).

A variation of this vulnerability can be reproduced on Firefox and IE (when the user tries to leave the attacker's webpage using the location bar, it's possible to redirect him to an arbitrary page). However I couldn't reproduce it on Chrome.

**VERSION**  

Chrome Version: [45.0.2454.101 m] + [stable] | I tested it too on [47.0.2520.0 canary] and it works.

Operating System: [Windows 7 Ultimate 32x, Service Pack 1]

**REPRODUCTION CASE**

1. Access <http://lherrera.16mb.com/>
2. Type <https://www.google.com> in the omnibox.
3. A fake error page similar to Google's should appear.
4. A prompt should show up too, asking for the user's credentials.
5. After typing a random username and password, you can check if it was stored in <http://lherrera.16mb.com/save.txt>

## Attachments

- [prompt.png](attachments/prompt.png) (image/png, 73.9 KB)

## Timeline

### md...@chromium.org (2015-09-28)

creis/kenrb: Another popup UI issue that seems similar to https://crbug.com/chromium/534639.  The popup indicates the correct origin, but the omnibox shows https://www.google.com while the content area shows attacker controlled content.  (Note: After step #2, hit enter to initiate navigation to https://www.google.com; don't just stop at having typed in the URL.)

### cr...@chromium.org (2015-09-28)

Actually, I think this is a different bug that doesn't seem to involve Ken's timer.  (There's no 2 second delay between hitting enter and seeing the dialog.)

This one seems to boil down to having a beforeunload handler that does a document.write of a page with a JavaScript prompt.  Normally prompts are disallowed during beforeunload, but apparently document.write bypasses that.

Minimal repro: Add this to a page (e.g., via DevTools) and then try to navigate away.
window.onbeforeunload = function() { document.write("<script>prompt('attack');</script>"); }

@dcheng: Do you know where the logic is that prevents most prompts during beforeunload?  Would you be able to help make that apply to this case as well?

### dc...@chromium.org (2015-09-28)

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/page/ChromeClient.cpp&rcl=1443410811&l=59 is the check in question. I'll look into why the check isn't triggered.

### dc...@chromium.org (2015-09-28)

Dispatching a beforeunload event does this:

bool Document::dispatchBeforeUnloadEvent(ChromeClient& chromeClient, bool& didAllowNavigation)
{
    // ... snip
    m_loadEventProgress = BeforeUnloadEventInProgress;
    m_domWindow->dispatchEvent(beforeUnloadEvent.get(), this);
    m_loadEventProgress = BeforeUnloadEventCompleted;
    // ... snip
}

so you would expect this to return BeforeUnloadDismissal:
Document::PageDismissalType Document::pageDismissalEventBeingDispatched() const
{
    if (m_loadEventProgress == BeforeUnloadEventInProgress)
        return BeforeUnloadDismissal;
    if (m_loadEventProgress == PageHideInProgress)
        return PageHideDismissal;
    if (m_loadEventProgress == UnloadEventInProgress)
        return UnloadDismissal;
    return NoDismissal;
}

But instead, it returns NoDismissal. It turns out this is because of document.open():
void Document::open()
{
    // ... snip
    if (m_loadEventProgress != LoadEventInProgress && m_loadEventProgress != UnloadEventInProgress)
        m_loadEventProgress = LoadEventNotRun;
}

I guess a simple fix is to change the second check to become a no-op as well, if a page dismissal event is being dispatched.

### he...@gmail.com (2015-09-28)

Shouldn't the severity be set to at least medium? Given that it doesn't require unusual user action and it disrupts the location bar?

By the way, on the actual version of Chrome (45.0.2454.101) the origin isn't displayed (not in a way a user would understand) because the prompt is executed from an iframe.

### cr...@chromium.org (2015-09-29)

https://crbug.com/chromium/536652#c5: Yes, I think this is likely higher than low severity, especially with the lack of origin in the dialog.  The fact that it requires user input (because we don't show the pending URL for renderer-initiated navigations) is a mitigating factor, but it still merits Medium in my opinion.

### me...@chromium.org (2015-09-29)

Drive by comment: Looks like the prompt doesn't show the origin because it's triggered by a javascript: URL. Should we do something about it? e.g. show the parent's origin in the dialog, given that javascript: isn't an isolated origin?

### cr...@chromium.org (2015-09-29)

https://crbug.com/chromium/536652#c7: It's worth understanding the prompt behavior more.  I just tested and there's a difference between M45 and M47.  M45 shows "JavaScript" for any dialogs from about:blank iframes (regardless of whether there's a javascript: URL involved).  M47 says "The page at about:blank says" instead. 

That's much better than before, though it would be even better to show the effective origin for the about:blank page (inherited from the page that controls it, which is not necessarily the parent frame).  I think we'll want to bisect to find when the dialog behavior changed, possibly merge that change to M46 if needed, and consider what it would take to show the effective origin instead.

### me...@chromium.org (2015-09-29)

+palmer because I think the difference might be because of his changes to the UI surfaces displaying URLs/origins.

palmer: Do you happen to know how the display of origin on alert/confirm/prompt dialogs were changed recently?

### bu...@chromium.org (2015-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e1e0c4301aaa8228e362f2409dbde2d4d1896866

commit e1e0c4301aaa8228e362f2409dbde2d4d1896866
Author: dcheng <dcheng@chromium.org>
Date: Tue Sep 29 22:28:05 2015

Don't change Document load progress in any page dismissal events.

This can confuse the logic for blocking modal dialogs.

BUG=536652

Review URL: https://codereview.chromium.org/1373113002

Cr-Commit-Position: refs/heads/master@{#351419}

[add] http://crrev.com/e1e0c4301aaa8228e362f2409dbde2d4d1896866/third_party/WebKit/LayoutTests/fast/events/alert-in-beforeunload-document-write-expected.txt
[add] http://crrev.com/e1e0c4301aaa8228e362f2409dbde2d4d1896866/third_party/WebKit/LayoutTests/fast/events/alert-in-beforeunload-document-write.html
[modify] http://crrev.com/e1e0c4301aaa8228e362f2409dbde2d4d1896866/third_party/WebKit/Source/core/dom/Document.cpp


### pa...@chromium.org (2015-09-29)

Yes, I recently changed how the origin is displayed in window.{alert,prompt,confirm}: 
https://codereview.chromium.org/1328663004.

The problem is that the calling origin is a javascript: URL, and we don't take into account the invoking origin when trying to display something to the user.

One might also say that the problem is that iframes are allowed to invoke window.{alert,prompt,confirm}...

### me...@chromium.org (2015-09-29)

Thanks palmer. For javascript: I suppose we could show the parent origin, but there is also data: and blob: and other isolated origins. In any case, I filed https://crbug.com/chromium/537452 to track that issue separately, feel free to chime in.

### cr...@chromium.org (2015-09-29)

https://crbug.com/chromium/536652#c11: Great.  Looks like the dialog change landed in 47.0.2501.0.  Do you think that's worth merging to M46, or is the change from "JavaScript" to "The page at about:blank says" not a big enough security gain?

Also, I'm pretty sure the javascript: URL thing is a red herring.  We're only interested in the effective origin of the frame, which we do have in the browser process (see https://crbug.com/chromium/469889#c35).  javascript: URLs won't work in an about:blank iframe unless they come from the effective origin of the frame, and they're not necessary either-- you can do the same prompt directly with script code (e.g., subframe.contentWindow.prompt("foo")).

I think this spoof can likely be considered fixed with Daniel's change in https://crbug.com/chromium/536652#c10, and perhaps we should file a separate bug for showing the effective origin for about:blank in dialog boxes?  (That applies to both subframes and main frames, such as about:blank popups.)  I'll take care of filing that one.

dcheng@: Your CL fixes the spoof, right?  Please reopen if not.

### cr...@chromium.org (2015-09-29)

https://crbug.com/chromium/536652#c12: Oops, you beat me to it.  I'll post a similar comment there, since it's not about javascript: URLs.

### dc...@chromium.org (2015-09-30)

Yep, my fix prevents the dialogs from appearing at all.

### cl...@chromium.org (2015-09-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-10-12)

Based on revision, this fix is already in M-47. 

Merge-request for M-46 (in case there is a patch release so that this fix can ride along).

### ti...@google.com (2015-10-12)

[Automated comment] Less than 2 weeks to go before stable on M46, manual review required.

### ti...@google.com (2015-10-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-12)

Adding reward-topanel for VRP panel consideration (details here: https://www.google.com/about/appsecurity/chrome-rewards/)

### ti...@google.com (2015-10-14)

Merge approved for potential M46 stable refresh (branch 2490).
Pls merge asap.

### bu...@chromium.org (2015-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/931acc8f51135cf1e52823fc6bfe6a93def085f7

commit 931acc8f51135cf1e52823fc6bfe6a93def085f7
Author: Daniel Cheng <dcheng@chromium.org>
Date: Mon Oct 19 22:33:08 2015

Don't change Document load progress in any page dismissal events.

This can confuse the logic for blocking modal dialogs.

BUG=536652

Review URL: https://codereview.chromium.org/1373113002

Cr-Commit-Position: refs/heads/master@{#351419}
(cherry picked from commit e1e0c4301aaa8228e362f2409dbde2d4d1896866)

Review URL: https://codereview.chromium.org/1415773002 .

Cr-Commit-Position: refs/branch-heads/2490@{#544}
Cr-Branched-From: 7790a3535f2a81a03685eca31a32cf69ae0c114f-refs/heads/master@{#344925}

[add] http://crrev.com/931acc8f51135cf1e52823fc6bfe6a93def085f7/third_party/WebKit/LayoutTests/fast/events/alert-in-beforeunload-document-write-expected.txt
[add] http://crrev.com/931acc8f51135cf1e52823fc6bfe6a93def085f7/third_party/WebKit/LayoutTests/fast/events/alert-in-beforeunload-document-write.html
[modify] http://crrev.com/931acc8f51135cf1e52823fc6bfe6a93def085f7/third_party/WebKit/Source/core/dom/Document.cpp


### ti...@google.com (2015-11-10)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Congratulations - our reward panel awarded a $1,000 reward for your report.

We'll credit you in the Chrome Release notes as "Luan Herrera". If you would like to use a different name, please update this bug and I'll update the release notes. We'll also provide you with a CVE ID in a few hours for your reference.

Someone from our finance area should be in contact within a week to arrange payment. If that doesn't happen, please either update this issue or email me directly at timwillis@.

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-12-01)

CVE-2015-6782

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-06)

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

This issue was migrated from crbug.com/chromium/536652?no_tracker_redirect=1

[Multiple monorail components: Blink, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082932)*
