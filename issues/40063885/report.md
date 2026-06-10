# Security: Very long extension name spoofs debugging infobar and breaks other UI

| Field | Value |
|-------|-------|
| **Issue ID** | [40063885](https://issues.chromium.org/issues/40063885) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Privacy and Security, Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | ab...@microsoft.com |
| **Created** | 2023-04-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

By giving an extension a really long name it is possible to spoof and break various UI.

When an extension starts debugging the browser, a message is shown that states "x is debugging this browser". By using a long extension name it is possible to spoof this message to say anything. This was reported and fixed in <https://crbug.com/chromium/823194>, but the fix can be bypassed by using an even longer extension name.

Even with no permissions, a long name causes issues in other parts of the UI. For example the uninstall prompt becomes too tall and the buttons to confirm an uninstall are no longer visible (the enter key can still be used), the extensions page takes a very long time to load, and the extension details page is covered by the extension name.

On a sidenote, this extension shows up on websites as "No access needed" even though it has the debugger permission.

**VERSION**  

Chrome Version: 113.0.5672.12 Stable + Dev  

Operating System: Windows 10

**REPRODUCTION CASE**  

Download the "manifest.js" and "background.js" files into a folder and load the folder as an unpacked extension.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jasper Rebane (popstonia)

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 2.9 MB)
- [background.js](attachments/background.js) (text/plain, 154 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.6 MB)
- [prompt.png](attachments/prompt.png) (image/png, 8.0 KB)
- [permissions_ext.png](attachments/permissions_ext.png) (image/png, 41.0 KB)
- [permissions_web.png](attachments/permissions_web.png) (image/png, 12.4 KB)
- [Screenshot 2024-11-29 111254.png](attachments/Screenshot 2024-11-29 111254.png) (image/png, 136.3 KB)
- [Screenshot 2024-11-29 111806.png](attachments/Screenshot 2024-11-29 111806.png) (image/png, 65.6 KB)
- [Screenshot 2024-11-29 122051.png](attachments/Screenshot 2024-11-29 122051.png) (image/png, 139.3 KB)
- [Screenshot 2024-11-29 122422.png](attachments/Screenshot 2024-11-29 122422.png) (image/png, 69.0 KB)
- [Screenshot 2024-11-29 152549.png](attachments/Screenshot 2024-11-29 152549.png) (image/png, 109.4 KB)

## Timeline

### [Deleted User] (2023-04-03)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-04-04)

caseq@ for the DevTools bar and tjudkins@ for the chrome://extensions funniness.

[Monorail components: Platform>DevTools>Security Platform>Extensions]

### [Deleted User] (2023-04-04)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-04)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tj...@chromium.org (2023-04-04)

That's a good one, we should likely be using overflows here like we do in other places. Copying on emiliapaz@ who has been doing a lot of work on extensions UI.

### tj...@chromium.org (2023-04-04)

lottie@: Do you know if there are any checks for limits on extension name length on the CWS side?

### ds...@chromium.org (2023-04-05)

I have a pending crrev.com/c/4396057 fixing this. The issue is that we truncate the text at 10000 before running doing any elision. 

### re...@gmail.com (2023-04-05)

I played around with the extension a bit more and found that alerts/prompts have a similar truncation issue as the infobar, which could be used for convincing phishing w/o permissions.

### gi...@appspot.gserviceaccount.com (2023-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/747b128e67a02dde483589c90f78b36b8f52735c

commit 747b128e67a02dde483589c90f78b36b8f52735c
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Apr 07 00:03:03 2023

[Extensions] Truncate extension name in infobar delegate

This is to avoid the text being truncated by the rendering routine before the elision occurs.

Bug: 1430269
Change-Id: Ib75d6a2f95e470c1a04887fc94d0f07e8746f9c7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4396057
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1127461}

[modify] https://crrev.com/747b128e67a02dde483589c90f78b36b8f52735c/chrome/browser/extensions/api/debugger/extension_dev_tools_infobar_delegate.cc


### re...@gmail.com (2023-04-09)

I found that both of the permissions prompts (web and extension) are also affected. One can be used to gain access to web features (eg webcam) and the other to escalate privileges through the chrome.permissions API.

