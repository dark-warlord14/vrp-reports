# Security: FSA API's directory methods allows traversing symlinks in folders on Windows (even to restricted directories)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061477](https://issues.chromium.org/issues/40061477) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2022-10-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

After reading <https://chromium-review.googlesource.com/c/chromium/src/+/3866767>, I noticed that the FSA (FileSystemAccess) API methods still allows traversing symlinks on Windows, more specifically, FSA (FileSystemAccess) will still allow a symlink present in a selected folder to be traversed.

This could result in accidental leak of files by user.

It seems weird to me that FSA still does this even though it has additional restrictions (such as disallowing upload Desktop, Downloads folder) over <input type=file>.

**VERSION**  

Chrome Version 107.0.5304.63 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins  

Operating System: [Windows 10 Version 21H2 (Build 19044.2130)]

**REPRODUCTION CASE**

1. On Windows, execute following in CMD prompt.

cd %USERPROFILE%  

mkdir poc-folder  

cd poc-folder  

mklink /D symlink "..\Desktop"

2. Now go to poc.html, and select the poc-folder.
3. Go to the Console and see the names of all the files present in the Desktop folder get printed, even though "Desktop" regarded sensitive directory in FSA.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-10-26)

Thanks for the report. xiaochengh, could you PTAL?

[Monorail components: Blink>Forms>File Blink>Storage>FileSystem]

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-10-26)

This is unrelated to Blink>Forms. Blink>Storage>FileSystem should be the proper owner.

[Monorail components: -Blink>Forms>File]

### me...@chromium.org (2022-10-26)

mek, could you PTAL?

### me...@chromium.org (2022-10-26)

I'm no longer involved with storage/file system things, so over to asully@ instead.

### ha...@gmail.com (2022-10-27)

Ok I've just tested this on my MacOS too. I also tested <input type="file">, whether a symlink pointing to a file gets traversed and compiled my results in a table.

Build: 107.0.5304.62
--------------------------------------------------------------------------------------------------------------------------------
Platform / Symlink Type / Implementation                                 |    symlink traversed?
---------------------------------------------------------------------------------------------------------------------------------
1. <input type="file" webkitdirectory> / file  / Windows                  |        Yes.
2. <input type="file" webkitdirectory> / directory / Windows          |        No.
3. FSA / file / Windows                                                                  |        Yes.
4. FSA / file / Windows                                                                  |        Yes.
5. <input type="file" webkitdirectory> / file  / MacOS                    |         No.
6. <input type="file" webkitdirectory> / directory / MacOS            |        Yes.
7. FSA / file / MacOS                                                                    |         No.
8. FSA / directory / MacOS                                                           |         No.
---------------------------------------------------------------------------------------------------------------------------------

So it also seems like for Windows <input type="file">, uploading a folder containing the symlink still uploads the symlink pointing to files (Test 1). And for MacOS, <input type="file"> still traverses the symlink when a directory containing symlink pointing to a directory gets uploaded (Test 6). I think I will file a new bug for that one

For FSA it just seems that Windows is the problem. (FSA doesn't traverse symlinks on MacOS)

### ha...@gmail.com (2022-10-27)

*For Test 4" it should say "FSA / directory / Windows"

### ha...@gmail.com (2022-10-27)

Regarding Test 1, it seems that the symlink will be traversed but attempting to read the file will result in nothing happening so I don't think it is an issue for <input type="file" webkitdirectory>. Also filed https://bugs.chromium.org/p/chromium/issues/detail?id=1378997 for Test 6.

### [Deleted User] (2022-10-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-10-27)

There's a couple different issues here:

(1) using the file picker to select a file or directory which is a symlink
(2) after gaining access to a directory, traversing symlinks within the directory

In both cases, it seems reasonable to allow the site to traverse the symlink as long as it doesn't point to a blocklisted path.

Case (1) is similar to https://crbug.com/chromium/1326788. We should normalize the path (including following symlinks) of any file or directory selected via the file picker to check whether it is on the blocklist.

Case (2) is trickier. Unlike <input type="file" webkitdirectory>, we don't scan the contents of the directory when it's selected. We cannot make the types of checks added in https://crrev.com/c/3866767. We'd have to normalize the path on every traversal... 

That being said, I'm not sure whether these are all that high-priority since it requires such a symlink to exist on your machine already (i.e. there's no way to create it from the web). Though (1) at least seems like low-hanging fruit that we should fix

### ha...@gmail.com (2022-10-28)

