# Security: Heap-use-after-free in PrintPreviewHandler::HandleGetPreview

| Field | Value |
|-------|-------|
| **Issue ID** | [40086858](https://issues.chromium.org/issues/40086858) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>PrintPreview |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-02-21 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 58.0.3018.0 (Build officiel) canary (64 bits)  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Visit <http://localhost/testcase.html>
2. Observe an alert is being displayed at the same time try to visit <https://example.com>
3. Crash!

Crash/1e71b6b580000000

rax=00000000101e7df0 rbx=0000000011202b90 rcx=000000000c264fc0  

rdx=01fd00010001ffff rsi=0000000000000000 rdi=00000000101e7df0  

rip=000007fee0bc6e84 rsp=000000000027bfb0 rbp=000000000027c0b0  

r8=00000000101e7de0 r9=00000000101e7df0 r10=000007fee1a99210  

r11=000000000027bf50 r12=000000000c264fc0 r13=0000000000000000  

r14=000000000fb9a3a0 r15=000000000027c330  

iopl=0 nv up ei pl nz na po nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010206  

\*\*\* WARNING: Unable to verify checksum for chrome.dll  

chrome\_7fedf160000!PrintPreviewHandler::HandleGetPreview+0x534:  

000007fe`e0bc6e84 ff5230 call qword ptr [rdx+30h] ds:01fd0001`0002002f=????????????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

Child-SP RetAddr Call Site  

00000000`0027bfb0 000007fe`df7a9cf2 chrome\_7fedf160000!PrintPreviewHandler::HandleGetPreview+0x534 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\ui\webui\print\_preview\print\_preview\_handler.cc @ 821]  

00000000`0027c200 000007fe`df7a9493 chrome\_7fedf160000!content::WebUIImpl::ProcessWebUIMessage+0xa2 [c:\b\build\slave\win64-pgo\build\src\content\browser\webui\web\_ui\_impl.cc @ 252]  

00000000`0027c240 000007fe`df7aa1d0 chrome\_7fedf160000!content::WebUIImpl::OnWebUISend+0x93 [c:\b\build\slave\win64-pgo\build\src\content\browser\webui\web\_ui\_impl.cc @ 112]  

00000000`0027c280 000007fe`df7a939f chrome\_7fedf160000!IPC::MessageT<ViewHostMsg\_WebUISend\_Meta,std::tuple<GURL,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >,base::ListValue>,void>::Dispatch<content::WebUIImpl,content::WebUIImpl,void,void (\_\_cdecl content::WebUIImpl::\*)(GURL const & \_\_ptr64,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const & \_\_ptr64,base::ListValue const & \_\_ptr64) \_\_ptr64>+0x154 [c:\b\build\slave\win64-pgo\build\src\ipc\ipc\_message\_templates.h @ 121]  

00000000`0027c430 000007fe`df787752 chrome\_7fedf160000!content::WebUIImpl::OnMessageReceived+0xdf [c:\b\build\slave\win64-pgo\build\src\content\browser\webui\web\_ui\_impl.cc @ 94]  

00000000`0027c540 000007fe`df6cbe47 chrome\_7fedf160000!content::WebContentsImpl::OnMessageReceived+0x62 [c:\b\build\slave\win64-pgo\build\src\content\browser\web\_contents\web\_contents\_impl.cc @ 695]  

00000000`0027ce20 000007fe`df6cfd62 chrome\_7fedf160000!content::RenderViewHostImpl::OnMessageReceived+0x117 [c:\b\build\slave\win64-pgo\build\src\content\browser\renderer\_host\render\_view\_host\_impl.cc @ 732]  

00000000`0027d6b0 000007fe`df6bef47 chrome\_7fedf160000!content::RenderWidgetHostImpl::OnMessageReceived+0x152 [c:\b\build\slave\win64-pgo\build\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc @ 517]  

00000000`0027e670 000007fe`dfebb728 chrome\_7fedf160000!content::RenderProcessHostImpl::OnMessageReceived+0x5f7 [c:\b\build\slave\win64-pgo\build\src\content\browser\renderer\_host\render\_process\_host\_impl.cc @ 2076]  

