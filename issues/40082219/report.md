# Memory corruption with invalid text node cast for edit commands

| Field | Value |
|-------|-------|
| **Issue ID** | [40082219](https://issues.chromium.org/issues/40082219) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **CVE IDs** | CVE-2010-1783, CVE-2010-3114 |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-07-20 |
| **Bounty** | $500.00 |

## Description

Split off from https://crbug.com/chromium/49596 from wooshi. Here src is arbitary, so looks like OOB read.

memcpy(unsigned char * dst=0x0b8849b4, unsigned char * src=0x002f0000, unsigned long count=2)  Line 358	Asm
WebCore::StringImpl::create(const wchar_t * characters=0x002f0000, unsigned int length=1)  Line 97 + 0x13 bytes	C++
WebCore::StringImpl::substring(unsigned int start=0, unsigned int length=1)  Line 174 + 0x1a bytes	C++
WebCore::CharacterData::substringData(unsigned int offset=0, unsigned int count=1, int & ec=0)  Line 59 + 0x1e bytes	C++
WebCore::DeleteFromTextNodeCommand::doApply()  Line 52 + 0x31 bytes	C++
WebCore::EditCommand::apply()  Line 91 + 0xf bytes	C++
WebCore::CompositeEditCommand::applyCommandToComposite(WTF::PassRefPtr<WebCore::EditCommand> cmd={m_document={m_styleSelector={...} m_didCalculateStyleSelector=false m_frame=0x0b4df000 ...} m_startingSelection={...} m_endingSelection={...} ...})  Line 100	C++
WebCore::CompositeEditCommand::replaceTextInNode(WTF::PassRefPtr<WebCore::Text> node={...}, unsigned int offset=0, unsigned int count=1, const WebCore::String & replacementText=" lle")  Line 334 + 0x35 bytes	C++
WebCore::DeleteSelectionCommand::fixupWhitespace()  Line 550	C++
WebCore::DeleteSelectionCommand::doApply()  Line 790	C++
WebCore::EditCommand::apply()  Line 91 + 0xf bytes	C++
WebCore::CompositeEditCommand::applyCommandToComposite(WTF::PassRefPtr<WebCore::EditCommand> cmd={m_document={m_styleSelector={...} m_didCalculateStyleSelector=false m_frame=0x0b4df000 ...} m_startingSelection={...} m_endingSelection={...} ...})  Line 100	C++
WebCore::CompositeEditCommand::deleteSelection(const WebCore::VisibleSelection & selection={...}, bool smartDelete=false, bool mergeBlocksAfterDelete=true, bool replace=false, bool expandForSpecialElements=true)  Line 370 + 0x34 bytes	C++
WebCore::TypingCommand::deleteKeyPressed(WebCore::TextGranularity granularity=CharacterGranularity, bool killRing=false)  Line 506	C++
WebCore::TypingCommand::doApply()  Line 260	C++
WebCore::EditCommand::apply()  Line 91 + 0xf bytes	C++
WebCore::TypingCommand::deleteKeyPressed(WebCore::Document * document=0x0990c000, bool smartDelete=false, WebCore::TextGranularity granularity=CharacterGranularity, bool killRing=false)  Line 101	C++
WebCore::executeDelete(WebCore::Frame * frame=0x0b4df000, WebCore::Event * __formal=0x00000000, WebCore::EditorCommandSource source=CommandFromDOM, WebCore::Event * __formal=0x00000000)  Line 320 + 0x24 bytes	C++
WebCore::Editor::Command::execute(const WebCore::String & parameter={...}, WebCore::Event * triggeringEvent=0x00000000)  Line 1554 + 0x24 bytes	C++
WebCore::Document::execCommand(const WebCore::String & commandName="Delete??", bool userInterface=false, const WebCore::String & value={...})  Line 3706 + 0x26 bytes	C++
WebCore::DocumentInternal::execCommandCallback(const v8::Arguments & args={...})  Line 1400 + 0x2d bytes	C++
v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...})  Line 972 + 0x13 bytes	C++
v8::internal::Builtin_Impl_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...})  Line 989 + 0xd bytes	C++
v8::internal::Builtin_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...})  Line 988 + 0x18 bytes	C++
033800ae()	
v8::internal::Invoke(bool construct=false, v8::internal::Handle<v8::internal::JSFunction> func={...}, v8::internal::Handle<v8::internal::Object> receiver={...}, int argc=0, v8::internal::Object * * * args=0x00000000, bool * has_pending_exception=0x0631eb23)  Line 95 + 0x19 bytes	C++
v8::internal::Execution::Call(v8::internal::Handle<v8::internal::JSFunction> func={...}, v8::internal::Handle<v8::internal::Object> receiver={...}, int argc=0, v8::internal::Object * * * args=0x00000000, bool * pending_exception=0x0631eb23)  Line 121 + 0x1f bytes	C++
v8::Script::Run()  Line 1246 + 0x19 bytes	C++
WebCore::V8Proxy::runScript(v8::Handle<v8::Script> script={...}, bool isInlineCode=false)  Line 457 + 0x13 bytes	C++
WebCore::V8Proxy::evaluate(const WebCore::ScriptSourceCode & source={...}, WebCore::Node * node=0x00000000)  Line 408 + 0x2a bytes	C++
WebCore::ScriptController::evaluate(const WebCore::ScriptSourceCode & sourceCode={...}, WebCore::ShouldAllowXSS shouldAllowXSS=DoNotAllowXSS)  Line 241	C++
WebCore::ScriptController::executeScript(const WebCore::ScriptSourceCode & sourceCode={...}, WebCore::ShouldAllowXSS shouldAllowXSS=DoNotAllowXSS)  Line 62	C++
WebCore::XMLDocumentParser::endElementNs()  Line 873 + 0x63 bytes	C++
WebCore::endElementNsHandler(void * closure=0x05a7d200, const unsigned char * __formal=0x0990fcc3, const unsigned char * __formal=0x0990fcc3, const unsigned char * __formal=0x0990fcc3)  Line 1086	C++
xmlParseEndTag2(_xmlParserCtxt * ctxt=0x05a7d200, const unsigned char * prefix=0x00000000, const unsigned char * URI=0x0990fc48, int line=0, int nsNr=0, int tlen=0)  Line 9222 + 0x25 bytes	C
xmlParseTryOrFinish(_xmlParserCtxt * ctxt=0x05a7d200, int terminate=0)  Line 11027 + 0x5b bytes	C
xmlParseChunk(_xmlParserCtxt * ctxt=0x05a7d200, const char * chunk=0x0b54b000, int size=9946, int terminate=0)  Line 11632 + 0xd bytes	C
WebCore::XMLDocumentParser::doWrite(const WebCore::String & parseString="
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:svg="http://www.w3.org/2000/svg" xmlns:mat="http://www.w3.org/1998/Math/MathML" xmlns:xht="http://www.w3.org/1999/xhtml">
<?xml-stylesheet href=")  Line 643 + 0x2b bytes	C++
WebCore::XMLDocumentParser::append(const WebCore::SegmentedString & s={...})  Line 143 + 0x15 bytes	C++
WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter * writer=0x0b4df18c, const char * data=0x03e40000, int length=4973, bool shouldFlush=false)  Line 55 + 0x1f bytes	C++
WebCore::DocumentWriter::addData(const char * str=0x03e40000, int len=4973, bool flush=false)  Line 200 + 0x20 bytes	C++
WebCore::FrameLoader::addData(const char * bytes=0x03e40000, int length=4973)  Line 1144	C++
WebKit::WebFrameImpl::commitDocumentData(const char * data=0x03e40000, unsigned int dataLen=4973)  Line 1022	C++
WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader * loader=0x05a79900, const char * data=0x03e40000, int length=4973)  Line 1042 + 0x20 bytes	C++
WebCore::FrameLoader::committedLoad(WebCore::DocumentLoader * loader=0x05a79900, const char * data=0x03e40000, int length=4973)  Line 2752 + 0x24 bytes	C++
WebCore::DocumentLoader::commitLoad(const char * data=0x03e40000, int length=4973)  Line 281	C++
WebCore::DocumentLoader::receivedData(const char * data=0x03e40000, int length=4973)  Line 293	C++
WebCore::FrameLoader::receivedData(const char * data=0x03e40000, int length=4973)  Line 1558	C++
WebCore::MainResourceLoader::addData(const char * data=0x03e40000, int length=4973, bool allAtOnce=false)  Line 148	C++
WebCore::ResourceLoader::didReceiveData(const char * data=0x03e40000, int length=4973, __int64 lengthReceived=4973, bool allAtOnce=false)  Line 260 + 0x1c bytes	C++
WebCore::MainResourceLoader::didReceiveData(const char * data=0x03e40000, int length=4973, __int64 lengthReceived=4973, bool allAtOnce=false)  Line 416	C++
WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle * __formal=0x04ab3860, const char * data=0x03e40000, int length=4973, int lengthReceived=4973)  Line 431 + 0x1f bytes	C++
WebCore::ResourceHandleInternal::didReceiveData(WebKit::WebURLLoader * __formal=0x05a01450, const char * data=0x03e40000, int dataLength=4973)  Line 173 + 0x31 bytes	C++
webkit_glue::WebURLLoaderImpl::Context::OnReceivedData(const char * data=0x03e40000, int len=4973)  Line 564 + 0x26 bytes	C++
ResourceDispatcher::OnReceivedData(const IPC::Message & message=class=16, index=53, int request_id=27, void * shm_handle=0x00000a00, int data_len=4973)  Line 397 + 0x1b bytes	C++
IPC::MessageWithTuple<Tuple3<int,void *,int> >::Dispatch<ResourceDispatcher,int,void *,int>(const IPC::Message * msg=class=16, index=53, ResourceDispatcher * obj=0x059e97d0, void (const IPC::Message &, int, void *, int)* func=0x54fd3c70)  Line 1079 + 0x18 bytes	C++
ResourceDispatcher::DispatchMessageW(const IPC::Message & message=class=16, index=53)  Line 535 + 0x12 bytes	C++
ResourceDispatcher::OnMessageReceived(const IPC::Message & message=class=16, index=53)  Line 303	C++
ChildThread::OnMessageReceived(const IPC::Message & msg=class=16, index=53)  Line 124 + 0x19 bytes	C++
IPC::ChannelProxy::Context::OnDispatchMessage(const IPC::Message & message=class=16, index=53)  Line 206 + 0x19 bytes	C++
DispatchToMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),IPC::Message>(IPC::ChannelProxy::Context * obj=0x059e7000, void (const IPC::Message &)* method=0x53eddae0, const Tuple1<IPC::Message> & arg={...})  Line 422 + 0xf bytes	C++
RunnableMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),Tuple1<IPC::Message> >::Run()  Line 326 + 0x1e bytes	C++
MessageLoop::RunTask(Task * task=0x0b85e980)  Line 409 + 0xf bytes	C++
MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 421	C++
MessageLoop::DoWork()  Line 525 + 0xc bytes	C++
base::MessagePumpForUI::DoRunLoop()  Line 203 + 0x1d bytes	C++
base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x0631fb80, base::MessagePumpWin::Dispatcher * dispatcher=0x00000000)  Line 52 + 0xf bytes	C++
base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x0631fb80)  Line 79 + 0x1c bytes	C++
MessageLoop::RunInternal()  Line 257 + 0x2a bytes	C++
MessageLoop::RunHandler()  Line 230	C++
MessageLoop::Run()  Line 208	C++
base::Thread::Run(MessageLoop * message_loop=0x0631fb80)  Line 137	C++
base::Thread::ThreadMain()  Line 160 + 0x16 bytes	C++
`anonymous namespace'::ThreadFunc(void * closure=0x04a6ac00)  Line 26 + 0xf bytes	C++
kernel32.dll!@BaseThreadInitThunk@12()  + 0xe bytes	
ntdll.dll!___RtlUserThreadStart@8()  + 0x23 bytes	
ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	


## Attachments

- [1.xhtml](attachments/1.xhtml) (text/x-c++; charset=us-ascii, 4.9 KB)

## Timeline

### in...@chromium.org (2010-07-20)

I am first trying to reduce the testcase, but i know the problem is bad cast on a svg node trying to convert into a text node.

### in...@chromium.org (2010-07-20)

Filed WebKit Bug
https://bugs.webkit.org/show_bug.cgi?id=42655

### in...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-20)

Committed r63773: <http://trac.webkit.org/changeset/63773>

### sc...@gmail.com (2010-07-22)

As per the other bug, a well-reduced test case would likely have made this worth $1000.

### bu...@gmail.com (2010-07-26)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=53680 

------------------------------------------------------------------------
r53680 | inferno@chromium.org | 2010-07-26 14:08:55 -0700 (Mon, 26 Jul 2010) | 30 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/editing/execCommand/editing-nontext-node-crash-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/editing/execCommand/editing-nontext-node-crash.xhtml
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/editing/DeleteSelectionCommand.cpp?r1=53680&r2=53679
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/editing/InsertLineBreakCommand.cpp?r1=53680&r2=53679
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/editing/InsertParagraphSeparatorCommand.cpp?r1=53680&r2=53679

Merge 63773 - 2010-07-20  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Check the node is a text node before doing the static cast
        for editing commands.
        https://bugs.webkit.org/show_bug.cgi?id=42655

        Test: editing/execCommand/editing-nontext-node-crash.xhtml

        * editing/DeleteSelectionCommand.cpp:
        (WebCore::DeleteSelectionCommand::fixupWhitespace):
        * editing/InsertLineBreakCommand.cpp:
        (WebCore::InsertLineBreakCommand::doApply):
        * editing/InsertParagraphSeparatorCommand.cpp:
        (WebCore::InsertParagraphSeparatorCommand::doApply):
2010-07-20  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Tests that applying an editing command on a non text node does not
        result in crash.
        https://bugs.webkit.org/show_bug.cgi?id=42655

        * editing/execCommand/editing-nontext-node-crash-expected.txt: Added.
        * editing/execCommand/editing-nontext-node-crash.xhtml: Added.

BUG=49628

Review URL: http://codereview.chromium.org/3027024
------------------------------------------------------------------------


### ch...@gmail.com (2010-08-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-17)

This was merged to 375:

http://src.chromium.org/viewvc/chrome?view=rev&revision=55444

Merge 63773 - 2010-07-20  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Check the node is a text node before doing the static cast
        for editing commands.
        https://bugs.webkit.org/show_bug.cgi?id=42655

        Test: editing/execCommand/editing-nontext-node-crash.xhtml

        * editing/DeleteSelectionCommand.cpp:
        (WebCore::DeleteSelectionCommand::fixupWhitespace):
        * editing/InsertLineBreakCommand.cpp:
        (WebCore::InsertLineBreakCommand::doApply):
        * editing/InsertParagraphSeparatorCommand.cpp:
        (WebCore::InsertParagraphSeparatorCommand::doApply):
2010-07-20  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Tests that applying an editing command on a non text node does not
        result in crash.
        https://bugs.webkit.org/show_bug.cgi?id=42655

        * editing/execCommand/editing-nontext-node-crash-expected.txt: Added.
        * editing/execCommand/editing-nontext-node-crash.xhtml: Added.


Review URL: http://codereview.chromium.org/3092017

### [Deleted User] (2010-08-18)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-08-18)

Works fine on Mac 5.0.375.127 (Official Build 55887).
Browser doesn't crash on loading and refreshing the page.

### [Deleted User] (2010-08-18)

Works fine with Google Chrome 5.0.375.127 (Official Build 55887) on Win Xp and Linux Ubuntu 9.04

### sc...@gmail.com (2010-08-25)

Payment in the electronic system.


### sc...@gmail.com (2010-09-08)

Was fixed by Safari. Releasing.
Not 100% sure about the CVE.

### g....@gmail.com (2010-09-08)

@scarybeasts
This is CVE-2010-3114, so probably CVE-2010-1783 is a duplicate



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

This issue was migrated from crbug.com/chromium/49628?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082219)*
