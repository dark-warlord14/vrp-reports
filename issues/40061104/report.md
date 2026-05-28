# Security: Web Share dialog URL is incorrectly elided in Android (ineffective fix for issue 1329541)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061104](https://issues.chromium.org/issues/40061104) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebShare, UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2022-09-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The fix for <https://crbug.com/chromium/1329541> in commit f2b34be8865a6b63005ebc65588aa49e0392e91c is ineffective.

The patch changes the URL display area to elide text from the end instead of the beginning. However, this is simple text elision performed by Android, not URL-aware elision provided by Chrome. Therefore, it elides the URL from the end of the string, not the end of the origin. The elision will include the path, hash, or other part of the URL after the origin.

For example, current behavior elides <https://subdomain.example.com/test/abc> as ...ample.com/test/abc in a particularly narrow display area, instead of ...in.example.com or https://...in.example.com

Additionally, <https://crbug.com/chromium/1329541> only describes invoking the share dialog from the browser menu, but this is also possible by calling navigator.share() in JavaScript. navigator.share() intentionally accepts an arbitrary URL, but the URL should still be reasonably displayed.

Variations that should be tested before considering this report fixed:  

\* Long subdomains (fixed in <https://crbug.com/chromium/1329541>)  

\* Long paths (verified repro)  

\* Long hashes (verified repro)  

\* Long query string parameters (verified repro)

**VERSION**  

Chrome Version: 105.0.5195.136 Stable, 108.0.5316.0 Canary  

Operating System: Android 12

**REPRODUCTION CASE**  

Scenario 1: navigator.share()

1. Navigate to <https://alesandroortiz.com/security/chromium/android-share-elision-1.html>
2. Tap once on page

Scenario 2: Fullscreen + navigator.share()

1. Navigate to <https://alesandroortiz.com/security/chromium/android-share-elision-2.html>
2. Tap twice on page (once to enter fullscreen, and again to show share dialog)

Scenario 3: Manual share

1. Navigate to <https://alesandroortiz.com/security/chromium/android-share-elision-3.html>
2. Open browser menu
3. Tap "Share"

For all scenarios:  

Observed: Share dialog elides URL from end of string, even if this hides the origin.  

Expected: Share dialog elides URL from end of origin, to ensure the end of the origin is always shown.

Expected behavior should be consistent with <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/url_display_guidelines/url_display_guidelines.md#eliding-urls>

Attached is video recording of all scenarios using 108.0.5316.0 Canary on Android 12.

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [android-share-elision-1.html](attachments/android-share-elision-1.html) (text/plain, 821 B)
- [android-share-elision-2.html](attachments/android-share-elision-2.html) (text/plain, 977 B)
- [android-share-elision-3.html](attachments/android-share-elision-3.html) (text/plain, 730 B)
- [android-share-incorrect-elision.mp4](attachments/android-share-incorrect-elision.mp4) (video/mp4, 2.6 MB)
- [android-share-elision-4.html](attachments/android-share-elision-4.html) (text/plain, 987 B)
- [android-share-inverted-fields.jpg](attachments/android-share-inverted-fields.jpg) (image/jpeg, 259.9 KB)
- [before-patch.png](attachments/before-patch.png) (image/png, 146.0 KB)
- [before-patch-2.png](attachments/before-patch-2.png) (image/png, 175.6 KB)
- [after-patch.png](attachments/after-patch.png) (image/png, 140.2 KB)
- [after-patch-2.png](attachments/after-patch-2.png) (image/png, 177.9 KB)
- [after-patch-long-origin.png](attachments/after-patch-long-origin.png) (image/png, 143.3 KB)
- [before-patch-Canary-5882.jpg](attachments/before-patch-Canary-5882.jpg) (image/jpeg, 145.5 KB)
- [after-patch-Canary-5883.jpg](attachments/after-patch-Canary-5883.jpg) (image/jpeg, 140.9 KB)

## Timeline

### [Deleted User] (2022-09-23)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-09-23)

There's some relevant comments in https://crbug.com/chromium/1329541 (comments 10-19) that show what led to the current behavior instead of safe behavior. Seems like only a URL without a path, hash, or other components was used to test.

It's unclear if sharing folks were okay with removing path, hash, and other URL components. This was asked in https://crbug.com/1329541#c17 but not clear to me if there was ever an answer (the next lgtm is ambiguous about whether it's for the CL or the preceding question).

