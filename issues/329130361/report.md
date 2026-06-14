# use-after-poison on blink::MIDIDispatcher::SessionStarted

| Field | Value |
|-------|-------|
| **Issue ID** | [329130361](https://issues.chromium.org/issues/329130361) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebMIDI |
| **Platforms** | Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-03-12 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
use-after-poison on blink::MIDIDispatcher::SessionStarted

VERSION
Chrome Version: I tested in chromium head: ea5c6cdc94d3ca4ab0fc7f5207df5edc30609e6a
Operating System: I tested in Windows

REPRODUCTION CASE
This may be a competition issue that I can't reproduce reliably. I will keep on attempting.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: see asan log

CREDIT INFORMATION
Reporter credit: Kiprey

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 6.1 KB)
- [EXECUTION_LOG.txt](attachments/EXECUTION_LOG.txt) (text/plain, 72.1 KB)

## Timeline

### ja...@chromium.org (2024-03-12)

Hello, thank you for the log file and for the bug report. Can you provide us with a proof of concept that we can try? Individual files uploaded as attachments is the preferred format.

<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/vrp-faq.md#proof-of-concept-poc>

Passing this back to the bug reporter for more information.

### ki...@gmail.com (2024-03-13)

This is a race condition vulnerability that cannot be reproduced by saved POC, please analyze the asan log directly.

### pe...@google.com (2024-03-13)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-03-13)

The NextAction date has arrived: 2024-03-13 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ki...@gmail.com (2024-03-14)

Based on my fuzzing cycle, I speculate that this commit is where the vulnerability was introduced. Please take a look. 

https://chromium.googlesource.com/chromium/src/+/44aadf5b9c2db38d3c9b8d08f8bcbb30de14c007

```
commit 44aadf5b9c2db38d3c9b8d08f8bcbb30de14c007
Author: Michael Wilson <mjwilson@chromium.org>
Date:   Fri Mar 8 19:43:49 2024 +0000

    Block or allow all MIDI using the existing SysEx permission

    We have changed our approach for gating all MIDI access behind a
    permission prompt.  Now, the existing SysEx permission and prompt will
    be used to control all access to the Web MIDI API.

    This CL does the following:
    - Roll back registration of the basic MIDI content setting and
      request type
    - Move the feature flag location from content/public/common to
      thrid_party/blink/public/common, since the feature is no longer
      related to content
    - Update test_driver tests (including WPTs) to request the
      permission with the SysEx flag set to true
    - Always show the SysEx version of the prompt by modifying
      midi_access_initializer.cc

    Note that one external WPT is also being updated.  Although other
    browsers may not need the sysex flag set to true for the idlharness
    tests to pass, setting it to true should not cause the tests to fail
    since it is stronger than the basic midi permission as per spec:
    https://webaudio.github.io/web-midi-api/#permissions-integration

    Bug: 1420307
    Change-Id: I5a6c45641c440f34bfdba0fb2076ae030528c634
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5154368
    Reviewed-by: Ravjit Uppal <ravjit@chromium.org>
    Reviewed-by: Nate Fischer <ntfschr@chromium.org>
    Reviewed-by: Sina Firoozabadi <sinafirooz@chromium.org>
    Commit-Queue: Michael Wilson <mjwilson@chromium.org>
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Charlie Reis <creis@chromium.org>
    Reviewed-by: Colin Blundell <blundell@chromium.org>
    Reviewed-by: Kentaro Hara <haraken@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1270342}
```

### ja...@chromium.org (2024-03-14)

This CL seems to have landed into M124. Setting that as found in. And adding Blink>WebMIDI as the component.

### ja...@chromium.org (2024-03-14)

Hi mjwilson@, we have a stack trace on this bug, but not a proof of concept yet. Can you take a look?

### mj...@chromium.org (2024-03-14)

Taking a look now.

### ja...@chromium.org (2024-03-14)

Provisionally setting severity to Medium because it seems like a read can happen.

<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-medium-severity>

### mj...@chromium.org (2024-03-14)

Also note that this change should be completely guarded behind the flag kBlockMidiByDefault which is currently disabled by default, so it shouldn't be able to affect production.

Is it possible for the submitter to verify if this reproduces with the flag disabled?

### ki...@gmail.com (2024-03-14)

I noticed I didn't enable this feature manually. Could you please check if  `--enable-blink-test-features --enable-experimental-web-platform-features` have been turned on?

