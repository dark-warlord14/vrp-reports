# Use-after-free in the filepicker

| Field | Value |
|-------|-------|
| **Issue ID** | [40061594](https://issues.chromium.org/issues/40061594) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views |
| **Platforms** | Android |
| **Reporter** | so...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2022-11-04 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

0. Install chrome, don't allow and dont't deny it to access to the camera (Canary, dev, beta, stable is crashing)

1. Open chrome
2. Open <https://google.com>
3. Switch to desktop view
4. Tap on the camera icon (photo search)
5. Tap on upload file
6. Tap on camera
7. Do not reply to the permission prompt, just tap anywhere else on the screen to close it
8. Tap on camera
9. Do not reply to the permission prompt, just tap anywhere else on the screen to close it
10. Crash

**Problem Description:**  

Please do not trust my analisys at glance, beacuase I have not enough resources to build a debug apk, so I started from the logcat and I tried to analyse the code based on this.

In SelectFileDialog.java at the line 319 it requests permission to the camera. [1]  

When the permission not granted, it calls onFileNotSelected() what calls onFileNotSelected(mNativeSelectFileDialog);  

In onFileNotSelected(mNativeSelectFileDialog) it calls the native method SelectFileDialogImpl::OnFileNotSelected in ui/shell\_dialogs/select\_file\_dialog\_android.cc  

SelectFileDialogImpl::OnFileNotSelected calls listener\_->FileSelectionCanceled(nullptr); [2]

void SelectFileDialogImpl::OnFileNotSelected(  

JNIEnv\* env,  

const JavaParamRef<jobject>& java\_object) {  

if (listener\_)  

listener\_->FileSelectionCanceled(nullptr);  

}

FileSelectionCanceled deletes itself [3]  

void FileSystemChooser::FileSelectionCanceled(void\* params) {  

DCHECK\_CALLED\_ON\_VALID\_SEQUENCE(sequence\_checker\_);  

RecordFileSelectionResult(type\_, 0);  

std::move(callback\_).Run(  

file\_system\_access\_error::FromStatus(  

blink::mojom::FileSystemAccessStatus::kOperationAborted),  

{});  

delete this;  

}

Then when the users taps again

When the permission not granted, it calls onFileNotSelected() what calls onFileNotSelected(mNativeSelectFileDialog);  

In onFileNotSelected(mNativeSelectFileDialog) it calls the native method SelectFileDialogImpl::OnFileNotSelected in ui/shell\_dialogs/select\_file\_dialog\_android.cc  

SelectFileDialogImpl::OnFileNotSelected calls listener\_->FileSelectionCanceled(nullptr), but the listener is already deleted (but not null, so the if is true)

void SelectFileDialogImpl::OnFileNotSelected(  

JNIEnv\* env,  

const JavaParamRef<jobject>& java\_object) {  

if (listener\_) // True, not null  

listener\_->FileSelectionCanceled(nullptr); //<- listener already destroyed here at second call  

}

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java;drc=0b7d10d4ae157cba02a0ed194045b89602911c3a;l=319>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:ui/shell_dialogs/select_file_dialog_android.cc;drc=f08548b51cc2ab6de6134968d597b269187387d8;l=94>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_chooser.cc;drc=0b7d10d4ae157cba02a0ed194045b89602911c3a;l=374>

Regards,  

Peter Nemeth

PS: There is any place when I can download prebuilt debug APK-s?

**Additional Comments:**  

I sent a lot of crashes.  

One-one sample (if you need more I can give more ids)  

Canary: 4ebc25c408b86835  

Stable: 098bafd4eba52541

\*\*Chrome version: \*\* 107.0.5304.91 \*\*Channel: \*\* Stable

**OS:** Android

## Attachments

- [logcat.txt](attachments/logcat.txt) (text/plain, 10.3 KB)
- deleted (application/octet-stream, 0 B)
- [fix.patch](attachments/fix.patch) (text/plain, 486 B)
- [fix-1381455.patch](attachments/fix-1381455.patch) (text/plain, 859 B)
- [Screen_Recording_20230407_144035_Chromium.mp4](attachments/Screen_Recording_20230407_144035_Chromium.mp4) (video/mp4, 8.8 MB)
- [Screen_Recording_20230411_172723_Chromium.mp4](attachments/Screen_Recording_20230411_172723_Chromium.mp4) (video/mp4, 9.7 MB)
- [Screen_Recording_20230424_120646_One UI Home.mp4](attachments/Screen_Recording_20230424_120646_One UI Home.mp4) (video/mp4, 2.3 MB)

## Timeline

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### so...@gmail.com (2022-11-04)

Reproduction video.
Please delete this attachment before you open this ticket to the public. Thank you!

### ke...@chromium.org (2022-11-04)

Thanks or the detailed report!

This doesn't seem to repro on my test phone, but the crash report IDs you provided do suggest a use-after-free. The crashes are segfaults on addresses 0x30 and 0x20, and since `listener_` has been checked for nullptr in the line earlier, I suspect that indicates an overwritten vtable getting used for a method call.

In general this is a known issue (see previous iterations of this form: https://crbug.com/chromium/1201032 and https://crbug.com/chromium/1306391) and we have a bug open tracking a general mitigation to these. I don't want to close this as a duplicate because this needs to be fixed as a one off.

Setting FoundIn as 106 since nothing here appears to be a recent regression, and Severity to High as a browser UAF that requires non-trivial user interaction.

lucmult@: I'm assigning this to you as the owner of https://crbug.com/chromium/1316211, since you already have an idea of what is happening. If you'd rather pass it off to a Views owner then please reassign or let me know.

[Monorail components: Internals>Views]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-11-04)

(auto-cc on security bug)

### so...@gmail.com (2022-11-04)

Thank you for the response and for Your openness!

Yes, it's similar. The main difference is that, if I saw correctly, they found a fault on the positive branch, I found on the negative, or rather the neutral.

Maybe this bug intruduced with the new media picker what shipped around sept., because this has a camera button, without this feature the notselected method never called twice on one instance.

Fixing this, if my assumption above is true, is not too difficult. On the one hand, if it receives a deny signal for a permission what it does not need (e.g. camera), it can simply ignore it. On the other hand, the picker should be closed in the (java) onFileNotSelected method (and this method should only called it if this is really the case).

Of course, this does not rule out calling this native function twice from a compromised renderer, so it might still be worth doing something with that listener (If this case can happen).
Because I can't build the apk, I can't validate this and this is the deepest what I can do in head, I have no usable idea for the listener- problem in the native layer.

Interesting, that you can't reproduce on your test phone. My device is a Samsung Galaxy Note 10+, with Android 12 (august sec. update). The only thing what is unique with this phone is that Samsung ships it here in the EU with the Exynos SOC (others get Qualcom). I don't know that is it matters or not.
Because I can reproduce constantly, just touch me if I can help in the investigation, in testing, or validating anything, or if I can give any relevant info.

Regards,
 Peter 

### lu...@chromium.org (2022-11-06)

Hi all,

https://crbug.com/chromium/1381455#c3 is correct.

I'll assign to finnur@ who was helping me with the Android implementation for file picker.

I think even after my intended refactoring this flow doesn't look 100% correct. 

Finnur, I think when the permission is dismissed we shouldn't call `onFileNotSelected()` [1], because the native/Java UI picker isn't closed.  The C++ implementation in select_file_dialog_android.cc expects this method to be called only once, when the native picker has finished (when it's finishing).

What do you think?

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java;l=323-347;drc=0b7d10d4ae157cba02a0ed194045b89602911c3a

### so...@gmail.com (2022-11-06)

Thank you for the investigation!

In this case, this whole requestpermission callback can go to the trash, since it makes no sense without the onNotFileSelected calls. (Only the 2 checks what can throw runtime exception)

### am...@chromium.org (2022-11-16)

[security marshal] Hello finnur@, it's your friendly neighborhood security marshal, just doing a quick check-in to see if there is any update this issue -or at a minimum this issue can be flipped to Started to reflect investigation or CL you working on that is not visible here? Thank you! 

### fi...@chromium.org (2022-11-17)

Thanks for the report. 

I don't think I'm the right person to own this. Granted, I was marked as owner for SelectFileDialog.java because I added a Java component specifically designed for media uploads, but people keep assuming (because of that) that I'm the expert on all file uploads in Android, which is not the case. I suspect pmonette is a better candidate, having thought about these security issues before.

But I have a couple of points (hope they don't come off as negative in tone, that's not the intent)...

I tried repro'ing using the steps on top with the latest canary (110.0.5423.0). I could not get a repro (I can ask as many times as I want for the permission and click outside the dialog, but see no crash). Perhaps the problem is fixed already?

> Yes, it's similar. The main difference is that, if I saw correctly, they found 
> a fault on the positive branch, I found on the negative, or rather the neutral.

I'm sorry. I don't know what a [ positive | negative | neutral ] branch is...?

> Maybe this bug introduced with the new media picker what shipped around sept., because this has a camera button

Sorry, I'm thoroughly confused by this statement. The current media picker (the one with the Camera button) launched years ago. The last update it had was in February where I added more formats (video support specifically), but I don't think that's what you are referring to. 

Now, I did launch a small scale study (on Stable this month) with a new native Android media picker that replaces the old one, but the (new) Android picker does not have the Camera button you refer to. However, there was a bug introduced where we'd ask for permissions the native Android picker didn't need, but I fixed that here (in Chrome 109):
https://chromiumdash.appspot.com/commit/ac23ab0e902031c7bb58066dcff5abf8d025ebd8

> Fixing this, if my assumption above is true, is not too difficult. 
> On the one hand, if it receives a deny signal for a permission what it does 
> not need (e.g. camera), it can simply ignore it

I don't think this is correct. Not replying back to the renderer breaks subsequent uploads (they are dropped on the floor).

> I think when the permission is dismissed we shouldn't call `onFileNotSelected()` 
> [1], because the native/Java UI picker isn't closed. 

The callback isn't tied to the closing of the dialog. It is, as the name suggests, to let the renderer know the outcome of the operation, so it can do any necessary cleanup.

> In this case, this whole requestpermission callback can go to the trash, since it 
> makes no sense without the onNotFileSelected calls. (Only the 2 checks what can 
> throw runtime exception)

Sorry, I don't know what this means (and given my feedback above it may not be relevant to the discussion).


### ke...@chromium.org (2022-11-17)

> Perhaps the problem is fixed already?

The reporter provided a crash ID generated from Clank canary on November 3, so if it is fixed then it is recent.

sokkis@: Are you still able to reproduce on canary, and if so can you provide the crash ID?

### so...@gmail.com (2022-11-17)

Hi,

Thank you very much for the detailed response!


> But I have a couple of points (hope they don't come off as negative in tone, that's not the intent)...

No, it's not negative, we must speak about it to move things forward, I'm happy with your response. Feel free anytime to response in this way. :)
As you, also I try to reply constructive and I hope it's not seens to be offensive. If yes, then I'm sorry, in this case this is because my bad english.

> I'm sorry. I don't know what a [ positive | negative | neutral ] branch is...?

Positive = When the user selects a file
Negative = When the user doesn't select a file and closes the dialog
Neutral = When the user doesn't select any file and doesn't close the dialog (neither grants nor rejects the permission prompt)


> Sorry, I'm thoroughly confused by this statement. The current media picker...

In this case this was my mistake. Thank you for pointing it out.


> I don't think this is correct. Not replying back to the renderer breaks subsequent uploads (they are dropped on the floor).

You don't need to reply back to the renderer when no reply exists. In my case you can reply that I didn't granted and didn't rejected the camera permission, this is not a valuable info for the renderer. I didn't select any file, I can select files, because I see the dialog, nothing happened until now.
You need to reply when the user closes the dialog, until this point the user can select files and can decide to close the dialog without selecting files.


> The callback isn't tied to the closing of the dialog. It is, as the name suggests, to let the renderer know the outcome of the operation, so it can do any necessary cleanup.

Yes, it's true. But, what is outcome? No outcome exists, I tapped the camera by a mistake then I tapped on an other place because I wouldn't response for the permission request. This is not an outcome, just an intermediate event in the flow, not an important information for the renderer. I didn't select any file, I didn't finish the selection flow, just tapped anything on the screen, and I can continue this progress and select any file or not select and close the dialog in the future.
I mean:
you may call onNoFileSelected only when you closes the dialog. Why? Because this method destroys the connected listener object in the native code. If you call it, but the dialog not closed, the you have a dialog with destroyed native listener. This is why my browser crashing. The native code calls a method on a destroyed listener.


> Sorry, I don't know what this means (and given my feedback above it may not be relevant to the discussion).

It's relevant to me, because I don't agree with a part of your feedback. :-)
I did a mistake, the last "if" and the last noFileSelected is needed, this is the case when we can not open the dialog, but the first if block not necessery. This is what would I do (but keep in mind I can't try it, so maybe this is a mistake from me):

```
            window.requestPermissions(requestPermissions, (permissions, grantResults) -> {
                for (int i = 0; i < grantResults.length; i++) {
                    if (grantResults[i] == PackageManager.PERMISSION_DENIED) {
//                        if (mCapture) {
//                            onFileNotSelected();
//                            return;
//                        }
                        // TODO(finnur): Remove once we figure out the cause of crbug.com/950024.
                        if (shouldUsePhotoPicker) {
                            if (permissions.length != requestPermissions.length) {
                                throw new RuntimeException(
                                        String.format("Permissions arrays misaligned: %d != %d",
                                                permissions.length, requestPermissions.length));
                            }

                            if (!permissions[i].equals(requestPermissions[i])) {
                                throw new RuntimeException(
                                        String.format("Permissions arrays don't match: %s != %s",
                                                permissions[i], requestPermissions[i]));
                            }
                        }

                        if (shouldUsePhotoPicker) {
                            if (permissions[i].equals(storagePermission)
                                    || permissions[i].equals(PermissionConstants.READ_MEDIA_IMAGES)
                                    || permissions[i].equals(
                                            PermissionConstants.READ_MEDIA_VIDEO)) {
                                onFileNotSelected();
                                return;
                            }
                        }
                    }
                }
```

> I tried repro'ing using the steps on top with the latest canary (110.0.5423.0). I could not get a repro (I can ask as many times as I want for the permission and click outside the dialog, but see no crash). Perhaps the problem is fixed already?

I can reproduce with the latest canary. I really don't know why you can't reproduce it, it's really interesting for me, because I can repro it anytime.

Thanks again for you constructive response! I hope you find my answer meaningful and constructive.

Peter

### so...@gmail.com (2022-11-17)

Hi @kenrb,

Sorry I didn't see you question.

Here are 2 fresh crash IDs:

7b739900bfa6d824
7f37d1ee9ec1a008

Regards,
 Peter

### so...@gmail.com (2022-11-17)

Oh sorry, a mistake. The two crash in my prevoius comment belongs to the prev. canary version.

Here are two from the latest canary:
d4cd35dc3e1c4f73
d33ed4b985de66b5

Sorry,
 Peter

### lu...@chromium.org (2022-11-17)

About the reproduction steps, one subtle detail is that you have to switch to "Desktop site" to see that file picker.

I just tried again on my phone chrome 107.0.5304.105 and I can still repro.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

finnur: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-12-06)

