# Integer overflow in vkr_cs_encoder_set_stream

| Field | Value |
|-------|-------|
| **Issue ID** | [40064697](https://issues.chromium.org/issues/40064697) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | zz...@chromium.org |
| **Created** | 2023-05-21 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

The vulnerability exists in the venus implementation of virglrenderer, which serves as the vulkan backend of crosvm and can be used to escape the vm through this.

Integer overflow leads to buffer overflow in vkr\_cs\_encoder\_set\_stream.

```
void  
vkr_cs_encoder_set_stream(struct vkr_cs_encoder \*enc,  
                          const struct vkr_resource \*res,  
                          size_t offset,  
                          size_t size)  
{  
   if (!res) {  
      memset(&enc->stream, 0, sizeof(enc->stream));  
      enc->cur = NULL;  
      enc->end = NULL;  
      return;  
   }  
  
   if (unlikely(size + offset > res->size)) {       <----- integer overflow  
      vkr_log(  
         "failed to set the reply stream: offset(%zu) + size(%zu) exceeds res size(%zu)",  
         offset, size, res->size);  
      vkr_cs_encoder_set_fatal(enc);  
      return;  
   }  
  
   enc->stream.resource = res;  
   enc->stream.offset = offset;  
   enc->stream.size = size;  
  
   enc->end = res->u.data + res->size;  
  
   vkr_cs_encoder_seek_stream(enc, 0);  
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

- [asan.log](attachments/asan.log) (text/plain, 1.7 KB)
- [poc.c](attachments/poc.c) (text/plain, 4.2 KB)

## Timeline

### fi...@gmail.com (2023-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-22)

Hi zzyiwei@, I see that you are the most recent committer to the file that contains this function in the Chromium code source. I am assigning this to you, but please feel free to triage this to whoever would be best suited to address this bug. I'm unsure what exactly the component for this would be, so if you could also add the component to this bug, that'd be great. Thanks!

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-22)

Please migrate this bug to issuetracker instead.

More importantly, venus issues like this is not security issue since venus context runs inside isolated forked render worker process instead of virtio-gpu device process, and cannot be used to escape from VM at all.

### zz...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-22)

No need to migrate to issuetracker since this is working as intended, and no security issue is involved.

### fi...@gmail.com (2023-05-22)

> More importantly, venus issues like this is not security issue since venus context runs inside isolated forked render worker process instead of virtio-gpu device process, and cannot be used to escape from VM at all.

The virgl_render_server is running on host. Is it considered a security boundary to exploit the process running on the host from the guest vm?

### fi...@gmail.com (2023-05-22)

What I want to explain is that the crashing process is virgl_render_server running in the host, and the poc should run in the guest vm.

### zz...@chromium.org (2023-05-22)

Yes, that's working as intended by design of the Virtio-GPU Venus stack for Vulkan virtualization.
1. Venus is mandated to run with isolated render server and forked render worker processes (Zygote model).
2. With sandbox enforced, the virgl_render_server process is started by crosvm upon the guest VM boots. Unlike virtio-gpu device process, the render server has no access to guest memory mapping.
3. Each guest Vulkan app's vkCreateInstance call would trigger an isolated render worker process to be forked from the sandbox'ed virgl_render_server process.
4. Vulkan commands are streamed via a shared ringbuffer between the guest app and the forked host render worker process.
5. Whenever the Vulkan driver crashes inside the forked render worker process, only that process crashes without affecting virtio-gpu device process. Meanwhile, guest venus driver detects the renderer crash and abort just the corresponding guest app.

Above is how Venus works to provide Vulkan support. From security stance, this is not a regression as compared to container based solution. It's working as intended that the guest app can easily gain code execution from the corresponding host render worker process, because host render worker process runs Vulkan, which can crash in random ways as long as the guest app violates the Vulkan spec.

Taking control of the host render work process is unable to be used to attack the guest OS, since it's isolated from virtio-gpu device process. At the same time from the host pov, gaining code execution won't hurt as long as host kernel boundary is secure, which is indeed the security boundary for 3D graphics across all native Linux environment in the industry.

So both issues are no issue by design since Vulkan allows you to easily achieve the same.

### fi...@gmail.com (2023-05-22)

But it can actually be used in such as chain. It is impossible to affect the host kernel from the guest vm directly, but through this vulnerability, you can access the host kernel and expand the attack surface, right?

This is a comment from your team, https://crbug.com/1430323#c15.


### zz...@chromium.org (2023-05-22)

This is by design of Venus. The goal is to provide 3D graphics support in the VM scenario while not regressing from the prior container based solution (e.g. ARC++, which runs Android in container natively on the host side). As a result, Venus does provide better security here since the host render server is sandboxed and jailed. So it's an improvement as compared to the prior container solution.

When host gpu drm kernel driver has security issues, our guest VM is still secure unless involving a chain of attack like: guest app -> host renderer -> host drm kernel -> host other kernel driver -> host other userspace pieces inside other virtio devices which has visibility into guest memory mapping. In the meanwhile, when such host kernel vulnerability shows up, the entire industry running gpu driver in the native environment is at much higher risk than ChromeOS.

### fi...@gmail.com (2023-05-22)

> When host gpu drm kernel driver has security issues, our guest VM is still secure unless involving a chain of attack like: guest app -> host renderer -> host drm kernel -> host other kernel driver -> host other userspace pieces inside other virtio devices which has visibility into guest memory mapping. 

guest app(the poc) -> host renderer(code execution through this vuln) -> host drm kernel(if there is vulnerability in host drm kernel, we can do anything in the host. Why do I need to use other vulnerabilities to affect the guest vm? I have the highest privilege on the host).

Considering the above scenario, this vulnerability can be used in a chain of attack to get root in host from guest.

You guys don't think moving from a guest app to a sandboxed process running on the host is a security issue, even if it can expand the attack surface (access to the drm kernel and some syscalls(e.g. create socket, sendmsg...) on host that should not be accessible from guest app), right?

### zz...@chromium.org (2023-05-22)

> guest app(the poc) -> host renderer(code execution through this vuln) -> host drm kernel(if there is vulnerability in host drm kernel, we can do anything in the host. Why do I need to use other vulnerabilities to affect the guest vm? I have the highest privilege on the host).

nvm, ignore that part. Late night fuzz ; )

> Considering the above scenario, this vulnerability can be used in a chain of attack to get root in host from guest.
>
> You guys don't think moving from a guest app to a sandboxed process running on the host is a security issue, even if it can expand the attack surface (access to the drm kernel and some syscalls(e.g. create socket, sendmsg...) on host that should not be accessible from guest app), right?

Again this is by design, and is an improvement from the prior container based solution, without regressing performance. Meanwhile, it has already provided better security protection agains the same surface (kernel drm driver) shared across the Linux ecosystem. This is not a perfect solution as I have mentioned earlier.

These 2 issues are no issues since you can easily gain code execution in the sandboxed isolated host venus render worker process forked directly via Vulkan API by violating the Vulkan spec. Vulkan userspace driver isn't fuzzable and is not designed to be fuzzable either, meanwhile the API is also not designed to ship with validation enabled. So process isolation is our answer to this problem, signed off by our security team.

### zz...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-22)

Meanwhile, we might fix the issue as a normal bug instead of a security bug. It'd be mainly for error logging to ease debugging in certain circumstance.

### pa...@chromium.org (2023-05-22)

Sometimes bugs that are shaped like this can be exploitable, and are at least correctness bugs (as you note), so I'd strongly suggest adopting a general solution to the integer overflow problem.

For vanilla C, I suggest stdckdint.h (new in C23) or the equivalent Clang/GCC intrinsics (`__builtin_mul_overflow`, et c.).

For C++, I suggest Chromium's //base/numerics or possibly https://github.com/chromium/subspace (talk to danakj@).

Also, compiler warnings will sometimes highlight integer problems, e.g. https://clang.llvm.org/docs/DiagnosticsReference.html#wshorten-64-to-32 and https://clang.llvm.org/docs/DiagnosticsReference.html#wsign-conversion. I suggest turning them on.

### aj...@google.com (2023-05-22)

-> RE https://crbug.com/chromium/1447373#c17 -> Untriaged

This issue should either be turned into a normal non-security issue (and fixed), or left as a security issue (then fixed). 

I believe this only affects ChromeOS -> OS=Chrome for further triage.

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-23)

Hi ajgo@, I was saying this didn't qualify as a security bug. Meanwhile, after dropping security tag, this wasn't even a bug anymore, since venus-protocol requires the driver side to obey the protocol expectation to not end up with undefined behavior. Hope I made it clear now ; )

### aj...@google.com (2023-05-23)

I may be being obtuse here - but other issues in virglrenderer are treated as security issues (e.g. https://crbug.com/1427332).

So I can understand what is happening - could you (zzyiwei) outline where the code is running and why that means it isn't a security issue?

### zz...@chromium.org (2023-05-23)

Re #22, see my https://crbug.com/chromium/1447373#c10 and #12 brief of the difference. Thanks!

### ch...@google.com (2023-05-23)

@zzyiwei@chromium.org : thanks for your input! Will follow your comment and remove Security label

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### zz...@chromium.org (2023-05-23)

Thanks Joerg! I'll keep this open for the code improvement ; )

### pa...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>Internals]

### jo...@chromium.org (2023-05-25)

This is a P1 high severity sandbox escape security bug.

### zz...@chromium.org (2023-05-26)

Could you help migrate this to issuetracker like the other 1447373? So we handle them in one place (more used to issuetracker). Thanks

### st...@google.com (2023-06-01)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/285399496). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### ch...@google.com (2023-06-12)

Fix (https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1141) has landed upstream a day ago but flow to CrOS side is still blocked by infra issue.

Marked as fixed.

Flowed to cros via virglrenderer uprev crrev/c/4594446.

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-17)

[Empty comment from Monorail migration]

[Monorail blocking: b/285399496]

### ch...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations rinngo! The VRP Panel has decided to award you $7,000 for this report of memory corruption in a sandboxed process in ChromeOS.Thank you for your efforts and reporting this issue to us!  

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1447373?no_tracker_redirect=1

[Monorail blocking: b/285399496]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064697)*
