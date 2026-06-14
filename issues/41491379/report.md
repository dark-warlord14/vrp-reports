# Security:  [Network Process] 8-byte use-after-free in `net::QuicChromiumClientSession`

| Field | Value |
|-------|-------|
| **Issue ID** | [41491379](https://issues.chromium.org/issues/41491379) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Mac |
| **Reporter** | op...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2024-01-15 |
| **Bounty** | $7,000.00 |

## Description

## Tested Version

  •  121.0.6140.0 (Developer Build)
  •  `mac-release-asan-mac-release-1227262` from storage bucket
  •  macOS 14.2 (23C5055b)

## Attachments

  •  Apple MacOS Crash Report: 1-apple-macos-crash-report.log
  •  Chromium ASAN Report: 2-chromium-asan-report.log
  •  Proof of Concept: 3-proof-of-concept.html

## Reproduction Steps

  #1 - Open proof-of-concept.html.
  #2 - Wait for approximately 2 to 3 seconds.
  #3 - Close the tab.

 ※ While `setTimeout(() => window.close(), 2500);` can be employed for step #3, manually closing the window tends to reproduce better.
 ※ It is hard to trigger the bug as it requires tightly timed race condition.

## AddressSanitizer Report

```
==24101==ERROR: AddressSanitizer: heap-use-after-free on address 0x608000588b30 at pc 0x00016cac4946 bp 0x000308b053f0 sp 0x000308b053e8
READ of size 8 at 0x608000588b30 thread T6
    #0 0x16cac4945 in net::QuicChromiumClientSession::StreamRequest::OnRequestCompleteFailure(int)+0x3e5 (/Users/dch3ck/Desktop/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Chromium Framework:x86_64+0x12e5f945)
    #1 0x16cac9ded in net::QuicChromiumClientSession::~QuicChromiumClientSession()+0xb9d (/Users/dch3ck/Desktop/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Chromium Framework:x86_64+0x12e64ded)
  ...  [ For the complete details, please refer to the chromium-asan-report.log file. ]
```

## Description

The `net::QuicChromiumClientSession::Handle::RequestStream` function creates a `StreamRequest` object that is susceptible to a use-after-free condition. This occurs when an 8-byte pointer, which has been previously freed, is reused in the `OnRequestCompleteFailure` method, potentially leading to the execution of a callback function. If an attacker manipulates the `callback_` object, it could be exploited to execute arbitrary code.

The UAF appears to stem from improper lifecycle management of a `callback_`. This callback is scheduled for execution in the OnRequestCompleteFailure function.

The nature of posting tasks for delayed execution `base::SingleThreadTaskRunner::PostTask` means that the callback might be executed at a time when the object it belongs to `StreamRequest` might already have been destroyed.

## Evidence

Stack trace pointing to `OnRequestCompleteFailure`.
The use of `base::BindOnce` with `callback_` for delayed execution.

## Allocation

```
previously allocated by thread T6 here:
    #0 0x109e12900 in __asan_memmove+0x2d30 (/path/to/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Helpers/Chromium Helper.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x52900)
    #1 0x16aa1b8f7 in operator new(unsigned long)+0x27 (/path/to/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Chromium Framework:x86_64+0x10db68f7)
    #2 0x16cac0a4b in net::QuicChromiumClientSession::Handle::RequestStream(bool, base::OnceCallback<void (int)>, net::NetworkTrafficAnnotationTag const&)+0x20b (/path/to/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Chromium Framework:x86_64+0x12e5ba4b)
    #3 0x16cb2e95f in net::QuicHttpStream::DoRequestStream()+0x3af (/path/to/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Chromium Framework:x86_64+0x12ec995f)
    #4 0x16cb289db in net::QuicHttpStream::DoLoop(int)+0x43b (/path/to/mac-release-asan-mac-release-1227262/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/121.0.6140.0/Chromium Framework:x86_64+0x12ec39db)
    ...
```

At `#4 0x16cb289d`, `DoRequestStream()` is called and the resulting integer value is stored in `rv`.

```
// chromium/src/net/quic/quic_http_stream.cc

int QuicHttpStream::DoLoop(int rv) {
  // ... [Snipped for brevity] ...
  do {
    // ... [State machine logic snipped for brevity] ...
        rv = DoRequestStream();
        break;
    // ... [Rest of the state machine logic snipped for brevity] ...
  } while (rv is not pending and states are still transitioning);
  return rv;
}
```

At `#3 0x16cb2e95f`, `RequestStream()` is invoked.

```
// chromium/src/net/quic/quic_http_stream.cc

int QuicHttpStream::DoRequestStream() {
  next_state_ = STATE_REQUEST_STREAM_COMPLETE; // Set next state

  return quic_session()->RequestStream(
      !can_send_early_, // Flag indicating if 0-RTT data can be sent
      base::BindOnce(&QuicHttpStream::OnIOComplete, weak_factory_.GetWeakPtr()), // Binding completion callback
      NetworkTrafficAnnotationTag(request_info_->traffic_annotation)); // Network traffic analysis tag
}
```

The memory for the `QuicChromiumClientSession::Handle` is allocated using `operator new(unsigned long)`.

The `RequestStream` method is called within `net::QuicHttpStream::DoRequestStream`, which subsequently calls `DoLoop` that processes the request loop and handles the state transitions.

```
// chromium/src/net/quic/quic_chromium_client_session.cc

int QuicChromiumClientSession::Handle::RequestStream(
    bool requires_confirmation,
    CompletionOnceCallback callback,
    const NetworkTrafficAnnotationTag& traffic_annotation) {
  DCHECK(!stream_request_);

  if (!session_)
    return ERR_CONNECTION_CLOSED;

  // ... [Logic to confirm the connection before starting the stream if 0-RTT is disabled] ...

  // Instantiate a new StreamRequest object
  stream_request_ = base::WrapUnique(
      new StreamRequest(this, requires_confirmation, traffic_annotation)); // Memory allocation here
  return stream_request_->StartRequest(std::move(callback));
}
```

 An object of type `StreamRequest` is created and assigned to the `stream_request_` variable, allocating `0x58` bytes of memory, as shown in the snippet where `edi` is set to `0x58` just before calling the `new` operator (denoted by `_Znwm`):

```
0x00005596e5aaca98 <+216>:   mov    a1,BYTE PTR [rbp-0x19]
0x00005596e5aaca9b <+219>:   and    al,0x1
0x00005596e5aaca9d <+221>:   movzx  eax,al
0x00005596e5aaca0 <+224>:    or     eax,ecx
0x00005596e5aaca2 <+226>:    cmp    eax,0x0
0x00005596e5aaca5 <+229>:    setne  al
0x00005596e5aaca8 <+232>:    and    al,0x1
0x00005596e5aacaa <+234>:    mov    BYTE PTR [rbp-0x19],al
=> 0x00005596e5aacad <+237>:   mov    edi,0x58
0x00005596e5aacab2 <+242>:    call   0x5596e637f6d0 <_Znwm>
0x00005596e5aacab7 <+247>:    mov    rsi,QWORD PTR [rbp-0x78]
0x00005596e5aacabb <+251>:    mov    rdi,rax
0x00005596e5aacabe <+254>:    mov    QWORD PTR [rbp-0x88],rdi
0x00005596e5aacac5 <+261>:    mov    al,BYTE PTR [rbp-0x19]
0x00005596e5aacac8 <+264>:    mov    rcx,QWORD PTR [rbp-0x28]
```

```
gef➤  x/88wx 0x00003700000a5260

0x3700000a5260: 0xabababab                        0xabababab                        0xabababab                        0xabababab
0x3700000a5270: 0xabababab                        0xabababab                        0xabababab                        0xabababab
0x3700000a5280: 0xabababab                        0xabababab                        0xabababab                        0xabababab
0x3700000a5290: 0xabababab                        0xabababab                        0xabababab                        0xabababab
0x3700000a52a0: 0xabababab                        0xabababab                        0xabababab                        0xabababab
0x3700000a52b0: 0xabababab                        0xabababab                        0xefbeadde                        0x0dd0feca
0x3700000a52c0: 0x05f03713                        0x1eab11ba                        0x00000000                        0x00000000
```

This snippet is from the disassembly of the `RequestStream` function where a new `StreamRequest` object is being created

```
0x5596e5aacac8 <net::QuicChromiumClientSession::Handle::RequestStream(bool,+)0> mov rcx, QWORD PTR [rbp-0x28]
0x5596e5aacacc <net::QuicChromiumClientSession::Handle::RequestStream(bool,+)4> and al, 0x1
0x5596e5aacace <net::QuicChromiumClientSession::Handle::RequestStream(bool,+)6> movzx edx, al
0x5596e5aacad1 <net::QuicChromiumClientSession::Handle::RequestStream(bool,+)9> call 0x5596e5aad1b0 <net::QuicChromiumClientSession::StreamRequest::StreamRequest(net::QuicChromiumClientSession::Handle*,+)> push rbp
0x5596e5aad1b0 <net::QuicChromiumClientSession::StreamRequest::StreamRequest(net::QuicChromiumClientSession::Handle*,+)> mov rbp, rsp
0x5596e5aad1b1 <net::QuicChromiumClientSession::StreamRequest::StreamRequest(net::QuicChromiumClientSession::Handle*,+)> sub rsp, 0x30
0x5596e5aad1b4 <net::QuicChromiumClientSession::StreamRequest::StreamRequest(net::QuicChromiumClientSession::Handle*,+)> mov al, dl
0x5596e5aad1b8 <net::QuicChromiumClientSession::StreamRequest::StreamRequest(net::QuicChromiumClientSession::Handle*,+)> mov QWORD PTR [rbp-0x8], rdi
0x5596e5aad1ba <net::QuicChromiumClientSession::StreamRequest::StreamRequest(net::QuicChromiumClientSession::Handle*,+)> mov QWORD PTR [rbp-0x10], rsi

_ZN3net25QuicChromiumClientSession13StreamRequestC2EPNS0_6HandleEbRKNS_27NetworkTrafficAnnotationTagE (
QWORD var_0 = 0x000037e0000a5260 -> 0xabababababababab,
QWORD var_1 = 0x000037000064820 -> 0x00005596e573acc8 -> 0x00005596e5aac380 -> net::QuicChromiumClientSession::Handle::Handle()+0> push rbp,
bool var_2 = 0x0000000000000000,
QWORD var_3 = 0x00007ffccf6b074c -> 0x00007ffccf6b4492
)
```

In the newly allocated memory space, a pointer to `QuicChromiumClientSession::Handle` is stored. This is done by initializing a `base::raw_ptr` to point to an instance of `QuicChromiumClientSession::Handle`.

```
gef➤ ni
Thread 1 "net_unittests" hit Hardware watchpoint 4: *0x000037e0000a5260

Old value = 0xabababab
New value = 0x64820
0x00005596e5ac2a88 in base::raw_ptr<net::QuicChromiumClientSession::Handle, (partition_alloc::internal::RawPtrTraits)>::raw_ptr (this=0x37e0000a5260, p=0x37e000064820) at ../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:460
460     : wrapped_ptr_(Impl::WrapRawPtr(p)) {}

gef➤ x/88wx 0x000037e0000a5260
0x37e0000a5260: 0x000064820   0xabababab  0xabababab  0xabababab
0x37e0000a5270: 0xabababab   0xabababab  0xabababab  0xabababab
0x37e0000a5280: 0xabababab   0xabababab  0xabababab  0xabababab
0x37e0000a5290: 0xabababab   0xabababab  0xabababab  0xabababab
0x37e0000a52a0: 0xabababab   0xabababab  0xfebdeadde 0xddd0feca
0x37e0000a52b0: 0xabababab   0x1eab11ba  0x00000000  0x00000000
0x37e0000a52c0: 0x05f03713   0xeab11ba   0xcdcdcdcd  0xcdcdcdcd
0x37e0000a52d0: 0xcd037e000 0x8d051a00  0xcdcdcdcd  0xcdcdcdcd
0x37e0000a52e0: 0xcdcdcdcd   0xcdcdcdcd  0xcdcdcdcd  0xcdcdcdcd
0x37e0000a52f0: 0xcdcdcdcd   0xcdcdcdcd  0xcdcdcdcd  0xcdcdcdcd
0x37e0000a5300: 0xcdcdcdcd   0xcdcdcdcd  0xcdcdcdcd  0xcdcdcdcd
0x37e0000a5310: 0xcdcdcdcd   0xcdcdcdcd  0xcdcdcdcd  0xcdcdcdcd
0x37e0000a5320: 0xcdcdcdcd   0xcdcdcdcd  0xcdcdcdcd  0xcdcdcdcd
0x37e0000a5330: 0xcdcdcdcd   0x00000001  0x00000000  0x00000000
0x37e0000a5340: 0x000646d00  0x000037e00  0xababab00  0x00000000
0x37e0000a5350: 0x00000000   0x00000000  0x00000000  0x00000000
0x37e0000a5360: 0x00000001   0x00000000  0xababab00  0x00000000
0x37e0000a5370: 0x00000000   0x00000000  0x00000000  0x00000000
0x37e0000a5380: 0x00000000   0x00000000  0x00000000  0x00000000
0x37e0000a5390: 0x00000000   0xabababab  0xeab11ba   0x00000000
```

## Free

```
// chromium/src/net/quic/quic_chromium_client_session.cc
QuicChromiumClientSession::Handle::~Handle() {
  if (session_)
    session_->RemoveHandle(this);
}

void QuicChromiumClientSession::RemoveHandle(Handle* handle) {
  DCHECK(base::Contains(handles_, handle));
  handles_.erase(handle);
}
```

## Use

The stack trace entry `#0 0x16cac4945` points to the `OnRequestCompleteFailure` function within `QuicChromiumClientSession`. The corresponding source code snippet suggests that if the `callback_` member variable is not `null`, it schedules a callback for later execution. A UAF could occur if `callback_` is referencing memory that has been freed prior to the callback's execution.

```
// chromium/src/net/quic/quic_chromium_client_session.cc
void QuicChromiumClientSession::StreamRequest::OnRequestCompleteFailure(
    int rv) {
  //DCHECK_EQ(STATE_REQUEST_STREAM_COMPLETE, next_state_);
  // This method is called even when the request completes synchronously.
  if (callback_) {
    // Avoid re-entrancy if the callback calls into the session.
    base::SingleThreadTaskRunner::GetCurrentDefault()->PostTask(
        FROM_HERE,
        base::BindOnce(&QuicChromiumClientSession::StreamRequest::DoCallback,
                       weak_factory_.GetWeakPtr(), rv));
  }
}
```

## Credit

 {rotiple, dch3ck} of CW Research Inc.

## Attachments

- [1-apple-macos-crash-report.log](attachments/1-apple-macos-crash-report.log) (text/plain, 26.1 KB)
- [2-chromium-asan-report.log](attachments/2-chromium-asan-report.log) (text/plain, 28.2 KB)
- deleted (application/octet-stream, 0 B)
- [3-proof-of-concept.html](attachments/3-proof-of-concept.html) (text/html, 320 B)

## Timeline

### op...@gmail.com (2024-01-15)

[Comment Deleted]

### op...@gmail.com (2024-01-15)

Could you please include `dch3ck@gmail.com`, `contact@cwresearchlab.co.kr` as he is a contributor to this report?

### [Deleted User] (2024-01-15)

[Empty comment from Monorail migration]

### mp...@chromium.org (2024-01-17)

Do you think you can provide a stack trace with line numbers, I'm unable to reproduce this on Linux.

The "use" stack trace indicates accessing `callback_` is the bug and so the QuicChromiumClientSession::StreamRequest is probably deleted. Bug the "free" stack trace looks like the QuicChromiumClientSession::Handle is being deleted so I'm a little confused.

### op...@gmail.com (2024-01-17)

Could you please refer to 1-apple-macos-crash-report.log?

### mp...@chromium.org (2024-01-18)

That helps but if I'm not mistaken that's not the ASAN crash log, so there aren't any line numbers for the alloc/free stack traces?

### mp...@chromium.org (2024-01-18)

Also the PoC seems to just trigger an infinite recursion under a try/catch block before finally constructing a PaymentRequest. I'm honestly confused why that is the case, why not just loop infintely creating the PaymentRequest? And where am I supposed to put the setTimeout if I want to automate the tab closing? It seems like this is just an infinite loop and so the setTimeout will never run?

### mp...@chromium.org (2024-01-18)

[Empty comment from Monorail migration]

### op...@gmail.com (2024-01-22)

When I initially encountered this issue, I manually closed the tab. Indeed, the 1-apple-macos-crash-report.log is not an ASan log, so we also tried to analyze the issue with reference to "1-apple-macos-crash-report.log". This issue manifested when the tab was closed, and the trace indicates it likely occurred due to some disruption or closure in the network. Therefore, I proposed that it might be possible to reproduce using JavaScript. Additionally, the issues you raised are also aspects we find confusing.

### [Deleted User] (2024-01-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@chromium.org (2024-01-23)

Can you reproduce again and provide an ASAN stack trace?

### op...@gmail.com (2024-01-24)

We have encountered difficulties in reproducing the issue, which has prompted us to report it without proper root cause. We will attempt reproduction once more. 

### [Deleted User] (2024-01-24)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2024-01-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2024-01-30)

(Adding CCs as requested by the reporter and adding tentative labels)

opveopve: Have you been able to reproduce again?

liza: Could you also PTAL since you are also looking at https://crbug.com/chromium/1522157? Thanks.

[Monorail components: Internals>Network>QUIC]

### ad...@google.com (2024-01-31)

(I am a bot: this is an auto-cc on a security bug)

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1518403?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### li...@chromium.org (2024-02-05)

I think the fundamental problem is that QuicChromiumClientSession::Handle::RequestStream only checks whether the session currently exists or not, but the session can be marked as going away in [QuicChromiumClientSession::NotifyFactoryOfSessionClosedLater](https://source.chromium.org/chromium/chromium/src/+/main:net/quic/quic_chromium_client_session.cc;l=3574;drc=0907824d24b445e547bf98c36806385688cf41d6;bpv=1;bpt=1). If this method is called in [QuicChromiumClientSession::OnPacket](https://source.chromium.org/chromium/chromium/src/+/main:net/quic/quic_chromium_client_session.cc;l=3554;drc=0907824d24b445e547bf98c36806385688cf41d6;bpv=1;bpt=1) the handles aren't closed before calling QuicChromiumClientSession::NotifyFactoryOfSessionClosedLater.

This is also likely why it's hard to reproduce this, as the race condition relies on QuicChromiumClientSession::NotifyFactoryOfSessionClosedLater specifically after the packet reader finishes a read, and depends on the QuicConnection being closed.

The session needs to outlive the StreamRequest, so QuicChromiumClientSession::Handle::RequestStream should be checking if the session is going away as well as if it is exists at all or not before creating the request.

### li...@chromium.org (2024-02-05)

I have a quick CL out at <https://chromium-review.googlesource.com/c/chromium/src/+/5268864> but still need to add tests for this.

Reporter, were you able to repro this again at all? If so, could you try repro-ing with the above patch? That would at least be a helpful starting point to see if I did identify the root cause correctly while I work on getting tests written.

### aj...@google.com (2024-02-05)

Updating labels: 120 as the code in the CL in #22 affects old code. S2/Medium as this is clearly very racy.

### op...@gmail.com (2024-02-06)

Unfortunately, I was unable to reproduce it. I'll analyze and attempt reproducing based on the RCA. Thank you liza.

### pe...@google.com (2024-02-06)

Thank you for providing more feedback. Adding the requester to the cc list.

### pe...@google.com (2024-02-06)

Setting milestone because of s2 severity.

### pe...@google.com (2024-02-20)

liza: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-02-21)

Project: chromium/src
Branch: main

commit de9ce1844e5024a8b9a822fa8321f59a05fb990c
Author: Liza Burakova <liza@chromium.org>
Date:   Wed Feb 21 19:02:15 2024

    Check if session is going away in Handle::RequestStream.
    
    This CL adds an extra check in the QuicChromiumClientSession
    handle's RequestSession to make sure the session is not
    marked as going away before creating a new StreamRequest.
    
    Bug: 41491379
    Change-Id: I687dfc23131871cdba345d3cf78dbbbd2e619ce9
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5268864
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
    Commit-Queue: Liza Burakova <liza@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1263483}

