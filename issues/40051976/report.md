# iOS: Omnibox doesn't display blob: origin for long URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40051976](https://issues.chromium.org/issues/40051976) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2020-04-08 |
| **Bounty** | $1,500.00 |

## Description

I was going through this issue "https://crbug.com/chromium/1321719" in firefox bugzilla to know more about blob URLS:

Here's what I observed in Chrome iOS:

You can reproduce the https://crbug.com/chromium/705778 but from a different end.

What steps will reproduce the problem?

(1) Go to this link: https://bugzilla.mozilla.org/attachment.cgi?id=8816351
(2) You'd be redirected to blob URL


What is the expected result?

...bug1321719.bmoattachments.org/...


What happens instead?

THE omni box shows:

...15-de95-45a8-9d20-c1c79d60d2be





## Attachments

- [URL spoofing.jpg](attachments/URL spoofing.jpg) (image/jpeg, 12.7 KB)
- [Simulator Screen Shot - iPhone X - 2020-04-27 at 14.50.43.png](attachments/Simulator Screen Shot - iPhone X - 2020-04-27 at 14.50.43.png) (image/png, 87.9 KB)
- [Simulator Screen Shot - iPhone X - 2020-04-27 at 14.52.16.png](attachments/Simulator Screen Shot - iPhone X - 2020-04-27 at 14.52.16.png) (image/png, 87.8 KB)
- [Android.jpeg](attachments/Android.jpeg) (image/jpeg, 18.1 KB)
- [blob.html](attachments/blob.html) (text/plain, 250 B)
- [perfect spoof.jpeg](attachments/perfect spoof.jpeg) (image/jpeg, 17.7 KB)

## Timeline

### ra...@gmail.com (2020-04-08)

Plus, I wanted to ask which could be another bug; aren't the navigation to blob URLs blacklisted by google chrome? Is this some kind of bug regression?

### xi...@chromium.org (2020-04-09)

Thanks for the report. Spoofy blob URL seems to be fixed in crbug.com/721184, but the reporter claimed the issue still exists. jdonnelly@, could you take a look from Omnibox side? Feel free to reassign if it is not the appropriate component. Thanks!

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### [Deleted User] (2020-04-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@gmail.com (2020-04-09)

Regarding C#1 - I'm not sure the correct display, "blob:https://bug13xxxxx.bmoattachments.org/...." is much less confusing. Attacker could supply the text he wanted to appear there. Could this be another bug?

### ra...@gmail.com (2020-04-09)

You can change the title: Omnibox doesn't elide origins correctly for the blob:Url (in iOS)

### me...@chromium.org (2020-04-09)

> Plus, I wanted to ask which could be another bug; aren't the navigation to blob URLs blacklisted by google chrome? Is this some kind of bug regression?

Only page initiated navigations to data: and filesystem: schemes are blocked, blob: isn't.

### xi...@chromium.org (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-10)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2020-04-11)

I'm a bit unclear about the main issue in this report-- is this iOS only?  The URL is indeed blob:https://bug1321719.bmoattachments.org/..., and Chrome is showing that correctly on Windows and even Android.  I'm guessing it's about iOS only (per https://crbug.com/chromium/1069246#c5), where the screenshot seems to show the omnibox scrolling to the end ("15-de95-45a8-9d20-c1c79d60d2be") rather than showing the beginning.

I agree that it should scroll to the beginning and show the blob:https://bug1321719.bmoattachments.org/ part in the limited available space.  jdonnelly@, are you able to help with that?  At least on desktop, I think there's already some omnibox logic that handles this scrolling.

I'll remove the other platform labels, but let us know if this affects other platforms as well.

For the other issues mentioned:
1) https://crbug.com/chromium/1069554 (which requests blocking renderer-initiated navigations to blob: URLs) is WontFix, per https://crbug.com/chromium/1069246#c6 from meacer@.

2) Re: https://crbug.com/chromium/1069246#c4: The attacker doesn't have full control over the blob's URL contents.  The blob: URL displays the origin of the page that created the blob: URL, so the attacker can't put a victim origin there.



### cr...@chromium.org (2020-04-11)

Also, I'm not sure there's a security issue here.  Can the attacker control a visible fragment to display a victim URL as if it's the committed origin?  (Not sure about the severity until we establish that part.)

### ra...@gmail.com (2020-04-11)

[Comment Deleted]

### jd...@chromium.org (2020-04-14)

