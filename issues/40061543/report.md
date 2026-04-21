# Use-after-poison in blink::CSSSelector::SelectorListOrParent

| Field | Value |
|-------|-------|
| **Issue ID** | [40061543](https://issues.chromium.org/issues/40061543) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2022-11-01 |
| **Bounty** | $10,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5142671283912704

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7e99002e8e08
Crash State:
  blink::CSSSelector::SelectorListOrParent
  blink::SelectorChecker::CheckPseudoClass
  blink::SelectorChecker::MatchSelector
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1065489:1065493

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5142671283912704

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- [clusterfuzz-testcase-minimized-4826435190718464.zip](attachments/clusterfuzz-testcase-minimized-4826435190718464.zip) (application/octet-stream, 702 B)

## Timeline

### cl...@chromium.org (2022-11-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-01)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS]

### cl...@chromium.org (2022-11-01)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/6be01182c14c5d0dc7026e5166cb10dbba5efec5 ([css-nesting] Move towards syntax proposal 3.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2022-11-01)

Assigning to sesse@, PTAL?

There are two CLs of yours in the regression range.

### se...@chromium.org (2022-11-01)

This is definitely an area I've been working on, so it's probably mine yes. But most likely, it only happens if you enable experimental web features, so it's not urgent. I'll have a look tomorrow (not the least because it seems to be 600 kB…).

### m....@gmail.com (2022-11-02)

mini testcase(https://clusterfuzz.com/testcase-detail/4826435190718464)

<script src="h1.js"></script><body onload="start();"><script>
	async function trigger1() {
{
}; 
try { help_tag2id("x-shadow",138).setAttribute(); } catch(e){}
 /*Int32Array*/ var v3318 = new Int32Array(536870911); 
	}
	function start() {
			trigger1();
}
</script>
<style>
#id7{
:root:lang(bas),:not(:lang(bas))>:lang(bas){
</style>
					<s id="id138" cs="cs14""11" lang="en"></s>

### se...@chromium.org (2022-11-02)

As expected, only happens with --enable-experimental-web-platform-features, so downgrading priority.

### m....@gmail.com (2022-11-02)

Because this is a security issue, the Security_Impact-None flag should be set instead of lower priority.
```
[1]
Can't impact Chrome users by default
If the bug can't impact Chrome users by default, this is denoted instead by the Security-Impact_None label. See the security labels document for more information. The bug should still have a severity set according to these guidelines.

[2]
Security_Impact-None says that the bug can‘t affect any users running the default configuration of Chrome. It’s most commonly used for cases where code is entirely disabled or absent in the production build.

Other cases where it's OK to set Security_Impact-None:

The impacted code runs behind a feature flag which is disabled by default, and the field trial configuration has not been switched on.
The impacted code only runs behind a command-line flag or chrome://flags entry. (In particular, if a bug can only affect those who have set #enable-experimental-web-platform-features, it is Security_Impact-None.
It's a V8 feature behind flags such as --future, --es-staging or --wasm-staging or other experimental flags that are disabled by default.
```
[1]https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-no-impact
[2]https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#When-to-use-Security_Impact_None-TOC_Security_Impact_None

### se...@chromium.org (2022-11-02)

[Empty comment from Monorail migration]

### se...@chromium.org (2022-11-02)

[Empty comment from Monorail migration]

### se...@chromium.org (2022-11-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/617c2ea64f9fd6f1439913c98031863b0cc87a33

commit 617c2ea64f9fd6f1439913c98031863b0cc87a33
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Wed Nov 02 12:48:26 2022

[css-nesting] Fix a use-after-free on inserted parent selectors.

When checking whether a selector list is nest containing,
we temporarily set last_in_selector_list_ on the selector
right before the (possibly) inserted &. However, when clearing
it afterwards, we'd clear it on the wrong element (we didn't
take into account that back() pointed to something else),
leaving the flag there. This meant that Oilpan tracing
would stop at the element, missing later complex selectors
in the same list, eventually causing use-after-free.

Only relevant when CSS Nesting is activated (which it isn't
by default).

Fixed: 1380313
Change-Id: Ia912ee2d5538d7067c0d14786158372a544d5cd3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3999320
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1066437}

[modify] https://crrev.com/617c2ea64f9fd6f1439913c98031863b0cc87a33/third_party/blink/renderer/core/css/parser/css_selector_parser.cc
[add] https://crrev.com/617c2ea64f9fd6f1439913c98031863b0cc87a33/third_party/blink/web_tests/external/wpt/css/css-nesting/implicit-parent-insertion-crash.html


### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-02)

ClusterFuzz testcase 5142671283912704 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1066435:1066439

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### se...@chromium.org (2022-11-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $2,000 fuzzer bonus for a total of $12,000 VRP reward. Thank you for your continue efforts in fuzzing Chrome -- nice work! 

### am...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1380313?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1380647, crbug.com/chromium/1380755, crbug.com/chromium/1381093]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061543)*
