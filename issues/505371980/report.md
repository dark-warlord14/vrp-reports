# heap-buffer-overflow in TabDragController::AttachToNewContext

| Field | Value |
|-------|-------|
| **Issue ID** | [505371980](https://issues.chromium.org/issues/505371980) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 149.0.7791.0 |
| **Reporter** | xp...@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2026-04-22 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Install extension to Chrome.
2. Drag chrome://whats-new/ tab out (titled "What's new").

# Problem Description

heap-buffer-overflow in TabDragController::AttachToNewContext. Please check comments for RCA and summary of the issue + patch.

# Summary

heap-buffer-overflow in TabDragController::AttachToNewContext

# Custom Questions

#### Type of crash:

browser

#### Reporter credit:

Sven @svn\_dy

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: Yes \

## Attachments

- [background.js](attachments/background.js) (text/javascript, 113 B)
- [inject.js](attachments/inject.js) (text/javascript, 125 B)
- [manifest.json](attachments/manifest.json) (application/json, 336 B)
- [asan.txt](attachments/asan.txt) (text/plain, 11.9 KB)
- [whats-new-asan.patch](attachments/whats-new-asan.patch) (text/x-diff, 876 B)
- [reproduction_hbo.mp4](attachments/reproduction_hbo.mp4) (video/mp4, 9.6 MB)
- [win_dbg_trace.txt](attachments/win_dbg_trace.txt) (text/plain, 13.4 KB)
- [Fri Jun 05 2026 16:26:16 GMT-0400 (Eastern Daylight Time).png](attachments/Fri Jun 05 2026 16_26_16 GMT-0400 (Eastern Daylight Time).png) (image/png, 275.2 KB)

## Timeline

### xp...@gmail.com (2026-04-22)

# Root cause analysis:

The reproduction begins on the install of the extension. `chrome://whats-new` is opened and using an i-frame from inside the webpage, the extension can postMessage the parent window and activate browser commands that are currently supported.

```
// Command id 12 = kOpenAISettings (chrome://settings/ai)
setInterval(() => {
   parent.postMessage({ data: { event: 'browser_command', commandId: 12, clickInfo: {}}}, '*');
}, 10);

```

That browser command 12, `kOpenAISettings`, repeatedly re-selects the existing `chrome://settings/ai` tab. The User-visible effect: the strip keeps snapping back to chrome://settings/ai.

The user clicks back to `chrome://whats-new` and starts dragging the tab out. At drag start, `TabDragController::Init` creates a snapshot of the dragged tab and is set into `drag_data_.tab_drag_data_` [Code:](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=bbf00ace04d1e5bb9c780c96506a599012e2dfef;l=494)

```
  for (TabSlotView* dragging_view : dragging_views) {
    ref->drag_data_.tab_drag_data_.emplace_back(source_context_, dragging_view);
    if (dragging_view->GetTabSlotViewType() ==
        TabSlotView::ViewType::kTabGroupHeader) {
      ref->drag_data_.dragging_groups.insert(*dragging_view->group());
    }
  }

```

[`AttachImpl`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=b7aa90cd3e2def886c543c9ff7e86c880f802e8d;l=1426) calls [`ResetSelection`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=b7aa90cd3e2def886c543c9ff7e86c880f802e8d;l=1971), which rebuilds the tab strip’s active/selected tab state from the `WebContents` recorded in `drag_data_`. At this point, the drag subsystem still identifies chrome://whats-new as the dragged tab.

During the attached-drag phase, the repeated `kOpenAISettings` execution keeps going through the settings re-open tab path and eventually calls [ActivateTabAt()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;drc=c7811f06445b48c0a7d58db99101c2428e8d7d09;l=969) on the existing chrome://settings/ai tab.

**That changes the original `TabStripModel`’s live active/selected tab state during the drag, separate from the drag session itself.** `TabDragController` had already recorded the dragged tab in [`drag_data_.tab_drag_data_`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=bbf00ace04d1e5bb9c780c96506a599012e2dfef;l=494) at drag start, and it only re-syncs the tab strip state from that snapshot at specific points via [`ResetSelection()`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=bbf00ace04d1e5bb9c780c96506a599012e2dfef;l=1971).

There is no continuous check to keep those in sync as the drag-time observer [`DraggedTabsClosedTracker`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=bbf00ace04d1e5bb9c780c96506a599012e2dfef;l=316) handles tab removal and replacement, but not selection changes. The result is that `drag_data_` still points to the originally dragged `chrome://whats-new`'s `WebContents`, while `attached_context_->GetTabStripModel()->selection_model()` now points to `chrome://settings/ai`. That mismatch is what later causes the detach/attach path to operate on different tab identities.

The user drags `chrome://whats-new` far enough out of the original window that a new window is made.

[Code:](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=bbf00ace04d1e5bb9c780c96506a599012e2dfef;l=1000)

```
TabDragController::Liveness TabDragController::DragBrowserToNewTabStrip(...)
   
  [...]
  if (!target_context) {
    return DetachIntoNewBrowserAndRunMoveLoop(point_in_screen);
  }


```

That path creates a new browser window and calls [DetachAndAttachToNewContext()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=bbf00ace04d1e5bb9c780c96506a599012e2dfef;l=1624), which detaches the tab from the original window and re-attaches it to the new one.

[Detach()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=b7aa90cd3e2def886c543c9ff7e86c880f802e8d;l=1453) chooses what to remove using the live, but incorrect, `selection_model()`. Because that state now points to `chrome://settings/ai`, it detaches settings/ai instead of the originally dragged `chrome://whats-new tab`.

[`AttachToNewContext()`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc;drc=b7aa90cd3e2def886c543c9ff7e86c880f802e8d;l=1326) then assumes the detached tab must exist in `drag_data_.tab_drag_data_` and looks it up, but because the detached `WebContents` is no longer represented in that drag snapshot, std::find\_if() returns .end(), which immediately dereferences as if it were a valid `TabDragData` => HBO

```
[...]
  for (auto& tab_or_collection : owned_tabs_and_collections) {
    if (auto* tab =
            std::get_if<std::unique_ptr<DetachedTab>>(&tab_or_collection)) {
      const WebContents* web_contents = tab->get()->tab->GetContents();
      // If it's a tab - we add it to the tabstrip.
      int add_types = AddTabTypes::ADD_NONE;
      TabDragData& tab_data = *std::find_if(
          drag_data_.tab_drag_data_.begin(), drag_data_.tab_drag_data_.end(),
          [web_contents](TabDragData& tab_data) {
            return web_contents == tab_data.contents;
          });
[...]

```
## Summary

Essentially, the live `TabStripModel` state and the drag-session snapshot in `drag_data_` have fallen out of sync. `Detach()` removed `chrome://settings/ai` based on the current `selection_model()`, but `drag_data_.tab_drag_data_` still only described the original `chrome://whats-new drag`. As a result, `std::find_if()` finds no matching `WebContents` and returns `.end()`, and immediately dereferences that end iterator as if a valid `TabDragData` had been found. That invalid dereference is what leads to the heap-buffer-overflow in `AttachToNewContext()`.

# Suggested Quick Fix:

Doesn't fix underlying state mismatch, but it will prevent on the off chance another variant of this bug occurs:

```
auto it = std::find_if(
    drag_data_.tab_drag_data_.begin(), drag_data_.tab_drag_data_.end(),
    [web_contents](const TabDragData& tab_data) {
      return web_contents == tab_data.contents;
    });
// Don’t assume `std::find_if()` will always return a valid matching iterator.
CHECK(it != drag_data_.tab_drag_data_.end());
TabDragData& tab_data = *it;

```
# Bisect:

[`a55f1e35bf2d53cea04ee7dfcc0f300bd8cf04a6`](https://chromium.googlesource.com/chromium/src/+/a55f1e35bf2d53cea04ee7dfcc0f300bd8cf04a6)
Detach groups when dragging them into a new window.

[`1b9b4dc759d89e0680b26606ac9ac042c64a916f`](https://chromium.googlesource.com/chromium/src/+/1b9b4dc759d89e0680b26606ac9ac042c64a916f)
Differentiate pinned and unpinned tab dragging across windows.

`a55f1e35bf2d53cea04ee7dfcc0f300bd8cf04a6` introduced the underlying state mismatch by letting `Detach()` follow the live tab-strip selection instead of the drag-session snapshot. `1b9b4dc759d89e0680b26606ac9ac042c64a916f` then made that mismatch crashable by changing AttachToNewContext() into a real WebContents lookup and still dereferencing the result without checking for `.end()`.

### ca...@chromium.org (2026-04-22)

I'm not able to reproduce this in the latest ASAN, can you add a video of this triggering?

### xp...@gmail.com (2026-04-22)

It's possible you need a patch to enable `chrome://whats-new` in ASan builds. Here is a patch.

### xp...@gmail.com (2026-04-22)

Here is a reproduction video.

### pe...@google.com (2026-04-22)

Thank you for providing more feedback. Adding the requester to the CC list.

### ca...@chromium.org (2026-04-23)

I'm still not able to reproduce, but I'm tentatively triaging this as valid based on the video and asan stacktrace. Triaging this as high severity since this is in the browser process but the gesture requirements are a mitigation.
Setting FoundIn to current extended stable based on reporter's bisect.

### ca...@chromium.org (2026-04-23)

shibalik and tbergquist: Can you help further triage this?

### xp...@gmail.com (2026-04-24)

Thank you for the triage. Adding WinDbg crash stack trace from latest Chrome Canary.

### ch...@google.com (2026-04-24)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-24)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### xp...@gmail.com (2026-04-28)

Hi, I don't believe shibalik works on Chromium anymore. I don't believe tbergquist does either—last commit to Chromium was over a year ago. Any chance you can help find a new owner? Thank you.

### ca...@chromium.org (2026-04-28)

Passing to code owners, dljames, alsan, dpenning: Can you help further triage this (and reassign as appropriate)? Thanks

### al...@google.com (2026-04-28)

Hi Sven, for your crash on Chrome Canary, could you please share the crash ID from chrome://crashes?

### xp...@gmail.com (2026-04-28)

Hello,

Here is the crash id.

Uploaded Crash Report ID: 4570126327f6e9fc

Another ID just in case: 08c0a7ec2167707e

### al...@google.com (2026-04-29)

Thanks! I wasn't able to repro this using the extension, but pasting `inject.js`[1] into the console while on `chrome://whats-new` was sufficient.

[1]

```
setInterval(() => {
   parent.postMessage({ data: { event: 'browser_command', commandId: 12, clickInfo: {}}}, '*');
}, 10);

```

### al...@google.com (2026-05-01)

<https://chromium-review.git.corp.google.com/c/chromium/src/+/7801697> should fix the HBO.

There's still some buggy behavior that happens with this repro (e.g. dragging within the tabstrip), but this was pre-existing and is less severe. Some more thought will need to be put into the lifecycle of tab dragging.

I'll mark this ticket as fixed when the CL lands.

### dx...@google.com (2026-05-01)

Project: chromium/src  

Branch:  main  

Author:  Kaan Alsan [alsan@chromium.org](mailto:alsan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7801697>

Use tab drag data as source of truth when detaching a tab drag

---


Expand for full commit details
```
     
    This resolves an HBO issue that was caused by TabDragController using 
    the tab strip's selection model as the source of truth while detaching 
    tabs during a drag. This was faulty because the selection model may 
    change during a drag. 
     
    This CL fixes this by using the tab drag data as the source of truth. 
     
    Note, there's still some existing buggy behavior when the selection 
    model changes during a drag that will require additional work. This CL 
    addresses the immediate HBO concern though. 
     
    Fixed: 505371980 
    Change-Id: Id82af5de05983974cb8ff8557b0e49e05af03fc8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7801697 
    Reviewed-by: Vince Lugli <lugli@google.com> 
    Commit-Queue: Kaan Alsan <alsan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1624124}

```

---

Files:

- M `chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc`
- M `chrome/browser/ui/views/tabs/dragging/tab_drag_controller_interactive_uitest.cc`

---

Hash: [9000f5659d4a257d2c6ddf804c5ea3146fffb07b](https://chromiumdash.appspot.com/commit/9000f5659d4a257d2c6ddf804c5ea3146fffb07b)  

Date: Fri May 1 22:36:30 2026


---

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Highly mitigated, never actually reprod under attacker conditions


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### xp...@gmail.com (2026-05-06)

Hello,

Thank you for the reward. Does the bisect bonus apply here?

Thank you.

### xp...@gmail.com (2026-06-05)

Hello Chromium VRP team,

Added the hotlist id:8186354. I believe this issue should have had the bisect bonus applied. Please see [comment #2](https://issues.chromium.org/issues/505371980#comment2), which includes the bisect.

Thank you.

### aj...@google.com (2026-06-05)

The award includes a consideration for a bisect.

### xp...@gmail.com (2026-06-05)

Hi,

Re #22: I checked the Wayback Machine (April 25th) snapshot of the Chrome VRP rules that was in effect at the time of this report.

Based on that policy text, I believe this issue should be classified as a moderately mitigated memory corruption issue in a non-sandboxed process.

Quote: `"Moderately mitigated: Security bug with multiple mitigations; e.g. a malicious extension combined with user interaction or other mitigation, ..."`. The steps in this bug match the description of a moderately mitigated bug exactly: malicious extension and a user drag.

The table states the minimum award would be $3,000 with an upper-bound of $4,000. Assuming the lower-bound is awarded, the minimum would be $3,000 + $1,000 (bisect bonus) = $4,000.

Thank you.

Ex. 325293263

### aj...@google.com (2026-06-25)

The panel classified this as Highly Mitigated due the user interaction required.

### xp...@gmail.com (2026-06-25)

Re #24: If the original decision of the panel was purely off of the "the user interaction required" then the classification would fall under "Moderately mitigated" and not "Highly Mitigated". The reproduction requires the exact mitigation pattern described for “Moderately mitigated” bugs: an installed malicious extension plus a user gesture.

Can this issue please be reevaluated? Thank you.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505371980)*
