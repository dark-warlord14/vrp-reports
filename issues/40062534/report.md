# Security: Directory Picker Dialog gives access to write .exe/.bat files

| Field | Value |
|-------|-------|
| **Issue ID** | [40062534](https://issues.chromium.org/issues/40062534) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>FileSystem, UI>Browser>Downloads |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | am...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2023-01-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

As stated in my another issue Reference added in next line when we download a extension say .exe/.bat it will show pop up for cross confirmation. but by using showDirectoryPicker() Method we can save the .bat file without any popup's

<https://bugs.chromium.org/p/chromium/issues/detail?id=1405195>

**VERSION**  

Chrome Version: Version 108.0.5359.125 (Official Build) (64-bit)  

Operating System: Windows 10 Updated to latest Patch

**REPRODUCTION CASE**

Poc

1. Open the below html file. Click on save the jpg file
2. It will show the Directory Picker Dialog
3. Approve them
4. You can now see the Bat file is saved into the disk without any popup

If we can specify the exact folder to open via showDirectoryPicker Method Then This will have a higher impact which of similar to my above report

We can trick the user to hold enter for 2 Sec this will Accept all the dialogs and save the file.

I have tried open the direct sub folder but it is not possible so it needs User interaction to download a file

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Ameen Basha M K (Acknowledge my name with my profile/ mail id)

## Attachments

- [Chromium-Malicous Dialog Bypass.mp4](attachments/Chromium-Malicous Dialog Bypass.mp4) (video/mp4, 3.1 MB)
- [click2.html](attachments/click2.html) (text/plain, 6.6 KB)

## Timeline

### am...@gmail.com (2023-01-06)

Title mismatch: Downloading Malicious File Extensions WithOut DangerousFile popUp

### [Deleted User] (2023-01-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-06)

Giving write access to a directory also lets the webpage write executable stuff there. For downloading single files, we warn the user, but not in this case. Intentional? Something we should fix?

=> UX folks, do you have thoughts? Please assign to dtrainor/qinmin after.

[Monorail components: UI>Browser>Downloads]

### am...@gmail.com (2023-01-10)

Hi Team, Any update on this

### am...@gmail.com (2023-01-12)

Team, Can i get some quick response regarding this issue

### am...@gmail.com (2023-01-16)

Hi its around 10 days since your last response. Can i get the further update on this

### am...@gmail.com (2023-01-24)

Hi team, can i get some quick update on this?

### es...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>FileSystem]

### es...@chromium.org (2023-02-03)

asully, do you know if this is WAI? Is there supposed to be an additional prompt or warning to save executable files using File System Access?

The keyboard-jacking (holding down Enter to accept all the dialogs) also needs some clarification, in the video it looks like Cancel is the default action so holding down Enter wouldn't result in the user accepting the dialogs.

### as...@chromium.org (2023-02-04)

> The keyboard-jacking (holding down Enter to accept all the dialogs) also needs some clarification, in the video it looks like Cancel is the default action so holding down Enter wouldn't result in the user accepting the dialogs.

Correct - the permission dialogs default to "Cancel" so holding down Enter will abort the flow

If the site were to show a file picker and attempt to save a file (with showSaveFilePicker()), we would show a dialog asking the user if they're sure they want to save a file with a potentially dangerous extension (and we limit the extension length to 16 characters (https://crrev.com/c/3841864) so that you can't add a bunch of whitespace after the fake extension, as is done here). 

In this case, the directory picker is shown instead. Once the user grants write access to a directory, there's not as many restrictions in place (see https://crbug.com/1405665#c7 for context). We could consider adding more restrictions, such as to extension length, here, too, but I'm not sure how much that would actually help.

What could be useful, perhaps, would be to show a dialog when a site tries to edit/save a file with a dangerous extension. However, once the site gets write access to a directory, no user interaction is required to make these writes. So the prompt could feel like it's coming out of nowhere from the user's perspective... but probably better than having an unexpected executable in a local directory

That being said, every saved/edited file is subject to Safe Browsing checks (and has the Mark-of-the Web added), so if Safe Browsing thinks it's okay... ¯\_(ツ)_/¯

THAT being said, the showSaveFilePicker() dialog for dangerous files will become bypassable for bad actors by our upcoming (M111) launch of the move() method for local files. For example:

