# Security: u-a-f in shared worker process in Allow{IndexedDB,FileSystem}MainThreadBridge

| Field | Value |
|-------|-------|
| **Issue ID** | [40077325](https://issues.chromium.org/issues/40077325) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Storage>IndexedDB |
| **Reporter** | th...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2013-04-01 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome crashes in commonClient->allowIndexedDB(name) (AllowIndexedDBMainThreadBridge::allowIndexedDBTask) with a zero'd ScriptExecutionContext when an IDB open, or deleteDatabase call is used in a shared worker with a location.reload call in its onmessage event.

The crash/issue on Windows XP is a bad instruction pointer, while on Windows 7 it causes an invalid handle crash (with stack corruption), probably caused by a non-IDB (shared) worker issue. The added repro causes an invalid handle crash with corruption on Windows 7 even with all IDB code removed from the script.

**VERSION**  

Chrome Version: stable v26.0.1410.43 - ToT v28.0.1459.0  

Operating System: Windows XP SP3 / Windows 7 SP1 (32-bit)

**REPRODUCTION CASE**  

Load the added repro file

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab/Child Process  

Crash State: Check added trace files

## Attachments

- [IDB_SW_tot_XP_trace.txt](attachments/IDB_SW_tot_XP_trace.txt) (text/x-c++; charset=us-ascii, 118.4 KB)
- [SW_tot_7_trace.txt](attachments/SW_tot_7_trace.txt) (text/x-c++; charset=us-ascii, 92.8 KB)
- [IDB_SW_stable_XP_trace.txt](attachments/IDB_SW_stable_XP_trace.txt) (text/x-c++; charset=us-ascii, 145.8 KB)
- [IDB_SW_small_repro.html](attachments/IDB_SW_small_repro.html) (text/plain; charset=us-ascii, 265 B)
- [GetCookieSettings_crash_incognito_stable.txt](attachments/GetCookieSettings_crash_incognito_stable.txt) (text/x-c++; charset=us-ascii, 16.4 KB)
- [GetCookieSettings_crash_normal_ToT.txt](attachments/GetCookieSettings_crash_normal_ToT.txt) (text/x-c++; charset=us-ascii, 89.2 KB)
- [GetURLRequestContext_crash.txt](attachments/GetURLRequestContext_crash.txt) (text/x-c++; charset=us-ascii, 12.3 KB)
- [GetCookieSettings_crash_normal_stable_txt.txt](attachments/GetCookieSettings_crash_normal_stable_txt.txt) (text/x-c++; charset=us-ascii, 121.0 KB)
- [fs_repro.html](attachments/fs_repro.html) (text/plain; charset=us-ascii, 410 B)
- [fs_asan_crash.txt](attachments/fs_asan_crash.txt) (text/x-c; charset=us-ascii, 11.1 KB)
- [shared_worker_crashes.txt](attachments/shared_worker_crashes.txt) (text/x-c++; charset=us-ascii, 26.4 KB)
- [225546_websockets_full_browser_crash.txt](attachments/225546_websockets_full_browser_crash.txt) (text/x-c++; charset=us-ascii, 50.6 KB)
- [225546_xhr_crash.txt](attachments/225546_xhr_crash.txt) (text/x-c; charset=us-ascii, 77.1 KB)
- [websockets_new_browser_crash.txt](attachments/websockets_new_browser_crash.txt) (text/x-c++; charset=us-ascii, 64.1 KB)
- deleted (application/octet-stream, 0 B)
- [websockets_purecall_browser_crash.txt](attachments/websockets_purecall_browser_crash.txt) (text/x-c; charset=us-ascii, 78.0 KB)
- [WebSocket_browser_crash_repro.html](attachments/WebSocket_browser_crash_repro.html) (text/plain; charset=us-ascii, 568 B)
- [XMLHttpRequest_worker_crash_repro.html](attachments/XMLHttpRequest_worker_crash_repro.html) (text/plain; charset=us-ascii, 599 B)
- [SharedWorker_Internal_field_out_of_bounds_crash_repro.html](attachments/SharedWorker_Internal_field_out_of_bounds_crash_repro.html) (text/plain; charset=us-ascii, 160 B)
- [Debug_SharedWorker_reloading_crash_trace.txt](attachments/Debug_SharedWorker_reloading_crash_trace.txt) (text/x-c++; charset=us-ascii, 10.9 KB)
- [WebSQL_browser_dangerous_mask_break_crash_repro.html](attachments/WebSQL_browser_dangerous_mask_break_crash_repro.html) (text/plain; charset=us-ascii, 294 B)

## Timeline

### in...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### ae...@chromium.org (2013-04-02)

Interesting, thanks for the report!

I haven't been able to reproduce on Windows 7 26.0.1410.43 though.
@dgrogan, jsbell: can you reproduce this?



### ae...@chromium.org (2013-04-02)

Ok, reproduced this on 27.0.1416.0 ASAN build.

### ae...@chromium.org (2013-04-02)

So yeah, looks like a UaF. The commonClient argument has been freed. The commonClient should be a field in WebSharedWorkerStub:

WebSharedWorkerClientProxy client_;

WebSharedWorkerStub is
- allocated in WorkerThread::OnCreateWorker (content/worker/worker_thread.cc)
- freed in WebSharedWorkerStub::Shutdown (content/worker/websharedworker_stub.cc)

So I guess when the page reloads, the worker is killed and then used in IDB code?

### ae...@chromium.org (2013-04-02)

It triggers quite racily. It is easier to trigger by filling all cores with while(1); :)

