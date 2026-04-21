# Security: UI spoofing for external protocol dialogues via iframe srcdoc on the malicious site

| Field | Value |
|-------|-------|
| **Issue ID** | [40060490](https://issues.chromium.org/issues/40060490) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-08-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Currently, when right-clicking on a link using an external protocol and clicking "Opening new window" or "Opening a new incognito window". The origin containing the external protocol link will be shown on the external protocol dialog on the new window. You can see <https://bugs.chromium.org/p/chromium/issues/detail?id=1219354#c4> for a detailed reason why

This is to prevent the scenario where Victim site A hosts an iframe to a Malicious Site B and Malicious Site B includes a external protocol link, the Malicious Site B can convince users that trust Victim site A that the link is trusted.

However, the origin can be hidden from the external protocol dialog if the Malicious Site B uses an iframe with a srcdoc attribute containing the malicious link instead.

**VERSION**  

104.0.5112.81 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 21H2 (Build 19044.1826)

**REPRODUCTION CASE**

1. Set up two servers, attacker.example and victim.example.
2. On victim.example, host the following file at poc-victim.html:

<iframe src="http://attacker.example/poc2.html"></iframe>

3. On attacker.example, host the following file (Note: you may change the protocol to tel:1 to match <https://bugs.chromium.org/p/chromium/issues/detail?id=1219354>) at poc-attacker.html:

<iframe srcdoc="<a href=ms-calculator:>test</a>"></iframe>

4. As a user visit <https://victim.example/poc-victim.html>, right click on the link labelled "test" and click "Open in new window". The external protocol dialog will incorrectly show "A website wants to open this application", which will trick users into believing that victim.example is the site that would like to open a new window.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 133.6 KB)
- [poc-victim.html](attachments/poc-victim.html) (text/plain, 65 B)
- [poc-attacker.html](attachments/poc-attacker.html) (text/plain, 62 B)

## Timeline

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-08-04)

Note: The expected behaviour is that the external protocol dialog should show: 

http://poc-attacker.example wants to open this application

### ha...@gmail.com (2022-08-04)

Hi, if you are looking on how to easily setup two domains on localhost you can edit the /etc/hosts or C:\Windows\System32\drivers\etc\hosts on Windows with the following

127.0.0.1      attacker.example
127.0.0.1      victim.example

### ha...@gmail.com (2022-08-04)

Correction to poc

poc-victim.html should be:

<iframe src="http://attacker.example/poc-attacker.html"></iframe>

Attached are the poc-attacker.html and poc-victim.html files




### ma...@google.com (2022-08-05)

rhalavati@, since you reviewed the fix for https://bugs.chromium.org/p/chromium/issues/detail?id=1219354, would you be able to take this one?

[Monorail components: UI>Browser]

### [Deleted User] (2022-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-06)

[Empty comment from Monorail migration]

### rh...@chromium.org (2022-08-08)

I don't know much about the involved protocols and had minimal role in fixing the previous issue.
Adding to privacy triage queue.

[Monorail components: Privacy UI>Browser>Incognito]

### ha...@gmail.com (2022-08-08)

Hi, I don't think this belongs under Incognito UI as it reproduces with incognito / normal windows, it should belong under external protocol dialog UI instead. Maybe the people mentioned in https://bugs.chromium.org/p/chromium/issues/detail?id=1197889#c3 can take this?

### rh...@chromium.org (2022-08-08)

Thank you for the pointer. I was originally involved because of Incognito but you are right. Updating the component.

[Monorail components: -UI>Browser -UI>Browser>Incognito UI>Browser>WebAppInstalls>ProtocolHandling]

### do...@chromium.org (2022-08-08)

This appears to be due to [1]: the initiating origin is blank or opaque, and this the generic string "A website ..." is displayed.

I'm not an expert on how to calculate iframe origins, but it appears to me that 

<iframe srcdoc="<a href=ms-calculator:>test</a>"></iframe>

could well have an opaque or blank origin as the HTML is directly inline rather than pulled from an actual URL. It's not exactly clear to me how this could be made more sensible given the nesting structure used here.

cthomp, do you have more thoughts?


1. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/external_protocol_dialog.cc;l=41?q=IDS_EXTERNAL_PROTOCOL_MESSAGE_WITH_INITIATING_ORIGIN

[Monorail components: -UI>Browser>WebAppInstalls>ProtocolHandling]

### ha...@gmail.com (2022-08-08)

It seems that clicking on the link in:

<iframe srcdoc="<a href=ms-calculator:>test</a>"></iframe>

instead of right click > opening it in a new tab / window will show the correct origin of http://attacker.example. Is there any reason why there is a difference between the behaviour when clicking on the link versus right clicking on the link and open in new tab / window?

### jo...@chromium.org (2022-11-08)

I'd argue that this is mostly working as intended. The context menu params pass the frame's URL, not the origin, and the URL for a srcdoc is about:blank.

Adding mkwst / clamy for additional input.

[Monorail components: -Privacy]

### ha...@gmail.com (2023-12-06)

I believe this is fixed in latest stable by https://chromium-review.googlesource.com/c/chromium/src/+/4763411

### ha...@gmail.com (2023-12-06)

I uploaded the PoCs to external sites.

When right clicking on the URL > open in new tab, https://goofy-fancy-ceiling.glitch.me/poc-victim.html will show the correct thunder... site as opposed to "This website"

### ha...@gmail.com (2023-12-06)

external sites -> my private glitch.me instance*

### ad...@chromium.org (2023-12-19)

ellyjones@ could you confirm whether your CL has fixed this? If so please mark it as as fixed, or as a duplicate of https://crbug.com/chromium/1457702 and add reward-topanel since I don't quite trust our bots to do that automtically.

### el...@chromium.org (2024-01-02)

I believe this is a duplicate of https://crbug.com/chromium/1457702 and was fixed by the linked CL from #15. Marking as such.

[Monorail components: UI>Browser>Navigation]

### [Deleted User] (2024-01-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Axel! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1350028?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1457702]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-04-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060490)*
