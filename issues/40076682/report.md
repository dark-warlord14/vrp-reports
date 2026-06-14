# Use after free in SVG path

| Field | Value |
|-------|-------|
| **Issue ID** | [40076682](https://issues.chromium.org/issues/40076682) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ho...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2012-12-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome freezes and crashes when it tries to load the attached SVG file. It complains to free an invalid pointer.

**VERSION**  

Chrome Version: 23.0.1271.95 + stable  

Operating System: Ubuntu 12.04.1 LTS, 3.5.0-030500-generic, x86\_64 x86\_64 x86\_64 GNU/Linux

The test crashes the same way on Windows too.  

Chrome version: 23.0.1271.95 m  

Operating System: Windows Vista Business, Service Pack 2, 32bit

**REPRODUCTION CASE**  

<svg version="1.0" id="Layer\_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">  

<path style="fill:none;fill-opacity:1;fill-rule:evenodd;stroke:black;stroke-width:0.5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:0.5, 0.5;stroke-dashoffset:0;stroke-opacity:1" d="M 45218 338941 L 183827 657703 M 148855 124573 M 415041 540786 L 532666 376450 L 614937 57822 M 409096 551271 L 774605 872478 L 544948 37679 M 883890 9894 M 67716 667598 L 792171 142377 L 72355 757052 L 752729 485398 M 810552 632109 M 361822 463156 M 136427 335634 L 880582 632573 L 642467 253020 L 155277 48759 M 297655 680373 M 370010 437424 M 818816 190153 L 704 418321 M 362527 881478 M 498954 217111 L 97693 616727 L 259194 17829 L 173107 743113 L 423485 106686 L 407502 659588 M 193715 542147 M 612037 897545 M 493514 286805 L 270959 864556 L 629365 670483 M 647195 364835 L 107947 387632 M 531433 494319 M 392342 901822 L 95536 333571 M 707573 231116 L 517921 822714 L 687270 720029 L 390511 823445 L 539583 784131 L 75194 394726 M 207030 787069 M 998456 230473 M 332027 725646 M 563143 635112 M 81063 457825 M 869943 145094 L 461729 349802 M 425558 105148 L 968442 836752 M 363168 258286 M 150237 581642 M 380710 533 L 126997 385538 L 466601 199293 L 344388 653099 L 2900 253005 M 108048 162541 M 76490 999293 L 257578 218161 L 708530 970607 L 76962 966751 L 421297 383065 M 115106 719610 M 768205 602662 M 771105 855668 M 879154 18208 L 17500 567517 M 275079 785678 L 494208 955806 L 32767 920802 L 342099 324662 L 44272 231036 M 646934 399266 L 799172 875668 L 831312 538310 M 226614 813389 L 927688 487844 M 881739 512977 M 802541 454575 M 144639 779238 L 823510 151543 L 550809 823769 L 699436 493854 L 32164 198380 L 192016 969174 L 136791 654980 M 337177 457520 L 602160 426650 M 204004 250159 M 31258 720603 M 855028 693648 M 554463 187502 M 85210 219667 L 65220 742422 L 422282 948538 M 615120 285714 L 674476 553121 L 757126 939342 M 788385 659945 M 643412 353593 L 541096 169808 M 760763 720213 M 825984 462635 L 884917 885941 M 500036 171654 M 762569 846131 L 829876 419095 M 274433 207479 M 730614 850891 M 548396 48765 L 331851 706491 M 457509 532474 L 196918 785969 M 354805 286005 M 463652 48574 M 125621 500325 M 544716 891419 M 752195 942457 M 603086 347088 L 292816 400161 L 838578 441212 L 836124 728699 L 83503 811604 L 860178 868121 L 996634 217492 M 399580 969688 M 533140 572773 L 224624 834283 L 833589 453835 L 193465 485663 M 719064 602639 M 530668 172122 L 40242 397504 L 614997 3271 M 584685 197649 L 739117 184693 M 573399 799951 L 253786 239949 L 725612 866425 M 328251 43995 L 768723 87830 L 839180 577493 L 13949 365909 M 983547 523367 L 905449 352616 L 759604 221977 L 669229 461419 M 835545 789671 M 532528 290044 M 620358 830661 M 459538 408153 M 301989 422103 L 405650 47832 M 573891 953282 M 542082 449140 M 764060 184947 L 646367 163874 M 436037 606255 L 817360 421718 L 881257 964896 M 183245 386999 L 792649 925545 L 878826 120565 L 354093 672681 L 105969 159279 M 374802 595317 L 321398 707071 L 901762 479137 L 662382 230035 M 187717 22684 M 834360 389224 L 297846 265057 M 970528 777971 M 76496 937251 L 532567 601768 L 308839 225341 L 704478 575142 M 366860 805177 L 827861 656597 M 217085 593689 M 514931 858746 L 636716 81481 L 793538 13253 M 395306 640714 L 866056 692606 L 267747 380355 L 978686 491972 L 880909 117871 M 224770 632802 M 877651 118260 L 680216 298399 L 404933 147976 M 365432 852122 M 58037 766868 L 147223 708167 M 125908 200139 M 761191 81047 M 990162 305818 M 77878 183469 M 802312 142601 L 895272 542114 L 876298 871076 L 929114 662239 L 809462 555476 L 755615 953105 L 370471 686723 M 420640 764601 M 589069 566912 M 437713 667623 M 979827 173266 M 856124 44342 M 932661 973456 L 228355 774145 M 881964 709515 M 835069 406076 L 92799 70204 L 396155 215247 M 864707 652961 M 228531 632788 M 635604 488912 M 938048 421572 M 902731 201541 L 536988 393319 M 628049 228387 L 433927 885267 L 742667 22132 M 166979 886840 L 115370 561102 L 50013 833662 L 116661 591753 L 268628 210115 M 655019 838164 M 447486 393936 L 19913 743756 M 42045 19109 M 928885 947423 L 508524 25428 L 859090 484251 M 975752 76003 L 344631 913366 L 751529 874829 M 145465 558480 L 302235 855306 M 321344 97703 M 268767 599015 M 777292 624444 L 483534 460043 M 459286 536047 M 63055 880679 L 880329 734098 L 879563 121468 M 44941 423704 L 745049 60361 M 13816 659377 L 283820 545030 M 767355 5072 M 226641 541120 L 421798 544664 L 278761 540846 L 662315 736944 M 86018 699602 M 831068 759963 L 419339 413541 L 958571 762932 M 963644 255823 L 817919 986852 L 964709 228689 L 858281 799668 M 595225 2933 M 294826 458564 M 54789 302868 L 716409 565832 M 674980 328764 L 584587 344960 M 402505 331812 M 765088 296520 M 406431 802074 M 206099 969943 L 223829 46968 L 101758 970465 M 575888 686873 L 361853 133219 M 476 717807 L 120312 77753 M 885400 374273 L 176347 669365 M 146289 421508 L 468477 374559 L 345023 917526 M 31896 721981 L 855201 300280 M 573008 46221 L 123974 751899 L 264346 870552 L 368481 820884 M 75443 191002 L 869905 393930 L 540053 826922 L 220671 364612 L 937620 785855 M 630940 909830 L 408077 169228 M 82672 102939 M 903557 458158 L 281854 974139 L 769164 751895 M 596086 261306 L 625919 394824 M 563538 180679 L 90509 489519 M 498586 658747 M 581258 761686 L 219844 457177 L 431316 543837 M 200479 295731 M 796565 557037 M 613322 182955 M 44974 746494 L 940972 714524 M 345110 213110 L 794369 539562 L 759406 219677 L 650993 402392 M 851473 698124 L 255160 880419 M 438116 323754 M 184610 947770 L 662293 55072 M 875403 832948 z" id="path3602"></path>  

</svg>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

tcmalloc: large alloc 1204989952 bytes == 0x7f6622077000 @ 0x7f650029ac3f  

tcmalloc: large alloc 1506238464 bytes == 0x7f6669fe2000 @ 0x7f65002a12b7  

tcmalloc: large alloc 1882800128 bytes == 0x7f66c3f28000 @ 0x20656772616c203a  

tcmalloc: large alloc 5457698816 bytes == 0x7f6734644000 @ 0x1  

tcmalloc: large alloc 1819234304 bytes == 0x7f687a54a000 @ 0x7f65002a124a  

tcmalloc: large alloc 5457698816 bytes == 0x7f6734644000 @  

tcmalloc: large alloc 4548083712 bytes == 0x7f68e6fa7000 @  

third\_party/tcmalloc/chromium/src/tcmalloc.cc:285] Attempt to free invalid pointer 0x7f65002a38a2

