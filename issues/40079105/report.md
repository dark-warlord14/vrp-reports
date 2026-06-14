# Security: Chrome for Android - URL bar spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40079105](https://issues.chromium.org/issues/40079105) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | kh...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2014-03-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This allows for phishing attacks where a malicious site can spoof the URL of another site.

**VERSION**  

Chrome Version: 33.0.1750.136 stable  

Operating System: Android 4.4.2; Nexus 5 Build/KOT49H

## Attachments

- [repro1.html](attachments/repro1.html) (text/html, 234 B)
- [repro2.html](attachments/repro2.html) (text/html, 297 B)

## Timeline

### js...@chromium.org (2014-03-13)

This looks like some bugs we used to have on other platforms, where the omnibox would get updated too early during a navigation. Adding some navigation knowledgeable people for assistance.

@palmer - Could you please route this to the correct owner on Android?


### cl...@chromium.org (2014-03-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-24)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-01)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pa...@chromium.org (2014-04-01)

Ted, are you a good person for this? Or do you know someone who is? Thanks!

### cr...@chromium.org (2014-04-04)

@dtrainor: This repro makes me think it's similar to https://crbug.com/chromium/324969, where we needed to make Android react to DidAccessInitialDocument.  Do you think that's involved here?

### dt...@chromium.org (2014-04-07)

It does look like it's related... the fix was more to keep the Java Tab object from using the old incorrect URL in that case.  Maybe we're missing something from native here, although it looks like we're calling WebContents::GetURL(), which gets the visible entry from the navigation controller and returns the virtual url.

### cl...@chromium.org (2014-04-10)

tedchoc@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-18)

tedchoc@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-04-26)

tedchoc@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ke...@chromium.org (2014-04-28)

dtrainor: Do you think you could have a look at this one?

### dt...@chromium.org (2014-05-02)

Will take a look.

### dt...@chromium.org (2014-05-06)

What's the expected behavior here?  The navigation controller entries all return keitahaga.com (active, visible, and pending).  The URL and the virtual URL also all match.  Desktop shows about:blank.  What should we be querying to get the right URL?

### cr...@chromium.org (2014-05-06)

Desktop is using NavigationControllerImpl::GetVisibleEntry(), so if it's showing about:blank that's where it's coming from.  That takes into account things like whether it's the initial navigation (false for document.write) and whether the initial document has been accessed.

I'm surprised you're seeing the attack URL from GetVisibleEntry().  Can you check how that code's actual behavior differs between desktop and Android, and why they're returning different results?

### dt...@chromium.org (2014-05-07)

Still digging some more... looks like the following is happening (still haven't tracked down the trigger though):

1. We have a pending entry with is_renderer_initiated = true AND IsUnmodifiedBlankTab.  This properly shows about:blank
2. At some point we get a FrameHostMsg_OpenURL from the renderer (for the new tab I guess?)
3. This builds a new pending entry that has is_renderer_initiated = false.  So even when IsUnmodifiedBlankTab is false we still show this pending entry as the valid url.

I need to track why we're getting an OpenURL message.

### dt...@chromium.org (2014-05-07)

Ah I think I tracked it down.  We're losing data in the jni bridge from native -> java -> native... We don't pass is_renderer_initiated so that gets lost in the translation process.  Hmm it looks like we might lose other data in this transfer.  I don't know if all of it is required though.  I can add the is_renderer_initiated though.

### dt...@chromium.org (2014-05-07)

Ok actually tracked down the cause.  It wasn't JNI related but it it happens in web_contents_delegate_android.  We just call web_contents->GetController().LoadURL(...) and pass in a few parameters.  We should really be calling web_contents->GetController().LoadURLWithParams(LoadURLParams&) to pass the relevant data.  We're different here because we don't use browser_navigator (we don't have a browser) and don't use chrome::Navigate to do our navigations.  There is a *ton* of stuff in Navigate that we're probably missing/rewriting throughout the codebase... we should look at refactoring that to maybe not rely on a browser instance and sharing that to Android.

I have a fix that populates the LoadURLParams from an OpenURLParams and use that in the right place.  I will upload that shortly.

### cl...@chromium.org (2014-05-13)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-05-13)

Dtrainor@, is this a WIP. Is there a codereview started (please add link here), if yes, please add WIP in the labels list.

### dt...@chromium.org (2014-05-13)

https://chromiumcodereview.appspot.com/267253007/ and https://chrome-internal-review.googlesource.com/#/c/163332/ are the two related CLs.  Working on the best way to test the fix and it might have to be downstream until we have a proper concept of multiple tabs upstream.

### bu...@chromium.org (2014-05-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98a50b76141f0b14f292f49ce376e6554142d5e2

commit 98a50b76141f0b14f292f49ce376e6554142d5e2
Author: dtrainor@chromium.org <dtrainor@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri May 30 17:44:30 2014

Use LoadURLWithParams in ChromeWebContentsDelegateAndroid

Build a LoadURLParams object from the OpenURLParams and properly set all
parameters on that object when calling into NavigationController.  This makes
sure we set the correct state for the load.

BUG=352083

Review URL: https://codereview.chromium.org/267253007

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@273865 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-05-30)

