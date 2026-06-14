# Security: URL bar spoofing with SSL error messages (Chrome on iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40068064](https://issues.chromium.org/issues/40068064) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2012-0674 |
| **Reporter** | lp...@gmail.com |
| **Assignee** | qs...@chromium.org |
| **Created** | 2012-09-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Dear All,  

I would like to report a less-serious variant of CVE-2012-0674.

It is possible to create a page with attacker-controlled HTML content  

and URL bar pointing to other domain using SSL error messages.

I found it today when checking another CVE-2012-0674 variant, so I  

didn't think about other possible options yet (normal  

page/dns error/restricted port error seem to be ok at first look).

**VERSION**  

Chrome Version: Chrome 21.0.1180.80 stable  

Operating System: iOS 5.1.1 (iPad 2)

**REPRODUCTION CASE**  

<http://runic.pl/testy/ipad/sslerr2.html>

## Attachments

- [chromeios.jpg](attachments/chromeios.jpg) (image/jpeg; charset=binary, 27.1 KB)
- [IMG_0002.PNG](attachments/IMG_0002.PNG) (image/png; charset=binary, 26.6 KB)

## Timeline

### js...@chromium.org (2012-09-06)

Not confirmed, but setting a few flags to get the ball rolling.

### pa...@chromium.org (2012-09-06)

For some reason, I can't reproduce the bug on Chrome for iOS 19, or when I updated, 21. I get the page you see, but the Omnibox shows about:blank instead of https://centrul24.pl. I am testing on an iPod Touch; perhaps it needs to be on the iPad with its more desktop-like tab display? (On small screens, you don't get tabs across the top of the screen; tabs are a bit more like separate windows.)

I have an iPad at home, so I can check tonight. For now, maybe pinkerton or astrange can try on an iPad, or replicate the problem on another iOS device?

Also changing the Area to UI because I suspect the problem is purely in the top-layer GUI code.

### pa...@chromium.org (2012-09-06)

Here's a screenshot.

### pi...@chromium.org (2012-09-06)

Ben, any ideas what's going on here?

### pi...@chromium.org (2012-09-06)

[Empty comment from Monorail migration]

### lp...@gmail.com (2012-09-07)

http://runic.pl/testy/ipad/sslerr.html - this test case didn't work when I first checked, but now it also spoofs URL for me... I don't know what triggered this change, will try to run on another iPad later.

### lp...@gmail.com (2012-09-07)

Just to clarify "didn't work": showed about:blank

### qs...@chromium.org (2012-09-07)

 Fixed for M22.

### sc...@gmail.com (2012-09-07)

@palmer: what do you think for a severity label?

### st...@chromium.org (2012-09-07)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-07)

I can't get either http://runic.pl/testy/ipad/sslerr.html or sslerr2.html to reproduce (shows "about:blank") on my iPad running Chrome 21.

qsr and stuartmorgan: Where you ever able to reproduce this bug? What did you fix?

scarybeasts: Since I can't reproduce the bug, I have no answer for severity. If it did reproduce as cleanly as it does in the screenshot, I think I'd call it P1, SecSeverity-High since it would be a straight-up failure of a crucial security indicator (the Omnibox).

### pa...@chromium.org (2012-09-07)

Good News, Everyone. I updated Chrome on my iPad to 21.0.1180.80, and now I can reproduce this vulnerability. It works consistently. sslerr.html still does not work for me, but sslerr2.html does.

So it seems to be specifically that version? And iPad-only (?) due to the differences in tab behavior/presentation on iPad vs. iPod/iPhone/small screens.

I'm leaving it as Fixed on the assumption that it is fixed in 22. Let me know if otherwise.

### sc...@gmail.com (2012-09-07)

[Empty comment from Monorail migration]

### lp...@gmail.com (2012-09-10)

I finally found some time for follow-up, I'm sorry for delay. sslerr.html works if I simply put longer delay in setTimeout (~1000 ms), so it's not adding anything new here.

Another issue that may be somewhat related to this one:
https://code.google.com/p/chromium/issues/detail?id=147625

### pa...@chromium.org (2012-09-10)

qsr, can you please point me to the CL that fixed this? Thanks.

### sc...@gmail.com (2012-09-25)

@lpilorz: interesting find, thanks!
This qualifies for $500 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### lp...@gmail.com (2012-09-25)

Hi, thanks, but I'm not sure if I'm eligible for reward here, because I initially reported it to Apple (not this exact testcase, but they are aware it works for SSL error pages in Chrome for iOS), before I realized this is a separate issue from what Safari has.

### lp...@gmail.com (2012-09-25)

I confirm it's fixed in 21.0.1180.82, thanks.

### pa...@google.com (2012-09-25)

It's good that it's fixed now, but I thought it was scheduled for M22? pinkerton, stuartmorgan, can you confirm that we shipped it in M21, and if so, update the Mstone tag? This means the release notes for yesterday left out information about this fix, and that we'll need to post-facto announce it in M22.

Adding kerz, with apologies...

### pi...@chromium.org (2012-09-25)

I can confirm that a fix was committed to our B21 branch at 2558f8893b3cc596cc7efd55fe777b0ec2589ac3 and released as part of .82 yesterday in the app store.

Note there will be no M22, we're on to M23 to get back on the desktop milestone schedule.

### pa...@chromium.org (2012-09-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-26)

@lpilorz: I can confirm that you're still eligible for the reward :) It's fine to report bugs to other potentially affected vendors. It's the third-party brokers who are not ok (due to leaks etc.)

### pa...@chromium.org (2012-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/146760?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068064)*
