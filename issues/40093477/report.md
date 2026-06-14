# Security: Origin header-based CSRF protection bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40093477](https://issues.chromium.org/issues/40093477) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>Submission, Blink>SecurityFeature, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | lu...@chromium.org |
| **Created** | 2018-12-16 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

CSRF protection bypass with user input is possible via a bug where refreshing a failed cross-origin form submission changes the request origin upon resubmission.

**VERSION**  

Chrome Version: 71.0.3578.98 (Official Build) (64-bit)  

Operating System: Mac OS Sierra 10.12.6

**REPRODUCTION CASE**  

Since this attack has to be demonstrated against a service employing Origin based CSRF protection, my videos demonstrate this bug to bypass CSRF protection and get RCE in the MacOS software Übersicht.

The flow for this attack is as follows:

1. wait for ctrl (windows) or command (macos)
2. submit a cross-origin form to the Origin protected endpoint
3. when the user completes pressing ctrl-r or cmd-r, the cross-origin submission is refreshed (doesn't appear to be a race here)
4. when the submission is refreshed, it's re-sent by Chrome with Origin header corresponding to the API origin
5. now having the correct origin header, the CSRF protection is bypassed

I recommend using Chrome Web Inspector to inspect the origin header sent upon submission and resubmission.

I provide two video examples:

1. chrome origin bypass devtools.mp4 -- showing the immediate effect if devtools is open
2. csrf bypass no devtools.mp4 -- showing if devtools is closed

USER INPUT NEEDED

1. if the user has chrome devtools open, no popup is opened asking to re-send, causing immediate CSRF when the refresh keystroke is used
2. if the user doesn't have devtools open, the user has to confirm (with a click or return) that they wish to refresh.  
   
   2a) the user can be told to press command + control + return (not unreasonable) instead of command + r  
   
   2b) the user can be coerced into inspecting an element with chrome dev tools  
   
   2c) the user already has chrome devtools open  
   
   2b) In my opinion most users confirm that dialog out of fear of losing what they're looking at (I know I have).
3. the method by which Chrome determines whether to open the popup or not is mysterious to me. I read the C++ code and there doesn't seem to be a means by which the dialog should not show, and yet in some cases it doesn't. If we can trigger this behavior without having devtools open, the issue is much more severe.

**CREDIT INFORMATION**  

thomas "zemnmez" shadwell

## Attachments

- [chrome origin bypass devtools.mp4](attachments/chrome origin bypass devtools.mp4) (video/mp4, 147.3 KB)
- [csrf bypass no devtools.mp4](attachments/csrf bypass no devtools.mp4) (video/mp4, 346.2 KB)
- [csrf-bypass-simple.html](attachments/csrf-bypass-simple.html) (text/plain, 649 B)
- [csrf-bypass-simple.html](attachments/csrf-bypass-simple_53014739.html) (text/plain, 666 B)

## Timeline

### ca...@chromium.org (2018-12-16)

Assigning low since this requires significant user interaction. This seems similar to crbug.com/747812. jam@: Can you take a look since you worked on the other bug? Thanks.

[Monorail components: Blink>Forms>Submission Blink>SecurityFeature]

### sh...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### [Deleted User] (2018-12-17)

I noticed that in Windows the effect of submitting the form is not immediate, causing a rather inconvenient race where if the user pressed ctrl-r too fast the bypass wouldn't work.

This is fixed by setting {capture:true} on the 'keydown' event to prevent bubbling.

### [Deleted User] (2018-12-17)

Ok. I just had a big realization that might bump the severity of this ticket. The code that decides whether to open the confirmation dialog looks like this:

https://github.com/chromium/chromium/blob/f1ef4405b08f701d2bdae9494e0cdf92506de98e/content/browser/frame_host/navigation_controller_impl.cc#L586

