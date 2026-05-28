# custom tab doesnt show main domain in samsung s24 ultra 

| Field | Value |
|-------|-------|
| **Issue ID** | [395544225](https://issues.chromium.org/issues/395544225) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>CustomTabs |
| **Platforms** | Android |
| **Chrome Version** | 132.0.0.0 |
| **Reporter** | mr...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2025-02-10 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. open <https://long-extended-subdomain-name-containing-many-letters-and-dashes.badssl.com/> in samsung s24 ultra
   in custom tab chrome dev
2. then u will see domain is not showing .

# Problem Description

chrome dev in cct tab not show correct domain
test on other android device to but found out on samsung is vulnerable for it

# Summary

custom tab doesnt show main domain in samsung s24 ultra

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- VID-20250210-WA0003.mp4 (video/mp4, 17.7 MB)
- VID-20250210-WA0004.mp4 (video/mp4, 13.5 MB)
- VID-20250211-WA0006.mp4 (video/mp4, 17.9 MB)
- [VID-20250212-WA0000.mp4](attachments/VID-20250212-WA0000.mp4) (video/mp4, 41.3 MB)
- [VID-20250212-WA0001.mp4](attachments/VID-20250212-WA0001.mp4) (video/mp4, 9.6 MB)

## Timeline

### mr...@gmail.com (2025-02-11)

chrome beta is also vulnerable  i dont know but only samsung s series have these issues 

### th...@chromium.org (2025-02-11)

Hi reporter, can you confirm if the following is what you're observing?

1. Video WA0003: On the Samsung device with Chrome Dev M135 installed, navigating to the badssl page from the Google app only displays the beginning of the URL. (This is unexpected behavior.)
2. Video WA0004: On the other Android device with Chrome Dev M135 installed, navigating to the badssl page from the Google app shows a 2-line UI for the URL. The 2nd line shows the end of the URL. (This is expected behavior.)
3. Video WA0006: On the Samsung device with Chrome Beta M134 installed, navigating to the badssl page from the Google app only displays the beginning of the URL. (This is unexpected behavior.)

Also, is the clickjacking portion of the POCs needed, or is it sufficient to search for badssl through the Google app?

### mr...@gmail.com (2025-02-11)

that click jacking website is just for search purpose its a recent search so i used that . canary is also have same issue 

### th...@chromium.org (2025-02-11)

Thanks for the update. Does Stable have the same issue too?

### mr...@gmail.com (2025-02-11)

no stable dont have these issue 

### th...@chromium.org (2025-02-11)

I have not been able to reproduce this issue (no access to a Samsung device). From discussion with other folks on the security team, this seems like unexpected behavior; the address bar is editable even though it's a CCT.

Setting severity to Medium. It's borderline High but not quite, because it's not full control of the address bar (spoofing is limited to URLs that are the exact width of the address bar). Setting a speculative FoundIn of Beta M134 based on the reporter's observations (again, I was not able to reproduce this myself).

jinsukkim@ - could you PTAL?

Note: chlily@ had a guess that this may be related to this logic: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/LaunchIntentDispatcher.java;l=480;drc=f861868a309b341e766ef9748873b610ffeb3688>

### mr...@gmail.com (2025-02-11)

hi guys able to got these issue in motorolla to i think all devices have these issues

### ji...@chromium.org (2025-02-11)

cc'ing sinansahin@ for help: would like to confirm that the difference between the 2 clips comes from an experiment enabled only on one of them.

### si...@google.com (2025-02-11)

I think this is because of SICCT. @Ender, could you confirm the URL is correctly elided? Also, the toolbar looks very crowded regardless, but that's a separate conversation to have.

### pe...@google.com (2025-02-12)

Setting milestone because of s2 severity.

### pe...@google.com (2025-02-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2025-02-12)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### en...@google.com (2025-02-12)

re: [comment#10](https://issues.chromium.org/issues/395544225#comment10): Doesn't SiCCT simply draw a pill shape around the url bar embedded on CCT?

I have made very little changes to CCT visuals, def nothing that would touch the functionality of the URL bar. That does look concerning.

### ji...@chromium.org (2025-02-12)

Looks like it is indeed from SiCCT experiment. The problem is that CCT URL bar handles the URL correctly (showing the domain) while the URL in SiCCT experiment doesn't.

What is the status of the experiment - dev/canary/beta? I'd like to suggest that we not deploy it to stable until this issue is sorted out.

### en...@google.com (2025-02-12)

we were considering entering stable channel. it's not out yet. i surfaced this to our xfn team.

### go...@google.com (2025-02-12)

PTAL ASAP as this is M134 RBS and  request a merge to M134 once a safe fix  is available to merge.

Please assess and remove RBS if needed. 

### ji...@chromium.org (2025-02-12)

The feature is behind a flag that lets us control when it can go stable. Removing RBS

### ap...@google.com (2025-02-13)

Project: chromium/src  

Branch: main  

Author: Tomasz Wiszkowski <[ender@google.com](mailto:ender@google.com)>  

Link:      <https://chromium-review.googlesource.com/6257039>

Bypass CCT logic repositioning URL bar when SiCCT is Active

---


Expand for full commit details
```
Bypass CCT logic repositioning URL bar when SiCCT is Active 
 
CCT utilizes its own logic to compute URL and position it within the 
URL bar, overriding the default behavior to `SCROLL_TO_TLD`. 
 
This change disables this mechanism if the SiCCT is enabled, ensuring 
that CCT does not reposition the URL. 
 
Fixed: b:395544225 b:396203317 
Change-Id: I18a77819e31dea94b52c2fc15c8e99bed81abb17 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6257039 
Commit-Queue: Tomasz Wiszkowski <ender@google.com> 
Reviewed-by: Sinan Sahin <sinansahin@google.com> 
Cr-Commit-Position: refs/heads/main@{#1419625}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/customtabs/features/toolbar/CustomTabToolbar.java`

---

Hash: c030f3e3d45d39852daba860055cbc4768653c51  

Date:  Wed Feb 12 16:49:13 2025


---

### mr...@gmail.com (2025-02-13)

hi as i seen u fixed the issue what about reward and cve for these issue 

### th...@chromium.org (2025-02-13)

Hi reporter, thanks for filing this bug. Reward discussions will be in the coming days/weeks, and this ticket will be updated with the conclusions.

### mr...@gmail.com (2025-02-13)

hi thanks for response actualy there is no  reward hotlist aded can u please add that and may i know  is that fixed beta version is released 

### th...@chromium.org (2025-02-13)

Automation will handle the next steps. You can see https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/security-labels.md#Sheriffbot-automation for more details.

### ph...@google.com (2025-02-17)

Security Merge Request Consideration: Requesting merge to beta (M134) because latest trunk commit (1419625) appears to be after beta branch point (1415337).
Security Merge Request - Manual Review: Merge review required: M134 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### go...@google.com (2025-02-18)

+ Amy & Grace (Security TPMs) for M134 merge review. 

### am...@chromium.org (2025-02-18)

<https://crrev.com/c/6257039> approved for merge to 134, please merge this fix to branch 6998 as soon as possible as M134 Stable RC is being cut later today

### ap...@google.com (2025-02-18)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Tomasz Wiszkowski <[ender@google.com](mailto:ender@google.com)>  

Link:      <https://chromium-review.googlesource.com/6276743>

Bypass CCT logic repositioning URL bar when SiCCT is Active

---


Expand for full commit details
```
Bypass CCT logic repositioning URL bar when SiCCT is Active 
 
CCT utilizes its own logic to compute URL and position it within the 
URL bar, overriding the default behavior to `SCROLL_TO_TLD`. 
 
This change disables this mechanism if the SiCCT is enabled, ensuring 
that CCT does not reposition the URL. 
 
(cherry picked from commit c030f3e3d45d39852daba860055cbc4768653c51) 
 
Fixed: b:396222201 b:395544225 
Change-Id: I18a77819e31dea94b52c2fc15c8e99bed81abb17 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6257039 
Commit-Queue: Tomasz Wiszkowski <ender@google.com> 
Reviewed-by: Sinan Sahin <sinansahin@google.com> 
Cr-Original-Commit-Position: refs/heads/main@{#1419625} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6276743 
Reviewed-by: Gang Wu <gangwu@chromium.org> 
Owners-Override: Krishna Govind <govind@chromium.org> 
Reviewed-by: Brandon Wylie <wylieb@google.com> 
Commit-Queue: Krishna Govind <govind@chromium.org> 
Auto-Submit: Tomasz Wiszkowski <ender@google.com> 
Reviewed-by: Krishna Govind <govind@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6998@{#986} 
Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/customtabs/features/toolbar/CustomTabToolbar.java`

---

Hash: e48c26b4dcd13b97cbde59c3158225ff02ea1b00  

Date:  Tue Feb 18 09:50:14 2025


---

### ct...@chromium.org (2025-02-20)

Per prior discussions about URL display guidelines and SiCCT, do we have any way to include automated tests for these elision bugs to ensure we don't regress in the future?

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Congratulations! Thank you for your efforts and reporting this issue to us.

### mr...@gmail.com (2025-02-20)

thanks for the reward team  can u help me  on credit of these issue please give my name Bharat(mrnoob)  

### en...@google.com (2025-02-21)

Re: [comment#28](https://issues.chromium.org/issues/395544225#comment28) - technically there are render tests that capture this, but these render tests use server started on localhost, thus the url, as shown, is `127.0.0.1:12345` (or any other port), which appears insufficient to capture this.

I'm not sure how to automate this. One thing that comes to my mind is *detect if [our logic](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/UrlBarMediator.java;l=108-139;drc=7d009257d6c59f53415d7a653c06d9327b63a9b1) falls back to (or is asked to use) [`SCROLL_TO_BEGINNING`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/UrlBarMediator.java;l=124;drc=7d009257d6c59f53415d7a653c06d9327b63a9b1)*, but I am not 100% sure if there's any scenarios where this is valid.

I'm happy to research this -- and enforce -- as soon as I have any cycles left to spare. I filed <http://b/398299315> so that it stays on my radar.

### pg...@google.com (2025-02-24)

(@reporter, your credit preference has been noted!)

### mr...@gmail.com (2025-03-05)

hi i seen 134 is released but no credit no cve published

### pg...@google.com (2025-03-05)

Hi, thanks for reaching out!

As this bug was fixed before it impacted stable, we have not assigned it a cve. <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### mr...@gmail.com (2025-03-05)

no credit also ? 

### ch...@google.com (2025-05-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/395544225)*
