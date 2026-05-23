# heap-use-after-free in cc::LayerTreeHost::NotifyTransitionRequestsFinished

| Field | Value |
|-------|-------|
| **Issue ID** | [411573532](https://issues.chromium.org/issues/411573532) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation, Internals>Services>Viz |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | vm...@chromium.org |
| **Created** | 2025-04-18 |
| **Bounty** | $11,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

## Reproduction Steps

- python -m http.server 8000
- Run: `chrome --headless --no-sandbox --user-data-dir=test --enable-logging=stderr http://localhost:8000/poc.html?url=http://localhost:8000/poc.html`
- Press the Escape key to trigger the bug

## About `headless`

The `headless` flag is added for easier reproduction—without it, a print dialog would pop up, but the vulnerability will still trigger no matter which button the user clicks in the print page.

## Root Cause Analysis (RCA)

- In the NotifyTransitionRequestsFinished function, the iterator of view\_transition\_callbacks\_ is first obtained
- Then, in [1] the code calls the callback function, which causes the iterator to become invalid
- Using the iterator leads to a UAF

```
https://source.chromium.org/chromium/chromium/src/+/main:cc/trees/layer_tree_host.cc;drc=d5e762e022c4d40d97ee0dc70521b161d72a06b1;l=538
void LayerTreeHost::NotifyTransitionRequestsFinished(
    const uint32_t sequence_id,
    const viz::ViewTransitionElementResourceRects& rects) {
  DCHECK(IsMainThread());
  // TODO(vmpstr): This might also be a good spot to expire long standing
  // requests if they were not finished.
  auto it = view_transition_callbacks_.find(sequence_id);
  if (it == view_transition_callbacks_.end()) {
    return;
  }
  std::move(it->second).Run(rects);       <<[1]>>
  view_transition_callbacks_.erase(it);
}

```

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab]

## ASAN

