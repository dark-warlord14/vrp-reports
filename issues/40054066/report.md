# Security: UAF in MediaStreamCapture

| Field | Value |
|-------|-------|
| **Issue ID** | [40054066](https://issues.chromium.org/issues/40054066) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | il...@chromium.org |
| **Created** | 2020-12-04 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: stable  

Operating System: Linux, Win, Chrome OS

**REPRODUCTION CASE**  

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python -m SimpleHTTPServer  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-blink-features=MojoJS "<http://localhost:8000/poc.html>"  

Click the trigger button to share the current tab, and then close the current tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 16.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)

## Timeline

### [Deleted User] (2020-12-04)

[Empty comment from Monorail migration]

### le...@gmail.com (2020-12-04)

Sorry for forgetting the VULNERABILITY DETAILS:

|MediaStreamUIProxy::Core::OnStarted|[1] task could be run after |infobars_entry| is erased from |infobars_|[2]. 
```
void TabSharingUIViews::OnInfoBarRemoved(infobars::InfoBar* infobar,
                                         bool animate) {
  ...
  infobar->owner()->RemoveObserver(this);
  infobars_.erase(infobars_entry); // <<<---------
  if (InfoBarService::WebContentsFromInfoBar(infobar) == shared_tab_)
    StopSharing();
}
```

|OnStarted| will eventually call |CreateInfobarsForAllTabs| which will add an observer to |browser_list|[3]. 

```
void TabSharingUIViews::CreateInfobarsForAllTabs() {
  BrowserList* browser_list = BrowserList::GetInstance();
  ...
  browser_list->AddObserver(this); // <<<---------
}
```

When |TabSharingUIViews| is destructed, this observer will not be cleaned up because |infobars_| is empty[4]. 
```
TabSharingUIViews::~TabSharingUIViews() {
  if (!infobars_.empty()) // <<<---------
    StopSharing();
}
```

Therefore, UAF is triggered when |OnBrowserRemoved| notification is sent to the observer[5].
```
void BrowserList::RemoveBrowser(Browser* browser) {
  // Remove |browser| from the appropriate list instance.
  BrowserList* browser_list = GetInstance();
  ...

  for (BrowserListObserver& observer : observers_.Get())
    observer.OnBrowserRemoved(browser); // <<<---------

  ...
```


[1]. https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/media/media_stream_ui_proxy.cc;l=300;drc=cbe6f7f3337a52eb630bb244d005f50a70269104
[2]. https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc;l=239;drc=403c57b8443e91016941a96d8dd03c3ad05b1071
[3]. https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc;l=274;drc=403c57b8443e91016941a96d8dd03c3ad05b1071
[4]. https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc;l=139;drc=403c57b8443e91016941a96d8dd03c3ad05b1071
[5]. https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/browser_list.cc;l=117;drc=a5bb1f0651f824098975f20f49b31ec6b71813db

### es...@chromium.org (2020-12-04)

miu@, can you please take a look at this security bug? Thanks!

[Monorail components: Internals>Media>ScreenCapture]

### [Deleted User] (2020-12-04)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mi...@chromium.org (2020-12-07)

[Empty comment from Monorail migration]

### mi...@chromium.org (2020-12-08)

The repro case (JS in poc.html) has an interesting issue: It has onStreamStarted() being called via a setInterval(). This is actually causing onStreamStarted() to be called repeatedly, every 10 ms. I'm guessing this was done to trigger the race condition leading to the ASAN errors?

However, the repeat calls to OnStreamStarted() causes a DCHECK() to trigger a crash in the browser process. Thus, the browser process only expects it to be called once.

So, I'll work on both: 1) ignoring repeated calls to OnStreamStarted(); and 2) having the TabSharingUIViews destructor unconditionally call StopSharing() to ensure there's nothing dangling (including its presence in the BrowserList observer list).


### mi...@chromium.org (2020-12-09)

Updating component (Blink>GUM includes UI prompts, Internals>Media>ScreenCapture is for the capturer itself).

