# Invalid memory access (with possible avenue to corruption)  in the xpath handling libxml

| Field | Value |
|-------|-------|
| **Issue ID** | [40083706](https://issues.chromium.org/issues/40083706) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **CVE IDs** | CVE-2010-4008 |
| **Reporter** | mi...@bkav.com.vn |
| **Assignee** | [Deleted User] |
| **Created** | 2010-10-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Google Chrome processes this .xml file (email attachment), the handling process tab will crash.

**VERSION**  

Chrome Version: latest version (stable and beta).  

Operating System: Windows XP3/Vista/7 (Linux and MacOS are likely to be affected).

**REPRODUCTION CASE**  

Open file (email attachment) with Google Chrome.

## Attachments

- [demo.zip](attachments/demo.zip) (application/zip; charset=binary, 424 B)
- [libxml2-xpath-ns-attr-axis.patch](attachments/libxml2-xpath-ns-attr-axis.patch) (text/plain; charset=us-ascii, 2.2 KB)

## Timeline

### mi...@bkav.com.vn (2010-10-11)

(730.f60): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=00000000 ebx=00daad00 ecx=00000003 edx=00dda820 esi=00000000 edi=ce0024c9
eip=67e7da5a esp=0024a1a0 ebp=0024a210 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
chrome_676c0000!xmlXPathNodeCollectAndTest+0x4fc:
67e7da5a 8b4704          mov     eax,dword ptr [edi+4] ds:0023:ce0024cd=????????
2:026> .exr -1
ExceptionAddress: 67e7da5a (chrome_676c0000!xmlXPathNodeCollectAndTest+0x000004fc)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: ce0024cd
Attempt to read from address ce0024cd
2:026> kp
ChildEBP RetAddr  
0024a210 67e7ef11 chrome_676c0000!xmlXPathNodeCollectAndTest(struct _xmlXPathParserContext * ctxt = 0x00e43fc0, struct _xmlXPathStepOp * op = 0x00000000, struct _xmlNode ** first = 0x00000000, struct _xmlNode ** last = 0x00000000, int toBool = 0)+0x4fc [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 12232]
0024a260 67e7f7bb chrome_676c0000!xmlXPathCompOpEval(struct _xmlXPathParserContext * ctxt = 0x00e43fc0, struct _xmlXPathStepOp * op = 0x00da4b04)+0x6d6 [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 13307]
0024a2a8 67e7f1af chrome_676c0000!xmlXPathCompOpEval(struct _xmlXPathParserContext * ctxt = 0x00e43fc0, struct _xmlXPathStepOp * op = 0x00da4b30)+0xf80 [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 13785]
0024a2f0 67e7efe5 chrome_676c0000!xmlXPathCompOpEval(struct _xmlXPathParserContext * ctxt = 0x00e43fc0, struct _xmlXPathStepOp * op = 0x00da4b5c)+0x974 [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 13420]
0024a338 67e7f7bb chrome_676c0000!xmlXPathCompOpEval(struct _xmlXPathParserContext * ctxt = 0x00e43fc0, struct _xmlXPathStepOp * op = 0x00da4b88)+0x7aa [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 13355]
0024a380 67e80092 chrome_676c0000!xmlXPathCompOpEval(struct _xmlXPathParserContext * ctxt = 0x00e43fc0, struct _xmlXPathStepOp * op = 0x00da4bb4)+0xf80 [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 13785]
0024a39c 67e805f6 chrome_676c0000!xmlXPathRunEval(struct _xmlXPathParserContext * ctxt = 0x00000000, int toBool = 0)+0x104 [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 14353]
0024a3b0 67e80758 chrome_676c0000!xmlXPathEvalExpr(struct _xmlXPathParserContext * ctxt = 0xce0024c9)+0x8f [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 14840]
0024a3d0 680867bd chrome_676c0000!xmlXPathEvalExpression(unsigned char * str = 0x00e60000 "number(//namespace::node()/following::text())", struct _xmlXPathContext * ctxt = 0x00dda820)+0x5d [c:\b\slave\chrome-official\build\src\third_party\libxml\xpath.c @ 14930]
0024a3e4 68086868 chrome_676c0000!xsltNumberFormatGetValue(struct _xmlXPathContext * context = 0xce0024c9, struct _xmlNode * node = 0x68078044, unsigned char * value = 0x00dab6a8 "", double * number = 0x00da8ae0)+0x43 [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\numbers.c @ 715]
0024f428 68078044 chrome_676c0000!xsltNumberFormat(struct _xsltTransformContext * ctxt = 0x00000003, struct _xsltNumberData * data = 0x00dab6a8, struct _xmlNode * node = 0x00da8ae0)+0x8a [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\numbers.c @ 768]
0024f438 68076237 chrome_676c0000!xsltNumber(struct _xsltTransformContext * ctxt = 0x00de8a20, struct _xmlNode * node = 0x00da8ae0, struct _xmlNode * inst = 0x00e3cf80, struct _xsltStylePreComp * castedComp = 0x00dab630)+0x4e [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 4494]
0024f498 68078f1d chrome_676c0000!xsltApplySequenceConstructor(struct _xsltTransformContext * ctxt = 0x00de8a20, struct _xmlNode * contextNode = 0x00da8ae0, struct _xmlNode * list = 0x00e3cf80, struct _xsltTemplate * templ = 0x00000000)+0x199 [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 2597]
0024f518 68076237 chrome_676c0000!xsltForEach(struct _xsltTransformContext * ctxt = 0x00000001, struct _xmlNode * contextNode = 0x00da8ae0, struct _xmlNode * inst = 0x00e3c780, struct _xsltStylePreComp * castedComp = 0x00daad50)+0x25e [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 5628]
0024f578 680768cc chrome_676c0000!xsltApplySequenceConstructor(struct _xsltTransformContext * ctxt = 0x00de8a20, struct _xmlNode * contextNode = 0x00da8ae0, struct _xmlNode * list = 0x00e3c780, struct _xsltTemplate * templ = 0x00e3ce80)+0x199 [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 2597]
0024f5b4 68075eda chrome_676c0000!xsltApplyXSLTTemplate(struct _xsltTransformContext * ctxt = 0x00de8a20, struct _xmlNode * contextNode = 0x00da8ae0, struct _xmlNode * list = 0x00e3c780, struct _xsltTemplate * templ = 0x00e3ce80, struct _xsltStackElem * withParams = 0x00000000)+0x195 [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 3050]
0024f5e4 68079594 chrome_676c0000!xsltProcessOneNode(struct _xsltTransformContext * ctxt = 0x00de8a20, struct _xmlNode * contextNode = 0x00da8ae0, struct _xsltStackElem * withParams = 0x00000000)+0x150 [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 2047]
0024f61c 67c4221b chrome_676c0000!xsltApplyStylesheetInternal(struct _xsltStylesheet * style = 0x00dae460, struct _xmlDoc * doc = 0x00da8ae0, char ** params = 0x0024f654, char * output = 0x0024f654 "???", struct _iobuf * profile = 0x0024f654, struct _xsltTransformContext * userCtxt = 0x00de8a20)+0x3e4 [c:\b\slave\chrome-official\build\src\third_party\libxslt\libxslt\transform.c @ 6049]
0024f654 67b37bce chrome_676c0000!WebCore::XSLTProcessor::transformToString(class WebCore::Node * sourceNode = 0x00000000, class WebCore::String * mimeType = 0x0024f680, class WebCore::String * resultString = 0x0024f684, class WebCore::String * resultEncoding = 0x0024f694)+0x135 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\xml\xsltprocessorlibxslt.cpp @ 310]
0024f688 67b355f2 chrome_676c0000!WebCore::Document::applyXSLTransform(class WebCore::ProcessingInstruction * pi = 0x00000000)+0x62 [c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\dom\document.cpp @ 4244]

