# Security: Webpages have access to some extension resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40081669](https://issues.chromium.org/issues/40081669) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Reporter** | pi...@live.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2015-03-19 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

It is possible to load some extension JavaScript resources from a regular webpage by adding setters to `Object.prototype`. In principle, only a couple of such resources are loaded by default when e.g. `chrome.webstore.onDownloadProgress` is accessed from a webpage. However, some extra resources can be loaded using these setters, and some functions inside these resources can be intercepted and certain native functions can then be called indirectly.

Some actions that are then possible are (including the release channel where the corresponding attachment works):

- [Stable+Canary, attachment bindtogc.html] Have a function called when an object has been garbage collected.
- [Stable+Canary, attachment blob.html] Get internal Blob UUIDs from a Blob and vice versa. This can, in theory, be used to share blobs cross-origin, but it requires first obtaining (guessing) an 128-bit cryptographically random UUID. (On stable, the attachment requires a slightly different `getBlob` function to work, see comment.)
- [Stable+Canary, attachment incognito.html] Get a boolean stating whether the page is viewed in incognito mode or not.
- [Canary only, attachment gesture.html] Execute functions that require an user gesture (e.g. `window.open`, `webkitRequestFullscreen`) without an user gesture.

It does not seem possible to intercept the native functions directly, but the JavaScript functions that call them can be intercepted. By passing a custom `this` value and/or custom arguments to certain functions, certain code paths can be triggered, and some native functions can be (indirectly) called with attacker-controlled data.

For example, accessing `chrome.webstore.onDownloadProgress` causes e.g. the `lastError` resource to be loaded. Intercepting the `run` function and calling it with certain arguments causes e.g. the `bindings` resource to be loaded. The `Binding.prototype.generate` function in `bindings` can be intercepted and then called with a certain `this` value to enter the function `createCustomType`. This function calls `require` with an attacker-controlled argument. This means other resources can be loaded (e.g. `webView`) which give access to some new native functions (e.g. `WebViewImpl.prototype.makeElementFullscreen`, which allows a gesture-required function to be called without a gesture).

I am not sure of a proper fix. The `exports` object in the resources system can be set to an `Object.create(null)` object so that it does not inherit from `Object.prototype`, but it would still be possible to intercept `bar` when code such as `Foo.prototype.bar = ...` is executed.

**VERSION**  

Chrome Version: In the above list, "Stable" refers to 41.0.2272.89 m, and "Canary" refers to 43.0.2338.1 canary SyzyASan  

Operating System: Windows 8.1 64-bit

**REPRODUCTION CASE**  

I am afraid the attachments are a bit dirty; they are such that certain code paths are triggered in the resources. Please let me know if they are not clear.

## Attachments

- [incognito.html](attachments/incognito.html) (text/html, 2.5 KB)
- [bindtogc.html](attachments/bindtogc.html) (text/html, 1.8 KB)
- [gesture.html](attachments/gesture.html) (text/html, 2.5 KB)
- [blob.html](attachments/blob.html) (text/html, 4.0 KB)
- [crossorigin_parent.html](attachments/crossorigin_parent.html) (text/plain, 2.7 KB)
- [crossorigin_child.html](attachments/crossorigin_child.html) (text/plain, 2.8 KB)
- [crash.html](attachments/crash.html) (text/plain, 2.5 KB)
- [crash.html](attachments/crash_53270506.html) (text/plain, 1.6 KB)
- [crash.html](attachments/crash_53270518.html) (text/plain, 2.1 KB)

## Timeline

### ke...@chromium.org (2015-03-20)

Thanks for the report. Interesting find.

danno@: This is a bindings issue, do you know who might be a good owner for this?

### ke...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-04-07)

PTAL

### jo...@chromium.org (2015-04-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-10)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-04)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 44 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

@kalman - do you have bandwidth to get this fixed in the next week or so?

@hablich - pending kalman's availability, may need you to find another owner.

### ha...@chromium.org (2015-05-11)

As this is a ChromeExtension issue I don't know if I can be of much help here. I added Miket@ and haraken@ on CC, maybe they know a good owner.

### mi...@chromium.org (2015-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-05-20)

kalman says he does not have cycles to work on this now.  It's basically the same bug as https://crbug.com/471523.  Assigning to jleichtling to find a new owner.

### [Deleted User] (2015-05-20)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-05-27)

Paraphrasing from jleichtling:

"Kalman he created the blocking bug crbug.com/490320 that provides a good explanation of the work that needs to be done. So there's a question of the priority for the general fix, which is quite a lot of effort

### ha...@chromium.org (2015-05-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-11)

