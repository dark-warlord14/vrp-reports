# Security: Debug check failed: s->IsFlat().

| Field | Value |
|-------|-------|
| **Issue ID** | [40061773](https://issues.chromium.org/issues/40061773) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Internationalization, Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | re...@gmail.com |
| **Assignee** | ft...@chromium.org |
| **Created** | 2022-11-16 |
| **Bounty** | $7,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

The arguements can be controled by user, so it will break the assumption in LocaleConvertCase.

```
MaybeHandle<String> LocaleConvertCase(Isolate\* isolate, Handle<String> s,  
                                      bool is_to_upper, const char\* lang) {  
  auto case_converter = is_to_upper ? u_strToUpper : u_strToLower;  
  int32_t src_length = s->length();  
  int32_t dest_length = src_length;  
  UErrorCode status;  
  Handle<SeqTwoByteString> result;  
  std::unique_ptr<base::uc16[]> sap;  
  
  if (dest_length == 0) return ReadOnlyRoots(isolate).empty_string_handle();  
  
  // This is not a real loop. It'll be executed only once (no overflow) or  
  // twice (overflow).  
  for (int i = 0; i < 2; ++i) {  
    // Case conversion can increase the string length (e.g. sharp-S => SS) so  
    // that we have to handle RangeError exceptions here.  
    ASSIGN_RETURN_ON_EXCEPTION(  
        isolate, result, isolate->factory()->NewRawTwoByteString(dest_length),  
        String);  
    DisallowGarbageCollection no_gc;  
    CHECK(s->IsFlat());  
    String::FlatContent flat = s->GetFlatContent(no_gc);  
    const UChar\* src = GetUCharBufferFromFlat(flat, &sap, src_length);  
    status = U_ZERO_ERROR;  
    dest_length =  
        case_converter(reinterpret_cast<UChar\*>(result->GetChars(no_gc)),  
                       dest_length, src, src_length, lang, &status);  
    if (status != U_BUFFER_OVERFLOW_ERROR) break;  
  }  
  

```

And then when GetUCharBufferFromFlat, it may lead to type confusion because it thinks the flat is TWO\_BYTE or ONE\_BYTE

```
  
const UChar\* GetUCharBufferFromFlat(const String::FlatContent& flat,  
                                    std::unique_ptr<base::uc16[]>\* dest,  
                                    int32_t length) {  
  DCHECK(flat.IsFlat());  
[\*]  if (flat.IsOneByte()) {  
    if (!\*dest) {  
      dest->reset(NewArray<base::uc16>(length));  
      CopyChars(dest->get(), flat.ToOneByteVector().begin(), length);  
    }  
    return reinterpret_cast<const UChar\*>(dest->get());  
  } else {  
    return reinterpret_cast<const UChar\*>(flat.ToUC16Vector().begin());  
  }  
}  

```
```
    base::Vector<const base::uc16> ToUC16Vector() const {  
      DCHECK_EQ(TWO_BYTE, state_);  
    []  return base::Vector<const base::uc16>(twobyte_start, length_);  
    }  

```

**VERSION**  

Chrome Version: v8 commit de96cb1552438e067f8727ac5f263fa5d649da4b  

Operating System: ALL Operating System

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

Run poc.js in d8 with "--allow-natives-syntax --harmony\_temporal".

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

// Stderr:  

// #  

// # Fatal error in ../../src/objects/intl-objects.cc, line 262  

// # Debug check failed: s->IsFlat().  

// #  

// #  

// #  

// #FailureMessage Object: 0x7ffccb66ef40Received signal 6

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 852 B)

## Timeline

### [Deleted User] (2022-11-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4890813000777728.

### cl...@chromium.org (2022-11-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-16)

Detailed Report: https://clusterfuzz.com/testcase?key=4890813000777728

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  s->IsFlat() in intl-objects.cc
  v8::internal::LocaleConvertCase
  v8::internal::Intl::ConvertToLower
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84072:84073

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4890813000777728

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### is...@chromium.org (2022-11-16)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Internationalization]

### dr...@chromium.org (2022-11-16)

[security sheriff] ishell@ or ftang@ - can you comment on the severity of this bug? I don't know this implications of this DCHECK. Should we assume it leads to RCE?

### is...@chromium.org (2022-11-17)

[Comment Deleted]

### is...@chromium.org (2022-11-17)

It's not a security issue yet because we are not shipping the Temporal feature, that's why --harmony_temporal flag is required to trigger the issue.

### re...@gmail.com (2022-11-17)

[Comment Deleted]

### am...@chromium.org (2022-11-17)

@saelo, can PTAL and adjust severity to this. Since it's a DCHECK failure, I'm going to conservatively set it at High for now. 
Setting at SI-None as that is the appropriate for issue in code behind flags/in features not yet enabled. 

### sa...@chromium.org (2022-11-17)

To me it looks like nothing bad will actually happen since String::GetFlatContent will handle non-flat strings as well from what I can tell [1], but I haven't looked at this in detail, maybe ftang@ can confirm, but otherwise I'd just conservatively leave it at High for now since its already marked as Security_Impact-None.

[1] https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/string.cc;l=792;drc=b75fd5075a90ada27a3360df23fa08c83e24e995;bpv=1;bpt=1 will 

### [Deleted User] (2022-11-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-21)

[Empty comment from Monorail migration]

### ft...@chromium.org (2022-11-22)

no risk at this point because we have not turn on harmony_temporal yet. Temporal is still under development and not shipped yet. 

### ft...@chromium.org (2022-11-22)

We probably should add
  id = String::Flatten(isolate, id);
before calling "id = Intl::ConvertToLower(isolate, id)" in js-temporal-objects.cc

but be aware the "new Temporal.Calendar(o4);" is not a code which shipped yet. There are no security risk at this point.

### ft...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2022-11-29)

https://chromium-review.googlesource.com/c/v8/v8/+/4062685

### [Deleted User] (2022-11-29)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

### ft...@chromium.org (2022-11-30)

we have not flip the bit for temporal yet, it won't be hit by the users

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/140bebbba7ba7906baeeb7a19bd1cc0a271d2fb7

commit 140bebbba7ba7906baeeb7a19bd1cc0a271d2fb7
Author: Frank Tang <ftang@chromium.org>
Date: Tue Nov 29 06:28:19 2022

[Intl] Fix IsFlat assertion

Add String::Flatten() before calling Intl::ConvertToLower

Bug: chromium:1385368
Change-Id: I28c282cd7ea27e2686d6eb68de074013fe335157
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4062685
Commit-Queue: Frank Tang <ftang@chromium.org>
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84561}

[add] https://crrev.com/140bebbba7ba7906baeeb7a19bd1cc0a271d2fb7/test/mjsunit/regress/regress-1385368.js
[modify] https://crrev.com/140bebbba7ba7906baeeb7a19bd1cc0a271d2fb7/src/objects/js-temporal-objects.cc


### cl...@chromium.org (2022-11-30)

ClusterFuzz testcase 4890813000777728 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84560:84561

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-05)

It appears that the security severity label was removed only because this issue is in a feature not yet enabled. The correct course of action and labeling for this issue adding the Security_Impact-None label (and removing any other SI labels applied based on a FoundIn- label). This will appease the bot and allow for the removal of the RBS label. I've re-added the severity label accordingly. 
If this issue is particular DCHECK failure does not result in security consequences, please removed all security labels and convert to type=Bug. Thank you! 

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-15)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you to arrange payment. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-08)

This issue was migrated from crbug.com/chromium/1385368?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Internationalization, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061773)*
