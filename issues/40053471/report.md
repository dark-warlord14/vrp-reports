# Security: UAF in PasswordGenerationPopupControllerImpl::PasswordAccepted

| Field | Value |
|-------|-------|
| **Issue ID** | [40053471](https://issues.chromium.org/issues/40053471) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Passwords>Generation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ka...@google.com |
| **Created** | 2020-09-30 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36

Steps to reproduce the problem:
VULNERABILITY DETAILS

From
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc;l=197;drc=380e3015e4c2b25e1e1faaa727c64a8d09c1e457

```
void PasswordGenerationPopupControllerImpl::PasswordAccepted() {
  if (state_ != kOfferGeneration)
    return;

  base::WeakPtr<PasswordGenerationPopupControllerImpl> weak_this = GetWeakPtr();
  driver_->GeneratedPasswordAccepted(form_data_, generation_element_id_,
                                     current_password_);        // =====> [1]
  // |this| can be destroyed here because GeneratedPasswordAccepted pops up
  // another UI and generates some event to close the dropdown.
  if (weak_this)
    weak_this->HideImpl();
}
```

In function PasswordGenerationPopupControllerImpl::PasswordAccepted, there is a virtual function call on {driver_} without any null-test [1]. This may cause UAF if {driver_} (ContentPasswordManagerDriver) has been freed before calling `PasswordAccepted`.

ContentPasswordManagerDriver is created in function `ContentPasswordManagerDriverFactory::GetDriverForFrame`, and its lifetime is bound to RenderFrameHost. When a RenderFrame is deleted, `ContentPasswordManagerDriverFactory::RenderFrameDeleted` will be called which will erase corresponding ContentPasswordManagerDriver in {frame_driver_map_} [2].

```
void ContentPasswordManagerDriverFactory::RenderFrameDeleted(
    content::RenderFrameHost* render_frame_host) {
  frame_driver_map_.erase(render_frame_host);   // =====> [2]
}
```

Under normal circumstances, when RenderFrame being deleted, the renderer would inform the browser that the generation element lost focus [3], so the browser will hide the generation popup view, and there will be no chance to call GeneratedPasswordAccepted after that. But a compromised renderer can choose not to send the message, which result in UAF when user click the password suggestion view.

```
void PasswordGenerationAgent::DidEndTextFieldEditing(
    const blink::WebInputElement& element) {
  if (!element.IsNull() && current_generation_item_ &&
      element == current_generation_item_->generation_element_) {
    GetPasswordGenerationDriver()->GenerationElementLostFocus();   // =====> [3]
    current_generation_item_->generation_element_.SetShouldRevealPassword(
        false);
  }
}
```

VERSION
Chrome Version: 85.0.4183.121 (stable)

REPRODUCTION CASE

Note:
1. In order to enable the password generation feature you need to turn on Chrome Sync, this may cause inconvenience if you run poc on asan builds of chromium. Another option is to force PasswordGenerationFrameHelper::IsGenerationEnabled to return true. (See patch.diff for details)

2. The poc requires several click, but only one click accepting the suggestion password is really needed if the renderer is already compromised. The approach to steal a user's click has alreay been described in this issue [https://bugs.chromium.org/p/chromium/issues/detail?id=1027152].

Steps to reproduce:
1. Apply the patch.diff

2. Setup a HTTPServer
python -m SimpleHTTPServer

3. Run asan build chrome
./chrome http://localhost:8000/poc.html

I only tested the poc on chrome version 87.0.4259.1, but it should work on other versions.

What is the expected behavior?
Not crash.

What went wrong?
UAF occurred.

Did this work before? N/A 

Chrome version: 85.0.4183.121  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 972 B)
- [patch.diff](attachments/patch.diff) (text/plain, 2.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.5 KB)

## Timeline

### do...@chromium.org (2020-09-30)

Thanks for the report.

+password generation folks. It looks like |driver_| should be null tested prior to it being used.

Assigning High severity (UaF in browser process), but needs a compromised renderer and user assistance to exploit. The need for user assistance probably puts this at the lower end of High/upper end of Medium Severity. Impact is on stable branch.

[Monorail components: UI>Browser>Passwords>Generation]

### jt...@gmail.com (2020-09-30)

Here is the asan log for your convenience.

### ka...@google.com (2020-09-30)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### ba...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-09-30)

Thanks for the summary dominickn@. I can confirm that the poc indeed results in dereferencing a null driver, however I fail to see how this can be exploited. Wouldn't we hit a SIGSEGV regardless? If this was exploitable, wouldn't we have to null-check every weak pointer dereference in Chromium code?

