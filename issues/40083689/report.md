# Heap-use-after-free in blink::InlineFlowBox::addToLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40083689](https://issues.chromium.org/issues/40083689) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | ea...@chromium.org |
| **Created** | 2016-02-13 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6566106111672320

Fuzzer: attekett_surku_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x7d1400014a58
Crash State:
  blink::InlineFlowBox::addToLine
  blink::LayoutBlockFlow::createLineBoxes
  blink::LayoutBlockFlow::constructLine
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=372998:373602

Minimized Testcase (0.72 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95p91HVcUbBOJdPOLxUIVClZcg0DuMoeRBRhVovDnz0izqSi4otl0_QEkbRvNJJ507JmR95KybHo4Rsx7KJiO2aLiXnJjVzhrzHJPVD8Awo7fHcuFnAlfER4-cKjeljnJsDtqZYttV1JjsbXUsWPM8GpWsp1w

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### cl...@chromium.org (2016-02-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-02-13)

Levi, Emil - Any idea on culprit cl from regression range, your help is appreciated, thanks!

### cl...@chromium.org (2016-02-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-14)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ri...@chromium.org (2016-02-15)

[Empty comment from Monorail migration]

### le...@chromium.org (2016-02-16)

I'm suspicious of the regression range, and the range itself is massive. I'm re-running the bisect.

### le...@chromium.org (2016-02-16)

Either way, I'm handing this off to eae to route as I have too many release blockers. Adding some other folks who may be able to help.

### ea...@chromium.org (2016-02-17)

[Comment Deleted]

### ea...@chromium.org (2016-02-17)

FYI: Re-ran the regression bisect and it came back with the same delta. Still odd though given that there are no relevant layout changes in the range.

### cb...@chromium.org (2016-02-17)

I have no time to really debug this right now but just quickly some debug info. I don't really know this code. I may be able to debug further in a couple days.

ASSERTION FAILED: obj->isLayoutInline() || obj == this
../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp(176) : blink::InlineFlowBox *blink::LayoutBlockFlow::createLineBoxes(blink::LayoutObject *, const blink::LineInfo &, blink::InlineBox *)
1   0x7f2c10a9aefc blink::LayoutBlockFlow::createLineBoxes(blink::LayoutObject*, blink::LineInfo const&, blink::InlineBox*)
2   0x7f2c10a9b57b blink::LayoutBlockFlow::constructLine(blink::BidiRunList<blink::BidiRun>&, blink::LineInfo const&)

(gdb) p *obj
$1 = (blink::LayoutBlockFlow) {

(gdb) p *this 
$2 = (blink::LayoutTableCell) {

(gdb) bt
#0  0x00007fffe4a9ff03 in blink::LayoutBlockFlow::createLineBoxes (this=0x20459f63c010, obj=0x20459f618230, lineInfo=..., 
    childBox=0x20459f668178) at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:176
#1  0x00007fffe4aa057b in blink::LayoutBlockFlow::constructLine (this=0x20459f63c010, bidiRuns=..., lineInfo=...)
    at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:293
#2  0x00007fffe4aa2e70 in blink::LayoutBlockFlow::createLineBoxesFromBidiRuns (this=0x20459f63c010, bidiLevel=0, bidiRuns=..., end=..., 
    lineInfo=..., verticalPositionCache=..., trailingSpaceRun=0x0, wordMeasurements=WTF::Vector of length 4, capacity 64 = {...})
    at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:709
#3  0x00007fffe4aa4a1b in blink::LayoutBlockFlow::layoutRunsAndFloatsInRange (this=0x20459f63c010, layoutState=..., resolver=..., 
    cleanLineStart=..., cleanLineBidiStatus=...) at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:904
#4  0x00007fffe4aa3267 in blink::LayoutBlockFlow::layoutRunsAndFloats (this=0x20459f63c010, layoutState=...)
    at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:778
#5  0x00007fffe4aa7e0a in blink::LayoutBlockFlow::layoutInlineChildren (this=0x20459f63c010, relayoutChildren=true, 
    paintInvalidationLogicalTop=0px, paintInvalidationLogicalBottom=0px, afterEdge=0px)
    at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlowLine.cpp:1604
#6  0x00007fffe4a99909 in blink::LayoutBlockFlow::layoutBlockFlow (this=0x20459f63c010, relayoutChildren=true, pageLogicalHeight=0px, 
    layoutScope=...) at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:374
#7  0x00007fffe4a8dce9 in blink::LayoutBlockFlow::layoutBlock (this=0x20459f63c010, relayoutChildren=true)
    at ../../third_party/WebKit/Source/core/layout/LayoutBlockFlow.cpp:296