> if (g_check_for_repost && check_for_repost &&
>      entry->GetHasPostData()) {
>    // The user is asking to reload a page with POST data. Prompt to make sure
>    // they really want to do this. If they do, the dialog will call us back
>    // with check_for_repost = false.
>    delegate_->NotifyBeforeFormRepostWarningShow();
>
>    pending_reload_ = reload_type;
>    delegate_->ActivateAndShowRepostFormWarningDialog();

The heuristic that's used to determine if the form post is state-changing is simply if the form *has POST data*. Virtually all frameworks, for example Go's allow parameters to be sent in URL Query params, rather than POST body.

This means, regardless of method, as long as we send the parameters *in the URL* the CSRF protection is bypassed **with no confirmation to the user**!! 

### [Deleted User] (2018-12-17)

[Comment Deleted]

### [Deleted User] (2018-12-19)

[Comment Deleted]

### [Deleted User] (2018-12-19)

previously I said that calling history.back() would trigger this bug, but I've found it's only the case if devtools is open with 'disable cache'

### ta...@google.com (2018-12-19)

Hey Chris, could you take a look at this, it feels like it might be close to a bad Origin bypass bug?

If Origin could be defeated, then a whole bunch of things are in trouble.

If I understand correctly, the missing piece is causing a cache eviction, but that seems totally plausible.

### pa...@chromium.org (2018-12-19)

There was a debate internally recently about whether or not we should write apps to rely solely on the Origin header for CSRF defense. The consensus was "No; or at least not yet", and I was a proponent of that view. This bug is another data point supporting that view, sadly. :)

FWIW, MDN documents Origin as only ever being sent with POSTs (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin), which to me makes it unsuitable for a generic CSRF defense — sometimes state-changing actions are formulated as GETs (rightly or wrongly).

So, I'd definitely consider reporting reliance on Origin as a bug to the Übersicht developers as well. 2 bugs for the price of 1! :)

