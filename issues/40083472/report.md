# Security: some extension bindings incorrectly injected into about:blank frames

| Field | Value |
|-------|-------|
| **Issue ID** | [40083472](https://issues.chromium.org/issues/40083472) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Mac, Windows, ChromeOS |
| **Reporter** | ju...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2015-12-30 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

A race condition allows for the injection of arbitrary content scripts in the context of any installed extension. We achieve this by setting the src of an iframe to a chrome-extension:// URL and injecting javascript before the frame has loaded.

**VERSION**  

Chrome Version: [47.0.2526.80] + dev  

Operating System: Debian 8.2

**REPRODUCTION CASE**  

For a demo, first make sure you have the hangouts plugin installed (<https://chrome.google.com/webstore/detail/google-hangouts/nckgahadagoaajjgafhacjanaoiihapd>).

Now visit <https://maxj.us/chromecsinj.html>

On that page the following iframe is loaded:

<iframe src="chrome-extension://nckgahadagoaajjgafhacjanaoiihapd/does/not/exist"></iframe>

Before the iframe has had a chance to fully load (document.location is still about:blank), we are able to execute content scripts from the parent page. To see that this is a race condition, try running s() from the console after the alert pops up.

## Attachments

- [chromecsinj.html](attachments/chromecsinj.html) (text/html, 592 B)

## Timeline

### mb...@chromium.org (2015-12-30)

Thanks for the report. If possible, could you please attach a proof of concept to this issue rather than hosting it at that location?

### ju...@gmail.com (2015-12-30)

Sure thing, attached.

### me...@google.com (2015-12-30)

I can confirm the repro works. Devlin, can you please take a look and reassign as appropriate?

### cl...@chromium.org (2015-12-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 34 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-17)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 48 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-02-18)

This is a high severity issue affecting stable so we should give it some attention of we can :)

rdevlin.cronin: Are you able to take a look?

### ra...@chromium.org (2016-02-18)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-02-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-03-10)

Antony or Istiaque, either of you have the time to take this on?  If not, I'll get around to it eventually, but I'm a bit swamped at the moment.

### la...@chromium.org (2016-03-10)

So the trick here is to run the script before the cross-site page navigation has committed? In that case, wouldn't the issue exist in any cross-site iframe and not just extension src ones?

### rd...@chromium.org (2016-03-11)

@14 - one difference is that for most pages, before the navigation occurs, scripting might not do you much good (it's about:blank). With extensions, you could access extension APIs.  Right now, this isn't terrible, since the script would only have access to limited APIs because it's an untrusted process, but if this repros with OOPIF it would be worse.  And, of course, it might turn  out that this is something that needs to be fixed somewhere other than the extensions level.

Adding Charlie as FYI and in case he has any thoughts.

### dc...@chromium.org (2016-03-11)

Hmm... why does an about:blank iframe have access to extension bindings? I wouldn't have expected these bindings to be injected until we're committing the navigation to the chrome-extension:// URL.

### rd...@chromium.org (2016-03-11)

I'd have to dig into it a bit more to be sure, but my guess is that we could trace it back to GetDataSourceURLForFrame(), which checks for the provisional data source url if the frame hasn't committed.

### cr...@chromium.org (2016-03-12)

That use of GetDataSourceURLForFrame for bindings sounds worth looking into.

At least in a manual test I just did (using DevTools rather than content scripts), if you inject script into the initial blank page of an iframe which is loading a slow URL, the injected code doesn't stick around after commit.  I haven't had time to check whether this exploit runs before or after the extension page commits.  (I know it's injected before-- does it run before as well?  Hopefully it doesn't exist after commit.)

### dc...@chromium.org (2016-03-12)

Injected code won't stick around, but non-persisted code being able to run stuff without extension bindings sounds scary: for example, if you captured the extension bindings into a closure, I wonder if you'd be able to call them indirectly via the closure...

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-21)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 40 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-06)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 55 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2016-05-23)

rdevlin.cronin@, any update on this one? Is it still possible to fix this Pri1 bug before M51 stable? Thanks! 

### rd...@chromium.org (2016-05-23)

I still haven't had time to look into this.  asargent@, this is tangentially related to web accessible resource work - any chance you can look into this?

### as...@chromium.org (2016-05-23)

Sure, I can have a look. 

### as...@chromium.org (2016-05-23)

Interestingly, it looks at the time the attacker-controlled script runs, the location.href is still about:blank and we've only injected the "default" extensions bindings like chrome.runtime and chrome.extension. This is still pretty bad - for instance, I was able to use chrome.runtime.sendMessage to send a fake message allegedly from hangouts to another extension (and it saw the sender as being hangouts, not about:blank), but for instance I wasn't able to use the chrome.tabs APIs (hangouts has this permission) to do something like modify an existing tab. 

