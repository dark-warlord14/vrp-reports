# Security: Read all local files using minimal user interaction and gesture laundering

| Field | Value |
|-------|-------|
| **Issue ID** | [40085079](https://issues.chromium.org/issues/40085079) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File>Directory |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | pb...@chromium.org |
| **Created** | 2016-08-11 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using a hidden input[type=file] element, in conjuncture with minimal user interaction I am able to read *ALL THE FILES IN A VICTIMS LOCAL DISK*

Please refer to the PoC for a live example.

**VERSION**  

Chrome Version: Version 52.0.2743.116 m + stable (64-bit)  

Operating System: Window 8.1 64-bit

**REPRODUCTION CASE**  

If you look at the PoC, you will notice I ask the user to hold down the Enter button. Using some simple javascript I am then able to trick the user into giving me access to all of his/her files on local disk. Having the user to hold down the enter key for literally no more than 5 seconds is enough to read their entire computer. I dont think this is a lot to ask given the severity.

There are multiple issues with the folder upload feature on chrome:

- The file dialogue always defaults to C:
- The file dialogue can be triggered without user clicking anything
- Once the dialogue opens, all a user needs to do is press enter with no other things needed. This is different with the normal file uploader where you have to select something first.
- Most importantly. The 'webkitdirectory' feature actually crawls through all the files, irrespective of the 'accept' attribute value. In the PoC here I set accept=plain/\* and I end up reading everything including images and binaries.

This is extremely dangerous for Chrome users and just to give you proof this is a bug, on firefox the file dialogue is blocked via popup blocker so its not automated as it is here.

---Suggestions to fix -------

I would suggest not always defaulting to C:/ but rather default to something like mycomputer and of course do not allow crawling of all the folders within a certain folder.

Alternatively, have the popup blocker block the file/folder choosing prompt from untrusted websites. (like firefox does)

## Attachments

- [PoC-Read-all-Files.html](attachments/PoC-Read-all-Files.html) (text/plain, 1.2 KB)
- [PoC-Read-all-Filesv2.html](attachments/PoC-Read-all-Filesv2.html) (text/plain, 1.4 KB)
- [folder-confirmation-dialog-update.png](attachments/folder-confirmation-dialog-update.png) (image/png, 20.7 KB)
- [folder_upload_update.png](attachments/folder_upload_update.png) (image/png, 6.9 KB)
- [637098@mac.mp4](attachments/637098@mac.mp4) (video/mp4, 511.9 KB)
- [637098@win10.mp4](attachments/637098@win10.mp4) (video/mp4, 616.5 KB)
- [PoC-Read-all-Files.html](attachments/PoC-Read-all-Files.html) (text/plain, 450 B)

## Timeline

### gr...@hotmail.com (2016-08-11)

It's worth pointing out that in FireFox even if we assume the user allowed popups on the malicious site, when the folder selector prompt appears it also defaults to C:/. However, if you press enter or select it will not allow you to select 'C:/' as a folder.
Further proof that there is something wrong here.

Also. While testing this, I understand it will be intensive for the chrome process (as the javascript will take a good 3-5 minutes for reading all the files) sometimes I do get a 'this page is unresponsive' But this was due to me being on a laptop computer. I'm sure if this was done to a user with a more powerful desktop computer, the javascript will be quicker and wont result in a 'this page is unresponsive' error.
Despite me being on a laptop, I still dont always get the error. Actually its more likely it passes than not.

### gr...@hotmail.com (2016-08-11)

After some more testing, I noticed that in the original PoC the tab crashes after displaying the two alerts (still reads the file).
In order to circumvent this, I made a new PoC which does not tab crash after finishing with the exploit. I do this by only reading 500 files from the list (which for me is >600k files) and then delete the input element alongside its huge array of files. 

Another problem was the 'unresponsive page' prompt popping up. Although I don't get it all the time, its still a problem. The only way I can stop it from working is if the user goes to another tab whilst the exploit works out of focus. 

I have attached the new version.

### gr...@hotmail.com (2016-08-12)

This seems to work on Opera as well. Do I need to send it to them as well? 

I'm asking because I know that they use the same webkit as chrome.

### oc...@chromium.org (2016-08-12)

kinuko, could you please take a look at this, or assign it to the right person?

[Monorail components: Blink>Storage>FileSystem]

### gr...@hotmail.com (2016-08-13)

Tested on Chromium 54.0.2821.0 - The default location is 'C:\Users\{Current user}' which is actually a good thing for the exploit since it does not take as long as it would crawling 'C:'.

Still crawls all sub folders.

### wf...@chromium.org (2016-08-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-13)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2016-08-14)

Another quick fix for this would be to only allow the folder uploader dialogue to appear if the click event is coming from a genuine user click.

This type of fix will prevent the 'hold enter for 5 seconds' method.

For example:

inputElement.onclick={inputElement.click()}//Only works from here

inputElement.click()//should not work

This type of fix will ensure that all the custom UI designs for any folder uploaders won't break.

### ta...@opera.com (2016-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-26)

kinuko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@hotmail.com (2016-08-29)

Any update on this?

### va...@chromium.org (2016-09-02)

kinuko@ -- Any update on this issue? If you are not the right person to own this issue, please help find this right owner. Thanks.

### el...@chromium.org (2016-09-09)

Re #9: I don't think that's practical, as legitimate sites use the pattern where you click on something else and that calls .click on a hidden input control.

### gr...@hotmail.com (2016-09-09)

Re #14: What I meant was that the element.click() should only execute within any OtherElement.onclick event. Essentially preventing inputElement.click() to be executed randomly from a non-mouseclick user event. So hitting enter (or holding it in this case) would not work as its from a keyboard event. Hope that makes sense.

### gr...@hotmail.com (2016-09-09)

Though, it will still be possible to 'trick' users into clicking a few times in one place and have them upload arbitrary folders unknowingly. The folder uploader needs to default into an unselectable location. (Like My Computer for windows)

### sh...@chromium.org (2016-09-10)

kinuko: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@hotmail.com (2016-09-30)

This is a pretty serious bug, I'm surprised its being ignored for this long.. I wish I knew how to write patches I would have done it myself, the fix seems pretty simple to me. Just block upload dialogue from any user events that are not mouse clicks.

### mm...@chromium.org (2016-10-11)

Friendly ping from Security Sheriff: kinuko@, could you please take a look?

Also CC'ing a few more storage/OWNERS.

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### ki...@chromium.org (2016-10-22)

(Sorry for slow response, I'm ooo and haven't been checking incoming bugs)

This is not really about FileSystem but about input=file with directory handling.

Taking a quick look at FileSelectHelper::GetSanitizedFilenameOnUIThread, it looks:
- it looks the default path seems to be 'last selected directory' but not C:. With a fresh profile it seems to point to Desktop on Windows and Downloads folder on Mac.
- the feature seems to be behind the safe browsing protection, so I think we still have some protection there

Given that I'm changing the severity to Low.

Adding some security folks to look for some advise, and unassigning myself as I don't think I'm the right owner for this issue.

### ki...@chromium.org (2016-10-22)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2016-10-22)

Testing this in Windows 10, fresh chrome install I get the folder picker pointing to 'C:\Users\{Current User}' which include desktop, downloads and myDocuments folder.

Microsoft found this vulnerability at least medium severity for their Edge browser, so I'm confused about the low severity. This is a reliable information leak with minimal user interaction (holding down enter for ~2-4 seconds.)

Not sure how safe browsing protects this? I tested this on an online website and it still works, is it the case that if an attacker were to use this method on a mass scale it would be behind 'dangerous website' wall?



### gr...@hotmail.com (2016-10-22)

Hrmm one odd thing re-testing this is that on localhost the PoC works fine (also goes to C: automatically) but once hosted on random non-localhost http website the PoC fails (though files are still read) and the directory is C:Users/{current}.

For some reason on non-localhost the onchange event does not fire. This still can be exploitable on web if we keep checking if thing.files.length is >1 within a setInterval, and then do what we want with the files loaded (or file pointers loaded rather).

Is this difference in behavior caused by safe browsing? If so, it seems still insufficient as a lot of files are still exposed.

### sh...@chromium.org (2016-10-22)

[Empty comment from Monorail migration]

### jw...@chromium.org (2016-10-22)

Thanks for the report, and I'm really sorry it's taken us a while to respond to this! It seems like we had earlier triaging issues, and I apologize for that.

Firstly, no need to report to Opera separately; their security team has access to these security bugs (and you can see that there's already one Opera person on this CL).

Secondly, jsbell@, I'm really not sure who to assign this to, can you help me find a good owner? I'm assigning to you in the meantime. Thanks!

Lastly, I have mixed feelings about Medium vs Low severity on this one. Generally, we do say that requiring a user gesture like this makes it a low severity, but I agree that it's a pretty low bar. That having been said... it doesn't really matter. We should fix this in some way.

Again, thanks for the report!

### js...@chromium.org (2016-10-24)

Just to clarify, here's a simpler equivalent:

1. Put focus on a button
2. Ask user to hit the Enter key twice
3. On the first keypress invoke a click() on an <input type=file webkitdirectory>

Step #3 launches the directory upload picker; the second keypress trigger the OK button, selecting whatever the directory was - depending on the OS dialog used.

(Side observation on Ubuntu Linux: each subsequent time the directory picker is launched the picker is showing the parent directory relative to the last pick. Weird.)

I can think of two approaches to pursue here:

* Attempt to flush keyboard state before the dialog is launched (i.e. so the key stops repeating)

* Avoid rooting the directory upload picker at random locations, e.g. always pick the local equivalent of "Documents" or "Downloads" or at least the user's home dir, never root of the drive.



[Monorail components: -Blink>Storage>FileSystem Blink>FileAPI]

### rb...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2016-10-24)

Filed https://crbug.com/chromium/658839 for the "showing the parent directory" problem

### js...@chromium.org (2016-10-26)

Another thought on Windows at least: if we make the default a non-file-system directory (e.g. Desktop) then the OK button would be disabled until selection is explicitly changed.

(Currently, the folder to select by default is remembered on a per-profile basis, common across file/directory upload actions.)

### gr...@hotmail.com (2016-10-30)

Given https://crbug.com/chromium/658839 I think the severity of this bug should be increased to medium. I hate to harp on this but I am participating in a bug bounty and so severity here matters to me. 




### gr...@hotmail.com (2016-11-19)

May I get an update on this? Will it be fixed soon? It's been more than 90 days...

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2017-04-14)

Reporter has posted externally about this issue

http://leucosite.com/Chrome-Firefox-Edge-Local-File-Disclosure/

### js...@chromium.org (2017-04-14)

A potentially straightforward fix is to simply not trigger the file/dir picker on keydown but on keyup, so that repeat is irrelevant.

### dt...@chromium.org (2017-04-14)

There is also a flag indicating keydown is repeated. 

### js...@chromium.org (2017-04-14)

> There is also a flag indicating keydown is repeated.

The problem is that we launch a system dialog, which apparently isn't checking this. Hence the other idea of flushing the input queue. None of this (how we trigger the UI or the details of the dialog) are in code I'm at all familiar with, alas.

### js...@chromium.org (2017-04-14)

... although that would help with this specific repro where the key is already in a "repeat" state before the focus is shifted to the control and hence - I see what you're getting at. Maybe that's sufficient.

### js...@chromium.org (2017-04-14)

Hrm... and 'repeat' seems broken on linux at the moment (57 and tip-of-tree). I swear it worked at one point.

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### dt...@chromium.org (2017-06-21)

Ella let's discuss this when you are back.

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-10-27)

