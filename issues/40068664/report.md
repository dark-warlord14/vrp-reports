# Security:  Use After Free in NetworkStateNotifier

| Field | Value |
|-------|-------|
| **Issue ID** | [40068664](https://issues.chromium.org/issues/40068664) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network, Platform |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ka...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2023-08-03 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Root cause:  

Web worker listens to network state changes by adding observers to NetworkStateNotifier’s connection\_observers\_, which is a HashMap. When erasing an observer in connection\_observers\_ without acquiring lock will lead to heap use-after-free or heap buffer-overflow.

Detail:  

Web worker listens to network state changes by adding observers to NetworkStateNotifier’s connection\_observers\_, which is a HashMap. Since HashMap is not thread-safe, a lock should be acquired when accessing it.  

In this case, the observer in connection\_observers\_ will be removed when there are no other listeners in the web worker. However, in function NetworkStateNotifier::RemoveObserver, no lock is acquired before erasing observer element from connection\_observers\_, which will cause heap use-after-free or heap buffer-overflow if another thread is accessing the HashMap at the same time.

Code link: Add observer into connection\_observers\_.  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/platform/network/network_state_notifier.cc;l=185;drc=2d2b9b660aaaa89018ad12bf053075bba58ce787>

std::unique\_ptr[NetworkStateNotifier::NetworkStateObserverHandle](javascript:void(0);)  

NetworkStateNotifier::AddConnectionObserver(  

NetworkStateObserver\* observer,  

scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) task\_runner) {  

AddObserverToMap(connection\_observers\_, observer, task\_runner);  

return std::make\_unique[NetworkStateNotifier::NetworkStateObserverHandle](javascript:void(0);)(  

this, ObserverType::kConnectionType, observer, task\_runner);  

}

Code link: Delete observer:  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/platform/network/network_state_notifier.cc;l=355;drc=2d2b9b660aaaa89018ad12bf053075bba58ce787>

void NetworkStateNotifier::RemoveObserver(  

ObserverType type,  

NetworkStateObserver\* observer,  

scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) task\_runner) {  

DCHECK(task\_runner->RunsTasksInCurrentSequence());  

DCHECK(observer);

ObserverListMap& map = GetObserverMapFor(type);  

DCHECK\_NE(map.end(), map.find(observer));  

map.erase(observer);  

}

**VERSION**  

Chrome Version: [112.0.5615.49] ~ Latest Stable Version

**REPRODUCTION CASE**

1. Host poc.html  
   
   python -m SimpleHTTPServer 8000
2. Elsewhere run  
   
   ./chrome <http://localhost:8000/poc.html>
3. Wait a few seconds to see the crash log

\*\*bisect\*\*  

The bug is introduced in the following commit. The first stable version that contains the commit is ‘112.0.5615.49’.  

<https://chromium.googlesource.com/chromium/src/+/9c3ac3d9ceea60ad946b807f8661fce2588d2056>

\*\*FIX\*\*  

The following diff shows my suggestion about how to fix this issue.

## diff --git a/third\_party/blink/renderer/platform/network/network\_state\_notifier.cc b/third\_party/blink/renderer/platform/network/network\_state\_notifier.cc index 39c417e0f8ec6..b65001842aa60 100644 --- a/third\_party/blink/renderer/platform/network/network\_state\_notifier.cc +++ b/third\_party/blink/renderer/platform/network/network\_state\_notifier.cc @@ -349,7 +349,8 @@ void NetworkStateNotifier::RemoveObserver( scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) task\_runner) { DCHECK(task\_runner->RunsTasksInCurrentSequence()); DCHECK(observer);


- base::AutoLock locker(lock\_);  
  
  ObserverListMap& map = GetObserverMapFor(type);  
  
  DCHECK\_NE(map.end(), map.find(observer));  
  
  map.erase(observer);

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: anonymous

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 76.3 KB)

## Timeline

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6197846220668928.

### cl...@chromium.org (2023-08-03)

Testcase 6197846220668928 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6197846220668928.

### ts...@chromium.org (2023-08-03)

Clicked "Retry" on CF.  Will do a few more times to see if it can hit it.

### cl...@chromium.org (2023-08-03)

Testcase 6197846220668928 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6197846220668928.

### ts...@chromium.org (2023-08-03)

CF DNR, assigning tentatively and setting foundin per claimed bisect. Perhaps there is enough information in the trace and analysis to move forward.

[Monorail components: Platform]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-03)

ClusterFuzz testcase 6197846220668928 appears to be flaky, updating reproducibility label.

### [Deleted User] (2023-08-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-08-15)

