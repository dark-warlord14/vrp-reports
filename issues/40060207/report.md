# sourceMappingURL directive allows use of UNC paths on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40060207](https://issues.chromium.org/issues/40060207) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Windows |
| **Reporter** | zi...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-07-07 |
| **Bounty** | $7,500.00 |

## Description

---

### Report description


sourceMappingURL directive allows use of UNC paths on Windows


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

### Description
Chrome support JavaScript source map files through the `//# sourceMappingURL` directive inside a `.js` file. Three protocols (HTTP, HTTPS, and file) are supported inside this directive to fetch a remote or local `.map` file. Suppose the `file://` protocol is used. In that case, an attacker can inject a UNC path under Windows operating system to trigger an SMB connection against the specified address, a malicious SMB server can be set up to steal NTLM hashes as also described in [this](https://bugs.chromium.org/p/chromium/issues/detail?id=1301920) other recent bugs in Chrome.

### PoC
1. Create an HTTP server
2. Create a SMB server with Responder.py (i.e. `sudo ./Responder.py -w -I <network_interface_name>`)
3. Host the two files attached to this report and called `index.html` and `index.js` after replacing `<smb_responder_ip>` with the IP address of the SMB server responder created at point 2 in `index.js`
4. Visit the hosted index.html and open the dev tools
5. Notice in Responder that a new SMB request has been received with the NetNTLMv2 hashes of the victim


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

To be exploited, the vulnerability requires the victim to visit any page controlled by the attacker. The victim must then open the dev tools within the page maintained by the attacker. An attacker could use social engineering techniques or target developers to be more likely to convince the victim to open the dev tools. The most likely victims of this attack are enterprise users, so the attacker can obtain NetNTLMv2 hashes and crack the password or use them directly with other techniques (well documented in the RedTeam world) to gain access to active directory-based networks.

I suggest looking at a similar issue already discussed and fixed, https://bugs.chromium.org/p/chromium/issues/detail?id=1301920#c5


---

### The cause


#### What version of Chrome have you found the security issue in?

Version 103.0.5060.114 (Official Build) (64-bit)


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Information Leak


#### How would you like to be publicly acknowledged for your report?

Andrea Cappa (zi0Black) @ Shielder




## Attachments

- [index.html](attachments/index.html) (text/plain, 198 B)
- [index.js](attachments/index.js) (text/plain, 93 B)

## Timeline

### zi...@gmail.com (2022-07-07)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2022-07-07)

[Empty comment from Monorail migration]

### aj...@google.com (2022-07-08)

Hi - can you attach Responder.py?

### zi...@gmail.com (2022-07-08)

Hi Ajho,
I forgot to include the link to the GitHub repository for the Responder.py: https://github.com/SpiderLabs/Responder

### jd...@chromium.org (2022-07-08)

Thanks for the report. I can't easily reproduce this, but it seems plausible.

In some senses, this is very similar to the Sev-High https://crbug.com/chromium/1301920, but is meaningfully mitigated by the need to get users to open devtools.

I'll find an owner in just a second.

[Monorail components: Blink>JavaScript]

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### jd...@chromium.org (2022-07-08)

Mathias, I'm not sure if this counts as a devtools issue or a JS/V8 issue, but would you mind taking a look at this? Something similar to the fix in 1301920 would likely apply here.

Feel free to re-assign as needed. Thanks!

[Monorail components: Platform>DevTools>JavaScript]

### ya...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2022-07-11)

Just a quick note:

The fix from crbug.com/1301920 seems irrelevant for DevTools. In DevTools, using UNCs for source maps is a valid use case (whereas for Web Share, this was just a bug).

Ideally, we would ask permissions for file system source maps, but that will have to be done very carefully because this could result in large numbers of permission requests, so we would just teach developers to click them away (and annoy them).

### zi...@gmail.com (2022-07-11)

@jarin I agree with you regarding requesting permission before accessing files on the filesystem. If it is made clear that access to a network share may lead to a leak of NTLM hashes may be the proper mitigation. Then assuming the message is only shown for the "file://" protocol during network share access, and the message is shown only once for IP in an entire browser session, in that case, it should be the right balance between security and usability.

Just my 2 cents.

### aj...@google.com (2022-07-11)

Setting Low severity as this is significantly mitigated by needing devtools.

### zi...@gmail.com (2022-07-11)

I disagree with the low impact assigned to vulnerability.  The need to open dev tools is for sure a partial mitigation (which is why I agreed with the previous medium impact classification), but at the same time, I believe that an attacker could use phishing techniques or target the IT field workers increasing the likelihood of the victim opening the development tools.

Of course, those are just my 2 cents, again.

### [Deleted User] (2022-07-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### ph...@gmail.com (2022-07-22)

Since developers use the Developer Tools daily, if not hourly and developers tend to have a higher privilege than normal users, I would say that exploits that involve the Developer Tools are high severity security issues. I am personally a little wary of opening the Developer Tools on untrusted websites, now that I know this issue exists.

### ph...@gmail.com (2022-07-22)

> I would say that exploits that involve the Developer Tools are high severity security issues
Especially if they do not involve any action other then opening the Developer Tools, which I believe is the case with source maps.

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/fe515ee1af6aabf990ac11a489c2dd166a22736e

commit fe515ee1af6aabf990ac11a489c2dd166a22736e
Author: Simon Zünd <szuend@chromium.org>
Date: Mon Jul 25 09:33:43 2022

[debugger] Type sourceMapURL as string

The sourceMapURL reported by the "script parsed" event is not
necessarily a valid Url as V8 just forwards whatever users put in the
sourceMappingUrl comment.

This CL changes the type back into a string. The actual conversion
into a Url happens in `SourceMapManager#resolveRelativeURLs` that
also does validation using `ParsedUrl`.

R=kimanh@chromium.org

Bug: 1342722
Change-Id: I4aad2865a000da2a3c89bc1b730d68a662bd8498
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3784586
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Kim-Anh Tran <kimanh@chromium.org>

[modify] https://crrev.com/fe515ee1af6aabf990ac11a489c2dd166a22736e/front_end/core/sdk/Script.ts
[modify] https://crrev.com/fe515ee1af6aabf990ac11a489c2dd166a22736e/front_end/core/sdk/DebuggerModel.ts
[modify] https://crrev.com/fe515ee1af6aabf990ac11a489c2dd166a22736e/front_end/core/sdk/SourceMapManager.ts


### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/65b0c978621ed420d7c34e81c164db1c3e4422c9

commit 65b0c978621ed420d7c34e81c164db1c3e4422c9
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 25 13:18:35 2022

Roll DevTools Frontend from 6af28179c240 to 6bf92a7bd6e1 (3 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/6af28179c240..6bf92a7bd6e1

2022-07-25 jamclema@microsoft.com Fully hide the default SplitWidget resizer element
2022-07-25 szuend@chromium.org [debugger] Type sourceMapURL as string
2022-07-25 kprokopenko@chromium.org [DOMStorage] Update protocol +  call clearByStorageKey in the frontend

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1313434,chromium:1342722,chromium:1346065
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I81a07cbc5a7847f7c2a25f7a8bed28241272adb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3784063
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1027730}

[modify] https://crrev.com/65b0c978621ed420d7c34e81c164db1c3e4422c9/DEPS


### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/1a1e7c6f50b85ad086654f9a8562efa15a943de6

commit 1a1e7c6f50b85ad086654f9a8562efa15a943de6
Author: Simon Zünd <szuend@chromium.org>
Date: Thu Jul 28 05:28:18 2022

Prevent host bindings from loading resources from UNC paths

This CL prevents loading of source maps and other resources
from Windows Shares via file:// UNC URLs.

We show a warning similar to other failed source map loads, for
example when the source map was not found (404).

Screenshot: https://i.imgur.com/5wVfAO7.png

The CL also adds a setting that allows the user to disable this
behavior. Please note that the 'host' module can't have settings
themselves, otherwise we'd have a circular dependency between 'host'
and 'common'. That is why the CL places the setting in the 'network'
module, as that is also the bottle-neck for the `loadNetworkResource`
host binding. Even though the setting is in the 'network' module, the
CL places it in the sources category, as source map loading is the
dominant use case.

R=bmeurer@chromium.org, jarin@chromium.org

Fixed: 1342722
Change-Id: I878e77592703cbfa97828650f256c2b4e4a2ac0d
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3784603
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>

[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/front_end/core/i18n/locales/en-US.json
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/test/unittests/front_end/core/sdk/PageResourceLoader_test.ts
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/front_end/core/sdk/NetworkManager.ts
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/test/unittests/front_end/helpers/EnvironmentHelpers.ts
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/front_end/panels/timeline/TimelineLoader.ts
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/front_end/core/i18n/locales/en-XL.json
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/front_end/core/host/ResourceLoader.ts
[modify] https://crrev.com/1a1e7c6f50b85ad086654f9a8562efa15a943de6/front_end/panels/network/network-meta.ts


### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### zi...@gmail.com (2022-07-28)

The impact of the vulnerability was lowered to low, and I am still of the opinion that this is not the appropriate impact for this vulnerability. I would appreciate it if you would re-evaluate this vulnerability's impact and take @phistuck's comment into account.

### aj...@google.com (2022-07-29)

Thanks for the discussion everyone - I agree this might be Medium as it is like https://bugs.chromium.org/p/chromium/issues/detail?id=1301920#c15 but very mitigated in practice.

### [Deleted User] (2022-07-29)

Requesting merge to beta M104 because latest trunk commit (1027730) appears to be after beta branch point (1012729).

Requesting merge to dev M105 because latest trunk commit (1027730) appears to be after dev branch point (1027018).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-29)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sz...@chromium.org (2022-08-01)

1. Fix for a medium severity security bug.
2. https://crrev.com/c/3784603
3. Landed with 106.0.5207.0 and I verified the fix is working in Canary
4. No
6: No

### am...@chromium.org (2022-08-01)

 M105 merge approved, please merge this fix to branch 5195 at your earliest convenience. 

### gi...@appspot.gserviceaccount.com (2022-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/cac73333ada165be3c10fec00626968753155e3b

commit cac73333ada165be3c10fec00626968753155e3b
Author: Simon Zünd <szuend@chromium.org>
Date: Thu Jul 28 05:28:18 2022

Prevent host bindings from loading resources from UNC paths

This CL prevents loading of source maps and other resources
from Windows Shares via file:// UNC URLs.

We show a warning similar to other failed source map loads, for
example when the source map was not found (404).

Screenshot: https://i.imgur.com/5wVfAO7.png

The CL also adds a setting that allows the user to disable this
behavior. Please note that the 'host' module can't have settings
themselves, otherwise we'd have a circular dependency between 'host'
and 'common'. That is why the CL places the setting in the 'network'
module, as that is also the bottle-neck for the `loadNetworkResource`
host binding. Even though the setting is in the 'network' module, the
CL places it in the sources category, as source map loading is the
dominant use case.

R=​bmeurer@chromium.org, jarin@chromium.org

Fixed: 1342722
Change-Id: I878e77592703cbfa97828650f256c2b4e4a2ac0d
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3784603
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Simon Zünd <szuend@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
(cherry picked from commit 1a1e7c6f50b85ad086654f9a8562efa15a943de6)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3802970
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/front_end/core/i18n/locales/en-US.json
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/test/unittests/front_end/core/sdk/PageResourceLoader_test.ts
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/front_end/core/sdk/NetworkManager.ts
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/test/unittests/front_end/helpers/EnvironmentHelpers.ts
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/front_end/core/i18n/locales/en-XL.json
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/front_end/panels/timeline/TimelineLoader.ts
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/front_end/panels/network/network-meta.ts
[modify] https://crrev.com/cac73333ada165be3c10fec00626968753155e3b/front_end/core/host/ResourceLoader.ts


### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations, Andrea! The VRP Panel has decided to award you $7500 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us -- great work! 

### zi...@gmail.com (2022-08-05)

Thanks for the bounty. Much appreciated!

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1342722?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Platform>DevTools>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060207)*
