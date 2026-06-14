# Security: Speech permission request UI spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40091350](https://issues.chromium.org/issues/40091350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-05-10 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 68.0.3424.0 (Official Build) canary (64-bit)  

Operating System: macOS Sierra 10.12.6

**REPRODUCTION CASE**

1. Load the testcase
2. Click on the button and wait
3. Observe the permission request stays open after navigation to mixed.badssl.com

## Attachments

- [Screen Shot 2018-05-10 at 01.02.18.png](attachments/Screen Shot 2018-05-10 at 01.02.18.png) (image/png, 555.8 KB)
- [poc (16).html](attachments/poc (16).html) (text/plain, 643 B)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 295.8 KB)

## Timeline

### ch...@gmail.com (2018-05-10)

raymes@, based on #2 (on https://crbug.com/chromium/816033), can you please try to repro this on Linux or macOS? Thanks.

### ch...@gmail.com (2018-05-10)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-05-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-05-10)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-05-10)

Confirmed on Mac dev 68.0.3423.2. Does not happen with --enable-features=MacViews, though.

[Monorail components: UI>Browser>Permissions>Prompts]

### ra...@chromium.org (2018-05-13)

I'm no longer working on permsissions. +mkwst to triage

### mk...@chromium.org (2018-05-14)

benwells@: Did y'all consider blocking permission requests during `beforeunload`? It seems unlikely that there are legitimate cases for a document to grab permissions on its way out the door.

msramek@: FYI.

### be...@chromium.org (2018-05-14)

I don't think we considered it. I agree it seems unlikely to break anything and is probably worth doing.

### sh...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-28)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2018-05-29)

mkwst@: We can look into this soon. Do we need a blink intent, since this is a web-facing behavior? Although I agree that nobody should be using this for anything meaningful.

### du...@chromium.org (2018-06-06)

It only works about 30% of the time but I can reproduce it on Linux as well. 

It can be fixed by ignoring permission requests for frames where RenderFrameHost::IsCurrent() is false. I'm not sure if that is the most reliable way to check for unloading frames? The documentation for IsCurrent() sounds like a frame can be non-current in other cases as well.
CL: https://crrev.com/c/1088616

### sh...@chromium.org (2018-06-11)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2018-07-21)

Ant update here? Thanks!

### du...@chromium.org (2018-07-23)

This is very similar to https://crbug.com/807280, which I also looked into. After a bit more testing, I discovered that the IsCurrent() check still doesn't catch all incorrectly displayed cookies, so I'm not sure if it would fix this issue completely.

Of course we could submit the CL linked in #12. The PoC is prevented and it is unknown if there are other ways to trigger a permission when navigating away. 
It is also possible that a frame is non-current in other scenarios than navigating away, so this might introduce cases where we don't show a prompt that should have been shown.
"During process transfer, a RenderFrameHost may be created that is not current." - https://cs.chromium.org/chromium/src/content/public/browser/render_frame_host.h?type=cs&q=iscurrent+renderframehost&sq=package:chromium&g=0&l=246

### mm...@chromium.org (2018-08-07)

mkwst@, benwells@, msramek@, ping from the security sheriff. I see that you agreed on something in c#7 - c#11, and also had a draft cl in c#12. Any plans to finish that soon? Thanks!

### ms...@chromium.org (2018-08-07)

dullweber@ has a proposed in #15, but he's OOO at the moment.

benwells@, you're owner of permissions/, so if that CL LGTY, perhaps you can approve and CQ it on dullweber@'s behalf.

### be...@chromium.org (2018-08-08)

The CL is simple but the RVH lifetime is mysterious to me, and I'm not sure if there will be side effects. If a RVH expert reviewed the change i would happily give it a +1 and CQ it.

### du...@chromium.org (2018-08-20)

I would be happy to submit the CL but I have the same concerns about possible side effects. Who might know more about frame lifetimes?

### mk...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### be...@chromium.org (2018-08-28)

Oh sorry missed #19. Maybe dcheng@ or creis@?

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### hk...@chromium.org (2018-10-19)

cc-ing the recommended people who might know more about frame lifetimes.
 
dcheng@ & creis@, please let me know what you think about c12. Do you think it would introduce any bugs by blocking valid permission requests?

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-13)

Friendly ping for dcheng@ and creis@ re https://crbug.com/chromium/841622#c12 :)

### cr...@chromium.org (2019-06-14)

Sorry for missing this.  Please ping us on chat if we miss a question and you're blocked on it.

