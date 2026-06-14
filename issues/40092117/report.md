# Use after free on 2-Step-Authentication-method-change

| Field | Value |
|-------|-------|
| **Issue ID** | [40092117](https://issues.chromium.org/issues/40092117) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | fe...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2011-06-22 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 14.0.797.0  

URLs (if applicable) :<https://www.google.com/accounts/SmsAuthConfig>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 5:**  

Firefox 4.x:OK  

IE 7/8/9:OK

**What steps will reproduce the problem?**  

1.Have 2 Step Authentication enabled (Android confirmation)  

2.Try to change how to recieve Codes

**What is the expected result?**  

No Crash

**What happens instead?**  

When you select any value from the dropdown menu that and some other open Google-Tabs crash (in my case GMail and GReader crash, Calendar stays open)

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

My Google-Account is german but my language-setting is english.. If that might be related

## Timeline

### th...@chromium.org (2011-06-23)

Can you get a crash report id?
http://dev.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug

### fe...@gmail.com (2011-06-23)

As I was reproducing it, I have several:
f4a4347e661dbc94
f4a4347e661db9cf
290eca01e3fd72f2
290eca01e3fd70ef


### th...@chromium.org (2011-06-23)

Thanks for the crash report ids.

Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_READ @ 0x00000000 )
0x6fabd8e0 	[chrome.dll 	- resourcehandle.cpp:162] 	WebCore::ResourceHandleInternal::didReceiveResponse(WebKit::WebURLLoader *,WebKit::WebURLResponse const &)
0x6f591259 	[chrome.dll 	- weburlloader_impl.cc:564] 	webkit_glue::WebURLLoaderImpl::Context::OnReceivedResponse(webkit_glue::ResourceResponseInfo const &)
0x6f0ac49a 	[chrome.dll 	- resource_dispatcher.cc:320] 	ResourceDispatcher::OnReceivedResponse(int,ResourceResponseHead const &)
0x6f0ad69b 	[chrome.dll 	- ipc_message_utils.h:964] 	IPC::MessageWithTuple<Tuple2<int,ResourceResponseHead> >::Dispatch<ResourceDispatcher,ResourceDispatcher,void ( ResourceDispatcher::*)(int,ResourceResponseHead const &)>(IPC::Message const *,ResourceDispatcher *,ResourceDispatcher *,void ( ResourceDispatcher::*)(int,ResourceResponseHead const &))
0x6f0acb68 	[chrome.dll 	- resource_dispatcher.cc:496] 	ResourceDispatcher::DispatchMessageW(IPC::Message const &)
0x6f0ac382 	[chrome.dll 	- resource_dispatcher.cc:277] 	ResourceDispatcher::OnMessageReceived(IPC::Message const &)
0x6f0a1c25 	[chrome.dll 	- child_thread.cc:149] 	ChildThread::OnMessageReceived(IPC::Message const &)
0x6fbbf1b9 	[chrome.dll 	- task.h:338] 	RunnableMethod<browser_sync::SyncBackendHost::Core,void ( browser_sync::SyncBackendHost::Core::*)(browser_sync::SyncBackendHost::Core::DoInitializeOptions const &),Tuple1<browser_sync::SyncBackendHost::Core::DoInitializeOptions> >::Run()
0x6f1b5470 	[chrome.dll 	- message_loop.cc:102] 	`anonymous namespace'::TaskClosureAdapter::Run()
0x6f1b5efb 	[chrome.dll 	- message_loop.cc:482] 	MessageLoop::RunTask(MessageLoop::PendingTask const &)

### ti...@gmail.com (2011-06-27)

I also get the crash whenever I select something in the select box (same build here). A (not very convenient) workaround is to manually edit the HTML of the box.

### to...@chromium.org (2011-06-27)

Does it only crash on that select box or have you seen a tab crash on other select boxes?


I tried to repro, but it seems to work for me (tip-of-tree build on Linux).  I turned on 2-step verification.  In the "How to receive codes" section of the page, I have Mobile Application (Android), backup phone number and printable backup codes.  If I click "Edit" next to Android, I got to a page with a drop down.  When I select another value (like iPhone) and press Next, the next page loads fine.  Are you experiencing the crash at a different point?


### to...@chromium.org (2011-06-27)

[Empty comment from Monorail migration]

### ka...@google.com (2011-06-27)

[Empty comment from Monorail migration]

### fe...@gmail.com (2011-06-27)

Crash is exactly there.
(2 new IDs: 82d6e63adb809aff, 6bbec6b0f792670b)
If I select "Choose One" or my Current option "Text message" the page loads fine.
On selection of any other option (namely Android, Blackberry, iPhone) it crashes.
I've disabled everything in flags, still using 14.0.797.0, german GMail (2 be precise; googlemail)-account, language settings in english because 2-step is (was) not available in german.

### to...@chromium.org (2011-06-27)

Can you try disabling any/all extensions to see if they're causing a problem?  You can disable them in chrome://extensions/ .

### fe...@gmail.com (2011-06-28)

Im Sorry I didnt think of that.
After disabling all that bug disappears, funnily after reenabling all of em it still doesnt come back.
After a couple of restarts I now found that its caused by AdBlock.
Im going to file a bug in their forum.
Thanks :)

### [Deleted User] (2011-06-28)

But we can't handle crashes. In case of a JS error we are able to find the cause of the crash, but a crash is something we can't handle. So it must be a Chrome bug that it crashes.
Famlam (AdBlockforChrome)

### to...@chromium.org (2011-06-28)

I agree, chrome should not crash.

Passing to Erik to triage.

### to...@chromium.org (2011-06-28)

[Empty comment from Monorail migration]

### fe...@gmail.com (2011-06-28)

After a little thinking I came up with the following;
In my view the only reasons for a crash are:
[*] AdBlock has a general fnord, that needs to be fixed, but only becomes visible on that website
[*] One of the Filters (AdBlock) blocks an important part of the page, but that shouldnt crash the whole tab
[*] The Website itself has some funny functions implemented that arent conform with something
[*] (As that page used to work in earlier versions, also with AdBlock) Some routines in Chrome <-> Extensions handling have changed, AdBlock didnt adapt to that.

### si...@gmail.com (2011-06-29)

I'm getting this issue as well with 14.0.803.0 dev-m on 64-bit Windows 7. I just want to reiterate that this issue is definitely related to extensions. After trying the page out in Incognito Mode (everything worked fine), I tried to go through my extensions one-by-one and figure out what was causing the problem. 

For me, Adblock Plus was not the issue. I've reproduced it multiple times, and everything works once I disable the official Google Voice extension (version 2.2.3.4), and only that one extension. 

Hope that helps! 

### [Deleted User] (2011-06-29)

The crash is in WebKit.  Handing to Dimitri.

### dg...@chromium.org (2011-06-30)

Nate, can you take a look?

### ja...@chromium.org (2011-07-08)

I just reproed this with a debugger attached, and it looks the stack is corrupt.  Marking as a security issue.

### ja...@chromium.org (2011-07-08)

The problem appears to be PopuListBox::handleMouseReleaseEvent().  It appears that the PopupContainer and PopupListBox (in PopupMenuChromium.cpp) that we're working with are being deleted by event handlers, and they aren't RefPtr protected anyway.

I'm pretty sure we're use-after-freeing 100% of the time, but we only crash with extensions because adblock reliably reuses the freed memory for us.

### ja...@chromium.org (2011-07-08)

Looks like this is a pretty easy protective RefPtr fix, though getting a working layout test may be tougher, since the hook in DRT for creating a  platform popup menu is stubbed out.

### in...@chromium.org (2011-07-10)

If layout test is not easy, we should go ahead with the refptr fix.

### ja...@chromium.org (2011-07-11)

WebKit bug opened: https://bugs.webkit.org/show_bug.cgi?id=64295

### ja...@chromium.org (2011-07-11)

Landed upstream: http://trac.webkit.org/changeset/90769

This bug was introduced in http://trac.webkit.org/changeset/88232, which hasn't made it to a branch yet, so I think this won't require any merges.

Leaving as FixUnreleased until the next Dev channel release.

### in...@chromium.org (2011-07-11)

That is called - "lightning fast fixx". Thanks Nate.

### ja...@chromium.org (2011-07-20)

This was a regression and only made it to dev channel, where it has now been fixed.

### ja...@chromium.org (2011-07-20)

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### aj...@chromium.org (2014-06-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Old bug is old! Found in a clean up of unpaid rewards. If you're still there, we'd like to pay you $500 for this bug.

We'll get in contact directly regarding payment details. Belated congratulations!

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-06)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/87120?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/87311, crbug.com/chromium/88925]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092117)*
