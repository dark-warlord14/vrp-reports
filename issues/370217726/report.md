# UAF in SupervisedUserGoogleAuthNavigationThrottle::WillStartOrRedirectRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [370217726](https://issues.chromium.org/issues/370217726) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | FamilyExperiences>Browser |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | tj...@google.com |
| **Created** | 2024-09-29 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

On Android platform, when an unauthenticated supervised user tries to access some Google-owned sites, the SupervisedUserGoogleAuthNavigationThrottle would start a reauthentication process, as shown in the following call sequence:

```
SupervisedUserGoogleAuthNavigationThrottle::WillStartOrRedirectRequest
  -> SupervisedUserGoogleAuthNavigationThrottle::ShouldProceed
    -> ReauthenticateChildAccount

```

`ReauthenticateChildAccount` may run the `on_failure_callback` synchronously if the native view is not available [1]. The `on_failure_callback` is `SupervisedUserGoogleAuthNavigationThrottle::OnReauthenticationFailed`, and it will cancel the navigation which deletes the current running throttle object [2]. After `ShouldProceed` returns, the code would continue access some member variables which results in UAF [3].

Note that the UAF would be triggered only if `on_failure_callback` is invoked synchronously, as the code comment indicates, it may only happen on tab or browser shutdown. I did not find a way to stably destroy the view while keeping the throttle running (although it might exist), so feel free to downgrade the severity.

```
void ReauthenticateChildAccount(
    content::WebContents* web_contents,
    const std::string& email,
    const base::RepeatingCallback<void()>& on_failure_callback) {
  ui::WindowAndroid* window_android =
      web_contents->GetNativeView()->GetWindowAndroid();
  if (!window_android) {
    // The native view may not be available on shutdown (crbug.com/1468955).
    on_failure_callback.Run();      // ===> [1]
    return;
  }
  ...
}

void SupervisedUserGoogleAuthNavigationThrottle::OnReauthenticationFailed() {
  // Cancel the navigation if reauthentication failed.
  CancelDeferredNavigation(content::NavigationThrottle::CANCEL_AND_IGNORE);  // ===> [2]
}

content::NavigationThrottle::ThrottleCheckResult
SupervisedUserGoogleAuthNavigationThrottle::WillStartOrRedirectRequest() {
  // ...
  content::NavigationThrottle::ThrottleCheckResult result = ShouldProceed();

  if (result.action() == content::NavigationThrottle::DEFER) {
    google_auth_state_subscription_ =
        child_account_service_->ObserveGoogleAuthState(       // ===> [3]
            base::BindRepeating(&SupervisedUserGoogleAuthNavigationThrottle::
                                    OnGoogleAuthStateChanged,
                                base::Unretained(this)));
  }

  return result;
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/child_accounts/child_account_service_android.cc;l=35;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=244;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=100;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

**VERSION**

Chrome Version: stable + dev

Operating System: Android

**REPRODUCTION CASE**

1. Apply the attached patch.diff, this is to simulate an signed-in unauthenticated supervised user to Chromium
2. Run webserver using nodejs
   
   node server.js
   
   adb reverse tcp:8000 tcp:8000
3. Launch asan build chromium on Android
   
   out/Default/bin/chrome\_public\_apk run
   
   and navigate to <http://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser

Crash State: see asan.log for details

**Bisection**

This was introduced in <https://chromium.googlesource.com/chromium/src/+/b40c9c2acdd4b858053ee4d8988daeb412db4d04>

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 1.3 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 50.5 KB)
- [server.js](attachments/server.js) (text/javascript, 358 B)

## Timeline

### jt...@gmail.com (2024-09-29)

Re-upload server.js

### th...@chromium.org (2024-09-30)

Hi reporter, I'm not seeing a poc.html attached. I see that one of the attachments was deleted in the original description, perhaps that was it.

Could you please attach a poc.html?

### jt...@gmail.com (2024-10-01)

Re #3:

Thanks for the quick response. Requests for 'poc.html' in handled directly by the server.js so no file is needed.

### pe...@google.com (2024-10-01)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-10-01)

The NextAction date has arrived: 2024-10-01
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### th...@chromium.org (2024-10-01)

Ah my bad, thanks for clarifying. I have not been able to reproduce this (my own local build issues). Reporter, do you have any repro steps that don't require a local Android asan build with a patch?

For now, triaging speculatively based on the ASAN stack trace and bisect CL. Setting Found In to M128 extended stable based on bisect CL. Setting Severity to High (S1) since this is a UAF in the browser process but may only happen on tab or browser shutdown. Assigning to triploblastic@ based on bisect CL as well.

triploblastic@: Do you agree this UAF can be hit in some scenarios without the patch? (i.e. is the patch a valid way to trigger reproducing this?) If so, could you PTAL at this or re-triage as relevant?

### pe...@google.com (2024-10-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-10-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ri...@google.com (2024-10-11)

[secondary shepherd] [triploblastic@google.com](mailto:triploblastic@google.com), could you confirm that the UAF scenarios in c#7?

### fe...@google.com (2024-10-17)

Re-assigning to [tju@google.com](mailto:tju@google.com) who is currently looking into supervised user throttles.

### tj...@google.com (2024-10-17)

@triploblastic

Can you elaborate more on <https://chromium-review.googlesource.com/c/chromium/src/+/4793609>: what problem it was fixing, what was the intention of this fix and what will happen if this change should be simply reverted?

Is reverted state worse (crash) than the current state (UAF and security vulnerability)?

### tr...@google.com (2024-10-17)

Reverting the cl would cause null pointer crash as mentioned in this bug: https://crbug.com/40925127. We certainly don't want either. Should we move the null pointer check before the construction (code creating the object should make sure window_android is not null)?

Or maybe not call on_failure_callback when window android is null. I don't have enough domain knowledge to say if this is the correct approach.

### tj...@google.com (2024-10-17)

Ok. From security standpoint, crash is better option than UAF; but I'll take a look at the root cause instead (logically reverting the [crrev/c/4793609](https://crrev.com/c/4793609) fix)

### tj...@google.com (2024-10-23)

CancelDeferredNavigation from [2] can be only called for already deferred navigations, but it's not determined if that throttle's deferred before the value from ShouldProceed() is actually returned from the throttle framework (see documentation of [CancelDeferredNavigation](https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/navigation_throttle.h;l=230;drc=cf333fc2ab01e6d6ee9f0c0cf1bed033bd9439f1)). The observation that the problem is occurring in a synchronous call is the hint.

The original fix to nullptr introduced this problem by calling CancelDeferredNavigation from undeferred navigation. To correct this, the throttle must first defer, and only after, cancel that deferred navigation (or better, cancel synchronously).

I'm unsure about `web_contents` itself, I'm pretty sure that it can never be null, but in our codebase [there are instances](https://source.chromium.org/search?q=if%20%22!web_contents%22%20f:throttle) of a (possibly overly defensive) check against that. If that's the case, we'll keep having crashing binary; which should not be a security threat.

### ap...@google.com (2024-10-24)

Project: chromium/src  

Branch: main  

Author: Tomasz Jurkiewicz <[tju@google.com](mailto:tju@google.com)>  

Link:      <https://chromium-review.googlesource.com/5957688>

Fixes UAF caused by calling CancelDeferredNavigation from undeferred navigation.

---


Expand for full commit details
```
Fixes UAF caused by calling CancelDeferredNavigation from undeferred 
navigation. 
 