### ae...@chromium.org (2013-04-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

dgrogan, is this on your radar or should we be looking for another owner?

### dg...@chromium.org (2013-04-16)

I'll plan on getting this done by Apr 26, the end of next week. Is that ok?

### th...@gmail.com (2013-04-17)

The repro seems to cause a full (stale pointer) browser crash if the current (repro) window is closed before the (commonClient) worker race/crash occurs (can be automated). Also, many other null (class) ptr crashes (like callonmainthread) can occur.

The first full browser crash is the familiar 0-ptr GetURLRequestContext (no IDB/workers on stack) crash. It is interesting, because it crashes the full browser. It does not seem to be very harmful (besides bringing the browser down).

(ae8.bac): Access violation - code c0000005 (!!! second chance !!!)
eax=00000000 ebx=0407a882 ecx=00000000 edx=7c90e514 esi=08e4d210 edi=06ca3220
eip=01d8c3b6 esp=057dfaf0 ebp=057dfb00 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
chrome_1c30000!ChromeURLRequestContextGetter::GetURLRequestContext+0x27:
01d8c3b6 8b01            mov     eax,dword ptr [ecx]  ds:0023:00000000=????????

The second browser crash is a (stale pointer) GetCookieSettings crash (with IDB/workers on stack). I tested this on stable/ToT and with normal/incognito mode. The difference between incognito and normal mode is easy to see (ProfileIOData vs CookieSettings). I ran ToT tests that confirm that it also reproduces there (check version in !analyze part).

(be0.294): Access violation - code c0000005 (!!! second chance !!!)
eax=53726550 ebx=00000000 ecx=53726550 edx=01c568a0 esi=53726550 edi=08b2ab00
eip=01c6f89f esp=0602f098 ebp=0602f154 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
chrome_1c30000!ProfileIOData::GetCookieSettings+0x6f:
01c6f89f 8b8624030000    mov     eax,dword ptr [esi+324h] ds:0023:53726874=????????

(138.830): Access violation - code c0000005 (!!! second chance !!!)
eax=057df90c ebx=00000000 ecx=057df90c edx=0000000f esi=0000000f edi=a44c1eee
eip=020bbf81 esp=057df7c4 ebp=057df92c iopl=0         nv up ei ng nz na pe cy
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000287
chrome_1c30000!CookieSettings::GetCookieSetting+0x82:
020bbf81 8b4f10          mov     ecx,dword ptr [edi+10h] ds:0023:a44c1efe=????????


### dg...@chromium.org (2013-04-23)

This affects filesystem as well. A trivial change to the IDB repro script yields an asan error with filesystem.  The IDB bridge was modeled after filesystem's. So was WebSQL's but I didn't try to repro with that.

### mi...@chromium.org (2013-04-23)

gotta say... therealholden rocks in finding these things :)

### th...@gmail.com (2013-04-23)

The FS repro seems to corrupt the stack with a write ptr. It also crashes in WebMessagePortChannelImpl::postMessage (added file) with a null class ptr and a changing ScriptExecutionContext.

