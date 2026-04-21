# Security: UAF in DigitalCredentialProviderAndroid

| Field | Value |
|-------|-------|
| **Issue ID** | [40940815](https://issues.chromium.org/issues/40940815) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | rb...@chromium.org |
| **Created** | 2023-11-08 |
| **Bounty** | $37,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using JS API `navigator.credentials.get()` to query digital credentials, it calls FederatedAuthRequestImpl::RequestToken and creates DigitalCredentialProvider object at line[1]. On Android platform, it also creates a Java object DigitalCredentialProvider in the constructor of class DigitalCredentialProviderAndroid [2]. DigitalCredentialProvider holds a raw pointer which points to DigitalCredentialProviderAndroid and uses it to call native functions through JNI [3]. This pointer does not get cleared even after the DigitalCredentialProviderAndroid is destroyed, which leads to UAF if we:

1. query digital credentials by calling `navigator.credentials.get()` in an iframe
2. close the iframe before the query gets response, thus destroy FederatedAuthRequestImpl and DigitalCredentialProviderAndroid subsequently
3. query is resolved async and will access the already freed DigitalCredentialProviderAndroid through JIN call

```
void FederatedAuthRequestImpl::RequestToken(  
    std::vector<IdentityProviderGetParametersPtr> idp_get_params_ptrs,  
    MediationRequirement requirement,  
    RequestTokenCallback callback) {  
    // ...  
    if (!digital_credential_provider_) {  
      digital_credential_provider_ = CreateDigitalCredentialProvider();  // ===> [1]  
    }  
  
  
DigitalCredentialProviderAndroid::DigitalCredentialProviderAndroid() {  
  JNIEnv\* env = AttachCurrentThread();  
  j_digital_credential_provider_android_.Reset(  
      Java_DigitalCredentialProvider_create(env,  // ===> [2]  
                                            reinterpret_cast<intptr_t>(this)));  
}  
  
  
@CalledByNative  
void requestDigitalCredential(WindowAndroid window, String origin, String request) {  
    sCredentials  
            .get(window.getActivity().get(), origin, request)  
            .then(  
                    data -> {  
                        DigitalCredentialProviderJni.get()  // ===> [3]  
                                .onReceive(mDigitalCredentialProvider, new String(data));  
                    },  
                    e -> {  
                        DigitalCredentialProviderJni.get().onError(mDigitalCredentialProvider);  
                    });  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=683;drc=c6239d599e27bb680984bd6e86e69321b3fe5a9d>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/digital_credentials/digital_credential_provider_android.cc;l=27;drc=c6239d599e27bb680984bd6e86e69321b3fe5a9d>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/public/android/java/src/org/chromium/content/browser/webid/DigitalCredentialProvider.java;l=52-58;drc=c6239d599e27bb680984bd6e86e69321b3fe5a9d>

**VERSION**  

Chrome Version: beta + dev  

Operating System: Android

**REPRODUCTION CASE**

1. Setup a local HTTP server  
   
   python -m SimpleHTTPServer 8000
2. Create a port forwarding from Android device to the local machine  
   
   adb reverse tcp:8000 tcp:8000
3. Run following command to launch asan build chrome on Android  
   
   out/Asan/bin/chrome\_public\_apk run --args='--enable-features=UserMediaScreenCapturing'  
   
   and navigate to <http://localhost:8000/poc.html>

Note that this bug can be triggered without a compromised renderer.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log

== Bisection ==  

This was introduces in <https://chromium.googlesource.com/chromium/src/+/a87ff580ed0b1c0f37b7dc438b335ca2845fcb0f>

== Fix suggestion ==  

Notify the Java side when DigitalCredentialProviderAndroid is destroyed and validate the raw pointer before using it, see fix.diff for details, hope it helps :)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 991 B)
- [asan.log](attachments/asan.log) (text/plain, 24.1 KB)
- [fix.diff](attachments/fix.diff) (text/plain, 2.2 KB)

## Timeline

### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### jt...@gmail.com (2023-11-08)

Sorry for the wrong command line in reproduction step 3, it should be
out/Asan/bin/chrome_public_apk run --args='--enable-features=WebIdentityDigitalCredentials'

### es...@chromium.org (2023-11-09)

Thanks for the report. I'm going to run this through Clusterfuzz, but directly cc'ing goto@ too since this is a high-quality credible report.

[Monorail components: Blink>Identity>FedCM]

### cl...@chromium.org (2023-11-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5185839114420224.

### np...@chromium.org (2023-11-09)

Marking P1 since report says UAF.

### es...@chromium.org (2023-11-09)

Reproduced in M120. Sam, can you PTAL? Also, can you please confirm that WebIdentityDigitalCredentials isn't enabled for any users (unless they manually flip the flag)? Based on that I'm setting this to Severity_Imapct-None.

### an...@chromium.org (2023-11-28)

[security shepherd]: Hi Sam! Just following up to see if you have had the chance to take a look? Can you confirm that WebIdentityDigitalCredentials is still a flag-enabled feature only? Thanks!

### yi...@chromium.org (2023-11-28)

yes it's still behind a flag

### an...@chromium.org (2023-11-28)

yigu@, thanks for confirming! So the Security_Impact-None is valid. Is there a feature bug that we can block w/ this bug? 

### yi...@chromium.org (2023-11-28)

blocking https://crbug.com/chromium/1416939

### rb...@chromium.org (2023-11-30)

Thanks for the great report and suggested fix! I'm working with Sam on this API, I can take this.

### jt...@gmail.com (2023-12-12)

Friendly ping. Seems like the fix CL [1] remains pending for a while.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/5075918

### am...@chromium.org (2023-12-19)

Hi, thanks for reaching out. A lot of folks are taking some time off right now since this winter festive season and end of year. Since this issue is SI-None, it's not likely to be completed until January. 

### rb...@chromium.org (2023-12-19)

Sorry for the delay, got distracted by other things and yeah we're not turning this flag on anytime soon so not urgent. But I finally made time today to reproduce the crash before the fix (even without ASAN it crashes reliably) and verify the fix does indeed address the issue. So will land the fix now.

### gi...@appspot.gserviceaccount.com (2023-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/557b7d4a4d681aafeeaf9ee3fb5950c3ba8b1b7a

commit 557b7d4a4d681aafeeaf9ee3fb5950c3ba8b1b7a
Author: Rick Byers <rbyers@chromium.org>
Date: Tue Dec 19 16:52:52 2023

Fix UaF in DigitalCredential code

This feature is still only behind a flag.
Credit to jtrrodant@gmail.com for finding the issue and suggesting the fix.

Bug: 1500565
Change-Id: I3005b59de49421fe931f2a4ec95ef54b2b557fc7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5075918
Commit-Queue: Rick Byers <rbyers@chromium.org>
Reviewed-by: Yi Gu <yigu@chromium.org>
Reviewed-by: Sam Goto <goto@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1239192}

[modify] https://crrev.com/557b7d4a4d681aafeeaf9ee3fb5950c3ba8b1b7a/content/public/android/java/src/org/chromium/content/browser/webid/DigitalCredentialProvider.java


### rb...@chromium.org (2023-12-19)

[Empty comment from Monorail migration]

### rb...@chromium.org (2023-12-19)

In case it's helpful for anyone else, I'm hosting the repro at https://rbyers.github.io/bug1500565-poc.html


### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-26)

ClusterFuzz testcase 5185839114420224 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations Rong! The Chrome VRP Panel has decided to award you $37,000 for this report (memory corruption in the browser process + renderer RCE bonus since a compromised renderer was not needed) + $1,000 patch bonus. Thank you for your efforts and reporting this issue to us -- excellent work! Happy New Year! 

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/1500565?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1416939]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-25)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40940815)*