00000000`0027eaf0 000007fe`df531b14 chrome\_7fedf160000!IPC::ChannelProxy::Context::OnDispatchMessage+0x28 [c:\b\build\slave\win64-pgo\build\src\ipc\ipc\_channel\_proxy.cc @ 330]  

00000000`0027eb20 000007fe`dfb48d83 chrome\_7fedf160000!base::internal::RunMixin<base::Callback<void \_\_cdecl(void),0,0> >::Run+0x24 [c:\b\build\slave\win64-pgo\build\src\base\callback.h @ 68]  

00000000`0027eb50 000007fe`dfaf7887 chrome\_7fedf160000!base::debug::TaskAnnotator::RunTask+0x183 [c:\b\build\slave\win64-pgo\build\src\base\debug\task\_annotator.cc @ 61]  

00000000`0027ece0 000007fe`dfaf843a chrome\_7fedf160000!base::MessageLoop::RunTask+0x217 [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_loop.cc @ 424]  

00000000`0027ee50 000007fe`dfb492f1 chrome\_7fedf160000!base::MessageLoop::DoWork+0x48a [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_loop.cc @ 527]  

00000000`0027f050 000007fe`dfb48f44 chrome\_7fedf160000!base::MessagePumpForUI::DoRunLoop+0x71 [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_pump\_win.cc @ 174]  

00000000`0027f0c0 000007fe`dfb1f630 chrome\_7fedf160000!base::MessagePumpWin::Run+0x54 [c:\b\build\slave\win64-pgo\build\src\base\message\_loop\message\_pump\_win.cc @ 58]  

00000000`0027f110 000007fe`dfa261f8 chrome\_7fedf160000!base::RunLoop::Run+0xc0 [c:\b\build\slave\win64-pgo\build\src\base\run\_loop.cc @ 38]  

00000000`0027f1c0 000007fe`df4be7ec chrome\_7fedf160000!ChromeBrowserMainParts::MainMessageLoopRun+0x138 [c:\b\build\slave\win64-pgo\build\src\chrome\browser\chrome\_browser\_main.cc @ 2005]  

00000000`0027f240 000007fe`df4b6679 chrome\_7fedf160000!content::BrowserMainRunnerImpl::Run+0x6c [c:\b\build\slave\win64-pgo\build\src\content\browser\browser\_main\_runner.cc @ 140]  

00000000`0027f290 000007fe`df9d7b13 chrome\_7fedf160000!content::BrowserMain+0x169 [c:\b\build\slave\win64-pgo\build\src\content\browser\browser\_main.cc @ 46]

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 87 B)
- [Rec.mp4](attachments/Rec.mp4) (video/mp4, 617.5 KB)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 471.6 KB)
- [Recording.mp4](attachments/Recording_53356481.mp4) (video/mp4, 467.2 KB)
- [PoC.rar](attachments/PoC.rar) (application/octet-stream, 972 B)
- [694382_Mar_28.mp4](attachments/694382_Mar_28.mp4) (video/mp4, 1.4 MB)
- [Recording #6.mp4](attachments/Recording #6.mp4) (video/mp4, 689.1 KB)
- [UAF.html](attachments/UAF.html) (text/plain, 348 B)
- [testcase.html](attachments/testcase_53356594.html) (text/plain, 112 B)
- [Recording #7.mp4](attachments/Recording #7.mp4) (video/mp4, 555.4 KB)

## Timeline

### ch...@gmail.com (2017-02-21)

Able to repro this on Dev (58.0.3013.3).

### ke...@chromium.org (2017-02-22)

Thanks for the report. I could not reproduce this on canary. Can you give it a quick try on canary and confirm if you are using an ASAN build or not, plus the canary version you reproduced this with? Thank you.

### ch...@gmail.com (2017-02-22)

[Comment Deleted]

### ch...@gmail.com (2017-02-25)

[Comment Deleted]

### ch...@gmail.com (2017-02-26)

On my machine I have the latest version of canary (58.0.3023.0).

- Able to reproduce this crash on Canary/Dev.
- Unable to reproduce this crash on Stable/Beta/ASan build.

Sometimes this crash can take several tries to repro. 

What happens is that PrintPreviewHandler::HandleGetPreview was called after the render_view_host_ has been destroyed by navigation to another origin.

### va...@chromium.org (2017-03-01)

I was able to repro this. See: crash/0671d73300000000

skau@ -- if you are not the right owner, please help identify the right owner. Thanks.

[Monorail components: UI>Browser>PrintPreview]

### cl...@chromium.org (2017-03-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4960837371691008

### sh...@chromium.org (2017-03-01)

Thank you for providing more feedback. Adding requester "kerrnel@chromium.org" to the cc list and removing "Needs-Feedback" label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2017-03-01)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-03-01)

