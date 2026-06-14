# An https iframe in an http page can use service worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40084193](https://issues.chromium.org/issues/40084193) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker |
| **Reporter** | fa...@chromium.org |
| **Assignee** | fa...@chromium.org |
| **Created** | 2016-04-28 |
| **Bounty** | $1,000.00 |

## Description

From private correspondence with Ben Kelly:

"A user recently reported that they are able to do the following:
1) We set up a secure domain test.com, and installed a service worker on it.
2) We set up an insecure page on http://test-insecure.com that opened an iframe to https://test.com - let's call that the "secure iframe". We found that while a script in the secure iframe could also not access getRegistration, any fetches it makes are intercepted by the service worker on test.com. That gives us a way to talk to an existing service worker from an insecure page."

The user reported this applies to Chrome as well as Firefox.

## Timeline

### be...@salesforce.com (2016-04-28)

(I'm the user who reported this).
For clarity - the secure iframe within the insecure page doesn't have access to `getRegistration()` (returns `undefined` in FF, rejects on Chrome) and can't register, unregister, etc. All that happens here is that fetch events within the scope of a *already registered worker* are intercepted. Emphasis intentional: in order for this to work, a service worker must already be registered for the secure domain serving the iframe source.

### rs...@chromium.org (2016-04-28)

Tentatively labeling as Medium-severity because of the requirement of a SW already being registered.

### sh...@chromium.org (2016-05-13)

falken: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-05-24)

Since this was filed as a security bug, adding Restrict-View-SecurityTeam for now.

falken: It's the security team's Fixit this week, and we're trying to get as many bugs as possible closed out. Would you mind providing a status update on this?

### fa...@chromium.org (2016-05-24)

Patch up for review: https://codereview.chromium.org/2009453002/

### fa...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-05-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### fa...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d

commit 59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d
Author: falken <falken@chromium.org>
Date: Tue Jun 07 05:06:12 2016

service worker: Don't control a subframe of an insecure context

We must check isSecureContext when creating the network provider to
adhere to https://w3c.github.io/webappsec/specs/powerfulfeatures/#settings-privileged.

We already did this for getRegistration(), register(), unregister() but must
also do this when deciding whether to control an in-scope document.

