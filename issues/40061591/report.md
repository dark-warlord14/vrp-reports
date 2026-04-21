# Security:  UAF in device_del

| Field | Value |
|-------|-------|
| **Issue ID** | [40061591](https://issues.chromium.org/issues/40061591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ap...@chromium.org |
| **Created** | 2022-11-04 |
| **Bounty** | $5,000.00 |

## Description

The hci\_error\_reset and hci\_rx\_work are two worker threads, so there is a possibility of race conditions. hci\_error\_reset will eventually call device\_del, hci\_rx\_work will eventually call device\_add, so there is a race condition vulnerability between [0] and [1],[2]

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/base/core.c;l=3571>  

int device\_add(struct device \*dev)  

{  

struct device \*parent;  

struct kobject \*kobj;  

struct class\_interface \*class\_intf;  

int error = -EINVAL;  

struct kobject \*glue\_dir = NULL;

```
dev = get_device(dev);  
if (!dev)  
	goto done;  

if (!dev->p) {  
	error = device_private_init(dev);  
	if (error)  
		goto done;  
}  

/\*  
 \* for statically allocated devices, which should all be converted  
 \* some day, we need to initialize the name. We prevent reading back  
 \* the name, and force the use of dev_name()  
 \*/  
if (dev->init_name) {  
	dev_set_name(dev, "%s", dev->init_name);  
	dev->init_name = NULL;  
}  

/\* subsystems can specify simple device enumeration \*/  
if (!dev_name(dev) && dev->bus && dev->bus->dev_name)  
	dev_set_name(dev, "%s%u", dev->bus->dev_name, dev->id);  

if (!dev_name(dev)) {  
	error = -EINVAL;  
	goto name_error;  
}  

pr_debug("device: '%s': %s\n", dev_name(dev), __func__);  

parent = get_device(dev->parent);  
kobj = get_device_parent(dev, parent);  
if (IS_ERR(kobj)) {  
	error = PTR_ERR(kobj);  
	goto parent_error;  
}  
if (kobj)  
	dev->kobj.parent = kobj;  

/\* use parent numa_node \*/  
if (parent && (dev_to_node(dev) == NUMA_NO_NODE))  
	set_dev_node(dev, dev_to_node(parent));  

/\* first, register with generic layer. \*/  
/\* we require the name to be set before, and pass NULL \*/  
error = kobject_add(&dev->kobj, dev->kobj.parent, NULL);  
if (error) {  
	glue_dir = get_glue_dir(dev);  
	goto Error;  
}  

/\* notify platform of device entry \*/  
device_platform_notify(dev);  

error = device_create_file(dev, &dev_attr_uevent);  
if (error)  
	goto attrError;  

error = device_add_class_symlinks(dev);  
if (error)  
	goto SymlinkError;  
error = device_add_attrs(dev);  
if (error)  
	goto AttrsError;  
error = bus_add_device(dev);  
if (error)  
	goto BusError;  
error = dpm_sysfs_add(dev);  
if (error)  
	goto DPMError;  
device_pm_add(dev);  

if (MAJOR(dev->devt)) {  
	error = device_create_file(dev, &dev_attr_dev);  
	if (error)  
		goto DevAttrError;  

	error = device_create_sys_dev_entry(dev);  
	if (error)  
		goto SysEntryError;  

	devtmpfs_create_node(dev);  
}  

/\* Notify clients of device addition.  This call must come  
 \* after dpm_sysfs_add() and before kobject_uevent().  
 \*/  
if (dev->bus)  
	blocking_notifier_call_chain(&dev->bus->p->bus_notifier,  
				     BUS_NOTIFY_ADD_DEVICE, dev);  

kobject_uevent(&dev->kobj, KOBJ_ADD);  

/\*  
 \* Check if any of the other devices (consumers) have been waiting for  
 \* this device (supplier) to be added so that they can create a device  
 \* link to it.  
 \*  
 \* This needs to happen after device_pm_add() because device_link_add()  
 \* requires the supplier be registered before it's called.  
 \*  
 \* But this also needs to happen before bus_probe_device() to make sure  
 \* waiting consumers can link to it before the driver is bound to the  
 \* device and the driver sync_state callback is called for this device.  
 \*/  
if (dev->fwnode && !dev->fwnode->dev) {  
	dev->fwnode->dev = dev;  
	fw_devlink_link_device(dev);  
}  

bus_probe_device(dev);  

/\*  
 \* If all driver registration is done and a newly added device doesn't  
 \* match with any driver, don't block its consumers from probing in  
 \* case the consumer device is able to operate without this supplier.  
 \*/  
if (dev->fwnode && fw_devlink_drv_reg_done && !dev->can_match)  
	fw_devlink_unblock_consumers(dev);  

if (parent)  
	klist_add_tail(&dev->p->knode_parent,  
		       &parent->p->klist_children);  

if (dev->class) {  
	mutex_lock(&dev->class->p->mutex);  
	/\* tie the class to the device \*/  
	klist_add_tail(&dev->p->knode_class,  
		       &dev->class->p->klist_devices);  

	/\* notify any interfaces that the device is here \*/  
	list_for_each_entry(class_intf,  
			    &dev->class->p->interfaces, node)  
		if (class_intf->add_dev)  
			class_intf->add_dev(dev, class_intf);  
	mutex_unlock(&dev->class->p->mutex);  
}  

```

done:  

put\_device(dev);  

return error;  

SysEntryError:  

if (MAJOR(dev->devt))  

device\_remove\_file(dev, &dev\_attr\_dev);  

DevAttrError:  

device\_pm\_remove(dev);  

dpm\_sysfs\_remove(dev);  

DPMError:  

bus\_remove\_device(dev);  

BusError:  

device\_remove\_attrs(dev);  

AttrsError:  

device\_remove\_class\_symlinks(dev);  

SymlinkError:  

device\_remove\_file(dev, &dev\_attr\_uevent);  

attrError:  

device\_platform\_notify\_remove(dev);  

kobject\_uevent(&dev->kobj, KOBJ\_REMOVE);  

glue\_dir = get\_glue\_dir(dev);  

kobject\_del(&dev->kobj);  

Error:  

cleanup\_glue\_dir(dev, glue\_dir);  

parent\_error:  

put\_device(parent);  

name\_error:  

kfree(dev->p); //[0]  

dev->p = NULL;  

goto done;  

}  

**-------------------------** ----------------

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/drivers/base/core.c;l=3659>

void device\_del(struct device \*dev)  

{  

struct device \*parent = dev->parent;  

struct kobject \*glue\_dir = NULL;  

struct class\_interface \*class\_intf;  

unsigned int noio\_flag;

```
device_lock(dev);  
kill_device(dev);  
device_unlock(dev);  

if (dev->fwnode && dev->fwnode->dev == dev)  
	dev->fwnode->dev = NULL;  

/\* Notify clients of device removal.  This call must come  
 \* before dpm_sysfs_remove().  
 \*/  
noio_flag = memalloc_noio_save();  
if (dev->bus)  
	blocking_notifier_call_chain(&dev->bus->p->bus_notifier,  
				     BUS_NOTIFY_DEL_DEVICE, dev);  

dpm_sysfs_remove(dev);  
if (parent)  
	klist_del(&dev->p->knode_parent);  //[1]  
if (MAJOR(dev->devt)) {  
	devtmpfs_delete_node(dev);  
	device_remove_sys_dev_entry(dev);  
	device_remove_file(dev, &dev_attr_dev);  
}  
if (dev->class) {  
	device_remove_class_symlinks(dev);  

	mutex_lock(&dev->class->p->mutex);  
	/\* notify any interfaces that the device is now gone \*/  
	list_for_each_entry(class_intf,  
			    &dev->class->p->interfaces, node)  
		if (class_intf->remove_dev)  
			class_intf->remove_dev(dev, class_intf);  
	/\* remove the device from the class list \*/  
	klist_del(&dev->p->knode_class);  //[2]  
	mutex_unlock(&dev->class->p->mutex);  
}  
device_remove_file(dev, &dev_attr_uevent);  
device_remove_attrs(dev);  
bus_remove_device(dev);  
device_pm_remove(dev);  
driver_deferred_probe_del(dev);  
device_platform_notify_remove(dev);  
device_links_purge(dev);  

if (dev->bus)  
	blocking_notifier_call_chain(&dev->bus->p->bus_notifier,  
				     BUS_NOTIFY_REMOVED_DEVICE, dev);  
kobject_uevent(&dev->kobj, KOBJ_REMOVE);  
glue_dir = get_glue_dir(dev);  
kobject_del(&dev->kobj);  
cleanup_glue_dir(dev, glue_dir);  
memalloc_noio_restore(noio_flag);  
put_device(parent);  

```

}

work thread 1 work thread2  

------------------ |--------------------  

|  

hci\_rx\_work | hci\_error\_reset  

|  

...... | ......  

|  

device\_add | device\_del  

kfree(dev->p)//[0] | klist\_del(&dev->p->knode\_parent)//[1]  

| klist\_del(&dev->p->knode\_class); //[2]  

|  

|

==================================================================  

BUG: KASAN: use-after-free in \_\_list\_del\_entry\_valid+0xf2/0x110 lib/list\_debug.c:59  

Read of size 8 at addr ffff888044e0ec68 by task kworker/u5:1/1226

CPU: 1 PID: 1226 Comm: kworker/u5:1 Not tainted 6.0.0-rc6 #10  

Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS 1.15.0-1 04/01/2014  

Workqueue: hci2 hci\_error\_reset  

Call Trace:  

<TASK>  

\_\_dump\_stack lib/dump\_stack.c:88 [inline]  

dump\_stack\_lvl+0xcd/0x134 lib/dump\_stack.c:106  

print\_address\_description mm/kasan/report.c:317 [inline]  

print\_report.cold+0x2ba/0x6e9 mm/kasan/report.c:433  

kasan\_report+0xb1/0x1e0 mm/kasan/report.c:495  

\_\_list\_del\_entry\_valid+0xf2/0x110 lib/list\_debug.c:59  

\_\_list\_del\_entry include/linux/list.h:134 [inline]  

list\_del include/linux/list.h:148 [inline]  

klist\_release+0x66/0x480 lib/klist.c:189  

kref\_put include/linux/kref.h:65 [inline]  

klist\_dec\_and\_del lib/klist.c:206 [inline]  

klist\_put+0x151/0x1d0 lib/klist.c:217  

device\_del+0x243/0xc80 drivers/base/core.c:3683  

hci\_conn\_del\_sysfs+0xdc/0x180 net/bluetooth/hci\_sysfs.c:78  

hci\_conn\_cleanup+0x315/0x7b0 net/bluetooth/hci\_conn.c:147  

hci\_conn\_del+0x29b/0x790 net/bluetooth/hci\_conn.c:1022  

hci\_conn\_hash\_flush+0x197/0x260 net/bluetooth/hci\_conn.c:2367  

hci\_dev\_close\_sync+0x55d/0x1130 net/bluetooth/hci\_sync.c:4476  

hci\_dev\_do\_close+0x2d/0x70 net/bluetooth/hci\_core.c:554  

hci\_error\_reset+0x96/0x130 net/bluetooth/hci\_core.c:1050  

process\_one\_work+0x991/0x1610 kernel/workqueue.c:2289  

worker\_thread+0x665/0x1080 kernel/workqueue.c:2436  

kthread+0x2e4/0x3a0 kernel/kthread.c:376  

ret\_from\_fork+0x1f/0x30 arch/x86/entry/entry\_64.S:306  

</TASK>

Allocated by task 17100:  

kasan\_save\_stack+0x1e/0x40 mm/kasan/common.c:38  

kasan\_set\_track mm/kasan/common.c:45 [inline]  

set\_alloc\_info mm/kasan/common.c:437 [inline]  

\_\_\_\_kasan\_kmalloc mm/kasan/common.c:516 [inline]  

\_\_\_\_kasan\_kmalloc mm/kasan/common.c:475 [inline]  

\_\_kasan\_kmalloc+0xa6/0xd0 mm/kasan/common.c:525  

kasan\_kmalloc include/linux/kasan.h:234 [inline]  

kmem\_cache\_alloc\_trace+0x25a/0x460 mm/slab.c:3559  

kmalloc include/linux/slab.h:600 [inline]  

kzalloc include/linux/slab.h:733 [inline]  

device\_private\_init drivers/base/core.c:3361 [inline]  

device\_add+0x1168/0x1e90 drivers/base/core.c:3411  

hci\_conn\_add\_sysfs+0x9b/0x1b0 net/bluetooth/hci\_sysfs.c:53  

hci\_conn\_complete\_evt+0x323/0xe50 net/bluetooth/hci\_event.c:3164  

hci\_event\_func net/bluetooth/hci\_event.c:7443 [inline]  

hci\_event\_packet+0x952/0xfd0 net/bluetooth/hci\_event.c:7495  

hci\_rx\_work+0xae7/0x1230 net/bluetooth/hci\_core.c:4007  

process\_one\_work+0x991/0x1610 kernel/workqueue.c:2289  

worker\_thread+0x665/0x1080 kernel/workqueue.c:2436  

kthread+0x2e4/0x3a0 kernel/kthread.c:376  

ret\_from\_fork+0x1f/0x30 arch/x86/entry/entry\_64.S:306

Freed by task 17327:  

kasan\_save\_stack+0x1e/0x40 mm/kasan/common.c:38  

kasan\_set\_track+0x21/0x30 mm/kasan/common.c:45  

kasan\_set\_free\_info+0x20/0x30 mm/kasan/generic.c:370  

\_\_\_\_kasan\_slab\_free mm/kasan/common.c:367 [inline]  

\_\_\_\_kasan\_slab\_free+0x13d/0x1a0 mm/kasan/common.c:329  

kasan\_slab\_free include/linux/kasan.h:200 [inline]  

\_\_cache\_free mm/slab.c:3418 [inline]  

kfree+0x173/0x390 mm/slab.c:3786  

device\_add+0x453/0x1e90 drivers/base/core.c:3571  

hci\_conn\_add\_sysfs+0x9b/0x1b0 net/bluetooth/hci\_sysfs.c:53  

hci\_le\_cis\_estabilished\_evt+0x57c/0xae0 net/bluetooth/hci\_event.c:6799  

hci\_le\_meta\_evt+0x2b8/0x510 net/bluetooth/hci\_event.c:7110  

hci\_event\_func net/bluetooth/hci\_event.c:7440 [inline]  

hci\_event\_packet+0x63d/0xfd0 net/bluetooth/hci\_event.c:7495  

hci\_rx\_work+0xae7/0x1230 net/bluetooth/hci\_core.c:4007  

process\_one\_work+0x991/0x1610 kernel/workqueue.c:2289  

worker\_thread+0x665/0x1080 kernel/workqueue.c:2436  

kthread+0x2e4/0x3a0 kernel/kthread.c:376  

ret\_from\_fork+0x1f/0x30 arch/x86/entry/entry\_64.S:306

The buggy address belongs to the object at ffff888044e0ec00  

which belongs to the cache kmalloc-512 of size 512  

The buggy address is located 104 bytes inside of  

512-byte region [ffff888044e0ec00, ffff888044e0ee00)

The buggy address belongs to the physical page:  

page:000000007aeba50a refcount:1 mapcount:0 mapping:0000000000000000 index:0x0 pfn:0x44e0c  

head:000000007aeba50a order:2 compound\_mapcount:0 compound\_pincount:0  

flags: 0xfff00000010200(slab|head|node=0|zone=1|lastcpupid=0x7ff)  

raw: 00fff00000010200 ffffea0001132600 dead000000000002 ffff888011841c80  

raw: 0000000000000000 0000000000100010 00000001ffffffff 0000000000000000  

page dumped because: kasan: bad access detected

Memory state around the buggy address:  

ffff888044e0eb00: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

ffff888044e0eb80: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc

> ffff888044e0ec00: fa fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb  
> 
> ^  
> 
> ffff888044e0ec80: fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb  
> 
> ffff888044e0ed00: fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb fb  
> 
> ==================================================================

This is another Bluetooth bug, a little different from <https://crbug.com/chromium/1355718>. The fix is to lock the thread when it is freed.

## Timeline

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-11-07)

