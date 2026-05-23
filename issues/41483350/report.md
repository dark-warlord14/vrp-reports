# Security: Heap-use-after-free in Accessibility

| Field | Value |
|-------|-------|
| **Issue ID** | [41483350](https://issues.chromium.org/issues/41483350) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Accessibility |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2023-12-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: gs://chromium-browser-asan/linux-debug/asan-linux-debug-1236152.zip  

Operating System: ubuntu 2204

**REPRODUCTION CASE**

1. launch chrome
2. go to chrome://accessibility/
3. click 'Start Recording' button
4. click 'Web Accessibility' checkbox

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

asan log

=================================================================  

==92476==ERROR: AddressSanitizer: heap-use-after-free on address 0x5130000f76c0 at pc 0x7f39a63a7ecf bp 0x7fff8d67b690 sp 0x7fff8d67b688  

READ of size 1 at 0x5130000f76c0 thread T0 (chrome)  

==92476==WARNING: invalid path to external symbolizer!  

==92476==WARNING: Failed to use and restart external symbolizer!  

#0 0x7f39a63a7ece (/home/ttt/asan/libbase.so+0xba7ece) (BuildId: 2ea62f5ae37135e0)  

#1 0x7f39a63a794f (/home/ttt/asan/libbase.so+0xba794f) (BuildId: 2ea62f5ae37135e0)  

#2 0x7f39511b150f (/home/ttt/asan/libaccessibility\_platform.so+0x5b150f) (BuildId: 03371261e9965fb1)  

#3 0x7f39511b14c9 (/home/ttt/asan/libaccessibility\_platform.so+0x5b14c9) (BuildId: 03371261e9965fb1)  

#4 0x7f39511aac54 (/home/ttt/asan/libaccessibility\_platform.so+0x5aac54) (BuildId: 03371261e9965fb1)  

#5 0x7f39511a5dda (/home/ttt/asan/libaccessibility\_platform.so+0x5a5dda) (BuildId: 03371261e9965fb1)  

#6 0x7f39511a5758 (/home/ttt/asan/libaccessibility\_platform.so+0x5a5758) (BuildId: 03371261e9965fb1)  

#7 0x7f392c0929ce (/lib/x86\_64-linux-gnu/libgobject-2.0.so.0+0x309ce) (BuildId: 7c47809b4e688382aab4127a2e07496450c5e6b0)

0x5130000f76c0 is located 0 bytes inside of 368-byte region [0x5130000f76c0,0x5130000f7830)  

freed by thread T0 (chrome) here:  

#0 0x55e916a5936d (/home/ttt/asan/chrome+0xcc3636d) (BuildId: 1873399a7f82f58a)  

#1 0x7f39916ab7a1 (/home/ttt/asan/libcontent.so+0xfeab7a1) (BuildId: 9dcb118d5a6da423)  

#2 0x7f398fa84a92 (/home/ttt/asan/libcontent.so+0xe284a92) (BuildId: 9dcb118d5a6da423)  

#3 0x7f398f9bb24f (/home/ttt/asan/libcontent.so+0xe1bb24f) (BuildId: 9dcb118d5a6da423)  

#4 0x7f398f972c66 (/home/ttt/asan/libcontent.so+0xe172c66) (BuildId: 9dcb118d5a6da423)  

#5 0x7f398f8e39b5 (/home/ttt/asan/libcontent.so+0xe0e39b5) (BuildId: 9dcb118d5a6da423)  

#6 0x7f398f8e1e4f (/home/ttt/asan/libcontent.so+0xe0e1e4f) (BuildId: 9dcb118d5a6da423)  

#7 0x7f398f7ceee8 (/home/ttt/asan/libcontent.so+0xdfceee8) (BuildId: 9dcb118d5a6da423)  

#8 0x7f398f8f33ce (/home/ttt/asan/libcontent.so+0xe0f33ce) (BuildId: 9dcb118d5a6da423)  

#9 0x7f398f8ee8d9 (/home/ttt/asan/libcontent.so+0xe0ee8d9) (BuildId: 9dcb118d5a6da423)  

#10 0x7f398fa5c182 (/home/ttt/asan/libcontent.so+0xe25c182) (BuildId: 9dcb118d5a6da423)  

#11 0x7f398fa5bdd0 (/home/ttt/asan/libcontent.so+0xe25bdd0) (BuildId: 9dcb118d5a6da423)  

#12 0x7f398fa5b9a5 (/home/ttt/asan/libcontent.so+0xe25b9a5) (BuildId: 9dcb118d5a6da423)  

#13 0x7f398fa5b7f8 (/home/ttt/asan/libcontent.so+0xe25b7f8) (BuildId: 9dcb118d5a6da423)  

#14 0x7f39893e440e (/home/ttt/asan/libcontent.so+0x7be440e) (BuildId: 9dcb118d5a6da423)  

#15 0x7f39893d7ee4 (/home/ttt/asan/libcontent.so+0x7bd7ee4) (BuildId: 9dcb118d5a6da423)  

#16 0x7f3999f2246e (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x12246e) (BuildId: 7af4b8f1c9110ade)  

#17 0x7f3999f20e28 (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x120e28) (BuildId: 7af4b8f1c9110ade)  

#18 0x7f3999f6c8db (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x16c8db) (BuildId: 7af4b8f1c9110ade)  

#19 0x7f3999f2827c (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x12827c) (BuildId: 7af4b8f1c9110ade)  

#20 0x7f397db7b9e1 (/home/ttt/asan/libipc.so+0x17b9e1) (BuildId: 06b96c6bc00843bd)  

#21 0x7f397db80c39 (/home/ttt/asan/libipc.so+0x180c39) (BuildId: 06b96c6bc00843bd)  

#22 0x7f397db80938 (/home/ttt/asan/libipc.so+0x180938) (BuildId: 06b96c6bc00843bd)  

#23 0x7f397db8059e (/home/ttt/asan/libipc.so+0x18059e) (BuildId: 06b96c6bc00843bd)  

#24 0x7f397db803e8 (/home/ttt/asan/libipc.so+0x1803e8) (BuildId: 06b96c6bc00843bd)  

#25 0x7f39a6206cc4 (/home/ttt/asan/libbase.so+0xa06cc4) (BuildId: 2ea62f5ae37135e0)  

#26 0x7f39a6806560 (/home/ttt/asan/libbase.so+0x1006560) (BuildId: 2ea62f5ae37135e0)  

#27 0x7f39a69405e5 (/home/ttt/asan/libbase.so+0x11405e5) (BuildId: 2ea62f5ae37135e0)  

#28 0x7f39a693f06e (/home/ttt/asan/libbase.so+0x113f06e) (BuildId: 2ea62f5ae37135e0)  

#29 0x7f39a693d274 (/home/ttt/asan/libbase.so+0x113d274) (BuildId: 2ea62f5ae37135e0)

previously allocated by thread T0 (chrome) here:  

#0 0x55e916a58b0d (/home/ttt/asan/chrome+0xcc35b0d) (BuildId: 1873399a7f82f58a)  

#1 0x7f39916aad8c (/home/ttt/asan/libcontent.so+0xfeaad8c) (BuildId: 9dcb118d5a6da423)  

#2 0x7f398f9145b3 (/home/ttt/asan/libcontent.so+0xe1145b3) (BuildId: 9dcb118d5a6da423)  

#3 0x7f3990d1ca48 (/home/ttt/asan/libcontent.so+0xf51ca48) (BuildId: 9dcb118d5a6da423)  

#4 0x7f3990d1a2ae (/home/ttt/asan/libcontent.so+0xf51a2ae) (BuildId: 9dcb118d5a6da423)  

#5 0x55e9257ecab7 (/home/ttt/asan/chrome+0x1b9c9ab7) (BuildId: 1873399a7f82f58a)  

#6 0x55e9257f6898 (/home/ttt/asan/chrome+0x1b9d3898) (BuildId: 1873399a7f82f58a)  

#7 0x55e9257f6492 (/home/ttt/asan/chrome+0x1b9d3492) (BuildId: 1873399a7f82f58a)  

#8 0x55e9257f6144 (/home/ttt/asan/chrome+0x1b9d3144) (BuildId: 1873399a7f82f58a)  

#9 0x55e9257f5fc0 (/home/ttt/asan/chrome+0x1b9d2fc0) (BuildId: 1873399a7f82f58a)  

#10 0x7f399138600c (/home/ttt/asan/libcontent.so+0xfb8600c) (BuildId: 9dcb118d5a6da423)  

#11 0x7f3991383d36 (/home/ttt/asan/libcontent.so+0xfb83d36) (BuildId: 9dcb118d5a6da423)  

#12 0x7f39913812d1 (/home/ttt/asan/libcontent.so+0xfb812d1) (BuildId: 9dcb118d5a6da423)  

#13 0x7f39894c072e (/home/ttt/asan/libcontent.so+0x7cc072e) (BuildId: 9dcb118d5a6da423)  

#14 0x7f399138cc94 (/home/ttt/asan/libcontent.so+0xfb8cc94) (BuildId: 9dcb118d5a6da423)  

#15 0x7f3999f22626 (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x122626) (BuildId: 7af4b8f1c9110ade)  

#16 0x7f3999f20e28 (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x120e28) (BuildId: 7af4b8f1c9110ade)  

#17 0x7f3999f6c8db (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x16c8db) (BuildId: 7af4b8f1c9110ade)  

#18 0x7f3999f2827c (/home/ttt/asan/libmojo\_public\_cpp\_bindings.so+0x12827c) (BuildId: 7af4b8f1c9110ade)  

#19 0x7f397db7b9e1 (/home/ttt/asan/libipc.so+0x17b9e1) (BuildId: 06b96c6bc00843bd)  

#20 0x7f397db80c39 (/home/ttt/asan/libipc.so+0x180c39) (BuildId: 06b96c6bc00843bd)  

#21 0x7f397db80938 (/home/ttt/asan/libipc.so+0x180938) (BuildId: 06b96c6bc00843bd)  

#22 0x7f397db8059e (/home/ttt/asan/libipc.so+0x18059e) (BuildId: 06b96c6bc00843bd)  

#23 0x7f397db803e8 (/home/ttt/asan/libipc.so+0x1803e8) (BuildId: 06b96c6bc00843bd)  

#24 0x7f39a6206cc4 (/home/ttt/asan/libbase.so+0xa06cc4) (BuildId: 2ea62f5ae37135e0)  

#25 0x7f39a6806560 (/home/ttt/asan/libbase.so+0x1006560) (BuildId: 2ea62f5ae37135e0)  

#26 0x7f39a69405e5 (/home/ttt/asan/libbase.so+0x11405e5) (BuildId: 2ea62f5ae37135e0)  

#27 0x7f39a693f06e (/home/ttt/asan/libbase.so+0x113f06e) (BuildId: 2ea62f5ae37135e0)  

#28 0x7f39a693d274 (/home/ttt/asan/libbase.so+0x113d274) (BuildId: 2ea62f5ae37135e0)  

#29 0x7f39a693f642 (/home/ttt/asan/libbase.so+0x113f642) (BuildId: 2ea62f5ae37135e0)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/ttt/asan/libbase.so+0xba7ece) (BuildId: 2ea62f5ae37135e0)  

Shadow bytes around the buggy address:  

0x5130000f7400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x5130000f7480: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa f7 fa  

0x5130000f7500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x5130000f7580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x5130000f7600: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  

=>0x5130000f7680: fa fa fa fa fa fa f7 fa[fd]fd fd fd fd fd fd fd  

0x5130000f7700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5130000f7780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5130000f7800: fd fd fd fd fd fd fa fa fa fa fa fa fa fa f7 fa  

0x5130000f7880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x5130000f7900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

==92476==ADDITIONAL INFO

==92476==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7f398b17b5c9 (/home/ttt/asan/libcontent.so+0x997b5c9) (BuildId: 9dcb118d5a6da423)  

#1 0x7f399b9a4e30 (/home/ttt/asan/libmojo\_public\_system\_cpp.so+0x92e30) (BuildId: b4bd78ec7327a291)  

#2 0x7f398f953f38 (/home/ttt/asan/libcontent.so+0xe153f38) (BuildId: 9dcb118d5a6da423)  

#3 0x7f399b9aa5eb (/home/ttt/asan/libmojo\_public\_system\_cpp.so+0x985eb) (BuildId: b4bd78ec7327a291)

MiraclePtr Status: PROTECTED  

This crash occurred while a raw\_ptr<T> object containing a dangling pointer was being dereferenced.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==92476==END OF ADDITIONAL INFO  

==92476==ABORTING

## Attachments

- poc1.webm (video/webm, 2.5 MB)

## Timeline

### [Deleted User] (2023-12-12)

[Empty comment from Monorail migration]

### ti...@gmail.com (2023-12-12)

debug version is too slow, I reproduce it in release version. video is in attachment

### th...@chromium.org (2023-12-12)

I can reproduce this on Stable (120.0.6099.0) on Linux. Speculatively setting OS to Desktop + Android.

This is a UAF in the browser process marked with `MiraclePtr Status:PROTECTED`, so downgrading 1 severity level (critical -> high). There are user interactions needed which could downgrade severity to medium, but they don't seem that hard to convince a user to do, so I'm leaving it as high for now.

Assigning to aleventhal@ -- could you PTAL or reassign as appropriate?

In the next comment I'll add a symbolized stack trace.

[Monorail components: Internals>Accessibility]

### th...@chromium.org (2023-12-12)

=================================================================
==111330==ERROR: AddressSanitizer: heap-use-after-free on address 0x5130002b8680 at pc 0x55da33e0ae25 bp 0x7fffc650c030 sp 0x7fffc650c028
READ of size 1 at 0x5130002b8680 thread T0 (chrome)
==111330==WARNING: invalid path to external symbolizer!
==111330==WARNING: Failed to use and restart external symbolizer!
    #0 0x55da33e0ae24 in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) _asan_rtl_:17
    #1 0x55da33e0a8f5 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) _asan_rtl_:5
    #2 0x55da3bec6d43 in SafelyUnwrapPtrForDereference<ui::AXPlatformTreeManager> ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr_hookable_impl.h:85:9
    #3 0x55da3bec6d43 in GetForDereference ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:833:12
    #4 0x55da3bec6d43 in operator-> ./../../base/allocator/partition_allocator/src/partition_alloc/pointers/raw_ptr.h:577:12
    #5 0x55da3bec6d43 in ui::AXEventRecorderAuraLinux::ProcessATKEvent(char const*, unsigned int, _GValue const*) ./../../ui/accessibility/platform/inspect/ax_event_recorder_auralinux.cc:137:8
    #6 0x55da3bec6ab4 in ui::AXEventRecorderAuraLinux::OnATKEventReceived(_GSignalInvocationHint*, unsigned int, _GValue const*, void*) ./../../ui/accessibility/platform/inspect/ax_event_recorder_auralinux.cc:45:16
    #7 0x7f56e91e554b in g_param_spec_variant ??:?
    #8 0x7f56e91e6950 in g_param_spec_variant ??:?
    #9 0x7f56e91ec80d in g_signal_emit_by_name ??:0:0

0x5130002b8680 is located 0 bytes inside of 360-byte region [0x5130002b8680,0x5130002b87e8)
freed by thread T0 (chrome) here:
    #0 0x55da1f87acdd in operator delete(void*) _asan_rtl_:3
    #1 0x55da2b8e2347 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #2 0x55da2b8e2347 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:297:7
    #3 0x55da2b8e2347 in content::RenderFrameHostImpl::SetEmbeddingToken(base::UnguessableToken const&) ./../../content/browser/renderer_host/render_frame_host_impl.cc:15729:36
    #4 0x55da2b85b468 in content::RenderFrameHostImpl::DidCommitNewDocument(content::mojom::DidCommitProvisionalLoadParams const&, content::NavigationRequest*) ./../../content/browser/renderer_host/render_frame_host_impl.cc:13368:3
    #5 0x55da2b859bdf in content::RenderFrameHostImpl::DidNavigate(content::mojom::DidCommitProvisionalLoadParams const&, content::NavigationRequest*, bool) ./../../content/browser/renderer_host/render_frame_host_impl.cc:4020:5
    #6 0x55da2b7e0b56 in content::Navigator::DidNavigate(content::RenderFrameHostImpl*, content::mojom::DidCommitProvisionalLoadParams const&, std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest>>, bool) ./../../content/browser/renderer_host/navigator.cc:589:22
    #7 0x55da2b86a655 in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::InlinedStructPtr<content::mojom::DidCommitSameDocumentNavigationParams>) ./../../content/browser/renderer_host/render_frame_host_impl.cc:13276:58
    #8 0x55da2b866d50 in content::RenderFrameHostImpl::DidCommitNavigation(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) ./../../content/browser/renderer_host/render_frame_host_impl.cc:13957:8
    #9 0x55da2b9476cd in Invoke<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), content::RenderFrameHostImpl *, content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams> > ./../../base/functional/bind_internal.h:713:12
    #10 0x55da2b9476cd in void base::internal::InvokeHelper<false, void, 0ul, 1ul>::MakeItSo<void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), std::__Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>>(void (content::RenderFrameHostImpl::*&&)(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), std::__Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>&&, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>&&) ./../../base/functional/bind_internal.h:868:12
    #11 0x55da2b9473cc in RunImpl<void (content::RenderFrameHostImpl::*)(content::NavigationRequest *, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), std::__Cr::tuple<base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL, 1UL> ./../../base/functional/bind_internal.h:968:12
    #12 0x55da2b9473cc in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(content::NavigationRequest*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>), base::internal::UnretainedWrapper<content::RenderFrameHostImpl, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<content::NavigationRequest, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>)>::RunOnce(base::internal::BindStateBase*, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadParams>&&, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>&&) ./../../base/functional/bind_internal.h:919:12
    #13 0x55da25974bcc in Run ./../../base/functional/callback.h:154:12
    #14 0x55da25974bcc in content::mojom::NavigationClient_CommitNavigation_ForwardToCallback::Accept(mojo::Message*) ./gen/content/common/navigation_client.mojom.cc:1149:26
    #15 0x55da3657bdb6 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1011:41
    #16 0x55da3659af32 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #17 0x55da36581015 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20
    #18 0x55da37009f32 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1075:24
    #19 0x55da36fffcff in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind_internal.h:713:12
    #20 0x55da36fffcff in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind_internal.h:868:12
    #21 0x55da36fffcff in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind_internal.h:968:12
    #22 0x55da36fffcff in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #23 0x55da33f49618 in Run ./../../base/functional/callback.h:154:12
    #24 0x55da33f49618 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #25 0x55da33fb46f8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:11)> ./../../base/task/common/task_annotator.h:89:5
    #26 0x55da33fb46f8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:461:23
    #27 0x55da33fb343a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:326:41
    #28 0x55da33fb55fa in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #29 0x55da34147b1f in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:646:46
    #30 0x55da3414af58 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #31 0x7f56e90c7703 in g_clear_list ??:?

previously allocated by thread T0 (chrome) here:
    #0 0x55da1f87a47d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55da2c59e0d1 in content::BrowserAccessibilityManager::Create(content::WebAXPlatformTreeManagerDelegate*) ./../../content/browser/accessibility/browser_accessibility_manager_auralinux.cc:29:10
    #2 0x55da2b88865f in content::RenderFrameHostImpl::GetOrCreateBrowserAccessibilityManager() ./../../content/browser/renderer_host/render_frame_host_impl.cc:11084:7
    #3 0x55da2c15d3b6 in content::WebContentsImpl::RecordAccessibilityEvents(bool, std::__Cr::optional<base::RepeatingCallback<void (std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&)>>) ./../../content/browser/web_contents/web_contents_impl.cc:5015:20
    #4 0x55da32e4eeb2 in AccessibilityUIMessageHandler::RequestAccessibilityEvents(base::Value::List const&) ./../../chrome/browser/accessibility/accessibility_ui.cc:721:19
    #5 0x55da32e53f5b in Invoke<void (AccessibilityUIMessageHandler::*)(const base::Value::List &), AccessibilityUIMessageHandler *, const base::Value::List &> ./../../base/functional/bind_internal.h:713:12
    #6 0x55da32e53f5b in MakeItSo<void (AccessibilityUIMessageHandler::*const &)(const base::Value::List &), const std::__Cr::tuple<base::internal::UnretainedWrapper<AccessibilityUIMessageHandler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, const base::Value::List &> ./../../base/functional/bind_internal.h:868:12
    #7 0x55da32e53f5b in RunImpl<void (AccessibilityUIMessageHandler::*const &)(const base::Value::List &), const std::__Cr::tuple<base::internal::UnretainedWrapper<AccessibilityUIMessageHandler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:968:12
    #8 0x55da32e53f5b in base::internal::Invoker<base::internal::BindState<void (AccessibilityUIMessageHandler::*)(base::Value::List const&), base::internal::UnretainedWrapper<AccessibilityUIMessageHandler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::Value::List const&)>::Run(base::internal::BindStateBase*, base::Value::List const&) ./../../base/functional/bind_internal.h:932:12
    #9 0x55da2c3b5b85 in base::RepeatingCallback<void (base::Value::List const&)>::Run(base::Value::List const&) const & ./../../base/functional/callback.h:337:12
    #10 0x55da2c3b57e4 in content::WebUIImpl::ProcessWebUIMessage(GURL const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::Value::List) ./../../content/browser/webui/web_ui_impl.cc:267:27
    #11 0x55da2c3b245d in content::WebUIImpl::Send(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::Value::List) ./../../content/browser/webui/web_ui_impl.cc:128:3
    #12 0x55da259a572b in content::mojom::WebUIHostStubDispatch::Accept(content::mojom::WebUIHost*, mojo::Message*) ./gen/content/common/web_ui.mojom.cc:198:13
    #13 0x55da3657b97e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54
    #14 0x55da3659af32 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #15 0x55da36581015 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20
    #16 0x55da37009f32 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1075:24
    #17 0x55da36fffcff in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind_internal.h:713:12
    #18 0x55da36fffcff in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind_internal.h:868:12
    #19 0x55da36fffcff in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind_internal.h:968:12
    #20 0x55da36fffcff in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #21 0x55da33f49618 in Run ./../../base/functional/callback.h:154:12
    #22 0x55da33f49618 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #23 0x55da33fb46f8 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:11)> ./../../base/task/common/task_annotator.h:89:5
    #24 0x55da33fb46f8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:461:23
    #25 0x55da33fb343a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:326:41
    #26 0x55da33fb55fa in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #27 0x55da34147b1f in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:646:46
    #28 0x55da3414af58 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #29 0x7f56e90c7703 in g_clear_list ??:?

SUMMARY: AddressSanitizer: heap-use-after-free (/usr/local/google/home/thefrog/security-sheriffing/asan-stable-120/chrome+0x238d1e24) (BuildId: 53d30629de87fa40)
Shadow bytes around the buggy address:
  0x5130002b8400: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
  0x5130002b8480: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x5130002b8500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x5130002b8580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x5130002b8600: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa f7 fa
=>0x5130002b8680:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130002b8700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130002b8780: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
  0x5130002b8800: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
  0x5130002b8880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x5130002b8900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==111330==ADDITIONAL INFO

==111330==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55da29dc22da in content::RenderAccessibilityHost::HandleAXEvents(mojo::StructPtr<blink::mojom::AXUpdatesAndEvents>, unsigned int, base::OnceCallback<void ()>) ./../../content/browser/accessibility/render_accessibility_host.cc:33:7
    #1 0x55da3660e50a in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple_watcher.cc:102:13


MiraclePtr Status: PROTECTED
This crash occurred while a raw_ptr<T> object containing a dangling pointer was being dereferenced.
MiraclePtr is expected to make this crash non-exploitable once fully enabled.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==111330==END OF ADDITIONAL INFO
==111330==ABORTING


### [Deleted User] (2023-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-12)

[Empty comment from Monorail migration]

### al...@chromium.org (2023-12-13)

David, can you find someone for this?

### [Deleted User] (2023-12-13)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@gmail.com (2023-12-14)

I find a simliar old issue in a11y with different OS: https://bugs.chromium.org/p/chromium/issues/detail?id=1277327
bisect may be this: https://chromium-review.googlesource.com/c/chromium/src/+/3966568

### [Deleted User] (2023-12-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-26)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@gmail.com (2024-01-08)

friendly ping ~

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2024-01-16)

