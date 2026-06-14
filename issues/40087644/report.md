# Security: Chrome ᴏꜱ buffer overflow in mount.exfat-fuse after a call to malloc(0)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087644](https://issues.chromium.org/issues/40087644) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **CVE IDs** | CVE-2015-8026 |
| **Reporter** | la...@gmail.com |
| **Assignee** | be...@chromium.org |
| **Created** | 2017-05-14 |
| **Bounty** | $3,000.00 |

## Description

ATTACK SCENARIO  

This kind of vulnerability is best suited for targeting a single person since an exploit can only work on a single vendor firmware, but here’s the steps :  

An ꜱᴅ card is dropped on a car park. Preferably a large ꜱᴅ card (1Tb) in it’s vendor plastic and it’s several hundred dollars price on it.  

The digitally illiterate user who don’t known what formatting a device or hidden files is, will just delete the family pictures and films he sees the disks that appear in the file manager of chrome ᴏꜱ. Then, the user will use the ꜱᴅ card for his own needs until the day one of the partition containing an exploit chain trigger the persistence exploit.

As chrome ᴏꜱ doesn’t offer partitioning tools, the user won’t delete the partitions that don’t appear (if mount.exfat-fuse crash on startup then the exfat partition doesn’t appear in the file manager but ccros-disk will always automatically mount all partition a device contains anyway, even if there’s more than one hundred)

**VULNERABILITY DETAILS**  

mount.exfat-fuse before <https://github.com/relan/exfat/commit/38d5c3a929124fd123675ac576401b7de3570b2f> didn’t checked sector and cluster size in the correct order.  

In some circumstances, ef->zero\_cluster = malloc(CLUSTER\_SIZE(\*ef->sb)) in mount.c line 211 can turn into a call to malloc(0) while SECTOR\_SIZE(\*ef->sb) line 220 return a larger attacker controlled size.  

