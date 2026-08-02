# Insufficient URL Scheme Validation in regex_rules_matcher.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [464217867](https://issues.chromium.org/issues/464217867) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | dj...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2025-11-28 |
| **Bounty** | $2,000.00 |

## Description

URL: src/extensions/browser/api/declarative\_net\_request/regex\_rules\_matcher.cc

Details

"source\_file": "src/extensions/browser/api/declarative\_net\_request/regex\_rules\_matcher.cc", "type": "Insufficient URL Scheme Validation"

The CreateRegexSubstitutionRedirectAction function, which handles declarativeNetRequest redirect rules with regex substitutions, fails to properly validate the scheme of the generated redirect URL. While it correctly blocks javascript: URLs, it does not prevent redirects to other dangerous schemes, most notably file:. This allows a malicious extension with the declarativeNetRequest permission to craft a rule that redirects a user's navigation to a file: URL. This URL can open internal files ,

# location :

std::optional<RequestAction>\nRegexRulesMatcher::CreateRegexSubstitutionRedirectAction(\n const RequestParams& params,\n const RegexRuleInfo& info) const {\n // ...\n GURL redirect\_url(redirect\_str);\n\n // Redirects to JavaScript urls are not allowed.\n // TODO([crbug.com/40111509](https://crbug.com/40111509)): this results in counterintuitive behavior.\n if (redirect\_url.SchemeIs(url::kJavaScriptScheme)) {\n return std::nullopt;\n }\n\n return CreateRedirectAction(params, \*info.regex\_rule->url\_rule(),\n std::move(redirect\_url));\n}

#impact:

i was able to downlaod html file and open it with file:/// direclty , also can use that vuln with other schema

Impact A malicious Chrome extension can download a file and then access it via a file:/// URL. This behavior allows extensions to open or read local files that should be protected by Chrome’s isolation of local file resources. An attacker can use any URL scheme and open nearly any file type on disk.

Important — dynamic rules.json The rules.json used in this attack is dynamic and generated at runtime after the extension is installed. It is not a static file shipped inside the extension package or stored in the extension folder. Because the redirect rules are created on-demand (after installation) and retrieved from the attacker's server, Web Store reviewers performing a static inspection of the extension bundle will not see these malicious rules. This means the attack cannot be detected simply by reviewing the extension package contents on the Web Store.

I’ve attached a video and PoC files.

Steps to reproduce

Download the PoC files.

Start attacker\_server.py.

Load the malicious extension into Chrome.

The extension generates file.html (which contains an alert in the PoC) and automatically downloads it to Chrome’s default download folder.

The extension detects where file.html was saved and sends that path to the attacker server.

The attacker server generates a dynamic rules.json (not present in the extension bundle) and returns it to the extension.

The extension updates its declarativeNetRequest rules with that rules.json.

The extension automatically opens a window or popup with a host such as example.com. The dynamic rules.json redirects example.com to file:///path/file.html so the local file is loaded and executed in the browser context. Attack scenario
Attack scenario

Result file:///path/file.html is loaded and executed in the browser, allowing execution of local-file content or access to local resources that should not be accessible. Because the redirect rules are created and deployed at runtime, the malicious behavior is not visible by inspecting the extension bundle or a static Web Store review.

## Attachments

- [dnrdnr.mp4](attachments/dnrdnr.mp4) (video/mp4, 1.6 MB)
- [background.js](attachments/background.js) (text/javascript, 3.9 KB)
- [manifest.json](attachments/manifest.json) (application/json, 313 B)
- [attacker_server.py](attachments/attacker_server.py) (text/x-python, 2.0 KB)
- [dnrdnr.mp4](attachments/dnrdnr_75678449.mp4) (video/mp4, 1.6 MB)
- [dnrdnr.mp4](attachments/dnrdnr_75953924.mp4) (video/mp4, 1.6 MB)

## Timeline

### rd...@chromium.org (2025-12-05)

Great catch! Kelvin, can you take a look?

### bl...@google.com (2025-12-15)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### bl...@google.com (2025-12-23)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### bl...@google.com (2025-12-31)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### bl...@google.com (2026-01-08)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### bl...@google.com (2026-01-16)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### dj...@gmail.com (2026-02-19)

Hello any update here ?

### bl...@google.com (2026-02-27)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### ke...@google.com (2026-02-27)

On it

### ke...@chromium.org (2026-03-03)

I wonder if it's the same issue as [crbug.com/40945803](https://crbug.com/40945803)

Basically: only allow file redirects if the extension has local file access permission?

### dj...@gmail.com (2026-03-04)

Nope is not the same vuln , the vuln allow file redirect without local file access , and you can check it , go load the extension , go to setting find the extension disable access to localfile and test it and you will get redirect , and also the attack happen remotly the user can't see what happening , because it happen from server of the attacker

### ke...@google.com (2026-03-04)

Rephrasing a bit: if extensions could only redirect to file:// URLs if they had local file access permissions? Or is the vulnerabilty STILL not solved EVEN if extensions had those permissions?

The pending code change in the other bug: crrev.com/c/6441363 attempts to fix this though IMO it's not checking at the right file

### dj...@gmail.com (2026-03-05)

Ah, I understand what you are asking now! Yes, rephrasing it your way: if you patch DNR so that it strictly enforces the local file access permission check for file:// redirects, it will successfully kill this exploit.

I also completely agree with your assessment of [crrev.com/c/6441363](https://crrev.com/c/6441363) . Shaheen's patch applies the check inside RulesetManager, which is too late in the pipeline and will cause priority collisions with other extensions. As I noted in my report, the vulnerability originates deeper down when the action is created. The validation really needs to happen inside RegexRulesMatcher::CreateRegexSubstitutionRedirectActio so that if the extension lacks file permissions, the rule returns std::nullopt and disqualifies itself before RulesetManager ever sees it.

### dj...@gmail.com (2026-03-05)

can you please give me access to <https://issues.chromium.org/issues/40945803>

### dj...@gmail.com (2026-03-05)

that report > <https://issues.chromium.org/issues/483777842>

you should close it as duplicated of my report

### dj...@gmail.com (2026-03-11)

@ke...@chromium.org any update here ?

### bl...@google.com (2026-03-19)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### bl...@google.com (2026-03-27)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### bl...@google.com (2026-04-04)

Hoi, ke...@chromium.org! This bug has not been updated for a while. Please update the bug to meet go/chrome-slo.

(Attention: @ke...@chromium.org)

Automated by Blunderbuss job chrome_blunderbuss_autoassigner for config p1_pinging_config for component 1456110.

### dj...@gmail.com (2026-04-10)

It seems there was a mistake in marking my report as a duplicate. In fact, the other issue is a duplicate of my report. You can verify this by checking the dates of the reports—my report was submitted first.

I would appreciate it if this could be reviewed and corrected.

### ke...@google.com (2026-04-11)

Ok I was thinking of handing priority to whatever bug describes the general culprit/problem...

### ke...@google.com (2026-04-11)

Anyway both bugs should be fixed by one CL which will explicitly check on an extension's access to file URLs before allowing/disallowing some of their DNR rules from operating on the request

### dx...@google.com (2026-04-17)

Project: chromium/src  

Branch:  main  

Author:  Kelvin Jiang [kelvinjiang@chromium.org](mailto:kelvinjiang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7746569>

[DNR] Require file access for file URL redirects

---


Expand for full commit details
```
     
    Require file access to be enabled for the extension before their DNR 
    rules (redirect) can operate on requests FROM file URLs, or if the 
    redirect rule would redirect a request TO a file URL. 
     
    Fixed: 464217867, 483777842 
    Change-Id: Ibad51967c28d13cf3f662265c9d61ccaefc4cc70 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7746569 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1616957}

```

---

Files:

- M `chrome/browser/extensions/api/declarative_net_request/declarative_net_request_browsertest.cc`
- M `chrome/browser/extensions/api/declarative_net_request/ruleset_manager_unittest.cc`
- M `extensions/browser/api/declarative_net_request/ruleset_manager.cc`

---

Hash: [53caa53855606e2a8bc96efc30bc040f6350c9eb](https://chromiumdash.appspot.com/commit/53caa53855606e2a8bc96efc30bc040f6350c9eb)  

Date: Fri Apr 17 23:56:54 2026


---

### dj...@gmail.com (2026-04-18)

Hello team,

Thank you for the update and for confirming the fix!

I would like to kindly request a reassessment of the severity and priority of this vulnerability. I believe this issue strongly warrants an S1/P1 classification based on the following factors

1- Zero User Interaction & Silent Exfiltration: As demonstrated in the attached video and my earlier PoCs, the exploit requires absolutely no user interaction once the extension is installed. The arbitrary local HTML file is opened and executed automatically, allowing an attacker to silently exfiltrate internal data from the victim's machine without their knowledge.

2- Bypass of Chrome Web Store Review: Because the declarativeNetRequest rules.json is fetched dynamically from an attacker-controlled server post-installation, the malicious code is never present inside the extension bundle. This guarantees that the extension will easily bypass static analysis and manual security reviews by the Chrome Web Store team.

3- High Impact (Local File Access): The failure to validate the file:/// scheme completely breaks Chrome's local file isolation, allowing attackers to access local resources that should be strictly protected.

Given the combination of high impact (local file read/exfiltration), high exploitability (zero-click post-install), and complete stealth (evading Web Store review), this poses a critical risk to users.

Additionally, in light of these factors and the severity of the exploit chain, I would be grateful if you could consider passing this report along for a top-tier bounty reward under the Chrome VRP.

Thank you again for your time, review, and the great work on patching this!

### ch...@google.com (2026-04-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ns...@chromium.org (2026-04-24)

Medium severity (S2) vulns should have P1 set. I've set the OS field to desktop, and FoundIn to the stable version when this vulnerability was disclosed. You may have to merge a fix to beta & stable, depending on how complex the fix is. Please reach out to the chrome security team if you have any questions.

### dj...@gmail.com (2026-04-24)

I would like to kindly request a reassessment of the severity and priority of this vulnerability. I believe this issue strongly warrants an S1/P1 classification based on the following factors

1- Zero User Interaction & Silent Exfiltration: As demonstrated in the attached video and my earlier PoCs, the exploit requires absolutely no user interaction once the extension is installed. The arbitrary local HTML file is opened and executed automatically, allowing an attacker to silently exfiltrate internal data from the victim's machine without their knowledge.

2- Bypass of Chrome Web Store Review: Because the declarativeNetRequest rules.json is fetched dynamically from an attacker-controlled server post-installation, the malicious code is never present inside the extension bundle. This guarantees that the extension will easily bypass static analysis and manual security reviews by the Chrome Web Store team.

3- High Impact (Local File Access): The failure to validate the file:/// scheme completely breaks Chrome's local file isolation, allowing attackers to access local resources that should be strictly protected.

Given the combination of high impact (local file read/exfiltration), high exploitability (zero-click post-install), and complete stealth (evading Web Store review), this poses a critical risk to users.

### ke...@chromium.org (2026-04-24)

3. I don't think DNR allows attackers to directly read or know of the contents of local files?

### ol...@chromium.org (2026-04-24)

I'm going to mark this bug as fixed again to see if it kicks off the workflow for bug bounty consideration. I'll keep an eye on it over the next few days - I know the reporter is still waiting for follow-up.

### dj...@gmail.com (2026-04-25)

Hi @ke...@chromium.org
,

Please review the video proof of concept (POC) and take a look at the POC files. I’d like your input on how I managed to escalate it to read internal files.

Thanks,

### dj...@gmail.com (2026-05-13)

Hello , any update here |?

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Web platform privilege escalation.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/464217867)*
