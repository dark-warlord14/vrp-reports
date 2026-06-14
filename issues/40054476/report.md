# potential uaf in rtc_peer_connection

| Field | Value |
|-------|-------|
| **Issue ID** | [40054476](https://issues.chromium.org/issues/40054476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Windows |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2021-01-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36

Steps to reproduce the problem:
1.Here is my opinion about the rtc_peer_connection, keep in mind that my opinion may be wrong.

https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;l=3529

- at this function RTCPeerConnection::CloseInternal() 
```
void RTCPeerConnection::CloseInternal() {
  '''other code '''
  for (auto& dtls_transport_iter : dtls_transports_by_native_transport_) {
    dtls_transport_iter.value->Close(); // here will use the function  RTCDtlsTransport::Close() 
  }

  feature_handle_for_scheduler_.reset();
}
```

And the function 
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/peerconnection/rtc_dtls_transport.cc;drc=131697ea2c25234744fe1917571bfa454c2d22cb;l=102
```
void RTCDtlsTransport::Close() {
  closed_from_owner_ = true;
  if (current_state_.state() != webrtc::DtlsTransportState::kClosed) {
    DispatchEvent(*Event::Create(event_type_names::kStatechange)); // wll trige user's javascript code
  }
  ice_transport_->stop();
}
```

the code pattern is similar as https://bugs.chromium.org/p/chromium/issues/detail?id=1107815

What is the expected behavior?

What went wrong?
above all, sorry for no poc now, I will try to make it.

Did this work before? N/A 

Chrome version: 87.0.4280.141  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-01-16)

Thanks for the report. hbos@, could you take a look on whether this is a potential uaf? Thanks!

[Monorail components: Blink>WebRTC>PeerConnection]

### ht...@chromium.org (2021-01-16)

If I read the other bug correctly, the fear is that one can add a new element to dtls_transports_by_native_transport_ while iterating over the dtls transports.

I don't know why we use an iterator and a list here, though - there should be only one DTLSTransport for each native transport; there's no room in the spec for having more than one. But this may be due to supporting some older code pattern.




### [Deleted User] (2021-01-16)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hb...@chromium.org (2021-01-18)

dtls_transports_by_native_transport_ uses a WeakMember reference so GC is a risk when JS events fire. I think there was a reason for using WeakMember instead of Member? I have fixed similar bugs by copying the vector and then iterating the copy, in this case the copy would need to use strong Member references to avoid the GC.

Although in this case we could just validate the reference prior to invoking it, right?

Care to own this Harald? I think you introduced this map if I recall correctly

### ht...@chromium.org (2021-01-18)

I can own this. As I said in #3, I think it's likely that this can't happen, because there can be only one dtls transport, but it seems sensible to use the copy-vector pattern to be 100% safe.



### ht...@chromium.org (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f62c7bb28b0ce77b773a611c6ba02b361db1c85

commit 4f62c7bb28b0ce77b773a611c6ba02b361db1c85
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 20 10:23:07 2021

Iterate more carefully over DTLS transports at close

Ensure that even if the set of DTLS transports is modified during
callbacks called from close, the process will be well-defined.

Bug: chromium:1167357
Change-Id: I712280e7382a647027912178156127831b437f75
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2639893
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/master@{#845122}

[modify] https://crrev.com/4f62c7bb28b0ce77b773a611c6ba02b361db1c85/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### ht...@chromium.org (2021-01-20)

Asking submitter to consider the change and see if he agrees that it fixes the issue.
Did not come up with an easy way to provoke an UAF here, so no test written.


### wx...@gmail.com (2021-01-20)

Yes, the copy is good

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### wx...@gmail.com (2021-01-27)

Thanks a lot.But I see that the baseline of high level is 5000.Would you like to tell me the reason?

### am...@google.com (2021-01-28)

Hi, wxhusst@. Rewards for qualifying security bugs typically range from $500 to $150,000. There is no baseline for a high severity bug report. Decisions made the VRP panel are based on the issue impact, report quality, the proof of concept (if provided), and if there is a functional exploit provided. The Panel decided today on a reward of $500 based on this report. If you would like, I am happy to bring it back to the panel for another discussion next week. In the interim, please tell me how you would like to be credited in release notes. 
Additionally a member of our finance team should be reaching out to you shortly to arrange payment. Thank you! 

### wx...@gmail.com (2021-01-28)

Thank you.
credit: raven(@raid_akame)
Can I get cve id?

### am...@google.com (2021-01-28)

Hi, raven! Thank you for your response. CVE number will be updated on this bug when it is assigned. If you track this bug ID, you will be notified of when it is updated with the CVE. 

### wx...@gmail.com (2021-01-28)

ok, thank you

### am...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-10)

It's normal for us to merge high severity security bug fixes to stable. Sheriffbot never asked for merge here because of https://crbug.com/chromium/1186797, so adding a merge request to 89 and immediately approving it. Please merge to M89, branch 4389, and we will release this in the next M89 security refresh.

### gi...@appspot.gserviceaccount.com (2021-03-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5651fb858b754b6bdee525b9a0c7b65616c4f93e

commit 5651fb858b754b6bdee525b9a0c7b65616c4f93e
Author: Harald Alvestrand <hta@chromium.org>
Date: Thu Mar 11 18:54:23 2021

[Merge to M89] Iterate more carefully over DTLS transports at close

Ensure that even if the set of DTLS transports is modified during
callbacks called from close, the process will be well-defined.

(cherry picked from commit 4f62c7bb28b0ce77b773a611c6ba02b361db1c85)

Bug: chromium:1167357
Change-Id: I712280e7382a647027912178156127831b437f75
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2639893
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#845122}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2752880
Reviewed-by: Adrian Taylor <adetaylor@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#1521}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/5651fb858b754b6bdee525b9a0c7b65616c4f93e/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### ad...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### ja...@google.com (2021-03-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-16)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1167357?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054476)*
