# Type Confusion In Chrome Lead to RCE 

| Field | Value |
|-------|-------|
| **Issue ID** | [40087661](https://issues.chromium.org/issues/40087661) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2017-05-16 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36

Steps to reproduce the problem:
1. open the hello_chrome.html with the latest version of chrome
2. We can control the RIP and go to the shellcode which is 0xcc(int 3)
3. 

What is the expected behavior?
nothing to happen

What went wrong?
We can control the RIP and go to the shellcode which is 0xcc(int 3)
The zip's passwrod:72427200dabao

Did this work before? N/A 

Chrome version: 58.0.3029.110  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: 

This problem belongs to the crankshaft,in the latest V8 version(16th May 2017)(use crankshaft to JIT),I can reproduce this issue.And this is a FULL EXP which works on the latest chrome stable version( 58.0.3029.110 ).At this version,the chrome use crankshaft to JIT.

## Attachments

- [hello_chrome.zip](attachments/hello_chrome.zip) (application/octet-stream, 2.0 KB)

## Timeline

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5115844635131904

### el...@chromium.org (2017-05-16)

This doesn't seem to crash in Canary, which fires the following script error: 
Uncaught TypeError: First argument to DataView constructor must be an ArrayBuffer
    at new DataView (<anonymous>)
    at hello_chrome.html:263

It does crash in M58; crash/bc9f55e170000000


### wf...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5537737125134336

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5976780828835840

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4676478607556608

### wf...@chromium.org (2017-05-16)

I just get "TypeError: First argument to DataView constructor must be an ArrayBuffer" every time, I've tried with d8 5.8.283.38 built with asan with --crankshaft flag. I also can't get a crash on clusterfuzz...

### el...@chromium.org (2017-05-16)

On Windows Stable, I see the alert message and then the tab crashes. Might it not crash on Clusterfuzz due to the alert() dialog?

Google Chrome	58.0.3029.110 (Official Build) (64-bit)
Revision	691bdb490962d4e6ae7f25c6ab1fdd0faaf19cd0-refs/branch-heads/3029@{#830}
OS	Windows
JavaScript	V8 5.8.283.38
Flash	25.0.0.171 C:\Users\elawrence\AppData\Local\Google\Chrome\User Data\PepperFlash\25.0.0.171\pepflashplayer.dll
User Agent	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
Command Line	"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --flag-switches-begin --mark-non-secure-as=non-secure --enable-features=password-import-export --flag-switches-end -- "C:\Users\elawrence\Desktop\hello_chrome.html"
Variations
ea8deb27-3f4a17df
241fff6c-ca7d8d80
3095aa95-3f4a17df
7c1bc906-f55a7974
1c752ce9-33c3eba5
ba3f87da-45bda656
cf558fa6-48a16532
f1ab784a-3d47f4f4
f3499283-7711d854
349d561b-65bced95
9e201a2b-65bced95
5274eb09-3f4a17df
b684f56f-4d2fac87
b791c1b8-ca7d8d80
9773d3bd-ca7d8d80
b22b3d54-4e046809
2e109477-ca7d8d80
99144bc3-3cc2175e
9e5c75f1-45096096
f79cb77b-3f4a17df
b7786474-d93a0620
23a898eb-ca7d8d80
4ea303a6-68942f92
7aa46da5-669a04e0
69bf80fa-91c810ef
b2f0086-93053e47
6844d8aa-669a04e0
494d8760-3d47f4f4
f47ae82a-746c2ad4
3ac60855-3ec2a267
f296190c-fd6d2f5a
4442aae2-4ad60575
ed1d377-e1cc0f14
75f0f0a0-d7f6b13c
e2b18481-6e3b1976
e7e71889-e1cc0f14
61b920c1-ca7d8d80
828a5926-c6c0a780
Compiler	MSVC 2015 (PGO)

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4670544841801728

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5537984622624768

### so...@gmail.com (2017-05-16)

[Comment Deleted]

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4771582068391936

### wf...@chromium.org (2017-05-16)

thanks, I can now repro on 5.8.283.38 but not 6.0.0 (candidate) r45347. Will see if I can persuade CF to repro...

### cl...@chromium.org (2017-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5744343037247488

### cl...@chromium.org (2017-05-16)

ClusterFuzz has detected this issue as fixed in range 43658:43659.

Detailed report: https://clusterfuzz.com/testcase?key=5744343037247488

Job Type: linux_asan_d8
Crash Type: UNKNOWN READ
Crash Address: 0x0024e2458007
Crash State:
  v8::internal::MemoryChunk::heap
  v8::internal::HeapObject::HeapObjectShortPrint
  v8::internal::operator<<
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Fixed: V8: 43658:43659

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5744343037247488


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-05-16)

Detailed report: https://clusterfuzz.com/testcase?key=5744343037247488

Job Type: linux_asan_d8
Crash Type: UNKNOWN READ
Crash Address: 0x0024e2458007
Crash State:
  v8::internal::MemoryChunk::heap
  v8::internal::HeapObject::HeapObjectShortPrint
  v8::internal::operator<<
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: V8: 36651:36652
Fixed: V8: 43658:43659

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5744343037247488


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

The recommended severity is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.


### wf...@chromium.org (2017-05-16)

CF analysis seems wrong - I can still repro on rev 43659 - v8 commit 76224f7e4994af40e896069a1372373e25699a7c

### wf...@chromium.org (2017-05-17)

I manual bisected the first commit where this bug is fixed is 0f716acadaed1d9e194593543dbe1340d600d6fc "Turn on Ignition + TurboFan."

### cl...@chromium.org (2017-05-17)

ClusterFuzz testcase 5744343037247488 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### so...@gmail.com (2017-05-17)

[Comment Deleted]

### in...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### so...@gmail.com (2017-05-17)

[Comment Deleted]

### jo...@chromium.org (2017-05-17)

Please note that ClusterFuzz is a bot which automatically recommend certain actions. Your report looks very interesting. Let me CC some more folks to look into fixing this

### jk...@chromium.org (2017-05-17)

#22: This is definitely a high-severity security issue. Please keep the reports coming! (Especially for Turbofan; but as long as Crankshaft is shipping on the stable channel, we definitely care about that too.)

Fix is up for review: https://chromium-review.googlesource.com/c/507209/

### mv...@chromium.org (2017-05-17)

Thanks for the great fix, Jakob!

### sh...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e33fd30777f99a0d6e16b16d096a2663b1031457

commit e33fd30777f99a0d6e16b16d096a2663b1031457
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed May 17 13:11:02 2017

[crankshaft] Fix HAliasAnalyzer for constants

BUG=chromium:722756

Change-Id: I04fc7fa0b8ef1e56d25f829fc5c8f53ae439aa52
Reviewed-on: https://chromium-review.googlesource.com/507209
Reviewed-by: Daniel Clifford <danno@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/master@{#45375}
[modify] https://crrev.com/e33fd30777f99a0d6e16b16d096a2663b1031457/src/crankshaft/hydrogen-alias-analysis.h
[add] https://crrev.com/e33fd30777f99a0d6e16b16d096a2663b1031457/test/mjsunit/regress/regress-crbug-722756.js


### so...@gmail.com (2017-05-18)

#24:Thank you for your imformation.

I will do some testings for your patch.

And in #1,there is a FULL EXPLOIT for this issue.If there are any confusions,welcome to contact me any time.

### jk...@chromium.org (2017-05-18)

Fixed by #27.

We don't have Canary coverage yet, but Canary coverage is also not going to be particularly useful in this case, because the bug is in Crankshaft, which is not used on Canary any more. Requesting merges now.

M59: Currently the Crankshaft pipeline is still being finched to a small fraction of users. As long as that is the case, we should fix this bug there.

M58: This is a high-severity security issue on the stable channel. I think that's a good reason to backmerge the fix? (Even if we don't immediately roll a new release for this.)

Note to security team / reward panel: The buggy code was >3 years old (I haven't verified if all releases in this time were vulnerable, but I assume so). I've verified that the exploit indeed allows execution of arbitrary attacker-provided machine code on M58.

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### sh...@chromium.org (2017-05-18)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7af4a42fc2a4e78e1acc0270531b2e2282ae828a

commit 7af4a42fc2a4e78e1acc0270531b2e2282ae828a
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Thu May 18 13:46:35 2017

Merged: [crankshaft] Fix HAliasAnalyzer for constants

Revision: e33fd30777f99a0d6e16b16d096a2663b1031457

BUG=chromium:722756
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=cbruni@chromium.org

Change-Id: I948e25bcaa536475e04702ea8124f22d9492c184
Reviewed-on: https://chromium-review.googlesource.com/508352
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/branch-heads/5.9@{#57}
Cr-Branched-From: fe9bb7e6e251159852770160cfb21dad3cf03523-refs/heads/5.9.211@{#1}
Cr-Branched-From: 70ad23791a21c0dd7ecef8d4d8dd30ff6fc291f6-refs/heads/master@{#44591}
[modify] https://crrev.com/7af4a42fc2a4e78e1acc0270531b2e2282ae828a/src/crankshaft/hydrogen-alias-analysis.h
[add] https://crrev.com/7af4a42fc2a4e78e1acc0270531b2e2282ae828a/test/mjsunit/regress/regress-crbug-722756.js


### jk...@chromium.org (2017-05-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-05-18)

+ awhalley@ for M58 merge review. Please note we're not planning further M58 releases. 

### am...@chromium.org (2017-05-18)

Not sec sev critical, there's no need to merge this late post branch.

### sh...@chromium.org (2017-05-19)

[Empty comment from Monorail migration]

### so...@gmail.com (2017-05-22)

Could you please assign a CVE to this issue?
Thanks

### aw...@chromium.org (2017-05-22)

soulchen8650@ - we assign CVEs when the fix goes out in a stable release.  That should be in a couple of weeks for M59.

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### so...@gmail.com (2017-05-25)

[Comment Deleted]

### so...@gmail.com (2017-05-25)

[Comment Deleted]

### so...@gmail.com (2017-05-25)

Thanks for your information.Here is my acknowledgment information:
Zhao Qixun(@S0rryMybad) of Qihoo 360 Vulcan Team
May be someting is wrong,my coomment have been deleted automatically...

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

Congratulations! The VRP panel decided to award $7,500 for this report!  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### so...@gmail.com (2017-06-19)

Hello,

Could you mind to tell me how long will I get the reward?


### aw...@chromium.org (2017-06-19)

Hello - should be about two weeks at this point.

### sh...@chromium.org (2017-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2017-09-18)

We have made a bunch of changes on ClusterFuzz side, so resetting ClusterFuzz-Wrong label.

### ki...@gmail.com (2017-10-05)

Hello,

Where can I get hello_chrome.html from? I would like to understand the issue better, and see if my product that is based on Chromium 53 is affected.




### jk...@chromium.org (2017-10-05)

#51: I don't know where you can get hello_chrome.html, but I can tell you with certainty that M53 is affected (see #29).

(It's probably affected by a bunch of other security issues too -- you really should update, and keep it up to date!)

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/722756?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087661)*
