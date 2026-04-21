# Security: TFC 2021 loader bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40057640](https://issues.chromium.org/issues/40057640) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2021-10-18 |
| **Bounty** | $10,000.00 |

## Description

The renderer rce bug from https://crbug.com/chromium/1260579

In function `ResourceLoader::CodeCacheRequest::MaybeSendCachedCode`, two timestamps (`cached_code_response_time_` and `resource_response_time_`) need to be equal to identify that the response for cached code data is the same with the response fetched by the resource loader [1].

void ResourceLoader::CodeCacheRequest::MaybeSendCachedCode(
    mojo_base::BigBuffer data,
    ResourceLoader* resource_loader) {
  // skip
  } else {
    // If the timestamps don't match or are null, the code cache data may be for
    // a different response. See https://crbug.com/1099587.
    if (cached_code_response_time_.is_null() ||
        resource_response_time_.is_null() ||
        resource_response_time_ != cached_code_response_time_) {
      ClearCachedCodeIfPresent();
      return;
    }
  }

  if (data.size() > 0) {
    resource_loader->SendCachedCodeToResource(std::move(data));
  }
}

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_loader.cc;l=419;drc=8bfdd22de56d672bb392980ad793b4da6cefe09f

With service worker, it is possible to have the same response time for different requests, which may cause type confusion in wasm streaming compile with code cache. Considering the following scenario:

1. The web page registers two service workers of different scope.
2. Two service workers produce Response at the same time but with different bodies, for the same fetch URL. For example:
```
function createResponse(start_time){
  var count = 5;
  var step = 300;
  var time = start_time + step;
  var arr = new Array(count);
  for(var i = 0; i < count; i++){
    while(true){
      if(Date.now() >= time){
        arr[i] = new Response(body, init);
        time += step;
        break;
      }
    }
  }
  return arr[count - 3];
}
```
3. Compile these two Response one after the other by calling compileStreaming API.

When compiling the seconde Response, it would hit the wasm code cache generated for the first Response, thus type confusion occurs.

Untagged WebAssembly global values are stored in a ArrayBuffer. The bounds check of accessing a global value is done at compile phase. As such, we can cause OOB access on partition heap by leveraging the type confusion bug and then achieves RCE.

Steps to reproduce:
1. Unzip the attached file render.zip to a dir
2. Setup a Http server
node ./server.js
3. Run chrome to visit test.html
./chrome http://localhost:8000/test.html

The render process would crash due to detecting the freelist corruption.



## Attachments

- [render.zip](attachments/render.zip) (application/octet-stream, 31.1 KB)
- [trace_earth_hash.json.gz](attachments/trace_earth_hash.json.gz) (application/octet-stream, 2.3 MB)
- [trace_earth_nohash.json.gz](attachments/trace_earth_nohash.json.gz) (application/octet-stream, 2.1 MB)
- [trace_adobe2.json.gz](attachments/trace_adobe2.json.gz) (application/octet-stream, 4.3 MB)

## Timeline

### ad...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2021-10-18)

Credit for bug to: "漏洞研究院青训队 via Tianfu Cup"

### ad...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2021-10-18)

I can't reproduce this on redshell with asan-linux-debug 911515. I will try some other builds.

### ad...@google.com (2021-10-18)

I also can't reproduce this with asan-linux-release-929491.

