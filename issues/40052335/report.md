# Security: Android WebView: iframe on different origin can execute arbitrary JavaScript in top document via window.open() or links with _blank target

| Field | Value |
|-------|-------|
| **Issue ID** | [40052335](https://issues.chromium.org/issues/40052335) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>WebView |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2020-05-18 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

An Android WebView instance with default configuration and JavaScript enabled allows an iframe on a different origin to bypass same-origin policies and execute arbitrary JavaScript in the top document.

To perform the attack, an iframe can call window.open() with a javascript: URL. That results in JavaScript from the iframe being executed in the context of the top document. Other methods of opening a new window, such as a link with target="\_blank" and href="javascript:...", result in the same behavior.

Due to user activation requirements, performing the attack requires a tap/click, focus, or other event within the iframe which results in a user activation consumable by window.open().

This behavior seems to occur if the WebView's WebSettings.setSupportMultipleWindows() option is set to false, which is the default value. Setting the value to true results in safe behavior.

When multiple windows support is false, WebView handles new windows with javascript: URLs in the same way as new windows with https:// URLs, which is to navigate the top document to the provided URL. This leads to JavaScript being executed in the top document context.

ADDITIONAL DETAILS  

I wasn't able to find any other crbug issues which indicate whether this behavior is or isn't intended for javascript: URLs. Luckily I was able to find a couple of issues with relevant discussion on adjacent behavior.

In <https://crbug.com/chromium/845983>, the report and discussion both indicate the top-level navigation behavior when calling window.open() with https:// URLs in an iframe is due to "legacy behavior". However, there is no mention of javascript: URLs or their different security impact.

Chrome on Android and Windows, and presumably on all other OSes, treats top-level navigation attempts by an iframe on a different origin as same-origin policy (SOP) violations. For reasons discussed in <https://crbug.com/chromium/845983>, this behavior is allowed in WebViews. However, it's unclear why the legacy behavior is maintained in WebViews, despite the behavior being actively prevented due to security concerns in other platforms.

Even if https:// URLs are intentionally allowed in order to maintain the "legacy behavior" (despite security concerns in other platforms), javascript: URLs should not be allowed to navigate the top-level document, because the security impact is greater than just unwanted navigation. If the legacy behavior is fully disabled, but an app wants to keep the legacy behavior for https:// URLs, the app can set WebSettings.setSupportMultipleWindows() to true and handle as desired via WebChromeClient.onCreateWindow().

The security concerns are also similar to those discussed in <https://crbug.com/chromium/1014371> with the scenario of executing JS in the parent document. In particular, the discussion establishes SOP applies in our attack scenario and different-origin iframes should not be able to execute JavaScript in the top-level document.

iframe sandboxing works as expected to prevent the attack. However, there are common configurations which still unexpectedly allow JavaScript from the iframe to execute in the parent document. For example, using sandbox="allow-popups allow-top-navigation allow-scripts" allows the attack to be performed by the iframe. Similar sandbox configurations may also allow the attack, but I have not tested them.

I discovered this behavior when pentesting over a dozen Android web browsers, and determined the cause was Android WebView behavior. A large amount of tested browsers are vulnerable. Surprisingly, many browsers which implement multiple tabs functionality are affected, because they often only allow new tabs to be opened via their UI (not by pages within the WebView), therefore they keep the Android WebView's multiple windows support setting at false. Many other browsers (with or without multiple tabs functionality) also use a popular third-party framework's WebView component which uses the default multiple windows support setting (I can provide the component name in a comment if desired).

**VERSION**  

Chrome Version: Android System WebView 81.0.4044.111 Stable, 83.0.4103.56 Beta, 85.0.4142.0 Dev, 85.0.5148.0 Canary  

Operating System: Android 10

**REPRODUCTION CASE**

I've attached a proof of concept (PoC) Android app with two common vulnerable WebView configuration scenarios and one safe Webview configuration scenario.

The remotely-hosted pages used by the PoC app are the same for all WebView configuration scenarios:  

<https://aogarantiza.com/chromiumwebview/window-open.html> - parent page  

<https://diff-origin.aogarantiza.com/chromiumwebview/window-open-iframe-js.html> - iframe page on different origin

Steps to reproduce with PoC app:

1. Open app
2. Tap iframe within a vulnerable-configuration tab

Expected behavior:  

JavaScript is not executed in top-level document. HTML is not written to top-level document and JS alert dialog is not shown (or a JS alert dialog is shown but with info from iframe document).

Observed behavior:  

JavaScript is executed in top-level document. HTML is written to top-level document, and if the WebView allows JS alert dialogs, a JS alert dialog is also shown.

To create your own basic PoC, roughly follow these steps:

1. Create an embeddable page with the JavaScript block or the anchor element below:

<script>
document.body.addEventListener('click', function () {
// Payload which writes to parent document and attempts to show JS alert (alerts are not guaranteed to be shown by WebView)
window.open('javascript:var elem = document.createElement("p");elem.innerHTML = "\*\*Executed JS in parent origin: "+window.location.origin+"\*\* "; document.body.append(elem);alert("XSS in doc.domain: "+document.domain+", win.origin: "+window.location.origin)');
// Simpler PoC payload if JS alerts are shown by WebView (not guaranteed to be shown)
// window.open("javascript:alert('Executed JS in target '+window.location.origin)");
});
</script>

<a href="javascript:EITHER\_PAYLOAD\_ABOVE" target="\_blank">Run PoC</a>

2. Create a parent page with an iframe which loads the step 1 page from another origin using either of these configurations:

<iframe src="https://DIFFERENT\_ORIGIN/iframe.html"></iframe>
<iframe src="https://DIFFERENT\_ORIGIN/iframe.html" sandbox="allow-popups allow-top-navigation allow-scripts"></iframe>

3. In an Android app, display a WebView with default configuration and JavaScript enabled:

class VulnerableActivity : AppCompatActivity() {  

override fun onCreate(savedInstanceState: Bundle?) {  

// ...other setup code...

```
    // Get WebView from layout  
    val myWebView: WebView = findViewById(R.id.webview)  
    // Enable JavaScript (only configuration required)  
    myWebView.settings.javaScriptEnabled = true  
    // Load parent page  
    myWebView.loadUrl("https://PARENT_ORIGIN/parent.html")  
}  

```

}

4. Run PoC app and interact with iframe

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [window-open.html](attachments/window-open.html) (text/plain, 786 B)
- [window-open-iframe-js.html](attachments/window-open-iframe-js.html) (text/plain, 1.5 KB)
- [window-open-poc-app.apk](attachments/window-open-poc-app.apk) (application/octet-stream, 2.8 MB)
- window-open-poc-app.zip (application/octet-stream, 135.3 KB)
- window-open.mp4 (video/mp4, 5.9 MB)
- window-open-cross-domain.jpg (image/jpeg, 359.4 KB)
- window-open-focus.html (text/plain, 1.4 KB)
- window-open-focus-iframe-js.html (text/plain, 2.8 KB)
- window-open-poc-app-v1.1.apk (application/octet-stream, 2.8 MB)
- window-open-focus.mp4 (video/mp4, 2.0 MB)

## Timeline

### ke...@chromium.org (2020-05-19)

Thank you for the thorough report. One question, first: Does it also work if the iframe is not a subdomain of the parent? Say, would this work as an XSS from host1.aogarantiza.com to host2.aogarantiza.com? I am just wondering if there is something funny going on with document.domain.

Adding rsesek@ for FYI. I don't have a non-corp device to verify this on but would appreciate any thoughts.

[Monorail components: Mobile>WebView]

### ke...@chromium.org (2020-05-19)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2020-05-19)

Yes, it works even across domains. Screenshot attached with parent page loaded from alesandroortiz.com and iframe page loaded from diff-domain.aogarantiza.com.

### al...@alesandroortiz.com (2020-05-19)

(The parent page URL is https://alesandroortiz.com/~aor/security/chromiumwebview/window-open.html in case someone wants to use it in their own PoC app or wants to update the provided PoC app.)

### [Deleted User] (2020-05-19)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2020-05-20)

rsesek@ would you be able to help triage this? I haven't verified it but it is potentially fairly serious.

### rs...@chromium.org (2020-05-20)

Routing to Torne from WebView.

### to...@chromium.org (2020-05-20)

I'll verify this but it sounds like a real and serious issue - I'm familiar with the weird multiple window behaviour of WebView that exists for legacy reasons as the reporter mentions, and I would not have expected this to work for javascript: URLs. When multiple window support is disabled we do indeed just convert all popup opens into top navigations, it just shouldn't allow this to happen for javascript:

### to...@chromium.org (2020-05-20)

Incidentally our recommendation for apps is to *always* enable multiple window support in WebView to avoid this legacy behaviour entirely. Apps that don't actually want to allow popup windows should *still* enable it, and then just return null from the onCreateWindow callback when it's invoked - we treat this like the popup was blocked by a popup blocker or similar. So, while we should definitely still fix this bug, the browser apps the reporter mentioned should ideally also change their implementation to prevent other potential problems caused by this surprising compatibility behaviour :(

### to...@chromium.org (2020-05-20)

Yep, confirmed this bug :(

I think it should be straightforward to fix.

### ke...@chromium.org (2020-05-20)

Thanks for verifying!

I'm tentatively flagging this as Security_Severity_Medium. SOP bypasses are bad but this requires specific preconditions to be a problem.

### to...@chromium.org (2020-05-20)

As the reporter notes this is the default configuration of WebView, and it's likely that the majority of WebView apps don't change this setting (though I haven't done an analysis on this). This probably isn't a regression, though - I would guess it's always been like this :(

### ke...@chromium.org (2020-05-20)

The particular precondition is that it involves a well-intentioned app to load a well-intentioned page in a WebView that then iframes a malicious page. The only scenario I can think of where this would happen is if a page in a WebView is loading display ads.

### to...@chromium.org (2020-05-20)

Unfortunately that also includes any case where apps load arbitrary 3P content at all (i.e. behaving like a browser), not just cases where their 1P content iframes 3P content without sandboxing :/

### al...@alesandroortiz.com (2020-05-21)

Thanks for the triage and additional context.

While the original PoC only works for visible iframes due to the tap/click requirement, an alternate method uses stolen keyboard events which allows both visible and hidden iframes to also exploit this vulnerability, as long as the iframes are not hidden via display:none (prevents receiving focus for keyboard events).

Using behavior described in https://crbug.com/chromium/622714 (repros in Stable through Canary), a hidden iframe can steal keyboard input focus from the top document. If the iframe steals the focus while the user is typing on the keyboard, the iframe can easily steal the single keyboard event required to obtain user activation, which can immediately be used to exploit this vulnerability.

Hidden iframes can only use the keyboard method. However, the ability to launch attacks from hidden iframes significantly increases the number of potential website targets due to their more widespread usage and ability to steal user activations with minimal cooperation (if you can call it that) from the user.

Visible iframes can also use the keyboard method alongside the click method to increase the attack launch surface.

The keyboard PoC uses a couple of techniques to reduce discoverability and increase chances of success, which makes widespread attacks more feasible for a determined attacker. For example, an iframe can detect when a user is likely typing or about to type in the top document, and time the focus theft more precisely so the user is less likely to realize their selected input field lost focus while they keep typing. After performing the attack, an iframe can also release the stolen focus, making it seem like an accidental loss of focus, to further reduce discoverability. (See the source code comments for more details on these techniques.)

For click user activation scenarios, in addition to display/video ads, other common scenarios where visible 3P iframes are likely to obtain a click user activation by mobile users include: video players, in-page chat, comment forms/display, share buttons, documents, and contact/survey forms. If the 3P is unscrupulous or has a stored XSS vuln within the iframe, an attack seems realistic, affecting users of vulnerable browsers/WebViews who browse sites with these 3P iframes. Any of these can also combine the keyboard method for increased effectiveness.

I've attached an updated PoC app APK which loads the keyboard PoC page under the tab "Vulnerable 1 crbug 622714". The remotely-hosted version of the pages are:
https://aogarantiza.com/chromiumwebview/window-open-focus.html - parent page
https://diff-origin.aogarantiza.com/chromiumwebview/window-open-focus-iframe-js.html - iframe page on different origin (hidden in the parent page)

Steps to reproduce with PoC app v1.1:
1. Tap the "search this site" input field to focus it. (This input field is in the parent page, not the iframe.)
2. Start typing. Before/while you type, the focus will be stolen by the iframe. (This can be made more subtle by delaying the focus theft, see code comments.)
3. After typing a character while the iframe input is focused, the attack is immediately performed with the same payload as the original PoC.

### al...@alesandroortiz.com (2020-05-21)

Regarding https://crbug.com/chromium/1083819#c9, is the recommendation and legacy behavior documented anywhere public? These Android docs don't seem mention anything about legacy behavior or potential pitfalls with iframes performing top-level navigations when it's kept at false/default:

https://developer.android.com/reference/android/webkit/WebSettings#setSupportMultipleWindows(boolean)
https://developer.android.com/reference/android/webkit/WebChromeClient#onCreateWindow(android.webkit.WebView,%20boolean,%20boolean,%20android.os.Message)
https://developer.android.com/reference/android/webkit/WebView

In the future, as I find browsers with the iframe framebusting behavior, will be helpful to know where to point vendors to other than this issue once it becomes public.

### al...@alesandroortiz.com (2020-05-29)

Couple more details on attack launch surface:

I've verified attacks can be launched from any iframe regardless of nesting depth. This means if the malicious iframe is nested within 5 other iframes, window.open() will still execute code at top level if the malicious iframe five levels deep obtains user activation. The keyboard focus theft attack also works at any nesting depth. Attack launch is possible even in an attacker's worst-case scenario where each iframe is on a different origin. e.g. top level is example.com, iframes are on exampleiframe1.com, exampleiframe2.com, exampleiframe3.com, etc.

Also verified that if an ancestor iframe receives activation, child iframes on the same origin will also receive activation. This is due to expected UAv2 behavior. However, the behavior can be used to activate the malicious iframe while interacting with an apparently safe iframe. This allows for easier obfuscation since the malicious code doesn't need to reside in the iframe which receives the click/tap/keypress. e.g. top level is example.com, all iframes on exampleiframe.com. Or alternatively, first iframe is exampleiframe1.com, second iframe is exampleiframe2.com, third iframe is exampleiframe1.com, if first iframe receives activation, third iframe will also receive activation.

### to...@chromium.org (2020-06-01)

ctzsm@ will take a look at implementing the fix and regression tests.

### to...@chromium.org (2020-06-01)

We need to change the WebView special case in RenderFrameHostImpl::CreateNewWindow so that it only returns a status of kReuse for "real" URLs and not javascript: - javascript: should just kIgnore instead. That's pretty simple, but we need a test to cover this and we don't appear to currently have any tests in Chromium for the no-multiple-windows behaviour at all, though we do have some in CTS I think.

### to...@chromium.org (2020-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-01)

ctzsm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2020-06-01)

Thanks torne@ for the suggestion, I think that's the right way to fix this. We actually filtered out `javascript: ` and other invalid scheme and replace the URL with `about:blank` (kBlockedURL) before the WebView special case, so I think we should just check against kBlockedURL to call the callback on kIgnore.

On the other hand, the test case is not very easy to write; Currently I am thinking to write the test in a_w/ directory since this is a WebView special case, this is also easier for us to demonstrate the issue is with setSupportMultipleWindows(false).

### ct...@chromium.org (2020-06-03)

+ jochen@ for the context.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8a50f446de0f738643adcb199b4c059445574688

commit 8a50f446de0f738643adcb199b4c059445574688
Author: Shimi Zhang <ctzsm@chromium.org>
Date: Thu Jun 04 00:50:52 2020

[WebView] Fix single-window-mode JS injection

- Check if the |target_url| is |kBlockedURL|, if true, call the callback
  with |kIgnore.|
- Add regression test.

Fixed: 1083819
Change-Id: I56bde76b749efa2dcaf9b3e178ace94b43aa9faf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2226496
Commit-Queue: Shimi Zhang <ctzsm@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Richard Coles <torne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#774907}

[modify] https://crrev.com/8a50f446de0f738643adcb199b4c059445574688/android_webview/javatests/src/org/chromium/android_webview/test/PopupWindowTest.java
[modify] https://crrev.com/8a50f446de0f738643adcb199b4c059445574688/content/browser/frame_host/render_frame_host_impl.cc


### to...@chromium.org (2020-06-04)

Do we want to merge this to 84?

### ke...@chromium.org (2020-06-04)

+adetaylor@ for question in https://crbug.com/chromium/1083819#c25.

This is a UXSS with some specific preconditions. I flagged as Sev-Medium but it arguably could be Sev-High.

### ad...@chromium.org (2020-06-04)

Thanks for the ping.

I think I'll uprate this to severity high. Malicious ads are a significant reason for site isolation in the first place, so I think this probably rates as a high.

Yes - we should merge to M84 and very probably back to the next M83 refresh too.

I'll add the merge request labels. Sheriffbot will ask some questions about why a merge is justified, which are not terribly useful. But what _would_ be useful - torne@ and/or ctzsm@ - is whether you feel this has any risk of change to legitimate use-cases. We are very nervous about merging back potentially breaking changes to the current stable milestone. And other commentary on the wisdom of backmerging to M83 is also appreciated!

### [Deleted User] (2020-06-04)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2020-06-04)

It should not be possible to trigger this exploit in a sandboxed iframe without allow-top-navigation due to the fix for https://crbug.com/chromium/845983 (just having allow-popups is not sufficient). Ads use cases generally should not allow top navigations (for a number of reasons, but especially in WebView where apps don't necessarily show the top level document URL anywhere and so top navigations can easily mislead users), so if they're sandboxing their iframes appropriately they should be safe even if WebView is in single-window mode. I don't know how common the vulnerability is going to be.

It's not *entirely* out of the question that someone might have been depending on this behaviour, but if they are it's likely by accident; it doesn't really make any sense for a developer to expect that window.open("javascript:foo", "_blank") is going to execute in the top frame.

The fix as implemented does not consider whether the iframe is cross-origin or not, and blocks this even for same-origin iframes. If the iframes are same-origin then it's trivial for them to communicate other ways that actually work outside of WebView too, so the developer really shouldn't have been depending on this. If we were really worried about the compat impact here I guess we could make it only block it for cross-origin frames but that seems like a very weird special case to add to what's already an extremely weird feature, and I'd rather not :/

### ct...@chromium.org (2020-06-04)

I think in general we wait a canary build to verify the fix before cherry-pick, but we didn't make yesterday's canary. With torne@'s https://crbug.com/chromium/1083819#c29, I personally think merging it back to M84 is reasonable but isn't super necessary for M83.


I'll just answer the required questions from sheriffbot, but govind@, please review the recent comments as well:

1. Does your merge fit within the Merge Decision Guidelines?
Yes
2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2226496
3. Has the change landed and been verified on master/ToT?
Verified on master/ToT.
4. Why are these changes required in this milestone after branch?
Security bug fix.
5. Is this a new feature?
No.
6. If it is a new feature, is it behind a flag using finch?
N/A

### [Deleted User] (2020-06-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-04)

OK, approving merge to M84 (branch 4147). Could you wait for a day to ensure there are no unexpected problems from Canary first.

The default for a high severity security bug (or even externally-reported medium severity bugs) _is_ to merge back to the current stable release (M83) unless there's a good reason why not. The compatibility implications seem negligible, so we may well merge this back, but let's wait for the fix to bake a bit first.

### ct...@chromium.org (2020-06-05)

Verified on 85.0.4165.0, used the test app from alesandro@. I'll cherry-pick this fix to 4147.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7be3e6e76090c48c03993b7c9bc56d85130230d1

commit 7be3e6e76090c48c03993b7c9bc56d85130230d1
Author: Shimi Zhang <ctzsm@chromium.org>
Date: Fri Jun 05 18:44:34 2020

[WebView] Fix single-window-mode JS injection

- Check if the |target_url| is |kBlockedURL|, if true, call the callback
  with |kIgnore.|
- Add regression test.

(cherry picked from commit 8a50f446de0f738643adcb199b4c059445574688)

Fixed: 1083819
Change-Id: I56bde76b749efa2dcaf9b3e178ace94b43aa9faf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2226496
Commit-Queue: Shimi Zhang <ctzsm@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Richard Coles <torne@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#774907}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2232819
Reviewed-by: Shimi Zhang <ctzsm@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#490}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/7be3e6e76090c48c03993b7c9bc56d85130230d1/android_webview/javatests/src/org/chromium/android_webview/test/PopupWindowTest.java
[modify] https://crrev.com/7be3e6e76090c48c03993b7c9bc56d85130230d1/content/browser/frame_host/render_frame_host_impl.cc


### ct...@chromium.org (2020-06-08)

+ satyavathir@ for testing purpose.

### ct...@chromium.org (2020-06-08)

Verified on 84.0.4147.39. 

### ad...@chromium.org (2020-06-08)

How's this looking in Canary? Assuming no problems, I am approving merge to M83 (branch 4103).

### ct...@chromium.org (2020-06-09)

Verified it on canary, see https://crbug.com/chromium/1083819#c33.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2002e2f5617a8a17f58d21c921e38c5ca0799311

commit 2002e2f5617a8a17f58d21c921e38c5ca0799311
Author: Shimi Zhang <ctzsm@chromium.org>
Date: Tue Jun 09 19:03:29 2020

[WebView] Fix single-window-mode JS injection

- Check if the |target_url| is |kBlockedURL|, if true, call the callback
  with |kIgnore.|
- Add regression test.

(cherry picked from commit 8a50f446de0f738643adcb199b4c059445574688)

Fixed: 1083819
Change-Id: I56bde76b749efa2dcaf9b3e178ace94b43aa9faf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2226496
Commit-Queue: Shimi Zhang <ctzsm@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Richard Coles <torne@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#774907}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2236928
Reviewed-by: Shimi Zhang <ctzsm@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#675}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/2002e2f5617a8a17f58d21c921e38c5ca0799311/android_webview/javatests/src/org/chromium/android_webview/test/PopupWindowTest.java
[modify] https://crrev.com/2002e2f5617a8a17f58d21c921e38c5ca0799311/content/browser/frame_host/render_frame_host_impl.cc


### al...@alesandroortiz.com (2020-06-09)

Thanks all for getting this fixed quickly, glad it'll be out on stable fairly soon.

Also verified on WebView Canary 85.0.4166.0 using my PoC app and a previously-affected third-party browser.

Will this vuln be assigned a CVE ID?

After this issue is made public in ~14 weeks, I plan to submit fixes to at least one open source library used by many browsers to fix the WebView config (per https://crbug.com/chromium/1083819#c9) for unpatched WebView users. A CVE ID will be helpful when communicating with library maintainers and browser vendors.

### to...@chromium.org (2020-06-09)

You could just reference https://crbug.com/chromium/845983 in support of changing the config in libraries/apps - this is unfortunately not the first time this ancient webview compatibility feature has had a security issue, and that one is already public.

I'm curious what library you're referring to; I'm not aware of a common library used by webview browsers, and I would guess that this is not the only suboptimal configuration setting in it, since WebView's defaults are very old and have lots of issues. :(

### al...@alesandroortiz.com (2020-06-09)

Thanks for suggestion to reference the other issue. Will consider doing so for the widely-used library to patch on their end before this becomes public.

However, for browser vendors will wait and reference this issue directly once it becomes public, if no CVE is issued. (Have had recent negative experiences reporting similar top-level nav from iframe vulns to some browser vendors, so doubt they'll see the other crbug issue as a vuln. Hopefully they do recognize a SOP bypass/UXSS issue as a vuln.

### al...@alesandroortiz.com (2020-06-09)

[Comment Deleted]

### ad...@chromium.org (2020-06-10)

Hi Alesandro, we'd definitely expect to issue a CVE number for this as soon as it's released, which (given its merge status) will likely be within 2 weeks and certainly within 6.

This bug is already visible to downstream browser vendors and embedders of Chromium. I'm not sure if you were aware of that with comment https://crbug.com/chromium/1083819#c43. I've marked this as Restrict-View-SecurityEmbargo which will remove visibility to those folks.

### al...@alesandroortiz.com (2020-06-10)

Hi adetaylor@, thanks for info. Will look out for CVE ID when it happens, no rush.

I wasn't aware of it was visible outside of sec team, apologies (now noticed view label is SecurityNotify, not SecurityTeam). I'll leave https://crbug.com/chromium/1083819#c43 up only as long as it's useful for discussion, so SecurityNotify folks can regain visibility sooner than later.

### al...@alesandroortiz.com (2020-06-11)

[Comment Deleted]

### al...@alesandroortiz.com (2020-06-11)

Since this is the first wide-impact cross-vendor vuln I've found, I'm facing unfamiliar complexities in notification procedures.

Based on https://crbug.com/chromium/1083819#c43 and https://crbug.com/chromium/1083819#c46, I have a request for advice:

1. Should the framework vendors (and some app vendors) be notified after issue is public in ~14 weeks, or should they be notified earlier with clearance from Security Team? (Again, doubt many vendors will respond appropriately if I only reference https://crbug.com/chromium/845983 based on its limited impact.)

2. After the date set by prior answer: Should I notify the vendors myself via their VRPs/security contacts, or does the Chrome Security Team prefer another process? I prefer to notify due to potential rewards, but open to suggestions.

### al...@alesandroortiz.com (2020-06-11)

https://crbug.com/chromium/1083819#c47 assumes notification to vendors is warranted, since there is an actionable to mitigate for unpatched WebView users. If no direct notification is warranted, also let me know.

### ad...@google.com (2020-06-11)

Hi Alesandro, it's completely fine to notify those vendors now; please go ahead. It's also OK to cc folks from those vendors onto this crbug, so they can see the details. Our goal is obviously to stop people _using_ this bug to exploit folks until it's widely fixed so we don't want to make it public, but it's perfectly fine to cc people with a legitimate need-to-know.

### na...@google.com (2020-06-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-11)

Congrats! The Panel decided to award $15,000 for this report! 

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2020-06-11)

Panel: Thanks for the significant reward, appreciate it!

adetaylor@: Thanks for clarification. I'll notify affected framework vendors and trustworthy app vendors as soon as possible. Will provide them a tailored report with vulnerability details from this issue. (If they request, will cc them here.)

Hopefully mitigation in frameworks and apps will help prevent in-the-wild exploitation for unpatched WebView users.

### to...@chromium.org (2020-06-11)

Well it's not just a mitigation for this issue but also a fix for bad UI in general - no other browser handles popups by overwriting the current tab with the popup contents, and I suspect likely to be weird/confusing to users more often than it is helpful. As I said, browser-like apps should *always* enable multiple window support, and if they lack the ability to open an actual popup or new tab or similar browser-like UI (with some kind of URL display showing the user where the popup/tab originates from) they should just block it entirely by returning null from onCreateWindow.

The ancient compatibility behaviour with multiple window support disabled is, as far as I know, intended for use cases where apps are using WebView to show simple, mostly static web content like help/support/terms-and-conditions pages, and the content on the page may use links with target="_blank" intended to open in new tabs for real browsers; redirecting those to top navigations means that those links aren't simply broken in this context and the user can actually read them. For this use case to be secure the app needs to be blocking all navigations to URLs outside of the domain(s) it trusts, multiwindow or not, because the URL is not usually displayed to the user and thus being able to navigate to a 3P page at all is a phishing/etc risk.

That's the only two choices really as far as I'm aware: either your app is intended to be able to render arbitrary 3P content like a browser, in which case it should enable multiwindow, handle/block popup requests explicitly, and show URLs in a trustworthy way; or it's intended to only render trusted 1P content, in which case it should whitelist navigations (and what it chooses to do with multiwindow/popups is much less important as a result).

### ad...@google.com (2020-06-12)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-12)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2020-06-17)

adetayor@: Thanks for CVE ID. I see fix is now on 83.0.4103.106 Stable, which is great! (Also verified fix on Stable)
https://chromereleases.googleblog.com/2020/06/stable-channel-update-for-desktop_15.html

torne@: Let me know if https://crbug.com/chromium/1083819#c43 and https://crbug.com/chromium/1083819#c46 are good to delete (if you've read them already). Otherwise will delete them by EOD Monday.

Thanks for additional context, especially around legacy behavior use case. Agree the fix will also help with inconsistent/bad UI in browsers. We're on the same page there.

Hopefully all browser vendors (not using frameworks) see it the same way and opt for the first choice you provided (enable multiwindow, etc). I'm not too worried about browser vendors since their use case is well-defined and constant, therefore their choice is clear. Any concerns should be addressable and probably won't outweigh security concerns.

However, both options are difficult for framework vendors to adopt. They don't necessarily know how their WebView will be used. They would need to choose a default behavior, allow developer override, and document accordingly. To prevent breaking changes, there's a good chance they will prefer to keep legacy behavior over blocking new windows as default behavior. With only those two options, this means keeping multiwindow off but risk making implementing apps vulnerable to this UXSS (for unpatched WebView users). This also allows phishing as you mentioned.

For those frameworks (and reluctant browsers), a third option is to enable multiwindow and then mimic old behavior, with optional origin filtering. They can implement this by obtaining the new window URL via a temporary WebView with shouldOverrideUrlLoading() which returns false, and calling loadUrl() with the obtained URL in the existing WebView. This would replicate legacy behavior while preventing JavaScript URLs and non-allowed origins from being unsafely loaded. It's messy, but so is anything related to legacy behaviors in any software.

A quick test indicates only HTTP(S) URLs result in a shouldOverrideUrlLoading() call, which is sufficient to mitigate UXSS in implementation above. Optional origin filtering should still be implemented in no-URL-display situations to mitigate phishing risk as you indicated, and as defense in depth against UXSS if shouldOverrideUrlLoading() behavior changes. I suspect this will be the preferred option for frameworks despite additional complexity, since it solves both UXSS and phishing concerns while minimizing breaking changes.

I'll provide a summary of your suggestions plus third option in the vendor security reports, which will go out to identified vendors starting tomorrow (Thursday). Thanks again for distilling the choices.

### to...@chromium.org (2020-06-17)

I've read the comments and you can delete details if necessary - thanks.

Your third option seems potentially fragile/easy to get wrong, but may be okay? One thing I'd note is that you would want to return *true* from shouldOverrideUrlLoading so that the temporary popup webview doesn't actually load the page - there's no need to load it there if you're going to load it again in the main webview, and some sites might break if you load it twice (e.g. poorly implemented session management that's trying to prevent users using the back button). For the cases where shouldOverrideUrlLoading is *not* called as you mention, it's unclear what you can really do - you would have to just.. wait for some timeout and then destroy the WebView I guess? Seems pretty gross.

If somebody really needs to be able to handle popup links and doesn't want to actually render a popup/tab UI then nothing stops them from just attaching the newly created WebView directly to the same view hierarchy as the parent WebView - I've seen a number of code examples where people do this and set it to the same layout parameters as the parent, which means it literally just draws over the top of it and covers the parent completely. This has the same security UX issues as any other kind of popup regarding showing the URL etc and should probably only be allowed if there's a URL whitelist; I mention it just to be clear that there isn't any strict need to actually design a popup UX to implement this.

### to...@chromium.org (2020-06-17)

My general advice to frameworks using WebView, even unrelated to this bug, would be to always use an origin whitelist and default to only allowing trustworthy non-network URLs (e.g. data: URIs since these would be supplied by the app or generated as a result of the loadData() API, or the magic file:///android_asset/ and file:///android_res/ URLs for loading app content from the APK). You could still allow the app to explicitly set a "whitelist" that's just a wildcard allowing anything, but the developer probably should have to do this explicitly rather than it being the default. Mandatory origin whitelists are the approach we're taking with new WebView APIs that need any kind of security filtering.

### al...@alesandroortiz.com (2020-06-18)

Comments with vendor identification deleted. (adetaylor@ or anyone else, feel free to remove view embargo if desired.)

Thanks for correction, return false was typo in comment. In my test implementation, shouldOverrideUrlLoading() returns true to prevent unnecessary loading.

For scenarios where shouldOverrideUrlLoading() is not called, it's a minor implementation detail and doesn't directly affect user experience. As you said, the app can destroy the temp WebView after a timeout, or lazily destroy the old temp WebView right before handling the current onCreateWindow() call (which is what my test implementation does).

Appreciate the fourth option of new WebView on top of old WebView; will offer it to vendors too. I've seen this approach in production apps as well. It's definitely cleaner and easy to implement for some vendors. For other frameworks which assume one Android WebView instance per Framework WebView instance, it can still be a complex fix in order to not break framework behavior dependent on that assumption. It also might still introduce smaller breaking changes to implementing apps. But overall a better option, so will recommend this fourth option over the third option.

(For anyone reading this in the future, if you use this fourth option, please destroy the bg WebView/unload the bg page or ensure bg events are handled safely. Otherwise you'll allow bg pages to perform actions which should only be allowed by foreground pages, which often cause other security issues. Have seen this pitfall too many times in production apps.)

For frameworks which don't use origin whitelists by default and don't address it while mitigating this issue, based on https://crbug.com/chromium/1083819#c59, I'll consider filing separate security reports at a later point. Thanks again for the public documentation, torne@. Will be useful in the future to refer vendors to your comments.

### to...@chromium.org (2020-06-18)

I suspect pushing everyone to whitelist origins is going to be a long uphill struggle since that's a pretty dramatically incompatible change, and if it just broke apps using a framework developers might be inclined to just turn the restriction off to fix it. I think we'd be interested in working with framework developers on this kind of thing, though.

Ideally we would provide an implementation of whitelisting to help developers get the details right; I've filed https://crbug.com/chromium/1096714 to discuss that potential feature.

### ad...@google.com (2020-06-18)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2020-07-09)

Can I submit this vulnerability to the Google Play Security Reward Program? https://www.google.com/about/appsecurity/play-rewards/

It may qualify under the "theft of sensitive data" and SDK/library rule.

### na...@google.com (2020-07-09)

Hi - You can submit it through their program but will have to follow their process as the programs are not linked. 

### al...@alesandroortiz.com (2020-07-09)

natashapabrai@: Thanks! Understood. Will submit to the GPSRP program in the coming days.

### al...@alesandroortiz.com (2020-07-20)

adetaylor@: An affected vendor has requested access to this crbug. F-Secure's security team provided Google Account securetester1@gmail.com for this purpose.

Can you please cc them in? Thanks.

### ad...@chromium.org (2020-07-20)

Done, thanks.

### se...@gmail.com (2020-07-21)

Thank you for granting the access. 

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2020-09-10)

Now that this is disclosed, I've posted an article on this vulnerability:

https://alesandroortiz.com/articles/uxss-android-webview-cve-2020-6506/

Article has updates on impacted vendors and will keep being updated over the next few weeks with more affected vendors.

Thanks again to everyone who worked on this crbug, especially torne@ for the insightful discussion and ctzsm@ for implementing the patch. Have a great week!

### al...@alesandroortiz.com (2020-09-30)

Disclosing this previously-omitted detail now that vendor has issued advisory:

In rare configurations, no user interaction is required (drive-by attack). The top-level page must be loaded using the file:// scheme and the WebView must set both WebSettings.setJavaScriptCanOpenWindowsAutomatically() and WebSettings.setAllowUniversalAccessFromFileURLs() to true.

Security advisory from a vendor with drive-by attack configuration: https://cordova.apache.org/news/2020/09/29/cve-2020-6506.html

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ea127dde94b98035b3b5568fbd673621d11a6bad

commit ea127dde94b98035b3b5568fbd673621d11a6bad
Author: Charlie Reis <creis@chromium.org>
Date: Mon Jul 10 21:08:52 2023

[WebView] Move fix for single-window-mode JS injection.

The previous fix relied on FilterURL behavior which may soon be
changing. Instead, detect the javascript: URL case in the
renderer process.

This is expected to cause no change in behavior, and relies on
the existing test coverage in
PopupWindowTest#testSingleWindowModeJsInjection.

Bug: 1083819
Change-Id: I1733d896064f4b193593ae9b47a02d28d9424284
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4675673
Reviewed-by: Richard Coles <torne@chromium.org>
Commit-Queue: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1168321}

[modify] https://crrev.com/ea127dde94b98035b3b5568fbd673621d11a6bad/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/ea127dde94b98035b3b5568fbd673621d11a6bad/content/renderer/render_frame_impl.cc


### is...@google.com (2023-07-10)

This issue was migrated from crbug.com/chromium/1083819?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052335)*
