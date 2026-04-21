# DCHECK failure in TCPReadableStreamWrapper::Pull()

| Field | Value |
|-------|-------|
| **Issue ID** | [453147449](https://issues.chromium.org/issues/453147449) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>DirectSockets |
| **Platforms** | ChromeOS |
| **Reporter** | i....@gmail.com |
| **Assignee** | vk...@google.com |
| **Created** | 2025-10-18 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

1. apply `diff.patch` and build asan chromium. This patch is just for making the reproduction easier and doesn't affect the bug's eligibility.
2. exec `echo -e "UAF" | nc -l 12321` on local.
3. serve `poc.html` on local, and open it by asan chromium built in step 1.
4. chromium crashes.

FYI: I tried it on commit `f7a9c0942b5641`.

# Problem Description

# Root Cause Analysis

`TCPReadableStreamWrapper::Pull()` uses `data_pipe_` to read data [1]. And the method assumes `data_pipe_` is valid at the end of data reading [2].

However, the attacker can run JavaScript synchronously through the execution of `Controller()->enqueue(script_state, buffer, exception_state);`. [3]

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc;l=91-142;drc=1cc7997baa714735aa78b08b94b64b02c22760ae>

```
void TCPReadableStreamWrapper::Pull() {
  [...]
  auto result =
      data_pipe_->BeginReadData(MOJO_BEGIN_READ_DATA_FLAG_NONE, data_buffer); // [1]
  switch (result) {
    case MOJO_RESULT_OK: {
      // respond() or enqueue() will only throw if their arguments are invalid
      // or the stream is errored. The code below guarantees that the length is
      // in range and the chunk is a valid view. If the stream becomes errored
      // then this method cannot be called because the watcher is disarmed.
      NonThrowableExceptionState exception_state;

      auto* script_state = GetScriptState();
      ScriptState::Scope scope(script_state);

      if (ReadableStreamBYOBRequest* request = Controller()->byobRequest()) {
        DOMArrayPiece view(request->view().Get());
        data_buffer =
            data_buffer.first(std::min(data_buffer.size(), view.ByteLength()));
        view.ByteSpan().copy_prefix_from(data_buffer);
        request->respond(script_state, data_buffer.size(), exception_state);
      } else {
        auto buffer = NotShared(DOMUint8Array::Create(data_buffer));
        Controller()->enqueue(script_state, buffer, exception_state); // [3]
      }

      result = data_pipe_->EndReadData(data_buffer.size()); // [2]
      DCHECK_EQ(result, MOJO_RESULT_OK);

      // Send data to DevTools protocol.
      probe::DirectTCPSocketChunkReceived(*script_state, inspector_id_,
                                          data_buffer);
      break;
    }
    [...]
  }
}

```

`Controller()->enqueue()` leads to JS sync execution if `Object.prototype.then` has getter. This is as follows.

- `ReadableByteStreamController::enqueue`
  - `ReadableByteStreamController::Enqueue`
    - `ReadableByteStreamController::ProcessReadRequestsUsingQueue`
      - `ReadableByteStreamController::FillReadRequestFromQueue`
        - `ReadableStreamDefaultReader::DefaultReaderReadRequest::ChunkSteps`
          - `ScriptPromiseResolver::Resolve`

Please note that [`ScriptPromiseResolver::Resolve` executes `Object.prototype.then` getter synchronously according to step 9 of `27.2.1.3.2 Promise Resolve Functions` in ECMAScript spec](https://tc39.es/ecma262/#sec-promise-resolve-functions).

Here, the attacker can leverage `ReadableStreamDefaultReader.cancel()` to invalidate `data_pipe_`. The function makes `data_pipe_` invalid along with the following call stack.

- `ReadableStreamDefaultReader.cancel()` (JS)
  - `ReadableStreamGenericReader::cancel` (IDL)
    - `ReadableStreamGenericReader::cancel()` (C++)
      - `ReadableStreamGenericReader::GenericCancel`
        - `ReadableStream::Cancel()`
          - `ReadableStreamDefaultController::CancelSteps()`
            - `ReadableStream::CancelAlgorithm::Run()`
              - `ForwardingUnderlyingByteSource::Cancel()`
                - `TCPReadableStreamWrapper::CloseStream()`
                  - `TCPReadableStreamWrapper::ResetPipe()`
                    - `data_pipe_.reset()`

So, in summary, the attacker can execute `ReadableStreamDefaultReader.cancel()` and invalidate `data_pipe_` in the middle of `TCPReadableStreamWrapper::Pull()`. After that, `TCPReadableStreamWrapper::Pull()` tries to use `data_pipe_` and it's already become invalid. So, the below DCHECK fails via `->` operator. [4]

<https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/system/handle.h;l=100-103;drc=1cc7997baa714735aa78b08b94b64b02c22760ae>

```
const HandleType* operator->() const {
  DCHECK(handle_.is_valid()); // [4]
  return &handle_;
}

```
# Impact in Production

I'm now building ASan Chromium with the `DCHECK` removed. I'll share the result.

# Additional Comments

As mentioned in `Impact in Production`, I'm now checking the consequence with the `DCHECK` disabled. If it leads to an exploitable memory corruption such as UaF, I will try to write exploit. I understand I can take about 6 weeks in such a case according to [the document](https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#can-i-submit-my-report_s_and-provide-a-working-exploit-later).

# Summary

DCHECK failure in TCPReadableStreamWrapper::Pull()

# Custom Questions

#### Type of crash:

tab

#### Crash state:

This is the same as the attached `asan.log`.

```
[34006:1982733:1019/034901.143966:FATAL:mojo/public/cpp/system/handle.h:101] DCHECK failed: handle_.is_valid().
0   Chromium Framework                  0x00000003706478c0 base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 28
1   Chromium Framework                  0x0000000370613014 base::debug::StackTrace::StackTrace(unsigned long) + 480
2   Chromium Framework                  0x00000003703081cc logging::LogMessage::Flush() + 656
3   Chromium Framework                  0x0000000370307d8c logging::LogMessage::~LogMessage() + 76
4   Chromium Framework                  0x00000003702c7568 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() + 100
5   Chromium Framework                  0x00000003702c63ec logging::CheckError::~CheckError() + 132
6   Chromium Framework                  0x00000003702c6528 logging::CheckError::~CheckError() + 12
7   Chromium Framework                  0x0000000385e8a22c blink::TCPReadableStreamWrapper::Pull() + 1492
8   Chromium Framework                  0x0000000385e6d378 blink::(anonymous namespace)::ForwardingUnderlyingByteSource::Pull(blink::ReadableByteStreamController*, blink::ExceptionState&) + 588
9   Chromium Framework                  0x000000037ea6d118 blink::ReadableStream::PullAlgorithm::Run(blink::ScriptState*, int, base::span<v8::Local<v8::Value>, 18446744073709551615ul, v8::Local<v8::Value>*>) + 1376
10  Chromium Framework                  0x000000037ea0665c blink::ReadableByteStreamController::CallPullIfNeeded(blink::ScriptState*, blink::ReadableByteStreamController*) + 680
11  Chromium Framework                  0x000000037ea1427c blink::ReadableByteStreamController::PullSteps(blink::ScriptState*, blink::ReadRequest*, blink::ExceptionState&) + 1016
12  Chromium Framework                  0x000000037ea9399c blink::ReadableStreamDefaultReader::Read(blink::ScriptState*, blink::ReadableStreamDefaultReader*, blink::ReadRequest*, blink::ExceptionState&) + 836
13  Chromium Framework                  0x000000037ea935c8 blink::ReadableStreamDefaultReader::read(blink::ScriptState*, blink::ExceptionState&) + 420
14  Chromium Framework                  0x00000003812b4898 blink::(anonymous namespace)::v8_readable_stream_default_reader::ReadOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) + 592
15  ???                                 0x00000003f79b0618 0x0 + 17039033880
16  ???                                 0x00000003f79adc14 0x0 + 17039023124
17  ???                                 0x00000003f7a669f0 0x0 + 17039780336
18  ???                                 0x00000003f7d66c78 0x0 + 17042926712
19  ???                                 0x00000003f7a27608 0x0 + 17039521288
20  ???                                 0x00000003f79a7214 0x0 + 17038995988
21  Chromium Framework                  0x000000035f9a27e0 v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 6020
22  Chromium Framework                  0x000000035f9a5b9c v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 380
23  Chromium Framework                  0x000000035f9a6630 v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) + 92
24  Chromium Framework                  0x000000035fa7960c v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) + 1048
25  Chromium Framework                  0x000000035fa7911c v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) + 396
26  Chromium Framework                  0x00000003699672a4 blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() + 368
27  Chromium Framework                  0x000000037c06723c blink::Agent::PerformMicrotaskCheckpoint() + 300
28  Chromium Framework                  0x00000003699a9444 blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() + 1880
29  Chromium Framework                  0x00000003699f4034 blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() + 1948
30  Chromium Framework                  0x0000000369a04754 blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 480
31  Chromium Framework                  0x0000000369a33b2c base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::* const&)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), blink::scheduler::MainThreadTaskQueue*>, base::internal::BindState<true, true, false, void (blink::scheduler::MainThreadTaskQueue::*)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::internal::BindStateBase*, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 316
32  Chromium Framework                  0x00000003704da444 base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const & + 468
33  Chromium Framework                  0x00000003704da1b0 base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 492
34  Chromium Framework                  0x00000003704a0c0c base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*) + 708
35  Chromium Framework                  0x00000003704a06f4 base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&) + 608
36  Chromium Framework                  0x000000037050d55c base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 3800
37  Chromium Framework                  0x000000037050c0b4 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 404
38  Chromium Framework                  0x00000003703319f8 base::MessagePumpDefault::Run(base::MessagePump::Delegate*) + 480
39  Chromium Framework                  0x000000037050efa4 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 1640
40  Chromium Framework                  0x00000003703f90a0 base::RunLoop::Run(base::Location const&) + 1164
41  Chromium Framework                  0x000000037a8a902c content::RendererMain(content::MainFunctionParams) + 2456
42  Chromium Framework                  0x000000036c80cd80 content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) + 1180
43  Chromium Framework                  0x000000036c80f2c0 content::ContentMainRunnerImpl::Run() + 1484
44  Chromium Framework                  0x000000036c80ab20 content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) + 2320
45  Chromium Framework                  0x000000036c80af98 content::ContentMain(content::ContentMainParams) + 404
46  Chromium Framework                  0x000000035a6ff400 ChromeMain + 1692
47  Chromium Helper (Renderer)          0x0000000104a44ce8 main + 600
48  dyld                                0x0000000195a9dd54 start + 7184
Crash keys:
  "gpu-glver" = "OpenGL ES 3.0.0 (ANGLE 2.1 git hash: unknown hash)"
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "3.00"
  "gpu-psver" = "3.00"
  "gpu-driver" = "26.0"
  "gpu_count" = "1"
  "gpu-devid" = "0x0000"
  "gpu-venid" = "0x106b"
  "view-count" = "2"
  "loaded-origin-0" = "http://localhost:8889"
  "web-frame-count" = "1"
  "renderer_foreground" = "true"
  "v8_ro_space_firstpage_address" = "0x107a00000000"
  "v8_isolate_address" = "0x633000020000"
  "variations" = "e8e963da-3f4a17df,6f27bc8a-3f4a17df,c203d55b-3f4a17df,a9ecc7b4-3f4a17df,a66dbd64-71c38a98,e32097a3-3f4a17df,102166ac-3f4a17df,96d0306-9a7ed248,89986dbe-3f01b610,f2b6a878-3f4a17df,580a9761-ef4576b6,be9ac099-f9095748,66abf9c6-3f4a17df,a1e5b5f5-3f4a17df,a66fd611-3f4a17df,de2a296c-3f4a17df,ff6056ba-3f4a17df,48a8d64c-3f4a17df,836f1ad3-3f4a17df,94e21eca-3f4a17df,47a0a3b2-3f4a17df,1b0dc97-3f4a17df,2c561bd6-3f4a17df,9feae158-212c8bfa,97063883-1f820d08,d4754f61-3f4a17df,8f80c10-78198108,a62c052e-3f4a17df,a4ca7cb1-3f4a17df,601dc969-3f4a17df,da968c94-3f4a17df,ae727645-d13781e7,facc182b-d8918098,d3aecf6a-3f4a17df,28c4043d-b9a3663e,e43b13da-3f4a17df,ec937206-3f4a17df,26016f9f-4df4f25e,5eb9e4fc-3f4a17df,cad2b12b-8ef57898,40ff6f40-fb6df2c9,fb92da45-3f4a17df,9540e055-f2018abe,3fff8fa8-3f4a17df,797fe373-3f4a17df,6d2935ee-3f4a17df,17a43872-3f4a17df,a88cddf3-3f4a17df,1ffefb1a-3f4a17df,f45c108d-65bced95,f7d06457-e9d42fcd,bcb58f65-3f4a17df,d512da3a-513c429d,54d601a5-3f4a17df,29990ed3-3f4a17df,bf9ed750-d9924ac7,bca7ba0b-8cb78501,999e8980-6ec7edcb,ccd5ee73-5ca664ae,46d7c84e-3f4a17df,4a2d56fe-3f4a17df,5133eb43-307b98b1,f314f5b9-89ed2dc6,6e4a21fe-efc28565,7ad58837-eb518a56,43bba9d8-d1b30714,78634d5f-2ba5dc1c,a36728e6-5a9796c4,4749874c-455e925b,f44c0371-3f4a17df,820f17d2-e484eeec,40debc11-3f4a17df,c38c2f13-711c494e,12733ec4-3f4a17df,4ffe7de9-3f4a17df,44666d99-3d47f4f4,a2db6721-3f4a17df,9c4e9263-f2280ca0,e14ee5ee-c6d6098d,fd051c38-3f4a17df,a98def31-2a5a8f5d,578a5e44-3f4a17df,fc1790de-3f4a17df,11d973f6-3f4a17df,35c106c9-3f4a17df,7dcaa2cd-3f4a17df,e6d68be3-105bef75,f6f5c542-3f4a17df,5e05ef36-3f4a17df,5e4b4ebb-974ef86d,18324944-3f4a17df,a85f151b-3f4a17df,3779be93-3f4a17df,707ac2b5-3f4a17df,de785b07-3f4a17df,7d9c4006-3f4a17df,8e9d6ad-3f4a17df,d7ce3099-d992c41f,caf19648-74472b0b,3b02c079-3f4a17df,54b15be4-1f4e6d62,669a7db8-3f4a17df,68f499c8-d24710ce,350559e5-3f4a17df,a05c89eb-67c903d4,91cba98-b3b3bb94,87684b46-4af1dc7d,c75c6bbe-3f4a17df,4eb998ce-3f4a17df,dd2c99d6-3f4a17df,4c64b66a-3f4a17df,3e15bfc6-3f4a17df,e3b0362b-67842f78,af41f030-3f4a17df,6e4912ad-3f4a17df,4fdf8ca1-3f4a17df,2f4e13c7-3f4a17df,8f4b3221-3f4a17df,779782d3-3f4a17df,e5c8270a-3f4a17df,a2d45efe-2319ef5a,ef3132a9-3f4a17df,3042ad4b-ad2fa222,7e6af697-3f4a17df,7ffaf59b-fa502eff,898b1ac3-3f4a17df,151258bf-3f4a17df,a716fea0-3f4a17df,3e672fd9-b8a67bb3,ae1581ef-35f6ea04,893cc7a4-3f4a17df,d500ce87-3f4a17df,3c978b59-3f4a17df,255aa854-194ea635,c297985a-3f4a17df,e41e244a-3f4a17df,acf2401-fc990a6f,2e7369a1-4aceb943,95a095bd-3f4a17df,96d006a-c3a49e71,f6264095-c3f8eab0,f42905ff-3f4a17df,b33256c0-3f4a17df,2faf225b-3f4a17df,d42e15c-3d47f4f4,7d05570e-76a4e021,864a51e5-aa32be6,1f70f502-3f4a17df,4146cc26-775f6248,e9844d40-3f4a17df,2b68be8f-3f4a17df,ad9b71e2-3f4a17df,98300167-3f4a17df,bc20eba6-3f4a17df,d1ae5bf4-3f4a17df,4be78f74-3f4a17df,15d1b2d8-3f4a17df,c408951f-3f4a17df,1683ee3a-b7cf2715,3dbad317-3f4a17df,e253e9e-3f4a17df,cad46b80-3f4a17df,8bccc03b-3f4a17df,57e6ff6b-3f4a17df,70404afa-803f8fc4,fecdbadb-3f4a17df,e6ed801e-cf4f6ead,3f032b9f-803f8fc4,6ff79bbe-3f4a17df,5a474f9e-3f4a17df,c823d1e9-3d47f4f4,66657049-3f4a17df,36860c1b-3f4a17df,7262ef2c-140d00b2,f93c9364-3f4a17df,b4c2bd17-23db2647,fca39b9a-3f4a17df,6ec84df5-3f4a17df,b86bee04-3f4a17df,9e5c75f1-30e1b12b,4d625646-3f4a17df,1dfb980c-3f4a17df,24b6a44d-1623a499,2394f90f-ecc8f8cf,d5f746a4-39aaf314,c2a9e35c-3f4a17df,bb84837d-3f4a17df,56aa5797-e5fec5a6,bfc33382-3f4a17df,54be7848-3f4a17df,e2d38844-3f4a17df,5c131b25-3f4a17df,eef5d69a-1dca273f,da493d3c-3f4a17df,72bafd3e-cdb4c186,f3ed486d-3f4a17df,81c84cff-e4e4c9a,b3c54bb3-88fcaf7d,4076100b-3f4a17df,8c162025-3d47f4f4,63c162ac-b1e84566,68fef0c-3f4a17df,3ac9fcb9-3f4a17df,10713630-3f4a17df,b76b514f-3ac589b9,741e95d4-3f4a17df,8f418b04-299bae22,d3566fbd-c6f74b94,e47d4c22-3f4a17df,147e9ecd-3f4a17df,bcb143fe-3f4a17df,b9ffbd4a-35efc336,d06639a1-3f4a17df,ed2195eb-3f4a17df,de028327-70abd7a5,2ca06d17-3f4a17df,a2f28ef8-d7d235fa,5abe5347-3f4a17df,35a386c3-3f4a17df,45a2f2f-f9e1b5a8,6495cb0f-3f4a17df,89eb0046-3f4a17df,88e285c2-3f4a17df,afeeb5d0-3f4a17df,186d6e2c-36c0e608,6cc45990-3f4a17df,dca2449f-3f4a17df,d5954b6b-3f4a17df,f9664fa0-3f4a17df,66b7a83f-3f4a17df,d721a76b-3f4a17df,137f6fe-3f4a17df,951dcd0c-3f4a17df,a890eff4-3f4a17df,4ea303a6-ecbb250e,ab7eb98c-3f4a17df,258151b3-3f4a17df,19593c6e-3f4a17df,c92d2cc4-3f4a17df,7c0d937f-3f4a17df,5eb745a8-3f4a17df,aa540f4f-3f4a17df,b56c57ae-8924bcae,35d20c89-3f4a17df,30cf4980-61673e6,82b178a6-3f4a17df,9850104b-395bafa,19e446cd-3f4a17df,f613598-3f4a17df,f3b6291d-7fa80c0f,bf46f37a-3f4a17df,40de0170-3f4a17df,5c78b732-3f4a17df,2f0a9b74-3f4a17df,f112d133-3f4a17df,8ec87690-cb114380,e6ec9393-3f4a17df,82b6db25-182c7a44,39bb70f9-3f4a17df,ea0d881d-fd860968,d0fa45e6-3f4a17df,2bac9a6a-3f4a17df,ff8b9cdb-3f4a17df,53c64de7-2433617a,e3559213-3f4a17df,58065933-e77f02dd,d990c4ac-3f4a17df,a374fdf0-964ff297,4c4325b3-d3bca005,23226e84-65aafa13,198413d6-3f4a17df,5870a003-3f4a17df,8e8365ea-3f4a17df,53fa9d2a-3f4a17df,4e83575c-3f4a17df,6ef0294d-3f4a17df,5baf22bc-3f4a17df,c8997723-3f4a17df,755d95c0-3f4a17df,3797f84b-3f4a17df,52a20523-3f4a17df,d0083347-3ec702d4,ef4764d7-88fcaf7d,2bac45ad-3f4a17df,613081e8-3f4a17df,c49d2b35-3f4a17df,377002b7-3f4a17df,cb03b921-3f4a17df,17d50bfc-3f4a17df,2b998963-2b8c9ae,935eb749-7a935877,e2d2a641-baec5b64,ea89c38c-3f4a17df,bc7471e4-3f4a17df,30182132-3f4a17df,94b88ba6-3f4a17df,1fce7d57-3f4a17df,ba98e1e4-3f4a17df,e8c68789-49a20295,dd8dccfb-3f4a17df,8b679bb8-3f4a17df,b0f15b33-b0f15b33,739df952-739df952,95ba3780-3f4a17df,cbe862f6-cbe862f6,15607410-b6e8dbb7,ad4acdda-3f4a17df,f48c01d3-6eb2bd2b,b1ceb06f-3f4a17df,14b2973a-5659f416,a39574eb-3f4a17df,ba6dd758-3f4a17df,db59f83a-3f4a17df,80b60e4a-3f4a17df,533ac6d2-3f4a17df,c1e0d32e-3f4a17df,1b07e46e-82669c6,bea4a9c2-94315184,2f6246c2-3f4a17df,7d758b3c-3f4a17df,d04818be-3f4a17df,e1933810-497e1286,45e0e828-3f4a17df,1ddbf293-3f4a17df,51d22fd4-3f4a17df,aa8204ea-3f4a17df,dd22be30-3d47f4f4,6332ffaf-3f4a17df,2e2ec567-3898461f,5910121-3f4a17df,f9a6f6e9-3f4a17df,595f5eb0-f23d1dea,e0e211ad-e0e211ad,bce5ae48-3f4a17df,f079e901-3f4a17df,e1adfff5-3f4a17df,638418b3-3f4a17df,e0041356-e8edc07e,1caa3332-20af8ffe,e11c0dd9-3586c521,b357b792-3f4a17df,f4f00e05-ca7d8d80,"
  "num-experiments" = "366"
  "chrome-trace-id" = "5123010722772190509"
  "reentry_guard_tls_slot" = "265"
  "switch-15" = "--seatbelt-client=133"
  "switch-14" = "--trace-process-track-uuid=3475578837407813278"
  "switch-13" = "--variations-seed-version"
  "switch-12" = "--field-trial-handle=1718379636,r,7232615197078900799,1085004410"
  "switch-11" = "--metrics-shmem-handle=1752395122,r,15386681632773476542,1748350"
  "switch-10" = "--shared-files"
  "switch-9" = "--launch-time-ticks=134544702110"
  "switch-8" = "--time-ticks-at-unix-epoch=-1760678787022907"
  "switch-7" = "--renderer-client-id=10"
  "switch-6" = "--enable-main-frame-before-activation"
  "switch-5" = "--enable-gpu-memory-buffer-compositor-resources"
  "switch-4" = "--enable-zero-copy"
  "switch-3" = "--num-raster-threads=4"
  "switch-2" = "--lang=ja"
  "switch-1" = "--origin-trial-disabled-features=CanvasTextNg|WebAssemblyCustomD"
  "num-switches" = "17"
  "commandline-enabled-feature-3" = "MulticastInDirectSockets"
  "commandline-enabled-feature-2" = "DirectSocketsInSharedWorkers"
  "commandline-enabled-feature-1" = "DirectSocketsInServiceWorkers"
  "osarch" = "arm64"
  "pid" = "34006"
  "ptype" = "renderer"

Received signal 6
0   Chromium Framework                  0x00000003706478c0 base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 28
1   Chromium Framework                  0x0000000370613014 base::debug::StackTrace::StackTrace(unsigned long) + 480
2   Chromium Framework                  0x00000003706476f4 base::debug::(anonymous namespace)::StackDumpSignalHandler(int, __siginfo*, void*) + 1652
3   libsystem_platform.dylib            0x0000000195e66744 _sigtramp + 56
4   libsystem_pthread.dylib             0x0000000195e5c888 pthread_kill + 296
5   libsystem_c.dylib                   0x0000000195d62808 abort + 124
6   Chromium Framework                  0x00000003703096ec logging::LogMessage::HandleFatal(unsigned long, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) const + 980
7   Chromium Framework                  0x0000000370308c38 logging::LogMessage::Flush() + 3324
8   Chromium Framework                  0x0000000370307d8c logging::LogMessage::~LogMessage() + 76
9   Chromium Framework                  0x00000003702c7568 logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() + 100
10  Chromium Framework                  0x00000003702c63ec logging::CheckError::~CheckError() + 132
11  Chromium Framework                  0x00000003702c6528 logging::CheckError::~CheckError() + 12
12  Chromium Framework                  0x0000000385e8a22c blink::TCPReadableStreamWrapper::Pull() + 1492
13  Chromium Framework                  0x0000000385e6d378 blink::(anonymous namespace)::ForwardingUnderlyingByteSource::Pull(blink::ReadableByteStreamController*, blink::ExceptionState&) + 588
14  Chromium Framework                  0x000000037ea6d118 blink::ReadableStream::PullAlgorithm::Run(blink::ScriptState*, int, base::span<v8::Local<v8::Value>, 18446744073709551615ul, v8::Local<v8::Value>*>) + 1376
15  Chromium Framework                  0x000000037ea0665c blink::ReadableByteStreamController::CallPullIfNeeded(blink::ScriptState*, blink::ReadableByteStreamController*) + 680
16  Chromium Framework                  0x000000037ea1427c blink::ReadableByteStreamController::PullSteps(blink::ScriptState*, blink::ReadRequest*, blink::ExceptionState&) + 1016
17  Chromium Framework                  0x000000037ea9399c blink::ReadableStreamDefaultReader::Read(blink::ScriptState*, blink::ReadableStreamDefaultReader*, blink::ReadRequest*, blink::ExceptionState&) + 836
18  Chromium Framework                  0x000000037ea935c8 blink::ReadableStreamDefaultReader::read(blink::ScriptState*, blink::ExceptionState&) + 420
19  Chromium Framework                  0x00000003812b4898 blink::(anonymous namespace)::v8_readable_stream_default_reader::ReadOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) + 592
20  ???                                 0x00000003f79b0618 0x0 + 17039033880
21  ???                                 0x00000003f79adc14 0x0 + 17039023124
22  ???                                 0x00000003f7a669f0 0x0 + 17039780336
23  ???                                 0x00000003f7d66c78 0x0 + 17042926712
24  ???                                 0x00000003f7a27608 0x0 + 17039521288
25  ???                                 0x00000003f79a7214 0x0 + 17038995988
26  Chromium Framework                  0x000000035f9a27e0 v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 6020
27  Chromium Framework                  0x000000035f9a5b9c v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 380
28  Chromium Framework                  0x000000035f9a6630 v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) + 92
29  Chromium Framework                  0x000000035fa7960c v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) + 1048
30  Chromium Framework                  0x000000035fa7911c v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) + 396
31  Chromium Framework                  0x00000003699672a4 blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() + 368
32  Chromium Framework                  0x000000037c06723c blink::Agent::PerformMicrotaskCheckpoint() + 300
33  Chromium Framework                  0x00000003699a9444 blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() + 1880
34  Chromium Framework                  0x00000003699f4034 blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() + 1948
35  Chromium Framework                  0x0000000369a04754 blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 480
36  Chromium Framework                  0x0000000369a33b2c base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::* const&)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), blink::scheduler::MainThreadTaskQueue*>, base::internal::BindState<true, true, false, void (blink::scheduler::MainThreadTaskQueue::*)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::internal::BindStateBase*, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 316
37  Chromium Framework                  0x00000003704da444 base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const & + 468
38  Chromium Framework                  0x00000003704da1b0 base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 492
39  Chromium Framework                  0x00000003704a0c0c base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*) + 708
40  Chromium Framework                  0x00000003704a06f4 base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&) + 608
41  Chromium Framework                  0x000000037050d55c base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 3800
42  Chromium Framework                  0x000000037050c0b4 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 404
43  Chromium Framework                  0x00000003703319f8 base::MessagePumpDefault::Run(base::MessagePump::Delegate*) + 480
44  Chromium Framework                  0x000000037050efa4 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 1640
45  Chromium Framework                  0x00000003703f90a0 base::RunLoop::Run(base::Location const&) + 1164
46  Chromium Framework                  0x000000037a8a902c content::RendererMain(content::MainFunctionParams) + 2456
47  Chromium Framework                  0x000000036c80cd80 content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) + 1180
48  Chromium Framework                  0x000000036c80f2c0 content::ContentMainRunnerImpl::Run() + 1484
49  Chromium Framework                  0x000000036c80ab20 content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) + 2320
50  Chromium Framework                  0x000000036c80af98 content::ContentMain(content::ContentMainParams) + 404
51  Chromium Framework                  0x000000035a6ff400 ChromeMain + 1692
52  Chromium Helper (Renderer)          0x0000000104a44ce8 main + 600
53  dyld                                0x0000000195a9dd54 start + 7184
[end of stack trace]

```
#### Reporter credit:

canalun (@i\_am\_canalun)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- asan.log (text/plain, 23.6 KB)
- diff.patch (text/x-diff, 4.9 KB)
- poc.html (text/html, 396 B)
- asan2.log (text/plain, 8.3 KB)
- diff2.patch (text/x-diff, 6.1 KB)
- poc.mov (video/quicktime, 26.1 MB)

## Timeline

### i....@gmail.com (2025-10-18)

My bad, I should've set the title as `DCHECK failure in ScopedHandleBase::operator->()`.

### i....@gmail.com (2025-10-19)

# Impact for Production

I tried the poc with DCHECK disabled, and the crash doesn't occur.
Specifically, I disabled these two DCHECKs.

<https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/system/handle.h;l=101;drc=1cc7997baa714735aa78b08b94b64b02c22760ae>

```
  const HandleType* operator->() const {
    DCHECK(handle_.is_valid());
    return &handle_;
  }

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc;l=123;drc=34a6d62b1a9aad2d48b504842feb03ef20b6185c>

```
void TCPReadableStreamWrapper::Pull() {
  [...]
  switch (result) {
    case MOJO_RESULT_OK: {
      [...]
      if (ReadableStreamBYOBRequest* request = Controller()->byobRequest()) {
        [...]
      } else {
        [...]
      }

      result = data_pipe_->EndReadData(data_buffer.size());
      DCHECK_EQ(result, MOJO_RESULT_OK);

      // Send data to DevTools protocol.
      probe::DirectTCPSocketChunkReceived(*script_state, inspector_id_,
                                          data_buffer);
      break;
    }
    [...]
  }
}

```

However, I found another issue. **If you follow the reproduction steps as explained but with DevTools opened and with the above two DCHECKs disabled, another crash occurs.** And it seems harmful. (The below is the same as the attached `asan2.log`.)

```
Received signal 11 SEGV_ACCERR 000166bdc000
0   Chromium Framework                  0x000000037063d2bc base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 28
1   Chromium Framework                  0x0000000370608a10 base::debug::StackTrace::StackTrace(unsigned long) + 480
2   Chromium Framework                  0x000000037063d0f0 base::debug::(anonymous namespace)::StackDumpSignalHandler(int, __siginfo*, void*) + 1652
3   libsystem_platform.dylib            0x0000000195e66744 _sigtramp + 56
4   libclang_rt.asan_osx_dynamic.dylib  0x0000000104df4a78 __asan_memcpy + 232
5   Chromium Framework                  0x0000000369a923c4 void blink::Vector<unsigned char, 0u, blink::PartitionAllocator>::Append<unsigned char>(unsigned char const*, unsigned int) + 512
6   Chromium Framework                  0x000000037d308300 blink::protocol::Binary::fromSpan(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) + 72
7   Chromium Framework                  0x000000037cf4e784 blink::InspectorNetworkAgent::DirectTCPSocketChunkReceived(unsigned long long, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) + 312
8   Chromium Framework                  0x0000000380093070 blink::probe::DirectTCPSocketChunkReceivedImpl(blink::ScriptState&, unsigned long long, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) + 424
9   Chromium Framework                  0x0000000385e7d45c blink::TCPReadableStreamWrapper::Pull() + 1360
10  Chromium Framework                  0x0000000385e6062c blink::(anonymous namespace)::ForwardingUnderlyingByteSource::Pull(blink::ReadableByteStreamController*, blink::ExceptionState&) + 588
11  Chromium Framework                  0x000000037ea60bc8 blink::ReadableStream::PullAlgorithm::Run(blink::ScriptState*, int, base::span<v8::Local<v8::Value>, 18446744073709551615ul, v8::Local<v8::Value>*>) + 1376
12  Chromium Framework                  0x000000037e9fa10c blink::ReadableByteStreamController::CallPullIfNeeded(blink::ScriptState*, blink::ReadableByteStreamController*) + 680
13  Chromium Framework                  0x000000037ea07d2c blink::ReadableByteStreamController::PullSteps(blink::ScriptState*, blink::ReadRequest*, blink::ExceptionState&) + 1016
14  Chromium Framework                  0x000000037ea8744c blink::ReadableStreamDefaultReader::Read(blink::ScriptState*, blink::ReadableStreamDefaultReader*, blink::ReadRequest*, blink::ExceptionState&) + 836
15  Chromium Framework                  0x000000037ea87078 blink::ReadableStreamDefaultReader::read(blink::ScriptState*, blink::ExceptionState&) + 420
16  Chromium Framework                  0x00000003812a8348 blink::(anonymous namespace)::v8_readable_stream_default_reader::ReadOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) + 592
17  ???                                 0x00000003f79b0618 0x0 + 17039033880
18  ???                                 0x00000003f79adc14 0x0 + 17039023124
19  ???                                 0x00000003f7a669f0 0x0 + 17039780336
20  ???                                 0x00000003f7d66c78 0x0 + 17042926712
21  ???                                 0x00000003f7a27608 0x0 + 17039521288
22  ???                                 0x00000003f79a7214 0x0 + 17038995988
23  Chromium Framework                  0x000000035f999e8c v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 6020
24  Chromium Framework                  0x000000035f99d248 v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) + 380
25  Chromium Framework                  0x000000035f99dcdc v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) + 92
26  Chromium Framework                  0x000000035fa70cb8 v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) + 1048
27  Chromium Framework                  0x000000035fa707c8 v8::internal::MicrotaskQueue::PerformCheckpointInternal(v8::Isolate*) + 396
28  Chromium Framework                  0x000000036995de8c blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() + 368
29  Chromium Framework                  0x000000037c05b2a0 blink::Agent::PerformMicrotaskCheckpoint() + 300
30  Chromium Framework                  0x00000003699a002c blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() + 1880
31  Chromium Framework                  0x00000003699eac1c blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() + 1948
32  Chromium Framework                  0x00000003699fb33c blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 480
33  Chromium Framework                  0x0000000369a2a714 base::internal::Invoker<base::internal::FunctorTraits<void (blink::scheduler::MainThreadTaskQueue::* const&)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), blink::scheduler::MainThreadTaskQueue*>, base::internal::BindState<true, true, false, void (blink::scheduler::MainThreadTaskQueue::*)(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*), base::internal::UnretainedWrapper<blink::scheduler::MainThreadTaskQueue, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::internal::BindStateBase*, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 316
34  Chromium Framework                  0x00000003704cfe40 base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const & + 468
35  Chromium Framework                  0x00000003704cfbac base::sequence_manager::internal::TaskQueueImpl::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) + 492
36  Chromium Framework                  0x0000000370496608 base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*) + 708
37  Chromium Framework                  0x00000003704960d8 base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&) + 608
38  Chromium Framework                  0x0000000370502f58 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) + 3800
39  Chromium Framework                  0x0000000370501ab0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() + 404
40  Chromium Framework                  0x00000003703273f4 base::MessagePumpDefault::Run(base::MessagePump::Delegate*) + 480
41  Chromium Framework                  0x00000003705049a0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) + 1640
42  Chromium Framework                  0x00000003703eea90 base::RunLoop::Run(base::Location const&) + 1164
43  Chromium Framework                  0x000000037a89d090 content::RendererMain(content::MainFunctionParams) + 2456
44  Chromium Framework                  0x000000036c803048 content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) + 1180
45  Chromium Framework                  0x000000036c805588 content::ContentMainRunnerImpl::Run() + 1484
46  Chromium Framework                  0x000000036c800de8 content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) + 2320
47  Chromium Framework                  0x000000036c801260 content::ContentMain(content::ContentMainParams) + 404
48  Chromium Framework                  0x000000035a6f7390 ChromeMain + 1692
49  Chromium Helper (Renderer)          0x0000000104a70ce8 main + 600
50  dyld                                0x0000000195a9dd54 start + 7184
[end of stack trace]

