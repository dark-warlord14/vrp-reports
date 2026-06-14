# Stack-buffer-overflow in _canonicalize

| Field | Value |
|-------|-------|
| **Issue ID** | [40051839](https://issues.chromium.org/issues/40051839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2011-12-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

ASan reports a stack buffer overflow for a page with a long -webkit-locale. This would otherwise look like <http://code.google.com/p/chromium/issues/detail?id=95486>, but here instead of a null crash the address moves easily with the locale string, so reporting as a separate potential security bug.

**VERSION**  

Chrome Version: 17.0.962.0 (Developer Build 112977)  

Operating System: Linux (Debian 6.0.3, x86\_64)

**REPRODUCTION CASE**  

data:text/html,<div style="-webkit-locale: 'en\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US\_US'">

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==16611== ERROR: AddressSanitizer stack-buffer-overflow on address 0x7fffffff5e69 at pc 0x7ffff09f4744 bp 0x7fffffff5830 sp 0x7fffffff5808  

READ of size 1 at 0x7fffffff5e69 thread T0  

#0 0x7ffff09f4744 in \_canonicalize  

#1 0x7ffff094c9ed in uloc\_addLikelySubtags\_46  

#2 0x7ffff582db2b in WebCore::localeToScriptCodeForFontSelection(WTF::String const&)  

#3 0x7ffff2bb3a67 in WebCore::CSSStyleSelector::applyProperty(int, WebCore::CSSValue\*)  

#4 0x7ffff2b9c0d8 in void WebCore::CSSStyleSelector::applyDeclarations<true>(bool, int, int, bool)  

#5 0x7ffff2b984ee in WebCore::CSSStyleSelector::applyMatchedDeclarations(WebCore::CSSStyleSelector::MatchResult const&)  

#6 0x7ffff2b89504 in WebCore::CSSStyleSelector::styleForElement(WebCore::Element\*, WebCore::RenderStyle\*, bool, bool)  

#7 0x7ffff23a61d5 in WebCore::Element::styleForRenderer()  

#8 0x7ffff23f7425 in WebCore::NodeRendererFactory::createRendererIfNeeded()  

#9 0x7ffff23d83f6 in WebCore::Node::createRendererIfNeeded()  

#10 0x7ffff23a4945 in WebCore::Element::attach()  

#11 0x7ffff2726118 in WTF::PassRefPtr[WebCore::Element](javascript:void(0);) WebCore::HTMLConstructionSite::attach[WebCore::Element](javascript:void(0);)(WebCore::ContainerNode\*, WTF::PassRefPtr[WebCore::Element](javascript:void(0);))  

#12 0x7ffff272a0a6 in WebCore::HTMLConstructionSite::insertHTMLElement(WebCore::AtomicHTMLToken&)  

#13 0x7ffff269657b in WebCore::HTMLTreeBuilder::processStartTagForInBody(WebCore::AtomicHTMLToken&)  

#14 0x7ffff2683221 in WebCore::HTMLTreeBuilder::processStartTag(WebCore::AtomicHTMLToken&)  

#15 0x7ffff26822bf in WebCore::HTMLTreeBuilder::processToken(WebCore::AtomicHTMLToken&)  

#16 0x7ffff2681e95 in WebCore::HTMLTreeBuilder::constructTreeFromAtomicToken(WebCore::AtomicHTMLToken&)  

#17 0x7ffff2681d8e in WebCore::HTMLTreeBuilder::constructTreeFromToken(WebCore::HTMLToken&)  

#18 0x7ffff263a0fb in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode)  

#19 0x7ffff263bbf4 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&)  

#20 0x7ffff57750a1 in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*)  

#21 0x7ffff2f1b339 in WebCore::DocumentWriter::endIfNotLoadingMainResource()  

#22 0x7ffff2f57c19 in WebCore::FrameLoader::finishedLoading()  

#23 0x7ffff2f7f574 in WebCore::MainResourceLoader::didFinishLoading(double)  

#24 0x7ffff45cdd3a in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::Time const&)  

#25 0x7ffff1ccef9b in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::Time const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::Time const&))  

#26 0x7ffff1ccce10 in ResourceDispatcher::DispatchMessage(IPC::Message const&)  

#27 0x7ffff1ccab50 in ResourceDispatcher::OnMessageReceived(IPC::Message const&)  

#28 0x7ffff1bdd6ba in ChildThread::OnMessageReceived(IPC::Message const&)  

#29 0x7ffff1d1fef9 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&)  

#30 0x7ffff0625e1f in MessageLoop::RunTask(base::PendingTask const&)  

#31 0x7ffff06266b6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&)  

#32 0x7ffff06279b1 in MessageLoop::DoWork()  

#33 0x7ffff0632287 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*)  

#34 0x7ffff0624a1e in MessageLoop::RunInternal()  

#35 0x7ffff0622d6f in MessageLoop::Run()  

#36 0x7ffff50c16fa in RendererMain(content::MainFunctionParams const&)  

#37 0x7ffff057e8a6 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*)  

#38 0x7ffff057dd64 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*)  

#39 0x7fffeee725f7 in ChromeMain  

#40 0x7fffeee7251b in main  

#41 0x7fffe84bfc4d in \_\_libc\_start\_main  

#42 0x7fffeee72439 in \_start  

Address 0x7fffffff5e69 is located at offset 585 in frame <uloc\_addLikelySubtags\_46> of T0's stack:  

This frame has 7 object(s):  

[32, 44) 'lang.i'  

[96, 100) 'langLength.i'  

[160, 166) 'script.i'  

[224, 228) 'scriptLength.i'  

[288, 292) 'region.i'  

[352, 356) 'regionLength.i'  

[416, 573) 'localeBuffer'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism  

(longjmp and C++ exceptions \*are\* supported)  

==16611== ABORTING  

Shadow byte and word:  

0x1fffffffebcd: f3  

0x1fffffffebc8: 00 00 00 05 f3 f3 f3 f3  

More shadow bytes:  

0x1fffffffeba8: 04 f4 f4 f4 f2 f2 f2 f2  

0x1fffffffebb0: 04 f4 f4 f4 f2 f2 f2 f2  

0x1fffffffebb8: 00 00 00 00 00 00 00 00  

0x1fffffffebc0: 00 00 00 00 00 00 00 00  

=>0x1fffffffebc8: 00 00 00 05 f3 f3 f3 f3  

0x1fffffffebd0: 00 00 00 00 00 00 00 00  

0x1fffffffebd8: 00 00 00 00 f1 f1 f1 f1  

0x1fffffffebe0: 00 00 00 00 00 00 00 00  

0x1fffffffebe8: 00 00 00 00 00 00 00 00

## Attachments

- [sbf.html](attachments/sbf.html) (text/plain; charset=us-ascii, 203 B)

## Timeline

### pa...@google.com (2011-12-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=3132562

Uploader: palmer@chromium.org

Crash Type: Stack-buffer-overflow READ 1
Crash Address: 0x7f2f37d82ae9
Crash State:
  - crash stack -
  _canonicalize
  uloc_addLikelySubtags_46
  WebCore::localeToScriptCodeForFontSelection
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv972LqDhG1Jbq8NfryMdMMouGIoBEGRrXI1SVXkwXXz1v09iyzooo8GITcVQEA0_6BH_vZQouOfqa-JZrnGqyeRHbvqUwQ72vXw3ICl3uj7mqz_nkXYMIn89u3QbQTeEwVPBFgS-ulEvBnU6nQlFjvTC7AZW5g

### in...@chromium.org (2011-12-05)

Matt, can you please take a look. It is probably coming from http://trac.webkit.org/changeset/92375

### in...@chromium.org (2011-12-05)

[Empty comment from Monorail migration]

### kc...@chromium.org (2011-12-05)

Report with line numbers: 
READ of size 1 at 0x7f9c59285e4c thread T0                                                                                                                                                          
    #0 0x7f9c6b3ac354 in _canonicalize third_party/icu/source/common/uloc.c:1808                                                                                                                    
    #1 0x7f9c6b301417 in do_canonicalize third_party/icu/source/common/loclikely.cpp:1201                                                                                                           
    #2 0x7f9c7043461f in WebCore::localeToScriptCodeForFontSelection(WTF::String const&) third_party/WebKit/Source/WebCore/platform/text/LocaleToScriptMappingICU.cpp:62 

_canonicalize not only reads the second parameter, but also writes to it.
So, unless I am mistaken, this is a controllable stack buffer overwrite. 

### in...@chromium.org (2011-12-05)

[Empty comment from Monorail migration]

### fa...@chromium.org (2011-12-06)

It looks like an issue in ICU _canonicalize.  It's accessing result past resultCapacity.  I'll try to make a patch for ICU.

### fa...@chromium.org (2011-12-06)

http://codereview.chromium.org/8822005/

(I marked it private since this bug is private.)

### bu...@chromium.org (2011-12-08)

Commit: c9287557a495aad7ff3faef2ac850c85caf842c9
 Email: falken@chromium.org@4ff67af0-8c30-449e-8e8b-ad334ec8d88c

Fix buffer overflow in _canonicalize.

Upstream bug is http://bugs.icu-project.org/trac/ticket/8984

BUG=chromium:106441
Review URL: http://codereview.chromium.org/8822005

git-svn-id: http://src.chromium.org/svn/trunk/deps/third_party/icu46@113543 4ff67af0-8c30-449e-8e8b-ad334ec8d88c

M	README.chromium
A	patches/canonicalize.patch
M	source/common/uloc.c

### fa...@chromium.org (2011-12-08)

Fixed in http://src.chromium.org/viewvc/chrome?view=rev&revision=113543

Does the security team recommend merging to M16/M17?

### in...@chromium.org (2011-12-08)

Yes, we will handle the merges.

### js...@chromium.org (2011-12-08)

Actually, ICU has to be rolled over. The CL (mentioned above) alone has null effect :-) I'll roll ICU to 113543. 
I've just done it. 
@inferno, would you take care of DEPS file changes in branches? I can do that, too. 





