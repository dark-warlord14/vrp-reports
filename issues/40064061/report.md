# Security: Chrome OS i915 drm gpu driver create_clone UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [40064061](https://issues.chromium.org/issues/40064061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-15 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

This i915 drm gpu driver is used on Pixelbook. The latest pixelbook image kernel version is 5.4.

In this ioctl call path has a bug can cause UAF:  

i915\_gem\_context\_create\_ioctl -> i915\_user\_extensions -> create\_clone

It doesn't increase the i915\_gem\_context object refcount when lookup in create\_clone.  

So another thread can free the i915\_gem\_context object by i915\_gem\_context\_destroy\_ioctl, cause UAF.

Ioctl function i915\_gem\_context\_create\_ioctl can receive an extension argument, which can trigger to call i915\_user\_extensions.  

if (args->flags & I915\_CONTEXT\_CREATE\_FLAGS\_USE\_EXTENSIONS) { <----- flags  

ret = i915\_user\_extensions(u64\_to\_user\_ptr(args->extensions),  

create\_extensions,  

ARRAY\_SIZE(create\_extensions),  

&ext\_data);  

if (ret)  

goto err\_ctx;  

}

i915\_user\_extensions will call functions in function table create\_extensions, using arguments from userspace.  

static const i915\_user\_extension\_fn create\_extensions[] = {  

[I915\_CONTEXT\_CREATE\_EXT\_SETPARAM] = create\_setparam,  

[I915\_CONTEXT\_CREATE\_EXT\_CLONE] = create\_clone,  

};

create\_clone is one of the function in table create\_extensions:

static int create\_clone(struct i915\_user\_extension \_*user \*ext, void \*data)  

{  

static int (\* const fn[])(struct i915\_gem\_context \*dst,  

struct i915\_gem\_context \*src) = { <-------- define function table  

#define MAP(x, y) [ilog2(I915\_CONTEXT\_CLONE*##x)] = y  

MAP(ENGINES, clone\_engines),  

MAP(FLAGS, clone\_flags),  

MAP(SCHEDATTR, clone\_schedattr),  

MAP(SSEU, clone\_sseu),  

MAP(TIMELINE, clone\_timeline),  

MAP(VM, clone\_vm),  

#undef MAP  

};

```
//skip...  

rcu_read_lock();     <--------- rcu lock  
src = __i915_gem_context_lookup_rcu(arg->fpriv, local.clone_id); <---- find src object by userspace id, but doesn't increase refcount  
rcu_read_unlock();  <--------- rcu unlock, after unlock another thread can free src object  
if (!src)  
	return -ENOENT;  

GEM_BUG_ON(src == dst);  

for (bit = 0; bit < ARRAY_SIZE(fn); bit++) {  
	if (!(local.flags & BIT(bit)))   <--------- local.flags is from userspace  
		continue;  

	err = fn[bit](dst, src);    <--------- Use src object, but another thread can free it after unlock.  
	if (err)  
		return err;  
}  

return 0;  

```

}

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/gpu/drm/i915/gem/i915_gem_context.c;drc=738d03377473ad797ef344867678ec17106c3e23;l=2305>

**VERSION**  

Pixelbook eve, 112.0.5615.62  

v5.4 latest kernel code

**REPRODUCTION CASE**

To demo this issue more clearly, I add a msleep in create\_clone right after the rcu\_read\_unlock().  

1, Build pixelbook image with the attached patch.  

2, Compile the poc code, run with chronos user shell, the kernel will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

On my self build pixelbook image using latest code, the crash call stack:

[ 8199.736085] general protection fault: 0000 [#1] PREEMPT SMP PTI  

[ 8199.736092] CPU: 2 PID: 23326 Comm: drm\_poc Not tainted 5.4.240-20638-gbc4b527279cb-dirty #8  

[ 8199.736097] Hardware name: Google Eve/Eve, BIOS Google\_Eve.9584.230.0 09/06/2021  

[ 8199.736106] RIP: 0010:clone\_engines+0x2c/0x15c  

[ 8199.736112] Code: 44 00 00 55 48 89 e5 41 57 41 56 41 55 41 54 53 48 83 ec 10 49 89 f5 49 89 fe 48 8d 5e 18 48 89 df e8 e5 dd 83 00 4d 8b 65 10 <41> 8b 7c 24 40 e8 ad f2 ff ff 48 85 c0 0f 84 01 01 00 00 49 89 c7  

[ 8199.736117] RSP: 0018:ffffa2d082633bf8 EFLAGS: 00010296  

[ 8199.736123] RAX: 0000000000000000 RBX: ffff9dcdc890ea18 RCX: 7ae35f424f48eb00  

[ 8199.736127] RDX: ffff9dcdd7e10000 RSI: 0000000000000002 RDI: ffff9dcdc890ea18  

[ 8199.736131] RBP: ffffa2d082633c30 R08: 8000000000000000 R09: ffffa2d102633a8f  

[ 8199.736136] R10: 00000000ffff0a00 R11: ffffffff9f0df609 R12: 0003000800000032  

[ 8199.736140] R13: ffff9dcdc890ea00 R14: ffff9dcdc890fe00 R15: 0000000000000000  

[ 8199.736145] FS: 00000000021503c0(0000) GS:ffff9dce2eb00000(0000) knlGS:0000000000000000  

[ 8199.736149] CS: 0010 DS: 0000 ES: 0000 CR0: 0000000080050033  

[ 8199.736153] CR2: 00007a9943f24950 CR3: 000000040889a001 CR4: 00000000003606e0  

[ 8199.736157] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000  

[ 8199.736161] DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400  

[ 8199.736164] Call Trace:  

[ 8199.736176] create\_clone+0x11a/0x183  

[ 8199.736185] i915\_user\_extensions+0xc2/0x120  

[ 8199.736194] i915\_gem\_context\_create\_ioctl+0x13e/0x1c4  

[ 8199.736203] drm\_ioctl\_kernel+0x130/0x1c1  

[ 8199.736209] ? i915\_gem\_user\_to\_context\_sseu+0x180/0x180  

[ 8199.736216] drm\_ioctl+0x213/0x3d5  

[ 8199.736223] ? i915\_gem\_user\_to\_context\_sseu+0x180/0x180  

[ 8199.736235] do\_vfs\_ioctl+0x173/0x317  

[ 8199.736242] \_\_x64\_sys\_ioctl+0x57/0x82  

[ 8199.736250] do\_syscall\_64+0x56/0xd4  

[ 8199.736259] entry\_SYSCALL\_64\_after\_hwframe+0x5c/0xc1

**CREDIT INFORMATION**  

Reporter credit: [lovepink]

## Attachments

- [create_clone.diff](attachments/create_clone.diff) (text/plain, 1.7 KB)
- [drm_poc.c](attachments/drm_poc.c) (text/plain, 4.1 KB)

## Timeline

### [Deleted User] (2023-04-15)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-18)

[Empty comment from Monorail migration]

[Monorail blocking: b/278655403]

### ch...@google.com (2023-04-18)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/278655403). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-25)

The change has been forklifted to chromeos-5.10. crrev/c/4448746 is for chromeos-5.4.

Explain how/why your merge fits within the Merge Decision Guidelines?
It fixes a security issue in the i915 kernel driver
Links to the CLs you are requesting to merge.
M112: crrev/c/4450250
M113: crrev/c/4450251
Has the change landed and been verified on ToT? If so, explain what testing has been done to limit the risk of regressions.
It has landed and been verified on ToT.
It removes an i915 kernel uapi that has no user in cros and is considered low risk
Does this change need to be merged into other active release branches (M-1, M+1)?
It should be merged into M112 and M113
Has your Eng Prod Representative approved (in any form) that testing for this change can be accommodated? (if this merge would change/add to the required testing)
NA
Why are these changes required in this milestone after branch?
It fixes a security issue
Is this a new/unlaunched/in-development feature or a bug fix related to a new/unlaunched/in-development feature in any way?
No
Does this change have the potential to impact released devices? If the request is specific to an unreleased device, but the cherry-pick is not going to land in a model-specific directory, please CC a member of the SIE team to LGTM that the change will not impact any released devices.
It affects all intel boards with 5.4 kernel: volteer, dedede, eve, nami, etc.

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

chmiel@ can you please work with someone on the OS security side to get a severity label for this issue ASAP and NLT EOD Monday? Thank you. 

### am...@chromium.org (2023-04-28)

This issue is in the upstream gpu driver, so Chrome CNA would not be the appropriate issuer of a CVE for this issue, removing release label 

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-02)

please see https://crbug.com/chromium/1433460#c11 

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### ha...@google.com (2023-05-03)

Severity label pending -- awaiting response to comment in issuetracker

### pi...@gmail.com (2023-05-03)

Hi @hardikgoyal,  I have replied your question in the issuetracker, please have a check. Thanks

### pi...@gmail.com (2023-05-10)

[Comment Deleted]

### pi...@gmail.com (2023-05-10)

[Comment Deleted]

### ch...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations on another one, lovepink! The VRP Panel has decided to award you $10,000 for this report, based on this issue being in the GPU driver, but mitigated by a race condition. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-01)

This issue was migrated from crbug.com/chromium/1433460?no_tracker_redirect=1

[Monorail blocking: b/278655403]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064061)*