jleichtling@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-06-11)

This extension is blocked on https://crbug.com/chromium/490320, in which we discuss a general class of security issues caused by monkey patching extension APIs implemented in JS.

### [Deleted User] (2015-06-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-10)

jleichtling@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-07-14)

Assigning to Kalman as I'm transitioning roles in ~3 weeks. Update in #17 still holds.

### wf...@chromium.org (2015-07-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-05)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-26)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-09-16)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-08)

kalman@: Uh oh! This issue is still open and hasn't been updated in the last 85 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-29)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 106 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ji...@chromium.org (2015-11-10)

Updating milestone label to M-48 since this is still blocked by https://crbug.com/chromium/490320.

### cl...@chromium.org (2015-11-19)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 127 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-12-11)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 149 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rd...@chromium.org (2015-12-14)

The root cause of this vulnerability is the same as crbug.com/546677, which has been fixed.  I haven't yet got around to combing through the various pieces of this to make sure *everything* we were doing wrong is better, but this is no longer an active vulnerability and no longer repros.

(Note: like this, https://crbug.com/chromium/546677 has multiple pieces and is still open, but again, the main vulnerability has been fixed.)

### cl...@chromium.org (2016-01-05)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-26)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-17)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 64 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-03-04)

rdevlin.cronin@, seems issue https://crbug.com/chromium/546677 is closed. Shall we close this one as well? 

### mb...@chromium.org (2016-03-04)

[Empty comment from Monorail migration]

### mi...@chromium.org (2016-03-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 86 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-03-10)

None of these cases reproduce anymore as a result of our bindings hardening.  There's probably some more somewhere (Yay inherently monkey-patchable JS!), but I'm going to close this bug.

### cl...@chromium.org (2016-03-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### pi...@live.nl (2016-03-24)

I do not have access to https://crbug.com/chromium/546677, but I do see a corresponding CL [1] with the `exports.$set` change. I am afraid that CL doesn't completely fix the vulnerability I reported here.

Some modules such as the webstore one don't use `$set`. Moreover, inside `binding.js`, `Binding.create` is still set the regular way. Thus, I can overwrite `Binding.create` and subsequently also `Binding.prototype.generate`. Quite some modules do `exports.$set('binding', binding.generate())`, and so I can still get those modules. In particular, I can still obtain the `test` module and thereby obtain the module system (e.g. `requireNative`) like I did for https://crbug.com/chromium/497507 and https://crbug.com/chromium/504011 (those specific issues are fixed, though).

In fact, I found two new exploits using `requireNative`, in `guest_view_internal_custom_bindings.cc` (see attachments):

 - Browser crash in `RegisterView`. My guess is that it is a CHECK in browser code [2] but I did not confirm this. So it likely is not a security vulnerability, but nevertheless nasty.

 - Cross-origin object sharing. However, both websites (victim and attacker) need to exploit the bug, so usability is limited. The trick here is to leverage `weak_view_map`, which is a per-renderer map of integers to JavaScript objects. If two websites are in the same renderer, website A can put something in the map (through `RegisterView`) and website B can fetch it (through `GetViewByID`).

 [1] https://chromium.googlesource.com/chromium/src/+/83a4b3aa72d98fe4176b4a54c8cea227ed966570
 [2] https://code.google.com/p/chromium/codesearch#chromium/src/components/guest_view/browser/guest_view_manager.cc&l=295


### bu...@chromium.org (2016-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/180e7e74926ea32ac039821926542452d1201c5e

commit 180e7e74926ea32ac039821926542452d1201c5e
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Mon Mar 28 19:34:12 2016

[Extensions] More bindings hardening

Revision 83a4b3aa72d98fe4176b4a54c8cea227ed966570 missed a few
(c/r/resources/extensions).

BUG=468931
BUG=591164

Review URL: https://codereview.chromium.org/1840453002

Cr-Commit-Position: refs/heads/master@{#383541}

[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/app_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/automation/automation_node.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/automation_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/browser_action_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/cast_streaming_receiver_session_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/cast_streaming_rtp_stream_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/cast_streaming_session_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/cast_streaming_udp_transport_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/certificate_provider_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/chrome_direct_setting.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/chrome_setting.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/content_setting.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/declarative_content_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/desktop_capture_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/developer_private_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/downloads_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/enterprise_platform_keys/internal_api.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/enterprise_platform_keys_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/feedback_private_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/file_browser_handler_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/file_entry_binding_util.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/file_manager_private_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/file_system_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/file_system_provider_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/gcm_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/identity_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/image_writer_private_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/input.ime_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/log_private_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/media_galleries_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/notifications_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/notifications_test_util.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/omnibox_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/page_action_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/page_capture_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/platform_keys/get_public_key.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/platform_keys/internal_api.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/platform_keys/key.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/platform_keys/utils.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/platform_keys_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/sync_file_system_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/system_indicator_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/tab_capture_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/tabs_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/tag_watcher.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/tts_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/tts_engine_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/web_view/chrome_web_view_internal_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/webrtc_desktop_capture_private_custom_bindings.js
[modify] https://crrev.com/180e7e74926ea32ac039821926542452d1201c5e/chrome/renderer/resources/extensions/webstore_custom_bindings.js


### pi...@live.nl (2016-03-30)

Thanks for the fix. However, I'm afraid the fix is not complete.

The ability to install setters on `exports` objects is not essential. Rather, (almost) *any* assignment of the form `obj.foo = bar` in the modules can make those modules call into the attacker's script. The `Binding.create` assignment in binding.js is of this form, and it turns out that assignment is sufficient to obtain `requireNative`.

See simplified attachment (warning: crashes the browser).

### pi...@live.nl (2016-04-13)

I saw commit [1], which makes it harder to exploit this bug. But exploiting is still possible.

Binding.prototype.generate calls runHooks_ at the end, which calls each customHooks_ function with the schema object. By intercepting customHooks_ and adding a custom hook in that array, the schema's context is leaked to the attacker. So, we can add getters to that context's Object.prototype, and then call Binding.prototype.generate. That function is now fooled by the getters, and with some additional trickery it can be fooled into loading the test module, and we can obtain requireNative as usual. See modified attachment for the browser crash.

PS: I wonder what those other bugs related to extension bindings are about. Did others find the same bug? (I don't have access to them.) I found that https://crbug.com/chromium/497597 (a special case of this one) was accidentally published. It seems to me that others could have been using my PoC.

 [1] https://chromium.googlesource.com/chromium/src/+/c089219d5f8794747f7ab7b966b4676f49532e1f

### pi...@live.nl (2016-04-13)

(Sorry, that should read "https://crbug.com/chromium/497507".)

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-22)

Pim - as an update, we're going to pay you $1,000 for the initial report and we'll keep this open for further work (and possibly further rewards).

rdevlin.cronin@ - can you please address Pim's comment at #47? Marking this as assigned so that it pops up on your radar.

### rd...@chromium.org (2016-04-22)

@50,47 - The general problem here is that our bindings leaked to the web page in multiple ways.  There's quite a bit of ongoing work to address all these issues.  I'll circle back to these once we've done a bit more so as to not prematurely mark them as fixed. :)

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-04-23)

Clusterfuzz - see https://crbug.com/chromium/468931#c51.

### cl...@chromium.org (2016-04-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### ti...@google.com (2016-04-25)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-26)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-26)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-04-26)

Clusterfuzz is going haywire on this issue.  For all humans, note this isn't fully fixed.

### ti...@google.com (2016-04-26)

mbarbella@ to the rescue - it's the merge-triage label.

### ti...@google.com (2016-04-26)

rdevlin - please make sure to re-add Merge-Triage when the bug is finally fixed.

### va...@chromium.org (2016-05-23)

rdevlin.cronin@: Any update on this bug? Would it be possible to get this fixed soon? Thanks!

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-05-26)

If we look at this as specific attacks, then this is fixed through a series of patches to harden our extension bindings.  However, there is still ongoing work in this area to make them even better and harder to exploit (most of that works is tracked in https://crbug.com/chromium/591164).

Security folks, do you have a preference of whether to close this issue (which no longer reproduces) as fixed, dupe it into the meta issue, or something else?

### va...@chromium.org (2016-05-26)

I'd say that if the issue reported in this bug is fixed, and the rest of the work is being tracked through https://crbug.com/chromium/591164, then it is best to mark this particular issue as fixed, which is what I am going to do.

If anyone disagrees, please feel free to re-open.

### ti...@google.com (2016-05-31)

Sending this to the panel again

### ti...@google.com (2016-06-01)

rdevlin - question from the reward panel:

#66, does that comment consider the test case at #47? Want to double check that we're not missing anything before we treat this as closed.

### va...@chromium.org (2016-06-01)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-01)

removing release label as unsure if this is actually fixed. Once we have an answer, we can mention this in the release notes.

### rd...@chromium.org (2016-06-01)

@71, yes, the exploit in #47 is also fixed.

### aw...@chromium.org (2016-07-14)

Yea! The rewards panel has awarded an additional $2,000 since there were multiple security bugs reported.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-09-13)

Putting back release label per #72

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/468931?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/490320]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081669)*
