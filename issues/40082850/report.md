# Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel;DOMWrapperMap.h:148:20

| Field | Value |
|-------|-------|
| **Issue ID** | [40082850](https://issues.chromium.org/issues/40082850) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Bindings |
| **Platforms** | Linux |
| **Reporter** | th...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2015-09-13 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5492489312534528

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f0909ea8150
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel
  DOMWrapperMap.h:148:20
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=348139:348261

Minimized Testcase (1.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95JXZesoQKkBirEAu3bMGHrOebaWuUDCfY4JjxxbZDYCTeB4Yg-KDDyByNFen5al_E2iOpA5FwBqhlmTHdrs2AXx46VVBQjPbfgdK00-VKYr7OZBb7k7pGoDUYwg_Wx3Wu9HFMEXWYgA1zn9Oafm4lzx7RNYg

Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### cl...@chromium.org (2015-09-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6581135075704832

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x000000000000
Crash State:
  Bad-cast to blink::ScriptWrappable from invalid vptr
  DOMWrapperMap.h:148:20
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=348347:348403

Minimized Testcase (4.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94C_QISKyXNtfHm3Wgpsun3j8RZeFw32fifYRI75V3R_Z4hxL0nMHNUdRif9GoBxMF-QNE4gyY87STFb8KOGc12-l7EmU5wi9aCd1UK9HA8sO0OlSusAKf8oteiKiPH8K7_AoYYJaWRUKOvgU-87Et7X7hCRA

Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-09-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5929541057380352

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f43dc009610
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::DirectoryEntry
  DOMWrapperMap.h:148:20
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95pqjkqDDImKtzE1fYmSNv10yrRDI_7jsDdaAZ0YVccocb3otI63WCnC0tyLYcv0Jfu0r_xh8CZYoeEPLTtq4XJiz0V-_gGXFpUnP-gC1TqwY_WWt5kPXZ30qXdm2IMeLF6w0gXRwLqYnoLTBDuYoPp-YWZSw


Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### in...@chromium.org (2015-09-13)

Yuki, this looks like a new bug and still reproducing.

### cl...@chromium.org (2015-09-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-13)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-09-13)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6581135075704832

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x000000000000
Crash State:
  Bad-cast to blink::ScriptWrappable from invalid vptr
  DOMWrapperMap.h:148:20
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=348347:348403

Minimized Testcase (4.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94C_QISKyXNtfHm3Wgpsun3j8RZeFw32fifYRI75V3R_Z4hxL0nMHNUdRif9GoBxMF-QNE4gyY87STFb8KOGc12-l7EmU5wi9aCd1UK9HA8sO0OlSusAKf8oteiKiPH8K7_AoYYJaWRUKOvgU-87Et7X7hCRA

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-09-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4746427857633280

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f56d51ceff0
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::V8FileSystemCallback
  DOMWrapperMap.h:148:20
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=348139:348261

Minimized Testcase (2.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96RKZHdp78HkBJo6iAZCSx98p66oltUlUaIcXzdPHrmol-76SD-EpQPuLOutqT2cZmFtMPL2r6bnfESEn8BZ7JUKAEpl0hjBondv0T5MWR2Ihb2zcSsD5NKLWhCFcDuRot_dxEEYTqjbCfZcPiHAPDacEsrUg

Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2015-09-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6581777844404224

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7ff60c04d3c0
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel::Peer
  DOMWrapperMap.h:148:20
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96L9hD9Uxi6x2gIs4YkyzGovvcfoV17JtmRL15J34fC6GDvlxTC4NBCOEMWis11wP7q5TYSXeoHn0nA7guXtG2plD9Vp14kfVD0q999qzkoISr4YxOdOWBF9lglicDokaEUSJ7z0LFeBOzu8wxhqezfk3iIEA


Additional requirements: Requires HTTP

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### yu...@chromium.org (2015-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-14)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6581777844404224

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7ff60c04d3c0
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel::Peer
  DOMWrapperMap.h:148:20
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96L9hD9Uxi6x2gIs4YkyzGovvcfoV17JtmRL15J34fC6GDvlxTC4NBCOEMWis11wP7q5TYSXeoHn0nA7guXtG2plD9Vp14kfVD0q999qzkoISr4YxOdOWBF9lglicDokaEUSJ7z0LFeBOzu8wxhqezfk3iIEA


Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-09-14)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5929541057380352

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f43dc009610
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::DirectoryEntry
  DOMWrapperMap.h:148:20
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95pqjkqDDImKtzE1fYmSNv10yrRDI_7jsDdaAZ0YVccocb3otI63WCnC0tyLYcv0Jfu0r_xh8CZYoeEPLTtq4XJiz0V-_gGXFpUnP-gC1TqwY_WWt5kPXZ30qXdm2IMeLF6w0gXRwLqYnoLTBDuYoPp-YWZSw


Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### jw...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-17)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4746427857633280

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f56d51ceff0
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::V8FileSystemCallback
  DOMWrapperMap.h:148:20
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=348139:348261

Minimized Testcase (2.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96RKZHdp78HkBJo6iAZCSx98p66oltUlUaIcXzdPHrmol-76SD-EpQPuLOutqT2cZmFtMPL2r6bnfESEn8BZ7JUKAEpl0hjBondv0T5MWR2Ihb2zcSsD5NKLWhCFcDuRot_dxEEYTqjbCfZcPiHAPDacEsrUg

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202431

------------------------------------------------------------------
r202431 | yukishiino@chromium.org | 2015-09-17T06:42:09.963955Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/DOMDataStore.h?r1=202431&r2=202430&pathrev=202431
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/WrapperTypeInfo.cpp?r1=202431&r2=202430&pathrev=202431
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8NPObject.cpp?r1=202431&r2=202430&pathrev=202431
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/DOMWrapperMap.h?r1=202431&r2=202430&pathrev=202431
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/WrapperTypeInfo.h?r1=202431&r2=202430&pathrev=202431

bindings/oilpan: Stops casting to ScriptWrappable* in DOMWrapperMap.

CFI(Control Flow Integrity) detects bad casting to ScriptWrappable*
from void* which points to a dead object.  We need almost the same fix
as http://crrev.com/1340513002 in DOMWrapperMap, too.

BUG=531057

Review URL: https://codereview.chromium.org/1336323002
-----------------------------------------------------------------

### yu...@chromium.org (2015-09-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-17)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5492489312534528

Fuzzer: therealholden_worker
Job Type: linux_cfi_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x7f0909ea8150
Crash State:
  Bad-cast to blink::ScriptWrappable from blink::WorkerWebSocketChannel
  DOMWrapperMap.h:148:20
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_cfi_chrome&range=348139:348261

Minimized Testcase (1.56 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95JXZesoQKkBirEAu3bMGHrOebaWuUDCfY4JjxxbZDYCTeB4Yg-KDDyByNFen5al_E2iOpA5FwBqhlmTHdrs2AXx46VVBQjPbfgdK00-VKYr7OZBb7k7pGoDUYwg_Wx3Wu9HFMEXWYgA1zn9Oafm4lzx7RNYg

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### cl...@chromium.org (2015-12-24)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

This is another reward backlog bug that we cleared out last week - $3,500 here as well. Thanks!

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

This issue was migrated from crbug.com/chromium/531057?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Bindings]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082850)*
