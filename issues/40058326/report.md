# Security: use-after-poison in blink::InspectorAccessibilityAgent::RefreshFrontendNodes 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058326](https://issues.chromium.org/issues/40058326) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2021-12-23 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

I think this vulnerability can be triggered in a simpler way, but I haven't found it yet.

=================================================================  

==12428==ERROR: AddressSanitizer: use-after-poison on address 0x7e9700534380 at pc 0x7fffc5246bad bp 0x0053d25fa5a0 sp 0x0053d25fa5e8  

READ of size 8 at 0x7e9700534380 thread T0  

==12428==WARNING: Failed to use and restart external symbolizer!  

==12428==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==12428==\*\*\* Most likely this means that the app is already \*\*\*  

==12428==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==12428==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==12428==\*\*\* or produce wrong results. \*\*\*  

#0 0x7fffc5246bac in blink::InspectorAccessibilityAgent::RefreshFrontendNodes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1076  

#1 0x7fffc5247933 in blink::InspectorAccessibilityAgent::AXObjectModified C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1127  

#2 0x7fffc137fbf9 in blink::AXObjectCacheImpl::MarkAXObjectDirtyWithCleanLayoutHelper C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:3396  

#3 0x7fffc51b8ff2 in blink::AXRelationCache::UpdateRelatedText C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_relation\_cache.cc:536  

#4 0x7fffc51b8cd7 in blink::AXRelationCache::UpdateRelatedTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_relation\_cache.cc:521  

#5 0x7fffc1379120 in blink::AXObjectCacheImpl::MaybeNewRelationTarget C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2863  

#6 0x7fffc1321f39 in blink::AXObject::Init C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:649  

#7 0x7fffc13716b3 in blink::AXObjectCacheImpl::CreateAndInit C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:1376  

#8 0x7fffc1370ede in blink::AXObjectCacheImpl::CreateAndInit C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:1194  

#9 0x7fffc5209ffc in blink::AXNodeObject::TextFromDescendants C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3422  

#10 0x7fffc51fbefb in blink::AXNodeObject::TextAlternative C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3239  

#11 0x7fffc51d03df in blink::AXLayoutObject::TextAlternative C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_layout\_object.cc:1154  

#12 0x7fffc13411c5 in blink::AXObject::GetName C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:3417  

#13 0x7fffc51faa11 in blink::AXNodeObject::GetName C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3146  

#14 0x7fffc132ca18 in blink::AXObject::SerializeNameAndDescriptionAttributes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:1417  

#15 0x7fffc132b260 in blink::AXObject::Serialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:1214  

#16 0x7fffc5236a44 in blink::InspectorAccessibilityAgent::BuildProtocolAXNodeForUnignoredAXObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:709  

#17 0x7fffc5232617 in blink::InspectorAccessibilityAgent::BuildProtocolAXNodeForAXObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:640  

#18 0x7fffc52468c2 in blink::InspectorAccessibilityAgent::RefreshFrontendNodes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1071  

#19 0x7fffc5247933 in blink::InspectorAccessibilityAgent::AXObjectModified C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1127  

#20 0x7fffc137fbf9 in blink::AXObjectCacheImpl::MarkAXObjectDirtyWithCleanLayoutHelper C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:3396  

#21 0x7fffc51b8ff2 in blink::AXRelationCache::UpdateRelatedText C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_relation\_cache.cc:536  

#22 0x7fffc51b8cd7 in blink::AXRelationCache::UpdateRelatedTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_relation\_cache.cc:521  

#23 0x7fffc1379120 in blink::AXObjectCacheImpl::MaybeNewRelationTarget C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2863  

#24 0x7fffc1321f39 in blink::AXObject::Init C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:649  

#25 0x7fffc13716b3 in blink::AXObjectCacheImpl::CreateAndInit C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:1376  

#26 0x7fffc1370ede in blink::AXObjectCacheImpl::CreateAndInit C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:1194  

#27 0x7fffc5209ffc in blink::AXNodeObject::TextFromDescendants C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3422  

#28 0x7fffc51fbefb in blink::AXNodeObject::TextAlternative C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3239  

#29 0x7fffc51d03df in blink::AXLayoutObject::TextAlternative C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_layout\_object.cc:1154  

#30 0x7fffc13411c5 in blink::AXObject::GetName C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:3417  

#31 0x7fffc51faa11 in blink::AXNodeObject::GetName C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3146  

