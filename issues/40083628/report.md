# Security: General bypass of SRI validation for subresources located on the same origin

| Field | Value |
|-------|-------|
| **Issue ID** | [40083628](https://issues.chromium.org/issues/40083628) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **CVE IDs** | CVE-2016-1636 |
| **Reporter** | ry...@cyph.com |
| **Assignee** | jw...@chromium.org |
| **Created** | 2016-02-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

The spec requires that subresources located on the same origin be treated identically to cross-origin resources in the context of SRI (<https://www.w3.org/TR/SRI/#is-response-eligible-for-integrity-validation>). However, as demonstrated, same-origin SRI in Chrome can (trivially) be entirely bypassed.

As far as severity, I would consider this to be Critical in that it allows arbitrary code execution in a context where the exploited feature's threat model explicitly guarantees protection from this attack vector.

**VERSION**

Chrome Version: 48.0.2564.103 (64-bit) stable

Operating System: Mac OS X El Capitan v10.11.3 (15D21)

**REPRODUCTION CASE**

<https://heisenberg.co/sridemo/sameorigin>

Expected result: this demo should behave identically to <https://heisenberg.co/sridemo>.

Actual result: clicking the button to inject the script with the invalid SRI hash correctly produces the expected error the first time, but on every subsequent click it actually executes.

## Attachments

- [Screen Shot 2016-02-05 at 4.22.08 pm.png](attachments/Screen Shot 2016-02-05 at 4.22.08 pm.png) (image/png, 267.9 KB)

## Timeline

### ry...@cyph.com (2016-02-04)

[Comment Deleted]

### ry...@cyph.com (2016-02-04)

Sorry, slight correction re: severity. I was going off of https://dev.chromium.org/developers/severity-guidelines, and misunderstood Critical's qualifier for arbitrary code execution.

This issue would actually be High ("A bug that allows arbitrary code execution within the confines of the sandbox").

### ke...@chromium.org (2016-02-04)

I verified the behavior in a VM. Joel, do you have bandwidth to take a look and verify if the behavior is incorrect?

### cl...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### ry...@cyph.com (2016-02-05)

Would you guys be able to give bryant@zadegan.net access to this issue? I'm about to go out of town for a week, and he wants to be able to keep up with the issue and provide any necessary information in my place (he and I discovered the bug together).

### jw...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### jw...@chromium.org (2016-02-05)

Yes, that's reasonable. I've added bryant@zadegan.net to the bug.

I'll take a look at this as soon as I can. I'm traveling, though, so my hours are a bit off at the moment.

I have mixed feelings about the security severity, since this requires the victim site to load the same script twice for the attack to happen. That feels "unusual" to me and that it might be more appropriate as a Medium, but that's just getting nit picky, so I'll leave it as high for now, unless inferno@ disagrees.

### br...@zadegan.net (2016-02-05)

That'll likely reduce the number of sites affected by a good amount, though it's worth considering how many sites may well dynamically load resources in this same fashion multiple times as an artifact of their design. Off the top of my head, I can think of at least two sites I've assessed which would be impacted by this (the specific pattern is a site which reverse-proxies resources from a third party/CDN in order to maintain same origin, and then loads a script multiple times as a side effect of fulfilling e.g. a never-ending-scroll pattern). 

Additionally, Ryan and I just tested to see whether or not scripts with query strings would continue to bypass it, and it appears (inconsistently, in our testing) to hold true. Assuming the first load of the script (e.g. "dir/script.js") bombs, the next load of a script seems to work *even in the event that there's a query strong on it* (e.g. "dir/script.js?page=2"). This would appear to broaden the impact in this case as there are many who may load resources dynamically through altering query strings. I've seen this pattern more frequently (query strings modifying CSS and scripts alike).

Ryan also believes he's seen this happen without loading the script twice. The inconsistency would suggest that an attacker need not target sites which double-load the script; rather, just targeting as many sites as possible which either load or proxy resources through the same origin will lead to some quick wins.

### ry...@cyph.com (2016-02-05)

re: Bryant's last comment, see attached screenshot (no error appeared in the console upon the first click).

It seems like this happens on occasion when the browser gets into a bad state from it having already been exploited once, but it's entirely possible that 1) that state could carry over to other script URLs and/or sites after having been triggered in one site (no clue, just speculation), and/or 2) that initially triggering the state with multiple script loads may not be a strict requirement.

### ry...@cyph.com (2016-02-05)

[Comment Deleted]

### ry...@cyph.com (2016-02-05)

[Comment Deleted]

### br...@zadegan.net (2016-02-05)

@ryan, oh, well that's pretty cool. Alright, so since there's certainty that at least in some cases an invalid SRI check will still fail to protect on the *initial* execution, this would make an attack against a popular script or a large CDN much more likely to be successful for applications which reverse proxy those resources. At least a few people will be dinged if a very common resource is tampered.

### jw...@chromium.org (2016-02-08)

I'm not surprised to hear that it happens on first load if it has already been exploited. I'm sitting down to work on this know, but I'm pretty sure it's a Memory Cache issue, so I'm guessing as long as the resource is sitting in the renderer's cache, it should be exploitable. I'll report back when I know more.

### br...@zadegan.net (2016-02-08)

Yup, my further testing suggests that's right. I reproduced it earlier today and noticed its based on the cached state of the script itself even if the loaded parent resource is different e.g. via query string, which means this is exploitable so long as the malicious script is already cached by the browser. It'll always load and bypass SRI in that event.

Whats the best way to upload a video? Private or Unlisted YouTube link sufficient? I'm having issues uploading it to this thread directly.

### ry...@cyph.com (2016-02-08)

[Comment Deleted]

### ry...@cyph.com (2016-02-08)

Ooh, that sounds kinda bad if the trigger is just that the malicious script is cached. Far from the original exploit case, this pretty much entirely nullifies any protection that SRI would otherwise offer.

Broader exploit steps:

1. Compromise/MitM a major CDN.

2. Replace all hosted resources with malicious code and set cache-control to max-age of one year.

3. User Alice visits any random website that pulls a compromised resource from that CDN; if that site happens to use SRI, then Alice is protected as expected.

4. SRI'd or not, every other website that depends on that particular resource is now compromised for Alice.

### jw...@chromium.org (2016-02-08)

No, I believe it is the Memory Cache, which is a Chrome internal caching mechanism separate from the general HTTP disk cache. It is used for recently requested resources that are not cache-invalid for the same origin only, so that attack wouldn't work. That is, if origin A requests a resource b from origin B, and separately origin C requests resource b from origin C, the resource would not be obtained from the memory cache because it's per-origin.

In any case, I'll try and verify if that's what's going on.

### ry...@cyph.com (2016-02-08)

Ahh, got it. That makes more sense (what I described couldn't work since I'd already confirmed that cross-origin SRI behaved as expected).

### jw...@chromium.org (2016-02-08)

Okay, I'm fairly confident I've found the root cause, but I'll have to test this later tonight.

After a script resource is grabbed from the memory cache, we check if the integrity has already been checked for the resource (see https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/PendingScript.cpp&sq=package:chromium&l=153&rcl=1454892886). We do this for scripts for reasons described in the comment at https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/dom/PendingScript.cpp&sq=package:chromium&l=120&rcl=1454892886, but that's not really all that important (basically, the buffer for script resources doesn't stick around, so we need to do our integrity checks at the beginning).

Unfortunately, that code assumes that if the integrity was checked, that it was *valid*. Clearly that's not true, as we're seeing here. So what we probably need is instead of an integrityChecked() method, we need an intergrityState() method that returns one of "not checked," "checked and valid," or "checked and invalid." I'm pretty sure that would solve this issue. I'll validate that hypothesis later tonight.

### br...@zadegan.net (2016-02-08)

That explanation seems to line up perfectly with the behavior I observed here (included with Private permissions with you added as a permitted viewer, per your guidance):

https://youtu.be/CH0F39jVuhM
https://youtu.be/deDAg_2B1sQ

Good luck on the fix. Do you have your own test logic, or are you testing it against heisenberg.co/sridemo/sameorigin?

### jw...@chromium.org (2016-02-08)

I have my own test that I've written that we'll use as the integration test for this in the fix, but I'll also make sure to test it against your demo.

### jw...@chromium.org (2016-02-08)

https://codereview.chromium.org/1675183003/ is up for review and should fix it. After it lands, I'll start the merge request process after it sits on Canary/Dev for a few days.

### br...@zadegan.net (2016-02-08)

Did you intend for the issue page to be public? It looks like I can access the page without authenticating under my account.

### jw...@chromium.org (2016-02-08)

That's normal. Our patches are always public by default, and the second it lands it will be public anyway. Occasionally we make them "protected", but it's quite a big hassle as it means folks like you can't see them.

### br...@zadegan.net (2016-02-08)

Makes sense. Thanks for the insight.

### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bf24693238d407f90bec71453b18aae8dd1c0f43

commit bf24693238d407f90bec71453b18aae8dd1c0f43
Author: jww <jww@chromium.org>
Date: Tue Feb 09 08:19:04 2016

Fix SRI bypass by loading same resource twice in same origin.

This fixes a bug where the memory cache was bypassing subresource
integrity checks when a resource is loaded for a second time in the same
origin. The resource in the memory cache was correctly storing that an
integrity check had already been done so whene it was retrieved later,
it wouldn't need to be checked again, but it didn't store the fact that
this was a *failure*, so when the load happened a second time, it
assumed it was a good integrity.

This modifies the resources to store a disposition for the integrity
check, rather than just that the integrity check occurred. On a reload
of the resource, if the integrity had failed the first time, the
resource will fail to load.

BUG=584155

Review URL: https://codereview.chromium.org/1675183003

Cr-Commit-Position: refs/heads/master@{#374336}

[add] http://crrev.com/bf24693238d407f90bec71453b18aae8dd1c0f43/third_party/WebKit/LayoutTests/http/tests/security/subresourceIntegrity/subresource-integrity-block-same-resource-twice.html
[modify] http://crrev.com/bf24693238d407f90bec71453b18aae8dd1c0f43/third_party/WebKit/Source/core/dom/PendingScript.cpp
[modify] http://crrev.com/bf24693238d407f90bec71453b18aae8dd1c0f43/third_party/WebKit/Source/core/fetch/ScriptResource.cpp
[modify] http://crrev.com/bf24693238d407f90bec71453b18aae8dd1c0f43/third_party/WebKit/Source/core/fetch/ScriptResource.h


### jw...@chromium.org (2016-02-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-18)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### jw...@chromium.org (2016-02-19)

[Comment Deleted]

### jw...@chromium.org (2016-02-19)

[Comment Deleted]

### jw...@chromium.org (2016-02-19)

tinazh: I received an auto "merge approved" email during the time that the Monorail transition was happening, and I'm afraid the approval was lost there. Can you confirm that this merge to 49 is approved?

### ti...@google.com (2016-02-19)

Can you pls copy the auto "merge approved" email in? We'll re-add the merge approval soon.

### jw...@chromium.org (2016-02-19)

Sure! The contents of the email were:

Updates:
        Labels: -Merge-Request-49 Merge-Approved-49 Hotlist-Merge-Approved

https://crbug.com/chromium/584155#c29 on https://crbug.com/chromium/584155 by tinazh@google.com: Security: General bypass
…

of SRI validation for subresources located on the same origin
https://code.google.com/p/chromium/issues/detail?id=584155#c29

Your change meets the bar and is auto-approved for M49 (branch: 2623)

### ti...@google.com (2016-02-19)

Great, I've added the merge approval back!

### bu...@chromium.org (2016-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0979e9712439b056355af462d68fe5c6d9ee5466

commit 0979e9712439b056355af462d68fe5c6d9ee5466
Author: Joel Howard Willis Weinberger <jww@chromium.org>
Date: Fri Feb 19 17:52:21 2016

Fix SRI bypass by loading same resource twice in same origin.

This fixes a bug where the memory cache was bypassing subresource
integrity checks when a resource is loaded for a second time in the same
origin. The resource in the memory cache was correctly storing that an
integrity check had already been done so whene it was retrieved later,
it wouldn't need to be checked again, but it didn't store the fact that
this was a *failure*, so when the load happened a second time, it
assumed it was a good integrity.

This modifies the resources to store a disposition for the integrity
check, rather than just that the integrity check occurred. On a reload
of the resource, if the integrity had failed the first time, the
resource will fail to load.

BUG=584155

Review URL: https://codereview.chromium.org/1675183003

Cr-Commit-Position: refs/heads/master@{#374336}
(cherry picked from commit bf24693238d407f90bec71453b18aae8dd1c0f43)

Review URL: https://codereview.chromium.org/1713093002 .

Cr-Commit-Position: refs/branch-heads/2623@{#452}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[add] https://crrev.com/0979e9712439b056355af462d68fe5c6d9ee5466/third_party/WebKit/LayoutTests/http/tests/security/subresourceIntegrity/subresource-integrity-block-same-resource-twice.html
[modify] https://crrev.com/0979e9712439b056355af462d68fe5c6d9ee5466/third_party/WebKit/Source/core/dom/PendingScript.cpp
[modify] https://crrev.com/0979e9712439b056355af462d68fe5c6d9ee5466/third_party/WebKit/Source/core/fetch/ScriptResource.cpp
[modify] https://crrev.com/0979e9712439b056355af462d68fe5c6d9ee5466/third_party/WebKit/Source/core/fetch/ScriptResource.h


### jw...@chromium.org (2016-02-19)

Thanks! I'll request a merge to stable after this percolates on Beta for a while, assuming all goes well.

### bu...@chromium.org (2016-02-19)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/0979e9712439b056355af462d68fe5c6d9ee5466

commit 0979e9712439b056355af462d68fe5c6d9ee5466
Author: Joel Howard Willis Weinberger <jww@chromium.org>
Date: Fri Feb 19 17:52:21 2016


### ti...@google.com (2016-02-29)

Adding reward-topanel to consider this reward under the Chrome reward program: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2016-03-02)

Congratulations Ryan - our reward panel decided to award you $2,000 for this report.

We'll list you in today's release notes for Chrome 49 as "ryan@cyph.com". If you'd like to update that to another name for credit, please let me know. I'll also follow up with a CVE-ID for your reference.

Someone from our finance team should be in touch within 7 days to collect your payment details. If this doesn't happen, please either update this bug or email me directly at timwillis@

Thanks again for your report and helping to keep Chrome awesome.

### ti...@google.com (2016-03-02)

CVE-2016-1636

### br...@zadegan.net (2016-03-03)

All, can we kindly edit the post (http://googlechromereleases.blogspot.com/2016/03/stable-channel-update.html) for credit? Per https://crbug.com/chromium/584155#c4, this was a collaborative effort.

### br...@zadegan.net (2016-03-03)

[Comment Deleted]

### ry...@cyph.com (2016-03-03)

Awesome, thanks Tim! re: Bryant's comments, that sounds good to me if you guys don't mind the dual attribution.

### ti...@google.com (2016-03-03)

#41/43: Thanks for confirming Ryan - updated: http://googlechromereleases.blogspot.com/2016/03/stable-channel-update.html

Also, can you both confirm how you want to be paid? I understand you want a $1500/$500 split, but grateful for your confirmations.

### ry...@cyph.com (2016-03-03)

Yep, that split is correct.

### br...@zadegan.net (2016-03-04)

Tim, two questions:

1) Any objections to us publicizing the PoC exploit we delivered with the vuln today?

2) What were the primary factors which went into deciding the bounty amount? This was our first submission, so given that we delivered a High with reporting that we believe met the bar for high quality reporting + functional exploit, we're looking to further refine our reporting based on the Chromium team's expectations in order to achieve the full bounty amount for vulnerabilities in the future.

### ti...@google.com (2016-03-09)

Hey Bryant,

1) I usually ask reporters to wait a few weeks from release to make sure that there's a high percentage of users with the update. If you want to publish earlier, would you mind providing some context as to why? (e.g. speaking at a conference, some other deadline, et c.). 

2) The $4000 (high quality report + functional exploit) is the highest reward in that category where the exploitation of the bug is usually unconstrained. When reviewing this bug, the panel likely determined that the constraints around exploitation meant that the provided POC didn't quite meet the high bar stated on the reward page[1]: "A high-quality report with a reliable exploit that demonstrates that the bug reported can be easily, actively and reliably used against our users".

If you want more info, feel free to take a look at reports that received $4,000[2] (though note that you probably don't want to back past Oct 2014 as we had different reward levels at that time).

Hope that helps - thanks again for your report!

[1] https://www.google.com/about/appsecurity/chrome-rewards/
[2] https://bugs.chromium.org/p/chromium/issues/list?can=1&q=label%3Areward-4000

### br...@zadegan.net (2016-03-09)

1) Ah, perfect. Thanks for the insight! The discovery came about during the drafting of a conference talk, so while we'd like to publicize the find sooner rather than later, it's not necessary by any means.

2) I believe I understand. So rather than this being a sole judgment of the proof of concept itself, the decision hinges equally on the actual exploitability of the flaw as well as the refinement of the proof of concept. Am I understanding correctly?

Thanks for your feedback!

### ti...@google.com (2016-03-09)

#48: Most welcome.

1) Cool. Note that the two weeks will be up on Tuesday next week (15 March), so if you don't mind waiting another five days, you should be good to go.

2) Yes. It's not a sole judgement on the PoC itself. The reliability of the exploit and the likelihood of success against victims are certainly considerations. 

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/584155?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083628)*
