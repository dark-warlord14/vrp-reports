# Security: v8 dcheck failure and fatal error

| Field | Value |
|-------|-------|
| **Issue ID** | [40095359](https://issues.chromium.org/issues/40095359) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | th...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2019-06-11 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**  

v8 dcheck failure and fatal error

**VERSION**  

Chrome Version: 75.0.3770.80 stable  

Operating System: ubuntu 16.04

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

run d8(verison 7.5.288.22) with this poc : gdb --args ./d8 ./poc.js

d8 will crash with dcheck failure

poc.js

function main() {  

const v1 = [13.37,13.37,13.37,13.37,13.37];  

const v2 = {forEach:v1};  

function v3(v4,v5) {  

const v10 = [13.37];  

const v12 = [1337,1337,1337];  

const v13 = [1337,2147483648,v10,v10];  

const v14 = {constructor:v12,asinh:v10,getUint8:parseInt,sinh:v13,MIN\_VALUE:v12};  

let v15 = 2147483648;  

const v19 = [1337,1337,1337];  

const v20 = ["boolean",Atomics,v19];  

let v21 = v20;  

let v23 = 2006948048;  

v20.valueOf = v23;  

const v25 = Object.seal(v21);  

function v26(v27,v28,v29,v30,v31) {  

}  

v25.valueOf = v26;  

let v33 = 0;  

let v35 = 0;  

const v36 = v35 + 1;  

v35 = v36;  

const v37 = v33 + 1;  

const v39 = [1337,1337,1337,1337];  

const v42 = [13.37];  

const v43 = [v42,Symbol,v42,13.37];  

function v44(v45,v46,v47) {  

return v43;  

}  

let v49 = 0;  

while (v49 < 6) {  

const v50 = v49 + 1;  

v49 = v50;  

let v53 = 0;  

while (v53 < 8) {  

const v55 = Symbol.replace;  

v2[v55] = 8;  

const v56 = v53 + 1;  

v53 = v56;  

}  

for (let v60 = 0; v60 < 3; v60++) {  

v50.valueOf = v44;  

}  

}  

}  

const v61 = v3();  

const v62 = v3();  

}  

main();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

# 

# Fatal error in ../../src/objects/map.cc, line 1020

# Debug check failed: to\_kind == DICTIONARY\_ELEMENTS || to\_kind == SLOW\_STRING\_WRAPPER\_ELEMENTS || IsFixedTypedArrayElementsKind(to\_kind).

# 

# 

# 

#FailureMessage Object: 0x7fffffffbdd0  

==== C stack trace ===============================

```
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x49ee92) [0x5555559f2e92]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x49c807) [0x5555559f0807]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x492bae) [0x5555559e6bae]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x492745) [0x5555559e6745]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0xd42399) [0x555556296399]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0xd419d4) [0x5555562959d4]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x18db643) [0x555556e2f643]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x18dad9c) [0x555556e2ed9c]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x18d0c3a) [0x555556e24c3a]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1786c11) [0x555556cdac11]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1786518) [0x555556cda518]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1785be0) [0x555556cd9be0]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1773a57) [0x555556cc7a57]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1767368) [0x555556cbb368]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1763e11) [0x555556cb7e11]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1763723) [0x555556cb7723]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x651448) [0x555555ba5448]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x65a859) [0x555555bae859]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x65bc46) [0x555555bafc46]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x102ac40) [0x55555657ec40]  
/home/test/Documents/fuzz/v8_for_test/fuzzbuild_test/d8(+0x1d247a0) [0x5555572787a0]  

```

Thread 1 "d8" received signal SIGILL, Illegal instruction.

[----------------------------------registers-----------------------------------]  

RAX: 0x88f  

RBX: 0x5555559f07e0 (<\_ZN2v88platform12\_GLOBAL\_\_N\_115PrintStackTraceEv>: )  

RCX: 0x4407  

RDX: 0x80  

RSI: 0x7ffff7ecb010 --> 0x89792  

RDI: 0x5555575492a4 --> 0x448100000000  

RBP: 0x7fffffffbdc0 --> 0x7fffffffc0d0 --> 0x7fffffffc0e0 --> 0x7fffffffc1d0 --> 0x7fffffffc220 --> 0x7fffffffc280 (--> ...)  

RSP: 0x7fffffffbdc0 --> 0x7fffffffc0d0 --> 0x7fffffffc0e0 --> 0x7fffffffc1d0 --> 0x7fffffffc220 --> 0x7fffffffc280 (--> ...)  

RIP: 0x5555559ed776 (<\_ZN2v84base2OS5AbortEv+54>: ud2)  

R8 : 0x7ffff728b770 --> 0x0  

R9 : 0x7ffff7fcc740 (0x00007ffff7fcc740)  

R10: 0x0  

R11: 0x0  

R12: 0x55555569a23d ("Debug check failed: %s.")  

R13: 0x7fffffffc090 --> 0x3000000020 (' ')  

R14: 0x3fc  

R15: 0x55555567eee4 ("../../src/objects/map.cc")  

EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)

