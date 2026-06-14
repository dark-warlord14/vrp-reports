# Stale observer in BrowsingDataRemover's observer_list_

| Field | Value |
|-------|-------|
| **Issue ID** | [40090691](https://issues.chromium.org/issues/40090691) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | th...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-05-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Reloading a page with a certain type/amount of cookies crashes Chrome while erasing history. Google Chrome goes down completely when the steps below are carried out.

It seems that the way some sites use cookies prevents the history erase process from completing. Once the tab is closed, the process may still access the cookies in use by the site. Once this site is reloaded, Chrome crashes completely.

**VERSION**  

Chrome Version: 11.0.696.65 stable  

Operating System: Windows XP SP3 & Ubuntu 11.04

**REPRODUCTION CASE**

1. Start Google Chrome with 1 tab (don't load previously closed tabs)
2. Load "www.twitter.com/google" (has something to do with the way Twitter (and some other sites) handles cookies)
3. Launch "Customize and control Google Chrome->History->Edit items...  
   
   ->Clear all browsing data..."
4. Check all checkboxes and select "beginning of time" from the combobox
5. Press the "Clear browsing data" button and wait for a while (does not close!!!!)
6. Press "Cancel"
7. Now press the "Clear browsing data..." button (brings up the dialog again) and press the "Clear browsing data" button and leave it running
8. Close the "Options - Under the Hood" tab while the "Clear Browsing Data" dialog/process still runs
9. Now reload the "www.twitter.com/google" page from the first tab
10. Full browser crash with 11.0.696.65!

I did not include extra crash information because I think that this crash is not difficult to reproduce. I'd be happy to do so if necessary.

## Attachments

- [issue_81916_stale_observer.html](attachments/issue_81916_stale_observer.html) (text/html; charset=us-ascii, 550 B)

## Timeline

### th...@gmail.com (2011-05-08)

I tested some more and found the following:

1. 
It does not matter which settings you use on the "Clear Browsing Data" form/dialog as long as "Delete cookies and other site data" is checked and Chrome is started without history. 

So this checkbox/setting causing the problem. If it is unchecked, the 
erase process doesn't stall and Chrome no longer crashes.

2. 
Chrome does not have to be started with no tabs open. You can restore/open as many as you want as long as you carry out the steps in my first post. However, I found that with multiple Twitter tabs open, only the first Twitter page/tab seems to
cause a crash upon reloading.

3. 
I have been unable to get a crashid from Chrome. Windows shows the default crash dialog with a message that an application has crashed (and generates a stalled application event), but there is no Chrome event saying that the crash data has been uploaded to Google (with Automatically send... checked).

Chome (Chromium) on Linux (Ubuntu 11.04) shows a "Pure virtual function call" error when launched from the console, but not every time. Sometimes the whole Chrome window with its tabs just disappears. It crashes everytime though.

After more testing (on Linux with gdb) multiple errors occurred. One of them is a "Segmentation fault".

4.
Twitter has more offline storage than most other sites. It does not only use cookies, but also (HTML5) "Database Storage" and "Local Storage".

And the "Database storage" part is the problem. The history erase process stalls when a connection with a local database is made (HTML5).

I prepared a small HTML file that can be used instead of "www.twitter.com/google" to show it. Just replace step 1 and step 9 with the following
html file.

<html>
<body>

<script type="text/javascript">
//Chromium https://crbug.com/chromium/81916

document.write("<h1>Reloading a page with a certain type/amount of cookies crashes Chrome while erasing history (https://crbug.com/chromium/81916)</h1>");
document.write("<p>Follow the 10 steps of the first post!</p>");

openDatabase('documents', '1.0', 'Local test storage', 5*1024*1024, function (db) {
   db.changeVersion('', '1.0', function (t) {
     t.executeSql('CREATE TABLE IF NOT EXISTS TEST (testid, testname, othertestdata)');
   }, error);
});
</script>

</body>
</html>


### th...@gmail.com (2011-05-09)

Here are some simplified steps to generate the crash:

1. Load the html file from the comment above (in a clean browser session because other HTML5 (storage) based sites/files may interfere)
2. Erase history with at least "Delete cookies and other site data" checked (does not close!!!)
3. Cancel it and erase again (stalls again!!)
4. Close the tab "Options - Clear Browsing Data" while the erase process is still active
5. Reload the first html file
6. Crash!

### ch...@gmail.com (2011-05-10)

Ok I believe I've tracked this down..

The crash occurs in BrowsingDataRemover::NotifyAndDeleteIfDone() when calling OnBrowsingDataRemoverDone() for each entry in the observer_list_. One of the entries seems to be stale at this point.

This also triggers the DCHECK in BrowsingDataRemover::Remove() when it is called from ClearBrowserDataHandler::HandleClearBrowserData() the second time that you clear browsing data.

I don't think there is a way to get to this without a ton of user interaction though so I am going to mark this SecSeverity-None for now until someone who knows this code can comment.

### ch...@gmail.com (2011-05-11)

Eric, can you help with an owner for this?

### er...@chromium.org (2011-05-11)

Michael--looks like another database race of some kind.  Would you have time to look at it, given that you're already in it up to your elbows?

### mi...@chromium.org (2011-05-11)

<rant>Who is cdn? content-distribution-network... names please </rant>

Given that this is easily reproducible should be straight forward to debug but I'm feeling a kind of time pressed with quota stuff right now.



### mi...@chromium.org (2011-05-11)

ah... cris neckar! thnx for using the name @google.com ldap name

### ch...@gmail.com (2011-05-11)

If I followed the trend set by my security brethren I would be something like D0ct0rD00m@chromium.org so be thankful :P

### mi...@chromium.org (2011-05-17)

I just tried to dup this given the steps in https://crbug.com/chromium/81916#c2, but it did not repro for me (i'm running tip-of-tree win7. The "clear all" tasks complete quickly so there's no change to cancel or close anything while it's still running.

Mildly related... i do hit a ThreadRestriction assertion while clearing all browsing data... InMemoryURLIndex::SaveToCacheFile() is being called on the main thread.


### th...@gmail.com (2011-05-17)

[Comment Deleted]

### th...@gmail.com (2011-05-17)

I wonder how you reproduced the steps of https://crbug.com/chromium/81916#c2. Did you leave the loaded file open? Or did you close it?

Does the original report reproduce the issue on your system?

Concluding from your comment that the history process closed quickly, you must have closed the file before the erase process began. Or am I drawing the wrong conclusions here and is there a difference between Ubuntu and WinXP SP3 on one side and Windows 7 (and Vista?) (64-bit?) on the other?

If you close the file (or Twitter site, or any site with this type of HTML5 database open), the history process continues normally (even if you close it while erasing history).

Build 13.0.768.0 (85602) crashes here when following the 6 steps from https://crbug.com/chromium/81916#c2 on Windows XP SP3.

I will try the Linux edition later on, but I have no doubt that it will crash there 
too.

There might be a slight difference between the original report and https://crbug.com/chromium/81916#c2, but when I filed the issue, all builds (Stable/ToT) I've tried crashed on WinXP SP3 and Ubuntu 11.04 with the original report as well as the https://crbug.com/chromium/81916#c2 and (at least) on WinXP SP3 that hasn't changed thus far.

### mi...@chromium.org (2011-05-17)

I'll try again

### [Deleted User] (2011-05-18)

+rdsmith

### [Deleted User] (2011-05-18)

http://crbug.com/82309 may be a dup of this. We don't have a repro for it so I'm not sure if it will be helpful but figured I would make this doubly linked.

Michael, I added you on the other bug.

### [Deleted User] (2011-05-18)

This still repros for me on trunk.. When you do the second clear data it seems to hang for a bit in ReadFile which suggests something else is holding a handle to the local storage database file maybe. 

here is the stack trace at the point where it crashes


>	chrome.dll!BrowsingDataRemover::NotifyAndDeleteIfDone()  Line 334 + 0x34 bytes	C++
 	chrome.dll!BrowsingDataRemover::OnClearedDatabases(int rv=0)  Line 447	C++
 	chrome.dll!DispatchToMethod<BrowsingDataRemover,void (__thiscall BrowsingDataRemover::*)(int),int>(BrowsingDataRemover * obj=0x0e9d3c70, void (int)* method=0x5daad320, const Tuple1<int> & arg={...})  Line 551 + 0x11 bytes	C++
 	chrome.dll!RunnableMethod<BrowsingDataRemover,void (__thiscall BrowsingDataRemover::*)(int),Tuple1<int> >::Run()  Line 332 + 0x1e bytes	C++
 	base.dll!`anonymous namespace'::TaskClosureAdapter::Run()  Line 101 + 0x17 bytes	C++
 	base.dll!base::internal::Invoker1<0,base::internal::InvokerStorage1<void (__thiscall `anonymous namespace'::TaskClosureAdapter::*)(void),A0xa6a0e0f6::TaskClosureAdapter *>,void (__thiscall `anonymous namespace'::TaskClosureAdapter::*)(void)>::DoInvoke(base::internal::InvokerStorageBase * base=0x06cde538)  Line 547 + 0x1b bytes	C++
 	base.dll!base::Callback<void __cdecl(void)>::Run()  Line 251 + 0xe bytes	C++
 	base.dll!MessageLoop::RunTask(const MessageLoop::PendingTask & pending_task={...})  Line 475	C++
 	base.dll!MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 494	C++
 	base.dll!MessageLoop::DoWork()  Line 682 + 0xc bytes	C++
 	base.dll!base::MessagePumpForUI::DoRunLoop()  Line 203 + 0x1d bytes	C++
 	base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x009bb378, base::MessagePumpWin::Dispatcher * dispatcher=0x0038e040)  Line 51 + 0xf bytes	C++
 	base.dll!MessageLoop::RunInternal()  Line 444	C++
 	base.dll!MessageLoop::RunHandler()  Line 422	C++
 	base.dll!MessageLoopForUI::Run(base::MessagePumpWin::Dispatcher * dispatcher=0x0038e040)  Line 831	C++
 	chrome.dll!`anonymous namespace'::RunUIMessageLoop(BrowserProcess * browser_process=0x009bc9f0)  Line 647 + 0x1d bytes	C++
 	chrome.dll!BrowserMain(const MainFunctionParams & parameters={...})  Line 1879 + 0x11 bytes	C++


### rd...@chromium.org (2011-05-18)

That does look pretty similar to 82309.  Can you look at the assembly and see if we're crashing in the same spot?  I'm specifically curious if we crash when retrieving the virtual function pointer (i.e. pointer to unallocated memory of mis-aligned pointer) or when calling the virtual function pointer (i.e. contents of memory pointed to is bad, which would fit better with an observer being deleted without removing itself).



### [Deleted User] (2011-05-18)

5DAAC8A0  mov         edx,dword ptr [eax] <-- crash here 
5DAAC8A2  call        edx  

It crashes when grabbing the virtual function pointer. IE the vtable ptr is bad which suggests the object was deleted. EAX = 0xfeeefeee (I think this is a magic value the allocator uses as the next ptr to mark the end of a free list maybe)



### rd...@chromium.org (2011-05-18)

> It crashes when grabbing the virtual function pointer. 

Cool; I think we can consider these as having the same root cause (but hold till end of comment before duping).

> IE the vtable ptr is bad which suggests the object was deleted. EAX = 0xfeeefeee (I think this is a magic value the allocator uses as the next ptr to mark the end of a free list maybe)

Could you say more here?  My understanding of the assembly is that eax is a pointer to the observer object, not an entry from the vtable.  So it should still be a valid pointer even if the object has been deleted; it should simply point to memory that has garbage in it.  And in that case, the crash wouldn't occur on that line in the assembly; it would on the next line when the call occurred (because edx would be garbage).  What am I missing?  (I'm hoping you're right, because then I still have a theory for root cause :-}.)

Ignoring that confusion and presuming you're right, I'm not sure we should dup the bugs.  If the observer has been deleted without removing itself, that means that there's a bug in the observer code, and BrowsingDataRemover and DownloadItem will have different observers.  So they're different bugs.  Does that make sense?


### mi...@chromium.org (2011-05-18)

cc'ing jochen

### [Deleted User] (2011-05-18)

My reading is this

5DAAC896  mov         edx,dword ptr [obs] <-- we grab the first pointer in the observer object
5DAAC899  mov         eax,dword ptr [edx] <-- grab the vtable pointer from this table
....
5DAAC8A0  mov         edx,dword ptr [eax] <-- grab the first virtual function out of the vtable
5DAAC8A2  call        edx  <-- call the virtual function pointer

That being said I just ran through it with a breakpoint on the virtual destructor for Observer and I don't see it being called anywhere for the object that we eventually act on.. 

The basic chain of events in my reading is

1. load the page
2. clear browsing data
  a. We create a BrowserDataRemover object (we'll call it BDR1) and add an observer (ClearBrowserDataHandler or CBDH1) to its observer_list_
3. cancel clear browsing data
  a. I would expect to see CBDH1 removed and possibly deleted here but I don't see either of those happening
4. clear browsing data again
  a. a new BrowsingDataRemover (BDR2) is created and an observer (ClearBrowserDataHandler or CBDH2) to its observer_list_
5. close the WebUI tab where this is occurring
  a. CBDH2 is removed from BDR2's observer_list_
  b. CBDH2 is destroyed
6. refresh the original page
  a. We crash within BDR1 when calling a virtual function on CBDH1

Again, I never see destructors called for either BDR1 or CBDH1 so I don't know why these are no longer valid.

### jo...@chromium.org (2011-05-18)

adding csilv@ and estade@ who worked on the WebUI implementation of this

### mi...@chromium.org (2011-05-19)

@jochen, just noticed r74433 from Feb2011. The DatabaseTracker should only be used on the FILE thread. I'm not sure why you switched to using the WEBKIT thread for that subsystem, but it definitely should only be utilized on the FILE thread.

No idea if that has anything to do with this particular bug, but calling things on the wrong threads certainly could be part of the problem. I'll be adding some DCHECKS to database_tracker.cc soon as the class comments didn't suffice.

### th...@gmail.com (2011-05-19)

I tried to reproduce the "DownloadItem" related issue (82309) with the steps of the current issue and I came up with the following:

1. Load the html file from the comment above (in a clean browser session because other HTML5 (storage) based sites/files may interfere)
2. Erase history with at least "Delete cookies and other site data" checked (does not close!!!)
3. Cancel it and erase again (stalls again!!)
4. Close the tab "Options - Clear Browsing Data" while the erase process is still active
5. [Reload the first html file, 81916] or [Save the first html file (page) to disk, 82309]
6. Crash!

My guess is that the second part of step 5 may reproduce 82309, but I'm only concluding this from the comments on 81916 (=above). If this is true, the issues are closely related indeed.

### jo...@chromium.org (2011-05-19)

@michaeln: because the methods invoke WebKit:: methods. They only ever must be invoked on the WEBKIT thread. I guess we have to get rid of them at this point, there are some replacements in database_util

btw, the database_quota_client seems to invoke WebKit::WebSecurityOrigin methods on the FILE thread as well? In that case, this also needs to be fixed

### th...@gmail.com (2011-05-19)

After a new test with a lot of different steps I finally managed to reproduce four different crashes related to (and including) this one. First let's repeat the four steps that are always used. I added the HTML file of https://crbug.com/chromium/81916#c1 for clarity.

1. Load the added HTML file (in a clean browser session because other HTML5 (storage) based sites/files may interfere)
2. Erase history with at least "Delete cookies and other site data" checked (does not close!!!) while making sure that the file/page is newer than the selected item from the (Obliterate ...) ComboBox.
3. Cancel it and erase again (stalls again!!)
4. Close the tab "Options - Clear Browsing Data" while the erase process is still active

After steps 1-4 are carried out, the HTML file's WebUI gets into an "about-to-crash" state.

Now step 5: 

For all (step 5) operations, I use the Tab/URL-bar of the page of step 1

5a. If you try to reload the page, Chrome will crash (81916)
5b. If you try to save the page, Chrome will crash (82309?)
5c. If you type anything in the URL-bar (followed by Enter), Chrome will crash (new issue?).
5d. If you try to close the Tab, Chrome will crash (new issue?)

### mi...@chromium.org (2011-05-19)

@michaeln: because the methods invoke WebKit:: methods. They only ever must be invoked on the WEBKIT thread. I guess we have to get rid of them at this point, there are some replacements in database_util

That's not entirely true. Certain WebKit primitives are fine to use on other threads, things like WebString for example. Not all methods of WebSecurityOrigin are fair game on any thread, but enough to produce and interpret 'origin_identifier' strings given origin_url strings is fine to use on any thread. We do that all throughout the database and file system backends.

The database related browsing data helpers stuff should use DatabaseUtil::GetOriginFromIdentifier(origin_identifier) to produce a GURL() to get a structured representation of the <scheme,host,port>. It's usable on anything thread. There's a reciprocal function in DatabaseUtil to go the other direction too.



### jo...@chromium.org (2011-05-19)

the following call stack leads to an ASSERT(isMainThread()):

WebCore::buildBaseTextCodecMaps()
WebCore::atomicCanonicalTextEncodingName()
WebCore::TextEncoding::TextEncoding()
WebCore::UTF8Encoding()
WebCore::decodeURLEscapeSequences()
WebCore::SecurityOrigin::createFromDatabaseIdentifier()
WebKit::WebSecurityOrigin::createFromDatabaseIdentifier()

### mi...@chromium.org (2011-05-19)

Yes, webkit must be initialized prior to using these classes, after webkit has been initialized the text encoding tables are initialized, and that code path isn't followed.

See WebKit::initialize().

void initialize(WebKitClient* webKitClient)
{
    ASSERT(!s_webKitInitialized);
    s_webKitInitialized = true;

    ASSERT(webKitClient);
    ASSERT(!s_webKitClient);
    s_webKitClient = webKitClient;

    WTF::initializeThreading();
    WTF::initializeMainThread();
    WTF::AtomicString::init();

    // There are some code paths (for example, running WebKit in the browser
    // process and calling into LocalStorage before anything else) where the
    // UTF8 string encoding tables are used on a background thread before
    // they're set up.  This is a problem because their set up routines assert
    // they're running on the main WebKitThread.  It might be possible to make
    // the initialization thread-safe, but given that so many code paths use
    // this, initializing this lazily probably doesn't buy us much.
    WebCore::UTF8Encoding();
}

### jo...@chromium.org (2011-05-19)

if it's initialized, you can get races (see the bug referenced in r74433)

### mi...@chromium.org (2011-05-19)

huh? can u cc me on that bug so i can see it?

### th...@gmail.com (2011-05-19)

I just discovered that step 4 of comments #2 and #25 and step 5 of https://crbug.com/chromium/81916#c20 do not require that the erase process is still running when you close the erase tab. So, the new step would be:

4. Cancel the erase process and close the "Options - Clear Browsing Data" tab

### es...@chromium.org (2011-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-05-19)

Talked to Evan, I'm taking this one.

### [Deleted User] (2011-05-19)

I will have a CL shortly to fix the stale observer bug.  But that is only half of the problem, the other half is the fact that BrowsingDataRemover stalls and never completes.  Is there a bug for that issue?

### [Deleted User] (2011-05-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-05-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=86030

------------------------------------------------------------------------
r86030 | michaeln@google.com | Thu May 19 18:22:24 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/browsing_data_database_helper.cc?r1=86030&r2=86029&pathrev=86030
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/browsing_data_database_helper.h?r1=86030&r2=86029&pathrev=86030

Use the DatabaseTracker only on the FILE thread.

TEST=none
BUG=81916
Review URL: http://codereview.chromium.org/7046013
------------------------------------------------------------------------

### bu...@chromium.org (2011-05-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=86146

------------------------------------------------------------------------
r86146 | csilv@chromium.org | Fri May 20 14:12:12 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/webui/options/clear_browser_data_handler.cc?r1=86146&r2=86145&pathrev=86146

dom-ui settings: Stop observing an existing BrowserDataRemover before creating a new one.

BUG=81916
TEST=Follow repro setps in bug report, verify that crash no longer occurs.
Review URL: http://codereview.chromium.org/7050031
------------------------------------------------------------------------

### [Deleted User] (2011-05-20)

The stale observer/crash is now fixed as of r81916.

If someone is working on the cause for BrowserDataRemover never completing, please let me know so I can pass ownership of this bug or mark it fixed.

### [Deleted User] (2011-05-20)

Sorry, I meant r86146.

### th...@gmail.com (2011-05-20)

works!!!! good job, fixes 5a..d from https://crbug.com/chromium/81916#c25.

It does not yet remove the "stalling" issue, but it no longer crashes.

I learned a lot from how you guys work on a massive (and very nice) project like Chromium.

### [Deleted User] (2011-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2011-05-20)

Do you guys want to open a separate issue for the non-security relevant bug that still needs to be addressed? We are probably going to want to merge the security fix that already landed.

### mi...@chromium.org (2011-05-20)

A separate bug for the stalling issue would be good. I have yet to see a "stall" when trying to repro. Does it only stall on XP?

### th...@gmail.com (2011-05-21)

@michaeln

On WinXP SP3 and Linux (Ubuntu 11.04) it stalls with the latest version from the build server (ToT, WinXP: 86206, Linux: 86210).

It does not crash anymore though.

### [Deleted User] (2011-05-21)

I've filed a separate bug for the stall as:

   http://crbug.com/83487

Marking this issue (the crash) as fixed.

### in...@chromium.org (2011-05-21)

The two fixes have to be merged to m12. We will do that.

### [Deleted User] (2011-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2011-05-23)

merged to m12 as r86314

### bu...@chromium.org (2011-05-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=86314

------------------------------------------------------------------------
r86314 | cdn@chromium.org | Mon May 23 11:51:07 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/742/src/chrome/browser/ui/webui/options/clear_browser_data_handler.cc?r1=86314&r2=86313&pathrev=86314

Merge 86146 - dom-ui settings: Stop observing an existing BrowserDataRemover before creating a new one.

BUG=81916
TEST=Follow repro setps in bug report, verify that crash no longer occurs.
Review URL: http://codereview.chromium.org/7050031
Review URL: http://codereview.chromium.org/7064003
------------------------------------------------------------------------

### in...@chromium.org (2011-06-01)

Do we need to merge r86030 from c#36 ?

### sc...@gmail.com (2011-06-02)

@inferno @cdn what's the deal with merging r86030? It's now too late for M12?

### sc...@gmail.com (2011-06-02)

@therealholden: congrats! Although we don't always reward Medium severity issues, this one is interesting enough to warrant a $500 reward. Thanks for the detailed steps, and taking the trouble to update the bug as you refined your findings.

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

### th...@gmail.com (2011-06-03)

Thank you!

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-05)

@therealholden: what name do you want us to use in our release notes to credit you?

### th...@gmail.com (2011-06-05)

You can use my real name, it is Collin Payne

### sc...@gmail.com (2011-06-07)

@therealholden: thanks!
Check out http://googlechromereleases.blogspot.com/2011/06/chrome-stable-release.html

To collect your reward, please e-mail cevans@chromium.org

### sc...@gmail.com (2011-06-14)

[Empty comment from Monorail migration]

### th...@gmail.com (2011-06-14)

Thanks, reward collection e-mail sent June 7th

### sc...@gmail.com (2011-07-08)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/81916?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090691)*
