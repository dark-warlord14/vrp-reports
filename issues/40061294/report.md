# Security: Heap-use-after-free in SpeechRecognitionRecognizerImpl::ChangeLanguage

| Field | Value |
|-------|-------|
| **Issue ID** | [40061294](https://issues.chromium.org/issues/40061294) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Platforms** | Linux |
| **Reporter** | tt...@gmail.com |
| **Assignee** | ev...@google.com |
| **Created** | 2022-10-10 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1056826.zip and unzip
2. start a server in the folder of poc.html: `python -m SimpleHTTPServer 8605`
3. run `./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html --no-sandbox`
4. enable 'Live Caption', and reload the tab when downloading is done.

**Problem Description:**  

`--no-sandbox` is used to show the symbolized ASAN log, because the crash occurs in a Speech-related sandboxed process.

1. Analysis

This is a typical problem introduced by `Unretained(this)`[1], if we could delete `this` before the task is called, UAF occurs.  

We can easily trigger this problem with the help of Mojo JS, you could see the `poc.html` for more informations.

```
void SpeechRecognitionRecognizerImpl::ChangeLanguage(  
    const std::string& language,  
    scoped_refptr<base::SequencedTaskRunner> main_sequence) {  
  absl::optional<speech::SodaLanguagePackComponentConfig>  
      language_component_config = GetLanguageComponentConfig(language);  
  if (!language_component_config.has_value())  
    return;  
  
  // Only reset SODA if the language changed.  
  LanguageCode language_code = language_component_config.value().language_code;  
  if (language_code == language_ || language_code == LanguageCode::kNone)  
    return;  
  
  // Only change the language if the new language pack is installed.  
  base::FilePath config_path = GetLatestSodaLanguagePackDirectory(language);  
  if (base::PathExists(config_path)) {  
    config_path_ = config_path;  
    language_ = language_component_config.value().language_code;  
  
    // SODA must be reset on the same sequence where it's actively used in order  
    // to avoid race conditions.  
    main_sequence->PostTask(  
        FROM_HERE, base::BindOnce(&SpeechRecognitionRecognizerImpl::ResetSoda,    
                                  base::Unretained(this)));  // Unretaiend is not safe here  
  }  
}  

```

2. Similar UAF  
   
   Besides this `Unretained(this)`, there are another `Unretained(this)` in speech\_recognition\_recognizer\_impl.cc[2], which will also leads to UAF problem, considering they are very similar, so I submit them together.  
   
   You could trigger this UAF with the same POC, but this need a litte race. You should delete this before `SpeechRecognitionRecognizerImpl::ChangeLanguage` is called.

```
void SpeechRecognitionRecognizerImpl::OnLanguageChanged(  
    const std::string& language) {  
  if (!task_runner_) {  
    task_runner_ = base::ThreadPool::CreateSequencedTaskRunner(  
        {base::MayBlock(), base::TaskPriority::BEST_EFFORT,  
         base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN});  
  }  
  
  // Changing the language requires a blocking call to check if the language  
  // pack exists on the device.  
  scoped_refptr<base::SequencedTaskRunner> current_task_runner =  
      base::SequencedTaskRunnerHandle::Get();  
  task_runner_->PostTask(  
      FROM_HERE,  
      base::BindOnce(&SpeechRecognitionRecognizerImpl::ChangeLanguage,  
                     base::Unretained(this), language, current_task_runner));  // Another unsafe Unretained   
}  

```

3. Patch  
   
   I think the patch should use WeakPtr instead of Unretained ptr.

```
diff --git a/chrome/services/speech/speech_recognition_recognizer_impl.cc b/chrome/services/speech/speech_recognition_recognizer_impl.cc  
index cc780884d1818..92a3ad5e9bfce 100644  
--- a/chrome/services/speech/speech_recognition_recognizer_impl.cc  
+++ b/chrome/services/speech/speech_recognition_recognizer_impl.cc  
@@ -306,7 +306,8 @@ void SpeechRecognitionRecognizerImpl::OnLanguageChanged(  
   task_runner_->PostTask(  
       FROM_HERE,  
       base::BindOnce(&SpeechRecognitionRecognizerImpl::ChangeLanguage,  
-                     base::Unretained(this), language, current_task_runner));  
+                     //base::Unretained(this), language, current_task_runner));  
+                     weak_factory_.GetWeakPtr(), language, current_task_runner));  
 }  
   
 void SpeechRecognitionRecognizerImpl::ChangeLanguage(  
@@ -332,7 +333,8 @@ void SpeechRecognitionRecognizerImpl::ChangeLanguage(  
     // to avoid race conditions.  
     main_sequence->PostTask(  
         FROM_HERE, base::BindOnce(&SpeechRecognitionRecognizerImpl::ResetSoda,  
-                                  base::Unretained(this)));  
+                                  //base::Unretained(this)));  
+                                  weak_factory_.GetWeakPtr()));  
   }  
 }  
  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/speech/speech_recognition_recognizer_impl.cc;l=335;drc=fbc3354d74d631da1294268781848f2b1ca43fd5;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/services/speech/speech_recognition_recognizer_impl.cc;l=309;drc=fbc3354d74d631da1294268781848f2b1ca43fd5;bpv=0;bpt=0>

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 26.2 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 573.5 KB)

## Timeline

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-10)

Setting Severity high because of UAF in sandboxed process. FoundIn set to M106 based on commit date of [1] (see codelink in problem description).

[Monorail components: Blink>Speech]

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1518d96971b30d08562ea3b5af8dad86cebf3892

commit 1518d96971b30d08562ea3b5af8dad86cebf3892
Author: evliu <evliu@google.com>
Date: Wed Oct 12 23:19:11 2022

Address potential use-after-free vulnerabilities in speech_recognition_recognizer_impl.cc

This CL addresses potential UAF vulnerabilities in
speech_recognition_recognizer_impl.cc that may be exploited by a
compromised renderer.

Bug: 1372999
Change-Id: I6359914ca35152860ca5b638f8ff9e2abab92040
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3943895
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Evan Liu <evliu@google.com>
Cr-Commit-Position: refs/heads/main@{#1058357}

[modify] https://crrev.com/1518d96971b30d08562ea3b5af8dad86cebf3892/chrome/services/speech/speech_recognition_recognizer_impl.cc
[modify] https://crrev.com/1518d96971b30d08562ea3b5af8dad86cebf3892/chrome/services/speech/speech_recognition_recognizer_impl.h
[modify] https://crrev.com/1518d96971b30d08562ea3b5af8dad86cebf3892/chrome/browser/speech/speech_recognition_service_browsertest.cc


### ev...@google.com (2022-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-13)

Requesting merge to stable M106 because latest trunk commit (1058357) appears to be after stable branch point (1036826).

Requesting merge to beta M107 because latest trunk commit (1058357) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-13)

Merge review required: M107 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-13)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ev...@google.com (2022-10-17)

1. Why does your merge fit within the merge criteria for these milestones?
Security bug.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3943895

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
N/A


### ev...@google.com (2022-10-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-19)

Hi evliu@ -- thanks so much for fixing this issue so quickly as well as updating the merge questionnaire. This issue is definitely in the security merge review queue. However the timing of the fix landing did not allow for sufficient bake time to allow this fix to be included in 107/stable cut. So merge review was deferred for that reason. Unfortunately, we'll have to defer a bit further as while stable cut/107 has occurred for desktop platform, Android stable cut for 107 is occurring tomorrow or Friday. I can't approve this now or the fix would be included in one platform and not the others. 
We'll need to revisit this for merge approval early next week until after stable and extended cut for all platforms has occurred.

### am...@google.com (2022-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-20)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-31)

okay, at last :) 
107/stable and 106/extended merge approved, please merge this fix to branches 5304 and 5249 respectively before 11am PST Friday, 4 November so this fix can be included in the next 107/stable and 106/extended security respins -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fa330f88adb728bc987338d480aba06cd1e5ebf4

commit fa330f88adb728bc987338d480aba06cd1e5ebf4
Author: evliu <evliu@google.com>
Date: Tue Nov 01 20:33:27 2022

[Merge to M107] Address potential use-after-free vulnerabilities in speech_recognition_recognizer_impl.cc

This CL addresses potential UAF vulnerabilities in
speech_recognition_recognizer_impl.cc that may be exploited by a
compromised renderer.

(cherry picked from commit 1518d96971b30d08562ea3b5af8dad86cebf3892)

Bug: 1372999
Change-Id: I6359914ca35152860ca5b638f8ff9e2abab92040
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3943895
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Evan Liu <evliu@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1058357}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3997571
Cr-Commit-Position: refs/branch-heads/5304@{#1144}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/fa330f88adb728bc987338d480aba06cd1e5ebf4/chrome/services/speech/speech_recognition_recognizer_impl.cc
[modify] https://crrev.com/fa330f88adb728bc987338d480aba06cd1e5ebf4/chrome/services/speech/speech_recognition_recognizer_impl.h


### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3d6dc9afe728c01fd6c78be9a1bff0fd1b63086d

commit 3d6dc9afe728c01fd6c78be9a1bff0fd1b63086d
Author: evliu <evliu@google.com>
Date: Tue Nov 01 20:44:58 2022

[Merge to M106] Address potential use-after-free vulnerabilities in speech_recognition_recognizer_impl.cc

This CL addresses potential UAF vulnerabilities in
speech_recognition_recognizer_impl.cc that may be exploited by a
compromised renderer.

(cherry picked from commit 1518d96971b30d08562ea3b5af8dad86cebf3892)

Bug: 1372999
Change-Id: I6359914ca35152860ca5b638f8ff9e2abab92040
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3943895
Reviewed-by: Frank Liberato <liberato@chromium.org>
Commit-Queue: Evan Liu <evliu@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1058357}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3995411
Cr-Commit-Position: refs/branch-heads/5249@{#897}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/3d6dc9afe728c01fd6c78be9a1bff0fd1b63086d/chrome/services/speech/speech_recognition_recognizer_impl.cc
[modify] https://crrev.com/3d6dc9afe728c01fd6c78be9a1bff0fd1b63086d/chrome/services/speech/speech_recognition_recognizer_impl.h


### am...@chromium.org (2022-11-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1372999?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061294)*
