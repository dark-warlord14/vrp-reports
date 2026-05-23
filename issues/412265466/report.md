# Android: Spoof the entire tab navigation delayed/confused omnibox rendering behavior

| Field | Value |
|-------|-------|
| **Issue ID** | [412265466](https://issues.chromium.org/issues/412265466) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | fa...@gmail.com |
| **Assignee** | sk...@google.com |
| **Created** | 2025-04-21 |
| **Bounty** | Confirmed (amount unknown) |

## Description

## Vulnerability Details

While testing Chromium on Android, I discovered a vulnerability involving navigation that allows complete confusion of the rendering flow and the omnibox (address bar). This can lead to address bar spoofing.

By quickly entering fullscreen and then immediately exiting from a site, the browser's method of displaying the omnibox origin becomes completely broken. As a result, the origin shown in the address bar remains that of the previous site, even though the content is changed.

I reproduced this behavior using permission.site and also created a working proof of concept that demonstrates how a malicious site can exploit this.

## Attack Scenario

1. A user visits a malicious site from a Google Search results and interacts with the site.
2. The attacker’s site automatically enters fullscreen and then triggers `history.back()` or simulates back navigation.
3. The browser incorrectly displays the previous origin, and every subsequent navigation on the tab is affected, incorrectly showing the previous origin's rendering instead of the current one, thereby spoofing the entire navigation flow.

---

## Steps to Reproduce Manually

1. Visit `google.com` using Chrome on Android.
2. Search for and click on `permission.site`.
3. Once on `permission.site`, enter fullscreen mode and quickly back out using the browser's back functionality (e.g., swipe back or call `history.back()`).
4. Observe that browser incorrectly displays the previous origin.
5. Now visit other links; the Omnibox will still display the previous domain (`google.com`), even though different pages are being loaded.

Video demo: `manual-demo.mp4`

## Steps to Reproduce PoC

1. Host the provided `poc.html` file using a local Python server:
   ```
   python3 -m http.server 8000
   
   ```
2. Visit google seach on Chrome Android.
3. Navigate to your hosted page (e.g., `http://<your-ip>:8000/poc.html`).
4. Click on the PoC button, which triggers fullscreen mode and then calls `history.back()`.
5. Now visit other links; the Omnibox will still display the previous domain (`google.com`), even though different pages are being loaded.

Video demo: `poc-demo.mp4`

---

## Affected Version

- Chrome Version: 135.0.7049.100
- Operating System: Android 14

---

## Credit

**Reporter**: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/html, 343 B)
- manual-demo.mp4 (video/mp4, 6.5 MB)
- poc-demo.mp4 (video/mp4, 5.1 MB)
- Screen_Recording_20250429_205231_Chrome Beta.mp4 (video/mp4, 41.8 MB)
- android-202533-161536.pftrace (application/octet-stream, 1.3 KB)
- trace.json (application/json, 6.3 KB)
- trace.json (application/json, 17.0 KB)
- android-202544-145321.pftrace (application/octet-stream, 4.7 KB)

## Timeline

### an...@chromium.org (2025-04-21)

[security shepherd]: Thanks for the report. Assigning this to @cr...@chromium.org who is the owner of URL spoofing in general. From the demo and POC, it looks like the omnibox URL doesn't match what the user sees on the page. I haven't been able to reproduce this on my end but the demo looks reasonable.

### cr...@chromium.org (2025-04-21)

Thanks for the report! I agree that this looks concerning from the video, but I haven't been able to repro it on the same version of Chrome for Android using either the manual steps or the JavaScript code in the PoC. Is it timing dependent, or have you found anything that makes it happen more reliably?

Adding Fullscreen and Navigation components just in case. I'm not sure what would cause the wrong URLs to be displayed as you continue to navigate after full screen exits.

### ch...@google.com (2025-04-22)

Setting milestone because of s2 severity.

### ch...@google.com (2025-04-22)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fa...@gmail.com (2025-04-22)

I have tested this on a Samsung device. When testing, could you also try testing the browser in floating mode and split-screen mode? Maybe this triggers the issue more common in devices.

### pe...@google.com (2025-04-22)

Thank you for providing more feedback. Adding the requester to the CC list.

### cr...@chromium.org (2025-04-23)

