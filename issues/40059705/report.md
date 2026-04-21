# Security: UAF in InterestGroupPermissionsChecker::OnRequestComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40059705](https://issues.chromium.org/issues/40059705) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>InterestGroups |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2022-05-19 |
| **Bounty** | $20,000.00 |

## Description

**Steps to reproduce the problem:**

## Reproduce

- chromium commit hash

```
commit 392465f82cafe6835f1995d949dfbd8dbd652897 (HEAD -> main, origin/main, origin/HEAD)  
Author: Yoshifumi Inoue <yosin@chromium.org>  
Date:   Wed May 18 07:55:08 2022 +0000  

```

- build config

```
is_asan = true  
is_debug = false  
enable_nacl = false  
is_component_build = true  
symbol_level=1  
dcheck_always_on=false  

```

No user interaction (extension)

0. Apply a patch for one of the two vulnerabilities.(The process race patch is recommended as this is the default json parsing function)
1. Host index.html with a web server: python3 -m http.server 8000
2. Install the attached extension (ext) and allow in incognito
3. run ./out/release/chrome -enable-blink-features=MojoJS --user-data-dir=./userdata --load-extension=/path/to/ext

see the attachment for the reproduced video, note that I omitted the step of and allow ext in incognito

\*\*Note: Allow incognito is just needed because I'm using the chrome.windows api to simulate closing a browser window.\*\*

User interaction (exit browser)

0. Apply a patch for one of the two vulnerabilities.(The process race patch is recommended as this is the default json parsing function)
1. Host index.html with a web server: python3 -m http.server 8000
2. Open incognito browser (\*\*can be another chrome instance, guest view, etc - we just need two Profile instances\*\*)
3. Navigate to to <http://127.0.0.1:8000/poc.html>
4. close incognito browser

**Problem Description:**

## Root Cause with two UAF pattern

This vulnerability is similar to two issue:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1289523>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1233942>

[0] InterestGroupPermissionsChecker is a field of InterestGroupManagerImpl and is owned by StoragePartitionImpl, so it is bound to the life cycle of the Profile, and when the Profile is released, InterestGroupPermissionsChecker is also released.

[1] InterestGroupPermissionsChecker::OnRequestComplete binds base::Unretained(this) to InterestGroupPermissionsChecker::OnJsonParsed callback，and as a callback parameter to ParseJson.

\*\*There are two paths in DataDecoder::ParseJson that can cause UAF.\*\*

### First place: \*\*thread callback race pattern\*\*

If we enable BUILD\_RUST\_JSON\_PARSER when compiling

[2] The `callback with Unretained InterestGroupPermissionsChecker raw ptr` is posted to a separate sequence in threadpool.

[3] InterestGroupPermissionsChecker may be destroyed in UI thread when ReadAndReturnValueWithError run in threadpool.

And when ParsingComplete is sent back to UI thread, it will be executed to InterestGroupPermissionsChecker::OnJsonParsed callback(bind Unretained InterestGroupPermissionsChecker raw ptr), thus triggering UAF.

### Second place: \*\*process callback race pattern\*\*

by default

[4] ParseJson will use callback with Unretained InterestGroupPermissionsChecker raw ptr to create a reference counted request, so even if the profile is released, the request will not be released, the mojo connection will not be disconnected, and the request will have callback as one of its fields callback\_ save.

[5] The JsonParserImpl::Parse function in the service process will be called through mojo.

[6] While Parse is executing asynchronously in the service process, we close the window in the browser process to release the Profile and the associated InterestGroupPermissionsChecker.

When the service process finishes executing JsonParserImpl::Parse, it will send the result back to the browser process through callback.

[7] This will eventually call the callback with Unretained InterestGroupPermissionsChecker raw ptr in the OnServiceValueOrError function, triggering the UAF.

### bug link

[0] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/storage_partition_impl.cc;l=1318;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/interest_group/interest_group_permissions_checker.cc;l=167;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/public/cpp/data_decoder.cc;l=187;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/public/cpp/data_decoder.cc;l=133;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/public/cpp/data_decoder.cc;l=208;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/public/cpp/data_decoder.cc;l=216;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[6] <https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/json_parser_impl.cc;l=19;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

