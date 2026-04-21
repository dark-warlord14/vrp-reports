# Use-after-Free in AudioDebugRecordingsHandler::StartAudioDebugRecordings

| Field | Value |
|-------|-------|
| **Issue ID** | [40056720](https://issues.chromium.org/issues/40056720) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC, Platform>Extensions>API |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-07-29 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description


Use-after-Free in AudioDebugRecordingsHandler::StartAudioDebugRecordings


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

# Use-after-Free in AudioDebugRecordingsHandler::StartAudioDebugRecordings
## Root Cause and some notes
The code schedule a call to GetLogDirectoryAndEnsureExists in a thread pool[0] followed by a call to DoStartAudioDebugRecordings with raw pointer `RenderProcessHost* host`[1] on the origin sequence (the ui thread in this case). 

While GetLogDirectoryAndEnsureExists is executed, the `RenderProcessHost* host` is destructed by closing the tab. 

When it returns to the UI thread to execute DoStartAudioDebugRecordings, it will trigger UAF in [2].

```cpp
void AudioDebugRecordingsHandler::StartAudioDebugRecordings(
    content::RenderProcessHost* host,
    base::TimeDelta delay,
    RecordingDoneCallback callback,
    RecordingErrorCallback error_callback) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);

  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE, {base::MayBlock(), base::TaskPriority::BEST_EFFORT},
      base::BindOnce(&GetLogDirectoryAndEnsureExists, browser_context_),//[0] free host by close tab.
      base::BindOnce(&AudioDebugRecordingsHandler::DoStartAudioDebugRecordings,
                     this, host, delay, std::move(callback), // [1]
                     std::move(error_callback)));
}

void AudioDebugRecordingsHandler::DoStartAudioDebugRecordings(
    content::RenderProcessHost* host,
    base::TimeDelta delay,
    RecordingDoneCallback callback,
    RecordingErrorCallback error_callback,
    const base::FilePath& log_directory) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);

  if (audio_debug_recording_session_) {
    std::move(error_callback).Run("Audio debug recordings already in progress");
    return;
  }

  base::FilePath prefix_path = GetAudioDebugRecordingsPrefixPath(
      log_directory, ++current_audio_debug_recordings_id_);
  host->EnableAudioDebugRecordings(prefix_path); //[2] use here!
  ...
}

```

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=75;drc=80def040657db16e79f59e7e3b27857014c0f58d

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=77;drc=80def040657db16e79f59e7e3b27857014c0f58d

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/webrtc/audio_debug_recordings_handler.cc;l=111;drc=80def040657db16e79f59e7e3b27857014c0f58d

**Note that StopAudioDebugRecordings has the same code and can also cause the same UAF.**

This issue is similar to issue-1233942, but the use of issue-1233942 occurs in threadpool, the freed object is BrowserContext, and this issue occurs when returning to the ui thread, the freed object is RenderProcessHost, and the triggering method is also different.

I will report to you as two issues, please decide whether to merge according to your judgment.

The repreoduce note have been explained in issue-1233942 and will not be repeated.

## Reproduce
1. Install the extension in the attachment, and then restart the browser.
2. Start chrome with the following parameters

```
python3 -m http.server 8000
out/release/chrome --enable-audio-debug-recordings-from-extension "about:blank" 127.0.0.1:8000/test.html
```

## uaf log
```
=================================================================
==69973==ERROR: AddressSanitizer: heap-use-after-free on address 0x61a000131a80 at pc 0x565468671a26 bp 0x7ffc972b0ef0 sp 0x7ffc972b0ee8
READ of size 8 at 0x61a000131a80 thread T0 (chrome)
    #0 0x565468671a25 in AudioDebugRecordingsHandler::DoStartAudioDebugRecordings(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&) chrome/browser/media/webrtc/audio_debug_recordings_handler.cc:113:9
    #1 0x565468672d72 in void base::internal::FunctorTraits<void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), void>::Invoke<void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), scoped_refptr<AudioDebugRecordingsHandler>, content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&>(void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), scoped_refptr<AudioDebugRecordingsHandler>&&, content::RenderProcessHost*&&, base::TimeDelta&&, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>&&, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>&&, base::FilePath const&) base/bind_internal.h:509:12
    #2 0x565468672d72 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), scoped_refptr<AudioDebugRecordingsHandler>, content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&>(void (AudioDebugRecordingsHandler::*&&)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), scoped_refptr<AudioDebugRecordingsHandler>&&, content::RenderProcessHost*&&, base::TimeDelta&&, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>&&, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>&&, base::FilePath const&) base/bind_internal.h:648:12
    #3 0x565468672d72 in void base::internal::Invoker<base::internal::BindState<void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), scoped_refptr<AudioDebugRecordingsHandler>, content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> >, void (base::FilePath const&)>::RunImpl<void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), std::__Cr::tuple<scoped_refptr<AudioDebugRecordingsHandler>, content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> >, 0ul, 1ul, 2ul, 3ul, 4ul>(void (AudioDebugRecordingsHandler::*&&)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), std::__Cr::tuple<scoped_refptr<AudioDebugRecordingsHandler>, content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul, 4ul>, base::FilePath const&) base/bind_internal.h:721:12
    #4 0x565468672d72 in base::internal::Invoker<base::internal::BindState<void (AudioDebugRecordingsHandler::*)(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&), scoped_refptr<AudioDebugRecordingsHandler>, content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> >, void (base::FilePath const&)>::RunOnce(base::internal::BindStateBase*, base::FilePath const&) base/bind_internal.h:690:12
    #5 0x5654686731ee in base::OnceCallback<void (base::FilePath const&)>::Run(base::FilePath const&) && base/callback.h:98:12
    #6 0x5654686731ee in void base::internal::ReplyAdapter<base::FilePath, base::FilePath const&>(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*) base/post_task_and_reply_with_result_internal.h:30:23
    #7 0x565468673566 in void base::internal::FunctorTraits<void (*)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), void>::Invoke<void (*)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>(void (*&&)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<void (base::FilePath const&)>&&, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*&&) base/bind_internal.h:404:12
    #8 0x565468673566 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*>(void (*&&)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<void (base::FilePath const&)>&&, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*&&) base/bind_internal.h:648:12
    #9 0x565468673566 in void base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<void (base::FilePath const&)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >, std::__Cr::default_delete<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> > > > >, void ()>::RunImpl<void (*)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), std::__Cr::tuple<base::OnceCallback<void (base::FilePath const&)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >, std::__Cr::default_delete<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> > > > >, 0ul, 1ul>(void (*&&)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), std::__Cr::tuple<base::OnceCallback<void (base::FilePath const&)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >, std::__Cr::default_delete<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> > > > >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:721:12
    #10 0x565468673566 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (base::FilePath const&)>, std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >*), base::OnceCallback<void (base::FilePath const&)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> >, std::__Cr::default_delete<std::__Cr::unique_ptr<base::FilePath, std::__Cr::default_delete<base::FilePath> > > > >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #11 0x7fba51855902 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #12 0x7fba51855902 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReply(base::(anonymous namespace)::PostTaskAndReplyRelay) base/threading/post_task_and_reply_impl.cc:115:29
    #13 0x7fba51855b48 in void base::internal::FunctorTraits<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), void>::Invoke<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay&&) base/bind_internal.h:404:12
    #14 0x7fba51855b48 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay&&) base/bind_internal.h:648:12
    #15 0x7fba51855b48 in void base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunImpl<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::__Cr::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0ul>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::__Cr::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:721:12
    #16 0x7fba51855b48 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #17 0x7fba517ba170 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #18 0x7fba517ba170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #19 0x7fba517fd9aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:344:23
    #20 0x7fba517fd1cb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:258:36
    #21 0x7fba5166e6e9 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:374:46
    #22 0x7fba5166e6e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:124:43
    #23 0x7fba10aa317c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c)

0x61a000131a80 is located 0 bytes inside of 1264-byte region [0x61a000131a80,0x61a000131f70)
freed by thread T0 (chrome) here:
    #0 0x565465966efd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x7fba517ba170 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #2 0x7fba517ba170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #3 0x7fba517fd9aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:344:23
    #4 0x7fba517fd1cb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:258:36
    #5 0x7fba5166d770 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:404:48
    #6 0x7fba517feb3e in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:451:12
    #7 0x7fba517127e1 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:134:14
    #8 0x7fba46eb7222 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:999:18
    #9 0x7fba46ebc015 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #10 0x7fba46eb0d45 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:47:28
    #11 0x7fba48f475c5 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:597:10
    #12 0x7fba48f475c5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1080:10
    #13 0x7fba48f468b9 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:955:12
    #14 0x7fba48f40e7c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:379:36
    #15 0x7fba48f413bc in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:405:10
    #16 0x5654659691bd in ChromeMain chrome/app/chrome_main.cc:151:12
    #17 0x7fba101a80b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:
    #0 0x56546596669d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x7fba47c852be in content::RenderProcessHostImpl::CreateRenderProcessHost(content::BrowserContext*, content::SiteInstanceImpl*) content/browser/renderer_host/render_process_host_impl.cc:1663:10
    #2 0x7fba47c852be in content::(anonymous namespace)::SpareRenderProcessHostManager::WarmupSpareRenderProcessHost(content::BrowserContext*) content/browser/renderer_host/render_process_host_impl.cc:619:34
    #3 0x7fba47c76bb4 in content::(anonymous namespace)::SpareRenderProcessHostManager::PrepareForFutureRequests(content::BrowserContext*) content/browser/renderer_host/render_process_host_impl.cc:726:7
    #4 0x7fba47c76bb4 in content::RenderProcessHostImpl::NotifySpareManagerAboutRecentlyUsedBrowserContext(content::BrowserContext*) content/browser/renderer_host/render_process_host_impl.cc:3105:48
    #5 0x7fba47c2ede2 in content::RenderFrameHostManager::GetSiteInstanceForNavigation(content::UrlInfo const&, content::WebExposedIsolationInfo const&, content::SiteInstanceImpl*, content::SiteInstanceImpl*, content::SiteInstanceImpl*, ui::PageTransition, bool, bool, bool, bool, bool, bool, bool, bool, bool, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >*) content/browser/renderer_host/render_frame_host_manager.cc:1815:5
    #6 0x7fba47c2a269 in content::RenderFrameHostManager::GetSiteInstanceForNavigationRequest(content::NavigationRequest*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >*) content/browser/renderer_host/render_frame_host_manager.cc:2911:52
    #7 0x7fba47c27eef in content::RenderFrameHostManager::GetFrameHostForNavigation(content::NavigationRequest*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >*) content/browser/renderer_host/render_frame_host_manager.cc:876:7
    #8 0x7fba47c275a0 in content::RenderFrameHostManager::DidCreateNavigationRequest(content::NavigationRequest*) content/browser/renderer_host/render_frame_host_manager.cc:815:37
    #9 0x7fba4791bc34 in content::FrameTreeNode::CreatedNavigationRequest(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest> >) content/browser/renderer_host/frame_tree_node.cc:530:21
    #10 0x7fba47b4225d in content::Navigator::Navigate(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest> >, content::ReloadType) content/browser/renderer_host/navigator.cc:580:20
    #11 0x7fba47a93a20 in content::NavigationControllerImpl::NavigateWithoutEntry(content::NavigationController::LoadURLParams const&) content/browser/renderer_host/navigation_controller_impl.cc:3243:21
    #12 0x7fba47a92f0c in content::NavigationControllerImpl::LoadURLWithParams(content::NavigationController::LoadURLParams const&) content/browser/renderer_host/navigation_controller_impl.cc:1138:10
    #13 0x56546cbb50b4 in (anonymous namespace)::LoadURLInContents(content::WebContents*, GURL const&, NavigateParams*) chrome/browser/ui/browser_navigator.cc:387:36
    #14 0x56546cbb2a3b in Navigate(NavigateParams*) chrome/browser/ui/browser_navigator.cc:659:7
    #15 0x56546cca919c in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, bool, std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:311:5
    #16 0x56546ccab7c4 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:580:13
    #17 0x56546cca8353 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool, std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:427:22
    #18 0x56546cca7815 in StartupBrowserCreatorImpl::Launch(Profile*, std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > const&, bool, std::__Cr::unique_ptr<LaunchModeRecorder, std::__Cr::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator_impl.cc:216:3
    #19 0x56546cc9d03f in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__Cr::unique_ptr<LaunchModeRecorder, std::__Cr::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator.cc:645:13
    #20 0x56546cca2e27 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1171:14
    #21 0x56546cc9c452 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1098:10
    #22 0x56546cc99f02 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:580:10
    #23 0x5654685505fd in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1683:25
    #24 0x56546854e792 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1064:18
    #25 0x7fba46eb53dc in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:949:28
    #26 0x7fba4800cf48 in base::OnceCallback<int ()>::Run() && base/callback.h:98:12
    #27 0x7fba4800cf48 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:41:29
    #28 0x7fba46eb49fd in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:857:25
    #29 0x7fba46ebb7ba in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser_main_runner_impl.cc:131:15
    #30 0x7fba46eb0d05 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:43:32
    #31 0x7fba48f475c5 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:597:10
    #32 0x7fba48f475c5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1080:10
    #33 0x7fba48f468b9 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:955:12

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/media/webrtc/audio_debug_recordings_handler.cc:113:9 in AudioDebugRecordingsHandler::DoStartAudioDebugRecordings(content::RenderProcessHost*, base::TimeDelta, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, bool, bool)>, base::OnceCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)>, base::FilePath const&)
Shadow bytes around the buggy address:
  0x0c348001e300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e320: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c348001e330: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c348001e340: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c348001e350:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e360: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e370: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e390: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c348001e3a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==69973==ABORTING
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

- [uaf4.log](attachments/uaf4.log) (text/plain, 25.2 KB)
- [test.html](attachments/test.html) (text/plain, 79 B)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 4.1 KB)
- [uaf4.mp4](attachments/uaf4.mp4) (video/mp4, 9.1 MB)

## Timeline

### et...@gmail.com (2021-07-29)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2021-07-29)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-07-30)

This is in the same code as https://crbug.com/chromium/1233942, about ten lines apart. I think we can merge them into the same bug, but I'll leave it to the VRP panel to decide.

[Monorail components: Blink>WebRTC Platform>Extensions>API]

### [Deleted User] (2021-07-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2021-08-03)

benjaminwagner@: Can you triage?

### et...@gmail.com (2021-08-03)

If you can't reproduce it directly, you can patch here to block it. 
```cpp
base::FilePath GetLogDirectoryAndEnsureExists(
    content::BrowserContext* browser_context) {
+sleep(4);
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

I set close timieout is 2500, 
<script>
    setTimeout(() => {
        window.close();
    }, 2500);
</script>
You can also adjust this time to ensure that the tab is closed before the callback is executed.

It is not necessary to patch the code on my computer,

But if you cannot trigger it directly, you may need to adjust this timeout.

### et...@gmail.com (2021-08-03)

[Comment Deleted]

### be...@chromium.org (2021-08-03)

Since this is essentially a duplicate of https://crbug.com/chromium/1233942, I'll follow up there.

### be...@chromium.org (2021-08-05)

[Empty comment from Monorail migration]

### gr...@chromium.org (2021-08-06)

Henrik A, are you the right one to look at this?

### he...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### he...@chromium.org (2021-08-06)

[Empty comment from Monorail migration]

### gr...@chromium.org (2021-08-12)

[Empty comment from Monorail migration]

### il...@chromium.org (2021-08-12)

The fix would be refactoring of the same code, but it's a separate scenario, so it should be separate.

I believe the solution might be to incorporate AudioDebugRecordingsHandler::DoStopAudioDebugRecordings in AudioDebugRecordingsHandler::StopAudioDebugRecordings.

The hop to the ThreadPool is done only to call base::CreateDirectoryAndGetError. It probably shouldn't be executed on the UI thread, but it can be posted then the logging is started. Then StopAudioDebugRecordings should wait in case that task didn't complete yet.

That way there will be no hop, and since the Stop function is called when the renderer is still alive, there will be no way to UaF here.

There's still an issue with delayed stop posted from the DoStartAudioDebugRecordings though... That definetely should somehow check if the host is still alive...

Maybe instead of passing a pointer to the host, some host id should be passed instead and the method itself should check if that host is alive.


### [Deleted User] (2021-08-12)

eladalon: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2021-08-16)

Is anyone fixing this bug?


### il...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### il...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-08-16)

I'm back from vacation. Let me triage this for urgency when compared to the other stuff on my plate.

### el...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d

commit ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d
Author: Elad Alon <eladalon@chromium.org>
Date: Mon Aug 16 12:48:52 2021

Fix UAF in AudioDebugRecordingsHandler::StartAudioDebugRecordings

Post the RPH's ID instead of a raw pointer to the RPH so as to
allow graceful handling of the case where it is destroyed while
the task is pending.

Bug: 1234284
Change-Id: I0da847fca65ee6333cfb9177c25a9fedc4444082
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097274
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/heads/master@{#912139}

[modify] https://crrev.com/ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc
[modify] https://crrev.com/ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d/chrome/browser/media/webrtc/audio_debug_recordings_handler.h


### el...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-17)

Requesting merge to beta M93 because latest trunk commit (912139) appears to be after beta branch point (902210).

Requesting merge to dev M94 because latest trunk commit (912139) appears to be after dev branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-17)

This bug requires manual review: We are only 13 days from stable.
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

### el...@chromium.org (2021-08-17)

This is only accessible to Google domains, and we're only using it on Googlers. We can just stop for m93 and m94. Björn Terelius has recently started searching for parties who make use of this, and could not find any. We can simply stop collecting these - if we even do - until m95. I don't think cherry-picking is necessary. Thoughts?

### il...@chromium.org (2021-08-18)

Re #27. I think any chrome extension can trigger that. Since it is a security vulnerability, I believe we must merge it as far back as possible.

### te...@chromium.org (2021-08-18)

Re #27. I don't think I've looked into AudioDebugRecordings usage recently.

### el...@chromium.org (2021-08-18)

Ilya, I believe this is not accessible to extensions unless --enable-audio-debug-recordings-from-extension is specified, which means it does not require CP.
Björn, I confused your dealings with RTP dumps with audio-recordings; beg pardon.

### el...@chromium.org (2021-08-18)

Ilya has raised a fine point - that the flag is not required on ChromeOS/Linux.

### el...@chromium.org (2021-08-18)

1. Does your merge fit within the Merge Decision Guidelines?
AFAICT, yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3097274

3. Has the change landed and been verified on ToT?
Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
M-1 would be good.

5. Why are these changes required in this milestone after branch?
Long-standing issue found that can crash the browser-process.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
N/A

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents
No.

### [Deleted User] (2021-08-18)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-19)

Congratulations (again!), Nan Wang and koocola! The VRP Panel has decided to award you $20,000 this report. Excellent work! 

### am...@chromium.org (2021-08-19)

as long as you are okay with performance and stability with the fix for this on Canary, please go ahead and merge to M93, branch 4577, asap (before 5pm PDT tomorrow, Friday, 20 August) so this fix can be in next week's beta release. 

Also this was prior approved for M94 merge, so please go ahead and merge this fix to branch 4606 as well. 

### am...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/28c4d811e3191f7c7ec6daca3aa7f4e5485d3009

commit 28c4d811e3191f7c7ec6daca3aa7f4e5485d3009
Author: Elad Alon <eladalon@chromium.org>
Date: Fri Aug 20 16:02:59 2021

Fix UAF in AudioDebugRecordingsHandler::StartAudioDebugRecordings

Post the RPH's ID instead of a raw pointer to the RPH so as to
allow graceful handling of the case where it is destroyed while
the task is pending.

(cherry picked from commit ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d)

Bug: 1234284
Change-Id: I0da847fca65ee6333cfb9177c25a9fedc4444082
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097274
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#912139}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110193
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#992}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/28c4d811e3191f7c7ec6daca3aa7f4e5485d3009/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc
[modify] https://crrev.com/28c4d811e3191f7c7ec6daca3aa7f4e5485d3009/chrome/browser/media/webrtc/audio_debug_recordings_handler.h


### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5936a8a5c08b4cdb8d4c6f4960dec4dddda83bde

commit 5936a8a5c08b4cdb8d4c6f4960dec4dddda83bde
Author: Elad Alon <eladalon@chromium.org>
Date: Fri Aug 20 16:04:13 2021

Fix UAF in AudioDebugRecordingsHandler::StartAudioDebugRecordings

Post the RPH's ID instead of a raw pointer to the RPH so as to
allow graceful handling of the case where it is destroyed while
the task is pending.

(cherry picked from commit ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d)

Bug: 1234284
Change-Id: I0da847fca65ee6333cfb9177c25a9fedc4444082
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097274
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#912139}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110194
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#169}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/5936a8a5c08b4cdb8d4c6f4960dec4dddda83bde/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc
[modify] https://crrev.com/5936a8a5c08b4cdb8d4c6f4960dec4dddda83bde/chrome/browser/media/webrtc/audio_debug_recordings_handler.h


### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

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
  https://chromium.googlesource.com/chromium/src/+/e7dcf6918690ec951bb501a1725be304fff6816c

commit e7dcf6918690ec951bb501a1725be304fff6816c
Author: Elad Alon <eladalon@chromium.org>
Date: Wed Sep 08 17:32:11 2021

[M90-LTS] Fix UAF in AudioDebugRecordingsHandler::StartAudioDebugRecordings

Post the RPH's ID instead of a raw pointer to the RPH so as to
allow graceful handling of the case where it is destroyed while
the task is pending.

(cherry picked from commit ad3ed52c2e59e40a92193328f22dc7e3dfbaaf6d)

(cherry picked from commit 28c4d811e3191f7c7ec6daca3aa7f4e5485d3009)

Bug: 1234284
Change-Id: I0da847fca65ee6333cfb9177c25a9fedc4444082
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3097274
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#912139}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110193
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4577@{#992}
Cr-Original-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3148112
Reviewed-by: Elad Alon <eladalon@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1582}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/e7dcf6918690ec951bb501a1725be304fff6816c/chrome/browser/media/webrtc/audio_debug_recordings_handler.cc
[modify] https://crrev.com/e7dcf6918690ec951bb501a1725be304fff6816c/chrome/browser/media/webrtc/audio_debug_recordings_handler.h


### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1234284?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC, Platform>Extensions>API]
[Monorail mergedinto: crbug.com/chromium/1233942]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056720)*
