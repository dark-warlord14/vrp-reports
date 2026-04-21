# UAF in GestureRecognizerImpl.

| Field | Value |
|-------|-------|
| **Issue ID** | [40059659](https://issues.chromium.org/issues/40059659) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input, UI>Input |
| **Platforms** | ChromeOS |
| **Reporter** | pt...@vewd.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-05-13 |
| **Bounty** | $5,000.00 |

## Description

This has been introduced in d2fdb99a2b5d87c75fef69968d4d477cbd66ebd9, "[ui] Handle late ACKed touch events more properly"

With this change in place we can have the following sequence of events:

1. GestureRecognizerImpl::consumer\_gesture\_provider\_ map holds std::unique\_ptr<GestureProviderAura>.
2. GestureRecognizerImpl destructor gets called which default implementation first destroys event\_to\_gesture\_provider\_ member followed by consumer\_gesture\_provider\_.
3. Since consumer\_gesture\_provider\_ holds unique\_ptr's to GestureProviderAura this class destructor gets called.
4. With the linked patch in place GestureProviderAura destructor calls GestureProviderAuraClient::OnGestureProviderAuraWillBeDestroyed which is implemented by GestureRecognizerImpl.
5. GestureRecognizerImpl::OnGestureProviderAuraWillBeDestroyed starts iterating over event\_to\_gesture\_provider\_ map which has been destroyed in step 2, leading to UAF.

I don't think this is easily exploitable since the time window between use and free is pretty narrow. Still its a UAF that affects current beta so I've decided to report it as a security bug.

**VERSION**  

Chrome Version: [104.0.5061.0] + [beta, dev] basically anything newer that M101.  

Operating System: Linux

**REPRODUCTION CASE**  

I have only reproduced this using some internal Vewd test suites, but the bug should be pretty easy to see after short code analysis.

**CREDIT INFORMATION**  

Reporter credit: Piotr Tworek, Vewd Software

## Timeline

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-15)

Thanks for your report. Since you added a particular CL I'm CCing those developers while Chrome OS do additional triage.

[Monorail components: Blink>Input UI>Shell>TabletMode]

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-05-17)

