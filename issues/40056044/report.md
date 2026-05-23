# (Chrome & Chromium Browsers) Blank Address Bar Temporary Spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40056044](https://issues.chromium.org/issues/40056044) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2021-05-29 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Open Chrome for Android and visit http://sha3.ezyro.com/blank.html
2. Click on the href link to open fake window.
3. You will first notice the legit site inside the address bar which you will think you are visiting to, but then you will notice blank address bar with fake contents.

##Code:

<script>
function pwned() {
var t = window.open('', 'ss');
t.document.write(`<h1>Paypal has been moved to</h1><a href="https://evil.com">Evil.com</a>`);
t.stop();
}
</script>
<a href="https://legitsite.com" target="ss" onclick="setTimeout('pwned()','500')">click me2</a>

##Note:

I can also create a POC which will show a fully fake phishing page inside blank address bar. Do let me know if that's needed.

What is the expected behavior?
There should be a "about:blank" text inside the address bar or the browser should redirect to the legit domain.

What went wrong?
Browser failed to redirect to the legit domain and shows blank URL bar with fake contents inside the page.

Did this work before? N/A 

Chrome version: 91.0.4472.77  Channel: n/a
OS Version: 
Flash Version: 

This issue is like race condition, if you have caches of the legit site or if you have visited the legit site before then the browser will successfully redirect to the legit domain but incase you never visited that specific legit domain before then this temporary spoof can be reproduced. This issue can be reproduced easily inside Incognito tab every time as the browser has no caches for Incognito Mode.

## Attachments

- [Chrome](attachments/Chrome) (text/plain, 8.9 MB)
- [blank.html](attachments/blank.html) (text/plain, 270 B)
- [Screenrecorder-2021-05-29-22-35-21-713.mp4](attachments/Screenrecorder-2021-05-29-22-35-21-713.mp4) (video/mp4, 8.9 MB)
- [Phishing-POC.mp4](attachments/Phishing-POC.mp4) (video/mp4, 8.5 MB)

## Timeline

### [Deleted User] (2021-05-29)

[Empty comment from Monorail migration]

### sh...@gmail.com (2021-05-29)

I have attached a POC video here:

### ad...@google.com (2021-05-29)

Thanks for the report and the clear instructions.

Reproduced on Chrome for Android 91.0.4472.77.

I agree that the completely blank address bar seems like a bug, and it seems to me that some users could fall for a spoof site. cthomp@, would you agree?

As there's no attacker-controlled URL displayed in the Omnibox, I think this falls under the severity definition of "An address bar spoof where only certain URLs can be displayed, or with other mitigating factors" and I'm going to rate it as Medium severity.

knollr@ - are you a good person for this one? If not, please could you move it to someone more appropriate? Thanks!

[Monorail components: UI>Browser>Navigation]

### [Deleted User] (2021-05-30)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kn...@chromium.org (2021-06-01)

I think estark@ is working on Omnibox issues like this? :-)

### ad...@google.com (2021-06-02)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-06-11)

twellington, do you know who might be familiar with the Clank omnibox to investigate this?

### es...@chromium.org (2021-06-11)

(my owner/label changes didn't apply for some reason...) twellington, do you know who might be familiar with the Clank omnibox to investigate this?


[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2021-06-13)

twellington: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2021-06-15)

ender@, will you please help evaluate this P1 security bug related to the omnibox while Filip is OOO?

### [Deleted User] (2021-06-27)

ender: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fg...@chromium.org (2021-06-28)

Adding Patrick, maybe he has capacity at the moment.

### en...@google.com (2021-06-28)

sorry i missed this! looking.

### en...@google.com (2021-06-28)

I think the Omnibox is only the tip of an ice berg here. I don't think this is related to the Omnibox.

It looks like the mobile webcontent is passing through the cross-origin request that is blocked on the desktop, sending the user over to paypal.com. Android is a whole different story and the more I stare at this the more it makes me scared about what could be done with this.

Looping in security team and Blink owners, hopefully we can identify who would be the best person to investigate this on the webcontent side.. 

FWIW: LOTS (LocationBar, Omnibox, Toolbar, Status) behave correctly here, responding directly to what WebContent is saying; the webcontent says:

- Visible URL is ''
- Committed URL is ''
- Titile is ''

