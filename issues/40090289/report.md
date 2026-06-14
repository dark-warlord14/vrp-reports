# Security: DevTools protocol clients (e.g. extensions) can read arbitrary local files via DOM.setFileInputFiles

| Field | Value |
|-------|-------|
| **Issue ID** | [40090289](https://issues.chromium.org/issues/40090289) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | dg...@chromium.org |
| **Created** | 2018-01-24 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

DevTools protocol v1.3 offers the DOM.setFileInputFiles method (implemented by content::protocol::DOMHandler::SetFileInputFiles [1]), to allow clients to assign a file to an <input type=file>. The file is given as a string, so DevTools API clients (e.g. extensions and remote debuggers) can read any local file at the DevTools host.

**VERSION**  

Chrome Version: 63.0.3239.132 (stable), 66.0.3330.0 (Canary)

**REPRODUCTION CASE**  

Load the attached extension, e.g. at chrome://extensions , "Enable Developer mode" and "Load unpacked extension".

The attached extension uses the chrome.debugger API to connect to the DevTools protocol backend, and show the contents of a local file in a dialog box.

[1] <https://chromium.googlesource.com/chromium/src/+/7654576158eac23f4a60e7bbdf40861138d00f3e/content/browser/devtools/protocol/dom_handler.cc#36>

## Attachments

- [debugger-setFileInputFiles.zip](attachments/debugger-setFileInputFiles.zip) (application/octet-stream, 1.2 KB)

## Timeline

### me...@chromium.org (2018-01-24)

Security sheriff here: Thanks for the report, but it's not clear to me what the vulnerability is here. It's expected that an extension that has access to devtools can use all its privileges.

Perhaps we need to make the debugger permission a bit more clear. It currently says "Access page debugger backend" and "Read and change all your data on the websites you visit", but devtools certainly can do more than that.

That said, I'll leave this to devtools and extension folks to triage.

### ro...@robwu.nl (2018-01-24)

Local file access is considered a very sensitive operation that requires an explicit manual opt-in via the chrome://extensions page (in addition to requesting the "file://" permission in the manifest file).

The vulnerability here is that extensions can read local files meeting these two conditions.

What I would suggest here is to require a Blob/File object (or a representation thereof) as input (instead of a string in the platform's native file path format), instead of a list of strings.
If that is infeasible, I would recommend blocking the DOM.setFileInputFiles command unless the extension is granted the "Allow access to local file URLs" capability.

### ro...@robwu.nl (2018-01-24)

s/meeting these two conditions/without meeting these two conditions/

### me...@chromium.org (2018-01-24)

Fair, but I'm not sure how maintainable such fixes are in the long term. Devtools is going to add new APIs and extensions will not be able to keep up. We should at least let the user know that installing a debugger extension has (or might have) implications beyond reading all site data.

### ro...@robwu.nl (2018-01-24)

The fact that DevTools evolves shouldn't be a blocker for trying to keep the extension API sane. Without the DevTools API, a malicious extension with all permissions can wreck the user's browsing experience, but anything outside the browser's scope (local files) is safe by default. This is a very nice aspect of the extension API design, and should be kept in that way IMO.

https://crbug.com/chromium/805043 (which you've opened) is about investigating the feasibility of guarding DevTools API access behind a "Developer Mode" checkbox. This would signal "that installing a debugger extension has (or might have) implications beyond reading all site data."

( I do really hope that efforts such as https://crbug.com/chromium/805043 won't be seen as a wildcard ticket to permit extensions to use really powerful functionality such as running external programs or reading/writing arbitrary local files through the extension API. )

### me...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@robwu.nl (2018-02-17)

In https://crbug.com/805445#c22 you're claiming that you're working on a new interface for downloads (to move from local files to some kind of stream), with a reference to https://crrev.com/c/861546

Any similar plans for uploads (this bug) ?

### sh...@chromium.org (2018-02-24)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-03-30)

Friendly ping from the security sheriff. Can we get any update on this?

### dg...@chromium.org (2018-03-30)

Now that we have a mechanism of restricted clients in place, this should be easy to fix.

### dg...@chromium.org (2018-03-30)

Actually, as we discussed offline, reading files is within capabilities expected from debugging extension. +Pavel for thoughts.

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-05-14)

dgozman: In #14, are you saying this is WAI? Or is there a fix that needs to be done?

### dg...@chromium.org (2018-05-14)

From debugging perspective, this is WAI. The browser can read files, and if debugging extension controls the browser, it can instruct browser to read files.

However, if someone from security feels strongly about this, we can restrict this specific API for extensions (as opposite to DevTools or automation drivers).

### rs...@chromium.org (2018-05-14)

Got it, thanks. I defer to meacer@ on the extension question.

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2018-11-12)

Any update here? Extensions that lack the "file:///" permission AND "Allow access to local files" opt-in should not be able to read arbitrary local files without user interaction.

The PoC still works in Chrome 70...

At the very least, a simple fix could be blocking "DOM.setFileInputFiles" at the extension implementation level if the extension is not supposed to have local file access.

### bu...@chromium.org (2018-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7aaf7e9031ee16b9d4212fa0bc03d94713b3261b

commit 7aaf7e9031ee16b9d4212fa0bc03d94713b3261b
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Wed Nov 14 04:25:36 2018

[DevTools] Guard DOM.setFileInputFiles under MayAffectLocalFiles

Bug: 805557
Change-Id: Ib6f37ec6e1d091ee54621cc0c5c44f1a6beab10f
Reviewed-on: https://chromium-review.googlesource.com/c/1334847
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Commit-Queue: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#607902}
[modify] https://crrev.com/7aaf7e9031ee16b9d4212fa0bc03d94713b3261b/content/browser/devtools/protocol/dom_handler.cc
[modify] https://crrev.com/7aaf7e9031ee16b9d4212fa0bc03d94713b3261b/content/browser/devtools/protocol/dom_handler.h
[modify] https://crrev.com/7aaf7e9031ee16b9d4212fa0bc03d94713b3261b/content/browser/devtools/render_frame_devtools_agent_host.cc


### ro...@robwu.nl (2018-11-14)

The above patch fixes the bug (verified in 72.0.3611.0), but also makes it impossible for extensions to use this API even with the right permissions because "ExtensionDevToolsClientHost::MayAffectLocalFiles" unconditionally returns false even if the extension was granted access to local files.

To test: Edit manifest.json of the test case, and add "file://*/*" or "<all_urls>".
If loaded as an unpacked extension, local file access is automatically granted.
Otherwise (if installed via a CRX file), local file access needs to be enabled at chrome://extensions/.

To fix that, replace "return false;" with:
return (extension_->creation_flags() & Extension::ALLOW_FILE_ACCESS);

at https://chromium.googlesource.com/chromium/src/+/c8aff835e08a6604b87bcc8c32aa85295eda654d/chrome/browser/extensions/api/debugger/debugger_api.cc#386

### ro...@robwu.nl (2018-11-14)

> and add "file://*/*" or "<all_urls>".

Should have been:
  and add "file://*/*" or "<all_urls>" to the "permissions" array.

And the suggested "return ( .. & ... );" should of course end with "!= 0".

### dg...@chromium.org (2018-11-14)

I am not sure we do want to expose access even for extensions with files permission. I am not aware of the usecase. Maybe Devlin has an opinion?

### rd...@chromium.org (2018-11-14)

It seems like it should, intuitively, work for extensions with file access.  They could otherwise access files by opening the file in the browser and injecting in the page.  I don't know enough about this specific devtools API to speak to the use cases.

### dg...@chromium.org (2018-11-26)

Alright, let me close this one until we hear about a usecase. There is no need to preemptively allow setFileInputFiles.

### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-12-14)

awhalley@ - seems like no merge required.

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thank you for your report, the Panel decided to reward $2,000 for this report. 

### ab...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/805557?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090289)*
