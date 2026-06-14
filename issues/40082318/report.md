# Use after free in document.close()

| Field | Value |
|-------|-------|
| **Issue ID** | [40082318](https://issues.chromium.org/issues/40082318) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2010-07-26 |
| **Bounty** | $500.00 |

## Description

---------- Forwarded message ----------
From: Microsoft Vulnerability Research msvr-at-microsoft.com <trax-proxy-disabled+672461097.1147046125@trakken.google.com>
Date: Mon, Jul 26, 2010 at 11:34 AM
Subject: [M#672461097] Vulnerability Report - MSVR-10-0103
To: Google Security Team <security@google.com>


=================================
The following Software vulnerability report is highly confidential and should be limited in distribution to members of the engineering team within Google with need-to-know for performance of security risk analysis and remediation.

We ask you to please direct all communications through msvr@microsoft.com for business and legal continuity purposes and not to the individual finder or other contacts you may have at Microsoft Corporation.
=================================

Hi Google Security Team,


We have found an exploitable use-after-free object lifetime bug in the latest version of Chrome.  We do not have the complete details but it appears from the disassembly that there is an attempt to reset a HTMLToken object after it has been deleted.  I have attached a repro that should help with root cause analysis. For MSVR internal tracking I have assigned this issue MSVR-10-0103.

Test Repro Environment:

Windows 7 RTM x86

Chrome 5.0.375.99

App Verifier/Page Heap


(8ec.ddc): Access violation - code c0000005 (!!! second chance !!!)

eax=00000000 ebx=05175000 ecx=0513b1e0 edx=00000000 esi=002ef244 edi=05175020

eip=5fb33fc0 esp=002ef22c ebp=002ef248 iopl=0         nv up ei pl zr na pe nc

cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246

chrome_5f9a0000!WebCore::Token::reset:

5fb33fc0 8b07            mov     eax,dword ptr [edi]  ds:0023:05175020=????????



1:018> u .

5fb33fc0 8b07            mov     eax,dword ptr [edi]

5fb33fc2 832700          and     dword ptr [edi],0  ß DWORD Size Write

5fb33fc5 56              push    esi

5fb33fc6 85c0            test    eax,eax

5fb33fc8 7408            je      chrome_5f9a0000!WebCore::Token::reset+0x12 (5fb33fd2)

5fb33fca 83c004          add     eax,4

5fb33fcd e8a0e9ecff      call    chrome_5f9a0000!WTF::RefCounted<WebCore::Clipboard>::deref (5fa02972)

5fb33fd2 8d7704          lea     esi,[edi+4]

1:018> dv

          this = 0x05175020



1:018> dt this

Local var @ edi Type WebCore::Token*

  +0x000 attrs            : WTF::RefPtr<WebCore::NamedMappedAttrMap>

  +0x004 text             : WTF::RefPtr<WebCore::StringImpl>

  +0x008 tagName          : WebCore::AtomicString

  +0x00c beginTag         : ??

  +0x00d selfClosingTag   : ??

  +0x00e brokenXMLStyle   : ??

  +0x010 m_sourceInfo     : WTF::OwnPtr<WTF::Vector<wchar_t,0> >

Memory read error 0517502e

1:018> k

ChildEBP RetAddr

002ef228 5fb37f30 chrome_5f9a0000!WebCore::Token::reset [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\html\htmltokenizer.h @ 73]

002ef248 5fb370ab chrome_5f9a0000!WebCore::HTMLTokenizer::processToken+0x140 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\html\htmltokenizer.cpp @ 1944]

002ef370 5fb378bb chrome_5f9a0000!WebCore::HTMLTokenizer::parseTag+0xea3 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\html\htmltokenizer.cpp @ 1513]

002ef410 5f9dc836 chrome_5f9a0000!WebCore::HTMLTokenizer::write+0x457 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\html\htmltokenizer.cpp @ 1765]

002ef470 5f9dc910 chrome_5f9a0000!WebCore::FrameLoader::write+0x311 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\loader\frameloader.cpp @ 945]

002ef494 5f9dc8dd chrome_5f9a0000!WebCore::FrameLoader::endIfNotLoadingMainResource+0x31 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\loader\frameloader.cpp @ 981]

002ef4c8 5fb7038f chrome_5f9a0000!WebCore::FrameLoader::end+0xf [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\loader\frameloader.cpp @ 967]

002ef4cc 5fbf64c5 chrome_5f9a0000!WebCore::ResourceLoader::didFinishLoading+0x5 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\loader\resourceloader.cpp @ 444]

