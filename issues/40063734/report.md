# Heap-use-after-free in SavedTabGroupBar

| Field | Value |
|-------|-------|
| **Issue ID** | [40063734](https://issues.chromium.org/issues/40063734) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Mac |
| **Reporter** | me...@gmail.com |
| **Assignee** | dl...@chromium.org |
| **Created** | 2023-03-23 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

commit at 9602ee4194b147a2b372c268a08714d7985cb5ba

1. compile chromium on Mac with M1 chip, enable ASAN
2. Open Chromium and save at least FIVE tabGroups, this will show the overflow menu in bookmark bar
3. start a server at the folder of poc.html
4. run chrome `./Chromium --enable-features=TabGroupsSave --user-data-dir=./noexist http://127.0.0.1:8605/poc.html` and open the SavedTabGroups' overflow menu

**Problem Description:**

1. Analysis

On Mac with an M1 chip, when you open Chromium, it sometimes will not display the Widget normally. The opened Bubble will not close even if we close the whole Browser. It will be closed after Browser shutdown.

In class `SavedTabGroupBar`, there is a member `widget_observation_`[1], which will observe the SavedTabGroupBar's overflow Bubble widget and it will be reset when `SavedTabGroupBar::OnWidgetClosing`[2] is called.  

But as I said, chromium on Mac M1 sometimes will not close the widget even if we close the browser, the `OnWidgetClosing` will also not be called. So this `widget_observation_` will not be reset even if browser is closed, but the Bubble will be closed after browser shutdown. When `SavedTabGroupBar` is destructed, `widget_observation_` will call RemoveObserver, which will use the close Bubble widget, UAF occurs.

```
void SavedTabGroupBar::OnWidgetClosing(views::Widget\* widget) {  
  widget_observation_.Reset();  
  overflow_menu_ = nullptr;  
  bubble_delegate_ = nullptr;  
}  

```

It seems that llvm-symbolizer cannot work normally on my Mac M1, so the log only has the binary info.

[1] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.h;l=165;bpv=1;bpt=0;drc=3ab53bb5dd10f35600d34883b97901fb57781cc2>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.cc;l=404;bpv=1;bpt=0;drc=3ab53bb5dd10f35600d34883b97901fb57781cc2>

2. Bisect  
   
   commit 3ab53bb5dd10f35600d34883b97901fb57781cc2  
   
   <https://chromium-review.googlesource.com/c/chromium/src/+/4347637>

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 171 B)
- [asan.txt](attachments/asan.txt) (text/plain, 25.7 KB)
- [video.mov](attachments/video.mov) (video/quicktime, 5.1 MB)

## Timeline

### [Deleted User] (2023-03-23)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-24)

dljames@, I'm told you might be the owner of the TabGroupsSave feature, mind taking a quick peek? Note that we are unable to repro this at all, so this may not be actionable, but I figured its worth a few minutes of quick looking.

### av...@chromium.org (2023-03-24)

Mac bug triage: has owner, -> assigned

### dl...@chromium.org (2023-03-24)

Thank you for passing the bug along, I will see what I can do.

### dl...@chromium.org (2023-03-24)

I have a potential fix out for review but I am not 100% sure if this will prevent the issue as I was also not able to reproduce this.
At worst, the fix does nothing (behavior stays the same), and we continue to see this crash. At best, the uaf is fixed! 

More information on how this was fixed in the CL once it lands.

Thank you once again!


[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### am...@chromium.org (2023-03-24)

Introduced in head/113, SI-None as this in TabGroupsSave which is not shipped
technically high severity due to UAF in browser process, but significantly mitigated by a large amount of user interaction 

### gi...@appspot.gserviceaccount.com (2023-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/54dd973e3608abc4e3698d19e6625aea4189dfb9

commit 54dd973e3608abc4e3698d19e6625aea4189dfb9
Author: dljames <dljames@google.com>
Date: Fri Mar 24 19:56:00 2023

Fix UAF by switching OnWidgetClosing -> OnWidgetDestroying

Fixes a UAF in the SavedTabGroupBar on MacOS devices with an M1 chip.
Specifically, OS native-widget destructions do not call the
WidgetObserver::OnWidgetClosing event. In this case, this means that on
certain devices, the SavedTabGroupBar was not able to reset its widget
observers for the context menu, which would cause UAFs to occur when the
widget being observed is recreated.

Instead, we use WidgetObserver::OnWidgetDestroying before a widget
has a chance to close which is much safer, and follows the documentation
in the WidgetObserver class.

More information can be found here: ui/views/widget/widget_observer.h

Change-Id: I7c39232d0162292175b5a7c5f6270402b866de77
Bug: 1427043
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4369764
Commit-Queue: Darryl James <dljames@chromium.org>
Reviewed-by: Eshwar Stalin <estalin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1121889}

[modify] https://crrev.com/54dd973e3608abc4e3698d19e6625aea4189dfb9/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.h
[modify] https://crrev.com/54dd973e3608abc4e3698d19e6625aea4189dfb9/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.cc


### dl...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### dl...@chromium.org (2023-03-24)

I will keep this as available until we can confirm that this is actually fixed; jumped the gun whoops.

### [Deleted User] (2023-03-25)

[Empty comment from Monorail migration]

### ad...@google.com (2023-03-25)

(I am a bot: this is an auto-cc on a security bug)

### me...@gmail.com (2023-03-28)

Hi, I have verified that this UAF is no longer reproducible after this patch, can we mark this as fixed?

### dl...@chromium.org (2023-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations, Krace! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-04)

This issue was migrated from crbug.com/chromium/1427043?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063734)*
