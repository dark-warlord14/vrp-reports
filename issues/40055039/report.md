# Heap use after free on chrome_content_browser_client.cc with webrtc

| Field | Value |
|-------|-------|
| **Issue ID** | [40055039](https://issues.chromium.org/issues/40055039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebRTC, Internals |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2012-03-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Attached test case causes a chrome browser crash due to heap use after free.

**VERSION**  

Chrome Version: [19.0.1071.0 (126899)] + [dev]  

Operating System: [Ubuntu 10.04 64 bit]

**REPRODUCTION CASE**

1. Open chrome
2. Visit chrome://flags
3. Locate Enable MediaStream and enable it.
4. Restart chrome.
5. Download attached test.html.
6. Open test.html in chrome and wait 2 seconds.
7. Chrome browser will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

Asan Output:

==16674== ERROR: AddressSanitizer heap-use-after-free on address 0x7fac29a50d80 at pc 0x7fac593de0bf bp 0x7fff0087d610 sp 0x7fff0087d608  

READ of size 4 at 0x7fac29a50d80 thread T0  

#0 0x7fac593de0bf in \_ZN6chrome26ChromeContentBrowserClient28RequestMediaAccessPermissionEPKN7content18MediaStreamRequestERKN4base8CallbackIFvRKSt6vectorINS1\_17MediaStreamDeviceESaIS8\_EEEEE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/chrome\_content\_browser\_client.cc:1101  

#1 0x7fac5a9eff66 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#2 0x7fac5a9f07c8 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:470  

#3 0x7fac5a9f1ab9 in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:660  

#4 0x7fac5aa9a0f0 in \_ZN4base15MessagePumpGlib17RunWithDispatcherEPNS\_11MessagePump8DelegateEPNS\_21MessagePumpDispatcherE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_glib.cc:210  

#5 0x7fac5a9eeb2e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#6 0x7fac5a9f2972 in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:745  

#7 0x7fac5a3b54c0 in \_ZN22ChromeBrowserMainParts18MainMessageLoopRunEPi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/chrome\_browser\_main.cc:1858  

#8 0x7fac5f47183d in \_ZN7content15BrowserMainLoop23RunMainMessageLoopPartsEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_loop.cc:452  

#9 0x7fac5f473a57 in \_ZN12\_GLOBAL\_\_N\_121BrowserMainRunnerImpl3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_runner.cc:94  

#10 0x7fac5f46e1f6 in \_Z11BrowserMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main.cc:21  

#11 0x7fac5a9463dd in RunNamedProcessTypeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:282  

#12 0x7fac5a944cca in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:35  

#13 0x7fac593c1ff7 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#14 0x7fac593c1f4b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#15 0x7fac5282bc4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

0x7fac29a50d80 is located 0 bytes inside of 120-byte region [0x7fac29a50d80,0x7fac29a50df8)  

freed by thread T11 here:  

#0 0x7fac610ee2f2 in \_ZdlPv ??:0  

#1 0x7fac5f85fa48 in \_ZNSt8\_Rb\_treeISsSt4pairIKSsPN12media\_stream32MediaStreamDeviceSettingsRequestEESt10\_Select1stIS5\_ESt4lessISsESaIS5\_EE5eraseESt17\_Rb\_tree\_iteratorIS5\_E /usr/lib/gcc/x86\_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/stl\_tree.h:1345  

#2 0x7fac5a9eff66 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#3 0x7fac5a9f07c8 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:470  

#4 0x7fac5a9f1ab9 in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:660  

#5 0x7fac5a987292 in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:241  

#6 0x7fac5a9eeb2e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#7 0x7fac5a9ecd1f in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:745  

#8 0x7fac5aa6b63c in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:161  

#9 0x7fac5aa6125c in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:63  

#10 0x7fac610f3645 in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

previously allocated by thread T11 here:  

#0 0x7fac610ee172 in \_Znwm ??:0  

#1 0x7fac5f85bd56 in *ZN12media\_stream25MediaStreamDeviceSettings25RequestCaptureDeviceUsageERKSsiiRKNS\_13StreamOptionsES2* /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/media/media\_stream\_device\_settings.cc:127  

#2 0x7fac5a9eff66 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#3 0x7fac5a9f07c8 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:470  

#4 0x7fac5a9f1ab9 in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:660  

#5 0x7fac5a987292 in \_ZN4base19MessagePumpLibevent3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_libevent.cc:241  

#6 0x7fac5a9eeb2e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#7 0x7fac5a9ecd1f in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:745  

#8 0x7fac5aa6b63c in \_ZN4base6Thread10ThreadMainEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:161  

#9 0x7fac5aa6125c in \_ZN4base12\_GLOBAL\_\_N\_110ThreadFuncEPv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:63  

#10 0x7fac610f3645 in \_ZN6\_\_asan10AsanThread11ThreadStartEv ??:0  

Thread T11 created by T0 here:  

#0 0x7fac610ee473 in pthread\_create ??:0  

#1 0x7fac5aa60f09 in \_ZN4base12\_GLOBAL\_\_N\_112CreateThreadEmbPNS\_14PlatformThread8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:124  

#2 0x7fac5aa60e0a in \_ZN4base14PlatformThread6CreateEmPNS0\_8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:228  

#3 0x7fac5aa6af15 in \_ZN4base6Thread16StartWithOptionsERKNS0\_7OptionsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:72  

#4 0x7fac5f4710ad in \_ZN7content15BrowserMainLoop13CreateThreadsEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_loop.cc:418  

#5 0x7fac5f4736f6 in \_ZN12\_GLOBAL\_\_N\_121BrowserMainRunnerImpl10InitializeERKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_runner.cc:81  

#6 0x7fac5f46e1ab in \_Z11BrowserMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main.cc:17  

#7 0x7fac5a9463dd in RunNamedProcessTypeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:282  

#8 0x7fac5a944cca in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:35  

#9 0x7fac593c1ff7 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#10 0x7fac593c1f4b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#11 0x7fac5282bc4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

==16674== ABORTING  

Stats: 181M malloced (318M for red zones) by 1100611 calls  

Stats: 8M realloced by 34623 calls  

Stats: 151M freed by 988405 calls  

Stats: 71M really freed by 302805 calls  

Stats: 432M (110633 full pages) mmaped in 105 calls  

mmaps by size class: 8:753618; 9:49146; 10:28665; 11:10235; 12:6144; 13:5120; 14:768; 15:512; 16:320; 17:32; 18:64; 19:16; 20:4; 21:2; 22:3; 24:1;  

mallocs by size class: 8:986820; 9:55716; 10:33857; 11:11347; 12:6056; 13:5126; 14:730; 15:465; 16:373; 17:26; 18:69; 19:18; 20:2; 21:2; 22:3; 24:1;  

frees by size class: 8:885661; 9:51165; 10:32771; 11:10084; 12:5554; 13:1642; 14:650; 15:434; 16:343; 17:13; 18:65; 19:18; 20:1; 21:1; 22:2; 24:1;  

rfrees by size class: 8:250655; 9:25068; 10:21650; 11:3058; 12:1225; 13:391; 14:465; 15:63; 16:196; 17:10; 18:7; 19:12; 20:1; 21:1; 22:2; 24:1;  

Stats: malloc large: 121 small slow: 3561  

Shadow byte and word:  

0x1ff58534a1b0: fd  

0x1ff58534a1b0: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff58534a190: fd fd fd fd fd fd fd fd  

0x1ff58534a198: fd fd fd fd fd fd fd fd  

0x1ff58534a1a0: fa fa fa fa fa fa fa fa  

0x1ff58534a1a8: fa fa fa fa fa fa fa fa  

=>0x1ff58534a1b0: fd fd fd fd fd fd fd fd  

0x1ff58534a1b8: fd fd fd fd fd fd fd fd  

0x1ff58534a1c0: fa fa fa fa fa fa fa fa  

0x1ff58534a1c8: fa fa fa fa fa fa fa fa  

0x1ff58534a1d0: fd fd fd fd fd fd fd fd

## Attachments

- [test.html](attachments/test.html) (text/html; charset=us-ascii, 543 B)

## Timeline

### in...@chromium.org (2012-03-15)

This looks like a variant of http://code.google.com/p/chromium/issues/detail?id=116994 or seems like it wasn't fixed completely. 

I cannot reproduce it on trunk, Chamal, can you please retry with trunk ?

macourteau@, can you please take a closer look ?

### ma...@chromium.org (2012-03-15)

I'm hitting one of the DCHECK's I added in this CL (that has not been submitted yet) when I try the file:
http://codereview.chromium.org/9662016/

Looks like an issue in the WebRTC code. I've done a bit of digging, but someone from the WebRTC team really should look into this as I'm not familiar enough with that code to play around in it.

Here are my findings:
1. A new request gets created, and calls to AvailableDevices are posted to MediaStreamDeviceSettings for every media type requested, and for every pending request in the kRequested state (media_stream_manager.cc, MediaStreamManager::DeviceRequest::RequestState) but not yet in the kOpening state.
2. A new tab/window is created that requests access to camera/microphone, _or_ the page gets refreshed (which issues another request).
3. Since the 1st request is still in the kRequested state, AvailableDevices gets called for it again. This will happen every time access to devices is requested, unless that request has been answered (it might never be, if the user reloads the page).

I would suggest maybe adding a state (e.g. kPosted) that would go after kRequested and before kOpening, to make sure that AvailableDevices does not get called again once it has been called for all media types requested once.

mflodman@, perkj@: can one of you look into this, or forward the issue to the appropriate person? Can one of you also review the inflight CL mentioned above?

Thanks!

### [Deleted User] (2012-03-15)

Setting medium severity as this doesn't happen without settings changes.

### ch...@gmail.com (2012-03-16)

Inferno I can still reproduce. Is this reproducible in your PC?

### js...@chromium.org (2012-03-16)

If it's behind a flag for development then use SecImpacts-None rather than altering the severity.

Adding in WebRTC since the bug seems to be there. This is a critical, so it absolutely must be fixed before WebRTC ships. Fortunately beta and stable are not impacted in their default configurations.

### mf...@chromium.org (2012-03-16)

A fix is uploaded, awaiting review:
http://codereview.chromium.org/9703117/


### la...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### mf...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-03-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=127308

------------------------------------------------------------------------
r127308 | mflodman@chromium.org | Fri Mar 16 17:14:13 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/media/media_stream_manager.cc?r1=127308&r2=127307&pathrev=127308

Fixing reloading of media capture device page before approving usage.


BUG=118414
TEST=See bug info.


Review URL: http://codereview.chromium.org/9703117
------------------------------------------------------------------------

### in...@chromium.org (2012-03-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-03-20)

Is this issue eligible for a reward? :)

### sc...@gmail.com (2012-03-20)

It is certainly eligible to go to the panel :)

### sc...@gmail.com (2012-03-21)

@chamal.desilva: the panel has decided that this IS indeed eligible for a reward. Generally, the fact that this is an unstable feature in deep devlopment and hidden behind a flag (i.e. not ready) would lower or cancel any reward. It was however a use-after-free in the browser process, which is quite serious.

All things balanced out, $1000

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

### ch...@gmail.com (2012-03-21)

Thank you very much for the reward :)

### sc...@gmail.com (2012-03-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### bu...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/118414?no_tracker_redirect=1

[Multiple monorail components: Blink>WebRTC, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055039)*
