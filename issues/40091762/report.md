# heap-use-after-free in ProfileCompare::operator()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091762](https://issues.chromium.org/issues/40091762) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Incognito, UI>Browser>Profiles |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-06-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36

Steps to reproduce the problem:
1. Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j4 -C out/chrome_asan chrome
2. Build a mini web server.
	I used python twisted module to build the webserver.
	1) run python web.py

3. Run chromium with args --incognito (using my fuzzer)

4. Press Ctrl+Alt+o to open bookmarkpage while fuzzer is running

What is the expected behavior?

What went wrong?
Got a UAF.

It seems like a member of router_map_ is referenced by another "point off_the_record_profile_" at the same time.After Off_the_record_profile_.reset(),the router_map_ call find(),which use the member again,then UAF happened.

It only happened once.But according to the stack trace,i doubt that if OffTheRecordProfile's lifetime got something wrong or router_map_ is not safe(another pointer free its member)?

Here are some of my ideas(Not sure if I am correct,but i wish it could help) :
1.When close the browser,the correct process about delete OffRecordProfile should be :
-->extensions::InputImeEventRouterFactory::RemoveProfile
-->some_other_function
-->ProfileImpl::DestroyOffTheRecordProfile

2.the UAF crash stacktrace shows that the sequence is :
-->ProfileImpl::DestroyOffTheRecordProfile
-->extensions::InputImeEventRouterFactory::RemoveProfile
-->UAF happened

3.So i consider that some operation between RemoveProfile and DestroyOffTheRecordProfile leads the result(like open bookmark page) .The operation will call GetRouter using the same profile and let router_map_ re-own OffRecordProfile member.Then DestroyOffTheRecordProfile happened,off_the_record_profile_ free the profile pointer.Finally RemoveProfile happened and called router_map_.find(profile),the ProfileCompare::operator leads the UAF.

Did this work before? N/A 

Chrome version: 68.0.3432.0  Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### oc...@chromium.org (2018-06-26)

Can you please provide a standalone repro (i.e. a single HTML file that we can run)? 

### cd...@gmail.com (2018-06-26)

The crash just related to my operation.I have no idea about imitating the operation by a HTML file yet.But theoretically there could be some file to repro.


As proof in another way,if add GetRouter(OffRecordProfile) after RemoveProfile in the sources code,once closes the browser,UAF will happen and get the same stacktrace as crash.txt. 

### sh...@chromium.org (2018-06-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### oc...@chromium.org (2018-06-26)

Could you clarify what your fuzzer is doing in these steps? 

3. Run chromium with args --incognito (using my fuzzer)

4. Press Ctrl+Alt+o to open bookmarkpage while fuzzer is running

We can't run your fuzzer to reproduce this. 

I'm setting some tentative security labels here for now, but i'm unsure of the exploitability here as it seems to occur during browser shutdown. 




[Monorail components: UI>Browser>Incognito UI>Browser>Profiles]

### oc...@chromium.org (2018-06-26)

msramek, would you be the right person to help with triaging this, as it seems to be related to incognito profile destruction? I haven't been able to repro, but the stacktrace the reporter provided may point to something obvious. 


### cd...@gmail.com (2018-06-26)

Sorry for my inaccurate description about fuzzer.
The purpose,i mentioned fuzzer,is to explain that the situation is complicated: Browser is openning tabs and loading some html files and i open the bookmark page at the same time.

So the step may become this one:

3. Run chromium with args --incognito 
4. Open some html files
5. Press Ctrl+Alt+o to open bookmarkpage




### sh...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-09)

msramek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-24)

msramek: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-08-06)

Friendly ping from the security sheriff. This is a high severity vulnerability affecting Stable branch. msramek@, please post an update / help to triage this. Thanks!

### ms...@chromium.org (2018-08-07)

Sorry, didn't mean to sit on a crash report, but I'm really swamped lately and this quickly bubbles down.

Based on the stack trace, bug description and the repro in https://crbug.com/chromium/856135#c2, it sounds to me like this bug is localized to how the Profile pointer is handled in input_ime/? Let me pass to shuchen@ who's the owner. Feel free to ping back if it actually turns out to be an issue with the Incognito Profile itself.

