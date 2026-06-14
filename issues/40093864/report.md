# Security: URL bar spoofing on iOS (repro issue 844881)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093864](https://issues.chromium.org/issues/40093864) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>PageLoad, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2019-01-26 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 72.0.3626.73  

Operating System: iOS 12.1.2

Similar to <https://crbug.com/chromium/844881>

1. Lunch the test case
2. Click Login Twitter
3. Spoof

## Attachments

- [test case.html](attachments/test case.html) (text/plain, 396 B)
- [E18AF79B-0805-4B29-BF8A-D8FA96F0728E.MOV](attachments/E18AF79B-0805-4B29-BF8A-D8FA96F0728E.MOV) (video/quicktime, 277.2 KB)
- [97D55D74-2BA9-4797-8FBA-EECDF4827376.MOV](attachments/97D55D74-2BA9-4797-8FBA-EECDF4827376.MOV) (video/quicktime, 2.7 MB)

## Timeline

### ch...@gmail.com (2019-01-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-01-26)

PoC: https://lbstyle.github.io

### li...@chromium.org (2019-01-27)

It looks like on Mac desktop this will actually redirect to Twitter but fail to connect and then land on the site on which you've called window.location.replace. On iOS it looks like there might be a mitigating factor for when the Twitter app is installed, which causes the script to open the Twitter app instead and then viewing the page in Chrome will show about:blank instead of spoofing. So I'll set the severity to medium.

Adding kenrb@ who worked on https://crbug.com/chromium/844881. Are you able to take a look and see why this is happening on iOS or find someone who might be able to point us to a fix? Thanks!

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### ch...@gmail.com (2019-01-27)

I'm able to repro with any website, in this PoC https://lbstyle.github.io I updated Twitter.com to Amazon.com.

### sh...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-01-30)

this doesn't repro on macOS. 

### ke...@chromium.org (2019-02-04)

https://crbug.com/chromium/844881 and similar bugs are about the content layer and when it signals the UI to update the URL vs when it updates the displayed web page. Since iOS doesn't have the content layer this is not related.

Punting to some Bling people -- stkhapugin@ can you PTAL?

### st...@chromium.org (2019-02-04)

Eugene, do you know what is happening here? Looks like the actual display URL from the webstate is wrong. 

[Monorail components: Mobile>iOSWeb>PageLoad]

### eu...@chromium.org (2019-02-04)

Srikanth, could you please check if the bug is reproducible with slim-navigation-manager?

### ch...@gmail.com (2019-02-04)

[Empty comment from Monorail migration]

### sr...@chromium.org (2019-02-04)

Re#9 Yes.

### ch...@gmail.com (2019-02-06)

Is this still repro on Canary? 

### eu...@chromium.org (2019-02-14)

Gauthier, this would be a good bug to look if you want to understand how Omnibox URL is provided by ios/web. The fact that the bug is reproducible with slim navigation manager makes me think that the bug is in WKWebView and WKWebView.backforwardList.currentItem.URL is incorrect.

### sh...@chromium.org (2019-02-15)

gambard: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2019-02-15)

Looking into this, it seems that we are getting out of sync with the URL provided by the WebView (i.e. WKWebView.URL is google.com, WebState's GetVisibleURL() is amazon.com).

### eu...@chromium.org (2019-02-15)

Gauthier if you feel like you stuck on this bug, feel free to flip back to me or schedule a VC and we can debug together.

### ga...@chromium.org (2019-02-20)

What happen is:
- The first document containing "this is no amazon" is loaded
- The page is redirected to amazon.com
- The URL of the WKWebView becomes amazon.com
- The navigation get committed, the URL displayed by Chrome becomes amazon.com, but the comment is sometimes the first page.
- The page is redirected to google.com:1234.
- The URL of the WKWebView becomes google.com, but the page isn't committed so the Chrome URL doesn't change.

Safari behavior is:
- Load the first document
- Load amazon.com and change the URL to amazon.com
- Actually load part of amazon.com
- Change the URL to google.com and try to load it
- The page becomes white

Test WK app
Same as Chrome, even if I don't answer to any of the delegate calls.

In my opinion, a good way to mitigate this would be to clear the page when getting a redirect to a new page while loading a page. With that, when the page redirects from amazon.com to google.com, the page would become empty.

I guess it is worth filing a radar.

### ga...@chromium.org (2019-02-21)

I have filed rdar://48275722

### eu...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### ga...@chromium.org (2019-02-27)

This bug is actually showing a bug in our code: the progress bar should be displayed. I will fix this bug in our code. Then I am not sure if we need to mitigate this further as it is very hard to reproduce.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b40348af225a6c6bbbc85317437a315df6554f76

commit b40348af225a6c6bbbc85317437a315df6554f76
Author: Gauthier Ambard <gambard@chromium.org>
Date: Wed Feb 27 13:01:11 2019

[iOS] Fix progress bar visibility

This CL fixes the progress bar visibility, which could be fooled when
the state was changing too quickly. For example, if the loading state
was changing during the hide animation, the progress bar wasn't shown
again.

Bug: 925598
Change-Id: Ief9d7cff09724467b244fa1aadecc7a41f7ac0ec
Reviewed-on: https://chromium-review.googlesource.com/c/1489238
Reviewed-by: Justin Cohen <justincohen@chromium.org>
Commit-Queue: Gauthier Ambard <gambard@chromium.org>
Cr-Commit-Position: refs/heads/master@{#635981}
[modify] https://crrev.com/b40348af225a6c6bbbc85317437a315df6554f76/ios/chrome/browser/ui/toolbar/adaptive_toolbar_view_controller.mm


### ch...@gmail.com (2019-03-01)

Fixed on Canary?

### ga...@chromium.org (2019-03-01)

This is mitigated on Canary: now the progress is shown, indicating that some website is loading.
The main issue comes from WKWebView. The behavior is different on Safari, I don't know what they are doing differently. We can try to find a workaround.
livvielin@, as you added the security label to this bug, what should be the next steps? I am not sure to be able to evaluate the severity of this bug.

### li...@chromium.org (2019-03-01)

Since the issue has been mitigated, we may just be able to close this bug. Then, I'd recommend filing a bug with WKWebView with this bug referenced for context and that one can be triaged separately. Does this sound ok?

### ga...@chromium.org (2019-03-05)

Thanks, I have filed https://crbug.com/chromium/938221.

### sh...@chromium.org (2019-03-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $2,000 for this report :) 

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: Less than 27 days to go before AppStore submit on M74
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@google.com (2019-03-26)

gambard: There's nothing to merge here correct? c21 is already in M74. Please remove request label if I'm right.

### ga...@chromium.org (2019-03-26)

Actually it seems that c21 is in M75.
We need to merge it if we want it in M74.

### ga...@chromium.org (2019-03-26)

nvm, it should be in M74, I misread the dates.

### aw...@google.com (2019-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/925598?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>iOSWeb>PageLoad, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093864)*
