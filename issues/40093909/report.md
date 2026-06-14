# Github Wiki Pages for GoogleChrome are publicly editable.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093909](https://issues.chromium.org/issues/40093909) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Infra>Git |
| **Reporter** | mk...@gmail.com |
| **Assignee** | je...@chromium.org |
| **Created** | 2019-01-31 |
| **Bounty** | $500.00 |

## Description

Github.com wikis are editable by anyone

https://github.com/GoogleChrome/webstore-docs/wiki/Hello-google-mkzreport@gmail.com

and many others... 

Can be edited by any logged in user in the system. This poses security and reputation risk for the company. 
As wikis listed above can be edited by any person on the internet, a malicious actor can accurately craft a message or a note which would lead a user to download a malicious component in a natural way.

The user would surely trust the code (of course if he trusts the company itself), so he will extrapolate this trust to the wiki and consider it being safe enough to follow the instructions and downloading himself a malware.


## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### me...@chromium.org (2019-01-31)

Thanks for this report.

I can confirm that the page was edited by you. I deleted it.

However, in the future, please don't actually perform the attack you are describing when reporting one. 
Proof-of-concept attacks against one's self are good, but in this case you actually did the attack against someone who did not agree (us) and publicly. 
A better way to demonstrate that this attack is possible would have been to instruct us to edit the page as an unauthenticated user and confirm for ourselves that it is possible.

dpranke@ Do you have control over the GoogleChrome repos?
jyasskin@ I see you are a member of the GoogleChrome Github org, do you have control?

We should probably lock down any other repos associated with Chrome/Google, since this issue was reported for other repos in https://crbug.com/chromium/918454.


[Monorail components: Infra>Git]

### jy...@chromium.org (2019-01-31)

https://github.com/orgs/GoogleChrome/people?utf8=✓&query=+role%3Aowner lists the org's owners, so I'll cc one.

It probably makes sense to turn off the github wiki for any repo that isn't actively using it. The "Restrict editing to users in teams with push access only" setting might be appropriate for repos that do use their wikis, although it might also make sense to decide that wikis are expected to be publicly editable.

### dp...@chromium.org (2019-01-31)

Ah, I had disabled all of the wikis for the 'Chromium' project. I didn't know (forgot?) we also had a 'GoogleChrome' project also.

We should disable the wikis there as well.

@ericbidelman / @jyasskin - if you can make me an owner for the project I can do that and also make the other ops Git admins owners as well, which they should be (but aren't).

### jy...@chromium.org (2019-01-31)

+Chris in case the WICG should make the same change.

(I can't do anything anywhere since I'm not an owner.)

### me...@chromium.org (2019-01-31)

Thanks everyone!

### mk...@gmail.com (2019-02-07)

[Comment Deleted]

### dp...@chromium.org (2019-02-07)

+paulkinlan, +paulirish, +addyo - can one of you help here?

### dp...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### je...@chromium.org (2019-02-08)

The following public repos under https://github.com/orgs/GoogleChrome that had problematic permissions have all been updated to restrict Wiki write access:

accessibility-developer-tools
chrome-app-codelab
chrome-app-samples
chromium-dashboard
custom-tabs-client
devsummit
dialog-polyfill
inert-polyfill
multi-device
webstore-docs

### mk...@gmail.com (2019-02-09)

[Comment Deleted]

### je...@chromium.org (2019-02-11)

[Empty comment from Monorail migration]

### dp...@chromium.org (2019-02-11)

@mkzreport - we're looking into that for you. 

### sh...@chromium.org (2019-02-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-02-25)

Thanks  mkzreport@! $500 for this bug, a member of finance staff will be in touch to arrange payment. Cheers!

### mk...@gmail.com (2019-02-26)

Thanks!

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-18)

This issue was migrated from crbug.com/chromium/927307?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093909)*