[secondary shepherd] 	yoichio@, could you confirm you intend to take a look at this, or if not, could you help re-triage?

[Monorail components: Blink>Network]

### ad...@google.com (2023-08-15)

(I am a bot: this is an auto-cc on a security bug)

### yo...@chromium.org (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a41479ba6efb5e48b82edad972c7dded6f385b79

commit a41479ba6efb5e48b82edad972c7dded6f385b79
Author: Yoichi Osato <yoichio@chromium.org>
Date: Thu Aug 24 05:33:18 2023

Readd lock when ObserverListMap::erase()

We should lock when remove an item from the map.
This lock was accidentally removed in:
https://chromium-review.googlesource.com/c/chromium/src/+/4280021

Bug: 1469928
Change-Id: I2512e14d4ad9b246cadae947023dbccb5158da51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790983
Auto-Submit: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1187668}

[modify] https://crrev.com/a41479ba6efb5e48b82edad972c7dded6f385b79/third_party/blink/renderer/platform/network/network_state_notifier.cc


### yo...@chromium.org (2023-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-25)

Requesting merge to stable M116 because latest trunk commit (1187668) appears to be after stable branch point (1160321).

Requesting merge to beta M117 because latest trunk commit (1187668) appears to be after beta branch point (1181205).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-08-25)

Setting OSes liberally - please feel free to remove any OSes that are surely not impacted.

### [Deleted User] (2023-08-26)

Requesting merge to stable M116 because latest trunk commit (1187668) appears to be after stable branch point (1160321).

Requesting merge to beta M117 because latest trunk commit (1187668) appears to be after beta branch point (1181205).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-27)

Requesting merge to stable M116 because latest trunk commit (1187668) appears to be after stable branch point (1160321).

Requesting merge to beta M117 because latest trunk commit (1187668) appears to be after beta branch point (1181205).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2023-08-28)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4790983

2. Has this fix been tested on Canary?
No. Since this is subtle race condition and hard to write a test.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
No?

4. Does this fix pose any known compatibility risks?
No?

5. Does it require manual verification by the test team? If so, please describe required testing.
No.

### pg...@google.com (2023-08-28)

Merge approved for M116! please merge to branch 5845 by Thursday EOD (MTV time) to get this fix into the next M116 stable respin!
Merge approved for M117! please merge to branch 5938 by Tuesday EOD (MTV time) to get this fix into M117 beta!

### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5f30f24fe7f688ac8ed7ec0edd1b7284b031018c

commit 5f30f24fe7f688ac8ed7ec0edd1b7284b031018c
Author: Yoichi Osato <yoichio@chromium.org>
Date: Tue Aug 29 01:49:50 2023

Readd lock when ObserverListMap::erase()

We should lock when remove an item from the map.
This lock was accidentally removed in:
https://chromium-review.googlesource.com/c/chromium/src/+/4280021

(cherry picked from commit a41479ba6efb5e48b82edad972c7dded6f385b79)

Bug: 1469928
Change-Id: I2512e14d4ad9b246cadae947023dbccb5158da51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790983
Auto-Submit: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1187668}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4820048
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/branch-heads/5938@{#699}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/5f30f24fe7f688ac8ed7ec0edd1b7284b031018c/third_party/blink/renderer/platform/network/network_state_notifier.cc


### [Deleted User] (2023-08-29)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/74a2eb9c8cb203d7cb916cfcd73053b1be745a2b

commit 74a2eb9c8cb203d7cb916cfcd73053b1be745a2b
Author: Yoichi Osato <yoichio@chromium.org>
Date: Tue Aug 29 02:37:46 2023

Readd lock when ObserverListMap::erase()

We should lock when remove an item from the map.
This lock was accidentally removed in:
https://chromium-review.googlesource.com/c/chromium/src/+/4280021

(cherry picked from commit a41479ba6efb5e48b82edad972c7dded6f385b79)

Bug: 1469928
Change-Id: I2512e14d4ad9b246cadae947023dbccb5158da51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790983
Auto-Submit: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Yoichi Osato <yoichio@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1187668}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4820108
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1666}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/74a2eb9c8cb203d7cb916cfcd73053b1be745a2b/third_party/blink/renderer/platform/network/network_state_notifier.cc


### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-29)

Not needed, the fix merged to 113 and it's present in the 114 branch.

### rz...@google.com (2023-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-31)

Issue was introduced by https://crrev.com/c/4280021, not merged to 108

### pg...@google.com (2023-09-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations! The VRP Panel has decided to award you $10,000 for this report of this UAF in the network process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work!  

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1469928?no_tracker_redirect=1

[Multiple monorail components: Blink>Network, Platform]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068664)*
