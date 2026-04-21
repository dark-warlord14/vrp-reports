# Compromised renderer can control your mouse and escape sbx

| Field | Value |
|-------|-------|
| **Issue ID** | [370856871](https://issues.chromium.org/issues/370856871) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views |
| **Platforms** | Windows |
| **Chrome Version** | 129.0.0.0 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2024-10-02 |
| **Bounty** | $50,000.00 |

## Description

# Steps to reproduce the problem

1. git apply patch.diff
2. Compile a.cpp into a.exe and put a.exe to the http server folder
3. python3 -m http.server
4. visit exp.html and click the button then you will see your mouse automatically click the exe in the download bubble and execute it.

# Problem Description

startDragging[1] is a mojo ipc interface that can be called at will by the compromised renderer. In Windows, if the user passes arbitrary coordinates and kTouch as the last parameter[2], as can be seen from the code[3][4] below, startDragging will control the user's mouse to click the coordinates using the windows api ui::SendMouseEvent, regardless of whether the coordinates are in the Chromium window.

```
  StartDragging(DragData drag_data,  ---------------------[1]
                AllowedDragOperations operations_allowed,
                skia.mojom.BitmapN32? image,
                gfx.mojom.Vector2d cursor_offset_in_dip,
                gfx.mojom.Rect drag_obj_rect_in_dip,
                DragEventSourceInfo event_info);----------[2]
struct DragEventSourceInfo {
  gfx.mojom.Point location;
  ui.mojom.DragEventSource source;
};

void DesktopWindowTreeHostWin::StartTouchDrag(gfx::Point screen_point) { -----------------[3]
  // Send a mouse down and mouse move before do drag drop runs its own event
  // loop. This is required for ::DoDragDrop to start the drag.
  ui::SendMouseEvent(screen_point, MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE);
  ui::SendMouseEvent(screen_point, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE);
  in_touch_drag_ = true;
}

void DesktopWindowTreeHostWin::FinishTouchDrag(gfx::Point screen_point) { --------------------[4]
  if (in_touch_drag_) {
    in_touch_drag_ = false;
    ui::SendMouseEvent(screen_point, MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE);
  }
}

```

exploit:
There are many ways to exploit this vulnerability, such as allowing the browser to grant arbitrary user permissions. The most destructive way to exploit is to let the mouse directly click on the downloaded exe file in download bubble to execute it, causing arbitrary code execution outside the sandbox.

# Additional Comments

bisect information: This bug is introduced by: <https://chromium-review.googlesource.com/c/chromium/src/+/3069450>

# Summary

Compromised renderer can control your mouse and escape sbx

# Custom Questions

#### Type of crash:

#### Crash state:

#### Reporter credit:

Micky

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [a.cpp](attachments/a.cpp) (text/x-c++src, 175 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 794.0 KB)
- [exp.html](attachments/exp.html) (text/html, 1.4 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.8 KB)
- [biggerwindow.mp4](attachments/biggerwindow.mp4) (video/mp4, 5.5 MB)
- [smallwindow.mp4](attachments/smallwindow.mp4) (video/mp4, 8.1 MB)
- deleted (application/octet-stream, 0 B)
- [exp_show.mp4](attachments/exp_show.mp4) (video/mp4, 7.4 MB)
- [exp.html](attachments/exp.html) (text/html, 2.8 KB)
- [a.cpp](attachments/a.cpp) (text/x-c++src, 175 B)
- [aaa.html](attachments/aaa.html) (text/html, 586 B)
- [exploit.html](attachments/exploit.html) (text/html, 865 B)
- [new_patch.diff](attachments/new_patch.diff) (text/x-diff, 3.5 KB)
- [exploit_record.mp4](attachments/exploit_record.mp4) (video/mp4, 966.0 KB)
- [exploit.mp4](attachments/exploit.mp4) (video/mp4, 12.7 MB)

## Timeline

### hc...@google.com (2024-10-02)

I am not able to exactly reproduce the bug; I can recreate that with that code patch on HEAD the mouse pointer goes all over the place (and definitely outside the window of browser, into other applications).

### hc...@google.com (2024-10-02)

some of my repro attempts (tried a few more times, couldn't get the click on the download)

### da...@google.com (2024-10-02)

There are several possible mitigations, all involving validating the params to DesktopWindowTreeHostWin::StartTouchDrag, or perhaps DesktopDragDropClientWin::StartDragAndDrop. We could validate that the screen point is in the source window, though it doesn't sound like that would block exploits involving generating a click inside the browser window. Perhaps we could use Env::GetLastPointerPoint() to see if the user really had a recent touch event at (or near?) that location. That's assuming the browser sees all events happening in the renderer. Conversely, perhaps blink could do this verification?

### es...@chromium.org (2024-10-02)

Re #4: we can't trust Blink to do the validation because in the exploitation scenario, the renderer (including Blink) would be compromised. I don't know much about how input works but I would imagine that the browser process knows about all the input events and passes them along to the renderer, so the browser should be able to validate that the drag event corresponds to a real input event?

### da...@google.com (2024-10-02)

I hope the browser can validate the drag event. I just remember some complexities involving the legacy hwnd stuff.

### da...@google.com (2024-10-02)

Another possibility is that we could send right mouse button events instead of left mouse button events when starting and finishing drags, if Windows is OK with that. Right mouse button down and up should be less dangerous.

Unfortunately, I can't get the touch tabstrip enabled on my Win 11 convertible, which is how I used to test all this.

### rb...@chromium.org (2024-10-03)

To input component for input events experts like @mustaq to weigh in.

I agree that in theory we should be able to have the browser process restrict this. But it's possible that a bigger re-architecture may be necessary to ensure compromised renderers can never spoof any input that would impact a frame or site outside their own.

### ha...@gmail.com (2024-10-03)

Re #3:
Thanks for your screen recording. From your screen recording, I found two problems in the HTML file:
1. Since I clicked the button to start the download operation, if I clicked too quickly and the download was not completed, the download bubble would not appear. To solve this problem, I set a pressed progress bar. Now we need to press the button and wait for the progress bar to be full after 1500ms before releasing it.
2. The coordinates in the HTML did not take into account the window size. I modified the HTML and now the click position will adapt to the window size.

Steps to reproduce the problem
1. git apply patch.diff
2. Compile a.cpp into a.exe and put a.exe to the http server folder
3. python3 -m http.server
4. visit exp.html and Press the button and wait for the progress bar to be full then you will see your mouse automatically click the exe in the download bubble and execute it.( The successful rate is nearly 50%)

I also attach a screen recording in the following files. If you still can't reproduce, please let me know. thanks!

### ha...@gmail.com (2024-10-03)

Another thing to note is that if you just opened the browser, you need to click the upper left corner to refresh the page as shown in the screen recording, or close the banner that Chromium is not your default browser. If you do not do this, the vertical axis coordinates of the download will not match. 
This operation is not necessary in actual attacks, because ***only the first tab*** opened after the browser is started will display this banner. Most pages are not the first page opened after the browser is started. In addition, the attacker can call windows.open to open a new tab, and the position value obtained from the new tab is correct.

### sk...@google.com (2024-10-03)

I wonder if we still need to send mouse events for touch dragging to work. May it's not necessary anymore?

Seems like the browser side should be able to do some minimal amount of validation here:

. Is a touch point down (or was down really recently)?
. Are the coordinates valid?

### pe...@google.com (2024-10-03)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### hc...@google.com (2024-10-03)

Setting foundin to extended stable, as this has been around for a while.

### ha...@gmail.com (2024-10-03)

Sorry, I find the exp.html in the comment 9 is the old one. Here is the update one

### da...@google.com (2024-10-03)

I'm reasonably sure the mouse events are needed - ::DoDragDrop is not touch aware, and folks at Microsoft didn't think it would ever be fixed. There is a new Drag Drop WinRT API, but when I tried it, it wasn't really ready for non UWP apps.

I think checking that there is a recent touch event at the location is a good approach.

### pe...@google.com (2024-10-04)

Setting milestone because of s2 severity.

### ha...@gmail.com (2024-10-07)

Update: After furture investigation, this bug can be triggered without any user interaction. I test in my win11 and win10 computer. The successful rate is nearly 99%.
Steps to reproduce the problem
1.git apply new_patch.diff.
2.Compile a.cpp into a.exe and put a.exe,aaa.html and exploit.html to the http server folder.
3.python3 -m http.server 8000
4.python3 -m http.server 8001 (We need two http server to create a cross-site environment.)
5.open chromium and if there is a prompt to set Chromium as your default browser, close this prompt.
6.visit exploit.html.
7.Wait and then you will see your mouse automatically click the exe in the download bubble and execute it.
8.If the exploit fail, close your chromium and repeate step 5-7.

### mu...@chromium.org (2024-10-07)

> Perhaps we could use Env::GetLastPointerPoint() to see if the user really had a recent touch event at (or near?) that location. That's assuming the browser sees all events happening in the renderer.

[davidbienvenu@google.com](mailto:davidbienvenu@google.com): Worth a try because I am pretty sure the browser sees all events. The risk there seems to be possibly getting confused with events from multiple pointers (mouse+pen+touch together or multitouch) but the does not sound bad to me because in this case the user had placed one pointer over (or near) the fake click.

An alternate (or even additional) fix could be that the browser won't ever set [in\_touch\_drag\_](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_window_tree_host_win.h;drc=f2bdeab65d21b19840ac5cb2801950cfb0dcb2f2;l=354-360) to `true` if the last touch-start event position seen in [DesktopWindowTreeHostWin::HandleTouchEvent](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_window_tree_host_win.cc;drc=4b44bd63028a5aa82976dc4d7ed51cb78cbc6891;l=1135) is not equal (or nearby). I think checking for "nearby" is needed only if in Windows we allow touch-dragging without a long-press.

### mu...@chromium.org (2024-10-07)

[davidbienvenu@google.com](mailto:davidbienvenu@google.com): We already agreed that a fix in Blink won't fix the vulnerability. Do you see an appropriate non-Blink component for this bug?

### da...@google.com (2024-10-07)

Chromium | Internal | Views  | Desktop is a possibility, as long as the bug access will still be locked down - perhaps the Vulnerability Type enforces that?

### aj...@chromium.org (2024-10-07)

(RE comment 20 - yep - this stays locked down)

### da...@google.com (2024-10-11)

Jesse, if you haven't started on this, I can take it back. 

### je...@google.com (2024-10-11)

I haven't started, assigning back to you : )

### da...@google.com (2024-10-12)

While I work on validating the touch drag coordinates, I have a CL out to switch to using right mouse button down and up instead of left mouse button down and up.  That should be less exploitable. I manually  tested drag in the touch tab UI and it works. This required hardcoding touch_ui() because tablet mode detection does not seem to be working, at least as far as automatically using the touch tab UI is concerned, and probably in general on Win 11.

### ha...@gmail.com (2024-10-16)

Hello, friendly ping, is there any update? Thanks!

And based on comment 17, is it eligible for a S1 severity bug?(Compromised renderer can escape sandbox without any user interaction)

### da...@google.com (2024-10-16)

I'm working on an issue with the CL I mentioned in #24. I'll leave the second question for the people responsible for those decisions.

### ha...@gmail.com (2024-10-16)

Thank you!

### ap...@google.com (2024-10-18)

Project: chromium/src  

Branch: main  

Author: David Bienvenu <[davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5927282>

win: tweaks to touch drag.

---


Expand for full commit details
```
win: tweaks to touch drag.

Verify that mouse cursor is in the drag source window.

Tested manually.

Low-Coverage-Reason: HARD_TO_TEST
Bug: 40312079, 370856871
Change-Id: I800e915f566d63354e4e1d1e1f7edd79200f7553
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5927282
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1370869}

```

---

Files:

- M `ui/views/views_features.cc`
- M `ui/views/views_features.h`
- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: 69eb90b5672be6a32ddf6f1b3a3ab4bb667b0d3b  

Date:  Fri Oct 18 22:45:38 2024


---

### ha...@gmail.com (2024-10-18)

Hello, thanks for the fix! It seems has a small question,  drag_drop_in_progress_ will never set to True if source is not ui::mojom::DragEventSource::kTouch. Maybe it should has an else condition to set  drag_drop_in_progress_ to True?

### ap...@google.com (2024-10-18)

Project: chromium/src  

Branch: main  

Author: Dana Fried <[dfried@google.com](mailto:dfried@google.com)>  

Link:      <https://chromium-review.googlesource.com/5944060>

Revert "win: tweaks to touch drag."

---


Expand for full commit details
```
Revert "win: tweaks to touch drag."

This reverts commit 69eb90b5672be6a32ddf6f1b3a3ab4bb667b0d3b.

Reason for revert: Breaks tests on CI

Bug: 374385590

Original change's description:
> win: tweaks to touch drag.
>
> Verify that mouse cursor is in the drag source window.
>
> Tested manually.
>
> Low-Coverage-Reason: HARD_TO_TEST
> Bug: 40312079, 370856871
> Change-Id: I800e915f566d63354e4e1d1e1f7edd79200f7553
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5927282
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1370869}

Bug: 40312079, 370856871
Change-Id: Iddc412d90f747af20e049f90267f2c26594752d2
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5944060
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Dana Fried <dfried@google.com>
Commit-Queue: Dana Fried <dfried@google.com>
Cr-Commit-Position: refs/heads/main@{#1370900}

```

---

Files:

- M `ui/views/views_features.cc`
- M `ui/views/views_features.h`
- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: aaf1527d61da6b1432631902f7d95cba024d9e61  

Date:  Fri Oct 18 23:57:47 2024


---

### ap...@google.com (2024-10-21)

Project: chromium/src  

Branch: main  

Author: David Bienvenu <[davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5943487>

Reland "win: tweaks to touch drag."

---


Expand for full commit details
```
Reland "win: tweaks to touch drag."

This is a reland of commit 69eb90b5672be6a32ddf6f1b3a3ab4bb667b0d3b
with a fix for the test failure, which is to move the setting
of drag_drop_in_progress_ so that it's set for both the touch
and non-touch case.

Original change's description:
> win: tweaks to touch drag.
>
> Verify that mouse cursor is in the drag source window.
>
> Tested manually.
>
> Low-Coverage-Reason: HARD_TO_TEST
> Bug: 40312079, 370856871
> Change-Id: I800e915f566d63354e4e1d1e1f7edd79200f7553
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5927282
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1370869}

Low-Coverage-Reason: HARD_TO_TEST
Bug: 40312079, 370856871, 374385590
Change-Id: I387757524615c3b3fe4dd6865825331db5bee44e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5943487
Reviewed-by: Dana Fried <dfried@chromium.org>
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1371525}

```

---

Files:

- M `ui/views/views_features.cc`
- M `ui/views/views_features.h`
- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: 5398c8d04355cd24ced9bc1ff8900ccb5540aea9  

Date:  Mon Oct 21 18:16:39 2024


---

### ha...@gmail.com (2024-10-22)

Thanks for your fix! In my test, Exploitation is completely blocked.

### da...@google.com (2024-10-23)

This is fixed on trunk. I'm working on getting the fix cherry picked to m131 and also on a follow on fix to ensure that the drag start corresponds to a nearby touch event. 

### da...@google.com (2024-10-23)

Requesting approval to land https://chromium-review.googlesource.com/c/chromium/src/+/5952499 for m131.

This fixes a security issue. I've tested it on Canary build. The fix is behind a feature/kill switch.

### pe...@google.com (2024-10-23)

Merge review required: M131 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### da...@google.com (2024-10-23)

1. It's a security vulnerability fix
2.  https://chromium-review.googlesource.com/c/chromium/src/+/5952499
3. yes
4. No, the feature (touch drag and drop) launched a couple years ago.


### pg...@google.com (2024-10-24)

This is a UI impacting change, but we are still on M131 beta and I dont see anything relevant on canary

Merge approved for M131 beta! Please merge to branch 6778 at your earliest convenience to get this change into the next beta release!

### ap...@google.com (2024-10-24)

Project: chromium/src  

Branch: refs/branch-heads/6778  

Author: David Bienvenu <[davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5952499>

Reland "win: tweaks to touch drag."

---


Expand for full commit details
```
Reland "win: tweaks to touch drag." 
 
This is a reland of commit 69eb90b5672be6a32ddf6f1b3a3ab4bb667b0d3b 
with a fix for the test failure, which is to move the setting 
of drag_drop_in_progress_ so that it's set for both the touch 
and non-touch case. 
 
Original change's description: 
> win: tweaks to touch drag. 
> 
> Verify that mouse cursor is in the drag source window. 
> 
> Tested manually. 
> 
> Low-Coverage-Reason: HARD_TO_TEST 
> Bug: 40312079, 370856871 
> Change-Id: I800e915f566d63354e4e1d1e1f7edd79200f7553 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5927282 
> Reviewed-by: Scott Violet <sky@chromium.org> 
> Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1370869} 
 
(cherry picked from commit 5398c8d04355cd24ced9bc1ff8900ccb5540aea9) 
 
Low-Coverage-Reason: HARD_TO_TEST 
Bug: 40312079, 370856871, 374385590 
Change-Id: I387757524615c3b3fe4dd6865825331db5bee44e 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5943487 
Reviewed-by: Dana Fried <dfried@chromium.org> 
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1371525} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5952499 
Reviewed-by: Robert Liao <robliao@chromium.org> 
Commit-Queue: David Bienvenu <davidbienvenu@google.com> 
Cr-Commit-Position: refs/branch-heads/6778@{#781} 
Cr-Branched-From: b21671ca172dcfd1566d41a770b2808e7fa7cd88-refs/heads/main@{#1368529}

```

---

Files:

- M `ui/views/views_features.cc`
- M `ui/views/views_features.h`
- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: 7e1b3bdbd19a2f7fc120248675d690ac39d8c01b  

Date:  Thu Oct 24 17:54:56 2024


---

### ha...@gmail.com (2024-11-25)

Hello, this is a video of the vulnerability reproducing on my computer(based on comment 17). It can be reproduced stably regardless of the size of the Chromium window. You can see in the exploit record, it just need a compromised renderer and don't need any other condition. If you encounter a problem that cannot be reproduced during the evaluation, please let me know. Thank you!

### sp...@google.com (2024-11-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High-quality report of security issue that can result in a sandbox escape with multiple preconditions / mitigations to exploit


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-26)

Congratulations Micky! Thank you for this clever finding and impactful report.

While a sandbox escape is able to be achieved, there are some mitigations in play that limit the exploitability, including getting the executable on the machine and past any AV and any other download protections, this is a somewhat noisy attack scenario and would be apparent to the user during the course of exploitation, and not fully reliably exploitable, not just by us but in a real world attack scenario with timing and resolution preconditions.

However, we do see this as an impactful issue that could result in a potential for user harm, and are happy to reward it accordingly. Thank you for your excellent efforts on this issue and reporting it to us – nice work!

### ha...@gmail.com (2024-11-27)

Thanks for the reward, cheers!

I didn't consider the UAC and AV issuesand and any other download protections, because Windows' UAC protection seems to be very weak. My computer is fully running with UAC, and the exe I compiled and downloaded can be fully executed when I open it. In fact, even if there is a UAC pop-up window, since the attacker can control the mouse, the UAC pop-up window can be easily bypassed by clicking the continue button. However, it's true that the exploit would be apparent to the user during the course of exploitation.

And here is a small request, is it this bug eligible for a high seveiry? Because I want write a blog after this issue is fully disclosed next year(14 weeks later). Medium severity seems less convincing. And In addtion, will this bug eligible to join the top researchers calculation for 2024?

It seems like a lot of questions, but thank you for your patience in replying!

### am...@chromium.org (2024-11-27)

Cheers to you, Micky!
A compromised renderer alone usually takes a critical severity bug, such as a non-mitigated sbx down to a high severity, but given the other mitigations here, I think medium severity is appropriate in our threat model.
I do, however, think that given the impact people will very much be interested in this issue regardless of the severity we assign and a blog post, once this issue has been disclosed next year will be very interesting. Please feel to comment here at that time with a link if you would like to include it on our bug write-ups in the Chrome VRP News and FAQ. [1]

Yes, this reward will be included in the Chrome VRP leaderboard calculations for 2024.

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#interesting-security-bug-write_ups>

### ha...@gmail.com (2024-11-28)

Thnank you! And thanks for the reply!

### pe...@google.com (2025-01-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High-quality report of security issue that can result in a sandbox escape with multiple preconditions / mitigations to exploit

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/370856871)*
