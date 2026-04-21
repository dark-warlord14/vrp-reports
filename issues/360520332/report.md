# Google Chrome on iOS sad tabs with the following testcase.

| Field | Value |
|-------|-------|
| **Issue ID** | [360520332](https://issues.chromium.org/issues/360520332) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Chrome Version** | 128.0.6613.34 |
| **Reporter** | nt...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-08-18 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

Put the following testcase in a file, e.g. testcase.html:

<script>
let x = new Intl.Locale("en-variant0-variant1-variant2-variant3-variant4-variant5-variant6-variant7-variant8-variant9-varianta-variantb-variantc-variantd-variante-variantf-variantg-varianth-varianti-variantj");
x["getHourCycles"]();
</script>
# Problem Description

The testcase should not sad tab.

# Additional Comments

This goes as far back as GitHub WebKit rev 34d7f551c40a (Apr 23, 2024) and happens as recently as WebKit rev 718f9c8cd131.

Once again, how do I get a crash stack for Google Chrome on iOS? I can't find anything in Settings -> Privacy & Security -> Analytics Data, only WebKit / Safari logs their crash stacks there.

# Summary

Google Chrome on iOS sad tabs with the following testcase.

# Custom Questions

#### Type of crash:

tab

#### Crash state:

Question: How do I get a crash stack for Google Chrome on iOS? I can't find anything in Settings -> Privacy & Security -> Analytics Data, only WebKit / Safari logs their crash stacks there.

I've attached WebKit stacks instead because Google Chrome on iOS should be using WebKit.

$ sw\_vers
ProductName: macOS
ProductVersion: 14.6.1
BuildVersion: 23G93

Using the following js testcase:

let x = new Intl.Locale("en-variant0-variant1-variant2-variant3-variant4-variant5-variant6-variant7-variant8-variant9-varianta-variantb-variantc-variantd-variante-variantf-variantg-varianth-varianti-variantj");
x"getHourCycles";

(compile with ./Tools/Scripts/build-jsc --jsc-only --debug --cmakeargs="-DCMAKE\_C\_COMPILER='/usr/bin/clang' -DCMAKE\_CXX\_COMPILER='/usr/bin/clang++'" )
on a WebKit debug build rev 718f9c8cd131:

Process 26274 stopped

- thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGABRT
  frame #0: 0x000000019d0895f0 libsystem\_kernel.dylib`__pthread_kill + 8 libsystem_kernel.dylib`:
  -> 0x19d0895f0 <+8>: b.lo 0x19d089610 ; <+40>
  0x19d0895f4 <+12>: pacibsp
  0x19d0895f8 <+16>: stp x29, x30, [sp, #-0x10]!
  0x19d0895fc <+20>: mov x29, sp
  Target 0: (jsc) stopped.
  (lldb) bt
- thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGABRT
  - frame #0: 0x000000019d0895f0 libsystem\_kernel.dylib`__pthread_kill + 8 frame #1: 0x000000019d0c1c20 libsystem_pthread.dylib`pthread\_kill + 288
    frame #2: 0x000000019cfceac4 libsystem\_c.dylib`__abort + 136 frame #3: 0x000000019cfc025c libsystem_c.dylib`\_\_stack\_chk\_fail + 96
    frame #4: 0x00000001a036452c libicucore.A.dylib`icu::DateTimePatternGenerator::addICUPatterns(icu::Locale const&, UErrorCode&) + 1320 frame #5: 0x00000001a0362ee4 libicucore.A.dylib`icu::DateTimePatternGenerator::initData(icu::Locale const&, UErrorCode&, signed char) + 76
    frame #6: 0x00000001a0362e70 libicucore.A.dylib`icu::DateTimePatternGenerator::DateTimePatternGenerator(icu::Locale const&, UErrorCode&, signed char) + 804 frame #7: 0x00000001a036269c libicucore.A.dylib`icu::DateTimePatternGenerator::createInstance(icu::Locale const&, UErrorCode&, signed char) + 92
    frame #8: 0x00000001a044bc98 libicucore.A.dylib`udatpg_open + 84 frame #9: 0x000000010976db5c JavaScriptCore`JSC::IntlLocale::hourCycles(this=0x0000000101018c48, globalObject=0x0000000102074088) at IntlLocale.cpp:670:91
    frame #10: 0x00000001097b56d0 JavaScriptCore`JSC::intlLocalePrototypeFuncGetHourCycles(globalObject=0x0000000102074088, callFrame=0x000000016fdfdc10) at IntlLocalePrototype.cpp:282:5
    frame #11: 0x000000011729003c
    (lldb)

(compile with ./Tools/Scripts/build-jsc --jsc-only --cmakeargs="-DCMAKE\_C\_COMPILER='/usr/bin/clang' -DCMAKE\_CXX\_COMPILER='/usr/bin/clang++'" )
Opt build on WebKit rev 718f9c8cd131:

Process 26285 stopped

- thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGABRT
  frame #0: 0x000000019d0895f0 libsystem\_kernel.dylib`__pthread_kill + 8 libsystem_kernel.dylib`:
  -> 0x19d0895f0 <+8>: b.lo 0x19d089610 ; <+40>
  0x19d0895f4 <+12>: pacibsp
  0x19d0895f8 <+16>: stp x29, x30, [sp, #-0x10]!
  0x19d0895fc <+20>: mov x29, sp
  Target 0: (jsc) stopped.
  (lldb) bt
- thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGABRT
  - frame #0: 0x000000019d0895f0 libsystem\_kernel.dylib`__pthread_kill + 8 frame #1: 0x000000019d0c1c20 libsystem_pthread.dylib`pthread\_kill + 288
    frame #2: 0x000000019cfceac4 libsystem\_c.dylib`__abort + 136 frame #3: 0x000000019cfc025c libsystem_c.dylib`\_\_stack\_chk\_fail + 96
    frame #4: 0x00000001a036452c libicucore.A.dylib`icu::DateTimePatternGenerator::addICUPatterns(icu::Locale const&, UErrorCode&) + 1320 frame #5: 0x00000001a0362ee4 libicucore.A.dylib`icu::DateTimePatternGenerator::initData(icu::Locale const&, UErrorCode&, signed char) + 76
    frame #6: 0x00000001a0362e70 libicucore.A.dylib`icu::DateTimePatternGenerator::DateTimePatternGenerator(icu::Locale const&, UErrorCode&, signed char) + 804 frame #7: 0x00000001a036269c libicucore.A.dylib`icu::DateTimePatternGenerator::createInstance(icu::Locale const&, UErrorCode&, signed char) + 92
    frame #8: 0x00000001a044bc98 libicucore.A.dylib`udatpg_open + 84 frame #9: 0x0000000103209180 JavaScriptCore`JSC::IntlLocale::hourCycles(JSC::JSGlobalObject\*) + 224
    frame #10: 0x0000000103228324 JavaScriptCore`JSC::intlLocalePrototypeFuncGetHourCycles(JSC::JSGlobalObject\*, JSC::CallFrame\*) + 132
    frame #11: 0x000000012481003c
    (lldb)

#### Reporter credit:

Gary Kwong

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 249 B)

## Timeline

### nt...@gmail.com (2024-08-18)

I've attached a slightly more reduced testcase.

As mentioned above, I'd like to know how do I get a crash stack for Google Chrome on iOS? I can't find anything in Settings -> Privacy & Security -> Analytics Data, only WebKit / Safari logs their crash stacks there.

### nt...@gmail.com (2024-08-18)

The Chrome iOS crash happens on iPadOS 17.6.1.

### xi...@chromium.org (2024-08-19)

Thanks for the report. I haven't attempted to reproduce this. +ajuma, could you help answer reporter's question and see if this issue in WebKit affects Chrome on iOS? Setting a provisional severity (S1), assuming this is a UaF in the renderer.

### nt...@gmail.com (2024-08-19)

Additionally, is there a website that shows the corresponding WebKit version used by Chrome on iPadOS 17.6.1 (M2 processor):

Chrome Stable installed from App Store is version 128.0.6613.34, so which WebKit commit is this based on?
Chrome TestFlight is version 128.0.6613.35 beta, so which WebKit commit is this based on?

### sd...@google.com (2024-08-19)

I've tried to load the page testcase.html from Chrome, but only the WKWebView die (i.e. the WebKit sub-process) so there is no Chrome stack. This appears to be fully a WebKit issue, not a Chrome issue.

### aj...@google.com (2024-08-19)

Do you see the same issue on Safari or in other WebKit-based apps? (Safari's UI for renderer crashes is different of course, no sad tab, but instead a message saying that the page had a problem or something to that effect.) If this also crashes in other WebKit apps, please file a WebKit security bug (at <https://bugs.webkit.org/enter_bug.cgi?product=Security>) and let us know the bug number. We can also file one, but if you file it directly it's easier to answer questions they have and to properly get credit for your report.

> Additionally, is there a website that shows the corresponding WebKit version used by Chrome on iPadOS 17.6.1 (M2 processor)

On iOS, the WebKit version is uniquely determined by the iOS version, since WebKit is a system library and can only update when iOS itself is updated. Mapping the iOS version to a WebKit branch is non-trivial. After an iOS version is released there's usual a branch on WebKit's git repository that corresponds to the release branch. You can see all the tags here: <https://github.com/WebKit/WebKit/tags> Based on timing, 17.6.1 likely corresponds to one of the WebKit-7618.3.11.\* branches. It's easier to map desktop Safari to one of these tags (go to Safari -> About Safari, take the version number that starts with 19618.X and that maps to the tag 7618.X).

> As mentioned above, I'd like to know how do I get a crash stack for Google Chrome on iOS?

Renderer crash stacks are not exposed anywhere by iOS afaik (even we don't get them -- iOS doesn't provide this to the app that embeds the WKWebView that crashed). If Chrome itself crashes (the whole app), you should see a stack in the usual spot (Settings -> Privacy & Security -> Analytics Data).

### pe...@google.com (2024-08-19)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### nt...@gmail.com (2024-08-19)

> It's easier to map desktop Safari to one of these tags (go to Safari -> About Safari, take the version number that starts with 19618.X and that maps to the tag 7618.X).

I'm guessing you mean to map iPad Safari as well.

> Do you see the same issue on Safari or in other WebKit-based apps?

Yes, it does seem to.

> If this also crashes in other WebKit apps, please file a WebKit security bug (at https://bugs.webkit.org/enter_bug.cgi?product=Security) and let us know the bug number.

I'm happy to file, but one more question. Would Apple Security (security.apple.com for their bug bounty/properly get credit) be a better place to file if Safari is also affected? Can I then paste the ID here - will that suffice for you? Or do I also file in WebKit Bugzilla -> Security as well?

This question is for you since Apple Security seems slower than WebKit Bugzilla at responding and will affect the speed and progress when I know something to update here, but they seem to imply that only Apple Security ID issues get paid out and I'm not sure about the WebKit Bugzilla.

Thank you for your responses so far, you have been very helpful.

### aj...@google.com (2024-08-19)

I don't know whether Apple's bug bounty program also applies to bugs filed at bugs.webkit.org, so in that case I'd say file at security.apple.com, paste the ID here, and let us know when they tell you the bug is fixed.

If the Apple bounty doesn't matter to you, then a WebKit security bug is a good way to go since it's a more direct way (IMO) of communicating with the WebKit team and we can follow along as well.

### nt...@gmail.com (2024-08-19)

> I'd say file at security.apple.com, paste the ID here, and let us know when they tell you the bug is fixed.

I've filed at security.apple.com, the ID is: OE1992768931411

### aj...@google.com (2024-08-19)

Thanks!

### pe...@google.com (2024-09-03)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### aj...@google.com (2024-09-03)

This is an external dependency, so nags aren't useful.

### pe...@google.com (2024-10-18)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### aj...@google.com (2024-10-18)

As mentioned above, this is an ExternalDependency. This bug is in an Apple product (WKWebView on iOS) and we have no control over the timing of a fix.

### nt...@gmail.com (2024-12-24)

Testing with Google Chrome 132.0.6834.54 beta, with iPadOS 18.1.1 the testcase causes a sad tab, but with iPadOS 18.2, the testcase no longer causes a sad tab.

Please feel free to verify.

### nt...@gmail.com (2025-02-14)

What's next that needs to be done here?

### mi...@google.com (2025-02-18)

Based on previous comments, this appears to be an issue in WebKit, so the only things to be done are follow up on the Apple security bug OE1992768931411 or re-test in Chrome iOS to see if it still reproduces.

### nt...@gmail.com (2025-02-21)

I've already done the test for Chrome iOS as per comment #18.

### mi...@google.com (2025-02-24)

Apologies, it looks like I misread [#comment18](https://issues.chromium.org/issues/360520332#comment18). IIUC, this is now fixed as of iOS 18.2

### ch...@google.com (2025-02-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-02-25)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [132, 133, 134].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@google.com (2025-02-25)

This was an issue in webkit, there are no merges needed.

### sp...@google.com (2025-03-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
below baseline report of memory corruption in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-06)

Congratulations Gary! Thank you for your efforts and reporting this issue to us!

### nt...@gmail.com (2025-03-06)

You're welcome!

### ch...@google.com (2025-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> below baseline report of memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360520332)*
