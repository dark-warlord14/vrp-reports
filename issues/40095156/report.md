# UAF in content::IndexedDBOriginState::AbortAllTransactions

| Field | Value |
|-------|-------|
| **Issue ID** | [40095156](https://issues.chromium.org/issues/40095156) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2019-05-24 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Build asan version of chromium. 
2. Make a dir named mojotest in out/gen and set up a webserver in mojotest.Put crash.html in it.
3. Run ./chrome  crash.html 

What is the expected behavior?

What went wrong?
Can stably get UAF crash.

It's another problem after fix the https://crbug.com/chromium/966762.

Did this work before? N/A 

Chrome version: 76.0.3804.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ts...@chromium.org (2019-05-24)

The previous indexeddb bugs have been marked sev critical, feel free to downgrade as appropriate.

### ts...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>IndexedDB]

### dm...@chromium.org (2019-05-24)

Same root cause as https://crbug.com/chromium/966762

### dm...@chromium.org (2019-05-24)

Actually - different code issue, so not a duplicate. Similar, though.

### dm...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e4760e8ba5684222adedef2205b1e74fc4f4babc

commit e4760e8ba5684222adedef2205b1e74fc4f4babc
Author: Daniel Murphy <dmurph@chromium.org>
Date: Fri May 24 23:06:55 2019

[IndexedDB] Handle OriginState reentry during transaction abort

Aborting transactions can cause databases to be deleted. This caused
reentry in the OriginState while iterating the databases_ map in
AbortAllTransactions. This change grabs the keys to the map first, so
it can iterate the keys instead of the map.

R: pwnall@chromium.org
Bug: 966784
Change-Id: I42a8710aff9d25deb3d9eace9fa06654bba46507
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1629190
Reviewed-by: Victor Costan <pwnall@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/master@{#663308}

[modify] https://crrev.com/e4760e8ba5684222adedef2205b1e74fc4f4babc/content/browser/indexed_db/indexed_db_origin_state.cc


### sh...@chromium.org (2019-05-25)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-25)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2019-05-28)

The cause of this bug landed in M76. The fix above is included in M76. I don't think there's anything else to do here.

### sh...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

### aw...@google.com (2019-05-28)

Security_Impact-Head to match https://crbug.com/chromium/966784#c9

### aw...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-29)

Congrats! The Panel decided to reward $5,000 for this report!

### aw...@google.com (2019-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wi...@gmail.com (2021-06-10)

Now, can we still have the crash.html?

### is...@google.com (2021-06-10)

This issue was migrated from crbug.com/chromium/966784?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/966762]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095156)*
