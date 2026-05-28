#  heap-use-after-free at browser.cc:869 in Browser::TryToCloseWindow (browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062622](https://issues.chromium.org/issues/40062622) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Profiles, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | xp...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2023-01-12 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

I may create a patch in the future that doesn't require the manual steps below.

Manual Steps:

1. Create a new profile.
2. In your "User Data" folder for Chrome, find the name of the new profile created e.g. "Profile 34" or "Profile 5".
3. Once found, open the new profile.
4. Visit chrome://profile-picker and open devtools console.
5. Execute:  
   
   setTimeout(()=>{  
   
   chrome.send("removeProfile", ["C:\Path\To\The\Profile Name from Step 3"]);  
   
   console.log("Profile is deleted, create a new tab in deleted profile and close it.");  
   
   },15000)
6. Focus new profile, create new tab and drag tab out. Hold tab with mouse, do not let go!
7. Wait for step 5 to execute then create a new tab.
8. Close the new tab. UAF triggers.

**Problem Description:**  

I see a few checks being hit as well:

[27396:22964:0112/155149.469:ERROR:profile\_attributes\_storage.cc(420)] Check failed: false.  

[27396:22964:0112/155347.212:ERROR:profile\_attributes\_storage.cc(420)] Check failed: false.  

[27396:22964:0112/155347.212:ERROR:profile\_manager.cc(662)] Loading a profile path that does not exist  

[27396:22964:0112/155448.853:ERROR:browser\_tabstrip.cc(95)] Check failed: false. CloseWebContents called for tab not in our strip

**Additional Comments:**  

Not protected by Miracle Pointer.

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.4 KB)
- [explorer_SOWLIuYFi7.mp4](attachments/explorer_SOWLIuYFi7.mp4) (video/mp4, 5.3 MB)
- [heap-buffer-overflow.txt](attachments/heap-buffer-overflow.txt) (text/plain, 16.6 KB)
- [fix_suggestion.patch](attachments/fix_suggestion.patch) (text/plain, 3.4 KB)
- [nullptrderef.txt](attachments/nullptrderef.txt) (text/plain, 15.6 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 16.8 KB)
- [asan__.txt](attachments/asan_.txt) (text/plain, 41.3 KB)
- [asan_dcheck_off.txt](attachments/asan_dcheck_off.txt) (text/plain, 25.8 KB)

## Timeline

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-13)

OK so I think I understand the bug. There are multiple ways to reach this use-after-free.

The problem is that when we destroy a profile, we attempt to close any windows that belong to the profile.

However, when we are actively dragging a tab, the dragged tab gets missed by the code that attempts to close all open windows.

Medium despite a UaF in the browser process because this requires a *lot* of user interaction. Assigning to a random OWNER in //Chrome/browser/profiles.

[Monorail components: UI>Browser>Profiles UI>Browser>TopChrome>TabStrip]

### [Deleted User] (2023-01-13)

[Empty comment from Monorail migration]

### ad...@google.com (2023-01-13)

(auto-cc on security bug)

### [Deleted User] (2023-01-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2023-01-16)

Re-assigning to David as he may have more bandwidth to look at this and also knows this code better.

### dr...@chromium.org (2023-01-16)

> However, when we are actively dragging a tab, the dragged tab gets missed by the code that attempts to close all open windows.

Maybe what's happening here is that the Browser C++ object is deleted, but somehow the tab-dragging code is keeping a reference to the deleted browser?

The UaF is about a browser object, not a profile object, so I expect there is a bug at the UI layer. There may be a problem with the profile too though, in particular maybe the tab-dragging code should take a ProfileKeepAlive, but it's not yet clear to me. I guess we'd need to repro to see what's going on internally.

### [Deleted User] (2023-01-30)

droger: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-14)

droger: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xp...@gmail.com (2023-02-14)

Another way to reproduce, but it's a heap-buffer-overflow this time around:

1: Delete profile while dragging tab as described in my previous comments.
2: Enable Reader Mode flag and setting (chrome://flags/#enable-reader-mode)
3: Enable reader mode on a supported website e.g. cnn.com

### dr...@chromium.org (2023-02-15)

Assigning to Gabriel who is doing other changes related to profile deletion.

### xp...@gmail.com (2023-03-06)

any chance for a fix? :)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### xp...@gmail.com (2023-05-04)

The issue looks to be with a improperly used method called Close() [1]. The method `b->window()->Close()` will close the window as soon as possible, however only if the window is currently NOT in a drag session [2]. It further states [3]: "Bad things happen if the Browser dtor is called directly as a result of invoking this method".

There is multiple UAF's around the code bound to happen when we access/dereference the deleted browser e.g. [4].

[1]. https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/browser_list.cc;drc=6100e0e35efe4b45dbf82acc22acfa2836a34df0;l=231

[2]. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_window.h;drc=350cefa0021b61bf0459d084c1d6c77e2481813f;l=141

[3]. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_window.h;drc=350cefa0021b61bf0459d084c1d6c77e2481813f;l=146

[4]. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/unload_controller.cc;drc=57a657e0ee27a2697d210e5d2a92237abe73925a;l=189

-

Suggested a fix (fix_suggestion.patch) that instead uses method CloseNow. CloseNow disregards the drag session, so that the browser is properly closed.

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-06-12)

Gabriel: please try to prioritize this bug, as this is a crash and potential security issue.

