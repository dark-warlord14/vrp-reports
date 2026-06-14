# Heap-buffer-overflow WRITE in read_markers third_party/libjpeg_turbo/jdmarker

| Field | Value |
|-------|-------|
| **Issue ID** | [40058947](https://issues.chromium.org/issues/40058947) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **CVE IDs** | CVE-2012-2806 |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-05-30 |
| **Bounty** | $1,000.00 |

## Description

Reprofile as attachment.

Chrome: 21.0.1156.0 (Developer Build 139280)

ASAN-Report:

=================================================================
==14748== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fda1fc6ac90 at pc 0x7fda2f0ee9f6 bp 0x7fff3fcd3f30 sp 0x7fff3fcd3f28
WRITE of size 8 at 0x7fda1fc6ac90 thread T0
    #0 0x7fda2f0ee9f6 in read_markers third_party/libjpeg_turbo/jdmarker.c:0
    #1 0x7fda2f0e644d in consume_markers third_party/libjpeg_turbo/jdinput.c:0
    #2 0x7fda2f0e3438 in chromium_jpeg_consume_input ???:0
    #3 0x7fda2f0e3102 in chromium_jpeg_read_header ???:0
    #4 0x7fda2fe103b9 in WebCore::JPEGImageReader::decode(WebCore::SharedBuffer const&, bool) ???:0
    #5 0x7fda2fe0edb9 in WebCore::JPEGImageDecoder::decode(bool) ???:0
    #6 0x7fda2fe0e5bf in WebCore::JPEGImageDecoder::isSizeAvailable() ???:0
    #7 0x7fda2fcca398 in WebCore::ImageSource::isSizeAvailable() ???:0
    #8 0x7fda2fc69d21 in WebCore::BitmapImage::isSizeAvailable() ???:0
    #9 0x7fda2fc69c3a in WebCore::BitmapImage::dataChanged(bool) ???:0
    #10 0x7fda2fcc8364 in WebCore::Image::setData(WTF::PassRefPtr<WebCore::SharedBuffer>, bool) ???:0
    #11 0x7fda30671134 in WebCore::CachedImage::data(WTF::PassRefPtr<WebCore::SharedBuffer>, bool) ???:0
    #12 0x7fda2fa07392 in WebCore::ImageDocumentParser::appendBytes(WebCore::DocumentWriter*, char const*, unsigned long) ???:0
    #13 0x7fda305aeb10 in WebCore::DocumentLoader::commitData(char const*, unsigned long) ???:0
    #14 0x7fda2f26619c in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int) ???:0
    #15 0x7fda305aedae in WebCore::DocumentLoader::commitLoad(char const*, int) ???:0
    #16 0x7fda30645d13 in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) ???:0
    #17 0x7fda3062223c in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) ???:0
    #18 0x7fda306472d8 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) ???:0
    #19 0x7fda2ece9cc8 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) ???:0
    #20 0x7fda2ece7fe1 in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0
    #21 0x7fda2ece62d6 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0
    #22 0x7fda2ebdd36b in ChildThread::OnMessageReceived(IPC::Message const&) ???:0
    #23 0x7fda2d8c3355 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0
    #24 0x7fda2d79d775 in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #25 0x7fda2d79debc in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #26 0x7fda2d79f422 in MessageLoop::DoWork() ???:0
    #27 0x7fda2d7a9247 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ???:0
    #28 0x7fda2d79c3c2 in MessageLoop::RunInternal() ???:0
    #29 0x7fda2d79a5ae in MessageLoop::Run() ???:0
    #30 0x7fda330794c3 in RendererMain(content::MainFunctionParams const&) ???:0
    #31 0x7fda2d657f85 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:0
    #32 0x7fda2d655f65 in content::ContentMain(int, char const**, content::ContentMainDelegate*) ???:0
    #33 0x7fda2c1a4c47 in ChromeMain ??:0
    #34 0x7fda2c1a4bab in main ???:0
    #35 0x7fda252edeff in __libc_start_main /build/buildd/eglibc-2.13/csu/libc-start.c:258
0x7fda1fc6ac90 is located 0 bytes to the right of 1040-byte region [0x7fda1fc6a880,0x7fda1fc6ac90)
allocated by thread T0 here:
    #0 0x7fda343ba022 in operator new(unsigned long) ??:0
    #1 0x7fda2fe0e9d7 in WebCore::JPEGImageDecoder::decode(bool) ???:0
    #2 0x7fda2fe0e5bf in WebCore::JPEGImageDecoder::isSizeAvailable() ???:0
    #3 0x7fda2fcca398 in WebCore::ImageSource::isSizeAvailable() ???:0
    #4 0x7fda2fc69d21 in WebCore::BitmapImage::isSizeAvailable() ???:0
    #5 0x7fda2fc69c3a in WebCore::BitmapImage::dataChanged(bool) ???:0
    #6 0x7fda2fcc8364 in WebCore::Image::setData(WTF::PassRefPtr<WebCore::SharedBuffer>, bool) ???:0
    #7 0x7fda30671134 in WebCore::CachedImage::data(WTF::PassRefPtr<WebCore::SharedBuffer>, bool) ???:0
    #8 0x7fda2fa07392 in WebCore::ImageDocumentParser::appendBytes(WebCore::DocumentWriter*, char const*, unsigned long) ???:0
    #9 0x7fda305aeb10 in WebCore::DocumentLoader::commitData(char const*, unsigned long) ???:0
    #10 0x7fda2f26619c in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int) ???:0
    #11 0x7fda305aedae in WebCore::DocumentLoader::commitLoad(char const*, int) ???:0
    #12 0x7fda30645d13 in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) ???:0
    #13 0x7fda3062223c in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) ???:0
    #14 0x7fda306472d8 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) ???:0
    #15 0x7fda2ece9cc8 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) ???:0
    #16 0x7fda2ece7fe1 in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0
    #17 0x7fda2ece62d6 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0
    #18 0x7fda2ebdd36b in ChildThread::OnMessageReceived(IPC::Message const&) ???:0
    #19 0x7fda2d8c3355 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0
    #20 0x7fda2d79d775 in MessageLoop::RunTask(base::PendingTask const&) ???:0
    #21 0x7fda2d79debc in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0
    #22 0x7fda2d79f422 in MessageLoop::DoWork() ???:0
==14748== ABORTING
Stats: 4M malloced (6M for red zones) by 19281 calls
Stats: 0M realloced by 37 calls
Stats: 2M freed by 8791 calls
Stats: 0M really freed by 0 calls
Stats: 44M (11270 full pages) mmaped in 11 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;
  mallocs by size class: 8:16617; 9:1166; 10:1185; 11:153; 12:51; 13:25; 14:16; 15:8; 16:59; 17:1;
  frees   by size class: 8:6875; 9:682; 10:1083; 11:49; 12:24; 13:14; 14:8; 15:3; 16:53;
  rfrees  by size class:
Stats: malloc large: 1 small slow: 100
Shadow byte and word:
  0x1ffb43f8d592: fb
  0x1ffb43f8d590: 00 00 fb fb fb fb fb fb
More shadow bytes:
  0x1ffb43f8d570: 00 00 00 00 00 00 00 00
  0x1ffb43f8d578: 00 00 00 00 00 00 00 00
  0x1ffb43f8d580: 00 00 00 00 00 00 00 00
  0x1ffb43f8d588: 00 00 00 00 00 00 00 00
=>0x1ffb43f8d590: 00 00 fb fb fb fb fb fb
  0x1ffb43f8d598: fb fb fb fb fb fb fb fb
  0x1ffb43f8d5a0: fa fa fa fa fa fa fa fa
  0x1ffb43f8d5a8: fa fa fa fa fa fa fa fa
  0x1ffb43f8d5b0: fa fa fa fa fa fa fa fa



## Attachments

- [cnode0006-heap-buffer-overflow-796.gif](attachments/cnode0006-heap-buffer-overflow-796.gif) (image/jpeg; charset=binary, 6.7 KB)
- [130240_asan.txt](attachments/130240_asan.txt) (text/x-c; charset=us-ascii, 13.3 KB)
- [sample-gif-0783.gif](attachments/sample-gif-0783.gif) (image/jpeg; charset=binary, 6.9 KB)

## Timeline

### sc...@gmail.com (2012-05-30)

Interesting!

The stack trace looks like it is missing accurate line numbers, any ideas?

I'll run it in my local ASAN build tomorrow.

### kc...@chromium.org (2012-05-30)

symbolizing asan logs may require a machine with LOTS of RAM. 
We are very close to solving this problem with the clang flag -gline-tables-only, 
meanwhile here is a symbolized log for your convenience (reproduces easily): 

==19009== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f08a2930c90 at pc 0x7f08c55405a7 bp 0x7f089e9746f0 sp 0x7f089e9746e8                                                           
WRITE of size 8 at 0x7f08a2930c90 thread T16                                                                                                                                                        
    #0 0x7f08c55405a7 in get_sos third_party/libjpeg_turbo/jdmarker.c:327                                                                                                                           
    #1 0x7f08c5537f2d in consume_markers third_party/libjpeg_turbo/jdinput.c:312                                                                                                                    
    #2 0x7f08c5534ec8 in chromium_jpeg_consume_input third_party/libjpeg_turbo/jdapimin.c:301                                                                                                       
    #3 0x7f08c5534b92 in chromium_jpeg_read_header third_party/libjpeg_turbo/jdapimin.c:249                                     


0x7f08a2930c90 is located 0 bytes to the right of 1040-byte region [0x7f08a2930880,0x7f08a2930c90)                                                                                                  
allocated by thread T16 here:                                                                                                                                                                       
    #0 0x7f08c61004b2 in operator new(unsigned long) ??:0                                                                                                                                           
    #1 0x7f08c37308ac in WebCore::JPEGImageDecoder::decode(bool) third_party/WebKit/Source/WebCore/platform/image-decoders/jpeg/JPEGImageDecoder.cpp:596                                            
    #2 0x7f08c373049f in WebCore::JPEGImageDecoder::isSizeAvailable() third_party/WebKit/Source/WebCore/platform/image-decoders/jpeg/JPEGImageDecoder.cpp:465                                       
    #3 0x7f08c35d97b8 in WebCore::ImageSource::isSizeAvailable() third_party/WebKit/Source/WebCore/platform/graphics/ImageSource.cpp:104                                                            
    #4 0x7f08c3586261 in WebCore::BitmapImage::isSizeAvailable() third_party/WebKit/Source/WebCore/platform/graphics/BitmapImage.cpp:277                                                            
    #5 0x7f08c3586179 in WebCore::BitmapImage::dataChanged(bool) third_party/WebKit/Source/WebCore/platform/graphics/BitmapImage.cpp:254                                                            
    #6 0x7f08c35d6afd in WebCore::Image::setData(WTF::PassRefPtr<WebCore::SharedBuffer>, bool) third_party/WebKit/Source/WebCore/platform/graphics/Image.cpp:79                                     
    #7 0x7f08c1127ea9 in WebCore::CachedImage::data(WTF::PassRefPtr<WebCore::SharedBuffer>, bool) third_party/WebKit/Source/WebCore/loader/cache/CachedImage.cpp:360                                
    #8 0x7f08c4fd4f22 in ~PassRefPtr third_party/WebKit/Source/WTF/wtf/PassRefPtr.h:67                                                                                                              
    #9 0x7f08c106d1ef in WebCore::DocumentLoader::commitData(char const*, unsigned long) third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:350          

### at...@gmail.com (2012-05-30)

same test-case also causes Null-pointer execution with Firefox. Is it okay if I report this also to Mozilla as a security bug?

### sc...@gmail.com (2012-05-30)

Yes, please do. Is their embedded libjpeg the turbo variety or plain variety (if so which version, 6 or 8?)

### at...@gmail.com (2012-05-30)

Chris: If you like I could ask if they could CC you for the bug?

### at...@gmail.com (2012-05-30)

Chris: From Firefox bug: "We use jpeg-turbo in Firefox, version v1.2.0."

### at...@gmail.com (2012-05-30)

From bugzilla.mozilla:
Justin Lebar [:jlebar] 2012-05-30 10:21:47 PDT
> This issue seems to affect also Google Chrome and I have already reported it to Google. 

Is there a Google bug report you can link us to?

cc DRC, the libjpeg-turbo maintainer.

### sc...@gmail.com (2012-05-30)

@attekett: this is very interesting. Can you attach the original unmutated file if possible?

Also, can you ask Mozilla if they'd like to be cc:ed on the bug? We should co-ordinate here, I'm starting to suspect it might be sensible to co-ordinate this one.

### sc...@gmail.com (2012-05-30)

I will own this.

### at...@gmail.com (2012-05-30)

I can find the file with highest possibility to be the original. My version of radamsa doesn't track original files.

### sc...@gmail.com (2012-05-30)

Please do. Incidentally, it's my belief that this will require reward.

### at...@gmail.com (2012-05-30)

[Comment Deleted]

### at...@gmail.com (2012-05-30)

I think that this is the original file. Beginning of the file seems to be mutated and endings are identical. 

Chris: If you think this is not the original file let me know. 

### at...@gmail.com (2012-05-30)

Chris: They CC:ed you to the bugzilla bug.

And the issue should be fixed in libjpeg-turbo SVN repository.

From Bugzilla:

DRC 2012-05-30 13:37:40 PDT
Fix checked into trunk and branches/1.2.x in libjpeg-turbo SVN repository.

### sc...@gmail.com (2012-05-30)

Oh thanks. I have a fix too. I'll see how close they are :)

FWIW, "normal" libjpeg does not appear to have the faulty code.


### bu...@chromium.org (2012-05-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=139642

------------------------------------------------------------------------
r139642 | cevans@chromium.org | Wed May 30 14:50:31 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/libjpeg_turbo/README.chromium?r1=139642&r2=139641&pathrev=139642
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/libjpeg_turbo/jdmarker.c?r1=139642&r2=139641&pathrev=139642

Pull in r830 from upstream.

BUG=130240
Review URL: https://chromiumcodereview.appspot.com/10459034
------------------------------------------------------------------------

### bu...@chromium.org (2012-05-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=139650

------------------------------------------------------------------------
r139650 | cevans@chromium.org | Wed May 30 15:22:58 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=139650&r2=139649&pathrev=139650

Pull in latest libjpeg-turbo.

BUG=130240
TBR=cdn
Review URL: https://chromiumcodereview.appspot.com/10442093
------------------------------------------------------------------------

### sc...@gmail.com (2012-05-30)

Any ideas how Firefox / upstream libjpeg-turbo / Linux distros want to handle this?

### sc...@gmail.com (2012-05-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-31)

CVE-2012-2806

BTW @attekett, I think we should try and make sure you qualify for the Mozilla security reward as well as the Chrome one, since this is a great find. I expect that'll happen automatically, but let me know if it doesn't -- I have good Mozilla contacts.

If you could share the CVE with Mozilla, that'd help prevent confusion.

### at...@gmail.com (2012-05-31)

@scarybeasts, I forwarded the CVE information. It would be great if this would qualify also on the Mozilla side.

### sc...@gmail.com (2012-05-31)

Good news. This broke in libjpeg_turbo r740:

http://libjpeg-turbo.svn.sourceforge.net/viewvc/libjpeg-turbo/trunk/jdmarker.c?view=log&pathrev=752

This most recent fix in r830 is the second tweak to the same condition :-/


We didn't pull in the original breakage until Chromium r136524:
http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/libjpeg_turbo/jdmarker.c?view=log

Accordingly, stable and beta are unaffected. Good regression catch :) May be good to explicitly target jpeg fuzzing some more? Tavis put together an excellent set of base jpeg images based on code coverage:
https://code.google.com/p/imagetestsuite/downloads/detail?name=imagetestsuite-jpg-1.00.tar.gz


