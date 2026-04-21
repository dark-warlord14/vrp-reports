# use after free content::FontAccessManagerImpl::DidChooseLocalFonts

| Field | Value |
|-------|-------|
| **Issue ID** | [40056362](https://issues.chromium.org/issues/40056362) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime, Blink>Storage>FontAccess |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | pw...@chromium.org |
| **Created** | 2021-06-28 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

Steps to reproduce the problem:
1.python -m SimpltHTTPServer 
2.open to the button and it will show a bubble, wait some seconds, and click cancel font button, then the browser crashes
3. it is not crash stability. but the root reason I think is that FontAccessManagerImpl::ChooseLocalFont use the callback of base::Unretained(this), and the bubble may use it after  
the FontAccessManagerImpl is destroyed.

What is the expected behavior?

What went wrong?
above all, I will try to attach a video.

And chrome://flags I enable three features.
- Experimental Web Platform features
- Font Access APIs
- Enable persistent access to the Font Access API
my chromium version is 93.0.4554.0.

Did this work before? N/A 

Chrome version: 91.0.4472.124  Channel: stable
OS Version: 10.0

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 34.0 KB)
- deleted (application/octet-stream, 0 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 5.5 MB)
- [mojo_test.html](attachments/mojo_test.html) (text/plain, 737 B)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 971 B)

## Timeline

### [Deleted User] (2021-06-28)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-06-28)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-06-28)

this is the correct poc,  and copy_mojo_js_bindings.py,
$python copy_mojo_js_bindings.py out\asan\gen
$out\asan\chrome.exe --enable-blink-features=MojoJS



### wx...@gmail.com (2021-06-28)

sorry my root analysis is wrong, please ignore it.

### wx...@gmail.com (2021-06-28)

the root reason is that  the function FontAccessManagerImpl::DidChooseLocalFonts is used by a callback.
```
void FontAccessManagerImpl::DidChooseLocalFonts(
    ChooseLocalFontsCallback callback,
    blink::mojom::FontEnumerationStatus status,
    std::vector<blink::mojom::FontMetadataPtr> fonts) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  // The chooser has fulfilled its purpose. It's safe to dispose of it.
  const BindingContext& context = receivers_.current_context();
  int erased = choosers_.erase(context.frame_id);
  DCHECK(erased == 1);

  std::move(callback).Run(std::move(status), std::move(fonts));
}
```
but the var of 'receivers_' could be reset before callback.

so the fix should add the function of  receivers_.set_disconnect_handler() to clear the receivers_.current_context();

well, just my opinion.

### cl...@chromium.org (2021-06-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6018445534363648.

### cl...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-06-29)

Maybe set a wrong v8's js to clusterfuzz? this sample is interesting.

### mp...@chromium.org (2021-06-29)

Ha, sorry, yes this is the wrong bug for that. Sorry.

### cl...@chromium.org (2021-06-29)

Detailed Report: https://clusterfuzz.com/testcase?key=6018445534363648

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  scheduled_exception() == ReadOnlyRoots(heap()).termination_exception() in isolat
  v8::internal::Isolate::CancelScheduledExceptionFromTryCatch
  v8::TryCatch::~TryCatch
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=74070:74071

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6018445534363648

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6018445534363648 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### mp...@chromium.org (2021-06-29)

Assigning to oyiptong@. Can you please answer these questions:

1. Is the FontAccess interface launched for all stable 91 users? I think yes, so I've added FoundIn-91.
2. Can you check the other uses of base::Unretained() in font_access_manager_impl.cc?
3. I'm not sure the cause of the bug yet, but is there possibly a wider problem, like with permissions::ChooserController or something else?

Thanks!

[Monorail components: Blink>Storage>FontAccess]

### mp...@chromium.org (2021-06-29)

And please ignore Clusterfuzz, I don't have permissions to edit clusterfuzz cases...

### cl...@chromium.org (2021-06-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>Runtime]

### [Deleted User] (2021-06-29)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-06-29)

pwnall@, can you help find an alternate owner for this?

### am...@google.com (2021-06-29)

Also CC'ing jsbell@ to help find an alternate owner given FontAccess discussion above.

### js...@chromium.org (2021-07-08)

"Is the FontAccess interface launched for all stable 91 users?" - it's not enabled by default. Users need to run Chrome with a flag set. There is no active origin trial for it either.

### js...@chromium.org (2021-07-08)

CC-ing mek@, ayui@, and reillyg@ to take a look, see if there's a quick fix. 

### me...@chromium.org (2021-07-08)

Ah yes, current_context() is documented as
  // NOTE: It is important to understand that this must only be called within
  // the stack frame of an actual interface method invocation or disconnect
  // notification scheduled by a receiver. It is a illegal to attempt to call
  // this any other time (e.g., from another async task you post from within a
  // message handler).

