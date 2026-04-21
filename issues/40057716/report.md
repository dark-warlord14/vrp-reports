# Google Chrome MediaStreamTrackGenerator use after free vulnerability (TALOS-2021-1398)

| Field | Value |
|-------|-------|
| **Issue ID** | [40057716](https://issues.chromium.org/issues/40057716) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-10-26 |
| **Bounty** | $7,500.00 |

## Description

TALOS-2021-1398

Google Chrome MediaStreamTrackGenerator use after free vulnerability

Summary

A potential code execution vulnerability exists in the MediaStreamTrackGenerator functionality of Google Chrome 94.0.4606.81 (Stable) and 97.0.4674.1 (Canary). A specially-crafted web page can lead to use after free. An attacker can provide a malicious web site to trigger this vulnerability.

Tested Versions

Google Chrome 94.0.4606.81 (Stable) 
Google Chrome 97.0.4674.1 (Canary)

Product URLs

https://www.google.com/chrome/

CVSSv3 Score

8.3 - CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L

CWE

CWE-416 - Use After Free

Details

Google Chrome is a cross-platform web browser, developed by Google.

The vulnerability exists in object MediaStreamTrackGenerator which is responsible for creating streams of audio/video.

MediaStreamTrackGenerator inherits from MediaStreamTrack. Thanks to this inheritance the MediaStreamTrackGenerator object can be cloned/copied to new object, see function below .

 1:      MediaStreamTrack* MediaStreamTrack::cloneMediaStreamTrack::clone(ScriptState* script_state) {
 2:      SendLogMessage(String::Format("%s()", __func__));
 3:      MediaStreamComponent* cloned_component = Component()->Clone();
 4:      MediaStreamTrack* cloned_track = MakeGarbageCollected<MediaStreamTrack>(
 5:          ExecutionContext::From(script_state), cloned_component, ready_state_,
 6:          base::DoNothing());
 7:      DidCloneMediaStreamTrack(Component(), cloned_component);
 8:      if (image_capture_) {
 9:          cloned_track->image_capture_ = image_capture_->Clone();
10:      }
11:      return cloned_track;
12:      }
The above function is resposible for making the copy of the MediaStreamTrackGenerator object, the allocation of new memory happens at line 4. By definition when using MakeGarbageCollected, the new object wont be deleted by delete but using Olipan, which is the Chromium garbage collector.

You can create an instance of your class through MakeGarbageCollected<T>, while you may not free the object with delete, 
as Oilpan is responsible for deallocating the object once it determines the object is unreachable.
During streaming we can abort the stream using the JS function abort, which corresponds to the C++ code shown below.

1:      ScriptPromise MediaStreamAudioTrackUnderlyingSink::abort(
2:          ScriptState* script_state,
3:          ScriptValue reason,
4:          ExceptionState& exception_state) {
5:      DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
6:      Disconnect();
7:      return ScriptPromise::CastUndefined(script_state);
8:      }
The interesting part happens at line 6, where the stream gets disconnected which triggers destructor of the MediaStreamTrackGenerator object. 
However we still have copy of this object which was marked by Olipan. This process can be interrupted using Events, one of those events is onended which is triggered when status of the stream is changed. 
During this event we can try to free once again the cloned MediaStreamTrackGenerator which would lead to use-after-free vulnerability.

With proper manipulation of objects, when onended event is executed, this vulnerability could lead to control over freed memory and ultimately arbitrary code execution.

Crash Information

=================================================================
==18564==ERROR: AddressSanitizer: use-after-poison on address 0x7e80003dc378 at pc 0x7ff63031244d bp 0x00a2070fccd0 sp 0x00a2070fcd18
READ of size 8 at 0x7e80003dc378 thread T0
    #0 0x7ff63031244c in v8::internal::ObjectVisitor::VisitCustomWeakPointers(class v8::internal::HeapObject, class v8::internal::CompressedObjectSlot, class v8::internal::CompressedObjectSlot) (D:\src\out\95.0.4638.49\content_shell.exe+0x14066244c)
    #1 0x7ff639d1f9a7 in base::OnceCallback<void ()>::Run D:\src\base\callback.h:100
    #2 0x7ff639d1f9a7 in blink::MediaStreamSource::SetReadyState(enum blink::MediaStreamSource::ReadyState) D:\src\third_party\blink\renderer\platform\mediastream\media_stream_source.cc:181:36
    #3 0x7ff639c88ceb in blink::WebPlatformMediaStreamSource::FinalizeStopSource(void) D:\src\third_party\blink\renderer\platform\exported\mediastream\web_platform_media_stream_source.cc:37:13
    #4 0x7ff64548150c in blink::PushableMediaStreamAudioSource::Broker::StopSourceOnMain D:\src\third_party\blink\renderer\modules\breakout_box\pushable_media_stream_audio_source.cc:93
    #5 0x7ff64548150c in blink::PushableMediaStreamAudioSource::Broker::StopSource(void) D:\src\third_party\blink\renderer\modules\breakout_box\pushable_media_stream_audio_source.cc:53:5
    #6 0x7ff6454846dd in blink::MediaStreamAudioTrackUnderlyingSink::Disconnect D:\src\third_party\blink\renderer\modules\breakout_box\media_stream_audio_track_underlying_sink.cc:116
    #7 0x7ff6454846dd in blink::MediaStreamAudioTrackUnderlyingSink::abort(class blink::ScriptState *, class blink::ScriptValue, class blink::ExceptionState &) D:\src\third_party\blink\renderer\modules\breakout_box\media_stream_audio_track_underlying_sink.cc:92:3
    #8 0x7ff639e3ba9f in blink::`anonymous namespace'::v8_underlying_sink_base::AbortOperationCallback D:\src\out\95.0.4638.49\gen\third_party\blink\renderer\bindings\core\v8\v8_underlying_sink_base.cc:103:23
    #9 0x7ff632f2c9d7 in v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo) D:\src\v8\src\api\api-arguments-inl.h:152:3
    #10 0x7ff632f29da4 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> D:\src\v8\src\builtins\builtins-api.cc:112:36
    #11 0x7ff632f27e42 in v8::internal::Builtins::InvokeApiFunction(class v8::internal::Isolate *, bool, class v8::internal::Handle<class v8::internal::HeapObject>, class v8::internal::Handle<class v8::internal::Object>, int, class v8::internal::Handle<class v8::internal::Object> *const, class v8::internal::Handle<class v8::internal::HeapObject>) D:\src\v8\src\builtins\builtins-api.cc:226:16
    #12 0x7ff63327090b in v8::internal::`anonymous namespace'::Invoke D:\src\v8\src\execution\execution.cc:283:20
    #13 0x7ff63326efd1 in v8::internal::Execution::Call(class v8::internal::Isolate *, class v8::internal::Handle<class v8::internal::Object>, class v8::internal::Handle<class v8::internal::Object>, int, class v8::internal::Handle<class v8::internal::Object> *const) D:\src\v8\src\execution\execution.cc:470:10
    #14 0x7ff632e245d8 in v8::Function::Call(class v8::Local<class v8::Context>, class v8::Local<class v8::Value>, int, class v8::Local<class v8::Value> *const) D:\src\v8\src\api\api.cc:5179:7
    #15 0x7ff63d4af89e in blink::PromiseCall(class blink::ScriptState *, class v8::Local<class v8::Function>, class v8::Local<class v8::Object>, int, class v8::Local<class v8::Value> *const) D:\src\third_party\blink\renderer\core\streams\miscellaneous_operations.cc:485:15
    #16 0x7ff63d4b1bee in blink::`anonymous namespace'::JavaScriptStreamAlgorithmWithoutExtraArg::Run D:\src\third_party\blink\renderer\core\streams\miscellaneous_operations.cc:139:12
    #17 0x7ff639c059d8 in blink::WritableStreamDefaultController::AbortSteps(class blink::ScriptState *, class v8::Local<class v8::Value>) D:\src\third_party\blink\renderer\core\streams\writable_stream_default_controller.cc:60:41
    #18 0x7ff639c01fd7 in blink::WritableStream::FinishErroring(class blink::ScriptState *, class blink::WritableStream *) D:\src\third_party\blink\renderer\core\streams\writable_stream.cc:574:55
    #19 0x7ff639c06e71 in blink::WritableStreamDefaultController::AdvanceQueueIfNeeded(class blink::ScriptState *, class blink::WritableStreamDefaultController *) D:\src\third_party\blink\renderer\core\streams\writable_stream_default_controller.cc:447:5
    #20 0x7ff639c09730 in blink::WritableStreamDefaultController::SetUp::ResolvePromiseFunction::CallWithLocal D:\src\third_party\blink\renderer\core\streams\writable_stream_default_controller.cc:163:7
    #21 0x7ff632f2c9d7 in v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo) D:\src\v8\src\api\api-arguments-inl.h:152:3
    #22 0x7ff632f29da4 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> D:\src\v8\src\builtins\builtins-api.cc:112:36
    #23 0x7ff632f271db in v8::internal::Builtin_Impl_HandleApiCall D:\src\v8\src\builtins\builtins-api.cc:142:5
    #24 0x7ff632f2652c in v8::internal::Builtin_HandleApiCall(int, unsigned __int64 *, class v8::internal::Isolate *) D:\src\v8\src\builtins\builtins-api.cc:130:1
    #25 0x7ec9000c113b  (<unknown module>)

Address 0x7e80003dc378 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison (D:\src\out\95.0.4638.49\content_shell.exe+0x14066244c) in v8::internal::ObjectVisitor::VisitCustomWeakPointers(class v8::internal::HeapObject, class v8::internal::CompressedObjectSlot, class v8::internal::CompressedObjectSlot)
Shadow bytes around the buggy address:
  0x1214ed1fb810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1214ed1fb820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1214ed1fb830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1214ed1fb840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1214ed1fb850: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x1214ed1fb860: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]
  0x1214ed1fb870: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1214ed1fb880: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1214ed1fb890: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1214ed1fb8a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1214ed1fb8b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==18564==ABORTING
