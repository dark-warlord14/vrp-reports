# Security: heap-buffer-overflow in gfx::RenderText::TextIndexToDisplayIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40940830](https://issues.chromium.org/issues/40940830) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | UI>GFX |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2023-11-08 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

VERSION
chrome commit run by fuzzer:
NOTE THAT IT'S NOT A GIT COMMIT FOR BISECTION.

```
commit 337b838893c1443b63acdd970ba844af5fdb4d5d (HEAD -> main, origin/main, origin/HEAD)
Author: James Zern <jzern@chromium.org>
Date:   Wed Nov 8 01:59:48 2023 +0000

    libaom,cmake_update.sh: fetch upstream tags

    Before generating aom_version.h, ensure the libaom repo has the latest
    tags. This avoids changes in aom_version.h when using a long lived tree
    to generate the configurations.

    Change-Id: I8cfa5fad4204b901f8e0b1101196a4eeedfb329f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5010899
    Reviewed-by: Wan-Teh Chang <wtc@google.com>
    Commit-Queue: James Zern <jzern@google.com>
    Cr-Commit-Position: refs/heads/main@{#1221347}
```

Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide a poc at this time. However, I have provided the ASAN log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

STEPS OF REPRO:

It is very easy to reproduce this crash WITHOUT POC.

1. Simply run: ./chrome.exe -user-data-dir=userdir --enable-features=RenderTextEarlyEliding
2. The log of address sanitizer will occurs very quickly.

BISECTION

After bisection, it is determined that the following commit introduce the issue: 1b1ae9bbc354b08dd3a04148a61908f11427ba7c

```
commit	1b1ae9bbc354b08dd3a04148a61908f11427ba7c	[log] [tgz]
author	David Yeung <dayeung@chromium.org>	Fri Nov 03 21:23:23 2023
committer	Chromium LUCI CQ <chromium-scoped@luci-project-accounts.iam.gserviceaccount.com>	Fri Nov 03 21:23:23 2023
tree	e7e15237383fe53556782e2ea6c9211f510e58bb
parent	6ad5f9c2cbafb5dca32fcab6abbb976470c859e1 [diff]
[gfx 2/5] Implement tail text eliding during layout phase

This CL will be picking up the work of an existing prototype.
https://crrev.com/c/2211075

This CL is implementing the eliding during layout (instead of
display text phase) for the ELIDE_TAIL eliding behavior.

The eliding behavior is the same and is gated under a finch
experiment but will become the default after validating
on stable channels.

1/5
https://crrev.com/c/4024384

Bug: 1085014
Change-Id: I90f44832d8c25cc8436459fdb22ebd2ed8e00c5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4919916
Reviewed-by: Etienne Bergeron <etienneb@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: David Yeung <dayeung@chromium.org>
Reviewed-by: Elaine Chien <elainechien@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1219708}
```
## Root Cause Analyze
The RenderText::TextIndexToDisplayIndex function in Chromium's codebase transforms a text index into a display index. The transformation process involves calling GetGraphemeIteratorAtTextIndex, which subsequently invokes EnsureLayoutTextUpdated and GetGraphemeIteratorAtIndex.

The EnsureLayoutTextUpdated function checks if the layout text is up-to-date. If it's not, it clears the layout_text_ and text_to_display_indices_. This last array is crucial for mapping text to display indices, and it must not be empty for the subsequent operations to work correctly.

However, there's a potential issue in GetGraphemeIteratorAtIndex. After ensuring the layout text is updated, it uses std::lower_bound to find a position in text_to_display_indices_. If the result points to the end or the index is not an exact match, it decrements the iterator. This is where the problem arises—if text_to_display_indices_ was cleared and remains empty, decrementing the iterator leads to a heap overflow when attempting to access iter->display_index.

The code assumes text_to_display_indices_ is not empty due to prior checks, but if it's cleared and not repopulated before GetGraphemeIteratorAtIndex is called, this assumption is violated, leading to undefined behavior.

