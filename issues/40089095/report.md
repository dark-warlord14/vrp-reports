# CSP inheritance to cross-origin navigated data URL allows cross-origin info leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40089095](https://issues.chromium.org/issues/40089095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Privacy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-09-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/simple.html
2. data URL navigated by cross-origin inherited parent's CSP

What is the expected behavior?
CSP does not inherit to cross-origin navigated data URL.

What went wrong?
Chrome always inherits CSP to data URL, whether it was navigated by same-origin page or cross-origin page. Thus allowing cross-origin page to gain information of CSP by navigating data URL which contains check of various CSP directives (PoC checks img-src and style-src).

PoC shows that image request was block by parent's CSP but stylesheet was allowed. This data can be used to determine parent's website (by CSP fingerprint) and/or weakness of parent's CSP.

Did this work before? N/A 

Chrome version: 61.0.3163.79  Channel: n/a
OS Version: OS X 10.12.6
Flash Version: 

Why Chrome started blocking server side redirect to data URL even inside iframe (see second iframe)?

## Timeline

### el...@chromium.org (2017-09-21)

It would be helpful if the POC explicitly showed information about success or failure of the test.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### s....@gmail.com (2017-09-22)

Okay updated PoC to show results inside iframe. Interestingly, img-src 'self' is inherited to data URL so 'self' became data:?

I didn't explicitly show result on first PoC because attacker usually needs to detect CSP without using script (so with HTTPLeaks).

### pa...@chromium.org (2017-09-22)

meacer: You might be able to respond to the question: "Why Chrome started blocking server side redirect to data URL even inside iframe (see second iframe)?"

aaj: General CSP interest, plus: thoughts on the feasibility CSP fingerprinting? Seems potentially interesting.

Presumably this would apply to Fuchsia.

It seems like the attack would be cross-origin discovery of what other pages a person has loaded, right? And the feasibility of that depends on the feasibility/precision of CSP fingerprinting? Do I have that right?

[Monorail components: Privacy]

### aa...@google.com (2017-09-23)

I thought about this a bit and it is interesting, though I'm still not clear about the security impact of this bug.

In the case of an HTML injection an attacker can already, by design, create arbitrary new documents which inherit the policy (e.g. iframe#src=data:text/html,... or iframe#srcdoc=...) and learn things about the CSP in the vulnerable document, so it doesn't give her new capabilities.

I think in this case we're mostly interested in the scenario where there is no HTML injection but a document with CSP loads legitimate cross-origin frames, and they attack the embedding page. That is:

1. victim.com has CSP and loads an iframe from evil.com
2. evil.com calls location.replace('data:text/html,...') like in s.h.h.n.j.k's PoC.
3. The data: iframe will now be bound by victim.com's CSP and evil.com can try to extract the CSP

Since a frame generally already knows its embedder (or can figure it out via frame-ancestors) it seems that the most interesting case are sites which serve different CSPs depending on some application-specific logic, because an attacker might be able to guess the CSP rules and learn something about the user based on them. In particular, it could potentially help an attacker guess the script-src nonce by creating a chain of frames if the data: URI recursively loads an iframe from evil.com which redirects to another data: URI which probes for a different nonce value and loads another iframe from evil.com, and so on.





### s....@gmail.com (2017-09-23)

I think you misunderstood the PoC. My PoC does just same as you said. it loads vuln.shhnjk.com/loc.html, which redirect data URL.

### aa...@google.com (2017-09-23)

I was mostly attempting to summarize your PoC focusing on the practical impact on sites which use CSP, but please clarify if anything above is incorrect. Thanks! :)

### s....@gmail.com (2017-09-23)

Okay, *I* misunderstood your comment :D

Anyways I think there is a conceptual problem in CSP's spec (https://w3c.github.io/webappsec-csp/#initialize-document-csp). Inheriting CSP to "local scheme" if it has embedding document or opener browsing context, is bit weird. 

Are you sure that embedding document created local scheme (which is this bug)? And are you sure that opener opened local scheme?

