# Security: Google Chrome for Android: Current-tab cross-application scripting (UXSS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061545](https://issues.chromium.org/issues/40061545) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-07-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Vulnerability exists in Google Chrome for Android version 18.0.1025123 and below, class "com.google.android.apps.chrome.SimpleChromeActivity" allows malicious application inject JavaScript code into the context of any domain. Part of AndroidManifest.xml file provided below  

<activity android:name="com.google.android.apps.chrome.SimpleChromeActivity" android:launchMode="singleTask" android:configChanges="keyboard|keyboardHidden|orientation|screenSize">  

<intent-filter>  

<action android:name="android.intent.action.VIEW" />  

<category android:name="android.intent.category.DEFAULT" />  

</intent-filter>  

</activity>  

Class "com.google.android.apps.chrome.SimpleChromeActivity" has defined <intent-filter> directive and "android:exported" doesn't set to "false". Malicious application can call this class with data has been set to '<http://example.com>'. The second call contains JavaScript code, such as 'javascript:alert(document.cookie)', this code will be executed in the context of <http://example.com> domain. "com.google.android.apps.chrome.SimpleChromeActivity" class can be started through Android API functions or am (ActivityManager) application. PoC using Android API provided in the attachement, PoC using the ActivityManager provided below

shell@android:/ $ am start -n com.android.chrome/com.google.android.apps.chrome.SimpleChromeActivity -d '<http://example.com>'  

Starting: Intent { dat=<http://example.com> cmp=com.android.chrome/com.google.android.apps.chrome.SimpleChromeActivity }

shell@android:/ $ am start -n com.android.chrome/com.google.android.apps.chrome.SimpleChromeActivity -d 'javascript:alert(document.cookie)'  

Starting: Intent { dat=javascript:alert(document.cookie) cmp=com.android.chrome/com.google.android.apps.chrome.SimpleChromeActivity }  

Warning: Activity not started, its current task has been brought to the front

FIX: change exported status of "com.google.android.apps.chrome.SimpleChromeActivity" class to "false" or start new tab on each calling of the class

**VERSION**  

Chrome Version: 18.0.1025123 + stable  

Operating System: Android 4.1 and below

**REPRODUCTION CASE**  

The source code of malicious application provided in the attachement.

## Attachments

- [chromexss.java](attachments/chromexss.java) (text/x-java; charset=us-ascii, 869 B)

## Timeline

### js...@chromium.org (2012-07-19)

@palmer - You're probably the best person to route this in the right direction (because I have literally no idea what the implementation or expectations of these mechanisms on Android are).

### pa...@chromium.org (2012-07-19)

Nice find, Chaykin! I was able to reproduce it and I verified that the main Chrome activity's cookies (for example) are available from SimpleChromeActivity. So, that's bad. :) We call these "universal XSS" instead of "global", so I changed the title of this bug.

This bug is rewardable under our Chrome vulnerability rewards program, so please keep it confidential. Here is our standard boilerplate text for new bug finders:

----
Boilerplate text:

Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward.

Also, please be considerate about disclosure when the bug affects a core library that may be used by other products.

Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward.

Please be honest if you have already disclosed anything publicly or to third parties.
----

Grace, Chaykin's fix will obviously address the immediate problem and is easy to apply, so that's good news. For defense in depth, I like to require a signatureOrSystem Permission to launch the Activity, in addition to the exported="false". I am paranoid. :)

Alternately, perhaps we can get rid of SimpleChromeActivity, at least in production builds? A comment in the AndroidManifest.xml makes it sound as if SimpleChromeActivity is only for development and testing:

190         <!-- This is here to allow access for command line launching of the simple
191             chrome activity. It can be launched via 'adb shell am start -d
192             "data:text/html;utf-8,<html> clank </html>" -n
193             com.google.android.apps.chrome/.SimpleChromeActivity'. This is useful in case
194             there is a problem with the main UI, ContentView development can use this. -->


Additionally, I ran into this problem when leaving SimpleChromeActivity and trying to start up the main Chrome activity:

E/AndroidRuntime( 9418): FATAL EXCEPTION: main
E/AndroidRuntime( 9418): java.lang.RuntimeException: Unable to destroy activity {com.android.chrome/com.google.android.apps.chrome.SimpleChromeActivity}: java.lang.NullPointerException
E/AndroidRuntime( 9418): 	at android.app.ActivityThread.performDestroyActivity(ActivityThread.java:3273)
E/AndroidRuntime( 9418): 	at android.app.ActivityThread.handleDestroyActivity(ActivityThread.java:3291)
E/AndroidRuntime( 9418): 	at android.app.ActivityThread.access$1200(ActivityThread.java:130)
E/AndroidRuntime( 9418): 	at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1248)
E/AndroidRuntime( 9418): 	at android.os.Handler.dispatchMessage(Handler.java:99)
E/AndroidRuntime( 9418): 	at android.os.Looper.loop(Looper.java:137)
E/AndroidRuntime( 9418): 	at android.app.ActivityThread.main(ActivityThread.java:4745)
E/AndroidRuntime( 9418): 	at java.lang.reflect.Method.invokeNative(Native Method)
E/AndroidRuntime( 9418): 	at java.lang.reflect.Method.invoke(Method.java:511)
E/AndroidRuntime( 9418): 	at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:786)
E/AndroidRuntime( 9418): 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:553)
E/AndroidRuntime( 9418): 	at dalvik.system.NativeStart.main(Native Method)
E/AndroidRuntime( 9418): Caused by: java.lang.NullPointerException
E/AndroidRuntime( 9418): 	at com.google.android.apps.chrome.WelcomePageHelper.destroy(WelcomePageHelper.java:127)
E/AndroidRuntime( 9418): 	at com.google.android.apps.chrome.Tab.destroyInternal(Tab.java:976)
E/AndroidRuntime( 9418): 	at com.google.android.apps.chrome.Tab.destroy(Tab.java:937)
E/AndroidRuntime( 9418): 	at com.google.android.apps.chrome.SimpleChromeActivity.onDestroy(SimpleChromeActivity.java:200)
E/AndroidRuntime( 9418): 	at android.app.Activity.performDestroy(Activity.java:5172)
E/AndroidRuntime( 9418): 	at android.app.Instrumentation.callActivityOnDestroy(Instrumentation.java:1109)
E/AndroidRuntime( 9418): 	at android.app.ActivityThread.performDestroyActivity(ActivityThread.java:3260)
E/AndroidRuntime( 9418): 	... 11 more
W/ActivityManager(  303):   Force finishing activity com.android.chrome/com.google.android.apps.chrome.Main

So that seems like a second (not security-critical) bug, Grace. What do you think?

### ch...@gmail.com (2012-07-19)

Hi, guys. Thanks for the fast answer. I'll keep it confidential and be waiting for update. BTW, my first name is Artem :)

Best Regards,
Artem Chaykin

### kl...@chromium.org (2012-07-19)

SimpleChromeActivity was for the testing. As we have content shell now, we should just remove this.

### [Deleted User] (2012-07-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### [Deleted User] (2012-08-03)

Fixed by change: https://gerrit-int.chromium.org/#change,22864

### ch...@gmail.com (2012-08-13)

Can I ask when the fixed version will be released and when I can disclose this and id=138210 vulns?
Thanks!

### pa...@google.com (2012-08-13)

That's a question for Srikanth. I think the answer is "the fix will come out soon, in the next release", but I can't promise that. Please hold off on disclosure until we hear from Srikanth. Thank you!

### [Deleted User] (2012-08-13)

Yes - that is correct. Fix rollout will happen in a few weeks - so probably best to hold talking about it till then. 

### sc...@gmail.com (2012-08-20)

@chaykin.artem: thanks for the report! This qualifies for a $500 Chromium Security Reward (separate from the other one).

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### sc...@gmail.com (2012-10-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/138035?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061545)*