M       net/quic/quic_chromium_client_session.cc

https://chromium-review.googlesource.com/5268864


### li...@chromium.org (2024-02-21)

opveopve@, could you attempt reproduction one more time with & without the fix that just landed? I'll wait to mark this as fixed until then.

### op...@gmail.com (2024-02-22)

liza@, Based on my examination, it appears that the issue was not caused by failing to check `going_away_`. This is because the `StartRequest` function re-checks `going_away_` when it calls `TryCreateStream`. Therefore, the flow should have been `net::QuicChromiumClientSession::Handle::Handle -> net::QuicChromiumClientSession::StreamRequest::OnRequestCompleteFailure -> net::QuicChromiumClientSession::Handle::~Handle`. However, I suspect the problem arose due to `network::ThrottlingNetworkTransaction::~ThrottlingNetworkTransaction` leading to a sequence of `net::QuicChromiumClientSession::Handle::Handle -> net::QuicChromiumClientSession::Handle::~Handle -> net::QuicChromiumClientSession::StreamRequest::OnRequestCompleteFailure`. Am I correct in this assumption?

```
#1  0x000055efd891c4d9 in net::QuicChromiumClientSession::TryCreateStream(net::QuicChromiumClientSession::StreamRequest*) (this=0x29680009f600, request=0x2968000a9420) at ../../net/quic/quic_chromium_client_session.cc:1188
#2  0x000055efd891c324 in net::QuicChromiumClientSession::Handle::TryCreateStream(net::QuicChromiumClientSession::StreamRequest*) (this=0x296800068b60, request=0x2968000a9420) at ../../net/quic/quic_chromium_client_session.cc:508
#3  0x000055efd891d73c in net::QuicChromiumClientSession::StreamRequest::DoRequestStream() (this=0x2968000a9420) at ../../net/quic/quic_chromium_client_session.cc:688
#4  0x000055efd891d0ef in net::QuicChromiumClientSession::StreamRequest::DoLoop(int) (this=0x2968000a9420, rv=0x0) at ../../net/quic/quic_chromium_client_session.cc:650
#5  0x000055efd891bed9 in net::QuicChromiumClientSession::StreamRequest::StartRequest(base::OnceCallback<void (int)>) (this=0x2968000a9420, callback=...) at ../../net/quic/quic_chromium_client_session.cc:583
#6  0x000055efd891bdb9 in net::QuicChromiumClientSession::Handle::RequestStream(bool, base::OnceCallback<void (int)>, net::NetworkTrafficAnnotationTag const&) (this=0x296800068b60, requires_confirmation=0x0, callback=..., traffic_annotation=...) at ../../net/quic/quic_chromium_client_session.cc:479

```
```
// src/net/quic/quic_chromium_client_session.cc
int QuicChromiumClientSession::TryCreateStream(StreamRequest* request) {
  if (goaway_received()) {
    DVLOG(1) << "Going away.";
    return ERR_CONNECTION_CLOSED;
  }

  if (!connection()->connected()) {
    DVLOG(1) << "Already closed.";
    return ERR_CONNECTION_CLOSED;
  }

  if (going_away_) {
    return ERR_CONNECTION_CLOSED;
  }

  bool can_open_next = CanOpenNextOutgoingBidirectionalStream();
  if (can_open_next) {
    request->stream_ =
        CreateOutgoingReliableStreamImpl(request->traffic_annotation())
            ->CreateHandle();
    return OK;
  }

```

