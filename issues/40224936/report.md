# Security: Chrome on Android requestFullscreen then back or forward navigation on BFcache page able to hide omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [40224936](https://issues.chromium.org/issues/40224936) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Navigation>BFCache |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-05-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

After requestFullscreen then run window.history.back() to perform back navigation to page stored in BFcache, interestingly with proper timing it will hide Chrome omnibox while Android status bar still remain visible.

As legitimate omnibox is hidden, attacker able to replace it with spoof omnibox showing address bar on trusted origin (as on attached video).

When I set chrome://flags/#back-forward-cache from "Default" to "Disabled" the omnibox will not hidden (will get restored back) even after repeated tries.

This similar to <https://crbug.com/chromium/1270593> and <https://crbug.com/chromium/1300253> which hide omnibox after tap to the page.

**VERSION**

- Chrome 101.0.4951.41 on Mi 9T
- Chrome Beta 102.0.5005.40 on Mi 9T
- Chrome Dev 103.0.5038.0 on Mi 9T
- Chrome Dev 103.0.5038.0 on Android Emulator Pixel\_2\_API\_29

**REPRODUCTION CASE**

1. Extract hideomniboxspoof-bfcache.zip
2. Run "python -m http.server" to serve cacheable HTTP server
3. Visit the web server ipaddress:8000 (i.e. 127.0.0.1:8000)
4. Tap spoofpage.html
5. Tap "Spoof1" link or "Spoof2" link
6. Tap anywhere on the page
7. Omnibox will hide immediately then spoofed with spoof omnibox.

If the legitimate omnibox is not hidden (as on PoC video) try press back then tap spoofpage.html (repeat from step 4) or tap directly testcase1.html or testcase2.html, or go to chrome://flags/#back-forward-cache set "Default" to "Enabled".

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- deleted (application/octet-stream, 0 B)
- [Chrome on Android - requestFullScreen then back on BFCache page able to hide omnibox.mp4](attachments/Chrome on Android - requestFullScreen then back on BFCache page able to hide omnibox.mp4) (video/mp4, 1.2 MB)
- [spoofpage.html](attachments/spoofpage.html) (text/plain, 32.6 KB)
- [testcase1.html](attachments/testcase1.html) (text/plain, 772 B)
- [testcase2.html](attachments/testcase2.html) (text/plain, 769 B)
- [back-delayed.html](attachments/back-delayed.html) (text/plain, 482 B)
- [back-direct.html](attachments/back-direct.html) (text/plain, 234 B)
- [success.log](attachments/success.log) (text/plain, 5.0 KB)
- [failed.log](attachments/failed.log) (text/plain, 10.1 KB)
- [exitpersistentfullscreen.patch](attachments/exitpersistentfullscreen.patch) (text/plain, 1.1 KB)
- [omnibox-hidden1.txt](attachments/omnibox-hidden1.txt) (text/plain, 7.5 KB)
- [omnibox-hidden2.txt](attachments/omnibox-hidden2.txt) (text/plain, 7.5 KB)
- [omnibox-restored-with-animation1.txt](attachments/omnibox-restored-with-animation1.txt) (text/plain, 9.1 KB)
- [omnibox-restored-with-animation2.txt](attachments/omnibox-restored-with-animation2.txt) (text/plain, 9.1 KB)
- [omnibox-restored-without-animation1.txt](attachments/omnibox-restored-without-animation1.txt) (text/plain, 6.0 KB)
- [omnibox-restored-without-animation2.txt](attachments/omnibox-restored-without-animation2.txt) (text/plain, 6.0 KB)
- [app.js](attachments/app.js) (text/plain, 462 B)
- [args.gn](attachments/args.gn) (application/octet-stream, 451 B)
- [back-delayed.html](attachments/back-delayed_53166138.html) (text/plain, 442 B)
- [omnibox-hidden1.txt](attachments/omnibox-hidden1_53166149.txt) (text/plain, 5.9 KB)
- [back-delayed html to Hide Omnibox on Chrome Dev.mp4](attachments/back-delayed html to Hide Omnibox on Chrome Dev.mp4) (video/mp4, 837.0 KB)
- [omnibox-hidden2.txt](attachments/omnibox-hidden2_53166163.txt) (text/plain, 6.1 KB)

## Timeline

### [Deleted User] (2022-05-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-11)

