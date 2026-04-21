# Security: Elevation of Privilege via Vulnerability in Keystone for macOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40075849](https://issues.chromium.org/issues/40075849) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Updater |
| **Platforms** | Mac |
| **Reporter** | ma...@gmail.com |
| **Assignee** | no...@google.com |
| **Created** | 2023-10-29 |
| **Bounty** | $5,000.00 |

## Description

# VULNERABILITY DETAILS

## 0x01 

On macOS, Keystone components are used in Chrome (and other Google software such as "Chrome Remote Desktop") for software updates.

When the user installs Chrome Enterprise, configures Chrome updates, or installs other Google software, the Keystone component will run with root privileges (for example: Keystone in GoogleSoftwareUpdate component: "/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle").

During software installation or update, the Keystone component implements a lock operation:

```
id __cdecl +[KSInstallSettings userInstallLockFile:](id a1, SEL a2, id a3)
{
  __CFString *v4; // rdi

  v4 = CFSTR("/tmp/com.google.Keystone");
  if ( objc_msgSend(a3, "length") )
    v4 = (__CFString *)a3;
  return objc_msgSend(v4, "stringByAppendingPathComponent:", CFSTR(".keystone_install_lock"));
}
```

This lock file will be opened and changed to the "-rw-rw-rw-" permission. The Keystone component detects whether it is a symbolic link (via O_NOFOLLOW) when the file is opened, but this detection can be bypassed by a hard link on macOS.

Since the "/tmp/" directory of macOS is writable by any user, a low-privileged user can create the "/tmp/com.google.Keystone" directory in advance and create a hard link ".keystone_install_lock" in it to point to any file. When the Chrome or other Google software is installed or updated, the Keystone component runs with root permissions, the attacker can change the permission of any file in system to readable and writable permissions for any user.

After the attacker gains the ability to read and write arbitrary files, it needs to be converted into executing arbitrary code with root privileges:

Since the modification permission is "-rw-rw-rw-", attackers cannot escalate privileges via "/etc/sudoers" or similar files. The system will check the permissions of these files. If the file is writable by ordinary users, the configuration will not take effect. And since there is no executable permission ("-rw-rw-rw-"), attackers can't escalate privileges via modifying the executable program running as root.

Under the old macOS version, attackers can escalate privileges via modifying "/etc/defaults/periodic.conf" (The settings are automatically triggered when macOS performs periodic tasks).

However, in higher versions, macOS has added TCC protection to the "/etc/defaults/periodic.conf" file (and some similar files). No matter what permissions the process (even root) modifies this file, "SomeApp would like to administer your computer" will be prompted by the system and requires the user's active allow. 

Although in lower versions, I have been able to silently escalate privileges and obtain a shell running with root privileges, I need an exploit that can escalate privileges by default setting under the latest version of macOS to complete the weaponized exploit and improve the severity of this issue. 

Apple is working on mitigations to reduce this exploit method (from "arbitrary file write" to "arbitrary code run with root") in the system itself.

I started reviewing components in Google itself to see if there are some issues that could be exploited to complete privilege escalation. Then I discovered the following 0x02 (actually 0x02 contains two issues).

## 0x02

I found that after the enterprise administrator deploys the installation package for Chrome Enterprise, when installing the GoogleChrome.pkg, the Keystone component will run with root privileges in the postinstall script of installation package and attempt to install GoogleSoftwareUpdate service to:


```
/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle
```

The `ksinstall` will be executed as root:

```
/path/to/ksinstall --install=/path/to/Keystone.tbz
```

The key issues in this process:

### https://crbug.com/chromium/1

 `ksinstall` will detect the version of GoogleSoftwareUpdate in Keystone.tbz, then unzip it to "/tmp/{random_path}/GoogleSoftwareUpdate.bundle" for checking its codesign.

However, it will only check the codesign information in Keystone.tbz when the installing version is greater than the GoogleSoftwareUpdate version that exists on the system:

```
2023-10-28 18:23:39.091656+0800 ksinstall[47378:757020] 2023-10-28 18:23:39.091 ksinstall[47378/0x7ff857d89640] [lvl=2] -[KeystoneInstallBackend shouldInstallWithVersion:error:] Google Software Update installer attempting to install unsigned bundle: <KSError:0x600000c23030
	......
		NSLocalizedDescription = "KSCodeSigningVerification failed to validate code signing for '/tmp/ksinstall.ysB18JUBzv/GoogleSoftwareUpdate.bundle'. Error code: -67030";
		line = 303;
		filename = "KSCodeSigningVerification.m";
		function = "+[KSCodeSigningVerification verifyBundle:applicationId:error:]";
		date = 2023-10-28 10:23:39 +0000;
	}
```

So if the GoogleSoftwareUpdate component does not exist on the system before, `ksinstall` will install GoogleSoftwareUpdate directly (without codesign check).

In this case, the attacker can directly combine the issue in 0x01, overwrite the Keystone.tbz (with a fake GoogleSoftwareUpdateDaemon), and wait until the GoogleSoftwareUpdate component is installed in "/Library/Google/GoogleSoftwareUpdate/". After that, the attacker can make a request to "com.google.Keystone.Daemon.UpdateEngineXPC" service through NSXPC, and the system will run "/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle/Contents/MacOS/GoogleSoftwareUpdateDaemon" with root privileges. The attacker successfully completed the LPE attack and executed arbitrary code with root privileges.


