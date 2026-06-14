# Browser crash @ JavaScriptAppModalDialog::Cleanup()

| Field | Value |
|-------|-------|
| **Issue ID** | [40085084](https://issues.chromium.org/issues/40085084) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, UI>Browser>TabContents |
| **Reporter** | av...@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2010-11-19 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 7.0.517.44  

URLs (if applicable) : <http://4su.ru/index.html>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 5: OK  

Firefox 3.x: OK  

IE 7/8: OK

**What steps will reproduce the problem?**

1. go to <http://4su.ru/index.html>
2. check "Prevent this page from creating additional dialogs."
3. close either tab with <http://4su.ru/index.html> or application

**What is the expected result?**  

tab or application should be closed

**What happens instead?**  

crash following by hanging of application. One time it comes along with drwtsn32 crash.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

## Attachments

- [ChromeCrashOnbeforeunload.zip](attachments/ChromeCrashOnbeforeunload.zip) (application/zip; charset=binary, 5.2 MB)

## Timeline

### te...@gmail.com (2010-11-19)

Thanks for reporting this and attaching the crash dumps and testcase. The client-id from the attached zip: 7BBCCCB7-7459-41FA-8384-6461DB3E9B62

I can reproduce the crash on Windows with 9.0.590.0 (66709).

### te...@gmail.com (2010-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2010-11-19)

Thanks for the report.

Steps to repro
---------------
1. Navigate to http://4su.ru/index.html and click OK on first alert dialog
2. Check the option 'Prevent this page blah blah' and click OK
3. Quickly try closing the window(I used Alt+F4) - You'll see another alert 'Goodbye Google'
4. Click on leave this page.

Kaboom!!!

Stack Trace
------------
Thread 0 *CRASHED* ( EXCEPTION_BREAKPOINT @ 0x63f1357b )

0x63f1357b	 [chrome.dll	 - chrome_dll_main.cc:147]	`anonymous namespace'::InvalidParameter(wchar_t const *,wchar_t const *,wchar_t const *,unsigned int,unsigned int)
0x64b6c1ac	 [chrome.dll	 - purevirt.c:47]	_purecall
0x6429d8e1	 [chrome.dll	 - js_modal_dialog.cc:150]	JavaScriptAppModalDialog::Cleanup()
0x64320eee	 [chrome.dll	 - js_modal_dialog_views.cc:110]	JSModalDialogViews::Accept()
0x64340994	 [chrome.dll	 - instant_confirm_view.cc:48]	views::DialogDelegate::Accept(bool)
0x64a3b22f	 [chrome.dll	 - dialog_client_view.cc:230]	views::DialogClientView::AcceptWindow()
0x64a3b598	 [chrome.dll	 - dialog_client_view.cc:406]	views::DialogClientView::ButtonPressed(views::Button *,views::Event const &)
0x64a34c8b	 [chrome.dll	 - button.cc:58]	views::Button::NotifyClick(views::Event const &)
0x64a2f0c7	 [chrome.dll	 - native_button.cc:128]	views::NativeButton::ButtonPressed()
0x64a49769	 [chrome.dll	 - native_button_win.cc:129]	views::NativeButtonWin::ProcessMessage(unsigned int,unsigned int,long,long *)
0x64a31584	 [chrome.dll	 - widget_win.cc:1229]	views::WidgetWin::OnWndProc(unsigned int,unsigned int,long)
0x649362e9	 [chrome.dll	 - window_impl.cc:195]	gfx::WindowImpl::WndProc(HWND__ *,unsigned int,unsigned int,long)
0x755c6237	 [user32.dll	 + 0x00016237]	InternalCallWinProc
0x755c68e9	 [user32.dll	 + 0x000168e9]	UserCallWinProcCheckWow
0x755ccd19	 [user32.dll	 + 0x0001cd19]	SendMessageWorker
0x755ccd80	 [user32.dll	 + 0x0001cd80]	SendMessageW
0x73544e94	 [comctl32.dll	 + 0x000a4e94]	Button_NotifyParent(tagBUTN *,unsigned int)
0x73544ef6	 [comctl32.dll	 + 0x000a4ef6]	Button_NotifyParent(tagBUTN *,unsigned int)
0x73544d88	 [comctl32.dll	 + 0x000a4d88]	_imp_load__GetThemeEnumValue
0x755c6237	 [user32.dll	 + 0x00016237]	InternalCallWinProc
0x755c68e9	 [user32.dll	 + 0x000168e9]	UserCallWinProcCheckWow
0x755d0aaf	 [user32.dll	 + 0x00020aaf]	CallWindowProcAorW
0x755d0ad5	 [user32.dll	 + 0x00020ad5]	CallWindowProcW
0x64a51241	 [chrome.dll	 - native_control_win.cc:220]	views::NativeControlWin::NativeControlWndProc(HWND__ *,unsigned int,unsigned int,long)
0x755c6237	 [user32.dll	 + 0x00016237]	InternalCallWinProc
0x755c68e9	 [user32.dll	 + 0x000168e9]	UserCallWinProcCheckWow
0x755c7d30	 [user32.dll	 + 0x00017d30]	DispatchMessageWorker
0x755c7df9	 [user32.dll	 + 0x00017df9]	DispatchMessageW
0x64a281b5	 [chrome.dll	 - accelerator_handler_win.cc:58]	views::AcceleratorHandler::Dispatch(tagMSG const &)
0x63ff4133	 [chrome.dll	 - message_pump_win.cc:352]	base::MessagePumpForUI::ProcessMessageHelper(tagMSG const &)
0x63ff3f8c	 [chrome.dll	 - message_pump_win.cc:197]	base::MessagePumpForUI::DoRunLoop()
0x63ff3da7	 [chrome.dll	 - message_pump_win.cc:49]	base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate *,base::MessagePumpWin::Dispatcher *)
0x63fdb6a0	 [chrome.dll	 - message_loop.cc:261]	MessageLoop::RunInternal()
0x63fdb630	 [chrome.dll	 - message_loop.cc:238]	MessageLoop::RunHandler()
0x63fdbd62	 [chrome.dll	 - message_loop.cc:676]	MessageLoopForUI::Run(base::MessagePumpWin::Dispatcher *)
0x6406592e	 [chrome.dll	 - browser_main.cc:506]	`anonymous namespace'::RunUIMessageLoop(BrowserProcess *)
0x64067439	 [chrome.dll	 - browser_main.cc:1611]	BrowserMain(MainFunctionParams const &)
0x63f13ff0	 [chrome.dll	 - chrome_dll_main.cc:838]	ChromeMain
0x00ab3dc8	 [chrome.exe	 - client_util.cc:282]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x00ab4199	 [chrome.exe	 - chrome_exe_main_win.cc:46]	wWinMain

Full report @ http://crash/reportdetail?reportid=78b79330c8daa243

### [Deleted User] (2010-11-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-11-20)

I was able to reproduce on a current dev. It looks like a stale pointer in the browser, so for now flagging as critical. We can reduce the severity if we determine that there's no way to trigger this without the multiple dialogs.

### js...@chromium.org (2010-11-24)

Had a chance to look at this. The tab_contents_ pointer is definitely stale. It looks like a pretty straightforward thing to fix. I'll try to take care of it today and get it rolled into the first m8 update.


### js...@chromium.org (2010-11-24)

@aa - Looks like you're familiar with this code. The problem here is that tab_contents_ is already deleted. I was digging around to see if the TabContents had an easy way to clear out the back pointer from JavaScriptAppModalDialog, but I didn't see an obvious solution and I'm not familiar with this code.

### js...@chromium.org (2010-11-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-12-01)

@aa - This is a critical severity bug (currently the only one we have). Since you're the original author I figured you were the best to take it. But if you don't have time, can you propose anyone else familiar with this particular code?

### js...@chromium.org (2010-12-01)

[Empty comment from Monorail migration]

### aa...@chromium.org (2010-12-01)

Sorry I did not see this earlier. I'm not the original author of this code, but I will take a quick look.

### js...@chromium.org (2010-12-01)

@aa - My bad. I saw you listed in svn blame and didn't realize it was just a revert. Please feel free to remove yourself from the CC.

@zelidrag - Could you take a look at this? I explained the issue above, but I'm not sure how best to fix it.


### aa...@chromium.org (2010-12-01)

My guess is that the extension_host_ and tab_contents_ back pointers should be cleared along with the delegate_ in ::Observe().

### aa...@chromium.org (2010-12-01)

Since I already started looking at this, I'm going to keep it.

### js...@chromium.org (2010-12-01)

Oh, thanks for grabbing it then; it's very much appreciated. I just didn't want to shove the bug on you if it wasn't your code in the first place. :)

### js...@chromium.org (2010-12-07)

@aa - We may be doing a stable refresh next week. Do you think the patch for this can make it?

### aa...@chromium.org (2010-12-07)

I think so. I should be able to land on trunk today or tomorrow. It looks like the related files have moved due to refactors since 8.x, but their contents look very similar, so hopefully merging won't be too bad.

The reason it has taken awhile is that this code has rotted quite a bit and there were several related things going on. See: http://code.google.com/p/chromium/issues/list?q=reporter:me+dialog and http://codereview.chromium.org/5548001/.

### aa...@chromium.org (2010-12-07)

[Empty comment from Monorail migration]

### aa...@chromium.org (2010-12-07)

Heh, obviously that should be:

http://code.google.com/p/chromium/issues/list?q=reporter:aa@chromium.org+dialog

### bu...@chromium.org (2010-12-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=68447

------------------------------------------------------------------------
r68447 | aa@chromium.org | Mon Dec 06 21:33:07 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/app_modal_dialogs/js_modal_dialog.h?r1=68447&r2=68446&pathrev=68447
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/app_modal_dialogs/js_modal_dialog.cc?r1=68447&r2=68446&pathrev=68447

It turns out the Cleanup() method in JsModalDialog is not
needed. The check in it was reversed, causing it to never
do anything, except in the case where the delegate had been
deleted, in which case it would crash.

The thing it was trying to do is already being done elsewhere
in the case of OnAccept() and OnCancel(). That just leaves
OnClose().

There are other things in here that really need cleanup, but
I will do those separately.

BUG=63732
TEST=See bug

Review URL: http://codereview.chromium.org/5548001
------------------------------------------------------------------------

### js...@chromium.org (2010-12-07)

Thanks Aaron. Hope the code shifting underfoot wasn't too much trouble. I should be able to handle the merge tomorrow. Like you said, the files have moved but the contents don't seem much changed.


### sc...@gmail.com (2010-12-20)

Justin, will you be sending this reward to the panel?

### js...@chromium.org (2010-12-20)

Downgrading to high-severity because of the user interaction required to trigger.

### js...@chromium.org (2011-01-04)

This code's changed quite a bit, so the merge to m8 looks very risky. Should be able to merge to m9 when the branch reopens.

### sc...@gmail.com (2011-01-05)

@avrelian234567: congratulations! This bug turned out to be a security issue,
and as such it has provisionally qualified for a $500 Chromium Security Reward.
---
NOTE: normally we do not reward security bugs unless initially filed with the
security templaye. Sometimes we make an exception for the first time an individual
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

### av...@gmail.com (2011-01-05)

Thank you.

I am sorry for not filing the bug as a security issue.
I was not aware it could be of this kind.

To be honest, as soon as I had submitted the bug, I have shared the link http://code.google.com/p/chromium/issues/detail?id=63732 with two of my friends. As far as I know they didn't share this information with anybody. Shortly afterwords this page was made hidden for third parties.

Regards,
Sergey Radchenko

### sc...@gmail.com (2011-01-05)

@avrelian234567: thanks for your honesty! The reward will still stand :D
Thanks for helping make Chromium stronger.
I expect we'll release the fix with the Chrome 9 release. If you could keep the bug confidential until then, that would be awesome!

Would you like us to credit you using your name of "Sergey Radchenko" ?

### av...@gmail.com (2011-01-05)

That's great!

I would prefer to be credited by my name - Sergey Radchenko.

Thank you.

### ch...@gmail.com (2011-01-11)

merged to m9 as 71093

### ch...@gmail.com (2011-01-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-19)

Aaron, can you please check the reasons for crashes introduced by m9 merge, it was reverted by @laforge in http://svnsearch.org/svnsearch/repos/CHROMIUM/search?logMessage=revert%2071093

### ch...@gmail.com (2011-02-10)

merged to m9 (finally) as 74473

### in...@chromium.org (2011-02-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-11)

w00t

### sc...@gmail.com (2011-03-01)

@avrelian234567 -- we released the fix to stable in 9.0.597.107
Please e-mail cevans@chromium.org and I'll help get you set up to collect your reward.

### la...@chromium.org (2011-03-19)

Chrome Version : 7.0.517.44  

URLs (if applicable) : <http://4su.ru/index.html>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 5: OK  

Firefox 3.x: OK  

IE 7/8: OK

**What steps will reproduce the problem?**

1. go to <http://4su.ru/index.html>
2. check "Prevent this page from creating additional dialogs."
3. close either tab with <http://4su.ru/index.html> or application

**What is the expected result?**  

tab or application should be closed

**What happens instead?**  

crash following by hanging of application. One time it comes along with drwtsn32 crash.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-11-23)

Payment _finally_ in system. That took too long; I apologize.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/63732?no_tracker_redirect=1

[Multiple monorail components: Internals, UI>Browser>TabContents]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085084)*
