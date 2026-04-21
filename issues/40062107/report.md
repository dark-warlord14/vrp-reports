# Security: ChromeOS Arbitrary Root File Delete

| Field | Value |
|-------|-------|
| **Issue ID** | [40062107](https://issues.chromium.org/issues/40062107) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | al...@google.com |
| **Created** | 2022-12-07 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

When preparing to mount a user's cryptohome, cryptohomed will unsafely recursively delete a directory in a chronos controlled path. A race condition exists to insert symbolic links which can result in the arbitrary deletion of files and directories across the filesystem.

**VERSION**  

Google Chrome 107.0.5304.110 (Official Build) (64-bit)  

Revision 2a558545ab7e6fb8177002bf44d4fc1717cb2998-refs/branch-heads/5304@{#1202}  

Platform 15117.112.0 (Official Build) stable-channel eve  

Firmware Version Google\_Eve.9584.230.0

**REPRODUCTION CASE**  

Execute the attached shell script as follows:

sh <(cat arbitrarydelete.sh)

Observe upon completion the file /run/agetty.reload is deleted. Note that this vulnerability is a race condition and therefore the time to execute can vary greatly. Each period output by the script indicates one iteration, to identify if the script has hung.

(agetty.reload is a file that exists by default on my system, is owned by root and isn't important, so was selected for this proof of concept. Other files can be targeted)

DETAILS  

When cryptohome attempts to mount /home/chronos/u-[hash], it will first delete this directory if it exists [1]. /home/chronos is owned by chronos and therefore this directory can be created before a cryptohome mount request is executed.

The deletion of /home/chronos/u-[hash], if present, is performed by DoDeleteFile, with recursive set to true. When recursive is true, a FileEnumerator is used to identify files inside the target directory to be deleted [2].

If a directory is created /home/chronos/u-[hash]/EXPLOIT, inside which contains a file /home/chronos/u-[hash]/EXPLOIT/agetty.reload, the FileEnumerator will include this file in it's list which is later iterated for deletion [3]. If between the creation of the FileEnumerator [2] and the execution of unlink [3], the /home/chronos/u-[hash]/EXPLOIT directory is replaced with a symbolic link to /run, the unlink will then delete /run/agetty.reload via /home/chronos/u-[hash]/EXPLOIT/agetty.reload.

Since this is a tight race, 1000 directories are created, /home/chronos/u-[hash]/EXPLOIT.0 to /home/chronos/u-[hash]/EXPLOIT.999. When the proof of concept identifies that these directories are being deleted, it will switch all directories for the symbolic link to /run, hopefully resulting in cryptohome traversing these symbolic links while the recursive delete is executed.

This vulnerability is cleanly retriable but quite unreliable, and therefore sometimes a large number of attempts are required to be successful.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/main/cryptohome/storage/mount_helper.cc#382>  

[2] <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/base/files/file_util_posix.cc#301>  

[3] <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/base/files/file_util_posix.cc#309>

Requirements

- None

Impact

- Arbitrary deletion of files and directories across the filesystem. This vulnerability can be used to target single files/directories but can be run repeatedly to delete directory trees.

Recommendation

- Don't perform recursive deletions as root into chronos owned directory trees, at least without SafeFD
- I've exploited FileEnumerator based races a couple of times now (cf 1115662), it may be appropriate to require FileEnumerator usage to be paired with SafeFD

## Attachments

- [arbitrarydelete.sh](attachments/arbitrarydelete.sh) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### be...@google.com (2022-12-07)

+

### be...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### lz...@google.com (2022-12-07)

I am not familiar with FileEnumerator's flag behavior. The SHOW_SYM_LINK flag is on for FileEnumerator. When a directory is a symlink to /run, will FileEnumerator follows the link throught the Next() call? No because the directory is actually becoming a symlink file. So the race is that:
1. FileEnumerator checks a directory D can be traversed.
2. FileEnumerator enters the directory D.
3. FileEnumerator traverses the files of D and starts to call unlink($D/filename) on each file.

if we change the directory D to a symlink of any other directory, between step 2 and 3 the $D/filename is pointing to some other files. 

Not sure if unlinkat() is a better replacement of unlink.

### lz...@google.com (2022-12-07)

To rory, are you referring the SafeFD in https://chromium.googlesource.com/chromiumos/platform2/+/HEAD/libbrillo/brillo/files/safe_fd.h?

### lz...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2022-12-08)

https://crbug.com/chromium/1398990#c6: Yes, it may not be a complete fix but my naive thought is that it should stop some/all symlink attacks in this case, as it can guarantee no symlinks in the entire tree when calling Unlink.

### le...@google.com (2022-12-08)

Assigning to lziest@ for triage

[Monorail components: Security]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-22)

lziest: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-05)

lziest: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@google.com (2023-01-20)

[Empty comment from Monorail migration]

### al...@google.com (2023-01-20)

It looks like the simplest solution is to move the path to a directory owned by root and without the x permission for group/other prior to calling delete.

### al...@google.com (2023-01-20)

I looked a few different options and I am not 100% settled on how I want to fix this yet, but we have options.

### al...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### al...@google.com (2023-03-03)

This doesn't reproduce for me using rmdir directly. I wrote the following minimal PoC:
```
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#include <sys/stat.h>

int main() {
    if (mkdirat(AT_FDCWD, "test-dir", 700)) {
        perror("mkdirat");
        return 1;
    }

    if (symlinkat("test-dir", AT_FDCWD, "to-unlink")) {
        perror("symlinkat");
        return 1;
    }

    if (rmdir("to-unlink")) {
        perror("rmdir");
        return 1;
        if (unlinkat(AT_FDCWD, "to-unlink", 0)) {
            perror("unlinkat('to-unlink')");
            return 1;
        }
    } else {
        if (unlinkat(AT_FDCWD, "to-unlink", 0)) {
            perror("unlinkat('to-unlink')");
        }
    }

    if (unlinkat(AT_FDCWD, "test-dir", AT_REMOVEDIR)) {
        perror("unlinkat");
        return 1;
    }


    return 0;
}

```

It returns:
```
localhost /tmp # /usr/local/bin/rmdir_test 
rmdir: Not a directory
```

Furthermore if I look for the symlink and its target, both are still there:
d-w-r-xr-T.  2 root    root        40 Mar  3 09:34 test-dir
lrwxrwxrwx.  1 root    root         8 Mar  3 09:34 to-unlink -> test-dir



### al...@google.com (2023-03-03)

I will try this again on 107 Eve when I get a chance in case it was fixed by a libc upgrade, or by a newer kernel.

### ro...@rorym.cnamara.com (2023-03-03)

https://crbug.com/chromium/1398990#c22: The expectation is the symlink is part of the path, not the final component, e.g /a/b/c where b is a symlink and c is to-be-deleted. In the above PoC the EXPLOIT directory is a symlink and .../EXPLOIT/agetty.reload is the deletion target.

### al...@google.com (2023-03-03)

Thanks. I will update the test case accordingly

### al...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### al...@google.com (2023-03-06)

[Empty comment from Monorail migration]

### al...@google.com (2023-03-06)

Here is a possible fix, but we would still probably need to move other usage of libchrome's DeletePath and DeleteFile over to the newer functions in libbrillo.

We could see if libchrome would pick up the fixed versions, but that is a harder sell because Chrome doesn't have to worry about UID privilege escalation (except maybe in user namespaces).

### al...@google.com (2023-03-06)

https://crrev.com/c/4310162

### gi...@appspot.gserviceaccount.com (2023-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/b8a5d418ef2f67a5864a28cf9cc5bcb31c46e4b9

commit b8a5d418ef2f67a5864a28cf9cc5bcb31c46e4b9
Author: Allen Webb <allenwebb@google.com>
Date: Wed Mar 08 16:51:51 2023

libbrillo: SafeFD ignore some ENOENT during recursive Rmdir

This does not return an error when ENOENT is encountered for contents
during a recursive Rmdir. We do not want ENOENT for contents being
conflated with ENOENT for the target directory. This should make this
less prone to failure when multiple processes are deleting overlapping
paths.

This also stops logging errors when Rmdir is called for a file since
that is an expected case in brillo::DeleteFile.

BUG=chromium:1398990
TEST=FEATURES=test emerge libbrillo

Change-Id: I3d8ceba935d3133f41c2837aff3caf4d4c636050
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4320545
Reviewed-by: Brian Norris <briannorris@chromium.org>
Tested-by: Allen Webb <allenwebb@google.com>
Commit-Queue: Allen Webb <allenwebb@google.com>

[modify] https://crrev.com/b8a5d418ef2f67a5864a28cf9cc5bcb31c46e4b9/libbrillo/brillo/files/safe_fd.cc


### gi...@appspot.gserviceaccount.com (2023-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/8339d508458a112770e7864b0f784dbe33df7ec0

commit 8339d508458a112770e7864b0f784dbe33df7ec0
Author: Allen Webb <allenwebb@google.com>
Date: Fri Mar 03 22:20:23 2023

libbrillo: Provide alternatives to base::Delete*

Use SafeFD rather than libchrome's delete operations because its recursion
is prone to ToCToU races.

BUG=chromium:1398990
TEST=FEATURES=test emerge-${BOARD} libbrillo cryptohome

Change-Id: Ide700990a3f5dee9399c17ff7da7853329511e8b
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4310162
Reviewed-by: Brian Norris <briannorris@chromium.org>
Tested-by: Allen Webb <allenwebb@google.com>
Commit-Queue: Allen Webb <allenwebb@google.com>

[modify] https://crrev.com/8339d508458a112770e7864b0f784dbe33df7ec0/libbrillo/brillo/files/file_util_test.cc
[modify] https://crrev.com/8339d508458a112770e7864b0f784dbe33df7ec0/libbrillo/brillo/files/file_util.h
[modify] https://crrev.com/8339d508458a112770e7864b0f784dbe33df7ec0/libbrillo/brillo/files/file_util.cc


### gi...@appspot.gserviceaccount.com (2023-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/2304204086d92dc10d8921cf5d3acc8770018075

commit 2304204086d92dc10d8921cf5d3acc8770018075
Author: Allen Webb <allenwebb@google.com>
Date: Fri Mar 03 19:15:03 2023

cryptohome: Swap out base::Delete* with brillo::Delete*

Use SafeFD rather than libchrome to do delete operations because
recursion is prone to ToCToU races.

BUG=chromium:1398990
TEST=FEATURES=test emerge-${BOARD} cryptohome

Change-Id: Ic7ad683e0feefa60db37296be56c028baa4a5ce8
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4310163
Reviewed-by: Sarthak Kukreti <sarthakkukreti@google.com>
Tested-by: Allen Webb <allenwebb@google.com>
Commit-Queue: Allen Webb <allenwebb@google.com>
Reviewed-by: John Admanski <jadmanski@chromium.org>

[modify] https://crrev.com/2304204086d92dc10d8921cf5d3acc8770018075/cryptohome/platform.cc


### al...@google.com (2023-03-09)

We still need to clean up other useage of base::DeletePathRecursively(), but we could probably track that in a follow-up bug and mark this as fixed.

### al...@google.com (2023-03-09)

The follow-up is tracked in b/272503861

### al...@google.com (2023-03-09)

[Empty comment from Monorail migration]

[Monorail blocking: b/272503861]

### al...@google.com (2023-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

[Empty comment from Monorail migration]

### vo...@google.com (2023-03-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations Rory! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### ro...@rorym.cnamara.com (2023-03-17)

Thank you!

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### rz...@google.com (2023-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-29)

1. 3 CLs https://chromium-review.googlesource.com/q/topic:%221398990%22
2. Low, only a simple conflict with a check not present in 108 branch
3. 113
4. Yes

### gm...@google.com (2023-03-30)

[Empty comment from Monorail migration]

### gm...@google.com (2023-05-12)

This is a medium, Further delaying until new policy is approved.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-06-20)

