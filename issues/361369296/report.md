# OOB in JSC::StackVisitor::readFrame in webkit/chrome ios

| Field | Value |
|-------|-------|
| **Issue ID** | [361369296](https://issues.chromium.org/issues/361369296) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-08-22 |
| **Bounty** | $7,000.00 |

## Description

Chrome on iOS uses WebKit as its engine, so I use WebKit with ASan to more easily reproduce this vulnerability.

## Reproduce

1.Download WebKit

```
git clone https://github.com/Webkit/WebKit

```

2.Build WebKit with ASAN(or not)

```
./Tools/Scripts/set-webkit-configuration --release --asan
./Tools/Scripts/build-webkit

```

3.Open Server and Run MiniBrowser to open poc.html

```
./Tools/Scripts/run-minibrowser --release --url http://127.0.0.1:8888/poc.html

```
## Crash Log

```
./Tools/Scripts/run-minibrowser --release --url http://127.0.0.1:8888/poc.html                                                                            
Starting MiniBrowser with DYLD_FRAMEWORK_PATH set to point to built WebKit in /Users/test/WebKit/WebKitBuild/Release.
AddressSanitizer:DEADLYSIGNAL
=================================================================
==98249==ERROR: AddressSanitizer: SEGV on unknown address 0x000100000018 (pc 0x00011d90703c bp 0x00016f3313f0 sp 0x00016f331360 T0)
==98249==The signal is caused by a READ memory access.
==98249==WARNING: invalid path to external symbolizer!
==98249==WARNING: Failed to use and restart external symbolizer!
    #0 0x11d90703c in JSC::StackVisitor::readFrame(JSC::CallFrame*)+0x90 (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x273303c)
    #1 0x11d8e7194 in JSC::Interpreter::getStackTrace(JSC::JSCell*, WTF::Vector<JSC::StackFrame, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&, unsigned long, unsigned long, JSC::JSCell*, JSC::JSCell*, JSC::CallLinkInfo*)+0x41c (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x2713194)
    #2 0x11e0dbe98 in JSC::ErrorInstance::finishCreation(JSC::VM&, WTF::String const&, JSC::JSValue, WTF::String (*)(WTF::String const&, WTF::StringView, JSC::RuntimeType, JSC::ErrorInstance::SourceTextWhereErrorOccurred), JSC::RuntimeType, bool)+0x210 (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x2f07e98)
    #3 0x11deda4e8 in JSC::ErrorInstance::create(JSC::VM&, JSC::Structure*, WTF::String const&, JSC::JSValue, WTF::String (*)(WTF::String const&, WTF::StringView, JSC::RuntimeType, JSC::ErrorInstance::SourceTextWhereErrorOccurred), JSC::RuntimeType, JSC::ErrorType, bool)+0x104 (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x2d064e8)
    #4 0x11f1ee870 in JSC::createJSWebAssemblyRuntimeError(JSC::JSGlobalObject*, JSC::VM&, JSC::Wasm::ExceptionType)+0x484 (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x401a870)
    #5 0x11f0e5ec4 in JSC::Wasm::throwWasmToJSException(JSC::CallFrame*, JSC::Wasm::ExceptionType, JSC::JSWebAssemblyInstance*)+0x170 (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x3f11ec4)
    #6 0x145a5c5e0  (<unknown module>)
    #7 0x145a6c48c  (<unknown module>)

==98249==Register values:
 x[0] = 0x0000000100000018   x[1] = 0x0000000100000000   x[2] = 0x000000011aa48800   x[3] = 0x0000000000000000  
 x[4] = 0x0000000000000064   x[5] = 0x0000000000000000   x[6] = 0x0000000000000000   x[7] = 0x0000000000000000  
 x[8] = 0x0000000000000000   x[9] = 0x000000011fde41e3  x[10] = 0x00000000000003cf  x[11] = 0x000000002de663cd  
x[12] = 0x000000702de86240  x[13] = 0x0000000023549106  x[14] = 0xfdfdfafa0000fafa  x[15] = 0x0000000000000006  
x[16] = 0x000000018b27ded0  x[17] = 0x00000001013c85e8  x[18] = 0x0000000000000000  x[19] = 0x000000016f331570  
x[20] = 0x0000000100000000  x[21] = 0x000000002de662c8  x[22] = 0x000000702de8626c  x[23] = 0x0000007000020000  
x[24] = 0x000000016f331360  x[25] = 0x0000000000000001  x[26] = 0x000000002de662b0  x[27] = 0x0000000000000001  
x[28] = 0x000000002de662b5     fp = 0x000000016f3313f0     lr = 0x000000011d8e7198     sp = 0x000000016f331360  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/Users/test/WebKit/WebKitBuild/Release/JavaScriptCore.framework/Versions/A/JavaScriptCore:arm64+0x273303c) in JSC::StackVisitor::readFrame(JSC::CallFrame*)+0x90
==98249==ABORTING
2024-08-22 10:31:47.105 MiniBrowser[98238:1514316] WebContent process crashed; reloading

```

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.8 KB)
- [2.png](attachments/2.png) (image/png, 261.3 KB)
- [1.png](attachments/1.png) (image/png, 559.9 KB)