Credit

Discovered by Marcin Towalski of Cisco Talos.

https://talosintelligence.com/vulnerability_reports/

Timeline

2021-10-26 - Vendor Disclosure 
YYYY-MM-DD - Public Release

## Attachments

- [TALOS-2021-1398 - Google_Chrome_MediaStreamTrackGenerator_use_after_free_vulnerability.txt](attachments/TALOS-2021-1398 - Google_Chrome_MediaStreamTrackGenerator_use_after_free_vulnerability.txt) (text/plain, 10.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 901 B)

## Timeline

### dt...@chromium.org (2021-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-26)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-10-27)

I was not able to reproduce, for whatever reason - it looks like it requires the right timing and the POC here might not hit it for me. Regardless...

MediaStreamTrack::MediaStreamTrack(ExecutionContext* context,
                                   MediaStreamComponent* component,
                                   MediaStreamSource::ReadyState ready_state,
                                   base::OnceClosure callback)
    : ready_state_(ready_state),
      component_(component),
      execution_context_(context) {
  component_->Source()->AddObserver(this);

My observations:

1. MediaStreamTrack observes MediaStreamSource, which holds a WeakMember<Observer> pointer to MediaStreamTrack.
2. MediaStreamTrack does not remove itself as an observer.
3. MediaStreamSource::SetReadyState() walks those weak pointers and and calls SourceChangedState.
4. The POC makes 2 MediaStreamTracks (via clone()). This means MediaStreamSource has 2 weak pointers as observers.
5.  The POC also makes a MediaStreamAudioTrackUnderlyingSink via MediaStreamTrackGenerator::writable().
6. Step 5 gives access to an abort() that will use both MediaStreamTracks by weak pointer, through Step 1.
8. The JS is holding a reference to both MediaStreamTracks

What I am missing is a step 9 where abort() actually frees the MediaStreamSource.

> The interesting part happens at line 6, where the stream gets disconnected which triggers destructor of the MediaStreamTrackGenerator object. 

Did you not get a "freed" stack trace from ASAN as well? Can you provide it? I can't locate how it would be freed.



[Monorail components: Blink>Media]

### da...@chromium.org (2021-10-27)

Maybe a media person can see something I can't here.

### vu...@sourcefire.com (2021-10-27)

The use-after-poison should always hit (maximum of 1 second delay) and we provided the ASAN stack trace for it, it works on both Windows and Linux, using the flags —no-sandbox —js-flags=—expose-gc

### vu...@sourcefire.com (2021-10-27)

reward_to-marcin.towalski_at_gmail.com


### [Deleted User] (2021-10-27)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-10-27)

> we provided the ASAN stack trace for it

ASAN generally gives 3 stack traces:

1) The crash (use after free)
2) The allocation
3) The free (which occurred before 1).