stkhapugin: Can you take a look at this or find another iOS team member who could? There might be a simple fix. There's existing logic that decides to scroll to a specific part of the URL on iOS, if I recall correctly from working on it years ago. It sounds like we just want to special-case blob: URLs.

### [Deleted User] (2020-04-23)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-24)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-25)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-26)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2020-04-27)

What we already do for data:// URLs is we clip them on head, so that the user sees "data://abcdef..." instead of "...xyz". I'll add an exception for blob too. Is it just blob and data? 

### st...@chromium.org (2020-04-27)

Sending CL 2166110 out for review. Attached before&after screenshots.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b606af053557d80d06305384c4f4383a931082a9

commit b606af053557d80d06305384c4f4383a931082a9
Author: Stepan Khapugin <stkhapugin@chromium.org>
Date: Mon Apr 27 17:14:08 2020

[iOS] Clip displayed blob URLs on tail.

Use the same treatment for blob: as for data:.

Bug: 1069246
Change-Id: I051981a2807bb308205f48889ede2fa77b8569b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2166110
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Justin Donnelly <jdonnelly@chromium.org>
Auto-Submit: Stepan Khapugin <stkhapugin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#762897}

[modify] https://crrev.com/b606af053557d80d06305384c4f4383a931082a9/ios/chrome/browser/ui/location_bar/location_bar_mediator.mm


### me...@chromium.org (2020-04-27)

Stepan, could you please clarify which version in https://crbug.com/chromium/1069246#c18 is the after version? (I assume Simulator Screen Shot - iPhone X - 2020-04-27 at 14.50.43.png but wanted to ask because of the timestamps.)

### ra...@gmail.com (2020-04-27)

C#18 - Why is there a lock sign in the blob urls? There shouldn't be any lock symbol infront of blob URLs. You also need to fix this bug too.

### jd...@chromium.org (2020-04-27)

The icon in both screenshots is unlocked, indicating that the connection was not secure. Which seems semantically correct but I stkhapugin, I think it should be an "i in a circle" icon, no?

### st...@chromium.org (2020-04-28)

[Empty comment from Monorail migration]

### st...@chromium.org (2020-04-28)

Yes, you're correct, the weird icon is tracked at crbug.com/1071729

### ra...@gmail.com (2020-04-28)

Ahh, After you updated the status as "Fixed" - I thought It won't be tracked here so I opened another bug too 1075930 - So I guess mine one is duplicate, Can you update the status and cc me on the respective bug please?

### [Deleted User] (2020-04-28)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-07)

Congrats! The Panel decided to award $500 for this report. 

### na...@google.com (2020-05-07)

[Empty comment from Monorail migration]

### oc...@google.com (2020-05-08)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-08)

https://bugs.chromium.org/p/chromium/issues/detail?id=1069246#c18

States the screenshot for before and after fixture. If you notice it, It's still not fixed. It would be spoofed using long subdomain.  

Expected result should be to display:
 
blob:...719.bmoattachments.org/ae099... (bmoattachments.org should be shown perfectly)

### ra...@gmail.com (2020-05-08)

[Comment Deleted]

### ra...@gmail.com (2020-05-08)

[Comment Deleted]

### ra...@gmail.com (2020-05-08)

Yes, Works in Android too as mentioned in the https://crbug.com/chromium/1080395. ss is attached.
> Here's the URL: http://bitly.ws/8vpo

### [Deleted User] (2020-05-09)

Requesting merge to beta M83 because latest trunk commit (762897) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-09)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bi...@google.com (2020-05-11)

Does this need to be merged separately or is done as part of crbugs.com/1080395

### jd...@chromium.org (2020-05-11)

I can't access crbug.com/1080395. And I guess it's ultimately up to the security team to decide. But in my opinion, this doesn't need to be merged.

### me...@chromium.org (2020-05-11)

I think Severity=Low could have been more appropriate for this bug since the attacker has limited control over the part of the displayed URL, so I'm leaning against no merge.

Also, comments #32 to #35 indicate that this isn't completely fixed. Could we take another look and confirm?

### st...@chromium.org (2020-05-12)

The before screenshot is the one that reads "...blahblahblah"; the "after" screenshot is the one that reads "blob:blahblah...". 
I believe that we should expect users to know that blob: is not the same as http(s). After all, any shortened version of URL can be exploited, which is why we show a full version when you tap the omnibox and in Page Info. 
If the security folks think we should display "blob:abc...xyz.domain.com" please file a feature request. 

The (i) vs open-lock is tracked in another bug and is fixed on ToT. The icon was changed and then rolled back.

### ra...@gmail.com (2020-05-12)

