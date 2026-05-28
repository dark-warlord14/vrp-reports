# Sandbox escape from extensions due to insufficent checks in chrome.devtools.inspectedWindow.reload and chrome://policy

| Field | Value |
|-------|-------|
| **Issue ID** | [338248595](https://issues.chromium.org/issues/338248595) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | yd...@google.com |
| **Created** | 2024-05-01 |
| **Bounty** | $20,000.00 |

## Description

## VULNERABILITY DETAILS

1. A race condition in the devtools API server and `chrome.devtools.inspectedWindow.reload`, along with insufficient permissions checks, allows an extension with the `devtools_page` permission to run arbitrary JS on any privileged page.
2. This is used to run JS on `chrome://policy`, which executes `cr.sendWithPromise("setLocalTestPolicies", policy, "");`. It is never checked if local test policies are actually allowed, so this applies arbitrary user policies to the browser.
3. The `BrowserSwitcherEnabled`, `BrowserSwitcherUrlList`, `AlternativeBrowserPath`, and `AlternativeBrowserParameters` policies are set. This sets `/bin/bash` (or cmd.exe) as the "alternative browser."
4. The extension navigates to `example.com`, which triggers the browser switcher, causing it to execute the commands specified by the policy.

## EXPLANATION

### Devtools API Permissions Bypass

As far as I can tell, the `chrome.devtools.inspectedWindow.reload` function has [no checks](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=812-826) to see if the extension is actually allowed to execute scripts on the inspected page. The only thing preventing this from being used normally is having the devtools extension server [block access](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=456-459) once the URL of the inspected page changes.

We can verify this by opening `chrome://settings/resetProfileSettings`, clicking on the "current settings" link (which opens an about:blank window with the `chrome://settings` origin), and opening devtools on that page. If our extension calls `chrome.devtools.inspectedWindow.reload`, then code will run on the privileged `about:blank` page.

Unfortunately, since [only the URL is checked](https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=1367-1405;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e) rather than the page's origin, so there is a small window of time after a navigation occurs where the origin is set to the new page but the URL is unchanged. If `chrome.devtools.inspectedWindow.reload` is called during this period, then it will execute arbitrary JS on the page that is being navigated to.

This window of time can be fairly reliably hit by spamming `chrome.devtools.inspectedWindow.reload` calls, then using `chrome.tabs.update(chrome.devtools.inspectedWindow.tabId, {url: "chrome://policy"});` to perform the navigation. Now we can run arbitrary JS on any `chrome://` page, bypassing any permissions checks.

### Sandbox Escape With `chrome://policy`

The `chrome://policy` page has a feature which allows a user to set local policies for testing. This is disabled by default, but the webui message listener [is added no matter what](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/policy/policy_ui_handler.cc;l=207-210?q=setLocalTestPolicies&ss=chromium%2Fchromium%2Fsrc).

Thus once we have code execution on `chrome://policy`, we can run `cr.sendWithPromise("setLocalTestPolicies", policy, "");`, and this will cause the test policies to be enabled. The `policy` variable is a JSON string containing a list of user policies that will be applied. These policies will be [immediately applied](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/policy/policy_ui_handler.cc;l=316-343;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e?q=setLocalTestPolicies&ss=chromium%2Fchromium%2Fsrc) to the running browser.

There is supposed to be two options which have to be explicitly enabled to prevent this, however [both checks fail](https://source.chromium.org/chromium/chromium/src/+/main:components/policy/core/common/policy_utils.cc;l=14-49;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e). The feature flag `policy::features::kEnablePolicyTestPage` defaults to false, and this is supposed to be checked, but for some reason this check always fails. The policy `policy_prefs::kPolicyTestPageEnabled` is also checked, however, it requires the `pref_service` argument to be passed into the `IsPolicyTestingEnabled` function. For some reason, the `pref_service` argument is [set to a `nullptr`](https://source.chromium.org/chromium/chromium/src/+/main:components/policy/core/common/local_test_policy_provider.cc;l=23;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e;bpv=1;bpt=1) when this function is run, negating this check.

Therefore, because the two previous checks both fail, only the release channel is taken into consideration when the browser decides whether or not to allow local test policies. Release channels `Channel::CANARY` and `Channel::DEFAULT` are always allowed (and `Channel::DEV` works on Linux). The release channel is always `Channel::DEFAULT` for builds that are not branded as Google Chrome, so test policies are always allowed on Chromium and its derivatives (or Google Chrome Canary/Dev).

Now that we have the ability to set any user policy we want, the following policies are set:

```
name: "BrowserSwitcherEnabled"
value: true

name: "BrowserSwitcherUrlList"
value: ["example.com"]

name: "AlternativeBrowserPath"
value: "/bin/bash"

name: "AlternativeBrowserParameters"
value: ["-c", "xcalc # ${url}"] 

```

The alternate browser switcher is enabled, and `example.com` is set to trigger it. The `AlternativeBrowserPath` policy is set to Bash, and the arguments provided specify which command to run. `# ${url}` is included so that the page URL is substituted in as a comment rather than its own argument.

Now all that's required is for the browser to navigate to `example.com`, which will cause Chrome to run `/bin/bash -c 'xcalc # https://example.com'`.

For reasons mentioned above, using `chrome://policy` will not work on official Google Chrome builds in the stable channel. However, `chrome://downloads` can be used to perform the sandbox escape instead, though this requires an extra user gesture. An POC for this alternative method is attached as `devtools_downloads.js`.

Although a full sandbox escape is not possible on Chrome OS, the devtools API permissions bypass will still work, so considerable damage can still be done. It may be possible for arbitrary code to be run on `chrome://settings` (which can steal passwords) or `chrome://file-manager` which can possibly inject something into the Crostini's bashrc.

## VERSION

I tested this to work on Chromium in Linux, Windows, and MacOS.

```
Chrome Version: 124.0.6367.78 (Official Build) 64-bit) 
Operating System: Linux (Debian 12) 
Chrome Version: 126.0.6453.0 (Developer Build) (64-bit) 
Operating System: Windows 10 22H2
Chrome Version: 126.0.6452.0 (Developer Build) (x86_64)
Operating System: MacOS 11.7.10

```
## REPRODUCTION CASE

1. Open Chromium on Windows, Linux, or MacOS.
2. Download the files attached to this report, and place them in the same folder.
3. Load the attached files as a Chrome extension.
4. Open devtools on `about:blank` or any other unprivileged page.

Videos are attached which demonstrate this.

## CREDIT INFORMATION

Reporter credit: Allen Ding

## Attachments

- [sandbox_escape_windows.mp4](attachments/sandbox_escape_windows.mp4) (video/mp4, 523.7 KB)
- [sandbox_escape_linux.mp4](attachments/sandbox_escape_linux.mp4) (video/mp4, 731.5 KB)
- [devtools.html](attachments/devtools.html) (text/html, 73 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 3.4 KB)
- [index.html](attachments/index.html) (text/html, 191 B)
- [manifest.json](attachments/manifest.json) (application/json, 248 B)
- [worker.js](attachments/worker.js) (text/javascript, 149 B)
- [devtools_downloads.js](attachments/devtools_downloads.js) (text/javascript, 1.9 KB)
- [devtools.js](attachments/devtools.js) (text/javascript, 3.2 KB)
- [sandbox_escape_linux_v2.mp4](attachments/sandbox_escape_linux_v2.mp4) (video/mp4, 546.5 KB)

## Timeline

### ch...@chromium.org (2024-05-04)

Thanks for the detailed report.

I tried your POC a bunch of times on Linux at ToT and could not get it to work reliably. It got as far as navigating to chrome://policy, but I did not see it load the test policies. I got a lot of `"Extension server error: Operation failed: Permission denied"` messages. It seems the inject\_script() race condition may not be reliable. I also tried increasing the number of loop iterations in start\_interval(). I also tried it on 124.0.6367.78, the version you indicated.

However, I also tried it with your chrome://downloads variant, and I got that to work, apparently, a single time (!). (I tested on Linux, so I made it download and open a random jpg instead of the exe, but if it were an executable it would also have that user gesture so it would run.)

Is there anything you found to make the repro more reliable? Setting High severity, since it does look like it works, but with mitigating factors.

Assigning to caseq: could you please take a look? (Also cc'ing pfaffe, who's OOO.) It looks a little similar to [crbug.com/40052752](https://crbug.com/40052752).

About the chrome://policy parts:

- It seems like we might create and initialize the thing unconditionally (based only on the channel) [here](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/policy/chrome_browser_policy_connector.cc;l=342;drc=0586a538d8b452fe3da212737140878ed16eed49) (very early in browser startup, so the FeatureList check doesn't work properly) which then gets [retrieved](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/policy/policy_ui_handler.cc;l=323;drc=0586a538d8b452fe3da212737140878ed16eed49), without checking the feature/pref [to load the UI page](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/policy/policy_ui.cc;l=256-259;drc=0586a538d8b452fe3da212737140878ed16eed49), because we are triggering setLocalTestPolicies directly and not through the UI. (cc'ing ydago)
- (cc'ing nicolaso) FYI, this is based on the LBS policies, similar to [crbug.com/40061541](https://crbug.com/40061541).

### pe...@google.com (2024-05-04)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ad...@gmail.com (2024-05-05)

I've figured out a far more reliable method that doesn't involve a race condition.

If we add a `debugger` statement to the content script that's injected, then run `inject_script()` twice, the tab will crash. However, the injected script is still queued up to run on the next page load. Thus when the tab gets navigated to `chrome://policy`, the content script will execute on the privileged page, without the need for any unreliable timing.

I'm not sure why, but this only works on `about:blank` pages. We can't simply do `chrome.tabs.update(tab_id, {url: "about:blank"})`, since this set the origin of the `about:blank` page to the extension's origin. If we crash this page, the extension's devtools page will also crash. The solution to this is to navigate to a different origin, then evaluate some JS on the inspected page to navigate to `about:blank` with the new origin.

I've attached the new version of `devtools.js` which implements this strategy.

### ch...@chromium.org (2024-05-06)

Thanks, the new repro in [comment #5](https://issues.chromium.org/issues/338248595#comment5) seems to work reliably for me. Upgrading to Critical severity.

Looks like part of this chain involves inducing a crash [at this CHECK](https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/render_frame_impl.cc;l=1345-1346;drc=770f3fce3719ee18c102ad0b1a347d82147fbb1a). The navigation commit state is not what we expect. cc dcheng: Mind taking a look?

### ad...@gmail.com (2024-05-06)

By the way, I took a look at the git history, and it looks like the chrome://policy bug exists ever since the test policy functionally was added [10 months ago on commit cd9f03412329ca2d8cff21c589dd15d6eedba536](https://chromium-review.googlesource.com/c/chromium/src/+/4658098). I verified this by testing the extension on [position 1166828 (version 117.0.5876.0)](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/1166828/) which did work, but testing on [position 1166822 (same version number)](https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/1156812/) did not.

Injecting scripts on `inspectedWindow.reload` was added [13 years ago](https://chromium.googlesource.com/chromium/blink/+/183eb96ce9836c3f1ccfd7ec82fcd7eac740319c%5E%21/#F8), so its likely that this part of the bug works on nearly every version of Chrome. ~~The crash that's required for the more reliable version to work was introduced [4 years ago](https://chromium-review.googlesource.com/c/chromium/src/+/2335323).~~ (this is inaccurate, any sort of crash works)

### ch...@chromium.org (2024-05-06)

Thank you for digging into it.

It would be helpful if you could break this down into the separate bugs that make up this chain, file a new issue for each one, and link them here.

### am...@chromium.org (2024-05-06)

The precondition of the installation of a malicious extension is a bit of a mitigation here that would reduce the severity of this issue from critical to high. I've update severity to reflect that.

### ap...@google.com (2024-05-17)

Project: chromium/src
Branch: main

commit beb3a0dab4470df7fb927c13935777f6d5228ec3
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Fri May 17 10:12:02 2024

    Add loaderId argument to Page.reload
    
    By passing the loaderId, clients can prevent accidentally reloading
    unintended targets when Page.reload is racing with a navigiation.
    
    Bug: 338248595
    Change-Id: I68883658a2112bba2a4cb428b4c3c33314c5e894
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5542082
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1302488}

M       content/browser/devtools/protocol/page_handler.cc
M       content/browser/devtools/protocol/page_handler.h
M       third_party/blink/public/devtools_protocol/browser_protocol.pdl
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
M       third_party/blink/web_tests/inspector-protocol/page/reload-dataurl.js
A       third_party/blink/web_tests/inspector-protocol/page/reload-loaderId-expected.txt
A       third_party/blink/web_tests/inspector-protocol/page/reload-loaderId.js
M       third_party/blink/web_tests/inspector-protocol/page/reload-on-breakpoint.js

https://chromium-review.googlesource.com/5542082


### ap...@google.com (2024-05-17)

Project: devtools/devtools-frontend
Branch: main

commit 50b6d6025d292d466dcaa152f8472ba7d7c907fe
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Fri May 17 11:33:09 2024

    Roll browser_protocol
    
    Bug: 338248595
    Change-Id: I5de396070433a915354eb8f337875444db337feb
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5546065
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>

M       front_end/generated/InspectorBackendCommands.js
M       front_end/generated/protocol.ts
M       third_party/blink/public/devtools_protocol/browser_protocol.json
M       third_party/blink/public/devtools_protocol/browser_protocol.pdl

https://chromium-review.googlesource.com/5546065


### ap...@google.com (2024-05-17)

Project: devtools/devtools-frontend
Branch: main

commit 33a09fb44a6f593270589acfac482d9b275b389c
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Fri May 17 13:18:02 2024

    Ensure inspectedWindow.reload reloads the correct page
    
    This prevents unintended reloads when racing with navigations.
    
    Drive-by: Check extension allowlist when loading page resources.
    
    Bug: 338248595
    Change-Id: Ibbac5bbd45b1db0d05e32fe8e384740933ee4639
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5546062
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>

M       front_end/core/sdk/ResourceTreeModel.test.ts
M       front_end/core/sdk/ResourceTreeModel.ts
M       front_end/models/extensions/ExtensionServer.test.ts
M       front_end/models/extensions/ExtensionServer.ts

https://chromium-review.googlesource.com/5546062


### pf...@chromium.org (2024-05-17)

This fixes the devtools extension step of the chain, by making sure the page we reload is actually the same that we allowed the inspectedWindow.reload call on. Assigning to ydago for the chrome://policy bug!

### ad...@gmail.com (2024-05-19)

I have filed separate bugs for each step in the chain:

- <https://issues.chromium.org/issues/341136300>
- <https://issues.chromium.org/issues/341472977>

### pf...@chromium.org (2024-05-21)

Would you mind CCing me on the second one?

The first bug is actually a different one than the one in your original chain. At least it has a different cause, as you correctly identified. Would you mind filing a separate one for the navigation/reload race, too? I believe I've fixed that already, but it'd be nicer to track the individual fixes in isolated bugs for merging etc.

### ad...@gmail.com (2024-05-21)

I've submitted the race condition bug as its own issue: <https://issues.chromium.org/issues/341875171>

Unfortunately I don't think I have the permissions to CC anyone, and even if I did, the issue tracker site redacts emails. You're only showing up as "[pf...@chromium.org](mailto:pf...@chromium.org)" right now.

### da...@google.com (2024-05-21)

I've cc'd you, Philip.

On Tue, May 21, 2024 at 2:18 PM ading2019 <buganizer-system@google.com>
wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/338248595
>
> *Changed*
>
> *ading2019@gmail.com <ading2019@gmail.com> added comment #16
> <https://issues.chromium.org/issues/338248595#comment16>:*
>
> I've submitted the race condition bug as its own issue:
> https://issues.chromium.org/issues/341875171
>
> Unfortunately I don't think I have the permissions to CC anyone, and even
> if I did, the issue tracker site redacts emails. You're only showing up as "
> pf...@chromium.org" right now.
>
> _______________________________
>
> *Reference Info: 338248595 Sandbox escape from extensions due to
> insufficent checks in chrome.devtools.inspectedWindow.reload and
> chrome://policy*
> component:  Public Trackers > Chromium Public Trackers > Chromium >
> Platform > DevTools <https://issues.chromium.org/components/1457055>
> status:  Assigned
> reporter:  ading2019@gmail.com
> assignee:  ydago@chromium.org
> cc:  ading2019@gmail.com, caseq@chromium.org, danilsomsikov@google.com,
> and 4 more
> collaborators:  pfaffe@chromium.org, security@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  124
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>, Untriaged
> <https://issues.chromium.org/hotlists/5614589>, User-Submitted
> <https://issues.chromium.org/hotlists/5562135>
> retention:  Component default
> Component Ancestor Tags:  Platform, Platform>DevTools
> Component Tags:  Platform>DevTools
> Milestone:  124
> OS:  Linux, Mac, Windows, ChromeOS
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 338248595
> <https://issues.chromium.org/issues/338248595> where you have the roles:
> cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/338248595?unsubscribe=true>
>


### ap...@google.com (2024-05-29)

Project: devtools/devtools-frontend
Branch: chromium/6478

commit 43a5bbfc701fac429efdfc3a6cd0fc7879ac514e
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Fri May 17 11:33:09 2024

    Roll browser_protocol
    
    Bug: 338248595
    Change-Id: I5de396070433a915354eb8f337875444db337feb
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5546065
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Commit-Queue: Danil Somsikov <dsv@chromium.org>
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
    (cherry picked from commit 50b6d6025d292d466dcaa152f8472ba7d7c907fe)
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5580036
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

M       front_end/generated/InspectorBackendCommands.js
M       front_end/generated/protocol.ts
M       third_party/blink/public/devtools_protocol/browser_protocol.json
M       third_party/blink/public/devtools_protocol/browser_protocol.pdl

https://chromium-review.googlesource.com/5580036


### ap...@google.com (2024-05-29)

Project: chromium/src
Branch: refs/branch-heads/6478

commit bdb10c5dca22b339f1075564e3623675eedf9e82
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Wed May 29 09:25:19 2024

    Add loaderId argument to Page.reload
    
    By passing the loaderId, clients can prevent accidentally reloading
    unintended targets when Page.reload is racing with a navigiation.
    
    (cherry picked from commit beb3a0dab4470df7fb927c13935777f6d5228ec3)
    
    Bug: 338248595, 341875171
    Change-Id: I68883658a2112bba2a4cb428b4c3c33314c5e894
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5542082
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org>
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1302488}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5576938
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#802}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/devtools/protocol/page_handler.cc
M       content/browser/devtools/protocol/page_handler.h
M       third_party/blink/public/devtools_protocol/browser_protocol.pdl
M       third_party/blink/renderer/core/inspector/inspector_page_agent.cc
M       third_party/blink/renderer/core/inspector/inspector_page_agent.h
M       third_party/blink/web_tests/inspector-protocol/page/reload-dataurl.js
A       third_party/blink/web_tests/inspector-protocol/page/reload-loaderId-expected.txt
A       third_party/blink/web_tests/inspector-protocol/page/reload-loaderId.js
M       third_party/blink/web_tests/inspector-protocol/page/reload-on-breakpoint.js

https://chromium-review.googlesource.com/5576938


### ap...@google.com (2024-05-29)

Project: devtools/devtools-frontend
Branch: chromium/6478

commit 3c74763045f44bea6319164593b4d6a0ed34990a
Author: Philip Pfaffe <pfaffe@chromium.org>
Date:   Wed May 29 08:21:01 2024

    Ensure inspectedWindow.reload reloads the correct page
    
    This prevents unintended reloads when racing with navigations.
    
    Drive-by: Check extension allowlist when loading page resources.
    
    Bug: 338248595, 341875171
    Change-Id: Ibbac5bbd45b1db0d05e32fe8e384740933ee4639
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5546062
    Reviewed-by: Danil Somsikov <dsv@chromium.org>
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
    (cherry picked from commit 33a09fb44a6f593270589acfac482d9b275b389c)
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5580037
    Reviewed-by: Ergün Erdoğmuş <ergunsh@chromium.org>

M       front_end/core/sdk/ResourceTreeModel.test.ts
M       front_end/core/sdk/ResourceTreeModel.ts
M       front_end/models/extensions/ExtensionServer.test.ts
M       front_end/models/extensions/ExtensionServer.ts

https://chromium-review.googlesource.com/5580037


### pe...@google.com (2024-06-05)

ydago: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ts...@google.com (2024-06-10)

Sent email to owner to see if this can be closed.

### ad...@gmail.com (2024-06-16)

I've found yet another way to trigger the code execution on privileged pages, which gets around the previous fix: <https://issues.chromium.org/issues/347495363>

### an...@chromium.org (2024-06-20)

Hi ydago, secondary security shepherd here. I've added some child issues based on the comments above. 2 of the child issues have been fixed while 2 remain open. Please mark this issue fixed when all child issues are fixed. Thanks!

### pe...@google.com (2024-06-20)

ydago: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-07-01)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ap...@google.com (2024-07-08)

Project: chromium/src
Branch: main

commit 99cafbf4b4b90cfc773826ea17fdaffe094207af
Author: Yann Dago <ydago@chromium.org>
Date:   Mon Jul 08 16:20:32 2024

    Ensure chrome://policy/test messages ignored when not supported
    
    It was possible to go to chrome://policy and in the dev tools and send
    the right message to set test policies even if the policy test page was disabled and/or unavailable because both pages share the same handler.
    
    Bug: 338248595
    Change-Id: If689325999cb108b2b71b2821d905e42efd3390d
    Low-Coverage-Reason: TRIVIAL_CHANGE
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5679162
    Auto-Submit: Yann Dago <ydago@chromium.org>
    Reviewed-by: Rohit Rao <rohitrao@chromium.org>
    Reviewed-by: Sergey Poromov <poromov@chromium.org>
    Commit-Queue: Rohit Rao <rohitrao@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1324277}

M       chrome/browser/ui/webui/policy/policy_test_ui_browsertest.cc
M       chrome/browser/ui/webui/policy/policy_ui_handler.cc
M       ios/chrome/browser/webui/ui_bundled/policy/policy_ui_handler.mm

https://chromium-review.googlesource.com/5679162


### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
consolidated reward for high quality report of crbug.com/338248595, crbug.com/341136300, crbug.com/341875171 -- resulting in a sandbox escape


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-17)

Congratulations Allen! While this sandbox escape is considerer mitigated by the precondition to install a malicious extension, we feel the $20k reward is warranted due to high quality and providing functional exploit, clear demonstration, and this was an overall clever set of discoveries chained together for high impact. As this is a consolidated reward for the child bugs for this issue, those are also considered to be web platform privilege escalation bugs and warranting the overall reward here. Thank you for this high quality and thorough report and your efforts in discovering these issues and reporting it to us -- excellent work!

### ad...@gmail.com (2024-07-19)

Thank you so much for the reward!

### pe...@google.com (2024-10-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338248595)*