### in...@chromium.org (2010-10-11)

Thanks @minhbq for this nice bug.

Memory corruption reproduces in both v7 trunk and v6 stable.

### in...@chromium.org (2010-10-11)

Evan, this is a bug in the current shipping version of libxml. Do you know the process for upstreaming bugs to libxml since you dealt with it last ?

### [Deleted User] (2010-10-11)

libxml FFFFFUUUU.

I don't think I upstreamed any bugs to them, but we should definitely take this upstream.

$ xsltproc --version; xsltproc demo.xml 
Using libxml 20706, libxslt 10126 and libexslt 815
xsltproc was compiled against libxml 20706, libxslt 10126 and libexslt 815
libxslt 10126 was compiled against libxml 20706
libexslt 815 was compiled against libxml 20706
Segmentation fault



### in...@chromium.org (2010-10-11)

Chris, I can file a bug on https://bugzilla.gnome.org/enter_bug.cgi?product=libxml2 but i dont see any way to hide with security tags. What to do then ? File it or contact the devs somehow channel ??

### [Deleted User] (2010-10-11)

I'm trying the IRC channel.  You could also mail the main dev directly, maybe.

### in...@chromium.org (2010-10-11)

Thanks Evan, I will let you handle it. If we dont get any response over IRC, then we can email them.

