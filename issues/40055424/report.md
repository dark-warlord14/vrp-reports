# Security: HeapOverflow in MediaFeeds

| Field | Value |
|-------|-------|
| **Issue ID** | [40055424](https://issues.chromium.org/issues/40055424) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Feeds |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2021-04-02 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

When making a search in |entity\_values|[1], there is no check whether the query result is end(). If the author's type is not "person", find\_if() will return end(). Then the HeapOverflow will be triggered when the |person|[2] get accessed.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/media/feeds/media_feeds_converter.cc;l=503;drc=09a4396a448775456084fe36bb84662f5757d988>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/media/feeds/media_feeds_converter.cc;l=509;drc=09a4396a448775456084fe36bb84662f5757d988>

**VERSION**  

Chrome Version: stable  

Operating System: All

**REPRODUCTION CASE**

1. Apply the attached https.patch to bypass HTTPS check, or use an HTTPS server. It has nothing to do with the vulnerability itself.
2. $ python -m SimpleHTTPServer  
   
   $ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"
3. visit chrome://media-feeds and click "Fetch Feed" in the "Actions" column.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 50.5 KB)
- [https.patch](attachments/https.patch) (text/plain, 1.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 114 B)
- [VideoObject](attachments/VideoObject) (text/plain, 2.0 KB)

## Timeline

### [Deleted User] (2021-04-02)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-04-05)

Thanks for the report! I was able to reproduce the PoC as described. Due to the need for some unusual user gestures, triaging as High severity. If you can demonstrate the same vulnerability without having the user open chrome://media-feeds, this would be higher severity.

steimel@ - can you take a look?

### [Deleted User] (2021-04-06)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2021-04-08)

Media feeds will never be fetched without the user going to chrome://media-feeds and either manually fetching one or turning on auto-fetching (which is disabled by default and can only be turned on by going to chrome://media-feeds and turning it on).

Media feeds has recently been completely deleted here: crrev.com/c/2803838

### ct...@chromium.org (2021-04-09)

Sheriff here: Should we consider crrev.com/c/2803838 to be the "fix" for this then, and handle things accordingly (i.e., marking this Fixed, handling merges as needed, etc.)? Can we disable this via Finch for current release milestones?

[Monorail components: Internals>Media>Feeds]

### st...@chromium.org (2021-04-09)

We can disable the automatic fetching via Finch (which will help the case where a user has explicitly gone to chrome://media-feeds and turned on automatic fetching). The manual fetching by going to chrome://media-feeds and fetching a feed cannot be disabled via Finch. Not sure the best path forward for merging stuff back.

### ct...@chromium.org (2021-04-12)

Is manual fetching controlled by the kMediaFeeds flag? That seems (to my very brief uneducated skimming) to be the simplest thing to cherry-pick into release branches.

  // Enables Media Feeds to allow sites to provide specific recommendations for
  // users.
  const base::Feature kMediaFeeds{"MediaFeeds", base::FEATURE_ENABLED_BY_DEFAULT};

### st...@chromium.org (2021-04-12)

Yep you're right i missed that somehow. Should we cherry-pick a CL to disable that by default or just land a Finch config to disable by Finch?

### ct...@chromium.org (2021-04-12)

+adetaylor@ for help deciding merges vs. Finch config changes here.

### ad...@chromium.org (2021-04-13)

I think we'd marginally prefer a CL to disable it in code, because of course there are some users who don't/can't access Finch, but I don't think we have a strong preference.

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-04-22)

friendly ping

### st...@chromium.org (2021-04-22)

[Empty comment from Monorail migration]

### st...@chromium.org (2021-04-22)

Do we need some sort of merge request acceptance to land the CL? There is no existing CL for trunk, since the code is gone in M91+. My goal is to land crrev.com/c/2847504

### ad...@chromium.org (2021-04-22)

+srinivassista, +govind as I don't know the answer.

### st...@chromium.org (2021-04-27)

friendly ping

### le...@gmail.com (2021-04-30)

Hi, any updates?

### sr...@google.com (2021-04-30)

Sorry for the delay, looks like this is specific merge to M90 only and cannot land on trunk for verificaion. I see this is only making the feature disabled, so i am assuming this to be really safe to take into M90 directly. 

Only question about one of the changes. chrome/test/data/webui/media/media_feeds_webui_browsertest.js has two features enabled in the list , where as other files seem to disable/remove the list , is this intended? 

Yes we do take merges to M90 directly for cases like this, as we cannot land on trunk One last question ( is the code and feature flag cleaned up in M91+ ? and hence we cannot land this on trunk? )


### st...@chromium.org (2021-04-30)

Re: "Only question about one of the changes. chrome/test/data/webui/media/media_feeds_webui_browsertest.js has two features enabled in the list , where as other files seem to disable/remove the list , is this intended? ":

Yes, this is intended. I opted to go for the simplest way to get the tests working, and enabling for the test there was easiest

Re: "is the code and feature flag cleaned up in M91+ ? and hence we cannot land this on trunk?":

Yes, the code and flag are completely removed in trunk

### sr...@google.com (2021-05-03)

sounds good then you can land the CL to M90 once adrian approves it, adding Merge-request-90 label 

### ad...@google.com (2021-05-04)

Approving merge to M90, branch 4430. Please merge by EOD PST Thursday for inclusion in next week's security refresh. Please mark this as Fixed too.

### st...@chromium.org (2021-05-04)

[Empty comment from Monorail migration]

### go...@chromium.org (2021-05-04)

Please merge your change to M90 branch 4430 ASAP so we can pick it up for next M90 respin. Thank you.

### gi...@appspot.gserviceaccount.com (2021-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b064a73431541e520d273c227e762983c2f177b7

commit b064a73431541e520d273c227e762983c2f177b7
Author: Tommy Steimel <steimel@chromium.org>
Date: Tue May 04 19:30:56 2021

Media Feeds: Disable Media Feeds and related features in M90

Media Feeds is deleted in M91 and later and is unused in previous
versions as well. There is a security issue with Media Feeds though, so
we'd like to force it to be disabled in previous versions, so this CL
turns it off for M90.

Bug: 1195340
Change-Id: I29e18be2abe4c1b4560d6324af3b6da93a97d947
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2847504
Reviewed-by: dpapad <dpapad@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1389}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b064a73431541e520d273c227e762983c2f177b7/chrome/browser/ui/webui/chrome_url_data_manager_browsertest.cc
[modify] https://crrev.com/b064a73431541e520d273c227e762983c2f177b7/chrome/test/data/webui/media/media_feeds_webui_browsertest.js
[modify] https://crrev.com/b064a73431541e520d273c227e762983c2f177b7/chrome/test/data/webui/media/media_history_webui_browsertest.js
[modify] https://crrev.com/b064a73431541e520d273c227e762983c2f177b7/media/base/media_switches.cc


