# Security: Web Share dialog URL is not elided correctly on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [40059765](https://issues.chromium.org/issues/40059765) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebShare, UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Android |
| **Reporter** | st...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2022-05-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

After reading <https://crbug.com/chromium/1291735>, I noticed that the URL is not elided [0](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/url_display_guidelines/url_display_guidelines.md#eliding-urls) in the share dialog on Android as well.

**VERSION**  

Chrome Version: 104.0.5084.0  

Operating System: Android 12 (this may also apply to other mobile platforms, I only have an Android to test)

**REPRODUCTION CASE**

1. Open <https://long-extended-subdomain-name-containing-many-letters-and-dashes.badssl.com>
2. Click the "Share" icon from the menu

## Attachments

- [poc.jpg](attachments/poc.jpg) (image/jpeg, 480.2 KB)
- [fullscreen.jpg](attachments/fullscreen.jpg) (image/jpeg, 229.6 KB)
- [Screenshot_20220609_175232.png](attachments/Screenshot_20220609_175232.png) (image/png, 258.9 KB)

## Timeline

### [Deleted User] (2022-05-26)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-26)

I can reproduce this in M102. Triaging to a WebShare OWNER and CC'ing some UrlFormatting folks

[Monorail components: Blink>WebShare UI>Security>UrlFormatting]

### [Deleted User] (2022-05-26)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-05-26)

Quick question as I don't have a test device handy: Do we force the Omnibox to show when the sharing dialog triggers? Or could the Omnibox be hidden when this is showing?

### st...@gmail.com (2022-05-26)

Re https://crbug.com/chromium/1329541#c4, I just tried a simple demo and the omnibox is not guaranteed to be always shown when the share dialog is present.

The page can, for example, enter fullscreen after the dialog is shown.


```
document.body.onclick = () => {
    setTimeout(() => {
        document.documentElement.requestFullscreen();
    }, 4000);
}
```

### ct...@chromium.org (2022-05-26)

Thanks for testing! That definitely increases the security impact of this vs. if the Omnibox was guaranteed to be showing.

(Aside: On desktop, we would prevent fullscreen and force fullscreen to drop when a dialog like this is shown. I don't think we have an equivalent thing on Android.)

### er...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2022-05-31)

[Empty comment from Monorail migration]

### fi...@chromium.org (2022-06-09)

I presume we'll need to do something like this...

  formatted_origin = url_formatter::FormatUrlForSecurityDisplay(
      url, url_formatter::SchemeDisplay::OMIT_CRYPTOGRAPHIC);


### fi...@chromium.org (2022-06-09)

Hmm, on second look, it seems like we are already using a cousin of the function above, specifically:

  formatUrlForDisplayOmitSchemeOmitTrivialSubdomains(url);

... but we're eliding the end, instead of the beginning, so the top-level domain is being crowded out by all the extra info. I can change this to elide from the start, instead, which fixes the url issue. But I've got a couple of questions:

1) Should we continue to use formatUrlForDisplayOmitSchemeOmitTrivialSubdomains or should we use FormatUrlForSecurityDisplay?

2) The two fields shown in https://crbug.com/chromium/1329541#c5 are title and url, respectively. The top one is free-flow text. The second is a formatted url. It seems obvious that we can elide the url from the start instead of the end, but do we have a preference for eliding the _title_ (start/end)?


### ct...@chromium.org (2022-06-09)

(1) I think part of the trickiness here is that the current URL display includes the path [1] (because that's part of what you're sharing), and we don't have good support for eliding the URL in these cases. The Omnibox on Android handles this by doing some complicated layout shenanigans (determining width of different URL components and scrolling the view correctly). Maybe it would be okay to just have origin (FormatURLForSecurityDisplay()) and title though, and then the elision problem is easier?

(2) Probably up to your best judgment. I think eliding title at the end is more what users would expect?

### ct...@chromium.org (2022-06-09)

Oops forgot to add the reference: [1] https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/url_formatter_android.cc;l=122;drc=7f3bd3d40fffacda522b97ddfa94085a35d0a0c9

### fi...@chromium.org (2022-06-09)

More context: https://chromium-review.googlesource.com/c/chromium/src/+/3698524

### fi...@chromium.org (2022-06-09)

Didn't see comments 12 and 13 before posting 14, but I've updated the CL now to reflect what you suggested. 

The result now looks like this...



### fi...@chromium.org (2022-06-09)

This is with title elided at the end and url elided at the start. Also using FormatURLForSecurityDisplay.

### ct...@chromium.org (2022-06-09)

Thanks! If Sharing folks are okay with losing the path here, that looks good to me.

### er...@chromium.org (2022-06-10)

lgtm

### fi...@chromium.org (2022-06-13)

Actually, I think it is the other way around (whether they are "if the Sharing folks are ok with adding more data"). 

If I switch out the formatting functions as I suggested, we are adding a bunch of data (scheme and subdomains) which were left out by design. 

It therefore looks like eliding the string is sufficient to fix the bug. 

### gi...@appspot.gserviceaccount.com (2022-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f2b34be8865a6b63005ebc65588aa49e0392e91c

commit f2b34be8865a6b63005ebc65588aa49e0392e91c
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Wed Jun 15 09:53:43 2022

[Android]: Webshare: Adjust the eliding in header.

Bug: 1329541
Change-Id: Id6dbdc3b8064265900f7e1e1cead2fce9f6f958d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3698524
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1014364}

[modify] https://crrev.com/f2b34be8865a6b63005ebc65588aa49e0392e91c/chrome/android/java/res/layout/share_sheet_content.xml


