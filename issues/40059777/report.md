# AddressSanitizer: heap-buffer-overflow in content::BucketManagerHost::DidGetBucket content/browser/b

| Field | Value |
|-------|-------|
| **Issue ID** | [40059777](https://issues.chromium.org/issues/40059777) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Storage>Buckets |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2022-05-27 |
| **Bounty** | $21,000.00 |

## Description

**Steps to reproduce the problem:**  

#Reproduce  

The problem was found by my fuzzer running on CF(CC Security team for access permission <https://clusterfuzz.com/testcase-detail/4878675220824064>),  

But it cannot be reproduced stably, CF may not automatically report.  

After manual analysis, the root cause of the vulnerability is clearly understood.

Type of crash  

Render process

**Problem Description:**  

#Analysis  

Introduced by this CL <https://chromium-review.googlesource.com/c/chromium/src/+/3627155>

1. Not checking if the iterator is valid AT[1] causes the issue

```
//https://source.chromium.org/chromium/chromium/src/+/main:content/browser/buckets/bucket_manager_host.cc;drc=51652535d059deac93e39df925023a4d8933f84e;l=179  
void BucketManagerHost::DidGetBucket(  
    mojo::ReceiverId receiver_id,  
    OpenBucketCallback callback,  
    storage::QuotaErrorOr<storage::BucketInfo> result) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  
  if (!result.ok()) {  
    // Getting a bucket can fail if there is a database error.  
    std::move(callback).Run(mojo::NullRemote());  
    return;  
  }  
  
  const auto& bucket = result.value();  
  auto it = bucket_map_.find(bucket.name);  
  if (it == bucket_map_.end()) {  
    it = bucket_map_  
             .emplace(bucket.name, std::make_unique<BucketHost>(this, bucket))  
             .first;  
  }  
  
  auto permission_it = permission_decider_map_.find(receiver_id);  
  auto pending_remote =														<<[1]  
      it->second->CreateStorageBucketBinding(permission_it->second);  
  std::move(callback).Run(std::move(pending_remote));  
}  
  

```

#PATCH

```
diff --git a/content/browser/buckets/bucket_manager_host.cc b/content/browser/buckets/bucket_manager_host.cc  
index c416115..0be5f2a 100644  
--- a/content/browser/buckets/bucket_manager_host.cc  
+++ b/content/browser/buckets/bucket_manager_host.cc  
@@ -176,6 +176,9 @@  
   }  
   
   auto permission_it = permission_decider_map_.find(receiver_id);  
+  if (permission_it == permission_decider_map_.end()) {  
+    return;  
+  }  
   auto pending_remote =  
       it->second->CreateStorageBucketBinding(permission_it->second);  
   std::move(callback).Run(std::move(pending_remote));  
  

```

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 12.4 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 565 B)

## Timeline

### m....@gmail.com (2022-05-27)

My initial description is incorrect, it may not be the crash of the renderer but the crash of the browser.

### dt...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>Buckets]

### [Deleted User] (2022-05-27)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-05-31)

Thanks for the report and the manual analysis (and suggested patch!), even if the test case itself is flaky. This seems like a good defensive improvement to the code, although it's slightly difficult to triage without knowing how it is getting triggered. That said, to do some initial triage:

* From a search of blink-dev@, it looks like the Storage Buckets API is at the Intent to Prototype stage, so does not yet have real world impact (the fuzzer sets the --enable-experimental-web-platform-features flag), so this as Security_Impact-None for now. If this starts to ship to OT or further, then this would impact real users and the Impacts label would need to be updated, but I think we can fix it before it ships which is a good thing :-)
* This is a browser-process crash that appears to be reachable from web content, which means this is Severity-Critical.
* Per https://storage.googleapis.com/chromium-find-releases-static/516.html#51652535d059deac93e39df925023a4d8933f84e this landed in M-104.
* This is plausibly reachable on all Blink platforms, so marking all Blink OSes.
* Because this is an Impact-None Severity-Critical, I'm marking this as only P-1 (rather than P-0). We'll see if sheriffbot yells about that -- if so I think it is reasonable to bump this back down but block enabling this for any users until this bug is fixed.

Assigning to estade@: could you please take a look at this report and the suggested fix? Also cc'ing other storage buckets owners for visibility.

### es...@chromium.org (2022-05-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f3b1ea95d838d2fabd93693bfb3c7e40b1b6c2d

commit 9f3b1ea95d838d2fabd93693bfb3c7e40b1b6c2d
Author: Evan Stade <estade@chromium.org>
Date: Wed Jun 01 02:13:00 2022

Storage buckets: avoid crash when page disconnects while opening bucket

Bug: 1329875
Change-Id: I3a6f0880997edfb4b65930c320b67faf21bfbe7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3681624
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1009413}

[modify] https://crrev.com/9f3b1ea95d838d2fabd93693bfb3c7e40b1b6c2d/content/browser/buckets/bucket_manager_host.cc


### ct...@chromium.org (2022-06-02)

Following up here: Is the CL in https://crbug.com/chromium/1329875#c6 a complete fix? (Checking whether we can mark this as Fixed.)

### es...@chromium.org (2022-06-05)

It should be, yes, although I haven't confirmed directly.

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you $20,000 for this report + $1,000 fuzzer bonus. Thank you for your efforts in this discovery and great work! 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-09-12)

This issue was migrated from crbug.com/chromium/1329875?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059777)*
