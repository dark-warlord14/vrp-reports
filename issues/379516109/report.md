# AddressSanitizer:heap-use-after-free on  LanguageDetectionModel::NotifyModelLoaded


| Field | Value |
|-------|-------|
| **Issue ID** | [379516109](https://issues.chromium.org/issues/379516109) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Language>Translate |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 130.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | fe...@chromium.org |
| **Created** | 2024-11-18 |
| **Bounty** | $50,000.00 |

## Description

# Steps to reproduce the problem

repro:

0. launch chrome with --enable-features=LanguageDetectionAPI
1. apply patch.diff which simplify trigger
2. run poc.html.

# Problem Description

0. In the function `LanguageDetectionModel:: NotifyModelLoaded`, there is an iterator operation. When AILanguageDetector performs detection, the callback `OnDetectComplete` will be added to the `model_loaded_callbacks_`, and the OnDetectComplete function body will have a user-defined callback `resolve ->Resolve`. The following is the reverse reference of the chain.

```
void LanguageDetectionModel::NotifyModelLoaded() {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  for (auto&& callback_ : model_loaded_callbacks_) {
    std::move(callback_).Run(*this);
  }
  loaded_ = true;
  model_loaded_callbacks_.clear();
}
------------------------
void LanguageDetectionModel::AddOnModelLoadedCallback(
    ModelLoadedCallback callback) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  if (loaded_ || model_loaded_callbacks_.size() >= kMaxPendingCallbacksCount) {
    std::move(callback).Run(*this);
  } else {
    model_loaded_callbacks_.emplace_back(std::move(callback));
  }
}
------------------------
void DetectLanguage(const WTF::String& text,
                    DetectLanguageCallback on_complete) {
  auto& model = language_detection::GetLanguageDetectionModel();
  model.AddOnModelLoadedCallback(
      WTF::BindOnce(DetectLanguageWithModel, text, std::move(on_complete)));
}
------------------------
ScriptPromise<IDLSequence<LanguageDetectionResult>> AILanguageDetector::detect(
    ScriptState* script_state,
    const WTF::String& input,
    AILanguageDetectorDetectOptions* options,
    ExceptionState& exception_state) {
[...]

  DetectLanguage(input, WTF::BindOnce(AILanguageDetector::OnDetectComplete,
                                      WrapPersistent(resolver)));
  return resolver->Promise();
}
-----------------------
void AILanguageDetector::OnDetectComplete(
    ScriptPromiseResolver<IDLSequence<LanguageDetectionResult>>* resolver,
    base::expected<WTF::Vector<LanguagePrediction>, DetectLanguageError>
        result) {
  if (result.has_value()) {
    // Order the result from most to least confident.
    std::sort(result.value().rbegin(), result.value().rend());
    resolver->Resolve(ConvertResult(result.value()));
  } else {
    switch (result.error()) {
      case DetectLanguageError::kUnavailable:
        resolver->Reject("Model not available");
    }
  }
}

```

1. `LanguageDetectionModel:: NotifyModelLoaded` is called in `LanguageDetectionAgent:: updateLanguageDetectionModel`, which can be traced back to `LanguageDetectionAgent:: WasShown`. However, in this`WasShown`, Mojo calls are made to communicate with the browser through`VNet anguageDetectionHandler () ->VNet anguageDetectionModel `` The final`callback`returns the`renderer`for calling, which represents an asynchronous process in the middle of the`renderer`execution. This means that we can construct a POC. Before running the`LanguageDetectionAgent:: Updating LanguageDetectionModel`, we will fill the corresponding quantity and contain user-defined iterator invalidation code in the` model\_loaded\_callback`. Ultimately, it will lead to the failure of iterators. Causing UAF.

```
void LanguageDetectionAgent::WasShown() {
  // Check if the the render frame was initially hidden and
  // the model request was delayed until the frame was in
  // the foreground.
[...]
  GetLanguageDetectionHandler()->GetLanguageDetectionModel(
      base::BindOnce(&LanguageDetectionAgent::UpdateLanguageDetectionModel,
                     weak_pointer_factory_.GetWeakPtr()));
}

```

0. <https://source.chromium.org/chromium/chromium/src/+/main:components/language_detection/core/language_detection_model.cc;l=230?q=LanguageDetectionModel::NotifyModelLoaded&ss=chromium%2Fchromium%2Fsrc>
1. <https://source.chromium.org/chromium/chromium/src/+/main:components/language_detection/content/renderer/language_detection_agent.cc;l=107?q=LanguageDetectionAgent::WasShown&ss=chromium%2Fchromium%2Fsrc>

bitset:
<https://source.chromium.org/chromium/chromium/src/+/6742751ccf591d9ba1670c3082efbf345084b7d0>

why need patch?
simplify trigger progress. No impact on the vulnerability principle.

fix sugesstions:
swap the model\_loaded\_callbacks\_. see fix.diff

# Summary

AddressSanitizer:heap-use-after-free on LanguageDetectionModel::NotifyModelLoaded

# Custom Questions

#### Type of crash:

tab

#### Crash state:

see asan.log

#### Reporter credit:

lime(@limeSec)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 38.2 KB)
- [fix.diff](attachments/fix.diff) (text/x-diff, 869 B)
- [poc.html](attachments/poc.html) (text/html, 673 B)
- [uaf15.patch](attachments/uaf15.patch) (text/x-diff, 2.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 90.8 KB)
- [demonstration.mov](attachments/demonstration.mov) (video/quicktime, 17.0 MB)
- [exploit_demonstration.md](attachments/exploit_demonstration.md) (text/markdown, 14.8 KB)
- [stable_poc.html](attachments/stable_poc.html) (text/html, 1.3 KB)

## Timeline

### aj...@google.com (2024-11-18)

Hello - the crash here is in the renderer but your patch modifies both the renderer and the browser.

Could you outline in more detail how the patch reproduces a situation that can occur without already having RCE in the renderer?

### li...@gmail.com (2024-11-18)

0. Let's take a look at this line of code. Here, the `GetLanguageDetectionModel` is a Mojo call that calls the browser side `GetLanguageDetectionModel` function through the renderer. This action will eventually call `LanguageDetectionAgent:: updateLanguageDetectionModel` as the wrapper for the callback on the browser side, and then call it in the renderer process. However, this process is designed to be asynchronous. Yes, that's right, it's asynchronous between the renderer and the browser, because before calling the callback on the browser side, we can add `model_loaded_callbacks_` on the renderer side at the same time, and finally just wait for `LanguageDetectionAgent:: updateLanguageDetectionModel` to be called on the renderer side.

```
void LanguageDetectionAgent::WasShown() {
  // Check if the the render frame was initially hidden and
  // the model request was delayed until the frame was in
  // the foreground.
[...]
  GetLanguageDetectionHandler()->GetLanguageDetectionModel(
      base::BindOnce(&LanguageDetectionAgent::UpdateLanguageDetectionModel,
                     weak_pointer_factory_.GetWeakPtr()));
}

```
```
void LanguageDetectionModel::AddOnModelLoadedCallback(
    ModelLoadedCallback callback) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
  if (loaded_ || model_loaded_callbacks_.size() >= kMaxPendingCallbacksCount) {
    std::move(callback).Run(*this);
  } else {
    model_loaded_callbacks_.emplace_back(std::move(callback));
  }
}