### fi...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

Requesting merge to beta M103 because latest trunk commit (1014364) appears to be after beta branch point (1002911).

Requesting merge to dev M104 because latest trunk commit (1014364) appears to be after dev branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-06-16)

+Amy (Security TPM) for M013 and M104 merge review. 

Please note we already cut M103 Stable RC. Thank you. 

### [Deleted User] (2022-06-16)

Merge approved: your change passed merge requirements and is auto-approved for M104. Please go ahead and merge the CL to branch 5112 (refs/branch-heads/5112) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-16)

Merge review required: M103 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fi...@chromium.org (2022-06-20)

1. Why does your merge fit within the merge criteria for these milestones?

It addresses a P1 security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3698524

3. Have the changes been released and tested on canary?

Yes and yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Probably no testing required, but if we decide to perform a manual test, the repro steps are in the original post (https://crbug.com/chromium/1329541#c0) and the results should look like https://crbug.com/chromium/1329541#c15, and not like 'poc.jpg' in the original post. Focus on the second line in the share window (below the text in bold). 

### [Deleted User] (2022-06-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e88ea882ac18312332c9d416af66b00bb92fb1c

commit 4e88ea882ac18312332c9d416af66b00bb92fb1c
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Tue Jun 21 11:22:10 2022

[Android]: Webshare: Adjust the eliding in header.

(Cherry picking to branch 104).

(cherry picked from commit f2b34be8865a6b63005ebc65588aa49e0392e91c)

Bug: 1329541
Change-Id: Id6dbdc3b8064265900f7e1e1cead2fce9f6f958d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3698524
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1014364}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714611
Cr-Commit-Position: refs/branch-heads/5112@{#158}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/4e88ea882ac18312332c9d416af66b00bb92fb1c/chrome/android/java/res/layout/share_sheet_content.xml


### gi...@appspot.gserviceaccount.com (2022-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/200316fcab7faa3ae07042edf6ff9c4add2d5761

commit 200316fcab7faa3ae07042edf6ff9c4add2d5761
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Tue Jun 21 12:23:00 2022

[Android]: Webshare: Adjust the eliding in header.

(Cherry picking to branch 103).

(cherry picked from commit f2b34be8865a6b63005ebc65588aa49e0392e91c)

Bug: 1329541
Change-Id: Id6dbdc3b8064265900f7e1e1cead2fce9f6f958d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3698524
Reviewed-by: Boris Sazonov <bsazonov@chromium.org>
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1014364}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714254
Cr-Commit-Position: refs/branch-heads/5060@{#1009}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/200316fcab7faa3ae07042edf6ff9c4add2d5761/chrome/android/java/res/layout/share_sheet_content.xml


### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations, Thomas! The VRP Panel has decided to award you $500 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### go...@chromium.org (2022-07-03)

Looks like this got merged to M103 branch 5060 without approval.

amyressler@, are you ok with this merge? 

### am...@chromium.org (2022-07-03)

This fix missed the deadline for M103 stable cut and did not require immediate review to backmerged it seems to have been backmerged without security review/approval. This is a super minimal fix, however, and is fine to be included in the next planned 103 stable respin on 19 July 

### fi...@chromium.org (2022-07-05)

I don't think this was merged to 103 without approval. 

I suspect this is just a bug labelling mismatch, possibly by the bot. 

Here is the summary from the bug comments above:

https://crbug.com/chromium/1329541#c20: CL is checked in to trunk.
https://crbug.com/chromium/1329541#c24: Request CL be merged to branches 103 and 104.
https://crbug.com/chromium/1329541#c26: Obtain merge approval for 104 branch.
https://crbug.com/chromium/1329541#c27: Receive questionnaire for merging to 103.
https://crbug.com/chromium/1329541#c28: Submit answers to questionnaire.
https://crbug.com/chromium/1329541#c29: Receive response (3hrs later) : "Issue approved for merge"
https://crbug.com/chromium/1329541#c30: Cherry pick to 104 (because of https://crbug.com/chromium/1329541#c26).
https://crbug.com/chromium/1329541#c31: Cherry pick to 103 (because of https://crbug.com/chromium/1329541#c29).


### am...@chromium.org (2022-07-08)

Thank you for that breakdown. I think this was a miscommunication of labeling and the bot's lack of specificity. 
I think Sheriffbot failed at being more specific in https://crbug.com/chromium/1329541#c29, as the "issue approved for merge" was specific to M104. https://crbug.com/chromium/1329541#c26 shows M104 merge approval as that was automatically approved at that time due to timing of this fix vs branching and release cycle. 

Merge review for M103/stable should have been manual due to this fix being included in a stable release. The fix was minimal and with the thorough checks and responses in the merge review questionnaire (thank you for that!) there's no concerns here. :) 


### [Deleted User] (2022-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

stw.stw.tom@ - sorry - due to the merge kerfuffle above, this doesn't seem to have been credited in the Chrome release notes, nor had a CVE allocated. We'll take care of that! Apologies for the delay.

### st...@gmail.com (2022-12-13)

No worries - you can use "Thomas Orlita" as the credit info (I forgot to mention that in https://crbug.com/chromium/1329541#c0).

### st...@gmail.com (2023-01-17)

finnur@, could you please clarify what the current expected behaviour of eliding the URL string is as mentioned in https://crbug.com/chromium/1329541#c19? Does this mean that the URL as a whole will be elided from start, hiding the origin if the path is too long (current behaviour)? Is that acceptable from a security perspective (especially if the omnibox is not visible)?

Thanks!

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1329541?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebShare, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059765)*
