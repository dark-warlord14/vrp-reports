# Heap-use-after-free in WebCore::ImageInputType::attach

| Field | Value |
|-------|-------|
| **Issue ID** | [40077544](https://issues.chromium.org/issues/40077544) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2013-05-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with input type image

**VERSION**  

Chrome Version:stable +dev  

Operating System: 64bit ubuntu

**REPRODUCTION CASE**

<html>
<body>
<input id="x" type="image" onerror="x.type=''" src="" />
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==6146==ERROR: AddressSanitizer: heap-use-after-free on address 0x61900189f608 at pc 0x55555a6e4c2b bp 0x7fffffffb140 sp 0x7fffffffb138  

READ of size 8 at 0x61900189f608 thread T0 (asan-release)  

#0 0x55555a6e4c2a in element /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/core/html/InputType.h:309  

#1 0x55555a3fd185 in attach /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/core/html/HTMLInputElement.cpp:775  

#2 0x55555a71b496 in insert /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp:110  

#3 0x55555a70d618 in executeInsertTask

0x61900189f608 is located 8 bytes inside of 24-byte region [0x61900189f600,0x61900189f618)  

freed by thread T0 (asan-release) here:  

#0 0x555556a092c2 in operator delete(void\*) ??:0  

#1 0x55555a3f7eab in deleteOwnedPtr[WebCore::InputType](javascript:void(0);) /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/wtf/OwnPtrCommon.h:47  

#2 0x55555a3fa81f in parseAttribute /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/core/html/HTMLInputElement.cpp:627  

#3 0x55555943a719 in attributeChanged

## Attachments

- [image-stable.txt](attachments/image-stable.txt) (text/plain; charset=us-ascii, 13.9 KB)
- [image.html](attachments/image.html) (text/html; charset=us-ascii, 95 B)
- [image.txt](attachments/image.txt) (text/plain; charset=us-ascii, 11.3 KB)

## Timeline

### pa...@chromium.org (2013-05-13)

https://cluster-fuzz.appspot.com/testcase?key=184493044

### in...@chromium.org (2013-05-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=183664630

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60a00008e928
Crash State:
  - crash stack -
  WebCore::ImageInputType::attach
  WebCore::HTMLInputElement::attach
  - free stack -
  WebCore::HTMLInputElement::updateType
  WebCore::HTMLInputElement::parseAttribute
  

Minimized Testcase (0.06 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95hNLuTiMzVvHWwDm2jI-dV4Oj93HFFn_WfFc5KFr6LgOFmGMAGpzHM04iP9AZIqJKkwGmf6F5cx9zTL79MGCBvmdyqtEUbQjf75gAZ1m6gch3jd3Qg3-hK8dUWcdWZFdgxe37oKEwYb-107c5dhbNrEKK5D2QOCxElbgUj1cm2sQEElZQ
<input id="x" type="image" onerror="x.type=''" src=""</body>

### pa...@chromium.org (2013-05-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-13)

        // Fire an error event if the url is empty.
        // FIXME: Should we fire this event asynchronoulsy via errorEventSender()?
        m_element->dispatchEvent(Event::create(eventNames().errorEvent, false, false));
    }

### in...@chromium.org (2013-05-13)

https://codereview.chromium.org/14741011/

### in...@chromium.org (2013-05-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-05-13)

------------------------------------------------------------------------
r150232 | inferno@chromium.org | 2013-05-13T17:29:52.573822Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/image/image-error-event-crash.html?r1=150232&r2=150231&pathrev=150232
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/image/image-error-event-crash-expected.txt?r1=150232&r2=150231&pathrev=150232
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/ImageLoader.cpp?r1=150232&r2=150231&pathrev=150232

Error event was fired synchronously blowing away the input element from underneath. Remove the FIXME and fire it asynchronously using errorEventSender().

BUG=240124

Review URL: https://chromiumcodereview.appspot.com/14741011
------------------------------------------------------------------------

### in...@chromium.org (2013-05-13)

https://src.chromium.org/viewvc/blink?view=rev&revision=150232

### cl...@chromium.org (2013-05-14)

ClusterFuzz has detected this issue as fixed in range 199907:199944.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=183664630

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60a00008e928
Crash State:
  - crash stack -
  WebCore::ImageInputType::attach
  WebCore::HTMLInputElement::attach
  - free stack -
  WebCore::HTMLInputElement::updateType
  WebCore::HTMLInputElement::parseAttribute
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=199907:199944

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95hNLuTiMzVvHWwDm2jI-dV4Oj93HFFn_WfFc5KFr6LgOFmGMAGpzHM04iP9AZIqJKkwGmf6F5cx9zTL79MGCBvmdyqtEUbQjf75gAZ1m6gch3jd3Qg3-hK8dUWcdWZFdgxe37oKEwYb-107c5dhbNrEKK5D2QOCxElbgUj1cm2sQEElZQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-05-28)

M27 is r151280
M28 is r151281

### sc...@gmail.com (2013-06-03)

$1000

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/240124?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077544)*