```

This is caused because opening the DevTools activates the following `probe::DirectTCPSocketChunkReceived`. [4]

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc;l=126;drc=34a6d62b1a9aad2d48b504842feb03ef20b6185c>

```
void TCPReadableStreamWrapper::Pull() {
  if (!GetScriptState()->ContextIsValid())
    return;

  DCHECK(data_pipe_);

  base::span<const uint8_t> data_buffer;
  auto result =
      data_pipe_->BeginReadData(MOJO_BEGIN_READ_DATA_FLAG_NONE, data_buffer);
  switch (result) {
    case MOJO_RESULT_OK: {
      [...]
      if (ReadableStreamBYOBRequest* request = Controller()->byobRequest()) {
        DOMArrayPiece view(request->view().Get());
        data_buffer =
            data_buffer.first(std::min(data_buffer.size(), view.ByteLength()));
        view.ByteSpan().copy_prefix_from(data_buffer);
        request->respond(script_state, data_buffer.size(), exception_state);
      } else {
        auto buffer = NotShared(DOMUint8Array::Create(data_buffer));
        Controller()->enqueue(script_state, buffer, exception_state);
      }

      result = data_pipe_->EndReadData(data_buffer.size());
      DCHECK_EQ(result, MOJO_RESULT_OK); // disabled

      // Send data to DevTools protocol.
      probe::DirectTCPSocketChunkReceived(*script_state, inspector_id_,
                                          data_buffer); // [4]
      break;
    }

    [...]
  }
}

