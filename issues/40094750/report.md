# Security: Possible to include mixed content in an about:blank popup opened by a https page

| Field | Value |
|-------|-------|
| **Issue ID** | [40094750](https://issues.chromium.org/issues/40094750) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2019-04-26 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, a https site can't use or access resources from a http site. The browser will block attempts by a https site to include a http iframe, for example.

However, a https site that opens a new window with a location of "javascript:" will be able to include a http iframe within that window, even though it shares the same (https) origin as the original page.

**VERSION**  

Chrome Version: Tested on 74.0.3729.108 (stable) and 76.0.3777.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The demo here requires a https page. Therefore, I've set up the following page:

<https://derceg.gitlab.io/mixed_content_popup/>

As a first step, you'll need to open this page. I've attached the source for the page to this issue, which will allow you to test it locally, if necessary.

2. The page contains a single link. When you click that link, a new window will be opened using the following call:

var newWindow = window.open("javascript:''", "\_blank");

3. Once this window has been opened, the original page will update it to include a http iframe using the following sequence of calls:

var iframe = newWindow.document.createElement("iframe");  

iframe.src = "<http://neverssl.com/>";

newWindow.document.body.appendChild(iframe);

This should fail, given that the window that was opened is same-origin with the original https page. However, it doesn't and the iframe is loaded successfully.

It appears this only really affects iframes. You still can't fetch() a http resource in the new window, for example.

Note that you don't need to use a location of "javascript:". The following calls will also work:

window.open("feed://", "\_blank");  

window.open("mailto://", "\_blank");  

window.open("file:///C:/", "\_blank");

The key point seems to be that you need to open a new tab whose initial location isn't about:blank (though in each of these cases, that's what the URL is ultimately rewritten to).

Finally, the behavior described above is different to the case in which you open an about:blank window directly using the following call:

window.open("about:blank", "\_blank");

Attempts to include a http iframe within that page will fail.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 202 B)
- [main.js](attachments/main.js) (text/plain, 417 B)

## Timeline

### mm...@chromium.org (2019-04-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### ca...@chromium.org (2019-04-26)

Hmm, this one's interesting. I think since the main frame URL is not https://, the mixed content checker doesn't run at all, so it's not too surprising that this one doesn't get marked, and I don't know if we'd call it mixed content. That being said the fact that the original window can set an iframe on the new window definitely seems like a bug to me, likely weirdness related to about:blank.

### sh...@chromium.org (2019-04-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@gmail.com (2019-04-29)

I think the issue here is that if you open an "about:blank" page directly (rather than something like "javascript:" which ultimately gets rewritten to "about:blank"), you can't include a http iframe. Any attempt to will fail and the following message will be logged to the devtools console:

Mixed Content: The page at 'about:blank' was loaded over HTTPS, but requested an insecure resource 'http://neverssl.com/'. This request has been blocked; the content must be served over HTTPS.

Aside from the message, the content blocking icon also appears in the right end of the Omnibox (which states that insecure content was blocked). I believe this happens because although the URL of the page is "about:blank", it's security origin matches that of its opener (i.e. https://derceg.gitlab.io). I think that's also the reason why you can write to the new window from the original page - because they have the same security origin.

### mm...@chromium.org (2019-04-29)

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

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-08-12)

This seems to have been fixed by the mixed content changes (likely the removal of the active mixed content shield)

### [Deleted User] (2022-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, David! The VRP Panel has decided to award you $3,000 for this report. Thank you for your patience as this was resolved, but also in the time delta of getting this issue closed out as fixed to get to panel! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-19)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/957002?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094750)*
