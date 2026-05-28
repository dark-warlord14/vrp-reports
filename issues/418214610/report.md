# Security: Permission prompt spoofs with Google Sans font ligatures (similar to issue 391788835)

| Field | Value |
|-------|-------|
| **Issue ID** | [418214610](https://issues.chromium.org/issues/418214610) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>LookalikeChecks |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2025-05-17 |
| **Bounty** | $10,000.00 |

## Description

## SUMMARY

Similar to [issue 391788835](https://issues.chromium.org/issues/391788835), the Google Sans font ligatures can be used to spoof origin in various permission prompts.

## VULNERABILITY DETAILS

While the fix for [issue 391788835](https://issues.chromium.org/issues/391788835) (<https://crrev.com/c/6227546>) shows an interstitial for top-level navigations if the domain contains a blocked ligature, iframes are allowed to navigate to URLs with domains containing these ligatures.

An iframe at `https://googlelogoligature.com` can open a new window to `about:blank` which will still be in the origin with ligatures. The opener iframe can then request permissions using the origin with ligatures. All the permission UIs we tested don't seem to sanitize these ligatures.

Affected permission prompts we've tested:

- Camera
- Microphone
- Location
- Notification
- Read clipboard
- Bluetooth
- USB
- Contacts

Probably all other permission prompts are affected.

## VERSION

Verified repro on these versions:

Chrome version: 136.0.7103.87 Stable, 137.0.7151.23 Beta, 138.0.7178.0 Dev, 138.0.7180.0 Canary

Operating System: Android 14, Android 15

## REPRODUCTION CASE

Setup:

1. Make your Android device resolve `googlelogoligature.com` to your malicious server that hosts a downloadable file. In my case, my router lets me override DNS entries so it's easy to test on physical device. For emulated devices, not sure if host's DNS resolution would affect the emulated devices.
2. Navigate once to <https://googlelogoligature.com> and accept the HTTPS warning (but NOT the fake site warning). Note that an attacker can get a valid cert for the ligature domains, so this is only needed for PoC.

### Permissions scenarios

1. Navigate to <https://alesandroortiz.com/security/chromium/ligatures-perm.html>
2. Click anywhere.
3. If indicated by instructions, click anywhere again. (This is for perm prompts that require user interaction.)

Repeat steps 1-3 for each variation using the in-page links.

Observed: Permission prompts shows spoofed origin (with font ligature).

Expected: Permission prompts show actual origin.

## Credit Information

Reporter credit: NDevTK <https://ndevtk.github.io/writeups/> and Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [ligatures-perm.html](attachments/ligatures-perm.html) (text/html, 1.6 KB)
- [ligatures-perm-frame.html](attachments/ligatures-perm-frame.html) (text/html, 2.5 KB)
- [ligatures-perm.mp4](attachments/ligatures-perm.mp4) (video/mp4, 18.1 MB)
- [elide_url.diff](attachments/elide_url.diff) (text/x-diff, 2.0 KB)
- [subframe-blocked-console-message.png](attachments/subframe-blocked-console-message.png) (image/png, 32.6 KB)
- [subframe-blocked.jpg](attachments/subframe-blocked.jpg) (image/jpeg, 143.7 KB)
- [subframe-blocked-active.jpg](attachments/subframe-blocked-active.jpg) (image/jpeg, 163.2 KB)

## Timeline

### al...@alesandroortiz.com (2025-05-17)

Please CC NDevTK when possible: [ndevtk@protonmail.com](mailto:ndevtk@protonmail.com)

### al...@alesandroortiz.com (2025-05-17)

Ignore the part that says `that hosts a downloadable file`, that's from another report.

### al...@alesandroortiz.com (2025-05-17)

This spoof also works with all the other ligatures identified in [issue 391788835](https://issues.chromium.org/issues/391788835). Pasting here for easier reference.

"googlelogoligature",
"glogoligature",
"ologoligature",
"llogoligature",
"elogoligature",
"g\_logo",
"o\_logo",
"l\_logo",
"e\_logo",
"google\_logo",
"google\_g",
"super\_g\_logo"

### al...@alesandroortiz.com (2025-05-17)

Many of these prompts use UrlIdentity to get the origin to display, and it does some IDN-related checks, so this might be a good place to change this to something safe to display.

Specifically `CreateFromUrl()` which calls `CreateDefaultUrlIdentityFromUrl()`.

This assumes the fix is to somehow change the output text. I'm not sure if that would work, since I think the font ligature means it'll be formatted automatically in the UI if the same string is provided. And we can't represent the string any other way in the same font, I think. Not sure if there's a way to easily disable ligatures completely in these UIs or only in the bits of UI showing the origin, or if some ligatures are needed, then at least when these spoofy ligatures are detected.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/url_identity.cc;l=138;drc=2ebedf8d40cdcd8bb6ad3c865d2d3133d85eaa47>

### al...@alesandroortiz.com (2025-05-17)

That call site is also used by other UI that has the spoof, such as the Site Settings and other browser UI. Not sure what attack scenarios would be for those, beyond user confusion when manually managing site settings, so haven't reported those separately.

### al...@alesandroortiz.com (2025-05-17)

A janky way of preventing the ligature might be adding a zero-width space or something similar that prevents the ligature from rendering but keeps the original text visually intact?

I'm not familiar with font rendering or ligature handling in Chrome, but I can't seem to find any similar treatments or an easy flag (on Chrome or Android) to prevent some or all ligatures from rendering in UI with untrusted inputs. And I think ligatures are legitimately used for many languages, so disabling them completely is probably not a good idea.

### al...@alesandroortiz.com (2025-05-17)

On Android there is `android:fontFeatureSettings="liga 0"` [1][2] for the TextView, but again, might not be a good idea to apply by default. And will probably be a PITA to do selectively for some TextViews, especially if the flag is set dependent on content.

[1] <https://developer.android.com/reference/android/widget/TextView#setFontFeatureSettings(java.lang.String)>

[2] <https://stackoverflow.com/a/29444434>

### al...@alesandroortiz.com (2025-05-17)

I tested a Google Sans woff2 file loaded by google.com for mobile devices, and setting `font-variant-ligatures: no-common-ligatures` or `font-feature-settings: "liga" off` in CSS disables this ligature when rendered on a web page, but I imagine it might disable other ligatures, which may be needed.

Ideally this ligature would be labeled as a discretionary ligature so using `no-discretionary-ligatures`/`"liga" off` would work, but this isn't the case AFAICT.

Per Android docs [1], CSS 3 `font-feature-settings` values should work in Android TextViews.

Not sure if this is exactly the same font as the font used in branded Chrome. Maybe the font used by Chrome does have these ligatures classified differently.

(Fun aside: Try typing "googlelogoligature" into Google Search or Gemini from a mobile browser.)

[1] <https://developer.android.com/reference/android/widget/TextView#setFontFeatureSettings(java.lang.String)>

[2] <https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-ligatures#discretionary-lig-values>

### al...@alesandroortiz.com (2025-05-17)

Maybe using zero-width non-joiner (ZWNJ) [1] as done in a web content issue [2] would work (almost what I suggested in [#comment7](https://issues.chromium.org/issues/418214610#comment7)). Wikipedia article says it's already used in some writing systems to prevent ligatures, and seems to do the trick in a web page. Will need to test in an Android app or in Chromium.

[1] <https://en.wikipedia.org/wiki/Zero-width_non-joiner>

[2] <https://issues.chromium.org/issues/40636759#comment39>

### al...@alesandroortiz.com (2025-05-18)

For future reference, this online tool lets you view ligatures and other font info: <https://fontdrop.info/>

### an...@chromium.org (2025-05-19)

Thanks for the report and the additional comments. I am not able to setup the DNS environment myself but the video is helpful.
meacer@ sending it your way for analsyis. PTAL and re-route as necessary (not sure if this is supposed to be handled by permissions prompt folks). Thanks!

### nd...@protonmail.com (2025-05-19)

Why can't we put all security UI in comic sans?

### al...@alesandroortiz.com (2025-05-19)

I'm working on a patch to add ZWNJ if any of these ligatures are in the host string.

First attempting in `ElideUrl::HostForDisplay()` [1] which is used by many (but not all) security surfaces that need to be fixed.

Current roadblock is there isn't a ligature I can test this with, since non-branded Chromium doesn't use Google Sans and the font used doesn't have ligatures for `fi`. Looking into whether I can somehow get Google Sans working in my build, or identify another ligature I can test with the current font.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/elide_url.cc;l=127;drc=4020c78e3f11938478699ff65e29101f44e7c2a5>

### al...@alesandroortiz.com (2025-05-19)

I think the ZWNJ trick will work.

For non-branded Chromium, it will use the OS default font. (So does branded Chrome for most surfaces, except for the ones using Google Sans specifically).

Therefore, on an Android device with Roboto preinstalled (probably all?), you can switch the OS font to Roboto, and Chromium will use it. Robot has `fi` ligature, so I used that to test the ZWNJ trick. With ZWNJ between `f` and `i`, the `fi` ligature isn't rendered and there are no other visual artifacts.

Seems like it works for all the permission prompts in the PoC from this report. I assume it should also break up the Google Sans ligatures. Will update code to actually work with Google Sans ligatures and upload CL later today or tmw.

### ch...@google.com (2025-05-20)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@alesandroortiz.com (2025-05-20)

Rough patch diff (since I was working on an outdated checkout to save time, so no clean .diff file or CL yet):

1. Move existing `kUnsafeLigatures` from `components/lookalikes/core/lookalike_url_util.cc` to `lookalike_url_util.h` with updated declaration:

`inline constexpr char const* kUnsafeLigatures[] = { ... }`

2. Update `IsUnsafeLigature()` in `lookalike_url_util.cc` to add namespace to `kUnsafeLigatures` in the loop (`lookalikes::kUnsafeLigatures`).
3. Update `components/url_formatter/elide_url.cc` with attached diff.

In manual testing, this mitigates the issue in the permission prompts listed in the report.

I haven't run automated tests against this diff, but will do so once I have updated checkout later today. Will upload CL within a day assuming existing tests pass.

Also need to test behavior with RTL, will do so soon as well.

### al...@alesandroortiz.com (2025-05-20)

Not sure if we want to guard the ZWNJ injection logic to only Android. I haven't tested iOS (don't have device), not sure if spoof (or fix) works there too. I think ChromeOS uses Google Sans in some places, but still need to check whether any ligature spoofs work in ChromeOS.

### al...@alesandroortiz.com (2025-05-20)

Hm, the ZWNJ approach has some downsides. Some UIs seem to pass the host again through some IDN logic (probably `IDNSpoofChecker::SafeToDisplayAsUnicode()` [1]), so sometimes the host with ZWNJ is displayed as punycode. It's a bit inconsistent even within the same feature, such as Site settings. This is the same behavior I observed with the address bar when I manually added the ZWNJ character using my keyboard. Not sure if best approach is to make all of this consistent and not display punycode if the only issue is ZWNJ in host.

Seems like in Unicode 15, ZWNJ was changed to restricted character per comment in `IDNSpoofChecker::SetAllowedUnicodeSet()` [2].

If there's a good reason to keep ZWNJ as restricted character, then either code cleanup of exisiting call sites to avoid calling or another approach will be needed.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/spoof_checks/idn_spoof_checker.cc;l=363;drc=2a62f53052a6c2575a102c60fa341e6bf6966cc1>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/spoof_checks/idn_spoof_checker.cc;l=724;drc=2a62f53052a6c2575a102c60fa341e6bf6966cc1>

### al...@alesandroortiz.com (2025-05-21)

Among other things, based on code analysis and some testing, the ligature spoof also likely affects these other UIs (assuming they use Google Sans font) and are likely fixed by the ZWNJ patch.

I've only verified some of these. There's also two other UIs (that are mostly but not fully fixed with the proposed ZWNJ patch above): [issue 418273622](https://issues.chromium.org/issues/418273622), [issue 418214612](https://issues.chromium.org/issues/418214612)

- Bookmarks (verified)
- Most if not all the autofill/password UIs (verified)
- Payment request address bar display (verified)
- PEPC (since it's same as regular permission prompt) (verified)
- HID chooser (IIRC)
- Serial device chooser (IIRC)
- Some other Bluetooth dialogs (such as scanner dialog)
- Secure payment confirmation
- Digital credentials
- PWA install prompts
- SMS fetcher

### al...@alesandroortiz.com (2025-05-21)

Another potential patch we can consider:

Block subframe navs (for [issue 418214612](https://issues.chromium.org/issues/418214612) scenario) and show interstitial based on origin, not URL in case an iframe is somehow able to open a top-level page with that origin but on about:blank or another not-blocked URL.

Or allow subframe navs, mitigate [issue 418214612](https://issues.chromium.org/issues/418214612) with targeted fix, and show interstitial based on origin for top-level pages with blank URLs.

Right now, the ZWNJ patch in `url_formatter/elide_url.cc` feels a bit risky given the widespread use and inconsistent post-processing we would likely need to fix.

### al...@alesandroortiz.com (2025-05-21)

Or, ship a version of the font for use in surfaces with untrusted input that doesn't have the spoofy ligatures. But that's something only Google can do.

### nd...@protonmail.com (2025-05-21)

I think having a font that's not creating extra spoofing vulnerabilities for Google services would be good. That's why I tried to convince them to move away from that design it's not really worth it.

### al...@alesandroortiz.com (2025-05-22)

Surprisingly, the first CL <https://crrev.com/c/6575322> had tests pass locally and in tryjobs, but that probably means test coverage is not catching the cases I was able to manually observe.

I uploaded a 2nd CL <https://crrev.com/c/6576707> to include embedded frames in lookalike throttle, since this seems less risky even if it doesn't tackle all the UIs. The remaining UIs can be fixed with targeted CLs.

I'll upload screenshots/videos of before/after throttle CL in the morning, along with details of remaining areas that require separate CLs.

### al...@alesandroortiz.com (2025-05-22)

For <https://crrev.com/c/6576707>:

Before: See video in [original report](#b418214610-c26-comment1).

After: See attached screenshots of frame blocked and console warning in DevTools. Frame error message is shown when frame is tapped, like with other frame error messages.

### ch...@google.com (2025-06-03)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### al...@alesandroortiz.com (2025-06-03)

I've been working on the CLs. <https://crrev.com/c/6576707> and <https://crrev.com/c/6608319> are pending review.

### al...@alesandroortiz.com (2025-06-11)

From meacer@ in <https://chromium-review.googlesource.com/c/chromium/src/+/6576707/comments/66285099_0f78df5b>

> Given the number of ligature related issues we have, at this point my preference would be for a fix that disables ligature rendering altogether in the UI. Android team said that that's possible. I started looking into the implementation, but haven't made much progress yet.

My comment:

> Thanks for the update. I did some digging on disabling Android ligatures in [#comment7](https://issues.chromium.org/issues/418214610#comment7) and subsequent comments, but it would also affect other ligatures, which may not be desirable.
> 
> Using a variant of the Google Sans font without the spoofy ligatures may work too, as I mentioned in another crbug comment.

### ch...@google.com (2025-06-18)

meacer: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2025-06-20)

Latest update on my end is that I'm talking to the Android and the fonts team about the possibility of disabling ligatures and contextual alternatives. As alesandro@ noted, we don't want to blanket disable ligatures so I'm trying to find a way to do it selectively (either disabling per-UI or by disabling the offending ligatures).

### ch...@google.com (2025-07-03)

meacer: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-18)

meacer: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-02)

meacer: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-17)

meacer: Uh oh! This issue still open and hasn't been updated in the last 89 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### nd...@protonmail.com (2025-08-17)

Bot I agree this should be fixed lets team up and start a riot.

### ch...@google.com (2025-09-01)

meacer: Uh oh! This issue still open and hasn't been updated in the last 104 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### nd...@protonmail.com (2025-09-02)

Bot you need to work on making your reply's less generic, developers will see that and go ah its the nag again like be convincing what's the harm to end users maybe even go a step further with a sob story about how this font issue resulted in you having a bad day.

### ch...@google.com (2025-09-16)

meacer: Uh oh! This issue still open and hasn't been updated in the last 119 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-01)

meacer: Uh oh! This issue still open and hasn't been updated in the last 134 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-16)

meacer: Uh oh! This issue still open and hasn't been updated in the last 149 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-31)

meacer: Uh oh! This issue still open and hasn't been updated in the last 164 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-15)

meacer: Uh oh! This issue still open and hasn't been updated in the last 179 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-30)

meacer: Uh oh! This issue still open and hasn't been updated in the last 194 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-15)

meacer: Uh oh! This issue still open and hasn't been updated in the last 209 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-30)

meacer: Uh oh! This issue still open and hasn't been updated in the last 224 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-14)

meacer: Uh oh! This issue still open and hasn't been updated in the last 239 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-29)

meacer: Uh oh! This issue still open and hasn't been updated in the last 254 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2026-02-02)

+sinansahin for visibility

### dx...@google.com (2026-02-02)

Project: chromium/src  

Branch:  main  

Author:  Mustafa Emre Acer [meacer@chromium.org](mailto:meacer@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7536052>

Disable ligatures in permission dialogs on Android

---


Expand for full commit details
```
     
    This change disables rendering of ligatures in permission dialogs 
    for security and readability. A similar change was previously made 
    for the omnibox in crrev.com/c/7199504. 
     
    Bug: 418214610 
    Change-Id: I4f0e61d87ea50304ef0909f939908393a81d9e78 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7536052 
    Reviewed-by: Sinan Sahin <sinansahin@google.com> 
    Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
    Reviewed-by: Elias Klim <elklm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1578393}

```

---

Files:

- M `components/permissions/android/java/src/org/chromium/components/permissions/PermissionDialogCoordinator.java`
- M `ui/android/java/src/org/chromium/ui/UiUtils.java`

---

Hash: [19ca206a62d08ed290bcda7f5974b1cdb6a765c1](https://chromiumdash.appspot.com/commit/19ca206a62d08ed290bcda7f5974b1cdb6a765c1)  

Date: Mon Feb 2 22:19:58 2026


---

### ch...@google.com (2026-02-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-02-03)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### me...@google.com (2026-02-03)

Third time is the charm.

### nd...@protonmail.com (2026-02-03)

🎉

### ch...@google.com (2026-02-11)

Security Merge Request Consideration: Not requesting merge to dev (M146) because latest trunk commit (1578393) appears to be prior to dev branch point (1582197). If this is incorrect please remove NA-146 from the 'Merge' field and add 146 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2026-02-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High Quality & High Impact UI spoof find


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### nd...@protonmail.com (2026-02-20)

Nice I wish VRP allowed for splitting rewards :)

### al...@alesandroortiz.com (2026-02-20)

Thanks for reward! On my end I'll split 80% with NDevTK, please make sure that 80% also goes towards them in the rankings. For reporter credit to use, see report ([#comment1](https://issues.chromium.org/issues/418214610#comment1)).

### ch...@google.com (2026-05-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/418214610)*