Sorry, I'm not having any luck repro'ing this. I'm also not sure what sort of code would be causing this bug, since the video shows a back navigation going to the correct URL but the omnibox displaying the previous page's URL (e.g., at 0:13 in manual-demo.mp4, Chrome goes back from MDN to Google Search, and shows MDN's URL above the search results). The NavigationEntry used in session history should be used for both the back navigation and what to display in the address bar, so I'm not sure how the address bar is getting out of sync while still navigating to the right place.

ender@: Can you take a look from an omnibox perspective, or do you know who's familiar with the fullscreen code involved? I'm curious if the omnibox is somehow caching a separate URL to display related to fullscreen, and maybe that's incorrectly being used after fullscreen exits here? (And are you able to repro the bug?)

I'm happy to answer questions about the session history side or even take another look if we can find how to repro it. Thanks!

### en...@google.com (2025-04-23)

unable to confirm // no repro with stable and canary. navigation works fine, and this bug doesn't seem directly related to the omnibox.

i wonder if there's any experiment that could be causing this; glancing through our ongoing studies i figure this might hypothetically be the case?

Lijin, can you confirm if this bug is possible with BackForward transition?

@Reporter - could you please collect the contents of the chrome://version and paste it here please?

thank you!

### la...@google.com (2025-04-23)

Unable to repro on canary 135.0.7049.100 with BackForward transition enabled.

Hi reporter, could you visit chrome://version and then share "Active Variations"?

### fa...@gmail.com (2025-04-23)

```
Chrome logo
Google LLC
Copyright 2025 Google LLC. All rights reserved.
Google Chrome	135.0.7049.100 (Official Build) (64-bit) 
Revision	88b2948b73f052ac9ac7d9b027abbecc788505aa-refs/branch-heads/7049@{#1841}
OS	Android 14; SM-S921B Build/UP1A.231005.007; 34; REL
APK versionCode	704910033
APK targetSdkVersion	35
isAtLeastU/targetsAtLeastU	true/true
Google Play services	SDK=251030000; Installed=251462029; Access=1p
JavaScript	V8 13.5.212.10
User agent	Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36
Command Line	--use-mobile-user-agent --use-mobile-user-agent --enable-viewport --validate-input-event-stream --enable-longpress-drag-selection --touch-selection-strategy=direction --disable-composited-antialiasing --enable-dom-distiller --flag-switches-begin --enable-features=IncognitoScreenshot --flag-switches-end --top-controls-show-threshold=0.5 --top-controls-hide-threshold=0.5 --top-controls-show-threshold=0.5 --top-controls-hide-threshold=0.5
Executable Path	No such file or directory
Profile Path	/data/user/0/com.android.chrome/app_chrome/Default
Command-line variations	eyJkaXNhYmxlLWZlYXR1cmVzIjoiQXV0b2ZpbGxQYXJzZUVtYWlsTGFiZWxB...	
Active variations	2b978349-ca7d8d80
1073a35d-377be55a
e1814b25-33c3eba5
fd9e245f-377be55a
87ef25e4-377be55a
7103530a-33c3eba5
181d9f0c-377be55a
89986dbe-ca7d8d80
d992c558-ca7d8d80
cae5a6b5-377be55a
f69863c5-8d55def
7651c438-ca7d8d80
d0d3d7ff-3f4a17df
f73edf58-ca7d8d80
bc06eaa3-1f8c5973
147c5d66-1f8c5973
48a8d64c-ca7d8d80
d8c497dc-377be55a
73b87075-377be55a
dc88470b-377be55a
54c87162-ca7d8d80
6b7d4090-ca7d8d80
2dbe7f3c-377be55a
95988a12-ca7d8d80
bd14a89-ca7d8d80
1eb32835-ca7d8d80
3095aa95-3f4a17df
e6c167d9-377be55a
4664617a-54fa415c
3843461e-377be55a
67282630-652dfd7a
7faa7be9-ca7d8d80
4505a270-989f556b
ce4a99f0-ca7d8d80
71bfd247-377be55a
41e765a5-ecf76f10
f314f5b9-6e22746a
7840af09-602e4a00
85754f87-e9bfc439
6e3d443c-10db844
6cd7aa52-ca7d8d80
691d4256-ca7d8d80
5e4b4ebb-eea4e1e8
b617cdf5-437694
a582a1b8-5ad3f43d
d7ce3099-ca7d8d80
bd6dd170-ca7d8d80
780df7d2-ca7d8d80
beae798-ca7d8d80
55920447-ca7d8d80
a05c89eb-ca7d8d80
fe949b23-377be55a
87684b46-ca7d8d80
cba789d9-ca7d8d80
d603785e-377be55a
a61cb6b8-ca7d8d80
8f321ce-377be55a
4df7655b-ca7d8d80
3c978b59-ca7d8d80
9cf6c713-34edeffa
5a24997e-377be55a
95ed2bbe-984c5c31
ac900222-ca7d8d80
f42905ff-12ede6a2
71c14987-f66697fa
9a8040c8-9d446b22
b0a7d2e0-3fa75b73
5da1d434-9d446b22
c863bbb5-b651d52a
3f720261-9d446b22
c081ffb5-9d446b22
ad9b71e2-cb420954
b36d892f-377be55a
5e3a236d-4113a79e
53efe597-b20da897
d43ddfd9-e36235cc
13080a68-37b6594d
17196951-377be55a
f7b9a9e3-ca7d8d80
4b82c9ff-ca7d8d80
c88fa1e2-ca7d8d80
fba0616d-377be55a
a8a12e4d-ca7d8d80
136ff6f9-377be55a
4076100b-6edc92c7
62e82091-4113a79e
f381b82f-ca7d8d80
97df86a8-a798c3cb
59a12fbe-c486d7d0
5bca9eee-8bdaba2b
7c0e4650-ca7d8d80
2be5fc80-ca7d8d80
66b7a83f-ca7d8d80
f3f1bfdb-377be55a
d721a76b-ca7d8d80
4ea303a6-5dddeea3
33d08a4f-28ad44a
f3b6291d-6bb2bb3c
3212781a-ca7d8d80
393339bd-28ad44a
1edcddf4-f726f89c
cae19fc9-ca7d8d80
79d7856f-377be55a
b6f29041-ca7d8d80
2bac9a6a-33c3eba5
e85106e5-ca7d8d80
c046d00b-ca7d8d80
3c68162d-377be55a
3ced0aa9-ca7d8d80
8e8365ea-ca7d8d80
6ef0294d-396a57df
52a20523-ca7d8d80
d0083347-ca7d8d80
f9675edd-377be55a
39cad3e5-ca7d8d80
f98f9dbf-377be55a
30bcdd88-ca7d8d80
54c1f277-42091cf6
494d8760-52325d43
3ac60855-486e2a9c
f48c01d3-dfb6e87
63dcb6a3-75dc9252
e706e746-b7d97d3d
f296190c-30f715f3
4442aae2-7158671e
f690cf64-4ad60575
ed1d377-e1cc0f14
75f0f0a0-e1cc0f14
710c3f90-6bdfffe7
e2b18481-4c073154
e7e71889-4ad60575
3a8271ac-e9e131c
bc9a7ea9-ca7d8d80
4c3ef716-377be55a
bea4a9c2-44fcf049
92c76c82-21e61bf2
72ee2098-377be55a
d89640a1-8b140fb3
762e8080-277b1d15
49171648-3f4a17df
797cbb37-ca7d8d80
b357b792-c836f3a2
f4f00e05-ca7d8d80
9481ce98-3f4a17df
2a426c03-3d47f4f4
aca9df2c-3f4a17df
a3bc7210-3f66c0bc
b100ac4-dee66fa8
4651ad61-8533ea9a
59748665-8e9604d4
65250343-206f6a6e
553aead6-4a95a5b1
fe4babb8-4a95a5b1
6205871c-4866ef6e
382b54bb-29f03e2f
70678518-206f6a6e
be338734-4866ef6e
6f316e34-cc562941
5f9907a9-206f6a6e
8eeccb9a-c35b209e
2b465683-3601ad67
52fc7926-1790ff02
bc9b361d-dee66fa8
a41a7188-b184655b
ff71bfdc-dee66fa8
a6fa7475-dee66fa8
92cfa89f-dee66fa8
6daa4147-dee66fa8
4b935545-3d47f4f4
9a38bae3-6046c8a7
2d1e43a3-3d47f4f4
30e58f57-ca7d8d80
c4a500a4-3d47f4f4
386dc267-3d47f4f4
d69d967d-1166396
a4406b35-ccf52fb6
408da146-1657e2d6
5168dcfa-9c6e7a3e
f6918184-75e97c92
d4e26075-e28f41e0
dc20670d-3f4a17df

```

### cr...@chromium.org (2025-04-23)

Thanks! Also, since we haven't been able to repro it, maybe you would be willing to collect a trace of the repro to let us see what Chrome is doing when it happens?

There's instructions at <https://perfetto.dev/docs/quickstart/android-tracing#recording-a-trace-through-the-perfetto-ui>. It's worth enabling the Chrome probes for "Navigation and loading," "IPC Flows," and "omnibox" (and you might want to make the buffer duration longer than 10 seconds if needed). This will capture everything Chrome is doing, so it makes sense to do it in a browser that is only running your repro, to avoid including activity from other pages, etc.

### aj...@google.com (2025-04-24)

-> lazzzis as security issues should have an owner.

### tw...@google.com (2025-04-24)

I think this got assigned to Lijin because of suspected possible interaction with back/forward transitions which per #10 doesn't seem to be the case (also not sure why it'd affect exiting fullscreen + omnibox).

Back to ender@ for tracking on the omnibox side. It seems the omnibox is displayed properly and fully visible but it's no longer updating to reflect the current URL.

There is code to reshow browser controls when fullscreen is exited and if that were the issue, I'd have someone in my team look into this (clhager@ or jinsukkim@)... but since the browser controls are reshowing as expected, I suspect the issue is elsewhere.

### en...@google.com (2025-04-24)

thanks Theresa - yes, sent this to Lijin to confirm no relation to BackForward study.

The Omnibox shouldn't be rendering here at all (IIUC we should see a toolbar capture there).
I'll comb through the feature hashes to see if there's a possible suspect when I get a minute.

### tw...@google.com (2025-04-24)

Why wouldn't the Java omnibox be rendering? This is across page navigations and the browser controls aren't moving if I understand the report and demo video correctly, so I'd expect the Java controls to be showing.

### en...@google.com (2025-04-24)

I will look nonetheless. I don't know the specific conditions where the toolbar capture kicks in, but I can confirm that we haven't changed anything related to how or when the omnibox updates in a long time.
i'm not entirely sure what goes on there.

### en...@google.com (2025-04-28)

I looked at the enabled experiments ([full list](http://gpaste/4824153045336064) and [distilled list](http://gpaste/5989618769723392)) but nothing seems relevant in this area.

Looping in Toolbar Capture folks to help determine possibility of TBC involvement, but I am at loss here. I can't repro this with the attached files, even after tweaking timeouts.

I'll spend a bit more time trying to repro this with any of my other devices, in case it needs either fast or slow device. Maybe our test team can help here, too.

At this time this bug appears to be non-reproducible; I speculate that the 100ms time, or the fact this reproduces at all, might be related to the device used to construct the original POC.

### sk...@google.com (2025-04-28)

I wonder if the fullscreen+back could be causing us to keep around a stuck navigation from the logic added in <https://chromium-review.googlesource.com/c/chromium/src/+/6040200/11/chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java#145>

It does look like we have a long tail of situations where we don't clear navigations <https://uma.googleplex.com/p/chrome/timeline_v2?sid=04358c9dd49f4ddbc852f455b05fdc53> . It'd be interesting to get the values being emitted to Android.BrowserControls.OutstandingNavigationsOnFinish from navigations after this issue repros.

### tw...@google.com (2025-04-28)

Re #19,

Hi reporter,

Could you please visit chrome://histograms before and after reproducing the issue and share a screenshot of what's captured in Android.BrowserControls.OutstandingNavigationsOnFinish before vs after repro?

### fa...@gmail.com (2025-04-29)

Hi, here is a screen recording of it. I'm not sure if I should refresh or not, so I made this recording to show both scenarios.

I'll also try setting up Perfetto tomorrow and attempt to get the repro traces as well.

### fa...@gmail.com (2025-04-30)

Hi, will Perfetto UI capture Chrome Beta traces as well? Also, regarding visiting permission sites from Google and fullscreening, then going back to Google—that's the repro, for this using a buffer duration of 30 seconds should be sufficient, right? I have also enabled "Navigation and loading," "IPC Flows," and "Omnibox" for Chrome browser tracing.

### en...@google.com (2025-04-30)

Tentatively assigning to Sky, who has done some work in directly adjacent territory. We might have to get the manual test team involved.

### yf...@chromium.org (2025-05-07)

Hmm, the trace file isn't complete, there's no data collected. Perhaps the probes weren't turned on or alternatively you need to ensure to enable tracing and then repro the broken case.

Video suggests it's at least not the bug with the histogram being non-zero :/

### fa...@gmail.com (2025-05-22)

Okay, this time I enabled tracing on my Android device as well.

### ch...@google.com (2025-05-27)

skym: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sk...@google.com (2025-06-05)

Sorry it's taking me so long to investigate this. Still on my radar.

### ch...@google.com (2025-08-05)

skym: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-20)

skym: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-04)

skym: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-19)

skym: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-14)

skym: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-25)

skym: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-10)

skym: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-25)

skym: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-09)

skym: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-01-20)

I can't reproduce the bug on 146, but the reporter was using 135. Reporter could you please try to see if you can reproduce it on a newer version of chrome? Also could you reproduce this consistently on your device, if yes, then we can find a culprit by bisecting.

@lb...@google.com Sky mentioned you were asking about this, just wondering if we can close this bug if we cant reproduce it.

### fa...@gmail.com (2026-01-21)

Tested this on the latest version of Chrome on Android, and the issue is no longer reproducing for me.

### pe...@google.com (2026-01-21)

Thanks for the update! I'm gonna close it for now, but if it happens again please reopen (we fixed a few bugs in the past months, we might have fixed this bug too without realizing it.)

### fa...@gmail.com (2026-01-21)

Hi, checking whether this bug is fixed with other code. Does this mean it’s eligible for rewards? Thanks.

### pe...@google.com (2026-01-21)

Ah I don't know anything about that, I think someone from security would know.

### aj...@chromium.org (2026-01-22)

Marking as Fixed with no known Fix following comment 39.

### sp...@google.com (2026-02-19)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Not reproducible

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-04-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Not reproducible
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/412265466)*
