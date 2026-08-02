#  I identified that the Chrome browser’s Reading List feature introduces an origin confusion issue by reordering domain names. This behavior can mislead users about the true origin of a website.

| Field | Value |
|-------|-------|
| **Issue ID** | [503346647](https://issues.chromium.org/issues/503346647) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>TopChrome>BookmarksBar>ReadingList |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ah...@gmail.com |
| **Assignee** | ag...@google.com |
| **Created** | 2026-04-16 |
| **Bounty** | $500.00 |

## Description

---

### Report description

I identified that the Chrome browser’s Reading List feature introduces an origin confusion issue by reordering domain names. This behavior can mislead users about the true origin of a website.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Chrome Browser

---

### The problem

#### Please describe the technical details of the vulnerability

I identified that the Chrome browser’s Reading List feature introduces an origin confusion issue by reordering domain names. This behavior can mislead users about the true origin of a website.

The Chrome Reading List feature alters how domains are displayed by reordering parts of the hostname. For example, visiting `1.attacker.com` shown as `attacker.com.1`, and `1111.google.com` appear as `google.com.1111`.

This transformation breaks the standard visual cues users rely on to identify legitimate domains, potentially causing them to misinterpret malicious domains as trusted ones.

# Step To Produce:

1. Open Chrome Browser.
2. Visit website like <https://1.attacker.com/> , <http://1111.google.com/>
3. Add these two sites to the reading list.
4. Now open the Chrome Reading List it'll show attacker.com.1, google.com.1111

#### Impact analysis

This issue can lead to origin confusion attacks, where users mistakenly trust a malicious domain due to misleading display formatting. An attacker could craft domains that appear similar to legitimate services (e.g., mimicking trusted brands) and rely on Chrome Browser's Reading List reordering to obscure the true origin. This increases the risk of phishing, credential theft, and unintended interaction with malicious websites, especially in scenarios where users rely on quick tab switching rather than carefully inspecting full URLs.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7727.57 (Official Build) (64-bit) (cohort: Control)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Security UI Spoofing

#### How would you like to be publicly acknowledged for your report?

Tareq Ahamed - itztrq

## Attachments

- [evd.png](attachments/evd.png) (image/png, 48.6 KB)
- [evd.png](attachments/evd_75624642.png) (image/png, 48.6 KB)
- [evds-2.png](attachments/evds-2.png) (image/png, 403.3 KB)

## Timeline

### ah...@gmail.com (2026-04-16)

One more thing, Urls should be elided from front when displaying anywhere in the user interface as per standard security guidelines for most browsers in order to avoid url spoofing or confusing users with actual domain name, when long domain/subdomain is used.

If I use this long domain: https://long-extended-subdomain-name-containing-many-letters-and-dashes.badssl.com/ , it gets elided from the end. But it should elide from the front.

### ch...@google.com (2026-04-17)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ag...@google.com (2026-04-20)

The domain gets elided from the front in the reading list so that is WAI. The title of the page does not and that is also WAI.

I've tested this on several sites with subdomains and the order of the url parts in the reading list are correct. It appears this is only an issue with numeric subdomains

### ah...@gmail.com (2026-04-21)

Happy to see the issue got accepted. Is this eligible for a monetary reward?

Regards,
Tareq Ahamed

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  main  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7782762>

[Reading List]Fix domain rendering for reading list

---


Expand for full commit details
```
     
    The url list item will render the title and domain or description of a 
    tab. Directionality of the text is reversed to elide from the front 
    which results in domains being rendered backwards. This ensures the 
    domain direction is isolated from the eliding so it will render 
    correctly. 
     
    https://screenshot.googleplex.com/BhFRWMFYrmJ7uN4 
     
    Bug: 503346647 
    Change-Id: Ic4ce0ef132d0b027a20922ed4d5da03f82b7a6a0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7782762 
    Commit-Queue: Alison Gale <agale@chromium.org> 
    Reviewed-by: John Lee <johntlee@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1618889}

```

---

Files:

- M `chrome/test/data/webui/cr_elements/cr_url_list_item_test.ts`
- M `ui/webui/resources/cr_elements/cr_url_list_item/cr_url_list_item.html.ts`

---

Hash: [d69cea6324b1be71f533c5b85a9cb7670935f654](https://chromiumdash.appspot.com/commit/d69cea6324b1be71f533c5b85a9cb7670935f654)  

Date: Wed Apr 22 15:34:01 2026


---

### ah...@gmail.com (2026-04-22)

Happy to see the issue got fixed. Is this eligible for a monetary reward?

Regards, Tareq Ahamed

### ah...@gmail.com (2026-05-02)

Hello Team,
It's been over a week. Wanted to know if this issue is eligible for a monetary reward?

Regards, Tareq Ahamed

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

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

### ch...@google.com (2026-07-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503346647)*
