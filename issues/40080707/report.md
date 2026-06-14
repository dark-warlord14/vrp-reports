# Use-of-uninitialized-value in blink::Font::glyphDataAndPageForCharacter

| Field | Value |
|-------|-------|
| **Issue ID** | [40080707](https://issues.chromium.org/issues/40080707) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>Fonts, Blink>Layout |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fs...@opera.com |
| **Created** | 2014-10-24 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5913173990309888

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Font::glyphDataAndPageForCharacter
  unsigned int blink::SimpleShaper::advanceInternal<blink::Latin1TextIterator
  blink::SimpleShaper::advance
  

Minimized Testcase (9.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95QN2XWHHb3CCjIQXOsJIeUnUICgizmmdUORzkFklIv8r-fn-nBEQcftueMcHD-BKBE_FNsdCLNjlFrocSNSC72S68QcigmatajqjN75zOX6HhBXN5nMJsXAg9m0x3Kqy4JSMdfu48bbuY7TRpF2SWL0BHDDA

Filer: inferno

## Timeline

### in...@chromium.org (2014-10-24)

Author: ksakamoto@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/eba96ba04a10667f9063ecee4b66b1de9d3e3450
Time: Thu Apr 24 03:05:35 2014
The CL last changed line 112 of file GlyphPage.h, which is stack frame 1.

### ks...@chromium.org (2014-10-24)

Interesting. From the report it looks like Chrome was trying to draw a text with uninitialized content, but the string was created by numberToString, so it should be initialized. I have no idea what is wrong.

### cl...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2014-10-24)

It means we're walking off the end of the string.

I looked at all strings created here:

blink::RenderCounter::originalText() const /mnt/ssd/chromium/src/out_goma_msan/Release/../../third_party/WebKit/Source/core/rendering/RenderCounter.cpp:403

they're all unpoisoned in the range [start, start + length), so if there's an uninitialized character, it must come from [start + length, end of allocated block).

Additionally, the last string created at line 403 just before the crash happens has a length of 1. Looks like a bug in handing 1-byte strings?

### kc...@chromium.org (2014-10-24)

If #4 is correct, such bugs can also be found with asan with 
https://code.google.com/p/address-sanitizer/wiki/ContainerOverflow

Annotating blink is in our TODO, but if anyone wants to take it from us -- 
[s]he is more than welcome. 

### mb...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### ks...@chromium.org (2014-10-27)

Suspecting blink@183620
https://src.chromium.org/viewvc/blink?revision=183620&view=revision

fmalita@, could you take a look?


### cl...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### fm...@chromium.org (2014-10-27)

Doesn't look like a regression. Release-build assert:

ASSERTION FAILED: offset + length <= m_length
../../third_party/WebKit/Source/wtf/text/StringView.h(63) : void WTF::StringView::narrow(unsigned int, unsigned int)

Debug assert:

RenderView 0x27181e204010              	#document	0x13174da04010
  RenderBlock 0x27181e21c010           	HTML	0x13174da10120
    RenderBody 0x27181e21c110          	BODY	0x13174da10010
      RenderBR 0x27181e26c010          	BR	0x13174da10450
      RenderProgress 0x27181e230010    	PROGRESS	0x13174da50010 ID="el0" CLASS="c9"
        RenderBlock (positioned) 0x27181e21c310	<pseudo:after>	0x13174da500a0
*         RenderCounter 0x27181e2200d8
          RenderTextFragment 0x27181e250010
      RenderHTMLCanvas 0x27181e220010  	CANVAS	0x13174da70010 CLASS="c4" STYLE="height: 344px;"
ASSERTION FAILED: !needsLayout()
../../third_party/WebKit/Source/core/rendering/RenderObject.h(224) : void blink::RenderObject::assertRendererLaidOut() const
Received signal 11 SEGV_MAPERR 0000fbadbeef
#0 0x7f76dc46d23e base::debug::StackTrace::StackTrace()
#1 0x7f76dc46cd73 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#2 0x7f76ce6e8f90 <unknown>
#3 0x7f76d68f2475 blink::RenderObject::assertRendererLaidOut()
#4 0x7f76d68f084b blink::RenderObject::assertSubtreeIsLaidOut()
#5 0x7f76d68e3a9e blink::FrameView::layout()
#6 0x7f76d609afa8 blink::Document::updateLayout()
#7 0x7f76d609b1cc blink::Document::updateLayoutIgnorePendingStylesheets()
#8 0x7f76d685cdbc blink::VisiblePosition::canonicalPosition()
#9 0x7f76d685cbc1 blink::VisiblePosition::init()
#10 0x7f76d685cb73 blink::VisiblePosition::VisiblePosition()
#11 0x7f76d681b717 blink::InsertLineBreakCommand::doApply()
#12 0x7f76d67ce0bc blink::CompositeEditCommand::applyCommandToComposite()
#13 0x7f76d6859473 blink::TypingCommand::insertLineBreak()
#14 0x7f76d68599f8 blink::TypingCommand::doApply()
#15 0x7f76d67cde7d blink::CompositeEditCommand::apply()
#16 0x7f76d68593db blink::TypingCommand::insertLineBreak()
#17 0x7f76d68001de blink::executeInsertLineBreak()
#18 0x7f76d67fdb7b blink::Editor::Command::execute()
#19 0x7f76d60a711e blink::Document::execCommand()
#20 0x7f76d59b282f blink::DocumentV8Internal::execCommandMethod()
#21 0x7f76d59a98e4 blink::DocumentV8Internal::execCommandMethodCallback()
#22 0x7f76dd8fdd90 v8::internal::FunctionCallbackArguments::Call()
#23 0x7f76dd930c2d v8::internal::Builtin_HandleApiCall()


So things go south way before we start painting (tree not fully laid out after editing). Do you know an editor expert that could take a look at this?


### [Deleted User] (2014-10-27)

#5 - yes, container-overflow annotations would've helped here.

### fm...@chromium.org (2014-11-03)

+some folks who may have a clue about editing.

### fm...@chromium.org (2014-11-03)

+some folks who may have a clue about editing.

### cl...@chromium.org (2014-11-11)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### yo...@chromium.org (2014-11-11)

The trigger is editing/ but the root cause is in rendering. It seems some nodes missing dirty flag.

### fm...@chromium.org (2014-11-11)

Hmm, ok, but you agree that this is not a paint-time issue - right? Based on the debug assert trace, we're crashing before Editor::Command::execute() returns.

### cl...@chromium.org (2014-11-19)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-26)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-03)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-04)

ClusterFuzz has detected this issue as fixed in range 305960:306538.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5913173990309888

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Font::glyphDataAndPageForCharacter
  unsigned int blink::SimpleShaper::advanceInternal<blink::Latin1TextIterator
  blink::SimpleShaper::advance
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=305960:306538

Minimized Testcase (9.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95QN2XWHHb3CCjIQXOsJIeUnUICgizmmdUORzkFklIv8r-fn-nBEQcftueMcHD-BKBE_FNsdCLNjlFrocSNSC72S68QcigmatajqjN75zOX6HhBXN5nMJsXAg9m0x3Kqy4JSMdfu48bbuY7TRpF2SWL0BHDDA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-11)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-18)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-18)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 37 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