[Empty comment from Monorail migration]

### gm...@google.com (2023-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/0e6669bf12ed6746db111a172f513b59024196a1

commit 0e6669bf12ed6746db111a172f513b59024196a1
Author: Allen Webb <allenwebb@google.com>
Date: Fri Mar 03 22:20:23 2023

[M108-LTS] libbrillo: Provide alternatives to base::Delete*

Use SafeFD rather than libchrome's delete operations because its recursion
is prone to ToCToU races.

BUG=chromium:1398990
TEST=FEATURES=test emerge-${BOARD} libbrillo cryptohome

Change-Id: Ide700990a3f5dee9399c17ff7da7853329511e8b
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4310162
Tested-by: Allen Webb <allenwebb@google.com>
Commit-Queue: Allen Webb <allenwebb@google.com>
(cherry picked from commit 8339d508458a112770e7864b0f784dbe33df7ec0)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4359700
Reviewed-by: Allen Webb <allenwebb@google.com>
Tested-by: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>

[modify] https://crrev.com/0e6669bf12ed6746db111a172f513b59024196a1/libbrillo/brillo/files/file_util_test.cc
[modify] https://crrev.com/0e6669bf12ed6746db111a172f513b59024196a1/libbrillo/brillo/files/file_util.h
[modify] https://crrev.com/0e6669bf12ed6746db111a172f513b59024196a1/libbrillo/brillo/files/file_util.cc