The PoC reports:
Info - ====== round 4 ======
Error - checkMessage : expected {success , undefined}, got {error , CompileError: WebAssembly.compileStreaming(): Compiling function #5:"get_2" failed: Invalid global index: 2 @+46066}

jtrrodant@gmail.com please can you let us know a specific chromium build number where this works? Linux if at all possible. Thanks!

### ad...@google.com (2021-10-18)

yhirano@ this was a competition entry at Tianfu Cup over the weekend. I can't reproduce it, but if you're able to confirm it's a real bug that would be great. If so, please confirm it affects back to M94.

### jt...@gmail.com (2021-10-19)

adetaylor@,

After further research, I found that the following CL [1] accidentally blocked the poc, in which it deletes some lines in function `ShouldUseIsolatedCodeCache`. Before that, response with 'application/wasm' mime type would always use isolated code cache. However, this won't work after the CL applied.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3199655

So the poc should work on version before this CL. And this doesn't mean that the bug has been fixed because there may exist another way to generate responses with different body and same timestamp, e.g. the web server respond two requests with high-precision time synchronization.


### yh...@chromium.org (2021-10-19)

cc: mythria@chromium.org

### es...@chromium.org (2021-10-20)

yhirano, mythria could you take a look and see if you can reproduce with https://chromium-review.googlesource.com/c/chromium/src/+/3199655 reverted?

### yh...@chromium.org (2021-10-20)

leszeks@, do you know anyone who is familiar with the code cache? It seems mythria@ left the team.

### ad...@google.com (2021-10-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-10-20)

Doing some source code archaeology, this appears to be a duplicate of https://crbug.com/chromium/1099587, though that's not marked as a security bug. I'll mark it as such in case I'm right.

### yh...@chromium.org (2021-10-20)

Can you cc us (people cc-ed in this bug) in the bug?

### ad...@google.com (2021-10-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-10-20)

mmenke@, morlovich@ - the risks of the current approach were discussed in a comment thread involving you all here back in 2018 - https://docs.google.com/document/d/1O_PVZPn37Ev3_DWJjQLX-gid__OKxnXP1UsE8g_YkRY/edit?disco=AAAAB55fWZk. I wonder if you might be able to dredge off those neurons and suggest a quick workaround/fix which we might be able to land this week. Presumably it will take somewhat longer to do the full fix of avoiding using timestamps.

### ad...@google.com (2021-10-20)

yhirano@ - re https://crbug.com/chromium/1260939#c13 done. Thanks for taking a look.

### mm...@chromium.org (2021-10-20)

So this is a renderer-only cache that only has access to the output of the ServiceWorker?  What output does the ServiceWorker actually provide that carry over from the real response?  Unless there's access to real output from net/, seems like this depends much more on output from the SW layer than from the net/ layer.

### le...@chromium.org (2021-10-20)

FWIW, I'm taking over JS code cache from mythria@, but WASM code cache is I guess wanderview@

### va...@google.com (2021-10-20)

[Empty comment from Monorail migration]

### ec...@chromium.org (2021-10-20)

@clemensb: PTAL as discussed, thanks!

### cl...@chromium.org (2021-10-20)

It looks like the immediate attack vector is blocked by https://crrev.com/c/3199655, which is in M96 and M95 (M95 is just rolling out to stable).
The underlying issue (using timestamp as a unique identifier) should be fixed on Chromium side, but that's out of my expertise.

On the V8 side, we could protect against misbehaving embedders (providing mismatched cache entries) by including a hash of the wire bytes in the serialized format, and verifying that on deserialization. Computing that hash might introduce a little overhead though.

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-10-20)

I agree that crrev.com/c/3199655 has blocked the POC because the code no longer uses code cache for "synthetic responses" created with `new Response()`.  This was done because these types of responses will never result in useful caching because they don't have a backing cache, always get a new timestamp, etc.

I think, however, this protection is easily defeated.  The POC can be changed to store the responses in cache_storage under some other request url.  Then they can move these responses in cache_storage to the correct request url when they want to execute their attack.  Since we freeze the response time at the time of response creation I think they could accomplish the same attack.

There is also a risk from a service worker that does a "passthrough" with something like `evt.respondWith(fetch(some_request))`.  I believe its theoretically possible to get two different network responses to have have the same time stamp.  Particularly if you have server cooperation.  In addition, the requests can have headers to tell the server to change the body, etc.  These could be returned directly from the service worker or laundered through cache_storage again to make the timing easier.

I agree the best long term solution is to implement real cache keys instead of using the response timestamps.  Also, wasm code caching should probably not create or consume code cache if a response comes from the server directly without hitting some kind of cache (http cache or cache_storage).

Does normal js code caching not have this problem?  How does it prevent the attack?

Note, I'm currently working two other P1 security bugs, so I don't have bandwidth to take this on myself right now.  Happy to help advise, however.

### le...@chromium.org (2021-10-20)

I'd have to take a closer look to check whether this can affect JS caching, but JS caches do include a checksum with a hash of the source (though it's not a crypto-safe hash).

### [Deleted User] (2021-10-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@chromium.org (2021-10-21)

Ah, so I think this is not an issue for JS because we don't have any safety/bounds checks at compile time that rely on compilation results matching source. If we get a source/compilation mismatch, it's a correctness issue, but not a security one, the generated bytecode is still safe and becomes the source of truth for any subsequent operations (beyond lazy compilation, which will likely either just fail or if brackets happen to line up accidentally succeed with similarly safe bytecode generated).

