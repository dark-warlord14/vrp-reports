# Chrome chrashes when pressing back button on a page that is still downloading a big gif image

| Field | Value |
|-------|-------|
| **Issue ID** | [40057340](https://issues.chromium.org/issues/40057340) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals, Internals>Network>Cache |
| **Reporter** | ef...@gmail.com |
| **Assignee** | rv...@chromium.org |
| **Created** | 2012-04-26 |
| **Bounty** | $1,337.00 |

## Description

Chrome Version : 18.0.1025.162 (revision 131933) m  

OS Version: 6.1 (Windows 7 Pro 64bit)  

**URLs (if applicable) :**  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 5:OK  

Firefox 4.x:OK  

IE 7/8/9:OK

**What steps will reproduce the problem?**

1. Open <http://www.upload.ee/top/toprated.html?p=0>
2. Click on the first item that navigates to:  
   
   <http://www.upload.ee/gallery/82/Igasugu_kraami.html?vid=5051>
3. Before the image has finished downloading (about 0.5 seconds after the layout gets displayed) press back button.

Sometimes it takes a few tries with back-click-back-click but essentially always reproducible.

**What is the expected result?**  

Chrome navigates back successfully and then continues working normally.

**What happens instead?**  

Chrome chrashes with C++ runtime error: "This application has requested the Runtime to terminate in an unusual way."

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

## Attachments

- [chrome_crash.png](attachments/chrome_crash.png) (image/png; charset=binary, 225.5 KB)
- [crash_asan_chromium_release_131054.txt](attachments/crash_asan_chromium_release_131054.txt) (text/plain; charset=us-ascii, 10.0 KB)
- [crash_asan_chromium_release_135549.txt](attachments/crash_asan_chromium_release_135549.txt) (text/plain; charset=us-ascii, 10.2 KB)
- [crash_asan_symbolized.txt](attachments/crash_asan_symbolized.txt) (text/x-c; charset=us-ascii, 12.2 KB)

## Timeline

### ef...@gmail.com (2012-04-26)

I managed to do a dump of all three chrome processes in memory with visual studio, compressed them and uploaded to: http://www.upload.ee/files/2294703/chrome_debug.zip.html

I did not manage to track down the exact place where the error itself occured since I'm not fluent native code debugger myself but perhaps those dumps with usecase can shed some light.

Note: browser cache must be cleaned before testing, since if the image itself is in cache the crash will not occur.

I started chrome with --no-sandbox --disable-extensions --disable-internal-flash --disable-plugins --disable-flash-sandbox --disable-java to keep the things simpler.
The bug occurs on normal startup also, but I wanted to minimize the amount of debugged code.

### me...@chromium.org (2012-04-26)

Is there a crash id at chrome://crashes to find ?

### ef...@gmail.com (2012-04-26)

Nope.
I had first auto-reporting disabled as chrome://crashes pointed out.
I re-enabled it, reproduced the crash with methods described in the bug, started chrome again.
Opened chrome://crashes but it was empty.
Can you perhaps try to reproduce it with same stable Chrome version on win7 64bit?

### ef...@gmail.com (2012-04-27)

I did some investigation about what requests are sent out after the image loading has been cancelled.

These are the headers chrome sends after I have cancelled image loading (pressed back) and then forward again.

GET /image/5051/accident22.gif HTTP/1.1
Host: www.upload.ee
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate,sdch
Accept-Language: et-EE,et;q=0.8,en-US;q=0.6,en;q=0.4
Accept-Charset: windows-1257,utf-8;q=0.7,*;q=0.3
Range: bytes=57927-57927
If-Range: Thu, 15 Jan 2009 15:39:01 GMT

Seems to be a resume-capability check for single byte, server responds with:

HTTP/1.1 206 Partial Content
Server: nginx
Date: Fri, 27 Apr 2012 12:49:29 GMT
Content-Type: image/gif
Content-Length: 1
Last-Modified: Thu, 15 Jan 2009 15:39:01 GMT
Connection: keep-alive
Expires: Mon, 26 Jul 1997 05:00:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Cache-Control: post-check=0, pre-check=0
Accept-Ranges: bytes
Content-Disposition: inline; filename="accident22.gif"
Content-Range: bytes 57927-57927/2446514

After that Chrome does another request since it confirmed file resume support:

GET /image/5051/accident22.gif HTTP/1.1
Host: www.upload.ee
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate,sdch
Accept-Language: et-EE,et;q=0.8,en-US;q=0.6,en;q=0.4
Accept-Charset: windows-1257,utf-8;q=0.7,*;q=0.3
Range: bytes=57927-2446513
If-Range: Thu, 15 Jan 2009 15:39:01 GMT

Server replies:

HTTP/1.1 206 Partial Content
Server: nginx
Date: Fri, 27 Apr 2012 12:49:29 GMT
Content-Type: image/gif
Content-Length: 2388587
Last-Modified: Thu, 15 Jan 2009 15:39:01 GMT
Connection: keep-alive
Expires: Mon, 26 Jul 1997 05:00:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Cache-Control: post-check=0, pre-check=0
Accept-Ranges: bytes
Content-Disposition: inline; filename="accident22.gif"
Content-Range: bytes 57927-2446513/2446514

And then the C++ runtime crash happens.
Note, Chrome kept downloading the image in the background and javascript on other open pages seems to remain running, but the rendering engine itself seems crashed: I can close any tabs but none will display their contents anymore.

I tried starting chrome with --single-process flag to see if I can catch something in rendering engine, but I was unable to do that because of known nullpointer issue https://code.google.com/p/chromium/issues/detail?id=110953

### li...@chromium.org (2012-04-27)

[Empty comment from Monorail migration]

### ef...@gmail.com (2012-04-29)

The initial request headers for the file were missing from last comment, I'll add them too:


GET /image/5051/accident22.gif HTTP/1.1
Host: www.upload.ee
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate,sdch
Accept-Language: et-EE,et;q=0.8,en-US;q=0.6,en;q=0.4
Accept-Charset: windows-1257,utf-8;q=0.7,*;q=0.3


HTTP/1.1 200 OK
Server: nginx
Date: Sun, 29 Apr 2012 09:13:26 GMT
Content-Type: image/gif
Content-Length: 2446514
Last-Modified: Thu, 15 Jan 2009 15:39:01 GMT
Connection: keep-alive
Expires: 
Cache-Control: public, max-age=604800, s-maxage=300, must-revalidate, proxy-revalidate
Accept-Ranges: bytes
Content-Disposition: inline; filename="accident22.gif"
Accept-Ranges: bytes


The headers are a bit different for resume request and for the initial request.
Initial request receives

Expires: 
Cache-Control: public, max-age=604800, s-maxage=300, must-revalidate, proxy-revalidate

Resume request receives

Expires: Mon, 26 Jul 1997 05:00:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Cache-Control: post-check=0, pre-check=0

This is likely due to a server side code that sets the headers and by changing the Cache-Control headers the crash goes away. But this behavior does not crash any other browsers I tested (FF, IE, Safari, Opera).

### ef...@gmail.com (2012-05-06)

Also reproducible with provided usecase on Ubuntu 64bit with latest asan build 135549.
==6590== ERROR: AddressSanitizer heap-use-after-free on address 0x7f62f7b40388 at pc 0x7f6326152d7f bp 0x7f630fa3c310 sp 0x7f630fa3c308

Crash logs attached (asan build 135549 and 131054). Logs are not symbolized, I don't have enough memory allocated for.

On linux the crash occurs when navigating back from that gif containing page.

### in...@chromium.org (2012-05-07)

Can you please symbolize your asan stack using asan_symbolize.py and c++filt. Also, if you minimize the repro, that might qualify you for chromium security reward. In the future, please file asan security reports (like use after frees, buffer overflow, etc) using the security template.

### ef...@gmail.com (2012-05-07)

Sorry for not using security template, I was not able to get any info about the crash on my windows. Only later when I downloaded ubuntu and ASAN build of chrome was I able to get any decent information.
After symbolizing the trace I got:

WRITE of size 8 at 0x7fc773909688 thread T11
    #0 0x7fc7a04ebd7f in net::HttpCache::DoneWritingToEntry(net::HttpCache::ActiveEntry*, bool) /b/build/slave/ASAN_Release__symbolized_/build/net/http/http_cache.cc:878
    #1 0x7fc7a04eba11 in net::HttpCache::DoneWithEntry(net::HttpCache::ActiveEntry*, net::HttpCache::Transaction*, bool) /b/build/slave/ASAN_Release__symbolized_/build/net/http/http_cache.cc:864
    #2 0x7fc7a04f908b in net::HttpCache::Transaction::~Transaction() /b/build/slave/ASAN_Release__symbolized_/build/net/http/http_cache_transaction.cc:158
    #3 0x7fc7a04f8e8e in net::HttpCache::Transaction::~Transaction() /b/build/slave/ASAN_Release__symbolized_/build/net/http/http_cache_transaction.cc:134
    #4 0x7fc7a04e73e7 in scoped_ptr<net::HttpTransaction>::reset(net::HttpTransaction*) /b/build/slave/ASAN_Release__symbolized_/build/./base/memory/scoped_ptr.h:185
    #5 0x7fc7a07cac70 in net::URLRequestHttpJob::DestroyTransaction() /b/build/slave/ASAN_Release__symbolized_/build/net/url_request/url_request_http_job.cc:254
    #6 0x7fc7a07cf32e in net::URLRequestHttpJob::Kill() /b/build/slave/ASAN_Release__symbolized_/build/net/url_request/url_request_http_job.cc:823
    #7 0x7fc7a064b571 in net::URLRequest::DoCancel(int, net::SSLInfo const&) /b/build/slave/ASAN_Release__symbolized_/build/net/url_request/url_request.cc:516
    #8 0x7fc7a06476e4 in net::URLRequest::Cancel() /b/build/slave/ASAN_Release__symbolized_/build/net/url_request/url_request.cc:483
    #9 0x7fc7a3a718f2 in
    #10 0x7fc7a3a6e0ac in
    #11 0x7fc7a3a6a520 in
...........
    #30 0x7fc7a51a6b2c in

Where can I see those ASAN build files to investigate it a bit more ? Looking at current svn verion of http_cache.cc I can see that it has only 817 lines and the function in question starts at line 581.

### ef...@gmail.com (2012-05-08)

Also for some reason the asan_symbolyze.py does not decode all addresses, is that normal?

The information block about where the free was done looks the same, no info:
0x7fc773909688 is located 8 bytes inside of 56-byte region [0x7fc773909680,0x7fc7739096b8)
freed by thread T11 here:
    #0 0x7fc7a51aa2a2 in
    #1 0x7fc7a04e93be in
    #2 0x7fc7a04ebc94 in
...............

    #27 0x7fc7a03b0658 in
    #28 0x7fc7a025a3da in
    #29 0x7fc7a025b834 in
previously allocated by thread T11 here:
    #0 0x7fc7a51aa122 in
    #1 0x7fc7a04e9995 in
    #2 0x7fc7a04edfdf in
........

### [Deleted User] (2012-05-08)

I was able to repro this on Win7 trunk today. It also hits a bunch of DCHECKs before blowing up. Given the required user interaction though I am thinking high severity unless someone feels strongly about treating it as critical.

rvargas, can you suggest an owner for this?

### rv...@chromium.org (2012-05-08)

I'll take a look.

### ef...@gmail.com (2012-05-08)

I gave the VM 11GB swap and it managed to symbolize the asan trace fully.

The entry gets deleted at:

0x7fc773909688 is located 8 bytes inside of 56-byte region [0x7fc773909680,0x7fc7739096b8)
freed by thread T11 here:
    #0 0x7fc7a51aa2a2 in operator delete(void*) ??:0
    #1 0x7fc7a04e93be in net::HttpCache::FinalizeDoomedEntry(net::HttpCache::ActiveEntry*) http_cache.cc:659
    #2 0x7fc7a04ebc94 in net::HttpCache::DoneWritingToEntry(net::HttpCache::ActiveEntry*, bool) http_cache.cc:889
    #3 0x7fc7a04fdfc0 in net::HttpCache::Transaction::DoneWritingToEntry(bool) http_cache_transaction.cc:2020


### ef...@gmail.com (2012-05-08)

[Comment Deleted]

### rv...@chromium.org (2012-05-08)

The problematic path:

net!net::HttpCache::FinalizeDoomedEntry+0x4b [http_cache.cc @ 649]
net!net::HttpCache::DestroyEntry+0x25 [http_cache.cc @ 802]
net!net::HttpCache::DoneWritingToEntry+0x241 [http_cache.cc @ 889]
net!net::HttpCache::Transaction::DoneWritingToEntry+0x1ed [http_cache_transaction.cc @ 2023]
net!net::HttpCache::Transaction::WriteResponseInfoToEntry+0x19a [http_cache_transaction.cc @ 1984]
net!net::HttpCache::Transaction::DoCacheWriteTruncatedResponse+0x8c [http_cache_transaction.cc @ 1265]
net!net::HttpCache::Transaction::DoLoop+0xf1c [http_cache_transaction.cc @ 607]
net!net::HttpCache::Transaction::AddTruncatedFlag+0x196 [http_cache_transaction.cc @ 199]
net!net::HttpCache::DoneWithEntry+0x216 [http_cache.cc @ 862]
net!net::HttpCache::Transaction::~Transaction+0x114 [http_cache_transaction.cc @ 150]
net!net::HttpCache::Transaction::`scalar deleting destructor'+0x16
net!scoped_ptr<net::HttpTransaction>::reset+0x49 [scoped_ptr.h @ 185]
net!net::URLRequestHttpJob::DestroyTransaction+0x12e [url_request_http_job.cc @ 266]
net!net::URLRequestHttpJob::Kill+0x38 [url_request_http_job.cc @ 841]
net!net::URLRequest::DoCancel+0x194 [url_request.cc @ 511]
net!net::URLRequest::Cancel+0x60

Basically the request is cancelled so we attempt to mark the entry as truncated, but that process figures out that the latest headers have "no-store" so instead the entry is deleted... but when we come back up the stack, the HttpCache doesn't realize that the Transaction deleted the entry, and attempts to close it (and delete the object again), and crashes in the process.

The good news is that nobody else has time to access the deleted object before the crash (at least with a thread-related allocator like tcmalloc).

### rv...@chromium.org (2012-05-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-05-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=136172

------------------------------------------------------------------------
r136172 | rvargas@google.com | Wed May 09 16:44:27 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_cache.cc?r1=136172&r2=136171&pathrev=136172
 M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_cache_unittest.cc?r1=136172&r2=136171&pathrev=136172
 M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_cache_transaction.cc?r1=136172&r2=136171&pathrev=136172
 M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_cache_transaction.h?r1=136172&r2=136171&pathrev=136172

Http cache: Don't attempt to doom the same entry multiple times
and make sure that side effects of adding the truncation flag are
considered by the cache.

BUG=125159
TEST=net_unittests
Review URL: https://chromiumcodereview.appspot.com/10382089
------------------------------------------------------------------------

### sc...@gmail.com (2012-05-10)

Could this be triggered without user interaction by using back() in Javascript?

### rv...@chromium.org (2012-05-10)

Yes. The proper server responses + javascript can trigger the crash.

### sc...@gmail.com (2012-05-10)

Seems critical then.

### js...@chromium.org (2012-05-10)

Why the critical label? Based on https://crbug.com/chromium/125159#c15 it sounds like this isn't exploitable.

### sc...@gmail.com (2012-05-10)

I +1'ed the severity based on https://crbug.com/chromium/125159#c11 by Cris (noting user interaction) and https://crbug.com/chromium/125159#c19 by Ricardo (script could achieve the same thing)

If we're comfortable that the stack unwind doesn't allocate any objects with any hint of attacker control into the freed slot -- is there a precedent for where to downgrade severity to?

### rv...@chromium.org (2012-05-10)

I followed the code again, and having queued requests will force them to be restarted while unwinding, and that's a complex path that most likely will end up allocating memory.

In fact I'll write another test to make sure everything works as expected in that case.

### rv...@chromium.org (2012-05-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-05-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=138195

------------------------------------------------------------------------
r138195 | cevans@chromium.org | Mon May 21 19:09:26 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/net/http/http_cache_unittest.cc?r1=138195&r2=138194&pathrev=138195
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/net/http/http_cache_transaction.h?r1=138195&r2=138194&pathrev=138195
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/net/http/http_cache.cc?r1=138195&r2=138194&pathrev=138195
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/net/http/http_cache_transaction.cc?r1=138195&r2=138194&pathrev=138195

Merge 136172 - Http cache: Don't attempt to doom the same entry multiple times
and make sure that side effects of adding the truncation flag are
considered by the cache.

BUG=125159
TEST=net_unittests
Review URL: https://chromiumcodereview.appspot.com/10382089

TBR=rvargas@google.com
Review URL: https://chromiumcodereview.appspot.com/10413045
------------------------------------------------------------------------

### bu...@chromium.org (2012-05-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=138196

------------------------------------------------------------------------
r138196 | cevans@chromium.org | Mon May 21 19:11:35 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/net/http/http_cache.cc?r1=138196&r2=138195&pathrev=138196
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/net/http/http_cache_transaction.cc?r1=138196&r2=138195&pathrev=138196
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/net/http/http_cache_transaction.h?r1=138196&r2=138195&pathrev=138196
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/net/http/http_cache_unittest.cc?r1=138196&r2=138195&pathrev=138196

Merge 136172 - Http cache: Don't attempt to doom the same entry multiple times
and make sure that side effects of adding the truncation flag are
considered by the cache.

BUG=125159
TEST=net_unittests
Review URL: https://chromiumcodereview.appspot.com/10382089

TBR=rvargas@google.com
Review URL: https://chromiumcodereview.appspot.com/10407086
------------------------------------------------------------------------

### sc...@gmail.com (2012-05-23)

@efbiaiinzinz: this qualifies for a $1337 Chromium security reward, congrats!

Normally we don't pay for things not filed as security issues, but in this case we balanced that against the possible severity of the issue, and the really great helpfulness shown.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issue.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---

### sc...@gmail.com (2012-05-23)

BTW, not sure I'll be able to get it in on time, but let us know if there's some particular name you'd like us to credit in our release notes.

### bu...@chromium.org (2012-05-29)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=139331

------------------------------------------------------------------------
r139331 | rvargas@google.com | Tue May 29 11:38:57 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_cache_unittest.cc?r1=139331&r2=139330&pathrev=139331

Http cache: Test deleting an entry with a pending_entry when
adding the truncated flag.

BUG=125159
TEST=net_unittests
Review URL: https://chromiumcodereview.appspot.com/10356113
------------------------------------------------------------------------

### ef...@gmail.com (2012-06-26)

How does the award process usually proceed?
I'm asking because no one has contacted me yet to ask for my address and other details. Stable Chrome with the fix was released more than a month ago already.

Regards,
Indrek Altpere

### sc...@gmail.com (2012-06-26)

Hey, I'll make sure someone reaches out shortly! Payments are usually handled in batches and a batch is coming up :)

### sc...@gmail.com (2012-07-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/125159?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Internals>Network>Cache]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057340)*