https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/render_text.cc;l=2382

```
internal::GraphemeIterator RenderText::GetGraphemeIteratorAtIndex(
    const std::u16string& text,
    const size_t internal::TextToDisplayIndex::*field,
    size_t index) const {
  DCHECK_LE(index, text.length());
  if (index == text.length())
    return text_to_display_indices_.end();

  DCHECK(layout_text_up_to_date_);
  DCHECK(!text_to_display_indices_.empty());

  // The function std::lower_bound(...) finds the first not less than |index|.
  internal::GraphemeIterator iter = std::lower_bound(
      text_to_display_indices_.begin(), text_to_display_indices_.end(), index,
      [field](const internal::TextToDisplayIndex& lhs, size_t rhs) {
        return lhs.*field < rhs;
      });

  if (iter == text_to_display_indices_.end() || *iter.*field != index) {
    DCHECK(iter != text_to_display_indices_.begin());
    --iter;
  }

  return iter;
}
```

## Bisect(new)
The RenderText::GetGraphemeIteratorAtIndex function is crucial in Chromium's code for mapping between text and display indices. The function was introduced in a specific commit, and a critical issue has been identified within its logic:
https://chromium-review.googlesource.com/c/chromium/src/+/1954189

## Patch
The primary concern is the handling of text_to_display_indices_. The code uses a DCHECK to assert that this vector should not be empty, which is only active in debug builds. However, in release builds where DCHECK is not active, if text_to_display_indices_ is indeed empty, decrementing the iterator iter leads to undefined behavior, potentially causing a heap overflow.

To address this, it is suggested to replace the DCHECK(!text_to_display_indices_.empty()); with CHECK(!text_to_display_indices_.empty());, which remains active in release builds and ensures that the function fails fast if text_to_display_indices_ is empty. Alternatively, adding an explicit check for the emptiness of text_to_display_indices_ before the iterator is decremented would prevent the operation if the vector is empty, thus avoiding the heap overflow.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 12.4 KB)
- [repro.jpg](attachments/repro.jpg) (image/jpeg, 362.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 12.4 KB)
- [repro.jpg](attachments/repro.jpg) (image/jpeg, 362.2 KB)

## Timeline

### ki...@gmail.com (2023-11-08)

VULNERABILITY DETAILS

VERSION
chrome commit run by fuzzer:
NOTE THAT IT'S NOT A GIT COMMIT FOR BISECTION.

```
commit 337b838893c1443b63acdd970ba844af5fdb4d5d (HEAD -> main, origin/main, origin/HEAD)
Author: James Zern <jzern@chromium.org>
Date:   Wed Nov 8 01:59:48 2023 +0000

    libaom,cmake_update.sh: fetch upstream tags

    Before generating aom_version.h, ensure the libaom repo has the latest
    tags. This avoids changes in aom_version.h when using a long lived tree
    to generate the configurations.

    Change-Id: I8cfa5fad4204b901f8e0b1101196a4eeedfb329f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5010899
    Reviewed-by: Wan-Teh Chang <wtc@google.com>
    Commit-Queue: James Zern <jzern@google.com>
    Cr-Commit-Position: refs/heads/main@{#1221347}
```

Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide a poc at this time. However, I have provided the ASAN log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-11-08)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-11-09)

It'll be difficult for us to address this without a PoC. Are you able to provide the PoC produced by your fuzzer, even if it's not minimized?

### es...@chromium.org (2023-11-09)

Note: it appears that 1500649 is likely the same bug, with a much more detailed report and analysis.

### ki...@gmail.com (2023-11-09)

Thank you for your reply, I will try to reproduce it, if it can be reproduced, I will upload the poc as soon as possible.

### es...@chromium.org (2023-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@gmail.com (2023-11-09)

STEPS OF REPRO:

It is very easy to reproduce this crash WITHOUT POC.

1. Simply run: ./chrome.exe -user-data-dir=userdir --enable-features=RenderTextEarlyEliding
2. The log of address sanitizer will occurs very quickly.

