# site information  change url to about:blank#https://google.com

| Field | Value |
|-------|-------|
| **Issue ID** | [354882231](https://issues.chromium.org/issues/354882231) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Mobile>CustomTabs |
| **Platforms** | Android |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | bh...@gmail.com |
| **Assignee** | si...@google.com |
| **Created** | 2024-07-23 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1. go to mrnoob790.github.io/blob.html
   click on click so url will show about:blank
   title show google.com and site information show about:blank#<https://www.google.com>
   so user will be confused and easily attacker can spoof it

# Problem Description

site information showing about:blank#url which need to show about:blank other wise its help to attacker if victim open it in android webview then he will see title to and in site information also showing google.com

# Summary

site information change url to about:blank#<https://google.com>

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [blob (1).html](attachments/blob (1).html) (text/html, 1.1 KB)
- [screen-20240723-180036.mp4](attachments/screen-20240723-180036.mp4) (video/mp4, 1.4 MB)
- [screen-20240723-232027.mp4](attachments/screen-20240723-232027.mp4) (video/mp4, 6.2 MB)
- [Screenshot_20240724-230110.png](attachments/Screenshot_20240724-230110.png) (image/png, 2.8 MB)
- [Screenshot_20240730-223324.png](attachments/Screenshot_20240730-223324.png) (image/png, 2.7 MB)
- [screen-20240730-223314.mp4](attachments/screen-20240730-223314.mp4) (video/mp4, 4.7 MB)
- [screen-20240806-155927.mp4](attachments/screen-20240806-155927.mp4) (video/mp4, 2.8 MB)
- [screen-20250130-212333.mp4](attachments/screen-20250130-212333.mp4) (video/mp4, 10.1 MB)

## Timeline

### bh...@gmail.com (2024-07-23)

when u change it to pip  the url change to about:blank#https://google.com  which help attacker to spoof easily 

### ma...@chromium.org (2024-07-23)

[security shepherd]
Testing this on Android with a recent Chrome 128 build on Android, I see inconsistent results. The first time I attempt to reproduce, the address field shows `about:blank`. If I then attempt to reproduce it again, the address field shows `about:blank#http://www.google.com`. On my test device it is truncated so only `about:blank#http:` is visible.

Setting severity to S2 as this appears to be an address bar spoof with mitigating factors. I tested the most recent stable M125 Android build and the same behavior is observed so setting Found In to 125.

Assigning to ender@ as I see they've worked on Android omnibox issues in the past. Please feel free to reassign if someone else would be better suited.

### pe...@google.com (2024-07-24)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-24)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### en...@google.com (2024-07-24)

I'm not sure I understand the bug.

is it because the script overwrote the page title as "google.com"?

the url is very clearly exposed as "about:blank". i am not sure what the expected resolution for this is.?

### bh...@gmail.com (2024-07-24)

no  u will see when u click on website information its show about:blank#https://www.google.com also when u change it to pip mode the ur will change about:blank to about:blank#https://www.google.com and also title show google.com in canary  if we change about:blank url to little long in pip it will not show about:blank to 

### en...@google.com (2024-07-24)

i still don't understand. `about:blank#google.com` is still properly formatted and valid url. the address of the page is `about:blank`. `chrome://version#https://google.com` is also a valid url, but the domain is "chrome://version", not what comes after hash.

i don't have the clarity what the expected resolution for this is; side matter - it looks like this isn't an omnibox bug (if a bug at all) so it's not for me

### bh...@gmail.com (2024-07-24)

i think these bug  for who handling site information because omnibox show about:blank which is perfect but the site information show about:blank#https://www.google.com if u change the browser to minimize mode u will see title show google.com and the #https:www.google.com in that window  u can check my  last poc u need to tag site information handling team ori think custom tab team 
i i have tried chrome://version#google.com but in site information its show about:blank 

### bh...@gmail.com (2024-07-24)

see in canary its show site information url in that minimize window  if i use little long domain then it will show perfectly

### ma...@chromium.org (2024-07-24)

You're quite right that this is not an omnibox issue. I'm not sure why I routed it as such.

To restate, when the URL of a "custom tab" in PIP mode is displayed in a truncated form, it is truncated in such a way that the origin is hidden and only the fragment of the URL remains visible. This may mislead the user as to the origin of the website.

Sending to eirage@ as an owner of chrome/browser/android/customtabs/OWNERS.

### bh...@gmail.com (2024-07-24)

but there one more thing  if in site information its show about:blank then it will not show in pip the main root cause issue is that   so u need to assigne them who handle that site information  

### ei...@chromium.org (2024-07-29)

It's not the URL. The page has `<title>google.com</title>` and url about 
CCT displays the page title (google.com) on the first line and the url origin (about:blank) 

Looks like we do have something to prevent "about:blank" page, but maybe it doesn't apply to URLs with query parameters and anchors?
https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/customtabs/features/toolbar/CustomTabToolbar.java;l=1599

sinansahin@ do you mind take a look? 

### bh...@gmail.com (2024-07-29)

deleted

### bh...@gmail.com (2024-07-30)

hi u can see these is latest poc with the help of long url 
u will see title is there but where about:blank need to show its show www.google.com/account
canary version is vulnerable 

### bh...@gmail.com (2024-07-31)

#13 u said about:blank should not show display which is fixed few days ago if i use about:https://google.com its show in pip mode only about:blank no title comes  but in these report when i used about:blank#https://url then its show title and url in pip mode  when u open custom tab  click on url information but its show about:blank#url if u fix that to about:blank its fixed it 

### si...@google.com (2024-07-31)

Changing the priority and severity to match [b/353858776](https://issues.chromium.org/issues/353858776).

### si...@google.com (2024-07-31)

`UrlFormatter.formatUrlForSecurityDisplay(url, SchemeDisplay.OMIT_CRYPTOGRAPHIC)` returns `about:blank#https://url` here which may look like an actual URL if it's long enough and it's ellipsized at the start.

### bh...@gmail.com (2024-07-31)

yes thats what i said  i think its a medium serverity sinan u can see if  i use long url then in pip url will show if i open in simple way on browser   nd in content if i said user to check 
site information he will see its show about:blank#url so it will be more serverity nd risky issue too 

### bh...@gmail.com (2024-08-06)

hi there is one more thing i found out if u hold click me button and click on preview u will see on preview window url of window show the about:url 
check the poc 

### bh...@gmail.com (2024-08-12)

any update ? 

### bh...@gmail.com (2024-08-24)

deleted

### bh...@gmail.com (2024-09-05)

hi any update

### bh...@gmail.com (2024-09-13)

hi  any update 

### bh...@gmail.com (2024-09-25)

hi sinan any update  its been a long time no update yet 

### si...@google.com (2024-09-25)

Chris, do you have any suggestions based on #comment18?

### bh...@gmail.com (2024-10-15)

hey any update 

### bh...@gmail.com (2024-10-24)

hey any update ?

### en...@google.com (2024-10-25)

Hello Reporter. You will see an update here when there is one. Please be patient, while we work on more urgent matters.

Thank you

### bh...@gmail.com (2024-12-13)

okk   waiting for the update 

### bh...@gmail.com (2025-01-20)

any update

### am...@chromium.org (2025-01-23)

Please refrain from using comments for updates. S3 / low severity issues to not have an SLO, so there is no ETA for resolution nor should updates be expected at a specific time.
Comments should only and specifically for technical information that is specific to demonstrating the security impact or working toward resolution of the bug.
As mentioned in c#29, updates will appear here when there are som.
Thank you for refraining from future status update pings in the future.

### ap...@google.com (2025-01-30)

Project: chromium/src  

Branch: main  

Author: Sinan Sahin <[sinansahin@google.com](mailto:sinansahin@google.com)>  

Link:      <https://chromium-review.googlesource.com/6213069>

[MCT] Limit display of info on minimized card for about:blank

---


Expand for full commit details
```
[MCT] Limit display of info on minimized card for about:blank 
 
This CL ensures we only display the about:blank string on the minimized 
card and no arbitrary title or URL if the actual page is about:blank. 
 
Bug: 391784821,354882231 
Change-Id: I3eaeb0cb15773be31a03a314d3ea318b03a60db0 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6213069 
Reviewed-by: Chris Thompson <cthomp@chromium.org> 
Commit-Queue: Sinan Sahin <sinansahin@google.com> 
Cr-Commit-Position: refs/heads/main@{#1413259}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/customtabs/features/minimizedcustomtab/CustomTabMinimizationManager.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/customtabs/features/minimizedcustomtab/CustomTabMinimizationManagerUnitTest.java`

---

Hash: e5cc2f4721f2bd525c91429222c5d4141cb6834c  

Date:  Wed Jan 29 17:20:04 2025


---

### bh...@gmail.com (2025-01-30)

hi in new canary update these issue is fixed but what i see still there is a one issue i dont know for these should i need to report new bug or u guys can merge it there please check mine these poc video where still  about:blank#url comes

### bh...@gmail.com (2025-01-30)

hey these issue is fixed in canary why its first change to accept now its change to wont fix ? 

### si...@google.com (2025-01-30)

The issue with the minimized Custom Tab has been fixed, but this bug was originally filed for page info within the browser app. I was a little confused and listed this bug on my CL because the discussion has moved on to minimized CCTs.

I'm closing this as WAI because there is no spoofing on the omnibox itself, and the page info is showing the full URL as expected. Please reopen if you disagree.

### bh...@gmail.com (2025-01-30)

hey these bug is for custom tab also . check the #2 my poc  and #9 reply where i told custom tab team these need to be fix for custom tab its a security issue 

### bh...@gmail.com (2025-01-30)

i have already  opened another ticket for site information issue  

### bh...@gmail.com (2025-01-30)

even on comment#11 the component will change to custom tab  i hope u will change it to accepted and i got the reward cve for that because  these is mine best bug on custom tab where am able to change url in pip mode 

### bh...@gmail.com (2025-01-30)

hey why its serverity level change to s4  as i know its a low issue  in custom tab where attacker able to show arbitrary  url in pip mode 

### am...@chromium.org (2025-01-30)

Since a fix was landed in relation to this issue and report, I am shifting this from WAI to Fixed.
The fix was in Custom Tabs, so please refrain from submitting additional reports.
We do consider incorrect / spoofed origin information to be a security issue, however, a blank origin is not generally considered a security issue, there was no spoofing achieved here and no security boundary violated.
We will, however, review this issue at VRP panel to determine if there is a potential reward. When a decision has been made, an update will be provided here on the bug directly.

### bh...@gmail.com (2025-01-30)

see these https://issues.chromium.org/issues/353858776 one of my old report which is rewarded and its s3 and there title is showing in pip mode but in these bug which fix in custom tab in pip mode url is show about:blank#gooogle.com because of long url in pip mode its starting from google 

### am...@chromium.org (2025-01-30)

Yes, as acknowledged with the reward, this is an issue with very low potential for user harm and little potential for exploitability, but because a beneficial change was able to be made based on your report, we did issue a thank you reward.
We'll perform a similar assessment for this issue.

### bh...@gmail.com (2025-01-30)

yea  before the wont fix i am expecting to get more reward then these earlier report because these time able to add url to can u change the serverity to s3 

### bh...@gmail.com (2025-02-05)

any update 

### am...@chromium.org (2025-02-06)

Sorry, we weren't able to get to this one in panel this week. It should be assessed within the coming weeks. Thank you for your patience.

### bh...@gmail.com (2025-02-13)

okk waiting for the vrp pannel reward dicisson

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for a report of an issue with a very low potential for user harm and requiring the user to engage in a non-standard workflow to go back to full from minimized CCT as minimized CCT is not an interactable surface. We were able to make a beneficial change from this report, so we wanted to acknowledge that with a small reward.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Thank you for your efforts and reporting this issue to us.

### bh...@gmail.com (2025-02-25)

thanks for the reward for credit please put my name Bharat(mrnoob)

### ch...@google.com (2025-05-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/354882231)*
