# CSP Bypass via Chrome Extension

| Field | Value |
|-------|-------|
| **Issue ID** | [40053061](https://issues.chromium.org/issues/40053061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gh...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2020-08-12 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

CSP(Content-Security-Policy) has a header frame-ancestors which blocks click jacking and UI Redressing Vulnerabilities. However, I have discovered a way to bypass the frame-ancestors header via Chrome Extension.

**VERSION**  

Chrome Version: 84.0.4147.125 (Official Build) (64-bit)  

Operating System: Windows 10 Home

**REPRODUCTION CASE**  

Bypassing Frame-ancestor header:

1. Create a PHP file which has the frame-ancestors header set.(No matter whats the value of header. self,none,url) .File attached (mysite\_csp.php). You can use any other site which has this header set or just upload this file to some url.
2. Download the exploit code, csp\_bypass\_extension.zip chrome extension . Turn ON Developer Mode at Chrome Extensions page and load the extracted extension folder by using Load Unpacked button.
3. Open the frame-ancestors URL and click the extension button, this extension will bypass the CSP and load the URL in extension popup. Popup.js file has the simple code to load the URL in iframe.

Bypassing X-Frame-Options header

1. Download mysite\_xframe.php file and upload somewhere.
2. Open URL and click the extension button and it will load the URL in iframe aswell. Basically if frame-ancestors is present with x-frame-options. X-Frame-Options header will get bypassed.

Video POC with Reproduction Steps : <https://youtu.be/bdbFQk4b2po>  

URL with CSP frame-ancestors set : <https://jasminderpalsingh.info/pentest/mysite_csp.php>  

URL With X-frame-options set : <https://jasminderpalsingh.info/pentest/mysite_xframe.php>

**CREDIT INFORMATION**  

Reporter credit: Jasminder Pal Singh, Web Services Point WSP, Kotkapura

## Attachments

- [csp_bypass_extension.zip](attachments/csp_bypass_extension.zip) (application/octet-stream, 28.2 KB)
- [mysite_csp.php](attachments/mysite_csp.php) (text/plain, 262 B)
- [mysite_xframe.php](attachments/mysite_xframe.php) (text/plain, 229 B)

## Timeline

### va...@chromium.org (2020-08-13)

I'm not sure if this is an issue in Chrome Extensions or CSP handling so adding both components and owners.
Could one of you please help me with the triage here? I'd really appreciate it.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy Platform>Extensions]

### ar...@chromium.org (2020-08-14)

+mkwst@ and +antoniosartori@
+karandeepb@ FYI, maybe this might have an interest to you relatively to https://crbug.com/chromium/896041.

> Basically if frame-ancestors is present with x-frame-options. X-Frame-Options header will get bypassed. 

This is expected:
https://www.w3.org/TR/CSP/#frame-ancestors-and-frame-options
```
In order to allow backwards-compatible deployment, the frame-ancestors directive _obsoletes_ the X-Frame-Options header. If a resource is delivered with an policy that includes a directive named frame-ancestors and whose disposition is "enforce", then the X-Frame-Options header MUST be ignored.
```

-----------

So, now the real question is: why the CSP:frame-ancestor doesn't apply here in the context of an extension?

Again, I think this is also expected, because the chrome-extension: scheme "bypass" CSP. So frame-ancestor do not block its parent.

```
bool CSPContext::IsAllowedByCsp(mojom::CSPDirectiveName directive_name,
                                const GURL& url,
                                bool has_followed_redirect,
                                bool is_response_check,
                                const mojom::SourceLocationPtr& source_location,
                                CheckCSPDisposition check_csp_disposition,
                                bool is_form_submission) {
  if (SchemeShouldBypassCSP(url.scheme_piece()))
    return true;
```

-----------

From what I understood, this is working the way it was designed and implemented. Maybe we should close as Working-As-Intented? (WontFix)
What do you think Mike?



### gh...@gmail.com (2020-08-14)

Hello, 
If that's the case many popular websites are vulnerable to extension based Clickjacking and UI Redressing Vulnerabilities. 

### mk...@chromium.org (2020-08-14)

The goal of the `chrome-extension:` carveout was to allow extension resources to be embeddable despite a page's desire to limit the sources from which it normally loaded resources. The `frame-ancestors` interaction isn't something I explicitly thought about at the time, and I can understand how it's unexpected.

I think we'd ideally carve out only extension resources that have access to the given page. That wasn't possible at the time, but perhaps it's possible today given that the implementation of `frame-ancestors` has shifted up to the browser process.

### gh...@gmail.com (2020-08-14)

Attack Scenario : In the video POC i mentioned a example website https://tweetdeck.twitter.com/ . Its a twiiter site and victim to this bug. It allows to tweet from logged account in two steps. Its easy to craft a interactive chrome extension by exploiting this bypass. 

There are hundreds of other sites that might be vulnerable to this. As per my experience, it should be fixed. 

### [Deleted User] (2020-08-14)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-08-17)

Adding Sev-Medium tentatively.

### [Deleted User] (2020-08-18)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gh...@gmail.com (2020-08-24)

Thanks. Looking forward for a fix and eligibility for reward.

### gh...@gmail.com (2020-08-28)

Hello Team,

Is it possible to continue the reward process parallel to fix ?
I want to make chromium research full time because i love it. On the other hand i want to make the survival out of it. So, is it possible to reward the researchers(if eligible) as early as possible? Or reward a before-fix amount until bug is fixed and final amount after fix. It will help the researchers like me to keep the motivation strong. 

In my case, i want to buy a Chromebook to continue my further research but here i am waiting since two weeks.

I hope you will take care of this for the sake to encourage researchers. 

Thanks

### [Deleted User] (2020-08-28)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-09-02)

> I think we'd ideally carve out only extension resources that have access to the given page. That wasn't possible at the time, but perhaps it's possible today given that the implementation of `frame-ancestors` has shifted up to the browser process.

This sounds like good trade-off.

+CC:benwells@ I am not super familiar with extensions/.
Could you point out a function to check if a given extension have access to a URL/Origin/iframe?

### gh...@gmail.com (2020-09-07)

Looking forward for a fix.

Thanks

### gh...@gmail.com (2020-09-15)

Looking for an update.

### [Deleted User] (2020-09-16)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gh...@gmail.com (2020-09-22)

Looking forward for an update.

### ar...@chromium.org (2020-09-22)

+benwells@

I am not familiar with extensions/.
Is the sentence: "extension have access to the given page" defined in a given way?
If yes, do you happen to know how I can retrieve this information?

### be...@chromium.org (2020-09-23)

I think you need someone from the core extensions team to chime in, either Karan or Devlin should be able to help.

### ka...@chromium.org (2020-09-23)

I don't think this is WAI. As Mike mentioned, the chrome-extension scheme bypassing is required for things like web accessible resources to work. This is how an extension can inject a web accessible iframe into a page without it being blocked by the page's CSP.

I am not sure I understand how the check is working correctly? Is it that the frame-ancestors is being checked against each parent frame and when it comes to the extension's frame we skip the check because the extension scheme is a CSP bypassing scheme? If yes, I don't think the notion of a CSP bypassing scheme is being followed correctly here. It's described as:

    // Registers a URL scheme whose resources can be loaded regardless of a
    // page's Content Security Policy.

at https://source.chromium.org/chromium/chromium/src/+/master:content/public/common/content_client.h;l=134;drc=c240cfc4b578dc6268356551922ba73762294795;bpv=1;bpt=0.

Hence I think the notion of a csp bypassing scheme should only be applicable to resources being loaded from that scheme and not to the urls of the ancestor frames in this case. 

### ar...@chromium.org (2020-09-23)

>  Is it that the frame-ancestors is being checked against each parent frame and when it comes to the extension's frame we skip the check because the extension scheme is a CSP bypassing scheme?

Yes.

--

So you are suggesting to apply CSP for frame-ancestor no matter the extension?
That would be very trivial.

Mike suggested to do it only if the extension have access to the embedded document. I am not sure to see what it really means. Is there any meaningful context were we can say that?

### ka...@chromium.org (2020-09-23)

> So you are suggesting to apply CSP for frame-ancestor no matter the extension?
Yes.

> Mike suggested to do it only if the extension have access to the embedded document. I am not sure to see what it really means. Is there any meaningful context were we can say that?

Yes. There is a concept of host permissions which an extension can specify and a user can modify (https://developer.chrome.com/extensions/runtime_host_permissions). IIUC the suggestion was for the extension to be able to embed a frame if it had access to a frame regardless of X-Frame-Options/frame-ancestors. I think this is a good thing to do given that:
- There are legit use cases for an extension to be able to embed a frame and if it has host permissions to a frame then its reasonable to bypass the frame-src and X-Frame-Options restriction.
- Currently if an extension has access to a page, it can already modify its X-Frame-Options and CSP header using the web request API to make this possible. However this is not ideal and in Manifest V3, we are hoping to prevent the extension from relaxing the CSP. If we automatically allow the extension to embed frames to which it has permission, it won't need to modify these headers.

TLDR: I think taking host permissions into account would be a net positive change, however I am not sure if it needs to necessarily block fixing this bug anc can probably be tackled separately.

Also do we know the relative prevalence of frame-ancestors vs X-Frame-Options (IIUC the latter is not exempting extension parent frames)? Want to get a sense of whether there might be extensions depending on this behavior.

### gh...@gmail.com (2020-09-28)

Looking forward for an update.

### ar...@chromium.org (2020-09-29)

Thanks karandeepb@ (https://crbug.com/chromium/1115590#c22)

I will make Chrome enforce CSP:frame-ancestor no matter the scheme of its parent (even extension).
I am a bit busy now, so I am expecting a 10 days delay before landing this.

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### gh...@gmail.com (2020-10-08)

Looking forward for an update.

Thanks.

### gh...@gmail.com (2020-10-11)

Looking forward for a fix this week.

Thanks

### ar...@chromium.org (2020-10-13)

(I'm back from vacation)

Let's fix this for today.

### ar...@chromium.org (2020-10-13)

> (I'm back from vacation)
> 
> Let's fix this for today.

Patch:
https://chromium-review.googlesource.com/c/chromium/src/+/2467897

### gh...@gmail.com (2020-10-14)

Thanks for the patch. 
Looking forward to get the patch reviewed.

### ka...@chromium.org (2020-10-15)

One point regarding the security severity: I am not sure if it is medium. The extension can still (even after the patch) modify the CSP header using the web request API to relax frame-ancestors and embed iframes. However doing so would require host permissions to the iframe url.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fd406771ba8565e5c58563b5492d45fe2ba5a3c8

commit fd406771ba8565e5c58563b5492d45fe2ba5a3c8
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Fri Oct 16 09:59:28 2020

[CSP] Do not bypass CSP:frame-ancestors

Extensions can load their own internal content into the document. They
shouldn't be blocked by the document's CSP.

There is an exception: CSP:frame-ancestors. This one is not about
allowing a document to embed other resources. This is about being
embedded. As such this shouldn't be bypassed. A document should be able
to deny being embedded inside an extension.

Bug: 1115590
Change-Id: I2176a25e67cd0d637ecb3b13a39de30259d9d7a1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2467897
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#817859}

[modify] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/chrome/browser/extensions/extension_csp_bypass_browsertest.cc
[add] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/chrome/test/data/extensions/csp/frame-ancestors-none.html
[add] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/chrome/test/data/extensions/csp/frame-ancestors-none.html.mock-http-headers
[modify] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/services/network/public/cpp/content_security_policy/content_security_policy.cc
[modify] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/services/network/public/cpp/content_security_policy/csp_context.cc


### ar...@chromium.org (2020-10-16)

Do you think we should attempt merging this to M87 beta? (release date 2020-11-10)
It would be released on M88 otherwise (release date 2021-01-19)

I think this update can potentially break some extensions. So I think not cherry-picking and let it go through canary/dev to be better.
WDYT?

---

> One point regarding the security severity: I am not sure if it is medium.

I don't know how to judge severity of this myself when this is about Extensions.
Extensions have an enormous amount of privileges already, this is removing tiny one. I wouldn't consider users safe if they install a malicious extension. The web store checking/banning extensions is the only reasonable barrier I can think of.

(I will let others judge about the Security_Severity of this.)

### ka...@chromium.org (2020-10-16)

> I think this update can potentially break some extensions. So I think not cherry-picking and let it go through canary/dev to be better.
WDYT?

I agree, especially since this is not a regression. 

### [Deleted User] (2020-10-16)

[Empty comment from Monorail migration]

### gh...@gmail.com (2020-10-18)

Thanks for the fix. Looking forward for the release and reward process.

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-19)

Requesting merge to beta M87 because latest trunk commit (817859) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-19)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-10-20)

arthursonzogni@ - please respond to the merge questionnaire in c#40 to consider the merge request

### ar...@google.com (2020-10-20)

> arthursonzogni@ - please respond to the merge questionnaire in c#40 to consider the merge request

See https://crbug.com/chromium/1115590#c34 and https://crbug.com/chromium/1115590#c35. We don't want to merge.

### ad...@google.com (2020-10-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-21)

ghulianisikh@gmail.com - Congratulations, the VRP panel has awarded $3000 for this report. Someone from our finance team will be in touch.

### gh...@gmail.com (2020-10-22)

Thank you so much for the reward. I really appreciate 🙏
Looking forward to be contacted by finance team.

### gh...@gmail.com (2020-10-22)

Please, also check my https://crbug.com/chromium/1115590#c11 if that's possible. 

### ad...@google.com (2020-10-22)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-22)

Aha, I hadn't spotted https://crbug.com/chromium/1115590#c11. Yes, I understand where you're coming from, but I'm afraid our rules are pretty firm here. It's often hard for the VRP panel to determine the correct reward amount until the fix has actually landed, so we can't and don't give early payouts. Sorry!

This reward is now submitted to our finance team and they will get in touch. I should warn you... that process can sometimes take a few weeks as well, for initial enrollment. Assuming you find lots more valid bugs, subsequent rewards should be much more efficient :)

### gh...@gmail.com (2020-10-22)

No worries. I am working on converting assumptions to reality. :)
Thanks :)

