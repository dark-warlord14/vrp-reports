# Crash in WebCore::SMILTimeContainer::begin

| Field | Value |
|-------|-------|
| **Issue ID** | [40084717](https://issues.chromium.org/issues/40084717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-11-08 |
| **Bounty** | $1,000.00 |

## Description

Crashes on linux 32-bit dev [9.0.570.1 (Developer Build 64589)] and stable [7.0.517.44 (Oficjalna wersja 64615)]

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e72b70 (LWP 8205)]
0x00000000 in ?? ()
#0  0x00000000 in ?? ()
#1  0x01ae43af in WebCore::SMILTimeContainer::updateAnimations (this=0x332ad00, elapsed={static unresolvedValue = 1,7976931348623157e+308, static indefiniteValue = 3,4028234663852886e+38, m_time = 0}) at third_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:308
#2  0x01ae4a86 in WebCore::SMILTimeContainer::begin (this=0x332ad00) at third_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:103
#3  0x01a8392f in WebCore::SVGDocumentExtensions::startAnimations (this=0x340e460) at third_party/WebKit/WebCore/svg/SVGDocumentExtensions.cpp:98
#4  0x016d405a in WebCore::Document::implicitClose (this=0x33d0200) at third_party/WebKit/WebCore/dom/Document.cpp:2083
#5  0x01801ba4 in WebCore::FrameLoader::checkCallImplicitClose (this=0x33aea80) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:902
#6  0x0180805a in WebCore::FrameLoader::checkCompleted (this=0x33a9828) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:850
#7  0x01806f9b in WebCore::FrameLoader::finishedParsing (this=0x33a9828) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:784
#8  0x016d4616 in WebCore::Document::finishedParsing (this=0x33d0200) at third_party/WebKit/WebCore/dom/Document.cpp:4154
[...]


Repro file (crash1.xml):
----------
<html xmlns="http://www.w3.org/1999/xhtml">
    <body>
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <text>
                <textPath>
                    <tref xlink:href="#foo">
                        <animateColor attributeName="keyPoints"></animateColor>
                        <animateColor attributeName="xlink:href"></animateColor>
                    </tref>
                </textPath>
            </text>
        </svg>
    </body>
</html>
----------
If it doesn't crash instantly try to refresh few times.

registers:

eax            0x33aee00    54193664
ecx            0x0  0
edx            0x33aea80    54192768
ebx            0x2cedc24    47111204
esp            0xb1e7181c   0xb1e7181c
ebp            0xb1e719a8   0xb1e719a8
esi            0x2  2
edi            0x8  8
eip            0x0  0
eflags         0x210202 [ IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51

(Full backtrace attached - bt1.txt)


In one of cases (with bigger repro file) I got that backtrace:

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e1fb70 (LWP 6859)]
0x0375b823 in ?? ()
#0  0x0375b823 in ?? ()
#1  0x01ae4a86 in WebCore::SMILTimeContainer::begin (this=0x3425000) at third_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:103
#2  0x01a8392f in WebCore::SVGDocumentExtensions::startAnimations (this=0x374c550) at third_party/WebKit/WebCore/svg/SVGDocumentExtensions.cpp:98
#3  0x016d405a in WebCore::Document::implicitClose (this=0x370f200) at third_party/WebKit/WebCore/dom/Document.cpp:2083
#4  0x01801ba4 in WebCore::FrameLoader::checkCallImplicitClose (this=0x375a540) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:902
#5  0x0180805a in WebCore::FrameLoader::checkCompleted (this=0x33a9828) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:850
#6  0x01806f9b in WebCore::FrameLoader::finishedParsing (this=0x33a9828) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:784
[...]

I attached full backtrace of this case as bt2.txt. I'll try to put simple repro file later.

It think it can be exploitable.

## Attachments

- [bt1.txt](attachments/bt1.txt) (text/x-c++; charset=us-ascii, 19.5 KB)
- [bt2.txt](attachments/bt2.txt) (text/x-c++; charset=us-ascii, 18.2 KB)
- [crash1.xml](attachments/crash1.xml) (text/html; charset=us-ascii, 548 B)

## Timeline

### js...@chromium.org (2010-11-08)

Just gonna go ahead and flag this as high since the state makes it clear that it's an exec null, meaning it's almost certainly a stale c++ class.

