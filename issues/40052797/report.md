# Security: HeapOverflow in BackgroundFetch

| Field | Value |
|-------|-------|
| **Issue ID** | [40052797](https://issues.chromium.org/issues/40052797) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2020-07-08 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

When making a search to |completed\_fetches\_|, there is no check whether the query result is |end()|[1]. And the fetch-item could also be erased at [2]. So the race makes the HeapOverflow happen. (Asan may throw it out as UAF）

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/background_fetch/background_fetch_scheduler.cc;l=241;drc=41ccef450c3600b0744f504f020cf35182c166bc;bpv=0;bpt=0?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:content/browser/background_fetch/background_fetch_scheduler.cc;l=309;drc=5ba77dad98cf94506cf3700f9e12fcdc65fadfb6;bpv=0?originalUrl=https:%2F%2Fcs.chromium.org%2F>

**VERSION**  

Chrome Version: stable  

Operating System: All

**REPRODUCTION CASE**

1.$python -m SimpleHTTPServer&  

$./out/Asan/chrome --user-data-dir="/tmp/xxxx" <http://localhost:8000/index.html>  

2.click "Trigger The Bug" button and click the downloading item frequently until it is aborted

(also see the attached video)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser  

Crash State: asan file

**CREDIT INFORMATION**

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab working with 360 BugCloud(<https://bugcloud.360.cn/>)

## Attachments

- [index.html](attachments/index.html) (text/plain, 700 B)
- [sw.js](attachments/sw.js) (text/plain, 411 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.9 MB)
- [asan](attachments/asan) (text/plain, 29.2 KB)
- [M83_Asan](attachments/M83_Asan) (text/plain, 10.8 KB)
- [index.html](attachments/index_53043505.html) (text/plain, 709 B)
- [sw.js](attachments/sw_53043506.js) (text/plain, 597 B)
- [demo2.mp4](attachments/demo2.mp4) (video/mp4, 1.4 MB)

## Timeline

### cl...@chromium.org (2020-07-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5633242662764544.

### mm...@chromium.org (2020-07-09)

Leecraso, thanks for the report. I'm having trouble reproducing it (tried both Linux and Windows), with e.g. this build https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-756066.zip, which corresponds to the current Stable version: https://chromium.googlesource.com/chromium/src/+/8f0c18b4dca9b6699eb629be0f51810c24fb6428

Could you please share a particular revision of Chromium you've used to reproduce this?

### mm...@chromium.org (2020-07-09)

rayankans@, could you please take a look at the stacktrace ("asan" file attached in c#0)?

We're still trying to figure out how to reproduce this and how severe the issue is, but it may turn out to be a Critical severity issue therefore taking a look at the code ASAP wouldn't hurt.

Thank you!

### le...@gmail.com (2020-07-09)

It may require frequent clicks on the downloading item. I successfully reproduced it on the M83_release version provided in https://crbug.com/chromium/1103195#c2, and the stacktrace in here.

### le...@gmail.com (2020-07-09)

It seems that the release version is indeed more difficult to trigger than the debug version. You can try this new poc, it's easier to trigger on the release version for me.

### ra...@chromium.org (2020-07-09)

I'm struggling to reproduce this, but inspecting the code there seems to be a window where this could potentially happen in between the the background fetch being aborted and the click event being dispatched.

### ra...@chromium.org (2020-07-09)

Fix here: https://chromium-review.googlesource.com/c/chromium/src/+/2289428

### ad...@google.com (2020-07-09)

As this now has a fix in progress, I'm going to set all the appropriate labels despite the fact we haven't definitively reproduced this yet. I will also give it a try this morning.

[Monorail components: Blink>BackgroundFetch]

### ad...@google.com (2020-07-09)

I also can't reproduce this on the build in https://crbug.com/chromium/1103195#c2 even with the new poc in https://crbug.com/chromium/1103195#c5. leecraso@ are you happy to test a fixed buiid? If so rayankans@ - could you point out where they can find a build?

### le...@gmail.com (2020-07-09)

Thanks for the quick fix. Unfortunately, it seems not completely fix this bug. I can still trigger it not by calling |Abort()| but by a normal download completion. In addition to |Abort()|, there will be other situations that lead to conditional competition, such as normal download finish. They will also call |DidMarkForDeletion()|. And as long as the registration has been removed from completed_fetches_, the heap-buffer-overflow will also be triggered.

### le...@gmail.com (2020-07-09)

adetaylor@ Thanks for your reproduce trying. It may require quick clicks and multiple attempts because the time window on the release version is much smaller than the debug version. Of course, you also could try to reproduce it on the debug version first.

### le...@gmail.com (2020-07-09)

This is my test with the poc in https://crbug.com/chromium/1103195#c5 on the build in https://crbug.com/chromium/1103195#c2. Try to quickly click and adjust the time of setTimeout() may help.

### ra...@chromium.org (2020-07-09)

Thanks for the quick response leecraso@. You're right, I was focused on the abort flow. I uploaded a new patchset to the CL that should handle all cases.

### mm...@chromium.org (2020-07-09)

Adrian, which milestone we should add to this?

### le...@gmail.com (2020-07-09)

The fix still seems to have some problems. Race condition will result in that: the registration not being removed from completed_fetches_ in time, but at this time it has been released from job_controllers_. So it will cause a null pointer reference. I printed a little log, hope it helps you.

```
void BackgroundFetchScheduler::DidMarkForDeletion(

	...

  if (error != BackgroundFetchError::NONE)
    return;

  auto it = completed_fetches_.find(registration_id.unique_id());
  //DCHECK(it != completed_fetches_.end());
  DLOG(INFO)<<"--->>> it == completed_fetches_.end()? : "<<(it == completed_fetches_.end());
  DLOG(INFO)<<"--->>> job_controllers_.find(registration_id.unique_id()) == job_controllers_.end()? : "<<(job_controllers_.find(registration_id.unique_id()) == job_controllers_.end());

  blink::mojom::BackgroundFetchRegistrationDataPtr& registration_data =
      it->second->registration;
  // Include any other failure reasons the marking for deletion may have found.
  if (registration_data->failure_reason == BackgroundFetchFailureReason::NONE)
    registration_data->failure_reason = failure_reason;
    ...
```


[30310:30310:0710/015854.119285:INFO:background_fetch_scheduler.cc(250)] --->>> it == completed_fetches_.end()? : 0
[30310:30310:0710/015854.119370:INFO:background_fetch_scheduler.cc(251)] --->>> job_controllers_.find(registration_id.unique_id()) == job_controllers_.end()? : 1
[30310:30310:0710/015854.119443:FATAL:struct_ptr.h(77)] Check failed: ptr_.    ************** it->second->registration crashed
#0 0x5566178d46fb (/home/leecraso/Desktop/Chromium_bk/src/out/x64_ipctest/chrome+0x7ea26fa)
#1 0x7f9cbccdcd0f (/home/leecraso/Desktop/Chromium_bk/src/out/x64_ipctest/libbase.so+0xc30d0e)
#2 0x7f9cbc606ecb (/home/leecraso/Desktop/Chromium_bk/src/out/x64_ipctest/libbase.so+0x55aeca)

### ad...@chromium.org (2020-07-09)

I'll add M-84 since that's imminent.

### go...@google.com (2020-07-09)

[Empty comment from Monorail migration]

### le...@gmail.com (2020-07-10)

I am sorry that my analysis in https://crbug.com/chromium/1103195#c15 is wrong, may late night destroyed my mind. The true reason for the null pointer reference may be that: Race condition causes |DispatchClickEvent()| to be called between |FinishJob()| and |DidMarkForDeletion()|. So |it->second->registration| was moved to event_dispatcher_[1] before it was used in |DidMarkForDeletion()|, and was released after the scope of |ServiceWorkerProxy::DispatchBackgroundFetchClickEvent()|. Here are some logs[2]:

[1].
```
void BackgroundFetchScheduler::DispatchClickEvent(
    const std::string& unique_id) {
    ...
auto it = completed_fetches_.find(unique_id);
  if (it == completed_fetches_.end())
    return;

  event_dispatcher_.DispatchBackgroundFetchClickEvent(
      it->second->registration_id, std::move(it->second->registration),   //<<<---------------  it->second->registration is moved into DispatchBackgroundFetchClickEvent
      base::DoNothing());

  if (it->second->processing_completed)
    ...
}
```

[2].
[10098:10098:0710/105713.842261:INFO:background_fetch_scheduler.cc(199)] --->>> Into BackgroundFetchScheduler::FinishJob
[10098:10098:0710/105713.842495:INFO:background_fetch.mojom.cc(108)] --->>> BackgroundFetchRegistrationData::BackgroundFetchRegistrationData 0x60600049e3e0
[10098:10098:0710/105713.842612:INFO:background_fetch_scheduler.cc(220)] --->>> NewRegistrationData: 0x60600049e3e0
[10098:10098:0710/105713.889615:INFO:background_fetch_scheduler.cc(308)] --->>> Into BackgroundFetchScheduler::DispatchClickEvent
[10098:10098:0710/105713.896734:INFO:service_worker.mojom.cc(2764)] --->>> ServiceWorkerProxy::DispatchBackgroundFetchClickEvent DONE
[10098:10098:0710/105713.896827:INFO:background_fetch.mojom.cc(112)] --->>> BackgroundFetchRegistrationData::~BackgroundFetchRegistrationData 0x60600049e3e0
[10098:10098:0710/105713.899522:INFO:background_fetch_scheduler.cc(240)] --->>> Into BackgroundFetchScheduler::DidMarkForDeletion
[10098:10098:0710/105713.899605:INFO:background_fetch_scheduler.cc(253)] --->>> it == completed_fetches_.end()? : 0
[10098:10098:0710/105713.899717:FATAL:struct_ptr.h(77)] Check failed: ptr_. 
#0 0x55cdb554e6fb (/home/leecraso/Desktop/Chromium_bk/src/out/x64_ipctest/chrome+0x7ea26fa)
#1 0x7f7f251f9d0f (/home/leecraso/Desktop/Chromium_bk/src/out/x64_ipctest/libbase.so+0xc30d0e)
#2 0x7f7f24b23ecb (/home/leecraso/Desktop/Chromium_bk/src/out/x64_ipctest/libbase.so+0x55aeca)


### ra...@chromium.org (2020-07-10)

You are right, nice catch! I think this is good to go now. Do you mind giving it another shot leecraso@?

### le...@gmail.com (2020-07-10)

It looks good, thanks for your patience to fix. Things seem to be resolved, there are no additional bug triggers for my tests.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6de0038b1125619e64315006b2b92872a83e8915

commit 6de0038b1125619e64315006b2b92872a83e8915
Author: Rayan Kanso <rayankans@google.com>
Date: Fri Jul 10 13:42:57 2020

[BackgroundFetch] Handle race condition between click & completion event.

Bug: 1103195
Change-Id: Ic7fca228e9aff2172fc59c16c01c7edc06003f51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2289428
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/master@{#787185}

[modify] https://crrev.com/6de0038b1125619e64315006b2b92872a83e8915/content/browser/background_fetch/background_fetch_scheduler.cc
[modify] https://crrev.com/6de0038b1125619e64315006b2b92872a83e8915/content/browser/background_fetch/background_fetch_scheduler.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c8ed2292ac7a57f2edf2f424ea92e0fdc0c0cfc4

commit c8ed2292ac7a57f2edf2f424ea92e0fdc0c0cfc4
Author: Rayan Kanso <rayankans@google.com>
Date: Fri Jul 10 14:22:10 2020

[BackgroundFetch] Handle race condition between click & completion event.

(cherry picked from commit 6de0038b1125619e64315006b2b92872a83e8915)

Bug: 1103195
Change-Id: Ic7fca228e9aff2172fc59c16c01c7edc06003f51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2289428
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#787185}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2292203
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4198@{#3}
Cr-Branched-From: 0634566b995c7b772c59e359814013128f143907-refs/heads/master@{#787021}

[modify] https://crrev.com/c8ed2292ac7a57f2edf2f424ea92e0fdc0c0cfc4/content/browser/background_fetch/background_fetch_scheduler.cc
[modify] https://crrev.com/c8ed2292ac7a57f2edf2f424ea92e0fdc0c0cfc4/content/browser/background_fetch/background_fetch_scheduler.h


### go...@google.com (2020-07-10)

Merged CL listed at #21 to current canary branch #4198 and triggered new canary #86.0.4198.2 for Android and Desktop.

### ad...@chromium.org (2020-07-10)

I'm approving merge of this critical bug fix to M84 (branch 4147) and M85 (branch 4183).

govind@, given the need to qualify M84 stable RC today, presumably you'd like this to be merged to M84 today? Or would you prefer to wait for some canary time?

(I am OOO for the rest of the day, hence pre-approving these)

### go...@google.com (2020-07-10)

Yeah, OK to merge to M84 &M85 after verifying in canary if change is safe to merge. Thank you. 

### ad...@chromium.org (2020-07-10)

OK. rayankans@ is in the UK timezone so you may wish to discuss exact timings today? It's already mid Friday afternoon :)

### go...@chromium.org (2020-07-10)

Sorry, on phone at Dentist appointment. Canary should be available in ~3 hrs. Provided build location in internal mail thread for early testing before it gets released.

### go...@chromium.org (2020-07-10)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-07-10)

[Empty comment from Monorail migration]

### go...@google.com (2020-07-10)

Canary is available now, please verify the fix and then merge to M84.

Also requesting to keep an eye on canary data and let us know if you see any stability or any other issues.

### go...@google.com (2020-07-10)

+awhalley@ as adetaylor@ is OOO and we need to get this verified on Canary  and merge to M84  ASAP. Thank you.

### [Deleted User] (2020-07-10)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@google.com (2020-07-10)

Looks like awhalley@ is OOO too. 

### go...@google.com (2020-07-10)

M84 merge is in CQ as we need to cut RC soon: https://chromium-review.googlesource.com/c/chromium/src/+/2292862.

rayankans@, please verify it on canary version 86.0.4198.2+ to make sure fix works and safe. If any issue, please let us know ASAP so we can revert M84 merge. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f80d83fa4b4fb5dbf2e2cab9a2b2ff331358a4bd

commit f80d83fa4b4fb5dbf2e2cab9a2b2ff331358a4bd
Author: Rayan Kanso <rayankans@google.com>
Date: Fri Jul 10 21:34:37 2020

[BackgroundFetch] Handle race condition between click & completion event.

(cherry picked from commit 6de0038b1125619e64315006b2b92872a83e8915)
TBR=rayankans@chromium.org

Bug: 1103195
Change-Id: Ic7fca228e9aff2172fc59c16c01c7edc06003f51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2289428
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#787185}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2292862
Reviewed-by: Ben Mason <benmason@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Ben Mason <benmason@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#851}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/f80d83fa4b4fb5dbf2e2cab9a2b2ff331358a4bd/content/browser/background_fetch/background_fetch_scheduler.cc
[modify] https://crrev.com/f80d83fa4b4fb5dbf2e2cab9a2b2ff331358a4bd/content/browser/background_fetch/background_fetch_scheduler.h


### jo...@chromium.org (2020-07-11)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-07-11)

Hi folks, any chance we can merge this to 83 as well? Chrome OS' stable release is planned for the week after next, which means this bug will be live on Chrome OS for an extra week unless we merge to 83 and do an extra M83 release.

(More details of this extra release at go/cros-patch-gap-process)

### ad...@google.com (2020-07-11)

Rayan, thanks for the swift action. Please mark this as Fixed assuming you're confident that this is a complete fix.

Once this is all resolved we should set about trying to make a MojoLPM fuzzer for these mojo interfaces. We should raise a separate crbug for that.

Jorge, for https://crbug.com/chromium/1103195#c37, I think you should directly contact the M83 branch owners (https://chromiumdash.appspot.com/schedule) by e-mail to check it's OK with them for you to merge. It's fine with me.

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### go...@google.com (2020-07-13)

M85 merge in CQ: https://chromium-review.googlesource.com/c/chromium/src/+/2295204

### [Deleted User] (2020-07-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/00c1eb8b72c748e3f3bde0d2067bb562d66bca39

commit 00c1eb8b72c748e3f3bde0d2067bb562d66bca39
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Jul 13 16:15:49 2020

[BackgroundFetch] Handle race condition between click & completion event.

(cherry picked from commit 6de0038b1125619e64315006b2b92872a83e8915)
TBR=rayankans@chromium.org

Bug: 1103195
Change-Id: Ic7fca228e9aff2172fc59c16c01c7edc06003f51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2289428
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#787185}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2295204
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4183@{#465}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/00c1eb8b72c748e3f3bde0d2067bb562d66bca39/content/browser/background_fetch/background_fetch_scheduler.cc
[modify] https://crrev.com/00c1eb8b72c748e3f3bde0d2067bb562d66bca39/content/browser/background_fetch/background_fetch_scheduler.h


### na...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ma...@google.com (2020-07-13)

M83 merge approved , discussed with govind@

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d5fab13a8528403ef1068fcdb7b8ad4f85edfabc

commit d5fab13a8528403ef1068fcdb7b8ad4f85edfabc
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Jul 13 17:58:45 2020

[BackgroundFetch] Handle race condition between click & completion event.

(cherry picked from commit 6de0038b1125619e64315006b2b92872a83e8915)
TBR=rayankans@chromium.org

Bug: 1103195
Change-Id: Ic7fca228e9aff2172fc59c16c01c7edc06003f51
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2289428
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#787185}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2295040
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Jorge Lucangeli Obes <jorgelo@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#742}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/d5fab13a8528403ef1068fcdb7b8ad4f85edfabc/content/browser/background_fetch/background_fetch_scheduler.cc
[modify] https://crrev.com/d5fab13a8528403ef1068fcdb7b8ad4f85edfabc/content/browser/background_fetch/background_fetch_scheduler.h


### go...@google.com (2020-07-13)

[Comment Deleted]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-13)

[Empty comment from Monorail migration]

### na...@google.com (2020-07-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-07-16)

Congrats! The Panel decided to award $15,000 for this report!

### na...@google.com (2020-07-16)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-07-21)

rayankans@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1103195?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052797)*