```

Then the below code is executed and `protocol::Binary::fromSpan` is called with invalid `data`. [5]

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_network_agent.cc;l=2218-2228;drc=822482f9ed46bed23677c3dfe05cfa0dc5df3bfd>

```
void InspectorNetworkAgent::DirectTCPSocketChunkReceived(
    uint64_t identifier,
    base::span<const uint8_t> data) {
  if (!report_direct_socket_traffic_.Get()) {
    return;
  }
  GetFrontend()->directTCPSocketChunkReceived(
      IdentifiersFactory::SubresourceRequestId(identifier),
      protocol::Binary::fromSpan(data), // [5]
      base::TimeTicks::Now().since_origin().InSecondsF());
}

```
# Mitigation

## fundamental solution

It seems dangerous that we can cancel `ReadableStreamDefaultReader` which is being used. So, it would be nice to adopt the concept of lock to `ReadableStreamDefaultReader` as well as `ReadableStream`. Actually `ReadableStream` cannot be cancelled when it's being read. In fact, if you change the poc to cancel not `defaultReader` but `readableStream`, it will cause a JS error and prevents the crash: `TypeError: Failed to execute 'cancel' on 'ReadableStream': Cannot cancel a locked stream`.

## quick solution

The above mitigation is fundamental, but that may need the spec fix also. So I think it's quick and enough to add handler validation (`is_valid()`) like below. [6]

```
void TCPReadableStreamWrapper::Pull() {
  [...]
  switch (result) {
    case MOJO_RESULT_OK: {
      [...]

      CHECK(data_pipe_.is_valid()); // [6]
      result = data_pipe_->EndReadData(data_buffer.size());
      DCHECK_EQ(result, MOJO_RESULT_OK);

      // Send data to DevTools protocol.
      probe::DirectTCPSocketChunkReceived(*script_state, inspector_id_,
                                          data_buffer);
      break;
    }
    [...]
  }
}

