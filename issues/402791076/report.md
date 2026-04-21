# Security: DevTools XSS allows sandbox escape, UXSS, CDP access, other impacts

| Field | Value |
|-------|-------|
| **Issue ID** | [402791076](https://issues.chromium.org/issues/402791076) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | da...@google.com |
| **Created** | 2025-03-13 |
| **Bounty** | $4,000.00 |

## Description

## SUMMARY

This is a variation of [issue 40942152](https://issues.chromium.org/issues/40942152) due to incomplete fix.

With `devtools://devtools/bundled/integration_test_runner.html` connected to a malicious remote WebSocket server, after user double-clicks on a network log item, an attacker can run JavaScript in `devtools://devtools` origin.

Impacts include universal XSS, browser sandbox escape by opening downloaded file, local file read, user interaction requirements bypass, and access to most CDP commands.

Initial report has PoCs for browser sandbox escape initiated from web page. I will provide the other PoCs once I've cleaned them up, including extension PoCs that reduce user interaction.

## VULNERABILITY DETAILS

`devtools://` URLs can be opened with drag-and-drop from any page, or automatically by an extension with `devtools_page` in manifest or `debugger` permission.

`devtools://devtools/bundled/integration_test_runner.html` renders data provided by the WebSocket server specified via `?ws=` param [1], including remotely-hosted WS servers.

A malicious WS server can generate network log rows for a resource with a `javascript:` URL. Double-clicking [2] a network log row will call `InspectorFrontendHost.openInNewTab()` [3] which calls `window.open(url, '_blank')` [4] with the URL of the resource, in this case the `javascript:` URL. (Right-clicking the row and selecting `Open in new tab` works similarly.)

Because `integration_test_runner.html` does not have CSP, the JS runs in a new window with the `devtools://devtools` origin. At this point, attacker can read/write to `localStorage` and set console pins. We then ask the user to press F12 to run the malicious console pins, which perform the rest of the attack. After the keypress, we also download the file we want to open (this download can occur at any point during the attack).

Because `devtools://` pages cannot directly navigate to `chrome://` URLs, the console pins will navigate to the PDF component extension (`chrome-extension://mhjfbmdgcfjbbpaeojofohoefgiehjai/pdf_viewer_wrapper.js`), then use the extension's `chrome.tabs` API to navigate to `chrome://downloads`, then execute JS in `chrome://downloads` to open the download.

In the provided PoCs, we then clean up the attack by deleting the malicious console pins, and either closing tabs or navigating tabs to benign pages.

Opening a downloaded file requires [5] a user interaction within the past 5 seconds, tracked per-tab using `WebContentsImpl::last_interaction_time_` [6]. In faster devices, this is satisified by the earlier F12 keypress because the attack takes less than 5 seconds (see Scenario 1a). For 100% reliability, particularly on slower devices, we can generate a user interaction using CDP `Input.*` commands immediately before the file open attempt (see Scenario 1b).

## Impacts

Immediately after initial XSS:

- Local file read: Read local files and directories with `DevToolsUIBindings::LoadNetworkResource()` [7] (which is handler of `loadNetworkResource` message sent through `DevToolsHost.sendMessageToEmbedder()`).
- Set console pins: UXSS where DevTools is opened in the future, used for further impacts

After opening DevTools with malicious console pins:

- Sandbox escape by opening downloaded file: See main vuln description.
- UXSS: We can navigate current tab to any page and execute arbitrary JS regardless of CSP.
- Open DevTools-on-DevTools to gain CDP access: We can open `chrome://inspect` and run JS to inspect the current DevTools instance (i.e. DevTools-on-Devtools), used for further impacts

After obtaining CDP access via DevTools-on-DevTools:

- Interaction requirement bypasses: We can send CDP `Input.*` commands to simulate user interaction and bypass user interaction restrictions.
- Parallel UXSS via CDP: For more efficient attacks, we can open multiple tabs and attack each of them simultaneously via CDP.
- Do anything else interesting with CDP against any listed target

[1] `ws` param read: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/core/sdk/Connections.ts;l=292;drc=5efc7e9be253ceb20ebc8fcc1710f42623272bf7>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/panels/network/NetworkDataGridNode.ts;l=1085;drc=ebb421b7cdc02be3ee4abf49d6bad7646b3da9ab>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/panels/network/NetworkDataGridNode.ts;l=1069;drc=ebb421b7cdc02be3ee4abf49d6bad7646b3da9ab>

[4] `InspectorFrontendHost.openInNewTab()` <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/core/host/InspectorFrontendHost.ts;l=190;drc=4ab8cec6e9a5640f553f44afeec821b9e7050eb9>

[5] `DownloadsDOMHandler::OpenFileRequiringGesture()` <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/downloads/downloads_dom_handler.cc;l=244;drc=b37413daa8803e67405b635419ab665e0374a093>

[6] `WebContentsImpl::last_interaction_time_` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.h;l=2380;drc=ebb421b7cdc02be3ee4abf49d6bad7646b3da9ab>

[7] `DevToolsUIBindings::LoadNetworkResource()` <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/devtools_ui_bindings.cc;l=1100;drc=de65c59454bb29fff1e642fb3528cd2c80e52fb4>

## ADDITIONAL CONTEXT

### Reduction of attack user interactions

For extensions with `devtools_page` in manifest, we can open `devtools://` URLs automatically. For extensions with `debugger` permission, most steps are automatic. I'll provide extension PoCs in comments.

### Other ways to reach `openInNewTab()`

While we use the Network panel to exploit this, any other usage of `InspectorFrontendHost.openInNewTab()` [4] is also vulnerable if attacker controls the URL (see Code Search [4]). Double clicking on network log row seemed like the easiest way to exploit.

## VERSION

Verified repro on these versions:

Chrome Version: 134.0.6998.37 Stable, 135.0.7049.17 Beta, 136.0.7052.2 Dev, 136.0.7065.0 Canary

Operating System: Windows 10 (should repro for all desktop platforms)

## PROPOSED PATCH

`InspectorFrontendHost.openInNewTab()` has many call sites. For example, most `Linkfier` methods call it but don't check for unsafe schemes except for `Linkifier::linkifyURL()` [1]. There are other ways to reach `openInNewTab()` outside of `Linkifier`.

To ensure all current and future call sites are protected, adding the scheme check in `InspectorFrontendHost.openInNewTab()`, right before the `window.open()` call, seems like the best approach. AFAICT none of the current callers have a legitimate need to pass JS URLs.

I'll upload a CL within a day or so.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/ui/legacy/components/utils/Linkifier.ts;l=533;drc=aec1575a78abeec098d606c3c738215ca874b3b4>

## BISECT

Had to do two bisects for the DevTools XSS. Earliest repro is Feb 2018 with `inspector.html`.

1. For `integration_test_runner.html`:
     
   
   Bisected to <https://chromium.googlesource.com/devtools/devtools-frontend.git/+/9327dc31d27d2a5061636ce35e726dfd755a6dd3> (Mar 2021)
     
   
   `integration_test_runner.html` fails to load a JS file before then, so PoC fails. But you can use `devtools_app.html` as shown in second bisect.
     
   
   The `devtools-frontend` commit above was rolled into Chromium in <https://crrev.com/ab3bc54ec9d1e6204ff73d71e4390903842af64b>
2. For `devtools_app.html`/`inspector.html` (and probably other "production" entrypoints):
     
   
   Bisected to <https://crrev.com/abbb84580486221060a05e452652e045086ebc6c> (Feb 2018) when `unsafe-inline` was added to CSP. Repro'd with `chrome-devtools://devtools/bundled/inspector.html`.
     
   
   Stopped reproducing in <https://chromium.googlesource.com/devtools/devtools-frontend.git/+/1e2c0032dae51afc104b525b621ad723c0501361> (Oct 2021) when `unsafe-inline` was removed for the non-test entrypoints.

## REPRODUCTION CASE

Additional PoCs will be provided in the coming days.

One-time setup for WebSocket server:

1. Download `package.json` and `websocket-server.js`
2. Run `npm i` to install dependency
3. Set desired port in source code (default `1337`)

Setup for *each* scenario:

1. Host per-scenario payload remotely or locally. Payload must be served with `Access-Control-Allow-Origin: *` and `Content-Type: text/javascript` headers.
2. Update WebSocket server source to point to per-scenario payload URL.
3. Run attacker WebSocket server with `node websocket-server.js`, remotely or locally.

### Scenario 1a: Sandbox escape via download

Payload: `devtools-xss-download-sandbox-escape-1a`

This depends on the automated steps occuring within 5 seconds. In slower devices, scenario 1b may be needed for 100% reliability.

Repro steps:

1. Navigate to <https://alesandroortiz.com/security/chromium/devtools-drag.html?ws=host:port> (replace `host:port` with your WS server)
2. Drag the icon to a new tab (or existing tab)
3. Double-click where DevTools says "CLICK TWICE HERE" to run JS payload (after this step, we have initial XSS with some impacts)
4. Press F12 when prompted, then wait a few moments

Observed: JavaScript runs in `devtools://devtools` origin. Downloaded file is opened.

Expected: JavaScript is blocked from executing in any `devtools://` origin. Downloaded file is not opened.

### Scenario 1b: Sandbox escape via download + generated user interaction via CDP

Payload: `devtools-xss-download-sandbox-escape-1b`

Optional: To verify that this PoC does not depend on user interaction, set `simulateDelayedLoading` to `true` in payload.

Same impacts as 1a, but with 100% reliability because it uses DevTools-on-DevTools to access CDP and generate user interaction.

Repro steps: Same as scenario 1a (with different payload).

Observed/Expected: Same as scenario 1a.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com> and Daniel Fröjdendahl <https://FrojdenSec.com>

## Attachments

- devtools-drag.html (text/html, 11.2 KB)
- devtools-xss-download-sandbox-escape-1a.js.php (application/x-httpd-php, 2.7 KB)
- devtools-xss-download-sandbox-escape-1b.js.php (application/x-httpd-php, 5.8 KB)
- package.json (application/json, 68 B)
- websocket-server.js (text/javascript, 1.7 KB)
- devtools-xss-scenario-1a.mp4 (video/mp4, 2.3 MB)
- devtools-xss-scenario-1b.mp4 (video/mp4, 2.9 MB)
- manifest.json (application/json, 325 B)
- background.js (text/javascript, 3.4 KB)
- devtools.html (text/html, 45 B)
- instructions-top.html (text/html, 449 B)
- instructions-bottom.html (text/html, 397 B)
- devtools-xss-extension-devtools_page.mp4 (video/mp4, 2.7 MB)
- devtools-xss-scenario-3.js.php (application/x-httpd-php, 4.8 KB)
- devtools-xss-scenario-3a-drag.mp4 (video/mp4, 4.7 MB)
- devtools-xss-scenario-3b-extension.mp4 (video/mp4, 5.0 MB)
- NullOriginXSSlogEntryAdded.PNG (image/png, 17.9 KB)
- extensionFishExample.png (image/png, 108.6 KB)
- remoteDesktopPoC.txt (text/plain, 1.7 KB)

## Timeline

### al...@alesandroortiz.com (2025-03-13)

Most of the techniques used in this report have been previously documented. David Erceg also compiled many of these techniques in <https://microsoftedge.github.io/edgevr/posts/attacking-the-devtools/>

Many thanks to the researchers who documented these techniques. 🙏🏻

### UXSS by setting console pins in localStorage

Earliest crbug AFAICT: [Issue 40051911](https://issues.chromium.org/issues/40051911)

### Gaining access to `DevToolsHost` bindings

There is no `DevToolsHost` binding available to windows with openers after <https://crrev.com/484f731aaead5d72c26a21ea012cd2a706146f19> (2017).
However, this can be bypassed by setting the opener to `null` and reloading the page.

Earliest crbug AFAICT: [Issue 40084203](https://issues.chromium.org/issues/40084203)

### DevTools-on-DevTools CDP access via XSS on chrome://inspect

Earliest crbug AFAICT: <https://crbug.com/40051715#comment14>

### Sandbox escape via Downloads with simulated user interaction

Earliest crbug AFAICT: [Issue 40051715](https://issues.chromium.org/issues/40051715). Also see [issue 40053103](https://issues.chromium.org/issues/40053103).

### File/dir read via `loadNetworkResource()`

Documented in numerous crbugs. Earliest crbug AFAICT: <https://crbug.com/40083420#comment13>

### Drag-and-drop to open `devtools://` URL

[Issue 40942152](https://issues.chromium.org/issues/40942152)

### al...@alesandroortiz.com (2025-03-13)

A couple of additional impacts:

- When we have `DevToolsHost` access, we can get account email address, name, image, browser sync status [1]:
    
  
  `InspectorFrontendHost.getSyncInformation((r) => console.info(r))`
- `localStorage` for `devtools://` leaks some data:
  
  - console history (even from previous DevTools windows)
  - all breakpoints and associated URLs (i.e. limited browsing history leak)
  - previously viewed files

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/devtools_ui_bindings.cc;l=1589;drc=ebb421b7cdc02be3ee4abf49d6bad7646b3da9ab>

### al...@alesandroortiz.com (2025-03-13)

For the drag-and-drop scenario, if user has not opened DevTools (or any `devtools://devtools` URL) since the browser profile start, the DevTools URL will not load. This was also the behavior for [issue 40942152](https://issues.chromium.org/issues/40942152), but it wasn't mentioned in the report or comments.

To solve this, attacker needs to have user press F12 (or drag-and-drop any `devtools://devtools` URL, even if it 404s) before navigating to the `integration_test_runner.html` URL. This is an extra user interaction, but is not always required depending on the target user.

This is not an issue in extension scenarios since they can open the URLs automatically.

### al...@alesandroortiz.com (2025-03-13)

Please CC collaborating researcher [daniel.frojdendahl@gmail.com](mailto:daniel.frojdendahl@gmail.com) when able

### al...@alesandroortiz.com (2025-03-13)

Uploaded CL: <https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6353071>

Verified patch fixes issue by using `--custom-devtools-frontend=http://{mybuildserver}:8000/` on 136.0.7066.0 Canary and testing out PoCs. Double-clicking on network log row with `javascript:` URL does nothing.

### al...@alesandroortiz.com (2025-03-13)

In addition to fix above, we could also re-enable CSP in integration\_test\_runner and make it match the CSP used for entrypoints.

The CSP in integration\_test\_runner was disabled in <https://chromium.googlesource.com/devtools/devtools-frontend/+/3d72768baa3f0bc735faf04b9a63b3e353e22002>

I don't see `eval()` calls anymore but maybe something else will break if CSP is re-enabled.

CSP used for entrypoints: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/entrypoint_template.html;l=17;drc=91816c4c3389eb4b923f4f1a17e90481d3bfdd70>

I'll try that approach to see if anything breaks when using it. If it seems to work locally, I'll upload CL and run test suite to verify tests work with the CSP.

### ke...@chromium.org (2025-03-13)

Thanks for the report.

I haven't been able to successfully reproduce this, because the fetch at this line currently fails:
`var url = 'devtools://devtools/bundled/integration_test_runner.html?inspected_test=https://aogarantiza.com&ws=${ws}&panel=network';`

However after reading through this, there is enough detail to demonstrate the issue and proceed with triage.

danilsomsikov@: Since you dealt with a similar issue previously, can you please have a look at this?

### al...@alesandroortiz.com (2025-03-13)

Thanks for triage.

If the `integration_test_runner.html` URL fails to load after the drag-and-drop, see [#comment4](https://issues.chromium.org/issues/402791076#comment4).

Please also CC collaborator ([#comment5](https://issues.chromium.org/issues/402791076#comment5)).

### al...@alesandroortiz.com (2025-03-13)

Re: [#comment7](https://issues.chromium.org/issues/402791076#comment7), when testing locally, the stricter CSP seems to work just fine if we remove the `importmap` (which wouldn't work because it's defined inline).

2nd CL with stricter CSP: <https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6353880>

~~I ran 2nd CL through tests with stricter CSP but with importmap and got no errors, but I'm not sure if `integration_test_runner` is tested or used by `devtools-frontend` tests or if it's only used by integration tests that run elsewhere.~~

Maybe someone with knowledge of how `integration_test_runner` is used and whether the importmap is still needed can determine whether we can or cannot use the stricter CSP.

Update: 2nd CL with stricter CSP does break the tests. :/

### ch...@google.com (2025-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### da...@google.com (2025-03-17)

Benedikt, does your recent change covers this?

### bm...@google.com (2025-03-17)

<http://crrev.com/c/6346913> will likely help, but is not sufficient. The motivation of that CL was to ensure that UTM parameters are present for documentation links. I didn't audit all uses of `InspectorFrontendHost.openNewTab`, but only those which can open links to documentation.

### al...@alesandroortiz.com (2025-03-17)

Re: <http://crrev.com/c/6346913>

There's no behavior change in the PoCs. Even with the updates in that CL, the `javascript:` links still reach `InspectorFrontendHost.openInNewTab()`.

My CL was branched after that CL was submitted (I double-checked now in git logs too), and I verified the behavior reproduced before my patch. I also reviewed the other CL on Thursday, also thinking it may have had some impact on the repro or overlap with patch. But it doesn't have any effect.

### al...@alesandroortiz.com (2025-03-17)

Can someone please CC collaborator ([#comment5](https://issues.chromium.org/issues/402791076#comment5))? :)

I've submitted CL, thanks for reviews!

I'm still working on the extension PoCs, will have those available sometime this week.

### al...@alesandroortiz.com (2025-03-18)

Can someone please mark this as fixed? Not sure why automation didn't do so. Verified as fixed in 136.0.7075.0 Canary.

CL landed yesterday: <https://crrev.com/c/6353071>

Rolled in: <https://crrev.com/71a64e50132262fcec55c24713b6005d70968472>

(Edit: Corrected CL/commit links)

### al...@alesandroortiz.com (2025-03-18)

Attached PoC that removes the drag-and-drop interaction and open-DevTools-once-before prerequisite. Requires `devtools_page` in manifest which asks for "Read and change all your data on all websites" (same as `tabs` permission), with no debugger-specific language. `devtools_page` key in manifest is required because extensions can only open `devtools://` URLs with this key in manifest (or `debugger` permission, which we don't uses here).

## REPRODUCTION CASE

One-time setup for WebSocket server: See original report.

Also see `Setup for _each_ scenario` steps in original report.

Extension setup:

1. Download `manifest.json` + `background.js` + `devtools.html` + `instructions-top.html` + `instructions-bottom.html`
2. Update `background.js` to use your WebSocket server.

### Scenario 2: Sandbox escape via download + extension with `devtools_page`

Payload: Use payload from either Scenario 1a or 1b. We use payload 1a in video.

Repro steps:

1. Install/reload attached extension (extension can execute attack at any time).
2. Double-click where it says "CLICK TWICE HERE" to run JS payload (after this step, we have initial XSS with some impacts)
3. Press F12 when prompted, then wait a few moments

Observed: JavaScript runs in `devtools://devtools` origin. Downloaded file is opened.

Expected: JavaScript is blocked from executing in any `devtools://` origin. Downloaded file is not opened.

### al...@alesandroortiz.com (2025-03-18)

I thought I would be able to automate more of the PoC, but due to restrictions in `Input.*` CDP commands from extensions, we cannot press F12 or invoke other browser-level shortcuts from an extension (these mitigations were added back in 2020-2021). So I think this will be the best PoC, which is only a small improvement compared to the web-only PoC, but also introduces the mitigation of having to install extension.

I'll provide additional PoCs for other lesser impacts soon.

### ch...@google.com (2025-03-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### al...@alesandroortiz.com (2025-03-20)

Attached PoC for full impacts possible immediately after initial XSS:

- Read local files and directories
- Leak NTLM hash: Bypass of fix for [issue 40060207](https://issues.chromium.org/issues/40060207) (update payload source config to observe)
- Get logged-in browser account email, name, image
- XSS any frameable page: web pages or extension pages
- Bypass extension's `web_accessible_resources` restriction: Load any extension's non-WAR page
- Bypass popup blocker: can open unlimited tabs; useful when attack is made by web page (update payload source config to observe)

These impacts are possible when attack is initiated from either web page or extension.

## REPRODUCTION CASE

One-time setup for WebSocket server: See original report.

Also see `Setup for _each_ scenario` steps in original report.

Extension setup:

1. From [#comment18](https://issues.chromium.org/issues/402791076#comment18), download `manifest.json` + `background.js` + `devtools.html` + `instructions-top.html` + `instructions-bottom.html`
2. Update `background.js` to use your WebSocket server.

Payload for both scenarios below: `devtools-xss-scenario-3`.

Payload setup:

1. Set `localFileToRead` in payload source (hardcoded for PoC).
2. Also update payload config to optionally observe popup blocker bypass and NTLM hash leak.
3. To observe extension WAR bypass, please install Google Translate extension: <https://chromewebstore.google.com/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb>

### Scenario 3a: Multiple impacts on initial XSS + drag-and-drop from web page

Repro steps:

1. Navigate to <https://alesandroortiz.com/security/chromium/devtools-drag.html?ws=host:port> (replace host:port with your WS server)
2. Drag the icon to a new tab (or existing tab)
3. Double-click where DevTools says "CLICK TWICE HERE" to run JS payload

### Scenario 3b: Multiple impacts on initial XSS + extension with `devtools_page`

Repro steps:

1. Install/reload attached extension (extension can execute attack at any time).
2. Double-click where it says "CLICK TWICE HERE" to run JS payload

Observed for both scenarios: Impacts listed at beginning of comment.

### am...@chromium.org (2025-03-26)

We appreciate the thoroughness of this report, however, there are pretty significant preconditions here, such as the direct interaction with devtools + significant user interaction || installing the extension + user interaction. Downgrading this to medium given that lessen potential for exploitability given the preconditions.

I'll consider <https://crrev.com/c/6353071> for backmerge since there is no dependency on the other previous CL for resolution, but I've been waiting for some Dev data, there hasn't been a new Dev update on Windows for some days now given timing with respins and a Dev release blocker on Windows.

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact web platform privilege escalation + $2,000 patch bonus + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Congratulations Alesandro! Thank you for your efforts in reporting this issue, but also submitting a patch. 

### al...@alesandroortiz.com (2025-03-27)

Hi Amy, thanks for reward! This was a collab with Daniel, so thanks goes to them too. :)

That said, can the VRP panel please take another look?

The maximum impact here is UXSS and sandbox escape, not web platform privilege escalation IMO. Even if mitigated by user interactions, it should be considered as a different vuln class.

[Issue 40942152](https://issues.chromium.org/issues/40942152) was rewarded $6k back in 2023 (limited UXSS, file/dir read) and [issue 40060207](https://issues.chromium.org/issues/40060207) $7.5k in 2022 (NTLM hash leak). This report demonstrates the *same* impacts as both issues *plus* additional impacts (sandbox escape and other lesser impacts). I know rewards table has changed since then and different bugs/rewards aren't often comparable, etc. but I want to make sure full impacts were considered, even if mitigated by user interaction (the user interaction requirements are identical to [issue 40942152](https://issues.chromium.org/issues/40942152) for the "initial" impacts).

[#comment21](https://issues.chromium.org/issues/402791076#comment21) mentions several "initial" impacts possible with only two steps: 1. drag-and-drop from web OR extension install, 2. double-click. Some of these initial impacts fall under `User information disclosure` vuln class:

- NTLM hash leak
- Sync'd account info leak (name, email, photo)
- Local file/dir read
- Limited history leak via breakpoints and associated URLs ([#comment3](https://issues.chromium.org/issues/402791076#comment3))

Initial impacts also can fall under `UXSS || Site isolation bypass`:

- UXSS any frameable web pages or extension pages

Maximum impacts after doing those two steps, and then pressing F12 (3 steps total), includes gaining unrestricted CDP access, which gives us free reign within the browser. CDP-related impacts include:

- UXSS anything, including restricted hosts such as DevTools itself, `chrome://` WebUI pages, other extensions, etc. We can also send `Input.*` commands at browser-level to bypass security checks that depend on user interaction, such as opening downloads, which leads to...
- running a binary in the host machine (sandbox escape)
- and anything else possible with unrestricted CDP access (such as reading/writing storage for any origin/extension)

### al...@alesandroortiz.com (2025-03-27)

For reference on other bugs that have same impacts, also see [#comment2](https://issues.chromium.org/issues/402791076#comment2).

### ch...@google.com (2025-04-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135, 136].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-04-04)

The fix was already landed to M136, so no merge needed.
M135 is already shipping to Stable, with the preconditions to exploit. I'm going to decline backmerge for this as M136 will be promoted to Stable in just over three weeks.

This has been tagged for VRP reassessment.

### ch...@google.com (2025-04-30)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M135, which branched on 2025-03-03 (Chromium branch: 7049, Chromium branch position: 1427262)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, add the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### am...@chromium.org (2025-05-17)

Apologies for the delay here. We did review this issue as part of a reassessment some time ago, but I did not update it following panel at that time. Sincere apologies for delay.

The outcome of that reassessment was that there was not sufficient new information provided and the core aspect of this report was pointing out an insufficient fix. And while we appreciate that, there are additionally significant preconditions for exploitability and attacker control via requirements for user interaction. As such, we determined the original reward was sufficient for this report.

Again, sincere apologies for the delay in updating this.

### da...@gmail.com (2025-06-11)

Hello! :)
Im trying to decipher the rules of the program as well as the rationale of the decision here.
The source Im looking at is [1] - please correct me if Im mistaken here!

As pointed out in #30:
"and the core aspect of this report was pointing out an insufficient fix."

This is incorrect. These are different vulnerabilites and I think some confusion is here.
We make use of **"Network.webSocketCreated"** which had a missing check for a "javascript:" URI's thus enabling the XSS.

If our report used the same method "Log.entryAdded" as [5] to achieve the XSS I would absolutely agree that it is pointing out an insufficient fix - as that would be 100% true.
The "Network.webSocketCreated" or "linkifier::linkifyURL()" [2] was something that was found by reviewing the codebase and thoroughly testing/enumerating, this is novel and new to our report.
The same can be said for the delivery method via an extension instead of using the drag-and-drop from the initial PoC landing page. All of this took quite some time to find and come up with this new path to exploitation.

While its still possible to use "Log.entryAdded" method it is simply not possible anymore to achieve a XSS using that method.
The only thing that could be counted as an "insufficient fix" here is the possibility to use "data:" URI's with "Log.entryAdded" like this:
`url: "data:text/html;base64,PHNjcmlwdD4KYWxlcnQoZG9jdW1lbnQuZG9tYWluKTsKPC9zY3JpcHQ+"` (see attached image: NullOriginXSSlogEntryAdded.PNG) which upon clicked opens a new tab and alert()'s its origin - which is null and thus rendered next to completely useless.

Our vulnerability stems from another websocket method alltogether and not bypassing a fix! :)

## Rationale for decision

"Rationale for this decision:
$1,000 for report of \*\* lower impact web platform privilege escalation. \*\*"

The rationale given isnt fully given here: Why is it still considered a lower web platform privilege escalation?
In my mind this is not a "web platform privilege escalation" but rather "Site Isolation bypass / UXSS".

But let's suppose it is a "web platform privilege escalation" - is it really of 'lower' impact?
Wouldnt that make the severity s3 and not s2? Comparing our vulnerability to [5] it has already had its severity lowered from 's1' to 's2'.
By looking into the policy [3] it seems like all the nessisary characteristics for a high-quality report has been met as well as a high impact.

Looking at [4] , I can see that `Mitigated security bugs are eligible for VRP rewards, but at a reduced reward amount.`
In [4] this is stated for memory corruption vulnerabilities rather than the "Other vulnerability classes" - but obviously(?) this applies here as well?

So even though if it is classified as an "insufficient fix" (#30) - it still leads to the same result which is uXSS + more impacts.

The steps to reproduce is also shortened (via extension), increasing the chances for a victim to be exploited.
The lure to the victim can also be even more improved as a quick example see attached file: extensionFishExample.png.

# For future reference

For future vulnerability research; any bypass to a previous issue will have rewards cut? By how much?
As this is not explicitly mentioned in the policy I would very much like to know how this is decided.

Also since this was vulnerable in stable, shouldnt this get a CVE issued as well?

I fully realize that the discretion is yours, and I agree that its not a '0-click uXSS' either - there are at a minimum 2 steps to UXSS.
I really want to understand the decision taken, as I think the decision is based upon pointing out a bypassable fix - which isnt the case.

## Another POC

To prove even more impact, there's also the possibillity to gain access to a victims screen, keyboard, mouse, and clipboard by using the XSS on '<https://remotedesktop.google.com/support>'.

The Attack Scenario: Access-Code theft from "remotedesktop.google.com/support" for RCE on victim's computer.

Precondition: The victim uses Chrome and has the Chrome Remote Desktop native host installed.

Step 1: Victim installs extension (or does the drag-n-drop)

Step 2:
Double click to get UXSS'ed

Step 3:
User presses 'OK' on the share dialog

After the XSS is triggered the user is redirected to '<https://remotedesktop.google.com/support>'.
Here the script is forcing an 'access-code' generation and sends this to our server.
Attacker uses this access-code to connect to the victims computer and execute any command (RCE).

Locales here is set to Swedish (see remoteDesktopPoC.js.txt), changing it to English would be very arbitrary.

[1]
<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules>

[2]
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/ui/legacy/components/utils/Linkifier.ts;l=533;drc=aec1575a78abeec098d606c3c738215ca874b3b4>

[3]
<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#report-quality>

[4]
<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts-for-mitigated-security-bugs>

[5]
<https://issues.chromium.org/issues/40942152>

### am...@chromium.org (2025-06-12)

Hello,

There’s a lot to respond to here, so I’ll do my best in responding to all the points and questions.

> As pointed out in #30: "and the core aspect of this report was pointing out an insufficient fix."
> This is incorrect. These are different vulnerabilites and I think some confusion is here. We make use of "Network.webSocketCreated" which had a missing check for a "javascript:" URI's thus enabling the XSS.

While there are different visibilities, the root cause here was an insufficient fix in the URL scheme checks in dev tools.
While a single bug can result in exploitation from multiple vectors, we reward for the single issue and root cause, not for the multiple types of outcomes for the single issue.

And while the vulnerability didn’t stem from bypassing the fix, the root cause itself was based on an insufficient fix for a previous issue.

> The rationale given isnt fully given here: Why is it still considered a lower web platform privilege escalation? In my mind this is not a "web platform privilege escalation" but rather "Site Isolation bypass / UXSS".
> But let's suppose it is a "web platform privilege escalation" - is it really of 'lower' impact? Wouldnt that make the severity s3 and not s2? Comparing our vulnerability to [5] it has already had its severity lowered from 's1' to 's2'. By looking into the policy [3] it seems like all the nessisary characteristics for a high-quality report has been met as well as a high impact.

> The rationale given isnt fully given here: Why is it still considered a lower web platform privilege escalation? In my mind this is not a "web platform privilege escalation" but rather "Site Isolation bypass / UXSS".

Given there were multiple issues here, we went with web platform privilege escalation, because that fit more discretely than UXSS, because at the end of the day to achieve the XSS this is significantly mitigated with many preconditions to exploit. The likely hood of a successful exploitation of XSS requires a lot of tricking a person in a way that does not seem feasible in a real world scenario.

> But let's suppose it is a "web platform privilege escalation" - is it really of 'lower' impact? Wouldnt that make the severity s3 and not s2? Comparing our vulnerability to [5] it has already had its severity lowered from 's1' to 's2'. By looking into the policy [3] it seems like all the nessisary characteristics for a high-quality report has been met as well as a high impact.

Not necessarily. There do exist lower-impact medium severity bugs. There is a spectrum of issues that fall into each severity level, and exploitability, potential for attacker control, and exploitation preconditions absolutely do impact our considerations regarding the security impact and reward. And while a report can be high quality, impact plays a heavy factor in reward decisions.

Because at the end of the day we do not want to create a overly weighted incentive for overly detailed reports of lower impact issues that would result in high rewards than solid reports of deeper, more impactful and exploitable bugs.

In this case, we did not backmerge the fix for this issue, and one of the reasons for that was the lower potential for exploitation for the scenarios presented.

And, in this regard, if we concurred on classifying this in the category of UXSS / site isolation bypass, the reward would still be the same given the number of steps and non-standard workflows a user would need to be coerced into engaging with and directly with dev tools to make exploitation possible.

> Looking at [4] , I can see that Mitigated security bugs are eligible for VRP rewards, but at a reduced reward amount. In [4] this is stated for memory corruption vulnerabilities rather than the "Other vulnerability classes" - but obviously(?) this applies here as well?

While we do not have a separate table for mitigated bugs, we do have a separate categories for impact and quality in the `other vulnerability classes` section, with each cell consisting of the language “up to”. This means that rewards issued may not meet the threshold of the reward in a particular column and row combination.

This is explained in the language following the `other vulnerability classes table`.

`Reward amounts for security bugs in these classes will be determined based on report quality and bug impact` followed by examples for each class per impact tier, and closed by the following, `Bugs with significant preconditions to exploit and no demonstrable risk to a user are not eligible for a Chrome VRP reward.`

> For future vulnerability research; any bypass to a previous issue will have rewards cut? By how much? As this is not explicitly mentioned in the policy I would very much like to know how this is decided.

Again, the reward amount was not decided basely solely on the fact of the that this issue demonstrated an insufficient fix of a previous issue, but that the vectors to exploitation were highly mitigated. These decisions were based on the POCs and reproduction scenarios provided in the report and follow up. This are all very involved scenarios that require a heavy level of direct UI interactions.

And while we do not have language strictly regarding issues that are based on reporting insufficient fixes of previous security bugs, we have taken this into consideration with other reports of similar issues, with the reward information being a combination of “what new information about the root cause of a vulnerability has been provided” AND the overall security impact and exploitability of the vulnerability being presented.
The overall policy, is however, “the decision whether to grant a reward and the amount of the reward is always determined at the sole discretion of the reward panel.”

And while we try to make fair decisions about each reward, we also know that the reporters of a given issue may not agree with that decision. This is why we have a reassessment policy. And even the outcome is not what is desirable by the reporter, we at least try to explain the rationale.

We have done that here, twice — for both reassessment and explanation about the rationale, both off bug and on it, so we are going to have to consider the matter of this reward decision closed.

We are happy to answer any additional questions you may have, both on or off bug (the preferred vehicle for off-bug questions related to a particular bug or reward decision is [security-vrp@chromium.org](mailto:security-vrp@chromium.org) rather than Discord), but we will not consider this issue for further reward reassessments.

### am...@chromium.org (2025-06-13)

It appears that when this was triaged on 13 March, the `found in` was incorrectly set to M135, which at the time was Beta, rather than stable, despite this issue went back at least to M121. This means that the Security Impact tag was set to Beta and the security fix release and CVE automation did not identify this issue as CVE eligible. 
I've corrected the `found in` and `security impact` as well as added the `relnotes update needed` hotlist. This should get issued a CVE as part of our clean up process to address any orphans. Unfortunately, since that isn't fully automated, it may be a bit more time before that is rectified. Apologies for the inconvenience and thanks for your patience in the meantime.


### ch...@google.com (2025-06-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-06-13)

danilsomsikov: Uh oh! This issue still open and hasn't been updated in the last 85 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-06-13)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $1,000 for report of lower impact web platform privilege escalation + $2,000 patch bonus + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/402791076)*
