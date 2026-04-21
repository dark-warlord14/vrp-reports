# Android/iOS: URL spoofing using long sub-domain for blob:URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40052250](https://issues.chromium.org/issues/40052250) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2020-05-07 |
| **Bounty** | $3,000.00 |

## Description

https://bugs.chromium.org/p/chromium/issues/detail?id=1069246#c18

States the screenshot for before and after fixture. If you notice it, It's still not fixed. It would be spoofed using long subdomain.  

Expected result should be to display:
 
...719.bmoattachments.org/ae099... (bmoattachments.org should be shown perfectly)





## Attachments

- [Simulator Screen Shot - iPhone X - 2020-04-27 at 14.50.43.png](attachments/Simulator Screen Shot - iPhone X - 2020-04-27 at 14.50.43.png) (image/png, 87.9 KB)
- [Simulator Screen Shot - iPhone X - 2020-04-27 at 14.52.16.png](attachments/Simulator Screen Shot - iPhone X - 2020-04-27 at 14.52.16.png) (image/png, 87.8 KB)
- [Android.jpeg](attachments/Android.jpeg) (image/jpeg, 18.1 KB)

## Timeline

### ra...@gmail.com (2020-05-07)

Similar to this bug: https://crbug.com/chromium/705778

### oc...@google.com (2020-05-08)

Please just update the original bug rather than creating a new one in the future.

### ra...@gmail.com (2020-05-08)

Okay, after leaving 3 comments there. Here's another here :P Let me gather my thoughts first I comment anything.
This bug isn't effected in only iOS but android too. 
For the suggested fixture try the same URL in Samsung internet browser. It doesn't shows blob: but show ...000.webhostapp.com... and I think it is less risked in this way. 

Here's the URL: http://bitly.ws/8vpo 

### me...@chromium.org (2020-05-11)

+jdonnelly from https://crbug.com/chromium/1069246

### ra...@gmail.com (2020-05-11)

Since I already registered authorization-microsoft.000webhostapp.com - The ss might not be very spoofing. But I can register other URLs too by judging how much area does it needs to get spoofed because using different subdomain names of long URLs will then allow something much more convincing:
"blob:https://manage.paypal.com.ATTACKER.com could be clipped to "blob:https://manage.paypal.com" or  "blob:https://login.apple.com.MYATTACKINGSITE.com" could be clipped to "login.apple.com" which will look more convincing to the users.

### cr...@chromium.org (2020-05-14)

I think this is a real issue affecting iOS and Android, separate from the iOS fix for https://crbug.com/chromium/1069246 (which was about showing the blob's path rather than the origin).  For non-blob URLs, long hostnames are elided from the left on iOS and Android (so that the long subdomain doesn't look like the eTLD+1), but that doesn't seem to be working for the origins within blob URLs.

I'm not sure how the omnibox elision code works on iOS and Android and whether that code is shared or not-- stkhapugin@, can you help find owner(s) for that?

I'll undupe this and set it to Medium severity.  It's mitigated by the fact that the full origin is still easily viewed by tapping on the address bar, but I think domain names can be chosen to look plausible enough that we should prioritize a fix.

Technically this affects desktop as well, but that's already tracked in https://crbug.com/chromium/527638.  Supposedly iOS and Android already get this right in the non-blob case, so hopefully we can apply the same elision logic to the blob case.

[Monorail components: Security UI>Browser>Omnibox UI>Security>UrlFormatting]

### [Deleted User] (2020-05-14)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-05-15)

+adetaylor@ (Security TPM) to take a look and assess for M83. 

Note: We already cut M83 stable RC for release on Tuesday. 

### ad...@chromium.org (2020-05-16)

It's medium severity and not a regression - there's no reason we'd hold M83 for it.

### go...@chromium.org (2020-05-16)

Re #10, agree. Thank you.

### st...@chromium.org (2020-05-20)

I do not understand what the desired behavior here is. I am not an expert in the URL spec. Can someone actually knowledgeable take a look here? 
Emily, could you please find a person who can clarify the desired behavior and reassign to me? 

### ra...@gmail.com (2020-05-20)

[Comment Deleted]

### [Deleted User] (2020-05-24)

estark: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-25)

estark: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-26)

estark: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-27)

estark: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-28)

estark: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-29)

estark: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-30)

estark: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-31)

estark: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-01)

estark: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-02)

estark: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-03)

estark: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-04)

estark: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2020-06-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-05)

estark: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-06)

estark: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-07)

estark: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

estark: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-10)

estark: Uh oh! This issue still open and hasn't been updated in the last 33 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2020-06-11)

Sorry I completely missed this issue.