Also, if you replace the FS part in the c#12 repro with openDatabase (more workers might improve reliability), it crashes ToT (full browser basic_info.GrantedAccess & kDangerousMask debug/check crash) while erasing history.

I have a bigger repro with WebWorkers/WebSQL that crashes the browser instantly (without erasing history). However, the (same) stack(s) and logfile(s) should give a clear view on what is going on.

### dg...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### dg...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### dg...@chromium.org (2013-04-25)

aedla, how certain are you that your suggestion in https://crbug.com/chromium/225546#c4 is the right fix?

Figuring this out seems like it will be harder now that the problem is known to be systemic, not IDB-specific. We might need some support or suggestions from dimich.

### me...@google.com (2013-04-26)

@dgrogan: Is this bug similar to https://crbug.com/chromium/176692? If so, maybe I can take a look as I recently fiddled with the worker stuff.

### dg...@chromium.org (2013-04-26)

meacer, can you cc me on that bug?

### me...@google.com (2013-04-26)

> meacer, can you cc me on that bug?

Done!

### dg...@chromium.org (2013-04-26)

meacer, it is similar. michaeln's description of storage x worker bugs in https://code.google.com/p/chromium/issues/detail?id=176692#c23 fits this issue. It also fits https://crbug.com/chromium/172240.

You're probably in a better position than anyone else to tackle https://crbug.com/chromium/172240 and https://crbug.com/chromium/225546 after your work on 176692. So feel free to take them on!


### th...@gmail.com (2013-04-28)

I can repro another (stale pointer) full browser crash with web sockets. I used the original repro script and replaced the IndexedDB part with "new WebSocket('ws://localhost:9998/echo');".

This time the crash happens in the IO thread of the main browser process. However, probably a lot has gone wrong in the shared worker process before the crash.

### th...@gmail.com (2013-04-28)

The same goes for XMLHttpRequest (worker process crash). I used an alternate (slightly more complicated) repro for this with an extra web worker. This time a break instruction exception occurs.

### me...@google.com (2013-04-29)

As promised, I'll take a look :)

### sc...@gmail.com (2013-05-02)

@therealholden: your comment https://crbug.com/chromium/225546#c22 is somewhat alarming. If you can crash the full browser with a stale pointer, without user interaction, then that's a critical issue. Please confirm! Maybe it deserves to be a different bug than the crashes in the worker process.

### th...@gmail.com (2013-05-02)

The repro originally required closing the browser window the script runs in. However, I have now automated that.

This new repro (with IDB instead of WebSockets) can probably (reliably) also reproduce the GetCookieSettings c#11 crash after the original issue is fixed.