### ki...@gmail.com (2023-11-09)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-11-09)

BISECTION

After bisection, it is determined that the following commit introduce the issue: 1b1ae9bbc354b08dd3a04148a61908f11427ba7c

```
commit	1b1ae9bbc354b08dd3a04148a61908f11427ba7c	[log] [tgz]
author	David Yeung <dayeung@chromium.org>	Fri Nov 03 21:23:23 2023
committer	Chromium LUCI CQ <chromium-scoped@luci-project-accounts.iam.gserviceaccount.com>	Fri Nov 03 21:23:23 2023
tree	e7e15237383fe53556782e2ea6c9211f510e58bb
parent	6ad5f9c2cbafb5dca32fcab6abbb976470c859e1 [diff]
[gfx 2/5] Implement tail text eliding during layout phase

This CL will be picking up the work of an existing prototype.
https://crrev.com/c/2211075

This CL is implementing the eliding during layout (instead of
display text phase) for the ELIDE_TAIL eliding behavior.

The eliding behavior is the same and is gated under a finch
experiment but will become the default after validating
on stable channels.

1/5
https://crrev.com/c/4024384

Bug: 1085014
Change-Id: I90f44832d8c25cc8436459fdb22ebd2ed8e00c5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4919916
Reviewed-by: Etienne Bergeron <etienneb@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: David Yeung <dayeung@chromium.org>
Reviewed-by: Elaine Chien <elainechien@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1219708}
```



### es...@chromium.org (2023-11-09)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-11-09)

VRP: please see https://bugs.chromium.org/p/chromium/issues/detail?id=1500649#c6 and the previous comments in that bug. This was a dupe but https://crbug.com/chromium/1500649 was a very high-quality report and the reporter also had some difficulty submitting.

### es...@chromium.org (2023-11-09)

dayeung@, can you please take a look? Also, can you please confirm that the feature isn't enabled for any users? It looks like the experiment is in a preperiod phase and thus shouldn't be enabled for any users.

[Monorail components: UI>GFX]

### da...@chromium.org (2023-11-10)

I can confirm that the feature is disabled by default and it shouldn't be running. There were other issues that I'm investigating which can cause crashes hence why the flag is disabled. I don't have permission to see https://bugs.chromium.org/p/chromium/issues/detail?id=1500649#c6 but if this can repro without the flag, I'll revert the change.

### ki...@gmail.com (2023-11-10)

## Root Cause Analyze
The RenderText::TextIndexToDisplayIndex function in Chromium's codebase transforms a text index into a display index. The transformation process involves calling GetGraphemeIteratorAtTextIndex, which subsequently invokes EnsureLayoutTextUpdated and GetGraphemeIteratorAtIndex.

The EnsureLayoutTextUpdated function checks if the layout text is up-to-date. If it's not, it clears the layout_text_ and text_to_display_indices_. This last array is crucial for mapping text to display indices, and it must not be empty for the subsequent operations to work correctly.

However, there's a potential issue in GetGraphemeIteratorAtIndex. After ensuring the layout text is updated, it uses std::lower_bound to find a position in text_to_display_indices_. If the result points to the end or the index is not an exact match, it decrements the iterator. This is where the problem arises—if text_to_display_indices_ was cleared and remains empty, decrementing the iterator leads to a heap overflow when attempting to access iter->display_index.

The code assumes text_to_display_indices_ is not empty due to prior checks, but if it's cleared and not repopulated before GetGraphemeIteratorAtIndex is called, this assumption is violated, leading to undefined behavior.

https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/render_text.cc;l=2382

