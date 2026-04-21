# Security: Samesite Cookies sent in a cross-site request navigated from Chrome's PDF viewer

| Field | Value |
|-------|-------|
| **Issue ID** | [40088888](https://issues.chromium.org/issues/40088888) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies, Internals>Plugins>PDF, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | na...@chromium.org |
| **Created** | 2017-08-31 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
Samesite cookies are never sent in a cross-site request unless the Samesite attribute in a cookie had been set to Lax, in which case the cookie is sent only when the request is a Top-level navigation using safe HTTP methods.

When clicking on a link from a PDF document loaded in Chrome's PDF viewer, the request is treated as a Same-site request, no matter the Origin of the PDF document. Consequently, the Samesite cookies will be sent. 

An attacker will be able to perform a CSRF attack by tricking the user into visiting a seemingly harmless PDF document, which is hosted on the attacker's server, and clicking on a malicious hyperlink in the PDF document (For example, http://www.non-malicious.com/?action=delete&id=1337). This will cause the Samesite=Strict cookie to be sent in a cross-site request context.

The CSRF attack is however, limited to only GET requests.

VERSION
Chrome Version: Version 60.0.3112.113 (Official Build) (64-bit)
Operating System: Windows 10 Home, Version 1703, OS Build 15063.540

REPRODUCTION CASE 
1) Create a Samesite cookie for target server (http://www.target.com/) set to Strict 
     - Create file cookie.php: <?php header("Set-Cookie: the_cookie=leet+bob; Samesite=Strict); ?>
2) Using Google Chrome, browse to http://www.target.com/cookie.php
3) On Google Chrome, press F12, Click on Applications tab, click on Cookies and ensure the value of the cookie "the_cookie" is marked as Strict under Column Samesite.
4) Create a PDF document (csrf.pdf) with a hyperlink to http://www.target.com/?action=delete&id=1337
5) Host the PDF document on http://www.attacker.com/csrf.pdf
6) Using Google Chrome, browse to http://www.attacker.com/csrf.pdf
7) Click on hyperlink in the PDF document.
8) Samesite=Strict cookie sent in the cross-site request context.

RECOMMENDATIONS
1) PDF documents loaded in the Chrome's PDF Viewer must take Origin from the URI of top-level browsing context.
2) Do not include Samesite cookies in requests if Origin of the request does not match the Registrable domain of the target's URI.

ADDITIONAL INFORMATION AND PROOF-OF-CONCEPT
Please refer to Attached for more details.

## Attachments

- [Samesite Cookie CSRF PoC.pdf](attachments/Samesite Cookie CSRF PoC.pdf) (application/pdf, 639.5 KB)
- [form.pdf](attachments/form.pdf) (application/pdf, 12.1 KB)
- [example.PNG](attachments/example.PNG) (image/png, 8.4 KB)

## Timeline

### el...@chromium.org (2017-08-31)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### el...@chromium.org (2017-09-01)

Verified repro in Chrome 62.3201.

Test Page: https://bayden.com/test/cookie/samesitecookie.aspx


### es...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-02)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-05)

The JS in the PDF viewer does (something very similar to):

    var disposition = e.detail.newtab ?
        Navigator.WindowOpenDisposition.NEW_BACKGROUND_TAB :
        Navigator.WindowOpenDisposition.CURRENT_TAB;
    this.navigator_.navigate(e.detail.uri, disposition);

I'm not sure what I need to do to navigate differently?

### el...@chromium.org (2017-09-05)

Re #8: Am I correct in thinking that this call ends up flowing down to chrome.windows.create[1] Extension API? If so, I don't see any arguments on that call[2] that would allow us to specify the initiator context that would be necessary for Chrome to implement SameSite cookie restrictions properly. (I also note that navigations initiated in this scenario lack a Referer header).

[1] https://cs.chromium.org/chromium/src/chrome/browser/resources/pdf/navigator.js?l=74&rcl=461ab1f5d4c1823d7e2e496ed2cfdbf9b80fb935

[2] https://developer.chrome.com/extensions/windows#method-create

### ha...@gmail.com (2017-09-06)