This bug seems to be languishing: reassigning to jsbell@ for triage.

### me...@google.com (2017-11-08)

[Empty comment from Monorail migration]

### me...@google.com (2017-11-08)

Looks like this bug is already publicly disclosed: http://leucosite.com/Chrome-Firefox-Edge-Local-File-Disclosure/

While there is a user interaction requirement, it doesn't seem impossible that a legitimate web page would ask something like this from a user. Given that, is low priority really appropriate here? I think this could be Medium and even P-1.


### el...@chromium.org (2017-11-08)

+Reporter of 782842, who included a nice POC in the report.

I agree that this seems higher than Low-- the user-interaction requirement is not in any way onerous.

### js...@chromium.org (2017-11-08)

Passing back to dtapuska@ - the plausible fixes we've discussed are on the input side of things (processing button press only on on keyup, flushing the input queue, etc).


### me...@google.com (2017-11-08)

I think we can remove view restrictions as the bug is already public. If nobody disagrees, I'll do that.

As an alternative fix, would it make sense to time the duration between displaying the dialog and getting a result, and ignore the result if the delta is less than the time for a human to respond? (e.g. 500ms) This probably won't work for computers with slow disks, but can raise the bar a bit.

### el...@chromium.org (2017-11-08)

On Windows, we could use BFFM_ENABLEOK to have the dialog start out with a disabled OK button, then start a timer from the BFFM_INITIALIZED message so that it's not enabled for a half-second or whatever timeout we think is reasonable.

