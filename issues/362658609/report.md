# security: heap-use-after-free on TouchToFillPaymentMethodControllerBridge_jni.h:31:108

| Field | Value |
|-------|-------|
| **Issue ID** | [362658609](https://issues.chromium.org/issues/362658609) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill, UI>Browser>Autofill>Payments |
| **Platforms** | Android |
| **Chrome Version** | 127.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | fr...@chromium.org |
| **Created** | 2024-08-28 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

will be update tonight with RCA.

# Problem Description

I don't have time now, I will analyze RCA tonight.

# Summary

security: heap-use-after-free on TouchToFillPaymentMethodControllerBridge\_jni.h:31:108

# Custom Questions

#### Type of crash:

brwoser

#### Crash state:

see asan

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [poc.html](attachments/poc.html) (text/html, 245 B)
- [sym2](attachments/sym2) (application/octet-stream, 10.4 KB)
- [uaf11-asan.log](attachments/uaf11-asan.log) (text/plain, 47.1 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 643.6 KB)
- [symbol.jpg.png](attachments/symbol.jpg.png) (image/png, 235.5 KB)
- [stack.txt](attachments/stack.txt) (text/plain, 19.8 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 787 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.1 KB)

## Timeline

### ti...@chromium.org (2024-08-28)

(security shepherd)

From the last bug: tested on commit 1f2922bea72e5fd29e84bf19a96bc53ef96feb6a

### ti...@chromium.org (2024-08-28)

[limmmmmeeee@gmail.com](mailto:limmmmmeeee@gmail.com) I think you may have accidentally uploaded the wrong poc:

```
<html><body>
</body>
<script>
    // w = window.open("http://localhost:8000/poc.html")
    w1 = window.open("https://fill.dev/form/credit-card-simple")
    setTimeout(()=>{
        w.close();
        // w1.close();
    },10000)
</script>
</html>

```

`w.close()` will throw an exception.

### li...@gmail.com (2024-08-28)

ohhhh, yes, you are right. should be this one.

```
<html><body>
</body>
<script>
    w1 = window.open("https://fill.dev/form/credit-card-simple")
    setTimeout(()=>{
        w1.close();
    },10000)
</script>
</html>

```

### pe...@google.com (2024-08-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### li...@gmail.com (2024-08-28)

I think I may have done other tests after the test, and did not check the POC, so I had this problem, Thanks for pointing it out.

### ti...@chromium.org (2024-08-28)

[limmmmmeeee@gmail.com](mailto:limmmmmeeee@gmail.com) could you symbolize your asan trace with `tools/valgrind/asan/asan_symbolize.py`. I am trying but not having any luck. I'm guessing you've modified the build just a little which is throwin off the symbols.

```
08-28 10:39:43.366 26913 26913 F DEBUG   : ==26048==ERROR: AddressSanitizer: heap-use-after-free on address 0x004fae7f8a58 at pc 0x006dc4dddb24 bp 0x007ff1015df0 sp 0x007ff1015de8
08-28 10:39:43.366 26913 26913 F DEBUG   : READ of size 8 at 0x004fae7f8a58 thread T0 (chromium.chrome)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #0 0x6dc4dddb20  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18bb7b20) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #1 0x6efc1a7570  (/apex/com.android.art/lib64/libart.so+0x3a7570) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #2 0x6efc4e53dc  (/apex/com.android.art/lib64/libart.so+0x6e53dc) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #3 0x6efc4e69b4  (/apex/com.android.art/lib64/libart.so+0x6e69b4) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #4 0x6efc4e69b4  (/apex/com.android.art/lib64/libart.so+0x6e69b4) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   : 
08-28 10:39:43.366 26913 26913 F DEBUG   : 0x004fae7f8a58 is located 472 bytes inside of 1600-byte region [0x004fae7f8880,0x004fae7f8ec0)
08-28 10:39:43.366 26913 26913 F DEBUG   : freed by thread T0 (chromium.chrome) here:
08-28 10:39:43.366 26913 26913 F DEBUG   :     #0 0x719d2f4710  (/system/lib64/libclang_rt.asan-aarch64-android.so+0xe8710) (BuildId: 076a3aa118eaf0d7275c7f5323293b645dde2fcb)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #1 0x6dc50a8f74  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18e82f74) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #2 0x6dc50a8744  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18e82744) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #3 0x6dbe8712e0  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x1264b2e0) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #4 0x6dbe8733a0  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x1264d3a0) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #5 0x6dc4c4fa68  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18a29a68) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #6 0x6efc1a7570  (/apex/com.android.art/lib64/libart.so+0x3a7570) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   : 
08-28 10:39:43.366 26913 26913 F DEBUG   : previously allocated by thread T0 (chromium.chrome) here:
08-28 10:39:43.366 26913 26913 F DEBUG   :     #0 0x719d2f3e90  (/system/lib64/libclang_rt.asan-aarch64-android.so+0xe7e90) (BuildId: 076a3aa118eaf0d7275c7f5323293b645dde2fcb)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #1 0x6dcd2c5c84  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x2109fc84) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #2 0x6dcd338be0  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x21112be0) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #3 0x6dc4c59b48  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18a33b48) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #4 0x6dbe89b6b0  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x126756b0) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #5 0x6dbe2c91c0  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x120a31c0) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #6 0x6dbc48fea8  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x10269ea8) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #7 0x6dc4f372a4  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18d112a4) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #8 0x6dc4f48860  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18d22860) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #9 0x6dc4f3af1c  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18d14f1c) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #10 0x6dc6ec8078  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x1aca2078) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #11 0x6dc6ec98b4  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x1aca38b4) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #12 0x6dc50b9358  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18e93358) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #13 0x6dc510bcf4  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18ee5cf4) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #14 0x6dc510b140  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18ee5140) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #15 0x6dc51e8f30  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18fc2f30) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #16 0x6dc51e8cd0  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18fc2cd0) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #17 0x6dc51e8204  (/data/app/~~-kJjMZuYR5bAJoDFkSEQ0w==/org.chromium.chrome-4odtA800riLB5GqYegrN4A==/lib/arm64/libchrome.so+0x18fc2204) (BuildId: cff9066ee28dccf2)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #18 0x719b8a65fc  (/system/lib64/libutils.so+0xf5fc) (BuildId: 76084bd1839ac5b79bbe3f2abb199da1)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #19 0x71a56147cc  (/system/lib64/libandroid_runtime.so+0x1817cc) (BuildId: 018f7126f3f91dbd25018e66353d2ba1)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #20 0x71356e80  (/system/framework/arm64/boot-framework.oat+0x1ede80) (BuildId: 85de1bdf510c2212a470fa4255a23560b2424fa6)

```

### li...@gmail.com (2024-08-28)

Hi, guy. how can i trace it with `tools/valgrind/asan/asan_symbolize.py`, i don't know the usage.

### pe...@google.com (2024-08-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### ti...@chromium.org (2024-08-28)

(security shepherd)

Good question [limmmmmeeee@gmail.com](mailto:limmmmmeeee@gmail.com). Pipe the output of your stacktrace to `tools/valgrind/asan/asan_symbolize.py` from within your build directory, reference here [1]

[1] <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md>

### ti...@chromium.org (2024-08-28)

Note: I am unable to reproduce with an MTE or asan build on the commit 1f2922bea72e5fd29e84bf19a96bc53ef96feb6a. [limmmmmeeee@gmail.com](mailto:limmmmmeeee@gmail.com) I will wait for the RCA and the reproduction instructions before triaging this. Thank you for reporting early :)

