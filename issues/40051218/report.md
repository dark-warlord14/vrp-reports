# UAF in chrome!content::FrameTreeNode::~FrameTreeNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40051218](https://issues.chromium.org/issues/40051218) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Portals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@blackowlsec.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2020-01-13 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

Use-After-Free vulnerability in chrome!content::FrameTreeNode::~FrameTreeNode+0xff [c:\b\s\w\ir\cache\builder\src\content\browser\frame\_host\frame\_tree\_node.cc @ 162]. It affects the browser process.

For reproducing the case it is required to enable portals (chrome://flags/#enable-portals).

**VERSION**  

Chrome Version: Google Chrome stable 79.0.3945.117 (Official Build) (64-bit)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

Minimized test case together with windbg logs attached.

**CREDIT INFORMATION**  

Reporter credit: Pawel Wylecial of REDTEAM.PL

## Attachments

- [windbg_log.txt](attachments/windbg_log.txt) (text/plain, 6.1 KB)
- [cm_frametreenode.html](attachments/cm_frametreenode.html) (text/plain, 624 B)

## Timeline

### cl...@chromium.org (2020-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5082006012624896.

### cl...@chromium.org (2020-01-13)

Testcase 5082006012624896 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5082006012624896.

### cl...@chromium.org (2020-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5262082918383616.

### cl...@chromium.org (2020-01-14)

Testcase 5262082918383616 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5262082918383616.

### mb...@chromium.org (2020-01-14)

I'm able to reproduce this locally but not on ClusterFuzz.

adithyas: Could you please take a look or help find another owner for this?

[Monorail components: Blink>HTML>Portal]

### ad...@chromium.org (2020-01-14)

I was able to reproduce this too. Hitting a DCHECK in debug builds:

[200291:1:0114/102606.382824:FATAL:html_portal_element.cc(341)] Check failed: !portal_. This element should have previously dissociated in DisconnectContentFrame
#0 0x7f2bf104562f base::debug::CollectStackTrace()
#1 0x7f2bf0d6057d base::debug::StackTrace::StackTrace()
#2 0x7f2bf0d60538 base::debug::StackTrace::StackTrace()
#3 0x7f2bf0da629d logging::LogMessage::~LogMessage()
#4 0x7f2bcf8ffd25 blink::HTMLPortalElement::RemovedFrom()
#5 0x7f2bced3f643 blink::ContainerNode::NotifyNodeRemoved()
#6 0x7f2bced3e679 blink::ContainerNode::RemoveChild()
#7 0x7f2bced3c94f blink::CollectChildrenAndRemoveFromOldParent()
#8 0x7f2bced3c5e9 blink::ContainerNode::AppendChild()
#9 0x7f2bcef356cb blink::Node::appendChild()
#10 0x7f2bd0bb803b blink::node_v8_internal::AppendChildMethodForMainWorld()
#11 0x7f2bd0bb7c44 blink::V8Node::AppendChildMethodCallbackForMainWorld()
#12 0x7f2bc87dca70 v8::internal::FunctionCallbackArguments::Call()
#13 0x7f2bc87db193 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#14 0x7f2bc87d90da v8::internal::Builtin_Impl_HandleApiCall()
#15 0x7f2bc87d8bcf v8::internal::Builtin_HandleApiCall()
#16 0x7f2bc8301f9f Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit


### ad...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### pa...@blackowlsec.com (2020-02-12)

any updates on this issue ? I see it currently does no longer reproduce on latest stable.

### ad...@chromium.org (2020-02-24)

CL in review: https://crrev.com/c/2002859

### lf...@google.com (2020-02-24)

Re#9: This CL fixes the renderer DCHECK, but do we know what fixed the browser process UaF?


### lf...@chromium.org (2020-02-24)

I've bisected the fix, the UaF was fixed by 8d444465714a0257eaa26754c8d724488b8f0c39.

However, there's still a nullptr deref in the browser process that we should still fix (we also fail the DCHECK(portal_contents_.OwnsContents()) in Portal::CreateProxyAndAttachPortal).


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/762211521e4b395ac5980247f66e97ab44770e08

commit 762211521e4b395ac5980247f66e97ab44770e08
Author: Adithya Srinivasan <adithyas@chromium.org>
Date: Tue Feb 25 19:52:13 2020

Portals: Handle edge case with connecting child frames

We shouldn't set the portal element's content frame if
SubframeLoadingDisabler::CanLoadFrame() returns false, this can lead to
discrepancies in the connected subframe count and result in frames not
being disconnected.

In the test case in this CL, we try inserting a portal into a subtree
that is being disconnected.

Bug: 1041406
Change-Id: I7e0377392457f5b0ca6537c27cb6a5835b8eedd9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2002859
Commit-Queue: Adithya Srinivasan <adithyas@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#744350}

[modify] https://crrev.com/762211521e4b395ac5980247f66e97ab44770e08/third_party/blink/renderer/core/html/portal/html_portal_element.cc
[add] https://crrev.com/762211521e4b395ac5980247f66e97ab44770e08/third_party/blink/web_tests/wpt_internal/portals/portals-crbug-1041406.html


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cc2d4aa6d886e08ac187b29a422d8f124d85565a

commit cc2d4aa6d886e08ac187b29a422d8f124d85565a
Author: Adithya Srinivasan <adithyas@chromium.org>
Date: Wed Feb 26 01:21:25 2020

Portals: Check if portal contents is already attached

Check if CreateProxyAndAttachPortal is called on a portal that has
already been attached, and kill the renderer that sent the message if
so.

Bug: 1041406
Change-Id: Idea04773db777ee0591003810bbe30dcb8fa7586
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2072465
Reviewed-by: Lucas Gadani <lfg@chromium.org>
Commit-Queue: Adithya Srinivasan <adithyas@chromium.org>
Cr-Commit-Position: refs/heads/master@{#744484}

[modify] https://crrev.com/cc2d4aa6d886e08ac187b29a422d8f124d85565a/content/browser/portal/portal.cc
[modify] https://crrev.com/cc2d4aa6d886e08ac187b29a422d8f124d85565a/content/browser/portal/portal_browsertest.cc


### ad...@chromium.org (2020-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-26)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-02)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-05)

CONGRATS! The Panel decided to award $20,000 for this report! 

### na...@google.com (2020-03-05)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-06)

[Empty comment from Monorail migration]

### mm...@google.com (2020-03-06)

adithyas@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@google.com (2020-03-10)

adithyas@, friendly ping re c#21.

### ad...@chromium.org (2020-03-10)

#22: Done!

### mm...@google.com (2020-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### is...@google.com (2020-10-12)

This issue was migrated from crbug.com/chromium/1041406?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051218)*
