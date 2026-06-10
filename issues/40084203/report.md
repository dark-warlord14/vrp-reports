# Security: Devtools allows running privileged scripts via XSS on chrome-devtools-frontend.appspot.com

| Field | Value |
|-------|-------|
| **Issue ID** | [40084203](https://issues.chromium.org/issues/40084203) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Privacy and Security |
| **CVE IDs** | CVE-2016-1699 |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-04-29 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

Specifically crafted input to whitelisted URLs on Devtools remote frontend, an attacker  

can run privileded code in Chrome with filesystem access.

The issue is similar to <https://crbug.com/chromium/571121>, but it has a different attack vector.

Overview:  

Chrome's remote devtools front-end accessed pages only from whitelisted domain (<https://chrome-devtools-frontend.appspot.com/>).  

Src: <https://chromium.googlesource.com/chromium/chromium/+/trunk/chrome/browser/ui/webui/devtools_ui.cc> [var: kRemoteFrontendBase]

For example accessing in Chrome:  

chrome-devtools://devtools/remote/serve\_rev/@199588/devtools.html loads  

<https://chrome-devtools-frontend.appspot.com/serve_rev/@199588/devtools.html>

However, the above URL takes an input param "remoteFrontendUrl" which is used to write an iframe's src param without sanitization.  

( document.write("<iframe id='inspector-app-iframe' class='fill' src='" + src + "'></iframe>"); )  

The CSP of the page allows unsafe-eval, and unsafe-inline javascript execution. This allows an attacker to run javascript  

code in context of devtools.

On first load, access to DevToolsAPI/DevToolsHost was not available and isHosted() call returned true. This didn't provide file-system access.  

However, I noticed that but triggering a reload was enough to change behaviour ie. isHosted() returns false, and also exposes more objects [DevToolsAPI/DevToolsHost].  

The above behaviour [reload] could be a different bug (didn't investigate root cause).

Demo Attack Script [pre-encoding]:  

function f() {  

c='d="",DevToolsAPI.streamWrite=function(e,o){d+=o},DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///C:/","",0],function(e){d.split("\n").map(function(e){e.match(/addRow.\*;/)&&document.write(e.match(/addRow.\*;/)[0]);})});' ;  

document.write("<script>window.parent.document.write('<script>'+c+'</scr'+'ipt>');</scr"+"ipt>");  

}  

if( typeof window.parent.DevToolsHost == "undefined" )  

setTimeout('window.parent.location.reload()', 100) ;  

else  

setTimeout('f()', 100) ;

The final exploit is delivered by specifying the providing the above script in encoded form as iframe's src url as javascript:eval(..).  

( The javascript was minified inorder to keep the input param to resonable size. Larger input causes the server to return bad request. )

**VERSION**  

Chrome Version: 50.0.2661.94m  

Operating System: All

**REPRODUCTION CASE**  

Copy-paste the full URL from the attached Devtools-Crafted-URI.txt into Chrome omnibox.  

For demo purposes, it displays the content of C:\ drive

## Attachments

- [Devtools-Crafted-URI.txt](attachments/Devtools-Crafted-URI.txt) (text/plain, 1.8 KB)

## Timeline

### el...@chromium.org (2016-04-29)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools>Security]

### me...@chromium.org (2016-04-29)

dgozman: Can you please take a look?

### rs...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-05-11)

I believe this issue can be resolved by disallowing remote frontend access to old revisions hosted on https://chrome-devtools-frontend.appspot.com/.

### me...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-14)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2016-05-16)

@dgozman: I don't think there is an issue here: there is no "remoteFrontendUrl" in our system and "remoteBase" is sanitized. Could you verify and close this?

### dg...@chromium.org (2016-05-16)

Old frontend versions used to have remoteFrontendUrl. I think we can filter in compatibility script.

### pf...@chromium.org (2016-05-16)

Ah. I wonder if remote modules should be managed by embedder only.

### bu...@chromium.org (2016-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c5eecf67fd8d5e8d24d2d4d9489753d2c8cf6c59

commit c5eecf67fd8d5e8d24d2d4d9489753d2c8cf6c59
Author: dgozman <dgozman@chromium.org>
Date: Mon May 16 22:26:05 2016

[DevTools] Sanitize remoteFrontendUrl for old frontends.

BUG=607939

Review-Url: https://codereview.chromium.org/1983933002
Cr-Commit-Position: refs/heads/master@{#393952}

[modify] https://crrev.com/c5eecf67fd8d5e8d24d2d4d9489753d2c8cf6c59/third_party/WebKit/Source/devtools/front_end/devtools.js


### dg...@chromium.org (2016-05-16)

Should be fixed - the crafted url from attachment doesn't work for me anymore.

### cl...@chromium.org (2016-05-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-05-18)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-05-18)

[Comment Deleted]

### ti...@google.com (2016-05-24)

Thanks for the report! We'll assess this under our Chrome Security Reward program - full details here: https://www.google.com/about/appsecurity/chrome-rewards/

Fix is already in M52 - let's try to get this into M-51 by 4pm today.


### ti...@google.com (2016-05-24)

[Automated comment] Less than 2 weeks to go before stable on M51, manual review required.

### ss...@google.com (2016-05-25)

Merge approved for M51 (branch 2704)

### bu...@chromium.org (2016-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/691a0629b89c7118063365a6846bc6baa0a0b0e5

commit 691a0629b89c7118063365a6846bc6baa0a0b0e5
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Wed May 25 17:50:49 2016

Merge to 2704 "[DevTools] Sanitize remoteFrontendUrl for old frontends."
>[DevTools] Sanitize remoteFrontendUrl for old frontends.
>
>BUG=607939
>
>Review-Url: https://codereview.chromium.org/1983933002
>Cr-Commit-Position: refs/heads/master@{#393952}
TBR=pfeldman@chromium.org
(cherry picked from commit c5eecf67fd8d5e8d24d2d4d9489753d2c8cf6c59)

Review URL: https://codereview.chromium.org/2010783002 .

Cr-Commit-Position: refs/branch-heads/2704@{#658}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/691a0629b89c7118063365a6846bc6baa0a0b0e5/third_party/WebKit/Source/devtools/front_end/devtools.js


### ti...@google.com (2016-05-31)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-06-03)

Noticed that I got credited, CVE assigned (+ reward mentioned) @ http://googlechromereleases.blogspot.in/2016/06/stable-channel-update.html (51.0.2704.79)

The labels haven't been updated here yet. Can we get the ball rolling ? :)


### ti...@google.com (2016-06-06)

#21: You're too fast! :)

Some notes from the reward panel regarding your reward: Reduced amount due to the user interaction required and pre-conditions for exploitation (copy-paste into DevTools or requires a malicious extension).

Someone from our finance department will be contact within 7 days to collect payment details. If that doesn't happen, please either update the bug or reach out to me at timwillis@.

CVE-ID is CVE-2016-1699.

Thanks again for your report - looking forward to seeing you back here sometime soon!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### ti...@google.com (2016-06-06)

Updating severity.

### ti...@google.com (2016-06-06)

[Empty comment from Monorail migration]

### gr...@gmail.com (2016-06-07)

Thank you :)

### gr...@gmail.com (2016-06-08)

I was able to bypass the fix (in combination with XSS Auditor bypass). Details @ https://crbug.com/chromium/618333

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### mf...@chromium.org (2017-11-14)

dgozman@: PTAL at https://bugs.chromium.org/p/chromium/issues/detail?id=780484#c24

### dg...@chromium.org (2017-11-14)

https://crbug.com/chromium/775527 tracks this (slightly different, but similar) problem. The original one was fixed.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/607939?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084203)*
