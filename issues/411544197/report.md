# A vulnerability in FileSystemFileHandle.move bypasses download restrictions.

| Field | Value |
|-------|-------|
| **Issue ID** | [411544197](https://issues.chromium.org/issues/411544197) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 137.0.7115.0 |
| **Reporter** | ia...@gmail.com |
| **Assignee** | my...@chromium.org |
| **Created** | 2025-04-18 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

On any HTTPS page, try the following JS code. It should correctly display a file save dialog prompt, asking you to save a file named hello.png. When you click "OK," an evil.bat file will actually be generated in the actual directory.

```
try {
    // 1. Call showSaveFilePicker()
    const fileHandle = await window.showSaveFilePicker({
        suggestedName: `hello`,
        startIn: "desktop",
        // Filename prompt visible to the user
        types: [{
            description: [`ImageFile`],
            accept: {
                'image/png': ['.png']
            },
        }, ],
    });
    // 2. Get the FileSystemWritableFileStream
    const writableStream = await fileHandle.createWritable();
    // 3.1 Write malicious file data to download, saved as exe
    // const evilFile = await fetch(`evil.exe`)
    // await evilFile.body.pipeTo(writableStream)
    // fileHandle.move("evil.exe")
    // 3.2 Or write custom content and close the stream, e.g., .bat
    await writableStream.write(new TextEncoder().encode(`calc`));
    await writableStream.close();
    fileHandle.move("evil.bat")
} catch (error) {
    console.log(error)
}

```
# Problem Description

In Chrome versions 112.0.5580.0 to 137.0.7115.0 (the latest Cannry release), after a user confirms a save via window.showSaveFilePicker, invoking the move method on the resulting FileSystemFileHandle object can download certain sensitive files under attacker control into “well known directories” (["desktop", "documents", "downloads", "music", "pictures", "videos"]). If the "desktop" is selected and the user does not change the save location, downloading a file like "Google Chrome.exe" or a similarly deceptive file designed to mimic a desktop shortcut could have a real impact on the user.

After a period of investigation, I have seemingly pinpointed the original commit that introduced the issue. By testing various versions of Chromium on the dev channel, I obtained the following results (The following versions were tested on Winx64.):

- 112.0.5572.0 – Not working, position: 1099442
- 112.0.5580.0 – Working, position: 1101520
- 112.0.5592.0 – Working, position: 1104296
- 112.0.5608.0 – Working, position: 1107400

This localizes the problematic change to somewhere between positions 1101520 and 1099442. By searching the history of changes regarding file\_system\_access for versions 112.0.5572.0 to 112.0.5580.0, I examined the URL:  

<https://source.chromium.org/chromium/chromium/src/+/refs/tags/112.0.5580.0:third_party/blink/renderer/modules/file_system_access/;bpv=1;bpt=0>

I found several suspicious related commit histories:

```
6ad1f40 asully@chromium.org 2023-02-04 05:07 FSA: Re-use the same task runner for each SAH.write()
c735f76 asully@chromium.org 2023-01-25 11:24 FSA: Point SyncAccessHandle idl comment to spec
02799cd asully@chromium.org 2023-01-19 00:30 FSA: Implement a cursor for SyncAccessHandles
7cd323e dslee@chromium.org 2023-01-18 02:58 [FSA] Clean up the deprecated code for async SyncAccessHandle interface.
56c5a8d dslee@chromium.org 2023-01-18 01:18 [FSA] Remove enterprise policy for deprecating async SyncAccessHandle interface.

```

Among these, the most likely commit is:

```
6ad1f40 asully@chromium.org 2023-02-04 05:07

FSA: Re-use the same task runner for each SAH.write()

Currently, we create a new task runner for every write operation. This
is wasteful and hurts performance.

Also removes a task runner member that was used for async operations,
back when that was a thing.

Bug: https://bugs.chromium.org/p/chromium/issues/detail?id=1406246
Change-Id: I94ff69f023f0db60724659b0236710a09e8f132b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4219170
Reviewed-by: Daseul Lee <dslee@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1101185}

```

This commit seems to be the most likely cause of the issue.

# Additional Comments

The following versions were tested on Winx64.

- 112.0.5572.0 – Not working, position: 1099442
- 112.0.5580.0 – Working, position: 1101520
- 112.0.5592.0 – Working, position: 1104296
- 112.0.5608.0 – Working, position: 1107400
- 135.0.7049.86 works
- 134.0.6998.89 works

# Summary

A vulnerability in FileSystemFileHandle.move bypasses download restrictions.

# Custom Questions

#### Type of crash:



#### Crash state:



#### Reporter credit:



# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: Yes

## Attachments

- [Mon Apr 21 2025 09:58:57 GMT+0800 (中国标准时间).png](attachments/Mon Apr 21 2025 09_58_57 GMT+0800 (中国标准时间).png) (image/png, 13.3 KB)
- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 10.0 KB)