Additionally, I'm not entirely sure if this commit introduced the vulnerability, but luckily, it seems that on macOS, this vulnerability can occasionally be reproduced. Here is the ASan log on macOS; I'll try to take a look.

```
=================================================================
[1m[31m==8698==ERROR: AddressSanitizer: use-after-poison on address 0x7ea300451d18 at pc 0x000174fcdfb4 bp 0x00016ae655d0 sp 0x00016ae655c8
[1m[0m[1m[34mREAD of size 8 at 0x7ea300451d18 thread T0[1m[0m
==8698==WARNING: invalid path to external symbolizer!
==8698==WARNING: Failed to use and restart external symbolizer!
    #0 0x174fcdfb0 in blink::MIDIDispatcher::SessionStarted(midi::mojom::Result)+0x5ec (/Users/test/xcode-chromium/src/out/asan-0314/libblink_modules.dylib:arm64+0x2c01fb0)
    #1 0x17585bd80 in midi::mojom::blink::MidiSessionClientStubDispatch::Accept(midi::mojom::blink::MidiSessionClient*, mojo::Message*)+0x3d0 (/Users/test/xcode-chromium/src/out/asan-0314/libblink_modules.dylib:arm64+0x348fd80)
    #2 0x105b5fc50 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x7c0 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x23c50)
    #3 0x105b73b2c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x348 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x37b2c)
    #4 0x105b63f94 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x27f94)
    #5 0x105b7f4a4 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x684 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x434a4)
    #6 0x105b7dc50 in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x534 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x41c50)
    #7 0x105b73b2c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x348 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x37b2c)
    #8 0x105b4cfb8 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x378 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x10fb8)
    #9 0x105b4e918 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x12918)
    #10 0x105b4e3f0 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x123f0)
    #11 0x105b50608 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::RunImpl<void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, 0ul, 1ul>(void (mojo::Connector::* const&)(char const*, unsigned int), std::__Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>> const&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, unsigned int&&)+0x208 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x14608)
    #12 0x105b503f0 in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x20 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x143f0)
    #13 0x105b4ffa4 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x13fa4)
    #14 0x105b4fd78 in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_cpp_bindings.dylib:arm64+0x13d78)
    #15 0x105ad39f0 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_system_cpp.dylib:arm64+0x179f0)
    #16 0x105ad33f8 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_system_cpp.dylib:arm64+0x173f8)
    #17 0x105ad4314 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_system_cpp.dylib:arm64+0x18314)
    #18 0x107688110 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/xcode-chromium/src/out/asan-0314/libbase.dylib:arm64+0x190110)
    #19 0x1076f1668 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x800 (/Users/test/xcode-chromium/src/out/asan-0314/libbase.dylib:arm64+0x1f9668)
    #20 0x1076f0af8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x158 (/Users/test/xcode-chromium/src/out/asan-0314/libbase.dylib:arm64+0x1f8af8)
    #21 0x10757b398 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x184 (/Users/test/xcode-chromium/src/out/asan-0314/libbase.dylib:arm64+0x83398)
    #22 0x1076f2c7c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3c8 (/Users/test/xcode-chromium/src/out/asan-0314/libbase.dylib:arm64+0x1fac7c)
    #23 0x10761c3a0 in base::RunLoop::Run(base::Location const&)+0x438 (/Users/test/xcode-chromium/src/out/asan-0314/libbase.dylib:arm64+0x1243a0)
    #24 0x113f594ac in content::RendererMain(content::MainFunctionParams)+0x7dc (/Users/test/xcode-chromium/src/out/asan-0314/libcontent.dylib:arm64+0x2e514ac)
    #25 0x1140fc230 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x23c (/Users/test/xcode-chromium/src/out/asan-0314/libcontent.dylib:arm64+0x2ff4230)
    #26 0x1140fde74 in content::ContentMainRunnerImpl::Run()+0x568 (/Users/test/xcode-chromium/src/out/asan-0314/libcontent.dylib:arm64+0x2ff5e74)
    #27 0x1140fa1fc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x670 (/Users/test/xcode-chromium/src/out/asan-0314/libcontent.dylib:arm64+0x2ff21fc)
    #28 0x1140faab0 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/xcode-chromium/src/out/asan-0314/libcontent.dylib:arm64+0x2ff2ab0)
    #29 0x11ac069d4 in ChromeMain+0x338 (/Users/test/xcode-chromium/src/out/asan-0314/libchrome_dll.dylib:arm64+0xa9d4)
    #30 0x104f98ce0 in main+0x250 (/Users/test/xcode-chromium/src/out/asan-0314/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6358.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce0)
    #31 0x1882460dc  (<unknown module>)
    #32 0x6630fffffffffffc  (<unknown module>)

Address 0x7ea300451d18 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison (/Users/test/xcode-chromium/src/out/asan-0314/libblink_modules.dylib:arm64+0x2c01fb0) in blink::MIDIDispatcher::SessionStarted(midi::mojom::Result)+0x5ec
Shadow bytes around the buggy address:
  0x7ea300451a80: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m
  0x7ea300451b00: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
  0x7ea300451b80: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m
  0x7ea300451c00: [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m
  0x7ea300451c80: [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
=>0x7ea300451d00: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m[[1m[34mf7[1m[0m][1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
  0x7ea300451d80: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
  0x7ea300451e00: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[34mf7[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
  0x7ea300451e80: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
  0x7ea300451f00: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
  0x7ea300451f80: [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m [1m[0m00[1m[0m
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           [1m[0m00[1m[0m
  Partially addressable: [1m[0m01[1m[0m [1m[0m02[1m[0m [1m[0m03[1m[0m [1m[0m04[1m[0m [1m[0m05[1m[0m [1m[0m06[1m[0m [1m[0m07[1m[0m 
  Heap left redzone:       [1m[31mfa[1m[0m
  Freed heap region:       [1m[35mfd[1m[0m
  Stack left redzone:      [1m[31mf1[1m[0m
  Stack mid redzone:       [1m[31mf2[1m[0m
  Stack right redzone:     [1m[31mf3[1m[0m
  Stack after return:      [1m[35mf5[1m[0m
  Stack use after scope:   [1m[35mf8[1m[0m
  Global redzone:          [1m[31mf9[1m[0m
  Global init order:       [1m[36mf6[1m[0m
  Poisoned by user:        [1m[34mf7[1m[0m
  Container overflow:      [1m[34mfc[1m[0m
  Array cookie:            [1m[31mac[1m[0m
  Intra object redzone:    [1m[33mbb[1m[0m
  ASan internal:           [1m[33mfe[1m[0m
  Left alloca redzone:     [1m[34mca[1m[0m
  Right alloca redzone:    [1m[34mcb[1m[0m

==8698==ADDITIONAL INFO

==8698==Note: Please include this section with the ASan report.
Task trace:
    #0 0x105ad3dd4 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x244 (/Users/test/xcode-chromium/src/out/asan-0314/libmojo_public_system_cpp.dylib:arm64+0x17dd4)


==8698==END OF ADDITIONAL INFO
==8698==ABORTING
```