https://crbug.com/chromium/841622#c12: It sounds like you're conflating beforeunload and unload.  During beforeunload, a RFH is still current (i.e., it is the FrameTreeNode::current_frame_host() for its frame).  During unload of a cross-process navigation, it may be pending deletion and not current anymore.

In that sense, checking IsCurrent() wouldn't block all cases where permissions are requested during beforeunload (I would imagine), but that also may not matter.  It seems to match the cases where the main frame is no longer showing the RFH that asked for the permission, which seems like the more important part.  Given that the report uses beforeunload, maybe there's something async allowing the permission request to be processed after the commit of a new document?

Maybe a better fix would be to ensure a RFH can't request permissions from a document after a new one has been committed.  dcheng@, is there a way to do that with the Mojo bindings reset?

### cr...@chromium.org (2019-06-14)

CC'ing some folks with knowledge of frame trees, pending delete nodes, and navigation as well.

[Monorail components: UI>Browser>Navigation]

### ar...@chromium.org (2019-06-14)

Re https://crbug.com/chromium/841622#c12:
~~~
It only works about 30% of the time but I can reproduce it on Linux as well. 

It can be fixed by ignoring permission requests for frames where RenderFrameHost::IsCurrent() is false. I'm not sure if that is the most reliable way to check for unloading frames? The documentation for IsCurrent() sounds like a frame can be non-current in other cases as well.
CL: https://crrev.com/c/1088616
~~~

1) As creis@ said, "beforeunload" is not "unload". So when the permission request is made, the document hasn't started deletion at all. It might continue to live if the user click on "do not proceed" in the beforeunload dialog.
To me, it looks likes the problem is the UI dialog continue to be displayed to the user, even after the document is gone.
We can try to block permission request for unloading document, but it will work only partially. You can receive the permission request and then to start unloading. Is it possible to discard the permission dialog whenever the RenderFrameHost is deleted?

2) RenderFrameHost::IsCurrent() will work, but only for the navigated frame. If you have iframes and do navigation for instance from A(B) to C. Then:
A.IsCurrent() == false, because C is now the current document in the main frame. In contrast, B.IsCurrent() == true, because B is still the current document it its frame.
Ideally, RenderFrameHostImpl::is_active() should be used, but there are no public content/public API for this.

### dc...@chromium.org (2019-06-18)

> This is very similar to https://crbug.com/807280, which I also looked into. After a bit more testing, I discovered that the IsCurrent() check still doesn't catch all incorrectly displayed cookies, so I'm not sure if it would fix this issue completely.

What are the cases where IsCurrent() is insufficient? Is it the case mentioned in https://crbug.com/chromium/841622#c33?

> Maybe a better fix would be to ensure a RFH can't request permissions from a document after a new one has been committed.  dcheng@, is there a way to do that with the Mojo bindings reset?

There appear to be multiple entrypoints into https://cs.chromium.org/chromium/src/chrome/browser/permissions/permission_manager.cc?rcl=ba64a0c7189543396c66e2affb2f414a21daf551&l=382, so I'n not sure if this will get them all. Promisingly, content::PermissionServiceImpl appears to be execution context-associated, and is stored here: https://cs.chromium.org/chromium/src/content/browser/permissions/permission_service_context.h?rcl=ba64a0c7189543396c66e2affb2f414a21daf551&l=29...

However, content::PermissionServiceContext already appears to be trying to close existing bindings on navigation... https://cs.chromium.org/chromium/src/content/browser/permissions/permission_service_context.cc?rcl=ba64a0c7189543396c66e2affb2f414a21daf551&l=128. So it seems like something is missing here--maybe what needs to happen is CloseBindings() needs to also ensure that any already-shown UI is closed?

> To me, it looks likes the problem is the UI dialog continue to be displayed to the user, even after the document is gone.
We can try to block permission request for unloading document, but it will work only partially. You can receive the permission request and then to start unloading. Is it possible to discard the permission dialog whenever the RenderFrameHost is deleted?

+1, this seems like a reasonable thing to do

> 2) RenderFrameHost::IsCurrent() will work, but only for the navigated frame. If you have iframes and do navigation for instance from A(B) to C. Then:
A.IsCurrent() == false, because C is now the current document in the main frame. In contrast, B.IsCurrent() == true, because B is still the current document it its frame.
Ideally, RenderFrameHostImpl::is_active() should be used, but there are no public content/public API for this.

Also, I guess this would only work if a process swap is involved? Or is there no race / do we not care at all in case of same-process navigations?

(This assumes the current implementation where we do not swap RFH on same-process navigation)

