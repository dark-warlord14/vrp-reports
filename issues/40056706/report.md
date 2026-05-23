# Use-after-Free on HandleOnPerformDrop

| Field | Value |
|-------|-------|
| **Issue ID** | [40056706](https://issues.chromium.org/issues/40056706) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DataTransfer |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2021-07-28 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description


Use-after-Free on HandleOnPerformDrop


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

# Use-after-Free on HandleOnPerformDrop
## Root Cause and some notes
[0] The `web_contents` is posted to a separate sequence

[1] `web_contents` may be destroyed in UI by the time the it runs, causing a UAF in ScanData callback.

https://chromium-review.googlesource.com/c/chromium/src/+/3041006
The pattern of this vulnerability is similar to this patch.

```cpp
void HandleOnPerformDrop(
    content::WebContents* web_contents,
    const content::DropData& drop_data,
    content::WebContentsViewDelegate::DropCompletionCallback callback) {
  ...
  if (drop_data.filenames.empty()) {
    ScanData(web_contents, std::move(callback), std::move(data));
  } else {
    base::ThreadPool::PostTaskAndReplyWithResult(
        FROM_HERE, {base::TaskPriority::USER_VISIBLE, base::MayBlock()},
        base::BindOnce(&GetPathsToScan, web_contents, std::move(drop_data),//---> posttask here [0]
                       std::move(data)),
        base::BindOnce(&ScanData, web_contents, std::move(callback)));//-->posttask reply here [0]
  }
}
```

```cpp
void ScanData(content::WebContents* web_contents,
              content::WebContentsViewDelegate::DropCompletionCallback callback,
              enterprise_connectors::ContentAnalysisDelegate::Data data) {
  enterprise_connectors::ContentAnalysisDelegate::CreateForWebContents(
      web_contents, std::move(data), //[1] enter use!
      base::BindOnce(&CompletionCallback, std::move(callback)),
      safe_browsing::DeepScanAccessPoint::DRAG_AND_DROP);
}
--->
// static
void ContentAnalysisDelegate::CreateForWebContents(
    content::WebContents* web_contents,
    Data data,
    CompletionCallback callback,
    safe_browsing::DeepScanAccessPoint access_point) {
  Factory* testing_factory = GetFactoryStorage();
  bool wait_for_verdict = data.settings.block_until_verdict ==
                          enterprise_connectors::BlockUntilVerdict::BLOCK;
  // Using new instead of std::make_unique<> to access non public constructor.
  auto delegate =
      testing_factory->is_null()
          ? std::unique_ptr<ContentAnalysisDelegate>(
                new ContentAnalysisDelegate(web_contents, std::move(data),// [1] enter use!
                                            std::move(callback), access_point))
          : testing_factory->Run(web_contents, std::move(data),
                                 std::move(callback));
--->
ContentAnalysisDelegate::ContentAnalysisDelegate(
    content::WebContents* web_contents,
    Data data,
    CompletionCallback callback,
    safe_browsing::DeepScanAccessPoint access_point)
    : data_(std::move(data)),
      callback_(std::move(callback)),
      access_point_(access_point) {
  DCHECK(web_contents);
  profile_ = Profile::FromBrowserContext(web_contents->GetBrowserContext());
  url_ = web_contents->GetLastCommittedURL(); // [1] use here!
  result_.text_results.resize(data_.text.size(), false);
  result_.paths_results.resize(data_.paths.size(), false);
  file_info_.resize(data_.paths.size());
}
```

[2] The root cause of this vulnerability is very clear, but to quick trigger this vulnerability, we need to patch two codes.

- First add `sleep(3)` at the beginning of the GetPathsToScan function. **Note that we can block the thread pool or create a folder, which continuously recursively stores the recursive folder to achieve the effect of sleep(3) , Because the for loop in GetPathsToScan needs to recursively scan and obtain some file information, which will take some time, so this patch is not necessary**

```cpp
enterprise_connectors::ContentAnalysisDelegate::Data GetPathsToScan(
    content::WebContents* web_contents,
    const content::DropData& drop_data,
    enterprise_connectors::ContentAnalysisDelegate::Data data) {
  sleep(3);//add sleep to here
  for (const auto& file : drop_data.filenames) {
    base::File::Info info;

    // Ignore the path if it's a symbolic link.
    if (!base::GetFileInfo(file.path, &info) || info.is_symbolic_link)
      continue;

    // If the file is a directory, recursively add the files it holds to |data|.
    if (info.is_directory) {
      base::FileEnumerator file_enumerator(file.path, /*recursive=*/true,
                                           base::FileEnumerator::FILES);
      for (base::FilePath sub_path = file_enumerator.Next(); !sub_path.empty();
           sub_path = file_enumerator.Next()) {
        data.paths.push_back(sub_path);
      }
    } else {
      data.paths.push_back(file.path);
    }
  }

  return data;
}
```

- patch HandleOnPerformDrop to simulate enable enterprise_connectors::ContentAnalysisDelegate

**Note that this should be a normal enterprise function, but I am not a enterprise user of chrome, I can only open it in this way.But there are still normal enterprise users who may be attacked because their enable is turned on and no patch is needed.**

```cpp
void HandleOnPerformDrop(
    content::WebContents* web_contents,
    const content::DropData& drop_data,
    content::WebContentsViewDelegate::DropCompletionCallback callback) {
  enterprise_connectors::ContentAnalysisDelegate::Data data;
  Profile* profile =
      Profile::FromBrowserContext(web_contents->GetBrowserContext());
  auto connector =
      drop_data.filenames.empty()
          ? enterprise_connectors::AnalysisConnector::BULK_DATA_ENTRY
          : enterprise_connectors::AnalysisConnector::FILE_ATTACHED;
-  if (!enterprise_connectors::ContentAnalysisDelegate::IsEnabled( //delete 
+  if (enterprise_connectors::ContentAnalysisDelegate::IsEnabled( // add
          profile, web_contents->GetLastCommittedURL(), &data, connector)) {
    std::move(callback).Run(
        content::WebContentsViewDelegate::DropCompletionResult::kContinue);
    return;
  }
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc;l=78;drc=80def040657db16e79f59e7e3b27857014c0f58d?q=HandleOnPerformDrop&ss=chromium%2Fchromium%2Fsrc

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc;l=70;drc=80def040657db16e79f59e7e3b27857014c0f58d;bpv=1;bpt=1?q=HandleOnPerformDrop&ss=chromium%2Fchromium%2Fsrc
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/analysis/content_analysis_delegate.cc;l=388;drc=80def040657db16e79f59e7e3b27857014c0f58d;bpv=1;bpt=1
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/analysis/content_analysis_delegate.cc;l=454;drc=80def040657db16e79f59e7e3b27857014c0f58d

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc;l=40;drc=80def040657db16e79f59e7e3b27857014c0f58d;bpv=1;bpt=1
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc;l=89;drc=80def040657db16e79f59e7e3b27857014c0f58d

## Reproduce
1. Refer to the instructions for simple patching of the code
2. Start chrome with the following parameters.
3. Before the second page is closed by `window.close`, drag a non-empty folder to the page.

```
python3 -m http.server 8000
out/release/chrome "about:blank" 127.0.0.1:8000/test.html
```

## ASAN LOG
```
[] ~/chromium/src <master> out/release/chrome "about:blank" 127.0.0.1:8000/test.html
[47272:47296:0728/211451.218627:ERROR:database.cc(1714)] Passwords sqlite error 1, errno 0: table logins_temp has 24 columns but 25 values were supplied, sql: INSERT INTO logins_temp SELECT * from logins
[47272:47296:0728/211451.218787:ERROR:login_database.cc(781)] Unable to migrate database from 22 to 29
[47272:47296:0728/211451.245888:ERROR:password_store_impl.cc(55)] Could not create/open login database.
[47309:47309:0728/211451.411734:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
=================================================================
==47272==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e00006e480 at pc 0x55cbfd665118 bp 0x7ffc1fc7c050 sp 0x7ffc1fc7c048
READ of size 8 at 0x61e00006e480 thread T0 (chrome)
    #0 0x55cbfd665117 in enterprise_connectors::ContentAnalysisDelegate::ContentAnalysisDelegate(content::WebContents*, enterprise_connectors::ContentAnalysisDelegate::Data, base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data const&, enterprise_connectors::ContentAnalysisDelegate::Result const&)>, safe_browsing::DeepScanAccessPoint) chrome/browser/enterprise/connectors/analysis/content_analysis_delegate.cc:372:56
    #1 0x55cbfd6642ef in enterprise_connectors::ContentAnalysisDelegate::CreateForWebContents(content::WebContents*, enterprise_connectors::ContentAnalysisDelegate::Data, base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data const&, enterprise_connectors::ContentAnalysisDelegate::Result const&)>, safe_browsing::DeepScanAccessPoint) chrome/browser/enterprise/connectors/analysis/content_analysis_delegate.cc:306:21
    #2 0x55cc024bf3c8 in (anonymous namespace)::ScanData(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data) chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc:72:3
    #3 0x55cc024c02db in void base::internal::FunctorTraits<void (*)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), void>::Invoke<void (*)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data>(void (*&&)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), content::WebContents*&&, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>&&, enterprise_connectors::ContentAnalysisDelegate::Data&&) base/bind_internal.h:404:12
    #4 0x55cc024c02db in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data>(void (*&&)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), content::WebContents*&&, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>&&, enterprise_connectors::ContentAnalysisDelegate::Data&&) base/bind_internal.h:648:12
    #5 0x55cc024c02db in void base::internal::Invoker<base::internal::BindState<void (*)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)> >, void (enterprise_connectors::ContentAnalysisDelegate::Data)>::RunImpl<void (*)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), std::__Cr::tuple<content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)> >, 0ul, 1ul>(void (*&&)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), std::__Cr::tuple<content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)> >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, enterprise_connectors::ContentAnalysisDelegate::Data&&) base/bind_internal.h:721:12
    #6 0x55cc024c02db in base::internal::Invoker<base::internal::BindState<void (*)(content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)>, enterprise_connectors::ContentAnalysisDelegate::Data), content::WebContents*, base::OnceCallback<void (content::WebContentsViewDelegate::DropCompletionResult)> >, void (enterprise_connectors::ContentAnalysisDelegate::Data)>::RunOnce(base::internal::BindStateBase*, enterprise_connectors::ContentAnalysisDelegate::Data&&) base/bind_internal.h:690:12
    #7 0x55cc024c06bd in base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>::Run(enterprise_connectors::ContentAnalysisDelegate::Data) && base/callback.h:98:12
    #8 0x55cc024c06bd in void base::internal::ReplyAdapter<enterprise_connectors::ContentAnalysisDelegate::Data, enterprise_connectors::ContentAnalysisDelegate::Data>(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*) base/post_task_and_reply_with_result_internal.h:30:23
    #9 0x55cc024c0a36 in void base::internal::FunctorTraits<void (*)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), void>::Invoke<void (*)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*>(void (*&&)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>&&, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*&&) base/bind_internal.h:404:12
    #10 0x55cc024c0a36 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*>(void (*&&)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>&&, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*&&) base/bind_internal.h:648:12
    #11 0x55cc024c0a36 in void base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >, std::__Cr::default_delete<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> > > > >, void ()>::RunImpl<void (*)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), std::__Cr::tuple<base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >, std::__Cr::default_delete<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> > > > >, 0ul, 1ul>(void (*&&)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), std::__Cr::tuple<base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >, std::__Cr::default_delete<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> > > > >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:721:12
    #12 0x55cc024c0a36 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >*), base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data)>, base::internal::OwnedWrapper<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> >, std::__Cr::default_delete<std::__Cr::unique_ptr<enterprise_connectors::ContentAnalysisDelegate::Data, std::__Cr::default_delete<enterprise_connectors::ContentAnalysisDelegate::Data> > > > >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #13 0x7f9ee7a80902 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #14 0x7f9ee7a80902 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReply(base::(anonymous namespace)::PostTaskAndReplyRelay) base/threading/post_task_and_reply_impl.cc:115:29
    #15 0x7f9ee7a80b48 in void base::internal::FunctorTraits<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), void>::Invoke<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay&&) base/bind_internal.h:404:12
    #16 0x7f9ee7a80b48 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay&&) base/bind_internal.h:648:12
    #17 0x7f9ee7a80b48 in void base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunImpl<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::__Cr::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0ul>(void (*&&)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::__Cr::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:721:12
    #18 0x7f9ee7a80b48 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #19 0x7f9ee79e5170 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #20 0x7f9ee79e5170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #21 0x7f9ee7a289aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:344:23
    #22 0x7f9ee7a281cb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:258:36
    #23 0x7f9ee78996e9 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:374:46
    #24 0x7f9ee78996e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:124:43
    #25 0x7f9ea6cce17c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c)

0x61e00006e480 is located 0 bytes inside of 2736-byte region [0x61e00006e480,0x61e00006ef30)
freed by thread T0 (chrome) here:
    #0 0x55cbfa293dfd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55cc015f6871 in std::__Cr::default_delete<content::WebContents>::operator()(content::WebContents*) const buildtools/third_party/libc++/trunk/include/memory:1335:5
    #2 0x55cc015f6871 in std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents> >::reset(content::WebContents*) buildtools/third_party/libc++/trunk/include/memory:1596:7
    #3 0x55cc015f6871 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:550:21
    #4 0x55cc015fed75 in TabStripModel::InternalCloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1816:5
    #5 0x55cc015fffa1 in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:760:10
    #6 0x7f9ede378d0a in content::WebContentsImpl::Close(content::RenderViewHost*) content/browser/web_contents/web_contents_impl.cc:7099:16
    #7 0x7f9ede378d0a in non-virtual thunk to content::WebContentsImpl::Close(content::RenderViewHost*) content/browser/web_contents/web_contents_impl.cc
    #8 0x7f9ed41ccf74 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) gen/third_party/blink/public/mojom/frame/frame.mojom.cc:19331:13
    #9 0x7f9ee66efcb9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:863:54
    #10 0x7f9ee66ffdea in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #11 0x7f9ee66f3ca5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:653:21
    #12 0x7f9ee2eb4a19 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:950:24
    #13 0x7f9ee2ead0b8 in void base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), void>::Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>&&, mojo::Message&&) base/bind_internal.h:509:12
    #14 0x7f9ee2ead0b8 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*&&)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>&&, mojo::Message&&) base/bind_internal.h:648:12
    #15 0x7f9ee2ead0b8 in void base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0ul, 1ul>(void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*&&)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:721:12
    #16 0x7f9ee2ead0b8 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:690:12
    #17 0x7f9ee79e5170 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #18 0x7f9ee79e5170 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #19 0x7f9ee7a289aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:344:23
    #20 0x7f9ee7a281cb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:258:36
    #21 0x7f9ee78996e9 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:374:46
    #22 0x7f9ee78996e9 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:124:43
    #23 0x7f9ea6cce17c in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5217c)

previously allocated by thread T0 (chrome) here:
    #0 0x55cbfa29359d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x7f9ede2dfe18 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) content/browser/web_contents/web_contents_impl.cc:1043:7
    #2 0x55cc014df676 in (anonymous namespace)::CreateTargetContents(NavigateParams const&, GURL const&) chrome/browser/ui/browser_navigator.cc:457:7
    #3 0x55cc014df676 in Navigate(NavigateParams*) chrome/browser/ui/browser_navigator.cc:644:28
    #4 0x55cc015d5fcc in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, bool, std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:311:5
    #5 0x55cc015d85f4 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:580:13
    #6 0x55cc015d5183 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool, std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:427:22
    #7 0x55cc015d4645 in StartupBrowserCreatorImpl::Launch(Profile*, std::__Cr::vector<GURL, std::__Cr::allocator<GURL> > const&, bool, std::__Cr::unique_ptr<LaunchModeRecorder, std::__Cr::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator_impl.cc:216:3
    #8 0x55cc015c9e6f in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__Cr::unique_ptr<LaunchModeRecorder, std::__Cr::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator.cc:645:13
    #9 0x55cc015cfc57 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1171:14
    #10 0x55cc015c9282 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:1098:10
    #11 0x55cc015c6d32 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*> > const&) chrome/browser/ui/startup/startup_browser_creator.cc:580:10
    #12 0x55cbfce7d4fd in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome/browser/chrome_browser_main.cc:1683:25
    #13 0x55cbfce7b692 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome/browser/chrome_browser_main.cc:1064:18
    #14 0x7f9edd0e03dc in content::BrowserMainLoop::PreMainMessageLoopRun() content/browser/browser_main_loop.cc:949:28
    #15 0x7f9ede237f48 in base::OnceCallback<int ()>::Run() && base/callback.h:98:12
    #16 0x7f9ede237f48 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup_task_runner.cc:41:29
    #17 0x7f9edd0df9fd in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser_main_loop.cc:857:25
    #18 0x7f9edd0e67ba in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser_main_runner_impl.cc:131:15
    #19 0x7f9edd0dbd05 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:43:32
    #20 0x7f9edf1725c5 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:597:10
    #21 0x7f9edf1725c5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1080:10
    #22 0x7f9edf1718b9 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:955:12
    #23 0x7f9edf16be7c in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:379:36
    #24 0x7f9edf16c3bc in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:405:10
    #25 0x55cbfa2960bd in ChromeMain chrome/app/chrome_main.cc:151:12
    #26 0x7f9ea63d30b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/enterprise/connectors/analysis/content_analysis_delegate.cc:372:56 in enterprise_connectors::ContentAnalysisDelegate::ContentAnalysisDelegate(content::WebContents*, enterprise_connectors::ContentAnalysisDelegate::Data, base::OnceCallback<void (enterprise_connectors::ContentAnalysisDelegate::Data const&, enterprise_connectors::ContentAnalysisDelegate::Result const&)>, safe_browsing::DeepScanAccessPoint)
Shadow bytes around the buggy address:
  0x0c3c80005c40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005c50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005c60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005c70: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3c80005c80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3c80005c90:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005ca0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005cb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005cc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005cd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3c80005ce0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
  Shadow gap:              cc
==47272==ABORTING
```



#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

This vulnerability can be used for sandbox escape, because the vulnerability is in the browser process, not in the render.

Because `enterprise_connectors::ContentAnalysisDelegate::IsEnabled`,so enterprise users are more vulnerable to attacks.

As long as the user is induced to drag the malicious folder to the malicious page, it may trigger a stable sandbox escape.



---

### The cause


#### What version of Chrome have you found the security issue in?

[92.0.4515.107+] + [stable]


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Sandbox Escape 


#### Please provide your credit information

Nan Wang (@eternalsakura13) and koocola (@alo_cook) of 360 Alpha Lab




## Attachments

- [test.html](attachments/test.html) (text/plain, 79 B)
- [uaf3.mp4](attachments/uaf3.mp4) (video/mp4, 3.2 MB)
- [uaf.log](attachments/uaf.log) (text/plain, 25.9 KB)

## Timeline

### et...@gmail.com (2021-07-28)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2021-07-28)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-07-28)

Thank you for the report. Setting severity=high because the drag & drop requirement is a mitigating factor.

avi, could you PTAL since this is under chrome/browser/ui/tab_contents/?

[Monorail components: Blink>DataTransfer]

### [Deleted User] (2021-07-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2021-07-28)

This is DLP, + those folks.

Dominique, you were the one who added much of this. Do you have the context to work on this?

### do...@chromium.org (2021-07-28)

I think so, I'll look into it.

### gi...@appspot.gserviceaccount.com (2021-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5d028192c1491fd190e5b8366bccbcfd967ade2

commit e5d028192c1491fd190e5b8366bccbcfd967ade2
Author: Dominique Fauteux-Chapleau <domfc@chromium.org>
Date: Wed Jul 28 23:10:06 2021

Refactor HandleOnPerformDrop to account for destroyed web contents

Bug: 1233975
Change-Id: Ief294ae69d5acc1225be949c222a6651d3198dfc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3056782
Reviewed-by: Roger Tawa <rogerta@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Dominique Fauteux-Chapleau <domfc@chromium.org>
Cr-Commit-Position: refs/heads/master@{#906438}

[modify] https://crrev.com/e5d028192c1491fd190e5b8366bccbcfd967ade2/chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc


### do...@chromium.org (2021-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-29)

Hi, domfc@ no need to manually request merges on security bugs. Once the status is updated to Fixed, Sheriffbot will kick in and updated with the appropriate merge requests. :) Thanks! 

### do...@chromium.org (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-29)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-07-30)

1. Yes
2. crrev.com/c/3056782
3. The fix has been reproed and verified locally, and landed on ToT yesterday.
4. M93 and M92 (if I'm reading the labels on this bug correctly)
5. This is a security issue (UAF)
6. No, this is a bug on an existing feature
7. n/a

### [Deleted User] (2021-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-02)

Hi Dominique- Approving for merge to M93. As long as you're happy with stability on canary and there's no issues/concerns, please merge to branch 4577 before 2pm PDT/5pm EDT tomorrow (Tuesday, 3 August) so that it can be a part of the this week's M93/beta release. Thank you!  

### gi...@appspot.gserviceaccount.com (2021-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e35d2fb18347daba5191e3f98c3aeb087f4f2c3c

commit e35d2fb18347daba5191e3f98c3aeb087f4f2c3c
Author: Dominique Fauteux-Chapleau <domfc@chromium.org>
Date: Mon Aug 02 22:04:32 2021

Refactor HandleOnPerformDrop to account for destroyed web contents

(cherry picked from commit e5d028192c1491fd190e5b8366bccbcfd967ade2)

Bug: 1233975
Change-Id: Ief294ae69d5acc1225be949c222a6651d3198dfc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3056782
Reviewed-by: Roger Tawa <rogerta@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Dominique Fauteux-Chapleau <domfc@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#906438}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3064223
Commit-Queue: Avi Drissman <avi@chromium.org>
Auto-Submit: Dominique Fauteux-Chapleau <domfc@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#352}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/e35d2fb18347daba5191e3f98c3aeb087f4f2c3c/chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc


### do...@chromium.org (2021-08-04)

The CL has been merged, let me know when/if it should be merged into M92.

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

And another one! Congratulations, Nan Wang and koocola- the VRP Panel has decided to award you $20,000 for this report. Great stuff! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-09-08)

LTS merge approved

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2520b380018fbcf315bdc76b9b20f894def52f9e

commit 2520b380018fbcf315bdc76b9b20f894def52f9e
Author: Dominique Fauteux-Chapleau <domfc@chromium.org>
Date: Wed Sep 08 17:32:58 2021

[M90-LTS] Refactor HandleOnPerformDrop to account for destroyed web contents

M90 merge conflicts:
* base/optional.h is not in original commit so automerge failed. No actual
  conflicts.

(cherry picked from commit e5d028192c1491fd190e5b8366bccbcfd967ade2)

(cherry picked from commit e35d2fb18347daba5191e3f98c3aeb087f4f2c3c)

Bug: 1233975
Change-Id: Ief294ae69d5acc1225be949c222a6651d3198dfc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3056782
Reviewed-by: Roger Tawa <rogerta@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Dominique Fauteux-Chapleau <domfc@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#906438}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3064223
Commit-Queue: Avi Drissman <avi@chromium.org>
Auto-Submit: Dominique Fauteux-Chapleau <domfc@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4577@{#352}
Cr-Original-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3148051
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1583}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/2520b380018fbcf315bdc76b9b20f894def52f9e/chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc


### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1233975?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056706)*