### https://crbug.com/chromium/2

In addition, for case that the GoogleSoftwareUpdate component already exists in the system:

There is a race condition issue between `ksinstall` check component version and check codesign information after compression.

`ksinstall` check the component version via：

```
/usr/bin/tar -Oxjf /path/to/Keystone.tbz GoogleSoftwareUpdate.bundle/Contents/Info.plist
```

Therefore, if an attacker has permission to write the /path/to/Keystone.tbz file, he can first fake a GoogleSoftwareUpdate component with a larger CFBundleVersion. When ksinstall determines that the version is newer than the local installed version, it will do the update process: decompress Keystone.tbz and check the codesign information in it.

Before decompression, the attacker can change the compressed GoogleSoftwareUpdate.bundle in /path/to/Keystone.tbz to a symbol link pointing to "/tmp/GoogleSoftwareUpdate.bundle" (a location controllable by the attacker). `ksinstall` does not prevent symbolic link when checking codesign information. Finally, `ksinstall` will move the symbolic link pointing to "/tmp/GoogleSoftwareUpdate.bundle" into "/Library/Google/GoogleSoftwareUpdate/":

```
$ ls -la /Library/Google/GoogleSoftwareUpdate/
total 0
drwxr-xr-x  4 root  wheel  128 Oct 28 22:14 .
drwxr-xr-x  4 root  wheel  128 Oct 28 22:14 ..
lrwxr-xr-x  1 root  wheel   32 Oct 28 12:35 GoogleSoftwareUpdate.bundle -> /tmp/GoogleSoftwareUpdate.bundle
drwxr-xr-x  4 root  wheel  128 Oct 28 22:14 TicketStore
```

At this point, the "/tmp/GoogleSoftwareUpdate.bundle/Contents/MacOS/GoogleSoftwareUpdateDaemon" is fully controllable by attacker. By modifying GoogleSoftwareUpdateDaemon and triggering it via NSXPC "com.google.Keystone.Daemon.UpdateEngineXPC", the attacker can complete the LPE attack and executed arbitrary code with root privileges.


Note that before `ksinstall` executes the installation, it will confirm whether 3550s has passed since the last update (through a file that records the update timestamp: {NSTemporaryDirectory}/.ksinstall-0-installAttempts.plist). So, to facilitate reproduction, you can manually change the computer time delay 1 hour when you reproduce, or just delete this file directly. I have implemented it into the `clean_sys.sh` script I mentioned below.


# VERSION

Chrome Version: 118.0.5993.117 stable (Official Build) (x86_64)
Operating System: macOS Sonoma 14.1 23B73 (all versions affected)

# REPRODUCTION CASE

a. This vulnerability can be automatically triggered in software updates (e.g., GoogleSoftwareUpdate.bundle component automatically update) / the enterprise administrator deploys Chrome installation package / or in any scenario where the Keystone component is used. In these enumerated scenarios, the triggering of this vulnerability does not require user interaction.

b. The exploit I wrote is for the installation of GoogleChrome.pkg, but these issues affect all processes mentioned above using Keystone.

c. There are two exploit_1 / exploit_2 in the attachment that exploit https://crbug.com/chromium/1 and https://crbug.com/chromium/2 in 0x02 respectively. The scenario of explot_1 is the first time to install Chrome Enterprise or configure Chrome update in the system (no "GoogleSoftwareUpdate.bundle" installed before). exploit_2 does not have any scenario restrictions and can be automatically triggered when Chrome is updated or when an enterprise administrator deploys GoogleChrome.pkg. So exploit_2 is more powerful. However, I recommend using exploit_1 to verify the vulnerability first, because exploit_2 exploits the race condition issue. Although it is 100% stable on my computer, I am not sure whether the `usleep(300000)` in "exploit_2/exploit.mm" is related to the computer configuration.

1. Download the attachment, unzip and enter the folder.

2. Clear the system through the script I provided to avoid previous reproduce from affecting this reproduce:

```
sudo ./clean_sys.sh
```

2. Compile the exploit and trigger (the trigger is used for sending NSXPC request):

```
clang++ ./exploit.mm -o exp
clang++ ./trigger.mm -framework foundation -o trigger
```

3. Run the exploit with a low-privileges user until prompt (keep exploit running and do next step):

```
$ ./exp         
[*] Setting the Environment ......
[*] Waiting for the install/update process ......
```


4. Simulate the scenario that the enterprise administrator deploys GoogleChrome.pkg for installation or updates: Download GoogleChrome.pkg from https://chromeenterprise.google/browser/download/#mac-tab and install it as an administrator.


5. Just wait. No user interaction is required. You can see that exploit finally obtains an interactive shell with root privileges (from the low-privileges user):

```
$ ./exp         
[*] Setting the Environment ......
[*] Waiting for the install/update process ......
[+] Overwrite the Magic File
[*] Waiting for the Attack ......
[+] Trigger the Fake GoogleSoftwareUpdateDaemon Service
[*] Elevation of Privilege ......
[+] Exploit Successfully!!!
[+] Please Enjoy Your ROOT SHELL:

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
bash-3.2# whoami
whoami
root
bash-3.2# 
```

# Suggestions

0x01: Check the case of HardLink.


0x02: I don't think the two issues in 0x02 can be exploited independently, but they do provide the ability to execute arbitrary code with root privileges after the attacker gains arbitrary file write. As Apple is working on mitigations to reduce this exploit method (from "arbitrary file write" to "arbitrary code run with root") in the system itself.

