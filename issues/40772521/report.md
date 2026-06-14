# Security: Use-after-free in NavigatorShare::OnConnectionError

| Field | Value |
|-------|-------|
| **Issue ID** | [40772521](https://issues.chromium.org/issues/40772521) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebShare |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2021-06-15 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**   
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webshare/navigator_share.cc;drc=71003be7ce59254518062bb7fa11ba4dc5106f0b;l=321  
```  
void NavigatorShare::OnConnectionError() {  
  for (auto& client : clients_) {  
    client-

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40772521)*
