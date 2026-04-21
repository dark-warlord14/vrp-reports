# Security:  type confusion  in chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40060083](https://issues.chromium.org/issues/40060083) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>SharedStorage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2022-06-27 |
| **Bounty** | $8,500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**  

all

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [test.log](attachments/test.log) (text/plain, 12.5 KB)
- [test.js](attachments/test.js) (text/plain, 91 B)
- [test.html](attachments/test.html) (text/plain, 113 B)
- [0001-trigger-type-confusion.patch](attachments/0001-trigger-type-confusion.patch) (text/plain, 1.3 KB)
- [0001-fix-type-confusion.patch](attachments/0001-fix-type-confusion.patch) (text/plain, 1.4 KB)

## Timeline

### [Deleted User] (2022-06-27)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-06-27)

https://source.chromium.org/chromium/chromium/src/+/main:content/services/shared_storage_worklet/shared_storage_worklet_global_scope.cc;l=220
```
  v8::Local<v8::Value> class_prototype =
      class_definition->Get(context, gin::StringToV8(isolate, "prototype"))
          .ToLocalChecked();

  v8::Local<v8::Value> run_function =
      class_prototype.As<v8::Object>().   //here don't check its type , we can use number to cause type confusion
          ->Get(context, gin::StringToV8(isolate, "run"))
          .ToLocalChecked();

```


https://developer.chrome.com/docs/privacy-sandbox/shared-storage/#try-the-shared-storage-api

you should enable chrome://flags/#privacy-sandbox-ads-apis

then visit test.html should cause check.

this is my command line
```
out/asan/Chromium.app/Contents/MacOS/Chromium --no-sandbox --enable-features=PrivacySandboxAdsAPIsOverride,InterestGroupStorage,Fledge,BiddingAndScoringDebugReportingAPI,AllowURNsInIframes,BrowsingTopics,ConversionMeasurement,FencedFrames,OverridePrivacySandboxSettingsLocalTesting,SharedStorageAPI --js-flags="-expose-gc --allow-natives-syntax" --no-sandbox --enable-blink-test-features http://127.0.0.1:8000/test.html
```



### wx...@gmail.com (2022-06-27)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-27)

I'm not able to repro on Windows asan - which commit are you basing your patch off?

### aj...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### wx...@gmail.com (2022-06-28)

You should use the debug asan chromium version after 2022-06-16.

### [Deleted User] (2022-06-28)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2022-06-28)

my chromium commit is eca4595293e0eb98a3650b4b6c1af29cda4f97cf

### ca...@chromium.org (2022-06-30)

I was able to reproduce on ToT in linux. This also reproduces in non-asan. Setting Impact-None since this requires non-default flags, but otherwise triaging as a high severity bug.

yaoxia and cammie: Could you help further triage this bug, and reassign as appropriate? Thanks

[Monorail components: Blink>Storage>SharedStorage]

### ya...@chromium.org (2022-06-30)

Thanks for reporting the bug. I can confirm that this bug exist, although it’ll only show up in non-default build (e.g. dcheck-on). Given this, I think it’s fine to just fix it in ToT, and it should be fine to skip merging back to M104. The fix is out for review: https://chromium-review.googlesource.com/c/chromium/src/+/3735330

### wx...@gmail.com (2022-06-30)

good  fix:)

### gi...@appspot.gserviceaccount.com (2022-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b64a4ff2d48a75bcbb678c57ca5b62448e16a102

commit b64a4ff2d48a75bcbb678c57ca5b62448e16a102
Author: Yao Xiao <yaoxia@chromium.org>
Date: Thu Jun 30 16:46:40 2022

[shared storage] throw an error when !class_prototype->IsObject()

Otherwise, it could crash the renderer when there's a type confusion.

Bug: 1339741
Change-Id: I4c63cdaf704cf92ddfb9898d59226f5b506be955
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3735330
Reviewed-by: Alex Gough <ajgo@chromium.org>
Commit-Queue: Yao Xiao <yaoxia@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019684}

[modify] https://crrev.com/b64a4ff2d48a75bcbb678c57ca5b62448e16a102/content/services/shared_storage_worklet/shared_storage_worklet_global_scope_unittest.cc
[modify] https://crrev.com/b64a4ff2d48a75bcbb678c57ca5b62448e16a102/content/services/shared_storage_worklet/shared_storage_worklet_global_scope.cc


### ya...@chromium.org (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations! the VRP Panel has decided to award you $8,500 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-06)

This issue was migrated from crbug.com/chromium/1339741?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060083)*