------------------------------------------------------------------
r273865 | dtrainor@chromium.org | 2014-05-30T17:44:30.362656Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/android/content_view_core_impl.h?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/android_webview/java/src/org/chromium/android_webview/AwWebContentsDelegateAdapter.java?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/components/web_contents_delegate_android/web_contents_delegate_android.cc?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/android/java/src/org/chromium/chrome/browser/Tab.java?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/public/android/java/src/org/chromium/content/browser/ContentViewCore.java?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/android/tab_android.cc?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/components/web_contents_delegate_android/android/java/src/org/chromium/components/web_contents_delegate_android/WebContentsDelegateAndroid.java?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/android/tab_android.h?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/public/android/java/src/org/chromium/content/browser/LoadUrlParams.java?r1=273865&r2=273864&pathrev=273865
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/android/content_view_core_impl.cc?r1=273865&r2=273864&pathrev=273865

Use LoadURLWithParams in ChromeWebContentsDelegateAndroid

Build a LoadURLParams object from the OpenURLParams and properly set all
parameters on that object when calling into NavigationController.  This makes
sure we set the correct state for the load.

BUG=352083

Review URL: https://codereview.chromium.org/267253007
-----------------------------------------------------------------

### bu...@chromium.org (2014-05-30)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/163332

### dt...@chromium.org (2014-05-30)

Fixed on trunk.  Added M-36 label as well.  Merge requested for M-36 first.

### cl...@chromium.org (2014-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2014-06-03)

Approved for 36.  Please re-request if you want it for 35.

### ti...@chromium.org (2014-06-03)

Removing M-35 (this won't make that timeline).

dtrainor@ - please merge this to M-36 (branch 1985).

### dt...@chromium.org (2014-06-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-06-04)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/165232

### bu...@chromium.org (2014-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/086e4be496f864c0379507a03239caadffbc79c3

commit 086e4be496f864c0379507a03239caadffbc79c3
Author: dtrainor@chromium.org <dtrainor@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jun 04 19:57:19 2014

Merge 273865 "Use LoadURLWithParams in ChromeWebContentsDelegate..."

> Use LoadURLWithParams in ChromeWebContentsDelegateAndroid
> 
> Build a LoadURLParams object from the OpenURLParams and properly set all
> parameters on that object when calling into NavigationController.  This makes
> sure we set the correct state for the load.
> 
> BUG=352083
> 
> Review URL: https://codereview.chromium.org/267253007

TBR=dtrainor@chromium.org

Review URL: https://codereview.chromium.org/317733005

git-svn-id: svn://svn.chromium.org/chrome/branches/1985/src@274888 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-06-04)

------------------------------------------------------------------
r274888 | dtrainor@chromium.org | 2014-06-04T19:57:19.618641Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/content/public/android/java/src/org/chromium/content/browser/LoadUrlParams.java?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/content/browser/android/content_view_core_impl.cc?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/content/browser/android/content_view_core_impl.h?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/android_webview/java/src/org/chromium/android_webview/AwWebContentsDelegateAdapter.java?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/components/web_contents_delegate_android/web_contents_delegate_android.cc?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/chrome/android/java/src/org/chromium/chrome/browser/Tab.java?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/content/public/android/java/src/org/chromium/content/browser/ContentViewCore.java?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/chrome/browser/android/tab_android.cc?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/components/web_contents_delegate_android/android/java/src/org/chromium/components/web_contents_delegate_android/WebContentsDelegateAndroid.java?r1=274888&r2=274887&pathrev=274888
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/chrome/browser/android/tab_android.h?r1=274888&r2=274887&pathrev=274888

Merge 273865 "Use LoadURLWithParams in ChromeWebContentsDelegate..."

> Use LoadURLWithParams in ChromeWebContentsDelegateAndroid
> 
> Build a LoadURLParams object from the OpenURLParams and properly set all
> parameters on that object when calling into NavigationController.  This makes
> sure we set the correct state for the load.
> 
> BUG=352083
> 
> Review URL: https://codereview.chromium.org/267253007

TBR=dtrainor@chromium.org

Review URL: https://codereview.chromium.org/317733005
-----------------------------------------------------------------

### cl...@chromium.org (2014-06-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-06-05)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/086e4be496f864c0379507a03239caadffbc79c3

commit 086e4be496f864c0379507a03239caadffbc79c3
Author: dtrainor@chromium.org <dtrainor@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jun 04 19:57:19 2014


### bu...@chromium.org (2014-06-10)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/165553

### in...@chromium.org (2014-06-17)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

Congratulations- $3000 for this report! 

We'll credit you as "khaga19937" in our release notes. If you want to be known as another name, please update this bug ASAP with that name.

Someone should be in contact within 1-2 weeks to arrange payment. If you haven't received an update by then, please either update this bug or e-mail me directly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
          *********************************

### ti...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-15)

[Empty comment from Monorail migration]

### kh...@gmail.com (2014-07-15)

Credit as "Keita Haga" would be good. Thanks! :-)

### ti...@chromium.org (2014-07-16)

Done: http://googlechromereleases.blogspot.com/2014/07/chrome-for-android-update.html

### kh...@gmail.com (2014-07-17)

Thanks!

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-11)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-09-17)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/352083?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079105)*
