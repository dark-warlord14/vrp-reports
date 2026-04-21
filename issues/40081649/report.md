# Alert popup with no and/or inaccurate origin identification

| Field | Value |
|-------|-------|
| **Issue ID** | [40081649](https://issues.chromium.org/issues/40081649) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox>SecurityIndicators, UI>Browser>PopupBlocker |
| **CVE IDs** | CVE-2016-1615 |
| **Reporter** | ro...@gmail.com |
| **Assignee** | kk...@chromium.org |
| **Created** | 2015-03-18 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. Visit a malicious website http://ronmasas.com/google
2. Click on a link (this link will open a popup)
3. Google.com ask for your password

What is the expected behavior?
When a website use javascript to create alerts using javascript by using one of the following commands:

alert('message');
confirm('message');
prompt('message')

It's usually something like that: " 
           http://website.com
           some message
"

I found a way to remove the "http://website.com" from the alert, by creating a popup to javascript:alert(4); you get an alert with any title you want, I created a POC that demonstrate how you can me someone think google is asking for your password.

POC:http://ronmasas.com/google

What went wrong?
I really don't know, this is the only way I manage to get this to work, for example creating an iframe to javascript:alert(4); will return about:null as the alert popup title.

Did this work before? N/A 

Chrome version: 41.0.2272.89  Channel: stable
OS Version: 8.2
Flash Version: Shockwave Flash 17.0 r0

Test this on my iPhone 6 Plus iOS 8.2 chrome 41.0.2272.56

## Attachments

- [google.html](attachments/google.html) (text/html, 691 B)
- [Screen Shot 2015-05-18 at 9.50.48 AM.png](attachments/Screen Shot 2015-05-18 at 9.50.48 AM.png) (image/png, 22.3 KB)
- [iOS Simulator Screen Shot May 18, 2015, 2.10.18 PM.png](attachments/iOS Simulator Screen Shot May 18, 2015, 2.10.18 PM.png) (image/png, 72.3 KB)
- [2.png](attachments/2.png) (image/png, 41.0 KB)

## Timeline

### js...@chromium.org (2015-03-18)

pinkerton@ - This appears to be iOS specific. Would you mind having someone take a look? I don't have an iOS device to test with, so I don't know what's actually going on. However, as long as it's not possible to get a prompt in front of a page from another origin, or otherwise spoof another origin as the source of a prompt, it wouldn't be a security issue.

### pi...@chromium.org (2015-03-18)

stuart, can you take a look, or find someone to?

### st...@chromium.org (2015-03-18)

For UIWebView there's nothing we can do about the lack of host, since the alert is controlled entirely by UIWebView (but interestingly, on desktop the alert doesn't have an origin either). Similarly, we can't prevent the alert from showing from a background tab, because again UIWebView controls the display of alerts.

I'm not sure what we can really do here. Theoretically we could prevent javascript: popups, but a) desktop doesn't, so there may be legitimate sites out there expecting that functionality, and b) it's probably possible to conduct a version of this attack that uses window.open followed immediately by document.write.


