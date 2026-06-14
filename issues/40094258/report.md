# Security: Security: Chrome renderer process persistence bug on android

| Field | Value |
|-------|-------|
| **Issue ID** | [40094258](https://issues.chromium.org/issues/40094258) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Core |
| **Platforms** | Android |
| **Reporter** | wy...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2019-03-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

#ChildProcessLauncherHelper::GetTerminationInfo# function in child\_process\_launcher\_helper\_android.cc maybe not return "TERMINATION\_STATUS\_STILL\_RUNNING" status.

Then, in #ChildProcessTerminationInfo ChildProcessLauncher::GetChildTerminationInfo#, the #Close# will assign "kNullProcessHandle" to "process\_".  

ChildProcessTerminationInfo ChildProcessLauncher::GetChildTerminationInfo(  

bool known\_dead) {  

//…  

termination\_info\_ = helper\_->GetTerminationInfo(process\_, known\_dead);  

//…  

if (termination\_info\_.status != base::TERMINATION\_STATUS\_STILL\_RUNNING) {  

process\_.process.Exited(termination\_info\_.exit\_code);  

process\_.process.Close(); //process\_ = kNullProcessHandle;

Then, in #ChildProcessLauncher::~ChildProcessLauncher#, the process isn't valid, so it will not execute #ChildProcessLauncherHelper::ForceNormalProcessTerminationAsync# to reap renderer process. So the compromised renderer process can be persistencet even user close the tab.

ChildProcessLauncher::~ChildProcessLauncher() {  

DCHECK\_CALLED\_ON\_VALID\_SEQUENCE(sequence\_checker\_);  

if (process\_.process.IsValid() && terminate\_child\_on\_shutdown\_) {  

// Client has gone away, so just kill the process.  

ChildProcessLauncherHelper::ForceNormalProcessTerminationAsync(  

std::move(process\_));

**VERSION**  

Chrome Version: [72.0.3626.0] + [stable, beta, or dev]  

Operating System: [Android]

**REPRODUCTION CASE**

1. Use the following patch, compile chromium on android.  
   
   void SyncChannel::SyncContext::OnChannelError() {  
   
   CancelPendingSends();  
   
   shutdown\_watcher\_.StopWatching();

- Context::OnChannelError();

- //Context::OnChannelError();  
  
  }

2. Install the apk on android device, open one tab, you will find a new sandboxed process by 'adb shell ps -A | grep org.chromium.chrome'
3. Close the tab, the new sandboxed process should exit, but it is still alive.
4. So, if one renderer process is compromised by "RCE" bug, the process can be persistent for a long time by hook #SyncChannel::SyncContext::OnChannelError#.

## Attachments

- [patch.diff](attachments/patch.diff) (application/octet-stream, 377 B)

## Timeline

### oc...@chromium.org (2019-03-11)

rsesek, could you please take a look? 

I'm not sure I understand the implications of this. It seems to be there are probably other, easier ways to persist a renderer exploit. 

[Monorail components: Internals>Core]

### wy...@gmail.com (2019-03-11)

Some info added:

In #ChildProcessLauncherHelper::GetTerminationInfo# of //src/content/browser/child_process_launcher_helper_android.cc, it returns either "TERMINATION_STATUS_OOM_PROTECTED" or "TERMINATION_STATUS_NORMAL_TERMINATION" status, but never returns "TERMINATION_STATUS_STILL_RUNNING" status.
So, I think it will never execute #ChildProcessLauncherHelper::ForceNormalProcessTerminationAsync# in #ChildProcessLauncher::~ChildProcessLauncher#.

### sh...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### bo...@chromium.org (2019-03-11)

Ahh, android abusing the termination status enum since forever.

I think I'll just make GetTerminationInfo kill the process if it's still running. Seems like the smallest/easiest fix

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37a0e90a956194a066dd31edd5b5ac5045701d31

commit 37a0e90a956194a066dd31edd5b5ac5045701d31
Author: Bo Liu <boliu@chromium.org>
Date: Mon Mar 11 21:11:00 2019

android: Stop child process in GetTerminationInfo

Android currently abuses TerminationStatus to pass whether process is
"oom protected" rather than whether it has died or not. This confuses
cross-platform code about the state process.

Only TERMINATION_STATUS_STILL_RUNNING is treated as still running, which
android never passes. Also it appears to be ok to kill the process in
getTerminationInfo as it's only called when the child process is dead or
dying. Also posix kills the process on some calls.

Bug: 940245
Change-Id: Id165711848c279bbe77ef8a784c8cf0b14051877
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1516284
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: ssid <ssid@chromium.org>
Commit-Queue: Bo <boliu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#639639}
[modify] https://crrev.com/37a0e90a956194a066dd31edd5b5ac5045701d31/content/browser/child_process_launcher_helper_android.cc
[modify] https://crrev.com/37a0e90a956194a066dd31edd5b5ac5045701d31/content/public/android/java/src/org/chromium/content/browser/ChildProcessLauncherHelperImpl.java


### bo...@chromium.org (2019-03-11)

Do we usually merge security fixes? What about for m73?

### rs...@chromium.org (2019-03-11)

I'd probably get this into M74 but it's not high enough severity to warrant M73.

### wy...@gmail.com (2019-03-12)

Quick fix!
And one thing I must let you know.
I will give a talk on BlackHat Asia 2019(March 28-29), and this issue is one of my case. 
So will you fix it as soon as possible? Or if you feel this issue is not so critical, you can do it as your original plan.

Thanks.

### wy...@gmail.com (2019-03-12)

And at first, I thought this was not a security bug, so I didn't file this issue.
But when I start to prepare my slides, I think I should let you know.

### rs...@chromium.org (2019-03-12)

This bug would qualify likely qualify for a reward under our program (https://www.google.com/about/appsecurity/chrome-rewards/index.html), but the fix will not be generally available by that March date, since it is 2 weeks away. If you were to disclose details of the bug prior to the fix being released to users, then it would be disqualified from the reward program.

Setting to Fixed so Clusterfuzz can handle the merge labels.

### sh...@chromium.org (2019-03-12)

[Empty comment from Monorail migration]

### wy...@gmail.com (2019-03-13)

OK, got it.
So, I will delete the details of this issue from my slides.
And I think I should file the issue as soon as possible, even though it's not so critical.

### rs...@chromium.org (2019-03-13)

Note to panel: this is a little more severe than on desktop because there are a finite number of processes declared in manifest, meaning that it'd be pretty easy for an attacker to get into every renderer process.

### bo...@chromium.org (2019-03-15)

Do I need to manually apply the merge labels? Probably been in trunk long enough to merge.

### aw...@google.com (2019-03-15)

Raising severity to Medium per https://crbug.com/chromium/940245#c14, and requesting merge to 74

### sh...@chromium.org (2019-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-16)

Your change meets the bar and is auto-approved for M74. Please go ahead and merge the CL to branch 3729 (refs/branch-heads/3729) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@appspot.gserviceaccount.com (2019-03-16)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/f3e42fe982a09c8bd8cd470e032b280c4830acae

Commit: f3e42fe982a09c8bd8cd470e032b280c4830acae
Author: boliu@chromium.org
Commiter: boliu@chromium.org
Date: 2019-03-16 19:26:16 +0000 UTC

[Merge M74] android: Stop child process in GetTerminationInfo

Android currently abuses TerminationStatus to pass whether process is
"oom protected" rather than whether it has died or not. This confuses
cross-platform code about the state process.

Only TERMINATION_STATUS_STILL_RUNNING is treated as still running, which
android never passes. Also it appears to be ok to kill the process in
getTerminationInfo as it's only called when the child process is dead or
dying. Also posix kills the process on some calls.

(cherry picked from commit 37a0e90a956194a066dd31edd5b5ac5045701d31)

Bug: 940245
Change-Id: Id165711848c279bbe77ef8a784c8cf0b14051877
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1516284
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: ssid <ssid@chromium.org>
Commit-Queue: Bo <boliu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#639639}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1526756
Reviewed-by: Bo <boliu@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#181}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### na...@google.com (2019-03-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-20)

Congrats the Panel decided to reward $1,000 for this report! 

### wy...@gmail.com (2019-03-21)

ok, and when will be a cve number assigned?

### aw...@google.com (2019-03-21)

Once M74 goes to stable. Thanks!

### aw...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/940245?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094258)*
