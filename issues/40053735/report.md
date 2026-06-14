# Stack-buffer-overflow at strcpy

| Field | Value |
|-------|-------|
| **Issue ID** | [40053735](https://issues.chromium.org/issues/40053735) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ao...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2012-02-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a stack buffer overflow (write of size 1) when the attached page is opened. The write is at offset 512 and the position seems to be controllable by changing the comment nesting level.

**VERSION**  

Chrome Version: 19.0.1040.0 (Developer Build 121661)  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**  

$ echo '<html lang=<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!--<!-->>>>>>>>>>>>>>>>>>>>>>>>>> •' > entryopen.html  

$ chrome-asan entryopen.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==17528== ERROR: AddressSanitizer stack-buffer-overflow on address 0x7fff48312020 at pc 0x7fd80ad15b64 bp 0x7fff48311b50 sp 0x7fff48311b38  

WRITE of size 1 at 0x7fff48312020 thread T0  

#0 0x7fd80ad15b64 in strcpy ??:0  

#1 0x7fd805211340 in entryOpen third\_party/icu/source/common/uresbund.c:0  

#2 0x7fd80520e515 in ures\_open\_46 ???:0  

#3 0x7fd8051202e6 in icu\_46::BreakIterator::buildInstance(icu\_46::Locale const&, char const\*, int, UErrorCode&) ???:0  

#4 0x7fd805120ddb in icu\_46::BreakIterator::makeInstance(icu\_46::Locale const&, int, UErrorCode&) ???:0  

#5 0x7fd805120b9c in icu\_46::BreakIterator::createInstance(icu\_46::Locale const&, int, UErrorCode&) ???:0  

#6 0x7fd80515d40f in ubrk\_open\_46 ???:0  

#7 0x7fd80726461c in WebCore::LineBreakIteratorPool::take(WTF::AtomicString const&) ???:0  

#8 0x7fd807263efa in WebCore::acquireLineBreakIterator(unsigned short const\*, int, WTF::AtomicString const&) ???:0  

#9 0x7fd808219e02 in WebCore::nextBreakablePosition(WebCore::LazyLineBreakIterator&, int, bool) ???:0  

#10 0x7fd807fb91f9 in WebCore::RenderBlock::LineBreaker::nextLineBreak(WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&, WebCore::LineInfo&, std::pair<WebCore::RenderText\*, WebCore::LazyLineBreakIterator>&, WebCore::RenderBlock::FloatingObject\*, unsigned int) ???:0  

#11 0x7fd807fa9fdc in WebCore::RenderBlock::layoutRunsAndFloatsInRange(WebCore::LineLayoutState&, WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&, WebCore::InlineIterator const&, WebCore::BidiStatus const&, unsigned int) ???:0  

#12 0x7fd807fa5bc5 in WebCore::RenderBlock::layoutRunsAndFloats(WebCore::LineLayoutState&, bool) ???:0  

#13 0x7fd807fbfa21 in WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) ???:0  

#14 0x7fd807f3c125 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) ???:0  

#15 0x7fd807f3a475 in WebCore::RenderBlock::layout() ???:0  

#16 0x7fd807f55a20 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox\*, WebCore::RenderBlock::MarginInfo&, int&, int&) ???:0  

#17 0x7fd807f4304b in WebCore::RenderBlock::layoutBlockChildren(bool, int&) ???:0  

#18 0x7fd807f3c141 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) ???:0  

#19 0x7fd807f3a475 in WebCore::RenderBlock::layout() ???:0  

#20 0x7fd807f55a20 in WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox\*, WebCore::RenderBlock::MarginInfo&, int&, int&) ???:0  

#21 0x7fd807f4304b in WebCore::RenderBlock::layoutBlockChildren(bool, int&) ???:0  

#22 0x7fd807f3c141 in WebCore::RenderBlock::layoutBlock(bool, int, WebCore::RenderBlock::BlockLayoutPass) ???:0  

#23 0x7fd807f3a475 in WebCore::RenderBlock::layout() ???:0  

#24 0x7fd8081f416f in WebCore::RenderView::layout() ???:0  

#25 0x7fd807a2ce0a in WebCore::FrameView::layout(bool) ???:0  

#26 0x7fd806c30137 in WebCore::Document::implicitClose() ???:0  

#27 0x7fd8078dfa56 in WebCore::FrameLoader::checkCompleted() ???:0  

#28 0x7fd8078dc348 in WebCore::FrameLoader::finishedParsing() ???:0  

#29 0x7fd806c4e0aa in WebCore::Document::finishedParsing() ???:0  

#30 0x7fd806f5ad93 in WebCore::HTMLDocumentParser::prepareToStopParsing() ???:0  

#31 0x7fd8078c1a14 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#32 0x7fd8078f8729 in WebCore::FrameLoader::finishedLoading() ???:0  

#33 0x7fd80791ef61 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#34 0x7fd808ffccf2 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#35 0x7fd8065a62aa in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#36 0x7fd8065a749b in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#37 0x7fd8065a3a6c in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#38 0x7fd8065a19f0 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#39 0x7fd8064aa08f in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#40 0x7fd806607679 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#41 0x7fd804de4c96 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#42 0x7fd804de54f6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#43 0x7fd804de67db in MessageLoop::DoWork() ???:0  

#44 0x7fd804df1217 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#45 0x7fd804de385e in MessageLoop::RunInternal() ???:0  

#46 0x7fd804de1a4f in MessageLoop::Run() ???:0  

#47 0x7fd809b8ba32 in RendererMain(content::MainFunctionParams const&) ???:0  

#48 0x7fd804d40906 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:0  

#49 0x7fd804d3f00a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#50 0x7fd803564837 in ChromeMain ??:0  

#51 0x7fd80356478b in main ???:0  

#52 0x7fd7fca5dc8d in \_\_libc\_start\_main /tmp/buildd/eglibc-2.11.3/csu/libc-start.c:260

Address 0x7fff48312020 is located at offset 512 in frame <entryOpen> of T0's stack:  

This frame has 8 object(s):  

[32, 36) 'intStatus'  

[96, 100) 'parentStatus'  

[160, 164) 'usrStatus'  

[224, 225) 'isDefault'  

[288, 289) 'isRoot'  

[352, 353) 'hasChopped'  

[416, 512) 'name'  

[544, 640) 'usrDataPath'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism  

(longjmp and C++ exceptions \*are\* supported)  

==17528== ABORTING  

Stats: 2M malloced (3M for red zones) by 10381 calls  

Stats: 0M realloced by 51 calls  

Stats: 0M freed by 3829 calls  

Stats: 0M really freed by 0 calls  

Stats: 40M (10246 full pages) mmaped in 10 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;  

mallocs by size class: 8:9276; 9:518; 10:246; 11:206; 12:44; 13:27; 14:48; 15:7; 16:7; 17:2;  

frees by size class: 8:3313; 9:178; 10:163; 11:107; 12:12; 13:12; 14:39; 15:4; 16:1;  

rfrees by size class:  

Stats: malloc large: 2 small slow: 54  

Shadow byte and word:  

0x1fffe9062404: f2  

0x1fffe9062400: 00 00 00 00 f2 f2 f2 f2  

More shadow bytes:  

0x1fffe90623e0: 01 f4 f4 f4 f2 f2 f2 f2  

0x1fffe90623e8: 01 f4 f4 f4 f2 f2 f2 f2  

0x1fffe90623f0: 01 f4 f4 f4 f2 f2 f2 f2  

0x1fffe90623f8: 00 00 00 00 00 00 00 00  

=>0x1fffe9062400: 00 00 00 00 f2 f2 f2 f2  

0x1fffe9062408: 00 00 00 00 00 00 00 00  

0x1fffe9062410: 00 00 00 00 f3 f3 f3 f3  

0x1fffe9062418: 00 00 00 00 00 00 00 00  

0x1fffe9062420: 00 00 00 00 00 00 00 00

## Attachments

- [entryopen.html](attachments/entryopen.html) (text/html; charset=us-ascii, 143 B)

## Timeline

### ts...@chromium.org (2012-02-15)

Hi jshin, this looks to be in ICU again.  There's some really sketchy looking stuff here:

static UResourceDataEntry *entryOpen(const char* path, const char* localeID, UErrorCode* status) {
...
    char name[96];
 ...
    uprv_strcpy(name, localeID);

where localeID came from passing ures_open's
    char canonLocaleID[100];

which is a mismatch even if were just being sloppy about maximum sizes.



### js...@chromium.org (2012-02-16)

We can fix ICU.  At the same time, it looks like we have to change WebKit to do some kind of sanity checking before setting webkit-locale to the input because 'lang' comes from a web page. 

### ts...@chromium.org (2012-02-16)

The lang attribute in the repro turns out to be 96 characters exactly.  The string length needs to be between 96 and 100 to trigger the issue.  When the string is over 100, ICU detects a bad parameter, returns NULL, and eventually segvs deref'ing it (harmless segv in that case).


### ts...@chromium.org (2012-02-16)

changing [96] to [100] in 3 places in icu/source/common/uresbund.c will solve the issue.  jshin, please do so if you get a chance.

Searching through the code, [100] is used as a common idiom instead of a sanely #define'd value, so this change makes things consistent.  Code like this makes me want to cry.

### js...@chromium.org (2012-02-16)

Thank you for the investigation. I feel like crying, too. :-) 
 I'll make a quick fix and file an upstream bug. 


### [Deleted User] (2012-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2012-02-16)

The sheer number of strcpy's throughout this code is terrifying. does someone want to do a quick pass and make sure there aren't similar conditions?

### bu...@chromium.org (2012-02-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=122360

------------------------------------------------------------------------
r122360 | jshin@chromium.org | Thu Feb 16 13:45:13 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/README.chromium?r1=122360&r2=122359&pathrev=122360
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/patches/uloc.patch?r1=122360&r2=122359&pathrev=122360
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/source/common/uresbund.c?r1=122360&r2=122359&pathrev=122360

Fix another buffer overflow bug in ICU

This is a 'hot' fix and a better patch will be made in the upstream and will be merged down later.  The investigation and the patch by tsepez.

BUG=114342
TEST=See the bug.
TBR=tsepez
Review URL: https://chromiumcodereview.appspot.com/9415012
------------------------------------------------------------------------

### bu...@chromium.org (2012-02-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=122362

------------------------------------------------------------------------
r122362 | jshin@chromium.org | Thu Feb 16 13:51:34 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=122362&r2=122361&pathrev=122362

Roll icu to 122360

For the actual change, see http://codereview.chromium.org/9415012

BUG=114342
TEST=See the bug. Or, go to http://www.i18nl10n.com/chrome/114342.html
TBR=tsepez
Review URL: https://chromiumcodereview.appspot.com/9419019
------------------------------------------------------------------------

### js...@chromium.org (2012-02-16)

Landed in the trunk. ICU roll to 122360 is landed in ToT @122362.  
M17 is not affeced, but M18 is. So, need to merge to M18. 

### in...@chromium.org (2012-02-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-02-16)

Just landed in M18 branch as well. (r22149) 


### ka...@google.com (2012-03-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

Few things make me happier than a regression catch :)
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

### sc...@gmail.com (2012-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=22149

------------------------------------------------------------------------
r22149 | jungshik@google.com | 2012-02-16T23:06:10.605988Z

------------------------------------------------------------------------

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

This issue was migrated from crbug.com/chromium/114342?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/114608]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053735)*