### pe...@google.com (2024-02-23)

The NextAction date has arrived: 2024-02-23

### li...@chromium.org (2024-02-26)

Hmm, I'm not sure actually. `TryCreateStream` does in fact check if the session is going away when the state machine reaches `STATE_REQUEST_STREAM`, however, the first state of the state machine calls `QuicChromiumClientSession::StreamRequest::DoWaitForConfirmation()` , and this state can wait for a handshake confirmation which would cause the whole state machine to wait, so there is a chance the session goes away while the StreamRequest is waiting for the handshake confirmation, and `OnRequestCompleteFailure` is called.

Looking through your original report, it's `QuicHttpStream::DoRequestStream` that calls `RequestStream`, I don't see `TryCreateStream` anywhere in the asan log or original report, so it's not obvious if that part of the state machine is even hit by your PoC before the UaF happens. :\

The `QuicChromiumClientSession::Handle` shouldn't create a StreamRequest if the session doesn't exist or won't exist soon precisely for this reason imho.

### op...@gmail.com (2024-02-29)

As you mentioned, since `TryCreateStream` is not visible in `QuicHttpStream::DoRequestStream`, it seems that `QuicChromiumClientSession::Handle` should not create a `StreamRequest`. I have attempted to reproduce this situation using unit tests and a PoC, but there have been no successful results. :/

