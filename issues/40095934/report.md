# SOP & Site Isolation bypass with Reader mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40095934](https://issues.chromium.org/issues/40095934) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>ReaderMode |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | wy...@chromium.org |
| **Created** | 2019-08-08 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Reader mode allows loading of untrusted image, videos, etc in chrome-distiller://[GUID] origin. Further more, there seems to be weak sanitization of contents. For example, <button> tag can contain `onclick` attribute. But this will be blocked by default CSP set in Reader mode. You can see all of this evidence by loading following page in Reader mode.  

<https://attack.shhnjk.com/reader_mode.html>

All of above fact seems to indicate that Reader mode process could theoretically be compromised (by image/video parsing bug) or run arbitrary script with CSP bypass.

Once renderer process is compromised or CSP is bypassed, attacker can run JS in chrome-distiller://[GUID]. While GUID in URL's hostname is different for different Reader mode pages, attacker can open new window with same GUID. And there is a url query parameter, that will be used to determine which content to load in Reader mode. So combining both of this, arbitrary website's content can commit into same-origin. After that, attacker can just call DOM APIs to access contents in other window to access cross-origin data.

There is additional small bug in Reader mode, where they don't inherit CSP of original site, so CSP in original site can be bypassed when viewed via Reader mode.

**VERSION**  

