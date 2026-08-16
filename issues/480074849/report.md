# Previous page executes JS after navigation, allowing history.back() tab hijack

| Field | Value |
|-------|-------|
| **Issue ID** | [480074849](https://issues.chromium.org/issues/480074849) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation>BFCache |
| **Platforms** | Mac |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | mr...@gmail.com |
| **Assignee** | ra...@google.com |
| **Created** | 2026-01-30 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

Steps to Reproduce

(Optional) Start the Node.js webhook server for logging.

Serve the provided PoCs (PoC-redir.html and PoC-listener.html) using any HTTP server (not file://).

Open PoC-listener.html in Chrome Stable.

Trigger a cross-origin navigation using any of the following methods:

Click the provided link

Type a new URL in the address bar and press Enter

Drag the link to the tab bar

Wait ~2 seconds after navigation completes.

✅ Expected Behavior

After a cross-origin navigation fully commits:

The previous document should be frozen (BFCache) or destroyed.

No JavaScript should execute.

History APIs such as history.back() or history.go() should not be callable.

The old document must not regain control of the tab.

❌ Actual Behavior

After navigation completes:

The previous document continues executing JavaScript for approximately 2–3 seconds.

The page is able to call history.back() and regain control of the tab without user interaction.

Chrome DevTools reports the page being restored from BFCache, but the page is still able to execute code before freeze occurs.

Observed console message:

Navigation to PoC-listener.html was restored from back/forward cache

Despite this, the previous document executes code and triggers automatic navigation back to the attacker-controlled page.

📄 PoC Behavior Details
PoC-redir.html

Uses two setTimeout(1ms) calls to trigger navigation and execute code before unload.

Allows the previous page to retain access to APIs such as localStorage after navigation has committed.

PoC-listener.html

Uses the pagehide event to execute code after navigation begins.

Demonstrates that the issue is not limited to programmatic navigation.

Works with:

Link clicks

Address bar navigation

Drag-and-drop navigation

This method is more realistic for real-world abuse.Additional Observations

requestAnimationFrame fires once after navigation.

Network requests initiated by the old document appear as permanently pending in the new page’s Network tab.

Request origin remains attributed to the original document.

Behavior is reproducible in:

Incognito mode

Fresh Chrome installation

rel=noopener does not mitigate this issue because it occurs in the same browsing context.

⚠ Security Impact

This allows a navigated-away document to:

Regain control of the active tab without user interaction.

Manipulate browser history using history.go(n) and history.back().

Perform phishing-style tab hijacking by forcing navigation back to attacker-controlled content.

This breaks the expected navigation lifecycle security guarantees.

# Problem Description

After a cross-origin navigation fully commits, the previous document is expected to be frozen (BFCache) or destroyed and must no longer be able to execute JavaScript or invoke browser APIs such as History. However, the previous page continues executing JavaScript for approximately 2–3 seconds after navigation has completed.

During this post-navigation window, the old document is able to call history.back() and regain control of the active tab without any user interaction. This behavior occurs even though Chrome reports the page as being restored from the back/forward cache. This indicates that there is a lifecycle race window where the document remains partially active before being frozen.

This issue is reproducible using both timer-based execution (PoC-redir.html) and event-based execution using the pagehide event (PoC-listener.html). The listener-based PoC demonstrates that the behavior is not limited to programmatic navigation and can also be triggered using normal user navigation methods such as clicking links, typing URLs in the address bar, or dragging links to the tab bar.

Additional observations show that requestAnimationFrame fires once after navigation, and network requests initiated by the old document appear as permanently pending in the new page’s Network tab while retaining the original origin attribution.

The issue is reproducible on a fresh Chrome installation and in Incognito mode without any extensions. The behavior does not rely on window.open or opener relationships and occurs in the same browsing context, making rel=noopener ineffective as a mitigation.

This behavior breaks the expected navigation lifecycle security guarantees. A navigated-away document should not retain the ability to execute code or manipulate browser history. The current behavior enables phishing-style tab hijacking attacks by allowing an attacker-controlled page to force navigation back to itself after the user has already navigated to a trusted cross-origin site.

# Summary

Previous page executes JS after navigation, allowing history.back() tab hijack

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [node-webhook.js](attachments/node-webhook.js) (text/javascript, 1.4 KB)
- [PoC-listener.html](attachments/PoC-listener.html) (text/html, 7.3 KB)
- [PoC-redir.html](attachments/PoC-redir.html) (text/html, 7.0 KB)

## Timeline

### xi...@chromium.org (2026-02-03)

Thanks for the report. I'm able to reproduce. +rakina, could you check if this behavior is expected?

### ch...@google.com (2026-02-04)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mr...@gmail.com (2026-02-11)

hi any update 

### ch...@google.com (2026-02-18)

rakina: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mr...@gmail.com (2026-02-25)

hi any update ?

### ra...@chromium.org (2026-03-02)

Sorry for the delay, I just repro-ed this. It seems like there's another report with the same repro around the same timing at [crbug.com/482496308](https://crbug.com/482496308), which itself mentioned it got the repro from another similar bug that focused on screenshare instead of navigation, [crbug.com/442860743](https://crbug.com/442860743). I think this should be fixed so that the behavior is the same regardless of the previous page is BFCached or not (so, make sure the navigation fails).

### mr...@gmail.com (2026-03-02)

Hello,

Thank you for reviewing the report.

I would like to request clarification regarding the duplicate classification of issue 480074849.

Based on the submission timeline, my report appears to have been filed before 482496308. Additionally, the previously referenced issue (442860743) had already been marked as fixed prior to my submission. My report specifically demonstrates that, despite the earlier fix, inconsistent navigation behavior still occurs when the previous page is restored from BFCache, allowing JavaScript execution after navigation and enabling history.back()-based tab manipulation.

Given that:

* 442860743 was already fixed before my submission,
* 480074849 was reported prior to 482496308,
* and my report highlights BFCache-dependent navigation enforcement inconsistencies,

could you please clarify how 480074849 is considered a duplicate of 482496308? If both reports share the exact same root cause, I would appreciate confirmation of the submission timestamps and whether the issues were independently discovered.

Thank you for your time and for taking another look at this.

Best regards,
Bharat


### ch...@google.com (2026-03-05)

rakina: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-20)

rakina: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-04-01)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### mr...@gmail.com (2026-04-29)

