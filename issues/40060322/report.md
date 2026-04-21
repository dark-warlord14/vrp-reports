# Security: Symbolic Link Following + Upload Warning Bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40060322](https://issues.chromium.org/issues/40060322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File, Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac |
| **Reporter** | ro...@imperva.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-07-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When opening a directory by dropping a folder onto a file input element, Chrome does not sufficiently account for when the folder contains symbolic links that resolve to a target outside the intended control sphere.

Other APIs used for reading files, such as the File System Access API or the Drop Event (event.dataTransfer.items) ignore symbolic links. I believe this is the right thing to do, as most users don’t really understand what symbolic links are and or when and how they can be shared with them.

When uploading a directory using the file input attribute symbolic links are resolved. This includes nested symbolic links to directories which may result in the user uploading thousands of files.

When a folder is selected using a directory picker a warning is presented. The warning states the number of files to be uploaded as well as urges the user to proceed only if he trusts the site.

However, I found that when a folder is directly dropped onto the file input element no warning is shown, and all files including full directories which were resolved through a symbolic link will be uploaded.

This can be exploited using CSS:

input {  

top: 0;  

left: 0;  

opacity: 0;  

display: block;  

position: fixed;  

transform: scale(1000);  

}

The CSS above will make it so the user can drop the folder anywhere on the page to trigger the upload.

I would also like to note that Chromium is the only browser I tested with this behavior, Safari does not resolve any symlinks while Firefox resolves the symlinks to specific files but not to directories.

The attached proof of concept is designed to trick the user into uploading a folder that contains a hidden directory with a number of symlinks to sensitive files/directories in macOS.

In my PoC I’ve used a zip file. However, it’s important to note symlinks can also be shared using SMB and other shared drive services.

**VERSION**  

Chrome Version: Google Chrome 103.0.5060.114 (Official Build) (arm64)  

Operating System: macOS Monterey, 12.4 (21F79)

**REPRODUCTION CASE**

1. Download the attached "poc.zip" and unzip it
2. Navigate to "fancy-poc" and serve the files (python3 -m http.server)
3. Open <http://localhost:8000> and follow the PoC instructions

Please note, I’ve also included the "basic-poc" with a simplified version of the bug.

**CREDIT INFORMATION**  

Ron Masas, Imperva.com

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 28.7 KB)

## Timeline

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-19)

This requires the user to upload a directory that contains a symbolic link to another directory, right?

I am going to tag this as High; for "Critical", an example bug is "A bug that enables web content to read local files".

This arguably does let an attacker read local files, but it requires user interaction to set up the local malicious directory that then needs to be uploaded.

+asully, can you help find an OWNER for this? I'm not sure if you're the right OWNER, but this is at least tangentially related to the file system API / drop (given the restrictions mentioned above), so it seems like this should be under a similar umbrella.

[Monorail components: Blink>Forms>File]

### [Deleted User] (2022-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-08-01)

I'm not sure who the right owner is here. The Blink>Forms>File component seems to have a number of unowned bugs... I'll mark this as available and hope someone sees it in triage

> This requires the user to upload a directory that contains a symbolic link to another directory, right?

Yes, and for the (hidden) symlinks to the sensitive files to already be on the user's machine. At which point the machine must already have malicious actors outside of the browser, since AFAIK sites can't use the browser to write symlinks to the file system (and if so, that seems like a bigger problem).

My understanding is this bug is saying that Chrome will follow symlinks, even to sensitive locations. So the symlinks are effectively a way to bypass the blocklists we have for sensitive directories. Which isn't great, but doesn't seem like a High severity bug to me?

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-08-10)

Chrome security marshal here. Looks like third_party/blink/renderer/core/html/forms/ has metadata Blink>Forms, maybe somebody from that OWNERS file can help? keishi@, tkent@ - any thoughts on who can own this?

### as...@chromium.org (2022-08-10)

whoops, forgot to actually mark this Available

### ma...@chromium.org (2022-08-11)

I am an owner for Forms, and reading the description of this bug, particularly https://crbug.com/chromium/1345275#c5, it doesn't seem like a high priority security bug to me. I agree it's not great that Chrome will follow symlinks to sensitive locations, but the machine seems fairly compromised already. Correct me if I'm wrong. I'm going to lower this to P-2 accordingly. Feel free to put it back if you disagree.

Code for dropped files is here:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/file_input_type.cc;l=485;drc=ee5503bf7e1ef7d95d7ff7b248fe82c2ab20d53a


### ro...@imperva.com (2022-08-11)

I think P-2 probably makes sense due to the user interaction required. However, I do want to point out I disagree with the idea that the machine have to be already compromised.

Symlinks can easily be shared using a zip file as shown in my PoC, or using popular drive services such as iCloud.

### [Deleted User] (2022-08-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### za...@google.com (2022-08-29)

Security marshal here, friendly ping to see if anyone can own this bug? cc: keishi@ and tkent@ 

### ma...@chromium.org (2022-08-29)

Could someone from the FileSystem team point me in the right direction here? It sounds like the file system API is sanitizing for symlinks, while the <input type=file> just reads whatever is selected (including if drag/drop is used). If there's an easy entry point to the same sanitization logic, and someone could give me some pointers, we can try to hook it up to <input type=file>.

[Monorail components: Blink>Storage>FileSystem]

### as...@chromium.org (2022-08-29)

base::PathExists() and base::DirectoryExists() return false for symlinks

We check FileSystemOperationRunner::DirectoryExists() before giving a site access to a directory handle, which has the effect of sanitizing for symlinks https://crsrc.org/c/content/browser/file_system_access/file_system_access_directory_handle_impl.cc;l=143-148?q=DirectoryExists

