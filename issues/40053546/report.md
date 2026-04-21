# Security: Spoofing download filename extension in 86 chrome - showSaveFilePicker

| Field | Value |
|-------|-------|
| **Issue ID** | [40053546](https://issues.chromium.org/issues/40053546) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2020-10-11 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: [86.0.4240.75] + [stable]  

Operating System: [Windows 10 OS Version 1903 (Build 18362.1082)]

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

Full Example: <https://nfz.dev/imageTest2.html>  

Gif Example: <https://nfz.dev/saveExample1.gif>  

I can delete examples if you want.

Files:  

imageTest2.html - code example + solution + explanation  

explanation.png - explanation

## Attachments

- [explanation.png](attachments/explanation.png) (image/png, 41.7 KB)
- [imageTest2.html](attachments/imageTest2.html) (text/plain, 2.2 KB)
- [picture1.png](attachments/picture1.png) (image/png, 38.1 KB)
- [picture2.png](attachments/picture2.png) (image/png, 29.3 KB)
- [picture3.png](attachments/picture3.png) (image/png, 25.3 KB)
- [rtltrick.gif](attachments/rtltrick.gif) (image/gif, 9.2 MB)
- [RTLExplanation.png](attachments/RTLExplanation.png) (image/png, 52.1 KB)
- [downloadExeAsJpeg.html](attachments/downloadExeAsJpeg.html) (text/plain, 2.0 KB)
- [picture7.png](attachments/picture7.png) (image/png, 88.2 KB)
- [picture10.png](attachments/picture10.png) (image/png, 4.0 KB)
- [picture11.png](attachments/picture11.png) (image/png, 3.2 KB)
- [picture12.png](attachments/picture12.png) (image/png, 2.9 KB)
- [lnk2.gif](attachments/lnk2.gif) (image/gif, 18.2 MB)
- [lnk.html](attachments/lnk.html) (text/plain, 4.6 KB)
- [picture20.png](attachments/picture20.png) (image/png, 38.5 KB)
- [picture21.png](attachments/picture21.png) (image/png, 24.0 KB)
- [picture30.png](attachments/picture30.png) (image/png, 73.1 KB)
- [picture31.png](attachments/picture31.png) (image/png, 31.3 KB)
- [spaceEnd.html](attachments/spaceEnd.html) (text/plain, 2.2 KB)
- [picture40.png](attachments/picture40.png) (image/png, 53.1 KB)
- [pic1.png](attachments/pic1.png) (image/png, 198.6 KB)
- [vid2.mp4](attachments/vid2.mp4) (video/mp4, 20.9 MB)

## Timeline

### me...@chromium.org (2020-10-12)

Thank you for the report. Triaging this as high severity even though this requires some user interaction.

mek: Can you PTAL?

[Monorail components: Blink>Storage>FileSystem]

### me...@chromium.org (2020-10-12)

(Correcting the severity)

### [Deleted User] (2020-10-12)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2020-10-13)

Another bug is that we can add more than one (dot) in accept extension: ['.jpg.bat']. but why?
It allows the website developer to add characters to the filename. If a user has hidden file extensions (default option on Windows) He will see more legit virus filename (picture1)
Solution: Only one dot in accept extension.

### ma...@gmail.com (2020-10-13)

In documentation there is:

https://wicg.github.io/file-system-access/#security-malware

"This API could be used by websites to try to store and/or execute malware on the users system.
To mitigate this risk, this API does not provide any way to mark files as executable
(on the other hand files that are already executable likely remain that way, even after the files are modified through this API)"

"not provide any way to mark files as executable" - I can save executable .bat and spoof as an .jpg. I can mark it to save as .bat??? So it is not working as planned.
I am a bit confused here. :P

### ma...@gmail.com (2020-10-13)

Another bug. If user has option "show all file extensions." activated, we can hide real extension by adding many white chars to accept extension. 
Solution: Accept extension shouldn't allow many white spaces. Should be limited with max chars or array of legit chars excluding white chars. 

### ma...@gmail.com (2020-10-13)

Next security bug. Accept extension allowing to put RTL (right-to-left) character. Extra spoofing extension of file on operation system side.

Full example: https://nfz.dev/downloadExeAsJpeg.html
Gif example: https://nfz.dev/rtltrick.gif

files:
rtltrick.gif - example gif
RTLExplanation.png - How to do it
downloadExeAsJpeg.html - code example




### ma...@gmail.com (2020-10-13)

The last example shows how to download .exe from server instead of .bat from content.

### ma...@gmail.com (2020-10-13)

Example is putty.exe from https://www.putty.org/.
Of course hacker can change icon of exe to jpg icon to increase trust.

### ma...@gmail.com (2020-10-15)

To improve script we can use UserAgent to check if client is exploitable. Example in attachments.


### ma...@gmail.com (2020-10-15)

Now I have understood the mechanism of description variable
description = "JPEG (.jpeg)" then in download window we can see: "JPEG (.jpeg) (*.exe;*.txt;*.text)" (picture10.png) - works good! Chrome is adding real extensions.
However we can bypass this in 2 ways:
1 method: Add extra space to description:
description = "JPEG (.jpeg)                       (50+more white chars)" then in download window we can see: "JPEG (.jpeg)" (picture11.png)
2 method: Add *. to description:
description = "JPEG (*.jpeg)" then in download window we can see: "JPEG (*.jpeg)" (picture12.png)

Solution: Always add real extensions. Block * character and multiple white characters.

### ma...@gmail.com (2020-10-18)

NEXT SECURITY vulnerability:
Based on default/main download function:
showSaveFilePicker bypassing the function "IsShellIntegratedExtension": https://source.chromium.org/chromium/chromium/src/+/master:net/base/filename_util_internal.cc;drc=1c58af32060fa0ef3cfd4037fdc7913092d16ba2;l=155?q=%20EnsureSafeExtension&ss=chromium
if extension ".lnk" or ".local" then Chrome should CHANGE extension to ".download", but not doing this:
https://source.chromium.org/chromium/chromium/src/+/master:net/base/filename_util_internal.cc;drc=1c58af32060fa0ef3cfd4037fdc7913092d16ba2;l=195?q=%20EnsureSafeExtension&ss=chromium
Solution: Replace ".lnk" and ".local" with ".download" or block downloading such a file.

URL EXAMPLE: https://nfz.dev/lnk.html

### ma...@gmail.com (2020-10-19)

The next bug is that we can add extra space at the end of the accept extension and save the file. 
By this trick, the windows user cannot delete file according to: https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file

"Do not end a file or directory name with a space or a period. Although the underlying file system may support such names, the Windows shell and user interface does not. However, it is acceptable to specify a period as the first character of a name. For example, ".temp"."









### me...@chromium.org (2020-10-19)

Would you mind filing separate bugs for separate issues? That will make it easier to track work fixing/triaging them, and make sure they don't fall through the gaps.

Re https://crbug.com/chromium/1137247#c4, supporting dots in extensions (i.e. "compound extensions") is something that we do need to support, as some file types do use that. For example things like .tar.gz. See also https://crbug.com/chromium/1136053 for some related issues to how compound extensions are treated.

One way to solve issues with misleading descriptions would be to completely ignore all descriptions in save dialogs, and only use auto-generated descriptions from the extensions. That wouldn't be great though since there are legit use cases for having multiple options for the same extension only differing in the description (for example chrome's save page as dialog has "Webpage, HTML only" and "Webpage, complete" options that both use the same (.htm) extension). Today that use case isn't supported since the API doesn't expose the selected option, but this still seems like a use case we don't want to preemptively rule out.

