# Security: Compromised renderer can steal cross-site data with minimal user interaction

| Field | Value |
|-------|-------|
| **Issue ID** | [433800617](https://issues.chromium.org/issues/433800617) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2025-07-23 |
| **Bounty** | $5,000.00 |

## Description

## SUMMARY

With a compromised renderer, a page can perform a credentialed download of a cross-site URL and then upload the downloaded response. The only user interaction needed is holding the enter key. The attack works for single files or multiple files.

To perform the attack, the PoCs performs these steps without user interaction:

1. Downloads one or more credentialed cross-site URLs, without user interaction.
2. Opens file pickers with filename prefilled with the download's predicted filename, also without user interaction.

We also bypass the user activation checks of several gated features. The only user interaction needed is holding enter to press the "Open" button in the file pickers.

This is an improved report chaining several behaviors to minimize user interaction, based on earlier research in [issue 428189828](https://issues.chromium.org/issues/428189828).

## VULNERABILITY DETAILS

### Download credentialed cross-site URL

A compromised renderer can call [`DownloadURL()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=514;drc=a5ef13fdb0138d4718cc0010b5798ec7fc753001) to initiate a credentialed download of a cross-site URL without user interaction. Cross-site URL downloads are credentialed and all cookies except `SameSite=Strict` cookies are sent. We can do this for multiple URLs when we bypass the download throttler. (I previously mentioned using `DownloadURL()` in <https://crbug.com/428189828#comment4> )

Due to [browser-side checks](https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/download_response_handler.cc;l=128;drc=5be4364dd3e4b307b5c6b3bafc5bc8652972177d), we cannot set the download filename, but we can accurately predict the filename since it's generated based on the URL path (see `getPredictedFilename()` in PoC source for details).

### Download throttler bypass

For the multiple files scenario, we need to bypass the download throttler which limits downloads to one per `WebContents` (window or tab). To bypass the download throttler, the compromised renderer calls [`LocalFrame::NotifyUserInteraction()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=888;drc=a5ef13fdb0138d4718cc0010b5798ec7fc753001) followed by `window.open()` to create a popup without user interaction. We repeat this for as many downloads as we need. (Download throttle bypass [used to be easier](https://crbug.com/40762068).)

### Set filename in open file picker

For security reasons, the open file picker isn't usually allowed to have a prefilled filename. However, there are no browser-side checks to enforce this in the file-type input code path, so a compromised renderer can call [`OpenFileChooser()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=136;drc=6c792755c1b149566fafb18355fecd7af082b799) with [`default_file_name`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=44;drc=6c792755c1b149566fafb18355fecd7af082b799) to set the prefilled filename (absolute paths are [rejected](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/file_chooser_impl.cc;l=166;drc=a789d5c7fac66ba6dc47f5b1bc02b31f6131207b) by browser). We set this to the download's filename to automatically select the downloaded file in the open file picker dialog.

In comparison, the FSA API browser-side code [ignores](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_access_manager_impl.cc;l=715;drc=23c8085b03a0c5b8cb812e4737454ad2f55a6e8b) any filename provided by renderer when using the Open dialog.

This behavior could be a standalone vulnerability since this may be useful in other attack scenarios; let me know if I should file separate crbug for this.

### User activation bypasses

To bypass various user activation checks to show file pickers, open popups, and start downloads, the compromised renderer calls [`LocalFrame::NotifyUserInteraction()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=888;drc=a5ef13fdb0138d4718cc0010b5798ec7fc753001). This is a [known issue](https://crbug.com/40091540).

### Mitigation: Last selected directory

There is a notable mitigation: The attack's happy path depends on the browser profile's [`last_selected_directory()`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;l=886;drc=1840486733c9d51af6b1c8c71d044f685a089496) being set to the user's downloads folder (on Windows, Chromium's default download folder is `%userprofile%/Downloads/`). This value is set when a user selects a file using *certain* open file pickers, including the one used by `OpenFileChooser()` (see callers of [`set_last_selected_directory()`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;l=890;drc=1840486733c9d51af6b1c8c71d044f685a089496)).

In the PoC, we try to detect if the last selected folder is **not** the downloads folder by checking if a file isn't selected within a couple of seconds. After the timeout, we ask the user to select their downloads folder and click "Open". Since the filename is prefilled, there's no need to click a specific file.

If mitigated due to a non-downloads folder, we can try to salvage the attack attempt:

- For the single file scenario, if we hit the non-downloads folder case, the attack becomes largely moot. The only attacker benefit is the prefilled filename. The page could try to convince the user they're uploading a "verification" file, but this may raise suspicion and the same goal can be achieved with pure social engineering.
- For the multiple file scenario, if we hit the non-downloads folder case, an attacker can still benefit. If the attacker convinces user to select the first file from the downloads folder, which can be an innocuous file, then holding the enter key will result in a successful attack for an unlimited number of files. The first step may raise suspicion for some users, but if the attacker succeeds there, the rest of the attack is less visible and very likely to be successful.

Anecdotally, most of the files I upload are from my downloads folder (downloading from website A to upload to website B). This may also be the case for many users who frequently download/upload PDFs, CSVs, images, etc. across websites in a similar manner.

## PROPOSED FIXES

There's several things that can be fixed, to break the chain and also mitigate any standalone impacts:

1. Prevent cross-site credentialed downloads initiated by user or compromised renderer, through Alt+Click/Enter or directly through `DownloadURL()` respectively. This work is tracked in [issue 428189828](https://issues.chromium.org/issues/428189828) per <https://crbug.com/428189828#comment3>, but as a **non**-security bug. This should break any variants that depend on cross-site credentialed download, such as the one reported in that other issue.
2. Ensure browser ignores [`default_file_name`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=44;drc=6c792755c1b149566fafb18355fecd7af082b799) in `OpenFileChooser()` params from renderer if the chooser isn't in [`kSave`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/choosers/file_chooser.mojom;l=35;drc=6c792755c1b149566fafb18355fecd7af082b799) mode. This is what the FSA API [currently does](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_access_manager_impl.cc;l=715;drc=23c8085b03a0c5b8cb812e4737454ad2f55a6e8b).
3. Longer-term: Implement browser-enforced user activation, to avoid bypasses when showing file pickers, opening popups, or starting downloads. This is a [known issue](https://crbug.com/40091540) but there are some features which currently have robust mitigations by checking [`WebContents::HasRecentInteraction()`](https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/web_contents.h;l=1522;drc=a3c9c4dcd0d6de500f41d7272d9515b6b81b7729). Of all three actions the browser could restrict, file pickers is probably the least risky option.

## VERSION

Chrome version:

- Cross-site credentialed download: 138.0.7204.169 Stable, 140.0.7313.0 Canary
- Set filename in file picker: Verified with custom build based on `aad34245b04df3c637ce7c51b5a10af879e1ac98` (July 3rd)

Operating System: Windows 10

## REPRODUCTION CASE

General notes:

- The repro shown in videos is slower than the actual repro time, due to resource constraints caused by video recording.
- In this PoC, we wait for user to interact with page before initiating downloads, but compromised renderer can perform multiple downloads at any time. We wait to avoid user suspicion before user interacts with page.

### Patch to simulate compromised renderer

To simulate a compromised renderer, the patch:

1. Disables some browser DCHECKs in `chrome/browser/file_select_helper.cc` and `ui/shell_dialogs/base_shell_dialog_win.cc`. You can alternatively build with DCHECKs disabled.
2. Updates `third_party/blink/renderer/core/html/html_marquee_element.cc` to call `NotifyUserActivation()` when `marqueeElem.stop()` is called in JS, to bypass user activation checks.
3. Updates `third_party/blink/renderer/core/html/forms/file_input_type.cc` to call `DownloadURL()` directly and set `default_file_name` in open file picker. See patch comments for how to use attributes to change behavior.

### Setup for both PoCs:

- If self-hosting or want to edit using DevTools, optionally configure the target URL in the source code (e.g. `https://myaccount.google.com/personal-info`).
- If using default target (such as on hosted PoC), navigate to <https://aogarantiza.com/set-cookies.php> to set cookies on target.
- Apply attached patch and build Chromium.

### Scenario: Single file

Using patched browser:

1. Navigate to <https://alesandroortiz.com/security/chromium/download-cross-site-theft-cr.html>
2. Press and hold enter.

- For happy path: Wait for attack to complete within a couple of seconds.
- For sad path (non-downloads folder case): Select downloads folder, then click "Open" button.

### Scenario: Multiple files

Using patched browser:

1. Navigate to <https://alesandroortiz.com/security/chromium/download-cross-site-theft-cr-multiple.html>
2. Press and hold enter.

- For happy path: Wait for attack to complete within a few seconds.
- For sad path (non-downloads folder case): Select downloads folder, then click "Open" button. Then continue from step 2 into happy path.

For both scenarios:

Observed: Compromised renderer can download multiple cross-site credentialed URLs and show open file pickers with prefilled filename. Because user is holding enter, the downloaded file is uploaded to attacker page shortly after file picker is shown.

Expected: Cross-site downloads are not credentialed, for downloads initiated by either regular or compromised renderers. Compromised renderer cannot show open file pickers with prefilled filename. To a lesser extent, a compromised renderer should not be able to download multiple files by bypassing popup blocker.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- download-cross-site-theft-cr.patch (text/x-diff, 7.2 KB)
- download-cross-site-theft-cr-multiple.html (text/html, 9.2 KB)
- download-cross-site-theft-cr-multiple.mp4 (video/mp4, 1.0 MB)
- get-cookies.php (application/x-httpd-php, 527 B)
- set-cookies.php (application/x-httpd-php, 1.3 KB)
- download-cross-site-theft-cr.html (text/html, 5.6 KB)
- download-cross-site-theft-cr.mp4 (video/mp4, 2.0 MB)

## Timeline

### al...@alesandroortiz.com (2025-07-23)

While I wasn't able to identify security impacts at a glance, several DCHECKs in `BaseShellDialogImpl` fail when a browser window tries to have multiple file pickers open at the same time. This is possible by a compromised renderer as shown in the attached PoC and in some other PoCs I have that actually show multiple file pickers at once.

The DCHECKs and comment state this isn't desired, but it may only be due to UX concerns. If someone can confirm this doesn't have security impacts, I'd appreciate it.

<https://source.chromium.org/chromium/chromium/src/+/main:ui/shell_dialogs/base_shell_dialog_win.cc;l=68;drc=e672a665ffa8fe4901184f03922e2cc548399da5>

```
std::unique_ptr<BaseShellDialogImpl::RunState> BaseShellDialogImpl::BeginRun(
    HWND owner) {
  // Cannot run a modal shell dialog if one is already running for this owner.
  DCHECK(!IsRunningDialogForOwner(owner));                                    <-- Fails when opening second file picker
  // The owner must be a top level window, otherwise we could end up with two
  // entries in our map for the same top level window.
  DCHECK(!owner || owner == GetAncestor(owner, GA_ROOT));
  auto run_state = std::make_unique<RunState>();
  run_state->dialog_task_runner = CreateDialogTaskRunner();
  run_state->owner = owner;
  if (owner) {
    GetOwners().insert(owner);
    DisableOwner(owner);
  }
  return run_state;
}

void BaseShellDialogImpl::EndRun(std::unique_ptr<RunState> run_state) {
  if (run_state->owner) {
    DCHECK(IsRunningDialogForOwner(run_state->owner));                     <-- Fails when closing second file picker
    SetOwnerEnabled(run_state->owner, true);
    DCHECK(GetOwners().find(run_state->owner) != GetOwners().end());       <-- Fails when closing second file picker
    GetOwners().erase(run_state->owner);
  }
}

```

### al...@alesandroortiz.com (2025-07-23)

## Patch (to fix prefilled filename in file picker)

The 2nd proposed fix is simple and I've verified it prevents renderers from prefilling filename in open file pickers. `FileChooserImpl::OpenFileChooser()` is only called by the renderer, normally when user opens file picker from file-type inputs, so this won't have any unintended consequences elsewhere. There's also an existing security check there.

We could go further and also restrict `title` param, since AFAICT renderer never has legitimate reason to set this, but I'll wait for feedback here since it's less important.

I'll upload CL once I have tests for this.

```
diff --git a/content/browser/web_contents/file_chooser_impl.cc b/content/browser/web_contents/file_chooser_impl.cc
index fa983471db2b..1e4cf773b153 100644
--- a/content/browser/web_contents/file_chooser_impl.cc
+++ b/content/browser/web_contents/file_chooser_impl.cc
@@ -160,6 +160,12 @@ void FileChooserImpl::OpenFileChooser(blink::mojom::FileChooserParamsPtr params,
   callback_ = std::move(callback);
   auto listener = base::MakeRefCounted<FileSelectListenerImpl>(this);
   listener_impl_ = listener.get();
+
+  // Do not allow open dialogs to have renderer-controlled default_file_name.
+  if (params->mode != blink::mojom::FileChooserParams::Mode::kSave) {
+    params->default_file_name = base::FilePath();
+  }
+
   // Do not allow messages with absolute paths in them as this can permit a
   // renderer to coerce the browser to perform I/O on a renderer controlled
   // path.

```

### ts...@google.com (2025-07-24)

Charlie, I wanted to confirm that this is within our site-isolation threat model before trying to reproduce.

### cr...@chromium.org (2025-07-24)

In general, yes, I would consider an attack that automatically downloads credentialed cross-site URLs and uploads them to the attacker to be a Site Isolation bypass, because it could be used similarly to a UXSS attack to steal credentialed information from other sites.

This looks like a nice report at first glance. I'll add dcheng@ here as well who discussed mitigating factors for [issue 428189828](https://issues.chromium.org/issues/428189828). Here it looks like a compromised renderer can avoid some of those mitigating factors (and is within scope for a Site Isolation bypass), while a few minor mitigating factors might remain (e.g., user has to hold the enter key).

Sounds like downloads folks may want to take a look if you're able to reproduce it?

### ts...@chromium.org (2025-07-24)

Good news is that patch -p0 < download-cross-site-theft-cr.patch applies at ToT 39a3c4d946


### ts...@chromium.org (2025-07-24)

Modified download-cross-site-theft-cr.html to remove all the set-cookies, will do this by hand if needed.
Removed references from reporter's site, will just host on localhost and try to snarf from example.com

### ts...@chromium.org (2025-07-24)

I must have busted something because I can't make it work against localhost, and policy prevents us from trying a cookie stealing attack against your live site.  We can believe that the requests are credentialed, so you can provide us with a version that shows the contents of, say, https://example.com/index.html in a textarea on download-cross-site-theft-cr.html as hosted on localhost, then we can continue.

### al...@alesandroortiz.com (2025-07-24)

You can edit `targetUrl` in `download-cross-site-theft-cr.html` or `targetUrls` in `download-cross-site-theft-cr-multiple.html` to use `https://example.com/index.html`, `https://www.google.com/robots.txt`, or any other URL you're allowed to use. These URLs are already included in the multiple files PoC source, you only need to comment them in/out as needed there. I've verified both PoCs work with these URLs when hosted on localhost.

### pe...@google.com (2025-07-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### ts...@google.com (2025-07-24)

Chain keeps stopping at Please select the downloads folder, then click open. I wasn't quite sure what to make of your instructions in this case.

### al...@alesandroortiz.com (2025-07-24)

Hm. Those fallback instructions are shown if you hit the mitigation mentioned in [Mitigation: Last selected directory](https://issues.chromium.org/issues/433800617#:~:text=Mitigation%3A%20Last%20selected%20directory). Is the directory picker still open when you see those instructions, or do you see the file contents at the bottom of the attacker page? I put a fairly short timeout for those instructions, maybe we're showing the fallback instructions too early and the attack would still succeed if you kept holding enter.

If the directory picker is still open, follow the "sad path" instructions per original report repro steps:

> For sad path (non-downloads folder case): Select downloads folder, then click "Open" button. (For multiple files scenario: Then continue from step 2 into happy path.)

After you've selected the directory once, you can restart the whole repro to see the happy path, where attack should occur quickly.

If the file picker is still open, do you see the filename prefilled and is the downloaded file in the folder? If filename is not prefilled, then something isn't working right in PoC. If it's prefilled, holding enter should click the "Open" button to upload the file as soon as the dialog starts to open.

The attack also only work on Windows, in case you're using another OS. I'm using Windows 10, not sure if Windows 11 may also have some differences.

### pe...@google.com (2025-07-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### ts...@google.com (2025-07-24)

Ah, we usually try to repro on linux as it is the most general. Will find a windows environment.

### al...@alesandroortiz.com (2025-07-25)

Uploaded CL with patch from [#comment3](https://issues.chromium.org/issues/433800617#comment3) to clear `default_file_name` in non-save file pickers: <https://crrev.com/c/6786387>

Will add reviewers after dryrun.

### al...@alesandroortiz.com (2025-07-25)

## Patch (to make cross-site downloads non-credentialed)

**Update:** Setting `credentials_mode_` doesn't seem to affect behavior, either with `kSameOrigin` or `kOmit`. Not sure why. I'll keep investigating.

**Update 2:** I got `credentials_mode_` to be set properly (needed to set `credentials_mode` in `CreateRequestInfo()` with value from download params, but now download fails due to a [network service check](https://source.chromium.org/chromium/chromium/src/+/main:services/network/cors/cors_url_loader_factory.cc;l=783;drc=ea0d5e794038736af8402e746fcda856985e476c). I'm not sure what the best way to proceed is, since the Fetch spec says downloads should always be treated as navigations, but we need an exception here for security purposes. As noted in <https://issues.chromium.org/issues/428189828#comment3>, Firefox and Safari don't send credentials in this scenario.

---

For the 1st proposed fix (which also fixes [issue 428189828](https://issues.chromium.org/issues/428189828)), we can set `parameters->credentials_mode_` to `kSameOrigin` in [`RenderFrameHostImpl::DownloadURL()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=7453;drc=285461c1e4957f186a9273ae4db8796ea3c35c88). Currently it uses the default credentials mode, [`kInclude`](https://source.chromium.org/chromium/chromium/src/+/main:components/download/public/common/download_url_parameters.cc;l=22;drc=285461c1e4957f186a9273ae4db8796ea3c35c88).

The renderer only seems to make the Mojo call when a user:

- clicks on link with `download` attribute
- uses Alt+Click/Enter on any link
- clicks download button on video player controls
- clicks "Save image as..." in context menu

In all the scenarios above, making them use `kSameOrigin` for downloads is probably fine. AFAIK for cross-site embedded content, the initial request when the content was embedded in page isn't credentialed, so downloading with `kSameOrigin` should not behave differently compared to the initial request.

But during CL review, I'll ask for someone to double-check that these are all the call sites, and that the new behavior is acceptable. ~~I'll upload CL for this soon.~~

### al...@alesandroortiz.com (2025-07-25)

To make cross-site downloads credentialless, I'll wait for team to decide whether they want this to actually happen before trying to implement further. See [#comment16](https://issues.chromium.org/issues/433800617#comment16) for details. I'll also mention this in [issue 428189828](https://issues.chromium.org/issues/428189828) which was meant to track this work too.

### dx...@google.com (2025-07-25)

Project: chromium/src  

Branch:  main  

Author:  Alesandro Ortiz [alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)  

Link:    <https://chromium-review.googlesource.com/6786387>

Clear `default_file_name` for non-save file pickers.

---


Expand for full commit details

```Clear `default_file_name` for non-save file pickers.

```
This only affects file pickers opened by renderer. This code path is 
used by file-type inputs. 
 
Bug: 433800617 
Change-Id: Ia144bda955fdd4b827448e49ebd051d48dd7dbf7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6786387 
Reviewed-by: Austin Sullivan <asully@chromium.org> 
Reviewed-by: Charlie Reis <creis@chromium.org> 
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
Commit-Queue: Alesandro Ortiz <alesandro@alesandroortiz.com> 
Cr-Commit-Position: refs/heads/main@{#1492358}

```
```

---

Files:
* M       `content/browser/web_contents/file_chooser_impl.cc`
* A       `content/browser/web_contents/file_chooser_impl_unittest.cc`
* M       `content/test/BUILD.gn`
* M       `third_party/blink/public/mojom/choosers/file_chooser.mojom`

---

Hash: [ebee769e5e2e914e34b4ce20f956863d62bb7c3b](http://crrev.com/ebee769e5e2e914e34b4ce20f956863d62bb7c3b)\
Date: Fri Jul 25 23:46:32 2025

</details>

---

```

### pg...@google.com (2025-07-29)

chlily@, can you take a look?

Setting S2 for cross site data leak with compromised renderer
I have not been able to repro, but setting foundin to 138 conservatively - please correct if I am wrong!

### al...@alesandroortiz.com (2025-07-29)

CL in [#comment18](https://issues.chromium.org/issues/433800617#comment18) breaks this chain, so this can be marked as fixed.

[Issue 428189828](https://issues.chromium.org/issues/428189828) is unassigned but supposed to track potential removal of credentialed cross-site downloads.

I have another PoC to read arbitrary local files using this technique. Should have it here within a day or so.

I also have yet another bypass that I'll report separately this week with nearly identical impacts, but requires different fix.

### ch...@google.com (2025-07-29)

Setting milestone because of s2 severity.

### ch...@google.com (2025-07-29)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@chromium.org (2025-07-29)

Marking fixed per [comment #20](https://issues.chromium.org/issues/433800617#comment20) (and I didn't help at all here, so reassigning).

### ch...@google.com (2025-07-30)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### cr...@chromium.org (2025-07-31)

[#comment20](https://issues.chromium.org/issues/433800617#comment20): Thanks! I'll mark [issue 428189828](https://issues.chromium.org/issues/428189828) and [issue 40091540](https://issues.chromium.org/issues/40091540) as non-blocking child issues of this, since they would provide additional lines of defense. Please post the new issue ID here as well once you file it, to help us follow along.

[#comment23](https://issues.chromium.org/issues/433800617#comment23): Ok, I'll try to move the merge along as well.

[#comment24](https://issues.chromium.org/issues/433800617#comment24):

> no relevant commits could be automatically detected (via Git Watcher comments)

That's weird, since <https://chromium-review.googlesource.com/6786387> was posted in [#comment18](https://issues.chromium.org/issues/433800617#comment18), and it shows up in the Code Changes field.

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/6786387> (which landed in 140.0.7319.0)

> Has this fix been verified on Canary to not pose any stability regressions?

It's hard to manually verify the fix on Canary because the repro steps involve patching the renderer process code. However, no new related stability issues seem to have been introduced in 140.0.7319.0, and there is a very low risk of stability issues from the CL itself.

> Does this fix pose any potential non-verifiable stability risks?

There's a small risk that there might have been some way for renderers to specify the default\_file\_path for non-save dialogs before, and that this change might affect that UX. We're not aware of any cases where that's possible, though.

> Does this fix pose any known compatibility risks?

No, it's purely about the default file name shown user-facing dialogs.

> Does it require manual verification by the test team? If so, please describe required testing.

No, it's not easy to test without a compromised renderer process.

> (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

I think it affects all desktop platforms, so I've updated that.

### pg...@google.com (2025-07-31)

nothing relevant as far as I can see in canary/dev, but please do review both before backmerging!

merge approved for M139 for <https://chromium-review.git.corp.google.com/c/chromium/src/+/6786387>! please merge by Friday 10AM Aug 1 to maybe get this fix into the next M139 release!

### al...@alesandroortiz.com (2025-07-31)

If creis@ can do backmerges, I would appreciate it. I'm a bit swamped with more bugs to report. :)

### cr...@chromium.org (2025-07-31)

Sure, will do.

### al...@alesandroortiz.com (2025-07-31)

As promised in [#comment20](https://issues.chromium.org/issues/433800617#comment20): See <https://issues.chromium.org/issues/435491101#comment3> for arbitrary local file read using separate vuln + chaining this vuln to minimize user interaction.

### dx...@google.com (2025-07-31)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Alesandro Ortiz [alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)  

Link:    <https://chromium-review.googlesource.com/6806917>

[M139] Clear `default_file_name` for non-save file pickers.

---


Expand for full commit details

```[M139] Clear `default_file_name` for non-save file pickers.

```
This only affects file pickers opened by renderer. This code path is 
used by file-type inputs. 
 
(cherry picked from commit ebee769e5e2e914e34b4ce20f956863d62bb7c3b) 
 
Bug: 433800617 
Change-Id: Ia144bda955fdd4b827448e49ebd051d48dd7dbf7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6786387 
Reviewed-by: Austin Sullivan <asully@chromium.org> 
Reviewed-by: Charlie Reis <creis@chromium.org> 
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
Commit-Queue: Alesandro Ortiz <alesandro@alesandroortiz.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1492358} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6806917 
Auto-Submit: Charlie Reis <creis@chromium.org> 
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
Cr-Commit-Position: refs/branch-heads/7258@{#2316} 
Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```
```

---

Files:
* M       `content/browser/web_contents/file_chooser_impl.cc`
* A       `content/browser/web_contents/file_chooser_impl_unittest.cc`
* M       `content/test/BUILD.gn`
* M       `third_party/blink/public/mojom/choosers/file_chooser.mojom`

---

Hash: [9026493c3ff47e300069b58e6ae671f3a0a310ee](http://crrev.com/9026493c3ff47e300069b58e6ae671f3a0a310ee)\
Date: Thu Jul 31 22:29:45 2025

</details>

---

```

### pe...@google.com (2025-07-31)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### al...@alesandroortiz.com (2025-08-02)

I filed a similar issue with slightly different impacts: [issue 435684924](https://issues.chromium.org/issues/435684924).

### cr...@chromium.org (2025-08-04)

Re: [#comment31](https://issues.chromium.org/issues/433800617#comment31) about LTS Milestone M138:

> Was this issue a regression for the milestone it was found in?

No, this was likely a longstanding issue predating M138.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### sp...@google.com (2025-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high quality report of mitigated site isolation bypass / user information disclosure, requiring compromised renderer, user interaction, and not covert / can be quite apparent to a user during exploitation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### al...@alesandroortiz.com (2025-08-26)

Thanks for the reward!

I landed the fix in [#comment18](https://issues.chromium.org/issues/433800617#comment18) so the patch bonus is missing :)

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 patch bonus for self-committed patch + unit test. Sorry we missed this the first time around!


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### al...@alesandroortiz.com (2025-09-04)

Cheers, thank you so much Amy!

### pe...@google.com (2025-09-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-05)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6862014
2. Low - There was no conflict.
3. 139
4. Yes, according to the comment #33, this issue seems a longstanding issue predating M138.

### pe...@google.com (2025-09-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-06)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6861703
2. Low - There was no conflict.
3. 139
4. Yes, according to the comment #33, this issue seems a longstanding issue predating M132.

### dx...@google.com (2025-09-11)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Alesandro Ortiz [alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)  

Link:    <https://chromium-review.googlesource.com/6861703>

[M132-LTS] Clear `default_file_name` for non-save file pickers.

---


Expand for full commit details

```[M132-LTS] Clear `default_file_name` for non-save file pickers.

```
This only affects file pickers opened by renderer. This code path is 
used by file-type inputs. 
 
(cherry picked from commit ebee769e5e2e914e34b4ce20f956863d62bb7c3b) 
 
Bug: 433800617 
Change-Id: Ia144bda955fdd4b827448e49ebd051d48dd7dbf7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6786387 
Commit-Queue: Alesandro Ortiz <alesandro@alesandroortiz.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1492358} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6861703 
Reviewed-by: Nasko Oskov <nasko@chromium.org> 
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
Cr-Commit-Position: refs/branch-heads/6834@{#5638} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```
```

---

Files:
* M       `content/browser/web_contents/file_chooser_impl.cc`
* A       `content/browser/web_contents/file_chooser_impl_unittest.cc`
* M       `content/test/BUILD.gn`
* M       `third_party/blink/public/mojom/choosers/file_chooser.mojom`

---

Hash: [2bb317fede2918fc0c31642745fbe7e1352bb80a](https://chromiumdash.appspot.com/commit/2bb317fede2918fc0c31642745fbe7e1352bb80a)\
Date: Thu Sep 11 04:09:37 2025

</details>

---

```

### dx...@google.com (2025-09-11)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Alesandro Ortiz [alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)  

Link:    <https://chromium-review.googlesource.com/6862014>

[M138-LTS] Clear `default_file_name` for non-save file pickers.

---


Expand for full commit details

```[M138-LTS] Clear `default_file_name` for non-save file pickers.

```
This only affects file pickers opened by renderer. This code path is 
used by file-type inputs. 
 
(cherry picked from commit ebee769e5e2e914e34b4ce20f956863d62bb7c3b) 
 
Bug: 433800617 
Change-Id: Ia144bda955fdd4b827448e49ebd051d48dd7dbf7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6786387 
Commit-Queue: Alesandro Ortiz <alesandro@alesandroortiz.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1492358} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6862014 
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: Nasko Oskov <nasko@chromium.org> 
Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
Cr-Commit-Position: refs/branch-heads/7204@{#3402} 
Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```
```

---

Files:
* M       `content/browser/web_contents/file_chooser_impl.cc`
* A       `content/browser/web_contents/file_chooser_impl_unittest.cc`
* M       `content/test/BUILD.gn`
* M       `third_party/blink/public/mojom/choosers/file_chooser.mojom`

---

Hash: [af46c960c59faaaa163c93301de44353810f7e1a](https://chromiumdash.appspot.com/commit/af46c960c59faaaa163c93301de44353810f7e1a)\
Date: Thu Sep 11 13:48:48 2025

</details>

---

```

### dx...@google.com (2025-09-26)

Project: chromium/src  

Branch:  refs/branch-heads/7204\_184  

Author:  Alesandro Ortiz [alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)  

Link:    <https://chromium-review.googlesource.com/6986402>

[CfM-M138] Clear `default_file_name` for non-save file pickers.

---


Expand for full commit details

```[CfM-M138] Clear `default_file_name` for non-save file pickers.

```
This only affects file pickers opened by renderer. This code path is 
used by file-type inputs. 
 
(cherry picked from commit ebee769e5e2e914e34b4ce20f956863d62bb7c3b) 
 
(cherry picked from commit af46c960c59faaaa163c93301de44353810f7e1a) 
 
Bug: 433800617 
Change-Id: Ia144bda955fdd4b827448e49ebd051d48dd7dbf7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6786387 
Commit-Queue: Alesandro Ortiz <alesandro@alesandroortiz.com> 
Cr-Original-Original-Commit-Position: refs/heads/main@{#1492358} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6862014 
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: Nasko Oskov <nasko@chromium.org> 
Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
Cr-Original-Commit-Position: refs/branch-heads/7204@{#3402} 
Cr-Original-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6986402 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Owners-Override: Joshua Pius <joshuapius@google.com> 
Cr-Commit-Position: refs/branch-heads/7204_184@{#55} 
Cr-Branched-From: 7ea839044480a944888296dc0cccc5afb60b736c-refs/branch-heads/7204@{#2436} 
Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```
```

---

Files:
* M       `content/browser/web_contents/file_chooser_impl.cc`
* A       `content/browser/web_contents/file_chooser_impl_unittest.cc`
* M       `content/test/BUILD.gn`
* M       `third_party/blink/public/mojom/choosers/file_chooser.mojom`

---

Hash: [9ebae766cde4b83b398193e29adf9df3d9c0f30c](https://chromiumdash.appspot.com/commit/9ebae766cde4b83b398193e29adf9df3d9c0f30c)\
Date: Fri Sep 26 19:51:29 2025

</details>

---

```

### ch...@google.com (2025-11-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality report of mitigated site isolation bypass / user information disclosure, requiring compromised renderer, user interaction, and not covert / can be quite apparent to a user during exploitation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/433800617)*
