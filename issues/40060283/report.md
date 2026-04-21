# chrome.debugger API bypasses the runtime_blocked_hosts cookie protection

| Field | Value |
|-------|-------|
| **Issue ID** | [40060283](https://issues.chromium.org/issues/40060283) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2022-07-14 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

- Setup  
  
  Add host to runtime\_blocked\_hosts <https://chromeenterprise.google/policies/?policy=ExtensionSettings>  
  
  For windows 10 using registry at HKEY\_CURRENT\_USER\SOFTWARE\Policies\Google\Chrome create string with name ExtensionSettings and content of { "\*": { "runtime\_blocked\_hosts": [ "\*://example.org" ] } }  
  
  Policy should be listed at chrome://policy/ may need to reload.  
  
  Create cookie at <https://example.org> like document.cookie = 'foo=foo';
- Exploit  
  
  Using a browser extension with the debugger permission.

1. Get tabId like with chrome.tabs.query({active: true});
2. Attach to a tab with await chrome.debugger.attach(target, '1.3');
3. Run Storage.getCookies with await chrome.debugger.sendCommand({tabId: <tabId>}, 'Storage.getCookies'); it should contain the cookie from the runtime blocked host.

**Problem Description:**  

Browser extensions are able to get cookies from a runtime blocked host using the chrome.debugger API via Storage.getCookies <https://chromedevtools.github.io/devtools-protocol/tot/Storage/#method-getCookies>  

runtime\_blocked\_hosts "Prevent extensions from interacting with or modifying websites that you specify. Modifications include blocking javascript injection, cookie access, and web-request modifications."

**Additional Comments:**  

There may be other APIs that leak information but thats all I have found so far, despite it being tot using it with version 1.3 still works.  

Tested with latest version of chrome canary.

\*\*Chrome version: \*\* 105.0.5180.0 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [background.js](attachments/background.js) (text/plain, 500 B)
- [manifest.json](attachments/manifest.json) (text/plain, 164 B)
- [block.reg](attachments/block.reg) (application/octet-stream, 176 B)

## Timeline

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-07-14)

The attachments are a browser extension and a registry file named block.reg to add a runtime_blocked_host of *://example.org
For step 2 target = {tabId: <tabId>};

### nd...@protonmail.com (2022-07-15)

Other ways to modify or view cookies should have checks.
Network.getAllCookies
Storage.getCookies


### nd...@protonmail.com (2022-07-17)

Network.loadNetworkResource (https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-loadNetworkResource) also leaks information and the body can be read like await IO.read(result.resource.stream);
There's also a setCookie feature I think the behavior should change to be like the cookie permission with <all_urls>

It seems that its not possible to intercept a request for a protected host via the debugger API.

### dc...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API]

### dc...@chromium.org (2022-07-18)

Similarly to https://crbug.com/chromium/1345102, assigning to nrpeter@ for clarification.

### bh...@google.com (2022-07-26)

Hi Nick, could you help us identify whether this is considered a security threat, and we can triage the bug accordingly.

### me...@chromium.org (2022-08-02)

(Last week's secondary sheriff here) chrome.debugger is already a powerful API. Given that, assigning medium as the tentative severity here.

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

nrpeter: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-18)

nrpeter: Uh oh! This issue still open and hasn't been updated in the last 34 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### si...@chromium.org (2022-08-18)

palmer@, might you be able to comment on this in place of nrpeter@?

### pa...@chromium.org (2022-08-18)

Unfortunately, I don't know anything about this.

### rd...@chromium.org (2022-08-18)

+dsv

Whether we consider this a security bug, I'd say it's probably a functional bug.  We should likely include policy-restricted hosts in the checks when we attach a debugger.

### nd...@protonmail.com (2022-08-18)

Think it already does and that was also a security issue https://bugs.chromium.org/p/chromium/issues/detail?id=1139156

### ds...@chromium.org (2022-09-26)

I'm not quite sure what the issue is: the description is referring to example.org while the background.js is using about:blank. I assume both are placeholders. For the same site or for different sites? It looks like we indeed block attaching to the policy-blocked URLs. So what is the attached chrome extension demostrating?

### nd...@protonmail.com (2022-09-27)