There's a few options, in order of apparent suitability:
* formatUrlForSecurityDisplay() with SchemeDisplay.OMIT_HTTP_AND_HTTPS or OMIT_CRYPTOGRAPHIC which I think would result in https://subdomain.example.com/test -> ...omain.example.com (used in patchset 2 but with default scheme display option of SHOW: https://chromium-review.googlesource.com/c/chromium/src/+/3698524/2 )
* formatUrlForDisplayOmitSchemePathAndTrivialSubdomains() which I think would result in https://subdomain.example.com/test -> ...omain.example.com
* formatOriginForSecurityDisplay() with SchemeDisplay.OMIT_HTTP_AND_HTTPS or OMIT_CRYPTOGRAPHIC which I think would result in https://subdomain.example.com/test -> ...omain.example.com

It's also worth testing these with ports in origins, to ensure they are displayed (they can't be excessively long so not an issue for elision).

I've uploaded a CL to use formatUrlForSecurityDisplay() as suggested in several comments of the other crbug, but with SchemeDisplay.OMIT_HTTP_AND_HTTPS:
https://chromium-review.googlesource.com/c/chromium/src/+/3913610/

I haven't tested my CL, so would appreciate someone building and testing that patch. I also don't have any privileges, so also need someone to trigger the automated tests, etc.

### hc...@google.com (2022-09-23)

Reproed on android  105.0.5195.136

making finnur@ owner as they were owner of https://crbug.com/chromium/1329541, added a bunch of CCs from that bug as well to comment on what fixes (if any) should look like.

[Monorail components: Blink>WebShare UI>Security>UrlFormatting]

### [Deleted User] (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-23)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-09-23)

While less security-relevant, the change in commit f2b34be8865a6b63005ebc65588aa49e0392e91c also affected how the URL is displayed when sharing highlighted text. After the change, the end of the URL is shown which can look odd to users if there's anything other than spaces and unencoded characters.

e.g. https://example.com/#:~:text=This%20domain%20is%20for%20use%20in%20illustrative%20examples is shown as "...main is for use in illustrative examples". Before, the beginning of the URL was shown, which wasn't safe per the other crbug but looked better than current behavior. Fixing this crbug would result in appropriate URL display when sharing highlighted text.



### al...@alesandroortiz.com (2022-09-23)

To avoid the ellipsis before the URL, an attacker can reverse the fields and set a fake URL in the title and set a fake title at the end of the URL.

PoC with navigator.share() (but works the same in any other sharing method): https://alesandroortiz.com/security/chromium/android-share-elision-4.html

### fi...@chromium.org (2022-09-26)

The suggested approach by OP was tried in patch 2 of the fix and later switched back to the original behavior...
https://chromium-review.googlesource.com/c/chromium/src/+/3698524/2..3
... after discussion on the original bug ...
https://bugs.chromium.org/p/chromium/issues/detail?id=1329541#c11

I believe the reason was that using this function changes behavior in how the sharing info is presented.

I'm not sure how to proceed, but I think others on this thread are better suited at discussing the merits of which function to use, both from a security perspective (cthomp) and feature perspective (ericwilligers).

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### fi...@chromium.org (2022-09-28)

Looking at the test results, it would seem that when sharing from https://www.example.com, we go from:

example.com   ... with the old function, to ... 
www.example.com  ... with the new function.

This seems acceptable to me, but I don't have much webshare context to say for sure. 

WDYT, Eric?

### al...@alesandroortiz.com (2022-09-28)

Thanks for the CQ+1s, finnur@.

If webshare folks want to remove trivial subdomains, I can try doing that prior to passing URL through formatUrlForSecurityDisplay. With current patch, behavior with other subdomains remains the same.

Will wait for feedback requested in https://crbug.com/chromium/1367085#c12.

### er...@chromium.org (2022-09-29)

The change https://crrev.com/c/3913610 seems fine to me.

We should show somebody from the privacy team, what the dialog looks like with and without the patch.


### fi...@chromium.org (2022-09-30)

Can you provide those, Alesandro?

### al...@alesandroortiz.com (2022-09-30)

If there's an easy way to get an APK from a trybot, I'm glad to do it. If not, might be faster for someone to build internally and attach APK for me to take screenshots.

finnur@, do you know if there's an APK built somewhere publicly, or are you able to build and attach the APK?

### [Deleted User] (2022-10-14)

finnur: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-10-21)

I haven't forgotten about this. I'll refresh my build server next week for this and a couple of other bugs, so should have screenshots sometime next week.

### fi...@chromium.org (2022-10-21)

Oh, sorry, I didn't see your question (https://crbug.com/chromium/1367085#c16). 

I am not aware of an ability to get APKs from trybot servers, but usually there's no need as you can just build it locally. It should be in your out/___foo___/apks/ directory.

### al...@alesandroortiz.com (2022-11-01)

