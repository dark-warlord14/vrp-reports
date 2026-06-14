# Security: Chrome shared memory file can be world readable and lacks security checks when opening existing mappings.

| Field | Value |
|-------|-------|
| **Issue ID** | [40077703](https://issues.chromium.org/issues/40077703) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, ChromeOS |
| **Reporter** | jl...@chromium.org |
| **Assignee** | jl...@chromium.org |
| **Created** | 2013-06-25 |
| **Bounty** | $500.00 |

## Description

Initially seen in http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=709413

It looks like SharedMemory::Create and the subsequently called functions don't do anything about the user's default umask. Files seem to be created with that umask.

Any temporary file should be only readable to the current user.

## Timeline

### jl...@chromium.org (2013-06-25)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-06-26)

https://codereview.chromium.org/17779002 up.

### jl...@chromium.org (2013-07-02)

Looks like Android is vulnerable as well and it could be worse on that OS. I need to take a look.

### jl...@chromium.org (2013-07-02)

Adding Christian, the original reporter to the bug.

### sc...@gmail.com (2013-07-02)

It's a good catch. We recently started using POSIX SHM more heavily for some builds of Chrome (including Chrome OS and Android, plus the Aura build of Linux desktop). In particular, we started using POSIX SHM to transport rendered web pages from renderer to browser, so there is definitely sensitive content.

I suspect the bug has always been there, it just got more obvious recently.

### jl...@chromium.org (2013-07-02)

In addition to Christian's report on file permissions, I'm fixing the two following issues:

- When opening an existing file, make sure we're not tricked into opening a file planted by an attacker.
- When opening an existing shared memory file, check for an attacker tricking us into opening another file via a symlink.

### bu...@chromium.org (2013-07-02)

------------------------------------------------------------------------
r209814 | jln@chromium.org | 2013-07-02T23:31:55.432358Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/memory/shared_memory_posix.cc?r1=209814&r2=209813&pathrev=209814
   M http://src.chromium.org/viewvc/chrome/trunk/src/base/memory/shared_memory_unittest.cc?r1=209814&r2=209813&pathrev=209814

Posix: fix named SHM mappings permissions.

Make sure that named mappings in /dev/shm/ aren't created with
broad permissions.

BUG=254159
R=mark@chromium.org, markus@chromium.org

Review URL: https://codereview.chromium.org/17779002
------------------------------------------------------------------------

### jl...@chromium.org (2013-07-11)

I would like to merge this security fix to M29, is the branch open ?

### ke...@google.com (2013-07-12)

How safe is this?

### jl...@chromium.org (2013-07-12)

It's Mac / Linux only. I'd say it's fairly safe to merge, but not "absolutely" safe.

### ke...@google.com (2013-07-12)

Please keep a close eye on it in beta and on trunk.

### bu...@chromium.org (2013-07-12)

------------------------------------------------------------------------
r211461 | jln@chromium.org | 2013-07-12T21:32:04.715122Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1547/src/base/memory/shared_memory_unittest.cc?r1=211461&r2=211460&pathrev=211461
   M http://src.chromium.org/viewvc/chrome/branches/1547/src/base/memory/shared_memory_posix.cc?r1=211461&r2=211460&pathrev=211461

Merge 209814 "Posix: fix named SHM mappings permissions."

> Posix: fix named SHM mappings permissions.
> 
> Make sure that named mappings in /dev/shm/ aren't created with
> broad permissions.
> 
> BUG=254159
> R=mark@chromium.org, markus@chromium.org
> 
> Review URL: https://codereview.chromium.org/17779002

TBR=jln@chromium.org

Review URL: https://codereview.chromium.org/19106006
------------------------------------------------------------------------

### jl...@chromium.org (2013-07-19)

[Empty comment from Monorail migration]

### be...@chromium.org (2013-07-23)

Is this merged to M-29?  If so, please update the merge label to "Merge-Merged" before closing the bug.

### jl...@chromium.org (2013-07-23)

The bot updated with merge-merged-1547. Is there a manual step to do ? I don't remember ever doing something manually.

### sc...@gmail.com (2013-07-31)

- Merge-Approved -> Merge-Merged
- Added Release-0
- Restrict-View set to Notify

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

Hey Christian,

The reward panel would like to send you $500 for this security bug :) Someone should get in contact within the next 2 weeks to get some payment info.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
          *********************************

### pa...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### kr...@chromium.org (2013-11-19)

Old bugs that are for milestones that are way before the current stable.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/254159?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077703)*
