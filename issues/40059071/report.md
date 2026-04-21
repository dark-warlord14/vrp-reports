# File picker UI spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40059071](https://issues.chromium.org/issues/40059071) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-03-11 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
onmouseup = _ => {
    let fs = showOpenFilePicker();
    open('https://www.google.com');
}

Click

What is the expected behavior?
For open() to require its own user interaction. (it also allows for a window popunder)
Stuff like window.close location.href should lose the FileSystemHandle anyway.

What went wrong?
File picker shown on the wrong origin while keeping FileSystemHandle.

Did this work before? N/A 

Chrome version: 99.0.4844.51  Channel: stable
OS Version: 10.0

## Attachments

- [pip-window-file-picker-macos.png](attachments/pip-window-file-picker-macos.png) (image/png, 454.5 KB)
- [popup-window-file-picker-macos.png](attachments/popup-window-file-picker-macos.png) (image/png, 473.1 KB)

## Timeline

### [Deleted User] (2022-03-11)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-03-14)

Thanks for the report! 

This behavior seems to be working as intended based on my limited understanding. CCing @creis for informed input about the nuances of Navigation and address bar properties. 

[Monorail components: Blink>Storage>FileAPI UI>Browser>Navigation]

### bo...@chromium.org (2022-03-14)

@mustaq, could you take a look please? Feedback from side channel conversation with @creis suggests this may not be WAI. 

### mu...@chromium.org (2022-03-15)

To me, both the popunder-like behavior (when the file dialog covers the whole tab) and wrong attribution about the file-opener site (when the file dialog is smaller than the tab) are bad.  Not sure if P2 is the correct priority here.

cc-ing mek@ who is an expert on file picker.

### nd...@protonmail.com (2022-03-15)

The popunder does not just cover the window it minimizes it.
Not sure what you mean by "when the file dialog is smaller than the tab" the issue is caused by the user interaction bypass. (you can even do showOpenFilePicker multiple times)

When the file dialog is dismissed such open() would be fine.

### nd...@protonmail.com (2022-03-15)

[Comment Deleted]

### mu...@chromium.org (2022-03-15)

Let me clarify https://crbug.com/chromium/1305663#c4:

- When the Chrome window is small, the file dialog covers the whole window.  In this case, the file-dialog completely hides the popup for the user.  I agree that closing the dialog reveals the popup to the user in this particular case, but this may not be true all the time.  For example, if the original opener window opens another popup after the user selects a file, the user won't know about the first popup.  This seems indistinguishable from pop-under to me.

- When the Chrome window is big enough, the user would see the popup right behind the file dialog, and would wrongly attribute the dialog to the popup.  A malicious site may open a Dropbox or GoogleDrive popup to fool the user into opening a file.

These scenarios need security team's attention for severity analysis.

### mu...@chromium.org (2022-03-15)

Thanks, the video in https://crbug.com/chromium/1305663#c6 confirms my first point.

### nd...@protonmail.com (2022-03-16)

[Comment Deleted]

### ad...@google.com (2022-03-17)

Tentatively rating as Medium severity, as this is a spoof which has some mitigating factors (applying only to file picker scenarios rather than complete omnibox control, which would be high). So bumping up to Pri-1. Assigning to mek because security issues need to be owned.



### ad...@google.com (2022-03-17)

The devtools snippet in https://crbug.com/chromium/1305663#c0 works for me on M99 so labelling this thus.

mek@ I assume nothing's changed here between M98 and M99. If that's the case, please could you also add a FoundIn-98 label so that the Extended Stable folks think about whether to take this fix into their branch.

### [Deleted User] (2022-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-03-17)