So perhaps better is to make sure the file dialog always shows the actual extension(s), regardless of the description shown. Exactly how that is done will probably depend a bit on the individual platform (although we could prepend the extensions to the description for example). There are a lot of differences already in how different platforms implement filters today. I think this will end up being a balance between fitting in with the platform and still giving enough information for users to make informed security decisions.

My plan is to figure out exactly what we're doing today on all the various platforms (and possibly even various settings on those platforms), and then come up with some proposal to run by UX and security.

+pwnall for visibilty
+asully since there is some overlap between this issue and allowing websites to provide a suggested filename as well

### me...@chromium.org (2020-10-19)

Actually +asully and +pwnall

### ma...@gmail.com (2020-10-20)

No problem. Created new issues:
Based on https://crbug.com/chromium/1137247#c6: https://bugs.chromium.org/p/chromium/issues/detail?id=1140403
Based on https://crbug.com/chromium/1137247#c7,8,9: https://bugs.chromium.org/p/chromium/issues/detail?id=1140410
Based on https://crbug.com/chromium/1137247#c12: https://bugs.chromium.org/p/chromium/issues/detail?id=1140417
Based on https://crbug.com/chromium/1137247#c13: https://bugs.chromium.org/p/chromium/issues/detail?id=1140435

Compound extensions - yes I forgot about .tar.gz . Standard download function of Chrome allowing many extensions ".jpg.psd" so maybe it is OK. Nothing can be done here.

