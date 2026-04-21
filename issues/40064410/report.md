# Security: Chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40064410](https://issues.chromium.org/issues/40064410) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>Referrer |
| **Platforms** | iOS |
| **Reporter** | ia...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-05-07 |
| **Bounty** | $1,000.00 |

## Description

This may fall under ExternalDependency as per Chrome Bug System. Already reported to Apple Report ID - OE09428599144

##Summary
`<meta name="referrer" content="no-referrer">`
The HTML code <meta name="referrer" content="no-referrer"> sets the referrer policy for the webpage. The referrer policy determines how much information about the referring URL (the page that linked to the current page) is sent when a user navigates from one page to another.

In this specific case, the content attribute is set to "no-referrer", which means that when a user clicks a link on the current page and navigates to another page, the referring URL will not be sent as the referrer information to the new page. Essentially, the "no-referrer" value prevents the receiving page from knowing the specific URL of the page that linked to it.

This can be useful for preserving privacy and preventing sensitive information from being exposed to external websites. However, it's important to note that the referrer policy can be overridden by certain conditions, such as navigating from a secure (HTTPS) page to a non-secure (HTTP) page or when using certain browser extensions or plugins.

#Problem
Browsers inadvertently leak the referrer information when navigating back to a page that contains resources embedded using object and embed tags.
When a user navigates to a webpage that includes resources, such as images or videos, embedded using object and embed tags, the browser sends a referrer header indicating the URL of the previous page.

##Tested On
Mac M1 Running MacOS Ventura 13.0.1 (22A400)
Chrome Version 113.0.5672.69

##What is the expected behavior?
Exclude referer in all subsequent requests

##What went wrong?
Referer is sent

##POC & Steps
POC Attached refleak.html
POC Video Attached here.
1. Open refleak.html Chrome iOS.
2.The page will load, initially it won't leak but the 2nd time it will reload itself after 2 seconds and referrer will get leak. (Screenshot attached)


## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-05-07)

[Empty comment from Monorail migration]

### bb...@google.com (2023-05-08)

Your report indicates an M1 Mac running MacOS Ventura - but your description and screenshots appear to indicate this is Chrome on iOS. Which is it? 

### bb...@google.com (2023-05-08)

Appears to be chrome on iOS.  Reproduces locally with 113.0.5672.69 running on iOS 16.1.2

Does *not* appear to reproduce for me on MacOS. 

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### bb...@google.com (2023-05-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>Referrer]

### ia...@gmail.com (2023-05-09)

My bad its for Chrome iOS only. Mistakenly mention Chrome Mac!

### [Deleted User] (2023-05-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-05-09)

(I am a bot: this is an auto-cc on a security bug)

### ia...@gmail.com (2023-05-13)

Just FYI, similar kind of referrer leakage was report https://bugs.chromium.org/p/chromium/issues/detail?id=1265193 treated as medium ! Any specific reason for marking severity as low?

### ah...@chromium.org (2023-05-15)

[OWP Security Bug Triage] Hi! thanks for the report. ajuma@ could you take a look? If that affects only chrome on iOS, could you also fill a report with webkit and link it here?

### ia...@gmail.com (2023-05-15)

@ajuma similar kind of referrer leakage was report https://bugs.chromium.org/p/chromium/issues/detail?id=1265193 treated as medium ! Any specific reason for marking severity as low?

### aj...@chromium.org (2023-05-15)

@10, the bug reporter mentioned above that they have already reported this to Apple (report OE09428599144), so I don't think we need to file another WebKit bug.

@11, not sure (I'm not a security triager) but I'm happy to mark it medium for now.


### [Deleted User] (2023-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-15)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ia...@gmail.com (2023-05-21)

is it possible to add some one from Apple Team here just to keep a track of the bug?

### ia...@gmail.com (2023-05-27)

Can we add ddkil...@apple.com in this report?

### aj...@chromium.org (2023-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-07-01)

Just an update. Apple Team responded that "they will address this issue in macOS Sonoma". MacOS Sonoma is in beta mode and based on Apple timeline of releasing new Operating System so macOS 14 Sonoma may release in September or October 2023.

### aj...@chromium.org (2023-07-04)

Based on that, this will also be fixed in iOS 17.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-09-26)

Fixed in iOS 17.

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-05)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us and WebKit. 

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1443238?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ia...@gmail.com (2024-03-21)

@Aj- This issue is fixed? Have you received any updates from Apple? Because I don't have it on original report I sent to Apple!

### aj...@google.com (2024-03-21)

I tested in iOS 17 (see comment 24) and couldn't repro, so marked it as fixed. Are you still able to repro this?

I didn't separately report it to Apple since you had done so already. For future bugs I'd recommend reporting them to Apple as WebKit security bugs at bugs.webkit.org so there's a bug we can all look at.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064410)*
