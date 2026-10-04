# Security: <select> data can cross browser line of death if input box is too large

| Field | Value |
|-------|-------|
| **Issue ID** | [424995036](https://issues.chromium.org/issues/424995036) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>Forms>Select, Blink>SecurityFeature |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2025-06-14 |
| **Bounty** | Confirmed (amount unknown) |

## Description

**VULNERABILITY DETAILS**

The PopupWidgetHost interface [1] allows a renderer to create a popup window, intended for features like dropdown menus. If the renderer is compromised, then it can set arbitrary bounds on the popup window, and paint arbitrary content in it. This allows the attacker to spoof trusted browser UI such as the omnibox, tricking the user into thinking they're on a different origin.

For simplicity, the attached poc.patch hardcodes the popup window bounds. A real attacker would likely want to adjust the bounds according to the browser window position (window.screenX, window.screenY), the browser window width (window.outerWidth), and the height of the browser UI (window.outerHeight - window.innerHeight). They may also choose to only cover the omnibox, to avoid the need to spoof other UI elements like the tabstrip.

Similarly, the attached poc.patch hardcodes a bitmap to use as the popup window content. A real attacker may generate the content more dynamically so as to match the user's OS and respond to user input.

The attached poc.patch also doesn't prevent the user from closing the popup, for example by clicking the page. A real attacker could prevent that by ignoring such clicks [2], or they could simply show a new popup whenever the current one gets closed.

Other examples of what the attacker could use this for include:

- Spoof other security-sensitive UI such as permission prompts, tricking the user into thinking they're granting permission for some other feature or for some other origin.
- Spoof content or security-sensitive UI relating to other tabs/windows, including those displaying content from other origins. Note that although creating a popup window requires the originating page to be visible [3], showing an already-created popup window doesn't have that requirement [4], so such spoofs are possible even if the attacker's page is invisible or occluded (bypassing the fix for <https://crbug.com/41494315>), by showing the popup window after the user switches to another tab, or by showing it over an auxiliary tab/window created by the attacker via window.open.
- Spoof a credential prompt in its entirety, for example by showing a fake OAuth popup window, or a fake HTTP authentication prompt, or a fake OS-level prompt for user/network credentials.
- Cover the entire screen with an uncloseable attacker-controlled window, perhaps claiming to be ransomware.

**VERSION**

Chrome Version: 137.0.7151.104 stable  

Operating System: Windows 10.0.19045

**REPRODUCTION CASE**

1. Build Chromium with the attached poc.patch, which simulates a compromised renderer.
2. Go to <https://www.example.com>.
3. Observe that the URL in the omnibox changes to <https://www.google.com>, despite the content area displaying <https://www.example.com>.

**BISECT**

With the attached poc.patch I can repro on at least:

- Chromium 139.0.7237.0 r1473483 (recent ToT)
- Chromium 137.0.7151.104
- Chromium 108.0.5359.0 r1058968

So the bug has existed for at least a few years and it looks like it impacts all active Chrome release channels including current Chrome 137.0.7151.104 stable.

I tested on Windows but I suspect this applies to other platforms too.

**FIX**

A potential fix could be to restrict popup windows to the content area (like Firefox does, at least for dropdown menus), and deny attempts to show a popup window if the originating page isn't active.

**CREDIT INFORMATION**

Reporter credit: Anonymous

[1] <https://chromium.googlesource.com/chromium/src.git/+/186d68e449ac3356147d86062d7e25be371a283b/third_party/blink/public/mojom/page/widget.mojom#229>  

[2] <https://chromium.googlesource.com/chromium/src.git/+/186d68e449ac3356147d86062d7e25be371a283b/third_party/blink/renderer/core/input/event_handler.cc#844>  

[3] <https://chromium.googlesource.com/chromium/src.git/+/186d68e449ac3356147d86062d7e25be371a283b/content/browser/web_contents/web_contents_impl.cc#5446>  

[4] <https://chromium.googlesource.com/chromium/src.git/+/186d68e449ac3356147d86062d7e25be371a283b/content/browser/web_contents/web_contents_impl.cc#5582>

## Attachments

- [poc.patch](attachments/poc.patch) (text/x-diff, 13.9 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 350.3 KB)

## Timeline

### dr...@chromium.org (2025-06-16)

[security triage] Thank you for the report! This is quite a good omnibox spoof. I'm testing on Linux, and the image styling and position don't quite line up, but I'm sure you can fix it. I do hit [this DCHECK](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/internal_popup_menu.cc;drc=33bc4b06a9ed6afd05d0065f907910e1da59e712;l=278) after a second, default, but that's also not going to affect users in the wild.

### dr...@chromium.org (2025-06-16)

It doesn't seem like anyone has changed any of this in a long time, and there's no local OWNERS files. Choosing a few random third\_party/blink/renderer/OWNERS in hopes that someone has some context on this.

### ch...@google.com (2025-06-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### es...@chromium.org (2025-06-17)

 "Complete control over the apparent origin in the omnibox" = High => Medium with the mitigating factor of needing a compromised renderer per https://chromium.googlesource.com/chromium/src/+/lkgr/docs/security/severity-guidelines.md

### es...@chromium.org (2025-06-17)

Adding Blink forms owners. Is it possible to constrain the popup created through InternalPopupMenu to the bounds of the web contents that creates it?

### db...@chromium.org (2025-06-25)

There's some possibly relevant discussion in [issue 40065947](https://issues.chromium.org/issues/40065947). Based on [this testcase](https://software.hixie.ch/utilities/js/live-dom-viewer/?%3C!DOCTYPE%20html%3E%0A%3Ciframe%20height%3D30%20width%3D200%20srcdoc%3D%22%3Cselect%3E%3Coption%3EOne%3C%2Foption%3E%3Coption%3ETwo%3C%2Foption%3E%3Coption%3EThree%3C%2Foption%3E%3Coption%3EFour%3C%2Foption%3E%3Coption%3EFive%3C%2Foption%3E%3Coption%3ESix%3C%2Foption%3E%3Coption%3ESeven%3C%2Foption%3E%3Coption%3EEight%3C%2Foption%3E%3Coption%3ENine%3C%2Foption%3E%3Coption%3ETen%3C%2Foption%3E%3C%2Fselect%3E%22%3E%3C%2Fiframe%3E) (including some resizing of the browser window while testing it) Firefox constrains `<select>` popups to the toplevel frame, though not to the iframe bounds. Based on Firefox behavior, it seems likely that constraining popups to the toplevel document may be a web-compatible change. But if we wanted to pursue it we'd need to roll it out carefully.

### ch...@google.com (2025-07-02)

keishi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-17)

keishi: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-01)

