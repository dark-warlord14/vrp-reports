# Security: Popup window tab doesn't show the origin elided from the right

| Field | Value |
|-------|-------|
| **Issue ID** | [40075024](https://issues.chromium.org/issues/40075024) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>TopChrome>TabStrip>HoverCards |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dp...@google.com |
| **Created** | 2023-10-17 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 120.0.6071.0 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Go to <https://long-extended-subdomain-name-containing-many-letters-and-dashes.badssl.com>
2. Hover over the tab

## Attachments

- [PXL_20231017_020147987~2.jpg](attachments/PXL_20231017_020147987~2.jpg) (image/jpeg, 1.0 MB)

## Timeline

### [Deleted User] (2023-10-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-10-17)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-10-17)

Triaging as low severity since the abuse potential is limited, since the correct URL still shows in the omnibox. The fix would be to change the tab strip hover bubble so it complies with the URL display guidelines (https://chromium.googlesource.com/chromium/src/+/master/docs/security/url_display_guidelines/url_display_guidelines.md) 

tbergquist: Can you help find an appropriate owner for this? Thanks

[Monorail components: UI>Browser>TopChrome>TabStrip]

### ca...@chromium.org (2023-10-17)

Actually assigning to tbergquist

### tb...@chromium.org (2023-10-17)

I think the right place for this bug is Available in the hover cards component, based on go/top-chrome-triage

[Monorail components: -UI>Browser>TopChrome>TabStrip UI>Browser>TopChrome>TabStrip>HoverCards]

### [Deleted User] (2023-10-18)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-10-18)

(I am a bot: this is an auto-cc on a security bug)

### aj...@google.com (2024-02-02)

assigning as security issues should have an owner; CC people in the tabstrip OWNERS - please assign to someone who can make progress on this issue.

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1493231?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### dl...@google.com (2024-02-05)

This looks like a hovercard issue. CCing stluong@ (who works with hovercards) to help triage.

### st...@google.com (2024-02-05)

I think hover cards in this case are behaving as expected. If I understand this bug correctly, hover cards could potentially pose a security issue due to not displaying the full URL origin. From what I can see this issue only lies with a super long URL where the ending of the URL gets replaced with "...". Also according to the URL display guidance "If in a space-constrained environment, it's acceptable to use registrable domain instead of the full origin." so I think the current behavior follows the guideline. However, I defer judgement to dfried@ since she has more historical context on hover cards and more familiar with how hover card elides text than I am.

### ag...@google.com (2024-05-16)

realized that blunderbuss doesn't reassign issues that aren't visible to all of Google

### ch...@gmail.com (2025-04-16)

Any update on this bug?

Thanks :)

### dx...@google.com (2025-04-16)

Project: chromium/src  

Branch: main  

Author: David Pennington [dpenning@chromium.org](mailto:dpenning@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6461121>

Move elide to head for the domain for security purposes

---


Expand for full commit details
```
     
    Domain is much more important than the subdomains, thus when showing the 
    URL we prioritize domain by eliding the head. 
     
    Fixed: 40075024 
    Change-Id: I48e725e32f746b4aa7bb92871a7b6c32d61d3037 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6461121 
    Reviewed-by: Steven Luong <stluong@chromium.org> 
    Commit-Queue: David Pennington <dpenning@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1447960}

```

---

Files:

- M `chrome/browser/ui/views/tabs/fade_label_view.cc`
- M `chrome/browser/ui/views/tabs/fade_label_view.h`
- M `chrome/browser/ui/views/tabs/tab_hover_card_bubble_view.cc`

---

Hash: d9a315b74c6648f185aec28d99bf824ddd86f48f  

Date:  Wed Apr 16 20:05:27 2025


---

### dp...@google.com (2025-04-16)

this new implementation elides the url from the left so that the domain is prioritized over subdomain if overflowing.

### sp...@google.com (2025-04-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
report of lower impact security UI issue with low potential for exploitation and security implications, but did allow us to make a security beneficial change


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue with low potential for exploitation and security implications, but did allow us to make a security beneficial change

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075024)*