Thank you for the report. This does look similar to others you reference, but also has a BFCache interaction. I have not yet reproduced this locally.

I'm adding some fullscreen owners but also BFCache folks to take a closer look. I will try to repro and bisect in the meantime.

[Monorail components: UI>Browser>FullScreen UI>Browser>Navigation>BFCache]

### [Deleted User] (2022-06-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-14)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-15)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2022-09-07)

Jinsuk, these P1 nags are for the bug owners comments/update on the bug. Mind dropping a comment w/ current status? Should this actually be a P1 or lower priority?

### [Deleted User] (2022-10-10)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2022-11-01)

Apology for late response. I haven't been able to reproduce this issue on the devices I have (Pixel, Pixel XL, Pixel 2XL, Pixel 4XL). Will try this out with an emulator too.

### ra...@chromium.org (2022-11-02)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-11-02)

Hi @jinsuk thanks for the update, I still able to reproduce this on Android Emulator Android 13; sdk_gphone64_x86_64 and on Mi 9T Android 11 using Chrome Dev 109.0.5382.0.

At first on Android Emulator Android 13 I'm not able reproduce the issue, but after set chrome://flags/#back-forward-cache "Back-forward cache" from "Default" to "Enabled" I able to reproduce the issue quickly.

### ji...@chromium.org (2022-11-03)

I can repro it about 1 out 3 times with Chrome stable on Pixel 4XL. Apparently the logic depends on subtle timing introduced by |calculatePrimes()| between successive fullscreen requests in testcase*.html to make the issue happen. Therefore it is very tricky to repro it with a local debug build. I was able to repro it just once after tweaking |iterations| and |multiplier|, but that also stopped working if I add one or more log for debugging.

Was there any specific duration between the requests (or history.back()) that make the issue happen deterministically (or at least more often)? 

### su...@gmail.com (2022-11-04)

@jinsukkim I'll try to improve the testcase reliability, look like using XHR delay is more reliable way rather than using calculatePrimes() which rely on CPU usage.

### su...@gmail.com (2022-11-18)

It looks like a race condition issue on restoring the toolbar, it requires optimized build compilation and fast hardware to reliably hide the omnibox, when running back-direct.html testcase on Chrome Dev (with Back-forward cache set to Enabled); Android Emulator Pixel_2_API_33 using Ryzen 7 5700G hardware (which is fast), without any delay code (calculatePrimes or XHR delay) it able to hide the omnibox.

I've tried reproducing this on Google Pixel 4 XL (Unlocked) using AWS Device Farm Remote access and my local device, when running back-delayed.html (which delay back with blocking XHR request) on Chrome Beta and Chrome Dev (with Back-forward cache set to Enabled) it can reliably hide the omnibox.

I've compiled Chromium Android with is_debug=true for x86_64 (for Android Emulator) and arm (for phone), unfortunately I unable to reproduce the hide omnibox on the debug build, the performance is slower on debug build, probably it due to race condition which require the optimized build.

Fortunately when compile Chromium with is_debug=false or is_official_build=true (which make Chromium faster) then running back-direct.html on x86_64 Android Emulator it able to hide the omnibox, but it requires couples of tries to hide the omnibox than on Play Store build.


### su...@gmail.com (2022-11-21)

Alright I can reproduce the issue on build "is_java_debug = true" with testcase back-direct.html, it require couple of tries to able reproduce the hide omnibox, sometimes one-time tries able to do so which is great.

I then insert a few of Log.d on enterFullscreen and exitFullscreen on FullscreenHtmlApiHandler, then when compare logcat on success attempt (hide omnibox) and failed attempt (restored omnibox) there is a noticeable difference after FullscreenHtmlApiHandler.java exitFullscreen -> OnLayoutChangeListener -> TabBrowserControlsConstraintsHelper.update is called, the getPersistentFullscreenMode is only called twice on success attempt, on failed attempt after TabBrowserControlsConstraintsHelper.update called the getPersistentFullscreenMode is called many times.

When run the Chromium with parameter --wait-for-java-debugger I still able to reproduce the hide omnibox while debugging Java code and adding breakpoint on Android Studio with testcase back-direct.html on Android Emulator.

When debugging the code,. the good things is after I remove mDelegate.exitFullscreenModeForTab(); on TabWebContentsDelegateAndroidImpl.java I unable reproduce the hide omnibox, the toolbar is now always get restored. The noticeable thing after remove the code the toolbar always restore with animation/transition (from top to down), before remove the code after tap to back-direct.html, the toolbar sometimes restored without animation/transition (the toolbar stays on top without movement), it's like instantly go back.

