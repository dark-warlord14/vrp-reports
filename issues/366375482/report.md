# Able to bypass URLBlocklist policy via custom_background_image

| Field | Value |
|-------|-------|
| **Issue ID** | [366375482](https://issues.chromium.org/issues/366375482) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Enterprise, UI>Browser>New Tab Page (use subcomponent)>Desktop |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cp...@gmail.com |
| **Assignee** | pa...@google.com |
| **Created** | 2024-09-13 |
| **Bounty** | $500.00 |

## Description

SUMMARY:

This report details a critical security vulnerability in Chromium (version 128.0.6613.138) that allows an attacker to bypass the URL blocklist and potentially leak user information through Server-Side Request Forgery (SSRF).

VULNERABILITY DETAILS

The chrome-untrusted://new-tab-page/custom_background_image functionality accepts user-provided URLs to fetch a background image for the new tab page.
This functionality does not enforce the URL blocklist policy, allowing requests to blacklisted URLs.

Additionally, all parameters for the request like size, positionX, and positionY etc. are susceptible to CSS injection.

Malicious CSS code within these parameters can be used to make additional requests to any URL, including blacklisted ones.
These requests include user cookies, potentially enabling authenticated SSRF attacks.

Crucially, these requests are not logged in the network logs, creating a blind spot for detection which breaks the security principle of non-repudiation.

VERSION
Chrome Version: 128.0.6613.138 (Official Build) (arm64) 
Operating System: MacOS Sonoma Version 14.6.1

REPRODUCTION CASE

Step 1:
Add 2 URLS into URLBlocklist policy, https://www.linux.com and https://www.google.com
Command:
defaults write com.google.Chrome URLBlocklist -array "https://www.linux.com"
defaults write com.google.Chrome URLBlocklist -array-add "https://www.google.com"
defaults read com.google.Chrome 

Step 2:
Navigate to chrome://policy/ and reload the policy. Confirm that policy is updated and status is OK

Step 3:
Try to navigate to https://www.linux.com" and "https://www.google.com" and see that it is blocked.

Step 4:
Navigate to chrome-untrusted://new-tab-page/custom_background_image?url=https://www.linux.com/wp-content/uploads/2019/08/favicon-300x300.png and observe that the image is loaded confirming the request is successful.

Step 5:
Open Devtools and navigate to chrome-untrusted://new-tab-page/custom_background_image?url=https://www.linux.com/wp-content/uploads/2019/08/favicon-300x300.png&size=;background-image:%20url(https://www.google.com/js/bg/heS4xvwnJ7N88fAaldUc2ARX0jFSn0IFmWsC0smzElE.js)

Confirm from devtools that both requests are made and with cookies.

Step 6:
Run this command from terminal to open the URL with payload to make request

open -a "Google Chrome" "chrome-untrusted://new-tab-page/custom_background_image?url=https://www.linux.com/wp-content/uploads/2019/08/favicon-300x300.png&size=;background-image:%20url(https://www.google.com/js/bg/heS4xvwnJ7N88fAaldUc2ARX0jFSn0IFmWsC0smzElE.js?anydata=toleak)" 



CREDIT INFORMATION
Reporter credit: Chinmay Pandya


## Timeline

### aj...@google.com (2024-09-16)

duping into [issue 40059921](https://issues.chromium.org/issues/40059921)

### cp...@gmail.com (2024-09-17)

I do not have access to 40059921

Can you let me know what is duplication in the report so that I can provide more information ?

### cp...@gmail.com (2024-09-18)

Hi, Can you give information on if the duplication if for CSS injection or URLBlockkList policy bypass?

If policy bypass is the duplication, then can I submit other pages and techniques to bypass the policy ? 

### cr...@chromium.org (2024-09-19)

ajgo@: I don't think this is a duplicate of [issue 40059921](https://issues.chromium.org/issues/40059921), since custom\_background\_image is a different endpoint not discussed there, and there are additional problems discussed in this report (such as CSS injection in the parameters). I'll split this back out.

pauladedeji@ and/or tiborg@: Can you take a look? The URLBlocklist fix issue may have a similar fix as <https://chromium-review.googlesource.com/c/chromium/src/+/4688344> from <https://crbug.com/40065551>. There may be additional work needed for the CSS injection issue.

### cp...@gmail.com (2024-09-19)

Thanks for reopening

On the same code file, there is another instance which is also not following the policy

chrome-untrusted://new-tab-page/image?https://www.linux.com/wp-content/uploads/2019/08/favicon-300x300.png

Also a question. Why this request was not showing in netlog ?

### pa...@google.com (2024-09-19)

Thanks for bringing this to my attention cpandya2909@ and creis@. The suggested fix from creis@ seems applicable here. I'll prepare a CL to implement something similar for NTP images.

### ap...@google.com (2024-09-19)

Project: chromium/src
Branch: main

commit d3a28113e036058a65e95839bf36f82a2ce5ef7a
Author: Paul Adedeji <pauladedeji@google.com>
Date:   Thu Sep 19 19:38:47 2024

    Respect policy for blocks.
    
    Change-Id: I6782e6cde51836898392a3af15a92877417a42c4
    Bug: 366375482
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5874126
    Commit-Queue: Riley Tatum <rtatum@google.com>
    Reviewed-by: Riley Tatum <rtatum@google.com>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Paul Adedeji <pauladedeji@google.com>
    Auto-Submit: Paul Adedeji <pauladedeji@google.com>
    Cr-Commit-Position: refs/heads/main@{#1357795}

M       chrome/browser/ui/webui/new_tab_page/untrusted_source.cc

https://chromium-review.googlesource.com/5874126


### pe...@google.com (2024-09-20)

Setting milestone because of s2 severity.

### ap...@google.com (2024-09-20)

Project: chromium/src
Branch: main

commit 5ade06574566c988a05b06122697155b1d086b3a
Author: Paul Adedeji <pauladedeji@google.com>
Date:   Fri Sep 20 21:13:57 2024

    Block data requests based on url_param instead of the full url.
    
    Change-Id: I35913b1cd4c97bf0e031ab8036fe6394e5d166b5
    Bug: 366375482
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876702
    Auto-Submit: Paul Adedeji <pauladedeji@google.com>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Riley Tatum <rtatum@google.com>
    Commit-Queue: Riley Tatum <rtatum@google.com>
    Cr-Commit-Position: refs/heads/main@{#1358378}

M       chrome/browser/ui/webui/new_tab_page/untrusted_source.cc
M       chrome/browser/ui/webui/new_tab_page/untrusted_source.h

https://chromium-review.googlesource.com/5876702


### cp...@gmail.com (2024-09-21)

In code change https://chromium-review.googlesource.com/5876702 similar checks should be for url_2x parameter also.

### cp...@gmail.com (2024-09-21)

Also, please add similar checks for this case also

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/new_tab_page/untrusted_source.cc;l=138

### pa...@google.com (2024-09-23)

Thanks for catching the oversight with `url_2x`. I'll send a CL out to fix that. As for the second case, I believe it is covered already. Navigating to `chrome-untrusted://new-tab-page/image?https://www.linux.com/wp-content/uploads/2019/08/favicon-300x300.png` doesn't load anything for me in the latest canary.

Also, I've followed two followup bugs to investigate why the requests don't show in the network logs & to prevent CSS injection on the background parameters ([b/369094128](https://issues.chromium.org/issues/369094128) and [b/369094511](https://issues.chromium.org/issues/369094511)).

### cp...@gmail.com (2024-09-23)

Hi. I am not sure why there is a difference but I am able to access chrome-untrusted://new-tab-page/image?https://www.linux.com/wp-content/uploads/2019/08/favicon-300x300.png

My version details

Google Chrome	129.0.6668.58 (Official Build) (arm64) 
Revision	81a06fb873a9b386848719cf9f93e59579fb5d4b-refs/branch-heads/6668@{#1318}
OS	macOS Version 14.6.1 (Build 23G93)
JavaScript	V8 12.9.202.18
User agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36

### pa...@google.com (2024-09-23)

Hey Chinmay,

The change is currently only shipping to Google Canary version 131.0.6730.0+. You'll have to download Canary if you want to verify the fix locally.

### ap...@google.com (2024-09-23)

Project: chromium/src
Branch: main

commit 6345decee9fc2a833c799750cfb3d57ea39f743b
Author: Paul Adedeji <pauladedeji@google.com>
Date:   Mon Sep 23 16:49:21 2024

    Respect policy for `url2x`.
    
    Change-Id: I748a27626e1e3f92473dea0eb676ee0bdfc4773a
    Bug: 366375482
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5882834
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Riley Tatum <rtatum@google.com>
    Auto-Submit: Paul Adedeji <pauladedeji@google.com>
    Commit-Queue: Riley Tatum <rtatum@google.com>
    Cr-Commit-Position: refs/heads/main@{#1358861}

M       chrome/browser/ui/webui/new_tab_page/untrusted_source.cc

https://chromium-review.googlesource.com/5882834


### cp...@gmail.com (2024-09-24)

For url parameter, there is check that only https and chrome-untrusted urls are accepted.

but url_2x accepts any valid url. Which can be any non http url also, like data url, javascript url.

Is there any specific reason why any url is accepted in url_2x but only https url in url parameter?

### rt...@google.com (2024-10-11)

Friendly out of SLO ping. It looks like quite a bit of work has been done for this task. I assume it isn't closed yet because of the comment from cpandya. If more time is needed, please extend the SLO time.

### ap...@google.com (2024-10-17)

Project: chromium/src  

Branch: main  

Author: Paul Adedeji <[pauladedeji@google.com](mailto:pauladedeji@google.com)>  

Link:      <https://chromium-review.googlesource.com/5933086>

[ntp] Restrict url\_2x schemes to https:// or chrome://untrusted.

---


Expand for full commit details
```
[ntp] Restrict url_2x schemes to https:// or chrome://untrusted.

Applies the same restriction we have on background URL params,
to the `url_2x` [1] associated with them, which is just meant
to be a bigger version of the same URL. This prevents
non-http urls, e.g. javascript urls from being used.

[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/new_tab_page/new_tab_page.mojom;drc=bbd749b149f5195a31b8633aae2f802331eb953c;l=61

Change-Id: Ifb2dc8a8ae614c9da78e8ca6d7c867eb5ca2239d
Bug: 366375482
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5933086
Commit-Queue: Paul Adedeji <pauladedeji@google.com>
Reviewed-by: Roman Arora <romanarora@chromium.org>
Commit-Queue: Roman Arora <romanarora@chromium.org>
Auto-Submit: Paul Adedeji <pauladedeji@google.com>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1370043}

```

---

Files:

- M `chrome/browser/ui/webui/new_tab_page/untrusted_source.cc`
- M `chrome/browser/ui/webui/new_tab_page/untrusted_source.h`

---

Hash: e20ca6527b1135bf7438cf84c665d40c069be270  

Date:  Thu Oct 17 15:45:49 2024


---

### ap...@google.com (2024-10-18)

Project: chromium/src  

Branch: main  

Author: Paul Adedeji <[pauladedeji@google.com](mailto:pauladedeji@google.com)>  

Link:      <https://chromium-review.googlesource.com/5942288>

[ntp][backgrounds] Update check for whether a url is allowed or not.

---


Expand for full commit details
```
[ntp][backgrounds] Update check for whether a url is allowed or not.

Problem: A regression was introduced by
https://chromium-review.googlesource.com/5933086,
where the scheme of a url wasn't correctly checked, since
it checks that the scheme is `http://` or `chrome://untrusted`
separately. Failing one of these checks would block the URL,
when it only needs to pass one.

Solution: Make sure scheme is http or untrusted in tandem,
instead of separately.

screencast/cast/NDkyOTYxOTQ5MTgxNTQyNHw0MGNjYzRiNy00OA

Change-Id: I77ab5e6b0306638d678902da65d4bd772f1be4c3
Bug: 374197378,366375482
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5942288
Reviewed-by: Roman Arora <romanarora@chromium.org>
Auto-Submit: Paul Adedeji <pauladedeji@google.com>
Commit-Queue: Roman Arora <romanarora@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1370647}

```

---

Files:

- M `chrome/browser/ui/webui/new_tab_page/untrusted_source.cc`

---

Hash: fdf5e0a43d9491342fd0511c6c055f4f952b1223  

Date:  Fri Oct 18 16:30:55 2024


---

### cr...@chromium.org (2024-10-31)

For reference (as discussed in <https://crbug.com/370013926>), it sounds like the URLBlocklist is not meant to comprehensively block all network connections to URLs on the list, and is only intended for navigation cases. A page may still loaded a blocked URL as a subresource, for example, according to <https://chromeenterprise.google/policies/?policy=URLBlocklist> (e.g., "If you blocked example.com/abc, then example.com could still load it using XMLHTTPRequest."). I think it's still good that this custom\_background\_image case is blocked, but that may be relevant for how other issues are considered.

### cp...@gmail.com (2024-10-31)

Hi 

On this bug, https://issues.chromium.org/issues/40065551, it is not JavaScript driven call to blocked URL but still it is considered as a vulnerability. 

### rt...@google.com (2024-10-31)

Would making our CSP more strict be a better route? We only really need to allow our background URLs, which I believe we have only a couple domain options for. That should block sub-resource as well, I believe.

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for this report of an issue that is not within Chrome's threat model, but allowed us to make a helpful change related to our defense-in-depth.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Thank you for your efforts, Chinmay, and reporting this issue to us!

### am...@google.com (2025-01-14)

updating fields to previous comment of this not being a security issue within Chrome's threat model

### pe...@google.com (2025-01-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/366375482)*