[7] <https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/public/cpp/data_decoder.cc;l=90;drc=8a609a649e36c8099c6801d41aca1ec3b0b3af73>

**Additional Comments:**

```
  
void StoragePartitionImpl::Initialize(  
	...  
	if (base::FeatureList::IsEnabled(blink::features::kInterestGroupStorage)) {  
	    // Auction worklets on non-Android use dedicated processes; on Android due  
	    // to high cost of process launch they try to reuse renderers.  
	    interest_group_manager_ = std::make_unique<InterestGroupManagerImpl>(  
        path, is_in_memory(), //<-------[0]  
  
class CONTENT_EXPORT StoragePartitionImpl  
    : public StoragePartition,  
      public blink::mojom::DomStorage,  
      public network::mojom::NetworkContextClient,  
      public network::mojom::URLLoaderNetworkServiceObserver {  
		...  
		std::unique_ptr<InterestGroupManagerImpl> interest_group_manager_;  
}  
  
class CONTENT_EXPORT InterestGroupManagerImpl : public InterestGroupManager {  
  ...  
	// Checks if a frame can join or leave an interest group. Global so that  
	// pending operations can continue after a page has been navigate away from.  
  InterestGroupPermissionsChecker permissions_checker_;  
}  

```
```
void InterestGroupPermissionsChecker::OnRequestComplete(  
    ActiveRequestMap::iterator active_request,  
    std::unique_ptr<std::string> response_body) {  
  const auto\* response_info =  
      active_request->second->simple_url_loader->ResponseInfo();  
  if (!response_body || !response_info ||  
      !blink::IsJSONMimeType(response_info->mime_type)) {  
    OnActiveRequestComplete(active_request, Permissions());  
    return;  
  }  
  
  // `simple_url_loader` is no longer needed after this point.  
  active_request->second->simple_url_loader.reset();  
  
  active_request->second->data_decoder.ParseJson(  
      \*response_body,  
      base::BindOnce(&InterestGroupPermissionsChecker::OnJsonParsed,  
                     base::Unretained(this), active_request)); //<------[1]  
}  

```
```
void DataDecoder::ParseJson(const std::string& json,  
                            ValueParseCallback callback) {  
#if BUILDFLAG(BUILD_RUST_JSON_PARSER)  
  // Parses JSON directly in the calling process using the memory-safe  
  // Rust parser.  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::TaskPriority::BEST_EFFORT},  
      base::BindOnce(  
          [](const std::string& json) {  
            return base::JSONReader::ReadAndReturnValueWithError(  
                json, base::JSON_PARSE_RFC);  
          },  
          json),  
      base::BindOnce(&ParsingComplete, std::move(callback)));//<-------[2]  
...  
}  
  
#if BUILDFLAG(IS_ANDROID) || BUILDFLAG(BUILD_RUST_JSON_PARSER)  
  
void ParsingComplete(DataDecoder::ValueParseCallback callback,  
                     base::JSONReader::ValueWithError value_with_error) {  
  if (!value_with_error.value) {  
    std::move(callback).Run(//<----------[3]  
        DataDecoder::ValueOrError::Error(value_with_error.error_message));  
  } else {  
    std::move(callback).Run(  
        DataDecoder::ValueOrError::Value(std::move(\*value_with_error.value)));  
  }  
}  
  

```
```
void DataDecoder::ParseJson(const std::string& json,  
                            ValueParseCallback callback) {  
...  
#else  
  // Parse JSON out-of-process.  
  auto request =  
      base::MakeRefCounted<ValueParseRequest<mojom::JsonParser, base::Value>>(  
          std::move(callback));//<-------[4]  
  GetService()->BindJsonParser(request->BindRemote());  
  request->remote()->Parse(  
      json, base::JSON_PARSE_RFC,  
      base::BindOnce(&ValueParseRequest<mojom::JsonParser,  
                                        base::Value>::OnServiceValueOrError,  
                     request));//<-------[5]  
#endif  
}  
  
void JsonParserImpl::Parse(const std::string& json,   
                           uint32_t options,  
                           ParseCallback callback) {  
  base::JSONReader::ValueWithError ret =  
      base::JSONReader::ReadAndReturnValueWithError(json, options);  
  if (ret.value) {  
    std::move(callback).Run(std::move(ret.value), absl::nullopt);//<-------[6]  
  } else {  
    std::move(callback).Run(absl::nullopt,  
                            absl::make_optional(std::move(ret.error_message)));  
  }  
}  
  
template <typename T, typename V>  
class ValueParseRequest : public base::RefCounted<ValueParseRequest<T, V>> {  
 public:  
  
	DataDecoder::ResultCallback<V>& callback() { return callback_; }  
  
  // Handles a successful parse from the service.  
  void OnServiceValueOrError(absl::optional<V> value,  
                             const absl::optional<std::string>& error) {  
    if (!callback())  
      return;  
  
    DataDecoder::ResultOrError<V> result;  
    if (value)  
      result.value = std::move(value);  
    else  
      result.error = error.value_or("unknown error");  
  
    // Copy the callback onto the stack before resetting the Remote, as that may  
    // delete |this|.  
    auto local_callback = std::move(callback());  
  
    // Reset the |remote_| since we aren't using it again and we don't want it  
    // to trip the disconnect handler. May delete |this|.  
    remote_.reset();  
  
    // We run the callback after reset just in case it does anything funky like  
    // spin a nested RunLoop.  
    std::move(local_callback).Run(std::move(result));//<-----[7]  
  }  
  
	...  
  DataDecoder::ResultCallback<V> callback_;   
};  
  

```
## Other

