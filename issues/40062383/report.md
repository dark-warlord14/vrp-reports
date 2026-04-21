# oob in RTCStatsCollector::ProduceTransportStats_n

| Field | Value |
|-------|-------|
| **Issue ID** | [40062383](https://issues.chromium.org/issues/40062383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2022-12-25 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

tested chrome version:  

Chromium 111.0.5497.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1086812.zip)  

Chromium 110.0.5478.4  

os version:  

22.04  

repro steps:  

(1) python3 -m http.server 8000 --dir=|Directory path for containing the crash.html file.|  

(2) ./chrome --user-data-dir=/tmp/xx --incognito <http://localhost:8000/crash.html>

The above method is very stable to repro in non-asan version, but may not be stable in asan version. If the asan version cannot reproduce, you can try the launcher.sh script. This script can open and execute multiple browsers at the same time. You need to modify the path of chrome and crash.html in the script.

**Problem Description:**  

RTCStatsCollector::ProduceTransportStats\_n` performs a lookup in the transport\_cert\_stats vector without first checking whether the iterator is valid(There is a debug version of Check), which will result in accessing data past the end of the vector.

void RTCStatsCollector::ProduceTransportStats\_n(

```
  const auto& certificate_stats_it =  
      transport_cert_stats.find(transport_name);  
  RTC_DCHECK(certificate_stats_it != transport_cert_stats.cend());   
  std::string local_certificate_id;  
  if (certificate_stats_it->second.local) {  
    local_certificate_id = RTCCertificateIDFromFingerprint(  
        certificate_stats_it->second.local->fingerprint);  
  }  
  std::string remote_certificate_id;  
  if (certificate_stats_it->second.remote) {  
    remote_certificate_id = RTCCertificateIDFromFingerprint(  
        certificate_stats_it->second.remote->fingerprint);  
  }  

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/rtc_stats_collector.cc;drc=50454ef84abbd479d65cfce8711639d786aa2476;l=2193>

patch suggestion:  

diff --git a/pc/rtc\_stats\_collector.cc b/pc/rtc\_stats\_collector.cc  

index 374780e941..43c210c70b 100644  

--- a/pc/rtc\_stats\_collector.cc  

+++ b/pc/rtc\_stats\_collector.cc  

@@ -2191,7 +2191,12 @@ void RTCStatsCollector::ProduceTransportStats\_n(  

// exist.  

const auto& certificate\_stats\_it =  

transport\_cert\_stats.find(transport\_name);

- RTC\_DCHECK(certificate\_stats\_it != transport\_cert\_stats.cend());

- //RTC\_DCHECK(certificate\_stats\_it != transport\_cert\_stats.cend());
- if (certificate\_stats\_it == transport\_cert\_stats.cend()) {
- ```
   RTC_LOG(LS_ERROR) << "Unable to find certificate stats for transport"  
  
  ```
- ```
                     << transport_name;  
  
  ```
- ```
   continue;  
  
  ```
- }  
  
  std::string local\_certificate\_id;  
  
  if (certificate\_stats\_it->second.local) {  
  
  local\_certificate\_id = RTCCertificateIDFromFingerprint(

**Additional Comments:**

\*\*Chrome version: \*\* 111.0.5497.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.1 KB)
- [RTCPeerConnection-helper.js](attachments/RTCPeerConnection-helper.js) (text/plain, 22.9 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 977 B)
- [asan-SEGV_MAPERR.log](attachments/asan-SEGV_MAPERR.log) (text/plain, 8.2 KB)
- [asan2-buffer-overflow.log](attachments/asan2-buffer-overflow.log) (text/plain, 20.9 KB)

## Timeline

### [Deleted User] (2022-12-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5109705476341760.

### xi...@chromium.org (2022-12-26)

Thanks for the report. I tried several times but still not able to reproduce on the ASAN or non ASAN builds. +hta@, could you take a look? Thanks!

I'm not sure if this is a new bug so setting FoundIn-108 for now.

[Monorail components: Blink>WebRTC>PeerConnection]

### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-12-27)

Have you tried launcher.js? If you still cannot reproduce it, you can also directly test it in the official latest release version, which should be easy to reproduce. I just tested it in 108.0.5359.124 (officail build arm64).

### [Deleted User] (2022-12-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-08)

hta: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2023-01-13)

Hm. The repro script basically creates pairs of PCs and connects them (ensuring they're not garbage collected), and when it can't do any more, it reloads the page. I have a suspicion that the real reason why this happens is an OOM that prevents the certificate from being put into the right place.




### ht...@chromium.org (2023-01-20)

Reporter: Can you check if this bug is affected by https://webrtc-review.googlesource.com/c/src/+/291112 that fixed a different bug involving missing certificates?


### hb...@chromium.org (2023-01-20)

I also landed https://webrtc-review.googlesource.com/c/src/+/291109 today which would avoid the oob even if the certificates were not found

### em...@gmail.com (2023-01-20)

#10
Confirmed, the issue does not repro after patching.
tested chromium version:
Chromium 110.0.5481.24

### ht...@chromium.org (2023-01-20)

Jubilation!


### ht...@chromium.org (2023-01-20)

(note: this report came in earlier than the one that got assigned to hbos that caused him to fix the issue.)


### em...@gmail.com (2023-01-20)

[Comment Deleted]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M108. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2023-01-21)

There is nothing here to merge, the CLs that need merging are being processed on another bug (CLs referenced in https://crbug.com/chromium/1403573#c10 and #11).

Deleteing merge-review labels.


### am...@chromium.org (2023-01-23)

Fix for this issue was landed https://crbug.com/chromium/1408392. Please merge either reports as a duplicate just yet. This issue was reported before https://crbug.com/chromium/1408392, and should be considered for potential VRP reward and CVE. 
The merge processes are occurring on https://crbug.com/chromium/1408392, so that report cannot be merged into this one yet. 

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-13)

cc'ing reporters of https://crbug.com/chromium/1408392 with permission of OP 

### [Deleted User] (2023-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403573?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062383)*
