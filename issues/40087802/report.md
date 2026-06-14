# Dev. console null character crash @ history::URLDatabase::GetMostRecentKeywordSearchTerms

| Field | Value |
|-------|-------|
| **Issue ID** | [40087802](https://issues.chromium.org/issues/40087802) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | al...@gmail.com |
| **Assignee** | br...@chromium.org |
| **Created** | 2011-02-10 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 9.0.597.94 under Win7  

URLs (if applicable) : n/a  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Firefox 3.x: OK

**What steps will reproduce the problem?**

1. Open up a blank tab (or any tab for that matter)
2. Press CTRL + SHIFT + J to bring up the dev. console
3. Paste in the following:  
   
   console.log(String.fromCharCode(0) + "test")
4. This should ouput the word "test". Select the WHOLE LINE that says "test". Make sure that your cursor goes a little to the left of the word when you select it.
5. Now right click on your selected word.

**What is the expected result?**  

Context menu with option to copy it.

**What happens instead?**  

Crash.

Please provide any additional information below. Attach a screenshot if possible.

-This is caused by the null character (ASCII 0) that was concatenated at the beginning of the string. It works fine if the null character is at the end or in the middle of it.

-Asked two other friends to test it under the same platform (both browser and os) as me, same results

## Timeline

### go...@charliesomerville.com (2011-02-10)

Doesn't affect Chrome on OS X.

### [Deleted User] (2011-02-10)

Can't reproduce this on Canary/XP.

Can you follow the instructions here to get a crash id or client id - 
http://www.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug?

### al...@gmail.com (2011-02-10)

For some reason, it doesn't appear in either eventvwr or in the CrashReports directory. I have crash reporting enabled. I have recorded a video of it happening (and on a different platform at that, WinXP this time), if it helps:
http://www.youtube.com/watch?v=RYGnRene6g4

I was able to get the client ID though:
3473D128-C251-4E65-8C6F-4373BCB3FEA6

### [Deleted User] (2011-02-10)

Thanks for the report. I can repro it on 9.0. But it's fixed in 10.0 and above.

Stack Trace
------------
Thread 0 *CRASHED* ( EXCEPTION_BREAKPOINT @ 0x64a035c3 )

0x64a035c3	 [chrome.dll	 - chrome_main.cc:140]	`anonymous namespace'::InvalidParameter(wchar_t const *,wchar_t const *,wchar_t const *,unsigned int,unsigned int)
0x65685309	 [chrome.dll	 - invarg.c:125]	_invalid_parameter_noinfo
0x64a0acac	 [chrome.dll	 - xstring:1570]	std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >::operator[](unsigned int)
0x64dfbb3a	 [chrome.dll	 - url_database.cc:427]	history::URLDatabase::GetMostRecentKeywordSearchTerms(__int64,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > const &,int,std::vector<history::KeywordSearchTermVisit,std::allocator<history::KeywordSearchTermVisit> > *)
0x64dde31c	 [chrome.dll	 - search_provider.cc:291]	SearchProvider::DoHistoryQuery(bool)
0x64dddf05	 [chrome.dll	 - search_provider.cc:180]	SearchProvider::Start(AutocompleteInput const &,bool)
0x64d13360	 [chrome.dll	 - autocomplete.cc:729]	AutocompleteController::Start(std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > const &,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > const &,bool,bool,bool,bool)
0x64cb55f7	 [chrome.dll	 - autocomplete_classifier.cc:36]	AutocompleteClassifier::Classify(std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > const &,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > const &,bool,AutocompleteMatch *,GURL *)
0x64dadc21	 [chrome.dll	 - render_view_context_menu.cc:588]	RenderViewContextMenu::AppendSearchProvider()
0x64dad6d5	 [chrome.dll	 - render_view_context_menu.cc:409]	RenderViewContextMenu::InitMenu()
0x64cd0f39	 [chrome.dll	 - tab_contents_view_win.cc:335]	TabContentsViewWin::ShowContextMenu(ContextMenuParams const &)
0x64bf7b61	 [chrome.dll	 - render_view_host.cc:1296]	RenderViewHost::OnMsgContextMenu(ContextMenuParams const &)
0x64bf99f2	 [chrome.dll	 - ipc_message_utils.h:944]	IPC::MessageWithTuple<Tuple1<ContextMenuParams> >::Dispatch<RenderViewHost,void ( RenderViewHost::*)(ContextMenuParams const &)>(IPC::Message const *,RenderViewHost *,void ( RenderViewHost::*)(ContextMenuParams const &))
0x64bf6aa8	 [chrome.dll	 - render_view_host.cc:798]	RenderViewHost::OnMessageReceived(IPC::Message const &)
0x64b5fef9	 [chrome.dll	 - browser_render_process_host.cc:929]	BrowserRenderProcessHost::OnMessageReceived(IPC::Message const &)
0x64ba3c19	 [chrome.dll	 - resource_message_filter.cc:131]	`anonymous namespace'::ContextMenuMessageDispatcher::Run()
0x64acbb26	 [chrome.dll	 - message_loop.cc:418]	MessageLoop::RunTask(Task *)
0x64acbbad	 [chrome.dll	 - message_loop.cc:427]	MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const &)
0x64acbd47	 [chrome.dll	 - message_loop.cc:534]	MessageLoop::DoWork()
0x64ae3cb8	 [chrome.dll	 - message_pump_win.cc:201]	base::MessagePumpForUI::DoRunLoop()
0x64ae3ac1	 [chrome.dll	 - message_pump_win.cc:49]	base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate *,base::MessagePumpWin::Dispatcher *)
0x64acb8c3	 [chrome.dll	 - message_loop.cc:261]	MessageLoop::RunInternal()
0x64acb853	 [chrome.dll	 - message_loop.cc:238]	MessageLoop::RunHandler()
0x64acbf85	 [chrome.dll	 - message_loop.cc:676]	MessageLoopForUI::Run(base::MessagePumpWin::Dispatcher *)
0x64b5a15b	 [chrome.dll	 - browser_main.cc:511]	`anonymous namespace'::RunUIMessageLoop(BrowserProcess *)
0x64b5bdf6	 [chrome.dll	 - browser_main.cc:1641]	BrowserMain(MainFunctionParams const &)
0x64a03f53	 [chrome.dll	 - chrome_main.cc:909]	ChromeMain
0x00d73d83	 [chrome.exe	 - client_util.cc:282]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x00d7412e	 [chrome.exe	 - chrome_exe_main_win.cc:46]	wWinMain

Full report @ http://crash/reportdetail?reportid=5af3c4446abf3418

Do we need to merge the fix in to M9 for this?

### la...@chromium.org (2011-02-10)

I'd be willing to take a patch for this if it's low risk.

### [Deleted User] (2011-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2011-02-11)

Steps from https://crbug.com/chromium/72702
-----------------------
Navigate to http://ajaxorg.github.com/ace/build/editor.html
Select some text and do a right click

Looks like we have to definitely fix this in 9.0.



### pf...@chromium.org (2011-02-11)

Non-devtools issue. Adding people to the CC.

### pk...@chromium.org (2011-02-11)

The actual crash here is in the line:

  next_prefix[next_prefix.size() - 1] = next_prefix[next_prefix.size() - 1] + 1;

The problem is that |next_prefix| is empty, so this is an out-of-bounds array access.

That's all I've got so far; still tracing through our source history to snoop out more.

### pk...@chromium.org (2011-02-11)

Here's the reason that code fails.  Just prior to the failing line, we do:

  DCHECK(!prefix.empty());
  ...
  string16 lower_prefix = l10n_util::ToLower(WideToUTF16(prefix));

ToLower(), in turn, does several things including critically:

  ...icu::UnicodeString(string.c_str())...

So, we pass in a non-empty |prefix| with an initial NUL, then ToLower() passes ICU the char16*, ICU sees the initial NUL and constructs an empty UnicodeString, and thus ToLower() eventually returns an empty string.

This code is still dangerous today; however, supposedly, the bug is no longer occurring.  My suspicion is that perhaps in Brett's r50597, where we converted a lot of stuff to string16, we may have changed something that resulted in code earlier than this newly seeing this as an "empty" string and thus never calling this function.

We probably need to track down why this bug isn't happening now (as it may only be due to something unintentional), and also fix ToLower() and any other functions that use .c_str() in this sort of unsafe fashion to do correct string conversions.  These could lead to other crashes and unexpected behavior besides this bug, so this fix is important.

Brett, I'm tentatively throwing this at you as I'm busy WebKit Sheriffing and you seem to be a good choice for this anyway.

### js...@chromium.org (2011-02-14)

It's a web triggerable OOB write in the browser process, so flagging as critical and bumping priority for now.

@brettw - I know you have a lot on your plate, so what are the odds of you getting to this? Or, is there someone else who should take it?

### br...@chromium.org (2011-02-14)

Do you have time to look at this since you've got it in your head?

### sc...@gmail.com (2011-02-14)

@jschuh - what makes it critical? Sounds like there's a lot of user interaction?

### pk...@chromium.org (2011-02-14)

No, I don't; I'm WK sheriff for several more days and am flooded behind that.

### js...@chromium.org (2011-02-15)

@pkasting - The repro from https://crbug.com/chromium/72517#c7 looks like it could be automated to level that's more reasonably exploitable. I'm happy to drop the severity if we know otherwise, but on browser crashes I prefer to err initially on the side of caution.

### pk...@chromium.org (2011-02-15)

I think you mean @scarybeasts :)

### js...@chromium.org (2011-02-15)

Yes... yes I did. :)

### sc...@gmail.com (2011-02-15)

Yeah, he means @scarybeasts :)

@jschuh: what some of automation did you have in mind? The last sentence from https://crbug.com/chromium/72517#c7 is "Select some text and do a right click". And the stack trace has on it:

0x64bf7b61	 [chrome.dll	 - render_view_host.cc:1296]	RenderViewHost::OnMsgContextMenu(ContextMenuParams const &)

There are other mitigations; for example on Windows, an OOB index on an STL array will always result in a runtime assert, even on optimized builds. It's also unclear if the dubious selection could be automated at the DOM API.

Perhaps High would be more appropriate; we can always adjust upwards later? I don't like to play the "critical" card unless we're sure.

### js...@chromium.org (2011-02-15)

@scarybeasts - On Windows it does, which is why this is an invalid parameter exception there. However, I thought gcc containers didn't bounds check containers. If they do, then it's a low-severity DoS across the board and we can drop the priority.

### sc...@gmail.com (2011-02-15)

@jschuh - I think STL on non-Windows platforms might not bounds check, so we're still alternating between high and critical. What did you think about the first half of https://crbug.com/chromium/72517#c18 ?

### js...@chromium.org (2011-02-16)

Yeah, I don't know what's going on well enough to know if the right-click can be automated or otherwise triggered. But I don't mind bumping it down to high-severity until we have more information.

### br...@chromium.org (2011-03-06)

[Empty comment from Monorail migration]

### br...@chromium.org (2011-03-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-03-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=77502

------------------------------------------------------------------------
r77502 | brettw@chromium.org | Wed Mar 09 11:40:34 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/l10n/l10n_util_unittest.cc?r1=77502&r2=77501&pathrev=77502
 M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/l10n/l10n_util.cc?r1=77502&r2=77501&pathrev=77502

Make ToUpper and ToLower properly handle embedded NULLs in the input.

BUG=72517
TEST=included unit test
Review URL: http://codereview.chromium.org/6625046
------------------------------------------------------------------------

### js...@chromium.org (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-18)

M10 is r78651, M11 is r78652

### sc...@gmail.com (2011-03-18)

@alex.turpin: thanks for your report, we found it very useful. It turned out to be a security issue, and therefore we'd like to offer you a $500 Chromium Security Reward for your help.

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issues.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-03-18)

[Empty comment from Monorail migration]

### la...@chromium.org (2011-03-19)

Chrome Version : 9.0.597.94 under Win7  

URLs (if applicable) : n/a  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Firefox 3.x: OK

**What steps will reproduce the problem?**

1. Open up a blank tab (or any tab for that matter)
2. Press CTRL + SHIFT + J to bring up the dev. console
3. Paste in the following:  
   
   console.log(String.fromCharCode(0) + "test")
4. This should ouput the word "test". Select the WHOLE LINE that says "test". Make sure that your cursor goes a little to the left of the word when you select it.
5. Now right click on your selected word.

**What is the expected result?**  

Context menu with option to copy it.

**What happens instead?**  

Crash.

Please provide any additional information below. Attach a screenshot if possible.

-This is caused by the null character (ASCII 0) that was concatenated at the beginning of the string. It works fine if the null character is at the end or in the middle of it.

-Asked two other friends to test it under the same platform (both browser and os) as me, same results

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-25)

@alex.turpin: mail cevans@google.com for instructions on collecting the reward.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### sc...@gmail.com (2012-12-14)

Payment in system.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/72517?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087802)*
