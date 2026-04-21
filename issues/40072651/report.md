# Security: UAF in base::win::MessageWindow::WindowProc

| Field | Value |
|-------|-------|
| **Issue ID** | [40072651](https://issues.chromium.org/issues/40072651) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>PlatformIntegration |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2023-09-18 |
| **Bounty** | $3,000.00 |

## Description

ULNERABILITY DETAILS

VERSION
chrome commit run by fuzzer:
NOTE THAT IT'S NOT A GIT COMMIT FOR BISECTION.

```
commit 2adab79f1d8206aba4469ea8b8dbd6aa0a4d9a3c (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sun Sep 17 11:12:04 2023 +0000

    Roll Chrome Mac Arm PGO Profile

    Roll Chrome Mac Arm PGO profile from chrome-mac-arm-main-1694937576-9469f3572aba2c979e475f057ccd33f0de01c2bc.profdata to chrome-mac-arm-main-1694944042-cb6db46829c90d937c2bc5acbf151548df45f172.profdata

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pgo-mac-arm-chromium
    Please CC chrome-brapp-engprod@google.com,pgo-profile-sheriffs@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Chromium main branch: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chrome.try:mac-chrome
    Tbr: pgo-profile-sheriffs@google.com
    Change-Id: I101e2c3e1d5c542ddd0cf9c702b324558b8dd813
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4870699
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1197616}
```

Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide a minimized poc at this time. However, I have provided the ASAN log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log

## BISECTION

https://crrev.com/c2729d382cc03cdfbe18d0f2694314813ef044b0

```
Use a map instead of SetWindowLongPtr(hwnd, GWLP_USERDATA, ...)

This is used so early in startup that feature flags cannot be used to killswitch this change in case something happens. 
I will monitor for crashes or unwanted behavior and revert quickly if needed.

Bug: 1480135

Change-Id: I15fc3fb2a197364d691a83c4e90f094d6093e6ff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4847130
Reviewed-by: Greg Thompson <grt@chromium.org>
Auto-Submit: Kristian Monsen <kristianm@chromium.org>
Commit-Queue: Kristian Monsen <kristianm@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1196700}
```

## Partial Root Cause Analysis

The RCA is not very clear from asan log.

When creating a new MessageWindow, Thread26(T26) will insert a tuple (hwnd, ref(MessageWindow)) to global singleton called `MessageWindowMap`[1].
And when this MessageWindow is about to be deconstructed, T26 will erase the registed hwnd from MessageWindowMap structure.

The stack traceback at the use point is almost identical to that at the free point, 
except for the USER32.dll library function that is called at the time of deconstructing the MessageWindow. 

I guess the free point and the use point should be triggered sequentially by 
different callbacks executed by the library function when the MessageWindow is deconstructed.

Confusingly, the use point is at [3], which is a Get operation on MessageWindowMap. 

What we can tell from the shadow memory is that the size of the object being UAF'd is 48 bytes (6x8byte) 
and that the asan crash was triggered while trying to read [32, 40) byte.

I guess the UAF'd object is a node object of map, which is a RB-tree node, but there is no conclusive proof and deeper analysis is still needed.

```cpp
// static
LRESULT CALLBACK MessageWindow::WindowProc(HWND hwnd,
                                           UINT message,
                                           WPARAM wparam,
                                           LPARAM lparam) {
  auto& message_window_map = MessageWindowMap::GetInstance();
  MessageWindow* self = message_window_map.Get(hwnd); // <------------------- [3]
  switch (message) {
    // Set up the self before handling WM_CREATE.
    case WM_CREATE: {        
      CREATESTRUCT* cs = reinterpret_cast<CREATESTRUCT*>(lparam);
      self = reinterpret_cast<MessageWindow*>(cs->lpCreateParams);
      // Make |hwnd| available to the message handler. At this point the control
      // hasn't returned from CreateWindow() yet.
      self->window_ = hwnd;
      // Store pointer to self to local map.
      message_window_map.Insert(hwnd, *self); // <------------------- [1]
      break;
    }
    // Clear the map key to stop calling the self once WM_DESTROY is
    // received.
    case WM_DESTROY: {
      message_window_map.Erase(hwnd); // <------------------- [2]
      break;
    }
  }
  // Handle the message.
  if (self) {
    LRESULT message_result;
    if (self->message_callback_.Run(message, wparam, lparam, &message_result))
      return message_result;
  }
  return DefWindowProc(hwnd, message, wparam, lparam);
}
```

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 19.1 KB)
- [EXECUTION_LOG.txt](attachments/EXECUTION_LOG.txt) (text/plain, 104.8 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 4.6 KB)

## Timeline

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-09-18)

VULNERABILITY DETAILS

VERSION
chrome commit run by fuzzer:
NOTE THAT IT'S NOT A GIT COMMIT FOR BISECTION.