### ds...@chromium.org (2023-04-11)

The DevTools infobar is fixed. Anyone else interested in looking at the other prompts?

### ds...@chromium.org (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-20)

Thank you for the report, Jasper. The VRP Panel would like to extend a $500 thank you reward for this report. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-21)

This issue was migrated from crbug.com/chromium/1430269?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools>Security, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

### ab...@microsoft.com (2024-07-01)

Re-opened this Issue and assigned it to myself to fix other UI surfaces breaking due to long extension names.

### ab...@microsoft.com (2024-07-03)

Proposal doc : https://docs.google.com/document/d/1zjJ2Y9Oc-nO2xnvvrsABd8ZLzLgq8U43DVM7n04QQE4/edit?usp=sharing

@rd...@chromium.org, @em...@chromium.org : Seeking feedback and review on this.

### ap...@google.com (2024-07-16)

Project: chromium/src
Branch: main

commit 5fd543ed189e76568e5310e2aa67595133eefaee
Author: Abhinav Kumar <abhinakumar@microsoft.com>
Date:   Tue Jul 16 05:27:14 2024

    [Extensions] Fix for UI surfaces breaking due to Very Long Extension Name
    
    Added utility method GetFixupExtensionNameForUIDisplay() which fixes very long
    extension name for UI display in various dialogs, prompts, infobars & pop-ups
    by truncating the long extension name to first 75 chars (with ellipsis "..."
    appended at the end).
    
    Bug: 40063885
    Change-Id: Ib1b5e5c60cf38c82012d1832d4acc0663e0510a6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5687014
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
    Commit-Queue: Abhinav Kumar <abhinakumar@microsoft.com>
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1327961}

M       chrome/browser/extensions/extension_install_prompt.cc
M       chrome/browser/extensions/extension_util.cc
M       chrome/browser/extensions/extension_util.h
M       chrome/browser/extensions/extension_util_unittest.cc

https://chromium-review.googlesource.com/5687014


### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: main

commit a7c9652135f9200c107ac0af06bdd6e29997c555
Author: Abhinav Kumar <abhinakumar@microsoft.com>
Date:   Tue Jul 30 10:15:57 2024

    [Extensions] Fix UI breaking due to Long Extension Name (Part-2)
    
    Used the utility method GetFixupExtensionNameForUIDisplay() to fix
    issues due to very long extension name in install & uninstall UI
    surfaces. UI display of following message IDs have been fixed to prevent
    message spoofing & UI break :
    
    1. IDS_EXTENSION_INSTALLED_HEADING : Title of the extension-installed
       bubble. Instructs that the extension was installed.
    2. IDS_EXTENSION_EXTERNAL_INSTALL_ALERT_BUBBLE_TITLE : The title for the
       bubble that alerts the user that a new external extension was
       installed.
    3. IDS_EXTENSION_PROMPT_UNINSTALL_TITLE : Title text for removing an
       extension.
    4. IDS_EXTENSION_PROMPT_UNINSTALL_TRIGGERED_BY_EXTENSION : Text in
       uninstall-extension dialog that indicates the uninstall was triggered
       by another extension (the name of the extension being uninstalled is
       already present in the dialog title).
    5. IDS_EXTENSION_PROMPT_UNINSTALL_REPORT_ABUSE_FROM_EXTENSION : Label
       for a checkbox the user can tick to report abuse for the extension
       being uninstalled.
    
    Part-1 of the CL to fix other UI surfaces :
    5687014: [Extensions] Fix for UI surfaces breaking due to Very Long Extension Name | https://chromium-review.googlesource.com/c/chromium/src/+/5687014
    
    Before/After screenshots of UI surfaces fixed :
    https://docs.google.com/document/d/1mwGSK3tacnvs9OFVZVuu3CNG3yuEQVc4FN8mU4PhYGM/edit?usp=sharing
    
    Bug: 40063885
    Change-Id: I2ca756964057dc9c9660d1b6a86b8982161df39d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5737853
    Commit-Queue: Abhinav Kumar <abhinakumar@microsoft.com>
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1334730}

