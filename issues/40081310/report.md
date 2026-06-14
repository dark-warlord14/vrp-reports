# Heap Use After Free @blink::BaseMultipleFieldsDateAndTimeInputType::readonlyAttributeChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40081310](https://issues.chromium.org/issues/40081310) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Reporter** | 0i...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2015-02-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

==5060==ERROR: AddressSanitizer: heap-use-after-free on address 0x0be9ee9c at pc 0x132924c1 bp 0xdeadbeef sp 0x002bb378  

READ of size 4 at 0x0be9ee9c thread T0  

#0 0x132924c0 in blink::BaseMultipleFieldsDateAndTimeInputType::readonlyAttributeChanged C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\wtf\RawPtr.h:119  

#1 0x12dddc99 in blink::HTMLInputElement::parseAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\HTMLInputElement.cpp:711  

#2 0x12b6cec1 in blink::Element::attributeChanged C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:1083  

#3 0x12b834b0 in blink::Element::didAddAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:2946  

#4 0x12b82c66 in blink::Element::appendAttributeInternal C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:2087  

#5 0x12b5e4a6 in blink::Element::setAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:1044  

#6 0x12b5df8a in blink::Element::setBooleanAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:330  

#7 0x15425db6 in blink::MediaQueryListEvent::create C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8HTMLFieldSetElement.cpp:63  

#8 0x11f5b023 in v8::internal::PropertyCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:89  

#9 0x116bf7a3 in v8::internal::Object::SetPropertyWithAccessor C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\objects.cc:371  

#10 0x117053ef in v8::internal::Object::SetProperty C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\objects.cc:2826  

#11 0x11f78651 in v8::internal::StoreIC::Store C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\ic\ic.cc:1585  

#12 0x11f8a0d4 in v8::internal::StoreIC\_Miss C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\ic\ic.cc:2390

Output from WinDBG:  

chrome\_child!WTF::OwnPtr[blink::DocumentOrderedMap](javascript:void(0);)::operator! [inlined in chrome\_child!blink::BaseMultipleFieldsDateAndTimeInputType::disabledAttributeChanged+0x85]:  

687c1a19 8b4e14 mov ecx,dword ptr [esi+14h] ds:002b:00000044=????????

**VERSION**  

Stable, asan-win32-release-314088  

Operating System: Windows 7, SP1

**REPRODUCTION CASE**  

Please open attached HTML File.

Type of crash: Tab

This issue (in stack trace) is a little related to already patched issue number 447906, but the way of triggering it, is totally different, thats why I decided to post it as another issue.

## Attachments

- [19519.html](attachments/19519.html) (text/html, 893 B)
- [sym.out](attachments/sym.out) (application/octet-stream, 32.4 KB)
- [19519.html](attachments/19519_53125312.html) (text/html, 321 B)

## Timeline

### cl...@chromium.org (2015-02-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5688691094716416

### in...@chromium.org (2015-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5688691094716416

Uploader: aarya@google.com
Job Type: Windows_asan_chrome

Crash Type: Stack-buffer-overflow READ 1
Crash Address: 0x0034554e
Crash State:
  std::num_get<char,std::istreambuf_iterator<char,std::char_traits<char>
  std::num_get<char,std::istreambuf_iterator<char,std::char_traits<char>
  std::basic_istream<char,std::char_traits<char>
  

