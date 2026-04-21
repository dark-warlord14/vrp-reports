# Location Bar URL and SSL Spoofing Risk using "Confirm Form Resubmission" box and a targeted website which allow a redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40085240](https://issues.chromium.org/issues/40085240) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | iOS |
| **Reporter** | jc...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2016-08-30 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to http://www.alternativ-testing.fr/Research/Google%20Chrome/Addressbar-spoofing-for-iOS/test4/poc-step1.html with Google Chrome for iOS and click on the link
2. After all browsing action automated , a "Confirm Form Resubmission" box will appear and click out of this box or click on the "cancel" button.
3. Click on the email input ( the JavaScript function window.stop(); will be actived )

( The targeted website which allow a redirect should use its redirect for a webpage of malicious website which is slow to load )

(You can look this video Example for more information about all steps used : https://www.youtube.com/watch?v=6zVuLZBGX60 )

What is the expected behavior?
This leads to a Location Bar URL and SSL Spoofing.

What went wrong?
When a "Confirm Form Resubmission" box appears and the Form submission is sent to another web site, the location bar shows the URL and the SSL indicator of website targeted but the content of the previous webpage continue to be shown.

Did this work before? N/A 

Chrome version: 59.0.2743.84  Channel: stable
OS Version: OS X 10.10
Flash Version: Shockwave Flash 22.0 r0

(On this testcase the targeted website is https://www.google.com/ and its automatic redirect URL : "https://www.google.com/search?btnI&q=allinurl:http://www.XXX.fr/" and the google redirect URL used is : https://www.google.com/search?btnI&q=allinurl:http://www.alternativ-testing.fr/ )

## Attachments

- [PoC Google Chrome for iOS Location URL and SSL Spoofing.zip](attachments/PoC Google Chrome for iOS Location URL and SSL Spoofing.zip) (application/octet-stream, 30.6 KB)
- [New TestCase (just need a click event to lead to Location Bar URL and SSL Spoofing).zip](attachments/New TestCase (just need a click event to lead to Location Bar URL and SSL Spoofing).zip) (application/octet-stream, 30.4 KB)

## Timeline

### jc...@gmail.com (2016-08-31)

Proof of Concept tested on Iphone 6+ v9.1 .

The testcase uploaded contains all files used by the PoC but to reproduce it, please go to : http://www.alternativ-testing.fr/Research/Google%20Chrome/Addressbar-spoofing-for-iOS/test4/poc-step1.html .

And I will try to code a better testcase soon. 

But like demonstrated in video example ( https://www.youtube.com/watch?v=6zVuLZBGX60 ) the PoC works as described in the Steps needed to reproduce this Location Bar URL and SSL Spoofing vulnerability.


### va...@chromium.org (2016-09-01)

felt@ -- it seems to require some stars to align (looks like a race condition) but it can be reproduced. I am not sure if we would consider it a security issue though. Can you please help triage? Thanks.
In my testing, doesn't seem to repro on Android or Linux but does on iOS.


### va...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>SafeBrowsing]

### sh...@chromium.org (2016-09-02)

[Empty comment from Monorail migration]

### jc...@gmail.com (2016-09-09)

I coded a better testcase needing only a click to lead to a Location Bar URL & SSL Bar Spoofing.
------

STR:

1) Click on the Link on the first PoC Webpage : http://www.alternativ-testing.fr/Research/Google%20Chrome/Addressbar-spoofing-for-iOS/test4/poc-step2.1.html

------

Results:

(You can look this video example of this new testcase in work -> https://www.youtube.com/watch?v=jJLYtK-K_L0 ).

The Location Bar is Spoofed with valid SSL/TLS certificate.

(This new testcase needing just a click event).

------
The last testcase (  ) uploaded needed more user interactions :
{On the last testcase, a click on the first webpage, click out of the "Confirm Resubmition Box" or click on the "cancel" button of it.


### va...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>SafeBrowsing Security>UX]

### fe...@chromium.org (2016-09-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-09-12)

Based on c#6 this seems more like a medium than a low.

This is somehow specific to iOS.  eugenebut@ can you take a look at this and triage and/or assign to the right people? thanks.

[Monorail components: UI>Browser>Navigation]

### eu...@chromium.org (2016-09-13)

Unlike other platforms Chrome for iOS updates last committed URL once you tap back or forward. Fixing this would require significant refactoring. Will, how soon this bug should be fixed?

### sh...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### jc...@gmail.com (2016-09-14)

On the webpage of the testcase I have reduced the time of the last setTimeout used in the testcase used which uses "window.stop();" for a better success rate of this Location Bar Spoofing (URL and SSL Spoofing):

(PoC Webpage : http://www.alternativ-testing.fr/Research/Google%20Chrome/Addressbar-spoofing-for-iOS/test4/poc-step2.1.html )

So, on the new Javascript code I use :
setTimeout("a.window.stop();" , 5300); 
 
// instead of 

setTimeout("a.window.stop();" , 5600);


### jc...@gmail.com (2016-09-14)

Ultimately, I restored the first testcase webpage (poc-step2.1.html) with its previous JavaScript code (same source code that on the testcase uploaded in the https://crbug.com/chromium/642490#c6 : https://bugs.chromium.org/p/chromium/issues/detail?id=642490#c6 ).

So the modifications described in the https://crbug.com/chromium/642490#c12 were deleted on the html file "poc-step2.1.html" on my website.

### sh...@chromium.org (2016-09-27)

eugenebut: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jc...@gmail.com (2016-09-27)

This Location Bar Spoofing (URL & SSL spoofing) vulnerability works on Google Chrome v53.0.2785.109 for iOS (tested today on my Iphone 6+) but sometime the testcase doesn't work the first time and you must try again.

### mm...@chromium.org (2016-10-11)

Friendly ping, any updates here?

eugenebut@, regarding you question c#10: we commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, but since this is Medium, it's up to you. 

### sh...@chromium.org (2016-10-11)

eugenebut: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### eu...@chromium.org (2016-10-11)

mmoroz@, this is planned as Q4 work and will require significant change in Chrome for iOS navigation code. There is no quick fix unfortunately.

### jc...@gmail.com (2016-10-11)

I have again tested this vulnerability (Location Bar URL & SSL Spoofing) today (2016-10-11) and this vulnerability works.
Tested on Google Chrome for iOS v53.0.2785.109 (Last stable update available).

Information about this vulnerability testing: like described in my last comment c#15 , the testcase should work the first time, but if the testcase doesn't work the first time, you must try again the testcase until it works like demonstrated on the link of video in the comment c#6 ( https://www.youtube.com/watch?v=jJLYtK-K_L0 ).

TestCase : http://www.alternativ-testing.fr/Research/Google%20Chrome/Addressbar-spoofing-for-iOS/test4/poc-step2.1.html


### eu...@chromium.org (2016-11-02)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### lg...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX UI>Browser>Omnibox>SecurityIndicators]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-12-22)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-12-22)

Srikanth, could you please retest with M-57 canary. 

### sh...@chromium.org (2016-12-23)

[Empty comment from Monorail migration]

### sr...@chromium.org (2016-12-28)

Both the POC test pages from https://crbug.com/chromium/642490#c1 and https://crbug.com/chromium/642490#c13 aren't working on stable chrome M55. I see a Google error 405page while running the testcase.
405. That’s an error.
The request method POST is inappropriate for the URL /search?btnI&q=allinurl:http://www.alternativ-testing.fr/. That’s all we know.

May be we need a new testcase page?

### jc...@gmail.com (2016-12-28)

yes the /search?btnI&q=allinurl:http://www.alternativ-testing.fr/ redirect to another webpage as the last time when i've coded the PoC.

I will make some tests as soon as possible and look if i should changed some code in the PoC or in the webpage where google redirect using this link :  /search?btnI&q=allinurl:http://www.alternativ-testing.fr/ .

### jc...@gmail.com (2016-12-29)

Srikanth, i've fixed the problem, Now the PoC works very well.

The problem was that /search?btnI&q=allinurl:http://www.alternativ-testing.fr/ redirects to another webpage which doesn't executed PHP.

(this webpage needs to use the sleep() PHP function for the exploitation of the PoC).

I fixed this problem for that the new HTML webpage used executes PHP code.

I've tested the PoC today on the last Google Chrome stable version for iOS and it works.

Information about PoC exploitation: if the testcase doesn't work the first time, you must try again the testcase until it works like demonstrated on the video link in the comment c#6 .

### sr...@chromium.org (2016-12-29)

I am still seeing the same error page on the poc links.
See the video below: https://drive.google.com/file/d/0B-xmXLQhjeKuNGZJWDA4ZUdSNkE/view
Can you point me to what exact URL i need to use inorder to reproduce this issue.

### jc...@gmail.com (2016-12-29)

Srikanth,
the PoC exploitation has a more longtime, after the Google redirect, the PoC uses history.back(), location.reload() and window.stop().

I think know what is the problem.
--------------------------
Try all these steps:

1) Delete all your browsing data.
2) Change your IP address (I think this might be necessary).
3) Verify if this Google redirect ->  www.google.com/search?btnI&q=allinurl:http://www.alternativ-testing.fr/ has a very long time loading and go to this web address -> www.alternativ-testing.fr/Research/Mozilla/6fgg654gvf654v/index.html (this webpage has a very long loading time due to the sleep() PHP function).
4) And after all these steps, retry the PoC.
-------------
[RESULT]
Now the PoC works.

If the PoC doesn't work the first time, try again until it works (delete the new tab opened by the malicious link of the PoC and go back to the tab previously opened which contains the PoC).
--------------------------

I will make also a new video to show you the successful exploitation of PoC on the same Google Chrome for iOS version shown in your video.

### sr...@chromium.org (2016-12-29)

Thanks for the update. I still can't get to repro it I am blocked by the same google.com 405 error page and then also "Site can't be reached" error page for www.alternativ-testing.fr/Research/Mozilla/6fgg654gvf654v/index.html.

We believe this bug is fixed in the 57 version of chrome as part of other changes. So please verify once Chrome 57 update is available.

### jc...@gmail.com (2016-12-30)

I can reproduce this issue.

I've make a new video with the same Google Chrome for iOS version:
https://www.youtube.com/watch?v=40xVFgJVnJQ

Info: I don't know why, but when i make a video recording of my Iphone's screen (using QuickTime Player) the PoC is much more hard to be exploited. But when i try the PoC without make a video recording of my Iphone's screen, the exploitation is very much more easy.

### aw...@chromium.org (2017-01-04)

thanks jconsultant.chancel@ - could you confirm the version you used in #33?

### jc...@gmail.com (2017-01-04)

I've tested the PoC on the same version used by srikanthg@ in its video on https://crbug.com/chromium/642490#c30.

My Google Chrome for iOS version used is visible on my video in https://crbug.com/chromium/642490#c33 (after the first 58 seconds): https://youtu.be/40xVFgJVnJQ?t=58s 

«
Google Chrome: 55.0.2883.79 (Build officiel) stable (64 bits)
Système d'exploitation: iOS 
(...)
»

### aw...@google.com (2017-01-10)

[Empty comment from Monorail migration]

### oc...@chromium.org (2017-01-18)

eugenebut@, were you able to reproduce this bug? was this fixed by one of your CLs?

### eu...@chromium.org (2017-01-18)

I was able to reproduce this problem and it should be fixed by now.

### wf...@chromium.org (2017-01-25)

hi eugenebut@ can you link the CL for the fix please? Thanks!

### eu...@chromium.org (2017-01-25)

There is no single CL. But design doc and CLs can be found in crbug.com/661858

### sh...@chromium.org (2017-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-04)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### eu...@chromium.org (2017-02-04)

There is nothing to merge. All changes were landed before the branch point.

### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Congratulations! The panel decided to award $1,000 for this report.  A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-02-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/642490?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox>SecurityIndicators]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085240)*
