# Security: RWHI UaF from bad fullscreen widget routing id

| Field | Value |
|-------|-------|
| **Issue ID** | [40083766](https://issues.chromium.org/issues/40083766) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Navigation |
| **Reporter** | gz...@gmail.com |
| **Assignee** | na...@chromium.org |
| **Created** | 2016-02-26 |
| **Bounty** | $10,500.00 |

## Description

When a fullscreen widget is created, a WebContentsImpl stores its routing id in fullscreen\_widget\_routing\_id\_. WCI assumes that this widget belongs to the process of the current main frame: GetRenderManager()->current\_host()->GetProcess(), which it normally does. A compromised renderer can swap the process of the main frame, while keeping the fullscreen widget alive. Normally, the fullscreen widget would be deleted as the renderer navigates, but there is an exception. If the navigation was within the page, then the fullscreen is kept alive. This happens for example when only the url fragment changes. In such case, renderer sets FrameHostMsg\_DidCommitProvisionalLoad\_Params::was\_within\_same\_page = true and the browser mostly trusts that, even if the the navigation wasn't within page and the process was swapped. If the renderer swaps the process and sets was\_within\_same\_page = true, the fullscreen\_widget\_routing\_id\_ will end up pointing to a wrong widget in the new process. If the renderer now closes fullscreen, this wrong widget is deleted. It is deleted manually in RenderWidgetHostImpl::Destroy(), because fullscreen widgets aren't owned by a smart pointer. Normal widgets are owned by a scoped\_ptr render\_widget\_host\_ in RenderViewHostImpl though. If such a widget is manually deleted by an attacker, the scoped\_ptr in RVHI ends up holding a dangling pointer, that can UaF.

**VERSION**  

Chrome Version: 48 stable and up  

Operating System: all

**REPRODUCTION CASE**

- Apply poc.patch and build (I've tested with a release build)
- Navigate to <http://www.example.com>

It should display something like:  

::OnDidCommitProvisionalLoad rphid=14 <http://www.example.com/>  

::OnDidCommitProvisionalLoad rphid=15 <http://www.example.net/>  

::OnDidCommitProvisionalLoad rphid=14 <http://www.example.com/>  

::OnDidCommitProvisionalLoad rphid=15 <http://www.example.com/>  

Trigger free  

Delete rwh=000026c38f3a71c0 with owner\_delegate\_  

Trigger use  

Use rwh=000026c38f3a71c0  

Segmentation fault

## Attachments

- [poc.patch](attachments/poc.patch) (application/octet-stream, 6.0 KB)
- [crash.txt](attachments/crash.txt) (text/plain, 6.5 KB)
- [poc.patch](attachments/poc.patch) (application/octet-stream, 9.5 KB)
- [crash.txt](attachments/crash.txt) (text/plain, 5.5 KB)
- [kanye.jpg](attachments/kanye.jpg) (image/jpeg, 81.4 KB)

## Timeline

### gz...@gmail.com (2016-02-26)

WIP CL: https://codereview.chromium.org/1738233002/

Please cc the reviewer clamy@chromium.org

### oc...@chromium.org (2016-02-26)

Thanks for another report, and fix!

[Monorail components: UI>Browser>FullScreen]

### cr...@chromium.org (2016-02-26)

Thanks for filing this!  I'm sending some comments on the CL, but I'll be OOO soon so I'll assign to Nasko to help triage in the meantime.  (I think he'll have a chance to look before clamy@.)

[Monorail components: UI>Browser>Navigation]

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8be1ff11dc1fae61146dbcfaa38e12314d290dca

commit 8be1ff11dc1fae61146dbcfaa38e12314d290dca
Author: gzobqq <gzobqq@gmail.com>
Date: Tue Mar 01 17:12:01 2016

Disallow was_within_same_page = true for a cross-process navigation.

BUG=590284
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1738233002

Cr-Commit-Position: refs/heads/master@{#378461}

[modify] https://crrev.com/8be1ff11dc1fae61146dbcfaa38e12314d290dca/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/8be1ff11dc1fae61146dbcfaa38e12314d290dca/content/browser/frame_host/navigator_impl_unittest.cc
[modify] https://crrev.com/8be1ff11dc1fae61146dbcfaa38e12314d290dca/content/test/test_render_frame_host.cc


### bu...@chromium.org (2016-03-02)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/8be1ff11dc1fae61146dbcfaa38e12314d290dca

commit 8be1ff11dc1fae61146dbcfaa38e12314d290dca
Author: gzobqq <gzobqq@gmail.com>
Date: Tue Mar 01 17:12:01 2016


### bu...@chromium.org (2016-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e5787005a9004d7be289cc649c6ae4f3051996cd

commit e5787005a9004d7be289cc649c6ae4f3051996cd
Author: gzobqq <gzobqq@gmail.com>
Date: Wed Mar 02 21:50:18 2016

Check that RWHI isn't deleted manually while owned by a scoped_ptr in RVHI

BUG=590284

Review URL: https://codereview.chromium.org/1747183002

Cr-Commit-Position: refs/heads/master@{#378844}

[modify] https://crrev.com/e5787005a9004d7be289cc649c6ae4f3051996cd/content/browser/renderer_host/render_widget_host_impl.cc


### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-03-07)

I think this is fixed now, correct?

### gz...@gmail.com (2016-03-07)

Yes, it should be good. The bug impacts M49, if I understand it correctly we also need to merge.

### ti...@google.com (2016-03-08)

Let's start with a merge to M-50.

### ti...@google.com (2016-03-08)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### bu...@chromium.org (2016-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1382808d47649a612f0c14346ccf5cc2e297dc48

commit 1382808d47649a612f0c14346ccf5cc2e297dc48
Author: Nasko Oskov <nasko@chromium.org>
Date: Wed Mar 09 22:55:51 2016

Disallow was_within_same_page = true for a cross-process navigation.

BUG=590284
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1738233002

Cr-Commit-Position: refs/heads/master@{#378461}
(cherry picked from commit 8be1ff11dc1fae61146dbcfaa38e12314d290dca)

Review URL: https://codereview.chromium.org/1784673002 .

Cr-Commit-Position: refs/branch-heads/2661@{#158}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/1382808d47649a612f0c14346ccf5cc2e297dc48/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/1382808d47649a612f0c14346ccf5cc2e297dc48/content/browser/frame_host/navigator_impl_unittest.cc
[modify] https://crrev.com/1382808d47649a612f0c14346ccf5cc2e297dc48/content/test/test_render_frame_host.cc


### na...@chromium.org (2016-03-09)

Merged: https://codereview.chromium.org/1784673002/

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### na...@chromium.org (2016-03-11)

Do we want this merged in M-49? It is currently merged in M-50 only.

### ti...@google.com (2016-03-11)

[Automated comment] Request affecting a post-stable build (M49), manual review required.

### ss...@google.com (2016-03-14)

Marking as OS-all, please change if this is incorrect

### go...@chromium.org (2016-03-15)

Per https://crbug.com/chromium/590284#c3, this is already merged to M50 branch 2661. If all is done for M50, please remove "Merge-Approved-50" label and apply "merge-merged-2661" label. Thank you.

### na...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-15)

As per c#11, timwillis@ wanted to start with a merge to M50. I will let him decide if he wants this now in M49 as well.

### ti...@google.com (2016-03-15)

#21: Yes, I vote for merging this to M49 so it ships with any new stable release.

### ss...@google.com (2016-03-16)

Merge approved for M49 (branch 2623)

### go...@chromium.org (2016-03-16)

Please merge your change to M49 branch so we can take it for next M49 stable release whenever it happens. Thank you.

### bu...@chromium.org (2016-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ce8285498bf60a2abae05d6ae58409b932a3579f

commit ce8285498bf60a2abae05d6ae58409b932a3579f
Author: Nasko Oskov <nasko@chromium.org>
Date: Wed Mar 16 23:49:39 2016

Disallow was_within_same_page = true for a cross-process navigation.

BUG=590284
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1738233002

Cr-Commit-Position: refs/heads/master@{#378461}
(cherry picked from commit 8be1ff11dc1fae61146dbcfaa38e12314d290dca)

Review URL: https://codereview.chromium.org/1811783002 .

Cr-Commit-Position: refs/branch-heads/2623@{#629}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] https://crrev.com/ce8285498bf60a2abae05d6ae58409b932a3579f/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/ce8285498bf60a2abae05d6ae58409b932a3579f/content/browser/frame_host/navigator_impl_unittest.cc
[modify] https://crrev.com/ce8285498bf60a2abae05d6ae58409b932a3579f/content/test/test_render_frame_host.cc


### ti...@google.com (2016-03-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-24)

Congrats - $5500 heading your way ($5000 for the report + $500 for the patch).

### ti...@google.com (2016-03-24)

Also, as discussed with the reporter, if they can show good control of EIP, we'll take this back through the panel and consider a higher reward.

### gz...@gmail.com (2016-03-24)

Thanks! This demonstrates vtable pointer control. Apply onto 50.0.2658 git 882a2c3c2f2340 in linux and navigate to http://www.example.com.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### gz...@gmail.com (2016-05-13)

Sorry to bother you guys. Was this ever considered for another round through the panel? #29 shows vtable pointer control. It should be pretty clear at demonstrating that "exploitation of this vulnerability is very likely (e.g. good control of EIP or another CPU register)". With good control of free and use timing and low noise from a large 448 tcmalloc slot, it's one of the nicest UaFs I've had.

### ti...@google.com (2016-05-13)

#31: It hasn't gone back through the panel, as I don't currently have a way of tagging issues for re-review (and the comment at #30 is automated so I didn't see #29). Thanks for the ping and sorry for the delay.

We'll put it on the next panel for re-review.

### gz...@gmail.com (2016-05-13)

:D I've been laughing at this with a silly grin for half an hour.

Yes, maybe not of all time, but from me, probably. If you guys disagree, that's fine of course. Let me know what I can do better in the future.

### sh...@chromium.org (2016-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-24)

As discussed, we took this back to the panel that decided to award an additional $5,000 for this report, bringing the total to $10,500. Congratulations! We'll start payment shortly.

Note to future me: Marking as reward-10500, but only paying the additional $5,000 here.

### gz...@gmail.com (2016-06-25)

Thank you for taking another look and thank you for the increased reward!

### aw...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### no...@google.com (2020-12-12)

[Empty comment from Monorail migration]

### is...@google.com (2020-12-12)

This issue was migrated from crbug.com/chromium/590284?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083766)*
