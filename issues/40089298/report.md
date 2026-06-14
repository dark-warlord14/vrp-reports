# Security: Permission request UI spoof (improper URL truncation)

| Field | Value |
|-------|-------|
| **Issue ID** | [40089298](https://issues.chromium.org/issues/40089298) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Mac, Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2017-10-13 |
| **Bounty** | $500.00 |

## Description

VERSION
Chrome Version: 61.0.3163.100/62.0.3202.52
Operating System: windows

Details
spoof the origin to '*.google.com'
when the html page request camera or other permission

Online Demo
https://www.math1as.com/chrome/camera_spoof.html
https://www.math1as.com/chrome/location_spoof.html



## Attachments

- [camera.jpg](attachments/camera.jpg) (image/jpeg, 17.0 KB)
- [location.png](attachments/location.png) (image/png, 5.8 KB)
- [Screenshot from 2017-11-14 14:22:10.png](attachments/Screenshot from 2017-11-14 14_22_10.png) (image/png, 90.0 KB)
- [Screenshot from 2017-11-14 15:52:29.png](attachments/Screenshot from 2017-11-14 15_52_29.png) (image/png, 72.3 KB)

## Timeline

### el...@chromium.org (2017-10-13)

We're showing the hostname of the URL from the left (truncating it before the end). If we must truncate, we need to elide from the left.

[Monorail components: UI>Browser>Permissions>Prompts UI>Security>UrlFormatting]

### es...@chromium.org (2017-10-13)

Over to raymes for permissions triage.

Marked as low severity because we think most users probably look at the omnibox rather than the origin in the permission prompt (which is also why we are getting rid of subframe permissions prompts that show the subframe origin).

### sh...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-11-14)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-11-14)

+mgiuca, lgarron, estark for thoughts on my fix.

I have a WIP CL for this that elides the entire title of the permission bubble from the head (i.e. left in LTR languages). This ensures that the most important part of the URL remains if the URL is too long to fit.

Anything more complex than operating on the entire title is somewhat complicated due to the way views/ works. My understanding is that bubbles don't actually know how wide they will be, but the width is a necessary piece of information to elide the URL.

There's also an issue if the translated title ends up being something like "wants to URL" or "wants URL to" - the "wants" will be elided if the URL is too long, so the title may be a bit weird. To me though, locking down the spoof and trying to address potential string strangeness is the right priority. Also, if really long URL cases are mostly malicious anyway, having the right part of the URL displayed and not the ancillary text also seems like the right priority

Attached are before and after representations of a too long URL.

### mg...@chromium.org (2017-11-14)

I discussed this with Dom and I'm OK with it from a security perspective. Doing anything better is hard. Clarifying a few things Dom said:

1. "if the translated title ends up being something like "wants to URL" or "wants URL to"" --- he means when translated into another UI language. For example, the Filipino (LANGUAGE=fil) string is "Gusto ng $ORIGIN na", which if the URL is very long will appear as "…$TRUNCATED_ORIGIN na". That's likely meaningless, but at least you'll still see the most significant part of the origin, and the list of permissions.

2. RTL origins are a consideration here, but fortunately should be correctly handled. Per https://crbug.com/chromium/650760, any RTL domain labels will be rendered as punycode for the time being (by FormatUrlForSecurityDisplay), which is actually kind of bad because the user has no idea what domain is asking for permission, but orthogonal to this issue. If we fixed https://crbug.com/chromium/650760, this would still render correctly by chopping off the START of the string (not the LEFT of the string), so we'll still see the most significant domain labels.

LGTM

### do...@chromium.org (2017-11-15)

+cc mcgreevy who is thinking about a similar case for desktop PWA installation.

### do...@chromium.org (2017-11-15)

estark/lgarron: WIP CL is at https://chromium-review.googlesource.com/c/chromium/src/+/768312. It has approval to land; but I'd like one of you to confirm that what we've done here is okay as well. :)

### bu...@chromium.org (2017-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/56762260ca8ef62578fa4718b7d47711f7e120dc

commit 56762260ca8ef62578fa4718b7d47711f7e120dc
Author: Dominick Ng <dominickn@chromium.org>
Date: Thu Nov 16 00:44:57 2017

Elide the permission bubble title from the head of the string.

Long URLs can be used to spoof other origins in the permission bubble
title. This CL customises the title to be elided from the head, which
ensures that the maximal amount of the URL host is displayed in the case
where the URL is too long and causes the string to overflow.

Implementing the ellision means that the title cannot be multiline
(where elision is not well supported). Note that in English, the
window title is a string "$ORIGIN wants to", so the non-origin
component will not be elided. In other languages, the non-origin
component may appear fully or partly before the origin (e.g. in
Filipino, "Gusto ng $ORIGIN na"), so it may be elided there if the
URL is sufficiently long. This is not optimal, but the URLs that are
sufficiently long to trigger the elision are probably malicious, and
displaying the most relevant component of the URL is most important
for security purposes.

BUG=774438

Change-Id: I75c2364b10bf69bf337c7f4970481bf1809f6aae
Reviewed-on: https://chromium-review.googlesource.com/768312
Reviewed-by: Ben Wells <benwells@chromium.org>
Reviewed-by: Lucas Garron <lgarron@chromium.org>
Reviewed-by: Matt Giuca <mgiuca@chromium.org>
Commit-Queue: Dominick Ng <dominickn@chromium.org>
Cr-Commit-Position: refs/heads/master@{#516921}
[modify] https://crrev.com/56762260ca8ef62578fa4718b7d47711f7e120dc/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc


### do...@chromium.org (2017-11-16)

c#10 landed in 64.0.3270.0 and should mitigate this spoofing vector. Closing as Fixed.

### sh...@chromium.org (2017-11-17)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Nice one! The Chrome VRP panel decided to award $500 for this - thanks for the report!

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### do...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/774438?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Permissions>Prompts, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/806708]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089298)*
