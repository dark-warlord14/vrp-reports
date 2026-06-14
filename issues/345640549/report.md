# heap-use-after-free in in content::RemoveWebUIManagedInterfaces

| Field | Value |
|-------|-------|
| **Issue ID** | [345640549](https://issues.chromium.org/issues/345640549) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation, UI>Browser>WebUI |
| **Platforms** | Windows |
| **Chrome Version** | 127.0.6524.1 |
| **Reporter** | xp...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2024-06-07 |
| **Bounty** | $2,500.00 |

## Description

# Steps to reproduce the problem

Hi happy friday,

2 methods to reproduce this UAF.

# Extension Method (automatic)

1. Make sure Chrome has only 1 tab open in current window. Only the chrome://extension tab.
2. Add poc.zip to Chrome

# Manual Method:

1. Visit chrome://print/ from URL bar.
2. Visit chrome://print/1 from URL bar
3. Press back button.
4. Press forward button.

I can reproduce in Stable.

# Problem Description

UAF in content::RemoveWebUIManagedInterfaces at RenderFrameHost\* rfh = webui\_controller->web\_ui()->GetRenderFrameHost();

# Additional Comments

Bisect:

You are probably looking for a change made after 1150389 (known good), but no later than 1150401 (first known bad).
CHANGELOG URL:
<https://chromium.googlesource.com/chromium/src/+log/51513d937d1e1ebb5c5134083c695f35ca895083..77b19d7e83c7ee09bd488df602ecaa4385403e04>

# Summary

heap-use-after-free in in content::RemoveWebUIManagedInterfaces

# Custom Questions

#### Type of crash:

browser

#### Reporter credit:

Sven Dysthe @svn-dys

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [NVIDIA_Share_dQ8ZSiZ8zv.gif](attachments/NVIDIA_Share_dQ8ZSiZ8zv.gif) (image/gif, 12.9 MB)
- [_asan_.txt](attachments/_asan_.txt) (text/plain, 20.8 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 1.1 KB)

## Timeline

### li...@chromium.org (2024-06-07)

I think <https://chromium.googlesource.com/chromium/src/+/0c460a3a47a5d22c04049b39cf0ebd22bfc3a3a0> might be the culprit CL since the UAF happens in the print webUI.

Assigning to thestig@ to confirm.

I did successfully repro this using the manual method, but I don't see the PoC.zip uploaded. Based on the gif it looks like it uses the Tabs API to automate the manual step anyways, so I think repro-ing with just the manual steps is sufficient.

Marking this as high severity instead of critical because even though this is memory corruption in the browser, the bug requires manual UI interactions or downloading a malicious extension to trigger, which is considered a mitigating factor.

### th...@chromium.org (2024-06-07)

Is poc.zip not attached to the bug, or did I miss it?

### th...@chromium.org (2024-06-07)

While this may be happening in PrintPreviewUI, the same issue can happen with other WebUIs as well. Considering <https://chromium.googlesource.com/chromium/src/+/0c460a3a47a5d22c04049b39cf0ebd22bfc3a3a0> is not doing anything out of the ordinary. IMO this is an issue in how content::NavigationRequest::CreateWebUIIfNeeded() is managing WebUI objects, so reassigning to rakina@ to take a look.

### li...@chromium.org (2024-06-07)

The PoC.zip is not attached, reporter if you could attach it that would be helpful.

However following the manual repro steps they shared should allow you to repro this.

### xp...@gmail.com (2024-06-07)

I'm very sorry. I'll be home soon and I will upload.

### xp...@gmail.com (2024-06-07)

Here is the extension repro.

### li...@chromium.org (2024-06-07)

Thank you! I ran the extension and also successfully repro'd the bug this way, just as an FYI for rakina@

### pe...@google.com (2024-06-07)

Setting milestone because of s0/s1 severity.

### cr...@chromium.org (2024-06-07)

I uploaded a crash report with the manual repro steps at <http://crash/c5af7601b0d0f92f>, which lets us see the lines responsible for the free.

The relevant part of NavigationRequest::CreateWebUIIfNeeded is:
<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;drc=c77135fb31a26e2b8243e206bd01778f7ce263f9;l=10383-10406>

```
  web_ui_ = std::make_unique<WebUIImpl>(this);
  std::unique_ptr<WebUIController> controller(
      WebUIControllerFactoryRegistry::GetInstance()
          ->CreateWebUIControllerForURL(web_ui_.get(), GetURL()));

  // If we have assigned (zero or more) bindings to the NavigationEntry in
  // the past, make sure we're not granting it different bindings than it
  // had before. If so, note it and don't give it any bindings, to avoid a
  // potential privilege escalation.
  if (bindings() != FrameNavigationEntry::kInvalidBindings &&
      bindings() != web_ui_->GetBindings()) {
    RecordAction(base::UserMetricsAction("ProcessSwapBindingsMismatch_RVHM"));
    base::WeakPtr<NavigationRequest> self = GetWeakPtr();
    web_ui_.reset();
    // Resetting the WebUI may indirectly call content's embedders and delete
    // `this`. There are no known occurrences of it, so we assume this never
    // happen and crash immediately if it does, because there are no easy ways
    // to recover.
    CHECK(self);
    return;
  }

  web_ui_->SetController(std::move(controller));
}

```

We are getting here on a forward navigation to chrome://print/1, which is not a valid URL and didn't get bindings on the previous visit. This means that bindings() is 0, which isn't kInvalidBindings (i.e., -1), and doesn't match the new WebUI object's bindings (i.e., 1), so we enter the ProcessSwapBindingsMismatch\_RVHM case. That's useful to know on its own-- we should probably find a way to avoid getting into this case.

The specific UaF outcome happens because of the `web_ui_.reset();` line, which deletes the WebUI object while `controller` is still referring to it. Then the early return causes `controller` to go out of scope, at which point it dereferences the already-deleted WebUI object as part of its destructor in RemoveWebUIManagedInterfaces [here](https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/web_ui_managed_interface.cc;drc=aee7aa3cddd6682a597d0e7be60d6590eee482f8;l=52).

At the least, we should be deleting `controller` first or ensuring it doesn't point to `web_ui_` before we delete `web_ui_`, but presumably there's another fix that would avoid getting into this situation to begin with as well.

CC'ing nasko@ who has also been looking at this with me.

### cr...@chromium.org (2024-06-08)

Nasko spotted the connection to thestig@'s change in <https://chromium-review.googlesource.com/c/chromium/src/+/4569063>. At the time, that code in GetWebUIFactoryFunction was updated to look like:

```
  if (url.host_piece() == chrome::kChromeUIPrintHost) {
    if (profile->GetPrefs()->GetBoolean(prefs::kPrintPreviewDisabled))
      return nullptr;
    // Filter out everything except chrome://print/ and test_loader.html.
    if (url.path() != "/" && url.path() != "/test_loader.html") {
      return nullptr;
    }
    return &NewWebUI<printing::PrintPreviewUI>;
  }

```

This means you could navigate from chrome://print/ (which is valid and created a PrintPreviewUI WebUI object) to chrome://print/1 (which doesn't pass the path check and thus returns nullptr here).

At first I thought that the same-site navigation from chrome://print/ to chrome://print/1 was to blame, and that we were somehow inheriting the WebUI object by staying in the same RenderFrameHost. But that's not it at all-- it turns out that once chrome://print/ creates the URLDataSource, it is available to any tab in the future, including the invalid chrome://print/1 request (which does happen in a new RFH). That means there are additional repro steps for this crash:

1. Visit chrome://print/
2. Create a second tab, close the first one, and navigate the second tab to chrome://print/1.
3. Navigate the second tab to example.com.
4. Go back. Crashes with the same UaF.

(If you skip step 1, navigating to chrome://print/1 doesn't work because there is no URLDataSource for it.)

When we return to chrome://print/1 in session history, we notice the mismatch from the FrameNavigationEntry's missing bindings and try (unsuccessfully) to handle it by clearing the WebUI object, but that causes the UaF because the controller isn't also cleared.

It looks like these steps do not crash for most WebUI pages, because most cases in GetWebUIFactoryFunction are based on the host and not the path. That means that any host with a URLDataSource will have WebUI throughout the host, rather than having some URLs that don't get a WebUI object but still have a successfully committed page in session history.

In contrast, the chrome://print case is path-dependent, so it's possible to navigate to a successful page from the URLDataSource but without a WebUI. It looks like that was the case even before thestig@'s CL, so pre-M116 you could probably have crashed like this by navigating from chrome://print to chrome://print/pdf/index.html.

Looking at GetWebUIFactoryFunction, it appears the DevTools case might also return nullptr for path or query dependent checks, so that's another way this bug might happen:
<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/chrome_web_ui_controller_factory.cc;drc=f4096571c202d7aa7e5c9d9b8dc9edebbbeb631e;l=613>

It also appears the chrome://print logic has moved somewhere else since M116, and I'm not sure where it lives now. It's possible other vulnerable cases might have been introduced since then as well.

In terms of fixes, I suspect that we'll want to both avoid the UaF (e.g., by deleting `controller` before `web_ui_` in this corner case), *and* prevent unsupported URLs from committing even when a URLDataSource exists.

rakina@ or nasko@: Can you help with these? The UaF fix is probably easy, and I'm less sure how to handle the URLDataSource situation. (Open to thoughts from thestig@ or other WebUI folks there.)

### th...@chromium.org (2024-06-10)

I'll see if the ability to navigate to chrome://print/1 as shown in [comment #11](https://issues.chromium.org/issues/345640549#comment11) can be removed.

The Print Preview code moved to chrome/browser/ui/webui/print\_preview/print\_preview\_ui.cc in <https://crrev.com/1217214>.

### th...@chromium.org (2024-06-11)

AFAICT, content::URLDataManagerBackend is going to hold on to the URLDataSource for the lifetime of a Profile. So trying to clean up didn't go anywhere.

### ra...@chromium.org (2024-06-11)

I can make a CL that just resets the controller before the WebUI object is reset, but Nasko / Charlie who actually investigated might be better authors? (I can do it if you don't have time, just don't want to take credit :D)

To solve the Non-UAF problem, I wonder if it's enough to make `WebUIControllerFactoryRegistry::GetWebUIType()` and `GetWebUIFactoryFunction()` be consistent by e.g. adding the path check in GetWebUIType as well? If we do that, step 2 in #comment12 won't create a WebUI object and the 0 bindings won't be saved in the FNE, right?

### cr...@chromium.org (2024-06-11)

Thanks! I won't have time to land a CL for this before next week (between meetings and packing my desk for a move today, and being OOO the rest of the week), so feel free to proceed with the fix!

### ap...@google.com (2024-06-19)

Project: chromium/src
Branch: main

commit c5dd8839bfaf4207a7db7a39c922daf67634936d
Author: Rakina Zata Amni <rakina@chromium.org>
Date:   Wed Jun 19 02:49:58 2024

    Destruct controller before referenced WebUI in CreateWebUIIfNeeded
    
    Reset `controller` first before resetting `web_ui_`, since the
    controller still has a pointer to `web_ui_`, to avoid referencing to
    the already deleted `web_ui_` object from `controller`'s destructor.
    
    Bug: 345640549
    Change-Id: Ie9c193436b593845d8269605f68bf94bc75beed7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5624749
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
    Reviewed-by: Nasko Oskov <nasko@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1316830}

M       content/browser/renderer_host/navigation_request.cc

https://chromium-review.googlesource.com/5624749


### ra...@chromium.org (2024-06-21)

The UaF itself should be fixed so I'm marking this as such, but nasko@ mentioned that there are some PDF improvements that can be done, to be discussed with thestig@.

### pe...@google.com (2024-06-21)

Requesting merge to stable (M126) because latest trunk commit (1316830) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1316830) appears to be after beta branch point (1313161).
Merge review required: M126 is already shipping to stable.

