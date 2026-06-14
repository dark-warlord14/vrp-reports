# blob:chrome-extension:-URLs should not bypass CSP in extension pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40088758](https://issues.chromium.org/issues/40088758) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2017-08-18 |
| **Bounty** | $1,000.00 |

## Description

The default Content Security Policy in Chrome extensions is designed to block remote scripts.
Extensions can opt in to allowing remote scripts, but only with a custom content_security_policy (https://developer.chrome.com/extensions/contentSecurityPolicy#relaxing). This makes it easier to audit the extension, even in an automated fashion.

I have found a couple of extensions in the Chrome Web Store (together about 35k users, I've reported them already) that are clones of other extensions and hide a snippet in their privileged background page that facilitates remote code execution, as follows (simplified, the actual logic is more obfuscated):

1. Send HTTP request to an external server.
2. Get the response as a Blob, and turn it into a blob:chrome-extension:-URL.
3. Create a script tag, assign the previous URL to this tag and insert it in the document to run any JS code with access to the full extension API (impersonations of ad blockers usually have permissions to intercept requests, so this is bad).



Steps to reproduce:
1. Download the attached files, save them to a directory.
2. Visit chrome://extensions, enable Developer mode and load the directory from the previous step as an unpacked extension.
3. Inspect the background page, e.g. by clicking on "Inspect views: background page".

Expected:
- Four CSP errors, indicating that attempts to execute non-static code (inline code or remote scripts) have been blocked.

Actual:
- An alert dialog pops up, indicating that non-static code was able to execute in the context of a privileged extension page.
- Three CSP errors, because the first test, loading a blob:chrome-extension:-URL failed.



The fix is is to make sure that blob:-URLs (and filesystem:-URLs) are not bypassing the content security policy by default.



I'd like to keep this bug private until it is fixed, to avoid more abuse of this mechanism.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 155 B)
- [background.js](attachments/background.js) (text/plain, 590 B)

## Timeline

### el...@chromium.org (2017-08-18)

Interesting!

I expected the same bypass via DATA but it turns out that it too is blocked by the default CSP: "Refused to load the script 'data:application/javascript,alert('data');' because it violates the following Content Security Policy directive: "script-src 'self' blob: filesystem: chrome-extension-resource:"."

I wonder if there are any legitimate use-cases that would be broken if we removed 'blob:' from the default CSP.

### ro...@robwu.nl (2017-08-18)

> I wonder if there are any legitimate use-cases that would be broken if we removed 'blob:' from the default CSP.

It is safe to remove "blob:" from the default CSP, because extensions can still relax the CSP by explictly adding "blob:" to the content_security_policy field in their manifest.json - https://developer.chrome.com/extensions/contentSecurityPolicy#relaxing

The reason that data: is blocked and blob:chrome-extension is not is because resources from extension origins are bypassing the CSP by default - https://w3c.github.io/webappsec-csp/#extensions

### rs...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-09-01)

Andy, do you think you could take a look at this CSP bug? Thanks!

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### an...@chromium.org (2017-09-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d65cb75de17203388bfd3b12c1bf7e9a5b503211

commit d65cb75de17203388bfd3b12c1bf7e9a5b503211
Author: Andy Paicu <andypaicu@chromium.org>
Date: Fri Oct 06 13:54:35 2017

UseCounters for seeing usage of blob: and filesystem: inside extensions

Bug: 756962
Change-Id: I32b887d5ca7bb46ef1b23f40ae55820bb36f9a4f
Reviewed-on: https://chromium-review.googlesource.com/704584
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#507049}
[modify] https://crrev.com/d65cb75de17203388bfd3b12c1bf7e9a5b503211/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp
[modify] https://crrev.com/d65cb75de17203388bfd3b12c1bf7e9a5b503211/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.h
[modify] https://crrev.com/d65cb75de17203388bfd3b12c1bf7e9a5b503211/third_party/WebKit/public/platform/web_feature.mojom
[modify] https://crrev.com/d65cb75de17203388bfd3b12c1bf7e9a5b503211/tools/metrics/histograms/enums.xml


### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### an...@chromium.org (2019-04-30)

I do not work on CSP anymore so leaving this for someone else to pick up

### ro...@robwu.nl (2019-07-23)

https://crbug.com/chromium/985759 was reported by Raymond. Although I cannot see that bug, based on his description it sounds like the same bug as this one.

### rh...@raymondhill.net (2019-07-23)

I confirm https://crbug.com/chromium/985759 is essentially a duplicate of the issue here.

### rd...@chromium.org (2019-07-25)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-07-25)

+Karan as well, who's been doing CSP work (related to our tightening for MV3).  If we can tighten the CSP for MV2 extensions, that'd be great.  It looks like andypaicu@ added some usage counters awhile back; it'd be good to revisit that data and see what the numbers are like.

If we aren't going to make the default CSP stricter, we should update the docs [1] to reflect the real default CSP [2].

[1] https://developer.chrome.com/extensions/contentSecurityPolicy
[2]  https://cs.chromium.org/chromium/src/extensions/common/manifest_handlers/csp_info.cc?l=31-33&rcl=ab652abf21b1e63786ff3beaefb6bf3fcebf8b07

### ka...@chromium.org (2019-07-25)

From the Blink.UseCounter.Features histogram, the count of InnerSchemeBypassesCSP was 56379 corresponding to a PageVisit count of 229,242,531,487 over the last 28 days (which seems low). 

Andy or Mike: It seems blob and filesystem were allow-listed in https://codereview.chromium.org/1184353002 since 'self' always matched these schemes earlier. Has the CSP implementation been corrected since?

Regarding tightening the default CSP for mv2 extensions, I think it should be ok:
- The usage of blob and filesystem urls with chrome-extension inner scheme seems to be low. (I am not that familiar with use counters, so if anyone has an opinion here, feel free to chime in).
- We don't document that blob and filesystem schemes are allowed. Only those extensions relying on this undocumented behavior will break. And they'll still have a way to get around this change by explicitly allowing blob and filesystem in their manifests.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-01-07)

mkwst, , ping for the question in https://crbug.com/chromium/756962#c16.

### ka...@chromium.org (2020-01-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ka...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### ah...@chromium.org (2021-10-19)

[Security Bug Triage Rotation] Assigning to rdevlin@ for redispatch.


### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### ro...@robwu.nl (2023-03-25)

Is there any intent to finish the work here, or can this be closed since this issue has been addressed in MV3?

The relevant CSPs are at https://source.chromium.org/chromium/chromium/src/+/main:extensions/common/manifest_handlers/csp_info.cc;l=33-46;drc=a867c0c2e3ca728d91afcfa4221f7efaf06157dc

- In MV3, blob: (and filesystem:) are no longer allowed by the CSP (kDefaultMV3CSP and kMinimumMV3CSP).
- In MV2, blob: (and filesystem:) are still allowed (kDefaultContentSecurityPolicy).


At this point, the following options are left for MV2 extensions. From low to high impact on extension deves:

1. Do nothing, i.e. allow MV2 extensions to continue to use blob:-URLs. Since the Chrome Web Store does not accept new MV2 submissions (https://developer.chrome.com/docs/extensions/mv3/mv2-sunset/), the potential for new abuse is limited.

2. Remove blob: (and filesystem:) from kDefaultContentSecurityPolicy, but allow extensions to opt in to it. The only advantage of this is that the use of blob:/filesystem:-scripts becomes more visible, at the cost of breaking existing extensions, though with the ability to easily rectify the functionality in an update.

3. Remove blob: (and filesystem:) from kDefaultContentSecurityPolicy with no exceptions. This has the most impact on extension devs, since may have to refactor the extension if their logic really depended on dynamic scripts via blob:/filesystem:-URLs.

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

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

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/756962?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/985759]
[Monorail components added to Component Tags custom field.]

### rd...@chromium.org (2024-02-22)

Closing this out.  As Rob mentioned in #53, this is addressed in MV3, and we're unlikely to change anything for MV2.

### rd...@chromium.org (2024-02-23)

Note to panel: This isn't within Chrome's threat model and no real changes were made (it was already being addressed in MV3)

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-07)

Thank you for the report, Rob. Since at the time this was reported (waaaaaay back in 2017), we did consider this be a security issue -- albeit a low severity one that deserved consideration -- and while this was ultimately resolved by the manifest V3, we did want to show our appreciation for your original report and effort here. Thanks again for your past efforts and reporting this issue to us, please accept this $1,000 reward from us -- the Chrome VRP Panel -- as appreciation.

### pe...@google.com (2024-05-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088758)*