### ad...@google.com (2021-05-06)

steimel@ thanks! Please could you mark this as Fixed too?

### st...@chromium.org (2021-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b255003117360100eb7c79f9caedf54dddda9fcd

commit b255003117360100eb7c79f9caedf54dddda9fcd
Author: Tommy Steimel <steimel@chromium.org>
Date: Wed May 12 09:22:21 2021

Media Feeds: Disable Media Feeds and related features in M90

Media Feeds is deleted in M91 and later and is unused in previous
versions as well. There is a security issue with Media Feeds though, so
we'd like to force it to be disabled in previous versions, so this CL
turns it off for M90.

(cherry picked from commit b064a73431541e520d273c227e762983c2f177b7)

Bug: 1195340
Change-Id: I29e18be2abe4c1b4560d6324af3b6da93a97d947
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2847504
Reviewed-by: dpapad <dpapad@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1389}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2884070
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430_101@{#22}
Cr-Branched-From: 3e9034a21f4b1f6707146b1309e001c3321ab48a-refs/branch-heads/4430@{#1364}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/b255003117360100eb7c79f9caedf54dddda9fcd/chrome/browser/ui/webui/chrome_url_data_manager_browsertest.cc
[modify] https://crrev.com/b255003117360100eb7c79f9caedf54dddda9fcd/chrome/test/data/webui/media/media_feeds_webui_browsertest.js
[modify] https://crrev.com/b255003117360100eb7c79f9caedf54dddda9fcd/chrome/test/data/webui/media/media_history_webui_browsertest.js
[modify] https://crrev.com/b255003117360100eb7c79f9caedf54dddda9fcd/media/base/media_switches.cc


### gi...@google.com (2021-05-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b45be0604d27b3e644978e57f581e810a65edca5

commit b45be0604d27b3e644978e57f581e810a65edca5
Author: Tommy Steimel <steimel@chromium.org>
Date: Wed May 12 19:03:44 2021

Media Feeds: Disable Media Feeds and related features in M90

Media Feeds is deleted in M91 and later and is unused in previous
versions as well. There is a security issue with Media Feeds though, so
we'd like to force it to be disabled in previous versions, so this CL
turns it off for M90.

(cherry picked from commit b064a73431541e520d273c227e762983c2f177b7)

Bug: 1195340
Change-Id: I29e18be2abe4c1b4560d6324af3b6da93a97d947
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2847504
Reviewed-by: dpapad <dpapad@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1389}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2883741
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1639}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/b45be0604d27b3e644978e57f581e810a65edca5/chrome/browser/ui/webui/chrome_url_data_manager_browsertest.cc
[modify] https://crrev.com/b45be0604d27b3e644978e57f581e810a65edca5/chrome/test/data/webui/media/media_feeds_webui_browsertest.js
[modify] https://crrev.com/b45be0604d27b3e644978e57f581e810a65edca5/chrome/test/data/webui/media/media_history_webui_browsertest.js
[modify] https://crrev.com/b45be0604d27b3e644978e57f581e810a65edca5/media/base/media_switches.cc


### am...@google.com (2021-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-12)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $15,000 for this report. Excellent work! 

### am...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195340?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055424)*
