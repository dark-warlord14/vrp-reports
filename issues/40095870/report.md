# Security: URL bar spoofing on iOS (with SlimNav ON)

| Field | Value |
|-------|-------|
| **Issue ID** | [40095870](https://issues.chromium.org/issues/40095870) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2019-07-31 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 76.0.3809.80 beta  

Operating System: iOS iPhone 8

**REPRODUCTION CASE**

- Enable slim-navigation-manager

After fixing <https://crbug.com/chromium/971740>, I'm still able to repro it with another way.

1. Go to <https://lbstyle.github.io/o.html>
2. Tap on the button, the page will open a new tab with about:www.verylongurl.googlecloudplatform.accounts.google.com  
   
   (In this case Chrome will show ...tform.accounts.google.com and this is WAI)
3. Wait the page will load <https://lbstyle.github.io/attack.html>
4. Now tap on the button.

Actual: Observe that ..tform.accounts.google.com URL displayed but the content area still shows lbstyle.github contents.

Expected: Page should not be displayed ..tform.accounts.google.com URL.

## Attachments

- [4C959071-9E4F-4F4C-B94F-2CA6A64E6BA3.MP4](attachments/4C959071-9E4F-4F4C-B94F-2CA6A64E6BA3.MP4) (video/mp4, 682.6 KB)

## Timeline

### ch...@gmail.com (2019-07-31)

[Empty comment from Monorail migration]

### do...@chromium.org (2019-08-01)

Thanks for the report. +iOS folks to take a look.

[Monorail components: UI>Browser>Navigation]

### ju...@chromium.org (2019-08-01)

+stk

What do you think about changing tail clip to include about URLs.  this would change this from looking like:
  `tform.accounts.google.com`
to showing the scheme, e.g. 
  `about:google.com

We could go a stop further and just show `about`, the same way we only show domains in the steady view.

I'm not sure if this mitigates it enough, but at least it will show 'about' instead of google.

### ju...@chromium.org (2019-08-01)

+jdeblasio, for left eliding about scheme like we do data schemes as well.  

### ju...@chromium.org (2019-08-01)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-08-01)

Emily, could you please advice us on the best way for URL eliding. 

### jd...@chromium.org (2019-08-01)

I lean towards showing only 'about' and not showing the rest. Everything after the : is attacker-controlled, so left-eliding after about: doesn't buy us very much, and we can't expect that users will understand that the about: scheme is different.

Another option might be to show the full about: URL only if it's known-valid. Since they're internal-only, this seems like it could be possible?

As an aside, are you able to navigate to data:// URIs in the top frame on iOS? If so, that's probably also a bug -- we specifically disable that on Desktop because of this sort of spoofing.

(While this particular case isn't specifically addressed, similar issues are discussed in https://chromium.googlesource.com/chromium/src/+/master/docs/security/url_display_guidelines/url_display_guidelines.md#uncommon-schemes-and-virtual-urls and https://chromium.googlesource.com/chromium/src/+/master/docs/security/url_display_guidelines/url_display_guidelines.md#Eliding-URLs )

### ju...@chromium.org (2019-08-01)

Are there any valid uses of about scheme other than about:blank?  What if we just only show `about:blank` for any about scheme in the location bar.  

+srikanthg@ See crbug.com/953294 for the data url conversation

### jd...@chromium.org (2019-08-01)

[Comment Deleted]

### jd...@chromium.org (2019-08-01)

There also might be about:srcdoc, but that will never happen in the top frame. There are also a bunch of valid-ish about: urls, but they're translated to chrome:// URLs by url_formatter on Desktop. See https://cs.chromium.org/chromium/src/chrome/browser/browser_about_handler.h

about:blank seems also fine from a security UI perspective.

### ju...@chromium.org (2019-08-02)

chromium.khalil@  Does this also effect chrome or file urls?  I wasn't able to reproduce myself by modifying o.html

### ch...@gmail.com (2019-08-02)

No, this doesn't effect chrome or file urls.

### ju...@chromium.org (2019-08-02)

Thank you!

I think a reasonable fix will be something like https://chromium-review.googlesource.com/c/chromium/src/+/1730558, which will change all 'about' scheme URLs to display in the omnibox as simply about:blank. 

### eu...@chromium.org (2019-08-05)

Re to https://crbug.com/chromium/989497#c13: do we really want to introduce platform inconsistency and make the change only for iOS?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0612701f131ea3e367c17e425ad9a85d23c0512c

commit 0612701f131ea3e367c17e425ad9a85d23c0512c
Author: Justin Cohen <justincohen@google.com>
Date: Mon Aug 05 19:04:52 2019

[ios] Display all about:// urls as about:blank in location bar.

Bug: 989497
Change-Id: I83cafb3fdb0a5e8695d89eab7ede78628e1f26e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1730558
Commit-Queue: Justin Cohen <justincohen@chromium.org>
Reviewed-by: Ali Juma <ajuma@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Reviewed-by: Stepan Khapugin <stkhapugin@chromium.org>
Reviewed-by: Eugene But <eugenebut@chromium.org>
Auto-Submit: Justin Cohen <justincohen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#684060}

[modify] https://crrev.com/0612701f131ea3e367c17e425ad9a85d23c0512c/ios/chrome/browser/ui/location_bar/location_bar_model_delegate_ios.mm
[modify] https://crrev.com/0612701f131ea3e367c17e425ad9a85d23c0512c/ios/chrome/browser/web/window_open_by_dom_egtest.mm


### ju...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-08-05)

Please mark this bug as fixed before requesting merge. 

### ju...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-06)

Your change meets the bar and is auto-approved for M77. Please go ahead and merge the CL to branch 3865 (refs/branch-heads/3865) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-08-07)

If this is genuinely high severity, we should merge to stable as well per our severity guidelines - https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md - unless there's zero chance of an iOS M76 respin.

### sh...@chromium.org (2019-08-07)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2019-08-07)

adetaylor@/dominickn@ slimnav is disabled for 99.5% of M76 users, the remaining small percentage is enable for gathering crash data.  Given we have no plans in M76 to increase that percentage, do you still think this needs to go on M76?



### ju...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-08-07)

Thanks - no, it sounds reasonable to skip merge to M76 in this case then.

### sh...@chromium.org (2019-08-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ju...@chromium.org (2019-08-12)

This was cherry picked here: https://chromium-review.googlesource.com/c/chromium/src/+/1739628 on Aug 6th.

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/989497?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095870)*
