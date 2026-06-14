# CSP not inherited to popups with "javascript:"-URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40083572](https://issues.chromium.org/issues/40083572) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Blink>SecurityFeature>ContentSecurityPolicy |
| **Reporter** | x....@googlemail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2016-01-29 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36

Steps to reproduce the problem:
Popups opened in the following way execute the contained script (which then have access to the DOM of the opener) even if the page was loaded with a CSP that forbids inline-scripts (works fine in FF):

<!DOCTYPE html>
<html>
<head>
<script>
  par = 'val';
  url1 = "javascript:'<scr" + "ipt>alert(`dom: `+document.domain+`\\\nPdom:`+parent.document.domain+`\\\npar: `+opener.par);</scr" + "ipt>'";
  open(url1);
  url2 = "javascript:alert(`dom: `+document.domain+`\\\nPdom:`+parent.document.domain+`\\\npar: `+opener.par);";
  open(url2);
</script>
</head>
</html>

What is the expected behavior?
Script execution in Popup is blocked due to CSP

What went wrong?
CSP is inherited to popup opened with "javascript:"-URL

Did this work before? No 

Chrome version: 48.0.2564.97  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 20.0 r0

## Timeline

### mm...@chromium.org (2016-01-29)

Does it work for you in Google Chrome browser?

### x....@googlemail.com (2016-01-29)

[Comment Deleted]

### x....@googlemail.com (2016-01-29)

No, doesn't work in Chrome browser as expected.

And to correct my original statement:
What went wrong? 
CSP is _not_ inherited to popup opened with "javascript:"-URL

### cl...@chromium.org (2016-02-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-02-05)

Thanks for the report, but I see the same behavior in Chrome, Edge and Firefox, so can you explain the problem in a bit more detail or attach another test case?

### x....@googlemail.com (2016-02-05)

Indeed my example was a little bit too short.
So, when sending a CSP-header like
  Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-xyz'
and using 
  <script nonce="xyz">
then the script in the popups is blocked in FF/Edge but executed in Chrome.

### ke...@chromium.org (2016-02-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-07)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-02-08)

Joel, can you please take a look? Thanks.

### cl...@chromium.org (2016-02-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-08)

[Empty comment from Monorail migration]

### jw...@chromium.org (2016-02-08)

Mike, what's our policy for popups and CSP these days? Assigning to you because I think you know more about popups than I do.

### mk...@chromium.org (2016-02-09)

We ought to be inheriting the policy to popups created via `about:blank`, `javascript:`, etc. in the same way that we're inheriting into frames. We're probably not actually doing that yet (it's not in CSP2), but I've certainly added it explicitly to CSP3 (see "opener" context in https://w3c.github.io/webappsec-csp/#initialize-document-csp).

Really, if we ban inline script, we should probably block the opening of a `javascript:` URL entirely. That's not in the spec, but it makes sense.

### pa...@chromium.org (2016-02-10)

Re: #14: If you look at Navigation.MainFrameScheme in UMA (Google-internal, sorry everyone) you'll see that javascript: for main frame navigation is fully dead already. We could, and should, simply remove it.

It does not justify carrying any code complexity.

### ri...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### mk...@chromium.org (2016-02-10)

+Jochen, who was looking at something related ~last week.

That's great information, Chris. I can totally get behind that. `javascript:` navigations make me sad.

Do we have similar data for nested frames?

### dc...@chromium.org (2016-02-10)

I looked at how this metric is being measured, and I don't think it's actually accurate. This UMA is being measured in the "did commit provisional load" signal (as far as I can tell): this is ultimately triggered by the renderer in DocumentLoader::ensureWriter.

However, javscript: URL navigations don't go through DocumentLoader::ensureWriter: they go through DocumentLoader::replaceDocumentWhileExecutingJavaScriptURL =(

Also, I have a rough patch in progress that I think CSP will be able to take advantage of... see https://codereview.chromium.org/1685003002. The basic idea behind the patch is to plumb through the actual owning document more proactively, rather than try to (sometimes incorrectly) guess it after the fact.

### cl...@chromium.org (2016-02-10)

[Comment Deleted]

### ri...@chromium.org (2016-02-11)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-08-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-15)

The POC provided in #0 and #7 no longer repros in Chrome.

https://whytls.com/test/csp/popup.php
"Refused to execute JavaScript URL because it violates the following Content Security Policy directive: "script-src 'self' 'nonce-xyz'". Either the 'unsafe-inline' keyword, a hash ('sha256-...'), or a nonce ('nonce-...') is required to enable inline execution."

A similar attempt to circumvent the policy, https://whytls.com/test/csp/popup2.php also fails.



### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-07)

Thanks for the report! The VRP panel decided to reward $500. Cheers!

### aw...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-25)

This issue was migrated from crbug.com/chromium/582387?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Blink>SecurityFeature>ContentSecurityPolicy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083572)*
