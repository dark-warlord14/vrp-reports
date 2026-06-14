# UAF in libglesv2!gl::Texture::onUnbindAsSamplerTexture

| Field | Value |
|-------|-------|
| **Issue ID** | [40051860](https://issues.chromium.org/issues/40051860) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | pa...@blackowlsec.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2020-03-26 |
| **Bounty** | $5,000.00 |

## Description

Use-After-Free vulnerability in libglesv2!gl::Texture::onUnbindAsSamplerTexture (Inline Function @ 00007ffd`8ba8767e) [c:\b\s\w\ir\cache\builder\src\third\_party\angle\src\libANGLE\Texture.h @ 441].

It affects the GPU process.

**VERSION**  

Chrome Version: Google Chrome 83.0.4093.3 dev (64 bit)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

Minimized test case together with a required media file and windbg logs attached.

**CREDIT INFORMATION**  

Reporter credit: Pawel Wylecial of REDTEAM.PL

## Attachments

- [cm_texture.html](attachments/cm_texture.html) (text/plain, 287 B)
- [mp4.mp4](attachments/mp4.mp4) (video/mp4, 374.6 KB)
- [windbg.txt](attachments/windbg.txt) (text/plain, 4.7 KB)
- [cm_texture.html](attachments/cm_texture_53150994.html) (text/plain, 249 B)

## Timeline

### pa...@blackowlsec.com (2020-03-26)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-03-27)

cwallez@: Can you take a look at this, and re-route as necessary? Thanks!

I'm unable to repro this because I don't have access to a Windows environment while WFH (and it doesn't repro on Linux). That means that I can't find out when this was first introduced, either. Setting security flags preliminarily, but these might change as we learn more.

[Monorail components: Internals>GPU>ANGLE]

### cw...@chromium.org (2020-03-27)

Routing to geofflang@ as TL of ANGLE.

### ge...@chromium.org (2020-04-03)

Fix landed https://chromium-review.googlesource.com/c/angle/angle/+/2124588

### [Deleted User] (2020-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-03)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M80. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M81. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-03)

This bug requires manual review: We are only 3 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-04-03)

+adetaylor@(Security TPM), Since this is Security-Severity-High want to check. Can this CL wait for next M81 respin? 

So that the change will be well baked in lower channels as CL listed at https://crbug.com/chromium/1065186#c4 isn't landed on Canary. 



### ad...@google.com (2020-04-03)

Yep, let's wait for first M81 refresh.

### ge...@chromium.org (2020-04-06)

1. Does your merge fit within the Merge Decision Guidelines?
 Yes, it has been in canary for almost a week (since 83.0.4101.0).  Rolled into Chromium here: https://chromium-review.googlesource.com/c/chromium/src/+/2128850

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/angle/angle/+/2124588

3. Has the change landed and been verified on master/ToT?

Yes.  It has been landed for a week.

4. Why are these changes required in this milestone after branch?

Security fixes.

5. Is this a new feature?

No.

6. If it is a new feature, is it behind a flag using finch?

N/A

### na...@google.com (2020-04-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-08)

Congrats! The Panel decided to award $5,000 for this report. 

### na...@google.com (2020-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-17)

Please merge to M81, branch 4044, assuming everything continues to look good on Canary.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/91c39dae9a518706f2635ac8b87f9f5b5ed9001c

commit 91c39dae9a518706f2635ac8b87f9f5b5ed9001c
Author: Geoff Lang <geofflang@chromium.org>
Date: Mon Apr 20 18:37:46 2020

Update the active texture cache before changing the texture binding.

When a new texture is bound, the texture binding state is updated before
updating the active texture cache. With this ordering, it is possible to delete
the currently bound texture when the binding changes and then use-after-free it
when updating the active texture cache.

BUG=chromium:1065186

Change-Id: Id6d56b6c6db423755b195cda1e5cf1bcb1ee7aee
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2124588
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Reviewed-by: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 1288aa12369e36c3413537a6cbef6b8e7260fe98)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2156966
Reviewed-by: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/91c39dae9a518706f2635ac8b87f9f5b5ed9001c/src/libANGLE/State.cpp


### ad...@google.com (2020-05-04)

We shipped this fix in 81.0.4044.122 but I missed it from the release notes due to a bug in the scripts - I'll adjust them.

### ad...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### kb...@chromium.org (2020-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1065186?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051860)*
