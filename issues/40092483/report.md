# Security: SiteInstanceImpl::GetSiteForURL ignores hash in Data URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40092483](https://issues.chromium.org/issues/40092483) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-09-18 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: 69 stable  

Operating System: Windows 10 RS4

**REPRODUCTION CASE**

1. Go to <https://attack.shhnjk.com/try_data.html>
2. Click on the button
3. Open new tab and enter "chrome://restart" and hit enter key

Observe that 2 Data URLs created from different site are now in same process.

<https://cs.chromium.org/chromium/src/content/browser/site_instance_impl.cc?q=site_instance_impl.cc&l=520>  

"Remove hash from the URL in either case, since same-document navigations shouldn't use a different site URL."

Unfortunately, hash in Data URL is still a part of body in Chrome. So in case hash contains secret, that might be leaked.

## Timeline

### s....@gmail.com (2018-09-19)

I made a PoC to specifically have secret after the hash, but secret could really be after the hash such as following:

data:text/html,<font color="#ff0000">test</font><input type="text" value="secret">

Here hash is used to specify color in hex. But secret comes after the hash thus it could be leaked.

### na...@chromium.org (2018-09-19)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### al...@chromium.org (2018-09-19)

Note regarding #1: using unescaped '#' characters in a data URI body is deprecated and will be removed in M71, see https://www.chromestatus.com/features/5656049583390720.

### s....@gmail.com (2018-09-19)

I reproed this bug in Chrome 71 (canary). That bug is still under development.

### al...@chromium.org (2018-09-19)

+smcgruer@ who seems to be working on #3 in https://crbug.com/chromium/123004 and might be able to comment on its status.

### sm...@chromium.org (2018-09-19)

At this point, we are very unlikely to be able to land the deprecation of using unescaped '#' characters in a data URI body - at least not anytime soon. WebView is effectively blocking us, and even Chrome side there is a lot of compat risk to landing it :(.

So for now, we should fix this assuming current '#' handling for data URIs.

### mb...@chromium.org (2018-09-25)

Is anyone from the cc list able to pick this up as owner? Also, feel free to adjust severity if you disagree.

### sm...@chromium.org (2018-11-05)

FYI we actually did manage to reland the removal of using unescaped '#' characters in a data URI body this week; http://crrev.com/b52ebdc80 . Yet to see if it will stick however.

If this sticks, this should be implicitly fixed in M72?

### s....@gmail.com (2019-03-11)

This is fixed by https://www.chromestatus.com/feature/5656049583390720

### na...@chromium.org (2019-03-11)

Thanks for the follow up s.h.h.n.j.k@. Closing as fixed as per https://crbug.com/chromium/885215#c9.

### sh...@chromium.org (2019-03-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-20)

Congrats the Panel decided to reward $500 for this report! 

### aw...@google.com (2019-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-06-18)

This issue was migrated from crbug.com/chromium/885215?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092483)*