Re #12: if the current URL is blob:https://google.com.evil.com/blahblahblah (for example) and doesn't fit in the omnibox fully, then we should show ...evil.com/blahblahblah instead of showing blob:https://google.com....

Does that clarify the desired behavior?

cc meacer who has thought about blob navigations and URL display previously.

### [Deleted User] (2020-06-11)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-12)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-13)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-14)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-15)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-16)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-17)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-18)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-19)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-20)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-21)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-22)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 33 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-23)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 34 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-24)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 35 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-25)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 36 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-26)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 37 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-28)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 39 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2020-06-29)

twellington, would you be able to suggest a good owner for this bug for Android?

(I will ping stkhapugin@ for iOS status out-of-band)

### [Deleted User] (2020-06-29)

twellington: Uh oh! This issue still open and hasn't been updated in the last 52 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2020-06-29)

This appears to be an issue with our omnibox elision logic. Passing to fgorksi@, cc'ing ender@.

### [Deleted User] (2020-06-30)

fgorski: Uh oh! This issue still open and hasn't been updated in the last 53 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-01)

fgorski: Uh oh! This issue still open and hasn't been updated in the last 54 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fg...@chromium.org (2020-07-01)

OK. OK sheriffbot. I'll take a look at this next week.

Based on https://crbug.com/chromium/1080395#c32 from estark@, this should be done this way:
if the current URL is blob:https://google.com.evil.com/blahblahblah (for example) and doesn't fit in the omnibox fully, then we should show ...evil.com/blahblahblah instead of showing blob:https://google.com....

I'll try to implement that.

Moving to M-86, but I can merge that to an earlier version if we have a reasonable fix.

### st...@chromium.org (2020-07-02)

Sorry about not noticing this earlier. 

Wait, if I'm reading this correctly, the proposed behaviour is just reverting to the old state where we don't show blob:, which will reintroduce crbug.com/1069246.

I think a good solution would be to elide like this: 
blob:...evil.com/abc....

WDYT?

### es...@chromium.org (2020-07-06)

Re #56: I don't think the proposed behavior reintroduces https://crbug.com/chromium/1069246. If I'm understanding that issue correctly, that was scrolling the URL all the way to the end, so we were showing the path. I'm proposing that we prioritize showing the blob URL's inner origin. Showing the blob: isn't important from a security perspective -- the important thing is that we show evil.com (in your example). So showing ...evil.com/blahblahblah is okay, and showing blob:https://google.com.evil.com/... is also okay, but it's not okay to show .../blahblahblah or blob:https://google.com...

### fg...@chromium.org (2020-07-08)

I started looking into this.

My first instinct was to not do any manual parsing of the URL, and try to use Java GURL or Uri instead, and both of these consider origin to be empty.

Added this to GURLJavaTest:

    @CalledByNativeJavaTest
    @SuppressWarnings(value = "AuthLeak")
    public void testBlobOriginHandling() throws URISyntaxException {
        final String kExpectedOrigin = "";
        GURL url = new GURL("blob:http://origin/guid");
        URI uri = new URI("blob:http://origin/guid");

        Assert.assertEquals(kExpectedOrigin, url.getOrigin().getSpec());
        Assert.assertEquals(kExpectedOrigin, uri.getOrigin().getSpec());
    }

Which is consistent with current expectation set by native gurl_unittest in line 370:
https://source.chromium.org/chromium/chromium/src/+/master:url/gurl_unittest.cc;l=370

This makes me think that we may need some custom code unfortunately.

Regarding https://crbug.com/chromium/1080395#c57: the way I understand the part: "showing blob:https://google.com.evil.com/... is also okay" is that it is OK to show blob:https://google.com, provided that the part with evil.com is also shown... Is that correct?

### es...@chromium.org (2020-07-08)

> Regarding https://crbug.com/chromium/1080395#c57: the way I understand the part: "showing blob:https://google.com.evil.com/... is also okay" is that it is OK to show blob:https://google.com, provided that the part with evil.com is also shown... Is that correct?

Yes, that's correct. Similarly, if you navigate to https://google[.]com[.]evil[.]com we show the whole thing in the omnibox (if it fits) and that's okay.

### fg...@chromium.org (2020-07-09)

I sent a patch for review: https://chromium-review.googlesource.com/c/chromium/src/+/2289382
It only addresses the Android part of the problem (emphasizing of origin happens in UI layer), therefore if there is work to be done for this on iOS, I may need Stepan to step in.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f0d1af8fa5b8172eb4d7908e228d11343f6e28ac

commit f0d1af8fa5b8172eb4d7908e228d11343f6e28ac
Author: Filip Gorski <fgorski@chromium.org>
Date: Fri Jul 10 13:33:44 2020

