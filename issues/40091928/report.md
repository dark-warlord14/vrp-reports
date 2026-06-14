# Security: Blob URL created from Data URL shares same process despite creator being cross-site

| Field | Value |
|-------|-------|
| **Issue ID** | [40091928](https://issues.chromium.org/issues/40091928) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2018-07-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a Blob URL is created from Data URL, it effectively has Opaque origin. But Site Isolation treat 2 opaque origins as same-site and commit it to same process when they are blob:null/. This is bad because those can be created from 2 different sites and may contain secret.

**VERSION**  

Chrome Version: 67.0.3396.99 + stable  

Operating System: macOS High Sierra 10.13.3

**REPRODUCTION CASE**

1. Go to <https://shhnjk.azurewebsites.net/ISO_blob_data.html>
2. Click on the button and observe that Blob URL created by process belongs to test.shhnjk.com and Blob URL created by process belongs to shhnjk.azurewebsites.net are now in the same process.

## Timeline

### es...@chromium.org (2018-07-14)

Over to Charlie for triage.

[Monorail components: Internals>Sandbox>SiteIsolation]

### sh...@chromium.org (2018-07-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-07-16)

Looks like we might be sharing processes for a unique origin?  (OOPIFs are normally put into an existing process for their site if possible, but obviously that shouldn't apply to unique origins.)  I'll try to confirm in a debugger this afternoon.

### dc...@chromium.org (2018-07-16)

I wonder if this could benefit from some of the work we've been talking about to track the creator origin / associate origins and URLs more strongly.

### al...@chromium.org (2018-07-16)

Checking on what's returned from GetSiteInstanceForNavigation, it looks like we end up placing the blob URL into a SiteInstance with site URL of "blob:".  That doesn't seem right -- presumably we should've left the blob URL in the same SiteInstance and process as the data URL that created it.

That explains why the second blob URL ended up incorrectly sharing the first blob URL's process - it also ends up needing a "blob:" SiteInstance, and it either reuses the first SiteInstance (if the second tab is in the same BrowsingInstance, which I believe is true in this repro), or it creates a new SiteInstance and reuses the first blob: SiteInstance's process, due to 
our subframe process reuse policy.  For the latter, the first process would be considered compatible for reuse since it's locked to the same "site" of "blob:".

### al...@chromium.org (2018-07-17)

I'll try to help out with this.  After chatting with Charlie, we think a reasonable short-term fix might be to also append the GUID portion of the blob URL to the site URL in cases where the blob URL has a unique origin, so that blobs created from different sites wouldn't share a process.

Ideally, we'd figure out that the blob URL was created by the data URL currently in the subframe and reuse that SiteInstance.  We could do this if we had GUIDs associated with unique origins, which I hear dcheng@ is working on, though we'd need additional plumbing to pass that information along with the dest_url of "blob:null/{guid}", since the latter is all we currently have in DetermineSiteInstanceForURL(), and that seems nontrivial.

I've also confirmed that you get "blob:null/{guid}" when creating a blob URL from a sandboxed iframe, so this is another way to get to this bug without using data URLs.

Another thing to consider here is whether we should disallow process reuse across processes locked to a site without a host, in case the URLs that resulted in these site URLs came from different sites.  This would affect site URLs like "blob:", "data:", "about:", "file:", "content:", etc.   This wouldn't be enough to fix this bug within the same BrowsingInstance, since we'd still find an existing SiteInstance when we look up something like "blob:".  OTOH, maybe the better thing to move toward is to make site URLs for these cases more granular (e.g., include path in site URL for a file URL, use full data URL as site URL), and keep the sharing where it doesn't pose any risks (e.g., for "about:").

### cr...@chromium.org (2018-07-18)

I agree with the plan to make site URLs more granular for unique origins.  We're already planning that for one case in https://crbug.com/chromium/780770, and it will help with data URLs in https://crbug.com/chromium/863069 as well.

### al...@chromium.org (2018-07-18)

I've got a CL started for using the full blob URL as site URL when the blob URL's origin is unique - https://chromium-review.googlesource.com/c/chromium/src/+/1142389

### bu...@chromium.org (2018-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b1f87486936ca0d6d9abf4d3b9b423a9c976fd59

commit b1f87486936ca0d6d9abf4d3b9b423a9c976fd59
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Thu Jul 19 01:51:51 2018

Avoid sharing process for blob URLs with null origin.

Previously, when a frame with a unique origin, such as from a data
URL, created a blob URL, the blob URL looked like blob:null/guid and
resulted in a site URL of "blob:" when navigated to.  This incorrectly
allowed all such blob URLs to share a process, even if they were
created by different sites.

This CL changes the site URL assigned in such cases to be the full
blob URL, which includes the GUID.  This avoids process sharing for
all blob URLs with unique origins.

This fix is conservative in the sense that it would also isolate
different blob URLs created by the same unique origin from each other.
This case isn't expected to be common, so it's unlikely to affect
process count.  There's ongoing work to maintain a GUID for unique
origins, so longer-term, we could try using that to track down the
creator and potentially use that GUID in the site URL instead of the
blob URL's GUID, to avoid unnecessary process isolation in scenarios
like this.

Note that as part of this, we discovered a bug where data URLs aren't
able to script blob URLs that they create: https://crbug.com/865254.
This scripting bug should be fixed independently of this CL, and as
far as we can tell, this CL doesn't regress scripting cases like this
further.

Bug: 863623
Change-Id: Ib50407adbba3d5ee0cf6d72d3df7f8d8f24684ee
Reviewed-on: https://chromium-review.googlesource.com/1142389
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#576318}
[modify] https://crrev.com/b1f87486936ca0d6d9abf4d3b9b423a9c976fd59/content/browser/site_instance_impl.cc
[modify] https://crrev.com/b1f87486936ca0d6d9abf4d3b9b423a9c976fd59/content/browser/site_instance_impl_unittest.cc
[modify] https://crrev.com/b1f87486936ca0d6d9abf4d3b9b423a9c976fd59/content/browser/site_per_process_browsertest.cc


### al...@chromium.org (2018-07-20)

Verified r576318 in Mac Canary 69.0.3497.0 using s.h.h.n.j.k@'s repro steps and URL.  The two blob subframes don't share a process anymore.  One side effect of the change is that the task manager entries now show up as "Subframe: blob:null/[guid]" instead of "Subframe: blob:".  The null/[guid] part may not really be worth showing to the user, but we can probably live with that for now.

### sh...@chromium.org (2018-07-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-28)

Just FYI, this might be known issue but any website can spawn hundreds of process. This is even easy after this patch because now all blob url with null origin are treat as cross-site.

PoC
https://test.shhnjk.com/max_iso.html

Code:
<body>
<script>
 setInterval(() => {document.body.appendChild(document.createElement("iframe")).src = "data:text/html,<script>location.href = URL.createObjectURL(new Blob(['test'], {type : 'text/html'}));<\/script>";},1);
</script>
</body>

This hangs Chrome as well as other application running in the OS. Maybe it's better to provide some detection against this technique and allow user to stop page's script as you do for infinity for-loop scripts.

### cr...@chromium.org (2018-07-30)

https://crbug.com/chromium/863623#c14: Thanks, yes, that's a known issue (https://crbug.com/chromium/841984).  Agreed that this might make it easier.

### aw...@chromium.org (2018-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-07-30)

$3,000 for this report. Thanks as always!

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-03)

Cl listed at #9 is already in M69 branch 3497 per https://crbug.com/chromium/863623#c10. Is there any merge needed for M69? If not, pls remove "Merge-Review-69" label. 

### al...@chromium.org (2018-08-03)

#21: Correct, r576318 initially appeared in 69.0.3497.0, so no need for a merge.

### go...@chromium.org (2018-08-03)

Adding "Merge-Reject-69" label so sheriffbot again doesn't request a merge to M69.

### go...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/863623?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091928)*