[security marshall] Hello, just following up on status and next steps for this issue.
finnur@ suggested pmonette@ may be a better person to tackle this issue. Should they become the new owner of this bug?
lucmult@, kenrb@ - Please help if you can re-assign as appropriate. Thank you!

### [Deleted User] (2022-12-17)

finnur: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-12-19)

[security marshal] Friendly ping to move this issue forward. pmonette@, should this issue (see https://crbug.com/chromium/1381455#c11) be assigned to you instead? I've also reached out to you (and CC'd kenrb@, lucmult@, finnur@) via email ICYMI.

### so...@gmail.com (2022-12-19)

Maybe this patch will fix the crash (but it needs testing)

### an...@chromium.org (2022-12-20)

Thanks for the patch, reporter!
finnur@, pmonette@ - can anyone take a look and comment?

### pm...@chromium.org (2022-12-20)

I looked at the patch and it seems resonable. I made a slightly different fix which I think is clearer and more generic. I am not sure if it truly fixes the issue because I can't build it myself easily but I'll test it on the dev build when my fix reaches that channel. In any case my change (and suggested patch) is correct, even if it doesn't fix the issue.

https://chromium-review.googlesource.com/c/chromium/src/+/4117255
CC'ed the reviewer to this bug.

### so...@gmail.com (2022-12-20)

Yes, your patch is more clean than my, this is the correct way to null this listener :-)
Thank you for the investigation.