```
=================================================================
==16784==ERROR: AddressSanitizer: heap-use-after-free on address 0x11b78c231e70 at pc 0x7ffe820f176e bp 0x00aad99fb780 sp 0x00aad99fb7c8
READ of size 4 at 0x11b78c231e70 thread T0
    #0 0x7ffe820f176d in std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >::operator= C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__utility\pair.h:236
    #1 0x7ffe820f176d in std::__Cr::__move_impl<std::__Cr::_ClassicAlgPolicy>::operator() C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__algorithm\move.h:46
    #2 0x7ffe820f176d in std::__Cr::__copy_move_unwrap_iters C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__algorithm\copy_move_common.h:94
    #3 0x7ffe820f176d in std::__Cr::__move C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__algorithm\move.h:122
    #4 0x7ffe820f176d in std::__Cr::move C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__algorithm\move.h:132
    #5 0x7ffe820f176d in std::__Cr::vector<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > >::erase C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__vector\vector.h:1175
    #6 0x7ffe820f176d in base::internal::flat_tree<unsigned int, struct base::internal::GetFirst, struct std::__Cr::less<void>, class std::__Cr::vector<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>, class std::__Cr::allocator<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>>>>::erase(class std::__Cr::__wrap_iter<struct std::__Cr::pair<unsigned int, class base::OnceCallback<void __cdecl(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>> *>) C:\b\s\w\ir\cache\builder\src\base\containers\flat_tree.h:862:16
    #7 0x7ffe820f132b in cc::LayerTreeHost::NotifyTransitionRequestsFinished(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:539:30
    #8 0x7ffe820b45e9 in base::internal::DecayedFunctorTraits<void (ProxyMain::*)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain> &&,unsigned int &&,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #9 0x7ffe820b45e9 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (ProxyMain::*&&)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain> &&,unsigned int &&,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #10 0x7ffe820b45e9 in base::internal::Invoker<base::internal::FunctorTraits<void (ProxyMain::*&&)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain> &&,unsigned int &&,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &&>,base::internal::BindState<1,1,0,void (ProxyMain::*)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain>,unsigned int,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #11 0x7ffe820b45e9 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl cc::ProxyMain::*&&)(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &), class base::WeakPtr<class cc::ProxyMain> &&, unsigned int &&, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl cc::ProxyMain::*)(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &), class base::WeakPtr<class cc::ProxyMain>, unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #12 0x7ffe7ce169d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #13 0x7ffe7ce169d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #14 0x7ffe7cde9a29 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #15 0x7ffe7cde9a29 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #16 0x7ffe7cde88cf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #17 0x7ffe7cf49427 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #18 0x7ffe7cdeb751 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #19 0x7ffe7ce8643e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #20 0x7ffe9278f8fb in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:369:16
    #21 0x7ffe79901686 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:781:14
    #22 0x7ffe799039d1 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1155:10
    #23 0x7ffe798f7ab3 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #24 0x7ffe798f866d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #25 0x7ffe6a1116bb in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #26 0x7ff6e68147bb in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #27 0x7ff6e6812021 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #28 0x7ff6e6cc55fb in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #29 0x7ff6e6cc55fb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #30 0x7fff890ae8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #31 0x7fff8b1dbf6b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800bbf6b)

0x11b78c231e70 is located 16 bytes inside of 32-byte region [0x11b78c231e60,0x11b78c231e80)
freed by thread T0 here:
    #0 0x7fff3e30b244  (E:\chrome_asan\asan-win32-release_x64-1448748\clang_rt.asan_dynamic-x86_64.dll+0x18005b244)
    #1 0x7ffe82107583 in std::__Cr::__libcpp_operator_delete C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__new\allocate.h:46
    #2 0x7ffe82107583 in std::__Cr::__libcpp_deallocate C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__new\allocate.h:86
    #3 0x7ffe82107583 in std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > >::deallocate C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\allocator.h:120
    #4 0x7ffe82107583 in std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > >::deallocate C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\allocator_traits.h:289
    #5 0x7ffe82107583 in std::__Cr::__split_buffer<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > &>::~__split_buffer C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__split_buffer:337
    #6 0x7ffe82107583 in std::__Cr::vector<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>, class std::__Cr::allocator<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>>>::emplace<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>(class std::__Cr::__wrap_iter<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>> const *>, unsigned int &&, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)> &&) C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__vector\vector.h:1263:3
    #7 0x7ffe820f7902 in base::internal::flat_tree<unsigned int,base::internal::GetFirst,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > > >::unsafe_emplace C:\b\s\w\ir\cache\builder\src\base\containers\flat_tree.h:1103
    #8 0x7ffe820f7902 in base::flat_map<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)>,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > > >::operator[] C:\b\s\w\ir\cache\builder\src\base\containers\flat_map.h:294
    #9 0x7ffe820f7902 in cc::LayerTreeHost::AddViewTransitionRequest(class std::__Cr::unique_ptr<class cc::ViewTransitionRequest, struct std::__Cr::default_delete<class cc::ViewTransitionRequest>>) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:975:5
    #10 0x7ffe8b6a36b4 in blink::PaintArtifactCompositor::Update(class blink::PaintArtifact const &, struct blink::PaintArtifactCompositor::ViewportProperties const &, class blink::HeapVector<class cppgc::internal::BasicMember<class blink::TransformPaintPropertyNode const, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 32> const &, class WTF::Vector<class std::__Cr::unique_ptr<class cc::ViewTransitionRequest, struct std::__Cr::default_delete<class cc::ViewTransitionRequest>>, 0, class WTF::PartitionAllocator>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\graphics\compositing\paint_artifact_compositor.cc:980:11
    #11 0x7ffe899cc848 in blink::LocalFrameView::PushPaintArtifactToCompositor(bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3016:31
    #12 0x7ffe899c8877 in blink::LocalFrameView::RunPaintLifecyclePhase(enum blink::PaintBenchmarkMode) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2683:5
    #13 0x7ffe899c6e6b in blink::LocalFrameView::UpdateLifecyclePhasesInternal(enum blink::DocumentLifecycle::LifecycleState) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2378:3
    #14 0x7ffe899c29cf in blink::LocalFrameView::UpdateLifecyclePhases(enum blink::DocumentLifecycle::LifecycleState, enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2163:3
    #15 0x7ffe899c210e in blink::LocalFrameView::UpdateAllLifecyclePhases(enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:1887:54
    #16 0x7ffe878671f4 in blink::PageAnimator::UpdateAllLifecyclePhases(class blink::LocalFrame &, enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\page_animator.cc:397:9
    #17 0x7ffe8987caf5 in blink::WebFrameWidgetImpl::UpdateLifecycle(enum blink::WebLifecycleUpdate, enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1764:14
    #18 0x7ffe8b359f6d in blink::WidgetBase::UpdateVisualState(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:1054:12
    #19 0x7ffe820ef283 in cc::LayerTreeHost::RequestMainFrameUpdate(bool) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:402:12
    #20 0x7ffe820c0359 in cc::ProxyMain::BeginMainFrame(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>) C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:297:21
    #21 0x7ffe820b64be in base::internal::DecayedFunctorTraits<void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #22 0x7ffe820b64be in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #23 0x7ffe820b64be in base::internal::Invoker<base::internal::FunctorTraits<void (ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>,base::internal::BindState<1,1,0,void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #24 0x7ffe820b64be in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl cc::ProxyMain::*&&)(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>), class base::WeakPtr<class cc::ProxyMain> &&, class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl cc::ProxyMain::*)(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>), class base::WeakPtr<class cc::ProxyMain>, class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #25 0x7ffe7ce169d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #26 0x7ffe7ce169d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #27 0x7ffe7cde9a29 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #28 0x7ffe7cde9a29 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #29 0x7ffe7cde88cf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #30 0x7ffe7cf49427 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #31 0x7ffe7cdeb7c8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:626:12
    #32 0x7ffe7ce8643e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #33 0x7ffe93241ceb in printing::PrintRenderFrameHelper::RequestPrintPreview(enum printing::PrintRenderFrameHelper::PrintPreviewRequestType, bool) C:\b\s\w\ir\cache\builder\src\components\printing\renderer\print_render_frame_helper.cc:2694:12
    #34 0x7ffe93240d49 in printing::PrintRenderFrameHelper::ScriptedPrint(bool) C:\b\s\w\ir\cache\builder\src\components\printing\renderer\print_render_frame_helper.cc:1229:5
    #35 0x7ffe928c9795 in content::RenderFrameImpl::ScriptedPrint(void) C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc:2104:14
    #36 0x7ffe895a09d1 in blink::ChromeClientImpl::PrintDelegate(class blink::LocalFrame *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\chrome_client_impl.cc:777:24
    #37 0x7ffe87f39d6d in blink::ChromeClient::Print(class blink::LocalFrame *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\chrome_client.cc:282:3
    #38 0x7ffe8a127890 in blink::EditorCommand::Execute(class WTF::String const &, class blink::Event *) const C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\commands\editor_command.cc:2161:10
    #39 0x7ffe8d9aa9e2 in blink::Document::execCommand(class WTF::String const &, bool, class blink::V8UnionStringOrTrustedHTML const *, class blink::ExceptionState &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\commands\document_exec_command.cc:149:25
    #40 0x7ffe8da0a4db in blink::`anonymous namespace'::v8_document::ExecCommandOperationCallback C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\bindings\modules\v8\v8_document.cc:6933:39
    #41 0x7ffe93ad1b44 in Builtins_CallApiCallbackGeneric (E:\chrome_asan\asan-win32-release_x64-1448748\chrome.dll+0x1a99c1b44)
    #42 0x7ffe93acfd34 in Builtins_InterpreterEntryTrampoline (E:\chrome_asan\asan-win32-release_x64-1448748\chrome.dll+0x1a99bfd34)
    #43 0x7ffe93acfd34 in Builtins_InterpreterEntryTrampoline (E:\chrome_asan\asan-win32-release_x64-1448748\chrome.dll+0x1a99bfd34)
    #44 0x7ffe93acd29b in Builtins_JSEntryTrampoline (E:\chrome_asan\asan-win32-release_x64-1448748\chrome.dll+0x1a99bd29b)
    #45 0x7ffe93accdfe in Builtins_JSEntry (E:\chrome_asan\asan-win32-release_x64-1448748\chrome.dll+0x1a99bcdfe)
    #46 0x7ffe6f5eefbe in v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call C:\b\s\w\ir\cache\builder\src\v8\src\execution\simulator.h:212
    #47 0x7ffe6f5eefbe in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:440:22
    #48 0x7ffe6f5ed68d in v8::internal::Execution::Call(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::Object>, class v8::internal::DirectHandle<class v8::internal::Object>, class v8::base::Vector<class v8::internal::DirectHandle<class v8::internal::Object> const>) C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:530:10
    #49 0x7ffe6f009468 in v8::Function::Call(class v8::Isolate *, class v8::Local<class v8::Context>, class v8::Local<class v8::Value>, int, class v8::Local<class v8::Value> *const) C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5427:7
    #50 0x7ffe8aeb6c68 in blink::V8ScriptRunner::CallFunction(class v8::Local<class v8::Function>, class blink::ExecutionContext *, class v8::Local<class v8::Value>, int, class v8::Local<class v8::Value> *const, class v8::Isolate *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:886:48
    #51 0x7ffe8ce54106 in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase,0,1>::CallInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:142
    #52 0x7ffe8ce54106 in blink::bindings::CallbackInvokeHelper<class blink::CallbackFunctionWithTaskAttributionBase, 0, 1>::Call(int, class v8::Local<class v8::Value> *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:157:10
    #53 0x7ffe8ce5cf3c in blink::V8ViewTransitionCallback::Invoke(class blink::bindings::V8ValueOrScriptWrappableAdapter) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\bindings\core\v8\v8_view_transition_callback.cc:57:13
    #54 0x7ffe8a492c00 in blink::DOMViewTransition::InvokeDOMChangeCallback(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\view_transition\dom_view_transition.cc:234:31
    #55 0x7ffe8a4802c9 in blink::ViewTransition::ProcessCurrentState(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\view_transition\view_transition.cc:528:27
    #56 0x7ffe8a48ae5f in base::internal::DecayedFunctorTraits<void (ViewTransition::*)(const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),blink::ViewTransition *>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #57 0x7ffe8a48ae5f in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (ViewTransition::*&&)(const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),blink::ViewTransition *>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #58 0x7ffe8a48ae5f in base::internal::Invoker<base::internal::FunctorTraits<void (ViewTransition::*&&)(const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),blink::ViewTransition *>,base::internal::BindState<1,1,0,void (ViewTransition::*)(const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),blink::internal::BasicUnwrappingCrossThreadHandle<blink::ViewTransition,blink::internal::WeakCrossThreadHandleWeaknessPolicy> >,void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #59 0x7ffe8a48ae5f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::ViewTransition::*&&)(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &), class blink::ViewTransition *>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::ViewTransition::*)(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &), class blink::internal::BasicUnwrappingCrossThreadHandle<class blink::ViewTransition, struct blink::internal::WeakCrossThreadHandleWeaknessPolicy>>, (class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>::RunOnce(class base::internal::BindStateBase *, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #60 0x7ffe820f1300 in base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #61 0x7ffe820f1300 in cc::LayerTreeHost::NotifyTransitionRequestsFinished(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:538:25
    #62 0x7ffe820b45e9 in base::internal::DecayedFunctorTraits<void (ProxyMain::*)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain> &&,unsigned int &&,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #63 0x7ffe820b45e9 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (ProxyMain::*&&)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain> &&,unsigned int &&,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #64 0x7ffe820b45e9 in base::internal::Invoker<base::internal::FunctorTraits<void (ProxyMain::*&&)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain> &&,unsigned int &&,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &&>,base::internal::BindState<1,1,0,void (ProxyMain::*)(unsigned int, const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &),base::WeakPtr<cc::ProxyMain>,unsigned int,std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #65 0x7ffe820b45e9 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl cc::ProxyMain::*&&)(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &), class base::WeakPtr<class cc::ProxyMain> &&, unsigned int &&, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl cc::ProxyMain::*)(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &), class base::WeakPtr<class cc::ProxyMain>, unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #66 0x7ffe7ce169d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #67 0x7ffe7ce169d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34