[secondary shepherd]

I've sent an email to dtseng asking them to assign this to a good owner on their team.

### ti...@gmail.com (2024-01-25)

C:\User\tt\> ping 1510762

### th...@chromium.org (2024-01-30)

dtseng@: Were you able to find an owner for this bug?

aleventhal@: Alternatively, any other ideas on who might be a good owner for this bug?

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1510762?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### wf...@chromium.org (2024-02-05)

hello this is the security shepherd here and I'm checking in on this HIGH severity security bug that affects STABLE channel. I wonder if there was any update on the resolution? Alternatively is it possible to put this code that's affected behing a base::Feature so it can be disabled for our users while the investigation is ongoing?

### dt...@google.com (2024-02-06)

There are really no direct owners here on my team.
https://chromium-review.googlesource.com/c/chromium/src/+/5273251
would be the fix.

### ap...@google.com (2024-02-07)

Project: chromium/src
Branch: main

commit 3796d6c889f4b603ed051b18537c5de39cce1824
Author: David Tseng <dtseng@google.com>
Date:   Wed Feb 07 01:06:48 2024

    [linux-a11y]: fix UAF in AXEventRecorderAuralinux
    
    R=aleventhal@chromium.org
    
    Fixed: 41483350
    Change-Id: I871a0333050d2e490cc767fe9adbd64da0c4472a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5273251
    Reviewed-by: Mark Schillaci <mschillaci@google.com>
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: David Tseng <dtseng@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1257109}

