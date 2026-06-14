# Security: OOB in NotificationDaemon::OnClicked

| Field | Value |
|-------|-------|
| **Issue ID** | [40065052](https://issues.chromium.org/issues/40065052) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | yq...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-05-31 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**   
  
[0] button_index is an interface parameter that can be controlled by the user, because it can be constructed with any size.   
action_keys_for_buttons is a vector variable belonging to click_action. Since [1] is a DCHECK, it will cause OOB read at [2]  
  
**------

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065052)*
