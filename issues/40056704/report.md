# Use-after-Free on AudioDebugRecordingsHandler::StopAudioDebugRecordings

| Field | Value |
|-------|-------|
| **Issue ID** | [40056704](https://issues.chromium.org/issues/40056704) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC, Platform>Extensions>API |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2021-07-28 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description


Use-after-Free on AudioDebugRecordingsHandler::StopAudioDebugRecordings


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

# Use-after-Free on AudioDebugRecordingsHandler::StopAudioDebugRecordings
## Root Cause and some notes
[0] The `browser_context_` is posted to a separate sequence

[1] `browser_context_` may be destroyed in UI by the time the it runs, causing a UAF in GetLogDirectoryAndEnsureExists callback.

```cpp
void AudioDebugRecordingsHandler::StopAudioDebugRecordings(
    content::RenderProcessHost* host,
    RecordingDoneCallback callback,
    RecordingErrorCallback error_callback) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);
  const bool is_manual_stop = true;
  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE, {base::MayBlock(), base::TaskPriority::BEST_EFFORT},
      base::BindOnce(&GetLogDirectoryAndEnsureExists, browser_context_), //---->[0] posttask to ThreadPool
      base::BindOnce(&AudioDebugRecordingsHandler::DoStopAudioDebugRecordings,
                     this, host, is_manual_stop,
                     current_audio_debug_recordings_id_, std::move(callback),
                     std::move(error_callback)));
}
```

**Note that there is the same problem in StartAudioDebugRecordings**

```cpp
base::FilePath GetLogDirectoryAndEnsureExists(
    content::BrowserContext* browser_context) {
  base::FilePath log_dir_path =
      webrtc_logging::TextLogList::GetWebRtcLogDirectoryForBrowserContextPath(
          browser_context->GetPath()); // [1] use here!
  base::File::Error error;
  if (!base::CreateDirectoryAndGetError(log_dir_path, &error)) {
    DLOG(ERROR) << "Could not create WebRTC log directory, error: " << error;
    return base::FilePath();
  }
  return log_dir_path;
}
```
[2] The root cause of this vulnerability is very clear, but to trigger this vulnerability, we need to use webrtcLoggingPrivate, which can be used from the Chrome app or from the chrome extension.
- For chrome app, you only need to add the `webrtcLoggingPrivate.audioDebug` permission in the `permissions` of `manifest.json`.
- For chrome extension, you need to add the option `--enable-audio-debug-recordings-from-extension` in the chrome startup parameters.

**Because I am more familiar with the extension, I chose to provide you with an extension version of the poc and enable the flag, but this vulnerability actually does not require the use of flags, and can also be triggered on Linux and Chrome OS by chrome app.**

```cpp
ExtensionFunction::ResponseAction
WebrtcLoggingPrivateStopAudioDebugRecordingsFunction::Run() {
  if (!CanEnableAudioDebugRecordingsFromExtension(extension())) {
    return RespondNow(Error(""));
  }
-->
bool CanEnableAudioDebugRecordingsFromExtension(
    const extensions::Extension* extension) {
  bool enabled_by_permissions = false;
#if defined(OS_LINUX) || defined(OS_CHROMEOS)
  if (extension) {
    enabled_by_permissions =
        extension->permissions_data()->active_permissions().HasAPIPermission(
            extensions::mojom::APIPermissionID::
                kWebrtcLoggingPrivateAudioDebug);
  }
#endif
  return base::CommandLine::ForCurrentProcess()->HasSwitch(
             ::switches::kEnableAudioDebugRecordingsFromExtension) ||
         enabled_by_permissions;
}
```

[3] In addition, due to conditional competition with the UI thread. The browser_context used by GetLogDirectoryAndEnsureExists is destructed first in UI, so the poc is not stable and may require multiple attempts to trigger.

On my computer, the timeout for closing the browser(to destruct browser_context) is set to 2500, and the success rate is 30%. I use ubuntu 20.04, 8 core and 16G.

```javascript
setTimeout(() => {
        window.close();
    }, 2500);
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=89;drc=80def040657db16e79f59e7e3b27857014c0f58d

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=89;drc=80def040657db16e79f59e7e3b27857014c0f58d

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/webrtc_logging_private/webrtc_logging_private_api.cc;l=503;drc=0775b29ae4f4dc6d3ad250f525d76c97320e6e75
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/webrtc_logging_private/webrtc_logging_private_api.cc;drc=80def040657db16e79f59e7e3b27857014c0f58d;l=39

## Reproduce
1. Install the extension in the attachment, and then restart the browser.
2. Start chrome with the following parameters, and note that test.html must be opened from the command line.
```
python3 -m http.server 8000
out/release/chrome --enable-audio-debug-recordings-from-extension 127.0.0.1:8000/test.html
```

## UAF log
```
[] ~/chromium/src <master> out/release/chrome --enable-audio-debug-recordings-from-extension 127.0.0.1:8000/test.html
[42807:42826:0728/201314.854967:ERROR:database.cc(1714)] Passwords sqlite error 1, errno 0: table logins_temp has 24 columns but 25 values were supplied, sql: INSERT INTO logins_temp SELECT * from logins
[42807:42826:0728/201314.855165:ERROR:login_database.cc(781)] Unable to migrate database from 22 to 29
[42807:42826:0728/201314.905727:ERROR:password_store_impl.cc(55)] Could not create/open login database.
[42841:42841:0728/201315.055466:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
=================================================================
==42807==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000132e80 at pc 0x55f46c26f50a bp 0x7fe9ceaf4a10 sp 0x7fe9ceaf4a08
READ of size 8 at 0x615000132e80 thread T6 (ThreadPoolForeg)
    #0 0x55f46c26f509 in (anonymous namespace)::GetLogDirectoryAndEnsureExists(content::BrowserContext*) chrome/browser/media/webrtc/audio_debug_recordings_handler.cc:48:28
    #1 0x55f46c271155 in base::FilePath base::internal::FunctorTraits<base::FilePath (*)(content::BrowserContext*), void>::Invoke<base::FilePath (*)(content::BrowserContext*), content::BrowserContext*>(base::FilePath (*&&)(content::BrowserContext*), content::BrowserContext*&&) base/bind_internal.h:404:12
    #2 0x55f46c271155 in base::FilePath base::internal::InvokeHelper<false, base::FilePath>::MakeItSo<base::FilePath (*)(content::BrowserContext*), content::BrowserContext*>(base::FilePath (*&&)(content::BrowserContext*), content::BrowserContext*&&) base/bind_internal.h:648:12
    #3 0x55f46c271155 in base::FilePath base::internal::Invoker<base::internal::BindState<base::FilePath (*)(content::BrowserContext*), content::BrowserContext*>, base::FilePath ()>::RunImpl<base::FilePath (*)(content::BrowserContext*), std::__Cr::tuple<content::BrowserContext*>, 0ul>(base::FilePath (*&&)(content::BrowserContext*), std::__Cr::tuple<content::BrowserContext*>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:721:12
    #4 0x55f46c271155 in base::internal::Invoker<base::internal::BindState<base::FilePath (*)(content::BrowserContext*), content::BrowserContext*>, base::FilePath ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #5 0x55f46c271637 in base::OnceCallback<base::FilePath ()>::Run() && base/callback.h:98:12
    #6 0x55f46c271637 in void base::internal::ReturnAsParamAdapter<base::FilePath>(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*) base/post_task_and_reply_with_result_internal.h:22:48
    #7 0x55f46c2719b6 in void base::internal::FunctorTraits<void (*)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), void>::Invoke<void (*)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>(void (*&&)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<base::FilePath ()>&&, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*&&) base/bind_internal.h:404:12
    #8 0x55f46c2719b6 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>(void (*&&)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<base::FilePath ()>&&, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*&&) base/bind_internal.h:648:12
    #9 0x55f46c2719b6 in void base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>, void ()>::RunImpl<void (*)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), std::__Cr::tuple<base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>, 0ul, 1ul>(void (*&&)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), std::__Cr::tuple<base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:721:12
    #10 0x55f46c2719b6 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<base::FilePath ()>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #11 0x7fea24958344 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #12 0x7fea24958344 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunTaskAndPostReply(base::(anonymous namespace)::PostTaskAndReplyRelay) base/threading/post_task_and_reply_impl.cc:97:28
    #13 0x7fea24958b48 in void base::internal::FunctorTraits<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), void>::Invoke<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay&&) base/bind_internal.h:404:12
    #14 0x7fea24958b48 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay&&) base/bind_internal.h:648:12
    #15 0x7fea24958b48 in void base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunImpl<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::__Cr::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0ul>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::__Cr::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:721:12
    #16 0x7fea24958b48 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #17 0x7fea248bd170 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #18 0x7fea248bd170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #19 0x7fea2492a546 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task*) base/task/thread_pool/task_tracker.cc:664:19
    #20 0x7fea24929187 in base::internal::TaskTracker::RunTaskWithShutdownBehavior(base::TaskShutdownBehavior, base::internal::Task*) base/task/thread_pool/task_tracker.cc:679:7
    #21 0x7fea24929187 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker.cc:525:5
    #22 0x7fea24a05d9c in base::internal::TaskTrackerPosix::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&) base/task/thread_pool/task_tracker_posix.cc:22:16
    #23 0x7fea249282ca in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:432:5
    #24 0x7fea24945602 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:367:34
    #25 0x7fea24944a41 in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:262:3
    #26 0x7fea24a07505 in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:96:13
    #27 0x7fe9e3cfc608 in start_thread /build/glibc-eX1tMB/glibc-2.31/nptl/pthread_create.c:477:8

0x615000132e80 is located 0 bytes inside of 456-byte region [0x615000132e80,0x615000133048)
freed by thread T0 (chrome) here:
    #0 0x55f4695655ed in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55f46c69e93b in ProfileDestroyer::DestroyOriginalProfileNow(Profile*) chrome/browser/profiles/profile_destroyer.cc:133:3
    #2 0x55f46c69de1f in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) chrome/browser/profiles/profile_destroyer.cc:61:5
    #3 0x55f46c703625 in ProfileManager::ProfileInfo::~ProfileInfo() chrome/browser/profiles/profile_manager.cc:1687:3
    #4 0x55f46c70b105 in std::__Cr::default_delete<ProfileManager::ProfileInfo>::operator()(ProfileManager::ProfileInfo*) const buildtools/third_party/libc++/trunk/include/memory:1335:5
    #5 0x55f46c70b105 in std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> >::reset(ProfileManager::ProfileInfo*) buildtools/third_party/libc++/trunk/include/memory:1596:7
    #6 0x55f46c70b105 in std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:1550:19
    #7 0x55f46c70b105 in std::__Cr::pair<base::FilePath const, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >::~pair() buildtools/third_party/libc++/trunk/include/utility:297:29
    #8 0x55f46c70b105 in void std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, void*> > >::destroy<std::__Cr::pair<base::FilePath const, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, void, void>(std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, void*> >&, std::__Cr::pair<base::FilePath const, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >*) buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:317:15
    #9 0x55f46c70b105 in std::__Cr::__tree<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, std::__Cr::__map_value_compare<base::FilePath, std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, std::__Cr::less<base::FilePath>, true>, std::__Cr::allocator<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > > > >::destroy(std::__Cr::__tree_node<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #10 0x55f46c70a0a9 in std::__Cr::__tree<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, std::__Cr::__map_value_compare<base::FilePath, std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > >, std::__Cr::less<base::FilePath>, true>, std::__Cr::allocator<std::__Cr::__value_type<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > > > >::~__tree() buildtools/third_party/libc++/trunk/include/__tree:1789:3
    #11 0x55f46c70a0a9 in std::__Cr::map<base::FilePath, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> >, std::__Cr::less<base::FilePath>, std::__Cr::allocator<std::__Cr::pair<base::FilePath const, std::__Cr::unique_ptr<ProfileManager::ProfileInfo, std::__Cr::default_delete<ProfileManager::ProfileInfo> > > > >::~map() buildtools/third_party/libc++/trunk/include/map:1092:5
    #12 0x55f46c70a0a9 in ProfileManager::~ProfileManager() chrome/browser/profiles/profile_manager.cc:534:1
    #13 0x55f46c6eae8d in ProfileManager::~ProfileManager() chrome/browser/profiles/profile_manager.cc:518:35
    #14 0x55f46c155f75 in std::__Cr::default_delete<ProfileManager>::operator()(ProfileManager*) const buildtools/third_party/libc++/trunk/include/memory:1335:5
    #15 0x55f46c155f75 in std::__Cr::unique_ptr<ProfileManager, std::__Cr::default_delete<ProfileManager> >::reset(ProfileManager*) buildtools/third_party/libc++/trunk/include/memory:1596:7
    #16 0x55f46c155f75 in BrowserProcessImpl::StartTearDown() chrome/browser/browser_process_impl.cc:416:22
    #17 0x55f46c151830 in ChromeBrowserMainParts::PostMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1828:21
    #18 0x7fea19fba98b in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() content/browser/browser_main_loop.cc:1039:13
    #19 0x7fea19fbf344 in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser_main_runner_impl.cc:179:17
    #20 0x7fea19fb3f77 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:16
    #21 0x7fea1c04a985 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:597:10
    #22 0x7fea1c04a985 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1080:10
    #23 0x7fea1c049c79 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:955:12
    #24 0x7fea1c04423c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:379:36
    #25 0x7fea1c04477c in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:405:10
    #26 0x55f4695678ad in ChromeMain chrome/app/chrome_main.cc:151:12
    #27 0x7fe9e32ab0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:
    #0 0x55f469564d8d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55f46c68b75a in Profile::CreateProfile(base::FilePath const&, Profile::Delegate*, Profile::CreateMode) chrome/browser/profiles/profile_impl.cc:410:55
    #2 0x55f46c6ef672 in ProfileManager::CreateAndInitializeProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:1797:38
    #3 0x55f46c6ec4e9 in ProfileManager::GetProfile(base::FilePath const&) chrome/browser/profiles/profile_manager.cc:756:10
    #4 0x55f4708a3660 in GetStartupProfile(base::FilePath const&, base::FilePath const&, base::CommandLine const&) chrome/browser/ui/startup/startup_browser_creator.cc:1504:39
    #5 0x55f46c150c63 in (anonymous namespace)::CreatePrimaryProfile(content::MainFunctionParams const&, base::FilePath const&, base::FilePath const&, base::CommandLine const&) chrome/browser/chrome_browser_main.cc:415:13
    #6 0x55f46c14d9df in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1409:14
    #7 0x55f46c14ce82 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1064:18
    #8 0x7fea19fb85dc in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:949:28
    #9 0x7fea1b110148 in base::OnceCallback<int ()>::Run() && base/callback.h:98:12
    #10 0x7fea1b110148 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:41:29
    #11 0x7fea19fb7bfd in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:857:25
    #12 0x7fea19fbe9ba in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser_main_runner_impl.cc:131:15
    #13 0x7fea19fb3f05 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:43:32
    #14 0x7fea1c04a985 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:597:10
    #15 0x7fea1c04a985 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1080:10
    #16 0x7fea1c049c79 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:955:12
    #17 0x7fea1c04423c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:379:36
    #18 0x7fea1c04477c in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:405:10
    #19 0x55f4695678ad in ChromeMain chrome/app/chrome_main.cc:151:12
    #20 0x7fe9e32ab0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

Thread T6 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x55f469524dac in pthread_create /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors.cpp:207:3
    #1 0x7fea24a0676e in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:139:13
    #2 0x7fea24943c8b in base::internal::WorkerThread::Start(base::WorkerThreadObserver*) base/task/thread_pool/worker_thread.cc:109:3
    #3 0x7fea24939685 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)::operator()(base::internal::WorkerThread*) const base/task/thread_pool/thread_group_impl.cc:186:15
    #4 0x7fea24939685 in void base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)>(base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl()::'lambda0'(base::internal::WorkerThread*)) base/task/thread_pool/thread_group_impl.cc:153:9
    #5 0x7fea249391e1 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl() base/task/thread_pool/thread_group_impl.cc:185:23
    #6 0x7fea2492f348 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor() base/task/thread_pool/thread_group_impl.cc:104:31
    #7 0x7fea24930664 in base::internal::ThreadGroupImpl::PushTaskSourceAndWakeUpWorkers(base::internal::TransactionWithRegisteredTaskSource) base/task/thread_pool/thread_group_impl.cc:445:1
    #8 0x7fea24940d30 in base::internal::ThreadPoolImpl::PostTaskWithSequenceNow(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:427:38
    #9 0x7fea2494123d in base::internal::ThreadPoolImpl::PostTaskWithSequence(base::internal::Task, scoped_refptr<base::internal::Sequence>) base/task/thread_pool/thread_pool_impl.cc:444:12
    #10 0x7fea24918bcc in base::internal::PooledSequencedTaskRunner::PostDelayedTask(base::Location const&, base::OnceCallback<void ()>, base::TimeDelta) base/task/thread_pool/pooled_sequenced_task_runner.cc:34:40
    #11 0x7fea246fd142 in base::DeferredSequencedTaskRunner::StartImpl() base/deferred_sequenced_task_runner.cc:122:28
    #12 0x7fea246fd3f3 in base::DeferredSequencedTaskRunner::StartWithTaskRunner(scoped_refptr<base::SequencedTaskRunner>) base/deferred_sequenced_task_runner.cc:89:3
    #13 0x7fea24b0226c in base::tracing::PerfettoPlatform::StartTaskRunner(scoped_refptr<base::SequencedTaskRunner>) base/tracing/perfetto_platform.cc:40:26
    #14 0x7fea1fa0c3f5 in tracing::PerfettoTracedProcess::OnThreadPoolAvailable() services/tracing/public/cpp/perfetto/perfetto_traced_process.cc:301:16
    #15 0x7fea1fa8571e in tracing::InitTracingPostThreadPoolStartAndFeatureList() services/tracing/public/cpp/trace_startup.cc:102:33
    #16 0x7fea1c04a2be in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1021:5
    #17 0x7fea1c049c79 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:955:12
    #18 0x7fea1c04423c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:379:36
    #19 0x7fea1c04477c in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:405:10
    #20 0x55f4695678ad in ChromeMain chrome/app/chrome_main.cc:151:12
    #21 0x7fe9e32ab0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/media/webrtc/audio_debug_recordings_handler.cc:48:28 in (anonymous namespace)::GetLogDirectoryAndEnsureExists(content::BrowserContext*)
Shadow bytes around the buggy address:
  0x0c2a8001e580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e590: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e5a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e5b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e5c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c2a8001e5d0:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e5e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e5f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8001e600: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c2a8001e610: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a8001e620: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==42807==ABORTING
```


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

This vulnerability can be used for sandbox escape, because the vulnerability is in the browser process, not in the render.



---

### The cause


#### What version of Chrome have you found the security issue in?

[ >= 92.0.4515.107] + [stable]


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Sandbox Escape 


#### Please provide your credit information

Nan Wang (@eternalsakura13) and koocola (@alo_cook) of 360 Alpha Lab




## Attachments

- [uaf_0728.mp4](attachments/uaf_0728.mp4) (video/mp4, 7.7 MB)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 4.2 KB)
- [test.html](attachments/test.html) (text/plain, 79 B)
- [uaf.log](attachments/uaf.log) (text/plain, 22.9 KB)
- [uaf2.mp4](attachments/uaf2.mp4) (video/mp4, 7.6 MB)

## Timeline

### et...@gmail.com (2021-07-28)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2021-07-28)

[Empty comment from Monorail migration]

### et...@gmail.com (2021-07-28)

https://chromium-review.googlesource.com/c/chromium/src/+/3041006
The pattern of this vulnerability is similar to this patch.

### et...@gmail.com (2021-07-29)

If you can't reproduce it directly, you can patch here to block it. This step is not necessary, just for advice.

In addition, I recorded a new video, including the complete process.

If you have any questions, please feel free to contact me. thanks :)
```cpp
base::FilePath GetLogDirectoryAndEnsureExists(
    content::BrowserContext* browser_context) {
+sleep(3);
  base::FilePath log_dir_path =
      webrtc_logging::TextLogList::GetWebRtcLogDirectoryForBrowserContextPath(
          browser_context->GetPath()); // [1] use here!
  base::File::Error error;
  if (!base::CreateDirectoryAndGetError(log_dir_path, &error)) {
    DLOG(ERROR) << "Could not create WebRTC log directory, error: " << error;
    return base::FilePath();
  }
  return log_dir_path;
}
```

### me...@chromium.org (2021-07-30)

guidou: Could you PTAL?

This codepath is only reachable from a private extension API so I don't think it's readily exploitable unless one can XSS an extension that has access to this API. Assigning medium severity based on that observation.

[Monorail components: Blink>WebRTC>Network Platform>Extensions>API]

### me...@chromium.org (2021-07-30)

No extensions on Android

### me...@chromium.org (2021-07-30)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WebRTC>Network Blink>WebRTC]

### me...@chromium.org (2021-07-30)

Similar to https://crbug.com/chromium/1234284.

### [Deleted User] (2021-07-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2021-08-03)

Hello, is anyone fixing this vulnerability?

### gu...@chromium.org (2021-08-03)

benjaminwagner@: Can you triage?

### be...@chromium.org (2021-08-03)

If I understand correctly, this vulnerability is limited to Linux and ChromeOS where an extension has the WebrtcLoggingPrivateAudioDebug permission enabled. (It's also possible if the enable-audio-debug-recordings-from-extension command-line flag is set.)

### et...@gmail.com (2021-08-04)

Yes, I think if not enable command-line flag, it will only trigger in Linux and ChromeOS.

### be...@chromium.org (2021-08-05)

Sending to grunell@chromium.org based on https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/webrtc_logging_private/OWNERS

### gr...@chromium.org (2021-08-06)

Henrik A, are you the right one to look at this?

### he...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### he...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### he...@chromium.org (2021-08-06)

[Comment Deleted]

### he...@chromium.org (2021-08-06)

eternalsakuraalpha@gmail.com: you are using an ASAN build. Which exact version was used? Does it still reproduce?

### he...@chromium.org (2021-08-06)

I don't have access to a Linux machine and will be OOO for the upcoming two weeks; hence not the best owner. Have not worked in this code base.

Can only refer to the owners at this stage but adding more resources to the CC list.

### et...@gmail.com (2021-08-06)

I can reproduce this vulnerability in the latest code from stable, but only in linux


### he...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### he...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### et...@gmail.com (2021-08-06)

This is the latest chromium commit hash I tested.
But it can also be triggered on the stable version

commit e082b60694320a9d60c84be3a3fb1847c1789e48 (HEAD -> master, origin/master, origin/main, origin/HEAD)
Author: Harkiran Bolaria <hbolaria@google.com>
Date:   Thu Jul 29 09:40:01 2021 +0000

build args
[] ~/chromium/src <master> cat out/release/args.gn                                           
is_debug = false
is_component_build = true
is_asan = true
symbol_level = 2

### he...@chromium.org (2021-08-06)

In the video, I can't see that you load the attached extension or that any JS runs in the browser. Care to elaborate?

### he...@chromium.org (2021-08-06)

Is the process in the video perfectly inline with the initial report?

### et...@gmail.com (2021-08-06)

[Comment Deleted]

### et...@gmail.com (2021-08-06)

[Comment Deleted]

### et...@gmail.com (2021-08-06)

Sorry, please refer to https://crbug.com/chromium/1233942#c4, I have already loaded the extension for the original video.


### et...@gmail.com (2021-08-06)

henrika@chromium.org  sorry, please refer to https://crbug.com/chromium/1233942#c4.
In addition, I gave another plugin and another trigger process in issue-1234284 to trigger the uaf of renderprocesshost in another callback.
And this vulnerability is the uaf of browsercontext.
Please pay attention to the difference when repairing.

### gr...@chromium.org (2021-08-06)

I took a look at this and my guess is that this is a lifetime issue. I believe the BrowserContext goes away when the browser is closed and this should not execute after it has. I haven't worked in Chrome for two years so I don't have this fresh in memory.

### kr...@chromium.org (2021-08-09)

[Empty comment from Monorail migration]

### il...@chromium.org (2021-08-12)

eladalon@ You are the remaining owner of chrome/browser/media/webrtc/ and chrome/browser/extensions/api/webrtc_logging_private/ which are involved in this vulterability.

Please take a look.

### il...@chromium.org (2021-08-12)

Am I understanding the issue correctly? The browser gets closed, it on main ui thread destroys the BrowserContext. However, shortly before that the extension has triggered WebrtcLoggingPrivateStopAudioDebugRecordingsFunction, which inside has posted something to a ThreadPool [1]. Then the pool starts executing this, the browser context is already destroyed.

That situation may happen anywhere where ThreadPool is used, so it would be surprising if there were no mechanism to ensure that doesn't happen.
And it seems to be there [2].

I suggest experimenting with task traits when posting the task in [1]. Maybe SKIP_ON_SHUTDOWN is even more preferable than BLOCK_SHUTDOWN, but I'm not sure what exactly this method should do.

Another way is maybe to get done with the browser_context_ before posting the task in [1]. it's only used to extract a path [3].

I'm not sure, maybe this can be done on the UI thread safely. Then the posted task will receive the path instead of a browser_context_.

The second solution might even be better.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=87;drc=80def040657db16e79f59e7e3b27857014c0f58d

[2] https://source.chromium.org/chromium/chromium/src/+/main:base/task/task_traits.h;l=117;drc=6fdd6d4796fc076fd06f31bce5ea2426e478620c

[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=46;drc=6fdd6d4796fc076fd06f31bce5ea2426e478620c

### et...@gmail.com (2021-08-12)

Yes, but close the browser is just one way to trigger the UAF.
I noticed that [1] hold the raw pointer of host and the host can be destroyed if we close the page when thread pool is run.  You can see https://crbugs.com/1234284.  (duplicate with this bug)

  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE, {base::MayBlock(), base::TaskPriority::BEST_EFFORT},
      base::BindOnce(&GetLogDirectoryAndEnsureExists, browser_context_), 
      base::BindOnce(&AudioDebugRecordingsHandler::DoStopAudioDebugRecordings,
                     this, host, is_manual_stop,
                     current_audio_debug_recordings_id_, std::move(callback),
                     std::move(error_callback)));[1]

### il...@chromium.org (2021-08-12)

eternalsakuraalpha@ please CC me on that other bug, otherwise I don't have an access.


### et...@gmail.com (2021-08-12)

Sorry, I don't have the permission to CC.It seems need security team's help. amyressler@ ,could you help to CC ilnik to issue: 1234284?Thanks.

### et...@gmail.com (2021-08-12)

@grunell@chromium.org
could you help to CC ilnik to issue: 1234284? Thanks.


### gr...@chromium.org (2021-08-12)

Done. (That bug should maybe be reopened since, as noted in https://crbug.com/chromium/1233942#c35, it's related but is a uaf of a different object.)

### et...@gmail.com (2021-08-12)

hello, grunell@chromium.org.
Can you consider canceling the Duplicate of 1234284 and reopening it? I think they should be treated as two vulnerabilities


### [Deleted User] (2021-08-12)

eladalon: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2021-08-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520

commit 5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520
Author: Tony Herre <toprice@chromium.org>
Date: Fri Aug 13 16:13:42 2021

Don't retain BrowserContext on stopping audio debug recordings

Grab the BrowserContext's path and just post that when stopping audio
debug recordings, rather than passing a raw pointer to the full
BrowserContext object, which might be destroyed in the meantime.

Both the BrowserContext and AudioDebugRecordingsHandler are owned by the
RenderProcessHost so we should be ok to access the BrowserContext were
we are now, within ADRH.

Bug: 1233942
Change-Id: Ic3a4b71bc4ccb93d17c904047b6f310717409ffb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094211
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/master@{#911765}

[modify] https://crrev.com/5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc


### to...@chromium.org (2021-08-13)

With this change, we're no longer dereferencing the BrowserContext raw pointer within the posted task, so aren't at risk of using it after free.

Note I've not actually reproduced the issue or verified the fix on that just yet but am very confident this fix covers it.

### to...@chromium.org (2021-08-13)

[Empty comment from Monorail migration]

### et...@gmail.com (2021-08-13)

hello, toprice@chromium.org
Can you fix another issue at the same time?
https://bugs.chromium.org/p/chromium/issues/detail?id=1234284

### [Deleted User] (2021-08-13)

This bug requires manual review: We don't branch M94 until 2021-08-12.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### sr...@google.com (2021-08-16)

Merge approved for M94 branch:4606 please merge asap ( pls merge once it is verified on canary)

### il...@chromium.org (2021-08-18)

Tony, could you also request merges to M93 and M92?

This vulnerability is exploitable in the wild, however, only on linux and with a special extension installed outside of the chrome web store (since it will probably limit this private api permission).

### to...@chromium.org (2021-08-18)

SG, requesting earlier merges too.

Merge to 94 is in CQ in crrev.com/c/3103312.

### il...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-18)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b668652bcd4bd9bfd55abcea22ca45460db5e21d

commit b668652bcd4bd9bfd55abcea22ca45460db5e21d
Author: Tony Herre <toprice@chromium.org>
Date: Wed Aug 18 13:32:56 2021

Don't retain BrowserContext on stopping audio debug recordings

Grab the BrowserContext's path and just post that when stopping audio
debug recordings, rather than passing a raw pointer to the full
BrowserContext object, which might be destroyed in the meantime.

Both the BrowserContext and AudioDebugRecordingsHandler are owned by the
RenderProcessHost so we should be ok to access the BrowserContext were
we are now, within ADRH.

(cherry picked from commit 5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520)

Bug: 1233942
Change-Id: Ic3a4b71bc4ccb93d17c904047b6f310717409ffb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094211
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#911765}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3103312
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#81}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/b668652bcd4bd9bfd55abcea22ca45460db5e21d/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc


### am...@google.com (2021-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-19)

Congratulations, Nan Wang and koocola! The VRP Panel has decided to award you $20,000 for this report. Nice work! 

### am...@chromium.org (2021-08-19)

Approving merge to M93, please merge to branch 4577 asap and by 5pm PDT tomorrow (Friday, 20 August) so that this fix can be in next week's M93 beta. 

Also, at your convenience, please go ahead and merge to M92, branch 4515. Though there are no further planned stable channel respins for M92, this branch will become the Extended Stable release channel as we transition to the 4W stable channel release cycle. Thank you! 

### am...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d99c9e2eeb012890d4581c64195accf3e44af45

commit 4d99c9e2eeb012890d4581c64195accf3e44af45
Author: Tony Herre <toprice@chromium.org>
Date: Mon Aug 23 16:39:49 2021

Don't retain BrowserContext on stopping audio debug recordings

Grab the BrowserContext's path and just post that when stopping audio
debug recordings, rather than passing a raw pointer to the full
BrowserContext object, which might be destroyed in the meantime.

Both the BrowserContext and AudioDebugRecordingsHandler are owned by the
RenderProcessHost so we should be ok to access the BrowserContext were
we are now, within ADRH.

(cherry picked from commit 5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520)

Bug: 1233942
Change-Id: Ic3a4b71bc4ccb93d17c904047b6f310717409ffb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094211
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#911765}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110463
Cr-Commit-Position: refs/branch-heads/4577@{#1067}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/4d99c9e2eeb012890d4581c64195accf3e44af45/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc


### sr...@google.com (2021-08-27)

assigning back to get engineer attention for M92 merge ( please merge asap) for extended stable release. Complete by 3pm PST today

### [Deleted User] (2021-08-27)

[Empty comment from Monorail migration]

### sr...@google.com (2021-08-30)

Can some one please submit this CL to CQ - https://chromium-review.googlesource.com/c/chromium/src/+/3128031

### il...@google.com (2021-08-30)

I've pressed CQ+2.

### gi...@appspot.gserviceaccount.com (2021-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61a77a0143056bb659b0087ffbcba2a525755467

commit 61a77a0143056bb659b0087ffbcba2a525755467
Author: Tony Herre <toprice@chromium.org>
Date: Mon Aug 30 15:21:52 2021

Don't retain BrowserContext on stopping audio debug recordings

Grab the BrowserContext's path and just post that when stopping audio
debug recordings, rather than passing a raw pointer to the full
BrowserContext object, which might be destroyed in the meantime.

Both the BrowserContext and AudioDebugRecordingsHandler are owned by the
RenderProcessHost so we should be ok to access the BrowserContext were
we are now, within ADRH.

(cherry picked from commit 5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520)

Bug: 1233942
Change-Id: Ic3a4b71bc4ccb93d17c904047b6f310717409ffb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094211
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#911765}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3128031
Auto-Submit: Tony Herre <toprice@chromium.org>
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2097}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/61a77a0143056bb659b0087ffbcba2a525755467/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc


### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-31)

returning to fixed as was re-opened as nudge for merge 

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-09-08)

LTS merge approved

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d6106fc8fd0cd7c266a6127071744e313a138239

commit d6106fc8fd0cd7c266a6127071744e313a138239
Author: Tony Herre <toprice@chromium.org>
Date: Wed Sep 08 18:27:57 2021

[M90-LTS] Don't retain BrowserContext on stopping audio debug recordings

Grab the BrowserContext's path and just post that when stopping audio
debug recordings, rather than passing a raw pointer to the full
BrowserContext object, which might be destroyed in the meantime.

Both the BrowserContext and AudioDebugRecordingsHandler are owned by the
RenderProcessHost so we should be ok to access the BrowserContext were
we are now, within ADRH.

(cherry picked from commit 5c788f4a3cc0762f8a21a50ccbd1b407b3bdf520)

(cherry picked from commit 61a77a0143056bb659b0087ffbcba2a525755467)

Bug: 1233942
Change-Id: Ic3a4b71bc4ccb93d17c904047b6f310717409ffb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094211
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#911765}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3128031
Auto-Submit: Tony Herre <toprice@chromium.org>
Commit-Queue: Ilya Nikolaevskiy <ilnik@chromium.org>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#2097}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3148014
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1586}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/d6106fc8fd0cd7c266a6127071744e313a138239/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc


### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1233942?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC, Platform>Extensions>API]
[Monorail mergedwith: crbug.com/chromium/1234284]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056704)*
