# Security: FileChooserImpl still traverse symlink in symlink to directory

| Field | Value |
|-------|-------|
| **Issue ID** | [40061499](https://issues.chromium.org/issues/40061499) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File>Directory |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-10-27 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

As a continuation of <https://bugs.chromium.org/p/chromium/issues/detail?id=1378484> (and <https://chromium-review.googlesource.com/c/chromium/src/+/3866767>), <input type="file" webkitdirectory>, will on MacOS, traverse the symlink when a folder containing a symlink pointing to a directory. (Test 6)

**VERSION**  

Chrome Version: [107.0.5304.62] + [stable]  

Operating System: MacOS

**REPRODUCTION CASE**

1. Execute command  
   
   mkdir poc-folder  
   
   cd poc-folder  
   
   ln -s ../Desktop symlink
2. Now go to input.html and upload the poc-folder
3. Execute in the JS console:

read = new FileReader();  

read.readAsBinaryString(document.getElementById('fileinput').files[1]);  

read.onloadend = function(){  

console.log(read.result);  

}

Content of one of the files stored in Desktop should be printed

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [input.html](attachments/input.html) (text/plain, 54 B)
- [poc-folder.zip](attachments/poc-folder.zip) (application/octet-stream, 196 B)

## Timeline

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-10-27)

As an added bonus, Unix file systems allow me to preserve symlinks in zip files, so I can possibly ask someone to download and unzip my zip file containing symlinks, and then they proceed to upload it and when they upload it, they will upload whatever directory the symlink points to. To test this you can try unzipping this file in MacOS in your home directory and then upload it to input.html + repeat the steps above.

### ha...@gmail.com (2022-10-27)

Note that this isn't a duplicate of https://bugs.chromium.org/p/chromium/issues/detail?id=1378484. This bug is about <input type="file" webkitdirectory> which is different from the Filesystem Access API in 1378484

### ha...@gmail.com (2022-10-28)

Also note that for Step 3; You should use index 0 instead (just in case your Desktop folder only has one file.)

read = new FileReader();
read.readAsBinaryString(document.getElementById('fileinput').files[0]);
read.onloadend = function(){
    console.log(read.result);
}

Owner of this should probably be same as https://chromium-review.googlesource.com/c/chromium/src/+/3866767.


### me...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>Forms>File>Directory]

### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-10-28)

This is similar to https://crbug.com/chromium/1378484 (CC'ing owners from there).

pbos: Could you please take a look or reassign as appropriate? 

### pb...@chromium.org (2022-10-28)

-> asully@ can you find an owner or triager, I have not touched any underlying stuff.

### [Deleted User] (2022-10-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-10-28)

xiaochengh could you look into this?

### xi...@chromium.org (2022-10-28)

+mmenke as /net/ owner

In https://chromium-review.googlesource.com/c/chromium/src/+/3866767, we removed the files that are themselves symlinks.

But this is not enough as DirectoryLister also follows directory symlinks, and returns non-link files in them.

If we want to remove them in FileChooserImpl, then we need to tell if a part of a Path is a symlink. I haven't seen an easy & clean way to do this.

Maybe a better solution is to pass a flag to DirectoryLister that disables it from following symlinks. WDYT?

### mm...@chromium.org (2022-10-30)

So how would it hide sym links?  Looks like it's not setting SHOW_SYM_LINKS in its call to FileEnumerator, so I'm not quite sure why it's seeing them (Though its primary purpose was for displaying file URLs, where it makes sense to show them, if the user has access to them).

Looks like the file URL stuff uses MakeAbsolutePath to check for permissions on resolved symbolic links, but since we care here not about where a symbolic link resolves to, but rather that it is a symbolic link, would be a bit more involved to use it in the calling code here.

### xi...@chromium.org (2022-11-01)

SHOW_SYM_LINKS doesn't seem to do anything with whether to include symlinks into the result (if I read the code correctly).

Given that DirectoryLister's NO_SORT_RECURSIVE mode is used by FileChooserImpl only, I'll try passing a flag to FileEnumerator to not traverse any symlink under this mode.

### xi...@chromium.org (2022-11-01)

Or maybe it's still safer to fix at FileChooserImpl... WIP: https://chromium-review.googlesource.com/c/chromium/src/+/3997423

### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4fa830d8af6b2fb293219edeb39eebccfd322305

commit 4fa830d8af6b2fb293219edeb39eebccfd322305
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Thu Nov 03 23:40:36 2022

Do not traverse directory symlinks when uploading folder

