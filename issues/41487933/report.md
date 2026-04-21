# Security: about:srcdoc session history entries leak document state cross-origin

| Field | Value |
|-------|-------|
| **Issue ID** | [41487933](https://issues.chromium.org/issues/41487933) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>History, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2024-01-03 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

It's possible to have two cross-origin parents with insufficient framing protections use the same session history entry when navigating history by using location.replace(). By creating a history entry in a subframe, then replacing the parent frame's active history entry with a different one (but still with a document containing an iframe\*), then calling history.back(), the history entry from the subframe of the previous page will be used to load into the iframe.

In particular, this means that if a victim page which is embeddable by an attacker page contains a srcdoc iframe, then it's possible for an attacker to load that history entry's document state into a subframe they control and, since an about:srcdoc URI inherits its origin from its embedder, read it as well. This could leak, e.g., document.baseURI (which is the unfiltered URL of the victim page embedding the srcdoc) and the CSP of the page.[1](http://attacker-d6bc41.ddns.net:8080/exp1.html)

Similarly, the reverse is possible. An attacker origin could apply malicious policies (e.g. CSP) that would be stored in the policy container of the session history entry of an about:srcdoc URI, or provide their own about base URI, then load this session history entry into a cross-origin page with an `<iframe srcdoc=...>`. The attacker CSP would override the srcdoc's original CSP, which could lead to a CSP bypass if the srcdoc content could be controlled.[2](http://attacker-d6bc41.ddns.net:8080/exp2.html)

Note that controlling the about base URI in a cross-origin srcdoc was already possible by navigating it to about:srcdoc, but applying a cross-origin CSP was not.[3](http://attacker-d6bc41.ddns.net:8080/exp3.html)

**VERSION**  

Chrome Version: 120.0.6099.130 + stable  

Operating System: Windows 11 Version 10.0.22621 Build 22621

**REPRODUCTION CASE**  

PoCs for each of the points above:

Please find all relevant files attached. Put all files into the same directory.

- In the 2nd PoC, the victim page inserts whatever is given in the "content" query parameter into the srcdoc. Note that usually any scripts would be unable to run, since the parent page has a strict CSP and the srcdoc inherits from the parent page.
- In the 3rd PoC, the victim page loads a script from a relative URL. If the victim expects this to load from their site, then an attacker can hijack the base URI to instead load from an attacker site, even with the base-uri CSP directive set. I'm not sure if this is expected behaviour. The same file `x.js` is used for both the attacker and victim sites for ease of reproducibility, but note that a victim would load their own `x.js`, and an attacker would upload a malicious script at the same path on their server.

\* A blob URI is used for this, but any same-origin page would work.

**CREDIT INFORMATION**  

Reporter credit: Harry Chen

## Attachments

- [exp1.html](attachments/exp1.html) (text/plain, 729 B)
- [exp2.html](attachments/exp2.html) (text/plain, 671 B)
- [exp3.html](attachments/exp3.html) (text/plain, 401 B)
- [victim1.html](attachments/victim1.html) (text/plain, 147 B)
- [victim2.html](attachments/victim2.html) (text/plain, 315 B)
- [victim3.html](attachments/victim3.html) (text/plain, 136 B)
- [redirect.html](attachments/redirect.html) (text/plain, 72 B)
- [x.js](attachments/x.js) (text/plain, 48 B)
- [exp2.html](attachments/exp2.html) (text/plain, 725 B)

## Timeline

### [Deleted User] (2024-01-03)

[Empty comment from Monorail migration]

### ha...@gmail.com (2024-01-03)

The last delay on PoC #2 may be too low, attached is it bumped up to 3000ms:

### ph...@chromium.org (2024-01-04)

[Empty comment from Monorail migration]

[Monorail components: Blink>History]

### [Deleted User] (2024-01-04)

[Empty comment from Monorail migration]

### ph...@chromium.org (2024-01-04)

creis@ Could you help triage this to the right owner?  Sorry if you're not the right person to ask.  I found you by searching "chrome history" on moma.

### cr...@chromium.org (2024-01-04)

Thanks for the report!  If we're using the wrong history item (FrameNavigationEntry) to put info from one origin into a different origin, that's certainly a concern.  I'll take a look to confirm, and can adjust the severity if needed.

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### [Deleted User] (2024-01-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2024-01-04)

Wow, this is a great find!  There appear to be several bugs which add up to a partial Site Isolation bypass, depending on what the victim URLs do.

The core problem is that NavigationController is incorrectly treating a location.replace in a subframe as kUpdate instead of kReplace.  This updates a shared FrameNavigationEntry in session history from one URL to another, rather than creating a new FrameNavigationEntry.  This makes us think the middle frame in the PoC doesn't need to be navigated when doing history.back().  Instead, we only navigate the innermost frame from about:blank to about:srcdoc.  That's a corruption of session history, which isn't great but might not be a terrible problem on its own.

After that, though, we have another bug that allows the about:srcdoc history navigation to commit in its parent frame's SiteInstance instead of the FrameNavigationEntry's SiteInstance (since we already had a record of the about:srcdoc document's origin and SiteInstance in session history).  Because of this, about:srcdoc loads with its previous parameters from the history item (CSP, base URI, etc) but in a different origin and SiteInstance.

We also should have caught this SiteInstance discrepancy in a few other places (e.g., CommitNavigation, RendererDidNavigate), making it result in a crash or a renderer kill, but that didn't happen.

I've verified that a quick fix to treat this case as kReplace instead of kUpdate disrupts the exp1.html and exp2.html attacks.  I'm a little surprised that exp3.html still works, but I might need to better understand what was meant by "controlling the about base URI in a cross-origin srcdoc was already possible by navigating it to about:srcdoc" in the report.

I'll post a more detailed writeup of the PoC behavior and the specific bugs in the code shortly.

First, I want to consider the severity.  If the attacker were able to run arbitrary script code in the victim's origin/process without mitigating factors, this would be a clear High severity Site Isolation bypass.  I was a little worried that this might be possible given that we put the srcdoc_value into commit_params at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;drc=72b07350427b6f4e7ba2e70b11bea6a4d8eaceb0;l=4112, where an attacker might be able to control the contents of the srcdoc frame.  At first glance, though, I'm not seeing a way to do that, because the srcdoc_value comes from the current FrameTreeNode and not the history item, and that value appears to only be controlled by the same origin as where the srcdoc ends up running.  I'm not 100% sure yet, so any evidence that this could be used to inject code into another origin would be useful.

Assuming that the attacker can't unilaterally run script in another origin due to this, it looks like the severity depends on what the victim URL does:

* In exp1.html, the victim page has (1) a srcdoc iframe, (2) no XFO/CSP-frame-ancestors, and (3) secrets in the base URI and CSP nonce which can be leaked to the attacker.  Leaking the full URL is probably mostly on par with an information leak like "A bug that allows an attacker to reliably read or infer browsing history" from https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md and would be Medium severity, though there are several mitigating factors (like the attacker doing the navigation to the victim, and not leaking arbitrary URLs the user visits).

* In exp2.html, the victim URL has 1) a srcdoc iframe, (2) no XFO/CSP-frame-ancestors, and (3) pulls content from the URL into the srcdoc relying only on CSP to block it.  That's a fair number of mitigating factors (and probably not all that common in practice) in order to get a CSP bypass, but then allows script execution in the victim origin.  The severity guidelines list a partial CSP bypass as Low; I could maybe see Medium due to the script execution.

* In exp3.html, the victim URL has 1) a srcdoc iframe, (2) no XFO/CSP-frame-ancestors, and (3) loads script from a relative URL without specifying its own base URL.  That might actually be possible to find in the wild and is perhaps the closest to allowing cross-origin script execution, though it's still somewhat mitigated.  I might call this Medium unless there's evidence that high profile sites would fall into this category, though I'm still curious about the comment that "controlling the about base URI in a cross-origin srcdoc was already possible by navigating it to about:srcdoc."  Is there a known issue for that?

I'll tentatively mark this as Medium as a result, and we can continue to discuss whether there are reasons to mark it High.

More specific details on the way.

### cr...@chromium.org (2024-01-05)

Ah, in retrospect it's obvious that my kReplace fix doesn't affect exp3.html, since that PoC doesn't use the location.replace + history.back() trick.  That appears to be an entirely separate bug where navigations to about:srcdoc are allowed, when they shouldn't be according to https://crbug.com/chromium/1169736.

As a result, a cross-origin about:srcdoc navigation is getting into a weird state, where the origin is not inherited from the initiator but the base URI is, while the content still comes from the parent frame's attribute (via the FrameTreeNode).  That behavior appears to have gotten worse with chrome://flags/#enable-new-base-url-inheritance-behavior (which wjmaclean@ added last year)-- if you disable that mode, the exp3.html PoC stops working because the base URI is not inherited.  That mode was meant to consistently inherit the origin and base URI together, but in this case it's causing us to inherit the base URI but not the origin.  And actually, inheriting both would be worse, since that would load the srcdoc_value from another origin into the initiator's origin, allowing a larger data leak.  So, at the least we need to not inherit the base URI in this case, and ideally we would block the navigation to about:srcdoc entirely.

dom@: Can we move forward with blocking about:srcdoc navigations in https://crbug.com/chromium/1169736, or are there any compatibility concerns?

(I'm also curious if this part should be split out into a separate bug, with the reporter getting credit for both discoveries.  We can continue to track fixes for both here if needed.)

### cr...@chromium.org (2024-01-05)

A few updates as I make progress...

----
Here's what's happening more specifically in exp1.html, and why Chrome gets it wrong:

1) The attacker document loads a victim document with a srcdoc frame: A(V(srcdoc_V)).

2) The attacker main frame navigates the innermost srcdoc frame to its own about:blank URL.
History is now: [A(V(srcdoc_V)), A(V(blank_A))*]
Note that the FrameNavigationEntry for V is correctly shared between the two NavigationEntries, so that minor changes (e.g., replaceState) affect both NavigationEntries (i.e., joint session history items).

3) The attacker main frame runs location.replace on the middle frame, with a new attacker URL containing a new about:blank subframe.
History should be: [A(V(srcdoc_V)), A(A2(blank2_A))*]
History actually is: [A(A2(srcdoc_V)), A(A2(blank2_A))*]
We should have stopped sharing the middle FrameNavigationEntry at this point, leaving the middle frame of the first NavigationEntry alone, by picking UpdatePolicy::kReplace at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;drc=67d90538f11c6b232dbfd716075db52aeb34fd15;l=2396.  Instead, we're updating the shared FrameNavigationEntry, which changes the first NavigationEntry as well.

