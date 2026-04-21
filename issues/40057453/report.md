# Security: Chrome 94 does not correctly set Integrity level of all processes to Untrusted

| Field | Value |
|-------|-------|
| **Issue ID** | [40057453](https://issues.chromium.org/issues/40057453) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox |
| **Platforms** | Windows |
| **Reporter** | ji...@gmail.com |
| **Assignee** | aj...@chromium.org |
| **Created** | 2021-09-30 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

In Process Explorer, child processes of chrome do not have Untrusted Integrity level. Instead, now they have Low Integrity. It persists after restarting process explorer, and I could set the Integrity Level to Untrusted, which showed updated Integrity Level (Untrusted).

Still, chrome://sandbox page shows their integrity level as Untrusted, so there are mismatch. I could reproduce this behavior in Chrome 94, 96 (Canary), but not 93.

**VERSION**  

Chrome Version: 94.0.992.31 stable  

Operating System: Windows 10 Version 21H1 (Build 19043.1237)

**REPRODUCTION CASE**  

Start chrome, navigate to any web pages, and check Integrity Levels with process explorer/etc.

**CREDIT INFORMATION**  

Reporter credit: Yonghwi Jin(@jinmo123) of Theori

## Attachments

- [capture.png](attachments/capture.png) (image/png, 21.8 KB)
- [after.png](attachments/after.png) (image/png, 104.8 KB)
- [before.png](attachments/before.png) (image/png, 98.8 KB)

## Timeline

### [Deleted User] (2021-09-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-09-30)

Will: Could you double check this? I can repro, but I'm not sure that this is actually an issue, given how the sandbox works. Hoping you can comment more.

### rs...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox]

### wf...@chromium.org (2021-09-30)

On first glance this report looks accurate. Will take a closer look.

### [Deleted User] (2021-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-09-30)

Thanks - chrome://sandbox only shows what the browser wants the process to be so if that's not getting to the children that's a problem! We'll take a look.

### aj...@chromium.org (2021-09-30)

Oddly this does not repro on the chromium bisect, but using official builds it does:-

python bisect_builds.py -o -a win64 -g 92.0.4515.107 -b 94.0.4606.61 --verify-range --use-local-cache -- --no-first-run
...
Bisecting range [909353 (good), 909355 (bad)].
Trying revision 909354...
Revision 909354 is [(g)ood/(b)ad/(r)etry/(u)nknown/(s)tdout/(q)uit]: b
You are probably looking for a change made after 909353 (known good), but no later than 909354 (first known bad).
CHANGELOG URL:
The script might not always return single CL as suspect as some perf builds might get missing due to failure.
  https://chromium.googlesource.com/chromium/src/+log/2d12b870e07b7b9f1fa6d52122f741f08943eefa..0394e042facd365087746734f65211702b78ad6d

### aj...@chromium.org (2021-09-30)

wfh - https://chromium.googlesource.com/chromium/src/+/0394e042facd365087746734f65211702b78ad6d

### aj...@chromium.org (2021-09-30)

Shows up with these gn args at least:-

```
is_debug = false
is_component_build = false
symbol_level = 2
blink_symbol_level = 1
use_goma = true

is_official_build = true
is_chrome_branded = true
media_use_ffmpeg = true
media_use_libvpx = true
proprietary_codecs = true
ffmpeg_branding = "Chrome"

win_enable_cfg_guards = true
```

### [Deleted User] (2021-09-30)

[Empty comment from Monorail migration]

### aj...@chromium.org (2021-09-30)

v. likely an lto devirtualization problem like https://crbug.com/chromium/1177001. Working on a CL.

### aj...@chromium.org (2021-09-30)

Testing CL https://chromium-review.googlesource.com/c/chromium/src/+/3198382

### aj...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### aj...@chromium.org (2021-09-30)

Confirming the theory that we're getting a wrong g_shared_delayed_integrity_level:

Grabbing the first renderer:

.shell -ci "!peb" findstr "CommandLine"
sxe ld:chrome
lm chrome
bp chrome!content::RendererMainPlatformDelegate::EnableSandbox

DWORD SetProcessIntegrityLevel(IntegrityLevel integrity_level) {
  // We don't check for an invalid level here because we'll just let it
  // fail on the SetTokenIntegrityLevel call later on.
  if (integrity_level == INTEGRITY_LEVEL_LAST) {
    // No mandatory level specified, we don't change it.
    return ERROR_SUCCESS;
  }

  HANDLE token_handle;
  if (!::OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_DEFAULT,
                          &token_handle))
    return ::GetLastError();

  base::win::ScopedHandle token(token_handle);

  return SetTokenIntegrityLevel(token.Get(), integrity_level);
}