As for severity, this sounds like High (https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#High-severity): "High severity vulnerabilities allow an attacker to execute code in the context of, or otherwise impersonate other origins." It's Chrome's mistake that the Origin header doesn't have the right value, so a mechanism that would otherwise arguably be OK for CSRF defense becomes ineffective. Whether Origin is intended as a CSRF defense, I am not sure; MDN doesn't say anything about it. The IETF draft (https://tools.ietf.org/id/draft-abarth-origin-03.html; is there a final RFC?) does claim Origin is a *mitigation*: "HTTP servers can use the Origin header to mitigate against Cross-Site Request Forgery (CSRF) vulnerabilities." — but that's not quite the same as a *solution*. I think the classic CSRF defense, a random token in the action formulation itself, is a reliable solution to CSRF.

The need for user interaction would bump this vulnerability down 1 level in severity, but not 2. So, I think Medium. But it seems like maybe user interaction is no longer necessary, depending on the particular web application framework? If so, one could still blame the web app framework a bit, since it should be designed knowing that Origin is (apparently) intended for POSTs and CORS only (MDN disagrees with the IETF draft), and that state-changing actions should be POSTs, not GETs.

Also I don't see why Chrome would behave differently on Android.

+mkwst and aaj for open web platform security knowledge
+jochen too

Also, it'd be great to update MDN with whatever the real guarantees of Origin are, and to create a Web Platform Test case for Origin? I don't see one in third_party/blink/web_tests/external.

### ca...@chromium.org (2018-12-19)

+1 on documenting what we can rely on Origin for. As for severity, I agree that we consider the Origin header a security guarantee (which I'm not entirely sure that's the current case), this seems like a high w/o user interaction required, medium with.

### [Deleted User] (2018-12-19)

In the context of this bug, I found the original paper which proposes it (on OWASP which describes it as a 'defence in depth' measure): https://seclab.stanford.edu/websec/csrf/csrf.pdf

I can't speak for how it's perceived within the chrome dev team of course, but outside that I'd always understood it as a fine CSRF mitigation for (1) transitional states to CSRF tokens (2) systems that only support browsers that send it and / or referer or (3) systems where implementing CSRF tokens is difficult AND (2) applies.

> The need for user interaction would bump this vulnerability down 1 level in severity, but not 2. So, I think Medium. But it seems like maybe user interaction is no longer necessary, depending on the particular web application framework? If so, one could still blame the web app framework a bit, since it should be designed knowing that Origin is (apparently) intended for POSTs and CORS only (MDN disagrees with the IETF draft), and that state-changing actions should be POSTs, not GETs.

The comment I was making was that regardless of method, the popup that asks to confirm the resubmit only comes up if there is *post body data*. It doesn't look at the request method at all to my knowledge.

Lots of web frameworks including, Go and I believe AWS lambda via API gateway put the query parameters in the body and those in the URL in the same place. I was suggesting, then that you make the request with no body at all, with the POST method and with your malicious parameters in the URL. That bypasses the 'confirm resubmit'? prompt we show the user.

The user interaction required, then is pressing ctrl (or command) r.

There's also I case that I hope gets looked into by someone who knows browser internals better where if the history cache is purged, issuing history.back() causes a resubmit and bypasses this Origin control.


### [Deleted User] (2018-12-19)

Sorry -- correction on my comment there. The paper proposes it as a *prevention* measure for CSRF attacks. This is the one that I read way back that gave me the impression it was, in some cases as good as using CSRF tokens.

### sh...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### ja...@chromium.org (2018-12-26)

I'm not really a good owner for this

### ts...@chromium.org (2019-01-03)

Mike, could you weigh in on this?  Thanks.

### sh...@chromium.org (2019-01-04)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-18)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2019-01-18)

For this bug specifically, +alexmos@ and +creis@, as they know significantly more about navigation code than I do. It feels like we're not writing the correct values to the navigation entry, but I'd just be guessing if I started digging through the code.

For `Origin` generally, I agree with Chris that it can't be a complete mitigation for CSRF, but agree more with Tavis that it must behave correctly in the places where we send it today.

### al...@chromium.org (2019-01-18)

For the underlying bug, it seems that on reload, the Origin header is getting set from AddAdditionalRequestHeaders in NavigationRequest [1]:

  if (!NeedsHTTPOrigin(headers, method))
    return;

  // Create a unique origin.
  url::Origin origin;
  if (frame_tree_node->IsMainFrame()) {
    // For main frame, the origin is the url currently loading.
    origin = url::Origin::Create(url);
  } else if ((frame_tree_node->active_sandbox_flags() &
              blink::WebSandboxFlags::kOrigin) ==
             blink::WebSandboxFlags::kNone) {
    // The origin should be the origin of the root, except for sandboxed
    // frames which have a unique origin.
    origin = frame_tree_node->frame_tree()->root()->current_origin();
  }

  headers->SetHeader(net::HttpRequestHeaders::kOrigin, origin.Serialize());

I.e., this is always setting the origin header to the current main frame's last committed origin.  Here, IIUC, we're submitting a form from A to B, and then we reload B, expecting the Origin header to still reflect A, but since B's already committed, the Origin header ends up being B.  I can repro this on https://csreis.github.io/tests/form-post.html.

mkwst@: is it correct that we should still set the Origin header to A on such reloads?  Technically, this is a browser-initiated navigation, and the frame that initiated the form post isn't even around anymore.

If that is the desired behavior, maybe we should be using the initiator origin here.  That's already passed into AddAdditionalRequestHeaders, but unfortunately it's null for browser-initiated navigations, and it's not stored anywhere.  We could consider storing it on FrameNavigationEntry (alongside the committed origin) and then using that for calculating the Origin header here.  I won't have cycles for this in the short term, so for now I'll pass this over to nasko@, given that this is somewhat related to https://crbug.com/chromium/882053 which he's been looking at recently.  clamy@ added the above Origin header logic in r437662 and could be another good person to take a look at this.

[1] https://cs.chromium.org/chromium/src/content/browser/frame_host/navigation_request.cc?l=239&rcl=5706fd9f809a27eab26f46774525a0e8098a6ffa


[Monorail components: UI>Browser>Navigation]

### na...@chromium.org (2019-01-19)

While this bug does seem potentially related to https://crbug.com/chromium/882053, it isn't really. As far as initiator origin goes, I don't think we should be storing it on the navigation entry, as it is something only used to calculate the new origin at commit time and is not useful afterwards. Actually, if we store it, it can be actively harmful.

Consider navigation to A first, which navigates to B, which navigates to C. If we store initiator origin, for the navigation to B the initiator will be A. However, if document C does history.back(), then it is incorrect to use A as the initiator, since in reality it is C that caused the navigation to happen.

I don't know enough about how Origin is supposed to behave for navigations. In general, for subresources we set Origin only on cross-origin request, so if we keep the spirit that Origin is only set on cross-origin cases, the logic of setting Origin to the URL we are navigating *to* does seem broken to me. Chatting briefly with Alex, he mentioned that we set Origin to null if we encounter cross-origin redirects, so maybe in this case it is safer to do the same.

I'm also not going to be able to look at this for the next few days, so assigning to clamy@ to move it forward in my absence.

### cl...@chromium.org (2019-01-23)

Sorry just seen that. I have been travelling all week and won't be back in office before Jan 25.

### me...@chromium.org (2019-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2019-02-28)

what's happening with this ticket?


### pa...@chromium.org (2019-02-28)

Friendly ping, clamy. :) If you're not the right person for this bug, can you help us find a more appropriate person? Thanks!

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2019-03-25)

