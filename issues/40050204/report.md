# Security: Use after free in MojoCdmProxyService

| Field | Value |
|-------|-------|
| **Issue ID** | [40050204](https://issues.chromium.org/issues/40050204) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Encrypted |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | xh...@chromium.org |
| **Created** | 2019-09-24 |
| **Bounty** | $5,000.00 |

## Description

This issue is similar to https://bugs.chromium.org/p/chromium/issues/detail?id=999311

The root cause is [MojoCdmProxyService::Initialize](https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_proxy_service.cc?rcl=cd722c54dece3fcc44e9f929d9746866b89f5ec3&l=30) can be called multiple times.

```c++
void MojoCdmProxyService::Initialize(
    mojom::CdmProxyClientAssociatedPtrInfo client,
    InitializeCallback callback) {
  DVLOG(2) << __func__;
  client_.Bind(std::move(client));

  cdm_proxy_->Initialize(
      this, base::BindOnce(&MojoCdmProxyService::OnInitialized,
                           weak_factory_.GetWeakPtr(), std::move(callback)));
}
```

If the function MojoCdmProxyService::Initialize is called twice, the same MojoCdmProxyService will be registered twice in the function [MojoCdmProxyService::OnInitialized](https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_proxy_service.cc?rcl=cd722c54dece3fcc44e9f929d9746866b89f5ec3&l=84)
```c++
void MojoCdmProxyService::OnInitialized(InitializeCallback callback,
                                        ::media::CdmProxy::Status status,
                                        ::media::CdmProxy::Protocol protocol,
                                        uint32_t crypto_session_id) {
  if (status == ::media::CdmProxy::Status::kOk)
    cdm_id_ = context_->RegisterCdmProxy(this);  ---------------------------->register twice here

  std::move(callback).Run(status, protocol, crypto_session_id, cdm_id_);
}
```

So in the function [MojoCdmServiceContext::RegisterCdmProxy](https://cs.chromium.org/chromium/src/media/mojo/services/mojo_cdm_service_context.cc?rcl=bf942a81e62d37194914684afb6284bae2775f9d&l=87), two cdm ids will be mapped to the same MojoCdmProxyService. when MojoCdmProxyService is destructed. only one cdm id is unregistered. and the other cdm id is mapped to a Dangling pointer. then if the function MojoCdmServiceContext::GetCdmContextRef is called, the UAF occurs.

```c++
int MojoCdmServiceContext::RegisterCdmProxy(
    MojoCdmProxyService* cdm_proxy_service) {
  DCHECK(cdm_proxy_service);
  int cdm_id = GetNextCdmId();
  cdm_proxy_services_[cdm_id] = cdm_proxy_service; ------------------------------->two cdm ids map to one cdm_proxy_service
  DVLOG(1) << __func__ << ": CdmProxyService registered with CDM ID " << cdm_id;
  return cdm_id;
}

std::unique_ptr<CdmContextRef> MojoCdmServiceContext::GetCdmContextRef(
int cdm_id) {
DVLOG(1) << __func__ << ": cdm_id = " << cdm_id;

....

#if BUILDFLAG(ENABLE_LIBRARY_CDMS)
  // Next check all CdmProxies.
  auto cdm_proxy_service = cdm_proxy_services_.find(cdm_id);
  if (cdm_proxy_service != cdm_proxy_services_.end()) {
    return std::make_unique<CdmProxyContextRef>(
        cdm_proxy_service->second->GetCdmContext());  -----------------------> UAF happen here
  }
#endif  // BUILDFLAG(ENABLE_LIBRARY_CDMS)

  LOG(ERROR) << "CdmContextRef cannot be obtained for CDM ID: " << cdm_id;
  return nullptr;
}
```

This issue exists on stable and master branch


## Timeline

### va...@chromium.org (2019-09-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>Encrypted]

### va...@chromium.org (2019-09-25)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-09-25)

jrummell@/xhwang@: could you help work on a fix for this? We aim to deploy fixes for critical vulnerabilities to all users in 30 days, so your help here is much appreciated.

I'm not sure how to repro this but the bug description seems reasonable.

### va...@chromium.org (2019-09-25)

Actually, it isn't clear how the PC can be controlled so lowering it to High.

### va...@chromium.org (2019-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-25)

[Empty comment from Monorail migration]

### xh...@chromium.org (2019-09-25)

Thanks for reporting!

Correct me if I am wrong. The MojoCdmProxyService is different from other mojo media services that it is not created/called directly from the render process. Rather, it's called from a CDM running in the CDM process via the browser process [1]. I don't see a way to easily compromise the CDM process or the browser process to call Initialize() twice to trigger the reported issue. So I don't feel this is a Security_Severity-High issue.

Regardless, I'll work on a fix.

[1] https://cs.chromium.org/chromium/src/content/browser/media/media_interface_proxy.cc?type=cs&sq=package:chromium&g=0&l=239

### xh...@chromium.org (2019-09-25)

vakh: See #7 on whether this should be Security_Severity-High or not.

A tentative fix is at: https://chromium-review.googlesource.com/c/chromium/src/+/1825462

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6693c6288f5cb1ff36a12ced459a4ba413da3f3e

commit 6693c6288f5cb1ff36a12ced459a4ba413da3f3e
Author: Xiaohan Wang <xhwang@chromium.org>
Date: Wed Sep 25 21:14:35 2019

Add more checks in MojoCdmProxyService

This is to prevent abnormal cases from happening.

Bug: 1007194
Test: Added a unittest.
Change-Id: Ica15709371e833ed5fc423ed8ddc4f39a9aa6517
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1825462
Reviewed-by: John Rummell <jrummell@chromium.org>
Commit-Queue: Xiaohan Wang <xhwang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#699961}

[modify] https://crrev.com/6693c6288f5cb1ff36a12ced459a4ba413da3f3e/media/mojo/services/mojo_cdm_proxy_service.cc
[modify] https://crrev.com/6693c6288f5cb1ff36a12ced459a4ba413da3f3e/media/mojo/services/mojo_cdm_proxy_service.h
[modify] https://crrev.com/6693c6288f5cb1ff36a12ced459a4ba413da3f3e/media/mojo/services/mojo_cdm_proxy_unittest.cc


### xh...@chromium.org (2019-10-03)

Requesting to merge the fix in #9 to M78. I could also merge to M77 if needed. The risk of the change is very low. But again, please see #7 and #8 on whether this is Security_Severity-High or not.

### sh...@chromium.org (2019-10-03)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-03)

merge approved for M78 branch:3904

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a593965a7a83942434fe8f46e9380d38eb703bb

commit 7a593965a7a83942434fe8f46e9380d38eb703bb
Author: Xiaohan Wang <xhwang@chromium.org>
Date: Fri Oct 04 01:21:21 2019

(merge m78) Add more checks in MojoCdmProxyService

This is to prevent abnormal cases from happening.

(cherry picked from commit 6693c6288f5cb1ff36a12ced459a4ba413da3f3e)

Bug: 1007194
Test: Added a unittest.
Change-Id: Ica15709371e833ed5fc423ed8ddc4f39a9aa6517
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1825462
Reviewed-by: John Rummell <jrummell@chromium.org>
Commit-Queue: Xiaohan Wang <xhwang@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#699961}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1838550
Reviewed-by: Xiaohan Wang <xhwang@chromium.org>
Cr-Commit-Position: refs/branch-heads/3904@{#611}
Cr-Branched-From: 675968a8c657a3bd9c1c2c20c5d2935577bbc5e6-refs/heads/master@{#693954}

[modify] https://crrev.com/7a593965a7a83942434fe8f46e9380d38eb703bb/media/mojo/services/mojo_cdm_proxy_service.cc
[modify] https://crrev.com/7a593965a7a83942434fe8f46e9380d38eb703bb/media/mojo/services/mojo_cdm_proxy_service.h
[modify] https://crrev.com/7a593965a7a83942434fe8f46e9380d38eb703bb/media/mojo/services/mojo_cdm_proxy_unittest.cc


### sh...@chromium.org (2019-10-04)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-04)

xhwang@ regarding https://crbug.com/chromium/1007194#c7, thanks for the analysis!

Supposing that there were crafted encrypted content which were able to compromise a CDM; could it conceivably use this bug to elevate privilege to the browser process? If so, it's still high.

For that reason I'm going to add Merge_Request-77.

However, xhwang@, maybe this is not a risk. If so please explain and I'll remove that label, and downgrade to medium. In particular it would be great if you can explain the process relationships a bit more. Is a CdmProxy a way for a CDM to control and interact with the browser process, or is it a way for the CDM to control and interact with things in the renderer process? Which processes are able to call Initialize?

### dc...@chromium.org (2019-10-04)

xhwang, it *does* seem like CreateCdmProxy is restricted and can't be retrieved from the renderer proxy directly. If that's truly the case, then this /might/ be lower severity.

However, it's quite hard to trace the code to understand this, and it's a bit fragile: someone could change the implementation of MediaInterfaceProxy in content/browser, and then this might no longer be true. So:

- documentation-wise, I think we might need to be more explicit about these services and where they're hosted: there's already some useful diagrams for Renderer, et cetera, but I'm thinking we might want one that shows the explicit relationship of various media services on various platforms (CDM is here, CDM proxy is to used to allow the CDM to talk to the GPU for certain capabilities (typically hardware CDM), et cetera.
- similarly, we should figure out a story for media interface factory: either it should be responsible for brokering everything centrally, and we only have one media interface factory, specifically for browser<->renderer communication or maybe we should split it up into more distinct capabilities

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### xh...@chromium.org (2019-10-07)

Re #15: If you compromise the CDM, it's not possible to use this attack because the interface that supports CdmProxy is not enabled yet. But if you say the whole CDM process is compromised somehow and you can run any code there, then yes it can try to create the CdmProxy and call Initialize() twice. But still, per #16, it's still true that you cannot trigger this issue directly from the renderer process (in the sense that you have to compromise the CDM process first).

Re #16: Will it be easier from security's perspective that all mojo media services could be running in a privileged process and hence should the security-proof and reviewed? I can add some documentation around this current section [1].

For the question on "media interface factory", I am not too sure what your proposal is. We can talk about this offline if you prefer. Thanks!

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/media/mojo/README.md#flexible-process-model


### xh...@chromium.org (2019-10-07)

Ah, I misread #15 and thought it's already merge approved and merged the fix (https://chromium-review.googlesource.com/c/chromium/src/+/1846011).

I'll revert that merge and wait for proper merge approval.

### xh...@chromium.org (2019-10-07)

Re #15 on how CdmProxy works exactly:

The CdmProxy is a way for the CDM (running the a CDM/utility process) to interact with a CdmProxy implementation (e.g. D3D11CdmProxy) that runs in the GPU process. See the diagram in [1].

I believe a hacker has to compromise the CDM process to run arbitrary code before this reported exploit can be triggered, because:
1. The interface (cdm::Host_11) that supports the creation of CdmProxy [2] is not supported by Chrome by default yet.
2. There's no CDM shipped to use CdmProxy yet.
3. There's no way to create a CdmProxy from the render process today [3].
Therefore, a hacker must exploit the CDM process to make a call to create CdmProxy directly, and then call Initialize() twice.

[1] http://shortn/_CjJ6geVXLi
[2] https://cs.chromium.org/chromium/src/media/cdm/api/content_decryption_module.h?q=content_decryption_module&sq=package:chromium&g=0&l=1362
[3] https://cs.chromium.org/chromium/src/content/browser/media/media_interface_proxy.cc?q=media_interface_pro&sq=package:chromium&g=0&l=242

### na...@google.com (2019-10-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-09)

Congrats! The Panel decided to reward $5,000 for this report :) 

### na...@google.com (2019-10-09)

[Empty comment from Monorail migration]

### la...@google.com (2019-10-17)

rejecting for M77 as the release is in Stable and no more re-spins are planned

### mm...@chromium.org (2019-12-03)

xhwang@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2019-12-11)

Aha, I failed to spot that this was released (the revert from M77 confused my scripts). Sorry about that higongguang@ - I'll update the release notes and I've allocated a CVE.

### hi...@gmail.com (2019-12-16)

[Comment Deleted]

### ad...@google.com (2020-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2020-02-26)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-26)

This issue was migrated from crbug.com/chromium/1007194?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050204)*
