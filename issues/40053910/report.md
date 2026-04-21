# Security: OOBW in the icu_68::FormattedStringBuilder::insert 

| Field | Value |
|-------|-------|
| **Issue ID** | [40053910](https://issues.chromium.org/issues/40053910) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ft...@chromium.org |
| **Created** | 2020-11-18 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

OOBW in the icu\_68::FormattedStringBuilder::insert

**VERSION**  

Chrome Version: the latest chromium dev version  

$ git branch -v  

\* master 35e3b12b95

**REPRODUCTION CASE**

Windows 10 20H2 (32GB RAM)  

The OS memory must be more than 16GB to reproduce this case.

Open the poc.html in the browser

$ chrome.exe --no-sandbox poc.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Asan log:

# C:\chromium\_source\_code\chromium\src\out\asan>chrome.exe --no-sandbox [14796:7336:1118/145417.342:ERROR:device\_event\_log\_impl.cc(211)] [14:54:17.343] Bluetooth: bluetooth\_adapter\_winrt.cc:1072 Getting Default Adapter failed.

==13828==ERROR: AddressSanitizer: access-violation on unknown address 0x122c28e51812 (pc 0x7ffbd9498ab3 bp 0xffffffff80040009 sp 0x00700c5fd7a0 T0)  

==13828==The signal is caused by a WRITE memory access.  

==13828==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==13828==\*\*\* Most likely this means that the app is already \*\*\*  

==13828==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==13828==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==13828==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffbd9498ab2 in icu\_68::FormattedStringBuilder::insert C:\chromium\_source\_code\chromium\src\third\_party\icu\source\i18n\formatted\_string\_builder.cpp:188  

#1 0x7ffbd9498887 in icu\_68::FormattedStringBuilder::insert C:\chromium\_source\_code\chromium\src\third\_party\icu\source\i18n\formatted\_string\_builder.cpp:175  

#2 0x7ffbd6e8ee83 in icu\_68::`anonymous namespace'::FormattedListBuilder::append C:\chromium_source_code\chromium\src\third_party\icu\source\i18n\listformatter.cpp:598 #3 0x7ffbd6e8e296 in icu_68::ListFormatter::formatStringsToValue C:\chromium_source_code\chromium\src\third_party\icu\source\i18n\listformatter.cpp:717 #4 0x7ffbd3c1b05d in v8::internal::JSListFormat::FormatList C:\chromium_source_code\chromium\src\v8\src\objects\js-list-format.cc:294 #5 0x7ffbd41dbe82 in v8::internal::Runtime_FormatList C:\chromium_source_code\chromium\src\v8\src\runtime\runtime-intl.cc:36 #6 0x7ffbd54f0dbb in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x3b (C:\chromium_source_code\chromium\src\out\asan\chrome.dll+0x1881f0dbb) #7 0x7ffbd556acc0 in Builtins_ListFormatPrototypeFormat+0x80 (C:\chromium_source_code\chromium\src\out\asan\chrome.dll+0x18826acc0) #8 0x7ffbd548a7ce in Builtins_InterpreterEntryTrampoline+0xce (C:\chromium_source_code\chromium\src\out\asan\chrome.dll+0x18818a7ce) #9 0x7ffbd548841a in Builtins_JSEntryTrampoline+0x5a (C:\chromium_source_code\chromium\src\out\asan\chrome.dll+0x18818841a) #10 0x7ffbd548806b in Builtins_JSEntry+0xcb (C:\chromium_source_code\chromium\src\out\asan\chrome.dll+0x18818806b) #11 0x7ffbd33eaba2 in v8::internal::`anonymous namespace'::Invoke C:\chromium\_source\_code\chromium\src\v8\src\execution\execution.cc:368  

#12 0x7ffbd33e99bd in v8::internal::Execution::Call C:\chromium\_source\_code\chromium\src\v8\src\execution\execution.cc:462  

#13 0x7ffbd2f828c1 in v8::Script::Run C:\chromium\_source\_code\chromium\src\v8\src\api\api.cc:2129  

#14 0x7ffbdb060f9c in blink::V8ScriptRunner::RunCompiledScript C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:365  

#15 0x7ffbdb0626de in blink::V8ScriptRunner::CompileAndRunScript C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:443  

#16 0x7ffbdb050b23 in blink::ScriptController::ExecuteScriptAndReturnValue C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\bindings\core\v8\script\_controller.cc:99  

#17 0x7ffbdb053d3d in blink::ScriptController::EvaluateScriptInMainWorld C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\bindings\core\v8\script\_controller.cc:297  

#18 0x7ffbdb04de52 in blink::ClassicScript::RunScript C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\script\classic\_script.cc:29  

#19 0x7ffbe3fb7032 in blink::PendingScript::ExecuteScriptBlockInternal C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\script\pending\_script.cc:264  

#20 0x7ffbe3fb67db in blink::PendingScript::ExecuteScriptBlock C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\script\pending\_script.cc:170  

#21 0x7ffbe1e94326 in blink::ScriptLoader::PrepareScript C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\script\script\_loader.cc:915  

#22 0x7ffbe1de07b0 in blink::HTMLParserScriptRunner::ProcessScriptElementInternal C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\script\html\_parser\_script\_runner.cc:609  

#23 0x7ffbe1de0384 in blink::HTMLParserScriptRunner::ProcessScriptElement C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\script\html\_parser\_script\_runner.cc:332  

#24 0x7ffbde357a3a in blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:595  

#25 0x7ffbde35b905 in blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:836  

#26 0x7ffbde35722b in blink::HTMLDocumentParser::PumpPendingSpeculations C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:896  

#27 0x7ffbde356adf in blink::HTMLDocumentParser::ResumeParsingAfterYield C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:582  

#28 0x7ffbd59a337a in blink::TaskHandle::Runner::Run C:\chromium\_source\_code\chromium\src\third\_party\blink\renderer\platform\scheduler\common\post\_cancellable\_task.cc:47  

#29 0x7ffbd698d47f in base::TaskAnnotator::RunTask C:\chromium\_source\_code\chromium\src\base\task\common\task\_annotator.cc:163  

#30 0x7ffbd8f22bc9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\chromium\_source\_code\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#31 0x7ffbd8f221a9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\chromium\_source\_code\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264  

#32 0x7ffbd8ef1e23 in base::MessagePumpDefault::Run C:\chromium\_source\_code\chromium\src\base\message\_loop\message\_pump\_default.cc:39  

#33 0x7ffbd8f2508f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\chromium\_source\_code\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460  

#34 0x7ffbd6941d85 in base::RunLoop::Run C:\chromium\_source\_code\chromium\src\base\run\_loop.cc:124  

#35 0x7ffbd8d274f7 in content::RendererMain C:\chromium\_source\_code\chromium\src\content\renderer\renderer\_main.cc:256  

#36 0x7ffbd6706576 in content::ContentMainRunnerImpl::Run C:\chromium\_source\_code\chromium\src\content\app\content\_main\_runner\_impl.cc:884  

#37 0x7ffbd67033b3 in content::RunContentProcess C:\chromium\_source\_code\chromium\src\content\app\content\_main.cc:372  

#38 0x7ffbd6703987 in content::ContentMain C:\chromium\_source\_code\chromium\src\content\app\content\_main.cc:398  

#39 0x7ffbcd30145a in ChromeMain C:\chromium\_source\_code\chromium\src\chrome\app\chrome\_main.cc:130  

#40 0x7ff6d5225bbf in MainDllLoader::Launch C:\chromium\_source\_code\chromium\src\chrome\app\main\_dll\_loader\_win.cc:169  

#41 0x7ff6d52229b7 in main C:\chromium\_source\_code\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:345  

#42 0x7ff6d55febff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#43 0x7ffc93d67033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#44 0x7ffc94e5cec0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cec0)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\chromium\_source\_code\chromium\src\third\_party\icu\source\i18n\formatted\_string\_builder.cpp:188 in icu\_68::FormattedStringBuilder::insert  

==13828==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 125 B)