Chrome Version: 76 stable (with chrome://flags/#enable-reader-mode enabled)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Enable chrome://flags/#enable-reader-mode
2. Go to <https://attack.shhnjk.com/reader_mode.html>
3. Click Menu -> Distill page
4. Observe that image which was blocked by CSP is now loaded
5. Open devtools and run following script in the console  
   
   url = "<https://twitter.com/messages>";  
   
   window.open(url,"w");  
   
   setTimeout(()=>{w=window.open(origin+"/?url="+url,"w");},3000);  
   
   interval=setInterval(()=>  
   
   {try{alert(w.document.body.innerHTML);clearInterval(interval)}catch(e)  
   
   {}},1000);
6. Wait for few seconds and observe that your Twitter message is alerted

## Attachments

- [reader_mode.html](attachments/reader_mode.html) (text/plain, 754 B)

## Timeline

### Ju...@microsoft.com (2019-08-08)

[Empty comment from Monorail migration]

### ke...@chromium.org (2019-08-08)

Security_Impact-None because this is disabled by default.

Charlie do you know who the best person to own this would be?

### Ju...@microsoft.com (2019-08-08)

Isn’t Reader mode enabled by default in mobile platforms?

### lu...@chromium.org (2019-08-08)

FWIW, it seems that chrome::android::kReaderModeInCCT is enabled by default:

//chrome/browser/android/chrome_feature_list.cc:
    const base::Feature kReaderModeInCCT{"ReaderModeInCCT",
                                         base::FEATURE_ENABLED_BY_DEFAULT};

So, maybe it is Security_Impact-Stable after all?

### lu...@chromium.org (2019-08-08)

wychen@, could you PTAL to triage this further? (since you've landed r582956 which enabled chrome::android::kReaderModeInCCT by default)

Also CC-ing mdjones@ and gilmanmh@ who are listed as flag owners in //chrome/browser/flag-metadata.json:
    {
      "name": "enable-reader-mode",
      "owners": [ "gilmanmh@google.com" ],
    ...
    {
      "name": "enable-reader-mode-in-cct",
      "owners": [ "mdjones" ],

### wy...@chromium.org (2019-08-08)

It's on by default on Android as "Simplified view", which is only available for non-mobile-friendly articles by default. On iOS, it's on by default and used in the offline mode of reading list. For desktop platforms, this is off by default for now. So, Security_Impact-Stable for Android and iOS, but Security_Impact-None for desktop.

I can confirm that DOM distiller doesn't sanitize the output fully, and attributes like onclick can be wrongly retained. This is why we block 'inline' in CSP. If this is chained with CSP bypass vulnerability, attacker can run JS in chrome-distiller://[GUID]. One way to fix this is to sanitize better by making an allow-list for attributes in DOM distiller and remove everything else.

Another issue is that the URL parameter is not checked when chrome-distiller://[GUID]?url=xxx is accessed. We always assume the URL is constructed by Chrome, but in the example above, with CSP bypass vulnerability and unsanitized DOM distiller output, the distilled content of arbitrary web pages can be read. One way to mitigate this is to use CSP 'sandbox' to stop window.open(), but I'm not sure if this makes much sense since we already assumed CSP bypass vulnerability. This might still make sense because a vulnerability breaking 'inline' doesn't necessarily break 'sandbox'. Another possible mitigation is to append URLs to a per-GUID allow-list before navigating there. This way, attacks from JS can be blocked, even if the URL is used in other reader mode sessions.

Inheriting CSP of original site can be tricky to get right. If done wrong, we would wrongly relax our own CSP. Is there a safe way to get the intersection of multiple CSP rules? Normally, web pages including something blocked by their own CSP rule is considered a bug on that page. That's why we decided not to consider the CSP of the original site. Of course, if this is chained with an XSS vulnerability on that page that would have been block by the site CSP, then it can be leaked to distilled content.

I'm not an expert so all above needs to be reviewed by security.

### lu...@chromium.org (2019-08-08)

nasko@ points out that Site Isolation hasn't shipped to Android yet, so we should probably demote Security_Impact-Stable to Security_Impact-Beta.

### wy...@chromium.org (2019-08-08)

The "site isolation" in the title might not be the same as our "Site Isolation" feature. The scenarios described in this bug seem orthogonal to whether our "Site Isolation" feature is turned on or not, since none of them uses iframes. Feel free to add the component back if my assessment is wrong.

[Monorail components: -Internals>Sandbox>SiteIsolation]

### Ju...@microsoft.com (2019-08-08)

>Another possible mitigation is to append URLs to a per-GUID allow-list before navigating there
This seems preferable, as CSP sandbox wouldn't trigger process separation by Site Isolation, since GUID will be same (event though origin will be different).
And I think if you register URL to specific GUID, then I don't think there will be a necessity of url parameter anymore. Which will completely eliminate this attack surface.

>Is there a safe way to get the intersection of multiple CSP rules?
You can have 2 CSP headers or meta tag, and it'll only make CSP stricter, not weaker, as long as it is separated.
One thing that you need to be care full though is that you would still want Reader mode resources to be loaded (e.g. CSS file). So you should make sure that your "safe" resource serving endpoint is not restricted by original CSP of the page.

### lu...@chromium.org (2019-08-08)

RE: https://crbug.com/chromium/991888#c8
Site Isolation attempts to restrict one site (e.g. attacker.com) from being able to access data of another site (e.g. victim.com) even if they don't include any subframes, (e.g. if the separate sites are in separate popups or tabs or browsing instances).  In that sense, this bug does seem to be a Site Isolation problem, because an attacker-controlled site can force content from a victim's site to share the same renderer process as an attacker-controlled content/scripts.

[Monorail components: Internals>Sandbox>SiteIsolation]

### na...@chromium.org (2019-08-08)

The root problem in my mind would be "... the URL parameter is not checked when chrome-distiller://[GUID]?url=xxx is accessed". Why does chrome-distiller:// even allow this to happen? It means that basically it acts as a proxy for all web content. This seems problematic to me and it will be useful to understand what is the goal of this feature and maybe we can modify it in some way to be safer and not serve cross-origin content without any checks.

As far as whether CSP will save us or not - we must assume that any renderer process can execute arbitrary attacker code, therefore we must protect the browser side in such a threat model. CSP is enforced in the renderer process, so we cannot rely on it at all. We must assume all requests coming from the renderer process can be malicious.

### wy...@chromium.org (2019-08-08)

Re: https://crbug.com/chromium/991888#c10
Ah, I was thinking about OOPIF, which is only a subset of what Site Isolation does. Thanks for the clarification!

Re: https://crbug.com/chromium/991888#c9
If CSP sandbox is used without 'allow-popups', all window.open() calls would silently fail, right? In that case, if script-src 'unsafe-inline' is used, specifying 'sandbox' would still make it safer. Does this make sense?


### Ju...@microsoft.com (2019-08-08)

Re: https://crbug.com/chromium/991888#c12
But what if an attacker has a way to compromise Reader mode process with allows tags and attributes (e.g. image, video, etc)? That would allow attacker to remove all restriction applied within the process including CSP sandbox.

### na...@chromium.org (2019-08-08)

Re: https://crbug.com/chromium/991888#c12, we cannot rely on CSP to be our defense against attackers. We have to structure distiller to work safely even when the renderer process is fully compromised and can execute arbitrary code.

### sh...@chromium.org (2019-08-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wy...@chromium.org (2019-08-20)

What is the expected timeline of fixing this issue? I'm planning to remove the url parameter in M78, and better distiller sanitation in M79. Sounds reasonable?

### lu...@chromium.org (2019-08-20)

RE: https://crbug.com/chromium/991888#c2: kenrb@ and other security sheriffs:

Why is this a Security_Severity-Medium?  I think this bug falls into the "Cross-site execution contexts unexpectedly sharing a renderer process despite Site Isolation" category which is a high severity [1].

RE: https://crbug.com/chromium/991888#c16: wychen@:

alexmos@, would you be able to comment on the expected fix timelines (since you are driving shipping Site Isolation for Android in M77)?  FWIW, our guidance [1] says that high severity bugs "are normally assigned priority Pri-1 and assigned to the current stable milestone" and that "SheriffBot will automatically assign the milestone".

[1] https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-high-severity

### cr...@chromium.org (2019-08-20)

https://crbug.com/chromium/991888#c17: I agree with the High severity rating (and Beta impact, since Site Isolation hasn't shipped on Android until M77).  The link you point to shows that we aim to get High severity fixes to all users in 60 days, which would indeed be targeting M77 given the August 8 report date.

wychen@: Let's try to get the URL parameter removed ASAP and we can discuss merge options.

I think we might have to do another step as well-- if the Reader mode page is operating on an isolated origin, we need to lock the Reader mode process to that origin, so that it won't share a process or leak data.  Doing that might make the sanitization less important, since cross-site data won't enter the process at that point.  We can meet to discuss if that helps, and alexmos@ can point to the right logic for locking the Reader process when needed.  Thanks!

### cr...@chromium.org (2019-08-20)

To clarify, I don't know if we'll be able to make the M77 target.  It may be the case that the fix needs to be M78 if it's too large, especially since we don't know the full extent of the changes needed yet.  I'm leaving this as targeting M77 for the moment given the security guidelines, but let's figure out what's needed and whether that will be achievable.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7be7426134cc4978a253f3be6dcdbf77ee25702f

commit 7be7426134cc4978a253f3be6dcdbf77ee25702f
Author: Aaron Colwell <acolwell@google.com>
Date: Thu Aug 22 18:25:12 2019

Require dedicated process for all WebUI schemes.

This changes SiteInstanceImpl::DoesSiteURLRequireDedicatedProcess() to
return true for all WebUI schemes instead of just singling out the
chrome: scheme. This ensures that these URLs get placed in dedicated
processes even if site isolation is disabled.

Bug: 991153,991888
Change-Id: I1af3b87ac39d93f6e45587a5b3845a176f98b7bd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1763643
Commit-Queue: Aaron Colwell <acolwell@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#689561}

[modify] https://crrev.com/7be7426134cc4978a253f3be6dcdbf77ee25702f/content/browser/site_instance_impl.cc
[modify] https://crrev.com/7be7426134cc4978a253f3be6dcdbf77ee25702f/content/browser/site_instance_impl_unittest.cc


### al...@chromium.org (2019-08-22)

r689561 should address the second part of https://crbug.com/chromium/991888#c18, in that we'll now use a process lock with chrome-distiller:// URLs.  The lock will be of form "chrome-distiller://guid" which should prevent the reader process from accessing data from other sites (or other sites entering that process), including the site from which the distiller page was constructed.  This isn't expected to break any reader functionality, and it already works like this if you manually turn on reader mode on desktop platforms, where we require a dedicated process for everything.  (Some internal discussion at https://groups.google.com/a/google.com/d/msg/chrome-site-isolation/T4zitsfod6w/IgM6rQMUBAAJ.)

We still need to fix the URL parameter vulnerability.

### cr...@chromium.org (2019-08-23)

Right.  Here's the current summary, as I understand it:

Reader mode pages load chrome-distiller://guid pages from a WebUI data source, but they do not have any WebUI bindings or capabilities in the renderer process.  (That's good, because it means any renderer compromise or CSP bypass doesn't lead to WebUI privileges.)  They use the data source to fetch distilled content from a URL that is currently specified as a URL parameter, and the renderer process can fetch subresources from any site.  There are no iframes in distilled pages, which simplifies the security model: there's only one origin, which is chrome-distiller://guid (and thus has no access to web origins).

Since the goal is to enable Site Isolation on Android in M77, we want Reader mode to be robust to compromised renderers in M77 if possible.  We also want to address the other issues found in this report if possible.  The current proposal has 4 parts:

1) Validate the URL parameter so that any given Reader mode process is limited to distilled content from a single site.

wychen@ noted offline that removing the URL parameter makes it hard for Reader mode to work after a session restore, unless the mapping of GUID to URL is persisted.  Instead, it should be sufficient to ensure that each Reader mode process can only ask its data source for content from a single site.  For example, a hash of the origin could be appended to the GUID as part of the hostname, which (when combined with Site Isolation for chrome-distiller:// URLs) ensures that (1) distilled content from different sites end up in different processes, and (2) there's a way to validate that the URL parameter matches the hashed origin before returning it.  Something along the lines of:

chrome-distiller://[GUID]-[hash(https://foo.com)]/?url=https://foo.com/article.html

The data source would reject requests for https://bar.com from a process locked to chrome-distiller://[GUID]-[hash(https://foo.com)].

Goal: Land in M78.  Merge to M77 if possible.


2) Lock processes containing chrome-distiller:// origins using Site Isolation on Android.

In the example above, the process would be locked to chrome-distiller://[GUID]-[hash(https://foo.com)], which means it would not have access to cookies, passwords, stored data, etc for any web site (including https://foo.com), which is fine for Reader mode.  It would also ensure CORB prevents pulling in HTML/XML/JSON for any sites, and that the only way to get HTML content is via the data source.  (This change has already landed in r689561.)

Goal: Merge r689561 to M77.


3) Improve sanitization when distilling.

Use an allowlist of attributes to make it harder to include script code that might abuse a CSP bypass.  This is purely a nice-to-have, since we have to assume a rogue subresource (e.g., image) is sufficient to exploit the reader process to run arbitrary code, with or without this sanitization.

Goal: M79


4) Find a way to inherit the page's CSP, if possible.

Sounds like we might be able to include both the page's and Reader's CSP policies, if we're careful not to block Reader's code (per https://crbug.com/chromium/991888#c9).  This seems mostly orthogonal to the SI bypass, but it might be worth addressing if we can (so that distilled content doesn't show things that are blocked in the original page).

Goal: M79?


Parts 1 and 2 are the most important to fix, and the reason for the High severity rating.  Seems reasonable to me to treat parts 3 and 4 as followup bugs with lower severity, as long as the reporter gets credit for them.

I'll be OOO until Sep 4, but it sounds like we've got a plan.  alexmos@ or nasko@ can probably help with any Site Isolation advice from here. Thanks!

### ac...@chromium.org (2019-08-26)

Requesting merge of https://chromium-review.googlesource.com/c/chromium/src/+/1763643 to M-77 branch. It has been available on canary for 3 days and I haven't seen any crashes related to it.

### sh...@chromium.org (2019-08-26)

This bug requires manual review: Less than 11 days to go before AppStore submit on M77
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

### ac...@chromium.org (2019-08-26)

Answers to questions in https://crbug.com/chromium/991888#c24
1. Yes. This is part of the fix for a release blocking security bug.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1763643
3. Yes. It landed last Thursday and has been in the Canary build for the last 3 days. No crashes related to this change have been observed.
4. This security issue was discovered & reported after branch cut.
5. No.
6. No.

### la...@google.com (2019-08-27)

merge approved for M77 branch 3865

### sh...@chromium.org (2019-08-27)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@google.com (2019-08-27)

<Bulk Update> M77 Stable cut is in one week (Sept 3) and this issue is currently marked to block Stable. Please make sure any planned work will be tested in Beta and verified before the Stable cut date, Sept 3.


### ac...@chromium.org (2019-08-27)

Reopening because all aspects of this bug are not fixed yet. Specifically item 1 in https://crbug.com/chromium/991888#c22 does not appear to be fixed yet. The commit in https://crbug.com/chromium/991888#c20 only addresses item 2 in https://crbug.com/chromium/991888#c22.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b368f94d3afdebd3d5002f8f653ada8083270dd7

commit b368f94d3afdebd3d5002f8f653ada8083270dd7
Author: Aaron Colwell <acolwell@google.com>
Date: Tue Aug 27 15:25:25 2019

Require dedicated process for all WebUI schemes.

This changes SiteInstanceImpl::DoesSiteURLRequireDedicatedProcess() to
return true for all WebUI schemes instead of just singling out the
chrome: scheme. This ensures that these URLs get placed in dedicated
processes even if site isolation is disabled.

(cherry picked from commit 7be7426134cc4978a253f3be6dcdbf77ee25702f)

Bug: 991153,991888
Change-Id: I1af3b87ac39d93f6e45587a5b3845a176f98b7bd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1763643
Commit-Queue: Aaron Colwell <acolwell@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#689561}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1773161
Reviewed-by: Aaron Colwell <acolwell@chromium.org>
Cr-Commit-Position: refs/branch-heads/3865@{#595}
Cr-Branched-From: 0cdcc6158160790658d1f033d3db873603250124-refs/heads/master@{#681094}

[modify] https://crrev.com/b368f94d3afdebd3d5002f8f653ada8083270dd7/content/browser/site_instance_impl.cc
[modify] https://crrev.com/b368f94d3afdebd3d5002f8f653ada8083270dd7/content/browser/site_instance_impl_unittest.cc


### wy...@chromium.org (2019-08-27)

[Empty comment from Monorail migration]

### wy...@chromium.org (2019-08-27)

[Empty comment from Monorail migration]

### na...@chromium.org (2019-08-28)

wychen@, would you be able to give us an estimate when the URL query parameter validation (part 1 from https://crbug.com/chromium/991888#c22) will be able to land? Branch cut is coming up in a week and we should aim to have a fix landed before that.

### wy...@chromium.org (2019-08-29)

An ongoing CL is here: https://chromium-review.googlesource.com/c/chromium/src/+/1763628

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1bb21e333978666d8a67593bd267a4f88df90b2a

commit 1bb21e333978666d8a67593bd267a4f88df90b2a
Author: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Date: Wed Sep 04 04:26:29 2019

Validate the URL parameter in DOM distiller viewer

In chrome-distiller:// URLs, validate the URL parameter by adding
its hash as part of the host. This way, changing the URL parameter
requires changing the origin as well, so it's harder to be misused.

TBR=sky@chromium.org

Bug: 991888
Change-Id: Ida641f697d77a2c9c1a93266208a55c0e773aeaa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1763628
Commit-Queue: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Reviewed-by: David Benjamin <davidben@chromium.org>
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Cr-Commit-Position: refs/heads/master@{#693009}

[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/chrome/browser/dom_distiller/dom_distiller_viewer_source_browsertest.cc
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/DEPS
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/content/browser/dom_distiller_viewer_source.cc
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/core/url_utils.cc
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/core/url_utils.h
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/core/url_utils_unittest.cc
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/core/viewer.cc
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/core/viewer.h
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/dom_distiller/core/viewer_unittest.cc
[modify] https://crrev.com/1bb21e333978666d8a67593bd267a4f88df90b2a/components/test/components_test_suite.cc


### be...@chromium.org (2019-09-04)

Do we need to get the CL in c#35 into M77?

### be...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### wy...@chromium.org (2019-09-04)

I think we want to merge this into M77. Do we wait for Canary build in this case as well? It's not available yet.

### sh...@chromium.org (2019-09-04)

This bug requires manual review: Less than 2 days to go before AppStore submit on M77
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

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fee9c9d0b1576831d914259b5f21a6c18101fd06

commit fee9c9d0b1576831d914259b5f21a6c18101fd06
Author: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Date: Wed Sep 04 18:10:18 2019

Validate the URL parameter in DOM distiller viewer

In chrome-distiller:// URLs, validate the URL parameter by adding
its hash as part of the host. This way, changing the URL parameter
requires changing the origin as well, so it's harder to be misused.

TBR=sky@chromium.org

(cherry picked from commit 1bb21e333978666d8a67593bd267a4f88df90b2a)

Bug: 991888
Change-Id: Ida641f697d77a2c9c1a93266208a55c0e773aeaa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1763628
Commit-Queue: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Reviewed-by: David Benjamin <davidben@chromium.org>
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#693009}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1785257
Reviewed-by: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/3902@{#6}
Cr-Branched-From: e1d18c78bda33e0cc8a853a8e5d0114b5d62a559-refs/heads/master@{#692639}

[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/chrome/browser/dom_distiller/dom_distiller_viewer_source_browsertest.cc
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/DEPS
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/content/browser/dom_distiller_viewer_source.cc
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/core/url_utils.cc
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/core/url_utils.h
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/core/url_utils_unittest.cc
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/core/viewer.cc
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/core/viewer.h
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/dom_distiller/core/viewer_unittest.cc
[modify] https://crrev.com/fee9c9d0b1576831d914259b5f21a6c18101fd06/components/test/components_test_suite.cc


### be...@chromium.org (2019-09-04)

Yes, let's see how it fares in Canary, I have cherry picked it to latest canary and kicked off a build again.

### ka...@google.com (2019-09-04)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-09-05)

Canary is out, can we get a verification for this?

### wy...@chromium.org (2019-09-05)

It is verified on Canary. Request merging https://crbug.com/chromium/991888#c35 to M77.

Jun, would you mind taking another look at Canary 78.0.3903.0? This is released on Windows as well. We've addressed the open proxy issue, but the sanitization and CSP issues are still ongoing.


### sh...@chromium.org (2019-09-05)

This bug requires manual review: Less than 1 days to go before AppStore submit on M77
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

### Ju...@microsoft.com (2019-09-05)

https://crbug.com/chromium/991888#c44: Yup, seems like this is now fixed.

### wy...@chromium.org (2019-09-05)

Answers to questions in https://crbug.com/chromium/991888#c45
1. Yes. This is part of the fix for a release blocking security bug.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1763628
3. Yes. The Canary build is verified by CL author and reporter.
4. This security issue was discovered & reported after branch cut.
5. No.
6. No.

### sr...@google.com (2019-09-05)

adetaylor@ can you review how critical is this to merge to M77  with just canary coverage

### ad...@google.com (2019-09-05)

It's a tough one. Looking into it right now (and thanks for the ping wychen@)

### ad...@google.com (2019-09-05)

I talked it through this nasko@ and wychen@. Yes - please merge. It's a little riskier than we'd normally like, but the fix is relatively straightforward, and it would be very disappointing l to have a known site isolation bypass in the first release where Android site isolation is launching.

There is one known problem that some users will encounter: if they have tabs open in distiller mode before the upgrade, those tabs will show an error after the upgrade. In this case, hitting "back" will get them back to the non-distilled version. srinivassista@, if you think that rules out us putting this into M77 then we should discuss further.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f302c75a95ec3a1d8941f703e8933a94812545fd

commit f302c75a95ec3a1d8941f703e8933a94812545fd
Author: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Date: Fri Sep 06 01:06:17 2019

Validate the URL parameter in DOM distiller viewer

In chrome-distiller:// URLs, validate the URL parameter by adding
its hash as part of the host. This way, changing the URL parameter
requires changing the origin as well, so it's harder to be misused.

TBR=sky@chromium.org

(cherry picked from commit 1bb21e333978666d8a67593bd267a4f88df90b2a)

Bug: 991888
Change-Id: Ida641f697d77a2c9c1a93266208a55c0e773aeaa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1763628
Commit-Queue: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Reviewed-by: David Benjamin <davidben@chromium.org>
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#693009}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1787564
Reviewed-by: Wei-Yin Chen (陳威尹) <wychen@chromium.org>
Cr-Commit-Position: refs/branch-heads/3865@{#762}
Cr-Branched-From: 0cdcc6158160790658d1f033d3db873603250124-refs/heads/master@{#681094}

[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/chrome/browser/dom_distiller/dom_distiller_viewer_source_browsertest.cc
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/DEPS
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/content/browser/dom_distiller_viewer_source.cc
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/core/url_utils.cc
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/core/url_utils.h
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/core/url_utils_unittest.cc
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/core/viewer.cc
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/core/viewer.h
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/dom_distiller/core/viewer_unittest.cc
[modify] https://crrev.com/f302c75a95ec3a1d8941f703e8933a94812545fd/components/test/components_test_suite.cc


### la...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### wy...@chromium.org (2019-09-09)

The vulnerability is patched in M77. Dropping ReleaseBlock-Stable. We still have some follow-up work that'd not block release, so keep this bug open for now.

### Ju...@microsoft.com (2019-09-09)

Hi, is it possible to CC me on follow-up bugs (especially on the sanitization of the content)? Thanks!

### wy...@chromium.org (2019-09-09)

Will do. Thanks for reporting the bug!

### sh...@chromium.org (2019-09-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### dg...@google.com (2019-09-16)

Adding ReleaseBlock-NA due to https://crbug.com/chromium/991888#c55 and comment # 58.

### Ju...@microsoft.com (2019-09-20)

Is this bug fixed?

### ad...@chromium.org (2019-09-23)

wychen@ re https://crbug.com/chromium/991888#c55, could we possibly close this bug and do the follow-up work in another crbug? I'd be happy to raise the follow-up bug. Because then we can get this properly credited in release notes, start the VRP process, award a CVE etc. Thanks!

### sh...@chromium.org (2019-09-24)

wychen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wy...@chromium.org (2019-09-25)

Yes, this bug is fixed. I'll have another bug for the follow-up work. Thanks for reporting it, Jun!

### sh...@chromium.org (2019-09-26)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-26)

wychen@ thanks! I assume from https://crbug.com/chromium/991888#c64 you'll file a follow-up crbug but let me know if you want me to file a placeholder.

### ad...@google.com (2019-09-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### wy...@chromium.org (2019-09-27)

[Empty comment from Monorail migration]

### wy...@chromium.org (2019-10-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $5,000 for this report :) 

### cr...@chromium.org (2019-10-09)

Comments 64, 66: I filed https://crbug.com/chromium/1012955 for the sanitization issue and https://crbug.com/chromium/1012956 for the CSP inheritance issue.  That should take care of parts 3 and 4 from https://crbug.com/chromium/991888#c22.

### Ju...@microsoft.com (2019-11-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

wychen@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/991888?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>ReaderMode]
[Monorail blocked-on: crbug.com/chromium/1009127]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095934)*
