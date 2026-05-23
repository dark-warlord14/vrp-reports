# Security: Origin spoof in external protocol dialogs via server-side redirect to external protocol

| Field | Value |
|-------|-------|
| **Issue ID** | [40055515](https://issues.chromium.org/issues/40055515) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-04-11 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

A URL responding with a server-side redirect to an external protocol can trigger an external protocol dialog with a spoofed origin. The origin is never the redirecting URL's origin. Instead, the initiating page's origin (or precursor origin if opaque) is shown in dialogs. This affects both application protocols (e.g. ms-calculator:) and the telephone protocol (tel:). The UI for these are different, but the effects are similar in most cases.

For example, if a page on [https://www.google[.]com](https://www.google%5B.%5Dcom) contains a link (<a href="...">) to [https://attacker[.]tld/redirect](https://attacker%5B.%5Dtld/redirect), and a user clicks the link, the dialog will show [https://www.google[.]com](https://www.google%5B.%5Dcom) as the origin instead of [https://attacker[.]tld](https://attacker%5B.%5Dtld) .

Similarly, if a page on [https://www.google[.]com](https://www.google%5B.%5Dcom) navigates the current window or new window via JavaScript (window.location or window.open()) to [https://attacker[.]tld/redirect](https://attacker%5B.%5Dtld/redirect), the dialog will show [https://www.google[.]com](https://www.google%5B.%5Dcom) as the origin.

In effect, the behavior is the same as if the page had directly used the external protocol URL (ms-calculator:) instead of the HTTPS URL ([https://attacker[.]tld/redirect](https://attacker%5B.%5Dtld/redirect)).

As far as I can tell, common protections such as CSP and iframe sandboxing are bypassed in most scenarios.

No user interaction is needed if a user previously checked "Always allow {origin} to open links of this type..." for the target origin and protocol, or if allowed for origin+protocol via enterprise policy: <https://chromeenterprise.google/policies/#AutoLaunchProtocolsFromOrigins>

ADDITIONAL INFO  

A malicious URL could be placed in search result pages, "external link" interstitial pages, user-provided URLs in content, among many other scenarios. Most websites filter input to only allow http(s) URLs (generally to avoid javascript: URLs which are blocked by browser in server-side redirects), therefore this works as an effective bypass to spoof the origin across most websites and navigation methods.

See attached video spoof-google-search.mp4 for Google Search demo with both calc and tel PoCs. Note that I only enabled this PoC to work from my IP address for a few minutes to record the video.

External protocols in server-side redirects probably should be treated similarly to javascript: URLs in server-side redirects, which are blocked by the browser as unsafe. Otherwise, the browser could render a blank page with origin set to the server-side redirect initiator, to ensure the dialog and address bar show the correct origin and the tab doesn't have another origin's content rendered.

Some of the PoCs benefit from behaviors described in <https://crbug.com/chromium/1196495> and <https://crbug.com/chromium/1096610>, but are not dependent on them for success.

**VERSION**  

Chrome Version: 89.0.4389.114 (Official Build) (64-bit) (cohort: Stable), also repros on 91.0.4468.0 Canary  

Operating System: Windows 10 OS Version 2009 (Build 19042.867)

**REPRODUCTION CASE**  

Scenario 1: Link click

1. Navigate to <https://alesandroortiz.com/security/chromium/external-protocol/spoof-links.html>
2. Click either of the links

Observed: External protocol dialog shown with current page origin ([https://alesandroortiz[.]com](https://alesandroortiz%5B.%5Dcom))  

Expected: External protocol dialog is not shown or is shown with redirecting origin ([https://aogarantiza[.]com](https://aogarantiza%5B.%5Dcom))

Scenario 2: JavaScript redirect (window.location)

1. Navigate to one of these URLs:  
   
   <https://www.google.com/url?q=https%3A%2F%2Faogarantiza.com%2Fchromium%2Fexternal-protocol%2Fcalc.php&sa=D&sntz=1&usg=AFQjCNGOqAoEa7AghaevcuD3T2XmJY62gw>  
   
   <https://www.google.com/url?q=https%3A%2F%2Faogarantiza.com%2Fchromium%2Fexternal-protocol%2Ftel.php&sa=D&sntz=1&usg=AFQjCNEUEKsWLeTxzL6gKZT1TR_zarnCJg>

Observed: Dialog shown with correct origin.  

Expected: Dialog shown with spoofed origin.

Scenario 3: Page has iframe with user-controlled src to URL responding with server-side redirect

1. Navigate to <https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-sandbox-calc.html>

Observed: Dialog shown with embedding page origin ([https://alesandroortiz[.]com](https://alesandroortiz%5B.%5Dcom))  

Expected: Dialog shown with iframe src origin ([https://aogarantiza[.]com](https://aogarantiza%5B.%5Dcom))

Scenario 4: Page with iframe srcdoc (sandboxed)

1. Navigate to <https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-srcdoc-calc.html>
2. Observe onload PoC of second iframe, then click link in first iframe

Observed: Dialog shown with embedding page origin ([https://alesandroortiz[.]com](https://alesandroortiz%5B.%5Dcom))  

Expected: Dialog shown with iframe src origin ([https://aogarantiza[.]com](https://aogarantiza%5B.%5Dcom))

Scenario 5: Attacker page with refreshing iframe with client-side redirect leading to server-side redirect

1. Navigate to <https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-src-calc.html>
2. With most extensions, prompt will be reshown without further user interactions (<https://crbug.com/chromium/173557>). Otherwise, interact with any page or browser UI to show prompt.

Observed: Dialog shown with embedding page origin ([https://alesandroortiz[.]com](https://alesandroortiz%5B.%5Dcom))  

Expected: Dialog shown with iframe src origin ([https://aogarantiza[.]com](https://aogarantiza%5B.%5Dcom))

Other scenarios in PoCs below.

You can re-test any of the app protocol PoCs after checking "Always allow..." to verify the app will be launched without interaction if previously allowed.

ALL PROOF OF CONCEPTS  

App protocols and tel: protocols:  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-links.html>

App protocols:  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-sandbox-calc.html>  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-srcdoc-calc.html>  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-src-calc.html>

App protocols, misc:  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-new-tab.html>

tel: protocol:  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-sandbox-tel.html>  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-srcdoc-tel.html>  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-tel-diff-tab.html>  

<https://alesandroortiz.com/security/chromium/external-protocol/spoof-iframe-src-tel.html>

Google external link demo, user click (equivalent to spoof-links.html PoC):  

<https://www.google.com/url?q=https://aogarantiza.com/chromium/external-protocol/calc.php>  

<https://www.google.com/url?q=https://aogarantiza.com/chromium/external-protocol/tel.php>

Google ~open client-side redirect demo, window.location (used in iframe PoCs to spoof Google origin):  

<https://www.google.com/url?q=https%3A%2F%2Faogarantiza.com%2Fchromium%2Fexternal-protocol%2Fcalc.php&sa=D&sntz=1&usg=AFQjCNGOqAoEa7AghaevcuD3T2XmJY62gw>  

<https://www.google.com/url?q=https%3A%2F%2Faogarantiza.com%2Fchromium%2Fexternal-protocol%2Ftel.php&sa=D&sntz=1&usg=AFQjCNEUEKsWLeTxzL6gKZT1TR_zarnCJg>

The automatic Google redirect links were created by creating links in Google Sites: <https://sites.google.com/view/aortest1/external-protocol-poc-1>

Source for HTML files attached. Source for server-side redirect URLs below:  

calc.php: <?php header('Location: ms-calculator:'); ?>  

tel.php: <?php header('Location: tel:5555555551'); ?>

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [spoof-links.html](attachments/spoof-links.html) (text/plain, 494 B)
- [spoof-iframe-sandbox-calc.html](attachments/spoof-iframe-sandbox-calc.html) (text/plain, 345 B)
- [spoof-iframe-srcdoc-calc.html](attachments/spoof-iframe-srcdoc-calc.html) (text/plain, 736 B)
- [spoof-iframe-src-calc.html](attachments/spoof-iframe-src-calc.html) (text/plain, 782 B)
- [spoof-new-tab.html](attachments/spoof-new-tab.html) (text/plain, 1.2 KB)
- [spoof-iframe-sandbox-tel.html](attachments/spoof-iframe-sandbox-tel.html) (text/plain, 343 B)
- [spoof-iframe-srcdoc-tel.html](attachments/spoof-iframe-srcdoc-tel.html) (text/plain, 733 B)
- [spoof-tel-diff-tab.html](attachments/spoof-tel-diff-tab.html) (text/plain, 1.2 KB)
- [spoof-iframe-src-tel.html](attachments/spoof-iframe-src-tel.html) (text/plain, 1.1 KB)
- [spoofs-calc.mp4](attachments/spoofs-calc.mp4) (video/mp4, 4.7 MB)
- [spoofs-tel.mp4](attachments/spoofs-tel.mp4) (video/mp4, 2.5 MB)
- [spoofs-google.mp4](attachments/spoofs-google.mp4) (video/mp4, 1.5 MB)
- [spoof-google-search.mp4](attachments/spoof-google-search.mp4) (video/mp4, 3.3 MB)

## Timeline

### [Deleted User] (2021-04-11)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-04-11)

Google Search spoof PoC recording attached.

### ct...@chromium.org (2021-04-13)

Thanks for the report and the great demo videos, particularly that last one :-)

meacer@ can you take a look a this one? Adding other c/b/external_protocol/OWNERS as well.

That this (1) shows the wrong origin in the dialog, but also (2) applies the wrong permissions/content settings makes this particularly nasty. I'm tentatively setting this to Sev-Medium (because it isn't quite "full circumvention of the same origin policy" or "complete control over the apparent origin in the omnibox" for Sev-High, but it kind of feels close).

[Monorail components: Internals>Permissions>Model UI>Browser>WebAppInstalls]

### [Deleted User] (2021-04-13)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2021-04-13)

This also repros in Chromium-based Edge.

1. Can someone determine (or guess) if fixing in Chromium would also fix in Edge?
2. Is it okay if I also report to Microsoft with context that it also affects Chromium?

Their security program states "Vulnerabilities that reproduce in Chrome at the time of submission" are out of scope (source: https://www.microsoft.com/en-us/msrc/bounty-new-edge ), so answer to first question would help determine whether MSRC report would be eligible or not (and help them get a jump start on separate fix).

(I may delete this comment prior to crbug disclosure.)

### ct...@chromium.org (2021-04-13)

I'll let external protocol OWNERS weigh in as well, but I'd assume that fixing this in Chromium will also fix this in Edge, as I've seen other external protocol handler bugs also affect Edge and I don't think they customize it much if at all downstream. In general for bug reports that affect multiple vendors, we're okay with you sending reports to each affected vendor though, but it's good for us to know if you do in case we need to coordinate disclosure.

### do...@chromium.org (2021-04-14)

I would also guess that fixing this in Chromium would fix it in Edge.

This is pretty interesting. I think the callpath is NavigationURLLoaderImpl::PrepareForNonInterceptedRequest() -> ChromeContentBrowserClient::HandleExternalProtocol(). In the former, we pass what eventually ends up in the dialog as ResourceRequest::request_initiator:

      bool handled = GetContentClient()->browser()->HandleExternalProtocol(
          resource_request_->url, web_contents_getter_,
          ChildProcessHost::kInvalidUniqueID, frame_tree_node_id_,
          navigation_ui_data_.get(),
          resource_request_->resource_type ==
              static_cast<int>(blink::mojom::ResourceType::kMainFrame),
          static_cast<ui::PageTransition>(resource_request_->transition_type),
          resource_request_->has_user_gesture,
          /* this is what ends up in the dialog -> */ resource_request_->request_initiator,
          &loader_factory);

I'm guessing that on a server side redirect, the initiator is still the origin from whence the navigation came. I'm not actually sure whether this is correct or not (it could well be?).

This field was added in https://chromium-review.googlesource.com/c/chromium/src/+/1829932 where there are some questions about whether the initiator is right. +estark, do you have any memory of other discussions?

At the very least, the origin in the omnibox matches the origin in the dialog in the top frame examples, which makes me suspect that this may actually be working as intended. It would be odd if the omnibox origin didn't match.

### do...@chromium.org (2021-04-14)

To expand on my https://crbug.com/chromium/1197889#c7, what I'm wondering is whether navigating to a URL which performs an immediate server-side redirect to an external protocol is effectively the same as the original site having a link directly embedding that external protocol. I could see that being regarded as true, which would mean this is working as intended.

For instance, directly navigating to https://aogarantiza.com/chromium/external-protocol/calc.php shows nothing in the omnibox, which suggests to me that no actual navigation is being committed, and all we've exchanged with the site is headers. That being said, we've exchanged at least headers with the second origin, but I don't know enough about the innards of navigation to say what we should do in this case :)

[Monorail components: -Internals>Permissions>Model -UI>Browser>WebAppInstalls UI>Browser>Permissions>Prompts]

### al...@alesandroortiz.com (2021-04-14)

Re: https://crbug.com/chromium/1197889#c7 + https://crbug.com/chromium/1197889#c8, this scenario seems closer to cross-origin javascript: server-side redirect than a direct link/embed.

This also seems close to a cross-origin HTTP Auth dialog scenario. When an HTTP Auth dialog is shown due to a cross-origin navigation, a blank page is rendered and the omnibox shows the dialog-initiating URL.

### al...@alesandroortiz.com (2021-04-14)

Re: https://crbug.com/chromium/1197889#c6 + https://crbug.com/chromium/1197889#c7, thanks for info on Edge repro. I'll verify once a fix lands on Edge Canary for this and other external protocol reports.

This also repros in Firefox. Reporting to them today. I'll keep both vendors in the loop of each other's disclosure dates if they are misaligned, since you may need to coordinate disclosure. (Disclosing one might lead to public discovery of vuln in the other browser.)

(I may delete this comment prior to crbug disclosure.)

### do...@chromium.org (2021-04-15)

> This also seems close to a cross-origin HTTP Auth dialog scenario. When an HTTP Auth dialog is shown due to a cross-origin navigation, a blank page is rendered and the omnibox shows the dialog-initiating URL.

Interesting observation - that seems to match the behaviour we see here where there's no committed navigation and the request initiator is still regarded as the initial origin that was navigated from.

We possibly need some navigation experts on this. +lukasza and +alexmos, can you weigh in on my questions in https://crbug.com/chromium/1197889#c7 and https://crbug.com/chromium/1197889#c8?

### al...@alesandroortiz.com (2021-04-15)

To clarify my comment, HTTP Auth *does* seem to commit navigation. What I meant was that external protocol handling seems similar to HTTP Auth in terms of behavior trigger (response header controls behavior) and user flow (sensitive dialog with origin info), therefore external protocol handling probably should look more like HTTP Auth flow which commits and shows origin of dialog initiator (server sending the triggering response headers).

### me...@chromium.org (2021-04-15)

This looks like a variant of https://crbug.com/chromium/1091961: The navigation doesn't update content area but ends up showing some non-content area dialog, causing a mismatch between the omnibox and the dialog.

We have many of these. Basically, anytime a navigation results in a UI (dialog, download shelf, external app opening etc) that doesn't update the omnibox, we'll have this issue. The similarity to the HTTP auth case is a great observation, and we might need to do something similar here as well.

### al...@alesandroortiz.com (2021-04-15)

Thanks for context. Don't have access to crbug with impact details of variants in other features, but for this feature, impact seems particularly dangerous beyond origin spoof in dialog:

1. An open redirect in an allowlisted origin can launch the protocol with zero interaction
e.g. Video conferencing site has open redirect + large % of userbase has origin+protocol allowlisted due to frequent use/enterprise policy + app has RCE vuln or other vuln via protocol handler

2. Reasonably sandboxed iframe embedded by allowlisted origin can launch the protocol with zero interaction
e.g. Video conferencing site embeds 3rd party/arbitrary sandboxed iframe + user/enterprise has origin+protocol allowlisted + app has vuln via protocol handler

3. Any link within allowlisted origin can launch protocol if clicked
e.g. Video conferencing site allows user-controlled HTTPS links in event descriptions, profile info, etc. + user/enterprise has origin+protocol allowlisted + app has vuln via protocol handler

If not allowlisted, only a single click in dialog is needed and it appears to be from the user-trusted website, so it's likely to be effective. There's also very few (if any) mitigations that I could find: CSP and sandboxing are largely ineffective; most websites with some type of user content allow user-controlled HTTPS links; combined with https://crbug.com/chromium/1196495 and https://crbug.com/chromium/1096610 behaviors, it's easy to bypass protocol launch user interaction requirements for many users.

### mk...@google.com (2021-04-16)

cc Anne from Mozilla for some cross-vendor coordination.

### al...@alesandroortiz.com (2021-04-16)

Firefox bug: https://bugzilla.mozilla.org/show_bug.cgi?id=1705211
This crbug's ID was also provided yesterday upon request.

### do...@chromium.org (2021-04-28)

lukasza@chromium.org/alexmos@chromium.org - ping for your thoughts here. :)

### lu...@chromium.org (2021-04-28)

Sorry for the delay.  Let me try to answer some of the questions above (and also add the UI>Browser>Navigation component for more people to take a look).

RE: external protocol handling probably should look more like HTTP Auth flow which commits

A navigation "commits", when a frame (e.g. content::RenderFrameImpl) will host a document.  External protocol handler doesn't create/commit a new document in a frames.

RE: External protocols in server-side redirects probably should be treated similarly to javascript: URLs in server-side redirects, which are blocked by the browser as unsafe.

Agreed.  AFAIK we already block HTTP -> chrome-extension:// and HTTP -> file:// redirects, so this seems like definitive bug.  Let me open a separate bug for this in https://crbug.com/chromium/1203814.


[Monorail components: UI>Browser>Navigation]

### lu...@chromium.org (2021-04-28)

RE: https://crbug.com/chromium/1197889#c7: dominickn@: passing `initiator_origin` into HandleExternalProtocol

Yeah, I think I missed the redirect problems in my earlier CR comment at 
https://chromium-review.googlesource.com/c/chromium/src/+/1829932/4/content/browser/loader/navigation_url_loader_impl.cc#671

I agree that we should pass the origin of the last redirecting server, and only fall back to `initiator_origin` if there were no redirects.

AFAICT, changing the origin passed to HandleExternalProtocol should take care of the origin spoof, right?  Or are there other scenarios that we need to consider (e.g. I see that the bug report mentions "Scenario 2: JavaScript redirect (window.location)" - I would expect the correct origin to be shown in the dialog here [here = in absence of http redirects]).

### al...@alesandroortiz.com (2021-04-28)

Re: https://crbug.com/chromium/1197889#c19, that's correct, passing origin of last redirecting server should take care of dialog origin spoof in all reported scenarios.

There's still other apparent issues, such as sandbox + CSP bypass and omnibox mismatch, but those would be moot if server-side redirect is blocked altogether (thanks for filing spinoff https://crbug.com/chromium/1203814).

> https://crbug.com/chromium/1197889#c19: I would expect the correct origin to be shown in the dialog here [here = in absence of http redirects]).

Yes, current behavior is safe for direct navigation scenarios (e.g. <a href="ms-calculator:">calc</a> or window.location = 'ms-calculator:'). The current page's origin is shown as expected. I would expect direct navigation to still be allowed, since untrusted non-HTTPS URLs can and should be blocked by websites, much like they often block direct javascript: URLs in anchor href, window.location, window.open, iframe src, etc.

Scenario 2 is for window.location navigation to a URL which returns a server-side redirect. Under the hood it's essentially the same behavior, but wanted to make it clear this repros with other common places where untrusted URLs are accepted by websites. (For reference, Scenario 2 PoC: https://www.google.com/url?q=https%3A%2F%2Faogarantiza.com%2Fchromium%2Fexternal-protocol%2Fcalc.php&sa=D&sntz=1&usg=AFQjCNGOqAoEa7AghaevcuD3T2XmJY62gw )

### [Deleted User] (2021-04-30)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-15)

meacer: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-06-01)

+engedy +ravjit - I think you're looking at some work on external protocol handling right now? I think I've diagnosed the issue in https://bugs.chromium.org/p/chromium/issues/detail?id=1197889#c7, but it's not clear to me what origin should be the correct one to pass to the protocol handling dialog if we don't use the request_initiator.

### lu...@chromium.org (2021-06-02)

RE: https://crbug.com/chromium/1197889#c24: it's not clear what origin should be the correct one to pass to the protocol handling dialog if we don't use the request_initiator

We've chatted offline and agreed that we should use the origin of the last redirecting server (falling back to the request_initiator if there were no redirects / if the request goes straight to an external protocol).

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-21)

ravjit@: if you're working on external protocol handlers generally, it sounds like you might be a better owner for this.

### me...@google.com (2021-08-02)

[Comment Deleted]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-08-11)

Hi all, there hasn't been any substantial updates to the crbug since early June. Are there any blockers on this? Mitigation strategy seemed agreed upon in https://crbug.com/chromium/1197889#c25.

### ra...@chromium.org (2021-08-11)

Sorry for the delay looking into it.

### al...@alesandroortiz.com (2021-08-11)

Thanks!

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-09-14)

ravjit@: The patch at https://chromium-review.googlesource.com/c/chromium/src/+/3113931 LGTM. I see there's still some outstanding comments regarding the tests; hope those are resolved soon so the fix can make it to users sooner than later.

The Firefox team was waiting on the Chromium team to decide on mitigation strategy. Now that the strategy is settled, I've left a comment in https://bugzilla.mozilla.org/show_bug.cgi?id=1705211#c15 to see if they're ready to implement similar fix or if they have any concerns. (Not sure if there's already been comms not documented in either bug tracker.)

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f781748dcb3c7d0420b884c1c24b9b4497bc7c97

commit f781748dcb3c7d0420b884c1c24b9b4497bc7c97
Author: Ravjit <ravjit@chromium.org>
Date: Thu Sep 16 12:29:55 2021

Show the origin of the last redirecting server in external protocol handler dialogs

External protocol handlers always show the initiating url's origin. This can be misleading if there are server side redirects.
Now we will show the origin of the last redirecting server (falling back to the request_initiator if there were no redirects / if the request goes straight to an external protocol).

Bug: 1197889
Change-Id: I3cf7ccf3a8bd79d161364680a1871d1c88bec813
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3113931
Commit-Queue: Ravjit Singh Uppal <ravjit@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Collin Baker <collinbaker@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/main@{#922096}

[modify] https://crrev.com/f781748dcb3c7d0420b884c1c24b9b4497bc7c97/chrome/browser/ui/views/external_protocol_dialog_browsertest.cc
[modify] https://crrev.com/f781748dcb3c7d0420b884c1c24b9b4497bc7c97/content/browser/loader/navigation_url_loader_impl.cc
[modify] https://crrev.com/f781748dcb3c7d0420b884c1c24b9b4497bc7c97/content/public/browser/content_browser_client.h


### al...@alesandroortiz.com (2021-09-16)

Thanks for merging! I'll verify once it lands on Canary.

### al...@alesandroortiz.com (2021-09-21)

Verified as fixed in Canary 96.0.4648.2 using all the PoCs in original report. They all result in expected behavior.

Thanks again!

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-09-28)

Ravjit, thanks for the fix! Can this issue be closed now, or is there follow-up work needed here (e.g. it seems that we would like to increase test coverage?).

### ra...@chromium.org (2021-10-21)

The test flakiness is fixed. We can mark this as done.

### [Deleted User] (2021-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-28)

Congratulations - the VRP Panel has decided to award you $2000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-11-11)

Thanks for the reward!

Can someone please add the embargo label (or other appropriate label) to this crbug? Firefox hasn't fixed the issue yet, so I don't want this crbug to become public in a few weeks. Thanks!

### am...@chromium.org (2021-11-11)

(Sheriffbot didn't ask for merges here. That Sheriffbot bug is tracked as https://crbug.com/chromium/1262390).


### am...@chromium.org (2021-11-11)

as per request in https://crbug.com/chromium/1197889#c53 

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2021-12-14)

Mozilla fixed their bugs related to this issue and agreed to March 21st, 2022 disclosure date. Will follow up in March to request embargo removal for this crbug.

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2022-01-27)

(Note to self: has embargo label, so not yet public)

### al...@alesandroortiz.com (2022-03-21)

Coordinated disclosure date has arrived. Can someone please make this bug public? I've requested the same from Mozilla for their related bugs.

### jd...@chromium.org (2022-03-21)

Removing security embargo per Comments 53, 55, and 60.

### al...@alesandroortiz.com (2022-03-22)

Thanks jdeblasio@!

### am...@chromium.org (2022-08-11)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1197889?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/1208246]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055515)*