keishi: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-16)

keishi: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-31)

keishi: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-15)

keishi: Uh oh! This issue still open and hasn't been updated in the last 89 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-30)

keishi: Uh oh! This issue still open and hasn't been updated in the last 104 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-15)

keishi: Uh oh! This issue still open and hasn't been updated in the last 119 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-30)

keishi: Uh oh! This issue still open and hasn't been updated in the last 134 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-14)

keishi: Uh oh! This issue still open and hasn't been updated in the last 149 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-29)

keishi: Uh oh! This issue still open and hasn't been updated in the last 164 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-14)

keishi: Uh oh! This issue still open and hasn't been updated in the last 179 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-29)

keishi: Uh oh! This issue still open and hasn't been updated in the last 194 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-13)

keishi: Uh oh! This issue still open and hasn't been updated in the last 209 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-28)

keishi: Uh oh! This issue still open and hasn't been updated in the last 224 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-12)

keishi: Uh oh! This issue still open and hasn't been updated in the last 239 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ke...@google.com (2026-02-20)

The complete fix of limiting popup bounds will break web apps. So I will mark this as WontFix.
But at the same time it is a good idea to add a bit more hardening so I've created a CL to do that.
https://chromium-review.googlesource.com/c/chromium/src/+/7593475

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Keishi Hattori [keishi@google.com](mailto:keishi@google.com)  