M       chrome/browser/extensions/external_install_error.cc
M       chrome/browser/ui/views/extensions/extension_installed_bubble_view.cc
M       chrome/browser/ui/views/extensions/extension_uninstall_dialog_view.cc

https://chromium-review.googlesource.com/5737853


### ap...@google.com (2024-09-14)

Project: chromium/src
Branch: main

commit 193c47b7a1311be79a169e942c0d4043597b4c45
Author: Sohail Rajdev <sorajdev@microsoft.com>
Date:   Sat Sep 14 03:23:27 2024

    Extensions: Truncate long extension name in ExtensionErrorUIDefault
    
    This CL truncates unusually long extension names in the dialog which
    is displayed when extensions are turned off by enterprise policy or
    when they are detected as a malware.
    
    Before: https://ibb.co/VD8yzzW
    
    After: https://ibb.co/FW9tw2z
    
    Bug: 40063885
    Change-Id: Ie98c854028fa718d6053638711a7d6893b3de4e5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5861696
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
    Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com>
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1355542}

M       chrome/browser/extensions/extension_error_ui_default.cc
M       chrome/browser/extensions/extension_error_ui_default_unittest.cc

https://chromium-review.googlesource.com/5861696


### ap...@google.com (2024-10-11)

Project: chromium/src  

Branch: main  