### [Deleted User] (2020-09-30)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2020-10-01)

#7: the ASAN log in #2[1] indicates a use-after-free on an actual address as opposed to a null pointer deref (I'm pretty sure ASAN is able to distinguish between the two). Given that user input is involved here, perhaps that indicates there is a race between when the weak pointer is being cleared and when the user input is processed and event handled in PasswordGenerationPopupControllerImpl.

1. https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=469109

### jd...@chromium.org (2020-10-01)

I looked into this a bit more today, here's what I found:

* `driver_.get()` is definitely null, so I don't think this code is racy.
* However, similarly to the reporter I do get a heap-use-after-free on an actual address in ASAN builds. This address matches `driver_.get()` when it was constructed. I'm not super sure why this happens, but I suspect this is some compiler optimization. Dereferencing a nullptr is undefined behaviour, and thus compilers are within their rights to assume `driver_` is never null when it is dereferenced. That could explain the read at 0x6150001a4828 in the report, since the compiler likely needs to copy the address of the driver on the stack so that it's available in the GeneratedPasswordAccepted member function call.
* In release builds (i.e. no ASAN) Chrome then attempts to invoke GeneratedPasswordAccepted, which sometimes (not always!) results in a SIGSEGV:

Received signal 11 SEGV_MAPERR 000000000038
#0 0x7fb4bc421e49 base::debug::CollectStackTrace()
#1 0x7fb4bc371a33 base::debug::StackTrace::StackTrace()
#2 0x7fb4bc4219eb base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7fb4af8c3140 (/usr/lib/x86_64-linux-gnu/libpthread-2.31.so+0x1413f)
#4 0x55d82a50cca3 PasswordGenerationPopupControllerImpl::PasswordAccepted()

We know have a CL in flight that performs `CHECK(driver_);`, and thus would reliably cause a crash: https://crrev.com/c/2440095

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2726c1afa88d130f3f8b9ec4e03c774f06af07a1

commit 2726c1afa88d130f3f8b9ec4e03c774f06af07a1
Author: Maria Kazinova <kazinova@google.com>
Date: Thu Oct 01 15:09:00 2020

Adding a driver check in PasswordGenerationPopupControllerImpl::
PasswordAccepted.

Having this check ensures there is no nullptr dereference in case the
driver is deleted and the browser process is not aware of it (i.e.
in case when the renderer is compromised).

Bug: 1133635
Change-Id: Ieee8c2200a4b323af39f730011e733b74e8bc911
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2440095
Commit-Queue: Maria Kazinova <kazinova@google.com>
Reviewed-by: Jan Wilken Dörrie <jdoerrie@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#812695}

[modify] https://crrev.com/2726c1afa88d130f3f8b9ec4e03c774f06af07a1/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc


### ka...@google.com (2020-10-01)

I would like to request a merge of #11 to M86.

As I could see from other bugs, there are no further M85 releases planned, so I shouldn't merge to M85, but please correct me if I'm wrong, thanks!

### [Deleted User] (2020-10-01)

This bug requires manual review: We are only 4 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@google.com (2020-10-01)

+adetaylor@ for M86 merge review.

Note: CL listed at #11 is not in canary yet.

### ka...@google.com (2020-10-01)

1. Does your merge fit within the Merge Decision Guidelines?
Yes, it's a fix for a security issue.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2440095

3. Has the change landed and been verified on ToT?
Yes. It hasn't been verified on Canary, but I'm requesting the merge in advance to save time. 

4. Does this change need to be merged into other active release branches (M-1, M+1)?
M+1 yes.

5. Why are these changes required in this milestone after branch?
Because the issue was discovered after BP.

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N\A

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### ko...@google.com (2020-10-07)

Sending a quick ping.

### ad...@chromium.org (2020-10-08)

Thanks for the ping. This was too late for the initial M86 release so I will approve a bunch of merges into the first scheduled M86 security refresh once we are sure we don't need any emergency M86 respins. This will probably be one of them.

Meanwhile, please mark as fixed if it's fixed! Thanks!

### jd...@chromium.org (2020-10-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-12)

Approving merge to M86, assuming no problems have shown up in Canary. Please merge to branch 4240.


### go...@google.com (2020-10-12)

Please merge your change to M86 branch 4240 now so it can be included in this week M86 respin for Android. Thank you.

### [Deleted User] (2020-10-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/20f66bb1619edbd12e72c0bd1f1c001890bad160

commit 20f66bb1619edbd12e72c0bd1f1c001890bad160
Author: Maria Kazinova <kazinova@google.com>
Date: Mon Oct 12 20:59:15 2020

