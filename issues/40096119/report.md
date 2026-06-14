# Security: Possible to temporarily spoof URL by navigating back then forward

| Field | Value |
|-------|-------|
| **Issue ID** | [40096119](https://issues.chromium.org/issues/40096119) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-08-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a browser-initiated navigation is pending, a page that calls history.back/history.forward can cancel the navigation, at least in the case where the page has user activation. If a page with user activation calls history.back, immediately followed by history.forward, any pending navigation will be cancelled, but the pending URL will be left in place.

This effect is temporary, in that the original URL will be shown if the user does something like click in the omnibox or switch to another tab and back. So long as the user remains on the page, however, the pending URL will remain in place.

Because of the user activation requirement, it's easier to take advantage of this issue from an extension.

**VERSION**  

Chrome Version: Tested on 76.0.3809.132 (stable) and 78.0.3894.0 (canary)  

Operating System: Windows 10 Pro, version 1903

**REPRODUCTION CASE**

1. index.html and spoof.html form a simple website. To begin with, download the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. Click anywhere on this page. This will open a new tab at <https://www.google.com>, before navigating it to <http://localhost:8080/spoof.html>. This is done only to ensure that spoof.html can call history.back.
5. spoof.html performs the following actions in its beforeunload handler:

setTimeout(() => {  

if (navigator.userActivation.isActive) {  

history.back();  

history.forward();  

}  

}, 0);

If you attempt to navigate away from the page, the initial history.back call will override the navigation, at least when the page has user activation. The history.forward call will then effectively negate this and result in no navigation taking place at all. The pending URL will be left in place, however.

A way to test this is to click the page (therefore granting it user activation), then click a bookmark before the transient activation has expired. That is, within 5 seconds:

<https://cs.chromium.org/chromium/src/third_party/blink/common/frame/user_activation_state.cc?l=12&rcl=5fa02df01ceb1f63ec25980b717382bce5a036fc>

This should result in the omnibox being updated, but no navigation taking place.

As mentioned above, it's easier to take advantage of this issue from an extension, as an extension can navigate a tab back/forward even if there's a pending browser-initiated navigation. The example below demonstrates this:

1. manifest.json and background.js form a simple extension. Install this extension.
2. When installed, the extension will open two tabs:

- The first will point to about:blank. This tab is created to ensure that there's at least one other tab to switch to (to force the omnibox to update).
- The second will initially point to <https://example.com> and then will be navigated to <https://www.google.com/>. This navigation is done only so that the call to history.back shown below will initiate a navigation.

3. Four seconds after opening both of these tabs, the extension will run the following commands:

chrome.tabs.update(secondTab.id, {url: "chrome://settings/"});  

chrome.tabs.update(firstTab.id, {active: true});  

chrome.tabs.update(secondTab.id, {active: true});  

chrome.tabs.goBack(secondTab.id);  

chrome.tabs.goForward(secondTab.id);

This should result in the second tab (hosting <https://www.google.com/>) displaying a URL of chrome://settings/.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.0 KB)
- [index.html](attachments/index.html) (text/plain, 401 B)
- [manifest.json](attachments/manifest.json) (text/plain, 195 B)
- [spoof.html](attachments/spoof.html) (text/plain, 720 B)

## Timeline

### ct...@chromium.org (2019-08-30)

Thanks for the report! Setting this to Severity-High (control over the apparent origin in the omnibox).

Some other interesting points from looking into this:
- Triggering this for chrome://settings makes the Omnibox show the "Chrome" verbose chip. This isn't core to this bug but seems less than ideal.
- Triggering this for other URLs (e.g., https://extended-validation.badssl.com) causes the security indicator to downgrade to the (i) icon (it does not cause the security indicator of the target page to be shown -- the navigation has not actually occurred and the Omnibox is correctly in the "pending" state).

Tentatively assigning this to arthursonzogni@ and CC'ing mustaq@, as this sounds similar to https://crbug.com/chromium/987994. Do you think this may have the same overall fix (consume user activation in beforeunload)? Do we have any ideas for a short-term fix if that is truly blocked until M-82?

[Monorail components: UI>Browser>Navigation]

### ct...@chromium.org (2019-08-30)

+rdevlin.cronin@ also for extensions: The PoC extension included in the report allows an extension to get the Omnibox into a spoofed state without any user gestures (and without any extra permissions). Not sure if there's anything specific to be done on the Extensions side though (since this requires a malicious extension), but it would not be resolved by the root fix proposed in https://crbug.com/chromium/987994.

### ar...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### ar...@chromium.org (2019-08-30)

I can reproduce the first one. The pending browser initiated navigation is canceled, but its URL is still being displayed in the omnibox. It should have been cleared.

Fixing https://crbug.com/chromium/987994 will prevent the bug from happening, but it will not fix the underlying bug.
I am still not really experienced with how the URL of the pending NavigationEntry is set in the omnibox, so I will happily give this bug to someone if they want it. Otherwise, I will have to take a look.

(I haven't tried the second one with extensions.)

### mu...@chromium.org (2019-08-30)

I was able to repro both cases.  I agree this is not specific to extensions, but URL/omnibox problem.

cc-ing tommycli@chromium.org, who looks like an active owner of components/omnibox/.

### rd...@chromium.org (2019-08-30)

FWIW, we're also working on making extension-initiated navigations via chrome.tabs.update() considered renderer-initiated, not browser-initiated.  That should also help (though not solve the problem fully, since there are other ways to get a browser-initiated navigation).

### ar...@chromium.org (2019-09-02)

[Comment Deleted]

### ar...@chromium.org (2019-09-02)

WIP regression test: https://chromium-review.googlesource.com/c/chromium/src/+/1780822

I guess the fix will simply be: "Invalidate the URL whenever the visible entry is updated." (I didn't try yet)

### ar...@chromium.org (2019-09-05)

regression test: https://chromium-review.googlesource.com/c/chromium/src/+/1780822
fix: https://chromium-review.googlesource.com/c/chromium/src/+/1781434

### ar...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ar...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ar...@chromium.org (2019-09-11)

I don't know why the bot hasn't updated this bug:

(regression test landed)

~~~
Add regression test for https://crbug.com/chromium/998284.

Content's embedders are not notified the visible URL has been
invalidated. This CL adds a regression test showing this.

Bug: 998284.
Change-Id: Ib3a239d65f98209688b3b682cbe9a6184707c371
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1780822
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#695543}
~~~

I still LGTM for the fix: https://chromium-review.googlesource.com/c/chromium/src/+/1781434/7

### ar...@chromium.org (2019-09-17)

Invalidate the URL systematically when DiscardNonCommittedEntries()

The NavigationController was not invalidating the URL when a pending
entry was removed.

To fix this, be more systematic, more stupid. Always invalidate the URL
when DiscardNonCommittedEntries() is called.

Bug: 998284.
Change-Id: I01f1d16bcb25fa827bf68a52db4de531429a8564
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1781434
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Tao Bai <michaelbai@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#697145}

### ar...@chromium.org (2019-09-17)

It should be fixed now.

### sh...@chromium.org (2019-09-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-17)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-17)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2019-09-18)

Do you think it is worth merging this? I think yes.

Where do we want to merge? I think M78 Beta. Let me know if you think otherwise. I don't think we can get M77 stable.

When do we want to merge? I guess we want to see how this patch behave on Canary for a few days. It emits a few more events to WebContentsObservers asking them to refresh the displayed URL more often. That is a priori not a problem for embedders, so the risk is limited.

---

1. Does your merge fit within the Merge Decision Guidelines?
   It fixes a security issue. We are in the beginning of the beta cycle and the patch is simple enough.

2. Links to the CLs you are requesting to merge.
   https://chromium-review.googlesource.com/c/chromium/src/+/1781434

3. Has the change landed and been verified on master/ToT?
   It landed: https://chromiumdash.appspot.com/commit/69a6a1b82a0fb87e6a87b39c48416ddd59636a5c
   I verified it fixed the security issue (verified on 0fb5128005c5f5e6fae4f3bdcfc2e2f1b7abb9fe)
   
4. Why are these changes required in this milestone after branch?
   It fixes a security issue (URL spoof)

5. Is this a new feature?
   No. It is simply fixing a security issue. The issue has been there for a while.
   Note that there are similar, but still not fixed related issues.

---

I want to wait for a few days (up to 2019-09-22) to ensure this is perfectly stable on Canary.
Then, I am requesting a merge into M78 beta.


### sh...@chromium.org (2019-09-18)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-18)

merge approved for M78, branch:3904

### go...@chromium.org (2019-09-19)

Please merge your change to M78 branch 3904 ASAP, Thank you.

### sr...@google.com (2019-09-23)

Pls help complete your merges to M78 branch:3904 before end of day Monday sept 23 . I would like to include all the merges to beta release this week .

### sh...@chromium.org (2019-09-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-23)

[Empty comment from Monorail migration]

### ar...@chromium.org (2019-09-23)

The patch has been used on Canary without known issues for a few days:
79.0.3916.3 Canary → Sep 18 2019
79.0.3916.3 Dev    → Sep 19 2019

Here is the cherry-pick:
https://chromium-review.googlesource.com/c/chromium/src/+/1814828

I pre-approuved it if you want to land it without me here. I am leaving the office now.

### cr...@chromium.org (2019-09-23)

https://crbug.com/chromium/998284#c26: Great, reviewing it now.

### cr...@chromium.org (2019-09-23)

Merge landed in https://chromium-review.googlesource.com/c/chromium/src/+/1814828.  Hopefully bugdroid will update the merge labels accordingly soon.

### go...@chromium.org (2019-09-23)

Please merge your change to M78 branch 3904 ASAP so we can pick it up for this week beta release. Thank you.

### ar...@chromium.org (2019-09-24)

The bot didn't updated this issue. I will do it myself:

[M78] Invalidate the URL systematically when DiscardNonCommittedEntries()

The NavigationController was not invalidating the URL when a pending
entry was removed.

To fix this, be more systematic, more stupid. Always invalidate the URL
when DiscardNonCommittedEntries() is called.

(cherry picked from commit 69a6a1b82a0fb87e6a87b39c48416ddd59636a5c)

Bug: 998284.
Change-Id: I01f1d16bcb25fa827bf68a52db4de531429a8564
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1781434
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Tao Bai <michaelbai@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#697145}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1814828
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/branch-heads/3904@{#383}
Cr-Branched-From: 675968a8c657a3bd9c1c2c20c5d2935577bbc5e6-refs/heads/master@{#693954}

### sr...@google.com (2019-09-24)

removing the merge-approved label per https://crbug.com/chromium/998284#c28 and #30

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-09-25)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-26)

arthursonzogni@ - there's an upcoming security respin of M77, so the release TPMs will be considering the M77 merge request here. Could you add a sentence or two about whether you consider this totally safe or at all risky? Obviously to merge fixes to a stable respin we have to be extremely confident, but we do want to get security fixes merged if we can. Thanks!

### ar...@chromium.org (2019-09-27)

The patch looks quite safe to me. However:
 - There are still other ways to spoof URL found: https://crbug.com/chromium/999932. So the problems won't be solved completely.
 - It causes navigations observers to be notified of changes more often. I don't really know how the various embedders would react to it. They should react properly, but who knows. Also, I have seen a slight performance regression on Android go: https://crbug.com/chromium/1006065

On the other side, it fixes an URL spoof vulnerability, which is valuable.

### to...@chromium.org (2019-09-27)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-09-27)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-27)

Not taking this change into M77 branch

### ad...@google.com (2019-09-27)

Thanks a lot for the comment in https://crbug.com/chromium/998284#c36, really helpful. We're going to reject the merge to stable M77 due to the potential performance issue (merging things directly to stable is scary and we only want to do it where we're 110% certain it's without consequences).

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/998284?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/962892, crbug.com/chromium/962915]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096119)*
