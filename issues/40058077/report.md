# PDF bookmarks bypass SameSite Strict cookies.

| Field | Value |
|-------|-------|
| **Issue ID** | [40058077](https://issues.chromium.org/issues/40058077) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>Cookies, Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2021-11-30 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36

Steps to reproduce the problem:
1. On the target set a cookie using document.cookie = "A=A;Secure;SameSite=Strict";
2. Create a PDF with a URL bookmark or use https://github.com/chromium/chromium/blob/main/chrome/test/data/pdf/test-bookmarks-with-zoom.pdf
3. Click the bookmark on the PDF and notice the cookies gets sent.
With the following headers:
 sec-fetch-site "none"
 sec-fetch-mode "navigate"
 sec-fetch-dest "document"

I think because extension APIs are used such as chrome.tabs.create,
Restrictions that are normally put on navigation's get bypassed excluding the schemes since that gets checked well not sure if it gets checked for submitForm but thats POST only.

What is the expected behavior?
For it to be like chrome.tabs.update and keep the initiator.

What went wrong?
PDF viewer bypassing SameSite Strict cookies and Fetch metadata defenses.

Did this work before? N/A 

Chrome version: 96.0.4664.45  Channel: stable
OS Version: 10.0

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-11-30)

I can't easily reproduce this, but it sounds plausible and feels similar to other recent SameSite bugs.

bingler@, would you be able to take a look into this?

Also CCing tsepez@ as an FYI because of the PDF connection.

[Monorail components: Internals>Network>Cookies Internals>Plugins>PDF]

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-30)

generally, we try not to grant a PDF any special capabilities based upon the site from which it is served, so in a sense all cookies might be considered cross-site even if posting back to the place from which the pdf was served.  No idea what workflows that would break.

### bi...@chromium.org (2021-11-30)

I can reproduce the issue.

Cookies are working as intended.

The issue is occuring because the mechanism being used to open the bookmarked link creates a navigation request that does not have an initiator (as mentioned by the reporter). Without an initiator the cookie code assumes this was a user initiated navigation (e.x.: typing into the URL bar) and purposefully allows SameSite=Strict cookies.

As far as I can tell this is an issue with the PDF extension. If it can be modified such that the bookmark navigation has an initiator then SameSite cookies should operate correctly.

### ts...@chromium.org (2021-11-30)

Thanks for the diagnosis in c5.  Over to Lei.

### nd...@protonmail.com (2021-12-01)

Also works as a popunder (embed iframe and trick user to click anywhere on the page)
I tried to code it my self theirs probably a better fix if you change the API. (https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/pdf/navigator.js)

  navigateInNewTab(url, active) {
    // Prefer the tabs API because it guarantees we can just open a new tab.
    // window.open doesn't have this guarantee.
    if (chrome.tabs) {
      chrome.tabs.create({url: 'about:blank'}, tab => {
	chrome.tabs.update(tab.id, {url: url});
      });
    } else {
      window.open(url);
    }
  }

  navigateInNewWindow(url) {
    // Prefer the windows API because it guarantees we can just open a new
    // window. window.open with '_blank' argument doesn't have this guarantee.
    if (chrome.windows) {
      chrome.windows.create({url: 'about:blank'}, w => {
	chrome.tabs.update(w.tabs[0].id, {url: url});
      });
    } else {
      window.open(url, '_blank');
    }
  }

### nd...@protonmail.com (2021-12-01)

...Will not "Send email" for this but forgot the popunder support.   :)
Not that I think website should be able to do it.

 navigateInNewTab(url, active) {
    // Prefer the tabs API because it guarantees we can just open a new tab.
    // window.open doesn't have this guarantee.
    if (chrome.tabs) {
      chrome.tabs.create({url: 'about:blank', active: active}, tab => {
	chrome.tabs.update(tab.id, {url: url});
      });
    } else {
      window.open(url);
    }
  }

### nd...@protonmail.com (2022-01-07)

Sill waiting on the "Over to Lei" be nice to know if they like my code :) its unlikely.

### th...@chromium.org (2022-01-12)

Sorry for being slow here. Hope to take a look later this week.

### nd...@protonmail.com (2022-01-19)

Maybe this week :)