### in...@chromium.org (2010-11-08)

Yeah the object is stale svg element.

### sl...@gmail.com (2010-11-09)

Few more backtraces with random(?) eip:

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e72b70 (LWP 18987)]
0x037ee94b in ?? ()

0x37ee94b:  0x00    0x80    0xdd    0xbb    0x04    0x10    0x00    0x00

#0  0x037ee94b in ?? ()
#1  0x01ae4a86 in WebCore::SMILTimeContainer::begin (this=0x32d3f00) at third_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:103
#2  0x01a8392f in WebCore::SVGDocumentExtensions::startAnimations (this=0x39e8280) at third_party/WebKit/WebCore/svg/SVGDocumentExtensions.cpp:98
#3  0x016d405a in WebCore::Document::implicitClose (this=0x37fa900) at third_party/WebKit/WebCore/dom/Document.cpp:2083
#4  0x01801ba4 in WebCore::FrameLoader::checkCallImplicitClose (this=0x37f0c40) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:902
#5  0x0180805a in WebCore::FrameLoader::checkCompleted (this=0x39bd828) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:850



Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e72b70 (LWP 18957)]
0x036752c3 in ?? ()

0x36752c3:  0x02    0x01    0x00    0x00    0x00    0x01    0x00    0x00

#0  0x036752c3 in ?? ()
#1  0x01ae4a86 in WebCore::SMILTimeContainer::begin (this=0x48d9380) at third_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:103
#2  0x01a8392f in WebCore::SVGDocumentExtensions::startAnimations (this=0x35658c0) at third_party/WebKit/WebCore/svg/SVGDocumentExtensions.cpp:98
#3  0x016d405a in WebCore::Document::implicitClose (this=0x34c4900) at third_party/WebKit/WebCore/dom/Document.cpp:2083
#4  0x01801ba4 in WebCore::FrameLoader::checkCallImplicitClose (this=0x3673a80) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:902


Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e72b70 (LWP 19179)]
0x03768eeb in ?? ()

0x3768eeb:  0x00    0x80    0xaf    0x53    0x03    0x10    0x00    0x00

#0  0x03768eeb in ?? ()
#1  0x01ae4a86 in WebCore::SMILTimeContainer::begin (this=0x39fd980) at third_party/WebKit/WebCore/svg/animation/SMILTimeContainer.cpp:103
#2  0x01a8392f in WebCore::SVGDocumentExtensions::startAnimations (this=0x371f320) at third_party/WebKit/WebCore/svg/SVGDocumentExtensions.cpp:98
#3  0x016d405a in WebCore::Document::implicitClose (this=0x3808900) at third_party/WebKit/WebCore/dom/Document.cpp:2083
#4  0x01801ba4 in WebCore::FrameLoader::checkCallImplicitClose (this=0x360f000) at third_party/WebKit/WebCore/loader/FrameLoader.cpp:902


I'm trying to reduce repro file of this case which I'll post when I'm done.


### in...@chromium.org (2010-11-09)

@slaweck, thank you very much for your detailed description and followup.

### in...@chromium.org (2010-11-09)

Fixed in http://trac.webkit.org/changeset/71686. will merge to 552.

### in...@chromium.org (2010-11-10)

merged to 552 in r71694.

### sc...@gmail.com (2010-11-10)

@slaweck: congratulations! You have provisionally qualified for a $1000 Chromium Security Reward.
We have rewarded above the base level because this is an excellent report. Thank you for the simple repro and the nice register / stack trace analysis.

How do you wish to be credited in our future release notes?

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

### sl...@gmail.com (2010-11-10)

Oh, it's great news :-) 
Thank You!

For credits just use my name: "Sławomir Błażek".

### sl...@gmail.com (2010-11-11)

Can You make a quick look at https://crbug.com/chromium/62806 to be sure it's not related to this one?
It's related to animations, at end of backtrace i see WebCore::SMILTimeContainer::begin() and it crashes on fixed 9.0.578.0 (Build 65638).

### sc...@gmail.com (2010-12-03)

@slawek: fix is live to all users! Thanks again; and e-mail cevans@chromium.org to get set up to collect the reward.

### sc...@gmail.com (2010-12-20)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/62401?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084717)*
