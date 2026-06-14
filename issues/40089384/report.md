# Relative report-uri for CSP combined against wrong base

| Field | Value |
|-------|-------|
| **Issue ID** | [40089384](https://issues.chromium.org/issues/40089384) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-10-23 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/csp_open.php
2. Click go

What is the expected behavior?
CSP violation report sent to test.shhnjk.com (CSP implementor)

What went wrong?
If <base> tag is specified to cross-origin (via local-scheme docuemnt or HTML injection) and CSP report-uri is relative URL, CSP violation report can be sent to cross-origin.

This could be used to steal cross-origin information in violation report since report might contain secret information like nonce, referrer, page URL, and so on. 

Did this work before? N/A 

Chrome version: 62.0.3202.62  Channel: stable
OS Version: 10.0
Flash Version: 

I'm wondering this might further affect other report-uri features such as HPKP, XSS auditor, Expect-CT, and so on. Which I will test later today(I hope).

## Timeline

### mk...@chromium.org (2017-10-23)

Handing the CSP bits of this to Andy.

It probably also affects XSS auditor (though, given the usage of that mechanism, I suspect we can just remove the reporting rather than fixing the bug). I suspect that the remaining types you're looking at will not be affected, as they happen outside the page's context and don't have any knowledge of the base URL.

### aa...@google.com (2017-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-23)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-10-23)

[Empty comment from Monorail migration]

### s....@gmail.com (2017-10-23)

AFAI-tested, XSS auditor isn't affected.

### sh...@chromium.org (2017-10-24)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-10-24)

I don't understand why this wouldn't be considered "Working as Intended." Supporting cross-origin submission of reports seems like a feature, not a bug. Is there some spec statement that relative URIs shouldn't be combined with the BASE?

There is a bug in that we don't always combine relative URIs correctly: https://crbug.com/chromium/685371

### el...@chromium.org (2017-10-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### s....@gmail.com (2017-10-24)

I was told to file this bug on https://bugs.chromium.org/p/chromium/issues/detail?id=767635#c19

### el...@chromium.org (2017-10-24)

Ah. I think the issue here is that the spec changed.

Old: https://www.w3.org/TR/CSP3/
     Let endpoint be the result of executing the URL parser on directive’s value.

New: https://w3c.github.io/webappsec-csp/#report-violation
     Let endpoint be the result of executing the URL parser with directive’s value as the input, and violation’s url as the base URL.

That breaks the traditional behavior of relative-URI combination, but it is arguably safer.

### aa...@google.com (2017-10-24)

Yeah, this is a good bug :) Mirroring the Firefox behavior (ignoring the base URL when resolving the report-uri) seems like a good way to go.

### go...@chromium.org (2017-10-30)

[Bulk Edit]
URGENT - PTAL.
M63 Stable promotion is coming soon and your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch ASAP. Thank you.


### aw...@chromium.org (2017-11-03)

Hi andypaicu@ - are you still best placed to look at this?  Cheers!

### el...@chromium.org (2017-11-03)

Andy Paicu said he was going to pick this up again on Monday when he gets back to Munich. 

I'm skeptical that this really warrants a Release-Block status, as the issue is limited to a scenario where a site is using a relative CSP reporting URL.

As far as I can tell, the POC does the following:

1. User visits https://test.shhnjk.com/csp_open.php and clicks a hyperlink. 
2. The hyperlink href is a cross-origin url https://vuln.shhnjk.com/loc3.html and the target attribute of the hyperlink is the frame named w. 
3. The specified w frame does not exist, so Chrome creates a new tab for the URL to load in. 
4. The loc3 page creates a string of HTML containing a base URI and an image reference, then creates a blob around the string and
5. Navigates to that blob URL.
6. Now, for whatever reason, Chrome decides to apply the CSP served in test.shhnjk.com to the blob navigated by vuln.shhnjk.com (this seems like the actual bug). 

This issue complains that the violation report is being sent to vuln.shhnjk.com instead of the site that asked for it, test.shhnjk.com.

It would seem to me that "fixing" the code to send the report against the absolute URL of the page that sent the policy would entail leaking to the cross-origin site a violation report. 


### s....@gmail.com (2017-11-03)

>6. Now, for whatever reason, Chrome decides to apply the CSP served in
>test.shhnjk.com to the blob navigated by vuln.shhnjk.com (this seems like the
>actual bug). 

That's the https://crbug.com/chromium/767635. CSP is inherited from opener/parent to local-scheme (no matter who navigated it). And that's what spec says to do right now :(

### go...@chromium.org (2017-11-03)

+awhalley@, PTAL and expedite the fix if it is indeed M63 Stable blocker. Thank you.

### el...@chromium.org (2017-11-03)

Re #15: Thanks. I'd misunderstood what was happening here-- I thought the CSP was getting applied to vuln.shhnjk.com, but I see now[1] that it's only getting applied to the |blob| from vuln.shhnjk.com and only if the |blob| actually replaced the top-level document, not if the blob was in a subframe.
 
CSP is weird. :)