```

You can do validation in if clause instead of `CHECK`. Actually, [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/data_pipe_bytes_consumer.cc;l=181;drc=1cc7997baa714735aa78b08b94b64b02c22760ae) and [there](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/url_loader/sync_load_context.cc;l=273;drc=1cc7997baa714735aa78b08b94b64b02c22760ae) already use `is_valid()` as an if condition.

FYI, please note that, also in the case of BYOB, `request->respond(script_state, data_buffer.size(), exception_state);` can cause synchronous JS execution. So mitigation is necessary for the both cases.

# Bisect

## `probe::DirectTCPSocketChunkReceived`

Commit [4416514](https://source.chromium.org/chromium/chromium/src/+/441651498a34309eff4224c5b67f633c93597552) adds `probe::DirectTCPSocketChunkReceived`.

## reentrancy by sync JS exec

And, for reentrancy by sync JS exec, commit [de0b805](https://source.chromium.org/chromium/chromium/src/+/de0b805eb61f0c342f1da7d2b51f088b1ac727d2) is the one adopting it.

This commit implemented ReadableStream for TCPSocket first. This commit has already re-entrancy path and it looks aware of that judging from the comment. [7]

```
void TCPReadableStreamWrapper::ReadFromPipeAndEnqueue() {
  [...]
  auto result = data_pipe_->BeginReadData(&buffer, &buffer_num_bytes,
                                          MOJO_BEGIN_READ_DATA_FLAG_NONE);
  switch (result) {
    case MOJO_RESULT_OK: {
      in_two_phase_read_ = true;
      // EnqueueBytes() may re-enter this method via pull(). // [7]
      EnqueueBytes(buffer, buffer_num_bytes);
      data_pipe_->EndReadData(buffer_num_bytes);
      [...]
    }
    [...]
  }
}