In my opinion, Chrome should always add the real extension in the description and preventing from editing extensions part in the description by the developer.

Misleading descriptions - How about creating a whitelist of chars in descriptions? Like "aA-zZ 0-9 , " + maximum 30 length? Because of that, the developer cannot add chars like "( ) . *" But this will block localization/globalization chars from other languages example: ł ó ż ź ć € ä ö ü and more... 

Moreover, Chrome could always add default name like : "file.<accept-extension>" (ex: file.jpg.bat) - By that user always see what kind of file he is downloading.

Keep in mind that Save button is focused by default is better to change it to cancel if possible to avoid attack like: https://bugs.chromium.org/p/chromium/issues/detail?id=637098
Right now user is forced to write a name of file. 


### me...@chromium.org (2020-10-21)

Looking into this one a bit more, you don't actually need any of the spaces to hide the real extension in the windows file dialog. Merely including (*.jpeg) in the description appears to be enough to have the system not include the real extensions. The space trick also works if you want a filter that doesn't show extensions at all.

### ma...@gmail.com (2020-10-21)

Yes, indeed. 

Please, check https://crbug.com/chromium/1137247#c11. As I mentioned there are two methods to hide real extensions:
1) By many space characters (hide real extensions)
2) By *. characters (real extensions disappears) (picture40.png)


### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-05)

mek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2020-11-06)

Any update?
Is it accepted?

Thanks :)

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ma...@gmail.com (2020-11-18)

Bug still persists in 87 version

### [Deleted User] (2020-11-21)

mek: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2020-11-30)

Bumping up mgt chain to see if there is a way to get some traction on this issue. Thanks.

### me...@chromium.org (2020-11-30)

Was my explanation of where we were with this bug in the email thread last week not satisfactory?

### pw...@chromium.org (2020-12-01)

TL;DR: mek@ is working with asully@ on designing and implementing a fix for this. Getting the fix right is non-trivial, and may take a bit of time.

I think we have a few related bugs, and folks may be getting confused. 

A discussion (Google-only, sorry) pointing to a document with solutions is at https://groups.google.com/a/google.com/g/chrome-security-enamel/c/q4NQ2N8r2yE/m/8qI-A4jpBAAJ

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c75c5a1e1d72fc923c82ebcaeacc874c88215eff

commit c75c5a1e1d72fc923c82ebcaeacc874c88215eff
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Dec 04 13:44:29 2020

Add restrictions to allowed extensions for File System Access API

These restrictions apply to showOpenFilePicker and showSaveFilePicker.

Existing restriction:
- Extension must start with "."

New restrictions:
- Allowed code points: [A-Za-z0-9+.]
- Extension length cannot exceed to 16, inclusive of leading "."
- Extension cannot end with "."
- Extension cannot end with "local" or "lnk"

Bug: 1137247, 1140410, 1140417, 1152327
Change-Id: I593f7ca60e05177402885bd3026add16b3a07d0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568534
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/master@{#833695}

[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/third_party/blink/renderer/modules/file_system_access/global_native_file_system.cc
[modify] https://crrev.com/c75c5a1e1d72fc923c82ebcaeacc874c88215eff/third_party/blink/web_tests/external/wpt/native-file-system/showPicker-errors.https.window.js


### as...@chromium.org (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

Requesting merge to stable M87 because latest trunk commit (833695) appears to be after stable branch point (812852).

Requesting merge to beta M88 because latest trunk commit (833695) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-05)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-07)

asully@ mek@ please help answer https://crbug.com/chromium/1137247#c33

### ad...@google.com (2020-12-07)

There's merge approval for this CL in https://crbug.com/chromium/1152327, so removing the duplication.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49

commit 96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Dec 07 22:09:02 2020

Add restrictions to allowed extensions for File System Access API

These restrictions apply to showOpenFilePicker and showSaveFilePicker.

Existing restriction:
- Extension must start with "."

New restrictions:
- Allowed code points: [A-Za-z0-9+.]
- Extension length cannot exceed to 16, inclusive of leading "."
- Extension cannot end with "."
- Extension cannot end with "local" or "lnk"

(cherry picked from commit c75c5a1e1d72fc923c82ebcaeacc874c88215eff)

Bug: 1137247, 1140403, 1140410, 1140417, 1140435, 1152327
Change-Id: I593f7ca60e05177402885bd3026add16b3a07d0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568534
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833695}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2576109
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#649}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/third_party/blink/renderer/modules/file_system_access/global_native_file_system.cc
[modify] https://crrev.com/96db1e0e8c1dfdfab9b8e305e3d2f3ffc9e1ba49/third_party/blink/web_tests/external/wpt/native-file-system/showPicker-errors.https.window.js