4) The attacker page does history.back().
Since the first NavigationEntry looks like it already has the right items loaded for the main frame and middle frame, Chrome only navigates the innermost frame from blank_A to about:srcdoc.  It *should* be about:srcdoc in V's origin and process according to the FrameNavigationEntry, but Chrome actually loads it in the parent frame's origin and process (i.e., A).  However, V's base URI and policy container (e.g., CSP) are used from the FrameNavigationEntry, so those values are leaked to A.

Note that it's actually a good thing that Chrome didn't use V's origin and process, though, because the srcdoc_value comes from A2, and that would have allowed script injection from A into V.  Instead, we should enforce that the destination FrameNavigationEntry's origin and SiteInstance match the parent frame, and never allow them to differ (either crashing or causing a renderer kill if they do).

----
Cause of the location.replace bug:

We're picking kUpdate instead of kReplace in RendererDidNavigateAutoSubframe because was_on_initial_empty_document is true, which is incorrect at the time.  The frame is actually moving from V to A2, and V is not the initial empty document.  The bug happens at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigator.cc;drc=0c8ffbe78dc0ef2047849e45cefb3f621043e956;l=586, where we compute was_on_initial_empty_document *after* swapping in the new speculative RenderFrameHost (which thinks it is on its own initial empty document), which happens in RenderFrameHostManager::DidNavigateFrame a few lines higher at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigator.cc;drc=0c8ffbe78dc0ef2047849e45cefb3f621043e956;l=528.