Merge review required: M127 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-06-25)

https://crrev.com/c/5624749 approved for merge 
Please merge this fix to M127 Beta / branch 6533 at soonest so this fix can be included in Wednesday's M127 Beta update 

M126 Stable update has already shipped for this week, please merge to branch 6478 at your convenience so this fix can be included in the first M126 Stable update following the forthcoming release freeze 

### ap...@google.com (2024-06-26)

Project: chromium/src
Branch: refs/branch-heads/6533

commit c010361c8e462dab4089e8e4e74cb8b6775b714d
Author: Rakina Zata Amni <rakina@chromium.org>
Date:   Wed Jun 26 17:25:46 2024

    [M127] Destruct controller before referenced WebUI in CreateWebUIIfNeeded
    
    Reset `controller` first before resetting `web_ui_`, since the
    controller still has a pointer to `web_ui_`, to avoid referencing to
    the already deleted `web_ui_` object from `controller`'s destructor.
    
    (cherry picked from commit c5dd8839bfaf4207a7db7a39c922daf67634936d)
    
    Bug: 345640549
    Change-Id: Ie9c193436b593845d8269605f68bf94bc75beed7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5624749
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
    Reviewed-by: Nasko Oskov <nasko@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316830}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5660217
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
    Auto-Submit: Rakina Zata Amni <rakina@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#726}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       content/browser/renderer_host/navigation_request.cc

