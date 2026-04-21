# Security: open an evil exe file via a "shortcut" in chrome://downloads/

| Field | Value |
|-------|-------|
| **Issue ID** | [40051192](https://issues.chromium.org/issues/40051192) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | ti...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2020-01-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When we download a file(named "fname") without an extension and then open the file with one click.  

If a file named "fname.exe" in the same download folder , the chrome will open the exe file.  

That means the "fname" is just a shortcut of the "fname.exe".

A lot of Client app will save the file in the DOWNLOAD folder.  

We can exploit the feature to open an evil software.

**VERSION**  

Chrome Version:  

Version 81.0.4021.2 (Official Build) dev (64-bit)  

Version 79.0.3945.117 (Official Build) stable (64-bit)  

Operating System: Windows 10 Pro 1909

**REPRODUCTION CASE**  

Step1. put a xxx.exe in the chrome download folder.  

Step2. download a file named xxx via the Internet.  

Step3. click the xxx in the Chrome.

Result: the xxx.exe will run.

See the poc.gif

## Attachments

- [poc.gif](attachments/poc.gif) (image/gif, 3.7 MB)
- [pppoc.png](attachments/pppoc.png) (image/png, 375.9 KB)

## Timeline

### ti...@gmail.com (2020-01-10)

Not only the exe file. 
.com | .pif |.cmd |.bat extension name also works.

### ti...@gmail.com (2020-01-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-01-11)

qinmin: Are you the right owner for this? Feel free to assign it back to me for re-triage if not.

[Monorail components: UI>Browser>Downloads]

### sh...@chromium.org (2020-01-11)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2020-01-13)

I guess it is probably the windows system calls appended the exe to the file open operation.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ti...@gmail.com (2021-01-05)

Hi, I found that the https://crbug.com/chromium/1092518 is a dump of my submission.
He submitted this on Tue, Jun 9, 2020.
I was earlier than him.
How do you deal with this kind of problem?

### am...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### je...@google.com (2021-01-15)

I implemented the fix to 1092518 and I can confirm that this report is for exactly the same issue.

It was caused by Chrome invoking Windows API function ::ShellExecuteExW(), which interpreted extensionless files as shell commands. The fix was to disable opening extensionless files from Chrome, and show the file in folder instead (crrev.com/c/2321528).

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

jessemckenna@ - thanks!

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

Congratulations, Zhong Zhaochen - the VRP panel has decided to award you $500 for this report! Thank you again for bringing this to our attention.

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### qi...@chromium.org (2021-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-12-31)

This issue was migrated from crbug.com/chromium/1040837?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051192)*
