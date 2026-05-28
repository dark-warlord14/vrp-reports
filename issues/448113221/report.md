# LPE - Arbitrary File Write in Google Chrome Enterprise (MacOS): The GoogleUpdater, which is executed by root, follows symlinks when writing the file settings.dat in the user folder

| Field | Value |
|-------|-------|
| **Issue ID** | [448113221](https://issues.chromium.org/issues/448113221) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Updater |
| **Platforms** | Mac |
| **Reporter** | jo...@gmail.com |
| **Assignee** | wa...@google.com |
| **Created** | 2025-09-29 |
| **Bounty** | $3,000.00 |

## Description

**Summary:** LPE - Arbitrary File Write in Google Chrome Enterprise (MacOS): The GoogleUpdater, which is executed by root, follows symlinks when writing the file settings.dat in the user folder

**Program:** Google VRP

**Vulnerability type:** Privilege Escalation

### Details

**Vulnerability Description**

When accessing [chrome://settings/help](javascript:void(0);) in **Google Chrome Enterprise** - Version 140.0.7339.214 (Official Build) (x86\_64) for MacOS, the **GoogleUpdater.app** ("/Library/Application Support/Google/GoogleUpdater/Current/GoogleUpdater.app/Contents/Helpers/launcher") is executed as root.

The launcher executes the following command:

- /Library/Application\ Support/Google/GoogleUpdater/Current/GoogleUpdater.app/Contents/MacOS/GoogleUpdater --server --service=update --system

Which will execute the following command:

- /Library/Application Support/Google/GoogleUpdater/142.0.7416.0/GoogleUpdater.app/Contents/MacOS/GoogleUpdater --crash-handler --system --database=/Library/Application Support/Google/GoogleUpdater/142.0.7416.0/Crashpad --url=<https://clients2.google.com/cr/report> --annotation=prod=Update4 --annotation=ver=142.0.7416.0 --handshake-fd=5

This will trigger a file read and write of:

- /Users/<User>/Library/Application Support/Google/Chrome/Crashpad/settings.dat

The user has full permissions on the folder **Crashpad** and the file **settings.dat**. This allows the user to create a symbolic link in the folder which will be followed by the **GoogleUpdater** application when writing the file **settings.dat**.

This allows a non-privileged user to obtain a arbitrary file write. However, I did not found a way to control the content of the file.

**Attack Preconditions**

To exploit this issue, an attacker must have access as non-privileged user to the machine.

**Reproduction Steps / POC**

To exploit this issue, perform the following steps:

1. Open **Google Chrome Enterpise**
2. Remove the file **/Users/<User>/Library/Application Support/Google/Chrome/Crashpad/settings.dat**
   if it exists
3. Create the symlink: **ln -sf /tmp/arbitrary\_write /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat**
4. Go to **Help -> About Google Chrome**
5. Verify that the file **/tmp/arbitrary\_write** was created by root

### Attack scenario

Every user in the system independently of their privileges is able to exploit this issue, since the GoogleUpdater will go through every user folder at **/Users**.

This allows a non-privileged user to overwrite any file in the filesystem. However, I did not found a way to control the content of the **settings.dat** file, which means that in the end the impact will depend on the file that the user overwrites.

## Attachments

- [arbitrary-file-write.mov](attachments/arbitrary-file-write.mov) (video/quicktime, 39.1 MB)
- [arbitrary-file-write.png](attachments/arbitrary-file-write.png) (image/png, 489.9 KB)
- [behavior.PNG](attachments/behavior.PNG) (image/png, 451.4 KB)
- [shared.PNG](attachments/shared.PNG) (image/png, 400.6 KB)

## Timeline

### sp...@google.com (2025-09-29)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### ae...@google.com (2025-09-30)

Hi. Thank you for your report.

> Create the symlink: ln -sf /tmp/arbitrary\_write /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat

It looks from the PoC that step 3 already requires root. Can you do this attack as an unprivileged user?

Thank you

### jo...@gmail.com (2025-09-30)

Hi, no root privileges is required,

Let's say I'm the non-privileged user **test**. The PoC would be like this:

1. Open **Google Chrome Enterprise** with user **test**
2. Remove the file **/Users/test/Library/Application Support/Google/Chrome/Crashpad/settings.dat** if it exists. This file is used by Google Chrome, which is executed by the user, so the user **test** has permissions to remove it.
3. Create the symlink using the **test** user: **ln -sf /tmp/arbitrary\_write /Users/test/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat**
4. In the browser opened in the first step, go to **Help -> About Google Chrome**
5. Verify that the file **/tmp/arbitrary\_write** was created by root

In the attachment **arbitrary-file-write.mov** from the original report, it is possible to see that the user **test** is able to overwrite the file **/etc/nfs.conf**, which the user **test** has no write permissions.

### jo...@gmail.com (2025-09-30)

This problem seems to be related with the **Crashpad** handler. Even in the non enterprise version, **Google Chrome** and **Google Updater** for **MacOS** follow symbolic links when accessing the file **/Users/<User>/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat**.

The difference is that in the regular **Google Chrome** for **MacOS** installation, **Google Chrome** and **Google Updater** are executed with user permissions, so there is no security impact in following symbolic links.

However, in the enterprise version **Google Updater** is executed as root, which means following a symbolic link created by the user allows the user to obtain an arbitrary write. As said before, I could not control the content of the file, but it still can overwrite any file in the filesystem.

### ...@google.com (2025-10-01)

Hey,

it looks like the arbitrary file in your PoC video was already created by root. Also, could you share a video PoC demonstrating this attack as an unprivileged user?

### jo...@gmail.com (2025-10-01)

Hi,

This vulnerability allows to create new files or overwrite existent ones. In the PoC video that I sent, I was able to overwrite the the file **/etc/nfs.conf**, which is owned by **root** and a non-privileged user should not be able to modify it. In the PoC video I perform the following commands:

1. **sudo su -** - This command shows that the **test** user does not have **sudo** permissions
2. **ls -la /etc/nfs.conf** - This command shows that the file **/etc/nfs.conf** is owned and only writable by **root**
3. **cat /etc/nfs.conf** - This command shows the content of the file
4. **ls -la /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad** - This command shows that the file **settings.dat** is owned by **test** user
5. **ln -sf /etc/nfs.conf /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat** - This command creates the symbolic link between the file **settings.dat** and **/etc/nfs.conf**
6. **ls -la /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad** - This command shows that the file **settings.dat** is a symbolic link to **/etc/nfs.conf**
7. **Help -> About Google Chrome** in the browser - This will trigger **Google Updater** to overwrite the file **/etc/nfs.conf**
8. **cat /etc/nfs.conf** - This command shows -that the content of the file changed
9. **ls -la /etc/nfs.conf** - This command shows that the file is owned by **root**
10. **xxd /etc/nfs.conf** - This command shows that the content of the file **/etc/nfs.conf** now is a **settings.dat** structure

### jo...@gmail.com (2025-10-01)

Also, I'm trying to send a new video, but I'm getting an error uploading. So I'm sending a screenshot in attachment that shows that this vulnerability also allows non-privileged users to create files and not just overwrite existent ones. In this screenshot I also show using **fs\_usage** that the process that writes **/tmp/arbitrary\_write** is **GoogleUpdater**

### ae...@google.com (2025-10-02)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### ca...@chromium.org (2025-10-02)

norberg: Can you PTAL? This seems similar to crbug.com/40075849 (so I triaged it similar to that) which you fixed. Thanks

### no...@google.com (2025-10-02)

I am CCing additional Omaha team members and Crashpad developers so we can all investigate it appropriately. Looks like a serious issue at first glance, we'll see if we can reproduce it and how to mitigate it.

From the report alone, it stands out as odd to me that Crashpad is trying to use `/Users/$USER/Library` instead of `/Library` given that the command line explicitly tells it to take a look at the root library (note the `--database` flag) and the launcher goes out of its way to disconnect the calling context from the running user. So, how did user identity other than "root" make it to the privileged Crashpad launch? Investigating...

### ma...@chromium.org (2025-10-02)

[#comment11](https://issues.chromium.org/issues/448113221#comment11):

> From the report alone, it stands out as odd to me that Crashpad is trying to use `/Users/$USER/Library` instead of `/Library` given that the command line explicitly tells it to take a look at the root library (note the `--database` flag) and the launcher goes out of its way to disconnect the calling context from the running user. So, how did user identity other than "root" make it to the privileged Crashpad launch? Investigating...

If Updater runs as root and starts Crashpad as root, it shouldn’t be using any user’s ~/Library (except, perhaps, for root’s). The `--database` in [#comment1](https://issues.chromium.org/issues/448113221#comment1) looks correct: root /Library, not any user’s ~/Library.

I don’t think that the `GoogleUpdater --crash-handler --database=/Library/Application Support/Google/GoogleUpdater/142.0.7416.0/Crashpad` process is responsible for this write. Rather, some client (such as `GoogleUpdater --server --service=update --system` itself) may be reaching something like [third\_party/crashpad/crashpad/client/settings.cc `crashpad::Settings::SetUploadsEnabled`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/crashpad/crashpad/client/settings.cc;l=185-199;drc=6aa04653af34215362b911e61d26e5ba7f43701f) ← [components/crash/core/app/crashpad.cc `crash_reporter::SetUploadConsent`](https://source.chromium.org/chromium/chromium/src/+/main:components/crash/core/app/crashpad.cc;l=266-267;drc=d8d26862f9418eb95dacff6313c1fc73f3c98690) ← [chrome/browser/google/google\_update\_settings\_posix.cc `GoogleUpdateSettings::SetCollectStatsConsent`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/google/google_update_settings_posix.cc;l=90;drc=6d5ee197f53b5c2e4beaec0534338965266c12bf) with a database path taken from `HOME` in the environment or something else that considers the home directory of the *real* user instead of the *effective* user.

But that’s not right either. [We had a long, hard, serious talk about hardening measures in `launcher`](https://chromium-review.googlesource.com/c/4117866) to include environment sanitization and setting the ruid to match the euid. And, sure enough, [I do see some very judicious hardening going on in there](https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/mac/launcher_main.c;drc=406947a0f1e0e6b596d387b6b14156f369e8c55d).

If this reproduces readily, it should be easy enough to set a breakpoint on [third\_party/crashpad/crashpad/client/settings.cc `crashpad::Settings::WriteSettings`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/crashpad/crashpad/client/settings.cc;drc=6b98c207facca73446d15164ad3f9a62f4b41d11;l=438-446) to catch the write to a ~/Library path, and then work backwards from there to see where that path is coming from.

### ma...@chromium.org (2025-10-02)

Yes: the code that starts Crashpad for Updater is [chrome/updater/crash\_reporter.cc `updater::StartCrashReporter`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/crash_reporter.cc;l=74,83-88,109-118;drc=6df28980fb3776af5d9095ea59904681c0c50dbb), which does an Updater-specific determination of the database path from [chrome/updater/util/util.cc `updater::EnsureCrashDatabasePath`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/util/util.cc;l=116-121;drc=76c7cb255cf9892ef1f02e80af7c3d8a0a59523c) → [`updater::GetCrashDatabasePath`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/util/util.cc;drc=6b98c207facca73446d15164ad3f9a62f4b41d11;l=110-114) → […] → [chrome/updater/util/mac\_util.mm `updater::GetInstallDirectory`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/util/mac_util.mm;l=272-279;drc=6b98c207facca73446d15164ad3f9a62f4b41d11) → [`updater::GetLibraryFolderPath`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/util/mac_util.mm;drc=6b98c207facca73446d15164ad3f9a62f4b41d11;l=107-121). That entire chain considers updater scope. At system scope, you correctly get a database path in /Library. This is how the `GoogleUpdater --crash-handler` process is started.

Contrast with [chrome/browser/google/google\_update\_settings\_posix.cc `GoogleUpdateSettings::SetCollectStatsConsent`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/google/google_update_settings_posix.cc;l=90;drc=6d5ee197f53b5c2e4beaec0534338965266c12bf), which doesn’t do anything Updater-specific, and winds up calling into Updater-unaware [components/crash/core/app/crashpad.cc `crash_reporter::SetUploadConsent`](https://source.chromium.org/chromium/chromium/src/+/main:components/crash/core/app/crashpad.cc;l=266-267;drc=d8d26862f9418eb95dacff6313c1fc73f3c98690). The database path that this will use will almost certainly be entirely different.

The path that’s used in this situation needs to be corrected, obviously. But I’m also concerned that Chrome’s path service, even when running as root by the hardened launcher, might be returning other paths in the user’s directory to the service running as root. So we should also launch an investigation into where that path is coming from, and if there’s anything that we can do to further sever the link to the user’s home directory when the setuid launcher invokes a program as root.

### wa...@google.com (2025-10-03)

My first thought was that this was a consequence of [issue 447666297](https://issues.chromium.org/issues/447666297), which launches the --unzip-worker subprocess as root but in the wrong scope. (And it will have its own crash handler.) But Mark, are you saying that the updater somehow call SetCollectStatsConsent? I think I understand the point about not allowing the user's home directory to cross the setuid launcher at all, if possible; that could defend against the entire class of mistakes.

### ma...@chromium.org (2025-10-03)

> My first thought was that this was a consequence of [issue 447666297](https://issues.chromium.org/issues/447666297), which launches the --unzip-worker subprocess as root but in the wrong scope. (And it will have its own crash handler.)

Ah, could be that!

> But Mark, are you saying that the updater somehow call SetCollectStatsConsent?

I actually didn’t look for a caller. I assumed that since there’s an implementation, it would be called by something. No?

### wa...@google.com (2025-10-03)

Hm, the unzip worker idea was a good one (and may be a different way to get this result) but I don't think it stands up as a root cause, because this seems to happen even if there's no update to apply (in which case the unzip worker would never get launched). I think the culprit is <https://source.chromium.org/chromium/chromium/src/+/main:chrome/updater/usage_stats_permissions_mac.mm;l=39;drc=6b98c207facca73446d15164ad3f9a62f4b41d11> where the updater is trying to query Chrome's crashpad DB to figure out if it can send usage stats / crash reports or not. (The updater can upload only if Chrome can upload.)

> I assumed that since there’s an implementation, it would be called by something.

I believe the code you linked is called, but I think only by Chrome.

### ma...@chromium.org (2025-10-03)

OK, I’m withdrawing [chrome/browser/google/google\_update\_settings\_posix.cc `GoogleUpdateSettings::SetCollectStatsConsent`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/google/google_update_settings_posix.cc;l=90;drc=6d5ee197f53b5c2e4beaec0534338965266c12bf) from consideration.

In the chat, I mentioned that any `crashpad::Settings` object being initialized, including any `crashpad::CrashReportDatabase::GetSettings`, would also cause the settings file to be created. waffles knows where we’re making such a call. Credit to norberg and noahrose who are aiding the investigation as well.

### jo...@gmail.com (2025-10-03)

Hi everyone,

Yes, this happens even when no update is available.

Also, it is not related to any user environment, since the crash handler goes through every folder at **/Users** individually (see attachment behavior.png).

Afterwards, for every folder at **/Users**, it iterates through all folders at **/Users/USER\_FOLDER/Library/Application Support/Google** (see attachment behavior.png) looking for the folder **Crashpad**.

So basically a user can even use the folder **/Users/Shared/Library/Application Support/Google/RandomFolder/Crashpad** to create the symbolic link **settings.dat** and get the file overwrite (see attachment shared.png).

Also, going to **Help -> About Google Chrome** triggers **GoogleUpdater**, however **GoogleUpdater** is executed from time to time without user interaction.

### ch...@google.com (2025-10-03)

Setting milestone because of s0/s1 severity.

### ma...@chromium.org (2025-10-03)

[#comment18](https://issues.chromium.org/issues/448113221#comment18): Thanks for the additional information. That agrees with our suspected culprit.

### wa...@google.com (2025-10-06)

Greg, can you help me figure out if there is a similar vulnerability on Windows in [this code](https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/setup/google_chrome_behaviors.cc;l=151;drc=13ca199c69edee9777c9089226f23e5a5632e791)? Sketching the worry briefly: if GetDistributionData is called with system privileges, GetSettings can potentially write a settings.dat file as system, traversing a junction or symlink. I think this is only called by the uninstaller, though (is that right)? If so, I would say it's perhaps a surprising side effect but not inherently an additional vulnerability, since the user running some kind of junction attack via their settings.dat path also has to be the one with sufficient privilege to run the uninstaller; but I don't know in what context the uninstaller runs (or how chrome::GetDefaultUserDataDirectory handles elevation) very well, so I figured it may be wise to check with you.

### gr...@chromium.org (2025-10-07)

Hi Josh. As you point out, this particular call is during uninstall. Uninstalling a per-machine Chrome requires admin rights (ordiarily acquired via UAC), so I agree that the attacker needs to be admin in order to pull this off.

### jo...@gmail.com (2025-10-07)

Hi everyone,

Just to add my perspective on the uninstaller discussion.

While it's true that on personal machines users typically need administrative rights to install/uninstall applications, the situation is different in corporate environments.

Many organizations now use solutions like Company Portal (Intune) for Windows or Jamf for macOS, which allow non-privileged users to install/remove applications without needing local admin rights.

In such environments, if an installer/uninstaller interacts with user controllable folders/files it may allow a user to elevate privileges.

### dx...@google.com (2025-10-10)

Project: crashpad/crashpad  

Branch:  main  

Author:  Joshua Pawlicki [waffles@chromium.org](mailto:waffles@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7022792>

crashpad: Introduce a new SettingsReader type for read-only access

---


Expand for full commit details
```
     
    Bug: 448113221 
    Change-Id: I0e7bc9513fdbc1c22b3d94a82efeb0adee6cb04c 
    Reviewed-on: https://chromium-review.googlesource.com/c/crashpad/crashpad/+/7022792 
    Reviewed-by: Mark Mentovai <mark@chromium.org> 
    Commit-Queue: Joshua Pawlicki <waffles@chromium.org>

```

---

Files:

- M `client/crash_report_database.h`
- M `client/crash_report_database_generic.cc`
- M `client/crash_report_database_mac.mm`
- M `client/crash_report_database_win.cc`
- M `client/settings.cc`
- M `client/settings.h`
- M `client/settings_test.cc`
- M `util/misc/initialization_state.h`

---

Hash: [b9d38f35eb99685dfd2c5156a5f629a486568f64](https://chromiumdash.appspot.com/commit/b9d38f35eb99685dfd2c5156a5f629a486568f64)  

Date: Fri Oct 10 21:03:04 2025


---

### dx...@google.com (2025-10-13)

Project: chromium/src  

Branch:  main  

Author:  Joshua Pawlicki [waffles@chromium.org](mailto:waffles@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7036932>

Update Crashpad to b9d38f35eb99685dfd2c5156a5f629a486568f64

---


Expand for full commit details
```
     
    2060cc8f6c5d Rename third_party/linux/README.crashpad to .md 
    b9d38f35eb99 crashpad: Introduce a new SettingsReader type for read-only 
                 access 
     
    Bug: 448113221 
    Change-Id: I2bb399c30a99e39e80c640e4b815a7d31d48abe2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7036932 
    Commit-Queue: Joshua Pawlicki <waffles@chromium.org> 
    Auto-Submit: Joshua Pawlicki <waffles@chromium.org> 
    Commit-Queue: Mark Mentovai <mark@chromium.org> 
    Reviewed-by: Mark Mentovai <mark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1529062}

```

---

Files:

- M `third_party/crashpad/README.chromium`
- M `third_party/crashpad/crashpad/client/crash_report_database.h`
- M `third_party/crashpad/crashpad/client/crash_report_database_generic.cc`
- M `third_party/crashpad/crashpad/client/crash_report_database_mac.mm`
- M `third_party/crashpad/crashpad/client/crash_report_database_win.cc`
- M `third_party/crashpad/crashpad/client/settings.cc`
- M `third_party/crashpad/crashpad/client/settings.h`
- M `third_party/crashpad/crashpad/client/settings_test.cc`
- R `third_party/crashpad/crashpad/third_party/linux/README.md`
- M `third_party/crashpad/crashpad/util/misc/initialization_state.h`

---

Hash: [d07f1a28289ee29a6f72e51d8d092db281a1de02](https://chromiumdash.appspot.com/commit/d07f1a28289ee29a6f72e51d8d092db281a1de02)  

Date: Mon Oct 13 19:26:04 2025


---

### dx...@google.com (2025-10-13)

Project: chromium/src  

Branch:  main  

Author:  Joshua Pawlicki [waffles@chromium.org](mailto:waffles@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7036620>

Updater: Use read-only crashpad SettingsReader.

---


Expand for full commit details
```
     
    Bug: 448113221 
    Change-Id: I6323e5befb738ca0144dbd0601ccb3b7788e108a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7036620 
    Commit-Queue: Sorin Jianu <sorin@chromium.org> 
    Auto-Submit: Joshua Pawlicki <waffles@chromium.org> 
    Reviewed-by: Sorin Jianu <sorin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1529104}

```

---

Files:

- M `chrome/updater/usage_stats_permissions_mac.mm`

---

Hash: [bbecc30052b609e7c50b5080dc5a6f8f35684ab4](https://chromiumdash.appspot.com/commit/bbecc30052b609e7c50b5080dc5a6f8f35684ab4)  

Date: Mon Oct 13 20:33:31 2025


---

### ch...@google.com (2025-10-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### wa...@google.com (2025-10-15)

I believe this is fixed in GoogleUpdater 143.0.7473.0, which is rolling out now. The rollout is currently to 0.01% of users.

Tips for verification:

You can trick an installed GoogleUpdater into being in this 0.01% by running this command (this will only work for this particular release):

`sudo sed -i '' 's/1:scr[^"]*/1:scr\/3b0r:3b0x@0.5/' /Library/Application\ Support/Google/GoogleUpdater/prefs.json; sudo sed -i '' 's/last_checked":"1/last_checked":"/' /Library/Application\ Support/Google/GoogleUpdater/prefs.json`

Within an hour after that (provided the device does not go to sleep), 143.0.7473.0 should be downloaded and installed. (i.e. `/Library/Application\ Support/Google/GoogleUpdater/143.0.7473.0` exists)

After another 1 to 2 hours, 143.0.7473.0 should have completed its self-testing and taken over as the active updater:

```
~ % sudo grep -o '"active_version":"[^"]*"' /Library/Application\ Support/Google/GoogleUpdater/prefs.json
"active_version":"143.0.7473.0"

```

Then, attempting to reproduce the issue:

```
~ % rm -rf /tmp/arbitrary_write; rm /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat; mkdir -p /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad; ln -sf /tmp/arbitrary_write /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad/settings.dat; ls -la /tmp/arbitrary*; ls -la /Users/$USER/Library/Application\ Support/Google/Chrome/Crashpad
zsh: no matches found: /tmp/arbitrary*
total 0
drwx------@  7 waffles  primarygroup   224 Oct 15 19:13 .
drwx------  69 waffles  primarygroup  2208 Oct 15 19:11 ..
drwxr-xr-x   2 waffles  primarygroup    64 Oct  4 10:53 attachments
drwxr-xr-x   3 waffles  primarygroup    96 Oct  7 14:36 completed
drwxr-xr-x   2 waffles  primarygroup    64 Oct  7 14:31 new
drwxr-xr-x   2 waffles  primarygroup    64 Oct  7 14:36 pending
lrwxr-xr-x   1 waffles  primarygroup    20 Oct 15 19:13 settings.dat -> /tmp/arbitrary_write

```

...Navigate to chrome://help, observe the update check...

...and then confirming that no file is created:

```
~ % ls -la /tmp/arbitrary_write
ls: /tmp/arbitrary_write: No such file or directory

```

### wa...@google.com (2025-10-15)

Note: GoogleUpdater releases from near-tip-of-tree, not from Chromium release branches; no merges are necessary.

### ch...@google.com (2025-10-18)

Security Merge Request Consideration: Requesting merge to extended stable (M140) because latest trunk commit (1529104) appears to be after extended stable branch point (1496484).
Security Merge Request Consideration: Requesting merge to stable (M141) because latest trunk commit (1529104) appears to be after stable branch point (1509326).
Security Merge Request Consideration: Requesting merge to beta (M142) because latest trunk commit (1529104) appears to be after beta branch point (1522585).
Security Merge Request - Manual Review: Merge review required: M140 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M141 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M142 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141, 142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### wa...@google.com (2025-10-19)

Hi team, no merge is necessary. The fix is in GoogleUpdater, not in Google Chrome, and our next release will be from 143.

### sp...@google.com (2025-10-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
limited impact privilege escalation (no control of data written) with a high quality report


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2025-10-27)

The NextAction date has arrived: 2025-10-27
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ch...@google.com (2026-01-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/448113221)*
