# heap-use-after-free in Tint SPIR-V parser

| Field | Value |
|-------|-------|
| **Issue ID** | [440964231](https://issues.chromium.org/issues/440964231) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Dawn>Tint |
| **Reporter** | vu...@darknavy.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2025-08-25 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# VULNERABILITY DETAILS

When calling `tint::spirv::reader::ReadIR` to load malicious SPIR-V code and parse it into IR, a UAF vulnerability occurs in the Tint parser.

```
        auto& switch_blocks = current_switch_blocks_.back(); // [0]

        auto* default_blk = b_.DefaultCase(switch_);
        if (default_id != merge_id) {
            switch_blocks.emplace(default_id);

            const auto& bb_default = current_spirv_function_->FindBlock(default_id);
            EmitBlockParent(default_blk, *bb_default); // [1]
        }
// ...
            if (blk_id != merge_id) {
                switch_blocks.emplace(blk_id); // [2]
            }
        }

```

The code obtains a reference (switch\_blocks) at [0]. However, when handling nested switches, it calls EmitBlockParent [1], which triggers an expansion of the current\_switch\_blocks\_ container. As a result, the previously acquired switch\_blocks variable ends up referencing invalid memory, eventually leading to a UAF at [2].

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/src/tint/lang/spirv/reader/parser/parser.cc;drc=d57639fceba51750cbf6d13a1cad552e865753aa;l=3686>

# VERSION

Operating System: Ubuntu 24.04

Dawn Version: HEAD (commit cdda346c7ce9483630118c275e20ee128b736afb)

# REPRODUCTION CASE

Build tint with ASAN.

```
$ cmake -GNinja -DTINT_BUILD_SPV_READER=ON -DDAWN_ENABLE_ASAN=ON ../..
$ ninja tint

```

Reproduce with tint

```
./tint --use-ir-reader=true tint_uaf.spv

```
# CRASH INFORMATION

Crash log: see asan.txt

# CREDIT INFORMATION

Reporter credit: DARKNAVY(@DarkNavyOrg)

## Attachments

- [tint_uaf.spv](attachments/tint_uaf.spv) (application/octet-stream, 1.1 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 18.4 KB)

## Timeline

### ds...@chromium.org (2025-08-25)

Note, this is not a Chrome security issue. The SPIR-V reader is not, and will not, be shipped in Chrome.

### an...@chromium.org (2025-08-25)

Marking this as a bug as this is not a Chrome security issue.

### dx...@google.com (2025-08-25)

Project: dawn  

Branch:  main  

Author:  dan sinclair [dsinclair@chromium.org](mailto:dsinclair@chromium.org)  

Link:    <https://dawn-review.googlesource.com/258974>

[spirv-reader] Fix issue with switch in switch default.

---


Expand for full commit details
```
     
    If the default block of a switch had a switch in it then we'd move the 
    current switch blocks pointer out from under ourselves. Use an index 
    instead of a reference. 
     
    Fixed: 440964231 
    Change-Id: I27acc6cc9e197cd77877a22482861363a06e38e2 
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/258974 
    Commit-Queue: dan sinclair <dsinclair@chromium.org> 
    Auto-Submit: dan sinclair <dsinclair@chromium.org> 
    Reviewed-by: James Price <jrprice@google.com> 
    Commit-Queue: James Price <jrprice@google.com>

```

---

Files:

- M `src/tint/lang/spirv/reader/parser/branch_test.cc`
- M `src/tint/lang/spirv/reader/parser/parser.cc`

---

Hash: 862482a2ab85b18bba042cc933875bbaf7b7e306  

Date: Mon Aug 25 16:58:13 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. As this issue does not impact shipped, production versions of Chrome, this issue is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-12-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. As this issue does not impact shipped, production versions of Chrome, this issue is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Security Bot
> 
> 
> --
> How did we do? Please fill out

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/440964231)*
