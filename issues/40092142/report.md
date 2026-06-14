# OOB read due to iterating over wrong textbox in TextIterator::emitText (first-letter + RTL)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092142](https://issues.chromium.org/issues/40092142) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-06-23 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

direction: rtl  

first-letter style  

non-letter character as first letter followed by stuff then a left-to-right-override  

leads to an out of bounds read

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**

<html style="direction: rtl;">
<style>
body:first-letter { color: black; }
</style>
!AAA&#x202E;

the out-of-boundness is easily controllable between 0 and 128 bytes.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan/vg + renderer  

Crash State:  

0x00007ff6c024e204 is located 0 bytes to the right of 36-byte region [0x00007ff6c024e1e0,0x00007ff6c024e204)

valgrind is confused about the semantics of the read. asan gives nicer results. :D

## Attachments

- [maximal2.html](attachments/maximal2.html) (text/html; charset=us-ascii, 229 B)
- [vg2.txt](attachments/vg2.txt) (text/plain; charset=us-ascii, 5.0 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain; charset=us-ascii, 4.9 KB)
- [maximal.html](attachments/maximal.html) (text/html; charset=us-ascii, 158 B)
- [minimal.html](attachments/minimal.html) (text/html; charset=us-ascii, 97 B)
- [asan1.txt](attachments/asan1.txt) (text/plain; charset=us-ascii, 4.9 KB)
- [vg1.txt](attachments/vg1.txt) (text/plain; charset=us-ascii, 4.7 KB)

## Timeline

### in...@chromium.org (2011-06-24)

This looks definitely same as http://code.google.com/p/chromium/issues/detail?id=74649 we have been trying to hunt for a while. Thanks a lot Miaubiz for finding it.

### in...@chromium.org (2011-06-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-24)

this looks to be introduced in http://trac.webkit.org/changeset/65062 and the person has left Google.

Offsets go wrong in TextIterator::emitText.

### in...@chromium.org (2011-06-24)

Add these asserts for easy reproduction 

Index: WebCore/editing/TextIterator.cpp
===================================================================
--- WebCore/editing/TextIterator.cpp	(revision 89499)
+++ WebCore/editing/TextIterator.cpp	(working copy)
@@ -975,6 +975,9 @@
     RenderText* renderer = toRenderText(renderObject);
     m_text = m_emitsTextWithoutTranscoding ? renderer->textWithoutTranscoding() : renderer->text();
     ASSERT(m_text.characters());
+    ASSERT(0 <= textStartOffset && textStartOffset < m_text.length());
+    ASSERT(0 <= textEndOffset && textEndOffset <= m_text.length());
+    ASSERT(textStartOffset <= textEndOffset);
 
     m_positionNode = textNode;
     m_positionOffsetBaseNode = 0;


### in...@chromium.org (2011-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2011-06-24)

Levi is probably most familiar with first-letter treatment in editing.

### [Deleted User] (2011-06-24)

Filed https://bugs.webkit.org/show_bug.cgi?id=63334.

### sc...@gmail.com (2011-06-25)

Sounds like we can fix this with a revert in the shorter term?

### [Deleted User] (2011-06-25)

No.  There are few tests that depend on the changeset so we can't.

### in...@chromium.org (2011-06-27)

http://trac.webkit.org/changeset/89831

### [Deleted User] (2011-06-29)

FTR, I'm seeing exactly the same stack on Windows using Dr. Memory while running the attached .html's on r90194.

Here's the drmemory report:
UNADDRESSABLE ACCESS: 0x0db71840-0x0db71841 1 byte(s) within 0x0db71840-0x0db71842
Note: next higher malloc: 0x0db71841-0x0db71855
Note: prev lower malloc:  0x0db71828-0x0db71840
 # 1 WTF::Vector<wchar_t,0>::append<wchar_t>    third_party\webkit\source\javascriptcore\wtf\vector.h:952
 # 2 WebKit::frameContentAsPlainText            third_party\webkit\source\webkit\chromium\src\webframeimpl.cpp:245
 # 3 WebKit::WebFrameImpl::contentAsText        third_party\webkit\source\webkit\chromium\src\webframeimpl.cpp:1770
 # 4 ChromeRenderViewObserver::CaptureText      chrome\renderer\chrome_render_view_observer.cc:580
 # 5 ChromeRenderViewObserver::CapturePageInfo  chrome\renderer\chrome_render_view_observer.cc:548
 # 6 DispatchToMethod<...>