002ef4d4 6002c5ae chrome_5f9a0000!WebCore::ResourceHandleInternal::didFinishLoading+0x13 [c:\b\slave\chrome-official\build\src\third_party\webkit\webkit\chromium\src\resourcehandle.cpp @ 149]

002ef4e8 6e13fdf9 chrome_5f9a0000!webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest+0x12e [c:\b\slave\chrome-official\build\src\webkit\glue\weburlloader_impl.cc @ 560]

WARNING: Stack unwind information not available. Following frames may be wrong.

002ef624 5ffdca06 verifier!VerifierGetProviderHelper+0x10599

002ef630 5ffdc380 chrome_5f9a0000!ResourceDispatcher::DispatchMessageW+0x25 [c:\b\slave\chrome-official\build\src\chrome\common\resource_dispatcher.cc @ 533]

00000000 00000000 chrome_5f9a0000!ResourceDispatcher::OnMessageReceived+0xe3 [c:\b\slave\chrome-official\build\src\chrome\common\resource_dispatcher.cc @ 303]



18> lmv m chrome_5f9a0000

start    end        module name

5f9a0000 60b6d000   chrome_5f9a0000   (private pdb symbols)  C:\Debuggers\sym\chrome_dll.pdb\91DCC128F9794E409D1BFF5780A03F4D1\chrome_dll.pdb

   Loaded symbol image file: c:\Users\ \AppData\Local\Google\Chrome\Application\5.0.375.99\chrome.dll

   Image path: c:\Users\ \AppData\Local\Google\Chrome\Application\5.0.375.99\chrome.dll

   Image name: chrome.dll

   Timestamp:        Mon Jun 28 17:51:03 2010 (4C294377)

   CheckSum:         01121656

   ImageSize:        011CD000

  File version:     5.0.375.99

   Product version:  5.0.375.99

   File flags:       0 (Mask 17)

   File OS:          4 Unknown Win32

   File type:        1.0 App

   File date:        00000000.00000000

   Translations:     0409.04b0

   CompanyName:      Google Inc.

   ProductName:      Google Chrome

   InternalName:     chrome_dll

   OriginalFilename: chrome.dll

   ProductVersion:   5.0.375.99

   FileVersion:      5.0.375.99

   FileDescription:  Google Chrome

## Attachments

- [msvr-10-0103.html](attachments/msvr-10-0103.html) (application/octet-stream; charset=binary, 27.5 KB)
- [bug50250.html](attachments/bug50250.html) (text/html; charset=us-ascii, 355 B)

## Timeline

### in...@chromium.org (2010-07-26)

Reduced testcase enclosed.

