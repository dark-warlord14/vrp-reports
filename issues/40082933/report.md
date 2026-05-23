# Chrome mobile for iOS thinks JavaScript redirects are a form of certificate spoofing of trusted domains

| Field | Value |
|-------|-------|
| **Issue ID** | [40082933](https://issues.chromium.org/issues/40082933) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL, UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2015-09-28 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
Opening this link on iOS with Chrome (latest stable) results in spoofing error of google.com

https://www.google.com/url?rct=j&sa=t&url=https://lbr.rand.org/content/dam/rand/pubs/reports/2006/R3113.1.pdf&ct=ga&cd=CAEYACoTNjIzMDg5NjczNDA0NDY0MDUxNTIaYWFjZGMzYjNiN2JlY2JiYzpjb206ZW46VVM&usg=AFQjCNHKAomHqBOlSAw9tTxJx8YIF2lmxA

Opening the same link on Chrome for Linux (latest stable) produces a certificate spoofing error as well, but for a rand.org subdomain.

This behavior could be a UI / security spoofing issue. Additionally, it should be consistent across platforms. Right now, something is wrong and it could speak to a larger issue that is a security bug in the Chrome base core logic.

$ curl -s 'https://www.google.com/url?rct=j&sa=t&url=https://lbr.rand.org/content/dam/rand/pubs/reports/2006/R3113.1.pdf&ct=ga&cd=CAEYACoTNjIzMDg5NjczNDA0NDY0MDUxNTIaYWFjZGMzYjNiN2JlY2JiYzpjb206ZW46VVM&usg=AFQjCNHKAomHqBOlSAw9tTxJx8YIF2lmxA'
<script>window.googleJavaScriptRedirect=1</script><script>var m={navigateTo:function(b,a,d){if(b!=a&&b.google){if(b.google.r){b.google.r=0;b.location.href=d;a.location.replace("about:blank");}}else{a.location.replace(d);}}};m.navigateTo(window.parent,window,"https://lbr.rand.org/content/dam/rand/pubs/reports/2006/R3113.1.pdf");
</script><noscript><META http-equiv="refresh" content="0;URL='https://lbr.rand.org/content/dam/rand/pubs/reports/2006/R3113.1.pdf'"></noscript>

What is the expected behavior?
The page should redirect properly without certificate spoofing.

What went wrong?
Certificate spoofing error was encountered for google.com

Did this work before? No 

Chrome version:   Channel: stable
OS Version: 
Flash Version: 

Interested in your perspective on this. Definitely odd behavior.

## Attachments

- [IMG_0106.PNG](attachments/IMG_0106.PNG) (image/png, 82.7 KB)
- [image1.PNG](attachments/image1.PNG) (image/png, 71.8 KB)

## Timeline

### es...@chromium.org (2015-09-29)

I'm able to reproduce this. It seems like somehow Chrome is using the current navigation entry URL for the interstitial during a redirect to the url in the query parameter. As a result, a user might click through a certificate error on google.com when they are in fact allowing the exception for lbr.rand.org.

droger, do you think you could take a look or help triage?

Tentatively assigning this Medium and M46.

### cl...@chromium.org (2015-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-19)

droger@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### kr...@gmail.com (2015-10-19)

I have not seen a fit yet. Let me know what milestone the fix is planned for so I can test then to confirm, but my fear is that the underlying issue here is a deep logic flaw in a chromium subsystem that may affect certificate handling issues in various ways and may be tough to understand or fix without breaking other components, which also means it might be abused by bad guys to that end.

### pa...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### dr...@chromium.org (2015-10-20)

It's likely that this is because our way to detect navigations is unreliable.
If so, I don't think this is new, and the fix is probably not trivial (if possible at all).

I think the first step would be to check if this bug reproes with WKWebView.

### kr...@gmail.com (2015-10-20)

Let's be clear. This issue ha been solved in chrome desktop and possibly also chrome android. So someone needs to investigate what the difference in code is between the platforms. If this isn't solved, sounds like I can make some good money weaponizing a useful version of this security bug ;)

### st...@chromium.org (2015-10-20)

> someone needs to investigate what the difference in code is between the platforms

The difference is that Chrome on iOS is constrained to use the OS-provided web view, rather than Blink, so roughly speaking the difference at this layer is "almost everything".

