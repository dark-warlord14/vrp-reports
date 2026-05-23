# Security: UAF in It2MeNativeMessagingHostLacros::OnSupportSessionStarted

| Field | Value |
|-------|-------|
| **Issue ID** | [40068868](https://issues.chromium.org/issues/40068868) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-06 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/2842583> commited at Jun 04, 2021

At the end of `It2MeNativeMessagingHostLacros::ProcessConnect`, the this pointer is  

bound in the Mojo callback. The callback will be called asynchronously.[1]

```
void It2MeNativeMessagingHostLacros::ProcessConnect(int message_id,  
                                                    base::Value::Dict message) {  
  // ......  
  
  auto\* lacros_service = chromeos::LacrosService::Get();  
  lacros_service->GetRemote<crosapi::mojom::Remoting>()->StartSupportSession(  
      std::move(session_params),  
      base::BindOnce(&It2MeNativeMessagingHostLacros::OnSupportSessionStarted,  
                     base::Unretained(this)));   // <-- this pointer is bound in the callback  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:remoting/host/it2me/it2me_native_messaging_host_lacros.cc;l=367-411;drc=5006fdd60301674cf49f16b9ce76d65c603c31f4>

In the `It2MeNativeMessagingHostLacros::OnMessage` function, if it receives an  

invalid message, client\_->CloseChannel() is executed, which will eventually  

delete this.

```
void It2MeNativeMessagingHostLacros::OnMessage(const std::string& message) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  std::string type;  
  base::Value::Dict contents;  
  if (!ParseNativeMessageJson(message, type, contents)) {  
    client_->CloseChannel(std::string());   // <--- this will be deleted.  
    return;  
  }  
  
  // ...  
}  

```

So when the callback is executed, a Use-After-Free (UAF) issue will occur.

```
void It2MeNativeMessagingHostLacros::OnSupportSessionStarted(  
    mojom::StartSupportSessionResponsePtr mojo_response) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  int response_id = connect_response_id_;  <--- UAF here  
  connect_response_id_ = kInvalidMessageId;  
  
  
  // ...  
}  

```

**VERSION**  

Chrome Version: 93 stable  

Operating System: Lacros

**REPRODUCTION CASE**

1. Run lacros
2. Go to chrome://extensions page, load attached extension

My Lacros build args.gn

```
chromeos_is_browser_only=true  
target_os="chromeos"  
is_component_build=true  
is_asan=true  
is_debug=false  
dcheck_always_on=false  