Explain the patch.

This vulnerability can obviously be triggered by mojojs using a compromise render, but since I haven't been able to construct the parameters of the mojo interface well, I can only patch some checks to execute the vulnerable code, but the vulnerable code is obviously OK Triggered by normal function.

In addition, I added sleep to JsonParserImpl::Parse or JSONReader::ReadAndReturnValueWithError to block it, which makes it easier to trigger this vulnerability.  

But this can obviously be blocked by constructing an extremely large json parameter, increasing the possibility of successful competition.

Because this vulnerability can be triggered by a plug-in without interaction, and the message loop can be blocked by sending a large json parameter or sending a large number of ipc messages, so as to control the timing of use.

So I think inducing users to install a malicious plugin that does not require any permissions will most likely lead to remote code execution, which is a serious vulnerability.

\*\*Chrome version: \*\* 101.0.4951.67 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.0 KB)
- [asan_process_race.txt](attachments/asan_process_race.txt) (text/plain, 36.6 KB)
- [patch_to_trigger_process_race_uaf.diff](attachments/patch_to_trigger_process_race_uaf.diff) (text/plain, 7.4 KB)
- [asan_thread_race.txt](attachments/asan_thread_race.txt) (text/plain, 36.4 KB)
- [patch_to_trigger_thread_race_uaf.diff](attachments/patch_to_trigger_thread_race_uaf.diff) (text/plain, 13.7 KB)
- [repro_with_extension.mp4](attachments/repro_with_extension.mp4) (video/mp4, 6.5 MB)
- [repro_with_exit_browser.mp4](attachments/repro_with_exit_browser.mp4) (video/mp4, 4.8 MB)
- [patch.diff](attachments/patch.diff) (text/plain, 2.0 KB)

## Timeline

### et...@gmail.com (2022-05-19)

attach repro video by exit incognito browser

### et...@gmail.com (2022-05-19)

This vulnerability is easy to fix, referring to this commit(https://chromium.googlesource.com/chromium/src/+/65080d25a92a1a4fb45d052277702ae2aac19be4%5E%21/#F0), I made a patch for this vulnerability.

please check it :)


### et...@gmail.com (2022-05-19)

