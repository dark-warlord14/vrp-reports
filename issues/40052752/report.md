# Security: Possible to escape sandbox via devtools_page (alternative method)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052752](https://issues.chromium.org/issues/40052752) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-07-03 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

In <https://crbug.com/chromium/1059577>, a method was provided for escaping the sandbox via devtools\_page. That issue relied on the fact that embedded extensions would remain active once the devtools was opened, no matter the target page.

That issue was fixed by updating the devtools to disable extensions when navigating to a privileged page. As noted in one of the CLs for that fix, there's still a potential timing issue present. Here, a method is presented that should allow an extension to reliably run code within the target page, even after it's been navigated to a privileged location. That then allows the extension to escape the sandbox.

**VERSION**  

Chrome Version: Tested on 83.0.4103.116 (stable) and 86.0.4190.4 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached extension.
2. Open the devtools on a non-privileged page.
3. The extension will go through a series of steps (described further below) to run code within the context of a privileged page (devtools://devtools/bundled/inspector.html).
4. Wait about 25 seconds.
5. The target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 540 B)
- [chrome_inspect.js](attachments/chrome_inspect.js) (text/plain, 1.1 KB)
- [devtools.js](attachments/devtools.js) (text/plain, 3.1 KB)
- [devtools_not_connected.js](attachments/devtools_not_connected.js) (text/plain, 2.5 KB)
- [devtools_page.html](attachments/devtools_page.html) (text/plain, 132 B)
- [devtools_page.js](attachments/devtools_page.js) (text/plain, 4.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 222 B)
- [notifier.html](attachments/notifier.html) (text/plain, 127 B)
- [notifier.js](attachments/notifier.js) (text/plain, 63 B)
- [devtools_page.html](attachments/devtools_page.html) (text/plain, 132 B)
- [devtools_page.js](attachments/devtools_page.js) (text/plain, 1.5 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 165 B)

## Timeline

### de...@gmail.com (2020-07-03)

There are three essential requirements for taking advantage of the timing issue present here:

1. You need the user to open the devtools on a non-privileged page. If they've installed a devtools_page extension, they're probably going to open the devtools and if they're someone like a web developer, they're probably going to be debugging a standard web page.

2. You need to be able to reliably take advantage of the timing issue. Although one of the CLs for https://crbug.com/chromium/1059577 incorporated a test for the timing issue (and the test has since been removed due to flakiness), I think that sort of approach can be intermittent.

If you can send the devtools a message, but delay it from processing that message until after the target page has been navigated to a privileged location, you should be able to reliably sidestep the timing issue.

The method here relies on sending a crafted setSidebarContent message to the devtools. Within the devtools, _onSetSidebarContent starts with the following code:

const sidebar = this._clientObjects[message.id];

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=396;drc=4576282f49d8129b6374dd0fd389271c0a291b6a

message.id is something that's controlled by the sending extension. In this case, the extension generates the id as follows:

let idArray = new Array(100000);
let innerArray = [];
for (let i = 0;i < 250;i++) {innerArray = [innerArray];}
idArray.fill(innerArray);

This array is relatively small and quick to generate. It's then sent to the devtools via the following call:

channel.port1.postMessage({command: "setSidebarContent", id: idArray, expression: "...", rootTitle: "Title", evaluateOnPage: true});

When the devtools runs the _clientObjects lookup line of code above, the array will be implicitly converted to a string. That operation takes a non-trivial amount of time to complete (due to the nested arrays). On my machine, it's about 15 seconds. However, the string that's generated is small (about 100 KB), because none of the nested arrays contribute to the final output.

So this gives you an array that's:

- quick to generate,
- reasonably small,
- time consuming to convert to a string,
- small when represented as a string.

The target page is then navigated to a privileged location. Once the devtools is done running the single line of code above, it will continue with the rest of the _onSetSidebarContent method. Once it's finished calling the method, the navigation change event will be handled.

By doing this, the extension can ensure that the setSidebarContent message is sent to the devtools before the target page is navigated, not fully processed until after navigation has finished, but before the navigation notification is handled.

3. The final requirement has to do with how the devtools handles evaluation requests. Firstly, the evaluate method in ExtensionServer performs several URL checks:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=949;drc=4576282f49d8129b6374dd0fd389271c0a291b6a

In this case, the URL checks don't matter, because the devtools effectively runs _onSetSidebarContent before it's handled the navigation change event. That means all of the context and URL information will still be for the previous page (which the extension had access to).