I already created a bug, https://crbug.com/chromium/1080395; Can we have discussion over there because https://crbug.com/chromium/1080395 isn't iOS specific only. I added my comment over there, I can copy it here too.

See ss in C#35: Since I already registered authorization-microsoft.000webhostapp.com - The ss might not be very spoofing. But I can register other URLs too by judging how much area does it needs to get spoofed because using different subdomain names of long URLs will then allow something much more convincing:
"blob:https://manage.account.paypal.com.ATTACKER.com could be clipped to "blob:https://manage.account.paypal.com" or  "blob:https://login.apple.com.MYATTACKINGSITE.com" could be clipped to "blob:https://login.apple.com" which will look more convincing to the users.

### ra...@gmail.com (2020-05-12)

[Comment Deleted]

### cr...@chromium.org (2020-05-14)

https://crbug.com/chromium/1069246#c42: Thanks for following up about the origin elision issue.  I can confirm that reproduces on Android (and it appears to still be an issue on iOS after the fix here), so I've reopened https://crbug.com/chromium/1080395 as a separate issue.

### ra...@gmail.com (2020-05-15)

[Comment Deleted]

### ra...@gmail.com (2020-05-15)

friendly disagreement: Hi, I kind of disagree with the reward and the risk it has been marked. Just like https://crbug.com/chromium/705778 is marked high; The ss clearly states that omni box is perfectly stating https://google.com. I believe this bug deserves much more than what has been given(which is the lowest of URL spoofing).
.
If you compare the screenshot from the https://crbug.com/chromium/709417; This spoofing is much more convincing. (without any ipaddress). Don't you think it should at least match the same reward? Can the VRP Panel recheck this issue regarding the reward? Thank you.

### ra...@gmail.com (2020-05-15)

[Comment Deleted]

### bi...@google.com (2020-05-18)

Merge to M83 pending decision from Security. 

### cr...@chromium.org (2020-05-19)

https://crbug.com/chromium/1069246#c46 provides a PoC to answer my question from https://crbug.com/chromium/1069246#c10, about whether it's possible to show a fragment or path at the end of the blob URL that looks like a spoof.  Using location.replace, it does appear mostly possible (without relying on the long subdomain problem tracked separately in https://crbug.com/chromium/1080395).  There are slight mitigating factors given the "..." in the address bar before the URL and an (i) instead of a padlock, but I'm not sure if those are enough to lower from High to Medium severity.  

adetaylor@ or awhalley@: I suspect this was rated Medium due to the non-concerning screenshot in https://crbug.com/chromium/1069246#c0.  Given the more effective PoC in https://crbug.com/chromium/1069246#c46, do you want to update this to High?

### ra...@gmail.com (2020-05-19)

[Comment Deleted]

### ad...@google.com (2020-05-19)

Even if this is upgraded to High, we're still not going to hold tomorrow's stable release to wait for it.

That said, given that the fix is very simple, and since it's at least nudging the upper end of Medium severity, I'll approve this merge to M83 in case there's a future M83 refresh. Approving merge to M83 (branch 4103).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f83437120b783da1903720dbae62716b5860f896

commit f83437120b783da1903720dbae62716b5860f896
Author: Stepan Khapugin <stkhapugin@chromium.org>
Date: Wed May 20 17:29:33 2020

[iOS] Clip displayed blob URLs on tail.

Use the same treatment for blob: as for data:.

(cherry picked from commit b606af053557d80d06305384c4f4383a931082a9)

Bug: 1069246
Change-Id: I051981a2807bb308205f48889ede2fa77b8569b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2166110
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Justin Donnelly <jdonnelly@chromium.org>
Auto-Submit: Stepan Khapugin <stkhapugin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#762897}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2210501
Reviewed-by: Stepan Khapugin <stkhapugin@chromium.org>
Commit-Queue: Stepan Khapugin <stkhapugin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#578}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/f83437120b783da1903720dbae62716b5860f896/ios/chrome/browser/ui/location_bar/location_bar_mediator.mm


### na...@google.com (2020-05-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ra...@gmail.com (2020-05-28)

[Comment Deleted]

### na...@google.com (2020-05-29)

Congrats! Due to the better POC demonstration in https://crbug.com/chromium/1069246#c46, the Panel re-evaluated this report as a medium severity and decided to award an additional $1,000 for this report. Please take a look at our high quality report guidelines for increased rewards. 



 *Please note this report was already rewarded $500 in PO# 1010108228. 

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1069246?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/1069554, crbug.com/chromium/1080395]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051976)*