## Attachments

- [chrome_snap_2_min.svg](attachments/chrome_snap_2_min.svg) (text/plain; charset=us-ascii, 5.5 KB)

## Timeline

### in...@chromium.org (2012-12-11)

Thanks hodovan.renata@ for the report.

Uploaded to ClusterFuzz to see it catches this use-after-free - https://cluster-fuzz.appspot.com/testcase?key=149968296

### fm...@chromium.org (2012-12-11)

Doesn't trigger on a ToT release ASAN build on Linux, but doesn't appear to work either (nothing is drawn).

OTOH, the Linux debug build runs out of memory:

tcmalloc: large alloc 1073745920 bytes == 0x7fc4cfd9d000 @  0x7fc56a4ab898 0x7fc56a4ab9aa 0x7fc56a4acb2f 0x7fc56a4ab69b 0x7fc56a4ac23d 0x7fc56a4ac31c 0x7fc56c06ba0d 0x7fc567de0b00 0x7fc567e7d393 0x7fc567e7d267 0x7fc567e7c176 0x7fc567e75461 0x7fc567e80bd7 0x7fc567e8195f 0x7fc567ee8826 0x7fc567e71286 0x7fc56342b862 0x7fc5631510df 0x7fc56314f897 0x7fc56312bc11 0x7fc56314fdb1 0x7fc56316268d 0x7fc56314bc60 0x7fc562b61486 0x7fc562b60ffd 0x7fc562b5c25e 0x7fc562b5b79e 0x7fc562d57098 0x7fc562d57690 0x7fc563bf18ce 0x7fc562df3833
tcmalloc: large alloc 2147487744 bytes == (nil) @  0x7fc56a4ab898 0x7fc56a4ab9aa 0x7fc56a4acb2f 0x7fc56a4ab69b 0x7fc56a4ac23d 0x7fc56a4ac31c 0x7fc56c06ba0d 0x7fc567de0b00 0x7fc567e7d393 0x7fc567e7d267 0x7fc567e7c176 0x7fc567e75461 0x7fc567e80bd7 0x7fc567e8195f 0x7fc567ee8826 0x7fc567e71286 0x7fc56342b862 0x7fc5631510df 0x7fc56314f897 0x7fc56312bc11 0x7fc56314fdb1 0x7fc56316268d 0x7fc56314bc60 0x7fc562b61486 0x7fc562b60ffd 0x7fc562b5c25e 0x7fc562b5b79e 0x7fc562d57098 0x7fc562d57690 0x7fc563bf18ce 0x7fc562df3833
[32281:32281:1211/090520:FATAL:process_util_linux.cc(726)] Out of memory.

