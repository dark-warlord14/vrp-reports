# Security: Chrome extensions bug cause crash in all Chrome processes

| Field | Value |
|-------|-------|
| **Issue ID** | [40061425](https://issues.chromium.org/issues/40061425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI |
| **Reporter** | ni...@gmail.com |
| **Assignee** | mp...@chromium.org |
| **Created** | 2012-07-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Hi,

I found an interesting crash in chrome's extension mechanism - it's related to the XMLHttpRequest object.

This crash is interesting becuase it carshes all chrome processes (!)  

This crash its most likely a security-related issue, as it is most likely caused by jumping to an illegal address (SEGFAULT).

You can reproduce the crash by installing the attached chrome extension and execute it.

You can see in the example (attached) chrome crash after:  

xhr.open("GET", "<http://api.duckduckgo.com/?q=>" + search\_value + "&format=json", true);

I also added a crash dump.

for more information you can contact me via email:  

[nmoshe@nds.com](mailto:nmoshe@nds.com)  

[0xlaser@walla.com](mailto:0xlaser@walla.com)

Nir.

**VERSION**  

Chrome Version: [20.0.1132.57] + [stable]  

Operating System: Windows 7

**REPRODUCTION CASE**  

Please include a demonstration of the security bug, such as an attached.  

I added a simple demo (chrome extension) that reproduce the crash: manifest.json + popup.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser, all chrome processes  

Crash State:  

Client ID (if relevant):

## Attachments

- [chrome.dmp](attachments/chrome.dmp) (application/octet-stream; charset=binary, 173.6 KB)
- [popup.html](attachments/popup.html) (text/html; charset=us-ascii, 777 B)
- [manifest.json](attachments/manifest.json) (text/plain; charset=us-ascii, 363 B)

## Timeline

### js...@chromium.org (2012-07-17)

This certainly looks ugly. Here's a search for similar crashes:
http://crash.corp.google.com/search?query=crashed_thread_function_name.contains%3A%22ChromeJavaScriptDialogCreator%3A%3ACancelPendingDialogs%22+-crash_address%3A%220%22

Anyone on the CC know where I should direct this for a quick turnaround?

### pk...@chromium.org (2012-07-17)

I looked at one crash stack and it had Extensions on the list, as well as TabContents teardown stuff, so I'm going to replace myself with some people who might know more about those.

### [Deleted User] (2012-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2012-07-18)

Opps wrong bug

### js...@chromium.org (2012-07-18)

Yep, there are some reports with WebHost, but none of them are exploitable crashes and the stack is different. So, it looks like the security bug is triggered only by ExtensionHost.

@aa - Could you direct this one to someone appropriate?

### aa...@chromium.org (2012-07-19)

Probably some expectation that WebContents has that we aren't fulfilling.

### ni...@gmail.com (2012-07-19)

Maybe it is related to the XMLHttpRequest timeout ?

http://www.w3.org/TR/XMLHttpRequest/#dom-xmlhttprequest-timeout
and 
http://www.w3.org/TR/XMLHttpRequest/#the-open-method

### av...@chromium.org (2012-07-19)

This isn't crashing on my Mac, so I can't comment from there, but looking at the backtrace from a sample crash pointed to by Justin:

ChromeJavaScriptDialogCreator::CancelPendingDialogs(content::WebContents *)
ChromeJavaScriptDialogCreator::ResetJavaScriptState(content::WebContents *)
WebContentsImpl::~WebContentsImpl()
WebContentsImpl::`vector deleting destructor'(unsigned int)
ExtensionHost::~ExtensionHost()

ExtensionHost gets destructed, so it kills the WebContents that it owns. The WebContents, in its destructor, calls back to the module providing Javascript dialogs, asking it to clear state. Boom.

I was working with an external contributor in this code, since I did the last big work on Javascript dialogs, and in ExtensionHost I made sure that he made the dialog creator precede the WebContents so it would outlive it. So it's not immediately obvious to me what's wrong.

I'm going to build Chrome on Windows to track this down, though it's been a while and I suspect I won't have answers for a while. If anyone wants to also poke at this, fire any questions about this area of the code to me; it's mine.

### av...@chromium.org (2012-07-23)

ChromeJavaScriptDialogCreator::CancelPendingDialogs(content::WebContents *) kills open dialogs. Further down on the stack is:

views::View::DoRemoveChildView(views::View *,bool,bool,bool)
views::View::RemoveAllChildViews(bool)
views::internal::RootView::~RootView()

How are dialogs implemented on Views? If they depend on the RootView, then it might make sense that trying to manipulate the currently-open dialog might crash.

I'm failing to reproduce on my Windows build, but I'm still happy to help.

### mp...@chromium.org (2012-07-26)

Based on my rudimentary reading of the disassembly[1] in WinDbg, it's crashing because the active_dialog of AppModalDialogQueue is non-NULL but garbage. Maybe there is a javascript alert open when the popup is dismissed, and the alert dialog is deleted just before the popup is deleted. I don't know much about AppModalDialogs, so I don't understand why the dialog could be deleted without notifying the queue and removing itself as active.

[1] chrome_1c30000!ChromeJavaScriptDialogCreator::CancelPendingDialogs:
02aeecb6 55              push    ebp
02aeecb7 8bec            mov     ebp,esp
02aeecb9 83ec10          sub     esp,10h
02aeecbc 56              push    esi
02aeecbd 57              push    edi
02aeecbe e8985b52ff      call    chrome_1c30000!AppModalDialogQueue::GetInstance (0201485b)
02aeecc3 8b7d08          mov     edi,dword ptr [ebp+8]
02aeecc6 8bf0            mov     esi,eax
02aeecc8 8b4e20          mov     ecx,dword ptr [esi+20h]
02aeeccb 85c9            test    ecx,ecx
02aeeccd 740a            je      chrome_1c30000!ChromeJavaScriptDialogCreator::CancelPendingDialogs+0x23 (02aeecd9)
02aeeccf 397928          cmp     dword ptr [ecx+28h],edi
02aeecd2 7505            jne     chrome_1c30000!ChromeJavaScriptDialogCreator::CancelPendingDialogs+0x23 (02aeecd9)
02aeecd4 8b01            mov     eax,dword ptr [ecx]
02aeecd6 ff5004          call    dword ptr [eax+4]
02aeecd9 56              push    esi  <<<=== crashes here, or maybe 1 line up


### av...@chromium.org (2012-07-26)

> Maybe there is a javascript alert open when the popup is dismissed

I'm pretty certain there is.

> I don't understand why the dialog could be deleted without notifying the queue and removing itself as active.

That's why I was asking about the views::View calls on the stack. Are the AppModalDialogs under views implemented in such a way that they would get torn down but leave the pointer dangling?


### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### in...@chromium.org (2012-08-16)

This bug is part of security bug yellow, do you think we will have a fix in time for m22 ?

### mp...@chromium.org (2012-08-16)

I don't think this will be fixed by M22. But I'll take another look. Last time didn't turn up much insight.

### mp...@chromium.org (2012-08-21)

OK, I was able to reproduce this on Windows. What's happening is that ExtensionPopup is closing itself directly when it loses focus. This seems to close the alert dialog as well (maybe because it is in the view hierarchy?). The AppModalDialog is deleted as the widget's delegate.

The ExtensionHost still isn't deleted in all this time, and won't be deleted until the ExtensionPopup is deleted. The dialog is cancelled from within ~ExtensionHost, and that's where the boom happens.

Not sure what the right fix is. Maybe we should have ~AppModalDialog cancel itself if it hasn't been already. Or maybe we should delete ExtensionHost earlier. I'll keep looking.

### av...@chromium.org (2012-08-21)

> What's happening is that ExtensionPopup is closing itself directly when it loses focus. This seems to close the alert dialog as well (maybe because it is in the view hierarchy?).

BTW, this is the key difference between this on the Mac and on Windows. On the Mac, the alert box is independent so it outlives the ExtensionPopup, and then it's around to be torn down when ~ExtensionHost is hit. Your suspicions seem reasonable.

> Maybe we should have ~AppModalDialog cancel itself if it hasn't been already.

That seems like a pretty good idea anyway.

### bu...@chromium.org (2012-08-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=152716

------------------------------------------------------------------------
r152716 | mpcomplete@chromium.org | 2012-08-22T03:15:56.168890Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/app_modal_dialogs/app_modal_dialog.cc?r1=152716&r2=152715&pathrev=152716
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/app_modal_dialogs/app_modal_dialog.h?r1=152716&r2=152715&pathrev=152716

Fix a Windows crash bug with javascript alerts from extension popups.

BUG=137707


Review URL: https://chromiumcodereview.appspot.com/10828423
------------------------------------------------------------------------

### in...@chromium.org (2012-08-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-22)

Matt, 144105 definitely looks like dup (exactly same stack), but also had a good test. if you get a chance, mind confirming that it is dup.

### mp...@chromium.org (2012-08-22)

https://crbug.com/chromium/144105 does seem like a dupe. I can only repro it if I skip step 3, but then it is the same crash.

### in...@chromium.org (2012-08-22)

Thanks a lot Matt for confirming. Really appreciate it.

### sc...@gmail.com (2012-09-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=155002

------------------------------------------------------------------------
r155002 | cevans@chromium.org | 2012-09-05T20:07:18.195781Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/browser/ui/app_modal_dialogs/app_modal_dialog.cc?r1=155002&r2=155001&pathrev=155002
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/browser/ui/app_modal_dialogs/app_modal_dialog.h?r1=155002&r2=155001&pathrev=155002

Merge 152716 - Fix a Windows crash bug with javascript alerts from extension popups.

BUG=137707


Review URL: https://chromiumcodereview.appspot.com/10828423

TBR=mpcomplete@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10928004
------------------------------------------------------------------------

### sc...@gmail.com (2012-09-22)

Thank you Nir. With what name would you like to be credited in our release notes? So far I have "Nir Moshe"

### ni...@gmail.com (2012-09-23)

"Nir Moshe" is ok :)

### sc...@gmail.com (2012-09-25)

@nmoshe@nds.com: thanks for the credit details!

This also qualifies for a $500 Chromium Security Reward :D Congrats.

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

### ni...@gmail.com (2012-09-27)

Thanks :)
Will you publish my name in the "Security Hall of Fame"?

### sc...@gmail.com (2012-09-27)

Sure thing! I'll try and do it later.

### sc...@gmail.com (2012-12-14)

Payment in system.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sr...@chromium.org (2014-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/137707?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI]
[Monorail mergedwith: crbug.com/chromium/143708, crbug.com/chromium/144105]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061425)*