any movement on this? I'm hoping to include advice *not* to rely on the Origin header in a security talk I'm making in about a month -- a ton of modern web (electron etc) desktop systems *have* to rely on Origin headers to protect themselves against CSRF from malicious sites unless they want to get into the complicated process of issuing CSRF tokens to yourself

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### na...@chromium.org (2019-04-25)

clamy@, I think in recent discussions there was an agreement that we can make progress on this. Any chance of moving this forward soon?

### dr...@chromium.org (2019-05-30)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

Pinged clamy@ over email.

### cl...@chromium.org (2019-07-02)

Assigning to nasko@ as he has better kowledge of what should be done to fix this.

### na...@chromium.org (2019-07-02)

One update on https://crbug.com/chromium/915538#c21 from myself - on different discussions it became more clear that we do need to store the initiator origin on the FrameNavigationEntry. I think lukasza@ even has a WIP CL to do this (https://chromium-review.googlesource.com/c/chromium/src/+/1662738). Once we have that stored on the FNE, we can easily change the code in this bug to use the initiator origin in its calculation of the Origin header.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

nasko@: now that you're back, do you have any updates for this issue? Thanks very much!

- a friendly security marshal

### lu...@chromium.org (2019-08-19)

I have a WIP CL with a fix at https://chromium-review.googlesource.com/c/chromium/src/+/1761051

I think that this CL should take care of using the right initiator/Origin-header in history navigations and in reloads.  Note that other attack vectors may be possible - for example Open-Link-In-New-Tab context menu doesn't preserve the initiator (see https://crbug.com/chromium/946505).

### lu...@chromium.org (2019-08-19)

