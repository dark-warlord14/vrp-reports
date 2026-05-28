# Speculation rules conflict with BFCache, causing potentially sensitive pages to be cached when they shouldn't

| Field | Value |
|-------|-------|
| **Issue ID** | [417215501](https://issues.chromium.org/issues/417215501) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation>BFCache |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | le...@google.com |
| **Created** | 2025-05-12 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

### VULNERABILITY DETAILS

Normally bfcache is cleared on pages with a `Cache-Control: no-cache` header when cookies change.
See <https://developer.chrome.com/docs/web-platform/bfcache-ccns> for details.
However, it seems like the [Speculation Rules Api](https://developer.mozilla.org/en-US/docs/Web/API/Speculation_Rules_API) conflicts with this mechanism, causing pages to remain cached after logging out from a site for example.

### VERSION

Chrome Version: 123.0.6300.0 (Developer Build) (arm64)

Operating System: macOS 15.4.1 (24E263)

#### A bisect gives the following info:

You are probably looking for a change made after 1260232 (known good), but no later than 1260262 (first known bad).

CHANGELOG URL:
<https://chromium.googlesource.com/chromium/src/+log/57c9ed1ccc03628d9088996ad57899deec1a4aee..29c4db2dad1378977a2334ffd62e0a8876677ace>

And this commit seems to be the most likely culprit, it is the only one touching bfcache as far as I can tell:
<https://chromium.googlesource.com/chromium/src/+/9ec5a4888be7a555a95aeb7d88cc7bb603a9f0ca>

### REPRODUCTION CASE

#### First let's check the expected behavior

1. Visit <https://bfcache-speculation-rules.deno.dev/>
2. Click the **Login** button
3. Click **Home**
4. Click **View the secret page**
5. Click **Logout**
6. Click the browser back button

Observe how the page now shows 'Access restricted', as expected since the user has been logged out.

#### Now for the actual behavior with speculation rules enabled

1. Visit <https://bfcache-speculation-rules.deno.dev/>
2. This time, make sure speculation rules are enabled (click **Toggle speculation rules**)
3. Click the **Login** button
4. Click **Home**
5. Click **View the secret page**
6. Click **Logout**
7. Click the browser back button

This time, the secret content is still visible, presumably due to bfcache showing the cached content. Only after refreshing the page will it show the 'Access restricted' message.

### CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: Jesper van den Ende - Pelican Party Studios

## Attachments

- [Screen Recording 2025 05 12 at 19.24.09.clip.mp4](attachments/Screen Recording 2025 05 12 at 19.24.09.clip.mp4) (video/mp4, 991.1 KB)
- [bfcacheSpeculationRules.ts](attachments/bfcacheSpeculationRules.ts) (text/texmacs, 3.8 KB)

## Timeline

### je...@gmail.com (2025-05-12)

A screen recording of the reproduction steps are attached below

### je...@gmail.com (2025-05-12)

And this is the server code. To run this locally, you should [install Deno](https://docs.deno.com/runtime/#install-deno). You can then run this using `deno run --allow-net bfcacheSpeculationRules.ts` on the command line.

### jd...@chromium.org (2025-05-13)

I'm unable to reproduce this on Chrome Stable or on Chrome Dev. You note that you used version 123.0.6300.0. That's quite old. Are you able to reproduce this with a recent build of Chrome?

### je...@gmail.com (2025-05-13)

Yeah I'm able to reproduce it in Chrome 136.0.7103.93 (Official Build) (arm64)

Though I tried Canary just now and I can't reproduce it there for some reason.

### je...@gmail.com (2025-05-13)

I can still reproduce it in a dev build though (138.0.7178.0), so it's definitely not fixed.

### pe...@google.com (2025-05-13)

Thank you for providing more feedback. Adding the requester to the CC list.

### je...@gmail.com (2025-05-13)

I created a new Chrome profile in Canary and am able to reproduce it there as well. This is version 138.0.7177.0 (Official Build) canary (arm64)

Not entirely sure why I can't reproduce it in my default profile though.

### je...@gmail.com (2025-05-13)

I did some more digging, it seems like my default profile has `net.network_prediction_options` set to `2` in the `Preferences` file of the profile. This preference is controlled by the 'Preload pages' toggle at `chrome://settings/?search=preload`.

So in order to reproduce this, you need to make sure 'Preload pages' is enabled (which seems to be the default)

### me...@google.com (2025-05-13)

I can repro on stable (136.0.7103.93) on Linux.

I got a smaller regression range from bisect that also contains 9ec5a4888be7a555a95aeb7d88cc7bb603a9f0ca: <https://chromium.googlesource.com/chromium/src/+log/b235e278e17c364c3a7d7b41915e6a58f4453b64..9ec5a4888be7a555a95aeb7d88cc7bb603a9f0ca>

9ec5a4888be7a555a95aeb7d88cc7bb603a9f0ca is a test only change, but I also didn't see any other relevant CL in the range.

leimy: Could you PTAL as the owner of that CL?

### me...@google.com (2025-05-13)

Tentatively assigning medium severity

### le...@google.com (2025-05-14)

Thanks for the report! I investigated this and it looks like the problem is that we don't have a cookie listener for the RFH that is activated from prerenderer. Previously we [asserted](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=2992-2995;drc=7d991745c7df8fca03eafa299e6fbcfe310cd337) that the listener is already set when it's page activation, but it seems that's wrong for prerendering.

### ch...@google.com (2025-05-14)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-14)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-05-20)

Project: chromium/src  

Branch: main  

Author: Mingyu Lei [leimy@chromium.org](mailto:leimy@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6550761>

CCNS: make sure the cookie listener is added for prerendered document

---


Expand for full commit details
```
     
    Previously the cookie listen is not added for the prerendered document 
    because we only check IsInPrimaryMainFrame(), this will lead to serious 
    security problem since we won't be notified when the cookie changes 
    throughout the life time of that document. 
     
    This CL fixes the check and update the browser test with prerendering 
    case. Only a subset of the tests are updated but that should provide 
    enough coverage for the scenarios we are caring about. 
     
    Change-Id: Ia538f6f9e72c1096f1d0b4ed5ade7e2bd56e5523 
    Bug: 417215501 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6550761 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1462580}

```

---

Files:

- M `content/browser/back_forward_cache_no_store_browsertest.cc`
- M `content/browser/renderer_host/navigation_request.cc`

---

Hash: c287a87a87fd8b223af761746252ae03292024af  

Date:  Tue May 20 06:01:44 2025


---

### je...@gmail.com (2025-05-20)

I can confirm the fix has landed in 138.0.7190.0 (Official Build) canary (arm64) 
Thanks!

### ch...@google.com (2025-05-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### le...@google.com (2025-05-21)

Which CLs should be backmerged? (Please include Gerrit links.)

- <https://chromium-review.googlesource.com/6550761>

Has this fix been verified on Canary to not pose any stability regressions?

- Yes it's landed in canary for 18h, nothing bad happens

Does this fix pose any potential non-verifiable stability risks?

- No, it's strengthen the previous check in the implementation.

Does this fix pose any known compatibility risks?

- No

Does it require manual verification by the test team? If so, please describe required testing.

- Better to verify the same repro case that the reporter mentioned.

### am...@chromium.org (2025-05-22)

Not seeing any issues related to this fix on Canary or Dev -  M137 merge approved, please merge https://crrev.com/c/6550761 to branch 7151 at your earliest convenience 

### dx...@google.com (2025-05-23)

Project: chromium/src  

Branch: refs/branch-heads/7151  

Author: Mingyu Lei [leimy@chromium.org](mailto:leimy@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6581716>

[M137] CCNS: make sure the cookie listener is added for prerendered document

---


Expand for full commit details
```
     
    Previously the cookie listen is not added for the prerendered document 
    because we only check IsInPrimaryMainFrame(), this will lead to serious 
    security problem since we won't be notified when the cookie changes 
    throughout the life time of that document. 
     
    This CL fixes the check and update the browser test with prerendering 
    case. Only a subset of the tests are updated but that should provide 
    enough coverage for the scenarios we are caring about. 
     
    (cherry picked from commit c287a87a87fd8b223af761746252ae03292024af) 
     
    Change-Id: Ia538f6f9e72c1096f1d0b4ed5ade7e2bd56e5523 
    Bug: 417215501 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6550761 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1462580} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6581716 
    Cr-Commit-Position: refs/branch-heads/7151@{#1566} 
    Cr-Branched-From: 8e0d32ed6e49a2415b16e5ed402957cac2349ce2-refs/heads/main@{#1453031}

```

---

Files:

- M `content/browser/back_forward_cache_no_store_browsertest.cc`
- M `content/browser/renderer_host/navigation_request.cc`

---

Hash: 26be5f5f125c94e0e7d0df831a94f1eb23e1ad7e  

Date:  Fri May 23 06:01:46 2025


---

### pe...@google.com (2025-05-23)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### le...@google.com (2025-05-26)

> Was this issue a regression for the milestone it was found in?

The change was enabled by default here (M123): <https://chromium-review.googlesource.com/c/chromium/src/+/5283554>

> Is this issue related to a change or feature merged after the latest LTS Milestone?

A change in M137 fixes the potential issue, so M123-M136 should be the affected milestones, but throughout the period we have a feature flag guarding the problematic logic and only some portion of the users should be affected.

### pe...@google.com (2025-05-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-05-27)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6579105
2. Low - There were a few conflicts in the browser test.
3. 137
4. Yes. According to the above comment, it looks like some users can be affected by this bug although the feature flag has guarded the problematic logic.

### sp...@google.com (2025-05-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
high quality report of an exploitation mitigation bypass, but lower impact due to the low attacker utility outside of a physically local attack 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-29)

Thank you for your efforts and reporting this issue to us!

### je...@gmail.com (2025-05-29)

No worries, thank you for the award!

### dx...@google.com (2025-06-18)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Mingyu Lei [leimy@chromium.org](mailto:leimy@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6579105>

[M132-LTS] CCNS: make sure the cookie listener is added for prerendered document

---


Expand for full commit details
```
     
    Previously the cookie listen is not added for the prerendered document 
    because we only check IsInPrimaryMainFrame(), this will lead to serious 
    security problem since we won't be notified when the cookie changes 
    throughout the life time of that document. 
     
    This CL fixes the check and update the browser test with prerendering 
    case. Only a subset of the tests are updated but that should provide 
    enough coverage for the scenarios we are caring about. 
     
    (cherry picked from commit c287a87a87fd8b223af761746252ae03292024af) 
     
    Change-Id: Ia538f6f9e72c1096f1d0b4ed5ade7e2bd56e5523 
    Bug: 417215501 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6550761 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1462580} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6579105 
    Auto-Submit: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5585} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `content/browser/back_forward_cache_no_store_browsertest.cc`
- M `content/browser/renderer_host/navigation_request.cc`

---

Hash: 0cde40ffe5a744cbebcfbf934ea1e60e297a9d38  

Date:  Wed Jun 18 06:11:24 2025


---

### ch...@google.com (2025-08-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/417215501)*
