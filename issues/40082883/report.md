# Browser crash in improper destruction of select file dialog (mac)

| Field | Value |
|-------|-------|
| **Issue ID** | [40082883](https://issues.chromium.org/issues/40082883) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Internals |
| **Platforms** | Mac |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-08-25 |
| **Bounty** | $500.00 |

## Description

Branched off from https://crbug.com/chromium/45400 since it was a different issue.
credit: Serg

Reproducer steps
1. Go to data:text/html,<script>w=open('data:text/html,<input type="file" 
id="f"><script>f.click()<\/script>');setTimeout('w.close()',1000)</script>
2. Wait until the file picker dialog appears
3. Try to close the dialog

It is reproducing as SecSeverity Critical.

Program received signal EXC_BAD_ACCESS, Could not access memory.
Reason: KERN_INVALID_ADDRESS at address: 0x64616286
0x97acded7 in objc_msgSend ()
(gdb) bt
#0  0x97acded7 in objc_msgSend ()
#1  0x07677230 in ?? ()
#2  0x9144afd3 in -[NSNavDataSource displayStateForNode:] ()
#3  0x914458db in -[NSNavBrowserDelegate browser:willDisplayCell:atRow:column:] ()
#4  0x91128bbb in -[NSBrowser _sendDelegateWillDisplayCell:atRow:column:] ()
#5  0x911288ec in -[NSTableView _delegateWillDisplayCell:forColumn:row:] ()
#6  0x910a59f5 in -[NSTableView preparedCellAtColumn:row:] ()
#7  0x9173c5bf in -[NSNavBrowserTableView preparedCellAtColumn:row:] ()
#8  0x910a4e04 in -[NSTableView _dirtyVisibleCellsForKeyStateChange] ()
#9  0x910a47e2 in -[NSTableView _windowChangedKeyState] ()
#10 0x97435ff0 in CFArrayApplyFunction ()
#11 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#12 0x97435ff0 in CFArrayApplyFunction ()
#13 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#14 0x97435ff0 in CFArrayApplyFunction ()
#15 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#16 0x97435ff0 in CFArrayApplyFunction ()
#17 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#18 0x97435ff0 in CFArrayApplyFunction ()
#19 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#20 0x97435ff0 in CFArrayApplyFunction ()
#21 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#22 0x910a42af in -[NSControl _windowChangedKeyState] ()
#23 0x91280964 in -[NSBrowser _windowChangedKeyState] ()
#24 0x97435ff0 in CFArrayApplyFunction ()
#25 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#26 0x97435ff0 in CFArrayApplyFunction ()
#27 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#28 0x910a44e3 in -[NSSplitView _windowChangedKeyState] ()
#29 0x97435ff0 in CFArrayApplyFunction ()
#30 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#31 0x97435ff0 in CFArrayApplyFunction ()
#32 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#33 0x97435ff0 in CFArrayApplyFunction ()
#34 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#35 0x97435ff0 in CFArrayApplyFunction ()
#36 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#37 0x97435ff0 in CFArrayApplyFunction ()
#38 0x90fd42d9 in -[NSView _windowChangedKeyState] ()
#39 0x910a425e in -[NSFrameView _windowChangedKeyState] ()
#40 0x90fd3fcb in -[NSWindow _setFrameNeedsDisplay:] ()
#41 0x911636fc in endKeyAndMain ()
#42 0x9100ad8b in -[NSApplication sendEvent:] ()
#43 0x0094adfe in -[CrApplication sendEvent:] (self=0x9f07210, _cmd=0x9176ea98, event=0x9f38210) at /Users/aarya/chrome/375/src/base/chrome_application_mac.mm:43
#44 0x90f9f5bb in -[NSApplication run] ()
#45 0x0093762a in base::MessagePumpNSApplication::DoRun (this=0x7611c80, delegate=0xbfffed38) at /Users/aarya/chrome/375/src/base/message_pump_mac.mm:677
#46 0x00937c19 in base::MessagePumpCFRunLoopBase::Run (this=0x7611c80, delegate=0xbfffed38) at /Users/aarya/chrome/375/src/base/message_pump_mac.mm:213
#47 0x009693cc in MessageLoop::RunInternal (this=0xbfffed38) at /Users/aarya/chrome/375/src/base/message_loop.cc:205
#48 0x009693e7 in MessageLoop::RunHandler (this=0xbfffed38) at /Users/aarya/chrome/375/src/base/message_loop.cc:177
#49 0x0096944b in MessageLoop::Run (this=0xbfffed38) at /Users/aarya/chrome/375/src/base/message_loop.cc:155
#50 0x001abea6 in (anonymous namespace)::RunUIMessageLoop (browser_process=0x760f2c0) at /Users/aarya/chrome/375/src/chrome/browser/browser_main.cc:182
#51 0x001adb28 in BrowserMain (parameters=@0xbffff618) at /Users/aarya/chrome/375/src/chrome/browser/browser_main.cc:1174
#52 0x00008c09 in ChromeMain (argc=3, argv=0xbffff780) at /Users/aarya/chrome/375/src/chrome/app/chrome_dll_main.cc:814
#53 0x00001f52 in main (argc=3, argv=0xbffff780) at /Users/aarya/chrome/375/src/chrome/app/chrome_exe_main.mm:16

## Timeline

### in...@chromium.org (2010-08-25)

[Empty comment from Monorail migration]

### lc...@gmail.com (2010-08-25)

I casually ran into the crash on closing the file picker on Chrome dev a number of times; I thought this is a known problem?

### ro...@chromium.org (2010-08-25)

7.0.503.0 (Official Build 57033) dev

This crash is reproducible with latest dev release. Stack trace we get is different than the given stack trace .

Steps:
1. Navigate to given script.
2. Cancel the file select dialog.

Result:
- Chrome crashes. 

Crash reports:
http://crash/reportdetail?reportid=15c4b5c7b908c059
http://crash/reportdetail?reportid=a68135be1931dfe4


Stack trace:
0x0026de24 	[Google Chrome Framework 	- objc_zombie.mm:211] 	ZombieObjectCrash
0x0026df02 	[Google Chrome Framework 	- objc_zombie.mm:249] 	-[CrZombie forwardingTargetForSelector:]
0x986e8415 	[CoreFoundation 	+ 0x0007a415] 	__NSGetForwardingTarget
0x986e838f 	[CoreFoundation 	+ 0x0007a38f] 	__forwarding_prep_0___
0x95f07309 	[AppKit 	+ 0x00553309] 	-[NSSavePanel _didEndSheet:returnCode:contextInfo:]
0x95bda1e8 	[AppKit 	+ 0x002261e8] 	-[NSApplication endSheet:returnCode:]
0x95f0066b 	[AppKit 	+ 0x0054c66b] 	-[NSSavePanel _cancelAndClose]
0x95a3af1d 	[AppKit 	+ 0x00086f1d] 	-[NSApplication sendAction:to:from:]
0x001e2153 	[Google Chrome Framework 	- chrome_browser_application_mac.mm:299] 	-[BrowserCrApplication sendAction:to:from:]
0x95b1a698 	[AppKit 	+ 0x00166698] 	-[NSControl sendAction:to:]
0x95b16145 	[AppKit 	+ 0x00162145] 	-[NSCell _sendActionFrom:]
0x95b1543c 	[AppKit 	+ 0x0016143c] 	-[NSCell trackMouse:inRect:ofView:untilMouseUp:]
0x95b6aa60 	[AppKit 	+ 0x001b6a60] 	-[NSButtonCell trackMouse:inRect:ofView:untilMouseUp:]
0x95b13e92 	[AppKit 	+ 0x0015fe92] 	-[NSControl mouseDown:]
0x95b11e9b 	[AppKit 	+ 0x0015de9b] 	-[NSWindow sendEvent:]
0x95a2aafe 	[AppKit 	+ 0x00076afe] 	-[NSApplication sendEvent:]
0x00804fa2 	[Google Chrome Framework 	- chrome_application_mac.mm:43] 	-[CrApplication sendEvent:]
0x959be5ba 	[AppKit 	+ 0x0000a5ba] 	-[NSApplication run]
0x008478ac 	[Google Chrome Framework 	- message_pump_mac.mm:677] 	base::MessagePumpNSApplication::DoRun
0x00847039 	[Google Chrome Framework 	- message_pump_mac.mm:213] 	base::MessagePumpCFRunLoopBase::Run
0x0081e2b3 	[Google Chrome Framework 	- message_loop.cc:256] 	MessageLoop::Run
0x001a3743 	[Google Chrome Framework 	- browser_main.cc:456] 	BrowserMain
0x0000a8ac 	[Google Chrome Framework 	- chrome_dll_main.cc:900] 	ChromeMain
0x00001f57 	[Google Chrome 	- chrome_exe_main.mm:16] 	main
0x00001f15 	[Google Chrome 	+ 0x00000f15] 	
0x00000001 			

### in...@chromium.org (2010-08-25)

Crashes both 375 and 472 with similar stack. I do see some bugs assigned to @shess, @avi with objc_msgSend crash, but none look to have reproducers. @shess/@avi, can you please take a look or help with an owner.

### ro...@chromium.org (2010-08-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-27)

Who should take ownership of this bug? It's critical severity, so we really want to have it fixed in time for the first v6 stable refresh.


### ro...@chromium.org (2010-08-27)

I'm looking at it now, trying to figure out what the *right* way to fix it is.

### js...@chromium.org (2010-08-27)

@rohitrao - Thanks. I'll assign you as the owner. Let me know if it should be handed off to someone else.


### ro...@chromium.org (2010-08-27)

A possible solution is at http://codereview.chromium.org/3216004/show .  I'm not sure if it's the best solution, but it's the most straightforward, which might make it best for M6.

### bu...@gmail.com (2010-08-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=57785 

------------------------------------------------------------------------
r57785 | rohitrao@chromium.org | 2010-08-28 08:04:02 -0700 (Sat, 28 Aug 2010) | 5 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/cocoa/shell_dialogs_mac.mm?r1=57785&r2=57784

[Mac] Close file select dialogs when windows go away.

BUG=53361
TEST=Testcase in bug.
Review URL: http://codereview.chromium.org/3216004
------------------------------------------------------------------------


### ro...@chromium.org (2010-08-28)

Patch was ready on Friday, but the tree was closed =)

This is committed now, so I'm kicking the bug back over to inferno for merging.

### in...@chromium.org (2010-08-28)

Thanks Rohit. When i get the green flag from Anthony for v6 1st patch merges, i will merge this alongwith any other important security fixes. thanks again for quickly fixing it.

### in...@chromium.org (2010-09-08)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-09-08)

------------------------------------------------------------------------
r58831 | inferno@chromium.org | Wed Sep 08 09:13:36 PDT 2010
Changed paths:
 M /branches/472/src/chrome/browser/cocoa/shell_dialogs_mac.mm
Merge 57785 - [Mac] Close file select dialogs when windows go away.

BUG=53361
TEST=Testcase in bug.
Review URL: http://codereview.chromium.org/3216004

Review URL: http://codereview.chromium.org/3295020
------------------------------------------------------------------------

### sc...@gmail.com (2010-09-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-10)

@remy.saissy: thank you for noticing that the test case for 45400 still crashed Mac. It led us to another bug (this bug). For your help, we'd like to provisionally offer you a $500 Chromium Security Reward.

### re...@gmail.com (2010-09-10)

ok, thank you very much.

### ke...@chromium.org (2010-09-14)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-09-14)

6.0.472.59 (Official Build 59126)

No crash as seen before the fix.

### sc...@gmail.com (2010-09-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-22)

@remy.saissy: not sure that I ever paid this. Please e-mail cevans@chromium.org to collect your reward.

### re...@gmail.com (2010-11-22)

Hi,
Indeed you didn't.  I will send the email. Thank you very much !

### sc...@gmail.com (2010-12-02)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/53361?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082883)*
