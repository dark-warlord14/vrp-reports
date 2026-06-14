# Security: In-memory Cache UaF

| Field | Value |
|-------|-------|
| **Issue ID** | [40090967](https://issues.chromium.org/issues/40090967) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>Cache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2018-03-30 |
| **Bounty** | $10,500.00 |

## Description

**VULNERABILITY DETAILS**  

Incognito mode uses an in-memory cache to avoid writing to disk like the blockfile and simple caches. This mode suffers from an issue with sparse writes similar to the bug reported in [crbug.com/826626](https://crbug.com/826626), but the issue is limited to a single function.

See the following snippet:

```
void MemBackendImpl::EvictIfNeeded() {  
  if (current_size_ <= max_size_)  
    return;  
  
  int target_size = std::max(0, max_size_ - kDefaultEvictionSize);  
  
  base::LinkNode<MemEntryImpl>\* entry = lru_list_.head();  
  while (current_size_ > target_size && entry != lru_list_.end()) {  
    MemEntryImpl\* to_doom = entry->value();  
    entry = entry->next();  
    if (!to_doom->InUse())  
      to_doom->Doom();  
  }  
}  

```

Eviction traverses the list of entries in the lru\_list\_. The line `entry = entry->next()` keeps a pointer to the next entry to process while we potentially doom the current entry. There's a problem here: if the next entry is a child of the current entry and neither is in use, the entry pointer on the next iteration will be stale, and dooming it again will lead to a double-doom which manifests as use-after-free.

My attached patch supplies a sample fix for the issue and a unit test to demonstrate it. I resolve the issue by resetting the entry to the lru\_list\_ head when we encounter a doomable parent. It might be improved by also checking if children are present.

**VERSION**  

Chrome Version: 65 Stable  

Operating System: All (? wherever in-memory cache is deployed)

**REPRODUCTION CASE**  

See attachments

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser  

Crash State: See asan.log

## Attachments

- [inmemory_eviction.patch](attachments/inmemory_eviction.patch) (application/octet-stream, 2.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 10.3 KB)

## Timeline

### el...@chromium.org (2018-03-30)

Thanks, again!

[Monorail components: Internals>Network>Cache]

### mm...@chromium.org (2018-03-30)

jkarlin@, could you please take a look? I can't see a better owner using git blame.

morlovich@, might be helpful, as he's been recently fixing a similar bug in a blockfile cache.

------

Hey Ned, how many of those you else have? :)

### mm...@chromium.org (2018-03-30)

[Empty comment from Monorail migration]

### mo...@chromium.org (2018-03-30)

Josh, feel free to dump it on me if you're too busy (though it's all that similar --- if you want similar, see https://codereview.chromium.org/1725363005)


### jk...@chromium.org (2018-03-30)

I can take this one. Thanks for the report Ned!

### ne...@gmail.com (2018-03-30)

Sure thing guys! Don't forget to add CacheTestFillBuffer in the unittest to avoid an uninitialized read.. security is hard :p

See https://chromium.googlesource.com/chromium/src.git/+/dd44592937e7d78c7c75489d5a6e9bb0b4967f4a

@mmoroz: maybe one more, but I think these two were the worst. I have one with DoomAllEntries as well but I'm trying to figure out if there's a variant without user interaction. I'm not blocking on it though; I'll figure it out as I'm writing the next report.

### ne...@gmail.com (2018-03-30)

BTW, I thought about a better patch this morning: if the current entry is a parent and next is one of the children, either reset the next head or just move it forward to a non-child. This prevents needlessly rescanning the list and only does extra work in the exact buggy case.

### ne...@gmail.com (2018-03-30)

"reset the next head" should read "reset the current entry to head" like in the original patch. Moving next forward until it finds a non-child should be better anyways since we always close the children if the parent is to be closed, so skipping those entries shouldn't miss any doomable entries.

### mo...@chromium.org (2018-03-30)

https://chromium-review.googlesource.com/c/chromium/src/+/987919/2/net/disk_cache/memory/mem_backend_impl.cc#342

:)


### ne...@gmail.com (2018-03-30)

Ha, great minds... ;)

Thanks for the quick fixes on these! I know you guys have a lot of responsibility and these types of bugs can interfere with daily development.

### bu...@chromium.org (2018-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c9d673b54832afde658f214d7da7d0453fa89774

commit c9d673b54832afde658f214d7da7d0453fa89774
Author: Josh Karlin <jkarlin@chromium.org>
Date: Fri Mar 30 19:24:28 2018

[MemCache] Fix bug while iterating LRU list in eviction

It was possible to reanalyze a previously doomed entry.

Bug: 827492
Change-Id: I5d34d2ae87c96e0d2099e926e6eb2c1b30b01d63
Reviewed-on: https://chromium-review.googlesource.com/987919
Commit-Queue: Josh Karlin <jkarlin@chromium.org>
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/heads/master@{#547236}
[modify] https://crrev.com/c9d673b54832afde658f214d7da7d0453fa89774/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/c9d673b54832afde658f214d7da7d0453fa89774/net/disk_cache/memory/mem_backend_impl.cc


### jk...@chromium.org (2018-04-02)

Looks good over the weekend. Requesting beta merge.

### sh...@chromium.org (2018-04-02)

This bug requires manual review: Less than 11 days to go before AppStore submit on M66
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-02)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-04-02)

Branch:3359

### bu...@chromium.org (2018-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1c8fd65cc3100148f6a4b2f203312a741d09b9e

commit c1c8fd65cc3100148f6a4b2f203312a741d09b9e
Author: Josh Karlin <jkarlin@chromium.org>
Date: Mon Apr 02 18:06:43 2018

[MemCache] Fix bug while iterating LRU list in eviction

It was possible to reanalyze a previously doomed entry.

Bug: 827492
Change-Id: I5d34d2ae87c96e0d2099e926e6eb2c1b30b01d63
Reviewed-on: https://chromium-review.googlesource.com/987919
Commit-Queue: Josh Karlin <jkarlin@chromium.org>
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#547236}(cherry picked from commit c9d673b54832afde658f214d7da7d0453fa89774)
Reviewed-on: https://chromium-review.googlesource.com/990372
Reviewed-by: Josh Karlin <jkarlin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#531}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/c1c8fd65cc3100148f6a4b2f203312a741d09b9e/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/c1c8fd65cc3100148f6a4b2f203312a741d09b9e/net/disk_cache/memory/mem_backend_impl.cc


### sh...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-11)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-20)

Thanks Ned, $10,500 for the report :-)

### aw...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### ne...@gmail.com (2018-04-20)

Thank you!

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/827492?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090967)*
