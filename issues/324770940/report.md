# Chrome Update Elevation of Privilege

| Field | Value |
|-------|-------|
| **Issue ID** | [324770940](https://issues.chromium.org/issues/324770940) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2020-1170 |
| **Reporter** | do...@pksecurity.io |
| **Assignee** | ga...@chromium.org |
| **Created** | 2024-02-11 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Chrome Update Elevation of Privilege

---

### Bug location

#### Which product or website have you found a vulnerability in?

Google Chrome

#### Which URL (or repository) have you found the vulnerability in?

N/A

---

### The problem

#### Please describe the technical details of the vulnerability

### VULNERABILITY SUMMARY

An EoP vulnerability exists in Chrome Installer, which runs automatically during the Chrome update process.

### VERSION

Chrome: Last Build

Tested OS Version: Windows 10 x64 22H2 Last Build

### VULNERABILITY DETAIL

During the Google update process, there is a process to get and install the latest version of Installer. This all happens automatically and runs with SYSTEM privileges.
As the installer installs the new version, it writes a log to %windir%\Temp\chrome\_installer.log.
Below is the code where the vulnerability occurs. (<https://github.com/chromium/chromium/blob/b1f5b97f28a8838c4d511af9718e4a4ee7af1b57/chrome/installer/util/logging_installer.cc#L45>)

```
  TruncateResult result = LOGFILE_UNTOUCHED;

  int64_t log_size = 0;
  if (base::GetFileSize(log_file, &log_size) &&
      log_size > kMaxInstallerLogFileSize) {
    // Cause the old log file to be deleted when we are done with it.
    uint32_t file_flags = base::File::FLAG_OPEN | base::File::FLAG_READ |
                          base::File::FLAG_WIN_SHARE_DELETE |
                          base::File::FLAG_DELETE_ON_CLOSE;
    base::File old_log_file(log_file, file_flags);

    if (old_log_file.IsValid()) {
      result = LOGFILE_DELETED;
      base::FilePath tmp_log(log_file.value() + FILE_PATH_LITERAL(".tmp"));
      // Note that base::Move will attempt to replace existing files.
      if (base::Move(log_file, tmp_log)) {
        int64_t offset = log_size - kTruncatedInstallerLogFileSize;
        std::string old_log_data(kTruncatedInstallerLogFileSize, 0);
        int bytes_read = old_log_file.Read(offset, &old_log_data[0],
                                           kTruncatedInstallerLogFileSize);
        if (bytes_read > 0 &&
            (bytes_read ==
                 base::WriteFile(log_file, &old_log_data[0], bytes_read) ||
             base::PathExists(log_file))) {
          result = LOGFILE_TRUNCATED;
        }
      }
    } else if (base::DeleteFile(log_file)) {
      // Couldn't get sufficient access to the log file, optimistically try to
      // delete it.
      result = LOGFILE_DELETED;
    }
  }

  return result;
}

```

As we can see in the code above, when the size of %windir%\Temp\chrome\_installer.log exceeds kMaxInstallerLogFileSize (1MB), it moves the existing log file to a temporary path.
However, in Windows, the %windir%\Temp path has unusual permissions characteristics that are different from other directories.
The peculiarity is that the normal user cannot read subfiles, but can create, delete, and write to them.
This means that an attacker can manipulate the size of the log file to be over 1 MB, which can cause chrome\_installer.log to be deleted in SYSTEM context.
Attackers can also set oplock on those files, giving them fine-grained control over this process.

This behavior is performed with SYSTEM privileges, and there is currently known primitive in the latest version of Windows that can achieve EoP to SYSTEM via high privilege file deletion.
Below is a description of the primitives, followed by their implementations.
<https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks>
<https://github.com/thezdi/PoC/tree/master/FilesystemEoPs>

In particular, the vulnerability related with this log file looks very similar to CVE-2020-1170, a vulnerability that has been seen in Windows Defender in the past.
<https://itm4n.github.io/cve-2020-1170-windows-defender-eop/>

### PATCH SUGGESTION

The most intuitive patch is to change the DACL for the chrome\_installer.log file.
Changing the permissions on that file so that normal users can't write and delete it will fix the problem.
Since normal users cannot query the %windir%\Temp subfiles and directories, including a sufficiently secure random number in the filename may be an option.

### Reference

Exploiting Windows Symbolic Link - <https://nixhacker.com/understanding-and-exploiting-symbolic-link-in-windows/>
File deletion to EoP - <https://www.zerodayinitiative.com/blog/2022/3/16/abusing-arbitrary-file-deletes-to-escalate-privilege-and-other-great-tricks>
File deletion to EoP (Implemetation) - <https://github.com/thezdi/PoC/tree/master/FilesystemEoPs>
CVE-2020-1170 - <https://itm4n.github.io/cve-2020-1170-windows-defender-eop/>

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

It can be exploited by an attacker to gain SYSTEM privileges on a Windows PC with Google Chrome.

---

### The cause

#### What version of Chrome have you found the security issue in?

Latest version (<https://github.com/chromium/chromium/blob/b1f5b97f28a8838c4d511af9718e4a4ee7af1b57/chrome/installer/util/logging_installer.cc>)

#### Is the security issue related to a crash?

No

#### Choose the type of vulnerability

Privilege Escalation

#### How would you like to be publicly acknowledged for your report?

Kim Dong-uk (@justlikebono)

## Timeline

### wf...@chromium.org (2024-02-12)

thank you for your report. if I am correct in my understanding this doesn't seem to provide arbitrary file delete but delete of a very specific file, in fact I can't quite see how an attacker would convert this into something that might be used to affect our users' safety.

sorin, I'm assigning this bug to you as you recently looked at temp files in the installer. I am giving it a tentative security severity of medium (S2) given the primitive it provides and the pre-reqs.

### fo...@chromium.org (2024-02-12)

Based on the description if the only thing the code can delete is an existing `chrome_installer.log` in the root of the `Temp` folder I can't see how it's exploitable unless NTFS symbolic links are enabled which requires either an admin process or a non-default configuration such as an admin configuration change or developer mode to be enabled. There's no point defending again an admin process (and by extension split-token UAC user) and we generally don't fix issues that only present themselves in non-default configurations.

That said, if symbolic links are enabled then it's possible (I've not verified however) that the `base::Move` might allow you to get an arbitrary file write primitive as you could write an over large file as the old log file and them symlink `chrome_installer.log.tmp` which would be a much worse security vulnerability. It could probably even be converted to an arbitrary read.

Unless there's an obvious exploit primitive for the original bug without needing a non-default configuration I wouldn't consider this high severity. If you wanted to fix it anyway I'm not sure just adding a random component to the name is worth it. The name has to be consistent between runs of the updater otherwise this code is meaningless, therefore that number would have to either be stored somewhere or generated using machine specific information. In that case you might as well just always write the log file with a randomly chosen per-run name and remove this code entirely, but then you'll likely end up spamming log files into `Temp`.

### do...@pksecurity.io (2024-02-13)

There's a big misconception.
CVE-2020-1170, the case I mentioned earlier, also involved a deletion of a specific file "C:\Windows\Temp\MpCmdRun.log" that led to a SYSTEM EoP.
Deletions in SYSTEM context on files with write/delete permissions for normal users can always lead to EoP as SYSTEM due to tricks of the file system.
One known trick is that object symlinks, unlike NTFS symlinks, do not require administrator privileges.
An explanation of this can be found in the references in the main text.
(https://nixhacker.com/understanding-and-exploiting-symbolic-link-in-windows/)
In fact, many Windows services are being exploited to delete files with SYSTEM privilege.

+)Also, for the patching solution, modifying the DACL for chrome_installer.log is more recommended.

### fo...@chromium.org (2024-02-13)

Certainly there are potential scenarios that could result in following a mount point if a file is deleted. In the example you give of CVE-2020-1170 the Windows Defender code converts the delete into a recursive delete when it encounters a directory. This can result in following the mount point if you replaced the log file with directory which is definitely exploitable.

However, the Chromium code base is not Windows Defender. In this case a call is made to `base::DeleteFile`. The underlying code does support recursive deletion, however calling `base::DeleteFile` should not enable this recursive behavior, you need to call `base::DeletePathRecursively` to enable it. What this means is that if you replace the file with mount point directory it'll generally just delete the mount point, it wouldn't follow the symlink.

That being said, having poked around at some of the underlying APIs I have sufficient concern that we should fix it regardless, I still don't think it's a serious vulnerability. Also, changing the DACL wouldn't fix the issue. The way the security is configured for `Temp` ensures that as long as it was SYSTEM which created the log file, then a normal user should have no rights to the file to delete it or modify it. For example, on my machine the DACL for the log file is:

```
<Owner> : NT AUTHORITY\SYSTEM
<Group> : NT AUTHORITY\SYSTEM
<DACL> (Auto Inherited)
BUILTIN\Administrators: (Allowed)(Inherited)(Full Access)
NT AUTHORITY\SYSTEM: (Allowed)(Inherited)(Full Access)

```

There is an inherent race in the code which would allow a user to drop the file, either by creating it before Chrome is ever installed, or exploiting the window of time between the call to `base::Move` and when a new file is created. The latter approach would be made pretty difficult as you'd have to wait until the log got to the correct size and write the file at the exact moment it is moved.

I think the only realistic solution is to either generate a random name, or write the log file into a location which isn't accessible by a normal user such as the Chrome installation directory in `Program Files`.

### do...@pksecurity.io (2024-02-13)

I agree with your judgment.
However, treating this as a vulnerability that simply involves deleting one specific file is a significant misstep.

### fo...@chromium.org (2024-02-13)

You're welcome to provide a working PoC to demonstrate impact if you'd like as I could certainly be wrong in my assessment. Also things can change in the underlying OS which make something which isn't usefully exploitable into something which has much more serious impact which is why I'd advocate for it to be fixed.

### gr...@chromium.org (2024-02-13)

one benefit of putting the file in system Temp is that it's there even if 1) installation failed and 2) after chrome is uninstalled. if i put on my time-traveling hat, these might be the rationale for why it's put there.

the issue is that we shouldn't delete anything in Temp? are we safe if we just stop deleting the file and instead use `SetFileInformationByHandle(..., FILE_END_OF_FILE_INFO, ...)` or similar to shrink it?

### wa...@chromium.org (2024-02-13)

re: comment #8, I see the benefit to keeping the log file around a bit, but I don't quite understand why we can't leak a log file in the Chrome dir if installation fails. Is the issue that the Program Files\Chrome directory is deleted during installation rollback after a failure? Or that we don't want to leak the log file indefinitely?

Greg, what do you think about putting the log file into C:\Program Files (x86)\Google\GoogleUpdater? The updater will eventually remove it when it self-uninstalls, but the window for a failed installation should still be large enough that it can be captured for debugging.

### gr...@chromium.org (2024-02-13)

we try not to leave a `%ProgramFiles%\Google\Chrome` directory behind if install fails. also, we start logging early in the process before we've created the install directory.

the `GoogleUpdater` dir works for Google Chrome. what should we do for chromium?

will shrinking the file in `Temp` (without deleting it) be good enough?

### pe...@google.com (2024-02-13)

Setting milestone because of s2 severity.

### pe...@google.com (2024-02-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-02-27)

sorin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-03-13)

sorin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### wa...@chromium.org (2024-03-18)

> the GoogleUpdater dir works for Google Chrome. what should we do for chromium?

Maybe C:\Program Files (x86)\Chromium\ChromiumUpdater\updater.log ? I'm not sure this is a good idea in the first place. But that's where the Chromium-branded updater goes.

### so...@chromium.org (2024-03-18)

I am setting the status as `new` for re-triaging this one.

### dc...@chromium.org (2024-03-19)

It's hard to see how this would be more than medium. It still seems nice to fix though.

> That being said, having poked around at some of the underlying APIs I have sufficient concern that we should fix it regardless, I still don't think it's a serious vulnerability.

forshaw@, can you elaborate on the concerns here? Is it because the implementation details of `base::DeleteFile()` might change at some point, or are there other potential issues?

At least based on the "delete a single file with a fixed path" perspective, this seems pretty hard to exploit. I'm curious if you think being able to hijack the location (or exploit the timing race) would be problematic for other reasons though?

### fo...@chromium.org (2024-03-19)

From my understanding `base::DeleteFile` will ultimately call the Win32 API `RemoveDirectory` to delete the directory if you replaced the log file with a mount point (which needs to be a directory to function). By default this API does not follow the mount point so if you replace the log with one so all it'll do is delete the mount point itself, not what it targets.

However, looking at the implementation of `RemoveDirectory` in more detail there are scenarios where it might be possible to get it to make calls into a kernel driver (the mount point manager) when deleting a mount point with a specific target name. Who knows if that might be an issue if done from a privileged user. There also looks to be a race condition if the directory has a non-standard reparse point which might be exploitable to delete a single directory somewhere else. The recommendation for a fix is just down to `RemoveDirectory` being more complex then it should be.

However, at worst these complex behavior would allow for a single *empty* directory to be deleted somewhere on the file system. That has the potential to be exploitable, but I don't know of any public technique to do so. And even then the default security of `Temp` should preclude trivial exploitation.

### do...@pksecurity.io (2024-04-17)

deleted

### gr...@chromium.org (2024-04-18)

@forshaw: wdyt of my question in comment 11 -- will shrinking the file in Temp (without deleting it) be good enough? we could change `TruncateLogFileIfNeeded` so that it reads data from the end of the file, overwrites the beginning of the file with that data, then truncates the file; all via one handle to it.

### do...@pksecurity.io (2024-05-14)

Any updates for this issue?

### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: main

commit 1c2359677af25b505a825e714d36fed4c83e00d5
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue Jul 30 18:53:45 2024

    chrome installer: log in the secure temp directory instead of DIR_TEMP
    
    The chrome installer now uses `%systemroot%\SystemTemp` by default as
    the logging directory for system installs, since it is more secure than
    DIR_TEMP.
    
    Fixed: 324770940,356064205
    Change-Id: I93633ddbc6042008db0851338f351990d2c3f406
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5747320
    Commit-Queue: S Ganesh <ganesh@chromium.org>
    Reviewed-by: Will Harris <wfh@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1335016}

