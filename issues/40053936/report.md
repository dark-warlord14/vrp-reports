# Security: Cross-origin iframe can navigate top window to different site via same-site open redirect or XSS redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40053936](https://issues.chromium.org/issues/40053936) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2020-11-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A non-sandboxed cross-origin iframe can navigate the top window to a different origin by abusing an open redirect or XSS vulnerability in a URL which is same-site with the top window's origin.

At first glance, this seems mostly intentional based on discussion in <https://crbug.com/chromium/640057>, <https://github.com/WICG/interventions/issues/16> and <https://www.chromestatus.com/feature/5851021045661696>. There's also <https://crbug.com/chromium/624061> which seems related but is private.

The same-origin bypass seems intentional. The same-site bypass might have been implemented to address compatibility issues/concerns.

However, I haven't identified any public discussion about bypasses via open redirects or XSS redirects. If the following scenarios were taken into consideration or discussed somewhere, then feel free to disregard this report.

Scenarios:

1. Same-origin: iframe loaded in <https://example.com> bypasses via top navigation to <https://example.com/redirect?url=https://attacker.com> or <https://example.com/?xss=location.href%3Dhttps%3A%2F%2Fattacker.com>
2. Same-site: iframe loaded in <https://example.com> bypasses via top navigation to <https://subdomain.example.com/redirect?url=https://attacker.com> or <https://example.com/?xss=location.href%3Dhttps%3A%2F%2Fattacker.com>
3. Same-origin/same-site, different scheme: iframe loaded in <https://example.com> bypasses via top navigation to plaintext <http://example.com/attacker-page> (note HTTP in destination URL)

The same-site behavior is notable, since same-site bypasses are much more likely due to increased surface area: an open redirect or XSS in \*any\* subdomain is sufficient to bypass.

The diff-scheme behavior is also notable, since an attacker who has PITM/MITM capabilities can redirect to an HTTP URL on any site without HSTS and then redirect to the attacker URL. No existing open redirect or XSS vulnerability is needed, though the PITM requirement is a significantly higher bar.

This does not affect sandboxed iframes, since they either require user interaction for top navigations (allow-top-navigation-by-user-activation) or intentionally allow all top navigations (allow-top-navigation).

Potential solutions:

1. Add same-scheme or secure-scheme limitation for destination URLs.
2. Allow only same-origin navigations (remove same-site exception).
3. Remove no-interaction top-navigation from iframes unless sandbox="allow-top-navigation" is set.
4. Somehow determine if destination page will redirect to different site. This is probably not feasible, since redirect can be initiated via meta tags or scripts on a delay.

Relevant commit: <https://source.chromium.org/chromium/chromium/src/+/3eef8b926bd46f329e372fb674dd6f2d5ad0844d>

**VERSION**  

Chrome Version: 87.0.4280.66 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 OS Version 2004 (Build 19041.630)

**REPRODUCTION CASE**  

Scenario 1 repro:

1. Navigate to <https://alesandroortiz.com/security/chromium/nav-top-no-interaction.html>

Expected behavior:  

iframe cannot navigate top window

Observed behavior:  

iframe can navigate top window

iframe URL: <https://aogarantiza.com/chromium/nav-top-no-interaction-frame.html>

To repro the other scenarios, modify the iframe source code (the other scenarios are commented out).

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [nav-top-no-interaction.html](attachments/nav-top-no-interaction.html) (text/plain, 716 B)
- [nav-top-no-interaction-frame.html](attachments/nav-top-no-interaction-frame.html) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2020-11-20)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-11-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### [Deleted User] (2020-11-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-05)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@google.com (2020-12-07)

I am not sure I understand correctly. A non-sandboxed cross-origin iframe can navigate the main page. For example, this is allowed:

