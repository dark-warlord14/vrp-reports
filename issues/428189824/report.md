# Security: PiP window obscures FSA API file picker dialog (env var leak)

| Field | Value |
|-------|-------|
| **Issue ID** | [428189824](https://issues.chromium.org/issues/428189824) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture, Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | le...@google.com |
| **Created** | 2025-06-27 |
| **Bounty** | $5,000.00 |

## Description

## SUMMARY

A PiP window can obscure the file/directory picker dialog, using the File System Access (FSA) API. Without user awareness, an attacker can:

- Read environment variables (similar to [issue 40057200](https://issues.chromium.org/issues/40057200))
- Read/write files (similar to [issue 40076120](https://issues.chromium.org/issues/40076120))

Using the FSA API bypasses existing protections that only apply to file/dir picker dialogs opened from file-type inputs.

## VULNERABILITY DETAILS

A PiP window can obscure a file/directory picker dialog opened through the FSA API: `showSaveFilePicker()`, `showOpenFilePicker()`, or `showDirectoryPicker()`.

### Prior fixes only mitigate for file-type inputs, not FSA API

There are two fixes for [issue 40076120](https://issues.chromium.org/issues/40076120), but neither mitigate the same vulnerability in file/dir pickers opened through the FSA API. They only mitigate the vuln for file/dir pickers opened through file-type inputs.

The first fix in <https://crrev.com/c/5753110> (September 2024) blocked or closed PiP windows if a file picker was open (feature flag [`FileDialogsBlockPictureInPicture`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/media_switches.cc;l=665;drc=6b12aa08faf21efc74ac0d0a036eed90f8a3fc50)).

The first fix was disabled in <https://crrev.com/c/6318768> (March 3rd, 2025) and a new fix was introduced in <https://crrev.com/c/6449682> (June 10th, 2025). The new fix tucks the PiP window instead of blocking/closing it (feature flag [`FileDialogsTuckPictureInPicture`](https://source.chromium.org/chromium/chromium/src/+/main:media/base/media_switches.cc;l=670;drc=6b12aa08faf21efc74ac0d0a036eed90f8a3fc50)).

Neither fix mitigates the vulnerability when using FSA API file/dir pickers, verified by enabling/disabling the features (see attached videos). On current 138.0.7204.50 Stable, neither fix is enabled so both attack approaches work anyway.

## Impacts

### Scenario 1: Read environment variables

An attacker can exfiltrate environment variables (similar to [issue 40057200](https://issues.chromium.org/issues/40057200)) on Windows by saving a file with the environment variable names (e.g. `%username%-%service_secret_key%`). The env var names are replaced with their values when saving the file, and we can read the file name containing the values.

To perform the attack, we write the env var names into the clipboard and then ask user to paste the payload into the file picker dialog while it's obscured by the PiP window. After the user presses enter to save the file, we read the file name which now contains the env var values. We then delete the file to clean up the attack.

There's [code to sanitize](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_access_manager_impl.cc;l=719;drc=d9274c81e2ea8e0eaeb88663b3e087b9c76b135f) pre-filled file names in the file picker dialog, but we work around this by having the user paste our payload into the dialog.

Env var exfil is possible with the FSA API but not with file-type inputs because file-type inputs use open dialogs, not save dialogs. An attacker needs to use save dialogs to get a file handle with the env var values in its file name.

### Scenario 2: Read+write file/dir

An attacker can read and write to a mostly-arbitrary file/dir without user awareness.

Similar to the first scenario, we write the file/dir path into the clipboard and ask user to paste payload into the dialog while it's obscured. This allows us to use env vars or known paths that would otherwise not be pre-fillable through the FSA API.

After [issue 40076120](https://issues.chromium.org/issues/40076120) was filed, [more protections](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc;l=289;drc=e65323be17a0ba06198d18b0a8bf5ae594e10348) were added to block access to common sensitive directories, but users may still have files of interest in non-blocked directories. Outside of these blocked dirs, path is arbitrary.

## VERSION

Chrome version: 138.0.7204.50 Stable, 140.0.7262.0 Canary

For potentially mitigating feature flags (`FileDialogsBlockPictureInPicture`, `FileDialogsTuckPictureInPicture`) I verified repro with:

- default config (on Stable, both disabled; on Canary, only tuck enabled)
- both disabled
- only one enabled

Operating System: Windows 10

## REPRODUCTION CASE

### Minimal comparison: Mitigation on file-type input dialog vs. FSA API dialog

This page shows observed mitigation differences between file-type input dialog (mitigated) and FSA API dialog (not mitigated). If mitigated, close/tuck occurs even if file picker and PiP window don't overlap.

1. Run Chrome with `--enable-features=FileDialogsTuckPictureInPicture --disable-features=FileDialogsBlockPictureInPicture` (or the opposite enabled/disabled feature combination) to enable one of the mitigations.
2. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip-minimal.html> and choose the opening method.
3. Click anywhere to open PiP window.
4. Click again to open file picker.

Observed: When file picker dialog is opened using file-type input, PiP window is closed or tucked (based on enabled mitigation). When same dialog is opened using FSA API, PiP window is not closed or tucked.

Expected: When file picker dialog is opened by attacker in any way, PiP window is closed or tucked (based on enabled mitigation).

### Scenario 1: Read environment variables

1. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip.html>
2. Press any key twice (or press and hold any key).
3. Press Ctrl+V, then enter.

Observed: File picker dialog is obscured by PiP window. Attacker can read environment variables without user awareness.

Expected: FIle picker dialog is visible to user. Ideally, attacker cannot read sensitive environment variables even if not obscured.

### Scenario 2a: Read file

Setup: Create a file in `Documents` named `example.txt` with any content.

1. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip.html?mode=readfile>

Steps 2-3: Same as first scenario.

Observed: File picker dialog is obscured by PiP window. File is read from attacker-specified path without user awareness.

Expected: File picker dialog is visible to user.

### Scenario 2b: Write file

1. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip.html?mode=writefile>

Steps 2-3: Same as first scenario.

Observed: File picker dialog is obscured by PiP window. File is written to attacker-specified path without user awareness.

Expected: File picker dialog is visible to user.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- filepicker-pip.html (text/html, 6.2 KB)
- filepicker-pip-minimal.html (text/html, 1.4 KB)
- filepicker-pip.mp4 (video/mp4, 3.1 MB)
- filepicker-pip-minimal-FileDialogsTuckPictureInPicture.mp4 (video/mp4, 2.7 MB)
- filepicker-pip-minimal-FileDialogsBlockPictureInPicture.mp4 (video/mp4, 2.0 MB)
- filepicker-pip-rce.html (text/html, 4.2 KB)
- filepicker-pip-rce.mp4 (video/mp4, 11.0 MB)
- filepicker-pip-rce-cr.patch (text/x-diff, 2.2 KB)
- filepicker-pip-rce-cr.html (text/html, 2.7 KB)
- filepicker-pip-rce-cr.mp4 (video/mp4, 7.5 MB)
- filepicker-pip-rce-cr.patch (text/x-diff, 3.2 KB)
- filepicker-pip-rce-bg-cr.html (text/html, 3.1 KB)
- filepicker-pip-rce-bg-cr.mp4 (video/mp4, 3.1 MB)
- Screencast From 2025-08-05 15-48-28.mp4 (video/mp4, 1.8 MB)
- Untitled.png (image/png, 23.4 KB)

## Timeline

### al...@alesandroortiz.com (2025-06-27)

I'll soon report a few related issues that benefit from file picker being obscured. Filing those separately because they still have standalone impacts even if file picker is not obscured.

Also, I'm fairly sure a compromised renderer can remove most user interactions for this report's PoCs, reducing user interaction to "Ctrl+V, then enter". I'll post an update once I verify.

### al...@alesandroortiz.com (2025-06-27)

## Root Cause

For file-type inputs, file picker is created through `FileSelectHelper::RunFileChooser()` which creates `ScopedTuckPictureInPicture` / `ScopedDisallowPictureInPicture`: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/file_select_helper.cc;l=620;drc=d350ca68909171a740a8e33c43fea86ed0574a05>

The FSA API does not use `ScopedTuckPictureInPicture` or `ScopedDisallowPictureInPicture` anywhere before creating dialog in [`FileSystemChooser::CreateAndShow()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_chooser.cc;l=292;drc=d350ca68909171a740a8e33c43fea86ed0574a05).

For comparison, fullscreen is blocked for both file-type input and FSA using `WebContentsImpl::ForSecurityDropFullscreen()`. File-type inputs call it in [`WebContentsImpl::RunFileChooser()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=8887;drc=d350ca68909171a740a8e33c43fea86ed0574a05). FSA API calls it in [`ShowFilePickerOnUIThread()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_access_manager_impl.cc;l=196;drc=d350ca68909171a740a8e33c43fea86ed0574a05).

## Proposed Patch

Use `ScopedTuckPictureInPicture` in `ShowFilePickerOnUIThread()`, in similar spot where fullscreen block is implemented.

I'll upload CL next week.

### dc...@chromium.org (2025-06-30)

I don't know of a way to trigger this on mobile Android, so I'll tentatively mark this as affecting desktop OSes only. Severity-wise... I think it's a bit of a judgement call between medium and high. I'll go with high for now, but I could see a case for medium as well.

### pe...@google.com (2025-06-30)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ch...@google.com (2025-06-30)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-30)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@alesandroortiz.com (2025-07-02)

## BISECT

The read environment variables scenario repros down to <https://crrev.com/4b039a0ef518c0722804c42d00ba33bc8b1f9585> (August 2020) when the FSA API was enabled by default. Verified using modified PoC that uses Video PiP API.

It probably also would repro in earlier versions, but the flags changed a few times so it's a bit of a pain to bisect. But essentially whenever `showSaveFilePicker()` was properly implemented.

The read arbitrary file scenario *should* repro down to the introduction of Video PiP, since that depends on file-type input field, but I haven't verified this since that's a bit less interesting and Video PiP flags also changed a few times so it's also a pain to bisect.

### le...@google.com (2025-07-04)

> Use ScopedTuckPictureInPicture in ShowFilePickerOnUIThread(), in similar spot where fullscreen block is implemented.

One concern is that the FSA API is a web API, and the implementation lives in //content, where the PiP is a chrome specific concept, so probably we can't directly create the `ScopedTuckPictureInPicture` instance in the API handling code. 

+ steimel@ maybe we need to extend the implementation of http://crrev.com/c/6449682 to handle the FSA API case?

### al...@alesandroortiz.com (2025-07-06)

This *might* also be useful to achieve RCE when combined with techniques described in this post: <https://mrd0x.com/filefix-clickfix-alternative/>

I'll need to write proper PoC, but manually testing works. Using the blog post's main attack ("FileFix Attack"), pressing Ctrl+L, then Ctrl+V, then enter will result in RCE (with MOTW bypass). When chained with this crbug, the attack would occur without user awareness.

### al...@alesandroortiz.com (2025-07-06)

This bug can also be chained to obscure other attacks involving file picker dialogs, such as [issue 428189828](https://issues.chromium.org/issues/428189828) and [issue 428989427](https://issues.chromium.org/issues/428989427) that I recently reported.

### al...@alesandroortiz.com (2025-07-06)

### RCE/sandbox escape PoC

As mentioned in [#comment10](https://issues.chromium.org/issues/428189824#comment10), pasting commands into the location bar of a file picker will execute the command. Seems like anything that would work with Win+R also works in location bar. This allows attacker to get RCE outside of sandbox.

### Reproduction Steps

1. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip-rce.html>
2. Press any key twice (or press and hold any key)
3. Press Ctrl+L, Ctrl+V, then enter (or hold down Ctrl, then press L, V, enter)

Observed: File picker is obscured by PiP window. Attacker can execute arbitrary commands through file picker location bar.

### st...@google.com (2025-07-07)

Yeah FSA definitely can't directly create a ScopedTuckPictureInPicture, and since //content can't depend on //ui/views (and the tucking is very views-specific), we'll probably need to indirectly create the ScopedTuckPictureInPicture (maybe through ContentBrowserClient or similar)

### al...@alesandroortiz.com (2025-07-07)

steimel@: Since the fix is a bit more complicated, I prefer if you worked on the patch instead of me to get this fixed sooner. Thanks!

### al...@alesandroortiz.com (2025-07-07)

As promised, RCE/sandbox escape with minimized user interaction to "Ctrl+L, Ctrl+V, Enter" or "Hold Ctrl, press L, V, Enter" with compromised renderer.

This vuln could be abused by attackers who are already using ClickFix-style (Win+R, Ctrl+V, Enter) attacks. If they perform a FileFix attack, as seen [in the wild](https://x.com/executemalware/status/1940771821940584533), this vuln could be used to hide the FileFix attack.

### RCE/sandbox escape PoC with compromised renderer

The renderer patch generates user activation to bypass browser-side user activation checks and also disables some renderer-side user activation checks. This lets us bypass clipboard write, popup, Document PiP, and File System Access API user activation checks. (Document PiP user activation bypass reported in May 2024: [issue 338398040](https://issues.chromium.org/issues/338398040))

Setup: Apply renderer patch `filepicker-pip-rce-cr.patch` and build Chromium.

### Reproduction Steps

1. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip-rce-cr.html>
2. Press Ctrl+L, Ctrl+V, then enter (or hold down Ctrl, then press L, V, enter)

Observed: File picker is obscured by PiP window. Attacker can execute arbitrary commands through file picker location bar. With compromised renderer, user only needs to interact with OS file picker.

### al...@alesandroortiz.com (2025-07-07)

Updated renderer patch to improve reliability in some edge cases.

### al...@alesandroortiz.com (2025-07-08)

For reference, [issue 339026518](https://issues.chromium.org/issues/339026518) (another PiP bug) can also be used for a similar RCE/sandbox escape as I noted in <https://issues.chromium.org/issues/339026518#comment10>

### al...@alesandroortiz.com (2025-07-08)

And we can chain [issue 338398040](https://issues.chromium.org/issues/338398040) (yet another PiP bug) to initiate the attack from background tabs at any time with a compromised renderer.

Setup: Apply renderer patch `filepicker-pip-rce-cr.patch` and build Chromium. (Same patch from [#comment16](https://issues.chromium.org/issues/428189824#comment16).)

### Reproduction Steps

1. Navigate to <https://alesandroortiz.com/security/chromium/filepicker-pip-rce-bg-cr.html>
2. Wait until tab opens to `example.com` (or manually open another tab)
3. Press Ctrl+L, Ctrl+V, then enter (or hold down Ctrl, then press L, V, enter)

Observed: Same as [#comment15](https://issues.chromium.org/issues/428189824#comment15), plus attack can be initiated by compromised renderer on a background tab without user interaction.

### ch...@google.com (2025-07-19)

leimy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### an...@chromium.org (2025-07-29)

[security shepherd] Hi leimy@, steimel@:  just checking in to see if there is any update regarding a potential fix. Thanks!

### le...@google.com (2025-07-30)

Sorry I was a bit unclear on who should be owning this fix since the solution is provided from the PiP side but it should be triggered from the FSA API.

Let me take a look at the implementation and try to create a fix this week.

### le...@google.com (2025-07-31)

re: [comment#4](https://issues.chromium.org/issues/428189824#comment4)

> I don't know of a way to trigger this on mobile Android, so I'll tentatively mark this as affecting desktop OSes only.

According to go/picture-in-picture-tucking-design-doc, "Android’s picture-in-picture UI is quite different. No plans to support".

### le...@google.com (2025-08-05)

@st...@google.com
I had this CL implemented: <http://crrev.com/c/6804805>, but with two questions:

1. Previously I tested with the poc, and it's confirmed that the issue exists before the patch and gets fixed after the patch. However, after some time last week, the PiP window is not being opened properly even on main branch. Is it a known issue from PiP side? (see the attached screencast)
2. Is there any browser test/WPT verifying the behavior of the fix? From <http://crrev.com/c/6449682> I only found unit test.

Thanks.

### st...@google.com (2025-08-05)

> Previously I tested with the poc, and it's confirmed that the issue exists before the patch and gets fixed after the patch. However, after some time last week, the PiP window is not being opened properly even on main branch. Is it a known issue from PiP side? (see the attached screencast)

There's no known issue from the PiP side. Does the devtools console show any errors? Also, have you tried the hosted one?

<https://alesandroortiz.com/security/chromium/filepicker-pip-minimal.html>

> Is there any browser test/WPT verifying the behavior of the fix? From <http://crrev.com/c/6449682> I only found unit test.

Good question. I don't think there is

### le...@google.com (2025-08-06)

I tried the hosted one, the result is the same, also there is no log in the console.

I can see the window icon shows up in the tab bar but there is no actual window.



### st...@google.com (2025-08-06)

Turns out there is a known document pip issue stemming from some recent navigation throttle changes. I'm working on a fix now

### al...@alesandroortiz.com (2025-08-06)

Is there a public crbug for that, so I can get more details and track fix? I'm doing other research with PiP today+tomorrow so don't want to be blocked on this.

### st...@google.com (2025-08-06)

In the meantime, you can run with `--disable-features=Prewarm` to prevent that issue. Note that Prewarm is only enabled in local builds due to a fieldtrial testing config, so this issue doesn't exist in released builds

### al...@alesandroortiz.com (2025-08-06)

Ah, thanks for workaround and details.

### st...@google.com (2025-08-06)

Just landed crrev.com/c/6823355, which disables the prewarm fieldtrial testing config and have reached out to the feature owner so we can get it to work witohut breaking document pip. If you fetch to get a ToT that contains that CL, it should work without needing to explicitly disable Prewarm

### dx...@google.com (2025-08-14)

Project: chromium/src  

Branch:  main  

Author:  Mingyu Lei [leimy@chromium.org](mailto:leimy@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6817757>

FileSystemChooser: wrap fullscreen block in ScopedObjects struct

---


Expand for full commit details
```
     
    Bug: 428189824 
    Change-Id: I331bf28de6ec543464037d2a7a17eb0f76e877d7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6817757 
    Reviewed-by: Fergal Daly <fergal@chromium.org> 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1501187}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/file_system_access/file_system_chooser.cc`
- M `content/browser/file_system_access/file_system_chooser.h`
- M `content/browser/file_system_access/file_system_chooser_unittest.cc`

---

Hash: [e7a0dbba158284911c37afbc4916dfb4252f80ea](https://chromiumdash.appspot.com/commit/e7a0dbba158284911c37afbc4916dfb4252f80ea)  

Date: Thu Aug 14 03:54:15 2025


---

### dx...@google.com (2025-08-15)

Project: chromium/src  

Branch:  main  

Author:  Mingyu Lei [leimy@chromium.org](mailto:leimy@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6804805>

FSA: Tuck Picture-in-Picture window when file dialog

---


Expand for full commit details
```
     
    When a file chooser dialog is opened, it can be obscured by an open 
    Picture-in-Picture window. This change introduces a mechanism to 
    automatically tuck the Picture-in-Picture window when the file chooser 
    is active, and restore it when the chooser is closed. 
     
    This is implemented by: 
    - Adding a new method MaybeGetScopedPictureInPictureTucker to 
    ContentBrowserClient which returns a ScopedClosureRunner. 
    - ChromeContentBrowserClient implements this method to create and 
    return a ScopedTuckPictureInPicture instance tied to the lifetime of the 
    ScopedClosureRunner. 
    - The FileSystemAccessManager gets this scoper and passes it to the 
    FileSystemChooser, which owns it for the duration the file dialog is 
    shown. 
     
    This ensures that the Picture-in-Picture window is tucked away while the 
    user is interacting with the file dialog, and is restored to its 
    original position afterward. 
     
    This follows the same pattern used in http://crrev.com/c/6449682. 
     
    A browser test is also added. 
     
    Bug: 428189824 
    Change-Id: I65cc1b878cac16efb96e0da3be486309e350c634 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6804805 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Reviewed-by: Tommy Steimel <steimel@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Fergal Daly <fergal@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1501810}

```

---

Files:

- M `chrome/browser/chrome_content_browser_client.cc`
- M `chrome/browser/chrome_content_browser_client.h`
- M `chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/file_system_access/file_system_chooser.cc`
- M `content/browser/file_system_access/file_system_chooser.h`
- M `content/public/browser/content_browser_client.cc`
- M `content/public/browser/content_browser_client.h`

---

Hash: [d207a18ef2361564aed5daef30ddf3343ecea7a1](https://chromiumdash.appspot.com/commit/d207a18ef2361564aed5daef30ddf3343ecea7a1)  

Date: Fri Aug 15 07:05:23 2025


---

### ch...@google.com (2025-08-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-08-15)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139, 140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-08-15)

This is not remote exploitable and requires a series of interactions in order to exploit, the fix is also non-trivial, so I am declining backmerge to M139 Stable and M138 Extended; reviewing now for potential M140 Beta backmerge only

### am...@chromium.org (2025-08-15)

There is no canary data available yet, as <https://crrev.com/c/6804805> was only landed just over 12 hours ago; will need to review this on Monday for potential beta backmerge

### sp...@google.com (2025-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high quality report of lower-end of moderate user information disclosure; there was some sufficient and specific gestures here need here to make this possible


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-08-21)

I had a chance to take a much closer look at this issue during VRP panel before I came back to merge review this. Given that tuck must be enabled here and also the other pretty significant UI preconditions, we don't believe this to be a high severity issue as alluded to in c#35. So I've lowered the severity accordingly.

This still qualifies for backmerge to stable as a medium severity issue.
I've had a look at canary and dev data and am not seeing any issues, please go merge <https://crrev.com/c/6804805> to M140 beta / branch 7339 at your earliest convenience.

### al...@alesandroortiz.com (2025-08-26)

Thanks for the reward!

Were the RCE/sandbox escape impacts considered in the reward decision? Rationale only mentions user information disclosure.

See sandbox escape PoCs in [#comment12](https://issues.chromium.org/issues/428189824#comment12) (regular renderer) and [#comment15](https://issues.chromium.org/issues/428189824#comment15) (compromised renderer).

### am...@chromium.org (2025-08-27)

Hi Alesandro, the RCE and sandbox escape were part of the reward calculation, but was not included in the rationale. If this the reward amount were simply based on the potential for RCE and sandbox escape this would be considered a highly mitigated version of that given this issue is not remote exploitable and based on the significant preconditions of user gesture and timing to trigger the RCE/sbx.

It was the combination of that and the UID, with the UID being on the lower end of moderate impact and the highly mitigated potential for SBX but all within a high-quality report that resulted in the $5,000 reward. That all doesn't exactly fit in our rationale boxes for our automation though. :)

Hope this helps!

### al...@alesandroortiz.com (2025-08-28)

Cheers, thanks for the full context!

### ch...@google.com (2025-11-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality report of lower-end of moderate user information disclosure; there was some sufficient and specific gestures here need here to make this possible

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/428189824)*