### in...@chromium.org (2011-12-08)

Jshin@, we can handle the merges. We just need to roll over DEPS for ICU to 113543 right? Thanks a lot guys for the fix.

### ao...@gmail.com (2011-12-15)

Will this one be going to the reward panel?

### in...@chromium.org (2011-12-15)

Yes definitely Aki. Sometimes, there can be latency in adding those labels to bugs, but it does eventually go to the rewards panel when we are closer to the next stable release.

### ao...@gmail.com (2011-12-15)

@inferno Thanks. Wouldn't have hurried otherwise, but the number of queued bugs currently affects some Christmas plans :)

### bu...@chromium.org (2011-12-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=114854

------------------------------------------------------------------------
r114854 | jungshik@google.com | Fri Dec 16 12:56:02 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/DEPS?r1=114854&r2=114853&pathrev=114854

Merge 113644 - Roll over ICU to 113543
(the actual DEPS file for the release build will be done separately).

1. Moscow timezone fix and some miscellaneous locale fixes
  (icu@r=113037 See http://crrev.com/113037 )

2. Fix buffer overflow in _canonicalize.

  Upstream bug is http://bugs.icu-project.org/trac/ticket/8984

  The actual fix is at
   http://codereview.chromium.org/8822005

BUG=106441
TBR=falken
Review URL: http://codereview.chromium.org/8873031

TBR=jshin@chromium.org
Review URL: http://codereview.chromium.org/8964020
------------------------------------------------------------------------

### sc...@gmail.com (2011-12-21)

@aohelin: nice bug and obviously deserves a $1000 Chromium Security Reward.

It looks like this affected M15 stable (SecImpacts-Stable label is present) but we failed to include this in the M16 release notes. Sorry about that. I'll make sure the Hall of Fame gets updated correctly.

### [Deleted User] (2011-12-21)

Actually, looks like this still needs to be merged to M16 for the first M16 patch.

### ao...@gmail.com (2011-12-21)

@scarybeasts Excellent! Project Christmas fuzz can help a few more families going through rough times with this. Ho ho :)