I refreshed my build server tonight and am building the Android APK now, so will have screenshots sometime tonight (or tomorrow if there are unexpected build issues). I don't have a local build since I use it infrequently, so I keep a remote build server, but hadn't used it since July so needed a refresh.

### al...@alesandroortiz.com (2022-11-01)

Attached screenshots before patch and after patch, including after patch with long origin (to ensure that's handled well).

I'm not sure if it "looks" better to have the scheme, since some Chrome for Android permission dialogs do show the scheme alongside origin (e.g. Bluetooth device chooser dialog). I'm inclined to add the scheme, but will defer to the team since screenshots in https://crbug.com/chromium/1329541 show that it didn't have the scheme before either. The scheme would be hidden with long origins anyway, so may be inconsistent.

### fi...@chromium.org (2022-11-02)

Thanks for the screenshots, alesandro@

I have contacted Privacy and asked them to weigh in.

### fi...@chromium.org (2022-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-17)

finnur: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-11-29)

Friendly ping: Checking in to see if the Privacy team has provided any feedback or if they need more time. (I'm sorry it took a while to provide screenshots.)

### sa...@chromium.org (2022-11-30)

Clarification on https://crbug.com/chromium/1367085#c22 - finnur@, who did you contact from privacy?

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### fi...@chromium.org (2022-12-08)

[Empty comment from Monorail migration]

### to...@chromium.org (2022-12-08)

From a privacy perspective I think it's mainly important that the user knows what they will be sharing. As such, I think the requirements are pretty much aligned with those of the security team. Personally I think that the schemeless origin (or site if the origin is too long to be displayed), along with the title conveys the most reliable information for users to infer what will be shared. The current approach matches that, so looks good to me 👍

### xi...@chromium.org (2022-12-26)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-04-22)

Hi folks, sorry for not following up on this.

Is https://crbug.com/chromium/1367085#c30 the approval from the Privacy team?

My CL [1] now has merge conflicts, so will need to take a look within a couple of weeks to rebase and retest patch.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3913610

### [Deleted User] (2023-05-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fi...@chromium.org (2023-07-04)

The merge conflicts look easy to overcome, please update when you can. Also, https://crbug.com/chromium/1367085#c30 is the approval needed.

If you sync again, fix the conflicts and merge, then I think we can get a quick resolution on this.

### fi...@chromium.org (2023-07-05)

Also, in order to minimize the chances of this falling through the cracks again I want to mention that I'll be OOO for a bit at the end of next week.

If you don't have time to sync and want me to lead the landing of the fix, just say the word. I'd be happy to help out.

### al...@alesandroortiz.com (2023-07-08)

Thanks for confirming https://crbug.com/chromium/1367085#c30 is the Privacy team approval. Will update CL next week (hopefully before you're OOO).

### al...@alesandroortiz.com (2023-07-08)

I pretended it's already next week and resolved the merge conflicts. However, edit.chromium.org created a new CL instead of updating my existing CL.

Please review https://chromium-review.googlesource.com/c/chromium/src/+/4670811 instead of the original CL.

Added finnur@ and two code owners as reviewers. See this comment for code-owner reasoning: https://chromium-review.googlesource.com/c/chromium/src/+/4670811/comments/c00f655d_3acbfb43

### al...@alesandroortiz.com (2023-07-08)

finnur@ (or anyone else with edit perm): Can you please cc the CL's reviewers into this crbug? Thanks!

### ct...@chromium.org (2023-07-08)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-07-08)

Thanks cthomp@!

### we...@google.com (2023-07-10)

Thanks for jumping in and propose a fix!!

Changes in crrev.com/c/4670811 LGTM. +boonsiri  for vis on this behavior change (see https://crbug.com/chromium/1367085#c21)

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0e8f231c58e749551637f25a1f9fe926f2ad9897

commit 0e8f231c58e749551637f25a1f9fe926f2ad9897
Author: Alesandro Ortiz <alesandro@alesandroortiz.com>
Date: Mon Jul 10 21:45:05 2023

[Android]: Webshare: Adjust URL formatting in header.

Use formatUrlForSecurityDisplay() in share dialog.
Fix tests to use same URL formatting method as share dialog code, and
change test input URL to a URL with path, query, and hash components
to ensure these are handled properly (i.e. removed).

Bug: 1367085
Change-Id: Ib04d3d8d16588d810c2ea916d218e7e058cf5a56
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4670811
Reviewed-by: Wenyu Fu <wenyufu@chromium.org>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Sophey Dong <sophey@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1168335}

[modify] https://crrev.com/0e8f231c58e749551637f25a1f9fe926f2ad9897/chrome/browser/share/android/java/src/org/chromium/chrome/browser/share/share_sheet/ShareSheetBottomSheetContent.java
[modify] https://crrev.com/0e8f231c58e749551637f25a1f9fe926f2ad9897/chrome/browser/share/android/javatests/src/org/chromium/chrome/browser/share/share_sheet/ShareSheetBottomSheetContentTest.java


### al...@alesandroortiz.com (2023-07-10)

Thanks for review + merge!

I'll verify fix once it lands on Canary.

finnur@: Since I don't have commit access, can you please do backmerges as needed? If I had commit access I would handle them.

### fi...@chromium.org (2023-07-11)

Thanks for offering to verify, Alesandro!

I'd be happy to do the backmerges if they fit within my schedule for this week (because I'm OOO next week). 