```

See attached file for a video PoC.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see attached remoting.asan

**CREDIT INFORMATION**  

Reporter credit: ChaobinZhang

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 2.2 KB)
- [bg.js](attachments/bg.js) (text/plain, 525 B)
- [remoting.asan](attachments/remoting.asan) (text/plain, 24.7 KB)
- [remoting-poc.mp4](attachments/remoting-poc.mp4) (video/mp4, 8.5 MB)
- remoting-poc-2.mp4 (video/mp4, 6.5 MB)

## Timeline

### [Deleted User] (2023-08-06)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-08-06)

I have created a CL that I believe could fix this problem as well. https://chromium-review.googlesource.com/c/chromium/src/+/4755684

### ch...@google.com (2023-08-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/294762255). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/294762255]

### gi...@appspot.gserviceaccount.com (2023-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61623b6eb7b39742e7e1a0fb152d40f47149d508

commit 61623b6eb7b39742e7e1a0fb152d40f47149d508
Author: ChaobinZhang <zhchbin@gmail.com>
Date: Tue Aug 08 14:38:35 2023

Use weak pointer in support session started callback.

The use of base::Unretained here is not obviously safe, considering
that the Mojo callback is executed asynchronously. This change uses
a weak pointer instead to prevent UaF issues after the instance of
It2MeNativeMessagingHostLacros is freed.

Bug: 1470553, b/294762255
Change-Id: If6b9221dc2c52eeb5f6191c49adaa4c0787c13e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4755684
Commit-Queue: Joe Downing <joedow@chromium.org>
Reviewed-by: Joe Downing <joedow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1180898}

[modify] https://crrev.com/61623b6eb7b39742e7e1a0fb152d40f47149d508/remoting/host/it2me/it2me_native_messaging_host_lacros.cc


### ch...@google.com (2023-08-10)

Project: chromium/src
Branch: main

commit 61623b6eb7b39742e7e1a0fb152d40f47149d508
Author: ChaobinZhang <zhchbin@gmail.com>
Date:   Tue Aug 08 14:38:35 2023

    Use weak pointer in support session started callback.
   
    The use of base::Unretained here is not obviously safe, considering
    that the Mojo callback is executed asynchronously. This change uses
    a weak pointer instead to prevent UaF issues after the instance of
    It2MeNativeMessagingHostLacros is freed.
   
    Bug: 1470553, b/294762255
    Change-Id: If6b9221dc2c52eeb5f6191c49adaa4c0787c13e4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4755684
    Commit-Queue: Joe Downing <joedow@chromium.org>
    Reviewed-by: Joe Downing <joedow@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1180898}

M       remoting/host/it2me/it2me_native_messaging_host_lacros.cc

https://chromium-review.googlesource.com/4755684
16:40
16:40
CLs: Merged:​<none>      crrev/c/4755684
CLs: Pending:​crrev/c/4755684      <none>

### [Deleted User] (2023-08-10)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-08-16)

Perhaps we could consider this as fixed?

### zh...@gmail.com (2023-08-20)

I have found that this issue may also be accessible via the web. It can be triggered by remote content from the following domains when Chrome Remote Desktop (https://chrome.google.com/webstore/detail/chrome-remote-desktop/inomeogfingihgjfjlpeplalcfajhgai) is installed. The web store indicates that this extension has over 10,000,000 users.

```
"https://remotedesktop.corp.google.com/*", "https://remotedesktop.google.com/*", "https://remotedesktop-dev.corp.google.com/*", "https://remotedesktop-autopush.corp.google.com/*", "https://remotedesktop-daily-0.corp.google.com/*", "https://remotedesktop-daily-1.corp.google.com/*", "https://remotedesktop-daily-2.corp.google.com/*", "https://remotedesktop-daily-3.corp.google.com/*", "https://remotedesktop-daily-4.corp.google.com/*", "https://remotedesktop-daily-5.corp.google.com/*", "https://remotedesktop-daily-6.corp.google.com/*", "https://remotesupport.corp.google.com/*", "https://remotesupport-dev.corp.google.com/*", "https://remotesupport-autopush.corp.google.com/*", "https://remotesupport-daily-0.corp.google.com/*", "https://remotesupport-daily-1.corp.google.com/*", "https://remotesupport-daily-2.corp.google.com/*", "https://remotesupport-daily-3.corp.google.com/*", "https://remotesupport-daily-4.corp.google.com/*", "https://remotesupport-daily-5.corp.google.com/*", "https://remotesupport-daily-6.corp.google.com/*", "https://remoting.sandbox.google.com/*", "https://remoting-autopush.sandbox.google.com/*", "https://remoting-daily-0.sandbox.google.com/*", "https://remoting-daily-1.sandbox.google.com/*", "https://remoting-daily-2.sandbox.google.com/*", "https://remoting-daily-3.sandbox.google.com/*", "https://remoting-daily-4.sandbox.google.com/*", "https://remoting-daily-5.sandbox.google.com/*", "https://remoting-daily-6.sandbox.google.com/*" 
```

REPRODUCTION CASE
1. Run lacros with Chrome Remote Desktop installed
2. Go the https://remotedesktop.google.com/, run following code 

```
const hostName = "com.google.chrome.remote_assistance";
port = chrome.runtime.connect("inomeogfingihgjfjlpeplalcfajhgai", {name: hostName});

port.postMessage({
  type: 'connect',
  userName: 'zhchbin',
  authServiceWithToken: 'zhchbin-token'
});
port.postMessage({
  text: 'hello uaf'
});
```

### ke...@chromium.org (2023-09-06)

Adding some Chrome OS security people explicitly. I think this bug just needs to be properly flagged and then closed. See https://crbug.com/chromium/1470553#c6.

### ja...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### st...@google.com (2023-09-07)

Marking this as fixed as it has been resolved in the companion bug on buganizer. 

### [Deleted User] (2023-09-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@google.com (2023-09-07)

[Empty comment from Monorail migration]

### st...@google.com (2023-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations Chaobin! The VRP Panel has decided to award you $10,000 for this mildly mitigated security bug -- mitigated by requiring an install of a malicious extension -- + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- great work! 

### zh...@gmail.com (2023-09-14)

Thank you very much! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-15)

This issue was migrated from crbug.com/chromium/1470553?no_tracker_redirect=1

[Monorail blocking: b/294762255]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068868)*
