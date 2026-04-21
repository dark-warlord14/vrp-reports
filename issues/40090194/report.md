# Origin can be removed from modal dialogs

| Field | Value |
|-------|-------|
| **Issue ID** | [40090194](https://issues.chromium.org/issues/40090194) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>WindowDialog |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2018-01-15 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/iframer.php?url=//vuln.shhnjk.com/xssable.php?xss=%3Ciframe%3E%3C/iframe%3E%20%3Cscript%3E%20window[0].prompt(%27No%20domain%20shown%27);%20%3C/script%3E

What is the expected behavior?
Should be same as https://test.shhnjk.com/iframer.php?url=//vuln.shhnjk.com/xssable.php?xss=%3Cscript%3E%20prompt(%27domain%20shown%27);%20%3C/script%3E

What went wrong?
See Remove domain from window.prompt of following post
https://www.brokenbrowser.com/free-ticket-to-the-intranet-zone/

Did this work before? N/A 

Chrome version: 63.0.3239.132  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [Screenshot 2026-02-24 at 3.30.21 PM.png](attachments/Screenshot 2026-02-24 at 3.30.21 PM.png) (image/png, 61.1 KB)

## Timeline

### mk...@chromium.org (2018-01-15)

Yup. That looks wrong; I bet we're misinterpreting `about:blank` without walking the ancestor tree.

Not my area of expertise, but the code in https://cs.chromium.org/chromium/src/components/app_modal/javascript_dialog_manager.cc?rcl=bd0a8738015bb53b26791e12e1e54669baa58228&l=133 might be responsible, and doesn't appear to be checking the top-level origin.

CCing avi@, elawrence@, and estark@, who know more about this kind of thing than I do.

[Monorail components: Blink>WindowDialog UI>Security>UrlFormatting]

### el...@chromium.org (2018-01-15)

https://crbug.com/chromium/537452 is an old active issue in this area.

https://crbug.com/chromium/789186 concerns the idea that we probably shouldn't be treating JavaScript alert(), prompt() etc as trusted UI at all and thus shouldn't need to be showing any sort of origin information. That's in line with other UX decisions we're making (e.g. Permission Delegation) to lower the cognitive load on the user and reflect the reality that 1st party sites are ultimately responsible for the behavior of the content they embed.

### np...@chromium.org (2018-01-17)

Thanks Eric.

--> avi to decide if crbug/789186 will make this obsolete.

### sh...@chromium.org (2018-01-17)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-01-21)

Re https://crbug.com/chromium/802007#c3, yes, getting custom UI would obsolete this. That's the challenge, eh?

### bu...@chromium.org (2018-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2fefc4bd0b63b9be05846fddaaf47047f103544c

commit 2fefc4bd0b63b9be05846fddaaf47047f103544c
Author: Avi Drissman <avi@chromium.org>
Date: Thu Feb 22 20:41:01 2018

Give the JS dialog manager the alerting frame.

Back when this interface was originally designed, frames did not
have a proper type. Now that they do, plumb it through. That
allows the manager to make more intelligent decisions about
presenting the dialogs.

BUG=696454, 802007

Change-Id: I8aef92770bd80cfb00a59761ac492394b78d1953
Reviewed-on: https://chromium-review.googlesource.com/928828
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#538552}
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/android_webview/browser/aw_javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/android_webview/browser/aw_javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/chrome/browser/ui/javascript_dialogs/javascript_dialog_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/components/app_modal/javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/components/app_modal/javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/frame_host/render_frame_host_delegate.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/frame_host/render_frame_host_impl_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/browser/web_contents/web_contents_impl_unittest.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/public/browser/javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/layout_test/layout_test_javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/layout_test/layout_test_javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/shell_javascript_dialog_manager.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/content/shell/browser/shell_javascript_dialog_manager.h
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/extensions/browser/guest_view/web_view/javascript_dialog_helper.cc
[modify] https://crrev.com/2fefc4bd0b63b9be05846fddaaf47047f103544c/extensions/browser/guest_view/web_view/javascript_dialog_helper.h


### bu...@chromium.org (2018-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560

commit 5eb6e6f5c005711ee0cb3b18c8b928fb5164f560
Author: Avi Drissman <avi@chromium.org>
Date: Tue Feb 27 16:54:20 2018

Get metrics on the use of cross-origin JavaScript dialogs.

BUG=696454, 802007

Change-Id: I32982c6c34a24f67cfbb7c8fe07b943efaf90822
Reviewed-on: https://chromium-review.googlesource.com/924373
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#539461}
[modify] https://crrev.com/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560/chrome/browser/ui/javascript_dialogs/javascript_dialog_tab_helper.cc
[modify] https://crrev.com/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/5eb6e6f5c005711ee0cb3b18c8b928fb5164f560/tools/metrics/histograms/histograms.xml


### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-07-16)

avi@ -- 👋 Security Marshall here!
Could you please add a note about the remaining work here to help future Marshalls? Thanks!

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-11-25)

Friendly ping. Avi, would you be able to note what remaining work there is here? Thanks!

### av...@chromium.org (2019-12-02)

Wow, my mental context is entirely gone here.

I was talking to Emily about this. The problem here is that it’s trivial to bypass origin information in these dialogs (as is this bug) and therefore we were pondering the solution of eliminating all cross-origin dialogs of these types. The metrics in https://crbug.com/chromium/802007#c7 were to do this.

Emily, should we push forward here?

### es...@chromium.org (2019-12-02)

I think we should. +carlosil has a (P2) goal to send an I2D&R cross-origin JS dialogs this quarter, though I suspect he wouldn't mind if someone else wanted to get the ball rolling instead. I expect we'll probably need an enterprise policy+comms around this change.

### jd...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### av...@chromium.org (2020-09-29)

As per https://crbug.com/chromium/802007#c16, and as per https://chromestatus.com/feature/5148698084376576, giving to carlosil.  Removing cross-origin dialogs would moot this bug.

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

### zh...@google.com (2021-03-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-09)

Opening visibility for the upcoming FixIt. Please be aware that the information on this bug report may be sensitive.

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/802007?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WindowDialog, UI>Security>UrlFormatting]
[Monorail blocked-on: crbug.com/chromium/789186]
[Monorail components added to Component Tags custom field.]

### sp...@google.com (2025-04-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-03)

Hello Jun! We are going through some of our oldest issues tracked as security bugs. We're unsure when we'll come to a resolution on this one, but given the low potential for user harm from this issue and the time since it has been reported, we feel it's reasonable to open this up despite not being resolved.

Thank you for your past efforts in discovering and reporting this issue to us. And thank for your patience while this remains in our backlog.

### el...@chromium.org (2026-02-24)

Security shepherd: this bug seems to be gone, but it's impossible to tell when it was actually fixed. The current behavior of the PoC (still live after all these years!) is as attached - we no longer show an incorrect origin. Fixed!

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090194)*
