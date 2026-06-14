# ASSERTION FAILED: !needsLayout(), UNKNOWN in WebCore::RenderTableSection::paint

| Field | Value |
|-------|-------|
| **Issue ID** | [40078092](https://issues.chromium.org/issues/40078092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | jc...@chromium.org |
| **Created** | 2013-09-12 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5254890674716672

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderTable::paintObject
  WebCore::RenderTable::paint
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668

Minimized Testcase (7.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96l3VyXFF7JPVvx97gAuC2axXPQDsGYV09iJZJGRILVhYfgGFBHffe3ymVfGoBCya3PVcPyDz0Jp02IvDyA4XJcAjKNFRJ9SWTpY-2_gbZQr7OVg6pu_ZQOaeMBF5rhitFwPqFK2Fe6l5RfiFn_V_dZsEUYXw

## Timeline

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

We might need to revert this - http://src.chromium.org/viewvc/blink?view=rev&revision=157488. Since i remember, if we don't bail out (like we previously did), we trigger a use-after-free. CF will hit the security assert, but i think badness happen after that point.

### cl...@chromium.org (2013-09-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5047649912750080

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderLayer::paintOutlineForFragments
  WebCore::RenderLayer::paintLayerContents
  

Minimized Testcase (1.36 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96M7Lefj7ULYTOFqAUhsdMI3hnTJzPnwWBKjuY8KqNT6cpz2_SOxbF0uizbHYQ6T72ACp2GVXcfls9cND57VdmdJb5KSyXZIbXSVNbZJ-X7iwIcGjb_30Ql_FcPBcAupVgOWOSSeUO6eq6rzsNsnuMP2sJp8g

Additional requirements: Requires Interaction Gestures



### cl...@chromium.org (2013-09-13)

ClusterFuzz has detected this issue as fixed in range 222745:222751.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5047649912750080

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderLayer::paintOutlineForFragments
  WebCore::RenderLayer::paintLayerContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668
Fixed: https://cluster-fuzz.appspot.com/revisions?range=222745:222751

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96M7Lefj7ULYTOFqAUhsdMI3hnTJzPnwWBKjuY8KqNT6cpz2_SOxbF0uizbHYQ6T72ACp2GVXcfls9cND57VdmdJb5KSyXZIbXSVNbZJ-X7iwIcGjb_30Ql_FcPBcAupVgOWOSSeUO6eq6rzsNsnuMP2sJp8g

Additional requirements: Requires Interaction Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-14)

This is hitting very frequently on ClusterFuzz. 
https://cluster-fuzz.appspot.com/testcase?key=6056668727083008
https://cluster-fuzz.appspot.com/testcase?key=5877764011851776

I think we should keep the needsLayout bailout unless we get a chance to verify all failures.  esp we need to analyze mitz's cryptic comment in https://bugs.webkit.org/show_bug.cgi?id=92954#c7

reverted in r157798

### cl...@chromium.org (2013-09-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5877764011851776

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderLayer::paintOutlineForFragments
  WebCore::RenderLayer::paintLayerContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668

Minimized Testcase (2.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96IO-cvwi7vClgce8kN-uUyjuZnP7SXh7Ap4PbQfrvFhjh9l-CM8extLX91x1qm-U0j5f1ynbpaiMkugtfcg3yMYhKCpRDYA0vKdoDrfDKX7pu9XBvhmKuydc9sOYed3frZjMSBRZ_boTQmjy4Z1geepJliOA



### cl...@chromium.org (2013-09-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4753242789511168

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderLayer::paintBackgroundForFragments
  WebCore::RenderLayer::paintLayerContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668

Minimized Testcase (11.67 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96g0cJWtAu6XnD7tp7HZwrDeeJBpmpd3SZqcY6MbIsbye1gNwF8O8XeUTtxe5QzNcouL-C-kUg2n-6l1Pv6-wtN8rCKE7KprjaeXxBd81_6WlMEBfQnu6CRvrN4202s6l2pV84VpCKB1lZ-feovsZkURkroVw



### cl...@chromium.org (2013-09-17)

ClusterFuzz has detected this issue as fixed in range 223385:223408.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4753242789511168

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderLayer::paintBackgroundForFragments
  WebCore::RenderLayer::paintLayerContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668
Fixed: https://cluster-fuzz.appspot.com/revisions?range=223385:223408

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96g0cJWtAu6XnD7tp7HZwrDeeJBpmpd3SZqcY6MbIsbye1gNwF8O8XeUTtxe5QzNcouL-C-kUg2n-6l1Pv6-wtN8rCKE7KprjaeXxBd81_6WlMEBfQnu6CRvrN4202s6l2pV84VpCKB1lZ-feovsZkURkroVw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-09-17)

ClusterFuzz has detected this issue as fixed in range 223385:223408.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5877764011851776

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderLayer::paintOutlineForFragments
  WebCore::RenderLayer::paintLayerContents
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668
Fixed: https://cluster-fuzz.appspot.com/revisions?range=223385:223408

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96IO-cvwi7vClgce8kN-uUyjuZnP7SXh7Ap4PbQfrvFhjh9l-CM8extLX91x1qm-U0j5f1ynbpaiMkugtfcg3yMYhKCpRDYA0vKdoDrfDKX7pu9XBvhmKuydc9sOYed3frZjMSBRZ_boTQmjy4Z1geepJliOA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-09-17)

ClusterFuzz has detected this issue as fixed in range 223385:223408.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5254890674716672

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000977537dd
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paint
  WebCore::RenderTable::paintObject
  WebCore::RenderTable::paint
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668
Fixed: https://cluster-fuzz.appspot.com/revisions?range=223385:223408

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96l3VyXFF7JPVvx97gAuC2axXPQDsGYV09iJZJGRILVhYfgGFBHffe3ymVfGoBCya3PVcPyDz0Jp02IvDyA4XJcAjKNFRJ9SWTpY-2_gbZQr7OVg6pu_ZQOaeMBF5rhitFwPqFK2Fe6l5RfiFn_V_dZsEUYXw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mi...@gmail.com (2013-09-26)

can I have the repro case please?

### in...@chromium.org (2013-09-26)

if you login using miaubiz@gmail.com, then you can access any clusterfuzz reports for your fuzzers. e.g. try https://cluster-fuzz.appspot.com/testcase?key=5254890674716672 and click download testcase.

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $500 reward. The assert being hit here tends to lead to OOB reads.

### pa...@chromium.org (2013-12-18)

Payment kicked off on this one and your other two. Sorry about the delay Miaubiz, and thanks again for your help here!

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/290165?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078092)*