Although this is easily missed, and this is not the first time issues like this have crept in...

### js...@chromium.org (2021-07-08)

Also, to expand on https://crbug.com/chromium/1224238#c19, there are no changes in feature exposure between 91 and 92; feature is still only behind a flag, no active OT.


### gi...@appspot.gserviceaccount.com (2021-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/68366d3638d4c1a71b31afd3f1276125b6c652cc

commit 68366d3638d4c1a71b31afd3f1276125b6c652cc
Author: Ayu Ishii <ayui@chromium.org>
Date: Fri Jul 09 04:18:28 2021

FontAccess: Don't expose mojo interface unless the feature is enabled.

The renderer side only tries to connect to this mojo interface gated
behind the same feature flag already, so this shouldn't cause any issues
and will make sure that any potential security issues in the FontAccess
browser side code aren't exposed yet.

Bug: 1224238
Change-Id: Ia10b9c92178c0d2369f5cb2c872aeebe2ceffa50
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3016404
Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#899855}

[modify] https://crrev.com/68366d3638d4c1a71b31afd3f1276125b6c652cc/content/browser/browser_interface_binders.cc
[modify] https://crrev.com/68366d3638d4c1a71b31afd3f1276125b6c652cc/content/browser/font_access/font_access_manager_impl_browsertest.cc


### me...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-09)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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

### ad...@google.com (2021-07-09)

Note to self: from https://crbug.com/chromium/1224238#c22 etc., this seems like it should be Security_Impact-None, but that's not in fact the case because the Mojo interface is accessible from a compromised renderer. Hence we do need to merge this to M92. The thing we're merging so far is just to shut down the browser-side Mojo interface if the feature is disabled; it's not an actual fix for the UaF.

Approving merge of https://crbug.com/chromium/1224238#c23 to M92, branch 4515.

### sr...@google.com (2021-07-12)

please complete the merge asap to M92 as we are cutting the stable RC tomorrow and would like to get this change into the fhinal build. 

### cl...@chromium.org (2021-07-12)

ClusterFuzz testcase 6018445534363648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=75681:75682

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### gi...@appspot.gserviceaccount.com (2021-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d457b379f98321b19e8cb0adf56f28f92c4b871d

commit d457b379f98321b19e8cb0adf56f28f92c4b871d
Author: Ayu Ishii <ayui@chromium.org>
Date: Mon Jul 12 18:44:20 2021

[M92] FontAccess: Don't expose mojo interface unless the feature is enabled.

The renderer side only tries to connect to this mojo interface gated
behind the same feature flag already, so this shouldn't cause any issues
and will make sure that any potential security issues in the FontAccess
browser side code aren't exposed yet.

(cherry picked from commit 68366d3638d4c1a71b31afd3f1276125b6c652cc)

Bug: 1224238
Change-Id: Ia10b9c92178c0d2369f5cb2c872aeebe2ceffa50
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3016404
Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#899855}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3016540
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Owners-Override: Prudhvi Kumar Bommana <pbommana@google.com>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1492}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/d457b379f98321b19e8cb0adf56f28f92c4b871d/content/browser/browser_interface_binders.cc
[modify] https://crrev.com/d457b379f98321b19e8cb0adf56f28f92c4b871d/content/browser/font_access/font_access_manager_impl_browsertest.cc


### me...@chromium.org (2021-07-12)

I filed https://crbug.com/chromium/1228510 to track fixing the underlying issue here.

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-21)

Re-opening since Clusterfuzz is still wrong here.

(As an aside: please don't mark this bug as fixed until the actual UaF is fixed -- these CLs look like great mitigations, but don't fix the underlying issue.)

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f40c93faff84b8cafe33bbe7bfe1d169f045ae0

commit 7f40c93faff84b8cafe33bbe7bfe1d169f045ae0
Author: Victor Costan <pwnall@chromium.org>
Date: Tue Jul 27 01:15:57 2021

Font Access: Remove invalid ReceiverSet::current_context() call.

Bug: 1228510, 1224238
Change-Id: I74b2860efbdddc4a64b86085ef41a58f5b3ee683
Tested: DCHECK-enabled browser and https://local-font-access.glitch.me/demo/
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3052711
Commit-Queue: Joshua Bell <jsbell@chromium.org>
Auto-Submit: Victor Costan <pwnall@chromium.org>
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#905532}

[modify] https://crrev.com/7f40c93faff84b8cafe33bbe7bfe1d169f045ae0/content/browser/font_access/font_access_manager_impl.cc
[modify] https://crrev.com/7f40c93faff84b8cafe33bbe7bfe1d169f045ae0/content/browser/font_access/font_access_manager_impl.h


### pw...@chromium.org (2021-07-27)

ReceiverSet::current_context() is now only used in appropriate contexts.

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Excellent work! 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1224238?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Runtime, Blink>Storage>FontAccess]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056362)*