I did test (1) and FSA API does prevent me from explicitly selecting a symlink to a system folder, so its just (2).

### me...@chromium.org (2022-10-28)

+pbos for visibility as this is similar to https://crbug.com/chromium/1378997.

### ds...@chromium.org (2022-11-01)

Symlink can be created to a file/dir after a permission is given to its parent directory. Also, a symlink can be created to a path that is not yet existent. So rather than traversing a directory upon picker selection, we can try to check it as close as possible to when a file or directory handle is requested. 


### [Deleted User] (2022-11-15)

dslee: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-15)

I am not too sure about the exact rationale behind https://chromium-review.googlesource.com/c/chromium/src/+/3866767 (I don't have access to the bug report itself) but I've a feeling its because zip can hold a symlink for Unix systems rather than just accidental file disclosure. Afaict, for windows systems, it is difficult for someone malicious to transport symlinks (I did try using 7zip but you need to enable a flag in order for the symlink to be unloaded).

So I agree with https://crbug.com/chromium/1378484#c11 that this issue not really high priority as the only risk is accidental disclosure, maybe not even a security issue. (but regardless this bug MUST still have restrict-view flags on as it contains references to the other security bugs)



 

### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6fa69be631ec6e50522a08a6776fae0e2cfd5de1

commit 6fa69be631ec6e50522a08a6776fae0e2cfd5de1
Author: Daseul Lee <dslee@chromium.org>
Date: Wed Nov 16 18:00:04 2022

[FSA] Check the blocklist when getting a file handle with symbolic link.

When getting a file handle from a directory handle via `GetFile()` or `GetEntries()`, the file handle may be a symlink file that could potentially point to a blocklisted path, if the said file is created after a permission is granted to the parent directory. While this cannot happen via web API, but can only be done on a local machine directly, additional checks against symlink destination can help reduce security risks. Currently, this check is only done on non-Windows only as we are lacking Windows file util for reading a symlink path.

In addition, this change also updates the way FileSystemAccessDirectoryEntriesListener is passed; instead of a raw pointer, refcounted pointer is used, wrapped by a struct that supports `base::RefCountedDeleteOnSequence` for deleting it on the right sequence.

Bug: 1378484
Change-Id: I28ebd38b11665b9c93b829a3bfbea5b208991222
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4005144
Reviewed-by: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Daseul Lee <dslee@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1072312}

[modify] https://crrev.com/6fa69be631ec6e50522a08a6776fae0e2cfd5de1/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/6fa69be631ec6e50522a08a6776fae0e2cfd5de1/content/public/browser/file_system_access_permission_context.h
[modify] https://crrev.com/6fa69be631ec6e50522a08a6776fae0e2cfd5de1/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc
[modify] https://crrev.com/6fa69be631ec6e50522a08a6776fae0e2cfd5de1/content/browser/file_system_access/file_system_access_directory_handle_impl.cc
[modify] https://crrev.com/6fa69be631ec6e50522a08a6776fae0e2cfd5de1/content/browser/file_system_access/file_system_access_directory_handle_impl_unittest.cc
[modify] https://crrev.com/6fa69be631ec6e50522a08a6776fae0e2cfd5de1/content/browser/file_system_access/file_system_access_directory_handle_impl.h


### ha...@gmail.com (2022-11-16)

Hmm, I noticed the fix CL excludes windows which was the platform I only observed the bug on. The bug here was that on windows, a directory containing directory symlink would still traverse the directory symlink (even those in the blocklist (ie. Desktop, Downloads) by FSA API). I did remember testing this on my Mac, and directory symlinks seem to not get traversed. So not sure what the above CL fixes.

### ds...@chromium.org (2022-11-17)

Thanks for clarifying that. Right now, we are missing some utility functions to check for symlink and reading the resolved path on Windows, so the follow-up change should include that and enabling the new logic in the CL from https://crbug.com/chromium/1378484#c18 on Windows as well. 

### ds...@chromium.org (2022-11-17)

Also, lowering the priority to 2 based on the discussions above.

### [Deleted User] (2022-11-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-01-12)

dslee, is there a bug for the utility function work in C20 that this could link to? Otherwise, is that work still blocking this issue?


### ds...@chromium.org (2023-01-26)

I only see an old TODO for rkc@ who no longer seems to work for Chromium, and I did not find any tracking bug for this.
https://source.chromium.org/chromium/chromium/src/+/main:base/files/file_util_win.cc;l=851;drc=63e1f9974bc57b0ca12d790b2a73e5ba7f5cec6e

