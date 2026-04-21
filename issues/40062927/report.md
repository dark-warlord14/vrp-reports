# Security: Race Condition UAF in hci_cmd_sync_work(2)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062927](https://issues.chromium.org/issues/40062927) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | lm...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-02-06 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**

The root cause of this issue is similar to <https://crbug.com/chromium/1413031>, race condition UAF, and both in the some function. This vulnerability is actually the incomplete fix of commit 0b94f2651f56b9e4aa5f012b0d7eb57308c773cf

\*hci\_cmd\_sync\_queue\* will check the flag of hdev not equal to \*HCI\_UNREGISTER\*[1], and enqueue \*hdev->cmd\_sync\_work\*(which is \*hci\_cmd\_sync\_work\*)[2]. There is a time window between the check and queue\_work. If \*hci\_unregister\_dev\* is called in the time window, and \*cancel\_work\_sync\*[4] is executed before queue\_work[2], the hdev will be freed, and cause a uaf in \*hci\_cmd\_sync\_work\*.

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
  
void hci_unregister_dev(struct hci_dev \*hdev)  
{  
	BT_DBG("%p name %s bus %d", hdev, hdev->name, hdev->bus);  
  
	hci_dev_set_flag(hdev, HCI_UNREGISTER);		// [3]  
  
	write_lock(&hci_dev_list_lock);  
	list_del(&hdev->list);  
	write_unlock(&hci_dev_list_lock);  
  
	cancel_work_sync(&hdev->power_on);  
  
	hci_cmd_sync_clear(hdev);  
	......  
}  
  
void hci_cmd_sync_clear(struct hci_dev \*hdev)  
{  
	struct hci_cmd_sync_work_entry \*entry, \*tmp;  
  
	cancel_work_sync(&hdev->cmd_sync_work);		// [4]  
	cancel_work_sync(&hdev->reenable_adv_work);  
  
	list_for_each_entry_safe(entry, tmp, &hdev->cmd_sync_work_list, list) {  
		if (entry->destroy)  
			entry->destroy(hdev, entry->data, -ECANCELED);  
  
		list_del(&entry->list);  
		kfree(entry);  
	}  
}  

```

hci\_cmd\_sync\_queue | hci\_unregister\_dev  

hci\_dev\_test\_flag(hdev, HCI\_UNREGISTER) [1] |  

| hci\_dev\_set\_flag(hdev, HCI\_UNREGISTER) [3]  

| hci\_cmd\_sync\_clear  

| cancel\_work\_sync(&hdev->cmd\_sync\_work) [4]  

queue\_work [2] |  

hci\_cmd\_sync\_work <--- UAF

[1] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=689>  

[2] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=704>  

[3] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/upstream/net/bluetooth/hci_core.c;drc=ef7d6da42cd8e1417505f747346d8be6a31ba055;l=2708>  

[4] <https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.1/net/bluetooth/hci_sync.c;drc=72068db5f0db1775a858528cb9671af4ff5de422;l=643>

**VERSION**  

Operating System: ChromiumOS Kernel 6.1 stable + dev

Bisect:  

<https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/kernel/+/0b94f2651f56b9e4aa5f012b0d7eb57308c773cf>

**REPRODUCTION CASE**

The time window is very small, please apply the patch which just expands the time window.

```
diff --git a/net/bluetooth/hci_sync.c b/net/bluetooth/hci_sync.c  
index 2337a1c4827d..23835b8ca786 100644  
--- a/net/bluetooth/hci_sync.c  
+++ b/net/bluetooth/hci_sync.c  
@@ -279,7 +279,7 @@ static void hci_cmd_sync_work(struct work_struct \*work)  
        struct hci_dev \*hdev = container_of(work, struct hci_dev, cmd_sync_work);  
   
        bt_dev_dbg(hdev, "");  
