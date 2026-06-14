# Security: RTL character in URL flips domain and path (Android 4.2 and earlier)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087276](https://issues.chromium.org/issues/40087276) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization>RTL |
| **Platforms** | Android |
| **Reporter** | ra...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2017-04-07 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: [56] + [stable] (Updated on April 3, 2017)
Operating System: [Android 4.1.2] 


Impact and Risk: the URL bar is the only reliable security indicator in browsers and if the only reliable security indicator could be controlled by an attacker it could carry adverse affects, For instance potentially tricking users into supplying sensitive information to a malicious website due to the fact that it could easily lead the users to believe that they are visiting is legitimate website as the address bar points to the correct website.

Reproduction Instructions/Proof of Concept:

1) Post the following link in the status bar: 127.0.0.1/ا/http://attack.com


2) You would notice that the URL has been flipped from Right to left and the status bar dispays http://attack.com/‭ا/127.0.0.1 while it displays the content from the IP address.

Suggested Fix: This bug does not work on iOS devices, hence, the screenshot was taken from an iOS device of google chrome which shows that URL must be shown like this.

## Attachments

- [PoC.jpg](attachments/PoC.jpg) (image/jpeg, 17.7 KB)
- [Suggested Fixture.jpg](attachments/Suggested Fixture.jpg) (image/jpeg, 24.1 KB)
- [Screenshot_2017-04-21-19-04-50.png](attachments/Screenshot_2017-04-21-19-04-50.png) (image/png, 62.6 KB)
- [Screenshot_2017-04-21-12-26-19.png](attachments/Screenshot_2017-04-21-12-26-19.png) (image/png, 64.1 KB)
- [Screenshot_2017-04-24-13-17-05.png](attachments/Screenshot_2017-04-24-13-17-05.png) (image/png, 54.4 KB)
- [Screenshot_2017-04-24-15-59-51.png](attachments/Screenshot_2017-04-24-15-59-51.png) (image/png, 55.0 KB)
- [Screenshot_2017-04-26-18-31-23.png](attachments/Screenshot_2017-04-26-18-31-23.png) (image/png, 72.4 KB)

## Timeline

### el...@chromium.org (2017-04-07)

This appears to be the same repro as https://crbug.com/chromium/708981 ?

### ra...@gmail.com (2017-04-07)

[Comment Deleted]

### ra...@gmail.com (2017-04-07)

[Comment Deleted]

### ra...@gmail.com (2017-04-09)

[Comment Deleted]

### do...@chromium.org (2017-04-09)

+mgiuca to dedupe.

[Monorail components: UI>Browser>Omnibox]

### ra...@gmail.com (2017-04-10)

[Comment Deleted]

### sh...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-04-12)

Hi, as with https://crbug.com/chromium/708981 I cannot reproduce this on Android in the latest version.

This is the same bug that was originally reported and fixed with https://crbug.com/chromium/609680 on Android. However, I am not duping to that yet, because if this is in fact still an issue on M56 then it is a regression.

Admittedly, I don't have Chrome 56 here (testing on 59) but it is not an issue for me that I can see. It is working as intended.

Please confirm that you are testing on Chrome 56 for Android, and not an older build.

I'm also confused because here you say it is fixed on iOS, but in https://crbug.com/chromium/708981, you reported this exact same bug on iOS.

### ra...@gmail.com (2017-04-12)

Hi, I just checked on Android again.. The bug is now not working on the Android 6.0.. However, It's working in older versions of Android (Latest version of chrome). To be more specific, Android version 4.1.2 - therefore, please look into the older versions of android such as 4.5 or 4.6 to check it. Regarding the iOS, I've sent the details, please look into it. Moreover, I apologize for the confusion I made. Thanks!

### mg...@chromium.org (2017-04-13)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-04-13)

Can't reproduce on Android 5.0 (Lollipop).

I am hunting around for an Android 4.x device. And not really sure how the Android version could affect this UX.

### mg...@chromium.org (2017-04-13)

+Ted: I'm having a hard time getting the right version of Android + the right version of Chrome. Do you have test devices? Are you able to repro this or find someone to do it?