I believe it is a UAF issue. I wrote a test (https://chromium-review.googlesource.com/c/chromium/src/+/3648376/4) trying to reproduce the issue. Surprisingly, this UAF issue is not caught by ASAN. I am still investigating why ASAN fails to detect this UAF issue. 

### an...@chromium.org (2022-05-17)

Here is the stack trace of `GestureRecognizerImpl::OnGestureProviderAuraWillBeDestroyed`

ERROR aura_unittests[3378587:3378587]: [gesture_recognizer_impl.cc(407)] GestureRecognizerImpl::OnGestureProviderAuraWillBeDestroyed
    #0 0x56176d17b68b in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4379:13
    #1 0x561771517579 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:874:39
    #2 0x5617712d97c3 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #3 0x5617712d97c3 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x561771dff907 in ui::GestureRecognizerImpl::OnGestureProviderAuraWillBeDestroyed(ui::GestureProviderAura*) ./../../ui/events/gestures/gesture_recognizer_impl.cc:408:3
    #5 0x561771e01eb9 in ui::GestureProviderAura::~GestureProviderAura() ./../../ui/events/gestures/gesture_provider_aura.cc:43:12
    #6 0x561771e01f14 in ui::GestureProviderAura::~GestureProviderAura() ./../../ui/events/gestures/gesture_provider_aura.cc:42:45
    #7 0x561771e00112 in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #8 0x561771e00112 in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #9 0x561771e00112 in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #10 0x561771e00112 in ~pair ./../../buildtools/third_party/libc++/trunk/include/utility:394:29
    #11 0x561771e00112 in destroy<std::__1::pair<ui::GestureConsumer *const, std::__1::unique_ptr<ui::GestureProviderAura, std::__1::default_delete<ui::GestureProviderAura> > >, void, void> ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #12 0x561771e00112 in std::__1::__tree<std::__1::__value_type<ui::GestureConsumer*, std::__1::unique_ptr<ui::GestureProviderAura, std::__1::default_delete<ui::GestureProviderAura> > >, std::__1::__map_value_compare<ui::GestureConsumer*, std::__1::__value_type<ui::GestureConsumer*, std::__1::unique_ptr<ui::GestureProviderAura, std::__1::default_delete<ui::GestureProviderAura> > >, std::__1::less<ui::GestureConsumer*>, true>, std::__1::allocator<std::__1::__value_type<ui::GestureConsumer*, std::__1::unique_ptr<ui::GestureProviderAura, std::__1::default_delete<ui::GestureProviderAura> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<ui::GestureConsumer*, std::__1::unique_ptr<ui::GestureProviderAura, std::__1::default_delete<ui::GestureProviderAura> > >, void*>*) ./../../buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #13 0x561771dfae5a in ~__tree ./../../buildtools/third_party/libc++/trunk/include/__tree:1789:3
    #14 0x561771dfae5a in ~map ./../../buildtools/third_party/libc++/trunk/include/map:1103:5
    #15 0x561771dfae5a in ui::GestureRecognizerImpl::~GestureRecognizerImpl() ./../../ui/events/gestures/gesture_recognizer_impl.cc:68:47
    #16 0x561771dfaf00 in ui::GestureRecognizerImpl::~GestureRecognizerImpl() ./../../ui/events/gestures/gesture_recognizer_impl.cc:68:47
    #17 0x56176d2efc44 in aura::test::GestureRecognizerTest_ResetGestureRecognizerWithGestureProvider_Test::TestBody() ./../../ui/aura/gestures/gesture_recognizer_unittest.cc:4842:29
    #18 0x5617704146c2 in HandleExceptionsInMethodIfSupported<testing::Test, void> ./../../third_party/googletest/src/googletest/src/gtest.cc:0:0
    #19 0x5617704146c2 in testing::Test::Run() ./../../third_party/googletest/src/googletest/src/gtest.cc:2670:5
    #20 0x561770416110 in testing::TestInfo::Run() ./../../third_party/googletest/src/googletest/src/gtest.cc:2849:11
    #21 0x5617704180bb in testing::TestSuite::Run() ./../../third_party/googletest/src/googletest/src/gtest.cc:3008:30
    #22 0x56177043b85a in testing::internal::UnitTestImpl::RunAllTests() ./../../third_party/googletest/src/googletest/src/gtest.cc:5866:44
    #23 0x56177043aea5 in HandleExceptionsInMethodIfSupported<testing::internal::UnitTestImpl, bool> ./../../third_party/googletest/src/googletest/src/gtest.cc:0:0
    #24 0x56177043aea5 in testing::UnitTest::Run() ./../../third_party/googletest/src/googletest/src/gtest.cc:5440:10
    #25 0x5617707cdcec in RUN_ALL_TESTS ./../../third_party/googletest/src/googletest/include/gtest/gtest.h:2284:73
    #26 0x5617707cdcec in base::TestSuite::Run() ./../../base/test/test_suite.cc:460:16
    #27 0x56176f5f2943 in base::OnceCallback<int ()>::Run() && ./../../base/callback.h:143:12
    #28 0x5617707d55e9 in base::(anonymous namespace)::LaunchUnitTestsInternal(base::OnceCallback<int ()>, unsigned long, int, unsigned long, bool, base::OnceCallback<void ()>) ./../../base/test/launcher/unit_test_launcher.cc:177:38
    #29 0x5617707d5276 in base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long) ./../../base/test/launcher/unit_test_launcher.cc:268:10
    #30 0x56176d30bb79 in main ./../../ui/aura/test/run_all_unittests.cc:67:10
    #31 0x7f6643b957fd in __libc_start_main ./csu/../csu/libc-start.c:332:16
    #32 0x56176d13fdea in _start ??:0:0


### pt...@vewd.com (2022-05-18)

For ASAN to report this you'll likely need GestureRecognizerImpl::event_to_gesture_provider_ map to be non empty. The fact that GestureRecognizerImpl indirectly calls ::OnGestureProviderAuraWillBeDestroyed is not ideal, but not fatal by itself. Problems start when the method iterates over event_to_gesture_provider_ map which at this point was freed.

In our setup we have an internal python test framework on top of chromium and this UAF can sometimes crash during touch input tests.

### an...@chromium.org (2022-05-18)

Reply to https://crbug.com/chromium/1325256#c9: I believe my CL in https://crbug.com/chromium/1325256#c7 ensures that `GestureRecognizerImpl::event_to_gesture_provider_ map` is non-empty. 

Also, the original UAF issue should occur during `GestureRecognizerImpl::dtor()` which should be called in `Env::dtor()`. It should be abnormal in the real world that  `GestureRecognizerImpl::event_to_gesture_provider_ map` is non-empty during `Env::dtor()`. Because `Window::CleanupGestureState()` is called a lot. It could explain partly why we have not received any related crash reports.

### an...@chromium.org (2022-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bf900c8c6744773f5a7031482d28c50c9d115a61

commit bf900c8c6744773f5a7031482d28c50c9d115a61
Author: Andrew Xu <andrewxu@chromium.org>
Date: Fri May 27 20:03:41 2022

[ui] Handle notifications sent by gesture provider during destruction

This CL clears `GestureRecognizerImpl::consumer_gesture_provider_`
explicitly so that the notifications from gesture provider during
destruction are handled by `GestureRecognizerImpl` properly.

Bug: 1325256
Change-Id: Iba3b645fc2ad18331947e5556015567a1e8eb513
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3648376
Commit-Queue: Andrew Xu <andrewxu@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1008393}