Tracked this down to TabWebContentsDelegateAndroidImpl [1]. I think the problem is rooted even deeper. 
Could it be that webcontent is misconfigured on Android? why does Android accept this while Desktop responds with

    Uncaught DOMException: Blocked a frame with origin "http://sha3.ezyro.com" from accessing a cross-origin frame.
        at pwned (http://sha3.ezyro.com/blank.html?i=1:4:3)
        at <anonymous>:1:1

and sends the user to paypal.com?

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabWebContentsDelegateAndroidImpl.java;l=104-108


[Monorail components: Blink]

### ad...@google.com (2021-06-28)

Had a quick chat with ender@ about this. creis@, would you be able to explain this symptom:

> It looks like the mobile webcontent is passing through the cross-origin request that is blocked on the desktop

or suggest who might be good to dig into that?

### rb...@chromium.org (2021-06-28)

Not sure what team in web platform is best to dig into this further - adding Blink>Loading and cc'ing jbroman@ as someone who may know how to best route it.

[Monorail components: -Blink Blink>Loader]

### sh...@gmail.com (2021-06-30)

Hi team,
As I mentioned in my report that this issue may not work if caches of any legit site is present inside browser or if users has visited that legit site before but now the new code will work in both private and normal mode no matter if any legit site is opened before or caches of that site is available in any Chromium browsers.

##New Code:

<script>
    window.onclick = function () {
        x = window.open('https://anything.com');
        setTimeout(function () {
            x.document.write(`<h1>POC</h1>`)
        }, 1);
    }
    </script>

I have also setup the new working phishing POC code on my site: http://sha3.ezyro.com/newb.html

### jb...@chromium.org (2021-07-06)

kinuko may be better to route within Blink here, though CSA is another possibility

### cr...@chromium.org (2021-07-08)

Sorry for the delay looking at this.  This appears to be a Chrome for Android omnibox bug, since the omnibox is responsible for displaying about:blank when there is no last committed URL or NavigationEntry.  (In these cases, WebContents::GetVisibleURL() and similar functions return an empty GURL.)  I'm not an expert on the omnibox code, but at least one place it appears to be doing that on Desktop is LocationBarModelImpl::GetURL():

GURL LocationBarModelImpl::GetURL() const {
  GURL url;
  return (ShouldDisplayURL() && delegate_->GetURL(&url))
             ? url
             : GURL(url::kAboutBlankURL);
}
https://source.chromium.org/chromium/chromium/src/+/main:components/omnibox/browser/location_bar_model_impl.cc;drc=180e57971e7cabc0a15c76112f8d37a942bc8d61;l=138

It appears we're missing something equivalent on Android, which is why we show "about:blank" on Desktop and nothing on Android.

Note that any page doing "window.open()" will repro this.  There's a simple repro here:
1) http://csreis.github.io/tests/window-open.html
2) Click "Open about:blank window"
On Desktop, this will show "about:blank," and on Android it won't.

In terms of severity, neither "about:blank" (i.e., the intended behavior) nor an empty string (i.e., this bug) provide any indication that the content you're looking at is authentic-- in both cases the user should be suspicious.  However, the "Search or type web address" shown in the omnibox may make some users think it's a message from Chrome, so maybe Medium severity is ok.

ender@: Can you talk with tommycli@ or other omnibox folks to figure out the right change on the Android side?  Thanks!

(Oh, and re: https://crbug.com/chromium/1214481#c15: The JavaScript error you were observing only happens if the destination page has a chance to commit before the document.write is attempted.  It's mostly unrelated.)

### to...@chromium.org (2021-07-08)

LocationBarModel is supposed to be cross-platform code that handles URL Formatting for all platforms, including Android.

In this case, GetURL() is called by GetURLForDisplay() and GetFormattedFullURL(), in this chain:

GetURLForDisplay() calls GetFormattedURL() calls GetURL().

So either:
 1. The Android UI doesn't respect the output of LocationBarModel, in which case it's an Android-specific bug needing an Android specific fix, or:

 2. The LocationBarModel doesn't always do the right thing, in which case this bug may actually affect multiple platforms and we noticed it first in Android, or in an Android-specific usage.

Let me do a bit more digging.

### to...@chromium.org (2021-07-08)

I (finally) managed to get an Android emulator setup with the Clankium build logging what's going on with LocationBarModelImpl.

It seems like in the success case, which is "named about:blank window" in creis's example, some Android code calls through to LocationBarModelImpl and gets the correct "about:flag" string.

In the failure case, the LocationBarModelImpl code is never called, at least as far as I can tell from logcat.

I think that means we are dealing with Case #1, which is a bug in Android's UI where it's failing to call LocationBarModelImpl to get the new string for the page.

I'll take a further look to see why that could be.

### to...@chromium.org (2021-07-08)

Alright, I'm pretty sure this behavior regressed with this patch:
https://chromium-review.googlesource.com/c/chromium/src/+/2635448

Specifically, the change in this file makes the Android LocationBarModel.java skip calling into the native code when the URL seems empty. That's what's causing the divergence in behavior from Desktop.

https://chromium-review.googlesource.com/c/chromium/src/+/2635448/17/chrome/android/java/src/org/chromium/chrome/browser/toolbar/LocationBarModel.java

I'm sending a patch to the original author (hanxi@) to revert that line:
https://chromium-review.googlesource.com/c/chromium/src/+/3016346

### gi...@appspot.gserviceaccount.com (2021-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/904100f6ec3eda5042c5bdb9da142b077b14e8e5

commit 904100f6ec3eda5042c5bdb9da142b077b14e8e5
Author: Tommy Li <tommycli@chromium.org>
Date: Fri Jul 09 18:53:23 2021

[omnibox] Fix Android about:blank security regression

The "about:blank" string is not showing up in the omnibox for some new
tabs created in Android.

This regressed here:
https://chromium-review.googlesource.com/c/chromium/src/+/2635448

It seems that with that above patch, Android stopped calling into the
native code that governed displaying about:blank, early exiting
instead.

This CL fixes that, although it may show about:blank again in some
cases that Android UI owners would not like.

Bug: 1214481
Change-Id: I68537657df2e0af328d6a3dc3d903525ff2f6aa2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3016346
Reviewed-by: Xi Han <hanxi@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Auto-Submit: Tommy Li <tommycli@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#900091}

[modify] https://crrev.com/904100f6ec3eda5042c5bdb9da142b077b14e8e5/chrome/android/javatests/src/org/chromium/chrome/browser/toolbar/LocationBarModelTest.java
[modify] https://crrev.com/904100f6ec3eda5042c5bdb9da142b077b14e8e5/chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/LocationBarModel.java


### to...@chromium.org (2021-07-09)

Requesting a merge to M92.

Too late to merge to M91.

### [Deleted User] (2021-07-09)

This bug requires manual review: We are only 10 days from stable.
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-07-09)