### th...@chromium.org (2022-01-21)

A bunch of security bugs labeled Severity=High came in last week and keep me occupied.

### nd...@protonmail.com (2022-01-21)

I understand how that might delay the fix of this bug.

### nd...@protonmail.com (2022-03-13)

I may as well add a PoC for the SameSite Strict bypass also including a tab under.

### nd...@protonmail.com (2022-03-13)

Turns out its missing the open menu part as that state seems to be remembered.
The tab under can also do window.close() so it can keep going :)

### nd...@protonmail.com (2022-08-11)

This seems inactive :(
I may end up forgetting about this myself.

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-03-22)

Comment for 2023! not forgotten yet.

### nd...@protonmail.com (2023-07-21)

Would be nice if the extension API had an option to say this is cross-site initiated guessing there's a reason its not done like that.

### is...@google.com (2023-07-21)

This issue was migrated from crbug.com/chromium/1275113?no_tracker_redirect=1

[Multiple monorail components: Internals>Network>Cookies, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

### nd...@protonmail.com (2024-02-05)

:(

### nd...@protonmail.com (2025-09-17)

I think similar to <https://issues.chromium.org/40088888> this issue has been fixed, PDF bookmark sent `Sec-Fetch-Site: cross-site`

### nd...@protonmail.com (2025-09-17)

Shift clicking a PDF link does still send `Sec-Fetch-Site: none` unlike websites.

### th...@chromium.org (2026-01-23)

<https://crrev.com/1471532> fixed the bookmarks issue. <https://crrev.com/c/7513027> will hopefully fix the shift clicking issue, and this issue can finally get closed out.

### dx...@google.com (2026-01-23)

Project: chromium/src  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7513027>

[PDF] Perform navigations from the PDF Viewer more consistently, part 2

---


Expand for full commit details
```
     
    In addition to chrome.tabs.update() and chrome.tabs.create(), the PDF 
    Viewer also uses chrome.windows.create() to navigate to links. Make this 
    navigation in WindowsCreateFunction::OnBrowserWindowCreated() behave 
    like TabsUpdateFunction::UpdateURL() and ExtensionTabUtil::OpenTab(). 
     
    It may be beneficial for WindowsCreateFunction::OnBrowserWindowCreated() 
    to use the PDF Viewer behavior for more chrome.windows.create() calls. 
    But for now, only apply it to the PDF Viewer to avoid potential 
    compatibility issues. 
     
    Bug: 40058077 
    Change-Id: Ifa58d9273c31f240b5d50d2e70aa930059018b4e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7513027 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1573951}

```

---

Files:

- M `chrome/browser/extensions/api/tabs/tabs_api.cc`
- M `chrome/browser/extensions/open_tab_helper.cc`

---

Hash: [bd1a771c86bad3b2f654f38718822d6b19dba63f](https://chromiumdash.appspot.com/commit/bd1a771c86bad3b2f654f38718822d6b19dba63f)  

Date: Fri Jan 23 22:18:58 2026


---

### dx...@google.com (2026-01-29)

Project: chromium/src  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7517501>

Refactor common code into OpenTabHelper::MaybeSetPdfNavigateParams()

---


Expand for full commit details
```
     
    Combine duplicate PDF navigation code in OpenTabHelper::OpenTab() and 
    WindowsCreateFunction::OnBrowserWindowCreated() into a common function. 
     
    Bug: 40058077 
    Change-Id: If0de22a2514a4ae79be478e565d34ad36147b8df 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7517501 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1576873}

```

---

Files:

- M `chrome/browser/extensions/api/tabs/tabs_api.cc`
- M `chrome/browser/extensions/open_tab_helper.cc`
- M `chrome/browser/extensions/open_tab_helper.h`

---

Hash: [b6371f6acfdb3ce7dbac92ff054f41123637020f](https://chromiumdash.appspot.com/commit/b6371f6acfdb3ce7dbac92ff054f41123637020f)  

Date: Thu Jan 29 22:44:40 2026


---

### sp...@google.com (2026-01-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
baseline / lower impact, web platform privilege escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### nd...@protonmail.com (2026-01-30)

Thanks :)

### ch...@google.com (2026-05-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058077)*
