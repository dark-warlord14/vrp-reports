# Security: Use-after-free with XSLT strip-space

| Field | Value |
|-------|-------|
| **Issue ID** | [40056191](https://issues.chromium.org/issues/40056191) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | we...@aevum.de |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-06-12 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

There's a bug in libxslt which can result in use-after-free in connection with the [xsl:strip-space](javascript:void(0);) feature. Under certain circumstances, function xsltApplyTemplates can delete text nodes which are still referenced from variables, keys or possibly other data structures.

**VERSION**  

Chrome Version: all versions  

Operating System: all systems

**REPRODUCTION CASE**  

See attachment. This should typically cause a renderer crash with STATUS\_ACCESS\_VIOLATION but the underlying issue is a use-after-free.

**CREDIT INFORMATION**  

I'm the current maintainer of libxslt and found this bug when investigating a related issue.

## Attachments

- [uaf.xml](attachments/uaf.xml) (text/plain, 912 B)
- [0001-Fix-use-after-free-in-xsltApplyTemplates.patch](attachments/0001-Fix-use-after-free-in-xsltApplyTemplates.patch) (text/plain, 6.0 KB)

## Timeline

### [Deleted User] (2021-06-12)

[Empty comment from Monorail migration]

### we...@aevum.de (2021-06-12)

Proposed fix. Just let me know when this can be committed to libxslt.

This should probably get a CVE ID as well. Please let me know if you're planning to assign one.

### mp...@chromium.org (2021-06-15)

Thanks for the report. schenney@ would you like to handle or triage this? Thanks!

[Monorail components: Blink>XML]

### [Deleted User] (2021-06-15)

[Empty comment from Monorail migration]

### sc...@chromium.org (2021-06-15)

jarhar@, it looks like the right thing here is to patch our code using the fix in https://crbug.com/chromium/1219209#c2 and wait for the new XSLT version to roll.

wellnhofer@ are you concerned with publicizing the issue by committing to libxslt? Just coordinating with us? Something else?

### we...@aevum.de (2021-06-15)

I'm just trying to coordinate with you. I haven't made anything public yet in accordance with the Chrome VRP rules.

### [Deleted User] (2021-06-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-06-15)

Thanks so much for the report!
Patch in progress here: https://chromium-review.googlesource.com/c/chromium/src/+/2965632

> Just let me know when this can be committed to libxslt.

I don't know when this would be, I've never been involved in this particular type of situation before.

> This should probably get a CVE ID as well. Please let me know if you're planning to assign one.

I've never assigned one before. I only know how to update CPE prefixes in chromium.

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79fc7bcbc940a66f4edfd2c49a5e63106074836a

commit 79fc7bcbc940a66f4edfd2c49a5e63106074836a
Author: Joey Arhar <jarhar@chromium.org>
Date: Wed Jun 16 02:41:13 2021

Fix use-after-free with XSLT strip-space

Fixed: 1219209
Change-Id: I3baab9d1b419407d964a80f10c6ca05e0294554f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965632
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/heads/master@{#892861}

[add] https://crrev.com/79fc7bcbc940a66f4edfd2c49a5e63106074836a/third_party/blink/web_tests/external/wpt/xslt/strip-space-crash.xml
[add] https://crrev.com/79fc7bcbc940a66f4edfd2c49a5e63106074836a/third_party/libxslt/chromium/Fix-use-after-free-in-xsltApplyTemplates.patch
[modify] https://crrev.com/79fc7bcbc940a66f4edfd2c49a5e63106074836a/third_party/libxslt/chromium/roll.py
[modify] https://crrev.com/79fc7bcbc940a66f4edfd2c49a5e63106074836a/third_party/libxslt/src/libxslt.spec
[modify] https://crrev.com/79fc7bcbc940a66f4edfd2c49a5e63106074836a/third_party/libxslt/src/libxslt/transform.c


### [Deleted User] (2021-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-16)

Requesting merge to stable M91 because latest trunk commit (892861) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (892861) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-16)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-06-16)

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2965632
3. The change has not landed in canary yet. Once it does, we can verify by seeing if opening the attachment in the bug description crashes the renderer or not.
4. According to https://crbug.com/chromium/1219209#c12, this should be merged to m91 and m92...?
5. Changes are required because this is a newly discovered security issue.
6. No, this is not a new feature.
7. This is not a new feature.

### ja...@chromium.org (2021-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-16)

since this isn't a small fix and the CL just landed < 24 hours ago, I'm going to suggest this bake a little more on Canary and be included for the following security respin, as we are trying to cut one this week. WDYT jahar@? 

### am...@chromium.org (2021-06-16)

*jarhar@ (sorry for the ldap typo!) 

### ja...@chromium.org (2021-06-16)

https://crbug.com/chromium/1219209#c16 that sounds good to me

### am...@chromium.org (2021-06-16)

to respond to CVE questions in comments #2 and #8 above, CVE will be issued when the bug fix is part of a stable channel release 

### sr...@google.com (2021-06-17)

Merge approved for M92 branch:4515 pls merge asap

Set the next action date to next monday so this can be verified on canary and once it looks good, go head and merge. 

### ja...@chromium.org (2021-06-17)

Thanks, merging to M92 here: https://chromium-review.googlesource.com/c/chromium/src/+/2970703

### gi...@appspot.gserviceaccount.com (2021-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/137da3f36a0bd3fb9b7e0cc85032369dfa3a3789

commit 137da3f36a0bd3fb9b7e0cc85032369dfa3a3789
Author: Joey Arhar <jarhar@chromium.org>
Date: Fri Jun 18 15:52:33 2021

Fix use-after-free with XSLT strip-space

(cherry picked from commit 79fc7bcbc940a66f4edfd2c49a5e63106074836a)

