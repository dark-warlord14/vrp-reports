# Security: remote debugging + DNS rebinding = UXSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40090537](https://issues.chromium.org/issues/40090537) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | pf...@chromium.org |
| **Created** | 2018-02-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When Chrome is started with the --remote-debugging-port=PORT flag, a HTTP + WebSocket server is enabled at the given port. This WebSocket server provides access to the remote debugging protocol, which offers control over the whole browser. This results in scripting access to arbitrary websites, the ability to read local files (<https://crbug.com/chromium/805557>), write to local files (<https://crbug.com/chromium/805445>), and launch external programs (<https://crbug.com/chromium/798222>).

To use the remote debugging protocol from a web page, an attacker needs the following:

- The port of the HTTP/WebSocket server.
- The GUID to identify the remote debugging target.

The port can trivially be found, e.g. by checking whether a static image resource at the DevTools server can be loaded.

The GUID can be discovered via the HTTP server. Normally the HTML and JSON responses are protected by the Same-Origin Policy, but because the DevTools server does not validate the host of the request, a DNS rebinding attack can be carried out to access the content anyway.

A brief sketch of the attack scenario is:

- User uses Chrome with --remote-debugging-port (e.g. via Puppeteer [1], Selenium or just via the CLI).
- User visits an attacker-controlled page (e.g. malicious advertisement in a frame).
- Attacker gains full control over the user's browser after a minute without further user interaction.

Puppeteer [1] deserves a special mention, because although is made by the Chrome team (and has 500k+ downloads in the last month [2]),  

its repository does not have any documentation about security.  

There is even a blog post on Google's developer blog [3] that promotes the use of Chrome through Puppeteer, again without mentioning security risks.

[1] <https://github.com/GoogleChrome/puppeteer>  

[2] <https://www.npmjs.com/package/puppeteer>  

[3] <https://developers.google.com/web/updates/2018/01/devtools-without-devtools>

**VERSION**  

Chrome Version: 64.0.3282.167 (stable) + 66.0.3351.0 (canary)

**REPRODUCTION CASE**  

This is a fully self-contained PoC, written for Linux & Node.js.

1. Download the attached two files (index.html and server.js).
2. Choose a port number that you want to use, and start Chrome with remote debugging enabled, e.g.  
   
   chrome --remote-debugging-port=1234
3. Start the server to simulate an attacker:  
   
   node server.js 127.0.0.2 1234
4. Edit /etc/hosts and add the following entry:  
   
   127.0.0.2 attacker.example.com
5. Open <http://attacker.example.com:1234> in a new tab in Chrome (any browser works, does not need to be the one from step 2).
6. Wait until the page detects the DevTools server.  
   
   When the page has found the DevTools port, it will redirect itself to the attacker's host + IP of DevTools server.  
   
   (coincidentally, the port in this test is the same as the port of the initial attack page).
7. When you see a redirect to <http://attacker.example.com:1234?/?runExploit>,  
   
   edit /etc/hosts and change the previously added entry to:  
   
   127.0.0.1 attacker.example.com
8. Wait a minute (you can go to chrome://net-internals/#dns to see when the DNS entry expires).
9. Observe that the content of a local file is printed.

To fix this problem, I suggest to verify that the Host header is either an IP address or "localhost".  

To support users who want to access the remote debugger through another host name, a new command-line flag can be added, e.g. --remote-debugging-hosts=custom.local,foo.example.com

## Attachments

- [index.html](attachments/index.html) (text/plain, 8.9 KB)
- [server.js](attachments/server.js) (text/plain, 1.7 KB)

## Timeline

### el...@chromium.org (2018-02-19)

> verify that the Host header is either an IP address or "localhost".

This sounds reasonable to me. 

Given the type of configuration required for exploit, this is probably Severity-Low at best.

### ro...@robwu.nl (2018-02-19)

> Given the type of configuration required for exploit, this is probably Severity-Low at best.

The only requirement for the user is the --remote-debugging-port flag.
All other steps in the PoC require some work on the attacker's part, but there are no unrealistic assumptions being made there.

The download numbers of Puppeteer (500k+ in the last month alone [1]) shows that there is a significant number of users who can readily be exploited by this, so wouldn't that classify the bug as Medium at least?

[1] https://www.npmjs.com/package/puppeteer

### el...@chromium.org (2018-02-19)

> The only requirement for the user is the --remote-debugging-port flag.

Correct, enabling remote debugging of your browser instance is not a common action and should not be positioned as super-safe.

### ro...@robwu.nl (2018-02-19)

Enabling remote debugging is a guaranteed action for Puppeteer, a product of Chrome's team which is actively supported and promoted, with multiple use cases that involve loading untrusted web pages.

I added the DevTools label on this bug, will those who work on Puppeteer also see this bug?

### oc...@chromium.org (2018-02-19)

Thanks for the report! Setting this to medium per the large user base of puppeteer.

pfeldman, could you please help with this one too? 

### sh...@chromium.org (2018-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-20)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-03-02)

pfeldman@, friendly ping. Are you able to have a look at this?

### sh...@chromium.org (2018-03-05)

pfeldman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2018-03-05)

The combination of Puppeteer and DNS spoofing does not sound like "medium". Puppeteer is used for lab testing in the controlled environment and web scraping where users should take measures to protect themselves anyways.

Host: header would sound fine. Puppeteer will eventually move to the pipes instead of http, that would close this topic once and for all.

### pf...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ba1513223e47b62ed53b61518b7f7b82ad1d8ccd

commit ba1513223e47b62ed53b61518b7f7b82ad1d8ccd
Author: Pavel Feldman <pfeldman@chromium.org>
Date: Wed Mar 07 20:14:13 2018

DevTools: check Host header for being IP or localhost when connecting over RDP.

Bug: 813540
Change-Id: I9338aa2475c15090b8a60729be25502eb866efb7
Reviewed-on: https://chromium-review.googlesource.com/952522
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Pavel Feldman <pfeldman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#541547}
[modify] https://crrev.com/ba1513223e47b62ed53b61518b7f7b82ad1d8ccd/content/browser/devtools/devtools_http_handler.cc


### sh...@chromium.org (2018-03-21)

pfeldman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2018-03-22)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-03-22)