### cl...@chromium.org (2021-10-21)

So who would be a good owner of this bug?

On the V8 side, we could mitigate the attack by including a hash of the Wasm wire bytes in the serialized data, but that would require including a cryptographically strong hash implementation in V8, which we currently don't have. So it's questionable if that complexity, binary size, and performance regression for serialization/deserialization is worth it, given that it's only needed to protect misidentified cache results.

Is it feasible to fix this on the caching side, and merge back the fix(es)?

### wa...@chromium.org (2021-10-21)

Adding cache keys instead of using response time is largely a plumbing exercise through the loading stack.  At a minimum we need the cache keys in cache_storage, but it would be good to have a uniform solution that also uses cache keys in isolated code cache.

Since this hits the loading stack and relates to service workers, maybe the loading team could take this on?  Kouhei, what do you think?

### ko...@chromium.org (2021-10-21)

> c#28

I just talked to yhirano.
The long term fix of plumbing cache keys - coincidentally, yhirano@'s team is planning to implement this for a different project, so his team can own this.
I don't have a good idea of what short term fix would look like. Given that this only affects WASM, would it be an option to temporarily disable wasm code cache just to stop bleeding?

### yh...@chromium.org (2021-10-21)

cc-ing adamk@ for WASM and code cache.

### wa...@chromium.org (2021-10-21)

> The long term fix of plumbing cache keys - coincidentally, yhirano@'s team is planning to implement this for a different project, so his team can own this.

That's great!  Thanks.

> would it be an option to temporarily disable wasm code cache

Unfortunately wasm code caching is pretty important for a large partner.  I think we need to avoid that if at all possible.

Would a short term fix using a non-crpyptographic hash in the wasm compiler be possible?

Another possible short term fix would be to change cache_storage to always update the response time to the current time when storing a response.  This would probably prevent the attack in https://crbug.com/chromium/1260939#c23.  The attacker would need to store in cache_storage, serve the wasm to the page, wait for code cache to be populated, then change response in the cache to a different body all within resolution of the response time (on the order of microseconds).

We would also need the changes to require either http cache or cache_storage in order to produce/consume code cache.

Is there someone who can own doing that work?  Again, I'm already working two pri1 security bugs, so don't have the bandwidth at the moment.

### ko...@chromium.org (2021-10-25)

+hiroshige: Would you be interested in exploring the short term fix?

### yh...@chromium.org (2021-10-26)

I see two possibilities for the long term solution.

1) Put an unguessable token for every response.
2) Put a content hash for every response.

1) is easier to implement and easier to calculate. On the other hand, we're planning to introduce 2) for another project, and assuming that we'll get 2) for free.
Hence I'm not sure which is better.

### ad...@google.com (2021-10-26)

yhirano@ please would you mark this bug or https://crbug.com/chromium/1099587 as a duplicate of the other one? Assuming they really are duplicates.