## Timeline

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-11-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5066776636620800.

### mb...@chromium.org (2020-11-19)

ftang: Would you mind taking a look at this? I've tentatively set this to Security_Impact-Head, but if you think stable or beta are affected we should update this.

[Monorail components: Blink>JavaScript>Internationalization]

### ft...@chromium.org (2020-11-19)

[Empty comment from Monorail migration]

### ft...@chromium.org (2020-11-20)

[Empty comment from Monorail migration]

### ft...@chromium.org (2020-11-20)

fix in https://github.com/unicode-org/icu/pull/1479



### ft...@chromium.org (2020-11-20)

int32_t overflow. ICU test env has memory allocation fail and cause the int32_t overflow issue got shadow and not caught. In V8/chrome the memory allocation succeed and then the int32_t overflow became negative index and cause crash. We should request merge into 88. This is part of ICU68 new code just landed before branching 88 so we do not need to worry about 87. 

### [Deleted User] (2020-11-21)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu.git/+/3bf08c6a50f77921ae79d4e715b580b959e494c7

commit 3bf08c6a50f77921ae79d4e715b580b959e494c7
Author: Frank Tang <ftang@chromium.org>
Date: Mon Nov 23 19:48:07 2020

Fix crash inside list format security bug

TBR=jshin@chromium.org
Bug: chromium:1150371
Change-Id: I5fb7aa071fb70e9edf0169b093a90f6a4e2b1eb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2555722
Reviewed-by: Frank Tang <ftang@chromium.org>

