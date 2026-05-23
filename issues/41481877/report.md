# Running JavaScript on file:// URI allowing to access information and access camera for iOS Chrome 

| Field | Value |
|-------|-------|
| **Issue ID** | [41481877](https://issues.chromium.org/issues/41481877) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Fundamentals>Security |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2022-4185 |
| **Reporter** | pr...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2023-12-07 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

30x redirect to javascript URI allows to run JavaScript on file:// Origin through the error page: <https://pwning.click/chrome302js.php>

We are able to run JavaScript on file:// URI from any https websites allowing to get UUID and other information accessible on file:// URI.

There are a few different ways to reproduce this, where 1 is the only case that requires user interaction.

1. Reloading the page with refresh.
2. Leave the page and coming back for browser pages reloading to automatically reproduce this issue.
3. Use simple crash bug to crash browser and come back which will reload pages and automatically reproduce this issue.

Additionally, we are able to pwn camera since user will think Chrome browser is asking for camera access after he/she came back to the browser after leaving: allow "" to use camera

<https://pwning.click/chrome302js2.php>

**Problem Description:**  

Running JavaScript on file:// URI allowing to access information and access camera for iOS Chrome

**Additional Comments:**

\*\*Chrome version: \*\* 120 \*\*Channel: \*\* Stable

**OS:** iOS

## Attachments

- [chrome302js.php](attachments/chrome302js.php) (text/plain, 83 B)
- [chrome302js2.php](attachments/chrome302js2.php) (text/plain, 300 B)
- chrome302js2.mp4 (video/mp4, 3.1 MB)
- chrome302js.mp4 (video/mp4, 2.2 MB)
- index.php (text/plain, 1.6 KB)
- [getcamera.js](attachments/getcamera.js) (text/plain, 2.5 KB)
- [camera302.php](attachments/camera302.php) (application/x-httpd-php, 607 B)
- [chrome302js_loc.php](attachments/chrome302js_loc.php) (application/x-httpd-php, 76 B)
- [chromeurl.php](attachments/chromeurl.php) (application/x-httpd-php, 319 B)
- [chromeurl_t.php](attachments/chromeurl_t.php) (application/x-httpd-php, 248 B)
- [RPReplay_Final1707244801.mp4](attachments/RPReplay_Final1707244801.mp4) (video/mp4, 9.7 MB)
- [media_tester_t.php](attachments/media_tester_t.php) (application/x-httpd-php, 253 B)
- [media_tester.php](attachments/media_tester.php) (application/x-httpd-php, 476 B)
- [RPReplay_Final1707264474.mp4](attachments/RPReplay_Final1707264474.mp4) (video/mp4, 7.1 MB)
- [RPReplay_Final1707337436.mp4](attachments/RPReplay_Final1707337436.mp4) (video/mp4, 3.3 MB)

## Timeline

### [Deleted User] (2023-12-07)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-12-07)

Can you please provide more details on the vulnerability? Where does file:// come into this? What are the specific steps to reproduce?

### pr...@gmail.com (2023-12-08)

Ok, I'll try to explain it better. When we 302 redirect to javascript: URI, iOS Chrome gives us error page on file:// URI so with "There are a few different ways to reproduce this, where 1 is the only case that requires user interaction." on main report, we are able to run JavaScript on file:// URI and take over Camera permission since "Allow "" to use camera" will pop up out of no where from iOS Chrome after your device is woke up from sleep.


### pr...@gmail.com (2023-12-08)

[Comment Deleted]

### pr...@gmail.com (2023-12-08)

If you don't have time to let your device sleep and wake up or no crash bug to test 2 and 3, please just reload it with iOS Chrome refresh to reproduce https://pwning.click/chrome302js.php and https://pwning.click/chrome302js2.php

### bo...@chromium.org (2023-12-08)

Please upload the POC to this report so we can host the POC locally. 

Per https://crbug.com/chromium/1509267#c2, please also include the precise sequence of steps someone needs to follow to reproduce the issue; be sure to be specific. The instructions in https://crbug.com/chromium/1509267#c1 and https://crbug.com/chromium/1509267#c5 don't have enough detail for us to be able to confidently reproduce the issue. What do we have to do to run the POC? What steps does the user have to take to trigger the issue after navigating to the POC? 

### bo...@chromium.org (2023-12-09)

Setting next action date to 11 December (US/Pacific). 

### [Deleted User] (2023-12-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@gmail.com (2023-12-09)

Like I already mentioned few times, just reload the page with refresh if you don't have time to let your iOS device to sleep for a while and come back to your browser.



### pr...@gmail.com (2023-12-09)

[Empty comment from Monorail migration]

### pr...@gmail.com (2023-12-09)

I couldn't attach video demos with letting device sleep for a while and wake up to reproduce this without user interaction and recording front, rear camera to send together with screenshots of them to attacker's server due to Max 10.0 MB size limit.

### bo...@chromium.org (2023-12-09)

Please upload the contents hosted at https://pwning.click/access_camera

### pr...@gmail.com (2023-12-09)

Please create access_camera directory and upload index.php under https://mydemosite.com/access_camera/ 

### [Deleted User] (2023-12-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2023-12-11)

@clamy, do you think you can route this issue to an appropriate owner? I'm unfortunately not able to reproduce the issue because I don't have access to an iOS device. This feels like a Web Content Security issue, but I'm not sure which area precisely. 

I'm tentatively setting triage flags as though this were a valid bug that allows web content to somehow be run from the file:// scheme. 

The camera permission prompt is probably best treated as a separate issue. 

[Monorail components: Blink>SecurityFeature]

### [Deleted User] (2023-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-12-12)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-12-21)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@gmail.com (2023-12-25)

We need someone who could test and confirm these issues with iOS device.

### [Deleted User] (2024-01-05)

clamy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### aj...@chromium.org (2024-01-30)

Perhaps we should just block all renderer-initiated navigations to javascript: URLs. I assume we need to support browser-initiated navigations for bookmarklets.

[Monorail components: -Blink>SecurityFeature Mobile>Fundamentals>Security]

### pr...@gmail.com (2024-01-30)

Thanks, I hope I'll have enough time to explore them before the fix :)

### gi...@appspot.gserviceaccount.com (2024-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ca4744673af3cab864762613ada06b03819dd69

commit 8ca4744673af3cab864762613ada06b03819dd69
Author: Mike Dougherty <michaeldo@chromium.org>
Date: Fri Feb 02 20:25:36 2024

Prevent redirect to Javascript scheme URL

Fixed: 1509267
Change-Id: I1dfabb259214291ce0e5e120ce0feca0746adc45
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5262999
Reviewed-by: Ali Juma <ajuma@chromium.org>
Commit-Queue: Mike Dougherty <michaeldo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1255730}