void TCPReadableStreamWrapper::EnqueueBytes(const void* source,
                                            uint32_t byte_length) {
  DVLOG(1) << "TCPReadableStreamWrapper::EnqueueBytes() this=" << this;

  auto* buffer =
      DOMUint8Array::Create(static_cast<const uint8_t*>(source), byte_length);
  controller_->Enqueue(buffer);
}

```

### i....@gmail.com (2025-10-20)

I submitted a CL. If it's alright, could I work on a fix with the CL?: <https://chromium-review.googlesource.com/c/chromium/src/+/7061692>

It seems a good opportunity for me as a contributor to learn the code :)

(Since I’ve already landed some patches before, I’m familiar with the contribution and review process.)

### ja...@chromium.org (2025-10-20)

[security shepherd]

Thanks for the bug report. I have not reproduced this yet. Looking at the POC this seems reasonable. The patch diff is removing mostly error handling code that handles secure connections -- so removing that makes it easier to reproduce using netcat without needing to setup a server.

Bug reporter, could you followup on your initial `I'm now building ASan Chromium with the DCHECK removed. I'll share the result.` statement, and when you get the stack trace, please provide the Chrome "ADDITIONAL INFORMATION" section as well so we can see the MiraclPtr verdict and any other useful information.

### ja...@chromium.org (2025-10-20)

[security shepherd]
tentatively adding Blink > Network > StreamAPI as the component.

### ja...@chromium.org (2025-10-20)

[shepherd] assigned wrong owner, so removed them.

### i....@gmail.com (2025-10-21)

Thank you for checking the report :)

I followed-up the initial statement in [c3](https://issues.chromium.org/issues/453147449#comment3).

In summary, the reproduction steps I wrote first in [c1](https://issues.chromium.org/issues/453147449#comment1) don't lead to any crash when DCHECK is disabled.

However, when you keep DevTools opened, it leads to crash when DCHECK is disabled. This means that it's supposed that you can reproduce the crash with the attached `diff2.patch`. I mean the below is the re-written reproduction step.

1. apply **`diff2.patch`** and build asan chromium.
2. exec `echo -e "UAF" | nc -l 12321` on local.
3. serve `poc.html` on local.
4. open a new tab and **open DevTools**.
5. open the served `poc.html` in the tab.
6. chromium crashes.

Also, I'd like to add the point that the crash log I got didn't any `ADDITIONAL INFORMATION`. I couldn't find any reason. (For the reference, I built asan chromium as below following [the doc](https://chromium.googlesource.com/chromium/src/+/master/docs/asan.md).) Could you please check it?

```
$ git show --format='%h' --no-patch
d464779279437