I am asking if you have the 3rd stack trace. For my I tried the POC for quite a while and was not able to reproduce.

If you don't have the freed-stack-trace, can you provide more detail on how the MediaStreamTrackGenerator is freed? Thank you!

### da...@chromium.org (2021-10-27)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Media Blink>MediaStream]

### vu...@sourcefire.com (2021-10-27)

From what we can tell gc() forces the garbage collector to run so it is run twice on the same object.

Because it's not a regular malloc/free that's happening, ASAN isn't detecting it as a UAF, but it's detecting that freed memory is being used that's why it doesn't provide the location that memory is being freed.

See https://github.com/google/sanitizers/issues/191 for more info

### ht...@chromium.org (2021-10-27)

toprice@ and benjaminwagner@ are OOO at the moment, which means we're seriously understaffed on the Breakout Box front.
Asking if eladalon@ can take a look.


### da...@chromium.org (2021-10-27)

> From what we can tell gc() forces the garbage collector to run so it is run twice on the same object.

gc() would run the GC, this helps to win race conditions where a reference is released but the GC has not freed it yet (and poisoned the memory). So it helps to make things reliable for ASAN to see. Though it did not work for me.

### da...@chromium.org (2021-10-27)

Thanks hta@. I will assign so that we ensure this has an owner who can look.

