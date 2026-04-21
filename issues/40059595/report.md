# Security: Share hub dialog doesn't show the origin elided from the right

| Field | Value |
|-------|-------|
| **Issue ID** | [40059595](https://issues.chromium.org/issues/40059595) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-05-09 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 103.0.5051.0 (Official Build) canary (arm64)  

Operating System: macOS

**REPRODUCTION CASE**

1. Enable chrome://flags/#sharing-desktop-share-preview
2. Visit <https://long-extended-subdomain-name-containing-many-letters-and-dashes.badssl.com/>
3. Click on share hub icon
4. Observe the URL origin isn't eliding correctly

## Attachments

- [Screen Shot 2022-05-09 at 01.23.55.png](attachments/Screen Shot 2022-05-09 at 01.23.55.png) (image/png, 285.4 KB)

## Timeline

### [Deleted User] (2022-05-09)

[Empty comment from Monorail migration]

### me...@google.com (2022-05-09)

ellyjones: Could you PTAL? Thanks.

[Monorail components: UI>Browser>Sharing]

### [Deleted User] (2022-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2022-05-10)

Accepted, although this is a bug in an unlaunched experiment.

### el...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-05-18)

https://chromium-review.googlesource.com/c/chromium/src/+/3654734

### gi...@appspot.gserviceaccount.com (2022-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8beb524e1e8ae80472e15385cc38b43a5a86df16

commit 8beb524e1e8ae80472e15385cc38b43a5a86df16
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Fri May 20 00:25:55 2022

desktop-share-hub: elide URLs correctly for display

When displaying a URL in a width-limited, single-line text field, there
are complicated rules to follow to prevent misleading elisions. These
are implemented inside url_formatter::ElideUrl. This change has the
PreviewView attempt to elide the URL it's about to display using that
function.

Specifically, it does this by having the URL label react to changes in
its own layout by recomputing the elided URL text it should display.
This approach (though ugly, see the danger comment in the
implementation) appears better than the other three obvious approaches:

1. Guess the eventual width and accept that elision may be off in either
   direction, or
2. Rework the UI entirely so that the URL is not displayed as a single
   line
3. Add support to Label itself to elide as a URL - this was promising at
   first but provides no help to Labels whose text happens to include a
   URL, and was ultimately challenging to implement properly

This change takes care to ensure the full URL is still available to
screenreaders and via the tooltip.

Fixed: 1323595
Change-Id: Iad73fb3f0fc0a388391069601a4d1370b63606e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3654734
Commit-Queue: Elly Fong-Jones <ellyjones@chromium.org>
Reviewed-by: Jeffrey Cohen <jeffreycohen@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1005518}

[modify] https://crrev.com/8beb524e1e8ae80472e15385cc38b43a5a86df16/chrome/browser/ui/views/DEPS
[modify] https://crrev.com/8beb524e1e8ae80472e15385cc38b43a5a86df16/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/8beb524e1e8ae80472e15385cc38b43a5a86df16/chrome/browser/ui/views/sharing_hub/preview_view.cc


### [Deleted User] (2022-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-20)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations, Khalil! The VRP Panel has decided to award you $500 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1323595?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059595)*
