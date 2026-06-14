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

[0] button\_index is an interface parameter that can be controlled by the user, because it can be constructed with any size.  

action\_keys\_for\_buttons is a vector variable belonging to click\_action. Since [1] is a DCHECK, it will cause OOB read at [2]

**-------------------------** -------------------------------------------------  

<event name="clicked">  

<description summary="Notification is clicked">  

Notifies the notification object that the notification or its button is clicked.  

</description>  

<arg name="button\_index" type="int" summary="-1 if the body of the notification is cliked as opposed to a button"/> //[0]  

</event>

**-------------------------** ---------------------------------------------------  

void NotificationDaemon::OnClicked(const std::string& notification\_key,  

int32\_t button\_index) {  

uint32\_t id = 0;  

bool ret = base::StringToUint(notification\_key, &id);  

DCHECK(ret);  

DCHECK(click\_actions.find(id) != click\_actions.end());

// Convert |button\_index| into action key using |click\_action|.  

const auto click\_action = click\_actions[id];  

std::string action\_key;  

if (button\_index == -1) {  

if (click\_action.default\_action\_enabled) {  

action\_key = kDefaultActionKey;  

}  

} else {  

DCHECK\_LT(button\_index, click\_action.action\_keys\_for\_buttons.size()); //[1]  

action\_key = click\_action.action\_keys\_for\_buttons[button\_index]; //[2]  

}

// Forward notification clicked event to client via D-Bus if associated action  

// key exists.  

if (!action\_key.empty()) {  

dbus\_service\_->SendActionInvokedSignal(id, action\_key);  

}  

}

**REPRODUCTION CASE**  

Not sure how to construct a PoC, although it seems to be a vulnerability in the dbus component

Patch

--- a/notification\_daemon.cc 2023-05-31 10:48:20.804447200 +0800  

+++ b/notification\_daemon.cc 2023-05-31 10:50:04.798535900 +0800  

@@ -172,8 +172,8 @@  

action\_key = kDefaultActionKey;  

}  

} else {

- DCHECK\_LT(button\_index, click\_action.action\_keys\_for\_buttons.size());
- action\_key = click\_action.action\_keys\_for\_buttons[button\_index];

- if(button\_index < click\_action.action\_keys\_for\_buttons.size());
- ```
   action_key = click_action.action_keys_for_buttons[button_index];  
  
  ```
  
  }
  
  // Forward notification clicked event to client via D-Bus if associated action

## Timeline

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### aj...@google.com (2023-06-01)

Hello - I cannot locate this code in our repository - https://source.chromium.org/search?q=notification_daemon.cc&ss=chromium%2Fchromium%2Fsrc - could you point to where this code is?

### yq...@gmail.com (2023-06-02)

https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform2/vm_tools/notificationd/notification_daemon.cc;l=160

### aj...@google.com (2023-06-02)

-> ChromeOS (not investigated yet)

### [Deleted User] (2023-06-02)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@google.com (2023-06-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286204915). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### st...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/286204915]

### ch...@google.com (2023-06-12)

Project: chromiumos/platform2
Branch: main

commit f769c8aaa8a5eb56137f020d01c149aead97b4de
Author: David Munro <davidmunro@google.com>
Date:   Fri Jun 09 12:13:04 2023

    vm_tools: Fix possible out-of-bounds read in notificationd
   
    Theoretically if a button_index larger than the number of buttons were
    sent to notificationd from exo we'd read past the end of the array. It's
    not performance-sensitive code so let's make it a CHECK instead of a
    DCHECK to always crash if that happens.
    Also fix a typo while I'm at it.
   
    BUG=b:286204915
    TEST=CQ, #yolo
   
    Change-Id: Ic2aa5d7c01ca85b99cc59ca20ba4e1630ac03c49
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4600416
    Reviewed-by: Nic Hollingum <hollingum@google.com>
    Commit-Queue: David Munro <davidmunro@google.com>
    Tested-by: David Munro <davidmunro@google.com>

M       vm_tools/notificationd/notification_daemon.cc
M       vm_tools/notificationd/protocol/notification-shell-unstable-v1.xml

https://chromium-review.googlesource.com/4600416
05:38
05:38
CLs: Merged:​<none>      crrev/c/4600416
CLs: Pending:​crrev/c/4600416      <none>

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-19)

Exploitability - Explain why/why not the bug is reachable and/or exploitable For example, if a bug mentions a race, details are needed about how easy that race would be to achieve / can the attack retry infinite times to win the race, etc.."

The OOB read can happen with a user click, passed through Exo. The bug is present in notification_dameon and is run inside crostini. The events come from Exo over wayland and that is not user controlable. So for this be exploited, the malicious command ("click") needs to run through Exo. No demonstration of exploitation in the bug. Just theoretical.

Privileges and Capabilities - Identify which process is exploited and where code execution potentially can be achieved if the attacker can break out of that process, and explain why

For this to work,exo needs to be compromised.

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility

The fix was uploaded by engineers on CrOS.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)

Exo/ Wayland needs to be compromised here for this to work and possibly dbus

Severity assessment - why not higher, why not lower

Low Severity; At worst this is OOB and this bug does not have any evidence that OOB can be reached.

Why not Medium Severity? There are mitigating factors such as notification events need to be passed over Exo.

Why not No Impact? The bug can still cause a potential OOB read. Had Exo not been there this would have medium severity. Essentially this is a potential security bug and has some theoretical impact so I cannot mark is as no impact.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1450118?no_tracker_redirect=1

[Monorail blocked-on: b/286204915]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065052)*
