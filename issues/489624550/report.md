# SpeechSynthesis audio can appear to originate from another domain after fast redirect (UI/Audio Spoofing – may trick users / tricky victim)

| Field | Value |
|-------|-------|
| **Issue ID** | [489624550](https://issues.chromium.org/issues/489624550) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Speech |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ec...@gmail.com |
| **Assignee** | ev...@google.com |
| **Created** | 2026-03-04 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

SpeechSynthesis audio can appear to originate from another domain after fast redirect (UI/Audio Spoofing – may trick users / tricky victim)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://cnfdnfial-ops.github.io/spoof/poc.html>

---

### The problem

#### Please describe the technical details of the vulnerability

A vulnerability has been identified in Chromium-based browsers where audio generated via the **Web Speech API (`speechSynthesis`)** can persist after a page navigation or redirect. According to the specification, `speechSynthesis` is **document-bound** and all utterances should terminate when the page is unloaded. In this case, a PoC demonstrates that speech audio can continue to play on the target page (e.g., `https://google.com`) after redirecting from the originating page.

---

**Steps to Reproduce:**

1. Open a test HTML page containing a button that triggers `speechSynthesis.speak()`.
2. Immediately after invoking `speechSynthesis.speak()`, redirect to another page using `window.location.href`.
3. Observe that the speech continues playing on the target page.

**PoC Example:**

```
<button onclick="
  const utter = new SpeechSynthesisUtterance('This is a test message.');
  speechSynthesis.speak(utter);
  setTimeout(() => { window.location.href='https://google.com'; }, 1000);
">Test</button>

```

---

**Expected Behavior:**
All speech utterances should terminate immediately when the page is unloaded or navigated away. No audio should persist on the destination page.

**Actual Behavior:**
Speech audio continues playing on the destination page after the redirect, effectively bypassing page boundaries.

---

**Impact / Security Implications:**

- **Cross-Origin Audio Injection:** Audio from one origin can play on a different origin without user consent.
- **Social Engineering / Phishing Potential:** A malicious page could redirect a user to a trusted site and continue playing audio messages, potentially misleading users.
- **User Experience / Privacy Risk:** Unexpected audio from unrelated origins can confuse or alarm users, violating trust expectations.

---

**Root Cause:**
Chromium currently does not properly terminate active `speechSynthesis` utterances when a page unloads or navigates away. The audio context from the original page leaks into the new page context.

**Recommended Mitigation:**
Ensure all active `speechSynthesis` utterances are canceled during page unload or navigation events (`beforeunload` or `unload`) to enforce strict page-bound behavior.

---

#### Impact analysis

## Impact and Potential Impact

**Immediate Impact:**

- Audio from the originating page continues to play on the destination page after navigation, violating the expected **document-bound behavior** of the Web Speech API (`speechSynthesis`).
- Users may hear messages originating from a different site without their consent, leading to confusion or disruption of the intended user experience.

**Potential Security and Privacy Implications:**

1. **Cross-Origin Audio Injection:**
   
   - Malicious sites could use this behavior to play audio on trusted or high-profile domains (e.g., `google.com`) without permission.
   - This represents a potential vector for **cross-origin abuse** of audio output.
2. **Phishing and Social Engineering:**
   
   - Attackers could redirect users from a malicious site to a legitimate site and continue playing misleading messages.
   - Users might perceive the audio as originating from the trusted site, increasing susceptibility to phishing or deceptive instructions.
3. **User Experience and Trust Risks:**
   
   - Unexpected or unauthorized audio on high-profile sites can erode user trust.
   - This can also cause accessibility or usability issues, especially if users rely on predictable audio feedback.
4. **Spec Compliance Issue:**
   
   - The Web Speech API specification dictates that speech utterances must terminate when a page unloads.
   - Allowing audio to persist across navigations represents a **violation of expected standards**, which could affect other browsers and future web platform implementations.

**Severity Consideration:**

- While not a direct code-execution vulnerability, the combination of **cross-origin audio leakage** and potential social engineering makes this a **high-impact UX/security issue**, especially for high-trust domains.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 145.0.7632.160 (Official Build) (64-bit)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Mixed content

#### How would you like to be publicly acknowledged for your report?

Qadhafy Muhammad Tera

## Attachments

- [RESULT.png](attachments/RESULT.png) (image/png, 41.2 KB)
- [POC CHROME WINDOWS 145.0.7632.117 .mp4](attachments/POC CHROME WINDOWS 145.0.7632.117 .mp4) (video/mp4, 13.8 MB)
- [POC-Chrome&ChromeCanary-Andro.mp4](attachments/POC-Chrome&ChromeCanary-Andro.mp4) (video/mp4, 5.4 MB)
- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [chromeCanary-Windows.mp4](attachments/chromeCanary-Windows.mp4) (video/mp4, 21.9 MB)
- [voice icon.png](attachments/voice icon.png) (image/png, 14.7 KB)
- [chrome and chrome canary.mp4](attachments/chrome and chrome canary.mp4) (video/mp4, 9.0 MB)
- [2026-03-13 15-29-58.mp4](attachments/2026-03-13 15-29-58.mp4) (video/mp4, 13.7 MB)
- [android.mp4](attachments/android.mp4) (video/mp4, 2.7 MB)
- [Record_2026-03-18-15-17-18.mp4](attachments/Record_2026-03-18-15-17-18.mp4) (video/mp4, 1.6 MB)
- [ScreenRecording_03-26-2026 11-47-55_1.MP4](attachments/ScreenRecording_03-26-2026 11-47-55_1.MP4) (video/mp4, 6.4 MB)
- [Record_2026-04-24-22-53-11.mp4](attachments/Record_2026-04-24-22-53-11.mp4) (video/mp4, 2.0 MB)
- [voice-icon.jpg](attachments/voice-icon.jpg) (image/jpeg, 128.3 KB)

## Timeline

### ec...@gmail.com (2026-03-04)

**Browsers:**

- **Chrome for Windows:** Version 145.0.7632.160 (Official Build) (64-bit)
- **Chrome for Android:** Version 145.0.7632.120
- **Chrome android Canary:** Version 147.0.7716.0

**Operating System:**

- **Windows 10** (64-bit)
- **Android 14** on **Oppo Reno 7**

**Devices Tested:**

- Desktop PC running Windows
- Mobile device: Oppo Reno 7 (Android 14)

**Notes:**

- The issue is reproducible across **both desktop and mobile Chromium-based browsers**, including stable Chrome and Canary builds.
- Behavior observed consistently when performing a **speechSynthesis speak() followed by immediate redirect**.

### ec...@gmail.com (2026-03-04)

affected Version 147.0.7716.0 (Official Build) canary (64-bit)

### ec...@gmail.com (2026-03-04)

List Affected
Browsers:

windows

Chrome for Windows: Version 145.0.7632.160 (Official Build) (64-bit)

Chrome Canary for windows: Version 147.0.7716.0 (Official Build) canary (64-bit)

mobile

Chrome for Android: Version 145.0.7632.120

Chrome android Canary: Version 147.0.7716.0

### ec...@gmail.com (2026-03-04)

voice icon on google.com

### ec...@gmail.com (2026-03-04)

**Clarification (Chrome Android only):**

In this PoC <https://cnfdnfial-ops.github.io/spoof/s0f.html>, SpeechSynthesis audio starts on an attacker page and the page quickly redirects to `https://google.com` using `window.location.replace()`.

On **Chrome Android only**:

- The previous page does **not appear in history** (expected).
- **Audio continues after redirect**, making it appear to come from the new domain.

"On Windows, it works, but the history of <https://cnfdnfial-ops.github.io/spoof/s0f.html>
still appears when clicking the back button."

### ec...@gmail.com (2026-03-04)

I’m sharing the PoC through the following URL: <https://cnfdnfial-ops.github.io/spoof/sp0f.html>.

In this PoC, I’m using `window.open('https://google.com', '_self');`, and the issue is present on both **Safari** and **Chrome on iOS**.

Given that this issue occurs on **Safari on iOS**, would you like to check first to see if a fix can be implemented on the **iOS** side before I report it to **WebKit** (specifically for iOS)

### ec...@gmail.com (2026-03-04)

if chromium team need information fell free to ask

### ec...@gmail.com (2026-03-05)

Using window.open('<https://google.com>', '\_blank')
in this PoC (<https://cnfdnfial-ops.github.io/spoof/test.html>) causes the speechSynthesis audio to keep playing, while the back button does not work on Chrome iOS and is disabled on Chrome Android.

### ec...@gmail.com (2026-03-06)

any update about this ?

### me...@google.com (2026-03-07)

evliu@, could you PTAL and reassign as appropriate? Thanks.

### ch...@google.com (2026-03-07)

Setting milestone because of s2 severity.

### ec...@gmail.com (2026-03-13)

Hi Chromium Team,

I’m sharing a Proof of Concept (PoC) demonstrating how `speechSynthesis` combined with page redirects behaves differently on **Chrome Windows** and **Chrome Android**.

**Link:** <https://cnfdnfial-ops.github.io/spoof/s0f.html>

**Observed Behavior:**

- On **Chrome Android**: the back button does **not return** to the previous page (“real POV”).
- On **Chrome Windows**: back button seems to clear history, and Google’s voice search icon sometimes overlaps or “sticks” during redirect.

**Expected Behavior:**

- Back button should navigate to the previous page.
- Page elements (like Google voice search) should not be affected by rapid redirects.

**Steps to Reproduce:**

1. Open the PoC link in Chrome Windows or Android.
2. Click the **“CLICK CALL CENTER GOOGLE”** button.
3. Observe speech synthesis and automatic redirect.
4. Attempt to use the back button.

**Additional Notes:**

- The issue is caused by using `window.location.replace()` and redirecting immediately after `speechSynthesis.speak()`.
- Switching to `window.location.href` and waiting for `utter.onend` fixes back button and UI issues.

### ec...@gmail.com (2026-03-13)

on chrome ios <https://cnfdnfial-ops.github.io/spoof/test.html>

using window.open('<https://google.com>
', '\_blank');
so when button start button left and right disable and sound apperan on google.com

### ec...@gmail.com (2026-03-18)

On POC bellow I also using web share api + SpeechSynthesis audio (combination)

<https://cnfdnfial-ops.github.io/spoof/s0f.html>

**Attack Scenario:**

The victim taps a button on a webpage, which triggers two APIs:

1. **SpeechSynthesis API**: The text-to-speech functionality starts playing on Google.com.
2. **Web Share API**: The share dialog opens on Google.com, containing attacker-controlled content in the shared text.

This could potentially deceive or trick the user into thinking they are interacting with legitimate content on Google.com, while they are actually being manipulated by the attacker.

---

Let me know if you'd like further adjustments or more details added!

### ch...@google.com (2026-03-22)

evliu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ev...@google.com (2026-03-24)

katydek@ - Do you still work on TTS?

### ec...@gmail.com (2026-03-26)

Poc bellow In iOS , no back button history, victim think the voice from Google.com

### ec...@gmail.com (2026-03-26)

Any update?

### ka...@google.com (2026-03-26)

Hi Evan, I'm not working on TTS, sorry!

### ec...@gmail.com (2026-03-26)

So it's not valid? Or are there any considerations?

### ec...@gmail.com (2026-03-26)

<https://issues.chromium.org/issues/40124701> is that issue show the Audio playing on legit domain? I also produce on desktop what showing icon voice playing on google.com

### ev...@google.com (2026-03-27)

On second examination, it looks like b/40124701 was already fixed by https://chromium-review.git.corp.google.com/c/chromium/src/+/2261098. The issue described in this bug is still valid.

### ec...@gmail.com (2026-03-27)

Thanks for update Evan

### ec...@gmail.com (2026-03-27)

I also report on Firefox, and they taking fix progress

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  Evan Liu [evliu@google.com](mailto:evliu@google.com)  

Link:    <https://chromium-review.googlesource.com/7705458>

Fix Web Speech API audio persisting across page navigations

---


Expand for full commit details
```
     
    Currently, speechSynthesis audio can continue playing after a page 
    unloads or redirects to another origin. This CL fixes the issue by 
    canceling the active TtsUtterance in the browser process when the 
    WebContents' primary page changes. 
     
    Fixed: 489624550 
    Change-Id: I385ffc9856c572576a27e3b95be807b66bc3f8a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705458 
    Reviewed-by: Katie D <katie@chromium.org> 
    Commit-Queue: Evan Liu <evliu@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1608024}

```

---

Files:

- M `content/browser/speech/tts_controller_impl.cc`
- M `content/browser/speech/tts_controller_impl.h`
- M `content/browser/speech/tts_controller_unittest.cc`

---

Hash: [0793f4fdce65f5900c343dea6b2f4f33c3ef4b5d](https://chromiumdash.appspot.com/commit/0793f4fdce65f5900c343dea6b2f4f33c3ef4b5d)  

Date: Tue Mar 31 19:39:40 2026


---

### ec...@gmail.com (2026-03-31)

deleted

### ec...@gmail.com (2026-04-01)

deleted

### ec...@gmail.com (2026-04-01)

deleted

### ec...@gmail.com (2026-04-02)

**Additional Clarification: Cross-Platform / Cross-OS Impact**

I would like to further emphasize that this issue is not limited to a single platform, but is reproducible across multiple operating systems and browser environments.

Based on my testing, the behavior is consistently observed on:

- Desktop (Windows)
- Android (Chrome Stable & Canary)
- iOS (Chrome & Safari/WebKit-based browsers)

This suggests that the issue is not an isolated implementation detail, but rather affects **multiple platform integrations of the Web Speech API and navigation handling**.

---

**Security-Relevant Observation Across OS:**

Across these platforms, the following behavior remains consistent:

- Audio initiated from an attacker-controlled origin continues playing after navigation
- The user is redirected to a trusted domain such as Google
- The **audio persists without clear origin indication**
- In some cases, **UI indicators (e.g., voice icon or disabled navigation controls)** remain visible or associated with the destination page

From the user’s perspective:

> The audio appears to originate from the trusted destination site, regardless of the actual source.

---

**Why Cross-OS Behavior Increases Severity:**

The cross-platform nature of this issue increases its impact because:

- It affects a **broad user base (desktop + mobile users)**
- It enables **consistent exploitation scenarios across devices**
- It reduces variability, making it more reliable for real-world abuse

In particular, on mobile platforms (Android/iOS):

- Navigation controls (e.g., back button) may be altered or unavailable
- Combined with persistent audio, this further reinforces the illusion that the content originates from the current (trusted) page

---

**Impact Perspective:**

When combined with previously described behavior:

- Cross-origin audio persistence
- UI indicator / browser signal appearing on a trusted domain
- Cross-platform reproducibility

This issue may represent a broader **origin confusion and trust-boundary violation**, rather than a platform-specific UX inconsistency.

---

**Closing Note:**

Given the consistency across operating systems and the potential for user confusion on high-trust domains, I would appreciate a comprehensive evaluation of the security impact in a cross-platform context.

### ec...@gmail.com (2026-04-04)

Any update for vrp?

### ec...@gmail.com (2026-04-05)

Was fix on chrome canary Android new version

### ec...@gmail.com (2026-04-06)

Any update please

### ec...@gmail.com (2026-04-06)

Any update vrp result?

### ec...@gmail.com (2026-04-08)

Any update vrp ? Please

### ec...@gmail.com (2026-04-09)

Please any update?

### ec...@gmail.com (2026-04-12)

Any updated for vrp result

### ec...@gmail.com (2026-04-12)

(Chrome & Chromium Browsers) File Download Pop-up Origin Spoof

https://issues.chromium.org/issues/40055527

This issue appears to share a similar root cause with the previously reported download and redirect origin confusion. However, in my case, the behavior affects a different UI component — the voice icon.

After redirection to a legitimate domain, the browser displays the voice icon as if the audio originates from that domain. In reality, the audio is controlled and delivered by an attacker. This creates a misleading trust signal, as users may assume the sound is coming from a trusted source.



### ec...@gmail.com (2026-04-12)

Any update?

### ec...@gmail.com (2026-04-13)

Any updateAny update?

### ec...@gmail.com (2026-04-15)

Ping 

### ec...@gmail.com (2026-04-15)

Ping 

### ec...@gmail.com (2026-04-15)

Fixed on chrome canary Android also chrome dev android 

### ec...@gmail.com (2026-04-16)

any update ?

### ec...@gmail.com (2026-04-20)

Any updated for vrp ?

### ec...@gmail.com (2026-04-21)

Hi team, any updates regarding the VRP decision?

### ec...@gmail.com (2026-04-24)

In Chrome android I just realized that the voice icon is stuck on the legit domain after the redirect.

Chrome android Chrome 147.0.7727.102

### ec...@gmail.com (2026-04-27)

Helo team any update? 

### ec...@gmail.com (2026-04-29)

Pinggg

### ec...@gmail.com (2026-04-30)

Any update please ?

### ec...@gmail.com (2026-05-01)

Any update for vrp?

### ec...@gmail.com (2026-05-01)

Hi team, just following up regarding the VRP review status for this report. Since the fix has shipped, I wanted to kindly ask if there are any updates on the reward decision. Thank you.


### ec...@gmail.com (2026-05-04)

Hi team, just following up regarding the VRP review status for this report. Since the fix has shipped, I wanted to kindly ask if there are any updates on the reward decision. Thank you.


### ec...@gmail.com (2026-05-04)

Hi team, just following up regarding the VRP review status for this report. Since the fix has shipped, I wanted to kindly ask if there are any updates on the reward decision. Thank you.

### ec...@gmail.com (2026-05-06)

Hi team, just following up regarding the VRP review status for this report. Since the fix has shipped, I wanted to kindly ask if there are any updates on the reward decision. Thank you.

### ec...@gmail.com (2026-05-08)

Thanks for cve team 

### ec...@gmail.com (2026-05-08)

Hi team, just following up regarding the VRP review status for this report. Since the fix has shipped, I wanted to kindly ask if there are any updates on the reward decision. Thank you.


### ec...@gmail.com (2026-05-11)

Hi team, just following up regarding the VRP review status for this report. Since the fix has shipped, I wanted to kindly ask if there are any updates on the reward decision. Thank you.

### ec...@gmail.com (2026-05-17)

Hi team , please any update for vrp ?

### ec...@gmail.com (2026-06-15)

Any update on this 

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Security UI Spoofing.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489624550)*
