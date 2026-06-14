# Security: Heap-use-after-free in extensions::`anonymous namespace'::LoadWatcher::DidCreateDocumentElement+68

| Field | Value |
|-------|-------|
| **Issue ID** | [40081748](https://issues.chromium.org/issues/40081748) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | pi...@live.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2015-03-28 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

By loading extension resources using JavaScript (see <https://crbug.com/chromium/468931>), I am able to trigger a heap-use-after-free on a SyzyASan build. I am filing this as a separate bug since fixing <https://crbug.com/chromium/468931> might only hide this UaF.

The idea is as follows:

- Leak the function that is passed to `appWindow.registerCustomHook` in the `app.window` resource (file `app_window_custom_bindings.js`).
- Open a popup.
- Call the leaked function with certain arguments (including a callback) to let it call `renderViewObserverNatives.OnDocumentElementCreated`. When the popup is being loaded, the callback will be called. A viewId of the popup must be passed as well; this number can be guessed by trial-and-error.
- Inside the callback, call `popup.document.write("a")`. (This makes the callback to be called again; ignore it this time.)

I presume that the `CallbackAndDie` function on line 44 of `render_view_observer_natives.cc` is called twice, which perhaps is not allowed.

If the bug is not triggered, try restarting the browser (I am assuming the viewId of the parent page is 2, which seems to be true on a fresh start).

I have attached part of the SyzyASan dump. The dump also contains an invalid write and a double-free, but I am not sure whether these are genuine or not.

**VERSION**  

Chrome Version: 43.0.2349.0, r322699 (with SyzyASan, downloaded from [1]). The UaF is also triggered on an older SyzyASan build (43.0.2323.0, r319247). The attachment crashes on stable, but it requires a slightly different call to `c_create` (drop the second argument, and turn the callback into `{ callback: function() { ... } }`. Possibly it is also an UaF, but I don't know since it's not an SyzyASan build.  

Operating System: I tested the SyzyASan builds on Windows Vista, and stable on Windows 8.1.

**REPRODUCTION CASE**  

See the attachment. I am sorry the code is dirty, it is such that certain code is triggered in the extension resources so as to call `renderViewObserverNatives.OnDocumentElementCreated` indirectly.

[1] <https://commondatastorage.googleapis.com/chromium-browser-syzyasan/index.html?prefix=win32-release/>

## Attachments

- [dump.txt](attachments/dump.txt) (text/plain, 36.3 KB)
- [appwindow.html](attachments/appwindow.html) (text/html, 3.8 KB)
- [appwindow3.html](attachments/appwindow3.html) (text/html, 3.8 KB)

## Timeline

### cl...@chromium.org (2015-03-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5709197371506688

### js...@chromium.org (2015-03-31)

So far this doesn't reproduce. Are you saying that a specific extension must be installed in order to reproduce?

### pi...@live.nl (2015-03-31)

No extension needs to be installed. I realize I failed to mention you have to click the button on the page. The UaF is triggered when clicking the button.

### js...@chromium.org (2015-04-01)

inferno@, mbarbella@ - Could one of you set the right flag to get cf to test opening the popup?

### cl...@chromium.org (2015-04-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5650702668398592

### cl...@chromium.org (2015-04-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5637145704792064

### cl...@chromium.org (2015-04-02)

meacer@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-04-02)

Assigning to danno@ for triage. I've been unable to repro this at all in current builds, but that maybe something has already changed for https://crbug.com/chromium/468931.

### js...@chromium.org (2015-04-02)

[Empty comment from Monorail migration]

### pi...@live.nl (2015-04-02)

I'm not sure why it doesn't reproduce for you. I've attached a slightly simplified version of the attachment that might succeed more reliably in guessing the view id. The UaF is still logged for me on the r322699 build. In canary it crashes (43.0.2355.0 canary (64-bit)).

Does this attachment reproduce for you when clicking the button "openPopup()"? If not, does it show the text "popupViewId == null"? If so, the view id of the popup could not be guessed. If you restart Chrome (completely quit the browser and restart), then the view ids seem to be low (starting from 1 if I'm not mistaken). The attachment should work in that case.

### js...@chromium.org (2015-04-03)

Assigning to hablich@ for triage.

### cl...@chromium.org (2015-04-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-07)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-04-07)

Ping. What's the status on getting this triaged?

### ha...@chromium.org (2015-04-07)

Jochen, can you evaluate please if this is valid?

### jo...@chromium.org (2015-04-07)

The UaF is in extension code, Ben, can you have a look please?

### [Deleted User] (2015-04-07)

> I presume that the `CallbackAndDie` function on line 44 of
> `render_view_observer_natives.cc` is called twice, which perhaps is not allowed.

I think it's more likely that the ScriptContext* it holds onto has been destroyed.

Anyway, I can immediately repro this with a Release build @ 323903.

### [Deleted User] (2015-04-07)

Btw the fundamental vulnerability here is that the test case managed to completely override our extensions bindings setup. Anything could happen really, in this case, a use-after-free. I can fix the crash but the bindings-overriding behavior is infeasible to fix.

### fe...@chromium.org (2015-04-17)

kalman: can you explain why the bindings-overriding behavior is infeasible to fix? 

it looks like 323903 is beta, so marking as Impact-Beta -- please update if you can get this to repro on stable too.

### cl...@chromium.org (2015-04-17)

[Empty comment from Monorail migration]

### [Deleted User] (2015-04-17)

I am quite confident that this can be reproed on every Chrome version for the last few years.

The reason it's infeasible to fix is because JS is infinitely monkey-patchable. I could fix this particular crash through some kind of nasty obfuscation technique (like making our view IDs much harder to guess), or I could fix it properly by rewriting the code in C++ so that it's not monkey patchable.

That's a fair amount of effort unfortunately. The author of the API is long-gone and the amount of time for somebody else to ramp up... etc... infeasible. There will be a long tail of similar issues as well.

### fe...@chromium.org (2015-04-17)

+meacer@, do you have an opinion about this?

### me...@google.com (2015-04-21)

I don't know much about bindings, so I'll defer to kalman's judgement, but it sounds like we'll have several UAFs in extension APIs with the status quo.
kalman: Do you mean rewriting all bindings in C++ or only app_window_natives? How much work do you estimate for that?

### [Deleted User] (2015-04-21)

In this case just the app window bindings, and in fact just the window opening flow. Currently it does this roundabout thing of using window.open() from JS then watching for events to get the correct view ID, which is what allows this bug to be triggered. There is probably some way to open a window from pure C++. Some time can be put into figuring out how and transitioning the code to using it.

Generally speaking though, anything that is implemented across the JS/C++ boundary is going to have bugs when developers poison the JS side.

### mb...@chromium.org (2015-04-21)

Fixing impact based on c#21.

### cl...@chromium.org (2015-05-13)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ha...@chromium.org (2015-05-20)

Removing V8 marker label as this is not a V8 bug.

### [Deleted User] (2015-05-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-11)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ms...@chromium.org (2015-06-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-02)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-24)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-14)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 85 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-04)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 106 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-09-26)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 128 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### [Deleted User] (2015-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-17)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 202 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-11-08)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 223 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-11-24)

FWIW I can't get this to reproduce on Linux with ASAN on tip-of-tree.

rdevlin.cronin: Is there any chance of getting at the root cause of this?

### cl...@chromium.org (2015-11-29)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 245 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-12-20)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 266 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-11)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 288 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-01)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 309 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-02-15)

rdevlin.cronin: Are you the right owner for this? 

meacer: Who else could we ask to triage this?

### rd...@chromium.org (2016-02-17)

@50, yes, sorry.  We've got a few in-flight patches that address similar bugs.  Once those land, I'll verify this is fixed.

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-03-10)

I think this was fixed with https://crbug.com/chromium/585268.  Rob can confirm.  This no longer repros.

### cl...@chromium.org (2016-03-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ro...@robwu.nl (2016-03-11)

I can't reproduce the reported bug (tried 42.0.2311.90, 43.0.2357.81, 46.0.2482.0 (ASAN)). The vulnerability that lead to the UAF is the one from https://crbug.com/chromium/585268, which has been fixed.

There is nothing left to merge, the patch is already in M-49.

### ti...@google.com (2016-03-23)

Even though this bug was fixed by the issue reported in https://crbug.com/chromium/585268 (see c#56), going to take it to the reward panel to see if this should be rewarded as well.

### ti...@google.com (2016-04-22)

Congrats pimvdb - $3,000 for this report. I'll add this to your other payment and start the process today.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/471523?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/490320]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081748)*
