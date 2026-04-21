# Security: XSS in Chrome UI (password settings) with malicious extension name

| Field | Value |
|-------|-------|
| **Issue ID** | [40059860](https://issues.chromium.org/issues/40059860) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Settings |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ol...@oliverdunk.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2022-06-03 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Extension names are not escaped when shown at chrome://settings/passwords. This allows an extension with a specially crafted name to render additional links in the UI and trick the user in to navigating to an external site. The extension also needs to make itself appear on this page by using the chrome.privacy.services.passwordSavingEnabled API: <https://developer.chrome.com/docs/extensions/reference/privacy/>

The issue exists because inner-h-t-m-l is used to avoid Polymer's default escaping behaviour (<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/settings/controls/extension_controlled_indicator.html;l=23>), and the extension name is directly included in the returned text (<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/settings/controls/extension_controlled_indicator.ts;l=47>). i18nAdvanced does restrict the allowed tags but this does not seem like an appropriate level of sanitisation given that extension names should never contain HTML. This allowed me to both include an external link and put an HTML comment at the end of the extension name that prevented the rest of the expected UI text from rendering.

An extension like this would likely not pass Chrome Web Store review. However, there are other scenarios in which an extension can be installed, such as through enterprise policy. In these scenarios my expectation as a user is that certain parts of the Chrome UI reliably tell me what is happening on the system. This vulnerability could be used to hinder that.

**VERSION**  

Chrome Version: Reproduced in 102.0.5005.61 stable  

Operating System: macOS

As far as I can tell, this affects all shipping Chromium versions.

**REPRODUCTION CASE**

1. Navigate to chrome://extensions and enable developer mode with the toggle in the top right.
2. Drag the attached xss-demo-extension.zip on to the page.
3. Navigate to chrome://settings/passwords
4. Notice that like in xss.png, a link is rendered which sends the user to example.com. This appears as though it is part of Chrome and not part of the extension name.

Notes:

- I've attached normal.png which shows how things render for a normal extension. Notice that more text shows.
- Since this template said not to include zip files, I've also included the background.js and manifest.json which can be put in to a folder and then loaded if you wish to avoid loading a zip.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: NA  

Crash State: NA  

Client ID (if relevant): NA

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Oliver Dunk

## Attachments

- [xss-demo-extension.zip](attachments/xss-demo-extension.zip) (application/octet-stream, 651 B)
- [xss.png](attachments/xss.png) (image/png, 128.5 KB)
- [normal.png](attachments/normal.png) (image/png, 123.0 KB)
- [background.js](attachments/background.js) (text/plain, 69 B)
- [manifest.json](attachments/manifest.json) (text/plain, 266 B)
- [malicious_case_after.png](attachments/malicious_case_after.png) (image/png, 112.6 KB)
- [malicious_case_before.png](attachments/malicious_case_before.png) (image/png, 121.0 KB)
- [normal_case_after.png](attachments/normal_case_after.png) (image/png, 38.5 KB)
- [normal_case_before.png](attachments/normal_case_before.png) (image/png, 34.3 KB)

## Timeline

### ol...@oliverdunk.com (2022-06-03)

I think adding the UI>Browser>WebUI component automatically added a CC. I hope that's ok.

### [Deleted User] (2022-06-03)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-06-03)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>WebUI UI>Settings]

### dp...@chromium.org (2022-06-03)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-06-03)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-06-03)

Thanks for the report. I am able to reproduce. Marking as Available for now, and will follow-up with any other updates in this thread.

### dp...@chromium.org (2022-06-03)

@jun.kokatsu: Please see comment at [1] which is related to a possible fix for this vulnerability.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2222115/27#message-d6fb92c66b9dd4a8d048bc82032927cd742f1113

### ol...@oliverdunk.com (2022-06-04)

dpapad@: Thanks for taking a look at this so quickly! One thing I would say (and forgive me if I’m misunderstanding the above comment) is that trying to restrict the URLs feels like the wrong fix? It would definitely be a nice improvement but realistically I don’t see a reason to allow any HTML whatsoever (links, comments etc.). The extension name should just be rendered as plain text.

### dp...@chromium.org (2022-06-04)

> ... is that trying to restrict the URLs feels like the wrong fix?

It would prevent the link to an external URL from showing up as part of Chrome's own UI, which could be considered as a partial fix I think

> I don’t see a reason to allow any HTML whatsoever (links, comments etc.)

Agreed. The ideal fix is to disallow any external HTML from being added to the page. This might be slighly more involved though, but would be required to consider this bug fully fixed.


### ct...@chromium.org (2022-06-06)

Setting some security labels. Rendering arbitrary links in chrome:// pages seems pretty bad, but the multiple limitations on this mitigate it somewhat, so I think this seems reasonably Severity-Medium. It looks like the root cause has been around for a while, so setting FoundIn-102.

dpapad@ could you own this, at least for now? Feel free to re-assign as you see fit though.

(Also, swapping Jun's email to their new one for visibility.)

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-06)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@chromium.org (2022-06-06)

Candidate fix at [1], which fixes by making a UI change. See attached before/after screenshots below.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3690569

### dp...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7

commit e7664fbc7d47fb3ffc92098f61dd53eff3d822d7
Author: dpapad <dpapad@chromium.org>
Date: Tue Jun 07 18:22:05 2022

Settings: Prevent rendering of extension name as HTML.

Bug: 1332881
Change-Id: I21d9b0e094003c7014e8b6745ffd30fa6b6fae92
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3690569
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1011562}