### mj...@chromium.org (2024-03-14)

That's great to know it also reproduces on Mac.  I haven't been able to reproduce it yet, but I am looking at possible causes.

I think the debug builds will turn all flags on by default.  That is why I asked if it reproduces with the flag explicitly disabled.

### mj...@chromium.org (2024-03-15)

Current conclusions:
- MidiAccessInitializer does start the MIDI session (https://crsrc.org/c/third_party/blink/renderer/modules/webmidi/midi_access_initializer.cc;l=138) and my change did modify MidiAccessInitializer, so it's possible my CL is the culprit.
- If the stack trace is trustworthy, it looks like client_ is going out of scope between the start of MIDIDispatcher::SessionStarted and crsrc.org/c/third_party/blink/renderer/modules/webmidi/midi_dispatcher.cc;l=122.
- I don't see any obvious causal link between my CL and the error.  It shouldn't have affected memory management, and it shouldn't have any effect if the flag is off.  However, there may be a secondary effect that isn't obvious so I will keep the issue assigned to me for now.

Submitter:
- Thank you for finding this!
- I know you don't have a POC, but can you give any more information about what you are running your fuzzer with?
- If you are able, please test with the command-line option "--disable-features=BlockMidiByDefault" and see if it still reproduces.  If it reproduces even with this option it is less likely that it is my change.  If it doesn't reproduce with this option it is very likely to be my change.
- If you have any bisection results please add them here.

I was having trouble getting Windows ASAN builds but will have access to a Mac tomorrow.  My next step will be to try to reproduce the problem.

### ki...@gmail.com (2024-03-15)

1. Thanks for your kind reply!
2. The POC can **still be reproduced** with the extra flag `--disable-features=BlockMidiByDefault`.
3. chrome commit **running in my fuzzer**, I suspect that the bisection commit should be about two weeks before this commit, since I am updating chrome commits once every two weeks.

```
commit ea5c6cdc94d3ca4ab0fc7f5207df5edc30609e6a (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Mon Mar 11 05:10:27 2024 +0000

    Roll Dawn from 78ee739f45b5 to 12c6b842d83d (1 revision)

    https://dawn.googlesource.com/dawn.git/+log/78ee739f45b5..12c6b842d83d

    2024-03-11 jiawei.shao@intel.com Remove DanglingUntriaged in BuddyAllocator

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/dawn-chromium-autoroll
    Please CC cwallez@google.com,senorblanco@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Bug: None
    Tbr: senorblanco@google.com
    Test: Test: dawn_unittests
    Include-Ci-Only-Tests: true
    Change-Id: I284b07d387b705d5f3560b3198a4b1558aa1ebe9
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5359984
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1270802}

```

4. I've attached the execution output of crashed chrome, hopefully that helps.

### pe...@google.com (2024-03-15)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-03-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mj...@chromium.org (2024-03-15)

Another possible culprit: https://source.chromium.org/chromium/chromium/src/+/3a052587991b866a377faf031b7da5b4bfa8ff2f

japhet@, could you please take a look if your change could have caused this, and pass back to me if you don't think so?

### ki...@gmail.com (2024-03-19)

This is my analysis of the vulnerability, please refer to it and feel free to point out any errors.

## Root Cause Analysis

1. MIDIAccessInitializer inherits from MIDIDispatcher::Client. During the first call of MIDIDispatcher::SessionStarted, client\_ will be a raw pointer pointing to MIDIAccessInitializer, which will call MIDIAccessInitializer::DidStartSession through client\_->DidStartSession[0].

```
void MIDIDispatcher::SessionStarted(midi::mojom::blink::Result result) {
[...]
    for (const auto& info : inputs_) {
      client_->DidAddInputPort(info.id, info.manufacturer, info.name,
                               info.version, info.state);
    }

    for (const auto& info : outputs_) {
      client_->DidAddOutputPort(info.id, info.manufacturer, info.name,
                                info.version, info.state);
    }
    client_->DidStartSession(result);//---> [0]
}

```

2. MIDIAccessInitializer::DidStartSession will initialize a MIDIAccess object through MakeGarbageCollected<MIDIAccess>[1], and pass it to the JavaScript side through resolver\_->Resolve[1], so only the JavaScript side holds a GC (Garbage Collection) reference to it. However, when MIDIAccess is initialized, it sets itself as the client of MIDIDispatcher[2], in the form of a raw\_ptr, meaning MIDIDispatcher cannot track the lifecycle of client\_.

```
void MIDIAccessInitializer::DidStartSession(Result result) {
  DCHECK(dispatcher_);
  // We would also have AbortError and SecurityError according to the spec.
  // SecurityError is handled in onPermission(s)Updated().
  switch (result) {
    case Result::NOT_INITIALIZED:
      NOTREACHED();
      return;
    case Result::OK:
      resolver_->Resolve(MakeGarbageCollected<MIDIAccess>( //<----[1]
          dispatcher_, options_->hasSysex() && options_->sysex(),
          port_descriptors_, resolver_->GetExecutionContext()));
[...]


MIDIAccess::MIDIAccess(
    MIDIDispatcher* dispatcher,
    bool sysex_enabled,
    const Vector<MIDIAccessInitializer::PortDescriptor>& ports,
    ExecutionContext* execution_context)
    : ActiveScriptWrappable<MIDIAccess>({}),
      ExecutionContextLifecycleObserver(execution_context),
      dispatcher_(dispatcher),
      sysex_enabled_(sysex_enabled),
      has_pending_activity_(false){
  dispatcher_->SetClient(this);// <-----[2]
[...]

```

3. During the second call to MIDIDispatcher::SessionStarted, at this point client\_ is the previously created MIDIAccess. While iterating over outputs\_, it re-enters JavaScript through client\_->DidAddOutputPort[3]. Since only the JavaScript side holds a GC reference to it, JavaScript can release its reference to force GC.
   In the next iteration of the loop [3], client\_ has already been released, and using it will trigger a use-after-poison.

```
void MIDIDispatcher::SessionStarted(midi::mojom::blink::Result result) {
[...]
    for (const auto& info : inputs_) {
      client_->DidAddInputPort(info.id, info.manufacturer, info.name,
                               info.version, info.state);
    }

    for (const auto& info : outputs_) {
      client_->DidAddOutputPort(info.id, info.manufacturer, info.name,
                                info.version, info.state); //<---[3]
    }
    client_->DidStartSession(result);
}

void MIDIAccess::DidAddOutputPort(const String& id,
                                  const String& manufacturer,
                                  const String& name,
                                  const String& version,
                                  PortState state) {
  DCHECK(IsMainThread());
  unsigned port_index = outputs_.size();
  auto* port = MakeGarbageCollected<MIDIOutput>(
      this, port_index, id, manufacturer, name, version, ToDeviceState(state));
  outputs_.push_back(port);
  DispatchEvent(*MIDIConnectionEvent::Create(port));//<----[3]
}

```
## Patch

The key issue here is that client\_ is stored as a raw pointer. Changing it to a WeakMember or Member should resolve the problem.

```
class MIDIDispatcher : public GarbageCollected<MIDIDispatcher>,
                       public midi::mojom::blink::MidiSessionClient {
[...]
-  raw_ptr<Client> client_ = nullptr;
+  WeakMember<Client> client_ = nullptr

```

### ja...@chromium.org (2024-03-20)

The analysis in #20 looks correct to me. `MIDIDispatcher::Client` should be a GarbageCollectedMixin<>, and we should hold `client_` with an oilpan wrapper (I don't know this code well enough to immediately know whether it should be a strong or weak reference)

### ap...@google.com (2024-03-21)

Project: chromium/src
Branch: main

commit 490fa6dc127b72fb6fd959e6b011a237a53b1c38
Author: Nate Chapin <japhet@chromium.org>
Date:   Thu Mar 21 00:41:13 2024

    Make MIDIDispatcher::Client a GarbageCollectedMixin
    
    Fixed: 329130361
    Change-Id: I6a25f07e191da57b75c45ac6adec4255928847bd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5376546
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Nate Chapin <japhet@chromium.org>
    Commit-Queue: Michael Wilson <mjwilson@chromium.org>
    Auto-Submit: Nate Chapin <japhet@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1275957}

