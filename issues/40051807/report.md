# Heap-use-after-free in WebCore::CounterNode::insertAfter

| Field | Value |
|-------|-------|
| **Issue ID** | [40051807](https://issues.chromium.org/issues/40051807) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-12-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

use after free

**VERSION**  

Chrome Version:

Chromium 17.0.960.0 (Developer Build 112931)  

OS Linux  

WebKit 535.11 (trunk@101868)  

JavaScript V8 3.7.11

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
td {
counter-increment: list-item;
}
</style>
</head>
<body>
<table>
<td></td>
<ul>
<ul></ul>
</ul>
<li></li>
</table>
<table>
<td></td>
</table>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan/vg  

Crash State:

==31104== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe62eaca0 at pc 0x55555aa9feb2 bp 0x7fffffff7100 sp 0x7fffffff70d8  

READ of size 8 at 0x7fffe62eaca0 thread T0  

#0 0x55555aa9feb2 in WebCore::CounterNode::insertAfter(WebCore::CounterNode\*, WebCore::CounterNode\*, WTF::AtomicString const&) ???:0

0x7fffe62eaca0 is located 32 bytes inside of 72-byte region [0x7fffe62eac80,0x7fffe62eacc8)  

freed by thread T0 here:  

#0 0x55555ce2d1dd in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:37  

#1 0x55555aa85b60 in WebCore::findPlaceForCounter(WebCore::RenderObject\*, WTF::AtomicString const&, bool, WebCore::CounterNode\*&, WebCore::CounterNode\*&) third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:0  

#2 0x55555aa7e5ad in WebCore::makeCounterNode(WebCore::RenderObject\*, WTF::AtomicString const&, bool) third\_party/WebKit/Source/WebCore/rendering/RenderCounter.cpp:0

## Attachments

- [3272-asan.txt](attachments/3272-asan.txt) (text/x-c; charset=us-ascii, 11.6 KB)
- [3272.html](attachments/3272.html) (text/html; charset=us-ascii, 274 B)
- [counternode.zip](attachments/counternode.zip) (application/zip; charset=binary, 19.3 KB)

## Timeline

### in...@chromium.org (2011-12-05)

Miaubiz, thanks for the repro. Please note that this repro does not crash on trunk reliably. I could only get it to repro once on ClusterFuzz and never locally. Having math.random in the repro or a repro which does not crash reliably will not be considered a reduced testcase and might not qualify for the higher reward. Please try to provide a reduced testcase. For enforcing layout, you can try using document.body.offsetTop at various points in the script.

### mi...@gmail.com (2011-12-05)

@inferno: I'll try to fix it up. this one doesn't have Math.random() in it, the others do however. 

thanks for the tip about offsetTop. 

### in...@chromium.org (2011-12-05)

Unable to reproduce with your c#0 repro. Please post a reliable repro.

### mi...@gmail.com (2011-12-08)

some repros

Chromium	18.0.966.0 (Developer Build 113610)
OS	Linux
WebKit	535.12 (trunk@102342)
JavaScript	V8 3.7.12.6

### in...@chromium.org (2011-12-14)

reopening for analysis.

### in...@chromium.org (2011-12-14)

I am able to use another bigger repro from the zip which reproduces reliably.

### in...@chromium.org (2011-12-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4435391

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f6a210a52a0
Crash State:
  - crash stack -
  WebCore::CounterNode::insertAfter
  WebCore::makeCounterNode
  - free stack -
  WebCore::findPlaceForCounter
  WebCore::makeCounterNode
  

Minimized Testcase (0.22 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96geAjp0WthEGpPXrc0Cb0pMxJ2bqTpZE5gjECSJ9kT97GQ71CDhAxeQlkpqPIFNTJbczdQ_9Krsz-_q4Y50CRcVmyfWiVKb3WPeGn4pX3eDJ4fywWkffu4zIoygXQPVen-8RMp1oc7zv7L_bucVxzyAPXwtg
<style>
    td {
      counter-increment: list-item;
</style>
                  <table>
                    <td>
                      </tbody>
                    <ol>
<ol>
<td>
                </td>
            <li>
<table>
<td>

### in...@chromium.org (2011-12-26)

Upstreamed- https://bugs.webkit.org/show_bug.cgi?id=75212

### [Deleted User] (2012-01-10)

I understand the issue here and am close to a patch.

### [Deleted User] (2012-01-10)

Per discussions with the team I am setting this to Medium severity.. My reasoning is that The parent of the counternode will always be nulled when it is deleted. After deletion a read occurs on the object (but there is no way to retrieve this value). The parent is then checked against a valid parent and if it doesn't match we return out and this isn't exploitable.

So the only way to make this into an exploitable use-after-free would be to reallocate the memory and either guess (or somehow determine) the old parent value back into the proper offset. Given that in the default case this will not crash the browser as it is guaranteed to be a simple read into a mapped address it would theoretically be possible to simply brute force the parent address by trying every viable address until the correct one is hit. 

Even though this is Medium severity it is still an interesting bug and I think it warrants a reward.

### [Deleted User] (2012-01-10)

made a big speech and forgot to flip the flag

### in...@chromium.org (2012-01-23)

The last M16 patch is already gone. Mass-updating all of these to M17

### [Deleted User] (2012-02-06)

fixed upstream http://trac.webkit.org/changeset/106852

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-08)

Thanks! Given the Medium severity, a $500 Chromium Security Reward

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

### sc...@gmail.com (2012-02-10)

M17: http://trac.webkit.org/changeset/107330
M18: http://trac.webkit.org/changeset/107331

### sc...@gmail.com (2012-02-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 120523:120954.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4435391

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f6a210a52a0
Crash State:
  - crash stack -
  WebCore::CounterNode::insertAfter
  WebCore::makeCounterNode
  - free stack -
  WebCore::findPlaceForCounter
  WebCore::makeCounterNode
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=120523:120954

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96geAjp0WthEGpPXrc0Cb0pMxJ2bqTpZE5gjECSJ9kT97GQ71CDhAxeQlkpqPIFNTJbczdQ_9Krsz-_q4Y50CRcVmyfWiVKb3WPeGn4pX3eDJ4fywWkffu4zIoygXQPVen-8RMp1oc7zv7L_bucVxzyAPXwtg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/106336?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051807)*