### [Deleted User] (2010-10-11)

I got no response.  :(  Can you email them?

### in...@chromium.org (2010-10-11)

Sent an email to Developer Daniel Veillard (daniel@veillard.com) [http://xmlsoft.org/bugs.html].

### mi...@bkav.com.vn (2010-10-12)

I checked other browsers. Safari is also affected by this bug.

### in...@chromium.org (2010-10-12)

Thanks @minhbq. Daniel has responded very quickly and came up a patch. He will be working on the disclosure process with RedHat. We will keep you updated.

### in...@chromium.org (2010-10-12)

[Empty comment from Monorail migration]

### la...@chromium.org (2010-10-12)

Bulk moving to mstone 8, at this point work on m7 should effectively be closed.  If something in this bulk edit is not actively being worked on, please change the mstone to m9.

### in...@chromium.org (2010-10-12)

We should aim v7 1st patch for this.

### in...@chromium.org (2010-10-12)

Trybot run for win, linux seems ok. http://codereview.chromium.org/3712004. Waiting for Daniel's reply before merging to trunk.

### [Deleted User] (2010-10-13)

If you can, run it through the layout test trybots.  They'll pick up any change in pages that rely on XSLT.

From the docs:
"Use layout try bots -- because they build in Debug. Any ASSERTs will be revealed on the try bots. Run them both through the standard set and  layout test try bots (gcl try foo --bot layout_win,layout_mac,layout_linux,layout_win_rel,layout_mac_rel,layout_linux_rel).
Tip: Linux layout bot runs almost twice the speed of the other platforms and will likely show the same debug crashes as other platforms."

### [Deleted User] (2010-10-13)

If you can, run it through the layout test trybots.  They'll pick up any change in pages that rely on XSLT.

From the docs:
"Use layout try bots -- because they build in Debug. Any ASSERTs will be revealed on the try bots. Run them both through the standard set and  layout test try bots (gcl try foo --bot layout_win,layout_mac,layout_linux,layout_win_rel,layout_mac_rel,layout_linux_rel).
Tip: Linux layout bot runs almost twice the speed of the other platforms and will likely show the same debug crashes as other platforms."

### in...@chromium.org (2010-10-13)

Thanks a lot Evan. I added these layout bots to the try run. 

### sc...@gmail.com (2010-10-13)

Yeah, I've worked with Daniel a bit and he's fast on security bugs :)

### sc...@gmail.com (2010-10-13)

@inferno: i'd like to see this merged to M7 if at all humanly possible. Open source projects have been known to disclose arbitrarily on their own timelines (see: Linux kernel). Also, we should make sure Daniel credits the correct person.

### sc...@gmail.com (2010-10-13)

@minhbq: what name should we use for credit in our release notes?

### mi...@bkav.com.vn (2010-10-13)

This is my information for credit: Bui Quang Minh from Bkis (www.bkis.com)

### in...@chromium.org (2010-10-13)

Mail from Daniel (ccing)
--------------------
Actually, looking at the bug, I don't think it really affects much
deployment in linux environment, it's only if the user trusts downloaded
stylesheets, standalone or embbeded, or XPath queries coming from
untrusted sources. This would affect Chrome and Safari but not really
Linux usual scenarios.
 So I think it's best if you get this though, maybe through CERT
or another channel which may be appropriate, but it should raise the
problem to Apple/Red Hat/Sun-Oracle

Please keep me updated with the progress, a 2-3 weeks timeframe
before disclosure sounds fine to me.

### sc...@gmail.com (2010-10-15)

I can ping vendor-sec on this.

Daniel, if you're happy with your fix, feel free to commit it upstream with a nondescript commit log ;-) It will be nice to have an official URL to link to.

### sc...@gmail.com (2010-10-15)

BTW, great bug Bui Quang! I will get the rewards panel to consider this, once we have merged the fix. We'd appreciate it if you continue to keep the details confidential.

### mi...@bkav.com.vn (2010-10-15)

OK. Thank you. 

### ve...@gmail.com (2010-10-15)

w.r.t. #24, yes please, contact vendor-sec, that's the best, thanks !
I already commited as such but not pushed yet to GNOME git, will do today,
I'm also pushing other fixes to not raise specific concerns,

Daniel

### ve...@gmail.com (2010-10-15)

The commit pushed upstream:

http://git.gnome.org/browse/libxml2/commit/?id=91d19754d46acd4a639a8b9e31f50f31c78f8c9c

Daniel

### sc...@gmail.com (2010-10-15)

@minhbq: congratulations! This bug has provisionally qualified for a $1000 Chromium Security Reward.

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

### sc...@gmail.com (2010-10-15)

Oh -- and a bit more detail why the reward amount is higher than the base $500. The panel was impressed by the quality of the report: small, simple repro along with symbolized stack trace indicating corrupt registers. Thank you!

### bu...@gmail.com (2010-10-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=62828

------------------------------------------------------------------------
r62828 | cevans@chromium.org | Fri Oct 15 17:58:12 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/xpath.c?r1=62828&r2=62827&pathrev=62828
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=62828&r2=62827&pathrev=62828

Pull in XPath fix from upstream.

BUG=58731
TEST=NONE

Review URL: http://codereview.chromium.org/3839002
------------------------------------------------------------------------

### sc...@gmail.com (2010-10-16)

[Empty comment from Monorail migration]

### ve...@gmail.com (2010-10-16)

@scarybeasts: what's the status on getting this through vendor-sec ? I would really
like to make sure that others and especially Apple get it quickly. If needed I will
try to reach them directly...

Daniel

### sc...@gmail.com (2010-10-18)

@veillard: I'll take care of this right now.

### sc...@gmail.com (2010-10-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-10-18)

@veillard: done, both Apple and vendor-sec

### ve...@gmail.com (2010-10-18)

@scarybeasts: thanks ! keep up updated on the expected disclosure timeframe
I will try to schedule a release accordingly,

Daniel 

### sc...@gmail.com (2010-10-19)

Likely disclosure date for now is something like Nov 3rd 2010.

### sc...@gmail.com (2010-10-19)

[Empty comment from Monorail migration]

### ve...@gmail.com (2010-10-19)

Okay, thanks !

Daniel

### mi...@bkav.com.vn (2010-10-19)

Thank you for reporting to xmlsoft, Apple, vendor-sec.
And thank you for reward :)