### li...@gmail.com (2024-08-28)

repro:

1. see mov

Note: I got symbolize with `asan_symbolize.py`.

```
08-28 10:39:43.366 26913 26913 F DEBUG   : ==26048==ERROR: AddressSanitizer: heap-use-after-free on address 0x004fae7f8a58 at pc 0x006dc4dddb24 bp 0x007ff1015df0 sp 0x007ff1015de8
08-28 10:39:43.366 26913 26913 F DEBUG   : READ of size 8 at 0x004fae7f8a58 thread T0 (chromium.chrome)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #0 0x18bb7b20 Java_org_1chromium_1chrome_1browser_1touch_11to_11fill_1payments_1TouchToFillPaymentMethodControllerBridge_1creditCardSuggestionSelected @ './gen/jni_headers/chrome/browser/touch_to_fill/autofill/android/internal/jni/TouchToFillPaymentMethodControllerBridge_jni.h:31:108'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #1 0x6efc1a7570  (/apex/com.android.art/lib64/libart.so+0x3a7570) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #2 0x6efc4e53dc  (/apex/com.android.art/lib64/libart.so+0x6e53dc) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #3 0x6efc4e69b4  (/apex/com.android.art/lib64/libart.so+0x6e69b4) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #4 0x6efc4e69b4  (/apex/com.android.art/lib64/libart.so+0x6e69b4) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :
08-28 10:39:43.366 26913 26913 F DEBUG   : 0x004fae7f8a58 is located 472 bytes inside of 1600-byte region [0x004fae7f8880,0x004fae7f8ec0)
08-28 10:39:43.366 26913 26913 F DEBUG   : freed by thread T0 (chromium.chrome) here:
08-28 10:39:43.366 26913 26913 F DEBUG   :     #0 0x719d2f4710  (/system/lib64/libclang_rt.asan-aarch64-android.so+0xe8710) (BuildId: 076a3aa118eaf0d7275c7f5323293b645dde2fcb)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #1 0x18e82f74 std::__Cr::default_delete<base::SupportsUserData::Data>::operator()(base::SupportsUserData::Data*) const @ './../../third_party/libc++/src/include/__memory/unique_ptr.h:80:5'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #2 0x18e82744 absl::container_internal::raw_hash_set<absl::container_internal::FlatHashMapPolicy<void const*, std::__Cr::unique_ptr<base::SupportsUserData::Data, std::__Cr::default_delete<base::SupportsUserData::Data>>>, absl::container_internal::HashEq<void const*, void>::Hash, absl::container_internal::HashEq<void const*, void>::Eq, std::__Cr::allocator<std::__Cr::pair<void const* const, std::__Cr::unique_ptr<base::SupportsUserData::Data, std::__Cr::default_delete<base::SupportsUserData::Data>>>>>::destructor_impl() @ './../../third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:3558:5'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #3 0x1264b2e0 content::WebContents::~WebContents() @ './../../content/public/browser/web_contents.h:392:35'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #4 0x1264d3a0 content::WebContentsImpl::~WebContentsImpl() @ './../../content/browser/web_contents/web_contents_impl.cc:1243:37'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #5 0x18a29a68 std::__Cr::default_delete<content::WebContents>::operator()(content::WebContents*) const @ './../../third_party/libc++/src/include/__memory/unique_ptr.h:80:5'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #6 0x6efc1a7570  (/apex/com.android.art/lib64/libart.so+0x3a7570) (BuildId: 7235eadf7f2345670bbe480eb7e491e7)
08-28 10:39:43.366 26913 26913 F DEBUG   :
08-28 10:39:43.366 26913 26913 F DEBUG   : previously allocated by thread T0 (chromium.chrome) here:
08-28 10:39:43.366 26913 26913 F DEBUG   :     #0 0x719d2f3e90  (/system/lib64/libclang_rt.asan-aarch64-android.so+0xe7e90) (BuildId: 076a3aa118eaf0d7275c7f5323293b645dde2fcb)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #1 0x2109fc84 autofill::ChromeAutofillClient::CreateForWebContents(content::WebContents*) @ './../../chrome/browser/ui/autofill/chrome_autofill_client.cc:180:26'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #2 0x21112be0 TabHelpers::AttachTabHelpers(content::WebContents*) @ './../../chrome/browser/ui/tab_helpers.cc:380:28'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #3 0x18a33b48 android::TabWebContentsDelegateAndroid::AddNewContents(content::WebContents*, std::__Cr::unique_ptr<content::WebContents, std::__Cr::default_delete<content::WebContents>>, GURL const&, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool, bool*) @ './../../chrome/browser/android/tab_web_contents_delegate_android.cc:357:3'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #4 0x126756b0 content::WebContentsImpl::ShowCreatedWindow(content::RenderFrameHostImpl*, int, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool) @ './../../content/browser/web_contents/web_contents_impl.cc:4983:15'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #5 0x120a31c0 content::RenderFrameHostImpl::ShowCreatedWindow(base::TokenType<blink::LocalFrameTokenTypeMarker> const&, WindowOpenDisposition, mojo::StructPtr<blink::mojom::WindowFeatures>, bool, base::OnceCallback<void ()>) @ './../../content/browser/renderer_host/render_frame_host_impl.cc:6560:34'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #6 0x10269ea8 blink::mojom::LocalMainFrameHostStubDispatch::AcceptWithResponder(blink::mojom::LocalMainFrameHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) @ './gen/third_party/blink/public/mojom/frame/frame.mojom.cc:21549:13'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #7 0x18d112a4 mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) @ './../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:990:56'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #8 0x18d22860 mojo::MessageDispatcher::Accept(mojo::Message*) @ './../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #9 0x18d14f1c mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) @ './../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:721:20'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #10 0x1aca2078 IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) @ './../../ipc/ipc_mojo_bootstrap.cc:1216:24'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #11 0x1aca38b4 void base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>::Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>(void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&) @ './../../base/functional/bind_internal.h:738:12'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #12 0x18e93358 base::OnceCallback<void ()>::Run() && @ './../../base/functional/callback.h:156:12'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #13 0x18ee5cf4 void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) @ './../../base/task/common/task_annotator.h:90:5'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #14 0x18ee5140 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() @ './../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #15 0x18fc2f30 base::MessagePumpAndroid::DoNonDelayedLooperWork(bool) @ './../../base/message_loop/message_pump_android.cc:208:33'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #16 0x18fc2cd0 base::MessagePumpAndroid::OnNonDelayedLooperCallback() @ './../../base/message_loop/message_pump_android.cc:194:3'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #17 0x18fc2204 base::(anonymous namespace)::NonDelayedLooperCallback(int, int, void*) @ './../../base/message_loop/message_pump_android.cc:57:9'
08-28 10:39:43.366 26913 26913 F DEBUG   :     #18 0x719b8a65fc  (/system/lib64/libutils.so+0xf5fc) (BuildId: 76084bd1839ac5b79bbe3f2abb199da1)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #19 0x71a56147cc  (/system/lib64/libandroid_runtime.so+0x1817cc) (BuildId: 018f7126f3f91dbd25018e66353d2ba1)
08-28 10:39:43.366 26913 26913 F DEBUG   :     #20 0x71356e80  (/system/framework/arm64/boot-framework.oat+0x1ede80) (BuildId: 85de1bdf510c2212a470fa4255a23560b2424fa6)


```

