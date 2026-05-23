# SUMMARY: AddressSanitizer: access-violation regexp-interpreter.cc:461 in v8::internal::`anonymous namespace'::RawMatch<unsigned char>

| Field | Value |
|-------|-------|
| **Issue ID** | [40057683](https://issues.chromium.org/issues/40057683) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Regexp |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2021-10-23 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4665.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-934183.zip

#Reproduce

1. python -m http.server 80
2. chrome --no-sandbox --enable-blink-test-features --disable-extensions --user-data-dir=test http://localhost/poc.html
3. click havtest button

If it does not reproduce, refresh the page and try again

What is the expected behavior?

What went wrong?
Type of crash
render tab

#Analysis
Come soon

#Patch
Not yet

Did this work before? N/A 

Chrome version: 97.0.4665.0  Channel: n/a
OS Version: 10.0

#asan
=================================================================
==628==ERROR: AddressSanitizer: access-violation on unknown address 0x7e8700000005 (pc 0x7ff8adbf1e36 bp 0x0073fabfcf00 sp 0x0073fabfce80 T0)
==628==The signal is caused by a READ memory access.
==628==*** WARNING: Failed to initialize DbgHelp!              ***
==628==*** Most likely this means that the app is already      ***
==628==*** using DbgHelp, possibly with incompatible flags.    ***
==628==*** Due to technical reasons, symbolization might crash ***
==628==*** or produce wrong results.                           ***
==628==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff8adbf1e35 in v8::internal::`anonymous namespace'::RawMatch<unsigned char> C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp-interpreter.cc:461
    #1 0x7ff8adbf1914 in v8::internal::IrregexpInterpreter::MatchInternal C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp-interpreter.cc:1092
    #2 0x7ff8adbf1506 in v8::internal::IrregexpInterpreter::Match C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp-interpreter.cc:1066
    #3 0x7ff8adbfe22b in v8::internal::IrregexpInterpreter::MatchForCallFromRuntime C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp-interpreter.cc:1143
    #4 0x7ff8adc4468f in v8::internal::RegExpImpl::IrregexpExecRaw C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp.cc:703
    #5 0x7ff8adc3fa08 in v8::internal::RegExpImpl::IrregexpExec C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp.cc:776
    #6 0x7ff8adc3f1f7 in v8::internal::RegExp::Exec C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp.cc:322
    #7 0x7ff8addb7f05 in v8::internal::Runtime_RegExpExecTreatMatchAtEndAsFailure C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-regexp.cc:923
    #8 0x7e8607f0987b  (<unknown module>)
    #9 0x1241085ad4c7  (<unknown module>)
    #10 0x1261092630af  (<unknown module>)
    #11 0x1e10857ffff  (<unknown module>)
    #12 0x7ff8ad2da5b0 in v8::internal::Runtime_LoadIC_Miss C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2531

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp-interpreter.cc:461 in v8::internal::`anonymous namespace'::RawMatch<unsigned char>
==628==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 151.5 KB)
- [worklet-recorder.js](attachments/worklet-recorder.js) (text/plain, 1.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 2.3 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-10-23)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-10-25)

jgruber, can you please help triage?

[Monorail components: Blink>JavaScript>Regexp]

### jg...@chromium.org (2021-10-26)

From the backtrace, looks like an OOB read while reading the regexp bytecode array.

### jg...@chromium.org (2021-10-26)

Can't repro on a non-asan build (Linux x64 97.0.4676.0)

### jg...@chromium.org (2021-10-26)

[Comment Deleted]

### jg...@chromium.org (2021-10-26)

- We're in the interpreter (--regexp-interpret-all may help to repro).
- Runtime_RegExpExecTreatMatchAtEndAsFailure in the backtrace tells us we're in RegExp.p.split; in the repro there are only 4 such calls:

var substitution_re = /\$\{([^ }]*)\}/g;
var components = input.split(substitution_re);

var lines = stack.split("\n");

var components = name.split(".");

output_location = assert.stack.split("\n", 1)

- The flaky repro & OOB read could be a symptom of the GC moving the bytecode array without irregexp updating its pointers.
- Or something goes wrong during bytecode interpretation causing us to read OOB.

### jg...@chromium.org (2021-10-26)

Can't repro with an asan build either (asan-linux-beta-96.0.4664.18 - not an exact version match, but at least it has the last recent bigger regexp change https://chromiumdash.appspot.com/commit/bba7c09aadca0c1cd231b5c75d8be2bfe726a5f4). 

I *do* get a fairly reliable crash with this one, but it looks like something else:

[146200:146200:1026/134019.514183:FATAL:script_promise_resolver.cc(51)] Check failed: false. ScriptPromiseResolver was not properly detached; created at

Maybe crbug.com/1258108?

