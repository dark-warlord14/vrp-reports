# Browser process heap-use-after-free with indexeddb cursors

| Field | Value |
|-------|-------|
| **Issue ID** | [40052260](https://issues.chromium.org/issues/40052260) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink, Blink>Storage>IndexedDB, Internals |
| **Reporter** | ao...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2011-12-19 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a heap use after free when the attached page is opened in Chrome.

**VERSION**  

Chrome Version: 18.0.973.0 (Developer Build 114785)  

Operating System: Linux (Debian 6.0.3, x86\_64)

**REPRODUCTION CASE**  

$ chrome cursor.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser (use after free, no crash)  

Crash State:

There were some different traces during minimization. This is is for the attached fairly minimized version.

=================================================================  

==10709== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffd3ed71b0 at pc 0x7ffff5c246c3 bp 0x7fffde9621b0 sp 0x7fffde9621a8  

READ of size 1 at 0x7fffd3ed71b0 thread T5  

#0 0x7ffff5c246c3 in WebCore::LevelDBTransaction::TransactionIterator::handleConflictsAndDeletes() ???:0  

#1 0x7ffff5c252d2 in WebCore::LevelDBTransaction::TransactionIterator::next() ???:0  

#2 0x7ffff59c4142 in WebCore::(anonymous namespace)::CursorImplCommon::continueFunction(WebCore::IDBKey const\*) third\_party/WebKit/Source/WebCore/storage/IDBLevelDBBackingStore.cpp:0  

#3 0x7ffff5a335ff in WebCore::IDBCursorBackendImpl::prefetchReset(int, int) ???:0  

#4 0x7ffff4b4a7c2 in IndexedDBDispatcherHost::CursorDispatcherHost::OnPrefetchReset(int, int, int) ???:0  

#5 0x7ffff4b4eec3 in bool IPC::SyncMessageSchema<Tuple3<int, int, int>, Tuple0>::DispatchWithSendParams<IndexedDBDispatcherHost::CursorDispatcherHost, IndexedDBDispatcherHost::CursorDispatcherHost, void (IndexedDBDispatcherHost::CursorDispatcherHost::\*)(int, int, int)>(bool, Tuple3<int, int, int> const&, IPC::Message const\*, IndexedDBDispatcherHost::CursorDispatcherHost\*, IndexedDBDispatcherHost::CursorDispatcherHost\*, void (IndexedDBDispatcherHost::CursorDispatcherHost::\*)(int, int, int)) ???:0  

#6 0x7ffff4b3e437 in IndexedDBDispatcherHost::CursorDispatcherHost::OnMessageReceived(IPC::Message const&, bool\*) ???:0  

#7 0x7ffff4b39c40 in IndexedDBDispatcherHost::OnMessageReceived(IPC::Message const&, bool\*) ???:0  

#8 0x7ffff48441ed in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) ???:0  

#9 0x7ffff484449f in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<bool (content::BrowserMessageFilter::\*)(IPC::Message const&)>, bool ()(content::BrowserMessageFilter\*, IPC::Message const&), void ()(content::BrowserMessageFilter\*, IPC::Message)>, bool ()(content::BrowserMessageFilter\*, IPC::Message const&)>::Run(base::internal::BindStateBase\*) ???:0  

#10 0x7fffef14b443 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(base::Callback<bool ()()>)>, void ()(base::Callback<bool ()()>), void ()(base::Callback<bool ()()>)>, void ()(base::Callback<bool ()()>)>::Run(base::internal::BindStateBase\*) ???:0  

#11 0x7ffff05b8c34 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#12 0x7ffff05b94b6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#13 0x7ffff05ba7a1 in MessageLoop::DoWork() ???:0  

#14 0x7ffff05c4fd7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#15 0x7ffff05b782e in MessageLoop::RunInternal() ???:0  

#16 0x7ffff05b58df in MessageLoop::Run() ???:0  

#17 0x7ffff062a2bc in base::Thread::ThreadMain() ???:0  

#18 0x7ffff062813c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:0  

#19 0x7ffff5c54ece in \_\_asan::AsanThread::ThreadStart() ??:0  

0x7fffd3ed71b0 is located 48 bytes inside of 80-byte region [0x7fffd3ed7180,0x7fffd3ed71d0)  

freed by thread T5 here:  

#0 0x7ffff5c52a54 in operator delete(void\*) ??:0  

#1 0x7ffff5c1f987 in WebCore::LevelDBTransaction::clearTree() ???:0  

#2 0x7ffff59c391c in WebCore::IDBLevelDBBackingStore::Transaction::rollback() ???:0  

#3 0x7ffff5a1b828 in WebCore::IDBTransactionBackendImpl::abort() ???:0  

#4 0x7ffff4b3ed3e in IndexedDBDispatcherHost::TransactionDispatcherHost::OnMessageReceived(IPC::Message const&, bool\*) ???:0  

#5 0x7ffff4b39c7b in IndexedDBDispatcherHost::OnMessageReceived(IPC::Message const&, bool\*) ???:0  

#6 0x7ffff48441ed in content::BrowserMessageFilter::DispatchMessage(IPC::Message const&) ???:0  

#7 0x7ffff484449f in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<bool (content::BrowserMessageFilter::\*)(IPC::Message const&)>, bool ()(content::BrowserMessageFilter\*, IPC::Message const&), void ()(content::BrowserMessageFilter\*, IPC::Message)>, bool ()(content::BrowserMessageFilter\*, IPC::Message const&)>::Run(base::internal::BindStateBase\*) ???:0  

#8 0x7fffef14b443 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (\*)(base::Callback<bool ()()>)>, void ()(base::Callback<bool ()()>), void ()(base::Callback<bool ()()>)>, void ()(base::Callback<bool ()()>)>::Run(base::internal::BindStateBase\*) ???:0  

#9 0x7ffff05b8c34 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#10 0x7ffff05b94b6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#11 0x7ffff05ba7a1 in MessageLoop::DoWork() ???:0  

#12 0x7ffff05c4fd7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#13 0x7ffff05b782e in MessageLoop::RunInternal() ???:0  

#14 0x7ffff05b58df in MessageLoop::Run() ???:0  

#15 0x7ffff062a2bc in base::Thread::ThreadMain() ???:0  

#16 0x7ffff062813c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:0  

#17 0x7ffff5c54ece in \_\_asan::AsanThread::ThreadStart() ??:0  

previously allocated by thread T5 here:  

#0 0x7ffff5c52854 in operator new(unsigned long) ??:0  

#1 0x7ffff5c20053 in WebCore::LevelDBTransaction::set(WebCore::LevelDBSlice const&, WTF::Vector<char, 0ul> const&, bool) ???:0  

#2 0x7ffff5c20d4b in WebCore::LevelDBTransaction::put(WebCore::LevelDBSlice const&, WTF::Vector<char, 0ul> const&) ???:0  

#3 0x7ffff59ba535 in WebCore::IDBLevelDBBackingStore::putIndexDataForRecord(long, long, long, WebCore::IDBKey const&, WebCore::IDBBackingStore::ObjectStoreRecordIdentifier const\*) ???:0  

#4 0x7ffff5a0de27 in WebCore::IDBObjectStoreBackendImpl::putInternal(WebCore::ScriptExecutionContext\*, WTF::PassRefPtr[WebCore::IDBObjectStoreBackendImpl](javascript:void(0);), WTF::PassRefPtr[WebCore::SerializedScriptValue](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBKey](javascript:void(0);), WebCore::IDBObjectStoreBackendInterface::PutMode, WTF::PassRefPtr[WebCore::IDBCallbacks](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBTransactionBackendInterface](javascript:void(0);)) ???:0  

#5 0x7ffff5a18820 in WebCore::CrossThreadTask6<WTF::PassRefPtr[WebCore::IDBObjectStoreBackendImpl](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBObjectStoreBackendImpl](javascript:void(0);), WTF::PassRefPtr[WebCore::SerializedScriptValue](javascript:void(0);), WTF::PassRefPtr[WebCore::SerializedScriptValue](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBKey](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBKey](javascript:void(0);), WebCore::IDBObjectStoreBackendInterface::PutMode, WebCore::IDBObjectStoreBackendInterface::PutMode, WTF::PassRefPtr[WebCore::IDBCallbacks](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBCallbacks](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBTransactionBackendInterface](javascript:void(0);), WTF::PassRefPtr[WebCore::IDBTransactionBackendInterface](javascript:void(0);) >::performTask(WebCore::ScriptExecutionContext\*) ???:0  

#6 0x7ffff5a1a589 in WebCore::IDBTransactionBackendImpl::taskTimerFired(WebCore::Timer[WebCore::IDBTransactionBackendImpl](javascript:void(0);)\*) ???:0  

#7 0x7ffff276a738 in WebCore::ThreadTimers::sharedTimerFiredInternal() ???:0  

#8 0x7ffff05b8c34 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#9 0x7ffff05b94b6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#10 0x7ffff05ba7a1 in MessageLoop::DoWork() ???:0  

#11 0x7ffff05c4fd7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#12 0x7ffff05b782e in MessageLoop::RunInternal() ???:0  

#13 0x7ffff05b58df in MessageLoop::Run() ???:0  

#14 0x7ffff062a2bc in base::Thread::ThreadMain() ???:0  

#15 0x7ffff062813c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:0  

#16 0x7ffff5c54ece in \_\_asan::AsanThread::ThreadStart() ??:0  

Thread T5 created by T0 here:  

#0 0x7ffff5c52c25 in pthread\_create ??:0  

#1 0x7ffff0627d29 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, unsigned long\*) base/threading/platform\_thread\_posix.cc:0  

#2 0x7ffff0627c2a in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate\*, unsigned long\*) ???:0  

#3 0x7ffff0629aa5 in base::Thread::StartWithOptions(base::Thread::Options const&) ???:0  

#4 0x7ffff062984b in base::Thread::Start() ???:0  

#5 0x7ffff495c8b8 in content::WebKitThread::Initialize() ???:0  

#6 0x7ffff484f231 in content::BrowserMainLoop::RunMainMessageLoopParts(bool\*) ???:0  

#7 0x7ffff484ced4 in BrowserMain(content::MainFunctionParams const&) ???:0  

#8 0x7ffff051129c in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main.cc:0  

#9 0x7ffff0510a94 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#10 0x7fffeede3da7 in ChromeMain ??:0  

#11 0x7fffeede3ccb in main ???:0  

#12 0x7fffe86d4c4d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.2/csu/libc-start.c:260  

==10709== ABORTING  

Stats: 36M malloced (47M for red zones) by 127235 calls  

Stats: 1M realloced by 5102 calls  

Stats: 25M freed by 95428 calls  

Stats: 0M really freed by 0 calls  

Stats: 120M (30735 full pages) mmaped in 30 calls  

mmaps by size class: 8:114681; 9:16382; 10:16380; 11:4094; 12:2048; 13:512; 14:256; 15:128; 16:192; 17:32; 18:16; 19:8; 21:2; 22:3;  

mallocs by size class: 8:106618; 9:4905; 10:12364; 11:1794; 12:798; 13:336; 14:219; 15:28; 16:131; 17:28; 18:8; 19:1; 21:2; 22:3;  

frees by size class: 8:78240; 9:3452; 10:11645; 11:1149; 12:490; 13:144; 14:162; 15:16; 16:116; 17:5; 18:5; 19:1; 21:1; 22:2;  

rfrees by size class:  

Stats: malloc large: 42 small slow: 564  

Shadow byte and word:  

0x1ffffa7dae36: fd  

0x1ffffa7dae30: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffffa7dae10: fd fd fd fd fd fd fd fd  

0x1ffffa7dae18: fd fd fd fd fd fd fd fd  

0x1ffffa7dae20: fa fa fa fa fa fa fa fa  

0x1ffffa7dae28: fa fa fa fa fa fa fa fa  

=>0x1ffffa7dae30: fd fd fd fd fd fd fd fd  

0x1ffffa7dae38: fd fd fd fd fd fd fd fd  

0x1ffffa7dae40: fa fa fa fa fa fa fa fa  

0x1ffffa7dae48: fa fa fa fa fa fa fa fa  

0x1ffffa7dae50: fd fd fd fd fd fd fd fd

## Attachments

- [cursor.html](attachments/cursor.html) (text/plain; charset=iso-8859-1, 2.0 KB)
- [asan.txt](attachments/asan.txt) (text/x-c; charset=us-ascii, 6.0 KB)
- [cursor-big.html](attachments/cursor-big.html) (text/html; charset=iso-8859-1, 18.7 KB)

## Timeline

### ts...@chromium.org (2011-12-19)

[Empty comment from Monorail migration]

### dg...@chromium.org (2011-12-19)

[Empty comment from Monorail migration]

### dg...@chromium.org (2011-12-19)

I can't get this to repro either at ToT or 114785.  aohelin, do you have your other versions of the repro script available?

Hans, can you take a look and see if you can figure out what's going on from the asan output?  There's a problem when a prefetchReset message arrives after the transaction has been aborted.

### ao...@gmail.com (2011-12-20)

The attached version works here at least against 114982. The smaller file apparently got too build-specific, because it didn't trigger this on my other machine here either. This one occurs at WTF::AVLTree.

ASan should report the issue on every load after about a second.

### ao...@gmail.com (2011-12-20)

Slightly cleaner way to reproduce:
$ cd /your/chromium/src/third_party/WebKit/LayoutTests/storage/indexeddb
$ cat cursor-skip-deleted.html | sed -e '/debug("indexCursorTest/{n;n;n;n;n;n;n;n;s/targets/tar\xc0/}' > repro.html
$ chrome-asan repro.html 2>&1 | grep Address
==13643== ERROR: AddressSanitizer heap-use-after-free on address 0x7fb55f728ec0 at pc 0x7fb582685d85 bp 0x7fb56a3032c0 sp 0x7fb56a3032b8


### dg...@chromium.org (2011-12-21)

Thanks for the updated test case, it consistently repros on my machine.  Now to figure out what's going on.

### dg...@chromium.org (2012-01-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-01-05)

https://bugs.webkit.org/show_bug.cgi?id=75596

### ao...@gmail.com (2012-01-05)

The patch from https://bugs.webkit.org/show_bug.cgi?id=75596 fixes the original case and also other files triggering this over here.

### in...@chromium.org (2012-01-06)

http://trac.webkit.org/changeset/104252

### dg...@chromium.org (2012-01-06)

Merged into webkit branch 963.

http://codereview.chromium.org/9121008
http://trac.webkit.org/changeset/104310


### dg...@chromium.org (2012-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2012-01-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-01-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=117196

------------------------------------------------------------------------
r117196 | dgrogan@chromium.org | Wed Jan 11 02:03:08 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=117196&r2=117195&pathrev=117196
 A http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/in_process_webkit/indexed_db_uitest.cc?r1=117196&r2=117195&pathrev=117196
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/chrome_tests.gypi?r1=117196&r2=117195&pathrev=117196

IndexedDB: Run cursor-prefetch webkit layout test as ui test.

The test exercises a bug that is only triggered when run in multi-process chromium.  The patch in https://bugs.webkit.org/show_bug.cgi?id=75596 has to be committed and rolled before this change can be committed.

This ui test will eventually run all of the IDB layout tests.

BUG=108071
TEST=


Review URL: http://codereview.chromium.org/9108004
------------------------------------------------------------------------

### js...@chromium.org (2012-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2012-01-19)

There was a massive re-factoring and this can't be safely merged to m16



### dg...@chromium.org (2012-01-19)

I don't think this vulnerability was present in m16.  I already patched this to webkit branch 963, see https://crbug.com/chromium/108071#c11.

### in...@chromium.org (2012-01-19)

Already merged to 963.

### sc...@gmail.com (2012-01-19)

@tsepez: did you see this crash on stable? https://crbug.com/chromium/108071#c1 sets Mstone-16 and SecImpacts-Stable
@aohelin: any idea if you ever saw stable crash with this?

### ao...@gmail.com (2012-01-19)

@scarybeasts: No. I assumed it did because SecImpacts-Stable was here. I didn't have stable or beta ASan builds at the time, and IIRC this didn't usually manifest as a crash in non-ASan builds.

### js...@chromium.org (2012-01-19)

Looks like @dgrogan is right. The affected code wasn't in the correct file on stable, so we assumed a major refactoring based on the bug flags. However, I can't get it to repro in stable, and it makes far more sense that it was just a mis-click.

### ao...@gmail.com (2012-01-19)

I'll have 16.0.912.75 w/ ASan to check with later today, but indeed looks like this doesn't affect it.

### sc...@gmail.com (2012-02-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

Aki, can't believe we missed nominating this one :)
It's a browser memory corruption => critical, and thanks so much for catching it before we released it to stable!

Congrats on (your first?) $3133.7 Chromium Security Reward!!

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

### ao...@gmail.com (2012-02-07)

@scarybeasts W00t! First one, yes :)

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2012-10-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/108071?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>Storage>IndexedDB, Internals]
[Monorail mergedwith: crbug.com/chromium/107625]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052260)*