### ma...@chromium.org (2022-08-30)

Cool, thanks for https://crbug.com/chromium/1345275#c14.

xiaochengh@, would it be possible for you to take a look at this bug? Essentially it requires an extra round trip to the browser to check whether files/directories exist (and aren't symlinks) before using them in the FileInputType.

### [Deleted User] (2022-08-31)

xiaochengh: Uh oh! This issue still open and hasn't been updated in the last 43 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-09-01)

Hi everyone,

I tried to put up a patch to make FileChooserImpl remove symlinks with base::PathExists(), but it doesn't work: https://chromium-review.googlesource.com/c/chromium/src/+/3866767

Is there something that I missed?

Btw the code that actually enumerates a directory is base::FileEnumerator, but it's used very widely and I'm not sure if I should change anything at such a deep level... So I'm planning to change FileChooserImpl only, which is the browser-side of <input type=file>

### as...@chromium.org (2022-09-01)

Hmm it looks like FileSystemOperationRunner::DirectoryExists may not actually call base::PathExists [1] as I had assumed, but explicitly filters out symlinks using base::IsLink [2]

Apologies for the confusion. base::IsLink is more descriptive of what we want here anyways. Give that a try?

[1] https://crsrc.org/c/storage/browser/file_system/local_file_util.cc;l=125-126;drc=cad8d0a2ad2538fb85df0160622da76107f79acf
[2] https://crsrc.org/c/storage/browser/file_system/local_file_util.cc;l=254-255;drc=cad8d0a2ad2538fb85df0160622da76107f79acf

### xi...@chromium.org (2022-09-01)

That works. Thanks!

### gi...@appspot.gserviceaccount.com (2022-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/933cc81c6bad0bb1aaf1b07b7255500efc58de6e

commit 933cc81c6bad0bb1aaf1b07b7255500efc58de6e
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Sat Sep 10 05:53:49 2022

Remove symlinks from FileChooserImpl folder upload result

FileChooserImpl is the browser-side implementation of
<input type=file>. When uploading a whole folder, it
currently uses DirectoryLister to list all the files in a
directory. The result also includes resolved symbolic links
(which may even hide deep in some subfolder), which is not a
desired behavior.

Therefore, this patch removes all symbolic links from the
result by checking each file against `base::IsLink()`. Since
the function needs blocking calls to access file data, the
job is sent to a worker pool thread.

Fixed: 1345275
Change-Id: I8ab58214c87944408c64b177e915247a7485925b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3866767
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1045491}

[modify] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/browser/web_contents/file_chooser_impl.cc
[add] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/test/data/file_chooser/dir_with_symlink/text_file.txt
[modify] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/browser/web_contents/file_chooser_impl_browsertest.cc
[modify] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/test/content_browser_test_utils_internal.h
[add] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/test/data/file_input_webkitdirectory.html
[modify] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/browser/web_contents/file_chooser_impl.h
[modify] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/test/content_browser_test_utils_internal.cc
[add] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/test/data/file_chooser/dir_with_symlink/symlink
[add] https://crrev.com/933cc81c6bad0bb1aaf1b07b7255500efc58de6e/content/test/data/file_chooser/linked_text_file.txt


### [Deleted User] (2022-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-10)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations, Ron! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### ro...@imperva.com (2022-11-10)

Hi everyone,

I've tested my proof of concept on the latest version of Chrome for Mac version 107.0.5304.110 (arm64) and it's still works.
According to the release notes https://chromereleases.googleblog.com/2022/10/stable-channel-update-for-desktop_25.html I assumed it was patched in version >=107.0.5304.62.

### xi...@chromium.org (2022-11-10)

I verified locally that it's fixed in Chrome 107 on Mac. Here's my screen recording:

https://drive.google.com/file/d/16OGixRam5qxe93N35gwHD4s4AzoGQv64/view?usp=share_link

Did I miss anything?

### ro...@imperva.com (2022-11-10)

I think so...

The recovery-phrase/.wave folder contains the following **relative** symbolic links:

.aws_2 -> ../../.aws
.aws_3 -> ../../../.aws
.aws_4 -> ../../../../.aws
.bash_history_2 -> ../../.bash_history
.bash_history_3 -> ../../../.bash_history
.bash_history_4 -> ../../../../.bash_history
ethereum_2 -> ../../.ethereum
.ethereum_3 -> ../../../.ethereum
ethereum_4 -> ../../../../.ethereum
.zsh_history_2 -> ../../.zsh_history
.zsh_history_3 -> ../../../.zsh_history
.zsh_history_4 -> ../../../../.zsh_history
hosts -> /etc/hosts
ssh_2 -> ../../.ssh
ssh_3 -> ../../../.ssh
ssh_4 -> ../../../../.ssh

It seems you are uploading the folder directly from the POC folder which means the symlinks are relatively pointing to a file that does not exists.
The "recovery-phrase" folder should only be used as part of "fancy-poc" flow, the POC was designed to work when the folder is uploaded from the user ~/Downloads folder. This is the normal attack flow when the victim downloads and extracts recovery-phrase.zip.

You can confirm the bug still exists by moving the folder to ~/Downloads.
I suspect the fix only handles absolute symbolic links since the "hosts" is correctly ignored now.

### xi...@chromium.org (2022-11-10)

I see. The fix in M107 was incomplete that it still allowed directory symlinks to be followed.

This has been fully blocked in M109 (see https://crbug.com/chromium/1378997).

### [Deleted User] (2022-12-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345275?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>File, Blink>Storage>FileSystem]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060322)*
