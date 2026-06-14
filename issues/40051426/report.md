# Use after free in CodeSerializer::Deserialize

| Field | Value |
|-------|-------|
| **Issue ID** | [40051426](https://issues.chromium.org/issues/40051426) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gk...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2020-02-04 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
In `CodeSerializer::Deserialize`, `info` is not protected by Handle. And it is used after `SharedFunctionInfo::EnsureSourcePositionsAvailable` triggers a GC, which moves `info` .

MaybeHandle<SharedFunctionInfo> CodeSerializer::Deserialize(
    Isolate* isolate, ScriptData* cached_data, Handle<String> source,
    ScriptOriginOptions origin_options) {
  ...
  for (SharedFunctionInfo info = iter.Next(); !info.is_null(); <-- define a raw pointer, `info`
           info = iter.Next()) {
        if (info.is_compiled()) {
          Handle<SharedFunctionInfo> shared_info(info, isolate);
          if (needs_source_positions) {
            SharedFunctionInfo::EnsureSourcePositionsAvailable(isolate,
                                                               shared_info); <-- this may call a GC
          }
          DisallowHeapAllocation no_gc;
          int line_num =
              script->GetLineNumber(shared_info->StartPosition()) + 1;
          int column_num =
              script->GetColumnNumber(shared_info->StartPosition()) + 1;
          PROFILE(isolate,
                  CodeCreateEvent(CodeEventListener::SCRIPT_TAG,
                                  handle(info.abstract_code(), isolate), <-- `info` is used.
                                  shared_info, name, line_num, column_num));
        }
      }
  ...
}

Patch: Use `shared_info` which is protected by Handle, instead of `info`.

MaybeHandle<SharedFunctionInfo> CodeSerializer::Deserialize(
    Isolate* isolate, ScriptData* cached_data, Handle<String> source,
    ScriptOriginOptions origin_options) {
  ...
  for (SharedFunctionInfo info = iter.Next(); !info.is_null();
           info = iter.Next()) {
        if (info.is_compiled()) {
          Handle<SharedFunctionInfo> shared_info(info, isolate);
          if (needs_source_positions) {
            SharedFunctionInfo::EnsureSourcePositionsAvailable(isolate,
                                                               shared_info);
          }
          DisallowHeapAllocation no_gc;
          int line_num =
              script->GetLineNumber(shared_info->StartPosition()) + 1;
          int column_num =
              script->GetColumnNumber(shared_info->StartPosition()) + 1;
          PROFILE(isolate,
                  CodeCreateEvent(CodeEventListener::SCRIPT_TAG,
                                  handle(shared_info->abstract_code(), isolate), <-- Use `shared_info` instead of `info`.
                                  shared_info, name, line_num, column_num));
        }
      }
  ...
}

Did this work before? N/A 

Chrome version: 79.0.3945.130  Channel: stable
OS Version: OS X 10.15.2
Flash Version:

## Timeline

### ca...@chromium.org (2020-02-04)

Thanks for reporting, do you have a POC that triggers the UaF? Thanks.

[Monorail components: Blink>JavaScript]

### gk...@gmail.com (2020-02-05)

I'm sorry that I don't have POC. But I think we should use `shared_info` instead of `info` to prevent the UaF bug.

### is...@chromium.org (2020-02-05)

I'm not sure about actual security implications given that it can be triggered only when the profiling is enabled but it's definitely a raw pointer misuse.
Dan, PTAL.

### is...@chromium.org (2020-02-05)

GCMole reported this issue here: https://crbug.com/v8/9992.

### is...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### gk...@gmail.com (2020-02-05)

[Comment Deleted]

### gk...@gmail.com (2020-02-05)

@ishell 
The report in https://crbug.com/v8/9992 ("https://bugs.chromium.org/p/v8/issues/attachmentText?aid=422017") seems to be different from this issue.
GCMole reported about `CreateInterpreterDataForDeserializedCode`, but this issue is about `CodeSerializer::Deserialize`.
Do you mean that this issue is related with https://crbug.com/v8/9992?

### is...@chromium.org (2020-02-05)

True, thanks!

Maya, FYI. Maybe we can tweak GCMole a bit.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f57e7da439b26cfb16a79d34f9f56e76e5287aa5

commit f57e7da439b26cfb16a79d34f9f56e76e5287aa5
Author: Dan Elphick <delphick@chromium.org>
Date: Wed Feb 05 11:15:58 2020

[snapshot] Fix deref of raw pointer after potential GC

Fixes the one case after calling EnsureSourcePositionsCollected that we
were still using the non-handle version of the SharedFunctionInfo.

Bug: chromium:1048555
Change-Id: Iefd35fab13623a1f05212c98864be62c37463942
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2037437
Commit-Queue: Dan Elphick <delphick@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Dan Elphick <delphick@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66130}

[modify] https://crrev.com/f57e7da439b26cfb16a79d34f9f56e76e5287aa5/src/snapshot/code-serializer.cc


### ms...@chromium.org (2020-02-05)

@ishell: Thanks for pointing out, GCMole should normally have caught all these similar issues in this file. Did any of you check if there are more left?

### gk...@gmail.com (2020-02-05)

In this week, I already reported 8 similar issues which my tool found. You can find them by searching my account with "use after free" keyword.

### ms...@chromium.org (2020-02-05)

Thanks for reporting those. I guess I don't have access to the ones I'm not CC'ed on.
@Dan, should we mark this bug as fixed?

### ca...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-02-05)

Assigining severity high, can someone on the V8 side confirm that's the case? Thanks