eax=04c55280 ebx=00000000 ecx=04c36980 edx=00000031 esi=04c1fd60 edi=04c1fd60
eip=548bb824 esp=04e2f520 ebp=04e2f5e0 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
chrome_541b0000!std::_Push_heap_0<WebCore::TimerHeapIterator,int,WebCore::TimerHeapElement>+0x44:
548bb824 8b0cb9          mov     ecx,dword ptr [ecx+edi*4] ds:002b:17cb5f00=????????
0:015> kb
ChildEBP RetAddr  Args to Child              
04e2f524 548bbb0c 00000000 04c1fd60 00000000 chrome_541b0000!std::_Push_heap_0<WebCore::TimerHeapIterator,int,WebCore::TimerHeapElement>+0x44 [c:\program files (x86)\microsoft visual studio 9.0\vc\include\algorithm @ 1991]
04e2f544 548bbbb8 0775a2d8 548bbc6d 00000000 chrome_541b0000!WebCore::TimerBase::heapPop+0x2c [d:\chromium2\src\third_party\webkit\webcore\platform\timer.cpp @ 268]
04e2f54c 548bbc6d 00000000 0775a2d8 548bbce0 chrome_541b0000!WebCore::TimerBase::heapIncreaseKey+0x8 [d:\chromium2\src\third_party\webkit\webcore\platform\timer.cpp @ 252]
04e2f558 548bbce0 46b47a57 41d31378 0782b000 chrome_541b0000!WebCore::TimerBase::setNextFireTime+0x8d [d:\chromium2\src\third_party\webkit\webcore\platform\timer.cpp @ 306]
04e2f568 54b4b316 00000000 00000000 00000000 chrome_541b0000!WebCore::TimerBase::start+0x20 [d:\chromium2\src\third_party\webkit\webcore\platform\timer.cpp @ 184]
04e2f5e0 54b4b6d6 00000000 078c7c00 54b4a150 chrome_541b0000!WebCore::HTMLDocumentParser::pumpTokenizer+0xd6 [d:\chromium2\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 185]
04e2f5ec 54b4a150 04e2f60c 07ad0d00 0782dd20 chrome_541b0000!WebCore::HTMLDocumentParser::append+0x76 [d:\chromium2\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 264]
04e2f634 54a1dd14 07ad0e64 00000000 078c7c00 chrome_541b0000!WebCore::DecodedDataDocumentParser::appendBytes+0xb0 [d:\chromium2\src\third_party\webkit\webcore\dom\decodeddatadocumentparser.cpp @ 55]
04e2f650 548d7e12 07ae5000 00d37b80 00000000 chrome_541b0000!WebCore::DocumentWriter::endIfNotLoadingMainResource+0x44 [d:\chromium2\src\third_party\webkit\webcore\loader\documentwriter.cpp @ 221]
04e2f660 54afd8f0 0783f320 0782dd20 54afebd7 chrome_541b0000!WebCore::FrameLoader::finishedLoading+0x32 [d:\chromium2\src\third_party\webkit\webcore\loader\frameloader.cpp @ 2225]
04e2f66c 54afebd7 54859f7c 05053f30 0782dd20 chrome_541b0000!WebCore::MainResourceLoader::didFinishLoading+0x30 [d:\chromium2\src\third_party\webkit\webcore\loader\mainresourceloader.cpp @ 440]
04e2f670 54859f7c 05053f30 0782dd20 00d06b40 chrome_541b0000!WebCore::ResourceLoader::didFinishLoading+0x7 [d:\chromium2\src\third_party\webkit\webcore\loader\resourceloader.cpp @ 444]
04e2f720 547baf3f 04e2f764 04e2f76c 547baeb0 chrome_541b0000!webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest+0x18c [d:\chromium2\src\webkit\glue\weburlloader_impl.cc @ 617]
04e2f744 547bc0cb 00000018 04e2f764 04e2f76c chrome_541b0000!ResourceDispatcher::OnRequestComplete+0x8f [d:\chromium2\src\chrome\common\resource_dispatcher.cc @ 470]
04e2f788 547bd061 04c63490 00ce1780 547baeb0 chrome_541b0000!IPC::MessageWithTuple<Tuple3<int,URLRequestStatus,std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >::Dispatch<ResourceDispatcher,void (__thiscall ResourceDispatcher::*)(int,URLRequestStatus const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>+0x5b [d:\chromium2\src\ipc\ipc_message_utils.h @ 1044]
04e2f7a4 547bd8cf 04c63490 04e2fa88 04c63490 chrome_541b0000!ResourceDispatcher::DispatchMessageW+0xa1 [d:\chromium2\src\chrome\common\resource_dispatcher.cc @ 537]
04e2f860 547b6f6d 04c63490 04c63480 00c9be70 chrome_541b0000!ResourceDispatcher::OnMessageReceived+0x27f [d:\chromium2\src\chrome\common\resource_dispatcher.cc @ 303]
04e2f874 5443e407 04c63490 04e2fb7c 542d53ef chrome_541b0000!ChildThread::OnMessageReceived+0x1d [d:\chromium2\src\chrome\common\child_thread.cc @ 124]
04e2f880 542d53ef 04e2fa88 00000000 00000003 chrome_541b0000!RunnableMethod<ChromeURLRequestContextGetter,void (__thiscall ChromeURLRequestContextGetter::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &),Tuple1<std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >::Run+0x17 [d:\chromium2\src\base\task.h @ 326]
04e2f934 542d6256 04c63480 00d3a9a8 771cbf18 chrome_541b0000!MessageLoop::RunTask+0xff [d:\chromium2\src\base\message_loop.cc @ 410]


### js...@chromium.org (2010-07-26)

Here's the simplest repro:

<iframe onload="document.open();document.close();" >


### ad...@google.com (2010-07-26)

I've confirmed receipt with MS and asked if they'd like to be cc'd on the bug.

### js...@chromium.org (2010-07-26)

Hey Nate. Please see the above line for a repro. It doesn't trigger Safari, so I'm thinking it might be an issue in the binding for Document.open? (Although, I haven't really had a chance for more than a cursory look.)


### js...@chromium.org (2010-07-26)

Nate, assigning to you as per discussion. Do you mind filing the upstream WebKit bug?

### sc...@gmail.com (2010-07-27)

I talked to MSVR and:

1) Credit can go to:  David Weston of Microsoft and Microsoft Vulnerability Research (MSVR)

2) We also do not have a plan to disclose this until Chrome has release a public fix.


