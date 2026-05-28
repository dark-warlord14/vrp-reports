# Command injection in "Copy as cURL (cmd)" due to improper sanitization

| Field | Value |
|-------|-------|
| **Issue ID** | [427367145](https://issues.chromium.org/issues/427367145) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Windows |
| **Chrome Version** | Version 139.0.7257.0 (Official Build) canary (64-bit) |
| **Reporter** | am...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2025-06-24 |
| **Bounty** | $1,500.00 |

## Description

# Steps to reproduce the problem

1. Open the poc html in chrome
2. open network teab and copy the requests with - copy all as curl (cmd) feature
3. paste the command on cmd you can see the calc popup

# Problem Description

A command injection vulnerability exists in the DevTools "Copy as cURL (cmd)" feature on Windows. The current implementation correctly handles carriage returns (\r) but fails to sanitize the tab character (\t).

The cmd.exe shell interprets the tab character as a delimiter, similar to a space. By injecting a payload containing a tab followed by a command separator (e.g., &) and a newline sequence, an attacker can break out of the intended cURL argument and execute arbitrary commands when the copied text is pasted into a Windows command prompt.

This is a bypass of a previous security fix that only addressed newline characters.

# Additional Comments

Security Impact:
This vulnerability allows for arbitrary code execution on a user's machine. If a user is tricked into pasting a crafted cURL command from a malicious source, the attacker can execute commands with the user's privileges.

Note: I have attached the poc video and html file for reference

# Summary

Command injection in "Copy as cURL (cmd)" due to improper sanitization

# Custom Questions

#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- [Chrome-CopyAsCurl-Codeexecution.mp4](attachments/Chrome-CopyAsCurl-Codeexecution.mp4) (video/mp4, 2.7 MB)
- [test.html](attachments/test.html) (text/html, 436 B)
- [Wed Jul 02 2025 19:50:03 GMT+0530 (India Standard Time).png](attachments/Wed Jul 02 2025 19_50_03 GMT+0530 (India Standard Time).png) (image/png, 209.8 KB)

## Timeline

### am...@gmail.com (2025-06-24)

Team i have fixed this issue from my end itself, i will be submitting the patch soon for review

### am...@gmail.com (2025-06-24)

Patch:
https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6666722

Note: Added a validation to replace all whitespace with standard one


Bisect:
I have tried bisected this issue, i have gone to the first build that was available in bisect build.py( Chrome 51 - may 2016) , the issue was reproducible in that too 

Literally this feature was introduced with this bug.


Kindly let me know about the patch and bisect bonus details too team

### ca...@chromium.org (2025-06-24)

Triaging the same as the similar crbug.com/406631048, danilsomsikov@: Can you help further triage this since you fixed the other issue? Thanks

I was not able to reproduce this since I don't have a Windows machine, but I'm triaging as valid since there's a video of the reproduction. Triaging as present in current stable (137) due to the provided bisection

### am...@gmail.com (2025-06-25)

Team is that my patch submitted way fine or do i need to submit it via any other way. eg: diff files

Kindly let me know the details.

### ch...@google.com (2025-06-25)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### da...@google.com (2025-07-02)

You patch is not submitted, it is not even sent for a review. You can sent it to me if you want.

### am...@gmail.com (2025-07-02)

Hi danil

Below is the link which i submitted my patch.

https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6666722

i wasnt sure why it is mentioned as not sent for review, if the above is not accesible and not able to review from your end, kindly let me know the details to assign you as a reviewer

Thanks waiting for your reply

### da...@google.com (2025-07-02)

See <https://gerrit-review.googlesource.com/Documentation/intro-user.html#adding-reviewers>

### am...@gmail.com (2025-07-02)

Your name wasn't listed in the reviewers section danil, kindly check on the attached image for reference

### da...@google.com (2025-07-02)

It's [dsv@chromium.org](mailto:dsv@chromium.org)

### am...@gmail.com (2025-07-02)

Thanks, I have assigned you as reviewer.

### dx...@google.com (2025-07-22)

Project: devtools/devtools-frontend  

Branch:  main  

Author:  Ameen [ameenbasha111@gmail.com](mailto:ameenbasha111@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6746171>

[DevTools] Sanitize special whitespace in "Copy as cURL (cmd)"

---


Expand for full commit details
```
     
    The escapeStringWin function did not properly sanitize special 
    whitespace characters (e.g., tabs, vertical tabs), which are 
    treated as delimiters by the Windows command prompt. 
     
    This change sanitizes all whitespace characters (other than normal space), which closes the vulnerability. 
     
    Bug: 427367145 
    Change-Id: If1f1be803a4b4a20a93b6982247eaf9cbebaf6ce 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6746171 
    Reviewed-by: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org>

```

---

Files:

- M `AUTHORS`
- M `front_end/panels/network/NetworkLogView.ts`

---

Hash: [553969206ce9e85d4f11dbe4756ddcfd1366e731](http://crrev.com/553969206ce9e85d4f11dbe4756ddcfd1366e731)  

Date: Tue Jul 22 11:03:11 2025


---

### dx...@google.com (2025-07-22)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6778080>

Roll DevTools Frontend from 1d75d2f8d2af to bc09a4034768 (7 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/1d75d2f8d2af..bc09a4034768 
     
    2025-07-22 jacktfranklin@chromium.org Add note about structured logs enable to AI Autorun README 
    2025-07-22 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update Chrome (for Testing) PIN 
    2025-07-22 nvitkov@chromium.org [cleanup] Prefer isOK to if not assert.fail 
    2025-07-22 samiyac@chromium.org Add widget for AI Code Completion Teaser 
    2025-07-22 nvitkov@chromium.org Use a single Unicode character for ellipsis 
    2025-07-22 ameenbasha111@gmail.com [DevTools] Sanitize special whitespace in "Copy as cURL (cmd)" 
    2025-07-22 nvitkov@chromium.org Fix CXX extension tests 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:427367145,chromium:429381318 
    Change-Id: I0004a84a5099a5507c6751023dfed517a40297db 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6778080 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1490144}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: [7b2814b50c170a73187b1238956abd99eee18e12](http://crrev.com/7b2814b50c170a73187b1238956abd99eee18e12)  

Date: Tue Jul 22 14:11:52 2025


---

### am...@gmail.com (2025-07-24)

Fixes are merged and CL rollout completed moving the issue to fixed state.

Kindly initaite the bounty process team. 
FYI: issue fixed from my end(patch bounus) and have sahred the bisect details that the issue was introduced with this bug itself (hope it is also eligible for bisect bonus)

### ch...@google.com (2025-07-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-07-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@gmail.com (2025-07-28)

Hi team, i have moved this issue to fixed state 4 days back, will this be automatically moved to bounty decision or should i have to do anything from my end?


Kindly confirm

### am...@gmail.com (2025-07-31)

@am...@chromium.org & danil any update on bounty? any action needed from my end?

### am...@chromium.org (2025-08-04)

The issue is marked `reward-topanel`, as always, it will be reviewed at a forthcoming VRP panel session

### am...@gmail.com (2025-08-19)

hi @am...@chromium.org and team hope you guys are back from bugswat event, Is there any update on the bounty for this case?

### am...@chromium.org (2025-08-21)

hello, while we have resumed regularly scheduled panel sessions as of last week, they are only once weekly and issues are assessed by severity and age. This issue will be assessed in at a future panel session within the coming weeks.

Thank you for your patience in the meantime and please avoid future pinging on the bug for updates.
If needed, please reach out to security-vrp@, however, as always, a VRP reward decision will be communicated on the bug after it has occurred. If there are no updates on the bug and it's one the reward-topanel hotlist, it just means we haven't gotten to it yet.

### sp...@google.com (2025-09-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1500.00 for this report.

Rationale for this decision:
$500 thank you reward for report of very low impact issue with little potential for security harm + $1000 patch bonus for very low size and complexity self-committed patch


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-10-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@gmail.com (2025-10-31)

Team Kindly update the CVE ID for this issue, Seems the issue is public but CVE is not assigned yet

@ds...@chromium.org can you check this case

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/427367145)*
