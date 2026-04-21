# Security: Chrome on IOS ignores Content-Type header when rendering XML and SVG content

| Field | Value |
|-------|-------|
| **Issue ID** | [40063810](https://issues.chromium.org/issues/40063810) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | iOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-03-28 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

XML files can contain HTML and thus run javascript if they are delivered as content-type: text/xml. A way to safely deliver user supplied files as raw data is to set the content-type to text/plain instead. This will make all desktop browsers render the XML data as plain text. Preventing any HTML injection or javascript execution.

When visiting a page delivering an .xml file in Chrome for IOS with the content-type: text/plain header the XML will still render. This will allow for HTML injection and javascript execution on all sites using this as their "safety feature" (this includes for example viewing raw file content on git hosting sites).

CSP will still block javascript execution if put in place. And a Content-Dispostion header containing a file name or "attachment" will force a download instead of rendering the file.

The same issue seems to exist for .svg files

**VERSION**  

Chrome Version: 111.0.5563.72  

Operating System: IOS 16.4

I do not own an android phone, so I don't know if it affect Chrome there.

**REPRODUCTION CASE**  

Visit <https://joaxcar.com/xss/test.xml> in Chrome on desktop and see the XML as plain text.  

Visit <https://joaxcar.com/xss/test.xml> in Chrome on IOS and an alert will pop up (XSS) and HTML will render in the page.

(SVG example <https://joaxcar.com/xss/image.svg>)

Reproduce yourself:  

Host this content

<?xml version="1.0" encoding="UTF-8"?>
<html xmlns:html="http://www.w3.org/1999/xhtml">
<html:script>alert(document.domain);</html:script>
</html>

in a file named test.xml

add this to a .htaccess file to force Content-Type

Header always set Content-Type "text/plain"

## Attachments

- [test.xml](attachments/test.xml) (text/plain, 313 B)

## Timeline

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### jo...@gmail.com (2023-03-28)

I might have been a bit to quick here. I found this while using my Chrome browser on my phone, but now realized that IOS forces browsers to use WebKit. I tested my POC sites in Safari for IOS as well and they have the same behavior.

I guess this could be an issue in WebKit. Should I report this somewhere else? Is it Apple who takes care of WebKit issues?

Sorry for the confusion!

Best
Johan

### mp...@chromium.org (2023-03-29)

I think this is the same as https://crbug.com/chromium/900441. Yes if you could file a WebKit bug that'd be great. Adding ajuma@

### jo...@gmail.com (2023-03-29)

I reported it as a webkit bug to Apple now. I will get back here when I get a response from them!

/Johan

### aj...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-03-29)

If this still repros it's different from https://crbug.com/chromium/900441, since the WebKit bug that depends on turns out to have been fixed in 2020.

### [Deleted User] (2023-03-29)

[Empty comment from Monorail migration]

### jo...@gmail.com (2023-09-25)

Hi team (ajuma@), just wanted to get back here. This bug is fixed in https://bugs.webkit.org/show_bug.cgi?id=257299 

I did some additional testing while this bug was still open. Using the described flaw I was able to perform XSS attacks against BitBucket (two instances) and GitLab. There did probably exist other vulnerable websites out there, but Git-hosting platforms stood out as most of them allow for RAW content being displayed to users through their APIs. These endpoints usually (as was the case for both GitLab and Bitbucket) protect themselves by adding a "Content-Type: text/plain" header.

Using the bug described here these sites instead rendered the supplied content. I mentioned XML here but the sniffing issue did also include SVG and XHTML

I can not access the webkit bug as I do not have the right permissions. But my testing does indeed verify that this is fixed in Chrome IOS as well

I don't know if this is eligible for a bounty, I found this while testing Chrome on IOS and Apple does not intetend to reward it. Feels like these WebKit issues are in a strange spot as they impact all browsers on the IOS platforms

Best regards
Johan

### aj...@chromium.org (2023-09-25)

Thanks! This is fixed by https://github.com/WebKit/WebKit/commit/d294c9bf0f3fe2c7bb92dff5efc544c886001681, which is in iOS 17 and might also be in 16.6.

> I don't know if this is eligible for a bounty, I found this while testing Chrome on IOS and Apple does not intetend to reward it. 

Now that this is marked Fixed, it will go into Chrome's process for determining rewards.  

### [Deleted User] (2023-09-25)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2023-09-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### vo...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations, Johan! The Chrome VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us and helping us keep Chrome users on iOS more secure! 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-02)

This issue was migrated from crbug.com/chromium/1428730?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063810)*