(Ideally, this one would be marked as the duplicate because it's newer, but as it's got more useful information it's OK to do it the other way round).

### wa...@chromium.org (2021-10-26)

Are we willing to delay fixing this until the other project is completed?  My impression was that had a longer time frame than we wanted here.  Just checking before we mark it as a dupe.

### ad...@google.com (2021-10-26)

Ah OK. If this bug will be used to track a short-term fix, and https://crbug.com/chromium/1099587 to track a longer-term solution, that sounds like a great reason to keep them separate. It looked to me like they were plain old duplicates.

### ad...@google.com (2021-11-01)

wanderview@ - note there's a possible bypass for this fix in https://crbug.com/chromium/1264866.

### wa...@chromium.org (2021-11-01)

Yes.  AIUI https://crbug.com/chromium/1264866 is implementing my suggested attack in https://crbug.com/chromium/1260939#c31.

This does make it easier to implement a fix, though, as we can verify it stops the new PoC.  I'll see if my idea fixes that.

### va...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### hi...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-11-08)

Unfortunately I don't think we can do the short term fix in https://crbug.com/chromium/1260939#c31.  I realized if we change the response.time we will break another security mechanism based on it.  We use response time to compute the opaque response padding in order to protect cross-origin resource size.  If we change response.time on every insertion into cache_storage it would allow an attacker to average out the opaque response padding.

So we need another short term solution.  I don't currently have any ideas, though.

### wa...@chromium.org (2021-11-08)

We might be able to plumb cache_storage "entry time" through all the response types and use it instead of response time, though.  That would leave response time untouched and working for opaque responses.

### hi...@chromium.org (2021-11-08)

Candidates for short-term fixes so far are:

(1) Check the cache matching in V8 WASM compiler side by calculating hashes (https://crbug.com/chromium/1260939#c21 and https://crbug.com/chromium/1260939#c27). Simplest, but is the hash calculation overhead acceptable given that WASM compilation is very fast?
(2) Plumb entry time (+ random bits) down to blink::ResourceResponse (https://crbug.com/chromium/1260939#c44).
(3) Disable wasm code cache (we want to avoid this according to https://crbug.com/chromium/1260939#c31).

(Preparing a design doc https://docs.google.com/document/d/15nP1OmCpcIlxLdqHpLttFJf2N87kaPi1q8T7QqpfSTI/edit?usp=sharing )

### ah...@chromium.org (2021-11-09)

I think (1) could actually be okay. At the moment V8 receives the cached module it still waits for the binary wasm module to arrive (which comes either from the network, or from the (I think) resource cache. During that time we could calculate the hash in the background.

About the hashing algorithm, maybe the embedder could provide it, over the V8 platform API.

### cl...@chromium.org (2021-11-10)

Wouldn't the hash be computed from the wire bytes, and compared against a hash contained in the cache entry? We would still need to wait for the wire bytes before computing the hash then. Even if we compute it incrementally, it would still happen in the foreground currently (where we receive the wire byte chunks).
Maybe it could fully be implemented in the embedder, by checking the hash and then stripping it from the cache entry before passing it to V8. There should be a point where the both the cache entry and the wire bytes are there, but it will probably require changes to the API. 
Does Chrome have a cryptographically secure (unforgeable) hashing algorithm that would be sufficiently fast? 

### ah...@chromium.org (2021-11-10)

I thought of it the following way: While V8 is receiving the wire bytes, it is calculating the hash instead of doing Liftoff compilation. I assume here that the hashing algorithm is incremental and at least as fast as Liftoff. If that's the case, then the hash should be completed once the download is completed. The hash can then be passed to the deserialization and be compared with the hash that is stored in the serialized module. If the hash does not match (unlikely), the module gets compiled with Liftoff instead. This bailout already exists and is used when the serialized module is corrupted, e.g. if bytes are missing.

If the hash computation is fast, then we could do it on the main thread. At least for AutoCAD and Photoshop the main thread does not seem too busy while we receive the wire bytes. If hash computation on the main thread causes problems, we could also move it to a background thread.

The hash could get computed incrementally on the Chrome side and then sent to V8, e.g. as a parameter to the `FinishStream` API function. This would allow a cleaner V8 API, because the hashing algorithm does not have to be provided to V8. Other than that I don't think there is much of a difference.

### wa...@chromium.org (2021-11-10)

You would also need to do this when generating the code cache the first time, right?  So you can incorporate the hash in the generated code cache?

### ah...@chromium.org (2021-11-10)

Yes, we would also need to calculate the hash when generating the code cache the first time. But I think this is not performance critical.

### cl...@chromium.org (2021-11-10)

We should really measure how fast the hash computation is. In the end, we would be patching over a bug in the cache implementation, and we pay in V8 in terms of maintainability (code complexity) and performance.

I would still prefer to fix the underlying problem in the caching infrastructure to avoid introducing (temporary?) mitigations in V8. 

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### hi...@chromium.org (2021-11-15)

Drafting a CL: https://chromium-review.googlesource.com/c/chromium/src/+/3282643
This aligns with (1) of https://crbug.com/chromium/1260939#c45 and https://crbug.com/chromium/1260939#c48.
The hash (currently using SHA-256) is calculated in a streaming fashion on the main thread while receiving the wire bytes, and is stored in the first 32 bytes of CachedMetadata. (Still needs to be refined, and V8 side API should be modified)

As for performance, is there any performance tests/benchmarks that we should try before landing?

### ah...@chromium.org (2021-11-16)

It would be good to measure the time it takes to calculate the hash in total, e.g. by adding trace events and looking at the resulting traces. It would also be interesting how much overhead it creates with the additions in the `BytesConsumer::Result::kDone`, also with a trace. As an example you can use earth.google.com.

### hi...@chromium.org (2021-11-22)

Performance measurement of the draft CL
(https://chromium-review.googlesource.com/c/chromium/src/+/3282643
patch set 8, streaming SHA-256 calculation) on my laptop (Dell 5520, Linux):

I measured the performance of instantiating
`third_party/blink/web_tests/http/tests/wasm/resources/large.wasm`
(131KB, see third_party/blink/web_tests/http/tests/wasm-test.html in the CL):

$ ./third_party/blink/tools/run_blink_httpd.py 

One iteration =
WebAssembly.instantiateStreaming(fetch(
  'http://127.0.0.1:8000/wasm/resources/load-wasm.php?name=large.wasm&cors'))

(Quoted names are the titles in the tracing)

[1] Run on clean profile (no cache):
    full compilation at `wasm.CompileBaseline`: ~18ms.
    => Code cache is generated and stored.

[2] Close the browser and run again (hits V8 Code Cache but not isolate code cache inside V8):
    Deserializing V8 code cache at `wasm.Deserialize`: ~1.3ms

[3] Run repeatedly (hits isolate code cache inside V8):
    - Total execution time of FetchDataLoaderForWasmStreaming::OnStateChange() (`v8.wasm.compileConsume`): ~0.82ms
      - Hash calculation (`v8.wasm.compileDigestForConsume`): ~0.35ms
      - kDone case (`v8.wasm.compileConsumeDone`): ~0.33ms
    - Total execution time of one iteration (including fetch + instantiateStreaming):
      - Without hash validation: ~4.5ms
      - With SHA-256 hash validation: ~4.8ms

So the hash calculation cost is ~0.35ms per 131KB wire bytes,
which slows down the case [3] a little,
but still much faster than deserialization (~1.3ms) or full compilation (~18ms).
(am I understanding the traces correctly?)

Is this performance acceptable?


### ah...@chromium.org (2021-11-22)

Could you measure with bigger wasm modules? earth.google.com would be good, and Photoshop (https://photoshop.adobe.com/id/urn:aaid:sc:US:11b9b1b9-71a5-45bf-a1b1-eedb77b70873?timing_marks=true). Could you attach the trace?

### hi...@chromium.org (2021-11-22)

> earth.google.com

`wasm.Deserialize` was ~500ms and hash calc (`v8.wasm.compileDigestForConsume`) was ~65ms for the scenario [2]:
> [2] Close the browser and run again (hits V8 Code Cache but not isolate code cache inside V8):

Attached traces with my CL, with hash validation on and off.

(So far I couldn't take traces with all tracing categories enabled or for Photoshop due to crashes and OOMs unrelated to my CL. The traces here enabled only v8.wasm.*, some v8.* and devtools.timeline categories.)

### ah...@chromium.org (2021-11-22)

Hmm, the overhead compared to onBytesReceived is quite significant, each chunk of bytes now takes 3 times as long. Then again, at least for Google Earth this is not the most busy time during startup, and the duration of streaming from start to finish only changes by 2ms. I think this solution is okay for now.

### hi...@chromium.org (2021-11-23)

Thank you for feedback! Then I'm going to land CLs based on this approach. Preparing codereviews:

1. V8 CL https://chromium-review.googlesource.com/c/v8/v8/+/3297548
2. Chromium CL https://chromium-review.googlesource.com/c/chromium/src/+/3282643

### hi...@chromium.org (2021-11-23)

Adobe Photoshop trace:

Setting `is_official_build = true` in `args.gn` prevented crashes (I'm not sure why; maybe PGO?).

Trace of Patch set 15 of https://chromium-review.googlesource.com/c/chromium/src/+/3282643/ with hash validation on:

`wasm.Deserialize` was ~290ms and hash calc (`v8.wasm.compileDigestForConsume`) was ~190ms for the scenario [2]:
> [2] Close the browser and run again (hits V8 Code Cache but not isolate code cache inside V8)

### gi...@appspot.gserviceaccount.com (2021-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b0c6dd86bd563672dba6256f482dc5e145f094ae

commit b0c6dd86bd563672dba6256f482dc5e145f094ae
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Tue Nov 23 13:32:18 2021

Allow compiled module invalidation at WasmStreaming::Finish()

This CL adds `can_use_compiled_module` parameter to
WasmStreaming::Finish() that is used by Chromium
https://chromium-review.googlesource.com/c/chromium/src/+/3282643
to invalidate compiled module bytes after SetCompiledModuleBytes().

Bug: chromium:1260939
Change-Id: Iebf0e8615c27c8622721777c664b06a53fb9ee91
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3297548
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/heads/main@{#78044}

[modify] https://crrev.com/b0c6dd86bd563672dba6256f482dc5e145f094ae/src/wasm/streaming-decoder.cc
[modify] https://crrev.com/b0c6dd86bd563672dba6256f482dc5e145f094ae/src/wasm/sync-streaming-decoder.cc
[modify] https://crrev.com/b0c6dd86bd563672dba6256f482dc5e145f094ae/include/v8-wasm.h
[modify] https://crrev.com/b0c6dd86bd563672dba6256f482dc5e145f094ae/src/wasm/streaming-decoder.h
[modify] https://crrev.com/b0c6dd86bd563672dba6256f482dc5e145f094ae/src/api/api.cc
[modify] https://crrev.com/b0c6dd86bd563672dba6256f482dc5e145f094ae/src/wasm/wasm-js.cc


### ko...@chromium.org (2021-11-24)

Thank you hiroshige and ahaas for investigating the performance issue.
I think we should proceed with hiroshige@ mitigation anyways even if that presents a performance regression, given the priority of this bug (P1).

### gi...@appspot.gserviceaccount.com (2021-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7077e03a4e02c198ac9fdb0814d195df7a75c229

commit 7077e03a4e02c198ac9fdb0814d195df7a75c229
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Wed Nov 24 07:16:06 2021

Store SHA-256 hash of wire bytes for WASM V8 Code Cache

This CL stores and validates SHA-256 hash of wire bytes
in WASM V8 Code Cache to prevent mismatches between
wire bytes and code cache metadata.

When hitting code cache, this CL calculates the hash
while streaming wire bytes, and
invalidates the code cache metadata on hash mismatch,
by setting `can_use_compiled_module` to `false`
in `WasmStreaming::Finish()`.

The cached metadata is passed to V8 by
`SetCompiledModuleBytes()` when the first bytes of
the wire bytes are received, but this only triggers
suppressiong of streaming compilation and the
content of the cached metadata is not used until
`WasmStreaming::Finish(true)` is called later.

This CL also adds tracing events to measure hashing overhead
and observe cache rejection by hash mismatch.

This CL depends on V8 side CL:
https://chromium-review.googlesource.com/c/v8/v8/+/3297548

Bug: 1260939
Change-Id: Ie7ee41c50e911fcf4cb2bdec9d1501b3e84e6d8f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3282643
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/heads/main@{#944867}

[modify] https://crrev.com/7077e03a4e02c198ac9fdb0814d195df7a75c229/third_party/blink/renderer/platform/loader/fetch/cached_metadata.h
[modify] https://crrev.com/7077e03a4e02c198ac9fdb0814d195df7a75c229/third_party/blink/renderer/bindings/core/v8/v8_wasm_response_extensions.cc
[modify] https://crrev.com/7077e03a4e02c198ac9fdb0814d195df7a75c229/third_party/blink/renderer/platform/loader/fetch/cached_metadata.cc


### hi...@chromium.org (2021-11-26)

The fix landed on 98.0.4727.0 and is available on the canary channels.

### hi...@chromium.org (2021-11-29)

Should we merge the fix to M-97 or earlier?

### ad...@google.com (2021-11-29)

Please mark it as Fixed, and then Sheriffbot will take care of the right merges. (It's nowadays normal practice to mark things as Fixed before requesting merges - see for instance https://groups.google.com/a/google.com/g/chromium-dev-internal/c/DTw4amOzLYk/m/lvuCRtwyAwAJ or https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels)

### hi...@chromium.org (2021-11-29)

I see. Marking as Fixed. I tested that at least the CLs fixed the test case at https://crbug.com/chromium/1264866, but feel free to reopen if 98.0.4727.0 or later is still failing.

### ad...@google.com (2021-11-29)

Thanks! Sheriffbot should request the relevant merges in a couple of hours. It will add a questionnaire which has various questions. The most important thing is - do you consider this risky (from a stability/compatibility point of view)? It sounds like the major risk is of performance regressions, but that the slowdowns are not so huge that we expect users to notice?

### ad...@google.com (2021-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-29)

Requesting merge to stable M96 because latest trunk commit (944867) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (944867) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-29)

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

### [Deleted User] (2021-11-29)

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

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### hi...@chromium.org (2021-11-30)

1. Why does your merge fit within the merge criteria for these milestones?
For M-97: "any security issues"
For M-96: security issues with an external reporter and high severity. Regression at M-94. 

Risks:
- The V8 side CL [A] is quite safe, because the changes are small & mostly straightforward plumbing, and it doesn't change the behavior without the Chromium side CL [B].
- The Chromium side CL [B] has medium-sized changes while it should affect the behavior and performance only around WASM compilation.
  Low compatibility risks because the functional behavior is changed only if there are mismatches between WASM wire bytes and V8 code cache (rare & with no valid use cases).
  A major concern was performance regressions, but probably the slowdowns are small/acceptable (Comments 55-58, no regression bugs assigned to me so far), and kouhei said that the fixes should land on ToT even with performance regressions if any (https://crbug.com/chromium/1260939#c62).

2. What changes specifically would you like to merge? Please link to Gerrit.

[A] https://chromium-review.googlesource.com/c/v8/v8/+/3297548
[B] https://chromium-review.googlesource.com/c/chromium/src/+/3282643

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

The test case posted at https://crbug.com/chromium/1264866 might be helpful for verification, as the affected code paths seem to lack automated test coverage since before the fix CLs (not sure it's required though).

### am...@chromium.org (2021-11-30)

merge approved for M97, please ensure the v8 fix is merged to the appropriate branch in the V8 repo for M97
for the Chromium commit, please merge into branch 4692; please merge to M97 ASAP so these fixes can be included in today's beta cut 

### am...@chromium.org (2021-11-30)

merge approved for M97, please ensure the v8 fix is merged to the appropriate branch in the V8 repo for M97
for the Chromium commit, please merge into branch 4664; please merge these fixes to m96 by EOD Friday, 3 December so these fixes can be included in next week's stable respin 

### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/417dee4d1b0f967e3cac360a0b012decbc9f6908

commit 417dee4d1b0f967e3cac360a0b012decbc9f6908
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Tue Nov 23 13:32:18 2021

Merged: Allow compiled module invalidation at WasmStreaming::Finish()

This CL adds `can_use_compiled_module` parameter to
WasmStreaming::Finish() that is used by Chromium
https://chromium-review.googlesource.com/c/chromium/src/+/3282643
to invalidate compiled module bytes after SetCompiledModuleBytes().

(cherry picked from commit b0c6dd86bd563672dba6256f482dc5e145f094ae)

Bug: chromium:1260939
Change-Id: I462df0e25fbc693f7e7114e6bcfe2a01dc60beba
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3306787
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.7@{#28}
Cr-Branched-From: 49162da459e2ca1f078389a84f0bbfcc7fed7a2b-refs/heads/9.7.106@{#1}
Cr-Branched-From: a7e9b8f0a4637caad6fcf27be999b97f49b6ac3d-refs/heads/main@{#77674}

[modify] https://crrev.com/417dee4d1b0f967e3cac360a0b012decbc9f6908/src/wasm/streaming-decoder.cc
[modify] https://crrev.com/417dee4d1b0f967e3cac360a0b012decbc9f6908/src/wasm/sync-streaming-decoder.cc
[modify] https://crrev.com/417dee4d1b0f967e3cac360a0b012decbc9f6908/include/v8-wasm.h
[modify] https://crrev.com/417dee4d1b0f967e3cac360a0b012decbc9f6908/src/wasm/streaming-decoder.h
[modify] https://crrev.com/417dee4d1b0f967e3cac360a0b012decbc9f6908/src/api/api.cc
[modify] https://crrev.com/417dee4d1b0f967e3cac360a0b012decbc9f6908/src/wasm/wasm-js.cc


### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578

commit 04a58fedd57dbf9d96b3ed3351ddef1eea1d1578
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Tue Nov 23 13:32:18 2021

Merged: Allow compiled module invalidation at WasmStreaming::Finish()

This CL adds `can_use_compiled_module` parameter to
WasmStreaming::Finish() that is used by Chromium
https://chromium-review.googlesource.com/c/chromium/src/+/3282643
to invalidate compiled module bytes after SetCompiledModuleBytes().

(cherry picked from commit b0c6dd86bd563672dba6256f482dc5e145f094ae)

Bug: chromium:1260939
Change-Id: I28554ed79ed56349fa38517ed03785e0c8146b4d
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3306788
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.6@{#36}
Cr-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}

[modify] https://crrev.com/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578/src/wasm/streaming-decoder.cc
[modify] https://crrev.com/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578/src/wasm/sync-streaming-decoder.cc
[modify] https://crrev.com/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578/include/v8-wasm.h
[modify] https://crrev.com/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578/src/wasm/streaming-decoder.h
[modify] https://crrev.com/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578/src/api/api.cc
[modify] https://crrev.com/04a58fedd57dbf9d96b3ed3351ddef1eea1d1578/src/wasm/wasm-js.cc


### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b991003092e22cc46b93a78127f802e09f7962fa

commit b991003092e22cc46b93a78127f802e09f7962fa
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Thu Dec 02 15:23:47 2021

Store SHA-256 hash of wire bytes for WASM V8 Code Cache

This CL stores and validates SHA-256 hash of wire bytes
in WASM V8 Code Cache to prevent mismatches between
wire bytes and code cache metadata.

When hitting code cache, this CL calculates the hash
while streaming wire bytes, and
invalidates the code cache metadata on hash mismatch,
by setting `can_use_compiled_module` to `false`
in `WasmStreaming::Finish()`.

The cached metadata is passed to V8 by
`SetCompiledModuleBytes()` when the first bytes of
the wire bytes are received, but this only triggers
suppressiong of streaming compilation and the
content of the cached metadata is not used until
`WasmStreaming::Finish(true)` is called later.

This CL also adds tracing events to measure hashing overhead
and observe cache rejection by hash mismatch.

This CL depends on V8 side CL:
https://chromium-review.googlesource.com/c/v8/v8/+/3297548

(cherry picked from commit 7077e03a4e02c198ac9fdb0814d195df7a75c229)

Bug: 1260939
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3282643
Cr-Original-Commit-Position: refs/heads/main@{#944867}
Change-Id: Ie7ee41c50e911fcf4cb2bdec9d1501b3e84e6d8f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3310061
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#644}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/b991003092e22cc46b93a78127f802e09f7962fa/third_party/blink/renderer/platform/loader/fetch/cached_metadata.h
[modify] https://crrev.com/b991003092e22cc46b93a78127f802e09f7962fa/third_party/blink/renderer/bindings/core/v8/v8_wasm_response_extensions.cc
[modify] https://crrev.com/b991003092e22cc46b93a78127f802e09f7962fa/third_party/blink/renderer/platform/loader/fetch/cached_metadata.cc


### sr...@google.com (2021-12-02)

merge is complete so dropping the label

### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/731871eeabb6a9c78669292a44e927c5f42b1f7d

commit 731871eeabb6a9c78669292a44e927c5f42b1f7d
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Thu Dec 02 19:23:45 2021

Store SHA-256 hash of wire bytes for WASM V8 Code Cache

This CL stores and validates SHA-256 hash of wire bytes
in WASM V8 Code Cache to prevent mismatches between
wire bytes and code cache metadata.

When hitting code cache, this CL calculates the hash
while streaming wire bytes, and
invalidates the code cache metadata on hash mismatch,
by setting `can_use_compiled_module` to `false`
in `WasmStreaming::Finish()`.

The cached metadata is passed to V8 by
`SetCompiledModuleBytes()` when the first bytes of
the wire bytes are received, but this only triggers
suppressiong of streaming compilation and the
content of the cached metadata is not used until
`WasmStreaming::Finish(true)` is called later.

This CL also adds tracing events to measure hashing overhead
and observe cache rejection by hash mismatch.

This CL depends on V8 side CL:
https://chromium-review.googlesource.com/c/v8/v8/+/3297548

(cherry picked from commit 7077e03a4e02c198ac9fdb0814d195df7a75c229)

Bug: 1260939
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3282643
Cr-Original-Commit-Position: refs/heads/main@{#944867}
No-Try: true
Change-Id: If074cbeeb7015a359566821cae544ff8f1cd3589
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3310065
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1207}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/731871eeabb6a9c78669292a44e927c5f42b1f7d/third_party/blink/renderer/platform/loader/fetch/cached_metadata.h
[modify] https://crrev.com/731871eeabb6a9c78669292a44e927c5f42b1f7d/third_party/blink/renderer/bindings/core/v8/v8_wasm_response_extensions.cc
[modify] https://crrev.com/731871eeabb6a9c78669292a44e927c5f42b1f7d/third_party/blink/renderer/platform/loader/fetch/cached_metadata.cc


### hi...@chromium.org (2021-12-02)

All CLs are merged to M-97/M-96.

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for continuing your efforts from Tian Fu Cup and reporting this issue to us. 

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260939?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1260579]
[Monorail mergedwith: crbug.com/chromium/1264866]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057640)*