Definitely nothing new in 99 here, yes. Not sure what the best way to address this would be though... I also wonder if <input type=file> is equally effected, or if the file dialog that can be triggered programmatically that way (via it's showPicker method for example) somehow behaves different enough to not have this problem? Both only require transient user activation without consuming that activation (which I think is the right default behavior for most APIs).

[Monorail components: -Blink>Storage>FileAPI Blink>Storage>FileSystem]

### [Deleted User] (2022-03-17)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-03-18)

Yeah this seems to affects all file pickers.
Accessed via showPicker() or click()  or showDirectoryPicker() or showSaveFilePicker()

Fix seems to be not allow open() or similar in the same user interaction until the dialog has been dismissed.

### me...@chromium.org (2022-03-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>Forms>File]

### me...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-03-22)

Given that this effects all file pickers, not just the file system access API, I'm not sure I'm the right person for this to be assigned to.

+domenic as person who worked on showPicker. Was transient user activation vs consuming user activation at all brought up/considered with showPicker? Given the recency of that method, changing it to consumer user activation would probably be easier than making similar changes for any of the other ways to trigger a file picker. But making that change without changing other APIs also doesn't really seem like it would make much sense. So not sure what the best approach would be here...

### do...@chromium.org (2022-03-22)

> Was transient user activation vs consuming user activation at all brought up/considered with showPicker? 

Not really. We just tested what click() did and made showPicker() exactly as powerful as click().

I agree this is a tough one. It seems like the best solution would be to make everything activation-consuming, but probably that will break some sites...

### nd...@protonmail.com (2022-03-22)

Can the file picker UI contain the origin in the window title?
Or hide the file picker when a tab loses focus.

Ideally dont want to break stuff adding the origin to the file picker would probably also make save as safer.

### nd...@protonmail.com (2022-03-22)

This also works on Firefox with <input type=file> via click()
I think unless you do just add the origin to the picker title it would need a spec change.

I know im not being helpful.

### as...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-04-12)

How come the priority got deceased? its still Medium.
This issue should be fixed by other browsers as well.

Im guessing theirs a reason why you dont have the origin part of the file picker at least for windows the API exists.

### [Deleted User] (2022-04-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-04-12)

Thanks bot!

### ma...@chromium.org (2022-04-13)

(Thanks bot, and sorry about https://crbug.com/chromium/1305663#c24 - that was a bulk change that likely should have skipped this issue.)

Is there an owner for this P-1 security bug? I don't think we should mark this Available.

### as...@chromium.org (2022-04-18)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-22)

As mek@ mentioned this affects all file pickers so I don't think I'm the right person to own this. But I'm curious... do we have any sense of the amount of breakage that would result from making the picker consume its user activation?

### nd...@protonmail.com (2022-04-22)

Would this affect the save as dialog for downloads as well?
I think one way to get feedback would be an issue on https://github.com/w3c/FileAPI or https://github.com/WICG/file-system-access

### as...@chromium.org (2022-04-22)

(mentioning https://crbug.com/chromium/1181486 here, since it would also be affected by a change to user activation behavior)

### as...@chromium.org (2022-04-22)

I believe this would affect the save as dialog for downloads. 

mek@ can you confirm?

### me...@chromium.org (2022-04-22)

In a default chrome configuration I don't think there is a way to trigger the save as dialog programmatically (as all downloads just go to ~/Downloads instead). But it does seem plausible that that would also be effected, although I've never looked at that part of the codebase...

### nd...@protonmail.com (2022-04-22)

You can trigger a save as dialog via showSaveFilePicker()
The save dialog for normal downloads seems opt in via "Ask where to save each file before downloading"

### as...@chromium.org (2022-04-28)

Removing the Blink>Storage>FileSystem component, since this is a more generic file picker issue (I'm still CCed of course :) )

[Monorail components: -Blink>Storage>FileSystem]

### nd...@protonmail.com (2022-04-28)

Is there an owner for generic file picker issues?

I think robliao owns https://source.chromium.org/chromium/chromium/src/+/main:ui/shell_dialogs/select_file_dialog_win.cc
No idea who owns https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_file_picker.cc

### an...@chromium.org (2022-05-09)

+CC dtrainor@, qinmin@ since they are OWNERS of //chrome/browser/download (via //components/download)

### ma...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-05-16)

Note that this is a duplicate of crbug.com/637639. Because there's more context here than there, I'll dupe that one into this one. Some work was done (see comment [1]) to add a use counter for how often a popup window is opened while a file picker is already open:

https://chromestatus.com/metrics/feature/timeline/popularity/2509

Surprisingly, that counter is at 0.12%, which is not small. I wonder if there's a "real" use case for this behavior? The proposal from crbug.com/637639 was to just force-close the file picker when a window popup was opened, which does seem to be sensible behavior. It also seems like it would cause fewer compat problems than making file picker consume its user activation. But I am curious if it would break some use case we're not considering here, based on the use counter numbers.

Even if that's the best solution for this problem, it'll take some work, since we have no capability to force-close native file pickers at the moment, and that requires per-OS implementations.

Given crbug.com/637639, which is allpublic and has been open since 2016, I'd question whether this bug needs to be P-1?

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=637639#c18

### ma...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-05-17)

I think it would also need to block popup.focus() that forcing user interaction would have fixed. (Also https://bugs.chromium.org/p/chromium/issues/detail?id=1181486)

Multiple file pickers may be opened so it would be nice to have the origin as part of the picker title if the platform allows it.

0.12% may not need to include same-origin popups.

In terms of P1 I think its okay for Severity-Medium this was decided in https://crbug.com/chromium/1305663#c11 maybe the standard has increased since 2016 :)

### ja...@chromium.org (2022-05-20)

I imagine that requiring user activation would break websites, and I don't think that the UseCounter from https://crbug.com/chromium/1305663#c40 shows the percent that would break.

> Even if that's the best solution for this problem, it'll take some work, since we have no capability to force-close native file pickers at the moment, and that requires per-OS implementations.

I briefly looked into this for mac. Here is our native implementation: https://source.chromium.org/chromium/chromium/src/+/main:components/remote_cocoa/app_shim/select_file_dialog_bridge.mm

I'm having a hard time understanding it and I'm not even sure if it's possible to close the picker:
https://developer.apple.com/forums/thread/39669
https://stackoverflow.com/questions/13355888/how-to-close-nsopenpanel-or-why-it-doesnt-close-automatically
https://stackoverflow.com/questions/4688925/close-nsopenpanel-as-soon-as-file-directory-has-been-selected

### ja...@chromium.org (2022-05-23)

I filed an issue to look at closing native file select dialogs: https://crbug.com/chromium/1328097

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-05-25)

Security marshal here: jarhar@ I'm going to assign this to you since it seems you are on top of this. Feel free to retriage!

### [Deleted User] (2022-06-06)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-06-09)

Security marshal here. jarhar@, is there any update on the status of this ticket or the blocking ticket (1328097)?

### ja...@chromium.org (2022-06-09)

avi, do you have any thoughts on https://crbug.com/chromium/1305663#c43 and https://crbug.com/chromium/1305663#c44 or know anyone who might know if it's possible to close a native file picker window?

### ja...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-06-09)

I have no experience with this but I will try anyway :)

For macOS it seems NSOpenPanel (https://developer.apple.com/documentation/appkit/nsopenpanel) -> NSSavePanel -> NSPanel -> NSWindow 
https://developer.apple.com/documentation/appkit/nswindow has a "Closing Windows" section.

For window https://social.msdn.microsoft.com/Forums/windows/en-US/d69a57c5-60ad-46aa-aa6d-4d872941e497/close-filedialog-programmatically?forum=winform

### av...@chromium.org (2022-06-15)

What was the conclusion as to what we want to do here? I’m happy to help wire up the Mac side of things, though I’ll need some assistance on other platforms.

### nd...@protonmail.com (2022-06-15)

I think its to force-close the file picker when a different origin is focused.
This needs https://crbug.com/chromium/1328097 to be fixed so theirs a way to close the popup.

### av...@chromium.org (2022-06-16)

OK, let’s do 1328097. I can take the Mac side of things, but Win/Lin/CrOS/Android need folks to work on it.

### av...@chromium.org (2022-06-16)

Has anyone looked at `BaseShellDialog::ListenerDestroyed()`? That would leave the dialog open but would nerf the callback.

### av...@chromium.org (2022-06-16)

I just looked at this.

The way to close a file picker dialog (as requested in https://crbug.com/chromium/1328097) is to destroy the file picker object. See https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/certificates_handler.cc;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;l=773 as an example:

  // There may be pending file dialogs, we need to tell them that we've gone
  // away so they don't try and call back to us.
  if (select_file_dialog_.get())
    select_file_dialog_->ListenerDestroyed();
  select_file_dialog_.reset();


### nd...@protonmail.com (2022-06-16)

:)

Not sure on what rules the force closing should use.

This issue happens when a different origin becomes visible.
1. window.open(target);
2. popup.focus();
3. popup.location = target;

Opening the same origin seems safe.

### nd...@protonmail.com (2022-06-18)

On tab change in the same window as the file picker it should always close.

For multiple windows it seems harder:
1. Attacker page opens attacker popup. (As small as possible)
2. User clicks attacker page and that interaction is shared to the popup to open a file picker and the popup gets minimized.
3. Attacker page goes to target.

To migrate this the file picker could close when the window is no longer visible but the picker might be used while using other programs.

### ja...@chromium.org (2022-06-22)

> The way to close a file picker dialog (as requested in https://crbug.com/chromium/1328097) is to destroy the file picker object. See https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/certificates_handler.cc;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;l=773 as an example:

Thanks! It looks like we are currently using FileSelectHelper::RunFileChooser. FileSelectHelper owns the SelectFileDialog, but manages it's own lifetime and doesn't really provide any way to get the object back. I think we will have to change this in order to initiate a destruction of the SelectFileDialog. Maybe ui::Browser can have a map of RenderFrameHost to FileSelectHelper so it can call into and/or delete the FileSelectHelper.

### [Deleted User] (2022-07-01)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-09-02)

This is a bulk comment on all P1 bugs in DOM that are outside the 20 day SLO. Please take a look at this bug! Either fix it, re-triage it, re-assign it, or downgrade its priority to P-2. Thank you!

### nd...@protonmail.com (2022-09-02)

I like the fix option since its medium severity but its blocked on https://bugs.chromium.org/p/chromium/issues/detail?id=1328097 and thats P3.

### ma...@chromium.org (2022-09-02)

Good point - I just raised the priority of that blocking bug.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-11-17)

Still no fix :(
Is it hard to close the file picker?

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-03-22)

Guessing its still not possible to close native file select dialogs :(

### ja...@chromium.org (2023-03-26)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-03-26)

I implemented this based on avi's suggestion of deleting the ui::SelectFileDialog, and it works on mac.
On Linux however, it doesn't work and frequently crashes. It also doesn't work on windows.
https://chromium-review.googlesource.com/c/chromium/src/+/4372101

### nd...@protonmail.com (2023-03-26)

Does https://chromium-review.googlesource.com/c/chromium/src/+/4372101 close on focus() of a hidden window?
There's probably a lot of users on mac so that's still a good patch :)

### ja...@chromium.org (2023-03-26)

> Does https://chromium-review.googlesource.com/c/chromium/src/+/4372101 close on focus() of a hidden window?

No. Could you provide a full example? This is likely another breaking change we would have to carefully consider.

### nd...@protonmail.com (2023-03-26)

w = open()
Go back to previous tab

onmouseup = _ => {
 w.focus();
 w.location='https://example.org';
 showOpenFilePicker();
}

### nd...@protonmail.com (2023-03-29)

Is that not in scope for the fix since it requires multiple tabs?
I think a less breaking change would be to embed the origin in the file picker title at least on windows.

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-07-21)

Quick ping on this P-1 bug, outside the 20 day SLO. Any status update? Does this need to be P-1?

### nd...@protonmail.com (2023-07-21)

Reminds me of https://crbug.com/chromium/1305663#c62 I would like to see this finally fixed.

### nd...@protonmail.com (2023-07-29)

Someone asked to be CCed https://bugs.chromium.org/p/chromium/issues/detail?id=637639#c28
Is this blocked on https://crbug.com/chromium/1305663#c73

### mu...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-08-25)

I'm not sure we have the resources to fix this bug. jarhar@ would you like to stay assigned, or do you have another suggestion for how to make progress?

Given that this has been a known bug for 7 years (https://crbug.com/637639) I don't think this deserves a P-1 priority. I don't disagree that it's a situation we want to avoid, but the user risk seems "medium" and while I know the bot (https://crbug.com/chromium/1305663#c26) would like that to be P-1, I think this might be an exception.

### nd...@protonmail.com (2023-08-25)

I'm not sure if its possible to prevent this attack there's a lot of ways to focus a different tab even extension APIs.

I still like the idea of putting the origin in the file dialog title for platforms that allow it that way the user will know who there sharing the file with but I don't think anyone else liked it :(

P1 was not done by a bot https://bugs.chromium.org/p/chromium/issues/detail?id=1305663#c10 but I agree its not high severity.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-11-03)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-12-03)

I saw https://bugs.chromium.org/p/chromium/issues/detail?id=1414936 strangely does not cover the showOpenFilePicker() case.
Only fileSelect.click(); I think the protection should cover every way to show the file picker.

The w.focus() attack requires multiple tabs open so this patch would still be worth adding.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

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

### av...@chromium.org (2024-01-30)

[Empty comment from Monorail migration]

### ch...@chromium.org (2024-01-31)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-31)

This issue was migrated from crbug.com/chromium/1305663?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>File, UI>Browser>Navigation]
[Monorail blocked-on: crbug.com/chromium/1328097]
[Monorail mergedwith: crbug.com/chromium/1328097, crbug.com/chromium/1494792, crbug.com/chromium/1500884, crbug.com/chromium/637639]
[Monorail components added to Component Tags custom field.]

### nd...@protonmail.com (2024-05-31)

Thanks for changing it back, hopefully this gets fixed some day consuming user activation in all browsers seems like the correct fix would be a breaking a change however.  

It does not look to be possible to change tab once the picker is open in both chrome and firefox.

### nd...@protonmail.com (2024-06-25)

There seems to be no reason to not apply the fix to `showOpenFilePicker()`

- fileselect.click() has a patch <https://chromium-review.googlesource.com/c/chromium/src/+/4755412>
- fileselect.showPicker() has a patch <https://chromium-review.googlesource.com/c/chromium/src/+/5235516>

Based of <https://github.com/whatwg/html/pull/10344> consuming user activation is the correct thing to do here I don't see why this should be delayed any longer.

### ja...@chromium.org (2024-07-08)

> There seems to be no reason to not apply the fix to showOpenFilePicker()

I thought this bug was about making the file picker close when calling window.open(). Would consuming user activation in showOpenFilePicker() be good enough to fix this? If so I'll happily do it.

### as...@chromium.org (2024-07-08)

> Would consuming user activation in showOpenFilePicker() be good enough to fix this?

It should, since then `open()` would not have user activation in the repro:

```
onmouseup = _ => {
    let fs = showOpenFilePicker();
    open('https://www.google.com');
}

```
> Based of <https://github.com/whatwg/html/pull/10344> consuming user activation is the correct thing to do here I don't see why this should be delayed any longer.

The [spec for `showOpenFilePicker()`](https://wicg.github.io/file-system-access/#api-showopenfilepicker) (see step 7.2) is independent from the spec for `showPicker()`, so we'd have to make similar changes in <https://github.com/WICG/file-system-access> if we were to require user activation to show a picker.

I investigated this a few years ago for some related issues ([issue 40170428](https://issues.chromium.org/issues/40170428) (also by OP) and [issue 40057599](https://issues.chromium.org/issues/40057599)) but didn't make any changes because (from <https://crbug.com/40057599#comment5> and <https://crbug.com/40057599#comment6>):

- concerns about breaking sites, and
- it wasn't clear that `showOpenFilePicker()`/`showSaveFilePicker()`/`showDirectoryPicker()` was the right layer to add this logic; ideally there would be logic at the system UI level or elsewhere in Chrome to make the file picker UI be scoped to the window and only showable by a foreground tab. Other APIs could still show file pickers, so blocking just pickers shown via the File System Access API felt like an insufficient hack. See [this thread](https://groups.google.com/a/google.com/g/deviceapi-team/c/hsPA4mvcJE8/) for more details.

If other pickers now consume user activation then the latter point is less relevant. It would still be nice if the layers from `SelectFileDialog` down were smarter, but it might be good enough if the Web Platform layer can prevent behaviors such as multiple pickers from being shown per window.

The concern about site breakage is still valid, though perhaps we shouldn't be as concerned since:

- `showOpenFilePicker()` mints a new user activation once the picker is resolved (see [step 7.9](https://wicg.github.io/file-system-access/#api-showopenfilepicker))
- requiring user activation for the other pickers doesn't seem to have broken much?... ¯\*(ツ)*/¯

So... aligning with `showPicker()` by consuming the activation seems like the right thing to do? Any other folks working on FSA have other thoughts?

### nd...@protonmail.com (2024-07-09)

Yeah without user activation you cant do `open()` or `win.focus();`  

So as long as every file picker consumes user activation ideally at a low level there's no security risk.  

The popup blocker can be bypassed for a website since a message shows automatically when there's no user activation.

I don't think closing the file picker is going to happen anytime soon.

### nd...@protonmail.com (2024-07-09)

By the looks of it `.click()` blocks `window.open()` but does not consume user activation so focusing a hidden tab works.  

`onclick = () => {file.click(); setTimeout(() => { w.focus(); w.location='https://www.google.com' }, 10)}`

### ds...@chromium.org (2024-07-09)

> So... aligning with showPicker() by consuming the activation seems like the right thing to do? Any other folks working on FSA have other thoughts?

I think this seems reasonable. The potential breakage is a little unclear, as the spec indicates being able to request another permission, but it seems rare to do that since the handle from the picker should already have permission.

### as...@chromium.org (2024-07-09)

Some pickers provide read-only handles, though. I imagine it's quite common for a site to immediately request write permission to these handles

### nd...@protonmail.com (2024-07-09)

The patch <https://chromium-review.googlesource.com/c/chromium/src/+/4755412/4/content/browser/web_contents/web_contents_impl.cc> works without consuming user activation but I wanted to also cover the `.focus();` case.  

And it seems better for `showPicker` to be like `showOpenFilePicker()`/`showSaveFilePicker()`/`showDirectoryPicker()`

### nd...@protonmail.com (2024-07-22)

If a site immediately requests write permission maybe that could wait until the user has chosen a file where there would then be user activation again.

### ja...@chromium.org (2024-07-23)

I started a patch: <https://chromium-review.googlesource.com/c/chromium/src/+/5735618>

### nd...@protonmail.com (2024-09-18)

Nice patch! I like the part where it does `ConsumeTransientUserActivation`

### pe...@google.com (2024-10-26)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 94 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

jarhar: Uh oh! This issue still open and hasn't been updated in the last 109 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ct...@chromium.org (2024-11-15)

jarhar@ are we close to being able to land a fix for the user activation issue here? This has come up again a slightly different context in [Issue 378890686](https://issues.chromium.org/issues/378890686) (cc'd you there as well for visibility).

### ct...@chromium.org (2024-11-22)

Merged [Issue 378890686](https://issues.chromium.org/issues/378890686) into this canonical issue, but explicitly noting here that this also affects PiP windows which may make this slightly easier to use for spoofing.

This appears to be platform specific in an interesting way as well. For example, on macOS if you call window.showOpenFilePicker() in a PiP or popup window it is bound to the window which is *much* better security UX -- see attachment. This matches the behavior of the file picker for a popup window on macOS (see second attachment).

I'm not sure if Windows gives us sufficient controls to replicate the much nicer macOS behavior though. The reporter on [Issue 378890686](https://issues.chromium.org/issues/378890686) did give the suggestion of making use of the dialog title on Windows to try to mitigate the spoofing risk (e.g., put the requesting origin there) which *might* help somewhat but might also be easy for users to overlook, so I think we would still be best served by landing the jarhar@'s fix in <https://crrev.com/c/5735618>.

### nd...@protonmail.com (2024-11-23)

Yeah consuming user activation in all picker cases seems like the right thing to do.
The dialog title with an origin seems not needed although this wont apply to a normal file download where it might have been useful.

### ja...@chromium.org (2024-12-10)

I just did some testing, and it seems like window.open() will still open a new window even if there is no user activation, so I don't see why consuming user activation in showOpenFilePicker is helpful. Is anyone seeing different behavior?

### ab...@microsoft.com (2024-12-11)

If you are running JS from devtools its automatically given user activation when fired. Try setTimeout(e=>{open()},6000) and make sure you don't send any events to the web content. You should see popup blocker.

### mu...@chromium.org (2024-12-11)

Good point re running JS from devtools. This can be turned off using the console>settings "⚙" >"treat code evaluation as user action".

### ja...@chromium.org (2024-12-12)

Oh I didn't realize that the difference without user activation is that the popup blocker shows up, that makes sense

### ca...@chromium.org (2025-04-10)

[Secondary security shepherd]

jarhar: Are there any updates since #129?

### ja...@chromium.org (2025-04-15)

I just updated the code review

### dx...@google.com (2025-04-18)

Project: chromium/src  

Branch: main  

Author: Joey Arhar [jarhar@chromium.org](mailto:jarhar@chromium.org)  

Link:      <https://chromium-review.googlesource.com/5735618>

Make FileSystemAccess APIs consume user activation

---


Expand for full commit details
```
     
    User activation is consumed in the browser process instead of the 
    renderer process like input.showPicker() because consuming user 
    activation in the renderer would make the existing user activation check 
    in the browser process fail. 
     
    There is no browsertest because content::EvalJs() sets user activation 
    after running script, even with the flag to not run user activation, and 
    I don't know how to make it stop. 
     
    There is no web_test because consuming user activation in the browser 
    process does not notify the renderer process that it lost user 
    activation. It does not look like there is any existing interface to 
    make the browser tell the renderer that it lost user activation, only 
    the other way around. 
     
    I manually verified that the attached bug is fixed. 
     
    Spec issue: https://github.com/WICG/file-system-access/issues/458 
     
    Fixed: 40059071 
    Change-Id: Ia1f5ff63a8bdf6cdec70dea1406e9865123f96a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5735618 
    Reviewed-by: Mustaq Ahmed <mustaq@chromium.org> 
    Reviewed-by: Fergal Daly <fergal@chromium.org> 
    Commit-Queue: Joey Arhar <jarhar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1448885}

```

---

Files:

- M `content/browser/file_system_access/file_system_access_manager_impl.cc`

---

Hash: d5561f9e792bef4da69074b13cc04bbf38f95d69  

Date:  Fri Apr 18 15:57:42 2025


---

### nd...@protonmail.com (2025-04-18)

Yay

### sp...@google.com (2025-04-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### nd...@protonmail.com (2025-04-25)

Thanks :)

### ch...@google.com (2025-04-30)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-04-30)

Something broke with the bot merge log, removing merge requests as this fix landed two weeks ago on 137

### ch...@google.com (2025-07-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059071)*