fmalita@: Uh oh! This issue is still open and hasn't been updated in the last 37 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-20)

ClusterFuzz has detected this issue as fixed in range 305960:306538.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5913173990309888

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::Font::glyphDataAndPageForCharacter
  unsigned int blink::SimpleShaper::advanceInternal<blink::Latin1TextIterator
  blink::SimpleShaper::advance
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=305960:306538

Minimized Testcase (9.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95QN2XWHHb3CCjIQXOsJIeUnUICgizmmdUORzkFklIv8r-fn-nBEQcftueMcHD-BKBE_FNsdCLNjlFrocSNSC72S68QcigmatajqjN75zOX6HhBXN5nMJsXAg9m0x3Kqy4JSMdfu48bbuY7TRpF2SWL0BHDDA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-12-20)

definitely fixed, confirmed twice by CF. maybe by this changeset in regression range.

commit	9e0d6c8c071f672cdf50b30adf942d86c3748e0e	
author	fs@opera.com <fs@opera.com>	Tue Dec 02 12:02:28 2014
committer	fs@opera.com <fs@opera.com>	Tue Dec 02 12:02:28 2014
Get rid of getCTM/setCTM pair in Font::paintGlyphsVertical

GC::setCTM is not safe to use in the presence of active recordings, since
it will end up accumulating the saved matrix on the currently active
SkCanvas. Use a GCSS to save/restore the CTM instead.

Review URL: https://codereview.chromium.org/748863004

git-svn-id: svn://svn.chromium.org/blink/trunk@186291 bbb929c8-8fbe-4397-9dbb-9b2b20218538
Source/platform/fonts/Font.cpp[diff]

### cl...@chromium.org (2014-12-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### fs...@opera.com (2014-12-22)

Based on the info in https://crbug.com/chromium/426762#c9 and the fuzzer report, I would suspect a rendering/ change. My (weak) counter-guess would be:

commit	10ead1fbccd4cbf4b822d9c5bd0a83885928eb03	
author	robhogan@gmail.com <robhogan@gmail.com>	Mon Dec 01 22:01:03 2014
committer	robhogan@gmail.com <robhogan@gmail.com>	Mon Dec 01 22:01:03 2014
Ensure layout on replaced elements in anonymous wrappers

When dimensions change on an ancestor we need to layout all the way down through
the percentage descendants. This means punching through any anonymous blocks that
sit between them. If a child is anonymous and its parent has a percentage height
then we need to layout that anonymous child so we can check for any percentage
children it is managing for the DOM parent.

BUG=414532

Review URL: https://codereview.chromium.org/764233002

git-svn-id: svn://svn.chromium.org/blink/trunk@186260 bbb929c8-8fbe-4397-9dbb-9b2b20218538

### in...@chromium.org (2014-12-22)

Yes might be. Since we can't verify without spending too much time and this is medium severity, we will let this roll into M41.

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### ti...@google.com (2015-01-22)

Congrats - $1000 for this report. Reward panel notes: "$500 for bug, +$500 ClusterFuzz bonus".

### ea...@chromium.org (2015-01-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-03-28)

Bulk update: removing view restriction from closed bugs.

### la...@google.com (2015-06-13)

[Empty comment from Monorail migration]

### la...@google.com (2015-06-13)

Attempting to remove dominik.rottsches@intel.com from cc.

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

This issue was migrated from crbug.com/chromium/426762?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Fonts, Blink>Layout]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080707)*