### li...@gmail.com (2024-08-28)

repro step:

1. open exp.html. You can set the delay at will
2. then open the select the creditcard autofill dialog (see video).
3. Then when the tab is about to close, hold the dialog of selecting creditcard and click on a card at will.

### pe...@google.com (2024-08-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### li...@gmail.com (2024-08-28)

RCA I still need to analyze for a while and think about the race between JavaDialog close and C++ function.

### li...@gmail.com (2024-08-28)

And i can easily repro on lastest canary version.

```
08-29 01:02:13.328 15301 15301 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x8080808080808094
08-29 01:02:13.328 15301 15301 F DEBUG   :     x0  00000072015b6350  x1  b400007510203b50  x2  0000007fdec33cf8  x3  0000000000000000
08-29 01:02:13.328 15301 15301 F DEBUG   :     x4  00000072015b6350  x5  0000007fdec33e48  x6  00000077975fc140  x7  00000074deb38334
08-29 01:02:13.328 15301 15301 F DEBUG   :     x8  8080808080808080  x9  b400007510203b50  x10 00000074502307a0  x11 0000007454108744
08-29 01:02:13.328 15301 15301 F DEBUG   :     x12 00000000000000e8  x13 0000000000000002  x14 0000000000000003  x15 00000000ebad6a89
08-29 01:02:13.328 15301 15301 F DEBUG   :     x16 0000007454108634  x17 0000007fdec33d40  x18 00000077a857c000  x19 00000072015b6350
08-29 01:02:13.328 15301 15301 F DEBUG   :     x20 0000000000000000  x21 b400007580213388  x22 00000074610f4542  x23 0000007463683028
08-29 01:02:13.328 15301 15301 F DEBUG   :     x24 00000074deb2e900  x25 0000007fdec33e60  x26 0000007fdec33e7c  x27 0000007fdec33e60
08-29 01:02:13.328 15301 15301 F DEBUG   :     x28 0000007fdec33d50  x29 0000007fdec33d20
08-29 01:02:13.328 15301 15301 F DEBUG   :     lr  00000074deb55434  sp  0000007fdec33cf0  pc  0000007454108764  pst 0000000040001000
08-29 01:02:13.328 15301 15301 F DEBUG   : 30 total frames
08-29 01:02:13.328 15301 15301 F DEBUG   : backtrace:
08-29 01:02:13.328 15301 15301 F DEBUG   :       #00 pc 0000000004508764  /data/app/~~JY0yqbjHr1KELD9t-SPt6Q==/com.google.android.trichromelibrary.canary_668100033-CNKNGTp_m5kjXQISsvnH8w==/base.apk!libmonochrome_64.so (offset 0x8e0000) (Java_J_N__1V_1ZJO+304) (BuildId: e926efbba1c562d7e8f2aa4b402d3232cb5a54d1)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #01 pc 0000000000227430  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+144) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #02 pc 0000000000209b1c  /apex/com.android.art/lib64/libart.so (nterp_helper+1948) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #03 pc 00000000004f4542  /data/app/~~X2NhPpSwNVCv1h1jnI3uKA==/com.chrome.canary-X8UfVUMSFe5AI5S8aSWedw==/split_chrome.apk (org.chromium.chrome.browser.touch_to_fill.payments.TouchToFillPaymentMethodControllerBridge.b+54)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #04 pc 000000000020b0f4  /apex/com.android.art/lib64/libart.so (nterp_helper+7540) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #05 pc 0000000000410d3c  /data/app/~~X2NhPpSwNVCv1h1jnI3uKA==/com.chrome.canary-X8UfVUMSFe5AI5S8aSWedw==/split_chrome.apk (.run wchar_t::*+60)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #06 pc 000000000020b0f4  /apex/com.android.art/lib64/libart.so (nterp_helper+7540) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #07 pc 000000000041138e  /data/app/~~X2NhPpSwNVCv1h1jnI3uKA==/com.chrome.canary-X8UfVUMSFe5AI5S8aSWedw==/split_chrome.apk (Uw4.onClick+58)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #08 pc 0000000000b068c8  /system/framework/arm64/boot-framework.oat (android.view.View.performClick+456) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #09 pc 00000000009f1b9c  /system/framework/arm64/boot-framework.oat (android.view.View$PerformClick.run+460) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #10 pc 00000000007dc1fc  /system/framework/arm64/boot-framework.oat (android.os.Handler.dispatchMessage+76) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #11 pc 00000000007dfbb8  /system/framework/arm64/boot-framework.oat (android.os.Looper.loopOnce+1080) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #12 pc 00000000007df6ec  /system/framework/arm64/boot-framework.oat (android.os.Looper.loop+572) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #13 pc 000000000045b030  /system/framework/arm64/boot-framework.oat (android.app.ActivityThread.main+2224) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #14 pc 0000000000210c80  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+640) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #15 pc 00000000002554c0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+224) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #16 pc 000000000064cbb4  /apex/com.android.art/lib64/libart.so (_jobject* art::InvokeMethod<(art::PointerSize)8>(art::ScopedObjectAccessAlreadyRunnable const&, _jobject*, _jobject*, _jobject*, unsigned long)+1588) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #17 pc 00000000005c48e0  /apex/com.android.art/lib64/libart.so (art::Method_invoke(_JNIEnv*, _jobject*, _jobject*, _jobjectArray*) (.__uniq.165753521025965369065708152063621506277)+32) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #18 pc 00000000000ae578  /system/framework/arm64/boot.oat (art_jni_trampoline+120) (BuildId: 4a75ea42b3b7454bce2f25fb5e4215ae8c841c7d)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #19 pc 0000000000cd5214  /system/framework/arm64/boot-framework.oat (com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run+132) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #20 pc 0000000000ce2550  /system/framework/arm64/boot-framework.oat (com.android.internal.os.ZygoteInit.main+3936) (BuildId: 29a5ef97cf8bbeac6fb8bb0814351e4db8267bae)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #21 pc 0000000000210c80  /apex/com.android.art/lib64/libart.so (art_quick_invoke_static_stub+640) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #22 pc 00000000002554c0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+224) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #23 pc 000000000064d438  /apex/com.android.art/lib64/libart.so (art::JValue art::InvokeWithVarArgs<art::ArtMethod*>(art::ScopedObjectAccessAlreadyRunnable const&, _jobject*, art::ArtMethod*, std::__va_list)+408) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #24 pc 000000000064da10  /apex/com.android.art/lib64/libart.so (art::JValue art::InvokeWithVarArgs<_jmethodID*>(art::ScopedObjectAccessAlreadyRunnable const&, _jobject*, _jmethodID*, std::__va_list)+80) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #25 pc 0000000000516e64  /apex/com.android.art/lib64/libart.so (art::JNI<true>::CallStaticVoidMethodV(_JNIEnv*, _jclass*, _jmethodID*, std::__va_list)+692) (BuildId: b9aed2f60572a46c0e56cf3244c61909)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #26 pc 00000000000dfca8  /system/lib64/libandroid_runtime.so (_JNIEnv::CallStaticVoidMethod(_jclass*, _jmethodID*, ...)+104) (BuildId: 282bb25132ccc31e32a1b5c6b5a1c8ea)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #27 pc 00000000000ebeac  /system/lib64/libandroid_runtime.so (android::AndroidRuntime::start(char const*, android::Vector<android::String8> const&, bool)+988) (BuildId: 282bb25132ccc31e32a1b5c6b5a1c8ea)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #28 pc 00000000000028fc  /system/bin/app_process64 (main+1356) (BuildId: 9f07d9eda26c3f1a4395c63856947c26)
08-29 01:02:13.328 15301 15301 F DEBUG   :       #29 pc 000000000009dbf8  /apex/com.android.runtime/lib64/bionic/libc.so (__libc_init+104) (BuildId: 35647bdbfd4abaae505972042de0d304)


```