previously allocated by thread T0 here:
    #0 0x7fff3e30a65d  (E:\chrome_asan\asan-win32-release_x64-1448748\clang_rt.asan_dynamic-x86_64.dll+0x18005a65d)
    #1 0x7ffe821073f4 in std::__Cr::__libcpp_operator_new C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__new\allocate.h:37
    #2 0x7ffe821073f4 in std::__Cr::__libcpp_allocate C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__new\allocate.h:64
    #3 0x7ffe821073f4 in std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > >::allocate C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\allocator.h:105
    #4 0x7ffe821073f4 in std::__Cr::__allocate_at_least C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__memory\allocate_at_least.h:41
    #5 0x7ffe821073f4 in std::__Cr::__split_buffer<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > &>::__split_buffer C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__split_buffer:325
    #6 0x7ffe821073f4 in std::__Cr::vector<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>, class std::__Cr::allocator<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>>>::emplace<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>>(class std::__Cr::__wrap_iter<struct std::__Cr::pair<unsigned int, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)>> const *>, unsigned int &&, class base::OnceCallback<(class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &)> &&) C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__vector\vector.h:1260:49
    #7 0x7ffe820f7902 in base::internal::flat_tree<unsigned int,base::internal::GetFirst,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > > >::unsafe_emplace C:\b\s\w\ir\cache\builder\src\base\containers\flat_tree.h:1103
    #8 0x7ffe820f7902 in base::flat_map<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)>,std::__Cr::less<void>,std::__Cr::vector<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >,std::__Cr::allocator<std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> > > > >::operator[] C:\b\s\w\ir\cache\builder\src\base\containers\flat_map.h:294
    #9 0x7ffe820f7902 in cc::LayerTreeHost::AddViewTransitionRequest(class std::__Cr::unique_ptr<class cc::ViewTransitionRequest, struct std::__Cr::default_delete<class cc::ViewTransitionRequest>>) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:975:5
    #10 0x7ffe8b6a36b4 in blink::PaintArtifactCompositor::Update(class blink::PaintArtifact const &, struct blink::PaintArtifactCompositor::ViewportProperties const &, class blink::HeapVector<class cppgc::internal::BasicMember<class blink::TransformPaintPropertyNode const, class cppgc::internal::StrongMemberTag, struct cppgc::internal::DijkstraWriteBarrierPolicy, class cppgc::internal::DisabledCheckingPolicy, class cppgc::internal::CompressedPointer>, 32> const &, class WTF::Vector<class std::__Cr::unique_ptr<class cc::ViewTransitionRequest, struct std::__Cr::default_delete<class cc::ViewTransitionRequest>>, 0, class WTF::PartitionAllocator>) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\graphics\compositing\paint_artifact_compositor.cc:980:11
    #11 0x7ffe899cc848 in blink::LocalFrameView::PushPaintArtifactToCompositor(bool) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3016:31
    #12 0x7ffe899c8877 in blink::LocalFrameView::RunPaintLifecyclePhase(enum blink::PaintBenchmarkMode) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2683:5
    #13 0x7ffe899c6e6b in blink::LocalFrameView::UpdateLifecyclePhasesInternal(enum blink::DocumentLifecycle::LifecycleState) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2378:3
    #14 0x7ffe899c29cf in blink::LocalFrameView::UpdateLifecyclePhases(enum blink::DocumentLifecycle::LifecycleState, enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2163:3
    #15 0x7ffe899c210e in blink::LocalFrameView::UpdateAllLifecyclePhases(enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:1887:54
    #16 0x7ffe878671f4 in blink::PageAnimator::UpdateAllLifecyclePhases(class blink::LocalFrame &, enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\page_animator.cc:397:9
    #17 0x7ffe8987caf5 in blink::WebFrameWidgetImpl::UpdateLifecycle(enum blink::WebLifecycleUpdate, enum blink::DocumentUpdateReason) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1764:14
    #18 0x7ffe8b359f6d in blink::WidgetBase::UpdateVisualState(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:1054:12
    #19 0x7ffe820ef283 in cc::LayerTreeHost::RequestMainFrameUpdate(bool) C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:402:12
    #20 0x7ffe820c0359 in cc::ProxyMain::BeginMainFrame(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>) C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:297:21
    #21 0x7ffe820b64be in base::internal::DecayedFunctorTraits<void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:731
    #22 0x7ffe820b64be in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:947
    #23 0x7ffe820b64be in base::internal::Invoker<base::internal::FunctorTraits<void (ProxyMain::*&&)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain> &&,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > &&>,base::internal::BindState<1,1,0,void (ProxyMain::*)(std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::__Cr::unique_ptr<cc::BeginMainFrameAndCommitState,std::__Cr::default_delete<cc::BeginMainFrameAndCommitState> > >,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1060
    #24 0x7ffe820b64be in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl cc::ProxyMain::*&&)(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>), class base::WeakPtr<class cc::ProxyMain> &&, class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>> &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl cc::ProxyMain::*)(class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>), class base::WeakPtr<class cc::ProxyMain>, class std::__Cr::unique_ptr<struct cc::BeginMainFrameAndCommitState, struct std::__Cr::default_delete<struct cc::BeginMainFrameAndCommitState>>>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:973:12
    #25 0x7ffe7ce169d3 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #26 0x7ffe7ce169d3 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:209:34
    #27 0x7ffe7cde9a29 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #28 0x7ffe7cde9a29 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456:23
    #29 0x7ffe7cde88cf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #30 0x7ffe7cf49427 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #31 0x7ffe7cdeb751 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629:12
    #32 0x7ffe7ce8643e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #33 0x7ffe9278f8fb in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:369:16
    #34 0x7ffe79901686 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:781:14
    #35 0x7ffe799039d1 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1155:10
    #36 0x7ffe798f7ab3 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:359:36
    #37 0x7ffe798f866d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372:10
    #38 0x7ffe6a1116bb in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #39 0x7ff6e68147bb in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #40 0x7ff6e6812021 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #41 0x7ff6e6cc55fb in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #42 0x7ff6e6cc55fb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #43 0x7fff890ae8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #44 0x7fff8b1dbf6b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800bbf6b)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__utility\pair.h:236 in std::__Cr::pair<unsigned int,base::OnceCallback<void (const std::__Cr::unordered_map<viz::ViewTransitionElementResourceId,gfx::RectF,std::__Cr::hash<viz::ViewTransitionElementResourceId>,std::__Cr::equal_to<viz::ViewTransitionElementResourceId>,std::__Cr::allocator<std::__Cr::pair<const viz::ViewTransitionElementResourceId,gfx::RectF> > > &)> >::operator=