```js
// No "dangerous file extension" dialog shown
let handle = await window.showSaveFilePicker({ suggestedName: 'innocuous.txt' });
// Safe Browsing checks will be run on this rename, but, as this bug report shows, that likely won't prevent the file from being renamed
await handle.move('bad.exe');
```

So... I'm not sure where that leaves us. Happy to hear thoughts from security / SB folks about whether we should supplement SB checks with another dialog

### as...@chromium.org (2023-11-09)

marking available since I'm no longer working on File System

### aj...@google.com (2024-02-03)

assigning to someone because security issues need an owner - feel free to assign to someone else who is likely to make progress on this issue.

### is...@google.com (2024-02-03)

This issue was migrated from crbug.com/chromium/1405409?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>FileSystem, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### ch...@chromium.org (2024-02-05)

estark@ do you have any thoughts on asully@'s message in Comment 11? If we decide that a solution should be engineered for this case, I think that updating restrictions to limit directory pickers would be a preferable experience compared to showing a dialog - curious to hear your thoughts. Please feel free to re-assign to me once you've had a chance to take a look at this. Thanks!

### es...@chromium.org (2024-02-05)

Re: #15, could you clarify what "updating restrictions to limit directory pickers" would mean?

Otherwise, I think drubery or chlily might be able to comment on whether we should be concerned about being able to bypass the "potentially dangerous extension" dialog -- any thoughts?

### dr...@chromium.org (2024-02-05)

The "potentially dangerous extension" prompt is determined by [this](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc;drc=b5d8130747dda4cffdb0905db9cd65f04bc8549b;l=526) function, right?

If so, I do feel like being able to bypass it for DANGEROUS file types is pretty dangerous. We currently only have three file types in that category: dll, scf, and ini. They're classified as DANGEROUS because they can negatively impact the user without the user ever opening the file (e.g. DLL hijacking attacks). I would definitely support restrictions on this very small set of file types, even if the UX is a little surprising.

I'm not convinced it's much of a security bug to be able to bypass it for ALLOW\_ON\_USER\_GESTURE file types. That's a much broader category of file types, and in practice, users tend to bypass these warnings fairly often for regular downloads. I don't know that the value of a warning outweighs the cost of this prompt coming out of nowhere.

### ch...@chromium.org (2024-02-06)

Yes, that's the correct prompt. It sounds like the preferred solution here is to add more restrictions as to what can be shown in the picker itself.

Current restrictions on extensions of files selected from the file picker: https://crsrc.org/c/content/browser/file_system_access/file_system_chooser.cc;l=287-297;drc=4e1b7bc33d42b401d7d9ad1dcba72883add3e2af

I'm planning on add on exe and bat (and ini due to being DANGEROUS even if not directly called out in the original report) file extensions after I do some digging to figure out if there's a reason that these extension types aren't restricted from being shown in the picker currently.
If anyone on CC has objections / thinks that there's some context that I'm missing please let me know!

### ch...@chromium.org (2024-02-06)

After further investigation, it seems like there'a s few open security bugs that would be impacted by implementing a solution here (due to overlap), regardless of approach taken.
Going to put this on hold temporarily until further offline / security-related discussions are completed and will followup afterwards.

### am...@gmail.com (2024-03-05)

Team any update on this? its been a year since the issue reported

### ch...@chromium.org (2024-03-07)

Taking a step back, and revisiting OP's demo: it turns out that the `DownloadCheckResult` retrieved in `AfterWriteCheckResult` is `Result::UNKNOWN` and therefore the `AfterWriteCheckResult` is "allow". I'm not sure that the exact reason as to why it's 'UNKNOWN' matters too much here, except that it leads to an "allowed" outcome for the write operation in question.

dslee@ and I discussed this offline, and agree that completely blocking *writes* of .exe files would be unexpected behavior (e.g. the user is writing a .exe file on the web in a text editor or something like VSCode - they should be able to download that file without being blocked entirely). 