### me...@google.com (2017-11-08)

I actually meant ignoring the result of the directory listing returned from the dialog if the time passed is too short (making the dialog a no-op), but not allowing the user to accept the dialog before a certain timeout also seems reasonable. We do that for extension install dialogs using a 500ms delay.

### dt...@chromium.org (2017-11-08)

jsbell@ flushing input queue is not possible. 

It seems reasonable some timeout to debounce this. Is that possible in the file input control?

I don't think there is anything that I can do in the input stack and it needs to be at the file api/input file control (which is Blink>Forms) to fix this.

### dt...@chromium.org (2017-11-09)

Over to Joshua..

### js...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-12-05)

This is one of our oldest open security bugs (480 days). We really need to get progress on it.

Note that Medium severity bugs are Pri-1, not 2. However, I think this may be worse than Medium. I would call it High; it works too easily. The 'gesture laundering' is quite problematic, as is the default directory (/home on Linux — ?!, and \Users\palmer on Windows).

fortunately, on Linux, the exploit (even the limited one in #2) simply crashes Chrome after grinding for a while. I take it webkitdirectory just doesn't work on Linux? The PoC works reliably on Windows.

Especially since the feature is non-standard and name-prefixed, I think we should consider removing it until we have a good story for how to make this safe. I don't consider it safe at all right now. I'm debating whether we should call it Critical severity, to be honest.

+estark for Security UX thoughts; +owencm for API design thoughts (we've been talking about this in other contexts)

Can someone please test how this behaves on Android? Thanks.

### pa...@chromium.org (2017-12-05)

[Empty comment from Monorail migration]

[Monorail components: -Blink>FileAPI Blink>Forms>File>Directory]

### pa...@chromium.org (2017-12-05)

Re-assigning based on the component. keishi, can you please take a look? Thanks.

### pa...@chromium.org (2017-12-05)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-12-05)

Re #59: this isn't very interesting on Android phones at least, as it requires multiple taps in precise places. Perhaps an Android tablet with an attached keyboard would behave a bit more like Desktop (due to default focus) but I expect not. Further, as far as I can tell, on Android and iOS, the picker acts as a single file picker rather than a folder picker. 

### pa...@chromium.org (2017-12-05)

#63: It sounds like `webkitdirectory` is not supported on Android or iOS, and is non-functional on Linux. That's a point in favor of un-shipping it (at least until we can make it safe), in my view.

### ct...@chromium.org (2017-12-05)

A quick check of our use counters for Blink.UseCounter.Features for PrefixedDirectoryAttribute versus total page visits shows that this appears to be used by a tiny percentage of page visits, which does align with this being non-standard and prefixed (and I think supports un-shipping this for now).

### sh...@chromium.org (2017-12-05)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-12-05)

webkitdirectory is supported on Linux - not sure how you're determining otherwise. It's also supported by Firefox, Edge and Safari (as of Tech Preview 42 I believe); despite the prefix in the name, it was in high enough demand that other browsers implemented support.



### js...@chromium.org (2017-12-05)

[Comment Deleted]

### js...@chromium.org (2017-12-05)

I implemented the suggestion in #55 locally (ignore the result of the dialog if < 500ms between dialog launch and dialog commit). On Linux this seems insufficient; using the focus-switch trick, focus is shifted to to the Input element after the first repeat; on the second repeat the dialog is shown (and the time is recorded); the dialog pops up with focus on the Upload button (which depresses); the dialog then waits until the user releases the Enter key - which could be past the threshold - at which point it commits, with no way for the user to cancel. It may be a better mitigation on other platforms.

Can we re-enumerate the possible mitigations here?

(1) show the picker on key up (so repeat won't be triggered) (#37)
(2) start the picker with focus not on the accept button (platform-specific; may not be possible everywhere)
(3) start the picker with the accept button disabled; enable after some threshold (platform-specific; may not be possible everywhere. what is behavior if the Enter key is held down?) (#54)
(4) ignore the key down if the event is repeating (this only mitigates the specific repro; if focus starts on the input it wouldn't help) (#38)

### es...@chromium.org (2017-12-05)

jsbell do you object to unshipping the webkitdirectory, at least for now? Other than that, it sounds like (1) (#37) is the fastest path to a reliable cross-platform fix?

### js...@chromium.org (2017-12-05)

Unshipping doesn't seem feasible; the usage is relatively high and it is relied upon by Google properties (e.g. Drive) and likely all the other "cloud storage" services (DropBox, etc)

Note that the default UX is so bad that most use of it is via script mapping a click on some more attractive UI to a click() call against the control, so I suspect the "key up" change wouldn't break the web, but I don't know forms/events that well.



### pa...@chromium.org (2017-12-06)

Re #67: The PoC in #2 consistently crashes the entire browser on Linux.

Re #71: Is there a use counter for it? We should at least have that.

It sounds like you're saying gesture laundering is the only way that it works in the field?

### js...@chromium.org (2017-12-06)

> Re #67: The PoC in #2 consistently crashes the entire browser on Linux.

That may be Chrome trying to recurse through the entire file hierarchy of your home directory. The *feature* works, even if the naive POC does not. If you run through a modified repro by initially selecting a subdir then the enter key repetition still behaves per POC.

> Re #71: Is there a use counter for it? We should at least have that.

PrefixedDirectoryAttribute is the right one.

https://www.chromestatus.com/metrics/feature/timeline/popularity/47

No idea about the recent spike, but 0.03% of sites sounds about right. It's that it's a critical feature on those sites. (like Drive)

> It sounds like you're saying gesture laundering is the only way that it works in the field?

If "only" means "primary" and "it works" means "the feature is used" then sure. E.g. run through Drive's UI for "Upload Directory". That's pretty typical.


### js...@chromium.org (2017-12-06)

FWIW, I mocked up the "keyup" approach and sent a sample patch to estark@. "Works for me" but I'm unsure if it's sufficient, i.e. are there tweaks to the POC that bypass it.


### es...@chromium.org (2017-12-06)

I suggest approaching this as follows:

(1) Land the keyup mitigation for webkitdirectory. It's not perfect because an attacker could still trick the user into clicking the upload button or pressing Enter again. But it helps a little bit, on all platforms. And there's no harm in committing a partial fix because the bug is already public.

(2) Land the keyup mitigation for <input type=file> as well. I suggest doing this separately because it seems more likely to cause compat controversy.

(3) Land platform-specific mitigations: change the default directory on Windows and/or see if we can get the timer to work as described in #54. Investigate if similar things are possible on Mac and Linux.

### bu...@chromium.org (2017-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/745e1b4545d51a2ad620d590682ca6eadd95f36c

commit 745e1b4545d51a2ad620d590682ca6eadd95f36c
Author: Joshua Bell <jsbell@chromium.org>
Date: Tue Dec 12 19:28:54 2017

<input type=file webkitdirectory>: Launch picker on Enter keyup

Avoid key repeat triggering an unintentional commit of the subsequent
dialog by launching the picker on the Enter keyup event rather than on
keydown.

Bug: 637098
Change-Id: Ia327a7a9f92c34fd3fcdf971d8c21a5ce744254b
Reviewed-on: https://chromium-review.googlesource.com/814916
Commit-Queue: Joshua Bell <jsbell@chromium.org>
Reviewed-by: Chris Palmer <palmer@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Reviewed-by: Keishi Hattori <keishi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#523507}
[modify] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/LayoutTests/fast/forms/enter-clicks-buttons.html
[add] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/LayoutTests/fast/forms/file/file-input-webkitdirectory-key-enter-prevent-keypress-expected.txt
[add] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/LayoutTests/fast/forms/file/file-input-webkitdirectory-key-enter-prevent-keypress.html
[add] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/LayoutTests/fast/forms/file/file-input-webkitdirectory-key-enter-prevent-keyup-expected.txt
[add] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/LayoutTests/fast/forms/file/file-input-webkitdirectory-key-enter-prevent-keyup.html
[modify] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/Source/core/html/forms/FileInputType.cpp
[modify] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/Source/core/html/forms/FileInputType.h
[modify] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/Source/core/html/forms/KeyboardClickableInputTypeView.cpp
[modify] https://crrev.com/745e1b4545d51a2ad620d590682ca6eadd95f36c/third_party/WebKit/Source/core/html/forms/KeyboardClickableInputTypeView.h


### pa...@chromium.org (2017-12-15)

So how well/not well does the PoC work in a ToT build with #76? Are we done, or is there more to do?

### el...@chromium.org (2017-12-18)

Re #77: I'm not sure what happened, but I don't think the fix in #76 was effective. In https://www.bayden.com/test/upload.asp, if you focus the upload button and hold down Enter, the dialog appears and auto-submits.

Similarly, the POC HTML file attached https://crbug.com/chromium/782842 still works in 65.0.3298.2. 

### el...@chromium.org (2017-12-18)

Re #78: Ah. I'm not sure why the behavior at upload.asp is flaky, but the mitigation is completely bypassed in the POC for 782842 because the attack page simply calls .click() on the control after verifying that the user has the Enter key depressed (this scenario is alluded to in https://crbug.com/chromium/637098#c75.1).

So I don't think we're out of the woods here yet.

### es...@chromium.org (2017-12-19)

I have a WIP patch at https://chromium-review.googlesource.com/c/chromium/src/+/833399 for Mac+Win that disables the OK button until the user changes the selection. Haven't successfully compiled/tested the windows version yet but the mac version defeats the PoC in this bug and 782842. I *think* this might be what Safari is doing as well.

Does anyone have thoughts about this approach? It could be a little annoying from a usability perspective but at this point I think we should prioritize a reliable fix asap, even if it's a little annoying.

### es...@chromium.org (2017-12-19)

(also have not investigated whether the same approach is possible on Linux)

### el...@chromium.org (2017-12-19)

Re #80: The approach for Windows in the WIP looks like it /should/ work, but unfortunately it doesn't, because the Selection change message is getting sent without a user action after initialization. To workaround, we could perhaps require that 500ms or so has passed between BFFM_INITIALIZED and BFFM_SELCHANGED before enabling the button?

(Additionally, compile fails with 
../../ui/shell_dialogs/select_file_dialog_win.cc(532,43):  error: reinterpret_cast from 'int' to 'LPARAM' (aka 'long') is not allowed
    SendMessage(window, BFFM_ENABLEOK, 0, reinterpret_cast<LPARAM>(1)); )

### es...@chromium.org (2017-12-19)

Re: compile fail, yeah I don't have a windows box so I'm compiling on the bots...

Is there anything to distinguish the BFFM_SELCHANGED messages before user action occurs? What's the value of the parameter in those cases? I was hoping to avoid timing stuff because it doesn't seem like half a second is enough for a user to see and process the dialog and realize that they should stop pressing the key... and the longer we go the more annoying it gets.

### el...@chromium.org (2017-12-19)

Re #83: The lParam on the BFFM_SELCHANGED is a PIDL (basically, a reference to the currently-selected path).

Unfortunately, I don't think there's a good way to use this approach that doesn't involve a timer. We could do something whereby we check (via GetAsyncKeyState or whatever) whether the ENTER key is down while the dialog is initializing and refuse to enable the OK button until it's not? 

Alternatively, we could require an out-of-band confirmation from the user that they do indeed want to upload the files (e.g. show a Chrome UI explaining exactly what the web page is going to receive, with no default button).

Another approach would be to select a non-valid path (e.g. "My Computer") as the default, such that Windows doesn't enable the OK button. Unfortunately, it sounds like this may have broken in Windows 10. https://answers.microsoft.com/en-us/insider/forum/insider_wintp-insider_files-insiderplat_pc/problem-with-shbrowseforfolder/a263da47-36f4-433f-b86f-20ef95d60fb8



### es...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-12-19)

Re #83: "it doesn't seem like half a second is enough for a user to see and process the dialog and realize that they should stop pressing the key"

An important point here is that it doesn't really matter if the user stops holding the key; the OK button will be disabled because we disabled it and the user hasn't selected a folder manually. The timer is only needed to prevent non-user-initiated BFFM_SELCHANGED events that occur as Windows expands the tree in the the dialog. 

  struct SelectFolderDialogOptions {
    const wchar_t* default_path;
    bool is_upload;
+   ULONGLONG initialized_tickcount;
  };

Inside if (message == BFFM_INITIALIZED) { if (options->is_upload) { we then disable the OK button and set the initialization tickcount:

      options->initialized_tickcount = GetTickCount64();
      SendMessage(window, BFFM_ENABLEOK, 0, 0);

Then, we reject enabling of the OK button on BFFM_SELCHANGED until a tick count expires:

    SendMessage(window, BFFM_ENABLEOK, 0, 
                static_cast<LPARAM>(
                    (GetTickCount64() - options->initialized_tickcount > 1000) ? 1 : 0 ));


The downside of this approach is that if the user picks a folder in less than a second, they'll have to reselect it to enable the OK button, making it potentially appear flaky.

### es...@chromium.org (2017-12-19)

Oh, I see, that makes sense and sounds okay to me. (I was thinking of the proposal in #53/54.) Is there anyone with a Windows dev environment set up who can build and test elawrence's proposal in #86? I'm trying to get one set up but it will take me a few days at least. (I changed my patch in #80 to be Mac-only.)

### es...@chromium.org (2017-12-19)

Btw meacer noticed that it looks like Edge is doing something different and using some other kind of file upload dialog (?) which doesn't suffer from this problem. Might be https://msdn.microsoft.com/en-us/library/windows/desktop/bb776913(v=vs.85).aspx

### el...@chromium.org (2017-12-19)

RE #87: I've been testing this on Windows for a while. It's effective against the POC's in this bug and https://crbug.com/chromium/782842.

With regard to Edge, yes, I believe it's using the IFileDialog with the FOS_PICKFOLDERS option as suggested by the SHBrowseForFolder documentation. However, using the IFileDialog alone isn't enough (it's what Firefox uses and Firefox is vulnerable to this attack). 

### es...@chromium.org (2017-12-19)

elawrence, are you going to upload your patch for review? I'm hoping someone can submit a fix faster than it takes me to get a Windows build up and running.

### bu...@chromium.org (2017-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/64ef541aad859cc5be38da44863fb1ea24c7c817

commit 64ef541aad859cc5be38da44863fb1ea24c7c817
Author: Emily Stark <estark@google.com>
Date: Tue Dec 19 21:29:51 2017

Mac: do not enable file upload until selection has changed

To avoid files being uploaded without the user realizing, require the
user to change the selection on the file dialog before the OK button
is enabled.

Bug: 637098
Change-Id: Ic6faffb3f6075fb969ae930992d2553162346d02
Reviewed-on: https://chromium-review.googlesource.com/833399
Reviewed-by: ccameron <ccameron@chromium.org>
Commit-Queue: Emily Stark <estark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#525148}
[modify] https://crrev.com/64ef541aad859cc5be38da44863fb1ea24c7c817/ui/shell_dialogs/select_file_dialog_mac.mm


### es...@chromium.org (2017-12-19)

Update: Eric's got a Windows fix up for review, thanks Eric!!!

So that leaves us with linux. +erg and estade: could either of you help us with this high-priority security UX bug? What we'd like to do ideally is disable the OK button on the file upload dialog until the user has changed the file/directory selection. Do you know if that's possible on Linux?

### es...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8dad1bd71cda36807d8b53f7f88ceb5d4227cd00

commit 8dad1bd71cda36807d8b53f7f88ceb5d4227cd00
Author: Emily Stark <estark@chromium.org>
Date: Tue Dec 19 22:40:27 2017

Revert "Mac: do not enable file upload until selection has changed"

This reverts commit 64ef541aad859cc5be38da44863fb1ea24c7c817.

Reason for revert:
(1) The CL fixes the webkitdirectory bug but breaks the normal
<input type=file> upload dialog.
(2) Can fix tapted's nits posted after submit.

Original change's description:
> Mac: do not enable file upload until selection has changed
> 
> To avoid files being uploaded without the user realizing, require the
> user to change the selection on the file dialog before the OK button
> is enabled.
> 
> Bug: 637098
> Change-Id: Ic6faffb3f6075fb969ae930992d2553162346d02
> Reviewed-on: https://chromium-review.googlesource.com/833399
> Reviewed-by: ccameron <ccameron@chromium.org>
> Commit-Queue: Emily Stark <estark@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#525148}

TBR=tapted@chromium.org,ccameron@chromium.org,estark@chromium.org

Change-Id: I885af00fff4f2a20b8a59e8c0dbc8e9f4b4a06fa
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 637098
Reviewed-on: https://chromium-review.googlesource.com/835208
Reviewed-by: Emily Stark <estark@chromium.org>
Commit-Queue: Emily Stark <estark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#525166}
[modify] https://crrev.com/8dad1bd71cda36807d8b53f7f88ceb5d4227cd00/ui/shell_dialogs/select_file_dialog_mac.mm


### av...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-12-19)

Windows CL up at https://chromium-review.googlesource.com/c/chromium/src/+/835068.

### es...@chromium.org (2017-12-21)

I have a patch here[1] for gtk. There's also a KDE file chooser which I didn't change.

Since there's no way to start with no selection, it disables the "open" button until the selection changes. My only misgiving is that if the default selection (first file in the list) is the one the user wants to open, it's unintuitive to have to select something else then re-select the first file. It might even mean they have to navigate to a different directory, then go back again if there's no other file there.

[1] https://chromium-review.googlesource.com/#/c/chromium/src/+/838411

### th...@chromium.org (2017-12-21)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-12-21)

estade@:  I think it would be too frustrating (especially for the single file in a directory case) to wonder why the OK button isn't becoming enabled.

Could we instead enable the OK button only when the enter key is released?  Or not open the dialog at all until it's released?

### es...@chromium.org (2017-12-21)

I implemented that idea as per #92, but now that I look at the windows patch what it actually does is delay acceptance for one second.

### el...@chromium.org (2017-12-21)

RE #100: To be precise, the Windows patch has exactly the same limitation as the gtk patch in #97-- the user must select a different item in the picker in order to enable the OK button. (The timer is used to avoid the problem that Windows sends "the user changed the selection" notifications erroneously during construction of the UI).

While we all agree that the "must select a different file once" behavior is a shortcoming, the alternative near-term proposal is to rip out the API entirely, which would definitely be more disruptive.

In an ideal world, we'd probably have something like what Firefox does for other dialogs (like the Save File prompt) whereby the dialog appears with the Acceptance Button disabled. The UI visually counts down for some short period (e.g. 3 seconds) so the user understands that they cannot accept right away. The problem with getting to that ideal world is that it would almost certainly require doing away with all of our platform-provided file picker UIs and rewriting our own in WebUI or Cocoa/Views, which would be a major project.


### el...@chromium.org (2017-12-21)

WRT #99: The patch in #76 was circumvented because it only handled the case where the dialog was shown because the user ENTER on the control itself. In an attack scenario, the attacker instead triggers the dialog by doing control.click() such that the held ENTER key flows through to the subsequent dialog.

We /could/ have code inside FileInputType::HandleDOMActivateEvent that does the equivalent of: 
  
   while GetAsyncKeyState(VK_RETURN) {
     // pump events
   }

...to avoid allowing a held-down ENTER key from flowing through to the platform-specific file picker dialog. The attacker would need to change their social engineering script to something like "Hit ENTER ten times" or something like that, and pop the dialog between the second and third keystroke.

### th...@chromium.org (2017-12-21)

c#102: I think that's better than having to select a different file.  If we're concerned about the "press enter 10 times" case, then we could combine the solution in #102 with a 1s delay to enable the OK button.

I just want to avoid the scenario where users are confused why the OK button isn't working :)

### el...@chromium.org (2017-12-21)

>  with a 1s delay to enable the OK button.

To be clear, I don't think we have the ability to enable the OK button at a specific time on Windows (and possibly other platforms). 

We *can* prevent the user's selection changes from automatically enabling the OK button for a fixed period of time (that's what the patch in #96 does) but the button does not automatically become enabled when that timer expires.

### th...@chromium.org (2017-12-21)

c#104.  I think it's possible, at least on Linux with the GtkFileChooser.

### es...@chromium.org (2017-12-21)

We had the same issue with selection changing during ui construction on Linux, but we're able to get around that without resorting to a (hacky?) timer by instead ignoring all selection changes that come before the ui is first drawn.

If the question is whether we can switch over to just using a timer completely, I think we can --- but would that solve the problem? If you hold Enter for five seconds it will just delay the confirmation of the selection by one second.

I'm not really that opposed to forcing the user to change the selection. We could add a message within the file chooser (GTK gives us that ability) if it's really that confusing; we could add an extra button or checkbox like the "I am not a robot" captcha; etc. If this is urgent I'd just land as is and worry about UI improvements later.

### el...@chromium.org (2017-12-21)

Re #106: On Windows, we unfortunately get non-user-initiated selection change events both before and after the BFFM_INITIALIZED event.

> If the question is whether we can switch over to just using a 
> timer completely, I think we can --- but would that solve the 
> problem? If you hold Enter for five seconds it will just delay 
> the confirmation of the selection by one second.

I think the hope is that the user, upon seeing the unexpected dialog, would release the Enter key. The concern noted in #83 is "How fast can we reasonably expect the user to react to the unexpected?"




### el...@chromium.org (2018-01-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2018-01-02)

From a security stand point what is the trigger we are using to know the user has recognized the dialog and intentionally pressed enter? An enter after the key repeat delay?

### el...@chromium.org (2018-01-02)

Re #109: Perhaps ideally we would not allow Enter alone to submit the dialog, instead requiring that the user first manually select a folder, as this is a user-gesture that is significantly harder to fake. Unfortunately, the platform-specific dialogs do not seem to generally offer a good mechanism for requesting such behavior.

### sk...@chromium.org (2018-01-03)

On windows I suspect you could inject a windows subclass of the dialog so that you can see mouse/key events. With that ability you could then reenable the button when some key/mouse combination occurs.

### es...@chromium.org (2018-01-17)

I think we need some more help from platform-specific UI experts to get this fixed.

tapted, would you be able to help with a Mac fix as you discussed in https://chromium-review.googlesource.com/c/chromium/src/+/833399#message-6e16fee88103110901b38fd125c8eb5bbaebf3ab?

elawrence/sky, what's the current state of the Windows fix? Do either of you have cycles to keep working on it?

### el...@chromium.org (2018-01-17)

Re #112: I believe the Windows fix at https://chromium-review.googlesource.com/c/chromium/src/+/835068 to be effective, but it results in the user-experience regression that the user is forced to pick a different folder in order to submit. I believe that's a fine tradeoff in a world where the alternative on the table is to remove the Web API entirely.

If the appropriate UX powers-that-be deem that unshippably confusing/bad/etc, we could take a narrower one liner fix that prevents the dialog from appearing until the user releases the ENTER key. That protects against fewer scenarios but is even less likely to be noticed by a user.

### ta...@chromium.org (2018-01-19)

I'm pretty swamped. For reference, the Mac-specific comment from http://crrev.com/c/835068 was

> Patch Set 8:
> 
> > Patch Set 8:
> > 
> > (1 comment)
> > avi@ said:
> > You're already reverting, but here are my thoughts:
> > 
> > You want to enable/disable the OK button. The way you find that button is that you use -[NSView viewWithTag:] to search for the OK button, which is documented to be tagged with NSFileHandlingPanelOKButton. That's what you should be enabling/disabling.

> tapted@ said:
> I played with the POC a bit. I'm not sure disabling the button is right. If someone really wants to pass their desktop folder or some other default `favourite` it's unclear what they need to do to enable the button.
> 
> Mac doesn't key-repeat like other platforms. Also buttons activate on keydown not keyup. I'm not sure this is because of key repeat. I think instead this might be because we are redispatching the event from the webcontents after it didn't preventDefault on it.
> 
> That is, it ends up in command_dispatcher.mm's redispatchKeyEvent where we just do `[NSApp sendEvent:event];`. In most valid use-cases this goes to the mainMenu to activate some menu command like Cmd+L. But Enter gets redispatched too AFAIK.
> 
> Maybe we can check something in redispatchKeyEvent. E.g. if `[owner_ attachedSheet]` is non-nil we probably don't want to redispatch the event.


I haven't done any experiments to see whether this is feasible yet. (if it is, and nothing else breaks, it should be a simple fix)

### ta...@chromium.org (2018-01-19)

So that theory was bung. But I found a much simpler fix: we can just refuse to accept the dialog if the current event is a key-repeat -> https://chromium-review.googlesource.com/875522



### bu...@chromium.org (2018-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/31f50deaacf54de542d01c557cf9f01cab4aa154

commit 31f50deaacf54de542d01c557cf9f01cab4aa154
Author: Trent Apted <tapted@chromium.org>
Date: Mon Jan 22 22:52:10 2018

Mac: Prevent a held-down Enter key from closing the Open File dialog

Bug: 637098
Change-Id: I18ddab35db1ff3155b847576880de4df4e1290ba
Reviewed-on: https://chromium-review.googlesource.com/875522
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Trent Apted <tapted@chromium.org>
Cr-Commit-Position: refs/heads/master@{#531035}
[modify] https://crrev.com/31f50deaacf54de542d01c557cf9f01cab4aa154/ui/shell_dialogs/select_file_dialog_mac.mm


### el...@chromium.org (2018-01-22)

The CL in #116 lands "Prevent a held-down Enter key from closing the Open File dialog" for Mac. I don't think we have a good way to do exactly that for Windows, but it should be pretty easy to do "Delay the Open File dialog from opening until the user releases the ENTER key" which should provide similar protection.

Would this be preferable to the current Windows CL in #113?


### es...@chromium.org (2018-01-24)

Proposal in #117 sounds good to me. I prefer landing an imperfect fix that helps somewhat rather than taking more time to try to come up with something perfect.

### pa...@chromium.org (2018-01-30)

Reminder that this is our oldest High severity security vulnerability (536 days), and is from an external reporter who is probably hoping to get a VRP payout. keishi, can you please make this bug a high priority, or reassign it to someone who can?

And, if that's not possible, I'll reiterate again that the feature is prefixed as well as being unsafe. Unshipping it absolutely should be an option. We can't have High severity bugs in nominally-experimental features for ~ 18 months. +awhalley FYI

### pa...@chromium.org (2018-01-30)

Ahh, I had forgotten about #50. That precludes the possibility of a VRP payout, but does mean we should make this bug public too.

### pa...@chromium.org (2018-01-30)

+jschuh: Can we get a Windows person to write a fix for Windows that will please the code review gods?

### js...@chromium.org (2018-02-02)

Bruce, could you have someone on the Windows side cover this? The right thing seems to be preventing a default directory selection at the interface to blink. However, it also seems that the other platforms have done some whack-a-mole at OS layer, so maybe we just do that for Windows (still assuming the right solution is to prevent a default selection rather than try to race the keypress).

I talked with @palmer about severity. This feels much more medium to me. High severity is reserved for zero-interaction bypass of critical security boundary (such as silent UXSS, RCE, or sandbox escape). I appreciate that it was under-scored originally as low, but given that the user interaction is significant enough to prevent e.g. mass exploitation via a malicious ad network, I feel that medium is the right call.

### br...@chromium.org (2018-02-02)

Acknowledged. I'll make sure this gets dealt with on Windows.

### pb...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### br...@chromium.org (2018-02-02)

Assigning to robliao@ for assessment, although implementation will probably fall to pbos@

### br...@chromium.org (2018-02-02)

Actually assign for assessment...

### pb...@chromium.org (2018-02-05)

Assigning to me per offline discussion.

### pb...@chromium.org (2018-02-05)

[Empty comment from Monorail migration]

### pb...@chromium.org (2018-02-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54

commit 2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54
Author: Peter Boström <pbos@chromium.org>
Date: Thu Feb 22 22:25:46 2018

Add modal confirmation dialog to folder upload

Before this change <input webkitdirectory/> contains a severe security
hole as tricking the user to hold ENTER is sufficient to share a large
swath of their filesystem (for Windows this is usually Desktop).

The exploit works as follows:

1. A site tricks the user into holding ENTER (this is trivial).
2. While detecting that the user is holding ENTER, trigger a hidden
   <input webkitdirectory/> field (input.click()).
3. The folder picker is shown but accepted instantly, which gives the
   site read access to whatever happens to be selected. On my Windows
   machine I've observed this to be the Desktop, but I've seen other
   selections as well (maybe the user folder).

To prevent sharing files without the user's consent this change
introduces a modal interstitial that:

1. Tells the user what's about to be shared (N files, from directory X).
2. Advises the user only to do this for sites they trust.
3. Defaults to Cancel so that the example gesture laundering does not
   work.

This method has a couple of benefits. It provides additional information
to the user which might accidentally have selected the wrong folder and
is about to upload more files than intended. It doesn't rely on
OS-specific behavior, so it provides level protection everywhere. It
also has a lower maintenance cost as it doesn't need to be added for new
platforms or updates to existing OS APIs.

There's opportunity for better laundering protection (such as preventing
the dialog from being accepted too quickly), but the attack surface is
significantly smaller with this mitigation implemented.

According to usage counters <input webkitdirectory/> is used for <0.001%
of page loads (below the consideration-for-deprecation threshold), which
makes the interruption fairly low while providing significant additional
protection against a malicious attacker.

Bug: chromium:637098
Change-Id: I8ac43f8a61cd4476f581b9e57b07cdf88e28f85c
Reviewed-on: https://chromium-review.googlesource.com/929809
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#538590}
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/app/generated_resources.grd
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/file_select_helper.cc
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/file_select_helper.h
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/ui/browser_dialogs.cc
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/ui/browser_dialogs.h
[add] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/ui/views/folder_upload_confirmation_view.cc
[add] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/ui/views/folder_upload_confirmation_view.h
[add] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/browser/ui/views/folder_upload_confirmation_view_browsertest.cc
[modify] https://crrev.com/2a02a69e3173a85fc6ae4f39c7aec28b2ea0da54/chrome/test/BUILD.gn


### pb...@chromium.org (2018-02-22)

#130 adds a confirmation dialog to all browsers building with toolkit_views enabled (this includes Mac). The dialog asks the user to confirm that they wanted to upload N files and which folder was selected. The dialog defaults to Cancel so tricking the user into accepting the dialog without noticing is significantly harder.

There's a few potential additional measures we could do, but given that the API usage is fairly low I'd opt for moving on.

### 93...@gmail.com (2018-02-23)

Since this is quite a nasty vulnerability, would it be possible to have the fix merged? (Just a suggestion, take it or leave it.)

### aw...@google.com (2018-02-26)

pbos@ - we're right up to the last merges before the final 65 Beta - what's your take on the regression risk of these changes? Cheers!

### pb...@chromium.org (2018-02-26)

I would like this change to spin more in Canary/Dev before making that call. The API usage is very low (<0.001% of page loads) so any crash rates or similar will take significantly longer to manifest. I'll do the merge if you want to make that call, but I think we should consider the change virtually untested in Canary until it's spun for a lot longer because of this.

If we have evidence of ongoing abuse that shifts my position here of course (or if you feel strongly about merging this change). I'm kind of shrugging my shoulders here.

### aw...@chromium.org (2018-02-26)

Thanks pbos@. Let's reconsider for a 65 merge after it's made it out to Beta, even if that means only picking it up if there's a stable refresh.

### bu...@chromium.org (2018-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/997810155defb24013257791f46dd1c50310cfc2

commit 997810155defb24013257791f46dd1c50310cfc2
Author: Peter Boström <pbos@chromium.org>
Date: Tue Feb 27 00:41:08 2018

Make OK the default folder-upload-dialog button

Removes the default-button override while maintaining that the focus
should initially be on the cancel button. This makes the "Upload" / OK
button the blue button, which is the expected style, even while not
initially focused to prevent abuse.

Bug: chromium:637098
Change-Id: I63cbd4f69f6d1033a2437691296087f466afbd3f
Reviewed-on: https://chromium-review.googlesource.com/938000
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#539351}
[modify] https://crrev.com/997810155defb24013257791f46dd1c50310cfc2/chrome/browser/ui/views/folder_upload_confirmation_view.cc
[modify] https://crrev.com/997810155defb24013257791f46dd1c50310cfc2/chrome/browser/ui/views/folder_upload_confirmation_view.h


### pb...@chromium.org (2018-02-27)

Update in #136 changes the button styling, attaching screenshot for posterity.

### kr...@chromium.org (2018-02-27)

Tested the issue on mac 10.13.3, win-10 and ubuntu 14.04 using chrome version #66.0.3356.0 using the html file from https://crbug.com/chromium/637098#c2.

Attached screen casts for reference.

Observations on mac:
====================
On opening the PoC-Read-all-Filesv2.html file in mac 10.13.3 and pressing the enter button for 5 seconds, opened a pop up to upload the files from a directory with "upload" and "cancel" button.

Observations on Win-10:
=======================
On opening the PoC-Read-all-Filesv2.html file in win-10 and pressing the enter button for 5 seconds, intermittently opened a pop up to upload the files from a directory with "upload" and "cancel" button as per the screenshot at https://crbug.com/chromium/637098#c137.

Observations on Ubuntu 14.04:
=============================
Fix is working as expected. On opening the PoC-Read-all-Filesv2.html file in ubuntu 14.04 and pressing the enter button for 5 seconds, opened a pop up to upload the files from a directory with "upload" and "cancel" button.

pbos@ - Could you please check the attached screen casts and please let us confirm the fix on OS-Win and OS-Mac.

Thanks...!!

### pb...@chromium.org (2018-02-27)

That you're not getting the interstitial on Mac is because tapted@ has already added some mitigation for when holding Enter in the MacOS folder picker. This can be defeated by making the user press Enter repeatedly instead of holding it.

Looks like WAI on Windows, the text of the page gets changed when it brings up the (that gets instantly accepted). It takes time before you get to confirm it is because it's counting your 45k files, which is unfortunate. There's an alert in there (alert('I can read ' + this.files.length + ' files from anywhere on your pc!');) that would've been triggered if you inadvertently shared files with the site.

Attaching a more visible version that you can use for exploit testing. Click on the <input> field and only press Enter. If nothing happens by just pressing Enter repeatedly (because you cancel the confirmation dialog), then the mitigation is working. If you hit the alert in there then the dialog got accepted by just pressing Enter which isn't expected.

tapted@ also brought to my attention that Mac will accept the default button when pressing Enter regardless of where focus lies, so this has to be revisited for Mac. One suggestion is to not provide a default button (no blue button). I'll have to check with UX, but at least MacOS have some level of mitigation in place.

### pb...@chromium.org (2018-02-27)

To append to #139 I spoke with tapted@, I think we're fine with the current level of mitigation for Mac. This is no longer a silent hold-enter trigger on any platform, any exploit is therefore significantly harder. Given that neither Windows or Mac end up passing files back on to the site by holding Enter, fix lgtm.

### 93...@gmail.com (2018-03-01)

I find it a bit odd that the prompt asking you whether or not you want to allow a website to exploit a security vulnerability to read your files has "OK" as the default button, yet the prompt asking you whether or not you really want an extension from the Chrome Web Store has "Cancel" as the default button.

### aw...@chromium.org (2018-03-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-07)

Hello greencardesh@ - the Chrome VRP panel took a look at this, and given circumstances decided to award $2,000 - cheers!

### aw...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: There is .grd file changes and we are only 31 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@chromium.org (2018-03-16)

This should already be in M66 so I don't know what sheriffbot's deal is here.

### ab...@google.com (2018-03-19)

removed merge-request label

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-07)

[Comment Deleted]

### sa...@gmail.com (2019-07-26)

With this feature in place , a developer looses the opportunity to find if the end user has cancelled the file selection dialog. Before this feature , on focus back to the dom body the file input could be checked for data. Now that the alert also puts the focus back on the body , it is not possible to find if the file upload is in process or has been cancelled . 

### pi...@chromium.org (2019-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-02)

[Comment Deleted]

### [Deleted User] (2020-07-02)

This issue still happens in Mac OS. I have tried and observed in my machine, if I hold the Enter long enough, it will pass file picker and approve the sharing instantly.
Do you intend to revisit this issue, with a new proposal not to provide a default button (no blue button)? With that, user have to click on the OK button to explicit approve the sharing.
I am happy if I could provide the fix if Chrome UX team approves.
pbos@, maybe (sorry if I tag a wrong person), do you agree with that?

### pb...@chromium.org (2020-07-06)

Perhaps it'd be worth visiting/revisiting whether *holding* enter when a Chrome dialog shows should be sufficient to trigger it. That way we'd at least need new input to accept the dialog. I don't know whether that's against any platform behavior that we need to preserve.

If you're interested could you split off a separate new issue and we can continue the discussion there? This has 150+ comments and a lot of people on it who might not need to be on this continued discussion.

### [Deleted User] (2020-07-09)

[Comment Deleted]

### [Deleted User] (2020-07-09)

Thanks, file a new https://crbug.com/chromium/1103609

### er...@microsoft.com (2021-09-01)

Historical note:

Firefox elected to take an approach like Chromium's. https://bugzilla.mozilla.org/show_bug.cgi?id=1338637

Microsoft got this bug for Edge Legacy in 2018 and added the FOS_OKBUTTONNEEDSINTERACTION flag to the Common File Dialogs on Windows 10 RS1. Notably, it's only useful for the Select Folder dialog; it isn't effective against holding ENTER in a general file save dialog.

### is...@google.com (2021-09-01)

This issue was migrated from crbug.com/chromium/637098?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/782842]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085079)*