Leaves CHECKs to assure preconditions. 
 
Bug: 370217726, 40925127 
Change-Id: Ic15884aed8fa3c89491f4c325cc99f9404eb61ab 
Low-Coverage-Reason: HARD_TO_TEST Backlogged in 375383826 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5957688 
Reviewed-by: Tanmoy Mollik <triploblastic@google.com> 
Commit-Queue: Tomek Jurkiewicz <tju@google.com> 
Cr-Commit-Position: refs/heads/main@{#1373322}

```

---

Files:

- M `chrome/browser/supervised_user/child_accounts/child_account_service_android.cc`
- M `chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc`

---

Hash: 69b4f06529d87991e80468525ab9f0e35baf8903  

Date:  Thu Oct 24 15:01:22 2024


---

### tj...@google.com (2024-10-24)

This should be merged as far as possible.

The priority of this bug is P1 but was not requested by security team, so it's possible that the merge to 131 will be enough.

### pg...@google.com (2024-10-25)

Once the bug is marked as fixed, our automation will come and apply the proper merge labels for review! Please mark the bug as fixed if it was not reopened for further work :D

### pg...@google.com (2024-10-28)

(note that this is on my merge review queue - but the fix landed too close to the release cut that I will be reviewing this tomorrow for the following stable respin. thank you in advance for your patience!!)

### pg...@google.com (2024-10-29)

I do not see any relevant crashes on Canary after five days of data!

Merge approved for M130 - please merge to branch 6723 by Thursday Oct 31 EOD MTV time to get this fix into the next M130 respin!  

Merge approved for M131 - please merge to branch 6778 by Monday Nov 4th EOD MTV time to get this fix into the M131 release!

### ap...@google.com (2024-10-30)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Tomasz Jurkiewicz <[tju@google.com](mailto:tju@google.com)>  

Link:      <https://chromium-review.googlesource.com/5977583>

Fixes UAF caused by calling CancelDeferredNavigation from undeferred navigation.

---


Expand for full commit details
```
Fixes UAF caused by calling CancelDeferredNavigation from undeferred 
navigation. 
 
Leaves CHECKs to assure preconditions. 
 
(cherry picked from commit 69b4f06529d87991e80468525ab9f0e35baf8903) 
 
Bug: 370217726, 40925127 
Change-Id: Ic15884aed8fa3c89491f4c325cc99f9404eb61ab 
Low-Coverage-Reason: HARD_TO_TEST Backlogged in 375383826 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5957688 
Reviewed-by: Tanmoy Mollik <triploblastic@google.com> 
Commit-Queue: Tomek Jurkiewicz <tju@google.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1373322} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5977583 
Auto-Submit: Tomek Jurkiewicz <tju@google.com> 
Commit-Queue: Tanmoy Mollik <triploblastic@google.com> 
Cr-Commit-Position: refs/branch-heads/6723@{#1591} 
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `chrome/browser/supervised_user/child_accounts/child_account_service_android.cc`
- M `chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc`

---

Hash: 000b168f868e0417e360517206c5426a0fa511dd  

Date:  Wed Oct 30 14:51:41 2024


---

### ap...@google.com (2024-10-30)

Project: chromium/src  

Branch: refs/branch-heads/6778  

Author: Tomasz Jurkiewicz <[tju@google.com](mailto:tju@google.com)>  

Link:      <https://chromium-review.googlesource.com/5976327>

Fixes UAF caused by calling CancelDeferredNavigation from undeferred navigation.

---


Expand for full commit details
```
Fixes UAF caused by calling CancelDeferredNavigation from undeferred 
navigation. 
 
Leaves CHECKs to assure preconditions. 
 
(cherry picked from commit 69b4f06529d87991e80468525ab9f0e35baf8903) 
 
Bug: 370217726, 40925127 
Change-Id: Ic15884aed8fa3c89491f4c325cc99f9404eb61ab 
Low-Coverage-Reason: HARD_TO_TEST Backlogged in 375383826 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5957688 
Reviewed-by: Tanmoy Mollik <triploblastic@google.com> 
Commit-Queue: Tomek Jurkiewicz <tju@google.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1373322} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5976327 
Auto-Submit: Tomek Jurkiewicz <tju@google.com> 
Commit-Queue: Tanmoy Mollik <triploblastic@google.com> 
Cr-Commit-Position: refs/branch-heads/6778@{#1259} 
Cr-Branched-From: b21671ca172dcfd1566d41a770b2808e7fa7cd88-refs/heads/main@{#1368529}

```

---

Files:

- M `chrome/browser/supervised_user/child_accounts/child_account_service_android.cc`
- M `chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc`

---

Hash: a338155fec6effbb5c10c27e0ba66cf687de81c7  

Date:  Wed Oct 30 14:51:36 2024


---

### am...@chromium.org (2024-11-08)

Thank you for the report. In VRP assessment, it appears the patch introduces changes to test code in production, this doesn't appear to us to be exploitable in a real-world situation without the introduction of this specific patch. As such, we are unable to extend a VRP reward for this issue at this time.

If there anything we are missing or have asserted incorrectly here in terms of exploitability that would result in security implications to a user in a shipped, production version of Chrome, please let us know and we would be happy to reassess this issue for a VRP reward.

### jt...@gmail.com (2024-11-09)

Thank you for the response.

The patched test code is modified for stable reproduction, it sets `skip_jni_call_for_testing_` to true so that `SupervisedUserGoogleAuthNavigationThrottle::OnReauthenticationFailed` is runned synchronously by `SupervisedUserGoogleAuthNavigationThrottle::ShouldProceed`. In the production code, this function can be invoked at line [1] if the native view is not available (The `on_failure_callback` is `OnReauthenticationFailed`). The call sequence would be:

```
SupervisedUserGoogleAuthNavigationThrottle::ShouldProceed
 -> ReauthenticateChildAccount
  -> SupervisedUserGoogleAuthNavigationThrottle::OnReauthenticationFailed

```

It would be great if you can reassess this issue :)