When analyzing the code I noticed the exit fullscreen method which call mPersistentModeSupplier.set(false) is called from C++ WebContentsDelegateAndroid::ExitFullscreenModeForTab method. After mDelegate.exitFullscreenModeForTab(); was removed, the fullscreen mode is still able to exit (e.g. after press back button, navigate to another link) as it also handled by another code, the navigation to another link exit fullscreen is now handled by onDidFinishNavigationInPrimaryMainFrame code instead of WebContentsDelegateAndroid::ExitFullscreenModeForTab, therefore the omnibox is now always restored. The things that doesn't work is when HTML5 code is calling document.exitFullscreen() it unable to exit the fullscreen mode.

To make the WebContentsDelegateAndroid::ExitFullscreenModeForTab only called by document.exitFullscreen() I modified onExitFullscreen(Tab tab) on FullscreenHtmlApiHandler.java from if (tab == mTab) exitPersistentFullscreenMode(); to if (tab == mTab && !tab.isLoading()) exitPersistentFullscreenMode(); now the document.exitFullscreen is now working again.

I haven't test this whether it solve the issue on more reliable build (Play store build), is there any way to compile Chromium as on Play Store edition? I've tried is_official_build=true but the reliability is still not same as on Play Store build. By the way it also works on Microsoft Edge and Vivaldi Browser (Play Store build).

@jinsukkim I think there are a better way to solve this issue, I hope it's help the analysis, thanks!

### su...@gmail.com (2022-11-26)

Here the patch I applied which solved the issue.

### ji...@chromium.org (2022-11-30)

Thanks susah.yak@ for the investigation. It helps a lot. Looking into it again now

### ji...@chromium.org (2022-12-08)

Unfortunately I'm still not able to repro the issue on local builds, with possible the combinations of gn args options (is_debug/is_official_build), either on x64 emulator or on Pixel 4XL. This makes it quite hard to assess the validity of all attempts.

I'm not confident on skipping |exitPersistenFullscreenMode()| if tab is loading. It is (should be) orthogonal to the fullscreen state change, and not quite sure about its impact on various situations.

susah.yak@ if you can still build Chrome, would you mind helping out by adding a little more debug log? I'd like to see the stack trace when |exitPersistenFullscreenMode()| is invoked. Could you call |printStack()| or along this line to print out the stack?

