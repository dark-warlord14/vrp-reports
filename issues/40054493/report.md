# Security: Context menu "Open" on a javascript: link bypasses Content-Security-Policy

| Field | Value |
|-------|-------|
| **Issue ID** | [40054493](https://issues.chromium.org/issues/40054493) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ni...@gmail.com |
| **Assignee** | ga...@google.com |
| **Created** | 2021-01-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When you long tap a hyperlink to javascript: URL in a page, context menu is shown.  

The menu has "Open" button that executes JavaScript code in the URL on the page even though inline script is prohibited by CSP.  

So, if a page prohibits inline script by CSP, an attacker can make victim to execute the script on the page through "Open" button in the context menu.

**VERSION**  

Chrome Version: 88.0.4324.69+beta  

Operating System: iPhone 8 Simulator with iOS 14.3

**REPRODUCTION CASE**

1. Visit: <http://csrf.jp/2021/chromium_ios/csp-bypass-by-open-link.php>  
   
   This page is protected by `Content-Security-Policy: default-src 'self'`
2. Long tap a hyper link to `javascript:alert(document.domain)` and tap "Open"
3. An alert dialog with `csrf.jp` is shown (i.e., original page's CSP was bypassed)

**CREDIT INFORMATION**  

Muneaki Nishimura (nishimunea)

## Attachments

- [csp-bypass-by-open-link.php](attachments/csp-bypass-by-open-link.php) (text/plain, 315 B)
- [demo.mov](attachments/demo.mov) (video/quicktime, 1.0 MB)

## Timeline

### [Deleted User] (2021-01-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-01-18)

Assigning to corising@ for investigation.

[Monorail components: UI>Browser>ReadLater]

### ke...@chromium.org (2021-01-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### ke...@chromium.org (2021-01-18)

Sorry, this was mis-triaged. It is strictly a CSP issue.

arthursonzogni@: Are you able to have a look? This might be a WebKit bug.

[Monorail components: -UI>Browser>ReadLater Mobile>iOSWeb>Security]

### mk...@chromium.org (2021-01-19)

This does appear to be related to CSP in WebKit, which we don't have much control over.

That said, there's something of an underlying question as to whether we should present "open" as a context menu option for `javascript:` URLs. That doesn't seem particularly valuable to me, and if it interacts strangely with WebKit's implementation of CSP, removing it might be reasonable. +pinkerton@ to triage from that perspective.

### pi...@chromium.org (2021-01-22)

Seems like something we should address. I thought we used to not show open in the case of javascript: links, maybe it regressed at some point. 

-> gauthier for triage. cc'ing eugene in case he remembers more context here. 

### ga...@chromium.org (2021-01-22)

We are handling the JavaScript in a very specific and deliberate way: https://source.chromium.org/chromium/chromium/src/+/master:ios/chrome/browser/ui/browser_view/browser_view_controller.mm;l=3361

So I think it is on purpose and not a regression.
Looking at the metrics, this is almost not used, so I am Ok with removing it if we don't remember why we added it.

### eu...@chromium.org (2021-01-22)

Is this bookmarklet? Maybe Eric knows (I have foggy memory of Eric telling me about Bookmarklets a while ago).

### no...@chromium.org (2021-01-25)

Copy is useful for a bookmarklet, open probably less so. If it is not used an a security risk, just remove it.

### ga...@chromium.org (2021-01-26)

I will remove the feature.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7982a50de2e1140d9cc8460a1bcc021191780877

commit 7982a50de2e1140d9cc8460a1bcc021191780877
Author: Gauthier Ambard <gambard@chromium.org>
Date: Tue Jan 26 20:06:40 2021

[iOS] Remove ContextMenu "Open" for JavaScript

Fixed: 1167629
Change-Id: I38f8ee2214db775cf970afe5dc7067affe589ab9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2648677
Commit-Queue: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: Weilun Shi <sweilun@chromium.org>
Reviewed-by: Justin Cohen <justincohen@chromium.org>
Reviewed-by: Weilun Shi <sweilun@chromium.org>
Cr-Commit-Position: refs/heads/master@{#847285}

[modify] https://crrev.com/7982a50de2e1140d9cc8460a1bcc021191780877/tools/metrics/actions/actions.xml
[modify] https://crrev.com/7982a50de2e1140d9cc8460a1bcc021191780877/ios/chrome/browser/ui/browser_view/browser_view_controller.mm


### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations, nishimunea@ - another one! The VRP Panel has decided to award you $1000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Nice work!

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-06-24)

This issue was migrated from crbug.com/chromium/1167629?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Mobile>iOSWeb>Security]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054493)*
