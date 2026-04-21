# Security: Security: Clickjacking RCE of Chrome headless with Remote Debugging

| Field | Value |
|-------|-------|
| **Issue ID** | [40056642](https://issues.chromium.org/issues/40056642) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Headless, Platform>DevTools>Extensions |
| **Platforms** | Mac |
| **Reporter** | ma...@m-austin.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2021-07-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to compromise a local machine running an instance of Chrome headless with remote debugging enabled through a combination of Cross-site Scripting on the chrome-devtools-frontend.appspot.com domain, and Click-jacking the DevTools HTTP handler. Through these two vulnerabilities, it is possible to obtain the GUID for a WebSocket connection to the local Remote Debugger and arbitrarily read and write local files, including startup scripts that will auto execute on user login.

Proof of concept video: <https://www.youtube.com/watch?v=luAxoZYUKLg>

**VERSION**  

Chrome Version: Version 94.0.4583.1 (Official Build) canary (x86\_64)  

Operating System: MacOS 10.15.7

**REPRODUCTION CASE**  

To confirm this issue, perform the following steps:

1. Launch and instance of Chrome headless with remote debugging enabled. /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --remote-debugging-port=9222
2. Open the attached chrome.html, and click the button on the page.
3. Observe the JavaScript alert boxes showing the identified System users, and the contents of the following files if they exist locally: /etc/password, ~/.aws/credentials, ~/.ssh/id\_rsa.
4. Observe that a Launch Agent configuration has been downloaded to ~/Library/LaunchAgents/chromeRCE.plist

How the exploit works:

Chrome is running with something like: --headless --remote-debugging-port=9222 (or if a random port is selected we can use javascript to “port sniff” using one of the devtools)

Frame #1 - Clickjacking:  

An iframe is created for Click-jacking the headless remote debugging UI, similar to:

<iframe src=”http://127.0.0.1:9222”></iframe>

The headless remote debugging UI inside Frame1 includes links to the UI hosted on chrome-devtools-frontend.appspot.com, like the following:

<https://chrome-devtools-frontend.appspot.com/serve_file/@1ea76e193b4fadb723bfea2a19a66c93a1bc0ca6/inspector.html?ws=127.0.0.1:9222/devtools/page/A375BA1BB436B2ADE802B44A94C934D6&remoteFrontend=true>

On our page we can set this frame to be 100% transparent, then specifically position a button over the iframe to “Clickjack” the user. This will render a click into the devtools UI, navigating the frame from <http://127.0.0.1:9222/> to the chrome-devtools-frontend.appspot.com domain with the WebSocket token in the URL.

Frame #2 - XSS / Bridge:  

Once the user has clicked through Frame 1, another iframe is created within the exploit page that leverages a Cross-site scripting vector on chrome-devtools-frontend.appspot.com, similar to the following:

<https://chrome-devtools-frontend.appspot.com/serve_rev/@191797/devtools.html?remoteFrontendUrl=javascript:alert(1)>

The XSS issue has been detailed in the following tickets:

<https://bugs.chromium.org/p/chromium/issues/detail?id=607939>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=618333>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=619414>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=775527>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=798163>

The XSS vector on Frame 2 can access top.frames[0] and grab the location.href of Frame 1, because they are now on the same origin domain. The XSS is then used to transmit the WebSocket GUID in the URL up to the exploit domain via top.postMessage.

The parent exploit page now has enough information to connect to the local WebSocket running remote debugging using the Chrome Debugging Protocol (<https://github.com/cyrus-and/chrome-remote-interface> or <https://unpkg.com/puppeteer-web>).

To read local directories and files, we simply opened and parsed file:// URLs. To write arbitrary files, we enable the functionality with Page.setDownloadBehavior in the debugging API, and specify the target directory, like /Users/.../Library/LaunchAgents/.

**CREDIT INFORMATION**  

Reporter credit: @DanAmodio and @mattaustin from Contrast Security

## Attachments

- [chrome.html](attachments/chrome.html) (text/plain, 8.5 KB)
- [ChromeDevToolsExploit.mp4](attachments/ChromeDevToolsExploit.mp4) (video/mp4, 1.5 MB)

## Timeline

### [Deleted User] (2021-07-23)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-23)

+devtools folks - can you please take a look at this and help assess the security ramifications?

reporter: thanks for the report. Do you mind attaching the video on this bug? it's a) private so we can't see it, and b) ideally we keep all the details for reported bugs in the tracker.

[Monorail components: Platform>DevTools>Platform]

### ma...@m-austin.com (2021-07-23)

Oops i intended to make that "unlisted", but i attached the video as requested. 

### bm...@chromium.org (2021-07-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Headless]

### [Deleted User] (2021-07-23)

[Empty comment from Monorail migration]

### ma...@m-austin.com (2021-07-23)

Would it be possible to add another external collaborator (deige101@gmail.com) to the ticket?

### ya...@chromium.org (2021-07-23)

Interesting issue. Thanks for reporting!

Any developer who runs a remote debugging instance may be victim of this attack if they browse the web at the same time. That's why I'm upgrading the severity.

It seems to me that applying the right cross-origin resource policy to chrome-devtools-frontend.appspot.com would block the XSS. Wolfgang, could you confirm and advice what policy we should set?


### ya...@chromium.org (2021-07-23)

And we should also apply CORS-RFC1918 in order to avoid embedding localhost into a non-localhost external page.

And we should probably prevent read and write capability for hosted mode.

### [Deleted User] (2021-07-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2021-07-23)

I don't think this is specific to headless -- --remote-debugging-port is also available for headful as well, and arguably can do more harm in the case of a headful browser.

I think the ultimate culprit here is --remote-debugging-port, as it is inherently insecure. We already recommend against using it and offer --remote-debugging-pipe as a more secure alternative (although it may not be usable in certain scenarios). We should aim at either deprecating --remote-debugging-port altogether, or requiring some strong form of authentication (a client certificate, perhaps?). See also b/185307177 for more problems caused by --remote-debugging-port.

As a short-term mitigation of this particular problem, I assume forbidding iframing of the localhost:9222 discovery page should be effective. Another option is to remove this page altogether, as there's a better alternative in the form of chrome://inspect that should not be susceptible to an exploit like this.

Doing better URL params sanitation on the front-end side might be nice as well, but considering we'll essentially dealing with archived older version of the front-end, it's probably not going to be immediately efficient.

"hosted mode" is a notion of the front-end, and the front-end role is rather indirect in this exploit, what happens here is that we just leak a CDP WebSocket URL, which is then being exploited without front-end being involved, so the only thing that can be done on the CDP level would be to treat any HTTP remote clients as insecure (similarly to the extensions). That's a palatable option, especially with the prospective of migrating the clients away from --remote-debugging-port, but it may as well break some users of external tools (puppeteer / ChromeDriver etc).


### ya...@google.com (2021-07-23)

indeed removing the localhost:9222 page might be a feasible short term solution.

### ya...@chromium.org (2021-07-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8e23347b3e089cd00c9d3741b394b92c21f70f88

commit 8e23347b3e089cd00c9d3741b394b92c21f70f88
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Jul 27 04:38:39 2021

Forbid embedding DevTools discovery page as an iframe

Also, mark the discovery page as deprecated and recommend
using chrome://inspect instead.

Bug: 1232509, 1232279
Change-Id: I41f8e9f4914d53b72b82ed8343612ad5bb794ce5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3049717
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#905584}

[modify] https://crrev.com/8e23347b3e089cd00c9d3741b394b92c21f70f88/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/8e23347b3e089cd00c9d3741b394b92c21f70f88/chrome/browser/devtools/frontend/devtools_discovery_page.html
[add] https://crrev.com/8e23347b3e089cd00c9d3741b394b92c21f70f88/chrome/test/data/devtools/discovery_page/background.js
[add] https://crrev.com/8e23347b3e089cd00c9d3741b394b92c21f70f88/chrome/test/data/devtools/discovery_page/manifest.json
[modify] https://crrev.com/8e23347b3e089cd00c9d3741b394b92c21f70f88/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/8e23347b3e089cd00c9d3741b394b92c21f70f88/headless/lib/resources/devtools_discovery_page.html


### ca...@chromium.org (2021-07-27)

I've actually tried to repro with a headfull chrome, and it turns out it is indeed headless specific, as the headfull version serves the front-end from localhost and is thus is not susceptible to (at least, known) XSS issues of older front-end. So, perhaps, we could downgrade the severity, given that this is headless-specific.

Other than that, the problem is fixed by the commit referenced in #15.

Requesting merge to m93 just in case, deferring to security team whether merge to earlier releases is justified,

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

Your change meets the bar and is auto-approved for M93. Please go ahead and merge the CL to branch 4577 (refs/branch-heads/4577) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-08-02)