import java.io.StringWriter;
import java.io.PrintWriter;
import java.util.Arrays;
import android.text.TextUtils;


    public static void printStack(String msg) {                                                                                                                                                                                        
        android.util.Log.i("crdebug", msg);
        StringWriter sw = new StringWriter();
        new Throwable().printStackTrace(new PrintWriter(sw));
        String[] s = sw.toString().split("\n");
        String[] log = Arrays.copyOfRange(s, 1, Math.min(s.length, 10));
        android.util.Log.i("crdebug", TextUtils.join("\n", log));
    }

    private void enterPersistentFullscreenMode(FullscreenOptions options) {
+        printStack("enter-persistent trigger: " + ((!getPersistentFullscreenMode() || !ObjectsCompat.equals(mFullscreenOptions, options))));
        ...
    }

     public void exitPersistentFullscreenMode() {
+        printStack("exit-persistent persistent: " + getPersistentFullscreenMode());


May need a few rounds of debugging, but I think it will help me see what's going on when things go wrong. For this to work, gn args needs to have:

is_debug=false
is_java_debug=true

I'm also curious if the issue still repro's with these options.

OTOH, I noticed something unexpected. |{enter|exit}PersistentFullscreenMode| is called more often than necessary, sometimes as many as 3 times per a fullscreen session. Ideally, I think the first call updates the internal state so that the subsequent calls will be no-op, but that is not exactly what's happening - the next calls also go through the flow. What stands out is that fullscreen observers get notification each time. Ideally they also should work in an idempotent manner but the right way would be for FullscreenManager to notify the observers only once per fullscreen session to prevent the spurious notifications in the first place. I need to rectify it before debugging the reported issue.

### ji...@chromium.org (2022-12-08)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-12-09)

> Unfortunately I'm still not able to repro the issue on local builds, with possible the combinations of gn args options (is_debug/is_official_build), either on x64 emulator or on Pixel 4XL. This makes it quite hard to assess the validity of all attempts.

I able to reproduce this quickly on Chrome Dev 110.0.5462.3 (back-forward-cache set to "Enabled") on python -m http.server. It took several retries  on local builds to hide the omnibox. 

> susah.yak@ if you can still build Chrome, would you mind helping out by adding a little more debug log? I'd like to see the stack trace when |exitPersistenFullscreenMode()| is invoked. Could you call |printStack()| or along this line to print out the stack?

Thanks I able to invoke printStack on three condition: omnibox-hidden, omnibox-restored-with-animation, omnibox-restored-without-animation (go back instantly without moving toolbar/omnibox)

### su...@gmail.com (2022-12-11)

> Unfortunately I'm still not able to repro the issue on local builds, with possible the combinations of gn args options (is_debug/is_official_build), either on x64 emulator or on Pixel 4XL. This makes it quite hard to assess the validity of all attempts.

Alright I've able to reproduce this on GCP Compute Engine VM Instances, launched machine "c2-standard-16" with OS "Ubuntu 22.10", SSD disk 120GB, then enable nested virtualization on the VM "enableNestedVirtualization: true" on this guide https://cloud.google.com/compute/docs/instances/nested-virtualization/enabling. After VM instances is created, I followed https://cloud.google.com/architecture/chrome-desktop-remote-on-compute-engine to remote desktop the instance.

Checking out Chromium for Android source by following https://chromium.googlesource.com/chromium/src/+/HEAD/docs/android_build_instructions.md. On "Get the code" I replaced "fetch --nohooks android" with "fetch --nohooks --no-history android" for faster download

"On Setting up the build" part I compiled Chromium for Android with command "gn args out/X64", then replaced entire file with attached args.gn, then run command "autoninja -C out/X64 chrome_public_apk". After build is completed I launched Chromium for Android with following command: "out/X64/bin/chrome_public_apk install && out/X64/bin/chrome_public_apk launch"

After that I download the app.js (XHR delay server) then run "npm install express cors && node app.js". Then download attached new back-delayed.html (delay changed to 5), and edit the file replace 127.0.0.1 to node app.js listening address (e.g. GCP Internal IP 10.138.0.6). Finally run "python -m http.server" inside back-delayed.html directory.

On Chromium for Android visit the "python -m http.server" address:port, then on Directory listing tap "back-delayed.html", then tap anywhere on the page. If omnibox is still restored, try again until it hidden. If you get black screen instead of window.history.back(), the XHR.open address might be incorrect.

On Android Emulator Pixel_3A_API_33_x86_64 (Google APIs) it able to hide omnibox after ~5 tries, sometimes 1 tries also do the hide. 

I noticed that Android Emulator on GCP VM Instances is appear laggy, I tried lower the Emulator resolution by "Create device" with lower resolution device "2.7 QVGA API 33" (Google APIs), then the great thing is that the omnibox is hidden more often (more reliable to reproduce) on this device.

@jinsukkim try to recompile Chromium with attached args.gn, run node app.js (XHR delay code), reproduce with attached back-delayed.html (under python -m http.server), and finally Android emulator with lower resolution device.

If you still unable to reproduce, I think it's great to try connect to my GCP instance server using RDP, so you can easily reproduce the issue on local builds. Or I can share the GCP disk custom image to your email, so you can launch the instance with same disk.

### ji...@chromium.org (2022-12-13)

Thanks for the detailed follow-up. To address the concern I had in https://crbug.com/chromium/1324188#c24, landed a fix to prevent multiple enter/exit calls into Fullscreen manager crrev.com/c/4090924 Would you mind testing again with the latest canary (110.0.5475.0) or dev when it becomes available? I'd like to start from there as it makes the flow simpler, also the investigation.

### su...@gmail.com (2022-12-13)

> Would you mind testing again with the latest canary (110.0.5475.0) or dev when it becomes available? I'd like to start from there as it makes the flow simpler, also the investigation.

I've update my existing chromium checkout to latest using "git rebase-update && gclient sync", then build the Chromium, now on "About Chrome" the application version is on Chromium 110.0.5476.0.

Then when I tried testcase back-delayed.html, I still able to reproduce the hide omnibox. I've attached the stack trace log.

### ji...@chromium.org (2022-12-14)

Unfortunately it is still very hard to repro on my end. Rebuilt Chromium with the provided args.gn, used app.js at port 3000 and ran Python server at 8000 to fetch back-delayed.html on emulator (x86_64_api33, Pixel 3A/4XL/2.7qvga), all to no avail. They all go back to the previous page, omnibox restored. I saw just once the page, when tested on a physical Pixel 4XL, enter fullscreen and stay there. But it could display the toast with no problem.

clip: https://drive.google.com/file/d/15O1WAesc1igD3PRGAlfLqh0zbT6OUqZj/view?usp=share_link

Omnibox won't be restored if the layout change listener in |exitFullscreen()| fails to trigger for whatever reason.  Could you do me another favor of running with another debug logs and capture the output when things go wrong?

The logs are in exitPersistentFullscreenMode and exitFullscreenMode respectively. I appreciate your patience and willingness to help.

--- a/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
+++ b/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
@@ -476,7 +476,9 @@ public class FullscreenHtmlApiHandler implements ActivityStateListener, WindowFo
         if (getPersistentFullscreenMode()) {
             cancelNotificationToast();
             mPersistentModeSupplier.set(false);
-
+            android.util.Log.i("crdebug",
+                    "exit-fs wc: " + (mWebContentsInFullscreen != null)
+                            + " tab: " + (mTabInFullscreen != null));
             if (mWebContentsInFullscreen != null && mTabInFullscreen != null) {
                 exitFullscreen(
                         mWebContentsInFullscreen, mContentViewInFullscreen, mTabInFullscreen);
@@ -524,6 +526,9 @@ public class FullscreenHtmlApiHandler implements ActivityStateListener, WindowFo
             @Override
             public void onLayoutChange(View v, int left, int top, int right, int bottom,
                     int oldLeft, int oldTop, int oldRight, int oldBottom) {
+                android.util.Log.i("crdebug", "exit-layout-change: "
+                    + " old:(" + oldLeft + "," + oldTop + "," + oldRight + "," + oldBottom + ")"
+                    + " new:(" + left + "," + top + "," + right + "," + bottom + ")");



### su...@gmail.com (2022-12-14)

> Unfortunately it is still very hard to repro on my end. Rebuilt Chromium with the provided args.gn, used app.js at port 3000 and ran Python server at 8000 to fetch back-delayed.html on emulator (x86_64_api33, Pixel 3A/4XL/2.7qvga), all to no avail. They all go back to the previous page, omnibox restored. I saw just once the page, when tested on a physical Pixel 4XL, enter fullscreen and stay there. But it could display the toast with no problem. clip: https://drive.google.com/file/d/15O1WAesc1igD3PRGAlfLqh0zbT6OUqZj/view?usp=share_link

Alright Jinsuk I see the clip, I forgot to mention you have to visit 127.0.0.1:8000 -> then tap back-delayed.html -> then tap anywhere on the page (as on attached video below).

### su...@gmail.com (2022-12-15)

Alright I've applied the crdebug exit-fs wc: and exit-layout-change code. Here the new attached log:

### [Deleted User] (2023-02-13)

This issue has not been updated for 60 or more days - lowering its priority to P2.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2023-08-05)

Hi @jinsukkim, I no longer able to reproduce the hide omnibox on latest Chromium. 

After git checkout some Chromium commit, and compile it, I confirm this has been fixed by commit [CT] Fix toolbar isn't hidden when returning to verified origin crrev.com/c/4252197.

The code add controls_initialized_ = false; to RenderWidgetHostViewAndroid::HideInternal(), so when the testcase trigger back, the omnibox is now no longer hidden.

### su...@gmail.com (2023-08-30)

jinsukkim@ as the issue has been resolved by crrev.com/c/4252197 on https://crbug.com/chromium/1405166, can we marked this as Fixed? Thanks!

### ji...@chromium.org (2023-08-30)

Glad to hear that this was also resolved. Marking as fixed.

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations Irvan! The Chrome VRP Panel has decided to award you $1,000 for the report, as this issue was very difficult to be reproduced and has a low possibility of exploitation in a way that would introduce real user harm. Thank you for all your efforts in reporting this issue to us along the way. 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-06)

This issue was migrated from crbug.com/chromium/1324188?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Navigation>BFCache]
[Monorail blocked-on: crbug.com/chromium/1399646]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40224936)*
