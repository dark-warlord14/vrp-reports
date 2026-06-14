# Heap-use-after-free in WebCore::InlineBox::deleteLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40051779](https://issues.chromium.org/issues/40051779) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | ke...@chromium.org |
| **Created** | 2011-12-02 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=2154493

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7fcd1a3e08b1
Crash State:
  - crash stack -
  WebCore::InlineBox::deleteLine
  WebCore::InlineFlowBox::deleteLine
  - free stack -
  WebCore::FrameView::updateWidgets
  WebCore::FrameView::performPostLayoutTasks
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108984:109026

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96WL2fe-GLYgbm6yPYqU6G7DipgynGrQPetaQW3ayNpPrcXyGB21VjeN7hd99fHgZlQVIRNqDfiJo-sJGQjPWozMuYDRMhqUG3zN7_AjAEtdypKjz_z9SGYN2RdEmYSmAOMdCS0lXU6SJkZH5fw1AEzdPxJnw

## Attachments

- [crash4.html](attachments/crash4.html) (text/plain; charset=us-ascii, 345 B)

## Timeline

### in...@chromium.org (2011-12-02)

credit: slaweck

This is coming from the hard delete to ASSERT change in https://trac.webkit.org/changeset/99462/. Ken is looking into it, it looks like a different UBA bug too.

### ke...@chromium.org (2011-12-02)

Very similar to https://crbug.com/chromium/104859, but a different issue. That one was a problem with entering and exiting isolates when they should be skipped. This one seems to be an issue with how isolates are tracked.

### in...@chromium.org (2011-12-04)

We have multiple repros of this on ClusterFuzz. We should try to evaluate if they are the same bug and if this regression is serious enough to revert to previous behavior.

https://cluster-fuzz.appspot.com/testcase?key=2415720
https://cluster-fuzz.appspot.com/testcase?key=2370333
https://cluster-fuzz.appspot.com/testcase?key=2343865
https://cluster-fuzz.appspot.com/testcase?key=2330148

### ke...@chromium.org (2011-12-05)

I'm looking at whether they are the same bug.

In WebKit r99462 I replaced a check and delete with an ASSERT. I definitely want to leave the ASSERT there, because m_lineBoxes should never be non-NULL and if when is then it signals a bug, likely a security bug.

I see the your point that a lot of different bugs seem to create that condition, and it is possible (though not really certain) that putting the delete back in would prevent some of these bugs from being security vulnerabilities.

Can we have both the ASSERT and the check+delete? I'm not sure if reviewers would like that but maybe it's worth a try.

### ke...@chromium.org (2011-12-05)

I just re-uploaded this test case to cluster-fuzz because my diagnosis looked suspiciously like this bug:
https://bugs.webkit.org/show_bug.cgi?id=69267

Cluster-fuzz gives no repro on it now. I think WebKit r101556 might have fixed this issue, working on verifying.

### in...@chromium.org (2011-12-05)

Can we have both the ASSERT and the check+delete?

Yeah definitely. That is a good idea and i have done that before. 

### ke...@chromium.org (2011-12-06)

Ryosuke's change to isolates affected the control flow for this bug, but it still manifests, so this has to stay open.

I'm attaching another test case that slaweck provided on https://crbug.com/chromium/104859. Cluster-fuzz dupes it to https://cluster-fuzz.appspot.com/testcase?key=2370333, which is in c#3.

### in...@chromium.org (2011-12-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=3148617

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7fa9b766f6b1
Crash State:
  - crash stack -
  WebCore::InlineBox::deleteLine
  WebCore::InlineFlowBox::deleteLine
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=111700:112063

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94ftSIddfORs7ZD2AIXMtDF08pjo_KVfQ4uusugMHNEhf7g-uT1zzo1QPrYStIHJqG_Mdyv1DeD9DkzREZdodoQRv5D17XMb28BeFtJ3962Ai7c8aNlTMSbuUS7JXB0AVIjD--6bD61QhqnKNkGZdgZ14KF0Q

### in...@chromium.org (2011-12-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=2370333

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f5aefc866b1
Crash State:
  - crash stack -
  WebCore::InlineBox::deleteLine
  WebCore::InlineFlowBox::deleteLine
  - free stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderInline::willBeDestroyed
  

Minimized Testcase (0.60 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Gi5rEjE8ZmPnvtFRIsH4SzqlMx3mt8Rh8h3MYfezlzMTIMSH8Ku433nSLm7NP8fSr1W0lppZhdjB-hg0r1VoOIqlS0E0BRXqSNQo6PFpYfvAwcOcwPb_NAEU3UQwrMJYZLFe1Ga7EzD-ZnrLXF-znmTT57w

### in...@chromium.org (2011-12-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=2343865

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7fa9667faeb1
Crash State:
  - crash stack -
  WebCore::InlineBox::deleteLine
  WebCore::InlineFlowBox::deleteLine
  - free stack -
  WebCore::RenderObject::willBeDestroyed
  WebCore::RenderBlock::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=112559:112644

Minimized Testcase (1.03 Kb): https://cluster-fuzz.appspot.com/download/AMIfv954Hgoyuy3AK1F5vlpmQk9xlHpw_4F0OYkve1J6y9UAh4lypRrW2yYf1IkWR8a2ou4WM4MGz7B7Fhz8KcVs-gsbU815Jk0w7z0qC3XWl4fnEfPI94RxOFLDG1pBoILqY624jFTTcwrsGGanWbO0tSbtFrmNjw

### ke...@chromium.org (2011-12-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-12-13)

Upstream as https://bugs.webkit.org/show_bug.cgi?id=74311

### js...@chromium.org (2011-12-13)

Bulk edit for pending m17 beta release.

### ke...@chromium.org (2011-12-15)

Landed: http://trac.webkit.org/changeset/102875

### in...@chromium.org (2011-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-12-21)

@slaweck: thanks for your help in this area. You provided slightly different and helpful repros to our internal ClusterFuzz efforts, so a $500 Chromium Security Reward. To be sure to maximize rewards, please try and de-duplicate crash reports to identify unique bugs.

Also changing SecImpacts-Beta to SecImpacts-None since we haven't yet put out a Chrome 17 beta release. We should merge this fix before then :)

### ke...@google.com (2012-01-03)

Can someone merge this today?

### in...@chromium.org (2012-01-03)

merged to m17 in r103966

### sc...@gmail.com (2012-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### ke...@chromium.org (2012-07-13)

[Empty comment from Monorail migration]

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

ClusterFuzz has detected this issue as fixed in range 114622:114634.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=2154493

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x7f7f7e4e18b1
Crash State:
  - crash stack -
  WebCore::InlineBox::deleteLine
  WebCore::InlineFlowBox::deleteLine
  - free stack -
  WebCore::FrameView::updateWidgets
  WebCore::FrameView::performPostLayoutTasks
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=108984:109026
Fixed: https://cluster-fuzz.appspot.com/revisions?range=114622:114634

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95gm0T39seVMwA_LsTtSBelV55mMaJZMTf9x6VQXb5f9fUl0T8PW5BnhWwksHKUL57NpMlE6iaviLgfV6wsSs9r12hV9v9CibGjnrqlTj4TZ7BHihxKo8_QpWh6UT7QVMQNdLAXftssUNjyBkOWwbaMwJxwsg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/106200?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/107192, crbug.com/chromium/107555]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051779)*