m.cooolie@ could you try to repro with --js-flags="--regexp-interpret-all --trace-regexp-bytecode --print-regexp-bytecode" and paste the output?

### m....@gmail.com (2021-10-26)

Adding the --js-flags="--regexp-interpret-all --trace-regexp-bytecode --print-regexp-bytecode" does not get any new information. I don't know if my method is wrong?

And the problem can still be reproduced on asan-win32-release_x64-934904, the reproduced stack is as follows.

This stack is the same as the original sample crash stack of this case. The regex related stack was discovered during the minisample production process.

D:\chrome_asan\asan-win32-release_x64-934904>chrome --no-sandbox --js-flags="--regexp-interpret-all --trace-regexp-bytecode --print-regexp-bytecode" --enable-blink-test-features --disable-extensions --user-data-dir=test http://localhost/poc.html
Error: unrecognized flag --trace-regexp-bytecode
The remaining arguments were ignored: --print-regexp-bytecode
Try --help for options
Error: unrecognized flag --trace-regexp-bytecode
The remaining arguments were ignored: --print-regexp-bytecode
Try --help for options
[1768:8876:1026/202501.526:ERROR:chrome_browser_main_extra_parts_metrics.cc(227)] START: ReportBluetoothAvailability(). If you don't see the END: message, this is crbug.com/1216328.
[1768:8876:1026/202501.526:ERROR:chrome_browser_main_extra_parts_metrics.cc(230)] END: ReportBluetoothAvailability()
[1768:8876:1026/202501.526:ERROR:chrome_browser_main_extra_parts_metrics.cc(235)] START: GetDefaultBrowser(). If you don't see the END: message, this is crbug.com/1216328.
[1768:8876:1026/202501.526:ERROR:chrome_browser_main_extra_parts_metrics.cc(239)] END: GetDefaultBrowser()
[1768:3764:1026/202501.544:ERROR:device_event_log_impl.cc(214)] [20:25:01.543] Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed.