To evaluate code on the target page, the devtools calls the Runtime.evaluate method and passes it the ID of the appropriate context:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/sdk/RuntimeModel.js;l=814;drc=080e864790b3c7fb5265341ed8091cbf8b3d35d7

The problem here is that if the context ID on the initial page isn't valid on the privileged page, the call will fail. The extension needs to ensure that the context ID on the original page is also valid for the privileged page.

My understanding is that the context ID gets incremented when there are multiple contexts (for a particular site) within the same process.

I believe that the context ID for the privileged page (in this case devtools://devtools/bundled/inspector.html) will always be 1, because going from a non-privileged page to a privileged page involves switching to a new process.

Ensuring that the context ID on the initial (non-privileged page) is 1 can be done by first navigating the target page from whatever page the user opened to a page that they're likely to have never opened (so that there won't be any other tabs open on that page). The page chosen here is https://example.com/, since it's unlikely that the user will have that open in another tab.

Ultimately, this should result in a situation where the context ID of the main frame on the initial page is 1 and ID of the main frame on the privileged page is also 1, which then means the call to Runtime.evaluate will succeed.

### de...@gmail.com (2020-07-03)

Putting these pieces above together, here's an overview of what happens once the extension is installed:

1. The user opens the devtools on a non-privileged page. The extension downloads the target executable and navigates the page being debugged to https://example.com/.

2. The extension creates a sidebar in the devtools by sending the createSidebarPane message.

3. The extension sends the setSidebarContent message to the devtools. The devtools starts processing this message, which will take a non-trivial amount of time.

4. The extension forwards the Alt+R keyboard shortcut to the devtools. As the devtools is busy handling the previous message, this message won't be handled immediately.

5. The extension navigates the page being debugged to devtools://devtools/bundled/inspector.html.

6. Some time later, the devtools finishes processing the setSidebarContent message. As part of that, it will run the expression that was given on the debugged page, which is now a privileged page. The expression that's run results in a console pin being added.

7. The extension will handle the Alt+R shortcut that was forwarded and reload. Although the keyboard shortcut message will always be sent before the navigation notification, I'm not sure if it's guaranteed that the devtools will handle it first. It is possible to perform the same process without reloading the devtools, though it would make the demonstration more complicated.

8. Once the devtools reloads, any embedded extensions will be disabled (since the target is a privileged page), but the console pin that was added in step 6 will run. From this point, the steps are the same as those described in https://crbug.com/chromium/1067382.

### ca...@chromium.org (2020-07-06)

caseq: Looks like this is an alternate case of what was fixed in crbug.com/1059577. Can you please take a look? Thanks.

[Monorail components: Platform>DevTools Platform>Extensions]

### me...@chromium.org (2020-07-06)

+tommycli and dpapad from https://crbug.com/chromium/1101924

### de...@gmail.com (2020-07-07)

It is also possible to take advantage of the same issue with the "Reload" method that the devtools makes available to extensions. This method allows an injected script to be run when the page is reloaded:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=467;drc=4576282f49d8129b6374dd0fd389271c0a291b6a

By generating options.injectedScript in the same sort of way as the sidebar ID, the devtools will take a non-trivial amount of time to process that specific line of code. If the target page has been navigated since the message was sent, the injected script will run on the new page (which can be privileged).

The advantage of this method over setSidebarContent is that the extension doesn't have to worry about the context IDs at all. The Reload method (which is ultimately implemented via Page.reload in the devtools protocol) always runs the injected script within the context of the main frame:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/inspector/inspector_page_agent.cc;l=903;drc=8178c4af08c01c3673549f2531953997cc74f09b

I've attached a small extension here that demonstrates that it's possible to use this method to run code within the context of a privileged page.

To test, install the extension, open the devtools on a non-privileged page, wait about 15 seconds, then check the console for the following message:

Injected script run on: devtools://devtools/bundled/inspector.html

### to...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### to...@chromium.org (2020-07-07)

Based on the explanation I'm reading in c#5, this can be used to run arbitrary JavaScript on chrome://settings.

If true, I'd recommend upgrading to at least High, depending on how easy it is to exploit.

Arbitrary JavaScript running on chrome://settings can steal the user's home address on chrome://settings/addresses. It can also steal users' saved passwords from chrome://settings/passwords.

