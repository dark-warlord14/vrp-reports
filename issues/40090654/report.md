# Security: ChromeOS persistent command execution as root

| Field | Value |
|-------|-------|
| **Issue ID** | [40090654](https://issues.chromium.org/issues/40090654) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | mo...@chromium.org |
| **Created** | 2018-03-01 |
| **Bounty** | $33,337.00 |

## Description

**VULNERABILITY DETAILS**  

Using vulnerabilities in the settingsPrivate API and crash\_reporter, it is possible for a user to break out of the ChromeOS sandbox and execute commands with full root privileges

The exploit requires manual 'installation', and cannot be triggered from guest mode. Once installed the payload will be triggered every hour until the machine is powerwashed.

It is necessary that "Automatically send diagnostic and usage data to Google" be enabled for crash\_sender to run.

## Local File Write

By directly calling the settingsPrivate.setPref function it is possible to set the user's download directory to above /home/chronos/user/Downloads. If the targeted directory does not exist, it will be created when the first file is downloaded. Only automatic downloads will be placed in this directory, if the user is prompted for a filename, files will be placed in the normal Downloads directory.

The following javascript snippet, when executed from the chrome://settings page, will set the Downloads directory to /home/chronos/user/crash

chrome.settingsPrivate.setPref('download.default\_directory', '/home/chronos/user/crash', '1', console.log)

## Command Execution as root (jailed)

By dropping a crafted .meta file in the crash directory, it is possible to break out of crash\_sender and gain command execution as root in a jail.

When parsing .meta files, crash\_sender will extract all key-values which start with 'upload\_' [1]. The extraction is performed using sed with user controlled data interpolated into the sed expression [2]. GNU sed supports the 'ep' suffix which will execute the result of the replace.

The following line in a .meta file will break out of the sed expression ('/p;'), and create a new expression ('s^.\*^[...]^ep;'), followed by fixing up the original expression ('/'). When executed as below, the bash script will be executed by sed as root but restricted by the jail [3]. The initial sed used to extract the user data in the first place breaks on [[:space:]], so spaces are replaced with ${IFS} which are expanded when executed by sed (which uses system() underneath).

upload\_/p;s^.\*^setsid${IFS}bash${IFS}/home/chronos/user/crash/payload.sh${IFS}&^ep;/=1

After interpolation, the sed expression to be run is as follows:

sed -n "/^/p;s^.\*^setsid${IFS}bash${IFS}/home/chronos/user/crash/payload.sh${IFS}&^ep;/[[:space:]]\*=/{s:^[^=]\*=::p;q}" "${file}"

It is necessary to have an otherwise well formed .meta file for this to be executed, and I have attached one at exploit.meta. exploit.dmp is an empty file but is necessary since the file extension is used and required by crash\_sender.

Once the attached files have been dropped, the user can immediately invoke the crash\_sender by using crosh (upload\_crashes), or wait for the periodic\_scheduler to execute crash\_sender (every hour). The result will be the same either way.

## Jail breakout

At this point we have root command execution with incomplete capabilities, in a new namespace. We have access to dbus from inside the jail so we can use this to break out. We use Upstart's dbus endpoint to execute a new job with a custom PATH environment, which can be used to exploit an existing Upstart job that does not have a full path in it's definition. I chose ureadahead for this, since it does not seem to already be running. ureadahead.conf [5] executes the ureadahead binary without a full path, so we can abuse this to execute our own binary as full root outside the jail. We first drop our payload named ureadahead under /run/containers/android\_[random]/root/dev which is mounted rw and exec. Then we can trigger the dbus endpoint using dbus-send, with a PATH pointing to this directory.

The payload to be written drops and executes a modified dropbear daemon to allow the user to then log in to the machine. Dropbear has been modified to allow a hardcoded password of EXPLOIT, as a proof of concept since /etc/shadow has not been populated. The firewall is not modified by the proof of concept so it's necessary to use the Secure Shell extension to log in to localhost. Since the dropper script is already running as root, any other payload can be used here.

## Persistence

crash\_sender looks in both the user crash directory and also /var/spool/crash [9]. We can drop the same exploit files into this directory and mark them as immutable (chattr +i). This will stop crash\_sender from successful deletion of the crash files upon crash sending, meaning that the vulnerability will be re-exploited whenever the periodic\_scheduler triggers crash\_sender, including after boot. This has not been fully tested.

## Reproduction Steps

1. Browse to chrome://settings
2. Execute the following snippet in the console chrome.settingsPrivate.setPref('download.default\_directory', '/home/chronos/user/crash', '1', console.log)
3. Download the attachments exploit.meta, exploit.dmp, payload.sh. I used Google Drive to ensure that the files are automatically downloaded and I am not prompted
4. OPTIONAL At this point I disabled WiFi to stop the false crash spamming the Google crash servers, this is not a requirement of the exploit
5. Wait for periodic\_scheduler or open crosh and execute upload\_crashes
6. crash\_sender will wait up to 30 seconds before sending, after which the payload will trigger. The screen should flash to indicate successful execution
7. dropbear should now be running, visible in 'top' from crosh, or by connecting to localhost with the ssh client using root:EXPLOIT as credentials
8. OPTIONAL persistence can be obtained by copying the crash files to /var/spool/crash, fixing the full paths and using chattr +i to stop deletion

## payload.sh explanation

payload.sh starts inside the jail, as executed by sed. We first use the SetFlagsForUser dbus endpoint to add a fallback bash shell to the user's profile for debugging and chronos level command execution. It is necessary to restart chrome for this flag to take effect.

The script will then check that it is the only instance running, after which it will use the org.chromium.PowerManager.SetScreenBrightnessPercent dbus endpoint to flash the screen to indicate successful execution.

The script then finds the randomized executable path, and drops a second script named ureadahead, marks it executable and triggers the Upstart job with the custom PATH environment variable.

The ureadahead script drops the modified dropbear binary and a host key and executes dropbear.

## Bonus Privilege escalation

I could not get this privilege escalation to work in the context of the crash\_sender command execution due to TTY issues, but I am reporting it anyway since I tried. This privilege escalation allows for any user to escalate their privileges to unrestricted root.

There is a missing \ character in capture\_utility.sh [6] which causes the value of ht\_location to be executed. This binary can be called via debugd's dbus interface [7] by any user [8], regardless of whether or not the machine is in dev mode. The injection forces the executed binary to have the following 3 arguments: "!= below ]". If the executed binary is 'vi', execution will not fail, after which the vi ':!' command can be used to execute an external command as root. This has been automated and attached in the script privesc.sh.

When executed from crosh this script will return an interactive root shell.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/crash_sender#369>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/crash_sender#241>  

[3] <https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/crash_sender#775>  

[4] <https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/crash_sender#293>  

[5] I couldn't find this in master, but this file is representative of what is on my device.  

<https://chromium.googlesource.com/chromiumos/platform/init/+/firmware-rambi-5216.B/ureadahead.conf#20>  

[6] <https://chromium.googlesource.com/chromiumos/platform2/+/master/debugd/src/helpers/capture_utility.sh#480>  

[7] <https://chromium.googlesource.com/chromiumos/platform2/+/master/debugd/dbus_bindings/org.chromium.debugd.xml#536>  

[8] <https://chromium.googlesource.com/chromiumos/platform2/+/master/debugd/share/org.chromium.debugd.conf>  

[9] <https://chromium.googlesource.com/chromiumos/platform2/+/master/crash-reporter/crash_sender#757>

**VERSION**  

ChromeOS  

Version 64.0.3282.169 (Official Build) (64-bit)  

Platform 10176.73.0 (Official Build) stable-channel eve  

Firmware Google\_Eve.9584.107.0  

Channel Stable  

Google Pixelbook

## Attachments

- [exploit.meta](attachments/exploit.meta) (application/octet-stream, 140 B)
- [exploit.dmp](attachments/exploit.dmp) (application/octet-stream, 0 B)
- [payload.sh](attachments/payload.sh) (text/plain, 368.7 KB)
- [privesc.sh](attachments/privesc.sh) (text/plain, 568 B)

## Timeline

### ke...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### jo...@chromium.org (2018-03-01)

Thanks for the report! We'll be breaking this one up shortly.

### jo...@chromium.org (2018-03-01)

Actually, given the requirement for manual intervention, and without a UXSS to get into chrome:settings, this probably qualifies as High. Still planning on fixing immediately.

### xz...@chromium.org (2018-03-01)

[Comment Deleted]

### mo...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2018-03-01)

Is it possible to be CCd on Blockedon bugs? I am interested in following the progress.

### jo...@chromium.org (2018-03-01)

Yeah. Micah, feel free to cc Rory on the blocking bugs.

### mo...@chromium.org (2018-03-01)

[Comment Deleted]

### mo...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### mn...@chromium.org (2018-03-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-02)

[Comment Deleted]

### va...@chromium.org (2018-03-02)

[Empty comment from Monorail migration]

### jo...@chromium.org (2018-03-02)

Assigning to Micah for tracking purposes for now.

### va...@chromium.org (2018-03-05)

[Comment Deleted]

### ke...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

[Monorail components: Internals]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

mortonm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-31)