### ml...@chromium.org (2021-10-27)

Oilpan as a Mark/Sweep GC that first marks a heap and then reclaims objects. Between marking and sweeping, objects are poisoned. WeakMember are synchronously cleared after marking.

I have not run the repro yet.

IIUC then MediaStreamSource is actually poisoned. Since WebPlatformMediaStreamSource::owner_ is a weak ptr it should have been cleared already at this point.

### ml...@chromium.org (2021-10-27)

Sorry, I didn't see the observer parts. The issue is here:

void MediaStreamSource::SetReadyState(ReadyState ready_state) {
  SendLogMessage(String::Format("SetReadyState({id=%s}, {ready_state=%s})",
                                Id().Utf8().c_str(),
                                ReadyStateToString(ready_state))
                     .Utf8());
  if (ready_state_ != kReadyStateEnded && ready_state_ != ready_state) {
    ready_state_ = ready_state;

    // Observers may dispatch events which create and add new Observers;
    // take a snapshot so as to safely iterate.
    Vector<base::OnceClosure> observer_callbacks;
    for (auto it = observers_.begin(); it != observers_.end(); ++it) {
      observer_callbacks.push_back(
          base::BindOnce(&Observer::SourceChangedState, *it)); <====== This is not binding the oberver strongly.
    }
    for (auto& observer_callback : observer_callbacks) {
      std::move(observer_callback).Run(); <===== callbacks themselves may allocate and invoke GC which may reclaim the weak observers.
    }
  }
}

