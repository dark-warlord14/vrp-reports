# Heap-use-after-free in aura::WindowTreeHostPlatform::OnBoundsChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40054892](https://issues.chromium.org/issues/40054892) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Internals>Aura |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | yj...@chromium.org |
| **Created** | 2021-02-18 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
1. download chromium with ASAN build
2. ./chrome "about:blank" "about:blank"
3. drag the second tab ,don't release the mouse and move around, crash occurs. See the video for more details.

What is the expected behavior?

What went wrong?
In function OnBoundsChanged at file ui/aura/window_tree_host_platform.cc, the BrowserDesktopWindowTreeHostLinux object will be freed by OnHostMovedInPixels at line 224 and it will be used at line 225, UAF occurs.
The ASAN log shows the full free path for this object.

210 void WindowTreeHostPlatform::OnBoundsChanged(const gfx::Rect& new_bounds) {
211   // It's possible this function may be called recursively. Only notify
212   // observers on initial entry. This way observers can safely assume that
213   // OnHostDidProcessBoundsChange() is called when all bounds changes have
214   // completed.
215   if (++on_bounds_changed_recursion_depth_ == 1) {
216     for (WindowTreeHostObserver& observer : observers())
217       observer.OnHostWillProcessBoundsChange(this);
218   }
219   float current_scale = compositor()->device_scale_factor();
220   float new_scale = ui::GetScaleFactorForNativeView(window());
221   gfx::Rect old_bounds = bounds_in_pixels_;
222   bounds_in_pixels_ = new_bounds;
223   if (bounds_in_pixels_.origin() != old_bounds.origin())
224     OnHostMovedInPixels(bounds_in_pixels_.origin());    // BrowserDesktopWindowTreeHostLinux will be freed in this function call
225   if (bounds_in_pixels_.size() != old_bounds.size() ||   // The freed obj is used here
226       current_scale != new_scale) {
227     pending_size_ = gfx::Size();
228     OnHostResizedInPixels(bounds_in_pixels_.size());
229   }
230   DCHECK_GT(on_bounds_changed_recursion_depth_, 0);
231   if (--on_bounds_changed_recursion_depth_ == 0) {
232     for (WindowTreeHostObserver& observer : observers())
233       observer.OnHostDidProcessBoundsChange(this);
234   }
235 }

Did this work before? N/A 

Chrome version: 87.0.4280.88  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [asan](attachments/asan) (text/plain, 9.8 KB)
- [video.webm](attachments/video.webm) (video/webm, 3.2 MB)

## Timeline

### [Deleted User] (2021-02-18)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-02-18)

yjliu@: can you take a look at this? If you're not the right owner, feel free to re-assign. Thanks!

[Monorail components: Internals>Aura]

### yj...@chromium.org (2021-02-18)

Hi, jdeblasio@, do you know if this is a new problem? Is this Linux specific? I tried building chrome on Linux just now, (chrome version:90.0.4422.0) and could not reproduce this crash.



### yj...@chromium.org (2021-02-18)

This is the version that I tried to reproduce this problem.
Google Chrome	90.0.4422.0 (Developer Build) unknown (64-bit)
Revision	2f4dbb4dc1ca90b88d8b41cb8523319720064279-refs/heads/master@{#855070}
OS	Linux
JavaScript	V8 9.0.207
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4422.0 Safari/537.36
Command Line	./src/out/linux_release/chrome --flag-switches-begin --disable-gpu-rasterization --flag-switches-end --origin-trial-disabled-features=SecurePaymentConfirmation about:blank about:blank
Executable Path	/usr/local/google/home/yjliu/chromium/src/out/linux_release/chrome
Profile Path	/usr/local/google/home/yjliu/.config/chrome-remote-desktop/chrome-profile/Profile 1
Variations	3ac60855-3ec2a267
63dcb6a3-99d57e67
e706e746-3fdb6cd0
f296190c-cc017729
4442aae2-7158671e
f690cf64-4ad60575
ed1d377-e1cc0f14
75f0f0a0-d7f6b13c
e2b18481-92bb99a9
e7e71889-4ad60575


### me...@gmail.com (2021-02-19)

Maybe you can download the newest asan-release-*.zip and try to reproduce it.
BTW, it this severity low? I think this is similar to https://crbug.com/chromium/1138911, which is also a browser UAF.

### yj...@chromium.org (2021-02-19)

The fix is currently under review.
https://chromium-review.googlesource.com/c/chromium/src/+/2705310

### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-02-26)

After this fix, this uaf can still be triggered with asan-release-857989.

### yj...@chromium.org (2021-02-26)

I am not able to reproduce this crash using a build from this morning's latest commit.

### me...@gmail.com (2021-02-27)

In step3, when you move around the tab, you need to merge and split the browser tab repeatedly(merge the tab will call the onClose function, and free BrowserDesktopWindowTreeHostLinux. Move around the tab will call the OnBoundsChanged, which will use the freed object ).See the video for how to repro that. Maybe you need to try more times to reproduce it.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-03-11)

hi, I find that this uaf has been patched in this patch: https://chromium-review.googlesource.com/c/chromium/src/+/2749355, which check the weak_ref after function OnHostMovedInPixels. However,it is releated to a bug id (https://bugs.chromium.org/p/chromium/issues/detail?id=1185482) that much later than this one. Any reply?

### me...@gmail.com (2021-03-11)

[Comment Deleted]

### me...@gmail.com (2021-03-13)

[Comment Deleted]

### me...@gmail.com (2021-03-17)

[Comment Deleted]

### jd...@chromium.org (2021-03-17)

Adding sky@ due to this being a possible duplicate of https://crbug.com/chromium/1185482.

sky@: can you confirm whether or not this is a duplicate or not?

merc.ouc@: if sky@ confirms, I'll make sure that you're credited.

### sk...@chromium.org (2021-03-17)

This is in fact a duplicate of https://crbug.com/chromium/1185482. Updated appropriately.

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### me...@gmail.com (2021-03-18)

This is a dup, but I submit it first, so will there be a cve or reward? 


### sk...@chromium.org (2021-03-18)

Someone from security will need to comment on that. +adetaylor

### ad...@google.com (2021-03-18)

Yep, we'll make sure that this is rewarded appropriately. In fact I believe jdeblasio@ already ensured this was lined up to go the VRP panel but I'll triple-check. You're right that any reward will be paid to the earliest report.

### me...@gmail.com (2021-03-18)

Thank you:)

### [Deleted User] (2021-03-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-23)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-03-24)

Congratulations, merc.ouc@! The VRP panel has decided to award you $7,500 for this report. Nice work! 

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-03-29)

Updating to reflect appropriate severity (since was originally deemed low severity) as it was not reproducible because fix for issue was landed in later reported https://bugs.chromium.org/p/chromium/issues/detail?id=1185482

### am...@chromium.org (2021-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1179635?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1185482]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054892)*
