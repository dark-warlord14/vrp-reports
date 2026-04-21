# URL spoofing on iOS by repeatedly navigating a new window

| Field | Value |
|-------|-------|
| **Issue ID** | [40052325](https://issues.chromium.org/issues/40052325) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>PageLoad, Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2020-05-15 |
| **Bounty** | $500.00 |

## Description

1) Go to parent.html
2) Click on the hyperlinked text
3) Observe.


Actual: 

Shown epicgames.com while the content is of twitter.com

Expected:

Update the content too.

## Attachments

- [Spoofing.mp4](attachments/Spoofing.mp4) (video/mp4, 1.5 MB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [attack1.html](attachments/attack1.html) (text/plain, 132 B)
- [Parent.html](attachments/Parent.html) (text/plain, 540 B)
- [UpdatedSpoof.mp4](attachments/UpdatedSpoof.mp4) (video/mp4, 1.6 MB)
- [TwitterSpoof.mp4](attachments/TwitterSpoof.mp4) (video/mp4, 311.7 KB)
- [Fixed.mp4](attachments/Fixed.mp4) (video/mp4, 6.1 MB)

## Timeline

### ra...@gmail.com (2020-05-15)

[Comment Deleted]

### ra...@gmail.com (2020-05-15)

I'm sorry for the above deleted files. I've updated my attachments. Please have a look here. 

Actual: 

Shown epicgames.com while the content is of google.com**

### ra...@gmail.com (2020-05-18)

[Comment Deleted]

### ra...@gmail.com (2020-05-18)

Similar to this https://crbug.com/chromium/1081081 - Note that we can spoof the lock too - no sign of loading or any thing. A perfect spoof. 

### ct...@chromium.org (2020-05-19)

Is the page interactable, or is this the same root cause as https://crbug.com/chromium/938221?

Agreed that this is an extension of https://crbug.com/chromium/1081081: the progress bar repeatedly shows because the attack uses repeated loads of the victim origin to get it to commit with a lock icon. So the fix in https://crbug.com/chromium/1081081 may have been too specific to the specific attack case rather than the underlying root cause.

Adding iOS components and creis@ since you helped out on the other iOS navigation bugs.

[Monorail components: Mobile>iOSWeb>PageLoad Mobile>iOSWeb>Security]

### ct...@chromium.org (2020-05-19)

Also setting Needs-Feedback per the question about interactability in https://crbug.com/chromium/1083337#c5

### ra...@gmail.com (2020-05-19)

Hi, The page is not interactive. However, since chrome is showing the attacker content while showing "epicgames.com" in the Omnibox. That does seem wrong.

there could be some cases where the attacker's page puts up a message for the user to read, like a phone number to call. In the end attacker wants to make sure user is convinced by his hacking skills. For eg; he can put up a message "Twitter.com is hacked by me  - If you want to hack any social media accounts Contact me on this number - $5000 for one account." - Attacker can fool many users out there since people are  crazy out there to pay thousands of bucks to have someone to hack others accounts. Using this bug, attacker can convince them paying into thousands of bucks.

### [Deleted User] (2020-05-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2020-05-19)

Regarding https://crbug.com/chromium/1083337#c7: Thanks. Agreed, but it affects how we reason about the root cause and triage the issue.

### ra...@gmail.com (2020-05-19)

[Comment Deleted]

### ct...@chromium.org (2020-05-19)

Triaging this as Severity-Medium and Impact-Stable, as this falls into the same category as https://crbug.com/chromium/1081081 (where the main mitigation is the lack of interactability).

gambard@ could you take a look at this report? It's similar to https://crbug.com/chromium/1081081 but is able to keep the lock icon security indicator by continually re-navigating the new window. Maybe we need to invalidate the security state each time? My initial guess is this is getting treated as a same-origin navigation and using a slightly different code path than the first navigation uses.

### ga...@chromium.org (2020-05-20)

To reproduce, a "bad" network is needed (e.g. simulated Edge).
This bug reproduces on Safari (with the lock). I think a bug to Apple and/or WebKit should be filed. I think it is slightly different from the other bugs.
I don't think there is anything we can do on our side:
The callbacks for the navigation is following the order of the ones expected from a "normal" navigation:
- decidePolicyForNavigationAction/Request
- didStartProvisionalNavigation
- didCommitNavigation
- didFinishNavigation
(The callbacks are slightly different from content/, didFinishNavigation indicates that the load of the page is complete, without error.)
So there is no callback on which we could update the lock.
My guess is that WebKit is actually downloading all the information from the server but the constant URL changes are preventing a repaint as the proc is too busy.

I think the OP should file the bugs to have the credit. Please add me/ajuma in cc on the WebKit bug and post the bug/radar numbers back.
cthomp@: what do you think?
+other for opinion.

### eu...@chromium.org (2020-05-20)

When does WKWebView.serverTrust change (it it even does change) in this bug?

### ga...@chromium.org (2020-05-20)

It doesn't really change.
Also, I think it is considered as a "normal" navigation. Just a long one with no repaint...

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-29)

