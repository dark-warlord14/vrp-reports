# Extension has an ability to execute script in New Tab Page

| Field | Value |
|-------|-------|
| **Issue ID** | [40094017](https://issues.chromium.org/issues/40094017) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2019-02-12 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3695.0 Safari/537.36 Edg/74.0.82.0

Steps to reproduce the problem:
1. Side load attached extension
2. Go to Google.com
3. Click on extension button
4. After an alert, open a New Tab Page

What is the expected behavior?
Extension doesn't have an ability to execute script in the New Tab Page.

What went wrong?
Chrome's New Tab Page uses Service Worker and Cache. Cache API is exposed to window, and therefore it's accessible from anywhere within the origin for read/write. 

Clicking extensnion button on the New Tab Page would throw an error in extension script. This suggests that extension script is usually not allowed to execute script in a New Tab Page. But this can be  bypassed by abusing the fact that Service Worker cache used in New Tab Page can be set in www.google.com.

Did this work before? N/A 

Chrome version: 74.0.3695.0  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [NewTabPage.zip](attachments/NewTabPage.zip) (application/octet-stream, 870 B)
- [NewTabPage 2.zip](attachments/NewTabPage 2.zip) (application/octet-stream, 792 B)
- [webReq.zip](attachments/webReq.zip) (application/octet-stream, 652 B)
- [webRequest.mp4](attachments/webRequest.mp4) (video/mp4, 259.0 KB)

## Timeline

### do...@chromium.org (2019-02-12)

The extension does have activeTab permission - I would assume that is sufficient to allow it to script the current page if it's the NTP...... extensions folks?

[Monorail components: Platform>Extensions]

### Ju...@microsoft.com (2019-02-12)

Another PoC with Content Script (without activeTab permission). It would work with any permission which has ability to execute script on www.google.com

### sh...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-02-12)

> I would assume that is sufficient to allow it to script the current page if it's the NTP...... extensions folks?

Nope - we try to prevent script injection on the NTP.  That said, the fact that the NTP consumes resources from an origin we do allow injection on (google.com) causes problems.  We've locked some of these down, but others are much harder.

I don't think there's anything we can do here on the extensions side; the solution would be for the NTP to stop consuming potentially-untrusted sources.  Karan, I think there might have been another similar bug for the NTP leveraging SWs; am I remembering that correctly?

### ka...@chromium.org (2019-02-12)

Yeah this is a known issue. It is an artifact of the fact that the remote NTP is served from google.com and hence shares a service worker with it. Marking it as a dupe of crbug.com/898463.

cc'ing ramyan@ since they had mentioned that the remote NTP was going to be deprecated soon, which should fix the issue.

### ra...@chromium.org (2019-02-12)

Thanks for looping me in. As noted in c#5, remote NTP is deprecated & we're hoping to transition to the local NTP in M74. I'll update crbug.com/898463 when the service worker usage that makes this sort of issue possible is gone.

### Ju...@microsoft.com (2019-02-15)

Hi, I noticed that extension can intercept subresources of NTP with "webRequest" permission. Attaching PoC and video. Is this intended?

### ka...@chromium.org (2019-02-15)

c#7 seems like a bug. Reopening.

### ka...@chromium.org (2019-02-15)

Setting a next action date so this doesn't slip under the radar.

### me...@chromium.org (2019-02-16)

Setting severity=low based on https://crbug.com/chromium/797461 and https://crbug.com/chromium/844428. Does this affect stable channel?

### Ju...@microsoft.com (2019-02-16)

Yes, PoC video was taken with stable build on Windows.

### ka...@chromium.org (2019-02-20)

So it seems the request made for the widget can be intercepted by extensions. I was only able to repro this with the local ntp. The request seems to have the initiator "chrome-search://local-ntp" which isn't protected by the extensions code. (We do protect requests with initiator chrome://newtab/). Also, since this is a sub-frame navigation, the extension doesn't need access to the request initiator. 

The fix would be to prevent the extension from intercepting the requests with "chrome-search://local-ntp" initiator. 

That said, I am confused with the multiple origins related to the NTP, there is chrome://newtab, chrome-search://local-ntp, chrome-search://remote-ntp. What's the distinction between all of these?

Also, I am not sure if this bug has any security implications. The NTP is semi-privileged but it isn't clear if this bug allows a way to exploit that.

### ka...@chromium.org (2019-02-20)

Correction: This is also reproducible on the remote NTP where the initiator of the request is google.com.

Also in both the cases the requests are browser initiated (render process id = -1), but are still visible to the extension since it's a subframe navigation.

Again, I am not sure if requests like this should be protected. Out of abundance of caution, I'll issue a fix for the local ntp. Since the remote NTP is going to be deprecated anyway, I won't take any action for it.

### ra...@chromium.org (2019-02-21)

re https://crbug.com/chromium/931013#c13:

For any given instance, there's a default NTP - local, remote or 3rd party. chrome://newtab navigates to whatever the default is. chrome-search://local-ntp/local-ntp.html goes directly to the local ntp, whatever the default, and chrome-search://remote-ntp is used internally as the effect "instant" ntp url mapping from whatever the actual server-provided URL is (https://cs.chromium.org/chromium/src/chrome/browser/search/search.cc?l=329).



### ka...@chromium.org (2019-02-22)

Ramya: Do you know if we can make network requests with chrome-search://remote-ntp as the initiator?

### me...@chromium.org (2019-02-22)

Impact=stable per https://crbug.com/chromium/931013#c11

### ka...@chromium.org (2019-02-22)

Also, I found that the local ntp can embed a frame to google.com to show the doodle. I am not sure if we can protect requests made by that subframe. But I guess it shouldn't matter since it will be in a separate process from the NTP anyway. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2748fa4d27f9e7dac941a07f5498f31ee1d4246b

commit 2748fa4d27f9e7dac941a07f5498f31ee1d4246b
Author: Karan Bhatia <karandeepb@chromium.org>
Date: Mon Feb 25 23:16:18 2019

Extensions: Protect requests from the local NTP.

Protect requests made by the local NTP by treating the chrome-search://local-ntp
as sensitive.

BUG=931013

Change-Id: I6480bfa606be837295daff9d7fd5c906cd7dd98f
Reviewed-on: https://chromium-review.googlesource.com/c/1483874
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#635303}
[modify] https://crrev.com/2748fa4d27f9e7dac941a07f5498f31ee1d4246b/chrome/browser/extensions/api/chrome_extensions_api_client.cc
[modify] https://crrev.com/2748fa4d27f9e7dac941a07f5498f31ee1d4246b/chrome/browser/extensions/api/web_request/web_request_permissions_unittest.cc


### ka...@chromium.org (2019-02-25)

c#19 should fix this for the local NTP. 

meacer@, Devlin: Feel free to chime in but I don't think this requires a merge (the extension can only redirect some sub-frame requests).  

For the remote NTP, ramyan@: Is there a remote ntp deprecation bug I can block this on?

### rd...@chromium.org (2019-02-25)

@20 Given there are still known avenues for modification (through the SW cache), I agree that this isn't worth merging.

### ra...@chromium.org (2019-02-26)

Re https://crbug.com/chromium/931013#c17: I don't think so, but in any case, that path is deprecated, so I wouldn't spend too much time on it.

The tracking bug for remote NTP deprecation is crbug.com/583289, and the launch bug is crbug.com/775965.

### ka...@chromium.org (2019-02-26)

Thanks for clarifying Ramya.

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2019-08-21)

Talked to Ramya over chat, work on  583289 is done, closing.

### sh...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-10-31)

This issue was migrated from crbug.com/chromium/931013?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/583289]
[Monorail mergedinto: crbug.com/chromium/898463]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094017)*
