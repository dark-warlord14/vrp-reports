# Security: storage estimate allows obtaining size of cached cross-origin resource

| Field | Value |
|-------|-------|
| **Issue ID** | [40094891](https://issues.chromium.org/issues/40094891) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>Quota, Internals>Network>Cache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2019-05-07 |
| **Bounty** | $500.00 |

## Description

The available quota is calculated as min(10% available disk space, 2GB); by opening/prerendering a website, certain resources might be cached. This will affect the available disk space (and the quota). By observing the quota before and after opening the website, it's possible to obtain the (exact) size of the cached resources (if an attacker can trick the website in loading an arbitrary (same-site) resource that will be cached, he can determine the size of any such cross-origin resource).

I created a PoC that's hosted here: https://lab.vagosec.org/cache-spy.html

To test, click the start button a couple of times with and without the random checkbox enabled. You should see a difference with the cached (Random not checked), and uncached (Random checked); there's still some noise, but it works relatively reliably on my setup. 

## Attachments

- [cache-spy.html](attachments/cache-spy.html) (text/plain, 1.1 KB)
- [cache-spy-url.html](attachments/cache-spy-url.html) (text/plain, 1.6 KB)

## Timeline

### mk...@chromium.org (2019-05-07)

Hey Josh, who's the right person on your team to think about this kind of thing? Leaking cache is a big part of the class of attacks we're looking at in https://github.com/xsleaks/xsleaks/wiki/Browser-Side-Channels, and this kind of approach might be low-hanging fruit after we close some simpler vectors.

Setting at medium as we triage.

[Monorail components: Blink>Storage>Quota Internals>Network>Cache]

### sh...@chromium.org (2019-05-07)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@gmail.com (2019-05-07)

It's also possible to determine the response size of resources that are cached (e.g. images) without opening the new window. This somewhat defeats the defense of adding random padding when an opaque response is added via the Cache API. AppCache was a previous bypass for this (see https://www.chromestatus.com/feature/5400170344742912 and the relevant bug: https://bugs.chromium.org/p/chromium/issues/detail?id=918293)

I've put a PoC for this at https://lab.vagosec.org/cache-spy-url.html ("Random" should remain checked). This will fetch a cross-origin image (https://kul.tom.vg/medium2.jpg?100), which should get cached. A few ms after the response is received, the diff should jump to -86016; which is related to the size of the response: 78kB. There might be some other random values afterwards, which is mainly noise caused by other interactions on the disk

### me...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### js...@chromium.org (2019-05-07)

pwnall@ should evaluate/reassign.

From reading the notes here and PoC code, it implies there is some interaction between the network cache (which is not quota managed) and the quota system (which navigator.storage.estimate() presents).  In theory, those should be separate, but likely they're competing for the same underlying resource (i.e. disk space) and that's revealing data. The storage quota system should not be reliant on "available disk space" except when the disk is close to full and additional heuristics kick in - that may be what's happening here. (The PoC doesn't work for me.)

The "available quota is calculated as min(10% available disk space, 2GB)" claim is interesting; that's not how storage quota is calculated, although there is seemingly similar logic at https://cs.chromium.org/chromium/src/storage/browser/quota/quota_settings.cc?q=quota_sett&sq=package:chromium&g=0&l=116 - that's not defining the overall quota, but additional factors that come into play when the disk is nearly full, as noted above.



### to...@gmail.com (2019-05-07)

My bad, I somewhat misinterpreted "Now the minimum of a fixed value (2GB) and 10% is used to limit the reserve on devices with plenty of storage, but scale down for devices with extremely limited storage." - https://cs.chromium.org/chromium/src/storage/browser/quota/quota_settings.cc?q=quota_sett&sq=package:chromium&g=0&l=68-71

Regardless, it seems that the available quota is directly related to the total disk space:

int64_t total = disk_info_helper->AmountOfTotalDiskSpace(partition_path);
int64_t pool_size = total * kTemporaryPoolSizeRatio;

https://cs.chromium.org/chromium/src/storage/browser/quota/quota_settings.cc?sq=package:chromium&g=0&l=106-112

### js...@chromium.org (2019-05-07)

And to clarify, in AmountOfTotalDiskSpace(), "disk space" == "disk capacity", not available/free space, so by design shouldn't change as the http cache is filled. 

(Not to say that there isn't a bug/bad design lurking here!)


### sh...@chromium.org (2019-05-21)

pwnall: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2019-05-23)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-05-24)

I've been having a look at this and it seems like I can only reproduce in a low available disk space state.  Because of this, I suspect that the size-exposing attack and the fingerprinting attack can be attributed to the same piece of logic:
https://cs.chromium.org/chromium/src/storage/browser/quota/quota_manager.cc?l=275-282

