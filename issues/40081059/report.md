# Use-of-uninitialized-value in unsigned int blink::SimpleShaper::advanceInternal<blink::SurrogatePairAware

| Field | Value |
|-------|-------|
| **Issue ID** | [40081059](https://issues.chromium.org/issues/40081059) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fm...@chromium.org |
| **Created** | 2014-12-22 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5339468436340736

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  unsigned int blink::SimpleShaper::advanceInternal<blink::SurrogatePairAware
  blink::SimpleShaper::advance
  blink::Font::buildGlyphBuffer
  

Minimized Testcase (6.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95xf-GB8cjslxAbg_feLmFWAJWAvVu3PigkStD0ne_hopjklpRkAGbLLMUgXcpqGco2qQ7HN1qYsveTf8XJOo7tIelKCFMIO8h-GawGe_SE-A84IX7ecatGMRIbEQ3rVn6xas6j4KwH9d4PZzN8yAwMsobn8w

Filer: inferno

## Timeline

### in...@chromium.org (2014-12-22)

Author: fmalita@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/ae6e22134fc3f8b319205aedc648d4fadd575370
Time: Tue Jul 15 00:56:00 2014
The CL last changed line 165 of file SimpleShaper.cpp, which is stack frame 1.

### cl...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

Florin, friendly ping.

### fm...@chromium.org (2015-01-08)

Sorry about the delay, still prioritizing stuff after the holidays.

I recall taking a quick look when this came up and concluding it's just another manifestation of the ubiquitous css counter layout bug (counter updates leaving subtrees unlaid out). Will triage tomorrow.

### fm...@chromium.org (2015-01-08)

Debug builds hit the following ASSERT:

ASSERTION FAILED: offset + length <= m_length
../../third_party/WebKit/Source/wtf/text/StringView.h(63) : void WTF::StringView::narrow(unsigned int, unsigned int)

Received signal 11 SEGV_MAPERR 0000fbadbeef
#0 0x7fded3624e5e base::debug::StackTrace::StackTrace()
#1 0x7fded3624993 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7fdecdd6f340 <unknown>
#3 0x7fded72007b9 [11891:11891:0108/105316:INFO:CONSOLE(1)] "Uncaught SyntaxError: Unexpected token ILLEGAL", source: file:///tmp/fuzz-9.html (1)
WTF::StringView::narrow()
#4 0x7fded71fc697 blink::InlineTextBoxPainter::paint()
#5 0x7fded72dd13c blink::InlineTextBox::paint()
#6 0x7fded71f5c4c blink::InlineFlowBoxPainter::paint()
#7 0x7fded72d63df blink::InlineFlowBox::paint()
#8 0x7fded7210934 blink::RootInlineBoxPainter::paint()
#9 0x7fded74642af blink::RootInlineBox::paint()
...


Sure enough, the issue is triggered by our old friend RenderCounter which updates the text using setTextInternal() and doesn't trigger a layout/linebox invalidation:

  void RenderCounter::updateCounter()
  {
      setTextInternal(originalText());
  }

So after the counter update, we end up with stale InlineTextBox data. I'm fairly ignorant when it comes to RenderCounter, but I think it should use setText() here (which does mark the node for layout/lineboxes inval). A quick test confirms that this change fixes the crash - I'll put together a CL.

### in...@chromium.org (2015-01-08)

[Empty comment from Monorail migration]

### fm...@chromium.org (2015-01-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188180

------------------------------------------------------------------
r188180 | fmalita@chromium.org | 2015-01-10T04:26:12.301364Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderCounter.cpp?r1=188180&r2=188179&pathrev=188180
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/counters/stale-inline-box-crash-expected.txt?r1=188180&r2=188179&pathrev=188180
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css/counters/stale-inline-box-crash.html?r1=188180&r2=188179&pathrev=188180
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/paint/InlineTextBoxPainter.cpp?r1=188180&r2=188179&pathrev=188180

RenderCounter::updateCounter should trigger a relayout.

Currently, the method calls setTextInternal() - which updates the text
but doesn't mark the node for layout and pref widths recalc. This can
leave stale text boxes behind.

Instead, we should use setText() - which triggers the needed
invalidations.

BUG=444707
R=jbroman@chromium.org,eae@chromium.org

Review URL: https://codereview.chromium.org/842913002
-----------------------------------------------------------------

### in...@chromium.org (2015-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-11)

ClusterFuzz has detected this issue as fixed in range 310958:310968.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5339468436340736

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  unsigned int blink::SimpleShaper::advanceInternal<blink::SurrogatePairAware
  blink::SimpleShaper::advance
  blink::Font::buildGlyphBuffer
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=310958:310968

Minimized Testcase (6.58 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95xf-GB8cjslxAbg_feLmFWAJWAvVu3PigkStD0ne_hopjklpRkAGbLLMUgXcpqGco2qQ7HN1qYsveTf8XJOo7tIelKCFMIO8h-GawGe_SE-A84IX7ecatGMRIbEQ3rVn6xas6j4KwH9d4PZzN8yAwMsobn8w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

Just m41 is good for this sec-medium bug.

### pe...@google.com (2015-01-25)

[Automated comment] Commit may have occurred before M41 branch point (1/10/2015), needs manual review.

### pe...@chromium.org (2015-01-26)

Confirmed we do need to merge this CL.  Merge approved for M41 branch 2272.

### bu...@chromium.org (2015-01-26)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188959

------------------------------------------------------------------
r188959 | fmalita@chromium.org | 2015-01-26T15:14:17.158921Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/css/counters/stale-inline-box-crash-expected.txt?r1=188959&r2=188958&pathrev=188959
   A http://src.chromium.org/viewvc/blink/branches/chromium/2272/LayoutTests/fast/css/counters/stale-inline-box-crash.html?r1=188959&r2=188958&pathrev=188959
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/paint/InlineTextBoxPainter.cpp?r1=188959&r2=188958&pathrev=188959
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/rendering/RenderCounter.cpp?r1=188959&r2=188958&pathrev=188959

Merge 188180 "RenderCounter::updateCounter should trigger a rela..."

> RenderCounter::updateCounter should trigger a relayout.
> 
> Currently, the method calls setTextInternal() - which updates the text
> but doesn't mark the node for layout and pref widths recalc. This can
> leave stale text boxes behind.
> 
> Instead, we should use setText() - which triggers the needed
> invalidations.
> 
> BUG=444707
> R=jbroman@chromium.org,eae@chromium.org
> 
> Review URL: https://codereview.chromium.org/842913002

TBR=pennymac@chromium.org

Review URL: https://codereview.chromium.org/862803003
-----------------------------------------------------------------

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $1000 for this report.

Notes from panel: $500 for the bug (though hard to tell if the value could be read back) + $500 ClusterFuzz bonus.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-04-18)

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

This issue was migrated from crbug.com/chromium/444707?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081059)*