Fixed: 1219209
Change-Id: I3baab9d1b419407d964a80f10c6ca05e0294554f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965632
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#892861}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2970703
Cr-Commit-Position: refs/branch-heads/4515@{#753}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[add] https://crrev.com/137da3f36a0bd3fb9b7e0cc85032369dfa3a3789/third_party/blink/web_tests/external/wpt/xslt/strip-space-crash.xml
[add] https://crrev.com/137da3f36a0bd3fb9b7e0cc85032369dfa3a3789/third_party/libxslt/chromium/Fix-use-after-free-in-xsltApplyTemplates.patch
[modify] https://crrev.com/137da3f36a0bd3fb9b7e0cc85032369dfa3a3789/third_party/libxslt/chromium/roll.py
[modify] https://crrev.com/137da3f36a0bd3fb9b7e0cc85032369dfa3a3789/third_party/libxslt/src/libxslt.spec
[modify] https://crrev.com/137da3f36a0bd3fb9b7e0cc85032369dfa3a3789/third_party/libxslt/src/libxslt/transform.c


### am...@chromium.org (2021-06-23)

Hi, Nick (wellnhofer). The VRP Panel declines to award this report since you are the maintainer of libxslt. I originally presumed we would issue the CVE for this, but since you are the libxslt maintainer, please let me know if you would like to do that yourself, or if you would like us to do so. I'm happy to accommodate either. Thank you!  

### we...@aevum.de (2021-06-24)

That's disappointing to hear. I totally understand that you don't reward people for fixing bugs in their own code but this is an issue that was introduced 20 years ago, even before the first working release and long before I got involved in libxslt:

https://gitlab.gnome.org/GNOME/libxslt/-/commit/ed0f60dea291f7ef39a33f5e815f8ba90a72a90d
https://gitlab.gnome.org/GNOME/libxslt/-/commit/7c481a940b35d9105fb5e7549c561734cb17c8c8

It would be nice if you could clarify the conditions under which maintainers can be rewarded for reporting security issues.

Regarding the CVE ID, please go ahead and assign one.

### am...@chromium.org (2021-06-24)

Completely understand the disappointment. Thanks for the feedback about the conditions and we will take that under consideration. This will get issued a CVE ID when it ships in the next stable channel release. 

### am...@chromium.org (2021-06-28)

At this time there isn't another stable channel security respin planned for M91. Merge approved to M91 to prepare for any potential unplanned security refresh scenarios before M92 release. Please merge to branch 4472 at your convenience. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d8558e4bbec758766c982b27386180e5fd76ce93

commit d8558e4bbec758766c982b27386180e5fd76ce93
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Jun 29 00:39:04 2021

Fix use-after-free with XSLT strip-space

(cherry picked from commit 79fc7bcbc940a66f4edfd2c49a5e63106074836a)

Fixed: 1219209
Change-Id: I3baab9d1b419407d964a80f10c6ca05e0294554f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965632
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#892861}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2993208
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1533}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[add] https://crrev.com/d8558e4bbec758766c982b27386180e5fd76ce93/third_party/blink/web_tests/external/wpt/xslt/strip-space-crash.xml
[add] https://crrev.com/d8558e4bbec758766c982b27386180e5fd76ce93/third_party/libxslt/chromium/Fix-use-after-free-in-xsltApplyTemplates.patch
[modify] https://crrev.com/d8558e4bbec758766c982b27386180e5fd76ce93/third_party/libxslt/chromium/roll.py
[modify] https://crrev.com/d8558e4bbec758766c982b27386180e5fd76ce93/third_party/libxslt/src/libxslt/transform.c


### [Deleted User] (2021-07-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2021-07-02)

This was merged to M91 in https://crbug.com/chromium/1219209#c27, I'm not sure why the labels weren't automatically updated.

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### we...@aevum.de (2021-07-21)

This is now fixed upstream: https://gitlab.gnome.org/GNOME/libxslt/-/commit/50f9c9cd3b7dfe9b3c8c795247752d1fdcadcac8

### rz...@google.com (2021-07-26)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7741771f84bcc8ddbd2d568c65612af18e2e33fa

commit 7741771f84bcc8ddbd2d568c65612af18e2e33fa
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Jul 28 09:34:36 2021

[M90-LTS] Fix use-after-free with XSLT strip-space

(cherry picked from commit 79fc7bcbc940a66f4edfd2c49a5e63106074836a)

Fixed: 1219209
Change-Id: I3baab9d1b419407d964a80f10c6ca05e0294554f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2965632
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#892861}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3042731
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1545}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[add] https://crrev.com/7741771f84bcc8ddbd2d568c65612af18e2e33fa/third_party/blink/web_tests/external/wpt/xslt/strip-space-crash.xml
[add] https://crrev.com/7741771f84bcc8ddbd2d568c65612af18e2e33fa/third_party/libxslt/chromium/Fix-use-after-free-in-xsltApplyTemplates.patch
[modify] https://crrev.com/7741771f84bcc8ddbd2d568c65612af18e2e33fa/third_party/libxslt/chromium/roll.py
[modify] https://crrev.com/7741771f84bcc8ddbd2d568c65612af18e2e33fa/third_party/libxslt/src/libxslt.spec
[modify] https://crrev.com/7741771f84bcc8ddbd2d568c65612af18e2e33fa/third_party/libxslt/src/libxslt/transform.c


### rz...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-02)

As you are the maintainer of the libxslt OSS project, the Chrome VRP Panel would like to extend to you a $2000 patch bonus. We understand this is a meager monetary bonus for your OSS contributions, but we would like to extend what we can to express our appreciation for your patch efforts. 

### [Deleted User] (2021-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-10-08)

reward will be processed for donation at researcher's request 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1219209?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056191)*