=================================================================
==9836==ERROR: AddressSanitizer: access-violation on unknown address 0x7ed700084540 (pc 0x7ed700084540 bp 0x00310cffcf80 sp 0x00310cffcef8 T0)
==9836==The signal is caused by a UNKNOWN memory access.
==9836==*** WARNING: Failed to initialize DbgHelp!              ***
==9836==*** Most likely this means that the app is already      ***
==9836==*** using DbgHelp, possibly with incompatible flags.    ***
==9836==*** Due to technical reasons, symbolization might crash ***
==9836==*** or produce wrong results.                           ***
==9836==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ed70008453f  (<unknown module>)
    #1 0x7ed707e8cb20  (<unknown module>)
    #2 0x7ed7080023b4  (<unknown module>)
    #3 0x7ed708317d0c  (<unknown module>)
    #4 0x7ed708043ee0  (<unknown module>)
    #5 0x7ed7080024cc  (<unknown module>)
    #6 0x7ed708043ec0  (<unknown module>)
    #7 0x7ed708043ec0  (<unknown module>)
    #8 0x7ed7080024cc  (<unknown module>)
    #9 0x7ed708043ee0  (<unknown module>)
    #10 0x7ed708317d0c  (<unknown module>)
    #11 0x7ed708043dcc  (<unknown module>)
    #12 0x7ed708043ee0  (<unknown module>)
    #13 0x77  (<unknown module>)
    #14 0x7ed7082ed284  (<unknown module>)
    #15 0x3  (<unknown module>)
    #16 0x7ed708043dec  (<unknown module>)
    #17 0x7ed708043da0  (<unknown module>)
    #18 0x310cffd007  (<unknown module>)
    #19 0x7ed707e8cb20  (<unknown module>)
    #20 0x7ed7080023b4  (<unknown module>)
    #21 0x7ed708317944  (<unknown module>)
    #22 0x7ed708043ec0  (<unknown module>)
    #23 0x7ed708043ed0  (<unknown module>)
    #24 0x7ed708043ed0  (<unknown module>)
    #25 0x7ed708043ec0  (<unknown module>)
    #26 0x7ed708317944  (<unknown module>)
    #27 0x7ed7080023b4  (<unknown module>)
    #28 0x7ed708317138  (<unknown module>)
    #29 0x7ed708043dec  (<unknown module>)
    #30 0x95  (<unknown module>)
    #31 0x7ed7082ecff8  (<unknown module>)
    #32 0x0  (<unknown module>)
    #33 0x7ed708043d80  (<unknown module>)
    #34 0x7ed708043da0  (<unknown module>)
    #35 0x310cffd057  (<unknown module>)
    #36 0x7ed707e8cb20  (<unknown module>)
    #37 0x7ed7080023b4  (<unknown module>)
    #38 0x7ed708043d80  (<unknown module>)
    #39 0x7ed7080023b4  (<unknown module>)
    #40 0x4b  (<unknown module>)
    #41 0x7ed7082ecbd8  (<unknown module>)
    #42 0x1  (<unknown module>)
    #43 0x7ed708210fa8  (<unknown module>)
    #44 0x7ed708317138  (<unknown module>)
    #45 0x310cffd087  (<unknown module>)
    #46 0x7fffa530035b in Builtins_JSEntryTrampoline+0x5b (D:\chrome_asan\asan-win32-release_x64-934904\chrome.dll+0x19d02035b)
    #47 0x7ed707e8cb20  (<unknown module>)
    #48 0x7ed7080023b4  (<unknown module>)
    #49 0x7ed708317944  (<unknown module>)
    #50 0x7ed708043ec0  (<unknown module>)
    #51 0x7ed708043ed0  (<unknown module>)
    #52 0x7ed708043ed0  (<unknown module>)
    #53 0x7ed708043ec0  (<unknown module>)
    #54 0x7ed708317944  (<unknown module>)
    #55 0x7ed7080023b4  (<unknown module>)
    #56 0x7ed708317138  (<unknown module>)
    #57 0x7ed708043dec  (<unknown module>)
    #58 0x95  (<unknown module>)
    #59 0x7ed7082ecff8  (<unknown module>)
    #60 0x0  (<unknown module>)
    #61 0x7ed708043d80  (<unknown module>)
    #62 0x7ed708043da0  (<unknown module>)
    #63 0x310cffd057  (<unknown module>)
    #64 0x7ed707e8cb20  (<unknown module>)
    #65 0x7ed7080023b4  (<unknown module>)
    #66 0x7ed708043d80  (<unknown module>)
    #67 0x7ed7080023b4  (<unknown module>)
    #68 0x4b  (<unknown module>)
    #69 0x7ed7082ecbd8  (<unknown module>)
    #70 0x1  (<unknown module>)
    #71 0x7ed708210fa8  (<unknown module>)
    #72 0x7ed708317138  (<unknown module>)
    #73 0x310cffd087  (<unknown module>)
    #74 0x7fffa530035b in Builtins_JSEntryTrampoline+0x5b (D:\chrome_asan\asan-win32-release_x64-934904\chrome.dll+0x19d02035b)
    #75 0x7ed707e8cb20  (<unknown module>)
    #76 0x7ed7080023b4  (<unknown module>)
    #77 0x7ed708043d80  (<unknown module>)
    #78 0x7ed7080023b4  (<unknown module>)
    #79 0x4b  (<unknown module>)
    #80 0x7ed7082ecbd8  (<unknown module>)
    #81 0x1  (<unknown module>)
    #82 0x7ed708210fa8  (<unknown module>)
    #83 0x7ed708317138  (<unknown module>)
    #84 0x310cffd087  (<unknown module>)
    #85 0x7fffa530035b in Builtins_JSEntryTrampoline+0x5b (D:\chrome_asan\asan-win32-release_x64-934904\chrome.dll+0x19d02035b)
    #86 0x7fffa530035b in Builtins_JSEntryTrampoline+0x5b (D:\chrome_asan\asan-win32-release_x64-934904\chrome.dll+0x19d02035b)
    #87 0x7fffa52fff5a in Builtins_JSEntry+0xda (D:\chrome_asan\asan-win32-release_x64-934904\chrome.dll+0x19d01ff5a)
    #88 0x7fff8ee20c81 in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:411
    #89 0x7fff8ee23efb in v8::internal::`anonymous namespace'::InvokeWithTryCatch C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:472
    #90 0x7fff8ee23ab7 in v8::internal::Execution::TryCallScript C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:557
    #91 0x7fff8f2923c1 in v8::internal::Genesis::CompileExtension C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:4127
    #92 0x7fff8f29fdc0 in v8::internal::Genesis::InstallExtension C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:5786
    #93 0x7fff8f29f017 in v8::internal::Genesis::InstallExtensions C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:5726
    #94 0x7fff8f230d19 in v8::internal::Bootstrapper::CreateEnvironment C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:330
    #95 0x7fff8e965b94 in v8::NewContext C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:6300
    #96 0x7fff8e96771b in v8::Context::FromSnapshot C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:6332
    #97 0x7fffa22435f9 in blink::V8ContextSnapshotImpl::CreateContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\modules\v8\v8_context_snapshot_impl.cc:349
    #98 0x7fff9eb068c7 in blink::V8ContextSnapshot::CreateContextFromSnapshot C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_context_snapshot.cc:28
    #99 0x7fff9ddb4930 in blink::LocalWindowProxy::CreateContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\local_window_proxy.cc:238
    #100 0x7fff9ddb28cd in blink::LocalWindowProxy::Initialize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\local_window_proxy.cc:157
    #101 0x7fff9a41f6c8 in blink::LocalWindowProxyManager::UpdateDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\window_proxy_manager.cc:136
    #102 0x7fff978aa9e4 in blink::LocalDOMWindow::InstallNewDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_dom_window.cc:718
    #103 0x7fff97bf87d7 in blink::DocumentLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:2259
    #104 0x7fff9790923f in blink::FrameLoader::CommitDocumentLoader C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1245
    #105 0x7fff97912e0d in blink::FrameLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1083
    #106 0x7fff95047b1a in blink::WebLocalFrameImpl::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_local_frame_impl.cc:2342
    #107 0x7fff951bf09c in content::RenderFrameImpl::CommitNavigationWithParams C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc:2911
    #108 0x7fff95203531 in base::internal::FunctorTraits<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),void>::Invoke<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content: C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:569
    #109 0x7fff95202f8b in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameImpl::*)(mojo::StructPtr<blink::mojom::CommonNavigationParams>, mojo::StructPtr<blink::mojom::CommitNavigationParams>, std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >, absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >, mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>, mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>, mojo::PendingRemote<network::mojom::URLLoaderFactory>, mojo::PendingRemote<blink::mojom::CodeCacheHost>, mojo::StructPtr<content::mojom::CookieManagerInfo>, mojo::StructPtr<content::mojom::StorageInfo>, std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> >, std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >),base::WeakPtr<content::RenderFrameImpl>,mojo::StructPtr<blink::mojom::CommonNavigationParams>,mojo::StructPtr<blink::mojom::CommitNavigationParams>,std::__1::unique_ptr<blink::PendingURLLoaderFactoryBundle,std::__1::default_delete<blink::PendingURLLoaderFactoryBundle> >,absl::optional<std::__1::vector<mojo::StructPtr<blink::mojom::TransferrableURLLoader>,std::__1::allocator<mojo::StructPtr<blink::mojom::TransferrableURLLoader> > > >,mojo::StructPtr<blink::mojom::ControllerServiceWorkerInfo>,mojo::StructPtr<blink::mojom::ServiceWorkerContainerInfoForClient>,mojo::PendingRemote<network::mojom::URLLoaderFactory>,mojo::PendingRemote<blink::mojom::CodeCacheHost>,mojo::StructPtr<content::mojom::CookieManagerInfo>,mojo::StructPtr<content::mojom::StorageInfo>,std::__1::unique_ptr<content::DocumentState,std::__1::default_delete<content::DocumentState> > >,void (std::__1::unique_ptr<blink::WebNavigationParams,std::__1::default_delete<blink::WebNavigationParams> >)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:791
    #110 0x7fff951bbd77 in content::RenderFrameImpl::CommitNavigation C:\b\s\w\ir\cache\builder\src\content\renderer\render_frame_impl.cc:2772
    #111 0x7fff97ff2e17 in content::NavigationClient::CommitNavigation C:\b\s\w\ir\cache\builder\src\content\renderer\navigation_client.cc:51
    #112 0x7fff8b1de008 in content::mojom::NavigationClientStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\navigation_client.mojom.cc:1325
    #113 0x7fff97ff3fcc in content::mojom::NavigationClientStub<mojo::RawPtrImplRefTraits<content::mojom::NavigationClient> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\navigation_client.mojom.h:193
    #114 0x7fff92fc38f9 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:862
    #115 0x7fff95890462 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #116 0x7fff92fc71dc in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657
    #117 0x7fff93835b04 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:984
    #118 0x7fff9382fa21 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:791
    #119 0x7fff92c72e9a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #120 0x7fff9574dc3f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:358
    #121 0x7fff9574d358 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #122 0x7fff95727247 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #123 0x7fff9574f055 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:463
    #124 0x7fff92bf2b93 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #125 0x7fff9520c7f2 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:265
    #126 0x7fff8e8cf81d in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1006
    #127 0x7fff8e8cc202 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:390
    #128 0x7fff8e8cd244 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:418
    #129 0x7fff882e147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:172
    #130 0x7ff753165b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:170
    #131 0x7ff753162c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #132 0x7ff75355d17f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #133 0x7ff82d3c7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #134 0x7ff82f1fcec0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cec0)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (<unknown module>)
