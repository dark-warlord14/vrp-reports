# Use-of-uninitialized-value in SkRecords::FillBounds::adjustAndMap

| Field | Value |
|-------|-------|
| **Issue ID** | [40081849](https://issues.chromium.org/issues/40081849) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mb...@chromium.org |
| **Created** | 2015-04-13 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5999705134202880

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkRecords::FillBounds::adjustAndMap
  void SkRecord::Record::visit<void, SkRecords::FillBounds>
  SkRecordFillBounds
  

Minimized Testcase (3.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95wOCQYwHv6X8xz63H6kL70KfMOOaUDt0W3JHO9OUVnq8aBAMPsHmhzL-jAjNATa2ZtlLN7pQ_Q6i19P7dx109df_UlFqRLsVzMNicQX72OVsE8ZMbyETEWWrjdXPZ8bKYeZZ9wGD87CvgbO3Ol-ePHV0zGuA

Filer: inferno

## Timeline

### in...@chromium.org (2015-04-13)

Author: robertphillips
Component: skia
Changelist: https://chromium.googlesource.com/skia.git/+/4e8e3421aa919a82eb1dd287fecbd079f5a320b4
Time: Wed Nov 12 14:46:08 2014
The CL last changed line 200 of file SkRecordDraw.cpp, which is stack frame 1.

### cl...@chromium.org (2015-04-13)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-04-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2015-04-27)

From the call stack it sure looks like we're getting an uninitialized bound for a TextBlob (although that should be impossible).

### [Deleted User] (2015-04-27)

So, I have tracked this as far as the HarfBuzzShaper but am, somewhat, at a loss as how to continue. It appears that bidirectional text is falling into the 'ComplexPath' case in Font::buildGlyphBuffer. For this example shaper.totalWidth() is returning an uninitialized value. This uninitialized value then pollutes the computation of the textblob's bounding box which gets accessed by Skia when drawing.

### [Deleted User] (2015-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2015-04-27)

So, I posted https://codereview.chromium.org/1103233003 but I defer to https://codereview.chromium.org/1108663003/.

### mb...@chromium.org (2015-04-27)

Thanks for taking a look and sorry for not updating this bug. I originally posted that patch with the wrong bug number associated with it, and forgot to mention it here.

### [Deleted User] (2015-04-27)

Readding derat (who has something to add).

### de...@chromium.org (2015-04-27)

(Repasting earlier comment.)

I don't know anything about this code, but I assume that this is pointing to a larger issue where the shaper is being used even though shape() either didn't get called or didn't complete successfully.

### bu...@chromium.org (2015-04-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=194541

------------------------------------------------------------------
r194541 | mbarbella@chromium.org | 2015-04-27T19:37:47.439909Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/shaping/shaping-width-initialized-expected.txt?r1=194541&r2=194540&pathrev=194541
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/fonts/shaping/HarfBuzzShaper.cpp?r1=194541&r2=194540&pathrev=194541
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/text/shaping/shaping-width-initialized.html?r1=194541&r2=194540&pathrev=194541

Always initialize |m_totalWidth| in HarfBuzzShaper::shape.

R=leviw@chromium.org
BUG=476647

Review URL: https://codereview.chromium.org/1108663003
-----------------------------------------------------------------

### mb...@chromium.org (2015-04-27)

Regarding c#11, shape was called but createHarfBuzzRuns failed. If anyone else is interested in investigating that case, the test case from the CL in c#12 still triggers that condition. Please file a new bug for this if it is a concern.

Going to mark this as Fixed since it should be initialized either way.

### cl...@chromium.org (2015-04-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mb...@chromium.org (2015-04-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-29)

ClusterFuzz has detected this issue as fixed in range 327115:327281.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5999705134202880

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkRecords::FillBounds::adjustAndMap
  void SkRecord::Record::visit<void, SkRecords::FillBounds>
  SkRecordFillBounds
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=327115:327281

Minimized Testcase (3.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95wOCQYwHv6X8xz63H6kL70KfMOOaUDt0W3JHO9OUVnq8aBAMPsHmhzL-jAjNATa2ZtlLN7pQ_Q6i19P7dx109df_UlFqRLsVzMNicQX72OVsE8ZMbyETEWWrjdXPZ8bKYeZZ9wGD87CvgbO3Ol-ePHV0zGuA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-05-08)

Merge requested for M43 (branch 2357)

### la...@google.com (2015-05-08)

[Automated comment] Less than 2 weeks to go before stable on M43, manual review required.

### mb...@chromium.org (2015-05-11)

Jeff, this would be a good one for testing that the MSan support in Findit is working properly.

### la...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195187

------------------------------------------------------------------
r195187 | mbarbella@chromium.org | 2015-05-11T17:08:05.891807Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/fast/text/shaping/shaping-width-initialized-expected.txt?r1=195187&r2=195186&pathrev=195187
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/platform/fonts/shaping/HarfBuzzShaper.cpp?r1=195187&r2=195186&pathrev=195187
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/fast/text/shaping/shaping-width-initialized.html?r1=195187&r2=195186&pathrev=195187

Merge 194541 "Always initialize |m_totalWidth| in HarfBuzzShaper..."

> Always initialize |m_totalWidth| in HarfBuzzShaper::shape.
> 
> R=leviw@chromium.org
> BUG=476647
> 
> Review URL: https://codereview.chromium.org/1108663003

TBR=leviw@chromium.org

Review URL: https://codereview.chromium.org/1137843003
-----------------------------------------------------------------

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### st...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-28)

Congrats - $500 for this report.

### ti...@google.com (2015-05-28)

-dominik (email bouncing)

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-08-03)

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

This issue was migrated from crbug.com/chromium/476647?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/482194]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081849)*