Link:    <https://chromium-review.googlesource.com/7593475>

Prevent background tabs from showing PopupWidgetHosts

---


Expand for full commit details
```
     
    A compromised renderer may try to show a popup to do UI spoofing. 
     
    Currently, Chromium checks if a tab is visible when *creating* a popup 
    (in CreateNewPopupWidget), but it does not re-verify visibility when 
    the popup is actually *shown* (in ShowCreatedWidget). 
     
    This CL adds the check to ShowCreatedWidget to close the 
    TOCTOU vulnerability. 
     
    Bug: 424995036 
    Change-Id: Ib45df5cf566a95d1da48b386ad55976d2d2366fe 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7593475 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Commit-Queue: Keishi Hattori <keishi@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593031}

```

---

Files:

- M `content/browser/web_contents/web_contents_impl.cc`

---

Hash: [948f7d11cebca4b17171e7038d93d311db2c5cfa](https://chromiumdash.appspot.com/commit/948f7d11cebca4b17171e7038d93d311db2c5cfa)  

Date: Tue Mar 3 07:50:36 2026


---

### fo...@gmail.com (2026-03-14)

Thanks for the partial fix. Is this still VRP-eligible? I see it's not yet on the reward-topanel hotlist.

### dr...@chromium.org (2026-03-19)

Hm let me marked it fixed so I don't have to fight with automation.

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### wf...@chromium.org (2026-06-04)

re [comment#25](https://issues.chromium.org/issues/424995036#comment25) are there not reasonable measures we can take here such as preventing painting over the omnibox or sensitive UI? Please can you provide a concrete reason why this would not be possible?

### ke...@google.com (2026-07-29)

It seems like we could do that but changing that policy will have a widespread impact so I don't know.
Assigning to Mason.

### ma...@google.com (2026-09-18)

I wish the bot was working. <https://crrev.com/c/8379462> landed 4 days ago. I'm marking this Fixed.

### sp...@google.com (2026-10-02)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided to issue a reward of
**$3000.00** for your report. Congratulations!

Rationale for this decision:

UI spoof - omnibox

Important payment guidance:

- **Legacy**: If you aren't already registered with Google as a supplier,
  [p2p-vrp@google.com](mailto:p2p-vrp@google.com) will reach out to you. If you have registered in the
  past, no need to repeat the process – you can sit back and relax, and we
  will process the payment soon.
  
  If you have any payment related requests, please direct them to
  [p2p-vrp@google.com](mailto:p2p-vrp@google.com). Please remember to include the subject of this email and
  the email address that the report was sent from.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot

P.S. One other thing we'd like to mention:

- Please do NOT publicly disclose details until a fix has been released to all
  our users. Early public disclosure may cancel the provisional reward. Also,
  please be considerate about disclosure when the bug affects a core library
  that may be used by other products. Please do NOT share this information
  with third parties who are not directly involved in fixing the bug. Doing so
  may cancel the provisional reward. Please be honest if you have already
  disclosed anything publicly or to third parties. Lastly, we understand that
  some of you are not interested in money. We offer the option to donate your
  reward to an eligible charity. Any rewards that are unclaimed after 12
  months will be donated to a charity of our choosing.

Please contact [security-vrp@chromium.org](mailto:security-vrp@chromium.org) with any questions.

## Bounty Award

> UI spoof - omnibox
> 
> 
> 
> 
> 
> 
> 
>   
>     
>   
> 
> 
> Important payment guidance:
> 
> 
> *   **Legacy**: If you aren't already registered with Google as a supplier,
>     p2p-vrp@google.com will reach out to you. If you have registered in the
>     past, no need to repeat the process – you can sit back and relax, and we
>     will process the payment soon.
> 
>     If you have any payment related requests, please direct them to
>     p2p-vrp@google.com. Please remember to include the subject of this email and
>     the email add

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/424995036)*