What I see injected are the chrome.app, chrome.extensions, chrome.runtime, and chrome.i18n bindings.

I'm going to start digging further to try and figure out where the race condition is. 

### rd...@chromium.org (2016-05-23)

@5 Have you tried running with --site-per-process?  Right now, the iframe is an unblessed extension process, so we'd limit what APIs it has available, but if it's in a separate process (and we still allow scripting) we might allow things like chrome.tabs.

### rd...@chromium.org (2016-05-23)

*@25, not @5

### ju...@gmail.com (2016-05-24)

[Comment Deleted]

### as...@chromium.org (2016-05-24)

FYI, It looks like --site-per-process didn't make any difference - chrome.tabs still was unavailable. 


### ji...@chromium.org (2016-05-24)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-07-01)

Hey everybody, 6 months is too long for a High-severity vulnerability to live. Can someone please take this on as a high-priority task? Thank you!

### as...@chromium.org (2016-07-01)

Sorry for lack of updates - I've been working on this the last week or two and now have a tentative fix I'll be putting up for review soon. 

### ju...@gmail.com (2016-07-14)

[Comment Deleted]

### as...@chromium.org (2016-07-14)

FYI, I have a fix going through codereview currently:

https://codereview.chromium.org/2151693002/

Also, I'm changing the title to better reflect the nature of the bug as the current title "Universal content script injection using about:blank URLs" sort of overstates the nature of the vulnerability. (The worst behavior we've been able to think of is that you can impersonate messages from an extension, and it does not let you call most API methods). 




### bu...@chromium.org (2016-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/91f655b19888da3f86b57ad8c548da93e7b9aba4

commit 91f655b19888da3f86b57ad8c548da93e7b9aba4
Author: asargent <asargent@chromium.org>
Date: Fri Jul 22 18:39:18 2016

Fix extension bindings injection for iframes

For iframes, we don't want to use the source url for determining the
associated extension because it starts out with an about:blank context
that is scriptable by its parent.

BUG=573131

