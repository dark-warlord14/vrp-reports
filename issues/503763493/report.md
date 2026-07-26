# Browser Process Heap-Use-After-Free in Digital Credentials API (Renderer → Browser Memory Corruption)

| Field | Value |
|-------|-------|
| **Issue ID** | [503763493](https://issues.chromium.org/issues/503763493) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>DigitalCredentials |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wo...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-04-17 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

incomplete fix of 488617440

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

content/browser/webid/digital\_credentials/

---

### The problem

#### Please describe the technical details of the vulnerability

i had sent a report about Heap-Use-After-Free in Digital Credentials API, <https://issues.chromium.org/issues/488617440>. the issue was fixed but i found a byass.
kindly cc/ping [mamir@chromium.org](mailto:mamir@chromium.org) because he fixed the previous issue.

## Reproduction Steps

1. Launch Chrome
2. Load the PoC page
3. Ensure Bluetooth is disabled
4. Trigger Digital Credentials request → error UI shown
5. Click "Try Again" (Bluetooth enabled / flow resumes)
6. Immediately disable Bluetooth again
7. Observe crash in Browser Process

The vulnerability originates in `TransactionImpl::AdapterPoweredChanged`, where a Bluetooth power state change triggers execution of a stored callback. The critical issue lies in the synchronous invocation of this callback:

```
std::move(callback_).Run(base::unexpected(SystemError::kLostPower));

```

This callback ultimately resolves the Digital Credentials request by calling back into `DigitalIdentityRequestImpl::CompleteRequest`, which leads to destruction of the `TransactionImpl` object (`provider_.reset()` → `TransactionImpl::~TransactionImpl`). Because the callback is executed synchronously, this destruction occurs **while still inside the `AdapterPoweredChanged` method**, resulting in a reentrant object lifetime violation.

Under normal conditions, this pattern is already unsafe because the method continues executing on a stack frame whose owning object (`this`) may have been freed. However, the issue becomes more pronounced under retry flows. When a user triggers a Digital Credentials request with Bluetooth disabled, an error is produced. Upon clicking “Try Again,” a new request flow is initialized, potentially reusing or overlapping internal state. If Bluetooth is then disabled again during this second execution, `AdapterPoweredChanged` is invoked in a context where previous teardown may still be in progress or partially completed.

This creates a **reentrant teardown scenario** where multiple destruction paths overlap. The destructor chain proceeds through:

- `TransactionImpl::~TransactionImpl`
- `RequestDispatcher::~RequestDispatcher`
- `Discovery::~Discovery`
- `BluetoothAdapterWinrt::~BluetoothAdapterWinrt`

During `BluetoothAdapterWinrt` destruction, the code attempts to unregister a Bluetooth radio state listener via:

```
TryRemoveRadioStateChangedHandler();

```

This eventually calls into the Windows Bluetooth COM layer:

```
ATL::IConnectionPointImpl<...>::Unadvise

```

At this point, the program crashes. The crash indicates that the COM connection point is in an invalid state—either due to double unregistration, use of a stale listener pointer, or inconsistent internal state caused by overlapping teardown. Since ATL connection points store raw interface pointers without strong lifetime guarantees, reentrant destruction can easily lead to dereferencing freed or invalid memory.

Although the current manifestation is a crash (BREAKPOINT in `BthRadioMedia.dll`), the underlying issue is a **lifetime violation caused by synchronous callback execution**, identical in nature to the previously reported use-after-free vulnerability. The original fix addressed asynchronous execution in one path but failed to account for this reentrant path triggered by Bluetooth state changes and retry flows.

In summary, the root cause is unsafe synchronous callback execution within `AdapterPoweredChanged`, allowing destruction of `TransactionImpl` during active method execution. This leads to inconsistent object state and ultimately causes a crash during COM listener unregistration. The bug represents an incomplete fix of the original vulnerability, with the same core issue—object lifetime mismanagement—still present under alternate execution paths.

---

```
KEY_VALUES_STRING: 1

    Key  : Analysis.CPU.mSec
    Value: 8000

    Key  : Analysis.Elapsed.mSec
    Value: 15521

    Key  : Analysis.IO.Other.Mb
    Value: 0

    Key  : Analysis.IO.Read.Mb
    Value: 4

    Key  : Analysis.IO.Write.Mb
    Value: 0

    Key  : Analysis.Init.CPU.mSec
    Value: 4656

    Key  : Analysis.Init.Elapsed.mSec
    Value: 5306

    Key  : Analysis.Memory.CommitPeak.Mb
    Value: 1725

    Key  : Analysis.Version.DbgEng
    Value: 10.0.29547.1002

    Key  : Analysis.Version.Description
    Value: 10.2602.27.2 amd64fre

    Key  : Analysis.Version.Ext
    Value: 1.2602.27.2

    Key  : Failure.Bucket
    Value: BREAKPOINT_80000003_BthRadioMedia.dll!ATL::IConnectionPointImpl_CBthRadioManager,_IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray_::Unadvise

    Key  : Failure.Exception.Code
    Value: 0x80000003

    Key  : Failure.Hash
    Value: {63fbc647-1b3c-4f88-e831-a46bf0c108a4}

    Key  : Failure.ProblemClass.Primary
    Value: BREAKPOINT

    Key  : Faulting.IP.Type
    Value: Null

    Key  : Timeline.OS.Boot.DeltaSec
    Value: 14002

    Key  : Timeline.Process.Start.DeltaSec
    Value: 865

    Key  : WER.OS.Branch
    Value: vb_release

    Key  : WER.OS.Version
    Value: 10.0.19041.1

    Key  : WER.Process.Version
    Value: 149.0.7793.0


FILE_IN_CAB:  chrome.exe_260417_181508.dmp

COMMENT:  
*** procdump  -ma 3824
*** Manual dump

NTGLOBALFLAG:  0

APPLICATION_VERIFIER_FLAGS:  0

EXCEPTION_RECORD:  (.exr -1)
ExceptionAddress: 0000000000000000
   ExceptionCode: 80000003 (Break instruction exception)
  ExceptionFlags: 00000000
NumberParameters: 0

FAULTING_THREAD:  1354

PROCESS_NAME:  chrome.exe

ERROR_CODE: (NTSTATUS) 0x80000003 - {EXCEPTION}  Breakpoint  A breakpoint has been reached.

EXCEPTION_CODE_STR:  80000003

CRITICAL_SECTION:  0000116226cea180 -- (!cs -s 0000116226cea180)

BLOCKING_THREAD:  269a36d0

STACK_TEXT:  
00000030`7cbfdca8 00007ffc`432f38ad     : 000011b6`28199b20 000011b6`27d6c9c0 0000113c`288130f0 0000113e`2a9c7a68 : ntdll!NtWaitForAlertByThreadId+0x14
00000030`7cbfdcb0 00007ffc`432f3762     : 00000000`00000000 00000000`00000000 00000030`7cbfdd98 000011b6`27cf5738 : ntdll!RtlpWaitOnAddressWithTimeout+0x81
00000030`7cbfdce0 00007ffc`432f357d     : 000011b6`27cf5730 00000000`00001722 00000000`00000000 00001162`26cea3b0 : ntdll!RtlpWaitOnAddress+0xae
00000030`7cbfdd50 00007ffc`432bfcb4     : 00000136`26980000 00000236`c4fdae60 00000000`fffffffa 00001162`26cea180 : ntdll!RtlpWaitOnCriticalSection+0xfd
00000030`7cbfde30 00007ffc`432bfae2     : 000011b6`27ed7300 000011b6`27ed7280 00000000`00000001 00007ffc`290d7d6e : ntdll!RtlpEnterCriticalSectionContended+0x1c4
00000030`7cbfde90 00007ffc`290dee50     : 0000078f`35bc37b3 00001162`26cea180 00001162`26cea320 00001150`27395cf8 : ntdll!RtlEnterCriticalSection+0x42
00000030`7cbfdec0 00007ffc`290def50     : 000011b6`27cf5708 00001150`27395cb0 000011b6`280bce00 00000000`00000000 : BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+0x34
00000030`7cbfdef0 00007ffc`3045640d     : 00000000`00000000 00000000`00000000 00001150`27395d10 000011b6`280bce00 : BthRadioMedia!CBthRadioManager::Unadvise+0x50
00000030`7cbfdf30 00007ffc`30457faf     : 000011b6`27cf5708 00000000`00000000 00000000`00000000 00000000`00000000 : Windows_Devices_Radios!RadioEventListener::UnregisterListener+0x49
00000030`7cbfdf60 00007ffb`c7c64b48     : 00001150`27395d10 00000030`7cbfdfc0 00000030`7cbfdff0 00000030`7cbfe010 : Windows_Devices_Radios!RadioImpl::remove_StateChanged+0xcf
00000030`7cbfdfa0 00007ffb`c7c63cd9     : 00000030`7cbfe120 0000113e`27242c90 00000236`c4ffffa0 000011b6`27fffd00 : chrome!device::BluetoothAdapterWinrt::TryRemoveRadioStateChangedHandler+0x178
00000030`7cbfe040 00007ffb`c7c8f240     : 00000030`7cbfd930 00000000`00000000 00001162`26cea188 00001162`26cea180 : chrome!device::BluetoothAdapterWinrt::~BluetoothAdapterWinrt+0x1e9
00000030`7cbfe170 00007ffb`c8bff18c     : 0000113a`2a2ed550 0000113a`2a2ed558 00000030`7cbfe238 00000136`26980000 : chrome!device::BluetoothAdapterWinrt::~BluetoothAdapterWinrt+0x10
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::RefCounted<device::BluetoothAdapter,base::DefaultRefCountedTraits<device::BluetoothAdapter> >::DeleteInternal+0x36
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::DefaultRefCountedTraits<device::BluetoothAdapter>::Destruct+0x36
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::RefCounted<device::BluetoothAdapter,base::DefaultRefCountedTraits<device::BluetoothAdapter> >::Release+0x5d
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!scoped_refptr<device::BluetoothAdapter>::Release+0x5d
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!scoped_refptr<device::BluetoothAdapter>::~scoped_refptr+0x80
00000030`7cbfe1b0 00007ffb`c8c067b0     : 00000000`00000001 00001152`3bfa03e0 000011b6`27fffc40 000011b6`28199128 : chrome!device::cablev2::Discovery::~Discovery+0x2ac
00000030`7cbfe210 00007ffb`b777e66c     : 00000030`7cbfe430 00001156`28bb31e0 00001162`26cea188 00001162`26cea180 : chrome!device::cablev2::Discovery::~Discovery+0x10
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::default_delete<device::FidoDiscoveryBase>::operator()+0x24
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<device::FidoDiscoveryBase,std::__Cr::default_delete<device::FidoDiscoveryBase> >::reset+0x40
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<device::FidoDiscoveryBase,std::__Cr::default_delete<device::FidoDiscoveryBase> >::~unique_ptr+0x40
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!content::digital_credentials::cross_device::RequestDispatcher::~RequestDispatcher+0x92
00000030`7cbfe250 00007ffb`b778143c     : 00000000`00000040 00007ffb`eadf9d20 00000136`26980000 000011b6`27d6c2e0 : chrome!content::digital_credentials::cross_device::RequestDispatcher::~RequestDispatcher+0x9c
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::default_delete<content::digital_credentials::cross_device::RequestDispatcher>::operator()+0x2e
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::digital_credentials::cross_device::RequestDispatcher,std::__Cr::default_delete<content::digital_credentials::cross_device::RequestDispatcher> >::reset+0x4f
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::digital_credentials::cross_device::RequestDispatcher,std::__Cr::default_delete<content::digital_credentials::cross_device::RequestDispatcher> >::~unique_ptr+0x4f
00000030`7cbfe290 00007ffb`b7785970     : 000011b6`28199100 00000136`26980000 00000000`00000001 00001158`2ba7fd80 : chrome!content::digital_credentials::cross_device::TransactionImpl::~TransactionImpl+0x18c
00000030`7cbfe2e0 00007ffb`bdb42206     : 000011b6`28199000 000011b6`28199240 000011b6`27d6c400 00007ffb`eadfaba7 : chrome!content::digital_credentials::cross_device::TransactionImpl::~TransactionImpl+0x10
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::default_delete<content::digital_credentials::cross_device::Transaction>::operator()+0x24
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::digital_credentials::cross_device::Transaction,std::__Cr::default_delete<content::digital_credentials::cross_device::Transaction> >::reset+0x40
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::digital_credentials::cross_device::Transaction,std::__Cr::default_delete<content::digital_credentials::cross_device::Transaction> >::~unique_ptr+0x40
00000030`7cbfe320 00007ffb`bdb4abf0     : 00000136`26980000 0000114c`2da15980 000011b6`27fffba0 000011b6`28199100 : chrome!DigitalIdentityProviderDesktop::~DigitalIdentityProviderDesktop+0x106
00000030`7cbfe360 00007ffb`b61f3632     : 0000113e`269a36d0 00000236`c4fad858 00000030`7cbfe410 00007ffb`c080ca5d : chrome!DigitalIdentityProviderDesktop::~DigitalIdentityProviderDesktop+0x10
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::default_delete<content::DigitalIdentityProvider>::operator()+0x30
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::DigitalIdentityProvider,std::__Cr::default_delete<content::DigitalIdentityProvider> >::reset+0x58
00000030`7cbfe3a0 00007ffb`b61f329e     : 000011b6`27fd7768 00007ffb`eae1b419 000011b6`27d07000 00000030`7cbfe4f0 : chrome!content::DigitalIdentityRequestImpl::CompleteRequestWithStatus+0x202
00000030`7cbfe480 00007ffb`b61fa9a0     : 000011b6`27edf880 00000136`2654f188 000011b6`27ed7028 000011b6`27ed7020 : chrome!content::DigitalIdentityRequestImpl::CompleteRequest+0x19e
00000030`7cbfe520 00007ffb`b61fa714     : 00000fff`7d3053b8 00007ffb`eae1b419 000011b6`27d07000 0000113c`291cdcd0 : chrome!base::internal::DecayedFunctorTraits<void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>::Invoke<void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),const base::WeakPtr<content::DigitalIdentityRequestImpl> &,base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics> >+0x1e0
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::DigitalIdentityRequestImpl::*&&)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>,void,0>::MakeItSo+0x64
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::Invoker<base::internal::FunctorTraits<void (content::DigitalIdentityRequestImpl::*&&)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>,base::internal::BindState<1,1,0,void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> >,void (base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>)>::RunImpl+0x7e
00000030`7cbfe5e0 00007ffb`bdb45ec8     : 00001160`269a2898 0000113a`269a0d90 00000030`7cbfe6f0 00007ffb`c087edcf : chrome!base::internal::Invoker<base::internal::FunctorTraits<void (content::DigitalIdentityRequestImpl::*&&)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>,base::internal::BindState<1,1,0,void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> >,void (base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>)>::RunOnce+0x144
(Inline Function) --------`--------     : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::OnceCallback<void (base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>)>::Run+0x8f
00000030`7cbfe680 00007ffb`bdb437e8     : 000011b6`27edf380 000011b6`27edf3a0 00000030`7cbfe7a0 00000030`7cbfe7a0 : chrome!DigitalIdentityProviderDesktop::EndRequestWithError+0x228
00000030`7cbfe740 00007ffb`bdb49802     : 00000136`26980000 00000026`c4ca9e31 000011b6`27ee01b0 000011b6`27ee0280 : chrome!DigitalIdentityProviderDesktop::OnFinished+0x218

STACK_COMMAND: ~0s; .ecxr ; kb

SYMBOL_NAME:  BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+34

MODULE_NAME: BthRadioMedia

IMAGE_NAME:  BthRadioMedia.dll

FAILURE_BUCKET_ID:  BREAKPOINT_80000003_BthRadioMedia.dll!ATL::IConnectionPointImpl_CBthRadioManager,_IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray_::Unadvise

OS_VERSION:  10.0.19041.1

BUILDLAB_STR:  vb_release

OSPLATFORM_TYPE:  x64

OSNAME:  Windows 10

IMAGE_VERSION:  6.2.19041.746

FAILURE_ID_HASH:  {63fbc647-1b3c-4f88-e831-a46bf0c108a4}

Followup:     MachineOwner
---------

0:000> !cs -s 0000116226cea180
-----------------------------------------
Critical section   = 0x0000116226cea180 (+0x116226CEA180)
DebugInfo          = 0x00007ffbe317d080
LOCKED
LockCount          = 0xFFFFFFFF
WaiterWoken        = Yes
OwningThread       = 0x0000113e269a36d0
RecursionCount     = 0xBEBEBEBE
LockSemaphore      = 0x2A2ED550
SpinCount          = 0x0000113a2a2ed550
ntdll!RtlpStackTraceDataBase is NULL. Probably the stack traces are not enabled.
0:000> lmvm BthRadioMedia
Browse full module list
start             end                 module name
00007ffc`290d0000 00007ffc`290ef000   BthRadioMedia   (pdb symbols)          C:\ProgramData\Dbg\sym\BthRadioMedia.pdb\0BD64DF67BB251C018DE698325D4CED81\BthRadioMedia.pdb
    Loaded symbol image file: BthRadioMedia.dll
    Image path: C:\Windows\System32\BthRadioMedia.dll
    Image name: BthRadioMedia.dll
    Browse all global symbols  functions  data  Symbol Reload
    Image was built with /Brepro flag.
    Timestamp:        CD2FAD7E (This is a reproducible build file hash, not a timestamp)
    CheckSum:         0001C4FF
    ImageSize:        0001F000
    Mapping Form:     Loaded
    File version:     6.2.19041.746
    Product version:  10.0.19041.746
    File flags:       0 (Mask 3F)
    File OS:          40004 NT Win32
    File type:        2.0 Dll
    File date:        00000000.00000000
    Translations:     0409.04b0
    Information from resource tables:
        CompanyName:      Microsoft Corporation
        ProductName:      Microsoft® Windows® Operating System
        InternalName:     BTHRADIOMEDIA
        OriginalFilename: BTHRADIOMEDIA.dll
        ProductVersion:   10.0.19041.746
        FileVersion:      10.0.19041.746 (WinBuild.160101.0800)
        FileDescription:  Bluetooth Radio Media Provider
        LegalCopyright:   © Microsoft Corporation. All rights reserved.

```
#### Impact analysis

crash

---

### The cause

#### What version of Chrome have you found the security issue in?

Chrome 149.0.7793.0 (Windows x64)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Remote Code Execution (RCE)

#### How would you like to be publicly acknowledged for your report?

sean wong

## Attachments

- [BTPoC.html](attachments/BTPoC.html) (text/html, 1.7 KB)
- [recording.mp4](attachments/recording.mp4) (video/mp4, 2.8 MB)

## Timeline

### ma...@google.com (2026-04-17)

This is lacking proof of a UaF bug, like I noted in your identical submission in <https://crbug.com/503731573>. Your log shows that you attached a debugger while the program was hanging, but I don't see any evidence of a UaF bug, or even a crash. If you can produce an ASAN log for this, feel free to resubmit.

This report does not provide enough information for us to quickly understand and
reproduce a problem. It will be closed as Won't Fix. Once you have gathered the
required information please open a new issue with a brief description that
attaches all necessary pocs, traces and patches as individual files.

In particular:

- attach a complete symbolized trace as `asan.log` including all additional information

For more information see: <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting>

### wo...@gmail.com (2026-04-17)

no debug was attached. i wish you could just watch the poc video and try
reproduce it. i have asan and it doesnt catch the the UAF or crash  because
the browser is dead/frozen i have to quit the browser manually. i used
procdump to capture the browser state when is frozen.

On Fri, Apr 17, 2026 at 9:27 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/503763493
>
> *Changed*
> status:  New → Not Reproducible
>
> *ma...@google.com <ma...@google.com> added comment #2
> <https://issues.chromium.org/issues/503763493#comment2>:*
>
> This is lacking proof of a UaF bug, like I noted in your identical
> submission in https://crbug.com/503731573. Your log shows that you
> attached a debugger while the program was hanging, but I don't see any
> evidence of a UaF bug, or even a crash. If you can produce an ASAN log for
> this, feel free to resubmit.
>
> This report does not provide enough information for us to quickly
> understand and reproduce a problem. It will be closed as Won't Fix. Once
> you have gathered the required information please open a new issue with a
> brief description that attaches all necessary pocs, traces and patches as
> individual files.
>
> In particular:
>
>    - attach a complete symbolized trace as asan.log including all
>    additional information
>
> For more information see:
> https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting
>
> _______________________________
>
> *Reference Info: 503763493 incomplete fix of 488617440*
> component:  Public Trackers > 1362134 > Chromium
> <https://issues.chromium.org/components/1363614>
> status:  Not Reproducible
> reporter:  wongsean926@gmail.com
> cc:  wongsean926@gmail.com
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P4
> severity:  S4
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>
> retention:  Component default
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you have the following role(s) on the
> issue: cc, reporter
> Unsubscribe from this issue
> <https://issues.chromium.org/issues/503763493?unsubscribe=true>.
>


### ch...@google.com (2026-04-17)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### wo...@gmail.com (2026-04-17)

you saying its not reproducible. send me a video of it failing to
reproduce. this is 100% reproducible in chrome   147.0.7727.102 (Official
Build) (64-bit) (cohort: Early Adopters)

On Fri, Apr 17, 2026 at 9:43 PM sean wong <wongsean926@gmail.com> wrote:

> no debug was attached. i wish you could just watch the poc video and try
> reproduce it. i have asan and it doesnt catch the the UAF or crash  because
> the browser is dead/frozen i have to quit the browser manually. i used
> procdump to capture the browser state when is frozen.
>
> On Fri, Apr 17, 2026 at 9:27 PM <buganizer-system@google.com> wrote:
>
>> Replying to this email means your email address will be shared with the
>> team that works on this product.
>> https://issues.chromium.org/issues/503763493
>>
>> *Changed*
>> status:  New → Not Reproducible
>>
>> *ma...@google.com <ma...@google.com> added comment #2
>> <https://issues.chromium.org/issues/503763493#comment2>:*
>>
>> This is lacking proof of a UaF bug, like I noted in your identical
>> submission in https://crbug.com/503731573. Your log shows that you
>> attached a debugger while the program was hanging, but I don't see any
>> evidence of a UaF bug, or even a crash. If you can produce an ASAN log for
>> this, feel free to resubmit.
>>
>> This report does not provide enough information for us to quickly
>> understand and reproduce a problem. It will be closed as Won't Fix. Once
>> you have gathered the required information please open a new issue with a
>> brief description that attaches all necessary pocs, traces and patches as
>> individual files.
>>
>> In particular:
>>
>>    - attach a complete symbolized trace as asan.log including all
>>    additional information
>>
>> For more information see:
>> https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting
>>
>> _______________________________
>>
>> *Reference Info: 503763493 incomplete fix of 488617440*
>> component:  Public Trackers > 1362134 > Chromium
>> <https://issues.chromium.org/components/1363614>
>> status:  Not Reproducible
>> reporter:  wongsean926@gmail.com
>> cc:  wongsean926@gmail.com
>> collaborators:  se...@chromium.org
>> type:  Vulnerability
>> access level:  Limited visibility
>> priority:  P4
>> severity:  S4
>> hotlist:  external_security_report
>> <https://issues.chromium.org/hotlists/5433527>
>> retention:  Component default
>>
>>
>> Generated by Google IssueTracker notification system.
>>
>> You're receiving this email because you have the following role(s) on the
>> issue: cc, reporter
>> Unsubscribe from this issue
>> <https://issues.chromium.org/issues/503763493?unsubscribe=true>.
>>
>


### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503763493)*