## Timeline

### ia...@gmail.com (2025-04-18)

Here is the translation:

It seems that I forgot to fill in some information:
Reporter credit: Huuuuu

Some additional notes:

1. I am sure that the file extensions that can be moved are .exe/.bat/.desktop ....
2. During the investigation, I found some relevant code. However, I am not sure if my analysis is correct; it is just some guesses.
   But I hope this is related to the issue and can help you quickly locate the problem.
   <https://chromium-review.googlesource.com/c/chromium/src/+/3257898>

> third\_party/blink/renderer/modules/file\_system\_access/file\_system\_file\_handle.cc

```
void FileSystemFileHandle::MoveImpl(
    mojo::PendingRemote<mojom::blink::FileSystemAccessTransferToken> dest,
    const String& new_entry_name,
    base::OnceCallback<void(mojom::blink::FileSystemAccessErrorPtr)> callback) {
  if (!mojo_ptr_.is_bound()) {
    std::move(callback).Run(mojom::blink::FileSystemAccessError::New(
        mojom::blink::FileSystemAccessStatus::kInvalidState,
        base::File::Error::FILE_ERROR_FAILED, "Context Destroyed"));
    return;
  }

  if (dest.is_valid()) {
    mojo_ptr_->Move(std::move(dest), new_entry_name, std::move(callback));
  } else {
    mojo_ptr_->Rename(new_entry_name, std::move(callback));
  }
}

```

In this method, it seems that Rename does not have any requirements for FileSystemAccessTransferToken.

### an...@chromium.org (2025-04-18)