### sh...@chromium.org (2018-08-15)

Sorry for missing this issue in the past days.

I start to look into this issue.


### sh...@chromium.org (2018-08-17)

My findings:
1) When hitting InputImeEventRouterFactory::RemoveProfile(profile), the passed-in profile MUST NOT cause the UAF.
2) Instead, some other saved Profile pointers in the InputImeEventRouterFactory::router_map_ causes the UAF.
3) Noticed that in the crash stack line #43, ProfileImpl::DestroyOffTheRecordProfile() is called, but InputImeEventRouterFactory seems not receiving the notification of NOTIFICATION_PROFILE_DESTROYED.
4) However, OffTheRecordProfileImpl::~OffTheRecordProfileImpl() do send the notification.

msramek@, can you please forward to off-the-record-profile owners to confirm whether there is a way to destruct a profile without sending the notification? Thanks!


### sh...@chromium.org (2018-08-24)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mp...@google.com (2018-09-05)

Hi, security sheriff here. Any movement on this?

### ms...@chromium.org (2018-09-10)

Thanks, shuchen@, for the pointers. Passing to rhalavati@ to PTAL per offline discussion.

### rh...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-15)

--Chrome Identity automated triaging--

This bug is P0 or P1 and has gone two weeks without any activity. Please provide a status update or lower the priority. Please see https://goo.gl/78kbny for more details. Please remove the Services>SignIn or UI>Browser>Profiles components if this bug isn't related to Chrome Identity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@chromium.org (2018-10-16)

I think I found a bug, but I don’t know if this can be the cause of this crash.  
shuchen@, what do you think?

1- In GetInputImeEventRouter, if the input profile has incognito profile, it is switched into the incognito one.

2- In InputImeEventRouterFactory::GetRouter, as |router_map_| uses Profile::ProfileCompare as the comparison function, it keeps and returns a common router for both incognito and regular profiles.

3- In InputImeEventRouterFactory::RemoveProfile, as |it->first| and |profile| are compared using regular == operator, the regular/incognito override does not work and the destroyed profile is removed from |router_map_|, only if it is the one that is originally registered. (If it's registered for incognito first, it's deleted when incognito profile is destroyed and if it's registered on regular, it's deleted when regular profile is destroyed.

4- If all regular windows are closed, regular profile is not destroyed until an incognito window is open.

From the above I gather that the expected behavior is to keep one InputImeEventRouter per both regular and incognito profiles, but it is supposed to be deleted when both of them are destroyed.
This behaviour is broken when browser starts in incognito mode and then a regular window is created (like opening bookmark manager) and then incognito window is closed. In this case, when incognito window is closed, the router is destroyed and the regular profile will remain without router (and on the next call to GetInputImeEventRouter, a new one is created).

This can be correct by either changing GetInputImeEventRouter to use GetOriginalProfile instead of GetOffTheRecordProfile, or use two separate routers for incognito and regular profiles by removing the ProfileCompare function. (Isn’t the latter the better approach as the router will know if it’s working in regular mode or incognito?)

But can this be the cause of the crash?

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-18)

I guess you've found the root cause! Thanks for the investigation!

I introduced the ProfileCompare by this cl: https://codereview.chromium.org/229633003.
The major reason was the extension framework tried to auto launch a new extension instance for the incognito profile (but the IME extension needs to work for the regular and corresponding incognito profiles) back in 2014.

As I've tried on the latest system, the extension framework no longer auto launches a new extension instance for the incognito profile. So I think the 1st solution you mentioned in #22 should work. And ProfileCompare should NOT be removed.

### rh...@chromium.org (2018-10-18)

Thank you shuchen@, I will create a CL.


### bu...@chromium.org (2018-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a9fb0358c3b590e6841e9b4c8dc577f7b3739719

commit a9fb0358c3b590e6841e9b4c8dc577f7b3739719
Author: Ramin Halavati <rhalavati@chromium.org>
Date: Thu Oct 18 11:39:48 2018

