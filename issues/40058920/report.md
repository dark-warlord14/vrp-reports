# Security: bypass resource requests whose URLs contained both removed whitespace (`\n`, `\r`, `\t`) characters and less-than characters (`<`) in the fencedframe element

| Field | Value |
|-------|-------|
| **Issue ID** | [40058920](https://issues.chromium.org/issues/40058920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>FencedFrames |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2022-02-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Security: bypass resource requests whose URLs contained both removed whitespace (`\n`, `\r`, `\t`) characters and less-than characters (`<`) in the fencedframe element  

Add url.PotentiallyDanglingMarkup() in the fencedframe src property

similar to <https://crbug.com/chromium/1039885>

**VERSION**  

Chrome Version: version 100.0.4896.12 (Official Build) dev (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

```
<fencedframe width="200" height="100"  src="ht  
tps://test.com/y<ay?fencedframe" />  

```

chrome.exe --enable-features=FencedFrames <http://localhost/poc.html>

Add response header("Supports-Loading-Mode", "fenced-frame") in the webserver to make the fencedframe feature avalible.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 182 B)

## Timeline

### [Deleted User] (2022-02-28)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-02)

Medium because while this isn't harmful by itself, it is potentially harmful when combined with other bugs (e.g. bugs in the site itself).

I believe this is disabled by default (including in M98), so there should be no security impact from this. However, I've marked this as blocking some other launches until this is resolved.

[Monorail components: Blink>FencedFrames]

### do...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-18)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-09)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-19)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-30)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-06-09)

Security marshal here. I'm seeing that in the past few months, there has been progress on the launch bug (1208744). dom@, can you confirm whether the feature is still disabled by default as mentioned in https://crbug.com/chromium/1301333#c2?

### do...@chromium.org (2022-06-12)

I'll be taking a closer look at this this week

### do...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fe04c0639254e5d021da539d321f2e3a64a0085c

commit fe04c0639254e5d021da539d321f2e3a64a0085c
Author: Dominic Farolino <dom@chromium.org>
Date: Thu Jun 16 15:54:39 2022

Fenced frames: Disallow URLs with potentially dangling markup

There is an old Fetch Standard PR up for review that blocks resource
requests whose URL contains potentially dangling markup [1]. This is
for security purposes, see [2] and [3]. While non-standard yet, Chromium
has shipped this behavior, and we intend to do the same for fenced
frames. This CL implements potentially dangling markup
restrictions on all embedder-provided URLs for fenced frame
navigations.

When a URL with dangling markup is passed to SharedStorage's `selectURL()` method, it is parsed and partially sanitized, therefore the resulting urn:uuid can be successfully navigated to. When crbug.com/1318970 is fixed, SharedStorage will reject these URLs as inputs.

[1]: https://github.com/whatwg/fetch/pull/519
[2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1039885
[3]: https://bugs.chromium.org/p/chromium/issues/detail?id=1301333

Bug: 1301333, 1318970
Change-Id: I1ada9de23b05795499408988529fa3a49486aea3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3702854
Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Dominic Farolino <dom@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1014928}

[add] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html.headers
[modify] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/third_party/blink/common/fenced_frame/fenced_frame_utils.cc
[add] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html
[modify] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/third_party/blink/web_tests/wpt_internal/fenced_frame/disallowed-navigations.https.html
[add] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-mparch/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/fe04c0639254e5d021da539d321f2e3a64a0085c/content/browser/security_exploit_browsertest.cc


### do...@chromium.org (2022-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/245696bb639221c56332cdea83bd961c99330183

commit 245696bb639221c56332cdea83bd961c99330183
Author: Łukasz Anforowicz <lukasza@chromium.org>
Date: Thu Jun 16 18:35:13 2022

Revert "Fenced frames: Disallow URLs with potentially dangling markup"

This reverts commit fe04c0639254e5d021da539d321f2e3a64a0085c.

Reason for revert: Suspecting that this CL caused https://crbug.com/1337025

Original change's description:
> Fenced frames: Disallow URLs with potentially dangling markup
>
> There is an old Fetch Standard PR up for review that blocks resource
> requests whose URL contains potentially dangling markup [1]. This is
> for security purposes, see [2] and [3]. While non-standard yet, Chromium
> has shipped this behavior, and we intend to do the same for fenced
> frames. This CL implements potentially dangling markup
> restrictions on all embedder-provided URLs for fenced frame
> navigations.
>
> When a URL with dangling markup is passed to SharedStorage's `selectURL()` method, it is parsed and partially sanitized, therefore the resulting urn:uuid can be successfully navigated to. When crbug.com/1318970 is fixed, SharedStorage will reject these URLs as inputs.
>
> [1]: https://github.com/whatwg/fetch/pull/519
> [2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1039885
> [3]: https://bugs.chromium.org/p/chromium/issues/detail?id=1301333
>
> Bug: 1301333, 1318970
> Change-Id: I1ada9de23b05795499408988529fa3a49486aea3
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3702854
> Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Dominic Farolino <dom@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1014928}

Bug: 1301333, 1318970
Change-Id: If4884825408c38882f439d8c5e47ba0271dc67a1
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3710059
Owners-Override: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Sebastien Lalancette <seblalancette@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Sebastien Lalancette <seblalancette@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1015011}