[security shepherd]: Thank you for the report! Per the [Chrome Security FAQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#i-can-download-a-file-with-an-unsafe-extension-and-it-is-not-classified-as-dangerous-is-this-a-security-bug), Chrome does warn users before it's downloaded as we have download protection security settings in Chrome. However, assigning this to [asully@chromium.org](mailto:asully@chromium.org) to confirm if this potentially exposes a security vulnerability.

### as...@chromium.org (2025-04-18)

A couple things:

1. `.bat` files are allowed according to the checks [here](https://crsrc.org/c/content/browser/file_system_access/file_system_access_manager_impl.cc?q=FileSystemAccessManagerImpl::IsSafePathComponent) which are called [during the Rename flow](https://crsrc.org/c/content/browser/file_system_access/file_system_access_handle_base.cc;l=231-236;drc=f908220bb370108a7d2380217483d767d3de93ac;bpv=0;bpt=1). See prior discussion about `.bat` files at <https://crbug.com/40062534#comment22>. Importantly, changing this to `evil.lnk` correctly fails (in my local testing)
2. Renaming a file in this fashion (to a new path which does not have permission) should require user activation. In this case, I suspect the `move()` happens soon enough after the call to `showSaveFilePicker()` that the user activation created by that method (see step 7.10 of <https://wicg.github.io/file-system-access/#api-showsavefilepicker>) is used

While the latter is certainly misleading, I'm inclined to say it's not a security issue per say, since user activations are unreliable indicators of user intent and should not be used as a meaningful security barrier anyways; in this case, the meaningful security barrier is the check in #1 which is WAI

### as...@chromium.org (2025-04-18)

Marking as WAI for now, though please feel free to re-open if there's something I'm missing

### ia...@gmail.com (2025-04-21)

Here is the translation:

However, there is a problem. If you use the following JS:

```
window.showSaveFilePicker({suggestedName: `hello.exe`})

```

When the user clicks save, a prompt will appear asking whether to allow saving this file, as shown in the image (Image 1).

But when executing:

```
(await window.showSaveFilePicker({suggestedName: `hello`})).move(`hello.exe`)

```

It indeed bypasses the prompt and saves the .exe file directly to the user's disk.

Would this also be considered expected behavior? This is what initially led me to believe it might be a security issue...

### as...@chromium.org (2025-04-21)

I just remembered that there's a section of the security FAQ which addresses this <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#i-can-download-a-file-with-an-unsafe-extension-but-a-different-extension-or-file-type-is-shown-to-the-user-is-this-a-security-bug>

In this case, the extension being presented in the dialog is different from the extension the file ends up with after the `move()`. So, the guidance there arguably does apply, especially since the user activation will reliably be available

One possible mitigation would be to check the file extension given to `move()` and show this dialog if appropriate. See [here](https://crsrc.org/c/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc;l=1982-2003;drc=1d737975521c1d4191937c2c659bd78d9f1681f4)

@my...@chromium.org would you like to take this on?

### my...@chromium.org (2025-04-22)

Observed that [#comment6](https://issues.chromium.org/issues/411544197#comment6) will fail in a DCHECK enabled build at [ObjectPermissionContextBase::UpdateObjectPermission](https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/object_permission_context_base.cc;l=193;drc=1d737975521c1d4191937c2c659bd78d9f1681f4).

### pa...@chromium.org (2025-05-23)

Just a driving-by comment since I just deduped a bug into that one. I kind of agree with [#comment7](https://issues.chromium.org/issues/411544197#comment7) that we could still do something about it and check the file extension in `move()`.

### my...@chromium.org (2025-06-10)

I've a CL ready, also I just discovered a crash that related to this bug in crbug.com/423663220.

### dx...@google.com (2025-06-10)

Project: chromium/src  

Branch: main  

Author: Ming-Ying Chung [mych@chromium.org](mailto:mych@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6475317>

Add safe browsing check to [`FileSystemHandle.move()`][1]

---


Expand for full commit details

```Add safe browsing check to [`FileSystemHandle.move()`][1]

```
When the API is used together with `window.showSaveFilePicker()`, 
e.g. 
 
```js 
(await window.showSaveFilePicker({suggestedName: `hello`})).move(`hello.swf`); 
``` 
 
It may create a potentially ambiguous scenario that misleads users about 
what the actual file is downloaded. In the above example, the final 
downloaded file will be `hello.swf` (not `hello` from file picker UI). 
Per [discussion][2], It's better to ask explicitly for confirmation. 
 
This CL adds a call to `ConfirmSensitiveEntryAccess()` before calling 
`FileSystemAccessSafeMoveHelper`, i.e. `DoFileSystemOperation()`. The 
call in chrome embedder will check the destination path against 
blocklist and [show prompt UI][3] for user permissions. Example screenshot: [4]. 
 
 
[1]: https://chromestatus.com/feature/5640802622504960 
[2]: http://crbug.com/411544197#comment7 
[3]: https://crsrc.org/c/chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc;l=1982-2003;drc=1d737975521c1d4191937c2c659bd78d9f1681f4 
[4]: http://screen/AUFXTfXZxvKufEJ 
 
Bug: 411544197 
Change-Id: I9a377b42495ef1f36bb02eb0be0fdfb6055d9d83 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6475317 
Reviewed-by: Austin Sullivan <asully@chromium.org> 
Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1471747}

```
```

---

Files:
* M       `chrome/browser/file_system_access/chrome_file_system_access_permission_context_browsertest.cc`
* M       `content/browser/file_system_access/file_system_access_file_handle_impl_unittest.cc`
* M       `content/browser/file_system_access/file_system_access_handle_base.cc`
* M       `content/browser/file_system_access/file_system_access_handle_base.h`

---

Hash: eea1c4bbbf146e39d4ef0599ec05a733cb4a1aab\
Date:&nbsp; Tue Jun 10 13:34:30 2025

</details>

---

```

### sp...@google.com (2025-06-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of web platform privilege escalation where an updated POC and helpful information was provided to better demonstrate the potential for security consequences


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-18)

Thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-06-19)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### my...@chromium.org (2025-06-19)

> 1. Why does your merge fit within the merge criteria for these milestones?

This is a security fix.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/6475317>

> 3. Have the changes been released and tested on canary?

It's currently in M139 Canary <https://chromiumdash.appspot.com/commit/eea1c4bbbf146e39d4ef0599ec05a733cb4a1aab>.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

No.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Not a major issue. But good to have test team verification.

### am...@chromium.org (2025-06-20)

This is a low severity vulnerability which does not meet the security justification for backmerge to either Stable (M137) or Beta (M138), which is why the security / merge automation did not update this issue with a merge review targ. Declining backmerge and removing the merge request tag.

### pg...@google.com (2025-08-05)

Hello @reporter! How would you like to be credited for this report?

edit: jk found it!! (Huuuuu)

### ch...@google.com (2025-09-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/411544197)*