mortonm: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-04-19)

Is this going to stable in M-66? Is this fixed now?

### mo...@chromium.org (2018-04-19)

Still blocked on crbug.com/818032, so we're leaving the bug open for now. However, exploit chain was broken by a fix that went in in crbug.com/817993

### mn...@chromium.org (2018-04-20)

+jrbarnette@ FYI

### sh...@chromium.org (2018-05-01)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2018-05-08)

That last blocker is now marked as fixed -- is there more work remaining on this?

### mo...@chromium.org (2018-05-08)

I can't tell if that bug was purposely marked as fixed by mnissler@ or if somehow sheriff bot marked it fixed when it shouldn't have. I'll check with mnissler@ and mark this one as fixed as well if the other one is indeed fixed.

### mo...@chromium.org (2018-05-08)

Nope, not yet fixed. Sheriff bot got a little too excited I guess

### mo...@chromium.org (2018-05-16)

Last blocking bug, crbug.com/818032, has been marked as fixed (intentionally this time). Marking this as fixed as well.

### sh...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

Congratulations rory@ - the VRP panel decided to award $33,337 for this chain.

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2018-06-16)

Thanks!

### sh...@chromium.org (2018-08-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-08-23)

This issue was migrated from crbug.com/chromium/817920?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/817993, crbug.com/chromium/818032, crbug.com/chromium/818135, crbug.com/chromium/818138]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090654)*