### ma...@google.com (2022-12-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ebc535683771cf049f5b411e1b8d1e2b14d600b5

commit ebc535683771cf049f5b411e1b8d1e2b14d600b5
Author: Patrick Monette <pmonette@chromium.org>
Date: Wed Dec 21 21:54:23 2022

Call ListenerDestroyed() in FileSelectHelper::RunFileChooserEnd()

The contract of the SelectFileDialog API specifies that
ListenerDestroyed() must be invoked whenever you no longer want the
listener to be called back by the dialog.

Bug: 1381455
Change-Id: I43da9364b4f8494353eb42e64ef2c1cf8c022bb7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117255
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1086097}

[modify] https://crrev.com/ebc535683771cf049f5b411e1b8d1e2b14d600b5/chrome/browser/file_select_helper.cc


### pm...@google.com (2022-12-22)

+cc reviewer for similar CL

### gi...@appspot.gserviceaccount.com (2022-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/971c3e94172e1d82cf4e07f7dc7bcb57b89720cd

commit 971c3e94172e1d82cf4e07f7dc7bcb57b89720cd
Author: Patrick Monette <pmonette@chromium.org>
Date: Thu Dec 22 16:51:56 2022

[weblayer] Call ListenerDestroyed in FileSelectHelper::RunFileChooserEnd

The contract of the SelectFileDialog API specifies that
ListenerDestroyed() must be invoked whenever you no longer want the
listener to be called back by the dialog.