```
commit 2adab79f1d8206aba4469ea8b8dbd6aa0a4d9a3c (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Sun Sep 17 11:12:04 2023 +0000

    Roll Chrome Mac Arm PGO Profile

    Roll Chrome Mac Arm PGO profile from chrome-mac-arm-main-1694937576-9469f3572aba2c979e475f057ccd33f0de01c2bc.profdata to chrome-mac-arm-main-1694944042-cb6db46829c90d937c2bc5acbf151548df45f172.profdata

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pgo-mac-arm-chromium
    Please CC chrome-brapp-engprod@google.com,pgo-profile-sheriffs@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Chromium main branch: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chrome.try:mac-chrome
    Tbr: pgo-profile-sheriffs@google.com
    Change-Id: I101e2c3e1d5c542ddd0cf9c702b324558b8dd813
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4870699
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1197616}
```

Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction. 
I am unable to provide a minimized poc at this time. However, I have provided the ASAN log to assist with the vulnerability fix.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan log


### ki...@gmail.com (2023-09-18)

## BISECTION

https://crrev.com/c2729d382cc03cdfbe18d0f2694314813ef044b0

```
Use a map instead of SetWindowLongPtr(hwnd, GWLP_USERDATA, ...)

This is used so early in startup that feature flags cannot be used to killswitch this change in case something happens. 
I will monitor for crashes or unwanted behavior and revert quickly if needed.

Bug: 1480135

Change-Id: I15fc3fb2a197364d691a83c4e90f094d6093e6ff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4847130
Reviewed-by: Greg Thompson <grt@chromium.org>
Auto-Submit: Kristian Monsen <kristianm@chromium.org>
Commit-Queue: Kristian Monsen <kristianm@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1196700}
```

## Partial Root Cause Analysis

The RCA is not very clear from asan log.

When creating a new MessageWindow, Thread26(T26) will insert a tuple (hwnd, ref(MessageWindow)) to global singleton called `MessageWindowMap`[1].
And when this MessageWindow is about to be deconstructed, T26 will erase the registed hwnd from MessageWindowMap structure.

The stack traceback at the use point is almost identical to that at the free point, 
except for the USER32.dll library function that is called at the time of deconstructing the MessageWindow. 

I guess the free point and the use point should be triggered sequentially by 
different callbacks executed by the library function when the MessageWindow is deconstructed.

Confusingly, the use point is at [3], which is a Get operation on MessageWindowMap. 

What we can tell from the shadow memory is that the size of the object being UAF'd is 48 bytes (6x8byte) 
and that the asan crash was triggered while trying to read [32, 40) byte.

I guess the UAF'd object is a node object of map, which is a RB-tree node, but there is no conclusive proof and deeper analysis is still needed.

```cpp
// static
LRESULT CALLBACK MessageWindow::WindowProc(HWND hwnd,
                                           UINT message,
                                           WPARAM wparam,
                                           LPARAM lparam) {
  auto& message_window_map = MessageWindowMap::GetInstance();
  MessageWindow* self = message_window_map.Get(hwnd); // <------------------- [3]
  switch (message) {
    // Set up the self before handling WM_CREATE.
    case WM_CREATE: {        
      CREATESTRUCT* cs = reinterpret_cast<CREATESTRUCT*>(lparam);
      self = reinterpret_cast<MessageWindow*>(cs->lpCreateParams);
      // Make |hwnd| available to the message handler. At this point the control
      // hasn't returned from CreateWindow() yet.
      self->window_ = hwnd;
      // Store pointer to self to local map.
      message_window_map.Insert(hwnd, *self); // <------------------- [1]
      break;
    }
    // Clear the map key to stop calling the self once WM_DESTROY is
    // received.
    case WM_DESTROY: {
      message_window_map.Erase(hwnd); // <------------------- [2]
      break;
    }
  }
  // Handle the message.
  if (self) {
    LRESULT message_result;
    if (self->message_callback_.Run(message, wparam, lparam, &message_result))
      return message_result;
  }
  return DefWindowProc(hwnd, message, wparam, lparam);
}
```

### nh...@google.com (2023-09-18)

Tentatively setting FoundIn based on the revision found in https://crbug.com/chromium/1483939#c3 and severity high.

Kristianm or Wfh, can one of you look into this?

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### kr...@chromium.org (2023-09-18)

[Empty comment from Monorail migration]

### kr...@chromium.org (2023-09-18)

Hey kipreyxx@gmail.com, can you reproduce this at all? I have tried to build with ASAN but not seeing a UAF.

If you can reproduce can you try to see if the free and later get (with UAF) have the same HWND, and if so if get on the map returns nullptr or the previous pointer?

### ki...@gmail.com (2023-09-19)

Hi kristianm. Guessing from previous analysis this vulnerability should be a race condition issue. This vulnerability is extremely difficult to reproduce, we have applied a patch based on https://crbug.com/chromium/1483939#c7 and are working very hard to try to reproduce it, will keep you updated on any progress.

I read the commit that introduced this vulnerability, and since it's a recently introduced code improvement with no major changes, if you also can not find the cause, reverting it might be a good fix so far.

Sincerely appreciate your fix.

### [Deleted User] (2023-09-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2023-09-19)

Can you point me to the command line that you used to run this? Was it a Chrome binary you compiled yourself? Does it have any changes?

