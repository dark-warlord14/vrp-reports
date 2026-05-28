# Chrome on IOS ignores Content-Type header (and nosniff) when rendering XHTML content

| Field | Value |
|-------|-------|
| **Issue ID** | [335611025](https://issues.chromium.org/issues/335611025) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2023-32445, CVE-2024-40785 |
| **Reporter** | jo...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-04-18 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Chrome on IOS ignores Content-Type header (and nosniff) when rendering XHTML content

---

### Bug location

#### Which product or website have you found a vulnerability in?

Google Chrome

#### Which URL (or repository) have you found the vulnerability in?

<https://joaxcar.com/xss/headers/a.xhtml>

---

### The problem

#### Please describe the technical details of the vulnerability

This is essentially a bypass to the fix for this issue <https://issues.chromium.org/u/1/issues/40063810> that led to CVE-2023-32445

The previous report showed how Chrome on IOS rendered XML and SVG as HTML even when the response headers contained

```
Content-Type: text/plain
X-Content-Type-Options: nosniff

```

This is now fixed, but when working on a writeup of the issue, I noticed that the fix did not cover XHTML files.

There are two places where this happens when the `Content-Type` is `text/plain`

1, Visiting a file with a `.xhtml` extension
2. Visiting a file without extension but with a `Content-Disposition: inline; filename="name.xhtml";` header

In both of these cases Chrome on IOS (and probably all Webkit browsers) will render the content despite the `content-type` and `nosniff` headers.

You can test it by visiting <https://joaxcar.com/xss/headers/a.xhtml> in Chrome IOS
This POC page looks like this

```
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns:html="http://www.w3.org/1999/xhtml">
<html:script>alert(document.domain);</html:script>
<html:form><html:input name="test" value="asfd">
    </html:input><html:input type="submit">
    </html:input></html:form><html:iframe src="test">
    </html:iframe>
</html>

```

And is just a test to see if content is loaded or rendered as text. If you instead go to <https://joaxcar.com/xss/headers/a.xml> you will see that its not rendering

This bug has a significant impact on sites that rely on this feature to show "raw" files. You can see the issue happening here on GitLab

<https://gitlab.com/api/v4/snippets/2521058/raw>

and Bitbucket

<https://bitbucket.org/!api/2.0/snippets/joaxcartest/rqq7Kp/47b6804c1b1ec3ace5a96a665d14efc653865f89/files/hej.xhtml>

**Steps to reproduce**

1. Host this file as `test.xhtml`

```
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns:html="http://www.w3.org/1999/xhtml">
<html:script>alert(document.domain);</html:script>
</html>

```

2. Make sure the server serves this with `text/plain`. I used a .htaccess file like this

```
Header always set Content-Type "text/plain"
Header always set Content-Disposition "inline"
Header always set X-Content-Type-Options "nosniff"

```

3. Visit the file and see the alert

I used Chrome IOS version: 120.0.6099.101
IOS version: 17.4.1

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

It's possible for attackers to gain content injection or XSS on pages where content is supposed to be rendered as `plain/text`. Currently, it impacts live sites such as GitLab and Bitbucket (even if the CSP there is blocking XSS)

---

### The cause

#### What version of Chrome have you found the security issue in?

120.0.6099.101

#### Is the security issue related to a crash?

No

#### Choose the type of vulnerability

Cross-site scripting (XSS)

#### How would you like to be publicly acknowledged for your report?

Johan Carlsson (joaxcar)

## Attachments

- [test.xhtml](attachments/test.xhtml) (application/xhtml+xml, 185 B)

## Timeline

### ma...@google.com (2024-04-18)

Thanks for the report. Did you report this issue to Apple already and can you share the report number?

Assigning to ajuma@ per [issue 40063810](https://issues.chromium.org/issues/40063810).

### jo...@gmail.com (2024-04-19)

Hi again! I have reported it to Apple but I don't think that they have set up a WebKit issue for it yet. I will come back here when I get a first response from them

### pe...@google.com (2024-04-19)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-04-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-05-03)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### aj...@google.com (2024-05-03)

This is an ExternalDependency, so setting Disable-Nags.

### pe...@google.com (2024-06-18)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### aj...@google.com (2024-06-18)

> We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

This is an ExternalDependency. We have no control over when this gets fixed.

### jo...@gmail.com (2025-06-25)

Hi, I belive that this is fixed and given the CVE CVE-2024-40785

looks like its fixed in

iOS 17.6 and iPadOS 17.6 (21G101 and later)
macOS Sonoma 14.6 public beta (23G5052d and later)
tvOS 17.6 public beta (21M5045c and later)
watchOS 10.6 public beta (21U5551b and later)

best regards Johan

### mi...@google.com (2025-06-26)

Thanks for the update Johan, marking as Fixed

### ch...@google.com (2025-06-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-06-27)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### mi...@google.com (2025-06-27)

Re [#comment13](https://issues.chromium.org/issues/335611025#comment13), see [#comment9](https://issues.chromium.org/issues/335611025#comment9), this is a change shipped in iOS, we have no control over merge or release of the change.

### am...@chromium.org (2025-06-30)

This is change in webkit and shipping in Apple updates, no merge needed here. Removing merge tags.

### am...@chromium.org (2025-07-02)

I'm noticing a merge was requested (despite this being in webkit) based on this being triaged as sev-high, I'm not sure I understand the rationale and believe it was probably based on a past bug that was referenced here. However, in investigating this it appears that past bug was triaged at S2 and converted to S1 sometime later via issue tracker migration automation. Reducing the severity here to reflect this issue in isolation, which is a bit moot anyway given that this issue isn't in Chromium and we could not control prioritization or fix timelines regardless, but for future reference. 

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-02)

Thank you for your efforts and reporting this issue to us!

### jo...@gmail.com (2025-07-03)

Hi again, great to see this resolved! I am a bit confused about the bounty assessment. The report impact is the same as for <https://issues.chromium.org/u/1/issues/40063810> which was payed 3000.

I dont see how this can be “baseline || low severity” which is described like this

> Lower impact: low potential of exploitability, significant preconditions to exploit, low attacker control, low risk to users

when the report contains a fully working XSS POC and two live examples from Gitlab and Bitbucket.

There were no special preconditions and the issue led to XSS on multiple big sites that rely on text/plain being a safe content type

Maybe I misunderstood what caused this to be treated at baseline, but I would appreciate if you could take another look at the assessment here

best regards
Johan

### ch...@google.com (2025-10-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pi...@gmail.com (2026-01-01)

i think this report have only one exploit and your old one have two bugs maybe btw i am big fan of you bro.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/335611025)*