If this is exploitable by merely installing an extension, I recommend upgrading this to a P0 / Critical.

### to...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-07)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2020-07-08)

Per chrome-security chat, https://crbug.com/chromium/1059577 could actually be high severity, so this one could be too. Code execution outside the sandbox is normally critical, but the extension install is a significant mitigation / friction, so we downgrade severity by one notch.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-17)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2020-07-28)

caseq: Friendly ping here as well?

### [Deleted User] (2020-07-31)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-01)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-10-22)

Friendly ping from the security 👮 for this High severity bug. Any updates?

For high severity vulnerabilities, we aim to deploy the patch to all Chrome
users in under 60 days.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bbf439e4e27540642b4ed172269274d2889c9cd6

commit bbf439e4e27540642b4ed172269274d2889c9cd6
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Dec 23 02:05:41 2020

DevTools: prepare tests for introduction of ExecutionContextDescription.uniqueID

This temporarily removes the newly added field from objects being dumped,
so that the test expectations do not change when upstream CL lands.

Bug: v8:11268, chromium:1101897
Change-Id: I8caa2bcf4a5b71250fb0712129771215c3a215bb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2601547
Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#839032}

[modify] https://crrev.com/bbf439e4e27540642b4ed172269274d2889c9cd6/third_party/blink/web_tests/http/tests/inspector-protocol/mixed-content-execution-contexts-1.js
[modify] https://crrev.com/bbf439e4e27540642b4ed172269274d2889c9cd6/third_party/blink/web_tests/http/tests/inspector-protocol/iframe-no-src-execution-contexts.js
[modify] https://crrev.com/bbf439e4e27540642b4ed172269274d2889c9cd6/third_party/blink/web_tests/http/tests/inspector-protocol/mixed-content-execution-contexts-2.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f656eab5928876809ef46e18de0c9d35d489e17a

commit f656eab5928876809ef46e18de0c9d35d489e17a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Dec 23 05:15:47 2020

DevTools: add support for system-unique execution context ids

This adds ExecutionContextDescription.uniqueId for a system-unique
way to identify an execution context and supports it in Runtime.evaluate.
This allows a client to avoid accidentally executing an expression
in a context different from that originally intended if a navigation
occurs while Runtime.evaluate is in flight.

Design doc: https://docs.google.com/document/d/1vGVWvKP9FTTX6kimcUJR_PAfVgDeIzXXITFpl0SyghQ

Bug: v8:11268, chromium:1101897
Change-Id: I4c6bec562ffc85312559316f639d641780144039
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2594538
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#71869}

