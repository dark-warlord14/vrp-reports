# Security: UAF in LocationBar

| Field | Value |
|-------|-------|
| **Issue ID** | [40054261](https://issues.chromium.org/issues/40054261) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | UI>Browser, UI>Browser>Omnibox |
| **Platforms** | Linux |
| **Reporter** | le...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2020-12-22 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

On Linux, when clicking the location icon with the middle mouse button, the browser will read the clipboard content[1] to navigate to a new site. And |ReadText| will run a nested message loop[2] to continue running the ui thread. If the LocationBarView are destroyed, the UAF will be triggered when accessing its member function[3] after the nested message loops exit. (Asan throw it out as heap-buffer-overflow)

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/location_bar/location_bar_view.cc;l=1253;drc=2a6d591c857ca0633bf9a237f2d7c690a95e8fbb>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/selection_requestor.cc;l=249;drc=eafec8441d8c6343f3d23a05a72da5835f4c87e4>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/location_bar/location_bar_view.cc;l=1257;drc=2a6d591c857ca0633bf9a237f2d7c690a95e8fbb>

**VERSION**  

Chrome Version: stable  

Operating System: Linux

**REPRODUCTION CASE**

1. Copy a lot of content(I used about 300M) from a non-chrome window.
2. $ python -m SimpleHTTPServer  
   
   $ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"
3. Click the location icon in the location bar with the middle mouse button.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 163 B)
- [LocationBar.asan](attachments/LocationBar.asan) (application/octet-stream, 6.3 KB)
- [LocationBar.asan.txt](attachments/LocationBar.asan.txt) (text/plain, 6.3 KB)

## Timeline

### [Deleted User] (2020-12-22)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-22)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-22)

Some (very) occasional crashes: goto/crash/c227cc9738461d12

Setting severity=high as while this is in the browser it requires user interaction.

Setting ayaelattar@ as owner following recent-ish commit to function on stack, feel free to assign to someone else, or CC more appropriate people.

[Monorail components: UI>Browser>Omnibox]

### aj...@google.com (2020-12-23)

leecraso: please let me if this can be controlled from a web context.

+ ui>browser as there are so many related bugs

[Monorail components: UI>Browser]

### aj...@google.com (2020-12-23)

See https://bugs.chromium.org/p/chromium/issues/detail?id=1161146#c5 for an example of how an attacker could manipulate the clipboard to make this exploitable. The process is somewhat convoluted so while this is accessible from a web context it will be difficult to exploit, so setting severity=High.

### ay...@google.com (2020-12-23)

Reassigning to jdonnelly@ as he's one of Omnibox owners.

### jd...@google.com (2020-12-23)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-12-23)

[Comment Deleted]

### es...@chromium.org (2020-12-23)

based on my understanding of the report (thanks leecraso@ for the details!), this should do the trick: https://chromium-review.googlesource.com/c/chromium/src/+/2602581

### jd...@chromium.org (2020-12-24)

Sorry, ignore my https://crbug.com/chromium/1161143#c8. I confused this bug with https://crbug.com/chromium/1161149.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4449153f10669e64e3afb8c5e4ceb2269cf182c

commit d4449153f10669e64e3afb8c5e4ceb2269cf182c
Author: Evan Stade <estade@chromium.org>
Date: Thu Dec 24 00:21:41 2020

Fix issue in Location Bar on Linux.

