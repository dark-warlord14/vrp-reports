# Chromium illegally paints outside of iframe when using -webkit-box-reflect

| Field | Value |
|-------|-------|
| **Issue ID** | [40055233](https://issues.chromium.org/issues/40055233) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals>Compositing |
| **Platforms** | Android, Linux |
| **Reporter** | pr...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2021-03-17 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36

Steps to reproduce the problem:
1. open "parent.html" on Chrome 89.0.4389.90 (official stable).
2. download "iframe.html" and load it by executing JS code.

prepare_iframe('iframe.html');

This will make iframe and import "iframe.html" onto "parent.html"

What is the expected behavior?
The contents of iframe should not be painted outside of iframe.

What went wrong?
The contents of iframe is drawn outside of iframe (as shown in ref.png).

Did this work before? N/A 

Chrome version: 89.0.4389.90  Channel: stable
OS Version: 18.04
Flash Version:

## Attachments

- [ref.png](attachments/ref.png) (image/png, 65.9 KB)
- [parent.html](attachments/parent.html) (text/plain, 315 B)
- [iframe.html](attachments/iframe.html) (text/plain, 1.4 KB)
- [ref2.png](attachments/ref2.png) (image/png, 269.5 KB)
- iframe.html (text/plain, 217 B)
- iframe.html (text/plain, 239 B)
- [main.html](attachments/main.html) (text/plain, 287 B)
- iframe.html (text/plain, 432 B)
- [samsungs21_chrome.jpg](attachments/samsungs21_chrome.jpg) (image/jpeg, 40.4 KB)
- [f955c742-f1ab-407a-8df4-44b3038015ca.png](attachments/f955c742-f1ab-407a-8df4-44b3038015ca.png) (image/png, 27.1 KB)
- iframe.html (text/plain, 568 B)
- [Screenshot_20221018-101544_Chrome.jpg](attachments/Screenshot_20221018-101544_Chrome.jpg) (image/jpeg, 57.1 KB)

## Timeline

### [Deleted User] (2021-03-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-03-17)

Thanks for this report! Very cool.

I can't get it to reproduce on Chrome OS (88.0.4324.186 (Official Build) (64-bit)), though. Maybe it's Linux-specific, or graphics driver-specific?

Can anyone reproduce this? Please feel free to CC anyone who can help. Thanks!

[Monorail components: Blink>CSS Blink>HTML>IFrame]

### da...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-03-17)

Iframe here is not an OOPIF so it's not a separate surface in the compositor. If it were the compositor would enforce a clip around it. This may be a painting bug then. Maybe an iframe should be clipped in paint as well.

kylechar can you have a look and confirm?

### fu...@chromium.org (2021-03-17)

[Empty comment from Monorail migration]

[Monorail components: -Blink>CSS Blink>Paint]

### [Deleted User] (2021-03-17)

[Empty comment from Monorail migration]

### pd...@chromium.org (2021-03-17)

I bisected this to https://chromium.googlesource.com/chromium/src/+log/3fc155bbfc3c1c0b13ced21abb575e213ab013b1..6e4cbcc8b2dfd93e84c11b9b9f285ee03ff9e3ee

I think this is likely to be https://crrev.com/799525, and confirmed this repros with CompositingOptimizations and not without it.

### ch...@chromium.org (2021-03-18)

I can reproduce the issue. Debugging now.

### ch...@chromium.org (2021-03-18)

Further reduced iframe.html attached.

### ch...@chromium.org (2021-03-18)

Another version attached. I can reproduce the issue also without CompositingOptimizations by moving #target up 5px via margin-top: -5px.
Also, it has nothing to do with backface-visibility specifically, any compositing trigger will do. 

It does seem to require indirect compositing for #target though. If I add a direct compositing reason for it the bug is gone.

### ch...@chromium.org (2021-03-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-03-18)

[Empty comment from Monorail migration]

### ch...@chromium.org (2021-03-18)

-> pdr to triage next steps.

My guess is the root cause is that the box reflection is escaping clip from the iframe. Either because we optimized away the clip, or the cc property trees are wrong.

### pd...@chromium.org (2021-03-22)

Stefan, can you take a look at this bug?

### sz...@chromium.org (2021-03-23)

Looking...

### ke...@chromium.org (2021-03-29)

Assigning Severity-Low on the basis that the iframe will normally have to be same-site with its embedder for this to happen, since it does not affect OOPIFs.

### es...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### pr...@gmail.com (2022-09-01)

I think this bug can be very malicious on Android OS because Android OS does not use OOPIFs.
Could you please review this bug again?

### bo...@chromium.org (2022-09-01)

Hi there, this is your friendly security sheriff checking in. 

Bumping to Medium Severity because it has plausible security implications for Android over the foreseeable future.

 

### ke...@chromium.org (2022-09-01)

This is marked as OS=Linux, has it been reproduced on Android?

### pr...@gmail.com (2022-09-02)

I attached other poc for reproduction and the screenshot of Android Chrome.
I also used two different domains (one for main and the other for iframe) to reproduce this bug on Android.

How to reproduce.
1. Download main.html and iframe.html
2. Open terminal and move to directory that main.html and iframe.html are stored.
3. Run two http servers: port 8000 for main.html and 9000 for iframe.html
   i) python3 -m http.server 8000
   ii) python3 -m http.server 9000