This is more likely similar to the https://crbug.com/chromium/925598 instead of https://crbug.com/chromium/1081081 where the progress bar visibility was fixed. Hence this reproduces the  https://crbug.com/chromium/925598 

https://chromium.googlesource.com/chromium/src.git/+/b40348af225a6c6bbbc85317437a315df6554f76

### [Deleted User] (2020-06-03)

gambard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2020-06-03)

In my opinion the correct fix here is to file a radar and mark this bug as externalDependency. Assigning to creis for opinion.

I think the op should do it to get the credit for it.

### [Deleted User] (2020-06-04)

creis: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-05)

creis: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2020-06-05)

gambard@: Can you clarify (from https://crbug.com/chromium/1083337#c12) which part makes this slightly different from the other bugs, needing a new radar?

From my perspective, it looks essentially like https://crbug.com/chromium/938221, where the victim URL (epicgames.com) commits but then never gets a chance to paint because of work happening in the renderer process.  If we had a paint timer or some way to clear the previous page after a delay (as tracked in https://crbug.com/chromium/938221), the problem would likely go away.  There's a radar for that issue already.

The padlock is just an outcome of showing the committed URL (epicgames.com) instead of the pending URL (also epicgames.com) for renderer-initiated navigations.  That's intentional and (I think) managed on the Chrome side.

Is there a separate WebKit issue you're hoping gets reported?  If this is just additional repro steps for the same underlying problem, maybe it's worth posting them to the existing radar instead, as additional motivation to get it fixed?

I'll pass this back, and feel free to mark it blocked on https://crbug.com/chromium/938221 if you agree.  (Note: I'm pretty low bandwidth these days due to some other things going on.)

### ra...@gmail.com (2020-06-05)

I think this is another way to reproduce the https://crbug.com/chromium/925598 where it fixed the progress bar visibility which could be fooled when the state was changing too quickly.

### ra...@gmail.com (2020-06-05)

https://chromium.googlesource.com/chromium/src.git/+/b40348af225a6c6bbbc85317437a315df6554f76


### cr...@chromium.org (2020-06-05)

https://crbug.com/chromium/1083337#c22: Sorry, I don't understand the comparison to https://crbug.com/chromium/925598.  In this bug's video in https://crbug.com/chromium/1083337#c2, the progress bar is (correctly) showing repeatedly as the navigation commits and then new navigations are started.  In https://bugs.chromium.org/p/chromium/issues/detail?id=925598#c1, the progress bar didn't show during the attack.  Those seem like different issues.

I'll mark this as External Dependency on https://crbug.com/chromium/938221 (since this seems to be about the old page staying visible too long), but gambard@ can feel free to correct.

### ra...@gmail.com (2020-06-06)

If you see the video from 0.27 to 0.31 - the progress bar doesn't get showed. It looks like the site has been complete loaded making it purely spoofable. Note that in https://crbug.com/chromium/938221; the progress bar does get showed. 

### cr...@chromium.org (2020-06-06)

Does it stop showing completely after 0:27 in this issue, or is that just a 4 second gap where it's not shown, and it comes back?  Up to that point, it had been showing and then not showing repeatedly.

I also don't see a progress bar in issue https://crbug.com/chromium/938221, other than a brief glimpse around 2 seconds.

At any rate, the underlying issue in the code seems to still be that we aren't clearing the old page long after a commit.

### ra...@gmail.com (2020-06-06)

> Does it stop showing completely after 0:27 in this issue, or is that just a 4 second gap where it's not shown, and it comes back? 

