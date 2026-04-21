# heap-use-after-free dawn\src\dawn\native\Device.cpp:285 in dawn::native::DeviceBase::DeviceLostEvent::Complete

| Field | Value |
|-------|-------|
| **Issue ID** | [354748063](https://issues.chromium.org/issues/354748063) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Dawn>Native |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | lo...@google.com |
| **Created** | 2024-07-23 |
| **Bounty** | $2,000.00 |

## Description

#REPRODUCTION CASE
This is a difficult-to-reproduce issue caused by conditional race conditions. I have provided the ASAN logs recorded by the FUZZER at the time and a root cause analysis report.

#BISECT
<https://dawn-review.googlesource.com/c/dawn/+/165527>

#RCA

1. DeviceBase is a reference-counted singleton object.
2. According to the ASAN logs, threads T0 and T34 both called DeviceBase::HandleError function.
3. T0 and T34 passed the conditional check mLostEvent != nullptr at position [0] simultaneously.
4. T0 reached position [1], causing mLostEvent to be released, but T34 had already proceeded to position [2], resulting in a Use-After-Free (UAF) issue.

```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/dawn/native/Device.cpp;drc=a72186c5de7a11109a88c45bbe1fe6d84e8baf00;l=280
void DeviceBase::HandleError(std::unique_ptr<ErrorData> error,
                             InternalErrorType additionalAllowedErrors,
                             WGPUDeviceLostReason lostReason) {
    AppendDebugLayerMessages(error.get());
...CUT...

    const std::string messageStr = error->GetFormattedMessage();
    if (type == InternalErrorType::DeviceLost) {
        // The device was lost, schedule the application callback's execution.
        // Note: we don't invoke the callbacks directly here because it could cause re-entrances ->
        // possible deadlock.
        if (mLostEvent != nullptr) {												<< [0]
            mLostEvent->mReason = FromAPI(lostReason);
            mLostEvent->mMessage = messageStr;
            GetInstance()->GetEventManager()->SetFutureReady(mLostEvent.Get());		<< [2]
            mLostEvent = nullptr;													<< [1]
        }

        mQueue->HandleDeviceLoss();

```

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 19.1 KB)

## Timeline

### am...@chromium.org (2024-07-24)

Thank you for the report. We understand this was discovered by your fuzzer, but if there's any sort of reproducer or testcase you can provide, that may be needed given that GPU related issues are often hard to diagnose and test.
That being said based on the stack trace, getting it over the the appropriate folks to start investigating this issue.
Setting at moderate severity based on the difficult to reproduce this issue and the race condition.
This can and may be adjusted based on investigation into this issue and if more information can be provided.

### pe...@google.com (2024-07-24)

Setting milestone because of s2 severity.

### pe...@google.com (2024-08-10)

lokokung: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-08-25)

lokokung: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-08-29)

Project: dawn
Branch: main

commit 0b1bba3f287e6228c13b90eaebba9e57f7d6f883
Author: Lokbondo Kung <lokokung@google.com>
Date:   Thu Aug 29 17:44:56 2024

    [dawn][native] Make sure to hold Device lock before handling errors.
    
    - Briefly, the bug we saw was a result of errors being generated in
      the Device during a ProcessEvent call which was not taking the
      appropriate Device lock. With the minimal change in PS1 by
      acquiring the lock, it exposed an existing issue where we could
      have lock acquiring inversion between the mEvents lock in the
      EventManager and the device lock. To fix this, we needed to
      release the mEvents lock in ProcessEvents before calling into
      the code that needs the device lock. Once that was fixed, we
      the tests were failing because ProcessEvents is no longer a fully
      "atomic" operation and the WaitRefs asserts were being triggered.
      To fix that, we removed the WaitRef entirely since it was more
      restrictive than the desired behavior.
    
    Bug: 354748063
    Change-Id: I586b3acdb8801ddd9d4b2b57da7824e37e23e595
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/204154
    Reviewed-by: Corentin Wallez <cwallez@chromium.org>
    Reviewed-by: Kai Ninomiya <kainino@chromium.org>
    Commit-Queue: Loko Kung <lokokung@google.com>

M       src/dawn/native/EventManager.cpp

https://dawn-review.googlesource.com/204154


### ap...@google.com (2024-08-29)

Project: chromium/src
Branch: main

commit 665d80856f8937ff6a2e481f97c8ba77c2a13d0b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Aug 29 22:16:07 2024

    Roll Dawn from 363eae1e5d18 to f5804298ecff (5 revisions)
    
    https://dawn.googlesource.com/dawn.git/+log/363eae1e5d18..f5804298ecff
    
    2024-08-29 senorblanco@chromium.org Compat CTS: add some flakes from the Pixel 6 bot.
    2024-08-29 bsheedy@google.com Sync expectation file tag headers
    2024-08-29 amaiorano@google.com infra/gn: add Mac 14 bots
    2024-08-29 lokokung@google.com [dawn][native] Make sure to hold Device lock before handling errors.
    2024-08-29 dsinclair@chromium.org Remove old test.
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/dawn-chromium-autoroll
    Please CC cwallez@google.com,shrekshao@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Dawn: https://bugs.chromium.org/p/dawn/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:dawn-android-arm-deps-rel;luci.chromium.try:dawn-android-arm64-deps-rel;luci.chromium.try:dawn-linux-x64-deps-rel;luci.chromium.try:dawn-mac-x64-deps-rel;luci.chromium.try:dawn-mac-arm64-deps-rel;luci.chromium.try:dawn-win10-x64-deps-rel;luci.chromium.try:dawn-win10-x86-deps-rel;luci.chromium.try:dawn-win11-arm64-deps-rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64
    Bug: chromium:346808585,chromium:354748063
    Tbr: shrekshao@google.com
    Include-Ci-Only-Tests: true
    Change-Id: I0da6107a8cecb52b86bbc1d474c99882a23f5c79
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5827385
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1348910}

M       DEPS
M       third_party/dawn

https://chromium-review.googlesource.com/5827385


### sp...@google.com (2024-09-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
moderately mitigated memory corruption in a highly privileged process (GPU), lacking a POC / demonstrable information


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-13)

Congratulations! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-12-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> moderately mitigated memory corruption in a highly privileged process (GPU), lacking a POC / demonstrable information

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/354748063)*