$ cat ./out/Default_asan/args.gn
# Set build arguments here. See `gn help buildargs`.
is_asan = true
is_debug = false  # Release build.

$ autoninja -C out/Default_asan chrome

```

### i....@gmail.com (2025-10-21)

`diff2.patch` = `diff.patch` + disabling two DCHECKs

### pe...@google.com (2025-10-21)

Thank you for providing more feedback. Adding the requester to the CC list.

### i....@gmail.com (2025-10-21)

Just in case, I attached a video. You can see the crash log including no `ADDITIONAL INFORMATION`.

### xi...@chromium.org (2025-10-21)

Thanks for the detailed report and submitting a CL for the fix. Looks like MiraclePtr is not enabled in renderer process, so setting severity to S1. Assigning to the original author of https://crrev.com/c/6434437, who may be able to land the fix. Thanks!

### vk...@google.com (2025-10-22)

I see that [i.am.kanaru.sato@gmail.com](mailto:i.am.kanaru.sato@gmail.com) has uploaded the CL.
But I am the assignee of the issue.
So should I copy and finish CL myself or [i.am.kanaru.sato@gmail.com](mailto:i.am.kanaru.sato@gmail.com) will take care of it?
[xinghuilu@chromium.org](mailto:xinghuilu@chromium.org)

### ch...@google.com (2025-10-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-22)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### i....@gmail.com (2025-10-24)

Now checking if it leads to leak of some important memory info. If any issue is found, I'll let you know.

### dx...@google.com (2025-10-24)

Project: chromium/src  

Branch:  main  

Author:  Vlad Krot [vkrot@google.com](mailto:vkrot@google.com)  

Link:    <https://chromium-review.googlesource.com/7079785>

Fix reentrancy issue in tcp readable stream wrapper

---


Expand for full commit details
```
     
    The root of the issue was in the fact that ScriptPromiseResolve::Resolve 
    can execute accessor of property 'then' synchronously, which with some 
    prototype magic in JS is possible to cancel socket while reading it, 
    which crashes the whole page. 
     
    Thanks i.am.kanaru.sato@gmail.com for the proposed fix 
    https://chromium-review.googlesource.com/c/chromium/src/+/7061692 which 
    only lacked correct test implementation. 
     
    Change-Id: I0d9faa757e752c7e13f60b39980e31ef2e5d9f76 
    Fixed: 453147449 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7079785 
    Reviewed-by: Simon Hangl <simonha@google.com> 
    Reviewed-by: Andrew Rayskiy <greengrape@google.com> 
    Commit-Queue: Vlad Krot <vkrot@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1534914}

