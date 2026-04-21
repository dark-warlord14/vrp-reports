# Security: Clickjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40056418](https://issues.chromium.org/issues/40056418) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Infra |
| **Reporter** | pt...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2021-07-04 |
| **Bounty** | $500.00 |

## Description

i found multi clickjacking vulnerability 

Clickjacking is an attack that tricks a user into clicking a webpage element which is invisible or disguised as another element. This can cause users to unwittingly download malware, visit malicious web pages, provide credentials or sensitive information, transfer money, or purchase products online

subdomain : developer.chrome.com

link : https://developer.chrome.com ,  https://developer.chrome.com/docs  ,  https://developer.chrome.com/blog"

code :

<html lang="en-US">
<head>
<meta charset="UTF-8">
<title>I Frame</title>
</head>
<body>
<h3>clickjacking vulnerability</h3>
<iframe src="https://developer.chrome.com/docs" height="550px" width="700px"></iframe>
</body>
</html>

save and run browser



impact:

Using a similar technique, keystrokes can also be hijacked. With a carefully crafted combination of stylesheets, iframes, and text boxes, a user can be led to believe they are typing in the password to their email or bank account, but are instead typing into an invisible frame controlled by the attacker

## Attachments

- [clickchromemain.png](attachments/clickchromemain.png) (image/png, 110.3 KB)

## Timeline

### [Deleted User] (2021-07-04)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-07-05)

Yes, looks like we could add an X-Frame-Options header here. But it is unclear if there is anything sensitive on that page that would warrant that level of protection.
(Reporeter: Note that the impact-none label I've added doesn't mean what you might think, just that it doesn't affect shipping chrome binaries)

dpranke@ - any idea who is responsible for developer.chrome.com ?

[Monorail components: Infra]

### pt...@gmail.com (2021-07-06)

Thankyou for the response 
impact none  ( * - * )
attacker create fake Hidden button and redirect  malicious web pages
like google fake login page etc , This can cause users to unwittingly download malware
and i have no idea who is responsible for developer.chrome.com



### pt...@gmail.com (2021-07-06)

issue triaged ? 

### dp...@google.com (2021-07-06)

robdsodson@, can you take a look?

### pt...@gmail.com (2021-07-07)

bug is not fix  
and my Question issue valid or not ?
thanks 

### ro...@chromium.org (2021-07-07)

We can take a look at adding that header.

### ro...@chromium.org (2021-07-07)

[Empty comment from Monorail migration]

### pt...@gmail.com (2021-07-08)

Any update ?

### ro...@chromium.org (2021-07-08)

I'm currently on vacation and so is Sam so it'll take us a bit to get to this. Because the security risk is low, it'll be prioritized with the rest of our backlog.

### pt...@gmail.com (2021-07-09)

Thanks for the response 
I will wait 
Thanks 


### th...@google.com (2021-07-20)

X-Frame-Options is now set. We also set the equivalent CSP header but we're still only in "content-security-policy-report-only" mode.

### pt...@gmail.com (2021-07-20)

Thanks

Any bounty ?

### [Deleted User] (2021-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-28)

Hello, the VRP Panel has decided to award you $500 for this report. A member of our finance team will be in touch in the coming days to arrange payment. In the meantime, please let us know how you would like this issue to be attributed or credited to you, such as the name/handle you would like used. Thank you again for your report!  

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-10-26)

This issue was migrated from crbug.com/chromium/1226373?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-05-20)

Hello reporter, the finance team has not received a response from you in their attempts to process your VRP reward payment. As is our policy, abandoned rewards are donated. So updating this issue to let you know we are doubling and donating this reward.

### pe...@google.com (2024-05-21)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### pt...@gmail.com (2024-05-21)

Sorry for the late thanks for reply
Pay me my reward through Bitcoin ( 15dqLQbuARZyXS32m1bGNpFMDkhd76ygmv) 

And pay me through usdt trc20 ( TVGFjiu1ziN2L1YoG5mck7HecbpFdeYajv ) 


Thanks

### am...@chromium.org (2024-05-21)

Sorry, we cannot pay through bitcoin, at this time.
Please reach out to [p2p-vrp@google.com](mailto:p2p-vrp@google.com) if you would still like to receive the reward, which would need to be via wire transfer.

### pt...@gmail.com (2024-05-22)

I send wire transfer details to this address p2p-vrp@google.com

On Tue, 21 May, 2024, 9:36 pm , <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/40056418
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #25
> <https://issues.chromium.org/issues/40056418#comment25>:*
>
> Sorry, we cannot pay through bitcoin, at this time. Please reach out to
> p2p-vrp@google.com if you would still like to receive the reward, which
> would need to be via wire transfer.
>
> _______________________________
>
> *Reference Info: 40056418 Security: Clickjacking*
> component:  Public Trackers > 1362134 > Chromium > Infra
> <https://issues.chromium.org/components/1456209>
> status:  Fixed
> reporter:  pt19278@gmail.com
> assignee:  ro...@chromium.org
> cc:  dp...@google.com, pt19278@gmail.com, th...@google.com
> type:  Vulnerability
> access level:  Default access
> priority:  P3
> severity:  S3
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-decline
> <https://issues.chromium.org/hotlists/5432432>, Security_Impact-None
> <https://issues.chromium.org/hotlists/5433277>
> retention:  Component default
> Chromium Labels:  allpublic, FoundIn-none
> Component Ancestor Tags:  Infra
> Component Tags:  Infra
> vrp-reward:  500
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 40056418
> <https://issues.chromium.org/issues/40056418> where you have the roles:
> reporter, cc, starred
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/40056418?unsubscribe=true>
>


### pt...@gmail.com (2024-05-22)

Any update? 
 I already send details to p2p-vrp@google.com

### am...@chromium.org (2024-05-22)

Hello -- we don't handle payments processing, the finance p2p-vrp team does.
They will need to email you with information to enroll you in the payments process.

### pt...@gmail.com (2024-05-22)

Thank you for your assistance.

On Thu, 23 May, 2024, 1:21 am , <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/40056418
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #28
> <https://issues.chromium.org/issues/40056418#comment28>:*
>
> Hello -- we don't handle payments processing, the finance p2p-vrp team
> does. They will need to email you with information to enroll you in the
> payments process.
>
> _______________________________
>
> *Reference Info: 40056418 Security: Clickjacking*
> component:  Public Trackers > 1362134 > Chromium > Infra
> <https://issues.chromium.org/components/1456209>
> status:  Fixed
> reporter:  pt19278@gmail.com
> assignee:  ro...@chromium.org
> cc:  dp...@google.com, pt19278@gmail.com, th...@google.com
> type:  Vulnerability
> access level:  Default access
> priority:  P3
> severity:  S3
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-decline
> <https://issues.chromium.org/hotlists/5432432>, Security_Impact-None
> <https://issues.chromium.org/hotlists/5433277>
> retention:  Component default
> Chromium Labels:  allpublic, FoundIn-none
> Component Ancestor Tags:  Infra
> Component Tags:  Infra
> vrp-reward:  500
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 40056418
> <https://issues.chromium.org/issues/40056418> where you have the roles:
> cc, starred, reporter
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/40056418?unsubscribe=true>
>


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056418)*
