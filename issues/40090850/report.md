# Security: Show javascript alert on a site by clicking on a link from that site

| Field | Value |
|-------|-------|
| **Issue ID** | [40090850](https://issues.chromium.org/issues/40090850) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WindowDialog |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-03-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This exploit abuses the history.replaceState JavaScript function to replace "From example.com" with "From this page" in javascript alert titles, while appearing to come from a page the link to this exploit was clicked from, after which, it will open a new page with a blank url and content of attacker's choice  

This could very easily be used for social engineering

If required, I can attach a screenrecording of a potential attack scenario

**VERSION**  

Chrome Version: 65.0.3325.162 + stable  

Operating System: Windows 8.1

**REPRODUCTION CASE**

1. Upload the included html file to the attacker's server
2. Add a link to the html file on a trusted website
3. Click on the link
4. A javascript alert box will show up, seemingly coming from the trusted website, with a title that says "From this page"
5. After clicking OK on the message, a website of attacker's choice appears, with the url set as "about:blank"

## Attachments

- deleted (application/octet-stream, 0 B)
- [alert_exploit.html](attachments/alert_exploit.html) (text/plain, 272 B)
- [chrome_2018-03-20_07-16-54.png](attachments/chrome_2018-03-20_07-16-54.png) (image/png, 23.6 KB)
- [2018-03-20_07-15-13.gif](attachments/2018-03-20_07-15-13.gif) (image/gif, 76.0 KB)

## Timeline

### re...@gmail.com (2018-03-19)

I uploaded the wrong version of the exploit, please use this one instead

### do...@chromium.org (2018-03-19)

Hmm, this is interesting. +avi and +clamy, can you take a first look at what's going on?

[Monorail components: Blink>WindowDialog]

### es...@chromium.org (2018-03-19)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-03-19)

Can you attach a picture of the time when the dialog is up, what the effect you've created looks like?

### re...@gmail.com (2018-03-20)

I've attached a screenshot and a short gif of it in action

### av...@chromium.org (2018-03-20)

I find it even more troublesome without replaceState, as then the URL that the dialog is attributed to is the old one, not the new one.

### av...@chromium.org (2018-03-20)

[Comment Deleted]

### av...@chromium.org (2018-03-20)

Ignore my last post. Brain fail on my part.

### av...@chromium.org (2018-03-20)

OK. replaceState is used to switch out the URL to something not parseable, so the JS dialogs switch to "this page". Meanwhile, since the dialog is the first thing the page does, it locks up the render process so that it can't provide rendering, and thus the view of the old page remains.

Even if we can't show the new page, how can we at least force the old page to stop showing?

### av...@chromium.org (2018-03-20)

What happens here is that RenderWidgetHostImpl has a TimeoutMonitor named new_content_rendering_timeout_. When a page is committed, in RenderWidgetHostImpl::DidNavigate() the timer starts. If it fires (after kNewContentRenderingDelayMs, or 4s) then the widget realizes that something is wrong and blanks the page.

The problem is that the render process is blocked with the dialog, and there *won't* be a new paint, and the browser *knows* this. Can we make a call on the widget to say "hey, if there's currently a paint timer, expire it immediately"?

### ke...@chromium.org (2018-03-20)

It sounds like the omnibox shows the correct URL for the 'this page' being referred to by the dialog, and there is only 4 seconds of this spoofing behavior. I'm downgrading the severity accordingly.

### bu...@chromium.org (2018-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2ccbb407dccc976ae4bdbaa5ff2f777f4eb0723b

commit 2ccbb407dccc976ae4bdbaa5ff2f777f4eb0723b
Author: Avi Drissman <avi@chromium.org>
Date: Tue Mar 20 21:11:36 2018

Force a flush of drawing to the widget when a dialog is shown.

BUG=823353
TEST=as in bug

Change-Id: I5da777068fc29c5638ef02d50e59d5d7b2729260
Reviewed-on: https://chromium-review.googlesource.com/971661
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#544518}
[modify] https://crrev.com/2ccbb407dccc976ae4bdbaa5ff2f777f4eb0723b/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/2ccbb407dccc976ae4bdbaa5ff2f777f4eb0723b/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/2ccbb407dccc976ae4bdbaa5ff2f777f4eb0723b/content/browser/web_contents/web_contents_impl.cc


### av...@chromium.org (2018-03-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-01)

Thanks for the report! The VRP panel decided to award $1,000 for this report. A member of our finance team will be in touch to arrange for payment.

Also, how would you like to be credited in release notes?

### aw...@google.com (2018-04-01)

[Empty comment from Monorail migration]

### re...@gmail.com (2018-04-02)

Awesome!
I'd like to be credited by my full name, Jasper Rebane

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/823353?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090850)*