I think this vulnerability was introduced in this commit: 
https://source.chromium.org/chromium/chromium/src/+/8b7e13c6059a37b01b7f11a7c53faa713919e580

### dt...@chromium.org (2022-05-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>InterestGroups]

### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-05-19)

Thanks for the report.

A UAF that requires a browser patch in order to trigger is always something we have to question, because the PoC doesn't really demonstrate that it's a reachable bug in Chrome. If it was just sleeps to rig race conditions that would be one thing, but there are functional changes to that code.

That said, passing a base::Unretained in the DataDecoder::ParseJson callback does look like a bug and should be fixed.

Setting at Security_Severity-High based on the need for an extension or compromised renderer, but if the race condition is really hard to hit then this could be lower.

mmenke@: The fix is trivial, as the reporter notes, but do you have any concerns? Or else thoughts on reachability of this bug, given the patches needed to repro?

### [Deleted User] (2022-05-19)

[Empty comment from Monorail migration]

### mm...@chromium.org (2022-05-20)

[+rsesek]:  DataDecoder has no docs on safe usage.  I had thought that "Encapsulates an exclusive connection to an isolated instance of the Data Decoder service" meant that deleting a DataDecoder would be analogous to tearing down a Mojo pipe, so no weak pointers would be needed.  It looks like it creates its own remotes...but wraps them in a refcounted objects in order to invoke callbacks after the DataDecoder itself is destroyed?  This seems unexpected to me.

I had assumed the difference between the static and non-static methods was precisely around the non-static API calls not invoking callbacks after the destruction of the DataDecoder.

### mm...@chromium.org (2022-05-20)

[rsesek]:  Actually, the description of the bug seems to directly contradict the API description:

  // Note that |callback| will only be called if the parsing operation succeeds
  // or fails before this DataDecoder is destroyed.
  void ParseJson(const std::string& json, ValueParseCallback callback);

That implies this method should be safe to call as InterestGroupPermissionsChecker does, with base::Unretained(this), where `this` owns the DataDecoder.  I think this is a DataDecoder bug.

Am I missing something?

### et...@gmail.com (2022-05-20)

I can understand your doubt, but after my test it is indeed: 
>> creates its own remotes, but wraps them in a refcounted objects in order to invoke callbacks after the DataDecoder itself is destroyed
Could you try to check it like this, thank you very much :)

content/browser/interest_group/interest_group_permissions_checker.cc
```
void InterestGroupPermissionsChecker::OnRequestComplete(
    ActiveRequestMap::iterator active_request,
    std::unique_ptr<std::string> response_body) {
  LOG(ERROR) << "InterestGroupPermissionsChecker::OnRequestComplete" << std::endl;
  ...
  // `simple_url_loader` is no longer needed after this point.
  active_request->second->simple_url_loader.reset();
  LOG(ERROR) << "data_decode addr is: " << &active_request->second->data_decoder << std::endl;
  active_request->second->data_decoder.ParseJson(
      *response_body,
      base::BindOnce(&InterestGroupPermissionsChecker::OnJsonParsed,
                     base::Unretained(this), active_request));
}
```

services/data_decoder/public/cpp/data_decoder.cc
```
DataDecoder::~DataDecoder(){
  LOG(ERROR) << "sakura in DataDecoder::~DataDecoder: " << this << std::endl;
}
```

[669367:669367:0520/213618.266859:ERROR:ad_auction_service_impl.cc(135)] sakura in AdAuctionServiceImpl::JoinInterestGroup

[669367:669367:0520/213618.272033:ERROR:interest_group_permissions_checker.cc(157)] InterestGroupPermissionsChecker::OnRequestComplete

[669367:669367:0520/213618.272163:ERROR:interest_group_permissions_checker.cc(168)] data_decode addr is: 0x608000399ec0  // <---------------------------[0]  print used DataDecoder addr here 

[669367:669367:0520/213618.272407:ERROR:data_decoder.cc(178)] sakura in DataDecoder::ParseJson

[669367:669367:0520/213618.273660:ERROR:json_parser.mojom.cc(111)] sakura in JsonParserProxy::Parse

