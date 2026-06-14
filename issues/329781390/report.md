# security: Type confusion lead to use-after-poison in AuthenticationCredentialsContainer::store

| Field | Value |
|-------|-------|
| **Issue ID** | [329781390](https://issues.chromium.org/issues/329781390) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>DigitalCredentials |
| **Platforms** | Linux, Mac, Windows |
| **Chrome Version** | 122.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2024-03-15 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

repro.

1. host the poc.html python3 -m http.server 9999
2. apply the patch.diff and compile chrome then run chromium with flag `WebIdentityDigitalCredentials` `./Chromium --enable-features=WebIdentityDigitalCredentials`
3. navigate to <https://127.0.0.1:9999/poc.html>

# Problem Description

[0]. At function `AuthenticationCredentialsContainer::store`, three kinds of Credential are valid.
[1]. at here, to get the iconURL, credential will be cast to corresponding class ,but here not consider the case of credential is DigitalCredential, so it will be cast to `PasswordCredential*`, and lead to type confusion. even UAP.

```
ScriptPromiseTyped<Credential> AuthenticationCredentialsContainer::store(
    ScriptState* script_state,
    Credential* credential,
    ExceptionState& exception_state) {
  auto* resolver = MakeGarbageCollected<ScriptPromiseResolverTyped<Credential>>(
      script_state);
  auto promise = resolver->Promise();

  if (!(credential->IsFederatedCredential() ||
        credential->IsPasswordCredential() ||
        credential->IsDigitalCredential())) { // <----[0]
    resolver->Reject(MakeGarbageCollected<DOMException>(
        DOMExceptionCode::kNotSupportedError,
        "Store operation not permitted for this credential type."));
    return promise;
  }
  [...]
  const KURL& url =
      credential->IsFederatedCredential()  // <---[1] 
          ? static_cast<const FederatedCredential*>(credential)->iconURL()
          : static_cast<const PasswordCredential*>(credential)->iconURL();
  if (!IsIconURLNullOrSecure(url)) {
    resolver->Reject(MakeGarbageCollected<DOMException>(
        DOMExceptionCode::kSecurityError, "'iconURL' should be a secure URL"));
    return promise;
  }

 [...]
}

```

[0]. <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/authentication_credentials_container.cc;l=1599;drc=c292340f0c721cd88f9b14c453c877c55d13ce6b;bpv=0;bpt=1>
[1]. <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/credentialmanagement/authentication_credentials_container.cc;l=1619;drc=c292340f0c721cd88f9b14c453c877c55d13ce6b;bpv=0;bpt=1>

fix suggestion: consider the case of DigitalCredential. see fix.patch

biset: I40fc6fb01ebad2db6cdb9cddd27003767949fb9c. It has been three days without anyone noticing, and there is a high possibility of more days.

note: the patch.diff is to more easier to trigger bug. beacause once use `DigitalCredential` as param. it will trigger type confusion.

# Summary

security: Type confusion lead to use-after-poison in AuthenticationCredentialsContainer::store

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 15.8 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 714 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 629 B)
- [uap.md](attachments/uap.md) (text/markdown, 2.5 KB)
- [poc.html](attachments/poc.html) (text/html, 804 B)

## Timeline

### me...@google.com (2024-03-16)

Thanks for the report, I can reproduce it with the provided patch.

pkotwicz: Could you PTAL as the owner of I40fc6fb01ebad2db6cdb9cddd27003767949fb9c?

### pe...@google.com (2024-03-16)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-03-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### li...@gmail.com (2024-03-17)

notice: the patch is only for this point which type confusion, but i think better regress it.

```
 if (!(credential->IsFederatedCredential() ||
        credential->IsPasswordCredential() ||
-        credential->IsDigitalCredential())) {

```

### li...@gmail.com (2024-03-17)

Notice: The patch is only intended for addressing the type confusion issue at this specific point, but I believe that regression would be a better approach.