-  
+       msleep(10);  
        /\* Dequeue all entries and run them \*/  
        while (1) {  
                struct hci_cmd_sync_work_entry \*entry;  
@@ -700,7 +700,7 @@ int hci_cmd_sync_queue(struct hci_dev \*hdev, hci_cmd_sync_work_func_t func,  
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
index 2337a1c4827d..365badd84beb 100644  
--- a/net/bluetooth/hci_sync.c  
+++ b/net/bluetooth/hci_sync.c  
@@ -703,6 +703,8 @@ int hci_cmd_sync_queue(struct hci_dev \*hdev, hci_cmd_sync_work_func_t func,  
   
        queue_work(hdev->req_workqueue, &hdev->cmd_sync_work);  
   
+       if (hci_dev_test_flag(hdev, HCI_UNREGISTER))  
+               cancel_work_sync(&hdev->cmd_sync_work);  
        return 0;  
 }  
 EXPORT_SYMBOL(hci_cmd_sync_queue);  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: kernel crash  

Crash State: please see the kasan.log

## Attachments

- [poc.c](attachments/poc.c) (text/plain, 9.1 KB)
- [kasan.log](attachments/kasan.log) (text/plain, 3.3 KB)

## Timeline

### [Deleted User] (2023-02-06)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-06)

=> to ChromeOS triage queue

### lz...@google.com (2023-02-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-02-15)

groeck@, could you please take a look? Thanks!

### gr...@chromium.org (2023-02-15)

The problem is quite obvious, but I am not a Bluetooth expert. Assigning it to me won't get it fixed. The patch looks wrong to me (it first queues work and then immediately cancels it) but, again, I am not a Bluetooth expert, and I don't know the code well enough to suggest a proper fix.

This should be submitted upstream (ie to security@kernel.org) if our Bluetooth team does not plan to address the problem. The fix should be submitted upstream either way. Quite frankly, maybe it should just be published. Maybe that would help to get someone who knows about the Bluetooth subsystem to look into the problem.

Also, please note that bugs against ChromeOS kernels should be submitted in buganizer. All ChromeOS specific information has been scrubbed from Monorail, and it is all but impossible to keep tracking kernel bugs there.

### lm...@gmail.com (2023-02-16)

Hi, I have submitted this to security@kernel.org for repair. If there is any new repair progress, I will sync it here.

### ch...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-04)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-14)

Dear lm0963hack@gmail.com,

Any progress here?

### lm...@gmail.com (2023-04-18)

Hi, sorry for the delay, still working on that.

### ch...@google.com (2023-04-19)

[Empty comment from Monorail migration]

[Monorail blocking: b/278827961]

### ch...@google.com (2023-04-19)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/278827961). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### ch...@google.com (2023-04-19)

Dear lm0963hack@gmail.com,

Please provide all upcoming updates in our new buganizer system:  https://issuetracker.google.com/issues/278827961

### ch...@google.com (2023-05-15)

Dear lm0963hack@gmail.com,

Can you please check the latest comments at  https://issuetracker.google.com/issues/278827961

### ch...@google.com (2023-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

chmiel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-06-12)

Marked as fixed.
Closing the bug as the patch is in bluetooth-next. (see https://crbug.com/chromium/1413104#c37 b/278827961)

### ch...@google.com (2023-06-12)

CLs:  ​crrev/c/4529175, crrev/c/4529176

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-06-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

Congratulations! The VRP Panel has decided to award you $4,000 for this report of this issue significantly mitigated by the race condition to the extent this issue was not able to be reproduced. Thank you for your efforts and reporting this issue to us as a follow-on issue of your previous report (1413031) and provided patch for that issue (https://git.kernel.org/pub/scm/linux/kernel/git/bluetooth/bluetooth-next.git/commit/?id=83ce39248d6d). 

### am...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-18)

This issue was migrated from crbug.com/chromium/1413104?no_tracker_redirect=1

[Monorail blocking: b/278827961]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062927)*