```

1. Here is an explanation of my patch
   The first one in `LanguageDetectionModelService::LanguageDetectionModelFile` is mainly to make this callback callback call back earlier for the convenience of my concept proof. Secondly, the patches in these two places actually represent a purpose, mainly to
   The return value of this `GetLanguageDetectionModelFile` is reasonable Although patches were applied in two places, their purpose is to accomplish the same situation, which is to make this callback reasonable. I believe that in normal logic, this return value is definitely reasonable.

```
diff --git a/components/language_detection/core/browser/language_detection_model_service.cc b/components/language_detection/core/browser/language_detection_model_service.cc
index 388ebdaf1d..b67a5c76ef 100644
--- a/components/language_detection/core/browser/language_detection_model_service.cc
+++ b/components/language_detection/core/browser/language_detection_model_service.cc
@@ -129,10 +129,11 @@ void LanguageDetectionModelService::GetLanguageDetectionModelFile(
     PostGetModelCallback(std::move(callback),
                          language_detection_model_file_.GetFile().Duplicate());
     return;
-  } else if (pending_model_requests_.size() < kMaxPendingRequestsAllowed) {
-    pending_model_requests_.emplace_back(std::move(callback));
-    return;
-  }
+  } 
+  // else if (pending_model_requests_.size() < 1) {
+  //   pending_model_requests_.emplace_back(std::move(callback));
+  //   return;
+  // }
 
   PostGetModelCallback(std::move(callback), base::File());
 }