This bug was introduced in https://chromium-review.googlesource.com/c/chromium/src/+/2953549, which added the only use of this was_on_initial_empty_document_value (for the location.replace computation).  Since it's not used for anything else, this particular bug shouldn't have additional implications.  The rest of the kUpdate vs kReplace code was added a bit earlier in https://chromium-review.googlesource.com/c/chromium/src/+/2910529.  Both of those CLs had tests, but apparently we forgot to include tests for the subframe replace case.

----
As a first change to disrupt the PoC, I've written https://chromium-review.googlesource.com/c/chromium/src/+/5172021, which moves the computation of was_on_initial_empty_document before the RFH swap (to get the right value) and includes a test.  Before landing, I want to look a bit closer to see if it's possible for an even earlier RFH swap to happen in this case (e.g., due to a crashed RFH, which would swap in the new RFH at the start of the navigation).

It's probably better to have the new RFH set is_initial_empty_document_ correctly, based on whether the FrameTreeNode has committed anything so far.  I might check with rakina@ about that.

Other changes in consideration:

* For exp3.html, blocking all about:srcdoc navigations apparently has compat issues for same-document cases (that arthursonzogni@ brought up in https://github.com/whatwg/html/issues/6316), but maybe we can block all cases that target another frame.  I'm chatting with Dom F about that.

* The browser process should catch the origin and SiteInstance discrepancies between the FrameNavigationEntry and the actual srcdoc navigation and cause either a renderer kill or a crash, since we shouldn't allow those to happen.

* We should more strongly enforce in the browser process that a srcdoc's origin and SiteInstance always match its parent frame's origin and SiteInstance, since the content comes from the parent frame.

I'll reiterate that it's great to get a report like this, which points out multiple bugs as well as areas for hardening.  Thanks!

### ha...@gmail.com (2024-01-06)

No problem, thank you for such a prompt fix and explanation! Please also cc + give reporter credit to Michael Guarino (guarinomi17@gmail.com)

### cr...@chromium.org (2024-01-08)

Thanks-- CC'd Michael for reporter credit.

### cr...@chromium.org (2024-01-08)

As a quick update, I've confirmed that the fix in https://chromium-review.googlesource.com/c/chromium/src/+/5172021 (PS1) doesn't quite work if the middle frame's renderer process crashes before the location.replace call.  As I suspected, that causes an early RFH swap, which makes it look like we're back on the initial empty document when committing the location.replace navigation.  It may not be super easy for an attacker to crash the middle frame's renderer process, but I'd like to avoid having this vulnerability in that case if possible.

Computing RFH's is_initial_empty_document_ more correctly would be ideal, but it's a little tricky for the initial fix since it poses more risk than I'd like.  I'm currently exploring a few options to see which one is the least risky.

### cr...@chromium.org (2024-01-08)

Hmm, part of the problem seems to have come from https://chromium-review.googlesource.com/c/chromium/src/+/3947845, which moved the initial empty document state from FrameTreeNode to RenderFrameHostImpl (for MPArch reasons in https://crbug.com/chromium/1179502).  That doesn't seem to have been a safe change, if it made it possible for the is_initial_empty_document value to go back to true for every new RFH in the FTN.  It's also somewhat non-trivial to fix while keeping the state on RFH, because that requires keeping multiple RFHs in sync (e.g., the current RFH and a speculative RFH).  I'll discuss with Rakina and Kevin to find a good short-term solution.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### cr...@chromium.org (2024-01-11)

Update: The first fix is going through the commit queue in https://chromium-review.googlesource.com/c/chromium/src/+/5172021.  That CL moves the initial empty document state back to FrameTreeNode to fix the location.replace issue in exp1.html and exp2.html.  It's less risky than I thought at first, given that it's effectively just a revert of r1074461 and going back to an earlier behavior.

That still leaves the bug in exp3.html, where base URI is being inherited from a cross-origin initiator frame.  I have a separate short-term fix in progress for that, which will avoid inheriting the initiator's base URI if the initiator isn't from the same origin as the parent (where the content comes from), taking into account precursor origins for sandbox cases.  That's just a temporary low-risk fix until we can block problematic about:srcdoc navigations in https://crbug.com/chromium/1169736.

We also met as a team to consider some additional lines of defense.  I'll post an updated list (compared to https://crbug.com/chromium/1515381#c10) once these initial fixes are in.

### gi...@appspot.gserviceaccount.com (2024-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/734db66cb259dd70f28566b21dd05efe11dee91d

commit 734db66cb259dd70f28566b21dd05efe11dee91d
Author: Charlie Reis <creis@chromium.org>
Date: Thu Jan 11 18:20:03 2024

Fix bug with computing was_on_initial_empty_document.

The previous code may have incorrectly computed true when not on the
initial empty document, if a speculative RFH was being committed. This
led to the wrong outcome for location.replace in a subframe, which is
the only place that this was_on_initial_empty_document value was used.

Instead, this CL moves the initial empty document state from
RenderFrameHost back to FrameTreeNode, where it lived before
https://chromium-review.googlesource.com/c/chromium/src/+/3947845. This
ensures that the value does not temporarily reset to true after each new
RenderFrameHost in the FrameTreeNode.

Bug: 1515381
Change-Id: I84624d89e9ee4796036b8e77124fd6567e1d619e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5172021
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1245966}