### xp...@gmail.com (2023-07-07)

Any chance for a fix?

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-09-29)

I think this has been fixed by the profile deletion refactoring done by Gabriel. We should no longer delete a profile if it has a browser open. Gabriel, please verify, and close the bug if it no longer reproes.

### xp...@gmail.com (2023-09-30)

It is a null pointer dereference now. 

### xp...@gmail.com (2023-09-30)

[Empty comment from Monorail migration]

### xp...@gmail.com (2023-10-11)

Hello, 

Can this security issue be closed? I can create another issue with the same steps that is updated with the correct crash/asan logs. 

Thanks.

### xp...@gmail.com (2023-11-01)

Hello,

Can a new owner be assigned? Owner is last seen 19 days ago + this UAF has almost been open for a year.

Thank you.

### dr...@chromium.org (2023-11-06)

So we should either force-close the dragged tab, or have the dragged tab keep a ScopedProfileKeepAlive. I think the keep-alive approach is generally what we use.

### xp...@gmail.com (2023-12-28)

🎉 Hello, almost 1 year bug anniversary. 🎉

Request: Can this bug be tagged for VRP reward since the underlying UAF was fixed?  

Thank you and happy holidays.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1406966?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Profiles, UI>Browser>TopChrome>TabStrip]
[Monorail components added to Component Tags custom field.]

### xp...@gmail.com (2024-03-14)

Updated ASan attached to this comment.

### xp...@gmail.com (2024-05-05)

A very similar bug, was closed, rewarded, and disclosed [0]. The code path that hit the nullptr deref here is no longer valid as the code path is prevented by a DCHECK [1]. 

[0]  https://issues.chromium.org/issues/40934491
[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/signin/profile_picker_handler.cc;drc=028530eff08eb34bb29bcda1a0d3b77348467ffe;l=819

If anyone is there, I'd appreciate if you put the vrp label on this bug as well. Thanks.

### am...@chromium.org (2024-05-15)

Sorry I got a bit Status happy a bit ago, still not used to the atomic changes of the new tracker all the time.

First, Sven, sorry this issue got a bit lost in the shuffle and no one responded here. I stumbled across this doing some analysis so I'm hoping to help here. (In the future, please free free to reach out to security-vrp@ if you need us to check in on an issue.)

I'm assigning this to droger@ since his CL ([1] in C#36) is propertied to have mitigated the null pointer reref (and apparently former OOB read and UAF this issue was previously).

I'm also going to set this as Fixed, but would appreciate it if droger@ if you could confirm there's not further this bug needs to be open for based on prior comments. Otherwise, we are going to consider this issue resolved so it can go to VRP.

### dr...@chromium.org (2024-05-16)

I don't know if this is really related to the CL at #36. The DCHECK is also not a good protection, as it's only active in debug builds and does not protect users of release builds.

The core of the issue is that a profile was deleted without closing the browser window (which was caused by the dragged tab, as explained in [#comment16](https://issues.chromium.org/issues/40062622#comment16)).

I *think* that we can no longer delete a profile while a browser still exists, this was fixed by gabolvr@ a few months ago.
We'd need to try again and see what happens, but hopefully there's nothing to do.

### xp...@gmail.com (2024-05-19)

Re #37, amy@ I appreciate the apology. It's totally understandable. It's a huge bug tracker, and I know issues can be lost in the void. In the future, I'll make sure to reach out to security-vrp@.

Re #38, Sorry, of course, DCHECK means debug build check. I built Chromium ASan with DCHECKS off and got asan_dcheck_off.txt. With the same steps, we currently crash at [0], blame: [1]

[0]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_attributes_entry.cc;drc=3e79aface557755e09fd9a58f53da14bebf3eb1f;l=860
[1]: https://chromium-review.googlesource.com/c/chromium/src/+/5374599

### sp...@google.com (2024-05-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 for this report of highly mitigated memory corruption, mitigated by substantial user interaction. While we appreciate all bug reports and the effort it takes to discover and report security issues, it is important to mention that bugs that involve a series of implausible user interactions may not be eligible for VRP rewards as there is a very low likelihood of real world exploitability of issues involving such user interactions.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-22)

Thank you for the report, Sven, and for understanding about it getting lost in the shuffle.

### xp...@gmail.com (2024-05-22)

Quick question, I know there has been numerous changes to the reward amounts since the inception (early 2023) of this bug - 2023-2024 introduced many. Was the reward values of highly mitigated bugs through user interaction changed at any point? Or was this reward amount left untouched?

### am...@chromium.org (2024-05-22)

Thanks for the question.
The reward values for mitigated security bugs, including the highly mitigated category and language about substantially mitigated security bugs [1] were landed in August 2022, and communicated to the VRP Reporters Chromium community at that time.

There has not been a change to mitigated reward values or the mitigated bug classifications since that time. Any change would have been communicated to the community, like all changes major and minor. :)

[1] [https://g.co/chrome/vrp##reward-amounts-for-mitigated-security-bugs](https://g.co/chrome/vrp#)
(Substantially mitigated: A heavily mitigated security bug, not likely to be able to be exploited in a real-world scenario; e.g. a bug requiring a series of implausible user interactions – such issues are not generally considered security issues and may not be eligible for a VRP reward.)

### xp...@gmail.com (2024-05-22)

Thank you very much for the explanation. And thank you for the reward!

### pe...@google.com (2024-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062622)*