## Timeline

### ar...@chromium.org (2024-08-23)

Thanks!

This is an iOS bug. So I am going to follow the [specific instructions](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md).

- Could you please report the issue directly to Webkit and provide us the WebKit issue ID?
- `Need-Feedback`: Do you know if this affect Chrome on iOS? What are the reproduction steps?
- All security issues need owners, the WebKit ones can be assigned to ajuma@.

### je...@gmail.com (2024-08-23)

I didn't report this bug to Apple. I only reported it to Google. You can help me open an issue for Apple. Just completely copy and reproduce the steps.

I think this will affect Chrome for iOS. Because it is the same as the mini browser I used for testing and should both directly use the WebKit kernel. So this reproduction should be reliable.

You may encounter a compilation warning when reproducing with the latest version of WebKit:

```
Source/JavaScriptCore/wasm/WasmOperations.cpp:331:17: error: unused variable 'jsCallerCC' [-Werror,-Wunused-variable]
    const auto& jsCallerCC = jsCallingConvention().callInformationFor(typeDefinition, CallRole::Caller);
                ^
1 error generated.

```

Just comment out that line.

As of now, I can still reproduce this problem on the latest version of WebKit. The current commit hash is:

```
commit 9a5672cee350242fc097767027e9fd8feaa638f9 (HEAD -> main, origin/main, origin/HEAD)
Author: Nitin Mahendru <nitinmahendru@apple.com>
Date:   Fri Aug 23 14:40:49 2024 -0700

    Use actual version numbers for Fall 2024 OS releases.
    https://bugs.webkit.org/show_bug.cgi?id=275439
    rdar://125427383
    
    Reviewed by Elliott Williams.
    
    Use the newly announced version numbers for API availability annotations.
    They are now public as per announcements at WWDC 24'.
    So we can safely remove the future value that is 9999.0 as these APIs need to be marked available.
    
    * Source/WebKit/WebKitSwift/GroupActivities/GroupSession.swift:
    
    Canonical link: https://commits.webkit.org/282676@main

```

In addition, it is also possible to reproduce this bug using jsc on Linux. such as:

```
➜  ~ /home/test/WebKit/FuzzBuild/bin/jsc poc.js
UndefinedBehaviorSanitizer:DEADLYSIGNAL
==316776==ERROR: UndefinedBehaviorSanitizer: SEGV on unknown address 0x7fff00000018 (pc 0x55fc8458ef18 bp 0x55fc859b112c sp 0x7fff2af767e0 T316776)
==316776==The signal is caused by a READ memory access.
    #0 0x55fc8458ef18 in JSC::CalleeBits::isNativeCallee() const /home/test/WebKit/Source/JavaScriptCore/interpreter/CalleeBits.h:131:52
    #1 0x55fc8458ef18 in JSC::CallFrame::isNativeCalleeFrame() const /home/test/WebKit/Source/JavaScriptCore/interpreter/CallFrameInlines.h:93:21
    #2 0x55fc8458ef18 in JSC::StackVisitor::readFrame(JSC::CallFrame*) /home/test/WebKit/Source/JavaScriptCore/interpreter/StackVisitor.cpp:116:20
    #3 0x55fc8458283c in void JSC::StackVisitor::visit<(JSC::StackVisitor::EmptyEntryFrameAction)0, JSC::Interpreter::getStackTrace(JSC::JSCell*, WTF::Vector<JSC::StackFrame, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&, unsigned long, unsigned long, JSC::JSCell*, JSC::JSCell*, JSC::CallLinkInfo*)::$_7>(JSC::CallFrame*, JSC::VM&, JSC::Interpreter::getStackTrace(JSC::JSCell*, WTF::Vector<JSC::StackFrame, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&, unsigned long, unsigned long, JSC::JSCell*, JSC::JSCell*, JSC::CallLinkInfo*)::$_7 const&, bool) /home/test/WebKit/Source/JavaScriptCore/interpreter/StackVisitor.h:157:21
    #4 0x55fc8458283c in JSC::Interpreter::getStackTrace(JSC::JSCell*, WTF::Vector<JSC::StackFrame, 0ul, WTF::CrashOnOverflow, 16ul, WTF::FastMalloc>&, unsigned long, unsigned long, JSC::JSCell*, JSC::JSCell*, JSC::CallLinkInfo*) /home/test/WebKit/Source/JavaScriptCore/interpreter/Interpreter.cpp:520:5
    #5 0x55fc84a1c92e in JSC::getStackTrace(JSC::VM&, JSC::JSObject*, bool, JSC::JSCell*, JSC::CallLinkInfo*) /home/test/WebKit/Source/JavaScriptCore/runtime/Error.cpp:172:20
    #6 0x55fc84a1c92e in JSC::ErrorInstance::finishCreation(JSC::VM&, WTF::String const&, JSC::JSValue, WTF::String (*)(WTF::String const&, WTF::StringView, JSC::RuntimeType, JSC::ErrorInstance::SourceTextWhereErrorOccurred), JSC::RuntimeType, bool) /home/test/WebKit/Source/JavaScriptCore/runtime/ErrorInstance.cpp:118:54
    #7 0x55fc8549926d in JSC::ErrorInstance::create(JSC::VM&, JSC::Structure*, WTF::String const&, JSC::JSValue, WTF::String (*)(WTF::String const&, WTF::StringView, JSC::RuntimeType, JSC::ErrorInstance::SourceTextWhereErrorOccurred), JSC::RuntimeType, JSC::ErrorType, bool) /home/test/WebKit/Source/JavaScriptCore/runtime/ErrorInstance.h:60:19
    #8 0x55fc8549926d in JSC::createJSWebAssemblyRuntimeError(JSC::JSGlobalObject*, JSC::VM&, JSC::Wasm::ExceptionType) /home/test/WebKit/Source/JavaScriptCore/wasm/js/JSWebAssemblyRuntimeError.cpp:43:28
    #9 0x55fc853f5d01 in JSC::Wasm::throwWasmToJSException(JSC::CallFrame*, JSC::Wasm::ExceptionType, JSC::JSWebAssemblyInstance*) /home/test/WebKit/Source/JavaScriptCore/wasm/WasmOperationsInlines.h:806:21
    #10 0x7fd8e0034032  (<unknown module>)

UndefinedBehaviorSanitizer can not provide additional info.
SUMMARY: UndefinedBehaviorSanitizer: SEGV /home/test/WebKit/Source/JavaScriptCore/interpreter/CalleeBits.h:131:52 in JSC::CalleeBits::isNativeCallee() const
==316776==ABORTING

```