Yes, it's still a blocking issue. Since base::IsLink is used in many places, I suppose there is a big dependency here.
tsepez@ - Do you know who owns base file and/or might be able to help here?

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-21)

[secondary shepherding]
dcheng@ - do you have an idea about the timeline for the utility functions mentioned in https://crbug.com/chromium/1378484#c26 and https://crbug.com/chromium/1378484#c20?

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-20)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-20)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-21)

Status update:

The utility function base::isLink is not yet ready and had not been staffed for implementation. Once this is ready we can have a mitigation for this issue and iterate from there for more granular control. 
Assigning to dcheng@ who has graciously volunteered to work on moving this forward!

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-10-25)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-11-20)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-11-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c6780249446e2baa1b6426d9936e11c0e0f30a8c

commit c6780249446e2baa1b6426d9936e11c0e0f30a8c
Author: Daseul Lee <dslee@chromium.org>
Date: Thu Dec 07 19:52:52 2023

[FSA] Handle symbolic links when checking blocklists.

(1) When checking blocklists, use a resolved path returned from
`base::MakeAbsoluteFilePath()`, which is expected to resolve any
symbolic link.

(2) Additionally, check for blocklist when getting a file handle or
entries (that are files) from a directory handle. With (1), this check
will make sure any new symlink created after the initial check on the
parent directory is caught and re-run with blocklist check on fully
resolved path.

Previously, crrev.com/c/4005144 attempted to handle case (2) partially
on POSIX, using `base::IsLink()` and `base::ReadSymbolicLink()`, causing
some potential bugs. This CL re-attempts to fix the issue using
`base::MakeAbsoluteFilePath()`, which is available on both POSIX and
Windows.

Both features are disabled and will be enabled after testing.

Bug: 1378484
Change-Id: If319359492c08dd829b42262918ad208bbc351c8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5068377
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Daseul Lee <dslee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1234657}

[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/content/browser/file_system_access/file_system_access_manager_impl_unittest.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/content/browser/file_system_access/features.h
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/content/browser/file_system_access/features.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/content/browser/file_system_access/file_system_access_directory_handle_impl.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/chrome/browser/file_system_access/file_system_access_features.h
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/chrome/browser/file_system_access/file_system_access_features.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/content/browser/file_system_access/file_system_access_directory_handle_impl_unittest.cc
[modify] https://crrev.com/c6780249446e2baa1b6426d9936e11c0e0f30a8c/content/browser/file_system_access/file_system_access_directory_handle_impl.h


### gi...@appspot.gserviceaccount.com (2024-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/296626af45dea3a6f53362a29c4d00f268ff790f

commit 296626af45dea3a6f53362a29c4d00f268ff790f
Author: Daseul Lee <dslee@chromium.org>
Date: Fri Jan 05 21:04:12 2024

[FSA] Enable blocklist check on symbolic links on POSIX.

Resolving symbolic links via `base::MakeAbsoluteFilePath()` only
works on POSIX, but not on Windows. Enable the partial fix on
POSIX only for now.

Bug: 1378484
Change-Id: I3a590153c320717f5a57cc777f8f50dec38d3b1b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5165788
Commit-Queue: Daseul Lee <dslee@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1243601}

[modify] https://crrev.com/296626af45dea3a6f53362a29c4d00f268ff790f/content/browser/file_system_access/features.cc


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

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1378484?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1503946]
[Monorail mergedwith: crbug.com/chromium/1493201, crbug.com/chromium/1503400]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 152 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ds...@chromium.org (2024-03-14)

dcheng@ - is there a plan for base file util implementation?

FWIW, I created a separate bug for tracking base::IsLink implementation: issue 329691615

### ap...@google.com (2024-04-11)

Project: chromium/src
Branch: main