any update ?

### ra...@google.com (2026-04-30)

Sorry for the delay, this slipped through the cracks. I've started a fix CL at [crrev.com/c/7805947](https://crrev.com/c/7805947), will try to land that soon.

### dx...@google.com (2026-05-04)

Project: chromium/src  

Branch:  main  

Author:  Rakina Zata Amni [rakina@chromium.org](mailto:rakina@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7805947>

Check lifecycle state on renderer-initiated navigation IPCs

---


Expand for full commit details
```
     
    We should disallow navigations from inactive RFHs consistently across 
    all navigation-related IPCs. We already disallow navigations in this 
    way in RFHI::BeginNavigation(), and this CL just extends the same 
    check to other renderer-initiated navigation entrypoints. 
     
    Bug: 480074849 
    Change-Id: Ifa3133dc2453c6782b1f99308398dd7fb44f50dd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7805947 
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1624850}

```

---

Files:

- M `content/browser/renderer_host/navigator.cc`
- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: [96f02574c13dad362717a59f1c654dda219aba08](https://chromiumdash.appspot.com/commit/96f02574c13dad362717a59f1c654dda219aba08)  

Date: Mon May 4 18:54:33 2026


---

### ra...@google.com (2026-05-05)

The CL above should fix the vulnerability. There are some TODOs but let me mark this as fixed first to initiate merges.

### mr...@gmail.com (2026-05-05)

hi as i seen u fixed the issue what about reward

### mr...@gmail.com (2026-05-16)

Hi, I wanted to ask if there are any updates regarding the reward review for this report. Since the issue was added to the top panel/hotlist on May 6 and related fix work appears to be in progress, I was wondering whether the reward panel review is still ongoing.

Thank you.


### mr...@gmail.com (2026-05-19)

Hello there,
I am writing to seek a thorough clarification regarding the ultimate severity assessment of the issue I recently reported. My understanding of the situation, especially concerning its evolution and the prior attempts at resolution, leads me to believe there might be a discrepancy in the final classification.
It is my firm recollection and understanding that the preceding vulnerability, which was documented and addressed at crbug.com/442860743, had been officially categorized as "fixed" well before I even initiated the submission of my detailed report. This pre-existing status suggested that the identified security flaw was considered resolved and no longer a threat within the system.
However, my subsequent report meticulously demonstrated that, despite these prior efforts and the declaration of a fix, the fundamental protection mechanism intended to safeguard against this type of bypass was, in fact, still vulnerable. Specifically, I illustrated how the bypass could be achieved through the intricate behaviors associated with BFCache (Back-Forward Cache) and the general navigation lifecycle. This intricate interaction allowed a previously loaded page to persistently execute its JavaScript code even after a user had navigated away from it. This continued execution, critically, enabled the manipulation of browser history through commands such as "history.back()", effectively undermining the intended security boundary.
Therefore, even in the wake of the supposed "fix" that was implemented for the earlier iteration of this vulnerability, the issue remained perfectly reproducible, albeit through a slightly different, yet equally impactful, vector. My report was not merely a re-demonstration of the original, ostensibly resolved behavior. On the contrary, it served as concrete evidence that the original mitigation strategy was inherently incomplete and that the underlying security boundary, which is paramount for maintaining user safety and system integrity, could still be successfully circumvented. This indicated a deeper, more persistent flaw than initially acknowledged or resolved.
Furthermore, it is noteworthy to mention that upon its initial submission and during the preliminary triage process, my report was treated internally with a significant degree of seriousness. It was classified as having a "high severity" (indicated by the P1/S1 automation tags), and it was even put forward for consideration by the rewards panel. This initial internal assessment strongly suggests that the potential impact and gravity of the vulnerability were, at that stage, considered to be substantial and warranted immediate attention. The fact that it progressed to being considered for a bounty further underscores the perceived importance and potential consequences of the exploit.
In light of these points, I find myself genuinely confused and seeking a more comprehensive explanation as to why the final severity assessment was ultimately downgraded to S3. This decision is particularly perplexing given that my report effectively highlighted that a previously identified and supposedly "fixed" security issue remained actively exploitable, presenting an ongoing risk that had not been fully mitigated by prior interventions. A clear and detailed rationale for this reclassification would be greatly appreciated to help me understand the full scope of the decision-making process.

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline lower impact Web platform privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mr...@gmail.com (2026-05-20)

creadit information please use -Bharat(mrnoob)

### mr...@gmail.com (2026-05-20)

deleted

### mr...@gmail.com (2026-05-29)

hi when i recive the cve and please cadd creadit information -Bharat(mrnoob)

### jd...@google.com (2026-06-03)

Hi Bharat, this change is scheduled be released with 149 Stable release. At that point CVE will be issued

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/480074849)*