### ti...@chromium.org (2024-08-28)

(security shepherd)

Thank you for the detailed reproduction instructions and the ASAN trace, hopefully asan\_symbolize.py will be helpful for you in the future :)

### ti...@chromium.org (2024-08-28)

(security shepherd)

I was able to reproduce on an MTE device as well. This bug requires clicking on the credit card number you want to autofill right when the window closes so it therefore requires unlikely user interaction but should still be fixed.

- According to the guidelines this is an S1 because it is a uaf not protected by miracleptr `MiraclePtr Status: NOT PROTECTED`, from an uncompromised renderer, but downgraded because it requires unlikely user interaction.
- OS is only Android
- Tentatively putting Foundin-128 while I build stable Android, but I see no new changes to this code that would have recently caused this in only head or canary so it is likely Foundin-128.

[limmmmmeeee@gmail.com](mailto:limmmmmeeee@gmail.com) please continue conducting your RCA in the meantime :)

### ti...@chromium.org (2024-08-28)

schwering@ you recently touched `TouchToFillPaymentMethodController::CreditCardSuggestionSelected` while fixing [crbug.com/41495835](https://crbug.com/41495835), would you be a good owner for this?

### li...@gmail.com (2024-08-29)

## RCA

1. The Java class `TouchToFillPaymentMethodControllerBridge` holds the `mNativeTouchToFillPaymentMethodViewController`.

```
@JNINamespace("autofill")
class TouchToFillPaymentMethodControllerBridge
        implements TouchToFillPaymentMethodComponent.Delegate {
    private long mNativeTouchToFillPaymentMethodViewController;

    private TouchToFillPaymentMethodControllerBridge(
            long nativeTouchToFillPaymentMethodViewController) {
        mNativeTouchToFillPaymentMethodViewController =
                nativeTouchToFillPaymentMethodViewController;
    }

```

2. I think that when `WebContents` is destroyed, `WebContentsDestroyed` is called, which then calls the view hide function, and then calls C++ `TouchToFillPaymentMethodController::OnDismissed` from Java, causing the `java_object_` to be `Reset`.

```
void TouchToFillPaymentMethodController::WebContentsDestroyed() {
  Hide();
}
------------------------------------------------------------------
void TouchToFillPaymentMethodController::Hide() {
  if (view_)
    view_->Hide();
}
------------------------------------------------------------------
void TouchToFillPaymentMethodController::OnDismissed(JNIEnv* env,
                                                  bool dismissed_by_user) {
  if (delegate_) {
    delegate_->OnDismissed(dismissed_by_user);
  }
  view_.reset();
  delegate_.reset();
  java_object_.Reset(); // !!!
  keyboard_suppressor_.Unsuppress();
}


```

3. After `java_object_` is reset, `WebContentsImpl::~WebContentsImpl` will be called, and then `TouchToFillPaymentMethodController` is destroyed, calling `TouchToFillPaymentMethodController::~TouchToFillPaymentMethodController`, but at this time `java_object_` has been reset, so `onNativeDestroyed` in the destructor is not called, and then `mNativeTouchToFillPaymentMethodViewController` is not cleared at all.

```
TouchToFillPaymentMethodController::~TouchToFillPaymentMethodController() {
  if (java_object_) { // !!!
    Java_TouchToFillPaymentMethodControllerBridge_onNativeDestroyed(
        base::android::AttachCurrentThread(), java_object_);
  }
}
------------------------------------------------------------------
@JNINamespace("autofill")
class TouchToFillPaymentMethodControllerBridge
        implements TouchToFillPaymentMethodComponent.Delegate {
    private long mNativeTouchToFillPaymentMethodViewController;

[...]

    @CalledByNative
    private void onNativeDestroyed() {
        mNativeTouchToFillPaymentMethodViewController = 0; // No call here.
    }
[...]

```

1.1 <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/internal/java/src/org/chromium/chrome/browser/touch_to_fill/payments/TouchToFillPaymentMethodControllerBridge.java;l=17;drc=82dff63dbf9db05e9274e11d9128af7b9f51ceaa;bpv=0;bpt=1>

2.1 <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc;l=64>

2.2 <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc;drc=82dff63dbf9db05e9274e11d9128af7b9f51ceaa;l=139>

2.3 <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc;l=151>

3.1 <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc;l=56>

3.2 <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/internal/java/src/org/chromium/chrome/browser/touch_to_fill/payments/TouchToFillPaymentMethodControllerBridge.java;l=38;drc=82dff63dbf9db05e9274e11d9128af7b9f51ceaa;bpv=0;bpt=1>

## fix suggestion:

```
Move `Reset()` to `WebContentsDestroyed` to be destroyed or directly delete `reset()` in `OnDismissed`. After testing. Both did a great job. But consider the consistency with the original code. So I recommend the first solution.

```
```
diff --git a/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc b/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
index 890b000f21809..80a5fd506ee60 100644
--- a/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
+++ b/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
@@ -61,6 +61,9 @@ TouchToFillPaymentMethodController::~TouchToFillPaymentMethodController() {
 
 void TouchToFillPaymentMethodController::WebContentsDestroyed() {
   Hide();
+  Java_TouchToFillPaymentMethodControllerBridge_onNativeDestroyed(
+    base::android::AttachCurrentThread(), java_object_);
+  java_object_.Reset();
 }
 
 void TouchToFillPaymentMethodController::DidFinishNavigation(
@@ -146,8 +149,7 @@ void TouchToFillPaymentMethodController::OnDismissed(JNIEnv* env,
     delegate_->OnDismissed(dismissed_by_user);
   }
   view_.reset();
-  delegate_.reset();
-  java_object_.Reset();
+  delegate_.reset(); 
   keyboard_suppressor_.Unsuppress();
 }



```

fix2:

```
diff --git a/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc b/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
index 890b000f21809..50efcafde5a47 100644
--- a/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
+++ b/chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
@@ -147,7 +147,6 @@ void TouchToFillPaymentMethodController::OnDismissed(JNIEnv* env,
   }
   view_.reset();
   delegate_.reset();
-  java_object_.Reset();
   keyboard_suppressor_.Unsuppress();
 }


```

### pe...@google.com (2024-08-29)

Setting milestone because of s0/s1 severity.

### li...@gmail.com (2024-08-29)

fix file. And bitset: <https://source.chromium.org/chromium/chromium/src/+/880bfb2a5a456eab7637ab48e87c3d97f7c0eccd>

### fr...@chromium.org (2024-08-30)

That fix is sensible. I'd propose to reset the java\_object\_ with a helper though so we can address [the other place in the same class where the object is reset without severing the connection via JNI](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc;l=107;drc=a8089279ed05c89d4fa360414bc79618faeacbdd).

### ap...@google.com (2024-09-02)

Project: chromium/src
Branch: main

commit b1f596c561fa3fdf982b227b2d36865077d82438
Author: Friedrich Horschig <fhorschig@chromium.org>
Date:   Mon Sep 02 15:46:42 2024

    [Android][UAF] Always clean up native ptr in bridge when resetting bridge
    
    At the moment, the java object is reset at various moments in the
    controller but the native ptr is only nulled in the destructor.
    
    Even worse, the destructor null-checks the java object which means that
    the native ptr is never actually nulled in the java bridge and may cause
    a number of UAFs. See bug for more details.
    
    Fixed: 362658609
    Change-Id: Id64d5b6f03b801aeed35383b012e6895f3de0fec
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5826557
    Reviewed-by: Christoph Schwering <schwering@google.com>
    Commit-Queue: Friedrich Hauser <fhorschig@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1349878}

