# Security: Heap-use-after-free in GetAuthorizationRightsWithPrompt

| Field | Value |
|-------|-------|
| **Issue ID** | [40067948](https://issues.chromium.org/issues/40067948) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Mac |
| **Reporter** | me...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2023-07-24 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the patch to Chromium and compile Chromium with ASAN enabled
2. start a http server in the folder of poc.html
3. run `./Chromium --enable-features=BiometricAuthenticationForFilling --user-data-dir=./noexist http://127.0.0.1:8605/poc.html` click the password field and choose the password.

**Problem Description:**  

0. Introduction

This is a security bug that relies on a compromised render to store a password, and there is a likely enough user interaction to trigger this bug.

Note that this bug could also be triggered WITHOUT a compromised render if a user has already stored one or more passwords in the browser.

1. Analysis

`GetAuthorizationRightsWithPrompt` will create a string `prompt_string` in an IF block, its lifetime will end after IF statement. But there is a pointer of `prompt_string.c_str()` passed out of the IF block, UAF occurs when the freed string is used in `AuthorizationCopyRights`.

```
ScopedAuthorizationRef GetAuthorizationRightsWithPrompt(  
    AuthorizationRights\* rights,  
    CFStringRef prompt,  
    AuthorizationFlags extra_flags) {  
  ScopedAuthorizationRef authorization = CreateAuthorization();  
  if (!authorization) {  
    return authorization;  
  }  
  
  // Never consider the current WatchHangsInScope as hung. There was most likely  
  // one created in ThreadControllerWithMessagePumpImpl::DoWork(). The current  
  // hang watching deadline is not valid since the user can take unbounded time  
  // to answer the password prompt. HangWatching will resume when the next task  
  // or event is pumped in MessagePumpCFRunLoop so there is not need to  
  // reactivate it. You can see the function comments for more details.  
  base::HangWatcher::InvalidateActiveExpectations();  
  
  AuthorizationFlags flags = kAuthorizationFlagDefaults |  
                             kAuthorizationFlagInteractionAllowed |  
                             kAuthorizationFlagExtendRights |  
                             kAuthorizationFlagPreAuthorize | extra_flags;  
  
  // product_logo_32.png is used instead of app.icns because Authorization  
  // Services can't deal with .icns files.  
  NSString\* icon_path =  
      [base::apple::FrameworkBundle() pathForResource:@"product_logo_32"  
                                               ofType:@"png"];  
  const char\* icon_path_c = [icon_path fileSystemRepresentation];  
  size_t icon_path_length = icon_path_c ? strlen(icon_path_c) : 0;  
  
  // The OS will display |prompt| along with a sentence asking the user to type  
  // the "password to allow this."  
  const char\* prompt_c = nullptr;  
  size_t prompt_length = 0;  
  if (prompt) {  
    std::string prompt_string = SysCFStringRefToUTF8(prompt);  // ==> prompt_string will be freed after if statement  
    prompt_c = prompt_string.c_str();  
    prompt_length = prompt_string.length();  
  }     
  
  AuthorizationItem environment_items[] = {  
    {kAuthorizationEnvironmentIcon, icon_path_length, (void\*)icon_path_c, 0},  
    {kAuthorizationEnvironmentPrompt, prompt_length, (void\*)prompt_c, 0}  
  };  
  
  AuthorizationEnvironment environment = {std::size(environment_items),  
                                          environment_items};  
  
  OSStatus status = AuthorizationCopyRights(authorization, rights, &environment,  
                                            flags, nullptr);  
  
  if (status != errAuthorizationSuccess) {  
    if (status != errAuthorizationCanceled) {  
      OSSTATUS_LOG(ERROR, status) << "AuthorizationCopyRights";  
    }  
    return ScopedAuthorizationRef();  
  }  
  
  return authorization;  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:base/mac/authorization_util.mm;l=77;drc=21e25b15d346744f44c15199d9c3098584774a09;bpv=0;bpt=0>

To trigger this bug, you need to enable `password_manager::prefs::kHadBiometricsAvailable` and `password_manager::prefs::kBiometricAuthenticationBeforeFilling`, which I patched in `change.txt`.

Besides, this bug needs a saved password, I patch the renderer to simulate a compromised renderer to save a password without user interaction. See the `change.txt` for more info.

2. Bisect

This problem is introduced by this commit: 21e25b15d346744f44c15199d9c3098584774a09  

<https://chromium-review.googlesource.com/c/chromium/src/+/4633989>

According to CrhomiumDash, this UAF affects Chrome DEV 117.0.5897.3

3. Suggested Patch  
   
   Move the `prompt_string` out of the IF block.

```
diff --git a/base/mac/authorization_util.mm b/base/mac/authorization_util.mm  
index 449136d8d70..afaba6273df 100644  
--- a/base/mac/authorization_util.mm  
+++ b/base/mac/authorization_util.mm  
@@ -74,8 +74,9 @@ ScopedAuthorizationRef GetAuthorizationRightsWithPrompt(  
   // the "password to allow this."  
   const char\* prompt_c = nullptr;  
   size_t prompt_length = 0;  
+  std::string prompt_string;  
   if (prompt) {  
-    std::string prompt_string = SysCFStringRefToUTF8(prompt);  
+    prompt_string = SysCFStringRefToUTF8(prompt);  
     prompt_c = prompt_string.c_str();  
     prompt_length = prompt_string.length();  
   }  

```

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.5897.3 \*\*Channel: \*\* Dev

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 461 B)
- [change.txt](attachments/change.txt) (text/plain, 3.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 22.0 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 613 B)
- [video.mov](attachments/video.mov) (video/quicktime, 3.3 MB)

## Timeline

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### fl...@google.com (2023-07-24)

Hello!  Thank you very much for the detailed explanation, PoC, and ASAN stacktrace.

Setting provisional severity HIGH b/c memory corruption in the browser process triggered via seems looks like a pretty plausible/standard user interaction (storing a password in the browser).

avi@, assigning to you since it looks like you've touched this area of the code most recently—feel free to reassign if you're not the right person for this.

Couldn't find a component for the Mac flow specifically so using UI>Browser>Passwords for now.

[Monorail components: UI>Browser>Passwords]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### ad...@google.com (2023-07-24)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-07-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cadb19a0afd329034f262bacb68ca02b7ae7d414

commit cadb19a0afd329034f262bacb68ca02b7ae7d414
Author: Avi Drissman <avi@chromium.org>
Date: Tue Jul 25 20:46:27 2023

Fix lifetime issue

https://crrev.com/c/4633989 fixed an issue where a null string would
crash. However, while creating a null-check, it moved a string
variable inside the null-checked block, causing a dangling pointer.

This moves the ownership of the string outside the null-checked block,
resolving the issue.

Fixed: 1467157
Change-Id: I9dca147a2b6feaf91a3bbf856905f7dc7fe43d63
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4717185
Commit-Queue: Mark Mentovai <mark@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Mark Mentovai <mark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1175061}

[modify] https://crrev.com/cadb19a0afd329034f262bacb68ca02b7ae7d414/base/mac/authorization_util.mm


### av...@chromium.org (2023-07-25)

Fixed in 117, broken in 117, so I don’t think merges are necessary.

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-31)

While the CL this issue bisects to was landed on 117, that fix was merged to 116 -- as such this issue impact 116/Beta, updating labels accordingly 

### am...@chromium.org (2023-07-31)

I'm going to go ahead and get ahead of the bot here and approve this fix for merge to M116 beta since it was landed almost a week ago and fix is fairly trivial (also canary and dev data look a-okay) 

### am...@chromium.org (2023-07-31)

I should have also added to please merge this fix to branch 5845 at your earliest convenience -- ty! 

### wf...@chromium.org (2023-08-02)

[vrp panel] it seems the string here that is used after being freed is passed to a safe API to eventually do the utf8 conversion, and it doesn't seem like this could result in code execution, but instead just data disclosure (e.g. ASLR defect via pointer disclosure).

### [Deleted User] (2023-08-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/98ee9a58da08baa3d8408745cd64f8a34d64107c

commit 98ee9a58da08baa3d8408745cd64f8a34d64107c
Author: Avi Drissman <avi@chromium.org>
Date: Wed Aug 09 20:07:43 2023

Fix lifetime issue

https://crrev.com/c/4633989 fixed an issue where a null string would
crash. However, while creating a null-check, it moved a string
variable inside the null-checked block, causing a dangling pointer.

This moves the ownership of the string outside the null-checked block,
resolving the issue.

(cherry picked from commit cadb19a0afd329034f262bacb68ca02b7ae7d414)

Fixed: 1467157
Change-Id: I9dca147a2b6feaf91a3bbf856905f7dc7fe43d63
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4717185
Commit-Queue: Mark Mentovai <mark@chromium.org>
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Mark Mentovai <mark@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1175061}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4765614
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Daniel Yip <danielyip@google.com>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Daniel Yip <danielyip@google.com>
Cr-Commit-Position: refs/branch-heads/5845@{#1319}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/98ee9a58da08baa3d8408745cd64f8a34d64107c/base/mac/authorization_util.mm


### am...@chromium.org (2023-08-09)

Thank you for the report. It does not appear that this issue would allow for attacker control to result in code execution and would result in an information leak.This report reported was also submitted within 24 hours of the change that introduced this issue and based on how this issue is triggered, we are fairly certain it would have been identified before impacting Stable channel users. Based on this, the VRP Panel has decided to decline a reward for this issue at this time. 

### me...@gmail.com (2023-08-10)

Hi Amy, I submit this issue after one month it is introduced… why you said “within 24h”? And this issue affects the dev channel, as I said in my report.

### me...@gmail.com (2023-08-10)

And info leak is not acceptable by VRP now?

### am...@chromium.org (2023-08-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-10)

Congratulations, Krace! The VRP Panel has decided to award you $2,000 for this information leak bug + $1,000 bisect bonus. Apologies for the original assessment as 0 based on a newly introduced commit. Each one of us on the panel misidentified the bisect commit as being introduced the day before your report, not a month before. Thanks for pointing that out, your efforts, and also reporting this issue to us! 

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1467157?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067948)*