#32 0x7fffc132ca18 in blink::AXObject::SerializeNameAndDescriptionAttributes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:1417  

#33 0x7fffc132b260 in blink::AXObject::Serialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:1214  

#34 0x7fffc5236a44 in blink::InspectorAccessibilityAgent::BuildProtocolAXNodeForUnignoredAXObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:709  

#35 0x7fffc5232617 in blink::InspectorAccessibilityAgent::BuildProtocolAXNodeForAXObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:640  

#36 0x7fffc52468c2 in blink::InspectorAccessibilityAgent::RefreshFrontendNodes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1071  

#37 0x7fffc5247933 in blink::InspectorAccessibilityAgent::AXObjectModified C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1127  

#38 0x7fffc137fbf9 in blink::AXObjectCacheImpl::MarkAXObjectDirtyWithCleanLayoutHelper C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:3396  

#39 0x7fffc51b8ff2 in blink::AXRelationCache::UpdateRelatedText C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_relation\_cache.cc:536  

#40 0x7fffc51b8cd7 in blink::AXRelationCache::UpdateRelatedTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_relation\_cache.cc:521  

#41 0x7fffc1379120 in blink::AXObjectCacheImpl::MaybeNewRelationTarget C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2863  

#42 0x7fffc1321f39 in blink::AXObject::Init C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:649  

#43 0x7fffc13716b3 in blink::AXObjectCacheImpl::CreateAndInit C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:1376  

#44 0x7fffc1370ede in blink::AXObjectCacheImpl::CreateAndInit C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:1194  

#45 0x7fffc5209ffc in blink::AXNodeObject::TextFromDescendants C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3422  

#46 0x7fffc51fbefb in blink::AXNodeObject::TextAlternative C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3239  

#47 0x7fffc51d03df in blink::AXLayoutObject::TextAlternative C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_layout\_object.cc:1154  

#48 0x7fffc13411c5 in blink::AXObject::GetName C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:3417  

#49 0x7fffc51faa11 in blink::AXNodeObject::GetName C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_node\_object.cc:3146  

#50 0x7fffc132ca18 in blink::AXObject::SerializeNameAndDescriptionAttributes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:1417  

#51 0x7fffc132b260 in blink::AXObject::Serialize C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object.cc:1214  

#52 0x7fffc5236a44 in blink::InspectorAccessibilityAgent::BuildProtocolAXNodeForUnignoredAXObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:709  

#53 0x7fffc5232617 in blink::InspectorAccessibilityAgent::BuildProtocolAXNodeForAXObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:640  

#54 0x7fffc52468c2 in blink::InspectorAccessibilityAgent::RefreshFrontendNodes C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1071  

#55 0x7fffc5246f4e in blink::InspectorAccessibilityAgent::AXEventFired C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1095  

#56 0x7fffc137c1ea in blink::AXObjectCacheImpl::PostPlatformNotification C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:3379  

#57 0x7fffc137bc0f in blink::AXObjectCacheImpl::FireAXEventImmediately C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2679  

#58 0x7fffc137794d in blink::AXObjectCacheImpl::PostNotification C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2601  

#59 0x7fffc137755b in blink::AXObjectCacheImpl::ChildrenChangedWithCleanLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2243  

#60 0x7fffc137ba66 in blink::AXObjectCacheImpl::FireTreeUpdatedEventImmediately C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2654  

#61 0x7fffc137b05d in blink::AXObjectCacheImpl::ProcessCleanLayoutCallbacks C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2536  

#62 0x7fffc1379d53 in blink::AXObjectCacheImpl::ProcessDeferredAccessibilityEvents C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\ax\_object\_cache\_impl.cc:2289  

#63 0x7fffc0c386c5 in blink::LocalFrameView::RunAccessibilityLifecyclePhase::<lambda\_31>::operator() C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2767  

#64 0x7fffc0c0870a in blink::LocalFrameView::ForAllNonThrottledLocalFrameViews<`lambda at ../../third\_party/blink/renderer/core/frame/local\_frame\_view.cc:2764:37'> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:382  

#65 0x7fffc0bfea16 in blink::LocalFrameView::RunAccessibilityLifecyclePhase C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2764  

#66 0x7fffc0bfcaad in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2348  

#67 0x7fffc0bfa090 in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2272  

#68 0x7fffc0d3f2c5 in blink::LayoutView::HitTest C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\layout\layout\_view.cc:147  

