# UNKNOWN in WebCore::RenderTableSection::addCell

| Field | Value |
|-------|-------|
| **Issue ID** | [40059841](https://issues.chromium.org/issues/40059841) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | jc...@chromium.org |
| **Created** | 2012-06-17 |
| **Bounty** | $1,000.00 |

## Description


Chrom-version: ASAN 21.0.1176.0 (Developer Build 142393)
OS: Ubuntu 11.04 x86_64

This issue seems to be some-sort of race condition. In most of the cases it shows up as a normal null-pointer crash. 

==20476== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x7f9746234782 sp 0x7fff2d0dfd20 bp 0x7fff2d0dfe70 T0)

However I was able to make a repro-file combination which is able to reproduce the crash in multiple different ways.

==19342== ERROR: AddressSanitizer unknown-crash on address 0x3ff33d674f501 at pc 0x7fe68d0209b0 bp 0x7fff2aafe170 sp 0x7fff2aafe168
==19348== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x7fe68d020782 sp 0x7fff2aafdf00 bp 0x7fff2aafe050 T0)
==19811== ERROR: AddressSanitizer crashed on unknown address 0x0000bbadbeef (pc 0x7fe68d033740 sp 0x7fff2aafe0f0 bp 0x7fff2aafe130 T0)
==19818== ERROR: AddressSanitizer crashed on unknown address 0x0007e559bed0 (pc 0x7fe68d020793 sp 0x7fff2aafe180 bp 0x7fff2aafe2d0 T0)
==20054== ERROR: AddressSanitizer attempting free on address which was not malloc()-ed: 0x7fe6769ae880
==3274== ERROR: AddressSanitizer heap-use-after-free on address 0x7f557156d080 at pc 0x7f55836b09b0 bp 0x7fff401f41d0 sp 0x7fff401f41c8

The repro is combination of six html-files loaded into a iframe source via javascript.

I have included all the files needed plus two full symbolized ASAN-traces into the attached zip-file.

The timing on on the following line in test.html seems to play a big role in reproducing this crash in other than null. That value is to reproduce with i7 2600K processor machine.  

onload=setTimeout(function(){sampleswitch()},5)

With dev-channel build version 21.0.1171.0 (Official Build 141382) dev the repro causes everytime

[14874.679412] chrome[20762] general protection ip:7ff823a71bf9 sp:7fffbec08bf0 error:0 in chrome[7ff821b85000+44d5000]

Snippets from ASAN-outputs included in attached zip-file.

symbolized2.txt:

==3274== ERROR: AddressSanitizer heap-use-after-free on address 0x7f557156d080 at pc 0x7f55836b09b0 bp 0x7fff401f41d0 sp 0x7fff401f41c8
WRITE of size 8 at 0x7f557156d080 thread T0
    #0 0x7f55836b09b0 in WebCore::RenderTableSection::addCell(WebCore::RenderTableCell*, WebCore::RenderTableRow*) ???:0
    #1 0x7f55836abec4 in WebCore::RenderTableRow::addChild(WebCore::RenderObject*, WebCore::RenderObject*) ???:0
    #2 0x7f55836af319 in WebCore::RenderTableSection::addChild(WebCore::RenderObject*, WebCore::RenderObject*) ???:0
    #3 0x7f5583681842 in WebCore::RenderTable::addChild(WebCore::RenderObject*, WebCore::RenderObject*) ???:0
    #4 0x7f5581b293a0 in WebCore::NodeRendererFactory::createRendererIfNeeded() ???:0

