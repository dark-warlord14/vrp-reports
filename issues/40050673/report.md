# Heap-use-after-free in WebBluetoothServiceImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40050673](https://issues.chromium.org/issues/40050673) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bluetooth |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | xb...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2019-11-13 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36

Steps to reproduce the problem:
There is an object life-cycle issue in web_bluetooth_service. I think the main reason is that there is a raw pointer of BluetoothAdapter pass to asynchronous task(WebBluetoothServiceImpl::RequestDeviceImpl) and finally own by BluetoothDeviceChooserController. 

If the two objects have inconsistent life cycles, there will be security risks. We can trigger this vulnerability via the mojo interface of Bluetooth. A compromised renderer can exploit this vulnerability to achieve sandbox escape. 

For laptops with a Bluetooth adapter(very common, and don't need to turn on Bluetooth), the success rate is very high. This logic can be triggered by mojo even without a Bluetooth adapter, So even a desktop computer without a Bluetooth adapter can be triggered by modifying the poc.

TESTED VERSION
Google Chrome 78.0.3904.70 (Official Build) (64-bit)
Chromium 80.0.3948.0, 79.0.3923.0, 78.0.3895.0 (Developer Build) (64-bit)
Operating System: Windows 10 version 1803 (OS build 17134.1099)

DETAILS
#################################################################

# Mojo Interface: 
# WebBluetoothServiceImpl::RequestDevice
# https://cs.chromium.org/chromium/src/content/browser/bluetooth/web_bluetooth_service_impl.cc?type=cs&q=WebBluetoothServiceImpl::RequestDevice&g=0&l=662
################################################################
void WebBluetoothServiceImpl::RequestDevice(
    blink::mojom::WebBluetoothRequestDeviceOptionsPtr options,
    RequestDeviceCallback callback) {
  RecordRequestDeviceOptions(options);

  if (!GetAdapter()) {
    if (BluetoothAdapterFactoryWrapper::Get().IsLowEnergySupported()) {
      BluetoothAdapterFactoryWrapper::Get().AcquireAdapter(                        
          this, base::BindOnce(&WebBluetoothServiceImpl::RequestDeviceImpl,    <== Trigger an asynchronous call (RequestDeviceImpl)
                               weak_ptr_factory_.GetWeakPtr(),
                               std::move(options), std::move(callback)));
      return;
    }
    RecordRequestDeviceOutcome(
        UMARequestDeviceOutcome::BLUETOOTH_LOW_ENERGY_NOT_AVAILABLE);
    std::move(callback).Run(
        blink::mojom::WebBluetoothResult::BLUETOOTH_LOW_ENERGY_NOT_AVAILABLE,
        nullptr /* device */);
    return;
  }
  RequestDeviceImpl(std::move(options), std::move(callback), GetAdapter());    
}

# Raw Pointer Passing - pass to the task (WebBluetoothServiceImpl::RequestDeviceImpl)
# https://cs.chromium.org/chromium/src/device/bluetooth/bluetooth_adapter_factory_wrapper.cc?type=cs&g=0&l=46
################################################################
scoped_refptr<BluetoothAdapter> adapter_;
callback  <====>  WebBluetoothServiceImpl::RequestDeviceImpl

void BluetoothAdapterFactoryWrapper::AcquireAdapter(
    BluetoothAdapter::Observer* observer,
    AcquireAdapterCallback callback) {
  DCHECK(thread_checker_.CalledOnValidThread());
  DCHECK(!GetAdapter(observer));

  AddAdapterObserver(observer);
  if (adapter_.get()) {
    base::ThreadTaskRunnerHandle::Get()->PostTask(
        FROM_HERE,
        base::BindOnce(std::move(callback), base::Unretained(adapter_.get())));   <== Got raw pointer and then post task
    return;
  }

  DCHECK(BluetoothAdapterFactory::Get().IsLowEnergySupported());
  BluetoothAdapterFactory::GetAdapter(
      base::BindOnce(&BluetoothAdapterFactoryWrapper::OnGetAdapter,
                     weak_ptr_factory_.GetWeakPtr(), std::move(callback)));
}

# Pass the raw pointer to BluetoothDeviceChooserController
# https://cs.chromium.org/chromium/src/content/browser/bluetooth/web_bluetooth_service_impl.cc?type=cs&q=WebBluetoothServiceImpl::RequestDeviceImpl&g=0&l=1354
###############################################################
BluetoothDeviceChooserController device::BluetoothAdapter* adapter_;

void WebBluetoothServiceImpl::RequestDeviceImpl
{
	...
	device_chooser_controller_.reset();
	device_chooser_controller_.reset(
		new BluetoothDeviceChooserController(this, render_frame_host_, adapter)); <=== adapter is raw pointer, now it own by device_chooser_controller_

	...
	device_chooser_controller_->GetDevice(
      std::move(options),
      base::Bind(&WebBluetoothServiceImpl::OnGetDeviceSuccess,
                 weak_ptr_factory_.GetWeakPtr(), copyable_callback),
      base::Bind(&WebBluetoothServiceImpl::OnGetDeviceFailed,
                 weak_ptr_factory_.GetWeakPtr(), copyable_callback))
}

# The life-cycle of BluetoothAdapter
# DidFinishNavigation to free adapter, So we can trigger the release of adapter by refreshing the page.
# https://cs.chromium.org/chromium/src/content/browser/bluetooth/web_bluetooth_service_impl.cc?type=cs&q=WebBluetoothServiceImpl::DidFinishNavigation&g=0&l=457
#################################################################
void WebBluetoothServiceImpl::DidFinishNavigation
   ===>
		void WebBluetoothServiceImpl::ClearState() {
		  .....
		  BluetoothAdapterFactoryWrapper::Get().ReleaseAdapter(this);
		}
		===> 
			void BluetoothAdapterFactoryWrapper::ReleaseAdapter(
				BluetoothAdapter::Observer* observer) {
			  DCHECK(thread_checker_.CalledOnValidThread());
			  if (!HasAdapter(observer)) {
				return;
			  }
			  RemoveAdapterObserver(observer);
			  if (adapter_observers_.empty())
				set_adapter(scoped_refptr<BluetoothAdapter>());    <==  free adapter
			}

# If the adapter is released, there are still some unprocessed tasks (WebBluetoothServiceImpl::RequestDeviceImpl), then The
# BluetoothDeviceChooserController uses adapter_ after adapter_ release, then UAF will occur.
# https://cs.chromium.org/chromium/src/content/browser/bluetooth/bluetooth_device_chooser_controller.cc?type=cs&q=BluetoothDeviceChooserController::GetDevice&g=0&l=263
#################################################################
void BluetoothDeviceChooserController::GetDevice
{
	...
    if (!adapter_->IsPresent()) {                                                    <===  UAF (device::BluetoothAdapter* adapter_)
    DVLOG(1) << "Bluetooth Adapter not present. Can't serve requestDevice.";
    RecordRequestDeviceOutcome(
        UMARequestDeviceOutcome::BLUETOOTH_ADAPTER_NOT_PRESENT);
    PostErrorCallback(WebBluetoothResult::NO_BLUETOOTH_ADAPTER);
    return;
  }
}

What is the expected behavior?

What went wrong?
# REPRODUCTION CASE

# [1] POC FOR CRASH (Test on a laptop with a Bluetooth adapter, Chromium 80.0.3948.0)
#################################################################
$ python ./copy_mojo_js_bindings.py E:\chromium_\src\out\gen
$ python -m SimpleHTTPServer&
$ E:\chromium_\src\out\release\chrome.exe --enable-blink-features=MojoJS --user-data-dir=D:\chrome\mojom\tmp\nonexist 

visit this webpage : 'http://127.0.0.1:8000/test_bluetooth.html' 

If the version is lower than 80.0.3948.0, you need to modify the all "Mojo.bindInterface(blink.mojom.WebBluetoothService.name, mojo.makeRequest(ptr).handle,"context", true)" to "Mojo.bindInterface(blink.mojom.WebBluetoothService.name, mojo.makeRequest(ptr).handle)"

Please see the attachment crash.txt and crash.png

# [2] EXP FOR HIJACKING VTABLE (Test on a laptop with a Bluetooth adapter, Chrome 64bit dev 80.0.3948.0)
#################################################################
After the object is released, we can use Blobs to allocate some heaps of the same size as adapter(size is 0x240), there is a chance that virtual table can be overwritten.

See attachment: exp_bluetooth.html and _trigger_bluetooth.html. The exploit code mainly hijacks the virtual table to 0x2323232323232323

$ python ./copy_mojo_js_bindings.py E:\chromium_\src\out\gen
$ python _local_http.py
$ E:\chromium_\src\out\release\chrome.exe --enable-blink-features=MojoJS --user-data-dir=D:\chrome\mojom\tmp\nonexist 

visit this webpage : 'http://127.0.0.1:8003/exp_bluetooth.html' 

If all goes well，after the trigger, the screenshot as follow (hijack.png). Can be used to achieve sandbox escape.
call    qword ptr [rax+38h] ds:23232323`2323235b=????????????????

# The strategy of hijacking virtual tables:
#################################################################
1. Need to create multiple WebBluetoothServiceImpl to bypass "if (!GetAdapter())";
2. Control the timing of subsequent by controlling the parameter "WebBluetoothRequestDeviceOptions of the WebBluetoothServiceImpl::RequestDevice function".
	2.1 Call the normal interface once, so that the adapter is created.
	2.2 First pass the parameter option_not_crash 3000 times, try to accumulate the queue, but will not run to the branch that will crash. 
	2.3 Then call the parameter option_delay_use for 100 times, through which the "BluetoothBlocklist::Get().RemoveExcludedUUIDs(options_.get())" logic enters the loop and delays the timing of the UAF, so that the released object is occupied by the heap spray and then used.

3. Release the object through the "document.location.replace" function, use the blob heap spray operation, wait for the UAF to hijack the virtual table.

After hijacking the virtual table, we can try to point the virtual table to the location where our shellcode is stored in memory, or use the function already loaded in the dll to hijack the control flow and finally execute the code.

# [3] EXP FOR SANDBOX ESCAPE WITHOUT ASLR (Win10 version 1803 (OS build 17134.1099) and Chrome 64bit dev 80.0.3948.0)
#################################################################
By using the compromised renderer, we can enable mojojs binding and we can get the base address of ntdll.dll/kernel32.dll, then use their rop gadgets. Combined with heap spray, we can execute code on 64-bit chrome without ASLR (On systems with ASLR enabled, code execution on 32-bit chrome should be possible by heap spray), complete the sandbox escape. 

See attachment: exp.html and _trigger_bluetooth.html.

$ python ./copy_mojo_js_bindings.py E:\chromium_\src\out\gen
$ python _local_http.py
$ E:\chromium_\src\out\release\chrome.exe --enable-blink-features=MojoJS --user-data-dir=D:\chrome\mojom\tmp\nonexist 

visit this webpage : 'http://127.0.0.1:8003/exp.html' 

If all goes well，the calculator program will be executed after the sandbox escapes. 

Did this work before? N/A 

Chrome version: 78.0.3904.70  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [test_bluetooth.html](attachments/test_bluetooth.html) (text/plain, 922 B)
- [crash.txt](attachments/crash.txt) (text/plain, 7.5 KB)
- [crash.png](attachments/crash.png) (image/png, 466.5 KB)
- [_local_http.py](attachments/_local_http.py) (text/plain, 592 B)
- [exp_bluetooth.html](attachments/exp_bluetooth.html) (text/plain, 2.5 KB)
- [_trigger_bluetooth.html](attachments/_trigger_bluetooth.html) (text/plain, 3.7 KB)
- [hijack.png](attachments/hijack.png) (image/png, 424.5 KB)
- deleted (application/octet-stream, 0 B)
- [exp_without_ASLR_win10_chrome_64bit_80.0.3948.0.mp4](attachments/exp_without_ASLR_win10_chrome_64bit_80.0.3948.0.mp4) (video/mp4, 3.1 MB)

## Timeline

### do...@chromium.org (2019-11-13)

Thanks - another compromised renderer can escape the sandbox vulnerability in Web Bluetooth.

reillyg/ortuno/dougt - can you take an urgent look at this?

[Monorail components: Blink>Bluetooth]

### re...@chromium.org (2019-11-13)

I have a fix for this out for review: https://chromium-review.googlesource.com/c/chromium/src/+/1914536

### do...@chromium.org (2019-11-14)

Upgrading to critical severity. We'll want a fix landed and merged to stable ASAP.

### aa...@google.com (2019-11-14)

[Empty comment from Monorail migration]

### aw...@google.com (2019-11-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a255d1be5723813c1a3e793b8388ed61edcea5b1

commit a255d1be5723813c1a3e793b8388ed61edcea5b1
Author: Reilly Grant <reillyg@chromium.org>
Date: Thu Nov 14 07:01:05 2019

Fix ownership of BluetoothAdapter in BluetoothDeviceChooserController

BluetoothAdapter is a reference counted object and so
BluetoothDeviceChooserController should own it using a scoped_refptr.
Fixing this requires also fixing BluetoothAdapterFactoryWrapper's
AcquireAdapterCallback to take a scoped_refptr rather than a raw
pointer. A test for proper ownership has been added.

Bug: 1024121
Change-Id: I6342322e059f9cbff2a0d5f073f6bccfb0ca7c36
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1914536
Reviewed-by: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#715206}

[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/content/browser/bluetooth/bluetooth_device_chooser_controller.cc
[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/content/browser/bluetooth/bluetooth_device_chooser_controller.h
[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/content/browser/bluetooth/web_bluetooth_service_impl.cc
[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/content/browser/bluetooth/web_bluetooth_service_impl.h
[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/content/browser/bluetooth/web_bluetooth_service_impl_unittest.cc
[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/device/bluetooth/bluetooth_adapter_factory_wrapper.cc
[modify] https://crrev.com/a255d1be5723813c1a3e793b8388ed61edcea5b1/device/bluetooth/bluetooth_adapter_factory_wrapper.h


### re...@google.com (2019-11-14)

I will verify this fix on the next canary build. Are we also planning a re-spin of M-78?

### sh...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-14)

Requesting merge to beta M79 because latest trunk commit (715206) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-14)

This bug requires manual review: M79's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-14)

CL listed at #6 is not in canary yet, please update bug with canary result tomorrow. 

### go...@chromium.org (2019-11-14)

Merged CL listed at #6 to current canary branches and triggered new canary

3966:  https://chromium.googlesource.com/chromium/src.git/+/12b0fa47c0ab1e69834ebaf0e4ac10650acbbc4d (Android and Mac)
3967: https://chromium.googlesource.com/chromium/src.git/+/ee9676976ecd8059f378dde4dfd8402fe5f61b26 (Windows)

Note: Latest 80.0.3967.0 either failed to build or not available for Android and mac, hence merged the change to 3966 branch and triggered new canary for Android and Mac from same branch.




### go...@chromium.org (2019-11-15)

Tentatively adding M78 labels for tracking purpose per internal mail thread. 

### go...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### aa...@google.com (2019-11-15)

Since these require a compromised renderer, moving these to High as per current severity ratings.

### sh...@chromium.org (2019-11-15)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-15)

How is the change looking in canary?

### re...@chromium.org (2019-11-15)

I'm investigating a regression in canary to determine if it is this change or another.

### go...@chromium.org (2019-11-15)

Per offline chat and mail thread, this change is merged to M78 branch 3904 - https://chromium.googlesource.com/chromium/src.git/+/471ac08ef7cd7e66765829550fa232ca0062f34c.
We will revert the change if this is the cause of regression in canary.

### go...@chromium.org (2019-11-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-18)

Approving merge to M79 branch 3945, please merge ASAP, thank you.

### ad...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-18)

Please merge your change to M79 branch 3945 ASAP so we can pick it up for this week Beta release. Thank you.

### go...@chromium.org (2019-11-19)

Please merge your change to M79 branch 3945 by 12:30 PM PT, today so we can pick it up for tomorrow's beta release. Thank you.

### re...@chromium.org (2019-11-19)

Bugdroid is being flaky again. Patch already merged: https://chromium-review.googlesource.com/c/chromium/src/+/1922283

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $20,000  for this report! 

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-11-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

reillyg@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### or...@chromium.org (2019-12-05)

Adding odejesush since reillyg is OOO

### mm...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/1024121?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050673)*