### gi...@appspot.gserviceaccount.com (2023-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/16a89e616b763ed03b758202816bb83a0d62e144

commit 16a89e616b763ed03b758202816bb83a0d62e144
Author: Allen Webb <allenwebb@google.com>
Date: Wed Mar 08 16:51:51 2023

[M108-LTS] libbrillo: SafeFD ignore some ENOENT during recursive Rmdir

This does not return an error when ENOENT is encountered for contents
during a recursive Rmdir. We do not want ENOENT for contents being
conflated with ENOENT for the target directory. This should make this
less prone to failure when multiple processes are deleting overlapping
paths.

This also stops logging errors when Rmdir is called for a file since
that is an expected case in brillo::DeleteFile.

BUG=chromium:1398990
TEST=FEATURES=test emerge libbrillo

Change-Id: I3d8ceba935d3133f41c2837aff3caf4d4c636050
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4320545
Tested-by: Allen Webb <allenwebb@google.com>
Commit-Queue: Allen Webb <allenwebb@google.com>
(cherry picked from commit b8a5d418ef2f67a5864a28cf9cc5bcb31c46e4b9)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4359701
Tested-by: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Allen Webb <allenwebb@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>

[modify] https://crrev.com/16a89e616b763ed03b758202816bb83a0d62e144/libbrillo/brillo/files/safe_fd.cc


