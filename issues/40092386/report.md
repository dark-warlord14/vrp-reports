# Security: URL Spoofing via Bidirectional Domain Names

| Field | Value |
|-------|-------|
| **Issue ID** | [40092386](https://issues.chromium.org/issues/40092386) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2018-09-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Chrome for Android, bidirectional domain names with RTL characters are not handled correctly in the omnibox and can lead to URL spoofing attacks.

**VERSION**  

Chrome Version: 69.0.3497.76  

Operating System: Android 8.0.0

**REPRODUCTION CASE**  

Visit the following URL using Chrome on Android:  

<http://example.com.xn--mgbh0fb.xn--mgberp4a5d4ar//////////////////////////%D9%AB> (shortened: <http://bit.do/spoofurl>)

The omnibox displays the subdomain "example.com" on the left while the RTL top level domain name is scrolled out of view to the right (see the attached screenshot).

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 35.8 KB)
- [bidispoof.png](attachments/bidispoof.png) (image/png, 13.6 KB)
- [photo5307609718862227936.jpg](attachments/photo5307609718862227936.jpg) (image/jpeg, 36.4 KB)
- [screenshot.jpg](attachments/screenshot.jpg) (image/jpeg, 32.2 KB)

## Timeline

### 0x...@gmail.com (2018-09-07)

Can't edit the title, please set to "URL Spoofing via Bidirectional Domain Names". Also, Chrome 68 for iOS seems to be affected as well.

### mp...@google.com (2018-09-07)

Thanks for the report! Assigning medium severity as it doesn't look extremely convincing.

[Monorail components: UI>Browser>Omnibox]

### sh...@chromium.org (2018-09-07)

[Empty comment from Monorail migration]

### mp...@chromium.org (2018-09-07)

thildebr@ and tedchoc@, I know you two have worked on positioning of text in the omnibox, sometime in RTL contexts.  Can one of you please take the lead on this issue?

-creis@, as this isn't his area

### 0x...@gmail.com (2018-09-16)

I think this spoof can become much more convincing with a URL like this:
https://www.google.com.xn--mgbh0fb.xn--mgberp4a5d4ar/%D9%A0 (shortened: http://bit.do/bidispoof)

### kr...@chromium.org (2018-09-17)

I'm not sure what this has to do with bi-directional names. Isn't it the same as "google.com............baddomain.com" ?

### 0x...@gmail.com (2018-09-17)

Re #6: Not really, URL segments are not shown in the right order when bidirectional domain names are used and the pathname includes one or more weak characters (e.g., %D9%A0). On top of that, the RTL domain name is also displayed out of view. So instead of "google.com.domain.tld/%D9%A0", it's displayed as "google.com.%D9%A0/domain.tld" with "domain.tld" entirely out of view.

### kr...@chromium.org (2018-09-17)

Ah, I misunderstood what was what in the URL. mgiuca, wasn't your proposal to not swap beyond slashes?


### mg...@chromium.org (2018-09-18)

Analysis:

ASCII URL: http://example.com.xn--mgbh0fb.xn--mgberp4a5d4ar//////////////////////////%D9%AB
  Hostname: example.com.xn--mgbh0fb.xn--mgberp4a5d4ar
  TLD: xn--mgberp4a5d4ar
  SLD: xn--mgbh0fb.xn--mgberp4a5d4ar
  Path: //////////////////////////%D9%AB

Unicode URL: example.com.مثال.السعودية//////////////////////////٫
  Hostname: example.com.مثال.السعودية
  TLD: السعودية
  SLD: مثال.السعودية
  Path: //////////////////////////٫

The fact that you can inject part of the path into the middle of the domain is well known (https://crbug.com/chromium/351639). I have the solution implemented behind the flag chrome://flags/#left-to-right-urls. #8: My proposal on https://crbug.com/chromium/351639 is to bidi-isolate each component of the URL (where components are delimited by any syntactic characters like '.', '/', '?', etc). Thus, this URL would display as:

‪example‬.‪com‬.‪مثال‬.‪السعودية‬//////////////////////////‪٫‬

However, I am confused as to why the view isn't automatically scrolling to include the Arabic part of the domain. I thought we scroll the view such that the LAST part of the domain is always visible in the Omnibox. In this case, the TLD is السعودية. I think it should be scrolled such that "مثال.السعودية" (the top- and second-level domain labels) is visible in the Omnibox.

Leaving this open and unduped because I think we could do better scrolling. Fixing https://crbug.com/chromium/351639 requires more time investment than I have (possibly ever) because of the need to debate in standards.

### mp...@chromium.org (2018-09-18)

>>>
However, I am confused as to why the view isn't automatically scrolling to include the Arabic part of the domain. I thought we scroll the view such that the LAST part of the domain is always visible in the Omnibox.
>>>
FYI, longstanding https://crbug.com/chromium/527638 tracks the fact that the omnibox doesn't scroll to the right side of the domain name (in LTR languages).

### mg...@chromium.org (2018-09-19)

Right, but that's a) on Desktop, not mobile (I believe we *do* have code to scroll to the right on mobile since it's much more likely for the origin not to fit in the box when left-aligned), and b) not specific to RTL origins (which I believe we fixed already on Desktop).

