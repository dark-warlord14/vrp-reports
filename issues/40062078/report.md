# Use-after-poison in content::InspectorMediaEventHandler::SendQueuedMediaEvents

| Field | Value |
|-------|-------|
| **Issue ID** | [40062078](https://issues.chromium.org/issues/40062078) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Core, Internals>Media |
| **Platforms** | Android, Linux, Mac |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $7,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5927302438518784

Fuzzer: jesse_avalanche
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7eaf002350a0
Crash State:
  content::InspectorMediaEventHandler::SendQueuedMediaEvents
  content::BatchingMediaLog::SendQueuedMediaEvents
  base::internal::Invoker<base::internal::BindState<void
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1057935:1057939

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5927302438518784

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-07)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core Internals>Media]

### ad...@google.com (2022-12-07)

Ted, could you take a look here?

ClusterFuzz is sure of two apparently conflicting things:

1) There's a use-after-poison here:
    #0 0x558f8a8510b0 in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::Cr::vector<media::MediaLogRecord, std::Cr::allocator<media::MediaLogRecord>>) content/renderer/media/inspector_media_event_handler.cc:157:25
    #1 0x558f8a858c9e in content::BatchingMediaLog::SendQueuedMediaEvents() content/renderer/media/batching_media_log.cc:236:14

2) The regression bisects to one of these four commits:
https://chromium.googlesource.com/chromium/src/+log/5b8f515d5c26a03287e2caa4438c3f3131ee6e9b..4f0bde3a57840515abcac2def20da2c5a7f7777e?pretty=fuller&n=10000

The most likely fit seems to be enabling picture-in-picture here - https://chromium.googlesource.com/chromium/src/+/4f0bde3a57840515abcac2def20da2c5a7f7777e%5E%21/. But I'm not at all sure. I assume that your InspectorMediaEventHandler is getting deleted at the wrong time. Please take a look.

### [Deleted User] (2022-12-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tm...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-12-07)

Yes, thats exactly what it looks like to me as well. I presume that PIP2 is allowing the player & therefore the media log to outlive the page, which wasn't supposed to ever be the case prior. I've cc'd Frank to see what we should do here, regarding either disabling the experiment while I make a fix, or just trying to rush the fix out and merge it back.

### li...@google.com (2022-12-07)

pip is not enabled by default, so even with no fix this shouldn't affect stable.  CF just turns on experimental web features, which is why any of that code is enabled.

the player in a pip window is not supposed to outlive either the pip window or the window that opened the pip window.  there's a bug in the existing behavior that CF could be running into, which should be fixed by [1], where non-pip same-origin windows (which don't have the handy lifetime guarantee) are reusing media players across frames.  this could cause it.

it's also possible for a player to get moved to the opener when it shouldn't, which might cause this as well (not sure -- might not).  either way, jazzhsu@ is looking into that one after [1].

[1] https://chromium-review.googlesource.com/c/chromium/src/+/4068769


### tm...@chromium.org (2022-12-07)

After talking with Frank, this seems like not a release block, since it's only enabled when PIP is enabled. (ie, this requires --enable-experimental-web-platform-features)

### li...@google.com (2022-12-07)

+cc:tmathmeyer to see the bug again :)

### [Deleted User] (2022-12-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2022-12-14)

re c#12: this really isn't RBS, since it only happens when experimental web features are enabled.  re-removing it, along with more security labels this time.

### [Deleted User] (2022-12-14)

[Empty comment from Monorail migration]

### sr...@google.com (2022-12-14)

i think CF would re-add unless you add Security impact-NA label , 

adding amyressler@ to help with that 

### am...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-14)

Thanks for tagging me, Srinivas. 
Security issues are still security issues even if they in code in features not enabled by default. Adding Security_Impact-None to reflect that and should dissuade the bot from re-adding the RBS label as the only SLO for SI-None bugs is that they are resolved before the feature ships by default. 

### li...@google.com (2022-12-14)

re c#17: ah, thanks for the info.

...for posterity, i guess, because amyressler@ is not receiving updates on this bug :)

### ja...@chromium.org (2022-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-16)

ClusterFuzz testcase 5927302438518784 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1084088:1084095

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-12-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-04)

Congratulations, Jesse! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your efforts towards Chrome fuzzing -- great work! 

### am...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1396730?no_tracker_redirect=1

[Multiple monorail components: Internals>Core, Internals>Media]
[Monorail blocked-on: crbug.com/chromium/1392441]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062078)*