The specific condition is Android 4.x + Chrome 56 (or any current channel of Chrome will do).

### te...@chromium.org (2017-04-13)

4.1 had a very broken implementation of RTL.  4.3 was really the first jellybean that was close to working.

All of the APIs that allow us to specify text direction and alignment are API 17.  4.1.2 is API 16.  I doubt there is anything that can be done here aside from disabling any RTL characters from being displayed (converting them all to punycode).

### mg...@chromium.org (2017-04-18)

Really? :| Do you think we should do that? Should I get a PM from the Omnibox team to help decide here?

### te...@chromium.org (2017-04-18)

I'm honestly not super convinced we should, but that is more from a maintenance perspective for devices that are nearly 5 years old.  Our coverage for these old devices in minimal and any special logic we introduce is likely to be bit-rotting immediately.

I think it would be fine to bring this up with the omnibox team as an issue (and if disabling RTL characters is easy then I'm less hesitant to make the shift), but I am tempted to mark this as WontFix as this is a problem with Android and there is only so much we should fight that.

### mg...@chromium.org (2017-04-19)

OK so I'm not sure if this is working on Kit Kat. If it's a a <=Jellybean only problem then it affects about 1/8 of users according to https://developer.android.com/about/dashboards/index.html. If it also includes Kit Kat then it affects about 3/8 of users.

Adding jdonnelly for Omnibox (not sure if you are familiar with the Android code). See #15: if you think it's easy to just disable RTL character rendering in the Omnibox (I guess just blacklist them and make them punycode on Android JB or earlier) then could you please find someone to do that? Else, WontFix.

Thanks

### ra...@gmail.com (2017-04-20)

[Comment Deleted]

### jd...@chromium.org (2017-04-20)

tommycli: I have a device we can flash KitKat on to test this.

tedchoc: can you confirm that if this issue is present on KitKat that 3/8 of all Android users would be affected? If so, this seems worth adding mgiuca's proposed fix.

emilyschechter: does that assessment sound right to you?

### mg...@chromium.org (2017-04-21)

I'm basing the 1/8 and 3/8 metrics on this dashboard:
https://developer.android.com/about/dashboards/index.html

The precise figure is 11.9% on JellyBean and earlier; 31.9% on KitKat and earlier (as at April 3, 2017).

### to...@chromium.org (2017-04-21)

I just tested this on 4.4, and it looks fine.

I will proceed to work backwards. I'm assuming based on #13 tedchoc@, that this problem only affects 4.2 and before.


### to...@chromium.org (2017-04-21)

4.3 also looks good.

### to...@chromium.org (2017-04-21)

I can confirm that this affects Android 4.2 and before (API level 17 and before).

I think this is worth a fix since 10.8% of our users are at this version and before. That's still over 100M devices...

I'm investigating how we can fix it. I think there can be a small fix.

### mg...@chromium.org (2017-04-24)

Maybe it's worth just banning RTL characters from appearing in URLs in Android 4.2 and earlier?

The code to manage URL escaping is in net/base/escape.cc (which is very general code, it might be hard to put Android-specific logic in there).

### to...@chromium.org (2017-04-24)

mgiuca: Thanks for the pointer! I am looking into this today. :)

### to...@chromium.org (2017-04-25)

One proposed fix. See screenshots for before and after: https://codereview.chromium.org/2839843002/

### to...@chromium.org (2017-04-27)

New fix in PS2

### bu...@chromium.org (2017-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e1fa8fc5972327ce78225c7de95153c63d3e3bb3

commit e1fa8fc5972327ce78225c7de95153c63d3e3bb3
Author: tommycli <tommycli@chromium.org>
Date: Thu Apr 27 19:06:56 2017

Android URL formatting: Disable RTL URLs for Android 4.2 and below.

Android 4.2 and below has a problematic RTL implementation. Force
formatted URLs to display in LTR.

BUG=709417