Re-raising this question for estark@ / drubery@: since it seems like blocking is not a viable solution here, should there be a warning prompt shown upon write operations of .exe / .bat files? It feels like the two options are either warning the user, or marking this as expected behavior if (as previously mentioned) this prompt would not add value and be readily dismissed by the user + increase prompt fatigue. Please let me know if there's something that I'm missing here, or if there's a third path forward that I'm not aware of!

### dr...@chromium.org (2024-03-18)

estark@ and I chatted and I'm talking this through with my team.

My general feeling is still well represented by [#comment17](https://issues.chromium.org/issues/40062534#comment17). I don't have any concern about .exe/.bat writes, since FSA gives strictly more protection than regular downloads there. For regular downloads, any user gesture could trigger a download which is then checked with Safe Browsing and no additional prompting is done (if its safe). For FSA, the user explicitly consented to *something* being written to disk. We also check with Safe Browsing for FSA.

The only remaining thing is that I'm a little torn on things like DLL/INI. The considerations are:

- DLL hijacking means the user could be harmed without every opening the file.
- INI (if I recall correctly) can leak an NTLM hash just by being shown in Explorer.
- On regular downloads, we show a soft warning about these downloads so they aren't on disk without explicit user consent
- For FSA, we do have the directory permission prompt, but that's far less explicit about it being a DLL/INI written to disk
- FSA does protect against directory write permission to a "sensitive" directory, which mitigates DLL a lot.

If anyone has thoughts on the balance of these, feel free to chime in. Otherwise my team's security UX folks can try to figure it out.

### am...@gmail.com (2024-04-18)

Team any update on this issue? Its been very long

### pe...@google.com (2024-04-18)

Thank you for providing more feedback. Adding the requester to the CC list.

### am...@gmail.com (2024-08-22)

Team its been a year since i reported this issue. Kindly update me the status.

### ap...@google.com (2024-09-20)

Project: chromium/src
Branch: main

commit 153ab68741786276ee86ff25e07d020c3aee43e6
Author: Nathan Memmott <memmott@chromium.org>
Date:   Fri Sep 20 21:31:34 2024

    FSA: Move IsSafePathComponent to FSA Manager
    
    Moves IsSafePathComponent to FSA Manager and makes it non-static.
    
    This is a refactor in preparation to make IsSafePathComponent check the
    Danger type. We will need access to the
    ChromeFileSystemAccessPermissionContext which will mean this function
    can no longer be static. And keeping it in
    FileSystemAccessDirectoryHandleImpl would mean always needing to call
    IsSafePathComponent on an instance of it. Which both doesn't make sense
    and isn't always possible. So this moves it to the FSA Manager.
    
    Bug: 40062534
    Change-Id: I41bf3902bb6e05ab04343c8f5435e56e612dc772
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5875188
    Commit-Queue: Nathan Memmott <memmott@chromium.org>
    Reviewed-by: Christine Hollingsworth <christinesm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1358389}

M       content/browser/file_system_access/file_system_access_directory_handle_impl.cc
M       content/browser/file_system_access/file_system_access_directory_handle_impl.h
M       content/browser/file_system_access/file_system_access_directory_handle_impl_unittest.cc
M       content/browser/file_system_access/file_system_access_handle_base.cc
M       content/browser/file_system_access/file_system_access_manager_impl.cc
M       content/browser/file_system_access/file_system_access_manager_impl.h
M       content/browser/file_system_access/file_system_access_manager_impl_unittest.cc

https://chromium-review.googlesource.com/5875188


### ap...@google.com (2024-10-03)

Project: chromium/src  

Branch: main  