[delete] https://crrev.com/30d76481ae680605dab7c99d9b2e2fa77d4f921e/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html.headers
[modify] https://crrev.com/245696bb639221c56332cdea83bd961c99330183/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/245696bb639221c56332cdea83bd961c99330183/third_party/blink/common/fenced_frame/fenced_frame_utils.cc
[delete] https://crrev.com/30d76481ae680605dab7c99d9b2e2fa77d4f921e/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html
[modify] https://crrev.com/245696bb639221c56332cdea83bd961c99330183/third_party/blink/web_tests/wpt_internal/fenced_frame/disallowed-navigations.https.html
[delete] https://crrev.com/30d76481ae680605dab7c99d9b2e2fa77d4f921e/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-mparch/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/245696bb639221c56332cdea83bd961c99330183/content/browser/security_exploit_browsertest.cc


### th...@chromium.org (2022-06-21)

Reopening because the CL got reverted -- dom@ to close with an explanation if reopening was in error.

### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d168b7e00bbbca61bcdb6078694b3500f74863d5

commit d168b7e00bbbca61bcdb6078694b3500f74863d5
Author: Dominic Farolino <dom@chromium.org>
Date: Tue Jun 28 23:11:02 2022

Reland "Fenced frames: Disallow URLs with potentially dangling markup"

This is a reland of commit fe04c0639254e5d021da539d321f2e3a64a0085c

Original change's description:
> Fenced frames: Disallow URLs with potentially dangling markup
>
> There is an old Fetch Standard PR up for review that blocks resource
> requests whose URL contains potentially dangling markup [1]. This is
> for security purposes, see [2] and [3]. While non-standard yet, Chromium
> has shipped this behavior, and we intend to do the same for fenced
> frames. This CL implements potentially dangling markup
> restrictions on all embedder-provided URLs for fenced frame
> navigations.
>
> When a URL with dangling markup is passed to SharedStorage's `selectURL()` method, it is parsed and partially sanitized, therefore the resulting urn:uuid can be successfully navigated to. When crbug.com/1318970 is fixed, SharedStorage will reject these URLs as inputs.
>
> [1]: https://github.com/whatwg/fetch/pull/519
> [2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1039885
> [3]: https://bugs.chromium.org/p/chromium/issues/detail?id=1301333
>
> Bug: 1301333, 1318970
> Change-Id: I1ada9de23b05795499408988529fa3a49486aea3
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3702854
> Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Commit-Queue: Dominic Farolino <dom@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1014928}