[modify] https://crrev.com/bf900c8c6744773f5a7031482d28c50c9d115a61/ui/aura/gestures/gesture_recognizer_unittest.cc
[modify] https://crrev.com/bf900c8c6744773f5a7031482d28c50c9d115a61/ui/events/gestures/gesture_recognizer_impl.h
[modify] https://crrev.com/bf900c8c6744773f5a7031482d28c50c9d115a61/ui/events/gestures/gesture_recognizer_impl.cc


### jo...@chromium.org (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations, Piotr! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

This issue in ash did not receive a severity from Chrome OS sheriffing. The fix for this issue will be included in tomorrow's release, so in the interest of time assigning this Medium severity. While it is a browser UAF, it is mitigated by requiring user gesture, is not remote exploitable, and there is a very narrow exploitability, providing minimal attacker control. If anyone from Chrome OS security would like to change this and how it is reflected in tomorrow's security fix notes, please do so at soonest. Thank you! 

### am...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

[Monorail components: UI>Input]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-02)

@rzanoni please evaluate for LTC-102

### rz...@google.com (2022-08-04)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-05)

1. Just https://crrev.com/c/3810496
2. Minor conflicts with one missing method
3. Merged to main on aug 04
4. Yes

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. just https://crrev.com/c/3816906
2. Low, no conflicts
3. Merged to main on aug 04
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/674b8ddeeff955b097549b7487f0bcd7f4cc183c

commit 674b8ddeeff955b097549b7487f0bcd7f4cc183c
Author: Andrew Xu <andrewxu@chromium.org>
Date: Tue Sep 13 12:16:58 2022

[M102-LTS][ui] Handle notifications sent by gesture provider during destruction

This CL clears `GestureRecognizerImpl::consumer_gesture_provider_`
explicitly so that the notifications from gesture provider during
destruction are handled by `GestureRecognizerImpl` properly.

(cherry picked from commit bf900c8c6744773f5a7031482d28c50c9d115a61)

Bug: 1325256
Change-Id: Iba3b645fc2ad18331947e5556015567a1e8eb513
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3648376
Commit-Queue: Andrew Xu <andrewxu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1008393}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816906
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1348}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/674b8ddeeff955b097549b7487f0bcd7f4cc183c/ui/aura/gestures/gesture_recognizer_unittest.cc
[modify] https://crrev.com/674b8ddeeff955b097549b7487f0bcd7f4cc183c/ui/events/gestures/gesture_recognizer_impl.h
[modify] https://crrev.com/674b8ddeeff955b097549b7487f0bcd7f4cc183c/ui/events/gestures/gesture_recognizer_impl.cc


### rz...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1325256?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Input, UI>Input, UI>Shell>TabletMode]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059659)*