==9836==ABORTING

### jg...@chromium.org (2021-10-26)

Something seems to be wrong with the quotes; try the comma-based syntax:

--js-flags=--regexp-interpret-all,--trace-regexp-bytecode,--print-regexp-bytecode

### m....@gmail.com (2021-10-26)

re https://crbug.com/chromium/1262676#c9
I provide an original sample, which can be reproduced stably and is convenient for debugging.

Adding or not adding the --regexp-interpret-all parameter to this sample will produce different crash stacks. If the two crashes are not the same problem, you can open another issue.

1. python -m http.server 80
2. chrome  --no-sandbox  --enable-blink-test-features --disable-extensions --user-data-dir=test http://localhost/fuzz1/1635111946777_60459/fuzz-00013.html
3. Click Havtest button and wait


### jg...@chromium.org (2021-10-28)

Got a repro of the ASAN crash on windows with the exact mentioned build (asan-win32-release_x64-934183). Symbolization doesn't yet work (any hints?). 

One data point is that the crash also occurs with --no-regexp-tier-up, which disables the regexp interpreter. That suggests the bug is elsewhere.

[Monorail components: -Blink>JavaScript>Regexp Blink>JavaScript]

### m....@gmail.com (2021-10-28)

https://crbug.com/chromium/1262676#c10 crash stack seem in JIT code range so symbole may not work. You can use windbg to reproduce the problem, so that most of the time you will get some symbol information.

