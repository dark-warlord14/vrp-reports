# Heap-use-after-free in WebCore::Node::~Node

| Field | Value |
|-------|-------|
| **Issue ID** | [40055337](https://issues.chromium.org/issues/40055337) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-03-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free happens when adopting shadow node.

**VERSION**  

Version 19.0.1068.0 (126348), Developer Build on Ubuntu 10.10

**REPRODUCTION CASE**  

There are two testcases -  

\* the tc-21-03-12-uaf-1.zip (asan-1.1.txt, asan-1.2.txt accordingly) - can generate two varying stack traces, with the read of 4 or 8 bytes.  

\* tc-21-03-12-uaf-2.zip (asan-2.txt) should produce one stacktrace.

Experimental feature Shadow DOM should be enabled.

## Attachments

- [tc-21-03-12-uaf-1.zip](attachments/tc-21-03-12-uaf-1.zip) (application/zip; charset=binary, 594 B)
- [tc-21-03-12-uaf-2.zip](attachments/tc-21-03-12-uaf-2.zip) (application/zip; charset=binary, 596 B)
- [asan-1.1.txt](attachments/asan-1.1.txt) (text/x-c; charset=us-ascii, 6.9 KB)
- [asan-1.2.txt](attachments/asan-1.2.txt) (text/x-c; charset=us-ascii, 6.5 KB)
- [asan-2.txt](attachments/asan-2.txt) (text/x-c; charset=us-ascii, 6.3 KB)
- [asan-shadow-dom.txt](attachments/asan-shadow-dom.txt) (text/x-c; charset=us-ascii, 12.8 KB)
- [asan-shadow-dom-2.txt](attachments/asan-shadow-dom-2.txt) (text/plain; charset=us-ascii, 5.9 KB)

## Timeline

### ke...@chromium.org (2012-03-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29039183

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f15157fc228
Crash State:
  - crash stack -
  WebCore::Node::~Node
  non-virtual thunk to WebCore::ShadowRoot::~ShadowRoot
  - free stack -
  WebCore::Node::~Node
  WebCore::Element::~Element
  

Minimized Testcase (0.39 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95qEgyiu_gmp0KaFGcGnfzI3vsk6czbTQCmHkYeCW9L5ePiq2miaOK6-vEffCt19CWTZePvwQxKkhdxDwNYxjh3LLJcexaFmbKx_soA6THolVFij2KtP0gGDfHdkgndr9rswIJhV-mXxaM0MgF54Sl4gyA08A

### ke...@chromium.org (2012-03-21)

The above report is with tc-21-03-12-uaf-1.zip.

This doesn't look exactly the same, but there is a reasonable chance that this is a duplicate of https://crbug.com/chromium/118642.

I say that based on this being related to objects being freed due to calls to RuntimeProfiler::isEnabled().

arv, if you're looking at that, would you be able to see if this is the same bug?

### in...@chromium.org (2012-03-21)

Regression range from ClusterFuzz should come soon, we will know who regressed it.

### in...@chromium.org (2012-03-21)

As per regression range, this is shadow dom specific. Hajime, can you please help to triage this.

### [Deleted User] (2012-03-22)

Sure. My plate is getting filled up with fuzzer salad..

### ax...@gmail.com (2012-03-22)

I have another testcase (not reduced yet) that produces attached ASan logs. Also requires Shadow DOM enabled and one of the logs (asan-shadow-dom-2.txt) makes me think that there is the same triggering bug. However, one log looks suspiciously different. I hope these logs may give some clues if this is the same bug. If logs does not help, then I'll reduce testcase. It just requires hours of manual work.

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-30)

Reverting wrong marking of security bugs by release management.

### cl...@chromium.org (2012-04-04)

ClusterFuzz has detected this issue as fixed in range 130617:130650.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29039183

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f15157fc228
Crash State:
  - crash stack -
  WebCore::Node::~Node
  non-virtual thunk to WebCore::ShadowRoot::~ShadowRoot
  - free stack -
  WebCore::Node::~Node
  WebCore::Element::~Element
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=119651:119661
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130617:130650

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95qEgyiu_gmp0KaFGcGnfzI3vsk6czbTQCmHkYeCW9L5ePiq2miaOK6-vEffCt19CWTZePvwQxKkhdxDwNYxjh3LLJcexaFmbKx_soA6THolVFij2KtP0gGDfHdkgndr9rswIJhV-mXxaM0MgF54Sl4gyA08A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-04-05)

ignore last comment. Bug is not fixed. There was a v8 bug which is causing asan builds to mess up on ClusterFuzz.

### js...@chromium.org (2012-04-08)

[Empty comment from Monorail migration]

### pa...@google.com (2012-04-09)

I get assertion failures on ToT (comment one out, get to the next...), but no Aw Snap on 19. I do seem to get a weird renderer DoS on 19 though.

### ax...@gmail.com (2012-04-09)

Both testcases are working for me also on Version 20.0.1091.0 (130353) Ubuntu 10.10. Have you enabled Shadow DOM?

### in...@chromium.org (2012-04-09)

ClusterFuzz confirms that the bug is still live on r127980. When in doubt, please use the redo interface in ClusterFuzz to check if the bug is fixed or not. Otherwise, it automatically does it once per day.

### [Deleted User] (2012-04-17)

Submitted a patch to https://bugs.webkit.org/show_bug.cgi?id=84127.


### in...@chromium.org (2012-04-18)

http://trac.webkit.org/changeset/114481

### cl...@chromium.org (2012-04-18)

ClusterFuzz has detected this issue as fixed in range 132759:132767.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29039183

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f15157fc228
Crash State:
  - crash stack -
  WebCore::Node::~Node
  non-virtual thunk to WebCore::ShadowRoot::~ShadowRoot
  - free stack -
  WebCore::Node::~Node
  WebCore::Element::~Element
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=119651:119661
Fixed: https://cluster-fuzz.appspot.com/revisions?range=132759:132767

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95qEgyiu_gmp0KaFGcGnfzI3vsk6czbTQCmHkYeCW9L5ePiq2miaOK6-vEffCt19CWTZePvwQxKkhdxDwNYxjh3LLJcexaFmbKx_soA6THolVFij2KtP0gGDfHdkgndr9rswIJhV-mXxaM0MgF54Sl4gyA08A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-04-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-24)

Nice catch Ax330d. Thanks for helping to polish the shadow dom feature. This is good for a $1000 Chromium Security Reward.


### sc...@gmail.com (2012-04-24)

Yeah nice. Sometimes we reward $500 or $0 for features behind flags if they are under heavy churn but we believe this feature is relatively complete, hence the full reward.

### sc...@gmail.com (2012-04-24)

Since this is behind a flag still, adjusting merge / milestone / impacts flags.

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/119305?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055337)*