### js...@chromium.org (2011-12-21)

@cevans : You're right that it's not been merged to M16. I'll add you to the thread discussing this issue. 


### js...@chromium.org (2012-01-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-19)

To risky to back-merge to ICU for M16. Already merged in a DEPS roll to m17.

### in...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-08)

Reward upped to $1337 and sent to American Red Cross.
Sigh..... I'll do the other three similarly when the stupid web site starts accepting my credit card again.

### sc...@gmail.com (2012-02-08)

Misunderstanding.

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### js...@chromium.org (2012-08-07)

Lifting restricted view. It's been fixed since M17 and CVE, RedHat, Debian bug trackers are all visible. 



### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=20705

------------------------------------------------------------------------
r20705 | jungshik@google.com | 2011-12-16T21:07:06.181952Z

------------------------------------------------------------------------

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 113603:113869.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=3132562

Uploader: palmer@chromium.org

Crash Type: Stack-buffer-overflow READ 1
Crash Address: 0x7f190968cae9
Crash State:
  - crash stack -
  _canonicalize
  uloc_addLikelySubtags_46
  WebCore::localeToScriptCodeForFontSelection
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=113603:113869

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94CBm_SS1cem-XrWG9-5BIJu3RpysNuyZEP3tT62i-TlS95PZvleP9e46JjqBp7rhmDn4STY1IdWvP_FPGsOTjJj8yXJF82n699bASkbReryMPdOwLOgYLTs5Z4yO_ziMNQoLOYuFcK6llclgYocQ1vFRpDrg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/106441?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051839)*
