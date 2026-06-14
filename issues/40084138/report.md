# Crash in v8::internal::Invoke

| Field | Value |
|-------|-------|
| **Issue ID** | [40084138](https://issues.chromium.org/issues/40084138) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | rm...@chromium.org |
| **Created** | 2016-04-21 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5948163801743360

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7ffff8635f58
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Recommended Security Severity: High

Regressed: V8: r35617:35618

Minimized Testcase (10.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96xyORxODQO9Cr0M4BC-NRF7gutg_RqwZxMRzawZr-PHSpdmYFziqCp1TXYnPDSPcItIbEOsYIR0neRsAPE-DxDa_0KFVWF0WLgpv2aGdfnFw9r5iExoR-lFD6IviDPBl2KNGR7CuPB2fnxvbbFKBam6VWE-A

Filer: mstarzinger

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### ms...@chromium.org (2016-04-21)

Looks like it only affecting the interpreter (which is not yet shipping). Will triage now and drop security labels if limited to interpreter.

### ms...@chromium.org (2016-04-21)

This is interpreter only. Regression range points towards ...

https://chromium.googlesource.com/v8/v8/+/623ad7de882019dff10168ef53bd539f01ef5b93

Reproduces as follows ...

$ git checkout 2d454e226a085f32ee6182625c691e98ad8a84f9
$ make -j1000 ia32.debug
$ ./out/ia32.debug/d8 --ignition boom.js
$ cat boom.js

// Flags: --ignition

function function_with_n_params_and_m_args(n, m) {
  test_prefix = 'prefix ';
  test_suffix = ' suffix';
  var source = 'test_prefix + (function f(';
  for (var arg = 0; arg < n ; arg++) {
    if (arg != 0) source += ',';
    source += 'arg' + arg;
  }
  source += ') { return arg' + (n - n % 2) / 2 + '; })(';
  for (var arg = 0; arg < m ; arg++) {
    if (arg != 0) source += ',';
    source += arg;
  }
  source += ') + test_suffix';
  return eval(source);
}

function_with_n_params_and_m_args(-0x8001, 0x7FFF);

### ms...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### rm...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-21)

Applying Security_Impact-Head.
rmcilroy@: Please feel free to remove it if that's incorrect.

### rm...@chromium.org (2016-04-22)

This only impacts the interpreter which isn't shipping yet, so I don't think it has a security impact. In any case, I have a fix landing right now.

### aa...@google.com (2016-04-22)

If this functionality is planned to be shipped in near future and this bug helped to knock down that vulnerability, we should still consider it for reward. impact label can be maybe depending on the timeframe.

### sh...@chromium.org (2016-04-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-23)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-04-23)

ClusterFuzz has detected this issue as fixed in range 35718:35719.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5948163801743360

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7ffff8635f58
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Recommended Security Severity: High

Regressed: V8: r35617:35618
Fixed: V8: r35718:35719

Minimized Testcase (10.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96xyORxODQO9Cr0M4BC-NRF7gutg_RqwZxMRzawZr-PHSpdmYFziqCp1TXYnPDSPcItIbEOsYIR0neRsAPE-DxDa_0KFVWF0WLgpv2aGdfnFw9r5iExoR-lFD6IviDPBl2KNGR7CuPB2fnxvbbFKBam6VWE-A

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### rm...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-06)

$3,500 for this one!

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/605470?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084138)*
