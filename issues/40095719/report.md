# The Permission for an important activity is set to null, as the result it can launched by any app.

| Field | Value |
|-------|-------|
| **Issue ID** | [40095719](https://issues.chromium.org/issues/40095719) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Bookmarks |
| **Platforms** | Android |
| **Reporter** | ja...@gmail.com |
| **Assignee** | tw...@chromium.org |
| **Created** | 2019-07-16 |
| **Bounty** | $1,000.00 |

## Description

**-------------------------**

VULNERABILITY :

Bookmarks in Google Chrome can be added by any android app.As the permissions for the activity, org.chromium.chrome.browser.bookmarks.BookmarkAddActivity, is set to null.

**VERSION**

Chrome Version: 75.0.3770.143  

Operating System: Android above 5.0.1

---

## REPRODUCTION STEPS|

You need to have drozer configured with your android device and your PC.  

If you don't know how to configure, Please read the manual of Drozer.

1. Configure drozer with your phone/pc, to simulate the attack.
2. Type the command, run app.activity.info -a com.android.chrome.
3. You will see some activities, look for the actvity namely BookmarkAddActivity
4. You will see the permission for the activity is set to null. Therefore this means, this can be launched by any third-party app.
5. Run the command in the drozer; run app.activity.start --component com.android.chrome org.chromium.chrome.browser.bookmarks.BookmarkAddActivity --extra string title FacebookLogin --extra string url <https://fakeFacebookPage.com>
6. The above command will add a bookmark.

## EXPLOITATION

1. Can be used for Phishing purpose.

## Explanation :

As we know, Why bookmarks are used ?  

Thus suppose, if an attacker adds a bookmark with its title as FB LOGIN and its url be <https://fakefacebookpage.com>  

Then, When user tries to search for facebook login page, then the bookmarked link will appear as FB LOGIN, now if the user clicks the link, he will be under the control of attacker.

2. Attacker can add huge amount of bookmarks, in the victim's google chrome browser.

## FIX |

The vulnerability can be fixed by setting, the appropriate permission for using the activity.

## Attachments

- [bookmark_add_intent.mp4](attachments/bookmark_add_intent.mp4) (video/mp4, 1.6 MB)

## Timeline

### in...@chromium.org (2019-07-17)

aee@, can you please help to triage if this is a security vulnerability.

[Monorail components: UI>Browser>Bookmarks]

### ja...@gmail.com (2019-07-17)

Yes.. 

### oc...@google.com (2019-07-25)

+twellington, OWNER of chrome/android/java/src/org/chromium/chrome/browser/bookmarks/. Is this intentional? In any case the security impact here is low.

### tw...@chromium.org (2019-07-25)

It appears it is based on https://crbug.com/chromium/581961. +Ted to confirm, since this was added before my time.

### tw...@chromium.org (2019-07-25)

(or rather before my time on bookmarks :) )

+yusufo@ as well, who was a reviewer on the CL that added the intent handling.

### sh...@chromium.org (2019-07-25)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@google.com (2019-07-26)

I don't have a strong recollection of that requirement, but it is well documented in the bug twellington@ linked.  I think we should probably make that activity do nothing at this point (probably can't remove it till L is deprecated per the documentation).  I would just log to logcat saying this is no longer a supported feature.

### tw...@chromium.org (2019-07-30)

That seems simple enough, thanks for the input Ted.

### ja...@gmail.com (2019-08-30)

Hello it's  been long time, any update for me. 


### tw...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-17)

[Empty comment from Monorail migration]

### ja...@gmail.com (2019-11-01)

Any updates

### tw...@chromium.org (2019-11-01)

Initial CL will be sent out for review later today: https://chromium-review.googlesource.com/c/chromium/src/+/1895380

Tested using following adb command:
adb shell am start -n "com.google.android.apps.chrome/org.chromium.chrome.browser.bookmarks.BookmarkAddActivity" -d "www.test.com"

### tw...@chromium.org (2019-11-01)

Video of new behavior

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/de9cb61b27cc806bbbfeeecdc90247987a21ad1f

commit de9cb61b27cc806bbbfeeecdc90247987a21ad1f
Author: Theresa Wellington <twellington@chromium.org>
Date: Wed Nov 06 16:23:56 2019

Remove support for adding bookmarks in BookmarkAddActivity

Removes support for adding bookmarks in BookmarkAddActivity (originally
added for L-only). If the activity is triggered, we now output an
informational log, show a toast and finish immediately.

BUG=984513

Change-Id: I31a8038bbafd215f1db2d84b08c0d025073084ab
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1895380
Commit-Queue: Theresa  <twellington@chromium.org>
Reviewed-by: Brian White <bcwhite@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/heads/master@{#713027}

[modify] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/chrome/android/java/AndroidManifest.xml
[modify] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/chrome/android/java/monochrome_public_bundle__base_bundle_module.AndroidManifest.expected
[modify] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/chrome/android/java/src/org/chromium/chrome/browser/bookmarks/BookmarkAddActivity.java
[modify] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/chrome/android/java/src/org/chromium/chrome/browser/bookmarks/BookmarkUtils.java
[modify] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/chrome/android/java/strings/android_chrome_strings.grd
[add] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/chrome/android/java/strings/android_chrome_strings_grd/IDS_UNSUPPORTED.png.sha1
[modify] https://crrev.com/de9cb61b27cc806bbbfeeecdc90247987a21ad1f/tools/metrics/actions/actions.xml


### tw...@chromium.org (2019-11-06)

[Empty comment from Monorail migration]

### ja...@gmail.com (2019-11-07)

Hello google chrome team,

Is this eligible for bounty ?
If yes, then please provide me further steps.

Regards
Jatin

### sh...@chromium.org (2019-11-08)

[Empty comment from Monorail migration]

### ja...@gmail.com (2019-11-16)

Am I eligible for bounty..

### tw...@chromium.org (2019-11-16)

I'm not familiar with our bounty process/requirements.

+ochang@ - are you able to comment?

### oc...@google.com (2019-11-18)

This will be routed to the VRP panel to decide whether if this is eligible.

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### ja...@gmail.com (2019-12-19)

Thanks for rewarding, Mam.


I would like to Claim this wonderful reward, as soon as possible. As, I am a student, I will this reward to further polish my skills.
Can you please tell me the steps for claiming the reward.

Regards,

 

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gh...@gmail.com (2020-04-03)

test

### is...@google.com (2020-04-03)

This issue was migrated from crbug.com/chromium/984513?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095719)*
