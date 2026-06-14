# Security: Read Access Violation on Control Flow at content::devtools::service_worker::ServiceWorkerHandler::UpdateHosts

| Field | Value |
|-------|-------|
| **Issue ID** | [40085334](https://issues.chromium.org/issues/40085334) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>ServiceWorker, Platform>DevTools, UI>Browser>Navigation |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-09-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

After a tab crash occurs (which is probably a non exploitable Read Access Violation near NULL) if we try to navigate to another website then either refresh (or sometimes going to a third website) we get a potentially exploitable browser crash.

**VERSION**  

Chrome Version: 53.0.2785.89 m (64-bit)  

Operating System: Windows 8.1 64bit

**REPRODUCTION CASE**

1. Open 'PoC.html' from local disk (File: URI scheme)
2. Open Dev Console
3. Press the button and go back to the main page after new window opens
4. Expand the 'window' object inside the devtool console.
5. Tab crash occurs
6. Type in the addressbar '<https://www.google.com/SOMETHING>' tab attempts to navigate but is still in crash state
7. To trigger the browser crash, either refresh the page (using the reflesh button and not hitting enter on the addressbar) OR attempt to navigate again to a different location like '<https://www.google.com/THING>'
8. Browser should crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab and browser  

Crash State: Read Access Violation on Control Flow starting at chrome\_7ffaa4260000!content::devtools::service\_worker::ServiceWorkerHandler::UpdateHosts+0x00000000000000c9 (Hash=0xe9460b9e.0x2f6aa713)

I attached the tab crash and the browser crash dump. Please note that the tab crash signature does vary when I reproduce this.

## Attachments

- [PoC.html](attachments/PoC.html) (text/plain, 212 B)
- [BrowserCrash.log](attachments/BrowserCrash.log) (text/plain, 11.5 KB)
- [TabCrash.log](attachments/TabCrash.log) (text/plain, 11.5 KB)
- [PoC2.html](attachments/PoC2.html) (text/plain, 375 B)
- [PoC3.html](attachments/PoC3.html) (text/plain, 250 B)

## Timeline

### gr...@hotmail.com (2016-09-08)

Note: If browser does not crash, please try to navigate to random websites that are not cached, try things like 'http://GOOGLE.com.' and then 'hello.com' ..etc

It should crash eventually. But I promise you dont have to do it for more than 4 times

### wf...@chromium.org (2016-09-08)

I can repro in 53.0.2785.101 m (64-bit) but not 55.0.2854.0. Investigating.

### wf...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### wf...@chromium.org (2016-09-08)

This seems to have been fixed between these revisions:

You are probably looking for a change made after 404867 (known bad), but no later than 404885 (first known good).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/af2f49b..57b70da?pretty=fuller

could be same root cause as https://crbug.com/chromium/623319. creis can you please investigate. Thanks.

### wf...@chromium.org (2016-09-08)

strange, comments in https://crbug.com/chromium/623319 imply any associated fixes were merged to M53 already. This is confusing. creis - can you diagnose whether I am up the wrong alley or not.

### cr...@chromium.org (2016-09-08)

wfh: I'm not familiar with ServiceWorkerHandler::UpdateHosts.  Do you have a crash ID I could glance at?  (I'm not able to investigate today, but hopefully I can take a look tomorrow.)  CC'ing horo@, since the crash sounds similar to the old https://crbug.com/chromium/508775.  Not sure yet whether my CL helped or not.

[Monorail components: Blink>ServiceWorker]

### wf...@chromium.org (2016-09-08)

the logs in #0 have the stack. I can reliably repro the renderer crash. Not so reliable with the browser one.

### gr...@hotmail.com (2016-09-08)

Here is a crash ID:

Crash ID 12c5e024-6892-44fb-86ac-afeae1dda5f6 (Server ID: 4ed5d16e00000000)


And just to be safe, here are the tab crashes leading up to it.