[669549:1:0520/213618.307387:ERROR:json_parser_impl.cc(22)] sakura in JsonParserImpl::Parse

[669367:669367:0520/213621.334993:ERROR:interest_group_permissions_checker.cc(80)] InterestGroupPermissionsChecker::~InterestGroupPermissionsChecker //<-----------[1] close browser to trigger InterestGroupPermissionsChecker destroy

[669367:669367:0520/213621.335051:ERROR:data_decoder.cc(150)] sakura in DataDecoder::~DataDecoder: 0x608000399ec0 // <---------------------------[2]  used DataDecoder destroy here 

[669367:669367:0520/213621.953971:ERROR:data_decoder.cc(150)] sakura in DataDecoder::~DataDecoder: 0x60600084ff80

[669367:669367:0520/213621.965165:ERROR:data_decoder.cc(150)] sakura in DataDecoder::~DataDecoder: 0x606000873e00

[669367:669367:0520/213628.309121:ERROR:interest_group_permissions_checker.cc(178)] sakura in InterestGroupPermissionsChecker::OnJsonParsed// <---------------------------[3]  callback invoke after the DataDecoder itself is destroyed, and uaf

=================================================================
==669367==ERROR: AddressSanitizer: heap-use-after-free on address 0x6140003495c8 at pc 0x7f92cbcf1940 bp 0x7ffdde4bbdb0 sp 0x7ffdde4bbda8
READ of size 8 at 0x6140003495c8 thread T0 (chrome)
    #0 0x7f92cbcf193f in operator-> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:284:19
...

This may indeed be a weird design, but it happens. And since DataDecoder::ParseJson is already widely used, I thought a trivial fix (as I attached) might be more appropriate?

### [Deleted User] (2022-05-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2022-05-20)

It's not currently enabled on stable.  I'm also not comfortable reverting a a half-dozen CLs and calling this fixed, because the issue is the underlying API it's using is violating its documented API contract, causing this security bug.

### mm...@chromium.org (2022-05-20)

Talked to rsesek offline, and he's of the opinion that there is indeed a bug in DataDecoder, but doesn't have the time to poke at it today.  I'll switch to using DataDecoder::ParseJSONIsolated (with a weak pointer) in the meantime, as DataDecoder objects with WeakPtrs aren't particularly useful.

### mm...@chromium.org (2022-05-20)

[+adetaylor, +morlovich]

### gi...@appspot.gserviceaccount.com (2022-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/752bfaf78c826c766b445fb0c8f524f7bdbdb07b

commit 752bfaf78c826c766b445fb0c8f524f7bdbdb07b
Author: Matt Menke <mmenke@chromium.org>
Date: Fri May 20 19:04:11 2022

[FLEDGE] Don't use DataDecoder objects.

Instead use DataDecoder::ParseJSONIsolated, which doesn't use an object.
DataDecoder appears to be broken, in that is can invoke callbacks passed
to it after it is destroyed, which violates its API contract.

InterestGroupPermissionsChecker doesn't actually need it. I had been
thinking we'd make operations individually cancellable, to better handle
having too many headless requests on navigate away, which is why I was
using it in the first place. However, I decided a simpler approach
would work well enough, so ParseJSONIsolated with a weak pointer works
just as well, and possibly with lower overhead.

Bug: 1327312
Change-Id: Ie0c22c214e7a818b21c1faae4ae7dbcb47721a27
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3653090
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1005899}

[modify] https://crrev.com/752bfaf78c826c766b445fb0c8f524f7bdbdb07b/content/browser/interest_group/interest_group_permissions_checker.h
[modify] https://crrev.com/752bfaf78c826c766b445fb0c8f524f7bdbdb07b/content/browser/interest_group/interest_group_permissions_checker.cc


### mm...@chromium.org (2022-05-20)

Note:  I'm not comfortable marking this as fixed, and subjecting it to the auto-make-public logic until the underlying bugs in DataDecoder have been addressed.

### ke...@chromium.org (2022-05-20)

Thanks for looking into this.

