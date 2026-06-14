# Security: Site Isolation bypass using FileSystem URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40092525](https://issues.chromium.org/issues/40092525) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2018-09-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

While searching variant of <https://crbug.com/chromium/886976>, I found out that File System URL can also be used to bypass Site Isolation.

PoC is similar to <https://crbug.com/chromium/886976>, only the difference is that it is rendered in iframe. To do so, there's additional step to bypass blink::SecurityOrigin::CanDisplay check.

**VERSION**  

Chrome Version: 71 dev (should also repro in stable)  

Operating System: Windows 10 RS4

**REPRODUCTION CASE**

1. Go to <https://www.shhnjk.com/fileSystem.html> and attach WinDbg to that renderer process
2. Set breakpoint in `chrome_child!blink::DOMFileSystemBase::CreateFileSystemURL` and `chrome_child!blink::SecurityOrigin::CanDisplay`, and then hit `g`
3. Click "Go!" button on the Webpage
4. Once WinDbg hits breakpoint, skip till you come to `return url`
5. Modify "shhnjk" (73 68 68 6e 6a 6b) in "url"'s "string" value to "google" (67 6f 6f 67 6c 65)
6. Repeat this for 3 times
7. Once WinDbg hits breakpoint again, hit `g`
8. WinDbg would hits breakpoint again. change skip till you come to `String protocol = url.Protocol()`
9. Skip that and change `filesystem` protocol to anything else.
10. Then hit `g`
11. Observe that exploit works

Attaching video for detailed repro :)

Thanks!

## Attachments

- deleted (application/octet-stream, 0 B)
- [PoC.html](attachments/PoC.html) (text/plain, 1.2 KB)

## Timeline

### na...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### s....@gmail.com (2018-09-21)

[Comment Deleted]

### s....@gmail.com (2018-09-21)

Ooops, wrong file. Here's the right one.

### al...@chromium.org (2018-09-22)

Nice, thanks for the report!  Indeed, it appears that the browser-side logic to create filesystem URLs also relies on CPSP::CanCommitURL, similarly to blob URLs in https://crbug.com/chromium/886976.  More specifically, ChildProcessSecurityPolicyImpl::HasPermissionsForFileSystemFile() checks CanCommitURL() here: https://cs.chromium.org/chromium/src/content/browser/child_process_security_policy_impl.cc?l=1013&rcl=91269b920348317e3f7eef39467dd9fc4750d11f

I'm guessing using a subframe is required since top-level navigations to filesystem URLs are now blocked.  It probably makes sense to expand the fix we're considering in https://crbug.com/chromium/886976 to also cover this case.  I'll assign to myself for now.

I wrote a SecurityExploitBrowserTest that repros this, mostly along the lines of nick@'s ChromeSecurityExploitBrowserTest.CreateFilesystemURLInExtensionOrigin but for a cross-origin setup rather than an extension one.  

For the fix, perhaps CPSP::CanCommitURL can just call CanAccessDataForOrigin directly?  This is also nice because CPSP::CanCommitURL already handles unique origins correctly for blob/filesystem URLs.  

CPSP::CanCommitURL is used by:
- blob URL creation (two places, one for classic IPC and one for mojo) 
- filesystem URL creation
- Origin header
- CPSP::CanCommitURL itself to deal with nested URLs.

The blob/filesystem cases should check CanAccessDataForOrigin() given these bugs, but I'm not sure about the Origin header.  My attempt at this (PS2 of https://chromium-review.googlesource.com/c/chromium/src/+/1235343) has some layout test failures, showing that a content script should be able to attach an Origin header that doesn't match the origin lock, which probably makes sense... but then do we really want to use CanCommitURL() for checking the origin header?  Charlie, any thoughts on that, since I think you worked on the Origin header enforcements?


### al...@chromium.org (2018-09-24)

Looks like https://crbug.com/chromium/515309 discusses CanCommitURL enforcements for the Origin header.  It also mentions whitelisting chrome-extension:// headers for content scripts.

### lu...@chromium.org (2018-09-24)

1) Can we do the origin checks on the UI thread? 