[modify] https://crrev.com/3bf08c6a50f77921ae79d4e715b580b959e494c7/README.chromium
[add] https://crrev.com/3bf08c6a50f77921ae79d4e715b580b959e494c7/patches/formatted_string_builder.patch
[modify] https://crrev.com/3bf08c6a50f77921ae79d4e715b580b959e494c7/source/i18n/formatted_string_builder.cpp


### ft...@chromium.org (2020-11-23)

verifying the fix in https://chromium-review.googlesource.com/c/v8/v8/+/2551212
and once the trybot show it pass I will land https://chromium-review.googlesource.com/c/chromium/src/+/2555661

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/308a9ad195166fdec288d2fb6b626d06fcab9390

commit 308a9ad195166fdec288d2fb6b626d06fcab9390
Author: Frank Tang <ftang@chromium.org>
Date: Mon Nov 23 23:15:49 2020

Roll ICU to fix ListFormat security bug

https://chromium.googlesource.com/chromium/deps/icu.git/+log/7db579a7..6a33b647c

Test to verify the fix inside v8 is in
https://chromium-review.googlesource.com/c/v8/v8/+/2551212

TBR=jshin@chromium.org

Bug: chromium:1150371
Change-Id: I3b372ac27848cd962a2987ecbb354e4fcd95871f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2555661
Reviewed-by: Frank Tang <ftang@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#830351}

[modify] https://crrev.com/308a9ad195166fdec288d2fb6b626d06fcab9390/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1341dbd2096b230129464fe244c46301eaf8dfea

commit 1341dbd2096b230129464fe244c46301eaf8dfea
Author: Frank Tang <ftang@chromium.org>
Date: Tue Nov 24 09:37:50 2020

[int] Fix security bug in Intl.ListFormat

Also add test to ensure it won't crash. The crash is caused by int32_t overflow inside ICU68-1

Real fix in https://chromium.googlesource.com/chromium/deps/icu/+/3bf08c6a50f77921ae79d4e715b580b959e494c7

Bug: chromium:1150371
Change-Id: I71c7bb3c50453fe3fa40226cab83bee0d865b0f0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2551212
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71357}

[add] https://crrev.com/1341dbd2096b230129464fe244c46301eaf8dfea/test/intl/regress-1150371.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f3b77a2ac96945b5c8b0082478df4afff71cc288

commit f3b77a2ac96945b5c8b0082478df4afff71cc288
Author: Maya Lekova <mslekova@chromium.org>
Date: Tue Nov 24 11:04:31 2020

