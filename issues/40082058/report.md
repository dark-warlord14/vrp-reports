# Heap-double-free in SkPictureData::~SkPictureData

| Field | Value |
|-------|-------|
| **Issue ID** | [40082058](https://issues.chromium.org/issues/40082058) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5849770518642688

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Heap-double-free
Crash Address: 0x609000009e90
Crash State:
  SkPictureData::~SkPictureData
  SkPictureData::~SkPictureData
  SkPictureData::CreateFromBuffer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=321145:321437

Minimized Testcase (0.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97et34PDpvBnUZ520T_8Iq_4nMqPrS5TIQGmbFVFBd4wWfQOpOT55_aeu0o25iAl56plm52cpg-ukepeaP-qx-4JQq_dmR-NbBQTY080vpfGXVdPffsC-hZLIp3sEGNdir7FwmecfKDISrWFNb_XWMfCGBO3A

Filer: mbarbella

## Timeline

### mb...@chromium.org (2015-05-11)

Bulk edit: I'm starting to look at some of the crashes from the batch of test cases we got now, but could use help with triage.

### mb...@chromium.org (2015-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### md...@chromium.org (2015-05-19)

It looks like this is probably because of the

    SkDELETE_ARRAY(fPictureRefs);

in SkPictureData::parseBufferTag (added by https://codereview.chromium.org/195223003).  Since it doesn't NULL out the fPictureRefs field afterwards, it's going to be freed again in the SkPictureData destructor.

The same problem appears to happen in parseStreamTag too.

(More generally, manual memory management like this seems like a very error-prone practice, but I'm not familiar with Skia development.)

### md...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-19)

Would the fix for https://crbug.com/chromium/486947 also resolve this?

### [Deleted User] (2015-05-19)

Yes.  It'll fix anything with SkPictureShader on the stack and SkRectShaderImageFilter above it.

### mb...@chromium.org (2015-05-20)

This is fixed in that it shouldn't be possible to trigger this in chromium now, but it seems like it would still be worth addressing c#7.

### am...@chromium.org (2015-05-20)

Is there a merge required here?

### cl...@chromium.org (2015-05-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-21)

ClusterFuzz has detected this issue as fixed in range 330758:330903.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5849770518642688

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Heap-double-free
Crash Address: 0x609000009e90
Crash State:
  SkPictureData::~SkPictureData
  SkPictureData::~SkPictureData
  SkPictureData::CreateFromBuffer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=321145:321437
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub&range=330758:330903

Minimized Testcase (0.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97et34PDpvBnUZ520T_8Iq_4nMqPrS5TIQGmbFVFBd4wWfQOpOT55_aeu0o25iAl56plm52cpg-ukepeaP-qx-4JQq_dmR-NbBQTY080vpfGXVdPffsC-hZLIp3sEGNdir7FwmecfKDISrWFNb_XWMfCGBO3A

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### pe...@chromium.org (2015-06-30)

No merge required here.   https://crbug.com/chromium/486947 is approved for merge (which is the fix for this).

### ti...@google.com (2015-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-28)

@cloudfuzzer - *finally* working through the backlog and decided to award you $5,000 for this report. Your other bugs pending payment will follow suit shortly.

Thanks for your patience! 



### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/486945?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082058)*
