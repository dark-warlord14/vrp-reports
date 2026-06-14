# HTTP 1xx response handling code allows a website to read memory from the main process' heap.

| Field | Value |
|-------|-------|
| **Issue ID** | [40078172](https://issues.chromium.org/issues/40078172) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network |
| **Reporter** | sk...@chromium.org |
| **Assignee** | ag...@chromium.org |
| **Created** | 2013-09-27 |
| **Bounty** | $4,000.00 |

## Description

VULNERABILITY DESCRIPTION  

Through carefully crafted HTTP responses, a malicious website is able to read information from the main chrome process.

**VULNERABILITY DETAILS**  

The "HttpStreamParser" class (src\net\http\http\_stream\_parser.cc) is used to send HTTP requests and receive HTTP responses. Its "read\_buf\_" member is used to store HTTP response data received from the server. Parts of the code are written under the assumption that the response currently being parsed is always stored at the start of this buffer ("read\_buf\_->StartOfBuffer()"), other parts take into account that this may not be the case ("read\_buf\_->StartOfBuffer() + read\_buf\_unused\_offset\_"). In most cases, responses are removed from the buffer once they have been parsed and any superfluous data is moved to the beginning of the buffer, to be treated as part of the next response. However, the code special cases HTTP 1xx replies and returns a result without removing the request from the buffer. This means that the response to the next request will not be stored at the start of the buffer, but after the HTTP 1xx response.

The code that special cases HTTP 1xx responses is:  

src\net\http\http\_stream\_parser.cc:  

580 | if (end\_of\_header\_offset == -1) {  

<snip>  

587 | } else {  

588 | // Note where the headers stop.  

589 | read\_buf\_unused\_offset\_ = end\_of\_header\_offset;  

590 |  

591 | if (response\_->headers->response\_code() / 100 == 1) {  

592 | // After processing a 1xx response, the caller will ask for the next  

593 | // header, so reset state to support that. We don't just skip these  

594 | // completely because 1xx codes aren't acceptable when establishing a  

595 | // tunnel.  

596 | io\_state\_ = STATE\_REQUEST\_SENT;  

597 | response\_header\_start\_offset\_ = -1;  

The code above does not remove the HTTP 1xx response from the buffer at this point.  

598 | } else {  

The code that follows either removes the response from the buffer immediately, or expects it to be removed in a call to ReadResponseBody later.  

<snip>  

619 | return result;  

620 |}

A look through the code has revealed one location where this can lead to a security issue (also in "DoReadHeadersComplete"). The code uses an offset from the start of the buffer (rather than the start of the current responses) to pass as an argument to a "DoParseResponseHeaders".

src\net\http\http\_stream\_parser.cc:  

540 | if (result == ERR\_CONNECTION\_CLOSED) {  

<snip>  

554 | // Parse things as well as we can and let the caller decide what to do.  

555 | int end\_offset;  

556 | if (response\_header\_start\_offset\_ >= 0) {  

557 | io\_state\_ = STATE\_READ\_BODY\_COMPLETE;  

558 | end\_offset = read\_buf\_->offset();  

"end\_offset" is relative to the start of the buffer ("read\_buf\_->StartOfBuffer()").  

559 | } else {  

560 | io\_state\_ = STATE\_BODY\_PENDING;  

561 | end\_offset = 0;  

"end\_offset" is relative to the start of the current response ("read\_buf\_->StartOfBuffer() + read\_buf\_unused\_offset\_").  

562 | }  

563 | int rv = DoParseResponseHeaders(end\_offset);  

<snip>

"DoParseResponseHeaders" passes the argument unchanged to "HttpUtil::AssembleRawHeaders":  

src\net\http\http\_stream\_parser.cc:  

782 |int HttpStreamParser::DoParseResponseHeaders(int end\_offset) {  

783 | scoped\_refptr<HttpResponseHeaders> headers;  

784 | if (response\_header\_start\_offset\_ >= 0) {  

785 | headers = new HttpResponseHeaders(HttpUtil::AssembleRawHeaders(  

786 | read\_buf\_->StartOfBuffer() + read\_buf\_unused\_offset\_, end\_offset));  

<snip>

"HttpUtil::AssembleRawHeaders" takes two arguments: a pointer to a buffer, and the length of the buffer. The pointer is calculated correctly (in "DoParseResponseHeaders") and points to the start of the current response. The length is the offset that was calculated incorrectly in "DoReadHeadersComplete". If the current response is preceded by a HTTP 1xx response in the buffer, this length is larger than it should be: the calculated value will be the correct length plus the size of the previous HTTP 1xx response ("read\_buf\_unused\_offset\_").

src\net\http\http\_util.cc:  

582 |std::string HttpUtil::AssembleRawHeaders(const char\* input\_begin,  

583 | int input\_len) {  

584 | std::string raw\_headers;  

585 | raw\_headers.reserve(input\_len);  

586 |  

587 | const char\* input\_end = input\_begin + input\_len;  

"input\_begin" was calculated as ("read\_buf\_->StartOfBuffer() + read\_buf\_unused\_offset\_"), "input\_len" was incorrectly calculated as "len(headers) + read\_buf\_unused\_offset\_", so "input\_end" will be "read\_buf\_->StartOfBuffer() + 2 \* read\_buf\_unused\_offset\_ + len(headers)", which is beyond the end of the actual headers. The code will continue to rely on this incorrect value to try to create a copy of the headers, inadvertently makeing a copy of data that is not part of the response and may not even be part of the read\_buf\_ buffer. This could cause the code to copy memory immediately following "read\_buf\_" into a string that represents the response headers. This string is passed to the process that made the request, allowing a webpage inside the sandbox to read memory from the main process' heap.

An ascii diagram might be useful to illustrate what is going on:

read\_buf\_: "HTTP 100 Continue\r\n...HTTP XXX Current response\r\n...Unused..."  

read\_buf\_->StartOfBuffer() -----^  

read\_buf\_->capacity() ----------[================================================================]  

read\_buf\_->offset() ------------[=======================================================]  

read\_buf\_unused\_offset\_ -------[=======================]

DoReadHeadersComplete/DoParseResponseHeaders:  

end\_offset ---------------------[=======================================================]

AssembleRawHeaders:  

input\_begin ---------------------------------------------^  

input\_len ----------------------------------------------[========================================###############]  

error in input\_len value --------------------------------------------------------------[========###############]  

(== read\_buf\_unused\_offset\_)  

Memory read from the main process' heap ---------------------------------------------------------[##############]

**VERSION**  

Since the affected code has not been changed since 2009, I assume this affects all versions of Chrome released in the last few years

**REPRODUCTION CASE**  

Attached is a simple proof-of-concept; it consist of a server that hosts a simple webpage. The webpage uses XMLHttpRequest to make requests to the server. The server responds with a carefully crafted reply to exploit the vulnerability. The webpage then uses getAllResponseHeaders() to read the memory copied from the main process' heap, and posts it to the server, which displays the memory. The PoC makes no attempt to influence the layout of the main process' memory, so arbitrary data will be shown and access violation may occur. With the PoC loaded in one tab, simply browsing the internet in another should put some interesting information on the heap that gets leaked tot the poc server.

IMPACT  

The impact depends on what happens to be stored on the heap immediately following the buffer. Since a webpage can influence the activities of the main process (eg. it can ask it to make other HTTP requests), a certain amount of control over the heap layout is possible. An attacker could attempt to create a "heap feng shui"-like attack where careful manipulation of the main process' activities allow reading of various types of information from the main process' heap. (The attached PoC does not attempt to do this). The most obvious targets that come to mind are http request/response data for different domains and function pointers that can be used to bypass ASLR/DEP. There are undoubtely many other forms of interesting information that can be revealed in this way.

There are little limits to the number of times an attacker can exploit this vulnerability. If the buffer happens to be stored at the end of the heap, attempts to exploit this vulnerability could trigger an access violation/segmentation fault when the code attempts to read beyond the buffer from unallocated memory addresses. An attacker might be able to reduce this risk with "heap feng shui"-like tricks as well.

FIX:  

I've identified and tested two approaches to fixing this bug:

1. Fix the code where it relies on the response being stored at the start of the buffer.  
   
   Attached is "option 1.patch", which fixes the code that causes this vulnerability as well as other parts of the code. These other parts of the code do not immediately appear to cause security issues, fixing them is a defense in depth.
2. Remove the HTTP 1xx response from the buffer.  
   
   There is inline documentation in the source that explains why HTTP 1xx responses are handled in a special way, but it doesn't make much sense to me. AFAICT the code should remove the response from the buffer and switch to STATE\_DONE. To be on the safe side, I've included a patch that does remove the response, but keeps the code that switches to STATE\_REQUEST\_SENT in case there really is a good reason to do so.  
   
   Added benfit of this fix is that it removes a potential DoS attack, where a server responds with many large HTTP 1xx replies to exhaust memory in the main process.

RELATED ISSUES  

There are multiple locations in http\_stream\_parser.cc that are affected by this problem, but none of them appear to cause (serious) issues. Patch #1 includes fixes for these as a precautionary measure.  

The PoC frequently triggers an unrelated NULL ptr in the renderer if you have the inspector open, for which I've filed <https://crbug.com/chromium/299880>.

Attached:  

poc.zip:  

poc.py -> A PoC server that serve a malicious webpage at <http://localhost:28876/>  

proxy.html -> PoC client side code (used by poc.py)  

option 1.patch -> Fixes the issue by removing the assumption that responses are always located at the start of the buffer.  

option 2.patch -> Fixes the issue by removing HTTP 1xx responses from the buffer.

## Attachments

- [option 2.patch](attachments/option 2.patch) (text/x-diff; charset=us-ascii, 3.1 KB)
- [poc.zip](attachments/poc.zip) (application/zip; charset=binary, 2.6 KB)
- [option 1.patch](attachments/option 1.patch) (text/x-diff; charset=us-ascii, 2.6 KB)
- [101.py](attachments/101.py) (text/x-c++; charset=us-ascii, 3.5 KB)

## Timeline

### aa...@google.com (2013-09-27)

Andrew, can you triage this http parser bug.

### sk...@chromium.org (2013-09-27)

In the description of patch #2, I mentioned a possible DoS scenario with sending "chained" HTTP 100 replies. I've created a PoC for that too, which I've attached.

I consider this another way to exploit this bug, hence I've not opened a new bug for it.

I believe the risk of this DoS to be minimal because the attack requires that an attacker sent vast amounts of data to the client (~1.5Gb, depending on memory fragmentation). This takes a minute or two locally on a fast computer and will probably to take too long to be practical over an average users' internet connection.

### [Deleted User] (2013-09-28)

Looks like ASAN builds are crashing right away with a heap-buffer-overflow (see asan-symbolized-linux-release-225767 below).  The memory leak appears to be working on Chrome 30.0.1599.66 beta / linux.


==11172==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x621000408500 at pc 0x7f7079a9f941 bp 0x7f7055b16ae0 sp 0x7f7055b16ad8
READ of size 1 at 0x621000408500 thread T16 (Chrome_IOThread)
    #0 0x7f7079a9f940 in QuickGetNext /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/strings/string_tokenizer.h:182
    #1 0x7f7079a9ecbd in GetNext /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/strings/string_tokenizer.h:130
    #2 0x7f7079ead666 in AssembleRawHeaders /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_util.cc:609
    #3 0x7f707a12d3fb in DoParseResponseHeaders /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:785
    #4 0x7f707a12bf7c in DoReadHeadersComplete /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:563
    #5 0x7f707a12a042 in DoLoop /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:387
    #6 0x7f707a12a487 in ReadResponseHeaders /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:313
    #7 0x7f7079e426f7 in DoLoop /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_network_transaction.cc:615
    #8 0x7f7079e4112d in OnIOComplete /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_network_transaction.cc:547
    #9 0x7f7079e4e523 in MakeItSo /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:898
    #10 0x7f7079e4e2db in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:1219
    #11 0x7f707a128518 in OnIOComplete /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:355
    #12 0x7f707a12fa04 in MakeItSo /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:909
    #13 0x7f7079f52869 in DidCompleteReadWrite /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/socket/tcp_client_socket.cc:305
    #14 0x7f7079f5349c in MakeItSo /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:927
    #15 0x7f7079f5323b in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:1343
    #16 0x7f7079f568a6 in DidCompleteRead /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/socket/tcp_socket_libevent.cc:714
    #17 0x7f7079f5d5da in MakeItSo /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:871
    #18 0x7f7079f5d3b3 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:1166
    #19 0x7f7079f55771 in OnFileCanReadWithoutBlocking /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/socket/tcp_socket_libevent.cc:109
    #20 0x7f7079a72deb in OnFileCanReadWithoutBlocking /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_pump_libevent.cc:99
    #21 0x7f7079a7424e in OnLibeventNotification /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_pump_libevent.cc:356
    #22 0x7f7079be5d38 in event_process_active /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libevent/event.c:385
    #23 0x7f7079be4f67 in event_base_loop /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/libevent/event.c:525
    #24 0x7f7079a74a82 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_pump_libevent.cc:269
    #25 0x7f7079af8f74 in RunInternal /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:441
    #26 0x7f7079b3e919 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/run_loop.cc:47
    #27 0x7f7079af7d1d in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:311
    #28 0x7f707dff081a in IOThreadRun /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_thread_impl.cc:162
    #29 0x7f707dff0a00 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_thread_impl.cc:188
    #30 0x7f7079b7c709 in ThreadMain /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/thread.cc:205
    #31 0x7f7079b6c9fc in ThreadFunc /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:80
    #32 0x7f7078581663 in ThreadStart _asan_rtl_
    #33 0x7f707011be99 in start_thread /build/buildd/eglibc-2.15/nptl/pthread_create.c:308
    #34 0x7f706ed82ccc in ?? /build/buildd/eglibc-2.15/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:112
0x621000408500 is located 0 bytes to the right of 4096-byte region [0x621000407500,0x621000408500)
allocated by thread T16 (Chrome_IOThread) here:
    #0 0x7f707857acfb in __interceptor_realloc _asan_rtl_
    #1 0x7f7079c1288a in SetCapacity /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/base/io_buffer.cc:96
    #2 0x7f707a12b677 in DoReadHeaders /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:509
    #3 0x7f707a12a02d in DoLoop /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:384
    #4 0x7f707a12a487 in ReadResponseHeaders /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_parser.cc:313
    #5 0x7f7079e426f7 in DoLoop /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_network_transaction.cc:615
    #6 0x7f7079e4112d in OnIOComplete /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_network_transaction.cc:547
    #7 0x7f7079e45540 in OnStreamReady /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_network_transaction.cc:443
    #8 0x7f7079e9da9b in OnStreamReady /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_factory_impl_request.cc:110
    #9 0x7f7079e8b70e in OnStreamReadyCallback /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../net/http/http_stream_factory_impl_job.cc:311
    #10 0x7f7079e9a40d in MakeItSo /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:882
    #11 0x7f7079af9924 in RunTask /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:491
    #12 0x7f7079afa28b in DeferOrRunPendingTask /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:503
    #13 0x7f7079afa4f1 in DoWork /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:617
    #14 0x7f7079a74b01 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_pump_libevent.cc:232
    #15 0x7f7079af8f74 in RunInternal /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:441
    #16 0x7f7079b3e919 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/run_loop.cc:47
    #17 0x7f7079af7d1d in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/message_loop/message_loop.cc:311
    #18 0x7f707dff081a in IOThreadRun /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_thread_impl.cc:162
    #19 0x7f707dff0a00 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_thread_impl.cc:188
    #20 0x7f7079b7c709 in ThreadMain /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/thread.cc:205
    #21 0x7f7079b6c9fc in ThreadFunc /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:80
    #22 0x7f7078581663 in ThreadStart _asan_rtl_
Thread T16 (Chrome_IOThread) created by T0 (chrome) here:
    #0 0x7f707856c451 in __interceptor_pthread_create _asan_rtl_
    #1 0x7f7079b6c2a9 in CreateThread /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:120
    #2 0x7f7079b6c052 in Create /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/platform_thread_posix.cc:199
    #3 0x7f7079b7be1e in StartWithOptions /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/thread.cc:92
    #4 0x7f707dfe3d13 in CreateThreads /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_main_loop.cc:662
    #5 0x7f707dfe92ba in MakeItSo /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:863
    #6 0x7f707dfe9093 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:1166
    #7 0x7f707e34f086 in RunAllTasksNow /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/startup_task_runner.cc:43
    #8 0x7f707dfe3180 in CreateStartupTasks /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_main_loop.cc:580
    #9 0x7f707dfebf41 in Initialize /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_main_runner.cc:109
    #10 0x7f707dfdf9e5 in BrowserMain /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/browser/browser_main.cc:22
    #11 0x7f7079a6746b in RunNamedProcessTypeMain /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/app/content_main_runner.cc:458
    #12 0x7f7079a682f4 in Run /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/app/content_main_runner.cc:781
    #13 0x7f7079a66132 in ContentMain /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/app/content_main.cc:35
    #14 0x7f707858ddd6 in ChromeMain /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/app/chrome_main.cc:39
    #15 0x7f707858dd1a in main /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:43
    #16 0x7f706ecb076c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
Shadow bytes around the buggy address:
  0x0c4280079050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c4280079060: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c4280079070: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c4280079080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c4280079090: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c42800790a0:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c42800790b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c42800790c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c42800790d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c42800790e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c42800790f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==11172==ABORTING

### cl...@chromium.org (2013-09-28)

Adding milestone and impact labels.

### [Deleted User] (2013-09-28)

agl@, can you take a look at this?  You were the last person to touch the relevant code.

### ag...@chromium.org (2013-09-30)

I was the last person to `touch' this code, by moving it around, and I clearly didn't notice that it was broken. Because of that, I think "option 2" (don't keep 1xx responses in the buffer) is preferable so that this subtle assumption doesn't trip anyone up in the future.

I've sent https://codereview.chromium.org/25312002/ to skylined for review. It's basically the option 2 patch from #1 and I've also cleaned up a few other cases where I believe that |read_buf_unused_offset_| is required to be zero.

### wi...@chromium.org (2013-09-30)

[Empty comment from Monorail migration]

### sk...@chromium.org (2013-09-30)

Btw. I think I found the "tunnel" that the inline documentation is referring to:

https://code.google.com/p/chromium/codesearch#chromium/src/net/http/http_proxy_client_socket.cc&q=IsMoreDataBuffered&sq=package:chromium&type=cs&l=452

I've not figured out how it would be affected by this patch yet, and I'm going to have to sign off for the day. I hope @agl can figure it out? :)

### [Deleted User] (2013-09-30)

skylined, I can reproduce the crash in https://crbug.com/chromium/299880 with the script you supplied here (on Chromium 32.0.1657.0 (225791) / linux / debug), but it looks like this test case does not use any non-ascii characters.  So I guess that issue must have some other root cause that's common to both test cases?

### sk...@chromium.org (2013-09-30)

@amtin... The repro for this case itself does not use non-ascii chars, but it causes Chrome to read semi-arbitrary memory as the headers and chances are that memory contains non-ascii chars, thus triggering https://crbug.com/chromium/299880. But since there is no need to use this issue to get non-ascii chars in the headers (simply having a server send a non-ascii char in the headers suffices), I opened a separate bug.

### [Deleted User] (2013-09-30)

Ah! I thought I must be missing something :)

### cb...@chromium.org (2013-10-01)

[Empty comment from Monorail migration]

### cb...@chromium.org (2013-10-01)

Moving to M-30 since this will be going out to stable very soon.

### aa...@google.com (2013-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-10-02)

Only just saw this. Nice bug / report!

### bu...@chromium.org (2013-10-02)

------------------------------------------------------------------------
r226539 | agl@chromium.org | 2013-10-02T19:59:24.108482Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_stream_parser.cc?r1=226539&r2=226538&pathrev=226539
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_stream_parser.h?r1=226539&r2=226538&pathrev=226539
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_proxy_client_socket_pool_unittest.cc?r1=226539&r2=226538&pathrev=226539

net: don't preserve 1xx responses in parser buffer.

It's unclear why 1xx responses were kept in the parser's buffer previously so
this change aligns their processing with all other response types.

BUG=299892

Review URL: https://codereview.chromium.org/25312002
------------------------------------------------------------------------

### in...@chromium.org (2013-10-02)

[Empty comment from Monorail migration]

### ke...@chromium.org (2013-10-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-10-02)

[Comment Deleted]

### ag...@chromium.org (2013-10-02)

(I'll leave it up to others to decide whether we want to merge this to M30 as well as M31.)

### ke...@chromium.org (2013-10-02)

inferno@: Right, old habits and all that. I've updated our security sheriff document with that tidbit: http://www.chromium.org/Home/chromium-security/security-sheriff

### in...@chromium.org (2013-10-02)

Thanks a lot Ken. I will give a presentation at some point on this stuff. Basically Restrict-* labels and Merge-* should be automatically added by sheriff bot :)

### in...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone labels first. Make sure to re-request merge for every milestone in the Merge-To-M-* label. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### la...@google.com (2013-10-18)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-10-21)

Merged to M31 in r229861. Not sure what the "Merge-To-M-31-30" label is, but I'll assume that we don't want to merge to M30.

### bu...@chromium.org (2013-10-21)

------------------------------------------------------------------------
r229861 | agl@chromium.org | 2013-10-21T18:06:30.200441Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/net/http/http_stream_parser.cc?r1=229861&r2=229860&pathrev=229861
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/net/http/http_stream_parser.h?r1=229861&r2=229860&pathrev=229861
   M http://src.chromium.org/viewvc/chrome/branches/1650/src/net/http/http_proxy_client_socket_pool_unittest.cc?r1=229861&r2=229860&pathrev=229861

Merge 226539 "net: don't preserve 1xx responses in parser buffer."

> net: don't preserve 1xx responses in parser buffer.
> 
> It's unclear why 1xx responses were kept in the parser's buffer previously so
> this change aligns their processing with all other response types.
> 
> BUG=299892
> 
> Review URL: https://codereview.chromium.org/25312002

TBR=agl@chromium.org

Review URL: https://codereview.chromium.org/33053003
------------------------------------------------------------------------

### in...@chromium.org (2013-10-21)

No more m30 patches, so work is complete here.

### mb...@chromium.org (2013-10-22)

Thanks for the great report! It qualifies for a $4000 reward because of the detailed analysis and working exploit for the issue.

### ag...@chromium.org (2013-10-31)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Thanks skylined! Payment kicked off on this one, so you should see it in a few weeks.

### sc...@gmail.com (2013-12-18)

@skylined: sorry for the slow payment! We will try to improve.

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ef...@chromium.org (2018-07-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network]

### ef...@chromium.org (2018-07-06)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Network>HTTP]

### is...@google.com (2018-07-06)

This issue was migrated from crbug.com/chromium/299892?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078172)*
