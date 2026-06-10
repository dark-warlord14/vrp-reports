# From secure page it is navigating to insecure page.

| Field | Value |
|-------|-------|
| **Issue ID** | [40051067](https://issues.chromium.org/issues/40051067) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | di...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2019-12-26 |
| **Bounty** | $1,000.00 |

## Description

**Chrome Version : <Copy from: 'about:version'>**  

**URLs (if applicable) :** <https://www.airtel.in>  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Safari:Working fine  

Firefox:Working fine  

Edge:Working fine

**What steps will reproduce the problem?**  

**(1)** navigate to the following url <https://www.airtel.in>  

**(2)** single click on the address bar  

**(3)** press the enter button

**What is the expected result?**  

it should navigate to the secure url

**What happens instead?**  

It is navigating to the insecure page.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

## Attachments

- [bug file.mp4](attachments/bug file.mp4) (video/mp4, 1.4 MB)
- [secure page.mp4](attachments/secure page.mp4) (video/mp4, 1.7 MB)
- [chrome-net-export-log.json](attachments/chrome-net-export-log.json) (text/plain, 1.8 MB)
- [chrome-net-export-log2.json](attachments/chrome-net-export-log2.json) (text/plain, 6.8 MB)

## Timeline

### ph...@chromium.org (2019-12-27)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network]

### al...@chromium.org (2019-12-30)

Tested the issue on latest Stable chrome version #79.0.3945.88 using Windows10, Linux Debian and Mac 10.14.6(Mojave) and the issue is not reproducible.

Steps followed:
---------
(1)navigate to the following url https://www.airtel.in
(2)single click on the address bar
(3)press the enter button

Not-Reproducible:
Canary: 81.0.4009.0
Dev: 81.0.4000.3
Beta: 80.0.3987.16

Attached screen-cast for the reference.

@Reporter: Could you please review the attached screencast and let us know if we missed anything from our end. Could you let us know the chrome and OS version in which the issue was observed. 

Could you please let us know if the issue exists on latest stable and update your observation . You can download latest stable from https://www.chromium.org/getting-involved/dev-channel.


Thanks..

### al...@chromium.org (2019-12-30)

[Empty comment from Monorail migration]

### di...@gmail.com (2019-12-30)

we are using the same version posted in the video. OS version is Windows 8.1

### sh...@chromium.org (2019-12-30)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@google.com (2019-12-30)

I tried to locally repro the issue, it only happened on the first before I selected netlog. All the subsequent runs are successful. HTTP 502 is usually a server error. I wonder if it's just a server glitch. 

divagaruser@: how often does this happen for you? Could you collect a netlog when it repros? Instructions can be found here: https://chromium.org/for-testers/providing-network-details

### di...@gmail.com (2020-01-02)

I have attached the json file

### sh...@chromium.org (2020-01-02)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### di...@gmail.com (2020-01-02)

I have attached the json file with bytes

### di...@gmail.com (2020-01-02)

It is happening frequently

### zh...@google.com (2020-01-02)

It looks like a server issue, the server materialistically replied 502 to your http request.
 
t= 4749 [st=   4]        HTTP_TRANSACTION_SEND_REQUEST_HEADERS
                         --> GET / HTTP/1.1
                             Host: airtel.in
                             Connection: keep-alive
                             Upgrade-Insecure-Requests: 1
                             User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36
                             Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
                             Accept-Encoding: gzip, deflate
                             Accept-Language: en-US,en;q=0.9
t= 4749 [st=   4]     -HTTP_TRANSACTION_SEND_REQUEST
t= 4749 [st=   4]     +HTTP_TRANSACTION_READ_HEADERS  [dt=9454]
t= 4749 [st=   4]        HTTP_STREAM_PARSER_READ_HEADERS  [dt=9454]
t=14203 [st=9458]        HTTP_TRANSACTION_READ_RESPONSE_HEADERS
                         --> HTTP/1.1 502 Connection reset by peer
                             Date: Thu, 02 Jan 2020 07:21:37 GMT
                             Cache-Control: no-cache
                             Pragma: no-cache
                             Content-Type: text/html; charset="UTF-8"
                             Content-Length: 0
                             Via: HTTP/1.1 forward.http.proxy:3128
                             Connection: close

When I tried to repro it locally by sending the HTTP request, I got 301 from the server, which then prefetch the 
t=193967 [st= 832]   +URL_REQUEST_START_JOB  [dt=3]
                      --> load_flags = 263168 (CAN_USE_RESTRICTED_PREFETCH | MAIN_FRAME_DEPRECATED)
                      --> method = "GET"
                      --> privacy_mode = 0
                      --> url = "http://www.airtel.in/"
t=193967 [st= 832]      URL_REQUEST_REDIRECT_JOB
                        --> reason = "HSTS"
t=193968 [st= 833]      URL_REQUEST_FAKE_RESPONSE_HEADERS_CREATED
                        --> HTTP/1.1 307 Internal Redirect
                            Location: https://www.airtel.in/
                            Non-Authoritative-Reason: HSTS
t=193968 [st= 833]      URL_REQUEST_DELEGATE_RECEIVED_REDIRECT  [dt=2]
t=193970 [st= 835]      URL_REQUEST_REDIRECTED
                        --> location = "https://www.airtel.in/"
t=193970 [st= 835]   -URL_REQUEST_START_JOB
t=193970 [st= 835]    NETWORK_DELEGATE_BEFORE_URL_REQUEST  [dt=0]
t=193970 [st= 835]   +URL_REQUEST_START_JOB  [dt=370]
                      --> load_flags = 263168 (CAN_USE_RESTRICTED_PREFETCH | MAIN_FRAME_DEPRECATED)
                      --> method = "GET"
                      --> privacy_mode = 0
                      --> url = "https://www.airtel.in/"

[Monorail components: Blink>Loader]

### di...@gmail.com (2020-01-03)

Thanks for the clarification.

### pa...@chromium.org (2020-01-03)

Can we close this bug as it looks like all request are secure and the 502 error is coming from the server?

### or...@chromium.org (2020-01-07)

This is an Omnibox bug, subtly caused by "elision" of the URL schema. Websites build their servers to work around it by redirecting http:// requests to https:// . Complexity and glitches can result on some servers, but the basic behavior is flawed even in common cases. Try this, to see:

* Open a new tab and access the Network section of the Inspector panel.
* Type into the location bar, `https://google.com` and press enter.
* Mouse over the top google.com request to see that the request went to https://google.com as expected. That's port 443.
* Now single click the address bar and press enter.
* Mouse over the top google.com request to see that the request went to http://google.com as expected. That's port 80, clearly a different endpoint.

What should have happened instead? The location bar shouldn't have "forgotten" the explicitly given https:// address. But it does, and that's a bug. It's not terrible because at least the domain name is kept, which means we'll talk to the right server -- but the site is obligated to serve on port 80 or else risk dropping visitors, even when they started with the correct address. And so they do!

Bumping the priority and looping in the URL elision experts because I'm concerned that similar glitches may change the state of the world further with www elision. Name resolution changes will hassle web developers even more than port redirects. Browser quirks shouldn't force websites to redirect port 80 to 443, or <hostname> to www.<hostname>. But presently, it's happening.

[Monorail components: UI>Browser>Omnibox]

### to...@chromium.org (2020-01-07)

I'll take a look.

### to...@chromium.org (2020-01-07)

This was the CL that regressed it:
https://chromium-review.googlesource.com/c/chromium/src/+/1854501/4/components/omnibox/browser/omnibox_edit_model.cc

### zh...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### zh...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Network]

### to...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### to...@chromium.org (2020-01-09)

Patch is in review: https://chromium-review.googlesource.com/c/chromium/src/+/1990253

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c2c9d409656ea561a7abdac1381d69d928a51a8b

commit c2c9d409656ea561a7abdac1381d69d928a51a8b
Author: Tommy Li <tommycli@chromium.org>
Date: Fri Jan 10 18:45:43 2020

[omnibox] Fix losing HTTPS for elided URLs when user reloads page

Currently, for elided HTTPS URLs, (omnibox displays 'google.com'
instead of 'https://www.google.com'), when the user mouse clicks into
the omnibox and presses Enter, we make a request to http://google.com.

This is a regression introduced in this CL:
https://chromium-review.googlesource.com/c/chromium/src/+/1854501

This CL is a partial revert of that CL. I think the reverted part wasn't
necessary to fix the original bug in the first place, and was likely
included by mistake.

This CL does the partial revert and also enhances our existing unit
test to make sure it won't happen again.

Bug: 1037889
Change-Id: Ia5e742c02ac35f7b013ce42bc01c1217304ab303
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1990253
Commit-Queue: Tommy Li <tommycli@chromium.org>
Reviewed-by: Kevin Bailey <krb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#730245}

[modify] https://crrev.com/c2c9d409656ea561a7abdac1381d69d928a51a8b/components/omnibox/browser/omnibox_edit_model.cc
[modify] https://crrev.com/c2c9d409656ea561a7abdac1381d69d928a51a8b/components/omnibox/browser/omnibox_edit_model_unittest.cc


### to...@chromium.org (2020-01-10)

We need to verify this on Monday when Canary comes out, then backmerge this to 80.

### to...@chromium.org (2020-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-11)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-01-13)

tommycli@ pls confirm the questions in https://crbug.com/chromium/1037889#c24 for merge review.

### to...@chromium.org (2020-01-13)

As of Canary build 81.0.4023.0, it's not fixed yet.

That's not surprising since that build was from Jan 10.

We can re-confirm when the next one comes out.

### sr...@google.com (2020-01-13)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-14)

pls confirm canary is working fine. 81.0.4026.0 is available since yesterday afternoon.

### to...@chromium.org (2020-01-14)

I can confirm it's working in Canary. I suggest we merge to 80.

### sr...@google.com (2020-01-14)

merge approved for M80, branch:3987, pls merge to branch asap.

### to...@chromium.org (2020-01-14)

One thing that confuses me: Did Merge Cherry Picks suddenly need someone to approve it (other than myself)?

In the past, if I LGTMed it myself and submitted to CQ, it would always accept it.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/edc25657f7e9f954f440ebbb4085b39f777daf92

commit edc25657f7e9f954f440ebbb4085b39f777daf92
Author: Tommy Li <tommycli@chromium.org>
Date: Tue Jan 14 18:36:06 2020

[omnibox] Fix losing HTTPS for elided URLs when user reloads page

Currently, for elided HTTPS URLs, (omnibox displays 'google.com'
instead of 'https://www.google.com'), when the user mouse clicks into
the omnibox and presses Enter, we make a request to http://google.com.

This is a regression introduced in this CL:
https://chromium-review.googlesource.com/c/chromium/src/+/1854501

This CL is a partial revert of that CL. I think the reverted part wasn't
necessary to fix the original bug in the first place, and was likely
included by mistake.

This CL does the partial revert and also enhances our existing unit
test to make sure it won't happen again.

(cherry picked from commit c2c9d409656ea561a7abdac1381d69d928a51a8b)

Bug: 1037889
Change-Id: Ia5e742c02ac35f7b013ce42bc01c1217304ab303
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1990253
Commit-Queue: Tommy Li <tommycli@chromium.org>
Reviewed-by: Kevin Bailey <krb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#730245}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2001287
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#526}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/edc25657f7e9f954f440ebbb4085b39f777daf92/components/omnibox/browser/omnibox_edit_model.cc
[modify] https://crrev.com/edc25657f7e9f954f440ebbb4085b39f777daf92/components/omnibox/browser/omnibox_edit_model_unittest.cc


### to...@chromium.org (2020-01-14)

[Empty comment from Monorail migration]

### di...@gmail.com (2020-01-20)

When this fix will be released in chrome.

### di...@gmail.com (2020-01-22)

Hi , 

Can we expect any rewards or recognition for this bug ? Kindly let me know 

Thanks,
Divagar S


### or...@google.com (2020-01-22)

It is a significant bug, thank you for raising it!

The only rewards program that I'm aware of is for security bugs:
https://www.google.com/about/appsecurity/chrome-rewards/

I'm not familiar with that process, but I went ahead and filed a bug to the security team to evaluate the threat level and to see if this bug qualifies for a reward.

### es...@chromium.org (2020-01-22)

Re-triaging as a security bug. You can see https://www.google.com/about/appsecurity/chrome-rewards/ (as mentioned in #37) for an explanation of the process for how this is evaluated for a reward. However, I'm not sure if this will be eligible for a reward because it was filed publicly initially.

[Monorail components: -Blink>Loader]

### es...@chromium.org (2020-01-22)

[Empty comment from Monorail migration]

### di...@gmail.com (2020-01-23)

Thanks for replying . I would like to know when will i be able to know if this bug qualifies for a reward . 

Regards,
Divagar S

### ad...@chromium.org (2020-01-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-01-23)

divagaruser@ - thanks for the report. It will go to the VRP panel to see if it qualifies for a reward.

You will be credited in the Chrome release notes for reporting this. How would you like to be credited?

### sh...@chromium.org (2020-01-23)

[Empty comment from Monorail migration]

### di...@gmail.com (2020-01-24)

Hi ,

I really appreciate your kind response , Thank you so much . I do have an account in googlepay. 
It is divagaruser@okhdfcbank

Thanks ,
Divagar S

### di...@gmail.com (2020-01-24)

Credits 

Divagar S  - Quality Analyst - Karya Technologies 
Bharathi V - Associate Quality Analyst  - Karya Technologies

### ad...@google.com (2020-01-28)

Thanks for the credit information. If it's OK with you, I will abbreviate that to "Divagar S and Bharathi V from Karya Technologies" so it fits.

### di...@gmail.com (2020-01-29)

Okay , Thank you 
I really appreciate it .

Regards,
Divagar S

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $1,000 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### di...@gmail.com (2020-01-30)

Hi ,

It is our pleasure to receive this reward .  Thank you so much
Could you please tell me the procedure to claim this reward and the processing time to receive this award ?

Thanks 
Divagar S

### ad...@chromium.org (2020-01-31)

Hello divagaruser@, I don't know the processing time and I'm afraid the person who usually handles this is away for a few days. But I can tell you that you don't need to *do* anything - someone from our finance team will get in touch with you.

Thanks again for the report.

### to...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-21)

This issue was migrated from crbug.com/chromium/1037889?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1038746, crbug.com/chromium/1040003, crbug.com/chromium/1044718]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051067)*
