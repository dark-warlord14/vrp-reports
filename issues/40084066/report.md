# Use after free of m_frame in FrameLoader::loadWithDocumentLoader

| Field | Value |
|-------|-------|
| **Issue ID** | [40084066](https://issues.chromium.org/issues/40084066) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | gu...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-10-22 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 8.0.552.5 (Official Build 62886) dev  

**URLs (if applicable) :**  

<http://i.nconspicuo.us/2007/12/21/outlook-2007-does-not-shutdown-on-exit-outlookexe-remains-in-task-manager/>

**What steps will reproduce the problem?**

1. Visit the URL above with AdBlock 2.2.6 installed
2. Middle click on the "See Post: Microsoft Outlook – Address List Cannot Be Displayed." link

**What is the expected result?**

It is opened.

**What happens instead?**

Aw, Snap!

This also happens in Chrome 6. I'm in Windows 7.

## Timeline

### th...@chromium.org (2010-10-22)

Does it happen if you turn off adblock?

Can you get a crash report id?
http://dev.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug

### [Deleted User] (2010-10-23)

Confirmed:
21e59f971cc33339

### th...@chromium.org (2010-10-25)

0x6938358a 	[chrome.dll 	- chrome_dll_main.cc:163] 	`anonymous namespace'::PureCall()
0x69f9828c 	[chrome.dll 	- purevirt.c:47] 	_purecall
0x698509fd 	[chrome.dll 	- frameloader.cpp:2024] 	WebCore::FrameLoader::clientRedirectCancelledOrFinished(bool)
0x698523d1 	[chrome.dll 	- frameloader.cpp:2917] 	WebCore::FrameLoader::continueLoadAfterNavigationPolicy(WebCore::ResourceRequest const &,WTF::PassRefPtr<WebCore::FormState>,bool)
0x6984fb18 	[chrome.dll 	- frameloader.cpp:1475] 	WebCore::FrameLoader::loadWithDocumentLoader(WebCore::DocumentLoader *,WebCore::FrameLoadType,WTF::PassRefPtr<WebCore::FormState>)
0x6984f853 	[chrome.dll 	- frameloader.cpp:1405] 	WebCore::FrameLoader::loadWithNavigationAction(WebCore::ResourceRequest const &,WebCore::NavigationAction const &,bool,WebCore::FrameLoadType,WTF::PassRefPtr<WebCore::FormState>)
0x69851cca 	[chrome.dll 	- frameloader.cpp:2738] 	WebCore::FrameLoader::loadPostRequest(WebCore::ResourceRequest const &,WTF::String const &,WTF::String const &,bool,WebCore::FrameLoadType,WTF::PassRefPtr<WebCore::Event>,WTF::PassRefPtr<WebCore::FormState>)
0x6984f19c 	[chrome.dll 	- frameloader.cpp:1282] 	WebCore::FrameLoader::loadFrameRequest(WebCore::FrameLoadRequest const &,bool,bool,WTF::PassRefPtr<WebCore::Event>,WTF::PassRefPtr<WebCore::FormState>,WebCore::ReferrerPolicy)
0x6985ab13 	[chrome.dll 	- navigationscheduler.cpp:199] 	WebCore::ScheduledFormSubmission::fire(WebCore::Frame *)
0x6985b052 	[chrome.dll 	- navigationscheduler.cpp:362] 	WebCore::NavigationScheduler::timerFired(WebCore::Timer<WebCore::NavigationScheduler> *)
0x69b4c894 	[chrome.dll 	- timer.h:98] 	WebCore::Timer<WebCore::V8GCForContextDispose>::fired()
0x69a21b2c 	[chrome.dll 	- threadtimers.cpp:112] 	WebCore::ThreadTimers::sharedTimerFiredInternal()
0x69a21a9f 	[chrome.dll 	- threadtimers.cpp:90] 	WebCore::ThreadTimers::sharedTimerFired()
0x69445e58 	[chrome.dll 	- message_loop.cc:410] 	MessageLoop::RunTask(Task *)

### [Deleted User] (2010-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2010-10-25)

This is happening on Stable build(7.0) as well.

### in...@chromium.org (2010-10-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-26)

Have a patch ready. uploading soon - https://bugs.webkit.org/show_bug.cgi?id=48281

### in...@chromium.org (2010-10-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-26)

Fixed in http://trac.webkit.org/changeset/70517. Needs merging to v7, v8 branches. This is too simple and no risk merge.

### in...@chromium.org (2010-10-26)

merged to m7 in r70526, m8 in r70527.

### sc...@gmail.com (2010-10-28)

@gundlach: congratulations! This bug provisionally qualifies for a $500 Chromium Security Reward.
Although this bug was not filed originally as a security bug, it was found to be a security bug. This report was therefore useful to us, hence the reward.
We will require that future reports be filed as security bugs in order to qualify for rewards. If in doubt, feel free to file "Aw, snap" bugs a security bugs -- some fraction of "Aw, snap"s have security consequence.

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

### gu...@gmail.com (2010-10-28)

Be aware that this was first reported by an AdBlock user at http://www.google.ru/support/forum/p/Chrome/thread?tid=6f36f12985d34078&hl=en .  So 1) I don't know that I'm the correct recipient of the reward, even though I'm the first to file a crbug about the issue; and 2) this probably counts as "disclosed".

### sc...@gmail.com (2010-10-28)

Hmm, the lineage of this bug is getting complicated :)
Any objections if we just donate this to charity?

### sc...@gmail.com (2010-11-03)

Donating to charity due to lack of objections :)

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/60238?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/60446]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084066)*
