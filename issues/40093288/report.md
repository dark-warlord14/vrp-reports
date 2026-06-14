# Security: XSS Auditor & History Web API can be chained to create a cross-origin covert channel

| Field | Value |
|-------|-------|
| **Issue ID** | [40093288](https://issues.chromium.org/issues/40093288) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>XSSAuditor, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | th...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-12-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

A cross-origin covert channel that can be used to leak information from a victim origin can be created by chaining the blocking mode of XSS Auditor with the History Web API.

Before we elaborate on the specifics of this attack, we'd like to draw attention to the recurring theme around information leaks made possible by the blocking mode of XSS Auditor. Case in point, there were at least three other reports that also chained XSS Auditor with another vector to achieve cross-origin information leak:

- <https://bugs.chromium.org/p/chromium/issues/detail?id=176137>
- <https://bugs.chromium.org/p/chromium/issues/detail?id=396544>
- <https://bugs.chromium.org/p/chromium/issues/detail?id=667079>

In each case, the XSS Auditor (in blocking mode) is compounded with another vector (e.g. the onload event) to create an oracle that tells a malicious origin whether or not a page on a victim origin contains a particular script. The script on the victim site may contain sensitive information and it is undesirable for the browser to allow such cross-origin leaks. Here, the second vector abetting the leak is the cross-origin `history.length` property and the conditions for the exploit are as follows:

1. The victim page must be using the blocking mode of XSS Auditor (i.e. does not specify a non-default X-XSS-Protection header)
2. The victim page does is framable (e.g. does not specify X-Frame-Options: sameorigin)
3. The victim page contains sensitive information in an inline <script> block (e.g. `<script>var secret = 42;</script>`)
4. The victim page contains a delayed redirect to another page (e.g. `<script>setTimeout(function() { document.location = "other_page.html"; }, 1000)</script>`, or `<meta http-equiv="refresh" content="2; URL=http://wikipedia.org" />`). We need a *delayed* redirect because the browser will only register the redirecting page if the redirection happens at least a certain amount of time after the page was loaded (Interestingly it seems that 1s is enough for `setTimeout` but not enough for the `Refresh` header).

At its simplest, we have a victim page that does not change the default mode of XSS protection, does not prevent framing, and contains the following inline code:

```
// https://victim.site/  
<script>var secret = 42;</script>  
<script>setTimeout(function() { document.location = "other_page.html"; }, 1000)</script>  

```

To guess the secret 42, a malicious site can simply:

1. Note down the existing `history.length` (let's call this h1)
2. Create an iframe as follows:

```
<iframe src="https://victim.site/#%3Cscript%3Evar%20secret%20=%2041;" id="abc"></iframe>  

```

3. Note the value of `history.length` after the iframe has loaded, and allowing enough time for the delayed redirect to be executed (let's call this h2)
4. Navigate the iframe to <https://victim.site/#%3Cscript%3Evar%20secret%20=%2042>;
5. Note the value of `history.length` again after the iframe has loaded, and after allowing enough time for the delayed redirect to be executed (let's call this h3)

Now, we can know if XSS Auditor had blocked either iframe src simply by observing the amount of increase in `history.length` after loading each iframe src. If an iframe src had been blocked, then loading that iframe src would only result in an increase of only 1 in `history.length`. Conversely, if an iframe src had not been blocked, then loading that iframe src would result in an increase of more than 1 in `history.length`. In this case, we will have observed that (h2 - h1) == 2 and (h3 - h2) == 1, which will allow us to deduce that the secret is 42 and not 41.

To scale this attack, we can pack multiple guesses into a single request. For example, the following query will allow us to determine if the secret is within the range of 0 - 99:

<https://victim.site/#><script>var secret = 0; var secret = 1; var secret = 2; ...; var secret = 99;

Since we now have the gadget to make "ranged queries", we can essentially bisect the value of `secret` and leak its value in log(n) requests, where n is the size of the search space of the secret. Of course, this assumes that we are able to fetch a URI of size O(n) - which is not true when n tends towards very large values.

**VERSION**  

Chrome Version: 70.0.3538.77 stable  

Operating System: Macintosh OS X 10.14.1

**REPRODUCTION CASE**

1. Add the following lines to your hosts file:  
   
   127.0.0.1 victim.site  
   
   127.0.0.1 attacker.site
2. Execute `python -m SimpleHTTPServer 80` in the directory containing both attacker.html, victim.html and destination.html
3. Visit <http://attacker.site/attacker.html> to witness the cross-origin exfiltration of inline data from <http://victim.site/victim.html>

**CREDIT INFORMATION**  

Reporter credit:

- Xinan Liu [[xinan.liu93@gmail.com](mailto:xinan.liu93@gmail.com)]
- Kai Yuan Thng [[thng.kaiyuan@gmail.com](mailto:thng.kaiyuan@gmail.com)]

## Attachments

- [attacker.html](attachments/attacker.html) (text/plain, 1.2 KB)
- [victim.html](attachments/victim.html) (text/plain, 127 B)

## Timeline

### ts...@chromium.org (2018-12-03)

Yes, but also note that wrt. the "secret", the usual conditions apply:
It must occur in the first N characters of the script block before any punctuation.
It must be low enough entropy to enumerate via brute force.

We expect those to be unlikely except in example sites.

### th...@gmail.com (2018-12-03)

> We expect those to be unlikely except in example sites.
Do we have any data to back this up?

Also, even if that were the case, isn't it already bad enough that we have a covert channel that can leak information across origins?

Lastly, I'd like to understand what are some use cases of the History.length API that would warrant it leaking cross-origin information?

### ct...@chromium.org (2018-12-03)

There seem to be two purported uses of the attack in this report:

(1) A covert channel where the two origins cooperate. This likely works well as the "target" origin can make sure the pre-conditions are met to leak the information successfully. However, I don't think we tend to consider covert channels as security bugs (as they require an attacker have access inside the target origin already).

(2) A side channel by which a malicious origin can probe a target origin and extract a secret value. Here the pre-conditions required (as stated in c#1) appear to mitigate this a lot.

The set of preconditions here on the victim page are particularly onerous, so I'm setting Security_Severity-Medium here as the preconditions seem strong and the effect is limited. (This aligns with similar prior leakage reports.)

Regarding the History length field, a cursory inspection of the spec appears to show this is intentional (https://html.spec.whatwg.org/#joint-session-history): "The joint session history of a top-level browsing context is the union of all the session histories of all browsing contexts of all the fully active Document objects that share that top-level browsing context, with all the entries that are current entries in their respective session histories removed except for the current entry of the joint session history."

It might be worth thinking about this as a cross-site channel in a post-site-isolation world. +creis@ in case he has thoughts here.

Also cross-referencing a similar but different bug: https://crbug.com/chromium/909638

[Monorail components: Blink Blink>SecurityFeature>XSSAuditor]

### cr...@chromium.org (2018-12-03)

Even if the spec were updated to remove history.length (which seems unlikely for backwards compatibility), I don't think that would be sufficient to remove the side channel.  The attacker could just count how many history.back() navigations it took to get back to a same origin page earlier in the history.  cthomp@ is correct that the notion of joint session history spans all frames in a page, for better or worse, and that seems unlikely to change.

If we're concerned about the length of the history leaking information, one option might be to keep the error page in the session history, making the number of entries the same whether the navigation succeeded or not.  nasko@ might have thoughts on that given his recent work on error pages.

[Monorail components: UI>Browser>Navigation]

### th...@gmail.com (2018-12-04)

> If we're concerned about the length of the history leaking information, one option might be to keep the error page in the session history, making the number of entries the same whether the navigation succeeded or not.

Unfortunately I don't think that will help. A victim page that redirects will still increment History.length more than a blocked error page.

### ko...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

[Monorail components: -Blink]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### th...@gmail.com (2018-12-07)

Any updates on how we're going to move forward on this? 

### cr...@chromium.org (2018-12-14)

https://crbug.com/chromium/911020#c5 is correct; the redirect would be missing.  There's no way to simulate that, but it's also a significant mitigating factor (requiring a victim page to have such a redirect).

At any rate, I think it's pretty unlikely the history API is going to change, due to the compatibility impact that would have.  Any change here would likely be on the XSS auditor side.

tsepez@: Any ideas for whether XSS auditor can mitigate this?  For example, could matches be determined on a per-token basis rather than on partial tokens, so that "secret = 123456" can't be matched one character at a time?  Or does that limit its overall effectiveness?

### ts...@chromium.org (2018-12-17)

Re #9: partial matches - we should not be triggering on partial matches, and https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/html/parser/xss_auditor.cc?rcl=99184716cea1cf5117f476b8cbdaab50f9145e28&l=844 goes to efforts to thwart this. If the page contained <script>secret=1234 and the URL contained ?x=<script>secret=123 then we will not be matching.

### sh...@chromium.org (2019-01-01)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@gmail.com (2019-01-10)

Hey all, happy new year! What's the plan for taking this forward? I'm considering using this bug as part of an upcoming CTF challenge and would love for it to be fixed/addressed before I do so.

### ts...@chromium.org (2019-01-11)

The options are limited, either reverting to mode=filter rather than blocking the page, or disabling the auditor by default unless an explicit x-xss-protection header.  Neither are appealing.

What's the timeline on your contest, and can you give us details about the page you intend to expoit?

### th...@gmail.com (2019-01-11)

> The options are limited, either reverting to mode=filter rather than blocking the page, or disabling the auditor by default unless an explicit x-xss-protection header.  Neither are appealing.

Unfortunately, I agree.

> can you give us details about the page you intend to expoit?

I was actually intending to write a challenge around it, rather that exploiting it. Sorry for being unclear.

### sh...@chromium.org (2019-01-25)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/543ab577f3ce4a1c64af827a4dbdaa37804845c2

commit 543ab577f3ce4a1c64af827a4dbdaa37804845c2
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jan 28 19:23:54 2019

XSS Auditor: Restore filter by default.

Blocking introduced a number of undesirable consequences, so
reverting to filtering is the softer option.

Bug: 922829
Bug: 911020
Bug: 909638
Bug: 870573
Bug: 709923
Bug: 702542
Bug: 654794
Change-Id: Iac5001793f0774d30460d9a86368656e85e9ecb1
Reviewed-on: https://chromium-review.googlesource.com/c/1417872
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Cr-Commit-Position: refs/heads/master@{#626651}


### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### th...@gmail.com (2019-02-19)

Hey tsepez, thanks for resolving this! May I know when will the bounty be paid out and when can I write about this publicly? Thanks again!

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-03-28)

tsepez: Can this bug be marked as Fixed, or is there additional work that needs to be done? Thanks!

### ts...@chromium.org (2019-03-28)

No, there's still work to be done.  This just makes the issue less likely.

### ts...@chromium.org (2019-04-10)

+panel because although the issue is still open, we've made most of the progress we're likely to make in the near term.

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### th...@gmail.com (2019-07-18)

Hello, when can I expect to hear from the panel?

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $500 for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-08-13)

Obsolete per https://crbug.com/968591

### sh...@chromium.org (2019-11-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2020-06-26)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/911020?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>XSSAuditor, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093288)*
