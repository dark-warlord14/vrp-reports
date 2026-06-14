# Security: UXSS/SOP bypass with document.write (Chrome on iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40070685](https://issues.chromium.org/issues/40070685) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | iOS |
| **Reporter** | lp...@gmail.com |
| **Assignee** | qs...@chromium.org |
| **Created** | 2012-09-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to get cross-domain JavaScript access using document.write:  

<http://runic.pl/testy/ipad/uxss.html>

**VERSION**  

Chrome Version: Chrome 21.0.1180.80 stable  

Operating System: iOS 5.1.1 (iPad 2)

**REPRODUCTION CASE**  

<http://runic.pl/testy/ipad/uxss.html>

May be also related to <http://code.google.com/p/chromium/issues/detail?id=146760>

## Timeline

### pa...@chromium.org (2012-09-10)

Assigning to qsr on the assumption that it is related to http://code.google.com/p/chromium/issues/detail?id=146760.

This does work on iPod/iPhone, not just iPad. The alert does fire, so the script does get injected to the other domain, although the pop-up box has "about://null" in its title bar, and the Omnibox shows "about:blank" instead of example.com. But the contents  of IANA's example.com page do indeed show up in the pop-up.

### pa...@chromium.org (2012-09-10)

[Empty comment from Monorail migration]

### pi...@chromium.org (2012-09-11)

This is being tracked by b/7143205.

### qs...@chromium.org (2012-09-11)

 This was not related to http://code.google.com/p/chromium/issues/detail?id=146760.

 This was due to not passing a baseURL when loading an HTML string in a webview, resulting in the internal URL of the webview being applewebdata://XXXX which seems to be able to do anything it wants, X-Origin.

 Fixed.

### qs...@chromium.org (2012-09-11)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-24)

[Empty comment from Monorail migration]

### lp...@gmail.com (2012-09-25)

I confirm it's fixed in 21.0.1180.82, thanks.

### pa...@chromium.org (2012-09-25)

pinkerton (or anybody), I take it this one also made it into M21 after all?

Again, sorry kerz. How shall we announce these fixes in release notes? Issue a correction in the M23 release notes?

### pi...@chromium.org (2012-09-26)

From qsr: "Pushed to B21 as cc06e1047cad8baa74320533a2322818a79d8f6f"



### pa...@google.com (2012-09-26)

lpilorz, how would you like us to credit you in the Chrome release notes? As Lukasz Pilorz, or in some other way?

### pa...@google.com (2012-09-26)

(Rather, I assume, Łukasz Pilorz. Took me a while to find the right Compose key combination on Linux. :))

### lp...@gmail.com (2012-09-26)

"Łukasz Pilorz" would be great, thanks :)

### pa...@chromium.org (2012-10-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-16)

Payment ready for wire as part of $1000 batch

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

This issue was migrated from crbug.com/chromium/147625?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070685)*