(also, for renderer-initiated reloads, see https://bugs.chromium.org/p/chromium/issues/detail?id=968529#c19)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2a2a89d6e8d77d5488107d071983c1f66dd4c07e

commit 2a2a89d6e8d77d5488107d071983c1f66dd4c07e
Author: Lukasz Anforowicz <lukasza@chromium.org>
Date: Thu Aug 22 18:25:43 2019

Use navigation initiator for calculating the `Origin` header's value.

Before this CL, AddAdditionalRequestHeaders would set the Origin header
to either the destination origin (for main frame navigations) or to the
main frame's origin (for subframe navigations).  Both of these are wrong
and don't match Blink behavior (which correctly uses the initiator of
the navigation to calculate the Origin header's value).

Bug: 915538
Change-Id: Ied0262462f7665d0004da3b298bf0618ae312aec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1761051
Auto-Submit: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/master@{#689562}

[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/chrome/browser/tab_contents/view_source_browsertest.cc
[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/content/browser/frame_host/navigation_request.cc
[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/content/public/common/referrer.cc
[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/content/public/common/referrer.h
[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/net/test/embedded_test_server/default_handlers.cc
[modify] https://crrev.com/2a2a89d6e8d77d5488107d071983c1f66dd4c07e/third_party/blink/web_tests/external/wpt/fetch/origin/assorted.window-expected.txt


### lu...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-08-22)

I think we should consider this security bug fix for M77 / Beta (I guess the guidelines [1] are asking for a merge to M76 / Stable but it seems a bit too late / too risky for that)

[1] https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-medium-severity

### sh...@chromium.org (2019-08-22)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-08-23)

lukasza@ - please respond to C#42 to consider the merge request

### sh...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-08-23)

Hmmm... apparently r689562 is not yet included in a Canary - apparently 78.0.3891.0's branch_base_position=689468 :-(
I'll reply to https://crbug.com/chromium/915538#c42 and https://crbug.com/chromium/915538#c43 on Monday, once the change has been included in a Canary.

### la...@google.com (2019-08-24)

lukasza@ - thanks. would be good to pick this in next week's beta

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-08-26)

RE:  https://crbug.com/chromium/915538#c42, https://crbug.com/chromium/915538#c43: lakpamarthy@:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes - I believe that https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#TOC-Medium-severity asks to merge such security bugs to Beta (and to consider merging them to the Stable channel depending on the fix complexity).


2. Links to the CLs you are requesting to merge.

r689562


3. Has the change landed and been verified on master/ToT?

Yes - commit 2a2a89d6... initially landed in 78.0.3892.0


4. Why are these changes required in this milestone after branch?

This is a fix for a medium-severity security bug.


5. Is this a new feature?

No.


6. If it is a new feature, is it behind a flag using finch?

N/A

### la...@google.com (2019-08-27)

merge approved for M77 branch 3865

### lu...@chromium.org (2019-08-27)

While merging:
- I've checked that commit 435bcb58... initially landed in 77.0.3852.0 (this is the commit that introduced FrameNavigationEntry::initiator_origin).  The fix being merged depends on this commit.
- There was a merge conflict in //content/browser/frame_host/navigation_request.cc.  This seemed simple to resolve (just ensuring that the referrer policy is passed to AddAdditionalRequestHeaders) so I proceeded with the merge.  I'll try monitoring Beta builders for any problems.


### lu...@chromium.org (2019-08-27)

M77 merge landed in https://chromium-review.googlesource.com/c/chromium/src/+/1769110

### lu...@chromium.org (2019-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2019-08-28)

The following code that's overwritten in the fix appears to use the origin of the root frame rather than the initiator if there is no sandboxed origin. This seems incorrect. Can someone throw some light on what this code does? It seems odd that frame_tree_node->frame_tree()->root()->current_origin() would return the initiator frame, and not the root frame.

} else if ((frame_tree_node->active_sandbox_flags() &
              blink::WebSandboxFlags::kOrigin) ==
             blink::WebSandboxFlags::kNone) {
    // The origin should be the origin of the root, except for sandboxed
    // frames which have a unique origin.
    origin = frame_tree_node->frame_tree()->root()->current_origin();
  }

https://chromium-review.googlesource.com/c/chromium/src/+/1769110/2/content/browser/frame_host/navigation_request.cc#b283

### lu...@chromium.org (2019-08-28)

RE: https://crbug.com/chromium/915538#c53: tshadwell@:

Maybe clamy@ or arthursonzogni@ can shed some more light on the motivation/reasoning behind the old code mentioned in https://crbug.com/chromium/915538#c53.  To me it seems that the old code is incorrect.  FWIW, this old code comes from r437662 for https://crbug.com/chromium/648588.

I don't think any aspect of the old code needs to be retained in the new code (i.e. I don't think the new code has any missing parts or functionality problems).  In particular:
- There is no need to special-case based on |active_sandbox_flags| - the |initiator_origin| from the new code should already be taking into account sandboxing that might have been applied to the initiator
- I think it is never right to unconditionally look at the root frame - the Origin header should be based on the initiator (which might not be the root, top-level frame).

### be...@chromium.org (2019-08-29)

This has been approved, please merge ASAP.

### pa...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-08-29)

RE: https://crbug.com/chromium/915538#c55: benmason@:

It has already been merged (as pointed out in https://crbug.com/chromium/915538#c51).  Commit 8e4265b5... initially landed in 77.0.3865.56 according to OmahaProxy.  I am not sure why bugdroid hasn't picked this up yet (AFAICT the CL description does correctly refer to this bug).

### ar...@chromium.org (2019-08-30)

RE: https://crbug.com/chromium/915538#c54: Lukasz

Indeed, using the initiator_origin instead of the current main document URL looks better in my opinion (I won't guarantee you anything though)

The initiator_origin was not an existing concept 2 years ago, that's probably why the old code wasn't using it in the first place.

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### lu...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $500 for this report! 

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2019-11-21)

Can I disclose on this now? @lukasza

### lu...@chromium.org (2019-11-22)

adetaylor@, can you please answer the disclosure question from https://crbug.com/chromium/915538#c66?  AFAIU, the details of the bug shouldn't be disclosed until the bug has been fixed for ~14 weeks and the sheriffbot@ applies the "allpublic" label.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

Re https://crbug.com/chromium/915538#c66, https://crbug.com/chromium/915538#c67, discussed with awhalley@ and we think enough time has passed for this fix to have been absorbed by ~100% of users. Go ahead!

### sh...@chromium.org (2019-11-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/915538?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>Submission, Blink>SecurityFeature, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/926145]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093477)*
