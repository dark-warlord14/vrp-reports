# Use after free - using speech API after loading a web page 

| Field | Value |
|-------|-------|
| **Issue ID** | [40077264](https://issues.chromium.org/issues/40077264) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Speech, UI>Browser>Navigation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-03-19 |
| **Bounty** | $1,000.00 |

## Description

Hi again,

1. Open PoC.html

2. In PoC.html we have speech API and then after almost a second it's loading google page so you should click only one click before loading of google page and you can get "speech API" then after loading of google page you can see "speech API" it's still on page even after changing of the page.

3. Then you can see a message on speech API "Speech recognition was aborted" and click on "try again" button and Chrome will crash.


0:017> k
ChildEBP RetAddr  
0572f98c 034c2d23 chrome_1c30000!`anonymous namespace'::PureCall+0x3 [c:\b\build\slave\win\build\src\content\app\startup_helper_win.cc @ 24]
0572f9ac 031e179e chrome_1c30000!_purecall+0x12 [f:\dd\vctools\crt_bld\self_x86\crt\src\purevirt.c @ 54]
0572faa8 031e055b chrome_1c30000!content::SpeechRecognitionManagerImpl::RecognitionAllowedCallback+0x18c [c:\b\build\slave\win\build\src\content\browser\speech\speech_recognition_manager_impl.cc @ 182]
0572fac0 031e05b9 chrome_1c30000!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::SpeechRecognitionManagerImpl::*)(int,bool,bool)>,void __cdecl(base::WeakPtr<content::SpeechRecognitionManagerImpl> const &,int const &,bool const &,bool const &)>::MakeItSo+0x4a [c:\b\build\slave\win\build\src\base\bind_internal.h @ 973]
0572fae0 02bf1d77 chrome_1c30000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::SpeechRecognitionManagerImpl::*)(int,bool,bool)>,void __cdecl(content::SpeechRecognitionManagerImpl *,int,bool,bool),void __cdecl(base::WeakPtr<content::SpeechRecognitionManagerImpl>,int)>,void __cdecl(content::SpeechRecognitionManagerImpl *,int,bool,bool)>::Run+0x1f [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1495]
0572faf4 02b1f100 chrome_1c30000!base::internal::InvokeHelper<0,void,base::Callback<void __cdecl(int,std::vector<history::MostVisitedURL,std::allocator<history::MostVisitedURL> >)>,void __cdecl(int const &,std::vector<history::MostVisitedURL,std::allocator<history::MostVisitedURL> > const &)>::MakeItSo+0xf [c:\b\build\slave\win\build\src\base\bind_internal.h @ 899]
0572fb0c 01c622f7 chrome_1c30000!base::internal::Invoker<2,base::internal::BindState<base::Callback<void __cdecl(bool,bool)>,void __cdecl(bool,bool),void __cdecl(bool,bool)>,void __cdecl(bool,bool)>::Run+0x20 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1257]
0572fb68 01c62072 chrome_1c30000!MessageLoop::RunTask+0x1e3 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 475]
0572fcb8 01c6519b chrome_1c30000!MessageLoop::DoWork+0x2ec [c:\b\build\slave\win\build\src\base\message_loop.cc @ 669]
0572fd1c 01c650a9 chrome_1c30000!base::MessagePumpForIO::DoRunLoop+0xe7 [c:\b\build\slave\win\build\src\base\message_pump_win.cc @ 523]
0572fd3c 01c61cd2 chrome_1c30000!base::MessagePumpWin::Run+0x3e [c:\b\build\slave\win\build\src\base\message_pump_win.h @ 48]
0572fd60 01c61c2a chrome_1c30000!MessageLoop::RunInternal+0x72 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 431]
0572fd70 01c65043 chrome_1c30000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 46]
0572fd98 01d5707f chrome_1c30000!base::Thread::Run+0x34 [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 150]
0572fe68 01d42294 chrome_1c30000!content::BrowserThreadImpl::IOThreadRun+0x2b [c:\b\build\slave\win\build\src\content\browser\browser_thread_impl.cc @ 150]
0572fe7c 01c64eaa chrome_1c30000!content::BrowserThreadImpl::Run+0x86 [c:\b\build\slave\win\build\src\content\browser\browser_thread_impl.cc @ 177]
0572ffa8 01c64dcc chrome_1c30000!base::Thread::ThreadMain+0xd7 [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 199]
0572ffb4 7c80b713 chrome_1c30000!base::`anonymous namespace'::ThreadFunc+0x1a [c:\b\build\slave\win\build\src\base\threading\platform_thread_win.cc @ 60]
WARNING: Stack unwind information not available. Following frames may be wrong.
0572ffec 00000000 kernel32!GetModuleFileNameA+0x1b4

## Attachments

- [PoC.html](attachments/PoC.html) (text/html; charset=us-ascii, 753 B)
- [1.PNG](attachments/1.PNG) (image/png; charset=binary, 37.7 KB)
- [2.PNG](attachments/2.PNG) (image/png; charset=binary, 80.0 KB)

## Timeline

### js...@chromium.org (2013-03-19)

I can't get this to reproduce, because the navigation occurs too fast. Could you please enable crash reporting and post a crash ID so we have more context to work from?

site isolation people - There seems to be something very fishy going on with the navigation here. The blocked popup notification appears for a fraction of a second, and then then page navigates to the location of the window.open. Could one of you take a look?

### pa...@chromium.org (2013-03-20)

Justin, I'm going to assign you owner just to make sure someone follows up with Khalil (or closes the issue if we can't duplicate).

