# Security:  Permission bypass due to not erase request  properly

| Field | Value |
|-------|-------|
| **Issue ID** | [40063511](https://issues.chromium.org/issues/40063511) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2023-03-10 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

In function `PermissionRequestManager::ValidateRequest`, if the request is invalid and `should_finalize` is set, the request will be finalized and removed from validated\_requests\_set\_ and request\_sources\_map\_ [1]. However, this request may still exist in the map duplicate\_requests\_, which is an unordered\_multimap containing raw pointers point to the request objects [2]. This does not cause memory safety issues, because the request being deleted was inserted into duplicate\_requests\_ as a key, and the key would nerver be dereferenced. But leaving the dangling pointer in duplicate\_requests\_ may result in permission check bypass. Consider the following scenario:

1. There is a key-value pair <Request\* a, Request\* a\_dup> in duplicate\_requests\_, and |Request a| has been deleted.
2. The attacker queries another permission, which constructs a new instance of Request, let's say, |Request b|.
3. The new |Request b| may reoccupy the memory freed by |Request a|, and if |Request b| is accepted, the function `PermissionRequestManager::RequestFinishedIncludingDuplicates` will search and finish all requests that were duplicated against |Request b| [3]. Because |Request b| has the same memory address as |Request a|, it will find the wrong |Request a\_dup| and grant the permission as well.

By exploiting this bug, a malicious website can silently gain access to sensitive permissions such as camera and microphone.

```
bool PermissionRequestManager::ValidateRequest(PermissionRequest\* request,  
                                               bool should_finalize) {  
  // skip  
  if (should_finalize) {    // ===> [1]  
    request->Cancelled();  
    request->RequestFinished();  
    validated_requests_set_.erase(request);  
    request_sources_map_.erase(request);  
  }  
  return false;  
}  
  
void PermissionRequestManager::RequestFinishedIncludingDuplicates(  
    PermissionRequest\* request) {  
  // skip  
  // Beyond this point, |request| has probably been deleted.  
  auto range = duplicate_requests_.equal_range(request);  
  for (auto it = range.first; it != range.second; ++it)  
    it->second->RequestFinished();    // ===> [3]  
  // Additionally, we can now remove the duplicates.  
  duplicate_requests_.erase(request);  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.cc;l=361;drc=dd597022c93047e88f6ddb812eb04ed392222b33>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.h;l=398;drc=dd597022c93047e88f6ddb812eb04ed392222b33>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.cc;l=1089;drc=dd597022c93047e88f6ddb812eb04ed392222b33>

**VERSION**  

Chrome Version: 111.0.5563.65 (stable) + dev

**REPRODUCTION CASE**  

It's a bit difficult to reproduce stably because it needs to accurately reoccupy a certain memory that has been released. The attached poc takes a rough approach to manipulate heap layout and it took quite a few runs to succeed on my local machine.

1. python3 -m http.server 8000
2. chrome.exe --user-data-dir=<xxx> and navigate to localhost:8000/poc.html
3. allow the second permission request prompt, check the permissions the site has, if succeed, the site would be granted MIDI permission silently

Fix Suggestion

Remove the duplicates when finalizing request.

diff --git a/components/permissions/permission\_request\_manager.cc b/components/permissions/permission\_request\_manager.cc  

index 59c679344065e..e610bca04b657 100644  

--- a/components/permissions/permission\_request\_manager.cc  

+++ b/components/permissions/permission\_request\_manager.cc  

@@ -363,6 +363,7 @@ bool PermissionRequestManager::ValidateRequest(PermissionRequest\* request,  

request->RequestFinished();  

validated\_requests\_set\_.erase(request);  

request\_sources\_map\_.erase(request);

- duplicate\_requests\_.erase(request);  
  
  }

return false;

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### jt...@gmail.com (2023-03-10)

[Comment Deleted]

### jt...@gmail.com (2023-03-10)

[Comment Deleted]

### ma...@chromium.org (2023-03-10)

Assigning based on recent changes in that area.
If you can, please provide a comment about when this issue may have been introduced or which active release branches of Chrome may be impacted. 
This information is critical so that we can ensure fixes are released urgently to help protect against n-day exploitation of newly landed security fixes, and so that we can avoid release of security regressions.


[Monorail components: UI>Browser>Permissions>Prompts]

### ma...@chromium.org (2023-03-10)

Setting medium severity as this can be used to get apparently arbitrary permissions that could for example, allow exposure of sensitive user information that an attacker can exfiltrate. It does require accepting a different permission prompt, but as that can apparently be another arbitrary permission, that's not a high bar. 

### jt...@gmail.com (2023-03-11)

[Comment Deleted]

### jt...@gmail.com (2023-03-11)

Re https://crbug.com/chromium/1423304#c4 > please provide a comment about when this issue may have been introduced

I think this issue was introduced in https://chromium.googlesource.com/chromium/src/+/5bd9b87658ea5ca9ffdae2239938cbbc555eff28, which added the function ValidateRequest.

### tu...@chromium.org (2023-03-13)

I traced down the code flow and determined that the function did not change the logic of the duplicated Request*.

>If you can, please provide a comment about when this issue may have been introduced or which active release branches of Chrome may be impacted. 
This information is critical so that we can ensure fixes are released urgently to help protect against n-day exploitation of newly landed security fixes, and so that we can avoid release of security regressions.

Unfortunately, I could reproduce the issue with Chrome 108.0.5357.1, before ValidateRequest was introduced, it means, the dangling pointer was existing for a while. I could not give an exact bisect number of active release branches might be impacted, but definitely < 108 (indeed it was really hard and took me quite a bit to reproduce)

### en...@chromium.org (2023-03-13)

Setting M108 as the regressed version, under the assumption that no channels are distributing a version earlier than that.

### [Deleted User] (2023-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-03-21)

That's anti-common-pattern to store the raw pointer as key of map, which might lead to logic corruptions (or bypass security controls). I could not simply remove the key from map as suggestion, due to the the complexity of renderframehost lifecycle (some RFH would be invalid due to nest-iframe-navigation)

I think we should go backward to use pair<type, GURL> as a key, and value as pointer, but make sure we will do some mitigations mentioned here
https://docs.google.com/document/d/1ygDQnRims35yAty2cExi0IdlWN6qlJm0JwvpTu8wrG4/edit#heading=h.8ubvleamtau8
It might require some refactoring works.



### tu...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-03-22)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-03-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f1ff7304338085a1e9b42dfd4f5df8baef69c36

commit 9f1ff7304338085a1e9b42dfd4f5df8baef69c36
Author: Thomas Nguyen <tungnh@google.com>
Date: Thu Mar 30 12:23:35 2023

Use weak pointer to store duplicate requests

Bug: 1423304
Change-Id: I7ab170f085c3d05c582f7065b88c1ad2510cc633
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4365724
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1124133}

[modify] https://crrev.com/9f1ff7304338085a1e9b42dfd4f5df8baef69c36/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/9f1ff7304338085a1e9b42dfd4f5df8baef69c36/components/permissions/permission_request_manager.h
[modify] https://crrev.com/9f1ff7304338085a1e9b42dfd4f5df8baef69c36/components/permissions/permission_request.cc
[modify] https://crrev.com/9f1ff7304338085a1e9b42dfd4f5df8baef69c36/components/permissions/permission_request_manager_unittest.cc
[modify] https://crrev.com/9f1ff7304338085a1e9b42dfd4f5df8baef69c36/components/permissions/permission_request.h


### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-03)

[Comment Deleted]

### tu...@chromium.org (2023-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-03)

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b213ffb9afd5d59e4b664645db4acdee15872e0

commit 8b213ffb9afd5d59e4b664645db4acdee15872e0
Author: Thomas Nguyen <tungnh@google.com>
Date: Mon Apr 03 12:37:41 2023

Use weak pointer to store duplicate requests

(cherry picked from commit 9f1ff7304338085a1e9b42dfd4f5df8baef69c36)

Bug: 1423304
Change-Id: I7ab170f085c3d05c582f7065b88c1ad2510cc633
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4365724
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1124133}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4394523
Reviewed-by: Thomas Nguyen <tungnh@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5672@{#199}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/8b213ffb9afd5d59e4b664645db4acdee15872e0/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/8b213ffb9afd5d59e4b664645db4acdee15872e0/components/permissions/permission_request_manager.h
[modify] https://crrev.com/8b213ffb9afd5d59e4b664645db4acdee15872e0/components/permissions/permission_request.cc
[modify] https://crrev.com/8b213ffb9afd5d59e4b664645db4acdee15872e0/components/permissions/permission_request_manager_unittest.cc
[modify] https://crrev.com/8b213ffb9afd5d59e4b664645db4acdee15872e0/components/permissions/permission_request.h


### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations on another one, Rong! The VRP Panel has decided to award you $7,500 for this report. This is a higher reward amount than we would generally extend for a bug of this type and class, however, we felt that the impact and that it did not require a compromised renderer warranted a higher reward. Additionally, we were impressed by the cleverness of this bug. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### jt...@gmail.com (2023-04-14)

> c#26:
Thanks for your kind words and confirmation, cheers!

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1423304?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1420625]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063511)*