[Monorail components: -Internals>Media>ScreenCapture Blink>GetUserMedia]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f

commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f
Author: Yuri Wiitala <miu@chromium.org>
Date: Thu Dec 10 18:07:39 2020

Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

Bug: 1155426
Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#835736}

[modify] https://crrev.com/3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### mi...@chromium.org (2020-12-11)

Fix landed. Will request merge to release branches Monday, after double-checking Canary is working as expected.

### [Deleted User] (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M87. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-12)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-12)

Pls answer https://crbug.com/chromium/1155426#c13 for merge review. 

### ad...@google.com (2020-12-14)

Approving merge to M88, branch 4324, assuming this looks good in canary.

### sr...@google.com (2020-12-14)

[Empty comment from Monorail migration]

### sr...@google.com (2020-12-14)

Merge CL sent through CQ dry-run - https://chromium-review.googlesource.com/c/chromium/src/+/2590967

Please land it once it passes CQ.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1e02557c9206059a845d83f806f6634ad2687f4f

commit 1e02557c9206059a845d83f806f6634ad2687f4f
Author: Yuri Wiitala <miu@chromium.org>
Date: Mon Dec 14 23:51:58 2020

Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

(cherry picked from commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f)

Bug: 1155426
Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#835736}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2590967
Reviewed-by: Yuri Wiitala <miu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#925}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/1e02557c9206059a845d83f806f6634ad2687f4f/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/1e02557c9206059a845d83f806f6634ad2687f4f/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $20,000 for this bug.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-30)

Assuming no problems have shown up in Canary, approving merge to M87, branch 4280.

### [Deleted User] (2021-01-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/de6de32e9733ae62d6bcd210691bb2a0577a8662

commit de6de32e9733ae62d6bcd210691bb2a0577a8662
Author: Yuri Wiitala <miu@chromium.org>
Date: Tue Jan 05 03:08:16 2021

Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

Bug: 1155426
Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#835736}
(cherry picked from commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f)


TBR=miu@chromium.org

Change-Id: Ic0e8bb5d92aec527855dbe5771952cc4a84b2452
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2610364
Reviewed-by: Yuri Wiitala <miu@chromium.org>
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1998}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/de6de32e9733ae62d6bcd210691bb2a0577a8662/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/de6de32e9733ae62d6bcd210691bb2a0577a8662/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### ad...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c4e038ad8b00d06264b67389ced7786c30a09562

commit c4e038ad8b00d06264b67389ced7786c30a09562
Author: Yuri Wiitala <miu@chromium.org>
Date: Fri Jan 08 18:38:21 2021

Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

Bug: 1155426
Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#835736}
(cherry picked from commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f)


TBR=miu@chromium.org

(cherry picked from commit de6de32e9733ae62d6bcd210691bb2a0577a8662)

Change-Id: Ic0e8bb5d92aec527855dbe5771952cc4a84b2452
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2610364
Reviewed-by: Yuri Wiitala <miu@chromium.org>
Commit-Queue: Yuri Wiitala <miu@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1998}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617560
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1501}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/c4e038ad8b00d06264b67389ced7786c30a09562/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/c4e038ad8b00d06264b67389ced7786c30a09562/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### ke...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### il...@google.com (2021-01-13)

The CL broke down "share this tab instead button" for all chrome users. It's most commonly used by Meet users: but now it interrupts the presentation instead of switching the capture source.

I've confirmed that with the CL reverted UI works as it was intended.

I suggest we revert ASAP. 

### il...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### il...@google.com (2021-01-13)

This is very tricky situations: The CL breaks user visible UI and affects all Meet users. But the vulnerability also sounds important, so I won't revert the CL before confirming with everyone.

And the worst situation - the author of the CL has left. 

mfoltz@, guidou@, could you help here? I'm not that familiar with the code in question. 
Could help me understand how that innocently looking CL broke "share this tab instead" button?

I guess the best way forward is to make a fix on top of the existing CL an backport it to M86-M88.