M       content/public/browser/ax_inspect_factory_auralinux.cc
M       ui/accessibility/platform/ax_platform_tree_manager.cc
M       ui/accessibility/platform/ax_platform_tree_manager.h
M       ui/accessibility/platform/inspect/ax_event_recorder_auralinux.cc
M       ui/accessibility/platform/inspect/ax_event_recorder_auralinux.h

https://chromium-review.googlesource.com/5273251


### pe...@google.com (2024-02-07)

Requesting merge to extended stable (M120) because latest trunk commit (1257109) appears to be after extended stable branch point (1217362).
Requesting merge to stable (M121) because latest trunk commit (1257109) appears to be after stable branch point (1233107).
Requesting merge to beta (M122) because latest trunk commit (1257109) appears to be after beta branch point (1250580).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-02-08)

Merge review required: M122 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-02-08)

Merge review required: M121 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-02-08)

Merge review required: M120 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2024-02-09)

M122 merge approved for https://crrev.com/c/5273251; please merge this fix to M122 branch 6261 by EOD Monday, 12 February so this fix can be included in M122 Stable cut on Tuesday 

Given that this issue is BRP protected, is not remote exploitable and requires a series of user interaction, M121 may not be especially warranted, but since this fix is rather low risk it can be merged to M121; last planned Stable update of M121 is being cut tomorrow at 10am PST. If this could be merged to 6167 before then that would be okay, otherwise this fix is fine to ship in M122 Stable the following week. 