symbolized1.txt
==20472== ERROR: AddressSanitizer crashed on unknown address 0x5cdce67431f2 (pc 0x7f9746234793 sp 0x7fff2d0dffa0 bp 0x7fff2d0e00f0 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7f9746234793 in WebCore::RenderTableSection::addCell(WebCore::RenderTableCell*, WebCore::RenderTableRow*) ???:0
    #1 0x7f974622fec4 in WebCore::RenderTableRow::addChild(WebCore::RenderObject*, WebCore::RenderObject*) ???:0
    #2 0x7f9746233319 in WebCore::RenderTableSection::addChild(WebCore::RenderObject*, WebCore::RenderObject*) ???:0
    #3 0x7f9746205842 in WebCore::RenderTable::addChild(WebCore::RenderObject*, WebCore::RenderObject*) ???:0
    #4 0x7f97446ad3a0 in WebCore::NodeRendererFactory::createRendererIfNeeded() ???:0




## Attachments

- [report.zip](attachments/report.zip) (application/zip; charset=binary, 20.7 KB)
- [WebCoreRenderTableSectionaddCellWebCoreRenderTableCell9b0.html](attachments/WebCoreRenderTableSectionaddCellWebCoreRenderTableCell9b0.html) (text/html; charset=us-ascii, 941 B)
- [133214-maybe.html](attachments/133214-maybe.html) (text/html; charset=us-ascii, 181 B)
- [WebCoreRenderTableSectionaddCellWebCoreRenderTableCell9b0.html](attachments/WebCoreRenderTableSectionaddCellWebCoreRenderTableCell9b0_53075542.html) (text/html; charset=us-ascii, 925 B)

## Timeline

### sc...@gmail.com (2012-06-17)

Hmm, RenderTable.... looks familiar, Julien / Abhishek?

### at...@gmail.com (2012-06-17)

@scarybeasts: Were you able to repro this as anything else than null-pointer? I could try to create a better repro or atleast try to find timeout-values for other machines tomorrow when I have access to more hardware.

### jc...@chromium.org (2012-06-18)

Reduced version of one of the test case. It's hitting an ASSERT in Debug.

ASSERTION FAILED: i < size()
Source/WTF/wtf/Vector.h(532) : T& WTF::Vector<T, inlineCapacity>::at(size_t) [with T = WebCore::RenderTableSection::CellStruct, long unsigned int inlineCapacity = 0ul]
1   0x1361457
2   0x1361299
3   0x1abb986
4   0x1ac776e
5   0x1ac5c8a
6   0x1ac7200
7   0x1ab511d
8   0x1965e5e
9   0x196659a
10  0x19664dc
11  0x77dfe6
12  0x76092b
13  0x736f6b
14  0x6d362b
15  0x6d1304
16  0x736ff5
17  0x6d362b
18  0x6d1304
19  0x736ff5
20  0x6d362b
21  0x6d1304
22  0x736ff5
23  0x73bfb6
24  0x737862
25  0x737f80
[30595:30595:7074470361:ERROR:process_util_posix.cc(143)] Received signal 11
        base::debug::StackTrace::StackTrace() [0x8718d6]
        base::(anonymous namespace)::StackDumpSignalHandler() [0x83191d]
        0x7f0ac0e99af0
        WTF::Vector<>::at() [0x1361461]
        WTF::Vector<>::operator[]() [0x1361299]
        WebCore::RenderTableSection::cellAt() [0x1abb986]
        WebCore::RenderTableSection::addCell() [0x1ac776e]
        WebCore::RenderTableRow::addChild() [0x1ac5c8a]
        WebCore::RenderTableSection::addChild() [0x1ac7200]
        WebCore::RenderTable::addChild() [0x1ab511d]
        WebCore::RenderBlock::addChildIgnoringAnonymousColumnBlocks() [0x1965e5e]
        WebCore::RenderBlock::addChildIgnoringContinuation() [0x196659a]
        WebCore::RenderBlock::addChild() [0x19664dc]
        WebCore::NodeRendererFactory::createRendererIfNeeded() [0x77dfe6]
        WebCore::Node::createRendererIfNeeded() [0x76092b]
        WebCore::Element::attach() [0x736f6b]
        WebCore::ContainerNode::attachChildren() [0x6d362b]
        WebCore::ContainerNode::attach() [0x6d1304]
        WebCore::Element::attach() [0x736ff5]
        WebCore::ContainerNode::attachChildren() [0x6d362b]
        WebCore::ContainerNode::attach() [0x6d1304]
        WebCore::Element::attach() [0x736ff5]
        WebCore::ContainerNode::attachChildren() [0x6d362b]
        WebCore::ContainerNode::attach() [0x6d1304]
        WebCore::Element::attach() [0x736ff5]
        WebCore::Node::reattach() [0x73bfb6]
        WebCore::Element::recalcStyle() [0x737862]
        WebCore::Element::recalcStyle() [0x737f80]

(i = 1, size() = 1)

### at...@gmail.com (2012-06-18)

Related to http://code.google.com/p/chromium/issues/detail?id=130922 ?

I haven't seen https://crbug.com/chromium/130922 in awhile in my tests, but don't know for sure if it is fixed already.

### jc...@chromium.org (2012-06-18)

> Related to http://code.google.com/p/chromium/issues/detail?id=130922 ?

Difficult to say as the reduced test involves counters. We mitigated the badness from the other bug but didn't fix the root cause. Someone should run the test under the layout invariant from https://bugs.webkit.org/show_bug.cgi?id=49019.

### [Deleted User] (2012-06-18)

Is this the same bug being hit by this?



### pa...@google.com (2012-06-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=58624268

Fuzzer: Inferno_twister

Crash Type: UNKNOWN
Crash Address: 0x0000bbadbeef
Crash State:
  - crash stack -
  WebCore::RenderTableSection::addCell
  WebCore::RenderTableRow::addChild
  WebCore::RenderTableSection::addChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108839:108881

Minimized Testcase (0.17 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv9681DZ-coS9Bqx1EPPFbwsngMcAKG1VA-5eyRNN-_X47mRs8HS7aHw8-ky9e_pp9avTFxa3jy1SoEqSt0YXmxpZoiFyxBh7yafCvKPdbusfIDw4Gd7TRBs7jeY1Tjw9oNoGKejo41H5LOH63iTmyPYtHKSe4VPZPljX8HL7YU2ZgUhn8UI
<html xmlns="http://www.w3.org/1999/xhtml">><head style='font: bold highlighted 5% serif; '>
<window>
</window><footer></footer></head>
>>>>><th colspan="2147483647"></th>
<td>>

### pa...@google.com (2012-06-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=64417597

Uploader: palmer@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebCore::RenderTableSection::addCell
  WebCore::RenderTableRow::addChild
  WebCore::RenderTableSection::addChild
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94XpCTRaKXPcSwJXi2Jp9D0FE1Lzs_rsDmt9tmjQohhp4UpMaBrRhxY--552t_-07J4LkyPk8QDbOXk1d3McAzetdMEFLQsYHRhl95S5-H-C1iwKP6h3tHjHn-1jS66HgAjq34z0fQ8OmXBqEFfgXTB2YRzWUTE1U90PWr_w-WmCA5hUKw

### [Deleted User] (2012-06-19)

This is crashing when it tries to access an out of bounds column in RenderTableSection::addCell().

When it does 
CellStruct& c = cellAt(insertionRow + r, m_cCol);

m_cCol is off by one so cellAt() will return whatever is right after the end of the vector. In this case that will be a cell that used to be part of the vector but has been deleted. Calling this a use after free isn't exactly correct although it does end up manifesting itself that way in this case.

In reality the issue appears to be an off-by-one.

Doesn't seem to affect Stable or Beta.

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=89496


### pa...@chromium.org (2012-06-20)

Is this similar to 131201, which I lovingly gave to jchaffraix? :)

(And which for some reason I can't see anymore)

### jc...@chromium.org (2012-06-27)

@cdn, the attachment doesn't crash for me on WebKit ToT DRT so I would say unrelated.

@palmer, it's unrelated to https://crbug.com/chromium/131201. https://crbug.com/chromium/131201 was related to fixed table layout and is fixed now, this one is not. Also no love went into this issue :)

### pa...@chromium.org (2012-06-27)

To clarify, I didn't think they had the same underlying cause, but that perhaps conceptually they were simlar in that the code gets confused about how many items are in the vector because there are two ways of tracking the count.

No love! How can you say there is no love? After all this bug has done for you...

### js...@chromium.org (2012-06-27)

Please, no discussions of love in the issue tracker, even among Frenchmen and residents of San Francisco. Lets just focus on who we're going to inflict this bug on to get a fix. @jchafraix it does look very tablerific?

### jc...@chromium.org (2012-06-28)

@palmer, I see what you mean. It's another instance of 2 structures drifting apart AFAICT. I didn't link those 2 issues together as there is very little overlap in which structures get confused.

@jschuh, I spend more time looking at it and it is table-related (the counters were a red-herring and can replaced by regular generated content). The big issue is that the reduction I have involves 5 - 6 nested tables which makes it hard to see what's wrong.

### js...@chromium.org (2012-06-29)

Bulk edit: updating impacts for target release.

### js...@chromium.org (2012-06-29)

Bulk Edit: High and critical severity regressions block the release of m21.

### ka...@google.com (2012-07-09)

[Empty comment from Monorail migration]

### ka...@google.com (2012-07-16)

julien you're looking at this right?

### jc...@chromium.org (2012-07-18)

Reduced test case, it's still pretty massive but I have found the issue: it stems from our table splitting logic.
The test case forces some anonymous tables to be splitted, however we never update the internal representation of the table to match the moved sections which leads to the bug. The obvious fix (likely the good one) would be to also invalidate any moved sections to force the table to regenerate its structure.

### jc...@chromium.org (2012-07-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-19)

http://trac.webkit.org/changeset/123062

### cl...@chromium.org (2012-07-20)

ClusterFuzz has detected this issue as fixed in range 147542:147576.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=64417597

Uploader: palmer@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebCore::RenderTableSection::addCell
  WebCore::RenderTableRow::addChild
  WebCore::RenderTableSection::addChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=138089:138090
Fixed: https://cluster-fuzz.appspot.com/revisions?range=147542:147576

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94NqL-RZEQEah4Of0FY3DJpqukbU9txg60vQqKbiGSq4Xc8b2TtCIcXQC9iXpOB0UYjL5lj60tZtLh_wK7AvILApUmwkGK8WyAMrqDV2yH8aI-aCZbyFwAS4rpeTCOnLYP-8A62nSdVJek4z4u8Y4IAreIHWIHulrEDQ8gG6Wzpv0UGrnI

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-07-24)

merged in r123513 to m21. leaving merge-approved as i am confused if it impacts stable ?

### ka...@google.com (2012-07-24)

[Empty comment from Monorail migration]

### jc...@chromium.org (2012-07-24)

After discussing with @dharani, it was decided that we won't merge the fix to M20 as we are not 100% sure it's impacted.

### sc...@gmail.com (2012-07-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

@attekett: thanks!
This test case was not particularly reduced, but the panel realizes that this is a weird / crazy bug and therefore the test case is hard to minimize.
So the reward is for the full $1000 level.

### sc...@gmail.com (2012-09-12)

Paid as part of $4500 batch

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-02-18)

ClusterFuzz has detected this issue as fixed in range 183010:183025.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=58624268

Fuzzer: Inferno_twister

Crash Type: UNKNOWN
Crash Address: 0x0000bbadbeef
Crash State:
  - crash stack -
  WebCore::RenderTableSection::addCell
  WebCore::RenderTableRow::addChild
  WebCore::RenderTableSection::addChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108839:108881
Fixed: https://cluster-fuzz.appspot.com/revisions?range=183010:183025

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv9681DZ-coS9Bqx1EPPFbwsngMcAKG1VA-5eyRNN-_X47mRs8HS7aHw8-ky9e_pp9avTFxa3jy1SoEqSt0YXmxpZoiFyxBh7yafCvKPdbusfIDw4Gd7TRBs7jeY1Tjw9oNoGKejo41H5LOH63iTmyPYtHKSe4VPZPljX8HL7YU2ZgUhn8UI

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/133214?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059841)*
