# SameSite Strict cookies are included when middle clicking a link to another site in a PDF document

| Field | Value |
|-------|-------|
| **Issue ID** | [416942878](https://issues.chromium.org/issues/416942878) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>Cookies, Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gn...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2025-05-11 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

SameSite Strict cookies are included when middle clicking a link to another site in a PDF document

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

Steps to reproduce:

- Navigate to a page that has set a cookie with SameSite=Strict
- Create a PDF document with a link to that page
- Open that PDF in Chrome, and open the link in a new tab with a middle mouse click
- The SameSite cookie is included with the request for that tab, even if the PDF was served from a different site.

The above steps detail the basic idea, however for ease of reproduction I have also created a Flask application to demonstrate the behaviour at the following GitHub repository: <https://github.com/gnea-sec/samesite-demo>

- Add an entry to your hosts file, such as `notlocalhost`, that also points to `127.0.0.1`.
- Launch the server, and navigate to <http://localhost:8181/setcookie>
  - This sets a cookie with SameSite=Strict
- Verify that the cookie is set at <http://localhost:8181/showcookie>
- Navigate to <http://notlocalhost:8181/pdflink>
  - Note that this is on a separate domain `notlocalhost`, and following links from this site should not include the SameSite cookie.
- Middle mouse click on the link to open it in a new tab. Note that the tab indicates that the SameSite cookie was received.
  - Opening the link by left clicking, or right clicking and selecting "Open link in new tab" does not include the cookie.
- The origin of the link can be further obfuscated, such as by loading it in an iframe, as demonstrated in the mentioned application at <http://notlocalhost:8181/frame>

The attached video `samesite-example.mp4` shows this server being used to demonstrate the issue. It shows a regular HTML link that does not include the SameSite cookie when followed from another site, and then shows the PDF document being served from another site. When the PDF link is followed with a left click, or right click and open in new tab, it does not include the SameSite cookie. However, when the link in a PDF document is middle clicked, it does include the SameSite cookie.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

SameSite Strict cookies should not be included when following links from another site. If a website has functionality that can perform a sensitive action with a GET request, and it is relying on a SameSite cookie to prevent unauthorized access, then this can be used in social engineering attacks against users of that site. Any malicious actor would be able to target users of websites that are vulnerable in this way, and use this issue to exploit CSRF vulnerabilities.

This issue can be exploited to circumvent SameSite cookie protections. Following a link from another site should not include SameSite cookies. While a secure web application should not be significantly impacted by this issue, it has the potential to exacerbate certain misconfigurations. For instance, if a GET request is able to perform a sensitive action (it would not be unheard of for an endpoint intended to receive POST requests to also accept GET), then a malicious site could display a PDF loaded in an iframe, and use social engineering techniques to convince users to middle click on the link. A targeted phishing campaign does not need to fool everyone, it just needs to fool one person.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 136.0.7103.93 (Official Build) (64-bit)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Cross-site request forgery (CSRF)

#### How would you like to be publicly acknowledged for your report?

Vincent Dragnea

## Attachments

- [samesite-example.mp4](attachments/samesite-example.mp4) (video/mp4, 1.1 MB)
- [samesitetest-link.pdf](attachments/samesitetest-link.pdf) (application/pdf, 9.8 KB)

## Timeline

### gn...@gmail.com (2025-05-11)

This issue can also be tested using the site <https://samesitetest.com/> instead of running a server locally.

- Navigate to <https://samesitetest.com/cookies/set> to set the cookie.
- Open the attached PDF document in Chrome.
- Middle mouse click on the link in the document to open the link in a new tab.
- Note that the Strict cookie was received.

### pe...@google.com (2025-05-13)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### jd...@chromium.org (2025-05-13)

Well that's kind of fun. I'm assigning this severity-low, since it's a limited bypass of something that can indeed be used as a CSRF protection.

thestig@: would you mind taking a look at this? Thanks!

### gn...@gmail.com (2025-05-13)

I think it has potential to score as medium severity. It requires active user interaction (middle clicking on the link), but it negates SameSite=Strict cookie protections for GET requests. A malicious site could also load the PDF link in an iframe, and style it to look like normal HTML, so while the issue is in the PDF viewer, the exploit could be hidden within any website, and it might not be obvious to the victim that they are clicking in a PDF. However, I'll defer to your judgment on scoring.

### ch...@google.com (2025-05-13)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2025-05-22)

I think this is bug 40088888. i.e. There's been a report open for this for an embarrassingly long amount of time.

### th...@chromium.org (2025-06-07)

I finally looked into [bug 40088888](https://issues.chromium.org/issues/40088888) but can't repro. Since I have a setup for SameSite Strict cookies, I'll look into this one soon.

### dx...@google.com (2025-06-10)

Project: chromium/src  

Branch: main  

Author: Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6629248>

[PDF] Perform navigations from the PDF Viewer more consistently

---


Expand for full commit details
```
     
    The PDF Viewer uses chrome.tabs.update() and chrome.tabs.create() to 
    navigate to links in the current tab and in a new tab, respectively. To 
    make their behavior more consistent, copy navigation params from 
    TabsUpdateFunction::UpdateURL() to ExtensionTabUtil::OpenTab(). 
     
    It may be beneficial for ExtensionTabUtil::OpenTab() to use the PDF 
    Viewer behavior for all chrome.tabs.create() calls. But for now, only 
    apply it to the PDF Viewer to avoid potential compatibility issues. 
     
    Bug: 416942878 
    Change-Id: I797b9efa38872fa9269ba01cde752e0796dd2ef8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6629248 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1471532}

```

---

Files:

- M `chrome/browser/extensions/extension_tab_util.cc`

---

Hash: d2d70e969646e9ba1c5f4a0ad586fe327eefc7b6  

Date:  Tue Jun 10 01:05:21 2025


---

### sp...@google.com (2025-06-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for a solid and helpful report of web platform privilege escalation issue


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-18)

Thank you for your efforts and reporting this issue to us -- nice work!

### ch...@google.com (2025-09-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/416942878)*
