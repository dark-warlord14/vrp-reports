# Security: Navigating to "chrome://" URLs inside pdf (iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40083877](https://issues.chromium.org/issues/40083877) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF, UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2016-03-17 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 49.0.2623.87 (stable 32-bit)  

Operating System: iOS

**REPRODUCTION CASE**  

On my machine (iOS) I can access to "chrome://" URLs via a pdf file and this is bad behavior. PDFs in iOS should not be allowed to navigate to "chrome://" URLs

This was fixed in <https://crbug.com/chromium/528505>, but didn't fixed for iOS.

## Attachments

- [testcase.pdf](attachments/testcase.pdf) (application/pdf, 45.4 KB)

## Timeline

### me...@chromium.org (2016-03-17)

Lucas, can you check if the POC works on iOS? 

### me...@chromium.org (2016-03-18)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### lg...@chromium.org (2016-03-18)

Confirmed.

### me...@chromium.org (2016-03-18)

Thanks!
+creis and tsepez, any thoughts?

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-05-13)

Any updates on this report?

### cr...@chromium.org (2016-05-13)

eugenebut@: Did this bug get fixed as well as part of https://crbug.com/chromium/604086?

### eu...@chromium.org (2016-05-13)

Yes, Claude could you please ask QA to retest.

### ch...@gmail.com (2016-05-13)

Verified on 50.0.2661.9. Fixed.

### sh...@chromium.org (2016-05-14)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-05-25)

Reward-topanel?

### eu...@chromium.org (2016-05-25)

CC felt@ to evaluate https://crbug.com/chromium/595514#c11.

### mb...@chromium.org (2016-05-25)

Should be fine to take it to the panel. It's not guaranteed that it will be rewarded, but it should be evaluated.

### fe...@chromium.org (2016-06-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

Congratulations, the panel has decided to award $500 for this bug.  Our finance team will be in touch in the next few weeks with more details.

### eu...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/595514?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Plugins>PDF, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083877)*