[add] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/app/settings_strings_grdp/IDS_SETTINGS_MANAGE.png.sha1
[modify] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/app/settings_strings.grdp
[modify] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/browser/resources/settings/controls/extension_controlled_indicator.ts
[modify] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/browser/resources/settings/controls/extension_controlled_indicator.html
[modify] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/browser/ui/webui/settings/settings_localized_strings_provider.cc
[modify] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/test/data/webui/settings/extension_controlled_indicator_tests.ts
[modify] https://crrev.com/e7664fbc7d47fb3ffc92098f61dd53eff3d822d7/chrome/browser/ui/webui/settings/chromeos/main_section.cc


### dp...@chromium.org (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

Requesting merge to beta M103 because latest trunk commit (1011562) appears to be after beta branch point (1002911).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-08)

Merge review required: M103 is already shipping to beta.

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

### dp...@chromium.org (2022-06-09)

> 1. Why does your merge fit within the merge criteria for these milestones?

Security vulnerability.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3690569

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Not a major issue.

### am...@chromium.org (2022-06-13)

M103 merge approved, please merge this fix to branch 5060 NTL 10am PST tomorrow, Tuesday 14 June so this fix can be included in the M103 cut for the next stable channel release -- thank you! 

### dp...@chromium.org (2022-06-13)

> M103 merge approved, please merge this fix to branch 5060 NTL 10am PST tomorrow, Tuesday 14 June so this fix can be included in the M103 cut for the next stable channel release -- thank you!

The CL to be merged is actually introducing a new string. Is this a problem for merging?

### pb...@google.com (2022-06-13)

+govind@ Translations TL to add more.

### go...@chromium.org (2022-06-13)

We passed the string freeze deadline for M103 and this will require emergency string translation and delay M103 Stable RC cut. It is best if this can wait for M104 or M103  security respin later.


+Security TPMs to assess merge for M103.




### am...@chromium.org (2022-06-13)

Yes, given the level of mitigation of this issue and the severity, I feel this can wait until M103 security refresh or 104 stable milestone. 

### dp...@chromium.org (2022-06-13)

> I feel this can wait until M103 security refresh or 104 stable milestone.

Do you have a preference between these two though? If not, let's just go with M104 then which requires the least amount of work (basiclaly nothing needs to be done, besides waiting for 104 to roll out).

### am...@chromium.org (2022-06-14)

Thank you for checking. I mean obviously as a security person, I would prefer earlier mitigation roll-outs, but given that we also need to balance with safety and stability, and given the heft of mitigations on this one, I believe we can wait on 104 for this. The time difference between 103 refresh to 104 is relatively negligible.  

### am...@chromium.org (2022-06-14)

removing merge approval for 103 to reflect above and avoid unnecessary automated or manual pings to merge. 

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-28)

Congratulations, Oliver! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1332881?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Settings]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059860)*