### ar...@chromium.org (2019-06-18)

> What are the cases where IsCurrent() is insufficient? Is it the case mentioned in https://crbug.com/chromium/841622#c33?

IsCurrent() == "This document is the current one in its frame."
If no new document replace the current one, then the current one continues to be the current one.

When a document starts unloading, it may continues to be the current one for instance when:
 - Navigating from A(B) to C. Then B.IsCurrent() == true until complete removal.
 - Deleting B from A(B). Then B.IsCurrent() == true continue to be true until complete removal.

B.is_active() correctly gives you: "The document started unloading".

> Also, I guess this would only work if a process swap is involved? Or is there no race / do we not care at all in case of same-process navigations?

Yes, I am speaking about cross-process navigation. For same-process navigation, the RenderFrameHost gets a new document "internally" and IsCurrent() stays true.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### hk...@chromium.org (2019-09-05)

I don't have cycles to look into this in September at least. 

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-09-25)

engedy or andypaicu, any chance you'd be able to take a look? Thanks!

### es...@chromium.org (2019-09-25)

I can't reproduce this on Chrome 77 on Linux. Does anyone still have a working repro?

In the console I see a message about navigations being throttled due to https://bugs.chromium.org/p/chromium/issues/detail?id=882238. That throttling can be disabled with --disable-ipc-flooding-protection, and when I try the POC with that flag, the browser hangs.

Is there an obvious way to exploit this without hitting the navigation throttling? Presumably there is still an underlying bug to be fixed here, but we could consider downgrading the severity to Low if it doesn't seem to be exploitable anymore.

### es...@chromium.org (2019-09-25)

Also, if you accept the prompt, which origin gets the permission? (the one in the dialog or the one in the omnibox?) If it's the one in the dialog, I think that's probably more like Low severity anyway; up until relatively recently, we allowed iframes to show permission prompts, expecting users to read the origin in the prompt, so it seems like a stretch to call it that a Medium vulnerability now.

### ar...@chromium.org (2019-09-26)

BTW FYI, I attempted fixing this by exporting RenderFrameHost::IsActive() to content/public and start using it for this component:

https://chromium-review.googlesource.com/c/chromium/src/+/1811250

(I am still a far from being able to land this CL)

### es...@chromium.org (2019-10-04)

Hey permissions team, would somebody be able to prioritize this bug in Q4? It's been lingering for quite a while.

### en...@chromium.org (2019-10-07)

We are planning to perform an audit of all clients of the permissions infrastructure, as well as of the infrastructure itself, to identify and fix any race conditions with navigations. I think this audit will take place in Q4 2019 or Q1 2020, depending on staffing. Let me know if you think we should prioritize this particular bug higher.

### es...@chromium.org (2019-10-07)

Re #44: do you know the answer to this question in c41?
> if you accept the prompt, which origin gets the permission? (the one in the dialog or the one in the omnibox?)
My opinion about prioritization depends on the answer to that question. If the origin shown in the dialog is not the one that gets the permission granted, then I think we should prioritize this bug higher.

### an...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-04-01)

Tested today on 83.0.4101.0 (Official Build) canary (64-bit) on macOS. Fixed.

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-05-06)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-05-06)

https://crbug.com/chromium/1077474 shows that this race appears to also affect page status bubbles like the Downloaded Multiple Files bubble (and potentially things like the Popup Blocker bubble) rather than just the Permission Bubble, although they also appear to show the correct origin in the dialog.

Did we resolve the questions around prioritization? Given https://crbug.com/chromium/1077474 this is definitely still reproducible in at least some fashion.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 265 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 279 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2020-08-03)

It's difficult to really tell without being able to reproduce the issue but I suspect https://bugs.chromium.org/p/chromium/issues/detail?id=1041021 incidentally covered the underlying issue in this bug as well.

Also considering that the issue can't be reproduced by the reporter anymore (#c50), I'll close this bug as fixed.

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-03)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M85. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-03)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-08-03)

andypaicu@ can you ptal and see if a merge to M85 is needed here 

### an...@chromium.org (2020-08-04)

There is no merge needed here as the issue has not been user visible since M83 at least.

I've closed this issue because the underlying problem has also been fixed but this should not result in any user-visible behavior change.

### sr...@google.com (2020-08-04)

Removing merge-review label for M85 per https://crbug.com/chromium/841622#c64

### ad...@google.com (2020-08-05)

(Since we're unsure when this was fixed, I'll credit it in M85 release notes)

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations, the VRP panel decided to award $500 for this report.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/841622?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/1077474]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091350)*
