# Security: URL Spoofing when victim tries to access another website from attacker's page.

| Field | Value |
|-------|-------|
| **Issue ID** | [40083010](https://issues.chromium.org/issues/40083010) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views, UI |
| **CVE IDs** | CVE-2016-1616 |
| **Reporter** | he...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2015-10-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display arbitrary content under the URL of the website that the user is trying to access (from the attacker's page, through the omnibox).

**VERSION**  

Chrome Version: [45.0.2454.101 m] + [stable] | I tested it too on [47.0.2520.0 canary] and it works.

Operating System: [Windows 7 Ultimate 32x, Service Pack 1]

**REPRODUCTION CASE**

1. Access <http://lherrera.16mb.com/Chrome/spoof.html>
2. Type <https://www.google.com> in the omnibox and press ENTER.
3. A fake error page should appear under Google's URL.

## Attachments

- [before.png](attachments/before.png) (image/png, 84.9 KB)
- [after.png](attachments/after.png) (image/png, 149.5 KB)

## Timeline

### he...@gmail.com (2015-10-09)

Oh, I forgot to mention that after you reproduce the attack once, if you want to reproduce it again you must open the attacker's page in incognito mode (given that this attack uses HTTP AUTH and the session takes some time to expire).

### fe...@chromium.org (2015-10-09)

I end up with a correct navigation. Could you please attach a screenshot so that I can see what you're seeing? Thanks!

### he...@gmail.com (2015-10-09)

Yes. The first screenshot is before typing https://www.google.com and pressing ENTER. The second is after.

### me...@chromium.org (2015-10-09)

I think I did repro this yesterday, at least once. Assigning to myself to take a look because this seems to have something to do with the Auth interstitial.

### fe...@chromium.org (2015-10-10)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-10-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-10-13)

+davidben since you mentioned you've been looking at HTTP auth code

What's happening here is that we get a URLRequestHttpJob::OnStartCompleted call after the navigation to google.com, and this call shows a new auth dialog because we get a AUTH_REQUIRED_RESPONSE_NO_ACTION from the network_delegate at URLRequest::NotifyAuthRequired

I'm not sure what exactly "start completed" means in url request http jobs, but it doesn't sound right: The new navigation cancelled the pending auth dialog, so "complete" sounds semantically incorrect to me.

I believe this bug isn't related to the login interstitial, but haven't dug deep enough yet.

### da...@chromium.org (2015-10-13)

+asanka who's actually more familiar with the auth stuff in //net and surrounding. I've just been bashing against the plumbing //content and up lately.

### as...@chromium.org (2015-10-20)

(Whoops. There should be some sort of footer in Pri-1 bug emails or something.)

#7: The behavior at URLRequestHttpJob::OnStartCompleted() is expected. The OnStartCompleted() just means that the request has progressed to the point of having received response headers or encountered some sort of error. For a request that needs HTTP server authentication, this is the point where the net stack sees the "WWW-Authenticate" headers and is able to notify its client about this.

What's happening is that:

1. The login dialog captures the <Enter> key. So even though the user is typing in the omnibox, when they press <Enter>, the login prompt attempts to proceed with the credentials that were already entered (along with all the side-effects involved)

2. Armed with the supplied credentials, the URLRequestHTTPJob attempts to send another request.

3. The server responds with another 401 since the credentials are wrong.

4. Another cycle of NotifyAuthRequired -> create LoginHandler etc.. results in another login dialog being presented to the user.

If at this point, the user cancels the dialog, or if the server accepts empty credentials, the tab ends up rendering the most recent response body. The omnibox hasn't received a navigation request since it never saw the <Enter> key. The situation is no different from the user typing 'google.com' into the omnibox and not hitting enter while the URLRequest from the previous navigation completes slowly.

I think the confusing part here is that the omnibox processes keystrokes, but not the <Enter> or <Esc> keys.

### me...@chromium.org (2015-10-23)

asanka: Thanks for tracking this down!

The problem isn't limited to HTTP Auth dialog: Any tab modal dialog steals enter key when out of focus. Another example is the cert viewer, it closes when the user hits enter in the omnibox, but no navigation occurs. I tried to find out where focus / input event handling is being done but got lost in UI and views code. 

msw, wittman: Can you please take a look and reassign if necessary? Thanks.

### ms...@chromium.org (2015-10-26)

Hmm, enter is set as an accelerator for the default dialog button, but I wouldn't suspect it to steal any key presses when the omnibox is focused. You could test my theory by experimentally disabling the accelerator code in LabelButton::SetIsDefault. 
https://code.google.com/p/chromium/codesearch#chromium/src/ui/views/window/dialog_client_view.cc&rcl=1445860033&l=414
https://code.google.com/p/chromium/codesearch#chromium/src/ui/views/controls/button/label_button.cc&rcl=1445860033&l=179

Perhaps the defect is in the DialogClientView::OnWillChangeFocus logic; maybe it could avoid setting the default button (and enter accelerator) when the newly focused view is outside the dialog's hierarchy.
https://code.google.com/p/chromium/codesearch#chromium/src/ui/views/window/dialog_client_view.cc&rcl=1445860033&l=150

### me...@chromium.org (2015-10-26)

@msw: Just tested by disabling the accelerator code in LabelButton::SetIsDefault and the bug indeed goes away.

Checking view hierarchy in DialogClientView::OnWillChangeFocus and setting button default to false if hierarchy roots are different works as well. Unless you think accelerator code needs to be fixed, I can go with this approach.

### me...@chromium.org (2015-10-26)

CL at https://codereview.chromium.org/1424753003

### me...@chromium.org (2015-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-10)

meacer@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2015-11-10)

Adjusting severity: The problem here is that the login dialog steals some key presses (particularly enter) from the omnibox while open, and the user ends up submitting empty login credentials to the original auth page. While the bug enables spoofing/phishing, it doesn't meet the bar for high severity.

### me...@chromium.org (2015-11-11)

+sky for bug visibility

### bu...@chromium.org (2015-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/297ae873b471a46929ea39697b121c0b411434ee

commit 297ae873b471a46929ea39697b121c0b411434ee
Author: meacer <meacer@chromium.org>
Date: Tue Nov 17 19:43:24 2015

Custom buttons should only handle accelerators when focused.

BUG=541415

Review URL: https://codereview.chromium.org/1437523005

Cr-Commit-Position: refs/heads/master@{#360130}

[modify] http://crrev.com/297ae873b471a46929ea39697b121c0b411434ee/ui/views/controls/button/custom_button.cc
[modify] http://crrev.com/297ae873b471a46929ea39697b121c0b411434ee/ui/views/controls/button/custom_button.h
[modify] http://crrev.com/297ae873b471a46929ea39697b121c0b411434ee/ui/views/controls/button/custom_button_unittest.cc


### me...@chromium.org (2015-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-11-23)

Congrats your change is auto-approved for M48 (branch: 2564)

### ti...@google.com (2016-01-11)

Changing owner as meacer@ is OOO - pinged felt to take over.

### bu...@chromium.org (2016-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f9ac4cc322f57588be9b138f9b4d8df4e7cf288

commit 1f9ac4cc322f57588be9b138f9b4d8df4e7cf288
Author: felt <felt@chromium.org>
Date: Mon Jan 11 18:00:07 2016

[Merge] Custom buttons should only handle accelerators when focused.

BUG=541415

Review URL: https://codereview.chromium.org/1437523005

Cr-Commit-Position: refs/heads/master@{#360130}
(cherry picked from commit 297ae873b471a46929ea39697b121c0b411434ee)

Review URL: https://codereview.chromium.org/1576073002 .

Cr-Commit-Position: refs/branch-heads/2564@{#520}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/1f9ac4cc322f57588be9b138f9b4d8df4e7cf288/ui/views/controls/button/custom_button.cc
[modify] http://crrev.com/1f9ac4cc322f57588be9b138f9b4d8df4e7cf288/ui/views/controls/button/custom_button.h
[modify] http://crrev.com/1f9ac4cc322f57588be9b138f9b4d8df4e7cf288/ui/views/controls/button/custom_button_unittest.cc


### fe...@chromium.org (2016-01-11)

merged, assigning back to meacer.

### bu...@chromium.org (2016-01-14)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/1f9ac4cc322f57588be9b138f9b4d8df4e7cf288

commit 1f9ac4cc322f57588be9b138f9b4d8df4e7cf288
Author: felt <felt@chromium.org>
Date: Mon Jan 11 18:00:07 2016


### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### me...@google.com (2016-01-19)

+sadrul for https://codereview.chromium.org/1544803004/

### ti...@google.com (2016-01-20)

Hi Luan - our reward panel reviewed this issue and decided to award you $500 for bringing this issue to our attention. Congrats! I'll start the payment process shortly using details you've previously provided.

We'll list your name in the Chrome release notes as "Luan Herrera". If you'd like me to update it to another name, please let me know.

I'll update this bug shortly with a CVE ID for your records. Thanks again for helping secure chrome and happy bug hunting!

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1616

### ti...@google.com (2016-02-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-02)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/541415?no_tracker_redirect=1

[Multiple monorail components: Internals>Views, UI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083010)*
