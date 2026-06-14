# Wrong origin shown for permission prompts after navigations that lead to interstitials

| Field | Value |
|-------|-------|
| **Issue ID** | [40089597](https://issues.chromium.org/issues/40089597) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Interstitials, UI>Browser>Permissions>Prompts, UI>Notifications |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2017-11-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.40 Safari/537.36

Steps to reproduce the problem:
1. Open PoC: http://t.cn/RjJursh
2. Click link, wait a moment

When we open a domain(jacking target) with invaild security certificate in a new window, url and page content have changed, but document.domain is not changed, this is the first issue.

According to this issue, We use setTimeout method to make the delay of triggering the browser UI notification, It looks like the site we jacking is asking notification permission.

The next issue is when we request a domain with long domain name, It will cut the part go beyond the window. That make a hacker can be enable a uijacking.

Together the two issues above, we can do as the video.

What is the expected behavior?
The chrome will not notifi in the target domain.

What went wrong?
ui jacking

Did this work before? N/A 

Chrome version: 63.0.3239.40  Channel: beta
OS Version: OS X 10.12.6
Flash Version: Shockwave Flash 27.0 r0

This PoC is cross platform despite UI behavior maybe vary, with minor modification it will work.

## Attachments

- [chrome_notification_uijacking.jpg](attachments/chrome_notification_uijacking.jpg) (image/jpeg, 22.6 KB)
- [chrome_notification_uijacking.mov](attachments/chrome_notification_uijacking.mov) (application/octet-stream, 11.5 MB)

## Timeline

### mm...@chromium.org (2017-11-15)

peter@, could you please help to find an owner for that?

[Monorail components: UI>Notifications]

### pe...@chromium.org (2017-11-16)

There's two issues here:

1) The document's domain not being updated for interstitial pages. +Chris
2) UI eliding behaviour for the permission request window. +Raymes

It does look like we're eliding on the left-hand side rather than the right-hand side, which means display of the important bits (i.e. the eTLD+1) is preserved.

### pa...@chromium.org (2017-11-16)

The origin elision behavior seems wrong in a weird way. The attack page is:

  https://t.longcabiltudinitatibus.expired.badssl.com.n0tr00t.com/test.html

whose code is:

```
<html>
<body>
<script>
    pwn = () => {
        x = open('https://expired.badssl.com/', '_self');
        setTimeout(`
            Notification.requestPermission(function(){});
            `
            ,3000);
    }
    setTimeout('pwn()', 100);
</script>
<a onclick="pwn()">Click Me</a>
</body>
</html>
```

yet the permission prompt shows "t.longcabiltudinitatibus.expired.badssl.com". So that's wrong.

I also would assume the navigation problem would exist on all platforms, since that's platform-neutral code? (Uncheck if not the case.) +nasko, creis, clamy for navigation thoughts.

[Monorail components: UI>Browser>Interstitials UI>Browser>Permissions>Prompts]

### pa...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### pe...@chromium.org (2017-11-16)

> The origin elision behavior seems wrong in a weird way.

Doh, clearly got me. Sorry for not being thorough enough.

### ra...@chromium.org (2017-11-20)

Dom just landed a patch to address origin elision in permission prompts in https://crbug.com/chromium/774438. dominickn@ could you confirm that your patch would fix the problem here?

The other issue is the more concerning one though. JavaScript from the previous navigation is still being run after the navigation to the interstitial. I don't think that should happen in general. dominickn@ mentioned this was possibly related to the fact that interstitial aren't committed fully and that this is something we're fixing. estark@ do you know if that's true?

### do...@chromium.org (2017-11-20)

https://crbug.com/chromium/774438 is the permission prompt elision bug and that should be fixed by crrev.com/c/768312, which elides the title of the permission prompt from the head and restricts it to one line. The has the effect of ensuring that prompt titles which are too long will cut off the starting text, leaving the end of the line (i.e. the ETLD+1) alone.

As c#6 said, I suspect that the weird origin is because the interstitial error page for expired.badssl.com is an overlay and not a fully committed navigation.

### es...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-12-01)

c6,7 are correct about the interstitial overlay. Should be fixed with the interstitial refactor, if we're willing to wait for that... estimate is M65 for SSL interstitials, maybe M66 for Safe Browsing.

### ev...@gmail.com (2018-01-24)

Hi, What is the present processing stage?


### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-02-21)

Hi, Has the vulnerability been fixed.

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-04-09)

hi, has it been fixed?



### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-09-28)

delay...

### do...@chromium.org (2018-09-28)

Committed interstitials are in limited release now. +carloslil for a check on progress.

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### ra...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### ev...@gmail.com (2019-04-12)

[Comment Deleted]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-08-21)

Committed SSL interstitials have since fully launched, keeping the bug open until SB committed interstitials launch, since those are technically also affected.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-03-06)

Committed interstitials now have also launched for SB 

### [Deleted User] (2020-03-07)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-09)

carlosil@ as this is externally reported, I need to credit this in the release notes for some Chrome version. What version did committed interstitials launch in? Thanks!

### ca...@chromium.org (2020-03-09)

since this also affected SB interstitials, it wasn't completely fixed until 80.

### ad...@chromium.org (2020-03-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-09)

Thanks. I will eventually add it to the release notes and add a CVE. It may take me some weeks as it's outside the normal processes.

### na...@google.com (2020-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-11)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-03-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

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

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/785159?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Interstitials, UI>Browser>Permissions>Prompts, UI>Notifications]
[Monorail blocked-on: crbug.com/chromium/448486]
[Monorail mergedwith: crbug.com/chromium/137220, crbug.com/chromium/903056]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089597)*
