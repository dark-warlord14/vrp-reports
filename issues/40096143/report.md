# Security: Use after free in MojoCdmService

| Field | Value |
|-------|-------|
| **Issue ID** | [40096143](https://issues.chromium.org/issues/40096143) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Media>Encrypted |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | jr...@chromium.org |
| **Created** | 2019-08-29 |
| **Bounty** | $30,000.00 |

## Description

(filed on behalf of the reporter)

The bug:

The root cause is [MojoCdmService::Initialize](https://cs.chromium.org/chromium/src/media/mojo/mojom/content_decryption_module.mojom?l=82&ct=xref_jump_to_def) can be called multiple times. 

```c++
void MojoCdmService::Initialize(const std::string& key_system,
                                const url::Origin& security_origin,
                                const CdmConfig& cdm_config,
                                InitializeCallback callback) {
  DVLOG(1) << __func__ << ": " << key_system;
  DCHECK(!cdm_);  ------------------>In debug version, this DCHECK will be trigger

  auto weak_this = weak_factory_.GetWeakPtr();
  cdm_factory_->Create(
      key_system, security_origin, cdm_config,
      base::Bind(&MojoCdmService::OnSessionMessage, weak_this),
      base::Bind(&MojoCdmService::OnSessionClosed, weak_this),
      base::Bind(&MojoCdmService::OnSessionKeysChange, weak_this),
      base::Bind(&MojoCdmService::OnSessionExpirationUpdate, weak_this),
      base::Bind(&MojoCdmService::OnCdmCreated, weak_this,
                 base::Passed(&callback)));
}
```
If the function MojoCdmService::Initialize is called twice, the same MojoCdmService will be registered twice in the function [MojoCdmService::OnCdmCreated](https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service.cc?rcl=a64ec63d6caf3838818b97a49dd95950f29ef6ad&l=140)
```c++
void MojoCdmService::OnCdmCreated(
    InitializeCallback callback,
    const scoped_refptr<::media::ContentDecryptionModule>& cdm,
    const std::string& error_message) {
  mojom::CdmPromiseResultPtr cdm_promise_result(mojom::CdmPromiseResult::New());

  // TODO(xhwang): This should not happen when KeySystemInfo is properly
  // populated. See http://crbug.com/469366
  if (!cdm) {
    cdm_promise_result->success = false;
    cdm_promise_result->exception = CdmPromise::Exception::NOT_SUPPORTED_ERROR;
    cdm_promise_result->system_code = 0;
    cdm_promise_result->error_message = error_message;
    std::move(callback).Run(std::move(cdm_promise_result), 0, nullptr);
    return;
  }

  cdm_ = cdm;

  if (context_) {
    cdm_id_ = context_->RegisterCdm(this); ---------------------------->register twice here
    DVLOG(1) << __func__ << ": CDM successfully registered with ID " << cdm_id_;
  }
  ...
}
```

So in the function [MojoCdmServiceContext::RegisterCdm](https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service_context.cc?rcl=3bcb70cef58efe3a14d211aff71e72e2d402c894&l=72), two cdm ids will be mapped to the same MojoCdmService. when MojoCdmService is destructed. only one cdm id is unregistered. and the other cdm id is mapped to a Dangling pointer. then if the function MojoCdmServiceContext::GetCdmContextRef is called, the UAF occurs.

```c++
int MojoCdmServiceContext::RegisterCdm(MojoCdmService* cdm_service) {
  DCHECK(cdm_service);
  int cdm_id = GetNextCdmId();
  cdm_services_[cdm_id] = cdm_service;------------------------------->two cdm ids map to one cdm_service
  DVLOG(1) << __func__ << ": CdmService registered with CDM ID " << cdm_id;
  return cdm_id;
}
```

Because the size of MojoCdmService is small, there is a lot of noise(many other objects have the same size range), it's hard to reoccupy the freed MojoCdmService object, but its member variable "scoped_refptr<::media::ContentDecryptionModule> cdm_" point to a large object, we can reoccupy the freed cdm_ with the controlled data. cdm_ has virtual table, the virtual table can be controlled too.
then when [MojoCdmServiceContext::GetCdmContextRef](https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service_context.cc?rcl=90e84c7240870d52c224cb8c07b52545a2ef7cef&l=103) is called, we can control pc with the virtual function GetCdmContext.

```c++
std::unique_ptr<CdmContextRef> MojoCdmServiceContext::GetCdmContextRef(
    int cdm_id) {
  DVLOG(1) << __func__ << ": cdm_id = " << cdm_id;

  // Check all CDMs first.
  auto cdm_service = cdm_services_.find(cdm_id);
  if (cdm_service != cdm_services_.end()) {
    if (!cdm_service->second->GetCdm()->GetCdmContext()) {   -------------------->PC controlled here
      NOTREACHED() << "All CDMs should support CdmContext.";
      return nullptr;
    }
    return std::make_unique<CdmContextRefImpl>(cdm_service->second->GetCdm());
  }
```


## Timeline

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>Encrypted]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2019-08-29)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-08-29)