#69 0x7fffc0cc7ebc in blink::Document::PerformMouseEventHitTest C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:4320  

#70 0x7fffc0ee6872 in blink::EventHandler::GetMouseEventTarget C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\event\_handler.cc:2511  

#71 0x7fffc0ee87de in blink::EventHandler::HandleMouseMoveOrLeaveEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\event\_handler.cc:1059  

#72 0x7fffc0ee7c3a in blink::EventHandler::HandleMouseMoveEvent C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\event\_handler.cc:946  

#73 0x7fffc3e076a6 in blink::MouseEventManager::RecomputeMouseHoverState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\input\mouse\_event\_manager.cc:448  

#74 0x7fffc0bbf277 in blink::WebFrameWidgetImpl::BeginMainFrame C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:2033  

#75 0x7fffc3c2795e in blink::WidgetBase::BeginMainFrame C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:823  

#76 0x7fffc179c9a1 in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:241  

#77 0x7fffc56a5672 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState,std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::\_\_1::unique\_ptr<cc::BeginMainFrameAndCommitState,std::\_\_1::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#78 0x7fffbc0d1f74 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#79 0x7fffbec057a5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#80 0x7fffbec04e78 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#81 0x7fffbebddda7 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:38  

#82 0x7fffbec06e71 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#83 0x7fffbc050ae3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#84 0x7fffbe6d7af2 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:283  

#85 0x7fffb7d03ccd in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:678  

#86 0x7fffb7d058a3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1028  

#87 0x7fffb7d01b21 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#88 0x7fffb7d02bac in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#89 0x7fffb15d148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#90 0x7ff778a15b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#91 0x7ff778a12b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#92 0x7ff778e1457f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#93 0x7ff85382134f in BaseThreadInitThunk+0xf (C:\WINDOWS\System32\KERNEL32.DLL+0x18001134f)  

#94 0x7ff854a31e77 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180051e77)

Address 0x7e9700534380 is a wild pointer inside of access range of size 0x000000000008.  

SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\accessibility\inspector\_accessibility\_agent.cc:1076 in blink::InspectorAccessibilityAgent::RefreshFrontendNodes  

Shadow bytes around the buggy address:  

0x115dcd4a6820: f7 f7 f7 00 00 00 00 00 f7 00 00 f7 00 00 f7 f7  

0x115dcd4a6830: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 f7  

0x115dcd4a6840: f7 f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x115dcd4a6850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x115dcd4a6860: 00 00 00 00 00 00 00 00 00 f7 00 00 00 00 00 f7  

=>0x115dcd4a6870:[f7]f7 00 00 00 00 00 00 00 00 f7 f7 f7 00 00 00  

0x115dcd4a6880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x115dcd4a6890: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x115dcd4a68a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x115dcd4a68b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x115dcd4a68c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==12428==ABORTING

**VERSION**  

Chrome Version: 99.0.4777.0 dev x64  

Operating System: win11

**REPRODUCTION CASE**  

1.enter to <http://www.baidu.com>  

2.enter to chrome://flags and then devtools debug and enter something  

3.search xxxxxxx in chrome://flags and delete the enter ,then wait

Type of crash: tab

Reporter credit: Zhihua Yao of Kunlun Lab

## Attachments

- [repro.mp4](attachments/repro.mp4) (video/mp4, 25.8 MB)
- [ddemo.mp4](attachments/ddemo.mp4) (video/mp4, 12.6 MB)

## Timeline

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-12-23)

Thanks for your report. Severity High as this is browser UAF with considerable interaction required. It seems to be related to changes that might have been introduced in M98.

jobay@chromium.org -> can you please take a look at this issue?

[Monorail components: Platform>DevTools>Accessibility Platform>DevTools>Authoring]

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2021-12-27)

I can't reproduce on linux asan 99.0.4789.0 (Developer Build) (64-bit).
Does the crash only happen with --no-sandbox?

### ha...@gmail.com (2021-12-27)

Yep, --no-sandbox

### jo...@google.com (2021-12-29)

I am still unable to reproduce on Linux.
nektar@chromium.org, alexrudenko@chromium.org, dsv@chromium.org, do any of you know why the use-after-poison line number[1] points to a line with just a "}"? I would have thought it should point to a line with a use of some pointer?

