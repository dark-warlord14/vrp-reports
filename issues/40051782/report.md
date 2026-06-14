# Security: UAF in InstalledAppProviderImpl (Desktop)

| Field | Value |
|-------|-------|
| **Issue ID** | [40051782](https://issues.chromium.org/issues/40051782) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>AppManifest |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tj...@theori.io |
| **Assignee** | su...@microsoft.com |
| **Created** | 2020-03-16 |
| **Bounty** | $25,000.00 |

## Description

**VULNERABILITY DETAILS**

InstalledAppProviderImpl is created with mojo::MakeSelfOwnedReceiver, and it holds a raw pointer to the RenderFrameHost without observing its lifetime.

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/installedapp/installed_app_provider_impl.cc;l=66;bpv=0;bpt=1>  

void InstalledAppProviderImpl::Create(  

RenderFrameHost\* host,  

mojo::PendingReceiver[blink::mojom::InstalledAppProvider](javascript:void(0);) receiver) {  

mojo::MakeSelfOwnedReceiver(std::make\_unique<InstalledAppProviderImpl>(host), // pass raw pointer  

std::move(receiver));  

}

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/installedapp/installed_app_provider_impl.cc;l=35;bpv=0;bpt=1>  

InstalledAppProviderImpl::InstalledAppProviderImpl(  

RenderFrameHost\* render\_frame\_host)  

: render\_frame\_host\_(render\_frame\_host) { // hold raw pointer  

DCHECK(render\_frame\_host\_);  

}

In InstalledAppProviderImpl::FilterInstalledApps, a virtual call is made on |render\_frame\_host\_|:

<https://source.chromium.org/chromium/chromium/src/+/master:content/browser/installedapp/installed_app_provider_impl.cc;l=49;bpv=0;bpt=1>  

bool is\_off\_the\_record =  

render\_frame\_host\_->GetProcess()->GetBrowserContext()->IsOffTheRecord();

If the RenderFrameHost is freed before FilterInstalledApps() is called, a virtual function call on a freed object occurs.

This could likely be triggered from regular JavaScript by repeatedly invoking |navigator.getInstalledRelatedApps| to clog the mojo message pipe and then racing the frame destruction, but Blink enforces the API can only be called from top-level frames, so this approach would be more difficult than usual.

However, a compromised renderer can easily trigger the UAF with no race needed. In the attached poc and exploit, the MojoJS and MojoJSTest bindings are used.

Note that as of <https://chromium.googlesource.com/chromium/src/+/d37dc2558a7c841c8439f0cae4dfa5807e56f61e> (which landed in 82.0.4065.0), this bug is only reachable on Windows with the InstalledAppProvider flag. However, the bug was introduced in <https://chromium.googlesource.com/chromium/src/+/0002875db334deb69d41f74adc15ad40089f04c5%5E%21/#F0> (which landed in 81.0.4041.0), where it is reachable by default on all desktop platforms. This means this bug will affect users on Chrome Stable version 81.

A working exploit for Chrome Beta 81.0.4044.69 on Windows x64 is included in the attachments.

Two possible patches are also included. One has InstalledAppProviderImpl inherit from WebContentsObserver to observe the render frame destruction and clear its reference. The other patch has InstalledAppProviderImpl store the (process\_id, frame\_id) pair in place of the raw pointer and perform dynamic lookup of the rfh.

**VERSION**  

Chrome Version: 81.0.4044.0+  

Operating System: Desktop

**REPRODUCTION CASE**

Attached as a zip because the MojoJS generated bindings are included. See poc.html for a minimal trigger and pwn.html for an exploit. The exploit appends --no-sandbox to the Browser process's command line object, causing all new subprocesses to run unsandboxed.

Instructions:  

Unzip gIRA.zip and serve from an HTTP server, e.g. on localhost port 8080.

PoC:  

Run chrome with --enable-blink-features=MojoJS,MojoJSTest and visit <http://localhost:8080/trigger.html>

Exploit:  

Run chrome beta (81.0.4044.69) with --enable-blink-features=MojoJS,MojoJSTest. Find base address of chrome.dll (e.g. using windbg) and replace the value of kChromeDllBase in pwn.html. (Note that this base address could be acquired from a compromised renderer). Then visit <http://localhost:8080/pwn.html>. After the exploit completes, open a new tab and check the process listing to confirm the subprocess is running with --no-sandbox.

**CREDIT INFORMATION**  

Reporter credit: Tim Becker of Theori

## Attachments

- [gIRA.zip](attachments/gIRA.zip) (application/octet-stream, 7.1 MB)
- [patch.diff](attachments/patch.diff) (text/plain, 3.2 KB)
- [patch2.diff](attachments/patch2.diff) (text/plain, 2.2 KB)

## Timeline

### tj...@theori.io (2020-03-16)

Adding attachments in comment because the attachment section of submission form was broken at the time of submission.

### ts...@chromium.org (2020-03-16)

[Empty comment from Monorail migration]

### pa...@google.com (2020-03-16)

Thanks for this good report!

+Adetaylor for your pattern-matching and data-gathering enjoyment.

### pa...@google.com (2020-03-16)

[Empty comment from Monorail migration]

### jo...@microsoft.com (2020-03-16)

[Empty comment from Monorail migration]

### jo...@microsoft.com (2020-03-16)

[Empty comment from Monorail migration]

### jo...@microsoft.com (2020-03-16)

I have pinged Sunggook on Teams and he's looking

### su...@microsoft.com (2020-03-17)

[Empty comment from Monorail migration]

### ne...@google.com (2020-03-17)

[Empty comment from Monorail migration]

### jo...@microsoft.com (2020-03-17)

[Empty comment from Monorail migration]

### jo...@microsoft.com (2020-03-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-03-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>AppManifest]

### su...@microsoft.com (2020-03-17)

There was a mitigation in 82 . The interim fix is to cherry-pick the below CL ((Tim agreed).

https://chromium.googlesource.com/chromium/src/+/d37dc2558a7c841c8439f0cae4dfa5807e56f61e


### [Deleted User] (2020-03-17)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@microsoft.com (2020-03-17)

				
1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge

This is a security bug and sent a mail to chrome-security@google.com, no reply yet.

- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
I can't access it.

2. Links to the CLs you are requesting to merge.
https://chromium.googlesource.com/chromium/src/+/d37dc2558a7c841c8439f0cae4dfa5807e56f61e

3. Has the change landed and been verified on master/ToT?
Yes, it is landed in 82 and verified.

4. Why are these changes required in this milestone after branch?
Here is an explanation from the Tim who filed a bug.

"This could likely be triggered from regular JavaScript by repeatedly invoking |navigator.getInstalledRelatedApps| to clog the mojo message pipe and then racing the frame destruction, but Blink enforces the API can only be called from top-level frames, so this approach would be more difficult than usual."

5. Is this a new feature?
Yes, it is new feature that is hidden by the flag initially, however the problematic code was added outside of the feature flag check.

6. If it is a new feature, is it behind a flag using finch?
Yes,  features::kInstalledAppProvider

problematic code was added outside of the feature flag check.: 

https://chromium.googlesource.com/chromium/src/+/0002875db334deb69d41f74adc15ad40089f04c5

### ad...@google.com (2020-03-18)

Approving merge to M81, branch 4044. Please merge.

### [Deleted User] (2020-03-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0c0bee9953f5e99dc690bef04391c67e4c146e93

commit 0c0bee9953f5e99dc690bef04391c67e4c146e93
Author: Sunggook Chue <sunggch@microsoft.com>
Date: Wed Mar 18 23:52:08 2020

Issue is invalid address access when render frame host was deleted in the middle of gIRA API call.

The changes are
- gIRA register WebContentOberser for render frame host deletion.
- In frame host deletion callback, it nullify member variable of frame host pointer.
- Render frame host pointer check is made before referencing it.

Bug: https://bugs.chromium.org/p/chromium/issues/detail?id=1062091
Change-Id: I7bc261a292b63c8e60865916315b3dea59130c4b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2107618
Commit-Queue: Sunggook Chue <sunggch@microsoft.com>
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/master@{#751516}

[modify] https://crrev.com/0c0bee9953f5e99dc690bef04391c67e4c146e93/content/browser/installedapp/installed_app_provider_impl.cc
[modify] https://crrev.com/0c0bee9953f5e99dc690bef04391c67e4c146e93/content/browser/installedapp/installed_app_provider_impl.h
[modify] https://crrev.com/0c0bee9953f5e99dc690bef04391c67e4c146e93/content/browser/installedapp/installed_app_provider_impl_win.cc
[modify] https://crrev.com/0c0bee9953f5e99dc690bef04391c67e4c146e93/content/browser/installedapp/installed_app_provider_impl_win.h


### [Deleted User] (2020-03-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@microsoft.com (2020-03-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-23)

sunggch@microsoft.com - what happened in https://crbug.com/chromium/1062091#c22? If you have merged to M81 I'd expect to see bugdroid adding a comment with details, and it would replace the Merge-Approved label with Merge-Merged labels. But then again sometimes bugdroid gets it wrong. Do you believe you have merged to M81? If so, can you provide details of the commit?

### ra...@chromium.org (2020-03-24)

The merged CL: https://chromium-review.googlesource.com/c/chromium/src/+/2109213

Looks like it's linking to another bug

### ad...@chromium.org (2020-03-24)

rayankans@ - thank you. That doesn't look to me like the right thing was merged, so I think we still need to hear from sunggch@.

This is a critical severity issue, and there's supposed to be an M81 beta later this week. We typically block betas for critical severity security issues so I am marking this as ReleaseBlock-Beta. I expect a horde of angry release TPMs to start shouting at us now.

rayankans@ - I've e-mailed sunggch@ but obviously people's working hours are a bit weird in these virus-riddled times. If they don't respond, please can you take care of this? Either by merging the correct fix or by reverting/switching off the feature for M81. Let's give sunggch@ a day...

### ra...@chromium.org (2020-03-24)

Hi adetaylor@, that's the fix we decided on merging.

The security vulnerability is behind a disabled feature flag now, so it won't affect any users.

### ad...@chromium.org (2020-03-24)

Ah OK. Perfect. In which case I'm going to consider this fixed in M81, thanks!

### ad...@chromium.org (2020-03-24)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-26)

Congrats! The Panel decided to award $25,000 for this report! 

### na...@google.com (2020-03-26)

[Empty comment from Monorail migration]

### tj...@theori.io (2020-04-20)

Hi, we have prepared a blog post explaining this bug and exploit. Can this be published now that the fix has been shipped, or must we wait for the view restriction to lift? 

### ad...@chromium.org (2020-04-20)

Thank you for asking. Yes, please go ahead. As I understand it, this bug never reached users of the stable channel thanks to your prompt report. We'll be happy to remove view restrictions on this bug early as well if you like - let us know if so.

### tj...@theori.io (2020-04-20)

Great. We would like to link to the report in the post, so removing the view restriction as soon as it's feasible would be appreciated. Thanks!

### ad...@google.com (2020-04-20)

OK, opening it now. Thanks again for the great report!

### is...@google.com (2020-04-20)

This issue was migrated from crbug.com/chromium/1062091?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051782)*