[-------------------------------------code-------------------------------------]  

0x5555559ed765 <\_ZN2v84base2OS5AbortEv+37>:  

call 0x5555574d3300 [abort@plt](mailto:abort@plt)  

0x5555559ed76a <\_ZN2v84base2OS5AbortEv+42>:  

lea rdi,[rip+0x1b5bb33] # 0x5555575492a4  

0x5555559ed771 <\_ZN2v84base2OS5AbortEv+49>:  

call 0x555555943f20 <\_\_sanitizer\_cov\_trace\_pc\_guard>  

=> 0x5555559ed776 <\_ZN2v84base2OS5AbortEv+54>: ud2  

0x5555559ed778: int3  

0x5555559ed779: int3  

0x5555559ed77a: int3  

0x5555559ed77b: int3  

[------------------------------------stack-------------------------------------]  

0000| 0x7fffffffbdc0 --> 0x7fffffffc0d0 --> 0x7fffffffc0e0 --> 0x7fffffffc1d0 --> 0x7fffffffc220 --> 0x7fffffffc280 (--> ...)  

0008| 0x7fffffffbdc8 --> 0x5555559e6bc2 (int3)  

0016| 0x7fffffffbdd0 --> 0xdecade10  

0024| 0x7fffffffbdd8 ("Debug check failed: to\_kind == DICTIONARY\_ELEMENTS || to\_kind == SLOW\_STRING\_WRAPPER\_ELEMENTS || IsFixedTypedArrayElementsKind(to\_kind).")  

0032| 0x7fffffffbde0 ("eck failed: to\_kind == DICTIONARY\_ELEMENTS || to\_kind == SLOW\_STRING\_WRAPPER\_ELEMENTS || IsFixedTypedArrayElementsKind(to\_kind).")  

0040| 0x7fffffffbde8 ("ed: to\_kind == DICTIONARY\_ELEMENTS || to\_kind == SLOW\_STRING\_WRAPPER\_ELEMENTS || IsFixedTypedArrayElementsKind(to\_kind).")  

0048| 0x7fffffffbdf0 ("ind == DICTIONARY\_ELEMENTS || to\_kind == SLOW\_STRING\_WRAPPER\_ELEMENTS || IsFixedTypedArrayElementsKind(to\_kind).")  

0056| 0x7fffffffbdf8 ("ICTIONARY\_ELEMENTS || to\_kind == SLOW\_STRING\_WRAPPER\_ELEMENTS || IsFixedTypedArrayElementsKind(to\_kind).")  

[------------------------------------------------------------------------------]  

Legend: code, data, rodata, value  

Stopped reason: SIGILL  

0x00005555559ed776 in v8::base::OS::Abort() ()  

at ../../src/base/platform/platform-posix.cc:400  

400 ../../src/base/platform/platform-posix.cc: No such file or directory.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Timeline

### th...@gmail.com (2019-06-11)

note:build d8 with this option:"    gn gen out/fuzzbuild --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_enable_verify_predictable=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'
"

### me...@chromium.org (2019-06-11)

Thanks for the report.

bmeurer: Can you please take a look?

### me...@chromium.org (2019-06-11)

+titzer, V8 CF sheriff

### me...@chromium.org (2019-06-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ti...@chromium.org (2019-06-12)

This may be related to 953659.

### bm...@chromium.org (2019-06-12)

Indeed, https://bugs.chromium.org/p/chromium/issues/detail?id=953659 looks very related.

### th...@gmail.com (2019-06-12)

[Comment Deleted]

### th...@gmail.com (2019-06-13)

Is "related" means dupe?

### me...@chromium.org (2019-06-13)

Tentatively adding severity (same as 953659)

th3mess: It's not clear yet, but if it turns out to be a duplicate, I'll CC you in on the other bug.

### me...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### th...@gmail.com (2019-06-14)

[Comment Deleted]

### sh...@chromium.org (2019-06-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@gmail.com (2019-06-17)

[Comment Deleted]

### is...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### is...@chromium.org (2019-06-18)

Re #11: This assert is related because it's caused by the same new functionality "new frozen, sealed elements kinds".
However, there were multiple issues with those new elements kinds found by external contributors and our infrastructure and fixed on tip of V8 tree.
The DCHECK failure you mentioned in this report was most likely fixed by https://chromium-review.googlesource.com/c/v8/v8/+/1574777 but it wasn't merged to M75.

It's hard to tell whether the root cause of this crash is actually the same as the one addressed in that CL because unfortunately I wasn't able to reproduce the crash on 7.5.288.22 so far. The gn args mentioned in #1 also did not help. 

### th...@gmail.com (2019-06-18)

[Comment Deleted]

### is...@chromium.org (2019-06-18)

We have another report reproducibility problem in https://crbug.com/chromium/974619. Let's try to repro that one first.

### th...@gmail.com (2019-06-18)

[Comment Deleted]

### is...@chromium.org (2019-06-18)