Bug: 1161143
Change-Id: Ifa6a401f033ec2192233432ff13d593290027e40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602581
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/master@{#839212}

[modify] https://crrev.com/d4449153f10669e64e3afb8c5e4ceb2269cf182c/chrome/browser/ui/views/location_bar/location_bar_view.cc


### le...@gmail.com (2020-12-24)

It seems that this patch does not completely solve the problem. There will be other UAF paths[1][2] after return.

[1]. https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/location_bar/location_icon_view.cc;l=81;drc=c5419aefd3c11dbb65f9083d424ad3c881b1651c
[2]. https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/location_bar/icon_label_bubble_view.cc;l=303;drc=b82690a8abd546e81f00af4d95e2ad7c940a49d8

### [Deleted User] (2020-12-24)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2020-12-24)

jeepers, OK, tried to be a bit more thorough in my investigation this time: https://chromium-review.googlesource.com/c/chromium/src/+/2603120

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79cee575dec9505dd8f290ef8ccdb8fc07626d01

commit 79cee575dec9505dd8f290ef8ccdb8fc07626d01
Author: Evan Stade <estade@chromium.org>
Date: Tue Jan 05 20:21:29 2021

Second try at fixing location icon view issue on Linux.

Bug: 1161143
Change-Id: I52317cbd7b760218036a3cb99a9e53f6e5ed1e97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2603120
Commit-Queue: Evan Stade <estade@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Cr-Commit-Position: refs/heads/master@{#840268}

[modify] https://crrev.com/79cee575dec9505dd8f290ef8ccdb8fc07626d01/chrome/browser/ui/views/location_bar/location_icon_view.cc


### es...@chromium.org (2021-01-05)

I filed https://crbug.com/chromium/1163313 to take a look at a more comprehensive solution, given that the underlying issue could crop up in other bits of code. This particular instance of this bug should be fixed. I don't know how to trigger a security reward review.

### le...@gmail.com (2021-01-07)

Thanks for the quick fix, it seems to work. And I think if you mark the issue as fixed, Sheriffbot will arrange the security reward review.

### es...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M87. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-08)

This bug requires manual review: We are only 10 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2021-01-09)

Sheriffbot needs its prescription checked. The two chromium commits are:

crrev.com/d4449153f10669e64e3afb8c5e4ceb2269cf182c
crrev.com/79cee575dec9505dd8f290ef8ccdb8fc07626d01

I'm not on the security team so I can't comment on whether it's really serious enough to warrant a merge to 87. I'd say probably not since I believe it requires the user to manually select a large amount of text in another app, AND middle click a specific piece of UI, before it can cause a crash.

### le...@gmail.com (2021-01-11)

[Comment Deleted]

### sr...@google.com (2021-01-11)

+adetaylor@ for merge review. 



### ad...@chromium.org (2021-01-11)

That does seem almost enough user interaction to merit bumping this down to Medium severity, but I'll keep it as High to err on the side of caution. And the fix is very simple so: approving merge to M88, branch 4324.

### sr...@google.com (2021-01-11)

Please complete your merge before Tuesday Jan 12 2pm PST, if you are in a different time zone , stable RC will be cut tomorrow so we need your help to get these all completed to be included in the final build for M88

### sr...@google.com (2021-01-12)

Please complete the merge to M88 branch before 2pm PST today so they can be included in M88 stable RC build 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/11e74dc44ebf419ee4113e2064bfb88456c7d015

commit 11e74dc44ebf419ee4113e2064bfb88456c7d015
Author: Evan Stade <estade@chromium.org>
Date: Tue Jan 12 19:41:54 2021

Fix issue in Location Bar on Linux.

(cherry picked from commit d4449153f10669e64e3afb8c5e4ceb2269cf182c)

Bug: 1161143
Change-Id: Ifa6a401f033ec2192233432ff13d593290027e40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602581
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#839212}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2625528
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1680}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/11e74dc44ebf419ee4113e2064bfb88456c7d015/chrome/browser/ui/views/location_bar/location_bar_view.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb5d66bdaf06ab4e91d82999912185d8ba75732c

commit fb5d66bdaf06ab4e91d82999912185d8ba75732c
Author: Evan Stade <estade@chromium.org>
Date: Tue Jan 12 19:42:21 2021

Second try at fixing location icon view issue on Linux.

(cherry picked from commit 79cee575dec9505dd8f290ef8ccdb8fc07626d01)