[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-debugger.cc
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-runtime-agent-impl.h
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-inspector-impl.cc
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-inspector-impl.h
[add] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/test/inspector/runtime/evaluate-unique-context-id-expected.txt
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/test/inspector/runtime/runtime-restore-expected.txt
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/test/inspector/protocol-test.js
[add] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-debugger-id.h
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/test/inspector/sessions/create-session-expected.txt
[add] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-debugger-id.cc
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/BUILD.gn
[add] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/test/inspector/runtime/evaluate-unique-context-id.js
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/inspected-context.cc
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/inspected-context.h
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/test/inspector/runtime/create-context-expected.txt
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-debugger.h
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/include/js_protocol.pdl
[modify] https://crrev.com/f656eab5928876809ef46e18de0c9d35d489e17a/src/inspector/v8-runtime-agent-impl.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/b961d44fa6990b049d82caeac1dc59c1d4be0848

commit b961d44fa6990b049d82caeac1dc59c1d4be0848
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Dec 24 05:30:57 2020

Roll js_protocol.pdl to include ExecutionContextDescription.uniqueId

Drive-by: roll inspector_protocol to fix pdl.py problem

DISABLE_THIRD_PARTY_CHECK=protocol update

Bug: v8:11268, chromium:1101897
Change-Id: I8c0be131e521d996fb718ee381fe67f14dfe737d
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2602555
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>

[modify] https://crrev.com/b961d44fa6990b049d82caeac1dc59c1d4be0848/front_end/generated/InspectorBackendCommands.js
[modify] https://crrev.com/b961d44fa6990b049d82caeac1dc59c1d4be0848/v8/include/js_protocol.pdl
[modify] https://crrev.com/b961d44fa6990b049d82caeac1dc59c1d4be0848/front_end/generated/protocol.d.ts
[modify] https://crrev.com/b961d44fa6990b049d82caeac1dc59c1d4be0848/third_party/blink/public/devtools_protocol/browser_protocol.json


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/58d64f52a1303ce60ef0e4abe17d0f36c67ebe4a

commit 58d64f52a1303ce60ef0e4abe17d0f36c67ebe4a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Dec 24 05:57:47 2020

Use ExecutionContext.uniqueId when evaluating on the global object

Design doc: https://docs.google.com/document/d/1vGVWvKP9FTTX6kimcUJR_PAfVgDeIzXXITFpl0SyghQ
Related test: https://chromium-review.googlesource.com/c/chromium/src/+/2602709

Bug: v8:11268, chromium:1101897
Change-Id: I35f8efba4d50ac8bd98e0fce995baf24dda55365
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2602710
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Auto-Submit: Andrey Kosyakov <caseq@chromium.org>

[modify] https://crrev.com/58d64f52a1303ce60ef0e4abe17d0f36c67ebe4a/front_end/sdk/RuntimeModel.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8afc6a72b00f9198409c4ed6ba9df82daab1fb8b

commit 8afc6a72b00f9198409c4ed6ba9df82daab1fb8b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 24 15:54:48 2020

Roll DevTools Frontend from b4a82aa3575f to b961d44fa699 (1 revision)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/b4a82aa3575f..b961d44fa699

2020-12-24 caseq@chromium.org Roll js_protocol.pdl to include ExecutionContextDescription.uniqueId

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1101897
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: Iab489f884fa4ae20dd0c6ceb25c40b00bae25f2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602835
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#839264}

[modify] https://crrev.com/8afc6a72b00f9198409c4ed6ba9df82daab1fb8b/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbe5f1ae8e69bdfb1be09c65a81db0755e63c356

commit cbe5f1ae8e69bdfb1be09c65a81db0755e63c356
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 24 17:09:59 2020

Roll DevTools Frontend from b961d44fa699 to fafa67016f36 (19 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/b961d44fa699..fafa67016f36

2020-12-24 changhaohan@chromium.org Change cursor to pointer when hovering over color swatches
2020-12-24 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools DEPS.
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ElementsSidebarPane.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ComputedStyleWidget.js
2020-12-24 mathias@chromium.org Use AVIF for “what’s new” image
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ComputedStyleModel.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ARIAAttributesView.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ConsolePinPane.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ImagePreview.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in DebuggerWorkspaceBinding.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in TempFile.js
2020-12-24 mathias@chromium.org Support AVIF in component server
2020-12-24 mathias@chromium.org Support AVIF in hosted mode
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ClassesPaneWidget.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in WarningErrorCounter.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ConsoleView.js
2020-12-24 mathias@chromium.org Clean up redundant Promise.resolve() in ContentProviderBasedProject.js
2020-12-24 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools Chromium DEPS.
2020-12-24 caseq@chromium.org Use ExecutionContext.uniqueId when evaluating on the global object

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1101897,chromium:1156835,chromium:1161501,chromium:1161661,chromium:1161667
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: Idfcb7cc3c70e50c62eab2aecce3dc2a2f5c0066a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2603119
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#839268}

[modify] https://crrev.com/cbe5f1ae8e69bdfb1be09c65a81db0755e63c356/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0e3033a6cb7e0283cab92b52f91642eb3cefc888

commit 0e3033a6cb7e0283cab92b52f91642eb3cefc888
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Sat Dec 26 23:54:37 2020

DevTools: add a test for chrome.devtools.inspectedWindow.eval using correct execution context

See also: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2602710

Bug: v8:11268, chromium:1101897
Change-Id: If57b53a910afe8945453f35689b63168c076db7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602709
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#839375}

[modify] https://crrev.com/0e3033a6cb7e0283cab92b52f91642eb3cefc888/third_party/blink/web_tests/http/tests/devtools/resources/extension-main.js
[add] https://crrev.com/0e3033a6cb7e0283cab92b52f91642eb3cefc888/third_party/blink/web_tests/http/tests/devtools/extensions/extensions-eval-execution-context-expected.txt
[add] https://crrev.com/0e3033a6cb7e0283cab92b52f91642eb3cefc888/third_party/blink/web_tests/http/tests/devtools/extensions/extensions-eval-execution-context.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b4db63fc67e6e6b2bf7e36b90dc86b7adf312c50

commit b4db63fc67e6e6b2bf7e36b90dc86b7adf312c50
Author: Sergey Poromov <poromov@chromium.org>
Date: Mon Dec 28 14:41:20 2020

Revert "DevTools: add a test for chrome.devtools.inspectedWindow.eval using correct execution context"

This reverts commit 0e3033a6cb7e0283cab92b52f91642eb3cefc888.

Reason for revert:
Consistently failing on Linux MSAN builds:
https://ci.chromium.org/p/chromium/builders/ci/WebKit%20Linux%20MSAN
First failure: https://ci.chromium.org/ui/p/chromium/builders/ci/WebKit%20Linux%20MSAN/8844/blamelist

Original change's description:
> DevTools: add a test for chrome.devtools.inspectedWindow.eval using correct execution context
>
> See also: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2602710
>
> Bug: v8:11268, chromium:1101897
> Change-Id: If57b53a910afe8945453f35689b63168c076db7c
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602709
> Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
> Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#839375}

TBR=caseq@chromium.org,bmeurer@chromium.org,chromium-scoped@luci-project-accounts.iam.gserviceaccount.com,pfaffe@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: v8:11268
Bug: chromium:1101897
Change-Id: Ie7aaebbd32400ffa5303774840eb7650c0cc1f4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602428
Reviewed-by: Sergey Poromov <poromov@chromium.org>
Commit-Queue: Sergey Poromov <poromov@chromium.org>
Cr-Commit-Position: refs/heads/master@{#839449}

[modify] https://crrev.com/b4db63fc67e6e6b2bf7e36b90dc86b7adf312c50/third_party/blink/web_tests/http/tests/devtools/resources/extension-main.js
[delete] https://crrev.com/79b51121c1d96457223e9fb1ab0b1ea253fbe688/third_party/blink/web_tests/http/tests/devtools/extensions/extensions-eval-execution-context-expected.txt
[delete] https://crrev.com/79b51121c1d96457223e9fb1ab0b1ea253fbe688/third_party/blink/web_tests/http/tests/devtools/extensions/extensions-eval-execution-context.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a042444563df9738971aeeb0cd067d89345cbce8

commit a042444563df9738971aeeb0cd067d89345cbce8
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Dec 29 01:18:52 2020

Reland "DevTools: add a test for chrome.devtools.inspectedWindow.eval using correct execution context"

This reverts commit b4db63fc67e6e6b2bf7e36b90dc86b7adf312c50.

Reason for revert: re-land the test along with a fix.

Original change's description:
> Revert "DevTools: add a test for chrome.devtools.inspectedWindow.eval using correct execution context"
>
> This reverts commit 0e3033a6cb7e0283cab92b52f91642eb3cefc888.
>
> Reason for revert:
> Consistently failing on Linux MSAN builds:
> https://ci.chromium.org/p/chromium/builders/ci/WebKit%20Linux%20MSAN
> First failure: https://ci.chromium.org/ui/p/chromium/builders/ci/WebKit%20Linux%20MSAN/8844/blamelist
>
> Original change's description:
> > DevTools: add a test for chrome.devtools.inspectedWindow.eval using correct execution context
> >
> > See also: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2602710
> >
> > Bug: v8:11268, chromium:1101897
> > Change-Id: If57b53a910afe8945453f35689b63168c076db7c
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602709
> > Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
> > Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#839375}
>
> TBR=caseq@chromium.org,bmeurer@chromium.org,chromium-scoped@luci-project-accounts.iam.gserviceaccount.com,pfaffe@chromium.org
>
> # Not skipping CQ checks because original CL landed > 1 day ago.
>
> Bug: v8:11268
> Bug: chromium:1101897
> Change-Id: Ie7aaebbd32400ffa5303774840eb7650c0cc1f4f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2602428
> Reviewed-by: Sergey Poromov <poromov@chromium.org>
> Commit-Queue: Sergey Poromov <poromov@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#839449}

TBR=caseq@chromium.org,poromov@chromium.org,bmeurer@chromium.org,chromium-scoped@luci-project-accounts.iam.gserviceaccount.com,pfaffe@chromium.org

# Not skipping CQ checks because this is a reland.

Bug: v8:11268
Bug: chromium:1101897
Change-Id: Ibcb4e38986ca13bc89b334bb90ea0d6704c5c86a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2605411
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#839521}

[modify] https://crrev.com/a042444563df9738971aeeb0cd067d89345cbce8/third_party/blink/web_tests/http/tests/devtools/resources/extension-main.js
[add] https://crrev.com/a042444563df9738971aeeb0cd067d89345cbce8/third_party/blink/web_tests/http/tests/devtools/extensions/extensions-eval-execution-context-expected.txt
[add] https://crrev.com/a042444563df9738971aeeb0cd067d89345cbce8/third_party/blink/web_tests/http/tests/devtools/extensions/extensions-eval-execution-context.js


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

### ad...@google.com (2021-04-08)

caseq@ is this now fixed? I've belatedly noticed that the commit description in https://crbug.com/chromium/1101897#c31 suggests so.

### bm...@chromium.org (2021-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/b7e80e33dc247c4bc1d0bef976954c4a70145982

commit b7e80e33dc247c4bc1d0bef976954c4a70145982
Author: Benedikt Meurer <bmeurer@chromium.org>
Date: Wed Apr 21 04:57:27 2021

[sdk] Support old backends that don't understand uniqueContextId.

With https://crrev.com/c/2602710 we broke support for Runtime.evaluate()
with different contexts for back-ends that don't yet support
uniqueContextId. This change restores support by using uniqueContextId
only when it was send by the back-end and otherwise using contextId as
before.

Fixed: chromium:1192621
Bug: v8:11268, chromium:1101897
Change-Id: I37909443eaea6fb4d92a1c258383a4753639c8b9
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2815125
Commit-Queue: Benedikt Meurer <bmeurer@chromium.org>
Auto-Submit: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>

[modify] https://crrev.com/b7e80e33dc247c4bc1d0bef976954c4a70145982/front_end/core/sdk/RuntimeModel.ts


### gi...@appspot.gserviceaccount.com (2021-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5d3026bc75b1f3d681e6d64cc57e38858ab7a400

commit 5d3026bc75b1f3d681e6d64cc57e38858ab7a400
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Apr 21 08:15:43 2021

Roll DevTools Frontend from c8dcfdebd148 to b7e80e33dc24 (1 revision)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/c8dcfdebd148..b7e80e33dc24

2021-04-21 bmeurer@chromium.org [sdk] Support old backends that don't understand uniqueContextId.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1101897
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I569d522cd9d0d0804038507023fde045e7463121
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2843269
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#874613}

[modify] https://crrev.com/5d3026bc75b1f3d681e6d64cc57e38858ab7a400/DEPS


### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-20)

Hi, caseq@ and bmeurer@, can this be marked as fixed or are additional fixes needed due to the revert above? 

### am...@google.com (2021-07-20)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-07-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-24)

Requesting merge to extended stable M91 because latest trunk commit (874613) appears to be after extended stable branch point (870763).

Not requesting merge to stable (M92) because latest trunk commit (874613) appears to be prior to stable branch point (885287). If this is incorrect, please replace the Merge-na label with Merge-Request-92. If other changes are required to fix this bug completely, please request a merge if necessary.

Not requesting merge to dev (M93) because latest trunk commit (874613) appears to be prior to dev branch point (902210). If this is incorrect, please replace the Merge-na label with Merge-Request-93. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-07-26)

[Comment Deleted]

### am...@google.com (2021-07-26)

Please ensure the changes from this rollback are included/merged in M91 as it is now the extended stable release branch as we move toward the 4W release cycle. Thanks! 

### ca...@chromium.org (2021-07-26)

FWIW, this is not a rollback.

Please note https://crbug.com/chromium/1101897#c52 refers to the commit that was fixing a regression resulting from the original fix of this issue, which is tracked separately by https://crbug.com/chromium/1192621 -- let's rather track the merge there. The last commit related to the original fix for this issue is landed in m89 (https://storage.googleapis.com/chromium-find-releases-static/a04.html#a042444563df9738971aeeb0cd067d89345cbce8)

Benedikt, does it look like something that we'd like to merge to m91 extended stable? My take is that considering we did not do any merges originally and that this is not a security issue, we don't have to.




### ad...@google.com (2021-07-27)

I agree; removing merge request.

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Hi, David! The VRP Panel has decided to award you $5000 for this report. Also, thank you for your patience as this one ducked some of our automation and was only recently noticed to be left open long after it was fixed. Our apologies for that and thank you for another great report. 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### vo...@google.com (2021-08-03)

Marking as not applicable for lts. The security issue was fixed in m89, so we don't need to merge anything to m90.

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1101897?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/1101924]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052752)*