```

---

Files:

- M `content/browser/direct_sockets/direct_sockets_tcp_browsertest.cc`
- M `third_party/blink/renderer/modules/direct_sockets/tcp_readable_stream_wrapper.cc`

---

Hash: [c1cf68d78c87a39e296c6c7118569a6896f74cec](https://chromiumdash.appspot.com/commit/c1cf68d78c87a39e296c6c7118569a6896f74cec)  

Date: Fri Oct 24 11:21:43 2025


---

### ch...@google.com (2025-10-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-10-24)

This V8 bug has been marked as a release blocker. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2025-10-24)

Security Merge Request Consideration: Requesting merge to extended stable (M140) because latest trunk commit (1534914) appears to be after extended stable branch point (1496484).
Security Merge Request Consideration: Requesting merge to stable (M141) because latest trunk commit (1534914) appears to be after stable branch point (1509326).
Security Merge Request Consideration: Requesting merge to beta (M142) because latest trunk commit (1534914) appears to be after beta branch point (1522585).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-10-25)

Merge review required: M142 has already been cut for stable release.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-10-25)

Merge review required: M141 is already shipping to stable.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-10-25)

Merge review required: M140 is already shipping to stable.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### vk...@google.com (2025-10-27)

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.) - <https://chromium-review.googlesource.com/c/chromium/src/+/7079785>
2. Has this fix been verified on Canary to not pose any stability regressions? - No
3. Does this fix pose any potential non-verifiable stability risks? - No
4. Does this fix pose any known compatibility risks? - No
5. Does it require manual verification by the test team? If so, please describe required testing. - No. The change is verified by automated tests.

### i....@gmail.com (2025-10-28)

Although I previously commented about additional investigation, I've had to deal with several priorities and have become unable to take the necessary time. So, please feel free to proceed with the standard triage and remediation process at your convenience. Thanks.

### vk...@google.com (2025-10-28)

Merge review required: M142 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?
   Chrome Browser: <https://chromiumdash.appspot.com/branches>
   Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>
2. What changes specifically would you like to merge? Please link to Gerrit. <https://chromium-review.googlesource.com/c/chromium/src/+/7067397>
3. Have the changes been released and tested on canary? - No.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels? - No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents> - No
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing. - No, tested via automated tests.

### sp...@google.com (2025-11-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
base value $2000, moderately mitigated (needs extension and user gesture) + 1k patch + 1k bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> base value $2000, moderately mitigated (needs extension and user gesture) + 1k patch + 1k bisect

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/453147449)*