Bug: 1381455
Change-Id: I6655b8c005ddf455157fc6ef7e0de807d7931f52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4120597
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Peter Beverloo <peter@chromium.org>
Auto-Submit: Patrick Monette <pmonette@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1086391}

[modify] https://crrev.com/971c3e94172e1d82cf4e07f7dc7bcb57b89720cd/weblayer/browser/file_select_helper.cc


### [Deleted User] (2023-01-03)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pm...@chromium.org (2023-01-04)

I tried to repro manually on Chrome Canary 111.0.5518.0 and it still crashes (my change landed in 111.0.5492.0) so I didn't fix the issue.

The crash report doesn't contain the full call stack (with the java bits) and is not super useful. finnur@ and lucmult@ can you advise on how to make sense of an android crash? Do I need to make my own local build?

### fi...@chromium.org (2023-01-05)

Normally, I would do a local build and if the crash stack looks obfuscated, I save it to a file (crash.txt) and run this command:

./third_party/android_platform/development/scripts/stack --output-directory out/default crash.txt

(this is also assuming my freshly built binaries are in out/default).

There is probably a way to get this to work with pre-existing symbol files, but if you already build Chromium you might as well build the Android binaries on Linux, because after you see the real stack you'd want to test your changes and that it is much easier to do if you have a build with your own symbols.

You should be able to build for Android easily from your current codebase. I switch between Linux/ChromeOS and Android and build regularly from the same tree each time.

For example, my .gclient file now has:

  target_os = [ 'android', 'chromeos' ]

and I build via:

  autoninja -C out/default chrome_public_apk

To run the binaries, I use:

  out/default/bin/chrome_public_apk run --args='--disable-death-ray' http://example.com

... and you can use a phone or an emulator to run it on. Android Studio has one and there's a good internal system I use when on corp machines. It is super easy to use.

Note that I skipped some setup steps above, for example you need to run gclient sync at least once, and run build/install-build-deps-android.sh but it should be relatively painless. More details here:

https://chromium.googlesource.com/chromium/src/+/main/docs/android_build_instructions.md



### ja...@chromium.org (2023-02-03)

[security marshal] Hi pmonette@ can you provide an update? Did you manage to land a fix for this? Or are you still able to reproduce the issue?

### ja...@chromium.org (2023-02-06)

Setting NextAction date to check back in for an update.

### wf...@chromium.org (2023-02-07)

[security marshal] https://crbug.com/chromium/1381455#c31 seems to imply this isn't yet fixed, I wonder if there was any progress made on this High severity security bug?

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### so...@gmail.com (2023-04-07)

Hi,

I finally managed to build an android version. It wasn't easy, because I don't use ubuntu and my phone's USB-C connector was dead, wireless adb didn't want to work, the emulator didn't want to start, finally my laptop power supply breaked. :D But in the end it worked, now I have a full functionality build enviroment for android and there is a solution for this bug.

The problem is similar to what I first thought, but not there. On line 602 of SelectFileDialog.java, if it doesn't get access to the camera, it calls onFileNotSelected method. This is not ok, because in this case nothing has happened yet. The user can choose files, the dialog remains open.

I am attaching the patch file. With this small modification it will be fixed. As you can see in the attached video, I can't kill the app, but all functionality is fully preserved. I searched for similar problems, but I not found any other issue with this method call.

A hope it helps.

Regards,
Peter

### so...@gmail.com (2023-04-07)

This bug maybe introduced in 2018, so it is more than 4 years old. :-) The bug maybe existed early, but because it was an other bug (the camera button disappered when it did not get the permission) it was not invokeable until the other bug fixed in 2018. :D
I think that the combination of this two commit is the reason, but it is a really old code, so it is hard to identify and maybe it does not matter after 5 years. 

https://source.chromium.org/chromium/chromium/src/+/5c781b7e8fde9009a05c769812b08640c4310cd8
https://source.chromium.org/chromium/chromium/src/+/52a6313050e4a77dd702652cb9157029c37c445e

### me...@chromium.org (2023-04-11)

(pinged pmonette@ offline)

### fi...@chromium.org (2023-04-11)

The same crash happens here also...

0. Start by taking a photo with the device (any photo will do). 
1. Install Chrome, don't allow and don't deny it access to the camera
2. Open Chrome
3. Open https://google.com
4. Switch to desktop view
5. Tap on the camera icon (photo search)
6. Tap on upload file
7. Tap on camera
8. Do not reply to the permission prompt, just tap anywhere else on the screen to close it
9. Select the photo you took (in step 0) from the photo grid
10. Crash


I offered to Patrick to take a look, since I have the setup already to test this locally.

### so...@gmail.com (2023-04-11)

I tried this steps Canary: crashes. But my patch fixes this also.

### so...@gmail.com (2023-04-11)

Just to make sure I tried good steps.

### pm...@chromium.org (2023-04-11)

Thanks for the investigation and the patch!

### fi...@chromium.org (2023-04-11)

Yes, I agreed with your analysis: Removing the onFileNotSelected seems correct and I expected it to also fix the crash I mentioned in https://crbug.com/chromium/1381455#c44. Thanks for verifying. 

### so...@gmail.com (2023-04-12)

Thank you! Please ping me, if I can do anything else.

Have a fine day!
Peter

### gi...@appspot.gserviceaccount.com (2023-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fac91c97973d1c610407c8115d35ef42129800e3

commit fac91c97973d1c610407c8115d35ef42129800e3
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Fri Apr 21 15:12:57 2023

[Android/MediaPicker]: Fix crash when dismissing permissions.

When dismissing the Camera permission prompt, we were
erroneously calling onFileNotSelected(), which ends the
pipeline prematurely, since the dialog is still up and
active. By removing that call, the dialog can continue
with the upload process.

Also added a few tests to exercise this path and other
similar ones.

Bug: 1381455
Change-Id: Ia58bd9f060905d9fc43abccbc948d93062352a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4447677
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1133820}

[modify] https://crrev.com/fac91c97973d1c610407c8115d35ef42129800e3/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/fac91c97973d1c610407c8115d35ef42129800e3/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### so...@gmail.com (2023-04-22)