[modify] https://crrev.com/734db66cb259dd70f28566b21dd05efe11dee91d/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/734db66cb259dd70f28566b21dd05efe11dee91d/content/browser/renderer_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/734db66cb259dd70f28566b21dd05efe11dee91d/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/734db66cb259dd70f28566b21dd05efe11dee91d/content/browser/renderer_host/frame_tree_node.h
[modify] https://crrev.com/734db66cb259dd70f28566b21dd05efe11dee91d/content/browser/renderer_host/render_frame_host_owner.h
[modify] https://crrev.com/734db66cb259dd70f28566b21dd05efe11dee91d/content/browser/renderer_host/frame_tree_node.cc


### cr...@chromium.org (2024-01-12)

Update: exp1.html and exp2.html should be fixed by r1245966.  We're discussing the fix for exp3.html in https://chromium-review.googlesource.com/c/chromium/src/+/5188098, and I'll leave the bug open until that lands.

There's a separate set of hardening measures we can land, after those two CLs are in and the bug is marked fixed.

### gi...@appspot.gserviceaccount.com (2024-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/56cedcb362af51440fb4c1aa2b2fbdf5fe0be68c

commit 56cedcb362af51440fb4c1aa2b2fbdf5fe0be68c
Author: Charlie Reis <creis@chromium.org>
Date: Thu Jan 18 20:41:31 2024