[Android][Omnibox] Fixing display of blob: URLs to show the end of origin

Adding logic that prevents inner scheme separator from being treated as
a path separator, but further consuming it when calculating the search
offset for path separator.

Bug: 1080395
Change-Id: I29f1f11b0b35e757d4cd4c75d27bc1e5ce0f5186
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2289382
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Commit-Queue: Filip Gorski <fgorski@chromium.org>
Cr-Commit-Position: refs/heads/master@{#787179}

[modify] https://crrev.com/f0d1af8fa5b8172eb4d7908e228d11343f6e28ac/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBarData.java
[modify] https://crrev.com/f0d1af8fa5b8172eb4d7908e228d11343f6e28ac/chrome/android/junit/src/org/chromium/chrome/browser/omnibox/UrlBarDataTest.java
[modify] https://crrev.com/f0d1af8fa5b8172eb4d7908e228d11343f6e28ac/components/embedder_support/android/java/src/org/chromium/components/embedder_support/util/UrlConstants.java


### fg...@chromium.org (2020-07-14)

Emily, Stepan, is there any work for this on iOS? Or can I close it, now that Android part is fixed?

### st...@chromium.org (2020-07-15)

Yes, I need to fix this for iOS as well, but I still have a question to Emily.
 
Currently on iOS we usually show the domain name, or sometimes (file://) the full URL, when the omnibox is defocused. We only ever trim the display URL on the tail and on the head.
I think you propose to show the full URL, but trimmed both at the head and at the tail to show ...om.evil.com/abc... This will work, but we don't have any logic to trim both ends of the displayed URL as of today, so this is a bit more work to implement.
Would it be OK to instead show scheme+domain, remove the path, and trim the head? This will be something like ...e.com.evil.com. 
This way I just need to reconfigure the format of the URL vs introducing new logic to compute how much of the string can we fit into a UILabel. And I think it still shows the important part (evil.com) which seems to be the goal.

Please reassign to me with a comment! 

### es...@chromium.org (2020-07-17)

Re #63: yes that would be fine, thanks! There's no need to show the path from a security perspective so that seems fine if it makes the implementation easier.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3e9e98cf97fd7524b6c1b3a908db011f659e03f9

commit 3e9e98cf97fd7524b6c1b3a908db011f659e03f9
Author: Stepan Khapugin <stkhapugin@chromium.org>
Date: Mon Jul 27 17:51:24 2020

[iOS] Adjust display URL formatting on iOS.

Makes blob: URLs just show the domain name, like all other URLs, and
formats by clipping the head.

Bug: 1080395
Change-Id: If9bf4921044dfd94bcd8cb79c53083ac49266f5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2310430
Commit-Queue: Stepan Khapugin <stkhapugin@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#791841}

[modify] https://crrev.com/3e9e98cf97fd7524b6c1b3a908db011f659e03f9/components/omnibox/browser/location_bar_model_impl.cc
[modify] https://crrev.com/3e9e98cf97fd7524b6c1b3a908db011f659e03f9/components/omnibox/browser/location_bar_model_impl_unittest.cc
[modify] https://crrev.com/3e9e98cf97fd7524b6c1b3a908db011f659e03f9/ios/chrome/browser/ui/location_bar/location_bar_mediator.mm


### ke...@chromium.org (2020-08-10)

stkhapugin@: Can this be closed or is there any follow up needed?

### ra...@gmail.com (2020-09-05)

[Comment Deleted]

### ra...@gmail.com (2020-09-25)

Friendly ping: Can you please close this bug as fixed?

### st...@chromium.org (2020-09-28)

Right, yes, this is fixed. 

### [Deleted User] (2020-09-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-05)

Not requesting merge to beta (M86) because latest trunk commit (791841) appears to be prior to beta branch point (800218). If this is incorrect, please replace the Merge-na label with Merge-Request-86. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-07)

[Comment Deleted]

### ad...@google.com (2020-10-07)

Congratulations, the VRP panel decided to award $3000 for this report ($1500 each for iOS and Android, because the fixes were in separate code so are considered separate root causes in this case).

### ad...@google.com (2020-10-08)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-10-29)

Sending to the VRP panel to reconsider this type of bug: the reporter notes that our reward here was inconsistent with what we've previously awarded in the similar https://crbug.com/chromium/1090352.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-04)

The VRP panel has decided not to alter the reward amount here.

### [Deleted User] (2021-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### is...@google.com (2021-01-20)

This issue was migrated from crbug.com/chromium/1080395?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Security, UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail mergedinto: crbug.com/chromium/1069246]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052250)*
