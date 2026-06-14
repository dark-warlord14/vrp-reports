# Security: METHOD_LOCALTIME browser->renderer infoleak

| Field | Value |
|-------|-------|
| **Issue ID** | [40089016](https://issues.chromium.org/issues/40089016) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | vi...@microsoft.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2017-09-15 |
| **Bounty** | $3,337.00 |

## Description

VULNERABILITY DETAILS

In the IPC method METHOD_LOCALTIME there is a full pointer infoleak when Chromium is built against glibc on Linux.

The bug is in the function HandleLocaltime(...).
It sends an entire “struct tm” from the browser process to renderer:

  const struct tm* expanded_time = localtime(&time);
  // ...
  result_string = std::string(reinterpret_cast<const char*>(expanded_time),
                             sizeof(struct tm));

Inspecting “struct tm” in glibc, it looks like this:

struct tm
{
  int tm_sec;
  int tm_min;
  int tm_hour;
  int tm_mday;
  int tm_mon;
  int tm_year;
  int tm_wday;
  int tm_yday;
  int tm_isdst;

# ifdef              __USE_BSD
  long int tm_gmtoff;
  const char *tm_zone;
# else
  long int __tm_gmtoff;
  const char *__tm_zone;
# endif
};

The struct has GNU extensions: a pointer “tm_zone” is accidentally sent from browser to renderer.

Further, on 64-bit builds, there is 4 byte of padding between members tm_isdst and tm_gmtoff that also gets sent.


VERSION
Chrome Version: 61.0.3163.91
Operating System: Linux, ChromeOS

REPRODUCTION CASE

[Step A] Attach to a renderer process, put a breakpoint on the first memcpy() in ProxyLocaltimeCallToBrowser(...).

[Step B] Inspect the contents at src+0x30 (in this case the memcpy was inlined):

(gdb) p/x $rcx
$1 = 0x33be3209ec90

[Step C] Verify this is not a valid pointer in renderer.

(gdb) x $rcx
0x33be3209ec90: Cannot access memory at address 0x33be3209ec90

[Step D] Verify this pointer is valid in the browser process (in this case browser pid=4782).

$ cat /proc/4782/maps | grep 0x33be320
33be31ff6000-33be32015000 rw-p 00000000 00:00 0 
33be32015000-33be32016000 ---p 00000000 00:00 0 
33be32016000-33be3204c000 rw-p 00000000 00:00 0 
33be3204c000-33be3204d000 ---p 00000000 00:00 0 
33be3204d000-33be32f7c000 rw-p 00000000 00:00 0


## Timeline

### me...@chromium.org (2017-09-15)

Thank you for the report once again!

jorgelo: Mind if I assign this to you? Feel free to reassign.

[Monorail components: Internals>Sandbox]

### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-09-22)

I'll look into fixing this while jorgelo is OOO.

### bu...@chromium.org (2017-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc5edc9c05901feeac616c075d0337e634f3a02a

commit dc5edc9c05901feeac616c075d0337e634f3a02a
Author: Chris Palmer <palmer@chromium.org>
Date: Sat Sep 23 21:59:41 2017

Serialize struct tm in a safe way.

BUG=765512

Change-Id: If235b8677eb527be2ac0fe621fc210e4116a7566
Reviewed-on: https://chromium-review.googlesource.com/679441
Commit-Queue: Chris Palmer <palmer@chromium.org>
Reviewed-by: Julien Tinnes <jln@chromium.org>
Cr-Commit-Position: refs/heads/master@{#503948}
[modify] https://crrev.com/dc5edc9c05901feeac616c075d0337e634f3a02a/content/browser/sandbox_ipc_linux.cc
[modify] https://crrev.com/dc5edc9c05901feeac616c075d0337e634f3a02a/content/zygote/zygote_main_linux.cc


### pa...@chromium.org (2017-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-24)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-09-27)

Thanks for fixing Chris!

### aw...@chromium.org (2017-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-27)

+awhalley@ (Security TPM) for M63 merge review

### aw...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dc5edc9c05901feeac616c075d0337e634f3a02a

commit dc5edc9c05901feeac616c075d0337e634f3a02a
Author: Chris Palmer <palmer@chromium.org>
Date: Sat Sep 23 21:59:41 2017

Serialize struct tm in a safe way.

BUG=765512

Change-Id: If235b8677eb527be2ac0fe621fc210e4116a7566
Reviewed-on: https://chromium-review.googlesource.com/679441
Commit-Queue: Chris Palmer <palmer@chromium.org>
Reviewed-by: Julien Tinnes <jln@chromium.org>
Cr-Commit-Position: refs/heads/master@{#503948}

[modify] https://crrev.com/dc5edc9c05901feeac616c075d0337e634f3a02a/content/zygote/zygote_main_linux.cc
[modify] https://crrev.com/dc5edc9c05901feeac616c075d0337e634f3a02a/content/browser/sandbox_ipc_linux.cc


### is...@google.com (2023-03-04)

This issue was migrated from crbug.com/chromium/765512?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089016)*