BUG=607543
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2009453002
Cr-Commit-Position: refs/heads/master@{#398229}

[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_browsertest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_context_core.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_context_request_handler_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_context_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_controllee_request_handler.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_controllee_request_handler_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_dispatcher_host.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_dispatcher_host.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_dispatcher_host_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_handle_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_job_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_provider_host.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_provider_host.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_provider_host_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_request_handler_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_storage_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_url_request_job_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_version_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/browser/service_worker/service_worker_write_to_cache_job_unittest.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/child/service_worker/service_worker_network_provider.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/child/service_worker/service_worker_network_provider.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/common/service_worker/service_worker_messages.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/public/browser/content_browser_client.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/renderer/service_worker/service_worker_context_client.cc
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/content/renderer/shared_worker/embedded_shared_worker_stub.cc
[add] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/LayoutTests/http/tests/serviceworker/insecure-parent-frame.html
[add] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-inscope.html
[add] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-parent.html
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/Source/core/dom/Document.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/Source/core/frame/Frame.cpp
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/Source/web/WebFrame.cpp
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/Source/web/tests/WebFrameTest.cpp
[modify] https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d/third_party/WebKit/public/web/WebFrame.h


### fa...@chromium.org (2016-06-07)

Fixed with #10. Simple test case: https://mattto.github.io/sw/test/insecure-parent-frame/

Security team: Does the severity warrant a merge to M51 and M52? It's a pretty disruptive change in that many files are touched.

### ti...@google.com (2016-06-07)

Let's get this into M52 after it survives a canary and dev build.

Adding reward-topanel based on #1 for consideration under our reward program - full details here: https://www.google.com/about/appsecurity/chrome-rewards/

### cl...@chromium.org (2016-06-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c363d41a6001cb7b27789484702d23fa4572a918

commit c363d41a6001cb7b27789484702d23fa4572a918
Author: dcheng <dcheng@chromium.org>
Date: Wed Jun 08 20:29:39 2016

Revert of service worker: Don't control a subframe of an insecure context (patchset #21 id:440001 of https://codereview.chromium.org/2009453002/ )

Reason for revert:
ServiceWorkerProviderHost::SetControllerVersionAttribute CHECK is firing in release builds: https://crbug.com/618365

Original issue's description:
> service worker: Don't control a subframe of an insecure context
>
> We must check isSecureContext when creating the network provider to
> adhere to https://w3c.github.io/webappsec/specs/powerfulfeatures/#settings-privileged.
>
> We already did this for getRegistration(), register(), unregister() but must
> also do this when deciding whether to control an in-scope document.
>
> BUG=607543
> CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation
>
> Committed: https://crrev.com/59a2e54eeb0e61971a0c27c44c54dd0c30b5d06d
> Cr-Commit-Position: refs/heads/master@{#398229}

TBR=alexmos@chromium.org,clamy@chromium.org,horo@chromium.org,jww@chromium.org,kinuko@chromium.org,lazyboy@chromium.org,rdevlin.cronin@chromium.org,falken@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=607543

Review-Url: https://codereview.chromium.org/2055433002
Cr-Commit-Position: refs/heads/master@{#398660}

[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_browsertest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_context_core.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_context_request_handler_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_context_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_controllee_request_handler.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_controllee_request_handler_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_dispatcher_host.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_dispatcher_host.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_dispatcher_host_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_handle_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_job_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_provider_host.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_provider_host.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_provider_host_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_request_handler_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_storage_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_url_request_job_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_version_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/browser/service_worker/service_worker_write_to_cache_job_unittest.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/child/service_worker/service_worker_network_provider.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/child/service_worker/service_worker_network_provider.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/common/service_worker/service_worker_messages.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/public/browser/content_browser_client.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/renderer/service_worker/service_worker_context_client.cc
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/content/renderer/shared_worker/embedded_shared_worker_stub.cc
[delete] https://crrev.com/ea1675fb67d48828efb8c6b168582aa9f33388a2/third_party/WebKit/LayoutTests/http/tests/serviceworker/insecure-parent-frame.html
[delete] https://crrev.com/ea1675fb67d48828efb8c6b168582aa9f33388a2/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-inscope.html
[delete] https://crrev.com/ea1675fb67d48828efb8c6b168582aa9f33388a2/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-parent.html
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/Source/core/dom/Document.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/Source/core/frame/Frame.cpp
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/Source/web/WebFrame.cpp
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/Source/web/tests/WebFrameTest.cpp
[modify] https://crrev.com/c363d41a6001cb7b27789484702d23fa4572a918/third_party/WebKit/public/web/WebFrame.h


### fa...@chromium.org (2016-06-14)

The fix was reverted.

### cl...@chromium.org (2016-06-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### ho...@chromium.org (2016-06-15)

This bug is not fixed yet.
The fix patch was reverted.

### cl...@chromium.org (2016-06-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### aw...@chromium.org (2016-06-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ad1850962644e19cdb040d60eb236e0ebc23c243

commit ad1850962644e19cdb040d60eb236e0ebc23c243
Author: falken <falken@chromium.org>
Date: Thu Jun 16 06:10:02 2016

Reland: service worker: Don't control a subframe of an insecure context

We must check isSecureContext when creating the network provider to
adhere to https://w3c.github.io/webappsec/specs/powerfulfeatures/#settings-privileged.

We already did this for getRegistration(), register(), unregister() but must
also do this when deciding whether to control an in-scope document.

BUG=607543
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation
TBR=reviewers from the original review

Original review: https://codereview.chromium.org/2009453002

Review-Url: https://codereview.chromium.org/2071433003
Cr-Commit-Position: refs/heads/master@{#400093}

[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_browsertest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_context_core.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_context_request_handler_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_context_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_controllee_request_handler.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_controllee_request_handler_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_dispatcher_host.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_dispatcher_host.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_dispatcher_host_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_handle_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_job_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_provider_host.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_provider_host.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_provider_host_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_registration.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_request_handler_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_storage_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_url_request_job_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_version_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/browser/service_worker/service_worker_write_to_cache_job_unittest.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/child/service_worker/service_worker_network_provider.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/child/service_worker/service_worker_network_provider.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/common/service_worker/service_worker_messages.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/public/browser/content_browser_client.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/renderer/service_worker/service_worker_context_client.cc
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/content/renderer/shared_worker/embedded_shared_worker_stub.cc
[add] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/LayoutTests/http/tests/serviceworker/insecure-parent-frame.html
[add] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-inscope.html
[add] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-parent.html
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/Source/core/dom/Document.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/Source/core/frame/Frame.cpp
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/Source/web/WebFrame.cpp
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/Source/web/tests/WebFrameTest.cpp
[modify] https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243/third_party/WebKit/public/web/WebFrame.h


### fa...@chromium.org (2016-06-16)

[Empty comment from Monorail migration]

### fa...@chromium.org (2016-06-20)

Canary looks good. Waiting for it to cycle through Dev.

### fa...@chromium.org (2016-06-21)

DCHECK is failing on Dev.

### bu...@chromium.org (2016-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8353baf8d1504dbdd4ad7584ff2466de657521cd

commit 8353baf8d1504dbdd4ad7584ff2466de657521cd
Author: falken <falken@chromium.org>
Date: Tue Jun 21 04:49:54 2016

Remove WebFrame::canHaveSecureChild

To simplify the public API, ServiceWorkerNetworkProvider can do the
parent walk itself.

Follow-up to https://crrev.com/ad1850962644e19.

BUG=607543

Review-Url: https://codereview.chromium.org/2082493002
Cr-Commit-Position: refs/heads/master@{#400896}

[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/content/child/service_worker/service_worker_network_provider.cc
[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/third_party/WebKit/Source/core/frame/Frame.cpp
[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/third_party/WebKit/Source/core/frame/Frame.h
[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/third_party/WebKit/Source/web/WebFrame.cpp
[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/third_party/WebKit/Source/web/tests/WebFrameTest.cpp
[modify] https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd/third_party/WebKit/public/web/WebFrame.h


### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd5dd98f5f59f4f53274308ec0a7dca74aba6525

commit dd5dd98f5f59f4f53274308ec0a7dca74aba6525
Author: falken <falken@chromium.org>
Date: Wed Jun 22 06:32:52 2016

service worker: When claiming, don't assume document_url is valid

Many provider hosts have an empty document_url, for example those
that haven't yet been loaded or those created for special URLs like
chrome-search://. So that claim can use IsContextSecureForServiceWorker,
return false when the URL is invalid instead of doing a
DCHECK that it's valid.

BUG=621762,607543

Review-Url: https://codereview.chromium.org/2085923002
Cr-Commit-Position: refs/heads/master@{#401216}

[modify] https://crrev.com/dd5dd98f5f59f4f53274308ec0a7dca74aba6525/content/browser/service_worker/service_worker_provider_host.cc


### fa...@chromium.org (2016-07-01)

This has cycled through a dev release and looks fine.

Request merge to M52 of:
https://crrev.com/ad1850962644e19cdb040d60eb236e0ebc23c243
https://crrev.com/8353baf8d1504dbdd4ad7584ff2466de657521cd
https://crrev.com/dd5dd98f5f59f4f53274308ec0a7dca74aba6525

### aw...@chromium.org (2016-07-06)

Congratulations, $1,000 for this report!

### fa...@chromium.org (2016-07-07)

Ping. The Merge-Request-52 label is still unresolved. (And strangely, it doesn't appear in the Labels section below).

### di...@chromium.org (2016-07-11)

tinazh@ is OOO, approving merge to M52.

### bu...@chromium.org (2016-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/894ba96d4f84f8cdbd13168bf14cb866ce8caecd

commit 894ba96d4f84f8cdbd13168bf14cb866ce8caecd
Author: Matt Falkenhagen <falken@chromium.org>
Date: Tue Jul 12 02:20:46 2016

M52: Merge  "Reland: service worker: Don't control a subframe of an insecure context"

This merge includes:

[1]
service worker: When claiming, don't assume document_url is valid

Many provider hosts have an empty document_url, for example those
that haven't yet been loaded or those created for special URLs like
chrome-search://. So that claim can use IsContextSecureForServiceWorker,
return false when the URL is invalid instead of doing a
DCHECK that it's valid.

BUG=621762,607543

Review-Url: https://codereview.chromium.org/2085923002
Cr-Commit-Position: refs/heads/master@{#401216}
(cherry picked from commit dd5dd98f5f59f4f53274308ec0a7dca74aba6525)

[2]
Remove WebFrame::canHaveSecureChild

To simplify the public API, ServiceWorkerNetworkProvider can do the
parent walk itself.

Follow-up to https://crrev.com/ad1850962644e19.

BUG=607543

Review-Url: https://codereview.chromium.org/2082493002
Cr-Commit-Position: refs/heads/master@{#400896}
(cherry picked from commit 8353baf8d1504dbdd4ad7584ff2466de657521cd)

[3]
Reland: service worker: Don't control a subframe of an insecure context

We must check isSecureContext when creating the network provider to
adhere to https://w3c.github.io/webappsec/specs/powerfulfeatures/#settings-privileged.

We already did this for getRegistration(), register(), unregister() but must
also do this when deciding whether to control an in-scope document.

BUG=607543
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Original review: https://codereview.chromium.org/2009453002

Review-Url: https://codereview.chromium.org/2071433003
Cr-Commit-Position: refs/heads/master@{#400093}
(cherry picked from commit ad1850962644e19cdb040d60eb236e0ebc23c243)

[4]
service worker: Remove unused PROVIDER_FOR_SANDBOXED_IFRAME

Clean-up only. This was added in https://codereview.chromium.org/1191293002/
then became unused in https://codereview.chromium.org/1399363004. Originally it
signaled to the ServiceWorkerNetworkProvider ctor that the provider id should
be set to invalid; now the default ctor is used accomplish that.

BUG=

Review-Url: https://codereview.chromium.org/2023733002
Cr-Commit-Position: refs/heads/master@{#396685}
(cherry picked from commit ae9107fb035320cc53558a0bb1ff5c9bf99cfffe)

TBR=horo

Review URL: https://codereview.chromium.org/2142523004 .

Cr-Commit-Position: refs/branch-heads/2743@{#614}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_browsertest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_context_core.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_context_request_handler_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_context_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_controllee_request_handler.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_controllee_request_handler_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_dispatcher_host.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_dispatcher_host.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_dispatcher_host_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_handle_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_job_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_provider_host.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_provider_host.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_provider_host_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_registration.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_request_handler_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_storage_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_url_request_job_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_version_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/browser/service_worker/service_worker_write_to_cache_job_unittest.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/child/service_worker/service_worker_network_provider.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/child/service_worker/service_worker_network_provider.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/common/service_worker/service_worker_messages.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/common/service_worker/service_worker_types.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/public/browser/content_browser_client.h
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/renderer/service_worker/service_worker_context_client.cc
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/content/renderer/shared_worker/embedded_shared_worker_stub.cc
[add] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/third_party/WebKit/LayoutTests/http/tests/serviceworker/insecure-parent-frame.html
[add] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-inscope.html
[add] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/third_party/WebKit/LayoutTests/http/tests/serviceworker/resources/insecure-parent.html
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/894ba96d4f84f8cdbd13168bf14cb866ce8caecd/third_party/WebKit/Source/core/dom/Document.h


### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### fa...@chromium.org (2016-07-21)

This should be fixed in 52.0.2743.75, 53.0.2770.0, and above.


### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/607543?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/621762]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084193)*
