# Security: Possible to cause incorrect origin to be used when performing a same document navigation

| Field | Value |
|-------|-------|
| **Issue ID** | [40051596](https://issues.chromium.org/issues/40051596) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2020-02-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

It's possible for a window to perform a same document navigation between its original URL (e.g. a http/https URL) and about:blank. If another window within the same namespace navigates the first window to about:blank and then goes back, a same document navigation will be performed, though the origin will now have changed to that of the second window.

This allows, for example, a data: window to control another window whose origin is opaque (the same opaque origin as the data: window), but whose visible URL is the original (http/https) URL.

**VERSION**  

Chrome Version: Tested on 80.0.3987.116 (stable) and 82.0.4067.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Download the attached files into a directory, then run the following command:

python3 -m http.server 8080

2. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

3. Wait three seconds.
4. index.html contains two iframes: a data: iframe and an iframe pointing to <http://localhost:8080/iframe.html> nested within it.

Click within the innermost iframe. This should open a new window with a visible URL of <http://localhost:8080/iframe.html> and an opaque origin (that matches the origin of the data: iframe on the original page).

The data: iframe controls this window. To demonstrate this, it adds the following content to the new page:

Content set by data: iframe

This seemingly shouldn't be possible, as the data: frame has an opaque origin, one that's not the same as the origin represented by a <http://localhost:8080> URL.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 650 B)
- [index.html](attachments/index.html) (text/plain, 146 B)
- [main.js](attachments/main.js) (text/plain, 939 B)
- [New Tab - Google Chrome 2020-02-24 12-32-20.mp4](attachments/New Tab - Google Chrome 2020-02-24 12-32-20.mp4) (video/mp4, 2.8 MB)

## Timeline

### de...@gmail.com (2020-02-23)

Some explanation of that's happening:

The core issue here can be demonstrated fairly easily:

1. Load a page that has a data: iframe.
2. Within the context of the data: iframe, run the following code via the devtools console:

var newWindow = open("about:blank", "newWindow");
newWindow.history.pushState({}, "");

3. Switch to the context of the main page and run:

var newWindow = open("about:blank", "newWindow");
newWindow.history.back();

In this case, there are two history entries, both for about:blank. Navigating between them counts as a same document navigation. When the main page calls open in step 3, the origin of newWindow is changed from the original origin (which is an opaque data: origin) to the origin of the main page.

When the main page navigates newWindow back, that's counted as a same document navigation. So the origin is still that of the main page, though the visible URL might change.

In this specific case, there's not really an issue, because the visible URL is always about:blank.

However, in the first demonstration above, the original URL that's navigated back to is http://localhost:8080/iframe.html.

I believe the issue is that a same document navigation is performed, even if the origin of an about:blank page has changed. In both of the demonstrations above, an about:blank page is opened by one page, but when another page opens an about:blank page in the same window, the origin changes, yet the page still participates in same document navigations.

This won't work in cases where two non-opaque origins are involved, due to the following security check:

https://cs.chromium.org/chromium/src/content/renderer/render_frame_impl.cc?l=5230&rcl=a1988fdc920daffa1f882b71c552e0a675f0b5b0

There's some discussion of similar past issues in https://crbug.com/chromium/628677, which lead to that check being added.

Finally, it is possible to retain the https padlock in cases like these. That is, a data: frame that navigates a window back to a https URL will result in the https padlock being kept, if it was shown originally. This is because the padlock is retained in cases of same document navigation.

### aj...@google.com (2020-02-24)

Thank you for the report and initial analysis.

Adding my repro video from Canary.

Setting Low as this requires a click.

ahemery: assigning to you via blame but feel free to find another person to look at this.

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2020-02-24)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### [Deleted User] (2020-02-25)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2020-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ah...@chromium.org (2023-07-24)

I had written a small doc to try to understand what was going on: https://docs.google.com/document/d/1Irn9kiKVkiOaTWrHMeg2fZATETo2OatnlQll1IAcpKE/edit?usp=sharing. The fix did not seem trivial at the time.

### ah...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2023-09-14)

[Empty comment from Monorail migration]

### is...@google.com (2023-09-14)