I am looking to remove the branch of logic that includes available disk space it it's per-host quota calculation, which results in QuotaManager returning the same StorageEstimate.quota regardless of how much disk space is available.  

tomvangoethem@gmail.com: Do you believe this would sufficiently mitigate the attack? Note: I realize that this only addresses the size-exposing attacks that make use of StorageEstimate.quota and not those based on StorageEstimate.usage based attacks mentioned here: https://github.com/whatwg/storage/issues/31.

### to...@gmail.com (2019-05-25)

I believe that for the reported issue, removing the logic where the quota depends on the disk space, should mitigate it. The PoC I provided leverages the HTTP cache, not the Cache API; as such, it doesn't count towards the quota, but it does affect the available disk space. However, I think it would be good to also make sure that the available quota of OriginA is not affected by the quota usage of OriginB (otherwise, OriginA may trick OriginB into storing a same-site resource with the Cache API, which size can then be learned by OriginA).

The StorageEstimate.usage based attacks are mitigated by adding random padding to cross-origin opaque responses. The issues that abuse the global quota and leverage eviction as a side-channel, still exists AFAIK; they are tracked here: https://github.com/whatwg/storage/issues/70

FYI: the approach of Firefox is to keep the reported quota static for the duration of a session; this works quite well to counter size-exposing attacks (with the exception of the eviction-based ones I presume)

### sh...@chromium.org (2019-06-04)

pwnall: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### pw...@chromium.org (2019-06-05)

Updated target because the best we can do at this point is to enable a fix via Finch in M76.

### pw...@chromium.org (2019-06-17)

jarrydg@ is working on an experiment that can address this problem.

### mm...@chromium.org (2019-07-01)

jarrydg@, could you please provided an update here? Thank you!

### ja...@chromium.org (2019-07-17)

mmoroz@, I have a change that modifies the line of code referenced in C#11.  The high level idea of the change is that we no longer consider disk space availability when calculating per-host quota, and will return the same quota value despite availability. 

This change is behind a Finch experiment that has recently moved to beta, but still waiting for data to trickle in. I will post updates as the experiment moves along.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-08-07)

Requesting a merge to M-76 and M-77 for https://crrev.com/c/1736002

Change summary: For origins with unlimitedStorage permission, the Quota system will now return available disk space + usage by origin as the quota for that origin.

The fix to this bug is making quota return the same value regardless of whether or not the device is low on available disk space.  That fix is currently behind an in-flight finch trial, StaticHostQuota.  The change I am requesting merge for will allow origins with unlimitedStorage permission, such as Docs, to continue using the Quota system as a guide for their own self-eviction policies, even for users in the StaticHostQuota experiment.

I would not like this merge to force a respin of M76, but would like it to be included with any respin that may happen.

### sh...@chromium.org (2019-08-07)

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
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2019-08-07)

1. Does your merge fit within the Merge Decision Guidelines?
    Yes

2. Links to the CLs you are requesting to merge.
    https://crrev.com/c/1736002

3. Has the change landed and been verified on master/ToT?
    Yes

4. Why are these changes required in this milestone after branch?
    Docs Offline had requested this change after the experiment was in flight, noting that the experiment would cause problems for their caching and eviction strategies.  The long term solution for them is to offer a storage pressure API.  This change fills their needs until said API is prioritized and implemented.

5. Is this a new feature?
    No

6. If it is a new feature, is it behind a flag using finch?
    N/A

### sh...@chromium.org (2019-08-08)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-08-08)

+adetaylor@ for M76 merge review, please note we're cutting M76 stable respin RC for Android soon today.

### go...@chromium.org (2019-08-08)

This change is not yet baked in Beta.

### ad...@chromium.org (2019-08-08)