In case CSP inheritance from opener works, then I think this is the only way to identify opener with CSP fingerprint (frame-ancestors won't work).

### s....@gmail.com (2017-09-23)

Quick test shows that opener case does work too.

https://test.shhnjk.com/csp_open.html

### pa...@chromium.org (2017-09-25)

+some more people who seem to have worked on CSP.

For assessing severity, I'm still hung up on how difficult it is to fingerprint a CSP policy, and how informative that would be. As for making brute-force guessing of CSP nonces feasible, that would seem to be quite severe if it is sufficiently feasible?

### pa...@chromium.org (2017-09-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-09-26)

Keeping as tentative medium based on above comments, feel free to move to low if needed.

Emily, can you please help with severity triage and any suggestion on who can own this ?

### me...@chromium.org (2017-09-26)

> meacer: You might be able to respond to the question: "Why Chrome started blocking server side redirect to data URL even inside iframe (see second iframe)?"

Sorry, just seeing this. Server side redirects to data URLs have been blocked for a long time, so this isn't related to the more recent blocking of top frame navigations to data URLs. I can't find the original bug, but https://crbug.com/chromium/723796 is about server side redirects.

nasko: Is the blocking of redirects intended for iframes as well?

### na...@chromium.org (2017-09-26)

Server redirect to data: URL has always been deemed unsafe and not allowed, regardless of top-level or subframe. It is done at the network layer.
What might have changed recently is which process does the error page commit in, but not sure if that makes a difference or not.

### sh...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-06)

estark: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2017-10-12)

Oops, sorry I missed this.

Bumping over to andypaicu.

Lowering severity because it seems like the most likely attack-scenario (nonce-guessing) would still require brute-forcing the nonce, IIUC.

### s....@gmail.com (2017-10-22)

Hi, I've found a terrible issue. When CSP report-uri of original document is relative path, attacker can simply add <base> tag on blob URL to send violation report to attacker's site. Which will leak whole CSP policy once. No brute-force or guessing required.

PoC
https://test.shhnjk.com/csp_open.php

I think severity would increase and hope that spec would change soon.

### s....@gmail.com (2017-10-22)

Note that this is general issue. If attacker has HTML injection and victim site's CSP does not have CSP base-uri set and report-uri is relative, attacker can simply inject base tag followed by any tag which triggers violation to steal CSP report. This is not the case in Firefox.

### mk...@chromium.org (2017-10-23)

That sounds like a bug in Chrome, but I think the spec matches Firefox's behavior (see step 4.2 of https://w3c.github.io/webappsec-csp/#report-violation).

I think it's a bit distinct from this bug, however: s.h.h.n.j.k@, would you mind filing a separate issue so we can track it at the right severity? (This `data:` bug still seems low, while the `base` issue seems more mediumey. :) )

Thanks!

### s....@gmail.com (2017-10-23)

Done!
https://bugs.chromium.org/p/chromium/issues/detail?id=777350

### s....@gmail.com (2017-10-23)

[Comment Deleted]

### s....@gmail.com (2017-10-23)

Filed. But I can't post URL. When I do, the comment gets deleted :(

### an...@chromium.org (2017-11-06)

Yeah I will look at trying to amend the spec, the intention was to make sure that opening a local scheme window/frame won't allow you to bypass the main page CSP. But after a navigation has occurred surely it shouldn't be inherited anymore.

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### ko...@chromium.org (2017-12-12)

andypaicu@ any progress on this? (open P1 issue without activity for 1month)

### s....@gmail.com (2018-01-23)

Hi andypaicu@

Could you somehow fix the spec bit? Edge has same issue and we are struggling because behavior is correct as per spec.

Thanks!

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-10-26)

Spec issue is in a PR, https://github.com/w3c/webappsec-csp/pull/358 starting to work at implementation.

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-12-10)

Fixed in https://chromium-review.googlesource.com/c/chromium/src/+/1353978

### sh...@chromium.org (2018-12-10)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-10)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thank you for your report, the Panel decided to reward $500 for this report. 

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/767635?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089095)*