### sc...@gmail.com (2010-10-19)

[Empty comment from Monorail migration]

### te...@gmail.com (2010-10-20)

Does this issue got a cve id?

### sc...@gmail.com (2010-10-20)

Not that I know of. You have the power to allocate one? :)

### te...@gmail.com (2010-10-20)

No.

I suggest you request one in the list.  :)

### ve...@gmail.com (2010-10-20)

BTW the title for this bug is wrong, it's not a memory corruption,
it's an invalid memory access, the in-memory structures are just fine.

Daniel

### sc...@gmail.com (2010-10-20)

@veillard: agree.
The attacker does control a pointer to an xmlNode, though, which implies full control over the contents of that struct. I'd be very surprised if that didn't confer arbitrary code execution via second- or third- order effects.

Generally, the Chromium project doesn't quibble about exploitability. We prefer to fix fast (and pay ;-) as appropriate.


### mi...@bkav.com.vn (2010-10-20)

@veillard: In my opinion, Either "Memory Corruption" or "Invalid memory Access" is acceptable:  http://en.wikipedia.org/wiki/Memory_corruption

But, I think also your title is more regular. Thank you.


### sc...@gmail.com (2010-10-20)

[Empty comment from Monorail migration]

### th...@googlemail.com (2010-10-21)

SUSE is fine with the release date. Thanks.

### ve...@gmail.com (2010-10-21)

Is there a CVE allocated to this issue ?

Daniel

### sc...@gmail.com (2010-10-21)

[Empty comment from Monorail migration]

### jo...@gmail.com (2010-10-22)

I believe the libxml2 patch for this issue changed the behavior of `following::` and `preceding::` axes to always return an empty list. I don't think that is what the spec says, so I opened a bug on Gnome bugzilla. I do believe this security issue was fixed, but introduce this bug as well. Keep an eye on the gnome bug to see if the fix for that doesn't regress this issue:
https://bugzilla.gnome.org/show_bug.cgi?id=632838


### ve...@gmail.com (2010-10-22)

Okay, this additional patch is then needed to get back `following::` and `preceding::` axis to the normal behaviour:

http://git.gnome.org/browse/libxml2/commit/?id=ea90b894146030c214a7df6d8375310174f134b9

I now get similar output with Saxon when walking those axis from an attribute node.
So both patches should be applied I think.

  thanks for raising the issue,

Daniel

### sc...@gmail.com (2010-10-22)

CVE-2010-4008

### bu...@gmail.com (2010-10-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=63572

------------------------------------------------------------------------
r63572 | cevans@chromium.org | Fri Oct 22 15:06:33 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/xpath.c?r1=63572&r2=63571&pathrev=63572
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=63572&r2=63571&pathrev=63572