govind@ as this is a medium (and I agree with the assessment in https://crbug.com/chromium/960305#c1) we'd normally want to merge it to beta but not stable. So perhaps merge to M77 and leave it at that?

### sh...@chromium.org (2019-08-08)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
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

### go...@chromium.org (2019-08-08)

Re #26, sounds good. Rejecting merge to M76.

### ja...@chromium.org (2019-08-08)

I understand that the process blocks a merge to M76 stable.  I would be remiss if I did not provide some more detailed context regarding the M76 merge review, I believe I originally understated the actual reason I want to merge to stable:

I have an experiment, StaticHostQuota, that is in beta right now and awaiting leadership review to move to Stable. I'm expecting this to be at 100% within the next month (before 77 stable release).  The experimental change will have quota return the same quota value, whether or not the device is low on disk space.  Previously, Docs offline was using the diminishing quota (when low on disk space) as a signal that they were running out of disk space to use, and would adjust their caching accordingly (or start evicting data).  Since they have the unlimitedStorage permission, they cannot rely on QuotaManager to handle eviction for them, and without any insight into available disk space, they may end up with incomplete caching that is equivalent to corrupt data.  This potentially breaks the experience for end-users.

The change I am seeking to merge to M76 stable would keep that signal alive for origins with the unlimitedStorage permission, allowing Docs offline to function properly.  Without this, there is no way for them to know whether or not they have enough disk space to cache X files.

With that being said and the M76 merge being rejected, I will most likely delay the rollout of the StaticHostQuota experiment, which is a privacy improvement, until M77 stable release so as not to break the experience for Docs offline.

### ad...@chromium.org (2019-08-08)

jarrydg@ thanks for the write-up.

Let me give my thought processes too. The bar to merging stuff to an existing stable release is extremely high, because we break the internet for billions of people if we mess it up. No matter how good our testing is, there is always the risk of discovering some unexpected behavior when it hits real users. I am acutely aware that within the security team we are in a privileged position of demanding lots of such merges, and we mustn't abuse that by demanding more than is absolutely, critically, necessary.

It would be terrific to have this side-channel closed down within M76, but I don't think we can insist upon it. If the experiment has to wait till M77, we can live with that within the security team.

Now, there might be other reasons to merge this into M76 sooner. If this is blocking other strategic work, is the number one priority for the privacy team, or is a complex multi-team problem where you're co-ordinating with the Docs team, you might have a good justification for getting this into the next M76 respin rather than waiting till M77. If you'd say that's a fair description of the situation, then I'd get on a quick call with govind@ and discuss the pros and cons of merging. Just expect the bar to be very high!

### ja...@chromium.org (2019-08-08)

adetaylor@ Thank you for sharing, very insightful.  If you (the security team) can live with waiting until M77 to rollout the experimental change, then we (the storage team) are too.

Merging this change to M77 seems like the right call.  Not sure if the second merge review survey needs a separate response, but just in case and for completeness:


1. Does your merge fit within the Merge Decision Guidelines?
    Yes

2. Links to the CLs you are requesting to merge.
    https://crrev.com/c/1736002

3. Has the change landed and been verified on master/ToT?
    Yes

4. Why are these changes required in this milestone after branch?
    Docs Offline had requested this change after the experiment was in flight, noting that the experiment would cause problems for their caching and eviction strategies.  The long term solution for them is to offer a storage pressure API.  This change fills their needs until said API is prioritized and implemented.

5. Is this a new feature?
    No

6. If it is a new feature, is it behind a flag using finch?
    N/A



### sh...@chromium.org (2019-08-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### la...@google.com (2019-08-23)

merge approved for M77 branch 3865

### be...@chromium.org (2019-08-29)

This has been approved, please merge ASAP.

### ja...@chromium.org (2019-08-30)

I'm sorry, this was merged and I did not include the bug id by accident: https://crrev.com/c/1768662

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### la...@google.com (2019-09-03)

Dropping the Merge-Approved-77 label per C#39

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### pw...@chromium.org (2019-12-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ee5078fbb4116ef0f58fa7bb6230a1ff956b956e

commit ee5078fbb4116ef0f58fa7bb6230a1ff956b956e
Author: Jarryd <jarrydg@chromium.org>
Date: Thu Mar 05 23:57:49 2020

Quota: Enable StaticHostQuota by default.

Change the default behavior to enabled, update unit tests to match new
default behavior, and remove fieldtrial testing config.

Bug: 960305
Change-Id: I8f045648c73ab8787dddc2a75d576f23c13dac1d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2090451
Commit-Queue: Jarryd Goodman <jarrydg@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Steven Holte <holte@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#747480}

[modify] https://crrev.com/ee5078fbb4116ef0f58fa7bb6230a1ff956b956e/storage/browser/quota/quota_features.cc
[modify] https://crrev.com/ee5078fbb4116ef0f58fa7bb6230a1ff956b956e/storage/browser/quota/quota_manager_unittest.cc
[modify] https://crrev.com/ee5078fbb4116ef0f58fa7bb6230a1ff956b956e/testing/variations/fieldtrial_testing_config.json


### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/960305?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Storage>Quota, Internals>Network>Cache]
[Monorail blocked-on: crbug.com/chromium/965710]
[Monorail blocking: crbug.com/chromium/959839]
[Monorail mergedwith: crbug.com/chromium/954605]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094891)*
