# Security: Inappropriate implementation in PushMessaging

| Field | Value |
|-------|-------|
| **Issue ID** | [40057994](https://issues.chromium.org/issues/40057994) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PushAPI, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | mv...@chromium.org |
| **Created** | 2021-11-23 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

There are three methods (Subscribe / Unsubscribe / GetSubscription) in PushMessaging mojo interface, which use `service_worker_registration_id` to identify the service worker subscribed to push service [1].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/push_messaging/push_messaging.mojom;l=37;drc=697b310f81caec1282cea5c88b579de60690cbe0>

However, the browser side implementation do not validate that the origin of the service worker is same with the origin from the renderer side, thus a compromised renderer can leak other site's PushSubscription info, including application\_server\_key and auth which should be treated as a secret. Furthermore, attacker could subscribe to other site and send fake message for spoofing.

**VERSION**  

Chrome Version: 96.0.4664.45 + [stable, beta, or dev]

**REPRODUCTION CASE**

1. Unzip poc.zip to a directory
2. Copy js mojo bindings, install web-push library for Node.js and setup a HTTPServer  
   
   python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  
   
   npm install web-push  
   
   node ./server.js
3. Run chrome with following command  
   
   ./chrome --user-data-dir=/tmp/xxx/ --ignore-certificate-errors --enable-blink-features=MojoJS --host-rules="MAP victim.com 127.0.0.1, MAP attacker.com 127.0.0.1" <https://victim.com:8000> <https://attacker.com:8000>
4. Click 'Subscribe' button on victim.com and allow to show notification. This simulates a normal web application to to receive messages.
5. Click 'Demo' buttom on attacker.com, this demostrate the info leak and push message spoofing.

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 6.7 KB)

## Timeline

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### jt...@gmail.com (2021-11-23)

[Comment Deleted]

### rs...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-23)

Thanks for the report. The relevant browser-side code is here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/push_messaging/push_messaging_manager.cc;l=175-185;drc=1d6a095400e3d9dee58fd6bcf83d391921d4e833, including a "TODO: Validate arguments?" for the registration information coming from the renderer. It looks like that even though the PushMessagingManager is a RenderFrameHost-scoped object, it uses the registration ID passed from the renderer to directly look up the SW registration in the StorageContext-wide map, without validating that the ID is appropriate for the current RFH.

Labeling as Sev-High because I think this qualifies as a Site Isolation bypass.

[Monorail components: Blink>PushAPI]

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### mv...@chromium.org (2021-11-23)

Thanks for reporting, I'll take a look.

### [Deleted User] (2021-11-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-07)

mvanouwerkerk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mv...@chromium.org (2021-12-10)

Yes I'm working on this.

### mv...@chromium.org (2021-12-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-12-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### mv...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c941c1be502c0f84a12731007bc99952d5cc5063

commit c941c1be502c0f84a12731007bc99952d5cc5063
Author: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Date: Tue Dec 21 15:41:03 2021

In PushMessagingManager check whether renderer can access data for origin.

Bug: 1273017
Change-Id: I992d2f004224ee186ec6620a4481912cc5fdb4ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3344789
Reviewed-by: Peter Beverloo <peter@chromium.org>
Auto-Submit: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Charles Reis <creis@chromium.org>
Commit-Queue: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#953214}

[modify] https://crrev.com/c941c1be502c0f84a12731007bc99952d5cc5063/content/browser/bad_message.h
[modify] https://crrev.com/c941c1be502c0f84a12731007bc99952d5cc5063/content/browser/push_messaging/push_messaging_manager.cc
[modify] https://crrev.com/c941c1be502c0f84a12731007bc99952d5cc5063/tools/metrics/histograms/enums.xml


### mv...@chromium.org (2021-12-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-12-21)

updating as fixed based on CL and merge request; in the future, please update fixed bugs accordingly and the sheriffbot will take care of appropriate merge request labeling :) 
I'm going to leave this in the review queue for now since this fix was only recently landed, I'd like to let it get at more bake time on Canary before approving. Thanks! 

### [Deleted User] (2021-12-22)

Merge approved: your change passed merge requirements and is auto-approved for M98. Please go ahead and merge the CL to branch 4758 (refs/branch-heads/4758) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e4195bf41feace94152b62b8c0f443887e8ada6f

commit e4195bf41feace94152b62b8c0f443887e8ada6f
Author: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Date: Wed Dec 22 18:35:34 2021

Merge to release branch: In PushMessagingManager check whether renderer can access data for origin.

(cherry picked from commit c941c1be502c0f84a12731007bc99952d5cc5063)