Bug: 1301333, 1318970, 1337025
Change-Id: I28fb3ed240344b795ceef8c3a65459f16b688524
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715554
Commit-Queue: Dominic Farolino <dom@chromium.org>
Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1018831}

[add] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html.headers
[modify] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/third_party/blink/common/fenced_frame/fenced_frame_utils.cc
[add] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html
[modify] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/third_party/blink/web_tests/wpt_internal/fenced_frame/disallowed-navigations.https.html
[add] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-mparch/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/d168b7e00bbbca61bcdb6078694b3500f74863d5/content/browser/security_exploit_browsertest.cc


### do...@chromium.org (2022-06-29)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-06-29)

Keeps getting reverted due to flakiness errors despite that not being reproducible locally... I am not sure when I'll be able to get to this.

### gi...@appspot.gserviceaccount.com (2022-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/249ad02da9846203ef3357bbc82c5145384b31b0

commit 249ad02da9846203ef3357bbc82c5145384b31b0
Author: Huanpo Lin <robertlin@chromium.org>
Date: Wed Jun 29 02:29:41 2022

Revert "Reland "Fenced frames: Disallow URLs with potentially dangling markup""

This reverts commit d168b7e00bbbca61bcdb6078694b3500f74863d5.

Reason for revert:
Witness the following tests in constant failure list (mac/linux) when sheriffing, and this CL is in the list of potential regression culprit.
virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/disallowed-navigations.https.html
virtual/fenced-frame-mparch/wpt_internal/fenced_frame/disallowed-navigations.https.html

Original change's description:
> Reland "Fenced frames: Disallow URLs with potentially dangling markup"
>
> This is a reland of commit fe04c0639254e5d021da539d321f2e3a64a0085c
>
> Original change's description:
> > Fenced frames: Disallow URLs with potentially dangling markup
> >
> > There is an old Fetch Standard PR up for review that blocks resource
> > requests whose URL contains potentially dangling markup [1]. This is
> > for security purposes, see [2] and [3]. While non-standard yet, Chromium
> > has shipped this behavior, and we intend to do the same for fenced
> > frames. This CL implements potentially dangling markup
> > restrictions on all embedder-provided URLs for fenced frame
> > navigations.
> >
> > When a URL with dangling markup is passed to SharedStorage's `selectURL()` method, it is parsed and partially sanitized, therefore the resulting urn:uuid can be successfully navigated to. When crbug.com/1318970 is fixed, SharedStorage will reject these URLs as inputs.
> >
> > [1]: https://github.com/whatwg/fetch/pull/519
> > [2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1039885
> > [3]: https://bugs.chromium.org/p/chromium/issues/detail?id=1301333
> >
> > Bug: 1301333, 1318970
> > Change-Id: I1ada9de23b05795499408988529fa3a49486aea3
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3702854
> > Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
> > Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> > Commit-Queue: Dominic Farolino <dom@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1014928}
>
> Bug: 1301333, 1318970, 1337025
> Change-Id: I28fb3ed240344b795ceef8c3a65459f16b688524
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715554
> Commit-Queue: Dominic Farolino <dom@chromium.org>
> Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1018831}