Re: "It's not currently enabled on stable." -> Do you just mean it hasn't rolled into a channel yet or is it flag guarded?

### mm...@chromium.org (2022-05-20)

It's behind a feature that isn't enabled on stable.  The code isn't on stable, either, for that matter, though it is in M103.

### ad...@chromium.org (2022-05-20)

Based on https://crbug.com/chromium/1327312#c13, this particular call site might be unreachable on stable so this might be Security_Impact-None. However, DataDecoder::ParseJSON has 13 call sites so there's a reasonable chance that this is reachable some other way, so we should probably regard it as impactful until proven otherwise. WDYT, kenrb?

If we consider that the data decoder service is the root of the problem here, this hasn't change for a while, so flipping to FoundIn-100 and removing ReleaseBlock-Stable (which was added because this was labelled as a regression).

### mm...@chromium.org (2022-05-20)

Going to go ahead and ask for an M103 merge of https://chromium-review.googlesource.com/c/chromium/src/+/3653090.  I'm not sure about the exact timeframe we plan on enabling the base::Feature gating this as part of an experiment, but would rather avoid any issues.

### ke...@chromium.org (2022-05-20)

adetaylor@: All other call sites use weak pointers, though, so don't they become null dereferences?

### ke...@chromium.org (2022-05-20)

Also this would affect ParseXml callers, who similarly seem to all have weak pointers used for their callbacks.

### mm...@chromium.org (2022-05-20)

Do all use weak pointers?

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/device_trust/device_trust_service.cc;l=84;drc=a08a4e1c3f6862b3b1385b8a040a4fdb524e509d;bpv=1;bpt=1?q=datadecoder::parsejson&ss=chromium
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/providers/cast/chrome_cast_message_handler.cc;drc=a08a4e1c3f6862b3b1385b8a040a4fdb524e509d;bpv=1;bpt=1;l=28?q=datadecoder::parsejson&ss=chromium
https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/declarative_net_request/file_backed_ruleset_source.cc;l=396;drc=a08a4e1c3f6862b3b1385b8a040a4fdb524e509d;bpv=1;bpt=1?q=datadecoder::parsejson&ss=chromium

The first two use a couple layers of callbacks, and I didn't dig, but don't think it's immediately obvious that they do use them.

### ke...@chromium.org (2022-05-20)

The first two do use WeakPtrs, but you're right, I had missed the third one which uses |this|.

That does mean there is possible security exposure on stable then, so the current flags are (conservatively) correct.

### et...@gmail.com (2022-05-21)

re https://crbug.com/chromium/1327312#c17
hi, mmenke, Thank you for the wonderful job of finding the root cause of this vulnerability. :)
Also, I would like to ask, will the refactoring of DataDecode also be resolved in this issue, or will you open another issue?

### et...@gmail.com (2022-05-21)

re https://crbug.com/chromium/1327312#c20
hi, adetaylor, since this issue seems to be considered underlying API design issue, it is marked as stable.
Can I get a cve and bug bounty after it's fixed?, thanks :)

### [Deleted User] (2022-05-21)

Merge approved: your change passed merge requirements and is auto-approved for M103. Please go ahead and merge the CL to branch 5060 (refs/branch-heads/5060) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2022-05-23)

deleted

### gi...@appspot.gserviceaccount.com (2022-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8c1ac7175745f8ab10550b6bb44a8aebe346b573

commit 8c1ac7175745f8ab10550b6bb44a8aebe346b573
Author: Matt Menke <mmenke@chromium.org>
Date: Mon May 23 16:56:50 2022

Merge: [FLEDGE] Don't use DataDecoder objects.

Instead use DataDecoder::ParseJSONIsolated, which doesn't use an object.
DataDecoder appears to be broken, in that is can invoke callbacks passed
to it after it is destroyed, which violates its API contract.

InterestGroupPermissionsChecker doesn't actually need it. I had been
thinking we'd make operations individually cancellable, to better handle
having too many headless requests on navigate away, which is why I was
using it in the first place. However, I decided a simpler approach
would work well enough, so ParseJSONIsolated with a weak pointer works
just as well, and possibly with lower overhead.

