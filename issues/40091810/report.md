# chrome_1c30000!webkit::ppapi::PPB_Widget_Impl::Invalidate crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40091810](https://issues.chromium.org/issues/40091810) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals, Internals>Plugins, Internals>Plugins>Pepper |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-06-11 |
| **Bounty** | $500.00 |

## Description

Test chrome 13.0.782.14 windows xp sp3

Open testcase.htm

(a40.c74): Access violation - code c0000005 (!!! second chance !!!)
eax=019de64d ebx=056fa870 ecx=0117e154 edx=026632f7 esi=056fa870 edi=056fa8a4
eip=31018300 esp=0012f7f8 ebp=0012f84c iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000202
31018300 ??              ???
0:000> .exr -1
ExceptionAddress: 31018300
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 31018300
Attempt to execute non-executable address 31018300

(460.c0c): Access violation - code c0000005 (!!! second chance !!!)
eax=077d36e0 ebx=011e9b40 ecx=011e9b40 edx=026632f7 esi=011e9b40 edi=011e9b74
eip=0265a711 esp=0012f804 ebp=0012f84c iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
chrome_1c30000!webkit::ppapi::PPB_Widget_Impl::Invalidate+0x8:
0265a711 8b4008          mov     eax,dword ptr [eax+8] ds:0023:077d36e8=????????
0:000> .exr -1
ExceptionAddress: 0265a711 (chrome_1c30000!webkit::ppapi::PPB_Widget_Impl::Invalidate+0x00000008)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 077d36e8
Attempt to read from address 077d36e8

## Attachments

- [testcase.htm](attachments/testcase.htm) (text/html; charset=us-ascii, 310 B)
- [log1.txt](attachments/log1.txt) (text/x-c; charset=us-ascii, 4.2 KB)
- [log.txt](attachments/log.txt) (text/x-c; charset=us-ascii, 4.8 KB)

## Timeline

### ku...@gmail.com (2011-06-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-06-11)

[Empty comment from Monorail migration]

### pi...@chromium.org (2011-06-11)

Flash doesn't use PPB_Widget, so it shouldn't be vulnerable

### [Deleted User] (2011-06-13)

My fix without a bug finally has a bug :)

It's the stale instance hanging off the resource in ppapi. I will upload the fix shortly.

### bu...@chromium.org (2011-06-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=89746

------------------------------------------------------------------------
r89746 | cdn@chromium.org | Mon Jun 20 15:33:52 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/resource.cc?r1=89746&r2=89745&pathrev=89746
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/resource.h?r1=89746&r2=89745&pathrev=89746
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=89746&r2=89745&pathrev=89746
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/resource_tracker.cc?r1=89746&r2=89745&pathrev=89746
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/ppb_widget_impl.cc?r1=89746&r2=89745&pathrev=89746
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/resource_tracker.h?r1=89746&r2=89745&pathrev=89746
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/ppb_url_loader_impl.h?r1=89746&r2=89745&pathrev=89746

Maintain a map of all resources in the resource tracker and clear instance back pointers when needed,

BUG=85808
Review URL: http://codereview.chromium.org/7196001
------------------------------------------------------------------------

### [Deleted User] (2011-06-20)

[Empty comment from Monorail migration]

### er...@chromium.org (2011-06-21)

[Empty comment from Monorail migration]

### er...@chromium.org (2011-06-21)

[Empty comment from Monorail migration]

### er...@chromium.org (2011-06-21)

[Empty comment from Monorail migration]

### er...@chromium.org (2011-06-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-06-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=90056

------------------------------------------------------------------------
r90056 | cevans@chromium.org | Wed Jun 22 11:12:36 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/resource.h?r1=90056&r2=90055&pathrev=90056
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/ppb_url_loader_impl.h?r1=90056&r2=90055&pathrev=90056
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=90056&r2=90055&pathrev=90056
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/ppb_widget_impl.cc?r1=90056&r2=90055&pathrev=90056
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/resource.cc?r1=90056&r2=90055&pathrev=90056
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/resource_tracker.h?r1=90056&r2=90055&pathrev=90056
 M http://src.chromium.org/viewvc/chrome/branches/782/src/webkit/plugins/ppapi/resource_tracker.cc?r1=90056&r2=90055&pathrev=90056

Merge 89746 - Maintain a map of all resources in the resource tracker and clear instance back pointers when needed,

BUG=85808
Review URL: http://codereview.chromium.org/7196001

TBR=cdn@chromium.org
Review URL: http://codereview.chromium.org/7233018
------------------------------------------------------------------------

### sc...@gmail.com (2011-06-22)

(added reward-topanel) -- just as a heads up, this is a tricky reward situation to resolve. Unfortunately, we first noticed the issue due to https://crbug.com/chromium/78639.

### ku...@gmail.com (2011-06-23)

Thank you :)

### sc...@gmail.com (2011-07-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-20)

@kuzzcc: despite technically being a duplicate, your report here was useful to us in fixing a bug, therefore we'd like to offer you a $500 Chromium Security Reward for this help.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/85808?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Internals, Internals>Plugins, Internals>Plugins>Pepper]
[Monorail mergedwith: crbug.com/chromium/81254, crbug.com/chromium/86234, crbug.com/chromium/87881, crbug.com/chromium/89726]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091810)*
