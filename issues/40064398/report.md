# Security: Chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40064398](https://issues.chromium.org/issues/40064398) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security, Mobile>iOSWeb>WebPlatform |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2023-38572 |
| **Reporter** | ia...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-05-06 |
| **Bounty** | $1,000.00 |

## Description

Bypass of https://bugs.chromium.org/p/chromium/issues/detail?id=1145553

Affecting Chrome iOS Version 113.0.5672.69
Tested On iPhone 12 Running 16.4.1 (a)

Steps
======

1.Download server.py (attached)

2.To run this you will need flask, if not already installed pip install flask
Run this python by python server.py

3.On different server Create a html file (attached)
 (http://examplevictim.com/hello.html) `

5. Now run your hello.html (http://examplevictim.com/hello.html)  page and just after you open, it will get redirected to https://google.com


This may fall under ExternalDependency as per Chrome Bug Report. Already reported to Apple Report ID - OE09424939821

Based on impact, my propose severity is High, as Many hacker groups have actively exploited similar kinds of bugs to serve fake pdf downloads and  support scams. On November 3rd 201.

## Attachments

- [server.py](attachments/server.py) (text/plain, 383 B)
- [hello.html](attachments/hello.html) (text/plain, 112 B)
- deleted (application/octet-stream, 0 B)
- [Screenshot 2023-05-25 at 11.50.13 AM.png](attachments/Screenshot 2023-05-25 at 11.50.13 AM.png) (image/png, 175.9 KB)
- [server1.py](attachments/server1.py) (text/plain, 383 B)
- [scenario1-chrome-refused-to-redirect.png](attachments/scenario1-chrome-refused-to-redirect.png) (image/png, 430.9 KB)
- [scenario1-safari-refused-to-redirect.png](attachments/scenario1-safari-refused-to-redirect.png) (image/png, 404.8 KB)
- [Scenario2 Chrome Mac Blocked Redirection.png](attachments/Scenario2 Chrome Mac Blocked Redirection.png) (image/png, 255.6 KB)
- [Scenario2 Safari Mac Allowed Redirection.mov](attachments/Scenario2 Safari Mac Allowed Redirection.mov) (video/quicktime, 3.1 MB)
- [server1.py](attachments/server1.py) (text/plain, 383 B)
- [scenario1-chrome-refused-to-redirect.png](attachments/scenario1-chrome-refused-to-redirect.png) (image/png, 430.9 KB)
- [scenario1-safari-refused-to-redirect.png](attachments/scenario1-safari-refused-to-redirect.png) (image/png, 404.8 KB)
- [Scenario2 Chrome Mac Blocked Redirection.png](attachments/Scenario2 Chrome Mac Blocked Redirection.png) (image/png, 255.6 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-05-06)

[Empty comment from Monorail migration]

### nh...@google.com (2023-05-08)

I am not able to reproduce on iOS 16.4.1 (a) in Chrome 113.0.5672.69. When I load /hello.html, I see the text "hello" and an empty iframe. No network request is being made to /test on port 5000. I'm also not able to reproduce this in Safari on the same device.

Can you provide more information on how to reproduce this issue and a screen recording of the issue?

### ia...@gmail.com (2023-05-08)

[Comment Deleted]

### [Deleted User] (2023-05-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ia...@gmail.com (2023-05-08)

One more thing, because server.py (Server B) is running on HTTP and hello.html (Server A) which might be running on HTTPS, that may be reason you are not getting network request on 5000 port.

In my POC video I have used Server A running on HTTP only (Not HTTPS) Hope it helps.

### ia...@gmail.com (2023-05-08)

Uploaded video here also for your reference.

### nh...@google.com (2023-05-09)

I am able to reproduce in Chrome and Safari on iOS 16.4.1 (a). I ran python3 server.py and python3 -m http.server 8000 from the directory containing both files, and modified hello.html to have the IP address reported by server.py's startup message.

### nh...@google.com (2023-05-09)

[Empty comment from Monorail migration]

[Monorail components: Mobile>iOSWeb>Security Mobile>iOSWeb>WebPlatform]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-05-09)

Even its affecting Safari MacOS as well.

### dd...@apple.com (2023-05-09)

> Already reported to Apple Report ID - OE09424939821

Apple Product Security is already tracking this as well from the above report.


### aj...@chromium.org (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ia...@gmail.com (2023-05-25)

[Comment Deleted]

### ia...@gmail.com (2023-05-25)

@ddkil...@apple.com  - Apple team responded that this is not a vulnerability. Response screenshot is attached. @ddkil...@apple.com can you suggest what should I do.

Surprisingly they have have decided to fix my other report (Apple Report OE09408828484, Chrome Report Number 1441648) which have exact same impact but the payload/vulnerability is different.

### dd...@apple.com (2023-05-25)

> Surprisingly they have have decided to fix my other report (Apple Report OE09408828484, Chrome Report Number 1441648) which have exact same impact but the payload/vulnerability is different.

Internally, I see "Apple Report OE09408828484" is mapped to <https://bugs.chromium.org/p/chromium/issues/detail?id=1151507>.

I can't see CR https://crbug.com/chromium/1441648, so I can't tell what that issue is.  (Maybe you meant to paste a different bug ID 1151507 instead?)

—

As far as this report ("Apple Report ID - OE09424939821"), there is a request for more information from you about the PoC.  You should have an email from Apple Product Security requesting more information.  You should reply to that message directly, but I'll paste the investigation comments here in case you can't find it (this is from another engineer—not me—so I can't answer questions directly about the issue):

'''
I reproduced the issue on [internal build] 22F56 [which is a pre-GM build of macOS Ventura 13.4]. Safari seem[s] to behave correctly. I don’t understand what’s the bug here, server allows iframes to change top level context with allow-top-navigation.

From W3C: https://www.w3schools.com/tags/att_iframe_sandbox.asp
“allow-top-navigation	Allows the iframe content to navigate its top-level browsing context”
'''


### ia...@gmail.com (2023-05-25)

 ddkil...@apple.com  [Report OE09408828484] & [Report OE09424939821] have same impact and exploitation the only different is of payload, that's it. That the reason I am surprised they accepted OE09408828484 but not this OE09424939821.

Can we add "ddkil...@apple.com" for the bug report CR Bug Report 1441648 as its required a fix from Webkit also so that "ddkil...@apple.com" can take a look.




### ia...@gmail.com (2023-05-25)

[Comment Deleted]

### dd...@apple.com (2023-05-25)

> [Report OE09408828484] & [Report OE09424939821] have same impact and exploitation the only different is of payload, that's it. That the reason I am surprised they accepted OE09408828484 but not this OE09424939821.

The Product Security engineer said that this isn't a bug because, the "server allows iframes to change top level context with allow-top-navigation."

So they're saying that the test case for this bug is "behaves correctly" because of the use of "allow-top-navigation" in the PoC.

You need to investigate that and then explain why this PoC doesn't "behave correctly" per the standard (<https://www.w3schools.com/tags/att_iframe_sandbox.asp>).



### ia...@gmail.com (2023-05-25)

[Comment Deleted]

### ia...@gmail.com (2023-05-25)

[Comment Deleted]

### ia...@gmail.com (2023-05-25)

nha...@google.com & aj....@chromium.org can you pleas also share your feedback on this meanwhile I am also cross checking.


### aj...@chromium.org (2023-05-25)

I'm not entirely clear on what the test case is exactly. Is the point that the *iframe* is itself creating an iframe, and setting "allow-top-navigation" on that frame, and that is allowing the new frame to redirect the top frame?

Specifically, we have: main frame->child frame->grandchild frame, and because "child frame" is setting "allow-top-navigation" on "grandchild frame", "grandchild frame" is now able to redirect the main frame?

That would certainly be a bug (assuming child/grandchild are cross-origin wrt main frame). If that's the test case, please consider writing it out that way to make it clear.

### ia...@gmail.com (2023-05-25)

Browser will block automatic redirects that are not activated by user interaction from cross-origin iframes.

Scenario 1
hello.html is hosted a DomainA ex. https://victim.com/b.html
==========b.html=====================
<h1>hello</h1>
<iframe src="http://attacker.com/test.html" title="Test"></iframe>
========================================

This is running on cross domain DomainB ex. https://attacker.com/attacker.html
============attacker.html================
<script>
    top.window.location = "https://apple.com";
</script>
========================================

Now if you access http://victim.com/b.html from Safari, it won't redirect to https://apple.com

I have created a test case here - https://secondtestingspace.000webhostapp.com/b.html check the attached screenshot [scenario1-safari-refused-to-redirect.png & scenario1-chrome-refused-to-redirect.png] Safari and Chrome will block the redirection.

Scenario 2
b.html is hosted a DomainA ex. http://victim.com/b.html
==========b.html=====================
<h1>hello</h1><iframe src="http://127.0.0.1:5000/test" title="Test"></iframe>
==========b.html=====================

This (server1.py) is running on cross domain DomainB ex. http://127.0.0.1:5000/test
===========server1.py========
attached below
====================================
Now if you run this in Safari Mac http://victim.com/b.html it will get redirected to https://apple.com When b.html loaded http://attacker.com:5000/test as iframe. This tricks the b.html to allow navigation to domain.  [Check=Scenario2 Safari Mac Allowed Redirection.mov]

But If you run this http://victim.com/b.html in Chrome Mac it will block redirection.  [Check -Scenario Chrome Mac Blocked Redirection.png]

Also If you run this http://victim.com/b.html in Chrome iOS and Safari iOS it will get redirected to https://apple.com.

Which means Safari Mac, iOS Safari and Chrome iOS are affected, that also means any browser running under iOS is also affected unless webkit releases a fix.

What is the expected behavior?
Automatic redirects from cross-origin iframes should be blocked by the browser.

What went wrong?
This is being bypassed with the payload provided above.

Hope I am able to explain now.

### ia...@gmail.com (2023-05-25)

Browser will block automatic redirects that are not activated by user interaction from cross-origin iframes.

Scenario 1
hello.html is hosted a DomainA ex. https://victim.com/b.html
==========b.html=====================
<h1>hello</h1>
<iframe src="http://attacker.com/attacker.html" title="Test"></iframe>
========================================

This is running on cross domain DomainB ex. https://attacker.com/attacker.html
============attacker.html================
<script>
    top.window.location = "https://apple.com";
</script>
========================================

Now if you access http://victim.com/b.html from Safari, it won't redirect to https://apple.com

I have created a test case here - https://secondtestingspace.000webhostapp.com/b.html check the attached screenshot [scenario1-safari-refused-to-redirect.png & scenario1-chrome-refused-to-redirect.png] Safari and Chrome will block the redirection.

Scenario 2
b.html is hosted a DomainA ex. http://victim.com/b.html
==========b.html=====================
<h1>hello</h1><iframe src="http://127.0.0.1:5000/test" title="Test"></iframe>
==========b.html=====================

This (server1.py) is running on cross domain DomainB ex. http://127.0.0.1:5000/test
===========server1.py========
attached below
====================================
Now if you run this in Safari Mac http://victim.com/b.html it will get redirected to https://apple.com When b.html loaded http://attacker.com:5000/test as iframe. This tricks the b.html to allow navigation to domain.  [Check=Scenario2 Safari Mac Allowed Redirection.mov]

But If you run this http://victim.com/b.html in Chrome Mac it will block redirection.  [Check -Scenario Chrome Mac Blocked Redirection.png]

Also If you run this http://victim.com/b.html in Chrome iOS and Safari iOS it will get redirected to https://apple.com.

Which means Safari Mac, iOS Safari and Chrome iOS are affected, that also means any browser running under iOS is also affected unless webkit releases a fix.

What is the expected behavior?
Automatic redirects from cross-origin iframes should be blocked by the browser.

What went wrong?
This is being bypassed with the payload provided above.

Hope I am able to explain now.

### aj...@chromium.org (2023-05-25)

Is it an accurate summary that the iframe is allowing itself to redirect the top frame by sending an allow-top-navigation Content-Security-Policy header, or are there other essential parts to triggering this?

### ia...@gmail.com (2023-05-27)

 ddkil...@apple.com I have sent revised information to produc...@apple.com email. That would be great if you can check internally if possible.

### dd...@apple.com (2023-05-27)

Yes, I can confirm that Product Security received the info.  Thanks!

### ia...@gmail.com (2023-05-27)

ddkil...@apple.com Thanks for confirming. Appreciate you response

### ia...@gmail.com (2023-05-27)

[Comment Deleted]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-06-27)

ddkil...@apple.com - I received an email from Product team that "They are addressing the issue you reported with a mitigation in an upcoming security update. While it will not receive a CVE, we want to publicly acknowledge your assistance on our security advisory."

If possible! Can you take a look on my feedback and response over product team email.  Very appreciate your response.

### dd...@apple.com (2023-06-27)

Please give Apple Product Security team time to respond.  I do not have access to those messages.

### ia...@gmail.com (2023-08-11)

Hello Team,

The vulnerability is now fixed in recent apple security update.

Just a feedback to reward top panel team, this report was a Bypass of previous vulnerability https://bugs.chromium.org/p/chromium/issues/detail?id=1145553

### dd...@apple.com (2023-08-11)

Tracked in WebKit by:

https://crbug.com/chromium/257903: Third Party IFrame Navigation Block Bypass via Content Security Policy Sandbox
<https://bugs.webkit.org/show_bug.cgi?id=257903>

Fixed in iOS 16.6.


### aj...@chromium.org (2023-08-11)

Thanks for the update! I believe this is https://bugs.webkit.org/show_bug.cgi?id=256549, fixed in iOS 16.6 as CVE-2023-38572

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ia...@gmail.com (2023-08-18)

Hello Team, I would like to bring your attention that my report is a Bypass of https://bugs.chromium.org/p/chromium/issues/detail?id=1145553 which was rewarded for $5000.

So can you please help me why my current report is only awarded as $1000 only?

Your response will help me in doing further security research on chrome!

### am...@chromium.org (2023-08-18)

Congratulations! The VRP Panel has decided to award you $1,000 for this webkit issue impacting Chrome on iOS. Thank you for your efforts and reporting this issue to us.

### am...@chromium.org (2023-08-18)

Hello, the issue you referenced (https://crbug.com/chromium/1145553) was a through and high-quality report that provide a clear and concise explanation and demonstration of the security impact of this issue being presented. While your report was appreciated, it lacked some of the qualities and characteristics expected for a high-quality or even baseline report [1]. The original report on 6 May did not define what the bug even being presented was or the security consequences were from the current conditions at the time.  There was much back and forth before we or the WebKit engineers could interpret the potential security issue being presented. I hope this helps explain the reward amount. You may want to review other security bug reports of similar bugs and compare them to the report quality guidelines linked below.

[1] https://g.co/chrome/vrp/#report-quality 

### ia...@gmail.com (2023-08-18)

Thanks. I just gone through the report https://bugs.chromium.org/p/chromium/issues/detail?id=1145553 and found the report details is similar to mine and the only difference is I didn’t mentioned the impact which I did intentionally because this report was a bypass of https://bugs.chromium.org/p/chromium/issues/detail?id=1145553 so I assumed that you can refer the impact from that report only.

I might be wrong but I tried to mentioned all possible information!

 Is it possible to for VRP team to take a look on this report again and reevaluate the reward?

### am...@chromium.org (2023-08-18)

Not all bypasses are equal. More importantly, https://crbug.com/chromium/1145553 affected practically all Chrome platforms and was due to and mitigated by changes to blink code used natively in Chromium. This is an iOS specific issue in WebKit . There was a lot of back and forth for us and the Apple folks to glean the security impact here. 
We spent a lot of time discussing this issue and were not even sure it warranted a VRP reward at first also. This reward amount seems sufficient given the amount of effort for engineering owners to move this issue forward toward a resolution and based on the information and impact presented of your own accord. 

We can take another look, but I feel it is important to level set your expectations and inform you that the outcome is unlikely to change on this one. 
As communicated in an email a bit ago, the Chrome VRP Panel is on hiatus for the next couple of weeks, so we would not be reassessing this issue until that time. 

### ia...@gmail.com (2023-08-18)

Thanks for the information.

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-17)

Hello Narendra! We consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks! 

### ia...@gmail.com (2023-12-04)

Sure. @am One of my personal information was there in POC Video so I am deleting it only. Rest is fine for me.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1443147?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Mobile>iOSWeb>Security, Mobile>iOSWeb>WebPlatform]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064398)*