+Security TPMs for M92 merge review (Note: We're cutting M92 Stable RC on Tuesday, July 13th)

### to...@chromium.org (2021-07-09)

I've only verified this on the local build on my machine.

Would be good to get the original tester to test this once it hits Canary.

That being said... if that's not possible... may still be good to merge this.

### ad...@google.com (2021-07-09)

We're cutting M92 on Tuesday. I'm not going to approve this for initial M92 release, but we may choose to merge into one of the M92 security refreshes once it's had a little bake time.

(Regression CL mentioned in https://crbug.com/chromium/1214481#c24 looks like it landed in M90, for the record).

### [Deleted User] (2021-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-10)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations - the VRP Panel has decided to award you $1,000 for this report. Thank you for reporting this issue to us!

### sh...@gmail.com (2021-07-22)

Thank you so much team for the bounty decision.!

### am...@google.com (2021-07-23)

Approved for merge to M92, please merge to branch 4515 at your earliest convenience. 
Also approving for merge to M91, as this is now the Extended Stable release branch; please merge to branch 4472 as well. Thank you! 

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### go...@google.com (2021-07-28)

Please merge your change to M92 branch 4515 ASAP so we can take it in for next M92 respin. Thank you.

### to...@chromium.org (2021-07-28)

Two CLs are here:
M91: https://chromium-review.googlesource.com/c/chromium/src/+/3059101
M92: https://chromium-review.googlesource.com/c/chromium/src/+/3058956

Govind, if you are on a tight timeline, you could do owners override on those so I could send it in.

### to...@chromium.org (2021-07-28)

In the olden (better) days, we merge TBR all merges. :/

### go...@google.com (2021-07-28)

Done for M92: https://chromium-review.googlesource.com/c/chromium/src/+/3058956

M91 merge is NOT needed as M92 is already in stable. 

### am...@google.com (2021-07-28)

right, apologies, Android isn't impacted by extended stable! Apologies for the confusion and extra labels. 

### gi...@appspot.gserviceaccount.com (2021-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/70a71e781d8d72aaee8c07d196457eb3efc8015f

commit 70a71e781d8d72aaee8c07d196457eb3efc8015f
Author: Tommy Li <tommycli@chromium.org>
Date: Wed Jul 28 19:52:01 2021

[Merge 92] [omnibox] Fix Android about:blank security regression

The "about:blank" string is not showing up in the omnibox for some new
tabs created in Android.

This regressed here:
https://chromium-review.googlesource.com/c/chromium/src/+/2635448

It seems that with that above patch, Android stopped calling into the
native code that governed displaying about:blank, early exiting
instead.

This CL fixes that, although it may show about:blank again in some
cases that Android UI owners would not like.

(cherry picked from commit 904100f6ec3eda5042c5bdb9da142b077b14e8e5)

Bug: 1214481
Change-Id: I68537657df2e0af328d6a3dc3d903525ff2f6aa2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3016346
Reviewed-by: Xi Han <hanxi@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Auto-Submit: Tommy Li <tommycli@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#900091}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3058956
Commit-Queue: Krishna Govind <govind@chromium.org>
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1879}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/70a71e781d8d72aaee8c07d196457eb3efc8015f/chrome/android/java/src/org/chromium/chrome/browser/toolbar/LocationBarModel.java
[modify] https://crrev.com/70a71e781d8d72aaee8c07d196457eb3efc8015f/chrome/android/javatests/src/org/chromium/chrome/browser/toolbar/LocationBarModelTest.java


### am...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-27)

Labeled as not applicable for M90-LTS because it affects only android.

### [Deleted User] (2021-10-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tw...@chromium.org (2022-09-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1214481?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail mergedwith: crbug.com/chromium/1218311, crbug.com/chromium/1231738]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056044)*