Let's target this fix for the next patch, perhaps in about 2 weeks?

### js...@chromium.org (2010-07-27)

Filed upstream at: https://bugs.webkit.org/show_bug.cgi?id=43055


### sc...@gmail.com (2010-08-04)

This report qualifies for a $500 Chromium Security Reward! (This would likely have qualified for $1000 had the test case been of higher quality, i.e. reduced to the construct actually causing the issue).

### sc...@gmail.com (2010-08-05)

To clarify https://crbug.com/chromium/50250#c4: we now know that this is a generic WebKit bug that does crash Safari (e.g. refresh the exploit a few times).

### sc...@gmail.com (2010-08-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-19)

Committed r65692: <http://trac.webkit.org/changeset/65692>

Merge to 472 will be hard. Nate, can you please help on this.

### ma...@google.com (2010-08-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-09-08)

---Mail from Adam, need to backport https://crbug.com/chromium/44533 as well--

As many of you know, we're getting ready to backport the detachable
parser logic to M6.  That patch is already written and should be
landed on the M6 branch soonish.

One thing we did in that patch is to make many of these use-after-free
bugs into null pointer dereferences by proactively clearing out the
document pointer.  Unfortunately, that revealed a bug in the XML
parser:

https://bugs.webkit.org/show_bug.cgi?id=44533

Without the detachable parser patch, we don't crash on the example
URL, but after the patch we do crash on a null pointer.  That means
we'll probably want to backport the patch for https://crbug.com/chromium/44533 as well.

Adam

### in...@chromium.org (2010-09-08)

Nate, Adam, can you please merge this to 472. We got the signal from Kerz that we can now merge things to the branch for 1st v6 patch.

### sc...@gmail.com (2010-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-09)

Committed the backport:

http://src.chromium.org/viewvc/chrome?view=rev&revision=58909
http://codereview.chromium.org/3341023

Did not include the new LayoutTests; unfortunately, my client does not have that directory mapped and at any rate, I'm not sure if they might trigger the temporary crash.

I tested the <iframe onload="document.open();document.close();" > case -- before this patch it was firing memory corruption. After this patch, it hits a clean CRASH(). (0xbbadbeef in the crash register). More on that in the next comment.

I also tested the possible-regression case in https://bugs.webkit.org/show_bug.cgi?id=44533. http://weblab.ab-c.nl/streetview loads just fine for me.

### sc...@gmail.com (2010-09-09)

@steve.manzuik: status update. We fixed this bug on our development builds a while back. In the interests of getting the fix to our customers sooner, we have backported a variant of the patch, which we will get into customer hands relatively shortly.

Important note on fix validation! Whilst the condition is handled cleanly in our latest development builds, the backport introduced a complication. When triggering the test case of <iframe onload="document.open();document.close();" >, the Chrome renderer process will still terminate with "Aw, snap!" aka. the "sad tab". However, it is a very clean renderer process termination with no security consequence. Whereas before there was memory corruption, there is a now a clean forced exit via our CRASH() macro. This macro will forcibly crash a process by accessing 0xbbadbeef then NULL. This can clearly be seen in a debugger. It may be necessary to pass this information on to David Weston in case he erroneously thinks the bug is not fixed.

Thanks again for the report. You will see the credit in the security notes section for an upcoming patch.

### sc...@gmail.com (2010-09-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-12)

Independently discovered by wushi via https://crbug.com/chromium/55235. I've credited him in the release notes too.

### sc...@gmail.com (2010-09-15)

I confirmed that the test case is asserting internally in 6.0.472.59 release:

Program received signal SIGSEGV, Segmentation fault.
0x09081e70 in ?? ()
(gdb) disass $eip $eip+10
Dump of assembler code from 0x9081e70 to 0x9081e7a:
0x09081e70:	movl   $0x0,0xbbadbeef
End of assembler dump.

Thanks to MSVR, Steve and David for their patience whilst we got this fix to users.

### sc...@gmail.com (2010-11-03)

Reward going to charity.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### st...@gmail.com (2011-04-06)

Quick question on this old bug (sorry I know its fixed now).  Was a CVE ever assigned to this one? 

-Steve

### sc...@gmail.com (2011-04-06)

Not that I know of. We only starting doing CVE assignments just recently.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/50250?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/55235]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082318)*
