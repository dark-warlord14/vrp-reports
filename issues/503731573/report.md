# Browser Process Heap-Use-After-Free in Digital Credentials API (Renderer → Browser Memory Corruption)

| Field | Value |
|-------|-------|
| **Issue ID** | [503731573](https://issues.chromium.org/issues/503731573) |
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

Incomplete Fix: Reentrant Teardown in Digital Credentials API Leads to Use-After-Free / Invalid Object Lifetime in Browser Process

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

content/browser/webid/digital\_credentials/

---

### The problem

#### Please describe the technical details of the vulnerability

**Previous Report Reference**
<https://issues.chromium.org/issues/488617440>

---

## Summary

The previously reported Browser Process heap-use-after-free in the Digital Credentials API was fixed by making error callbacks asynchronous. However, the fix does not fully address reentrant execution paths.

A new trigger sequence involving retry flows and Bluetooth state transitions leads to premature destruction of `TransactionImpl` and associated objects while they are still in use. This results in a crash during teardown and indicates that the original lifetime issue is not fully resolved.

The issue remains reachable from renderer-controlled input and still affects the Browser Process.

---

## Affected Component

content/browser/webid/digital\_credentials/
Specifically involving:

- `TransactionImpl`
- `RequestDispatcher`
- `Discovery`
- `BluetoothAdapterWinrt`

---

## Tested Version

Chrome 149.0.7793.0 (Windows x64)

---

## Vulnerability Type

- Incomplete Fix / Variant of Use-After-Free
- Cross-thread / reentrant object lifetime violation

---

## Root Cause Analysis

The original fix ensured that error callbacks were dispatched asynchronously to prevent immediate destruction of `TransactionImpl`.

However, a reentrant execution path remains:

1. A Digital Credentials request is initiated
2. Bluetooth is disabled → error path triggered
3. User clicks "Try Again" → request reinitializes
4. Bluetooth is disabled again during active flow
5. Teardown occurs while objects are still in use

This results in overlapping execution of:

- Active request flow
- Teardown/destructor chain

Leading to destruction of:

- `TransactionImpl`
- `RequestDispatcher`
- `Discovery`
- `BluetoothAdapterWinrt`

while dependent components are still executing.

---

## Crash Evidence

The crash occurs in the Browser Process during Bluetooth teardown:

- `BluetoothAdapterWinrt::~BluetoothAdapterWinrt`
- `Discovery::~Discovery`
- `TransactionImpl::~TransactionImpl`
- `DigitalIdentityProviderDesktop::~`

Eventually triggering a failure in:

- `BthRadioMedia.dll! ... Unadvise`

```
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

```

This indicates invalid object state or use of an already-destroyed COM listener during cleanup.

i havent attached the DMP file because is 7GB

---

#### Impact analysis

## Impact

Use-After-Free

---

## Conclusion

The fix for the original vulnerability does not fully address object lifetime issues under reentrant conditions. The retry + Bluetooth toggle flow exposes a remaining flaw that leads to invalid object destruction and potential memory safety violations in the Browser Process.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chrome 149.0.7793.0 (Windows x64)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Remote Code Execution (RCE)

#### How would you like to be publicly acknowledged for your report?

sean wong

## Attachments

- [recording.mp4](attachments/recording.mp4) (video/mp4, 2.8 MB)
- [crash.txt](attachments/crash.txt) (text/plain, 15.7 KB)
- [poc.html](attachments/poc.html) (text/html, 1.9 KB)

## Timeline

### wo...@gmail.com (2026-04-17)

0:000> x /D /d BthRadioMedia!a\*
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

00007ffc`290e2aa0 BthRadioMedia!ATL::CComClassFactory::`vftable' = <no type information>
00007ffc`290e2d70 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vftable' = <no type information>
00007ffc`290e2cf0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::`vftable' = <no type information>
00007ffc`290e9a50 BthRadioMedia!ATL::_AtlBaseModule = <no type information> 00007ffc`290e2ac8 BthRadioMedia!ATL::CComObjectCached[ATL::CComClassFactory](javascript:void(0);)::`vftable' = <no type information> 00007ffc`290e9b50 BthRadioMedia!ATL::g\_strmgr = <no type information>
00007ffc`290e2b70 BthRadioMedia!ATL::CWin32Heap::`vftable' = <no type information>
00007ffc`290e9120 BthRadioMedia!ATL::CAtlException` RTTI Type Descriptor' = <no type information>
00007ffc`290e2e28 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`vftable' = <no type information>
00007ffc`290e2e50 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`vftable' = <no type information>
00007ffc`290e9ce0 BthRadioMedia!ATL::_pPerfRegFunc = <no type information> 00007ffc`290e2ea8 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::`vftable' = <no type information> 00007ffc`290e9ab0 BthRadioMedia!ATL::\_AtlWinModule = <no type information>
00007ffc`290e9a00 BthRadioMedia!ATL::_AtlComModule = <no type information> 00007ffc`290e9b38 BthRadioMedia!ATL::g\_strheap = <no type information>
00007ffc`290e2d98 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vftable' = <no type information>
00007ffc`290e9980 BthRadioMedia!ATL::CAtlBaseModule::m_bInitFailed = <no type information> 00007ffc`290e9ce8 BthRadioMedia!ATL::\_pPerfUnRegFunc = <no type information>
00007ffc`290e2dd8 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vftable' = <no type information>
00007ffc`290e99a0 BthRadioMedia!ATL::IConnectionPointContainerImpl<CBthRadioManager>::pConnMap = <no type information> 00007ffc`290e2b40 BthRadioMedia!ATL::CAtlStringMgr::`vftable' = <no type information> 00007ffc`290e2d30 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::`vftable' = <no type information> 00007ffc`290e9978 BthRadioMedia!ATL::\_pAtlModule = <no type information>
0:000> x /D /f BthRadioMedia!a\*
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

00007ffc`290d5d64 BthRadioMedia!ATL::AtlFindExtension (void) 00007ffc`290d3ce0 BthRadioMedia!ATL::`dynamic atexit destructor for '_AtlBaseModule'' (void) 00007ffc`290d3d00 BthRadioMedia!ATL::`dynamic atexit destructor for 'g_strheap'' (void) 00007ffc`290d3cd0 BthRadioMedia!ATL::`dynamic atexit destructor for '_AtlComModule'' (void) 00007ffc`290d3d10 BthRadioMedia!ATL::`dynamic atexit destructor for 'g_strmgr'' (void) 00007ffc`290d11c0 BthRadioMedia!ATL::`dynamic initializer for '_AtlBaseModule'' (void) 00007ffc`290d11e0 BthRadioMedia!ATL::`dynamic initializer for '_AtlWinModule'' (void) 00007ffc`290d11a0 BthRadioMedia!ATL::`dynamic initializer for '_AtlComModule'' (void) 00007ffc`290d3cf0 BthRadioMedia!ATL::`dynamic atexit destructor for '_AtlWinModule'' (void) 00007ffc`290d1240 BthRadioMedia!ATL::`dynamic initializer for 'g_strmgr'' (void) 00007ffc`290d1200 BthRadioMedia!ATL::`dynamic initializer for 'g_strheap'' (void) 00007ffc`290d7af0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::QueryInterface (public: virtual long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::QueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d7030 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::EnumConnections (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::EnumConnections(struct IEnumConnections * *)) 00007ffc`290d5dc8 BthRadioMedia!ATL::AtlHresultFromLastError (long \_\_cdecl ATL::AtlHresultFromLastError(void))
00007ffc`290d37e0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::AddRef ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::AddRef`adjustor{32}' (void))
00007ffc`290d65c0 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA> >::Clone (public: virtual long __cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA> >::Clone(struct IEnumConnections * *)) 00007ffc`290d8148 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> >::Skip (public: virtual long \_\_cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >::Skip(unsigned long))
00007ffc`290d7574 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::Init (public: long __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::Init(struct IConnectionPoint * *,struct IConnectionPoint * *,struct IUnknown *,enum ATL::CComEnumFlags)) 00007ffc`290d5ac0 BthRadioMedia!ATL::CComObjectCached[ATL::CComClassFactory](javascript:void(0);)::AddRef (public: virtual unsigned long \_\_cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::AddRef(void))
00007ffc`290d12a0 BthRadioMedia!ATL::CAtlModule::Lock (public: virtual long __cdecl ATL::CAtlModule::Lock(void)) 00007ffc`290d52dc BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::~CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> (public: virtual \_\_cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::~CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>(void))
00007ffc`290d37f0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::QueryInterface ([thunk]:public: virtual long __cdecl ATL::CComObject<class CBthRadioManager>::QueryInterface`adjustor{32}' (struct \_GUID const &,void \* \*))
00007ffc`290d1320 BthRadioMedia!ATL::CAtlStringMgr::Clone (public: virtual struct ATL::IAtlStringMgr * __cdecl ATL::CAtlStringMgr::Clone(void)) 00007ffc`290d9ab4 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::~CSimpleStringT<unsigned short,0> (public: \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::~CSimpleStringT<unsigned short,0>(void))
00007ffc`290d84cc BthRadioMedia!ATL::_Copy<tagCONNECTDATA>::destroy (public: static void __cdecl ATL::_Copy<struct tagCONNECTDATA>::destroy(struct tagCONNECTDATA *)) 00007ffc`290d67f8 BthRadioMedia!ATL::CComCreator<ATL::CComObject<CBthRadioManager> >::CreateInstance (public: static long \_\_cdecl ATL::CComCreator<class ATL::CComObject<class CBthRadioManager> >::CreateInstance(void \*,struct \_GUID const &,void \* \*))
00007ffc`290d7820 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::Next (public: virtual long __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::Next(unsigned long,struct IConnectionPoint * *,unsigned long *)) 00007ffc`290de310 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::QueryInterface (public: virtual long \_\_cdecl ATL::CComObject<class CBthRadioInstance>::QueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d9c44 BthRadioMedia!ATL::AtlFindStringResourceInstance (struct HINSTANCE__ * __cdecl ATL::AtlFindStringResourceInstance(unsigned int,unsigned short)) 00007ffc`290e1840 BthRadioMedia!ATL::CAtlStringMgr::Free (public: virtual void \_\_cdecl ATL::CAtlStringMgr::Free(struct ATL::CStringData \*))
00007ffc`290d5270 BthRadioMedia!ATL::CComPtrBase<IUnknown>::CComPtrBase<IUnknown> (protected: __cdecl ATL::CComPtrBase<struct IUnknown>::CComPtrBase<struct IUnknown>(struct IUnknown *)) 00007ffc`290d98b4 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > > (public: \_\_cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >(unsigned short const \*))
00007ffc`290dbd10 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class CBthRadioInstance>::`vector deleting destructor'(unsigned int)) 00007ffc`290d84cc BthRadioMedia!ATL::\_CopyInterface<IConnectionPoint>::destroy (public: static void \_\_cdecl ATL::\_CopyInterface<struct IConnectionPoint>::destroy(struct IConnectionPoint \* \*))
00007ffc`290d9cf0 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::CheckImplicitLoad (private: bool __cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::CheckImplicitLoad(void const *)) 00007ffc`290d630c BthRadioMedia!ATL::AtlThrowImpl (void \_\_cdecl ATL::AtlThrowImpl(long))
00007ffc`290d3450 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Reset (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Reset(void)) 00007ffc`290d1330 BthRadioMedia!ATL::CAtlStringMgr::GetNilString (public: virtual struct ATL::CStringData \* \_\_cdecl ATL::CAtlStringMgr::GetNilString(void))
00007ffc`290d6c9c BthRadioMedia!ATL::CRegKey::DeleteSubKey (public: long __cdecl ATL::CRegKey::DeleteSubKey(unsigned short const *)) 00007ffc`290d9874 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::CSimpleStringT<unsigned short,0> (public: \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::CSimpleStringT<unsigned short,0>(struct ATL::IAtlStringMgr \*))
00007ffc`290d632c BthRadioMedia!ATL::AtlUnRegisterTypeLib (long __cdecl ATL::AtlUnRegisterTypeLib(struct HINSTANCE__ *,unsigned short const *)) 00007ffc`290d5a40 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::AddRef (public: virtual unsigned long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::AddRef(void))
00007ffc`290de420 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::QueryInterface (public: virtual long __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::QueryInterface(struct _GUID const &,void * *)) 00007ffc`290d7738 BthRadioMedia!ATL::CComCriticalSection::Init (public: long \_\_cdecl ATL::CComCriticalSection::Init(void))
00007ffc`290d9af8 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::operator= (public: class ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > > & __cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::operator=(char const *)) 00007ffc`290d1280 BthRadioMedia!ATL::CComCoClass<CBthRadioManager,&CLSID\_BthRadioManager>::GetObjectDescription (public: static unsigned short const \* \_\_cdecl ATL::CComCoClass<class CBthRadioManager,&struct \_GUID const CLSID\_BthRadioManager>::GetObjectDescription(void))
00007ffc`290d735c BthRadioMedia!ATL::CAtlComModule::ExecuteObjectMain (public: void __cdecl ATL::CAtlComModule::ExecuteObjectMain(bool)) 00007ffc`290d8488 BthRadioMedia!ATL::\_CopyInterface<IConnectionPoint>::copy (public: static long \_\_cdecl ATL::\_CopyInterface<struct IConnectionPoint>::copy(struct IConnectionPoint \* \*,struct IConnectionPoint \* \*))
00007ffc`290d8030 BthRadioMedia!ATL::CComObject<CBthRadioManager>::Release (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::Release(void)) 00007ffc`290d5f6c BthRadioMedia!ATL::AtlRegisterClassCategoriesHelper (long \_\_cdecl ATL::AtlRegisterClassCategoriesHelper(struct \_GUID const &,struct ATL::\_ATL\_CATMAP\_ENTRY const \*,int))
00007ffc`290d7490 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::GetConnectionInterface (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::GetConnectionInterface(struct _GUID *)) 00007ffc`290dbd10 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`scalar deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class CBthRadioInstance>::`scalar deleting destructor'(unsigned int))
00007ffc`290d63e8 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::Clone (public: virtual long __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::Clone(struct IEnumConnectionPoints * *)) 00007ffc`290dae64 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::SetString (public: void \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::SetString(unsigned short const \*,int))
00007ffc`290dbf00 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::AddRef (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::AddRef(void)) 00007ffc`290d3450 BthRadioMedia!ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Reset (public: virtual long \_\_cdecl ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Reset(void))
00007ffc`290e1920 BthRadioMedia!ATL::CWin32Heap::Reallocate (public: virtual void * __cdecl ATL::CWin32Heap::Reallocate(void *,unsigned __int64)) 00007ffc`290d1280 BthRadioMedia!ATL::CComObjectRootBase::GetCategoryMap (public: static struct ATL::\_ATL\_CATMAP\_ENTRY const \* \_\_cdecl ATL::CComObjectRootBase::GetCategoryMap(void))
00007ffc`290dac40 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::Reallocate (private: void __cdecl ATL::CSimpleStringT<unsigned short,0>::Reallocate(int)) 00007ffc`290d8188 BthRadioMedia!ATL::CAtlModuleT<CBthRadioModule>::UnregisterServer (public: long \_\_cdecl ATL::CAtlModuleT<class CBthRadioModule>::UnregisterServer(int,struct \_GUID const \*))
00007ffc`290d9d48 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::CloneData (private: static struct ATL::CStringData * __cdecl ATL::CSimpleStringT<unsigned short,0>::CloneData(struct ATL::CStringData *)) 00007ffc`290d5df0 BthRadioMedia!ATL::AtlLoadTypeLib (long **cdecl ATL::AtlLoadTypeLib(struct HINSTANCE** \*,unsigned short const \*,unsigned short \* \*,struct ITypeLib \* \*))
00007ffc`290d2d15 BthRadioMedia!amsg_exit (_amsg_exit) 00007ffc`290d5b1c BthRadioMedia!ATL::AtlCallTermFunc (void \_\_cdecl ATL::AtlCallTermFunc(struct ATL::\_ATL\_MODULE70 \*))
00007ffc`290d5890 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::`scalar deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::`scalar deleting destructor'(unsigned int)) 00007ffc`290d6a50 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::CreateInstance (public: static long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::CreateInstance(class ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> > \* \*))
00007ffc`290d32c0 BthRadioMedia!ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Clone (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Clone(struct IEnumConnections * *)) 00007ffc`290d552c BthRadioMedia!ATL::CComObject<CBthRadioManager>::~CComObject<CBthRadioManager> (public: virtual \_\_cdecl ATL::CComObject<class CBthRadioManager>::~CComObject<class CBthRadioManager>(void))
00007ffc`290e1790 BthRadioMedia!ATL::CAtlStringMgr::Allocate (public: virtual struct ATL::CStringData * __cdecl ATL::CAtlStringMgr::Allocate(int,int)) 00007ffc`290d34ac BthRadioMedia!ATL::CComMultiThreadModel::SafeDecrementReference (public: static unsigned long \_\_cdecl ATL::CComMultiThreadModel::SafeDecrementReference(long \*))
00007ffc`290d9c14 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::AllocSysString (public: unsigned short * __cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::AllocSysString(void)const ) 00007ffc`290d2bf8 BthRadioMedia!atexit (atexit)
00007ffc`290d5200 BthRadioMedia!ATL::CComObject<CBthRadioManager>::CComObject<CBthRadioManager> (public: __cdecl ATL::CComObject<class CBthRadioManager>::CComObject<class CBthRadioManager>(void *)) 00007ffc`290d3f0c BthRadioMedia!ATL::CComBSTR::~CComBSTR (public: \_\_cdecl ATL::CComBSTR::~CComBSTR(void))
00007ffc`290d3810 BthRadioMedia!ATL::CComObject<CBthRadioManager>::Release ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::Release`adjustor{32}' (void))
00007ffc`290d77b8 BthRadioMedia!ATL::InlineIsEqualUnknown (int __cdecl ATL::InlineIsEqualUnknown(struct _GUID const &)) 00007ffc`290d8100 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint> >::Skip (public: virtual long \_\_cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint> >::Skip(unsigned long))
00007ffc`290d5a80 BthRadioMedia!ATL::CComObject<CBthRadioManager>::AddRef (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::AddRef(void)) 00007ffc`290d8330 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::\_LocCPQueryInterface (public: virtual long \_\_cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct \_GUID const IID\_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::\_LocCPQueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d323c BthRadioMedia!ATL::CComAutoCriticalSection::~CComAutoCriticalSection (public: __cdecl ATL::CComAutoCriticalSection::~CComAutoCriticalSection(void)) 00007ffc`290d12c0 BthRadioMedia!ATL::CComObjectRootBase::ObjectMain (public: static void \_\_cdecl ATL::CComObjectRootBase::ObjectMain(bool))
00007ffc`290d31e8 BthRadioMedia!ATL::CComAutoCriticalSection::CComAutoCriticalSection (public: __cdecl ATL::CComAutoCriticalSection::CComAutoCriticalSection(void)) 00007ffc`290d4f70 BthRadioMedia!ATL::AtlAdd<unsigned \_\_int64> (long \_\_cdecl ATL::AtlAdd<unsigned \_\_int64>(unsigned \_\_int64 \*,unsigned \_\_int64,unsigned \_\_int64))
00007ffc`290d3840 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::Release ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstance>::Release`adjustor{8}' (void))
00007ffc`290d3820 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::AddRef ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstance>::AddRef`adjustor{8}' (void))
00007ffc`290d73b0 BthRadioMedia!ATL::IConnectionPointContainerImpl<CBthRadioManager>::FindConnectionPoint (public: virtual long __cdecl ATL::IConnectionPointContainerImpl<class CBthRadioManager>::FindConnectionPoint(struct _GUID const &,struct IConnectionPoint * *)) 00007ffc`290dac94 BthRadioMedia!ATL::CStringData::Release (public: void \_\_cdecl ATL::CStringData::Release(void))
00007ffc`290d7a94 BthRadioMedia!ATL::CRegKey::QueryDWORDValue (public: long __cdecl ATL::CRegKey::QueryDWORDValue(unsigned short const *,unsigned long &)) 00007ffc`290deaa0 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::Release (public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioInstance>::Release(void))
00007ffc`290d5890 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::`vector deleting destructor'(unsigned int)) 00007ffc`290e1820 BthRadioMedia!ATL::CWin32Heap::Allocate (public: virtual void \* \_\_cdecl ATL::CWin32Heap::Allocate(unsigned \_\_int64))
00007ffc`290d3550 BthRadioMedia!ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Skip (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Skip(unsigned long)) 00007ffc`290d6b48 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::CreateInstance (public: static long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::CreateInstance(class ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> > \* \*))
00007ffc`290d7d10 BthRadioMedia!ATL::CComObject<CBthRadioManager>::QueryInterface (public: virtual long __cdecl ATL::CComObject<class CBthRadioManager>::QueryInterface(struct _GUID const &,void * *)) 00007ffc`290e1890 BthRadioMedia!ATL::CWin32Heap::GetSize (public: virtual unsigned \_\_int64 \_\_cdecl ATL::CWin32Heap::GetSize(void \*))
00007ffc`290daf48 BthRadioMedia!ATL::_AtlGetStringResourceImage (struct ATL::ATLSTRINGRESOURCEIMAGE const * __cdecl ATL::_AtlGetStringResourceImage(struct HINSTANCE__ *,struct HRSRC__ *,unsigned int)) 00007ffc`290d77f0 BthRadioMedia!ATL::CComClassFactory::LockServer (public: virtual long \_\_cdecl ATL::CComClassFactory::LockServer(int))
00007ffc`290d13c4 BthRadioMedia!ATL::CAtlBaseModule::CAtlBaseModule (public: __cdecl ATL::CAtlBaseModule::CAtlBaseModule(void)) 00007ffc`290d12d0 BthRadioMedia!ATL::CAtlModule::Unlock (public: virtual long \_\_cdecl ATL::CAtlModule::Unlock(void))
00007ffc`290d17c4 BthRadioMedia!ATL::CAtlBaseModule::~CAtlBaseModule (public: __cdecl ATL::CAtlBaseModule::~CAtlBaseModule(void)) 00007ffc`290d5a10 BthRadioMedia!ATL::CAtlModuleT<CBthRadioModule>::AddCommonRGSReplacements (public: virtual long \_\_cdecl ATL::CAtlModuleT<class CBthRadioModule>::AddCommonRGSReplacements(struct IRegistrarBase \*))
00007ffc`290dbec0 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::AddRef (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstance>::AddRef(void)) 00007ffc`290d80b0 BthRadioMedia!ATL::CComObjectCached[ATL::CComClassFactory](javascript:void(0);)::Release (public: virtual unsigned long \_\_cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::Release(void))
00007ffc`290d77e4 BthRadioMedia!ATL::CComObjectRootEx<ATL::CComMultiThreadModel>::InternalRelease (public: unsigned long __cdecl ATL::CComObjectRootEx<class ATL::CComMultiThreadModel>::InternalRelease(void)) 00007ffc`290d146c BthRadioMedia!ATL::CAtlWinModule::CAtlWinModule (public: \_\_cdecl ATL::CAtlWinModule::CAtlWinModule(void))
00007ffc`290d6c40 BthRadioMedia!ATL::CComClassFactory::CreateInstance (public: virtual long __cdecl ATL::CComClassFactory::CreateInstance(struct IUnknown *,struct _GUID const &,void * *)) 00007ffc`290d5d18 BthRadioMedia!ATL::AtlCrtErrorCheck (int \_\_cdecl ATL::AtlCrtErrorCheck(int))
00007ffc`290d1778 BthRadioMedia!ATL::CAtlWinModule::~CAtlWinModule (public: __cdecl ATL::CAtlWinModule::~CAtlWinModule(void)) 00007ffc`290d33c0 BthRadioMedia!ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Next (public: virtual long \_\_cdecl ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Next(unsigned long,struct tagCONNECTDATA \*,unsigned long \*))
00007ffc`290d7e10 BthRadioMedia!ATL::CComObjectCached<ATL::CComClassFactory>::QueryInterface (public: virtual long __cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::QueryInterface(struct _GUID const &,void * *)) 00007ffc`290dbd50 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::`scalar deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::`scalar deleting destructor'(unsigned int))
00007ffc`290d52a4 BthRadioMedia!ATL::_ATL_SAFE_ALLOCA_IMPL::CAtlSafeAllocBufferManager<ATL::CCRTAllocator>::~CAtlSafeAllocBufferManager<ATL::CCRTAllocator> (public: __cdecl ATL::_ATL_SAFE_ALLOCA_IMPL::CAtlSafeAllocBufferManager<class ATL::CCRTAllocator>::~CAtlSafeAllocBufferManager<class ATL::CCRTAllocator>(void)) 00007ffc`290dc0fc BthRadioMedia!ATL::CComObject<CBthRadioInstance>::CreateInstance (public: static long \_\_cdecl ATL::CComObject<class CBthRadioInstance>::CreateInstance(class ATL::CComObject<class CBthRadioInstance> \* \*))
00007ffc`290d6798 BthRadioMedia!ATL::CRegKey::Close (public: long __cdecl ATL::CRegKey::Close(void)) 00007ffc`290e1860 BthRadioMedia!ATL::CWin32Heap::Free (public: virtual void \_\_cdecl ATL::CWin32Heap::Free(void \*))
00007ffc`290d12c0 BthRadioMedia!ATL::CComCriticalSection::~CComCriticalSection (public: __cdecl ATL::CComCriticalSection::~CComCriticalSection(void)) 00007ffc`290e16cc BthRadioMedia!ATL::CSimpleArray<unsigned short,ATL::CSimpleArrayEqualHelper<unsigned short> >::RemoveAll (public: void \_\_cdecl ATL::CSimpleArray<unsigned short,class ATL::CSimpleArrayEqualHelper<unsigned short> >::RemoveAll(void))
00007ffc`290d9de0 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::Empty (public: void __cdecl ATL::CSimpleStringT<unsigned short,0>::Empty(void)) 00007ffc`290dbf3c BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Advise (public: virtual long \_\_cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct \_GUID const IID\_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::Advise(struct IUnknown \*,unsigned long \*))
00007ffc`290d58d0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`scalar deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class CBthRadioManager>::`scalar deleting destructor'(unsigned int)) 00007ffc`290db818 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::~CComObject<CBthRadioInstance> (public: virtual \_\_cdecl ATL::CComObject<class CBthRadioInstance>::~CComObject<class CBthRadioInstance>(void))
00007ffc`290dacc4 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::SetLength (private: void __cdecl ATL::CSimpleStringT<unsigned short,0>::SetLength(int)) 00007ffc`290d54bc BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::~CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> > (public: virtual \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::~CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >(void))
00007ffc`290da038 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::Fork (private: void __cdecl ATL::CSimpleStringT<unsigned short,0>::Fork(int)) 00007ffc`290d1648 BthRadioMedia!ATL::CWin32Heap::~CWin32Heap (public: virtual \_\_cdecl ATL::CWin32Heap::~CWin32Heap(void))
00007ffc`290d1290 BthRadioMedia!ATL::CAtlModule::GetLockCount (public: virtual long __cdecl ATL::CAtlModule::GetLockCount(void)) 00007ffc`290dabd4 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::PrepareWrite2 (private: void \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::PrepareWrite2(int))
00007ffc`290d8444 BthRadioMedia!ATL::_Copy<tagCONNECTDATA>::copy (public: static long __cdecl ATL::_Copy<struct tagCONNECTDATA>::copy(struct tagCONNECTDATA *,struct tagCONNECTDATA const *)) 00007ffc`290d9ab4 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::~CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > > (public: \_\_cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::~CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >(void))
00007ffc`290d7f18 BthRadioMedia!ATL::CAtlModuleT<CBthRadioModule>::RegisterServer (public: long __cdecl ATL::CAtlModuleT<class CBthRadioModule>::RegisterServer(int,struct _GUID const *)) 00007ffc`290dbd50 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::`vector deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::`vector deleting destructor'(unsigned int))
00007ffc`290d34e0 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Skip (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Skip(unsigned long)) 00007ffc`290d5594 BthRadioMedia!ATL::CComObjectRootEx[ATL::CComMultiThreadModel](javascript:void(0);)::~CComObjectRootEx[ATL::CComMultiThreadModel](javascript:void(0);) (public: \_\_cdecl ATL::CComObjectRootEx<class ATL::CComMultiThreadModel>::~CComObjectRootEx<class ATL::CComMultiThreadModel>(void))
00007ffc`290dbd90 BthRadioMedia!ATL::CComDynamicUnkArray::Add (public: unsigned long __cdecl ATL::CComDynamicUnkArray::Add(struct IUnknown *)) 00007ffc`290d531c BthRadioMedia!ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::~CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> (public: virtual \_\_cdecl ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::~CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>(void))
00007ffc`290d76f8 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA> >::Init (public: long __cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA> >::Init(struct tagCONNECTDATA *,struct tagCONNECTDATA *,struct IUnknown *,enum ATL::CComEnumFlags)) 00007ffc`290d4f94 BthRadioMedia!ATL::AtlMultiply<unsigned \_\_int64> (long \_\_cdecl ATL::AtlMultiply<unsigned \_\_int64>(unsigned \_\_int64 \*,unsigned \_\_int64,unsigned \_\_int64))
00007ffc`290dc1f4 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::CreateInstance (public: static long __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::CreateInstance(class ATL::CComObject<class CBthRadioInstanceCollection> * *)) 00007ffc`290db55c BthRadioMedia!ATL::CComObject<CBthRadioInstance>::CComObject<CBthRadioInstance> (public: \_\_cdecl ATL::CComObject<class CBthRadioInstance>::CComObject<class CBthRadioInstance>(void \*))
00007ffc`290d50e4 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> > (public: __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >(void *)) 00007ffc`290deb20 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::Release (public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioInstanceCollection>::Release(void))
00007ffc`290d58d0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class CBthRadioManager>::`vector deleting destructor'(unsigned int)) 00007ffc`290d544c BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::~CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> > (public: virtual \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::~CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >(void))
00007ffc`290d67d0 BthRadioMedia!ATL::CComCreator2<ATL::CComCreator<ATL::CComObject<CBthRadioManager> >,ATL::CComFailCreator<-2147221232> >::CreateInstance (public: static long __cdecl ATL::CComCreator2<class ATL::CComCreator<class ATL::CComObject<class CBthRadioManager> >,class ATL::CComFailCreator<-2147221232> >::CreateInstance(void *,struct _GUID const &,void * *)) 00007ffc`290d4fc8 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> > (public: \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >(void \*))
00007ffc`290d6920 BthRadioMedia!ATL::CComCreator<ATL::CComObjectCached<ATL::CComClassFactory> >::CreateInstance (public: static long __cdecl ATL::CComCreator<class ATL::CComObjectCached<class ATL::CComClassFactory> >::CreateInstance(void *,struct _GUID const &,void * *)) 00007ffc`290e18b0 BthRadioMedia!ATL::CAtlStringMgr::Reallocate (public: virtual struct ATL::CStringData \* \_\_cdecl ATL::CAtlStringMgr::Reallocate(struct ATL::CStringData \*,int,int))
00007ffc`290d535c BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::~CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> > (public: virtual __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::~CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >(void)) 00007ffc`290d74f0 BthRadioMedia!ATL::CAtlModule::GetGITPtr (public: virtual long \_\_cdecl ATL::CAtlModule::GetGITPtr(struct IGlobalInterfaceTable \* \*))
00007ffc`290d7a38 BthRadioMedia!ATL::CRegKey::Open (public: long __cdecl ATL::CRegKey::Open(struct HKEY__ *,unsigned short const *,unsigned long)) 00007ffc`290d5850 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::`vector deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::`vector deleting destructor'(unsigned int))
00007ffc`290d7fb0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::Release (public: virtual unsigned long __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::Release(void)) 00007ffc`290d5810 BthRadioMedia!ATL::CRegKey::~CRegKey (public: \_\_cdecl ATL::CRegKey::~CRegKey(void))
00007ffc`290d6db0 BthRadioMedia!ATL::IConnectionPointContainerImpl<CBthRadioManager>::EnumConnectionPoints (public: virtual long __cdecl ATL::IConnectionPointContainerImpl<class CBthRadioManager>::EnumConnectionPoints(struct IEnumConnectionPoints * *)) 00007ffc`290d3780 BthRadioMedia!alloca\_probe (\_alloca\_probe)
00007ffc`290daf30 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::ThrowMemoryException (protected: static void __cdecl ATL::CSimpleStringT<unsigned short,0>::ThrowMemoryException(void)) 00007ffc`290d3800 BthRadioMedia!ATL::CComObject<CBthRadioManager>::Release ([thunk]:public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioManager>::Release`adjustor{8}' (void)) 00007ffc`290e1710 BthRadioMedia!ATL::CAtlStringMgr::`vector deleting destructor' (public: virtual void * __cdecl ATL::CAtlStringMgr::`vector deleting destructor'(unsigned int))
00007ffc`290d581c BthRadioMedia!ATL::CComPtr<IMediaRadioManagerNotifySink>::~CComPtr<IMediaRadioManagerNotifySink> (public: __cdecl ATL::CComPtr<struct IMediaRadioManagerNotifySink>::~CComPtr<struct IMediaRadioManagerNotifySink>(void)) 00007ffc`290daaf8 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::LoadStringW (public: int **cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::LoadStringW(struct HINSTANCE** \*,unsigned int))
00007ffc`290e1750 BthRadioMedia!ATL::CWin32Heap::`scalar deleting destructor' (public: virtual void \* **cdecl ATL::CWin32Heap::`scalar deleting destructor'(unsigned int)) 00007ffc`290e163c BthRadioMedia!ATL::CAtlBaseModule::GetHInstanceAt (public: struct HINSTANCE** \* \_\_cdecl ATL::CAtlBaseModule::GetHInstanceAt(int))
00007ffc`290d3830 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::QueryInterface ([thunk]:public: virtual long __cdecl ATL::CComObject<class CBthRadioInstance>::QueryInterface`adjustor{8}' (struct \_GUID const &,void \* \*))
00007ffc`290db5c0 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::CComObject<CBthRadioInstanceCollection> (public: __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::CComObject<class CBthRadioInstanceCollection>(void *)) 00007ffc`290d7c00 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::QueryInterface (public: virtual long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::QueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d5270 BthRadioMedia!ATL::CComPtrBase<CBthRadioInstance>::CComPtrBase<CBthRadioInstance> (protected: __cdecl ATL::CComPtrBase<class CBthRadioInstance>::CComPtrBase<class CBthRadioInstance>(class CBthRadioInstance *)) 00007ffc`290d14e0 BthRadioMedia!ATL::CAtlStringMgr::CAtlStringMgr (public: \_\_cdecl ATL::CAtlStringMgr::CAtlStringMgr(struct ATL::IAtlMemMgr \*))
00007ffc`290d5910 BthRadioMedia!ATL::CComObjectCached<ATL::CComClassFactory>::`scalar deleting destructor' (public: void \* \_\_cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::`scalar deleting destructor'(unsigned int)) 00007ffc`290d5850 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::`scalar deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::`scalar deleting destructor'(unsigned int))
00007ffc`290d55c0 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::~IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray> (public: __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::~IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>(void)) 00007ffc`290d3330 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Next (public: virtual long \_\_cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Next(unsigned long,struct IConnectionPoint \* \*,unsigned long \*))
00007ffc`290d74c0 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::GetConnectionPointContainer (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::GetConnectionPointContainer(struct IConnectionPointContainer * *)) 00007ffc`290d5cbc BthRadioMedia!ATL::AtlComPtrAssign (struct IUnknown \* \_\_cdecl ATL::AtlComPtrAssign(struct IUnknown \* \*,struct IUnknown \*))
00007ffc`290d8224 BthRadioMedia!ATL::_ATL_SAFE_ALLOCA_IMPL::_AtlVerifyStackAvailable (bool __cdecl ATL::_ATL_SAFE_ALLOCA_IMPL::_AtlVerifyStackAvailable(unsigned __int64)) 00007ffc`290d792c BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> >::Next (public: virtual long \_\_cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >::Next(unsigned long,struct tagCONNECTDATA \*,unsigned long \*))
00007ffc`290dee1c BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::Unadvise(unsigned long)) 00007ffc`290d37d0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::AddRef ([thunk]:public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioManager>::AddRef`adjustor{8}' (void)) 00007ffc`290d53d4 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> >::~CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> > (public: virtual \_\_cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >::~CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >(void))
00007ffc`290d3250 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Clone (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Clone(struct IEnumConnectionPoints * *)) 00007ffc`290d1340 BthRadioMedia!ATL::CAtlComModule::CAtlComModule (public: \_\_cdecl ATL::CAtlComModule::CAtlComModule(void))
00007ffc`290d16f4 BthRadioMedia!ATL::CAtlComModule::~CAtlComModule (public: __cdecl ATL::CAtlComModule::~CAtlComModule(void)) 00007ffc`290d5b9c BthRadioMedia!ATL::AtlComModuleGetClassObject (long \_\_cdecl ATL::AtlComModuleGetClassObject(struct ATL::\_ATL\_COM\_MODULE70 \*,struct \_GUID const &,struct \_GUID const &,void \* \*))
00007ffc`290e1710 BthRadioMedia!ATL::CAtlStringMgr::`scalar deleting destructor' (public: virtual void \* \_\_cdecl ATL::CAtlStringMgr::`scalar deleting destructor'(unsigned int)) 00007ffc`290d5a40 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::AddRef (public: virtual unsigned long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::AddRef(void))
00007ffc`290db8b4 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::~CComObject<CBthRadioInstanceCollection> (public: virtual __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::~CComObject<class CBthRadioInstanceCollection>(void)) 00007ffc`290d7fb0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::Release (public: virtual unsigned long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::Release(void))
00007ffc`290e1750 BthRadioMedia!ATL::CWin32Heap::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CWin32Heap::`vector deleting destructor'(unsigned int))

### wo...@gmail.com (2026-04-17)

The crash occurs during COM connection point unregistration (Unadvise), indicating that a previously registered listener is being removed after its lifetime has ended or while the container is in an inconsistent state.

### wo...@gmail.com (2026-04-17)

sorry i forgot to attach the html.

## Reproduction Steps

1. Launch Chrome
2. Load the PoC page
3. Ensure Bluetooth is disabled
4. Trigger Digital Credentials request → error UI shown
5. Click "Try Again" (Bluetooth enabled / flow resumes)
6. Disable Bluetooth again
7. Observe crash in Browser Process

### ma...@google.com (2026-04-17)

We require a full asan log for UaF bugs.

This report does not provide enough information for us to quickly understand and
reproduce a problem. It will be closed as Won't Fix. Once you have gathered the
required information please open a new issue with a brief description that
attaches all necessary pocs, traces and patches as individual files.

In particular:

- attach a complete symbolized trace as `asan.log` including all additional information

For more information see: <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting>

### wo...@gmail.com (2026-04-17)

but the first report was accepted with dmp file and is the same report.

### wo...@gmail.com (2026-04-17)

asan doesnt record the crash because the browser freezes thats whz i used procdump to capture the crash

### wo...@gmail.com (2026-04-17)

its the same problem as <https://issues.chromium.org/issues/488617440>

### wo...@gmail.com (2026-04-17)

kindly cc [mamir@chromium.org](mailto:mamir@chromium.org)

### ch...@google.com (2026-04-17)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503731573)*