You can mitigate the two issues in 0x02 through strict codesign and symlink checking, or just fix the issue in 0x01


# CREDIT INFORMATION

Reporter credit: NorthSea


## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [exploit_2.mp4](attachments/exploit_2.mp4) (video/mp4, 2.9 MB)
- [exploit_1.mp4](attachments/exploit_1.mp4) (video/mp4, 3.3 MB)
- [clean_sys.sh](attachments/clean_sys.sh) (text/x-sh, 275 B)
- [exploit.mm](attachments/exploit.mm) (application/x-freemind, 3.5 KB)
- [trigger.mm](attachments/trigger.mm) (application/x-freemind, 800 B)
- [FakeKeystone.tbz](attachments/FakeKeystone.tbz) (application/x-bzip2, 2.9 MB)
- [FakeGoogleSoftwareUpdateDaemon](attachments/FakeGoogleSoftwareUpdateDaemon) (application/x-shellscript, 329 B)
- [clean_sys.sh](attachments/clean_sys.sh) (text/x-sh, 265 B)
- [Keystone.tbz](attachments/Keystone.tbz) (application/x-bzip2, 2.9 MB)
- [FakeKeystone1.tbz](attachments/FakeKeystone1.tbz) (application/x-bzip2, 2.9 MB)
- [FakeKeystone2.tbz](attachments/FakeKeystone2.tbz) (application/x-bzip2, 155 B)
- [remove_installAttempts.mm](attachments/remove_installAttempts.mm) (application/x-freemind, 369 B)
- [trigger.mm](attachments/trigger.mm) (application/x-freemind, 800 B)
- [exploit.mm](attachments/exploit.mm) (application/x-freemind, 5.1 KB)

## Timeline

### [Deleted User] (2023-10-29)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-10-29)

deleted

### dc...@chromium.org (2023-10-30)

This is an interesting report, but is there a repro that doesn't contain pre-built binary artifacts? I don't think there's a way to repro this without assuming the .tbzs are harmless. Which they might be, but there's no easy way to verify that :)


### dc...@chromium.org (2023-10-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>Updater]

### ma...@gmail.com (2023-10-30)

Hello, are you referring to the "*.tbz" files I provided in ChromeExploit.zip? I can provide a script to make them (without pre-built binary) later.

### [Deleted User] (2023-10-30)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2023-10-30)

deleted

### ma...@gmail.com (2023-10-30)

deleted

### dc...@chromium.org (2023-10-30)

Guessing a bit at severity and foundin.

### [Deleted User] (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2023-10-30)

[Empty comment from Monorail migration]

### wa...@chromium.org (2023-10-30)

[Empty comment from Monorail migration]

### wa...@chromium.org (2023-10-30)

[Empty comment from Monorail migration]

### no...@google.com (2023-10-30)

As a general matter, hardlinks cannot be detected on a POSIX system. Hardlinks are just how a file is represented on the file system. std::filesystem (among other things) will help us count the number of hardlinks to a file system object, but making assumptions about how macOS chooses to represent the contents of /tmp sounds brittle. 

At its core, this is another vulnerability caused by the root-level installer referring to, and trusting, a user-writeable file (in this case, the install lock). This specific instance is highly exploitable because it is at a well-known location. Keystone has various alternate mechanisms for avoiding running into itself, but it retained this lock file in an effort to avoid making a mess with old versions; this compatibility layer should be removed. The new cross-platform Chromium Update platform (https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/), currently in canary, avoids using file-based locking entirely and takes a more aggressive approach to hardening its root environment in a variety of ways; we need to think hard about whether to fix this in Keystone or to (aggressively) accelerate our timeline for getting rid of it completely. 

I agree that issue 0x01 is the "real" issue and 0x02 is a way to use permissions on arbitrary files. I'm less interested in fixing 0x02 in Keystone (defense-in-depth in Chromium Updater might be worth the investment) because "an unprivileged user can write to the files root is using" is one of those Just Plain Bad situations where some elaborate defenses are possible but most of them at least have time-of-check/time-of-use (TOCTOU) flaws.

Acquiring a file lock requires a file handle, which requires at least read or write permissions. The source code has a long comment explaining why it's using the specific permission set it is using, which has successfully persuaded me that there is no right way to do this, so the options I see are:

a) remove Keystone's use of lock files on well-known untrustworthy paths, using the algorithm currently used to validate other root operations to aggressively define "trustworthy path" when running as root
b) remove KSLockFile entirely
c) remove Keystone entirely

Of these three, I think `b)` is probably the least viable because rewriting KSTicketStore in a nontrivial way when we're planning to release Chromium Updater sooner rather than later is clearly a poor use of time. `c)` is possibly worth considering since we are already mid-launch for Chromium Updater. 

These are my initial thoughts on the exploit. I'll investigate the severity a bit and make a recommendation on that, although the Chrome Security folks are the ones who would make a real call here.

### wa...@chromium.org (2023-10-30)

Thank you for reporting, and especially for the high quality of the report.

We are investigating remediation options.

Since this vulnerability is in Keystone, particularly in Keystone's install, the fix for this will not be a Chrome side change (although a Chrome side change will be required, to package the new version of Keystone). Google distributes other applications as well that embed Keystone. In practice, Chrome is the first and fastest to pick up and deploy new versions of Keystone. We would like to avoid early disclosure (e.g. through Chrome's normal process) until we have also engaged with all other product teams and ensured that they are also distributing a fixed version of Keystone within their applications. Daniel, Robert, Mark, and/or other Chrome security folks, can you help us achieve this while still ensuring we properly credit / etc?