[modify] https://crrev.com/8ca4744673af3cab864762613ada06b03819dd69/ios/web/navigation/crw_wk_navigation_handler.mm


### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1509267?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pr...@gmail.com (2024-02-05)

Just for the note, I have to provide Camera PoC that works independently without https://issues.chromium.org/issues/40945830 to prove the camera part here is a separate issue, which will be done soon.

I also need to report other bugs with different impact that works from "" origin with error_page.html so please give me some time until all of them is done.

### pr...@gmail.com (2024-02-06)

We can reproduce this again with same steps on latest iOS and Chrome: https://pwning.click/camera302.php

### pr...@gmail.com (2024-02-06)

And this is showing where we're located, leaking UUID and accessing file URI: https://pwning.click/chrome302js_loc.php

### pr...@gmail.com (2024-02-06)

We can access to Privileged URLs like chrome:// and about:// through domainless world.

1. Open https://pwning.click/chromeurl_t.php and Tap on Cat.

2. Wait until google.com is loaded and just go back to tap on Cat.

*This impact alone* is already High Severity like https://issues.chromium.org/issues/40054421

### pr...@gmail.com (2024-02-06)

For the clear record, asking to add ajuma for the progress and the fix suggestion from my side was on here:  https://issues.chromium.org/issues/41495552#comment4  

### pr...@gmail.com (2024-02-06)

I clearly mentioned to add ajuma in the main report of https://issues.chromium.org/issues/41495552 to this report https://bugs.chromium.org/p/chromium/issues/detail?id=1509267 with the fix suggestion on  https://issues.chromium.org/issues/41495552#comment4 

It's only fair to let me further prove the ultimate impact of this report because of this reason.

### pr...@gmail.com (2024-02-07)

This duplicate issue https://issues.chromium.org/issues/41496159 allows to run all permissions including camera and microphone as any origin.

1. Please tap on Cat: https://pwning.click/media_test_t.php

2. Wait until you're located to https://google.com and just go back twice.

### pr...@gmail.com (2024-02-07)

Tested on latest 17.3 and Chrome.

### am...@chromium.org (2024-02-07)

Hi James, as I explained over email in response to your inquiries , while we see your effort in trying to provide additional POCs and we appreciate this. These sorts of details from comment #30 and after are best provided up front as part of the initial report or as fast follow-up to help us in security appropriately assess and triage the issue and for engineering team to investigate and resolve it. These sorts of follow-ups after the issue is resolved are only fully impact and helpful if you are demonstrating how the fix does not truly mitigate the issue and can by bypassed. 

