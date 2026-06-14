# Security: Information leak in xsltFormatNumberConversion (libxslt)

| Field | Value |
|-------|-------|
| **Issue ID** | [40084524](https://issues.chromium.org/issues/40084524) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2016-4607 |
| **Reporter** | we...@aevum.de |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-06-10 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

Due to a missing string termination check, libxslt's format-number function can leak bytes after the heap-allocated buffer that holds the pattern string.

**VERSION**  

Chrome Version: 51.0.2704.84 stable  

Operating System: Windows 10, 64-bit  

Operating System: OS X 10.11.5

**REPRODUCTION CASE**  

See the attached files format-number-leak-poc.xml and format-number-leak-poc.xsl. If you open the XML file locally, make sure to run Chrome with --allow-file-access-from-files. In some cases, loading the POC results in an infinite loop and the file must be reloaded.

DETAILS  

When processing the decimal separator, the libxslt function xsltFormatNumberConversion doesn't check for a zero byte terminating the pattern string. This can be exploited to reveal bytes after the string buffer on the heap.

To make this work, the decimal separator must be set to the empty string which makes libxslt use a zero byte as decimal separator. Further care has to be taken to avoid placing the zero decimal separator in the output string, terminating the output before the leaked bytes. To achieve this, the pattern has to include at least one integer digit (hash or zero), at least one hash in the fraction part, and no zero digits in the fraction part. To get a hash into the fraction part, the byte immediately following the pattern string has to be guessed. The POC tries multiples of eight between 0x20 and 0x78 (only valid XML chars and valid UTF-8 sequences can be used) and uses several hundred iterations.

The POC also uses various buffer sizes for the pattern string: multiples of four ranging from 4 to 160. When memory for the pattern string is allocated, an area previously occupied by a similar-sized object is often used. I think that in most cases, the leak allows to read the last bytes of these objects after they were freed and sometimes the first bytes of the following heap chunk. Consequently, many of the leaked bytes seem to be heap addresses.

Limitations:

- Only contents up to the first zero byte are leaked.
- The leaked bytes must pass some loose UTF-8 checks in xsltUTF8Size.
- The POC won't show invalid XML characters (0x01-0x1F with the exception of tab, CR, and LF). They're stripped from the output.
- If a single quote character is hit, libxslt goes into an infinite loop.

Possible improvements:

- Other "special" characters of the decimal format could be set to rare UTF-8 code points to increase the number of hits.
- Code that stresses the heap allocator could be executed at certain intervals to get more and different hits.
- Experiment with different pattern string sizes and guessed bytes.

PATCH  

I also attached a patch that fixes the problem.

DISCLOSURE  

I'm an active libxslt committer, but I haven't shared details about this issue with anyone, and I don't plan to do so until it is fixed in Webkit browsers. This bug was found with afl-fuzz and ASan.

## Attachments

- [format-number-leak-poc.xml](attachments/format-number-leak-poc.xml) (text/plain, 968 B)
- [format-number-leak-poc.xsl](attachments/format-number-leak-poc.xsl) (text/plain, 3.7 KB)
- [format-number-leak.diff](attachments/format-number-leak.diff) (application/octet-stream, 535 B)

## Timeline

### np...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

[Monorail components: Blink>XML]

### np...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-11)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-06-11)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-06-17)

Thank you for filing this interesting bug w/ POC and fix. Here's how content_shell chokes on this:

[120624:120643:0617/153418:258101006351:ERROR:entry.cc(172)] Entry::Deserialize: manifest_version must be an integer.
=================================================================
==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6020000321d4 at pc 0x00000b5c27ea bp 0x7ffd1c808130 sp 0x7ffd1c808128
READ of size 1 at 0x6020000321d4 thread T0 (content_shell)
    #0 0xb5c27e9 in xsltFormatNumberConversion ./out/asan/../../third_party/libxslt/libxslt/numbers.c:1107:12
    #1 0xb5ba578 in ?? ./out/asan/../../third_party/libxslt/libxslt/functions.c:640:6
    #2 0xb52408d in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13597:17
    #3 0xb522e1b in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13988:26
    #4 0xb52248a in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13617:26
    #5 0xb522365 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13609:26
    #6 0xb521981 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13540:25
    #7 0xb522e1b in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13988:26
    #8 0xb5134e4 in xmlXPathRunEval ./out/asan/../../third_party/libxml/src/xpath.c:14563:2
    #9 0xb5125d3 in xmlXPathCompiledEvalInternal ./out/asan/../../third_party/libxml/src/xpath.c:14930:11
    #10 0xb5122ee in ?? ./out/asan/../../third_party/libxml/src/xpath.c:14993:5
    #11 0xb59fdc0 in xsltEvalVariable ./out/asan/../../third_party/libxslt/libxslt/variables.c:903:11
    #12 0xb5a1606 in xsltBuildVariable ./out/asan/../../third_party/libxslt/libxslt/variables.c:1773:19
    #13 0xb5a1606 in xsltRegisterVariable ./out/asan/../../third_party/libxslt/libxslt/variables.c:1835:0
    #14 0xb58f3e4 in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2775:3
    #15 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #16 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #17 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2
    #18 0xb58ecaa in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2755:17
    #19 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #20 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #21 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2
    #22 0xb58ecaa in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2755:17
    #23 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #24 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #25 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2
    #26 0xb58ecaa in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2755:17
    #27 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #28 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #29 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2
    #30 0xb58ecaa in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2755:17
    #31 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #32 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #33 0xb59b041 in xsltApplyStylesheetInternal ./out/asan/../../third_party/libxslt/libxslt/transform.c:6054:5
    #34 0x52ba581 in transformToString ./out/asan/../../third_party/WebKit/Source/core/xml/XSLTProcessorLibxslt.cpp:338:31
    #35 0x526dd2d in applyXSLTransform ./out/asan/../../third_party/WebKit/Source/core/xml/DocumentXSLT.cpp:109:21
    #36 0x526e6a9 in sheetLoaded ./out/asan/../../third_party/WebKit/Source/core/xml/DocumentXSLT.cpp:173:13
    #37 0x3d2e155 in sheetLoaded ./out/asan/../../third_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:186:14
    #38 0x3d2f188 in setXSLStyleSheet ./out/asan/../../third_party/WebKit/Source/core/dom/ProcessingInstruction.cpp:228:5
    #39 0x4bc6c9c in checkNotify ./out/asan/../../third_party/WebKit/Source/core/fetch/XSLStyleSheetResource.cpp:90:12
    #40 0x4b8d0dd in finish ./out/asan/../../third_party/WebKit/Source/core/fetch/Resource.cpp:414:5
    #41 0x4bac747 in didFinishLoading ./out/asan/../../third_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:925:19
    #42 0x175d9df in OnCompletedRequest ./out/asan/../../content/child/web_url_loader_impl.cc:764:16
    #43 0x17016ce in OnRequestComplete ./out/asan/../../content/child/resource_dispatcher.cc:379:9
    #44 0x1706398 in DispatchToMethodImpl<content::ResourceDispatcher *, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), int, content::ResourceRequestCompletionStatus, 0, 1> ./out/asan/../../base/tuple.h:126:3
    #45 0x1706398 in DispatchToMethod<content::ResourceDispatcher *, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), int, content::ResourceRequestCompletionStatus> ./out/asan/../../base/tuple.h:133:0
    #46 0x1706398 in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &), void, std::__1::tuple<int, content::ResourceRequestCompletionStatus> > ./out/asan/../../ipc/ipc_message_templates.h:26:0
    #47 0x1706398 in Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void, void (content::ResourceDispatcher::*)(int, const content::ResourceRequestCompletionStatus &)> ./out/asan/../../ipc/ipc_message_templates.h:121:0
    #48 0x16fbfdf in DispatchMessage ./out/asan/../../content/child/resource_dispatcher.cc:510:5
    #49 0x16fad41 in OnMessageReceived ./out/asan/../../content/child/resource_dispatcher.cc:126:3
    #50 0xacf7e8f in Run<std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > ./out/asan/../../base/bind_internal.h:160:12
    #51 0xacf7e8f in MakeItSo<base::internal::RunnableAdapter<void (*)(std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> >)> &, std::__1::unique_ptr<blink::WebTaskRunner::Task, std::__1::default_delete<blink::WebTaskRunner::Task> > > ./out/asan/../../base/bind_internal.h:312:0
    #52 0xacf7e8f in Run ./out/asan/../../base/bind_internal.h:364:0
    #53 0x835f034 in Run ./out/asan/../../base/callback.h:397:12
    #54 0x835f034 in RunTask ./out/asan/../../base/debug/task_annotator.cc:51:0
    #55 0xad0c1bb in ProcessTaskFromWorkQueue ./out/asan/../../components/scheduler/base/task_queue_manager.cc:289:19
    #56 0xad08f5d in DoWork ./out/asan/../../components/scheduler/base/task_queue_manager.cc:201:13
    #57 0x835f034 in Run ./out/asan/../../base/callback.h:397:12
    #58 0x835f034 in RunTask ./out/asan/../../base/debug/task_annotator.cc:51:0
    #59 0x82334fc in RunTask ./out/asan/../../base/message_loop/message_loop.cc:493:19
    #60 0x82340b5 in DeferOrRunPendingTask ./out/asan/../../base/message_loop/message_loop.cc:502:5
    #61 0x823501c in DoWork ./out/asan/../../base/message_loop/message_loop.cc:618:13
    #62 0x823bd50 in Run ./out/asan/../../base/message_loop/message_pump_default.cc:33:31
    #63 0x8287958 in Run ./out/asan/../../base/run_loop.cc:35:10
    #64 0x823192e in ?? ./out/asan/../../base/message_loop/message_loop.cc:295:12
    #65 0x5f1e410 in RendererMain ./out/asan/../../content/renderer/renderer_main.cc:197:37
    #66 0x6a14845 in RunZygote ./out/asan/../../content/app/content_main_runner.cc:345:14
    #67 0x6a1767d in Run ./out/asan/../../content/app/content_main_runner.cc:787:12
    #68 0x6a13aca in ContentMain ./out/asan/../../content/app/content_main.cc:20:28
    #69 0x507075 in main ./out/asan/../../content/shell/app/shell_main.cc:48:10
    #70 0x7fbf26f03f44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287:0

0x6020000321d4 is located 0 bytes to the right of 4-byte region [0x6020000321d0,0x6020000321d4)
allocated by thread T0 (content_shell) here:
    #0 0x4db8ad in __interceptor_malloc ??:?
    #1 0xb4e5b28 in xmlStrndup ./out/asan/../../third_party/libxml/src/xmlstring.c:45:23
    #2 0xb4e5b28 in xmlStrdup ./out/asan/../../third_party/libxml/src/xmlstring.c:71:0
    #3 0xb4f519c in xmlXPathObjectCopy ./out/asan/../../third_party/libxml/src/xpath.c:5415:23
    #4 0xb523d25 in xmlXPathVariableLookup ./out/asan/../../third_party/libxml/src/xpath.c:5066:8
    #5 0xb523d25 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13504:0
    #6 0xb522e1b in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13988:26
    #7 0xb52248a in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13617:26
    #8 0xb522365 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13609:26
    #9 0xb521981 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13540:25
    #10 0xb522e1b in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13988:26
    #11 0xb52248a in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13617:26
    #12 0xb522365 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13609:26
    #13 0xb521981 in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13540:25
    #14 0xb522e1b in xmlXPathCompOpEval ./out/asan/../../third_party/libxml/src/xpath.c:13988:26
    #15 0xb5134e4 in xmlXPathRunEval ./out/asan/../../third_party/libxml/src/xpath.c:14563:2
    #16 0xb5125d3 in xmlXPathCompiledEvalInternal ./out/asan/../../third_party/libxml/src/xpath.c:14930:11
    #17 0xb5122ee in ?? ./out/asan/../../third_party/libxml/src/xpath.c:14993:5
    #18 0xb59fdc0 in xsltEvalVariable ./out/asan/../../third_party/libxslt/libxslt/variables.c:903:11
    #19 0xb5a1606 in xsltBuildVariable ./out/asan/../../third_party/libxslt/libxslt/variables.c:1773:19
    #20 0xb5a1606 in xsltRegisterVariable ./out/asan/../../third_party/libxslt/libxslt/variables.c:1835:0
    #21 0xb58f3e4 in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2775:3
    #22 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #23 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #24 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2
    #25 0xb58ecaa in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2755:17
    #26 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #27 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #28 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2
    #29 0xb58ecaa in xsltApplySequenceConstructor ./out/asan/../../third_party/libxslt/libxslt/transform.c:2755:17
    #30 0xb58d56f in xsltApplyXSLTTemplate ./out/asan/../../third_party/libxslt/libxslt/transform.c:3216:5
    #31 0xb58bdb5 in xsltProcessOneNode ./out/asan/../../third_party/libxslt/libxslt/transform.c:2184:2
    #32 0xb597e84 in xsltApplyTemplates ./out/asan/../../third_party/libxslt/libxslt/transform.c:5176:2

SUMMARY: AddressSanitizer: heap-buffer-overflow (/usr/local/google/work/cb/src/out/asan/content_shell+0xb5c27e9)
Shadow bytes around the buggy address:
  0x0c047fffe3e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffe3f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffe400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffe410: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffe420: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c047fffe430: fa fa fa fa fa fa 02 fa fa fa[04]fa fa fa 02 fa
  0x0c047fffe440: fa fa 04 fa fa fa 00 00 fa fa 04 fa fa fa fd fa
  0x0c047fffe450: fa fa 00 00 fa fa fd fa fa fa fd fa fa fa 00 00
  0x0c047fffe460: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 04 fa
  0x0c047fffe470: fa fa 04 fa fa fa 00 01 fa fa 00 01 fa fa 00 01
  0x0c047fffe480: fa fa 00 02 fa fa 05 fa fa fa 00 07 fa fa 00 03
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1==ABORTING
[120651:120651:0617/153428:258111435540:WARNING:x11_util.cc(1409)] X error received: serial 215, error_code 3 (BadWindow), request_code 4, minor_code 0 (Unknown)

### do...@chromium.org (2016-06-17)

Thank you again for this splendid bug and repro case.

CCing ddkilzer based on your comment about disclosing this to WebKit-based browsers. Do let us know when this has an upstream bug so that we can link to it.

I have uploaded your patch here:

https://codereview.chromium.org/2076003002

IIRC Chromium doesn't commit POCs as LayoutTests until this is released. (Maybe someone from the security team can confirm that.) Maybe a C++ unit test which fails under ASAN would be an acceptable middle ground.

### mm...@chromium.org (2016-06-17)

Since it is external report, adding reward-topanel label.

### am...@chromium.org (2016-06-21)

Initial report on Windows, but my working assumption is that libxslt is bundled with all of our products?  As such marking OS-All but you can correct me if I'm wrong.

### dd...@apple.com (2016-06-21)

amineer@chromium.org:  Yes, it's cross-platform:

> Operating System: Windows 10, 64-bit
> Operating System: OS X 10.11.5

Nick:  Thanks for coordinating!  I'm working on integrating the fix now.  I will know more about when the fix will ship in a bit.


### do...@chromium.org (2016-06-22)

Patchset 1 (id:??) landed as https://crrev.com/f878ab7a662f23f54d8a978366d6e8d4b2455d23
Cr-Commit-Position: refs/heads/master@{#400737}

Please keep Restrict-View-SecurityTeam on this until there's a public upstream bug.

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### dd...@apple.com (2016-06-22)

> I will know more about when the fix will ship in a bit.

The fix will be shipping before the end of July.  I don't have an exact date (it's still subject to change), but I'll update when I know more.  Please feel free to contact me via this bug or offline via email if you want a status update.  Thanks!


### mm...@chromium.org (2016-06-23)

Thanks ddkilzer@ for keeping us updated!

### do...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-27)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### go...@chromium.org (2016-06-27)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### go...@chromium.org (2016-06-29)

dominicc@, could you please reply to https://crbug.com/chromium/619006#c21 so I can approve the merge to M52 based on your reply. 

### aw...@chromium.org (2016-07-06)

Congratulations, the panel decided to award $1,500 for this, which includes $500 since we used the patch you provided.

Somebody from our finance team will reach out in the next week or so.

### do...@chromium.org (2016-07-08)

Should be fine to merge.

This is not really OS-All because as I understand it we don't build libxslt on iOS. Blink is the only libxslt user in Chromium; iOS uses the Apple web view and not Blink.

### am...@chromium.org (2016-07-12)

Merge approved for M52 branch 2743.

### aw...@chromium.org (2016-07-12)

Hello!  Please merge to M52 by 5pm PDT Today (Tuesday 12th) if at all possible.  Cheers!

### aw...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Please merge your change to M52 branch 2743 before 5:00 PM PST Friday (07/15/16) as we are very close to M52 stable candidate cut. 

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2cf6d66ecc3ea794e4f1c1174bd954ca436d5098

commit 2cf6d66ecc3ea794e4f1c1174bd954ca436d5098
Author: Dominic Cooney <dominicc@chromium.org>
Date: Fri Jul 15 01:17:52 2016

Limit XSLT number format strings to their length.

BUG=619006

Review-Url: https://codereview.chromium.org/2076003002
Cr-Commit-Position: refs/heads/master@{#400737}
(cherry picked from commit f878ab7a662f23f54d8a978366d6e8d4b2455d23)

Review URL: https://codereview.chromium.org/2156433002 .

Cr-Commit-Position: refs/branch-heads/2743@{#639}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/2cf6d66ecc3ea794e4f1c1174bd954ca436d5098/third_party/libxslt/README.chromium
[modify] https://crrev.com/2cf6d66ecc3ea794e4f1c1174bd954ca436d5098/third_party/libxslt/libxslt/numbers.c


### sh...@chromium.org (2016-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### we...@aevum.de (2016-10-12)

This is now fixed upstream: https://git.gnome.org/browse/libxslt/commit/?id=eb1030de31165b68487f288308f9d1810fed6880

### do...@chromium.org (2017-01-13)

Thanks! I am backing out the local patch in <https://codereview.chromium.org/2634473003>

### dd...@apple.com (2017-06-12)

This was assigned CVE-2016-4607 by Apple.


### is...@google.com (2017-06-12)

This issue was migrated from crbug.com/chromium/619006?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084524)*