[1] (http://webdbg.com/test/cspinheritence.html)

### sh...@chromium.org (2017-11-06)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2017-11-06)

The CR is waiting for a review: https://chromium-review.googlesource.com/c/chromium/src/+/748321. Unfortunately lots of CSP knowing people are at TPAC this week.

Also regarding the blob inheriting the CSP cross-origin I agree that it's something that needs to be changed 

### go...@chromium.org (2017-11-06)

M63 Stable promotion is coming soon and your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge to M63 ASAP. Thank you.

### aw...@chromium.org (2017-11-07)

Hi mkwst@ - I'm not convinced this is a stable blocker, wdyt?

### an...@chromium.org (2017-11-07)

Hi  awhalley@ - I agree that it's not a stable blocker as well. I think we should take that label off.



### aw...@chromium.org (2017-11-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2017-11-08)

[Empty comment from Monorail migration]

### s....@gmail.com (2017-11-08)

Why is it severity-low?

### el...@chromium.org (2017-11-08)

Re #26: The change here is a Defense-in-Depth that helps protect a page which has a vulnerability that allows an attacker to inject a BASE element; the requirement that the page contain such a vulnerability significantly reduces the scope of this threat.

### s....@gmail.com (2017-11-08)

Base tag injection is not necessary in Victim site since we can inherit CSP cross origin. If that's the only reason then I dont understand the decision.

### el...@chromium.org (2017-11-08)

Inheritance of CSP cross-origin is indeed an interesting issue, but my understanding is that is tracked as https://crbug.com/chromium/767635.

In the POC supplied in https://crbug.com/chromium/777350#c0 for this issue, the behavior is actually *more* secure (because the CSP report goes to the "victim" site, not the attacker).

### s....@gmail.com (2017-11-08)

test.shhnjk.com is victim, and vuln.shhnjk.com is attacker. And report is sent to attacker in PoC.

https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#Medium-severity

Medium severity bugs allow attackers to read or modify limited amounts of information, or are not harmful on their own but potentially harmful when combined with other bugs. This includes ... exposure of sensitive user information that an attacker can exfiltrate.

### el...@chromium.org (2017-11-08)

Re #30: Adding information to the Proof-of-Concept would aid in its understandability (for instance, it seems unusual to name the attacker's server "vuln"). 

It would also be helpful for the report or POC to clearly specify what information is "leaked" (as far as I can tell, the interesting information is limited to the "original-policy" token in the report, which leaks information about the CSP policy?  

With regard to severity:
https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#low-severity begins "Low severity vulnerabilities are usually bugs that would normally be a higher severity, but which have extreme mitigating factors or highly limited scope."

### aa...@google.com (2017-11-08)

I don't think this should necessarily be release-blocking, but the ability to force a CSP violation report to be sent to an attacker's endpoint (if the policy specifies a relative URL as the report-uri) probably warrants more than Severity-Low.

The main reason is that this lets the attacker with an injection obtain the value of the script-src nonce. Knowing the nonce is usually sufficient to bypass CSP restrictions and execute scripts, so this allows a fairly generic bypass of the protections of nonce-based CSP (which is used by some large applications, including many at Google).

IOW I personally would be fairly sad if we let this linger for more than a few weeks.



### el...@chromium.org (2017-11-08)

RE #32: Interesting. Is there some reason that the script-src nonce ever needs to be sent as a part of the violation report?

### an...@chromium.org (2017-11-09)

This bug is not getting left around, as mentioned in #19 I have a CR that is ready for review and I expect around Monday someone should have time to have a look.

In terms of the severity discussion, "Partial CSP bypass" is one of the examples and I would argue that it applies since this can lead to a CSP bypass if a certain combination of conditions apply (as aaj@ detailed in #32).

### s....@gmail.com (2017-11-09)

Chrome has history of rating Severity-Medium to CSP bypasses which requires unsafe-inline to be present. And I think that this bug is more realistic than those.

https://bugs.chromium.org/p/chromium/issues/detail?id=669086
https://bugs.chromium.org/p/chromium/issues/detail?id=747847

### aa...@google.com (2017-11-09)

Fair enough, thanks for staying on top of this, Andy.

Re: eliding nonces from violation reports, my guess is that developers don't rely on their values, so perhaps we could strip them as a hardening measure. 

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/03b06bd7dfaae96461a43248c4dbb5eeeb616646

commit 03b06bd7dfaae96461a43248c4dbb5eeeb616646
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Nov 21 15:31:31 2017

Modified the report-uri logic to not respect base elements

When a relative URL is specified for report-uri, we should not respect
any base elements.

Spec: https://w3c.github.io/webappsec-csp/#report-violation

Bug: 777350
Change-Id: I1ca513d056047bcbe71f5faaefcd800d9f70363e
Reviewed-on: https://chromium-review.googlesource.com/748321
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#518260}
[add] https://crrev.com/03b06bd7dfaae96461a43248c4dbb5eeeb616646/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/base-uri/report-uri-does-not-respect-base-uri.sub.html
[add] https://crrev.com/03b06bd7dfaae96461a43248c4dbb5eeeb616646/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/base-uri/report-uri-does-not-respect-base-uri.sub.html.sub.headers
[modify] https://crrev.com/03b06bd7dfaae96461a43248c4dbb5eeeb616646/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp
[modify] https://crrev.com/03b06bd7dfaae96461a43248c4dbb5eeeb616646/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.h


### an...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-01-29)

awhalley@ this seems to be fixed in Chrome 64 stable. But I don't see acknowledgement as well as reward decision.

### s....@gmail.com (2018-01-29)

Oops, sorry. It's not fixed in Chrome 64.

### aw...@google.com (2018-01-31)

s.h.h.n.j.k@ - oh, can you confirm that it isn't fixed in 64 - the fix in #38 was included in 64, so we should re-open this if that fix didn't work.

### s....@gmail.com (2018-01-31)

I think it's fixed. Report isn't sent to anywhere (which might be a bug, but not a security bug).

### aw...@google.com (2018-02-06)

Thanks! The VRP Panel decided to award $500 for this report. Cheers!

### sh...@chromium.org (2018-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-21)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-23)

This issue was migrated from crbug.com/chromium/777350?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089384)*