Is there any further work to do here, or does the CL in #12 mean that it can be changed to FIXED?

### pf...@chromium.org (2018-03-22)

[Empty comment from Monorail migration]

### pf...@chromium.org (2018-03-22)

Actually, I'd like to merge it into M66.

### pf...@chromium.org (2018-03-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-22)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-03-23)

Approving merge to M66. Branch:3359

### el...@chromium.org (2018-03-23)

This attack is effectively public: https://medium.com/0xcc/visual-studio-code-silently-fixed-a-remote-code-execution-vulnerability-8189e85b486b

### ro...@robwu.nl (2018-03-23)

The conclusion of that article is "Better use an alternative random port than 9333 to avoid potential exploit.".
That doesn't resolve the security issue, it only obscures the problem (and it's not even effective). Just like Chrome, VSC/Electron/Node.js should validate the Host header to avoid exploitation through web browsers.

Since ofrobots@ was CC'd in https://crbug.com/chromium/813540#c18, I guess that the Node.js team is aware of this.
Eric: If not, could you reach out to the relevant teams?

### pf...@chromium.org (2018-03-23)

Node fix is on its way, VSC/Electron no longer listen to the port by default afaik. They are based on chromium, so they should pick the upstream fix as they roll.

### pf...@chromium.org (2018-03-23)

@John: could you check if remote ChromeDriver scenarios are working as expected with this? If you are not sending Host: header in your RDP requests, you should not be affected.

### pf...@chromium.org (2018-03-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0e914b95f7cae6e8238e4e9075f248f801c686e6