Mark, Robert, and others, we are investigating at least two paths to fix:
1. Cease shipping Keystone for new installs, and cut over to Omaha 4, which is at 25% right now anyways. For Chrome this can be done with Finch, since Chrome already packages a version of O4, but it may be safer to mirror other applications and use a minimal registration framework shim. Investigation is underway on how large or risky such a shim is.
2. Remove ksinstall's usage of the lock file altogether. This reported lock file is used for backward compatibility with old versions of Keystone. Investigation is still underway on whether removal is feasible and whether there are other usages of lock files in Keystone that are equivalently affected. We would then have to conduct a release of keystone and rebuild.

### rs...@chromium.org (2023-10-31)

+amyressler for coordination given the impact to other Google products

Would (1) also affect other products or would those products need to also choose to adopt O4? Going with option (2) seems like a less-risky and easier-to-deploy remediation.

### am...@chromium.org (2023-10-31)

>>> We would like to avoid early disclosure (e.g. through Chrome's normal process) until we have also engaged with all other product teams and ensured that they are also distributing a fixed version of Keystone within their applications. 

I've added RV-SecurityEmbargo here. We can decided on a next-action date to revisit lifting the embargo once we have a better understanding of remediation plan in general and specific to other affected products. Once there is a remediation in place, we can still perform all the other appropriate functions in terms of acknowledgement, VRP etc. 

In terms of "until we have also engaged with all other product teams and ensured that they are also distributing a fixed version of Keystone within their applications," it sounds like investigation to make the determination of remediation plan is still in progress. Once this is more solidified, we can assist with coordination to ensure teams with other affected products are pulled in to be aware of and leverage the remediation. 


### wa...@chromium.org (2023-10-31)

In path (1), yes, those products would have to adopt O4. We would provide a drop-in replacement for the current Keystone registration framework (i.e. provide a shim of the registration framework that uses O4 under the hood). However, this does mean that the fix would be limited to macOS 10.15+, and those products would have to drop compatibility with macOS 10.14-. While that has to be done eventually (since Keystone will become unsupported soon), it seems daunting to me to do that deprecation in an emergency context (e.g. coupled to this issue).

I think my main concern with (2) is that even if the ksinstall lock file issue is easy to remediate via removal, there are other places in the code where a lock file is used and I'm concerned that they may have the same or similar issues, but can't be easily removed or changed without significant rewriting of Keystone's concurrency model, which is probably infeasible. Maybe there's an alternative way to fix the lock file, such as checking the contents of the file are either empty or parseable as a lock file after opening it, but before calling fchmodat? This area of Keystone is thorny and dangerous (e.g. fchmodat before opening instead of fchmod after opening is intentional) and mistakes can brick the updater or worse. I also share the concerns mentioned in https://crbug.com/chromium/1497239#c15 about TOCTOU.

### ma...@chromium.org (2023-10-31)

https://crbug.com/chromium/1497239#c15:
> As a general matter, hardlinks cannot be detected on a POSIX system.

stat::st_nlink reliably produces a count of hard links. If you want to check it, the prudent move would be:

  int fd = open(…);
  fstat(fd, &sb);
  if (sb.st_nlink > 1) /* handle it */

taking special care to only interact with this file via the open `fd`, and not by path again.

That said, if recent Keystone has other ways to solve the problem that this lock was solving, it may well be better to remove the lock altogether rather than trying to detect undesirable cases. How old is “old Keystone” that wouldn’t know about the other ways to deal with what this lock file dealt with?

https://crbug.com/chromium/1497239#c16:
> Mark, Robert, and others, we are investigating at least two paths to fix:

I think it’s prudent to at least attempt to develop (2) while we work through timelines and risks of both (1) and (2). That doesn’t mean we’re committed to releasing (2), but I’d rather have it ready if it turns out that we want to do it.

### ma...@google.com (2023-10-31)

Checking `st_nlink` isn't sufficient to avoid this issue. The attacker can unlink the lock file between the `open` and the `fstat` to ensure the check sees the number of links as 1.

### wa...@chromium.org (2023-10-31)

> I think it’s prudent to at least attempt to develop (2) while we work through timelines and risks of both (1) and (2). That doesn’t mean we’re committed to releasing (2), but I’d rather have it ready if it turns out that we want to do it.

100% agree. The more options we find, the better.

### ma...@chromium.org (2023-10-31)

https://crbug.com/chromium/1497239#c21:

I disagree.

While it is valid for the attacker to link a filesystem node anywhere that they can write to on the same filesystem, it’s not necessarily valid for them to remove the links they created.

With the sticky bit set on /tmp (as it should be, and if it’s not set, then there’s a wider hole on the system that’s not our bug), it will be impossible for the attacker to unlink the lock file unless they have permission—they must own the file. If they have this level of access to the file, they necessarily already have the ability to write to it, and they don’t need Keystone’s help.

### ma...@google.com (2023-10-31)

You're right, the sticky bit being set on /tmp does protect against the scenario I described.

### ma...@chromium.org (2023-10-31)

There is a bit more nuance, actually. Per the report, we're not in /tmp directly but in /tmp/com.google.Keystone. I suspect that we can neither apply nor enforce a restrictive enough mode on that directory while maintaining backward compatibility with existing Keystones.

### wa...@chromium.org (2023-10-31)

Based on go/keystone-var-pm we might pessimistically conclude that (in 2019) the sticky bit (and /tmp in general) would be under attacker control between 0.1% and 0.5% of devices.

### no...@google.com (2023-10-31)

While "the user's machine is bizarrely configured in a way that is harmful to security" is something we need to consider for "do not break the system" and "do not expose the user to new remote attacks", unusually insecure preexisting configurations are probably not reasonable to defend against for a purely local privilege escalation attack, since the system is already in a configuration that generally does not defend correctly against escalation of privilege. It's certainly better to avoid creating additional vulnerability in these odd configurations, of course, but I don't think they're totally fatal to a working system.

What I'm less convinced about is that there are no "ordinary" system configurations that would not give us extra hardlinks to arbitrary files (even in `tmp`) on tolerably ordinary macOS systems. This is what I was referring to by "mak[ing] assumptions about how macOS chooses to represent the contents of /tmp" in https://crbug.com/chromium/1497239#c15. The technique in https://crbug.com/chromium/1497239#c20 is equivalent to my mention of std::filesystem and the sticky bit might be some mitigation against removal of links, but I'm not persuaded we can reasonably act on some "unexpected" greater number of hardlinks to a file because I'm reluctant to believe that there are no widespread enterprise or system management tools that don't regularly make weird networks of hardlinks based on monitoring kernel file system events as part of some odd backup, malware scanning, sharing, or other unforeseen file management scheme. Maybe I'm being much too cautious or cautious in the wrong way here? It just feels like making assumptions about how many hardlinks there will be to ordinary stuff in `/tmp` is one of those things that sounds okay on paper but will cause a bunch of incompatibilities in the field in system configurations we never anticipated using software we've never seen before.

If we choose to update Keystone instead of accelerating a migration to Omaha 4, I think discontinuing use of cross-user lock files in well-known locations is much more appropriate than trying to do anything clever with hardlink counting. I would prefer to remove all use of file locks but that is probably not practical; removing all use of cross-user file locks is probably viable and represents some improvement to the status quo. Then what to do about an extant file in a non-readable mode in the location we check for a lock file as root? The current algorithm tries to change the file mode, which is the behavior that produces the vulnerability. If we make no attempt to correct the file mode, then anything dependent on lock files has no obvious way to recover from a stray file with an unexpected mode. I don't know of any way to estimate the update success rate loss from that.

Unfortunately, it looks like my memories and understanding of my own code are wrong and ksinstall doesn't use anything other than lock files to avoid colliding with another instance of itself. (I was misunderstanding comments I'd left about "lock file is used by older installers" when looking this up previously and fooled by my own memories, apparently.) ksinstall can adopt techniques implemented by Omaha 4 to use Mach service names for locking to avoid interfering with itself going forward but runs the risk of running into a concurrent copy of an old ksinstall if it doesn't at least look, and would get run over by an old ksinstall running concurrently if it doesn't try to set the lock file. 