### me...@chromium.org (2020-12-08)

Actually this bug should not have been marked as fixed yet. We're still waiting to hear back from the security team to figure out what to do with misleading descriptions.

### ma...@gmail.com (2020-12-08)

Let me just make a point that the bug is a serious high-security problem.

If a user sees the OS/Chrome download dialog [pic1.png], he is 100% sure that he can trust it because the window is not a part of the website, it is a part of the Operating System. I can respect that the description should be editable, I agree with that. However, right now it is allowed to trick users to download a dangerous file.

In the video case, the user sees “JPEG Image (*.jpg)”, therefore the user is 100% sure that he can download and run it. Most users don't double-check to recognize if a file has the right extension, especially if the downloading file is an image .JPG that cannot be a virus.

The method is great for ransomware spreading, remote administration tools, and spreading other viruses. It will increase the open success rate by victims. Obviously, the bug is not an RCE, indeed is a security bug.

Why just not use the simplest way to solve the problem?
Block * character in the description and limit characters length?

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-12-08)

Not sure I agree with the severity of this (since I'm not convinced most users will understand that "jpg" is safe while "bat" isn't, but I'm definitely not an expert here).

That said, "Block * character in the description and limit characters length" is exactly what I suggested to the chrome security team in the above linked document (at least on Windows).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5bf1c6c22201394711a9067d2c970ab9f55555d0

commit 5bf1c6c22201394711a9067d2c970ab9f55555d0
Author: Marijn Kruisselbrink <mek@google.com>
Date: Thu Dec 10 20:51:08 2020

Ensure that showSaveFilePicker always shows the extension on Mac.

While not a very strong security boundary, making it possible for
users to know what extension a file will be saved with is a good idea.

This also fixes support for compound extensions with the File System
Access API (i.e. ".tar.gz"). The mac file dialog already had a
workaround if the default path ended in such an extension, but the
same problem occurs if the file type filters include a type with a
compound extension.

Bug: 1137247
Change-Id: I492bf36baced3de044b8fed5d57fc7b9b5b64400
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2582842
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#835803}

[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/ui/shell_dialogs/select_file_dialog_mac.mm
[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/components/remote_cocoa/common/select_file_dialog.mojom
[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/ui/shell_dialogs/select_file_dialog_mac_unittest.mm
[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/components/remote_cocoa/app_shim/select_file_dialog_bridge.mm
[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/ui/shell_dialogs/select_file_dialog.cc
[modify] https://crrev.com/5bf1c6c22201394711a9067d2c970ab9f55555d0/ui/shell_dialogs/select_file_dialog.h


### [Deleted User] (2020-12-12)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-15)

mek@ is this still waiting on input from security (estark@?), or is the commit in https://crbug.com/chromium/1137247#c41 complete? If so please mark this as Fixed and sheriffbot will initiate merge procedures. Thanks!

Please could you comment on whether you feel this has any compatibility or stability concerns, or if you would deem this safe to merge to M88/M87?

### me...@chromium.org (2020-12-15)

Sorry, I'm still working on a second CL to fix this on windows. So not complete yet. Hopefully will land that soon.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/25f38bb6322c0d93722c1faa3f6b4ea2daf2dc90

commit 25f38bb6322c0d93722c1faa3f6b4ea2daf2dc90
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed Dec 16 01:59:35 2020

[FSA] Sanitize descriptions for file types.

This collapses white space, limits the length of descriptions to 64
characters, and on windows strips out '*' characters to ensure the
windows dialog itself will still include the true extension.

This last behavior is triggered by the `keep_extension_visible` flag
that was added in https://crrev.com/c/2582842 to fix a similar problem
on Mac.

Tested: Verified that the extension is shown in the pickers shown by https://fsa-tests.glitch.me/accepts.html
Bug: 1137247
Change-Id: Ife2344589427dbc1055234026601642113b6a791
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2586958
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Robert Liao <robliao@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#837391}

[modify] https://crrev.com/25f38bb6322c0d93722c1faa3f6b4ea2daf2dc90/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/25f38bb6322c0d93722c1faa3f6b4ea2daf2dc90/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/25f38bb6322c0d93722c1faa3f6b4ea2daf2dc90/ui/shell_dialogs/select_file_dialog_win.cc


### me...@chromium.org (2020-12-17)

This should be fixed now.

### me...@chromium.org (2020-12-17)

Oh, and to answer the compatibility/stability concerns I think both the CL in https://crbug.com/chromium/1137247#c41 and the CL in https://crbug.com/chromium/1137247#c45 should be pretty safe to merge. They only effect UI treatment, and shouldn't have web exposed changes.

### ad...@google.com (2020-12-17)

I discussed with mek@. The merge labels here are in a bit of a mess, so I'm not sure what Sheriffbot will say, but I'm approving merge of the CLs in https://crbug.com/chromium/1137247#c41 and https://crbug.com/chromium/1137247#c45 to M88, branch 4324. I do not intend to approve merge to M87 given that these changes are somewhat complicated and the delay by waiting for M88 isn't very long.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd0863684fd07f37b78b53a78e71bebe924c5802

commit fd0863684fd07f37b78b53a78e71bebe924c5802
Author: Marijn Kruisselbrink <mek@google.com>
Date: Fri Dec 18 00:49:47 2020

Ensure that showSaveFilePicker always shows the extension on Mac.

While not a very strong security boundary, making it possible for
users to know what extension a file will be saved with is a good idea.

This also fixes support for compound extensions with the File System
Access API (i.e. ".tar.gz"). The mac file dialog already had a
workaround if the default path ended in such an extension, but the
same problem occurs if the file type filters include a type with a
compound extension.

(cherry picked from commit 5bf1c6c22201394711a9067d2c970ab9f55555d0)

Bug: 1137247
Change-Id: I492bf36baced3de044b8fed5d57fc7b9b5b64400
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2582842
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#835803}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2597785
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1044}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/ui/shell_dialogs/select_file_dialog_mac.mm
[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/components/remote_cocoa/common/select_file_dialog.mojom
[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/ui/shell_dialogs/select_file_dialog_mac_unittest.mm
[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/components/remote_cocoa/app_shim/select_file_dialog_bridge.mm
[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/ui/shell_dialogs/select_file_dialog.cc
[modify] https://crrev.com/fd0863684fd07f37b78b53a78e71bebe924c5802/ui/shell_dialogs/select_file_dialog.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bc9cb11cabd3a907b6bcbd60287015887fd4ea3b

commit bc9cb11cabd3a907b6bcbd60287015887fd4ea3b
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Fri Dec 18 02:41:27 2020

[FSA] Sanitize descriptions for file types.

This collapses white space, limits the length of descriptions to 64
characters, and on windows strips out '*' characters to ensure the
windows dialog itself will still include the true extension.

This last behavior is triggered by the `keep_extension_visible` flag
that was added in https://crrev.com/c/2582842 to fix a similar problem
on Mac.

(cherry picked from commit 25f38bb6322c0d93722c1faa3f6b4ea2daf2dc90)

Tested: Verified that the extension is shown in the pickers shown by https://fsa-tests.glitch.me/accepts.html
Bug: 1137247
Change-Id: Ife2344589427dbc1055234026601642113b6a791
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2586958
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Robert Liao <robliao@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#837391}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2597151
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1052}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/bc9cb11cabd3a907b6bcbd60287015887fd4ea3b/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/bc9cb11cabd3a907b6bcbd60287015887fd4ea3b/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/bc9cb11cabd3a907b6bcbd60287015887fd4ea3b/ui/shell_dialogs/select_file_dialog_win.cc


### ma...@gmail.com (2021-01-03)

Could you add reporter credits:

Reporter credit: Maciej Pulikowski

Thank you very much :)

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

Will do. In fact we'll do that by default for any bugs you submit henceforth, so let us know if you ever want us to change how you're credited. Thanks for the report!

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations, Maciej! The VRP panel decided to award you $1,000 for this report! Someone from our finance team will be in touch. Great job!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-27)

Desktop-only, not suitable for LTS

### vs...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2021-08-25)

Hi,

File extension still can be hidden if user has unchecked "File name extension" in File explorer on Windows. By default the option is UNCHECKED.

Example: https://pulik.io/msexploit/Dynamics365web.pdf

For a better view of the problem, I have created an example - PDF Reader with the exploit. Below we can read an example use case.

The user read a pdf file, but after 3 seconds he gets a pop-up to encourage him to download a file. The user downloads the file because he knows that pdf is a safe file, he runs a downloaded file and gets infected by ransomware. (in example .bat runs only calculator)

Someone first reported that here: https://bugs.chromium.org/p/chromium/issues/detail?id=1208439

The bug works on production in Google Chrome, Microsoft Edge and Opera

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1137247?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053546)*
