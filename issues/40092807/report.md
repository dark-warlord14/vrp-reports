# Security: URL in Omnibox doesn't always match page content

| Field | Value |
|-------|-------|
| **Issue ID** | [40092807](https://issues.chromium.org/issues/40092807) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2018-10-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a redirect response is received for a request, the browser will follow the redirect. If the redirect location is given as "javascript:", however, the navigation will be cancelled. If this is done at the page level, the URL in the Omnibox will be updated (to whatever the URL was that was being redirected), while the page contents won't have changed (they'll still be whatever was there originally).

This allows a web server or extension to create a situation where the URL shown in the Omnibox doesn't match the contents of the page.

**VERSION**  

Chrome Version: Tested on 70.0.3538.67 (stable) and 72.0.3588.0 (dev)  

Operating System: Windows 10 Pro, version 1803

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will open a new tab pointing to a HTML file it contains (extension\_page.html).
3. The extension will then use the chrome.tabs.update method to update the URL of the page to a target URL, in this case <https://www.google.com/>.
4. Using the chrome.webRequest API, the extension will then redirect the request for <https://www.google.com/> to "javascript:". This will result in the navigation being cancelled.
5. At this point, the URL shown in the Omnibox will be that of the target URL (i.e. <https://www.google.com/>), while the actual page contents won't have changed (they'll still be that of the extension\_page.html file opened in step 2).

The situation as described above isn't terribly useful, since an extension needs to request permission to access the target URL (so that it can redirect requests for that URL). If an extension does have permission to access the URL, it can just inject content directly using chrome.tabs.executeScript.

An extension could simply request permission for its own domain, then use the steps above to make it appear that content being served by another domain is being served by it, but I'm not sure how useful that is.

It's also possible to take advantage of this on a regular web page (by having a server return a redirect to "javascript:"), though I don't think that would be too useful or practical, for at least two reasons. The first is that the Omnibox won't be updated if the site uses one of the window.location update methods to change the URL, or if the user clicks a link. The user would have to enter the target address in the Omnibox directly.

The second reason is that an attacker would need to return the redirect response from a server that they control, meaning that they could really only make it appear that another site is their own.

The steps below can be used to reproduce the issue without an extension. This requires a Linux environment, or something like Bash on Windows 10.

1. In the browser, open a new tab and load a website.
2. Start a one-shot webserver with Netcat:

{ echo -ne "HTTP/1.0 307 Internal Redirect\r\nLocation:javascript:\r\n\r\n"; } | nc -l -p 8080

3. In the tab you opened in step 1, navigate to the following location using the Omnibox:

<http://127.0.0.1:8080/>

At this point, the URL that's displayed (<http://127.0.0.1:8080/>) won't match the contents of the page.

Some other observations/notes:

- Opening the site settings for the page opens the settings for the target site.
- The actual origin on the page doesn't change. In the first situation above, it would still be that of the extension page.
- The chrome.tabs API reports the URL of the tab as that of the target URL.
- The tab that's created in the first situation above (by the attached extension) isn't initially active. It's only made active in step 3. If the tab is active the entire time, the URL shown in the Omnibox won't be updated until you switch away from the tab, then switch back.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 896 B)
- [extension_page.html](attachments/extension_page.html) (text/plain, 85 B)
- [manifest.json](attachments/manifest.json) (text/plain, 415 B)

## Timeline

### in...@chromium.org (2018-10-22)

Devlin, can you please help to triage this security issue.

[Monorail components: Platform>Extensions]

### rd...@chromium.org (2018-10-22)

Great find!

I see two issues here:
Primary: The URL in the omnibox is updated immediately even though the page may not load immediately.  This isn't just limited to the javascript: URL update case; this would also enable phishing if you update to a super-slow loading page.
Secondary: We shouldn't allow redirecting to a javascript: URL.  We changed this for chrome.tabs.update() in https://crbug.com/chromium/827288, but we should do the same here.

For the primary issue, we even have a well-written TODO [1] to make these navigations renderer-initiated, which will result in the origin in the omnibox only changing once the site commits.  There's some good discussion in the comments here [2] on the risks and discontinuity it creates, which are the reasons we didn't previously do it.  I think it's probably about time we revisit that decision.  creis@, nasko@, can we discuss this a bit and see if we can come up with something reasonable?

The secondary issue, I think, is much more straight-forward.  I'm going to file a new blocking bug to track that.

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/chrome/browser/extensions/api/tabs/tabs_api.cc#1382
[2] https://codereview.chromium.org/2475033002/

### rd...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-10-22)

https://crbug.com/chromium/897641#c2:

For the primary issue, I think you're right that it's because we've treated these as browser-initiated navigations in the past, and thus show the pending entry.  From [2], it sounds like we're all interested in making them renderer-initiated if we can, with the slight complication that it might confuse extensions if the Web Navigation API's tab object doesn't update its url value after chrome.tabs.update.  (Then again, I view that as more accurate, and I agree that we could add a pendingUrl value if really necessary.)

For the secondary issue, that's interesting about the change in https://crbug.com/chromium/827288 for chrome.tabs.update.  If we extended this to extension redirects in https://crbug.com/chromium/897749 (which is attractive to me), would it break extensions like Tampermonkey (as we found in https://crbug.com/chromium/879212)?  That extension redirects to javascript:history.back().  That behavior is problematic on its own, but we could try to fix it to not leave the old URL around afterward rather than preventing it, if we're worried about regressions.  Personally, I'd rather have us reach out to that developer and get them to not rely on it, since this sort of redirect seems problematic.

On the web, though, we would also want to be sure to clear the failed redirect from the address bar.  If a web server redirects to javascript:, we already don't run the code in the javascript: URL and the redirect does fail, but we aren't clearing the pending entry.  We should probably fix that (ideally with the same fix for https://crbug.com/chromium/879212).

### rd...@chromium.org (2018-10-22)

> If we extended this to extension redirects in https://crbug.com/chromium/897749 (which is attractive to me), would it break extensions like Tampermonkey (as we found in https://crbug.com/chromium/879212)?

Yes, it likely would.  We'd need to reach out to the tampermonkey developer about this.  We'll also need to check whether that's the only significant extension using that approach.

### sh...@chromium.org (2018-11-06)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-20)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2018-12-11)

Ping from the Security Sheriff. This is a medium severity issue affecting Stable.


### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-03-29)

Friendly security sheriff ping. Is there any movement on this bug?

### cr...@chromium.org (2019-03-30)

Update: Sorry for losing track of this (since I was thinking it was more about the browser-initiated behavior of chrome.tabs.update).  We fixed the problem where redirects to javascript: URLs weren't being cleared from the omnibox after being canceled in https://crbug.com/chromium/935175 and https://crbug.com/chromium/941653 (both merged to M73), which should resolve this bug.

awhalley@: I would suggest considering this for reward as well, since it predates https://crbug.com/chromium/935175 and is basically the same issue.  We just didn't tie them together.

Devlin: I'm still happy with the idea of disallowing these redirects via WebRequest in https://crbug.com/chromium/897749, once we provide a better API for extensions in https://crbug.com/chromium/943223.  And the chrome.tabs.update issue is orthogonal to this report now that we clear the omnibox for redirects to javascript: URLs.  We probably still want to pursue it for the slow navigation case, but that might belong in a separate bug.

### sh...@chromium.org (2019-03-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-04)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-04-08)

Seems like this is already fixed, per #12, so removing M74 merge request.

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats the Panel decided to reward $1,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/897641?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/897749]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092807)*