Maybe the difference is due to ASAN builds disabling tcmalloc?

But something is definitely wrong if we're allocating GBs at a time and running out of mem.


### sc...@chromium.org (2012-12-11)

My guess is that this is related to the large coordinates. It's very simple otherwise.

### fm...@chromium.org (2012-12-11)

Right, seems that way, but the path-related structures should not depend on large values. There's either a nasty bug in path handling or we're allocation bitmaps for these (which could also qualify as a nasty bug :).

I'm tracing it now...

### ho...@gmail.com (2012-12-11)

It seems it's enough to keep the stroke and stroke-dasharray attributes from style to reproduce the crash. (I suspect it generates too many small dash fragments and  allocates memory for each of them.)

### sc...@chromium.org (2012-12-11)

Yep, that would be the cause. Either too many paths created for stroke outlines or precision issues in creating the dashes. That makes this a skia bug, really.

### fm...@chromium.org (2012-12-11)

Yup, we were looking at it with Mike and noticed the 0.5 dasharray :) That coupled with very long lines is what's causing the Skia path stroker to run out of memory as it tries to break the path into a gazillion pieces for dashing.

Not sure what the proper fix for memory exhaustion would look like short of imposing arbitrary limits or implementing dashing in a completely different manner.

But the attempted invalid free observed on Windows is probably still a valid security issue. I'm suspecting that once system memory is exhausted, random allocations start failing and some code doesn't handle that condition. It would be good to get the stack trace resolved to see exactly where that happens.