Keystone Agent contains logic to check the install lock file to determine if the installer is running, which it uses to determine if various error conditions during a self-update check are expected because the self-update started, removing available services. It seems like there should be a much better way to plumb this but it might require some puzzle-solving. A bigger problem is that the _existing_ Keystone Agent is interested in that check to determine if a _new_ `ksinstall` is running, so concurrently updating Keystone Agent to understand ksinstall's presence by some other means will not prevent the situation from getting handled incorrectly.

So, unfortunately, I was wrong -- this lock file might still be load-bearing in some ways. I think the Keystone Agent logic will only cause spurious errors and the system will still converge on the correct updated state (it's only Keystone Agent that won't understand what's happening during the update, and then only in some circumstances --- the control flow is tangled here and it would take more time for me to determine if this check is ever actually relevant), but conflicts between ksinstall and old versions of itself might be more of a concern. Still investigating.

### ma...@chromium.org (2023-10-31)

https://crbug.com/chromium/1497239#c27:
> Unfortunately, it looks like my memories and understanding of my own code are
> wrong and ksinstall doesn't use anything other than lock files to avoid
> colliding with another instance of itself.

Can we be more specific about “colliding with another instance of itself”? Perhaps focusing only on ksinstall for the time being, can we answer:

What operations are the lock guarding? (On the filesystem, presumably, but other operations too.)

What need is there to guard system and user ksinstalls against one another across privilege boundaries? I am assuming that at present, both user and system ksinstalls share the /tmp/com.google.Keystone/.keystone_install_lock path.

Are there other users of /tmp/com.google.Keystone beyond /tmp/com.google.Keystone/.keystone_install_lock path?

### no...@google.com (2023-10-31)

The lock file guards:
* stopping Keystone services
* extracting/copying Keystone to its installed location
* installing/replacing Keystone service configuration (LaunchAgent/LaunchDaemon plists)
* starting Keystone services

If two different versions of Keystone attempt to perform these operations concurrently, they may interleave in unpredictable order, leaving the user with a Keystone bundle on disk that won't run because its bundle-level signature doesn't match, among other issues. User Keystone prefers not to install itself at all when a system-wide Keystone (which also configures itself to run non-elevated to perform per-user updates as well) is available, so System Keystone attempts to also take the user lock to prevent User Keystone from installing itself only to immediately uninstall, but if it can't get the lock after a modest timeout it just goes on without it anyway, it's not doing anything to guard state consistency.

This suggests that the locks currently in `/tmp` could be moved somewhere under `[~]/Library/ApplicationSupport` so they're not accessible by other users (under normal security configurations; how hard do we want to try to defend against bad ones?) to mitigate this attack, with System Keystone no longer taking any interest in the user lock file, although this doesn't provide lockout cross-compatibility with old versions of `ksinstall` (which we may not care about enough to handle). I can imagine logic that "gently" looks at lock files in the legacy locations (that is, with no chmod) in a best-effort way -- creating and respecting them if present -- but never writes or chmods them, handling an inability to open them by ignoring them and using only the "real" lock file that moved to the new location. (It wouldn't try to "gently" acquire the "legacy" lock until after successfully acquiring the repositioned lock. If it can open the legacy lock but gets a lock conflict, it interprets this as "legacy installer busy", which is different from "cannot open file" which it interprets as "y'know, this is why we moved the file in the first place" and does not touch it, treating it as unlocked.)

This file is apparently used by Keystone Agent to figure out if it is in the middle of self-updating (although I have my doubts about whether it needs to do this when it does) and by Keystone Registration Framework to weakly, opportunistically try to not do stuff while Keystone is updating and to block Keystone from installing over itself while it has a task pending, which is intended to reduce the rate of user-visible update errors and avoidable spurious crash reports caused by updates running concurrently with interactive requests for update checks.

### wa...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### pb...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pb...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### wa...@chromium.org (2023-11-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/425894fa253be30a2f813a27d9d1a9e0966ada29

commit 425894fa253be30a2f813a27d9d1a9e0966ada29
Author: Joshua Pawlicki <waffles@chromium.org>
Date: Wed Nov 01 22:33:08 2023

Updater: Default to using ChromiumUpdater.

Bug: 1497239
Change-Id: I74c98530539b5fbab452d7bc19446894d02a149a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4993921
Reviewed-by: Xiaoling Bao <xiaolingbao@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1218504}

[modify] https://crrev.com/425894fa253be30a2f813a27d9d1a9e0966ada29/chrome/common/chrome_features.cc


### wa...@chromium.org (2023-11-07)

We plan to remediate in Chrome by discontinuing the use of Keystone in Chrome. We will handle other products by patching Keystone. 

To accomplish this for Chrome, we'll have to take the following combined merge, or something close to it: https://chromium-review.googlesource.com/c/chromium/src/+/5010752

The code changes in that CL are fairly low-risk, except for flipping UseChromiumUpdater to FEATURE_ENABLED_BY_DEFAULT, which activates large sections of code. On the bright side, that can be remotely disabled if necessary. These changes are currently live in canary, and most of them are live in dev. Still, to mitigate risk, I'd like to merge to 120 and let the change bake in beta for a little before moving to stable and extended stable. Still, I'll request merge approvals now for 120, 119, and 118.

### [Deleted User] (2023-11-07)

Merge review required: M120 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-07)