### il...@google.com (2021-01-13)

I've confirmed the issue on 86.0.4240.261,
87.0.4280.141, 88.0.4324.77 and 89.0.4387.0.


I've found exact line breaking the presentations: https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc;l=141;drc=073e74ade285c0c22ef01bccdf260854d7b1aa85

I don't yet understand if stopping the presentation is important for the CVE fix.

Maybe underlying issue is that TabUI is destroyed on pressing the button when it shouldn't?

Guidou, do you know where's the code which is executed after the button is clicked? I'm having troubles finding it.


### il...@google.com (2021-01-13)

Also, interesting observations: there are two sets of TabSharingUI created when presentation is started. In the old way, once the presentation is stopped of switched other, only one TabSharingUI is destroyed, but with the CVE fix, both of them are.

So, it seems that there may be two TabSharingUI instances, there only one is actually responsible for stopping the presentation, but the one being destroyed on the button click is the other one.

### il...@google.com (2021-01-13)

When presentation starts, we create TabSharingUIView here:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/media/webrtc/desktop_capture_access_handler.cc;l=449;drc=7ccffaf0933ccc647c744bf66971bcf5f33a676a

Then on the button press we create a second TabSharingUIView here:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/media/webrtc/desktop_capture_access_handler.cc;l=594;drc=7ccffaf0933ccc647c744bf66971bcf5f33a676a

Then, the old one is destroyed. But at that point the presentation stop is called because TabSharingUiView now calls for it in destructor.
The destruction happens here: https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/media/media_stream_ui_proxy.cc;l=200;drc=7ccffaf0933ccc647c744bf66971bcf5f33a676a

### il...@google.com (2021-01-13)

After offline discussion we decided to revert the CL on trunk and M88 for now.

We will work on a new fix and hopefully it should make it to M88 before RC for stable.

### sr...@google.com (2021-01-13)

Adding RBS for M88 for tracking purpose. 

### ac...@chromium.org (2021-01-13)

We (the LTS team) also picked this fix for 86-LTS (go/4240-merge). Do we also need to revert this there?

### il...@google.com (2021-01-13)

The revert introduces the CVE back. I don't know which we prefer more, a broken UI for some users with workarounds or a CVE.
We are fine with it on M88 because we will fix it later, but I'm not sure about LTS. Would you be able to pick the fix later also?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d829cb6e268cb91aaebbe5836db7a9a804174865

commit d829cb6e268cb91aaebbe5836db7a9a804174865
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Wed Jan 13 19:57:48 2021

Revert "Minor UI logic changes to prevent a UAF bug when starting tab capture."

This reverts commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f.

Reason for revert: Broke "Share this tab instead" button.

Original change's description:
> Minor UI logic changes to prevent a UAF bug when starting tab capture.
>
> See discussion in crbug 1155426 for details. Changes:
>
> MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
> OnStarted().
>
> TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.
>
> Bug: 1155426
> Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
> Reviewed-by: Guido Urdaneta <guidou@chromium.org>
> Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
> Commit-Queue: Yuri Wiitala <miu@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#835736}

TBR=miu@chromium.org,guidou@chromium.org,marinaciocea@chromium.org,chromium-scoped@luci-project-accounts.iam.gserviceaccount.com

# Not skipping CQ checks because original CL landed > 1 day ago.

TBR=marinaciocea@chromium.org

Bug: 1155426, 1165947
Change-Id: I9df25d596cb4df7b5e98db78f019b2665b01e8b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2627848
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#843148}

[modify] https://crrev.com/d829cb6e268cb91aaebbe5836db7a9a804174865/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/d829cb6e268cb91aaebbe5836db7a9a804174865/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fa98b4ac3068c24c701cd90ee40dfb6a9d128054

commit fa98b4ac3068c24c701cd90ee40dfb6a9d128054
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Wed Jan 13 20:03:36 2021

Revert "Minor UI logic changes to prevent a UAF bug when starting tab capture."