Your change has been approved for M93. Please go ahead and merge the CL to branch 4577 manually asap, so that it would be part of this week’s Beta release.

### pb...@google.com (2021-08-02)

Your change has been approved for M93. Please go ahead and merge the CL to branch 4577 manually asap, so that it would be part of this week’s Beta release.

### [Deleted User] (2021-08-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-08-03)

Please complete your merges to M93 today asap. I am cutting beta RC today at 3pm PST, so please help complete merges so we can include in this weeks beta release

### gi...@appspot.gserviceaccount.com (2021-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b2a2af62825bab8790135f41d3f7bcf25db513a

commit 8b2a2af62825bab8790135f41d3f7bcf25db513a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Aug 04 02:27:50 2021

Forbid embedding DevTools discovery page as an iframe

Also, mark the discovery page as deprecated and recommend
using chrome://inspect instead.

(cherry picked from commit 8e23347b3e089cd00c9d3741b394b92c21f70f88)

Bug: 1232509, 1232279
Change-Id: I41f8e9f4914d53b72b82ed8343612ad5bb794ce5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3049717
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#905584}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3064289
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#417}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/8b2a2af62825bab8790135f41d3f7bcf25db513a/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/8b2a2af62825bab8790135f41d3f7bcf25db513a/chrome/browser/devtools/frontend/devtools_discovery_page.html
[add] https://crrev.com/8b2a2af62825bab8790135f41d3f7bcf25db513a/chrome/test/data/devtools/discovery_page/background.js
[add] https://crrev.com/8b2a2af62825bab8790135f41d3f7bcf25db513a/chrome/test/data/devtools/discovery_page/manifest.json
[modify] https://crrev.com/8b2a2af62825bab8790135f41d3f7bcf25db513a/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/8b2a2af62825bab8790135f41d3f7bcf25db513a/headless/lib/resources/devtools_discovery_page.html


### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations - the VRP Panel has decided to award you $3,000 for this report! A member of our finance team will be in touch soon to arrange payment. Thank you for reporting this issue! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M92, which branched on 2021-05-20 (Chromium branch: 4515, Chromium branch position: 885287)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-25)

please merge to M92, branch 4515, at your earliest convenience. While there are no further planned releases of M92 at this time, 92 will become the Extended Stable release channel upon M93 promotion as we transition to the 4W stable channel release cycle. Thanks! 

### sr...@google.com (2021-08-27)

assigning back to get engineer attention for M92 merge ( please merge asap) for extended stable release. Complete by 3pm PST today

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

caseq: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-08-30)

created a CP for M92 CL - https://chromium-review.googlesource.com/c/chromium/src/+/3128603

### gi...@appspot.gserviceaccount.com (2021-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/74a4908b9e33ea73edb461c26fa6434c21e97ca4

commit 74a4908b9e33ea73edb461c26fa6434c21e97ca4
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Mon Aug 30 16:54:52 2021

Forbid embedding DevTools discovery page as an iframe

Also, mark the discovery page as deprecated and recommend
using chrome://inspect instead.

(cherry picked from commit 8e23347b3e089cd00c9d3741b394b92c21f70f88)

Bug: 1232509, 1232279
Change-Id: I41f8e9f4914d53b72b82ed8343612ad5bb794ce5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3049717
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#905584}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3128603
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2098}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/74a4908b9e33ea73edb461c26fa6434c21e97ca4/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/74a4908b9e33ea73edb461c26fa6434c21e97ca4/chrome/browser/devtools/frontend/devtools_discovery_page.html
[add] https://crrev.com/74a4908b9e33ea73edb461c26fa6434c21e97ca4/chrome/test/data/devtools/discovery_page/background.js
[add] https://crrev.com/74a4908b9e33ea73edb461c26fa6434c21e97ca4/chrome/test/data/devtools/discovery_page/manifest.json
[modify] https://crrev.com/74a4908b9e33ea73edb461c26fa6434c21e97ca4/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/74a4908b9e33ea73edb461c26fa6434c21e97ca4/headless/lib/resources/devtools_discovery_page.html


### ca...@google.com (2021-08-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M94, which branched on 2021-08-12 (Chromium branch: 4606, Chromium branch position: 911515)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4256065890eda5825c1da6811a0aadcf7a7ad3e1

commit 4256065890eda5825c1da6811a0aadcf7a7ad3e1
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Sep 10 14:25:30 2021

[M90-LTS] Forbid embedding DevTools discovery page as an iframe

Also, mark the discovery page as deprecated and recommend
using chrome://inspect instead.

M90 merge conflicts:
* devtools_browsertest.cc in original commit is named
  devtools_sanity_browsertest.cc in M90.

(cherry picked from commit 8e23347b3e089cd00c9d3741b394b92c21f70f88)

(cherry picked from commit 74a4908b9e33ea73edb461c26fa6434c21e97ca4)

Bug: 1232509, 1232279
Change-Id: I41f8e9f4914d53b72b82ed8343612ad5bb794ce5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3049717
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#905584}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3128603
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#2098}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3148056
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1596}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/4256065890eda5825c1da6811a0aadcf7a7ad3e1/chrome/browser/devtools/devtools_sanity_browsertest.cc
[modify] https://crrev.com/4256065890eda5825c1da6811a0aadcf7a7ad3e1/chrome/browser/devtools/frontend/devtools_discovery_page.html
[add] https://crrev.com/4256065890eda5825c1da6811a0aadcf7a7ad3e1/chrome/test/data/devtools/discovery_page/background.js
[add] https://crrev.com/4256065890eda5825c1da6811a0aadcf7a7ad3e1/chrome/test/data/devtools/discovery_page/manifest.json
[modify] https://crrev.com/4256065890eda5825c1da6811a0aadcf7a7ad3e1/content/browser/devtools/devtools_http_handler.cc
[modify] https://crrev.com/4256065890eda5825c1da6811a0aadcf7a7ad3e1/headless/lib/resources/devtools_discovery_page.html


### as...@google.com (2021-09-10)

[Empty comment from Monorail migration]

### sr...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### ma...@m-austin.com (2021-12-07)

Any timeline on making this public? 

### [Deleted User] (2021-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1232279?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Headless, Platform>DevTools>Platform]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056642)*
