# Security: Site Isolation bypass using Blob URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40092507](https://issues.chromium.org/issues/40092507) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage, Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2017-5124 |
| **Reporter** | s....@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2018-09-19 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

Masato Kinugawa found out that Site Isolation in Chrome 61 can be bypassed using UXSS[1] and Blob URL. Since we don't have UXSS in latest version, we can't confirm this vulnerability with UXSS. But I could simulate renderer compromise by attaching WinDbg and confirmed that this bug still exists.

Following PoC shows 3 evidences of Site Isolation bypass

1. Response of `fetch` to <https://www.google.com> is readable (first alert)
2. Cookie can be obtained by accessing DOM of `https://www.google.com` iframe (second alert)
3. Task manager in the end shows only 1 renderer process, indicating that Blob URL and `https://www.google.com` iframe are in the same process

**VERSION**  

Chrome Version: 71 dev (should also repro in stable)  

Operating System: Windows 10 RS4

**REPRODUCTION CASE**

1. Go to <https://www.shhnjk.com/blob.html> and attach WinDbg to that renderer process
2. Set breakpoint by `bp chrome_child!blink::BlobURLRegistry::RegisterURL` and hit `g`
3. Click "Go!" button on the Webpage.
4. Once WinDbg hits breakpoint, modify "shhnjk" (73 68 68 6e 6a 6b) in "origin"'s "host" value to "google" (67 6f 6f 67 6c 65)
5. And then modify "shhnjk" (73 68 68 6e 6a 6b) in "public\_url"'s "string" value to "google" (67 6f 6f 67 6c 65)
6. Then hit `g`
7. Observe that exploit works

If you are not familiar with WinDbg (like me), see attached video for detailed repro.

If this bug qualifies for bounty, please pay that to Masato Kinugawa.  

But please give acknowledgement to Masato and me :)

Thanks!

[1] <https://github.com/Bo0oM/CVE-2017-5124>

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### s....@gmail.com (2018-09-19)

Please CC masatokinugawa@gmail.com in this report, who's the original finder of this bug!

### mb...@chromium.org (2018-09-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### lu...@chromium.org (2018-09-19)

Thanks for the report!  I see that BlobDispatcherHost::OnRegisterPublicBlobURL tries to verify the IPC payload received from the renderer, but it does so using CanCommitURL which AFAIK does't consider the origin lock that Site Isolation might have put on the renderer:

void BlobDispatcherHost::OnRegisterPublicBlobURL(const GURL& public_url,
                                                 const std::string& uuid) {
  DCHECK_CURRENTLY_ON(BrowserThread::IO);
  ChildProcessSecurityPolicyImpl* security_policy =
      ChildProcessSecurityPolicyImpl::GetInstance();

  // Blob urls have embedded origins. A frame should only be creating blob URLs
  // in the origin of its current document. Make sure that the origin advertised
  // on the URL is allowed to be rendered in this process.
  if (!public_url.SchemeIsBlob() ||
      !security_policy->CanCommitURL(process_id_, public_url)) {
    DVLOG(1) << "BlobDispatcherHost::OnRegisterPublicBlobURL("
             << public_url.spec() << ", " << uuid
             << "): Invalid or prohibited URL.";
    bad_message::ReceivedBadMessage(this, bad_message::BDH_DISALLOWED_ORIGIN);
    return;
  }

### cr...@chromium.org (2018-09-20)

Yes, thanks for the report!  Some of the enforcements for compromised renderers are still works in progress, but this is a nice finding.  We chatted about this and realized the blob code is probably using the wrong check-- it should most likely be using CanAccessDataForOrigin instead of CanCommitURL (which seems to be a more suitable check, and would have avoided this bug even before we tighten CanCommitURL).

We'll sanity check that to make sure we're not regressing anything from Nick's r422474, but I suspect that will be the right way to apply origin lock checks.

Alex or Lukasz, would one of you want to take a closer look to confirm?

[Monorail components: Blink>Storage]

### al...@chromium.org (2018-09-20)

Looking closer, I don't think we can just change CanCommitURL to CanAccessDataForOrigin, as CanAccessDataForOrigin only works if the process creating the blob URL is origin-locked.  This won't be the case in some cases, including extensions and WebUI.  The latter is covered  ChromeSecurityExploitBrowserTest.CreateBlobInOtherChromeUIOrigin, which I confirmed starts to fail if we remove CanCommitURL.  So I think we do want to still check the scheme grant performed by CanCommitURL, and additionally check origin locks with CanAccessDataForOrigin.  (Eventually, CanCommitURL should just handle everything.)  I'll also add the enforcements bug here for tracking.

I put together a content_browsertest which seems to repro this, along with this potential fix, at https://chromium-review.googlesource.com/c/chromium/src/+/1235343.  If it's green, I can clean it up and send for review.

### na...@chromium.org (2018-09-20)

Adding mek@, who has worked on blob: navigations code moving to Mojo. I was under the impression that even blob: registration was moved over to Mojo, but the code being referenced in https://crbug.com/chromium/886976#c3 and the test Alex has put up all assume classic IPC.

Poking at this, it looks like we do have Mojo based blob: URL registration in third_party/blink/public/mojom/blob/blob_registry.mojom. mek@, can you help clarify what is the current state of blob: mojofication?

### me...@chromium.org (2018-09-20)

blob: mojofication should all be working (and is turned on/required by network servicification). Shipping blob URL mojofication on its own though is still blocked by https://crbug.com/chromium/705114 (which itself is blocked by https://crbug.com/chromium/819761). And I have no idea what the status of either of those is.

### na...@chromium.org (2018-09-20)

[Empty comment from Monorail migration]

### al...@chromium.org (2018-09-20)

Looks like the mojo path has the same problem in BlobURLStoreImpl::Register(), which also checks CanCommitURL() currently:  https://cs.chromium.org/chromium/src/storage/browser/blob/blob_url_store_impl.cc?l=78&rcl=b8d3bfaa306273d85c542c0aca9352d767a95e33

Also, looking at tryjob results from #5, I think we'll need to relax the CanAccessDataForOrigin check for unique origins: e.g., a sandboxed frame on foo.com, locked in a foo.com renderer, should be able to create a blob URL with a null origin.  Not sure if there are any other special cases.

Also, found some relevant discussion that mek@ and I had in: https://chromium-review.googlesource.com/c/chromium/src/+/823828/5/storage/browser/blob/blob_registry_impl.cc#563, where we kind of anticipated that this would be problematic with --site-per-process and --isolate-origins and that we should strengthen the check in a followup - now is a good time for that followup.

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

I verified the fix from #10 in Win Canary 71.0.3567.0.  I followed the windbg-based repro steps and confirmed that they now lead to a renderer kill (crash id 3c87724eb339387e).

### al...@chromium.org (2018-10-02)

Also double-checked and didn't see any new crashes that might've been introduced by this in 71.0.3564.0+.

### sh...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-15)

Nice one! The VRP Panel decided to award $8,000 for this report.  Cheers!

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-10-15)

Thanks awalley@! As per https://crbug.com/chromium/886976#c0, could you make sure that this bug is rewarded to Masato? Thanks again!

### ma...@gmail.com (2018-10-15)

I'd like to share the bounty with Jun (s.h.h.n....@gmail.com) since he helped me in investigating the details of this bug.
Could you pay Jun and me $4000 each? Thanks!

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

(Already in 71)

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2019-09-24)

Going forward, Site Isolation bypasses leading to unexpected process sharing should be treated as high severity - please see r679314 and r698638.

### lu...@chromium.org (2019-09-24)

[Empty comment from Monorail migration]

### is...@google.com (2019-09-24)

This issue was migrated from crbug.com/chromium/886976?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Storage, Internals>Sandbox>SiteIsolation]
[Monorail blocking: crbug.com/chromium/786673]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092507)*