tl;dr: The receiver was not properly bound strongly until the callbacks were executed. This is a problem if callbacks themselves are generic and thus allocate and invoke GC.

Quickfix is here: https://chromium-review.googlesource.com/c/chromium/src/+/3247159

I thought that Blink mandates the use of WTF::Bind() to be used instead of base::BindOnce.


### da...@chromium.org (2021-10-27)

For my learning: Why does the callback need a Persistent<T> and not a WeakPersistent<T>?

> I thought that Blink mandates the use of WTF::Bind() to be used instead of base::BindOnce.

It does. This slips in, among other uses of base things like WeakPtr, and cause bugs.

### ml...@chromium.org (2021-10-27)

> For my learning: Why does the callback need a Persistent<T> and not a WeakPersistent<T>?

Persistent will make sure the callback gets fired.

WeakPersistent should in theory allow that the callback gets cancelled if the observer gets executed until then. I think this is controlled somewhere through Unwrap traits. (I fail to find the codesearch place now).

Not sure what the intended semantics here is, maybe media folks can clarify.

### ml...@chromium.org (2021-10-27)

s/gets executed/gets reclaimed/ :) 

### da...@chromium.org (2021-10-27)

I see.

I read this line and I thought it's binding a WeakPersistent already so it would get cancelled. But I guess base won't know about such things.. That leaves me unclear how it compiles at all. Perhaps WeakPersistent<T> can be implicitly converted to T*... Yep :( https://source.chromium.org/chromium/chromium/src/+/main:v8/include/cppgc/persistent.h;drc=5539ecff898c79b0771340051d62bf81649e448d;l=184

That seems awfully dangerous.

### ml...@chromium.org (2021-10-27)

IIUC, then IsWeakReceiver<> [1] should handle the cancellation in base bind. The trait override for WeakPersistent is here [2].

[1] https://source.chromium.org/chromium/chromium/src/+/main:base/bind_internal.h;l=1332;drc=5539ecff898c79b0771340051d62bf81649e448d;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/persistent.h;drc=5539ecff898c79b0771340051d62bf81649e448d;bpv=1;bpt=1;l=203

### da...@chromium.org (2021-10-27)

Then just adding the header would make this work correctly? That's perhaps an even worse situation.

### ml...@chromium.org (2021-10-27)

No, because we were not having WeakPersistent in first place but the original `*it` just returned a raw pointer from a WeakMember<> (or maybe resulted in a WeakMember<>&, not exactly sure). If we had a WeakPersistent<>, the binding should have worked.


### da...@chromium.org (2021-10-27)

Ah, so iterating a set of WeakMember<T> gives you T* entries, not WeakMember<T>, or WeakPersistent<T>..?

I don't see that in the traits. I think a WeakMember<T> should give a const WeakMember<T>&: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/hash_traits.h;drc=5539ecff898c79b0771340051d62bf81649e448d;l=134

But WeakMember<T> also converts to T* implicitly: https://source.chromium.org/chromium/chromium/src/+/main:v8/include/cppgc/member.h;drc=5539ecff898c79b0771340051d62bf81649e448d;l=179

### gi...@appspot.gserviceaccount.com (2021-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d1055cb23b15e42381bc815eeabb207ce18394d9

commit d1055cb23b15e42381bc815eeabb207ce18394d9
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Thu Oct 28 12:31:03 2021

MediaStreamSource: Retain observers till callbacks have been executed

Bug: chromium:1263620
Change-Id: I0655474bd3c5f4f927db1834e95b2724a20ba4e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247159
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#935842}

[modify] https://crrev.com/d1055cb23b15e42381bc815eeabb207ce18394d9/third_party/blink/renderer/platform/mediastream/media_stream_source.cc


### el...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-28)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-10-28)

mlippautz@, assigned back to you because you authored the fix, but you're welcome to assign back to me know if you don't have the bandwidth to handle cherry-picks.

### el...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-28)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-10-28)

Hi eladalon, mlippautz won't be able to get the merges in as quickly as you would and had asked me last night before signing off to ask you to look after it. Would you mind helping out with that?

### el...@chromium.org (2021-10-28)

As mentioned on https://crbug.com/chromium/1263620#c28, no worries about reassigning to me.

### ml...@chromium.org (2021-10-28)

Just saw this now, thanks for taking over the merges.

### el...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

Merge review required: M96 is already shipping to beta.

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

### [Deleted User] (2021-10-29)

Merge review required: M95 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-29)