### li...@chromium.org (2024-02-29)

Okay, in this case I think I'm going to close out this bug as fixed, then, since I'm reasonably confident the fix I landed addresses the issue even though we still can't test it.

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-07)

Congratulations {rotiple, dch3ck}! The Chrome VRP Panel has decided to award you $7,000 for this report of a mildly mitigated memory corruption bug in the network process reachable from the renderer, mitigated by race condition and network process interruption. A member of the Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for efforts and reporting this issue to us!

### dc...@gmail.com (2024-03-08)

Thank you for the reward. Could you please forward the reward to contact@cwresearchlab.co.kr? Additionally, we have removed the proof-of-concept from the original report in accordance with c#8, as it is not relevant to the reproduction process.

### am...@chromium.org (2024-03-08)

We don't handle payments. But when we send the reward data over to the p2p-vrp finance team, I can stipulate that they should reach out to the email address provided in c#37 for enrolling for payment.

### am...@chromium.org (2024-03-08)

An additional note, I have restored the POC since it was the artifact provided that we used to attempt to reproduce and investigate this issue. This artifact is considered part of the report for VRP and disclosure processes. Thanks!

### dc...@gmail.com (2024-04-22)

deleted

### li...@chromium.org (2024-04-30)

Hello,

We don't think this qualified for security embargo as we can mitigate the PII shared.
I deleted your initial PoC and am re-uploading it with the domain removed. We can also delete [#comment40](https://issues.chromium.org/issues/41491379#comment40) to remove the domain as well, you should be able to delete the comment yourself or I can delete it for you. Edit history will be public so I suggest fully deleting the comment, not just editing.

I also suggest checking with your registrar as it may be possible to add whois privacy to your domain, it could take some amout of business days to take effect, though.

### pe...@google.com (2024-06-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ap...@google.com (2024-07-16)

Project: chromium/src
Branch: main

commit f2bfc40f7d6d135da090e04f35d376c93a4ab24c
Author: Xinan Lin <linxinan@google.com>
Date:   Tue Jul 16 23:05:16 2024

    Add test to cover cases that proxy sessions go away for JobController
    
    BUG=336318587,41491379
    TEST=net_unittests -- \
         gtest_filter=JobControllerReconsiderProxyAfterErrorTest.*
    
    Change-Id: Ib243c94cabe58afff3cb0b1980b944a61158c630
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5698005
    Reviewed-by: Dustin Mitchell <djmitche@chromium.org>
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
    Commit-Queue: Xinan Lin <linxinan@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1328511}

M       net/http/http_stream_factory_job_controller_unittest.cc
M       net/quic/quic_chromium_client_session.cc
M       net/quic/quic_chromium_client_session.h
M       net/quic/quic_session_pool.cc
M       net/quic/quic_session_pool.h

https://chromium-review.googlesource.com/5698005


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41491379)*