```
void ReauthenticateChildAccount(
    content::WebContents* web_contents,
    const std::string& email,
    const base::RepeatingCallback<void()>& on_failure_callback) {
  ui::WindowAndroid* window_android =
      web_contents->GetNativeView()->GetWindowAndroid();
  if (!window_android) {
    // The native view may not be available on shutdown (crbug.com/1468955).
    on_failure_callback.Run();      // ===> [1]
    return;
  }
  ...
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/child_accounts/child_account_service_android.cc;l=35;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

### tj...@google.com (2024-11-09)

[amyressler@chromium.org](mailto:amyressler@chromium.org) - as stated in [#comment24](https://issues.chromium.org/issues/370217726#comment24), ReauthenticateChildAccount (with UAF or not) is reachable from the prod code - see the other branch of the `if` statement that is veryfying the `skip_jni_call_for_testing_` value.

### am...@chromium.org (2024-11-14)

Apologies, I didn't fully / accurately articulate the concern here, in terms of a real world exploitability, it was not clear if on\_failure\_callback is able to be invoked synchronously which would allow for the UAF to be triggered. Looking at the code, the patch seems to alter testing code in production to make this achievable. Could this be possible without the patch?

### jt...@gmail.com (2024-11-14)

Without the patch, the code goes to the statement following the `else` branch, which calls `ReauthenticateChildAccount` [1]. And the on\_failure\_callback would be invoked at line [2]. This requires the window object is not avaliable which I believe the issue([crbug.com/1468955](https://crbug.com/1468955)) in the code comment already provides evidence that it can be triggered in some race or shutdown cases.

```
if (skip_jni_call_for_testing_) {
  // Returns callback without JNI call for testing. Resets
  // has_shown_reauth_.
  base::BindRepeating(
      &SupervisedUserGoogleAuthNavigationThrottle::OnReauthenticationFailed,
      weak_ptr_factory_.GetWeakPtr())
      .Run();
} else {
  ReauthenticateChildAccount(               // <=== [1]
      web_contents, account_info.email,
      base::BindRepeating(&SupervisedUserGoogleAuthNavigationThrottle::
                              OnReauthenticationFailed,
                          weak_ptr_factory_.GetWeakPtr()));
}