I'm not sure which branches we'd need. I'll go with 116 until someone tells me otherwise...

### ct...@chromium.org (2023-07-11)

Marking this as Fixed now that the CL has landed so that the automated security tooling with Sheriffbot will kick in for merges.

### [Deleted User] (2023-07-11)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2023-07-12)

Verified as fixed in Canary 117.0.5883.0 on Android 12, physical device. Tested with PoCs from https://crbug.com/chromium/1367085#c0, https://crbug.com/chromium/1367085#c8, https://crbug.com/chromium/1367085#c9, and long origins on badssl.com

Attached screenshots from today of first PoC, 117.0.5882.0 before patch and 117.0.5883.0 after patch.

### fi...@chromium.org (2023-07-12)

Thanks for verifying. I have started the merge process.

### [Deleted User] (2023-07-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fcae350c427acd83c11596c799ebed311b38e61e

commit fcae350c427acd83c11596c799ebed311b38e61e
Author: Alesandro Ortiz <alesandro@alesandroortiz.com>
Date: Wed Jul 12 17:02:20 2023

[Android]: Webshare: Adjust URL formatting in header.

Use formatUrlForSecurityDisplay() in share dialog.
Fix tests to use same URL formatting method as share dialog code, and
change test input URL to a URL with path, query, and hash components
to ensure these are handled properly (i.e. removed).

(cherry picked from commit 0e8f231c58e749551637f25a1f9fe926f2ad9897)

Bug: 1367085
Change-Id: Ib04d3d8d16588d810c2ea916d218e7e058cf5a56
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4670811
Reviewed-by: Wenyu Fu <wenyufu@chromium.org>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Sophey Dong <sophey@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1168335}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4679174
Auto-Submit: Finnur Thorarinsson <finnur@chromium.org>
Commit-Queue: Wenyu Fu <wenyufu@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#447}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/fcae350c427acd83c11596c799ebed311b38e61e/chrome/browser/share/android/java/src/org/chromium/chrome/browser/share/share_sheet/ShareSheetBottomSheetContent.java
[modify] https://crrev.com/fcae350c427acd83c11596c799ebed311b38e61e/chrome/browser/share/android/javatests/src/org/chromium/chrome/browser/share/share_sheet/ShareSheetBottomSheetContentTest.java


### [Deleted User] (2023-07-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Thank you for the report, Alesandro! The VRP Panel has decided to award you $500 for this report of this URL elision issue as a thank you. Thank you for your efforts in finding and reporting this issue. 

### al...@alesandroortiz.com (2023-07-19)

Thanks for the reward! Was a patch bonus already considered by the VRP Panel?

### al...@alesandroortiz.com (2023-07-19)

(And was a bisect bonus also considered by the VRP Panel?)

### am...@chromium.org (2023-07-19)

Hi Alesandro, while we appreciate the additional information provided in this report, this is fairly trivial issue in terms of security impact with very low security implications, esulting in the thank you reward. Given the obvious introduction of this issue and it being incorrectly resolved, the provided bisect information was not used or necessary for the triage of this issue. 
We did not see the patch provided by you. I do see now that you did commit the patch yourself directly.  
It, however, also appears this patch was based on a strategy discussed and publicly disclosed at the time of this report. So, we'll need to discuss as a panel to make a determination about a potential patch bonus here. Thanks for your patience in the meantime while we discuss. 

### al...@alesandroortiz.com (2023-07-19)

Fair enough, thanks for additional context!

### am...@chromium.org (2023-07-20)

Hi Alesandro -- since you did directly commit the suggested patch yourself directly to Chromium, we did decide to add an additional $500 patch bonus reward here to make your total VRP reward $1000. Thanks for your work in submitting that patch.

### al...@alesandroortiz.com (2023-07-21)

Hi Amy and VRP Panel: Thanks for the patch bonus, appreciate it!

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-18)

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

This issue was migrated from crbug.com/chromium/1367085?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebShare, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/1403571]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061104)*