Putting this is the ChromeOS security bug queue.

### en...@google.com (2022-11-08)

groeck@ I was told to bring this to your attention. I'm not sure who to assign it to as the code is not from anyone internal.

### ha...@gmail.com (2022-11-08)

This may could be assign to apusaka@.

### gr...@chromium.org (2022-11-09)

Excellent writeup and analysis. Similar bugs, found and reported by syyzbot: b/251203572; b/251210507; b/251812386; b/244141951, and more. Most if not all of those should have been reported upstream.


### gr...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-09)

Thanks for sure, hope this writeup helps you.

### en...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### en...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-30)

Any update?

### ap...@chromium.org (2022-11-30)

Not really any. I rarely work on kernels these days and priority is set to 3. Is this urgent?

So I took a look today but I found both the crashing task and the freeing task actually has hci_dev_lock, so not sure what's causing the crash.

int hci_dev_close_sync(struct hci_dev *hdev)
{
	...
	hci_dev_lock(hdev);

	hci_discovery_set_state(hdev, DISCOVERY_STOPPED);

	auto_off = hci_dev_test_and_clear_flag(hdev, HCI_AUTO_OFF);

	if (!auto_off && hdev->dev_type == HCI_PRIMARY &&
	    !hci_dev_test_flag(hdev, HCI_USER_CHANNEL) &&
	    hci_dev_test_flag(hdev, HCI_MGMT))
		__mgmt_power_off(hdev);

	hci_inquiry_cache_flush(hdev);
	hci_pend_le_actions_clear(hdev);
	hci_conn_hash_flush(hdev);              // <-- CRASHING STACKTRACE
	/* Prevent data races on hdev->smp_data or hdev->smp_bredr_data */
	smp_unregister(hdev);
	hci_dev_unlock(hdev);
	...
}