finnur@:

Thank you very much for your cooperation and help! Today, I retested the merged fix for safety reasons and everything is working well.

Have a nice day!
Peter






### so...@gmail.com (2023-04-24)

Oh, I found an other issue that this bug has been masking so far. If you quickly tap the camera icon (similar to before, without granting camera permission, just rapidly tapping the camera icon. You should tap very quick), then the android system will invoke the callback in the following block with a zero-length array after a lot of taps (I don't know why android do this, there is no reason for this):

mWindowAndroid.requestPermissions(new String[] {Manifest.permission.CAMERA},
                            (permissions, grantResults) -> {
                                assert grantResults.length == 1; //<- Debug builds crash here
                                if (grantResults[0] == PackageManager.PERMISSION_DENIED) { // <- release builds crash here
                                    return;
                                }
                                new GetCameraIntentTask(true, mWindowAndroid, this)
                                        .executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                            });

While an assert statement checks for this, it will only fail in debug builds, but in release builds, it will over-index the grantResults array in the if statement, causing an ArrayIndexOutOfBoundsException.

This can also be considered a separate issue, but I thought that since we're here, it's worth fixing it as well. Maybe it's not complicated, I think that we just need to replace the assert with an if statement:

mWindowAndroid.requestPermissions(new String[] {Manifest.permission.CAMERA},
                            (permissions, grantResults) -> {
                                if (grantResults.length < 1) {
                                    return;
                                }
                                if (grantResults[0] == PackageManager.PERMISSION_DENIED) {
                                    return;
                                }
                                new GetCameraIntentTask(true, mWindowAndroid, this)
                                        .executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                            });


Please let me know if this should be treated as a separate issue, in which case I will submit a new stability crash ticket with this and my proposal for a fix!

Stack trace from my debug build:
2023-04-24 12:10:12.854 org.chromium.chrome E/AndroidRuntime: FATAL EXCEPTION: main
    Process: org.chromium.chrome, PID: 20542
    java.lang.AssertionError
        at org.chromium.ui.base.SelectFileDialog.lambda$onPhotoPickerUserAction$1$org-chromium-ui-base-SelectFileDialog(SelectFileDialog.java:627)
        at org.chromium.ui.base.SelectFileDialog$$ExternalSyntheticLambda0.onRequestPermissionsResult(Unknown Source:2)
        at org.chromium.ui.permissions.AndroidPermissionDelegateWithRequester.handlePermissionResult(AndroidPermissionDelegateWithRequester.java:127)
        at org.chromium.ui.base.WindowAndroid.handlePermissionResult(WindowAndroid.java:487)
       ....

Stack trace from Canary:
2023-04-23 23:59:44.748 ? E/AndroidRuntime: FATAL EXCEPTION: main
    Process: com.chrome.canary, PID: 7435
    java.lang.ArrayIndexOutOfBoundsException: length=0; index=0
        at DM2.b(chromium-TrichromeChromeGoogle6432.aab-canary-572900039:16)
        at A5.f(chromium-TrichromeChromeGoogle6432.aab-canary-572900039:162)
        at org.chromium.ui.base.WindowAndroid.f(chromium-TrichromeChromeGoogle6432.aab-canary-572900039:5)
        at Li.onRequestPermissionsResult(chromium-TrichromeChromeGoogle6432.aab-canary-572900039:5)
        at android.app.Activity.requestPermissions(Activity.java:5363)
        ...

Regards,
 Peter

### so...@gmail.com (2023-04-24)

"I don't know why android do this, there is no reason for this"
MaybeI know. :-)
Quote from the documentation https://developer.android.com/reference/android/app/Activity.html#onRequestPermissionsResult(int,%20java.lang.String[],%20int[])

Note: It is possible that the permissions request interaction with the user is interrupted. In this case you will receive empty permissions and results arrays which should be treated as a cancellation.

Maybe when I click anywhere else, then it's a permission denial. If I click on the button and ask again for the permission while the first permission request is not finished, then it is a cancellation and the result array is empty.

### gi...@appspot.gserviceaccount.com (2023-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f183491b38cf8a4703f0f21bc58da90af3fc63c4

commit f183491b38cf8a4703f0f21bc58da90af3fc63c4
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Tue Apr 25 10:55:01 2023

[Android/MediaPicker]: Fix crash during permission interrupt

When the permission dialog is interrupted, Android can call
the callback with empty arrays. This must be handled correctly.

Bug: crbug.com/1381455 (see https://crbug.com/chromium/1381455#c52)
Change-Id: I2abe3351b82005cdef423c5f021d4fab3a8bf64a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4467669
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1135120}

[modify] https://crrev.com/f183491b38cf8a4703f0f21bc58da90af3fc63c4/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/f183491b38cf8a4703f0f21bc58da90af3fc63c4/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### fi...@chromium.org (2023-04-25)

Thanks for the report, Peter! (and for the documentation link)

I didn't know that requestPermissions could send an empty string array when the request was interrupted. It would seem more logical to send a deny message. :)

But, it is fixed now (and the original issue as well)! :)

I think we can close this now. Feel free to let me know if this does not fix your issue.

And a reminder to anyone looking at making this public. See the request in https://crbug.com/chromium/1381455#c2.

### fi...@chromium.org (2023-04-25)

[Empty comment from Monorail migration]

### so...@gmail.com (2023-04-25)

Yes, now the original issue and the other hidden by it have been fixed. Luckily I don't see any more. :D
Thank you very much again for your help, I learned a lot from this issue too!

### fi...@chromium.org (2023-04-25)

Well, thank you for sticking with us and for the level of effort you put in!

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd9caec306ad7cc3308651a2fcf0c6d70a58540d

commit bd9caec306ad7cc3308651a2fcf0c6d70a58540d
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Tue Apr 25 17:31:39 2023

[Android/MediaPicker]: Flesh out the test a bit more.

Bug: 1381455
Change-Id: Ic825efece372dc238d841919582fdbbba870c4a9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4471970
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1135336}

