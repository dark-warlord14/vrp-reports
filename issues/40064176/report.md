# Security: Chrome OS amd drm gpu driver UAF bug in amdgpu_sched_ioctl which can be triggered from chrome browser context

| Field | Value |
|-------|-------|
| **Issue ID** | [40064176](https://issues.chromium.org/issues/40064176) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2023-04-23 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Lenovo ThinkPad C13 Yoga Chromebook is using amd graphics card, the driver is amd drm gpu driver. The zork board's latest kernel version is 5.4.

In amd drm gpu driver, there is an ioctl handler called amdgpu\_sched\_ioctl.  

DRM\_IOCTL\_DEF\_DRV(AMDGPU\_SCHED, amdgpu\_sched\_ioctl, DRM\_MASTER), <---- chrome browser is master  

You can see, it needs DRM\_MASTER to call, but chrome brower process itself is the master, so this bug can be triggered from browser context.

In amdgpu\_sched\_ioctl, it will call amdgpu\_sched\_process\_priority\_override which accept a fd from userspace argument.  

amdgpu\_sched\_process\_priority\_override will iterate all ctx objects from that fd file, but it doesn't obtain the refcount of ctx first. So another thread can call amdgpu\_ctx\_ioctl to free ctx objects.  

And because we can alloc many ctx objects, so it's easy to make a big iterate loop which will provide wide race time window.

static int amdgpu\_sched\_process\_priority\_override(struct amdgpu\_device \*adev,  

int fd,  

enum drm\_sched\_priority priority)  

{  

struct fd f = fdget(fd); <----- get file from input fd  

struct amdgpu\_fpriv \*fpriv;  

struct amdgpu\_ctx \*ctx;  

uint32\_t id;  

int r;

```
if (!f.file)  
	return -EINVAL;  

r = amdgpu_file_to_fpriv(f.file, &fpriv); <------ this file should be amd drm gpu file  
if (r) {  
	fdput(f);  
	return r;  
}  

idr_for_each_entry(&fpriv->ctx_mgr.ctx_handles, ctx, id)  
	amdgpu_ctx_priority_override(ctx, priority); <------ iter all ctx objects, but without get refcount  

fdput(f);  
return 0;  

```

}

amdgpu\_ctx\_ioctl can alloc and free ctx objects:

```
switch (args->in.op) {  
case AMDGPU_CTX_OP_ALLOC_CTX:  
	r = amdgpu_ctx_alloc(adev, fpriv, filp, priority, &id);  
	args->out.alloc.ctx_id = id;  
	break;  
case AMDGPU_CTX_OP_FREE_CTX:  
	r = amdgpu_ctx_free(fpriv, id);  

```

How to prove the chrome browser is the master of drm?  

I add a log in kernel function drm\_new\_set\_master in attached diff file.  

When chrome os start, the chrome browser will trigger this function to be master:

localhost /home/chronos/user # dmesg -w | grep poc  

[ 1.575639] [poc] drm\_new\_set\_master become master current->comm=[frecon], pid=466  

[ 3.474934] [poc] drm\_new\_set\_master become master current->comm=[chrome], pid=1738  

[ 3.475150] [poc] drm\_new\_set\_master become master current->comm=[chrome], pid=1738

**VERSION**  

Lenovo ThinkPad C13 Yoga Chromebook , zork, 112.0.5615.134  

v5.4 kernel latest code

**REPRODUCTION CASE**

For convinent, I add a patch to drm driver, let our poc process to be master, after this, we can run the poc with chronos shell user:  

1, build with the attached kernel diff and flash to chromebook  

2, build the poc, and run it with chronos shell user, the kernel will crash

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

[ 120.481823] general protection fault: 0000 [#1] PREEMPT SMP NOPTI  

[ 120.481831] CPU: 5 PID: 4156 Comm: drm\_poc Not tainted 5.4.240-20638-gbc4b527279cb-dirty #14  

[ 120.481833] Hardware name: Google Morphius/Morphius, BIOS Google\_Morphius.13434.356.0 05/17/2021  

[ 120.481838] RIP: 0010:drm\_sched\_entity\_set\_priority+0x38/0x93  

[ 120.481840] Code: 41 89 f7 49 89 fe 48 8d 5f 24 48 89 df e8 b4 7f 45 00 41 83 7e 20 00 4d 63 ff 74 2a 31 c0 4b 8d 0c bf 49 8b 56 18 48 8b 34 c2 <48> 8b 76 08 48 8d 34 ce 48 83 c6 20 48 89 34 c2 48 ff c0 41 8b 56  

[ 120.481842] RSP: 0018:ffffa0ecc1eafc88 EFLAGS: 00010246  

[ 120.481844] RAX: 0000000000000000 RBX: ffff8c98b18532b4 RCX: 0000000000000005  

[ 120.481846] RDX: ffff8c98b1ea5880 RSI: d2e1931dd7aed152 RDI: ffff8c98b18532b4  

[ 120.481847] RBP: ffffa0ecc1eafca0 R08: ffff8c98b1853150 R09: 0000000000000437  

[ 120.481848] R10: 0000000000000000 R11: ffff8c98fe624000 R12: ffff8c994f00df01  

[ 120.481850] R13: 0000000000000718 R14: ffff8c98b1853290 R15: 0000000000000001  

[ 120.481852] FS: 00000000022653c0(0000) GS:ffff8c99a6f40000(0000) knlGS:0000000000000000  

[ 120.481853] CS: 0010 DS: 0000 ES: 0000 CR0: 0000000080050033  

[ 120.481855] CR2: 00000000004da000 CR3: 00000001316a8000 CR4: 00000000003406e0  

[ 120.481856] Call Trace:  

[ 120.481862] amdgpu\_ctx\_priority\_override+0x35/0x4c  

[ 120.481865] amdgpu\_sched\_ioctl+0xb8/0x173  

[ 120.481867] ? amdgpu\_to\_sched\_priority+0x69/0x69  

[ 120.481871] drm\_ioctl\_kernel+0xdb/0x148  

[ 120.481873] drm\_ioctl+0x213/0x3d5  

[ 120.481875] ? amdgpu\_to\_sched\_priority+0x69/0x69  

[ 120.481877] amdgpu\_drm\_ioctl+0x49/0x7d  

[ 120.481880] do\_vfs\_ioctl+0x173/0x317  

[ 120.481882] \_\_x64\_sys\_ioctl+0x57/0x82  

[ 120.481884] do\_syscall\_64+0x56/0xd4  

[ 120.481888] entry\_SYSCALL\_64\_after\_hwframe+0x5c/0xc1  

[ 120.481890] Modules linked in: dm\_integrity async\_xor xor async\_tx 8021q ccm uinput veth xt\_cgroup iio\_trig\_hrtimer industrialio\_sw\_trigger xt\_MASQUERADE kvm\_amd industrialio\_configfs ccp snd\_acp3x\_pcm\_dma snd\_acp3x\_i2s snd\_soc\_rt5682\_i2c snd\_soc\_rt5682 snd\_soc\_rl6231 snd\_hda\_codec\_hdmi snd\_soc\_cros\_ec\_codec i2c\_cros\_ec\_tunnel snd\_soc\_acp\_rt5682\_mach acpi\_als snd\_hda\_intel snd\_intel\_dspcfg snd\_hda\_codec snd\_hwdep snd\_hda\_core snd\_pci\_acp3x snd\_soc\_max98357a i2c\_piix4 ip6table\_nat fuse rtw88\_8822ce rtw88\_pci rtw88\_8822c rtw88\_core uvcvideo videobuf2\_vmalloc videobuf2\_memops videobuf2\_v4l2 videobuf2\_common iio\_trig\_sysfs mac80211 cros\_ec\_lid\_angle cros\_ec\_sensors cros\_ec\_sensors\_core cfg80211 industrialio\_triggered\_buffer kfifo\_buf industrialio cros\_ec\_sensorhub lzo\_rle lzo\_compress zram btusb btrtl btintel btbcm bluetooth ecdh\_generic ecc joydev  

[ 120.488220] gsmi: Log Shutdown Reason 0x03  

[ 120.488243] ---[ end trace 26e95f0d3a5dccbd ]---

**CREDIT INFORMATION**

Reporter credit: [lovepink]

## Attachments

- [drm_auth.diff](attachments/drm_auth.diff) (text/plain, 935 B)
- [drm_poc.c](attachments/drm_poc.c) (text/plain, 3.8 KB)

## Timeline

### pi...@gmail.com (2023-04-23)

code link:
https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v5.4/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c;drc=f867723b41f871c88388462c007976bb9a4c72da;l=75

### [Deleted User] (2023-04-23)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

Hi leonwinter@ can you please help triage or investigate this UAF bug in ChromeOS? Thanks. 

[Monorail components: Internals>GPU>Internals]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-24)

Adding some ChromeOS GPU friends. Can one of you please take a look? Thanks! Feel free to CC or assign to anyone relevant.

### ol...@chromium.org (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-04-26)

I put up https://lore.kernel.org/dri-devel/20230426004831.650908-1-olvaffe@gmail.com/ for review.

### gi...@appspot.gserviceaccount.com (2023-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/99e5b350fe4d35c41f50d0680b868d1aee2a728a

commit 99e5b350fe4d35c41f50d0680b868d1aee2a728a
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: Idae1ce9f78318b2c7c82dd1b2490679d4782e2f8
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4501725
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Chia-I Wu <olv@google.com>
Commit-Queue: Chia-I Wu <olv@google.com>
Auto-Submit: Chia-I Wu <olv@google.com>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>

[modify] https://crrev.com/99e5b350fe4d35c41f50d0680b868d1aee2a728a/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gi...@appspot.gserviceaccount.com (2023-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/e8bc8d786e7f6e979d3743caf428a8b9c6f44799

commit e8bc8d786e7f6e979d3743caf428a8b9c6f44799
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: Id1578c688f69e83552dc798b7ff89192ff9e483e
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4503871
Tested-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Auto-Submit: Chia-I Wu <olv@google.com>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/e8bc8d786e7f6e979d3743caf428a8b9c6f44799/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gi...@appspot.gserviceaccount.com (2023-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/49b8b42a2634a1dcd1ed1341a9c5018865b9b3ef

commit 49b8b42a2634a1dcd1ed1341a9c5018865b9b3ef
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: I626ddc10f88acb357ba414b2a813158917f0f0f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4501324
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Chia-I Wu <olv@google.com>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Auto-Submit: Chia-I Wu <olv@google.com>

[modify] https://crrev.com/49b8b42a2634a1dcd1ed1341a9c5018865b9b3ef/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### ol...@chromium.org (2023-05-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-04)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-05-04)

1. Why does your merge fit within the merge criteria for these milestones?
They fix a security issue in kernel amdgpu driver.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4507240
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4507241
https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4507242

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
NA.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No.

### ce...@google.com (2023-05-05)

Merge approved for M-114.

Merge Category: Non-performance Regression.

### gi...@appspot.gserviceaccount.com (2023-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/d6447a7dca06e66958fa6152c38af5bd43341075

commit d6447a7dca06e66958fa6152c38af5bd43341075
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: Idae1ce9f78318b2c7c82dd1b2490679d4782e2f8
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4501725
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Chia-I Wu <olv@google.com>
Commit-Queue: Chia-I Wu <olv@google.com>
Auto-Submit: Chia-I Wu <olv@google.com>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
(cherry picked from commit 99e5b350fe4d35c41f50d0680b868d1aee2a728a)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4507240
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/d6447a7dca06e66958fa6152c38af5bd43341075/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gi...@appspot.gserviceaccount.com (2023-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/daf860182ca331d50c19a12ca12f35edeb04efce

commit daf860182ca331d50c19a12ca12f35edeb04efce
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: Id1578c688f69e83552dc798b7ff89192ff9e483e
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4503871
Tested-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Auto-Submit: Chia-I Wu <olv@google.com>
Reviewed-by: Sean Paul <sean@poorly.run>
(cherry picked from commit e8bc8d786e7f6e979d3743caf428a8b9c6f44799)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4507241
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/daf860182ca331d50c19a12ca12f35edeb04efce/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gi...@appspot.gserviceaccount.com (2023-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/2facec2a7d29e456a9a0f43392fc4a419cb66bb0

commit 2facec2a7d29e456a9a0f43392fc4a419cb66bb0
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: I626ddc10f88acb357ba414b2a813158917f0f0f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4501324
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Chia-I Wu <olv@google.com>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Auto-Submit: Chia-I Wu <olv@google.com>
(cherry picked from commit 49b8b42a2634a1dcd1ed1341a9c5018865b9b3ef)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4507242
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/2facec2a7d29e456a9a0f43392fc4a419cb66bb0/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### ol...@chromium.org (2023-05-05)

Fixed on M114 and ToT.

### ol...@chromium.org (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ol...@chromium.org (2023-05-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### ol...@chromium.org (2023-05-23)

FWIW, only the browser process can make the ioctl in question.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations on another one, lovepink! The VRP Panel has decided to award you $10,000 for this report based on this issue being mildly mitigated by race condition. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-07-05)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-05)

[Empty comment from Monorail migration]

### mf...@google.com (2023-07-24)

[Empty comment from Monorail migration]

### mf...@google.com (2023-07-26)

[Empty comment from Monorail migration]

### mf...@google.com (2023-08-07)

Re #31:

LTS Milestone M108 merge request:

1. security issue.
2. no



### mf...@google.com (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@google.com (2023-08-10)

Re #38:
1. security.
2. https://chromium-review.googlesource.com/q/change:4739746+OR+change:4739745+OR+change:4738490
3. yes
4. no
5. no
6. no

### gm...@google.com (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/7ecd0b12d93698b300448916dcbe3a2f7baa8dde

commit 7ecd0b12d93698b300448916dcbe3a2f7baa8dde
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: Id1578c688f69e83552dc798b7ff89192ff9e483e
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4503871
Tested-by: Chia-I Wu <olv@google.com>
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Auto-Submit: Chia-I Wu <olv@google.com>
Reviewed-by: Sean Paul <sean@poorly.run>
(cherry picked from commit e8bc8d786e7f6e979d3743caf428a8b9c6f44799)
Signed-off-by: Martin Faltesek <mfaltesek@google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4738490
Reviewed-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/7ecd0b12d93698b300448916dcbe3a2f7baa8dde/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/1d860065f89135a5345a86d8764aef0ccc40fea6

commit 1d860065f89135a5345a86d8764aef0ccc40fea6
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: Idae1ce9f78318b2c7c82dd1b2490679d4782e2f8
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4501725
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Chia-I Wu <olv@google.com>
Commit-Queue: Chia-I Wu <olv@google.com>
Auto-Submit: Chia-I Wu <olv@google.com>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Commit-Queue: Rob Clark <robdclark@chromium.org>
(cherry picked from commit 99e5b350fe4d35c41f50d0680b868d1aee2a728a)
Signed-off-by: Martin Faltesek <mfaltesek@google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4739746
Reviewed-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/1d860065f89135a5345a86d8764aef0ccc40fea6/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/195816c312c3c72997dd19d776d3d6fb7365a1f1

commit 195816c312c3c72997dd19d776d3d6fb7365a1f1
Author: Chia-I Wu <olvaffe@gmail.com>
Date: Wed Apr 26 22:54:55 2023

FROMGIT: drm/amdgpu: add a missing lock for AMDGPU_SCHED

mgr->ctx_handles should be protected by mgr->lock.

v2: improve commit message
v3: add a Fixes tag

Signed-off-by: Chia-I Wu <olvaffe@gmail.com>
Reviewed-by: Christian König <christian.koenig@amd.com>
Fixes: 52c6a62c64fa ("drm/amdgpu: add interface for editing a foreign process's priority v3")
Signed-off-by: Alex Deucher <alexander.deucher@amd.com>
(cherry picked from commit a890efed1dc45af258c2d632bc3bb29198813e71
 https://gitlab.freedesktop.org/agd5f/linux.git drm-next)

BUG=chromium:1436790
TEST=CQ

Change-Id: I626ddc10f88acb357ba414b2a813158917f0f0f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4501324
Commit-Queue: Rob Clark <robdclark@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Tested-by: Chia-I Wu <olv@google.com>
Reviewed-by: Rob Clark <robdclark@chromium.org>
Auto-Submit: Chia-I Wu <olv@google.com>
(cherry picked from commit 49b8b42a2634a1dcd1ed1341a9c5018865b9b3ef)
Signed-off-by: Martin Faltesek <mfaltesek@google.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4739745
Reviewed-by: Guenter Roeck <groeck@chromium.org>

[modify] https://crrev.com/195816c312c3c72997dd19d776d3d6fb7365a1f1/drivers/gpu/drm/amd/amdgpu/amdgpu_sched.c


### gm...@google.com (2023-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-11)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-15)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1436790?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064176)*
