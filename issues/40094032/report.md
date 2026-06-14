# Security: http authentication spoof on chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40094032](https://issues.chromium.org/issues/40094032) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | kk...@chromium.org |
| **Created** | 2019-02-13 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 72.0.3626.100 beta  

Operating System: 12.1.2

**REPRODUCTION CASE**

(similar to <https://crbug.com/chromium/884179>)

1. Go to <https://lbstyle.github.io/ios.html>
2. Click >> observe

## Attachments

- [WhatsApp Image 2019-02-13 at 11.45.06 PM.jpeg](attachments/WhatsApp Image 2019-02-13 at 11.45.06 PM.jpeg) (image/jpeg, 73.4 KB)
- [IMG_0915.PNG](attachments/IMG_0915.PNG) (image/png, 320.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 252 B)

## Timeline

### me...@chromium.org (2019-02-13)

eugenebut, can you PTAL?

[Monorail components: Internals>Network>Auth]

### eu...@chromium.org (2019-02-13)

I think Chrome should match Safari behavior and hide web page content and address bar if authentication URL does not match last committed URL (attached screenshot). Assigning to Kurt, who owns dialogs and tentatively adding RBS.

### me...@google.com (2019-02-14)

I think you meant to set security-impact-stable :) Assigning severity to match https://crbug.com/chromium/884179.

### sh...@chromium.org (2019-02-28)

kkhorimoto: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kk...@chromium.org (2019-02-28)

[Empty comment from Monorail migration]

### kk...@chromium.org (2019-03-06)

[Empty comment from Monorail migration]

### kk...@chromium.org (2019-03-08)

[Comment Deleted]

### kk...@chromium.org (2019-03-08)

Fixing this security bug will require some refactoring; the process is being outlined in go/bling-javascript-dos-prevention

### kk...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### kk...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-04-01)

[Empty comment from Monorail migration]

### kk...@chromium.org (2019-04-01)

Just a heads up on this bug: the solution is planned to be shipped with OverlayService in M76.

### kk...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-26)

kkhorimoto@, could you please provide an update here? Security team would greatly appreciate that.

### kk...@chromium.org (2019-04-26)

The fix should be available in the M76 release.

### ch...@gmail.com (2019-05-29)

Any update on this bug? Thanks :=)

### kk...@chromium.org (2019-05-31)

Quick update on this: the feature that fixes this issue got pushed back to the M77 release, so will be available in September.

### mm...@chromium.org (2019-07-01)

As per c#17.

### kk...@chromium.org (2019-08-08)

Adding RBS since this is a security bug that can now be fixed in M77.

### kk...@chromium.org (2019-08-14)

Fix is in progress and will be ready soon, but will require merging way too much code post-branch.  Pushing this to the M78 milestone since it's not a new attack vector and we've already shipped many released with this vulnerability.

### kk...@chromium.org (2019-09-03)

crrev.com/c/1783722

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bc66f9f6d46ed812c8c37dbdd48bfba536eda301

commit bc66f9f6d46ed812c8c37dbdd48bfba536eda301
Author: Kurt Horimoto <kkhorimoto@chromium.org>
Date: Wed Sep 04 18:35:13 2019

[iOS] Replace location bar text while showing HTTP auth dialog.

When HTTP authentication dialogs are displayed, the URL in the omnibox
should be replaced with a string denoting that the page is asking the
user to sign in.  This is done because HTTP authentication is sometimes
requested for pages that differ from the URL in the location bar.

Bug: 931894
Change-Id: I031d0733872bb065da18eb707de1241b963aff4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1783722
Auto-Submit: Kurt Horimoto <kkhorimoto@chromium.org>
Reviewed-by: Stepan Khapugin <stkhapugin@chromium.org>
Commit-Queue: Stepan Khapugin <stkhapugin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#693271}

[modify] https://crrev.com/bc66f9f6d46ed812c8c37dbdd48bfba536eda301/ios/chrome/app/strings/ios_strings.grd
[modify] https://crrev.com/bc66f9f6d46ed812c8c37dbdd48bfba536eda301/ios/chrome/browser/ui/location_bar/BUILD.gn
[modify] https://crrev.com/bc66f9f6d46ed812c8c37dbdd48bfba536eda301/ios/chrome/browser/ui/location_bar/location_bar_mediator.mm
[modify] https://crrev.com/bc66f9f6d46ed812c8c37dbdd48bfba536eda301/ios/chrome/browser/ui/location_bar/location_bar_mediator_unittest.mm


### kk...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-09-04)

Here's the PoC: 

<body>
  <script>
function go() {
  var x = window.open('https://www.google.com');
  setTimeout(function(){x.location = "https://jigsaw.w3.org/HTTP/Basic/"}, 1800);
};
</script>
<input onclick="go()" value="Click here" type="button" /></body>
</body>


### ch...@gmail.com (2019-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### sr...@chromium.org (2019-09-13)

cc,ramesh for verification.

### ra...@chromium.org (2019-09-16)

Tested in 78.0.3904.15 Beta on iPhone 8plus(iOS 12.4.1)

Test URL: https://chrome-test.github.io/bugs/931894/

Steps: 
1. Enable non-modal flag from chrome://flags
2. Load above mentioned test URL
3. Tap on Click here button

Observed results: On displaying HTTP auth dialogue the URL in the omnibox is replaced with string 'Sign in to website' but the webpage content didn't hide as it is happening in Safari

@kkhorimoto, Could you please confirm whether this is an expected behaviour.

### kk...@chromium.org (2019-09-16)

Yes, this is the desired UX.  The non-modal specs did not include Safari's background shim.

### sr...@chromium.org (2019-09-16)

Marking verified based on comments#29,30

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $1,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-20)

Not requesting merge to beta (M78) because latest trunk commit (693271) appears to be prior to beta branch point (693954). If this is incorrect, please replace the Merge-na label with Merge-Request-78. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-12-12)

This issue was migrated from crbug.com/chromium/931894?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/941745]
[Monorail mergedwith: crbug.com/chromium/948209]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094032)*