### fm...@chromium.org (2012-12-11)

Oh wait, there is no full stack trace :(

Renata, are you seeing that attempt to free invalid pointer consistently on Windows or is it hit and miss?

### ho...@gmail.com (2012-12-11)

The error message with invalid pointer and tcmalloc problems turns up every time if I run google-chrome from terminal on linux. On Windows the browser "just crashes" and I got the following message: 

[4132:7748:1211/170733:ERROR:gpu_info_collector_win.cc(91)] Can't retrieve a
 valid WinSAT assessment.
[4132:7748:1211/170740:ERROR:window_impl.cc(55)] Failed to unregister class Chro
me_WidgetWin_0. Error = 1412

But I'm not really familiar how to get a detailed trace on windows.

### fm...@chromium.org (2012-12-11)

Interesting, I'm seeing the tcmalloc warnings with ToT Linux builds, but we're crashing with an out of mem error instead of invalid free:

tcmalloc: large alloc 1073741824 bytes == 0x7f9dcbd9a000 @ 
tcmalloc: large alloc 2147483648 bytes == (nil) @  0x20656772616c203a
[21279:21279:1211/111110:FATAL:process_util_linux.cc(726)] Out of memory.

Maybe the allocation strategy changed since 23.0.1271.95, and now we're crashing instead of attempting to recover?


### ho...@gmail.com (2012-12-11)

Since we are experiencing different symptoms, I can add here how the error appears on my box. First, the 7 tcmalloc warnings are printed to the console, then the "rotating blueish circle icon" that shows that something is going on in the background stops rotating, and everything freezes. Finally, the free invalid pointer message appears on the console and the tab shows the "Aw, snap!" screen. Perhaps that helps...

### sc...@gmail.com (2012-12-11)

@hodovan.renata: I don't see the same behavior on my Linux x64 box. It does have a lot of memory, though!

My SVG tab remains blank. and I only get "large alloc" messages before things seem to calm down. This is with 23.0.1271.95.

Do you have crash reporting turned on? If so, do you have any crash IDs for the "invalid pointer" case in chrome://crashes ?

### ho...@gmail.com (2012-12-11)

Hmm... interesting. I always get the invalid pointer message. I start the browser and don't do anything else at all. Neither click on the "Kill" nor on the "Wait" button in the warning popup windwow. I'm just waiting. And when everything seems fine again (no rotating status icon, no more large alloc messages), then after a while comes the snap window and the invalid pointer message on the console.

Btw I'm not at my own PC right now and I cannot look for the crash ID, but I'll send it too ASAP.

### sc...@gmail.com (2012-12-11)

Thanks for the (pending) crash ID :)

How long does the sequence take for you from the start of the SVG load to the snap window?

### ho...@gmail.com (2012-12-11)

On linux it took pretty much time. At least 5 minutes (a coffee break :P )

### fm...@chromium.org (2012-12-11)

Thanks Renata. It is interesting that we're seeing three different symptoms:

* crash w/ invalid free
* crash w/ out-of-mem
* no crash

We understand what's causing the memory exhaustion, the only remaining mystery is this inconsistency.

I have some confirmation that the allocation strategy for dash segments has indeed changed not long ago, so it's possible that we're now crashing on allocation failures whereas 23 was maybe continuing and not handling the condition correctly.

Scarybeasts: are you trying this on an ASAN build? I have gobs of RAM too (64GB), and this is still crashing - but only with tcmalloc, not with ASAN builds.

### ho...@gmail.com (2012-12-12)

Crash ID c2eef9d082a2aea7

Occurred Wednesday, December 12, 2012 10:54:27 AM

### ho...@gmail.com (2012-12-12)

And it took ~6-7 minutes.

### sc...@gmail.com (2012-12-12)

The crash trace implies that keeping / moving the mouse in the SVG window is key to a repro.


Thread 0 *CRASHED* ( SIGSEGV @ 0x00000039 )