The repro steps are with the new script (I'll post later):

1. Start Chrome and open an incognito window
2. Launch the script in the incognito window
3. Move focus back to the non-incognito window
4. Browser crash

I've added a new trace with the new script because it seems that the browser crashes can differ (slightly). However, the most occurring crash is the c#22 crash.

### th...@gmail.com (2013-05-02)

Repro scripts: c#23 worker crash and c#22/c#26 browser crash.

Also, I've added a PureCall c#26 trace (browser process).

### th...@gmail.com (2013-05-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### me...@chromium.org (2013-05-02)

[Empty comment from Monorail migration]

### me...@google.com (2013-05-02)

As mentioned before, the same pattern is used in many workers related code, so it's not surprising that we get the same sort of bugs.

Even without any IDB, WebSocket or XHR code involved, the loop in therealholden's repros fails with null deref after some time. FWIW, I also disabled  AllowIndexedDBMainThreadBridge which hits the UAF in the original IndexedDB repro, and then hit another UAF for IDBFactoryBackendProxy::m_webIDBFactory :/

I hope we'll be able to address WebSocket and XHR related issues with similar patches, but there seem to be other problems as well, which may take some time to figure out.

### th...@gmail.com (2013-05-06)

The XHR crash does not seem to need XHR. It seems to repro with anything (or nothing) in a loop. All it needs is a loop in a shared worker with an onconnect event.

Even further testing shows that the repro requires only two iterations.

### me...@google.com (2013-05-06)

Here is the patch for IndexedDB: https://codereview.chromium.org/14995004/

This fixes the UAF, but there is a separate memory leak which I think isn't related to the AllowIndexedDBMainThreadBridge code that is changed here. When I take out the the whole bridge code, the leak is still there. It's probably related to one of https://crbug.com/chromium/27837, https://crbug.com/chromium/27838 or https://crbug.com/chromium/28200.

@therealhoden: Good catch with the last repro, I believe it's a separate bug. The problematic part seems to be the truth path in WebSharedWorkerStub::OnConnect. Eventually it causes script->Run() at V8ScriptRunner::runCompiledScript to fail with a null deref. I'll try to step through it to understand what's going on.

### me...@chromium.org (2013-05-09)

Here is the new patch that addresses IndexedDB, Filesystem and WebSQL: https://codereview.chromium.org/14720005/


### me...@chromium.org (2013-05-10)

Trying to summarize all the findings in this bug:

I checked other worker related code which has *MainThreadBridge and *CallbacksBridge classes.

*MainThreadBridge classes (these should be fixed in https://codereview.chromium.org/14720005/):
IDBFactoryBackendProxy 
LocalFileSystemChromium
DatabaseObserver

*CallbacksBridge classes:
WorkerFileSystemCallbacksBridge: should be affected by this bug but I can't trigger UAF
WorkerStorageQuotaCallbacksBridge: affected by this bug
WorkerFileWriterCallbacksBridge: seems OK
WorkerAsyncFileSystemChromium: seems OK
WebFileSystemCallbacksImpl: not affected
StorageQuotaChromium: affected via WorkerStorageQuotaCallbacksBridge

I'll have a separate patch for WorkerFileSystemCallbacksBridge and WorkerStorageQuotaCallbacksBridge.

Regarding https://crbug.com/chromium/225546#c22: I'm not sure if that crash is already covered in https://crbug.com/chromium/172240.  However, I'm certain that it's a separate issue than this one (it's a UAF in net::SocketStream::Finish). I'll create another bug for it if I'm convinced it's not a duplicate of 172240.

Regarding https://crbug.com/chromium/225546#c32: I filed https://crbug.com/chromium/239669 (this also covers XHR related issues).

@therealholden: Is there anything I'm missing?

### th...@gmail.com (2013-05-10)

That seems to be about it.

I did find a few other crashes like the c#11 GetCookieSettings (stale pointer browser) crash. However, they are more difficult to reproduce, because the GetURLRequestContext (0-ptr browser) crash now seems to be in front of them. 

That crash has the following repro steps:

1. Open Chrome with at least one normal and one incognito tab
2. Launch the original, or the c#12 repro (WebSQL also seems to work) in the incognito tab and close it quickly (can be automated)

If this still reproduces after the bridge and callback fixes have landed, I'm pretty sure the GetCookieSettings crash is also still there. I will file a new bug if it is.

I can also still repro the c#14 WebSQL "basic_info.GrantedAccess & kDangerousMask" breakdebugger crash. However, this seems to be a debug specific crash, since not all Chrome versions have this check enabled? It may also be fixed by the fix(es) mentioned above.

That crash has the following repro steps:

1. Launch the attached repro
2. Erase all history

The stack trace is @ the bottom of the file attached to https://crbug.com/chromium/225546#c14.

I have a few other crashes, some of them are null (class) pointers (like WebMessagePortChannelImpl::postMessage c#14), or they are crashes caused by the u-a-f scripts' stack corruption. If any of them exist after the fix(es) above, I will file a new issue.

Other crashes (probably related/caused to/by the worker races/corruption) happen when you try to use chrome:inspect to debug the reloading SharedWorker. I've added one of them (another stale pointer browser crash).

Finally, 172240 is not related to the WebSocket browser crash (afaik). It is mostly a WebWorker (ScriptExecutionContext being released while the worker still runs) issue/crash that affects IDB. I have seen WebSQL being affected too, but that's harder to repro. I will post a new and improved repro there shortly.

### me...@chromium.org (2013-05-22)

CC'ing jamesr so that he can see the bug for review.

### bu...@chromium.org (2013-05-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=150847

------------------------------------------------------------------------
r150847 | meacer@chromium.org | 2013-05-22T01:30:14.795185Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/WebKit.gyp?r1=150847&r2=150846&pathrev=150847
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/DatabaseObserver.cpp?r1=150847&r2=150846&pathrev=150847
   A http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/WorkerAllowMainThreadBridgeBase.cpp?r1=150847&r2=150846&pathrev=150847
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/IDBFactoryBackendProxy.cpp?r1=150847&r2=150846&pathrev=150847
   A http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/WorkerAllowMainThreadBridgeBase.h?r1=150847&r2=150846&pathrev=150847
   M http://src.chromium.org/viewvc/blink/trunk/Source/WebKit/chromium/src/LocalFileSystemChromium.cpp?r1=150847&r2=150846&pathrev=150847

Fix crash in Worker related code for IndexedDB, file system and WebSQL.

A worker context can be destroyed while a cross-thread request is in
progress. This patch introduces a base class, WorkerAllowMainThreadBridgeBase.
This class has a WorkerContext::Observer field that observes WorkerContext
destruction and notifies the subclasses of WorkerAllowMainThreadBridgeBase
during shutdown. This will prevent subclasses from attempting to access
a stale worker context pointer.

BUG=225546

Review URL: https://chromiumcodereview.appspot.com/14720005
------------------------------------------------------------------------

### in...@chromium.org (2013-05-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-22)

Adding reward-topanel, this bug definitely needs it :-)
@therealholden: how are things looking with this patch? At this stage, any additional issues and repros you wanted to add probably belong in a new bug!!

### me...@chromium.org (2013-05-22)

There is one more angle for this bug. I'll spin it off as a separate issue (https://crbug.com/chromium/225546#c22).

### me...@chromium.org (2013-05-22)

Filed https://crbug.com/chromium/242762 for https://crbug.com/chromium/225546#c22 (WebSocket + Worker)

### th...@gmail.com (2013-05-22)

@scarybeasts: I'll test once the (Blink) 150847 patch/revision has rolled into a snapshot build. Right now the latest version == v150819.

### th...@gmail.com (2013-05-23)

After testing with Blink 150885, it seems that the (three, WebSQL, IndexedDB and FileSystem) crashes (and the c#11 GetCookieSettings browser crash) fixed by this patch are indeed gone.

However, I still see worker races and this patch has also uncovered at least one reliable (CheckDuplicateHandle break debugger) browser crash (1). 

The following (non-filed) crashes still occur.

1. The bigger WebSQL repro I have (c#14) now seems to be reliable (it isn't on the current stable version, last c#14 trace). I will file a new (security) issue later. It is slightly different, because it relies on web workers to crash the browser. It does repro with shared workers, but requires the user to erase history.

2. The c#12 filesystem repro now causes a reliable c#14 WebMessagePortChannelImpl::postMessage 0-ptr renderer crash. Since this is a non-security issue, I will file it once I have a non-security repro.

3. Closing the (incognito) window a shared worker reloads in (c#11) still causes a full browser (0-ptr) ChromeURLRequestContextGetter::GetURLRequestContext crash. Is there already an issue about this?

4. Inspecting a reloading shared worker (c#36) can cause varying browser crashes. I will file these once I have a minimized repro.

Most of the issues above will probably show up earlier with ASAN. I have only posted issues that cause(d) browser, or renderer crashes.


### js...@chromium.org (2013-05-23)

> However, I still see worker races and this patch has also uncovered at least one reliable (CheckDuplicateHandle break debugger) browser crash (1). 

Well, that's very bad. Please file a new bug with a repro so I can investigate.

### th...@gmail.com (2013-05-23)

Ok, filed as https://crbug.com/chromium/243339.

### me...@chromium.org (2013-05-23)

> 3. Closing the (incognito) window a shared worker reloads in (c#11) still causes a full browser (0-ptr) ChromeURLRequestContextGetter::GetURLRequestContext crash. Is there already an issue about this?

There seems to be an old https://crbug.com/chromium/99242 for this.

### sc...@gmail.com (2013-05-28)

M27 is r151283
M28 is r151282

### sc...@gmail.com (2013-06-03)

@therealholden: thanks for all your work on this issue! Although we fixed it with one patch, your work did uncover a general class of issue, so we're rewarding at the $1337 level.

### th...@gmail.com (2013-06-03)

Thanks!

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/225546?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>Storage>IndexedDB]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077325)*
