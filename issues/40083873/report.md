# Security: Navigating to "chrome://" URLs and "file://" URLs via window.open()

| Field | Value |
|-------|-------|
| **Issue ID** | [40083873](https://issues.chromium.org/issues/40083873) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-03-16 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 51.0.2680.0 canary  

Operating System: Windows 7

**REPRODUCTION CASE**  

I expect that clicking the link will navigate to "about:blank" (which is what happens in 49.0.2623.87 beta-m), since should not be allowed to navigate to "file://" URLs and "chrome://".

- Please watch the video is attached "actual.mp4".

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 440 B)
- [actual.mp4](attachments/actual.mp4) (application/octet-stream, 363.5 KB)

## Timeline

### me...@chromium.org (2016-03-16)

Bisect points to this range: https://chromium.googlesource.com/chromium/src/+log/8a3777d77af8e154f4eb03bfa87a8c73b58fa880..6dc5f17704d3b1465ab48f25a11b7c9979892df3

Alex,  https://chromium.googlesource.com/chromium/src/+/9ab970c98034692afa06d7f4bb1ff813d2ffd3f2 is the only navigation related change in the range. Can you please take a look? Thanks.

[Monorail components: UI>Browser>Navigation]

### me...@chromium.org (2016-03-16)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-03-16)

[Empty comment from Monorail migration]

### al...@chromium.org (2016-03-16)

I've confirmed that this is indeed due to my r377832.  I'll investigate what's happening exactly.

I believe this only affects cross-process popups.  I'm pretty sure the original test case only works because it uses www.google.com for the popup, which is put in a separate process because Google is the default search provider.  This didn't repro for me if the popup's initial URL is changed to any other site.

### al...@chromium.org (2016-03-16)

OK, found the problem.  Before my patch, proxy navigations went through RenderFrameHostImpl::OpenURL, which validated the destination URL with FilterURL() before passing the request on to NavigatorImpl.  When we switched them to the transfer path, we lost the FilterURL coverage (NavigatorImpl::RequestTransferURL does some URL validation with ShouldAllowOpenURL, but that apparently doesn't cover what FilterURL covers).  The actual blocking for these cases happens in ChildProcessSecurityPolicyImpl::CanCommitURL, called as part of FilterURL.

The solution should be simple -- add FilterURL validation in RenderFrameProxyHost::OnOpenURL.  Charlie, does that sound right to you?

### cr...@chromium.org (2016-03-16)

Yes, that sounds exactly right.  Thanks for looking into it!

### al...@chromium.org (2016-03-17)

Fix up for review at https://codereview.chromium.org/1812723002/

### ch...@gmail.com (2016-03-17)

Is this bug higher than low severity?


### me...@chromium.org (2016-03-17)

Alex: Thanks for the quick fix!

chromium.khalil: Simply opening a chrome:// or file:// url shouldn't be dangerous by itself (none of the items in medium severity list at https://www.chromium.org/developers/severity-guidelines apply), but if you could demonstrate that this bug could be chained with another bug or lead to privilege escalation we are happy to reevaluate its severity.

For example, can the opener read the contents of the file:// URL? That would definitely raise the severity to medium.

### ch...@gmail.com (2016-03-17)

Mustafa, Hmm I understood now. Thanks a lot! 

### bu...@chromium.org (2016-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5b50b674d36956c84a499b4f93e65a874de28713

commit 5b50b674d36956c84a499b4f93e65a874de28713
Author: alexmos <alexmos@chromium.org>
Date: Thu Mar 17 20:38:05 2016

Add URL validation to navigations initiated via RenderFrameProxyHosts.

When we changed RenderFrameProxyHost::OnOpenURL to use the transfer
logic in r377832, we lost FilterURL validation provided by
RenderFrameHostImpl::OpenURL.  This CL adds that validation to
navigations initiated via proxies.

BUG=595339
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1812723002

Cr-Commit-Position: refs/heads/master@{#381788}

[modify] https://crrev.com/5b50b674d36956c84a499b4f93e65a874de28713/content/browser/frame_host/render_frame_proxy_host.cc
[modify] https://crrev.com/5b50b674d36956c84a499b4f93e65a874de28713/content/browser/site_per_process_browsertest.cc


### al...@chromium.org (2016-03-17)

This should be fixed now.  chromium.khalil: thanks for the report!

### cl...@chromium.org (2016-03-18)

[Empty comment from Monorail migration]

### al...@chromium.org (2016-03-22)

Should this be merged to beta?

### ti...@google.com (2016-03-22)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### bu...@chromium.org (2016-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/52505b8cec39e5dcbf8e04f6dbe7ea1b92890e49

commit 52505b8cec39e5dcbf8e04f6dbe7ea1b92890e49
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Tue Mar 22 23:48:24 2016

Add URL validation to navigations initiated via RenderFrameProxyHosts.

When we changed RenderFrameProxyHost::OnOpenURL to use the transfer
logic in r377832, we lost FilterURL validation provided by
RenderFrameHostImpl::OpenURL.  This CL adds that validation to
navigations initiated via proxies.

BUG=595339
TBR=creis@chromium.org
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1812723002

Cr-Commit-Position: refs/heads/master@{#381788}
(cherry picked from commit 5b50b674d36956c84a499b4f93e65a874de28713)

Review URL: https://codereview.chromium.org/1821043005 .

Cr-Commit-Position: refs/branch-heads/2661@{#350}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/52505b8cec39e5dcbf8e04f6dbe7ea1b92890e49/content/browser/frame_host/render_frame_proxy_host.cc
[modify] https://crrev.com/52505b8cec39e5dcbf8e04f6dbe7ea1b92890e49/content/browser/site_per_process_browsertest.cc


### ch...@gmail.com (2016-03-23)

[Comment Deleted]

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

Thanks for taking the time to report this issue - our reward panel decided in $500 for this report.

We'll start payment next week.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/595339?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083873)*
