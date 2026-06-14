# SameSite cookies leakage via child browsing context

| Field | Value |
|-------|-------|
| **Issue ID** | [40091690](https://issues.chromium.org/issues/40091690) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | mo...@chromium.org |
| **Created** | 2018-06-18 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : 66.0.3359.181 (Official Build) (64-bit)  

**URLs (if applicable) :** [http://cm2.pw/xss?xss=%3Ciframe%20style=%27width:100%;height:500px%27%20src=%27http://cm3.pw/httpleaks/child.html%27%3E%3C/iframe%3E](javascript:void(0);)

**Other browsers tested:**  

Firefox: OK (version: 61.0b14 (64-bit))

There are two issues here;

1. SameSite "Lax" cookies being sent to nested browsing contexts
2. SameSite "Strict" cookies being sent on pressing back button

The reproduction steps are as follows;

1. Visit [http://raw.cm2.pw/cookies/cookies.php?url=%0dlocation=`http://cm2.pw/xss?xss=%3Ciframe%20style=%27width:100%;height:500px%27%20src=%27http://cm3.pw/httpleaks/child.html%27%3E%3C/iframe%3E`//](javascript:void(0);)

- Here, cookies.php sets 3 cookies- normal, SameSite Strict and SameSite Lax. Using following curl command can reveal what's being done;  
  
  $ curl -i <http://raw.cm2.pw/cookies/cookies.php>
- Then, it redirects to [http://cm2.pw/xss?xss=%3Ciframe%20style=%27width:100%;height:500px%27%20src=%27http://cm3.pw/httpleaks/child.html%27%3E%3C/iframe%3E](javascript:void(0);)
- Here, the top-level browsing context is 'cm2.pw' and its direct child browsing context is an iframe whose src is '<http://cm3.pw/httpleaks/child.html>'. The "child.html" of 'cm3.pw' loads another 3 child frames, all of which references to resources from 'raw.cm2.pw' i.e.  
  
  cm2.pw -> cm3.pw (iframe) -> raw.cm2.pw (3x frames)

2. You should already see SameSite "Lax" cookies in each frame (RAW HTTP request is being dumped in response)
3. Press "ANCHOR" link below the frame
4. Press back button or Alt + <-
5. Now, you should see all cookies in each frame

I'm not sure why `history.back()` is not working, while it works in Firefox. If history.back() works somehow, it wouldn't need any user-interaction at all. All that is required is- victim site allowing framing of arbitrary URL.

**What is the expected result?**  

SameSite cookies shouldn't have been sent at all

**What happens instead?**  

SameSite cookies sent

## Attachments

- [child.png](attachments/child.png) (image/png, 59.0 KB)
- [child2.html](attachments/child2.html) (text/plain, 913 B)
- [cookies.php](attachments/cookies.php) (text/plain, 976 B)
- [SameSite-cookies.png](attachments/SameSite-cookies.png) (image/png, 146.5 KB)

## Timeline

### mk...@chromium.org (2018-06-18)

Reporter asked for this to be restricted.

### pr...@gmail.com (2018-06-19)

Okay! I have made it to work with history.back() which almost requires no user-interaction. So, if you visit (Note, it's 'child2.html');
http://cm2.pw/xss?xss=%3Ciframe%20style=%27width:100%;height:500px%27%20src=%27http://cm3.pw/httpleaks/child2.html%27%3E%3C/iframe%3E

And hover your mouse over parent iframe's body, it redirects you to http://bughuntersclub.ipage.com/rm/xss?xss=%3cscript%3ehistory.back()%3c/script%3e which just sends you back with history.back(). To avoid infinite loop, I've made use of history.replaceState(), so it will only happens once (the mouseover thing).


### bo...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>SecurityFeature Internals>Network>Cookies]

### oc...@chromium.org (2018-06-20)

mkwst, would you be able to take this one, or help with finding someone to?

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### pr...@gmail.com (2018-06-22)

Further note: "Print Preview" also has same behavior

### sh...@chromium.org (2018-07-02)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-16)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2018-08-02)

Mike, friendly ping from the security sheriff :) Maybe there is someone else whom you can assign this to?

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-12-11)

Misha, could you please help to find an owner here as per c#13? Thanks a lot!


### me...@chromium.org (2018-12-21)

Maks, could you assess what needs to be done?

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this? Are you able to reproduce the bug?

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### mo...@chromium.org (2019-09-16)

Apologies for missing this for so long. Managed to miss the email due to its timing, until I was pinged about it.

Sadly the testcase seems down..

### pr...@gmail.com (2019-09-24)

Sorry! I also missed the notification email too.

Yeah, I got rid of cm3.pw. Thus, I'm attaching the POC files so that you can reproduce it locally.  What you need to do is;

- Change your /etc/hosts file and make cm3.pw point to 127.0.0.1
- Tweak the URL as required for cm3.pw (replace child.html with child2.html)

So, basically you'll want to visit;
http://raw.cm2.pw/cookies/cookies.php?url=http://cm2.pw?xss=<iframe%20style=%27width:100%;height:500px%27%20src=%27http://cm3.pw/child2.html%27></iframe>

** if you put child2.html directly under your http root.

I hope you're able to reproduce the issue. If you need anything else or have any questions, please let me know.

### mo...@chromium.org (2019-09-25)

Had to just use 127.0.0.1 in the testcase to get it to run, since something seems to rewrite http://cm3.pw -> https://cm3.pw  on server end, but the result looks sane --- cookies just have:
normalHeader=true; normalScript=true (as well as some UIDish thing).   This is both on a trunk build and 78.0.3904.21 beta.



### pr...@gmail.com (2019-09-26)

Maybe, you could use some other hostname which doesn't have HSTS preload enabled. You should not only see normalXXX cookies but rather all cookies i.e laxXXX as well as strictXXX cookies. The UIDish things could be Cloudflare adding their cookies.

### mo...@chromium.org (2019-10-02)

Not seeing the bug when using an alternative hostname, either; testing on:
78.0.3904.34 (Official Build) beta (64-bit)

### pr...@gmail.com (2019-10-05)

I see the behavior has changed. It no longer sends cookies even when framed under same domain (see screenshot). Though, that would not be a security issue, I guess.

### mo...@chromium.org (2019-10-07)

Well, it's inside localhost, isn't it? All the frames have to match..

### me...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### pr...@gmail.com (2019-10-11)

Re https://crbug.com/chromium/853670#c31, The main frame is under localhost while all other 3 frames are under raw.cm2.pw. So, the requests should be same-domain, I guess. I don't what you mean by all frames have to match. 
The POC uses localhost as main domain which has an iframe pointing to raw.cm2.pw which has 3 frames which all again points to raw.cm2.pw. So, the 3 frames match with requesting frame's origin, don't they?


### mm...@chromium.org (2019-10-11)

htttp://localhost/ is not the same origin as http://raw.cm2.pw/.  Origin is scheme+domain+port.  Note that if domains map to the same IP they are still not the same origin.

### mo...@chromium.org (2019-10-11)

re: https://crbug.com/chromium/853670#c33: since the first raw.cm2.cw iframe doesn't match localhost, everything below it is considered not-same-site.
See https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-03#section-5.2
in particular how it looks at all the ancestors.


### pr...@gmail.com (2019-10-12)

Okay! That makes sense. Thanks for the clarification.

### pr...@gmail.com (2019-10-17)

I guess, we can close this out. Just wondering about the bounty.

### mm...@chromium.org (2019-10-17)

I defer to the security team on how that works, but I think security bugs are reviewed for that only after they've been marked as fixed.

### sh...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

mmenke@ morlovich@, was there actually any fix here? If so, we should consider merge to M78. If not, please can you switch the status to WontFix?

prakash0x00@ - this will go to the VRP panel if there was an actual fix here, but to me it doesn't look like there was. Thanks for the report nevertheless though!

### mm...@chromium.org (2019-10-18)

[morlovich]:  You have much more context here, so I'm deferring to you.

### na...@google.com (2019-10-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-22)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M78. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-22)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mo...@chromium.org (2019-10-22)

I have no idea on what fixed it, but it looked already fixed in M78 when I tested in https://crbug.com/chromium/853670#c29.


### go...@chromium.org (2019-10-22)

+adetaylor@, for Android we're ready to go with M78 stable promotion, We can take this merge in for next M78 respin if safe and needed. 

### go...@chromium.org (2019-10-22)

Per https://crbug.com/chromium/853670#c45 it is already fixed in M78 so merge may not be needed. 

### ad...@google.com (2019-10-23)

govind@ and I discussed this - please can we verify on the current stable build (78.0.3904.70 for desktop, or .62 for Android). Assuming that's all fine, there's no need to merge this anywhere.

### na...@google.com (2019-10-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-23)

Congrats! The Panel decided to award $1,000 for this report :) 

### pr...@gmail.com (2019-10-24)

Re https://crbug.com/chromium/853670#c48, I can confirm it's been fixed. And, thanks for the bounty :)

### ad...@chromium.org (2019-10-24)

Thanks for the verification prakash0x00@!

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

Looks like this was fixed in M78 or earlier, but I'm going to include it in the release notes for M79 so that it's properly credited somewhere. Thanks prakash0x00@ again for the report.

### ad...@google.com (2019-12-06)

prakash0x00@ how would you like to be credited in the Chrome release notes?

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### pr...@gmail.com (2019-12-06)

Re #55, as
Prakash (@1lastBr3ath)

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/853670?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091690)*