This issue was migrated from crbug.com/chromium/1055145?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

### cr...@chromium.org (2025-01-08)

[Site Isolation triage]

This still seems to reproduce in 134.0.6944.0. Since ahemery@ has moved on, I'll try to find time to take a look.

### cr...@chromium.org (2025-01-10)

Thanks for the report! It does look like Blink is incorrectly reusing the same document sequence number on a cross-origin, cross-document navigation from about:blank (origin A) to about:blank (origin B), at least when it's in the same renderer process. That code is in [DocumentLoader::SetHistoryItemStateForCommit](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=1257-1265), which doesn't account for cross-origin cases, and thus reuses the document sequence number (and other state):

```
  // Don't propagate state from the old item if this is a different-document
  // navigation, unless the before and after pages are logically related. This
  // means they have the same url (ignoring fragment) and the new item was
  // loaded via reload or client redirect.
  if (navigation_type == HistoryNavigationType::kDifferentDocument &&
      (history_commit_type != kWebHistoryInertCommit ||
       !EqualIgnoringFragmentIdentifier(old_item->Url(), history_item_->Url())))
    return;
  history_item_->SetDocumentSequenceNumber(old_item->DocumentSequenceNumber());

```

As a result, a later back navigation will see that the document sequence number matches in NavigationControllerImpl::DetermineActionForHistoryNavigation [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=3557-3559) and treat it as same-document, even though the other details in the history item come from a different origin.

We definitely want to fix this, and can probably catch issues like it in a few places. Thankfully, there are several mitigations already that limit the security impact of the issue:

- This won't happen for any cross-process navigations, because of the SiteInstance comparison in DetermineActionForHistoryNavigation [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=3535-3537). That includes all cross-site navigations on desktop, or any for any isolated sites on Android, but won't catch any cross-origin cases that stay in the same process.
- Most same-process cross-origin cases will be caught when the back navigation commits, in [CanCommitOriginAndUrl](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/child_process_security_policy_impl.cc;drc=d15fd76ecbf7fb17bbe4e2833c7537c120d4e045;l=1845-1867) because the precursor tuple from the actual origin of the resulting document doesn't match the origin derived from the URL. For example, if the data: URL in the repro had come from a different origin (A) than the iframe.html URL (C) that gets shown in the address bar, then the data: URL has an origin precursor tuple of A which doesn't match C. That causes a renderer kill, such as <http://crash/2da26c8c95600517> (where A=`www.example.com` and C=`example.com`).
- If origin A distrusted the data URL enough to sandbox it, then this would become a cross-process sandboxed iframe case as of <https://crbug.com/510122> (launched in M124), and likely would not repro.

As a result, this spoof seems to be limited to cases where a non-sandboxed opaque origin (e.g., the data URL) can show content under the URL of the origin that created it. That's still a security issue that shouldn't be allowed, but I agree with the low severity rating, since the initiating origin generally has control over the data URL's contents anyway.

In two upcoming comments, I'll walk through the repro (since it's pretty clever and uses several tricks to get the URL to display), and then a set of suggested fixes to explore.

### cr...@chromium.org (2025-01-10)

The repro is fun, using the bug on an A(B(C)) page to get the innermost iframe into a state with origin B but with C's URL. Using that iframe, origin B can create a popup, inherit C's URL there using document.open, and display C's URL in the address bar using pushState.

As noted above, the other mitigations seem to mean that origin A must equal origin C, origin B is limited to an opaque origin derived from origin A, and all of them need to be in the same renderer process. That works if B is a data URL, and possibly only in that case.

Manual repro steps using simple test page URLs, in case you want to walk through by hand:

1. Visit <https://csreis.github.io/tests/cross-site-iframe.html>, which has an iframe with a data URL.
2. In DevTools Console for the data iframe B:
   `f = document.createElement("iframe"); f.src = "https://csreis.github.io/tests/cross-site-iframe-initially-blank.html"; document.body.appendChild(f);`

- This creates the C iframe, with its own about:blank iframe D.

3. In DevTools Console for the innermost about:blank frame D:
   `parent.document.open()`