Merge review required: M94 is already shipping to stable.

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

### el...@chromium.org (2021-10-29)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-10-29)

1. Why does your merge fit within the merge criteria for these milestones?

Security fix for a UAF issue

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3247159

3. Have the changes been released and tested on canary?

Yes, the change has been released on Canary 97.0.4685.0 without causing any more issues.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

n/a

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No manual testing required. Patch was tested against the POC in https://crbug.com/chromium/1263620#c0 on main branch and is well understood. Optionally, the POC in https://crbug.com/chromium/1263620#c0 can be tested against a stable build but that would require an ASAN-configured build.



### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-29)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-02)

Merge approved for M96 and M95, please merge to branches 4664 and 4638 respectively. 
Please also backmerge to M94, branch 4606. Thank you! 

### sr...@google.com (2021-11-02)

Please complete the merges to M96 branch today before 2pm PST so these changes can go out in beta release tomorrow and get beta verification and baking before stable promotion.

### el...@chromium.org (2021-11-02)

m94: crrev.com/c/3257269
m95: crrev.com/c/3257492
m96: crrev.com/c/3257647

### gi...@appspot.gserviceaccount.com (2021-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/109fde1088bef0ad849f0c5dc74d905ff739a05e

commit 109fde1088bef0ad849f0c5dc74d905ff739a05e
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Tue Nov 02 21:21:27 2021

MediaStreamSource: Retain observers till callbacks have been executed

(cherry picked from commit d1055cb23b15e42381bc815eeabb207ce18394d9)

Bug: chromium:1263620
Change-Id: I0655474bd3c5f4f927db1834e95b2724a20ba4e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247159
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#935842}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3257492
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#1004}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/109fde1088bef0ad849f0c5dc74d905ff739a05e/third_party/blink/renderer/platform/mediastream/media_stream_source.cc


### gi...@appspot.gserviceaccount.com (2021-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/562a2931f4f6a7de6655d369b64139820b850283

commit 562a2931f4f6a7de6655d369b64139820b850283
Author: Michael Lippautz <mlippautz@chromium.org>
Date: Wed Nov 03 12:42:52 2021

MediaStreamSource: Retain observers till callbacks have been executed

(cherry picked from commit d1055cb23b15e42381bc815eeabb207ce18394d9)

Bug: chromium:1263620
Change-Id: I0655474bd3c5f4f927db1834e95b2724a20ba4e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247159
Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#935842}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3257647
Auto-Submit: Elad Alon <eladalon@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#694}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/562a2931f4f6a7de6655d369b64139820b850283/third_party/blink/renderer/platform/mediastream/media_stream_source.cc


### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Congratulations, Marcin! The VRP Panel has decided to award you $7500 for this report. Excellent work and thank you for reporting this issue to us! 

### am...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2022-02-01)

Will restrictions be removed for public disclosure this week?

### am...@chromium.org (2022-02-01)

Yes, this should be automatically made allpublic by the bot on Thursday, 3 February based on the 28 October fix date.

### [Deleted User] (2022-02-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1263620?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057716)*
