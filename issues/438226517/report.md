# Address Bar Spoofing on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [438226517](https://issues.chromium.org/issues/438226517) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-08-13 |
| **Bounty** | $3,000.00 |

## Description

redacted

## Attachments

- samsunga31.mp4 (video/mp4, 2.6 MB)
- samsunga56.mp4 (video/mp4, 7.7 MB)
- [truncateddomainvirtualkeyboard.jpg](attachments/truncateddomainvirtualkeyboard.jpg) (image/jpeg, 87.6 KB)
- [spoofnewbottombar.html](attachments/spoofnewbottombar.html) (text/html, 1.4 KB)
- spoofgooglea56.mp4 (video/mp4, 7.2 MB)
- [a56spoof.jpeg](attachments/a56spoof.jpeg) (image/jpeg, 30.0 KB)
- [spoofgooglea31.mp4](attachments/spoofgooglea31.mp4) (video/mp4, 4.7 MB)
- [a31spoof.jpeg](attachments/a31spoof.jpeg) (image/jpeg, 45.0 KB)
- VID-20250816-WA0000.mp4 (video/mp4, 4.7 MB)
- deleted (application/octet-stream, 0 B)
- VID-20250821-WA0001.mp4 (video/mp4, 12.8 MB)
- [logcat.txt](attachments/logcat.txt) (text/plain, 224.5 KB)
- samsunga56poc.mp4 (video/mp4, 3.1 MB)
- samsungaa31poc.mp4 (video/mp4, 2.2 MB)
- oppo.mp4 (video/mp4, 6.9 MB)

## Timeline

### sa...@gmail.com (2025-08-14)

redacted

### an...@chromium.org (2025-08-14)

[security shepherd]: I'm not able to reproduce this exactly as I see in your POC, but it's still somewhat a spoof. Also, I have the URL bar at the top and not the bottom so it's not as convincing. However, it could be convincing if all steps are aligned. I will be triaging this to @ct...@chromium.org for thoughts.

### sa...@gmail.com (2025-08-14)

I forgot step 1, you have to change the position of the address bar to the bottom:
 go to settings -> address bar-> bottom

### ch...@google.com (2025-08-15)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ct...@chromium.org (2025-08-15)

The incorrectly elided/displayed origin in the original report seems like a bug and we should definitely fix it.