Use original profile in InputImeEventRouter.

GetInputImeEventRouter uses the incognito profile as a common reference
for an incognito profile and its original profile. But when a profile is
destroyed, it deletes the reference based on the profile itself.

This can cause problems when Chrome starts in incognito mode, then a
regular window is opened, and the incognito window is closed. In this
scenario, the InputImeEventRouter is deleted when the incognito profile
is closed, but it is still referenced by the original profile.

To fix this, the original profile is used as the reference for both
modes as it is always destroyed after the incognito one.

Bug: 856135
Change-Id: Ieb4f006e9cc5c36cd9264fd0b1b4ef490e1f3162
Reviewed-on: https://chromium-review.googlesource.com/c/1288350
Reviewed-by: Shu Chen <shuchen@chromium.org>
Commit-Queue: Ramin Halavati <rhalavati@chromium.org>
Cr-Commit-Position: refs/heads/master@{#600727}
[modify] https://crrev.com/a9fb0358c3b590e6841e9b4c8dc577f7b3739719/chrome/browser/extensions/api/input_ime/input_ime_api.cc


### rh...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

govind@ - good for 71

### go...@chromium.org (2018-10-27)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/856135#c32. Please merge latest by 3:00 PM PT, Monday (10/29) so we can pick it up for next week beta. Thank you.

### cr...@appspot.gserviceaccount.com (2018-10-29)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/83519494c059ebb2d47c5177b5bf978760121650

Commit: 83519494c059ebb2d47c5177b5bf978760121650
Author: rhalavati@chromium.org
Commiter: rhalavati@chromium.org
Date: 2018-10-29 06:57:25 +0000 UTC

Use original profile in InputImeEventRouter.

GetInputImeEventRouter uses the incognito profile as a common reference
for an incognito profile and its original profile. But when a profile is
destroyed, it deletes the reference based on the profile itself.

This can cause problems when Chrome starts in incognito mode, then a
regular window is opened, and the incognito window is closed. In this
scenario, the InputImeEventRouter is deleted when the incognito profile
is closed, but it is still referenced by the original profile.

To fix this, the original profile is used as the reference for both
modes as it is always destroyed after the incognito one.

Bug: 856135
Change-Id: Ieb4f006e9cc5c36cd9264fd0b1b4ef490e1f3162
Reviewed-on: https://chromium-review.googlesource.com/c/1288350
Reviewed-by: Shu Chen <shuchen@chromium.org>
Commit-Queue: Ramin Halavati <rhalavati@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#600727}(cherry picked from commit a9fb0358c3b590e6841e9b4c8dc577f7b3739719)
Reviewed-on: https://chromium-review.googlesource.com/c/1303359
Reviewed-by: Ramin Halavati <rhalavati@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#364}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### bu...@chromium.org (2018-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/83519494c059ebb2d47c5177b5bf978760121650

commit 83519494c059ebb2d47c5177b5bf978760121650
Author: Ramin Halavati <rhalavati@chromium.org>
Date: Mon Oct 29 06:57:25 2018

Use original profile in InputImeEventRouter.

GetInputImeEventRouter uses the incognito profile as a common reference
for an incognito profile and its original profile. But when a profile is
destroyed, it deletes the reference based on the profile itself.

This can cause problems when Chrome starts in incognito mode, then a
regular window is opened, and the incognito window is closed. In this
scenario, the InputImeEventRouter is deleted when the incognito profile
is closed, but it is still referenced by the original profile.

To fix this, the original profile is used as the reference for both
modes as it is always destroyed after the incognito one.

Bug: 856135
Change-Id: Ieb4f006e9cc5c36cd9264fd0b1b4ef490e1f3162
Reviewed-on: https://chromium-review.googlesource.com/c/1288350
Reviewed-by: Shu Chen <shuchen@chromium.org>
Commit-Queue: Ramin Halavati <rhalavati@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#600727}(cherry picked from commit a9fb0358c3b590e6841e9b4c8dc577f7b3739719)
Reviewed-on: https://chromium-review.googlesource.com/c/1303359
Reviewed-by: Ramin Halavati <rhalavati@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#364}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/83519494c059ebb2d47c5177b5bf978760121650/chrome/browser/extensions/api/input_ime/input_ime_api.cc


### aw...@chromium.org (2018-10-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-30)

Hi cdsrc2016@, thanks for the report. The VRP panel took a look at this and thought it would be very difficult to exploit, especially as it's in the shutdown path. The decided to reward $500 for your help with this. They did note that they'd take another look for a higher reward if you could describe how it could be exploited.

### aw...@google.com (2018-10-31)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-11-01)

[Comment Deleted]

### cd...@gmail.com (2018-11-01)

Hi awhalley@,Thanks a lot for the reward:)
I think it's hard to exploite too.But another point is that this one happened in main process.Could this one be the last part of sandbox escape? Combined with another hard to exploite one, such as   https://bugs.chromium.org/p/chromium/issues/detail?id=888366 which perhaps is not easy to exploite either but could shutdown the browser directly.
Above is sheerly a personal view,only for reference.