M       chrome/installer/util/logging_installer.cc

https://chromium-review.googlesource.com/5747320


### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit f77951dcb735d44fd852ff0ab7ce708dab0ceef4
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue Aug 13 12:36:13 2024

    chrome installer: log in the secure temp directory instead of DIR_TEMP
    
    The chrome installer now uses `%systemroot%\SystemTemp` by default as
    the logging directory for system installs, since it is more secure than
    DIR_TEMP.
    
    (cherry picked from commit 1c2359677af25b505a825e714d36fed4c83e00d5)
    
    Fixed: 324770940,356064205
    Change-Id: I93633ddbc6042008db0851338f351990d2c3f406
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5747320
    Commit-Queue: S Ganesh <ganesh@chromium.org>
    Reviewed-by: Will Harris <wfh@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1335016}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5785025
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#990}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       chrome/installer/util/logging_installer.cc

https://chromium-review.googlesource.com/5785025


### do...@pksecurity.io (2024-08-14)

deleted

### am...@chromium.org (2024-08-15)

Hello, now that this issue is resolved, it is in the queue for assessment for potential reward at a VRP panel session.
A reward decision will be updated directly on the bug after a reward decision has been made.
CVEs are issued at the time the fix ships in a Stable channel update of Chrome.

For more information see: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>
<https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#how-do-i-know-if-my-bug-report-is-possibly-eligible-for-a-vrp-reward>