I can't really see how this can happen as all the access is from the same thread.

### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2023-09-19)

[Description Changed]

### dr...@chromium.org (2023-09-19)

[Description Changed]

### ki...@gmail.com (2023-09-20)

Re https://crbug.com/chromium/1483939#c11

I've uploaded two attachments EXECUTION_LOG.txt and patch.diff, which are the output messages from chromium when the crash was triggered, and the patch that was applied to the git commit under fuzzing.

Also, the full (very long) parameters for executing chromium are located in the first line of EXECUTION_LOG.txt.

While I did a little patch on the chromium under fuzzing, I don't think those patches affect the logic where the vulnerabilities are.

I understand how you feel, and in fact, I'm also very confused as to how this vulnerability came about. As far as the vulnerability itself is concerned, I am also very curious about the mechanism or code logic that triggered this vulnerability and wonder if there is any black magic in the Windows API mechanism. 


### wf...@chromium.org (2023-09-20)

Maybe we could put a sequence checker around the map and then land that and see if it triggers anywhere on bots/canary?

[Monorail components: Internals>PlatformIntegration]

### ki...@gmail.com (2023-09-21)

Hi, Do you have any further plans for fixing this issue in the near future?

Although I can't reproduce this vulnerability reliably at the moment, it's evident from the ASan logs that it's a real issue.

If there isn't a solid fix plan in the short term, placing a sequence checker would be a good option.

### kr...@chromium.org (2023-09-21)

Yes, I know what is happening and working on a fix.

Each window only access the map from one thread, but different windows can have different thread (the gamepad one here is the one I know which use a different thread). This can mess with the internal structure of the map if another thread writes to it at the wrong time.

### ki...@gmail.com (2023-09-22)

Nice find! Interesting race issue :)

### gi...@appspot.gserviceaccount.com (2023-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/da0106499dbde98e092e37b91abe15be035817ee

commit da0106499dbde98e092e37b91abe15be035817ee
Author: Kristian Monsen <kristianm@google.com>
Date: Mon Sep 25 23:19:26 2023

Use TLS for map to avoid access from different threads

There is a potential UAF as the map for a window is always used
from the same thread, but different windows can be on different
threads. One example is the gamepad controller that has its own
thread created here:
https://source.chromium.org/chromium/chromium/src/+/main:device/gamepad/gamepad_provider.cc;l=235

Note that even though all usage in the bug is from the same thread
this is not safe if another thread is writing to the map at the
same time.

These operations are very rare and very quick which is why this is
hard to reproduce.

Bug: 1483939

Change-Id: Ic3b1a7c27151eb0b28f4bd3fc41e9128ba7296d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4875460
Reviewed-by: Will Harris <wfh@chromium.org>
Reviewed-by: Greg Thompson <grt@chromium.org>
Commit-Queue: Kristian Monsen <kristianm@chromium.org>
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1201204}

[modify] https://crrev.com/da0106499dbde98e092e37b91abe15be035817ee/base/win/message_window.cc


### kr...@google.com (2023-09-26)

kipreyxx@gmail.com This should be fixed now, if you can reproduce it would be nice if you could see if that his the case. 119.0.6031.0 is the version it landed in.

### kr...@google.com (2023-09-26)

This is potentially solved. I believe the root cause is the same as https://bugs.chromium.org/p/chromium/issues/detail?id=1484558 and will monitor that it the crashes go down and marked this as fixed if so.

### ki...@gmail.com (2023-09-27)

I think the issue should have been fixed already, and very appreciate your fix. I am running heavy fuzzer and will update again if there are any new issues.

### kr...@chromium.org (2023-09-27)

We also saw these as crashes here: https://crbug.com/1484558. Have not seen any new crashes since the fix landed so I think this is fixed as well. Will keep monitoring for the rest of the week and will revert if it appears not fixed.

Thank you for reporting.

### kr...@chromium.org (2023-09-28)

This was also reproduced by the fuzzers here: https://bugs.chromium.org/p/chromium/issues/detail?id=1486334

### [Deleted User] (2023-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-28)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M118, which branched on 2023-09-05 (Chromium branch: 5993, Chromium branch position: 1192594)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2023-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-29)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M118, which branched on 2023-09-05 (Chromium branch: 5993, Chromium branch position: 1192594)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-10-05)

I stumbled across this bug for other reasons, but I am noticing the bot did not append the reward-topanel label to this issue. 
I did some checks and this appears to be an anomaly, but will look into this further to see what happened here. 
My only theory is potentially the needs-feedback label prevented the bot from updating but that doesn't seem correct. I am going to remove the needs-feedback label anyway. 

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations, Kiprey! The Chrome VRP Panel has decided to award you $3,000 + $1,000 bisect bonus for this report of a moderately mitigated security bug. The reward amount was decided amount due to the difficult to win race condition and difficulty to reproduce. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-27)

The bisected commit (c2729d382cc03cdfbe18d0f2694314813ef044b0) landed in M119 - updating foundin and removing merge-tbd labels

### [Deleted User] (2024-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1483939?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072651)*