### ad...@google.com (2020-11-23)

cc chamal.desilva@gmail.com as requested by e-mail, given that this bug is cited from https://crbug.com/chromium/1134338.

### gh...@gmail.com (2020-12-23)

Wondering, when its getting patched in stable ?

### rd...@chromium.org (2020-12-23)

The fix landed in M88, which is currently slated to reach stable on Jan 19.

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5eaa1618eb73c224ad154f7297bb200698e44472

commit 5eaa1618eb73c224ad154f7297bb200698e44472
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Thu Jan 21 18:38:43 2021

[CSP] Do not bypass CSP:frame-ancestors

Extensions can load their own internal content into the document. They
shouldn't be blocked by the document's CSP.

There is an exception: CSP:frame-ancestors. This one is not about
allowing a document to embed other resources. This is about being
embedded. As such this shouldn't be bypassed. A document should be able
to deny being embedded inside an extension.

(cherry picked from commit fd406771ba8565e5c58563b5492d45fe2ba5a3c8)

Bug: 1115590
Change-Id: I2176a25e67cd0d637ecb3b13a39de30259d9d7a1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2467897
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#817859}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2639764
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1526}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/5eaa1618eb73c224ad154f7297bb200698e44472/services/network/public/cpp/content_security_policy/csp_context.cc
[add] https://crrev.com/5eaa1618eb73c224ad154f7297bb200698e44472/chrome/test/data/extensions/csp/frame-ancestors-none.html
[add] https://crrev.com/5eaa1618eb73c224ad154f7297bb200698e44472/chrome/test/data/extensions/csp/frame-ancestors-none.html.mock-http-headers
[modify] https://crrev.com/5eaa1618eb73c224ad154f7297bb200698e44472/chrome/browser/extensions/extension_csp_bypass_browsertest.cc
[modify] https://crrev.com/5eaa1618eb73c224ad154f7297bb200698e44472/services/network/public/cpp/content_security_policy/content_security_policy.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd406771ba8565e5c58563b5492d45fe2ba5a3c8

commit fd406771ba8565e5c58563b5492d45fe2ba5a3c8
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Fri Oct 16 09:59:28 2020

[CSP] Do not bypass CSP:frame-ancestors

Extensions can load their own internal content into the document. They
shouldn't be blocked by the document's CSP.

There is an exception: CSP:frame-ancestors. This one is not about
allowing a document to embed other resources. This is about being
embedded. As such this shouldn't be bypassed. A document should be able
to deny being embedded inside an extension.

Bug: 1115590
Change-Id: I2176a25e67cd0d637ecb3b13a39de30259d9d7a1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2467897
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#817859}

[modify] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/services/network/public/cpp/content_security_policy/csp_context.cc
[add] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/chrome/test/data/extensions/csp/frame-ancestors-none.html
[add] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/chrome/test/data/extensions/csp/frame-ancestors-none.html.mock-http-headers
[modify] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/chrome/browser/extensions/extension_csp_bypass_browsertest.cc
[modify] https://crrev.com/fd406771ba8565e5c58563b5492d45fe2ba5a3c8/services/network/public/cpp/content_security_policy/content_security_policy.cc


### ja...@google.com (2021-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1115590?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053061)*