Author: Nathan Memmott <[memmott@chromium.org](mailto:memmott@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5875189>

[FSA] Check for DANGEROUS extension types when creating a new file.

---


Expand for full commit details
```
[FSA] Check for DANGEROUS extension types when creating a new file.

FSA API already checks for safe_browsing::DownloadFileType::DangerLevel
on showSaveFilePicker(), but not on handle.getFileHandle().
This change aligns these two cases, with an exception of ".local" files,
per the existing comment on local files affecting its own directory,
and that the directory already has permission, hence okay to allow.

Bug: 40062534
Change-Id: I695dce1dfc68cf5f2518172d4e63aada074588fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5875189
Commit-Queue: Nathan Memmott <memmott@chromium.org>
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1363763}

```

---

Files:

- M `android_webview/browser/file_system_access/aw_file_system_access_permission_context.cc`
- M `android_webview/browser/file_system_access/aw_file_system_access_permission_context.h`
- M `chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc`
- M `chrome/browser/file_system_access/chrome_file_system_access_permission_context.h`
- M `content/browser/file_system_access/file_system_access_directory_handle_impl.cc`
- M `content/browser/file_system_access/file_system_access_directory_handle_impl_unittest.cc`
- M `content/browser/file_system_access/file_system_access_file_handle_impl_unittest.cc`
- M `content/browser/file_system_access/file_system_access_handle_base.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.h`
- M `content/browser/file_system_access/file_system_access_manager_impl_unittest.cc`
- M `content/browser/file_system_access/mock_file_system_access_permission_context.cc`
- M `content/browser/file_system_access/mock_file_system_access_permission_context.h`
- M `content/public/browser/file_system_access_permission_context.h`
- M `content/public/test/fake_file_system_access_permission_context.cc`
- M `content/public/test/fake_file_system_access_permission_context.h`

---

Hash: e401c21f259351d1eee212d6c04b306f018f1973  

Date:  Thu Oct 03 18:37:55 2024


---

### am...@gmail.com (2024-10-04)

Hi team, i hope the fix is implemented, can i get to know when the CVE will be registered and bounty details will be shared.

### pe...@google.com (2024-10-15)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### am...@gmail.com (2024-10-17)

Hi team, Since the ticket is moved to fixed status kindly let me know the CVE and bounty details

### am...@chromium.org (2024-10-22)

Hello, as always, reward decisions will be updated on the bug after a VRP decision panel has been made. This is in the queue for a reward decision. As rewards are decided in order of severity, it may be a bit more time before we get to this one.

CVEs are issued when a fix for a security bug ships in a Stable channel update of Chrome. This fix landed in 131, so this fix should ship in the M131 Stable channel release of Chrome.
<https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### am...@gmail.com (2024-11-03)

Team i hope bounty panel will meet every week so is there be any update on this?

### am...@chromium.org (2024-11-05)

We did not meet last week due to many of us being out of office. Additionally, bugs are assessed in order of severity so it may be some more weeks until we get to this issue.
As always bugs will be updated directly with the reward decision once that has occurred. Thank you for your patience.

### sp...@google.com (2024-11-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation || exploitation mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-22)

Congratulations Ameen! Thank you for your efforts and reporting this issue to us.

### am...@gmail.com (2024-11-23)

Hi team, thanks for the bounty.

Can i get to know what are all the places my name is acknowledged.(kindly share the links too)

also is this included in google hall of fame too?

inaddition to this, should i have to wait for a mail from p2p-vrp(how long will it take) or I have to sent mail?

### am...@chromium.org (2024-11-25)

Hello,

> Can i get to know what are all the places my name is acknowledged.(kindly share the links too)

You are acknowledged in the Chrome Stable release notes in the release version the fix for the issue you reported ships.
In this case, it's:
<https://chromereleases.googleblog.com/2024/11/stable-channel-update-for-desktop_12.html>

> also is this included in google hall of fame too?

The Google HoF no longer exists.
There is the Bughunters (<https://bughunters.google.com/leaderboard>) leaderboard and honorable mentions lists. To be included on these you need to have a bughunters profile.

> inaddition to this, should i have to wait for a mail from p2p-vrp(how long will it take) or I have to sent mail?

As explained above in c#34, p2p-vrp will process your payment or reach out to you, if needed.
It will not be immediately however, and may a day or two.

### am...@gmail.com (2024-11-26)

Thanks for the update

regarding the hall of fame, i have the bughunters profile but my name is not listed in any of the leaderboard. i tried with search also but my name is not listed, Kindly help on this

### am...@chromium.org (2024-11-26)

Your profile must be public. Please check the status of your profile.
If this issue persists, please reach out to [bughunters-feedback@google.com](mailto:bughunters-feedback@google.com)

### pe...@google.com (2025-01-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@gmail.com (2025-01-22)

Team still i havent received the bounty for this issue, i have completed all the details at embark to receive the payment but even after following up in vrp-support mail there is no response on this, Kindly help me to get the bounty reflect in my account

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062534)*