0x7fd9e4be8600	 [chrome]	 - third_party/tcmalloc/chromium/src/base/abort.cc:15]	tcmalloc::Abort
0x7fd9e4befe1b	 [chrome]	 - third_party/tcmalloc/chromium/src/internal_logging.cc:120]	tcmalloc::Log
0x7fd9e4be3902	 [chrome]	 - third_party/tcmalloc/chromium/src/tcmalloc.cc:285]	InvalidFree
0x7fd9e564b866	 [chrome]	 - third_party/skia/src/core/SkRegion_path.cpp:102]	SkRgnBuilder::~SkRgnBuilder
0x7fd9e564bc2b	 [chrome]	 - third_party/skia/src/core/SkRegion_path.cpp:327]	SkRegion::setPath
0x7fd9e5e29d84	 [chrome]	 - third_party/WebKit/Source/WebCore/platform/graphics/skia/SkiaUtils.cpp:155]	WebCore::SkPathContainsPoint
0x7fd9e5e26cb9	 [chrome]	 - third_party/WebKit/Source/WebCore/platform/graphics/skia/PathSkia.cpp:307]	WebCore::Path::strokeContains
0x7fd9e6865170	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGShape.cpp:113]	WebCore::RenderSVGShape::shapeDependentStrokeContains
0x7fd9e68556e8	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGPath.cpp:108]	WebCore::RenderSVGPath::shapeDependentStrokeContains
0x7fd9e6864e22	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGShape.cpp:142]	WebCore::RenderSVGShape::strokeContains
0x7fd9e6865018	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGShape.cpp:331]	WebCore::RenderSVGShape::nodeAtFloatPoint
0x7fd9e672b7d6	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/svg/RenderSVGRoot.cpp:434]	WebCore::RenderSVGRoot::nodeAtPoint
0x7fd9e6416348	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderObject.cpp:2545]	WebCore::RenderObject::hitTest
0x7fd9e63d60b6	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3744]	WebCore::RenderLayer::hitTestContents
0x7fd9e63ecbb5	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3698]	WebCore::RenderLayer::hitTestLayer
0x7fd9e63edf92	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3787]	WebCore::RenderLayer::hitTestList
0x7fd9e63ecad4	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3678]	WebCore::RenderLayer::hitTestLayer
0x7fd9e63ee0a7	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:3459]	WebCore::RenderLayer::hitTest
0x7fd9e647cc79	 [chrome]	 - third_party/WebKit/Source/WebCore/rendering/RenderView.cpp:95]	WebCore::RenderView::hitTest
0x7fd9e5812efc	 [chrome]	 - third_party/WebKit/Source/WebCore/dom/Document.cpp:3189]	WebCore::Document::prepareMouseEvent
0x7fd9e613ff23	 [chrome]	 - third_party/WebKit/Source/WebCore/page/EventHandler.cpp:2090]	WebCore::EventHandler::prepareMouseEvent
0x7fd9e614d5f9	 [chrome]	 - third_party/WebKit/Source/WebCore/page/EventHandler.cpp:1764]	WebCore::EventHandler::handleMouseMoveEvent
0x7fd9e614daaa	 [chrome]	 - third_party/WebKit/Source/WebCore/page/EventHandler.cpp:1686]	WebCore::EventHandler::mouseMoved
0x7fd9e57c20ee	 [chrome]	 - third_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:197]	WebKit::PageWidgetEventHandler::handleMouseMove
0x7fd9e57c1e7e	 [chrome]	 - third_party/WebKit/Source/WebKit/chromium/src/PageWidgetDelegate.cpp:118]	WebKit::PageWidgetDelegate::handleInputEvent
0x7fd9e5796e02	 [chrome]	 - third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1953]	WebKit::WebViewImpl::handleInputEvent
0x7fd9e7157385	 [chrome]	 - content/renderer/render_widget.cc:573]	RenderWidget::OnHandleInputEvent
0x7fd9e7152629	 [chrome]	 - ./ipc/ipc_message.h:170]	RenderWidget::OnMessageReceived
0x7fd9e7149a98	 [chrome]	 - content/renderer/render_view_impl.cc:1061]	RenderViewImpl::OnMessageReceived
0x7fd9e55765d1	 [chrome]	 - content/common/message_router.cc:47]	MessageRouter::RouteMessage
0x7fd9e550c952	 [chrome]	 - content/common/child_thread.cc:275]	ChildThread::OnMessageReceived

### in...@chromium.org (2012-12-13)

[Empty comment from Monorail migration]

### fm...@chromium.org (2012-12-13)

Thanks for the stack trace, I see the problem: if SkRgnBuilder::init() fails to allocate storage, it returns an error and the code tries to recover. But the destructor just assumes fStorage is valid and attempts to free it.

