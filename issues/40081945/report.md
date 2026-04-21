# Security: Boundless Tunes - universal SOP bypass through ActionSctipt's Sound object

| Field | Value |
|-------|-------|
| **Issue ID** | [40081945](https://issues.chromium.org/issues/40081945) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | oj...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-04-27 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

An instance of ActionScript's Sound class allows for loading and extracting for further processing any kind of external data, not only sound files. Same-origin policy doesn't apply here. Each input byte of raw data, loaded previously from given URL, is encoded by an unspecified function to the same 8 successive sample blocks of output. The sample block consists of 8 bytes (first 4 bytes for left channel and next 4 bytes for right channel). Only 2 bytes from 8 sound blocks (64 bytes) are crucial, the rest 52 bytes are useless. Each byte of input from range 0-255 has corresponding constant unsigned integer value (a result of encoding), so for decoding purposes you can use simply lookup table (cf. source code from BoundlessTunes.as).

**VERSION**  

Chrome Version: 42.0.2311.90, 64-bit, stable  

Operating System: Linux (Debian), 7.0, kernel 3.18.0

Chrome Version: 42.0.2311.90 m, 64-bit, stable  

Operating System: Windows 7 Home Premium, Service Pack 1

**REPRODUCTION CASE**

1. Put attached file BoundlessTunes.swf on the HTTP server.
2. Open http://<SERVER\_HOSTNAME>/BoundlessTunes.swf?url=<URL>, where <URL> is an URL address (e.g. leading to cross-origin resource). A received response will be displayed in alert window.

## Attachments

- [BoundlessTunes.swf](attachments/BoundlessTunes.swf) (application/octet-stream, 2.4 KB)
- [BoundlessTunes.as](attachments/BoundlessTunes.as) (application/octet-stream, 4.1 KB)

## Timeline

### sc...@gmail.com (2015-04-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-04-27)

Haven't verified this yet, but setting security and impact labels based on the description.

### cl...@chromium.org (2015-04-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-04-30)

Yeah, confirmed cross-origin access, including clearly cookie-authenticated data. I'll file the report with Adobe.

### sc...@gmail.com (2015-04-30)

How would you like Adobe to credit you?

### oj...@gmail.com (2015-04-30)

[Comment Deleted]

### [Deleted User] (2015-05-01)

Adobe tracking as PSIRT-3631.

### sc...@gmail.com (2015-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-09)

Fixed: https://helpx.adobe.com/security/products/flash-player/apsb15-16.html

### oj...@gmail.com (2015-08-10)

Hey,
what does "reward-topanel" mean?

Gamoń

### ti...@google.com (2015-08-31)

#10: It means that we'll take this bug report to our reward panel - details here: https://www.google.com/about/appsecurity/chrome-rewards/

You should have an answer within a few weeks.

### oj...@gmail.com (2015-09-28)

I think this case is considered too long. The issue was reported 5 months ago.

Gamoń

### ti...@google.com (2015-09-28)

I agree - the delay is entirely my fault. 

That said, your report is in front of the panel this week. You should have an answer this week (for real this time).

### ti...@google.com (2015-10-09)

There was some debate over impact of this bug, but our reward panel decided to award you $7500 for this report! Congratulations!

Our finance team should be in contact to collect payment details within a week from today. Please contact me at timwillis@ or update this bug if that doesn't happen.

### cl...@chromium.org (2015-10-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-06-29)

Thank you very much indeed for electing to donate your reward!  We've doubled the amount and I've just approved the request - the money is on its way to the charity you nominated now.  Sorry this process has taken so long!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/481639?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081945)*
