# Security: use after free in cups_printers_handler

| Field | Value |
|-------|-------|
| **Issue ID** | [40059038](https://issues.chromium.org/issues/40059038) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Printing |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | bm...@chromium.org |
| **Created** | 2022-03-09 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

In <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/chromeos/cups_printers_handler.cc;l=887>  

select\_file\_dialog\_ = ui::SelectFileDialog::Create(  

this, std::make\_unique<ChromeSelectFilePolicy>(web\_contents));

The previous select\_file\_dialog\_ could be destructed because of the duplicate creation. The use after free will occur when using this SelectFileDialog.

**VERSION**  

Chrome Version: 99.0.4844.57 stable  

Operating System: chromeos

**REPRODUCTION CASE**

open chrome://os-settings, inspect the window, and run the follow code:

chrome.send("selectPPDFile",[""]);  

chrome.send("selectPPDFile",[""]);

Close the file chooser dialog.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State:  

I don't have a local chromeos test environment, so I used <https://storage.googleapis.com/chromium-browser-asan/linux-release-chromeos/asan-linux-release-977036.zip> to test.

==22203==ERROR: AddressSanitizer: heap-use-after-free on address 0x6100001c9450 at pc 0x55f0feef1b44 bp 0x7ffcfc396490 sp 0x7ffcfc396488  

READ of size 8 at 0x6100001c9450 thread T0 (chrome)  

#0 0x55f0feef1b43 (/home/ori/asan-linux-release-977036/chrome+0x28b3ab43) (BuildId: 16aaf0f432fe0664)  

#1 0x55f0feef16c1 (/home/ori/asan-linux-release-977036/chrome+0x28b3a6c1) (BuildId: 16aaf0f432fe0664)  

#2 0x55f0f8461ba3 (/home/ori/asan-linux-release-977036/chrome+0x220aaba3) (BuildId: 16aaf0f432fe0664)  

#3 0x55f0f8450465 (/home/ori/asan-linux-release-977036/chrome+0x22099465) (BuildId: 16aaf0f432fe0664)  

#4 0x55f0ffa28bf6 (/home/ori/asan-linux-release-977036/chrome+0x29671bf6) (BuildId: 16aaf0f432fe0664)  

#5 0x55f0ffa29697 (/home/ori/asan-linux-release-977036/chrome+0x29672697) (BuildId: 16aaf0f432fe0664)  

#6 0x55f0e7586ffb (/home/ori/asan-linux-release-977036/chrome+0x111cfffb) (BuildId: 16aaf0f432fe0664)  

#7 0x55f0f3de5cd2 (/home/ori/asan-linux-release-977036/chrome+0x1da2ecd2) (BuildId: 16aaf0f432fe0664)  

#8 0x55f0f3df9027 (/home/ori/asan-linux-release-977036/chrome+0x1da42027) (BuildId: 16aaf0f432fe0664)  

#9 0x55f0f3de8cb6 (/home/ori/asan-linux-release-977036/chrome+0x1da31cb6) (BuildId: 16aaf0f432fe0664)  

#10 0x55f0f3dab961 (/home/ori/asan-linux-release-977036/chrome+0x1d9f4961) (BuildId: 16aaf0f432fe0664)  

#11 0x55f0f3da55d3 (/home/ori/asan-linux-release-977036/chrome+0x1d9ee5d3) (BuildId: 16aaf0f432fe0664)  

#12 0x55f0f2603726 (/home/ori/asan-linux-release-977036/chrome+0x1c24c726) (BuildId: 16aaf0f432fe0664)  

#13 0x55f0f26453c7 (/home/ori/asan-linux-release-977036/chrome+0x1c28e3c7) (BuildId: 16aaf0f432fe0664)  

#14 0x55f0f2644ac7 (/home/ori/asan-linux-release-977036/chrome+0x1c28dac7) (BuildId: 16aaf0f432fe0664)  

#15 0x55f0f2646061 (/home/ori/asan-linux-release-977036/chrome+0x1c28f061) (BuildId: 16aaf0f432fe0664)  

#16 0x55f0f278765d (/home/ori/asan-linux-release-977036/chrome+0x1c3d065d) (BuildId: 16aaf0f432fe0664)  

#17 0x55f0f264671a (/home/ori/asan-linux-release-977036/chrome+0x1c28f71a) (BuildId: 16aaf0f432fe0664)  

#18 0x55f0f257d79c (/home/ori/asan-linux-release-977036/chrome+0x1c1c679c) (BuildId: 16aaf0f432fe0664)  

#19 0x55f0e8fdd5f4 (/home/ori/asan-linux-release-977036/chrome+0x12c265f4) (BuildId: 16aaf0f432fe0664)  

#20 0x55f0e8fe1c71 (/home/ori/asan-linux-release-977036/chrome+0x12c2ac71) (BuildId: 16aaf0f432fe0664)  

#21 0x55f0e8fd786a (/home/ori/asan-linux-release-977036/chrome+0x12c2086a) (BuildId: 16aaf0f432fe0664)  

#22 0x55f0f235ae8f (/home/ori/asan-linux-release-977036/chrome+0x1bfa3e8f) (BuildId: 16aaf0f432fe0664)  

#23 0x55f0f235d9ef (/home/ori/asan-linux-release-977036/chrome+0x1bfa69ef) (BuildId: 16aaf0f432fe0664)  

#24 0x55f0f235ce28 (/home/ori/asan-linux-release-977036/chrome+0x1bfa5e28) (BuildId: 16aaf0f432fe0664)  

#25 0x55f0f2357609 (/home/ori/asan-linux-release-977036/chrome+0x1bfa0609) (BuildId: 16aaf0f432fe0664)  

#26 0x55f0f2357c85 (/home/ori/asan-linux-release-977036/chrome+0x1bfa0c85) (BuildId: 16aaf0f432fe0664)  

#27 0x55f0e4333c2a (/home/ori/asan-linux-release-977036/chrome+0xdf7cc2a) (BuildId: 16aaf0f432fe0664)

0x6100001c9450 is located 16 bytes inside of 192-byte region [0x6100001c9440,0x6100001c9500)  

freed by thread T0 (chrome) here:  

#0 0x55f0e4331c6d (/home/ori/asan-linux-release-977036/chrome+0xdf7ac6d) (BuildId: 16aaf0f432fe0664)  

#1 0x55f0feef614b (/home/ori/asan-linux-release-977036/chrome+0x28b3f14b) (BuildId: 16aaf0f432fe0664)  

#2 0x55f0feef5cff (/home/ori/asan-linux-release-977036/chrome+0x28b3ecff) (BuildId: 16aaf0f432fe0664)  

#3 0x55f0feef5ad1 (/home/ori/asan-linux-release-977036/chrome+0x28b3ead1) (BuildId: 16aaf0f432fe0664)  

#4 0x55f0feef167d (/home/ori/asan-linux-release-977036/chrome+0x28b3a67d) (BuildId: 16aaf0f432fe0664)  

#5 0x55f0f8461ba3 (/home/ori/asan-linux-release-977036/chrome+0x220aaba3) (BuildId: 16aaf0f432fe0664)  

#6 0x55f0f8450465 (/home/ori/asan-linux-release-977036/chrome+0x22099465) (BuildId: 16aaf0f432fe0664)  

#7 0x55f0ffa28bf6 (/home/ori/asan-linux-release-977036/chrome+0x29671bf6) (BuildId: 16aaf0f432fe0664)  

#8 0x55f0ffa29697 (/home/ori/asan-linux-release-977036/chrome+0x29672697) (BuildId: 16aaf0f432fe0664)  

#9 0x55f0e7586ffb (/home/ori/asan-linux-release-977036/chrome+0x111cfffb) (BuildId: 16aaf0f432fe0664)  

#10 0x55f0f3de5cd2 (/home/ori/asan-linux-release-977036/chrome+0x1da2ecd2) (BuildId: 16aaf0f432fe0664)  

#11 0x55f0f3df9027 (/home/ori/asan-linux-release-977036/chrome+0x1da42027) (BuildId: 16aaf0f432fe0664)  

#12 0x55f0f3de8cb6 (/home/ori/asan-linux-release-977036/chrome+0x1da31cb6) (BuildId: 16aaf0f432fe0664)  

#13 0x55f0f3dab961 (/home/ori/asan-linux-release-977036/chrome+0x1d9f4961) (BuildId: 16aaf0f432fe0664)  

#14 0x55f0f3da55d3 (/home/ori/asan-linux-release-977036/chrome+0x1d9ee5d3) (BuildId: 16aaf0f432fe0664)  

#15 0x55f0f2603726 (/home/ori/asan-linux-release-977036/chrome+0x1c24c726) (BuildId: 16aaf0f432fe0664)  

#16 0x55f0f26453c7 (/home/ori/asan-linux-release-977036/chrome+0x1c28e3c7) (BuildId: 16aaf0f432fe0664)  

#17 0x55f0f2644ac7 (/home/ori/asan-linux-release-977036/chrome+0x1c28dac7) (BuildId: 16aaf0f432fe0664)  

#18 0x55f0f2646061 (/home/ori/asan-linux-release-977036/chrome+0x1c28f061) (BuildId: 16aaf0f432fe0664)  

#19 0x55f0f278765d (/home/ori/asan-linux-release-977036/chrome+0x1c3d065d) (BuildId: 16aaf0f432fe0664)  

#20 0x55f0f264671a (/home/ori/asan-linux-release-977036/chrome+0x1c28f71a) (BuildId: 16aaf0f432fe0664)  

#21 0x55f0f257d79c (/home/ori/asan-linux-release-977036/chrome+0x1c1c679c) (BuildId: 16aaf0f432fe0664)  

#22 0x55f0e8fdd5f4 (/home/ori/asan-linux-release-977036/chrome+0x12c265f4) (BuildId: 16aaf0f432fe0664)  

#23 0x55f0e8fe1c71 (/home/ori/asan-linux-release-977036/chrome+0x12c2ac71) (BuildId: 16aaf0f432fe0664)  

#24 0x55f0e8fd786a (/home/ori/asan-linux-release-977036/chrome+0x12c2086a) (BuildId: 16aaf0f432fe0664)  

#25 0x55f0f235ae8f (/home/ori/asan-linux-release-977036/chrome+0x1bfa3e8f) (BuildId: 16aaf0f432fe0664)  

#26 0x55f0f235d9ef (/home/ori/asan-linux-release-977036/chrome+0x1bfa69ef) (BuildId: 16aaf0f432fe0664)  

#27 0x55f0f235ce28 (/home/ori/asan-linux-release-977036/chrome+0x1bfa5e28) (BuildId: 16aaf0f432fe0664)  

#28 0x55f0f2357609 (/home/ori/asan-linux-release-977036/chrome+0x1bfa0609) (BuildId: 16aaf0f432fe0664)  

#29 0x55f0f2357c85 (/home/ori/asan-linux-release-977036/chrome+0x1bfa0c85) (BuildId: 16aaf0f432fe0664)

previously allocated by thread T0 (chrome) here:  

#0 0x55f0e433140d (/home/ori/asan-linux-release-977036/chrome+0xdf7a40d) (BuildId: 16aaf0f432fe0664)  

#1 0x55f0feef0e0d (/home/ori/asan-linux-release-977036/chrome+0x28b39e0d) (BuildId: 16aaf0f432fe0664)  

#2 0x55f0f9afc522 (/home/ori/asan-linux-release-977036/chrome+0x23745522) (BuildId: 16aaf0f432fe0664)  

#3 0x55f0ff199f70 (/home/ori/asan-linux-release-977036/chrome+0x28de2f70) (BuildId: 16aaf0f432fe0664)  

#4 0x55f0ea016385 (/home/ori/asan-linux-release-977036/chrome+0x13c5f385) (BuildId: 16aaf0f432fe0664)  

#5 0x55f0ea0132d9 (/home/ori/asan-linux-release-977036/chrome+0x13c5c2d9) (BuildId: 16aaf0f432fe0664)  

#6 0x55f0e86b9d27 (/home/ori/asan-linux-release-977036/chrome+0x12302d27) (BuildId: 16aaf0f432fe0664)  

#7 0x55f0f3de5a46 (/home/ori/asan-linux-release-977036/chrome+0x1da2ea46) (BuildId: 16aaf0f432fe0664)  

#8 0x55f0f3df9027 (/home/ori/asan-linux-release-977036/chrome+0x1da42027) (BuildId: 16aaf0f432fe0664)  

#9 0x55f0f3de8cb6 (/home/ori/asan-linux-release-977036/chrome+0x1da31cb6) (BuildId: 16aaf0f432fe0664)  

#10 0x55f0f3dab961 (/home/ori/asan-linux-release-977036/chrome+0x1d9f4961) (BuildId: 16aaf0f432fe0664)  

#11 0x55f0f3da55d3 (/home/ori/asan-linux-release-977036/chrome+0x1d9ee5d3) (BuildId: 16aaf0f432fe0664)  

#12 0x55f0f2603726 (/home/ori/asan-linux-release-977036/chrome+0x1c24c726) (BuildId: 16aaf0f432fe0664)  

#13 0x55f0f26453c7 (/home/ori/asan-linux-release-977036/chrome+0x1c28e3c7) (BuildId: 16aaf0f432fe0664)  

#14 0x55f0f2644ac7 (/home/ori/asan-linux-release-977036/chrome+0x1c28dac7) (BuildId: 16aaf0f432fe0664)  

#15 0x55f0f2646061 (/home/ori/asan-linux-release-977036/chrome+0x1c28f061) (BuildId: 16aaf0f432fe0664)  

#16 0x55f0f278765d (/home/ori/asan-linux-release-977036/chrome+0x1c3d065d) (BuildId: 16aaf0f432fe0664)  

#17 0x55f0f264671a (/home/ori/asan-linux-release-977036/chrome+0x1c28f71a) (BuildId: 16aaf0f432fe0664)  

#18 0x55f0f257d79c (/home/ori/asan-linux-release-977036/chrome+0x1c1c679c) (BuildId: 16aaf0f432fe0664)  

#19 0x55f0e8fdd5f4 (/home/ori/asan-linux-release-977036/chrome+0x12c265f4) (BuildId: 16aaf0f432fe0664)  

#20 0x55f0e8fe1c71 (/home/ori/asan-linux-release-977036/chrome+0x12c2ac71) (BuildId: 16aaf0f432fe0664)  

#21 0x55f0e8fd786a (/home/ori/asan-linux-release-977036/chrome+0x12c2086a) (BuildId: 16aaf0f432fe0664)  

#22 0x55f0f235ae8f (/home/ori/asan-linux-release-977036/chrome+0x1bfa3e8f) (BuildId: 16aaf0f432fe0664)  

#23 0x55f0f235d9ef (/home/ori/asan-linux-release-977036/chrome+0x1bfa69ef) (BuildId: 16aaf0f432fe0664)  

#24 0x55f0f235ce28 (/home/ori/asan-linux-release-977036/chrome+0x1bfa5e28) (BuildId: 16aaf0f432fe0664)  

#25 0x55f0f2357609 (/home/ori/asan-linux-release-977036/chrome+0x1bfa0609) (BuildId: 16aaf0f432fe0664)  

#26 0x55f0f2357c85 (/home/ori/asan-linux-release-977036/chrome+0x1bfa0c85) (BuildId: 16aaf0f432fe0664)  

#27 0x55f0e4333c2a (/home/ori/asan-linux-release-977036/chrome+0xdf7cc2a) (BuildId: 16aaf0f432fe0664)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/ori/asan-linux-release-977036/chrome+0x28b3ab43) (BuildId: 16aaf0f432fe0664)  

Shadow bytes around the buggy address:  

0x0c2080031230: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2080031240: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2080031250: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2080031260: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c2080031270: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2080031280: fa fa fa fa fa fa fa fa fd fd[fd]fd fd fd fd fd  

0x0c2080031290: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c20800312a0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c20800312b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c20800312c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c20800312d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: anonymous

## Timeline

### [Deleted User] (2022-03-09)

[Empty comment from Monorail migration]

### aj...@google.com (2022-03-09)

[Empty comment from Monorail migration]

### ke...@google.com (2022-03-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-03-10)

[Comment Deleted]

### ch...@gmail.com (2022-03-15)

Hello, is there anyone to handle this issue?

### ha...@google.com (2022-03-15)

Hey skau@ could you please look into this?

[Monorail components: Internals>Printing]

### th...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

### sk...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-03-29)

[Comment Deleted]

### ch...@gmail.com (2022-03-31)

[Comment Deleted]

### ch...@gmail.com (2022-04-05)

Hello, this is a security bug that can affect stable releases, but has not been handled for a long time. Do you have any plans to deal with it?

### th...@chromium.org (2022-04-05)

+pmonette@: Can you help take a look and see if r985491 took care of this issue?

### pm...@google.com (2022-04-06)

This is a similar report to crbug.com/1306391. So yes, this specific case is fixed.

### [Deleted User] (2022-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-15)

Hello -- thank you for this report. Based on the mitigations of requiring direct user interaction to trigger this issue and report quality, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@chromium.org (2022-04-15)

setting labels to stop bug nags, FoundIn-100 since this is the oldest active release channel and this issue has existed well before this milestone
SI-none only because the CL was landed in another bug (to which this issue should be merged into, but this was the earlier report of this issue), so want to disable any sheriffbot merge processes. 



### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1304884?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059038)*