chrome!sandbox::SetProcessIntegrityLevel:
00007ffe`184033c0 56              push    rsi
5:110> r
rax=0000f62a08701829 rbx=000000ea47fff110 rcx=0000000000000007
rdx=0000000000000004 rsi=00007ff688e94ff0 rdi=000000ea47fff120
rip=00007ffe184033c0 rsp=000000ea47ffef38 rbp=00001c6000110000
 r8=0000000000000000  r9=000000ea47ffef70 r10=00000fffd3ca8203
r11=000000000000021e r12=00002e4000058320 r13=00002e40000a8540
r14=0000000000068300 r15=aaaaaaaaaaaaaaaa
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000200
chrome!sandbox::SetProcessIntegrityLevel:
00007ffe`184033c0 56              push    rsi
5:110> p
chrome!sandbox::SetProcessIntegrityLevel+0x18:
00007ffe`184033d8 83f907          cmp     ecx,7 << INTEGRITY_LEVEL_LAST

... so does nothing we got the default value in g_shared_delayed_integrity_level

With cl in https://crbug.com/chromium/1254631#c13 (Fixed):

start             end                 module name
00007ffe`16160000 00007ffe`20a3d000   chrome   C (private pdb symbols)  c:\src\chromium\src\out\release\chrome.dll.pdb
...
5:110> t
chrome_exe!sandbox::TargetServicesBase::LowerToken:
00007ff7`fbb8bc60 56              push    rsi
5:110> lma @rip
Browse full module list
start             end                 module name
00007ff7`fba10000 00007ff7`fbc7e000   chrome_exe C (private pdb symbols)  c:\src\chromium\src\out\release\chrome.exe.pdb

chrome_exe!sandbox::SetProcessIntegrityLevel:
00007ff7`fbb8b630 56              push    rsi
5:110> r
rax=0000ba07382401b1 rbx=000000870edff190 rcx=0000000000000006
rdx=0000000000000004 rsi=00007ff7fbc24ff0 rdi=000000870edff1a0
rip=00007ff7fbb8b630 rsp=000000870edfefb8 rbp=00001f1e00110000
 r8=0000000000000000  r9=0000023b66bd3ac0 r10=00000ffeff77178c
r11=0000000000001000 r12=00000ef000058320 r13=00000ef0000a8540
r14=0000000000068300 r15=aaaaaaaaaaaaaaaa
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000206
chrome_exe!sandbox::SetProcessIntegrityLevel:
00007ff7`fbb8b630 56              push    rsi

rcx == 6 now as it should be.

### aj...@chromium.org (2021-09-30)

CC'd some MS folks - FYI this is happening in Edge too.

### aj...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### ss...@microsoft.com (2021-09-30)

Thanks for a heads up! Based on your analysis, there is a link time optimization (ThinLTO) that is removing the virtualization of c++ class functions that cross module boundaries, unless properly decorated? I assume dllexport and dllimport work for this as well?

### gi...@appspot.gserviceaccount.com (2021-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19d2be5d47e0edc406ef7d93096f54009e47937f

commit 19d2be5d47e0edc406ef7d93096f54009e47937f
Author: Alex Gough <ajgo@chromium.org>
Date: Thu Sep 30 21:23:47 2021

Tell clang not to devirtualize TargetServices

Before this change in official builds a child process's delayed
integrity level was not being set correctly. With this change
renderers run at Untrusted IL as intended.

Tests: https://bugs.chromium.org/p/chromium/issues/detail?id=1254631#c13
Bug: 1254631
Change-Id: I52c149cca3de5218033ed0f37d9f76782b9a6302
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3198382
Reviewed-by: Will Harris <wfh@chromium.org>
Commit-Queue: Will Harris <wfh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#926934}

[modify] https://crrev.com/19d2be5d47e0edc406ef7d93096f54009e47937f/sandbox/win/src/sandbox.h


### ss...@microsoft.com (2021-09-30)

I also wonder about other interfaces that seem to cross module boundaries, like TargetPolicy and the diagnostic interfaces in sandbox.h?

### aj...@chromium.org (2021-09-30)

ssmole: yes, others might move too - it mainly shouldn't matter unless they reference an important global.

### aj...@chromium.org (2021-09-30)

Marking Fixed as it would be good to merge CL in https://crbug.com/chromium/1254631#c19 once it works on Canary.

### fo...@chromium.org (2021-09-30)

