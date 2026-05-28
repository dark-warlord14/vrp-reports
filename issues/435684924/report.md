# Security: Compromised renderer can read files through file picker dialog with kSave mode + prefilled filename

| Field | Value |
|-------|-------|
| **Issue ID** | [435684924](https://issues.chromium.org/issues/435684924) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileAPI |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | my...@chromium.org |
| **Created** | 2025-08-02 |
| **Bounty** | $2,000.00 |

## Description

## SUMMARY

A compromised renderer can use a file picker dialog with `kSave` mode and prefilled filename to read local files. In ideal scenarios, this occurs with minimal user interaction (holding enter) and can be used to read one or multiple files.

This is similar to [issue 433800617](https://issues.chromium.org/issues/433800617) that I reported and [fixed](https://crrev.com/c/6786387) recently. See that issue for more context on some of the details I mention below.

## VULNERABILITY DETAILS

When a user clicks a file-type input, the renderer calls [`FileChooser::OpenFileChooser()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=137;drc=ebee769e5e2e914e34b4ce20f956863d62bb7c3b) with a `FileChooserParams::Mode` to open file picker dialogs. In most cases, open file pickers are restricted by the browser from having a prefilled filename to prevent reading files without additional confirmation.

A compromised renderer can read files while bypassing the prefilled filename restrictions. When using [`Mode::kSave`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=35;drc=ebee769e5e2e914e34b4ce20f956863d62bb7c3b) instead of `Mode::kOpen`, the renderer can set [`default_file_name`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=45;drc=ebee769e5e2e914e34b4ce20f956863d62bb7c3b) which prefills the filename.

When the user clicks the "Save" button, the page gets read access to the file path. No file is created or written at the path, but we can read any current or future file at that path. When targeting a non-existent file, the attacker needs to know/predict the target filename, but this is easily predictable in many cases such as downloads.

There's two ways an attacker can use this dialog:

- Selecting non-existent file: Even when a file does not yet exist, the renderer gets a file handle when the user clicks "Save". After selection, when something else creates a file in the same selected location, the renderer can read the file without further user interaction. For example, a file can be created through browser downloads or external processes.
- Selecting existing file: For existing files, Windows will show an overwrite confirmation prompt. If the user accepts, the file is not actually overwritten and the renderer can read the file. This has same impacts as [issue 433800617](https://issues.chromium.org/issues/433800617), with the only user flow differences being the overwrite confirmation prompt and the "Save" button instead of "Open" button.

### Last selected directory behavior

As mentioned in [issue 433800617](https://issues.chromium.org/issues/433800617), the file picker dialog for file-type inputs will show the [`last_selected_directory`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;l=886;drc=d32f634388f26f8c7bbb98c82fa9718d30636b1e) which may not be the target folder. If the user needs to select the target folder, this increases user interaction and prevents the happy path from occuring for the first targeted file. However, for any subsequent targeted files in the same folder, the happy path can be used.

This is less of a mitigation here compared to [issue 433800617](https://issues.chromium.org/issues/433800617) because this attack asks users to save a file which doesn't exist, instead of opening an existing file. Even when the user has to manually change folders, the user isn't aware they are providing read access to any future file at that path.

For example, if an attacker wants to read future files from the downloads folder:

- In the happy path (if it's the downloads folder): The attacker can easily read one or more future downloads with minimal interaction (holding enter).
- In the sad path (if it's another folder): The attacker can ask the user to "Save" the file in the Downloads folder, which alllows attacker to read one future download. Any subsequent attempts can use the happy path (hold enter) to read multiple files.

### Chained impact: Cross-site downloads

When chained with [issue 428189828](https://issues.chromium.org/issues/428189828) to perform cross-site downloads, we can read the cross-site downloads with minimal user interaction (holding enter).

AFAICT, `Mode::kSave` was used by the PPAPI in the past and isn't currently used by the renderer through `OpenFileChooser()`.

### Chained impact: Arbitrary local file reads

There's a vulnerability that can be chained to achieve arbitrary local file reads, but I haven't submitted that report yet. I'll provide the chained PoC in comments once report is submitted.

### Potential impact: File write to potentially bypass Safe Browsing + MOTW

Notably, using `Mode::kSave` in [`FileChooserImpl::FileSelected()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/file_chooser_impl.cc;l=227;drc=d32f634388f26f8c7bbb98c82fa9718d30636b1e) calls `CPSPI::GrantCreateReadWriteFile()` which means the renderer could in theory ask the browser to write to the selected file path in the future. However, I have not found a way to do so since AFAICT the renderer needs to make writes through the browser process, and the the only way a renderer can ask the browser process to write files is through the FSA API. But if there's a way to write to this file, and if those paths don't use Safe Browsing or set MOTW, this would be a bypass of one or both security features.

If you, reader, know how to write to a file if we have a path from `OpenFileChooser()`, please comment below. :)

## PROPOSED FIX

AFAICT, `Mode::kSave` was used by the PPAPI in the past and isn't currently used by the renderer through `FileChooser::OpenFileChooser()`. Therefore, blocking `Mode::kSave` in [`FileChooser::OpenFileChooser()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=137;drc=ebee769e5e2e914e34b4ce20f956863d62bb7c3b) should fix the issue without affecting any other uses of save dialogs that don't go through the renderer. But I'll need to verify this once I implement the fix.

## VERSION

Chrome version:

- Cross-site credentialed download: 138.0.7204.169 Stable, 140.0.7326.0 Canary
- Show kSave file picker with prefilled filename: Verified with custom build based on `aad34245b04df3c637ce7c51b5a10af879e1ac98` (July 3rd)

Operating System: Windows 10

## REPRODUCTION CASE

Patch to simulate compromised renderer
To simulate a compromised renderer, the patch:

- Updates `third_party/blink/renderer/core/html/html_marquee_element.cc` to call `NotifyUserActivation()` when `marqueeElem.stop()` is called in JS, to bypass user activation checks.
- Updates `third_party/blink/renderer/core/html/forms/file_input_type.cc` to call `DownloadURL()` directly and set `default_file_name` in open file picker. See patch for how to use attributes to change behavior.

### Setup for PoCs:

- If self-hosting or want to edit using DevTools, optionally configure the target URL in the source code (e.g. `https://myaccount.google.com/personal-info`).
- If using default target (such as on hosted PoC), navigate to <https://aogarantiza.com/set-cookies.php> to set cookies on target.
- Apply attached patch and build Chromium.

### Scenario 1a: Non-existent file (hold enter) + chained with cross-site download

Using patched browser:

1. Navigate to <https://alesandroortiz.com/security/chromium/download-theft-input-ksave-cr.html?mode=holdenter>
2. Press and hold enter.

- For happy path (shows downloads folder): Wait for attack to complete within a couple of seconds.
- For sad path (non-downloads folder case): When prompted again, select downloads folder, then click "Save" button.

Observed: Page can show save dialog with prefilled filename. When user clicks/presses "Save" for non-existent file, page gets file handle for specified path. When page performs cross-site download to the same path, page can read download.

Expected: Page cannot show save dialog with prefilled filename. When user clicks/presses "Save", page does not get file handle for specified path. When page performs cross-site download to the same path, page cannot read download.

### Scenario 1b: Non-existent file (normal dialog interaction) + chained with cross-site download

Using patched browser:

1. Navigate to <https://alesandroortiz.com/security/chromium/download-theft-input-ksave-cr.html>
2. Click anywhere. (Note: a compromised renderer can show the dialog without user interaction.)

- For happy path (shows downloads folder): Click "Save" button.
- For sad path (non-downloads folder case): Select downloads folder, then click "Save" button.

3. Wait for attack to complete within a couple of seconds.

Observed/Expected: Same as Scenario 1a.

### Scenario 2: Existing file (normal dialog interaction)

Note: Ignore PoC's built-in instructions.

Using patched browser:

1. Navigate to <https://alesandroortiz.com/security/chromium/download-theft-input-ksave-cr.html>
2. Click anywhere. (Note: a compromised renderer can show the dialog without user interaction.)
3. Click any existing file in the folder.
4. Click "Yes" in overwrite confirmation prompt.

Observed: When user clicks "Save", page can read existing file without further warnings.

Expected: When user clicks "Save", page cannot read existing file without further warnings.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [filepicker-ksave-cr.patch](attachments/filepicker-ksave-cr.patch) (text/x-diff, 3.4 KB)
- [download-theft-input-ksave-cr.html](attachments/download-theft-input-ksave-cr.html) (text/html, 6.1 KB)
- [download-theft-input-ksave-cr.mp4](attachments/download-theft-input-ksave-cr.mp4) (video/mp4, 3.7 MB)
- [set-cookies.php](attachments/set-cookies.php) (application/x-httpd-php, 1.3 KB)
- [get-cookies.php](attachments/get-cookies.php) (application/x-httpd-php, 527 B)

## Timeline

### ja...@chromium.org (2025-08-04)

[security shepherd]

Thanks for the well written report!

I haven't reproduced the bug but the screencast is pretty clear.

Provisionally marking this as Medium severity (S2) for being something similar to "An uninitialized memory read in the browser process where the values are passed to a compromised renderer via IPC"

[FAQ entry here](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#TOC-Medium-severity).

I'll find an appropriate component to start with and find an owner.

### ja...@chromium.org (2025-08-04)

Assigning to fergal@ similar to [issue 429630718](https://issues.chromium.org/issues/429630718)

fergal@, can you please take a look?

### ja...@chromium.org (2025-08-04)

adding a few others based on bugs in the same area: [issue 40071290](https://issues.chromium.org/issues/40071290)

### ch...@google.com (2025-08-05)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-08-19)

fergal: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-03)

fergal: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-18)

fergal: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fe...@chromium.org (2025-09-29)

mych@ I think this is solved by your recent change to add write-only mode. Could you confirm?

### ch...@google.com (2025-10-13)

mych: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### al...@alesandroortiz.com (2025-10-16)

Re: [#comment10](https://issues.chromium.org/issues/435684924#comment10), I'm still able to repro at commit 44b2e34e898c67b896a61ca1e68e4601eeb02e0a (HEAD from a few hours ago).

### ch...@google.com (2025-10-28)

mych: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-12)

mych: Uh oh! This issue still open and hasn't been updated in the last 43 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-27)

mych: Uh oh! This issue still open and hasn't been updated in the last 58 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-12)

mych: Uh oh! This issue still open and hasn't been updated in the last 73 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-27)

mych: Uh oh! This issue still open and hasn't been updated in the last 88 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-01-06)

Project: chromium/src  

Branch:  main  

Author:  Tom Anderson [thomasanderson@chromium.org](mailto:thomasanderson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7399531>

[GTK] Don't preselect file dialog accept buttons

---


Expand for full commit details
```
     
    R=thestig 
     
    Change-Id: I61cc29e0560af5dd433ea07c234b9813e3d72c74 
    Fixed: 470928605 
    Bug: 435684924 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7399531 
    Commit-Queue: Thomas Anderson <thomasanderson@chromium.org> 
    Reviewed-by: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1564733}

```

---

Files:

- M `ui/gtk/select_file_dialog_linux_gtk.cc`

---

Hash: [e93121e97478a41d529c8586a48b4ec34173f79a](https://chromiumdash.appspot.com/commit/e93121e97478a41d529c8586a48b4ec34173f79a)  

Date: Tue Jan 6 01:42:17 2026


---

### my...@chromium.org (2026-01-06)

The non-existent scenario, i.e. obtaining a new file handle to allow editing it later, is fixed with <http://crbug.com/419035409>, or <https://chromium-review.googlesource.com/c/chromium/src/+/7010652>.

However, the scenario 2 may still be an issue is kSave somehow reaches browser via this FileChooser path. Sending out <https://crrev.com/c/7400881>.

### dx...@google.com (2026-01-07)

Project: chromium/src  

Branch:  main  

Author:  Ming-Ying Chung [mych@chromium.org](mailto:mych@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7400881>

[FileChooser] Block `FileChooserParams::Mode::kSave` in content

---


Expand for full commit details

```[FileChooser] Block `FileChooserParams::Mode::kSave` in content

```
`FileChooserImpl::OpenFileChooser()` previously allowed `Mode::kSave`, 
which permitted the renderer to specify a default_file_name. If the 
user accepted the dialog, the renderer would be granted read/write 
access to the chosen file. A compromised renderer could exploit this 
by prefilling a sensitive filename and tricking the user into granting 
access. 
 
`Mode::kSave` was primarily used by the legacy PPAPI and is not used 
anymore in [Blink][1]. Instead, the File System Access API handles 
save pickers in the browser process, bypassing this 
`blink::mojom::FileChooser` interface. 
 
This CL explicitly blocks `Mode::kSave` and reports a bad message in 
`FileChooserImpl::OpenFileChooser()` if a renderer attempts to use it. 
It also removes the corresponding permission grant logic in 
`FileChooserImpl::FileSelected()` and adds a safety check. 
 
Related CL: https://crrev.com/c/6786387 
 
[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/file_input_type.cc;l=210-215;drc=56535b80c32d3a618b8fc8cfd7b1afdd3862e1b2 
 
Bug: 435684924 
Change-Id: Ic696d0e7f01d1ddda1e5630c6bcb9ba889ce33ed 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7400881 
Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1565463}

```
```

---

Files:
* M       `content/browser/security_exploit_browsertest.cc`
* M       `content/browser/web_contents/file_chooser_impl.cc`
* M       `content/browser/web_contents/file_chooser_impl_browsertest.cc`
* M       `content/browser/web_contents/file_chooser_impl_unittest.cc`

---

Hash: [b709f9933538dc78cfd681bab3e09a1bc5357b20](https://chromiumdash.appspot.com/commit/b709f9933538dc78cfd681bab3e09a1bc5357b20)\
Date: Wed Jan 7 08:14:27 2026

</details>

---

```

### ch...@google.com (2026-01-21)

mych: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-05)

mych: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Low impact user information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/435684924)*
