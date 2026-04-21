# Security: SoftNavigation + first-paint can leak history information

| Field | Value |
|-------|-------|
| **Issue ID** | [40066208](https://issues.chromium.org/issues/40066208) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>PerformanceAPIs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2023-06-22 |
| **Bounty** | $5,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

Soft navigations are a newly introduced metric inside of Chrome that allows  

developers to keep track of metrics such as LCP/FCP/FP inside of single page  

apps by designating certain user-driven events as "navigations" where the FP/FCP  

and LCP metrics are reset for the page.

By tying a soft navigation to a CSS change that adds styling for visited links on  

a page, and then listening/probing for first-paint/first-contentful-paint events  

(or the lack thereof) we are able to determine if a link has previously been visited  

by the user previously.

**VERSION**  

Chrome Version: 114.0.5735.133 (Official Build) (64-bit) + stable  

Chrome Version: 115.0.5790.32 (Official Build) beta (64-bit) + beta  

Chrome Version: 116.0.5829.0 (Official Build) dev (64-bit) + dev  

Operating System: Linux 6.1.34-1-lts

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

- Download attached driver.html and exploit.html into a seperate directory
- Create a server using the following command: `python3 -m http.server 8089`
- Open a Chrome browser instance and navigate to <https://en.wikipedia.org/wiki/Behala>
- Enable the Experimental Web platforms feature at chrome://flags/#enable-experimental-web-platform-features  
  
  and relaunch the browser
- Navigate to <http://0.0.0.0:8089/driver.html> and make sure it has permissions to open popups
- When <http://0.0.0.0:8089/test_stuff.html> opens, click on the text at > 500ms intervals untill it does  
  
  not reappear
- Once the text stops appearing, navigate back to the tab that has <http://0.0.0.0:8089/driver.html> and  
  
  open the developer console.
- The console should correctly identify <https://en.wikipedia.org/wiki/Behala> as having been visited and  
  
  <https://thisisnotgoogle.local> as having not been visited

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

NOTES

- Unblocking the popup blocker is not integral to the issue, and this could probably be achieved in a single page. However, doing it in a seperate page increases the reliability of the paint event.

EXPLANATION

- The exploit first sets up a page with some link styling CSS a link to a known unvisited page <https://thisisnotgoogle.local> and a button that a user can click.
- On clicking the button, the link href is changed to the target page being sniffed (say <https://en.wikipedia.org/wiki/Behala>) and the following CSS is injected into the page:

```
a:visited > button {  
    background-color: blue;  
}  
a:visited > button {  
    color: #fff;  
}`;  

```

thus triggering a soft navigation

- After every soft navigation, performance.getEntries() is queried to check if a new first paint/first-contentful-paint entry is added.
- If we do not detect a first-paint entry later than the soft navigation, we know that that the link is unvisited since  
  
  there was no paint update triggered from the last known unvisited link
- If we do detect a first-paint entry later than the soft navigation, we know that the link is visited since the page got updated  
  
  from the previously univisted styled link

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Sohom Datta

## Attachments

- [driver.html](attachments/driver.html) (text/plain, 962 B)
- [exploit.html](attachments/exploit.html) (text/plain, 2.3 KB)

## Timeline

### [Deleted User] (2023-06-22)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-22)

Thanks for the detailed report! I'm able to reproduce on 114.0.5735.133 Linux. Setting impact none since it is behind enable-experimental-web-platform-features; severity medium as it allows an attacker to reliably infer browsing history.

+yoavweiss@ to take a look. Thanks!

### da...@gmail.com (2023-06-23)

yoavweiss@ I was digging into the underlying code and it seems like there are two seperate bugs here:
- We are considering the color change of the link element to be a contentful event when it probably shouldn't be a contentful event
- We probably shouldn't be surfacing the raw first paint event since it does not provide the mitigations outlined in the [soft-navigation explainer](https://github.com/WICG/soft-navigations#mitigations) for the other metrics.

### yo...@chromium.org (2023-06-23)

Thanks for reporting! I'll look at mitigations, but the real solution here is to partition the :visited cache. kyraseevers@ - how far away are we from making it happen?

### ky...@chromium.org (2023-06-23)

Hey Yoav - for partitioning :visited history, I'm aiming for a Q3 experimentation period, and if all goes well, a Q4 launch rollout (of 2023). Still tentative, of course, but I hope this helps!

### yo...@chromium.org (2023-06-29)

pdr@ - any thoughts on ways for us to ignore paints that involve :visited related changes?

### yo...@chromium.org (2023-06-29)

[Empty comment from Monorail migration]

### yo...@chromium.org (2023-06-29)

[Empty comment from Monorail migration]

### pd...@chromium.org (2023-06-29)

Is this a new issue, beyond what is exposed for PerformancePaintTiming on first load, because we have an existing element that either paints or does not paint? If so, could we always invalidate the paint of visited link styles after soft navigations to mitigate this?

### mm...@chromium.org (2023-06-29)

You mean like if a page is entirely blank and only a :visited style will make it non-blank, and so fire FP/FCP?

### pd...@chromium.org (2023-06-29)

There is code to invalidate paint when visited link colors change (see: SetTextDecorationOrColorChanged in computed_style.cc). We can always treat the visited color style as changed after a soft navigation, so FP is reported for all links.

### yo...@chromium.org (2023-06-29)

I'm not 100% sure how that would work. Would I need to go over all the relevant LayoutObjects and invalidate them? Would that have performance implications?

### pd...@chromium.org (2023-06-30)

We already need to go over all the relevant LayoutObjects to determine if the visited color has changed. The proposal is to just always treat the visited color as changed after a soft navigation, rather than early-outing (without paint) if the visited color doesn't change.

### yo...@chromium.org (2023-07-03)

I was able to reproduce this (in a WPT) for FP and FCP, but not for LCP, since LCP doesn't take into account the same text element more than once. Given that, maybe the best/simplest solution is to disable FP and FCP reporting for soft navigations until partitioning takes place.

### yo...@chromium.org (2023-07-03)

ahemery@ - just remembered our discussion on https://groups.google.com/a/chromium.org/g/blink-dev/c/MK01W5X_x6E/m/EoflhJsJAgAJ
This is relevant :(

### gi...@appspot.gserviceaccount.com (2023-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145

commit caf3834a5cb3e46c2bdb6c18bd48f066eafd0145
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Thu Jul 06 13:41:00 2023

[soft navigations] Block FP and FCP entries behind a flag

Bug: 1457049
Change-Id: I3065b5941f89cedb8ee0df3331a5adaf9415b84d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4665521
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1166497}

[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/renderer/platform/runtime_enabled_features.json5
[add] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/visited-link.tentative.html
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/renderer/core/timing/soft_navigation_heuristics.cc
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/dropped-entries.tentative.html
[add] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/virtual/soft-navigation-fp-fcp/README.md
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/chrome/browser/page_load_metrics/integration_tests/data/soft_navigation.html
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/image-lcp-followed-by-two-image-softnavs-lcp.tentative.html
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/resources/soft-navigation-helper.js
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/multiple-paint-entries-buffered.tentative.html
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/renderer/core/timing/performance.idl
[modify] https://crrev.com/caf3834a5cb3e46c2bdb6c18bd48f066eafd0145/third_party/blink/renderer/core/timing/performance.h


### gi...@appspot.gserviceaccount.com (2023-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b1bdcc3456d6e658c7462269930a700e0885750

commit 6b1bdcc3456d6e658c7462269930a700e0885750
Author: Owen Min <zmin@chromium.org>
Date: Thu Jul 06 15:38:56 2023

Revert "[soft navigations] Block FP and FCP entries behind a flag"

This reverts commit caf3834a5cb3e46c2bdb6c18bd48f066eafd0145.

Reason for revert: 
Multiple external/wpt/soft-navigation-heuristics testing failure on
Mac:

https://ci.chromium.org/ui/p/chromium/builders/ci/mac11-arm64-rel-tests/21535/overview
https://ci.chromium.org/ui/p/chromium/builders/ci/mac12-arm64-rel-tests/9757/overview
https://ci.chromium.org/ui/p/chromium/builders/ci/mac13-arm64-rel-tests/1806/overview

Original change's description:
> [soft navigations] Block FP and FCP entries behind a flag
>
> Bug: 1457049
> Change-Id: I3065b5941f89cedb8ee0df3331a5adaf9415b84d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4665521
> Reviewed-by: Ian Clelland <iclelland@chromium.org>
> Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1166497}

Bug: 1457049
Change-Id: I705063df58ae9753db882533025d37c07826ab8f
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4667856
Commit-Queue: Owen Min <zmin@chromium.org>
Auto-Submit: Owen Min <zmin@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Owen Min <zmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1166558}

[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/renderer/platform/runtime_enabled_features.json5
[delete] https://crrev.com/0e15630d9358c9fe25034cdc0c83c0b4116f3781/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/visited-link.tentative.html
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/renderer/core/timing/soft_navigation_heuristics.cc
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/chrome/browser/page_load_metrics/integration_tests/data/soft_navigation.html
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/dropped-entries.tentative.html
[delete] https://crrev.com/0e15630d9358c9fe25034cdc0c83c0b4116f3781/third_party/blink/web_tests/virtual/soft-navigation-fp-fcp/README.md
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/image-lcp-followed-by-two-image-softnavs-lcp.tentative.html
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/resources/soft-navigation-helper.js
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/multiple-paint-entries-buffered.tentative.html
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/renderer/core/timing/performance.h
[modify] https://crrev.com/6b1bdcc3456d6e658c7462269930a700e0885750/third_party/blink/renderer/core/timing/performance.idl


### gi...@appspot.gserviceaccount.com (2023-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8

commit 22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Wed Jul 12 16:25:00 2023

Reland "[soft navigations] Block FP and FCP entries behind a flag"

This is a reland of commit caf3834a5cb3e46c2bdb6c18bd48f066eafd0145

Original change's description:
> [soft navigations] Block FP and FCP entries behind a flag
>
> Bug: 1457049
> Change-Id: I3065b5941f89cedb8ee0df3331a5adaf9415b84d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4665521
> Reviewed-by: Ian Clelland <iclelland@chromium.org>
> Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1166497}

Bug: 1457049
Change-Id: I4ef2b65c1f009c30fa17bbce8957dc85565babe4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4674335
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1169385}

[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/renderer/platform/runtime_enabled_features.json5
[add] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/visited-link.tentative.html
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/renderer/core/timing/soft_navigation_heuristics.cc
[add] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/virtual/soft-navigation-fp-fcp/README.md
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/dropped-entries.tentative.html
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/chrome/browser/page_load_metrics/integration_tests/data/soft_navigation.html
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/image-lcp-followed-by-two-image-softnavs-lcp.tentative.html
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/resources/soft-navigation-helper.js
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/multiple-paint-entries-buffered.tentative.html
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/renderer/core/timing/performance.idl
[modify] https://crrev.com/22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8/third_party/blink/renderer/core/timing/performance.h


### yo...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-14)

Hi yoavweiss@ thanks for your work on this issue, some quick questions 
1) I noticed you've requested a merge here on an open issue. Is there other work that is expected to be landed here to fully resolve this issue? 
2) This issue seems to be specific to an unlaunched feature behind a flag, labeled as Security_Impact-None -- is this issue going to field / OT in 116 or is there other reasons why a merge is being requested for this fix? 


### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2023-07-19)

anyressler@ - There are no other work expected, and yes, I'm hoping to run an OT with this feature in M116. Thanks!!

### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a2ef10dead3b21a1409e6be64f60b6a870306058

commit a2ef10dead3b21a1409e6be64f60b6a870306058
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Wed Jul 19 12:23:23 2023

Reland "[soft navigations] Block FP and FCP entries behind a flag"

This is a reland of commit caf3834a5cb3e46c2bdb6c18bd48f066eafd0145

Original change's description:
> [soft navigations] Block FP and FCP entries behind a flag
>
> Bug: 1457049
> Change-Id: I3065b5941f89cedb8ee0df3331a5adaf9415b84d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4665521
> Reviewed-by: Ian Clelland <iclelland@chromium.org>
> Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1166497}

(cherry picked from commit 22f1d2ed87d0cb515f5763fdebdad3d7bac3e0e8)

Bug: 1457049
Change-Id: I4ef2b65c1f009c30fa17bbce8957dc85565babe4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4674335
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1169385}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4697054
Reviewed-by: Noam Rosenthal <nrosenthal@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#600}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/renderer/platform/runtime_enabled_features.json5
[add] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/visited-link.tentative.html
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/renderer/core/timing/soft_navigation_heuristics.cc
[add] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/virtual/soft-navigation-fp-fcp/README.md
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/dropped-entries.tentative.html
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/chrome/browser/page_load_metrics/integration_tests/data/soft_navigation.html
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/image-lcp-followed-by-two-image-softnavs-lcp.tentative.html
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/resources/soft-navigation-helper.js
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/external/wpt/soft-navigation-heuristics/multiple-paint-entries-buffered.tentative.html
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/renderer/core/timing/performance.idl
[modify] https://crrev.com/a2ef10dead3b21a1409e6be64f60b6a870306058/third_party/blink/renderer/core/timing/performance.h


### am...@chromium.org (2023-07-19)

yoavweiss@ -- thank you for confirming and also proactively requesting a merge for and merging this bug fix that will impact OT in 116! 

### am...@google.com (2023-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-21)

Congratulations Sohom! The VRP Panel has decided to award you $5,000 for this high quality report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-20)

This issue was migrated from crbug.com/chromium/1457049?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066208)*