### sh...@chromium.org (2018-11-05)

The fix caused the regression https://crbug.com/chromium/900124. Working on a quick fix now.


### bu...@chromium.org (2018-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2f0b419df243400f954e11b649f4862a1e0ff367

commit 2f0b419df243400f954e11b649f4862a1e0ff367
Author: Shu Chen <shuchen@google.com>
Date: Mon Nov 05 09:00:58 2018

Fix the regression caused by http://crrev.com/c/1288350.

Bug: 900124,856135
Change-Id: Ie11ad406bd1ea383dc2a83cc8661076309154865
Reviewed-on: https://chromium-review.googlesource.com/c/1317010
Reviewed-by: Lan Wei <azurewei@chromium.org>
Commit-Queue: Shu Chen <shuchen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#605282}
[modify] https://crrev.com/2f0b419df243400f954e11b649f4862a1e0ff367/chrome/browser/extensions/api/input_ime/input_ime_api.cc


### bu...@chromium.org (2018-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4b768d814aae82c5db388c8a5dfd2a4b45426ce1

commit 4b768d814aae82c5db388c8a5dfd2a4b45426ce1
Author: Shu Chen <shuchen@google.com>
Date: Tue Nov 06 01:06:48 2018

Fix the regression caused by http://crrev.com/c/1288350.

Bug: 900124,856135
Change-Id: Ie11ad406bd1ea383dc2a83cc8661076309154865
Reviewed-on: https://chromium-review.googlesource.com/c/1317010
Reviewed-by: Lan Wei <azurewei@chromium.org>
Commit-Queue: Shu Chen <shuchen@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#605282}(cherry picked from commit 2f0b419df243400f954e11b649f4862a1e0ff367)
Reviewed-on: https://chromium-review.googlesource.com/c/1318772
Reviewed-by: Shu Chen <shuchen@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#531}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/4b768d814aae82c5db388c8a5dfd2a4b45426ce1/chrome/browser/extensions/api/input_ime/input_ime_api.cc


### cr...@appspot.gserviceaccount.com (2018-11-06)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/4b768d814aae82c5db388c8a5dfd2a4b45426ce1

Commit: 4b768d814aae82c5db388c8a5dfd2a4b45426ce1
Author: shuchen@google.com
Commiter: shuchen@chromium.org
Date: 2018-11-06 01:06:48 +0000 UTC

Fix the regression caused by http://crrev.com/c/1288350.

Bug: 900124,856135
Change-Id: Ie11ad406bd1ea383dc2a83cc8661076309154865
Reviewed-on: https://chromium-review.googlesource.com/c/1317010
Reviewed-by: Lan Wei <azurewei@chromium.org>
Commit-Queue: Shu Chen <shuchen@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#605282}(cherry picked from commit 2f0b419df243400f954e11b649f4862a1e0ff367)
Reviewed-on: https://chromium-review.googlesource.com/c/1318772
Reviewed-by: Shu Chen <shuchen@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#531}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/856135?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Incognito, UI>Browser>Profiles]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091762)*
