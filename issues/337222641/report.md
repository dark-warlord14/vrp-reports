# Autofill Drop Down List Scroll Swaps Datalist Leading To Clickjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [337222641](https://issues.chromium.org/issues/337222641) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 124.0.6367.78 |
| **Reporter** | le...@gmail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2024-04-26 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Upload poc.html file to your server
2. Open the poc.html link via your windows 64 bit (Chrome Browser)
3. Click the green box. Autofill dropdown will popup and then as you point the drop down with the mouse it will scroll downwards.

# Problem Description

When the autofill drop down list is constrained on top of the screen, the datalist auto scrolls on mouse hover, making it vulnerable to clickjacking.

# Summary

Autofill Drop Down List Scroll Swaps Datalist Leading To Clickjacking

# Custom Questions

#### Reporter credit:

Levit Nudi from Kenya

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [poc video.mp4](attachments/poc video.mp4) (video/mp4, 868.1 KB)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [example_form.html](attachments/example_form.html) (text/html, 723 B)
- [poc-337222641-2024-05-06_16.11.05.mkv](attachments/poc-337222641-2024-05-06_16.11.05.mkv) (video/x-matroska, 446.2 KB)
- [autofill-clickjack.png](attachments/autofill-clickjack.png) (image/png, 115.4 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### le...@gmail.com (2024-04-27)

When the AutofillPopup is shown, there is a minimum bound (amount of single autofill label / pixel amount currently visible to the user) requirement for a hidden suggestion to be autofocused before selected by the user. This is a normal behavior meant to ensure that web users only click suggestions that are visible to them and it helps to prevent accidental clicks on hidden suggestions. However, when the autofill popup UI is constrained to only show one suggestion, the user is capable of accidentally clicking the hidden suggestion as soon as it comes into focus onMouseHover event.

Since this is where we determine the position of the popup on the screen, it is possible to adjust the input field size to constrain popup at the top of the screen such that only a single suggestion is shown per time. You might want to introduce a short delay such that when the hidden suggestion scrolls into focus, the user is less likely to accidentally clickjack.

`kMaximumPixelsToMoveSuggestionToCenter` in `chrome/browser/ui/views/autofill/popup/popup_base_view.cc`, alternatively, instead of moving the hidden suggestion into focus, when the mouse hovers over it, it could be moved out of focus (downwards).

`PopupScreenLocation` in `components/autofill/core/browser/autofill_client.h`

### hc...@google.com (2024-04-29)

I am unable to repro this (using 124.0.6367.63 (Official Build) (64-bit) (cohort: Control) on Windows).

Can you confirm which version of windows you're using?

### le...@gmail.com (2024-04-29)

Hello, thanks for reaching out. I'm using:

```
Edition	Windows 10 Enterprise
Version	22H2
Installed on	‎2/‎20/‎2023
OS build	19045.3086
Experience	Windows Feature Experience Pack 1000.19041.1000.0
System Type     64-bit operating system, x64-based processor
Processor       Intel(R) Core(TM) i7-6500U CPU @ 2.50GHz   2.59 GHz

```

How the poc works:
`The input size constrains autofill drop down ui to the top >> The victim can only see one autofill suggestion labeled "Click Here Fast" >> While the victim moves the mouse to click that suggestion, the mouse hovers over the hidden address suggestion beneath, causing it to scroll upwards to visibility very fast, leading to clickjacking.`

### pe...@google.com (2024-04-29)

Thank you for providing more feedback. Adding the requester to the CC list.

### le...@gmail.com (2024-04-29)

redacted

### hc...@google.com (2024-04-29)

Sorry bad question. I actually wanted to ask which version of Chrome you were using, but i see that's in the bug already, my bad. I'm unable to reproduce this.

Adding schwering@ from Autofill to take a quick look; schwering@ if this doesn't look like an issue at first glance feel free to close this quickly as wontfix.

### le...@gmail.com (2024-04-29)

You have to make sure that you have at least one physical address showing
in your autofill. In short, you need more than one options in the datalist.




Be Futuristic, Be Optimistic, Go Upwards Only

*But the path of the just is like the shining sun, That shines ever
brighter unto the perfect day. Proverbs 4:18*


On Mon, Apr 29, 2024 at 9:49 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/337222641
>
> *Changed*
>
> *hc...@google.com <hc...@google.com> added comment #7
> <https://issues.chromium.org/issues/337222641#comment7>:*
>
> Sorry bad question. I actually wanted to ask which version of Chrome you
> were using, but i see that's in the bug already, my bad. I'm unable to
> reproduce this.
>
> Adding schwering@ from Autofill to take a quick look; schwering@ if this
> doesn't look like an issue at first glance feel free to close this quickly
> as wontfix.
>
> _______________________________
>
> *Reference Info: 337222641 Autofill Drop Down List Scroll Swaps Datalist
> Leading To Clickjacking*
> component:  Public Trackers > 1362134 > Chromium
> <https://issues.chromium.org/components/1363614>
> status:  New
> reporter:  levitnudi@gmail.com
> cc:  hc...@google.com, levitnudi@gmail.com
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P4
> severity:  S4
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> BuildNumber:  124.0.6367.78
> OS:  Windows
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 337222641
> <https://issues.chromium.org/issues/337222641> where you have the roles:
> reporter, cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/337222641?unsubscribe=true>
>


### th...@chromium.org (2024-04-30)

I also cannot reproduce this. I do not see a physical address showing in my autofill (but I have an address defined in chrome://settings/addresses, and I do see autofill show up with an element like this: <input type="text" autocomplete="email">). Reporter - what requirements are needed for a physical address to show up in your POC's options list?

(Also adding schwering@ as [#comment7](https://issues.chromium.org/issues/337222641#comment7) intended to.)

### le...@gmail.com (2024-05-01)

redacted

### ja...@chromium.org (2024-05-06)

[Secondary Security Shepherd]

I was able to reproduce this issue using 124.0.6367.118 (Official Build) (64-bit).

I ended up changing the "address" field on the provided proof of concept to "street" and I had submitted a form that used that field name before opening the POC.

Here are the steps:

1. Renamed the field called in the original poc.html file to "street"
2. I created a form page just to populate the address field, that included common address fields: street city state zipcode (attached as example\_form.html)
3. I ran a server using python -m http.server 8888
4. I loaded example\_form.html and added an address and let Chrome save it
5. I loaded the reporter's modified poc.html and tried the proof of concept as the reporter had described.

I've attached the poc.html and example\_form.html and a screencast.

One thing I'll note is that in this proof of concept, if I just hover over the popup I can see the drop downlist scroll, so the user would really need to be motivated to click quickly.

Please take a look schwering@ and let us know what you think.

### ja...@chromium.org (2024-05-06)

Provisionally setting the severity to Medium following the guidelines that the browser content can tamper with trusted UI: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-medium-severity>

This can change if there are other mitigating factors.

### ja...@chromium.org (2024-05-06)

This didn't really have the same issue on Android. The Autofill appears above the keyboard. It's a little confusing, but much less so than on Desktop. I've attached a screenshot.

### le...@gmail.com (2024-05-06)

Thank you for the reproduction in [#comment11](https://issues.chromium.org/issues/337222641#comment11)!. I see you're being more careful with clicking because you already know the anticipated outcome :), in a gamified setting where one is supposed to click faster on a rabbit emoji as soon as it pops out of the hole, you may not have paused on hover. That said, consider persons with disabilities, certain conditions may not allow informed judgement with that kind of swap on a short span.

### le...@gmail.com (2024-05-06)

Yes, this only applies in Desktop, the attribute is set here `kMaximumPixelsToMoveSuggestionToCenter` in `chrome/browser/ui/views/autofill/popup/popup_base_view.cc`. For android, the autofill UI applies 500ms delay to prevent tapjacking.

### pe...@google.com (2024-05-07)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-07)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-05-17)

schwering: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ri...@google.com (2024-05-22)

[Secondary Security Shepherd]

Hi schwering@, any thoughts on the severity of the issue from [comment#11](https://issues.chromium.org/issues/337222641#comment11) and [comment#13](https://issues.chromium.org/issues/337222641#comment13)?

### ap...@google.com (2024-08-05)

Project: chromium/src
Branch: main

commit 78bdcf8fe60ffd1606089a1017e6ed4d78af7abb
Author: Dmitry Vykochko <vykochko@google.com>
Date:   Mon Aug 05 08:47:21 2024

    On desktops, accept visible enough suggestions only.
    
    This CL implements protection from quick suggestion accepting (tricking the user) at the row view level. A similar thing exists at the popup level, but there are cases where it's not enough (see  the ticket
    details). Before triggering suggestion acceptance, the row view checks
    its visible area and for how long it was present on the screen.
    
    Bug: 337222641
    Change-Id: Ic8bf0d84b0da8f684eecd7cd6b3acb5ff96acf09
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5748574
    Reviewed-by: Jan Keitel <jkeitel@google.com>
    Commit-Queue: Dmitry Vykochko <vykochko@google.com>
    Cr-Commit-Position: refs/heads/main@{#1337186}

M       chrome/browser/ui/autofill/autofill_popup_controller.h
M       chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
M       chrome/browser/ui/autofill/autofill_popup_controller_impl.h
M       chrome/browser/ui/autofill/mock_autofill_popup_controller.h
M       chrome/browser/ui/views/autofill/popup/popup_row_view.cc
M       chrome/browser/ui/views/autofill/popup/popup_row_view.h
M       chrome/browser/ui/views/autofill/popup/popup_row_view_unittest.cc
M       components/autofill/core/common/autofill_features.cc
M       components/autofill/core/common/autofill_features.h
M       testing/variations/fieldtrial_testing_config.json

https://chromium-review.googlesource.com/5748574


### ap...@google.com (2024-08-20)

Project: chromium/src
Branch: main

commit 4452bfda6404bfa27e1add0f5fe54ab65a4c1451
Author: Dmitry Vykochko <vykochko@google.com>
Date:   Tue Aug 20 08:37:39 2024

    Add a sanity check metric for the quick suggestion accepting safeguard.
    
    This CL adds a temporary metric that serves as a sanity check
    for the guarding logic. It will be removed during cleaning of
    the `feature::kAutofillPopupDontAcceptNonVisibleEnoughSuggestion`.
    
    This CL also moves feature initialization into PopupRowViewTest's
    constructor (per `base::test::ScopedFeatureList`'s recommendations)
    for all tests, as having it in the test body's manifested flaky in
    the newly added test.
    
    Bug: 337222641
    Change-Id: I588c7daa920e04ccbefabe312b8e93dd1800370a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5769240
    Commit-Queue: Dmitry Vykochko <vykochko@google.com>
    Auto-Submit: Dmitry Vykochko <vykochko@google.com>
    Reviewed-by: Jan Keitel <jkeitel@google.com>
    Cr-Commit-Position: refs/heads/main@{#1344008}

M       chrome/browser/ui/views/autofill/popup/popup_row_view.cc
M       chrome/browser/ui/views/autofill/popup/popup_row_view_unittest.cc
M       components/autofill/core/common/autofill_features.cc
M       tools/metrics/histograms/metadata/autofill/histograms.xml

https://chromium-review.googlesource.com/5769240


### le...@gmail.com (2024-08-28)

Hello,

nice job with the fix. Is this update available in the latest stable release?

### vy...@google.com (2024-08-29)

Hi, not yet, it is in the Dev channel from now (130.0.6669.0, you can track releases [here](https://chromiumdash.appspot.com/releases), higher versions must include the fix), and also behind a feature flag (`AutofillPopupDontAcceptNonVisibleEnoughSuggestion`). Thank you for the report!

### le...@gmail.com (2024-08-29)

Amazing! Thank you too.

### le...@gmail.com (2024-09-05)

Hello,

Is this bug in in consideration for vrp reward?

### sp...@google.com (2024-09-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI / web platform privilege escalation bug


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-12)

Congratulations Levit. Thank you for your efforts and reporting this issue to us!

### le...@gmail.com (2024-09-13)

Thank you so much for the reward @amy

### le...@gmail.com (2024-09-19)

redacted

### pe...@google.com (2024-12-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ji...@google.com (2026-05-23)

Reopening as the feature still needs to be rolled out and the added metric needs to be extended because it has expired.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/337222641)*