https://chromium-review.googlesource.com/5660217


### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2500.00 for this report.

Rationale for this decision:
$2000 for report of highly mitigated memory corruption + $500 bisect bonus for partial bisect 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations Sven! Thank you for your efforts and reporting this issue to us.

### xp...@gmail.com (2024-06-27)

deleted

### am...@chromium.org (2024-06-28)

Hi Sven, the mitigations here are both the BRP protection and the precondition of installation of a malicious extension. 
During each VRP Panel session for each bug, we do go through all the information in each report throughly, including but not limited to what was included in the original report, but feedback from the engineers and looking through the code and patch. 

This does not mean that we never miss something or never make a mistake, but we try to ensure we are taking all information and bug impact into account when making a reward decision. 


### xp...@gmail.com (2024-06-29)

deleted

### pe...@google.com (2024-07-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-07-02)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 1d2eed9bb236665d05c8bb5e039413f25574d02d
Author: Rakina Zata Amni <rakina@chromium.org>
Date:   Tue Jul 02 06:38:31 2024

    [M126] Destruct controller before referenced WebUI in CreateWebUIIfNeeded
    
    Reset `controller` first before resetting `web_ui_`, since the
    controller still has a pointer to `web_ui_`, to avoid referencing to
    the already deleted `web_ui_` object from `controller`'s destructor.
    
    (cherry picked from commit c5dd8839bfaf4207a7db7a39c922daf67634936d)
    
    Bug: 345640549
    Change-Id: Ie9c193436b593845d8269605f68bf94bc75beed7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5624749
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
    Reviewed-by: Nasko Oskov <nasko@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1316830}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5662057
    Auto-Submit: Rakina Zata Amni <rakina@chromium.org>
    Reviewed-by: Fergal Daly <fergal@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#1679}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/renderer_host/navigation_request.cc

