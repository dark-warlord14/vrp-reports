# CSS injection in any website using Color Enhancer extension

| Field | Value |
|-------|-------|
| **Issue ID** | [40095668](https://issues.chromium.org/issues/40095668) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2019-07-10 |
| **Bounty** | $2,000.00 |

## Description

Note: Google VRP told me to file this bug to Chrome, since this extension is owned by Chrome accessibility team

**VULNERABILITY DETAILS**  

Color Enhancer extension has following code in content script.

```
var baseUrl = window.location.href.replace(window.location.hash, '');  
style = document.createElement('style');  
style.id = STYLE_ID;  
style.setAttribute('type', 'text/css');  
style.innerHTML = cssTemplate.replace(/#/g, baseUrl + '#'); // <-- Taking unverified URL into style  
document.head.appendChild(style);  

```

**VERSION**  

Chrome Version: 75 stable  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Install <https://chrome.google.com/webstore/detail/color-enhancer/ipkjmjaledkapilfdigkgfmpekpfnkih>
2. Go to <https://www.google.com/');background-image:url('https://attack.shhnjk.com/test.jpeg>
3. Observe that CSS is injected into Google.

## Attachments

- [Capture.PNG](attachments/Capture.PNG) (image/png, 1.9 MB)

## Timeline

### pa...@chromium.org (2019-07-10)

aboxhall, can you please look into this or reassign to someone better? Thank you!

[Monorail components: Internals>Accessibility]

### Ju...@microsoft.com (2019-07-10)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-08-21)

Alice, have you had a chance to look at this bug yet, or do you have a suggestion for another owner? Thank you!

### Ju...@microsoft.com (2019-08-21)

BTW, I'm not sure if this is low severity.
This bug allows:
1. SameSite cookie bypass (because you can make request from any origin using image).
2. Breaks Site Isolation guarantee (because attacker controlled image can be loaded in any origin).

### es...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### dm...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### dm...@chromium.org (2019-08-27)

Patch up for review.

https://chromium-review.googlesource.com/c/chromium/src/+/1772571


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a6084aef9bbb5a5c4a3170ae00de0fff27da9e6

commit 0a6084aef9bbb5a5c4a3170ae00de0fff27da9e6
Author: Dominic Mazzoni <dmazzoni@chromium.org>
Date: Tue Aug 27 06:19:04 2019

Fix vulnerability in CSS ref to SVG filter in colorenhancer extension.

The colorenhancer extension adds an SVG filter to the page and then references
the filter using CSS.

At the time the extension was written, the filter couldn't be referenced using a
simple fragment with the filter ID, like:

  filter: url('#cvd');

...because this didn't work when the page had a <base href="..."> element, which
changed how all relative urls were resolved. As a result, we substituted the current
location, like this:

  filter: url('http://example.com/page.html#cvd');

This worked around the <base> issue, but introduced a vulnerability (see bug).

However, in crbug.com/470608, the underlying SVG issue was finally fixed,
so the <base> element no longer affects how url fragments are resolved to
SVG filters. So now we can fix the vulnerability by removing the substitution
of the page url.

Bug: 982812
Change-Id: I4049a82f4d0ad9eec7c2f9a39cf4194ffb656f83
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1772571
Reviewed-by: Alice Boxhall <aboxhall@chromium.org>
Commit-Queue: Dominic Mazzoni <dmazzoni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#690642}

[modify] https://crrev.com/0a6084aef9bbb5a5c4a3170ae00de0fff27da9e6/ui/accessibility/extensions/colorenhancer/manifest.json
[modify] https://crrev.com/0a6084aef9bbb5a5c4a3170ae00de0fff27da9e6/ui/accessibility/extensions/colorenhancer/src/cvd.js


### dm...@chromium.org (2019-08-27)

Code change has landed and extension update has been deployed.

I'm working on updating the deployment documentation, but otherwise this is done.


### sh...@chromium.org (2019-08-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $2,000 for this report :) 

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/982812?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095668)*
