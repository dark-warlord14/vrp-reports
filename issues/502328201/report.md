# Contact dialog can be shown over a cross-origin page which might confuse a user into leaking sensitive information to an attacker

| Field | Value |
|-------|-------|
| **Issue ID** | [502328201](https://issues.chromium.org/issues/502328201) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Contacts |
| **Platforms** | Android |
| **Reporter** | he...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2026-04-14 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Access <https://attacked14.github.io/x/contact.html> using Chrome on Android.
2. Click anywhere on the page (ensure you have not previously granted the Contacts permission to the browser).
3. Observe that a Contact permission dialog appears, but the underlying visible web page is from <https://www.google.com> (or another cross-origin page opened by the script).
4. If the user accepts the permission and selects a few contacts from the dialog, the contact details (names, emails, phone numbers) are leaked to the attacker-controlled server.

# Problem Description

**Description**
similar issues : <https://issues.chromium.org/issues/40057597>

When a user clicks on an attacker-controlled page, it is possible to trigger navigator.contacts.select (Contact Picker API) and simultaneously open a cross-origin page in a new browser window.

This causes the Contact permission dialog to appear above the newly opened cross-origin page. This behavior can confuse the user into believing the permission request originates from the visible (spoofed) page rather than the hidden attacker's origin. Consequently, the user may unintentionally grant access to their contact list, leaking sensitive information to the attacker.

Although the dialog technically displays the origin that requested the Contact Picker, the dialog should ideally be dismissed or blocked when a cross-origin navigation or new window occurs. The current behavior obscures the malicious origin’s relationship with the foreground cross-origin page.

The attack is most effective when:

The user has not previously granted Chrome/Edge the Contacts permission.
The attacker uses a domain similar to the targeted origin being spoofed (e.g., a typosquat or lookalike domain).

# Summary

The contact dialog box may appear on top of the cross-origin page, which could confuse users

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [Chrome Beta.webm](attachments/Chrome Beta.webm) (video/webm, 48.3 MB)
- [Chrome.webm](attachments/Chrome.webm) (video/webm, 22.7 MB)
- [spoof.html](attachments/spoof.html) (text/html, 931 B)

## Timeline

### la...@google.com (2026-04-15)

Able to repro the issue. Looks like a regression per [b/40057597](https://issues.chromium.org/issues/40057597).

### mo...@gmail.com (2026-04-17)

Hey team any update?

### ch...@google.com (2026-04-18)

The Found In field may only contain numeric values.
Some values were corrected.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2026-04-18)

Setting milestone because of s2 severity.

### mo...@gmail.com (2026-04-20)

hey team any update?

### mo...@gmail.com (2026-04-22)

Hey Team any update?

### mo...@gmail.com (2026-04-24)

hey team any update?

### an...@google.com (2026-04-27)

Taking a look. Apologies for the delay.

### dx...@google.com (2026-04-28)

Project: chromium/src  

Branch:  main  

Author:  Andy Paicu [andypaicu@chromium.org](mailto:andypaicu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7795739>

[Contacts] Dismiss picker when spawning tab is hidden

---


Expand for full commit details
```
     
    A WebContentsObserver is added to ContactsPicker to automatically cancel 
    the dialog if the spawning tab becomes hidden or destroyed. 
     
    This prevents spoofing attacks where the native contacts picker dialog 
    is shown at the same time as opening a new tab. This can make the 
    contact picker show up on the newly opened tab potentially tricking the 
    user into thinking the contact sharing request is from the new tab. 
     
    Fixed: 502328201 
    Change-Id: I8f0281cdaa002327b2263e0bf68d22015515a240 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7795739 
    Reviewed-by: Wenyu Fu <wenyufu@chromium.org> 
    Reviewed-by: Yaron Friedman <yfriedman@chromium.org> 
    Commit-Queue: Andy Paicu <andypaicu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1621858}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/contacts_picker/ChromeContactsPickerDelegate.java`
- M `chrome/android/javatests/src/org/chromium/chrome/browser/contacts_picker/ContactsPickerLauncherTest.java`
- M `components/browser_ui/contacts_picker/android/java/src/org/chromium/components/browser_ui/contacts_picker/ContactsPickerDialogTest.java`
- M `content/public/android/java/src/org/chromium/content_public/browser/ContactsPicker.java`
- M `content/public/android/java/src/org/chromium/content_public/browser/ContactsPickerDelegate.java`
- M `content/public/android/javatests/src/org/chromium/content/browser/ContactsProviderTest.java`

---

Hash: [7deafb683b1ac41212904c5e36860a71b340e8fc](https://chromiumdash.appspot.com/commit/7deafb683b1ac41212904c5e36860a71b340e8fc)  

Date: Tue Apr 28 17:09:59 2026


---

### mo...@gmail.com (2026-04-28)

Hey team, any updates on the VRP?

### dx...@google.com (2026-04-29)

Project: chromium/src  

Branch:  main  

Author:  Kay Lin [kaiyilin@google.com](mailto:kaiyilin@google.com)  

Link:    <https://chromium-review.googlesource.com/7803114>

Revert "[Contacts] Dismiss picker when spawning tab is hidden"

---


Expand for full commit details
```
     
    This reverts commit 7deafb683b1ac41212904c5e36860a71b340e8fc. 
     
    Reason for revert: Test failure rate is pretty high (only 1/6 passed). Error msg: `androidx.test.espresso.NoMatchingViewException: No views in hierarchy found matching...`. Check https://ci.chromium.org/ui/p/chrome/builders/ci/android-desktop-16-x64-rel-brya-tests/9362/overview for more information.  
     
    Original change's description: 
    > [Contacts] Dismiss picker when spawning tab is hidden 
    > 
    > A WebContentsObserver is added to ContactsPicker to automatically cancel 
    > the dialog if the spawning tab becomes hidden or destroyed. 
    > 
    > This prevents spoofing attacks where the native contacts picker dialog 
    > is shown at the same time as opening a new tab. This can make the 
    > contact picker show up on the newly opened tab potentially tricking the 
    > user into thinking the contact sharing request is from the new tab. 
    > 
    > Fixed: 502328201 
    > Change-Id: I8f0281cdaa002327b2263e0bf68d22015515a240 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7795739 
    > Reviewed-by: Wenyu Fu <wenyufu@chromium.org> 
    > Reviewed-by: Yaron Friedman <yfriedman@chromium.org> 
    > Commit-Queue: Andy Paicu <andypaicu@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1621858} 
     
    Bug: 502328201 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I55c284e352e4e0ac2e63f5c85b28d7c2f196b91b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7803114 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Kay Lin <kaiyilin@google.com> 
    Commit-Queue: Kay Lin <kaiyilin@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1622232}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/contacts_picker/ChromeContactsPickerDelegate.java`
- M `chrome/android/javatests/src/org/chromium/chrome/browser/contacts_picker/ContactsPickerLauncherTest.java`
- M `components/browser_ui/contacts_picker/android/java/src/org/chromium/components/browser_ui/contacts_picker/ContactsPickerDialogTest.java`
- M `content/public/android/java/src/org/chromium/content_public/browser/ContactsPicker.java`
- M `content/public/android/java/src/org/chromium/content_public/browser/ContactsPickerDelegate.java`
- M `content/public/android/javatests/src/org/chromium/content/browser/ContactsProviderTest.java`

---

Hash: [cfb7ca239da7e42018d42120fd12639721e573a8](https://chromiumdash.appspot.com/commit/cfb7ca239da7e42018d42120fd12639721e573a8)  

Date: Wed Apr 29 05:02:48 2026


---

### an...@google.com (2026-04-29)

Fix was reverted, need to investigate the failure that caused it.

### mo...@gmail.com (2026-04-30)

Hey Team any update?

### mo...@gmail.com (2026-05-01)

Hey Team any update?

### mo...@gmail.com (2026-05-04)

Hey Team any update?

### mo...@gmail.com (2026-05-04)

deleted

### mo...@gmail.com (2026-05-08)

deleted

### mo...@gmail.com (2026-05-17)

deleted

### mo...@gmail.com (2026-05-28)

Hi team, any updates on Chrome VRP? Thanks

### sp...@google.com (2026-06-22)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Would not be confused by reasonably prudent user.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### mo...@gmail.com (2026-06-22)

Hello Chrome VRP Team,

Thank you for reviewing my report. I respectfully request that this issue be re-evaluated based on the precedent set by Issue [#40057597,](https://issues.chromium.org/issues/40057597) which was previously accepted and awarded $1,000.

My report demonstrates the exact same security impact and attack vector: exploiting a visual race condition to display a critical permission dialog on top of a trusted cross-origin page. Since the core behavior, context confusion, and risk of user exploitation are identical to the archived case, I believe this report deserves the same severity rating to ensure consistency with VRP policy.

Could the panel please reconsider this matter in light of this historical precedent?

Thank you for your time and fairness.

### mo...@gmail.com (2026-06-23)

Please add this issue to the Security-VRP-Reassessment-Request hotlist (id:8186354).

### mo...@gmail.com (2026-07-09)

Please add this issue to the reward-topanel hotlist (id:5432096).

### mo...@gmail.com (2026-07-21)

Are there any updates on the panel discussion?

### aj...@chromium.org (2026-08-04)

panel: see comment 22

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-08-13)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

No change - old precedent.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502328201)*
