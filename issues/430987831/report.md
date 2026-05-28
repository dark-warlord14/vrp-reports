# The Windows 10 "Show text suggestions as I type" feature does not work

| Field | Value |
|-------|-------|
| **Issue ID** | [430987831](https://issues.chromium.org/issues/430987831) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>Editing>IME, Blink>Input, Internals>PlatformIntegration, Internals>Views, UI>Input>Text |
| **Platforms** | Windows |
| **Reporter** | ph...@gmail.com |
| **Assignee** | si...@microsoft.com |
| **Created** | 2025-07-10 |
| **Bounty** | Confirmed (amount unknown) |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
Happens with earlier versions of the browsers as well of course.

It is possible that it happens with other browsers as well (Now I just checked Firefox for example and it seems like the security bug is not happening with that browser.).

For some reason this security bug is only occurring in regular browsing mode. So it can only be reproduced in that mode, since for some reason it is not happening in guest and incognito mode.

As I remember I started to notice this security bug somewhat recently. Like a week ago or so.

VERSION
Chrome Version: 138.0.7204.101 + stable ((Official version) (arm64))
Operating System: Windows 11 Home 24H2 26100.4652

REPRODUCTION CASE

1. Enable Windows text suggestions (or similar operating system feature in case other operating systems are affected as well).
2. Open the browser and open a page with a password field.
3. Enter into the field and start to type to trigger Windows text suggestions (or other operating system's similar feature (in case affected)) to appear.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Erik Engi [Oengi.com](https://oengi.com)

## Attachments

- [Mon Jul 21 2025 17:57:23 GMT+0200 (Central European Summer Time).png](attachments/Mon Jul 21 2025 17_57_23 GMT+0200 (Central European Summer Time).png) (image/png, 17.3 KB)
- [Recording 2025-07-24 141433.mp4](attachments/Recording 2025-07-24 141433.mp4) (video/mp4, 13.3 MB)

## Timeline

### el...@chromium.org (2025-07-10)

Security shepherd: thanks for the report. This does not describe a security problem - users being prompted by the system to autofill passwords is not a vulnerability in the browser. It might be a functional autofill bug, so I'll route this to the autofill team.

### ki...@gmail.com (2025-07-10)

This is not about the users being prompted by the system to autofill passwords.

This is about text suggestions appearing when the user is typing in a password field (this is not and not the same as password auto filling).

I assume that with password auto filling suggested texts do not appear (unless the user clicks and makes the password visible).
With Windows text suggestions the texts do appear as is (above the password field) based on what the user is typing in the password field. So an attacker can read the visible texts and get the password or at least enough information that the password can be easily figured out. Making the password compromised.

### ki...@gmail.com (2025-07-10)

related feature: <https://support.microsoft.com/en-us/windows/enable-text-suggestions-in-windows-0bf313ca-c992-4173-aa5f-8341d3953498>

### sc...@google.com (2025-07-11)

IIUC we'd want to disable Windows text suggestion on `<input type=password>`. +CC Mason because that sounds Blink-related.

### ki...@gmail.com (2025-07-12)

I think this is not something that should be enableable in the first place.
Since Windows text suggestion does not suggest texts with other password fields for example in the Windows account password change field or in password fields in Firefox for example.

Also as I noted before as well for some reason in guest and incognito mode this security bug is not present.

### ki...@gmail.com (2025-07-18)

related issue: <https://issues.chromium.org/issues/41441826>

(<https://github.com/chromium/chromium/commit/4210af6a47951557bb06e28513b3e4dbb1b57478>)

### ki...@gmail.com (2025-07-18)

can be related: <https://github.com/chromium/chromium/commit/fb2a2b5fb9f370d51dcf1134a51b2736cdbd47de> (, <https://github.com/chromium/chromium/commit/906b794a4ef51432fb2cf08f2bd54b5109aa5c38>)

### la...@google.com (2025-07-21)

It seems that for password fields, in regular browsing mode, we pass `IS_PASSWORD` to the Windows TSF API. [code](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/ime/win/tsf_input_scope.cc;l=115;drc=d0cdb873a9f5d9b6ef2696f65cdd80b619240b14)

This is confirmed by the tests [here](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/ime/win/tsf_input_scope_unittest.cc;l=42;drc=24d53e3e9a861c76d0e1626522c93e371f5d9223)
and [here](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/ime/win/tsf_input_scope_unittest.cc;l=125;drc=24d53e3e9a861c76d0e1626522c93e371f5d9223)

As per the [docs](https://learn.microsoft.com/en-us/windows/win32/api/InputScope/ne-inputscope-inputscope#remarks):

```
IS_PASSWORD
Value: 31
Indicates a password. IS_PASSWORD is not supported and may be altered or unavailable in the future.

Note: IS_PASSWORD only indicates the password; it doesn't provide any security around the password.
All passwords fields should have text services disabled to maintain password secrecy, and therefore 
it is not valid to have a password field with an IS_PASSWORD input scope.

```

It seems that this would be fixed by changing the scope to IS\_PRIVATE - this is what is done for Incognito and Guest mode [here](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/ime/win/tsf_input_scope.cc;l=174;drc=d0cdb873a9f5d9b6ef2696f65cdd80b619240b14). This would be consistent with the fact that this problem does not occur in Incognito and Guest mode.

I will try to repro and fix on a Windows machine and merge if it works.

### la...@google.com (2025-07-21)

I was able to reproduce this on a Windows machine - see attached screenshot. It's pretty bad!

### la...@google.com (2025-07-23)

I'll fix this next week or whenever I get Windows Cloudtop approvals.

### la...@google.com (2025-07-24)

The CL fixes this bug as verified by some manual testing. See attached video.

### dx...@google.com (2025-07-24)

Project: chromium/src  

Branch:  main  

Author:  Teodor Lamort de Gail [lamort@google.com](mailto:lamort@google.com)  

Link:    <https://chromium-review.googlesource.com/6783020>

Update deprecated TSF scope

---


Expand for full commit details
```
     
    The Windows Text Services Framework (TSF) handles text completion 
    suggestions. It has different modes depending on what kind of data is 
    being typed (numeric, email, private/non-private etc), which is handled 
    by passing a "scope" enum. 
     
    `tsf_input_scope.cc` is currently incorrectly passing `IS_PASSWORD` as 
    the scope for password fields, which is deprecated and not handled correctly (see bug). This CL changes `IS_PASSWORD` to `IS_PRIVATE`. 
     
    Bug: 430987831 
     
    Change-Id: I8441287615b6cb4a5cc06cd08ecfa521ae311dc7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6783020 
    Reviewed-by: Karol Sygiet <sygiet@google.com> 
    Reviewed-by: Colin Blundell <blundell@chromium.org> 
    Commit-Queue: Teo Lamort de Gail <lamort@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1491395}

```

---

Files:

- M `ui/base/ime/win/tsf_input_scope.cc`
- M `ui/base/ime/win/tsf_input_scope_unittest.cc`

---

Hash: [160bdd06ab574387f06de9b61baf5259c34ef22b](http://crrev.com/160bdd06ab574387f06de9b61baf5259c34ef22b)  

Date: Thu Jul 24 13:05:49 2025


---

### ki...@gmail.com (2025-07-24)

Maybe it is good to **update** this issue's **Severity** (to **S0** for example) and it's **Type** (to **Vulnerability**).

Plus **Component Tags** to one or more of the following ones:

- UI>Browser>Passwords
- Blink>SecurityFeature
- Blink>Editing>IME
- Blink>Forms>Password
- UI>Browser>ContentSuggestions

Since they are likely wrong currently. (It looks like only priority was updated since the above fields where initially set (likely to wrong values).

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. This appears to be a functional issue rather than an exploitable security issue, therefore, we are unable to extend a Chrome VRP reward for this report. 

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-10-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. This appears to be a functional issue rather than an exploitable security issue, therefore, we are unable to extend a Chrome VRP reward for this report. 
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Security Bot
> 
> 
> --
> How did we d

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/430987831)*