### gi...@appspot.gserviceaccount.com (2023-06-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/6f2ae84fa6cdafb82021a366ae899db3e1749d21

commit 6f2ae84fa6cdafb82021a366ae899db3e1749d21
Author: Allen Webb <allenwebb@google.com>
Date: Fri Mar 03 19:15:03 2023

[M108-LTS] cryptohome: Swap out base::Delete* with brillo::Delete*

M108 merge issues:
  The path DCHECKs from the original change aren't present in 108.
  Kept the 108 code without the DCHECKs but applied the fixes.

Use SafeFD rather than libchrome to do delete operations because
recursion is prone to ToCToU races.

BUG=chromium:1398990
TEST=FEATURES=test emerge-${BOARD} cryptohome

Change-Id: Ic7ad683e0feefa60db37296be56c028baa4a5ce8
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4310163
Tested-by: Allen Webb <allenwebb@google.com>
Commit-Queue: Allen Webb <allenwebb@google.com>
(cherry picked from commit 2304204086d92dc10d8921cf5d3acc8770018075)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4359702
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Allen Webb <allenwebb@google.com>
Tested-by: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>

[modify] https://crrev.com/6f2ae84fa6cdafb82021a366ae899db3e1749d21/cryptohome/platform.cc


### rz...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/3b8566c5d1273ddc2bfb2233ba969eb0309308db

commit 3b8566c5d1273ddc2bfb2233ba969eb0309308db
Author: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Date: Thu Jun 29 07:51:19 2023

Revert "[M108-LTS] libbrillo: SafeFD ignore some ENOENT during recursive Rmdir"

This reverts commit 16a89e616b763ed03b758202816bb83a0d62e144.

Reason for revert: Requested by RM

Original change's description:
> [M108-LTS] libbrillo: SafeFD ignore some ENOENT during recursive Rmdir
>
> This does not return an error when ENOENT is encountered for contents
> during a recursive Rmdir. We do not want ENOENT for contents being
> conflated with ENOENT for the target directory. This should make this
> less prone to failure when multiple processes are deleting overlapping
> paths.
>
> This also stops logging errors when Rmdir is called for a file since
> that is an expected case in brillo::DeleteFile.
>
> BUG=chromium:1398990
> TEST=FEATURES=test emerge libbrillo
>
> Change-Id: I3d8ceba935d3133f41c2837aff3caf4d4c636050
> Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4320545
> Tested-by: Allen Webb <allenwebb@google.com>
> Commit-Queue: Allen Webb <allenwebb@google.com>
> (cherry picked from commit b8a5d418ef2f67a5864a28cf9cc5bcb31c46e4b9)
> Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4359701
> Tested-by: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Reviewed-by: Allen Webb <allenwebb@google.com>
> Reviewed-by: Jana Grill <janagrill@google.com>