Thanks!

### th...@gmail.com (2019-06-19)

[Comment Deleted]

### is...@chromium.org (2019-06-19)

Thank you! --interrupt-budget=1024 did help.

It seems there are more sealed/frozen elements kind commits that has to be merged back to M75. I looks it was too early to ship them in M75.
I'll prepare the CL to disable these new elements kinds and merge it back to M75.

### is...@chromium.org (2019-06-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/de6382dfc88b90a28c051ed2b434315586035717

commit de6382dfc88b90a28c051ed2b434315586035717
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed Jun 19 11:19:15 2019

Make frozen/sealed elements kinds disablable

Bug: chromium:972921
Change-Id: Ieb13c2f18714abc60aeb4a6a77c1e43b88681f43
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1667005
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#62280}

[modify] https://crrev.com/de6382dfc88b90a28c051ed2b434315586035717/src/builtins/builtins-handler-gen.cc
[modify] https://crrev.com/de6382dfc88b90a28c051ed2b434315586035717/src/flags/flag-definitions.h
[modify] https://crrev.com/de6382dfc88b90a28c051ed2b434315586035717/src/objects/elements-kind.h
[modify] https://crrev.com/de6382dfc88b90a28c051ed2b434315586035717/test/cctest/test-field-type-tracking.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/77476cb278a2e82de8779000b13206645c6ee02f

commit 77476cb278a2e82de8779000b13206645c6ee02f
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed Jun 19 12:07:35 2019

Temporarily disable frozen/sealed elements kinds

... to prepare for merging this back to stable chanel.

Bug: chromium:972921
Change-Id: I04ced1c81b5f8730014ecee8935799fccc377a49
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1667006
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#62283}

[modify] https://crrev.com/77476cb278a2e82de8779000b13206645c6ee02f/src/flags/flag-definitions.h


### is...@chromium.org (2019-06-19)

Once we got Canary coverage we need to merge these two CLs to M75.

### sh...@chromium.org (2019-06-19)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@gmail.com (2019-06-19)

[Comment Deleted]

### sr...@google.com (2019-06-19)

adetaylor@ can you review this bug, at this point for M75, I am planning to go to 50% today and 100% tomorrow barring no new blockers and we dont have any re-spins planned or in pipeline at this moment, Can this wait till M76 or is this a potential re-spin candidate?

### du...@microsoft.com (2019-06-19)

Yes, it has been fixed in tip of v8, just not merge into v7.5

### ad...@chromium.org (2019-06-19)

ishell@ Can you check that the Security_Severity is appropriate? Specifically, what would be the expected behavior on a release build if it sailed past the DCHECK? Guidelines here - https://www.chromium.org/developers/severity-guidelines. If in doubt, keep it at High.

As this is in v8 but not yet in Chromium, I'd say there's a very high chance people will notice and start to craft exploits for this, so if there's any chance it's exploitable then we should respin M75. It's a while before M76 stable so it seems likely we'll respin anyway.

### sh...@chromium.org (2019-06-20)

[Empty comment from Monorail migration]

### is...@chromium.org (2019-06-21)

Re #30: Given that 
1) new elements kinds support seems to be an ongoing work and we already had to merge several fixes to M75 and
2) the elements kind handling logic is spread over the V8 code base and not trivial to audit
I'm suggesting to disable it altogether in M75 (to avoid more potential merge-backs) and merge #23 to M76 (to be ready for merging #24 if we miss merge-backs to M76 again).

BTW, we shipped these changes to Canary an hour ago. We'll have a stability data soon.

### is...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### sr...@google.com (2019-06-21)

thank you ishell@, for this info. 

Based on https://crbug.com/chromium/972921#c33 , i am rejecting the merge request for M75 , pls go head and request a merge to M76.

### is...@chromium.org (2019-06-21)

I'm sorry, why did you reject the merge request to M75?
Are you instead suggesting to merge to M75 all the fixes related to new elements kinds that was made after M75?

### th...@gmail.com (2019-06-24)

[Comment Deleted]

### ha...@chromium.org (2019-06-24)

The plan in https://crbug.com/chromium/972921#c33 sounds fine to me. What is going to be the expected performance hit?

### is...@chromium.org (2019-06-24)

The the new elements kinds seem to improve only some of the frameworks (see the design doc: bit.ly/fast-frozen-sealed-elements-in-v8), so the regression in real-world should not be that high.

I'll proceed with merging #23 and #24 to M75.

### is...@chromium.org (2019-06-24)

Merged to M75: https://chromium-review.googlesource.com/c/v8/v8/+/1674030

### ad...@chromium.org (2019-06-24)

th3mess@ - I'd expect this to get a CVE when we release the fix, yes. As to a reward, that's up to the VRP panel to decide.

### th...@gmail.com (2019-06-24)

ok, thanks a lot, plz credit to: m3plex

### ad...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### th...@gmail.com (2019-07-18)

oh! many thanks~

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/972921?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/976185]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095359)*
