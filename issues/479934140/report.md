# Heap-buffer-overflow in FFmpeg (mov.c) via malformed stsd atom in MP4/DASH

| Field | Value |
|-------|-------|
| **Issue ID** | [479934140](https://issues.chromium.org/issues/479934140) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>FFmpeg |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2026-01-30 |
| **Bounty** | $7,000.00 |

## Description

---

### Report description

Heap-buffer-overflow in FFmpeg (mov.c) via malformed stsd atom in MP4/DASH

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src.git>

---

### The problem

#### Please describe the technical details of the vulnerability

The vulnerability is a Heap Buffer Overflow located within the FFmpeg stsd (Sample Description) atom parser, specifically reachable via the mov\_read\_stsd function in third\_party/ffmpeg/libavformat/mov.c.

The issue stems from insufficient validation of the entry count or atom size within the stsd box of an ISO BMFF (MP4) container. When a malformed MP4/DASH fragment provides an excessively large size for a sub-atom (as observed in my testing with an overread of 1.9GB), the parser fails to properly bounds-check the subsequent memory operations.

As shown in the attached ASan report, this results in a memory corruption event:

Allocation: A 16-byte region is allocated via av\_mallocz / av\_calloc called by mov\_read\_stsd.

Corruption: A subsequent operation attempts an out-of-bounds READ of size 8 at an offset that exceeds the allocated buffer.

Failure Point: The crash is caught by AddressSanitizer during a call to av\_freep, indicating that the heap metadata or the pointer itself was corrupted by the prior out-of-bounds access.

Because this occurs within the Renderer Process during the demuxing phase of media playback, it can be triggered remotely by a malicious website without user interaction beyond the normal loading of a video element or MediaSource object when visiting a webpage. Given that it involves a heap overflow, this could potentially be leveraged for remote code execution (RCE) within the sandboxed renderer process.

This can be reproduced by building Chrome with the following:

`gn gen out/Asan --args='is_asan=true is_debug=false symbol_level=1 enable_ncl=false ffmpeg_branding="Chrome" proprietary_codecs=true'`

`autoninja -C out/Asan chrome`

Serve the trigger.html file (with the poc\_stsd in the same directory) via python:

`python3 -m http.server 8000`

Then visit the page with the Asan build of chrome. (I used the following command from the command line and a headless browser since I was testing on a headless server install)

`ASAN_OPTIONS=symbolize=1 ./out/Asan/chrome --headless --disable-gpu --no-sandbox --disable-features=SymphoniaAudioDecoder,SymphoniaVideoDecoder --extra-ffmpeg-flags="--disable-alsa" --enable-logging=stderr http://localhost:8000/trigger.html`

#### Impact analysis

Who can exploit it? Any remote attacker who can convince a user to visit a malicious website or view a page with an embedded malformed media file. No special privileges are required, and the attack works against default configurations of Chromium-based browsers.

What do they gain? An attacker gains the ability to trigger a Renderer Process crash (Denial of Service) at minimum. More significantly, since this is a Heap Buffer Overflow, it provides a primary primitive for Remote Code Execution (RCE) within the sandboxed renderer process.

By corrupting heap metadata, an attacker could potentially hijack control flow to execute arbitrary code. While the Chrome sandbox provides a layer of defense, a successful renderer exploit is the necessary first step in a "full chain" exploit to compromise the underlying system. Given that FFmpeg is used across multiple platforms, this vulnerability likely impacts Chrome on Windows, macOS, and Linux.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chromium 146.0.7659.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tommy (dawgyg) DeVoss - Braze Security Team

## Attachments

- [trigger.html](attachments/trigger.html) (text/html, 733 B)
- [poc_stsd](attachments/poc_stsd) (application/octet-stream, 2.3 KB)
- [chrome_asan.txt](attachments/chrome_asan.txt) (text/plain, 9.6 KB)
- [trigger.html](attachments/trigger.html) (text/html, 733 B)
- [poc_stsd](attachments/poc_stsd) (application/octet-stream, 2.3 KB)

## Timeline

### an...@chromium.org (2026-02-02)

[security shepherd] [jophba@google.com](mailto:jophba@google.com), can you PTAL? I haven't tried reproducing myself, but there is an ASAN trace among the attachments.
Please re-route as necessary if you are not the right person.
Provisionally assigning S1 severity since it is a memory corruption in a renderer process.

### da...@chromium.org (2026-02-02)

=>Ted who is current ffmpeg roller.

### ch...@google.com (2026-02-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-02-03)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### tm...@chromium.org (2026-02-03)

Well, at the very least it does not seem to be caused by the most recent ffmpeg roll, so this bug has been around for some time now. I'll see what I can do about getting it fixed.

### dx...@google.com (2026-02-05)

Project: chromium/third\_party/ffmpeg  

Branch:  master  

Author:  Ted Meyer [tmathmeyer@chromium.org](mailto:tmathmeyer@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7543003>

Fix overflow in STSD parser

---


Expand for full commit details
```
     
    Reset `sc->stsd_count` before parsing entries. This number doesn't get 
    reset, which means that multiple parse passes can increment it past the 
    `sc->extradata` array end and cause OOB writes. 
     
    Bug: 479943596 
    Bug: 479934140 
    Change-Id: I3d773122251647c69ae7ea21716f87b76ff53594 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/third_party/ffmpeg/+/7543003 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org>

```

---

Files:

- M `libavformat/mov.c`

---

Hash: [9e588ab02e16326026aa61cc3b6515da20520cec](https://chromiumdash.appspot.com/commit/9e588ab02e16326026aa61cc3b6515da20520cec)  

Date: Thu Feb 5 22:54:33 2026


---

### da...@gmail.com (2026-02-05)

I can confirm the fix solves for this and the duplicate issue. I applied the patch locally, and was no longer able to get any of my poc files to work here anymore. Awesome job getting a fix figured out so quickly. (Apologies for not including one myself, was focused on getting other working. All future reports will come with a patch).

### tm...@chromium.org (2026-02-06)

https://chromium.googlesource.com/chromium/src/+/a6858b8241962b03ce5ce8ce889722ffdd0e5b4f

### tm...@chromium.org (2026-02-06)

No worries :) Appreciate the work. I'm not sure who takes over from here for the VRP side of things. I assume chrome-security-blintz-continuous-runner does a thing now.

### da...@gmail.com (2026-02-06)

It's been great working with you! This has been one of the better interactions I have had in my 10 years of bug bounty hunting, so wanted to let you all know. Hope to see ya again here soon :P

### tm...@chromium.org (2026-02-09)

The fix has also now landed in ffmpeg upstream.

### da...@gmail.com (2026-02-09)

Thanks for assisting with that!

### ch...@google.com (2026-02-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-02-12)

Fix is already in M146.

### sp...@google.com (2026-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### da...@gmail.com (2026-02-21)

Thanks for the bounty.

### ch...@google.com (2026-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/479934140)*