### sc...@gmail.com (2012-06-22)

$1000
Let us know how the Mozilla reward goes ;-)

### si...@gmail.com (2012-06-22)

We are not making this public, until Mozilla releases it i suppose?
By public, i mean able to announce that this is a security issue, no need to give full details though.

### at...@gmail.com (2012-06-22)

@scarybeasts: Thanks. I'll let you know.

### sc...@gmail.com (2012-06-22)

@sidhpurwala.huzaifa: Chrome stable was never affected by this so you won't see anything from us. I'll leave this bug hidden for plenty of time.

### at...@gmail.com (2012-06-22)

@scarybeasts: Mozilla also marked the bug as sec-critical. The opinion you emailed about null write exploitability helped. Thanks.

### si...@gmail.com (2012-06-26)

@scarybeats,

Do you think we can make this issue semi-public and fix it in fedora. 
I have copied you in https://bugzilla.redhat.com/show_bug.cgi?id=826849

(You should be able to use your Red Hat bugzilla password to login)
So that you can have a look at the flaw description we have used here.

Thanks!

### sc...@gmail.com (2012-06-26)

Production versions of Chromium are unaffected so no particular constraints here. You might want to co-ordinate with Mozilla, not sure what their status is.

### at...@gmail.com (2012-06-26)

@scarybeasts: The bugzilla bug number is 759802 ( https://bugzilla.mozilla.org/show_bug.cgi?id=759802 ).

You have been CC:ed in there so you should be able to check the status. 

### si...@gmail.com (2012-06-26)

@scarybeasts
The mozilla bug suggests that this affects firefox 14, which is going to be released on 17-July-2012, which i think implies that this issue will be open then.

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-10-12)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/130240?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058947)*
