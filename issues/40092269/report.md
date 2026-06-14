# Use after free in third_party/WebKit/LayoutTests/fast/dom/HTMLLinkElement/link-and-subresource-test.html

| Field | Value |
|-------|-------|
| **Issue ID** | [40092269](https://issues.chromium.org/issues/40092269) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2011-06-28 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version:  

Chromium 14.0.805.0 (Developer Build 90701) Ubuntu 11.04  

WebKit 535.1 (trunk@89816)

not affected: beta, stable

Operating System: linux 64bit

**REPRODUCTION CASE**

<link rel="prefetch" href="resources/nick.jpg" onload="nick\_onload()" />
<img src="resources/nick.jpg" onload="nick\_onload()" />

or  

third\_party/WebKit/LayoutTests/fast/dom/HTMLLinkElement/link-and-subresource-test.html

nick.jpg is not required to exist

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan/vg  

Crash State:

Invalid read of size 4  

at 0x1AAD59C: WebCore::CachedResource::stopLoading() (CachedResource.h:184)  

by 0x1AB62A1: WebCore::CachedResourceRequest::didFail(WebCore::SubresourceLoader\*, WebCore::ResourceError const&) (CachedResourceRequest.cpp:200)

Address 0x3628c9c8 is 24 bytes inside a block of size 920 free'd  

at 0x4C29146: free (vg\_replace\_malloc.c:913)  

by 0x1AAF74E: WebCore::CachedResource::unregisterHandle(WebCore::CachedResourceHandleBase\*) (CachedResource.cpp:520)  

by 0x1AB04E8: WebCore::CachedResourceHandleBase::setResource(WebCore::CachedResource\*) (CachedResourceHandle.cpp:36)

## Attachments

- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 4.0 KB)

## Timeline

### in...@chromium.org (2011-06-28)

This looks like a very recent regression and might be coming from http://trac.webkit.org/changeset/89719.

Gavin, can you please take a look.

### sc...@gmail.com (2011-06-28)

The implicated WebKit revision looks like it's in M14 but not M13.

### ga...@chromium.org (2011-06-28)

Thanks, inferno & scarybeasts.  I'm on this now.

### in...@chromium.org (2011-06-28)

Looks like the failure was filed in http://webkit.org/b/60097 and http://test-results.appspot.com/dashboards/flakiness_dashboard.html#showExpectations=true&tests=fast%2Fdom%2FHTMLLinkElement%2Flink-and-subresource-test.html

The testcase is different since in this case, image does not exist which helps to delay load.

### in...@chromium.org (2011-06-28)

just a fyi, it easily reproduces for me on windows canary build (without needing any memory debugging tool like ASAN, valgrind, etc).

### mi...@gmail.com (2011-06-28)

@inferno: cool. can I get stack traces from canary build? does canary build have asserts enabled? can I run linux debug build outsite of debugger? can I ask you questions outside these comments? :D 

### ga...@chromium.org (2011-06-28)

Thanks.  I am reproducing this well in Linux, too.  I believe this is not a regression, but rather a new bug this change has uncovered.  I'll update if I have something more specific.

### in...@chromium.org (2011-06-28)

can I get stack traces from canary build? 
No, but you can get crash id and it is awesome to tell us about those when filing bugs. Browse to chrome://crashes/

does canary build have asserts enabled? 
No, sorry, it is a release build.

can I run linux debug build outsite of debugger? can I ask you questions outside these comments? :D 
Why would do need that, debug build is for hitting the asserts. 

Yeah you can add me on google chat at aarya@google.com

### in...@chromium.org (2011-06-28)

Talked to Gavin, this is not a regression. Fixing tags.

Also adding security labels and credits to webkit bug.

### in...@chromium.org (2011-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-06)

Moving all M12 bugs to M13. We won't have another M12 patch.

### in...@chromium.org (2011-07-07)

http://trac.webkit.org/changeset/90595

### sc...@gmail.com (2011-07-12)

Merged to M13: http://trac.webkit.org/changeset/90857

### ab...@chromium.org (2011-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2011-07-15)

[Empty comment from Monorail migration]

### ga...@chromium.org (2011-07-20)

I have some concerns about the merge for this back to m13.  It's far from obvious that this merge did the right thing.  Take a look at https://bugs.webkit.org/show_bug.cgi?id=62308 , which is not in m13 and conflicts a lot with the original patch.

This may be ultimately what's responsible for the crash observed in https://crbug.com/chromium/89774 , which forced the revert today of the backport of https://crbug.com/chromium/80729.

I am going to focus my investigation of https://crbug.com/chromium/89774 on the possibility that this backport was not great...  As well, I have grave concerns about the backport: looking at this stack, I think the only way we can be saved is if the timer dies quickly (and I bet most of the time it probably does), since before the revert of 80729 we had a null dereference in the timer waiting to be, whereas the change we rolled back had the dereference immediately.  Neither are good or acceptable.  The good news is I bet that this will reproduce well.

japhat, what do you think about any of these three issues?  

### sc...@gmail.com (2011-07-20)

$1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-21)

https://bugs.webkit.org/show_bug.cgi?id=60097

### sc...@gmail.com (2011-08-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/87729?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/200215]
[Monorail mergedwith: crbug.com/chromium/87593, crbug.com/chromium/89061]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092269)*