https://crbug.com/chromium/1262676#c0 sample was got when i try make minipoc with https://crbug.com/chromium/1262676#c10,so i'm not sure they are the same issue.

you can try https://crbug.com/chromium/1262676#c0 poc file, refresh page if not reproduce.

### jg...@chromium.org (2021-10-28)

#12 symbolization doesn't work at all for me, the entire backtrace is unsymbolized. 

Please split off the non-regexp report from #10 to let someone from the chromium team triage it. A bisect would be helpful as well - locally I can repro the crash in 934183, but not in 927096 so that gives us a starting range. 

For the regexp interpreter crash: I haven't seen that one yet. I'll have another look there.

### jg...@chromium.org (2021-10-28)

Re https://crbug.com/chromium/1262676#c0: also here, I don't see the crash inside the regexp interpreter. The backtrace is:

    #0 0x7e940008453f  (<unknown module>)
[...]
    #45 0x7795bfcee7  (<unknown module>)
    #46 0x7ffecefae61b in Builtins_JSEntryTrampoline+0x5b (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x19cffe61b)
    #47 0x7e9407e8cb20  (<unknown module>)
[...]
    #73 0x7795bfcee7  (<unknown module>)
    #74 0x7ffecefae61b in Builtins_JSEntryTrampoline+0x5b (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x19cffe61b)
    #75 0x7e9407e8cb20  (<unknown module>)
[...]
    #84 0x7795bfcee7  (<unknown module>)
    #85 0x7ffecefae61b in Builtins_JSEntryTrampoline+0x5b (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x19cffe61b)


### jg...@chromium.org (2021-10-28)

Scratch that, just caught it. The trick is to pass --no-opt, then repeatedly click HavTest and press F5 to refresh.

    #0 0x7ffeb97d1e35 in v8::internal::`anonymous namespace'::RawMatch<unsigned char> C:\b\s\w\ir\
cache\builder\src\v8\src\regexp\regexp-interpreter.cc:461
    #1 0x7ffeb97d1914 in v8::internal::IrregexpInterpreter::MatchInternal C:\b\s\w\ir\cache\builder\src\v8\src\regexp\regexp-interpreter.cc:1092                                                        #2 0x7ffeb97d1506 in v8::internal::IrregexpInterpreter::Match C:\b\s\w\ir\cache\builder\src\v8
\src\regexp\regexp-interpreter.cc:1066                                                                #3 0x7ffeb97de22b in v8::internal::IrregexpInterpreter::MatchForCallFromRuntime C:\b\s\w\ir\ca
che\builder\src\v8\src\regexp\regexp-interpreter.cc:1143                                              #4 0x7ffeb982468f in v8::internal::RegExpImpl::IrregexpExecRaw C:\b\s\w\ir\cache\builder\src\v
8\src\regexp\regexp.cc:703                                                                            #5 0x7ffeb9826ce6 in v8::internal::RegExpGlobalCache::FetchNext C:\b\s\w\ir\cache\builder\src\
v8\src\regexp\regexp.cc:1178                                                                          #6 0x7ffeb999f0b7 in v8::internal::Runtime_RegExpExecMultiple C:\b\s\w\ir\cache\builder\src\v8
\src\runtime\runtime-regexp.cc:1461                                                                   #7 0x7ee807f0987b  (<unknown module>)                                                             #8 0x2aae9fc767  (<unknown module>)
    #9 0x11f0f41ad4c7  (<unknown module>)
[...]
    #21 0x7ee80866b778  (<unknown module>)                                                            #22 0x7ee80866b794  (<unknown module>)
    #23 0x7ffeb8ebc0ae in v8::internal::Stats_Runtime_LoadIC_Miss+0x16de (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x186f0c0ae)
    #24 0xdeadeba60e75  (<unknown module>)                                                            #25 0x7ee808654a48  (<unknown module>)
    #26 0x2  (<unknown module>)                                                                       #27 0x7ffeb98fd63e in v8::internal::Stats_Runtime_CreateArrayLiteral+0x197e (C:\Users\jgruber\
Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x18794d63e) 