4. Open http://0.0.0.0:8000/main.html on chrome.
5. Or change 0.0.0.0 to ip address and open on android.

Chrome Version: 104.0.5112.97 + stable
Operating System: Android 12

### bo...@chromium.org (2022-09-02)

Adding Android OS tag per c#20 and c#21

### [Deleted User] (2022-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

szager: Uh oh! This issue still open and hasn't been updated in the last 533 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

szager: Uh oh! This issue still open and hasn't been updated in the last 548 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sz...@chromium.org (2022-10-13)

I can no longer reproduce this, tried ChromeOS/107.0.5304.14 and Android/108.0.5340.9 using this perma-link:

https://shining-tropical-pencil.glitch.me/

I'll leave this open for another week for feedback before closing wontfix.

### sz...@chromium.org (2022-10-13)

Perma-link for the reproduction described in https://crbug.com/chromium/1189131#c21, with cross-origin iframe:

https://chestnut-linen-icecream.glitch.me/

Attached screenshot from Android

### pr...@gmail.com (2022-10-18)

I tried Android/106.0.5249.126 using the attached iframe.html.

Please try this permanent link: https://garnet-peppermint-allspice.glitch.me/




### sz...@chromium.org (2022-10-18)

I can reproduce the failure from https://crbug.com/chromium/1189131#c31 on Android/108.0.5354.5, though not on ChromeOS.

I'll start digging into it.

### sz...@chromium.org (2022-10-20)

The fact that the bug is platform-dependent suggests to me that it's not a bug in blink, because all the blink code involved here is platform-agnostic.

Sending this to the graphics/compositing team for further triage.

[Monorail components: -Blink>HTML>IFrame -Blink>Paint Internals>Compositing]

### ke...@chromium.org (2022-11-02)

zmo@: Can you please help find an owner for this security bug?

### zm...@chromium.org (2022-11-03)

Vasily, can you take a look?

### [Deleted User] (2022-12-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2022-12-05)

So I did look a bit into this and in the repro case cc creates render pass that is larger than iframe and there is no clip rect, so display compositor just draws it. I suspect that only in-process iframes are affected (display compositor should enforce clipping of SurfaceDrawQuad for OOP-IFs), but I haven't verified that yet. 

I'll try to find where it comes from cc, but I'm not very familiar with how cc allocates render surfaces.

### [Deleted User] (2023-01-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-26)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-18)

This issue has not been updated for 60 or more days - lowering its priority to P2.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2023-04-27)

[Security Marshal]

