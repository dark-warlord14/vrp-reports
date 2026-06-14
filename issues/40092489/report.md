# [LangFuzz] CHECK(!value->IsTheHole()) failed // Crash with invalid read in shell

| Field | Value |
|-------|-------|
| **Issue ID** | [40092489](https://issues.chromium.org/issues/40092489) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2011-07-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

The following code crashes an optimized v8 shell (version as in Chrome 14.0.813.0 which is v8-trunk r8431) or asserts in a debug shell. The same code does not crash in Chromium, I suspect it could be that the memory layout is different there and the specific test case therefore fails on Chromium. Please check if this really does not affect Chromium as well.

Debug builds abort with:

# 

# Fatal error in src/objects.cc, line 1797

# CHECK(!value->IsTheHole()) failed

# 

**VERSION**  

V8 Version: <http://v8.googlecode.com/svn/trunk@8431> (as in Chrome Version 14.0.813.0).  

Operating System: Ubuntu Linux 11.04

**REPRODUCTION CASE**

(function () {  

function classOf(object) { typeof(value); };  

})();  

function F() {}  

Object.prototype.**defineSetter**('x', function(value) { result\_x = value; });  

this.**proto** = { x: 42 };  

try {  

fail;  

} catch (e) {  

eval('const x = 7');  

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Shell  

Crash Trace:

==26391== Use of uninitialised value of size 8  

==26391== at 0x4E3490: v8::internal::JSObject::GetNormalizedProperty(v8::internal::LookupResult\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x5502A2: v8::internal::Runtime\_InitializeConstContextSlot(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x9F48341: ???  

==26391== by 0x9F6C0DD: ???  

==26391== by 0x9F48C2D: ???  

==26391== by 0x9F6B08E: ???  

==26391== by 0x9F493E6: ???  

==26391== by 0x9F48127: ???  

==26391== by 0x447FA8: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x448468: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x414477: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x402F73: ExecuteString(v8::Handle[v8::String](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);), bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391==  

==26391== Invalid read of size 8  

==26391== at 0x4E3490: v8::internal::JSObject::GetNormalizedProperty(v8::internal::LookupResult\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x5502A2: v8::internal::Runtime\_InitializeConstContextSlot(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x9F48341: ???  

==26391== by 0x9F6C0DD: ???  

==26391== by 0x9F48C2D: ???  

==26391== by 0x9F6B08E: ???  

==26391== by 0x9F493E6: ???  

==26391== by 0x9F48127: ???  

==26391== by 0x447FA8: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x448468: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Object\*\*\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x414477: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== by 0x402F73: ExecuteString(v8::Handle[v8::String](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);), bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/shell)  

==26391== Address 0xffffffff96781a20 is not stack'd, malloc'd or (recently) free'd  

==26391==  

==26391==  

==26391== Process terminating with default action of signal 11 (SIGSEGV)  

==26391== Access not within mapped region at address 0xFFFFFFFF96781A20

## Timeline

### in...@chromium.org (2011-07-06)

Mads, can you please help to triage.

### sc...@gmail.com (2011-07-08)

(Add Erik "fixing machine" Corry and Soren to cc: as well)

### er...@gmail.com (2011-07-08)

I sending this on to Vyacheslav because I am on my way out of the door for a vacation.

### sc...@gmail.com (2011-07-08)

Happy vacation :)

### in...@chromium.org (2011-07-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2011-07-10)

Kevin, could this be related to r8496?

### ri...@chromium.org (2011-07-10)

Never mind, I did a revert of 8496 and the failure is still there.

### de...@googlemail.com (2011-07-10)

A bisect shows r8224 as the revision introducing this, but given the log text, I'm not sure that's accurate.

### sc...@gmail.com (2011-07-11)

@inferno: is this marked Mstone-13 because the test case also crashes M13?

### ri...@chromium.org (2011-07-11)

decoder: r8224 actually makes good sense, since this is only crashing with try-catch. 

### km...@chromium.org (2011-07-11)

I'll take a look.

### km...@chromium.org (2011-07-11)

This was previously reported as http://code.google.com/p/v8/issues/detail?id=1528.

Bug was introduced in http://code.google.com/p/v8/source/detail?r=8224, fixed in http://code.google.com/p/v8/source/detail?r=8523.  It affects V8 trunk versions in the range 3.4.4 to 3.4.8, inclusive.

### km...@chromium.org (2011-07-11)

I spoke too soon, this bug is still present in v8 bleeding_edge.  I'm working on a fix.

### km...@chromium.org (2011-07-11)

I did speak too soon.  Though it has a very similar reproduction, this is a different issue than http://code.google.com/p/v8/issues/detail?id=1528.

This bug has nothing essential to do with try/catch.  The assertion can also be triggered by:

Object.prototype.__defineSetter__('x', function (x) {});
this.__proto__ = { x: 42 };
with ({}) { eval('const x = 7'); }


### km...@chromium.org (2011-07-11)

Sorry, was fixed in http://code.google.com/p/v8/source/detail?r=8602

### in...@chromium.org (2011-07-11)

Kevin has pushed the fix to m13 and m12 branches.

### sc...@gmail.com (2011-07-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-20)

@decoder.oh: thanks for your continued help in catching these very interesting corner-case v8 issues! It's a fairly easy panel decision to offer you a $1000 Chromium Security Reward for your help.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/88591?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092489)*
