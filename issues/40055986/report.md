# Security: libxml CVE-2021-3541

| Field | Value |
|-------|-------|
| **Issue ID** | [40055986](https://issues.chromium.org/issues/40055986) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>XML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-3541 |
| **Reporter** | se...@pipping.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-05-24 |
| **Bounty** | Confirmed (amount unknown) |

## Description

CVE-2021-3541 "Parameter Laughs" fixed in libxml2 2.9.11

https://blog.hartwork.org/posts/cve-2021-3541-parameter-laughs-fixed-in-libxml2-2-9-11/

Maybe this fix will be absorbed by the work in https://crbug.com/chromium/1211314 anyway (https://chromium.googlesource.com/chromium/src/+/b0a66f930c41a1c5e8307c0f7996adc02ccd3cbd) but I can't see the linked libxml2 https://crbug.com/chromium/228, so I am not sure.

## Timeline

### ja...@chromium.org (2021-05-24)

I'll roll it in very soon

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-05-24)

https://chromium-review.googlesource.com/c/chromium/src/+/2915101

### gi...@appspot.gserviceaccount.com (2021-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/acd34896d98b09a96a5d61a86dc4baca08acd3ba

commit acd34896d98b09a96a5d61a86dc4baca08acd3ba
Author: Joey Arhar <jarhar@chromium.org>
Date: Tue May 25 14:27:54 2021

Roll libxml from bfd2f430 to a46e85f6

2021-05-22 rickert@fortiss.org Update CMake project version
2021-05-22 rickert@fortiss.org Add CMake alias targets for embedded projects
2021-05-18 dking@redhat.com Fix some validation errors in the FAQ
2021-05-19 dking@redhat.com Remove unused variable in xmlCharEncOutFunc
2021-05-16 rickert@fortiss.org Add missing file xmlwin32version.h.in to EXTRA_DIST
2021-05-16 rickert@fortiss.org Add instructions on how to use CMake to compile libxml
2021-05-18 wellnhofer@aevum.de Work around lxml API abuse
2021-05-20 mike.dalessio@gmail.com fix: avoid segfault at exit when using custom memory functions
2021-05-13 veillard@redhat.com Release of libxml2-2.9.12
2021-05-13 veillard@redhat.com Release of libxml2-2.9.11
2021-05-13 veillard@redhat.com Patch for security issue CVE-2021-3541

Fixed: 1212694
Bug: 934413
Change-Id: I696f8c50cba19b47eb5cfd58ecbda3f6b4273868
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915101
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Joey Arhar <jarhar@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886279}

[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/README.chromium
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/linux/config.h
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/linux/include/libxml/xmlversion.h
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/linux/xml2-config
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/mac/config.h
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/mac/include/libxml/xmlversion.h
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/CMakeLists.txt
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/HTMLtree.c
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/configure.ac
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/encoding.c
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/Makefile.am
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/Makefile.in
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/fuzz.h
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-11
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-12
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-13
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/branch-9
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-11
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-12
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-13
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-14
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-15
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-16
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug316338-9
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/bug420596-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/content-9
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/hard-9
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ncname-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ncname-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ncname-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ncname-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ncname-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-11
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-12
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges-9
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-11
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-12
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/ranges2-9
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-1
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-10
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-11
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-12
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-13
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-14
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-15
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-16
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-17
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-18
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-19
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-2
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-20
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-21
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-22
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-23
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-24
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-25
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-26
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-27
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-28
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-29
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-3
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-30
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-31
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-32
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-33
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-34
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-35
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-4
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-5
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-6
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-7
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-8
[add] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/fuzz/seed/regexp/xpath-9
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/include/libxml/Makefile.am
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/libxml2.spec
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/parser.c
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/testapi.c
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/src/xmlsave.c
[modify] https://crrev.com/acd34896d98b09a96a5d61a86dc4baca08acd3ba/third_party/libxml/win32/include/libxml/xmlversion.h


### [Deleted User] (2021-05-25)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-05-26)

From https://blog.hartwork.org/posts/cve-2021-3541-parameter-laughs-fixed-in-libxml2-2-9-11/

> Parameter Laughs is "only" a denial of service attack

jarhar@ -- can you confirm that assessment?

If so, then per https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/faq.md#Are-denial-of-service-issues-considered-security-bugs, this isn't a security issue.

### ja...@chromium.org (2021-05-26)

I agree, I believe this isn't a security issue. I'd imagine that it would be just as easy to exhaust resources with some javascript.

### ad...@google.com (2021-05-26)

Yep. We in Chrome don't consider this a security issue. Other clients of libxml might do so, which is why it has a CVE number. Unless anyone really objects, I'd like to keep this in the security queue with severity low, just because we tend to track CVE numbers that way. No big deal if people want to track it as a non-security bug.

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### ja...@chromium.org (2021-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-05)

The VRP Panel has decided to award $500 for reporting this issue and https://crbug.com/chromium/1212733. We appreciate you bringing this to our attention! Reward amount was updated on https://crbug.com/chromium/1212733. A member of our finance team will be in touch soon to arrange payment. 

### [Deleted User] (2021-09-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

considering the roll in https://crbug.com/chromium/1212694#c7 to be the final fix

### pg...@google.com (2023-01-18)

removing relnotes_update_needed since this bug is tracking the roll of an already fixed issue

### is...@google.com (2023-01-18)

This issue was migrated from crbug.com/chromium/1212694?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1228671]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055986)*
