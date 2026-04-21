# Tapjacking on Custom Tabs using animations

| Field | Value |
|-------|-------|
| **Issue ID** | [376491759](https://issues.chromium.org/issues/376491759) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | Android |
| **Reporter** | ph...@gmail.com |
| **Assignee** | si...@google.com |
| **Created** | 2024-10-31 |
| **Bounty** | $10,000.00 |

## Description

# VULNERABILITY DETAILS

## Short Summary

An application without any permissions can exploit animations and launch a Chrome Custom Tab (CCT) to bypass permission checks on websites and perform clickjacking attacks against arbitrary websites.

## Primitives

Android applications can use Chrome Custom Tabs (CCT) to open web content with minimal context switching, as Custom Tab Activities are launched within the same Task as the requesting application. Through the `ActivityOptions.makeCustomAnimation` method, Android also allows applications to specify custom enter and exit animations for cross-activity and same-task transitions, such as the transition between an app and a CCT.

An application installed on the user's device can exploit this functionality by launching a Custom Tab and setting an enter animation with a long fade-in duration, set to low opacity. This transition brings the Custom Tab to the foreground yet keeps it invisible to the user while the animation completes since the CCT is basically transparent (e.g., opacity=0.0005). As the CCT Activity is on top of the stack, and Chrome does not wait for animations to be finished before handling touches, screen interactions are handled by the browser.

The following minimum working example demonstrates this exploit, assuming Chrome is the default browser:

**MainActivity.kt**

```
val builder = CustomTabsIntent.Builder()
// setStartAnimation internally uses ActivityOptions#makeCustomAnimation
builder.setStartAnimations(this, R.anim.fade_in, R.anim.fade_out) 
val customTabsIntent = builder.build()
customTabsIntent.launchUrl(this, victimUrl)

```

**res/anim/fade\_in.xml**

```
<?xml version="1.0" encoding="utf-8"?>
<!-- Long-running animation with low opacity -->
<alpha xmlns:android="http://schemas.android.com/apk/res/android"
    android:fromAlpha="0.0"
    android:toAlpha="0.0005"
    android:duration="20000"/>

```

**res/anim/fade\_out.xml**

```
<?xml version="1.0" encoding="utf-8"?>
<!-- This boils down to no animation, as duration = 0 -->
<alpha xmlns:android="http://schemas.android.com/apk/res/android"
    android:fromAlpha="1.0"
    android:toAlpha="1.0"
    android:duration="0" />

```

Chrome is not vulnerable when opening a website via a non-CCT Intent, as the `FLAG_ACTIVITY_NEW_TASK` flag is set on the Intent when launched (see relevant [Chromium source code](https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/LaunchIntentDispatcher.java;drc=7804fc4cc9837d70a6f52f7617612884cac261a5;bpv=1;bpt=1;l=497?gsn=setFlags&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Djava%3Fpath%3Dandroid.content.Intent%23dad7272f323513f01d4f2511a91d49e1f9ea1cfd40fd26ca2b36d7b2181493bb)). This flag causes Chrome to start in a new task, which prevents the use of custom animations.

This report is part of a coordinated responsible disclosure on the underlying animation-based tapjacking vulnerability we discovered on Android.

## Security Implications

The vulnerability opens doors for the following Chrome/Web-specific issues:

1. Permission Bypass

By launching a CCT with this technique, an application can open an attacker-controlled website that requests sensitive permissions, such as microphone or camera access. By luring the user to tap a button that is positioned at the same location as the allow button in the permission prompt, the permission is granted to the website without user awareness. Since CCT permissions are shared with Chrome, any permissions granted in this way go beyond the CCT, granting persistence to the attacker in the victim's browser. This vulnerability also allows attackers to install PWAs on the user's device.

2. Web Clickjacking Attacks

An app can secretly request a website, i.e., a checkout page of an online store, and lure the user into performing critical actions, such as clicking the 'buy' button. Existing standard web-based clickjacking prevention, such as the Content Security Policy `frame-ancestors` directive and the `X-Frame-Options` headers, do not apply here and do not mitigate these attacks. Note also that SameSite Lax cookies are attached to CCT-initiated navigations.

The implications of this clickjacking attack differ significantly from clickjacking in Android WebViews. Unlike WebViews, which do not share state with the browser, Custom Tabs do. That means that sessions established by the user on any websites in Chrome are available in the CCT.

## Existing and Proposed Mitigations

Existing efforts made by Chrome to mitigate tapjacking vulnerabilities on Android, such as using `View.setFilterTouchesWhenObscured` and checks for the `FLAG_WINDOW_IS_PARTIALLY_OBSCURED` flag in modals ([see relevant source code here](https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogView.java?q=symbol%3A%5Cborg.chromium.components.browser_ui.modaldialog.ModalDialogView.setupFilterTouchForView%5Cb%20case%3Ayes)) only mitigate attacks from malicious overlays on top of Chrome activities, not animations. Similarly, [system level-protections built into Android 12+](https://developer.android.com/privacy-and-security/risks/tapjacking) only target overlays.

The source of this vulnerability is twofold: (1) Chrome does not wait for animations to be finished until it handles touches, and (2) Android allows long-running animations with low opacity.

To offer mitigations to protect users until (2) is fixed on the system level, we propose to also fix (1) and mitigate this issue at the browser level. Chrome can ignore all touch events until the `onEnterAnimationComplete` lifecycle method is called. This method is triggered once the enter animations are complete, thereby protecting against animation-based tapjacking.

## Practicality of the Attack

A slow fade-in transition would reveal the Chrome window after a few seconds, but an app can re-launch its own activity before the animation ends to effectively hide the Custom Tab. According to our experiments, a delay of 2500ms between starting the CCT and re-launching the app's activity is effective. This means that the permission prompt is clickable for 2.5 seconds. Although this is a relatively short time frame for user interaction, attack scenarios like games, where users are prompted to tap quickly, make this attack practical. An app can further optimize load times by pre-warming the browser with the `warmup` method and pre-fetching the target page using `mayLaunchUrl`.

# VERSION

Chrome Version: 130.0.6723.73 stable
Operating System: Android 15, Pixel 6a

# REPRODUCTION CASE

The Proof of Concept application and the attached video demonstrate bypassing the Chrome permission prompt via tapjacking (source code can be found [here](https://gitfront.io/r/philippbeer/PZo34NhDiR1c/tapjacking-browser-poc/)).
Notice that the button positioning is manually adjusted for a Pixel 6a and might require some tweaking to generalize to different devices.
The application opens <https://webrtc.github.io/test-pages/src/iframe-video/>, which immediately requests camera permission on load.

To replicate the permission tapjacking, follow these steps:

- Grant Chrome permission to access the user's camera
- Install the PoC application (source code and APK available here)
- Click 'Choose browser' and choose Chrome
- Click 'open com.android.chrome'
- Click on the red button when it appears
- The site is now allowed to access the camera

# CREDIT INFORMATION

Reporter credit: Philipp Beer, TU Wien (@beerphilipp)

## Attachments

- [poc_chrome.mp4](attachments/poc_chrome.mp4) (video/mp4, 16.4 MB)
- [tapjacking-browser-poc.apk](attachments/tapjacking-browser-poc.apk) (application/vnd.android.package-archive, 11.6 MB)

## Timeline

### ph...@gmail.com (2024-10-31)

If possible, please also add [squarcina@gmail.com](mailto:squarcina@gmail.com) to this report. Thanks!

### sr...@google.com (2024-10-31)

Thanks for the report!

mthiesse@, I personally think this is something that should be fixed on the Android side, but can you take a look if this is something we'd want to do: `Chrome can ignore all touch events until the onEnterAnimationComplete lifecycle method is called.`

### pe...@google.com (2024-10-31)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ph...@gmail.com (2024-10-31)

Hi, we have also responsibly disclosed this issue with the Android Security Team (<https://issuetracker.google.com/issues/376620895>) as well as the following affected browser vendors:

- Firefox (<https://bugzilla.mozilla.org/show_bug.cgi?id=1928334>)
- Brave (<https://hackerone.com/bugs?subject=user&report_id=2813717>)
- Edge (<https://msrc.microsoft.com/report/vulnerability/VULN-137894>)

Best,
Philipp

### mt...@chromium.org (2024-10-31)

I think we can certainly mitigate this in Chrome. Is there a way to make it so our Activity cannot be launched with a custom animation? If so that's they way I would go with this. We could have our theme specify a transition animation but I don't know how that interacts with custom launch animations, and we probably don't want to override platform default.

Otherwise, blocking touches at the root level while our Activity is animating, or when it's not opaque, sound like good ideas.

### ph...@gmail.com (2024-10-31)

The custom animation can be overriden by calling the ‘overridePendingTransition’ method in the activity’s ‘onCreate’ method. This would, however, completely disable the functionality of custom animations, which may not be a good idea from a UX point of view. Also, this API has been deprecated in API level 34.
Calling the replacement method, ‘overrideActivityTransition’, did not seem to cancel the entry animation when I tried it out. But having a closer look at it might still be worth it.

### mt...@chromium.org (2025-01-31)

Sorry, this fell off of my radar. Passing over to Theresa for triage.

### tw...@chromium.org (2025-01-31)

> This would, however, completely disable the functionality of custom animations, which may not be a good idea from a UX point of view.

+1 -- I think from a non-malicious app perspective, we also want Custom Tabs to be able to be opened with custom animations (although could run that by PMs)

The #onEnterAnimationComplete API sounds promising... we could possibly set up an event filter that just swallows all touches until this API is called.

-> Sinan (or could see if Jinsuk has cycles) to investigate whether this API works.

### si...@google.com (2025-02-06)

I did a quick prototype, and returning true early until #onEnterAnimationComplete is called seems to work.

We already have some code preventing taps from overlays [here](https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabActivity.java;drc=003b43cb850a2fb81bb482cd95381338b7205933;l=318). However, we probably don't want to inject the missed touches in this case.

### ap...@google.com (2025-02-11)

Project: chromium/src  

Branch: main  

Author: Sinan Sahin <[sinansahin@google.com](mailto:sinansahin@google.com)>  

Link:      <https://chromium-review.googlesource.com/6244912>

Block touches in CCT until enter animation is completed

---


Expand for full commit details
```
Block touches in CCT until enter animation is completed 
 
Bug: 376491759 
Change-Id: I989b1bcb3aee842a0080e01603c5717771368cab 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6244912 
Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org> 
Commit-Queue: Sinan Sahin <sinansahin@google.com> 
Cr-Commit-Position: refs/heads/main@{#1418416}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/customtabs/CustomTabActivity.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/customtabs/CustomTabsFilterTouchUnitTest.java`
- M `chrome/browser/flags/android/chrome_feature_list.cc`
- M `chrome/browser/flags/android/chrome_feature_list.h`
- M `chrome/browser/flags/android/java/src/org/chromium/chrome/browser/flags/ChromeFeatureList.java`

---

Hash: a9a7be5f5c0a41b054d18e1e95c26ba1ab15f0b4  

Date:  Mon Feb 10 17:34:45 2025


---

### ph...@gmail.com (2025-02-11)

Dear Chrome Security Team,

I’d like to provide an update from our side. We are in the process of publishing our findings and evaluation of the Android Tapjacking vulnerability at the [USENIX Security Symposium 2025](https://www.usenix.org/conference/usenixsecurity25). While the paper does not focus directly on Chrome, it discusses the broader impact of this vulnerability on the Web ecosystem as well, including Chrome.

The paper is currently under review. If accepted, it will be published in June 2025 and presented at the conference in August 2025.

Best,
Philipp Beer

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality report of local privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Congratulations Philipp Beer! Very nice finding on this interesting variation on tapjacking in CCT and thank you for the comprehensive report. This was definitely one of the more impactful types of tapjacking bugs we've seen. Thanks for reporting this issue to us and updating us with your intent discuss these types of issues at USENIX Security in August. Best of luck on your paper and talk!

### ph...@google.com (2025-02-20)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### si...@google.com (2025-02-20)

Severity has already been set by Amy.

### ch...@google.com (2025-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality report of local privilege escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/376491759)*