### in...@chromium.org (2012-12-13)

Isn't fStorage null when it fails to allocate ?

    fStorage = (SkRegion::RunType*)sk_malloc_flags(size.get32(), 0);
    if (NULL == fStorage) {
        return false;
    }

Why does this error comes for reporter.
"third_party/tcmalloc/chromium/src/tcmalloc.cc:285] Attempt to free invalid pointer 0x7f65002a38a2" instead of 0x0

### fm...@chromium.org (2012-12-13)

I suspect that it might be a different path - this particular crash trace indicates it is a NULL pointer issue: Thread 0 *CRASHED* ( SIGSEGV @ 0x00000039 )

Once we've exhausted the system memory, allocations may fail all over the place and I can imagine there are multiple sites that don't handle the condition gracefully.

Several angles here:

* fix the memory exhaustion root cause (dash-limiting patch in progress)
* fix this particular mishandled allocation failure (patch in progress)
* make all allocations crash on failure (something to consider)


### sc...@gmail.com (2012-12-13)

@fmalita: I don't think the stack trace indicates a NULL issue. The stack trace bounces through a frame called "InvalidFree" and the actual crash is in tcmalloc::Abort(). I believe it dereferences a pointer close to NULL as a way of doing a runtime assert / bail.

### fm...@chromium.org (2012-12-13)

@scarybeasts: you're right, the 0x39 address is hardcoded in tcmalloc::Abort.

Additionally, skia/ext/SkMemory_new_handler.cpp::sk_free() does guard against null pointers, so something more interesting must be going on.

### fm...@chromium.org (2012-12-17)

Landed a Skia CL to address the trigger for this (memory exhaustion): https://code.google.com/p/skia/source/detail?r=6845

I'm reluctant to mark the bug as fixed since we don't fully understand how we end up in an invalid free call, but OTOH I cannot repro it on any recent builds. Thoughts?

### in...@chromium.org (2012-12-26)

Can't reproduce anything on trunk, tried playing with mouse a lot too. Parts of SVG code get rewritten quite frequently, so it might be the case that this bug is already fixed on trunk. We can't proceed on this without being able to reproduce locally.

hodovan.renata@, can you please try with chrome canary and see if you can reproduce it there.

### ho...@gmail.com (2012-12-27)

@inferno: do you think of this version? : 
https://www.google.com/intl/en/chrome/browser/canary.html

I've reinstalled my laptop with Ubuntu 12.10 (64 bit) and I only installed a canary from the link above on it (64 bit too; without any addons).

This way I also could reproduce the use-after-free effect, but not so often (3-4 times from 10 tries). It seems it helps if you open other tabs and switch between them, but I'm still experiencing what are the certain circumstances what cause this symptom.

The crash id-s I get with this clean OS and canary:
e4027e881371eb03
08aec81c7a9213b5
33a6f3fb0adb4e09
54f08ad40827cb9a
48e0fef58808f7ee
de9c79da663c7f98
8a5c387016906f14
a6e5847995fd78e0

### in...@chromium.org (2012-12-27)

@hodovan.renata, thanks for confirming it on Ubuntu 12. We will take another look. Reopening bug.

### ho...@gmail.com (2012-12-28)

One more hint: I often get this crash if I left the test open in a tab and I'm surfing in other tabs. After a while (the processing of svg test seems done already) everything get slow and the tab with the SVG test crashes with invalid pointer use attempt.

### ho...@gmail.com (2013-01-07)

I've built a debug chrome and I cannot reproduce the use-after-free anymore. I guess it's fixed (or hidden) by fmalitas patch.The official stable and canary binaries I tested did not have this patch yet, that might be the reason why I could reproduce it after the fix too.

### in...@chromium.org (2013-01-07)

Ok, we will merge fmalita's patch.

### sc...@gmail.com (2013-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-29)

M25: Skia r7455

### sc...@gmail.com (2013-02-11)

@hodovan.renata: thanks for the report. I'm still not sure we got to the root cause here but your report did enable us to harden the area, so a $500 Chromium Security Reward has been issued!

### ho...@gmail.com (2013-02-11)

@scarybeasts: Thank you very much! :)

### sc...@gmail.com (2013-02-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/165432?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076682)*