### js...@chromium.org (2013-03-20)

Closed due to lack of feedback. If we get more information I'll reaopen. Although, I'd still like someone to clarify what's going on with that navigation.

### ch...@gmail.com (2013-03-20)

[Comment Deleted]

### cr...@chromium.org (2013-03-20)

The explanation is indeed unclear, but it's a valid bug.  It's much easier to repro if you change the 200 ms timeout to 5 seconds.

I see two independent problems.  The first is the wacky popup behavior Justin noticed: if you do a cross-process navigation in a blocked popup, the navigation appears to commit in the tab that opened.  Bad news.

The second problem is that we're leaving around the speech bubble after a cross-process navigation commits.  That's independent of the first problem.  If you replace all the window.open stuff in the setTimeout with window.location = "https://chrome.google.com/webstore", we'll force a process swap and the same thing happens.  I'm not familiar with the speech bubble stuff, but that seems like what this bug report is really about.

I'll file a separate bug for the blocked popup issue and maybe we can find someone to look at the speech bubble thing.

### cr...@chromium.org (2013-03-20)

For reference, the speech bubble crash is in SpeechRecognitionManagerImpl::OnRecognitionError.
Crash id: db3e6326b1809b24

Looks like it only crashes if you navigate while it's still setting up.  If the microphone input is already working, then the bubble gets cleared when you navigate away.  Perhaps it just isn't handling a navigation event properly while setting up.

@tommi, can you help triage?

### cr...@chromium.org (2013-03-20)

Filed https://crbug.com/chromium/222568 to fix the blocked popup issue mentioned in https://crbug.com/chromium/222000#c5.

### cr...@chromium.org (2013-03-21)

Dale, maybe you can take a look?  There's a crash ID in https://crbug.com/chromium/222000#c6.

### da...@chromium.org (2013-03-22)

Looks like something is destroying SpeechRecognitionSessionConfig::event_listener, but never calling AbortSession(), so a SpeechRecognitionSessionConfig sticks around holding a raw pointer to an event listener that no longer exists.

It appears that there are about four different ways sessions can be created and destroyed. I don't see anything obvious in what could be going wrong. tommi or xians will know better.

Also, I repro'd the crash on Windows here so I could get a WinDBG accessible dump :)

https://crash.corp.google.com/reportdetail?reportid=8ebef9b085e87164

### ch...@gmail.com (2013-03-22)

Looks like it's a complex bug 

### js...@chromium.org (2013-03-26)

This is a browser crash, but the carefully timed user interaction seems enough of a bar to rate high-severity rather than critical. That said, it's a browser crash so I'm still making it a pri-0.