I'm not familiar with the JS for the PDF Viewer but I created a PDF document with a form submission using HTTP POST, and opened it in Chrome. (see attached)

Hope it might help:

=======================================
POST /test.php HTTP/1.1
Host: test.com
Content-Length: 272
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Origin: chrome-extension://mhjfbmdgcfjbbpaeojofohoefgiehjai
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8
Connection: close

<PDF file>
=======================================

### rd...@chromium.org (2017-09-06)

Thoughts below:

We know which extension initiated the request.  The most restrictive version of this would be to treat the extension as the origin, and only consider it the samesite if it's to one of those extension's pages.  The less strict version would be to allow the extension to specify whether to consider the navigation should be considered samesite and only allow it to do so if it has permissions to that origin.

Do we have any instinct for whether just taking the strict model would break anything?

Also, what would we have to do differently from the windows/tabs API to let chrome enforce this?

At a higher level, I'm not entirely clear on why this is worse than existing cases.  I think that we send a samesite=strict cookie for most non-renderer initiated navigations (like middle clicking), and nharper@ confirmed this was the case.  So is this particular attack (using a malicious PDF) and different than having a malicious website with the user middle-clicking?  We frequently treat extension-initiated navigations as being browser-initiated (similar to a middle click).

### el...@chromium.org (2017-09-06)

Ah, I didn't realize middle-click, shift-click, and right-click>OpenInNewTab all circumvent the protections of SameSite cookies. All of those seem like a pretty low bar for an attacker to clear.

> Also, what would we have to do differently from the windows/tabs
> API to let chrome enforce this?

I /think/ we'd need to add a field to the createData object passed to chrome.windows.create. The initiatorURL would allow the extension to pass the URL that should be used as a Referer and against which SameSite restrictions would be consulted. 

### rd...@chromium.org (2017-09-06)

Sorry, I meant "what in our implementation of the tabs/windows API would need to change", rather than "what should change in the public API".  Specifically, we use chrome::Navigate with chrome::NavigateParams; is it just a matter of setting a referrer on the navigate params?

### ha...@gmail.com (2017-09-07)

Re #11:
> So is this particular attack (using a malicious PDF) and different than having a malicious website with the user middle-clicking?

A PDF can be hidden in an <iframe> that is crafted to make the hyperlink appear 'normal' on the malicious site. Even though this vulnerability requires user interaction, a simple left-click (usual behaviour) would suffice to perform the CSRF attack.

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### ha...@gmail.com (2018-01-19)

Hello! Would like to ask if there has been a fix for this and does this bug qualify for a bounty? Thanks!

### el...@chromium.org (2018-01-19)

RE #16: This has not yet been fixed (the Status field will be updated when it has been). After vulnerabilities are fixed, they're sent for consideration to Chrome's Vulnerability Rewards Panel. Thanks for your report and patience!

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### ji...@chromium.org (2018-04-09)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-04-23)

[Empty comment from Monorail migration]

### oc...@chromium.org (2018-06-25)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-09-04)

Setting PDF bugs assigned to me back to untriaged so they can get re-assigned as needed.

### hn...@chromium.org (2018-09-05)

I'm not sure who is a good owner to take a look at this. Lei, can you reroute?

### ha...@gmail.com (2018-09-26)

Hello. Is there update on this? It has been more than a year since disclosure.

### th...@chromium.org (2018-09-26)

CCing bug reporter from https://crbug.com/chromium/855931.

### th...@chromium.org (2018-09-26)

Thanks for checking in. It looks like the previous bug owner did not get a chance to fix this, so there have not been any progress here.

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### ha...@gmail.com (2020-07-27)

Hello! I believe this issue has been here for some years now. Is there an update on this?

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-04-30)

Hello! It's been awhile. Wanted to check in on the status. TIA!

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/761038?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies, Internals>Plugins>PDF]
[Monorail mergedwith: crbug.com/chromium/830799, crbug.com/chromium/855931]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2025-03-26)

