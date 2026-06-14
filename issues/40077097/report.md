# Security: H.264 scaling list parsing overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40077097](https://issues.chromium.org/issues/40077097) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | jo...@chromium.org |
| **Assignee** | po...@chromium.org |
| **Created** | 2013-03-08 |
| **Bounty** | $40,000.00 |

## Description

In content/common/gpu/media/h264_parser.cc:

res = ParseScalingList(sizeof(sps->scaling_list4x4[i]),
                       sps->scaling_list4x4[i], &use_default);

sizeof(sps->scaling_list4x4[i]) is used in that function as a count of
int-sized elements, causing an overflow.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077097)*