Merge review required: M119 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-07)

Merge review required: M118 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2023-11-07)

1. Fits because it is an important security fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/5010752
3. Yes.
4. Yes. It is behind Finch. Experiments are active in Canary.
5. N/A
6. It would be helpful for the test team to verify that the install flows on macOS work correctly:
  - The PKG installer installs correctly, and navigating to chrome://help shows that the browser is up to date.
  - The drag-install experience acts correctly, and navigating to chrome://help shows that the browser is up to date.

### wa...@chromium.org (2023-11-07)

Mark and I talked; unless the security team feels otherwise, to balance the risk of the fix with the exposure of the vulnerability, we'd prefer to fix in M120 but hold off on deploying to M118 and M119 until we have more confidence in the overall safety of the fix.

### am...@chromium.org (2023-11-07)

While this is a sufficiently serious issue, looking over https://crrev.com/c/5010752 from a security merge approval perspective I would be exceptionally concerned about approving for backmerge to Stable or Extended Stable. I concur with potential backmerge to 120 Beta only (after sufficient bake time / testing) and declining backmerge to 119 and 118. 


### wa...@chromium.org (2023-11-08)

The most relevant change (EnableChromiumUpdater enabled_by_default) has been live on canary and dev for a few days (and this led us to discover some of the others in that CL); I've also conducted manual tests of most of the relevant features and situations (but I don't want to claim perfect coverage, since I only have a single platform). Amy / Srinivas, are you comfortable approving merge to 120? Once we are on beta we will generate PKG installers that can be tested.

Lindsay, can I work with you or could you nominate someone I could work with to understand the existing manual testing that is done on the install flows for each release candidate? I'd also like to collaborate to develop a comprehensive install test plan.

### wa...@chromium.org (2023-11-10)

Amy, can you approve merging to 120?

### am...@chromium.org (2023-11-10)

Okay, based on all of the above and looking at dev and canary since the EnableChromiumUpdater default enablement landed a few days ago, I'm think we're okay to merge this. Especially next Beta is next week followed by a release freeze week, so let's go ahead and get this merged. 
Approving for 120, please merge to branch 6099 by EOD Monday 
Thanks, Joshua! 

### wa...@chromium.org (2023-11-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2bede8b2fb8a2c13e7647311854cfd999a4468e3

commit 2bede8b2fb8a2c13e7647311854cfd999a4468e3
Author: Joshua Pawlicki <waffles@chromium.org>
Date: Fri Nov 10 22:41:26 2023

