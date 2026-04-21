# Security:Integer overflow in vn_decode_vkExecuteCommandStreamsMESA_args_temp

| Field | Value |
|-------|-------|
| **Issue ID** | [40064696](https://issues.chromium.org/issues/40064696) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-05-21 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

The vulnerability exists in the venus implementation of virglrenderer, which serves as the vulkan backend of crosvm and can be used to escape the vm through this.

Integer overflow leads to buffer overflow in vn\_decode\_vkExecuteCommandStreamsMESA\_args\_temp.

```
static inline void vn_decode_vkExecuteCommandStreamsMESA_args_temp(struct vn_cs_decoder \*dec, struct vn_command_vkExecuteCommandStreamsMESA \*args)  
{  
    vn_decode_uint32_t(dec, &args->streamCount);  
    if (vn_peek_array_size(dec)) {  
        const uint32_t iter_count = vn_decode_array_size(dec, args->streamCount);  
        args->pStreams = vn_cs_decoder_alloc_temp(dec, sizeof(\*args->pStreams) \* iter_count);      <----- 32-bit integer overflow  
        if (!args->pStreams) return;  
        for (uint32_t i = 0; i < iter_count; i++)  
            vn_decode_VkCommandStreamDescriptionMESA_temp(dec, &((VkCommandStreamDescriptionMESA \*)args->pStreams)[i]);    <----- buffer overflow  
    } else {  
        vn_decode_array_size(dec, args->streamCount);  
        args->pStreams = NULL;  
    }  
    if (vn_peek_array_size(dec)) {  
        const size_t array_size = vn_decode_array_size(dec, args->streamCount);  
        args->pReplyPositions = vn_cs_decoder_alloc_temp(dec, sizeof(\*args->pReplyPositions) \* array_size);  
        if (!args->pReplyPositions) return;  
        vn_decode_size_t_array(dec, (size_t \*)args->pReplyPositions, array_size);  
    } else {  
        vn_decode_array_size_unchecked(dec);  
        args->pReplyPositions = NULL;  
    }  
    vn_decode_uint32_t(dec, &args->dependencyCount);  
    if (vn_peek_array_size(dec)) {  
        const uint32_t iter_count = vn_decode_array_size(dec, args->dependencyCount);  
        args->pDependencies = vn_cs_decoder_alloc_temp(dec, sizeof(\*args->pDependencies) \* iter_count);  
        if (!args->pDependencies) return;  
        for (uint32_t i = 0; i < iter_count; i++)  
            vn_decode_VkCommandStreamDependencyMESA_temp(dec, &((VkCommandStreamDependencyMESA \*)args->pDependencies)[i]);  
    } else {  
        vn_decode_array_size(dec, args->dependencyCount);  
        args->pDependencies = NULL;  
    }  
    vn_decode_VkFlags(dec, &args->flags);  
}  

```

**VERSION**

virglrenderer: virglrenderer-0.10.4  

ChromeOS: 113.0.5672.134

**REPRODUCTION CASE**

1. Start termia with vulkan enable via command: vmc start --enable-gpu --enable-vulkan termina
2. Copy & Compile the poc.c in termina
3. Run the poc

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 3.6 KB)
- [poc.c](attachments/poc.c) (text/plain, 3.1 KB)

## Timeline

### [Deleted User] (2023-05-21)

[Empty comment from Monorail migration]

### fi...@gmail.com (2023-05-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-22)

Hi zzyiwei@, I see that you are the most recent committer to the file that contains this function in the Chromium code source. I am assigning this to you, but please feel free to triage this to whoever would be best suited to address this bug. I'm unsure what exactly the component for this would be, so if you could also add the component to this bug, that'd be great. Thanks!

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-22)

Please migrate this bug to issuetracker instead.

More importantly, venus issues like this is not security issue since venus context runs inside isolated forked render worker process instead of inside virtio-gpu device process, and cannot be used to escape from VM at all.

### zz...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-22)

No need to migrate to issuetracker since this is working as intended, and no security issue is involved.

### pa...@chromium.org (2023-05-23)

I'm really not sure this is WontFix, WAI. It's a straightforward case of a potential integer overflow resulting in an allocation not large enough to hold `iter_count` objects, but then the code goes on to process `iter_count` objects regardless. This is a classic bug pattern, and sometimes exploitable.

So it's at least a crasher that could be easily fixed. And it might also lead to correctness problems/weird output on the screen/et c.

But, also, it might enable some other calling process to compromise the process this code runs in. If this code is running at even slightly higher privilege than the caller, that is an escalation of privilege to some degree (even if not VM escape). I don't know enough about Venus to know whether that is the case. If the process this code runs in is guaranteed to always have *lower* privilege than any caller, then let's document that and get all the Chrome and ChromeOS security teams aware of that.

Fixing this bug is easy enough:

```
uint32_t size = 0;
if (__builtin_mul_overflow(iter_count, sizeof(*args->pStreams), &size)) return;
args->pStreams = vn_cs_decoder_alloc_temp(dec, size);
```

so I'd really like to see at least that.

And it's a good idea to do a variant analysis (using e.g. semantic grep or https://github.com/weggli-rs/weggli) to get ahead of this class of bug. There's been a handful lately.

+cc some security crew more knowledgeable than me.

[Monorail components: Internals>GPU>Internals]

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-23)

It's more about expectation for the Venus working model.  There're a lot more details on the other issue.

Vulkan itself runs in an unvalidated manner, and the venus-protocol which bridges the guest venus driver and host vkr renderer is following the "Vulkan" style of defining "Valid Usage" for the client. As long as the client venus driver is obeying venus-protocol, this kind of issue never happens.

The _fix_ is intended to be an "assert" or a debug log if violating, instead of handling silently.

This issue doesn't qualify as a security bug, and the detailed rationale is on https://crbug.com/chromium/1447373

### zz...@chromium.org (2023-05-23)

I am willing to secure up the vkr pieces to the extend not affecting performance (the overhead here is trivial), but we should only fix that as a normal bug instead of a security bug.

### fi...@gmail.com (2023-05-23)

https://crbug.com/chromium/1447372#c8
> But, also, it might enable some other calling process to compromise the process this code runs in. If this code is running at even slightly higher privilege than the caller, that is an escalation of privilege to some degree (even if not VM escape). 

The caller is guest app running in guest vm which can not directly access to host resource(e.g. host drm kernel, some host syscalls like socket, sendmsg...)
The process this code runs is a sandboxed process running on the host, which can directly access to some host resources which guest app can't(e.g. host drm kernel, some host syscalls like socket, sendmsg...)

As I said in another comment, this can be used in a chain of attack to get root in host from guest. See https://crbug.com/1447373#c13.

### zz...@chromium.org (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/284107046). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting  Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/284107046]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

Marked as fixed.

Fix (https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1141) has landed upstream 

Flowed to cros via virglrenderer uprev crrev/c/4594446.

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### st...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations on another one, rinngo! The VRP Panel has decided to award you $7,000 for this report of memory corruption in a sandboxed process. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1447372?no_tracker_redirect=1

[Monorail blocking: b/284107046]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064696)*