Review-Url: https://codereview.chromium.org/2151693002
Cr-Commit-Position: refs/heads/master@{#407214}

[modify] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/browser/extensions/extension_bindings_apitest.cc
[add] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/test/data/extensions/api_test/bindings/external_message_listener/background.js
[add] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/test/data/extensions/api_test/bindings/external_message_listener/manifest.json
[add] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/test/data/extensions/api_test/bindings/frames_before_navigation.html
[add] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/test/data/extensions/api_test/bindings/message_sender/background.js
[add] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/test/data/extensions/api_test/bindings/message_sender/manifest.json
[add] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/chrome/test/data/extensions/api_test/bindings/message_sender/public.html
[modify] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/extensions/renderer/script_context.cc
[modify] https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4/extensions/renderer/script_context_set.cc


### as...@chromium.org (2016-07-25)

Requesting permission to merge to M53 since this has been live on canary for a day or two. 


### di...@chromium.org (2016-07-25)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### bu...@chromium.org (2016-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d578daf3167747cbfe89cba4c4ca70a88e78651a

commit d578daf3167747cbfe89cba4c4ca70a88e78651a
Author: Antony Sargent <asargent@chromium.org>
Date: Mon Jul 25 17:41:31 2016

Fix extension bindings injection for iframes

For iframes, we don't want to use the source url for determining the
associated extension because it starts out with an about:blank context
that is scriptable by its parent.

BUG=573131

Review-Url: https://codereview.chromium.org/2151693002
Cr-Commit-Position: refs/heads/master@{#407214}
(cherry picked from commit 91f655b19888da3f86b57ad8c548da93e7b9aba4)

Review URL: https://codereview.chromium.org/2183443002 .

Cr-Commit-Position: refs/branch-heads/2785@{#331}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/browser/extensions/extension_bindings_apitest.cc
[add] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/test/data/extensions/api_test/bindings/external_message_listener/background.js
[add] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/test/data/extensions/api_test/bindings/external_message_listener/manifest.json
[add] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/test/data/extensions/api_test/bindings/frames_before_navigation.html
[add] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/test/data/extensions/api_test/bindings/message_sender/background.js
[add] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/test/data/extensions/api_test/bindings/message_sender/manifest.json
[add] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/chrome/test/data/extensions/api_test/bindings/message_sender/public.html
[modify] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/extensions/renderer/script_context.cc
[modify] https://crrev.com/d578daf3167747cbfe89cba4c4ca70a88e78651a/extensions/renderer/script_context_set.cc


### sh...@chromium.org (2016-07-26)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2016-07-26)

FYI, this change broke something in hangouts screen sharing, so I'm going to revert the merge from the M53 branch for now until I can figure out what's going wrong. 


### as...@chromium.org (2016-07-26)

The revert for M53 branch 2785 landed as https://codereview.chromium.org/2184833002

I accidentally used https://crbug.com/chromium/630928 for the BUG= line, which is the bug tracking the hangouts problem. 


### sh...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4b8ca0a9fbbe79fa5a7819917e5a31d237f0f499

commit 4b8ca0a9fbbe79fa5a7819917e5a31d237f0f499
Author: benwells <benwells@chromium.org>
Date: Thu Jul 28 07:38:36 2016

Revert of Fix extension bindings injection for iframes (patchset #5 id:120001 of https://codereview.chromium.org/2151693002/ )

Reason for revert:
This Cl caused a test failure under DrMemory.

First build with failing test: https://build.chromium.org/p/chromium.memory.fyi/builders/Windows%20Browser%20%28DrMemory%20full%29%20%282%29/builds/3969

Sample failure output: FramesExtensionBindingsApiTest.FramesBeforeNavigation:

[1420:4432:0722/173632:WARNING:chrome_browser_main_win.cc(419)] Command line too long for RegisterApplicationRestart

[1420:4432:0722/174006:INFO:CONSOLE(0)] "Denying load of chrome-extension://ficgdghpakbhhkmdjamiedmcoobamkoo/nonexistent.html. Resources must be listed in the web_accessible_resources manifest key in order to be loaded by pages outside the extension.", source: about:blank (0)

[1420:4432:0722/174015:INFO:CONSOLE(24)] "caught exception: SecurityError: Blocked a frame with origin "http://127.0.0.1:50285" from accessing a cross-origin frame.", source: http://127.0.0.1:50285/extensions/api_test/bindings/frames_before_navigation.html (24)

[1420:4432:0722/174018:INFO:CONSOLE(0)] "Denying load of chrome-extension://ficgdghpakbhhkmdjamiedmcoobamkoo/nonexistent.html. Resources must be listed in the web_accessible_resources manifest key in order to be loaded by pages outside the extension.", source: about:blank (0)

[1420:4988:0722/174053:WARNING:embedded_test_server.cc(193)] Request not handled. Returning 404: /favicon.ico

c:\b\build\slave\drm-cr\build\src\chrome\browser\extensions\extension_bindings_apitest.cc(257): error: Value of: page_success

Actual: false

Expected: true

Original issue's description:
> Fix extension bindings injection for iframes
>
> For iframes, we don't want to use the source url for determining the
> associated extension because it starts out with an about:blank context
> that is scriptable by its parent.
>
> BUG=573131
>
> Committed: https://crrev.com/91f655b19888da3f86b57ad8c548da93e7b9aba4
> Cr-Commit-Position: refs/heads/master@{#407214}

TBR=rdevlin.cronin@chromium.org,asargent@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=573131

Review-Url: https://codereview.chromium.org/2191793002
Cr-Commit-Position: refs/heads/master@{#408355}

[modify] https://crrev.com/4b8ca0a9fbbe79fa5a7819917e5a31d237f0f499/chrome/browser/extensions/extension_bindings_apitest.cc
[delete] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/chrome/test/data/extensions/api_test/bindings/external_message_listener/background.js
[delete] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/chrome/test/data/extensions/api_test/bindings/external_message_listener/manifest.json
[delete] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/chrome/test/data/extensions/api_test/bindings/frames_before_navigation.html
[delete] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/chrome/test/data/extensions/api_test/bindings/message_sender/background.js
[delete] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/chrome/test/data/extensions/api_test/bindings/message_sender/manifest.json
[delete] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/chrome/test/data/extensions/api_test/bindings/message_sender/public.html
[modify] https://crrev.com/4b8ca0a9fbbe79fa5a7819917e5a31d237f0f499/extensions/renderer/script_context.cc
[modify] https://crrev.com/4b8ca0a9fbbe79fa5a7819917e5a31d237f0f499/extensions/renderer/script_context_set.cc


### bu...@chromium.org (2016-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/79b64c3e741cc9c6afbb23885945831a45c6baa5

commit 79b64c3e741cc9c6afbb23885945831a45c6baa5
Author: asargent <asargent@chromium.org>
Date: Thu Aug 04 17:17:14 2016

Fix extension bindings injection for iframes (reland)

For iframes, we don't want to use the source url for determining the
associated extension because it starts out with an about:blank context
that is scriptable by its parent.

This originally landed in codereview.chromium.org/2151693002/ but
was reverted because of https://crbug.com/chromium/630928 as well as the test failing under
DrMemory (not with memory errors; just not succeeding which likely
indicates some kind of race condition in the test). I've added a fix for
https://crbug.com/chromium/630928 but haven't been able to locally reproduce the test failure
under DrMemory, so I've added some extra logging to the test to hopefully
better understand what might be going wrong.

Memory sheriffs: If the FramesExtensionBindingsApiTest.FramesBeforeNavigation
test fails again without any actual memory errors, please do not revert the
entire CL (since it is an important security fix); instead just disable the
test or add it to a suppression file so I can iterate on a fix.

BUG=573131,630928

Review-Url: https://codereview.chromium.org/2208483002
Cr-Commit-Position: refs/heads/master@{#409819}

[modify] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/browser/extensions/extension_bindings_apitest.cc
[modify] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/browser/extensions/extension_messages_apitest.cc
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/bindings/external_message_listener/background.js
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/bindings/external_message_listener/manifest.json
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/bindings/frames_before_navigation.html
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/bindings/message_sender/background.js
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/bindings/message_sender/manifest.json
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/bindings/message_sender/public.html
[add] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/chrome/test/data/extensions/api_test/messaging/externally_connectable/sites/popup_opener.html
[modify] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/extensions/renderer/script_context.cc
[modify] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/extensions/renderer/script_context.h
[modify] https://crrev.com/79b64c3e741cc9c6afbb23885945831a45c6baa5/extensions/renderer/script_context_set.cc


### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-08-18)

I just realized I forgot to remove the merge-merged-2785 label when I reverted my original patch. Removing it now. 

govind - my second attempt fix has been live on canary for a week and a half or so with no problem reports so far - is it ok to merge to M53, or you would you prefer I merge to M54 first and wait a couple days to see if everything is ok there first? 


### go...@chromium.org (2016-08-18)

M54 is not branched yet so no merged is needed.
For M53, I'm OK to take this merge in per your https://crbug.com/chromium/573131#c50  as it is well baked in canary for a week and a half. But it will be + inferno@'s call whether to take this in for M53 or not.

Re-adding "Merge-Request-53" label.

### di...@chromium.org (2016-08-18)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### go...@chromium.org (2016-08-18)

asargent@, M53 merge is auto approved so please merge ASAP. Thank you.

### bu...@chromium.org (2016-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c

commit 7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c
Author: Antony Sargent <asargent@chromium.org>
Date: Thu Aug 18 21:51:42 2016

Fix extension bindings injection for iframes (reland)

For iframes, we don't want to use the source url for determining the
associated extension because it starts out with an about:blank context
that is scriptable by its parent.

This originally landed in codereview.chromium.org/2151693002/ but
was reverted because of https://crbug.com/chromium/630928 as well as the test failing under
DrMemory (not with memory errors; just not succeeding which likely
indicates some kind of race condition in the test). I've added a fix for
https://crbug.com/chromium/630928 but haven't been able to locally reproduce the test failure
under DrMemory, so I've added some extra logging to the test to hopefully
better understand what might be going wrong.

Memory sheriffs: If the FramesExtensionBindingsApiTest.FramesBeforeNavigation
test fails again without any actual memory errors, please do not revert the
entire CL (since it is an important security fix); instead just disable the
test or add it to a suppression file so I can iterate on a fix.

BUG=573131,630928

Review-Url: https://codereview.chromium.org/2208483002
Cr-Commit-Position: refs/heads/master@{#409819}
(cherry picked from commit 79b64c3e741cc9c6afbb23885945831a45c6baa5)

Review URL: https://codereview.chromium.org/2257273002 .

Cr-Commit-Position: refs/branch-heads/2785@{#670}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/browser/extensions/extension_bindings_apitest.cc
[modify] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/browser/extensions/extension_messages_apitest.cc
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/bindings/external_message_listener/background.js
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/bindings/external_message_listener/manifest.json
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/bindings/frames_before_navigation.html
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/bindings/message_sender/background.js
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/bindings/message_sender/manifest.json
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/bindings/message_sender/public.html
[add] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/chrome/test/data/extensions/api_test/messaging/externally_connectable/sites/popup_opener.html
[modify] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/extensions/renderer/script_context.cc
[modify] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/extensions/renderer/script_context.h
[modify] https://crrev.com/7ba4c1bf12cc650bacfb38c1acc6e54120e4db4c/extensions/renderer/script_context_set.cc


### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-25)

Congratulations! The panel awarded $7,500 for this bug.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### as...@chromium.org (2016-08-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### ju...@gmail.com (2016-08-26)

Thank you!

### aw...@chromium.org (2016-09-08)

Thank you for donating; the payment has been made to the charity you selected.

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-12)

[Comment Deleted]

### aw...@chromium.org (2017-01-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/573131?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/631348]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083472)*
