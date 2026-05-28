# Security: ASCII can be autodetected as ISO-2022-JP

| Field | Value |
|-------|-------|
| **Issue ID** | [40089450](https://issues.chromium.org/issues/40089450) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Loader, Blink>TextEncoding |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hs...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2017-10-31 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

All-ASCII HTML can get autodetected as ISO-2022-JP, which makes ASCII content that doesn't look like markup treated as active content. This may lead to XSS if the site serves user-supplied content.

As a mitigating factor, to be vulnerable a site has to violate two best practices:
 1) The site needs not to declare its character encoding. (Pretty realistic, unfortunately.)
 2) Instead of escaping all less-than signs in user-supplied content as would be proper, the site needs to try to filter out markup specifically. (The proof of concept includes an ASCII less-than sign byte followed by a non-alphabetic byte, so there's a chance there are filter out there that wouldn't consider it as matching a regexp for an HTML tag.)

However, from the work I've seen Mike West do, I have inferred that Chrome considers these kinds of site mistakes to be in scope for browser-based counter-measures.

As a remedy, I suggest excluding ISO-2022-JP from potential autodetection outcomes.

VERSION
Google Chrome	62.0.3202.75 (Official Build) (64-bit)
Revision	67b212ffb03c4401235f8961e2d15371b96cde27-refs/branch-heads/3202@{#750}
OS	Ubuntu 16.04

REPRODUCTION CASE
Load https://hsivonen.com/test/p/iso-2022-jp-autodetect.htm in Chrome.

ADDITIONAL INFO
For bug unhiding, coordination with unhiding https://bugzilla.mozilla.org/show_bug.cgi?id=1362365 would be appreciated.

## Timeline

### hs...@gmail.com (2017-10-31)

I'd CC Jinsuk Kim but the CC UI isn't available to me.

### el...@chromium.org (2017-10-31)

Yes, failing to declare the character set is a critical mistake in the web application.

While removing character sets from those that are auto-detectable does reduce attack surface, doing so tends to have a compatibility impact.

We do not usually track issues like this as Security Vulnerabilities, but it looks like the Mozilla bug is view-restricted so we may not want to open this one up just yet.

[Monorail components: Blink>Loader Blink>TextEncoding]

### el...@chromium.org (2017-10-31)

Notably, the first byte of the document's title is 0x1B (the ESCAPE control character) and removing it seems to break the repro.

Is there a repro of this issue that only uses the printable set of ASCII?

### el...@chromium.org (2017-10-31)

The proposed mitigation (not sniffing ISO-2022-JP) appears to be under discussion in https://crbug.com/chromium/691985. See https://crbug.com/chromium/780024#c6 and later.

### hs...@gmail.com (2017-10-31)

> Is there a repro of this issue that only uses the printable set of ASCII?

No. (ISO-2022-JP always uses the same byte range as ASCII, and two byte streams that do not contain the ESCAPE byte decode the same as ASCII and ISO-2022-JP.)

### pa...@chromium.org (2017-10-31)

Fundamentally I'd say the vulnerability lies on the server side, and it's probably mostly a quirk on the browser side (and as such, this bug is probably really a duplicate of 691985).

However, let's keep it as a separate bug, and with view restrictions at least temporarily, since Mozilla currently seems to regard it as needing that. But we should tend toward simply duping it into 691985 and removing the view restrictions, I think.

### hs...@gmail.com (2017-11-01)

This really is a data point for the discussion in https://crbug.com/chromium/691985, but I didn't want to add the PoC to a public bug. Sorry about failing to mention https://crbug.com/chromium/691985 when filing.

Mozilla's security team rated the corresponding Firefox bug as "moderate" in the taxonomy given at https://wiki.mozilla.org/Security_Severity_Ratings . (In Firefox, ISO-2022-JP autodetection is enabled by default only for the Japanese locale, but user can enable Japanese autodetection in any localization of Firefox or be enticed to choose ISO-2022-JP from the override menu, which Firefox still has.)

The reason we haven't landed a fix (removal of ISO-2022-JP from the menu and from possible Japanese autodetection outcomes) in Firefox is that we're interested in Chrome's take (but I was too busy to tweak the PoC to apply to Chrome right away, hence the delay in filing here).

To be clear, this totally involves a failure on the part of the site to do things properly. However, as noted in the initial report, I've seen Mike West pursue various Chrome-side mitigations for problems that, fundamentally, are site mistakes, which is why I thought Chrome might treat this one, too, as being in scope for mitigation.

### hs...@gmail.com (2017-11-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-11-01)

As an Attack Surface Reduction, this is Severity-Low.

### mk...@chromium.org (2017-11-02)

I agree that if we can get away with turning off autodetection for ISO-2022-JP, then we should. We'd need to add some metrics to determine how often this happens in the wild, and evaluate the breakage, if any, in the same way we deal with other deprecations.

Does Mozilla have that kind of data already?

### hs...@gmail.com (2017-11-02)

We don't have telemetry data for how often autodetection detects ISO-2022-JP or how often users choose ISO-2022-JP from the menu.

In Firefox 55 release from August 3 to August 24 (we stopped collecting this information in 56), the ISO-2022-JP decoder was instantiated at least once (for any reason, including content that's labeled as ISO-2022-JP) in 0.01% of Firefox sessions (browser start to quit) globally (we have restrictions on filtering the data by locale, so I don't have data scoped to the ja-JP locale at hand).

In other words, 99.99% of Firefox sessions didn't see any ISO-2022-JP content at all.

During the same period the character encoding menu was used (for any selection from the menu, not just for selecting ISO-2022-JP) at least once in 0.002% of Firefox sessions globally.

In other words, 99.998% of Firefox sessions didn't see encoding menu usage at all.

So it's safe to conclude that the user choosing ISO-2022-JP from the menu is extremely rare. However, we don't have data on how the ISO-2022-JP encounters are split between labeled resources (unaffected by the proposed change) and autodetection (which in Firefox is enabled by default only for the ja-JP localization).

Apart from telemetry, I think it's relevant that IE11 doesn't have ISO-2022-JP in its encoding menu and, AFAICT, the Japanese autodetector in IE11 doesn't detect ISO-2022-JP. (Tested with ISO-2022-JP content that exercised only the JIS X 0208 state and not the Roman state that the XSS PoC relies on. Also, as a control, I checked that IE11's Japanese detector detected EUC-JP.)

