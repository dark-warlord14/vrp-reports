# Email with multiple attribute and datalist may scramble field values on autocomplete

| Field | Value |
|-------|-------|
| **Issue ID** | [41336093](https://issues.chromium.org/issues/41336093) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Forms>Datalist, UI>Browser>Autofill |
| **Platforms** | Linux, Windows |
| **Reporter** | va...@gmail.com |
| **Assignee** | mg...@chromium.org |
| **Created** | 2017-07-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36

Steps to reproduce the problem:
1. Open about:blank and inject the following into the body
<form>
   <input type="email" multiple="multiple" autocapitalize="off" list="emailsfield-1-list">
   <datalist id="emailsfield-1-list">
      <option>a@a.test.ch</option>
      <option>test@valio.ch</option>
   </datalist>
</form>
2. Focus the field, type an "a"
3. Use the ARROW keys and select "a@a.test.ch" with ENTER => "a@a.test.ch" is the field value
4. Type ",t"
5. Use the ARROW keys and select "test@valio.ch" with ENTER

What is the expected behavior?
"a@a.test.ch,test@valio.ch" is the field value

What went wrong?
"test@valio.,test@valio.ch" is the new field value

Did this work before? N/A 

Chrome version: 60.0.3112.78  Channel: stable
OS Version: 10.0
Flash Version: 

I had similar odd results when I was fiddling with email addresses that will hardly occur in reality (e.g. try [a@a.ch, ba@a.ch] as options and in step 4 don't type anything; then the first charcode will become 0, instead of 97/"a").

I assume that there is some RegExp magic in the background that fails sometimes to perform as intended.

## Timeline

### va...@gmail.com (2017-07-27)

About that second example I mentioned: in step 4 you'd have to type a "," of course, but not any letter. Mea culpa.

### ny...@chromium.org (2017-07-28)

[Empty comment from Monorail migration]

### ka...@chromium.org (2017-07-28)

Able to reproduce the issue on windows 7, Ubuntu 14.04 using chrome version 60.0.3112.78  and canary 62.0.3168.0.
This is regression issue broken in M59.Please find the bisect information as below

Narrow Bisect::
Good:: 59.0.3054.0   ---  (Revision 459950)
Bad:: 59.0.3055.0   ---  (Revision 460255)

Change Log::
https://chromium.googlesource.com/chromium/src/+log/4c370c113bf4cc5369818f8ab72027d8c1865676..30f7588201a275c75d0382ad4d63d4329a2fd9e8

Possible suspect::
https://chromium.googlesource.com/chromium/src/+/30f7588201a275c75d0382ad4d63d4329a2fd9e8

mgiuca@ could you please look into this issue if it is related to your change,else please help us in finding the appropriate owner for this issue.

Thanks,

### rb...@chromium.org (2017-07-28)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>Forms>Datalist UI>Browser>Autofill]

### mg...@chromium.org (2017-07-31)

I just tried to repro this on Linux and got:
"◌ః⢀ﵰ￿츣仕�￿.ch,test@valio.ch"

This looks like a buffer overrun; marking as security as I continue to investigate.

### mg...@chromium.org (2017-07-31)

Got it, the suspect CL (r459983) introduced a use-after-free in AutofillAgent::DoAcceptDataListSuggestion.

-    std::vector<base::string16> parts = base::SplitString(
+    std::vector<base::StringPiece16> parts = base::SplitStringPiece(
         input_element->editingValue().utf16(), base::ASCIIToUTF16(","),
         base::KEEP_WHITESPACE, base::SPLIT_WANT_ALL);

input_element->editingValue().utf16() is temporary so the resulting StringPiece16s point at freed memory.

Mitigations:
- This is user-controlled, not site-controlled (JavaScript code can't trigger it).
- This can only be used to read freed memory, not write it.
- Code runs in renderer, not browser.

Keeping this as severity medium. Probably not worth a stable merge but definitely a beta merge. Fix incoming.

valiodotch@: Please refrain from discussing this outside of this bug page for the time being (https://www.chromium.org/Home/chromium-security/reporting-security-bugs). Thanks.

### va...@gmail.com (2017-07-31)

mgiuca@ Thanks for the precaution note. 
I will refrain from discussing this anywhere else.

### mg...@chromium.org (2017-07-31)

CL: https://chromium-review.googlesource.com/c/593428/

+vabr for review. Note that I was vague in the CL description due to the security sensitive nature of the bug being fixed.

valiodotch@: Thanks, and thanks for the bug report. It's appreciated.

### bu...@chromium.org (2017-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93bc1587148b876300ef5d9f4700fa55db00c194

commit 93bc1587148b876300ef5d9f4700fa55db00c194
Author: Matt Giuca <mgiuca@chromium.org>
Date: Tue Aug 01 05:09:57 2017

Fix AutofillAgent::DoAcceptDataListSuggestion string splicing.

Store the intermediate value in a string variable rather than using a
temporary.

Adds a browser test for DoAcceptDataListSuggestion that would've failed.

Bug: 749451
Change-Id: I0bb14330ed6f0e9e110b8abedaec06e3e3d05317
Reviewed-on: https://chromium-review.googlesource.com/593428
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Vaclav Brozek <vabr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#490853}
[modify] https://crrev.com/93bc1587148b876300ef5d9f4700fa55db00c194/chrome/renderer/autofill/form_autocomplete_browsertest.cc
[modify] https://crrev.com/93bc1587148b876300ef5d9f4700fa55db00c194/components/autofill/content/renderer/autofill_agent.cc


### mg...@chromium.org (2017-08-01)

This should fix the issue.

Requesting a merge to M61. Rationale: Security (though note the mitigations listed in #6). Simple 2-line fix (excluding tests).

Although this was actually a regression in M59, I don't think it's worth merging to stable (due to the mitigations listed above). But still worth fixing on the beta branch.

### sh...@chromium.org (2017-08-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-02)

Your change meets the bar and is auto-approved for M61. Please go ahead and merge the CL to branch 3163 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid @(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mg...@chromium.org (2017-08-02)

Waiting for confirmation on Canary tomorrow.

Also adding reward-topanel (see https://www.google.com/about/appsecurity/chrome-rewards/). Notes for panel:

- Bug was reported publicly (not as security). There was nothing in the original bug report to directly suggest that this was a security issue, until it was investigated further.
- Bug was marked private before discussion of security issue was started, so it may still qualify.
- See Mitigations in #6 (this was a fairly minor issue).

### mg...@chromium.org (2017-08-03)

Confirmed fixed on Canary 62.0.3174.1. Merging to 3163.

### bu...@chromium.org (2017-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f8ccdde3ebcc38814fb8c39b833e1e1b31f1c508

commit f8ccdde3ebcc38814fb8c39b833e1e1b31f1c508
Author: Matt Giuca <mgiuca@chromium.org>
Date: Thu Aug 03 01:19:38 2017

Fix AutofillAgent::DoAcceptDataListSuggestion string splicing.

Store the intermediate value in a string variable rather than using a
temporary.

Adds a browser test for DoAcceptDataListSuggestion that would've failed.

TBR=mgiuca@chromium.org

(cherry picked from commit 93bc1587148b876300ef5d9f4700fa55db00c194)

Bug: 749451
Change-Id: I0bb14330ed6f0e9e110b8abedaec06e3e3d05317
Reviewed-on: https://chromium-review.googlesource.com/593428
Commit-Queue: Matt Giuca <mgiuca@chromium.org>
Reviewed-by: Vaclav Brozek <vabr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#490853}
Reviewed-on: https://chromium-review.googlesource.com/598659
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#262}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/f8ccdde3ebcc38814fb8c39b833e1e1b31f1c508/chrome/renderer/autofill/form_autocomplete_browsertest.cc
[modify] https://crrev.com/f8ccdde3ebcc38814fb8c39b833e1e1b31f1c508/components/autofill/content/renderer/autofill_agent.cc


### go...@chromium.org (2017-08-03)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-08-03)

Rechecked this issue on Ubuntu 14.04 using build 61.0.3163.31 and fix is working as intended. 

Not adding TE-verified labels as, could not verify on Windows OS as builds are not yet available (till 6:40 PM IST)

Request @pbomanna to take a look into it.

Thanks.!

### pb...@chromium.org (2017-08-03)

Verified the issue on Windows 7 and 10 with chrome 61.0.3163.31.

### aw...@chromium.org (2017-08-09)

Changing severity to low after VRP panel review, per mitigations mentioned in #6

### aw...@chromium.org (2017-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-09)

Nice one! The VRP panel decided to award $500 for this report.  A member of our finance team will be in touch to arrange payment.

Also, how would you like to be credited if this bug is mentioned in release notes?

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@gmail.com (2017-11-29)

Nice! :)

If it's still possible to set the credits, please use 
"Pat Mächler, ICFM AG, Urdorf"

Sorry, for the delayed response. I accidentally used a GMail account for reporting this issue, that I actually only use for certain Google services (but not as a mail address). 

### va...@chromium.org (2018-11-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-29)

This issue was migrated from crbug.com/chromium/749451?no_tracker_redirect=1

[Multiple monorail components: Blink>Forms>Datalist, UI>Browser>Autofill]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41336093)*