Ensure that srcdoc documents do not inherit the wrong base URL.

The initiator's base URL should only be inherited if the initiator's
origin is also inherited.

Note that Chromium's current behavior is not spec-compliant, and allows
about:srcdoc navigations to inherit the wrong base URL. This CL
maintains the spec non-compliance in order to make a minimal change,
while fixing an associated security issue. Follow-up work in
https://crbug.com/1169736 will bring us into alignment with the spec by
disallowing about:srcdoc navigations in the cases that this CL affects,
altogether.

Bug: 1515381
Change-Id: Icb78224c7de58fe3f85b143c16bdb9a2ede4170e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5188098
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: W. James Maclean <wjmaclean@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1249009}

[modify] https://crrev.com/56cedcb362af51440fb4c1aa2b2fbdf5fe0be68c/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/56cedcb362af51440fb4c1aa2b2fbdf5fe0be68c/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/56cedcb362af51440fb4c1aa2b2fbdf5fe0be68c/content/browser/navigation_browsertest.cc


### cr...@chromium.org (2024-01-18)

Now that r1249009 has landed, exp3.html is also fixed, so I'll close this bug.  For VRP purposes, I would probably consider this as two separate Medium severity reports in the same issue, one involving session history corruption (fixed by r1245966) and one involving base URL inheritance (fixed by r1249009).

We'll continue to investigate a few hardening measures as followup:

* https://crbug.com/chromium/1169736: Block cross-document about:srcdoc navigations when the initiator origin does not agree with the parent frame's origin.  This is a more spec-compliant fix than r1249009, but it has higher compatibility risk so we wanted to eliminate the security issue first.

* https://crbug.com/chromium/1519641: Verify at navigation commit time that session history item's origin agrees with the origin that will be used unless a redirect occurs. This is aspirational, but it seems like we should be able to notice if we've picked the wrong origin when the session history item knows what origin it expects (and may have other things like base URL or CSP that are based on it).

* https://crbug.com/chromium/1519642: Verify at navigation did-commit time that the session history item's SiteInstance agrees with the one that was used, unless a different document committed (e.g., due to a redirect). This is also aspirational, but hopefully it can be another way to catch bugs like this.

* https://crbug.com/chromium/1519643: Delete all affected subframe FrameNavigationEntries when updating a shared FrameNavigationEntry to a different document.  We should not load subframe history items from a prior document into the new document.


### [Deleted User] (2024-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Harry! The Chrome VRP Panel has decided to award you a total of $8,000 for this report of the two separate issues you presented here-- $3,000 for an high-quality exploit mitigation bypass + $5,000 for a report of a high-quality exploit mitigation bypass with a functional exploit. While you didn't technically provide a full functional exploit your test case + details in your high-quality report combined presented enough evidence to fully demonstrate real-wold exploitability and the security impact. A member of our Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1515381?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>History, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

### gu...@gmail.com (2024-02-22)

Hi, I'm not sure who handles this but would it be possible to add my name to the release notes here per comments #12/#13? https://chromereleases.googleblog.com/2024/02/stable-channel-update-for-desktop_20.html

Thanks!

### am...@chromium.org (2024-02-22)

Hi, thanks for reaching out. I'll reach out to the release team about having this updated on the blog.

### pe...@google.com (2024-03-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### rz...@google.com (2024-03-12)

1. 2 CLs <https://chromium-review.googlesource.com/q/topic:%226099_41487933%22>
2. Low, no conflicts
3. 122
4. No, without any conflicts the CLs introduced an issue on an unrelated test, it's likely that the CLs interact badly with portals in 120.

### pe...@google.com (2024-04-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@gmail.com (2025-12-28)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41487933)*