Revert "[int] Fix security bug in Intl.ListFormat"

This reverts commit 1341dbd2096b230129464fe244c46301eaf8dfea.

Reason for revert: The new test is failing on arm64 simulator MSAN - https://ci.chromium.org/p/v8/builders/ci/V8%20Linux%20-%20arm64%20-%20sim%20-%20MSAN/35559

Original change's description:
> [int] Fix security bug in Intl.ListFormat
>
> Also add test to ensure it won't crash. The crash is caused by int32_t overflow inside ICU68-1
>
> Real fix in https://chromium.googlesource.com/chromium/deps/icu/+/3bf08c6a50f77921ae79d4e715b580b959e494c7
>
> Bug: chromium:1150371
> Change-Id: I71c7bb3c50453fe3fa40226cab83bee0d865b0f0
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2551212
> Reviewed-by: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Michael Achenbach <machenbach@chromium.org>
> Commit-Queue: Frank Tang <ftang@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#71357}

TBR=jkummerow@chromium.org,machenbach@chromium.org,ftang@chromium.org,syg@chromium.org

Change-Id: I10862ad1fb308d1610b8f7a80cca43c010475397
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1150371
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2557512
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71362}

[delete] https://crrev.com/c343c06d5aff5390149fd0ecae7c1de66767c2a6/test/intl/regress-1150371.js


### ft...@chromium.org (2020-11-25)

the above got reverted is just the test which cause issue because the test itself need to allocate a lot of memory and therefore flaky

### ft...@chromium.org (2020-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-25)

This release blocking issue appears to be targeted for M88, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after November 12 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-88 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-11-27)

ftang@ can you please confirm that no merge to M88 is needed. If so please remove the Merge-TBD label. Thanks!

### sr...@google.com (2020-11-30)

friendly ping ^ ftang@

### ft...@chromium.org (2020-11-30)

no, we should merge into 88, I was waiting for the daily build to verify before I put in the Merge-Request-88 request

### [Deleted User] (2020-11-30)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2020-11-30)


1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
> YES

2. Links to the CLs you are requesting to merge.

Just https://chromium-review.googlesource.com/c/chromium/src/+/2555661
which only has the changes in https://chromium.googlesource.com/chromium/deps/icu.git/+log/7db579a7..6a33b647c

3. Has the change landed and been verified on ToT?
YES

4. Does this change need to be merged into other active release branches (M-1, M+1)?
NO. The bug is introduced by ICU68 and we land ICU68 into only m88, m87 is on ICU67 and does not have this bug.

5. Why are these changes required in this milestone after branch?
Security concern

6. Is this a new feature?
NO

7. If it is a new feature, is it behind a flag using finch?
N/A

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents
N/A

### sr...@google.com (2020-11-30)

merge approved for m88 branch:4324 please merge asap

### ft...@chromium.org (2020-11-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ea9cfd6db8715ef8024def8388c83c80ee5ed016

commit ea9cfd6db8715ef8024def8388c83c80ee5ed016
Author: Frank Tang <ftang@chromium.org>
Date: Mon Nov 30 18:19:40 2020

Roll ICU to fix ListFormat security bug

https://chromium.googlesource.com/chromium/deps/icu.git/+log/7db579a7..6a33b647c

Test to verify the fix inside v8 is in
https://chromium-review.googlesource.com/c/v8/v8/+/2551212

TBR=jshin@chromium.org

(cherry picked from commit 308a9ad195166fdec288d2fb6b626d06fcab9390)

Bug: chromium:1150371
Change-Id: I3b372ac27848cd962a2987ecbb354e4fcd95871f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2555661
Reviewed-by: Frank Tang <ftang@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#830351}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2565790
Cr-Commit-Position: refs/branch-heads/4324@{#420}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/ea9cfd6db8715ef8024def8388c83c80ee5ed016/DEPS


### ft...@chromium.org (2020-11-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

Congratulations, the VRP panel has decided to award $5000 for this bug.

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

0xasnine - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1150371?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053910)*