[Monorail components: -Blink>JavaScript Blink>JavaScript>Regexp]

### jg...@chromium.org (2021-10-28)

And again, the regexp interpreter crash vanishes. I started bisecting, but now even the originally broken version 934183 no longer crashes.

Worth noting, the other SEGV occurs when compiling an extension:

    #85 0x7ffecefae61b in Builtins_JSEntryTrampoline+0x5b (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x19cffe61b)
    #86 0x7ffecefae61b in Builtins_JSEntryTrampoline+0x5b (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x19cffe61b)
    #87 0x7ffecefae21a in Builtins_JSEntry+0xda (C:\Users\jgruber\Downloads\asan-win32-release_x64-934183\asan-win32-release_x64-934183\chrome.dll+0x19cffe21a)
    #88 0x7ffeb8add311 in v8::internal::`anonymous namespace'::Invoke C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:383
    #89 0x7ffeb8adff2b in v8::internal::`anonymous namespace'::InvokeWithTryCatch C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:444
    #90 0x7ffeb8adfafa in v8::internal::Execution::TryCall C:\b\s\w\ir\cache\builder\src\v8\src\execution\execution.cc:511
    #91 0x7ffeb8f4dbe6 in v8::internal::Genesis::CompileExtension C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:4125
    #92 0x7ffeb8f5b5e0 in v8::internal::Genesis::InstallExtension C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:5783
    #93 0x7ffeb8f5a837 in v8::internal::Genesis::InstallExtensions C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:5723
    #94 0x7ffeb8eec539 in v8::internal::Bootstrapper::CreateEnvironment C:\b\s\w\ir\cache\builder\src\v8\src\init\bootstrapper.cc:330
    #95 0x7ffeb8622494 in v8::NewContext C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:6297
    #96 0x7ffeb862401b in v8::Context::FromSnapshot C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:6329
    #97 0x7ffecbef2011 in blink::V8ContextSnapshotImpl::CreateContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\modules\v8\v8_context_snapshot_impl.cc:349
    #98 0x7ffec87b8d47 in blink::V8ContextSnapshot::CreateContextFromSnapshot C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_context_snapshot.cc:28
    #99 0x7ffec7a8ca40 in blink::LocalWindowProxy::CreateContext C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\local_window_proxy.cc:238
    #100 0x7ffec7a8a9dd in blink::LocalWindowProxy::Initialize C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\local_window_proxy.cc:157
    #101 0x7ffec40dc628 in blink::LocalWindowProxyManager::UpdateDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\window_proxy_manager.cc:136
    #102 0x7ffec1560e04 in blink::LocalDOMWindow::InstallNewDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_dom_window.cc:718
    #103 0x7ffec18adb57 in blink::DocumentLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:2259
    #104 0x7ffec15bf31f in blink::FrameLoader::CommitDocumentLoader C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1242
    #105 0x7ffec15c8eed in blink::FrameLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1080
    #106 0x7ffebecfcc0a in blink::WebLocalFrameImpl::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_local_frame_impl.cc:2342
   

### jg...@chromium.org (2021-10-28)

I'm still having difficulty reproducing this in a stable, debuggable way. To summarize findings so far:

- There appear to be two different crashes, see the backtraces in https://crbug.com/chromium/1262676#c15 (crash in irregexp) and in https://crbug.com/chromium/1262676#c14 and https://crbug.com/chromium/1262676#c16 (something else). I've only investigated the former in this bug report.
- Crashes are reproduced by clicking HavTest and refreshing. Sometimes the crash seems to reproduce easily, at other times it can take many attempts. Due to memory pressure? Due to cache states? It seems to help to change window focus before refreshing the page.
- I attempted to bisect but the crash is too flaky.
- The symptoms quite clearly point at a problem with the regexp bytecode array or regexp interpreter dispatch, specifically dispatch seems to jump to an invalid address (we use the computed goto extension for interpreter dispatch).
- This can happen either because the read bytecode is invalid (the bytecode array may be corrupted, may have moved, we may read OOB, or may not be a bytecode array at all); or because ASAN somehow interferes with the computed goto extension. The latter is not an academic possibility, we've seen crashes related due to addtl requirements on registers from ASAN in the past.
- Unfortunately I haven't managed to debug this properly yet. On my linux laptop, I get neither an ASAN report, nor does gdb break on the segv. On my Windows VM, after jumping through many hoops, I do get symbolized ASAN reports - but the crash is super-flaky and I know nothing about debugging chromium with windbg. Plus the VM is severely resource-constrained and I can't compile custom builds there.
- Next steps: attempt to repro on a non-ASAN build.

### jg...@chromium.org (2021-10-28)

