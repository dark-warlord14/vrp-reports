# Security: Multiple cros_ec bugs when handling host commands from Application Processor

| Field | Value |
|-------|-------|
| **Issue ID** | [40065552](https://issues.chromium.org/issues/40065552) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-06-09 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Hi, I reviewed the cros\_ec host command handlers, found some bugs.  

I'm not sure if chromeos bug bounty has interests on cros\_ec bugs, so I report all the found bugs in one ticket for you to review

cros\_ec is a MCU of chromebook, Host(AP) side can send host commands through a driver:

localhost ~ # ls -l /dev/cros\_ec  

crw-rw----. 1 root cros\_ec-access 10, 57 Dec 19 09:00 /dev/cros\_ec

cros\_ec firmware codes will handle the host command using corresponding handlers. cros\_ec uses DECLARE\_HOST\_COMMAND to define host command handlers.

In below 3 handlers, there are memory safety bugs.

Problem 1:

Almost arbitrary memory read in handler read\_memory\_dump because of integer overflow:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/ec/common/host_command_memory_dump.c;drc=bb348806dfcc219e8e388617d1748077b0965b9c;l=134>

The logic is read entries information by cmd EC\_CMD\_MEMORY\_DUMP\_GET\_METADATA and EC\_CMD\_MEMORY\_DUMP\_GET\_ENTRY\_INFO, then trigger read\_memory\_dump cmd with proper args.

static enum ec\_status read\_memory\_dump(struct host\_cmd\_handler\_args \*args)  

{  

const struct ec\_params\_memory\_dump\_read\_memory \*p = args->params; <-------- parameters from host  

void \*r = args->response;  

struct memory\_dump\_entry entry;

```
//skip..  

entry = entries[p->memory_dump_entry_index];  

if (p->address < entry.address ||  
    p->address + p->size > entry.address + entry.size) { <---- can integer overflow to bypass check, so p->address can be any value which >= entry.address  
	return EC_RES_INVALID_PARAM;  
}  

/\* Must leave room for ec_host_response header \*/  
args->response_size = MIN(  
	p->size, args->response_max - sizeof(struct ec_host_response));  

memcpy(r, (void \*)p->address, args->response_size); <----- read args->response_size to rsp buffer , return to AP side  

mutex_unlock(&memory_dump_mutex);  

return EC_RES_SUCCESS;  

```

}

Problem 2:

OOB write in host command handler port80\_command\_read:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/ec/common/port80.c;drc=71b2ef709dcb14260f5fdaa3ab4ced005a29fb46;l=212>  

const struct ec\_params\_port80\_read \*p = args->params;  

uint32\_t offset = p->read\_buffer.offset;  

uint32\_t entries = p->read\_buffer.num\_entries; <------- entries from args

```
    //skip..  

    else if (p->subcmd == EC_PORT80_READ_BUFFER) {  
	/\* do not allow bad offset or size \*/  
	if (offset >= ARRAY_SIZE(history) || entries == 0 ||  
	    entries > args->response_max)    <--------- if entries == args->response_max  
		return EC_RES_INVALID_PARAM;  

	for (i = 0; i < entries; i++) {   
		uint16_t e =  
			history[(i + offset) % ARRAY_SIZE(history)];  
		rsp->data.codes[i] = e; <-------- codes is uint16_t array, if entries is args->response_max, will write args->response_max \* 2 bytes, oob write  
	}  

	args->response_size = entries \* sizeof(uint16_t); <------ set bigger response_size, will cause a error when return to host, host side /dev/cros_ec will log a error  
	return EC_RES_SUCCESS;  
}  

```

Problem 3:

OOB access in host cmd handler hc\_usb\_pd\_mux\_ack:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/ec/driver/usb_mux/usb_mux.c;drc=98406285eb79141babdae0710cc24b9d9dde9db9;l=852>

static enum ec\_status hc\_usb\_pd\_mux\_ack(struct host\_cmd\_handler\_args \*args)  

{  

\_\_maybe\_unused const struct ec\_params\_usb\_pd\_mux\_ack \*p = args->params;

```
if (!IS_ENABLED(CONFIG_USB_MUX_AP_ACK_REQUEST))  
	return EC_RES_INVALID_COMMAND;  

if (ack_task[p->port] != TASK_ID_INVALID)   <------- not check p->port, can oob  
	task_set_event(ack_task[p->port], PD_EVENT_AP_MUX_DONE); <------ in some implementation of task_set_event it will cause oob write  

return EC_RES_SUCCESS;  

```

}

There are several task\_set\_event implementations in cros\_ec, some can cause oob write, for example:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/ec/core/host/task.c;drc=9d53cabe56d5c33cb3169161f3f8438ab16f45fe;l=209>  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/ec/core/cortex-m/task.c;drc=42167827fbbc9d0100f151c2980d15a46e61957b;l=452>

**VERSION**  

latest code of platform/ec

**REPRODUCTION CASE**

Problem 1: on my chromebook in hand, this command returns invalid command, maybe need chromebooks with CONFIG\_ZEPHYR

Problem 2: I can reproduce the issue by the error log from /dev/cros\_ec which indicates the response\_size is bigger than response\_max, but don't have crash, I think this depends on what behind the rsp buffer, some boards may have interesting structures behind the rsp buffer

Problem 3: On my chromebook, it's not crash, may needs proper chromebooks

Attachments are sample codes which can trigger these host commands from host side by access /dev/cros\_ec driver.

## Attachments

- [EC_CMD_MEMORY_DUMP_READ_MEMORY_poc.c](attachments/EC_CMD_MEMORY_DUMP_READ_MEMORY_poc.c) (text/plain, 3.7 KB)
- [EC_CMD_PORT80_READ_poc.c](attachments/EC_CMD_PORT80_READ_poc.c) (text/plain, 3.1 KB)
- [EC_CMD_USB_PD_MUX_ACK_poc.c](attachments/EC_CMD_USB_PD_MUX_ACK_poc.c) (text/plain, 1.9 KB)

## Timeline

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-09)