FWIW: I can't repro this on Chrom Dev on Linux.

### sk...@chromium.org (2017-03-01)

Yes.  I'm the right owner. I'm looking into it.

### sk...@chromium.org (2017-03-01)

I edited that file recently but I didn't touch that section.  Looks like it was last edited by thestig@ in this commit https://chromium.googlesource.com/chromium/src/+/cb959ce66a9a8%5E%21/#F11

Message handling must not be sequenced with whatever cleans up the RenderFrame.  Reassigning as I'm not sure how to mitigate this.

### cl...@chromium.org (2017-03-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5615695061843968

### va...@chromium.org (2017-03-02)

Setting the severity as Low since it requires too many user gestures.

### sh...@chromium.org (2017-03-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-03-08)

https://crbug.com/chromium/698622 may be the same issue, but without user gestures. It's weird that skau@ assigned it to me but left it in with Started status. I guess I should start looking at this...

### dc...@chromium.org (2017-03-08)

I guess print preview needs to listen for RFH deletion and null out print_preview_rfh() if needed.

### bu...@chromium.org (2017-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/746da1cc6b2fbc2f725934542eedc49b41e5f17b

commit 746da1cc6b2fbc2f725934542eedc49b41e5f17b
Author: thestig <thestig@chromium.org>
Date: Thu Mar 16 06:18:21 2017

Properly clean up in PrintViewManager::RenderFrameCreated().

BUG=694382,698622