The optdebug build fails with

# Fatal error in ../../v8/src/regexp/regexp.cc, line 448
# Debug check failed: FLAG_regexp_interpret_all implies bytecode.IsByteArray().

despite the FLAG_regexp_interpret_all not being set. This can happen in a jitless isolate (e.g. pdfium); or something is corrupting the flag value.

### jg...@chromium.org (2021-10-28)

Getting closer - in a non-ASAN build, the trace is

# Fatal error in ../../v8/src/regexp/regexp.cc, line 451
# Debug check failed: FLAG_regexp_interpret_all implies bytecode.IsByteArray().
#
#

#6 0x7fb3eb099b42 v8::internal::RegExpImpl::EnsureCompiledIrregexp()
#7 0x7fb3eb0969cd v8::internal::RegExpImpl::IrregexpPrepare()
#8 0x7fb3eb09aba7 v8::internal::RegExpGlobalCache::RegExpGlobalCache()
#9 0x7fb3eb14f9e6 v8::internal::__RT_impl_Runtime_RegExpExecMultiple()
#10 0x7fb3ea04babf Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit

And the bytecode array slot contains the smi -1 marker. An open q is still why the --regexp-interpret-all flag is set.

### da...@chromium.org (2021-10-28)

As this is happening in regex handling, I am guessing this bug has been around since at least M94, please update if it was introduced more recently.

### da...@chromium.org (2021-10-28)

Thanks for working on root causing this!

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-10-29)

I opened a new case for https://crbug.com/chromium/1262676#c10 https://bugs.chromium.org/p/chromium/issues/detail?id=1264813

### [Deleted User] (2021-10-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-11-03)

jgruber@ any updates on this?

### jg...@chromium.org (2021-11-03)

Due to long weekend and other things I haven't made any progress yet - what I'll do until I get around to a final fix is introduce a CHECK to hard-crash instead of OOB-read.

### jg...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f5274dfe75ea315203cada7ebfe4216cebe19ef3

commit f5274dfe75ea315203cada7ebfe4216cebe19ef3
Author: Jakob Gruber <jgruber@chromium.org>
Date: Wed Nov 03 12:25:37 2021

[regexp] Check we've got a ByteArray in the interpreter

Happy hunting.

Bug: chromium:1262676
Change-Id: I0f3a5519cb9ed3dc4787acd61cb437ee8c2bf2d1
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3257716
Auto-Submit: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77681}

[modify] https://crrev.com/f5274dfe75ea315203cada7ebfe4216cebe19ef3/src/regexp/regexp-interpreter.cc


### jg...@chromium.org (2021-11-03)

Tracing isolate creation and flag values suggests something is altering flag values after the Isolate has started:

Isolate::Init 0x55614d0e2b10 --jitless 0 --regexp-interpret-all 0
Isolate::Init 0x55614d0e24d0 --jitless 0 --regexp-interpret-all 0
Isolate::Init 0x7fe744008d50 --jitless 1 --regexp-interpret-all 1
Isolate::Init 0x7fe70800d570 --jitless 1 --regexp-interpret-all 1
[...]
isolate 0x55614d0e2b10  // Immediately prior to the DCHECK failure.

Note isolate 0x55614d0e2b10 starts with --regexp-interpret-all unset but has the flag set prior to the crash.

It looks like chrome is misusing V8 by starting multiple isolates with different jitless configs in the same process. I vaguely recall hearing related chatter in recent months, gotta do some research.


### jg...@chromium.org (2021-11-03)

+thestig +mlippautz fyi this happens when attempting to use different FLAG_jitless values within the same process.

### jg...@chromium.org (2021-11-03)

Added in crrev.com/c/3093127

yaoxia@ ptal - is it possible that you start a V8 isolate with --jitless in a renderer process? Is shared_storage_worklet hidden behind --enable-blink-test-features?

### jg...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### jg...@chromium.org (2021-11-03)

We should either CHECK-fail if a process hosts multiple isolates with different --jitless (and derived flag) values; or, and this is the better solution, finally implement crbug.com/v8/9019

### le...@google.com (2021-11-03)

We were discussing anyway that flags should be immutable after isolate initialisation.

### ml...@chromium.org (2021-11-03)

tsepez as well.

Seems like https://crbug.com/v8/9019 is the way to go.

### le...@google.com (2021-11-03)

If we want this for security reasons, then we also need to figure out a way to make that flag's memory location read-only.

### ya...@chromium.org (2021-11-03)

jgruber@:
- is it possible that you start a V8 isolate with --jitless in a renderer process?
Yes. The worklet runs in a renderer process (behind a runtime enabled flag). See crrev.com/c/3093127 crrev.com/c/3102525
- Is shared_storage_worklet hidden behind --enable-blink-test-features?
Yes. The RuntimeEnabledFeature is "SharedStorageAPI" and is currently in "test" status.


