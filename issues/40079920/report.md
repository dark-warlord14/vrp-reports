# Use-of-uninitialized-value in WebCore::BiquadDSPKernel::updateCoefficientsIfNecessary

| Field | Value |
|-------|-------|
| **Issue ID** | [40079920](https://issues.chromium.org/issues/40079920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | rt...@chromium.org |
| **Created** | 2014-06-26 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4686250902552576

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  WebCore::BiquadDSPKernel::updateCoefficientsIfNecessary
  WebCore::BiquadDSPKernel::getFrequencyResponse
  WebCore::BiquadProcessor::getFrequencyResponse
  

Minimized Testcase (1.83 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95U80z6MrWK6ndvvHB1TDunZW6-TqpTAUEoIpKL7AABpfeR5sRN_6uV4ielUFZzY1PXnnQ2F7WVJVXx0q1-Ik5E0mlQbW2EwXxvCpLQfRt3awXUBYqSfUpZ8TYR9I3peDiHoY9d--H2SZhuMWRfyNzg31MAEw
Filer: inferno@chromium.org

## Timeline

### in...@chromium.org (2014-06-26)

If !isGood, value in finalValue() never gets initialized.

float AudioParam::finalValue()
{
    float value;
    calculateFinalValues(&value, 1, false);
    return value;
}

void AudioParam::calculateFinalValues(float* values, unsigned numberOfValues, bool sampleAccurate)
{
    bool isGood = context() && context()->isAudioThread() && values && numberOfValues;
    ASSERT(isGood);
    if (!isGood)
        return;

### rt...@chromium.org (2014-06-26)

This fails because context()->isAudioThread is false.  Need to investigate why getFrequencyResponse is calling this function.

### in...@chromium.org (2014-06-26)

I understand that context()->isAudioThread might be the real functional bug, but to prevent this from happening in future, please also initialize float value to some default.

### cl...@chromium.org (2014-06-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-30)

[Comment Deleted]

### rs...@chromium.org (2014-06-30)

Did a CL land for this, or is ClusterFuzz mistaken?

### rt...@chromium.org (2014-06-30)

I think it's a clusterfuzz mistake. I do have a CL in the CQ for this: https://codereview.chromium.org/354213002/

### bu...@chromium.org (2014-06-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=177250

------------------------------------------------------------------
r177250 | rtoy@chromium.org | 2014-06-30T23:29:01.905735Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/BiquadDSPKernel.cpp?r1=177250&r2=177249&pathrev=177250
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioParam.cpp?r1=177250&r2=177249&pathrev=177250
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/BiquadDSPKernel.h?r1=177250&r2=177249&pathrev=177250

Initialize value since calculateFinalValues may fail to do so.

Fix threading issue where updateCoefficientsIfNecessary was not always
called from the audio thread. This causes the value not to be
initialized.

Thus,

o Initialize the variable to some value, just in case.
o Split updateCoefficientsIfNecessary into two functions with the code
  that sets the coefficients pulled out in to the new function
  updateCoefficients.
o Simplify updateCoefficientsIfNecessary since useSmoothing was always
  true, and forceUpdate is not longer needed.
o Add process lock to prevent the audio thread from updating the
  coefficients while they are being read in the main thread. The audio
  thread will update them the next time around.
o Make getFrequencyResponse set the lock while reading the
  coefficients of the biquad in preparation for computing the
  frequency response.

BUG=389219

Review URL: https://codereview.chromium.org/354213002
-----------------------------------------------------------------

### in...@chromium.org (2014-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-07-07)

[Comment Deleted]

### ti...@chromium.org (2014-07-07)

amineer@ - Merge-Requested for M37 (branch 2062).

### am...@chromium.org (2014-07-14)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-07-14)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=178109

------------------------------------------------------------------
r178109 | rtoy@google.com | 2014-07-14T23:14:53.340854Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/modules/webaudio/AudioParam.cpp?r1=178109&r2=178108&pathrev=178109
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/modules/webaudio/BiquadDSPKernel.h?r1=178109&r2=178108&pathrev=178109
   M http://src.chromium.org/viewvc/blink/branches/chromium/2062/Source/modules/webaudio/BiquadDSPKernel.cpp?r1=178109&r2=178108&pathrev=178109

Merge 177250 "Initialize value since calculateFinalValues may fa..."

> Initialize value since calculateFinalValues may fail to do so.
> 
> Fix threading issue where updateCoefficientsIfNecessary was not always
> called from the audio thread. This causes the value not to be
> initialized.
> 
> Thus,
> 
> o Initialize the variable to some value, just in case.
> o Split updateCoefficientsIfNecessary into two functions with the code
>   that sets the coefficients pulled out in to the new function
>   updateCoefficients.
> o Simplify updateCoefficientsIfNecessary since useSmoothing was always
>   true, and forceUpdate is not longer needed.
> o Add process lock to prevent the audio thread from updating the
>   coefficients while they are being read in the main thread. The audio
>   thread will update them the next time around.
> o Make getFrequencyResponse set the lock while reading the
>   coefficients of the biquad in preparation for computing the
>   frequency response.
> 
> BUG=389219
> 
> Review URL: https://codereview.chromium.org/354213002

TBR=rtoy@chromium.org

Review URL: https://codereview.chromium.org/390003006
-----------------------------------------------------------------

### in...@chromium.org (2014-07-24)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-28)

Thanks again for the fuzzer contribution! This report qualifies for a $500 reward.

### ti...@chromium.org (2014-09-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-07)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-10-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/389219?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079920)*