Review-Url: https://codereview.chromium.org/2742853003
Cr-Commit-Position: refs/heads/master@{#457363}

[modify] https://crrev.com/746da1cc6b2fbc2f725934542eedc49b41e5f17b/chrome/browser/printing/print_view_manager.cc
[add] https://crrev.com/746da1cc6b2fbc2f725934542eedc49b41e5f17b/chrome/browser/printing/print_view_manager_unittest.cc
[modify] https://crrev.com/746da1cc6b2fbc2f725934542eedc49b41e5f17b/chrome/test/BUILD.gn


### na...@chromium.org (2017-03-16)

https://codereview.chromium.org/2742853003 should be backported to M58 and M57, as it fixes a nasty bug with printing and extensions described in https://crbug.com/chromium/702085.

### th...@chromium.org (2017-03-16)

Yes, I'll do M58 today and M57 early next week assuming there's no issues.

### sh...@chromium.org (2017-03-17)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-17)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-18)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-03-20)

I've found a way to reduce too many user gestures for this crash. I tested on stable 57.0.2987.110 (64-bit).

1- Open http://localhost/UAF.html.
2- click "click here" then "then here" buttons.
3- click "OK" in the alert box.
4- Wait 4 seconds >> Crash.

Note: there are two different crashes "render/browser" (I'm talking about the browser crash).

In this case is this report qualified for "Severity-Medium" at leaset?

### sh...@chromium.org (2017-03-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2017-03-20)

Medium per c24.

### th...@chromium.org (2017-03-20)

M58 merge from last week: https://chromium.googlesource.com/chromium/src/+/23107311dcb2bc1ecfa1c0fbe63f5f210c154049

### ke...@chromium.org (2017-03-20)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8839f8f3d22dc169ede6edad06d75735dbf3c34a

commit 8839f8f3d22dc169ede6edad06d75735dbf3c34a
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Mar 27 03:40:04 2017

M57: Properly clean up in PrintViewManager::RenderFrameCreated().

BUG=694382,698622

Review-Url: https://codereview.chromium.org/2742853003
Cr-Commit-Position: refs/heads/master@{#457363}
(cherry picked from commit 746da1cc6b2fbc2f725934542eedc49b41e5f17b)

Review-Url: https://codereview.chromium.org/2775133002 .
Cr-Commit-Position: refs/branch-heads/2987@{#881}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[modify] https://crrev.com/8839f8f3d22dc169ede6edad06d75735dbf3c34a/chrome/browser/printing/print_view_manager.cc
[add] https://crrev.com/8839f8f3d22dc169ede6edad06d75735dbf3c34a/chrome/browser/printing/print_view_manager_unittest.cc
[modify] https://crrev.com/8839f8f3d22dc169ede6edad06d75735dbf3c34a/chrome/test/BUILD.gn


### aw...@google.com (2017-03-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-03-27)

[Empty comment from Monorail migration]

### du...@chromium.org (2017-03-28)

Was unable to reproduce the crash on Win 7 and Win 10 using reported version 58.0.3018.0 and 57.0.2987.98/110 using steps from comment # 24.After allowing the plugin no alert is seen or it says the plugin is not supported.

And using steps from Original report(https://crbug.com/chromium/694382#c1), was unable to click on Back/Forward buttons of the browser and not able to enter text on Omnibox until the Ok button is clicked.

Requesting MTV team to take a look into this.

### sh...@chromium.org (2017-03-28)

This bug is a regression and does not impact stable. Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-03-28)

Thanks sheriffbot!

### ch...@gmail.com (2017-03-28)

I just repro this on stable 57.0.2987.110. This crash needs several attempts.

### ch...@gmail.com (2017-03-28)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-03-28)

It does take several attempts to crash. I sometimes see renderer crashes too. I'll look some more.

### th...@chromium.org (2017-03-28)

I'm testing with 57.0.2987.130 here. I got one browser crash earlier as mentioned, but the crash server never processed that crash so I don't know what happened. I kept trying, and the browser process hasn't crashed since. The renderer crash has been filed as https://crbug.com/chromium/706103. I keep hitting it all the time using PoC.rar.

### ch...@gmail.com (2017-03-28)

Attaching mnimized testcase. (Only browser crash)

### th...@chromium.org (2017-03-28)

I tried the test case in https://crbug.com/chromium/694382#c40 but I haven't been able to reproduce a browser crash with it. If it's racy, I could just be having bad (good rather?) luck.

If you have crash report IDs, that may be helpful.

### th...@chromium.org (2017-03-28)

Oh, and if this is on 57.x, we will hopefully have a new build out this week with the merge in https://crbug.com/chromium/694382#c30. Maybe try that once released?

### ch...@gmail.com (2017-03-28)

C#41 - Unable to get a server crash ID, anyway I got the same stack traces from WinDbg.

C#42 - Okey, but release- labels were removed!

### th...@chromium.org (2017-03-28)

Are you testing 57.0.2987.110? Is the problem present on Canary?

I'm not sure about the release- labels. If the concern is about which 57.x builds have the potential fix in https://crbug.com/chromium/694382#c30, the answer is 57.0.2987.130 and newer.

### ch...@gmail.com (2017-03-28)

The crash has been fixed in Canary, the reason why I attached the mnimized testcase in https://crbug.com/chromium/694382#c40 is to proof that's repro on Stable (57.0.2987.110), against in https://crbug.com/chromium/694382#c34.

### mb...@chromium.org (2017-03-29)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-03-29)

Verified on stable 57.0.2987.133. Thanks for the fix :)

### th...@chromium.org (2017-03-29)

Glad to hear it. Thank you for looking into this and coming up with more test cases.

### ch...@gmail.com (2017-03-29)

[Comment Deleted]

### ch...@gmail.com (2017-03-31)

[Comment Deleted]

### ch...@gmail.com (2017-03-31)

Note - Actually this was very easy to repro the crash with this below mnimized test case instead of the all test cases (in comments 1/24/40).

<script>
document.location = "https://www.google.com"
 window.onunload = function(){
  print();
 }
</script>

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Good news! The panel decided to award $2,000 for this bug.  There was another report of this bug from an external researcher that came in after yours, but with a much better PoC that required no user interaction and is what triggered us to make the fix. For future reference the reward would have been much higher had this report had a better PoC.  Thanks!

### ch...@gmail.com (2017-03-31)

Andrew, what do you think about https://crbug.com/chromium/694382#c51?

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/694382?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086858)*