M       chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
M       chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.h

https://chromium-review.googlesource.com/5826557


### pe...@google.com (2024-09-03)

Security Merge Request Consideration: Requesting merge to stable (M128) because latest trunk commit (1349878) appears to be after stable branch point (1331488).
Security Merge Request Consideration: Requesting merge to beta (M129) because latest trunk commit (1349878) appears to be after beta branch point (1343869).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-09-03)

Merge review required: M129 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-09-03)

Merge review required: M128 is already shipping to stable.

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

### fr...@chromium.org (2024-09-04)

Re [comment #25](https://issues.chromium.org/issues/362658609#comment25): (security questionaire)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/5826557>
2. Tested on Canary.
3. Very small risk. The UAF is happened on closing the sheet, so it's notoriously hard to test.
4. No? Compatibility to what could be affected here?
5. No.
6. Done. (Clank only)

Re [comment #26](https://issues.chromium.org/issues/362658609#comment26) & [comment #27](https://issues.chromium.org/issues/362658609#comment27):

1. It's a security & stability fix without user-visible change.
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5826557>
3. Yes, released and tested on Canary.
4. Not feature-guarded anymore.
5. —
6. No manual testing recommended.

### pg...@google.com (2024-09-05)

thank you for the detailed responses to the questionnaire!

I've looked at both Canary and Dev data and I don't see any stability concerns with this fix

Merge approved for M128! Please merge to branch 6613 by Friday Sep 5 10AM MTV time to get this change into the next M128 respin!   

Merge approved for M129! Please merge to branch 6668 by Monday Sep 9 EOD MTV time to get this change into the next M129 release!

### ap...@google.com (2024-09-06)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 916f4ee42f992407bbc7df69ed55b3b19c23543b
Author: Friedrich Horschig <fhorschig@chromium.org>
Date:   Fri Sep 06 11:33:39 2024

    [M128][Android][UAF] Always clean up native ptr in bridge when resetting bridge
    
    At the moment, the java object is reset at various moments in the
    controller but the native ptr is only nulled in the destructor.
    
    Even worse, the destructor null-checks the java object which means that
    the native ptr is never actually nulled in the java bridge and may cause
    a number of UAFs. See bug for more details.
    
    (cherry picked from commit b1f596c561fa3fdf982b227b2d36865077d82438)
    
    Fixed: 362658609
    Change-Id: Id64d5b6f03b801aeed35383b012e6895f3de0fec
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5826557
    Reviewed-by: Christoph Schwering <schwering@google.com>
    Commit-Queue: Friedrich Hauser <fhorschig@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1349878}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5839729
    Reviewed-by: Timofey Chudakov <tchudakov@google.com>
    Auto-Submit: Friedrich Hauser <friedrichh@chromium.org>
    Commit-Queue: Timofey Chudakov <tchudakov@google.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#1620}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
M       chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.h

https://chromium-review.googlesource.com/5839729


### ap...@google.com (2024-09-06)

Project: chromium/src
Branch: refs/branch-heads/6668

commit 5e3af1606bb4d30f674162b52531d4c611ad88fb
Author: Friedrich Horschig <fhorschig@chromium.org>
Date:   Fri Sep 06 11:34:29 2024

    [M129][Android][UAF] Always clean up native ptr in bridge when resetting bridge
    
    At the moment, the java object is reset at various moments in the
    controller but the native ptr is only nulled in the destructor.
    
    Even worse, the destructor null-checks the java object which means that
    the native ptr is never actually nulled in the java bridge and may cause
    a number of UAFs. See bug for more details.
    
    (cherry picked from commit b1f596c561fa3fdf982b227b2d36865077d82438)
    
    Fixed: 362658609
    Change-Id: Id64d5b6f03b801aeed35383b012e6895f3de0fec
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5826557
    Reviewed-by: Christoph Schwering <schwering@google.com>
    Commit-Queue: Friedrich Hauser <fhorschig@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1349878}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5840234
    Auto-Submit: Friedrich Hauser <friedrichh@chromium.org>
    Commit-Queue: Timofey Chudakov <tchudakov@google.com>
    Commit-Queue: Friedrich Hauser <friedrichh@chromium.org>
    Reviewed-by: Timofey Chudakov <tchudakov@google.com>
    Cr-Commit-Position: refs/branch-heads/6668@{#930}
    Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

M       chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.cc
M       chrome/browser/touch_to_fill/autofill/android/touch_to_fill_payment_method_controller.h

https://chromium-review.googlesource.com/5840234


### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$4,000 for report of moderately mitigated security bug in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Congratulations, lime! Thank you for your efforts and reporting this issue to us!

### li...@gmail.com (2024-09-11)

Hi, @Amy. Thanks again, but I have a question, according to this vulnerability, issue: 358296941, this issue have more/Large UI operations than this vulnerability. Why is the reward for this payment vulnerability not even 1/6 of it?

### am...@chromium.org (2024-09-12)

Hi lime, thanks for reaching out. The report for [crbug.com/358296941](https://crbug.com/358296941) is not publicly available, so I'm presuming you're basing your assumptions on the fix for [crbug.com/358296941](https://crbug.com/358296941) rather than the details of the issue and POC, but that issue was demonstrated with exceptionally minimal and standard user interaction via a high quality report, warranting the reward amount.

For this issue, there is a requirement for non-standard user interaction with a race and timing issue involved, requiring the user to click on the credit card number for autofill precisely before the window closure / profile destruction. This method provides higher preconditions to exploit and lower potential for successful exploitation and attacker control.

Hope that helps!

### pe...@google.com (2024-12-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/362658609)*
