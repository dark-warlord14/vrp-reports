# ASSERTION FAILED: positionOffset <= node->length()

| Field | Value |
|-------|-------|
| **Issue ID** | [40079733](https://issues.chromium.org/issues/40079733) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing, Blink>Layout |
| **Reporter** | rh...@partner.samsung.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2014-06-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Assertion check with security implication is firing with release ASAN chromium (the offset value is 1 but the length of the node is 0).

**VERSION**  

Chrome Version: 37.0.2045.0 (Developer Build 276470) (Blink @175949)  

Operating System: Ubuntu 13.10, x86\_64

**REPRODUCTION CASE**  

Load the following test case:

<head>
<script>
function dom\_manipulation() {
document.execCommand("selectAll", false, null);
document.execCommand("removeFormat" , true ,null);
}
</script>
 <style>
\\* {
text-transform:uppercase;
}
</style>
</head>
<body onload='dom\_manipulation()'>
<data></data>
<embed></embed>
<textarea autofocus>&#329</textarea>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

@sigbjornf is added to CC list since he changed the firing assertion to security assertion in r171165.

Backtrace:

# ASSERTION FAILED: positionOffset <= node->length() ../../third\_party/WebKit/Source/core/editing/FrameSelection.cpp(397) : WebCore::Position WebCore::updatePositionAfterAdoptingTextReplacement(const WebCore::Position &, WebCore::CharacterData \*, unsigned int, unsigned int, unsigned int) 1 0x7f450f2f7ca0 2 0x7f451065ac8c 3 0x7f451065a8df 4 0x7f450fea5772 5 0x7f450fea6b55 6 0x7f4510bbf7fc 7 0x7f4510bbf4e1 8 0x7f4510b747c4 9 0x7f4510b76a38 10 0x7f4510b62159 11 0x7f4510b5fdd8 12 0x7f4510b5d28f 13 0x7f4510b747c4 14 0x7f451067364c 15 0x7f4510b74099 16 0x7f451063c599 17 0x7f451064c3f3 18 0x7f45106460f6 19 0x7f450fcd6681 20 0x7f45117e7503 21 0x7f45117e00e7 22 0x7f450faea4d3 23 0x7f450f465a4d 24 0x7f450f45ef8c 25 0x7f44a63066ee ASAN:SIGSEGV

==16941==ERROR: AddressSanitizer: SEGV on unknown address 0x00009f7537dd (pc 0x7f451065ac96 sp 0x7f44c9f0cf40 bp 0x7f44c9f0cff0 T31)  

#0 0x7f451065ac95 in updatePositionAfterAdoptingTextReplacement /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/FrameSelection.cpp:397 (discriminator 2)  

#1 0x7f451065a8de in didUpdateCharacterData /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/FrameSelection.cpp:410  

#2 0x7f450fea5771 in setDataAndUpdate /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/CharacterData.cpp:184  

#3 0x7f450fea6b54 in deleteData /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/CharacterData.cpp:134  

#4 0x7f4510bbf7fb in insertText1AndTrimText2 /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/SplitTextNodeCommand.cpp:103  

#5 0x7f4510bbf4e0 in doApply /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/SplitTextNodeCommand.cpp:67  

#6 0x7f4510b747c3 in applyCommandToComposite /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/CompositeEditCommand.cpp:246  

#7 0x7f4510b76a37 in splitTextNode /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/CompositeEditCommand.cpp:440  

#8 0x7f4510b62158 in splitTextAtEnd /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/ApplyStyleCommand.cpp:1211  

#9 0x7f4510b5fdd7 in applyInlineStyle /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/ApplyStyleCommand.cpp:588  

#10 0x7f4510b5d28e in doApply /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/ApplyStyleCommand.cpp:214  

#11 0x7f4510b747c3 in applyCommandToComposite /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/CompositeEditCommand.cpp:246  

#12 0x7f451067364b in doApply /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/RemoveFormatCommand.cpp:96  

#13 0x7f4510b74098 in apply /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/CompositeEditCommand.cpp:205  

#14 0x7f451063c598 in removeFormattingAndStyle /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/Editor.cpp:578  

#15 0x7f451064c3f2 in executeRemoveFormat /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/EditorCommand.cpp:973  

#16 0x7f45106460f5 in execute /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/editing/EditorCommand.cpp:1687  

#17 0x7f450fcd6680 in execCommand /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4360  

#18 0x7f45117e7502 in execCommandMethod /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:5008  

#19 0x7f45117e00e6 in execCommandMethodCallback /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/gen/blink/bindings/core/v8/V8Document.cpp:5014  

#20 0x7f450faea4d2 in Call /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/arguments.cc:33  

#21 0x7f450f465a4c in HandleApiCallHelper<false> /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/builtins.cc:1208  

#22 0x7f450f45ef8b in Builtin\_HandleApiCall /b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../v8/src/builtins.cc:1224

## Attachments

- [crash.html](attachments/crash.html) (text/html, 348 B)

## Timeline

### in...@chromium.org (2014-06-12)

Sigbjornf@, can you please take a look.

### in...@chromium.org (2014-06-12)

This was found on CF as well. https://cluster-fuzz.appspot.com/testcase?key=5153273923239936

### cl...@chromium.org (2014-06-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5153273923239936

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_chrome_v8_arm

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  - crash stack -
  WebCore::updatePositionAfterAdoptingTextReplacement
  WebCore::FrameSelection::didUpdateCharacterData
  WebCore::CharacterData::setDataAndUpdate
  

Minimized Testcase (4.86 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97FDmU7zc4Y1iXqWMSpCXiv8dKlQWkj4LNe58Bp-yzoGGRPT5_eYfMyyGm4fVN39SXMNa7cjDnwKLxxs5XAeoNUPjAMrb7aeyxSOIwBZ4Pp8F7EqfAuStadFu4Lg1W08VDOrpic36KocDR-jjopHpimYHAZ2g



### ts...@chromium.org (2014-06-12)

Marking impacts beta/stable based on CF regression range starting at 0.

### cl...@chromium.org (2014-06-12)

[Empty comment from Monorail migration]

### yo...@chromium.org (2014-06-13)

I hit assertion on Win syzyasan:

ASSERT_AT(false, m_file, m_line, "");

This is caused by throwing an exception in Range::checkNodeWOffset(),
where |n| is |Text| node, "\u0149"=&#329 length=1, offset=2


blink_web.dll!WebCore::NoExceptionStateAssertionChecker::throwDOMException(const int & __formal, const WTF::String & __formal) Line 45 C++
blink_web.dll!WebCore::Range::checkNodeWOffset(WebCore::Node * n, int offset, WebCore::ExceptionState & exceptionState) Line 992 C++
blink_web.dll!WebCore::Range::setEnd(WTF::PassRefPtr<WebCore::Node> refNode, int offset, WebCore::ExceptionState & exceptionState) Line 194 C++
blink_web.dll!WebCore::Range::Range(WebCore::Document & ownerDocument, WebCore::Node * startContainer, int startOffset, WebCore::Node * endContainer, int endOffset) Line 94 C++
blink_web.dll!WebCore::Range::create(WebCore::Document & ownerDocument, WebCore::Node * startContainer, int startOffset, WebCore::Node * endContainer, int endOffset) Line 99 C++
blink_web.dll!WebCore::TextIterator::range() Line 1176 C++
blink_web.dll!WebCore::TextIterator::node() Line 1188 C++
blink_web.dll!WebCore::nextBoundary(const WebCore::VisiblePosition & c, unsigned int (const wchar_t *, unsigned int, unsigned int, WebCore::BoundarySearchContextAvailability, bool &) * searchFunction) Line 571 C++
blink_web.dll!WebCore::endOfWord(const WebCore::VisiblePosition & c, WebCore::EWordSide side) Line 674 C++
blink_web.dll!WebCore::SpellChecker::respondToChangedSelection(const WebCore::VisibleSelection & oldSelection, unsigned int options) Line 725 C++
blink_web.dll!WebCore::Editor::respondToChangedSelection(const WebCore::VisibleSelection & oldSelection, unsigned int options) Line 1291 C++
blink_web.dll!WebCore::FrameSelection::setSelection(const WebCore::VisibleSelection & newSelection, unsigned int options, WebCore::FrameSelection::CursorAlignOnScroll align, WebCore::TextGranularity granularity) Line 287 C++
blink_web.dll!WebCore::HTMLTextFormControlElement::setSelectionRange(int start, int end, WebCore::TextFieldSelectionDirection direction) Line 315 C++
blink_web.dll!WebCore::HTMLTextFormControlElement::restoreCachedSelection() Line 474 C++
blink_web.dll!WebCore::HTMLTextAreaElement::updateFocusAppearance(bool restorePreviousSelection) Line 248 C++
blink_web.dll!WebCore::Element::focus(bool restorePreviousSelection, WebCore::FocusType type) Line 2120 C++
blink_web.dll!WebCore::AutofocusTask::performTask(WebCore::ExecutionContext * context) Line 376 C++
blink_web.dll!WebCore::MainThreadTaskRunner::perform(WTF::PassOwnPtr<WebCore::ExecutionContextTask> task) Line 88 C++
blink_web.dll!WebCore::PerformTaskContext::didReceiveTask(void * untypedContext) Line 62 C++
content.dll!base::internal::RunnableAdapter<void (__cdecl*)(void *)>::Run(void * const & a1) Line 171 C++
content.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void * const &)>::MakeItSo(base::internal::RunnableAdapter<void (__cdecl*)(void *)> runnable, void * const & a1) Line 872 C++
content.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void *),void __cdecl(void *)>,void __cdecl(void *)>::Run(base::internal::BindStateBase * base) Line 1169 C++
base.dll!base::Callback<void __cdecl(void)>::Run() Line 401 C++
base.dll!base::MessageLoop::RunTask(const base::PendingTask & pending_task) Line 452 C++
base.dll!base::MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task) Line 465 C++
base.dll!base::MessageLoop::DoWork() Line 576 C++
base.dll!base::MessagePumpForUI::DoRunLoop() Line 218 C++
base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher) Line 65 C++
base.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate) Line 47 C++
base.dll!base::MessageLoop::RunHandler() Line 400 C++
base.dll!base::RunLoop::Run() Line 50 C++
base.dll!base::MessageLoop::Run() Line 294 C++
base.dll!base::Thread::Run(base::MessageLoop * message_loop) Line 173 C++
base.dll!base::Thread::ThreadMain() Line 225 C++
base.dll!base::`anonymous namespace'::ThreadFunc(void * params) Line 78 C++


### yo...@chromium.org (2014-06-13)

yutak@, It seems this is TextIterator issue. TextIterator::range() calls Range::create with wrong text offset.

It seems this is caused by U+0149 (Latin small Letter N preceded by Apostrophe)
http://www.marathon-studios.com/unicode/U0149/Latin_Small_Letter_N_Preceded_By_Apostrophe
when I replaced &#329; to "x", it works.

It seems upper case transformation make "'N" Apostrophe + "N".

Here is JS results:

"\u0149".toUpperCase() => "
"\u0149".toLocaleUpperCase() => "ʼN"


Here is hand minimize test case:

<!DOCTYPE html>
<html>
<head>
<script>
onload = function() {
    document.execCommand('SelectAll');
    document.execCommand('RemoveFormat');
}
</script>
<style>
* { text-transform: uppercase; }
</style>
</head>
<body>
<textarea autofocus>&#329;</textarea>
</body>
</html>




### yo...@chromium.org (2014-06-13)

Since, TextIterator::handleTextNode() and TextIterator::handleTextBox() iterator over RenderText, fix for this isn't easy...

### yo...@chromium.org (2014-06-13)

Characters marked "F" in below table indicates case folding changes number of characters: ftp://ftp.unicode.org/Public/UCD/latest/ucd/CaseFolding.txt

Note: It seems some character don't follow this table in V8, e.g. spec says U+1F88 to U+1F00 U+03B9, but V8 "\u1F88".toLowerCase() yield "\u1F80".

### cl...@chromium.org (2014-06-21)

[Comment Deleted]

### cl...@chromium.org (2014-06-23)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-06-23)

yutak@ - Is this still on track for M36? Grateful for an update.

### yo...@chromium.org (2014-06-26)

TextIterator iterates over rendered text rather than text in Text node.
On this issue, rendered text is different from text in Text Node. We need to map rendered text to text in Text node to consider one character in Text node mapped to two characters in rendered text.

### yo...@chromium.org (2014-06-26)

esprenh@, jshin@, Could you shed light to this issue? Fundamental cause is RenderText and Text have different characters, 
 - RenderText=\u02BC \u004E
 - Text=\u0149
This is cause by CSS text-transform: uppercase.
Note: https://crbug.com/chromium/388382 has an example of text-transform: lowercase. However, I couldn't find lowecase mapping to yield two characters in Unicode table.

So, we need to have offset mapping table between rendered text and text. This isn't only TextIterator but also document.caretRangeFromPoint and RenderObject::hitTest.

Any idea?


### cl...@chromium.org (2014-07-04)

[Comment Deleted]

### mb...@chromium.org (2014-07-09)

esprehn@, jshin@: Have either of you had a chance to look at this?

### cl...@chromium.org (2014-07-12)

[Comment Deleted]

### cl...@chromium.org (2014-07-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6754675292372992

Fuzzer: Bj_broddelwerk
Job Type: Mac_asan_chrome

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  - crash stack -
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  blink::CharacterData::setDataAndUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=262830:262871

Minimized Testcase (12.08 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97RgMsR_LqoeTvcUkhHxYNKiAkcEBo2epRv2tU2AN4Cs7GWVY2yLom1GEDh6gunXsrJv5lTXkMB31HbVlhFFVrn19bu-L7Lk2AWf_Vah1u882GAuQ2QOt_CYOGh5o6VadqDE9UicXFyGwy4B4zdcRjylrSeHQ
Filer: inferno@chromium.org

### cl...@chromium.org (2014-07-21)

[Comment Deleted]

### es...@chromium.org (2014-07-24)

I haven't had a chance to look at this..

@yosin why are we mapping between the RenderText value and the Text value at all? Why does editing need to do that?

### es...@chromium.org (2014-07-24)

leviw@ Could you look into this? I suspect the TextIterator wants to either operate on the RenderText values or the Text values, and not be trying to take offsets from one and index into the other.

### cl...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-03)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-11)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-12)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### le...@chromium.org (2014-08-12)

I'm working on the CY so I don't expect to get to this soon. Seeing if JWW can get to this in the meantime.

### jw...@chromium.org (2014-08-21)

I am not going to be able to tackle this before I hit a vacation shortly, so I'm going to unassign myself.

### jw...@chromium.org (2014-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-22)

yosin: Can you please take a look or find someone else to own it.

You are auto-assigned this issue since you are the top fixer for area label 'Cr-Blink-Editing'.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-08-22)

@yosin: 
> So, we need to have offset mapping table between rendered text and text. This isn't > only TextIterator but also document.caretRangeFromPoint and RenderObject::hitTest.

Sorry for the delayed reply (I've not recovered from my email backlog after a long vacation). Anyway, I don't see any way around other than what you have suggested above because case-folding is not 1:1. 

re: https://crbug.com/chromium/383777#c9

> Characters marked "F" in below table indicates case folding changes number of 
> characters: ftp://ftp.unicode.org/Public/UCD/latest/ucd/CaseFolding.txt

> Note: It seems some character don't follow this table in V8, e.g. spec says U+1F88 > to U+1F00 U+03B9, but V8 "\u1F88".toLowerCase() yield "\u1F80".

CaseFolding.txt has two entries for U+1F88, Full casefolding ("F") and Simple case-folding ("S"). V8 appears to use a simple case-folding. 

1F88; F; 1F00 03B9; # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
1F88; S; 1F80; # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI



### yo...@chromium.org (2014-09-08)

Rendering API should return DOM text offset rather than rendered text offset to out side of rendering layer.

### pa...@chromium.org (2014-09-08)

Hi, we really need someone to nail down this bug. It's Security_Severity-High and getting pretty long in the toof. yosin, can you please, or delegate?

### in...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6512254007640064

### cl...@chromium.org (2014-09-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6512254007640064

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  blink::CharacterData::setDataAndUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=262987:263028

Minimized Testcase (0.29 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95RaRr2Dj9Sj9FVt3qSfEIlUpzdAD6fMt7o_-Rl9fx1KHuiJAx6CZgCLdu768VlEK3VDTBXaA_vn10eeq1IC5UYLCZfG9Uc4m1RC4tMmrCwo8xspfNT0qgbJXHfVsoDRTOl120n3gHNfDo1PYDUZw40M-YmMA
<script>
    function dom_manipulation() {
      document.execCommand("selectAll", null);
      document.execCommand("removeFormat" , true ,null);
    }
  </script>

  <style>
    * {
      text-transform:uppercase;
</style>
<body onload='dom_manipulation()'>  
  <embed><textarea autofocus>&#329




### oj...@chromium.org (2014-10-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6655057624825856

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  blink::CharacterData::setDataAndUpdate
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96XBZ7Zxg9EABGc3DWPzo2rUFoy7ecL22ZLw01r553hqwvke33WgVmGia5h3dXA5ovxl45h46HkfP4GV3VcgmSjhffI3i7un6FWsiRHEr5l1QYc905hv9bTP70EBO2BvKlDKh_YupwO3QewK7NsmVqnse6jGA


Filer: inferno

### cl...@chromium.org (2014-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6655057624825856

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  blink::CharacterData::setDataAndUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=262987:263028

Minimized Testcase (7.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv971Ns78EQK8dEPgkN2fCvDc9uC6_FZXvPZ6Nt7lTzHtjrISK4FoJg8Mr0GZmfS8nzLiK4ayiSGSwUVU7sOeej4Q9ndp5ZuDC4eNmwYbi69UxWCM8X6eD1mcYZApGeoKULEa2mIdGtM-znMUyglc70a9axu9Rg



### rh...@partner.samsung.com (2014-11-28)

[Empty comment from Monorail migration]

### zh...@partner.samsung.com (2014-12-02)

The following simple test also crash when you start typing in the text box:

<head>
  <style>
    * { text-transform:uppercase; }
  </style>
</head>
<body>
<textarea>&#329</textarea>

Reason: codepoint 329 is an interesting character:

http://codepoints.net/U+0149

Its uppercase and titlecase are constructed from two characters: N + MODIFIER LETTER APOSTROPHE. However, the lowercase is a single character. Firefox is very clever, since it supports extended grapheme clusters (heh, this knowledge is coming from developing a regex engine). However, the textarea in Blink splits the uppercase form into two characters.

The unicode standard says this:

It is important to recognize that what the user thinks of as a “character”—a basic unit of a writing system for a language—may not be just a single Unicode code point.

Source: http://www.unicode.org/reports/tr29/#Grapheme_Cluster_Boundaries


### zh...@partner.samsung.com (2014-12-04)

This bug worth looking at.

I know now that the dom/Text object keep the original (non-uppercase) content, but the RenderText object has the uppercase version created by the RenderText::applyTextTransform. I suspect the frame->selection() is coming from the RenderText. But the RenderText has a different (uppercase) version of the content, so its offsets are not valid. Perhaps positionInsideTextNode should be made more clever, but this is only one part of the problem.

1) The offsets computed by RenderText (e.g. nextOffset) uses its own m_text. This is incorrect, since m_text is a transformed text.

2) The selection also depends on the transformed m_text of the RenderObject. Obviously this is also incorrect.

I am not sure how can we fix that, but it would be a big change.


### zh...@partner.samsung.com (2014-12-05)

Today I confirmed again that what I told you yesterday is correct.

This exploit cannot be usable, because CharacterData::insertData throws an exception if "offset > length()". This exception is not visible, since InsertIntoTextNodeCommand::doApply() pass IGNORE_EXCEPTION.

Hence if type at the end of the following textbox:

<textarea style="text-transform:uppercase">&#223</textarea>

Nothing happens. 223 is the codepoint of german sharp S, turned to SS. If you type something after the first S, it appears at the end (after the two SS).

You can do other funny things:

<p style="text-transform:uppercase">&#223m</p>

You see SSM on the screen, you can select it and copy it onto the clipboard. However, after you insert it into an editor, only two SS appears. You can "protect" your text :D

Fixing it is difficult, but somebody should do it, because FireFox handles these cases very nicely. Basically we need to maintain an offset vector, which tells the starting position of the characters in the original stream if a transformation is applied.

We need to use this vector for previousOffset/previousOffsetForBackwardDeletion/nextOffset/positionForPoint and likely in other functions, editing needs to be aware of it, etc. This is a huge work. Considering the review activity of Blink, you will not even get a review if you are not a Google dev. So this is not a task for me. But I hope the detailed description might help someday.


### js...@chromium.org (2014-12-17)

To resolve the security issue (since the bigger fix seems far more complicated) can we just clamp the position offset within range of the text node it's created from?

### cl...@chromium.org (2014-12-18)

ClusterFuzz has detected this issue as fixed in range 275840:275883.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5153273923239936

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_chrome_v8_arm

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  WebCore::updatePositionAfterAdoptingTextReplacement
  WebCore::FrameSelection::didUpdateCharacterData
  WebCore::CharacterData::setDataAndUpdate
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=275840:275883

Minimized Testcase (44.36 Kb): https://cluster-fuzz.appspot.com/download/AMIfv947ttQ4hQxewRvvOkfKwXkFUIKRIvw3Y9COnivb1fzz19rpKhH5HkbRpXh_wQ6EMplHiVYnL58Gp9-6HKct7T_5m3xTZxsWNdsXG6DbVZsYI3OVgzMi7CZQFSgvcZtFDbbG67hRgIHc4jcVHNgNuRIsbZjNa4FKMzzDQTiTQZRIGETKnAU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-18)

ClusterFuzz has detected this issue as fixed in range 275840:275883.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5153273923239936

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_chrome_v8_arm

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  WebCore::updatePositionAfterAdoptingTextReplacement
  WebCore::FrameSelection::didUpdateCharacterData
  WebCore::CharacterData::setDataAndUpdate
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=275840:275883

Minimized Testcase (44.36 Kb): https://cluster-fuzz.appspot.com/download/AMIfv947ttQ4hQxewRvvOkfKwXkFUIKRIvw3Y9COnivb1fzz19rpKhH5HkbRpXh_wQ6EMplHiVYnL58Gp9-6HKct7T_5m3xTZxsWNdsXG6DbVZsYI3OVgzMi7CZQFSgvcZtFDbbG67hRgIHc4jcVHNgNuRIsbZjNa4FKMzzDQTiTQZRIGETKnAU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-18)

ClusterFuzz has detected this issue as fixed in range 275840:275883.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5153273923239936

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_chrome_v8_arm

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  WebCore::updatePositionAfterAdoptingTextReplacement
  WebCore::FrameSelection::didUpdateCharacterData
  WebCore::CharacterData::setDataAndUpdate
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=275840:275883

Minimized Testcase (44.36 Kb): https://cluster-fuzz.appspot.com/download/AMIfv947ttQ4hQxewRvvOkfKwXkFUIKRIvw3Y9COnivb1fzz19rpKhH5HkbRpXh_wQ6EMplHiVYnL58Gp9-6HKct7T_5m3xTZxsWNdsXG6DbVZsYI3OVgzMi7CZQFSgvcZtFDbbG67hRgIHc4jcVHNgNuRIsbZjNa4FKMzzDQTiTQZRIGETKnAU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-18)

ClusterFuzz has detected this issue as fixed in range 275840:275883.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5153273923239936

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_chrome_v8_arm

Crash Type: UNKNOWN
Crash Address: 0xfbadbeef
Crash State:
  WebCore::updatePositionAfterAdoptingTextReplacement
  WebCore::FrameSelection::didUpdateCharacterData
  WebCore::CharacterData::setDataAndUpdate
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=275840:275883

Minimized Testcase (44.36 Kb): https://cluster-fuzz.appspot.com/download/AMIfv947ttQ4hQxewRvvOkfKwXkFUIKRIvw3Y9COnivb1fzz19rpKhH5HkbRpXh_wQ6EMplHiVYnL58Gp9-6HKct7T_5m3xTZxsWNdsXG6DbVZsYI3OVgzMi7CZQFSgvcZtFDbbG67hRgIHc4jcVHNgNuRIsbZjNa4FKMzzDQTiTQZRIGETKnAU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-12-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4779553380630528

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_content_shell_drt

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: positionOffset <= node->length()
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_content_shell_drt&range=262987:263028

Minimized Testcase (8.90 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95TFoutpr95fjK0PBxgCpVg9XXf6sRJ8esaCkDCPhYyWE-n_ZZbG-MtHvs8N41-JUNSBUgNNZDDklaoKDlcA-NtsfL00frsrF1KKnhZplX1Gxv7AQv_C6ojFCPSGUCj9btnn5CHo8DvJQ9JOzNU2ZHqTKAjyw

Filer: inferno

### in...@chromium.org (2014-12-18)

See latest testcase from c#49, which still reproduces on trunk.

Author: yurys@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/071e3d587af73642b265d1ee48aa743c68ca3720
Time: Thu Apr 10 07:41:11 2014
Lines 141 of file CharacterData.cpp which potentially caused crash are changed in this cl (frame #3, "blink::CharacterData::deleteData").
Minimum distance from crash line to modified line: 0. (file: CharacterData.cpp, crashed on: 141, modified: 141).

### yu...@chromium.org (2014-12-19)

I just added initialization to 0 of the vars. Assigning to sigbjornf - author of the change that causes compile failure.

### [Deleted User] (2014-12-19)

It is a contenteditable issue, I merely added the release assert as part of clearing away some other security bug. Not my territory.

### cl...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-12-23)

Adding some friends in the hope that someone can help identify an owner or an interim solution (still wondering if clamping is an option).

### cl...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-01-06)

Post-holiday ping, anyone got ideas for who could be an owner? :)

### jw...@chromium.org (2015-01-06)

szager@, does this fall under your purview these days?

### in...@chromium.org (2015-01-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### in...@chromium.org (2015-01-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-09)

[Empty comment from Monorail migration]

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### zh...@partner.samsung.com (2015-01-13)

Again, this is not a security bug, because there are internal checks, which captures these events and throws errors. These errors are ignored, so users only see strange behaviour. That is all.

There will be no simple fix for this, since a large amount of code needs to be rewritten. The text known by renderer is a transformed text, and the assumption of every character is mapped to another single character is simply false in unicode. So the positions determined by the renderer cannot be used as positions in the dom text.


### bu...@chromium.org (2015-01-13)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188326

------------------------------------------------------------------
r188326 | szager@chromium.org | 2015-01-13T21:06:08.751415Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/FrameSelection.cpp?r1=188326&r2=188325&pathrev=188326

Clamp text range offsets to the length of the Text node.

Due to case folding, RenderText length will not necessarily be the
same as Text length.  A correct fix would entail mapping character
offsets between the RenderText and Text.  This change just prevents
using an offset beyond the end of the Text.

BUG=383777
R=eae@chromium.org,yosin@chromium.org

Review URL: https://codereview.chromium.org/853533003
-----------------------------------------------------------------

### in...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-14)

ClusterFuzz has detected this issue as fixed in range 311294:311376.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4779553380630528

Fuzzer: Bj_broddelwerk
Job Type: Linux_asan_content_shell_drt

Crash Type: ASSERT
Crash Address: 
Crash State:
  ASSERTION FAILED: positionOffset <= node->length()
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_content_shell_drt&range=262987:263028
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_content_shell_drt&range=311294:311376

Minimized Testcase (8.90 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95TFoutpr95fjK0PBxgCpVg9XXf6sRJ8esaCkDCPhYyWE-n_ZZbG-MtHvs8N41-JUNSBUgNNZDDklaoKDlcA-NtsfL00frsrF1KKnhZplX1Gxv7AQv_C6ojFCPSGUCj9btnn5CHo8DvJQ9JOzNU2ZHqTKAjyw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-01-14)

ClusterFuzz has detected this issue as fixed in range 311294:311376.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6655057624825856

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  blink::CharacterData::setDataAndUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=262987:263028
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=311294:311376

Minimized Testcase (7.64 Kb): https://cluster-fuzz.appspot.com/download/AMIfv971Ns78EQK8dEPgkN2fCvDc9uC6_FZXvPZ6Nt7lTzHtjrISK4FoJg8Mr0GZmfS8nzLiK4ayiSGSwUVU7sOeej4Q9ndp5ZuDC4eNmwYbi69UxWCM8X6eD1mcYZApGeoKULEa2mIdGtM-znMUyglc70a9axu9Rg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-01-15)

ClusterFuzz has detected this issue as fixed in range 311294:311376.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6512254007640064

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x00009f7537dd
Crash State:
  blink::updatePositionAfterAdoptingTextReplacement
  blink::FrameSelection::didUpdateCharacterData
  blink::CharacterData::setDataAndUpdate
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=262987:263028
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=311294:311376

Minimized Testcase (0.29 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95RaRr2Dj9Sj9FVt3qSfEIlUpzdAD6fMt7o_-Rl9fx1KHuiJAx6CZgCLdu768VlEK3VDTBXaA_vn10eeq1IC5UYLCZfG9Uc4m1RC4tMmrCwo8xspfNT0qgbJXHfVsoDRTOl120n3gHNfDo1PYDUZw40M-YmMA
<script>
    function dom_manipulation() {
      document.execCommand("selectAll", null);
      document.execCommand("removeFormat" , true ,null);
    }
  </script>

  <style>
    * {
      text-transform:uppercase;
</style>
<body onload='dom_manipulation()'>  
  <embed><textarea autofocus>&#329

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### pe...@google.com (2015-01-25)

Approved for M41 (branch: 2272)

### bu...@chromium.org (2015-01-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189158

------------------------------------------------------------------
r189158 | pennymac@google.com | 2015-01-29T03:12:06.884295Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/editing/FrameSelection.cpp?r1=189158&r2=189157&pathrev=189158

Merge 188326 into M41 branch 2272: "Clamp text range offsets to the length of the Text..."

> Clamp text range offsets to the length of the Text node.
> 
> Due to case folding, RenderText length will not necessarily be the
> same as Text length.  A correct fix would entail mapping character
> offsets between the RenderText and Text.  This change just prevents
> using an offset beyond the end of the Text.
> 
> BUG=383777
> R=eae@chromium.org,yosin@chromium.org
> 
> Review URL: https://codereview.chromium.org/853533003

TBR=szager@chromium.org

Review URL: https://codereview.chromium.org/884943002
-----------------------------------------------------------------

### bu...@chromium.org (2015-01-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189170

------------------------------------------------------------------
r189170 | pennymac@google.com | 2015-01-29T08:32:15.790445Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/editing/FrameSelection.cpp?r1=189170&r2=189169&pathrev=189170

Revert 189158 "Merge 188326 into M41 branch 2272: "Clamp text ra..."

Broke continuous beta build: https://code.google.com/p/chromium/issues/detail?id=453206

> Merge 188326 into M41 branch 2272: "Clamp text range offsets to the length of the Text..."
> 
> > Clamp text range offsets to the length of the Text node.
> > 
> > Due to case folding, RenderText length will not necessarily be the
> > same as Text length.  A correct fix would entail mapping character
> > offsets between the RenderText and Text.  This change just prevents
> > using an offset beyond the end of the Text.
> > 
> > BUG=383777
> > R=eae@chromium.org,yosin@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/853533003
> 
> TBR=szager@chromium.org
> 
> Review URL: https://codereview.chromium.org/884943002

TBR=pennymac@google.com

Review URL: https://codereview.chromium.org/882323002
-----------------------------------------------------------------

### pe...@chromium.org (2015-01-29)

I've had to temporarily revert the CL (#68) from M41 branch 2272.  It seems to have broken the continuous beta builder: https://code.google.com/p/chromium/issues/detail?id=453206.

+inferno@ as the name associated with the requesting merge.  Could you or szager@ please have a quick look at the build log.  Let me know how you want to move forward.  If you want a new merge, I'll approve it, but I'll let you handle the execution.



### sz...@chromium.org (2015-01-29)

There's nothing in the build log to suggest this patch broke the build, and there's nothing I would do differently in applying the patch again.

### pe...@chromium.org (2015-01-30)

Thanks for your input as well - I got that feeling looking at the log this morning.  Must have been a build flake, and I was too tired last night to notice.

So I'm going to try to re-merge tomorrow morning (so I have the whole day to watch the internal continuous beta builders).

### bu...@chromium.org (2015-01-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189274

------------------------------------------------------------------
r189274 | pennymac@google.com | 2015-01-30T19:22:35.897967Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/core/editing/FrameSelection.cpp?r1=189274&r2=189273&pathrev=189274

Re-try Merge 188326 to M41 branch 2272:  "Clamp text range offsets to the length of the Text..."

> Clamp text range offsets to the length of the Text node.
> 
> Due to case folding, RenderText length will not necessarily be the
> same as Text length.  A correct fix would entail mapping character
> offsets between the RenderText and Text.  This change just prevents
> using an offset beyond the end of the Text.
> 
> BUG=383777
> R=eae@chromium.org,yosin@chromium.org
> 
> Review URL: https://codereview.chromium.org/853533003

TBR=szager@chromium.org

Review URL: https://codereview.chromium.org/888933002
-----------------------------------------------------------------

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-21)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-12-17)

This reporter isn't from Samsung as initially thought, so is eligible for consideration under the Chrome Reward Program: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2016-04-22)

Congratulations - $1,000 for this report. I'll add this in with your other payments.

### ti...@google.com (2016-04-25)

Adding in OP's new email address.

### ti...@google.com (2016-04-25)

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

This issue was migrated from crbug.com/chromium/383777?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing, Blink>Layout]
[Monorail mergedwith: crbug.com/chromium/388382, crbug.com/chromium/406870, crbug.com/chromium/446517, crbug.com/chromium/447572]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079733)*