(cherry picked from commit 752bfaf78c826c766b445fb0c8f524f7bdbdb07b)

Bug: 1327312
Change-Id: Ie0c22c214e7a818b21c1faae4ae7dbcb47721a27
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3653090
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1005899}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3660902
Auto-Submit: Matt Menke <mmenke@chromium.org>
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#184}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/8c1ac7175745f8ab10550b6bb44a8aebe346b573/content/browser/interest_group/interest_group_permissions_checker.h
[modify] https://crrev.com/8c1ac7175745f8ab10550b6bb44a8aebe346b573/content/browser/interest_group/interest_group_permissions_checker.cc


### rs...@chromium.org (2022-05-23)

We’ll re-use this bug for the DataDecoder fix.

A CVE will be assigned and reward assessed later in the process.

### rs...@chromium.org (2022-05-23)

https://chromium-review.googlesource.com/c/chromium/src/+/3660173

### gi...@appspot.gserviceaccount.com (2022-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/31db673339b79447daab14281e76140a02a6b297

commit 31db673339b79447daab14281e76140a02a6b297
Author: Robert Sesek <rsesek@chromium.org>
Date: Thu May 26 20:43:26 2022

DataDecoder: Implement callback lifetime guarantees as documented.

The DataDecoder instance-based API says that callbacks "will only be
called if the parsing operation succeeds or fails before this
DataDecoder is destroyed." However, this is not what the implementation
currently does: nothing binds the lifetime of the DataDecoder instance
to the callback. That makes it potentially unsafe to store an instance
of a DataDecoder as a member variable and then bind Unretained
`this` pointers to the DataDecoder callbacks.

This change adds a cancellation flag to DataDecoder requests so that the
API guarantees are fulfilled.

Bug: 1327312
Change-Id: Ic973cb62c802c8f6fceb2d3fe4c826579cd6b0c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3660173
Commit-Queue: Nasko Oskov <nasko@chromium.org>
Auto-Submit: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1007974}

[modify] https://crrev.com/31db673339b79447daab14281e76140a02a6b297/services/data_decoder/public/cpp/data_decoder.cc
[modify] https://crrev.com/31db673339b79447daab14281e76140a02a6b297/services/data_decoder/public/cpp/data_decoder.h
[modify] https://crrev.com/31db673339b79447daab14281e76140a02a6b297/content/browser/data_decoder_browsertest.cc


### rs...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2022-05-27)

[rsesek] Should we add the "reward-topanel" label?

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-30)

Flag not enabled in M96

### [Deleted User] (2022-05-30)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-31)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### mm...@chromium.org (2022-06-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-01)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. While this issue does require an extension and a compromised renderer to exploit, your report, analysis, and POCs made clear the limitations of this bug and how it could be exploited. We appreciate the additional analysis you provided from report to fix as well providing the information as to where this fix was introduced. Thank you for your efforts and great work! 

### et...@gmail.com (2022-06-02)

re #46:
Hi, @amyressler, thanks Chrome VRP! :)
Also, I have another bug submitted that hasn't been reviewed, can you help me see if it's a duplicate?
https://bugs.chromium.org/p/chromium/issues/detail?id=1330489

### am...@chromium.org (2022-06-02)

Hi Nan Wang and Guang Gong, thanks again for your awesome report and great work! 

>>>Also, I have another bug submitted that hasn't been reviewed, can you help me see if it's a duplicate?
https://bugs.chromium.org/p/chromium/issues/detail?id=1330489

Looks like that one was marked as a Type=Bug rather than a security bug, I've updated it as a security bug so it will now be in our queue. 
I'll look at it tomorrow for triage and try to confirm if it is a dupe as long as one of the other sheriffs does not beat me to it. :) 

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-06-20)

[Comment Deleted]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

Commit that introduced the issue (https://crbug.com/chromium/1327312#c3) landed on 103

### [Deleted User] (2022-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1327312?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059705)*