[modify] https://crrev.com/bd9caec306ad7cc3308651a2fcf0c6d70a58540d/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java


### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

Requesting merge to stable M112 because latest trunk commit (1135336) appears to be after stable branch point (1109224).

Requesting merge to beta M113 because latest trunk commit (1135336) appears to be after beta branch point (1121455).

Merge review required: M112 is already shipping to stable.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-25)

Thanks for landing the fix for this issue. As this fix just landed a few hours ago and RC cut for M113/Stable release next week is currently taking place right now, let's let this fix get appropriate bake time on Canary and I'll revisit for merge review and approval Thursday or Friday. 
This fix should ship in the next updates of M113/Stable and M112/Extended. 

### [Deleted User] (2023-04-26)

Merge review required: M113 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-02)

https://chromium-review.googlesource.com/c/chromium/src/+/4447677 
https://chromium-review.googlesource.com/c/chromium/src/+/4467669
-- tentatively approved for backmerge for M113 and M112. Please ensure there are no stability/performance or other issues prior to backmerging these fixes
if no issue or other concerns/risks, please backmerge to M113 branch 5672 and M112 branch 5615 at your earliest convenience so this fix can be included in the next updates of M113 Stable and M112 Extended Stable -- thank you! 



### am...@google.com (2023-05-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-05)

Congratulations! The VRP Panel had decided to award you $1,000 for this report of a highly mitigated issue. Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2023-05-05)

While I am here, finnur@ during further evaluation, there was no concrete evidence in data remaining of a UAF and this looked like a null pointer deref. All the crash reports provided in the course of this issue were no longer available so make a solid determination. Regardless, this issue is significantly mitigated and I'm going to suggest avoiding a backmerge here. Apologies for making this determination only after I originally approved the merges and you staged the CPs. 


### so...@gmail.com (2023-05-05)

Hi amyressler,@

Is this a null deref? 0x38313a30303a40 is zero? :-)

2022-11-04 10:53:31.501 ? A/DEBUG: signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x38313a30303a40

All the crash reports provided in the course of this issue were no longer available.
It was, when I posted this issue in november. I'm sorry, but I don't think it's something I have any control over.  Or should I have found the solution and patch a few months earlier? Overall, the content of your message is very hurtful to me (no, it's not the amount of reward that matters to me)


### fi...@chromium.org (2023-05-05)

> Apologies for making this determination only after I originally approved the merges and you staged the CPs.

No worries.

Also, I don't have insight/influence into the rewards panel, but just wanted to say a big thanks to Peter (sokkis@) for sticking with this for so long, proposing a fix and verifying the final outcome (and finding an additional crash on top of that). It showed real dedication and I'm really appreciative. Thank you!

### so...@gmail.com (2023-05-05)

@finnur: Thank you very much! :-)

---

amyressler@: First of all, sorry, I was a bit cranky this morning.

"All the crash reports provided in the course of this issue were no longer available so make a solid determination"

Actually, we can very easily help with the problem that there are no more crash reports because they have been deleted. 4-5 taps and here is the new one, the latest stable version 112, SEGFAULT at address 0x3033353633. The address is not fixed, so much so that sometimes it can actually go low to null deref (0x10 - 0x31), but in most cases it ranges between 0x100000000 and 0x700000000. So here is today's crash report from the stable release and a logcat. That doesn't seem like a null deref to me at address 0x3033353633. It is certainly highly mitigated, but it is a beautiful example of use after free, which is very difficult to grasp and fix.

Crash report ID: 89de8ec1067a8883

If you can see the others from my phone, I sent a lot of crash reports, it cointains null derefs and use after frees between the 0x100000000 and 0x700000000 addresses. (And 1-2 ArrayIndexOutOfBounds exception for gratis, this is the other bug what we fixed with finnur. :-) )

If you have any questions don't hesitate to ask me. 

Have a fine day! :)
Peter