Combined cherry picks for https://crbug.com/chromium/1497239.

Chrome: When a restart to update is needed, say so in chrome://help.

Bug: 1497239

Fixed: 1499881
Change-Id: Iacfdd037d86b38aad848a63cb1b4708dc55e371b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5002022
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Commit-Queue: Rebekah Potter <rbpotter@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1220437}
(cherry picked from commit 812a35ef5efb96fb4609e25cc56a25b3a9a44790)


Change unretaineds to weak_ptrs in about_page handler.

Fixed: 1499047
Change-Id: I6498b88fee31a14fa0b51a630513456d6e9d328d
Low-Coverage-Reason: HARD_TO_TEST
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5001395
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Commit-Queue: Rebekah Potter <rbpotter@chromium.org>
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1220383}
(cherry picked from commit 1324ed92cc0fa9fd9a55d5e664b91634e36ab1fc)


Chrome: Use GoogleUpdater in PKG installer instead of Keystone.

Fixed: 1499285
Change-Id: Ib34c23468cd7911e123d9d8b7a474a9660dcdddc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5001744
Reviewed-by: Xiaoling Bao <xiaolingbao@chromium.org>
Reviewed-by: Mark Mentovai <mark@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1219681}
(cherry picked from commit 24c06b218ee831488a745ac948f52509fae0dcf8)


Chrome: Create a product registration from the privileged helper.

Fixed: 1498924
Change-Id: Idd13b0fd98c17d19d38b8f56b524a48326b5a794
Low-Coverage-Reason: COVERAGE_UNDERREPORTED - The code only runs in google-branded mac builds, and is covered in that case. Or perhaps the coverage bot doesn't run updater_tests_system because of passwordless sudo.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5002727
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Reviewed-by: Xiaoling Bao <xiaolingbao@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1219097}
(cherry picked from commit b1ec4b9af24866c9947422b5b6c5c60ac2ce3a15)


Chrome/Updater: Fix health check to use case-insensitive compare.

Fixed: 1498960
Change-Id: I5eee79300f402c6c27a1c41b099ecf3b0d85b5dc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5002067
Reviewed-by: Noah Rose Ledesma <noahrose@google.com>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Commit-Queue: Sorin Jianu <sorin@chromium.org>
Commit-Queue: Noah Rose Ledesma <noahrose@google.com>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1218938}
(cherry picked from commit f5d6aa1b6651a8acd3c2761c9bdeadac3884dd3f)


Updater: Default to using ChromiumUpdater.

Bug: 1497239
Change-Id: I74c98530539b5fbab452d7bc19446894d02a149a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4993921
Reviewed-by: Xiaoling Bao <xiaolingbao@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1218504}
(cherry picked from commit 425894fa253be30a2f813a27d9d1a9e0966ada29)


Updater: Fix privileged helper copy step.

base::CopyDirectory does not copy symlinks, updater::CopyDir does.
Also added more comprehensive unit testing of that install flow.

Fixed: 1498444
Change-Id: Iafbc47741dcd216719cbee330d3d838377832a8b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4994134
Reviewed-by: Xiaoling Bao <xiaolingbao@chromium.org>
Commit-Queue: Xiaoling Bao <xiaolingbao@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1218287}
(cherry picked from commit 06cb948a262444206fc89edfd25662a6a94cc166)


Updater: Update mac prod updater to 120.0.6077.0.

(cherry picked from commit 09ee2d454732d08dfed86324d97f5820dd395291)

Change-Id: Ia8dc649ea718b67276beea8a2c9842abb3d42153
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4994877
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Commit-Queue: Sorin Jianu <sorin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1218270}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5010752
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Commit-Queue: Rebekah Potter <rbpotter@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#511}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/mac/privileged_helper/service.mm
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/BUILD.gn
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/common/chrome_features.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_test_commands.h
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/browser/ui/webui/settings/about_handler.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/mac/privileged_helper/service.h
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_tests_impl.h
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/installer/mac/pkg_postinstall.in
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/browser/ui/webui/help/version_updater_mac.mm
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_test_commands_user.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_test_commands_system.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_tests.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/browser/updater/browser_updater_client.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_tests_mac.mm
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/chrome/updater/test/integration_tests_helper.cc
[modify] https://crrev.com/2bede8b2fb8a2c13e7647311854cfd999a4468e3/DEPS


### wa...@chromium.org (2023-11-29)

Hello all, this bug is now a month old and I want to give an update.

All macOS devices running macOS 10.15+ are transitioning away from using Keystone, replacing it with GoogleUpdater (AKA ChromiumUpdater AKA Omaha 4).

A fix within Keystone is also under development. We intend to deploy the fix to machines running macOS 10.13 to 10.15.

There is still some Keystone use in Chrome. Chrome will transition away from using Keystone in M120, and Keystone will be removed altogether from Chrome in either M121 or M122.

There is still some Keystone use in other Google applications. We have taken an inventory of usages and are in the process of working with those teams to either package a fixed Keystone (once available) or GoogleUpdater (we hope to have a working drop-in replacement PKG tomorrow). This time of year has numerous production / deployment freezes and it is not yet clear that all teams will update their software before January 2024.

### wa...@chromium.org (2023-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-13)

[secondary security shepherd]

This bug looks well on its way to being fixed. I'm adding a NextAction date Jan 11, about 1 week after M120 is out so we can post an update.