Posix requires malloc(0) to create a unique pointer that can be passed to free() (<http://www.unix.com/man-page/POSIX/3posix/malloc/>). In practice glibc will create a unique pointer pointing to an allocated area of 12 bytes on 32 bits and 24 bytes on 64 bits.  

It’s also worth noting such pointer isn’t randomized relative to the beginning of the heap.

The overwriting of dlmalloc data happens in verify\_vbr\_checksum() located in mount.c.  

The attacker doesn’t have fine grained control over the exact size returned by SECTOR\_SIZE(\*ef->sb), but pread() can succeed while returning less bytes than requested and thus overwriting less dlmalloc data (mount.exfat-fuse doesn’t check the amount of data returned by pread). This can be achieved by reducing the size of the partition.  

The attack in the libc begin when mount.exfat-fuse will complain and try to print an error message. This will call several glibc functions which will call vfprintf which will allocate data and read a damaged heap.

There’s 2 repeating factor that can overcome ᴀꜱʟʀ : the fact that cros-disk will automatically mount filesystems instead of doing it on request in the file manager and the exploits only takes bytes which allows to have more than one hundred partitions on the device which will be all mount attempted. As long as they crash mount.exfat-fuse, they won’t show up in the file manager and the user cannot format them without using command line (provided he/she even knows what command line interface is)

**VERSION**  

I’m not aware of a version or device not affected above 25.0.1364.126 (<https://chromium.googlesource.com/chromiumos/platform2/+/af455a08a8de7d88cd9550d2d63c865a7c3fc69f>).

**REPRODUCTION CASE**  

I repeatedly tried to run the real Chrome ᴏꜱ, but all my attempts failed. As the size of the libraries used determine partially the organization of the stack and the heap I can’t build successful exploit that would run outside my Debian Linux install. So the only thing I can provide is a ᴘᴏᴄ demontrating a partial or full pointer overwrite with attacker controlled data (it bypass glibc buffer detection algorithm see annotated attachment), so this allow writing to arbitrary address.  

In order to run the ᴘᴏᴄ, you can use this command as root under developer mode :  

mount.exfat-fuse "ᴀᴍᴅ⁶⁴ ᴘᴏᴄ for Chrome ᴏꜱ" /media/removable/archive

There’s three ways to launch a hidden file script as root which will perform a downgrade to a previously valid version allowing mitigated persistence exploits to work again (take a look at the attachments For obvious reason I can’t put a rootfs in those attachements) :  

— The 1ˢᵗ is to call setreuid(0,0) as SECBIT\_NOROOT is not set, next call to execve will allow to gain full superuser capabilities. Partitions are mounted with noexec : to overcome this, the executable that will be called is /bin/bash with the path to the downgrade script called .s as argument (it’s important for paths to take as less space as possible in the exploit)

— The 2ⁿd consists to call the mount() system call directly to mount a filesystem containing the binaries of /sbin but with a modified chromeos\_shutdown script (since no execve system call is performed while the user is logged in) that will install the downgrade images located in the same directory (it requires the user to withdraw the ꜱᴅ card only after shutting down the computer). As I couldn’t ran Chrome ᴏꜱ, I couldn’t determine if /media/removable folder where unmounted on logoff. So the mount system call needs to use a block device, that is, a partition on the ꜱᴅ card with a filesystem that won’t be mounted by cros-disk. This require a file system type supported by the kernel but not by cros-disk which leave squashfs as the only option. Of course, in that case the file manager propose to erase the device but this can be mitigated by write protecting the partition through the controller located on the ꜱᴅ card.

## Attachments

- [ᴀᴍᴅ⁶⁴ ᴘᴏᴄ for Chrome ᴏꜱ](attachments/ᴀᴍᴅ⁶⁴ ᴘᴏᴄ for Chrome ᴏꜱ) (text/plain, 116 B)
- [core](attachments/core) (text/plain, 508.0 KB)
- [annotated malloc for arbitrary address write by fetching partially corrupted pointer from heap.c](attachments/annotated malloc for arbitrary address write by fetching partially corrupted pointer from heap.c) (text/plain, 14.1 KB)
- [second partition containing script data in the case of setresuid(0,0) in the ʀᴏᴘ chain.vfat](attachments/second partition containing script data in the case of setresuid(0,0) in the ʀᴏᴘ chain.vfat) (application/octet-stream, 64.0 KB)
- [partition block device that should be mounted over sbin containing modified chromeos_shutdown script and old firmware.squashfs](attachments/partition block device that should be mounted over sbin containing modified chromeos_shutdown script and old firmware.squashfs) (application/octet-stream, 2.8 MB)
- [chromiumos-overlay.patch](attachments/chromiumos-overlay.patch) (application/octet-stream, 3.8 KB)

## Timeline

### in...@chromium.org (2017-05-15)

benchan@, can you please help to triage.

[Monorail components: OS>Systems]

### la...@gmail.com (2017-05-15)

Please note I won’t buy a Chromebook as I already have a more powerful netbook and there’s no rental service for that in my country.

### la...@gmail.com (2017-05-15)

[Comment Deleted]

### be...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### be...@chromium.org (2017-05-15)

CVE-2015-8026 seems to be related

### la...@gmail.com (2017-05-15)

Yes but I studied exploitability and preve it is possilble to bypass glibc's bufer overflow detection mechanism. In both cases, things are fixed upstream for a long time.

### be...@chromium.org (2017-05-16)

re #6: Thanks for disclosing the issue and providing the detailed information. We're working on fixes to address the issue.

### in...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

### la...@gmail.com (2017-05-16)

I am willing to write any fixes within hours. They were several ways to fix this so I could not write other things than the upgrade patch.

### mn...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

### be...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

### la...@gmail.com (2017-05-17)

Would it be possible to get access to the blockedon bugs?

### be...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### be...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### be...@chromium.org (2017-05-17)

https://crbug.com/chromium/723102 is about updating fuse-exfat and exfat-utils

### la...@gmail.com (2017-05-17)

and 722946?

### jo...@chromium.org (2017-05-17)

722946 is about further restricting the environment of the mount helpers.

### la...@gmail.com (2017-05-17)

I checked about seccomp and found the set of system calls in not fixed accross version. Anyway, as the reported, I would like to participate in fixing 722946

### la...@gmail.com (2017-05-21)

[Comment Deleted]

### la...@gmail.com (2017-05-21)

Also, what about the automatic downgrade exploit ?
I fully detailed things line by line inside the scripts

### la...@gmail.com (2017-06-06)

He helped me on the idea to use squashfs

### la...@gmail.com (2017-06-06)

[Comment Deleted]

### la...@gmail.com (2017-06-06)

[Comment Deleted]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### be...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### la...@gmail.com (2017-06-06)

Sorry, but does the bug is currently eligible for reward?

### jo...@chromium.org (2017-06-06)

We should send it to the panel.

### sh...@chromium.org (2017-06-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-09)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@gmail.com (2017-06-10)

Please note this was just a question.
I do not want to be paid for what I have already found if it prevent me from getting $100,000 reward for the full exploit chain later (minus what I would have already earned for what I already found).
The answer is yes otherwise.

### jo...@chromium.org (2017-06-14)

What is the CL that needs to be merged here?

### jo...@chromium.org (2017-06-19)

ping for the CL?

### jo...@chromium.org (2017-06-21)

Fix was merged to 59 in https://bugs.chromium.org/p/chromium/issues/detail?id=723102.

### jo...@chromium.org (2017-06-24)

ok, approving this one for m60 

### jo...@chromium.org (2017-06-27)

Pretty sure the original CLs landed in time for M60.

### be...@chromium.org (2017-06-27)

The CL landed in M60 and merged to M59.

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

Congratulations lael.cellier@ - the VRP panel has decided to award $3,000 for the report. A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-06-27)

Also, how would you like to be credited if this bug is included in future Chrome release notes?

### la...@gmail.com (2017-06-27)

Just credit it to me : Laël Cellier.

But as stated, I don’t want reward if it further prevent me from getting the full reward (minus 3000 on full Attack chain later)

### la...@gmail.com (2017-06-27)

Is it the case ?

### la...@gmail.com (2017-06-27)

Oh, I forget, please also credit it to Baptiste Cellier

### jo...@chromium.org (2017-06-27)

Andrew can confirm/correct me but I don't think we've ever blocked a full exploit chain on the grounds that a previous bug reported by the same person had already been rewarded. I don't recall if the reward amounts change, but we always try to reward good bugs.

### aw...@chromium.org (2017-06-27)

Correct - we don't want to incentive people to hold on to bugs in hope of a larger payout if they delay reporting it to us.  We'd do the right thing.

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/722126?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/722946, crbug.com/chromium/723102]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087644)*