2023-05-05 15:03:10.345 ? A/libc: Fatal signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x3033353633 in tid 23679 (.android.chrome), pid 23679 (.android.chrome)
2023-05-05 15:03:10.720 ? A/DEBUG: *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
2023-05-05 15:03:10.720 ? A/DEBUG: Build fingerprint: 'samsung/d2seea/d2s:12/SP1A.210812.016/N975FXXS8HWA1:user/release-keys'
2023-05-05 15:03:10.720 ? A/DEBUG: Revision: '24'
2023-05-05 15:03:10.720 ? A/DEBUG: ABI: 'arm64'
2023-05-05 15:03:10.720 ? A/DEBUG: Processor: '6'
2023-05-05 15:03:10.720 ? A/DEBUG: Timestamp: 2023-05-05 15:03:10.420527826+0200
2023-05-05 15:03:10.720 ? A/DEBUG: Process uptime: 22s
2023-05-05 15:03:10.720 ? A/DEBUG: Cmdline: com.android.chrome
2023-05-05 15:03:10.720 ? A/DEBUG: pid: 23679, tid: 23679, name: .android.chrome  >>> com.android.chrome <<<
2023-05-05 15:03:10.720 ? A/DEBUG: uid: 10210
2023-05-05 15:03:10.720 ? A/DEBUG: signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x3033353633
2023-05-05 15:03:10.720 ? A/DEBUG:     x0  1500003033353633  x1  0000007382f69968  x2  000000700300efa0  x3  0000007fe3533580
2023-05-05 15:03:10.720 ? A/DEBUG:     x4  0000000000000000  x5  0000000000000000  x6  0000000000000000  x7  0000000000000000
2023-05-05 15:03:10.720 ? A/DEBUG:     x8  33f27cc0c4518231  x9  33f27cc0c4518231  x10 0000000000430000  x11 0000000000000000
2023-05-05 15:03:10.720 ? A/DEBUG:     x12 0000000000000000  x13 0000000000000000  x14 00000000000000c0  x15 00002bc53a75a0ec
2023-05-05 15:03:10.720 ? A/DEBUG:     x16 0000007fe3533580  x17 0000000000000070  x18 00000076af046000  x19 000000750edb0010
2023-05-05 15:03:10.720 ? A/DEBUG:     x20 0000000000000000  x21 0000000000000007  x22 00000073850398ac  x23 000000738508cff2
2023-05-05 15:03:10.720 ? A/DEBUG:     x24 000000739c608d00  x25 0000007fe3533598  x26 0000007fe35335a4  x27 0000007fe3533598
2023-05-05 15:03:10.720 ? A/DEBUG:     x28 0000007fe35335b0  x29 0000007fe35335a4
2023-05-05 15:03:10.720 ? A/DEBUG:     lr  0000007326d7f8d8  sp  0000007fe35334c0  pc  00000073145f9e98  pst 0000000020000000
2023-05-05 15:03:10.720 ? A/DEBUG: backtrace:
2023-05-05 15:03:10.720 ? A/DEBUG:       #00 pc 0000000005992e98  /data/app/~~43wMnQXRpA-g9KOKpx_rXQ==/com.google.android.trichromelibrary_561513634-x-hTseEJu-5QKksaatErtQ==/base.apk!libmonochrome_64.so (Java_J_N_MGVJOCWv+12) (BuildId: 59bbf83e545eb5c992b12e691ff7d93b6a4b2830)
2023-05-05 15:03:10.720 ? A/DEBUG:       #01 pc 00000000000828d4  /data/app/~~bVsdxOV39HLFS3e1nPsXyw==/com.android.chrome-xhyMZd7ocX46x--Qo4Y27w==/oat/arm64/base.odex (art_jni_trampoline+116)
2023-05-05 15:03:10.720 ? A/DEBUG:       #02 pc 0000000000211d0c  /apex/com.android.art/lib64/libart.so (nterp_helper+1948) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.720 ? A/DEBUG:       #03 pc 000000000021c8ac  /data/app/~~bVsdxOV39HLFS3e1nPsXyw==/com.android.chrome-xhyMZd7ocX46x--Qo4Y27w==/base.apk (org.chromium.ui.base.SelectFileDialog.m+16)
2023-05-05 15:03:10.720 ? A/DEBUG:       #04 pc 00000000002124c4  /apex/com.android.art/lib64/libart.so (nterp_helper+3924) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.720 ? A/DEBUG:       #05 pc 000000000018e9ce  /data/app/~~bVsdxOV39HLFS3e1nPsXyw==/com.android.chrome-xhyMZd7ocX46x--Qo4Y27w==/base.apk (pJ2.b+26)
2023-05-05 15:03:10.720 ? A/DEBUG:       #06 pc 00000000002132e4  /apex/com.android.art/lib64/libart.so (nterp_helper+7540) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.720 ? A/DEBUG:       #07 pc 00000000000a3a54  /data/app/~~bVsdxOV39HLFS3e1nPsXyw==/com.android.chrome-xhyMZd7ocX46x--Qo4Y27w==/base.apk (n5.h+304)
2023-05-05 15:03:10.720 ? A/DEBUG:       #08 pc 00000000002132e4  /apex/com.android.art/lib64/libart.so (nterp_helper+7540) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.720 ? A/DEBUG:       #09 pc 000000000021dedc  /data/app/~~bVsdxOV39HLFS3e1nPsXyw==/com.android.chrome-xhyMZd7ocX46x--Qo4Y27w==/base.apk (org.chromium.ui.base.WindowAndroid.h+8)
2023-05-05 15:03:10.720 ? A/DEBUG:       #10 pc 00000000002124c4  /apex/com.android.art/lib64/libart.so (nterp_helper+3924) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.720 ? A/DEBUG:       #11 pc 000000000013cafc  /data/app/~~bVsdxOV39HLFS3e1nPsXyw==/com.android.chrome-xhyMZd7ocX46x--Qo4Y27w==/split_chrome.apk (ki.onRequestPermissionsResult+8)
2023-05-05 15:03:10.720 ? A/DEBUG:       #12 pc 0000000000703f84  /system/framework/arm64/boot-framework.oat (android.app.Activity.dispatchActivityResult+1492) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.720 ? A/DEBUG:       #13 pc 00000000004fd004  /system/framework/arm64/boot-framework.oat (android.app.ActivityThread.deliverResults+548) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.720 ? A/DEBUG:       #14 pc 000000000051914c  /system/framework/arm64/boot-framework.oat (android.app.ActivityThread.handleSendResult+1052) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #15 pc 0000000000735e14  /system/framework/arm64/boot-framework.oat (android.app.servertransaction.ActivityResultItem.execute+132) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #16 pc 0000000000716600  /system/framework/arm64/boot-framework.oat (android.app.servertransaction.ActivityTransactionItem.execute+96) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #17 pc 000000000041c0e8  /system/framework/arm64/boot-framework.oat (android.app.servertransaction.TransactionExecutor.executeCallbacks+1944) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #18 pc 000000000041b898  /system/framework/arm64/boot-framework.oat (android.app.servertransaction.TransactionExecutor.execute+984) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #19 pc 00000000004f7e3c  /system/framework/arm64/boot-framework.oat (android.app.ActivityThread$H.handleMessage+1484) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #20 pc 000000000078d33c  /system/framework/arm64/boot-framework.oat (android.os.Handler.dispatchMessage+188) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #21 pc 000000000079058c  /system/framework/arm64/boot-framework.oat (android.os.Looper.loopOnce+1036) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #22 pc 00000000007900e4  /system/framework/arm64/boot-framework.oat (android.os.Looper.loop+516) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #23 pc 000000000050d770  /system/framework/arm64/boot-framework.oat (android.app.ActivityThread.main+800) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #24 pc 0000000000218be8  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+568) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #25 pc 000000000028520c  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+212) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #26 pc 0000000000627760  /apex/com.android.art/lib64/libart.so (_jobject* art::InvokeMethod<(art::PointerSize)8>(art::ScopedObjectAccessAlreadyRunnable const&, _jobject*, _jobject*, _jobject*, unsigned long)+1384) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #27 pc 0000000000597a38  /apex/com.android.art/lib64/libart.so (art::Method_invoke(_JNIEnv*, _jobject*, _jobject*, _jobjectArray*)+48) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #28 pc 00000000000b2f74  /apex/com.android.art/javalib/arm64/boot.oat (art_jni_trampoline+132) (BuildId: cb3f7d683b4276aeb0f07ebac9fc30ac8eefbaa9)
2023-05-05 15:03:10.721 ? A/DEBUG:       #29 pc 0000000000ae27bc  /system/framework/arm64/boot-framework.oat (com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run+140) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #30 pc 0000000000aebbe8  /system/framework/arm64/boot-framework.oat (com.android.internal.os.ZygoteInit.main+2376) (BuildId: f519502c52bf7011435c2899d175b46f19202f80)
2023-05-05 15:03:10.721 ? A/DEBUG:       #31 pc 0000000000218be8  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+568) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #32 pc 000000000028520c  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+212) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #33 pc 0000000000627ec0  /apex/com.android.art/lib64/libart.so (art::JValue art::InvokeWithVarArgs<art::ArtMethod*>(art::ScopedObjectAccessAlreadyRunnable const&, _jobject*, art::ArtMethod*, std::__va_list)+448) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #34 pc 0000000000628394  /apex/com.android.art/lib64/libart.so (art::JValue art::InvokeWithVarArgs<_jmethodID*>(art::ScopedObjectAccessAlreadyRunnable const&, _jobject*, _jmethodID*, std::__va_list)+92) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #35 pc 0000000000501094  /apex/com.android.art/lib64/libart.so (art::JNI<true>::CallStaticVoidMethodV(_JNIEnv*, _jclass*, _jmethodID*, std::__va_list)+612) (BuildId: 600193f4a9fcf9ced238223aee6c1164)
2023-05-05 15:03:10.721 ? A/DEBUG:       #36 pc 00000000000b2b28  /system/lib64/libandroid_runtime.so (_JNIEnv::CallStaticVoidMethod(_jclass*, _jmethodID*, ...)+120) (BuildId: f84f32a05859391d762aeab6c7145b7b)
2023-05-05 15:03:10.721 ? A/DEBUG:       #37 pc 00000000000becd8  /system/lib64/libandroid_runtime.so (android::AndroidRuntime::start(char const*, android::Vector<android::String8> const&, bool)+856) (BuildId: f84f32a05859391d762aeab6c7145b7b)
2023-05-05 15:03:10.721 ? A/DEBUG:       #38 pc 00000000000025b0  /system/bin/app_process64 (main+1368) (BuildId: 9a7b5029aaf92752a6307785aa874b5a)
2023-05-05 15:03:10.721 ? A/DEBUG:       #39 pc 0000000000049b40  /apex/com.android.runtime/lib64/bionic/libc.so (__libc_init+96) (BuildId: eb0c8b7f827292af83855e89b431276a)