Bug: 1301333, 1318970, 1337025
Change-Id: I08c09fc7d7d35ccd5a826ce3d7f03e954a860bc0
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3734127
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Huanpo Lin <robertlin@chromium.org>
Owners-Override: Robert Lin <robertlin@google.com>
Cr-Commit-Position: refs/heads/main@{#1018955}

[delete] https://crrev.com/28591de4aedd13a3e4279ba4b5b1dea3a25b9f32/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html.headers
[modify] https://crrev.com/249ad02da9846203ef3357bbc82c5145384b31b0/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/249ad02da9846203ef3357bbc82c5145384b31b0/third_party/blink/common/fenced_frame/fenced_frame_utils.cc
[delete] https://crrev.com/28591de4aedd13a3e4279ba4b5b1dea3a25b9f32/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html
[modify] https://crrev.com/249ad02da9846203ef3357bbc82c5145384b31b0/third_party/blink/web_tests/wpt_internal/fenced_frame/disallowed-navigations.https.html
[delete] https://crrev.com/28591de4aedd13a3e4279ba4b5b1dea3a25b9f32/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-mparch/wpt_internal/fenced_frame/disallowed-navigations.https-expected.txt
[modify] https://crrev.com/249ad02da9846203ef3357bbc82c5145384b31b0/content/browser/security_exploit_browsertest.cc


### [Deleted User] (2022-08-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-08-01)

I've had a re-land up at crrev.com/c/3781483, but it is failing *only* the bfcache bot for an unknown reason. I'll try and figure out. I have a hunch that just splitting up the test into multiple files might fix it, which would be werid.

### gi...@appspot.gserviceaccount.com (2022-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd8569850d538adc8e3012da1c7c8573f16a5356

commit fd8569850d538adc8e3012da1c7c8573f16a5356
Author: Dominic Farolino <dom@chromium.org>
Date: Wed Aug 24 22:26:25 2022

Reland "Reland "Fenced frames: Disallow URLs with potentially dangling markup""

This is a reland of commit d168b7e00bbbca61bcdb6078694b3500f74863d5

Original change's description:
> Reland "Fenced frames: Disallow URLs with potentially dangling markup"
>
> This is a reland of commit fe04c0639254e5d021da539d321f2e3a64a0085c
>
> Original change's description:
> > Fenced frames: Disallow URLs with potentially dangling markup
> >
> > There is an old Fetch Standard PR up for review that blocks resource
> > requests whose URL contains potentially dangling markup [1]. This is
> > for security purposes, see [2] and [3]. While non-standard yet, Chromium
> > has shipped this behavior, and we intend to do the same for fenced
> > frames. This CL implements potentially dangling markup
> > restrictions on all embedder-provided URLs for fenced frame
> > navigations.
> >
> > When a URL with dangling markup is passed to SharedStorage's `selectURL()` method, it is parsed and partially sanitized, therefore the resulting urn:uuid can be successfully navigated to. When crbug.com/1318970 is fixed, SharedStorage will reject these URLs as inputs.
> >
> > [1]: https://github.com/whatwg/fetch/pull/519
> > [2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1039885
> > [3]: https://bugs.chromium.org/p/chromium/issues/detail?id=1301333
> >
> > Bug: 1301333, 1318970
> > Change-Id: I1ada9de23b05795499408988529fa3a49486aea3
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3702854
> > Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
> > Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> > Commit-Queue: Dominic Farolino <dom@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1014928}
>
> Bug: 1301333, 1318970, 1337025
> Change-Id: I28fb3ed240344b795ceef8c3a65459f16b688524
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3715554
> Commit-Queue: Dominic Farolino <dom@chromium.org>
> Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1018831}

Bug: 1301333, 1318970, 1337025
Change-Id: I12c002d7f42d7138a9ad07eaa3b25b6c5b3d5d36
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3781483
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Dominic Farolino <dom@chromium.org>
Reviewed-by: Garrett Tanzer <gtanzer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1038987}

[add] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/third_party/blink/web_tests/wpt_internal/fenced_frame/disallowed-navigations-dangling-markup.https.html
[add] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html.headers
[modify] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/third_party/blink/common/fenced_frame/fenced_frame_utils.cc
[add] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/disallowed-navigations-dangling-markup.https-expected.txt
[add] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/third_party/blink/web_tests/wpt_internal/fenced_frame/resources/report-url.html
[add] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/third_party/blink/web_tests/platform/generic/virtual/fenced-frame-mparch/wpt_internal/fenced_frame/disallowed-navigations-dangling-markup.https-expected.txt
[modify] https://crrev.com/fd8569850d538adc8e3012da1c7c8573f16a5356/content/browser/security_exploit_browsertest.cc


### do...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-01)

This issue was migrated from crbug.com/chromium/1301333?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1208744]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058920)*
