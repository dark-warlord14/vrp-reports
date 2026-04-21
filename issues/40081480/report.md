# OOB write in v8 due to elements kind confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [40081480](https://issues.chromium.org/issues/40081480) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | [Deleted User] |
| **Assignee** | is...@chromium.org |
| **Created** | 2015-02-23 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 42.0.2311.0 (Developer Build) (64-bit)  

**URLs (if applicable) :**  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

Safari 7.1.3: OK  

Firefox 35.0.1: OK  

IE 7/8/9/10: N/A

**What steps will reproduce the problem?**

1. Turn on a specific graphics feature (section plane view) in our WebGL-based software ([www.onshape.com](http://www.onshape.com))
2. Manipulate the view, rotate the camera, etc.
3. Shortly after, sometimes an Aw Snap tab crash will happen.

**What is the expected result?**

Tab doesn't crash

**What happens instead?**

Tab crashes (Aw Snap)

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

I apologize that this report does not include solid repro steps. This is a rare crash that feels like a race condition and occurs perhaps 1 of 5-10 times a specific visualization mode is used. Unfortunately the software itself ([www.onshape.com](http://www.onshape.com)) is also closed for a little while longer, but if anyone would like to work on this bug I can provide an invitation.

This bug appears on Mac and Windows in the latest Chrome and Chromium.

I have managed to trap the crash in Xcode in a debug Chromium build. It appears that somehow the internal v8 javascript function handle for the requestAnimationFrame callback becomes NULL. I have seen it crash the same way twice in the debugger. The crash is definitely triggered by a specific WebGL graphics feature (section view) that shows a cutaway of the model, though the causal link there is mysterious.

I have attached a screenshot of the debugger stopped at the offending line.

The about version information is:

Chromium 42.0.2311.0 (Developer Build) (64-bit)  

Revision ca068183ed1ef472599cbd1acb69d954d7a3b635-refs/heads/master@{#317350}  

OS Mac OS X  

Blink 537.36 (@190452)  

JavaScript V8 4.2.77  

Flash (Disabled)  

User Agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_9\_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.0 Safari/537.36  

Command Line /Users/fcole/chromium/src/out/Debug/Chromium.app/Contents/MacOS/Chromium --disable-background-networking --disable-client-side-phishing-detection --disable-component-update --disable-default-apps --disable-hang-monitor --disable-prompt-on-repost --disable-sync --disable-web-resources --enable-logging --ignore-certificate-errors --ignore-gpu-blacklist --enable-logging --v=1 --load-extension=/var/folders/pf/llj71sj90r30369h0pnfgrn40000gn/T/.org.chromium.Chromium.sc8Vm8/internal --log-level=0 --metrics-recording-only --no-first-run --password-store=basic --remote-debugging-port=12997 --safebrowsing-disable-auto-update --safebrowsing-disable-download-protection --test-type=webdriver --use-mock-keychain --user-data-dir=/var/folders/pf/llj71sj90r30369h0pnfgrn40000gn/T/.org.chromium.Chromium.fLrNZY --enable-avfoundation --flag-switches-begin --flag-switches-end data:,  

Executable Path /Users/fcole/chromium/src/out/Debug/Chromium.app/Contents/MacOS/Chromium  

Profile Path /private/var/folders/pf/llj71sj90r30369h0pnfgrn40000gn/T/.org.chromium.Chromium.fLrNZY/Default  

Variations InfiniteCache:No  

Prerender:PrerenderEnabled

## Attachments

- [chrome_crash_screen.png](attachments/chrome_crash_screen.png) (image/png, 624.0 KB)

## Timeline

### me...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### ds...@chromium.org (2015-02-23)

@fcole, could you provide a crash id from chrome://crashes?

### ds...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### [Deleted User] (2015-02-23)

Sorry, I somehow thought that crash ids were only for crashes for the whole program. I just reran my test and got:

Crash ID 7ec4e9dfbe7cb48e (Chrome)

Occurred Monday, February 23, 2015 at 5:58:30 PM

### aj...@chromium.org (2015-02-25)

This is crash in invoke as per the stack trace of crash id 7ec4e9dfbe7cb48e.The crash id is from the chrome version:40.0.2214.115.

fcole@: Could you please confirm the chrome version where you are facing this issue.

Stack trace of 7ec4e9dfbe7cb48e :
===========================================
Thread 0 CRASHED [EXC_BAD_ACCESS / 0x0000000d @ 0x00000000] MAGIC SIGNATURE THREAD
0x00003a781d5a9398		
0x00003a781f2d748d		
0x00003a781d539865		
0x00003a781e882303		
0x00003a781f13219a		
0x00003a781f15b281		
0x00003a781f15afeb		
0x00003a781f15afeb		
0x00003a781e6b5284		
0x00003a781f226fb0		
0x00003a781d506a74		
0x00003a781f2bb61a		
0x00003a781d53681f		
0x00003a781d531030		
0x000000010e00dbfd	[Google Chrome Framework -execution.cc:103 ]	v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)
0x000000010df02730	[Google Chrome Framework -api.cc:4216 ]	v8::Function::Call(v8::Handle<v8::Value>, int, v8::Handle<v8::Value>*)
0x000000010eb94b2d	[Google Chrome Framework -V8ScriptRunner.cpp:231 ]	blink::V8ScriptRunner::callFunction(v8::Handle<v8::Function>, blink::ExecutionContext*, v8::Handle<v8::Value>, int, v8::Handle<v8::Value>*, v8::Isolate*)
0x000000010eb6208b	[Google Chrome Framework -ScriptController.cpp:171 ]	blink::ScriptController::callFunction(blink::ExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Value>, int, v8::Handle<v8::Value>*, v8::Isolate*)
0x000000010eced8ba	[Google Chrome Framework -V8RequestAnimationFrameCallback.cpp:47 ]	blink::V8RequestAnimationFrameCallback::handleEvent(double)
0x000000010e3db11e	[Google Chrome Framework -ScriptedAnimationController.cpp:188 ]	blink::ScriptedAnimationController::executeCallbacks(double)
0x000000010e3db309	[Google Chrome Framework -ScriptedAnimationController.cpp:220 ]	blink::ScriptedAnimationController::serviceScriptedAnimations(double)
0x000000010e89def8	[Google Chrome Framework -PageAnimator.cpp:66 ]	blink::PageAnimator::serviceScriptedAnimations(double)
0x000000010e2f7e28	[Google Chrome Framework -PageWidgetDelegate.cpp:56 ]	blink::PageWidgetDelegate::animate(blink::Page&, double, blink::LocalFrame&)
0x000000010e34bbc4	[Google Chrome Framework -WebViewImpl.cpp:1878 ]	blink::WebViewImpl::beginFrame(blink::WebBeginFrameArgs const&)
0x00000001102d7f61	[Google Chrome Framework -render_widget_compositor.cc:790 ]	non-virtual thunk to content::RenderWidgetCompositor::BeginMainFrame(cc::BeginFrameArgs const&)
0x000000010d808d09	[Google Chrome Framework -layer_tree_host.cc:252 ]	cc::LayerTreeHost::BeginMainFrame(cc::BeginFrameArgs const&)
0x000000010d834b3c	[Google Chrome Framework -thread_proxy.cc:763 ]	cc::ThreadProxy::BeginMainFrame(scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)
0x000000010d838d27	[Google Chrome Framework -bind_internal.h:190 ]	base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (cc::ThreadProxy::*)(scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)>, void (base::WeakPtr<cc::ThreadProxy> const&, scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)>::MakeItSo(base::internal::RunnableAdapter<void (cc::ThreadProxy::*)(scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)>, base::WeakPtr<cc::ThreadProxy> const&, scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)
0x000000010d838c84	[Google Chrome Framework -bind_internal.h:1248 ]	base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (cc::ThreadProxy::*)(scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)>, void (cc::ThreadProxy*, scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >), void (base::WeakPtr<cc::ThreadProxy>, base::internal::PassedWrapper<scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> > >)>, void ()(cc::ThreadProxy*, scoped_ptr<cc::ThreadProxy::BeginMainFrameAndCommitState, base::DefaultDeleter<cc::ThreadProxy::BeginMainFrameAndCommitState> >)>::Run(base::internal::BindStateBase*)
0x000000010cce1f43	[Google Chrome Framework -callback.h:401 ]	base::debug::TaskAnnotator::RunTask(char const*, char const*, base::PendingTask const&)
0x000000010cd1381e	[Google Chrome Framework -message_loop.cc:446 ]	base::MessageLoop::RunTask(base::PendingTask const&)
0x000000010cd13c3e	[Google Chrome Framework -message_loop.cc:456 ]	base::MessageLoop::DoWork()
0x000000010cccbfc0	[Google Chrome Framework -message_pump_mac.mm:325 ]	base::MessagePumpCFRunLoopBase::RunWork()
0x00007fff91e585b0	[CoreFoundation + 0x0007f5b0 ]	__CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__
0x00007fff91e49c61	[CoreFoundation + 0x00070c61 ]	__CFRunLoopDoSources0
0x00007fff91e493ee	[CoreFoundation + 0x000703ee ]	__CFRunLoopRun
0x00007fff91e48e74	[CoreFoundation + 0x0006fe74 ]	CFRunLoopRunSpecific
0x00007fff89f5916b	[Foundation + 0x0006916b ]	-[NSRunLoop(NSRunLoop) runMode:beforeDate:]
0x000000010cccc423	[Google Chrome Framework -message_pump_mac.mm:592 ]	base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)
0x000000010cccbe2b	[Google Chrome Framework -message_pump_mac.mm:235 ]	base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)
0x000000010cd28ab2	[Google Chrome Framework -run_loop.cc:55 ]	base::RunLoop::Run()
0x000000010cd1313c	[Google Chrome Framework -message_loop.cc:308 ]	base::MessageLoop::Run()
0x000000011035c97f	[Google Chrome Framework -renderer_main.cc:234 ]	content::RendererMain(content::MainFunctionParams const&)
0x000000010ccae553	[Google Chrome Framework -content_main_runner.cc:789 ]	content::ContentMainRunnerImpl::Run()
0x000000010ccadba5	[Google Chrome Framework -content_main.cc:19 ]	content::ContentMain(content::ContentMainParams const&)
0x000000010c6483f1	[Google Chrome Framework -chrome_main.cc:57 ]	ChromeMain
0x000000010c63ff38	[Google Chrome Helper -chrome_exe_main_mac.cc:16 ]	main
0x000000010c63ff23	[Google Chrome Helper + 0x00000f23 ]	start


### [Deleted User] (2015-02-25)

I can provoke the crash both in Chrome and Chromium. I was debugging it in Chromium, but I submitted the crash report from my system Chrome because apparently crash reporting is disabled in Chromium (that's the message on chrome://crashes at least). 

We've also seen this issue intermittently for a while (months) on windows and mac, and different versions of Chrome. I can't be certain it's the same crash but the symptoms are the same.

### rs...@chromium.org (2015-02-25)

Do you have a reduced test case that we could try?

### [Deleted User] (2015-02-25)

The best I can do is give you access to the system with a small model. I have sent an invitation to rsesek@chromium.org. Please let me know if you receive it. I can also invite anyone else who needs to look at this issue.

I have added a google doc with repro steps and a link to a small model here:

https://docs.google.com/document/d/1SVk9zwFOQTK3TyKOkAFGX413OuU6r7j6NJd9Py8y8XA/edit?usp=sharing

### [Deleted User] (2015-03-03)

Have you guys had any luck reproducing this issue? Please let me know if I can help provide any more information.

### rs...@chromium.org (2015-03-03)

I was not able to reproduce the issue, sorry. It would be very helpful if you could create an isolated test case file that minimizes the reproducible issue.

### [Deleted User] (2015-03-03)

Thanks for the quick response. Do you mean you were able to run the steps I suggested and the crash did not occur, or you were not able to run the steps? 

I will think some more about how to try to isolate this, though it is a difficult problem since the issue only appears in a fairly complex case. I will also try with the latest Chromium.

### rs...@chromium.org (2015-03-03)

If you can still repro on the latest Canary or Chromium, what I'd do is save the entire page (File > Save Page As > Web Page, Complete), and then start removing resources and code while it still reproduces.

### [Deleted User] (2015-03-03)

Unfortunately, it's not that simple to produce a simple test case. The system is a cloud-based CAD modeling system and it loads geometry over a socket connection for rendering. The crash happens when rendering graphics after a lot of socket communication has occurred. While theoretically possible, it isn't practical for us right now to engineer a version that will run standalone in a page. 

For what it's worth, it still reproduces using the steps I put in the google doc above.

### pi...@chromium.org (2015-03-04)

[Empty comment from Monorail migration]

### kb...@chromium.org (2015-03-09)

@jkummerow and I have both reproduced this, him on 32-bit Linux, me on 64-bit Mac. Jakob has triaged it to a good degree though the root cause is not known yet. Jakob, may I assign this to you for further investigation?

Restricting view because the nature of the crash appears to be a possible security issue.


### jk...@chromium.org (2015-03-10)

Yes, I'll look; however I won't have much time this week.

fcole, if you do happen to come across an easier or more reliable way to reproduce this, I'd love to hear about it (would make it easier to bisect, or test if various flags have any impact); but I can also work with the repro we have.

### jk...@chromium.org (2015-03-11)

As I suspected: elements kind confusion leading to invalid stores into arrays. On 32-bit platforms this can be an out-of-bounds store (depending on index). On 64-bit it'll "just" cause corruption (however over lunch we just came up with an idea for a few intermediate steps that can probably turn it into an arbitrary OOB write as well). The issue is triggered by having two HValues referring to the same array, and having one of them transition the array's elements kind, which the other doesn't realize.

Repro:

function boom(a1, a2) {
  // Do something with a2 that needs a map check (for DOUBLE_ELEMENTS).
  var s = a2[0];
  // Emit a load that transitions a1 to FAST_ELEMENTS.
  var t = a1[0];
  // Emit a store to a2 that assumes DOUBLE_ELEMENTS.
  // The map check is considered redundant and will be eliminated.
  a2[0] = 0.3;
}

// Prepare type feedback for the "t = a1[0]" load: fast elements.
var fast_elem = new Array(1);
fast_elem[0] = "tagged";
boom(fast_elem, [1]);

// Prepare type feedback for the "a2[0] = 0.3" store: double elements.
var double_elem = new Array(1);
double_elem[0] = 0.1;
boom(double_elem, double_elem);

// Reset |double_elem| and go have a party.
double_elem = new Array(10);
double_elem[0] = 0.1;

%OptimizeFunctionOnNextCall(boom);
boom(double_elem, double_elem);

assertEquals(0.3, double_elem[0]);
assertEquals(undefined, double_elem[1]);


--nocheck-elimination fixes it. Probably what we need to do is in HCheckElimination, whenever an HTransitionElementsKind is seen, discard all knowledge about all HValues with JSArray maps.

Igor offered to take a look. Thanks!

We've had this bug for about a year now, so once we have a fix it should be backmerged to all channels.

### in...@chromium.org (2015-03-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-11)

[Empty comment from Monorail migration]

### kb...@chromium.org (2015-03-11)

Excellent diagnosis Jakob. Thank you for getting to the bottom of this and for coming up with a minimized reproduction.


### bu...@chromium.org (2015-03-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0902b5f4dfdea599bf3d96fb9fb258904aff84ec

commit 0902b5f4dfdea599bf3d96fb9fb258904aff84ec
Author: ishell <ishell@chromium.org>
Date: Thu Mar 12 11:44:23 2015

Incorrect handling of HTransitionElementsKind in hydrogen check elimination phase fixed.

BUG=chromium:460917
LOG=Y

Review URL: https://codereview.chromium.org/1000893003

Cr-Commit-Position: refs/heads/master@{#27154}

[modify] http://crrev.com/0902b5f4dfdea599bf3d96fb9fb258904aff84ec/src/hydrogen-check-elimination.cc
[modify] http://crrev.com/0902b5f4dfdea599bf3d96fb9fb258904aff84ec/src/hydrogen-instructions.h
[add] http://crrev.com/0902b5f4dfdea599bf3d96fb9fb258904aff84ec/test/mjsunit/regress/regress-460917.js


### in...@chromium.org (2015-03-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-03-16)

Merge Requested for M42

### am...@google.com (2015-03-16)

[Automated comment] Request affecting a post-stable build (M41), manual review required.

### am...@google.com (2015-03-16)

Approved for M42 (branch: 2311)

### jk...@chromium.org (2015-03-16)

Note that we don't have good Canary coverage yet (due to a V8 revert over the weekend).

### ti...@google.com (2015-03-16)

OK - in that case, best to hold off for a few days and then land the merge at a later time.

### bu...@chromium.org (2015-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/35b44e5fa8542a64117257465b5810e7afca0e27

commit 35b44e5fa8542a64117257465b5810e7afca0e27
Author: ishell@chromium.org <ishell@chromium.org>
Date: Thu Mar 19 15:51:55 2015

Version 4.2.77.8 (cherry-pick)

Merged 0902b5f4dfdea599bf3d96fb9fb258904aff84ec

Incorrect handling of HTransitionElementsKind in hydrogen check elimination phase fixed.

BUG=chromium:460917
LOG=N
R=jkummerow@chromium.org

Review URL: https://codereview.chromium.org/1019033004

Cr-Commit-Position: refs/branch-heads/4.2@{#9}
Cr-Branched-From: 3dfd929ea07487f2295553df397720d8d75d227c-refs/heads/4.2.77@{#2}
Cr-Branched-From: e0110920d6f98f0ba2ac0d680f635ae3f094a04e-refs/heads/master@{#26757}

[modify] http://crrev.com/35b44e5fa8542a64117257465b5810e7afca0e27/include/v8-version.h
[modify] http://crrev.com/35b44e5fa8542a64117257465b5810e7afca0e27/src/hydrogen-check-elimination.cc
[modify] http://crrev.com/35b44e5fa8542a64117257465b5810e7afca0e27/src/hydrogen-instructions.h
[add] http://crrev.com/35b44e5fa8542a64117257465b5810e7afca0e27/test/mjsunit/regress/regress-460917.js


### bu...@chromium.org (2015-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1ae3be793d3a643a098f2706f4369d20976c2456

commit 1ae3be793d3a643a098f2706f4369d20976c2456
Author: ishell@chromium.org <ishell@chromium.org>
Date: Thu Mar 19 16:03:09 2015

Version 4.1.0.24 (cherry-pick)

Merged 0902b5f4dfdea599bf3d96fb9fb258904aff84ec

Incorrect handling of HTransitionElementsKind in hydrogen check elimination phase fixed.

BUG=chromium:460917
LOG=N
R=jkummerow@chromium.org

Review URL: https://codereview.chromium.org/1020863005

Cr-Commit-Position: refs/branch-heads/4.1@{#26}
Cr-Branched-From: 2e08d2a7aa9d65d269d8c57aba82eb38a8cb0a18-refs/heads/candidates@{#25353}

[modify] http://crrev.com/1ae3be793d3a643a098f2706f4369d20976c2456/include/v8-version.h
[modify] http://crrev.com/1ae3be793d3a643a098f2706f4369d20976c2456/src/hydrogen-check-elimination.cc
[modify] http://crrev.com/1ae3be793d3a643a098f2706f4369d20976c2456/src/hydrogen-instructions.h
[add] http://crrev.com/1ae3be793d3a643a098f2706f4369d20976c2456/test/mjsunit/regress/regress-460917.js


### pe...@google.com (2015-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2015-04-01)

Just saw that this update made it into the stable branch. Tested on my machine and I can no longer produce the crash. Thanks all!

### jk...@chromium.org (2015-04-02)

#33: Thanks for reporting back; glad to hear that the fix indeed resolves the crashes you were seeing.

Also, thanks again for reporting this issue in the first place, and for providing the repro! As you can see from the discussion above, this was quite an important bug for us to find and fix.

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

Congratulations - our reward panel has decided to award you $500 for your help here!

Someone from our finance area should be in contact in two weeks to collect payment details. Please contact me directly if this doesn't happen.

We'll credit you in our release notes as "fcole@onshape.com" (this will go out in our M42 release notes, even though it was fixed earlier). Please let me know if you'd like to use another name or handle.

Cheers,
Tim


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### [Deleted User] (2015-04-14)

Wow, that's generous. Thanks! Happy to help and thanks again for fixing the bug, it's saved me a lot of headache.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### ha...@chromium.org (2016-03-03)

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

This issue was migrated from crbug.com/chromium/460917?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081480)*
