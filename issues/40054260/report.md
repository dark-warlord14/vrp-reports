# Security: UAF in ContextMenu

| Field | Value |
|-------|-------|
| **Issue ID** | [40054260](https://issues.chromium.org/issues/40054260) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Linux |
| **Reporter** | le...@gmail.com |
| **Assignee** | ad...@igalia.com |
| **Created** | 2020-12-22 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

When right-clicking an editable element, the menu will add the paste item[1]. At the same time, the browser will check whether the content can be pasted[2]. |IsPasteEnabled|[3] will run a nested message loop[4] to continue running the ui thread. If the web content or other related instances are destroyed, the UAF will be triggered after the nested message loops exit.

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/renderer_context_menu/render_view_context_menu.cc;l=1729;drc=591e975ca8f1338faeb56d983f9c9946ebc4014d>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/renderer_context_menu/render_view_context_menu.cc;l=2073;drc=591e975ca8f1338faeb56d983f9c9946ebc4014d>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/renderer_context_menu/render_view_context_menu.cc;l=2723;drc=591e975ca8f1338faeb56d983f9c9946ebc4014d>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/master:ui/base/x/selection_requestor.cc;l=249;drc=eafec8441d8c6343f3d23a05a72da5835f4c87e4>

And there is the same problem in |IsPasteAndMatchStyleEnabled|[5], I think it also should be deal with.

[5]. <https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/renderer_context_menu/render_view_context_menu.cc;l=2729;drc=591e975ca8f1338faeb56d983f9c9946ebc4014d>

**VERSION**  

Chrome Version: stable  

Operating System: Linux

**REPRODUCTION CASE**

1. Copy any content from a non-chrome window.
2. $ python -m SimpleHTTPServer  
   
   $ out/asan/chrome --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"
3. Right click the textarea field.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 169 B)
- [ContextMenu.asan](attachments/ContextMenu.asan) (application/octet-stream, 19.3 KB)

## Timeline

### [Deleted User] (2020-12-22)

[Empty comment from Monorail migration]

### aj...@google.com (2020-12-22)

Setting severity High as this requires user interaction but is reachable from web contents.

### [Deleted User] (2020-12-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-12-23)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser]

### [Deleted User] (2020-12-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-12-23)

See https://bugs.chromium.org/p/chromium/issues/detail?id=1161146#c5 for an example of how an attacker could manipulate the clipboard to make this exploitable. The process is somewhat convoluted so while this is accessible from a web context it will be difficult to exploit, so keeping severity=High.

### aj...@google.com (2020-12-28)

Cannot repro on Windows.

### av...@chromium.org (2020-12-29)

Given that the link to the nested message loop is in /base/x, calling this Linux-only.

Thomas, do you have advice here?

### th...@chromium.org (2020-12-29)

Over to adunaev for X11 copy/paste

### [Deleted User] (2021-01-05)

adunaev: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@igalia.com (2021-01-11)

[Empty comment from Monorail migration]

### ad...@igalia.com (2021-01-11)

My apologies for the delay, I was on holidays.  I am working on the fix.

For the record, this likely should be added to the list of UAF issues mentioned in the https://crbug.com/chromium/1138143 [1].  Ultimately it is related to https://crbug.com/chromium/443355.

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=1138143#c41

### ad...@igalia.com (2021-01-11)

This problem (sync menu APIs vs. async nature of the Linux clipboard) is directly mentioned in the https://crbug.com/chromium/443355, see https://crbug.com/chromium/1161141#c1. Unfortunately, that means that this issue cannot be fixed easily, and what is more, trying to fix it separately from the main thing wouldn't be right.

Given that we have a bunch of related and possibly similar issues, I am uncertain how to proceed here.  Perhaps we need to prioritize work on the head issue instead?

As a side node: Without questioning the danger of the UAF, what is the real exploitablilty of this?  To hit the UAF, the sequence of events needs to be fine tuned.  The POC suggests closing the window in the oncontextmenu handler, but chrome doesn't allow window.close() unless that window has been previously opened by the script…

### le...@gmail.com (2021-01-11)

Thanks for the reply, but is there anything wrong with right-clicking a webpage opened by the script to trigger the bug?

### ad...@igalia.com (2021-01-11)

Adding msisov@ and nickdiego@ as they are also into X11-related changes that we do there.

### ad...@igalia.com (2021-01-11)

