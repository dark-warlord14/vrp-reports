# Security: remote code execution attack chain

| Field | Value |
|-------|-------|
| **Issue ID** | [40092560](https://issues.chromium.org/issues/40092560) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>PlatformIntegration |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-09-26 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: chrome 70 beta / 69 stable  

Operating System: windows7

Ignore Sandbox , Ignore Applock , Ignore download restriction , so funny :)

combined 3 bugs into logical vulnerability attack chain

1. url spoof  
   
   popup on sites.google.com , the popup did not show the real origin which open it
2. download safe.txt , bypass the check.
3. user click the button , here comes the calc.exe.

online demo : <https://sites.google.com/view/userslogin>

reproduce see rce.mp4

when try to reproduce it by yourself

visit <http://f.3cm.me/r/chrome_rce.html> and edit username variable to yourself

as we know python is usually installed like java , but only it did not check the extension , ".py" is blocked by the downloader

I also found attack chain by windows itself using file format vulnerability (do not need to install anything) , but I reported it to microsoft , I think it's the right place , when it was fixed by microsoft , then it would be fixed in chrome.

## Attachments

- [rce.mp4](attachments/rce.mp4) (video/mp4, 828.1 KB)

## Timeline

### ke...@chromium.org (2018-09-26)

Interesting report, thanks. The main problem here seems to be that we allow ProgIDs to be launched as external protocol handlers on Windows, and that is pretty scary on its own.

Adding some people who might have thoughts on how to prevent that.

### sh...@chromium.org (2018-09-27)

[Empty comment from Monorail migration]

### ma...@gmail.com (2018-09-29)

confirm it would also affect popular application like java with default installation config. (which use jarfile: in regedit,  and do not check extension so bypassed the download check , also bypass the sandbox) 

### aw...@google.com (2018-10-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-01)

The reason for allowing ProgIDs is that the difference between a ProgID and a custom protocol is small, from Windows's point of view. Both are registered under HKEY_CLASSES_ROOT\<string>\, but custom protocols have an extra "URL Protocol" key with an empty string.

So when we are launching an external protocol, we ought to make sure if the protocol is a valid one by checking a "URL Protocol" key exists under the registered class.

I tested this on Windows by creating a .url file pointing to an iTunes link in Windows Explorer:

[InternetShortcut]
URL=itmss://itunes.apple.com/deeplink?app=music&p=subscribe&ign-refClientId=3z1mamAFz6MRz4XczD3ozBJwRKWNQ
IDList=
HotKey=0
[{000214A0-0000-0000-C000-000000000046}]
Prop3=19,0

When iTunes is installed, this shortcut works properly. But when I remove HKEY_CLASSES_ROOT\itmss\"URL Protocol" key, Explorer complains with "Unable to open this Internet Shortcut. The protocol itmss does not have a registered program."

So this would be my suggested fix. But as a quick bandaid, we can also add python.file and jarfile to the denided schemes: https://cs.chromium.org/chromium/src/chrome/browser/external_protocol/external_protocol_handler.cc?rcl=5e3bf2a1f618d292d253ee5b0236fcd2cb909c50&l=36


[Monorail components: Internals>PlatformIntegration]

### pa...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-02)

Tentative patch: https://chromium-review.googlesource.com/c/chromium/src/+/1256208

This also affects Windows 10, by the way.

### me...@chromium.org (2018-10-02)

nasko, wfh: As Windows experts, would you be able to take a look at https://crbug.com/chromium/889459#c5 and see if the fix makes sense to you?  

### me...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### wf...@chromium.org (2018-10-02)

the fix in #5 seems reasonable, but I don't know if it might break behavior people are relying on...?

### me...@chromium.org (2018-10-02)

Probably will, but there is a workaround (adding the relevant registry key) so I'm not overly concerned about breakage.

### me...@chromium.org (2018-10-02)

+grt for bug visibility

### ma...@gmail.com (2018-10-08)

sorry , the online demo URL changed to http://1vpctucm.3cm.me/chrome_rce.html
if you want to check the patch is effective or not, visit it please.

### bu...@chromium.org (2018-10-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d19a75fc26fd0ab1ce79ef3d1c1c9b3cc1fbd098

commit d19a75fc26fd0ab1ce79ef3d1c1c9b3cc1fbd098
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Mon Oct 08 18:15:14 2018

Validate external protocols before launching on Windows

Bug: 889459
Change-Id: Id33ca6444bff1e6dd71b6000823cf6fec09746ef
Reviewed-on: https://chromium-review.googlesource.com/c/1256208
Reviewed-by: Greg Thompson <grt@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#597611}
[modify] https://crrev.com/d19a75fc26fd0ab1ce79ef3d1c1c9b3cc1fbd098/chrome/browser/shell_integration_win.cc


### me...@chromium.org (2018-10-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-17)

[Comment Deleted]

### aw...@google.com (2018-10-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-22)

Hi ma7h1as.l@ - thanks for the report! The VRP Panel decided that this bug should be tracked as medium severity, and awarded $1,000 - cheers!

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### ma...@gmail.com (2018-10-22)

[Comment Deleted]

### ma...@gmail.com (2018-10-22)

[Comment Deleted]

### ma...@gmail.com (2018-11-05)

[Comment Deleted]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/889459?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092560)*