#8  0x00007fffe4b91807 in blink::LayoutTableCell::layout (this=0x20459f63c010)
    at ../../third_party/WebKit/Source/core/layout/LayoutTableCell.cpp:234
#9  0x00007fffe4b98b3a in blink::LayoutTableRow::layout (this=0x20459f6081e0)
    at ../../third_party/WebKit/Source/core/layout/LayoutTableRow.cpp:170

(gdb) call showLayoutTreeForThis() 
LayoutView 0x20459f604010              	#document	0x1f43fa142550
  LayoutBlockFlow 0x20459f618010       	HTML	0x1f43fa143138
    LayoutBlockFlow 0x20459f618120     	BODY	0x1f43fa143318
      LayoutTable 0x20459f61c010       	OL	0x1f43fa143380
        LayoutTableSection (anonymous) 0x20459f630010
          LayoutTableRow (anonymous) 0x20459f6081e0
*           LayoutTableCell (anonymous) 0x20459f63c010
              LayoutText 0x20459f628010	#text	0x1f43fa1433f8 "BUNGALOOO!!!aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaç–¨aÌ”aaaaaaÍ¥aaaaaaaÌ­aaaaaaaaaaaaaaaaa"
              LayoutBlockFlow 0x20459f618230	H1	0x1f43fa143448
                LayoutBR 0x20459f6280b8	BR	0x1f43fa1434b0
                LayoutText 0x20459f628160	#text	0x1f43fa143518 "aaaaaaaaaaaaaaaaaaá—‰aaaaaaà·±aå‰‡aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
              LayoutBlockFlow (anonymous) 0x20459f618450
                LayoutText 0x20459f628208	#text	0x1f43fa143568 "aaaaaaaç‘¬aç”°Í“aÍÌ’aaaaaã½´Ìœaá¾”ÍŠç‰­aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        LayoutTableCol 0x20459f6082c8  	LI	0x1f43fa1435b8 CLASS="C39 C18"
        LayoutTableSection (anonymous) 0x20459f630168
          LayoutTableRow (anonymous) 0x20459f6083b0
            LayoutTableCell (anonymous) 0x20459f63c130
              LayoutInline 0x20459f628358	SMALL	0x1f43fa143688
                LayoutText 0x20459f628400	#text	0x1f43fa1436f0 "\n"


### cl...@chromium.org (2016-02-17)

ClusterFuzz has detected this issue as fixed in range 375259:375683.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6566106111672320

Fuzzer: attekett_surku_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x7d14000149b8
Crash State:
  blink::InlineFlowBox::addToLine
  blink::LayoutBlockFlow::createLineBoxes
  blink::LayoutBlockFlow::constructLine
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=372998:373602
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=375259:375683

Minimized Testcase (0.72 Kb): https://cluster-fuzz.appspot.com/download/AMIfv966NRJhlhgeRXtcU2zm04OBjPM1bMRrHYAi0VYN1jZ_DoqPhX1CMBJp-yxekKECiI9ary1uXuScie9KEJMZXa6ius-GL_klg2JFtns0YpbxE73eOLurABwcwBkKwqV9b_VFMdhfoUa1zhXCE9OS6VPh-c4row

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ea...@chromium.org (2016-02-17)

Re-running fixed step to verify.

### cl...@chromium.org (2016-02-18)

ClusterFuzz has detected this issue as fixed in range 375259:375683.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6566106111672320

Fuzzer: attekett_surku_fuzzer
Job Type: linux_tsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x7d14000149b8
Crash State:
  blink::InlineFlowBox::addToLine
  blink::LayoutBlockFlow::createLineBoxes
  blink::LayoutBlockFlow::constructLine
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=372998:373602
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_tsan_chrome_mp&range=375259:375683

Minimized Testcase (0.72 Kb): https://cluster-fuzz.appspot.com/download/AMIfv966NRJhlhgeRXtcU2zm04OBjPM1bMRrHYAi0VYN1jZ_DoqPhX1CMBJp-yxekKECiI9ary1uXuScie9KEJMZXa6ius-GL_klg2JFtns0YpbxE73eOLurABwcwBkKwqV9b_VFMdhfoUa1zhXCE9OS6VPh-c4row

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ea...@chromium.org (2016-02-18)

Alright then, clusterfuzz considers it fixed and came back with the same delta for the fix when re-running. That's good enough for me, marking as fixed.

### cl...@chromium.org (2016-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

Atte - $3,500 for this report ($3,000 for the report, $500 for the fuzzer). Thanks as always!

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/586720?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083689)*
