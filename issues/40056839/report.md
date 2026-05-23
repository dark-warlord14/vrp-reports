# Security: heap-use-after-free in in download::NetworkStatusListenerImpl::OnNetworkStatusReady

| Field | Value |
|-------|-------|
| **Issue ID** | [40056839](https://issues.chromium.org/issues/40056839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | yu...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2021-08-10 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

This issue import by <https://chromium-review.googlesource.com/c/chromium/src/+/3036233>.

When chrome startup, it associate a download service instance as keyed service and register self as a observer in NetworkStatusListener.  

<https://source.chromium.org/chromium/chromium/src/+/main:components/download/network/network_status_listener.h;drc=f0831f26cd194c819e0f3aa5920fdd88c8d2380e;l=51>

When a task trigger OnNetworkStatusReady run after all keyed services destroyed, raw pointer |observer\_| to download service in download::NetworkStatusListenerImpl::OnNetworkStatusReady use after free.  

<https://source.chromium.org/chromium/chromium/src/+/main:components/download/network/network_status_listener_impl.cc;drc=4de6ea67c54d8ade8c12a53d9c7f1dc2ce37187e;l=49>

From asan log, maybe OnNetworkStatusReady event could be triggered by Mojo calls.

**VERSION**  

Chrome Version: asan-win32-release\_x64-907395  

Operating System: windows

**REPRODUCTION CASE**  

ASAN log attached. I am still investigating this issue and will submit PoC files soon.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: heap-use-after-free

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan of MoyunSec VLab

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 14.9 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 6.2 KB)
- [logs.txt](attachments/logs.txt) (text/plain, 45.5 KB)
- [record.mov](attachments/record.mov) (video/quicktime, 13.6 MB)

## Timeline

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-10)

Thanks for the report. CCing people from the CL referenced. I have not verified this issue yet. Hopefully there will be proof of concepts incoming soon, but in the meantime do we want to consider reverting 3036233 if it's introduced a UAF?

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-08-10)

I don't think reverting makes sense. The root cause is we don't use weak ptr in this class, which is not introduced in that CL. This is pretty easy to fix.

### yu...@gmail.com (2021-08-10)

hi, xingliu@, sorry for my bad anlysis which confuse you. 

According to the asan log, it is a WRITE of size 4 UaF, which is try to write |connection_type_| to a freed NetworkStatusListenerImpl object.
https://source.chromium.org/chromium/chromium/src/+/main:components/download/network/network_status_listener_impl.cc;drc=4de6ea67c54d8ade8c12a53d9c7f1dc2ce37187e;l=48

Maybe the cause is push a async OnNetworkStatusReady call to NetworkConnectionTracker and run after NetworkStatusListenerImpl was freed.
https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/network_connection_tracker.cc;drc=ce29454af324a1f7b72af4eeed3145c63f9405a9;l=83

This crash info was found in my fuzz system and I am still try to reproduce it.  But I am confused by why the network.mojom.NetworkChangeManagerClient can't bind to Mojo . Any info can help me? Thank you.

Sorry for my mistake again.

### xi...@chromium.org (2021-08-10)

Hi,  yuanvi.cn@, your report is very helpful.  Thanks for filing this.
 
When OnNetworkStatusReady is called, NetworkStatusListenerImpl could be freed. The actual calling is done in the base::OnceCallback, internally as a std::function or something. Chromium's callback code will check the weak ptr when the callback is called.  The weak ptr will be marked as invalid when the weak ptr factory is destroyed, this is the mechanism to fix this issue. I assume the NetworkConnectionTracker should handle the IPC correctly. 

### yu...@gmail.com (2021-08-10)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47f86d849d371cf25664130257bb243aeb6417d8

commit 47f86d849d371cf25664130257bb243aeb6417d8
Author: Xing Liu <xingliu@chromium.org>
Date: Tue Aug 10 22:37:53 2021

Background download: Use WeakPtr in NetworkStatusListenerImpl.

Use WeakPtr in NetworkStatusListenerImpl.

Bug: 1238268
Change-Id: I434c226151346e1a9405cb6a5a74cd04b064b5cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3086726
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#910524}

[modify] https://crrev.com/47f86d849d371cf25664130257bb243aeb6417d8/components/download/network/network_status_listener.h
[modify] https://crrev.com/47f86d849d371cf25664130257bb243aeb6417d8/components/download/network/network_status_listener_impl.cc
[modify] https://crrev.com/47f86d849d371cf25664130257bb243aeb6417d8/components/download/network/network_status_listener_impl.h


### xi...@chromium.org (2021-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### yu...@gmail.com (2021-08-11)

Thank you for the quick fix. The fix verified worked.

A simple poc submit as expect.

Similar to https://crbug.com/chromium/1197904, a NetworkChangeManagerClient::OnInitialConnectionType Mojo call can be recieved after all keyed service destoryed and run all callbacks in |connection_type_callbacks_|.
https://source.chromium.org/chromium/chromium/src/+/main:out/android-Debug/gen/services/network/public/mojom/network_change_manager.mojom.cc;drc=9d1ccebc2fa67f5a624835e692f3f27c7e60acae;l=164

I use a sync task instead of this Mojo call in patch file to reproduce stablely.

Reproduce step:
1. apply patch file and rebuild chrome 
2. open chrome and wait several seconds (DeviceStatusListener::StartAfterDelay call)
3. click close button

### [Deleted User] (2021-08-14)

Not requesting merge to dev (M94) because latest trunk commit (910524) appears to be prior to dev branch point (911515). If this is incorrect, please replace the Merge-na label with Merge-Request-94. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-19)

Congratulations, Wei Yuan! The VRP Panel has decided to award you $20,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for this report and nice find! 

### xi...@chromium.org (2021-08-19)

Hi, I'm curious how hacker can attack Chrome with invalidate pointer like this, can anyone do a brief introduction about how to use this bug?

### xi...@chromium.org (2021-08-19)

I'm also curious how we judge the importance of a security bug, can anyone provide more context?

### yu...@gmail.com (2021-08-19)

[Comment Deleted]

### am...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-20)

Hi xingliu@, when you say the importance of the a security bug, do you mean for security severity and triage? Or for VRP rewarding? 
For severity and triage, the Security Sheriffs, following https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/sheriff.md#step-2_assess-the-severity and assess the severity using these guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

Since this issue results in memory corruption via a user after free in the browser process which would allow for potential of arbitrary code execute in a browser process, it is a high severity issue. Browser process memory corruption issues are usually of Critical severity, however, it is bumped down to high severity due to it the mitigating factor of needing MojoJS to trigger. 

For VRP reward consideration, a bug report must meet the eligibility based on https://www.google.com/about/appsecurity/chrome-rewards/.

For reward determination each eligible report is judged individually based on the bug class and impact, report quality, details and effort provided by the researcher such as in root cause analysis, providing POCs, providing an exploit, and/or providing a patch. 
Happy to chat in more detail and I'm sure others are as well, but I wanted to cover some of your questions as I was working through my bug queue this evening. 


### xi...@chromium.org (2021-08-20)

Thanks for the details. 

There are quite some base::UnRetained usage in chromium(a few thousands?).  Not all of them, but definitely some percentage of the it can be categorized into use after free in unsandboxed process. 

### [Deleted User] (2021-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1238268?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056839)*