Adding a driver check in PasswordGenerationPopupControllerImpl::
PasswordAccepted.

Having this check ensures there is no nullptr dereference in case the
driver is deleted and the browser process is not aware of it (i.e.
in case when the renderer is compromised).

(cherry picked from commit 2726c1afa88d130f3f8b9ec4e03c774f06af07a1)

Bug: 1133635
Change-Id: Ieee8c2200a4b323af39f730011e733b74e8bc911
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2440095
Commit-Queue: Maria Kazinova <kazinova@google.com>
Reviewed-by: Jan Wilken Dörrie <jdoerrie@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#812695}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2465773
Commit-Queue: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1219}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/20f66bb1619edbd12e72c0bd1f1c001890bad160/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc


### dc...@chromium.org (2020-10-13)

For merge this seems fine, but we shouldn't CHECK() in browser-side code for conditions that a renderer can trigger.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0c25f1ec6b4d380d76c4d901ac0da525e7e7f518

commit 0c25f1ec6b4d380d76c4d901ac0da525e7e7f518
Author: Jan Wilken Dörrie <jdoerrie@chromium.org>
Date: Tue Oct 13 12:34:54 2020

[Passwords] Handle null driver in generation popup gracefully

This change gracefully handles a null PasswordManagerDriver in
PasswordGenerationPopupControllerImpl::PasswordAccepted instead of
forcing a CHECK failure.

Bug: 1133635
Change-Id: Ife83a3c8c78b5dff18c3252c3beb0092750d4420
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2463834
Commit-Queue: Jan Wilken Dörrie <jdoerrie@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#816536}

[modify] https://crrev.com/0c25f1ec6b4d380d76c4d901ac0da525e7e7f518/chrome/browser/ui/passwords/password_generation_popup_controller_impl.cc


### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-21)

jtrrodant@gmail.com we discussed at length at the VRP panel. Null pointer dereferences are regarded as non-exploitable, and are not subject to a reward. It _appears_ that in this case the compiler is optimizing away some important checks which is why it's showing up as a UaF in an ASAN build.

However, we see no evidence that this sinister magic is achievable in a release build, so the provisional reward is 0. However, if you can reproduce a UaF in a release build we'll be happy to reconsider.

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### jt...@gmail.com (2020-11-10)

Hi adetaylor@,

Sorry for the delay.

I installed the official build of Chrome 86.0.4240.75 (version before the patch) on Windows and looked into the assembly code of function `PasswordGenerationPopupControllerImpl::PasswordAccepted`. It seems that the compiler indeed optimized away the validation check of WeakPtr. Here are the asm code:

> u chrome!PasswordGenerationPopupControllerImpl::PasswordAccepted L50
chrome!PasswordGenerationPopupControllerImpl::PasswordAccepted [c:\b\s\w\ir\cache\builder\src\chrome\browser\ui\passwords\password_generation_popup_controller_impl.cc @ 194]:
// ... skip
lea     rcx,[rsi+290h]           // rsi points to {this}, and rcx will point to {driver_}
call    chrome!base::internal::WeakReference::MaybeValid (00007fff`900a4640)  // calls to MaybeValid to check the WeakPtr
mov     rcx,qword ptr [rsi+298h] // the code just ignores the check result returned by MaybeValid
lea     r9,[rsi+2F8h]
mov     r8d,dword ptr [rsi+2B4h]
add     rsi,28h
mov     rax,qword ptr [rcx]
mov     rdx,rsi
call    qword ptr [rax+28h]      // driver_->GeneratedPasswordAccepted, which results in UaF
// ... skip

So my understanding is that this bug can be triggered in official release build and can be exploited as a Uaf bug. We also found another bug with the same code pattern (optimization of WeakPtr), and successfully exploited it in TFC 2020 (https://bugs.chromium.org/p/chromium/issues/detail?id=1146670).

If you could reconsider this issue that would be great!

### va...@chromium.org (2020-11-10)

That issue was fixed in r816701. Obviously, WeakPtr should not allow undefined behaviors in either debug or release builds.

### ad...@chromium.org (2020-11-10)

jtrrodant@ thanks, yes, I'll take it back to the panel for reconsideration. The VRP panel's main concern was that the WeakPtr optimization trick was not proven to be exploitable in a release build, and I think we now have sufficient evidence to reconsider. You probably saw that we wrote up https://crbug.com/chromium/1146679 about the WeakPtr problem specifically and released a fix yesterday.

### [Deleted User] (2020-11-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-18)

The VRP panel has considered the new evidence and decided to award $20,000. Congratulations!

### ad...@google.com (2020-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1133635?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053471)*