- This causes iframe C to inherit iframe D's URL (i.e., about:blank), even though its origin is still `https://csreis.github.io`. This document.open trick is necessary so that the repro can navigate from about:blank to about:blank on different origins, while keeping a non-about:blank URL in this history item. (It also overwrites the contents of iframe C, so iframe D happens to be destroyed, but that doesn't matter for the outcome.)

4. In DevTools Console for the new about:blank iframe C:
   `location.hash = "1";`

- This creates a normal same-document history item on the about:blank document, which does two things. First, it lets us go back within the same document even though the next navigation will replace its current entry. Second, it preserves the original URL for iframe C (`https://csreis.github.io/tests/cross-site-iframe-initially-blank.html`) on the earlier history item, which will show up in the popup.

5. In DevTools Console for the data iframe B:
   `f.contentWindow.location.href = "about:blank";`

- This does a cross-document, cross-origin navigation in iframe C, replacing about:blank#1 on `https://csreis.github.io` with about:blank on the data URL's opaque origin (which has a precursor tuple of `https://csreis.github.io`).
- This is a replacement navigation because it looks similar to a same-URL or reload case. I think it's fine not to create a new history item here even when the origin does change, as long as we properly replace the old one.
- We should be using a new document sequence number here in the replacement history item, but the bug causes us to use the same one. Nothing goes wrong from that until we try to go back in the next step.

6. In DevTools Console for the data iframe B:
   `f.contentWindow.history.back();`

- Because of the incorrect document sequence number above, this does a same-document history navigation, leaving the origin as opaque but changing the URL to `https://csreis.github.io/tests/cross-site-iframe-initially-blank.html`. This is a bad state, but it's not yet visible to the user.

7. In DevTools Console for the data iframe B:
   `f.src = "javascript:w=window.open();w.document.write('from origin '+origin);w.history.pushState({}, '');"`

- Here, the data iframe runs script in iframe C, creating a popup.
- The document.write call (like document.open) causes the popup to inherit the URL of iframe C, though it isn't displayed in the address bar until the pushState call.

### cr...@chromium.org (2025-01-10)

Some proposed fixes to consider:

1. Use a different DSN on reload-like navigations that change origin, in [DocumentLoader::SetHistoryItemStateForCommit](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=1257-1265). I think this is the primary bug, though I'm not sure yet how to get to the origins we need to compare in Blink. (We can't just derive them from the URL; we need to get them from the previous document or history item, and from the destination, such as `origin_to_commit`). Hopefully dcheng@, rakina@, or japhet@ can help.
2. Treat cross-origin FrameNavigationEntry traverses as cross-document in FindFramesToNavigate (similar to the SiteInstance check [here](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=3535-3537). This would help avoid the bug even if Blink gets it wrong, and it's possible we could do this first while investigating how to do the origin check in Blink.
3. Possibly kill the renderer if it reports the same document sequence number as the current history item on a cross-origin navigation? That sort of collision shouldn't normally happen. We do have a defense against it in the cross-SiteIntance case, but it's probably worth verifying in the same-SiteInstance case.
4. Update the [SiteInstanceGroupsForDataUrls feature](https://crbug.com/40269084) to treat remote-to-local same-origin navigations as part of the data SiteInstance. This would have caused the data iframe's about:blank navigation in step 5 of the repro steps to be cross-SiteInstance, which should have prevented the back navigation from being treated as same-document.
5. Add a crash key to CanCommitOriginAndUrl to make it easier to diagnose the different reasons for `rfhi_can_commit_failure_reason=cpspi_disallowed_commit` reports, since there are several ways those can happen. That would have made it easier to spot reports of these tuple-mismatch cases in the wild.
6. I thought about trying to catch cases where an opaque data origin derived from A differs from the non-opaque origin derived from URL A (as part of the tuple checks in [CanCommitOriginAndUrl](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/child_process_security_policy_impl.cc;drc=d15fd76ecbf7fb17bbe4e2833c7537c120d4e045;l=1845-1867). This seems hard to distinguish from the case that a CSP sandboxed URL on origin A legitimately commits, though, since that also has an opaque origin whose precursor tuple matches URL A (which isn't opaque if you just look at the URL on its own).

Tangentially related things I noticed while investigating:

7. We should use kReplace in [RendererDidNavigateAutoSubframe](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=2474-2480) if the origin differs, not just if the URL differs.
8. DocumentLoader::SetHistoryItemStateForCommit should probably compare actual origins [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;drc=44a9b8bbbd2a5bd505c337808f774dcad56ce85c;l=1235-1241), not origins derived from URLs (which may not differ in the about:blank case).

### ap...@google.com (2025-01-29)

Project: chromium/src  

Branch: main  

Author: Charlie Reis <[creis@chromium.org](mailto:creis@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6181594>

Use cross-document history navigations for cross-origin about:blank.

---


Expand for full commit details
```
Use cross-document history navigations for cross-origin about:blank. 
 
If a same-process, cross-document navigation from about:blank to 
about:blank changes origins due to a different initiator, ensure that a 
back navigation is also considered cross-document. 
 
Bug: 40051596 
Change-Id: Ie8f6b2366ccb037393031c1cc35c88fb4449fad7 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6181594 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Charlie Reis <creis@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1413147}

```

---

Files:

- M `content/browser/renderer_host/navigation_controller_impl.cc`
- M `content/browser/renderer_host/navigation_controller_impl_browsertest.cc`
- M `third_party/blink/renderer/core/loader/document_loader.cc`

---

Hash: 71e4ae376a1c11b1ae8585451ee3af1909081880  

Date:  Wed Jan 29 13:37:57 2025


---

### ap...@google.com (2025-02-14)

Project: chromium/src  

Branch: main  

Author: Charlie Reis <[creis@chromium.org](mailto:creis@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6185347>

Do not reuse document sequence number on cross-origin navigations.

---


Expand for full commit details
```
Do not reuse document sequence number on cross-origin navigations. 
 
Cross-document navigations only reuse document sequence numbers for 
"logically related" navigations. This CL ensures that they are not 
reused for cross-origin navigations as well (e.g., about:blank with 
different owners), by computing this in the browser process and sending 
it in the CommitNavigationParams. 
 
Note that an exception is needed for error pages, which should preserve 
the document sequence number and other history item state, though they 
transition to and from an opaque origin with the same precursor. 
 
Bug: 40051596 
Change-Id: I502251ce12ec8b3e613596b914fbe8a63330b4fc 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6185347 
Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
Commit-Queue: Charlie Reis <creis@chromium.org> 
Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1420736}

```

---

Files:

- M `content/browser/renderer_host/navigation_controller_impl.cc`
- M `content/browser/renderer_host/navigation_controller_impl_browsertest.cc`
- M `content/browser/renderer_host/navigation_entry_impl.cc`
- M `content/browser/renderer_host/navigation_request.cc`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/renderer/render_frame_impl.cc`
- M `third_party/blink/public/mojom/navigation/navigation_params.mojom`
- M `third_party/blink/public/web/web_navigation_params.h`
- M `third_party/blink/renderer/core/loader/document_loader.cc`
- M `third_party/blink/renderer/core/loader/document_loader.h`

---

Hash: cdb798347ad78bcb1cffdbdc0e06eb1ec1867a57  

Date:  Fri Feb 14 14:04:46 2025


---

### cr...@chromium.org (2025-02-14)

The primary fixes have now landed and I've moved the other tasks from [comment #19](https://issues.chromium.org/issues/40051596#comment19) to [issue 396611141](https://issues.chromium.org/issues/396611141), so I'll close this bug.

For those proposed fixes:

1. Landed in <https://chromium-review.googlesource.com/c/chromium/src/+/6185347> (r1420736, will be in M135).
2. Landed in <https://chromium-review.googlesource.com/c/chromium/src/+/6181594> (r1413147, 134.0.6988.0).
3. Moved to followup issue.
4. Moved to followup issue.
5. Moved to followup issue.
6. Probably not worth pursuing, given the challenge from the CSP sandbox case.
7. Moved to followup issue.
8. Moved to followup issue.

### ph...@google.com (2025-02-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-03-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-13)

Congratulations David! Thank you for past efforts (almost five years back) and reporting this issue to us!

### ch...@google.com (2025-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051596)*
