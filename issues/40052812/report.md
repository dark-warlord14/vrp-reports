# Security: Insufficient data validation in deserialize TransformStream

| Field | Value |
|-------|-------|
| **Issue ID** | [40052812](https://issues.chromium.org/issues/40052812) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ju...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2020-07-10 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

---

```
case kTransformStreamTransferTag: {  
  if (!TransferableStreamsEnabled())  
    return nullptr;  
  uint32_t index = 0;  
  if (!ReadUint32(&index) || !transferred_stream_ports_ ||  
      index + 1 >= transferred_stream_ports_->size()) {  
    return nullptr;  
  }  
  ReadableStream\* readable = ReadableStream::Deserialize(  
      script_state_, (\*transferred_stream_ports_)[index].Get(),  
      exception_state);  
  if (!readable)  
    return nullptr;  

  WritableStream\* writable = WritableStream::Deserialize(  
      script_state_, (\*transferred_stream_ports_)[index + 1].Get(),  
      exception_state);  
  if (!writable)  
    return nullptr;  

  return MakeGarbageCollected<TransformStream>(readable, writable);  
}  

```

---

- [1] <https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_deserializer.cc;l=572-593;bpv=1;bpt=1>

kTransformStreamTransferTag only validate out-of-bound access, it should also check integer overflow to protect accessing the different readable stream.  

It can be using with bypassing site-isolation since we can send a serialized message via postMessage.

**VERSION**

navigator.userAgent == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

**REPRODUCTION CASE**

[PoC]

<html>
<head>
<?php
if ($\_GET['x'] == 1) { // app.imjuno.com
?>
<meta http-equiv="origin-trial" content="AhPJIdzCggLn5eyC5UyXR1T+zK/cyngs5obkhmVNihHRn/nQ8dZHYv/sO792DhhqdLYZbzBao1vu9JqyIYrt7AIAAABweyJvcmlnaW4iOiJodHRwczovL3Rlc3Rkb21haW4uanVubzo0NDMiLCJmZWF0dXJlIjoiUlRDSW5zZXJ0YWJsZVN0cmVhbXMiLCJleHBpcnkiOjE1OTc5OTc1ODIsImlzU3ViZG9tYWluIjp0cnVlfQ==">
<?php
} else { // testdomain.juno (different process)
?>
<meta http-equiv="origin-trial" content="Auaakp264bS0a1jJ9m6KFG4DTeuwl3Bvgw8+ZiIf6LKlcs2VyBbcyPM/m4ihnwqW+Jj7lFuyI3g0bJe4mGtDcgoAAABceyJvcmlnaW4iOiJodHRwczovL2FwcC5pbWp1bm8uY29tOjQ0MyIsImZlYXR1cmUiOiJSVENJbnNlcnRhYmxlU3RyZWFtcyIsImV4cGlyeSI6MTU5Nzk5MDExNH0=">
<?php
}
?>
```
</head>  
<body>  
<script>  

```

if (location.search.length > 1) // testdomain.juno (different process)  

window.onmessage = function() { console.log('yeah', arguments[0].data) }  

else { // app.imjuno.com  

var orig = new TransformStream();  

var other = new TransformStream()  

var target = window.open('<https://testdomain.juno/m/a.php?x=1>');  

setTimeout(function() { console.log(1234); target.postMessage(orig, '\*', [orig]); }, 1000);  

}  

</script>  

</body>

</html>

index must be changed to UINT\_MAX (0xffffffff) with debugger (or code execution via renderer RCE).

Below is a possible patch. (return nullptr if read index is kNotFound (-1))

```
  if (!ReadUint32(&index) || index == kNotFound || !transferred_stream_ports_ ||  
      index + 1 >= transferred_stream_ports_->size()) {  
    return nullptr;  
  }

```

## Timeline

### cl...@chromium.org (2020-07-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5630508043665408.

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5660710662635520.

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5763595322851328.

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5630794934059008.

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5715093934899200.

### cl...@chromium.org (2020-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5632154968588288.

### cl...@chromium.org (2020-07-11)

Testcase 5763595322851328 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5763595322851328.

### mm...@google.com (2020-07-14)

Thanks for your report. I wasn't able to reproduce it while serving your testcase with PHP. Could you please provide a clearer instruction on how to reproduce this?

Since my sheriffing rotation is ending today, I'm triaging this issue assuming it's reproducible.

[Monorail components: Blink>JavaScript]

### ri...@chromium.org (2020-07-14)

Thanks for the excellent find. I am working on a fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/da59cd312493cdf2069c8b7c8cf5be5fe9c7309f

commit da59cd312493cdf2069c8b7c8cf5be5fe9c7309f
Author: Adam Rice <ricea@chromium.org>
Date: Tue Jul 14 13:06:06 2020

TransformStream deserialize: perform additional validation

The TransformStream deserialization code did not check for a message
port index of 0xffffffff. Add a check for it.

Also add a unit test for this condition.

BUG=1104103

Change-Id: Ic04af9d7a27171c471c0125662ee68dccb88abb4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2296549
Commit-Queue: Adam Rice <ricea@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#788128}

[modify] https://crrev.com/da59cd312493cdf2069c8b7c8cf5be5fe9c7309f/third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_deserializer.cc
[modify] https://crrev.com/da59cd312493cdf2069c8b7c8cf5be5fe9c7309f/third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_serializer_test.cc


### [Deleted User] (2020-07-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2020-07-14)

#10 fixes the issue. I think we probably don't need to merge to M85 because this is only available behind an origin trial but +srinivassista for a second opinion.

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### sr...@google.com (2020-07-15)

+adetaylor@  Please check if we can wait for this to go out in M86 as the issue happens in origin trial only

### ad...@chromium.org (2020-07-15)

Marking as Fixed per https://crbug.com/chromium/1104103#c12. If it's behind an origin trial I'm happy waiting for M86.

### ri...@chromium.org (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-30)

Congratulations! The VRP panel has decided to award $7,500 for this report.

### ad...@google.com (2020-07-30)

junorouse@gmail.com - how would you like to be credited in the Chrome release notes?

(A member of our finance team will get in touch with you to arrange payment.)

### ad...@google.com (2020-07-30)

[Empty comment from Monorail migration]

### ju...@gmail.com (2020-08-01)

Juno Im (junorouse) of Theori is fine. Thanks :D


### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1104103?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052812)*