Minimized Testcase (0.00 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94cWlOdLjcgGxGm43LOPYtqrwhNGnDv1MfnFruz6kOKyHKUK3wGPY2sqlKTdSqWJ__018ZU02aU1YdQaztt424KPFLc61Y1pS1hIvPZzZeEB2y6lhnDjVArlg2xwSt65UCcvjXQgi7nG2gbOO2QYOURYpLHfQ



### in...@chromium.org (2015-02-02)

Windows Clang ASAN is broken atm. Crashing on startup, please ignore https://cluster-fuzz.appspot.com/testcase?key=5688691094716416

### 0i...@gmail.com (2015-02-02)

Sorry for bug in repro, 
try{try {QMCCDIEF.selectionDirection='ABCD';}catch(e){}}catch(e){}
 <- This line isn't required.

### ri...@chromium.org (2015-02-03)

I hand-minimized it down to the following. I do get a UAF on Linux ASAN even without some of the lines that you needed. Interestingly, it doesn't crash on a non-ASAN build. I assume the new InputType just happens to get allocated where the old InputType was.

I also attached the full ASAN output from Linux.


### cl...@chromium.org (2015-02-03)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-02-06)

The root cause is to dispatch 'change' event unexpectedly.  In the test case, it shouldn't be dispatched.

    frame #42: blink::HTMLFormControlElement::dispatchChangeEvent(this=0x00001683e0a30010) + 69 at HTMLFormControlElement.cpp:311
    frame #43: blink::HTMLTextFormControlElement::dispatchFormControlChangeEvent(this=0x00001683e0a30010) + 132 at HTMLTextFormControlElement.cpp:203
    frame #44: blink::BaseMultipleFieldsDateAndTimeInputType::spinButtonDidReleaseMouseCapture(this=0x0000035b296b1120, eventDispatch=EventDispatchAllowed) + 70 at BaseMultipleFieldsDateAndTimeInputType.cpp:249
    frame #45: non-virtual thunk to blink::BaseMultipleFieldsDateAndTimeInputType::spinButtonDidReleaseMouseCapture(this=0x0000035b296b1158, eventDispatch=EventDispatchAllowed) + 50 at BaseMultipleFieldsDateAndTimeInputType.cpp:250
    frame #46: blink::SpinButtonElement::releaseCapture(this=0x00001683e0a94010, eventDispatch=EventDispatchAllowed) + 304 at SpinButtonElement.cpp:202
    frame #47: blink::BaseMultipleFieldsDateAndTimeInputType::disabledAttributeChanged(this=0x0000035b296b1120) + 52 at BaseMultipleFieldsDateAndTimeInputType.cpp:422
    frame #48: blink::HTMLInputElement::parseAttribute(this=0x00001683e0a30010, name=0x000000010b271bb0, value=0x000000011cd7ff60) + 2806 at HTMLInputElement.cpp:775
    frame #49: blink::Element::attributeChanged(this=0x00001683e0a30010, name=0x000000010b271bb0, newValue=0x000000011cd7ff60, reason=ModifiedDirectly) + 152 at Element.cpp:1067
    frame #50: blink::Element::didAddAttribute(this=0x00001683e0a30010, name=0x000000010b271bb0, value=0x000000011cd7ff60) + 87 at Element.cpp:2930
    frame #51: blink::Element::appendAttributeInternal(this=0x00001683e0a30010, name=0x000000010b271bb0, value=0x000000011cd7ff60, inSynchronizationOfLazyAttribute=NotInSynchronizationOfLazyAttribute) + 153 at Element.cpp:2071
    frame #52: blink::Element::setAttributeInternal(this=0x00001683e0a30010, index=18446744073709551615, name=0x000000010b271bb0, newValue=0x000000011cd7ff60, inSynchronizationOfLazyAttribute=NotInSynchronizationOfLazyAttribute) + 144 at Element.cpp:1028
    frame #53: blink::Element::setAttribute(this=0x00001683e0a30010, name=0x000000010b271bb0, value=0x000000011cd7ff60) + 173 at Element.cpp:1010
    frame #54: blink::Element::setBooleanAttribute(this=0x00001683e0a30010, name=0x000000010b271bb0, value=true) + 78 at Element.cpp:330
    frame #55: blink::HTMLInputElementV8Internal::disabledAttributeSetter(v8Value=Local<v8::Value> at 0x0000000135800818, info=0x0000000135800890) + 205 at V8HTMLInputElement.cpp:305



### bu...@chromium.org (2015-02-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189774

------------------------------------------------------------------
r189774 | tkent@chromium.org | 2015-02-09T03:38:47.083873Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/forms/BaseMultipleFieldsDateAndTimeInputType.cpp?r1=189774&r2=189773&pathrev=189774
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/number/number-change-event-by-readonly-expected.txt?r1=189774&r2=189773&pathrev=189774
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/date-multiple-fields/date-multiple-fields-disabled-crash-expected.txt?r1=189774&r2=189773&pathrev=189774
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/number/number-change-event-by-readonly.html?r1=189774&r2=189773&pathrev=189774
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLInputElement.cpp?r1=189774&r2=189773&pathrev=189774
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/date-multiple-fields/date-multiple-fields-disabled-crash.html?r1=189774&r2=189773&pathrev=189774

Do not dispatch 'change' event if the INPUT value is not changed.

This CL fixes two problems.

* When the INPUT type is changed, m_textAsOfLastFormControlChangeEvent is not
  initialized correctly.  So, we dispatched unexpected change events.

* When readonly/disabled state is changed, we call
  SpinButtonElement::releaseCapture(), which can dispatch a 'change' event. Its
  callsite should protect |this|.

BUG=454231,455193

Review URL: https://codereview.chromium.org/880473005
-----------------------------------------------------------------

### in...@chromium.org (2015-02-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### tk...@chromium.org (2015-02-16)

[Empty comment from Monorail migration]

### pe...@google.com (2015-02-16)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### pe...@google.com (2015-02-16)

Approved for M41 (branch: 2272)

### bu...@chromium.org (2015-02-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190223

------------------------------------------------------------------
r190223 | tkent@chromium.org | 2015-02-16T06:58:28.539384Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/forms/number/number-change-event-by-readonly.html?r1=190223&r2=190222&pathrev=190223
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/html/HTMLInputElement.cpp?r1=190223&r2=190222&pathrev=190223
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/forms/date-multiple-fields/date-multiple-fields-disabled-crash.html?r1=190223&r2=190222&pathrev=190223
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/html/forms/BaseMultipleFieldsDateAndTimeInputType.cpp?r1=190223&r2=190222&pathrev=190223
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/forms/number/number-change-event-by-readonly-expected.txt?r1=190223&r2=190222&pathrev=190223
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/forms/date-multiple-fields/date-multiple-fields-disabled-crash-expected.txt?r1=190223&r2=190222&pathrev=190223

Merge 189774 "Do not dispatch 'change' event if the INPUT value ..."

> Do not dispatch 'change' event if the INPUT value is not changed.
> 
> This CL fixes two problems.
> 
> * When the INPUT type is changed, m_textAsOfLastFormControlChangeEvent is not
>   initialized correctly.  So, we dispatched unexpected change events.
> 
> * When readonly/disabled state is changed, we call
>   SpinButtonElement::releaseCapture(), which can dispatch a 'change' event. Its
>   callsite should protect |this|.
> 
> BUG=454231,455193
> 
> Review URL: https://codereview.chromium.org/880473005

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/932533002
-----------------------------------------------------------------

### pe...@chromium.org (2015-02-18)

Following discussions with Tim Willis, no more security fixes going to M40.  M41 hits stable in 2 weeks.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $2000 from this report.

Notes from reward panel: $2000 amount due to node partition.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-18)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/454231?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081310)*