Review-Url: https://codereview.chromium.org/2839843002
Cr-Commit-Position: refs/heads/master@{#467740}

[modify] https://crrev.com/e1fa8fc5972327ce78225c7de95153c63d3e3bb3/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBar.java


### to...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

### ra...@gmail.com (2017-04-27)

Does it qualify for a bounty?

### mg...@chromium.org (2017-04-28)

#29: I think it falls into the bounty category, but the decision is not up to me (+awhalley).

The panel should keep in mind that this is a bug we already knew about, and had fixed (https://crbug.com/chromium/609680). But we didn't know the previous fix was ineffective on older versions of Android.

### ra...@gmail.com (2017-04-28)

If that's the case with android maybe that'd be the case with other operating systems such as iOS? Maybe tedc...@chromium.org have the idea of it since he was the one who told the reason in #15 for Android. (Still I'll check on other OS If get an access to suitable machine)

### mg...@chromium.org (2017-04-28)

The fix on iOS was independent to the Android one, so it would be a big coincidence if it also had an issue with older versions of iOS. This is an Android-specific problem.

### sh...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-28)

Let's see what the VRP panel say

### to...@chromium.org (2017-04-28)

Yes, FWIW, I think this report is worthy.

### to...@chromium.org (2017-04-28)

Fix should show up in Android Canary versions 3084.0 and later (not released yet).

### lg...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization>RTL UI>Security>UrlFormatting]

### aa...@google.com (2017-05-03)

[Empty comment from Monorail migration]

### to...@chromium.org (2017-05-03)

Nice! I fixed a "High" security bug!

### mg...@chromium.org (2017-05-04)

Downgrading this to Medium (fits the description of "Medium" spoof on https://www.chromium.org/developers/severity-guidelines, and also this is the exact same bug as https://crbug.com/chromium/609680, which is Medium, but on a much smaller set of devices).

### aw...@chromium.org (2017-05-05)

Hi mgiuca@ - I'm reverting it to high, but that's for spotting that https://crbug.com/chromium/609680 was still Medium. We discussed this at the VRP panel and agreed both fall into "Complete control over the apparent origin in the omnibox" which is high. Good point about the reduced population, but we don't like calling that a mitigation if we still support those platforms.  Cheers!

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### ra...@gmail.com (2017-05-05)

[Comment Deleted]

### ra...@gmail.com (2017-05-05)

[Comment Deleted]

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-05)

Congratulations rayyanh12@! The VRP panel decided to award $3,000 for this bug.  A member of our finance team will be in touch shortly to arrange payment.  Also how would you like to be credited?

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************



### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### ra...@gmail.com (2017-05-06)

[Comment Deleted]

### ra...@gmail.com (2017-05-06)

#47: Thank you. Can we discuss that via email? 

### aw...@chromium.org (2017-05-08)

rayyanh12@ - certainly - drop me a line at awhalley@chromium.org

### jd...@chromium.org (2017-05-09)

awhalley: should this have Merge-Request-59?

### aw...@chromium.org (2017-05-09)

Yep - been in dev a good few days.  Thanks!

### sh...@chromium.org (2017-05-09)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0c5c382d741cade4d1b89295a45a7fb4c97fe317

commit 0c5c382d741cade4d1b89295a45a7fb4c97fe317
Author: Tommy C. Li <tommycli@chromium.org>
Date: Tue May 09 16:34:10 2017

Android URL formatting: Disable RTL URLs for Android 4.2 and below.

Android 4.2 and below has a problematic RTL implementation. Force
formatted URLs to display in LTR.

BUG=709417

Review-Url: https://codereview.chromium.org/2839843002
Cr-Commit-Position: refs/heads/master@{#467740}
(cherry picked from commit e1fa8fc5972327ce78225c7de95153c63d3e3bb3)

Review-Url: https://codereview.chromium.org/2870943002 .
Cr-Commit-Position: refs/branch-heads/3071@{#480}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/0c5c382d741cade4d1b89295a45a7fb4c97fe317/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBar.java


### to...@chromium.org (2017-05-09)

I just merged the patch to 59. Thanks!

### aw...@google.com (2017-05-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/709417?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization>RTL, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/709415, crbug.com/chromium/709418]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087276)*
