# heap-buffer-overflow in apps::AppShimManager::OnShimLaunchRequested

| Field | Value |
|-------|-------|
| **Issue ID** | [350869463](https://issues.chromium.org/issues/350869463) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2024-07-03 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

`OnShimLaunchRequested` in `[0]` dont' check the `apps_` bound,because it use DCHECK,so out of bound occur in `[1]`.

```
void AppShimManager::OnShimLaunchRequested(
    AppShimHost* host,
    web_app::LaunchShimUpdateBehavior update_behavior,
    web_app::ShimLaunchMode launch_mode,
    apps::ShimLaunchedCallback launched_callback,
    apps::ShimTerminatedCallback terminated_callback) {
  // A shim can only be launched through an active profile, so find a profile
  // through which to do the launch. For multi-profile apps, select one
  // arbitrarily. For non-multi-profile apps, select the specified profile.
  Profile* profile = nullptr;
  {
    auto found_app = apps_.find(host->GetAppId());
    DCHECK(found_app != apps_.end());                 // [0]
    AppState* app_state = found_app->second.get();    // [1]
    if (app_state->IsMultiProfile()) {
      DCHECK(!app_state->profiles.empty());
      profile = app_state->profiles.begin()->first;
    } else {
      profile = ProfileForPath(host->GetProfilePath());
    }
  }

  // If `update_behavior` was set to possible recreate shims, it can happen that
  // the app got uninstalled while an initial launch attempt took place (and
  // failed). So check first if the app is still installed.
  // TODO(mek): Rather than this workaround, we should make sure to destroy
  // AppShimHost and terminate app shims when an app is uninstalled.
  if (web_app::RecreateShimsRequested(update_behavior) &&
      (!delegate_->AppIsInstalled(profile, host->GetAppId()) ||
       !AppShimRegistry::Get()->IsAppInstalledInProfile(host->GetAppId(),
                                                        profile->GetPath()))) {
    LOG(ERROR)
        << "Attempting to launch shim for an app that is no longer installed.";
    std::move(terminated_callback).Run();
    return;
  }

  delegate_->LaunchShim(profile, host->GetAppId(), update_behavior, launch_mode,
                        std::move(launched_callback),
                        std::move(terminated_callback));
}

```
```
=================================================================
==65603==ERROR: AddressSanitizer: qon address 0x60600090b8e8 at pc 0x00011c228880 bp 0x00016ee6ce50 sp 0x00016ee6ce48
READ of size 8 at 0x60600090b8e8 thread T0
==65603==WARNING: invalid path to external symbolizer!
==65603==WARNING: Failed to use and restart external symbolizer!
    #0 0x11c22887c in apps::AppShimManager::OnShimLaunchRequested(AppShimHost*, web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode, base::OnceCallback<void (base::Process)>, base::OnceCallback<void ()>)+0x7d8 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x25a087c)
    #1 0x11c21d71c in AppShimHost::LaunchShimInternal(web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode)+0x3f4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x259571c)
    #2 0x11c21dac4 in AppShimHost::OnShimProcessTerminated(web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode)+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2595ac4)
    #3 0x11c21f914 in void base::internal::Invoker<base::internal::FunctorTraits<void (AppShimHost::*&&)(web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode), base::WeakPtr<AppShimHost>&&, web_app::LaunchShimUpdateBehavior&&, web_app::ShimLaunchMode&&>, base::internal::BindState<true, true, false, void (AppShimHost::*)(web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode), base::WeakPtr<AppShimHost>, web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode>, void ()>::RunImpl<void (AppShimHost::*)(web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode), std::__Cr::tuple<base::WeakPtr<AppShimHost>, web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode>, 0ul, 1ul, 2ul>(void (AppShimHost::*&&)(web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode), std::__Cr::tuple<base::WeakPtr<AppShimHost>, web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)+0x1a0 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2597914)
    #4 0x11baea988 in base::OnceCallback<void ()>::Run() &&+0x134 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x1e62988)
    #5 0x11bc9d834 in -[AppShimTerminationObserver onTerminated]+0x34 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2015834)
    #6 0x11bc9da48 in base::internal::Invoker<base::internal::FunctorTraits<void () block_pointer __strong&&>, base::internal::BindState<false, true, false, void () block_pointer __strong&&>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2015a48)
    #7 0x1037e8930 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1bc930)
    #8 0x1038585a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xacc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x22c5a4)
    #9 0x103857610 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x22b610)
    #10 0x1039bb288 in base::MessagePumpCFRunLoopBase::RunWork()+0x1cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x38f288)
    #11 0x1039a81f8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x37c1f8)
    #12 0x1039b9768 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x38d768)
    #13 0x19ecca4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #14 0xd40480019ecca468  (<unknown module>)
    #15 0x7b3d00019ecca1d8  (<unknown module>)
    #16 0x3c0e00019ecc8dc4  (<unknown module>)
    #17 0xe02a00019ecc8430  (<unknown module>)
    #18 0x8d000001a946c198  (<unknown module>)
    #19 0x422c0001a946bfd4  (<unknown module>)
    #20 0xa4288001a946bd2c  (<unknown module>)
    #21 0x9c318001a2527d64  (<unknown module>)
    #22 0x3d608001a2d1d804  (<unknown module>)
    #23 0x860f00011cf37a3c  (<unknown module>)
    #24 0x1039a81f8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x37c1f8)
    #25 0x11cf376f4 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x32af6f4)
    #26 0x1a251b098 in -[NSApplication run]+0x1d8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2d098)
    #27 0xb6008001039bd4b0  (<unknown module>)
    #28 0x1039b7fdc in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x2b0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x38bfdc)
    #29 0x103859b94 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x22db94)
    #30 0x10376c754 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x140754)
    #31 0x10f48cfc8 in content::BrowserMainLoop::RunMainMessageLoop()+0x188 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xdf4fc8)
    #32 0x10f493468 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xdfb468)
    #33 0x10f485728 in content::BrowserMain(content::MainFunctionParams)+0x1f8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xded728)
    #34 0x111b0e2b0 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x1a8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x34762b0)
    #35 0x111b10f98 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x8e8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3478f98)
    #36 0x111b103a0 in content::ContentMainRunnerImpl::Run()+0x4b8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x34783a0)
    #37 0x111b0c470 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x474 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3474470)
    #38 0x111b0cdd0 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3474dd0)
    #39 0x119c93044 in ChromeMain+0x380 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0xb044)
    #40 0x100f90b94 in main+0x20c (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000b94)
    #41 0x19e8620dc  (<unknown module>)
    #42 0x1f087ffffffffffc  (<unknown module>)

0x60600090b8e8 is located 8 bytes after 64-byte region [0x60600090b8a0,0x60600090b8e0)
allocated by thread T0 here:
    #0 0x101bb80f8 in __sanitizer_finish_switch_fiber+0x61c (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x600f8)
    #1 0x11c226970 in apps::AppShimManager::GetOrCreateProfileState(Profile*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)+0x238 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x259e970)
    #2 0x11c225588 in apps::AppShimManager::LaunchShimInBackgroundMode(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::OnceCallback<void (AppShimHost*)>)+0x1bc (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x259d588)
    #3 0x11c226174 in apps::AppShimManager::ShowNotificationPermissionRequest(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::OnceCallback<void (mac_notifications::mojom::RequestPermissionResult)>)+0x5bc (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x259e174)
    #4 0x1231aab14 in PermissionPromptNotificationsMac::ShowPrompt()+0x208 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x9522b14)
    #5 0x1231ab698 in void base::internal::Invoker<base::internal::FunctorTraits<void (PermissionPromptNotificationsMac::*&&)(), base::WeakPtr<PermissionPromptNotificationsMac>&&>, base::internal::BindState<true, true, false, void (PermissionPromptNotificationsMac::*)(), base::WeakPtr<PermissionPromptNotificationsMac>>, void ()>::RunImpl<void (PermissionPromptNotificationsMac::*)(), std::__Cr::tuple<base::WeakPtr<PermissionPromptNotificationsMac>>, 0ul>(void (PermissionPromptNotificationsMac::*&&)(), std::__Cr::tuple<base::WeakPtr<PermissionPromptNotificationsMac>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)+0x178 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x9523698)
    #6 0x1037e8930 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1bc930)
    #7 0x1038585a4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0xacc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x22c5a4)
    #8 0x103857610 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x22b610)
    #9 0x1039bb288 in base::MessagePumpCFRunLoopBase::RunWork()+0x1cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x38f288)
    #10 0x1039a81f8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x37c1f8)
    #11 0x1039b9768 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x38d768)
    #12 0x19ecca4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #13 0xd40480019ecca468  (<unknown module>)
    #14 0x7b3d00019ecca1d8  (<unknown module>)
    #15 0x3c0e00019ecc8dc4  (<unknown module>)
    #16 0xe02a00019ecc8430  (<unknown module>)
    #17 0x8d000001a946c198  (<unknown module>)
    #18 0x422c0001a946bfd4  (<unknown module>)
    #19 0xa4288001a946bd2c  (<unknown module>)
    #20 0x9c318001a2527d64  (<unknown module>)
    #21 0x3d608001a2d1d804  (<unknown module>)
    #22 0x860f00011cf37a3c  (<unknown module>)
    #23 0x1039a81f8 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x37c1f8)
    #24 0x11cf376f4 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x32af6f4)
    #25 0x1a251b098 in -[NSApplication run]+0x1d8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2d098)
    #26 0xb6008001039bd4b0  (<unknown module>)
    #27 0x1039b7fdc in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x2b0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x38bfdc)
    #28 0x103859b94 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x32c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x22db94)
    #29 0x10376c754 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x140754)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x25a087c) in apps::AppShimManager::OnShimLaunchRequested(AppShimHost*, web_app::LaunchShimUpdateBehavior, web_app::ShimLaunchMode, base::OnceCallback<void (base::Process)>, base::OnceCallback<void ()>)+0x7d8
Shadow bytes around the buggy address:
  0x60600090b600: 00 00 00 00 00 00 00 00 fa fa f7 fa 00 00 00 00
  0x60600090b680: 00 00 00 fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x60600090b700: fa fa f7 fa 00 00 00 00 00 00 00 00 fa fa f7 fa
  0x60600090b780: fd fd fd fd fd fd fd fd fa fa f7 fa 00 00 00 00
  0x60600090b800: 00 00 00 fa fa fa f7 fa 00 00 00 00 00 00 00 00
=>0x60600090b880: fa fa f7 fa 00 00 00 00 00 00 00 00 fa[fa]f7 fa
  0x60600090b900: 00 00 00 00 00 00 00 00 fa fa f7 fa fd fd fd fd
  0x60600090b980: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x60600090ba00: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa
  0x60600090ba80: 00 00 00 00 00 00 00 fa fa fa f7 fa 00 00 00 00
  0x60600090bb00: 00 00 00 00 fa fa f7 fa 00 00 00 00 00 00 00 fa
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

==65603==ADDITIONAL INFO

==65603==Note: Please include this section with the ASan report.
Task trace:
    #0 0x11bc9d458 in -[AppShimTerminationObserver observeValueForKeyPath:ofObject:change:context:]+0x19c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2015458)


Command line: `out/Default/Chromium.app/Contents/MacOS/Chromium --enable-features=AppShimNotificationAttribution --user-data-dir=/Users/test/tmp --flag-switches-begin --flag-switches-end http://127.0.0.1:8000/`


==65603==END OF ADDITIONAL INFO
==65603==ABORTING


```

VERSION
Chrome Version: 128.0.6565.0 + [stable, beta, or dev]
Operating System: Macos

REPRODUCTION CASE
see [Issue 348793134](https://issues.chromium.org/issues/348793134),same steps.

FIX

- DCHECK(found\_app != apps\_.end());

- CHECK(found\_app != apps\_.end());

Bisect

<https://chromium-review.googlesource.com/c/chromium/src/+/1787589>

## Timeline

### ha...@gmail.com (2024-07-03)

bisect

<https://chromium-review.googlesource.com/c/chromium/src/+/1894067>

Many of them use the DCHECK function, which is problematic.

### da...@chromium.org (2024-07-03)

Thanks for the report.

We now explicitly request that checks like these are written as CHECK, not DCHECK, because of issues like this:

- <https://source.chromium.org/chromium/chromium/src/+/main:docs/security/checklist.md;l=46-48;drc=3f6d6b6eb259f44ccfea823f9a75cbea8cb29c4e>
- <https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/checks.md>

### da...@chromium.org (2024-07-03)

From the stack trace, the memory corruption is happening during process shutdown. That should be sufficient to mitigate this from being S0 down to S1.

### da...@chromium.org (2024-07-03)

The code in question is 5 years old, marking found in 126 tentatively unless we learn otherwise.

### me...@chromium.org (2024-07-03)

I think the analysis that it's the apps\_ lookup that is failing is incorrect (if the app didn't exist in apps\_, it would have crashed much earlier, as the AppShimHost higher up the stack is owned by apps\_). But this does seem the same as [issue 348793134](https://issues.chromium.org/issues/348793134), in that this is probably also the `DCHECK(!app_state->profiles.empty());` that is failing like in that bug (I thought I looked for other places of the same pattern when fixing that bug, but I guess I overlooked this one...)

### me...@chromium.org (2024-07-03)

(and like the other bug, this bug would also be specific to the not-yet-launched AppShimNotificationAttribution feature)

### ap...@google.com (2024-07-03)

Project: chromium/src
Branch: main

commit e4cb16bc3259cc66d560583a3c5d01fd69f12dcc
Author: Marijn Kruisselbrink <mek@chromium.org>
Date:   Wed Jul 03 18:50:48 2024

    Fix another bad !profiles.empty() assumption in AppShimManager.
    
    Bug: 350869463
    Change-Id: Ic00646e827ca241cf69261a590c95b1bced500b0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5676925
    Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
    Reviewed-by: Dibyajyoti Pal <dibyapal@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1322930}

M       chrome/browser/apps/app_shim/app_shim_manager_mac.cc
M       chrome/browser/apps/app_shim/app_shim_manager_mac_unittest.cc

https://chromium-review.googlesource.com/5676925


### pe...@google.com (2024-07-04)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-04)

Requesting merge to stable (M126) because latest trunk commit (1322930) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1322930) appears to be after beta branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### me...@chromium.org (2024-07-04)

FWIW I don't think it makes sense to merge this fix but not the fix for [bug 348793134](https://issues.chromium.org/issues/348793134), as in addition to everything that needs to happen to trigger that bug for this bug the app shim itself also needs to fail to launch (which in ASAN builds can happen for a variety of reasons, but really should be super rare/not happen in the wild).

### da...@google.com (2024-07-05)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-07-08)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pg...@google.com (2024-07-09)

Updating impact to None as AppShimNotificationAttribution is off by default and removing merge labels - thanks for pointing this out, mek@!

### sp...@google.com (2024-07-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1,000 for report of highly mitigated memory corruption in a non-sandboxed process -- mitigated by shutdown, difficult of attacker to trigger and control based on timing and triggering shutdown in conjunction with logging + $1,000 bisect bonus 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Congratulations and thank you for your efforts in finding and reporting this issue to us. While we welcome future reporting, when submitting a patch as part of the reproduction to trigger the issue, we would appreciate it if you can include the purpose for the patch and a reasonable explanation / analysis of how the issue could be exploited outside of the context and use of the patch. [ref: https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#report-attachments]

### pe...@google.com (2024-10-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/350869463)*