static void hci_le_cis_estabilished_evt(struct hci_dev *hdev, void *data,
					struct sk_buff *skb)
{
	...
	hci_dev_lock(hdev);
	...
	if (!ev->status) {
		conn->state = BT_CONNECTED;
		hci_debugfs_create_conn(conn);
		hci_conn_add_sysfs(conn);                 // <-- FREEING STACKTRACE
		hci_iso_setup_path(conn);
		goto unlock;
	}

	hci_connect_cfm(conn, ev->status);
	hci_conn_del(conn);

unlock:
	hci_dev_unlock(hdev);
}

### gr...@chromium.org (2022-11-30)

This has nothing to do with locks. The problem may be fixed (or concealed) with upstream commit 448a496f7606 ("Bluetooth: hci_sysfs: Fix attempting to call device_add multiple times").


### ha...@gmail.com (2022-11-30)

The dev should be protected by device_lock, not  hci_dev_lock.


void device_del(struct device *dev)
{
	struct device *parent = dev->parent;
	struct kobject *glue_dir = NULL;
	struct class_interface *class_intf;
	unsigned int noio_flag;

	device_lock(dev);
	kill_device(dev);
	device_unlock(dev);
......
	if (parent)
		klist_del(&dev->p->knode_parent);  //[1]

### ap...@chromium.org (2022-11-30)

If the problematic section of the code lies in drivers/base/core, probably it's outside the bluetooth domain and I won't be an ideal owner for the issue.

### ha...@gmail.com (2022-11-30)

Yes, access to exploit code via bluetooth code

### gr...@chromium.org (2022-11-30)

#15: This is incorrect. The problem lies in te bluetooth code which tries to create the same sysfs attribute several times. Blaming the driver core is wrong. Again, see upstream commit 448a496f7606.


### gr...@chromium.org (2022-11-30)

448a496f7606 should address the symptoms of this problem. It won't address the root cause; that is hidden somewhere in the bluetooth code. The error handler is known to be racy, and the bluetooth code should under no circumstance attempt to create the same sysfs attribute file twice.


### ha...@gmail.com (2022-12-02)

Yep,448a496f7606 should fix this issue.

### ha...@gmail.com (2022-12-02)

Just merge this fix

### ap...@chromium.org (2023-02-28)

448a496f7606 was merged around end of Oct 2022.

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### al...@google.com (2023-03-17)

We havent cherry-picked the fix so this is only fixed on the v6.1 branch and later.

### al...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### al...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### gr...@chromium.org (2023-03-17)

Upstream commit 448a496f760 ("Bluetooth: hci_sysfs: Fix attempting to call device_add multiple times")
  Integrated in v6.1-rc1
  Fixed in chromeos-5.15 with merge of v5.15.75 (sha 3423a50fa018)
    Not in R102, R108
    In R110, R111, R112
  Fixed in chromeos-5.10 with merge of v5.10.150 (sha 7b674dce4162)
    Not in R102, R108
    In R110, R111, R112
  Fixed in chromeos-5.4 with merge of v5.4.220 (sha 6e85d2ad958c)
    Not in R102, R108
    In R110, R111, R112
  Fixed in chromeos-4.19 with merge of v4.19.262 (sha 671fee73e08f)
    Not in R102, R108
    In R110, R111, R112
  Fixed in chromeos-4.14 with merge of v4.14.296 (sha 6144423712d5)
    Not in R102, R108
    In R110, R111, R112

### al...@google.com (2023-03-17)

You are right that we have the first patch in the series, I was searching for the second patch in the series:
https://lore.kernel.org/all/20220921055026.380196-1-yin31149@gmail.com/t/
https://chromium.git.corp.google.com/chromiumos/third_party/kernel/+/7096daba731eea262e0f7bf03453ceddcad89f70%5E%21/#F0

```
diff --git a/net/bluetooth/hci_debugfs.c b/net/bluetooth/hci_debugfs.c
index 902b40a9..3f401ec 100644
--- a/net/bluetooth/hci_debugfs.c
+++ b/net/bluetooth/hci_debugfs.c
@@ -1245,7 +1245,7 @@
 	struct hci_dev *hdev = conn->hdev;
 	char name[6];
 
-	if (IS_ERR_OR_NULL(hdev->debugfs))
+	if (IS_ERR_OR_NULL(hdev->debugfs) || conn->debugfs)
 		return;
 
 	snprintf(name, sizeof(name), "%u", conn->handle);
```

### ro...@google.com (2023-03-28)

@hackyzh002@gmail.com I am a little unclear on this report. I don't see that you were able to reproduce this on ChromeOS given that ChromeOS doesn't allow arbitrary code execution. Is there a POC I am missing?

Also it looks like this was fixed upstream before it was reported to us.

### ha...@gmail.com (2023-03-29)

This vulnerability appeared when I was fuzzing, so there is no poc restoration. And there is a vuln when I am fuzzing, it should be fixed in the later version

### ha...@gmail.com (2023-03-29)

And this is a local kernel privilege escalation vulnerability, not a code execution vulnerability. The key point is to escalate privileges. Only developers who use root to grant code execution permissions can execute this exploit. Or cooperate with the chrome sandbox to escape and execute this vulnerability to perform privilege escalation operations

### al...@google.com (2023-04-13)

We need to figure out if we need to merge back the commit in https://crbug.com/chromium/1381375#c28

### gr...@chromium.org (2023-04-13)

Oh, lets just take it. It is just a small patch with no risk involved, after all. I'll submit CLs.


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/4443ca899b3fd9826ce24ee5cb1288b45a418c1b

commit 4443ca899b3fd9826ce24ee5cb1288b45a418c1b
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4425255
Reviewed-by: Archie Pusaka <apusaka@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/4443ca899b3fd9826ce24ee5cb1288b45a418c1b/net/bluetooth/hci_debugfs.c


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/c683a821b835fe71d52bb06d6e9dae07d47ce5b0

commit c683a821b835fe71d52bb06d6e9dae07d47ce5b0
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4422204
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Archie Pusaka <apusaka@chromium.org>

[modify] https://crrev.com/c683a821b835fe71d52bb06d6e9dae07d47ce5b0/net/bluetooth/hci_debugfs.c


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/da7f077e80603c566f5ab6d3af15124cd559aadb

commit da7f077e80603c566f5ab6d3af15124cd559aadb
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4425254
Reviewed-by: Archie Pusaka <apusaka@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/da7f077e80603c566f5ab6d3af15124cd559aadb/net/bluetooth/hci_debugfs.c


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/45a30c4082a5c516cce65910de0b07a8807b56ae

commit 45a30c4082a5c516cce65910de0b07a8807b56ae
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4425252
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Archie Pusaka <apusaka@chromium.org>

[modify] https://crrev.com/45a30c4082a5c516cce65910de0b07a8807b56ae/net/bluetooth/hci_debugfs.c


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/c683a821b835fe71d52bb06d6e9dae07d47ce5b0

commit c683a821b835fe71d52bb06d6e9dae07d47ce5b0
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4422204
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Archie Pusaka <apusaka@chromium.org>

[modify] https://crrev.com/c683a821b835fe71d52bb06d6e9dae07d47ce5b0/net/bluetooth/hci_debugfs.c


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/45a30c4082a5c516cce65910de0b07a8807b56ae

commit 45a30c4082a5c516cce65910de0b07a8807b56ae
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4425252
Reviewed-by: Sean Paul <sean@poorly.run>
Reviewed-by: Archie Pusaka <apusaka@chromium.org>

[modify] https://crrev.com/45a30c4082a5c516cce65910de0b07a8807b56ae/net/bluetooth/hci_debugfs.c


### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/kernel/+/52f163e37505b1c1e2ab5d1ddef0cb940e84650a

commit 52f163e37505b1c1e2ab5d1ddef0cb940e84650a
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date: Mon Sep 19 17:57:00 2022

UPSTREAM: Bluetooth: hci_debugfs: Fix not checking conn->debugfs

hci_debugfs_create_conn shall check if conn->debugfs has already been
created and don't attempt to overwrite it.

Signed-off-by: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
(cherry picked from commit 7096daba731eea262e0f7bf03453ceddcad89f70)

BUG=chromium:1381375
TEST=CQ

Change-Id: If6bae934244d2642c91c9f0066b374a08274ee3f
Disallow-Recycled-Builds: test-failures
Signed-off-by: Guenter Roeck <groeck@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/kernel/+/4425253
Reviewed-by: Archie Pusaka <apusaka@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>

[modify] https://crrev.com/52f163e37505b1c1e2ab5d1ddef0cb940e84650a/net/bluetooth/hci_debugfs.c


### ha...@gmail.com (2023-04-20)

please change the status

### ch...@google.com (2023-05-23)

Since already merged, I'll mark as closed/fixed

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### al...@google.com (2023-06-06)

IIUC this requires winning a race based on when devices are added. What would it take for the attacker to reach this? Is it during probe, pairing, etc?

### ha...@google.com (2023-06-27)

Chatted with apusaka@ offline -- A device can also have multiple bluetooth connections and trigger add, which may trigger the race between add and delete.  Feel free to add any more context. 

From what I understand, https://crbug.com/chromium/1381375#c19, 448a496f7606 fixed this issue and was merged to chromeOS before this report. 
The reason we have more CLs is because the issue that 448a496f7606 was a part of has multiple CLs, so did cherry-picked that as well. There is no POC here as well.

### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

Congratulations Zhihua Yao! The VRP Panel has decided to award you $5,000 for this report of a security issue in the kernel mitigated by precondition of pairing the bluetooth device. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-29)

This issue was migrated from crbug.com/chromium/1381375?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061591)*