That is, it looks like Microsoft, despite being very serious about compatibility, has already made the proposed change. (Edge doesn't have an encoding menu and, so far, I have seen no evidence of it having any encoding detector, either.)

Using an EUC-JP control case, I have been unable to work out the circumstances in which Safari's Japanese detector activates, so I can't say if it would detect ISO-2022-JP.

### mk...@chromium.org (2017-11-02)

That sounds compelling to me.

jinsukkim@, would you be willing to drive an "Intent to Deprecate and Remove" thread on blink-dev@ (and the implementation :) ). I'd LGTM it, based on this data, Firefox's willingness, and Edge's behavior.

### ji...@chromium.org (2017-11-09)

+kenjibaheux, tkent

Invited more people who I believe are more familiar/knowledgeable on the encoding up for discussion here. To the best of my knowledge, most ISO-2022-JP pages are static ones, come from legacy websites that stopped maintenance, while modern web sites in Japanese all switched to UTF-8. I think that's another fact to be taken into account when debating stopping autodetection support for it. I'd like to hear more before taking on it.

### ke...@chromium.org (2017-11-13)

Visits to iso-2022-jp pages should be very rare. As jinsukkim mentioned, these pages tend to be very old websites that are not maintained anymore.

If the majority of browser vendors agree that autodetecting iso-2022-jp pages isn't worth the trouble, then it makes sense for us to do the same. So, +1 to at least start an intent to deprecate and remove. Ideally, a metrics would be useful in case of loud opposition/complaints either on the thread or after the change makes it to stable.

### ji...@chromium.org (2017-11-13)

See https://bugs.chromium.org/p/chromium/issues/detail?id=691985#c30 for (conflicting) test results on other browsers:

> I checked other browser behavior:
>
> IE11: Auto-detect ISO-2022-JP by default
> Edge: Auto-detect ISO-2022-JP by default if Windows language is Japanese
> Firefox: Auto-detect ISO-2022-JP if Auto-detect>Japanese is enabled.
> Safari: Auto-detect ISO-2022-JP if HTTP header or meta charset is one of Shift_JIS, EUC-JP, ISO-2022-JP.  The code looks to auto-detect ISO-2022-JP in other cases, but I couldn't confirm the behavior.



### ke...@chromium.org (2017-11-13)

Thanks jinsukkim. If these behaviors are unchanged then we should do an intent to deprecate, land the right metrics, and make a call on "remove" based on the metrics + intent/opinion from other vendors.

### ji...@chromium.org (2018-02-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ke...@chromium.org (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/780024?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, Blink>TextEncoding]
[Monorail mergedwith: crbug.com/chromium/647582]
[Monorail components added to Component Tags custom field.]

### ma...@google.com (2024-04-17)

[Security shepherd]

Resuscitating this dormant security bug, since we just received another report in [issue 334977818](https://issues.chromium.org/issues/334977818). (Please ping me if you would like access to that issue.)

The original report here in [comment#1](https://issues.chromium.org/issues/40089450#comment1) states as a mitigating factor that

> Instead of escaping all less-than signs in user-supplied content as would be proper, the site needs to try to filter out markup specifically`

The new report points out that if the victim website transforms user-generated markdown into HTML, you can get around this restriction.

From reading through the comments here, it sounds like the consensus was that Chromium should do an Intent to Deprecate and Remove for ISO-2022-JP auto-detection. Is that still the preferred way forward? Is there someone who could drive that?

### ma...@google.com (2024-04-18)

kouhei@ is currently working on finding an owner for this.

Also please note that the reporter of [issue 334977818](https://issues.chromium.org/issues/334977818) is planning to disclose their findings after 90 days (i.e. July 15, 2024).

### hs...@gmail.com (2024-07-19)

There's now https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/ . AFAICT, the main differences compared to autodetecting Big5, gbk, or Shift_JIS, which, realistically, are going to continue to get detected, is how few bytes are required to convince a detector that the input is ISO-2022-JP and then masking a backslash does not require a non-ASCII byte before the backslash.

### jk...@google.com (2025-01-15)

I've added a use counter for ISO-2022-JP auto detection of HTML and XML. We'll see usage once M134 lands.
<https://crrev.com/c/6155577>

### jk...@google.com (2025-03-18)

Auto-detection of ISO-2022-JP occurs around 0.000002% of page loads. I think we can remove it.
<https://chromestatus.com/metrics/feature/timeline/popularity/5244>

### jk...@google.com (2025-03-24)

WIP CL at <https://crrev.com/c/6378605>.
This will land once Intent to Deprecate email goes out and gets approved.

### am...@chromium.org (2025-03-26)

please note, this is not fixed but I am temporarily setting as fixed to trick our automation

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of exploitation mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Hello -- thank you for this report from back in 2017. 
We are going through some of our oldest reports classified as low severity security bugs. In reviewing this issue, we still concur that there is security impact here and are pleased to see this one getting some active traction and on it's way to resolution. 
Despite that it's not fully resolved, we're going to go ahead and open this issue for public disclosure as it seems prudent so that sites that might be affected can add the appropriate character encoding tag / can take action to mitigate impact here. 

Also, given the age and impact of this bug, we felt it appropriate to go ahead and evaluate for a reward at this time. 
Thank you for your past efforts and reporting this issue to us as well as your patience for it to be resolved. 


### gj...@google.com (2025-04-07)

[Loading bug triage]

@jk...@google.com It has been some time since the last update of the WIP CL. Is the team still actively working on it?

### jk...@google.com (2025-04-07)

I'm blocked by the [Debuggability review](https://chromestatus.com/feature/6576566521561088?gate=6494044362113024). No response for 2 weeks even though I pinged in the comment a few times.

### dx...@google.com (2025-04-18)

Project: chromium/src  

Branch: main  

Author: Jun Kokatsu [jkokatsu@google.com](mailto:jkokatsu@google.com)  

Link:      <https://chromium-review.googlesource.com/6469534>

Add deprecation warning for ISO-2022-JP auto-detection

---


Expand for full commit details
```
     
    Add deprecation warning in Devtool for auto-detection of ISO-2022-JP 
    charset. 
     
    Bug: 40089450 
    Change-Id: I81c17e47edb9e46272e2cf83589fc232ceafaf12 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6469534 
    Reviewed-by: Ari Chivukula <arichiv@chromium.org> 
    Auto-Submit: Jun Kokatsu <jkokatsu@google.com> 
    Reviewed-by: David Baron <dbaron@chromium.org> 
    Commit-Queue: David Baron <dbaron@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1448881}

```

---

Files:

- M `third_party/blink/renderer/core/dom/decoded_data_document_parser.cc`
- M `third_party/blink/renderer/core/frame/deprecation/deprecation.json5`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/issues/iso-2022-jp-auto-detection-expected.txt`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/issues/iso-2022-jp-auto-detection.js`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/resources/iso_2022_jp.html`

---

Hash: 0dd1c5ff57ca550269c61455b9a3385289c033bc  

Date:  Fri Apr 18 15:50:58 2025


---

### jk...@google.com (2025-05-05)

Added deprecation warning in M137. I plan to ship the deprecation on M139.

### dx...@google.com (2025-06-18)

Project: chromium/src  

Branch: main  

Author: Jun Kokatsu [jkokatsu@google.com](mailto:jkokatsu@google.com)  

Link:      <https://chromium-review.googlesource.com/6378605>

Disable auto-detection of ISO-2022-JP charset

---


Expand for full commit details
```
     
    Per approval in the intent to ship thread[1], this CL removes support 
    for auto-detection of ISO-2022-JP charset in HTML. 
     
    Timelines: 
    - Warning messages added in [2], in M137. 
    - Flag added and disabled, now, in M139. 
    - Flag and code can be removed in M141 or so, once there are no problems 
    when M139 goes to stable. 
     
    [1]: 
    https://groups.google.com/a/chromium.org/g/blink-dev/c/yIgrr5YNGJ4/m/jKvlEerFCAAJ 
    [2]: 
    https://chromiumdash.appspot.com/commit/0dd1c5ff57ca550269c61455b9a3385289c033bc 
     
    Bug: 40089450 
    Change-Id: Id3bd642da8c630188775276909e6e2bffbad174c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6378605 
    Auto-Submit: Jun Kokatsu <jkokatsu@google.com> 
    Reviewed-by: Mason Freed <masonf@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Mason Freed <masonf@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1475633}

```

---

Files:

- M `chrome/browser/chrome_web_platform_security_metrics_browsertest.cc`
- M `third_party/blink/renderer/core/dom/decoded_data_document_parser.cc`
- M `third_party/blink/renderer/core/frame/deprecation/deprecation.json5`
- M `third_party/blink/renderer/core/html/parser/text_resource_decoder.cc`
- M `third_party/blink/renderer/core/html/parser/text_resource_decoder_test.cc`
- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`
- A `third_party/blink/web_tests/external/wpt/encoding-detection/ja-ISO-2022-JP-late.tentative-expected.txt`
- A `third_party/blink/web_tests/external/wpt/encoding-detection/ja-ISO-2022-JP.tentative-expected.txt`
- D `third_party/blink/web_tests/http/tests/inspector-protocol/issues/iso-2022-jp-auto-detection-expected.txt`
- D `third_party/blink/web_tests/http/tests/inspector-protocol/issues/iso-2022-jp-auto-detection.js`
- D `third_party/blink/web_tests/http/tests/inspector-protocol/resources/iso_2022_jp.html`

---

Hash: a2d76e87da6b467dfcc11e84327e7c00f0a1b5a7  

Date:  Wed Jun 18 16:06:21 2025


---

### pg...@google.com (2025-08-05)

This was filed a very long while ago, but we are here (: @reporter! How would you like to be credited for this report?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089450)*
