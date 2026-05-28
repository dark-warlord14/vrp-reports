# Third party installed extensions can silently increase permissions on update

| Field | Value |
|-------|-------|
| **Issue ID** | [435980394](https://issues.chromium.org/issues/435980394) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | po...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2025-08-03 |
| **Bounty** | $2,000.00 |

## Description

# Vulnerability Details

Extensions on Chrome are very powerful. They can control many aspects of the browser including (but not limited to) accessing user data, downloading files on user's machine, modifying the webpages visited by the user. Whenever a user installs an extension from Chrome Web Store, they see a list of permissions which the extension asks for. The extension can only be installed if the user grants those permissions.

When a new version of the extension asks for more permissions than what the user originally accepted, Chrome disables the extension and notifies the user. The updated permissions are shown to the user and the extension is only enabled when the user accepts the new permissions.

In addition to the user themselves installing an extension from Chrome Web Store, [third party apps can also install extensions](https://developer.chrome.com/docs/extensions/how-to/distribute/install-extensions) on Chrome. This is done by adding a registry entry on Windows or via a preferences JSON file on macOS. Extensions added by this mechanism are **disabled initially**. User must accept their permissions to enable them. However, once they are enabled, **Chrome doesn't disable them if a new extension update increases its permissions**. The new update can have significantly different permissions than what the user allowed. The permissions are silently granted and the user doesn't even know that the extension can do more things now (possibly malicious).

# Version

Chrome Version: 138.0.7204.184 - Stable.

Operating System: Tested on macOS, but should repro on all platforms.

# Reproduction Case

1. Publish an extension on Chrome Web Store.
2. Install it via a preferences file on macOS.
3. Extension will be disabled initially. Enable it by accepting the permissions.
4. Publish an update to the extension on Chrome Web Store. The update should have more permissions.
5. Restart Chrome and wait for extension updates to finish.

Observe that the extension is still enabled but has increased permissions.

Since this reproduction is difficult (because it requires publishing to store), I am attaching videos of the repro case.

1. The first video shows the case where the extension is installed normally. It gets disabled on update due to permissions increase.
2. The second video shows the same extension installed via preferences file (macOS). It can be observed that it silently increases permissions on update and remains enabled.

# Code references

1. [Permissions increase check](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/chrome_extension_registrar_delegate.cc;l=517;drc=877c4eff05eee91a64ab498b2f02928fe718278b) is only done for extensions with `kInternal` manifest location.
2. This wasn't always the case. When the check was originally added, it also checked for kExternal manifest locations. A later commit changed to code to just check for kInternal location, probably unintentionally.

Original commit (see ExtensionsService::OnExtensionsLoaded method): <https://codereview.chromium.org/165414/diff/3007/chrome/browser/extensions/extensions_service.cc>

The commit which probably introduced the regression (see ExtensionsService::OnExtensionsLoaded method):
<https://codereview.chromium.org/4687005/diff/73001/chrome/browser/extensions/extensions_service.cc>

# Potential fix

`ChromeExtensionRegistrarDelegate::CheckPermissionsIncrease` only checks for kInternal manifest location. It should also check for external manifest locations (but still exclude policy installs and component installs).

```
 if (extension->location() == ManifestLocation::kInternal &&
     !auto_grant_permission) {
// ...

```

The above code should be changed to something like this

```
bool is_trusted_location = Manifest::IsComponentLocation(extension->location()) ||
                           Manifest::IsPolicyLocation(extension->location())
                           Manifest::IsUnpackedLocation(extension->location());
if (!is_trusted_location && !auto_grant_permission) {
// ...

```

## Attachments

- [Installed_by_user.mov](attachments/Installed_by_user.mov) (video/quicktime, 18.9 MB)
- [Installed_externally.mov](attachments/Installed_externally.mov) (video/quicktime, 17.6 MB)
- third party.svg (image/svg+xml, 19.2 KB)

## Timeline

### ja...@chromium.org (2025-08-04)

[security shepherd]
Adding anunoy@ to take a look and help with triage.

### an...@google.com (2025-08-04)

The later commit referenced by the reporter was created 10 years ago, so the current behavior has been in place for a long time! Tagging in @tj...@google.com, @so...@google.com to see if they know why the permissions check is only limited to extensions with kInternalLocation. (<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/chrome_extension_registrar_delegate.cc;l=517;drc=877c4eff05eee91a64ab498b2f02928fe718278b>).

### so...@chromium.org (2025-08-04)

redacted

### so...@chromium.org (2025-08-04)

The CL labeled as a regression actually merged 15 years [ago](https://crbug.com/40259901#comment6) in 2010.

### ja...@chromium.org (2025-08-04)

[security shepherd]

Assigning to you as the owner for now, solomonkinard@.

I'll assign Medium severity provisionally.

OS as desktop.
Component as Extensions. found in to extended stable.

### ch...@google.com (2025-08-05)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### po...@gmail.com (2025-08-11)

Please let me know if any additional information is required.

### ch...@google.com (2025-08-19)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### so...@chromium.org (2025-08-19)

Looking.

### so...@chromium.org (2025-08-19)

Changed priorities.

### aj...@google.com (2025-09-11)

(Please consult the security team before changing an issue's severity).

### ch...@google.com (2025-09-12)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### so...@chromium.org (2025-09-27)

I glanced at this in the morning, but worked on an unrelated crash fix today, which still needs a little more time. Can take a look at this 3P bug next week since H. pinged me about it -- not knowing that the priority increased to P1 until today.

### ch...@google.com (2025-10-11)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### so...@chromium.org (2025-10-14)

WIP.

### so...@chromium.org (2025-10-14)

(was out for a few days)

### ch...@google.com (2025-10-29)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-13)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-28)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### so...@chromium.org (2025-12-09)

WIP.

### ch...@google.com (2025-12-24)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-08)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-01-14)

Project: chromium/src  

Branch:  main  

Author:  Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7265369>

Extensions: Permissions: Disable external extensions on increase

---


Expand for full commit details
```
     
    Disable externally installed extensions if their permissions have 
    increased. 
     
    Bug: 435980394 
    Change-Id: I39ab160ecade0cbd582d65801a3f47b72976ce7d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7265369 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1569353}

```

---

Files:

- M `chrome/browser/extensions/chrome_extension_registrar_delegate.cc`
- A `chrome/browser/extensions/external_extension_install_browsertest.cc`
- M `chrome/test/BUILD.gn`

---

Hash: [b846067dcb8e1024449a9682761a4867b85140a7](https://chromiumdash.appspot.com/commit/b846067dcb8e1024449a9682761a4867b85140a7)  

Date: Wed Jan 14 22:49:06 2026


---

### sp...@google.com (2026-01-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
mitigated web platform privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/435980394)*