Bug: 1273017
Change-Id: I992d2f004224ee186ec6620a4481912cc5fdb4ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3344789
Reviewed-by: Peter Beverloo <peter@chromium.org>
Auto-Submit: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Charles Reis <creis@chromium.org>
Commit-Queue: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#953214}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3353488
Reviewed-by: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#191}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/e4195bf41feace94152b62b8c0f443887e8ada6f/content/browser/bad_message.h
[modify] https://crrev.com/e4195bf41feace94152b62b8c0f443887e8ada6f/content/browser/push_messaging/push_messaging_manager.cc
[modify] https://crrev.com/e4195bf41feace94152b62b8c0f443887e8ada6f/tools/metrics/histograms/enums.xml


### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-05)

because manual merge request was done, it looks like the bot got confused and didn't add merge review/request labels for merge to M96 or M97. Given the severity and the impact back to Extended/96, adding so end up in my merge review queue and fix can be included in security refresh for Stable as well as 96/Extended. 

### [Deleted User] (2022-01-05)

Merge review required: M97 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-05)

Merge review required: M96 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in reporting this issue to us and excellent work! 

### gm...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-07)

Given the length of this fix on canary and not seeing any obvious stability or other issues, approving for merge to M96 and M97, please go ahead and merge to branches 4664 and 4692 respectively. Thank you! 

### cr...@chromium.org (2022-01-07)

There are actually crashes happening from this, unfortunately, so I wouldn't recommend merging yet.

PMM_GET_SUBSCRIPTION_INVALID_ORIGIN renderer kills (6 so far):
https://crash.corp.google.com/browse?q=expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25%5BRenderer+kill+261%5D%25%27#-propertyselector,productname:1000,productversion:100,magicsignature:50,magicsignature2:50,stablesignature:50

I don't see any reports for the other cases:
PMM_SUBSCRIBE_INVALID_ORIGIN:
https://crash.corp.google.com/browse?q=expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25%5BRenderer+kill+259%5D%25%27#-propertyselector,productname:1000,productversion:100,magicsignature:50,magicsignature2:50,stablesignature:50

PMM_UNSUBSCRIBE_INVALID_ORIGIN:
https://crash.corp.google.com/browse?q=expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25%5BRenderer+kill+260%5D%25%27#-propertyselector,productname:1000,productversion:100,magicsignature:50,magicsignature2:50,stablesignature:50


mvanouwerkerk@: Can you take a look to see why we might be failing the check in that case, and whether a change is needed before merging?

### cr...@chromium.org (2022-01-07)

mvanouwerkerk@ points out these reports are all from a single client, so it's possible that this isn't a general stability concern.  We have one theory to try to confirm, and after that it may be safe to proceed with the merge and consider this fixed.  Let's keep an eye on the reports for the moment.

### am...@chromium.org (2022-01-07)

Thanks so much for this update and digging into this. Concur with holding off merging just yet until confirm it isn't a general stability concern. We don't have any sort of cut deadline for 97 or 96 this week. 

### cr...@chromium.org (2022-01-07)

I'll set a next action date for Monday, when we can make the call.  So far, we aren't seeing more reports, so hopefully it isn't a stability issue.

### mv...@chromium.org (2022-01-10)

I checked on the theory that the original reporter might be verifying the fix on Canary, but that is apparently not the case.

Still, we now have 13 crash reports but all with the same client id, all in Canary. In Fields > Product data the expected_process_lock and killed_process_origin_lock are the same, though in a few cases reversed.

The merge to M98 was rolled out to Dev and Beta last week:
https://chromiumdash.appspot.com/commit/e4195bf41feace94152b62b8c0f443887e8ada6f
But there are no crash reports for Dev and Beta.

I suspect my original theory might still be valid, that a single person somewhere is trying it out, and that there is not yet a known use case on a site in the wild.

### mv...@chromium.org (2022-01-10)

In UMA I see a count 35 in histogram Stability.BadMessageTerminated.Content for value PMM_GET_SUBSCRIPTION_INVALID_ORIGIN. These are also all in Canary, though of course there is more lag in the UMA data than in the crash data so there has been less of a chance to collect Dev and Beta data there.

### cr...@chromium.org (2022-01-10)

Thanks!  At this point, with all reports still from a single client and only from Canary, I think you're right-- it doesn't seem like a general stability concern, and the most likely explanation is that a single person is trying out the fix.  I think it's safe to proceed with the merges and just set a reminder for a few weeks from now to confirm we're still ok.  I'll mark this fixed again!

### [Deleted User] (2022-01-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/55339e4207939a6fc7ffc9fb30e448fcfc462670

commit 55339e4207939a6fc7ffc9fb30e448fcfc462670
Author: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Date: Mon Jan 10 18:30:27 2022

Merge to M97: In PushMessagingManager check whether renderer can access data for origin.

(cherry picked from commit c941c1be502c0f84a12731007bc99952d5cc5063)

