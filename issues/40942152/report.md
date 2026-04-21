# Security: Attacker Can Execute Arbitrary JavaScript Code in the Highly Privileged "devtools://devtools" Origin

| Field | Value |
|-------|-------|
| **Issue ID** | [40942152](https://issues.chromium.org/issues/40942152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2023-11-13 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**  

I have identified an XSS vulnerability in the highly privileged Chrome DevTools Frontend origin (devtools://devtools). This vulnerability exists in any DevTools frontend page, in the filtering of JavaScript URIs when handling Log.EntryAdded events.  

The vulnerability can be exploited by making the victim navigate to a particular URL, which makes the DevTools frontend connect to the attacker's WebSocket server (using the "ws" or "wss" query parameters). The attacker's WebSocket servers then sends a malicious Log.EntryAdded event in that connection, with a JavaScript URI in the "url" property. The handler for that event does try to block JavaScript URIs, but an attacker can bypass that by inserting either a \n, \r, or \t byte into the scheme of the URI (e.g "javascr\tipt:alert(origin)").  

Then, a message will be printed to the console. prompting the user to click on a legitimate-looking link, which when clicked on, executes the attacker's JavaScript code. An example of this can be seen in the video PoC.  

If you try to reproduce this vulnerability in the devtools://devtools/bundled/devtools\_app.html endpoint, the XSS will get blocked by the CSP of the page, due to the removal of the "unsafe-inline" directive from the "script-src" in 2020. However, the vulnerability can still be exploited in the devtools://devtools/bundled/integration\_test\_runner.html endpoint, which was missed during the change.

The following URL can be used to exploit this XSS vulnerability: devtools://devtools/bundled/integration\_test\_runner.html?debugFrontend=true&inspected\_test=[https://example.com&ws=[URL](https://example.com&ws=%5BURL) of attacker WebSocket server, without the protocol].  

This isn't the final exploit URL though, as an attacker can't simply redirect a victim to this URL, as it contains the "devtools" protocol.  

I have however found a way to make a victim navigate to that devtools URL, by using a drag and drop interaction. An example of a malicious site which uses that interaction to open the exploit URL is included in the reproduction case.

After triggering the XSS, the exploit script gets a reference to the DevToolsAPI object using the following steps (I am not sure if this is meant to be possible):

1. The script opens "devtools://devtools/bundled/devtools\_app.html" in a new tab (window.opener.open is used in order to save a click from being necessary), and saves a reference to it in the "w" variable. At this stage, w.DevToolsAPI is undefined, as the window loaded with an opener property set
2. The script sets w.opener to null
3. The script reloads the window by calling w.location.reload()
4. The script waits for the window to load again
5. As the window was loaded without an opener property set, w.DevToolsAPI is now defined, and the exploit script can use it.

After getting access to the DevToolsAPI object, the script then uses it to read local files. I am fairly certain that a higher impact can be achieved using this API (as demonstrated in <https://microsoftedge.github.io/edgevr/posts/attacking-the-devtools/>), and I will continue to investigate this.  

Finally, the opened window is closed, and the extracted information is parsed and displayed. As the CSP which the exploit script runs under is very permissive, exfiltrating this information would be trivial.

**VERSION**  

Chrome Version: 119.0.6045.124 stable  

Operating System: Windows 11 (also tested on Linux)

**REPRODUCTION CASE**  

I have attached all of the files needed to run the HTTP and WebSocket attack servers. Please follow these steps to run them:

1. Download all of the attached files (except the video PoC) into a single folder
2. Navigate to that folder and run "npm install"
3. Run the following command to start the servers: "npx supervisor node attack-servers.mjs". This will automatically restart the servers if they encounter an error.

Steps to Reproduce as the Victim:

1. Navigate to <http://localhost:9123/#devtools://devtools/bundled/integration_test_runner.html?ws=127.0.0.1:6123&panel=console&inspected_test=https://example.com&debugFrontend=true> (the attacker's http server)
2. Drag the installer icon into a new tab, as shown in the attached video PoC
3. Notice that the potentially suspicious "javascript:" URI is trimmed in the "update chrome now" link, due to the many "\r" bytes preceding it, and click on the link
4. Wait for the exploit to finish (should take about 0.5 seconds, as I was generous with the wait times), and notice the leaked file information.

**CREDIT INFORMATION**  

Reporter credit: Matan Berson (<https://twitter.com/MtnBer>, <https://matanber.com>)

Cheers,  

Matan.

## Attachments

- [attack-servers.mjs](attachments/attack-servers.mjs) (application/octet-stream, 1.8 KB)
- [devtools-xss.js](attachments/devtools-xss.js) (text/plain, 1.5 KB)
- [index.html](attachments/index.html) (text/plain, 2.0 KB)
- [installer_drag.png](attachments/installer_drag.png) (image/png, 6.6 KB)
- [update_link.png](attachments/update_link.png) (image/png, 28.9 KB)
- [package.json](attachments/package.json) (text/plain, 138 B)
- [devtools-xss.js](attachments/devtools-xss.js) (text/plain, 870 B)

## Timeline

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-11-13)

Thank you for the report and thank you for the effort put into the PoC! While this is a fair number of user gestures, the drag and drop makes this much smoother than it otherwise would be.

I think we have several security issues here:
1. The handler for Log.EntryAdded attempts to filter javascript: schemes, but has incomplete coverage
2. The missing CSP in devtools://devtools/bundled/integration_test_runner.html
3. The ability to drag-and-drop to a URL that is supposed to be hard for a site to generate

And maybe:
4. The technique you use to get the DevToolsAPI object. Like you, I'm not sure if that's supposed to be possible.

Is that comprehensive? Is there anything else you bypassed along the way we should be fixing?

caseq@, dsv@ - can you take a look? I'm fairly certain you would be the owners for 1, 2, and 4. Let me know if 3 is outside your scope and I can try to find an owner for it as well.

[Monorail components: Platform>DevTools]

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### bm...@chromium.org (2023-11-14)

I cannot reproduce the issue with Chrome Stable (119) or Dev (121) on Linux.

However, I can partly reproduce this with a self-build Chromium ToT (121) on Linux (the XSS JS uses a Windows path, so this would need to be changed for Linux to make sense).

I'm a bit puzzled that we include the integration_test_runner.html (and maybe other test-only artifacts) in the final production Chrome build at all.

Danil, please take a look. I already briefly discussed with Simon, who'd be happy to help.

### ad...@gmail.com (2023-11-14)

Yes Drubery, the vulnerabilities which you have listed are comprehensive.

### ha...@google.com (2023-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@gmail.com (2023-11-15)

This issue can easily be escalated to universal XSS, by running the following payload in the privileged DevTools window:

const URL = "https://example.com";
InspectorFrontendHost.setInjectedScriptForOrigin(URL, "console.log('Script run in ' + origin)//");
const ifr = document.createElement("iframe");
ifr.src = URL;
document.body.appendChild(ifr)

I will provide an updated exploit script shortly.

### ad...@gmail.com (2023-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/081ba89b58575aae4bdb8fb84f71375c53bbb82e

commit 081ba89b58575aae4bdb8fb84f71375c53bbb82e
Author: Danil Somsikov <dsv@chromium.org>
Date: Thu Nov 16 07:47:52 2023

Add a function to check URL scheme reliably and use it everywhere.

Bug: 1501835
Change-Id: I94632bf91f39a66152e2ee9909834db169ed07aa
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5028164
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>

[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/persistence/NetworkPersistenceManager.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/persistence/PersistenceUtils.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/ui/legacy/components/utils/Linkifier.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/logs/NetworkLog.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/core/sdk/DebuggerModel.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/core/sdk/Target.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/core/common/ParsedURL.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/core/sdk/Script.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/application/components/BackForwardCacheView.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/console/ConsoleContextSelector.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/issues_manager/CookieIssue.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/test/unittests/front_end/ui/components/ChromeLink_test.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/timeline/TimelineUIUtils.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/bindings/ResourceMapping.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/coverage/CoverageModel.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/ui/components/chrome_link/ChromeLink.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/application/preloading/components/PreloadingDisabledInfobar.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/core/sdk/NetworkRequest.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/core/sdk/SourceMap.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/persistence/PersistenceActions.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/recorder/models/RecordingPlayer.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/snippets/ScriptSnippetFileSystem.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/persistence/Automapping.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/models/bindings/DebuggerLanguagePlugins.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/application/components/BounceTrackingMitigationsView.ts
[modify] https://crrev.com/081ba89b58575aae4bdb8fb84f71375c53bbb82e/front_end/panels/console/ConsoleFormat.ts


### ds...@chromium.org (2023-11-16)

1. DevTools renderer is privileged, regardless of wether it is running in a DevToolsWindow or not. We might want to reconsider this and only expose UI bindings to the frontend running with a DevToolsWindow.
2. Until then, we have are handling untrusted input in a privileged context and the only adequate fix I can think of is the CL above with a more robust URL sanitization.
Once we get untrusted code to run in a privileged context, everything is lost, regardless of whether we expose integration test runner or not and if it has CSP or not.

### ds...@chromium.org (2023-11-16)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-11-16)

+creis, dcheng

Even though this is fixed, exploit relies on devtools:// URL being draggable from an untrusted renderer to the tab strip. We probably don't want that (https://crbug.com/1142410#c5) Could you please help me route this properly.

### [Deleted User] (2023-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-16)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-17)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-19)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-11-20)

1. https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5028164
2. Yes
3. Yes
4. No
5. No

### [Deleted User] (2023-11-20)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-11-21)

1. https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5028164
2. Yes
3. Yes
4. No
5. No

### [Deleted User] (2023-11-21)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2023-11-22)

[vrp panel] is there any follow-on action required based on https://crbug.com/chromium/1501835#c13?

### [Deleted User] (2023-11-22)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M119. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M120. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-22)

Congratulations, Matan! The Chrome VRP Panel has decided to award you $6,000 for this report. The reward amount was decided on based on the significant preconditions to exploit this issue in a real-world scenario as well as the mitigated impact of the aspects of the scenario that require direct access to devtools. We did consider this a very thorough and high-quality report and a solid POC, so we definitely wanted to acknowledge and reward for that. 

A member for our finance team will be in touch with you soon to arrange payment. Thank you for you efforts in discovering and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-11-22)

Hi dsv@, thanks for the great work on getting this resolved. Due to change in adding an entirely new function and not being confident that Canary data is going to be super informative for this change, combined with the timing of release freeze followed immediately by 119 Stable channel update and 120 Stable Cut and Early Stable release, I'm veering on the side of caution and suggest not backmerging https://crrev.com/c/5028164. 
Please let me know if you have different thoughts/considerations. We can chat / reassess on Monday, but for now I am going to remove the merge review labels. 

### am...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1501835?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### cs...@gmail.com (2024-07-12)

deleted

### ji...@gmail.com (2025-10-01)

Great

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942152)*