### sp...@google.com (2024-08-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
reward for lower impact local privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Thank you for the report. The reward amount was decided lower impact and very narrow potential for exploitability here. Since we were able to make a security relevant change, we did want to extend a VRP reward for your effort.

### ap...@google.com (2024-09-12)

Project: website
Branch: main

commit cd5742159eae701e0bf078a38e4e63979352c891
Author: S. Ganesh <ganesh@chromium.org>
Date:   Thu Sep 12 12:27:35 2024

    chrome installer: update the log location in the documentation
    
    The log is now generated in the secure temp directory for `system`
    installs.
    
    Bug: 324770940,356064205,366249599
    Change-Id: I626492b1424d829ad8084b6587f1dbaecf96b9a2
    Reviewed-on: https://chromium-review.googlesource.com/c/website/+/5856050
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Commit-Queue: Daniel Cheng <dcheng@chromium.org>
    Reviewed-by: Daniel Cheng <dcheng@chromium.org>

M       site/administrators/configuring-other-preferences/index.md
M       site/developers/testing/windows-installer-tests/index.md

https://chromium-review.googlesource.com/5856050


### ap...@google.com (2024-09-13)

Project: chromium/src
Branch: main

commit 554a0097525f5c22fe4e389e7cd128040af2ff5b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Fri Sep 13 09:29:38 2024

    Roll Website from 8f1eff86f2c6 to cd5742159eae (1 revision)
    
    https://chromium.googlesource.com/website.git/+log/8f1eff86f2c6..cd5742159eae
    
    2024-09-12 ganesh@chromium.org chrome installer: update the log location in the documentation
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/website-chromium
    Please CC dpranke@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Website: https://bugs.chromium.org/p/chromium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:324770940,chromium:356064205,chromium:366249599
    Tbr: dpranke@google.com
    Change-Id: I297f783f2d1716aa173ec75016fbf3e8758ed522
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5858669
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1355077}

M       DEPS
M       docs/website

https://chromium-review.googlesource.com/5858669


### ap...@google.com (2024-09-23)

Project: chromium/src
Branch: main

commit 51578a451179da179d3190e07f34b59edfcec523
Author: Jinyoung <hur.ims@navercorp.com>
Date:   Mon Sep 23 23:43:52 2024

    chrome installer: Update README.md regarding log file path
    
    Update the doc according to the changed behavior, https://chromium-review.googlesource.com/c/chromium/src/+/5747320.
    
    Bug: 324770940
    Change-Id: Ie8e1078facfec5fecab1f50210e77dcc00f7277a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5872170
    Reviewed-by: S Ganesh <ganesh@chromium.org>
    Commit-Queue: Jinyoung Hur <hur.ims@navercorp.com>
    Cr-Commit-Position: refs/heads/main@{#1359067}

M       chrome/installer/mini_installer/README.md

https://chromium-review.googlesource.com/5872170


### pe...@google.com (2024-11-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/324770940)*