Apply behaviour change fix from upstream for previous XPath change.

BUG=58731
TEST=NONE

Review URL: http://codereview.chromium.org/4027006
------------------------------------------------------------------------

### sc...@gmail.com (2010-10-22)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-10-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=63581

------------------------------------------------------------------------
r63581 | cevans@chromium.org | Fri Oct 22 15:44:23 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/517/src/third_party/libxml/src/xpath.c?r1=63581&r2=63580&pathrev=63581
 M http://src.chromium.org/viewvc/chrome/branches/517/src/third_party/libxml/README.chromium?r1=63581&r2=63580&pathrev=63581

Merge 62828 - Pull in XPath fix from upstream.

BUG=58731
TEST=NONE

Review URL: http://codereview.chromium.org/3839002

TBR=inferno@chromium.org
Review URL: http://codereview.chromium.org/4054006
------------------------------------------------------------------------

### bu...@gmail.com (2010-10-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=63584

------------------------------------------------------------------------
r63584 | cevans@chromium.org | Fri Oct 22 15:46:14 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/517/src/third_party/libxml/src/xpath.c?r1=63584&r2=63583&pathrev=63584
 M http://src.chromium.org/viewvc/chrome/branches/517/src/third_party/libxml/README.chromium?r1=63584&r2=63583&pathrev=63584

Merge 63572 - Apply behaviour change fix from upstream for previous XPath change.

BUG=58731
TEST=NONE

Review URL: http://codereview.chromium.org/4027006

TBR=inferno@chromium.org
Review URL: http://codereview.chromium.org/4032005
------------------------------------------------------------------------

### sc...@gmail.com (2010-10-22)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-10-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=63591

------------------------------------------------------------------------
r63591 | cevans@chromium.org | Fri Oct 22 16:15:17 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/third_party/libxml/src/xpath.c?r1=63591&r2=63590&pathrev=63591
 M http://src.chromium.org/viewvc/chrome/branches/552/src/third_party/libxml/README.chromium?r1=63591&r2=63590&pathrev=63591

Merge 62828 - Pull in XPath fix from upstream.

BUG=58731
TEST=NONE

Review URL: http://codereview.chromium.org/3839002

TBR=inferno@chromium.org
Review URL: http://codereview.chromium.org/4021005
------------------------------------------------------------------------

### bu...@gmail.com (2010-10-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=63593

------------------------------------------------------------------------
r63593 | cevans@chromium.org | Fri Oct 22 16:17:02 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/third_party/libxml/src/xpath.c?r1=63593&r2=63592&pathrev=63593
 M http://src.chromium.org/viewvc/chrome/branches/552/src/third_party/libxml/README.chromium?r1=63593&r2=63592&pathrev=63593

Merge 63572 - Apply behaviour change fix from upstream for previous XPath change.

BUG=58731
TEST=NONE

Review URL: http://codereview.chromium.org/4027006

TBR=inferno@chromium.org
Review URL: http://codereview.chromium.org/4002004
------------------------------------------------------------------------

### [Deleted User] (2010-10-26)

Works fine with Google Chrome 8.0.552.18 (Official Build 63841) on Win7 and Linux Ubuntu 10.04 Lucid.

### js...@chromium.org (2010-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-02)

I think our release will go out Nov 4 (not Nov 3 as originally suggested).

### [Deleted User] (2010-11-02)

Works fine with Google Chrome 7.0.517.44 (Official Build 64615) as well.

### mi...@bkav.com.vn (2010-11-03)

Hi scarybeasts,

Thanks for your information about the release. And I also would like to know more details about what you have exchanged with Apple around the bug and when Apple is going to issue the patch. It would be great if I can see the information is exchanged.

Thank you.

### sc...@gmail.com (2010-11-03)

I believe Apple are going to release a Safari update on Nov 15 or so.

We will credit you in our release notes but keep the full details of this bug private until at least Nov 15.


### sc...@gmail.com (2010-11-21)

Payment is in the electronic system.

### ve...@gmail.com (2010-11-22)

 ??? what does that mean ?

Daniel

### sc...@gmail.com (2010-11-22)

@veillard: which bit?

### ve...@gmail.com (2010-11-22)

  I would assume this is related to the reward for minhbq@bkav.com.vn
and I was surprized
to get a mail about this maybe it's related to an associated bugzilla
state change, that's all

Daniel

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

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

### pa...@chromium.org (2013-12-20)

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

This issue was migrated from crbug.com/chromium/58731?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083706)*
