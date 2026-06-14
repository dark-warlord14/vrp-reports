# javascript URL is broken in ChromeCustom tab for Android Apps

| Field | Value |
|-------|-------|
| **Issue ID** | [40056896](https://issues.chromium.org/issues/40056896) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents, UI>Browser>Mobile>CustomTabs |
| **Platforms** | Android |
| **Reporter** | as...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2021-08-16 |
| **Bounty** | $1,000.00 |

## Description

**Device name:** Moto G(7)

**From "Settings > About Chrome"**  

**Application version:** 92.0.4515.131  

**Operating system:** Android 10

**URLs (if applicable):**

**Steps to reproduce:**  

**(1)** From Android app try to launch customtabs with javascript url  

**(2)** New chrome update doesn't handle javascript URL  

**(3)**

**Expected result:** Chrome customtabs in Android app should be able to open Javascript URL

Below is the code snippet to replicate the issue

```
    String openUrl = "javascript:    var targetUrl = 'https://www.myhostedsite.com';    var params = {'token' : 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9'};    var submitForm = document.createElement('form');    submitForm.method='post';    submitForm.action = targetUrl;    for (var param in params) {        var inputValues = document.createElement('input');        inputValues.setAttribute('type', 'text');        inputValues.setAttribute('name', param);        inputValues.setAttribute('value', params[param]);        submitForm.appendChild(inputValues);    }    document.body.appendChild(submitForm);    submitForm.submit();    document.body.removeChild(submitForm);";  

            CustomTabsIntent.Builder builder = new CustomTabsIntent.Builder();  

            // if OCA page block branch journey(popup from branch on OCA page)  
            Uri uri = Uri.parse(url);  
            builder.build().launchUrl(context, uri);

```

## Timeline

### ke...@chromium.org (2021-08-17)

Reporter@: Could you please provide sample test file to check this issue and screencast for better understanding the issue

Thanks!

### as...@gmail.com (2021-08-18)

I created a small video from my device to replicate the issue.. Please find the link below
https://drive.google.com/file/d/13C1tp2m4wteyTw41DC5_iWKFH_iYRwdC/view?usp=sharing

In the above video you can see that on older version of the chrome app the customtab is opened successfully. After upgrading chrome browser the link stops working and the app gets exception that "AcitvityNotFound". 

The source code of the sample app can be found below. This app is sample app with one button, clicking on which it tries to use javascript URL. 
https://github.com/pickeyboy/chrometab

Happy to share more information if required related to this issue. 


### [Deleted User] (2021-08-18)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-08-19)

Thanks for providing the info.
Requesting someone from the dev team to kindly look into this issue or help in reassigning to proper owner.

Thanks!!

[Monorail components: Blink]

### as...@gmail.com (2021-08-24)

Hi There, 

I found some additional information from links below: 

We compared the AndroidManifest file for the previous version and latest version and found that  " <data android:scheme="javascript" />" support has been removed from intent-filter of Chrome browser. 
Referral links are as below: 
https://chromium.googlesource.com/chromium/src/+/refs/tags/88.0.4324.181/chrome/android/java/AndroidManifest.xml

https://chromium.googlesource.com/chromium/src/+/refs/tags/92.0.4515.131/chrome/android/java/AndroidManifest.xml?autodive=0%2F%2F%2F%2F%2F%2F%2F%2F

Does this mean, chrome won't support javascript URL from this version onwards? Kindly confirm. 

### js...@google.com (2021-08-25)

This was removed in https://chromium-review.googlesource.com/c/chromium/src/+/2826392. Michael, is this a permanent change, or what should developers expect going forward wrt javascript: URLs in Chrome custom tabs?

[Monorail components: -Blink Mobile>Fundamentals]

### mt...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

[Monorail components: -Mobile>Fundamentals Mobile>Intents]

### ha...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Mobile>CustomTabs]

### mt...@chromium.org (2021-08-25)

Hi ashwinagarwal, thanks for the report.

I'll give the CustomTab folks a chance to weigh in, but it looks to me like it was an oversight that this was ever possible in CCT. We disallow loading javascript URLs in other cases (I think for security reasons?), even in CCT for any intents we receive except the initial one.

Are you experiencing any breakages in production systems?

### mt...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### mt...@chromium.org (2021-08-25)

I think we might need to treat this as a security bug. See https://crbug.com/chromium/169401.

We currently still allow javascript 'URLs' to load in CCT because CCT fails to call IntentHandler#shouldIgnoreIntent for its initial intent (though it does for subsequent intents).

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### ha...@chromium.org (2021-08-25)

[Empty comment from Monorail migration]

### as...@gmail.com (2021-08-26)

Hi mthiesse

This is a big impact for our app because all our in-app browser session handover is failing due to this. All of the links opened in the CCT through app is no more working because the handover happen over POST request which we current do it through javascript URL. Our customers initially reported error on Chrome version 92.0.4515.131 in Android playstore. 

Any clarification on changes around supporting javascript URL in CCT or announcement in release note would help. 

Regards
Ashwin

### pe...@chromium.org (2021-08-26)

The easiest thing to do may be to add a check in LaunchIntentDispatcher#launchCustomTabActivity that just no-ops when shouldIgnoreIntent returns true.

Otherwise we need to think of what Custom Tabs UI to show for invalid Intents.

### mt...@chromium.org (2021-08-26)

Re #14 I'll defer to the security team for how to deal with breakages like this and surrounding comms.

### ye...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-08-27)

I do think blocking javascript: in CCTs is the correct result, though I think peconn@ is in a better position to comment on the correct behavior from the CCT API perspective. We don’t typically do comms when fixing a security issue breaks unintended functionality, and I can’t find any release notes section in the CCT docs (though peconn@ can also probably comment here).

CCTs and regular Intents were not meant to issue POST requests (doing so would violate a user’s expectations of safety from simply clicking on a link), so the use case in c#0 was relying on an undocumented misfeature. I think a potential way forward for this use case would be to write the session handoff page into a temporary file, expose it to the CCT using a FileProvider and grantUriPermission(), and then opening the CCT with a content:// URI. Alternatively, the server should accept a GET request and redirect back to the app.

### ad...@google.com (2021-09-07)

ashwinagarwal@ sorry on behalf of everyone here that we inadvertently broke your use-case, even if it wasn't something that was intentionally allowed in the first place. Does the suggestion in https://crbug.com/chromium/1240065#c18 help you?

Regarding https://crbug.com/chromium/1240065#c11 and https://crbug.com/chromium/1240065#c15 showing that there's still some remaining work to do to fully block javascript: URIs here, I'm going to provisionally rate that as severity medium (similar to https://crbug.com/chromium/169401) and since the problem has existed for a while, adding FoundIn tags to indicate that this impacts stable.

ashwinagarwal@ if this results in us making a security fix to tighten this up a little more, you'll get a credit in the Chrome release notes. By what name/handle/identifier would you like to be credited?

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-09)