```
internal::GraphemeIterator RenderText::GetGraphemeIteratorAtIndex(
    const std::u16string& text,
    const size_t internal::TextToDisplayIndex::*field,
    size_t index) const {
  DCHECK_LE(index, text.length());
  if (index == text.length())
    return text_to_display_indices_.end();

  DCHECK(layout_text_up_to_date_);
  DCHECK(!text_to_display_indices_.empty());

  // The function std::lower_bound(...) finds the first not less than |index|.
  internal::GraphemeIterator iter = std::lower_bound(
      text_to_display_indices_.begin(), text_to_display_indices_.end(), index,
      [field](const internal::TextToDisplayIndex& lhs, size_t rhs) {
        return lhs.*field < rhs;
      });

  if (iter == text_to_display_indices_.end() || *iter.*field != index) {
    DCHECK(iter != text_to_display_indices_.begin());
    --iter;
  }

  return iter;
}
```

## Bisect(new)
The RenderText::GetGraphemeIteratorAtIndex function is crucial in Chromium's code for mapping between text and display indices. The function was introduced in a specific commit, and a critical issue has been identified within its logic:
https://chromium-review.googlesource.com/c/chromium/src/+/1954189

## Patch
The primary concern is the handling of text_to_display_indices_. The code uses a DCHECK to assert that this vector should not be empty, which is only active in debug builds. However, in release builds where DCHECK is not active, if text_to_display_indices_ is indeed empty, decrementing the iterator iter leads to undefined behavior, potentially causing a heap overflow.

To address this, it is suggested to replace the DCHECK(!text_to_display_indices_.empty()); with CHECK(!text_to_display_indices_.empty());, which remains active in release builds and ensures that the function fails fast if text_to_display_indices_ is empty. Alternatively, adding an explicit check for the emptiness of text_to_display_indices_ before the iterator is decremented would prevent the operation if the vector is empty, thus avoiding the heap overflow.



### ki...@gmail.com (2023-11-10)

I spent some time analyzing this vulnerability, please check it out. The core vulnerable code has been in existence since 2019, and there may be other paths that could trigger it. However, a recent introduction has made it more easily detectable by fuzzing.


### da...@chromium.org (2023-11-10)

Thanks for the review and the detailed investigation! I agree with the short term patch. To add on as to why this was more prevalent with my feature flag RenderTextEarlyEliding, its because we are marking render text as fully elided for text elements with 0 width which leads to EnsureLayout not adding additional codepoints to the text_display_indices container. I don't think this is reachable without the feature flag enabled. Will update with a patch. 

https://source.chromium.org/chromium/chromium/src/+/main:ui/gfx/render_text_harfbuzz.cc;drc=82c1f29effa1cd66820098a3a619cfaa359dc210;l=2495



### ki...@gmail.com (2023-11-14)

Hello, is there still active? Thanks!

### am...@chromium.org (2023-11-14)

[Description Changed]

### am...@chromium.org (2023-11-14)

[security shepherd] hi dayeung@ just wanted to check in to see if you've had a change to work on the CL for this. 
Since this seems to be specific to a feature that is not enabled, there's not SLO other than launch or OT or field experiments, however, it would be to get this off the board if possible. 
If you're not able to work on it right away, can you please update with a next-action date as a ballpark estimate on when you'll be able to work on this. 
This will also help you avoid some other security shepherd check-ins in the near term. Thank you!

### da...@chromium.org (2023-11-14)

Hey folks, I'm working on reverting the change now. Just waiting for owners to sign off. 

### am...@chromium.org (2023-11-16)

Awesome -- ty for working on this! 

### gi...@appspot.gserviceaccount.com (2023-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a528a468a97a6c5a45e9532ead6c8ef3002e0828

commit a528a468a97a6c5a45e9532ead6c8ef3002e0828
Author: David Yeung <dayeung@chromium.org>
Date: Thu Nov 16 19:25:13 2023

Revert "[gfx 2/5] Implement tail text eliding during layout phase"

This reverts commit 1b1ae9bbc354b08dd3a04148a61908f11427ba7c.

Reason for revert: Introduced a heap overflow with feature flag enabled.
Bug: 1500580