Author: Abhinav Kumar <[abhinakumar@microsoft.com](mailto:abhinakumar@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/5921098>

[Extensions] Fix UI breaking due to Long Extension Name (Part-3)

---


Expand for full commit details
```
[Extensions] Fix UI breaking due to Long Extension Name (Part-3)

Used the utility method GetFixupExtensionNameForUIDisplay() to fix
issues due to very long extension name in: (i) dialog for extension
blocked due to policy, and (ii) Infobar for extension blocked due to
malware. UI display of following message IDs have been fixed to prevent message spoofing & UI break :
1. IDS_EXTENSION_BLOCKED_BY_POLICY_PROMPT_TITLE : Title of the
   extension or app install blocked prompt. Tells the user they can't
   install this extension as it's blocked by policy.
2. IDS_EXTENSION_IS_BLOCKLISTED : Text displayed in an infobar when an
   extension is blocklisted and prevented from being installed.

Part-2 of the CL to fix other UI surfaces :
5737853: [Extensions] Fix UI breaking due to Long Extension Name (Part-2) | https://chromium-review.googlesource.com/c/chromium/src/+/5737853

Before/After screenshots of UI surfaces fixed :
https://docs.google.com/document/d/1mwGSK3tacnvs9OFVZVuu3CNG3yuEQVc4FN8mU4PhYGM/edit?usp=sharing

Bug: 40063885
Change-Id: Iced0f18deedb5b75cd70671efb27c7c194d2a152
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5921098
Reviewed-by: Emilia Paz <emiliapaz@chromium.org>
Reviewed-by: Tim <tjudkins@chromium.org>
Commit-Queue: Abhinav Kumar <abhinakumar@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#1367368}

```

---

Files:

- M `chrome/browser/extensions/crx_installer.cc`
- M `chrome/browser/ui/views/extensions/extension_install_blocked_dialog_view.cc`

---

Hash: 04ed670039e2f6319456c955f384d859f0b2a93c  

Date:  Fri Oct 11 09:10:12 2024


---

### ap...@google.com (2024-10-16)

Project: chromium/src  

Branch: main  

Author: EmiliaPaz <[emiliapaz@chromium.org](mailto:emiliapaz@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5938112>

[Extensions c2s] Truncate extension name in reload page dialog

---


Expand for full commit details
```
[Extensions c2s] Truncate extension name in reload page dialog

Used the utility method GetFixupExtensionNameForUIDisplay() to truncate
very long extension names in reload page dialog.

Screenshot:
https://drive.google.com/file/d/1Z5ys8Vv957FFwTwWRmk-gf18OdxJPSFi/view?usp=sharing

Bug: 373759993, 40063885
Change-Id: Ide7ed30e9e5bfd0b74712737458a81b17756bc6d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5938112
Reviewed-by: Oliver Dunk <oliverdunk@chromium.org>
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1369600}

```

---

Files:

- M `chrome/browser/extensions/extension_util.cc`
- M `chrome/browser/extensions/extension_util.h`
- M `chrome/browser/ui/views/extensions/dialogs/reload_page_dialog.cc`

---

Hash: e9f567b38a25e9fb00c21d12849299964003e0e6  

Date:  Wed Oct 16 20:22:51 2024


---

### ap...@google.com (2024-11-20)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6038094>

Extensions: Truncate long extension names in web auth infobar

---


Expand for full commit details
```
Extensions: Truncate long extension names in web auth infobar 
 
This change truncates long extension names shown in the infobar which 
is displayed on windows created via chrome.identity.launchWebAuthFlow() 
 
Before: https://ibb.co/mzsG8t6 
After: https://ibb.co/kQnvHjx 
 
Bug: 40063885 
Change-Id: Id7900f863c24cdbfe6874b664e059826e8a1fbf4 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6038094 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Alex Ilin <alexilin@chromium.org> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1385800}

```

---

Files:

- M `chrome/browser/extensions/api/identity/web_auth_flow_info_bar_delegate.cc`
- M `chrome/browser/extensions/api/identity/web_auth_flow_info_bar_delegate.h`
- A `chrome/browser/extensions/api/identity/web_auth_flow_info_bar_delegate_unittest.cc`
- M `chrome/test/BUILD.gn`

---

Hash: c03c6e44d285f1da0dff5f188c347c85d5318e07  

Date:  Wed Nov 20 19:14:39 2024


---

### ap...@google.com (2024-11-20)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6035908>

Truncate long extension names in ExtensionDisabledGlobalError

---


Expand for full commit details
```
Truncate long extension names in ExtensionDisabledGlobalError 
 
This change truncates long extension names in the Global Error which is 
seen when an extension is disabled due to DISABLE_REMOTE_INSTALL or 
DISABLE_PERMISSIONS_INCREASE reason. 
 
Before 
- https://ibb.co/SfwM430 
- https://ibb.co/pyX9Tk6 
 
After 
- https://ibb.co/sF9xmFm 
- https://ibb.co/n0yMW3F 
 
Bug: 40063885 
Change-Id: I2aee8f05da7e3c2bce71fed5c97e819a690fadbf 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6035908 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Reviewed-by: Peter Kasting <pkasting@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1385854}

```

---

Files:

- M `chrome/browser/extensions/extension_disabled_ui.cc`
- M `chrome/browser/ui/global_error/global_error_browsertest.cc`

---

Hash: 6e1069d8fa67ec77653a656e5d6d8b4f5945cf37  

Date:  Wed Nov 20 20:18:21 2024


---

### ap...@google.com (2024-11-21)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6042077>

Extensions: Truncate long extension names in MV2 deprecation dialog

---


Expand for full commit details
```
Extensions: Truncate long extension names in MV2 deprecation dialog 
 
This change truncates long extension names present in the dialog 
displayed when Manifest V2 extensions are automatically disabled by the 
browser. 
 
Before: https://ibb.co/m9K3Cmq 
After: https://ibb.co/PzjzS0Z 
 
Bug: 40063885 
Change-Id: I6f00cbb3cc237e6446385851619d59d95eb1e6f5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6042077 
Reviewed-by: Darryl James <dljames@chromium.org> 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1386347}

```

---

Files:

- M `chrome/browser/ui/views/extensions/dialogs/mv2_deprecation_disabled_dialog.cc`

---

Hash: 0fdab01fe4b502278682008c867e5cc0665e1a1c  

Date:  Thu Nov 21 18:46:57 2024


---

### ap...@google.com (2024-11-23)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6043718>

Extensions: Truncate extension names in Manifest V2 deprecation dialogs

---


Expand for full commit details
```
Extensions: Truncate extension names in Manifest V2 deprecation dialogs 
 
This change truncates long extension names in the dialogs which appear 
when: 
 
1. The user dismisses the Manifest V2 deprecation warning on the 
extensions WebUI page. 
 
2. User tries to re-enable a Manifest V2 extension which was disabled 
by the browser as a part of the deprecation. 
 
Before: 
- https://ibb.co/XX6Rc4D 
- https://ibb.co/mz0BLkz 
 
After: 
- https://ibb.co/QpYcFQ6 
- https://ibb.co/R0sLYFr 
 
Bug: 40063885 
Change-Id: Ib3880e1f24fe82e5c3ec0b1209cd81f76d3e839c 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6043718 
Reviewed-by: Darryl James <dljames@chromium.org> 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1387216}

```

---

Files:

- M `chrome/browser/ui/views/extensions/dialogs/mv2_deprecation_keep_dialog.cc`
- M `chrome/browser/ui/views/extensions/dialogs/mv2_deprecation_keep_dialog_browsertest.cc`
- M `chrome/browser/ui/views/extensions/dialogs/mv2_deprecation_reenable_dialog.cc`
- M `chrome/browser/ui/views/extensions/dialogs/mv2_deprecation_reenable_dialog_browsertest.cc`
- M `testing/buildbot/filters/pixel_tests.filter`

---

Hash: a165f3f363604d0e01cb403869329a015933ae6f  

Date:  Sat Nov 23 04:22:29 2024


---

### ap...@google.com (2024-11-27)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6049394>

Truncate long extension names in Controlled Homepage bubble

---


Expand for full commit details
```
Truncate long extension names in Controlled Homepage bubble 
 
This change truncates long extension names in the "Controlled Home 
Page" bubble. This bubble is shown when the user sees an extension 
overridden homepage for the first time. The extension name is only shown 
when the bubble is not anchored to a browser action (this happens for 
default installed extensions with no popup page). 
 
Long names can break the UI (e.g. other UI elements can go out of the 
screen). In the worst case, it can trick the user into doing something 
unintentional. Thus, we truncate the extension name before displaying 
it. 
 
Before: https://ibb.co/P607n3D 
After: https://ibb.co/sW2VLGD 
 
Bug: 40063885 
Change-Id: Iae33a03fc84f2f2c66586ea9de646fab6f6f9742 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6049394 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Reviewed-by: Darryl James <dljames@chromium.org> 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Cr-Commit-Position: refs/heads/main@{#1388627}

```

---

Files:

- M `chrome/browser/ui/extensions/controlled_home_bubble_delegate.cc`
- M `chrome/browser/ui/extensions/controlled_home_bubble_delegate_unittest.cc`

---

Hash: f93a2e202f6d7d993d2a59c1899241ceb1d7954f  

Date:  Wed Nov 27 04:46:16 2024


---

### ap...@google.com (2024-11-27)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6050384>

Truncate long extension names in the Chrome Sign-in Dialog

---


Expand for full commit details
```
Truncate long extension names in the Chrome Sign-in Dialog 
 
This dialog is shown when an extension starts a signin-in flow via the 
chrome.identity API and the user is not signed-in to the browser (but 
signed in on web). 
 
Long names can break the UI (e.g. other UI elements can go out of the 
screen). In the worst case, it can trick the user into doing something 
unintentional. Thus, we truncate the extension name before displaying 
it. 
 
Before: https://ibb.co/S3K7JRf 
After: https://ibb.co/1KT8mCf 
 
Bug: 40063885 
Change-Id: Id076a83f40772b32d2e21ad5f34a872310b57925 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6050384 
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org> 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1388801}

```

---

Files:

- M `chrome/browser/extensions/api/identity/identity_api.cc`
- M `chrome/browser/extensions/api/identity/identity_api.h`
- M `chrome/browser/extensions/api/identity/identity_api_unittest.cc`
- M `chrome/browser/extensions/api/identity/identity_get_auth_token_function.cc`
- M `chrome/browser/ui/signin/signin_view_controller.cc`
- M `chrome/browser/ui/signin/signin_view_controller.h`
- M `chrome/browser/ui/signin/signin_view_controller_browsertest.cc`

---

Hash: fa9734ddf076858aa674a8b265678d1941402edd  

Date:  Wed Nov 27 14:21:33 2024


---

### ap...@google.com (2024-11-27)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6052152>

Truncate long extension names in Parent Permission dialog

---


Expand for full commit details
```
Truncate long extension names in Parent Permission dialog 
 
This change truncates the extension names in the dialog which asks the 
user to seek parent's permission when installing a restricted extension. 
 
Long names can break the UI (e.g. other UI elements can go out of the 
screen). In the worst case, it can trick the user into doing something 
unintentional. Thus, we truncate the extension name before displaying 
it. 
 
Before: https://ibb.co/tKLPrK8 
After: https://ibb.co/52sZYSw 
 
Bug: 40063885 
Change-Id: I19464a581a5512f470bac989ca0804c6de18dcb5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6052152 
Reviewed-by: Peter Kasting <pkasting@chromium.org> 
Reviewed-by: Darryl James <dljames@chromium.org> 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Cr-Commit-Position: refs/heads/main@{#1388977}

```

---

Files:

- M `chrome/browser/ui/views/supervised_user/parent_permission_dialog_view.cc`
- M `chrome/browser/ui/views/supervised_user/parent_permission_dialog_view_browsertest.cc`
- M `testing/buildbot/filters/pixel_tests.filter`

---

Hash: d1391927f5dda4c113361bd8df4c89c17b1f3c4d  

Date:  Wed Nov 27 19:08:21 2024


---

### ap...@google.com (2024-11-28)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6054657>

Truncate long extension names in settings overridden dialog

---


Expand for full commit details
```
Truncate long extension names in settings overridden dialog 
 
This CL truncates long extension names when they are displayed on the 
settings overridden dialog. This dialog is shown when extensions 
override the new tab page or the browser search engine for the first 
time. 
 
Long names can break the UI (e.g. other UI elements can go out of the 
screen). In the worst case, it can trick the user into doing something 
unintentional. Thus, we truncate the extension name before displaying 
it. 
 
Before: 
- https://ibb.co/p3TKw1m 
- https://ibb.co/QFVdKYX 
 
After: 
- https://ibb.co/CW6WJkZ 
- https://ibb.co/stGWb4f 
 
Bug: 40063885 
Change-Id: I2ba42e2bcc6d1a7bc88ea5e8f2e7940a1e5bd87d 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6054657 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org> 
Reviewed-by: Darryl James <dljames@chromium.org> 
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1389368}

```

---

Files:

- M `chrome/browser/ui/extensions/settings_overridden_params_providers.cc`
- M `chrome/browser/ui/extensions/settings_overridden_params_providers_browsertest.cc`
- M `chrome/browser/ui/extensions/settings_overridden_params_providers_unittest.cc`
- M `chrome/test/data/extensions/search_provider_override/manifest.json`
- A `chrome/test/data/extensions/search_provider_override_2/_locales/en/messages.json`
- A `chrome/test/data/extensions/search_provider_override_2/manifest.json`
- A `chrome/test/data/extensions/search_provider_override_long_name/_locales/en/messages.json`
- A `chrome/test/data/extensions/search_provider_override_long_name/manifest.json`

---

Hash: 393528593491d6b1dab465f31f084d864ec4bd10  

Date:  Thu Nov 28 13:40:31 2024


---

### ap...@google.com (2024-12-02)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6059069>

Truncate long extension names in Chrome Apps deprecation dialogs

---


Expand for full commit details
```
Truncate long extension names in Chrome Apps deprecation dialogs 
 
This change truncates long extension names which are shown in the Chrome 
Apps deprecation dialogs. These dialogs are shown when the user tries to 
interact with Chrome Apps, which are now deprecated. 
 
Long names can break the UI (e.g. other UI elements can go out of the 
screen). In the worst case, it can trick the user into doing something 
unintentional. Thus, we truncate the extension name before displaying 
it. 
 
Before: 
- https://issues.chromium.org/40063885#attachment61175849 
- https://issues.chromium.org/40063885#attachment61175850 
 
After: 
- https://issues.chromium.org/40063885#attachment61178629 
- https://issues.chromium.org/40063885#attachment61175851 
 
Bug: 40063885 
Change-Id: If85f56bedf1ef95af7784e3bf812348fabf4bc02 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6059069 
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
Reviewed-by: Peter Kasting <pkasting@chromium.org> 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Cr-Commit-Position: refs/heads/main@{#1390427}

```

---

Files:

- M `chrome/browser/ui/views/web_apps/deprecated_apps_dialog_view.cc`
- M `chrome/browser/ui/views/web_apps/force_installed_deprecated_apps_dialog_view.cc`
- M `chrome/browser/ui/views/web_apps/force_installed_deprecated_apps_dialog_view.h`

---

Hash: 61d6ad012e01981bbaef18f85f133bb3bd2a290b  

Date:  Mon Dec 02 17:37:18 2024


---

### ap...@google.com (2024-12-06)

Project: chromium/src  

Branch: main  

Author: Sohail Rajdev <[sorajdev@microsoft.com](mailto:sorajdev@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6053866>

Truncate long extension names in Open Download Confirmation dialog

---


Expand for full commit details
```
Truncate long extension names in Open Download Confirmation dialog 
 
This change truncates long extension names in the confirmation dialog 
which is shown when an extension tries to open a downloaded file 
via the `chrome.downloads.open` API. 
 
Long names can break the UI (e.g. other UI elements can go out of the 
screen). In the worst case, it can trick the user into doing something 
unintentional. Thus, we truncate the extension name before displaying 
it. 
 
Before: https://ibb.co/N1QSm7C 
After: https://ibb.co/7gJ5M8m 
 
Bug: 40063885 
Change-Id: Ie3d0657d2adbaeb89894dfd57bff780f608ed178 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6053866 
Commit-Queue: Sohail Rajdev <sorajdev@microsoft.com> 
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org> 
Reviewed-by: Min Qin <qinmin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1393015}

```

---

Files:

- M `chrome/browser/download/download_open_prompt.cc`
- M `chrome/browser/download/download_open_prompt.h`
- M `chrome/browser/extensions/api/downloads/downloads_api.cc`

---

Hash: c77ca4571e9777a812d711cb7ca548215c34cdd7  

Date:  Fri Dec 06 18:17:07 2024


---

### bo...@gmail.com (2025-03-03)

deleted

### aj...@google.com (2025-04-28)

[Bulk edit comment]

Issue Status is - In Progress(Accepted) hence removing the Unconfirmed hotlist from this issue.

### dj...@gmail.com (2025-10-16)

Hi , can you review that report > <https://issuetracker.google.com/issues/451297405>

### el...@chromium.org (2026-02-24)

Security shepherd: I see a lot of fix CLs and no further traffic. Is this one fixed? :)

### em...@chromium.org (2026-02-24)

[`GetFixupExtensionNameForUIDisplay()`](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/ui_util.h;l=22-28?q=GetFixupExtensionNameForUIDisplay&ss=chromium) was introduced to provide the extension name to be used in UI, to prevent extension name spoofs.

I think we can call this fixed, as most of the surfaces have been updated

### pe...@google.com (2026-03-03)

The NextAction date has arrived: 2026-03-03
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### df...@google.com (2026-05-12)

Reopening due to [issue 505481691](https://issues.chromium.org/issues/505481691)

> After Fixed <https://issues.chromium.org/issues/40063885> , my last report on <https://issues.chromium.org/issues/477452354> (duplicate of 40063885) cannot be reproduced . but on versiojn 149.0.7807.0 it can be reproduced (bisect)
> 
> when the extension name is added many spaces this will make the end part invisible thus causing spoof, normally when added many spaces in the name chrome space will replace many spaces into just one space while when using spaces on <https://emojidb.org/space-emojis>, the spaces are not cut into one. this bug is almost similar to: <https://issues.chromium.org/issues/40063885> but on <https://issues.chromium.org/issues/40063885> this occurs because of the break character. while in this bug it is not visible because of many spaces
> 
> VERSION
> Chrome Version: 149.0.7807.0 (Official Build) canary (64-bit)
> Operating System: Windows 11
> 
> REPRODUCTION CASE
> 
> 1. Go to <https://emojidb.org/space-emojis>
> 2. choose space then click
> 3. download manifest.json and background.js in same folder
> 4. open manifest.json then paste in "name": "<https://google.com>" , do many paste before <https://google.com> then save it.
> 5. load the extension, it will shown as blank name of extension
> 6. it will open google.com with notification debugger: " <https://google.com>" started debugging this browser.

See attached files on other issues for PoC and screen recording

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063885)*