diff --git a/third_party/blink/renderer/modules/ai/on_device_translation/ai_language_detector.cc b/third_party/blink/renderer/modules/ai/on_device_translation/ai_language_detector.cc
index 76b99d7dc9..f59dd09c8b 100644
--- a/third_party/blink/renderer/modules/ai/on_device_translation/ai_language_detector.cc
+++ b/third_party/blink/renderer/modules/ai/on_device_translation/ai_language_detector.cc
@@ -51,10 +51,14 @@ void AILanguageDetector::OnDetectComplete(
     ScriptPromiseResolver<IDLSequence<LanguageDetectionResult>>* resolver,
     base::expected<WTF::Vector<LanguagePrediction>, DetectLanguageError>
         result) {
-  if (result.has_value()) {
+  if (!result.has_value()) {
     // Order the result from most to least confident.
-    std::sort(result.value().rbegin(), result.value().rend());
-    resolver->Resolve(ConvertResult(result.value()));
+    // std::sort(result.value().rbegin(), result.value().rend());
+
+    auto* one = MakeGarbageCollected<LanguageDetectionResult>();
+    HeapVector<Member<LanguageDetectionResult>> result;
+    result.push_back(one);
+    resolver->Resolve(result);
   } else {
     switch (result.error()) {
       case DetectLanguageError::kUnavailable:

```

This is an RCE vulnerability because it directly uses `std::vector` instead of `HeapVector`, so its memory exists in traditional memory, combined with user-defined callbacks, which is clearly an RCE vulnerability.

If you have any questions, feel free to ask me. thanks.

### pe...@google.com (2024-11-18)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2024-11-19)

The change in the browser code can only be triggered if > 100 model requests are in flight at once.

However, the renderer change:

```
-  if (result.has_value()) {
+  if (!result.has_value()) {
     // Order the result from most to least confident.
-    std::sort(result.value().rbegin(), result.value().rend());
-    resolver->Resolve(ConvertResult(result.value()));
+    // std::sort(result.value().rbegin(), result.value().rend());
+
+    auto* one = MakeGarbageCollected<LanguageDetectionResult>();
+    HeapVector<Member<LanguageDetectionResult>> result;
+    result.push_back(one);
+    resolver->Resolve(result);

```

With `base::expected<WTF::Vector<LanguagePrediction>, DetectLanguageError> result` doesn't make sense as if `result` has no value the renderer normally calls resolver->Reject(). The patch here seems to send an invalid result into resolver?

How can the browser be coerced to achieve this situation without your patch?

### li...@gmail.com (2024-11-19)

Hello, I think you may have misunderstood what I meant. The purpose of my patch is to simplify the triggering steps. According to the normal logic of the code, it should enter `pending_model_requests_.emplace_back(std::move(callback));` and then under this premise, the callback call will be triggered later, rather than just in the case of my patch, that is, `PostGetModelCallback(std::move(callback), base::File());`.

So under normal circumstances, it will get a correct result and call `resolver->Resolve` instead of reject, so I just simulate a normal return situation, so no matter when it calls this callback, as long as the browser runs the callback, the response of this callback is asynchronous for the renderer process, and I think the update of this model is more troublesome, so I directly patch it to let this callback run in advance, thereby proving the existence of this vulnerability.

If you have any questions, feel free to pin me.

### aj...@google.com (2024-11-19)

A better proof is that if I run `poc.html` in a release build it hits a crash dereferencing a callback - the patch provided above is not necessary!

```
run-chrome-release --enable-features=LanguageDetectionAPI poc.html
.childdbg 1
sxn ibp
sxn epr
g
...
6:098> r
rax=bf1d9effffffffff rbx=00007ffdf18885b7 rcx=bf1d9effffffffff
rdx=000047bc005fa340 rsi=00007ffdf370f2d8 rdi=000047bc0059f950
rip=00007ffdee87abfb rsp=0000000df87fdc90 rbp=000047bc0059f948
 r8=000047bc00110880  r9=00007ffde7537460 r10=00000fffbcea6e8c
r11=0000040004001000 r12=00007ffdf18885bb r13=0000000df87fdcd8
r14=00007ffdf1888596 r15=0000000df87fdcb8
iopl=0         nv up ei ng nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010286
chrome!base::internal::BindStateHolder::polymorphic_invoke+0x5 [inlined in chrome!language_detection::LanguageDetectionModel::NotifyModelLoaded+0x7b]:
00007ffd`ee87abfb 488b4108        mov     rax,qword ptr [rcx+8] ds:bf1d9f00`00000007=????????????????

6:098> k
 # Child-SP          RetAddr               Call Site
00 (Inline Function) --------`--------     chrome!base::internal::BindStateHolder::polymorphic_invoke+0x5 [D:\chromium\src\base\functional\callback_internal.h @ 154] 
01 (Inline Function) --------`--------     chrome!base::OnceCallback<void (language_detection::LanguageDetectionModel &)>::Run+0x1b [D:\chromium\src\base\functional\callback.h @ 154] 
02 0000000d`f87fdc90 00007ffd`ee87a200     chrome!language_detection::LanguageDetectionModel::NotifyModelLoaded+0x7b [D:\chromium\src\components\language_detection\core\language_detection_model.cc @ 233] 
03 0000000d`f87fdd30 00007ffd`ee87b120     chrome!language_detection::LanguageDetectionModel::SetModel+0x40 [D:\chromium\src\components\language_detection\core\language_detection_model.cc @ 218] 
04 (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (language_detection::LanguageDetectionModel::*)(std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >),base::WeakPtr<language_detection::LanguageDetectionModel> &&>::Invoke+0x41 [D:\chromium\src\base\functional\bind_internal.h @ 738] 
05 (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (language_detection::LanguageDetectionModel::*&&)(std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >),base::WeakPtr<language_detection::LanguageDetectionModel> &&>,void,0>::MakeItSo+0x5c [D:\chromium\src\base\functional\bind_internal.h @ 954] 
06 (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (language_detection::LanguageDetectionModel::*&&)(std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >),base::WeakPtr<language_detection::LanguageDetectionModel> &&>,base::internal::BindState<1,1,0,void (language_detection::LanguageDetectionModel::*)(std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >),base::WeakPtr<language_detection::LanguageDetectionModel> >,void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>::RunImpl+0x5c [D:\chromium\src\base\functional\bind_internal.h @ 1067] 
07 0000000d`f87fdd70 00007ffd`ee87b428     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (language_detection::LanguageDetectionModel::*&&)(std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >),base::WeakPtr<language_detection::LanguageDetectionModel> &&>,base::internal::BindState<1,1,0,void (language_detection::LanguageDetectionModel::*)(std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >),base::WeakPtr<language_detection::LanguageDetectionModel> >,void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>::RunOnce+0x80 [D:\chromium\src\base\functional\bind_internal.h @ 980] 
08 0000000d`f87fddf0 00007ffd`ee87b2e5     chrome!base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>::Run+0x58 [D:\chromium\src\base\functional\callback.h @ 156] 
09 0000000d`f87fde70 00007ffd`ee87b274     chrome!<lambda_1>::operator()+0x55 [D:\chromium\src\base\functional\callback_internal.h @ 207] 
0a (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<`lambda at ..\..\base\functional\callback_internal.h:202:12',base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)> &&,base::OnceCallback<void ()> &&>::Invoke+0x61 [D:\chromium\src\base\functional\bind_internal.h @ 656] 
0b (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,base::internal::FunctorTraits<`lambda at ..\..\base\functional\callback_internal.h:202:12' &&,base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)> &&,base::OnceCallback<void ()> &&>,void,0,1>::MakeItSo+0x61 [D:\chromium\src\base\functional\bind_internal.h @ 930] 
0c (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<`lambda at ..\..\base\functional\callback_internal.h:202:12' &&,base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)> &&,base::OnceCallback<void ()> &&>,base::internal::BindState<0,0,0,`lambda at ..\..\base\functional\callback_internal.h:202:12',base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>,base::OnceCallback<void ()> >,void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>::RunImpl+0x61 [D:\chromium\src\base\functional\bind_internal.h @ 1067] 
0d 0000000d`f87fdf00 00007ffd`ee87b428     chrome!base::internal::Invoker<base::internal::FunctorTraits<`lambda at ..\..\base\functional\callback_internal.h:202:12' &&,base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)> &&,base::OnceCallback<void ()> &&>,base::internal::BindState<0,0,0,`lambda at ..\..\base\functional\callback_internal.h:202:12',base::OnceCallback<void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>,base::OnceCallback<void ()> >,void (std::__Cr::optional<std::__Cr::unique_ptr<tflite::task::text::nlclassifier::NLClassifier,std::__Cr::default_delete<tflite::task::text::nlclassifier::NLClassifier> > >)>::RunOnce+0x74 [D:\chromium\src\base\functional\bind_internal.h @ 980]

```

In an ASAN build:-

```
==32264==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffdd3096f26 in language_detection::LanguageDetectionModel::UpdateWithFileAsync(class base::File, class base::OnceCallback<(void)>) D:\chromium\src\components\language_detection\core\language_detection_model.cc:192:7
    #1 0x7ffdd3096f26 in language_detection::LanguageDetectionModel::UpdateWithFileAsync(class base::File, class base::OnceCallback<(void)>) D:\chromium\src\components\language_detection\core\language_detection_model.cc:192:7
    #2 0x7ffdc1c7d3ce in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `"d:\chromium\src\out\Asan\chrome.exe" --type=renderer --string-annotations --user-data-dir="d:\temp\asan-profile" --enable-dinosaur-easter-egg-alt-images --no-pre-read-main-dll --no-sandbox --enable-blink-features=MojoJS --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1731700301914503 --launch-time-ticks=355192278816 --metrics-shmem-handle=3336,i,6395715662685379638,9907109661051326816,2097152 --field-trial-handle=3324,i,8562003059834976515,3524362264920471876,262144 --enable-features=LanguageDetectionAPI --variations-seed-version --enable-logging=handle --log-file=3332 --v=1 --mojo-platform-channel-handle=3304 /prefetch:1`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==32264==END OF ADDITIONAL INFO
==32264==ABORTING

```

### aj...@google.com (2024-11-19)

Sev=High (unprotected RCE in renderer).

-> people on CL <https://chromium-review.googlesource.com/c/chromium/src/+/5856234>

### aj...@google.com (2024-11-19)

FoundIn from commit 6742751ccf591d9ba1670c3082efbf345084b7d0

Looks like this is on all OSes but would appreciate it if the team could update OS labels otherwise.

### li...@gmail.com (2024-11-20)

Good job! In the debug version, there are Google API and some model updates that do not automatically start, so I directly patch the code to trigger it. However, I'm glad you could trigger it directly.

### pe...@google.com (2024-11-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### li...@gmail.com (2024-11-25)

I have completed the process of calling any address, which is `RIP control`. In the next few days, I will update my write up to this issue interface, but I also hope to fix it as soon as possible. :)

### am...@chromium.org (2024-11-28)

Since this requires the --enable-features=LanguageDetectionAPI command line flag, which is not enabled by default, it seems SI-None is appropriate here.

### li...@gmail.com (2024-11-28)

Here is an exploitable demonstration.

### li...@gmail.com (2024-11-28)

Because the `stable` version has regular pulls of `Google API` and `Optimization Model`, there is no need for any `patches`. So I think the `patchs` I gave can prove the existence of vulnerabilities on the dev version without any problem. Because `callback` will eventually return, regardless of when, whether it is early or delayed. The vulnerability is essentially caused by adding a `resolver` in JavaScript, which is normally processed by the browser before returning. Therefore, at this point, our `vector` is completely under our control, so we can process it directly after returning it without any conditional competition. Because when we use the `detect` function to build vulnerability models, the target is already under our control. and the fix only needs to be done on the iterator side. :)

For stable version:

repro step:

1. `./Google\ Chrome --enable-features=LanguageDetectionAPI --js-flags="--expose-gc" http://localhost:8000/stable_poc.html`
2. `cd ~/Library/Application Support/Google/Chrome/Crashpad/completed`
3. `minidump_stackwalk ed20f4cb-0eb0-4fd2-a744-c48770f3d360.dmp|head -n 10`

then you can get crash state in stable version.

```
[...]
Operating system: Mac OS X
                  15.1.0 24B83
CPU: arm64
     11 CPUs

GPU: UNKNOWN

Crash reason:  EXC_BAD_ACCESS / 0x00000101
Crash address: 0x6161616161616161
Crash parameters:

```

### fe...@chromium.org (2024-11-29)

I've sent <https://crrev.com/c/6054828> for review to fix this.

Unfortunately language detection is in origin trial, so this potentially has real world impact.

@ajgo once that CL has landed, I will CP it into any pending releases.

Rather than CPing it back into earlier releases, it's probably best to just hit the kill-switch on the feature. There's a finch freeze right now and it's thanksgiving, so that's going to be hard.

### aj...@google.com (2024-11-29)

I haven't validated the provided r/w poc in comment 16 but it makes sense to treat this as potentially exploitable.

I'm not sure how the killswitch can skip the freeze - you will need to get in touch with a release manager perhaps to figure that out.

Either way, once the CL lands mark this as Fixed and the robots will help you manage the merges.

### ap...@google.com (2024-11-29)

Project: chromium/src  

Branch: main  

Author: Fergal Daly <[fergal@chromium.org](mailto:fergal@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6054828>

Fix callbacks in LanguageDetectionModel::NotifyModelLoaded.

---


Expand for full commit details
```
Fix callbacks in LanguageDetectionModel::NotifyModelLoaded. 
 
Bug: 379516109 
Change-Id: Idb9a853f71478fe3da8676df486076e5f87fd9f2 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6054828 
Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
Commit-Queue: Fergal Daly <fergal@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1389623}

```

---

Files:

- M `components/language_detection/core/language_detection_model.cc`

---

Hash: 9c299bcdb77c63cc75c29c009ed035c6c223067e  

Date:  Fri Nov 29 05:01:07 2024


---

### ap...@google.com (2024-11-29)

Project: chromium/src  

Branch: main  

Author: Fergal Daly <[fergal@chromium.org](mailto:fergal@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6056711>

Disable LanguageDetectionAPI.

---


Expand for full commit details
```
Disable LanguageDetectionAPI. 
 
We intend to disable it for users via the kill switch. Disabling it in 
the test config is a prerequisite for doing that. 
 
Following http://go/finch-killswitch 
 
Bug: 379516109 
Change-Id: I64c6bb31ccc671d64adcbcd269aca9c6f0c23332 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6056711 
Auto-Submit: Fergal Daly <fergal@chromium.org> 
Commit-Queue: Tsuyoshi Horo <horo@chromium.org> 
Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1389647}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`
- M `third_party/blink/web_tests/TestExpectations`
- M `third_party/blink/web_tests/http/tests/serviceworker/webexposed/global-interface-listing-service-worker-expected.txt`
- M `third_party/blink/web_tests/webexposed/global-interface-listing-dedicated-worker-expected.txt`
- M `third_party/blink/web_tests/webexposed/global-interface-listing-expected.txt`
- M `third_party/blink/web_tests/webexposed/global-interface-listing-shared-worker-expected.txt`

---

Hash: 3725ff38e13b18721aee8c33a77914855eeab8a1  

Date:  Fri Nov 29 06:45:56 2024


---

### fe...@chromium.org (2024-12-02)

Added merge requests. It would be great if we could merge this to 131 in case a respin is pushed.

### pe...@google.com (2024-12-02)

Merge review required: M132 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-12-02)

Merge review required: M131 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-12-03)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2024-12-03)

Language Detection API appears to be in OT from 130-135; updated Security-Impact to Extended Stable to reflect that.
Added review tag for merge review for M130 as well since it should be merged back to M130 Extended Stable in addition to 131 Stable.

### am...@chromium.org (2024-12-03)

Since this fix was landed on 28 November, going ahead and reviewing it now. No issues related to this fix on Canary in that time.
<https://crrev.com/c/6054828> approved for merges; please merge to M132 Beta / branch 6834 ASAP so this fix can be included in tomorrow's Beta release.

Please merge to M131 Stable / branch 6778 and M130 Extended Stable / branch 6723 by EOD Thursday, 5 December so this fix can be included in next week's Stable update.

### ap...@google.com (2024-12-04)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Fergal Daly <[fergal@chromium.org](mailto:fergal@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6068829>

Fix callbacks in LanguageDetectionModel::NotifyModelLoaded.

---


Expand for full commit details
```
Fix callbacks in LanguageDetectionModel::NotifyModelLoaded. 
 
(cherry picked from commit 9c299bcdb77c63cc75c29c009ed035c6c223067e) 
 
Bug: 379516109 
Change-Id: Idb9a853f71478fe3da8676df486076e5f87fd9f2 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6054828 
Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
Commit-Queue: Fergal Daly <fergal@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1389623} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6068829 
Auto-Submit: Fergal Daly <fergal@chromium.org> 
Commit-Queue: Alexander Bolodurin <alexbn@chromium.org> 
Reviewed-by: Alexander Bolodurin <alexbn@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6834@{#1539} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `components/language_detection/core/language_detection_model.cc`

---

Hash: 11e2ea366050aa710c98bbcacb40fed355992580  

Date:  Wed Dec 04 05:14:13 2024


---

### ap...@google.com (2024-12-05)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Fergal Daly <[fergal@chromium.org](mailto:fergal@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6068832>

Fix callbacks in LanguageDetectionModel::NotifyModelLoaded.

---


Expand for full commit details
```
Fix callbacks in LanguageDetectionModel::NotifyModelLoaded. 
 
(cherry picked from commit 9c299bcdb77c63cc75c29c009ed035c6c223067e) 
 
Bug: 379516109 
Change-Id: Idb9a853f71478fe3da8676df486076e5f87fd9f2 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6054828 
Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
Commit-Queue: Fergal Daly <fergal@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1389623} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6068832 
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com> 
Auto-Submit: Fergal Daly <fergal@chromium.org> 
Reviewed-by: Alexander Bolodurin <alexbn@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6723@{#2690} 
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `components/language_detection/core/language_detection_model.cc`

---

Hash: 881d0229c5a13b9d4ab53c9d31f87e20aaf0989b  

Date:  Thu Dec 05 17:31:19 2024


---

### ap...@google.com (2024-12-05)

Project: chromium/src  

Branch: refs/branch-heads/6778  

Author: Fergal Daly <[fergal@chromium.org](mailto:fergal@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6069027>

Fix callbacks in LanguageDetectionModel::NotifyModelLoaded.

---


Expand for full commit details
```
Fix callbacks in LanguageDetectionModel::NotifyModelLoaded. 
 
(cherry picked from commit 9c299bcdb77c63cc75c29c009ed035c6c223067e) 
 
Bug: 379516109 
Change-Id: Idb9a853f71478fe3da8676df486076e5f87fd9f2 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6054828 
Reviewed-by: Tsuyoshi Horo <horo@chromium.org> 
Commit-Queue: Fergal Daly <fergal@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1389623} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6069027 
Reviewed-by: Alexander Bolodurin <alexbn@chromium.org> 
Auto-Submit: Fergal Daly <fergal@chromium.org> 
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com> 
Cr-Commit-Position: refs/branch-heads/6778@{#2574} 
Cr-Branched-From: b21671ca172dcfd1566d41a770b2808e7fa7cd88-refs/heads/main@{#1368529}

```

---

Files:

- M `components/language_detection/core/language_detection_model.cc`

---

Hash: 35f3a2eedf1c6d92144c292842951308f5d2ee1c  

Date:  Thu Dec 05 19:29:20 2024


---

### pe...@google.com (2024-12-09)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2024-12-10)

Labeling as LTS-NotApplicable-126 because the suspected CL[1] was not merged to M126 according to the description. 

[1] https://chromium-review.googlesource.com/c/chromium/src/+/5856234

### li...@gmail.com (2024-12-11)

Hello, I saw the credit in the chromereleases, so I want to update the credit to `lime(@limeSec)`, not `lime(@limeSec_) from TIANGONG Team of Legendsec at QI-ANXIN Group`. I will always use `lime(@limeSec)` in the future, thanks:)

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
high quality report demonstrating controlled write in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Congratulations lime! Thank you for your awesome efforts here and reporting this issue to us -- great work!

### ch...@google.com (2025-03-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@chops-service-accounts.iam.gserviceaccount.com (2025-06-03)

The unexpected pass finder removed the last expectation associated with this bug. An associated CL should be landing shortly, after which this bug can be closed once a human confirms there is no more work to be done.

## Bounty Award

> high quality report demonstrating controlled write in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/379516109)*
