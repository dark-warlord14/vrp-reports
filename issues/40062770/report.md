# Security: SwiftShader binaries are included in the following Dockerfile by just pulling them from a bucket

| Field | Value |
|-------|-------|
| **Issue ID** | [40062770](https://issues.chromium.org/issues/40062770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Infra |
| **Platforms** | Linux |
| **Reporter** | an...@gmail.com |
| **Assignee** | jc...@google.com |
| **Created** | 2023-01-23 |
| **Bounty** | $2,000.00 |

## Description

Original (internal) report b/265118669

Vulnerability description
There is a Remote Code Execution vulnerability in your service at https://github.com/youtube/cobalt/blob/d2bc3b69d823bbaf46d1c4355b23486a85a6d791/third_party/skia/docker/skia-build-tools/Dockerfile.

NOTE: I did not reproduce this vulnerability. Reason: This Dockerfile does not really seem to be used by Cobalt, so low priority

Summary: code injection through .so file

Product: Youtube

URL: https://github.com/youtube/cobalt/blob/d2bc3b69d823bbaf46d1c4355b23486a85a6d791/third_party/skia/docker/skia-build-tools/Dockerfile

Vulnerability type: Remote Code Execution (RCE)

Details
hello team,

Summary
I found out that at the https://github.com/youtube/cobalt/blob/d2bc3b69d823bbaf46d1c4355b23486a85a6d791/third_party/skia/docker/skia-build-tools/Dockerfile in this Dockerfile, file there is a google bucket that is hosting binary file which can be used for execution in victim PC, as the google bucket is available for takeover.

The ADD instruction downloads 2 files from specific URL, libGLESv2.so and libEGL.so and places it under /usr/local/lib, this files are related to openGL es support. And it also changes the ownership of these files to user skia and group skia using --chown=skia:skia

Attack scenario
Step To Reproduce
https://github.com/youtube/cobalt/blob/d2bc3b69d823bbaf46d1c4355b23486a85a6d791/third_party/skia/docker/skia-build-tools/Dockerfile 2.you can see that
ADD --chown=skia:skia https://storage.googleapis.com/swiftshader-binaries/OpenGL_ES/Latest/Linux/libGLESv2.so /usr/local/lib/libGLESv2.so ADD --chown=skia:skia https://storage.googleapis.com/swiftshader-binaries/OpenGL_ES/Latest/Linux/libEGL.so /usr/local/lib/libEGL.so the script will download a .so which I have control over.

POC
I have takeover the https://storage.googleapis.com/swiftshader-binaries/index.html google bucket .

Impact
An attacker can take over the google bucket and upload malicious code in .so which will execute in the victim's PC


Reporter:
AnupamAS01


from jclinton@ of ChOPs Security:  
Indeed this seems to be addressed but that binaries were downloaded and used in the build process of unknown provenance is a BCID violation. We should also take over the old bucket to ensure that no one else is hit by the attacker.

I think the reporter should receiving a moderate reward for finding these two items as this is was valuable for us.



## Timeline

### am...@chromium.org (2023-01-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-23)

[Empty comment from Monorail migration]

[Monorail components: Infra]

### [Deleted User] (2023-01-23)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-24)

setting arbitrary foundin-108 to satisfy the bot (no merges are happening from this issue); setting jclinton@ as owner based on ChOPS involvement and input on b/265118669, but no action required here. 
May the Bot overlord be satisfied by this metadata sacrifice! 

### am...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-24)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-25)

there is no merge required here 

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

We are awaiting response on the buganizer bug to add the original reporter to this issue and issue this VRP reward to them. 

### am...@chromium.org (2023-01-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-27)

[Comment Deleted]

### am...@chromium.org (2023-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### an...@gmail.com (2023-02-02)

hello team,
I hope you are doing well ,
is the reward issued to me?

thanks 


### am...@chromium.org (2023-02-02)

Hello, the reward information has been sent over to the finance team for payment processing and are working arranging payment. 


### an...@gmail.com (2023-02-02)

thanks for the reward ,
sorry, I was just confused, as i didn't received a Congratulations message. 

thanks

### am...@chromium.org (2023-02-07)

Oh! apologies for that At the time the reward decision was made we didn't have your name or email address from the buganzier bug so I would have just been congratulating myself. Belated congratulations! And thank you again for the report!!

### [Deleted User] (2023-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1409650?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062770)*
