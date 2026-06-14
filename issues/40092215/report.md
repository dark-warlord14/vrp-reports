# Chrome notification system permits to a domain to request permissions for each 3rd level domain with no restriction

| Field | Value |
|-------|-------|
| **Issue ID** | [40092215](https://issues.chromium.org/issues/40092215) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions>Prompts, UI>Notifications |
| **Platforms** | Linux |
| **Reporter** | al...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2018-08-17 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36

Steps to reproduce the problem:
1.Go to this link https://ovx5b.browsersecurely.com/index2.php?t=90&c=11&hash=5241408335b72b23&subid=52ed9gxuqoja23y801&url=https%3A%2F%2Ftralipon.tk%2Fclick.php%3Fkey%3Df8oncxh3s3cbfkns02fr&r=714671
2. Deny the consent to notification
3. Loop

What is the expected behavior?
Request stop after some redirects.

What went wrong?
The website ask to the user infinite amount of time the notification permission

Did this work before? N/A 

Chrome version: 68.0.3440.84  Channel: stable
OS Version: 
Flash Version: 

See the source of the html file
Regards

## Attachments

- [chrome_exploit.html](attachments/chrome_exploit.html) (text/plain, 27.6 KB)

## Timeline

### ca...@chromium.org (2018-08-18)

peter: Looks like this allows sites to ask for notification permission endless times, can you take a look?

In my opinion this wouldn't be a security bug (merely an annoyance), but keeping it as a low severity one just in case.

[Monorail components: UI>Notifications]

### ts...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### pe...@chromium.org (2018-08-28)

+Dominick for his opinion.

We're looking at requiring a user gesture for requesting notification permission, but other than that there's not a whole lot here that's immediately actionable...

### do...@chromium.org (2018-08-28)

Yeah, this is a notable crack in the web's permission model - that you can just redirect to different origins and request again. We'll need to make platform breaking changes (like requiring a gesture) , or do an browser intervention (e.g. throttle permission requests to N per minute) to address it.

Users should always be able to close the tab and leave the loop, making this less serious (though it's more annoying on Android where the permission prompt is modal).

+ some other permissions folks. The idea of throttling permission requests through the PermissionRequestManager has come up before and might be a good way to tackle this. We could simply rate-limit the number of requests that can be made per some time frame. If we want to be fancier, we can rate-limit per origin or per ETLD+1, but a global limit seems simpler - even having something like limiting to 1 request of the same permission per 10 seconds might be enough to take the teeth out of this sort of abusive site.

[Monorail components: UI>Browser>Permissions>Prompts]

### ts...@chromium.org (2018-08-29)

[Empty comment from Monorail migration]

### en...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### pe...@chromium.org (2019-12-06)

I'm going to close this as Fixed - the Reparo team introduced a restriction in M76 (IIRC) where this flow becomes infeasible: permission requests will be placed under embargo after the third dismissed request.

### pe...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-30)

peter@chromium.org - with regards to https://crbug.com/chromium/875503#c15, was that change in the initial M76 release? (I assume so, as opposed to in some subsequent respin). We'll need to allocate a CVE for this and amend the relevant release notes to credit this reporter. If you can provide a crbug number for the Reparo change that'd be great, but no worries if not.

### pe...@chromium.org (2020-01-31)

engedy@ - do you have that information handy?

### en...@chromium.org (2020-02-20)

The mitigation is tracked in crbug.com/900997. It was merged back to 74.0.3729.91. According to [1], the initial M74 release was a later revision than this.

[1]: https://chromereleases.googleblog.com/2019/04/stable-channel-update-for-desktop_23.html

### ad...@google.com (2020-03-09)

Thanks.

### [Deleted User] (2020-03-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-03)

alessio.dimaria@gmail.com, how would you like to be credited in the release notes here? Sorry for the delay in getting this properly credited!

### al...@gmail.com (2020-06-03)

you can put my full name: Alessio Di Maria

regards

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-03)

Thanks, will do.

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-08)

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

This issue was migrated from crbug.com/chromium/875503?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Permissions>Prompts, UI>Notifications]
[Monorail mergedwith: crbug.com/chromium/888219]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092215)*
