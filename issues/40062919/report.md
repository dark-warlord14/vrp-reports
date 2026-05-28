# Security: Race Condition UAF in hci_cmd_sync_work

| Field | Value |
|-------|-------|
| **Issue ID** | [40062919](https://issues.chromium.org/issues/40062919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ap...@chromium.org |
| **Created** | 2023-02-05 |
| **Bounty** | $8,500.00 |

## Description

**VULNERABILITY DETAILS**

The root cause of this issue is similar to <https://crbug.com/chromium/1355718>, race condition UAF.

\*hci\_cmd\_sync\_queue\* will check the flag of hdev not equal to \*HCI\_UNREGISTER\*[1], and enqueue \*hdev->cmd\_sync\_work\*(which is \*hci\_cmd\_sync\_work\*)[2]. \*hci\_cmd\_sync\_work\* will get entry[3] from \*hdev->cmd\_sync\_work\_list\*, and remove it from \*hdev->cmd\_sync\_work\_list\* under \*hdev->cmd\_sync\_work\_lock\*. But \*hci\_cmd\_sync\_clear\* get entry from \*hdev->cmd\_sync\_work\_list\* and delete it[4] without any lock. There will be a race condition between \*hci\_cmd\_sync\_work\* and \*hci\_cmd\_sync\_clear\*.

```
int hci_cmd_sync_queue(struct hci_dev \*hdev, hci_cmd_sync_work_func_t func,  
		       void \*data, hci_cmd_sync_work_destroy_t destroy)  
{  
	struct hci_cmd_sync_work_entry \*entry;  
  
	if (hci_dev_test_flag(hdev, HCI_UNREGISTER))	// [1]  
		return -ENODEV;  
  
	entry = kmalloc(sizeof(\*entry), GFP_KERNEL);  
	if (!entry)  
		return -ENOMEM;  
  
	entry->func = func;  
	entry->data = data;  
	entry->destroy = destroy;  
  
	mutex_lock(&hdev->cmd_sync_work_lock);  
	list_add_tail(&entry->list, &hdev->cmd_sync_work_list);  
	mutex_unlock(&hdev->cmd_sync_work_lock);  
  
	queue_work(hdev->req_workqueue, &hdev->cmd_sync_work);	// [2]  
  
	return 0;  
}  
  
static void hci_cmd_sync_work(struct work_struct \*work)  
{  
	struct hci_dev \*hdev = container_of(work, struct hci_dev, cmd_sync_work);  
  
	bt_dev_dbg(hdev, "");  
  
	/\* Dequeue all entries and run them \*/  
	while (1) {  
		struct hci_cmd_sync_work_entry \*entry;  
  
		mutex_lock(&hdev->cmd_sync_work_lock);  
		entry = list_first_entry_or_null(&hdev->cmd_sync_work_list,		// [3]  
						 struct hci_cmd_sync_work_entry,  
						 list);  
		if (entry)  
			list_del(&entry->list);  
		mutex_unlock(&hdev->cmd_sync_work_lock);  
  
		if (!entry)  
			break;  
  
		bt_dev_dbg(hdev, "entry %p", entry);  
  
		if (entry->func) {  
			int err;  
  
			hci_req_sync_lock(hdev);  
			err = entry->func(hdev, entry->data);  
			if (entry->destroy)  
				entry->destroy(hdev, entry->data, err);  
			hci_req_sync_unlock(hdev);  
		}  
  
		kfree(entry);  
	}  
}  
  
void hci_cmd_sync_clear(struct hci_dev \*hdev)  
{  
	struct hci_cmd_sync_work_entry \*entry, \*tmp;  
  
	cancel_work_sync(&hdev->cmd_sync_work);  
	cancel_work_sync(&hdev->reenable_adv_work);  
  
	list_for_each_entry_safe(entry, tmp, &hdev->cmd_sync_work_list, list) {  
		if (entry->destroy)  
			entry->destroy(hdev, entry->data, -ECANCELED);  
  
		list_del(&entry->list);  
		kfree(entry);		// [4]  
	}  
}  

```

hci\_cmd\_sync\_queue | hci\_unregister\_dev  

hci\_dev\_test\_flag(hdev, HCI\_UNREGISTER) [1] |  

| hci\_dev\_set\_flag(hdev, HCI\_UNREGISTER)  

| hci\_cmd\_sync\_clear  

| cancel\_work\_sync(&hdev->cmd\_sync\_work)  

queue\_work[2] |  

hci\_cmd\_sync\_work |  

list\_first\_entry\_or\_null [3] |  

| kfree(entry) [4]  

list\_del(&entry->list) <--- UAF

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=689>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=704>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=288>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=651>

**VERSION**  

Operating System: ChromiumOS Kernel 6.1 stable + dev

Bisect:  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/6a98e3836fa2077b169f10a35c2ca9952d53f987>

**REPRODUCTION CASE**

The time window is very small, please apply the patch which just expands the time window.

```
diff --git a/net/bluetooth/hci_sync.c b/net/bluetooth/hci_sync.c  
index 2337a1c4827d..60f961ebcfeb 100644  
--- a/net/bluetooth/hci_sync.c  
+++ b/net/bluetooth/hci_sync.c  
@@ -288,6 +288,7 @@ static void hci_cmd_sync_work(struct work_struct \*work)  
                entry = list_first_entry_or_null(&hdev->cmd_sync_work_list,  
                                                 struct hci_cmd_sync_work_entry,  
                                                 list);  
+               msleep(20);  
                if (entry)  
                        list_del(&entry->list);  
                mutex_unlock(&hdev->cmd_sync_work_lock);  
@@ -642,7 +643,7 @@ void hci_cmd_sync_clear(struct hci_dev \*hdev)  
   
        cancel_work_sync(&hdev->cmd_sync_work);  
        cancel_work_sync(&hdev->reenable_adv_work);  
-  
+       msleep(110);  
        list_for_each_entry_safe(entry, tmp, &hdev->cmd_sync_work_list, list) {  
                if (entry->destroy)  
                        entry->destroy(hdev, entry->data, -ECANCELED);  
@@ -700,7 +701,7 @@ int hci_cmd_sync_queue(struct hci_dev \*hdev, hci_cmd_sync_work_func_t func,  
        mutex_lock(&hdev->cmd_sync_work_lock);  
        list_add_tail(&entry->list, &hdev->cmd_sync_work_list);  
        mutex_unlock(&hdev->cmd_sync_work_lock);  
-  
+       msleep(100);  
        queue_work(hdev->req_workqueue, &hdev->cmd_sync_work);  
   
        return 0;  

```

1. Compile the poc.
2. Run poc in ChromiumOS system. It needs CAP\_NET\_ADMIN privilege.

FIX PATCH SUGGESTION  

I think the follwing patch should fix the problem.

```
diff --git a/net/bluetooth/hci_sync.c b/net/bluetooth/hci_sync.c  
index 2337a1c4827d..ed141c7a47fb 100644  
--- a/net/bluetooth/hci_sync.c  
+++ b/net/bluetooth/hci_sync.c  
@@ -643,6 +643,7 @@ void hci_cmd_sync_clear(struct hci_dev \*hdev)  
        cancel_work_sync(&hdev->cmd_sync_work);  
        cancel_work_sync(&hdev->reenable_adv_work);  
   
+       mutex_lock(&hdev->cmd_sync_work_lock);  
        list_for_each_entry_safe(entry, tmp, &hdev->cmd_sync_work_list, list) {  
                if (entry->destroy)  
                        entry->destroy(hdev, entry->data, -ECANCELED);  
@@ -650,6 +651,7 @@ void hci_cmd_sync_clear(struct hci_dev \*hdev)  
                list_del(&entry->list);  
                kfree(entry);  
        }  
+       mutex_unlock(&hdev->cmd_sync_work_lock);  
 }  
   
 void __hci_cmd_sync_cancel(struct hci_dev \*hdev, int err)  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: kernel crash  

Crash State: please see the kasan.log

Ref Link:  

<https://www.openwall.com/lists/oss-security/2021/06/08/2>

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 9.1 KB)
- [kasan.log](attachments/kasan.log) (text/plain, 5.6 KB)
- [kasan.log](attachments/kasan.log) (text/plain, 4.1 KB)

## Timeline

### [Deleted User] (2023-02-05)

[Empty comment from Monorail migration]

### lm...@gmail.com (2023-02-06)

Hi, here is a more clear kasan.log with allocated/freed stack.

### fl...@google.com (2023-02-06)

=> forwarding to ChromeOS triage queue

### lz...@google.com (2023-02-09)

So this is a race condition in kernel/bluetooth. From a quick glance, hci_cmd_sync_clear is used to reset everything. In practice no hci_cmd_sync_work will likely start before hci_sync_clear ends. Have you considered to raise this point to the v6.1 kernel maillist?

### lm...@gmail.com (2023-02-10)

Hello, sir, I'm not sure if reporting this to the v6.1 kernel maillist violates the VRP rule. If not, I'm glad to report this to the v6.1 kernel maillist for fix.

### lm...@gmail.com (2023-02-15)

Hello, is that fine to report this to security@kernel.org? Looking forward to your reply.

### lm...@gmail.com (2023-02-16)

Hi, I have submitted this to security@kernel.org for repair. If there is any new repair progress, I will sync it here.

### pa...@chromium.org (2023-02-16)

Sorry for the slow response. Thanks for reporting it here and upstream!

[Monorail components: Platform]

### lm...@gmail.com (2023-03-08)

Hi, here is the patch, and has been applied to bluetooth/bluetooth-next.git

https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git/commit/?id=83ce39248d6d

### en...@google.com (2023-03-13)

Assigning owner based on similar bugs linked in the description. Please let me know if the owner is incorrect by assigning it to me or the correct owner.

### ap...@chromium.org (2023-03-14)

Thanks! I will cherry-pick the fix.
Btw, what is the next step after that? Should I just close the issue or reassign to someone else?

### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/16cd89427273230c51046c4696d231a9d460c18c

commit 16cd89427273230c51046c4696d231a9d460c18c
Author: Min Li <lm0963hack@gmail.com>
Date: Sat Mar 04 13:50:35 2023

FROMGIT: Bluetooth: Fix race condition in hci_cmd_sync_clear

There is a potential race condition in hci_cmd_sync_work and
hci_cmd_sync_clear, and could lead to use-after-free. For instance,
hci_cmd_sync_work is added to the 'req_workqueue' after cancel_work_sync
The entry of 'cmd_sync_work_list' may be freed in hci_cmd_sync_clear, and
causing kernel panic when it is used in 'hci_cmd_sync_work'.

Here's the call trace:

dump_stack_lvl+0x49/0x63
print_report.cold+0x5e/0x5d3
? hci_cmd_sync_work+0x282/0x320
kasan_report+0xaa/0x120
? hci_cmd_sync_work+0x282/0x320
__asan_report_load8_noabort+0x14/0x20
hci_cmd_sync_work+0x282/0x320
process_one_work+0x77b/0x11c0
? _raw_spin_lock_irq+0x8e/0xf0
worker_thread+0x544/0x1180
? poll_idle+0x1e0/0x1e0
kthread+0x285/0x320
? process_one_work+0x11c0/0x11c0
? kthread_complete_and_exit+0x30/0x30
ret_from_fork+0x22/0x30
</TASK>

Allocated by task 266:
kasan_save_stack+0x26/0x50
__kasan_kmalloc+0xae/0xe0
kmem_cache_alloc_trace+0x191/0x350
hci_cmd_sync_queue+0x97/0x2b0
hci_update_passive_scan+0x176/0x1d0
le_conn_complete_evt+0x1b5/0x1a00
hci_le_conn_complete_evt+0x234/0x340
hci_le_meta_evt+0x231/0x4e0
hci_event_packet+0x4c5/0xf00
hci_rx_work+0x37d/0x880
process_one_work+0x77b/0x11c0
worker_thread+0x544/0x1180
kthread+0x285/0x320
ret_from_fork+0x22/0x30

Freed by task 269:
kasan_save_stack+0x26/0x50
kasan_set_track+0x25/0x40
kasan_set_free_info+0x24/0x40
____kasan_slab_free+0x176/0x1c0
__kasan_slab_free+0x12/0x20
slab_free_freelist_hook+0x95/0x1a0
kfree+0xba/0x2f0
hci_cmd_sync_clear+0x14c/0x210
hci_unregister_dev+0xff/0x440
vhci_release+0x7b/0xf0
__fput+0x1f3/0x970
____fput+0xe/0x20
task_work_run+0xd4/0x160
do_exit+0x8b0/0x22a0
do_group_exit+0xba/0x2a0
get_signal+0x1e4a/0x25b0
arch_do_signal_or_restart+0x93/0x1f80
exit_to_user_mode_prepare+0xf5/0x1a0
syscall_exit_to_user_mode+0x26/0x50
ret_from_fork+0x15/0x30

Fixes: 6a98e3836fa2 ("Bluetooth: Add helper for serialized HCI command execution")
Cc: stable@vger.kernel.org
Signed-off-by: Min Li <lm0963hack@gmail.com>
Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 83ce39248d6dd78db72525a52733ac1b392bb151 https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git master)

BUG=chromium:1413031
TEST=build

Signed-off-by: Archie Pusaka <apusaka@chromium.org>
Change-Id: I266e7233cc9164b1b3243ed510251ebef9602b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4335059
Reviewed-by: Yun-Hao Chung <howardchung@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/16cd89427273230c51046c4696d231a9d460c18c/net/bluetooth/hci_sync.c


### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/9f9f62fa340ce6618d8ff4cf3d061be17b641463

commit 9f9f62fa340ce6618d8ff4cf3d061be17b641463
Author: Min Li <lm0963hack@gmail.com>
Date: Sat Mar 04 13:50:35 2023

FROMGIT: Bluetooth: Fix race condition in hci_cmd_sync_clear

There is a potential race condition in hci_cmd_sync_work and
hci_cmd_sync_clear, and could lead to use-after-free. For instance,
hci_cmd_sync_work is added to the 'req_workqueue' after cancel_work_sync
The entry of 'cmd_sync_work_list' may be freed in hci_cmd_sync_clear, and
causing kernel panic when it is used in 'hci_cmd_sync_work'.

Here's the call trace:

dump_stack_lvl+0x49/0x63
print_report.cold+0x5e/0x5d3
? hci_cmd_sync_work+0x282/0x320
kasan_report+0xaa/0x120
? hci_cmd_sync_work+0x282/0x320
__asan_report_load8_noabort+0x14/0x20
hci_cmd_sync_work+0x282/0x320
process_one_work+0x77b/0x11c0
? _raw_spin_lock_irq+0x8e/0xf0
worker_thread+0x544/0x1180
? poll_idle+0x1e0/0x1e0
kthread+0x285/0x320
? process_one_work+0x11c0/0x11c0
? kthread_complete_and_exit+0x30/0x30
ret_from_fork+0x22/0x30
</TASK>

Allocated by task 266:
kasan_save_stack+0x26/0x50
__kasan_kmalloc+0xae/0xe0
kmem_cache_alloc_trace+0x191/0x350
hci_cmd_sync_queue+0x97/0x2b0
hci_update_passive_scan+0x176/0x1d0
le_conn_complete_evt+0x1b5/0x1a00
hci_le_conn_complete_evt+0x234/0x340
hci_le_meta_evt+0x231/0x4e0
hci_event_packet+0x4c5/0xf00
hci_rx_work+0x37d/0x880
process_one_work+0x77b/0x11c0
worker_thread+0x544/0x1180
kthread+0x285/0x320
ret_from_fork+0x22/0x30

Freed by task 269:
kasan_save_stack+0x26/0x50
kasan_set_track+0x25/0x40
kasan_set_free_info+0x24/0x40
____kasan_slab_free+0x176/0x1c0
__kasan_slab_free+0x12/0x20
slab_free_freelist_hook+0x95/0x1a0
kfree+0xba/0x2f0
hci_cmd_sync_clear+0x14c/0x210
hci_unregister_dev+0xff/0x440
vhci_release+0x7b/0xf0
__fput+0x1f3/0x970
____fput+0xe/0x20
task_work_run+0xd4/0x160
do_exit+0x8b0/0x22a0
do_group_exit+0xba/0x2a0
get_signal+0x1e4a/0x25b0
arch_do_signal_or_restart+0x93/0x1f80
exit_to_user_mode_prepare+0xf5/0x1a0
syscall_exit_to_user_mode+0x26/0x50
ret_from_fork+0x15/0x30

Fixes: 6a98e3836fa2 ("Bluetooth: Add helper for serialized HCI command execution")
Cc: stable@vger.kernel.org
Signed-off-by: Min Li <lm0963hack@gmail.com>
Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 83ce39248d6dd78db72525a52733ac1b392bb151 https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git master)

BUG=chromium:1413031
TEST=build

Signed-off-by: Archie Pusaka <apusaka@chromium.org>
Change-Id: I266e7233cc9164b1b3243ed510251ebef9602b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4337526
Reviewed-by: Yun-Hao Chung <howardchung@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/9f9f62fa340ce6618d8ff4cf3d061be17b641463/net/bluetooth/hci_sync.c


### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/ae3969b3404d24eaee0627f4eb72008d97eb2bf6

commit ae3969b3404d24eaee0627f4eb72008d97eb2bf6
Author: Min Li <lm0963hack@gmail.com>
Date: Sat Mar 04 13:50:35 2023

FROMGIT: Bluetooth: Fix race condition in hci_cmd_sync_clear

There is a potential race condition in hci_cmd_sync_work and
hci_cmd_sync_clear, and could lead to use-after-free. For instance,
hci_cmd_sync_work is added to the 'req_workqueue' after cancel_work_sync
The entry of 'cmd_sync_work_list' may be freed in hci_cmd_sync_clear, and
causing kernel panic when it is used in 'hci_cmd_sync_work'.

Here's the call trace:

dump_stack_lvl+0x49/0x63
print_report.cold+0x5e/0x5d3
? hci_cmd_sync_work+0x282/0x320
kasan_report+0xaa/0x120
? hci_cmd_sync_work+0x282/0x320
__asan_report_load8_noabort+0x14/0x20
hci_cmd_sync_work+0x282/0x320
process_one_work+0x77b/0x11c0
? _raw_spin_lock_irq+0x8e/0xf0
worker_thread+0x544/0x1180
? poll_idle+0x1e0/0x1e0
kthread+0x285/0x320
? process_one_work+0x11c0/0x11c0
? kthread_complete_and_exit+0x30/0x30
ret_from_fork+0x22/0x30
</TASK>

Allocated by task 266:
kasan_save_stack+0x26/0x50
__kasan_kmalloc+0xae/0xe0
kmem_cache_alloc_trace+0x191/0x350
hci_cmd_sync_queue+0x97/0x2b0
hci_update_passive_scan+0x176/0x1d0
le_conn_complete_evt+0x1b5/0x1a00
hci_le_conn_complete_evt+0x234/0x340
hci_le_meta_evt+0x231/0x4e0
hci_event_packet+0x4c5/0xf00
hci_rx_work+0x37d/0x880
process_one_work+0x77b/0x11c0
worker_thread+0x544/0x1180
kthread+0x285/0x320
ret_from_fork+0x22/0x30

Freed by task 269:
kasan_save_stack+0x26/0x50
kasan_set_track+0x25/0x40
kasan_set_free_info+0x24/0x40
____kasan_slab_free+0x176/0x1c0
__kasan_slab_free+0x12/0x20
slab_free_freelist_hook+0x95/0x1a0
kfree+0xba/0x2f0
hci_cmd_sync_clear+0x14c/0x210
hci_unregister_dev+0xff/0x440
vhci_release+0x7b/0xf0
__fput+0x1f3/0x970
____fput+0xe/0x20
task_work_run+0xd4/0x160
do_exit+0x8b0/0x22a0
do_group_exit+0xba/0x2a0
get_signal+0x1e4a/0x25b0
arch_do_signal_or_restart+0x93/0x1f80
exit_to_user_mode_prepare+0xf5/0x1a0
syscall_exit_to_user_mode+0x26/0x50
ret_from_fork+0x15/0x30

Fixes: 6a98e3836fa2 ("Bluetooth: Add helper for serialized HCI command execution")
Cc: stable@vger.kernel.org
Signed-off-by: Min Li <lm0963hack@gmail.com>
Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 83ce39248d6dd78db72525a52733ac1b392bb151 https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git master)

BUG=chromium:1413031
TEST=build

Signed-off-by: Archie Pusaka <apusaka@chromium.org>
Change-Id: I266e7233cc9164b1b3243ed510251ebef9602b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4337602
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Yun-Hao Chung <howardchung@chromium.org>

[modify] https://crrev.com/ae3969b3404d24eaee0627f4eb72008d97eb2bf6/net/bluetooth/hci_sync.c


### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/16cd89427273230c51046c4696d231a9d460c18c

commit 16cd89427273230c51046c4696d231a9d460c18c
Author: Min Li <lm0963hack@gmail.com>
Date: Sat Mar 04 13:50:35 2023

FROMGIT: Bluetooth: Fix race condition in hci_cmd_sync_clear

There is a potential race condition in hci_cmd_sync_work and
hci_cmd_sync_clear, and could lead to use-after-free. For instance,
hci_cmd_sync_work is added to the 'req_workqueue' after cancel_work_sync
The entry of 'cmd_sync_work_list' may be freed in hci_cmd_sync_clear, and
causing kernel panic when it is used in 'hci_cmd_sync_work'.

Here's the call trace:

dump_stack_lvl+0x49/0x63
print_report.cold+0x5e/0x5d3
? hci_cmd_sync_work+0x282/0x320
kasan_report+0xaa/0x120
? hci_cmd_sync_work+0x282/0x320
__asan_report_load8_noabort+0x14/0x20
hci_cmd_sync_work+0x282/0x320
process_one_work+0x77b/0x11c0
? _raw_spin_lock_irq+0x8e/0xf0
worker_thread+0x544/0x1180
? poll_idle+0x1e0/0x1e0
kthread+0x285/0x320
? process_one_work+0x11c0/0x11c0
? kthread_complete_and_exit+0x30/0x30
ret_from_fork+0x22/0x30
</TASK>

Allocated by task 266:
kasan_save_stack+0x26/0x50
__kasan_kmalloc+0xae/0xe0
kmem_cache_alloc_trace+0x191/0x350
hci_cmd_sync_queue+0x97/0x2b0
hci_update_passive_scan+0x176/0x1d0
le_conn_complete_evt+0x1b5/0x1a00
hci_le_conn_complete_evt+0x234/0x340
hci_le_meta_evt+0x231/0x4e0
hci_event_packet+0x4c5/0xf00
hci_rx_work+0x37d/0x880
process_one_work+0x77b/0x11c0
worker_thread+0x544/0x1180
kthread+0x285/0x320
ret_from_fork+0x22/0x30

Freed by task 269:
kasan_save_stack+0x26/0x50
kasan_set_track+0x25/0x40
kasan_set_free_info+0x24/0x40
____kasan_slab_free+0x176/0x1c0
__kasan_slab_free+0x12/0x20
slab_free_freelist_hook+0x95/0x1a0
kfree+0xba/0x2f0
hci_cmd_sync_clear+0x14c/0x210
hci_unregister_dev+0xff/0x440
vhci_release+0x7b/0xf0
__fput+0x1f3/0x970
____fput+0xe/0x20
task_work_run+0xd4/0x160
do_exit+0x8b0/0x22a0
do_group_exit+0xba/0x2a0
get_signal+0x1e4a/0x25b0
arch_do_signal_or_restart+0x93/0x1f80
exit_to_user_mode_prepare+0xf5/0x1a0
syscall_exit_to_user_mode+0x26/0x50
ret_from_fork+0x15/0x30

Fixes: 6a98e3836fa2 ("Bluetooth: Add helper for serialized HCI command execution")
Cc: stable@vger.kernel.org
Signed-off-by: Min Li <lm0963hack@gmail.com>
Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 83ce39248d6dd78db72525a52733ac1b392bb151 https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git master)

BUG=chromium:1413031
TEST=build

Signed-off-by: Archie Pusaka <apusaka@chromium.org>
Change-Id: I266e7233cc9164b1b3243ed510251ebef9602b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4335059
Reviewed-by: Yun-Hao Chung <howardchung@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/16cd89427273230c51046c4696d231a9d460c18c/net/bluetooth/hci_sync.c


### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/ae3969b3404d24eaee0627f4eb72008d97eb2bf6

commit ae3969b3404d24eaee0627f4eb72008d97eb2bf6
Author: Min Li <lm0963hack@gmail.com>
Date: Sat Mar 04 13:50:35 2023

FROMGIT: Bluetooth: Fix race condition in hci_cmd_sync_clear

There is a potential race condition in hci_cmd_sync_work and
hci_cmd_sync_clear, and could lead to use-after-free. For instance,
hci_cmd_sync_work is added to the 'req_workqueue' after cancel_work_sync
The entry of 'cmd_sync_work_list' may be freed in hci_cmd_sync_clear, and
causing kernel panic when it is used in 'hci_cmd_sync_work'.

Here's the call trace:

dump_stack_lvl+0x49/0x63
print_report.cold+0x5e/0x5d3
? hci_cmd_sync_work+0x282/0x320
kasan_report+0xaa/0x120
? hci_cmd_sync_work+0x282/0x320
__asan_report_load8_noabort+0x14/0x20
hci_cmd_sync_work+0x282/0x320
process_one_work+0x77b/0x11c0
? _raw_spin_lock_irq+0x8e/0xf0
worker_thread+0x544/0x1180
? poll_idle+0x1e0/0x1e0
kthread+0x285/0x320
? process_one_work+0x11c0/0x11c0
? kthread_complete_and_exit+0x30/0x30
ret_from_fork+0x22/0x30
</TASK>

Allocated by task 266:
kasan_save_stack+0x26/0x50
__kasan_kmalloc+0xae/0xe0
kmem_cache_alloc_trace+0x191/0x350
hci_cmd_sync_queue+0x97/0x2b0
hci_update_passive_scan+0x176/0x1d0
le_conn_complete_evt+0x1b5/0x1a00
hci_le_conn_complete_evt+0x234/0x340
hci_le_meta_evt+0x231/0x4e0
hci_event_packet+0x4c5/0xf00
hci_rx_work+0x37d/0x880
process_one_work+0x77b/0x11c0
worker_thread+0x544/0x1180
kthread+0x285/0x320
ret_from_fork+0x22/0x30

Freed by task 269:
kasan_save_stack+0x26/0x50
kasan_set_track+0x25/0x40
kasan_set_free_info+0x24/0x40
____kasan_slab_free+0x176/0x1c0
__kasan_slab_free+0x12/0x20
slab_free_freelist_hook+0x95/0x1a0
kfree+0xba/0x2f0
hci_cmd_sync_clear+0x14c/0x210
hci_unregister_dev+0xff/0x440
vhci_release+0x7b/0xf0
__fput+0x1f3/0x970
____fput+0xe/0x20
task_work_run+0xd4/0x160
do_exit+0x8b0/0x22a0
do_group_exit+0xba/0x2a0
get_signal+0x1e4a/0x25b0
arch_do_signal_or_restart+0x93/0x1f80
exit_to_user_mode_prepare+0xf5/0x1a0
syscall_exit_to_user_mode+0x26/0x50
ret_from_fork+0x15/0x30

Fixes: 6a98e3836fa2 ("Bluetooth: Add helper for serialized HCI command execution")
Cc: stable@vger.kernel.org
Signed-off-by: Min Li <lm0963hack@gmail.com>
Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 83ce39248d6dd78db72525a52733ac1b392bb151 https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git master)

BUG=chromium:1413031
TEST=build

Signed-off-by: Archie Pusaka <apusaka@chromium.org>
Change-Id: I266e7233cc9164b1b3243ed510251ebef9602b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4337602
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Yun-Hao Chung <howardchung@chromium.org>

[modify] https://crrev.com/ae3969b3404d24eaee0627f4eb72008d97eb2bf6/net/bluetooth/hci_sync.c


### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/a68f975689e424739a95277141bbb2f37c89a9fc

commit a68f975689e424739a95277141bbb2f37c89a9fc
Author: Min Li <lm0963hack@gmail.com>
Date: Sat Mar 04 13:50:35 2023

FROMGIT: Bluetooth: Fix race condition in hci_cmd_sync_clear

There is a potential race condition in hci_cmd_sync_work and
hci_cmd_sync_clear, and could lead to use-after-free. For instance,
hci_cmd_sync_work is added to the 'req_workqueue' after cancel_work_sync
The entry of 'cmd_sync_work_list' may be freed in hci_cmd_sync_clear, and
causing kernel panic when it is used in 'hci_cmd_sync_work'.

Here's the call trace:

dump_stack_lvl+0x49/0x63
print_report.cold+0x5e/0x5d3
? hci_cmd_sync_work+0x282/0x320
kasan_report+0xaa/0x120
? hci_cmd_sync_work+0x282/0x320
__asan_report_load8_noabort+0x14/0x20
hci_cmd_sync_work+0x282/0x320
process_one_work+0x77b/0x11c0
? _raw_spin_lock_irq+0x8e/0xf0
worker_thread+0x544/0x1180
? poll_idle+0x1e0/0x1e0
kthread+0x285/0x320
? process_one_work+0x11c0/0x11c0
? kthread_complete_and_exit+0x30/0x30
ret_from_fork+0x22/0x30
</TASK>

Allocated by task 266:
kasan_save_stack+0x26/0x50
__kasan_kmalloc+0xae/0xe0
kmem_cache_alloc_trace+0x191/0x350
hci_cmd_sync_queue+0x97/0x2b0
hci_update_passive_scan+0x176/0x1d0
le_conn_complete_evt+0x1b5/0x1a00
hci_le_conn_complete_evt+0x234/0x340
hci_le_meta_evt+0x231/0x4e0
hci_event_packet+0x4c5/0xf00
hci_rx_work+0x37d/0x880
process_one_work+0x77b/0x11c0
worker_thread+0x544/0x1180
kthread+0x285/0x320
ret_from_fork+0x22/0x30

Freed by task 269:
kasan_save_stack+0x26/0x50
kasan_set_track+0x25/0x40
kasan_set_free_info+0x24/0x40
____kasan_slab_free+0x176/0x1c0
__kasan_slab_free+0x12/0x20
slab_free_freelist_hook+0x95/0x1a0
kfree+0xba/0x2f0
hci_cmd_sync_clear+0x14c/0x210
hci_unregister_dev+0xff/0x440
vhci_release+0x7b/0xf0
__fput+0x1f3/0x970
____fput+0xe/0x20
task_work_run+0xd4/0x160
do_exit+0x8b0/0x22a0
do_group_exit+0xba/0x2a0
get_signal+0x1e4a/0x25b0
arch_do_signal_or_restart+0x93/0x1f80
exit_to_user_mode_prepare+0xf5/0x1a0
syscall_exit_to_user_mode+0x26/0x50
ret_from_fork+0x15/0x30

Fixes: 6a98e3836fa2 ("Bluetooth: Add helper for serialized HCI command execution")
Cc: stable@vger.kernel.org
Signed-off-by: Min Li <lm0963hack@gmail.com>
Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 83ce39248d6dd78db72525a52733ac1b392bb151 https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git master)

BUG=chromium:1413031
TEST=build

Signed-off-by: Archie Pusaka <apusaka@chromium.org>
Change-Id: I266e7233cc9164b1b3243ed510251ebef9602b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4334999
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Yun-Hao Chung <howardchung@chromium.org>

[modify] https://crrev.com/a68f975689e424739a95277141bbb2f37c89a9fc/net/bluetooth/hci_sync.c


### ap...@chromium.org (2023-03-16)

Related patches all merged, assigning back to you enlightened@

### ap...@chromium.org (2023-03-16)

[Empty comment from Monorail migration]

### en...@google.com (2023-03-21)

Assigning back to fixer and marking as fixed.

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### ro...@google.com (2023-03-28)

@ lm0963hack@gmail.com were you actually able to exploit this bug on ChromeOS given Chrome OS does not allow arbitrary code execution? Your proof of concept requires CAP_NET_ADMIN and expands the time window in order to reproduce the bug. 

### lm...@gmail.com (2023-03-29)

re #23

> were you actually able to exploit this bug on ChromeOS 
No, I don't have a exp to get root shell via this bug.

> given Chrome OS does not allow arbitrary code execution?
According to the vrp page, this bug should be evaluated in developer mode to create proper starting conditions. It is a priviledge escape bug, not a remote code execution bug.

"Reports that break individual layers without including a vector to trigger the bug via a web page or a malicious app may be evaluated in developer mode to create the appropriate starting condition."

> Your proof of concept requires CAP_NET_ADMIN and expands the time window in order to reproduce the bug.
The CAP_NET_ADMIN requirement may be satisfied by creating new namespace via unshare. The purpose of expanding the time window is to make it easier to reproduce the bug. In many race condition reports, the time window is manually expanded too, for example https://bugs.chromium.org/p/project-zero/issues/detail?id=2373

### pa...@chromium.org (2023-04-25)

The `msleep` for the PoC is a normal part of writing a PoC.

Requiring CAP_NET_ADMIN for exploitation means that the bar to exploitation is on the high side; e.g. web renderer → priv esc to something with the ability to call `unshare`, or otherwise get CAP_NET_ADMIN → kernel via this bug. (I don't think you can call `unshare` in a renderer, but I could be wrong.)

As discussed in other bugs of this type, that is a legitimate attack path but is high-cost. I suggest Medium as the ceiling for severity, but it could be Low if the middle step is relatively easy to achieve.

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-28)

Congratulations! The VRP Panel has decided to award you $7500 for this report + $1000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-28)

This issue was migrated from crbug.com/chromium/1413031?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062919)*