Storage.getCookies "Returns all browser cookies." it does not matter what site the debugger is attached to.
https://chromedevtools.github.io/devtools-protocol/tot/Storage/#method-getCookies

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e124986e8b3eb701f630b95bd12f096a8418de4

commit 5e124986e8b3eb701f630b95bd12f096a8418de4
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Sep 30 09:24:59 2022

Disable Storage.getCookies for untrusted clients. It doesn't seem to be
used by extensions right now and is exposing information that is browser
wide and might be inappropriate for extensions.

Bug: 1344647
Change-Id: I37e3fcdfed312342d100b489ed523425bd2b0a0e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929023
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1053471}

[modify] https://crrev.com/5e124986e8b3eb701f630b95bd12f096a8418de4/content/browser/devtools/browser_devtools_agent_host.cc
[modify] https://crrev.com/5e124986e8b3eb701f630b95bd12f096a8418de4/content/browser/devtools/protocol/storage_handler.h
[modify] https://crrev.com/5e124986e8b3eb701f630b95bd12f096a8418de4/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/5e124986e8b3eb701f630b95bd12f096a8418de4/content/browser/devtools/protocol/storage_handler.cc
[modify] https://crrev.com/5e124986e8b3eb701f630b95bd12f096a8418de4/content/browser/devtools/render_frame_devtools_agent_host.cc


### ds...@chromium.org (2022-09-30)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-09-30)

Not fixed. https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-getAllCookies
Storage.getCookies -> Network.getAllCookies

Maybe there are other APIs that are browser wide. https://crbug.com/chromium/1344647#c3 and https://crbug.com/chromium/1344647#c4

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-09-30)

Storage.getCookies https://chromium-review.googlesource.com/c/chromium/src/+/3929023
Network.getAllCookies https://chromium-review.googlesource.com/c/chromium/src/+/3929054)

Network.getCookies also needs protection https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-getCookies
Page.getCookies also needs protection https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-getCookies

Maybe should also include changing cookies
https://chromedevtools.github.io/devtools-protocol/tot/Storage/#method-setCookies
https://chromedevtools.github.io/devtools-protocol/tot/Storage/#method-setCookies
https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-setCookie
https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-setCookies

Network.loadNetworkResource can include credentials so may need to be protected https://chromedevtools.github.io/devtools-protocol/tot/Network/#type-LoadNetworkResourceOptions


### gi...@appspot.gserviceaccount.com (2022-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/097fa9c3cfab09409e39b3cb050fc8819bb65d5c

commit 097fa9c3cfab09409e39b3cb050fc8819bb65d5c
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Oct 05 04:41:15 2022

Update comments for Page.getCookies to better reflect semantics.

Bug: 1344647
Change-Id: I034386f3e97a419a58bac779f524dbeab5deeb15
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3931557
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1055125}

[modify] https://crrev.com/097fa9c3cfab09409e39b3cb050fc8819bb65d5c/third_party/blink/public/devtools_protocol/browser_protocol.pdl


### nd...@protonmail.com (2022-10-11)

Maybe this issue should be reopened for now since its not fixed yet.

Asking before attaching the debugger would make it harder to exploit the current warning happens to late.

### rd...@chromium.org (2022-10-11)

Re-opening just to make sure dsv@ has a chance to re-evaluate from https://crbug.com/chromium/1344647#c23 and onwards.  Danil, if you'd like to split those out into separate bugs, feel free to file + re-close.

### ds...@chromium.org (2022-10-12)

Overall this is working as intended. Debugger permission allows injecting any request into a page and inspecting them, including their cookies. runtime_blocked_hosts is ignored along with other host permissions. Basically debugger extensions need a full control over the page to be a debugger. I am going to block Network.getAllCookies to reduce the exposure, and I updated to comments of the Page.getCookies to say what it really does. 

However, we have to plans to address the general issues for the reasons stated above.

### nd...@protonmail.com (2022-10-12)

"Debugger permission allows injecting any request into a page and inspecting them" I think the debugger gets detached if you create an iframe of a protected host.

runtime_blocked_hosts is meant to restrict <all_urls> which would allow all websites to be attacked.
The debugger extension implies <all_urls> so should have the same restrictions thats why I think this is not working as intended for that policy.

If thats not practical to implement there should be a confirmation before attaching the debugger to tell the user there enterprise policy is being ignored.



### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### aj...@google.com (2022-10-12)

