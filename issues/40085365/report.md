# Unable to block cookies

| Field | Value |
|-------|-------|
| **Issue ID** | [40085365](https://issues.chromium.org/issues/40085365) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Permissions, Privacy |
| **Reporter** | pa...@gmail.com |
| **Assignee** | ls...@chromium.org |
| **Created** | 2016-09-10 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2856.0 Safari/537.36

Steps to reproduce the problem:
1. go to a website that has cookies
2. select a cookie (like doubleclick.net) and click on <block> (I have chromium in german)
3. It prompts you to refresh the page

What is the expected behavior?
After refresh the cookie (or the domain holding cookies) should be seen at the "blocked"-top on the cookie list

What went wrong?
The same cookie domain is visible on the cookie tab and nothing got blocked.

Did this work before? Yes Probably the versions before this?

Chrome version: 55.0.2856.0  Channel: n/a
OS Version: Linux Kachel 4.4.0-36-generic #55-Ubuntu SMP Thu Aug 11 18:01:55 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
Flash Version: 

I've downloaded the daily build of chromium from https://download-chromium.appspot.com/

## Timeline

### el...@chromium.org (2016-09-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Permissions]

### wf...@chromium.org (2016-09-12)

I can repro in 55.0.2858.0 canary (64-bit) but not in 53.0.2785.101 m (64-bit) so this seems like a regression.

[Monorail components: Privacy]

### wf...@chromium.org (2016-09-12)

You are probably looking for a change made after 408064 (known good), but no later than 408071 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/e8d5056..32dad58?pretty=fuller

looks like https://codereview.chromium.org/2075103002 -> lshang

### wf...@chromium.org (2016-09-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-09-12)

This CL was initially in 54.0.2810.0 so it's actually in M54 already? Please address this as soon as possible since this seems like quite a serious regression to me.

### ra...@chromium.org (2016-09-13)

Thanks for catching. lshang@ I think we should probably revert the cookies change on ToT and merge the fix to M54. 

We should investigate why this is happening though, as discussed.

### sh...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742

commit 88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742
Author: lshang <lshang@chromium.org>
Date: Tue Sep 13 14:08:20 2016

Revert cookies back to be domain scoped

Revert cookie scoping back to domain-based.

BUG=645745

Review-Url: https://codereview.chromium.org/2337873002
Cr-Commit-Position: refs/heads/master@{#418233}

[modify] https://crrev.com/88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742/chrome/browser/browsing_data/cookies_tree_model_unittest.cc
[modify] https://crrev.com/88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742/chrome/browser/content_settings/host_content_settings_map_unittest.cc
[modify] https://crrev.com/88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742/components/content_settings/core/browser/content_settings_registry.cc
[modify] https://crrev.com/88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742/components/content_settings/core/browser/host_content_settings_map.cc
[modify] https://crrev.com/88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742/components/content_settings/core/browser/website_settings_info.h


### ms...@chromium.org (2016-09-13)

The revert has landed - let's see if it fixed OP's problem when it gets to Canary and merge it.

The migration to origin scoping has been reverted much earlier, so there's nothing more to do there. But we might want to consider doing backwards migration (on the same heuristic principle - assuming that all non-wildcard exceptions are wrong) to fix it retrospectively for users like the bug reporter.

More importantly, we could take advantage of these changes and of what we have learned from the problems with the migration, and finally get the cookie scoping right - and that's not to ContentSettingsPattern::FromUrl(), but to the eTLD+1.

### ls...@chromium.org (2016-09-15)

Requesting merge of #8 to M54. We did some migration in M54 and this cookie bug occurred due to the migration. This revert fix has been verified on Canary. Merging it to M54 so that the bug won't go into stable.

### di...@chromium.org (2016-09-15)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### bu...@chromium.org (2016-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8

commit 8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8
Author: Raymes Khoury <raymes@chromium.org>
Date: Thu Sep 15 02:43:04 2016

Revert cookies back to be domain scoped

Revert cookie scoping back to domain-based.

BUG=645745

Review-Url: https://codereview.chromium.org/2337873002
Cr-Commit-Position: refs/heads/master@{#418233}
(cherry picked from commit 88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742)

Review URL: https://codereview.chromium.org/2342743002 .

Cr-Commit-Position: refs/branch-heads/2840@{#372}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/chrome/browser/browsing_data/cookies_tree_model_unittest.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/chrome/browser/content_settings/host_content_settings_map_unittest.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/components/content_settings/core/browser/content_settings_registry.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/components/content_settings/core/browser/host_content_settings_map.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/components/content_settings/core/browser/website_settings_info.h


### sh...@chromium.org (2016-09-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-09-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-09-26)

Note that this affected a very specific UI path - it was still possible to block cookies through several other UI entrypoints.

### aw...@chromium.org (2016-10-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Congratulations, the panel decided to award $500 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8

commit 8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8
Author: Raymes Khoury <raymes@chromium.org>
Date: Thu Sep 15 02:43:04 2016

Revert cookies back to be domain scoped

Revert cookie scoping back to domain-based.

BUG=645745

Review-Url: https://codereview.chromium.org/2337873002
Cr-Commit-Position: refs/heads/master@{#418233}
(cherry picked from commit 88f013bd979ec30333bd7ce6c0bd2e0b5f6f2742)

Review URL: https://codereview.chromium.org/2342743002 .

Cr-Commit-Position: refs/branch-heads/2840@{#372}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/chrome/browser/browsing_data/cookies_tree_model_unittest.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/chrome/browser/content_settings/host_content_settings_map_unittest.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/components/content_settings/core/browser/content_settings_registry.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/components/content_settings/core/browser/host_content_settings_map.cc
[modify] https://crrev.com/8f5dd2a6fd71dbf05fcd87524d3a53aa3b9696c8/components/content_settings/core/browser/website_settings_info.h


### sh...@chromium.org (2016-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-04-21)

patently.paul@gmail.com - Please claim your reward by April 30 2020 otherwise it will be donated to charity. 

### na...@google.com (2020-05-05)

processing this as a donation. 

### is...@google.com (2020-05-05)

This issue was migrated from crbug.com/chromium/645745?no_tracker_redirect=1

[Multiple monorail components: Internals>Permissions, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085365)*
