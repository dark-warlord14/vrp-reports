# Address bar spoofing with window.open() + 204 No Content

| Field | Value |
|-------|-------|
| **Issue ID** | [40078012](https://issues.chromium.org/issues/40078012) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Reporter** | ma...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2013-08-29 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36

Steps to reproduce the problem:
1. Go to attached PoC.
2. Click go button.
3. You can see www.google.com in address bar. But it is incorrect.

What is the expected behavior?
Chrome should point URL correctly.

What went wrong?
Chrome points incorrect URL.

Did this work before? N/A 

Chrome version: 29.0.1547.62  Channel: stable
OS Version: 6.2 (Windows 8)
Flash Version: Shockwave Flash 11.8 r800

## Attachments

- deleted (application/octet-stream, 0 B)
- [chrome_204_spoof.html](attachments/chrome_204_spoof.html) (text/plain; charset=us-ascii, 9.4 KB)
- [chromeforandroid_204_spoof.html](attachments/chromeforandroid_204_spoof.html) (text/html; charset=us-ascii, 9.6 KB)

## Timeline

### ma...@gmail.com (2013-08-29)

PoC is here:

### js...@chromium.org (2013-08-29)

It looks like prompts for the previous page are getting fired after we update the omnibox. This may have been introduced after we changed these modal dialogs into constrained dialogs.

@creis - Any thoughts on who I can point at this?

### cr...@chromium.org (2013-08-29)

I'll take a look along with the other spoof bug.  Likely fallout from https://crbug.com/chromium/9682.

### cr...@chromium.org (2013-08-29)

Ah, nice.  We normally detect any access to the initial empty document and report it to the browser process so that we can prevent spoofs like this.  (That was implemented in https://bugs.webkit.org/show_bug.cgi?id=107963.)

However, we do the notification in a one-shot timer, which means it doesn't arrive until after the modal JavaScript dialogs in this attack have been shown to the user under the spoofed URL.

I can block this by calling DidAccessInitialDocument in the browser process if it tries to show a JavaScript dialog, though that may not cover 100% of the ways an attacker could put off the notification.  One alternative would be making the notification without using a timer.  Adam, you argued against that in https://crbug.com/chromium/281256#c18 of https://bugs.webkit.org/show_bug.cgi?id=107963.  Do you think we should stick with the timer and just try to catch cases like this in the browser process?

### in...@chromium.org (2013-09-03)

Fix labels.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### cr...@chromium.org (2013-09-04)

We have a plausible patch in progress here:
https://codereview.chromium.org/23620020/

### bu...@chromium.org (2013-09-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157196

------------------------------------------------------------------------
r157196 | creis@chromium.org | 2013-09-04T05:01:09.562958Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameLoader.cpp?r1=157196&r2=157195&pathrev=157196
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameLoader.h?r1=157196&r2=157195&pathrev=157196
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/WebFrameTest.cpp?r1=157196&r2=157195&pathrev=157196
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/PageGroupLoadDeferrer.cpp?r1=157196&r2=157195&pathrev=157196

Don't wait to notify client of spoof attempt if a modal dialog is created.

BUG=281256
TEST=See bug for repro steps.

Review URL: https://chromiumcodereview.appspot.com/23620020
------------------------------------------------------------------------

### in...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### cr...@chromium.org (2013-09-04)

I'll wait to merge this to M30 and M29 until it bakes on tomorrow's canary for a bit, but it does affect both of those branches.

### cr...@chromium.org (2013-09-09)

Ok, this has been baking since 31.0.1622.0.  It seems to prevent the attack and I don't see any fallout in the crash logs.  I'll plan to merge it to M30 and then M29 if that's ok.

### sc...@gmail.com (2013-09-09)

Just M30 is probably ok, if it limits the work / risk :)

### cr...@chromium.org (2013-09-10)

Ok, I'll stick with that unless I hear otherwise.

### bu...@chromium.org (2013-09-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157486

------------------------------------------------------------------------
r157486 | creis@chromium.org | 2013-09-10T00:07:58.064630Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/page/PageGroupLoadDeferrer.cpp?r1=157486&r2=157485&pathrev=157486
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/FrameLoader.cpp?r1=157486&r2=157485&pathrev=157486
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/FrameLoader.h?r1=157486&r2=157485&pathrev=157486
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/web/tests/WebFrameTest.cpp?r1=157486&r2=157485&pathrev=157486

Merge 157196 "Don't wait to notify client of spoof attempt if a ..."

> Don't wait to notify client of spoof attempt if a modal dialog is created.
> 
> BUG=281256
> TEST=See bug for repro steps.
> 
> Review URL: https://chromiumcodereview.appspot.com/23620020

TBR=creis@chromium.org

Review URL: https://codereview.chromium.org/23710021
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

Nice spoof & repro. $2000

### ma...@gmail.com (2013-10-04)

Latest Chrome for android (30.0.1599.82) still has similar issue.
I attached PoC. This case can spoof without using modal dialog.
Should I report it as new issue?

### cr...@chromium.org (2013-10-04)

Confirmed.  The original repro case appears to work on Android as well (and I expect several other recent spoofs are possible).  It's harder for me to verify, but I suspect that NotifyNavigationStateChanged(content::INVALIDATE_TYPE_URL) is not causing the omnibox to refresh its URL on Android, since that's what we're using in didAccessInitialDocument.

@inferno, I'll reopen this for the time being, but let me know if it's better to file a separate bug for the Android behavior.

### in...@chromium.org (2013-10-04)

we should file a seperate bug, since reward handling, merging, etc will be easier to track.

### cr...@chromium.org (2013-10-04)

Thanks.  Filed https://crbug.com/chromium/304226, which we can attribute to masatokinugawa.

### pa...@chromium.org (2013-10-18)

I just kicked off payment via e-payment system, which can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/281256?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078012)*