Adding folks who have recently worked on the related media mojo bindings.

xhwang@ could you help work on a fix for this? This was reported as part of a full-chain exploit (combined with https://crbug.com/chromium/999310 -- let me know if you'd like access). We aim to deploy fixes for critical vulnerabilities to all users in 30 days, so your help here is much appreciated.

### dc...@chromium.org (2019-08-29)

Btw, we can make a simple fix for getting this resolved quickly, but I'd suggest that we need to start being stricter about how stateful interfaces like this work. Stateful interfaces are proving somewhat difficult to reason about the safety of. We should split this up into:

interface CdmFactory {
  Initialize(..., pending_remote<ContentDecryptionModuleClient>, pending_receiver<ContentDecryptionModule>);
};

interface ContentDecryptionModule {
  ...
};

To ensure initialization is actually one-shot.


### xh...@chromium.org (2019-08-29)

dcheng: Given I'll be OOO tomorrow followed by long weekend and we want to have a quick fix asap, does it make sense I upload a quick fix now, and then we can discuss your idea later?

### ct...@chromium.org (2019-08-29)

Yes, a quick fix would be best for now and splitting up the interface can be a followup. The quick fix may be easier to merge back as well.

### xh...@chromium.org (2019-08-30)

Tentative fix uploaded at https://chromium-review.googlesource.com/c/chromium/src/+/1777139

### aw...@google.com (2019-08-30)

[Empty comment from Monorail migration]

### xh...@chromium.org (2019-08-30)

jrummell: I'll be OOO tomorrow. The fix https://chromium-review.googlesource.com/c/chromium/src/+/1777139 is in CQ right now and should land shortly. I've tested on shaka demo player but please also help test a bit more with protected content playback. Then we'll need to merge this to both M77 and M76. The fix is very small so I don't expect pushbacks for the merge request. Thanks in advance for the help!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b7b305f3389017cc42e2cfac6e7a319f42d5bde3

commit b7b305f3389017cc42e2cfac6e7a319f42d5bde3
Author: Xiaohan Wang <xhwang@chromium.org>
Date: Fri Aug 30 02:07:20 2019

Add more checks in MojoCdmService

This is to prevent abnormal cases from happening.

Bug: 999311
Test: Tested w/ shaka player demo and existing unit tests pass
Change-Id: Icef06d979351f16386cf3cbb177971a57a1e264c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1777139
Auto-Submit: Xiaohan Wang <xhwang@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: John Rummell <jrummell@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Xiaohan Wang <xhwang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#691911}

[modify] https://crrev.com/b7b305f3389017cc42e2cfac6e7a319f42d5bde3/media/mojo/services/mojo_cdm_service.cc
[modify] https://crrev.com/b7b305f3389017cc42e2cfac6e7a319f42d5bde3/media/mojo/services/mojo_cdm_service.h


### ad...@google.com (2019-08-30)

I'm going to mark this as Fixed and add the Merge-Request labels. xhwang@ please reopen if any problems occur; plus jrummell@ please poke and it and test as appropriate to give confidence to the release TPMs that this can be merged to stable.

### sh...@chromium.org (2019-08-30)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2019-08-30)

Filling out the merge survey:

1. Yes, this is a critical security vulnerability.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1777139
3. Yes.
4. This fixes a critical security vulnerability that is part of a full chain exploit (alongside https://crbug.com/chromium/999310)
5. No
6. N/A

### go...@chromium.org (2019-08-30)

[Comment Deleted]

### ct...@chromium.org (2019-08-30)

Assigning this to jrummell@ to handle the merges (feel free to ping me as needed).

### go...@chromium.org (2019-08-30)

Approving merge to M76 branch 3809 and M77 branch 3865 based on https://crbug.com/chromium/999311#c17 and per internal mail thread. Please merge ASAP. Thank you.

Note: Change listed at #14 is not yet baked in canary, pls merge the change to current canary branch 3896 so we can trigger new canary from same branch.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/621812eec2ac165cf8786a6a0db76c8cf00fbdfc

commit 621812eec2ac165cf8786a6a0db76c8cf00fbdfc
Author: Xiaohan Wang <xhwang@chromium.org>
Date: Fri Aug 30 04:00:26 2019

[Canary] Add more checks in MojoCdmService

This is to prevent abnormal cases from happening.

(cherry picked from commit b7b305f3389017cc42e2cfac6e7a319f42d5bde3)

Bug: 999311
Test: Tested w/ shaka player demo and existing unit tests pass
Change-Id: Icef06d979351f16386cf3cbb177971a57a1e264c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1777139
Auto-Submit: Xiaohan Wang <xhwang@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: John Rummell <jrummell@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Xiaohan Wang <xhwang@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#691911}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1777160
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/branch-heads/3896@{#7}
Cr-Branched-From: 2fe8b7f1c9edabaffdd52448ef4745cfb3d05b2e-refs/heads/master@{#691365}

[modify] https://crrev.com/621812eec2ac165cf8786a6a0db76c8cf00fbdfc/media/mojo/services/mojo_cdm_service.cc
[modify] https://crrev.com/621812eec2ac165cf8786a6a0db76c8cf00fbdfc/media/mojo/services/mojo_cdm_service.h


### ct...@chromium.org (2019-08-30)

I've cherry-picked the CL from #14 to branch 3896 for Canary.

### go...@chromium.org (2019-08-30)

Thank you  cthomp@. Triggering new canary for Desktop and Android from 3896 branch.



### go...@chromium.org (2019-08-30)

Requesting to verify this bug on canary version 78.0.3896.6+. Please merge to M76 and M77 if change looks good and after well baked in canary.

### sh...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-08-30)

Manually tested with Shaka Demo Player with Widevine (https://shaka-player-demo.appspot.com/demo/#audiolang=en-US;textlang=en-US;uilang=en-US;asset=https://storage.googleapis.com/shaka-demo-assets/sintel-widevine/dash.mpd;panel=HOME;build=uncompiled) and did not see any breakage on Canary.

jrummell@ Is there other testing we should do before merging?

### sr...@google.com (2019-08-30)

Rejecting merge to M76 , per meeting with security TPM's. We are going to target the fix to M77. Please merge to M77 once canary coverage looks good

lakpamarthy@ Pls help get this bug before beta next week

### go...@chromium.org (2019-08-30)

Thank you Srinivas.
If change looks good in canary, please merge to M77 beta branch 3865 on Tuesday (09/03) morning.

+benmason@ as well.

### jr...@chromium.org (2019-08-30)

Tried Shaka, Netflix, and Amazon with Canary 78.0.3898.0. All is fine. Will merge to M77 now.

### sh...@chromium.org (2019-09-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### jr...@chromium.org (2019-09-03)

Not sure what happened to the merge email, but this was merged to M77 with https://chromium-review.googlesource.com/c/chromium/src/+/1779096.
Change has been successfully rebased and submitted as 9a20bf43332d6c2289067d2cc4fb409b455375b3

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### jr...@chromium.org (2019-09-03)

The merge landed on Friday (Aug 30 10:45 AM). No idea why the bug hasn't been updated.

Merge "Add more checks in MojoCdmService"

This is to prevent abnormal cases from happening.

(cherry picked from commit b7b305f3389017cc42e2cfac6e7a319f42d5bde3)

Bug: 999311
Test: Tested w/ shaka player demo and existing unit tests pass
Change-Id: Icef06d979351f16386cf3cbb177971a57a1e264c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1777139
Auto-Submit: Xiaohan Wang <xhwang@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: John Rummell <jrummell@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Xiaohan Wang <xhwang@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#691911}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1779096
Cr-Commit-Position: refs/branch-heads/3865@{#688}
Cr-Branched-From: 0cdcc6158160790658d1f033d3db873603250124-refs/heads/master@{#681094}
Cherry picks
refs/branch-heads/3896: [Canary] Add more checks in MojoCdmService
master: Add more checks in MojoCdmService

### la...@google.com (2019-09-03)

Dropping the Merge-Approved-77 label as the change has landed in M77 (3865) branch

### aw...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-09-05)

For reference the internal tracking bug with some more details is b/140174798

### aw...@google.com (2019-09-05)

Hi higongguang@ - shall we use your usual credit string for this and https://crbug.com/chromium/999310 in the M77 release notes?
 


### hi...@gmail.com (2019-09-06)

awhalley@ yes, you can use that

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-16)

Congrats! The Panel decided to reward $30,000 for this report! 

### pa...@chromium.org (2019-09-16)

[Comment Deleted]

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### hi...@gmail.com (2019-11-22)

Hi, Can we keep this bug private? please don't remove Restrict-View-SecurityNotify, I want to disclose it myself, thanks.

### ad...@google.com (2019-11-22)

Re https://crbug.com/chromium/999311#c46, the Restrict-View-SecurityEmbargo label will ensure this stays private even if Restrict-View-SecurityNotify is removed.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

jrummell@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### dc...@chromium.org (2020-02-26)

[Empty comment from Monorail migration]

### aw...@google.com (2020-07-07)

Remove allpublic from bugs that have Restrict-View-SecurityEmbargo

### aw...@google.com (2020-07-08)

higongguang@ - Confirming we're now OK to open this bug publically?

### xh...@chromium.org (2020-07-08)

[Empty comment from Monorail migration]

### hi...@gmail.com (2020-07-09)

 awhalley@  I want to delay it until I finish the BLACKHAT USA 2020 presentation

### aw...@google.com (2020-07-09)

Sounds good. Setting a Next Action of 2020-10-05 to open up after Blackhat.

### aw...@google.com (2020-08-20)

Opening up now Blackhat's happened. (The presentation was "TiYunZong: An Exploit Chain to Remotely Root Modern Android Devices - Pwn Android Phones from 2015 to 2020", and it's certainly worth a watch if you have access to the recordings — thanks Guang!)


### is...@google.com (2020-08-20)

This issue was migrated from crbug.com/chromium/999311?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096143)*