This issue is out of the hands of the engineers now since they have resolved it. The next place for evaluation is for the Chrome VRP Panel, which as I communicate to you already, will soon be reviewing your issue and we, as always, will directly and openly communicate the reward amount and the factors going into that decision directly on bug. The VRP Panel only meets once a week. In the meantime, have patience until that point that we can review and communicate a reward decision to you here. 


### pr...@gmail.com (2024-02-07)

I requested the fix, these proof on latest were already sent in  https://issues.chromium.org/issues/41496159  and I'm proving this work. Also I have a complete PoC demo with video before the fix happened which I couldn't update because of finger injury, as I can't just upload video with no explanation.

How is this a fair situation if the whole fix process was done by me taking an action and I'm not allowed to elaborate further impacts I already discovered before the fix but couldn't add due to injury?

https://issues.chromium.org/issues/41481877#comment27 my intention here was to add it all in upcoming 1~2 days but I had to delay everything due to my finger injury and that's the reason of time gap where I came back on Feb 6th for the other report. 

### pr...@gmail.com (2024-02-07)

Camera and Microphone take over on any origin where in real world attack scenario it's camera pwn with no restriction through legitimate video chat sites like skype. facetime, zoom.

Reproducing all of these issues are same to https://issues.chromium.org/issues/41495552 waiting to be loaded and just go back, twice in this test case. 

### pr...@gmail.com (2024-02-07)

Those demo videos will prove my point as we can see the date on it.

I requested the fix and that happened, I don't even have a right to make bugs I found get into account to the panel just because I was not able to type until about 2 days after the fix which is already happened?

I don't know how many times I'm emphasizing this but I added ajuma@ and that's the ONLY reason why this was even fixed on Feb 3! reporter should've full right to add details he couldn't, let alone finger injury since that's my fault.

I also think duplicate reports are not going to be checked and missed if I don't mention all together here.

Again, I didn't say anything about vrp is being unfair, it's just that the situation here I'm experiencing is unfair because of reason I stated.

### pr...@gmail.com (2024-02-07)

This should be seen as exception scenario because the fix on Feb 3 happened as I added ajuma@ who brought appropriate engineer for this.

You told me Alesandro case is very different to my case https://bugs.chromium.org/p/chromium/issues/detail?id=1311820

indeed it's different, more than a month of waiting was granted for him which is good but now that doesn't apply to me because of some wrong assumptions like me not providing details on initial report-- there was no one with iOS device to test it, while reproduce step was so simple like other 302 redirection issue https://issues.chromium.org/issues/40054421

Isn't Full UXSS higher impact and grants reward of $20000? why can't I prove that with extra time like Alesandro and S case? let alone you told me that elaborating already mentioned reports will not be taken into account neither.

By the way, this need to be under the embargo since this is Full UXSS on Webkit Safari and Firefox Focus! could you please check my final email?

I also want this to get settled and no more discussion so I can prove my point with already done Jan dated demo videos and explanation.


### pr...@gmail.com (2024-02-08)

*Timeline update*

https://issues.chromium.org/issues/41481877#comment27

"Thanks, I hope I'll have enough time to explore them before the fix :)"

For the record, I got my right hand index finger injured about 8 hours after that comment iirc, I was not able to type many words from Jan 31 ~ Feb 5 which is why there is almost no update since that comment until Feb 5, as I can't just upload demo videos and PoCs with no explanation.

Yes, it is my fault and not to be used as an excuse but I also had situation like him https://bugs.chromium.org/p/chromium/issues/detail?id=1311820 but I had to rest my finger as long as possible during then, I'm still not completely recovered but much better as you can tell by my typing.

Even without this unexpected situation, the fix is pushed by my action so everything I add after the fix should be taken into account as well. Other vendors all accept this EVEN after a few months or the fix is solely from them not me. In this case, I brought ajuma and asked to fix by blocking javascript 302 redirection and added https://issues.chromium.org/issues/41481877#comment27 before the injury.

I'll update the rest after this is checked since they might blind this comment.


### am...@google.com (2024-02-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pr...@gmail.com (2024-02-08)

Yeah, another 1000$ throw away update. With no update on my comment, I reject the bounty this all together can worth up to $20000. I'll consider full disclosure after sharing promised remaining details. I'll let people to reproduce this.

CVE-2022-4185 https://issues.chromium.org/issues/41495552 replication report alone could be worth $5000 here, everything is reported BEFORE the fix.

I won't further participate chrome bounty from now on with this kind of communication problem too, I guess no one cares about that anyway and that means I might decide to full disclose all of my future findings too.

### am...@chromium.org (2024-02-08)

Hello, James -- the Chrome VRP Panel has decided to award you $1,000 for this report of an information disclosure. The reward amount based on the limited security impact and user harm presented from this issue. While this issue could potentially result in the loading of an arbitrary file url, the attacker would not be able to execute javascript in the new file url, nor can the attacker access any previously opened files so while there is an user information disclosure there is minimal impact presented from it. 
Examples of previous VRP reports of issues with similar impacts are crbug.com/40095183 and crbug.com/40052526. 