Original change's description:
> [gfx 2/5] Implement tail text eliding during layout phase
>
> This CL will be picking up the work of an existing prototype.
> https://crrev.com/c/2211075
>
> This CL is implementing the eliding during layout (instead of
> display text phase) for the ELIDE_TAIL eliding behavior.
>
> The eliding behavior is the same and is gated under a finch
> experiment but will become the default after validating
> on stable channels.
>
> 1/5
> https://crrev.com/c/4024384
>
> Bug: 1085014
> Change-Id: I90f44832d8c25cc8436459fdb22ebd2ed8e00c5d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4919916
> Reviewed-by: Etienne Bergeron <etienneb@chromium.org>
> Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
> Commit-Queue: David Yeung <dayeung@chromium.org>
> Reviewed-by: Elaine Chien <elainechien@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1219708}

Bug: 1085014
Change-Id: I4a78a3a90c249f7961f414ecf52e25dec01719e3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5028612
Reviewed-by: Elaine Chien <elainechien@chromium.org>
Reviewed-by: Etienne Bergeron <etienneb@chromium.org>
Commit-Queue: David Yeung <dayeung@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1225649}

[modify] https://crrev.com/a528a468a97a6c5a45e9532ead6c8ef3002e0828/ui/gfx/render_text.cc
[modify] https://crrev.com/a528a468a97a6c5a45e9532ead6c8ef3002e0828/ui/gfx/render_text.h
[modify] https://crrev.com/a528a468a97a6c5a45e9532ead6c8ef3002e0828/ui/gfx/render_text_harfbuzz.cc
[modify] https://crrev.com/a528a468a97a6c5a45e9532ead6c8ef3002e0828/ui/gfx/render_text_unittest.cc
[modify] https://crrev.com/a528a468a97a6c5a45e9532ead6c8ef3002e0828/ui/gfx/render_text_harfbuzz.h


### cl...@chromium.org (2023-11-17)

ClusterFuzz testcase 6349966679670784 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1225648:1225649

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-22)

Thank you for this report. Given that this issue seems to be trigged in the browser launch process, early in the startup process (StartupBrowserCreatorImpl), it is unclear how this issue could be reasonably exploited in a real-world scenario. As such, we -- the Chrome VRP Panel -- consider this issue to be significantly mitigated and have decided to extend a $1,000 reward. 

Thank you for your efforts in reporting this issue to us, and we were able to make a change to mitigate this possibility. 

In full transparency, since the your report was reported was not actionable at the time it was initially received (the asan evidence of this issue was submitted at 3:48am PST, but actionable reproduction information was submitted the next day at 12:00am PST -- in c#9) we have also extended a VRP reward for another high-quality report of this issue that was reported before your reproduction was provided. 

While we do have a policy regarding collisions and duplicate reports, in the future, reports that are not actionable and are lacking necessary information to proceed with triage may not be considered "first in" and may not be the report that is eligible for the VRP reward if other higher-quality actionable reports are received in the same time frame.

### am...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8389dbaec4d628f789dc477aa7d5f8105d147c66

commit 8389dbaec4d628f789dc477aa7d5f8105d147c66
Author: David Yeung <dayeung@chromium.org>
Date: Mon Dec 11 19:48:50 2023

[RenderText] Change DCHECK To CHECK in GetGraphemeIteratorAtIndex.

There is a potential heap overflow that happens in
RenderText::GetGraphemeIteratorAtIndex that is currently caught by DCHECKS.
Modifying this to use a CHECK instead of a DCHECK.

Bug: 1500580
Change-Id: Iae351dce72c6833c5648af06828d8df3d43287f6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5040904
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: David Yeung <dayeung@chromium.org>
Reviewed-by: Elaine Chien <elainechien@chromium.org>
Reviewed-by: Etienne Bergeron <etienneb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1235896}

[modify] https://crrev.com/8389dbaec4d628f789dc477aa7d5f8105d147c66/ui/gfx/render_text.cc


### is...@google.com (2023-12-11)

This issue was migrated from crbug.com/chromium/1500580?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1500601, crbug.com/chromium/1500649, crbug.com/chromium/1500829]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40940830)*