void ReauthenticateChildAccount(
    content::WebContents* web_contents,
    const std::string& email,
    const base::RepeatingCallback<void()>& on_failure_callback) {
  ui::WindowAndroid* window_android =
      web_contents->GetNativeView()->GetWindowAndroid();
  if (!window_android) {
    // The native view may not be available on shutdown (crbug.com/1468955).
    on_failure_callback.Run();      // ===> [2]
    return;
  }

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=224;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/child_accounts/child_account_service_android.cc;l=35;drc=f522344e45882da4c7f7cb1b3a0a7bd747d654bb>

### tj...@google.com (2024-11-14)

It's maybe worth explaining when the `ShouldProceed()` method is called synchronously, because this was the root of the problem (throttle was calling `CancelDeferredNavigation` which is only allowed in asynchronous mode; throttle is in that mode after deferring). Synchronously means on the thread that is processing the request / redirect event.

This is possible exactly when upon processing a request or a redirect, the user is requesting [one of the special urls](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=94;drc=e1cbaa0450faaa8aba9c12ee04cbd8d213a628a4), [is not authenticated](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=144;drc=e1cbaa0450faaa8aba9c12ee04cbd8d213a628a4) and [is not already in the process of authentication](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=148;drc=e1cbaa0450faaa8aba9c12ee04cbd8d213a628a4).

If they were already in the process of authentication, the throttle flips to the deferred mode and then cancels deferred navigation (in order to show the reauth interstitial). But if somehow during processing the request (or redirect) the user gets into the unauthenticated mode, then the synchronous calls occur. The observation that such sequence is more probable in test environment is feasible and is definitely an edge case for actual prod environment, but I can't rule this out at this time. User's report proves that possibility.

As a side note, it's not obvious if the [condition that prevents multiple interstitial impressions](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_google_auth_navigation_throttle.cc;l=206;drc=e1cbaa0450faaa8aba9c12ee04cbd8d213a628a4) is needed at all (this condition is also guarding the code that caused the UAF / crash), but this is also outside of the scope of this problem (interstitials are definitely presented at least once).

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$4,000 for report of moderately mitigated memory corruption in a non-sandboxed process (by shutdown / race condition) + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Thank you both for the follow-up here. Upon review of the additional context, we have assessed this as eligible for a Chrome VRP reward. This does appear to be moderately mitigated by shutdown and/or race condition, therefore it was extended a rewarded based on that criteria.
Congratulations, thank you for your efforts here and reporting this issue to us.

### pe...@google.com (2025-02-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/370217726)*