[just a tool sanity confirmation]

### in...@chromium.org (2011-06-29)

timurrr, as a tool sanity confirmation :), dr memory is no longer complaining right, so this bug is fixed ?

### [Deleted User] (2011-06-29)

My checkout is slightly out-of-date, I *think* I'm running Chromium r90194 or even older.
Looks like the fix was landed in Chromium r90713, I didn't run Dr. Memory on that yet.

### kc...@chromium.org (2011-06-29)

I observe this on r90931. 
Is it the same or different? 



READ of size 2 at 0x00007f30cfd617a8 thread T0
    #0 0x7f310d24fc6c in void WTF::Vector<unsigned short, 0ul>::append<unsigned short> third_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:952
    #1 0x7f310de31df3 in WebCore::SearchBuffer::append third_party/WebKit/Source/WebCore/editing/TextIterator.cpp:1943
    #2 0x7f310de2f05d in WebCore::findPlainText third_party/WebKit/Source/WebCore/editing/TextIterator.cpp:2547
    #3 0x7f310de2eb78 in WebCore::findPlainText third_party/WebKit/Source/WebCore/editing/TextIterator.cpp:2578
    #4 0x7f310dded9a4 in WebCore::Editor::findString third_party/WebKit/Source/WebCore/editing/Editor.cpp:2972
    #5 0x7f310dded40e in WebCore::Editor::findString third_party/WebKit/Source/WebCore/editing/Editor.cpp:2940
    #6 0x7f310e01b5e1 in WebCore::DOMWindow::find const third_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1055
    #7 0x7f310d47fe8e in WebCore::DOMWindowInternal::findCallback out/Release/obj/gen/webcore/bindings/V8DOMWindow.cpp:2791
    #8 0x7f310c9c6e61 in HandleApiCallHelper v8/src/builtins.cc:1105
    #9 0x7f30da22414e in  
0x00007f30cfd617a8 is located 0 bytes to the right of 40-byte region [0x00007f30cfd61780,0x00007f30cfd617a8)
allocated by thread T0 here:
    #0 0x7f310f8c7a8a in malloc _asan_rtl_
    #1 0x7f310d70e469 in WTF::fastMalloc third_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:248
    #2 0x7f310d71ad3a in WTF::StringImpl::createUninitialized third_party/WebKit/Source/JavaScriptCore/wtf/text/StringImpl.cpp:87
    #3 0x7f310d82f2d5 in WTF::String::createUninitialized third_party/WebKit/Source/JavaScriptCore/wtf/text/WTFString.h:254
    #4 0x7f310daf35ec in WebCore::StringTraits<WTF::String>::fromV8String third_party/WebKit/Source/WebCore/bindings/v8/V8Binding.cpp:346
    #5 0x7f310daf3313 in WTF::String WebCore::v8StringToWebCoreString<WTF::String> third_party/WebKit/Source/WebCore/bindings/v8/V8Binding.cpp:391
    #6 0x7f310d3582f3 in WTF::String WebCore::V8ParameterBase::toString<WTF::String> third_party/WebKit/Source/WebCore/bindings/v8/V8Binding.h:325
    #7 0x7f310d3581e1 in WebCore::V8ParameterBase::operator WTF::String third_party/WebKit/Source/WebCore/bindings/v8/V8Binding.h:272
    #8 0x7f310d40e042 in WebCore::TextInternal::replaceWholeTextCallback out/Release/obj/gen/webcore/bindings/V8Text.cpp:77
    #9 0x7f310c9c6e61 in HandleApiCallHelper v8/src/builtins.cc:1105


### kc...@chromium.org (2011-06-29)

The stack above is from 
Chromium: r90931
WebKit: r89967

which means (probably) that https://crbug.com/chromium/74649 is a separate bug. 
Shall we reopen  it?

### [Deleted User] (2011-06-29)

I think this is a different bug and we should un-dup

### in...@chromium.org (2011-06-29)

They both use the same ugly textiterator ugly, but if we have a repro, that is awesome. Please go ahead and undup 74649.

### sc...@gmail.com (2011-07-12)

Merged to M13: http://trac.webkit.org/changeset/90858

### sc...@gmail.com (2011-07-20)

$500 on account of possibility of reading back the OOB content

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

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2011-07-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

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

### bu...@chromium.org (2013-04-01)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/87298?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/82699]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092142)*