Yes, The progress bar completely stops showing. Refer to my C#22 and C#23: This bug isn't about showing the old content because it has been tackled in other bugs. This is actually about reproducing the https://crbug.com/chromium/925598 in another way. That is, fixing the progress bar visibility (Please change the title to this). 

Expected behavior in this bug: The lock icon shouldn't be shown and progress bar visibility should be shown that the page is still loading.

The fact that it reproduces because rendering timer stops after few navigations, hence, chrome gets confused and the output is shown to the users that page is 'loaded'. 

All the other bugs you see about committing it to the old page for a long time has one thing common that it shows the progress bar to show users that navigation is still going on. I've made a video of https://crbug.com/chromium/925598 where the progress bar visibility issue is fixed and is showing. (note that it still shows old content which depends externally)

### ga...@chromium.org (2020-06-08)

I think solving https://crbug.com/chromium/938221 would indeed solve the problem here (as we would have a white screen), but I think it is an issue in itself in the sense that here the load does complete (I get all the callbacks I would get on a "normal" load). In the other examples, the load doesn't complete (i.e. it is always loading).

I don't see a way of exploiting this bug other than using the fact that it doesn't repaint.

But once again, there is nothing we can do on the Chrome side. rayyanh12, please open a bug at WebKit/Apple.

### ra...@gmail.com (2020-06-08)

I've already reported similar bugs to Apple (product-security@apple.com)

### ga...@chromium.org (2020-06-09)

Then it is an external dependency and there isn't much we can do.
creis, should we leave it as external dependency until it is fixed?

### ra...@gmail.com (2020-06-09)

Fixing the issue for the old paint could take a long time, Safari is too broken to begin with. (Not only it has the old paint issue; but the page is interactive too) - Plus, I've reported multiple bugs High-Risked of URL spoofing which are perfect issues of URL spoofing (chrome doesn't have them); They're taking too long to fix them. At-least chrome should clone this  behavior to show the progress bar visibility as 

https://chromium.googlesource.com/chromium/src.git/+/b40348af225a6c6bbbc85317437a315df6554f76

### ga...@chromium.org (2020-06-09)

Once again, I don't see what could Chrome do to prevent that. WebKit is sending all the signals that the navigation is successful and done.

### ga...@chromium.org (2020-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### eu...@chromium.org (2021-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### ra...@gmail.com (2021-08-09)

Please, check on this bug. I think this bug has been fixed.

### aj...@chromium.org (2021-08-09)

Thanks for checking, I'm no longer able to reproduce this either.

Do you happen to know which iOS version this was fixed in?

### ra...@gmail.com (2021-08-09)

It’s hard to say since I’ve the updated version of iOS. (14.7.1)

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

The VRP Panel has decided to award you $500 for this report. Thank you for reporting this issue. 

### ra...@gmail.com (2021-08-11)

Request to VRP Panel: Can you please recheck this bug as this bug is similar (or reproduces) https://crbug.com/chromium/925598 - So the reward should match, right?

### am...@chromium.org (2021-08-11)

Hello, reward decisions are not based solely on the security bug type and impact alone. Each security report is individually judged, not in comparison to the other bug reports of its type. Reward decisions made by the VRP panel take in consideration the vulnerability itself and its impact, but also quality of the report, analysis provided in the report and follow-up interactions, especially exploits, patches, and other artifacts provided. 
Reward amounts will not automatically match the reward amount for another reports of a similar security issue. Please see https://www.google.com/about/appsecurity/chrome-rewards/ for more information. 

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-18)

hello, rayyanh@, the VRP Panel declines to adjust the reward amount as the original reward amount has been deemed as adequate for this report. 
It was also recommended that you review the Chromium Community Code of Conduct (https://chromium.googlesource.com/chromium/src/+/refs/heads/main/CODE_OF_CONDUCT.md) as some of your comments to the security team and developers in bug reports and emails over time are potentially violating this code of conduct. 

We greatly appreciate your bug reports, but please remember to be respectful and kind to the community members with whom you interact in the course of discussing security issues. Thank you! 

### ra...@gmail.com (2021-08-18)

[Comment Deleted]

### [Deleted User] (2021-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1083337?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>iOSWeb>PageLoad, Mobile>iOSWeb>Security]
[Monorail blocked-on: crbug.com/chromium/938221]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052325)*