With WKWebView we could control the alert presentation, perhaps waiting to display it until tab switch (although I'm not sure what that would do to JS execution on other tabs), or switching to that tab before showing the popup.

### ke...@chromium.org (2015-03-19)

This looks like a real phishing issue. The password prompt appears in front of a (real) google.com tab, without any origin indicator.

On desktop, the popup is missing an origin indicator but doesn't appear on a navigated page. Also, it is constrained by the popup blocker.

Is there any way to bring the originating tab to the foreground when it launches a popup?

### ke...@chromium.org (2015-03-19)

[Empty comment from Monorail migration]

### st...@chromium.org (2015-03-19)

No, there isn't. The only way we can have knowledge of, or control over, alerts in UIWebView is to replace the method via JS, but a sufficiently clever attacker can prevent us from doing that until after they have saved off the original method.

So we could make this attacker harder to set up, but I don't see any way to prevent it entirely with UIWebView.

### st...@chromium.org (2015-03-19)

I just realized you said popup, not alert. If we make window.open open background tabs instead of foreground tabs, there are going to be a whole lot of very confused users.

### st...@chromium.org (2015-03-27)

I'm going to remove the milestone from this, since I don't see any way to solve the general problem using UIWebView.

However, Eugene, can you make sure we do something reasonable with this case (like, but a domain descriptor of some kind) with WKWebView?

### eu...@chromium.org (2015-03-27)

Kurt worked on WKWebView alerts, reassigning.

### ts...@chromium.org (2015-03-30)

I'm going to put a milestone back, and a reduced priortiy, to ensure this doesn't fall off the radar forever ...

### cl...@chromium.org (2015-04-18)

kkhorimoto@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

Kurt - can you please try to have this fixed by the end of next week so that we can make M44? Let me know if that's not going to happen.

### kk...@chromium.org (2015-05-08)

I have a CL out for review that will use "about:null" as the source host of JavaScript alerts when none is found (https://chromereviews.googleplex.com/196897013/).  Keep in mind, however, that this only fixes the issue for WKWebView since as Stuart explained above, we do not have control over these alerts for UIWebView.

### st...@chromium.org (2015-05-09)

M46 is the earliest possible build I can imagine this shipping in; even that's unlikely, but if we have to put an arbitrary milestone here let's start with that.

### kk...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-05-18)

Could someone with an iOS device add a screenshot of what happens on iOS? I want to make sure we have the right security labels on the bug. Thanks!

This also seems to be a small problem on desktop (see screenshot) but it doesn't sound as convincing as the iOS version. 

### bu...@chromium.org (2015-05-18)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/b43f96e3b8eec2e2e141db46cdc8617fa48e21e5

commit b43f96e3b8eec2e2e141db46cdc8617fa48e21e5
Author: kkhorimoto <kkhorimoto@google.com>
Date: Mon May 18 20:22:49 2015


### kk...@chromium.org (2015-05-18)

Here's a screenshot of the JS prompt shown using the link in https://crbug.com/chromium/468179#c1 on a UIWebView-based Bling.

### kk...@chromium.org (2015-05-19)

I'm resetting the status to "Available", since this bug is still not fixed (nor fixable) on UIWebView.

Also adding vkaruturi@ to verify the fix on WKWebView.

### fe...@chromium.org (2015-05-20)

Desktop prompts are *supposed* to show the origin, and it's a bug that the origin is missing.

Are iOS prompts also supposed to show the origin?

If so maybe at least one fix is to add the origin to the alert.

### kk...@chromium.org (2015-05-20)

There are two default localized strings IDS_JAVASCRIPT_ALERT_DEFAULT_TITLE and IDS_JAVASCRIPT_MESSAGEBOX_DEFAULT_TITLE that are presumably being used on desktop when there is no hostname.  This yields the "Javascript" title on the desktop screenshot above in c#16.

On iOS, the CL in c#17 changes this to use the prompt title with the hostname, using "about:null" as the host when none is available, but only for WKWebView.  For UIWebView, we don't have control over the title used in the prompt, resulting in the screenshot in c#18.

### wf...@chromium.org (2015-05-21)

Can we raise a bug with Apple for them to add an origin to the alert for UIWebView?

### mb...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-05-26)

If we were somehow able to prevent alerts from showing from background tabs, that seems like it would be a better solution. (Using "about:null" still seems confusing, since you see google.com behind the alert.)

Is preventing alerts from the background possible in WKWV?

### st...@chromium.org (2015-05-26)

I'm not sure what would happen if we just sat on the callback until the tab was shown again, given that the JS call is synchronous from the page. We could send back default answers, but that seems undesirable.

Do you know how exactly Desktop handles this, internally? Do they let the JS execution block?

### fe...@chromium.org (2015-05-26)

> Do you know how exactly Desktop handles this, internally? Do they let the JS execution block?

My understanding is that desktop lets the prompt show from the background, but it isn't nearly as convincing w/r/t phishing because it's a little dialog in the middle of a large screen. But maybe we shouldn't show alerts from the background on desktop either.

Adding jochen@ or jww@ who might have more to add.

### pa...@chromium.org (2015-05-26)

There's enough weird things going on here that I don't think we should consider this bug to be specific to Chrome on iOS. Check out this weird screenshot from Linux. The 2 named origins are "https://google.com/" and "" ("Always allow pop-ups from"), yet both should be "about:blank". Of course, I agree with #24.

### pa...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### jo...@chromium.org (2015-05-27)

On desktop, a JS modal dialog will raise the tab that requested it, and block all of chrome.

On android, JS modal dialogs are horribly broken.

### st...@chromium.org (2015-05-27)

For iOS, we should be able to raise the tab (in WKWebView only).

Kurt, could you implement that as well? (Also, per https://crbug.com/chromium/468179#c22, please file a Radar about the UIWebView missing host issue.)

palmer@, could we split the other-platform parts into a new bug? Most of this bug is about iOS, and both the issues and solutions on iOS are distinct, even if related.

### ti...@google.com (2015-06-15)

@kkhorimoto - what's the timeline for implementing a fix for iOS?

@palmer - can you please address Stuart's question in #30?

### pi...@chromium.org (2015-06-15)

The earliest we could have a fix for WKWebView (only) is M46, though we're not 100% confident at this point we can ship a product based on it. Just keep that in mind. 

### st...@chromium.org (2015-06-15)

[Comment Deleted]

### pa...@chromium.org (2015-06-18)

#31: Sure, I think it would be fine to break this out into a new bug.

### cl...@chromium.org (2015-07-10)

kkhorimoto@: Uh oh! This issue is still open and hasn't been updated in the last 24 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### st...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-21)

kkhorimoto@: Uh oh! This issue is still open and hasn't been updated in the last 41 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### st...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-23)

What's the latest here? We are now in the M48 timeline and want to make sure that someone is still invested in fixing this bug. Thanks!

### st...@chromium.org (2015-09-23)

There's still lots of blocking work to do before we could ship WKWebView, which is a precondition to being able to fix this.

### ji...@chromium.org (2015-11-12)

stuartmorgan@, could you link the blocking bug(s) to this one?

### kk...@chromium.org (2015-11-12)

This is blocked on shipping Chrome with WKWebView on iOS, which is slated for M48 or M49, depending on the metrics we receive for our staged roll-out experiment in M47.

### st...@chromium.org (2015-11-12)

To clarify slightly: the rollout of a fix is blocked on that, but the work to fix the bug in WKWebView mode can and should happen now.

### bu...@chromium.org (2015-12-10)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/80cd68a53b1cb0cfc6644993ccf0ff63f4eba968

commit 80cd68a53b1cb0cfc6644993ccf0ff63f4eba968
Author: kkhorimoto <kkhorimoto@google.com>
Date: Thu Dec 10 23:37:57 2015


### kk...@chromium.org (2015-12-10)

The CL in c#44 fixes this issue for WKWebView.  I'm going to mark this as fixed, as this will no longer occur once WKWebView is released (M48).

### cl...@chromium.org (2015-12-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### kk...@chromium.org (2015-12-11)

The merge status is being tracked in https://crbug.com/chromium/526727, as this CL fixed multiple bugs and I didn't want to request in multiple places.

### bu...@chromium.org (2015-12-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/f828c8c511600ad37052f3f60ee7ba091e6019da

commit f828c8c511600ad37052f3f60ee7ba091e6019da
Author: kkhorimoto <kkhorimoto@google.com>
Date: Thu Dec 10 23:37:57 2015


### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

Hi Ron - our reward panel reviewed this issue and decided to award you $500 for bringing this issue to our attention. Congrats!

We'll list your name in the Chrome release notes as "Ron Masas". If you'd like me to update it to another name, please let me know.

Someone from our finance team should be in touch within 7 days to collect some details for payment. Please let me know if that doesn't happen by updating the bug or reaching out to me at timwillis@

I'll update this bug shortly with a CVE ID for your records. Thanks again for helping secure chrome and happy bug hunting!

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1615

### ro...@gmail.com (2016-01-31)

Hi, thank you for the award, "Ron Masas" is fine.
No one from the finance team contacted me yet, please let me know what should I do.

Thanks,
Ron

### ti...@google.com (2016-02-02)

#53: I've chased up - they should be in contact within 24 hours. Please let me know if that doesn't happen.

### sh...@chromium.org (2016-03-18)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### lg...@chromium.org (2017-04-18)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>PageActionBox UI>Browser>Omnibox>SecurityIndicators]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/468179?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox>SecurityIndicators, UI>Browser>PopupBlocker]
[Monorail blocked-on: crbug.com/chromium/423444]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081649)*
