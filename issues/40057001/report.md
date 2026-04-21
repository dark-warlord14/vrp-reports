# Security: UAF in AvailableOfflineContentProvider

| Field | Value |
|-------|-------|
| **Issue ID** | [40057001](https://issues.chromium.org/issues/40057001) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Offline |
| **Platforms** | Android |
| **Reporter** | hu...@gmail.com |
| **Assignee** | cu...@chromium.org |
| **Created** | 2021-08-24 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

AvailableOfflineContentProvider holds a raw pointer to `Profile\* profile_;`

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/android/available_offline_content_provider.cc;drc=2771b0fedf0c9f42d16523c155d916292a38f68b;l=218>

```
AvailableOfflineContentProvider::AvailableOfflineContentProvider(  
    Profile\* profile)  
    : profile_(profile) {}  

```

This `profile_` pointer comes from |Profile::FromBrowserContext|

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile.cc;drc=54bae635414d532eb776749cdacfb59ba0e40d8b;l=220>

```
// static  
Profile\* Profile::FromBrowserContext(content::BrowserContext\* browser_context) {  
  if (!browser_context)  
    return nullptr;  
  
  // For code running in a chrome/ environment, it is safe to cast to Profile\*  
  // because Profile is the only implementation of BrowserContext used. In  
  // testing, however, there are several BrowserContext subclasses that are not  
  // Profile subclasses, and we can catch them. http://crbug.com/725276  
#if DCHECK_IS_ON()  
  base::AutoLock lock(g_profile_instances_lock.Get());  
  if (!g_profile_instances.Get().count(browser_context)) {  
    DCHECK(false)  
        << "Non-Profile BrowserContext passed to Profile::FromBrowserContext! "  
           "If you have a test linked in chrome/ you need a chrome/ based test "  
           "class such as TestingProfile in chrome/test/base/testing_profile.h "  
           "or you need to subclass your test class from Profile, not from "  
           "BrowserContext.";  
  }  
#endif  // DCHECK_IS_ON()  
  return static_cast<Profile\*>(browser_context);  
}  

```

It actually is a BrowserContext object.

`AvailableOfflineContentProvider` is created in function |AvailableOfflineContentProvider::Create|

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/android/available_offline_content_provider.cc;drc=54bae635414d532eb776749cdacfb59ba0e40d8b;l=261>

```
// static  
void AvailableOfflineContentProvider::Create(  
    Profile\* profile,  
    mojo::PendingReceiver<chrome::mojom::AvailableOfflineContentProvider>  
        receiver) {  
  // Self owned receiveres remain as long as the pipe is error free. The  
  // renderer is on the other side of the pipe, and the profile outlives the  
  // RenderProcessHost, so the profile will outlive the Mojo pipe.  
  mojo::MakeSelfOwnedReceiver(  
      std::make_unique<AvailableOfflineContentProvider>(profile),  
      std::move(receiver));  
}  

```

A comment "the profile will outlive the Mojo pipe" is not true. If we use Incognito mode, the profile will be a OffTheRecordProfileImpl and this profile will not outlive the Mojo pipe (like in issue <https://bugs.chromium.org/p/chromium/issues/detail?id=1197904>).

This makes AvailableOfflineContentProvider can continue receiving Mojo calls after Profile is freed, resulting in a use after free on a virtual function pointer of this interface like in function |AvailableOfflineContentProvider::ListVisibilityChanged|

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/android/available_offline_content_provider.cc;drc=2771b0fedf0c9f42d16523c155d916292a38f68b;l=255>

```
void AvailableOfflineContentProvider::ListVisibilityChanged(bool is_visible) {  
  profile_->GetPrefs()->SetBoolean(feed::prefs::kArticlesListVisible,  
                                   is_visible);  
}  

```

This interface can be created only on Android so this bug is only affected on Android.

## Timeline

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-25)

This all sounds plausible, are you able to create any kind of PoC for this issue?

### dr...@chromium.org (2021-08-31)

Friendly ping on the PoC. Also CC some offline_pages owners to evaluate this. petewil@, robertogden@ - does this report look plausible?

[Monorail components: UI>Browser>Offline]

### pe...@google.com (2021-08-31)

bengr's team owns offfline pages now, passing over to him.

### ro...@chromium.org (2021-08-31)

looking into this a bit

this larger feature is currently inactive, but the code path in question is not guarded by a feature flag so that's not really helpful.

Otherwise, this reminds me a lot of https://bugs.chromium.org/p/chromium/issues/detail?id=1197904 so I'm going to bump the priority and put this on the radar for the current feature owner

### bu...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-08-31)

Max - I'm happy to help

### ct...@chromium.org (2021-09-01)

Thanks for looking into this Robert. It sounds like this is plausibly reachable by an attacker (although we don't have actual triggering steps), but requires an Incognito window and to actual exploit likely needs a compromised renderer, so marking this Severity-High. Looking at blame data for the linked code this is likely Impact-Stable. 

### ro...@chromium.org (2021-09-02)

High severity is what I was thinking too.

Max has a fix out, and we'll make sure it gets merged back to all current releases + LTS
https://chromium-review.googlesource.com/c/chromium/src/+/3134520

### ct...@chromium.org (2021-09-02)

Forgot the new labeling process for sheriffs -- swapping Impact for FoundIn-90 (as a conservative estimate and so it triggers all necessary merges) so Sheriffbot can correctly track this for us :-)

### ct...@chromium.org (2021-09-02)

(Correct label this time...)

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b3c8c1619e1f6d0323bd613128bfe7e003c3044

commit 3b3c8c1619e1f6d0323bd613128bfe7e003c3044
Author: Max Curran <curranmax@chromium.org>
Date: Thu Sep 02 21:26:00 2021

Fix UAF in AvailableOfflineContentProvider.

AvailableOfflineContentProvider previously held a raw pointer to a
Profile with the assumption that the profile will outlive the Mojo pipe.
This assumption does not hold in Incognito mode, and can result in use
after free. This CL changes the raw pointer to a Profile to the ID of
the associated RenderProcessHost instead.

Bug: 1243117
Change-Id: I0933c296d9010376857104785f355b1ef7b2c0d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3134520
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Commit-Queue: Max Curran <curranmax@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917832}

