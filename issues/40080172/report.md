# Heap-use-after-free in blink::RenderBox::pixelSnappedClientHeight

| Field | Value |
|-------|-------|
| **Issue ID** | [40080172](https://issues.chromium.org/issues/40080172) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | cl...@chromium.org |
| **Assignee** | tk...@chromium.org |
| **Created** | 2014-08-07 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5447389445881856

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x04132b60
Crash State:
  - crash stack -
  blink::RenderBox::pixelSnappedClientHeight
  blink::RenderBox::canBeScrolledAndHasScrollableArea
  - free stack -
  blink::RenderTextControlSingleLine::`scalar
  blink::RenderObject::postDestroy
  

Minimized Testcase (2.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95c_B7ePMZz3qVAJCMD6vRJKRZc0arjO3_u9u9Pn-ZECqeJsO9j9cJmQc4KN81wog3W8Mco-a_-DryUC1z56t8s8iIxlbZZvhdUjEQDn30rV-FJZsZto7bctnlbmdqVuZbhEz9Yo2N3r0aXjVhyLEwwd15Qiw

Additional requirements: Requires Gestures

Filer: inferno

## Timeline

### in...@chromium.org (2014-08-07)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-08-08)

jchaffraix, can you please take a look?

### in...@chromium.org (2014-08-08)

Looks input element specific and events stuff. Assigning to tkent@

### cl...@chromium.org (2014-08-09)

[Empty comment from Monorail migration]

### tk...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### tk...@chromium.org (2014-08-11)

This looks Windows-specific.  Was this on SyzyASan?


Node::defaultEventHandler:

#if OS(WIN)
    } else if (eventType == EventTypeNames::mousedown && event->isMouseEvent()) {
        MouseEvent* mouseEvent = toMouseEvent(event);
        if (mouseEvent->button() == MiddleButton) {
            if (enclosingLinkEventParentOrSelf())
                return;

            RenderObject* renderer = this->renderer();
            while (renderer && (!renderer->isBox() || !toRenderBox(renderer)->canBeScrolledAndHasScrollableArea()))  // *** Happening here
                renderer = renderer->parent();

            if (renderer) {
                if (LocalFrame* frame = document().frame())
                    frame->eventHandler().startPanScrolling(renderer);
            }
        }
#endif



### in...@chromium.org (2014-08-11)

Yes this was on windows with clang asan (not syzyasan), see build instructions on http://www.chromium.org/developers/testing/addresssanitizer

### tk...@chromium.org (2014-08-12)

> Note: This is not yet available for developers. 

It's unfortunate that I need to use such tool to reproduce the issue.


### in...@chromium.org (2014-08-12)

Just follow past that note, the build instructions always work. That note was added by thakis@ since developer can't do debugging with that build. Otherwise, for checking whether a fix worked or not, it does work.

# You should have CMake installed and added to your PATH
    set GYP_DEFINES=clang=1 asan=1 component=static_library disable_nacl=1
    gclient runhooks
    ninja -C out\Release chrome

### tk...@chromium.org (2014-08-12)

#9, I tried it today, and didn't work.

> set GYP_DEFINES=...
> gclient runhooks
...
________ running 'D:\src\depot_tools\python276_bin\python.exe src/tools/clang/scripts/update.py
--if-needed' in 'D:\src\chrome'
Checked out revision 215204.
Checked out revision 215204.
Checked out revision 215204.
Updating Clang to 215204...
Clobbering Chromium build files...
Checking out LLVM r215204 into 'D:\src\chrome\src\third_party\llvm'
Running ['svn', 'checkout', '--force', 'https://llvm.org/svn/llvm-project/llvm/trunk@215204', 'D
:\\src\\chrome\\src\\third_party\\llvm'] (try #1)
Checking out Clang r215204 into 'D:\src\chrome\src\third_party\llvm\tools\clang'
Running ['svn', 'checkout', '--force', 'https://llvm.org/svn/llvm-project/cfe/trunk@215204', 'D:
\\src\\chrome\\src\\third_party\\llvm\\tools\\clang'] (try #1)
Checking out compiler-rt r215204 into 'D:\src\chrome\src\third_party\llvm\projects\compiler-rt'
Running ['svn', 'checkout', '--force', 'https://llvm.org/svn/llvm-project/compiler-rt/trunk@2152
04', 'D:\\src\\chrome\\src\\third_party\\llvm\\projects\\compiler-rt'] (try #1)
Traceback (most recent call last):
  File "src/tools/clang/scripts/update.py", line 235, in <module>
  File "src/tools/clang/scripts/update.py", line 231, in main
  File "src/tools/clang/scripts/update.py", line 155, in UpdateClang
  File "D:\src\chrome\src\tools\gyp\pylib\gyp\MSVSVersion.py", line 106, in SetupScript
    os.path.join(self.path, 'VC/vcvarsall.bat')), arg]
  File "D:\src\depot_tools\python276_bin\lib\ntpath.py", line 96, in join
    assert len(path) > 0
TypeError: object of type 'NoneType' has no len()
Error: Command D:\src\depot_tools\python276_bin\python.exe src/tools/clang/scripts/update.py --i
f-needed returned non-zero exit status 1 in D:\src\chrome
Hook ''D:\src\depot_tools\python276_bin\python.exe' src/tools/clang/scripts/update.py --if-neede
d' took 84.94 secs


### in...@chromium.org (2014-08-12)

Do you have windows 8 sdk installed (that should fix this) ? I remember seeing this when i was first trying this couple of months back. I switched from VS 2010 to vs 2013 and installed the latest sdk and running all this in a visual studio command prompt.

### tk...@chromium.org (2014-08-14)

I finally built chrome.exe with clang + asan, however it didn't load any pages :-(
I'll try to reproduce this bug by adding some diagnostic code.


Off topic: How to build with clang+asan ---------------
- |gclient runhooks| failed on my machine (#10)
- My machine had VS2010 [a] installed by a normal way, and VS2013 toolchain [b] downloaded by depot_tools.
- vcvars*.bat of [b] didn't work due to lack of registry entries
- I installed VS2013 [c] by a normal way, and uninstalled [a].
- I ran vcvars*.bat of [c], then |gclient runhooks] on the same console.  ==> Succeeded


### [Deleted User] (2014-08-14)

> however it didn't load any pages
That doesn't look right :(
Do you pass --no-sandbox? Can you try passing --disable-gpu?

### tk...@chromium.org (2014-08-15)

> Do you pass --no-sandbox? Can you try passing --disable-gpu?

Bingo!  --no-sandbox resolved the issue.

I had the following log without --no-sandbox:

> [6268:6748:0814/160524:ERROR:gpu_process_transport_factory.cc(418)] Failed to establish GPU channel.
> [6268:6748:0814/160524:ERROR:web_resource_service.cc(54)] Utility process crashed while trying to retrieve web resources.


### tk...@chromium.org (2014-08-15)

ok, I reproduced the UAF, and made a reproduction without user interaction.

--------------------------------------
<script>
onload = function() {
  el0 = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  document.body.appendChild(el0);
  el28 = document.createElement('input');
  el0.parentNode.insertBefore(el28, el0);
  el28.setAttribute('class', 'c0');
  setTimeout(next1, 0);
}

function next1() {
  var c0 = document.querySelector('.c0');
  c0.setAttribute('style', 'content: counter(c, ethiopic-halehame-ti-er) attr(id);');
  var ev = new MouseEvent('mousedown', {button:1});
  c0.dispatchEvent(ev);
  console.log('Crashed?');
}
</script>
--------------------------------------


### tk...@chromium.org (2014-08-15)

Minimized:
--------------------------------------
<script>
onload = function() {
  var c0 = document.querySelector('input');
  c0.style.display = 'none';
  c0.dispatchEvent(new MouseEvent('mousedown', {button:1}));
  console.log('Crashed?');
};
</script>
<input>
--------------------------------------


### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180539

------------------------------------------------------------------
r180539 | tkent@chromium.org | 2014-08-19T09:33:39.236003Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Node.cpp?r1=180539&r2=180538&pathrev=180539
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/events/panScroll-crash.html?r1=180539&r2=180538&pathrev=180539
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/events/panScroll-crash-expected.txt?r1=180539&r2=180538&pathrev=180539

Windows: Fix crash by starting pan-scrolling when render tree needs to be updated.

It's possible that RenderBox::canBeScrolledAndHasScrollableArea()
modifies render tree and the |while| loop in Node::defaultEventHandler
is confused. We should make sure render tree is up-to-date before the
loop.

BUG=401362

Review URL: https://codereview.chromium.org/471373002
-----------------------------------------------------------------

### in...@chromium.org (2014-08-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-21)

ClusterFuzz has detected this issue as fixed in range 290178:290740.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5447389445881856

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x04132b60
Crash State:
  blink::RenderBox::pixelSnappedClientHeight
  blink::RenderBox::canBeScrolledAndHasScrollableArea
  - free stack -
  blink::RenderTextControlSingleLine::`scalar
  blink::RenderObject::postDestroy
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=290178:290740

Minimized Testcase (2.48 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95c_B7ePMZz3qVAJCMD6vRJKRZc0arjO3_u9u9Pn-ZECqeJsO9j9cJmQc4KN81wog3W8Mco-a_-DryUC1z56t8s8iIxlbZZvhdUjEQDn30rV-FJZsZto7bctnlbmdqVuZbhEz9Yo2N3r0aXjVhyLEwwd15Qiw

Additional requirements: Requires Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### tk...@chromium.org (2014-08-21)

[Empty comment from Monorail migration]

### tk...@chromium.org (2014-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2014-08-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-25)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=180836

------------------------------------------------------------------
r180836 | tkent@chromium.org | 2014-08-24T23:57:48.347187Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/fast/events/panScroll-crash-expected.txt?r1=180836&r2=180835&pathrev=180836
   M http://src.chromium.org/viewvc/blink/branches/chromium/2125/Source/core/dom/Node.cpp?r1=180836&r2=180835&pathrev=180836
   A http://src.chromium.org/viewvc/blink/branches/chromium/2125/LayoutTests/fast/events/panScroll-crash.html?r1=180836&r2=180835&pathrev=180836

Merge 180539 "Windows: Fix crash by starting pan-scrolling when ..."

> Windows: Fix crash by starting pan-scrolling when render tree needs to be updated.
> 
> It's possible that RenderBox::canBeScrolledAndHasScrollableArea()
> modifies render tree and the |while| loop in Node::defaultEventHandler
> is confused. We should make sure render tree is up-to-date before the
> loop.
> 
> BUG=401362
> 
> Review URL: https://codereview.chromium.org/471373002

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/502823002
-----------------------------------------------------------------

### tk...@chromium.org (2014-08-25)

Merged to M-38 branch.  Merge-Request for M37.


### aa...@google.com (2014-09-03)

merged to m37 in r181342

### bu...@chromium.org (2014-09-03)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=181342

------------------------------------------------------------------
r181342 | amineer@chromium.org | 2014-09-03T21:51:04.291760Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2062/LayoutTests/fast/events/panScroll-crash.html?r1=181342&r2=181341&pathrev=181342
   A http://src.chromium.org/viewvc/blink/branches/chromium/2062/LayoutTests/fast/events/panScroll-crash-expected.txt?r1=181342&r2=181341&pathrev=181342
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/core/dom/Node.cpp?r1=181342&r2=181341&pathrev=181342

Merge 180539 "Windows: Fix crash by starting pan-scrolling when ..."

Merging into M37 branch 2062
BUG=401362

> Windows: Fix crash by starting pan-scrolling when render tree needs to be updated.
> 
> It's possible that RenderBox::canBeScrolledAndHasScrollableArea()
> modifies render tree and the |while| loop in Node::defaultEventHandler
> is confused. We should make sure render tree is up-to-date before the
> loop.
> 
> BUG=401362
> 
> Review URL: https://codereview.chromium.org/471373002

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/540573002
-----------------------------------------------------------------

### mb...@chromium.org (2014-09-04)

Thanks again for the fuzzer contribution! This qualifies for a $2000 reward.

### mb...@chromium.org (2014-09-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-11-25)

Bulk update: removing view restriction from closed bugs.

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

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

This issue was migrated from crbug.com/chromium/401362?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080172)*
