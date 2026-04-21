# Security:  UAF in PlatformAuthNavigationThrottle::FetchHeadersCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40063127](https://issues.chromium.org/issues/40063127) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Enterprise |
| **Platforms** | Windows |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ig...@chromium.org |
| **Created** | 2023-02-17 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

The fucntion `PlatformAuthNavigationThrottle::FetchHeaders` calls `PlatformAuthProviderManager::GetData` to request some auth data from CloudAP at line [1]. The NavigationRequest may be deferred until the callback `PlatformAuthNavigationThrottle::FetchHeadersCallback` calls `Resume`. However, calling `Resume` may delete PlatformAuthNavigationThrottle synchronously, which result in UAF write at line [2].

There are several ways to let `Resume` delete the NavigationRequest synchronously. For example, if we do a cross-site prerendering, the PrerenderNavigationThrottle would cancel the navigation.

```
content::NavigationThrottle::ThrottleCheckResult  
PlatformAuthNavigationThrottle::FetchHeaders() {  
  // skip  
  PlatformAuthProviderManager::GetInstance().GetData(  // ===> [1]  
      navigation_handle()->GetURL(),  
      base::BindOnce(&PlatformAuthNavigationThrottle::FetchHeadersCallback,  
                     weak_ptr_factory_.GetWeakPtr()));  
  // skip  
  is_deferred_ = true;  
  return content::NavigationThrottle::DEFER;  
}  
  
void PlatformAuthNavigationThrottle::FetchHeadersCallback(  
    net::HttpRequestHeaders auth_headers) {  
  net::HttpRequestHeaders::Iterator it(auth_headers);  
  // skip  
  // Resume the deferred request.  
  if (is_deferred_) {  
    Resume();  
    is_deferred_ = false;  // ===> [2]  
  }  
  fetch_headers_callback_ran_ = true;  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/platform_auth/platform_auth_navigation_throttle.cc;l=69;drc=201b30c56179ff5e6f4c915ec69b19c62e8951d2>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/platform_auth/platform_auth_navigation_throttle.cc;l=95;drc=201b30c56179ff5e6f4c915ec69b19c62e8951d2>

**VERSION**  

Chrome Version: Tested on 112.0.5593.1 asan buid  

Operating System: Chrome on Windows only

**REPRODUCTION CASE**

1. Apply the attached path.diff, this is to simulate Azure AD SSO for Chromium, for the convenience of reproduction in the local asan environment
2. Host poc.html at localhost:8000 using nodejs  
   
   node .\server.js
3. Run  
   
   out\asan\chrome.exe --enable-features=CloudApAuth <http://localhost:8000/poc.html>

\*Fix Suggestion\*  

Since `Resume` may delete PlatformAuthNavigationThrottle synchronously, we can reorder `PlatformAuthNavigationThrottle::FetchHeaders` to make sure no code would run after `Resume`

diff --git a/chrome/browser/enterprise/platform\_auth/platform\_auth\_navigation\_throttle.cc b/chrome/browser/enterprise/platform\_auth/platform\_auth\_navigation\_throttle.cc  

index 7d3e6f41f3356..3f69c5354212b 100644  

--- a/chrome/browser/enterprise/platform\_auth/platform\_auth\_navigation\_throttle.cc  

+++ b/chrome/browser/enterprise/platform\_auth/platform\_auth\_navigation\_throttle.cc  

@@ -89,12 +89,12 @@ void PlatformAuthNavigationThrottle::FetchHeadersCallback(  

navigation\_handle()->SetRequestHeader(it.name(), it.value());  

}

- fetch\_headers\_callback\_ran\_ = true;  
  
  // Resume the deferred request.  
  
  if (is\_deferred\_) {

- Resume();  
  
  is\_deferred\_ = false;

- Resume();  
  
  }

- fetch\_headers\_callback\_ran\_ = true;  
  
  }

} // namespace enterprise\_auth

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 1.5 KB)
- [server.js](attachments/server.js) (text/plain, 660 B)
- [poc.html](attachments/poc.html) (text/plain, 170 B)
- [asan.log](attachments/asan.log) (text/plain, 14.3 KB)
- [patch2.diff](attachments/patch2.diff) (text/plain, 1.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 170 B)
- [server.js](attachments/server.js) (text/plain, 664 B)

## Timeline

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-17)

I can reproduce this on head on Windows. I still have to figure out if it can be reproduced on other channels.

Setting critical severity because this is a UAF in the browser process. The field trial configuration for CloudApAuth has been enabled, so this is not Security_Impact-None.

Assigning to igorruvinov@ based on git history:
1. Could you PTAL and prioritize a fix, or triage as relevant?
2. Also, could you confirm that the patch in patch.diff used to simulate Azure AD SSO for Chromium is reasonable, and there is a configuration where this would be enabled for users without it?

[Monorail components: Enterprise]

### th...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-17)

Tentatively setting the FoundIn to M110 based on the suspected CL[1] having been added in M110. igorruvinov@ -- please say so if the code path is actually only possible in M111 or M112. Note that whether or not the feature is enabled on a certain channel is irrelevant for the FoundIn label, only whether the code path exists.

[1]: https://crrev.com/c/4022015

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-18)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ig...@chromium.org (2023-02-18)

Re https://crbug.com/chromium/1417122#c2:

1. SG, I'll work on a fix. Thanks jtrrodant@ for the great write-up!

2. The patch diff is reasonable but not realistic. The feature is only enabled for certain hard-coded URLs (currently only login.live.com and login.microsoftonline.com) and the patch diff changes the list of supported URLs which is not possible in practice. Is there a way to reproduce the issue with the supported URLs?


Re https://crbug.com/chromium/1417122#c4:

The code path does not exist in M110.

Although the feature is implemented in M110, it is behind both a feature flag and a default-disabled policy (CloudAPAuthEnabled), and support for the policy begins in M111. It's possible to reach the code path in M110, but the user would have to enable the policy and add it to the "EnableExperimentalPolicies" policy: https://chromeenterprise.google/policies/#EnableExperimentalPolicies

Once the feature launches in M111, it will still be gated by the default-disabled CloudAPAuthEnabled. Users that don't enable the policy will never come across the code path.

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### ig...@chromium.org (2023-02-18)

+CC thefrog@ in case any of the labels need to be updated.

### jt...@gmail.com (2023-02-20)

Re https://crbug.com/chromium/1417122#c7:
> Is there a way to reproduce the issue with the supported URLs?

Yes, the patch added aa.com as one of the supported URLs, it is ok if you change aa.com to login.live.com or login.microsoftonline.com. The purpose of adding the URL is to let PlatformAuthNavigationThrottle fetch data in the local environment, and the URL origin does not matter.
The attached files added login.live.com to the list for your convenience.

### ad...@google.com (2023-02-20)

Thanks for https://crbug.com/chromium/1417122#c7. Adjusting to Security_Impact-Beta.

### ig...@chromium.org (2023-02-20)

Re https://crbug.com/chromium/1417122#c10:
Thanks jtrrodant@ for explaining. I was able to repro with the updated server.js without explicitly adding login.live.com to the list of origins.

The fix CL (recommended by jtrrodant@) is approved and should land soon: https://crrev.com/c/4268390. I confirmed locally that it fixes the UAF.

Once the fix lands and we confirm the UAF is gone in Canary, we can request permission to merge into M111 (Beta). To confirm, the M111 branch is refs/branch-heads/5563, correct?

### gi...@appspot.gserviceaccount.com (2023-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f19d038a9cb7c37653a7fa79f6060359a1ddcb56

commit f19d038a9cb7c37653a7fa79f6060359a1ddcb56
Author: Igor Ruvinov <igorruvinov@chromium.org>
Date: Mon Feb 20 16:27:26 2023

[CloudAP SSO] Move navigation throttle Resume() to end of method.

Resume() can synchronously delete the corresponding navigation throttle,
so nothing after it should reference the throttle.

Bug: 1417122
Change-Id: Ib8f8cae27cc1a7500bb2644f68a18e95e7f84cb9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4268390
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Auto-Submit: Igor Ruvinov <igorruvinov@chromium.org>
Commit-Queue: Igor Ruvinov <igorruvinov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1107483}

[modify] https://crrev.com/f19d038a9cb7c37653a7fa79f6060359a1ddcb56/chrome/browser/enterprise/platform_auth/platform_auth_navigation_throttle.cc


### [Deleted User] (2023-02-20)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ig...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### ig...@chromium.org (2023-02-21)

The fix was picked up by Canary (112.0.5609.0). I'm trying to verify it, but keep getting ""ERROR: AddressSanitizer: breakpoint on unknown address ..." when running the ASAN version of Chrome downloaded via https://chromium.googlesource.com/chromium/src/+/HEAD/tools/get_asan_chrome/README.md.

Can someone advise on how to get around this or help verify the fix?

### [Deleted User] (2023-02-21)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ig...@chromium.org (2023-02-21)

Setting M111 as target milestone.

### th...@chromium.org (2023-02-21)

re https://crbug.com/chromium/1417122#c16 -- I am not sure why that would be. Maybe you could try verifying it with a local ASAN build instead? gn args as specified here: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md#configuring-the-build

### ig...@chromium.org (2023-02-21)

Re https://crbug.com/chromium/1417122#c19: I verified that the issue is no longer reproducible on head with a local ASAN build.

Should we add M111 merge request labels?

### ad...@google.com (2023-02-21)

Please mark it as Fixed (if it is indeed fixed), and then sheriffbot will start the merge process.

### ig...@chromium.org (2023-02-21)

SG, marking as Fixed.

In the meantime if someone else could verify the fix on head that'd be a good sanity check.

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

Requesting merge to beta M111 because latest trunk commit (1107483) appears to be after beta branch point (1097615).

Merge review required: M111 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ig...@chromium.org (2023-02-22)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://crrev.com/c/4268390

2. Has this fix been tested on Canary?

Not Canary since the testing the fix requires an ASAN build, but it was tested on the tip of main with a local ASAN build (see https://crbug.com/chromium/1417122#c16 and https://crbug.com/chromium/1417122#c20).

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

The fix is simple and does not pose any stability regressions or risks.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No as it is a simple fix. Feel free to test if you'd like by following go/cbe-aa-testplan.

### am...@chromium.org (2023-02-23)

M111 merge approved; please merge this fix to branch 5563 by Monday, 27 February so this fix can be included in M111/Stable RC cut. 


### gi...@appspot.gserviceaccount.com (2023-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a8b3eaf63fccc14009c2ded03e93c827933eb3f0

commit a8b3eaf63fccc14009c2ded03e93c827933eb3f0
Author: Igor Ruvinov <igorruvinov@chromium.org>
Date: Thu Feb 23 15:12:47 2023

[CloudAP SSO] Move navigation throttle Resume() to end of method.

Resume() can synchronously delete the corresponding navigation throttle,
so nothing after it should reference the throttle.

(cherry picked from commit f19d038a9cb7c37653a7fa79f6060359a1ddcb56)

Bug: 1417122
Change-Id: Ib8f8cae27cc1a7500bb2644f68a18e95e7f84cb9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4268390
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Auto-Submit: Igor Ruvinov <igorruvinov@chromium.org>
Commit-Queue: Igor Ruvinov <igorruvinov@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1107483}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4284860
Commit-Queue: Fabio Tirelo <ftirelo@chromium.org>
Reviewed-by: Fabio Tirelo <ftirelo@chromium.org>
Cr-Commit-Position: refs/branch-heads/5563@{#753}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/a8b3eaf63fccc14009c2ded03e93c827933eb3f0/chrome/browser/enterprise/platform_auth/platform_auth_navigation_throttle.cc


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Rong! The VRP Panel has decided to award you $30,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- excellent work! 

### jt...@gmail.com (2023-03-03)

Re https://crbug.com/chromium/1417122#c30:
Hi Amy, thanks for the reward! I'm also wondering whether this report is eligible for a renderer RCE (not requiring a compromised renderer) and patch bonus?

### am...@chromium.org (2023-03-03)

Hi Rong, sorry we missed the bit about the patch being yours. Thanks for pointing that out and I've updated the reward amount accordingly to reflect that. Regarding the RCE bonus, given this does require the Azure AD SSO auth and the addition of the policy to enterprise policies, we'll have to reassess as a Panel on that bit. I'll have an update after the next panel discussion next week. 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### jt...@gmail.com (2023-03-10)

Hi Amy, a friendly ping to understand if there are any updates? Thanks : )

### am...@chromium.org (2023-03-10)

Hi Rong, apologies for not having an update for this just yet. We had more bugs than time to review them this week. I'll put this at the top of the list for next week. Thanks for your patience! 

### am...@chromium.org (2023-03-17)

Congratulations Rong! Upon further assessment we've decided to extend the RCE renderer bonus for this issue since a compromised renderer was not required to trigger this UAF in the browser process. Thanks again for your efforts in discovering and reporting this issue to us! 

### jt...@gmail.com (2023-03-17)

Thanks for the assessment and updates!

### am...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1417122?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063127)*