I've talked with Alex about this bug and he pointed out that blob/filesystem creation takes place on the IO thread and therefore doesn't/cannot inspect RenderFrameHostImpl::GetLastCommittedOrigin (which is only available on the UI thread).  This means that tightening of RenderFrameHostImpl::CanCommitOrigin (see https://crbug.com/chromium/770239) wouldn't directly help in the blob/filesystem cases... unless we would consider bouncing to the UI thread when processing blob/filesystem requests.

I wonder if this is worth pursuing further (to do CanCommitOrigin checks only once, on the UI thread, in RenderFrameHostImpl and to avoid imperfectly duplicated CanCommitOrigin checks for the IO thread, in ChildProcessSecurityPolicy [imperfectly, because these IO-thread checks don't have visibility into UI-only data like hosted apps or site urls]).

AFAIR cookies are another example of checks happening on the IO thread, but I think that this case should go away after NetworkService ships (right?).


2) Previous attempts of CanCommitOrigin tightening led to some undesirable kills in the wild.

In https://crbug.com/797968#c12, Alex speculates about a scenario that might have made it difficult to enforce origin-lock-related checks in RenderFrameHostImpl::GetLastCommittedOrigin on the UI-thread.  We've wondered whether this same scenario would also spell trouble for IO-thread checks for blob/filesystem cases.  Maybe we can hope that the problematic scenario doesn't happen as frequently for blob/filesystem cases?


### cr...@chromium.org (2018-09-24)

Comments 4-5: I could see using CanAccessDataForOrigin for those cases, and maybe changing how the Origin header enforcement is done if it needs to special case content scripts.

https://crbug.com/chromium/888001#c6: We can't solely rely on a commit-time check on the UI thread, right?  The correct attacker origin can commit, but a later IPC can use a victim origin without attempting to commit it as a navigation.  I agree that being on the IO thread here is tricky, but I don't remember where we left off in discussing how to address it.  (Did it depend on Mojo?)

### bu...@chromium.org (2018-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2078096efde1976b0fa9c820df90cedbfb2b13bc

commit 2078096efde1976b0fa9c820df90cedbfb2b13bc
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Thu Sep 27 23:17:04 2018

Lock down blob/filesystem URL creation with a stronger CPSP::CanCommitURL()

ChildProcessSecurityPolicy::CanCommitURL() is a security check that's
supposed to tell whether a given renderer process is allowed to commit
a given URL.  It is currently used to validate (1) blob and filesystem
URL creation, and (2) Origin headers.  Currently, it has scheme-based
checks that disallow things like web renderers creating
blob/filesystem URLs in chrome-extension: origins, but it cannot stop
one web origin from creating those URLs for another origin.

This CL locks down its use for (1) to also consult
CanAccessDataForOrigin().  With site isolation, this will check origin
locks and ensure that foo.com cannot create blob/filesystem URLs for
other origins.

For now, this CL does not provide the same enforcements for (2),
Origin header validation, which has additional constraints that need
to be solved first (see https://crbug.com/515309).

Bug: 886976, 888001
Change-Id: I743ef05469e4000b2c0bee840022162600cc237f
Reviewed-on: https://chromium-review.googlesource.com/1235343
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#594914}
[modify] https://crrev.com/2078096efde1976b0fa9c820df90cedbfb2b13bc/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/2078096efde1976b0fa9c820df90cedbfb2b13bc/content/browser/child_process_security_policy_impl.h
[modify] https://crrev.com/2078096efde1976b0fa9c820df90cedbfb2b13bc/content/browser/security_exploit_browsertest.cc


### al...@chromium.org (2018-10-02)

Marking as fixed - see comments 11&12 on https://crbug.com/886976.

### sh...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-15)

Hi s.h.h.n.j.k@ - we looked into how the fixes landed, and believe were already fixing this issue after your reporting of https://crbug.com/chromium/886976. However for the additional test case and info, the VRP panel decided to award $500 for this one. Thanks as ever!

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-10-15)

Thanks!

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

(Already in 71)

### sh...@chromium.org (2019-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-01-08)

This issue was migrated from crbug.com/chromium/888001?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/786673]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092525)*