So leaving this open.

### sh...@chromium.org (2018-09-21)

thildebr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-10-01)

I'm not at all familiar with how the text is rendered in the omnibox, so I'm unsure as to why it looks different when displayed vs. what we're basing our scroll offset on.

We don't scroll to the appropriate portion of the URL on Android because we're basing our offset on example.com.مثال.السعودية/////////////////////////// instead of example.com.مثال.السعودية///////////////////////////٫. That final ٫ character completely changes the way the string is displayed, and I'm not even close to an expert on why.

Is this the sort of thing that the fix from #9 is supposed to tackle? Is there anybody with more expertise on RTL/bidi text than me that can take this one?

### te...@chromium.org (2018-10-02)

I actually wonder if this is the line that causes it to break:
https://chromium.googlesource.com/chromium/src/+/e87c0946c520dfe7a904b58137be27710cacd588/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBar.java#701

In this particular case, we compare the end of the domain and the beginning of the domain to determine RTL-ness.  The problem is the beginning of the domain is LTR and only the trailing part if RTL.  I wonder if the "fix" is to just do getLayout().getPrimaryHorizontal(mOriginEndIndex - 1).  Then RTL is determined by the last two characters of the domain.

I can take a look tomorrow to see how horribly that breaks.

### te...@chromium.org (2018-10-02)

I think it will work.  Will try to send out a CL today.

### bu...@chromium.org (2018-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/18c10ae06ccb39b4ff6edc4c40f11127239c4f63

commit 18c10ae06ccb39b4ff6edc4c40f11127239c4f63
Author: Ted Choc <tedchoc@chromium.org>
Date: Tue Oct 02 23:16:01 2018

Fix scroll positioning logic for BiDirection omnibox text.

BUG=881659

Change-Id: Ib1ad439d73b7951603a35fb9760d9cec943f0acd
Reviewed-on: https://chromium-review.googlesource.com/c/1257666
Commit-Queue: Ted Choc <tedchoc@chromium.org>
Reviewed-by: Theresa <twellington@chromium.org>
Reviewed-by: Troy Hildebrandt <thildebr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#596036}
[modify] https://crrev.com/18c10ae06ccb39b4ff6edc4c40f11127239c4f63/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBar.java


### te...@chromium.org (2018-10-02)

This should be fixed in today's or tomorrow's canary.  It will roll out with 71 (would be very hesitant to pull it back as scroll positioning is gnarly).

### te...@chromium.org (2018-10-02)

Actually...probably should be punted to the iOS team to address this on iOS too (+stkhapugin)

### st...@chromium.org (2018-10-03)

I think this looks OK as is on iOS (see screenshot). WDYT? 

### 0x...@gmail.com (2018-10-03)

Re #20: FWIW, a click/touch on the omnibox will cause the URL to be displayed like in the screenshot below.

Unrelated question: I wonder if this issue could possibly be nominated for the Chrome Reward Program (https://www.google.com/about/appsecurity/chrome-rewards/index.html)?


### me...@chromium.org (2018-10-04)

stkhapugin: Assigning to you per https://crbug.com/chromium/881659#c19.

### st...@chromium.org (2018-10-04)

It is expected behaviour for iOS edit view to have the URL left-aligned. In defocused state, as you can see, we're handling this correctly, but we also need the user to be able to actually edit their URL in a natural way. 

### sh...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-15)

Nice one 0xsobky@! The VRP Panel decided to reward $2,000 for this report. A member of our finance team will be in touch to arrange payment. Also. how would you like to be credited in Chrome release notes?

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2018-10-25)

Re #23: You are right. Note, however, that if the "UI Refresh Location Bar" flag (chrome://flags/#ui-refresh-location-bar) gets disabled, this spoof would still be possible (future changes to the defocused state might affect this too).

Re #28: For the release notes, "Ahmed Elsobky (@0xsobky)" would be fine; thanks!

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2018-10-26)

Removing the spurious merge request bits.  The CL is already in 71 (71.0.3570.0).

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/881659?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092386)*