I checked I can still reproduce on Android.
On desktop, I can reproduce by disabling OOPIF:
```
google-chrome-unstable --disable-site-isolation-trials https://garnet-peppermint-allspice.glitch.me/
```


@vasilyt, would you have an update on this?

### ar...@google.com (2023-04-27)

[Security Marshal]

From code:

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/core/paint/box_reflection_utils.cc;l=55-58;drc=332f92aab4a32607f7813ac1a824f6ff0d86c369;bpv=1;bpt=0
```
  PhysicalRect mask_rect(PhysicalOffset(),
                         layer.GetLayoutBox()->FrameRect().Size());
  PhysicalRect mask_bounding_rect(mask_rect);
  mask_bounding_rect.Expand(style.ImageOutsets(mask_nine_piece));
```

I see we are expanding the mask_bound_rect. Maybe this is as simple as that?


From the code, I believe @wangxianzhu might be able to help fixing this security bug, or finding a good owner. Could you please take a look?

### wa...@chromium.org (2023-04-27)

I don't think the root cause is the expansion (it's needed), but the expanded rect is not properly clipped by the iframe's overflow clip. It seems that this is OOPIF only? Then the problem is in OOPIF code calculating the geometry of the OOPIF, not the code above.

[Monorail components: Internals>Sandbox>SiteIsolation]

### cr...@chromium.org (2023-04-27)

https://crbug.com/chromium/1189131#c47: All the previous discussion (e.g., https://crbug.com/chromium/1189131#c4, https://crbug.com/chromium/1189131#c45, etc) say this is about the non-OOPIF case.

### pg...@google.com (2023-07-19)

Hi Xianzhu! Might you be able to find a better owner for this? Please keep security bugs assigned to someone (:

We can reproduce the issue by disabling OOPIF - does that provide you with more context to identify where the root cause may be?

### wa...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Sandbox>SiteIsolation]

### [Deleted User] (2023-07-21)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-07-25)

I got in contact with wangxianzhu@ and they said they won't be able to look closely for a few weeks. I'll set a next action date for 4 weeks from now.

### wa...@chromium.org (2023-08-22)

[Empty comment from Monorail migration]

### wa...@chromium.org (2023-08-28)

On desktop, the bug started to reproduce in https://chromium.googlesource.com/chromium/src/+log/be82cef6def900567e84acd2ea15459217cf2cad..601731e922911904ea2b9a741be1971ee2940366 (105.0.5183.0) and was fixed in https://chromium.googlesource.com/chromium/src/+log/be82cef6def900567e84acd2ea15459217cf2cad..601731e922911904ea2b9a741be1971ee2940366 (117.0.5889.0). Verified that this bug doesn't reproduce on the latest canary on Android/Desktop.

Both the regression range and the progression range contain my change about clips of filters. However, this bug was reproduced earlier on Android than the desktop regression range (105.0.5183.0), which may indicate there was/is some underlying issue somewhere causing the output clip of filter to affect whether the clip state of a layer is applied to the filtered result. Nevertheless, as now blink always set output clips of filters, the condition of the issue no longer exists.  



### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-19)

wangxianzhu@ it appears that you used the same link twice in https://crbug.com/chromium/1189131#c56, can you please update the revision range in which this issue was resolved or provide the gerrit link or commit hash for this fix. Thank you. 

### wa...@chromium.org (2023-09-19)

Sorry for the wrong link. The second link should be https://chromium-review.googlesource.com/c/chromium/src/+/4658020. I believe the fix was just a side effect of the CL and the root cause has not been fixed yet. The root cause will probably be fixed for https://crbug.com/chromium/1478908 which tracks a case similar to this one.

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-04)

[Comment Deleted]

### am...@chromium.org (2024-01-04)

This is a single root cause and issue demonstrated in separate reports. Both reports are from the same reporter so I'm merging this issue into the newer report since the fix was landed there. 

### is...@google.com (2024-01-04)

This issue was migrated from crbug.com/chromium/1189131?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1357465]
[Monorail mergedinto: crbug.com/chromium/1478908]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055233)*