ssmole@ I believe that ThinLTO will at least ignore anything with a uuid declspec (https://clang.llvm.org/docs/LTOVisibility.html) to avoid this becoming a problem for COM. Not sure about dllexport/dllimport though. For the sandbox at least the best fix for this would be move out the implementation of the sandbox classes into a separate library and only link them into one executable such as the main executable but that's going to be more complex.

### ss...@microsoft.com (2021-09-30)

forshaw- That link mentions dllexport/dllimport:
"When targeting Windows, classes with dllimport or dllexport attributes receive public LTO visibility."


### aj...@chromium.org (2021-09-30)

see https://crbug.com/chromium/1254910 for follow-on so this issue can concentrate on merges for the specific fix.

### [Deleted User] (2021-10-01)

[Empty comment from Monorail migration]

### aj...@chromium.org (2021-10-01)

Confirmed this is fixed in Canary 96.0.4659.3 - I'll prepare some merges.

### [Deleted User] (2021-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-01)

Requesting merge to stable M94 because latest trunk commit (926934) appears to be after stable branch point (911515).

Requesting merge to beta M95 because latest trunk commit (926934) appears to be after beta branch point (920003).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-01)

Merge review required: M95 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-01)

Merge review required: M94 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-10-01)

For both https://crbug.com/chromium/1254631#c30 and https://crbug.com/chromium/1254631#c31:

1. Yes this is a security fix for a High severity sandbox issue.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3200146 to 4606 and https://chromium-review.googlesource.com/c/chromium/src/+/3200145 to 4638 they are clean merges of the fix in https://crbug.com/chromium/1254631#c19.
3. Yes, and I have verified that they work.
4. No.
5. N/A.
6. N/A.

### am...@chromium.org (2021-10-01)

Thanks for the detailed responses for the merge review questions, ajgo@! Please go ahead merge the respective commits to their appropriate branches as specified above. Does not have to be today, but please get them in by Tuesday, 5 October EOD so that this fix can be in next week's stable channel respin. 

### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/466e04a85740c20faa126afc6120d098f503c96e

commit 466e04a85740c20faa126afc6120d098f503c96e
Author: Alex Gough <ajgo@chromium.org>
Date: Fri Oct 01 23:26:35 2021

Tell clang not to devirtualize TargetServices

Before this change in official builds a child process's delayed
integrity level was not being set correctly. With this change
renderers run at Untrusted IL as intended.

(cherry picked from commit 19d2be5d47e0edc406ef7d93096f54009e47937f)

Tests: https://bugs.chromium.org/p/chromium/issues/detail?id=1254631#c13
Bug: 1254631
Change-Id: I52c149cca3de5218033ed0f37d9f76782b9a6302
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3198382
Reviewed-by: Will Harris <wfh@chromium.org>
Commit-Queue: Will Harris <wfh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#926934}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3200145
Commit-Queue: Alex Gough <ajgo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#519}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/466e04a85740c20faa126afc6120d098f503c96e/sandbox/win/src/sandbox.h


### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a5bafa35defbaf3fd82bd2220034bd403e76243

commit 3a5bafa35defbaf3fd82bd2220034bd403e76243
Author: Alex Gough <ajgo@chromium.org>
Date: Fri Oct 01 23:30:09 2021

Tell clang not to devirtualize TargetServices

Before this change in official builds a child process's delayed
integrity level was not being set correctly. With this change
renderers run at Untrusted IL as intended.

(cherry picked from commit 19d2be5d47e0edc406ef7d93096f54009e47937f)

Tests: https://bugs.chromium.org/p/chromium/issues/detail?id=1254631#c13
Bug: 1254631
Change-Id: I52c149cca3de5218033ed0f37d9f76782b9a6302
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3198382
Reviewed-by: Will Harris <wfh@chromium.org>
Commit-Queue: Will Harris <wfh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#926934}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3200146
Commit-Queue: Alex Gough <ajgo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#1285}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/3a5bafa35defbaf3fd82bd2220034bd403e76243/sandbox/win/src/sandbox.h


### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, Yonghwi Jin! The VRP Panel has decided to award you $3000 for this report. Nice catch and thank you for reporting this issue to us! 

### am...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-07)

[Empty comment from Monorail migration]

### ji...@gmail.com (2021-10-08)

Hello, can I update the credit information? The company name is omitted.

### rz...@google.com (2021-10-08)

Labelling as not applicable for M90 as it affects only Windows

### am...@chromium.org (2021-10-08)

hi jinmoteam@, thanks for raising our attention to this. I see that accidentally accidentally omitted the company name in the release notes and will have that corrected by EOD today. Thanks! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2021-10-14)

Perhaps not my place to say (and definitely not arguing against the novelty or value of the report) but should this really have been Security_Severity-High given that it doesn't seem to weaken the sandbox at all?

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1254631?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057453)*
