# Security: bypass of CSP validator to run remote code in extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40051270](https://issues.chromium.org/issues/40051270) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | mo...@google.com |
| **Created** | 2020-01-17 |
| **Bounty** | $3,000.00 |

## Description

The CSP validator blocks remote code in extensions by restricting script-src, object-src, worker-src and default-src (<https://cs.chromium.org/DoesCSPDisallowRemoteCode> and <https://cs.chromium.org/GetSecureDirectiveValues>). Other directives are accepted as is.

The script-src-elem and script-src-attr directives are not checked. Consequently, malicious extension authors can use these directives to bypass the remote code restrictions.

**REPRODUCTION CASE**

1. Create a directory and save the attached extension files in that directory.
2. Visit chrome://extensions , enable Developer mode and click on "Load unpacked", then select the directory from step 1.

Expected:

- The script shoud be blocked (along with the error message "Refused to load script ..." in the background's console).
- The chrome://extensions page should display an error about the directive being insecure,  
  
  e.g. "Ignored insecure CSP value "data:" in directive 'script-src-elem'."

Actual:

- The script runs, a dialog with the message "CSP validation bypassed" is shown.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 266 B)
- [background.js](attachments/background.js) (text/plain, 132 B)

## Timeline

### ct...@chromium.org (2020-01-17)

Confirmed behavior from the report in Canary 81.0.4029.0.

+karandeepb@ who has most recently worked on the CSP validator it looks like. Could you take a look? Thanks!

I'm not completely clear how to go from loading javascript from a hard-coded data: URL to running remote code, but this also feels like maybe a violation of unsafe-eval. Do you have ideas for what the next step a malicious extension would use here given this?

### ro...@robwu.nl (2020-01-17)

In the test case, a data:-URL was hard-coded to make the test case fully self-contained.
If you edit manifest.json, replace data: with http:, and replace the data:-URL in background.js with a remote http(s):-URL, then that remote script still runs, unexpectedly.

To compare with the expected behavior, remove the `script-src-elem ...;` directive from manifest.json, and add data: and/or http: to the script-src directive. Then you would see the expected behavior (as reported).

> Do you have ideas for what the next step a malicious extension would use here given this?

Remote code is supposed to be blocked by the CSP, without exceptions ( https://developer.chrome.com/extensions/migrating_to_manifest_v3#csp_changes ). If this were to be implemented correctly, then code reviewers and static analysis tools can more reliably determine the level of risk that an extension poses, and block extension submissions that are malicious.

With the ability to run remote code, malicious extensions can bypass those checks.

### ct...@chromium.org (2020-01-17)

Thanks for the followup. That this can run with "http:" added to the CSP and loading remote scripts makes more sense as a bypass, and hopefully can give karandeepb@ more of a starting point for how to address this.

### ka...@chromium.org (2020-01-17)

Thanks for catching this Rob. 

Regarding the severity of this, currently extensions can override the CSP anyway, but we place restrictions on what kind of sources one can specify as part of secure directives like script-src. See https://cs.chromium.org/chromium/src/extensions/common/csp_validator.cc?sq=package:chromium&g=0&rcl=9f8b4ed1eb51748892bf28289663b02b328d6336&l=250. 

For example, unsafe-inline is not allowed, but extensions can specify a hash for the inline source. Similarly http:// sources are not allowed. These restrictions are described at: https://developer.chrome.com/extensions/contentSecurityPolicy#relaxing. 

Using script-src-elem and script-src-attr, extensions can bypass these restrictions, however it's not clear if it amounts to much. For example, extensions can already allow remote code by specifying unsafe-eval as part of their content security policy. Rob and Devlin: Does that line up with your understanding?

However, this also means that our implementation of disallowing remote code in Manifest V3 is buggy and extensions have a way to bypass remote code restrictions as of now. Note that Manifest v3 is still in development. 

Another thing: It'd be nice to check if our internal automated review systems handle things like these correctly.

### ka...@chromium.org (2020-01-17)

Regarding a fix: It should be easy to modify the functions Rob linked to check for script-src-elem and script-src-attr. 

For manifest V3, we might be able to do something more robust to ensure that future additions to the CSP spec don't break the security guarantees we enforce. For the case where the extension overrides the content security policy, instead of checking whether it disallows remote code, we can instead supply two CSP headers to the extension background contexts and isolated worlds: The one supplied by the extension and another default CSP header which disallows remote code. IIRC, as per the CSP spec, if multiple CSP headers are supplied, both of them must be checked. Hence we should be able to guarantee that the default CSP header is always obeyed. (Idea courtesy simeonv@). 

### ro...@robwu.nl (2020-01-18)

> Using script-src-elem and script-src-attr, extensions can bypass these restrictions, however it's not clear if it amounts to much. For example, extensions can already allow remote code by specifying unsafe-eval as part of their content security policy. Rob and Devlin: Does that line up with your understanding?

That is currently the case with manifest v2 extensions. An explicitly documented goal of manifest v3 / CSP dictionary is to restrict remote code.

> However, this also means that our implementation of disallowing remote code in Manifest V3 is buggy and extensions have a way to bypass remote code restrictions as of now.

And not the first one. I know of multiple, and have reported one a few years ago, but no action has been taken on that. I can mail you details if you'd like.

> Another thing: It'd be nice to check if our internal automated review systems handle things like these correctly.

Raising awareness of the issue is one of the reasons for filing this bug. The Chrome Web Store's review process is opaque to me, but I suspect that static analysis and reliance on documented platform capabilities is part of it.

### ka...@chromium.org (2020-01-21)

>> However, this also means that our implementation of disallowing remote code in Manifest V3 is buggy and extensions have a way to bypass remote code restrictions as of now.

> And not the first one. I know of multiple, and have reported one a few years ago, but no action has been taken on that. I can mail you details if you'd like.

Can you elaborate Rob? Disallowing remote code is a relatively new thing, so it's not clear to me if you are pointing to remotely hosted code restrictions or something else. In any case, feel free to reply here or email me the details. 


### ro...@robwu.nl (2020-01-21)

> Can you elaborate Rob? Disallowing remote code is a relatively new thing, so it's not clear to me if you are pointing to remotely hosted code restrictions or something else. In any case, feel free to reply here or email me the details.

CSP is primarily a shield against accidental XSS.

But CSP in extensions is also used to enforce policies. So far the policy only rejected http: and inline code. Remote code was blocked by default, with an officially documented opt-in via unsafe-eval or sandboxed pages. The next step is the restriction of remote code.

If properly implemented, CSP can be relied upon to assess the risk that an extension poses.

In Chrome, there are several ways to bypass CSP to run arbitrary code, outside of the officially documented methods. In case this bug gets fixed sooner than the other, I won't delve in the details (feel free to mail me if you want to discuss further), but here are the list of bugs that come to mind right now:

- https://crbug.com/chromium/756962 (2 methods)
- https://crbug.com/chromium/899726
- https://crbug.com/chromium/1042963 (this bug)

### ka...@chromium.org (2020-01-21)

> If properly implemented, CSP can be relied upon to assess the risk that an extension poses.

I see where you are coming from. And agree that we should fix these bugs. I'll try to get to this and https://crbug.com/chromium/756962 soon. Note that there would always be ways to get around CSP restrictions, so in a sense the guarantees at the platform level would never be entirely robust.


### ka...@chromium.org (2020-01-22)

[Empty comment from Monorail migration]

### ka...@chromium.org (2020-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

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

### ka...@chromium.org (2021-10-11)

Putting these back into triage queue.

### ka...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-05-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2022-12-18)

For MV3 extensions, this bug has been fixed by:
https://chromium.googlesource.com/chromium/src/+/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3

This issue is referenced in a comment of the implementation:
https://chromium.googlesource.com/chromium/src/+/21889514b9a909c28996028e25c17020e97f0874%5E%21/#F4

Both commits are part of https://crbug.com/chromium/899726 and https://crbug.com/chromium/1200198 ; Can I be cc'd there?

The bug still exists in MV2 extensions, because the implementation reads whatever CSP is specified in the manifest (using the buggy validation as mentioned in this bug):
- `CSPInfo::GetMinimumCSPToAppend`
  https://source.chromium.org/chromium/chromium/src/+/main:extensions/common/manifest_handlers/csp_info.cc;l=171-172;drc=e87daef07a9edfb0f1ac1d51335f73e5f54aeeba
- https://source.chromium.org/chromium/chromium/src/+/main:extensions/common/manifest_handlers/csp_info.cc;l=155;drc=e87daef07a9edfb0f1ac1d51335f73e5f54aeeba

Historically, remote script URLs have been allowed in MV2. The current version of the docs is next to useless, but at the time of reporting this issue, the documentation did accurately state that the CSP can be relaxed to permit "secure" (https) scripts:
https://web.archive.org/web/20200118005758/https://developer.chrome.com/extensions/contentSecurityPolicy/#relaxing

Therefore this issue can be marked as Fixed IMO.

### tj...@chromium.org (2022-12-20)

Thanks for the thorough update here rob. Marking this particular one fixed as suggested.

### [Deleted User] (2022-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations on another one! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1042963?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051270)*
