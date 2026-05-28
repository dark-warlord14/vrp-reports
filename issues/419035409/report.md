# Malicious Site can Steal Other Site's Downloads

| Field | Value |
|-------|-------|
| **Issue ID** | [419035409](https://issues.chromium.org/issues/419035409) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Mac, Windows |
| **Reporter** | va...@hotmail.com |
| **Assignee** | my...@chromium.org |
| **Created** | 2025-05-20 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Malicious Site can Steal Other Site's Downloads

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Google Chrome Version 136.0.7103.114

---

### The problem

#### Please describe the technical details of the vulnerability

A victim visiting an attacker's website can, given minimal user-input (Holding the `Enter` key), steal files that can be downloaded from other websites.

In the proof of concept, I showcase how an attacker is able to steal the source code of a private GitHub repositories just by tricking the victim into holding the `Enter` key.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Any website that has a link which when visited downloads a file with a predictable filename can be attacked. If the attacker can trick the victim into holding their `Enter` key on the attacker's website, then the attacker can steal the file, as shown in the attached proof of concept with a private GitHub repository's source code.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 136.0.7103.114

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

Robbe Van Roey - PinkDraconian

## Attachments

- [file-stealer.mp4](attachments/file-stealer.mp4) (video/mp4, 1.0 MB)
- [full_poc.py](attachments/full_poc.py) (text/x-python, 3.7 KB)
- [small_poc.html](attachments/small_poc.html) (text/html, 2.3 KB)
- [attacker.html](attachments/attacker.html) (text/html, 2.2 KB)

## Timeline

### ct...@chromium.org (2025-05-21)

I can repro on macOS. While safe to run (based on reading over the files), the PoC needed some editing to make it not rely on a private repo I don't have access to -- I've attached that here (the smaller HTML-only poc seems sufficient to me to demonstrate this).

This can also be repro'd by manually doing the following:

1. Navigate to a test page like <https://example.com>
2. Open DevTools and in the console paste in the following snippet, and then **hold down enter**:

```
const fileHandle = await window.showSaveFilePicker({'startIn':'downloads', 'suggestedName': 'permission.site-master.zip'});
fileHandle.remove(); window.open('https://github.com/chromium/permission.site/archive/refs/heads/master.zip');
setTimeout(async () => {
    console.log(await (await fileHandle.getFile()).text())
}, 3000);

```

(This uses an archive of a public chromium test site in place of the private download.)

3. See that the raw zip contents are output to the DevTools console.

The enter press continues to go through the file picker dialog and accepts the default button. In this case the file picker dialog *very* briefly flashes on the screen.

This is combining two pieces to cause a user information disclosure:

1. The filepicker from `window.showSaveFilePicker()` is default accepted when holding down the ENTER key (and the directory/filename is attacker controlled, within some restrictions), so the user never sees the warning disclosure about edits being visible
2. The attacker can trigger a download via `window.open()` for a file it would not have access to, but it can predict the filename (and download location)

Combining the two, the user grants read/write access to that file, but then the download "writes" to it and the attacker site can read the updated contents still.

(2) is user visible (the download appears in the download menu, etc.) but (1) is pretty well hidden from the user.

One obvious mitigation would be to break the ENTER key input on the file picker menu, but I believe this is OS-controlled so it may be difficult or impossible.

Setting some initial security labels:

- Medium severity (S2) -- this is a cross-origin data disclosure, but with some preconditions (only downloads) and user interaction requirements.
- Found-In M136 as this repros on Stable
- OS=macOS,Windows as this seems does not seem to repro for me on Linux (although that may depend on the exact desktop environment being used)

Passing to content/browser/file\_system\_access/OWNERS and randomly assigning to fergal@ out of that set (feel free to re-assign).

### ct...@chromium.org (2025-05-21)

Forgot to actually attach the modified HTML poc

### le...@google.com (2025-05-22)

> One obvious mitigation would be to break the ENTER key input on the file picker menu, but I believe this is OS-controlled so it may be difficult or impossible.

Even if it's mitigated in this way, I think the attacker side can simply change the instruction to something like "How many times can you smash that Enter key in 10 seconds?" to achieve the same goal.

To me the key problem here is a page with a file handle can keep using it to access the file content even if the file is modified elsewhere. This file then becomes a "shared storage" across different origins. This "enter key hack" here is just a way to trick the user and gain the permission, there could be other possible variations (like the one mentioned above, or asking the user to paste something into the devtools console etc.)

### ch...@google.com (2025-05-22)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-22)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### my...@chromium.org (2025-05-23)

@as...@chromium.org  Could you provide some insights here about the cross-domain permission checking on FileHandle operation?

### as...@chromium.org (2025-05-23)

> One obvious mitigation would be to break the ENTER key input on the file picker menu, but I believe this is OS-controlled so it may be difficult or impossible.

Yeah unfortunately I'm not aware of a way to do this. For example we use [NSSavePanel](https://developer.apple.com/documentation/appkit/nssavepanel) on Mac and I don't see any options in their docs to e.g. set the default button to "Cancel" rather than "Save"

> This file then becomes a "shared storage" across different origins

Well, sort of. The site from which the data is downloaded does not have visibility into this file once the download occurs. This is basically a fetch of data from another origin through the user's file system

It seems like the real issue here is that this "cross-origin fetch" is different from a typical `fetch` because using `window.open` means cookies etc are all available which might give access to resources gated behind login? I assume this is why OP mentions private GitHub repos

> @[asully@chromium.org](mailto:asully@chromium.org) Could you provide some insights here about the cross-domain permission checking on FileHandle operation?

Can you clarify what you mean here?

We have no checks that a given `FileHandle` is only held by one origin, if that's what you're asking. The thinking has always been that the user must go out of their way to grant two websites access to the same file, and if they do then they probably are intentionally doing so and we shouldn't prevent the user from carrying out that use case

That's not relevant in this issue, though, since the site triggering the download (in this case `github.com`) does not use the FSA API

### fe...@chromium.org (2025-06-02)

This seems like 2 different issues to me.

1. Holding enter can cause things to happen invisibly and the default focus on file access dialogs are dangerous
2. From cthomp@ #2, saving a file grants access to that *filename* indefinitely. I have opened <https://crbug.com/421690393> separately for that.

It might make sense to postpone opening (or moving focus to) any file picker (or other window) while a key is held down. It doesn't fix the "keep hitting enter" version of this but at least that version will presumably flash the dialog on screen briefly, whereas the continuous enter version seems to show nothing at all. This doesn't sound like a trivial change.

Alternatively, maybe there's something related to the fact that showing a file upload dialog requires transient user activation? Should key-down without key-up be considered a transient user activation? In many cases that requirement is protecting actions that lead to a permission prompt or a window of some kind, showing that prompt/window with enter held down is going to be a bad UX. This would have broad reach but perhaps key-down should not count as a TUA. Maybe it could just be enter-down (would we need space-down also? are these keys customizable?)

### fe...@chromium.org (2025-06-02)

Also, I think addressing <https://crbug.com/421690393> would make the enter-down problem go away, since forcing the site to reopen the file after its removal would require a call to `showOpenFilePicker` which does not have a `suggestedName` option and (for me anyway) does not seem to have a default selection. That said, opening new windows and permission prompts while a key is held down *is* probably a bad idea.

So if I'm correct there's really only one security bug, it doesn't requires holding down enter and it applies to all OSes, I think.

### ct...@chromium.org (2025-06-02)

> Alternatively, maybe there's something related to the fact that showing a file upload dialog requires transient user activation? Should key-down without key-up be considered a transient user activation? In many cases that requirement is protecting actions that lead to a permission prompt or a window of some kind, showing that prompt/window with enter held down is going to be a bad UX. This would have broad reach but perhaps key-down should not count as a TUA. Maybe it could just be enter-down (would we need space-down also? are these keys customizable?)

This would be neat (and I think would be a better systematic fix for this class of "hold down enter and then it triggers the default focus in a dialog" problem that affects more than just the FS API. However, I imagine that actually making the change of requiring key-down+key-up for transient user activation would be a bigger web platform ecosystem lift -- cc'ing mustaq@ as they might have opinions or know if we have previously considered this.

Agreed that for this particular case if we handle the sub-issue and require a new read-access prompt that sounds sufficient here.

### ch...@google.com (2025-06-16)

fergal: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-01)

fergal: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-16)