Bug: 1273017
Change-Id: I57a80030de830f4dbf1d5ec86560f45edadf6c99
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3344789
Reviewed-by: Peter Beverloo <peter@chromium.org>
Auto-Submit: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Charles Reis <creis@chromium.org>
Commit-Queue: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#953214}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3373104
Cr-Commit-Position: refs/branch-heads/4692@{#1394}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/55339e4207939a6fc7ffc9fb30e448fcfc462670/content/browser/bad_message.h
[modify] https://crrev.com/55339e4207939a6fc7ffc9fb30e448fcfc462670/content/browser/push_messaging/push_messaging_manager.cc
[modify] https://crrev.com/55339e4207939a6fc7ffc9fb30e448fcfc462670/tools/metrics/histograms/enums.xml


### gm...@google.com (2022-01-12)

[Empty comment from Monorail migration]

### cr...@chromium.org (2022-01-13)

There's a M96 merge in review for this here: https://chromium-review.googlesource.com/c/chromium/src/+/3372762

I checked the crash data from the link in https://crbug.com/chromium/1273017#c28, and we're now seeing reports from 2 different Windows clients, one exclusively M99 Canary and the other exclusively M98 Beta.  That may not be enough to conclude there's a stability bug, but we should definitely keep monitoring this.

The crash keys indicate YouTube tends to be involved, either as the requested origin (i.e., expected_process_lock) or the actual origin (i.e., killed_process_origin_lock):
count	expected_process_lock	killed_process_origin_lock
14	{ https://facebook.com/ }	{ https://youtube.com/ }
7	{ https://youtube.com/ }	{ https://facebook.com/ }
1	{ https://youtube.com/ }	{ https://twitter.com/ }

Since this is high severity and we don't see clear evidence of a functional bug yet, I'll approve the merge, but let's check back in once these merges get out to users.

### sr...@google.com (2022-01-13)

we are releasing this next week to M97 ( Merge already landed)  stable and M96 extended stable ( merge pending) I just clicked the failed bot to retry for the CL from https://crbug.com/chromium/1273017#c39. 

Pls keep a watch out for stability trends next week. 



### [Deleted User] (2022-01-13)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c51812de4d7a8614b2e445dbcb62478edc4c4f37

commit c51812de4d7a8614b2e445dbcb62478edc4c4f37
Author: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Date: Fri Jan 14 08:49:50 2022

M96: In PushMessagingManager check whether renderer can access data for origin.

M96 merge issues:
  DeprecatedGetOriginAsURL() not present in M96

(cherry picked from commit c941c1be502c0f84a12731007bc99952d5cc5063)

Bug: 1273017
Change-Id: I992d2f004224ee186ec6620a4481912cc5fdb4ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3344789
Reviewed-by: Peter Beverloo <peter@chromium.org>
Auto-Submit: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Charles Reis <creis@chromium.org>
Commit-Queue: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#953214}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3372762
Reviewed-by: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1402}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/c51812de4d7a8614b2e445dbcb62478edc4c4f37/content/browser/bad_message.h
[modify] https://crrev.com/c51812de4d7a8614b2e445dbcb62478edc4c4f37/content/browser/push_messaging/push_messaging_manager.cc
[modify] https://crrev.com/c51812de4d7a8614b2e445dbcb62478edc4c4f37/tools/metrics/histograms/enums.xml


### mv...@chromium.org (2022-01-17)

We have 29 crash reports now. There are only two client ids. They are all on Canary and Beta. They are all on Windows 10. As it stands, I don't think these merit blocking any rollouts.

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### gm...@google.com (2022-01-24)

Merged to 96. No need to cherry pick for LTS.

### cr...@chromium.org (2022-02-28)

Following up on this, it appears we now have 1860 reports of renderer kill 261 (and 136 of renderer kill 259) from the crash links in https://crbug.com/chromium/1273017#c28, mostly from stable channel and not limited to a small number of clients.  I'm concerned that there might be a real stability bug here that still needs attention.  mvanouwerkerk@, maybe you could file a new bug to track those crashes and what we might do to fix them?  (That's probably better than reverting the security fix at this point.)  Thanks!

### cr...@chromium.org (2022-03-07)

mvanouwerkerk@: Friendly ping on https://crbug.com/chromium/1273017#c47.  Can you file a bug to investigate the crashes and whether we need to make any other changes?  (I appreciate the followup changes you landed in https://crbug.com/chromium/1281894, btw!)  Thanks!

### mv...@chromium.org (2022-03-08)

Yes I see them. They do look more diverse. I've filed crbug.com/1304242 and will continue there, thanks!

### [Deleted User] (2022-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1273017?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>PushAPI, Internals>Sandbox>SiteIsolation]
[Monorail mergedwith: crbug.com/chromium/1273016]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057994)*