hi thestig@, we recently reviewed this issue for potential disclosure (we're going through our oldest sev-low bugs for potential disclosure). In reviewing this we determined that at this time we'd consider this sufficiently serious and warrant some traction toward a resolution.

I've updated this to medium severity and P1 accordingly.
Could you PTAL and look at a potential resolution. Thank you.

### ch...@chromium.org (2025-03-26)

Setting FoundIn to current extended version based on historical report of this longstanding issue

### ch...@google.com (2025-03-27)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2373 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-28)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2374 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-29)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2375 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-30)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2376 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-31)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2377 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-01)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2378 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-02)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2379 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-03)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2380 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-04)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2381 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-04)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2381 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-05)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2382 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-06)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2383 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-07)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2384 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-08)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2385 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-09)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2386 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-10)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2387 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-11)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2388 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-12)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2389 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-13)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2390 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-14)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2391 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-15)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2392 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-16)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2393 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-17)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2394 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-18)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2395 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-19)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2396 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-20)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2397 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-21)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2398 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-22)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2399 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-23)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2400 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-24)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2401 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-25)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2402 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-26)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2403 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-27)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2404 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-28)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2405 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-29)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2406 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-30)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2407 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-01)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2408 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-02)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2409 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-03)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2410 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-04)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2411 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-05)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2412 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-06)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2413 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2414 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2414 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-08)

thestig: Uh oh! This issue still open and hasn't been updated in the last 2415 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### es...@chromium.org (2025-05-16)

[Security triage] There hasn't been any update on this issue in quite a while, and actually it's unclear if anyone has ever really looked into it. thestig@, are you the right owner? cc'ing some other PDF folks too. If somebody could please take a look and see what would be involved in fixing this, that would be great.

### th...@chromium.org (2025-05-21)

Yes, it's been a while. I'll take a look sooner rather than later.

### ch...@google.com (2025-06-05)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### th...@chromium.org (2025-06-07)

I finally got around to setting up a test server to reproduce this, and couldn't. After bisecting old builds, I found <https://crrev.com/621626> fixed the issue for my test set-up. Can someone confirm this issue no longer happens before I close it out? Just in case I missed something.

### ha...@gmail.com (2025-06-07)

Hi, it would appear that the bug is no longer reproducible on my end as well.

I understand it's been awhile, but I'd like to request for a CVE, and for the team to review for a bug bounty.

Greatly appreciated!
Thank you

### th...@chromium.org (2025-06-07)

Marking this fixed (in 73.0.3668.0) and hopefully Chrome Security Team will go through the normal VRP reward progress, albeit a bit late.

### na...@chromium.org (2025-06-09)

thestig@, the bots did the right thing and flagged it with "reward-topanel", so it will be looked by the VRP panel. It doesn't make sense for me to be the owner, but also don't feel strongly for how to handle this edge case.

### th...@chromium.org (2025-06-09)

nasko@: I wanted to give you credit for fixing this with <https://crrev.com/621626>.

### na...@chromium.org (2025-06-10)

Whoa! Thanks! I hadn't looked at the link for the fix ... fun times! : )

### sp...@google.com (2025-06-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
baseline report of user information disclosure 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-12)

Congratulations! Thank you for your efforts and reporting this issue to us back in 2017. Apologies for the delay from resolution to closing this out.
We are happy to issue a reward, but unfortunately at this time, we are not able to issue a CVE for an issue resolved and shipped in a Stable channel update back in 2019, over six years ago. Especially given that the fix was not directly associated with this report and seems to be associated with other known / planned work outside of this report.

We are happy to provide the reward in good faith and to show our appreciate. Thank you again, and for your patience.

### ha...@gmail.com (2025-06-12)

Thank you for following up on this. It's always hard to look into backlogs. Appreciate it!

### am...@chromium.org (2025-06-14)

No worries at all -- thank you for your patience! 

### ha...@gmail.com (2025-08-17)

Hello! I'm checking in on the status of the bounty payment. I'm a little unsure if my tax submissions and all the admin matters went through. It has been a little too long and I haven't receive the bounty.
Thank you, best regards.

### am...@chromium.org (2025-08-18)

Hello, we don't handle payments or the enrollment for payments processing, please contact the p2p-vrp team as referenced above in c#156

### ch...@google.com (2025-09-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline report of user information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088888)*
