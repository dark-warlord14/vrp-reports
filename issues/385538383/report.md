# Hard coded storage bucket URL in Chrome allows for malicious Javascript / HTML to be run on numerous users without they knowledge

| Field | Value |
|-------|-------|
| **Issue ID** | [385538383](https://issues.chromium.org/issues/385538383) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>HaTS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ak...@gmail.com |
| **Assignee** | fj...@google.com |
| **Created** | 2024-12-22 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Hard coded storage bucket URL in Chrome allows for malicious Javascript / HTML to be run on numerous users without they knowledge

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://github.com/youtube/cobalt/blob/main/chrome/browser/ui/views/hats/hats_next_web_dialog.cc#L135>

---

### The problem

#### Please describe the technical details of the vulnerability

This issue appears to be affecting Chrome browsers up to at least version 122:

## -- Example of the User Agent -- Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36

While I found this issue looking at the Youtube / Cobalt Repo after some research I believe this is more generic to Chrome itself. (<https://github.com/youtube/cobalt/blob/main/chrome/browser/ui/views/hats/hats_next_web_dialog.cc#L135>)

The part in question is "HaTS" which is defined as: "HaTS (Happiness Tracking Survey) is used to service the display of surveys launched from any trigger point within Chrome."

The HaTS service has a static link to a Storage bucket that was no longer registered and I was able to take it over. I uploaded an index.html file and put a JavaScript redirect on it to a Canary Token to see if anyone loaded the page. After only a minute or two I got a hit following by another one every few minutes, constantly. All of these are coming from different IPs and there is some variety of user agents. They all are Windows or MacOS based (so far).

The fact they are executing my JavaScript means that I could replace it with malicious JavaScript and engage in more malicious behavior if I so desired. This looks like the latest versions of Chrome may no longer link to this bucket but there are numerous version of chrome still connecting to it including versions released earlier this year. This bucket should be controlled by Google to prevent attackers form leveraging this and exploiting these versions.

I am also more than willing to turn the bucket over to Google so they can lock it / control it and do any research they deem necessary. I don't want to understate that I am seeing dozens of connections per hour on this bucket attempting the load the index.html file so something should be done with this bucket.

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Currently only I can exploit this as I am the owner of the bucket but this bucket should likely be locked or at least controlled by Google to prevent further exploitation.

Any device connecting to it appears to be executing the JavaScript I put on the page. Its standard cross site scripting attack vector type stuff. This means that anything that can be done with malicious webpages / JavaScript could be done to these devices. Depending on the security / patch level etc that could mean malware or cookie / session stealing, loading up spam ads etc,

---

### The cause

#### Choose the type of vulnerability

Cross Site Script Inclusion (XSSI)

#### Does anyone else know about this vulnerability?

No, this vulnerability is private

#### Do you plan to disclose this bug publicly?

I don't know

## Attachments

- [hats1.png](attachments/hats1.png) (image/png, 143.9 KB)
- [hats3.png](attachments/hats3.png) (image/png, 82.6 KB)
- [hats4.png](attachments/hats4.png) (image/png, 12.0 KB)
- [hats2.png](attachments/hats2.png) (image/png, 332.0 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ak...@gmail.com (2024-12-22)

I have now seen up to version 124 of Chrome connecting to this bucket.
'''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'''

Also if there is any confusion the bucket is "chrome_hats_staging" I realized its in the Github source and the images but I didn't put it in the report text. You can also see my proof of takeover @ https://storage.googleapis.com/chrome_hats_staging/proof.txt

### ak...@gmail.com (2024-12-22)

Following up again it looks like the change was made to the Chromium source on April 12th this year. https://github.com/chromium/chromium/commit/423ea953436127ec9e17ee0e13ed42ab6f5bf987
At some point after that the bucket was allowed to lapse which allowed me to register it and be able to exploit this on any version of Chrome prior to that release.

### ak...@gmail.com (2024-12-22)

I conducted some further testing and downloaded a version of Chromium from March of this year (https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1280050/)

It does indeed appear that when I trigger the little survey's that pop up (ie HaTS) the page from the storage bucket is loaded. I loaded a bunch of Google pages for various products and noticed that my alert had been trigger from my ip address. I checked the tabs and sure enough there was a survey that had popped up on the Chrome help page @ https://support.google.com/chrome/answer/95417

I am having trouble getting another one to pop up anywhere but at this point I do believe that anyone running a version before April 12th of this year who receives a HaTS survey will connect to the Bucket and execute the JavaScript contained inside of it. This does NOT require any user interactions as I saw the alert from my JavaScript before I even saw the survey. 

I will work on additional testing incase I find anything else of value but let me know if there are any specific questions I can answer regarding this issue.

### ak...@gmail.com (2024-12-22)

redacted

### ak...@gmail.com (2024-12-22)

redacted

### ak...@gmail.com (2024-12-22)

I have refined my research a bit more and wanted to provide an update. I wrote some JavaScript that will record information about the user and upload it to a Google Storage Bucket. I was looking to capture the number of request and better understand what is generating them. I was able to capture that these are in fact coming from legitimate surveys. In the video I uploaded the surveys are generated showing product_specific_data={"Test+Field+1":"true","Test+Field+2":"false","Test+Field+3":"Test+value"}. This is clearly test data generated because I enabled the flag in Chrome to generate surveys. 

The data I am getting uploaded to the storage bucket is more telling to the origin. I won't post too much here since this is semi public but the first one was from a major online retailer. It looks like it generated a survey to this user on the retailers website and when it loaded up in Chrome it triggered my JavaScript. So this does look to me like its affecting regular users who are just browsing the internet with these affected versions of Chrome/Chromium. If this information would be helpful to you let me know and I can provide access to the storage bucket or I can provide a sample of the results.

view-source:https://storage.googleapis.com/chrome_hats_staging/index.html --- To see the JavaScript that is executing currently to provide me details on the requests. 

I also had a request come back for a survey w/ a google owned endpoint which I will post below. I am still seeing requests from numerous major websites not directly affiliated with Google. They are likely customers of Google using this survey services so I will avoid directly calling them out here.

Example of a legitimate survey from a user triggering my JavaScript:

trigger_id=Xrna7ZFaz0ugnJ3q1cK0Nn4Zgupz&product_specific_data={"Action":"Accepted","HadGesture":"true","OneTimePromptsDecidedBucket":"2_3","PromptDisposition":"LocationBarLeftChipAutoBubble","PromptDispositionReason":"DefaultFallback","PromptSurveyUrl":"https://www.google.ca/search?q=sofa+store+ner+me&sca_esv=9b4d23ecaaae12f0&source=hp&ei=<redacted>&iflsig=<redacted>&ved=<redacted>&uact=5&oq=sofa+store+ner+me&gs_lp=<redacted>&sclient=gws-wiz","ReleaseChannel":"stable","RequestType":"Geolocation","SurveyDisplayTime":"OnPromptResolved"}&languages=["en-US"]

### ak...@gmail.com (2024-12-22)

redacted

### ak...@gmail.com (2024-12-23)

Just as a follow up I think I have collected enough data to show to impact and likely root cause. I am going to modify the JavaScript to no longer report as there is no longer a need for any more data in my research I believe. 

### ma...@chromium.org (2024-12-23)

[Security shepherd] This appears to be a consequence of [b/358488025](https://issues.chromium.org/issues/358488025).

### ma...@chromium.org (2024-12-23)

akirassj@, thank you for bringing this to our attention.

### ak...@gmail.com (2024-12-23)

Your very welcome, Let me know if you want me to turn over the storage bucket. Since you can't "patch" previous version of Chrome that's really the key to the exploit and the key to the fix.

### fj...@google.com (2024-12-24)

Thanks for bringing this to our attention and offering to hand over the bucket!

We have updated the URL in M125 <https://chromiumdash.appspot.com/commit/423ea953436127ec9e17ee0e13ed42ab6f5bf987>, and later removed the falsely assumed unused bucket, leaving it open to take over. Newer clients are unaffected, but clients who have not been restarted since that milestone are indeed accessing the old bucket and would hence access the previous location. There are rate limits and special conditions required to trigger a HaTS survey, which means that only few of the old active clients actually hit this situation, but as [akirassj@gmail.com](mailto:akirassj@gmail.com) points out, it happens. This leaves those clients vulnerable to the reported attack.

[renewitt@google.com](mailto:renewitt@google.com), [markrowe@chromium.org](mailto:markrowe@chromium.org) can you help us with the process of handing over the bucket?

### ak...@gmail.com (2024-12-24)

Whomever needs the bucket the easiest way I have done this in the past is add you as an admin on the bucket. Then you can delete it and recreate it under whatever project it needs to be in. If you want to do it that way just give me the email to add and I will do it.

I am open to any other methods too if there is a better way to do it.

### pe...@google.com (2024-12-24)

Setting milestone because of s2 severity.

### re...@google.com (2025-01-02)

Hello, thank you very much for reporting this and working with us! Please add `renewitt@google.com` as admin on the bucket, and I will re-create it. Thanks again!

### ak...@gmail.com (2025-01-02)

Done, you have been added as an admin. Let me know if it didn't work for any reason.

### re...@google.com (2025-01-02)

Bucket has been deleted and recreated in a Chrome controlled project, so this issue is now remediated. Thanks for responding so swiftly.

Back to Security Shepherd for any further handling or assessment.

### am...@chromium.org (2025-01-02)

Thanks renewitt@ and fjacky@ for all the work, updates, and context. Closing this issue as resolved.

### pe...@google.com (2025-01-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### fj...@google.com (2025-01-02)

None of the resolutions except really match well. I've added the critique CL to the "Fixed by Code Changes" field. If the automation reopens, add to the hotlist for manual resolution.

### pe...@google.com (2025-01-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-03)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [132].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-01-03)

no relevant Chromium merge related to this issue

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Thank you reward: this issue only impacted <M125 versions of Chrome and did not impact any active release versions of Chrome at the time it was reported. We did, however, appreciate this report and would like to see types of report of this kind that potentially impact users on active release channels. 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Thank you again for your efforts and reporting this issue to us.

### ch...@google.com (2025-04-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/385538383)*