### st...@chromium.org (2015-10-20)

This does indeed work correctly in WKWebView (where we have correct redirect information).

### kr...@gmail.com (2015-10-20)

Right. If I follow the same link in Safari on iOS I have no issues. 

### st...@chromium.org (2015-10-20)

https://crbug.com/chromium/536701#c15 refers to Chrome using WKWebView, not to Safari.

### cl...@chromium.org (2015-11-10)

droger@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-11-13)

[Empty comment from Monorail migration]

### st...@chromium.org (2015-11-19)

Bulk-moving M47 iOS bugs to M48. Please evaluate whether this bug is realistically something that should be fixed for M48, given that M48 has now branched.

### pa...@chromium.org (2015-11-25)

On Chrome 47 Beta with WKWebView, I get the attached when visiting the URL

https://www.google.com/url?rct=j&sa=t&url=https://lbr.rand.org/content/dam/rand/pubs/reports/2006/R3113.1.pdf&ct=ga&cd=CAEYACoTNjIzMDg5NjczNDA0NDY0MDUxNTIaYWFjZGMzYjNiN2JlY2JiYzpjb206ZW46VVM&usg=AFQjCNHKAomHqBOlSAw9tTxJx8YIF2lmxA

. It looks like WKWebView fixes the issue. Does that make this bug obsolete?

### st...@chromium.org (2015-11-25)

Right, see https://crbug.com/chromium/536701#c15.

Generally speaking we are leaving bugs fixed by a switch to WKWebView open for now, and tracking them with a hotlist.

### st...@chromium.org (2015-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-17)

droger@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-07)

droger@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### st...@chromium.org (2016-01-27)

Closing, as this is fixed in M48 by the switch to WKWebView (https://crbug.com/chromium/423444)

### cl...@chromium.org (2016-01-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### st...@chromium.org (2016-01-27)

No additional merge necessary; fixed on M48 and M49 branches already

### ti...@google.com (2016-02-03)

Adding this for panel reward consideration, even though this was fixed by the switch to WKWebView. Full details here: https://www.google.com/about/appsecurity/chrome-rewards/

### kr...@gmail.com (2016-02-03)

Thank you for considering my bug report for a Google Chrome security reward :)
--
Kristian Erik Hermansen
https://www.linkedin.com/in/kristianhermansen

### ti...@google.com (2016-02-24)

Marking as Release-NA as a fix isn't shipping for this bug as it was made obsolete by the WKWebView switch.

### ev...@google.com (2016-03-16)

[Empty comment from Monorail migration]

### kr...@gmail.com (2016-03-16)

Thanks! I am no longer able to access this security
bug in Chrome I reported below (it is restricted now). But there was a
mention of a potential reward, which I would donate. Was this resolved
and closed? Any reward? Thanks

### me...@chromium.org (2016-03-16)

@kristian.hermansen: Do you mean you can access https://crbug.com/536701? That shouldn't be the case since you are the reporter of the bug.

### me...@chromium.org (2016-03-16)

^ Should read "Do you mean you CAN'T access ..."

### kr...@gmail.com (2016-03-16)

Got in now. I got some error about Monorail-Prod before. Thank you much whatever got changed.

### sh...@chromium.org (2016-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2016-05-06)

Adding google view restriction. Please remove if this wasn't appropriate. See https://crbug.com/chromium/609744 for reference.

### ma...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

### kr...@gmail.com (2016-05-06)

Please provide me view access to 609744. I have still not received a Chromium reward or any update on status of reward for reporting this security issue. It seems like 609744 builds on my prior finding to become critical severity and remotely exploitable?

### da...@chromium.org (2016-05-06)

(Nah, just some bug management confusion. Nothing to do with this issue.)

### ti...@google.com (2016-06-30)

Hi Kristian,

Our reward panel reviewed this issue and decided to award you $500 for your efforts here. Congratulations!

Our finance team should be in touch within 7 days. If that doesn't happen, please contact me directly at timwillis@

Thanks again for taking the time to report this issue.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-11)

Hello Kristian!  Thanks for opting to donate this reward. I've doubled it to $1,000 and made the payment to the charity you nominated.  Cheers!

### aw...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-12-09)

This issue was migrated from crbug.com/chromium/536701?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>SSL, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082933)*