Thanks for the bug report!

Reading: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#Life-Of-A-Security-Bug
```
If the bug is a security bug, but is only applicable to Chrome OS:
The Chrome OS Security team now has their own sheriffing rotation. To get bugs into their triage queue, just set OS to the single value of “Chrome”. No other steps or labels are needed.
```

So, I will let ChromeOS security sheriff to take a look.
Reading: src/platform/ec/README.md this might be a component ChromeOS isn't using anymore?


### pi...@gmail.com (2023-06-09)

I think code of platform/ec is still used, even on new chromebooks. 

I think the underlying RTOS has changed to zephyr on newer chromebooks according to picture in:
https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/platform/ec/docs/zephyr/README.md

Also the source explaination in above doc: 
platform/ec - local repository containing code shared by the legacy EC and the Zephyr EC

### st...@google.com (2023-06-09)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286540890). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

[Monorail blocking: b/286540890]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### pi...@gmail.com (2023-07-10)

Hi, b/286540890 has been fixed, I think this ticket should be updated to Fixed. Thanks

### ch...@google.com (2023-07-25)

Marked as Fixed 

Project: chromiumos/platform/ec
Branch: main

commit 56cc37da2047d63f941336c79bb95efbd4453c31
Author: Boris Mittelberg <bmbm@google.com>
Date:   Mon Jun 26 19:09:18 2023

    ec: memory access fixes
   
    Add bound checks on memory access
   
    BUG=b:286540890
    TEST=make -j buildall and adding unit tests
    LOW_COVERAGE_REASON=added tests where possible
   
    Change-Id: I93097fb4f731d5dc78bf31fc66c80c706e5e9359
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform/ec/+/4648449
    Tested-by: Boris Mittelberg <bmbm@google.com>
    Reviewed-by: caveh jalali <caveh@chromium.org>
    Reviewed-by: Daisuke Nojiri <dnojiri@chromium.org>
    Commit-Queue: Boris Mittelberg <bmbm@google.com>

M       common/host_command_memory_dump.c
M       common/port80.c
M       driver/usb_mux/usb_mux.c
M       zephyr/test/drivers/host_command_memory_dump/src/host_command_memory_dump.c

https://chromium-review.googlesource.com/4648449
03:52
03:52
CLs: Merged:​<none>      crrev/c/4648449
CLs: Pending:​crrev/c/4648449      <none>

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### al...@google.com (2023-08-15)

This should probably be treated as 3 separate low severity bugs.

### pi...@gmail.com (2023-08-16)

Hi, May I know why the severity is low? According to cros_ec introduction document, the cros_ec is responsible for : 
    power sequencing, keyboard control, thermal control, battery charging, and verified boot
https://chromium.googlesource.com/chromiumos/platform/ec/+/HEAD/README.md#Introduction

So I think cros_ec is safety(thermal control) and security critical component, from AP to cros_ec the protection domain has been changed.

Thanks

### [Deleted User] (2023-08-16)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-19)

Note: this probably should've been filed as several separate bugs as they don't have all the same attributes, which makes it a bit awkward to summarize them.

Exploitability: Requires the ability to send arbitrary commands to the EC. Can perform OOB writes, although not with control over what values are written and so it would require a very special exploit. Can demonstrate a way to trigger the OOB writes but not necessarily to do anything with them.

Privileges and Capabilities: Trigger OOB writes on EC with limited/no control over the values written

Origin of fix: Not known upstream until reported by the reporter

Mitigations: Difficult to exploit, as there does not seem to be any control over what OOB writes get written.

Severity Assessment: Low severity due to the limited ability to exploit the writes (no control over values or addresses). Even reproducing a crash with these appears to be challenging.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-31)

This issue was migrated from crbug.com/chromium/1453507?no_tracker_redirect=1

[Monorail blocking: b/286540890]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065552)*
