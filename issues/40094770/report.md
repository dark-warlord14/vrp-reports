# Security: CSP restrictions aren't applied when navigating a frame to about:blank

| Field | Value |
|-------|-------|
| **Issue ID** | [40094770](https://issues.chromium.org/issues/40094770) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2019-04-29 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When a page with CSP restrictions applied creates an about:blank frame (either in an iframe or within a new window), that frame inherits the same restrictions. That prevents CSP from being bypassed within the frame.

However, if a page with CSP restrictions first opens another website in a frame, then changes the location of the frame to about:blank, the frame won't have any CSP restrictions applied, even though it's now same-origin with the original page. The same thing also applies to data: URLs.

**VERSION**  

Chrome Version: Tested on 74.0.3729.108 (stable) and 76.0.3780.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 server.py 8080

This will start a simple web server that can be used to serve the files in the directory. server.py is necessary here, as it sets the following Content-Security-Policy header:

Content-Security-Policy: img-src none

This prevents images of any source from being included.

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page includes a single iframe, initially pointing to <http://example.com/>.
5. Two seconds after the page loads, the location of the iframe is changed to about:blank. The following image element is then injected into the frame 1 second later:

<img src="test\_image.png">

The image referenced here shouldn't load, given the above CSP restriction. Instead, it loads successfully and is displayed. Note that the image is in this case just a 10x10 black square.

It's not possible to do this when embedding an about:blank iframe directly (i.e you have to load a different website, then change the location to about:blank). Note that the same thing also works with data: URLs.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 195 B)
- [main.js](attachments/main.js) (text/plain, 477 B)
- [server.py](attachments/server.py) (text/plain, 434 B)
- [test_image.png](attachments/test_image.png) (image/png, 157 B)

## Timeline

### mm...@chromium.org (2019-04-29)

Thanks for your report. I'm able to reproduce and passing this over to CSP experts.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### de...@gmail.com (2019-05-01)

I would imagine it has the same cause, but you can also just create an iframe with a location that's not initially about:blank, but gets rewritten to about:blank. For example,

<iframe src="javascript:;'';"></iframe>
<iframe src="feed://"></iframe>
<iframe src="non-existent-scheme://"></iframe>

### an...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-04-20)

It seems likely https://crbug.com/chromium/1064676 is a duplicate of this.

### ar...@google.com (2020-05-14)

I checked again. This isn't a duplicate of https://crbug.com/chromium/1064676. I can still reproduce.

I think we should check the new function FrameLoader::CreateCSP().
It is totally plausible |initiator_csp| not to be available in this case. This causes us not to inherit CSP.
I remember I let some TODO in the code warning us the current state with the |initiator_csp| to be very fragile. That might be the issue.

Maybe we should inherit from the parent when the initiator isn't known. This isn't correct, but probably slightly safer. I don't know.
+antoniosartori for visibility. FYI.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-05)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-05)

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2725520.



### [Deleted User] (2021-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-05)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-11)

In https://crbug.com/chromium/957606#c23 I copied the wrong CL.

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2667858.

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

Congratulations, David! The VRP Panel has decided to award you $7500 this report. Thanks for your report and patience while the team did some rather comprehensive work on policy inheritance!

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/957606?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094770)*