Crash ID cdbb46ed-0796-4e0a-9ea5-39000d1b5544 (Server ID: 9d02eb3500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:58 PM

Provide additional details

Crash ID 1b2d5da6-dbd2-4caa-b31f-f8868dfda865 (Server ID: e09eeb3500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:57 PM

Provide additional details

Crash ID 56858899-f9cf-4b2a-bfe3-a637d5c17578 (Server ID: 0c51eb3500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:55 PM

Provide additional details

Crash ID c2028291-f075-4043-a143-c22ac810c43d (Server ID: f5e2e91500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:53 PM

Provide additional details

Crash ID a64892e4-7c4f-413f-9a84-543b328009b5 (Server ID: 5be4eb3500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:51 PM

Provide additional details

Crash ID 98bffde9-75cd-4567-b1cf-b84e7efe8ede (Server ID: 2a65d16e00000000)

Automatically reported Thursday, September 8, 2016 at 6:24:48 PM

Provide additional details

Crash ID 336b679f-e6df-4c97-bc0d-7ecda3261e7e (Server ID: e3c9eb3500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:44 PM

Provide additional details

Crash ID 39894a56-438e-46dd-aaf3-4551d55cffa8 (Server ID: 68c8eb3500000000)

Automatically reported Thursday, September 8, 2016 at 6:24:39 PM

Provide additional details

### cr...@chromium.org (2016-09-08)

Thanks, that helps.  We're crashing while notifying observers in DidCommitProvisionalLoadForFrame.  Not sure whether the RenderFrameHost, ServiceWorkerHandle, or RenderFrameDevToolsAgentHost is gone at first glance.  I'll note that it's possible a previous WebContentsObserver might be deleting the RFH and we just crash when getting to this observer afterward.

I'll see if I can repro locally tomorrow.

### cr...@chromium.org (2016-09-09)

I've looked into this and there's probably something we still need to fix in the browser process.

I can repro it on 53.0.2785.89, as long as I use different URLs in steps 6 and 7.  I can't repro it in M55.

The renderer crash in step 5 is https://crbug.com/chromium/534672 (blink::V8WrapperInstantiationScope::securityCheck), which jochen@ fixed.  Unfortunately, there's no CL listed on that bug, so I'm not sure yet which CL fixed it.  (That means I can't revert the CL on trunk to try to repro the bug there.)

The renderer crash in step 6 is a separate crash from https://crbug.com/chromium/629636 (blink::V8InspectorSessionImpl::findInjectedScript), which eostroukhov@ fixed in r406456 (M54).  Interestingly, this crash only seems to happen if we do steps 1-5, and not if the renderer crashes in any other way (e.g., killed via task manager, visited chrome://crash, etc).

We may want to merge the fixes for both of those renderer crashes to M53 if possible, but we still shouldn't crash the browser process in step 7.  I'm concerned about a bad WebContentsObserver, as noted in https://crbug.com/chromium/644963#c9.  (CC'ing dcheng@ and nick@, since we've seen WCOs incorrectly delete the RenderFrameHost before while we're still iterating over observers.)

jochen@: Can you let me know which CL fixed https://crbug.com/chromium/534672?  If so, I can revert that and r406456 locally to try to catch the browser crash in a debugger.

[Monorail components: Platform>DevTools]

### cr...@chromium.org (2016-09-10)

I took a guess that r404874 was the fix for https://crbug.com/chromium/534672 (since it was in wfh's bisect in https://crbug.com/chromium/644963#c4), but unfortunately I still can't repro the crash on trunk after reverting it locally.  (I'll note that it was hard to revert because of conflicts with yukishiino's r413132, and eostroukhov's r406456 was hard to revert due to conflicts with dgozman's r409131 and other CLs from https://crbug.com/chromium/635948.)

Jochen, can you take a look at how to recreate these renderer crashes and catch the browser crash in a debugger?  Feel free to assign back to me if you find a way for me to repro it.

### gr...@hotmail.com (2016-09-10)

Minimized testcase for the tab crash from step 1-5:

This PoC does not require you to be within File: uri scheme. 

Open it from HTTP and follow instructions.

### gr...@hotmail.com (2016-09-10)

A smaller PoC. Removed the need to open a new URL, replaced with an iframe.

### cr...@chromium.org (2016-09-10)

I ended up doing an M53 debug build and was able to repro the crash.  There were a bunch of DCHECKs hit along the way, but the end result is that we get to ServiceWorkerHandler::UpdateHosts via RenderFrameDevToolsAgentHost::DidCommitProvisionalLoadForFrame, when ServiceWorkerHandler's render_frame_host_ is a stale pointer to an RFH that has already been deleted.  (It's a different RFH than the one passed into DidCommitProvisionalLoadForFrame.)

pfeldman: It looks like you added the render_frame_host_ pointer in r320555 (https://codereview.chromium.org/1003263002/).  Can you take a look at why it isn't getting cleared when the RenderFrameHost is deleted?  Maybe that class should be notified when the RFH goes away?

I'm guessing this is probably still reachable even though the two renderer crash bugs used in the original repro steps have been fixed.

### cr...@chromium.org (2016-09-19)

pfeldman@: Can you take a look or find an owner for this?  This is a use-after-free in the browser process.  I'm rating it high severity because it's memory corruption in the browser process that requires user interaction (per https://dev.chromium.org/developers/severity-guidelines).

### gr...@hotmail.com (2016-09-19)

You said high severity but its rated medium? Can you clarify please?

### cr...@chromium.org (2016-09-20)

My mistake.  After checking the guidelines, I revised it upward in the description but forgot to update the label.

dgozman@, maybe you could help triage or find an owner?  (Not sure if pfeldman@ is out.)

### sh...@chromium.org (2016-09-20)

[Empty comment from Monorail migration]

### dg...@chromium.org (2016-09-21)

I wasn't able to reproduce the problem without building M53, but I think there could be a bug in how we handle crashed tab. I'll try to come up with a patch and test.

### dg...@chromium.org (2016-09-22)

After experimenting with different scenarios, I'm not able to find any issues. I've added CHECKs everywhere that we don't use stale RFHI, and it never triggers.

On a side note, I've found strange navigation behavior:
- Go to google.com.
- Open task manager.
- Navigate to a slow to commit page (e.g. with sleep(10) on the web server).
- End process of google.com in task manager.
- Wait for the page to commit. It's now there (I can see correct DOM in DevTools), but the tab still shows crashed page.
- Go to omnibox, hit enter. Page reloads (e.g. DOM updates in DevTools), but the tab still shows crashed page.


### cr...@chromium.org (2016-09-22)

https://crbug.com/chromium/644963#c20: Nice find!  Can you file a separate bug for that and assign it to me?

I looked at the M53 build in a debugger to learn more about this UaF, and I think there is a bug in how the RFH is tracked.  Here's more reliable repro steps:

1) Open repro page.
2) Open DevTools.
3) Click button and go back to first tab.
4) Expand "window" object in DevTools console.  Tab crashes (https://crbug.com/chromium/534672).
5) Navigate to chromium.org in address bar.  Tab crashes again (https://crbug.com/chromium/629636).
   (We're setting pending_ to the chromium.org RFH in RenderFrameHostChanged here.)
6) Hit enter in the address bar.  Tab crashes again.
   (AboutToNavigateRenderFrame sets pending_ to the chromium.org RFH here.)
7) Hit Ctrl+R to reload.

At this point, we get to RenderFrameHostChanged and pending_ points to old_host.  new_host says file:/// for GetSiteInstance()->GetSiteURL(), which suggests that we're reloading the original page?  (Weird; maybe that's because DevTools is open and handles reloads?)  The fact that pending_ points to old_host causes the DCHECK to fail in debug builds.  We don't update pending_, which means it stays pointing to old_host, which is about to be deleted.  When we get to ServiceWorkerHandler::UpdateHosts, the RFH is stale and we get the UaF.

Pavel was suggesting removing the "return" from RenderFrameDevToolsAgentHost::FrameDeleted, but we never get there for this bug.  It looks like the problem is that RenderFrameHostChanged leaves pending_ set to old_host_, just before committing it (and as that RFH gets deleted).

I'm guessing that these steps expose a case that RenderFrameDevToolsAgentHost is missing, where we should have avoided setting pending_ to old_host.  (We could just handle it in RenderFrameHostChanged, but that might be papering over the bug.  I'd rather upgrade that DCHECK to a CHECK and make sure we don't get into that state.)

I do worry this bug could be exploited with a different set of crashes post-M53, so I think it's worth fixing.  Can you get a build working to try out a fix?

### dg...@chromium.org (2016-09-23)

I was able to repro on manual 53 build by making chromium.org tab crash manually (https://crbug.com/chromium/629636 does not happen for me).

The problem here is:
- RFDTAH gets crash notification;
- AboutToNavigateRenderFrame happens with the same RFH when I hit enter on the same url - here we set pending but not current;
- page crashes again, so we never get commit;
- on reload we get new RFH, but stale one is left in pending.

I have a fix in mind, but writing a test here is tricky: somehow I have to crash the page so that RFH is reused on second crash. This is not the case for chrome://kill.

### ni...@chromium.org (2016-09-23)

content::CrashTab() might give you a different behavior from a navigation to "chrome://kill". It should be pretty close to what happens in a real crash.

### bu...@chromium.org (2016-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f07d611e4c7c7e0b38521119c42166b6104bba1b

commit f07d611e4c7c7e0b38521119c42166b6104bba1b
Author: dgozman <dgozman@chromium.org>
Date: Thu Sep 29 00:48:01 2016

[DevTools] Avoid current_ and pending_ being the same host in RenderFrameDevToolsAgentHost.

This happens when we resue RenderFrameHost after crash.
The fix is to commit immediately to avoid pending. This is safe because
we don't even have two RenderFrameHosts.

BUG=644963

Review-Url: https://codereview.chromium.org/2366773003
Cr-Commit-Position: refs/heads/master@{#421697}

[modify] https://crrev.com/f07d611e4c7c7e0b38521119c42166b6104bba1b/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/f07d611e4c7c7e0b38521119c42166b6104bba1b/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/f07d611e4c7c7e0b38521119c42166b6104bba1b/content/browser/devtools/render_frame_devtools_agent_host.h


### dg...@chromium.org (2016-09-30)

With the fix landed, let's wait a bit for crashes/bugs on canary and merge to M54. Not sure it's worth to merge to M53 at this point.

### cr...@chromium.org (2016-10-04)

Thanks for the fix!  For security bugs, we mark them fixed as soon as the CL lands on trunk, and we can track merges separately.  It's too late for M53, but merging to M54 might be an option.

Can you check whether any resulting crashes have happened?  Do you think this would be a safe CL to request an M54 merge for?

### dg...@chromium.org (2016-10-04)

Fix looks pretty safe, and I haven't found any related crashes. Let's merge to M54 to give it some time there.

### di...@chromium.org (2016-10-04)

[Automated comment] Less than 2 weeks to go before stable on M54, manual review required.

### sh...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

### bu...@google.com (2016-10-06)

SGTM, plus it's an externally reported security bug so I'd like to take it.  Approved for merging into M54

### bu...@chromium.org (2016-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a5593d910bbdacce805ac0e5bd4a139799c7123b

commit a5593d910bbdacce805ac0e5bd4a139799c7123b
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Thu Oct 06 23:42:33 2016

Merge to 2840 "[DevTools] Avoid current_ and pending_ being the same host in RenderFrameDevToolsAgentHost."
> [DevTools] Avoid current_ and pending_ being the same host in RenderFrameDevToolsAgentHost.
>
> This happens when we resue RenderFrameHost after crash.
> The fix is to commit immediately to avoid pending. This is safe because
> we don't even have two RenderFrameHosts.
>
> BUG=644963
>
> Review-Url: https://codereview.chromium.org/2366773003
> Cr-Commit-Position: refs/heads/master@{#421697}
(cherry picked from commit f07d611e4c7c7e0b38521119c42166b6104bba1b)
TBR=pfeldman

Review URL: https://codereview.chromium.org/2400863002 .

Cr-Commit-Position: refs/branch-heads/2840@{#673}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/a5593d910bbdacce805ac0e5bd4a139799c7123b/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/a5593d910bbdacce805ac0e5bd4a139799c7123b/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/a5593d910bbdacce805ac0e5bd4a139799c7123b/content/browser/devtools/render_frame_devtools_agent_host.h


### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

The panel awarded $500 for this bug, noting it is mitigated by the amount of user interaction required.  Thanks for the report!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2016-10-16)

[Comment Deleted]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a5593d910bbdacce805ac0e5bd4a139799c7123b

commit a5593d910bbdacce805ac0e5bd4a139799c7123b
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Thu Oct 06 23:42:33 2016

Merge to 2840 "[DevTools] Avoid current_ and pending_ being the same host in RenderFrameDevToolsAgentHost."
> [DevTools] Avoid current_ and pending_ being the same host in RenderFrameDevToolsAgentHost.
>
> This happens when we resue RenderFrameHost after crash.
> The fix is to commit immediately to avoid pending. This is safe because
> we don't even have two RenderFrameHosts.
>
> BUG=644963
>
> Review-Url: https://codereview.chromium.org/2366773003
> Cr-Commit-Position: refs/heads/master@{#421697}
(cherry picked from commit f07d611e4c7c7e0b38521119c42166b6104bba1b)
TBR=pfeldman

Review URL: https://codereview.chromium.org/2400863002 .

Cr-Commit-Position: refs/branch-heads/2840@{#673}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/a5593d910bbdacce805ac0e5bd4a139799c7123b/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/a5593d910bbdacce805ac0e5bd4a139799c7123b/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/a5593d910bbdacce805ac0e5bd4a139799c7123b/content/browser/devtools/render_frame_devtools_agent_host.h


### sh...@chromium.org (2017-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/644963?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>ServiceWorker, Platform>DevTools, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085334)*