Was anyone able to determine if this impacts stable (since I couldn't repro it, even after fiddling with the timeout as @creis had)?

### to...@chromium.org (2013-03-26)

Tommy - can you take a look at this?

### [Deleted User] (2013-03-27)

I spent some time on the crash log and the code, the problem is not on Webkit but in the chromium speech code.

When clicking try again, we try to restart the session by copying the previous session info and make a new one:
void ChromeSpeechRecognitionManagerDelegate::RestartLastSession() {
  DCHECK(last_session_config_.get());
  SpeechRecognitionManager* manager = SpeechRecognitionManager::GetInstance();
  DLOG(WARNING) << "RestartLastSession CreateSession";
  const int new_session_id = manager->CreateSession(*last_session_config_);
  DCHECK_NE(SpeechRecognitionManager::kSessionIDInvalid, new_session_id);
  last_session_config_.reset();
  manager->StartSession(new_session_id);
}

Note that last_session_config_ contains the pointer of the listener, and I believe we simply copy the pointer to the new session but then soon release the object.

Tommy is on vacation this week and I will take over the issue.


### [Deleted User] (2013-03-27)

After digging into the code more, I finally understand what has happened.
In ChromeSpeechRecognitionManagerDelegate, we copy and store the session configuration to last_session_config_, which includes the SpeechRecognitionDispatcherHost as the event_listener in the struct.
And in PoC.htm, it will load the google page after timeout, which will remove the old SpeechRecognitionDispatcherHost and create the new one. But since the "try again" will try to re-use the configuration of the previous session to create a new session, it is then trying to access the SpeechRecognitionDispatcherHost which has gone away.

I have quite little understanding on the speech API and a bit not sure what we should do in this case that the render view has gone: should we just close the bubble when the old render view is going away? or simply invalidate the "try again" action?

I made a CL https://codereview.chromium.org/12982009 to avoid the crash by simply invalidating the "try again", but let me know if you guys think it is not a appropriate solution to the issue.


### [Deleted User] (2013-04-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-04)

------------------------------------------------------------------------
r192299 | xians@chromium.org | 2013-04-04T11:37:11.674705Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/speech/chrome_speech_recognition_manager_delegate.cc?r1=192299&r2=192298&pathrev=192299

Fixed the speech crash when the render view has gone away then users click "try again".

After a speech recognition session is done, chrome will pop up a bubble to allow users to choose "cancel" or "try again".
If the users choose "try again", it will use the last session's SpeechRecognitionSessionConfig which is stored in ChromeSpeechRecognitionManagerDelegate to create a new session.
But the render view might have gone away if the page is automatically refreshed to another url. Then the event_listener in the SpeechRecognitionSessionConfig is not valid anymore and should not be used.

This patch added a OnAbortSessionsForListener callback from SpeechRecognitionManagerImpl to ChromeSpeechRecognitionManagerDelegate to notify chrome we should not try to restore the session for "try again" event.

BUG=222000
TEST=open the PoC.html in the issue, click on the page and then click on "try again" button.

Review URL: https://chromiumcodereview.appspot.com/12982009
------------------------------------------------------------------------

### [Deleted User] (2013-04-04)

Ted, could you please verify the fix after it gets to canary? We need to merge it to the branch.

### in...@chromium.org (2013-04-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2013-04-05)

Is this report qualified for a chromium security reward ?

### js...@chromium.org (2013-04-05)

Seems like it would be.

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-08)

------------------------------------------------------------------------
r192849 | xians@chromium.org | 2013-04-08T18:43:19.926596Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1453/src/chrome/browser/speech/chrome_speech_recognition_manager_delegate.cc?r1=192849&r2=192848&pathrev=192849

Merge 192299 - Fixed the speech crash when the render view has gone away then users click "try again".

After a speech recognition session is done, chrome will pop up a bubble to allow users to choose "cancel" or "try again".
If the users choose "try again", it will use the last session's SpeechRecognitionSessionConfig which is stored in ChromeSpeechRecognitionManagerDelegate to create a new session.
But the render view might have gone away if the page is automatically refreshed to another url. Then the event_listener in the SpeechRecognitionSessionConfig is not valid anymore and should not be used.

This patch added a OnAbortSessionsForListener callback from SpeechRecognitionManagerImpl to ChromeSpeechRecognitionManagerDelegate to notify chrome we should not try to restore the session for "try again" event.

BUG=222000
TEST=open the PoC.html in the issue, click on the page and then click on "try again" button.

Review URL: https://chromiumcodereview.appspot.com/12982009

TBR=xians@chromium.org
Review URL: https://codereview.chromium.org/13801016
------------------------------------------------------------------------

### [Deleted User] (2013-04-08)

I saw lots of crash reports in M26, should we also merge it to M26?

### ke...@chromium.org (2013-04-08)

Thanks for doing that, but we usually do merges for security fixes ourselves in advance of the patch going out.

### sc...@gmail.com (2013-04-16)

For now, I'm going to mark this as dealt with in M27 but if there's another M26 security patch we can revisit.

### ch...@gmail.com (2013-04-30)

Chris, Please you can credit me as "Khalil Zhani" when the time of the release :)

### sc...@gmail.com (2013-05-03)

Thank you Khalil! And we're happy to issue you a $1000 Chromium Security Reward for finding and helping us get to the bottom of this issue :D

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### ch...@gmail.com (2013-05-04)

Thank you so much Chris !!

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/222000?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Speech, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077264)*