M       third_party/blink/renderer/modules/webmidi/midi_access_initializer.h
M       third_party/blink/renderer/modules/webmidi/midi_dispatcher.cc
M       third_party/blink/renderer/modules/webmidi/midi_dispatcher.h

https://chromium-review.googlesource.com/5376546


### pe...@google.com (2024-03-21)

Requesting merge to beta (M124) because latest trunk commit (1275957) appears to be after beta branch point (1274542).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-03-22)

Merge approved: your change passed merge requirements and is auto-approved for M124. Please go ahead and merge the CL to branch 6367 (refs/branch-heads/6367) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-03-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@google.com (2024-03-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ki...@gmail.com (2024-03-27)

Hi, Amy, I have provided a detailed analysis. Please let me know why this cannot be regarded as a high-quality vulnerability report. Thank you!

### am...@chromium.org (2024-03-27)

Hi Kiprey, this was considered a renderer process memory corruption issue, mildly mitigated by race condition and a below baseline report. While we appreciate your report, the analysis in c#20 was provided 8 days after the initial report and also a POC was never provided and it was never made completely clear what flags were required in triggering to investigate this issue. This required a great deal of back and forth to triage and investigate this issue to bring it to resolution. Based on all these factors, we cannot assess this a high quality report.

### ki...@gmail.com (2024-03-27)

Thank you for your explanation. I accept other suggestions. But I don't think the time to provide analysis will affect how it becomes a high-quality report. I always think it is better to submit the report as soon as possible, which will reduce the possibility of users being threatened. I spent a lot of time investigating this issue, so this is the reason why the analysis was submitted late. Since the final solution to this vulnerability still depends on the analysis I provide, please consider this aspect as appropriate to consider whether more bonuses can be provided.

### ki...@gmail.com (2024-03-27)

I want to discuss with you about this vulnerability and the problem of the reporting process. More streamlined flags and poc are difficult to obtain in the fuzz test. I will try my best to improve this, but I can't guarantee it. In addition, I would like to know whether you prefer to submit the vulnerability before analyzing it, or get it at the same time? As I said, this bug took me a lot of time to study and rely on my analysis to solve it. If I submitted it too early and got a lower bonus, it might be unfair. What do you think?

### ki...@gmail.com (2024-03-27)

I don't mean to make it more difficult for you to deal with the vulnerability and try my best to investigate it. Please help me communicate this to chrome vrp, please let me know which way you prefer to submit vulnerabilities, and let me know if I can get more bounty. Thank you!

### am...@chromium.org (2024-03-27)

Sorry for the delay in my follow-up response. As usual it's a bit busy here in Chrome Security land.
We completely appreciate your willingness and instinct to provide reports sooner than later, and while we generally encourage that -- especially as it relates to exploit submissions or in depth analysis -- we also have to balance that with ensuring that reports are complete enough to fully triage and investigate by an engineer. We don't mean for this to seem unfair to you, but it is what is necessary for us to balance individual bug reports amount the other numerous security issues and other work each team is encountered with each week.

In this case, the security shepherd had to track this for three days and just to provide minimal information to one engineer, who ended up not being the correct person to take on this issue, for it to be assigned to japhet@ in the end. This resulted in a much back and forth before even being able to get it to the right person or understand where the core issue lies and what features were involved.

Chrome Security sees upwards of new 70 security bug reports from external researcher in a given week. In order to triage them effectively we need at least baseline details to do verify the bug is a security issue and is reachable and exploitable one.

Which flags are needed to trigger an issue is important, because not only is the information valuable in our analysis and investigation, but simply, it helps us know if it is SI-None. While that doesn't matter to VRP eligibility, it does matter to triage and more importantly, to the engineers working the issue, so they know how to prioritize it.

Which bring me to the most important part of the equation about why complete security bug reporting matters -- security bugs are the highest priority for Chrome engineering teams. For us in Security to pass over bug reports to engineers, we want to make sure we have first determine to be a valid and exploitable security issue, prioritized as such, We also want to make sure we can assign it to the right person or team have brought to surface and the report has present most of the basic elements they would need to investigate and fix the issue efficiently.

While one of the best parts of our Chromium bug processes is that it allows with everyone involved to interact on bugs, it should not require engineering teams to need to ask about basic elements of the bug, such as for a reproducer or the flags involved.

Based on this timeline of this report, we would have definitely preferred you not have reported it until the information in c#15 and c#20 could have been provided in the original report before submitting, since this was all information necessary to investigate and resolve this issue.
I do want to mention, that when you are chatting with me, you are chatting with both a representative of the security team, but also the Chrome VRP. I am the person responsible for it, but I also am on the Panel, so anything I have communicated to you is communicated to, from, and on behalf of the Chrome VRP.

I hope this helps you understand what is needed to begin with future reports and why we lean into the importance of report quality and making assessments based on when certain information (such as POCs, analysis, or even bisects) are provided. All of this is information that we use to getting bugs to the right Chrome engineers to be prioritized, fixed, and allow fixes to be shipped to Chrome users in a timely fashion as that is what is most important and the reason for a security bug bounty program to begin with.

### ki...@gmail.com (2024-03-28)

I will optimize my report process to ensure that I have a preliminary analysis of asan log before submitting it. Thanks to chrome VRP.

### pe...@google.com (2024-04-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mj...@chromium.org (2024-04-01)

It looks like the merge cherry-pick failed auto-submit due to a probably unrelated failure: https://crrev.com/c/5396497

It is a clean cherry-pick so I will try to submit it again.

### ap...@google.com (2024-04-01)

Project: chromium/src
Branch: refs/branch-heads/6367

commit c300d073639a4e01bd46cfad3caeb434fec9326d
Author: Nate Chapin <japhet@chromium.org>
Date:   Mon Apr 01 18:42:24 2024

    Make MIDIDispatcher::Client a GarbageCollectedMixin
    
    (cherry picked from commit 490fa6dc127b72fb6fd959e6b011a237a53b1c38)
    
    Fixed: 329130361
    Change-Id: I6a25f07e191da57b75c45ac6adec4255928847bd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5376546
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Nate Chapin <japhet@chromium.org>
    Commit-Queue: Michael Wilson <mjwilson@chromium.org>
    Auto-Submit: Nate Chapin <japhet@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1275957}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5396497
    Auto-Submit: Daniel Yip <danielyip@google.com>
    Owners-Override: Daniel Yip <danielyip@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6367@{#445}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/renderer/modules/webmidi/midi_access_initializer.h
M       third_party/blink/renderer/modules/webmidi/midi_dispatcher.cc
M       third_party/blink/renderer/modules/webmidi/midi_dispatcher.h

https://chromium-review.googlesource.com/5396497


### mj...@chromium.org (2024-04-01)

Should be fully resolved now.  Thanks everyone.

### pe...@google.com (2024-06-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/329130361)*
