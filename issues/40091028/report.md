# rel=NoOpener circumvents samesite=strict cookie restrictions

| Field | Value |
|-------|-------|
| **Issue ID** | [40091028](https://issues.chromium.org/issues/40091028) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2018-04-06 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
1. Go to https://shhnjk.azurewebsites.net/SameSite.php (Sets SameSite cookie)
2. Go to https://attack.shhnjk.com/SuperCSRF.html
3. Click Bypass link

What is the expected behavior?
SameSite cookie not sent

What went wrong?
rel=noopener removes association with opener from new window. Therefore bypasses SameSite cookie restriction. Am I missing something?

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: OS X 10.13.4
Flash Version:

## Timeline

### ji...@chromium.org (2018-04-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>Cookies]

### ji...@chromium.org (2018-04-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### el...@chromium.org (2018-04-09)

Ouch, nice find! Still present in 67.0.3390.0.

### ji...@chromium.org (2018-04-09)

[Empty comment from Monorail migration]

### ji...@chromium.org (2018-04-09)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-04-09)

I think this is either Low or Medium, depending on how important we think this defense is. Of the existing bypasses on file, this one is probably the most plausible I've seen.

### sh...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-21)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2018-04-23)

I think this regressed when shipping PlzNavigate, though since I didn't write any tests for this particular interaction, folks couldn't possibly have know that. :)

arthursonzogni@/alexmos@: I'm unfortunately getting lost tracing through the current implementation. It looks like `noopener` navigations end up routed through `NavigationRequest::CreateBrowserInitiated`, and therefore losing the initiator information that should have come over from the renderer. It's not at all clear to me how we'd best pass that information along. Do y'all have any thoughts about the right way to get the initiator origin from A to Z?

### ar...@chromium.org (2018-04-23)

For most navigations, the initiator origin is transmitted by BeginNavigationParams::initiator_origin
It is set in RenderFrameImpl::BeginNavigation()

Opening a new Window is using RenderFrameImpl::OpenURL(). There is currently no way to specify the initiator origin in FrameHostMsg_OpenURL_Params. I guess we can add one. +CC clamy@ and nasko@.
It will effectively use NavigationRequest::CreateBrowserInitiated(). In this case, we are expecting the initiator_origin to be base::nullopt.

OpenURL() was already used before PlzNavigate, so maybe it hasn't worked for much longer than that. I haven't checked.


### el...@chromium.org (2018-04-23)

When looking at fixes, we might also want to ensure that our solution also resolves https://crbug.com/chromium/761038.

### ar...@chromium.org (2018-04-24)

I am OOO until 2018-05-02.
I don't see any non-{OOO, busy} persons to assign this issue. If solving it is urgent, feel free to take it.

mkwst: One question. Do you think the opener.GetLastCommittedOrigin() can be used has the |initiator_origin| in this case? I remember there is edge case with frame that has not already committed a document.

In WebContentsImpl::createNewWindow(), there is this code:
-----
  if (params.opener_suppressed) {
    // When the opener is suppressed, the original renderer cannot access the
    // new window.  As a result, we need to show and navigate the window here.

[...] 

      OpenURLParams open_params(params.target_url, params.referrer,
                                WindowOpenDisposition::CURRENT_TAB,
                                ui::PAGE_TRANSITION_LINK,
                                true /* is_renderer_initiated */);
      open_params.user_gesture = params.user_gesture;
[...]

        new_contents->OpenURL(open_params);
---

I guess we could add OpenURParams::initiator_origin and define open_params.initiator_origin = opener->GetLastCommittedOrigin().

### sh...@chromium.org (2018-05-07)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2018-06-05)

I agree with #12. And see also https://crbug.com/chromium/831761.

This issue is getting old; friendly ping. :)

### oc...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2018-07-23)

+andy, do you mind looking at this while mkwst is OOO?

### mk...@chromium.org (2018-07-23)

https://chromium-review.googlesource.com/c/chromium/src/+/1146644

### mm...@chromium.org (2018-08-07)

I assume Mike will be finishing the fix (mentioned in c#18) soon, but friendly ping from the security sheriff never hurts :)

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-12-11)

Misha, could you please help to find an owner here as per c#21? Thanks a lot!

### mo...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-12-18)

My bug id is older. Why is my bug duplicated?

### mo...@chromium.org (2018-12-18)

That one had a more relevant owner (and more recent discussion for fixing it)

### s....@gmail.com (2018-12-18)

So what happens in bounty process? The bug needs to be marked as fixed to process a bounty.

### mo...@chromium.org (2018-12-18)

Uff. Good point. Let me re-open this and just add notes.

### sh...@chromium.org (2018-12-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-12-21)

Maks, could you assess what needs to be done?

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### s....@gmail.com (2019-03-15)

Could anyone check if https://crbug.com/chromium/876365 is fixed? If so, this bug should be fixed too.

### na...@chromium.org (2019-03-15)

https://crbug.com/chromium/876365 is not fixed yet.

### s....@gmail.com (2019-03-15)

That's weird. I can't repro this bug anymore. Probably fix on https://crbug.com/chromium/830091#c18 is already landed?

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### s....@gmail.com (2019-04-25)

Hi I think this issue is fixed. Could anyone confirm and mark this bug as fixed?

### ad...@google.com (2019-05-01)

Hi s.h.h.n.j.k@gmail.com, just to keep you updated. The fix in https://crbug.com/chromium/830091#c18 didn't land yet. https://crbug.com/chromium/882053 landed some groundwork for the fix in https://crbug.com/chromium/876365, but we haven't *knowingly* fixed this yet.

### na...@chromium.org (2019-05-01)

Yes, I've accidentally fixed it when implementing precursor origin support in Chrome (https://crbug.com/chromium/882053). The CL responsible for fixing this is r617708, which added initiator origin information for all renderer-initiated navigations. I suspect that plumbing this information through the window.open() path is what allowed the SameSite cookie filtering mechanism to have the right data and make the correct decision. I'll resolve it as fixed.

### sh...@chromium.org (2019-05-02)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-02)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-02)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-07)

Requesting merge to M75 even though there is no obvious Chromium repository trunk commit here. Perhaps it was fixed in another ticket; please investigate.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-07)

This bug requires manual review: M75 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-05-07)

morlovich@ can you ptal and confirm if a merge is needed and if so what CL to M75.

### na...@chromium.org (2019-05-07)

The fix (r617708) has been in the codebase since 73.0.3645.0, so no need to merge anything into M75.

### sr...@google.com (2019-05-07)

removing the merge-review label for M75 per https://crbug.com/chromium/830091#c48

### na...@google.com (2019-05-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-15)

Congrats the Panel decided to reward $2,000 for this report

### na...@google.com (2019-05-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2019-09-13)

CC'ing fbraun@ from https://crbug.com/chromium/876365.

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/830091?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies]
[Monorail mergedwith: crbug.com/chromium/856140, crbug.com/chromium/857194, crbug.com/chromium/876365]
[Monorail mergedinto: crbug.com/chromium/876365]
[Monorail components added to Component Tags custom field.]

### mm...@chromium.org (2025-07-17)

[clamy]:  Not sure what buganizer is up to, but buganizer flipped which issue was marked as a dupe, and the other issue was assigned to you.  mef hasn't worked on Chrome in 5 years, so won't be tackling any Chrome bugs anytime soon.

### es...@chromium.org (2026-01-28)

I'm not sure why this got reopened, based on the comment history it sounds like this has been fixed a while ago. Please reopen if that's not the case.

### ch...@google.com (2026-05-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091028)*
