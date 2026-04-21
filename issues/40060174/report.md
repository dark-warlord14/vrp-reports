# Security: V8 Typer hardening bypass via ReduceArrayPrototypeAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40060174](https://issues.chromium.org/issues/40060174) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ji...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2022-07-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Array.prototype.at [1](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/at) retrieves an array element at the specified index.  

This function is recently added to JSCallReducer. While there are some boundary checks [2](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/js-call-reducer.cc;l=1362-1366;drc=4c81827c8d6ca1d3d9b0cb6a2ef1264eb0f59524),  

they can be eliminated by typer bugs.

js-call-reducer.cc [2](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/js-call-reducer.cc;l=1362-1366;drc=4c81827c8d6ca1d3d9b0cb6a2ef1264eb0f59524):

```
// Bound checking.  
GotoIf(NumberLessThan(real_index_num, ZeroConstant()), &out,  
       UndefinedConstant());  
GotoIfNot(NumberLessThan(real_index_num, length), &out,  
          UndefinedConstant());  

```

This can result in OOB read in arrays.

function foo(a) {  

... (see poc.js)

```
confused = -confused | 0; // Range(0, 0) but 1  
var arr = [1.1, 1.2, 1.3];  
return arr.at(confused << 30); // OOB crash  

```

}

print(foo(3));  

for(var i = 0; i < 1e5; i++) foo(0);  

print(foo(3));

**VERSION**  

Chrome Version: V8 10.5.0 (candidate) commit 4c81827c8d6ca1d3d9b0cb6a2ef1264eb0f59524  

Operating System: All

**REPRODUCTION CASE**  

I've attached a RCE PoC for Linux x64 d8 environment Release mode.  

The PoC uses <https://crbug.com/1234770>, so the patch [3](https://chromium-review.googlesource.com/c/v8/v8/+/3068941) should be manually reverted.

**CREDIT INFORMATION**  

Reporter credit: Yonghwi Jin (@jinmo123) at Theori

## Attachments

- [exploit.js](attachments/exploit.js) (text/plain, 3.7 KB)

## Timeline

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### ji...@gmail.com (2022-07-06)

+ please add rjtgupta09@gmail.com as Cc. Thanks!

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### va...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-21)

tebbi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-07-22)

Thanks a lot for this report! It's great to find and close these hardening bypasses! I'll write a fix in the next days.

### te...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-08-11)

Chrome security marshal here. tebbi@ - it seems like you'd already started a fix. Any chance that fix will land soon?

### te...@chromium.org (2022-08-22)

I had to de-prioritize this one, so I didn't finish it yet. It's not very urgent I would say because we always assumed that there are typer hardening bypasses, so it doesn't change the security story much.

### [Deleted User] (2022-08-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-09-30)

[security marshal] Thanks for looking into this issue, tebbi@. We'd like high severity security bugs to be fixed in 60 days. Do you think you will have bandwidth to work on it soon? Or can you reassign it to another owner?  Thanks!

### te...@chromium.org (2022-10-11)

The typer hardening mitigation is just best effort and we never expected it to be complete. Therefore, fixing this bug doesn't have very high priority. I adjusted the priority and severity.
That being said, I still plan to fix it eventually, I just didn't get to it yet.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### te...@chromium.org (2023-06-19)

Fixed in: https://chromium-review.googlesource.com/c/v8/v8/+/4454339

### [Deleted User] (2023-06-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-19)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations Yonghwi Jin! The VRP Panel has decided to award you $5,000 for this high quality exploit mitigation bypass. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1342115?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1423487]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060174)*