[modify] https://crrev.com/3b3c8c1619e1f6d0323bd613128bfe7e003c3044/chrome/browser/chrome_content_browser_client_receiver_bindings.cc
[modify] https://crrev.com/3b3c8c1619e1f6d0323bd613128bfe7e003c3044/chrome/browser/download/android/available_offline_content_provider.cc
[modify] https://crrev.com/3b3c8c1619e1f6d0323bd613128bfe7e003c3044/chrome/browser/download/android/available_offline_content_provider.h
[modify] https://crrev.com/3b3c8c1619e1f6d0323bd613128bfe7e003c3044/chrome/browser/download/android/available_offline_content_provider_unittest.cc


### cu...@chromium.org (2021-09-02)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-09-03)

adding merge request tags for 93 and 94, which according to https://chromiumdash.appspot.com/schedule are the only previous versions that still have upcoming stables refreshes

### [Deleted User] (2021-09-03)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2021-09-03)

1. Does your merge fit within the Merge Decision Guidelines?
Yes

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3134520

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes

5. Why are these changes required in this milestone after branch?
Security bug - UAF

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
No

### go...@chromium.org (2021-09-03)

+amyressler@ for M94 and M93 merge reviews. Thank you. 

+benmason as FYI

### am...@chromium.org (2021-09-03)

since this fix just landed yesterday, I'd prefer it to get a bit more bake time on canary before approving for merge to beta or stable

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-09-07)

friendly bump :) the change has been stable over the long weekend

### am...@chromium.org (2021-09-07)

thanks for the bump and info :) 
merge approved for m94, please go ahead and merge to branch 4606. 

### go...@chromium.org (2021-09-07)

Please merge your change to M94 branch 4606 ASAP so we can take it in for tomorrow's beta release. Beta RC cut @ 2:00 PM PT today, 09/07. Thank you.

### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/31d14e25dc829f25a039a1c963ef0ad43157fff4

commit 31d14e25dc829f25a039a1c963ef0ad43157fff4
Author: Max Curran <curranmax@chromium.org>
Date: Tue Sep 07 21:25:59 2021

Fix UAF in AvailableOfflineContentProvider.

AvailableOfflineContentProvider previously held a raw pointer to a
Profile with the assumption that the profile will outlive the Mojo pipe.
This assumption does not hold in Incognito mode, and can result in use
after free. This CL changes the raw pointer to a Profile to the ID of
the associated RenderProcessHost instead.

(cherry picked from commit 3b3c8c1619e1f6d0323bd613128bfe7e003c3044)

Bug: 1243117
Change-Id: I0933c296d9010376857104785f355b1ef7b2c0d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3134520
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Commit-Queue: Max Curran <curranmax@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917832}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3144241
Auto-Submit: Max Curran <curranmax@chromium.org>
Reviewed-by: Robert Ogden <robertogden@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#841}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/31d14e25dc829f25a039a1c963ef0ad43157fff4/chrome/browser/chrome_content_browser_client_receiver_bindings.cc
[modify] https://crrev.com/31d14e25dc829f25a039a1c963ef0ad43157fff4/chrome/browser/download/android/available_offline_content_provider.cc
[modify] https://crrev.com/31d14e25dc829f25a039a1c963ef0ad43157fff4/chrome/browser/download/android/available_offline_content_provider.h
[modify] https://crrev.com/31d14e25dc829f25a039a1c963ef0ad43157fff4/chrome/browser/download/android/available_offline_content_provider_unittest.cc


### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for this report! 

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-22)

Marked as not applicable for M90-LTS because it affects only android.

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1243117?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057001)*