peconn: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@gmail.com (2021-09-16)

Hi @adetaylor Thanks for your quick response. And thanks for credit offer in Chrome release. Please use following information "Ashwin Agrawal from Optus, Sydney" as name 

Regards
Ashwin Agrawal 

### [Deleted User] (2021-09-23)

peconn: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-15)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-08)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-07-20)

peconn - does this still reproduce? Is there perhaps another owner that might have time to look at this?

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### pe...@chromium.org (2022-08-08)

I've got a CL out for this, it's about halfway there:
  https://chromium-review.googlesource.com/c/chromium/src/+/3790983

### gi...@appspot.gserviceaccount.com (2022-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a006fac8a949c5afb61dc90a1ff6d62699d334dd

commit a006fac8a949c5afb61dc90a1ff6d62699d334dd
Author: Peter E Conn <peconn@google.com>
Date: Thu Aug 11 10:31:09 2022

🛃 Prevent CCT launch to JavaScript URLs.

Because Custom Tabs don't have a fallback UI like ChromeTabbedActivity
does (the New Tab Page), it would be awkward to check whether a given
URL is valid after launching the Custom Tab. So we prevent the Custom
Tab being launched if the URL is invalid.

Bug: 1240065
Change-Id: If4e5ce0ff6522f06a400f70746cfc08808dabcbc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3790983
Commit-Queue: Peter Conn <peconn@chromium.org>
Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1033921}

[modify] https://crrev.com/a006fac8a949c5afb61dc90a1ff6d62699d334dd/chrome/android/java/src/org/chromium/chrome/browser/LaunchIntentDispatcher.java
[modify] https://crrev.com/a006fac8a949c5afb61dc90a1ff6d62699d334dd/chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java
[modify] https://crrev.com/a006fac8a949c5afb61dc90a1ff6d62699d334dd/chrome/android/java/src/org/chromium/chrome/browser/app/ChromeActivity.java
[modify] https://crrev.com/a006fac8a949c5afb61dc90a1ff6d62699d334dd/chrome/android/javatests/src/org/chromium/chrome/browser/IntentHandlerUnitTest.java
[modify] https://crrev.com/a006fac8a949c5afb61dc90a1ff6d62699d334dd/chrome/android/java/src/org/chromium/chrome/browser/customtabs/BaseCustomTabActivity.java
[modify] https://crrev.com/a006fac8a949c5afb61dc90a1ff6d62699d334dd/chrome/android/javatests/src/org/chromium/chrome/browser/customtabs/CustomTabActivityTest.java


### pe...@chromium.org (2022-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, Ashwin! Due to the bug you reported having security consequences, the Chrome VRP (Vulnerability Rewards Program [1]) panel has decided to award a $1,000 reward to you for this report. A member of our finance team will reach out to you soon via email to arrange payment. Thank you for reporting this issue to us! 

[1] https://g.co/chrome/vrp

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1240065?no_tracker_redirect=1

[Multiple monorail components: Mobile>Intents, UI>Browser>Mobile>CustomTabs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056896)*