There are no further planned updates of M120 Extended, so no 120 merge is needed here

### sr...@google.com (2024-02-12)

since this fix has not been merged to M121 so far and per comment #27 its ok to wait for M122, i am dropping the merge-approved-121 label and will let this go in m122.

### pb...@google.com (2024-02-13)

Please get the Cl's merged to M122 branch asap, Since we are planning to cut M122 Stable RC around 3PM PST today. 

Please get them cherry picked asap and reach out to me if you need any help.

### ap...@google.com (2024-02-13)

Project: chromium/src
Branch: refs/branch-heads/6261

commit f6422b69b313e56cd840a37d81ba951b98cb4efc
Author: David Tseng <dtseng@google.com>
Date:   Tue Feb 13 20:52:57 2024

    m122: [linux-a11y]: fix UAF in AXEventRecorderAuralinux
    
    R=aleventhal@chromium.org
    
    (cherry picked from commit 3796d6c889f4b603ed051b18537c5de39cce1824)
    
    Fixed: 41483350
    Change-Id: I871a0333050d2e490cc767fe9adbd64da0c4472a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5273251
    Reviewed-by: Mark Schillaci <mschillaci@google.com>
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: David Tseng <dtseng@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1257109}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5292817
    Auto-Submit: David Tseng <dtseng@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Avi Drissman <avi@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6261@{#738}
    Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

M       content/public/browser/ax_inspect_factory_auralinux.cc
M       ui/accessibility/platform/ax_platform_tree_manager.cc
M       ui/accessibility/platform/ax_platform_tree_manager.h
M       ui/accessibility/platform/inspect/ax_event_recorder_auralinux.cc
M       ui/accessibility/platform/inspect/ax_event_recorder_auralinux.h

https://chromium-review.googlesource.com/5292817


### pe...@google.com (2024-02-13)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pb...@google.com (2024-02-13)

The Cl is already merged to M122 branch https://chromium-review.googlesource.com/c/chromium/src/+/5292817

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of a highly mitigated security bug, mitigated by BRP protection, significant user gesture / not being remote exploitable. A member of the p2p-vrp finance team will be in touch with you soon to arrange payment. In the meantime, please let us know the name or handle you would like us to use in acknowledging you for this finding. Thank you for your efforts and reporting this issue to us.

### am...@chromium.org (2024-02-14)

adjusting severity to medium, since this issue is a low/medium severity issue based on the level of mitigations

### ti...@gmail.com (2024-02-18)

reply to #34: credited name is ttt 

### pe...@google.com (2024-03-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-03-20)

1. One <https://crrev.com/c/5379701>
2. Low - simple change, no conflicts
3. M122
4. Yes

### ap...@google.com (2024-04-01)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 360c6151c4e313265b41d3995dc628b17fdc5c5c
Author: David Tseng <dtseng@google.com>
Date:   Mon Apr 01 18:53:15 2024

    [M120-LTS][linux-a11y]: fix UAF in AXEventRecorderAuralinux
    (cherry picked from commit 3796d6c889f4b603ed051b18537c5de39cce1824)
    
    (cherry picked from commit f6422b69b313e56cd840a37d81ba951b98cb4efc)
    
    Fixed: 41483350
    Change-Id: I871a0333050d2e490cc767fe9adbd64da0c4472a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5273251
    Commit-Queue: David Tseng <dtseng@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1257109}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5292817
    Auto-Submit: David Tseng <dtseng@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Avi Drissman <avi@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6261@{#738}
    Cr-Original-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5379701
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
    Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
    Reviewed-by: David Tseng <dtseng@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#1998}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       content/public/browser/ax_inspect_factory_auralinux.cc
M       ui/accessibility/platform/ax_platform_tree_manager.cc
M       ui/accessibility/platform/ax_platform_tree_manager.h
M       ui/accessibility/platform/inspect/ax_event_recorder_auralinux.cc
M       ui/accessibility/platform/inspect/ax_event_recorder_auralinux.h

https://chromium-review.googlesource.com/5379701


### pe...@google.com (2024-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ni...@google.com (2024-06-18)

This seems to no longer be occurring. Therefore I am marking as verified.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41483350)*
