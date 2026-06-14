# Security: ChromeOS root privilege escalation and persistence

| Field | Value |
|-------|-------|
| **Issue ID** | [40052058](https://issues.chromium.org/issues/40052058) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | mn...@chromium.org |
| **Created** | 2020-04-19 |
| **Bounty** | $45,000.00 |

## Description

**VULNERABILITY DETAILS**  

Via Cups, arc-setup, and udev it is possible for command execution as chronos to escalate privileges to unconstrained root. Persistence can also be achieved using the signed device policy.

This chain has been tested in dev mode from crosh, but I do not believe any non-dev security changes will impact the chain.

As is, this chain will not work from guest mode, since the guest user is used as part of the chain. If either of the following actions can be performed, I believe that it will be possible from guest mode also but I was unable to find these methods:

- Unmount a specific user’s cryptohome. UnmountEx will unmount all, including the current user which will break their session.
- Remount the current user’s cryptohome without the credentials. This would allow the use of UnmountEx  
  
  The Guest user is used because their Cryptohome can be mounted and unmounted independently (described below), but if another user can be mounted and unmounted independently then this user could be used instead.

**VERSION**  

81.0.4044.103 (Official Build) (64-bit)  

Platform 12871.76.0 (Official Build) stable-channel eve  

Firmware Version Google\_Eve.9584.195.0

**REPRODUCTION CASE**  

=== Repro requirement: OpenSSH server ===  

To automatically exploit the entire chain, you’ll need an ssh server that your ChromeOS device can access. It will need to run a patched sftp-server and have key login enabled, with the keys inserted into the shell script.  

The attached patch should be applied to OpenSSH commit c593cc5e826c9f4ec506e22b629d37cabfaacff9. It’s not strictly necessary to use the entire new SSH, only sftp-server is relevant. I modified my laptop SSH server sshd\_config to include:  

Subsystem sftp /home/rory/cros/openssh/sftp-server  

Which was the location of the compiled patched binary.  

Once up and running, the SSH\_USER and SSH\_HOST variables should be updated in privesc.sh (or privesc.sh.pre). SSH\_KEY should be the base64 encoded private key which will allow passwordless login on SSH\_HOST as SSH\_USER.

I think that it would be possible to use the penguin container in the VM to exploit this, but as far as I can tell this would only work while the user is logged in (so won't work as part of the persistence step), so an internet connection would be necessary to exploit this chain automatically.

=== Repro steps ===  

Run privesc.sh as chronos. To bypass the shell scripts on noexec mounts error, run:

sh <(cat privesc.sh) $PWD/privesc.sh patchpolicy

This must also be done from bash (crosh shell) so <() works.  

Other options for the second argument (patchpolicy) include ‘interactive’ for a root shell (sshd is executed as root in both cases). The path to the script as the first argument is required by patchpolicy to make a copy for the persistence.  

In all cases an ssh server will be started on port 1337, with the passwordless root ssh key available at /tmp/ssh\_host\_rsa\_key

DETAILS  

=== Cups cmdexec ===  

FoomaticRIPCommandLine in a ppd will be executed by bash -c when something is printed. Command execution is as cups:root, standard cups minijail. This option is used by the first printer available in the printer dialog dropdown (Anitech M24).

The following path permissions (used later) are relevant to this resultant access:  

drwxrwx--t. 3 root root 4096 Apr 15 20:57 /home/root  

--w--w----. 1 root root 4096 Apr 18 12:33 /sys/devices/pci0000:00/0000:00:00.0/remove  

--w--w----. 1 root root 4096 Apr 18 12:33 /sys/devices/pci0000:00/0000:00:00.0/rescan

=== Creating unmounted Guest Cryptohome directories ===  

Guest /home/root/[hash] and /home/user/[hash] can be created, unmounted, with the following procedure:  

MountEx guest ephemerally  

Create a random username, break future mounting by touching /home/chronos/u-[user hash]  

MountEx the new random username.  

The mount will fail due to step 2 [1], and the Guest ephemeral mount will also have been unmounted, as unmount of Guest [2] happens before the check that the new user’s directories can be used [3]. The exact AuthorizationRequest and MountRequest protobufs are shown in privesc.sh.

/home/user is only writable by root:root but the hash directory must exist for running StartSession later. /home/root/[hash] when unmounted can be removed by arc-remove-data and recreated by cups for use with the root file write later.

[1] <https://chromium.googlesource.com/chromiumos/platform/cryptohome/+/refs/heads/master/mount.cc#1719>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cryptohome/service.cc#2633>  

[3] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cryptohome/service.cc#2707> MountCryptohome -> MountCryptohomeInner -> EnsureCryptohome -> EnsureUserMountPoints

=== Root rm -rf ===  

arc-stale-directory-remover performs an rm -rf against /home/root/${CHROMEOS\_USER}/android-data-old/\* after arc-remove-data has been executed. Since arc-remove-data can be run by chronos via dbus, CHROMEOS\_USER is controllable, and the rm -rf will traverse a symlink at android-data-old if present. [1]  

This is used to delete the /home/root/[guest hash] directory so cups can modify it (by default it’s owned by root:root in a sticky dir so cups can’t modify)

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/scripts/arc-stale-directory-remover.conf#27>

=== Root file write ===  

The arc-remove-data upstart job (launchable by chronos), performs a directory copy from /home/root/[cryptohome hash]/android-data/ to /home/root/[cryptohome hash]/android-data-old/android-data\_[random]. [1] [2]. In master this job is in a mount namespace restricted to /home/root, and therefore arc-remove-data is used here to make a backup of the current user’s cryptohome only. Arc-remove-data imports the CHROMEOS\_USER variable from dbus, and therefore chronos can target this copy against any /home/root/[hash] directory. [3]

OnBootContinue also performs a directory copy using the same function (MoveDirIntoDataOldDir) in DeleteUnusedCacheDirectory [4] without a jail. OnBootContinue can be triggered by chronos for a specific user hash by calling the following sessionmanager dbus functions: StartSession (takes a username), StopArcInstance, StartArcMiniContainer, UpgradeArcContainer (takes a username in the protobuf). Similar to the above, the username specification allows the copy to target any /home/root/[hash] directory.

In short:  

arc-remove-data moves /home/root/[hash]/android-data to /home/root/[hash]/android-data-old/android-data\_XXXXXX in a mount jail.  

OnBootContinue moves /home/root/[hash]/android-data/cache to /home/root/[hash]/android-data-old/android-data\_XXXXXX unjailed.

No symlink validation is performed against this copy, and there is a race condition for files copied from android-data to android-data-old/android-data\_[random].

It is possible to reliably win this race condition by creating a symlink from android-data-old to a mounted sshfs drive, and using a patched sftp-server to bypass the sshfs follow\_symlinks option.

follow\_symlinks is a client side option which controls whether stat or lstat opcodes are sent to the ssh server. The ssh server is free to ignore this request and provide results for either stat/lstat. By default follow\_symlinks exclusively uses ‘stat’, such that symlinks appear to the client as the file to which they point rather than a symlink. If the server does not honour the client request and instead returns the result for lstat, the client will see a symlink rather than a regular file. The result is that symlinks are therefore possible inside an sshfs mount even with follow\_symlinks set.

By patching sftp-server on a controlled server, it’s possible to return a symlink lstat for the target of a file which arc-setup is about to copy. Therefore when arc-setup attempts to copy (e.g) android-data/EXPLOIT to android-data-old/android-data\_XXXXXX/EXPLOIT, the server indicates that the target is a symlink, which arc-setup will follow and perform an arbitrary file write. [5]

Since the filesystem access is over sshfs, and therefore controlled by our patched server, the race condition is now no longer racey.

Arc-remove-data can be used to move files around /home/root in a less controlled manner (the random android-data\_XXXXX can’t be touched).  

OnBootContinue can be used to move files anywhere using a double symlink to the sshfs and from the sshfs to any file.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/HEAD/arc/setup/arc_setup.cc#2221>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/HEAD/arc/setup/arc_setup_util.cc#659>  

[3] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/scripts/arc-remove-data.conf#18>  

[4] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/setup/arc_setup.cc#2164>  

[5] <https://chromium.googlesource.com/chromium/src/+/master/base/files/file_util_posix.cc#284>

=== File write command execution ===  

/run/udev/data contains udev variables.  

The default 50-udev-default.rules rules file will execute the variable REMOVE\_CMD when a udev managed device is removed [1]

We can pick a device, e.g ‘pci:0000:00:00.0’, replace its data file to include a REMOVE\_CMD of our own.

We can now trigger the removal of this device since /sys/devices/pci0000:00/0000:00:00.0/remove is --w--w---- root:root (ie writable by gid root, which we have via cups)

Writing ‘1’ to that file via cups will trigger the udev REMOVE\_CMD, giving unconstrained root command execution via udev.

[1] <https://github.com/systemd/systemd/blob/6281c6e56c51f45edbf41a83fd13c9d290f6a691/rules.d/50-udev-default.rules.in#L4>

=== Persistence ===  

Although the policy at /var/lib/whitelist/policy.\* contains a signature, the signature is not validated by login\_manager before it uses the start\_up\_flags (PolicyFetchResponse.policy\_data.policy\_value.start\_up\_flags.flags[]). These flags are applied to the pre-login Chrome instance, and supports flags such as --gpu-launcher. This is a command line prefix which can be used to execute gpu processes in e.g a debugger.  

By patching this flag into the current policy file in /var/lib/whitelist/, the flags will take effect on next ui restart (ie logout, reboot). --gpu-launcher can give chronos command execution on reboot. Since the signature is no longer valid, login is not possible, but since command execution has already begun, the privesc above can be re-used to restore the unmodified policy and restart the ui upstart job.  

It’s probably possible to obtain the keys and validly sign this policy, however it was not deemed necessary since this exploitation path is functional, and shows slightly higher impact as a naive root file write could be used to modify the policy without needing full access to the key data.

A C++ program was built (patchpolicy) to apply a flag passed as an argument to the policy file also passed as an argument.

=== Step by step exploitation walkthrough of privesc.sh: ===  

create\_guest\_dirs():

1. MountEx Guest cryptohome as ephemeral
2. Generate a random username and touch /home/chronos/u-[salted username hash]
3. MountEx the new user. This will fail, but unmount the Guest cryptohome.  
   
   viacups stage\_backup(), trigger\_ard():
4. If we’re logged in (ie not on boot), use arc-remove-data symlinks to recursively copy /home/root/${CROS\_USER\_ID\_HASH} to /home/root/.${CROS\_USER\_ID\_HASH} (note the dot). This is just for user data backup. By making android-data-old relative to the android-data symlink, we can protect the copied data from arc-stale-directory-remover, as arc-remove-data will remove the android-data symlink as it’s last step, breaking the android-data-old symlink.  
   
   brute\_empty\_hash():
5. Bruteforce a username for which the hashed user id lexigraphically sorts after the guest hash. This is so that when we perform rm -rf /home/root/\* later, we can keep the symlink android-data-old -> /home/root around long enough to wipe out the guest directory (since the rm -rf will eventually include the parent directory of android-data-old)  
   
   viacups stage\_empty():
6. Using cups command execution, stage the brute forced user’s /home/root/[hash] directory such that /home/root/[hash]/android-data-old is a symlink which points to /home/root/.  
   
   trigger\_ard()
7. Trigger arc-remove-data, which will then trigger arc-stale-directory-remover, which will rm -rf /home/root/\* lexigraphically up to the brute forced user, and wiping out the guest user hash directory. This may also wipe out the current user’s cryptohome mount (but not the mount directory), hence the backup in step 4. The rm -rf \* will not impact dot directories (the backup).  
   
   mount\_sshfs():
8. Mount the malicious ssh server via cros-disks sshfs  
   
   viacups stage\_overwrite():
9. Using cups command execution, re-create and stage the guest user’s /home/root/[hash] directory, /home/root/[hash]/android-data/cache is created and a file named ‘EXPLOIT’ is created containing the to-be-overwitten file contents. The contents to be written is a E:REMOVE\_CMD line which launches sshd. ‘EXPLOIT’ here maps to ‘EXPLOIT’ used to trigger the symlink lstat in the sftp-server. /home/root/[hash]/android-data-old is a symlink that points into the sshfs mount /media/fuse/exploit/android-data  
   
   trigger\_copy():
10. Use SessionManager as chronos to StartSession for guest, StopArcInstance, StartArcMiniContainer, and UpgradeArcContainer for guest. This triggers arc-boot-continue which triggers the un-jailed cache file copy similar to arc-remove-data.
11. Wait for the file at /run/udev/data/+pci:0000:00:00.0 to be overwritten. This path is hardcoded into the sftp-server patch and the copy of the ‘EXPLOIT’ file will be pointed to here via a symlink.  
    
    viacups stage\_rescan():
12. Using cups, trigger the removal of the pci device via writing ‘1’ to /sys/devices/pci0000:00/0000:00:00.0/remove. This will trigger udev to execute the REMOVE\_CMD now defined in /run/udev/data.  
    
    restore\_backup():
13. If not running post boot (ie the user is presently logged in), use the now-running ssh server to restore the backup of the user’s /home/root/[hash]  
    
    interactive(), postboot(), patchpolicy():
14. Hand off to the post routine: interactive gives a root shell, postboot restores the policy backup (read on), and patchpolicy will patch the device policy
15. Patchpolicy drops a compiled c++ binary which uses the protobuf libs to add the gpu-process startup flag to the latest /var/lib/whitelist/policy.\*, and creates a backup (as restored in step 14)

=== src.tar.gz ===  

Makefile - will combine all the below files into privesc.sh, provided separately.  

sftp-server.patch - patch to openssh sftp-server to trigger the lstat vulnerability.  

privesc.sh.pre - privesc.sh without the packaged files.  

assets/pdf.pdf - a generic pdf sample, only used to trigger cups, not a payload  

assets/ppd.ppd - modified Anitech M24 ppd, adding command execution on line 70  

policy/patchpolicy.cc - C++ to backup, parse, patch and save the PolicyFetchResponse in /var/lib/whitelist  

policy/\*.pb.\* - C++ files generated via protoc  

policy/proto/\* - The relevant proto files taken from platform2  

policy/protobuf - not included due to size, statically built protobuf checkout and library

**CREDIT INFORMATION**  

Reporter credit: Rory McNamara

## Attachments

- [src.tar.bz2](attachments/src.tar.bz2) (application/octet-stream, 4.3 MB)
- [privesc.sh](attachments/privesc.sh) (text/plain, 1.8 MB)

## Timeline

### do...@chromium.org (2020-04-20)

Thanks for the very detailed report! Looping in some Chrome OS security folks to help triage this. I'm seeing a couple of key items in the breakdown:

1. This relies on an attacker-controller SSH server running a patched version of sftp-server, and has been repro'd in dev mode from crosh. Does not work from guest mode.
2. The sftp-server is used to exploit a copy race condition through symlinks in arc-remove-data / OnBootContinue, with the goal of allowing arc-stale-directory-remover to remove a previously created (and known) guest user directory and thus assign permissions such that CUPS can write to that directory
3. Persistence is achieved through patching the policy whitelist, since the signature isn't checked before the policy is used by login_manager for the pre-login Chrome instance.

I'll split out a sub bug for (3), and leave this bug for the MountEx/CUPS/arc-remove-data/arc-stale-directory-remover dance (unless other folks think there are parts in there that can be split out too).

[Monorail components: OS>Systems]

### do...@chromium.org (2020-04-20)

+cryptohome owners.

### do...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2020-04-20)

+cups owners
It seems the most critical part of this attack is cups command execution as root.

IIUC root rm -rf using arc-stale-directory-remover and root file write using arc-remove-data and arc-setup's OnBootContinue are not possible without modifying /home/root using cups to execute commands as root (please correct me if I'm wrong).
Also, I'm not sure if it's possible to make arc-stale-directory-remover, arc-remove-data, and arc-setup safe in case the attacker has write access as root.

### ro...@rorym.cnamara.com (2020-04-20)

cups executes commands as gid root, which allows for the creation of symlinks in /home/root.

If arc-stale-directory-remover, arc-remove-data and arc-setup ignored/detected symlinks in /home/root the rm -rf and file copies would not be possible to locations outside /home/root, which should block even a root attacker with write access.

### ha...@chromium.org (2020-04-20)

Thank you for the explanation.
I wasn't aware of the difference between gid root and uid root, and still not sure if it's possible to make everything safe against attackers who can execute command as gid root (i.e. isn't the game already over?), but the people from the security team may have different opinions.

### mn...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-04-20)

Splitting  this into individual bugs (step numbers per original report for reference)

1-3: cryptohomed manipulating chronos-owned file system locations: https://crbug.com/chromium/1072444
4,7,10: arc-setup should be more cautious when accessing the file system as root: https://crbug.com/chromium/1072467
(various): cups shouldn't be running with gid=0: https://crbug.com/chromium/1072470
8: mounts via cros_disks shouldn't allow to inject symlinks to outside the mount: https://crbug.com/chromium/1072474
9: root file write to root command execution in udev via REMOVE_CMD: https://crbug.com/chromium/1072486
15: session_manager code exec from policy: https://crbug.com/chromium/1072276 already filed, will comment on that.



### mn...@chromium.org (2020-04-20)

Upgrading to critical since this is a verified boot bypass (via session_manager policy cmd exec)

### mn...@chromium.org (2020-04-21)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-04-21)

One more for the CUPS cmdexec: https://crbug.com/chromium/1073063

### [Deleted User] (2020-04-21)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2020-04-22)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-04-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-04-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-04-25)

Has the chain been officially broken at this point? Has anything been merged to 83?

### jo...@chromium.org (2020-04-28)

83 merge for the CUPS issue is at https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/2169367.

### mn...@chromium.org (2020-04-29)

The CUPS root gid fix has landed and got merged. That addresses the arguably most severe link in the chain. Let's close this bug and track the remaining work on the individual bugs.

### [Deleted User] (2020-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-30)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M83. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-30)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2020-05-01)

The merge happened in one of the blocking bugs.

### na...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-05-06)

Notes to discuss in the panel. Per https://www.google.com/about/appsecurity/chrome-rewards/index.html#chromeos this is a:

Sandbox Escape
Persistence 

Both with a working proof-of-concept

### na...@google.com (2020-05-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-07)

Congrats the Panel decided to award $45,000 for this report! Nice one! 

### ro...@rorym.cnamara.com (2020-05-07)

Thank you!

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1072233?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1072276, crbug.com/chromium/1072444, crbug.com/chromium/1072467, crbug.com/chromium/1072470, crbug.com/chromium/1072474, crbug.com/chromium/1072486, crbug.com/chromium/1073063]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052058)*