### [Deleted User] (2023-12-28)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### wa...@chromium.org (2024-01-11)

Hello all. We have a fix in Keystone and are working with product teams to deploy it ASAP.

Amy, should we mark this as fixed, or wait until we've gotten confirmation from Drive, Earth, etc that they've all updated to include the new version of Keystone? (I'd prefer we do not disclose until that has happened, or until it becomes clear that that final stage will take too long.)

### am...@chromium.org (2024-01-12)

Nice work getting this resolved and coordination with the product teams as well, Joshua! 

We can go ahead and mark this as Fixed, which I've taken the liberty of doing. :)  I've added a release label to identify which version of Stable channel this CP fixes shipped in so we can back-issue a CVE here. The CVE description is minimal and we can keep it high level to avoid revealing any details that would n-day other products. 

The report itself won't be disclosed until 14 weeks from when the bug is closed as Fixed / today. If you think that is not enough time, please let me know. It's currently under embargo, so that wouldn't happen anyway. I'm removing embargo for now, but if you think that 14 weeks (18 April) isn't enough time I can add the embargo label back on. I'd at least like to open this up to security-notify for now so that downstream Chromium embedders can know about this issue and pick up the fixes if they haven't already. 

Also, closing this as fixed today, will allow the bug to go into the VRP queue for VRP Panel assessment, so we can work on the report getting a potential reward. :) 

Please let me know if there are any issues or concerns with any of the above. 

### [Deleted User] (2024-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-13)

[Empty comment from Monorail migration]

### wa...@chromium.org (2024-01-18)

Thank you, Amy, that all sounds right to me!

### no...@google.com (2024-01-18)

I would definitely expect 14 weeks from now to be enough time; all known product teams that need to pick up the Keystone fix (separately from moving to Omaha 4, which was Chrome's approach) have at least started the process, although for many of them building and releasing is a more fiddly, manual task than it is for Chrome.

### ma...@gmail.com (2024-01-19)

Hi all, thanks for your work on this report! It's a pleasure working with your team!

### ma...@chromium.org (2024-01-19)

Thanks for your well-described and actionable report!

### am...@google.com (2024-01-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-19)

Congratulations NorthSea! The Chrome VRP Panel has decided to award you $5,000 for this report of web platform privilege escalation with functional exploit (or demonstrated exploitability). A member of the Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your exemplary efforts and your excellent report and working with us throughout -- great work! 

### ma...@gmail.com (2024-01-19)

deleted

### am...@chromium.org (2024-01-19)

Thanks for reaching out with your questions / concerns. 
It's important to note that not every VRP report is a precedent for a future reward amount for a similar report. It is, however, a fair point to question the reward amount here, especially given that you did provide the components for exploitation and given that similar reports were, related to privesc vulnerabilities via installer/updater were rewarded higher reward amounts. In terms of reward amount discrepancy, it's also important to not that https://crbug.com/chromium/1279188 did provide a similar exploit. 

While we understand this is not a web platform privilege escalation, we do not have a category for OS priv-esc, since our threat model (and thus our VRP reward scope) is focused on that of our web platform and associated vulnerabilities. So the vulnerability in Chrome and in Chromium code that we can make a security beneficial change is by way of the web platform. Which rather brings to one of the primary factors of the reward determination: "Since this vulnerability is in Keystone, particularly in Keystone's install, the fix for this will not be a Chrome side change (although a Chrome side change will be required, to package the new version of Keystone). Google distributes other applications as well that embed Keystone." 

We are happy to take another look here and reassess if this report potentially warrants a higher reward. Thank you for your patience in the meantime. 



### am...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### ma...@gmail.com (2024-01-23)

deleted

### am...@chromium.org (2024-01-25)

Hello NorthSea, we have reassessed your report and have determined have decided to increase the VRP reward for your report to $10,000. During assessment, we determined that we did not get the assessment correct the first time around. Our review left us with the notion that there were significant preconditions to exploitation; however, your very detailed report disabused of that notion during our follow-up review. We considered this as mitigated by race condition; however, we consulted with the engineers who worked on this issue and it was conveyed that this is not a significant race and one that case be realistically won by an attacker in a real-world exploitation scenario. We don't always get every reward decision right the first time around, so we appreciate you voicing your concerns about the reward decision and allowing us to reassess. 

### am...@chromium.org (2024-01-25)

Something I should have mentioned in my previous comment -- the original $5,000 reward information was already forwarded to finance for processing. Additional $5,000 from this reassessment will be sent as a separate payment at the same time or to soon follow the original reward amount, depending on the speed of your enrollment into the payment system. 

### am...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### ma...@gmail.com (2024-01-26)

Hi Amy, thank you for your reassessment and quick detailed response!

Glad to see the final bounty reward decision for this report. And thanks again to your team for the fix and great work!

### am...@google.com (2024-01-27)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-27)

This issue was migrated from crbug.com/chromium/1497239?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-04-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-05-09)

there is bug in the automation that is resulted in some reports that were reassessed to a higher reward amount to have the field reverted to the original reward amount; updated the vrp-reward field to the correct reward amount

### am...@chromium.org (2024-05-10)

It also appears the POC files have been deleted from this issue, so I'm re-uploading them.

### am...@chromium.org (2024-05-10)

exploit\_1 files

### am...@chromium.org (2024-05-10)

exploit 2 files

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075849)*
