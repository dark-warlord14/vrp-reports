# CSP Violation reports contain blockedURI's hostname

| Field | Value |
|-------|-------|
| **Issue ID** | [40057239](https://issues.chromium.org/issues/40057239) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2021-09-13 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
For reproduction, simply visit https://cm2.pw/research/xsleaks/csp-url?url=https://fb.com/4&domain=fb.com and notice the `blockedURI` directive which says `facebook.com` instead of fb.com. 

** Note: It's a vulnerability in WebKit and not in Chrome itself. 

What is the expected behavior?
Instead of destination URI, it should show the requesting URI which is as per spec as well.

What went wrong?
The destination URI was reported instead of requesting URI.

Did this work before? N/A 

Chrome version: 93.0.4577.39  Channel: stable
OS Version: 15.0

The report is identical to that of crbug.com/932892. However, the fault here is of WebKit instead of Chromium. 

The vulnerability was originally reported to WebKit at- https://bugs.webkit.org/show_bug.cgi?id=226316
<rdar://problem/78552912>

And, it was said to be fixed but it hasn't. We're still in communication but it's a little slow.

Here are some references;
https://bugs.webkit.org/show_bug.cgi?id=208089
https://bugs.chromium.org/p/chromium/issues/detail?id=313737&thanks=313737&ts=1383237203
https://web.archive.org/web/20150319213525/http://homakov.blogspot.com/2014/01/using-content-security-policy-for-evil.html

As described in Homakov's "Using CSP for evil", we can abuse this behaviour to detect whether user has authorized a certain application and stuff like that. For example, if a user has already authorized Facebook to access his Instagram account,  sending request to Instagram's OAuth endpoint with Facebook's `client_id` would redirect to Instagram instead of Facebook. That basically reveals whether the user uses Instagram or not and if s/he's using Facebook to login to Instagram. There are few more attack surfaces, also described in Homakov's blogpost. Please let me know if if you've any questions or concerns.

## Attachments

- [blockedURI.jpg](attachments/blockedURI.jpg) (image/jpeg, 137.5 KB)

## Timeline

### [Deleted User] (2021-09-13)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-13)

Antonio, please could you confirm that Chrome-for-iOS suffers from the same problem you fixed in https://crbug.com/chromium/932892?

If so, please assign this to sdefresne@ to see if the iOS team can put any pressure on Apple to fix it :)

### ad...@google.com (2021-09-13)

[Empty comment from Monorail migration]

[Monorail components: Mobile>iOSWeb>Security]

### [Deleted User] (2021-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@google.com (2021-09-15)

I run into some problems installing chrome on iOS, so I tested this with Safari, but that shouldn't matter. I can confirm that WebKit seems to reports the destination URL (stripped to the origin) after redirects instead of the original request URL (prior to any redirects) in the blocked-uri field.

As per https://crbug.com/chromium/1248889#c2, assigning to sdefresne@.

See also https://bugs.chromium.org/p/chromium/issues/detail?id=1055049, regarding the document-uri field of the report in the exact situation. It looks like Apple fixed that, but did not fix the blocked-uri field.

### [Deleted User] (2021-09-27)

sdefresne: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2021-09-27)

Ajuma, should we file a radar/webkit bug for this?

### pr...@gmail.com (2021-09-27)

#9, I already reported it to WebKit, also mentioned in the initial report;
> The vulnerability was originally reported to WebKit at- https://bugs.webkit.org/show_bug.cgi?id=226316
> <rdar://problem/78552912>

Or should I file a new one?


### ol...@chromium.org (2021-09-27)

Small issue is that radars are not accessible from other people/organisation. So if we want to contact Apple about it, we will probably need to create a new one.
Also, I don't have access to this webkit bug, so I don't know if we also need a new one or if ajuma can access it.

### aj...@chromium.org (2021-09-27)

The WebKit bug is fixed (as of Aug 21), by https://trac.webkit.org/changeset/281431/webkit.

In your initial comment in this bug, you said "it was said to be fixed but it hasn't". Do you mean there is some case not covered by this patch? Or is it that the fix hasn't rolled out to users yet?

This fix was only cherry-picked to the Safari 15.0 branch 5 days ago (see https://trac.webkit.org/changeset/282928/webkit) so I wouldn't expect to see it until a later beta of iOS 15.1 or otherwise in iOS 15.2

If there are some cases that are not covered by this patch, please file a new WebKit bug with the details, so that the WebKit team can look into it.

### aj...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-28)

[Empty comment from Monorail migration]

### aj...@chromium.org (2021-10-18)

This is fixed in iOS 15.1 beta 4.

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations, Prakash! The VRP Panel has decided to award you $1000 for this report. Thank you for reporting this issue to us so we could be aware of the fix in WebKit. 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1248889?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057239)*
