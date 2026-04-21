# uaf in FrameSinkVideoCaptureDevice::OnLog

| Field | Value |
|-------|-------|
| **Issue ID** | [40059009](https://issues.chromium.org/issues/40059009) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qi...@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2022-03-08 |
| **Bounty** | $500.00 |

## Description


Steps to reproduce the problem:

https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/frame_sink_video_capture_device.cc;l=297

- in this Mojo function FrameSinkVideoCaptureDevice::OnLog
```c++
void FrameSinkVideoCaptureDevice::OnLog(const std::string& message) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  if (receiver_) {
    if (BrowserThread::CurrentlyOn(BrowserThread::IO)) {
      receiver_->OnLog(message);
    } else {
      GetIOThreadTaskRunner({})->PostTask(
          FROM_HERE,
          base::BindOnce(&media::VideoFrameReceiver::OnLog,
                         base::Unretained(receiver_.get()), message));
    }
  }
}
```

here use the io thread to post task and send the raw_pointer
```base::Unretained(receiver_.get()) ``` and don't have other check.
it may cause race uaf in io thread of the api.


https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/frame_sink_video_capture_device.cc;l=189


```
void FrameSinkVideoCaptureDevice::StopAndDeAllocate() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
[...]
 if (receiver_) {
    receiver_.reset();
    DidStop();
  }
[...]
```

I don't have a poc, just code inspection.


What went wrong?
above all.

Did this work before? N/A 

Chrome version: 99.0.4844.51  Channel: stable
OS Version: 10.0


## Timeline

### dt...@chromium.org (2022-03-08)

Tentatively marking as Bug-Security due to UAF. Over to Internals>Media team to investigate.

[Monorail components: Internals>Media]

### [Deleted User] (2022-03-08)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-03-09)

Assigning high severity based on potential UAF in browser process; severity assessment may be revised following further review. 

Directly assigning to an owner of the FrameSinkVideoCaptureDevice subsystem to make sure the Security label is not preventing visibility from owners. 

@jophba, can you please help validate this bug? Feel free to redirect if you feels someone else is better placed to help. 

@qiaoli010, it is helpful if you can prepare and share a POC to assist with triage. Including a POC is regarded as a positive factor for VRP reward decisions. 

### [Deleted User] (2022-03-09)

[Empty comment from Monorail migration]

### mf...@chromium.org (2022-03-09)

This looks related to WebRTC logging added by ilnik@.

### qi...@gmail.com (2022-03-10)

@bookholt, I will try to construct the POC, but this will take a while and may not be reliable because I am not familiar with MoJo.

### il...@chromium.org (2022-03-10)

[Empty comment from Monorail migration]

### il...@chromium.org (2022-03-10)

I doubt it can actually be employed, since this affected FrameSinkVideoCaptureDevice::OnLog is called only by the |capturer_| which is destroyed prior to destroying the |receiver_|.

However, I'm preparing a CL to remove any possibility of UaF here in the future.

### [Deleted User] (2022-03-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/956d5a2d6a8f84a3c782a70d2a4520d81b261b4a

commit 956d5a2d6a8f84a3c782a70d2a4520d81b261b4a
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Thu Mar 10 22:18:22 2022

Fix potential UaF in FrameSinkVideoCaptureDevice

Bug: 1304075
Change-Id: I684cce65a63a9f8b9af6b71ff196c6799e725a8b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3516113
Reviewed-by: Jordan Bayles <jophba@chromium.org>
Commit-Queue: Jordan Bayles <jophba@chromium.org>
Cr-Commit-Position: refs/heads/main@{#979976}

[modify] https://crrev.com/956d5a2d6a8f84a3c782a70d2a4520d81b261b4a/content/browser/media/capture/frame_sink_video_capture_device.cc


### il...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

Requesting merge to stable M99 because latest trunk commit (979976) appears to be after stable branch point (961656).

Requesting merge to beta M100 because latest trunk commit (979976) appears to be after beta branch point (972766).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

Merge review required: M100 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

Merge review required: M99 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### il...@chromium.org (2022-03-17)

I don't believe this requires merges because, as described in #8.

I'm removing merge requests and decreasing the priority.

### il...@chromium.org (2022-03-17)

Actually, I'm not sure how to proceed with this security bug.

bookholt@, should I just replace Security_Severity-High with Security_Severity-Low?

The uaf is not possible to exploit. It's not happening anywhere. There's no PoC, It was named as such solely by reading the code.

### bo...@google.com (2022-03-17)

Thanks for your help ilnik@. As you say, if the error condition is not in fact reachable upon analysis, then this is not a security bug. Dropping the Security Impact label. 

### bo...@google.com (2022-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-17)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-03-17)

Unsetting more labels to appease SheriffBot

### bo...@chromium.org (2022-03-17)

Undoing unintentional flag changes

### [Deleted User] (2022-03-17)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2022-03-17)

Ugh, sorry for the spam. Changing bug type from Bug-Security to Bug. 

### il...@chromium.org (2022-03-18)

Removing merge requests.

### qi...@gmail.com (2022-03-18)

ilnik@,  One possible trigger I found was to destroy the window while FrameSinkVideoCaptureDevice::OnLog was being executed, which would result in a chain of calls like this ： OnWindowDestroying(aura::Window* window)  -> FrameSinkVideoCaptureDevice::OnTargetPermanentlyLost ->  OnFatalError -> StopAndDeAllocate -> receiver_.reset().   There will be a race.  This is just my shallow analysis, please analyze in depth whether this is possible.

### il...@chromium.org (2022-03-18)

Yes, that is a possible chain of events.  However, on a deeper analysis, it's in the "dead" code.

This OnLog function may be called from a separate thread only by FrameSinkVideoCapturerImpl. There are several call sites like [1] but all them are gated on a log_to_webrtc_ flag. All the other places where OnLog could be called are already on IOThread, so nothing is posted there and there's no race condition.

This flag is plumbed there from here [2]. It essentially comes from the disabled by default kWebRtcLogCapturePipeline feature. That feature is left in code for debugging purposes only.

It has to be enabled manually from the command line to run the affected code.

@bookholt, is it considered a security bug if a permanently disabled feature is required to run the affected code?

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/service/frame_sinks/video_capture/frame_sink_video_capturer_impl.cc;l=515;drc=88989bcd7983c93c8d294e1472160d0718299f62

[2] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/common/features.cc;l=268;drc=88989bcd7983c93c8d294e1472160d0718299f62




### bo...@chromium.org (2022-03-18)

@ilnik, it depends on what you mean by "permanently disabled." If there is a command line flag to re-enable the code then my interpretation of the severity guidelines [1] is yes, it can be a security bug with at most a medium severity due to the requirement for users to put Chrome in a nonstandard state to make themselves vulnerable. Alternatively, if the code is truly unreachable in release builds, but still retained in the codebase so a developer can temporarily patch it back in for local troubleshooting, then that's not a security bug. (Notwithstanding clever linkers that try to prune unused code, I hope keeping truly dead code in the codebase is extremely rare.)

At a glance it looks like it is possible to enable the kWebRtcLogCapturePipeline feature with a command line flag because it's defined as a feature and IIUC all features can be toggled by command line flags. So if the example in https://crbug.com/chromium/1304075#c29 is a valid series of events then it would qualify as a security bug with at most medium severity. I think low severity is reasonable hedge here since we lack a POC to 100% validate reachability. 

@ilnik, before I toggle the security bit again, does all that sounds reasonable? 

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity

### il...@chromium.org (2022-03-18)

I agree with our reasoning. The feature can be enabled from the command line. low severity is fitting here.

### bo...@chromium.org (2022-03-18)

OK, thanks a bunch for your help with analysis. Re-setting security bits. SheriffBot may be back with (hopefully less urgent) merge requests. 

I'm assuming the earliest affected version that's currently shipping is Extended since FrameSinkVideoCaptureDevice::OnLog had that base::unretained pointer for at least a couple years. 

I took a guess at the impacted platforms based on my reading of the BUILD.gn files and related docs [1] that give the impression this code is cross-platform. A quick double check is appreciated. 

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/viz/README.md

### il...@chromium.org (2022-03-21)

Thank you for helping here. Yes, the selected palatforms are correct.

### [Deleted User] (2022-03-21)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-21)

[Empty comment from Monorail migration]

### il...@chromium.org (2022-03-22)

I don't get why the sheriffbot is complaining. The bug clearly has "Security_Severity-Low" and "FoundIn-96" labels. 

 bookholt@, could you take a look?

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Hello! Thank you for this report. Given that there is no demonstrated exploitability of this issue and this issue is behind a debugging flag, the VRP Panel has decided to extend a $500 thank you for this report. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-25)

[Comment Deleted]

### am...@chromium.org (2022-04-26)

[Comment Deleted]

### [Deleted User] (2022-06-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

I think per https://crbug.com/chromium/1304075#c31 this is probably Security_Impact-None.

### is...@google.com (2022-12-13)

This issue was migrated from crbug.com/chromium/1304075?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059009)*