Shadow bytes around the buggy address:
  0x11b78c231b80: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
  0x11b78c231c00: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa
  0x11b78c231c80: fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd fd fd
  0x11b78c231d00: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
  0x11b78c231d80: fd fd f7 fa fd fd fd fd f7 fa 00 00 00 fa f7 fa
=>0x11b78c231e00: 00 00 00 fa f7 fa 00 00 00 00 f7 fa fd fd[fd]fd
  0x11b78c231e80: f7 fa fd fd fd fa f7 fa fd fd fd fd f7 fa fd fd
  0x11b78c231f00: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa
  0x11b78c231f80: 00 00 00 00 f7 fa fd fd fd fd f7 fa fd fd fd fd
  0x11b78c232000: f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa fd fd
  0x11b78c232080: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fd f7 fa
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

==16784==ADDITIONAL INFO

==16784==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffe820ac7c7 in cc::ProxyImpl::NotifyTransitionRequestFinished(unsigned int, class std::__Cr::unordered_map<class viz::ViewTransitionElementResourceId, class gfx::RectF, struct std::__Cr::hash<class viz::ViewTransitionElementResourceId>, struct std::__Cr::equal_to<class viz::ViewTransitionElementResourceId>, class std::__Cr::allocator<struct std::__Cr::pair<class viz::ViewTransitionElementResourceId const, class gfx::RectF>>> const &) C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_impl.cc:643:7
    #1 0x7ffe7d330a58 in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:102:13



MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==16784==END OF ADDITIONAL INFO
==16784==ABORTINGs

```

CREDIT INFORMATION
Reporter credit: [f4@dnpushme]

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 60.1 KB)
- deleted (application/octet-stream, 0 B)
- [fixpatch.diff](attachments/fixpatch.diff) (text/x-diff, 526 B)
- [simple_poc.html](attachments/simple_poc.html) (text/html, 1.9 KB)
- [writeup_en.md](attachments/writeup_en.md) (text/markdown, 17.2 KB)
- [exp.html](attachments/exp.html) (text/html, 4.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### m....@gmail.com (2025-04-18)

My bad,I didn't enclose the ASAN log in ```, but I can't edit the message anymore. Mind fixing that for me?

### m....@gmail.com (2025-04-18)

# Bisect

The vulnerability pattern was introduced by this CL.  

<https://chromium-review.googlesource.com/c/chromium/src/+/2716603>

### an...@chromium.org (2025-04-18)

[security shepherd]: Thank you for the report and the POC + asan text. I fixed the description. Assigning to @vm...@chromium.org to investigate the UAF. 

### an...@chromium.org (2025-04-18)

[security shepherd]: To add another note for reporter and the assignee, I am unable to reproduce the issue exactly. The print popup does occur despite the flag, and I am unable to trigger this when pressing the escape key. I will mark this as need more feedback for now but it is assigned to the developer who made this change for any further analysis. The Found-In was set to 91 to mark the milestone the change listed has landed under [comment #3](https://issues.chromium.org/issues/411573532#comment3)

### ch...@google.com (2025-04-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### m....@gmail.com (2025-04-19)

re #c5  

I apologize for the previous description causing confusion.  

If you use --headless to reproduce, no action is needed.  

If you don't, then click the cancel button in the print window (you may need to click multiple times) to reproduce.

### m....@gmail.com (2025-04-21)

reprodeuce video

### th...@chromium.org (2025-04-25)

[secondary shepherd] Adding vasilyt@ + kylechar@ to cc since they reviewed the suspect culprit CL mentioned in #comment3.

### m....@gmail.com (2025-04-28)

**Here is my fix suggestion:**  

deletion the iterator deletion before executing the callback.

```
diff --git a/cc/trees/layer_tree_host.cc b/cc/trees/layer_tree_host.cc
index d133392a5302a..6fd0a8f20f9fc 100644
--- a/cc/trees/layer_tree_host.cc
+++ b/cc/trees/layer_tree_host.cc
@@ -535,8 +535,9 @@ void LayerTreeHost::NotifyTransitionRequestsFinished(
   if (it == view_transition_callbacks_.end()) {
     return;
   }
-  std::move(it->second).Run(rects);
+  auto callback = std::move(it->second);
   view_transition_callbacks_.erase(it);
+  std::move(callback).Run(rects);
 }
 
 void LayerTreeHost::SetLayerTreeFrameSink(


```

### m....@gmail.com (2025-04-28)

Here is a clearer PoC: the print pop-up will trigger the vulnerability no matter what you click.

`chrome --no-first-run --no-sandbox --user-data-dir=test C:\Users\12700k\Documents\250410\simple_poc.html`

### va...@chromium.org (2025-04-28)

It's a bit tricky, callback from viz OnCompositorFrameTransitionDirectiveProcessed triggers to js callback, which in turn triggers printing, that starts nested run loop [here](https://source.chromium.org/chromium/chromium/src/+/main:components/printing/renderer/print_render_frame_helper.cc;drc=73bcf25e4b0c06b1a86422a2fc30023c7b850f33;l=2694). That runloop starts next compositing update and that update adds new callback to `view_transition_callbacks_` resulting in reallocation.

Fix in [#comment11](https://issues.chromium.org/issues/411573532#comment11) would avoid UaF problem, but I'm not sure there is no bigger problem to start next frame from nested runloop, maybe we should dispatch js callbacks as a separate PostTask, not sure what spec says about when callback supposed to run.

### m....@gmail.com (2025-04-30)

Here is an exploitable demonstration.  

**Repro step**  

`chrome --js-flags="-expose-gc" --no-sandbox --user-data-dir=test --enable-logging=stderr exp.html`

**NOTE**  

The print window triggered by this vulnerability does not affect the exploit regardless of the user's choice, making it effectively equivalent to requiring no user interaction.

### ch...@google.com (2025-05-03)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-04)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-05)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-06)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-05-07)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### m....@gmail.com (2025-05-08)

@ping anyone worked on this issue?

### ch...@google.com (2025-05-08)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@chromium.org (2025-05-12)

Adding more animation owners for visibility. Not reassigning as this seems to be assigned to the correct owner based on bisect.

vmpstr@ and vasilyt@ can you PTAL at this issue since it's a renderer UAF that affects Stable channel for some time and is fairly easy to trigger with updated information for a more reliable repro without user interaction

### vm...@chromium.org (2025-05-13)

Sorry, this slipped my radar, I'm going to investigate

### dx...@google.com (2025-05-14)

Project: chromium/src  

Branch: main  

Author: Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6542846>

vt/cc: Post a callback task instead of a synchronous call

---


Expand for full commit details
```
     
    The callback can end up calling more script to start view transitions 
    which can add more requests, and re-enter into modifying the vector. 
     
    So, instead, unwind the task to post the task. 
     
    R=khushalsagar@chromium.org 
     
    Bug: 411573532 
    Change-Id: I80880e9e3ecf41c346910fb5cb6f44609ee5ef17 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6542846 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Khushal Sagar <khushalsagar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1460048}

```

---

Files:

- M `cc/trees/layer_tree_host.cc`

---

Hash: 02ddca5de087c833fede8c46fb971acdc42a7e91  

Date:  Wed May 14 13:52:57 2025


---

### ch...@google.com (2025-05-15)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pg...@google.com (2025-05-20)

6 days worth of reports in dev and canaries look good where applicable - i do not see any relevant crashes as far as I can tell - merge approved!

Please merge to branch 7151 asap to get this change into the next M137 stable release!\ 

please hold a bit longer for the M136 merge - this week is a bit funky of a schedule (:


### pg...@google.com (2025-05-20)

chatted with vmpstr@ off-bug and learned these paths originally impacted clank as well so updating OS to include Android. \
(happy to correct if the paths diverged at some point and this actually does not impact Android)

### dx...@google.com (2025-05-20)

Project: chromium/src  

Branch: refs/branch-heads/7151  

Author: Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6570729>

vt/cc: Post a callback task instead of a synchronous call

---


Expand for full commit details
```
     
    The callback can end up calling more script to start view transitions 
    which can add more requests, and re-enter into modifying the vector. 
     
    So, instead, unwind the task to post the task. 
     
    R=khushalsagar@chromium.org 
     
    (cherry picked from commit 02ddca5de087c833fede8c46fb971acdc42a7e91) 
     
    Bug: 411573532 
    Change-Id: I80880e9e3ecf41c346910fb5cb6f44609ee5ef17 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6542846 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Khushal Sagar <khushalsagar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1460048} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6570729 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7151@{#1428} 
    Cr-Branched-From: 8e0d32ed6e49a2415b16e5ed402957cac2349ce2-refs/heads/main@{#1453031}

```

---

Files:

- M `cc/trees/layer_tree_host.cc`

---

Hash: 84781974514aed5a20568f597bab8b98907ecbb1  

Date:  Tue May 20 22:14:25 2025


---

### pe...@google.com (2025-05-20)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pg...@google.com (2025-05-21)

thanks for your patience! canary and dev still arent showing anything relevant, and the fix was successfully merged to the M137 release.

merge approved for M136 - please merge to branch 7103 by EOD MTV time Thursday May 22 to get this safely into M136 extended stable respin!\

### sp...@google.com (2025-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high-quality report demonstrating memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-05-22)

Thank you for the report. I wanted to let you know in advance that we did review the write-up and POC provided in c#14 in our assessment. We did not consider this eligible for a higher reward for a couple of reasons:

- This issue is in the renderer and is mildly mitigated by very light user standard interactions that a user would be likely to choose, in terms of exiting out the dialog, therefore based on the quality of this report and this issue as a standalone, we allocated the full high-quality memory corruption reward rather than a reward amount in line with a mitigated bug in a sandboxed process.
- Reviewing all the data provided and available, it looks like CFG is hit here. If you can provide a POC or other info showing a call / where attacker control of the write value can be demonstrated, we are happy to assess this for a higher reward.

Based on the information provided and how this bug is demonstrated, this does not look like a highly, remote exploitable issue that would provide a much attacker control or value to result in user harm. As mentioned, we are happy to revisit if a strong demonstration can be provide that proves this isn't also mitigated by CFG.

### m....@gmail.com (2025-05-22)

> Reviewing all the data provided and available, it looks like CFG is hit here. If you can provide a POC or other info showing a call / where attacker control of the write value can be demonstrated, we are happy to assess this for a higher reward

Thank you for providing detailed decision-making information, but I have a few questions:

1. The PoC I provided already achieves RIP control, but `mov rax,0x616161616161616,call rax_with_cfg_check` triggers CFG checks on Windows. In actual exploitation, it seems sufficient to provide a valid target address through information leakage.
2. Taking the same issue as an example, `https://issues.chromium.org/issues/379516109#comment15`, the exploit in this case also achieves RIP control, but on macOS with Silicon processors, there is PAC to prevent unsigned pointer code execution, similar to CFG on Windows. Is it also necessary to provide a PAC bypass on mac?

### pe...@google.com (2025-05-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### m....@gmail.com (2025-05-22)

Update an error in the content of C#34: Chrome cannot enable PAC on Mac.

### m....@gmail.com (2025-05-22)

As mentioned earlier, on Mac, RIP can be directly controlled to any value.  

I have uploaded the DMP file to the Chromium backend with the ID `20d58bdd-4498-4031-bd5b-98e855f1551e.dmp`.

```
Crash from Thursday, May 22, 2025 at 6:18:05 PM
Status:	Not yet uploaded, or ignored
Local Crash Context:	20d58bdd-4498-4031-bd5b-98e855f1551e

```

`minidump_stackwalk 20d58bdd-4498-4031-bd5b-98e855f1551e.dmp`

```
Operating system: Mac OS X
                  15.5.0 24F74
CPU: arm64
     10 CPUs

GPU: UNKNOWN

Crash reason:  EXC_BAD_ACCESS / KERN_INVALID_ADDRESS
Crash address: 0x5555555544444444
Process uptime: 6 seconds

Thread 0 (crashed)
 0  0x5555555544444444
     x0 = 0x0000287c000c3900    x1 = 0x0000010419b7cdc8
     x2 = 0x000001040f4465e0    x3 = 0x0000000000000000
     x4 = 0x0000000000000000    x5 = 0x0000000000000001
     x6 = 0x0000287800db5d55    x7 = 0x0000000000000011
     x8 = 0x5555555544444444    x9 = 0x0000287c000c3900
    x10 = 0x0000010400000000   x11 = 0x0000010000000000
    x12 = 0x0000000000000000   x13 = 0x0000000000000000
    x14 = 0xffc9ffffffffffff   x15 = 0x00000000656c6966
    x16 = 0x000000018c739bf0   x17 = 0x0000000177f30220
    x18 = 0x0000000000000000   x19 = 0x0000010419b7cdb8
    x20 = 0x0000010400444db0   x21 = 0x0000010426dac310
    x22 = 0x0000010419b7cdc0   x23 = 0x0000010419b7cdb0
    x24 = 0xaaaaaaaaaaaaaa00   x25 = 0x0000000000000092
    x26 = 0x0000000000000001   x27 = 0x00000104000cf000
    x28 = 0x000000011d23ac90    fp = 0x000000016b321c00
     lr = 0x0000000116041b30    sp = 0x000000016b321be0
     pc = 0x5555555544444444
    Found by: given as instruction pointer in context

```

### m....@gmail.com (2025-05-22)

The DMP file doesn't seem to have uploaded successfully. I've included it in the attachment, and I will delete it before the issue is made public.

### qk...@google.com (2025-05-22)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6575520
2. Low - There was no conflict.
3. 137
4. Yes. According to comment #3, this issue has existed since Feb. 2021. Thus, it's likely we need to merge the CL to M132.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2716603

### gm...@google.com (2025-05-29)

Delaying the approval to LTS-132 until 137 ChromeOS goes to stable.
This was not cherry picked to M136.

### sp...@google.com (2025-06-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $39000.00 for this report.

Rationale for this decision:
Additional $39,000 to bring the total reward to $50,000 for demonstrating a controlled write in a sandboxed process / the renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-12)

Congratulations! Thank you for the additional information. We agree that the combined information in this report meets the criteria for demonstration of a controlled write in the renderer. Thank you again for your efforts and reporting this issue to us -- great work!

### dx...@google.com (2025-06-17)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6575520>

[M132-LTS] vt/cc: Post a callback task instead of a synchronous call

---


Expand for full commit details
```
     
    The callback can end up calling more script to start view transitions 
    which can add more requests, and re-enter into modifying the vector. 
     
    So, instead, unwind the task to post the task. 
     
    R=khushalsagar@chromium.org 
     
    (cherry picked from commit 02ddca5de087c833fede8c46fb971acdc42a7e91) 
     
    Bug: 411573532 
    Change-Id: I80880e9e3ecf41c346910fb5cb6f44609ee5ef17 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6542846 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Khushal Sagar <khushalsagar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1460048} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6575520 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Auto-Submit: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5583} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `cc/trees/layer_tree_host.cc`

---

Hash: fd5e650a103f29fae481f72ab5b562ac4e46466d  

Date:  Tue Jun 17 16:48:48 2025


---

### ch...@google.com (2025-08-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $10,000 for high-quality report demonstrating memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/411573532)*