BUG=chromium:1398990

Change-Id: Ie11a45c9c11a23024a7606347a24acf61d9732ad
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4650684
Reviewed-by: Jana Grill <janagrill@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>

[modify] https://crrev.com/3b8566c5d1273ddc2bfb2233ba969eb0309308db/libbrillo/brillo/files/safe_fd.cc


### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/bbf326db3b8d1742f7aa9c1eefc9d97d7957cb56

commit bbf326db3b8d1742f7aa9c1eefc9d97d7957cb56
Author: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Date: Thu Jun 29 07:51:46 2023

Revert "[M108-LTS] cryptohome: Swap out base::Delete* with brillo::Delete*"

This reverts commit 6f2ae84fa6cdafb82021a366ae899db3e1749d21.

Reason for revert: Requested by RM

Original change's description:
> [M108-LTS] cryptohome: Swap out base::Delete* with brillo::Delete*
>
> M108 merge issues:
>   The path DCHECKs from the original change aren't present in 108.
>   Kept the 108 code without the DCHECKs but applied the fixes.
>
> Use SafeFD rather than libchrome to do delete operations because
> recursion is prone to ToCToU races.
>
> BUG=chromium:1398990
> TEST=FEATURES=test emerge-${BOARD} cryptohome
>
> Change-Id: Ic7ad683e0feefa60db37296be56c028baa4a5ce8
> Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4310163
> Tested-by: Allen Webb <allenwebb@google.com>
> Commit-Queue: Allen Webb <allenwebb@google.com>
> (cherry picked from commit 2304204086d92dc10d8921cf5d3acc8770018075)
> Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4359702
> Owners-Override: Jana Grill <janagrill@google.com>
> Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Reviewed-by: Allen Webb <allenwebb@google.com>
> Tested-by: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Reviewed-by: Jana Grill <janagrill@google.com>

BUG=chromium:1398990

Change-Id: I7a213fed875d2617621da3089d5bdcef58673984
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4650685
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/bbf326db3b8d1742f7aa9c1eefc9d97d7957cb56/cryptohome/platform.cc


### gi...@appspot.gserviceaccount.com (2023-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/c96dc92cb65cffe43337875eb80ae35e6737095e

commit c96dc92cb65cffe43337875eb80ae35e6737095e
Author: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Date: Thu Jun 29 07:50:42 2023

Revert "[M108-LTS] libbrillo: Provide alternatives to base::Delete*"

This reverts commit 0e6669bf12ed6746db111a172f513b59024196a1.

Reason for revert: Requested by RM

Original change's description:
> [M108-LTS] libbrillo: Provide alternatives to base::Delete*
>
> Use SafeFD rather than libchrome's delete operations because its recursion
> is prone to ToCToU races.
>
> BUG=chromium:1398990
> TEST=FEATURES=test emerge-${BOARD} libbrillo cryptohome
>
> Change-Id: Ide700990a3f5dee9399c17ff7da7853329511e8b
> Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4310162
> Tested-by: Allen Webb <allenwebb@google.com>
> Commit-Queue: Allen Webb <allenwebb@google.com>
> (cherry picked from commit 8339d508458a112770e7864b0f784dbe33df7ec0)
> Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4359700
> Reviewed-by: Allen Webb <allenwebb@google.com>
> Tested-by: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Reviewed-by: Jana Grill <janagrill@google.com>

BUG=chromium:1398990

Change-Id: Ia905a3bca34a0f6f14442f405111dacf8c01550d
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4650683
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>

[modify] https://crrev.com/c96dc92cb65cffe43337875eb80ae35e6737095e/libbrillo/brillo/files/file_util_test.cc
[modify] https://crrev.com/c96dc92cb65cffe43337875eb80ae35e6737095e/libbrillo/brillo/files/file_util.h
[modify] https://crrev.com/c96dc92cb65cffe43337875eb80ae35e6737095e/libbrillo/brillo/files/file_util.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1398990?no_tracker_redirect=1

[Monorail blocking: b/272503861]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062107)*