This reverts commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f.

Reason for revert: Broke "Share this tab instead" button.

Original change's description:
> Minor UI logic changes to prevent a UAF bug when starting tab capture.
>
> See discussion in crbug 1155426 for details. Changes:
>
> MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
> OnStarted().
>
> TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.
>
> Bug: 1155426
> Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
> Reviewed-by: Guido Urdaneta <guidou@chromium.org>
> Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
> Commit-Queue: Yuri Wiitala <miu@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#835736}

TBR=miu@chromium.org,guidou@chromium.org,marinaciocea@chromium.org,chromium-scoped@luci-project-accounts.iam.gserviceaccount.com

# Not skipping CQ checks because original CL landed > 1 day ago.

TBR=marinaciocea@chromium.org

Bug: 1155426, 1165947
Change-Id: I9df25d596cb4df7b5e98db78f019b2665b01e8b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2627849
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4387@{#5}
Cr-Branched-From: 7a47a61b26f401e0c3bf5d1720626d636657d790-refs/heads/master@{#842744}

[modify] https://crrev.com/fa98b4ac3068c24c701cd90ee40dfb6a9d128054/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/fa98b4ac3068c24c701cd90ee40dfb6a9d128054/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b3eeefe7f5149cc34c375e54421850e9d4860a9c

commit b3eeefe7f5149cc34c375e54421850e9d4860a9c
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Thu Jan 14 17:36:53 2021

Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

MediaStreamUI and contents::MediaStreamUI: Now has SetStopCallback method which is used to remove the
stop callback when MediaStreamUI is replaced on switching the tab source.

Bug: 1155426, 1166260
Change-Id: I0482c82f921fdc2f20931ab83458deec2f2da30c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2629278
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Mike Pinkerton <pinkerton@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#843598}

[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/media/webrtc/media_stream_capture_indicator.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/content/browser/renderer_host/media/media_stream_ui_proxy_unittest.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.h
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/content/browser/renderer_host/media/media_stream_ui_proxy.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/media/webrtc/media_stream_capture_indicator.h
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/content/public/browser/media_stream_request.h
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/ui/views/screen_capture_notification_ui_views.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate_unittest.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/weblayer/browser/webrtc/media_stream_manager.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/ui/screen_capture_notification_ui_stub.cc
[modify] https://crrev.com/b3eeefe7f5149cc34c375e54421850e9d4860a9c/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73825c6cca2bcad158c2913e79e5a24963fb95bb

commit 73825c6cca2bcad158c2913e79e5a24963fb95bb
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Thu Jan 14 17:38:21 2021

Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

MediaStreamUI and contents::MediaStreamUI: Now has SetStopCallback method which is used to remove the
stop callback when MediaStreamUI is replaced on switching the tab source.

TBR=guidou@chromium.org,yfriedman@chromium.org,pinkerton@chromium.org

Bug: 1155426, 1166260
Change-Id: I0482c82f921fdc2f20931ab83458deec2f2da30c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2628956
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Cr-Commit-Position: refs/branch-heads/4388@{#7}
Cr-Branched-From: 1fc9246ae2ea04bc1ea6f9a114d2b84ea7e0c439-refs/heads/master@{#843296}

[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/media/webrtc/media_stream_capture_indicator.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/content/browser/renderer_host/media/media_stream_ui_proxy_unittest.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.h
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/content/browser/renderer_host/media/media_stream_ui_proxy.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/media/webrtc/media_stream_capture_indicator.h
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/content/public/browser/media_stream_request.h
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/ui/views/screen_capture_notification_ui_views.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate_unittest.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/weblayer/browser/webrtc/media_stream_manager.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/ui/screen_capture_notification_ui_stub.cc
[modify] https://crrev.com/73825c6cca2bcad158c2913e79e5a24963fb95bb/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.cc


### gu...@chromium.org (2021-01-14)

[Empty comment from Monorail migration]

### il...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### sr...@google.com (2021-01-14)

Merge approved for M88 branch:4324 please merge this change to M88 branch after the verification on canary ( build M89.0.4388.4 goes out and verify crash data for 8 hrs of canary.

### ac...@chromium.org (2021-01-14)

86-LTS can merge the fix later. We'll hold off on the revert until the new security fix is available

### sr...@google.com (2021-01-14)

+benmason@ to help trigger a desktop stable RC once the merge lands for M88. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/048650d034dd02235529b0cc18c904e17a82ce49

commit 048650d034dd02235529b0cc18c904e17a82ce49
Author: Ilya Nikolaevskiy <ilnik@chromium.org>
Date: Fri Jan 15 09:43:54 2021

Merge to M88: Minor UI logic changes to prevent a UAF bug when starting tab capture.

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

MediaStreamUI and contents::MediaStreamUI: Now has SetStopCallback method which is used to remove the
stop callback when MediaStreamUI is replaced on switching the tab source.

TBR=guidou@chromium.org,yfriedman@chromium.org,pinkerton@chromium.org

Bug: 1155426, 1166260
Change-Id: I0482c82f921fdc2f20931ab83458deec2f2da30c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2629311
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1761}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/media/webrtc/media_stream_capture_indicator.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/content/browser/renderer_host/media/media_stream_ui_proxy_unittest.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.h
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/content/browser/renderer_host/media/media_stream_ui_proxy.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/media/webrtc/media_stream_capture_indicator.h
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/content/public/browser/media_stream_request.h
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/ui/views/screen_capture_notification_ui_views.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate_unittest.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/weblayer/browser/webrtc/media_stream_manager.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/ui/screen_capture_notification_ui_stub.cc
[modify] https://crrev.com/048650d034dd02235529b0cc18c904e17a82ce49/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.cc


### il...@google.com (2021-01-15)

benmason@, It has landed, please trigger the build.

### sr...@google.com (2021-01-19)

can we close this bug? 

### il...@chromium.org (2021-01-19)

There's still an open question of what to do with M87. Shall we merge a fix just in case there will be a new respin or something?

### ad...@google.com (2021-01-19)

M88 stable is going out today, and there's unlikely to be any new M87 release unless something very weird happens. I don't think it would be worth the effort to pre-emptively merge back to M87.

### ad...@google.com (2021-01-19)

My mistake: there's going to be a ChromeOS M87 refresh tomorrow. Please co-ordinate with marinakz@ if it's merited to fit this in - it probably is.

### ma...@google.com (2021-01-19)

Adding cindyb@ to confirm if we can still merge it to M87. I think we already have a build going

### ci...@chromium.org (2021-01-19)

A new version of M87 started two hours ago, a release record to be created and tested tomorrow.

### ci...@chromium.org (2021-01-19)

Labels suggest this was already merged, but I do not see the CL for 4280 nor can I find it in diff.

### ad...@google.com (2021-01-19)

This issue has a complex history. The original security bug was merged (including into M87) but this caused a functional regression, so a revised fix landed. I suspect this latter fix hasn't been merged to M87. AIUI this means that the "share this tab instead button" won't work in the release you're making.

### ci...@chromium.org (2021-01-19)

Thanks for the clarification. This is the last stable for M87 and we are pushing to get it rolled out quickly, we have critical devices running stale versions.  Looks like in #55 you are willing to accept a version of M87 without it? 

### ad...@google.com (2021-01-19)

Well, I'm not really the right person to comment on that. With either the old fix or the new fix, the security vulnerability is resolved. The problem with the old fix is a functional problem which apparently was causing quite a lot of support calls.

My comment in https://crbug.com/chromium/1155426#c55 relates to the fact that M88 stable went out today except on ChromeOS.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/becccd83bb0ef76913666588d0fa3f2835afbd7e

commit becccd83bb0ef76913666588d0fa3f2835afbd7e
Author: Jana Grill <janagrill@google.com>
Date: Wed Jan 20 13:04:16 2021

Revert "Minor UI logic changes to prevent a UAF bug when starting tab capture."

This reverts commit c4e038ad8b00d06264b67389ced7786c30a09562.

Reason for revert: The fix breaks the "Share this tab instead" button.

Original change's description:
> Minor UI logic changes to prevent a UAF bug when starting tab capture.
>
> See discussion in crbug 1155426 for details. Changes:
>
> MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
> OnStarted().
>
> TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.
>
> Bug: 1155426
> Change-Id: I392fba38118ce51744ba36b4dec19ebfe39f1fbe
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2581028
> Reviewed-by: Guido Urdaneta <guidou@chromium.org>
> Reviewed-by: Marina Ciocea <marinaciocea@chromium.org>
> Commit-Queue: Yuri Wiitala <miu@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#835736}
> (cherry picked from commit 3ca3d70c7af50aa7024a351f70b289b8ccdc4a5f)
>
>
> TBR=miu@chromium.org
>
> (cherry picked from commit de6de32e9733ae62d6bcd210691bb2a0577a8662)
>
> Change-Id: Ic0e8bb5d92aec527855dbe5771952cc4a84b2452
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2610364
> Reviewed-by: Yuri Wiitala <miu@chromium.org>
> Commit-Queue: Yuri Wiitala <miu@chromium.org>
> Cr-Original-Commit-Position: refs/branch-heads/4280@{#1998}
> Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617560
> Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
> Cr-Commit-Position: refs/branch-heads/4240@{#1501}
> Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

Bug: 1155426
Change-Id: I9ef1a732c106a85be6df57907b820fe0b4c441c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2632655
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1523}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/becccd83bb0ef76913666588d0fa3f2835afbd7e/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/becccd83bb0ef76913666588d0fa3f2835afbd7e/chrome/browser/media/webrtc/media_stream_capture_indicator.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d485dfd93a8ee810542358e7ff5e308c3e98e79d

commit d485dfd93a8ee810542358e7ff5e308c3e98e79d
Author: Jana Grill <janagrill@google.com>
Date: Wed Jan 20 15:30:06 2021

Merge to LTS-M86: Minor UI logic changes to prevent a UAF bug when starting tab capture.

Cherry-picked from:
https://chromium-review.googlesource.com/c/chromium/src/+/2629311

See discussion in crbug 1155426 for details. Changes:

MediaStreamCaptureIndicator::UIDelegate: Ignore multiple calls to
OnStarted().

TabSharingUIViews: Unconditionally execute clean-up tasks in destructor.

MediaStreamUI and contents::MediaStreamUI: Now has SetStopCallback method which is used to remove the
stop callback when MediaStreamUI is replaced on switching the tab source.

Bug: 1155426, 1166260
Change-Id: I9335e7df984e0b667b396436e16066dd1eee88cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2636396
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1524}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/media/webrtc/media_stream_capture_indicator.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/content/browser/renderer_host/media/media_stream_ui_proxy_unittest.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.h
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/content/browser/renderer_host/media/media_stream_ui_proxy.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/media/webrtc/media_stream_capture_indicator.h
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/content/public/browser/media_stream_request.h
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.h
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/ui/views/screen_capture_notification_ui_views.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate_unittest.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/weblayer/browser/webrtc/media_stream_manager.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/ui/screen_capture_notification_ui_stub.cc
[modify] https://crrev.com/d485dfd93a8ee810542358e7ff5e308c3e98e79d/chrome/browser/chromeos/ui/screen_capture_notification_ui_chromeos.cc


### il...@chromium.org (2021-01-20)

 cindyb@,
You really only need to pick up this CL [1]. It applies mostly undoes the revert before it.
Here's a cherry-pick created and dry-running for your convenience, land it, if you have an approval: 
https://chromium-review.googlesource.com/c/chromium/src/+/2640536

[1] https://chromium.googlesource.com/chromium/src/+/b3eeefe7f5149cc34c375e54421850e9d4860a9c

### ja...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1155426?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054066)*