(on https://a.com)
<iframe src="https://b.com"></iframe>

(on https://b.com)
<script>
window.top.location = "https://c.com";
<script>

You don't need to exploit any redirect. Did I miss something here?

### al...@alesandroortiz.com (2020-12-07)

The example in https://crbug.com/chromium/1151507#c6 should not work. If it does work on your device, it's due to another bug (e.g. https://crbug.com/chromium/1085982: extensions may inadvertently activate frames).

Baseline PoC: https://alesandroortiz.com/security/chromium/nav-top-baseline.html (iframe: https://aogarantiza.com/chromium/nav-top-baseline-frame.html )

The redirect will be blocked unless the iframe has had user activation at least once since page load (code [2] checks sticky user activation).

For historical context, the same-origin allowed behavior was added in this commit to implement https://crbug.com/chromium/640057: https://source.chromium.org/chromium/chromium/src/+/3eef8b926bd46f329e372fb674dd6f2d5ad0844d

The current code is here, annotated below: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/frame/local_frame.cc;l=1695;drc=c58b1362e545b075450790b1f3aada2e3952fcea

Scenario 1 PoC at https://alesandroortiz.com/security/chromium/nav-top-no-interaction.html hits [3].
Scenario 2 PoC at https://c2.alesandroortiz.com/security/chromium/nav-top-no-interaction.html hits [6] (same PoC, diff origin)
Scenario 3 would also hit [6]. (No hosted PoC currently available, but I have verified in my environment.)

  if (target_frame == Tree().Top()) {                                             <-- [1] True when iframe navigates top frame
    // A frame navigating its top may blocked if the document initiating
    // the navigation has never received a user gesture and the navigation
    // isn't same-origin with the target.
    if (HasStickyUserActivation() ||                                                <-- [2] Another bug + sticky activation check may be causing https://crbug.com/chromium/1151507#c6 behavior
        target_frame.GetSecurityContext()->GetSecurityOrigin()->CanAccess(
            SecurityOrigin::Create(destination_url).get())) {            <-- [3] CanAccess() returns true for Scenario 1 (same-origin scenario, target_frame and destination_url origins are both https://alesandroortiz.com)
      return true;
    }

    String target_domain = network_utils::GetDomainAndRegistry(
        target_frame.GetSecurityContext()->GetSecurityOrigin()->Domain(),   <-- [4] Domain() returns alesandroortiz.com for origin https://c2.alesandroortiz.com (subdomain) or http://alesandroortiz.com (HTTP scheme)
        network_utils::kIncludePrivateRegistries);                         
    String destination_domain = network_utils::GetDomainAndRegistry(
        destination_url.Host(), network_utils::kIncludePrivateRegistries);        <-- [5] GetDomainAndRegistry() returns alesandroortiz.com for origin https://alesandroortiz.com
    if (!target_domain.IsEmpty() && !destination_domain.IsEmpty() &&
        target_domain == destination_domain) {                            <-- [6] target_domain == destination_domain returns true for Scenarios 2 and 3 (same-site scenario or diff-scheme scenario, target_domain and destination_domain are alesandroortiz.com)
      return true;
    }
    if (auto* settings_client = Client()->GetContentSettingsClient()) {
      if (settings_client->AllowPopupsAndRedirects(false /* default_value*/))
        return true;
    }
    PrintNavigationErrorMessage(
        target_frame,
        "The frame attempting navigation is targeting its top-level window, "
        "but is neither same-origin with its target nor has it received a "
        "user gesture. See "
        "https://www.chromestatus.com/features/5851021045661696.");
    GetLocalFrameHostRemote().DidBlockNavigation(
        destination_url, GetDocument()->Url(),
        mojom::NavigationBlockedReason::kRedirectWithNoUserGesture);             <-- [7] Navigation is blocked (shows omnibox icon on desktop, infobar on Android)
  } else { ... }





### al...@alesandroortiz.com (2020-12-07)

Minor corrections for https://crbug.com/chromium/1151507#c7:
[4] should read "GetDomainAndRegistry() returns..."
[7] The navigation is actually blocked by caller when they get `return false` at the end of LocalFrame::CanNavigate() (DidBlockNavigation() [7] triggers the UI).

### wf...@chromium.org (2020-12-09)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-09)

based on interaction above, I'm assigning this bug to you, antoniosartori@google.com - can you update with any progress made?

### [Deleted User] (2020-12-21)

antoniosartori: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@google.com (2020-12-23)

[Empty comment from Monorail migration]

### an...@chromium.org (2020-12-23)

This does not seem so easy to fix. The code from https://crbug.com/chromium/1151507#c7 currently checking whether the frame is allowed to navigate or not is in Blink. However, the redirect will be processed in the Browser later in the navigation logic, so we would need to check again there. We might want to move the check in the Browser in order to deduplicate code.

This looks like a bigger task.

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### pm...@chromium.org (2021-03-09)

Confirming the behavior, a cross origin iframe is allowed to navigate its top level frame to a same etld+1 document, without a user gesture. This ignores the scheme. See change's review at  https://chromium-review.googlesource.com/c/chromium/src/+/1187326/
I believe this is reasonable from a security perspective, the goal of this intervention being to reduce user annoyance, Embedded iframes must be sandboxed if they are considered untrustworthy. The reflective XSS example is interesting.

Nate: Since you were the author of the change aforementioned, I'd like to have your opinion on that before closing: Was the algorithm made scheme agnostic on purpose? Do you have references that led to the decision of restricting to eTLD + 1? I suppose that's related to the efforts to mitigate the reports we see in https://github.com/WICG/interventions/issues/16?

### pm...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-03-10)

Yeah, the eTLD+1 restriction was mostly a product of trial and error: we kept having to loosen the intervention because of compatibility requirements for legitimate use cases.  I don't know of any specific cases that require scheme-agnosticism, but I'd be surprised if it wouldn't break *something* out there on the web. It might be small enough that it's still worth tightening though?

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1baf9eba07b806f86a6e60851428c7ab318da093

commit 1baf9eba07b806f86a6e60851428c7ab318da093
Author: Pâris Meuleman <pmeuleman@chromium.org>
Date: Wed Mar 17 20:19:13 2021

Prevent Cross-Origin iframe from navigating top to a different scheme

Cross-origin iframes were prevented to navigate top with [1]. Those
iframes were allowed to navigate top only to same domain (eTLD+1)
following reports of adverse impact. This severely restrains the ability
of said iframe to cause nuisance.
It does not seem necessary however to loosen the constraint to allow
different schemes, especially from https to http. As a result this CL
prevents a cross-origin iframe from navigating top to the same eTLD + 1
with a different schemes if there's no user gesture.

[1] https://github.com/WICG/interventions/issues/16

Bug: 1151507
Fixed: 1151507

Change-Id: Ia1568175c044831594154ceea3e3aacb4e2efb2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2756509
Commit-Queue: Nate Chapin <japhet@chromium.org>
Auto-Submit: Pâris Meuleman <pmeuleman@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Cr-Commit-Position: refs/heads/master@{#863936}

[modify] https://crrev.com/1baf9eba07b806f86a6e60851428c7ab318da093/third_party/blink/renderer/core/frame/local_frame.cc
[add] https://crrev.com/1baf9eba07b806f86a6e60851428c7ab318da093/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/iframe-that-performs-different-scheme-same-etld-plus-one-top-navigation-without-user-gesture.html
[add] https://crrev.com/1baf9eba07b806f86a6e60851428c7ab318da093/third_party/blink/web_tests/http/tests/security/frameNavigation/xss-DENIED-different-scheme-same-etld-plus-1-top-navigation-without-user-gesture-expected.txt
[add] https://crrev.com/1baf9eba07b806f86a6e60851428c7ab318da093/third_party/blink/web_tests/http/tests/security/frameNavigation/xss-DENIED-different-scheme-same-etld-plus-1-top-navigation-without-user-gesture.html


### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-19)

Requesting merge to beta M90 because latest trunk commit (863936) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-19)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-03-19)

pls answer https://crbug.com/chromium/1151507#c28 for review

### ja...@chromium.org (2021-03-22)

pmeuleman and I just chatted, and we both would recommend against merge here. This issue has been present for quite some time, and the fix has a higher-than-average risk of compatibility issues. Waiting for M91 should be fine.

(Feel free to remove Merge-Rejected-90 label if this is an incorrect usage)

### al...@alesandroortiz.com (2021-03-22)

To confirm info from https://crbug.com/chromium/1151507#c21 and https://crbug.com/chromium/1151507#c23, the only planned change is to fix Scenario 3 (different scheme)?

Given the strong compatibility concerns and multiple prerequisites for Scenario 1 (same origin), this seems acceptable.

I still have concerns about Scenario 2 (same site/eTLD+1). Large-scale malicious redirect campaigns launched from iframes have been seen in the wild before (e.g. https://crbug.com/chromium/991568, forced redirect via sandbox restriction bypass). I understand the prerequisites are difficult and impacts are limited to a single site (eTLD+1), but it's still valuable in high-traffic sites and is easier than Scenario 3.

For Scenario 2, in addition to open redirects or XSS vulnerabilities, subdomain takeovers can also be used to perform top-level navigations. e.g. Attacker takes over subdomain.example.com, and compromised unsandboxed iframe navigates to https://subdomain.example.com which then navigates to a malicious URL (or hosts a malicious page.)

Seems like the decision is that compatibility concerns override security concerns for Scenario 2, but want to triple-confirm this.

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

Congratulations, Alesandro! The VRP Panel has awarded you $3000 for this report. Excellent work!

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### pm...@chromium.org (2021-03-29)

The implementation in c23 covers removes the tolerance for different schemes, i.e. scenario 3:
- navigating top to a same site different scheme (https -> http) url will not be an accepted exception anymore.

I believe we tried to be more restrictive in the past (see pushback on https://github.com/WICG/interventions/issues/16) and settled on this as a best effort.

While scenario 2, i.e. allowing a cross-origin iframe to navigate top same site  leads to issues, can be problematic as you highlight I reckon there's quite a few flows, especially around authentication, that break. 
IIUC sites that include untrusted iframes must use sandboxes.

japhet@: We could add a behavior (behind a flag) that would forbid scenario 2, and metrics to decide on an activation. But I believe you already did that and the current state was the results of your previous experiments. Do you confirm this and the above? 

### gi...@appspot.gserviceaccount.com (2021-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d29062199696de8226720fd8211fe4cf3d36b1de

commit d29062199696de8226720fd8211fe4cf3d36b1de
Author: Pâris MEULEMAN <pmeuleman@chromium.org>
Date: Thu Apr 08 14:44:10 2021

Kill switch for blocking top navigation to different scheme

Add a feature flag acting as a kill switch for the change introduced
in https://chromium-review.googlesource.com/c/chromium/src/+/2756509
This feature flag is enabled by default and can be switched off in
the event the change has impact on legitimate uses.

Bug: 1151507
Change-Id: Ibe99cff264f9ce3da29e69512e0f4325130a99e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2807363
Auto-Submit: Pâris Meuleman <pmeuleman@chromium.org>
Commit-Queue: Pâris Meuleman <pmeuleman@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Cr-Commit-Position: refs/heads/master@{#870512}

[modify] https://crrev.com/d29062199696de8226720fd8211fe4cf3d36b1de/third_party/blink/common/features.cc
[modify] https://crrev.com/d29062199696de8226720fd8211fe4cf3d36b1de/third_party/blink/public/common/features.h
[modify] https://crrev.com/d29062199696de8226720fd8211fe4cf3d36b1de/third_party/blink/renderer/core/frame/local_frame.cc


### al...@alesandroortiz.com (2021-05-03)

japhet@: Please see open question re: same-site navigation in https://crbug.com/chromium/1151507#c31 and https://crbug.com/chromium/1151507#c35.

pmeuleman@: Thanks for context in https://crbug.com/chromium/1151507#c35.

If there's data supporting compat issues, then I'm okay leaving as-is. Sandboxing the iframe is currently available as a mitigation for websites.

### ja...@chromium.org (2021-05-03)

I don't think we explicitly measured the case described in Scenario 2. We tried it and got enough compat breakage reports that we decided it wasn't worth the effort. But that was several years ago, and the landscape might've changed. I'd certainly be open to adding metrics and seeing if we can do something now.

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-25)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-25)

[Empty comment from Monorail migration]

### gi...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc4d50606409e3cc2cdff252001649ada3697ef4

commit dc4d50606409e3cc2cdff252001649ada3697ef4
Author: Pâris Meuleman <pmeuleman@chromium.org>
Date: Wed May 26 16:06:30 2021

[86-LTS] Prevent Cross-Origin iframe from navigating top to a different scheme

Cross-origin iframes were prevented to navigate top with [1]. Those
iframes were allowed to navigate top only to same domain (eTLD+1)
following reports of adverse impact. This severely restrains the ability
of said iframe to cause nuisance.
It does not seem necessary however to loosen the constraint to allow
different schemes, especially from https to http. As a result this CL
prevents a cross-origin iframe from navigating top to the same eTLD + 1
with a different schemes if there's no user gesture.

[1] https://github.com/WICG/interventions/issues/16

Bug: 1151507
Fixed: 1151507

(cherry picked from commit 1baf9eba07b806f86a6e60851428c7ab318da093)

Change-Id: Ia1568175c044831594154ceea3e3aacb4e2efb2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2756509
Commit-Queue: Nate Chapin <japhet@chromium.org>
Auto-Submit: Pâris Meuleman <pmeuleman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#863936}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917013
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1649}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/dc4d50606409e3cc2cdff252001649ada3697ef4/third_party/blink/renderer/core/frame/local_frame.cc
[add] https://crrev.com/dc4d50606409e3cc2cdff252001649ada3697ef4/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/iframe-that-performs-different-scheme-same-etld-plus-one-top-navigation-without-user-gesture.html
[add] https://crrev.com/dc4d50606409e3cc2cdff252001649ada3697ef4/third_party/blink/web_tests/http/tests/security/frameNavigation/xss-DENIED-different-scheme-same-etld-plus-1-top-navigation-without-user-gesture-expected.txt
[add] https://crrev.com/dc4d50606409e3cc2cdff252001649ada3697ef4/third_party/blink/web_tests/http/tests/security/frameNavigation/xss-DENIED-different-scheme-same-etld-plus-1-top-navigation-without-user-gesture.html


### ja...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fa42dbe9b20c062f5bbccc589aee86ae43174cdc

commit fa42dbe9b20c062f5bbccc589aee86ae43174cdc
Author: Pâris Meuleman <pmeuleman@chromium.org>
Date: Wed Jun 16 13:15:07 2021

[M90-LTS] Prevent Cross-Origin iframe from navigating top to a different scheme

Cross-origin iframes were prevented to navigate top with [1]. Those
iframes were allowed to navigate top only to same domain (eTLD+1)
following reports of adverse impact. This severely restrains the ability
of said iframe to cause nuisance.
It does not seem necessary however to loosen the constraint to allow
different schemes, especially from https to http. As a result this CL
prevents a cross-origin iframe from navigating top to the same eTLD + 1
with a different schemes if there's no user gesture.

[1] https://github.com/WICG/interventions/issues/16

Bug: 1151507
Fixed: 1151507

(cherry picked from commit 1baf9eba07b806f86a6e60851428c7ab318da093)

Change-Id: Ia1568175c044831594154ceea3e3aacb4e2efb2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2756509
Commit-Queue: Nate Chapin <japhet@chromium.org>
Auto-Submit: Pâris Meuleman <pmeuleman@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#863936}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2960870
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1528}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/fa42dbe9b20c062f5bbccc589aee86ae43174cdc/third_party/blink/renderer/core/frame/local_frame.cc
[add] https://crrev.com/fa42dbe9b20c062f5bbccc589aee86ae43174cdc/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/iframe-that-performs-different-scheme-same-etld-plus-one-top-navigation-without-user-gesture.html
[add] https://crrev.com/fa42dbe9b20c062f5bbccc589aee86ae43174cdc/third_party/blink/web_tests/http/tests/security/frameNavigation/xss-DENIED-different-scheme-same-etld-plus-1-top-navigation-without-user-gesture-expected.txt
[add] https://crrev.com/fa42dbe9b20c062f5bbccc589aee86ae43174cdc/third_party/blink/web_tests/http/tests/security/frameNavigation/xss-DENIED-different-scheme-same-etld-plus-1-top-navigation-without-user-gesture.html


### vs...@google.com (2021-06-16)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-09-19)

This issue has been fixed for 14 weeks (see https://crbug.com/chromium/1151507#c23 on March 17th). Is there a reason sheriffbot didn't make it public? IIUC should have been automatically disclosed around June 23rd.

### [Deleted User] (2021-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/301ecd231061729fff89eb9db3fd628e45d991a8

commit 301ecd231061729fff89eb9db3fd628e45d991a8
Author: 揚帆起航 <uioptt24@gmail.com>
Date: Tue Nov 22 19:16:02 2022

Remove "kBlockCrossOriginTopNavigationToDiffentScheme"

Bug: 1151507

Change-Id: I1b78eab4207aaa827d0d36a514190b64ed7014a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4048380
Reviewed-by: Philip Rogers <pdr@chromium.org>
Auto-Submit: 揚帆起航 <uioptt24@gmail.com>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1074783}

[modify] https://crrev.com/301ecd231061729fff89eb9db3fd628e45d991a8/third_party/blink/common/features.cc
[modify] https://crrev.com/301ecd231061729fff89eb9db3fd628e45d991a8/third_party/blink/public/common/features.h
[modify] https://crrev.com/301ecd231061729fff89eb9db3fd628e45d991a8/third_party/blink/renderer/core/frame/local_frame.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1151507?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053936)*
