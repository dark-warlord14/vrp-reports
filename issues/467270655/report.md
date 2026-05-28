# V8 SBX bypass: Perfetto Heap-Buffer-Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [467270655](https://issues.chromium.org/issues/467270655) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** |  V8 version 14.5.0 (candidate) |
| **Reporter** | am...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2025-12-09 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. code analysis

# Problem Description

HI Team, While doing code analysis found **PerfettoV8String::PerfettoV8String** in tracing-category-observer.cc is vulnerable for Heap Buffer Overflow

```
PerfettoV8String::PerfettoV8String(Tagged<String> string)
    : is_one_byte_(string->IsOneByteRepresentation()), size_(0) {
  if (string->length() <= 0) {
    return;
  }
  size_ = static_cast<size_t>(string->length()) *
          (string->IsOneByteRepresentation() ? sizeof(uint8_t)
                                             : sizeof(base::uc16));    <----- length is obtained from v8 heap
  buffer_.reset(new uint8_t[size_]);
  if (is_one_byte_) {
    String::WriteToFlat(string, buffer_.get(), 0, string->length()); <--- again length is obtained from v8 heap
  } else {
    String::WriteToFlat(string, reinterpret_cast<base::uc16*>(buffer_.get()), 0,
                        string->length());
  }
}

```

in the above code length is obtained from v8 heap and buffer is created with size \* some calculation assume buffer[10] is created, later we corrupt the length using SBX API to set length to 100 making the write post allocated location Resulting in Heap BOF

My another Issue of same double fetch type Ref: <https://issues.chromium.org/issues/467177779>

Note: in this issue i wasnt able to reach this area since it requires many flag and still im surfing on this, but as per code this is vulnerable, so raised it

In Build gn args: v8\_use\_perfetto = true is mandatory
in d8 running arg: --perfetto-code-logger --enable-tracing is mandatory

This will invoke the perfetto initialize in d8 main code but below code in **perfetto-logger.cc** didnt add the listener, in all the case the num\_active\_data\_sources\_ is 0

```
 void Register(Isolate* isolate) {
    auto logger = std::make_unique<PerfettoLogger>(isolate);
    base::MutexGuard lock(&mutex_);
    if (num_active_data_sources_ != 0) {
      isolate->logger()->AddListener(logger.get());
    }
    CHECK(isolates_.emplace(isolate, std::move(logger)).second);
  }

```

num\_active\_data\_sources\_ is incremented on same file

```
  void OnCodeDataSourceStart() {
    base::MutexGuard lock(&mutex_);
    ++num_active_data_sources_;
    if (num_active_data_sources_ == 1) {
      StartLogging(lock);
    }
    LogExistingCodeForAllIsolates(lock);
  }

```

This will be invoked from in code-data-source.cc

```
void CodeDataSource::OnStart(const StartArgs&) {
  PerfettoLogger::OnCodeDataSourceStart();
}

```

These are my current traces and im trying to enable the perfetto properly to trigger this path.

My d8 args: --allow-natives-syntax --enable-tracing --perfetto-code-logger --log-code --fuzzing --sandbox-fuzzing --single-threaded --expose-gc poc.js

Kindly share details on where it was missed to initialize the onstart method in perfetto, where it is missed in the flow (experts need your inputs)

Note: once i reached the path in **PerfettoV8String::PerfettoV8String** i will try to share working POC

**Currently the exploit is possible similar to my attached issue reference: <https://issues.chromium.org/issues/467177779>**

# Summary

V8 SBX bypass: Perfetto Heap-Buffer-Overflow

# Custom Questions

#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [perfetto_heap_bof_fix.diff](attachments/perfetto_heap_bof_fix.diff) (text/x-diff, 950 B)

## Timeline

### am...@gmail.com (2025-12-09)

Bisection Details
Commit Link: https://chromium.googlesource.com/v8/v8/+/471aeba455c35f456ffb270fd44dc549896d6744%5E%21/src/tracing/perfetto-utils.cc
Commit ID: 471aeba455c35f456ffb270fd44dc549896d6744

Introduced On: Feb 19 2024

### am...@gmail.com (2025-12-09)

Team, Any leads to reach the PerfettoV8String method? seems the issue was in listener addition, not working in my v8 seems it is common issue, Did i miss any flags to achieve this

carlscab@google.com Author based on commit, Waiting to know from your end

### li...@chromium.org (2025-12-09)

Thanks for the report. @ca...@google.com is no longer at Google, unfortunately.

Tentatively reassigning to @md...@google.com for V8 triage. This issue does not have a POC and hence isn't reproducible, but the code analysis seems reasonable.

### md...@google.com (2025-12-10)

Assigning to Igor as an owner of V8 sandbox violations

### ch...@google.com (2025-12-11)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-12-15)

The NextAction date has arrived: 2025-12-15
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### am...@gmail.com (2025-12-18)

**Fix Patch Attached**

### pe...@google.com (2025-12-18)

Thank you for providing more feedback. Adding the requester to the CC list.

### is...@chromium.org (2025-12-19)

Thank you for the report!

`v8_use_perfetto` is enabled for Chrome, but I'm still not sure how severe/exploitable it is given that it requires from user to start profiling of a harmful web site.

### sa...@google.com (2025-12-19)

Yeah given that this requires non-default flags (the user must enable perf tracing from what I understand) it's definitely not an S1. I guess we can leave it as type-vuln though.

### am...@gmail.com (2025-12-19)

Thanks for the update team, Can i submit the above patch through gerrit? also kindly let me know whom should i assign for reviewer in gerrit

### is...@chromium.org (2025-12-19)

Please don't. There's a bit more correct version here: <https://crrev.com/c/7276998>.

### am...@gmail.com (2025-12-19)

Yeah i have seen there is an is_one_byte was changed in the above fix, Others are already included in my previously uploaded fix 

kindly confirm whether the patch bonus will be eligible. since my patch includes almost changes

### am...@gmail.com (2026-01-07)

Team seems the CL have missing code-owners block to satisfy the CV Run, Kindly check on the CL

### ch...@google.com (2026-01-07)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### dx...@google.com (2026-01-12)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7276998>

[tracing] Fix double length read in PerfettoV8String

---


Expand for full commit details
```
     
    Fixed: 467270655 
    Change-Id: I183169c91ab397ad2acfb2ae8c589398dbb89582 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7276998 
    Reviewed-by: Samuel Groß <saelo@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104647}

```

---

Files:

- M `src/tracing/perfetto-utils.cc`

---

Hash: [e269a617e8804c1bb6dfe6e00b78222bcbedbd96](https://chromiumdash.appspot.com/commit/e269a617e8804c1bb6dfe6e00b78222bcbedbd96)  

Date: Fri Dec 19 15:41:09 2025


---

### am...@gmail.com (2026-01-30)

Team kindly share the bounty update

### sp...@google.com (2026-01-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Highly Mitigated Memory corruption in a sandboxed process + bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467270655)*
