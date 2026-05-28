# Security: heap-use-after-free ui/ozone/platform/wayland/host/wayland_connection.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40064072](https://issues.chromium.org/issues/40064072) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Ozone |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-17 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Build cros & lacros under ASAN
2. Launch cros wait until has finished and launch lacros on second terimnal and pass <http://rhezashan.github.io/pocs/tabFlood.html> --disable-popup-blocking
3. Wait until page has loading and select any tab before close itself.

**Problem Description:**  

I think this bug maybe race condition.

`WaylandToplevelWindow` has two parameters, namely `PlatformWindowDelegate` and `WaylandConnection`[1]. When creating a new window, the `ui::WaylandWindow::Create(ui::PlatformWindowDelegate\*, ui::WaylandConnection\*, ui::PlatformWindowInitProperties)[2]` function is called and still requires the `ui::WaylandConnection\*` parameter as a connection to Wayland.

The following stack trace occurs when the user drags from WaylandToplevelWindow:

```
#15 0x55b7518586eb in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:1491:28  
#16 0x55b7518579de in TabDragController::DragBrowserToNewTabStrip(TabDragContext\*, gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:931:5  
#17 0x55b751854407 in TabDragController::ContinueDragging(gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:892:16  
#18 0x55b75184c84e in TabDragController::Drag(gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:627:7  
#19 0x55b75187c4bb in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) chrome/browser/ui/views/tabs/tab_strip.cc:315:25  
#20 0x55b751882e02 in TabStrip::TabDragContextImpl::OnMouseDragged(ui::MouseEvent const&) chrome/browser/ui/views/tabs/tab_strip.cc:182:5  
#21 0x7f979ceb68ea in views::View::ProcessMouseDragged(ui::MouseEvent\*) ui/views/view.cc:3428:9  

```

When the Tab drag is performed, the function `const gfx::PointF WaylandConnection::MaybeConvertLocation(const gfx::PointF& location, const WaylandWindow\* window)[3]` is called to convert the position to a specific location, but using an crafted HTML script that can close the window itself will make the `|window|` destroyed and trigger a UaF because `|window|` has been deleted and called again on `converted.InvScale(window->applied_state().window_scale)`.

I think adding window observer on `WaylandConnection` can be good approach fix.

bisect: <https://chromium-review.googlesource.com/c/chromium/src/+/3662488>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_toplevel_window.h;drc=4bda591adbb4279c83ca0c9c919f2c4e49a1716c;l=53>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_window.h;drc=de237ca3dd2d2d7070a3de72d50dc1b568f62807;l=71>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:ui/ozone/platform/wayland/host/wayland_connection.cc;drc=446e2ae1963fe5d3ea0ffb548aad44e4182cef04;l=604>

**Additional Comments:**  

Tested all versions:

1. Branch 5615
2. Branch 5672
3. Branch main head

Screencast: <https://drive.google.com/file/d/1FPDzqrBkmkA4fF2_ldnw0RFYCHF0UzhJ/view?usp=share_link>

\*\*Chrome version: \*\* 112.0.5615.63 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [asan_main.log](attachments/asan_main.log) (text/plain, 10.4 KB)
- [asan_main_not_drag.log](attachments/asan_main_not_drag.log) (text/plain, 11.4 KB)
- [asan_branch_5672.log](attachments/asan_branch_5672.log) (text/plain, 11.0 KB)
- [asan_branch_5615.log](attachments/asan_branch_5615.log) (text/plain, 11.0 KB)

## Timeline

### [Deleted User] (2023-04-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-17)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/278482149). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/278482149]

### rh...@gmail.com (2023-04-17)

[Comment Deleted]

### [Deleted User] (2023-04-17)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-04-17)

Thank you chmiel@ for rapid respond.

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-16)

Project: chromium/src
Branch: main

commit 49ec1448912276048ae577b675bf03e3642ae96f
Author: Thomas Lukaszewicz <tluk@chromium.org>
Date:   Mon May 15 14:54:47 2023

    Reland "[wayland] Cancel dnd when drag target or dragged window destroyed"
   
    This is a reland of commit 0d9b005cd03fcea1466c8ee5e7f600690a8e380e
   
    See diff against patchset 1 for changes to the original CL.
   
    The original CL was reverted due to flaky failures of the following
    test case
      WaylandWindowDragControllerTest.
      HandleDraggedWindowDestructionAfterMoveLoop
   
    When `move_loop_handler->RunMoveLoop({})` is called it is expected
    the server generates a wl_data_device.data_offer and
    wl_data_device.enter event. The `drag_target_window_` is set during
    a drag when the enter event is received.
   
    The issue was that sometimes ``move_loop_handler->RunMoveLoop({})``
    would return before the client had received the offer and enter
    events, and sometimes not.
   
    If there is no enter received by the client, the target window is
    not set - and deleting the target window will not cancel the drag.
    When the events arrive later in this case the offer / enter events
    are correctly no-oped as the window does not exist.
   
    The inconsistency of delivered events for the test made it impossible
    to test without flakiness. This CL added a call to `wl::SyncDisplay()` and updated expectations for what occurs when the target window is
    destroyed.
   
    Original change's description:
    > [wayland] Cancel dnd when drag target or dragged window destroyed
    >
    > This CL updates the WaylandWindowDragController to cancel the dnd
    > session client-side when either of the drag target window or the
    > dragged window are destroyed.
    >
    > The dnd session is not cancelled when either the pointer grab or
    > origin window are destroyed as this occurrence is already supported
    > and defined by the dnd code.
    >
    > The client terminates the dnd session by calling OnDataSourceFinish()
    > which resets the wl_data_source and performs some client-side
    > cleanup. The spec indicates that the destruction of the data source
    > can be performed to cancel the dnd session.
    >
    > To handle any possible events sent by the server, but not yet
    > received by the client after the dnd session has been cancelled, the
    > client will no-op any further dnd events after this has occurred.
    >
    > Bug: b/278482149
    > Change-Id: I9f4af789b5392d2c589b31ec08077079c2b18daa
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4502756
    > Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
    > Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1142496}
   
    Bug: b/278482149
    Change-Id: Iec19e02aa34bb93cf291e761fc8f78a67fd52c69
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4518934
    Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
    Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Thomas Lukaszewicz <tluk@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1144095}

M       ui/ozone/platform/wayland/host/wayland_window_drag_controller.cc
M       ui/ozone/platform/wayland/host/wayland_window_drag_controller.h
M       ui/ozone/platform/wayland/host/wayland_window_drag_controller_unittest.cc

https://chromium-review.googlesource.com/4518934
16:55
16:55
CLs: Merged:​crrev/c/4502756, crrev/c/4518933      crrev/c/4502756, crrev/c/4518933, crrev/c/4518934
CLs: Pending:​crrev/c/4518334, crrev/c/4518934      crrev/c/4518334

### [Deleted User] (2023-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-16)

[Empty comment from Monorail migration]

### ni...@igalia.com (2023-05-17)

+max@ +tonikitoo@ fyi.

[Monorail components: Internals>Ozone]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-22)

This issue was migrated from crbug.com/chromium/1433577?no_tracker_redirect=1

[Monorail blocking: b/278482149]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064072)*