The mini origin bar seems to be displaying as intended in the video and screenshot in [comment #2](https://issues.chromium.org/issues/438226517#comment2). It maybe is a bit hard to tell that it's there, but it's also new (we have had the mini origin bar on iOS for a long time, but not until recently on Android). This UI seems like it is strictly better than the prior status quo where it was trivial to do an inception bar attack [1](https://jameshfisher.com/2019/04/27/the-inception-bar-a-new-phishing-method/) on users.

### pn...@google.com (2025-08-15)

> The mini origin bar seems to be displaying as intended in the video and screenshot in [comment #2](https://issues.chromium.org/issues/438226517#comment2). It maybe is a bit hard to tell that it's there, but it's also new (we have had the mini origin bar on iOS for a long time, but not until recently on Android). This UI seems like it is strictly better than the prior status quo where it was trivial to do an inception bar attack

I think there is a likely UI glitch in this scenario in that the toolbar should probably be visible after the navigation to the spoof site but before focusing the form field, but as you point out we're displaying the origin bar when the form field is focused. That's not really a novel *vulnerability*, unless there's some scenario where the mini origin bar fails to display even with the form field focused.

The incorrect elision is indeed a bug and I am looking into it presently.

### pn...@google.com (2025-08-15)

> I think there is a likely UI glitch in this scenario...

This may be moot; I can't repro this unless I back out a fix for a similar mini origin bar issue that landed right after this one was tested. Reporter, are you able to repro the first issue on Canary versions >= 141.0.7354.0 ?

### sa...@gmail.com (2025-08-15)

Hi i can reproduced it in version 141.0.7356.0 as comment 2 https://issues.chromium.org/issues/438226517#comment2 

### pn...@google.com (2025-08-15)

Got it. I'll continue to try to repro that after I address the elision issue; I haven't had any luck so far, although I'm using different devices.

### sa...@gmail.com (2025-08-15)

redacted

### sa...@gmail.com (2025-08-15)

deleted

### sa...@gmail.com (2025-08-15)

redacted

### pn...@google.com (2025-08-18)

I was able to reproduce a version of this problen with a samsung device, I think because these devices are subject to a scenario (bug probably) where an onPrepare signal for the insets animation is delivered but no subsequent start, progress, or end signals. We're not robust to this right now.

Regarding the improper elision, I think that's actually the result of the other UI glitch. The animation of the mini origin text is set up so that the final x coordinate puts the text in a centered position with the end of the origin text showing. To animate this process, the text is translated to the right until the animation is over. For long origins, this can mean that a right-side segment of the text is cut off. If the animation never ends, the text remains cut off for long origins indefinitely.

I think it's best to just make ourselves robust to unreliable insets animation signals by bailing out after some period of time (animation duration + xxx ms), fast-forwarding to whatever the correct end state is.

### sa...@gmail.com (2025-08-18)

The bug is not affected on samsung only i also can reproduce on oppo A17

### dx...@google.com (2025-08-18)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6859564>

[mobar] Cancel mobar animation after fixed duration

---


Expand for full commit details
```
     
    The OS does not reliably deliver animation signals in all cases, which 
    means we can get stuck in an intermediate state. 
     
    Bug: 438226517 
    Change-Id: I8fb904b6571e9f20b2b29b760603ff12eab9e333 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6859564 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1503048}

```

---

Files:

- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarControllerTest.java`

---

Hash: [64768fe68df9624fa07c2edec664646522d2b403](https://chromiumdash.appspot.com/commit/64768fe68df9624fa07c2edec664646522d2b403)  

Date: Mon Aug 18 23:54:39 2025


---

### sa...@gmail.com (2025-08-20)

redacted

### pn...@google.com (2025-08-20)

What about on versions 141.0.7366.0+ ? (video appears to show 141.0.7363)

### sa...@gmail.com (2025-08-21)

i got crash on version 141.0.7368.0:

2025-08-21 07:50:29.701 27889-27889 AndroidRuntime          com.chrome.canary                    E  FATAL EXCEPTION: main
                                                                                                    Process: com.chrome.canary, PID: 27889
                                                                                                    java.lang.ClassCastException: android.widget.FrameLayout$LayoutParams cannot be cast to nc5
                                                                                                    	at androidx.coordinatorlayout.widget.CoordinatorLayout.u(chromium-TrichromeChromeGoogle6432.aab-canary-736800033:42)
                                                                                                    	at oc5.onPreDraw(chromium-TrichromeChromeGoogle6432.aab-canary-736800033:4)
                                                                                                    	at android.view.ViewTreeObserver.dispatchOnPreDraw(ViewTreeObserver.java:1093)
                                                                                                    	at android.view.ViewRootImpl.performTraversals(ViewRootImpl.java:3698)
                                                                                                    	at android.view.ViewRootImpl.doTraversal(ViewRootImpl.java:2421)
                                                                                                    	at android.view.ViewRootImpl$TraversalRunnable.run(ViewRootImpl.java:9502)
                                                                                                    	at android.view.Choreographer$CallbackRecord.run(Choreographer.java:1242)
                                                                                                    	at android.view.Choreographer.doCallbacks(Choreographer.java:996)
                                                                                                    	at android.view.ChoreographerExtImpl.checkScrollOptSceneEnable(ChoreographerExtImpl.java:389)
                                                                                                    	at android.view.Choreographer.doFrame(Choreographer.java:865)
                                                                                                    	at android.view.Choreographer$FrameDisplayEventReceiver.run(Choreographer.java:1227)
                                                                                                    	at android.os.Handler.handleCallback(Handler.java:938)
                                                                                                    	at android.os.Handler.dispatchMessage(Handler.java:99)
                                                                                                    	at android.os.Looper.loopOnce(Looper.java:233)
                                                                                                    	at android.os.Looper.loop(Looper.java:344)
                                                                                                    	at android.app.ActivityThread.main(ActivityThread.java:8249)
                                                                                                    	at java.lang.reflect.Method.invoke(Native Method)
                                                                                                    	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:589)
                                                                                                    	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1071)
2025-08-21 07:50:29.709  1703-1819  WindowManager           system_server                        W  performShowLocked abort for not ready:Window{ce4a410 u0 com.chrome.canary/com.google.android.apps.chrome.Main}
2025-08-21 07:50:29.725  1703-1819  WindowStateExtImpl      system_server                        I  onSurfaceShowChange show = true mPackageName = com.chrome.canary parentPkgName = com.chrome.canary
2025-08-21 07:50:29.733  1703-1818  OplusKeepAliveManager   system_server                        D  TOP_APP is ProcessRecord{a13bbd9 27889:com.chrome.canary/u0a437} uid is 10437
2025-08-21 07:50:29.733  1703-1838  OplusThermalStats       system_server                        E  Error getting package info: com.chrome.canary
2025-08-21 07:50:29.781  1703-6302  OplusAppLi...eptManager system_server                        D  shouldFilterTask::packageName = com.chrome.canary
2025-08-21 07:50:30.097  1703-6302  OplusZoomW...gerService system_server                        V  onAnimationFinished:  r = ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039}
2025-08-21 07:50:30.098  1703-6302  OplusAppSw...gerService system_server                        I   handleAppVisible , r = ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039}
2025-08-21 07:50:30.178  3015-3142  AuthDialogHelper        com.oplus.persist.system             W  checkNotificationSwitchFirst() called with: context = [com.oplus.notification.NotificationCenterService@ffa775f], pkg = [com.chrome.canary], uid = [10437], userId = [0], init checker
2025-08-21 07:50:30.179  3015-3142  AuthDialogHelper        com.oplus.persist.system             E  CheckNotificationCanBeSetSecond: check com.chrome.canary , Notification master switch on, unable to pop dialog
2025-08-21 07:50:31.060 28250-28250 chromium                linker64                             W  [0821/075031.060249:WARNING:third_party/crashpad/crashpad/snapshot/linux/exception_snapshot_linux.cc:263] fpsimd not found
2025-08-21 07:50:31.182  1703-3107  OplusAppStartupMonitor  system_server                        D  notifyUnstableAppInfo: Bundle[{unstableTime=1755737431181, reason=crash, userId=0, safecenter=unstable, exceptionMsg=android.widget.FrameLayout$LayoutParams cannot be cast to nc5, exceptionClass=java.lang.ClassCastException, packageName=com.chrome.canary, unstable_restrict_switch=true}]
2025-08-21 07:50:31.184  2568-27570 abnormalUtils           com.oplus.exsystemservice            D  com.chrome.canary is foreground =true
2025-08-21 07:50:31.189  1703-6302  ActivityTaskManager     system_server                        W    Force finishing activity com.chrome.canary/com.google.android.apps.chrome.Main
2025-08-21 07:50:31.194  1703-6302  OplusZoomW...gerService system_server                        V  prepareZoomTransition: curStack=Task{834660d #2039 type=standard A=10437:com.chrome.canary U=0 visible=false mode=fullscreen translucent=true sz=1}   nextStackTask{5f74147 #1 type=undefined ?? U=0 visible=true mode=fullscreen translucent=true sz=1}
2025-08-21 07:50:31.207 27889-27889 Process                 com.chrome.canary                    I  Sending signal. PID: 27889 SIG: 9
2025-08-21 07:50:31.284  1703-2378  ConnectivityService     system_server                        D  releasing NetworkRequest [ REQUEST id=702, [ Capabilities: INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VCN_MANAGED Uid: 10437 RequestorUid: 10437 RequestorPkg: com.chrome.canary UnderlyingNetworks: Null] ] (release request)
2025-08-21 07:50:31.285  1703-6250  WindowManager           system_server                        I  WIN DEATH: Window{ce4a410 u0 com.chrome.canary/com.google.android.apps.chrome.Main}
2025-08-21 07:50:31.286  1703-6250  InputManager-JNI        system_server                        W  Input channel object 'ce4a410 com.chrome.canary/com.google.android.apps.chrome.Main (client)' was disposed without first being removed with the input manager!
2025-08-21 07:50:31.288  1703-2378  ConnectivityService     system_server                        D  releasing NetworkRequest [ REQUEST id=696, [ Capabilities: INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VCN_MANAGED Uid: 10437 RequestorUid: 10437 RequestorPkg: com.chrome.canary UnderlyingNetworks: Null] ] (release request)
2025-08-21 07:50:31.290  1703-6250  WindowManager           system_server                        D  setParent old=ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039 f}},new=null,this window=Window{ce4a410 u0 com.chrome.canary/com.google.android.apps.chrome.Main},callers=com.android.server.wm.WindowContainer.removeChild:648 com.android.server.wm.ActivityRecord.removeChild:4199 com.android.server.wm.ActivityRecord.removeChild:394 com.android.server.wm.WindowContainer.removeImmediately:704 com.android.server.wm.WindowState.removeImmediately:2552 com.android.server.wm.WindowState.removeIfPossible:2748 
2025-08-21 07:50:31.291  1703-6250  OplusStart...dowManager system_server                        D  interceptRemoveStartingWindow activity =ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039 f}}, hasSurfaceView:false, isSnapshot=true, mIsDrawCompleted=false, mStartingRemoveRunnable=null
2025-08-21 07:50:31.300  1106-1106  Layer                   surfaceflinger                       D  reparent to null sequence=485, seq[5], name=ce4a410 com.chrome.canary/com.google.android.apps.chrome.Main#0
2025-08-21 07:50:31.301  1106-1106  OplusLayer              surfaceflinger                       D  ~Layer() sequence=485, name=ce4a410 com.chrome.canary/com.google.android.apps.chrome.Main#0 0xb400007e5c0d6000
2025-08-21 07:50:31.306  1703-4923  TheiaManager            system_server                        D  KEY:appNameVALUE:Chrome Canary
2025-08-21 07:50:31.306  1703-4923  TheiaManager            system_server                        D  KEY:packageNameVALUE:com.chrome.canary
2025-08-21 07:50:31.306  1703-4923  TheiaCrashMonitor       system_server                        D  com.chrome.canarycrash
2025-08-21 07:50:31.307  1703-4923  ActivityManager         system_server                        I  Process com.chrome.canary (pid 27889) has died: prcp TOP 
2025-08-21 07:50:31.312  4530-4530  BoundBrokerSvc          com.google.android.gms               D  onUnbind: Intent { act=com.google.android.gms.chromesync.service.firstparty.START dat=chimera-action: cmp=com.google.android.gms/.chimera.GmsApiService }
2025-08-21 07:50:31.312  1703-4923  ProcessStats            system_server                        E  Executing service ServiceState{8af1f8b org.chromium.content.app.SandboxedProcessService0 pkg=com.chrome.canary proc=eaef868} without owner
2025-08-21 07:50:31.316  1703-4923  ProcessStats            system_server                        E  Binding service ServiceState{8af1f8b org.chromium.content.app.SandboxedProcessService0 pkg=com.chrome.canary proc=eaef868} without owner
2025-08-21 07:50:31.317  1703-4923  ProcessStats            system_server                        E  Starting service ServiceState{8af1f8b org.chromium.content.app.SandboxedProcessService0 pkg=com.chrome.canary proc=eaef868} without owner
2025-08-21 07:50:31.318  1703-4923  ProcessStats            system_server                        E  Binding service ServiceState{8af1f8b org.chromium.content.app.SandboxedProcessService0 pkg=com.chrome.canary proc=eaef868} without owner
2025-08-21 07:50:31.325  1703-4923  ActivityManager         system_server                        I  Killing 27974:com.chrome.canary:sandboxed_process0:org.chromium.content.app.SandboxedProcessService0:0/u0a437i-9000 (adj 0): isolated not needed
2025-08-21 07:50:31.337 27958-27958 Zygote                  com.chrome.canary_zygote             I  Process 27974 exited cleanly (0)
2025-08-21 07:50:31.344  1703-4923  OplusZoomW...gerService system_server                        V  onAnimationFinished:  r = ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039 f}}
2025-08-21 07:50:31.345  1703-4923  WindowStateExtImpl      system_server                        I  onSurfaceShowChange show = false mPackageName = com.chrome.canary parentPkgName = com.chrome.canary
2025-08-21 07:50:31.353  1703-4923  WindowManager           system_server                        D  setParent old=ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039 f}},new=null,this window=Window{956ea8f u0 SnapshotStartingWindow for taskId=2039},callers=com.android.server.wm.WindowContainer.removeChild:648 com.android.server.wm.ActivityRecord.removeChild:4199 com.android.server.wm.ActivityRecord.removeChild:394 com.android.server.wm.WindowContainer.removeImmediately:704 com.android.server.wm.WindowState.removeImmediately:2552 com.android.server.wm.WindowState.destroySurface:3749 
2025-08-21 07:50:31.362  1703-4923  WindowManager           system_server                        D  setParent old=Task{834660d #2039 type=standard A=10437:com.chrome.canary U=0 visible=false mode=fullscreen translucent=true sz=0},new=null,this window=ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t2039 f}},callers=com.android.server.wm.WindowContainer.removeChild:648 com.android.server.wm.Task.removeChild:1875 com.android.server.wm.Task.removeChild:1854 com.android.server.wm.WindowContainer.removeImmediately:704 com.android.server.wm.WindowToken.removeImmediately:376 com.android.server.wm.ActivityRecord.removeImmediately:3998 
2025-08-21 07:50:31.366  1703-4923  OplusScreenSecurityMask system_server                        I  onStackRemoved task = Task{834660d #2039 type=standard A=10437:com.chrome.canary U=0 visible=false mode=fullscreen translucent=true sz=0} record = null displayId = 0
2025-08-21 07:50:31.367  1703-4923  WindowManager           system_server                        D  setParent old=DefaultTaskDisplayArea@22252352,new=null,this window=Task{834660d #2039 type=standard A=10437:com.chrome.canary U=0 visible=true mode=fullscreen translucent=true sz=0},callers=com.android.server.wm.WindowContainer.removeChild:648 com.android.server.wm.TaskDisplayArea.removeChildTask:427 com.android.server.wm.TaskDisplayArea.removeChild:414 com.android.server.wm.WindowContainer.removeImmediately:704 com.android.server.wm.Task.removeImmediately:3444 com.android.server.wm.Task.removeIfPossible:1054 
2025-08-21 07:50:31.368  1703-4923  TaskExtImpl             system_server                        D  remove ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main t-1 f}} to mActivityRecordSum = Counter{ }
2025-08-21 07:50:31.370  1703-4923  OplusHansManager        system_server                        I  front pkg: com.android.launcher, uid: 10167, prev pkg: com.chrome.canary, prev uid: 10437
2025-08-21 07:50:31.371  1703-3112  OplusHansManager        system_server                        I  uid=10437, pkg=com.chrome.canary enter SM
2025-08-21 07:50:31.371  1703-3112  OplusHansManager        system_server                        I  uid=10437, pkg=com.chrome.canary R enter(), D stay=1
2025-08-21 07:50:31.384  1106-1106  Layer                   surfaceflinger                       D  reparent to null sequence=477, seq[8], name=ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main#0
2025-08-21 07:50:31.385  1106-1106  OplusLayer              surfaceflinger                       D  ~Layer() sequence=477, name=ActivityRecord{da685fa u0 com.chrome.canary/com.google.android.apps.chrome.Main#0 0xb400007e289c8000
2025-08-21 07:50:31.422  1703-6250  ActivityManager         system_server                        I  Process com.chrome.canary:privileged_process0 (pid 28024) has died: fg  SVC 
2025-08-21 07:50:31.441  1703-3167  OplusHansManager        system_server                        I  onUidGone(), 10437 com.chrome.canary exit SM
2025-08-21 07:50:31.442  1703-3112  OplusHansManager        system_server                        I  uid=10437, pkg=com.chrome.canary R exit SM
2025-08-21 07:50:31.442  1703-3112  OplusHansManager        system_server                        I  uid=10437, pkg=com.chrome.canary R exit(), R stay=0
2025-08-21 07:50:31.470  1703-2807  OplusAppLi...eptManager system_server                        D  shouldFilterTask::packageName = com.chrome.canary
2025-08-21 07:50:31.475  1703-2807  OplusAppLi...eptManager system_server                        D  shouldFilterTask::packageName = com.chrome.canary

### pn...@google.com (2025-08-22)

That crash might be fixed as of the latest canary (141.0.7369.0+), can you test again?

And if not, please pull the crash id from chrome://crashes and post it here so I can look it up and fix it :)

### sa...@gmail.com (2025-08-22)

i tested on 141.0.7371 and still got crash. the uploaded crash ID: 07fe3418519e871d

### dx...@google.com (2025-08-28)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6896264>

[mobar] Force re-measure of coordinator layout on leaving mobar

---


Expand for full commit details
```
     
    This avoids a bug in CoordinatorLayout where a stale list of children 
    can cause a ClassCastException after reparenting. 
     
    Bug: 438226517 
    Change-Id: I2924109bfeb7fd8c855317a27dff730446b78a0b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6896264 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1508003}

```

---

Files:

- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/top/ToolbarControlContainer.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/top/ToolbarControlContainerTest.java`

---

Hash: [cb2f937012403bbfa165cc067d2923223afcf86e](https://chromiumdash.appspot.com/commit/cb2f937012403bbfa165cc067d2923223afcf86e)  

Date: Thu Aug 28 21:12:21 2025


---

### sa...@gmail.com (2025-08-29)

redacted

### pn...@google.com (2025-09-04)

Should we call this fixed then?

### sa...@gmail.com (2025-09-04)

Yes i cannot reproduce the poc. The address bar is appears when back to chromium

### ch...@google.com (2025-09-04)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
security UI spoofing but mitigated as needs some complex gesture from user. thank you for the bug report on this new feature.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sa...@gmail.com (2025-09-19)

hello chrome vrp team is this bug worth getting a CVE? if this bug gets a cover can the credit be given to:
hafiizh (https://www.linkedin.com/in/hafiizh-7aa6bb31) & kang ali (https://www.linkedin.com/in/mohammad-ali-syarief)?

thank you

### ch...@google.com (2025-12-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> security UI spoofing but mitigated as needs some complex gesture from user. thank you for the bug report on this new feature.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/438226517)*
