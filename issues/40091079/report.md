# Security: In-memory Cache UaF 2

| Field | Value |
|-------|-------|
| **Issue ID** | [40091079](https://issues.chromium.org/issues/40091079) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>Cache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | mo...@chromium.org |
| **Created** | 2018-04-12 |
| **Bounty** | $10,500.00 |

## Description

**VULNERABILITY DETAILS**  

There's another variant of <http://crbug.com/827492> for the in-memory cache when doing cache clearing (DoomAllEntries/DoomEntriesBetween).

It appears this code path isn't reachable until the network service is enabled by default, and even then I believe renderer control is needed. If it's indeed possible to clear the in-memory cache currently then this is more severe.

Let's go ahead and fix this now so we can take our time merging the fix and don't have headaches if/when it becomes reachable.

Related network service bit - note the cache comes from the url\_request\_context which I think can have an in-memory cache:  

<https://cs.chromium.org/chromium/src/services/network/http_cache_data_remover.cc?l=140&rcl=1c257c23dc3b13c22d5121401cf997341ffe475f>

**VERSION**  

Chrome Version: 65 Stable  

Operating System: All that have in-memory/off-the-record cache

**REPRODUCTION CASE**  

See attached patch and unit test (fix.patch).

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser/Network Process  

Crash State: See asan.log

## Attachments

- [fix.patch](attachments/fix.patch) (application/octet-stream, 1.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 9.1 KB)

## Timeline

### el...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-04-13)

Assigning Critical severity since this is out of the sandbox, jkarlin: feel free to readjust to high if that seems better (since this only happens with the network service enabled). 

[Monorail components: Internals>Network>Cache]

### jk...@chromium.org (2018-04-13)

Moving this one over to Maks as I don't have the cycles at the moment.

### mm...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-14)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mo...@chromium.org (2018-04-16)

Not sure that something requiring a non-standard flag that's not set by any experiment (but which is in chrome://flags) should be ReleaseBlock.

Having said that, IIRC NetworkContext methods are only supposed to be callable from the browser process, but I am not certain of the mechanism for that.

You can indeed have an in-memory cache for a URLRequestContext --- that's what happens in incognito mode.

(Patch does look good, on my queue for today)

### mo...@chromium.org (2018-04-16)

Josh, are you too busy to review as well?

### jk...@chromium.org (2018-04-16)

Nope, can review.

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9ab771022535b499e4d7a7f12fa6c60a294f7de4

commit 9ab771022535b499e4d7a7f12fa6c60a294f7de4
Author: Maks Orlovich <morlovich@chromium.org>
Date: Tue Apr 17 01:10:32 2018

[MemCache] Fix bug while iterating LRU list in range doom

This is exact same thing as https://chromium-review.googlesource.com/c/chromium/src/+/987919
but on explicit mass-erase rather than eviction.

Thanks to nedwilliamson@ (on gmail) for the report and testcase.

Bug: 831963
Change-Id: I96a46700c1f058f7feebe038bcf983dc40eb7102
Reviewed-on: https://chromium-review.googlesource.com/1014023
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Reviewed-by: Josh Karlin <jkarlin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551205}
[modify] https://crrev.com/9ab771022535b499e4d7a7f12fa6c60a294f7de4/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/9ab771022535b499e4d7a7f12fa6c60a294f7de4/net/disk_cache/memory/mem_backend_impl.cc


### go...@chromium.org (2018-04-17)

We're not planning any further M65 releases and M66 is going to stable this week. 

Applying M-66, M-67 & M-68 labels. awhalley@, pls eveulate if for appropriate milestone merges. Thank you. 

### go...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-04-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

govind@ - good for 67

Once it's been out in Dev or Beta for a bit we can merge to 66 to pick it up in any re-spin.


### go...@chromium.org (2018-04-17)

Approving merge to M67 branch 3396 based on https://crbug.com/chromium/831963#c16. Please merge ASAP so we can pick it up for this week Dev release. Thank you.

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/76b3dbf91e4f5ebd348d53c03ef74c7fdf0b9037

commit 76b3dbf91e4f5ebd348d53c03ef74c7fdf0b9037
Author: Maks Orlovich <morlovich@chromium.org>
Date: Tue Apr 17 17:37:08 2018

[MemCache] Fix bug while iterating LRU list in range doom

This is exact same thing as https://chromium-review.googlesource.com/c/chromium/src/+/987919
but on explicit mass-erase rather than eviction.

Thanks to nedwilliamson@ (on gmail) for the report and testcase.

Bug: 831963
Change-Id: I96a46700c1f058f7feebe038bcf983dc40eb7102
Reviewed-on: https://chromium-review.googlesource.com/1014023
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Reviewed-by: Josh Karlin <jkarlin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#551205}(cherry picked from commit 9ab771022535b499e4d7a7f12fa6c60a294f7de4)
Reviewed-on: https://chromium-review.googlesource.com/1015321
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/branch-heads/3396@{#49}
Cr-Branched-From: 9ef2aa869bc7bc0c089e255d698cca6e47d6b038-refs/heads/master@{#550428}
[modify] https://crrev.com/76b3dbf91e4f5ebd348d53c03ef74c7fdf0b9037/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/76b3dbf91e4f5ebd348d53c03ef74c7fdf0b9037/net/disk_cache/memory/mem_backend_impl.cc


### sh...@chromium.org (2018-04-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-19)

Now that this has been out in Dev, requesting merge to M66 in case there's a respin.

### sh...@chromium.org (2018-04-19)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-04-23)

Approving merge for M66 branch:3359

### mo...@chromium.org (2018-04-23)

Are any special steps required for the actual merge? I've only ever done early beta ones...

(Also I am not sure of impact --- the only non-user-interaction-requiring path I can see of involves the pnacl cache, and I don't know much about that).


### bu...@chromium.org (2018-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c352625fe9db8660710e9cce16a6d92c5e09a5b5

commit c352625fe9db8660710e9cce16a6d92c5e09a5b5
Author: Maks Orlovich <morlovich@chromium.org>
Date: Wed Apr 25 16:45:03 2018

[MemCache] Fix bug while iterating LRU list in range doom

This is exact same thing as https://chromium-review.googlesource.com/c/chromium/src/+/987919
but on explicit mass-erase rather than eviction.

Thanks to nedwilliamson@ (on gmail) for the report and testcase.

Bug: 831963
Change-Id: I96a46700c1f058f7feebe038bcf983dc40eb7102
Reviewed-on: https://chromium-review.googlesource.com/1014023
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Reviewed-by: Josh Karlin <jkarlin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#551205}(cherry picked from commit 9ab771022535b499e4d7a7f12fa6c60a294f7de4)
Reviewed-on: https://chromium-review.googlesource.com/1028430
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#765}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/c352625fe9db8660710e9cce16a6d92c5e09a5b5/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/c352625fe9db8660710e9cce16a6d92c5e09a5b5/net/disk_cache/memory/mem_backend_impl.cc


### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Very nicely done, nedwilliamson@! The Chrome VRP panel decided to award $10,500 for this report and patch :-) 

### aw...@google.com (2018-04-27)

[Empty comment from Monorail migration]

### ne...@gmail.com (2018-04-27)

Wow! Thanks so much again for the generous reward!

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/831963?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091079)*