In general, it's important that we communicate a couple of other points here: 
1) VRP reports bug reports should be clear and concise, providing security impact and demonstrated through a reproducible test case or steps to reproduce. 
This is clearly defined in our VRP policies (https://g.co/chrome/vrp)

2) One report should be submitted per root cause, if there are multiple impacts per a given bug::root cause, that should be clearly explained in an organized fashion in the original report or in a quick follow-up, not in a series of unclear comments submitted over the course of days and weeks after the report is submitted and definitely before the bug is resolved. 
The exception here is a functional exploit; a functional exploit can be provided after the issue is fixed for additional / higher reward consideration, even after the initial VRP reward assessment. 

We aim to be as fair (and even generous) as possible with VRP rewards, but at the end of the we can only reward the report proportional to the impact and quality of the issue reported to us and how much of what was reported was used in investigating and resolving the issue as swiftly as possible.

Thank you for your efforts and reporting this issue to us as well as taking the time to review and consider this feedback. 


### pr...@gmail.com (2024-02-08)

2) One report should be submitted per root cause, if there are multiple impacts per a given bug::root cause, that should be clearly explained in an organized fashion in the original report or in a quick follow-up, not in a series of unclear comments submitted over the course of days and weeks after the report is submitted and definitely before the bug is resolved.
The exception here is a functional exploit; a functional exploit can be provided after the issue is fixed for additional / higher reward consideration, even after the initial VRP reward assessment.

> they haven't been checked, my quote from above "CVE-2022-4185 https://issues.chromium.org/issues/41495552 replication report alone could be worth $5000 here, everything is reported BEFORE the fix."

no origin permission requests were ignored too, which was rewarded $3000 way before: https://issues.chromium.org/issues/40057508

> We aim to be as fair (and even generous) as possible with VRP rewards, but at the end of the we can only reward the report proportional to the impact and quality of the issue reported to us and how much of what was reported was used in investigating and resolving the issue as swiftly as possible.

It's no where near fair let alone generous, for my situation *even we consider only bugs I provided before the fix*. vrp is fair, it's not for this situation.

I'm currently exhausted with all of this so let me refresh and come back.

### pr...@gmail.com (2024-02-08)

Summary: duplicate reports and camera case were not factored in for the reward amount on this report: https://issues.chromium.org/action/issues/41481877/attachments/53180723?download=true, https://issues.chromium.org/issues/40057508, https://issues.chromium.org/issues/41496159

They were both sent on Jan while the fix was on Feb 3 but they were not factored in for the reward with the camera and other permission case which is same impact to this $3000 report: https://bugs.chromium.org/p/chromium/issues/detail?id=1255713

I'd like this to get reassessed too. 

Again, I'm having a lot of patience here before giving up everything. Not sending in email anymore since you told me your perspective and categorized my action as spamming.

This need to be under the embargo since this is Full UXSS on Safari and Firefox product with simple trick!

Communication is completely broken here.

If other thing than impacts I've proven is not the only factor for reward process but showing bias toward reporter keep stating false fact that I did not report full details on #c1 while the truth was that this report was not understood by not following the step on #c1, this is a faulty bounty program for some reporters like me with this case. I understand this is probably not your intention and they were not checked but they're keep being forgotten and never getting addressed together with this report: https://issues.chromium.org/issues/40057508, https://issues.chromium.org/issues/41496159


It is frustrating that factors besides impact can play a major role when deciding the reward amount for similar issues like $5000 rewarded 1495521 https://issues.chromium.org/issues/40075537 (actually, this camera one is even worse than that my $5000 rewarded report) under Chrome's VRP which is wide range of arbitrary amount.



### am...@chromium.org (2024-02-20)

when I merged [issue 323898905](https://issues.chromium.org/issues/323898905) into this issue as a duplicate, this issue seems to have inherited hotlists from that issue
removing hotlists security and triage related hotlists that do not apply here

### pr...@gmail.com (2024-02-29)

https://issues.chromium.org/issues/41481877#comment1

https://issues.chromium.org/issues/41481877#comment4

I already explained this works because we are running from file:// URI where location.origin is file:// but document.domain is empty "" origin, which is "domainless world" like I mentioned, allowing to request any permissions with no origin "" including the most serious permission like Camera.

But vrp did not consider that part and only assessed approaching to file:// URI location one telling me it's not clear if this is same bug or different one while I clearly explained above that this is all possible because we're runnning on file:// origin which has a document.domain of "".

### pe...@google.com (2024-05-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41481877)*
