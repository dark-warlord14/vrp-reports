# Heap-buffer-overflow in SkOpSegment::addCoinOutsides

| Field | Value |
|-------|-------|
| **Issue ID** | [40080542](https://issues.chromium.org/issues/40080542) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ca...@chromium.org |
| **Created** | 2014-09-28 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5152611855499264

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x619000051d90
Crash State:
  SkOpSegment::addCoinOutsides
  SkOpSegment::addTCoincident
  SkOpContour::calcCommonCoincidentWinding
  

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94owLLuZkw5Z_M8FOMUo0auZBDQgRACkYWFgku9v5S89UKyD5DShITL_L8phWhP0Ouj-B-o_TLN4P0Zi5prkTF4gzJI_C482aoPkV73v8AiEbcD7qD_kXT8MRKEV_qRLGMu15ou4AV6mPeyauymQq_WrjNmnQ

Filer: inferno

## Timeline

### in...@chromium.org (2014-09-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-28)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4998706534285312

### cl...@chromium.org (2014-09-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998706534285312

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x619000076b90
Crash State:
  SkOpSegment::addCoinOutsides
  SkOpSegment::addTCoincident
  SkOpContour::calcCommonCoincidentWinding
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Eb7niLvm2tEs11UNaYubkL0ihrPkxpujpWdcrnXDVl5EedcwX5gd86gJFANGkp7xnWqJYD11LWKwOpt9ImFdZgo9vO4c5WNLC_K4L8_XvXjgNy23ARN9ZFp0ZuCw95EMJkuRzCsq0EsAQqhK6IekAjq2x9Q



### in...@chromium.org (2014-09-28)

[Empty comment from Monorail migration]

### ca...@chromium.org (2014-09-29)

Skia test case generated from Chrome:

static void op1(skiatest::Reporter* reporter, const char* filename) {
    SkPath path;
    path.setFillType((SkPath::FillType) 1);
path.moveTo(SkBits2Float(0x430c0000), SkBits2Float(0x42200000));
path.lineTo(SkBits2Float(0x43480000), SkBits2Float(0x43520000));
path.lineTo(SkBits2Float(0x42200000), SkBits2Float(0x42c80000));
path.lineTo(SkBits2Float(0x64969569), SkBits2Float(0x42c80000));
path.lineTo(SkBits2Float(0x64969569), SkBits2Float(0x43520000));
path.lineTo(SkBits2Float(0x430c0000), SkBits2Float(0x42200000));
path.close();

    SkPath path1(path);
    path.reset();
    path.setFillType((SkPath::FillType) 0);
path.moveTo(SkBits2Float(0x43200000), SkBits2Float(0x42700000));
path.lineTo(SkBits2Float(0x435c0000), SkBits2Float(0x43660000));
path.lineTo(SkBits2Float(0x42700000), SkBits2Float(0x42f00000));
path.lineTo(SkBits2Float(0x64969569), SkBits2Float(0x42f00000));
path.lineTo(SkBits2Float(0x64969569), SkBits2Float(0x43660000));
path.lineTo(SkBits2Float(0x43200000), SkBits2Float(0x42700000));
path.close();

    SkPath path2(path);
    testPathOp(reporter, path1, path2, (SkPathOp) 2, filename);
}


### ca...@chromium.org (2014-09-29)

Fixed in Skia: https://codereview.chromium.org/607913007 committed to the Skia codebase as c06d9a7a7e7fdd7002e6f7e41e78d90cadfb6094

### in...@chromium.org (2014-09-29)

We will let you do the skia roll to pick up change in chrome.

### ca...@chromium.org (2014-09-29)

Skia change landed into Chrome as https://crrev.com/ef5e10a622157f30ef36fb2e4905d7df900294ee

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-30)

ClusterFuzz has detected this issue as fixed in range 296715:297214.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4998706534285312

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x619000076b90
Crash State:
  SkOpSegment::addCoinOutsides
  SkOpSegment::addTCoincident
  SkOpContour::calcCommonCoincidentWinding
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=296715:297214

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95Eb7niLvm2tEs11UNaYubkL0ihrPkxpujpWdcrnXDVl5EedcwX5gd86gJFANGkp7xnWqJYD11LWKwOpt9ImFdZgo9vO4c5WNLC_K4L8_XvXjgNy23ARN9ZFp0ZuCw95EMJkuRzCsq0EsAQqhK6IekAjq2x9Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-09-30)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5152611855499264

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x619000051d90
Crash State:
  SkOpSegment::addCoinOutsides
  SkOpSegment::addTCoincident
  SkOpContour::calcCommonCoincidentWinding
  

Minimized Testcase (0.44 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94owLLuZkw5Z_M8FOMUo0auZBDQgRACkYWFgku9v5S89UKyD5DShITL_L8phWhP0Ouj-B-o_TLN4P0Zi5prkTF4gzJI_C482aoPkV73v8AiEbcD7qD_kXT8MRKEV_qRLGMu15ou4AV6mPeyauymQq_WrjNmnQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-01-05)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-01-22)

$1000 for the report, +$500 for ClusterFuzz.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/418381?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080542)*
