# Security: url spoofing using 304 status code

| Field | Value |
|-------|-------|
| **Issue ID** | [40092414](https://issues.chromium.org/issues/40092414) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2018-09-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

By pasting a url in the omnibox that leads to a request with status code 304 (not modified) and then pressing enter, the page doesn't load but the url stays there. Using window.onbeforeunload it is possible to see when the user hits enter. This way one can create a maliciously crafted website that looks like an account login page for example.

**VERSION**  

Chrome Version: 69.0.3497.81 (Official Build) (64-bit) (Stable)  

Operating System: Mac OS 10.13.6

**REPRODUCTION CASE**  

please check dangerous.html  

It is a simple demo that spoofs the httpstat.us domain (I couldn't find many servers that are actually hosting the 304 status code) But something like this can be done with any website that hosts a 304 status code. Any website hosting redirects (301, 302 etc.) is vulnerable as well. <http://bit.ly/totallylegitwebsite> for instance.

I'm not sure how severe this issue is. Other browsers seem to actually load the other domain but as a white page. But if this behaviour is super normal and obvious feel free to let me know.

## Attachments

- [dangerous.html](attachments/dangerous.html) (text/plain, 1.0 KB)

## Timeline

### je...@gmail.com (2018-09-09)

It appears like this behaviour doesn't happen in canary. But I'm not sure if this has intentionally been fixed or if this is a side effect of other changes.

### mp...@google.com (2018-09-10)

Hi, adding Omnibox and navigation experts to the CC list. This may have already been fixed. Thanks for the report!

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### sh...@chromium.org (2018-09-10)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-09-10)

Thanks for the report.  The fact that the user has to type the URL that has a 304 response (e.g., https://httpstat.us/304) is a pretty big mitigating factor (maybe reducing this to Low severity?), but it's true that there is/was a bug here.  We intend to clear the pending URL from the address bar when the 304 response happens.

This was working correctly in M68 (tested on ChromeOS 68.0.3440.118), and I can confirm it's not working correctly on Windows 69.0.3497.81 or 70.0.3538.9.  I ran a bisect and got clamy@'s r574553 (69.0.3491.0) from https://crbug.com/chromium/738177:

----
You are probably looking for a change made after 574552 (known good), but no later than 574553 (first known bad).
CHANGELOG URL:
The script might not always return single CL as suspect as some perf builds might get missing due to failure.
  https://chromium.googlesource.com/chromium/src/+log/efd642e61e6933f8e78a607f02b2478652547e92..d3bfdb09875f6b6cdadd5075d7c1f7305b5118ec
----

On Canary, we see yet another behavior, where an error page is displayed for a 304 response.  I find that unexpected as well, but I wasn't able to bisect to find where it changed.  There might be a field trial affecting it (in which case bisects don't pick up the field trial config).  The network service trial doesn't seem like the one that caused the error page-- that one takes us to a blank page on 304 instead of an error page or staying on the previous page.

The error page does avoid the spoof, but I'm not sure it's intended behavior or not.  If that's a bug that gets fixed, then we want to make sure the spoof doesn't come back.

clamy@, can you help track down what's happening in the current Canary to see why we get an error page, and check why your r574553 changed the 304 behavior in M69?  Thanks!

### sh...@chromium.org (2018-09-24)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2018-09-24)

clamy@: Friendly ping.  It appears the error page has gone away recently, since I don't see it on 71.0.3559.0.  That means we're back to leaving the 304's URL in the omnibox after a browser-initiated navigation to it, which is incorrect.

As noted in https://crbug.com/chromium/882270#c4, I don't see this as Medium since the user has to enter a victim URL that returns as 304 for this to happen, but we should definitely still fix this.  Thanks!

### cl...@chromium.org (2018-09-25)

So I've been looking at the issue on trunk, and I still get the error page. AFAICS, this is due to us misclassifying the httpstat.us/304 as a download, and then deciding that we can't read a download with status 304 so showing an error page. I modified the code so that it doesn't get classified as a download (ie set the value to always be false), and I don't see the URL spoof: the browser-initiated navigation is cancelled, and its URL does not stay in the address bar.

+mmenke for the issue of download misclassification

### sh...@chromium.org (2018-09-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-09-25)

Hrm...I think if you navigate to a page that returns a 304 status code by using the omnibox, ideally we'd display an error page (Or display a blank page) - just ignoring the request in favor of displaying the old page is confusing.

Of course, if you click a link that navigates to a 304 response, we presumably want to abort the navigation.

It does seem a bit weird that we aren't sniffing empty responses as text/html or text/plain - if you navigate to a page, and get a 200 with an empty response body, presumably we want to treat it as HTML.  It looks like we are actually currently downloading 200 responses with empty bodies, which seems like pretty broken behavior.

### mm...@chromium.org (2018-09-25)

Oops...there was a bug in my test server code, so we're not downloading in the 200 case.

### mm...@chromium.org (2018-09-27)

[clamy]:  Are you working on this, or can I take it?  Don't want to steal it if you've already started.

### cl...@chromium.org (2018-09-28)

I'm sheriff for 4 days in a row, so I don't think I'll have much time to investigate.

### mm...@chromium.org (2018-09-28)

Thanks!  I'll take this, then.

### bu...@chromium.org (2018-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4f8104c528f0147c7527718d5aa7c9c38c8220d0

commit 4f8104c528f0147c7527718d5aa7c9c38c8220d0
Author: Matt Menke <mmenke@chromium.org>
Date: Mon Oct 01 23:42:52 2018

Abort navigations on 304 responses.

A recent change (https://chromium-review.googlesource.com/1161479)
accidentally resulted in treating 304 responses as downloads. This CL
treats them as ERR_ABORTED instead. This doesn't exactly match old
behavior, which passed them on to the renderer, which then aborted them.

The new code results in correctly restoring the original URL in the
omnibox, and has a shiny new test to prevent future regressions.

Bug: 882270
Change-Id: Ic73dcce9e9596d43327b13acde03b4ed9bd0c82e
Reviewed-on: https://chromium-review.googlesource.com/1252684
Commit-Queue: Matt Menke <mmenke@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#595641}
[modify] https://crrev.com/4f8104c528f0147c7527718d5aa7c9c38c8220d0/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/4f8104c528f0147c7527718d5aa7c9c38c8220d0/content/browser/loader/navigation_url_loader_impl.cc


### mm...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-08)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-15)

Cheers jespertheend@! The VRP Panel decided to reward $500 for this report. A member of our finance team will be in touch to arrange payment. Also. how would you like to be credited in Chrome release notes?

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### je...@gmail.com (2018-10-15)

Thanks a lot! I'd like to be credited as 'Jesper van den Ende'.

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/882270?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092414)*