### am...@chromium.org (2023-05-05)

Hello, thank you both for your responses. I feel like streams were a bit crossed here, https://crbug.com/chromium/1381455#c68 was solely directed at finnur@ in relation to merge consideration and assessment. I probably should have put more space or time between comments #67 and #68 however, I wanted be timely about why I wasn't approving merges here given deadlines and the work that finnur@ did to stage the cherry-picks. 

I apologize if my crossing these steams resulted in a messaging that you found hurtful. This was just direct output from our technical assessment of the issue at hand and related to a merge decision. Merges must be very deliberate and we must be careful not to introduce undue changes that may result in platform instability and crashes as to not break Chrome for all Android users. 

The reward in https://crbug.com/chromium/1381455#c67 was based on this bug as if it were a UAF, not on if it were a null pointer deref. We do not consider null pointer derefs as security bugs and they are not eligible for VRP [1][2]. Because we did not have concrete evidence this was a UAF and the initial fixes in December as well as the initial triage [3] referred to "rashes are segfaults on addresses 0x30 and 0x20", which indicates a null pointer deref. 
Since we - as a security team - did not have any concrete evidence that was not a security bug, we did decided to ultimately reward it as it seemed like the fair thing to do, especially given all your responsiveness from the original report to the resolution of these crashes. The reward amount decided was based on this being a highly and significantly mitigated security bug, requiring much non-trivial user interaction. [4] The reward amount was consistent with any other UAF or memory corruption that is this heavily mitigated. The reward decision was not at all related to the assessment that this was potentially not a UAF. 

While it is not your fault at in any way that the crashes for the crash IDs you provided were no longer available in the crash data, it is rather expected that VRP reports contain a symbolized stack trace uploaded directly to the report [5]. This helps with triage, so that the security shepherd doing triage does not have to track down the crash, and also provides a permanent record / evidence of the issue you were able to discover and reproduce. In the future, it would be most helpful to provide an ASAN stack trace in your reports. [6]

Thanks again for continued effort and responses on this one, they are very much appreciated and in the future I'll be more specific to separate messaging related to merges versus reward decisions. 

[1] e.g. https://bugs.chromium.org/p/chromium/issues/detail?id=1323687
[2] https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#why-aren_t-null-pointer-dereferences-considered-security-bugs
[3] https://bugs.chromium.org/p/chromium/issues/detail?id=1381455#c3
[4] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts-for-mitigated-security-bugs
[5]  https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#report-quality
[6] https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md#run-chrome-under-asan

### so...@gmail.com (2023-05-05)

[Comment Deleted]

### so...@gmail.com (2023-05-05)

Thank you very much for the detailed answer! 

We'll leave the reward, it's a good thing, but I don't care if it's a null deref, or if it's not ok for any reason, then let's reset it, if you look at it, I've send more simple bugs than null derefs, it's a relaxation for me since I'm no longer a developer and the  time that I spend pleasantly with this is valuable.

I know the message wasn't meant for me, but anyone can read it in 14 weeks. I wrote that I find it hurtful, because what came out of it was that I can't distinguish a use after free from a null deref and that would be a terrible shame for me. That is why I now reproduced a couple of crashes with high memory addresses to show that I can distinguish between real memory addresses and null. That's all, developer self-esteem.  :)

PS: There was a language error in the deleted comment, which made it mean utter nonsense, I fixed it by deleting and re-posting :)

### am...@google.com (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1381455?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061594)*
