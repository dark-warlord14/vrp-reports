# Security: History Cached Page of the Lens region search cause url spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40056980](https://issues.chromium.org/issues/40056980) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Permissions>SearchEngineGeolocation, UI>Browser>Navigation, UI>Browser>Navigation>BFCache |
| **Platforms** | Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | sk...@chromium.org |
| **Created** | 2021-08-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

History Cached Page of the Lens region search cause url spoof  

The Lens region search page is always on the top of the webpage cause the URL spoof.

**VERSION**  

Chrome Version:95.0.4616.0 (Developer Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**  

0. Enabel chrome://flags/#enable-lens-region-search

1. open the <http://localhost/poc.html>
2. Click the "First Click Me" to navigator to the google.com
3. Click to go back button to leave on the <http://localhost/poc.html> page
4. Right click and select "Search part of the page with Google Lens" and wait

## Attachments

- [poc.gif](attachments/poc.gif) (image/gif, 3.0 MB)
- [poc.html](attachments/poc.html) (text/plain, 251 B)

## Timeline

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-08-23)

Hmm, perhaps this feature only exists on Windows? I don't get the context menu item on Canary on macOS. Can someone with Windows and navigation-spoofing experience please see if they can confirm? Thanks!

[Monorail components: Internals>Permissions>SearchEngineGeolocation UI>Browser>Navigation]

### cr...@chromium.org (2021-08-23)

Thanks for the report-- there's indeed a few issues here!  I can repro on Windows Canary 95.0.4619.2.  It looks like the biggest problem is a bad interaction between the back-forward cache desktop trial and the Lens search feature, but there are some minor issues even without bfcache.  I'm not sure which platforms Lens is available on, so I'll tentatively just list Windows.

First, it appears the main repro might depend on chrome://flags#back-forward-cache being enabled.  If I disable that, the Lens screenshot is replaced by the intended page when the forward navigation occurs after 5 seconds.  If I set it to "Enabled force caching all pages (experimental)," then the bug repros.  It repros whenever there's a "Back/Forward Cached Page" available in Chrome's task manager, when you activate the page by going back/forward to it.  That's true whether you use the back/forward buttons or the window.history API.  

I'm guessing bfcache isn't triggering the event that normally causes the Lens screenshot to be discarded?  I would suggest that both teams discuss this, both to fix this case for Lens and to help the bfcache team prevent similar bugs in other features in the future.  :)

When the bug occurs, the user ends up seeing the updated address bar above the Lens screenshot of the previous page.  That makes it a URL spoof, with some mitigating factors that the screenshot is dimmed and the page is non-interactive (apart from selecting part of the screenshot to upload to Search).  That seems like Medium severity, due to the mitigating factors.

Note that there are still issues even with bfcache disabled, though.  If you go back/forward while the Lens screenshot is showing in that mode, the screenshot is cleared and you see the new page, but the cursor is still a crossbar and you can still select a portion of the (now invisible) screenshot to upload by dragging.  It's really important to exit that selection mode whenever there's a cross-document navigation.

(As a side note, it also appears that the Lens search is enabled on all pages, even chrome:// URLs.  Is that intentional, and is there a strong reason to need that?  Actually, chrome://settings works but the NTP only shows a blank screenshot, which is also a bit surprising.)

[Monorail components: UI>Browser>Navigation>BFCache]

### cr...@chromium.org (2021-08-23)

Also adding carlosil@, because my first impression is that the Lens feature might be implemented as a full-tab overlay above an active page?  That was an approach that caused many problems for interstitials (https://crbug.com/chromium/392354), so it might be worth discussing that aspect of the design if so.  (Since the search results appear to end up in a new tab, I wonder if it's safer to have the screenshot shown in that new tab as well?)

### st...@google.com (2021-08-24)

[Empty comment from Monorail migration]

### ju...@google.com (2021-08-24)

[Empty comment from Monorail migration]

### st...@google.com (2021-08-24)

IIUC the issue is that the `history.forward()` call in poc.html is able to change the active URL while the screenshot overlay with poc.html is still displayed?

Passing this to skare@ who owns the screenshot functionality that is used by Lens here and can comment more about the implementation.

That is a reasonable callout about Lens on chrome:// URLs. We will separately look into disabling the experience there.

### st...@google.com (2021-08-25)

[Empty comment from Monorail migration]

### st...@google.com (2021-08-25)

[Empty comment from Monorail migration]

### st...@google.com (2021-08-25)

[Empty comment from Monorail migration]

### sk...@google.com (2021-08-30)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### sk...@chromium.org (2021-09-09)

[Empty comment from Monorail migration]

### sk...@google.com (2021-09-15)

fyi. a change was landed:
https://chromium-review.googlesource.com/c/chromium/src/+/3134746
which listens for PrimaryPageChanged.

A change to a semitransparent mask for the overlay is out for review.

### sk...@chromium.org (2021-11-15)

We switched to a semitransparent mask overlay and added webcontents observers to close when navigating away as well. From an offline discussion it sounded like this was resolved however please feel free to reraise or follow up. thank you!

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations -- the VRP Panel has decided to award you $2000 for this report. Thank you for reporting this issue to us! 

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-02-21)

This issue was migrated from crbug.com/chromium/1242424?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Permissions>SearchEngineGeolocation, UI>Browser>Navigation, UI>Browser>Navigation>BFCache]
[Monorail blocked-on: crbug.com/chromium/1247918]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056980)*
