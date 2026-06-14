# Uninitialized variable usage in ANGLE may cause a memory disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40090901](https://issues.chromium.org/issues/40090901) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | al...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2018-03-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
Blit11::copyAndConvert(/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp) does not check the return value of ID3D11DeviceContext::Map, when it's called on a system which has Nvidia drivers below a certain version installed:  
  
1515: gl::Error Blit11::copyAndConvert  
...

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090901)*
