# Spoof on virtual keyboard

| Field | Value |
|-------|-------|
| **Issue ID** | [446463993](https://issues.chromium.org/issues/446463993) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | pn...@chromium.org |
| **Created** | 2025-09-21 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS

when the virtual keyboard is displayed and at the same time the navigation is directed to the previous page (history.go(-1)) the virtual keyboard still appears and the color of the minibar above the virtual keyboard becomes dynamic (the color follows the --theme-color of the background color so that the writing in the minibar is the same so that the domain is not visible in this bug I use white color) , leading to a spoof.

OS: Android 15
Device: Samsung A56
Chrome Version:  142.0.7396.0 Canary

Steps to reproduce:
1. download detx.html,spoofkeyboard.html in same folder / host detx.html,spoofkeyboard.html on local web server using https:// protocol
2. open https://you-can-billowy-nimble-login-secure-docs-google-source-attacker.com/detx.html or open detx.html on local web server using https: protocol
3. click the button
4. clik the go to google button


## Attachments

- spoofkeyboard.mp4 (video/mp4, 1.8 MB)
- [detx.html](attachments/detx.html) (text/html, 3.8 KB)
- [spoofkeyboard.html](attachments/spoofkeyboard.html) (text/html, 701 B)
- IMG-20250923-WA0000.jpg (image/jpeg, 61.8 KB)
- VID-20250923-WA0001.mp4 (video/mp4, 1.9 MB)
- [detx1.html](attachments/detx1.html) (text/html, 3.8 KB)
- [spoofkeyboard1.html](attachments/spoofkeyboard1.html) (text/html, 705 B)
- beta.mp4 (video/mp4, 1.8 MB)
- stable.mp4 (video/mp4, 1.8 MB)
- bgcolorwhite.mp4 (video/mp4, 2.0 MB)
- [VID-20250925-WA0003.mp4](attachments/VID-20250925-WA0003.mp4) (video/mp4, 2.0 MB)
- [IMG-20250925-WA0002.jpg](attachments/IMG-20250925-WA0002.jpg) (image/jpeg, 35.1 KB)

## Timeline

### sa...@gmail.com (2025-09-22)

the vulnerability is similar (not identical) as https://issues.chromium.org/issues/439262604 (on IOS) but this bug affected on android

### ct...@chromium.org (2025-09-22)

Thanks for the report. When this is showing it is moderately convincing IMO, as there is just what appears to be a (small) visual glitch on the virtual keyboard.

Setting some security labels:

- S2 Sev-Medium (control over apparent origin in Omnibox, but somewhat mitigated because it is only in effect while the virtual keyboard is displayed)
- FoundIn-142

Reporter: Have you also been able to repro on Stable or Beta channels?

Over to pnoland@ for Android (mini) Omnibox.

### pn...@chromium.org (2025-09-22)

Not reproing on Pixel, will try samsung.

### pn...@chromium.org (2025-09-22)

Hmm, I think the core issue here and in 446539525 is that the toolbar is effectively disappearing when it shouldn't. That's going to give you the ability to spoof, but I can't yet reproduce this behavior (or the persistence of the virtual keyboard) on the given test page. I might need Android 15 + Samsung, which I haven't tested with yet.

### pn...@chromium.org (2025-09-22)

Still can't repro. Reporter, can you post the contents of chrome://version ? I'm specifically interested in "Active Variations"

### sa...@gmail.com (2025-09-22)

Tbis is the version

### pn...@chromium.org (2025-09-22)

I need the entire contents of the page; that doesn't show me "Active Variations"

### sa...@gmail.com (2025-09-22)

Google Chrome	142.0.7428.0 (Official Build) canary (64-bit) 
Revision	4f3bb66031474e02b3e168f56612e509dd02a73c-refs/branch-heads/7428@{#1}
OS	Android 15; SM-A566B Build/AP3A.240905.015.A2; 35; REL
APK versionCode	742800033
APK targetSdkVersion	36
Google Play services	SDK=253910000; Installed=253534035; Access=1p
JavaScript	V8 14.2.180
User Agent	Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36
Command Line	--use-mobile-user-agent --background-thread-pool-field-trial=1 --use-mobile-user-agent --enable-viewport --validate-input-event-stream --enable-longpress-drag-selection --touch-selection-strategy=direction --disable-composited-antialiasing --enable-dom-distiller --flag-switches-begin --flag-switches-end --top-controls-show-threshold=0.5 --top-controls-hide-threshold=0.5 --background-thread-pool-field-trial=1 --background-thread-pool-field-trial=1 --background-thread-pool-field-trial=1 --background-thread-pool-field-trial=1
Executable Path	No such file or directory
Profile Path	/data/user/0/com.chrome.canary/app_chrome/Default
Command-line Variations	eyJkaXNhYmxlLWZlYXR1cmVzIjoiQWJsYXRlU2VhcmNoUHJvdmlkZXJXYXJt...	
Active Variations	6f27bc8a-94da29d
a66dbd64-ca7d8d80
2e98983f-5d219690
b7f7d766-f23d1dea
73c75572-72f96e8d
b21f80-3668efa6
6166a7f-617e75d8
ee81190c-3f4a17df
8c0a964a-615737e1
4b1af6a5-2c07ccaf
8704866f-2edf459f
7a88d725-c65c0ed
abac8c9c-d1e7c2b3
507bff23-cc5c4f8c
d6f45283-f23d1dea
89986dbe-1410f10
4cc571d9-f23d1dea
d99b5d-28f3f77f
9ab96e3-d8e50c9a
3f5b2031-3b1802be
580a9761-e08dbdc6
590c3834-f23d1dea
ce1c1bed-50e64713
58ecc37a-3f4a17df
66abf9c6-3f4a17df
a1e5b5f5-45e611f9
de2a296c-38b4e628
4223ef11-f23d1dea
bff5056b-7304c056
94e21eca-38b4e628
6b23255-d32665f9
91990785-ed39c668
9d165456-12b32dff
a063a097-f23d1dea
24269aa8-b2694c5e
afa6e3c-12b32dff
8f80c10-f23d1dea
7ac84b22-3bc6d251
a62c052e-45e611f9
cbc0b4bb-e74e8556
6c9cf024-e4b3e18f
1eb32835-3f4a17df
9e17aca1-17606bad
28c4043d-371e4aa7
ec937206-3f4a17df
6025934e-3f4a17df
c178cf5-c20daa92
2a71e74f-3f4a17df
64b725ce-72c20c49
58035371-f23d1dea
832b8234-9d9e26c4
54d601a5-7255afe3
999e8980-b9386c08
41e765a5-f2622d89
f314f5b9-366a9213
36726ffb-3f4a17df
2eb01e0a-4cb74ed2
6c7e9dc6-f23d1dea
4385c43e-eb164536
3747a4f2-f23d1dea
e14ee5ee-305d45a1
1ece817e-4a62d861
fc1790de-f23d1dea
11d973f6-f23d1dea
3779be93-2bcc3773
f32b2e65-2758793c
a582a1b8-5ad3f43d
bd6dd170-53ba0e82
9554a831-3f4a17df
68f499c8-ca7d8d80
b318ffd-9547bab5
7a0fa40a-4ad60575
87684b46-38b4e628
3606b64e-ed3e37c1
ce9fa089-f23d1dea
bac1cdd-f23d1dea
9680f843-ca7d8d80
7e6af697-362d0d74
a716fea0-3f4a17df
3e672fd9-ac64c575
ae1581ef-85ca1fba
255aa854-2c007b12
9cf6c713-a4256e92
78049c75-8092bf7d
7b94f396-ca7d8d80
d7ea6e04-18064ad6
96d006a-daa0bf89
f552eb19-c6d4c740
743dd923-31090a32
b5ddc834-1c78016a
be526704-3f4a17df
1683ee3a-ca7d8d80
5e3a236d-59e286d0
930b1a0-f23d1dea
b85fc163-3f4a17df
d43ddfd9-b20da897
fecdbadb-f23d1dea
3f032b9f-72f96e8d
51165636-72c20c49
a716659b-3c502689
6ec84df5-943f231d
8a9719ac-d5eca890
cbe8c9f8-e16c1d15
cacd54c8-ca7d8d80
f7b9a9e3-2758793c
ca130381-b2694c5e
8b7b96c7-d1e7c2b3
81c84cff-8fbcbfa1
4076100b-108cf35e
d649160f-bebc2386
80258df6-13b50ba9
62e82091-59e286d0
8f418b04-65632614
72c1eeea-e2e589d8
bcb143fe-afa46f38
b9ffbd4a-efd18772
59a12fbe-35355319
de028327-ca7d8d80
5ac9f58-3f4a17df
6495cb0f-f23d1dea
ba9b9c76-aff6cce1
eed5bb5e-b8c6f53e
66b7a83f-f23d1dea
d721a76b-3f4a17df
4ea303a6-ecbb250e
e35e8246-7973e862
11b4cb76-f23d1dea
b56c57ae-d9417f7c
82b178a6-20afc8eb
c8f6111a-ca7d8d80
bf46f37a-50e64713
40de0170-f23d1dea
5c78b732-f23d1dea
cae19fc9-94a80f74
82b6db25-e16c1d15
412429ed-ca7d8d80
b6f29041-92970c
d0fa45e6-73cdab1
e85106e5-6042f503
c046d00b-d1e7c2b3
e3559213-68f20d64
8082e3d1-3ac589b9
a374fdf0-1df864c9
9a1e45b8-377be55a
ff29b1bd-c690bc69
53fa9d2a-2758793c
89ccddbe-f23d1dea
a8df36b5-afbbe761
c8997723-f23d1dea
fdad6755-f23d1dea
b7f7e802-823fa09a
ea89c38c-f23d1dea
bc7471e4-3f4a17df
94b88ba6-3f4a17df
58db629a-f23d1dea
74aec266-f020d8d4
af295c80-f23d1dea
90855740-3f4a17df
30bcdd88-f8d07804
941406f8-2f43229e
494d8760-52325d43
3ac60855-486e2a9c
f48c01d3-9aeeedc9
63dcb6a3-84d9448d
e706e746-477de798
f296190c-610f13e6
4442aae2-a90023b1
f690cf64-4ad60575
ed1d377-e1cc0f14
75f0f0a0-6bdfffe7
710c3f90-4ad60575
e2b18481-e1cc0f14
e7e71889-e1cc0f14
90e10a4-3f4a17df
2f6246c2-34533ac9
b6e701e2-ca7d8d80
7d758b3c-3f4a17df
45e0e828-f23d1dea
aa8204ea-f23d1dea
89fd5de1-f1e7ab1
6332ffaf-8cd0bc9c
cb1fd885-f23d1dea
1572bcde-dd411bc1
638418b3-3f4a17df
c10b07d0-f23d1dea
e92dc7d-9bedbb42
a68352e7-7c73a71a
3c8a4df0-5d219690
51ef5a7e-f23d1dea
55212d34-e12bd7c1
b357b792-c836f3a2
f4f00e05-3f4a17df
6c377b0f-a744f381
9481ce98-3d47f4f4
2a426c03-3d47f4f4
aca9df2c-3f4a17df
a3bc7210-5762d4a7
b100ac4-dee66fa8
4651ad61-8533ea9a
59748665-8e9604d4
65250343-999b333
553aead6-4a95a5b1
fe4babb8-4a95a5b1
6205871c-4a95a5b1
382b54bb-29f03e2f
70678518-206f6a6e
be338734-4a95a5b1
6f316e34-cc562941
5f9907a9-206f6a6e
8eeccb9a-c35b209e
2b465683-3601ad67
52fc7926-ee3d6169
bc9b361d-dee66fa8
a41a7188-b184655b
ff71bfdc-dee66fa8
a6fa7475-dee66fa8
2159dd0c-52ab4875
92cfa89f-dee66fa8
6daa4147-dee66fa8
8601fbe0-3d47f4f4
4ed45b7a-3d47f4f4
4b935545-3d47f4f4
9a38bae3-6046c8a7
2d1e43a3-3d47f4f4
30e58f57-ca7d8d80
c4a500a4-3d47f4f4
370ace14-3f4a17df
386dc267-3d47f4f4
d69d967d-894154fa
3c8f75a1-7a2089c1
a4406b35-ccf52fb6
408da146-1657e2d6
d4e26075-fea05d06
f6918184-a714ab2
dc20670d-3f4a17df

### sa...@gmail.com (2025-09-22)

This is the variation

### sa...@gmail.com (2025-09-22)

i can repro on stable and beta  but it must modified the code in spoofkeyboard.html part of this:

setTimeout('history.go(-1);',350);  changed into   setTimeout('history.go(-1);',600);

### sa...@gmail.com (2025-09-22)

hi pn...@google.com 
i updated the poc , may you tried the poc ?

1.download detx1.html, spoofkeyboard1.html in same folder / host detx1.html,spoofkeyboard1.html on local web server using https:// protocol
2. open https://you-can-billowy-nimble-login-secure-docs-google-source-attacker.com/detx1.html or open detx1.html on local web server using https: protocol
3. click the button
4. clik the go to google button

### pn...@chromium.org (2025-09-22)

I appreciate your prompt responses. Unfortunately, no luck yet on my end reproducing with the updated PoC. The variations haven't really turned up anything obvious either, especially given that you can repro on Beta/Stable which no doubt have a totally different set of variations.

### sa...@gmail.com (2025-09-22)

It seems like this bug is different from 446539525, in this bug when the web background color is set to white, the minibar becomes clearly visible, whereas when the web background color is set to a darker color (other than white such as red, blue, black, etc.), the URL text in the minibar becomes white so it is not visible because the minibar background color is white.

### pn...@chromium.org (2025-09-22)

> whereas when the web background color is set to a darker color (other than white such as red, blue, black, etc.), the URL text in the minibar becomes white so it is not visible because the minibar background color is white.

But the minibar text is only white when the minibar background, which matches the web background color, is sufficiently dark to warrant it. If you're seeing the minibar background as white bg + white text I think it's more likely that the minibar is just not being rendered at all vs having an incorrect bg color. But without a repro I can't say one way or the other.

### sa...@gmail.com (2025-09-22)

i updated the poc on https://issues.chromium.org/issues/446463993#comment12

### ch...@google.com (2025-09-23)

Setting milestone because of s2 severity.

### ch...@google.com (2025-09-23)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pn...@chromium.org (2025-09-23)

Got a repro. Mea culpa, you were right about the coloring being key. Next time I'll wait to repro instead of speculating.

### dx...@google.com (2025-09-23)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6976339>

[mobar] Update mobar bg color in sync with toolbar primary color

---


Expand for full commit details
```
     
    The source of truth for this is is ToolbarDataProvider. This avoids the 
    rare but bad case of color changes while the mobar is showing. 
     
    Bug: 446463993 
    Change-Id: I6268839d362865245473ccef31220b90a8af0d82 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6976339 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1519663}

```

---

Files:

- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/LocationBarModel.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/ToolbarDataProvider.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/top/ToolbarControlContainer.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/top/ToolbarControlContainerTest.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/top/TopToolbarCoordinator.java`

---

Hash: [b6d8c675b3417e6e3bafb37921d4f914eb8b25f6](https://chromiumdash.appspot.com/commit/b6d8c675b3417e6e3bafb37921d4f914eb8b25f6)  

Date: Tue Sep 23 23:27:56 2025


---

### sa...@gmail.com (2025-09-24)

Is this already fixed?

### pn...@chromium.org (2025-09-24)

The fix has not made it to Canary yet; lets verify tomorrow

### sa...@gmail.com (2025-09-25)

I confimed i cannot repro the poc on version 142.0.7433.0

### pe...@google.com (2025-09-25)

The NextAction date has arrived: 2025-09-25
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ch...@google.com (2025-09-26)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@chromium.org (2025-09-26)

1. <https://chromium-review.googlesource.com/6976339>
2. yes
3. No
4. No
5. No

### ch...@google.com (2025-10-01)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [141, 142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@chromium.org (2025-10-01)

See #26

### ts...@google.com (2025-10-06)

S2, so avoiding merge to stable, but let's shoot for m142 (7444) ideally by 7-Oct, but realizing this is short notice.

### pn...@chromium.org (2025-10-06)

No merge needed for 142 as this landed ahead of branch; what tag should I use for that?

### ch...@google.com (2025-10-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2025-10-20)

[Bulk Edit]
Please merge your change to M142 by 4:00 PM PT today, M142 Early Stable RC cut tomorrow morning PT. Thank you. 

### sp...@google.com (2025-10-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
somewhat mitigated omnibox spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> somewhat mitigated omnibox spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/446463993)*