https://chromium-review.googlesource.com/5662057


### am...@chromium.org (2024-07-03)

re [comment #25](https://issues.chromium.org/issues/345640549#comment25)

> Thank you. I have a follow-up. I hope you hear me out and respond.

Hi, I'll always respond (as long as I can see / get notification of an update on a bug / am monitoring that bug), I just may not be able to respond immediately. :)
Such as in this case where the response would be a bit involved.

> Am I required to do the analysis on BRP protection for this UAF?

*required* no. But it is helpful in cases such as this, when you discover that BRP protection is not in effect OR when you disagree with the assertion that it is and have the demonstration to back that.

> Or was this determined earlier in another chat or VRP meeting? The ASan report indicates MiraclePtr Status: MANUAL ANALYSIS REQUIRED. If there were notes or discussions done outside of this report, I'd like to see how the BRP protections were determined.

It was determined based on off-bug discussions and in VRP evaluation. We try to comments and notes related to investigation regarding RCA and fix of a bug on the bug to keep a sole source record and provide transparency to the details of the bug for the eventual public disclosure.

In terms of a VRP analysis or off-bug discussions, unfortunately the details of which aren't going to make it in full on the bug each time. Apologies for that, but there is also scaling issue. I try to provide summaries for the reward decision, but full notes for our assessment of a bug aren't possible.

In terms of the BRP protection, we assert this is BRP protection is WAI, as the memory is quarantined.
`We UAF when when we deref webui_controller->web_ui() returning the raw_ptr<WebUI> web_ui_. While the memory is quarantined, the value dereferenced from raw_ptr itself still holds a dangling pointer to freed memory,` the dangling pointer should be supported, since the slot / WebUIController is presumably still alive.

If you can demonstrate that BRP protection is not WAI here and that this indeed is exploitable, we'd welcome that information. You did note that you are writing demonstration for this being exploitable from a webpage. Because that you had commented requesting a reassessment, I did put this onto the docket for our review earlier today and while we did review this again, we believe or assertion is correct at this time. We'll await that information and demonstration and will be happy to reassess this again at that time.

Feel free to take your time. Much if the time is away next week due to summer holidays, so we'll not be having a VRP panel session. I'm OOO starting tomorrow, so I won't be able to respond immediately until I return, but we'll review any new information you provide at a future VRP Panel session after we receive it.

### xp...@gmail.com (2024-07-10)

deleted

### pe...@google.com (2024-09-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345640549)*