fergal: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-31)

fergal: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fe...@chromium.org (2025-08-01)

FYI we are working on changing the permission model so that in this repro, after deleting the file, the page would no longer have read access but could still write a new file under that name if it wanted.

The one thing we need to be careful of there is to make sure that the following race cannot occur:

- start download
- delete file
- recreate file
- download finishes and gets moved into recreated filename

### ch...@google.com (2025-08-16)

mych: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-31)

mych: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-15)

mych: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-30)

mych: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-10-09)

Project: chromium/src  

Branch:  main  

Author:  Ming-Ying Chung [mych@chromium.org](mailto:mych@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7010652>

[FSA] Enable the fix to FileSystemAccess API that disallows accessing a path via outdated permission

---


Expand for full commit details
```
     
    The following 3 flags are all part of a single fix to the attached 
    security bugs (same cause): when a path pointed by FileSystemAccess 
    handle is removed via `handle.remove()`, its "read" permission is still 
    retained internally, which leads to potential cross-origin access issue. 
     
    - `FileSystemAccessMoveWithOverwrite` 
    - `FileSystemAccessRevokeReadOnRemove` 
    - `FileSystemAccessWriteMode` 
     
    Bug: 421690393, 419035409 
    Change-Id: I0feeb9744f51aa2073014f53b76afa60618dafe9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7010652 
    Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    Reviewed-by: Mingyu Lei <leimy@chromium.org> 
    Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1527308}

```

---

Files:

- M `chrome/browser/file_system_access/file_system_access_features.cc`
- M `content/browser/file_system_access/file_system_access_directory_handle_impl_unittest.cc`
- M `content/browser/file_system_access/file_system_access_file_writer_impl_unittest.cc`
- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`

---

Hash: [48e20e5954c6a6f58eb6a4f8c446fadce0887b5a](https://chromiumdash.appspot.com/commit/48e20e5954c6a6f58eb6a4f8c446fadce0887b5a)  

Date: Thu Oct 9 03:40:52 2025


---

### ch...@google.com (2025-10-15)

mych: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-30)

mych: Uh oh! This issue still open and hasn't been updated in the last 89 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### my...@chromium.org (2025-10-31)

The fix will be rolled out along with M143.

### ch...@google.com (2025-11-14)

mych: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-09)

mych: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
mitigated user information disclosure with multiple gesture requirements


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/419035409)*