-> Fixed as we did some work based on this report, and no further work is necessary.

### nd...@protonmail.com (2022-10-12)

Page.getCookies returns any cookies you ask it to.
await chrome.debugger.sendCommand(target, 'Page.getCookies', {urls: ['https://example.org']});

loadNetworkResource would still work disabling APIs is not much of a solution it should be checking for the protected host.

Its still WONTFIX reward-ineligible unfortunately despite other runtime_blocked_hosts reports getting fixed.


### am...@chromium.org (2022-10-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations! The VRP Panel had decided to award you $3,000 for this report! Thank you for your efforts in discovering and reporting this issue to us!

### nd...@protonmail.com (2022-10-14)

Thanks :)

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f0539553369692ee993a3249ebe9bdb237322abf

commit f0539553369692ee993a3249ebe9bdb237322abf
Author: Danil Somsikov <dsv@chromium.org>
Date: Thu Dec 29 18:01:44 2022

Mark Network.getAllCookies as deprecated.

Bug: 1344647
Change-Id: Idf206e97a7ff192798edd0761f4530c63f4f40ba
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4128123
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1087613}

[modify] https://crrev.com/f0539553369692ee993a3249ebe9bdb237322abf/third_party/blink/public/devtools_protocol/browser_protocol.pdl


### [Deleted User] (2023-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1344647?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### da...@google.com (2024-04-04)

Philip, do I understand correctly that since we've added support for runtime_blocked_hosts, we can allow extensions access to Storage.getCookies

### pf...@chromium.org (2024-04-04)

Did we add that support for chrome.debugger, or just for chrome.devtools? I remember we did the second, but I'm not sure about the former.

### da...@google.com (2024-04-04)

Yeah, I don't think we did. Also it was for attaching to the URL, not inspecting cookies. 

And filtering doesn't fit very well into the StorageHandler::getCookies

I think the best we can do is have a boolean parameter to StorageHandler like can_read_cookies that will be true for all clients except for extensions with at least one entry in runtime_blocked_hosts. 

WDYT?

### pf...@chromium.org (2024-04-04)

We did some cookie filtering in <https://issues.chromium.org/issues/40069061>, but yeah, that doesn't help here. Do you think we could the pass PolicyBlockedHosts pattern set into the NetworkHandler for [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/protocol/network_handler.cc;l=1166;drc=f85e2931070f20b81171b91298bda280ca337a09) somehow? But if that's tricky, I like your solution, it's very pragmatic!

### nd...@protonmail.com (2024-04-04)

I think this issue was never fully fixed, comment 35 and comment 27

### ap...@google.com (2024-04-18)

Project: chromium/src
Branch: main

commit a179cb521fc14cb2bf167a50ae2f7b0a4730b7e0
Author: Danil Somsikov <dsv@chromium.org>
Date:   Thu Apr 18 06:26:26 2024

    Filter out cookies for hosts that extension don't have access to, instead of banning Storage.getCookies completely.
    
    Also apply the same protection to Network.getCookies, which previous was allowed, even with custom urls parameter.
    
    Bug: 40060283
    Change-Id: I064e62d797a41d7e997f01af5000f0f08cf35d35
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5424794
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Auto-Submit: Danil Somsikov <dsv@chromium.org>
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1289162}

M       chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
M       content/browser/devtools/browser_devtools_agent_host.cc
M       content/browser/devtools/dedicated_worker_devtools_agent_host.cc
M       content/browser/devtools/protocol/devtools_protocol_browsertest.cc
M       content/browser/devtools/protocol/network_handler.cc
M       content/browser/devtools/protocol/network_handler.h
M       content/browser/devtools/protocol/storage_handler.cc
M       content/browser/devtools/protocol/storage_handler.h
M       content/browser/devtools/render_frame_devtools_agent_host.cc
M       content/browser/devtools/service_worker_devtools_agent_host.cc
M       content/browser/devtools/shared_worker_devtools_agent_host.cc
M       content/public/test/test_devtools_protocol_client.cc
M       content/public/test/test_devtools_protocol_client.h

https://chromium-review.googlesource.com/5424794


### nd...@protonmail.com (2024-04-18)

Does this fix `Network.loadNetworkResource` the protection would seem very pointless when other cross-site leaks are not getting patched.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060283)*