commit 6bbf3a1af202ac5c0ae24266f4b2e4ace23de8a0
Author: Daniel Soromou <fosoromo@microsoft.com>
Date:   Thu Apr 11 21:26:45 2024

    Windows: Implement IsLink
    
    This CL adds helpers IsLink(...) for symbolic link handling in
    the Windows to unblock https://issues.chromium.org/issues/40061477.
    
    The necessity for the `IsLink` helper arises from a specific
    security concern related to file handling during directory traversal.
    When a file handle is obtained through `GetFile()` or `GetEntries()`
    from a directory handle, there's a possibility that this file handle
    represents a symlink file. This symlink could potentially point to a
    path that is blocklisted, posing a security risk. Such a scenario might
    occur if the symlink file is created after permissions have been
    granted to access the parent directory. Although this situation cannot
    occur through web API and it's only possible when it done on the local
    machine.
    
    However, the isuse is currently implemented on non-Windows platforms
    only, due to the absence of a helper on Windows to detect symlinks.
    
    Bug: 329691615, 40061477
    Change-Id: I32b2f14bf02a096bae693b8867a2690eeffb1c2d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5376340
    Reviewed-by: Greg Thompson <grt@chromium.org>
    Reviewed-by: Mark Mentovai <mark@chromium.org>
    Reviewed-by: Daseul Lee <dslee@chromium.org>
    Commit-Queue: Daniel Soromou <fosoromo@microsoft.com>
    Cr-Commit-Position: refs/heads/main@{#1286106}

M       base/files/file_util.h
M       base/files/file_util_unittest.cc
M       base/files/file_util_win.cc

https://chromium-review.googlesource.com/5376340


### ap...@google.com (2024-04-12)

Project: chromium/src
Branch: main

commit dbce6a8e933bf1af781a40d33b04e27b81d2fa9e
Author: Osama Fathy <osamafathy@google.com>
Date:   Fri Apr 12 08:16:38 2024

    Revert "Windows: Implement IsLink"
    
    This reverts commit 6bbf3a1af202ac5c0ae24266f4b2e4ace23de8a0.
    
    Reason for revert: FileUtilTest.IsLink* tests are failing - Step "base_unittests on Windows-10" failing on builder "chrome/ci/win-chrome"
    
    Original change's description:
    > Windows: Implement IsLink
    >
    > This CL adds helpers IsLink(...) for symbolic link handling in
    > the Windows to unblock https://issues.chromium.org/issues/40061477.
    >
    > The necessity for the `IsLink` helper arises from a specific
    > security concern related to file handling during directory traversal.
    > When a file handle is obtained through `GetFile()` or `GetEntries()`
    > from a directory handle, there's a possibility that this file handle
    > represents a symlink file. This symlink could potentially point to a
    > path that is blocklisted, posing a security risk. Such a scenario might
    > occur if the symlink file is created after permissions have been
    > granted to access the parent directory. Although this situation cannot
    > occur through web API and it's only possible when it done on the local
    > machine.
    >
    > However, the isuse is currently implemented on non-Windows platforms
    > only, due to the absence of a helper on Windows to detect symlinks.
    >
    > Bug: 329691615, 40061477
    > Change-Id: I32b2f14bf02a096bae693b8867a2690eeffb1c2d
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5376340
    > Reviewed-by: Greg Thompson <grt@chromium.org>
    > Reviewed-by: Mark Mentovai <mark@chromium.org>
    > Reviewed-by: Daseul Lee <dslee@chromium.org>
    > Commit-Queue: Daniel Soromou <fosoromo@microsoft.com>
    > Cr-Commit-Position: refs/heads/main@{#1286106}
    
    Bug: 329691615, 40061477
    Change-Id: Ic38018d6a9d5ceaccc7928f26dc7626a4990035a
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5447698
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Owners-Override: Osama Fathy <osamafathy@google.com>
    Commit-Queue: Osama Fathy <osamafathy@google.com>
    Cr-Commit-Position: refs/heads/main@{#1286351}

M       base/files/file_util.h
M       base/files/file_util_unittest.cc
M       base/files/file_util_win.cc

https://chromium-review.googlesource.com/5447698


### ap...@google.com (2024-04-16)

Project: chromium/src
Branch: main

commit 0bfea22d30a66f9622e7a211f0a2edb6b9840e32
Author: Daniel Soromou <fosoromo@microsoft.com>
Date:   Tue Apr 16 09:59:49 2024

    Reland "Windows: Implement IsLink"
    
    This is a reland of commit 6bbf3a1af202ac5c0ae24266f4b2e4ace23de8a0.
    
    In the previous update, the `FileUtilTest.IsLink*` tests were failing on
    Windows 10 because the availability of `CreateSymbolicLink` can vary
    based on several factors, including whether the user has
    administrative privileges, is in developer mode, or due to Group
    Policy and User Account Control (UAC) settings.
    
    In this reattempt, the tests have been updated to skip cases where
    `CreateSymbolicLink` fails.
    
    Original change's description:
    > Windows: Implement IsLink
    >
    > This CL adds helpers IsLink(...) for symbolic link handling in
    > the Windows to unblock https://issues.chromium.org/issues/40061477.
    >
    > The necessity for the `IsLink` helper arises from a specific
    > security concern related to file handling during directory traversal.
    > When a file handle is obtained through `GetFile()` or `GetEntries()`
    > from a directory handle, there's a possibility that this file handle
    > represents a symlink file. This symlink could potentially point to a
    > path that is blocklisted, posing a security risk. Such a scenario might
    > occur if the symlink file is created after permissions have been
    > granted to access the parent directory. Although this situation cannot
    > occur through web API and it's only possible when it done on the local
    > machine.
    >
    > However, the isuse is currently implemented on non-Windows platforms
    > only, due to the absence of a helper on Windows to detect symlinks.
    >
    > Bug: 329691615, 40061477
    > Change-Id: I32b2f14bf02a096bae693b8867a2690eeffb1c2d
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5376340
    > Reviewed-by: Greg Thompson <grt@chromium.org>
    > Reviewed-by: Mark Mentovai <mark@chromium.org>
    > Reviewed-by: Daseul Lee <dslee@chromium.org>
    > Commit-Queue: Daniel Soromou <fosoromo@microsoft.com>
    > Cr-Commit-Position: refs/heads/main@{#1286106}
    
    Bug: 329691615, 40061477
    Change-Id: Ifa47562bea1a43f9218198a6e991975f7af77d68
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5454121
    Reviewed-by: Mark Mentovai <mark@chromium.org>
    Reviewed-by: Greg Thompson <grt@chromium.org>
    Commit-Queue: Daniel Soromou <fosoromo@microsoft.com>
    Cr-Commit-Position: refs/heads/main@{#1287897}

M       base/files/file_util.h
M       base/files/file_util_unittest.cc
M       base/files/file_util_win.cc

https://chromium-review.googlesource.com/5454121


### ap...@google.com (2024-04-18)

Project: chromium/src
Branch: main

commit e00151a08c157db10ed21379f6d05c8e4206177e
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date:   Thu Apr 18 06:17:29 2024

    Revert "Reland "Windows: Implement IsLink""
    
    This reverts commit 0bfea22d30a66f9622e7a211f0a2edb6b9840e32.
    
    Reason for revert: Suspicious for causing FileUtilTest.IsLink* tests to fail again.
    i.e. https://ci.chromium.org/ui/p/chrome/builders/ci/win-chrome/33846/overview
    
    Original change's description:
    > Reland "Windows: Implement IsLink"
    >
    > This is a reland of commit 6bbf3a1af202ac5c0ae24266f4b2e4ace23de8a0.
    >
    > In the previous update, the `FileUtilTest.IsLink*` tests were failing on
    > Windows 10 because the availability of `CreateSymbolicLink` can vary
    > based on several factors, including whether the user has
    > administrative privileges, is in developer mode, or due to Group
    > Policy and User Account Control (UAC) settings.
    >
    > In this reattempt, the tests have been updated to skip cases where
    > `CreateSymbolicLink` fails.
    >
    > Original change's description:
    > > Windows: Implement IsLink
    > >
    > > This CL adds helpers IsLink(...) for symbolic link handling in
    > > the Windows to unblock https://issues.chromium.org/issues/40061477.
    > >
    > > The necessity for the `IsLink` helper arises from a specific
    > > security concern related to file handling during directory traversal.
    > > When a file handle is obtained through `GetFile()` or `GetEntries()`
    > > from a directory handle, there's a possibility that this file handle
    > > represents a symlink file. This symlink could potentially point to a
    > > path that is blocklisted, posing a security risk. Such a scenario might
    > > occur if the symlink file is created after permissions have been
    > > granted to access the parent directory. Although this situation cannot
    > > occur through web API and it's only possible when it done on the local
    > > machine.
    > >
    > > However, the isuse is currently implemented on non-Windows platforms
    > > only, due to the absence of a helper on Windows to detect symlinks.
    > >
    > > Bug: 329691615, 40061477
    > > Change-Id: I32b2f14bf02a096bae693b8867a2690eeffb1c2d
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5376340
    > > Reviewed-by: Greg Thompson <grt@chromium.org>
    > > Reviewed-by: Mark Mentovai <mark@chromium.org>
    > > Reviewed-by: Daseul Lee <dslee@chromium.org>
    > > Commit-Queue: Daniel Soromou <fosoromo@microsoft.com>
    > > Cr-Commit-Position: refs/heads/main@{#1286106}
    >
    > Bug: 329691615, 40061477
    > Change-Id: Ifa47562bea1a43f9218198a6e991975f7af77d68
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5454121
    > Reviewed-by: Mark Mentovai <mark@chromium.org>
    > Reviewed-by: Greg Thompson <grt@chromium.org>
    > Commit-Queue: Daniel Soromou <fosoromo@microsoft.com>
    > Cr-Commit-Position: refs/heads/main@{#1287897}
    
    Bug: 329691615, 40061477
    Change-Id: Ia63a993a87acb3cb3156aeaf236eaad4aa342fe2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5465001
    Auto-Submit: Nidhi Jaju <nidhijaju@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Owners-Override: Nidhi Jaju <nidhijaju@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1289161}

M       base/files/file_util.h
M       base/files/file_util_unittest.cc
M       base/files/file_util_win.cc

https://chromium-review.googlesource.com/5465001


### ap...@google.com (2024-09-19)

Project: chromium/src
Branch: main

commit 04f5edcea73076d0e1a9b0f93c6816c575506efa
Author: Nathan Memmott <memmott@chromium.org>
Date:   Thu Sep 19 14:31:44 2024

    FSA: Re-enable kFileSystemAccessSymbolicLinkCheck
    
    Both kFileSystemAccessSymbolicLinkCheck and
    kFileSystemAccessDirectoryIterationBlocklistCheck were enabled in the
    same CL. Later it was found that the CL introduced breakage in the CrOS
    camera app, so both flags were disabled.
    
    From investigation, it turns that enabling
    kFileSystemAccessDirectoryIterationBlocklistCheck was what caused the
    breakage due to bug https://crbug.com/266019073.
    
    This re-enables kFileSystemAccessSymbolicLinkCheck since it didn't
    introduce the breakage.
    
    Bug: 40061477
    Change-Id: I905f1a19b42b250f6f87b273e6dcb28fcaf9af7d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5858538
    Reviewed-by: Christine Hollingsworth <christinesm@chromium.org>
    Commit-Queue: Christine Hollingsworth <christinesm@chromium.org>
    Auto-Submit: Nathan Memmott <memmott@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1357587}

M       chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc
M       chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc
M       chrome/browser/file_system_access/file_system_access_features.cc

https://chromium-review.googlesource.com/5858538


### ap...@google.com (2024-09-20)

Project: chromium/src
Branch: main

commit ccb5057b2bc07ea7288e185331d9e6d0914c4437
Author: Nathan Memmott <memmott@chromium.org>
Date:   Fri Sep 20 22:33:27 2024

    FSA: Normalize blocked paths before doing blocklist checks
    
    We normalize paths before checking them against the blocklist but the
    paths in the blocklist may not be normalized.
    
    This CL adds logic to normalize the blocked paths.
    
    Bug: 40061477
    Change-Id: I31f6a4a617a79aebbabf2dc08153386496afe8af
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5871321
    Reviewed-by: Christine Hollingsworth <christinesm@chromium.org>
    Commit-Queue: Nathan Memmott <memmott@chromium.org>
    Reviewed-by: Ayu Ishii <ayui@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1358423}

M       chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc
M       chrome/browser/file_system_access/chrome_file_system_access_permission_context_unittest.cc

https://chromium-review.googlesource.com/5871321


### pe...@google.com (2024-10-26)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 400 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-10-28)

Project: chromium/src  

Branch: main  

Author: Nathan Memmott <[memmott@chromium.org](mailto:memmott@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5960800>

FSA: Enable directory iteration blocklist check

---


Expand for full commit details
```
FSA: Enable directory iteration blocklist check 
 
Enables the kFileSystemAccessDirectoryIterationBlocklistCheck to perform 
blocklist checks on calls to GetFile() and GetEntries(). 
 
This was previously disabled due to it causing an issue with the 
ChromeOS camera app. Now that it is fixed, we can re-enable this flag. 
 
Fixed: 40061477 
Change-Id: I0a8d0e975114e88e983afca4ed627260ebde5f87 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5960800 
Reviewed-by: Daseul Lee <dslee@chromium.org> 
Commit-Queue: Nathan Memmott <memmott@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1374690}

```

---

Files:

- M `content/browser/file_system_access/features.cc`

---

Hash: 6739e1899e4782d67fe759d291b3a1e4d333f4dc  

Date:  Mon Oct 28 17:04:17 2024


---

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
thank you for report of issue that falls outside our threat model, but resulted in defense-in-depth hardening work


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Thank you again for this report Axel, and your efforts in reporting this issue to us.

### pe...@google.com (2025-02-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061477)*