Bug: 1161143
Change-Id: I52317cbd7b760218036a3cb99a9e53f6e5ed1e97
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2603120
Commit-Queue: Evan Stade <estade@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#840268}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2625529
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1681}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/fb5d66bdaf06ab4e91d82999912185d8ba75732c/chrome/browser/ui/views/location_bar/location_icon_view.cc


### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel had decided to award you $5000 for this report. Nice job and thank you!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f6658bc4fcfe269c53f8806e02492c658bedb09f

commit f6658bc4fcfe269c53f8806e02492c658bedb09f
Author: Tom Anderson <thomasanderson@chromium.org>
Date: Sat Jan 16 00:59:21 2021

Avoid spinning a nested message loop for X11 clipboard

BUG=443355,1138143,1161141,1161143,1161144,1161145,1161146,1161147,1161149,1161151,1161152

Change-Id: I5c95a9d066683d18f344d694e517274e3ef7ccb4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2622521
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/heads/master@{#844318}

[modify] https://crrev.com/f6658bc4fcfe269c53f8806e02492c658bedb09f/ui/base/x/selection_requestor_unittest.cc
[modify] https://crrev.com/f6658bc4fcfe269c53f8806e02492c658bedb09f/ui/base/x/selection_requestor.cc


### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e5f1ac5b63af60b02d23b007398d01a5dbc53b3

commit 5e5f1ac5b63af60b02d23b007398d01a5dbc53b3
Author: Evan Stade <estade@chromium.org>
Date: Wed Jan 20 21:05:47 2021

Revert "Second try at fixing location icon view issue on Linux."

This reverts commit fb5d66bdaf06ab4e91d82999912185d8ba75732c.

Reason for revert: no longer necessary after crrev.com/f6658bc4fcfe269c53f8806e02492c658bedb09f

Original change's description:
> Second try at fixing location icon view issue on Linux.
>
> (cherry picked from commit 79cee575dec9505dd8f290ef8ccdb8fc07626d01)
>
> Bug: 1161143
> Change-Id: I52317cbd7b760218036a3cb99a9e53f6e5ed1e97
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2603120
> Commit-Queue: Evan Stade <estade@chromium.org>
> Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
> Cr-Original-Commit-Position: refs/heads/master@{#840268}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2625529
> Reviewed-by: Evan Stade <estade@chromium.org>
> Cr-Commit-Position: refs/branch-heads/4324@{#1681}
> Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

TBR=estade@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1161143
Change-Id: I7d60bb3847cbfccd728fdcb9f7db286b4a7cb548
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2637958
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1864}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/5e5f1ac5b63af60b02d23b007398d01a5dbc53b3/chrome/browser/ui/views/location_bar/location_icon_view.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1205f0267c42d40c5f225b9813d86af39768cbd2

commit 1205f0267c42d40c5f225b9813d86af39768cbd2
Author: Evan Stade <estade@chromium.org>
Date: Thu Jan 21 04:13:45 2021

Reland "Second try at fixing location icon view issue on Linux."

This is a reland of fb5d66bdaf06ab4e91d82999912185d8ba75732c

This was accidentally reverted (it was intended to revert the original,
not the cherry pick).

Original change's description:
> Second try at fixing location icon view issue on Linux.
>
> (cherry picked from commit 79cee575dec9505dd8f290ef8ccdb8fc07626d01)
>
> Bug: 1161143
> Change-Id: I52317cbd7b760218036a3cb99a9e53f6e5ed1e97
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2603120
> Commit-Queue: Evan Stade <estade@chromium.org>
> Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
> Cr-Original-Commit-Position: refs/heads/master@{#840268}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2625529
> Reviewed-by: Evan Stade <estade@chromium.org>
> Cr-Commit-Position: refs/branch-heads/4324@{#1681}
> Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

Bug: 1161143
Change-Id: I1717a7acfbf38c51850b0657288bd89e2c086384
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2641302
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1875}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/1205f0267c42d40c5f225b9813d86af39768cbd2/chrome/browser/ui/views/location_bar/location_icon_view.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/84ea488b311380f83d7fd3fc4f9c45f10f0ba52b

commit 84ea488b311380f83d7fd3fc4f9c45f10f0ba52b
Author: Evan Stade <estade@chromium.org>
Date: Thu Jan 21 18:37:21 2021

Revert changes to location bar on Linux.

This reverts commits d4449153f10669e64e3afb8c5e4ceb2269cf182c and
79cee575dec9505dd8f290ef8ccdb8fc07626d01 which are no longer necessary
after f6658bc4fcfe269c53f8806e02492c658bedb09f

Bug: 1161143
Change-Id: I0893d147bb4a6384204198738df7a46cd855a932
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2640378
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/master@{#845719}

[modify] https://crrev.com/84ea488b311380f83d7fd3fc4f9c45f10f0ba52b/chrome/browser/ui/views/location_bar/location_icon_view.cc
[modify] https://crrev.com/84ea488b311380f83d7fd3fc4f9c45f10f0ba52b/chrome/browser/ui/views/location_bar/location_bar_view.cc


### ac...@chromium.org (2021-01-26)

The fix is in views, which I believe is also applicable to ChromeOS - is that right?

### ac...@chromium.org (2021-01-26)

Is the final fix https://chromium-review.googlesource.com/c/chromium/src/+/2622521? I believe that's not applicable to ChromeOS.

### es...@chromium.org (2021-01-26)

[Comment Deleted]

### es...@chromium.org (2021-01-26)

correct, only relevant to desktop linux.

### ac...@chromium.org (2021-01-26)

[Empty comment from Monorail migration]

### vs...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-28)

After discussion with thomasanderson@chromium.org, we consider that the root cause here is the same as https://crbug.com/chromium/1138143, so closing as a duplicate rather than Fixed.

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73721b793078b83953bb87945a11769c5f7ea394

commit 73721b793078b83953bb87945a11769c5f7ea394
Author: Tom Anderson <thomasanderson@chromium.org>
Date: Wed Feb 10 23:52:01 2021

[Merge to M89] Avoid spinning a nested message loop for X11 clipboard

> BUG=443355,1138143,1161141,1161143,1161144,1161145,1161146,1161147,1161149,1161151,1161152
>
> Change-Id: I5c95a9d066683d18f344d694e517274e3ef7ccb4
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2622521
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#844318}

BUG=1138143
TBR=sky

Change-Id: I9260ecc7a3b06b97e54d03e6dbced0c4736f92c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2686346
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#905}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/73721b793078b83953bb87945a11769c5f7ea394/ui/base/x/selection_requestor_unittest.cc
[modify] https://crrev.com/73721b793078b83953bb87945a11769c5f7ea394/ui/base/x/selection_requestor.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/202b40b9aee4971905c4bf7ec9be789ecc6b39ba

commit 202b40b9aee4971905c4bf7ec9be789ecc6b39ba
Author: Tom Anderson <thomasanderson@chromium.org>
Date: Wed Feb 10 23:53:26 2021

[Merge to M88] Avoid spinning a nested message loop for X11 clipboard

*** NOTE: THIS IS NOT A CLEAN MERGE ***

> BUG=443355,1138143,1161141,1161143,1161144,1161145,1161146,1161147,1161149,1161151,1161152
>
> Change-Id: I5c95a9d066683d18f344d694e517274e3ef7ccb4
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2622521
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#844318}

BUG=1138143
TBR=sky

Change-Id: I7269ac8af7c91988a7d5520b3faf88dac89a577e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2688137
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Thomas Anderson <thomasanderson@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#2166}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/202b40b9aee4971905c4bf7ec9be789ecc6b39ba/ui/base/x/selection_requestor_unittest.cc
[modify] https://crrev.com/202b40b9aee4971905c4bf7ec9be789ecc6b39ba/ui/base/x/selection_requestor.cc


### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1161143?no_tracker_redirect=1

[Multiple monorail components: UI>Browser, UI>Browser>Omnibox]
[Monorail mergedinto: crbug.com/chromium/1138143]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054261)*
