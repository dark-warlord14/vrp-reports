# Security: Fetch leaks information about cross-origin redirects

| Field | Value |
|-------|-------|
| **Issue ID** | [40057322](https://issues.chromium.org/issues/40057322) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>SecurityFeature>CORS, Privacy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2021-09-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to determine if a cross-origin site redirects, similar to <https://crbug.com/chromium/1157818>.

**VERSION**  

Chrome Version: Version 93.0.4577.82 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**

```
const isRedirect = async (url) => {  
    try {  
        const foo = await fetch(url, {mode: "cors", redirect: "manual", credentials: "include"});  
        return foo.type === "opaqueredirect";  
    } catch(e) {  
        return false;  
    }  
}  

```

`await isRedirect("https://google.com")` returns true and `await isRedirect("https://www.google.com")` returns false.

It seems like the `redirect: "manual"` check is done before the CORS check, resulting in an `opaqueredirect`. When specifying `mode: "no-cors"` for example it is not allowed to use `redirect: "error"` or `redirect: "manual" and using` mode: "cors"`and`redirect: "error"` results in a CORS error.

**CREDIT INFORMATION**  

Maurice Dauer

## Timeline

### [Deleted User] (2021-09-20)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-09-20)

Yoav: Can you help further triage this one since you worked in the similar bug? Feel free to reassign as appropriate. Thanks

I did not try the reproduction case, but the report seems very plausible, nothing has changed in the related code recently, so I think this is present in 93. Triageing as medium severity since the other similar bug is also medium.

[Monorail components: Blink>JavaScript Privacy]

### [Deleted User] (2021-09-20)

[Empty comment from Monorail migration]

### yo...@chromium.org (2021-09-21)

I can confirm the issue exists, and Firefox doesn't seem to suffer from the same. At the same time, I don't think I'm the right owner here. Passing to yhirano@ for further triage.

[Monorail components: Blink>SecurityFeature>CORS]

### [Deleted User] (2021-09-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-28)

Any updates on this one?

### yh...@chromium.org (2021-09-29)

Sorry for the delay, looking...

### yh...@chromium.org (2021-09-29)

https://chromium-review.googlesource.com/c/chromium/src/+/3193481

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/27eb11a2855511c42900d82626b75bc1058d004d

commit 27eb11a2855511c42900d82626b75bc1058d004d
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Sep 29 07:58:26 2021

Run CORS check for manual redirects

...to prevent status code leak.

Bug: 1251179
Change-Id: I7fcab0daf49e16305ed53702f42d1d1eacc933e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3193481
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/main@{#926166}

[modify] https://crrev.com/27eb11a2855511c42900d82626b75bc1058d004d/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/27eb11a2855511c42900d82626b75bc1058d004d/third_party/blink/web_tests/external/wpt/fetch/api/redirect/redirect-mode.any.js


### yh...@chromium.org (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations on another one, Maurice. The VRP Panel has decided to award you $1000 for this report. Thanks for reporting this issue to us! 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1251179?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>SecurityFeature>CORS, Privacy]
[Monorail mergedwith: crbug.com/chromium/1119450]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057322)*