```
 if (!(credential->IsFederatedCredential() ||
        credential->IsPasswordCredential() ||
-        credential->IsDigitalCredential())) {

```

### li...@gmail.com (2024-03-17)

if u guys didn't want patch, also can use flags `./Chromium --enable-features=WebIdentityDigitalCredentials --use-fake-ui-for-digital-identity` to repro :)

### li...@gmail.com (2024-03-19)

friendly ping, the vulnerability exists for 7 days. Is anyone here to solve it?

### li...@gmail.com (2024-03-22)

hi,any update?

### li...@gmail.com (2024-03-27)

i found the vulnerability code still exists, can you take a look at it?

### ap...@google.com (2024-03-28)

Project: chromium/src
Branch: main

commit a3dd300be68031df896543dbb93797d6c9bd38f2
Author: Peter Kotwicz <pkotwicz@chromium.org>
Date:   Thu Mar 28 16:26:59 2024

    Reject store() operation for digital credentials
    
    This CL fixes a bug where store() operation was not rejected for
    digital credentials.
    
    BUG=329781390
    
    Change-Id: Ie49a58524c1fa5d67c01c808c4038bf97abf8489
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5405472
    Reviewed-by: Christian Biesinger <cbiesinger@chromium.org>
    Commit-Queue: Peter Kotwicz <pkotwicz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1279709}

M       third_party/blink/renderer/modules/credentialmanagement/authentication_credentials_container.cc

https://chromium-review.googlesource.com/5405472


### pe...@google.com (2024-03-29)

Requesting merge to beta (M124) because latest trunk commit (1279709) appears to be after beta branch point (1274542).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-03-29)

Merge review required: M124 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### am...@chromium.org (2024-03-29)

This issue specific to --WebIdentityDigitalCredentials, which is not enabled. I've updated this issue as SI-None, and removing the merge label accordingly since this is an unlaunched feature.

### am...@chromium.org (2024-03-29)

pkotwicz@, please let me know if RWI is going into OT in 124 and I can revisit this for merge review

### pe...@google.com (2024-03-30)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M124, which branched on 2024-03-18 (Chromium branch: 6367, Chromium branch position: 1274542)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

### li...@gmail.com (2024-03-31)

Notice: the changid `I40fc6fb01ebad2db6cdb9cddd27003767949fb9c` corresponds to commit `https://source.chromium.org/chromium/chromium/src/+/7566677fe2e20dfc808e812909c94450c865ab67`

### pk...@chromium.org (2024-04-02)

RWI is not going into OT in 124

### am...@google.com (2024-04-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-04)

Congratulations! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of memory corruption in a sandboxed process + $1,000 bisect bonus. A member of the Google p2p-vrp team will be in touch with you soon to arrange payment. In the mean time, please let us know what name or handle/tag you would like us to use in acknowledging you for this finding.

Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### li...@gmail.com (2024-04-05)

ok,got it ,very big thanks, just credit to `Lime with From TianGong Team of Legendsec at Qi'anxin Group`. btw, i want to ask whether the reward includes the `patch reward`. I think the fix is exactly the same as what i provided. (#6)

### li...@gmail.com (2024-04-22)

hi, nice day. So does this qualify for patch rewards?:)

### am...@chromium.org (2024-04-22)

It does not appear that the patch we used for this issue is the same as the patch that you provided, therefore, patch rewards would not be applicable here.

### li...@gmail.com (2024-04-22)

deleted

### li...@gmail.com (2024-04-22)

RE: #23 Okay,

Although #6 is not exactly the same, it means the best patch way, so it needs to be exactly the same, right? Thank you very much for your reply. :)

### am...@chromium.org (2024-04-22)

yes, patch rewards are only applicable when we absorb the same patch as provided. Attempts or patch suggestions that are not used in their entirety would not be eligible for a reward.

### pe...@google.com (2024-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/329781390)*