[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/accessibility/inspector_accessibility_agent.cc;l=1076

### ha...@gmail.com (2021-12-29)

[Comment Deleted]

### ha...@gmail.com (2021-12-29)

I found a simpler way to reproduce on windows, you can refer to the video.And you can use my  chromium test user data to reproduce

https://drive.google.com/file/d/1h0bKSM4OMdDoFpMJxY-rsv9341OenQ_I/view?usp=sharing

chrome  "--no-sandbox --user-data-dir=.\tmp"

### jo...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-01-07)

We found that in some circumstances, we can end up re-entering InspectorAccessibilityAgent::RefreshFrontendNodes.
Initial fix is to make RefreshFrontendNodes handle re-entrancy in a more graceful way.

### ma...@chromium.org (2022-01-07)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/3372823

### jo...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/90769f72ac83f5f6c9d9075c453ce353f8aed662

commit 90769f72ac83f5f6c9d9075c453ce353f8aed662
Author: Johan Bay <jobay@chromium.org>
Date: Sat Jan 08 14:05:56 2022

Fix when reentering RefreshFrontendNodes

The re-entrancy happens roughly like this:
- An object is marked dirty
- We serialize the object to build a protocol AXNode for it
- Serializing kicks name computation, which in turn marks some other
  objects dirty
- This makes us reenter RefreshFrontendNodes, which was not expected
  when that function was written

Bug: 1282320
Change-Id: Ia659a858ec6a2f4f2bf4b334ff9b60a9f4968f18
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3372823
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Commit-Queue: Johan Bay <jobay@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956836}

[modify] https://crrev.com/90769f72ac83f5f6c9d9075c453ce353f8aed662/third_party/blink/renderer/modules/accessibility/inspector_accessibility_agent.cc


### jo...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-01-10)

@meysarabadani can you help me figure out the next steps for getting this back-merged?

### ya...@google.com (2022-01-10)

Johan: all you need to do is to figure out the affected milestones, and mark this issue with appropriate labels, e.g. Merge-Request-98.

### ya...@google.com (2022-01-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-01-10)

Ah, perfect. Thank you!

### [Deleted User] (2022-01-10)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-01-10)

1. Why does your merge fit within the merge criteria for these milestones?
Security issue.
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3372823
3. Have the changes been released and tested on canary?
Fix landed on Sat Jan 08.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Not a feature.
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
See ASAN repro described in this bug report.


### sr...@google.com (2022-01-10)

Merge approved for M98 branch:4758 pls merge your changes asap ( before 12pm PST tuesday Jan 11 , so it can be part of beta release for this week) 

Pls verify on canary channel before merging, if you think this requires more bake time on canary pls wait until then to merge. 

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0cbd4260ce67b4c9fa15e25c93f189a8fdca5145

commit 0cbd4260ce67b4c9fa15e25c93f189a8fdca5145
Author: Johan Bay <jobay@chromium.org>
Date: Tue Jan 11 16:37:35 2022

Fix when reentering RefreshFrontendNodes

The re-entrancy happens roughly like this:
- An object is marked dirty
- We serialize the object to build a protocol AXNode for it
- Serializing kicks name computation, which in turn marks some other
  objects dirty
- This makes us reenter RefreshFrontendNodes, which was not expected
  when that function was written

(cherry picked from commit 90769f72ac83f5f6c9d9075c453ce353f8aed662)

Bug: 1282320
Change-Id: Ia659a858ec6a2f4f2bf4b334ff9b60a9f4968f18
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3372823
Reviewed-by: Aaron Leventhal <aleventhal@chromium.org>
Commit-Queue: Johan Bay <jobay@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956836}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3380587
Auto-Submit: Johan Bay <jobay@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Nektarios Paisios <nektar@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#503}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/0cbd4260ce67b4c9fa15e25c93f189a8fdca5145/third_party/blink/renderer/modules/accessibility/inspector_accessibility_agent.cc


### am...@chromium.org (2022-01-12)

based on this bug not being able to accessible via the web and triggering relies solely on exceptional amount of direct UI user interaction, adjusting security severity accordingly 

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### [Deleted User] (2022-01-13)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-13)

Thank you for this report, hacky@! The VRP Panel would like to extend a $500 thank you award for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-10)

The code in question wasn't added until https://crrev.com/c/3253352 which hasn't landed to M96 so marking as not applicable.

### vo...@google.com (2022-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2022-09-26)

Crash no longer being reported. Issue presumed fixed

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1282320?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools>Accessibility, Platform>DevTools>Authoring]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058326)*