### pe...@google.com (2024-08-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2024-08-26)

This is a bug in WebKit, not in Chromium. Please report this to Apple as [documented in our processes](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#:~:text=Chrome%20for%20iOS%20%2D%20bugs%20suspected%20to%20be%20in%20WebKit):

You may do so at <https://bugs.webkit.org/enter_bug.cgi?product=Security>, or at <https://security.apple.com/bounty/>

### je...@gmail.com (2024-08-26)

Here: <https://bugs.webkit.org/show_bug.cgi?id=278650>

### je...@gmail.com (2024-08-27)

Fix here:
<https://github.com/WebKit/WebKit/commit/cb7f341491b77d31200bd7d273d7a89ae17a52fc>

@ajuma, Please let me know what our next step is?

### aj...@google.com (2024-08-27)

The next step is to wait for this fix to ship in an iOS release. And the timing of that depends on whether Apple decides to cherry-pick the fix to a release branch (in that case, this could ship as soon as iOS 18.1) or if they wait for the next time they branch WebKit from trunk (they don't announce this, but based on past history, the next branch point would be in January, to ship in the March release of iOS).

Since the POC doesn't crash in non-ASan builds, to figure out if Apple has cherry-picked the fix we'll have to look at the release tags here: <https://github.com/WebKit/WebKit/tags> (Apple's releases are the ones starting in WebKit-76).

Once that happens, we can mark this bug as fixed. For now, I'll set a NextAction date for November to see if this fix made it into 18.1.

### pe...@google.com (2024-11-11)

The NextAction date has arrived: 2024-11-11
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### aj...@google.com (2024-11-11)

Not in 18.1 (based on browsing the tags that Apple added in October). So this will likely not ship until the March release of iOS.

### aj...@google.com (2024-11-11)

Please mark this as Fixed whenever the March release of iOS is out.

### pe...@google.com (2025-01-09)

michaeldo: Uh oh! This issue still open and hasn't been updated in the last 58 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-24)

michaeldo: Uh oh! This issue still open and hasn't been updated in the last 73 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-03-10)

The NextAction date has arrived: 2025-03-10
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pe...@google.com (2025-03-25)

The NextAction date has arrived: 2025-03-25
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### mi...@google.com (2025-03-25)

This fix was released in iOS 18.2. I was able to verify by comparing the tag on the [webkit commit](https://github.com/WebKit/WebKit/commit/cb7f341491b77d31200bd7d273d7a89ae17a52fc) which is "WebKit-7620.1.10" to the version listed at <https://opensource.apple.com/releases/> (I also downloaded the version archive to verify.)

### ch...@google.com (2025-03-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-03-27)

AFAICT (which is very little since I don't have access to the bug in the WebKit tracker) is that this issue was fixed based on this report, so I'm going to update this as Fixed.
I did not find anything in [Apple's security fix notes for 18.2](https://support.apple.com/en-us/121837) about this issue to verify this, however.

### ch...@google.com (2025-03-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-03-27)

copy paste error on my part

### je...@gmail.com (2025-03-28)

<https://github.com/WebKit/WebKit/pull/32739>
<https://bugs.webkit.org/show_bug.cgi?id=278650>

Apple's bug acknowledgments are always messed up, but you can see the connection between PR and my report.

### ch...@google.com (2025-03-28)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-04-03)

Realizing because this was closed as `wontfix` originally it was set as reward-ineligible. I'm going to send this to the panel, however, I do want to levelset expectations, looking through this report there is no demonstration that this is reachable and exploitable in Chrome. While we do ship webkit in Chrome on iOS, it doesn't mean that all webkit issues are exploitable through Chrome. I've looked through our history of webkit JSC issues and the specific cases we have rewarded when webkit JSC was involved is where a demonstration of exploitation in Chrome was provided.

### sp...@google.com (2025-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-10)

Congratulations Sakura! Thank you for your efforts and reporting this issue to Apple WebKit and us!

### ch...@google.com (2025-07-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361369296)*