commit 0e914b95f7cae6e8238e4e9075f248f801c686e6
Author: Pavel Feldman <pfeldman@chromium.org>
Date: Fri Mar 23 16:43:55 2018

DevTools: check Host header for being IP or localhost when connecting over RDP.

TBR=pfeldman@chromium.org

(cherry picked from commit ba1513223e47b62ed53b61518b7f7b82ad1d8ccd)

Bug: 813540
Change-Id: I9338aa2475c15090b8a60729be25502eb866efb7
Reviewed-on: https://chromium-review.googlesource.com/952522
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Pavel Feldman <pfeldman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#541547}
Reviewed-on: https://chromium-review.googlesource.com/978444
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#397}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/0e914b95f7cae6e8238e4e9075f248f801c686e6/content/browser/devtools/devtools_http_handler.cc


### jo...@chromium.org (2018-03-23)

@Pavel: ChromeDriver always uses Host header while communicating to DevTools, and there seems to be no easy way to disable it. https://cs.chromium.org/chromium/src/net/http/http_network_transaction.cc?type=cs&q=HttpNetworkTransaction::BuildRequestHeaders unconditionally adds Host header. So we'll have to modify the net library to add a new option.

By the way, how do I tell DevTools to allow remote connections? Even though it's called remote-debugging-port, my testing showed that by default it refuses remote connections.

### ro...@robwu.nl (2018-03-23)

> ChromeDriver always uses Host header while communicating to DevTools, and there seems to be no easy way to disable it.

RDP is allowed if the host header is missing, "localhost" or an IP address. This probably covers the most significant (if not all) use cases of ChromeDriver, doesn't it?

> So we'll have to modify the net library to add a new option.

If the host restriction is too strict, I would suggest supporting a new flag to whitelist additional hosts (see the end of my bug report) instead of modifying net/.

> how do I tell DevTools to allow remote connections

$ chromium --user-data-dir=/tmp/whatever --remote-debugging-port=9333 &
$ netstat -na |grep 9333
tcp        0      0 127.0.0.1:9333          0.0.0.0:*               LISTEN     

Chrome binds to 0.0.0.0, so it should be remotely accessible. If it does not in your case, check whether your firewall is blocking connections.

### pf...@chromium.org (2018-03-23)

>> By the way, how do I tell DevTools to allow remote connections? Even though it's called remote-debugging-port, my testing showed that by default it refuses remote connections.

Could you resolve address to IP first and then establish the RDP connection using that IP address?

### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2018-03-26)

>> Could you resolve address to IP first and then establish the RDP connection using that IP address?

I can, but there are complications. Resolving one host name can resulting in multiple IP addresses. It will be an additional complexity in ChromeDriver to explicitly try each IP address. An alternative would be requiring the user to pass in IP address instead of host name for remote connections.

### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-03-29)

This apparently got filed in 2016 as https://crbug.com/chromium/650094

### aw...@chromium.org (2018-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-01)

The panel decided to award $500 for this report. Thanks as ever!

### aw...@google.com (2018-04-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### ra...@gmail.com (2019-07-10)

The fix for this issue is to NOT OPEN the socket on 0.0.0.0 by default : problem solved.

Running a debugger opened to the wide-opened web is not what should dictate debugger protocol itself.
There are dozens of valid uses for the debugger like internal application testing where it's perfectly normal to have working protocol without any hostname constraints.
Moreover OP proposed a `--remote-debugging-hosts` which was not implemented.

A **debugger** protocol must be robust ; blacklisting requests based on `hostname` is not. 
I run the debugger under a variety of hostname like `my_debugger` or `phpfpm` which may not even be under my control and would prefer to avoid an extra DNS-resolution step. Please revert to a hostname-agnostic protocol.


### is...@google.com (2019-07-10)

This issue was migrated from crbug.com/chromium/813540?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/824816]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090537)*