### jg...@chromium.org (2021-11-04)

#38: Thanks, that confirms my suspicions. Since v8 flags are process-wide, it's not valid to spawn multiple isolates with different flags in the same process. For --jitless and friends (e.g. --regexp-interpret-all) it's especially problematic. I suspect the second bug report with different symptoms (crbug.com/1264813) may have the same root cause.

1) Since SharedStorageAPI is *not* on by default, there is currently no direct user-visible impact.

2) SharedStorageAPI is currently spawns V8 isolates in a way that interferes with other V8 isolates in the same renderer process and will lead to all kinds of hard-to-debug followup errors. The solution is to not spawn SharedStorageAPI isolates with custom flags (-> remove --jitless).

3) For the V8 side, two potential work items are in https://crbug.com/chromium/1262676#c34.

yaoxia@ I'm reassigning to you for point 2) above.

[Monorail components: Blink>JavaScript]

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/3a46c81c26ea52fc10d9114b3ee090bbe354db25

commit 3a46c81c26ea52fc10d9114b3ee090bbe354db25
Author: Jakob Gruber <jgruber@chromium.org>
Date: Mon Nov 08 11:06:32 2021

[flags] Add a sanity check for unchanged jitless flags

V8 flags in general should not change in a process after the
first Isolate has been initialized. --jitless and related flags
especially sensitive to this, so we introduce a dedicated check
just for them.

Bug: chromium:1262676, v8:9019, v8:12366
Change-Id: I239726889d236a3785c1fdc076fa21d1b8983c92
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3260508
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77759}

[modify] https://crrev.com/3a46c81c26ea52fc10d9114b3ee090bbe354db25/src/execution/isolate.cc


### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f86046ca112254c087b62c23b492b8d70179680f

commit f86046ca112254c087b62c23b492b8d70179680f
Author: Yao Xiao <yaoxia@chromium.org>
Date: Mon Nov 08 19:34:18 2021

[shared storage] Remove isolate initialization flags

Why: SharedStorage currently spawns V8 isolates in a way that
interferes with other V8 isolates in the same renderer process and will
lead to all kinds of hard-to-debug followup errors.

Bug: 1262676
Change-Id: I1d84caf968a008ea869e489163fc64c38992b261
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3260459
Commit-Queue: Yao Xiao <yaoxia@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#939469}

[modify] https://crrev.com/f86046ca112254c087b62c23b492b8d70179680f/content/services/shared_storage_worklet/shared_storage_worklet_global_scope.cc


### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/87370c6b58f48366b81f50495f6b8597e8d3c471

commit 87370c6b58f48366b81f50495f6b8597e8d3c471
Author: Leszek Swirski <leszeks@chromium.org>
Date: Tue Nov 09 08:34:18 2021

Revert "[flags] Add a sanity check for unchanged jitless flags"

This reverts commit 3a46c81c26ea52fc10d9114b3ee090bbe354db25.

Reason for revert: Breaking roll (or rather, oh no, cast_shell is broken, need to fix that before relanding): https://ci.chromium.org/ui/p/chromium/builders/try/cast_shell_linux/1053410/overview

Original change's description:
> [flags] Add a sanity check for unchanged jitless flags
>
> V8 flags in general should not change in a process after the
> first Isolate has been initialized. --jitless and related flags
> especially sensitive to this, so we introduce a dedicated check
> just for them.
>
> Bug: chromium:1262676, v8:9019, v8:12366
> Change-Id: I239726889d236a3785c1fdc076fa21d1b8983c92
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3260508
> Commit-Queue: Jakob Gruber <jgruber@chromium.org>
> Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#77759}

Bug: chromium:1262676, v8:9019, v8:12366
Change-Id: Ie47d183bfd68633c3d30a13a038219051c38eba0
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3268734
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Owners-Override: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#77785}

[modify] https://crrev.com/87370c6b58f48366b81f50495f6b8597e8d3c471/src/execution/isolate.cc


### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

yaoxia: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-29)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-12-07)

Any updates on this one?

### m....@gmail.com (2021-12-07)

I think we shoud mark this issues as fixed.

### va...@chromium.org (2021-12-08)

Based on https://crbug.com/chromium/1262676#c47

### [Deleted User] (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-08)

Requesting merge to stable M96 because latest trunk commit (939469) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (939469) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-08)

Merge review required: M97 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-08)

Merge review required: M96 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-12-09)

Per https://crbug.com/chromium/1262676#c38, this bug occurs only behind a test flag, so marking Security_Impact-None.

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for this report and nice work! 

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### jg...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1262676?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Regexp]
[Monorail blocked-on: crbug.com/v8/9019]
[Monorail mergedwith: crbug.com/chromium/1264813]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057683)*