leecraso@, just right clicking should do no harm, the trick is in closing the window exactly at right clicking.

### le...@gmail.com (2021-01-11)

Yea, I mean the attacker can trigger the bug by executing window.close() on the webpage opened by the script. :P

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


### th...@chromium.org (2021-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-16)

Requesting merge to stable M87 because latest trunk commit (844318) appears to be after stable branch point (812852).

Requesting merge to beta M88 because latest trunk commit (844318) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-16)

This bug requires manual review: We are only 2 days from stable.
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

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-21)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-26)

Adding M89 merge request as it landed after branch point.

### ad...@google.com (2021-01-27)

Merge requests for the CL are being handled on https://crbug.com/chromium/1138143.

### ad...@google.com (2021-01-28)

After discussion with thomasanderson@chromium.org, we consider that the root cause here is the same as https://crbug.com/chromium/1138143, so closing as a duplicate rather than Fixed.

### le...@gmail.com (2021-01-28)

adetaylor@, thomasanderson@:

Thanks for the fix and reply, but I do not think that these issues should be marked as duplicate. And there are three reasons:

1. The root cause of these security bugs is not the synchronous call to the clipboard, but the not checking after the call is completed in these issues. During my research, I found there are many codes that used the nested run loop, but most of them did check after the loop was exited. The patch is effective, but the root cause is that these modules did not do strictly check.

2. This is a bug pattern like "free during the promise resolution"(https://bugs.chromium.org/u/744552254/updates and so on). Bugs are in different paths and modules, with different contexts and checks. The similar calls that can be marked as duplicates I have merged in the issues(such as this issue, 1161146, 1161149).

3. This is kind of unfair to a security researcher. I submitted 8 high-severity bugs(Especially for this issue, it doesn't even need to copy a lot of content, just need to right-click the webpage) and did different crash backtrace analysis. But all of these were eventually merged into an issue submitted three months ago, and I don't even have permission to view it. And it also means I can't even get any cve number, I am deeply frustrated by that.

### [Deleted User] (2021-01-28)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-01-29)

leecraso@ thanks.

Because this is an unusual situation, we were in any case planning to discuss it at the next VRP panel.

### le...@gmail.com (2021-01-29)

Thanks for your attention on this matter.

### am...@google.com (2021-02-10)

Hi Leecraso and Guang Gong, the VRP Panel has decided to award you $20,000 for this series of UAF bugs resulting from the nested message loop. While the linked and earlier submitted issue into which these reports were merged was identified as the root cause, we wanted to thank you for displaying the exploitability of this issue as well show our appreciation for your analysis and engagement as a fix was determined. Thank you for your efforts! 

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


### le...@gmail.com (2021-02-11)

[Comment Deleted]

### le...@gmail.com (2021-02-11)

Thanks for the bounty. But according to crbug.com/1138143#c70 and crbug.com/1138143#c74, the root cause of these issues are different from crbug.com/1138143. Could these issues be marked as fixed and assign CVEs?

### am...@google.com (2021-02-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-12)

Hi Leecraso@, in follow-up conversations with thomasanderson@, the engineer on this, while the exploitation result is different for the two sets of bugs - one being a stack overflow and your batch being UAFs- the root cause was the same for all - the nested message loop. 
The identification of this vulnerability from spinning the nested message loop in the X11 clipboard was identified from the analysis of the earlier submitted issue, crbug.com/1138143. The resulting fix from this issue resolved all the issues, which is why they were merged together and will be batched with a single CVE assigned to 1138143. It's our policy to assign CVEs based on a per code fix, even if a single fix solves security bugs that can manifest in a variety of ways, like here with producing a stack overflow and a UAF. 

Thank you again for your efforts in all of this. Your analysis and attention to detail were much appreciated. 

### le...@gmail.com (2021-02-13)

Thanks for the explanation. But:

1. I noticed in the recent update that you seem to have assigned multiple CVEs to the same patch. (https://chromium.googlesource.com/chromium/src/+/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49)

2. As https://crbug.com/chromium/1161141#c29 said, I still think the nested message loop is not a security bug. And I think if there are not enough UAF issues, you may not immediately patch it to an asynchronous call. Because there are too many codes that correctly use the nested message loop.

These are just my opinions, thank you anyway.

### [Deleted User] (2021-04-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1161141?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1138143]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054260)*
