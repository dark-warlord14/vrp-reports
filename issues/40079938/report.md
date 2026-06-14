# Security: You can spoof any domain in the URL bar

| Field | Value |
|-------|-------|
| **Issue ID** | [40079938](https://issues.chromium.org/issues/40079938) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Reporter** | is...@gmail.com |
| **Assignee** | na...@chromium.org |
| **Created** | 2014-06-27 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36

Steps to reproduce the problem:
Run this on any page:

history.replaceState(null, null, "blob:" + location.protocol + "//www.google.com" + Array(0x1000).join(" ") + "@" + location.host)

What is the expected behavior?
The username part of the URL should be collapsed from view in the URL bar, as is normally done. For example, history.replaceState(null, null, location.protocol + "//www.google.com@" + location.host) is handled properly.

What went wrong?
The username part of the URL is not collapsed from view in the URL bar.

Did this work before? No 

Chrome version: 35.0.1916.153  Channel: stable
OS Version: 6.3
Flash Version: Shockwave Flash 14.0 r0

In order to spoof an https: URL (e.g. https://www.google.com) this exploit needs to be run on a page that is already being served as https.


## Attachments

- [unexpected.png](attachments/unexpected.png) (image/png, 75.5 KB)
- [expected.png](attachments/expected.png) (image/png, 63.9 KB)

## Timeline

### is...@gmail.com (2014-06-28)

There can be any Unicode whitespace characters (and some control characters) between blob: and the original protocol. I didn't look into it enough to see if I am able to hide the blob: part using various Unicode characters, though it may be possible (see Zalgo).

### is...@gmail.com (2014-06-28)

My simplest proposed solution: Disallow blob: URLs from being used for replaceState/pushState. If that is done, you won't have to worry about specifically handling the username stuff at all.

### is...@gmail.com (2014-06-28)

Actually, you can still do location.href = "blob:http://www.google.com@yourdomain" if that fix is done, so maybe you will want to handle the username and blob: URL stuff as well. Please note that it is impossible to exploit the location.href = ... method, as it is equivalent to an empty page, and therefore cannot run any code by itself.

### cl...@chromium.org (2014-06-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-06-30)

The SSL state of the page does indicate that the location bar has been changed, but yes, this does seem like spoofing. I was able to repro on stable and beta, though the current Mac Chrome Canary/trunk@280597 seems to have the browser killing the page:

* thread #1: tid = 0x11e9bb6, 0x007eebec Chromium Framework`base::KillProcess(process_id=35423, exit_code=3, wait=<unavailable>) + 12 at kill_posix.cc:138, name = 'CrBrowserMain', queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
  * frame #0: 0x007eebec Chromium Framework`base::KillProcess(process_id=35423, exit_code=3, wait=<unavailable>) + 12 at kill_posix.cc:138
    frame #1: 0x02ed4e85 Chromium Framework`content::RenderProcessHostImpl::ReceivedBadMessage(this=<unavailable>) + 213 at render_process_host_impl.cc:977
    frame #2: 0x02da405e Chromium Framework`content::(anonymous namespace)::AreURLsInPageNavigation(existing_url=<unavailable>, new_url=<unavailable>, renderer_says_in_page=<unavailable>, rfh=<unavailable>) + 238 at navigation_controller_impl.cc:129
    frame #3: 0x02da51fc Chromium Framework`content::NavigationControllerImpl::IsURLInPageNavigation(this=0x80a31c48, url=0xbffd2e84, renderer_says_in_page=<unavailable>, rfh=0x7cd4c250) const + 60 at navigation_controller_impl.cc:1263
    frame #4: 0x02daab7f Chromium Framework`content::NavigatorImpl::DidNavigate(this=0x818430e0, render_frame_host=0x7cd4c250, input_params=0xbffd3220) + 799 at navigator_impl.cc:450
    frame #5: 0x02daea6d Chromium Framework`content::RenderFrameHostImpl::OnNavigate(this=0x7cd4c250, msg=0x8188dba4) + 733 at render_frame_host_impl.cc:511
    frame #6: 0x02dae2f9 Chromium Framework`content::RenderFrameHostImpl::OnMessageReceived(this=0x7cd4c250, msg=0x8188dba4) + 4889 at render_frame_host_impl.cc:319
    frame #7: 0x02ed6130 Chromium Framework`content::RenderProcessHostImpl::OnMessageReceived(this=<unavailable>, msg=0x9b7c786c) + 400 at render_process_host_impl.cc:1415
    frame #8: 0x02ed707b Chromium Framework`non-virtual thunk to content::RenderProcessHostImpl::OnMessageReceived(this=0x7cd3c2e4, msg=0x8188dba4) + 27 at render_process_host_impl.cc:1416
    frame #9: 0x00e2fca9 Chromium Framework`IPC::ChannelProxy::Context::OnDispatchMessage(this=0x7fd28e00, message=0x8188dba4) + 121 at ipc_channel_proxy.cc:273
    frame #10: 0x00e316e9 Chromium Framework`base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) [inlined] base::internal::RunnableAdapter<void (object=<unavailable>)(IPC::Message const&)>::Run(IPC::ChannelProxy::Context*, IPC::Message const&) + 41 at bind_internal.h:190
    frame #11: 0x00e316d6 Chromium Framework`base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) [inlined] base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) at bind_internal.h:898
    frame #12: 0x00e316d6 Chromium Framework`base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (base=0x8188db90)(IPC::Message const&)>, void (IPC::ChannelProxy::Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) + 22 at bind_internal.h:1248
    frame #13: 0x007ddcca Chromium Framework`base::MessageLoop::RunTask(base::PendingTask const&) [inlined] base::Callback<void ()>::Run() const + 490 at callback.h:401
    frame #14: 0x007ddcc1 Chromium Framework`base::MessageLoop::RunTask(this=0x79f38a70, pending_task=0xbffd3f28) + 481 at message_loop.cc:458
    frame #15: 0x007de347 Chromium Framework`base::MessageLoop::DoWork() [inlined] base::MessageLoop::DeferOrRunPendingTask(this=<unavailable>) + 583 at message_loop.cc:470
    frame #16: 0x007de33b Chromium Framework`base::MessageLoop::DoWork(this=<unavailable>) + 571 at message_loop.cc:584
    frame #17: 0x00792ced Chromium Framework`base::MessagePumpCFRunLoopBase::RunWork(this=0x79f38d40) + 109 at message_pump_mac.mm:558
    frame #18: 0x91d5cb6f CoreFoundation`__CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__ + 15
    frame #19: 0x91d4d96b CoreFoundation`__CFRunLoopDoSources0 + 235
    frame #20: 0x91d4d06e CoreFoundation`__CFRunLoopRun + 1022
    frame #21: 0x91d4c9fa CoreFoundation`CFRunLoopRunSpecific + 394
    frame #22: 0x91d4c85b CoreFoundation`CFRunLoopRunInMode + 123
    frame #23: 0x91226b5d HIToolbox`RunCurrentEventLoopInMode + 259
    frame #24: 0x912268e2 HIToolbox`ReceiveNextEventCommon + 526
    frame #25: 0x912266bd HIToolbox`_BlockUntilNextEventMatchingListInModeWithFilter + 92
    frame #26: 0x9b5ba369 AppKit`_DPSNextEvent + 1602
    frame #27: 0x9b5b9890 AppKit`-[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:] + 119
    frame #28: 0x9b5ac17c AppKit`-[NSApplication run] + 727
    frame #29: 0x00793437 Chromium Framework`base::MessagePumpNSApplication::DoRun(this=0x79f38d40, delegate=0x79f38a70) + 423 at message_pump_mac.mm:905
    frame #30: 0x007929fc Chromium Framework`base::MessagePumpCFRunLoopBase::Run(this=0x79f38d40, delegate=0x79f38a70) + 92 at message_pump_mac.mm:460
    frame #31: 0x007dd8e1 Chromium Framework`base::MessageLoop::RunHandler(this=0x79f38a70) + 33 at message_loop.cc:408
    frame #32: 0x007f5821 Chromium Framework`base::RunLoop::Run(this=0xbffd5880) + 65 at run_loop.cc:49
    frame #33: 0x00113928 Chromium Framework`ChromeBrowserMainParts::MainMessageLoopRun(this=0x7cc35a60, result_code=<unavailable>) + 152 at chrome_browser_main.cc:1590
    frame #34: 0x02d14640 Chromium Framework`content::BrowserMainLoop::RunMainMessageLoopParts(this=0x7cc35b30) + 80 at browser_main_loop.cc:709
    frame #35: 0x02d16c43 Chromium Framework`content::BrowserMainRunnerImpl::Run(this=0x7cc35520) + 19 at browser_main_runner.cc:118
    frame #36: 0x02d1012e Chromium Framework`content::BrowserMain(parameters=<unavailable>) + 190 at browser_main.cc:26
    frame #37: 0x0075840a Chromium Framework`content::RunNamedProcessTypeMain(process_type=<unavailable>, main_function_params=<unavailable>, delegate=<unavailable>) + 186 at content_main_runner.cc:417
    frame #38: 0x00758d6e Chromium Framework`content::ContentMainRunnerImpl::Run(this=<unavailable>) + 126 at content_main_runner.cc:763
    frame #39: 0x00758162 Chromium Framework`content::ContentMain(params=0xbffd59f8) + 50 at content_main.cc:19
    frame #40: 0x00030865 Chromium Framework`ChromeMain(argc=2, argv=0xbffd5a68) + 53 at chrome_main.cc:46
    frame #41: 0x0002bf78 Chromium`main(argc=2, argv=0xbffd5a68) + 24 at chrome_exe_main_mac.cc:53


### na...@chromium.org (2014-06-30)

The renderer is killed because it is trying to do something that doesn't make sense. This is fixed in r279232 and should be backported to beta and stable if possible.

### rs...@chromium.org (2014-06-30)

japhet: Is this change reasonable to merge?

### fe...@chromium.org (2014-06-30)

Which part of this problem does r279232 fix? Just the browser killing the page?

### rs...@chromium.org (2014-06-30)

Yes, I think r279232 changes the way in which navigation messages are considered "bad," which results in the browser killing the renderer. Without that, the navigation can take place and the URL can be spoofed.

### ja...@chromium.org (2014-06-30)

Yes, this seems reasonable to merge, though we should probably also rope in someone who better understands blob urls and url parsing to figure out why we are allowing the renderer to send a bad message in the first place.

Someone else should probably do the merge, though. I'm out on leave and only sporadically paying attention to work stuff. 

### na...@chromium.org (2014-06-30)

I will not be online for a couple of days, so anyone is free to merge this earlier. Adding Merge-Requested label.

### ja...@chromium.org (2014-06-30)

One word of warning: it occurs to me that this code has likely changed non-trivially since beta/stable, so the merge may be a bit painful and might genuinely depend on earlier patches like http://src.chromium.org/viewvc/chrome?view=revision&revision=274734

### na...@google.com (2014-07-03)

Adding pkasting@ to look at URL/omnibox behavior.

### pk...@chromium.org (2014-07-03)

The address bar in this case says "blob:https://www.google.com".  That doesn't seem like a spoof of google.com to me unless the word "blob" can be hidden.

I think the security folks need to state clearly what the intended behavior is here.  This should also be reflected in the blob spec.  If there is a decision that Chrome's behavior needs to change, I can implement that.

### fe...@chromium.org (2014-07-03)

I think it's pretty confusing for the address bar to say "blob:https://www.google.com" while the page still displays the contents of the prior page.

### pa...@chromium.org (2014-07-07)

Potentially of interest to mkwst, as part of his overall efforts to clarify the various, ahh... "informal" specifications we've all been relying on. :) (E.g. mixed content.)

I found that after you run the attack code, the contents of the context menu that you get when you right-click on the link take a change for the worse (see screenshots). Yikes!

(And, of course, I couldn't post this comment in the attacked window. Don't know if that's expected. Basically navigation is a total mess after the attack code runs.)

### rs...@chromium.org (2014-07-07)

[Empty comment from Monorail migration]

### is...@gmail.com (2014-07-08)

In reply to https://crbug.com/chromium/389734#c16: While navigation is a mess, it is still possible to use event handlers, etc. to keep the page interactive.

### cl...@chromium.org (2014-07-09)

nasko@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### na...@chromium.org (2014-07-09)

felt@, do you think there is action item here in terms of UI?

From navigation logic perspective, this is fixed on ToT. The fixes in this area are not easy to backport to stable, so unless people object, I'll let those roll out to branches as time goes by.

### na...@chromium.org (2014-07-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-09)

[Empty comment from Monorail migration]

### fe...@chromium.org (2014-07-10)

My understanding is that the CL leads to a sad tab. What other UI changes do you think might be needed?

### is...@gmail.com (2014-07-10)

I just noticed that this also works in stable (I ran it on http://www.squarefree.com/shell/shell.html):

open(URL.createObjectURL(new Blob(["<script>history.replaceState(null, null, " + JSON.stringify(location.href) + ")</script>"], {type: "text/html"})))

Is this also a security vulnerability? I'm not sure, as the blob URL inherits the origin of the page that created the blob URL. It makes sense for it to work, and it would be useful for the kind of pre-loading you normally use with history.pushState for same-origin links opened in the same tab. This would enable those types of scripts to also support Ctrl+click/middle click->new tab pre-loading.

### ti...@chromium.org (2014-07-11)

Removing merge-requested as the fix is apparently on ToT as r279232 and happy to roll out over time due to the non-easy backport (see c#20).

Please update if my understanding is incorrect.

### is...@gmail.com (2014-09-08)

If I understand correctly, this should be M-38.

### is...@gmail.com (2014-09-09)

Btw, when combined with tabnabbing (http://www.azarask.in/blog/post/a-new-type-of-phishing-attack/), this becomes a really powerful phishing tool, which I think warrants Security_Severity-High. What do you guys think?

### fe...@chromium.org (2014-09-10)

Yes, this will be going with 38.

### na...@chromium.org (2014-09-11)

According to the severity descriptions (http://www.chromium.org/developers/severity-guidelines), it does appear that this is High, so I'm adjusting it accordingly.


### is...@gmail.com (2014-10-07)

Chrome 38 is out now. Has this been assigned a CVE for the googlechromereleases.blogspot.com blog post later today?

### fe...@chromium.org (2014-10-07)

tim, can you answer the CVE question?

### ti...@chromium.org (2014-10-07)

Let me look into this. Because the labels were wrong on the bug (marked as M37, not M38), it hasn't gone to the M38 reward panel so won't be in the release notes today.

We'll take a look and we can update the release notes once this goes through the panel. I'll update this thread with progress.

### is...@gmail.com (2014-10-07)

I'm sorry for sounding greedy, but can you put this into a different blog post instead of updating the release notes? All of the third party syndication will only be using the initial blog post, and I'd rather not be left out of free PR.

### ti...@google.com (2014-10-08)

Understood - the best I can offer you if you don't want me to update the M38 release notes is to list this fix in the next set of release notes. That way you'll be part of the syndication. 

Do you want to do that and wait for the next set of release notes? 

### is...@gmail.com (2014-10-08)

Yeah, that sounds good. Thanks Tim.

### ti...@chromium.org (2014-10-10)

Good times.

For future me/someone else: Adding Release-0-M38 release label (as this is when this fixed rolled out) as well as Release-1-M38 so that this gets added to the next set of release notes. Please remove the Release-1-M38 label after the release notes come out.

### cl...@chromium.org (2014-10-15)

Bulk update: removing view restriction from closed bugs.

### is...@gmail.com (2014-10-18)

Was http://googlechromereleases.blogspot.com/2014/10/stable-channel-update-for-chrome-os_16.html about Release-1?

### mb...@chromium.org (2014-11-17)

Thanks again for the report. It qualified for a $500 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-12)

Submitted for payment - you should see the cash in your account in 4-6 weeks from today. If not, contact me directly to chase it.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/389734?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079938)*
