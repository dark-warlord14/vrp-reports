# Security: heap-use-after-free in base::SupportsUserData::GetUserData

| Field | Value |
|-------|-------|
| **Issue ID** | [40058794](https://issues.chromium.org/issues/40058794) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox, UI>Browser>Sharing |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | yu...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2022-02-16 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

When we enable #share-context-menu in chrome://flags, "Share" submenu will be created in the menu when we right click omnibox. A raw webcontents pointer hold in ShareSubmenuModel and not observer it's lifecycle. If the webcontents destroyed before click "Create QRCode.." option, UaF will occur.

This issue maybe introduced by <https://chromium-review.googlesource.com/c/chromium/src/+/3306414>.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/omnibox/omnibox_view_views.cc;drc=c26af9bfc075bbed0c70d2371b9021d3a3479d92;l=1919>  

void OmniboxViewViews::MaybeAddShareSubmenu(  

ui::SimpleMenuModel\* menu\_contents) {  

content::WebContents\* web\_contents = location\_bar\_view\_->GetWebContents();  

...  

share\_submenu\_model\_ = std::make\_unique[share::ShareSubmenuModel](javascript:void(0);)(  

web\_contents, // raw pointer webcontents in the model  

std::make\_unique[ui::DataTransferEndpoint](javascript:void(0);)(ui::EndpointType::kDefault,  

false),  

share::ShareSubmenuModel::Context::PAGE, page\_url,  

web\_contents->GetTitle());  

...  

}

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/share/share_submenu_model.h;drc=c26af9bfc075bbed0c70d2371b9021d3a3479d92;l=89>

**VERSION**  

Chrome Version: stable  

Operating System: all

**REPRODUCTION CASE**

1. enable #share-context-menu option in chrome://flags
2. install attached extension
3. right click the first tab omnibox and click "Create QRCode.." option after first tab discard

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan of MoyunSec VLab

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.2 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 176 B)
- [background.js](attachments/background.js) (text/plain, 194 B)
- [record.mov](attachments/record.mov) (video/quicktime, 5.6 MB)

## Timeline

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### yu...@gmail.com (2022-02-17)

There is a same problom in SendTabToSelfSubMenuModel. Even though it use a weakptr wrap webcontents, but does not check if it is null. And will cause a null pointer dereference crash in CreateNewEntry.

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/send_tab_to_self/send_tab_to_self_sub_menu_model.h;drc=a0c577275320741e104ae963aac4d8d7388da800;l=57
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/send_tab_to_self/send_tab_to_self_desktop_util.cc;drc=c26af9bfc075bbed0c70d2371b9021d3a3479d92;l=37

### cl...@chromium.org (2022-02-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5765900007178240.

### yu...@gmail.com (2022-02-18)

I don't think this issue needs to be verified by ClusterFuzz, maybe there are something wrong.

### ye...@google.com (2022-02-22)

Yep you're right, that was my bad, I didn't realize this was in the browser process at first.

Victor could you confirm if this issue is related to  https://chromium-review.googlesource.com/c/chromium/src/+/3306414?


[Monorail components: UI>Browser>Omnibox]

### ye...@google.com (2022-02-22)

[Empty comment from Monorail migration]

### vi...@google.com (2022-02-22)

Before I dig into the details:
- Does this qualify as P0? There is no experiment enabled for this feature, only users who manually enable it in chrome://flags would run into this.
- Elly, do we intend to launch kShareMenu at all? If we'll just delete the code, we probably don't need to bother here.

### vi...@google.com (2022-02-22)

yelizaveta@ please assign back after confirming the priority https://crbug.com/chromium/1298015#c7

### el...@chromium.org (2022-02-22)

#7: ShareMenu itself is disabled (cl/419920971) and we have no plans to ship it currently; the code could indeed be removed.

I concur that this should not be considered a Pri-0 bug, but we could call it Pri-1 and expedite removing the ShareMenu code.

[Monorail components: UI>Browser>Sharing]

### ye...@google.com (2022-02-22)

Changing it to Pri-0 sgtm. I'll set the severity as High as well given the extra work required for users, and the fact that ShareMenu is disabled.

### ye...@google.com (2022-02-23)

Meant to say changing it to Pri-1, not Pri-0

### vi...@google.com (2022-02-23)

Thanks both. If this is just about removing the flag code now, I'll leave it up to Elly who knows the implementation better.

### vi...@google.com (2022-02-23)

On second thought, let me clean this up given my CL is probably the culprit.
crrev.com/c/3484116

### ad...@google.com (2022-02-23)

As this is behind a flag which is not enabled for any proportion of our users, this counts as Security_Impact-None.

### gi...@appspot.gserviceaccount.com (2022-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4265ea715910b909db81fad760a15508b0db2fd

commit d4265ea715910b909db81fad760a15508b0db2fd
Author: Victor Hugo Vianna Silva <victorvianna@google.com>
Date: Wed Feb 23 16:51:46 2022

Delete kShareMenu feature code

This won't be launched anytime soon, let's delete the code.
The feature was disabled by default, no behavior changes.

Fixed: 1298015
Change-Id: I5488ae1c503f616be578385658c8b229e8da8c0f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3484116
Auto-Submit: Victor Vianna <victorvianna@google.com>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#974218}

[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/flag_descriptions.cc
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/ui/views/omnibox/omnibox_view_views.h
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/about_flags.cc
[delete] https://crrev.com/23529364bdaf86970114e07263c806940e1222b4/chrome/browser/share/share_submenu_model.cc
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/flag_descriptions.h
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/flag-metadata.json
[delete] https://crrev.com/23529364bdaf86970114e07263c806940e1222b4/chrome/browser/share/share_submenu_model.h
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/renderer_context_menu/render_view_context_menu.h
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/tools/metrics/actions/actions.xml
[delete] https://crrev.com/23529364bdaf86970114e07263c806940e1222b4/chrome/browser/share/share_submenu_model_unittest.cc
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/test/BUILD.gn
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/share/share_metrics.h
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/BUILD.gn
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/d4265ea715910b909db81fad760a15508b0db2fd/chrome/browser/ui/views/omnibox/omnibox_view_views.cc


### [Deleted User] (2022-02-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-03)

Congratulations - the VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-06-01)

This issue was migrated from crbug.com/chromium/1298015?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Browser>Sharing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058794)*