Previous patch crrev.com/c/3866767 removed symlink files when uploading
a folder. However, while the remaining files are themselves not
symlinks, they may be included as the result of traversing directory
symlink.

This patch further excludes such files by checking if any parent
directory is a symlink, all the way until the base directory (which is
the directory chosen for upload).

Fixed: 1378997
Change-Id: I75a92df4cd50f9aba7824955a3de792583bc6154
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3997720
Reviewed-by: Austin Sullivan <asully@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1067310}

[modify] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/browser/web_contents/file_chooser_impl.cc
[add] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/test/data/file_chooser/dir_with_dir_symlink/symlink
[modify] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/browser/web_contents/file_chooser_impl_browsertest.cc
[modify] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/test/content_browser_test_utils_internal.h
[add] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/test/data/file_chooser/linked_dir/bar.txt
[modify] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/test/content_browser_test_utils_internal.cc
[add] https://crrev.com/4fa830d8af6b2fb293219edeb39eebccfd322305/content/test/data/file_chooser/dir_with_dir_symlink/foo.txt


### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-11-10)

I'm afraid that we probably need to merge it to M108 or even M107.

Although this is an existing issue, this is actually part of https://crbug.com/chromium/1345275, which we landed an incomplete fix [1] in M107 and announced it in the release notes with a bug number [2]. Although https://crbug.com/chromium/1345275 is still restricted, people can still find its details by searching the bug number at Gerrit [3]. So we have sort of publicized a security vunerability while we only have a partial fix landed.

So we should probably merge the full fix (#c15).

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3866767
[2] https://chromereleases.googleblog.com/2022/10/stable-channel-update-for-desktop_25.html
[3] https://chromium-review.googlesource.com/q/bug:1345275

### [Deleted User] (2022-11-10)

Merge review required: M108 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-11-10)

1. Security issue
2. https://chromium-review.googlesource.com/c/chromium/src/+/3997720
3. Yes
4. No
5. N/A
6. N/A

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations on another one this week, Axel! The VRP Panel has decided to award you $3,000 for this report. Thank you for all your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-12)

Hi Xiaocheng, thanks for landing the fix for this issue. WRT https://crbug.com/chromium/1378997#c19, this is the correct assertion and thank you for working through that and taking it into consideration. 
As a medium severity security bug, this should be merged to 108 (currently beta) regardless, so the fix can be included in the 108 Stable milestone release.

Regardless of the partial fix being published through release notes, commits are public once they are landed and adversaries work monitor our repos looking for potential security fixes that can be RE to exploit. Because of this, we aim to keep our patch gap as small as possible. Please update security bugs as fixed as soon as the resolving CL is landed. This allows the bot to add the relevant security merge request/review labels based on severity and impact. This allows us to also make that determination and work with you if there are issues or complications with backporting. :) 

M108 merge approved, please merge this fix to branch 5359 by 11am Pacific Time, Monday 14 November so this fix can be included in M108 Stable cut occurring on Tuesday morning Pacific. 

### sr...@google.com (2022-11-14)

I have CP'ed the CL to M108 here -
https://chromium-review.googlesource.com/c/chromium/src/+/4025427

Please monitor and make sure merge lands before EOD today

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f46db6aac3e9b23511c70e3afe84b641e7ef8812

commit f46db6aac3e9b23511c70e3afe84b641e7ef8812
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Mon Nov 14 20:01:38 2022

Do not traverse directory symlinks when uploading folder

Previous patch crrev.com/c/3866767 removed symlink files when uploading
a folder. However, while the remaining files are themselves not
symlinks, they may be included as the result of traversing directory
symlink.

This patch further excludes such files by checking if any parent
directory is a symlink, all the way until the base directory (which is
the directory chosen for upload).

(cherry picked from commit 4fa830d8af6b2fb293219edeb39eebccfd322305)

Fixed: 1378997
Change-Id: I75a92df4cd50f9aba7824955a3de792583bc6154
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3997720
Reviewed-by: Austin Sullivan <asully@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1067310}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025427
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#823}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/browser/web_contents/file_chooser_impl.cc
[add] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/test/data/file_chooser/dir_with_dir_symlink/symlink
[modify] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/test/content_browser_test_utils_internal.h
[modify] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/browser/web_contents/file_chooser_impl_browsertest.cc
[add] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/test/data/file_chooser/linked_dir/bar.txt
[modify] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/test/content_browser_test_utils_internal.cc
[add] https://crrev.com/f46db6aac3e9b23511c70e3afe84b641e7ef8812/content/test/data/file_chooser/dir_with_dir_symlink/foo.txt


### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1378997?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061499)*