### gk...@gmail.com (2020-02-06)

And I have some points which are not buggy for now, but may be buggy in the future if we use them incorrectly.
We can enforce their safe usage by changing a few lines. Where should I report them?

### ms...@chromium.org (2020-02-06)

gksgudtjr456@ if they're not related to this class, please write them down in a separate issue. Thanks!

### de...@chromium.org (2020-02-06)

Re: #14, this bug allows a pointer to memory that has moved to be read. This could then result in a crash or further memory corruption in the renderer process.

That said, it requires the user to have started the profiler, which is not a common action, so I think it falls under these two Medium Memory severity bullet points:
* An out-of-bounds read in a renderer process
* Memory corruption in a renderer process that requires specific user interaction, such as dragging an object


### de...@chromium.org (2020-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-14)

Your change meets the bar and is auto-approved for M81. Please go ahead and merge the CL to branch 4044 (refs/branch-heads/4044) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3c466721964d924500046c04ec067e5da8c3615e

commit 3c466721964d924500046c04ec067e5da8c3615e
Author: Dan Elphick <delphick@chromium.org>
Date: Mon Feb 17 15:50:30 2020

Merged: [snapshot] Fix deref of raw pointer after potential GC

Revision: f57e7da439b26cfb16a79d34f9f56e76e5287aa5

BUG=chromium:1048555
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=mythria@chromium.org

Change-Id: Ib1ba3ae35a1fd696ab82495521f9a7d83fddca91
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2060498
Reviewed-by: Mythri Alle <mythria@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.1@{#19}
Cr-Branched-From: a4dcd39d521d14c4b1cac020812e44ee04a7f244-refs/heads/8.1.307@{#1}
Cr-Branched-From: f22c213304ec3542df87019aed0909b7dafeaa93-refs/heads/master@{#66031}

[modify] https://crrev.com/3c466721964d924500046c04ec067e5da8c3615e/src/snapshot/code-serializer.cc


### pb...@google.com (2020-02-17)

The Cl from https://crbug.com/chromium/1048555#c24 is already part of M81 branch,  	delphick@ if all required CL's are in M81 can we please make the bug as fixed.

### de...@chromium.org (2020-02-18)

It is marked as fixed. 

### na...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@chromium.org (2020-02-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-20)

Nice work! The Panel decided to award $500 for this report 

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f57e7da439b26cfb16a79d34f9f56e76e5287aa5

commit f57e7da439b26cfb16a79d34f9f56e76e5287aa5
Author: Dan Elphick <delphick@chromium.org>
Date: Wed Feb 05 11:15:58 2020

[snapshot] Fix deref of raw pointer after potential GC

Fixes the one case after calling EnsureSourcePositionsCollected that we
were still using the non-handle version of the SharedFunctionInfo.

Bug: chromium:1048555
Change-Id: Iefd35fab13623a1f05212c98864be62c37463942
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2037437
Commit-Queue: Dan Elphick <delphick@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Dan Elphick <delphick@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66130}

[modify] https://crrev.com/f57e7da439b26cfb16a79d34f9f56e76e5287aa5/src/snapshot/code-serializer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f57e7da439b26cfb16a79d34f9f56e76e5287aa5

commit f57e7da439b26cfb16a79d34f9f56e76e5287aa5
Author: Dan Elphick <delphick@chromium.org>
Date: Wed Feb 05 11:15:58 2020

[snapshot] Fix deref of raw pointer after potential GC

Fixes the one case after calling EnsureSourcePositionsCollected that we
were still using the non-handle version of the SharedFunctionInfo.

Bug: chromium:1048555
Change-Id: Iefd35fab13623a1f05212c98864be62c37463942
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2037437
Commit-Queue: Dan Elphick <delphick@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Dan Elphick <delphick@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66130}

[modify] https://crrev.com/f57e7da439b26cfb16a79d34f9f56e76e5287aa5/src/snapshot/code-serializer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f57e7da439b26cfb16a79d34f9f56e76e5287aa5

commit f57e7da439b26cfb16a79d34f9f56e76e5287aa5
Author: Dan Elphick <delphick@chromium.org>
Date: Wed Feb 05 11:15:58 2020

[snapshot] Fix deref of raw pointer after potential GC

Fixes the one case after calling EnsureSourcePositionsCollected that we
were still using the non-handle version of the SharedFunctionInfo.

Bug: chromium:1048555
Change-Id: Iefd35fab13623a1f05212c98864be62c37463942
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2037437
Commit-Queue: Dan Elphick <delphick@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Dan Elphick <delphick@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66130}

[modify] https://crrev.com/f57e7da439b26cfb16a79d34f9f56e76e5287aa5/src/snapshot/code-serializer.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f57e7da439b26cfb16a79d34f9f56e76e5287aa5

commit f57e7da439b26cfb16a79d34f9f56e76e5287aa5
Author: Dan Elphick <delphick@chromium.org>
Date: Wed Feb 05 11:15:58 2020

[snapshot] Fix deref of raw pointer after potential GC

Fixes the one case after calling EnsureSourcePositionsCollected that we
were still using the non-handle version of the SharedFunctionInfo.

Bug: chromium:1048555
Change-Id: Iefd35fab13623a1f05212c98864be62c37463942
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2037437
Commit-Queue: Dan Elphick <delphick@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Dan Elphick <delphick@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66130}

[modify] https://crrev.com/f57e7da439b26cfb16a79d34f9f56e76e5287aa5/src/snapshot/code-serializer.cc


### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1048555?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/v8/9992]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051426)*
